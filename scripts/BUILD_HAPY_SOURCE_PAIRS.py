"""Reconstruct upstream function pairs intersecting confident human bugfix votes.

Downloads source text, validates every available diff hunk against first-parent
and fixing snapshots, and parses ASTs. Downloaded programs are never executed.
"""

import argparse
import ast
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import textwrap
from urllib.parse import quote
import warnings

from BUILD_CANDIDATE_SPLITS import make_pair, production, save
from PROBE_CANDIDATE_SOURCES import fetch


BUG_PROJECTS = {
    "PySnooper": "cool-RR/PySnooper", "ansible": "ansible/ansible", "black": "psf/black",
    "cookiecutter": "cookiecutter/cookiecutter", "fastapi": "fastapi/fastapi", "httpie": "httpie/cli",
    "keras": "keras-team/keras", "luigi": "spotify/luigi", "matplotlib": "matplotlib/matplotlib",
    "pandas": "pandas-dev/pandas", "sanic": "sanic-org/sanic", "scrapy": "scrapy/scrapy",
    "spacy": "explosion/spaCy", "thefuck": "nvbn/thefuck", "tornado": "tornadoweb/tornado",
    "tqdm": "tqdm/tqdm", "youtube-dl": "ytdl-org/youtube-dl",
}


def changed_files(diff):
    files = []
    current = None
    for line in diff.splitlines():
        if line.startswith("diff --git "):
            current = {"hunks": []}
            files.append(current)
        elif current is not None:
            if line.startswith("--- a/"):
                current["before_path"] = line[6:]
            elif line.startswith("+++ b/"):
                current["after_path"] = line[6:]
            elif line.startswith("@@ "):
                match = re.match(r"@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@", line)
                if not match:
                    raise ValueError("Unsupported hunk header")
                current["hunks"].append({"before": int(match[1]), "after": int(match[2]), "lines": []})
            elif current["hunks"] and line[:1] in (" ", "-", "+"):
                current["hunks"][-1]["lines"].append(line)
    return files


def check_diff(file, before, after):
    lines = {"before": before.splitlines(), "after": after.splitlines()}
    changed = {"before": set(), "after": set()}
    for hunk in file["hunks"]:
        positions = {side: hunk[side] - 1 for side in lines}
        for line in hunk["lines"]:
            sides = ("before", "after") if line[0] == " " else ("before",) if line[0] == "-" else ("after",)
            for side in sides:
                position = positions[side]
                if position >= len(lines[side]) or lines[side][position] != line[1:]:
                    raise ValueError(f"Diff context disagrees with {side} source at line {position + 1}")
                if line[0] != " ":
                    changed[side].add(position + 1)
                positions[side] += 1
    return changed


def functions(source):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", SyntaxWarning)
        tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    found = {}
    def visit(node, parents):
        named = isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))
        path = parents + (node.name,) if named else parents
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            first = min([node.lineno] + [d.lineno for d in node.decorator_list])
            name = ".".join(path)
            if name in found:
                # Conditional/redefined methods require a richer identity scheme.
                found[name] = None
            else:
                found[name] = {"start": first, "end": node.end_lineno,
                               "code": textwrap.dedent("".join(lines[first - 1:node.end_lineno]))}
        for child in ast.iter_child_nodes(node):
            visit(child, path)
    visit(tree, ())
    return {k: v for k, v in found.items() if v is not None}


def resolve_repo(case, commit):
    if case["dataset_source"] == "bugs-in-py":
        project = case["original_case"].rsplit("-", 1)[0]
        return BUG_PROJECTS.get(project)
    urls = [link["url"] for link in case["data"]["initialAnnotation"].get("hyperlinks", [])]
    for url in urls:
        match = re.search(r"github\.com/([^/]+/[^/]+)/commit/([0-9a-f]+)", url)
        if match and (match[2].startswith(commit) or commit.startswith(match[2])):
            return match[1]
    # No guessing from generic advisory URLs or similarly named repositories.
    return None


def process(job, cache):
    case, commit, file, refs, repo = job
    identity = case["case_id"] + ":" + str(commit["index"]) + ":" + file["before_path"]
    result = {"job_id": identity, "case_id": case["case_id"], "repository": repo,
              "fixing_commit": commit["fixing_commit"], "pairs": [], "exclusions": Counter()}
    try:
        sha = commit["fixing_commit"]
        urls = {"before": f"https://raw.githubusercontent.com/{repo}/{sha}%5E/{quote(file['before_path'])}",
                "after": f"https://raw.githubusercontent.com/{repo}/{sha}/{quote(file['after_path'])}"}
        raw = {side: fetch(url, cache) for side, url in urls.items()}
        code = {side: value.decode("utf-8-sig") for side, value in raw.items()}
        changed = check_diff(file, code["before"], code["after"])
        parsed = {side: functions(source) for side, source in code.items()}
        before_refs = {r["line"] for r in refs if r["side"] == "beforeChange"} & changed["before"]
        matched_names = set()
        for line in before_refs:
            containing = [(name, function) for name, function in parsed["before"].items() if function["start"] <= line <= function["end"]]
            if containing:
                # Assign each labelled line to its innermost containing function.
                matched_names.add(min(containing, key=lambda item: item[1]["end"] - item[1]["start"])[0])
        for name in sorted(matched_names):
            if name not in parsed["after"]:
                result["exclusions"]["function deleted/renamed"] += 1
                continue
            before, after = parsed["before"][name], parsed["after"][name]
            try:
                pair = make_pair("HaPy-Bug", identity + ":" + name, "https://github.com/" + repo, sha,
                                 before["code"], after["code"], {
                    "issue_group": "correctness_candidate" if case["dataset_source"] == "bugs-in-py" else "security_candidate",
                    "cves": [] if case["dataset_source"] == "bugs-in-py" else [case["original_case"]], "cwes": [],
                    "hapy_case_id": case["case_id"], "hapy_commit_index": commit["index"],
                    "hapy_original_source": case["dataset_source"], "qualified_function": name,
                    "path": file["before_path"], "after_path": file["after_path"],
                    "before_start_line": before["start"], "after_start_line": after["start"],
                    "before_end_line": before["end"], "after_end_line": after["end"],
                    "source_urls": urls, "full_file_sha256": {side: hashlib.sha256(value).hexdigest() for side, value in raw.items()},
                    "dataset_licence": "CC-BY-4.0", "dataset_doi": "10.6084/m9.figshare.24448663.v1",
                    "source_code_licence": "retain upstream repository/file terms; dataset licence does not override them",
                    "reference_validity": "upstream diff-verified function intersects a changed before-line marked bugfix/programming by >=2 confident manual reviewers",
                    "reference_lines": [r for r in refs if r["side"] == "beforeChange" and before["start"] <= r["line"] <= before["end"] and r["line"] in changed["before"]],
                    "commit_message": commit["message"], "issue_description": case["data"].get("cve", {}).get("summary"),
                })
                pair["label_status"] = "published_human_line_purpose_reference_with_source_verified_context; not independently reproduced bug behaviour"
                result["pairs"].append(pair)
            except (ValueError, SyntaxError) as error:
                result["exclusions"][type(error).__name__ + ": " + str(error).split(" (<unknown>")[0][:80]] += 1
        result["diff_hunks_match_upstream"] = True
        result["before_annotated_changed_lines"] = len(before_refs)
    except (ValueError, SyntaxError, UnicodeError, IndexError) as error:
        result["error"] = str(error)[:240]
    return result


def build(output, cache, workers):
    cases = {r["case_id"]: r for r in json.loads((output / "HAPY_BUG_CASE_METADATA.json").read_text())}
    refs = json.loads((output / "HAPY_BUG_MAJORITY_PROGRAMMING_LINES.json").read_text())
    by_commit = defaultdict(lambda: defaultdict(list))
    for r in refs:
        by_commit[(r["case_id"], r["commit_index"])][r["path"]].append(r)
    jobs, excluded = [], Counter()
    for (identity, index), files in sorted(by_commit.items()):
        case = cases[identity]
        if "REJECT" in case["data"].get("cve", {}).get("summary", ""):
            excluded["rejected CVE record"] += 1
            continue
        commits = [c for c in case["commits"] if c["index"] == index]
        if len(commits) != 1 or not commits[0]["fixing_commit"]:
            excluded["unresolved exact patch hash"] += 1
            continue
        commit = commits[0]
        repo = resolve_repo(case, commit["fixing_commit"])
        if not repo:
            excluded["unresolved repository"] += 1
            continue
        for file in changed_files(commit["diff"]):
            path = file.get("before_path")
            if not path or not file.get("after_path") or path not in files or not production(path):
                continue
            if not any(r["side"] == "beforeChange" for r in files[path]):
                excluded["no labelled changed-before context"] += 1
                continue
            jobs.append((case, commit, file, files[path], repo))
    results = []
    log = output / "HAPY_BUG_SOURCE_RECONSTRUCTION_LOG.jsonl"
    with log.open("w") as stream, ThreadPoolExecutor(max_workers=workers) as pool:
        pending = [pool.submit(process, job, cache) for job in jobs]
        for future in as_completed(pending):
            result = future.result()
            results.append(result)
            stream.write(json.dumps({k: v for k, v in result.items() if k != "pairs"}, ensure_ascii=False) + "\n")
            stream.flush()
            if len(results) % 50 == 0:
                print(json.dumps({"jobs_done": len(results), "jobs_total": len(jobs),
                                  "pairs": sum(len(r["pairs"]) for r in results)}), flush=True)
    unique, duplicates = {}, 0
    for result in sorted(results, key=lambda r: r["job_id"]):
        excluded.update(result["exclusions"])
        for pair in result["pairs"]:
            key = (pair["before_ast_sha256"], pair["after_ast_sha256"])
            if key in unique:
                unique[key].setdefault("duplicate_pair_provenance", []).append({k: pair[k] for k in ("pair_id", "repository", "fixing_commit", "cves", "hapy_case_id")})
                duplicates += 1
            else:
                unique[key] = pair
    pairs = list(unique.values())
    with (output / "HAPY_BUG_CANDIDATE_PAIRS.jsonl").open("w") as stream:
        for pair in pairs:
            stream.write(json.dumps(pair, ensure_ascii=False) + "\n")
    summary = {"source_jobs": len(jobs), "diff_verified_file_pairs": sum(r.get("diff_hunks_match_upstream", False) for r in results),
               "failed_jobs": sum("error" in r for r in results), "failure_reasons": Counter(r["error"] for r in results if "error" in r),
               "candidate_pairs": len(pairs), "candidate_groups": Counter(r["issue_group"] for r in pairs),
               "repositories": len({r["repository"] for r in pairs}), "cases": len({r["hapy_case_id"] for r in pairs}),
               "exact_ast_pair_duplicates_collapsed": duplicates, "exclusions": excluded,
               "context": "Complete upstream functions including decorators/docstrings, 3–250 lines; enclosing module/class not included in function text",
               "negative_interpretation": "After version is a counterpart fixed for the referenced change, not a verified universally clean negative"}
    save(output / "HAPY_BUG_SOURCE_BUILD_AUDIT.json", summary)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--cache-dir", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--background", action="store_true")
    args = parser.parse_args()
    if not args.output_dir.is_dir() or not args.cache_dir.is_dir():
        parser.error("Existing output and cache directories required")
    if args.background:
        log = args.cache_dir / "hapy-source-build.log"
        with log.open("a") as stream:
            child = subprocess.Popen([sys.executable, str(Path(__file__).resolve()),
                                      "--output-dir", str(args.output_dir), "--cache-dir", str(args.cache_dir),
                                      "--workers", str(args.workers)], stdout=stream, stderr=stream, start_new_session=True)
        save(args.output_dir / "HAPY_BUG_SOURCE_BUILD_JOB.json", {"pid": child.pid, "log": str(log)})
        print(json.dumps({"pid": child.pid, "log": str(log)}))
    else:
        build(args.output_dir, args.cache_dir, args.workers)
