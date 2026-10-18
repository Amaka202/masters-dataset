"""Reconstruct a small deterministic sample from upstream commit snapshots.

This checks provenance, code fidelity and published licence metadata. It does not
run project code or establish an independent gold-standard issue judgement.
"""

import argparse
import ast
import difflib
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import textwrap
from urllib.parse import quote
import warnings

from BUILD_CANDIDATE_SPLITS import normalise, production, save, sha


def fetch(url, cache):
    path = cache / ("probe-" + hashlib.sha256(url.encode()).hexdigest()[:24])
    if not path.exists():
        result = subprocess.run(["curl", "--location", "--fail-with-body", "--silent", "--show-error",
                                 "--max-time", "60", "--retry", "1", url], capture_output=True)
        if result.returncode:
            raise ValueError(f"HTTP retrieval failed: {result.stderr.decode()[:180]}")
        # Several candidate functions can share one source URL. Publish the
        # complete response atomically so another worker cannot parse a partial
        # file while a concurrent download truncates/writes the cache entry.
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(dir=cache, prefix="probe-pending-", delete=False) as stream:
                temporary = Path(stream.name)
                stream.write(result.stdout)
            temporary.replace(path)
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
    return path.read_bytes()


def find_functions(source, name):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", SyntaxWarning)
        tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    matches = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name:
            start = node.lineno - 1
            matches.append(textwrap.dedent("".join(lines[start:node.end_lineno])))
    return matches


def ast_without_docstrings(code):
    tree = ast.parse(textwrap.dedent(code))
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant) and isinstance(node.body[0].value.value, str):
                node.body = node.body[1:]
    return ast.dump(tree, include_attributes=False)


def probe(output, cache, sample_size):
    with (output / "PYTHON_COMBINED_CANDIDATE_PAIRS.jsonl").open() as stream:
        pairs = [json.loads(line) for line in stream]
    selected, seen = [], set()
    for source in ("CVEfixes", "PyResBugs"):
        count = 0
        for row in sorted(pairs, key=lambda r: (r["repository"], r["pair_id"])):
            if row["source"] != source or not row["repository"].startswith("github.com/") or row["repository"] in seen:
                continue
            if len(row["before"].splitlines()) > 100:
                continue
            selected.append(row)
            seen.add(row["repository"])
            count += 1
            if count == sample_size:
                break
    results = []
    canonical = []
    for pair in selected:
        result = {k: pair[k] for k in ("pair_id", "source", "repository", "fixing_commit", "issue_group", "cves")}
        result["dataset_before_after_diff"] = "".join(difflib.unified_diff(
            pair["before"].splitlines(keepends=True), pair["after"].splitlines(keepends=True), fromfile="before", tofile="after"))
        repo = pair["repository"].removeprefix("github.com/")
        try:
            url = f"https://api.github.com/repos/{repo}/commits/{pair['fixing_commit']}"
            commit = json.loads(fetch(url, cache))
            result["commit_url"] = commit["html_url"]
            result["commit_message"] = commit["commit"]["message"]
            result["first_parent"] = commit["parents"][0]["sha"]
            result["changed_files_returned"] = len(commit["files"])
            candidates = [f for f in commit["files"] if f["filename"].endswith(".py") and production(f["filename"])]
            if pair.get("path"):
                candidates = sorted(candidates, key=lambda f: f["filename"] != pair["path"])
            else:
                candidates = sorted(candidates, key=lambda f: pair["function_before"] not in f.get("patch", ""))
            result["files_checked"] = []
            for file in candidates[:4]:
                path_after = file["filename"]
                path_before = file.get("previous_filename", path_after)
                urls = {
                    "before": f"https://raw.githubusercontent.com/{repo}/{result['first_parent']}/{quote(path_before)}",
                    "after": f"https://raw.githubusercontent.com/{repo}/{commit['sha']}/{quote(path_after)}",
                }
                attempt = {"path": path_after, "urls": urls}
                result["files_checked"].append(attempt)
                try:
                    snippets = {}
                    for side in ("before", "after"):
                        raw = fetch(urls[side], cache)
                        attempt[side + "_file_sha256"] = hashlib.sha256(raw).hexdigest()
                        matches = find_functions(raw.decode(), pair["function_" + side])
                        matching = [code for code in matches if normalise(code)[1] == pair[side + "_ast_sha256"]]
                        attempt[side + "_matching_functions"] = len(matching)
                        if not matching and len(matches) == 1:
                            attempt[side + "_upstream_difference"] = "".join(difflib.unified_diff(
                                pair[side].splitlines(keepends=True), matches[0].splitlines(keepends=True),
                                fromfile="dataset", tofile="upstream"))
                        ignoring_docs = [code for code in matches if ast_without_docstrings(code) == ast_without_docstrings(pair[side])]
                        attempt[side + "_matching_ignoring_docstrings"] = len(ignoring_docs)
                        chosen = matching if matching else ignoring_docs
                        if len(chosen) != 1:
                            break
                        snippets[side] = normalise(chosen[0])[0]
                    if len(snippets) == 2:
                        result["both_versions_match_upstream_ast"] = all(attempt[side + "_matching_functions"] == 1 for side in snippets)
                        result["both_versions_match_ignoring_docstrings"] = True
                        corrected = {**pair, **snippets, "path": path_after, "source_urls": urls,
                                     "source_fidelity": "Function bodies checked against first-parent/fix snapshots; decorator lines not reconstructed by this probe"}
                        for side in snippets:
                            corrected[side + "_sha256"] = sha(snippets[side])
                            corrected[side + "_ast_sha256"] = normalise(snippets[side])[1]
                        canonical.append(corrected)
                        break
                except (ValueError, SyntaxError, UnicodeError, KeyError) as error:
                    attempt["error"] = str(error)[:220]
            result.setdefault("both_versions_match_upstream_ast", False)
            try:
                licence = json.loads(fetch(f"https://api.github.com/repos/{repo}/license?ref={commit['sha']}", cache))
                result["upstream_licence_at_fix"] = {"spdx_id": licence.get("license", {}).get("spdx_id"),
                                                     "path": licence.get("path"), "url": licence.get("html_url")}
            except ValueError as error:
                result["upstream_licence_lookup_error"] = str(error)
        except (ValueError, KeyError, IndexError) as error:
            result["error"] = str(error)[:300]
        results.append(result)
        print(json.dumps({"pair_id": pair["pair_id"], "matched": result.get("both_versions_match_upstream_ast", False),
                          "error": result.get("error")}), flush=True)
    save(output / "PYTHON_COMBINED_SOURCE_FIDELITY_PROBES.json", {
        "selection": f"First {sample_size} distinct GitHub repositories per source in lexical order; before functions <=100 lines; nonrandom",
        "probes": results, "matched_pairs": sum(r.get("both_versions_match_upstream_ast", False) for r in results),
        "matched_pairs_ignoring_docstrings": len(canonical), "attempted_pairs": len(results),
        "warning": "Source fidelity is not independent issue relevance, nonsecurity status or licence clearance of every file",
    })
    with (output / "PYTHON_SOURCE_VERIFIED_SAMPLE.jsonl").open("w") as stream:
        for pair in canonical:
            stream.write(json.dumps(pair, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--cache-dir", type=Path, required=True)
    parser.add_argument("--sample-size", type=int, default=4)
    args = parser.parse_args()
    if not args.output_dir.is_dir() or not args.cache_dir.is_dir():
        parser.error("Existing output and cache directories required")
    probe(args.output_dir, args.cache_dir, args.sample_size)
