"""Measure original CVEfixes additions beyond the whole HaPy-Bug release.

Outputs are review candidates, not automatically validated vulnerable functions.
Downloaded source is parsed as data and is never executed.
"""

import argparse
import ast
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import difflib
import hashlib
import json
from pathlib import Path
import re
import sqlite3
import warnings
from urllib.parse import quote

from BUILD_CANDIDATE_SPLITS import repository, save
from PROBE_CANDIDATE_SOURCES import ast_without_docstrings, fetch, find_functions


def codes(row):
    return {row[side + suffix] for side in ("before", "after")
            for suffix in ("_sha256", "_ast_sha256")}


def linked_cves(row):
    return set(row["cves"]) | {c for d in row.get("duplicate_pair_provenance", []) for c in d["cves"]}


def shingles(code):
    tokens = re.findall(r"\w+|[^\w\s]", code)
    return {tuple(tokens[i:i + 5]) for i in range(max(1, len(tokens) - 4))}


def audit(output):
    with (output / "HAPY_BUG_CANDIDATE_PAIRS.jsonl").open() as stream:
        hapy = [json.loads(line) for line in stream]
    metadata = json.loads((output / "HAPY_BUG_CASE_METADATA.json").read_text())
    all_cves = {r["original_case"] for r in metadata if r["original_case"].startswith("CVE-")}
    all_fixes = {c["fixing_commit"] for r in metadata for c in r["commits"] if c["fixing_commit"]}
    all_fixes.update(c for r in metadata for c in r["recorded_patch_hashes"])
    all_codes = set().union(*(codes(r) for r in hapy))
    all_repos = {r["repository"] for r in hapy}
    existing_cves = {c for r in hapy for c in r["cves"]}
    hapy_sets = [(r["pair_id"], shingles(r[side])) for r in hapy for side in ("before", "after")]
    with (output / "PYTHON_COMBINED_CANDIDATE_PAIRS.jsonl").open() as stream:
        source = [r for line in stream if (r := json.loads(line))["source"] == "CVEfixes"]
    excluded, retained = Counter(), []
    for row in source:
        if linked_cves(row) & all_cves:
            excluded["CVE present anywhere in original HaPy-Bug release"] += 1
            continue
        linked_fixes = {row["fixing_commit"]} | {d["fixing_commit"] for d in row.get("duplicate_pair_provenance", [])}
        if linked_fixes & all_fixes:
            excluded["fix present anywhere in original HaPy-Bug release"] += 1
            continue
        if codes(row) & all_codes:
            excluded["exact code/AST overlap with retained HaPy-Bug"] += 1
            continue
        if ast_without_docstrings(row["before"]) == ast_without_docstrings(row["after"]):
            excluded["docstring-only AST change"] += 1
            continue
        if row["fixing_commit"] == "007d948cb982daa05bc6619cd20ee55b7e834c38" and row["function_before"] == "set_k304":
            excluded["author explicitly says function change unnecessary to security fix"] += 1
            continue
        near = False
        for side in ("before", "after"):
            tokens = shingles(row[side])
            for _, other in hapy_sets:
                if min(len(tokens), len(other)) / max(len(tokens), len(other)) < .9:
                    continue
                common = len(tokens & other)
                if common / (len(tokens) + len(other) - common) >= .9:
                    near = True
                    break
            if near:
                break
        if near:
            excluded["5-token-shingle Jaccard >=0.90 overlap with retained HaPy-Bug"] += 1
            continue
        retained.append(row)
    with (output / "CVEFIXES_SECURITY_EXPANSION_CANDIDATES.jsonl").open("w") as stream:
        for row in retained:
            stream.write(json.dumps(row, ensure_ascii=False) + "\n")
    new_repo = [r for r in retained if repository("https://" + r["repository"]) not in all_repos]
    connection = sqlite3.connect(f"file:{output / 'CVEFIXES_PYTHON.sqlite'}?mode=ro", uri=True)
    methods = {r[0]: r[1:] for r in connection.execute("SELECT method_change_id,file_change_id,start_line,end_line FROM method_change")}
    source_integrity = 0
    for row in retained:
        before = methods[row["method_change_id_before"]]
        after = methods[row["method_change_id_after"]]
        assert before[0] == row["file_change_id"] == after[0]
        assert int(before[1]) > 0 and int(after[1]) > 0
        source_integrity += 1
    counts = lambda rows: {"function_pairs": len(rows), "distinct_cves": len({c for r in rows for c in linked_cves(r)}),
                            "distinct_fixes": len({r["fixing_commit"] for r in rows}),
                            "repositories": len({r["repository"] for r in rows})}
    report = {"existing_hapy": counts(hapy), "existing_hapy_security_cves": len(existing_cves),
              "original_hapy_release_cves_excluded": len(all_cves), "original_cvefixes_candidate_pool": counts(source),
              "additional_nonoverlapping_candidates": counts(retained), "additional_candidates_in_new_repositories": counts(new_repo),
              "potential_total_security_cves_if_all_candidates_validated": len(existing_cves | {c for r in retained for c in linked_cves(r)}),
              "method_to_file_links_checked": source_integrity, "exclusions": excluded,
              "dataset_licence": "CC-BY-4.0; original archive licence already verified",
              "status": "Novel source-linked candidates; issue relevance needs record-level review before admission",
              "near_duplicate_rule": "5-token-shingle Jaccard >=0.90, either version, against retained HaPy-Bug",
              "limitations": ["No semantic-clone or exhaustive fork-identity proof", "CVE association does not prove every changed method contains the issue",
                              "No fixed-version universal-cleanliness assumption", "Larger combined corpus requires rebuilding grouped splits"]}
    save(output / "CVEFIXES_SECURITY_EXPANSION_AUDIT.json", report)
    # A fixed nonrandom source-review sample, distinct repositories/CVEs and <=60-line functions.
    sample, seen_repos, seen_cves = [], set(), set()
    for row in sorted(retained, key=lambda r: (r["repository"], r["pair_id"])):
        if row["repository"] in seen_repos or set(row["cves"]) & seen_cves or len(row["before"].splitlines()) > 60:
            continue
        sample.append(row)
        seen_repos.add(row["repository"])
        seen_cves.update(row["cves"])
        if len(sample) == 10:
            break
    save(output / "CVEFIXES_SECURITY_EXPANSION_REVIEW_SAMPLE.json", sample)
    review = ["# Additional security-function review sample", "", "First 10 lexical distinct repositories/CVE groups; before functions <=60 lines. Nonrandom, not a quality estimate.", ""]
    for row in sample:
        review.extend(["## " + row["pair_id"], "", "CVEs: " + ", ".join(row["cves"]), "",
                       "Commit: https://" + row["repository"] + "/commit/" + row["fixing_commit"], "",
                       "Path: " + row["path"], "", "Description: " + json.dumps(row["descriptions"], ensure_ascii=False), "",
                       "Commit message: " + str(row["commit"]["msg"]), "", "```diff",
                       "".join(difflib.unified_diff(row["before"].splitlines(keepends=True), row["after"].splitlines(keepends=True), fromfile="before", tofile="after")).rstrip(), "```", ""])
    (output / "CVEFIXES_SECURITY_EXPANSION_REVIEW_SAMPLE.md").write_text("\n".join(review))
    print(json.dumps(report, indent=2))


def probe_sample(output, cache):
    sample = json.loads((output / "CVEFIXES_SECURITY_EXPANSION_REVIEW_SAMPLE.json").read_text())
    connection = sqlite3.connect(f"file:{output / 'CVEFIXES_PYTHON.sqlite'}?mode=ro", uri=True)
    paths = {r[0]: r[1:] for r in connection.execute("SELECT file_change_id,old_path,new_path FROM file_change")}
    def check(row):
        result = {k: row[k] for k in ("pair_id", "repository", "fixing_commit", "cves", "function_before", "path")}
        try:
            repo = row["repository"].removeprefix("github.com/")
            parent = ast.literal_eval(row["commit"]["parents"])[0]
            result["parent"] = parent
            versions = {"before": (parent, paths[row["file_change_id"]][0]),
                        "after": (row["fixing_commit"], paths[row["file_change_id"]][1])}
            result["snapshots"] = {}
            for side, (commit, path) in versions.items():
                url = f"https://raw.githubusercontent.com/{repo}/{commit}/{quote(path)}"
                raw = fetch(url, cache)
                matches = find_functions(raw.decode("utf-8-sig"), row["function_" + side])
                matched = [m for m in matches if ast_without_docstrings(m) == ast_without_docstrings(row[side])]
                result["snapshots"][side] = {"url": url, "sha256": hashlib.sha256(raw).hexdigest(),
                                             "matching_function_bodies_ignoring_docstrings": len(matched)}
            result["both_function_versions_match_upstream"] = all(v["matching_function_bodies_ignoring_docstrings"] > 0 for v in result["snapshots"].values())
            result["advisories"] = []
            for cve in row["cves"]:
                try:
                    advisories = json.loads(fetch("https://api.github.com/advisories?cve_id=" + cve, cache))
                    if not isinstance(advisories, list):
                        raise ValueError("Unexpected advisory response")
                    result["advisories"].extend({"cve_id": a["cve_id"], "ghsa_id": a["ghsa_id"], "url": a["html_url"],
                                                 "summary": a["summary"], "description": a["description"],
                                                 "references": a["references"]} for a in advisories)
                except ValueError as error:
                    result.setdefault("advisory_lookup_errors", []).append(str(error))
        except (ValueError, SyntaxError, UnicodeError, IndexError, KeyError) as error:
            result["error"] = str(error)[:250]
        return result
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(check, sample))
    report = {"selection": "Fixed ten-case nonrandom expansion review sample", "probes": results,
              "both_versions_match_count": sum(r.get("both_function_versions_match_upstream", False) for r in results),
              "attempted": len(results), "warning": "Upstream source matching is separate from issue relevance; sample is not a population quality estimate"}
    save(output / "CVEFIXES_SECURITY_EXPANSION_UPSTREAM_PROBES.json", report)
    print(json.dumps({"attempted": len(results), "both_versions_match_count": report["both_versions_match_count"],
                      "cases": [{"cves": r["cves"], "matched": r.get("both_function_versions_match_upstream"),
                                 "advisories": len(r.get("advisories", [])), "error": r.get("error")} for r in results]}, indent=2))


def review(output):
    expected_pairs = {
        "CVE-2024-34359": "CVEfixes:234972625470322:31534987156542",
        "CVE-2024-37301": "CVEfixes:221462273273842:221694810061732",
        "CVE-2024-26134": "CVEfixes:37124422765174:171028133210182",
        "CVE-2024-30251": "CVEfixes:118748627772256:179339447712205",
        "CVE-2019-25066": "CVEfixes:233486512677834:136865694333523",
        "CVE-2024-4340": "CVEfixes:145591340700199:125551005275033",
        "CVE-2015-6240": "CVEfixes:205290039003413:105819897026174",
        "CVE-2021-4041": "CVEfixes:102817320279789:30565809177595",
        "CVE-2018-1000089": "CVEfixes:130125534823174:96907832057000",
        "CVE-2024-31451": "CVEfixes:4244925349306:119894775406109",
    }
    decisions = {
        "CVE-2024-34359": ("source_advisory_supported", "Advisory names the unsandboxed Jinja2 environment in Jinja2ChatFormatter; selected constructor replaces it with an immutable sandbox."),
        "CVE-2024-37301": ("source_advisory_supported", "Publisher advisory identifies server-side template injection; selected environment factory switches to SandboxedEnvironment, in the referenced patch."),
        "CVE-2024-26134": ("reject_python_pair", "Advisory says the recorded commit introduced the crash, rather than fixing it; reported corruption concerns the native CBOR decoder. Do not label these Python before/after functions as this vulnerability/fix."),
        "CVE-2024-30251": ("needs_issue_context", "Advisory locates the minimal security fix in _read_chunk_from_length; sampled _get_part_reader only propagates parameters and is not established as the vulnerable function."),
        "CVE-2019-25066": ("source_advisory_supported", "Advisory references this exact patch; the author identifies shell injection and the selected authenticate function adds quoting to the username interpolated into a shell command."),
        "CVE-2024-4340": ("source_advisory_supported", "Advisory stack trace reaches flatten and references this patch; the selected function converts uncontrolled RecursionError to the library's SQLParseError. This does not prove all resource-exhaustion issues are eliminated."),
        "CVE-2015-6240": ("reject_selected_function", "Selected connect method changes its docstring and a diagnostic log message. It does not implement the symlink/environment escape fix."),
        "CVE-2021-4041": ("needs_issue_context", "Selected documentation-command argument builder is not the shell-execution sink identified by the advisory; relevant downstream context must be traced."),
        "CVE-2018-1000089": ("needs_issue_context", "Security effect depends on Django's settings-name redaction and deployment configuration, not just this constructor's behaviour."),
        "CVE-2024-31451": ("needs_issue_context", "Source change restricts download URLs before writing files, but the complete file-write/route context and a detailed vulnerability reference need review."),
    }
    sample = json.loads((output / "CVEFIXES_SECURITY_EXPANSION_REVIEW_SAMPLE.json").read_text())
    probes = {r["pair_id"]: r for r in json.loads((output / "CVEFIXES_SECURITY_EXPANSION_UPSTREAM_PROBES.json").read_text())["probes"]}
    reviewed, supported, rejected = [], [], set()
    for row in sample:
        assert row["pair_id"] == expected_pairs[row["cves"][0]], "A changed sample needs a fresh review; do not transfer these decisions"
        decision, reason = decisions[row["cves"][0]]
        probe = probes[row["pair_id"]]
        assert probe["both_function_versions_match_upstream"]
        evidence = {"pair_id": row["pair_id"], "cves": row["cves"], "decision": decision, "reason": reason,
                    "upstream_body_match": True, "advisory_urls": [a["url"] for a in probe.get("advisories", [])],
                    "reviewer": "assistant source/advisory inspection; not independent human adjudication or reproduced failing tests"}
        reviewed.append(evidence)
        if decision == "source_advisory_supported":
            assert any(a["cve_id"] in row["cves"] for a in probe.get("advisories", []))
            supported.append({**row, "expansion_review": evidence, "upstream_snapshots": probe["snapshots"],
                              "label_status": "source_advisory_supported_candidate_requires_researcher_confirmation_for_gold_evaluation"})
        elif decision.startswith("reject"):
            rejected.add(row["pair_id"])
    with (output / "CVEFIXES_SECURITY_EXPANSION_CANDIDATES.jsonl").open() as stream:
        candidates = [json.loads(line) for line in stream]
    retained = [r for r in candidates if r["pair_id"] not in rejected and "CVE-2024-26134" not in linked_cves(r)]
    assert not rejected & {r["pair_id"] for r in retained}
    for filename, rows in (("CVEFIXES_SECURITY_EXPANSION_FILTERED_CANDIDATES.jsonl", retained),
                           ("CVEFIXES_SECURITY_EXPANSION_SUPPORTED_SAMPLE.jsonl", supported)):
        with (output / filename).open("w") as stream:
            for row in rows:
                stream.write(json.dumps(row, ensure_ascii=False) + "\n")
    with (output / "HAPY_BUG_CANDIDATE_PAIRS.jsonl").open() as stream:
        hapy = [json.loads(line) for line in stream]
    assert len({r["pair_id"] for r in hapy + retained}) == len(hapy) + len(retained)
    assert not {c for r in retained for c in linked_cves(r)} & {c for r in hapy for c in linked_cves(r)}
    with (output / "HAPY_CVEFIXES_EXPANSION_CANDIDATE_PAIRS.jsonl").open("w") as stream:
        for row in hapy + retained:
            stream.write(json.dumps(row, ensure_ascii=False) + "\n")
    report = {"sample_reviews": reviewed, "sample_decisions": Counter(r["decision"] for r in reviewed),
              "sample_method": "Ten fixed nonrandom distinct-repository/CVE examples; not an estimated acceptance rate",
              "post_review_candidate_function_pairs": len(retained),
              "post_review_candidate_distinct_cves": len({c for r in retained for c in linked_cves(r)}),
              "combined_potential_security_cves": len({c for r in hapy + retained for c in linked_cves(r)}),
              "combined_candidate_function_pairs_all_categories": len(hapy) + len(retained),
              "supported_sample_pairs": len(supported), "removed_after_review": len(candidates) - len(retained),
              "status": "Four source/advisory-supported additions demonstrated; full candidate pool is not validated gold",
              "licence": "Both published datasets CC-BY-4.0; retain original attribution and applicable upstream code terms"}
    save(output / "CVEFIXES_SECURITY_EXPANSION_REVIEW_RESULTS.json", report)
    print(json.dumps({k: v for k, v in report.items() if k != "sample_reviews"}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("audit", "probe", "review"), default="audit", nargs="?")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--cache-dir", type=Path)
    args = parser.parse_args()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", SyntaxWarning)
        if args.stage == "probe":
            if args.cache_dir is None or not args.cache_dir.is_dir():
                parser.error("Probe stage requires an existing --cache-dir")
            probe_sample(args.output_dir, args.cache_dir)
        elif args.stage == "review":
            review(args.output_dir)
        else:
            audit(args.output_dir)
