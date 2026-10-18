"""Offline independent integrity checks for the conservative combined snapshot.

This does not adjudicate issue labels. Never imports or executes dataset code.
Reconstructs code directly by source line slicing and independently enumerates
all cross-split pairs meeting the specified lexical near-duplicate threshold.
"""

import argparse
import ast
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
import textwrap
from urllib.parse import quote
import warnings
import zipfile


def digest(value):
    return hashlib.sha256(value if isinstance(value, bytes) else value.encode()).hexdigest()


def load_rows(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def main(output):
    prefix = "HAPY_CVEFIXES_ADMITTED"
    master = {r["pair_id"]: r for r in load_rows(output / (prefix + "_CANDIDATE_PAIRS.jsonl"))}
    assert len(master) == len(load_rows(output / (prefix + "_CANDIDATE_PAIRS.jsonl")))
    decisions = {r["pair_id"]: r for r in load_rows(output / "SECURITY_ADMISSION_FINAL_DECISIONS.jsonl")}
    evidence = {r["cve_id"]: r for r in load_rows(output / "SECURITY_ADMISSION_CVE_EVIDENCE.jsonl")}
    original = {r["pair_id"]: r for r in load_rows(output / "CVEFIXES_SECURITY_EXPANSION_FILTERED_CANDIDATES.jsonl")}
    assert set(decisions) == set(original)
    assert all(d.get("review_decision_recorded") for d in decisions.values()), "Full-pool triage is incomplete"
    admitted = {r["pair_id"]: r for r in load_rows(output / "CVEFIXES_SECURITY_ADMITTED_PAIRS.jsonl")}
    assert set(admitted) == {p for p, d in decisions.items() if d["status"] == "admit"}
    base = {r["pair_id"]: r for r in load_rows(output / "HAPY_BUG_CANDIDATE_PAIRS.jsonl")}
    assert master == base | admitted
    release_cases = json.loads((output / "HAPY_BUG_CASE_METADATA.json").read_text())
    release_cves = {r["original_case"] for r in release_cases if r["original_case"].startswith("CVE-")}
    assert not release_cves & {c for r in admitted.values() for c in r["cves"]}
    pairs, seen_ids, keys, shingles, source_urls = [], set(), defaultdict(set), [], set()
    counts, human_refs, split_cves, source_counts = {}, 0, {}, {}
    with zipfile.ZipFile(output / "HAPY_BUG_UPSTREAM_SNAPSHOTS.zip") as hapy_zip, \
            zipfile.ZipFile(output / "SECURITY_ADMISSION_UPSTREAM_SNAPSHOTS.zip") as security_zip:
        security_index = json.loads(security_zip.read("index.json"))
        for split in ("train", "validation", "test"):
            rows = load_rows(output / f"{prefix}_{split.upper()}_CANDIDATES.jsonl")
            counts[split] = Counter(r["issue_group"] for r in rows)
            source_counts[split] = Counter(r["source"] for r in rows)
            split_cves[split] = len({c for r in rows for c in r["cves"]})
            inputs, references = [], []
            for row in rows:
                pid = row["pair_id"]
                assert pid not in seen_ids and row["split"] == split
                seen_ids.add(pid)
                assert {k: v for k, v in row.items() if k != "split"} == master[pid]
                identities = ["repo:" + row["repository"], "fix:" + row["fixing_commit"]]
                identities += ["cve:" + c for c in row["cves"] + row.get("commit_linked_cves", [])]
                for d in row.get("duplicate_pair_provenance", []):
                    identities += ["repo:" + d["repository"], "fix:" + d["fixing_commit"]]
                    identities += ["cve:" + c for c in d["cves"]]
                for side in ("before", "after"):
                    if row["source"] == "CVEfixes":
                        snap = row["upstream_snapshots"][side]
                        url = snap["url"]
                        item = security_index[url]
                        raw = security_zip.read(item["member"])
                        assert digest(raw) == snap["sha256"] == item["sha256"]
                        if "source_location_evidence" in row:
                            assert digest(raw.decode("utf-8-sig")) == row["full_file_text_sha256"][side]
                            assert snap["released_full_file_text_matches"]
                        start, end = snap["function_start"], snap["function_end"]
                        assert (start, end) == (row[side + "_start_line"], row[side + "_end_line"])
                    else:
                        url = row["source_urls"][side]
                        raw = hapy_zip.read("sources/" + digest(url) + ".py")
                        assert digest(raw) == row["full_file_sha256"][side]
                        start, end = row[side + "_start_line"], row[side + "_end_line"]
                    source_urls.add(url)
                    lines = raw.decode("utf-8-sig").splitlines(keepends=True)
                    reconstructed = textwrap.dedent("".join(lines[start - 1:end])).strip() + "\n"
                    assert reconstructed == row[side], pid
                    tree = ast.parse(reconstructed)
                    assert len(tree.body) == 1 and isinstance(tree.body[0], (ast.FunctionDef, ast.AsyncFunctionDef))
                    assert 3 <= len(reconstructed.splitlines()) <= 250
                    assert digest(reconstructed) == row[side + "_sha256"]
                    assert digest(ast.dump(tree, include_attributes=False)) == row[side + "_ast_sha256"]
                    identities += ["text:" + digest(reconstructed), "ast:" + row[side + "_ast_sha256"]]
                    tokens = re.findall(r"\w+|[^\w\s]", reconstructed)
                    token_set = {tuple(tokens[i:i + 5]) for i in range(max(1, len(tokens) - 4))}
                    shingles.append((pid, side, split, token_set))
                assert row["before_ast_sha256"] != row["after_ast_sha256"]
                if row["source"] == "CVEfixes":
                    if "source_location_evidence" in row:
                        location = row["source_location_evidence"]
                        assert location["original_repository"] == row["repository"]
                        assert digest(location["commit_record_text"]) == location["commit_record_sha256"]
                        commit_record = json.loads(location["commit_record_text"])
                        assert commit_record["sha"] == row["fixing_commit"]
                        assert commit_record["parents"][0]["sha"] == ast.literal_eval(row["commit"]["parents"])[0]
                    decision = decisions[pid]
                    assert decision["issue_relevance_inspection_recorded"]
                    assert set(row["cves"]) <= set(original[pid]["cves"])
                    assert row["cves"] == decision["supported_cves"]
                    for cve in row["cves"]:
                        assert evidence[cve]["state"] == "PUBLISHED"
                    for side in ("before", "after"):
                        assert decision["inspected_code_sha256"][side] == row[side + "_sha256"]
                    assert "assistant" in row["label_status"]
                    for snap in row.get("companion_snapshots", []):
                        item = security_index[snap["url"]]
                        raw = security_zip.read(item["member"])
                        assert digest(raw) == snap["sha256"] == item["sha256"]
                        lines = raw.decode("utf-8-sig").splitlines(keepends=True)
                        helper = textwrap.dedent("".join(lines[snap["function_start"] - 1:snap["function_end"]])).strip() + "\n"
                        assert digest(helper) == snap["function_sha256"]
                        ast.parse(helper)
                        source_urls.add(snap["url"])
                    expected_context = {item["path"]: item["sha256"] for item in decision.get("context_files", [])}
                    snapshots = row.get("context_snapshots", [])
                    assert len(snapshots) == len(expected_context)
                    assert {snap["path"] for snap in snapshots} == set(expected_context)
                    retrieval_repo = row.get("source_location_evidence", {}).get("retrieval_repository", row["repository"])
                    for snap in snapshots:
                        path = snap["path"]
                        assert not path.startswith("/") and ".." not in path.split("/")
                        if retrieval_repo.startswith("github.com/"):
                            root = "https://raw.githubusercontent.com/" + retrieval_repo.removeprefix("github.com/")
                            expected_url = f"{root}/{row['fixing_commit']}/{quote(path)}"
                        else:
                            assert retrieval_repo.startswith("gitlab.com/")
                            expected_url = f"https://{retrieval_repo}/-/raw/{row['fixing_commit']}/{quote(path)}"
                        assert snap["url"] == expected_url
                        item = security_index[snap["url"]]
                        raw = security_zip.read(item["member"])
                        assert digest(raw) == snap["sha256"] == item["sha256"] == expected_context[path]
                        source_urls.add(snap["url"])
                else:
                    assert row["reference_lines"]
                    for ref in row["reference_lines"]:
                        assert ref["side"] == "beforeChange"
                        assert row["before_start_line"] <= ref["line"] <= row["before_end_line"]
                        confident = sum(v[0] in ("bug(fix)", "bug(fix) + refactoring") and v[1] == "programming" and v[2]
                                        for v in ref["manual_votes"].values())
                        assert confident >= 2 and confident == ref["bugfix_programming_votes"]
                        human_refs += 1
                for key in identities:
                    keys[key].add(split)
                input_id = digest(pid)
                inputs.append({"input_id": input_id, "language": "Python", "code": row["before"]})
                references.append({"input_id": input_id, "pair_id": pid, "issue_group": row["issue_group"],
                                   "cves": row["cves"], "label_status": row["label_status"]})
                pairs.append(row)
            for suffix, entries in (("BEFORE_ONLY_INPUTS", inputs), ("REFERENCE_INDEX", references)):
                with (output / f"{prefix}_{split.upper()}_{suffix}.jsonl").open("w") as stream:
                    for entry in entries:
                        stream.write(json.dumps(entry, ensure_ascii=False) + "\n")
            assert {i["input_id"] for i in inputs} == {r["input_id"] for r in references}
    assert seen_ids == set(master)
    assert all(len(splits) == 1 for splits in keys.values()), "Cross-split provenance/code leakage"
    assert len({(r["before_ast_sha256"], r["after_ast_sha256"]) for r in pairs}) == len(pairs)
    near = []
    for i, (pid, side, split, tokens) in enumerate(shingles):
        for other_id, other_side, other_split, other in shingles[:i]:
            if split == other_split or min(len(tokens), len(other)) / max(len(tokens), len(other)) < .9:
                continue
            similarity = len(tokens & other) / len(tokens | other)
            if similarity >= .9:
                near.append([pid, side, other_id, other_side, similarity])
    assert not near, "Cross-split lexical near duplicate"
    report = {"status": "offline integrity/provenance/split verification passed; not issue-label adjudication",
              "combined_pairs": len(pairs), "function_versions_checked": len(pairs) * 2,
              "unique_full_source_snapshots_checked": len(source_urls), "human_reference_lines_checked": human_refs,
              "admitted_additions_checked": len(admitted), "complete_pool_decisions_checked": len(decisions),
              "split_counts": counts, "split_security_cve_counts": split_cves, "split_annotation_source_counts": source_counts,
              "cross_split_provenance_text_ast_violations": [], "exhaustive_cross_split_near_duplicates": near,
              "inference_inputs": "Opaque hashed identifier, Python language, before-code only. No CVE, after-code, commit message, or reference fields. Original source comments/docstrings preserved.",
              "limits": ["No semantic-clone or exhaustive fork proof", "No assertion about public-model pretraining contamination",
                         "CVEfixes labels are assistant source/advisory judgements, not independent human gold"]}
    (output / "SECURITY_ADMISSION_INDEPENDENT_VERIFICATION.json").write_text(json.dumps(report, indent=2) + "\n")
    files = sorted({p for pattern in ("SECURITY_ADMISSION_*", "CVEFIXES_SECURITY_ADMITTED_PAIRS.jsonl", "HAPY_CVEFIXES_ADMITTED_*")
                    for p in output.glob(pattern) if p.is_file() and p.suffix in (".json", ".jsonl", ".zip")
                    and p.name != "SECURITY_ADMISSION_RELEASE_MANIFEST.json"})
    files += [output / name for name in ("HAPY_BUG_UPSTREAM_SNAPSHOTS.zip", "ADMIT_SECURITY_EXPANSION.py",
              "VERIFY_SECURITY_ADMISSION.py", "INSPECT_SECURITY_CANDIDATES.py", "BUILD_CANDIDATE_SPLITS.py", "BUILD_HAPY_SOURCE_PAIRS.py",
              "PROBE_CANDIDATE_SOURCES.py", "SECURITY_EXPANSION_AUDIT.py", "CVEFIXES_UPSTREAM_LICENSE.txt",
               "SECURITY_ADMISSION_FINDINGS.md", "SECURITY_EXPANSION_FINDINGS.md", "DATASET_DECISION.md", "README.md")]
    manifest = {"status": report["status"], "dataset_licences": "HaPy-Bug and CVEfixes dataset releases CC-BY-4.0; preserve original source terms",
                "sources": ["https://doi.org/10.6084/m9.figshare.24448663.v1", "https://zenodo.org/records/13118970"],
                "required_base_source_archive": "HAPY_BUG_UPSTREAM_SNAPSHOTS.zip",
                "files": {p.name: {"bytes": p.stat().st_size, "sha256": digest(p.read_bytes())} for p in files}}
    (output / "SECURITY_ADMISSION_RELEASE_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", SyntaxWarning)
        main(args.output_dir)
