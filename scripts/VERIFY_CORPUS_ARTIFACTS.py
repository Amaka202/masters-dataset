"""Independently check exported corpus integrity against cached upstream text."""

import argparse
import ast
from collections import Counter, defaultdict
import difflib
import hashlib
import json
from pathlib import Path
import re
import sqlite3
import textwrap
import warnings
import zipfile

from BUILD_CANDIDATE_SPLITS import save
from PROBE_CANDIDATE_SOURCES import ast_without_docstrings


def verify(output, cache):
    pairs = []
    splits = {}
    for split in ("train", "validation", "test"):
        with (output / f"HAPY_BUG_{split.upper()}_CANDIDATES.jsonl").open() as stream:
            rows = [json.loads(line) for line in stream]
        for row in rows:
            assert row["split"] == split
            assert row["pair_id"] not in splits
            splits[row["pair_id"]] = split
        pairs.extend(rows)
    with (output / "HAPY_BUG_CANDIDATE_PAIRS.jsonl").open() as stream:
        master = [json.loads(line) for line in stream]
    assert {r["pair_id"] for r in master} == set(splits)
    keys, source_text, code_sets = defaultdict(set), {}, []
    snapshot_path = output / "HAPY_BUG_UPSTREAM_SNAPSHOTS.zip"
    preserved = zipfile.ZipFile(snapshot_path) if snapshot_path.exists() else None
    checked_references, docstring_only = 0, []
    for row in pairs:
        split = row["split"]
        identifiers = ["repo:" + row["repository"], "commit:" + row["fixing_commit"]]
        identifiers += ["cve:" + c for c in row["cves"]]
        for duplicate in row.get("duplicate_pair_provenance", []):
            identifiers += ["repo:" + duplicate["repository"], "commit:" + duplicate["fixing_commit"]]
            identifiers += ["cve:" + c for c in duplicate["cves"]]
        for side in ("before", "after"):
            url = row["source_urls"][side]
            if url not in source_text:
                cached = cache / ("probe-" + hashlib.sha256(url.encode()).hexdigest()[:24])
                if cached.exists():
                    raw = cached.read_bytes()
                elif preserved is not None:
                    raw = preserved.read("sources/" + hashlib.sha256(url.encode()).hexdigest() + ".py")
                else:
                    raise FileNotFoundError("Neither cached nor preserved source snapshot exists: " + url)
                source_text[url] = (raw, raw.decode("utf-8-sig").splitlines(keepends=True))
            raw, lines = source_text[url]
            assert hashlib.sha256(raw).hexdigest() == row["full_file_sha256"][side]
            expected = textwrap.dedent("".join(lines[row[side + "_start_line"] - 1:row[side + "_end_line"]])).strip() + "\n"
            assert expected == row[side]
            text_hash = hashlib.sha256(row[side].encode()).hexdigest()
            ast_hash = hashlib.sha256(ast.dump(ast.parse(row[side]), include_attributes=False).encode()).hexdigest()
            assert text_hash == row[side + "_sha256"]
            assert ast_hash == row[side + "_ast_sha256"]
            identifiers += ["code:" + text_hash, "ast:" + ast_hash]
            tokens = re.findall(r"\w+|[^\w\s]", row[side])
            shingles = {tuple(tokens[j:j + 5]) for j in range(max(1, len(tokens) - 4))}
            code_sets.append((row["pair_id"] + ":" + side, split, shingles))
        for key in identifiers:
            keys[key].add(split)
        assert row["reference_lines"]
        for line in row["reference_lines"]:
            assert line["side"] == "beforeChange"
            assert row["before_start_line"] <= line["line"] <= row["before_end_line"]
            confident = sum(v[0] in ("bug(fix)", "bug(fix) + refactoring") and v[1] == "programming" and v[2]
                            for v in line["manual_votes"].values())
            assert confident >= 2
            assert confident == line["bugfix_programming_votes"]
            checked_references += 1
        if ast_without_docstrings(row["before"]) == ast_without_docstrings(row["after"]):
            docstring_only.append(row["pair_id"])
    crossed = [k for k, s in keys.items() if len(s) > 1]
    assert not crossed
    near = []
    for i, (identity, split, shingles) in enumerate(code_sets):
        for other, other_split, other_shingles in code_sets[:i]:
            if split == other_split or min(len(shingles), len(other_shingles)) / max(len(shingles), len(other_shingles)) < .9:
                continue
            common = len(shingles.intersection(other_shingles))
            similarity = common / (len(shingles) + len(other_shingles) - common)
            if similarity >= .9:
                near.append({"left": other, "right": identity, "jaccard": similarity})
    assert not near
    database = sqlite3.connect(f"file:{output / 'CVEFIXES_PYTHON.sqlite'}?mode=ro", uri=True)
    security_hashes = {r[0] for r in database.execute("SELECT DISTINCT hash FROM fixes")}
    ambiguous = [{"pair_id": r["pair_id"], "commit": r["fixing_commit"]} for r in pairs
                 if r["issue_group"] == "correctness_candidate" and r["fixing_commit"] in security_hashes]
    duplicate_asts = Counter((r["before_ast_sha256"], r["after_ast_sha256"]) for r in pairs)
    assert max(duplicate_asts.values(), default=0) <= 1
    cwe_by_cve = defaultdict(set)
    for cve, cwe in database.execute("SELECT cve_id,cwe_id FROM cwe_classification"):
        cwe_by_cve[cve].add(cwe)
    report = {"pair_count": len(pairs), "unique_full_source_snapshots_checked": len(source_text),
              "function_versions_checked": len(pairs) * 2, "human_reference_lines_checked": checked_references,
              "cross_split_provenance_or_exact_ast_keys": crossed, "exhaustive_cross_split_near_duplicates": near,
              "docstring_only_ast_changes": docstring_only,
              "correctness_origin_pairs_also_in_original_cve_fix_hashes": ambiguous,
              "split_counts": Counter(r["split"] for r in pairs),
              "split_case_counts": {s: len({r["hapy_case_id"] for r in pairs if r["split"] == s}) for s in ("train", "validation", "test")},
              "split_security_cve_counts": {s: len({c for r in pairs if r["split"] == s for c in r["cves"]}) for s in ("train", "validation", "test")},
              "security_cwe_metadata_counts": Counter(cwe for c in {c for r in pairs for c in r["cves"]} for cwe in cwe_by_cve[c]),
              "limitations": ["No assertion that public-model pretraining excludes these repositories",
                              "No semantic-clone or exhaustive fork audit", "After counterpart is not verified universally clean",
                              "Reference lines are published human judgements; project tests were not executed"]}
    save(output / "HAPY_BUG_INDEPENDENT_EXPORT_VERIFICATION.json", report)
    if preserved is not None:
        preserved.close()
    with zipfile.ZipFile(output / "HAPY_BUG_UPSTREAM_SNAPSHOTS.zip", "w", compression=zipfile.ZIP_DEFLATED) as archive:
        index = {}
        for url, (raw, _) in sorted(source_text.items()):
            filename = "sources/" + hashlib.sha256(url.encode()).hexdigest() + ".py"
            archive.writestr(zipfile.ZipInfo(filename), raw, compress_type=zipfile.ZIP_DEFLATED)
            index[url] = {"path": filename, "sha256": hashlib.sha256(raw).hexdigest()}
        archive.writestr(zipfile.ZipInfo("SOURCE_INDEX.json"), json.dumps(index, indent=2), compress_type=zipfile.ZIP_DEFLATED)
    sample, seen = [], set()
    for group in ("security_candidate", "correctness_candidate"):
        selected = 0
        for row in sorted(pairs, key=lambda r: (r["repository"], r["pair_id"])):
            if row["issue_group"] != group or row["repository"] in seen or len(row["before"].splitlines()) > 60:
                continue
            sample.append(row)
            seen.add(row["repository"])
            selected += 1
            if selected == 3:
                break
    review = ["# HaPy-Bug source-linked review sample", "", "Nonrandom: first three lexical distinct repositories per group; before function <=60 lines.", ""]
    for row in sample:
        review += ["## " + row["pair_id"], "", "Group: " + row["issue_group"], "",
                   "Commit: https://" + row["repository"] + "/commit/" + row["fixing_commit"], "",
                   "Description: " + str(row.get("issue_description")), "", "Message: " + row["commit_message"], "",
                   "Reference lines: " + json.dumps(row["reference_lines"]), "", "```diff",
                   "".join(difflib.unified_diff(row["before"].splitlines(keepends=True), row["after"].splitlines(keepends=True), fromfile="before", tofile="after")).rstrip(),
                   "```", ""]
    (output / "HAPY_BUG_SOURCE_LINKED_REVIEW_SAMPLE.md").write_text("\n".join(review))
    files = ["HAPY_BUG_CANDIDATE_PAIRS.jsonl", "HAPY_BUG_TRAIN_CANDIDATES.jsonl", "HAPY_BUG_VALIDATION_CANDIDATES.jsonl",
             "HAPY_BUG_TEST_CANDIDATES.jsonl", "HAPY_BUG_MAJORITY_PROGRAMMING_LINES.json", "HAPY_BUG_CASE_METADATA.json",
             "HAPY_BUG_OFFICIAL_RELEASE_METADATA.json", "HAPY_BUG_SPLIT_AUDIT.json", "HAPY_BUG_UPSTREAM_SNAPSHOTS.zip"]
    fingerprints = {}
    for filename in files:
        with (output / filename).open("rb") as stream:
            fingerprints[filename] = hashlib.file_digest(stream, "sha256").hexdigest()
    save(output / "HAPY_BUG_RELEASE_MANIFEST.json", {
        "upstream_doi": "10.6084/m9.figshare.24448663.v1", "dataset_licence": "CC-BY-4.0",
        "attribution": "Przymus, Fejzer, Narębski, Woźniak, Halada, Kazecki et al. (2025), HaPy-Bug",
        "local_modifications": "Confident manual vote filtering; exact upstream patch/source reconstruction; function extraction; deduplication and grouped splits",
        "file_sha256": fingerprints,
    })
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--cache-dir", type=Path, required=True)
    args = parser.parse_args()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", SyntaxWarning)
        verify(args.output_dir, args.cache_dir)
