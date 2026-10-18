"""Record-level admission pipeline for the fixed CVEfixes expansion pool.

Source programs and downloaded advisory examples are never executed. Source
checks are distinct from issue-relevance decisions recorded in the review ledger.
"""

import argparse
import ast
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import difflib
import hashlib
import json
from pathlib import Path
import re
import sqlite3
import subprocess
import sys
import warnings
import zipfile
from urllib.parse import quote

from BUILD_CANDIDATE_SPLITS import normalise, save, sha
from BUILD_HAPY_SOURCE_PAIRS import changed_files, check_diff, functions
from PROBE_CANDIDATE_SOURCES import ast_without_docstrings, fetch
from SECURITY_EXPANSION_AUDIT import linked_cves, shingles


def read_rows(path):
    with path.open() as stream:
        return [json.loads(line) for line in stream]


def write_rows(path, rows):
    with path.open("w") as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False) + "\n")


def literal(value, default):
    try:
        return ast.literal_eval(value)
    except (ValueError, SyntaxError, TypeError):
        return default


def evidence(output, cache):
    rows = read_rows(output / "CVEFIXES_SECURITY_EXPANSION_FILTERED_CANDIDATES.jsonl")
    cves = sorted({c for row in rows for c in linked_cves(row)})
    db = sqlite3.connect(f"file:{output / 'CVEFIXES_PYTHON.sqlite'}?mode=ro", uri=True)
    original_refs = {c: literal(refs, []) for c, refs in db.execute("SELECT cve_id,reference_json FROM cve")}
    def collect(cve):
        year, number = cve.split("-")[1:]
        url = f"https://raw.githubusercontent.com/CVEProject/cvelistV5/main/cves/{year}/{int(number) // 1000}xxx/{cve}.json"
        result = {"cve_id": cve, "record_url": url, "original_references": original_refs.get(cve, [])}
        try:
            raw = fetch(url, cache)
            record = json.loads(raw)
            if record.get("cveMetadata", {}).get("cveId") != cve:
                raise ValueError("CVE identity mismatch")
            result["record_sha256"] = hashlib.sha256(raw).hexdigest()
            result["state"] = record["cveMetadata"]["state"]
            result["cna"] = record.get("containers", {}).get("cna", {})
            result["record"] = record
            refs = result["original_references"] + result["cna"].get("references", [])
            identifiers = {ghsa for ref in refs for ghsa in re.findall(r"GHSA-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}", ref.get("url", ""))}
            result["advisories"] = []
            for ghsa in sorted(identifiers):
                advisory_url = "https://api.osv.dev/v1/vulns/" + ghsa
                try:
                    advisory_raw = fetch(advisory_url, cache)
                    advisory = json.loads(advisory_raw)
                    if cve not in advisory.get("aliases", []):
                        raise ValueError("OSV advisory does not declare this CVE alias")
                    result["advisories"].append({"url": advisory_url, "sha256": hashlib.sha256(advisory_raw).hexdigest(), "record": advisory})
                except (ValueError, json.JSONDecodeError) as error:
                    result.setdefault("advisory_errors", []).append({"url": advisory_url, "error": str(error)[:200]})
        except (ValueError, KeyError) as error:
            result["error"] = str(error)[:250]
        return result
    results = []
    with (output / "SECURITY_ADMISSION_CVE_EVIDENCE.jsonl").open("w") as log, ThreadPoolExecutor(max_workers=6) as pool:
        futures = [pool.submit(collect, cve) for cve in cves]
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            log.write(json.dumps(result, ensure_ascii=False) + "\n")
            log.flush()
            if len(results) % 50 == 0:
                print(json.dumps({"cves_done": len(results), "cves_total": len(cves)}), flush=True)
    write_rows(output / "SECURITY_ADMISSION_CVE_EVIDENCE.jsonl", sorted(results, key=lambda r: r["cve_id"]))
    report = {"cves": len(results), "states": Counter(r.get("state", "unavailable") for r in results),
              "with_osv_advisory": sum(bool(r.get("advisories")) for r in results),
              "fetched_at_utc": datetime.now(timezone.utc).isoformat(), "errors": sum("error" in r for r in results)}
    save(output / "SECURITY_ADMISSION_EVIDENCE_AUDIT.json", report)
    print(json.dumps(report, indent=2))


def fingerprint(code):
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            node.decorator_list = []
    return ast_without_docstrings(ast.unparse(tree))


def contexts(output, cache):
    rows = read_rows(output / "CVEFIXES_SECURITY_EXPANSION_FILTERED_CANDIDATES.jsonl")
    db = sqlite3.connect(f"file:{output / 'CVEFIXES_PYTHON.sqlite'}?mode=ro", uri=True)
    db.row_factory = sqlite3.Row
    methods = {r["method_change_id"]: dict(r) for r in db.execute("SELECT method_change_id,start_line,end_line FROM method_change")}
    files, results, complete = {}, [], []
    for row in rows:
        checked = {"pair_id": row["pair_id"], "cves": row["cves"]}
        try:
            fid = row["file_change_id"]
            if fid not in files:
                file = dict(db.execute("SELECT * FROM file_change WHERE file_change_id=?", (fid,)).fetchone())
                raw_diff = file["diff"]
                if not raw_diff.startswith("diff --git"):
                    raw_diff = "diff --git a/x b/x\n--- a/x\n+++ b/x\n" + raw_diff
                parsed_diff = changed_files(raw_diff)
                if len(parsed_diff) != 1 or not parsed_diff[0]["hunks"]:
                    raise ValueError("Unsupported/empty file diff")
                changed = check_diff(parsed_diff[0], file["code_before"], file["code_after"])
                parsed = {s: functions(file["code_" + s]) for s in ("before", "after")}
                files[fid] = (file, changed, parsed)
            file, changed, parsed = files[fid]
            canonical = dict(row)
            qualified = []
            for side in ("before", "after"):
                method = methods[row["method_change_id_" + side]]
                matches = [(name, fn) for name, fn in parsed[side].items()
                           if fn["start"] <= int(method["start_line"]) <= fn["end"]
                           and fn["end"] == int(method["end_line"])
                           and fingerprint(fn["code"]) == fingerprint(row[side])]
                if len(matches) != 1:
                    raise ValueError(side + " method does not uniquely match full source")
                name, fn = matches[0]
                code, ast_hash, _ = normalise(fn["code"])
                canonical.update({side: code, side + "_sha256": sha(code), side + "_ast_sha256": ast_hash,
                                  side + "_start_line": fn["start"], side + "_end_line": fn["end"]})
                canonical[side + "_changed_lines"] = sorted(line for line in changed[side] if fn["start"] <= line <= fn["end"])
                qualified.append(name)
            if qualified[0] != qualified[1]:
                raise ValueError("Qualified method identity differs between versions")
            if not canonical["before_changed_lines"] and not canonical["after_changed_lines"]:
                raise ValueError("Function contains no changed line")
            if ast_without_docstrings(canonical["before"]) == ast_without_docstrings(canonical["after"]):
                raise ValueError("No executable AST change")
            canonical["qualified_function"] = qualified[0]
            canonical["full_file_text_sha256"] = {s: sha(file["code_" + s]) for s in ("before", "after")}
            canonical["source_context_check"] = "Complete released file snapshots parse; diff hunks match both versions; unique qualified decorated function slices match method metadata"
            complete.append(canonical)
            checked["status"] = "source_context_pass"
        except (ValueError, SyntaxError, TypeError, KeyError, IndexError) as error:
            checked.update({"status": "quarantine_source_context", "reason": str(error)[:220]})
        results.append(checked)
    write_rows(output / "SECURITY_ADMISSION_SOURCE_CONTEXTS.jsonl", complete)
    write_rows(output / "SECURITY_ADMISSION_SOURCE_DECISIONS.jsonl", results)
    report = {"input_pairs": len(rows), "passed": len(complete), "statuses": Counter(r["status"] for r in results),
              "pass_cves": len({c for r in complete for c in r["cves"]}),
              "quarantine_reasons": Counter(r["reason"] for r in results if "reason" in r)}
    save(output / "SECURITY_ADMISSION_SOURCE_AUDIT.json", report)
    print(json.dumps(report, indent=2))


def packets(output, cache):
    evidence_rows = {r["cve_id"]: r for r in read_rows(output / "SECURITY_ADMISSION_CVE_EVIDENCE.jsonl")}
    rows = read_rows(output / "SECURITY_ADMISSION_SOURCE_CONTEXTS.jsonl")
    packaged = []
    for row in rows:
        linked = [evidence_rows[c] for c in row["cves"]]
        descriptions = [d["value"] for e in linked for d in e.get("cna", {}).get("descriptions", []) if d.get("lang", "").startswith("en")]
        if not descriptions:
            descriptions = list(row["descriptions"].values())
        description = " ".join(descriptions)
        patch = [line for line in difflib.unified_diff(row["before"].splitlines(), row["after"].splitlines(), n=1)
                 if not line.startswith(("---", "+++", "@@"))]
        changed_text = "\n".join(line for line in patch if line[:1] in ("+", "-"))
        terms = r"sandbox|safe_load|safe_join|compare_digest|verify|escape|sanitize|quote|realpath|normpath|is_relative_to|\.\.\.|startswith|allowlist|whitelist|unpickle|pickle|subprocess|shell|redirect|password|secret|chmod|limit|max_|csrf|auth|resolve|travers|tarfile|extract|symlink|secure|deserialize|eval\(|exec\(|sha256|md5"
        score = len(re.findall(terms, changed_text.lower()))
        if row["function_before"] not in ("__init__", "__call__", "get", "post", "run", "main") and row["function_before"] in description:
            score += 10
        if any(e.get("state") != "PUBLISHED" for e in linked):
            score = -100
        packaged.append({"pair_id": row["pair_id"], "cves": row["cves"], "function": row["qualified_function"],
                         "path": row["path"], "repository": row["repository"], "score": score,
                         "description": description, "commit_message": row["commit"]["msg"], "patch": patch,
                         "advisories": [{"id": a["record"].get("id"), "details": a["record"].get("details", ""),
                                         "url": a["url"]} for e in linked for a in e.get("advisories", [])]})
    packaged.sort(key=lambda r: (-r["score"], r["cves"], r["pair_id"]))
    write_rows(output / "SECURITY_ADMISSION_REVIEW_PACKETS.jsonl", packaged)
    # Distinct-CVE first pass; compact packets are an index, not automatic admission.
    seen, first = set(), []
    for row in packaged:
        if set(row["cves"]) & seen:
            continue
        first.append(row)
        seen.update(row["cves"])
    for offset in range(0, len(first), 30):
        text = ["# Source/advisory review batch " + str(offset // 30 + 1), ""]
        for i, row in enumerate(first[offset:offset + 30], offset + 1):
            text += [f"## {i}. " + row["pair_id"] + " | " + ",".join(row["cves"]),
                     row["repository"] + " | " + row["function"] + " | " + row["path"],
                     "DESCRIPTION: " + row["description"][:500], "COMMIT: " + row["commit_message"][:160],
                     "```diff", "\n".join(row["patch"])[:2000], "```", ""]
        (output / f"SECURITY_ADMISSION_REVIEW_BATCH_{offset // 30 + 1:02}.md").write_text("\n".join(text))
    print(json.dumps({"packets": len(packaged), "distinct_cve_first_pass_packets": len(first)}, indent=2))


def decisions(output):
    ledger = json.loads((output / "SECURITY_ADMISSION_REVIEW_LEDGER.json").read_text())
    result = {r["pair_id"]: r for r in ledger["decisions"]}
    assert len(result) == len(ledger["decisions"]), "Duplicate manual decision"
    # Preserve the earlier pair-bound, upstream-verified four-case inspection.
    prior = json.loads((output / "CVEFIXES_SECURITY_EXPANSION_REVIEW_RESULTS.json").read_text())
    for row in prior["sample_reviews"]:
        if row["pair_id"] not in result and row["decision"] == "source_advisory_supported":
            result[row["pair_id"]] = {"pair_id": row["pair_id"], "status": "admit", "supported_cves": row["cves"],
                                      "reason": row["reason"], "prior_evidence": row}
    queue_review = output / "SECURITY_ADMISSION_QUEUE_REVIEW.json"
    if queue_review.exists():
        queue_path = output / "SECURITY_ADMISSION_REMAINING_QUEUE.jsonl"
        queue = read_rows(queue_path)
        review = json.loads(queue_review.read_text())
        assert review["queue_sha256"] == hashlib.sha256(queue_path.read_bytes()).hexdigest(), "Changed queue needs fresh decisions"
        seen = set()
        grouped = [{k: v for k, v in group.items() if k != "indices"} | {"index": i}
                   for group in review.get("groups", []) for i in group["indices"]]
        followups = [{k: v for k, v in group.items() if k != "indices"} | {"index": i, "followup": True}
                     for group in review.get("followups", []) for i in group["indices"]]
        updated = set()
        for decision in review["decisions"] + grouped + followups:
            number = decision["index"]
            is_followup = decision.get("followup", False)
            assert 1 <= number <= len(queue)
            assert (number in seen and number not in updated) if is_followup else number not in seen
            if is_followup:
                updated.add(number)
            seen.add(number)
            row = queue[number - 1]
            assert row["index"] == number and (is_followup or row["pair_id"] not in result)
            assert decision["status"] in {"admit", "reject", "quarantine"}
            record = {**decision, "pair_id": row["pair_id"], "reviewed_code_sha256": row["code_sha256"]}
            if is_followup:
                record["previous_review"] = result[row["pair_id"]]
            if record["status"] == "admit":
                record.setdefault("supported_cves", row["cves"] if len(row["cves"]) == 1 else [])
            result[row["pair_id"]] = record
    return ledger, result


def progress(output, cache):
    _, reviewed = decisions(output)
    rows = read_rows(output / "SECURITY_ADMISSION_REMAINING_QUEUE.jsonl")
    contexts_by_id = {r["pair_id"]: r for r in read_rows(output / "SECURITY_ADMISSION_SOURCE_CONTEXTS.jsonl")}
    missing = []
    for row in rows:
        decision = reviewed.get(row["pair_id"])
        if decision is None:
            missing.append(row["index"])
        elif row["pair_id"] in contexts_by_id:
            current = {s: contexts_by_id[row["pair_id"]][s + "_sha256"] for s in ("before", "after")}
            assert decision["reviewed_code_sha256"] == current, "Reviewed source changed"
    print(json.dumps({"recorded": len(rows) - len(missing), "missing_indices": missing}, indent=2))


def queue(output, cache):
    # Queue is an immutable, hash-bound index. Do not regenerate after reviewing it.
    target = output / "SECURITY_ADMISSION_REMAINING_QUEUE.jsonl"
    if target.exists():
        raise ValueError("Review queue already exists; preserve its indices and fingerprint")
    _, reviewed = decisions(output)
    original = read_rows(output / "CVEFIXES_SECURITY_EXPANSION_FILTERED_CANDIDATES.jsonl")
    contexts_by_id = {r["pair_id"]: r for r in read_rows(output / "SECURITY_ADMISSION_SOURCE_CONTEXTS.jsonl")}
    checks = {r["pair_id"]: r for r in read_rows(output / "SECURITY_ADMISSION_SOURCE_DECISIONS.jsonl")}
    records = {r["cve_id"]: r for r in read_rows(output / "SECURITY_ADMISSION_CVE_EVIDENCE.jsonl")}
    rows = sorted((r for r in original if r["pair_id"] not in reviewed),
                  key=lambda r: (r["cves"], r["repository"], r["fixing_commit"], r["path"], r["pair_id"]))
    class NoDocstrings(ast.NodeTransformer):
        def visit_FunctionDef(self, node):
            self.generic_visit(node)
            if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant) and isinstance(node.body[0].value.value, str):
                node.body.pop(0)
            return node
        visit_AsyncFunctionDef = visit_FunctionDef
    queue_rows, text, last_cves = [], [], None
    for i, original_row in enumerate(rows, 1):
        row = contexts_by_id.get(original_row["pair_id"], original_row)
        entry = {"index": i, "pair_id": row["pair_id"], "cves": row["cves"],
                 "code_sha256": {s: row[s + "_sha256"] for s in ("before", "after")},
                 "source_check": checks[row["pair_id"]]}
        queue_rows.append(entry)
        if (i - 1) % 50 == 0:
            text, last_cves = [], None
        if row["cves"] != last_cves:
            text.append("\n## " + ",".join(row["cves"]))
            for c in row["cves"]:
                descriptions = [d["value"] for d in records[c].get("cna", {}).get("descriptions", []) if d.get("lang", "").startswith("en")]
                text.append(c + ": " + " ".join(descriptions)[:430])
            last_cves = row["cves"]
        text.append(f"\n{i}. {row['repository']} {row.get('qualified_function', row['function_before'])} [{row['path']}]")
        if checks[row["pair_id"]]["status"] != "source_context_pass":
            text.append("SOURCE BLOCKED: " + checks[row["pair_id"]]["reason"])
        else:
            versions = {s: ast.unparse(NoDocstrings().visit(ast.parse(row[s]))) for s in ("before", "after")}
            diff = "\n".join(line for line in difflib.unified_diff(versions["before"].splitlines(), versions["after"].splitlines(), n=0)
                             if not line.startswith(("---", "+++", "@@")))
            text.extend(["```diff", diff[:1300], "```" + (" [TRUNCATED; inspect full source before admission]" if len(diff) > 1300 else "")])
        if i % 50 == 0 or i == len(rows):
            (output / f"SECURITY_ADMISSION_REMAINING_BATCH_{(i - 1) // 50 + 1:02}.md").write_text("\n".join(text) + "\n")
    write_rows(target, queue_rows)
    fingerprint = hashlib.sha256(target.read_bytes()).hexdigest()
    print(json.dumps({"remaining": len(rows), "queue_sha256": fingerprint}, indent=2))


def upstream(output, cache):
    _, ledger = decisions(output)
    rows = [r for r in read_rows(output / "SECURITY_ADMISSION_SOURCE_CONTEXTS.jsonl")
            if ledger.get(r["pair_id"], {}).get("status") == "admit"]
    db = sqlite3.connect(f"file:{output / 'CVEFIXES_PYTHON.sqlite'}?mode=ro", uri=True)
    paths = {r[0]: r[1:] for r in db.execute("SELECT file_change_id,old_path,new_path FROM file_change")}
    location_path = output / "SECURITY_ADMISSION_SOURCE_LOCATIONS.json"
    locations = json.loads(location_path.read_text()) if location_path.exists() else {}
    companion_sources = {}
    def source_url(repository, commit, path):
        if repository.startswith("github.com/"):
            return f"https://raw.githubusercontent.com/{repository.removeprefix('github.com/')}/{commit}/{quote(path)}"
        if repository.startswith("gitlab.com/"):
            return f"https://{repository}/-/raw/{commit}/{quote(path)}"
        raise ValueError("Unsupported upstream source host: " + repository)
    for row in rows:
        for item in ledger[row["pair_id"]].get("companion_functions", []):
            key = (row["fixing_commit"], item["path"])
            matches = db.execute("SELECT code_after FROM file_change WHERE hash=? AND new_path=?", key).fetchall()
            assert len(matches) == 1, "Companion source is not uniquely bound to fixing commit"
            companion_sources[key] = matches[0][0]
    def check(row):
        result = {"pair_id": row["pair_id"], "snapshots": {}, "companion_snapshots": []}
        try:
            parent = literal(row["commit"]["parents"], [])[0]
            location = locations.get(row["repository"])
            retrieval_repository = location["repository"] if location else row["repository"]
            if location:
                if not retrieval_repository.startswith("github.com/"):
                    raise ValueError("Alternate source location requires GitHub commit metadata verification")
                commit_url = f"https://api.github.com/repos/{retrieval_repository.removeprefix('github.com/')}/commits/{row['fixing_commit']}"
                commit_raw = fetch(commit_url, cache)
                commit_record = json.loads(commit_raw)
                if commit_record["sha"] != row["fixing_commit"] or commit_record["parents"][0]["sha"] != parent:
                    raise ValueError("Alternate repository commit or first parent differs from released metadata")
                result["source_location_evidence"] = {
                    "original_repository": row["repository"], "retrieval_repository": retrieval_repository,
                    "reason": location["reason"], "commit_record_url": commit_url,
                    "commit_record_sha256": hashlib.sha256(commit_raw).hexdigest(),
                    "commit_record_text": commit_raw.decode("utf-8")}
            for side, commit, path in (("before", parent, paths[row["file_change_id"]][0]),
                                       ("after", row["fixing_commit"], paths[row["file_change_id"]][1])):
                url = source_url(retrieval_repository, commit, path)
                raw = fetch(url, cache)
                source = raw.decode("utf-8-sig")
                fn = functions(source)[row["qualified_function"]]
                code, ast_hash, _ = normalise(fn["code"])
                if code != row[side] or ast_hash != row[side + "_ast_sha256"]:
                    raise ValueError(side + " complete decorated function differs from upstream")
                result["snapshots"][side] = {"url": url, "sha256": hashlib.sha256(raw).hexdigest(),
                    "source_text_sha256": sha(source), "function_start": fn["start"], "function_end": fn["end"],
                    "released_full_file_text_matches": sha(source) == row["full_file_text_sha256"][side]}
                if location and not result["snapshots"][side]["released_full_file_text_matches"]:
                    raise ValueError("Alternate repository complete module differs from released source")
            for item in ledger[row["pair_id"]].get("companion_functions", []):
                url = source_url(retrieval_repository, row["fixing_commit"], item["path"])
                raw = fetch(url, cache)
                source = raw.decode("utf-8-sig")
                expected = companion_sources[(row["fixing_commit"], item["path"])]
                if source != expected:
                    raise ValueError("Companion complete module differs from released source")
                fn = functions(source)[item["function"]]
                result["companion_snapshots"].append({"url": url, "sha256": hashlib.sha256(raw).hexdigest(),
                    "qualified_function": item["function"], "function_sha256": sha(normalise(fn["code"])[0]),
                    "function_start": fn["start"], "function_end": fn["end"]})
            # Configuration and unchanged modules may be essential evidence but
            # absent from the released Python-only file-change table. Require
            # an explicit review-time byte hash at this exact fixing commit.
            for item in ledger[row["pair_id"]].get("context_files", []):
                if item["path"].startswith("/") or ".." in item["path"].split("/"):
                    raise ValueError("Context path must be repository-relative")
                url = source_url(retrieval_repository, row["fixing_commit"], item["path"])
                raw = fetch(url, cache)
                digest = hashlib.sha256(raw).hexdigest()
                if digest != item["sha256"]:
                    raise ValueError("Context file differs from review-time hash")
                result.setdefault("context_snapshots", []).append({
                    "url": url, "sha256": digest, "path": item["path"]})
            result["status"] = "both_complete_functions_match_upstream"
        except (ValueError, KeyError, IndexError, UnicodeError, SyntaxError) as error:
            result.update({"status": "quarantine_upstream", "reason": str(error)[:250]})
        return result
    with ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(check, rows))
    write_rows(output / "SECURITY_ADMISSION_UPSTREAM_CHECKS.jsonl", results)
    print(json.dumps({"attempted": len(results), "statuses": Counter(r["status"] for r in results)}, indent=2))


def export(output, cache):
    ledger, reviewed = decisions(output)
    original = read_rows(output / "CVEFIXES_SECURITY_EXPANSION_FILTERED_CANDIDATES.jsonl")
    contexts_by_id = {r["pair_id"]: r for r in read_rows(output / "SECURITY_ADMISSION_SOURCE_CONTEXTS.jsonl")}
    source_checks = {r["pair_id"]: r for r in read_rows(output / "SECURITY_ADMISSION_SOURCE_DECISIONS.jsonl")}
    records = {r["cve_id"]: r for r in read_rows(output / "SECURITY_ADMISSION_CVE_EVIDENCE.jsonl")}
    probes = {r["pair_id"]: r for r in read_rows(output / "SECURITY_ADMISSION_UPSTREAM_CHECKS.jsonl")}
    database = sqlite3.connect(f"file:{output / 'CVEFIXES_PYTHON.sqlite'}?mode=ro", uri=True)
    cwe_by_cve = {}
    for cve, cwe in database.execute("SELECT cve_id,cwe_id FROM cwe_classification"):
        cwe_by_cve.setdefault(cve, set()).add(cwe)
    assert set(reviewed) <= {r["pair_id"] for r in original}, "Stale review IDs"
    hapy = read_rows(output / "HAPY_BUG_CANDIDATE_PAIRS.jsonl")
    old_codes = {r[s + suffix] for r in hapy for s in ("before", "after") for suffix in ("_sha256", "_ast_sha256")}
    old_shingles = [shingles(r[s]) for r in hapy for s in ("before", "after")]
    admitted, final = [], []
    for original_row in original:
        pid = original_row["pair_id"]
        decision = reviewed.get(pid, {"pair_id": pid, "status": "quarantine", "reason":
            "No pair-specific issue-relevance inspection has been recorded; source/advisory presence alone is not admission."})
        decision = {**decision, "reviewer": ledger["reviewer"], "original_commit_linked_cves": original_row["cves"],
                    "review_decision_recorded": pid in reviewed,
                    "issue_relevance_inspection_recorded": pid in reviewed and source_checks[pid]["status"] == "source_context_pass"
                    and decision.get("inspection_scope") != "source_blocked"}
        if pid in contexts_by_id and "reviewed_code_sha256" in decision:
            assert decision["reviewed_code_sha256"] == {s: contexts_by_id[pid][s + "_sha256"] for s in ("before", "after")}, "Reviewed source changed"
        if source_checks[pid]["status"] != "source_context_pass":
            decision.update({"status": "quarantine", "reason": "Source-context check failed: " + source_checks[pid]["reason"]})
        if decision["status"] == "admit":
            row = dict(contexts_by_id[pid])
            supported = decision["supported_cves"]
            assert supported and set(supported) <= set(original_row["cves"]), "Unsupported CVE attribution"
            why = None
            for cve in supported:
                evidence_row = records[cve]
                description = json.dumps(evidence_row.get("cna", {})).lower()
                if evidence_row.get("state") != "PUBLISHED" or '"disputed"' in description or "** disputed **" in description:
                    why = "CVE is not an undisputed published record"
                if any(a["record"].get("withdrawn") for a in evidence_row.get("advisories", [])):
                    why = "An associated OSV advisory is withdrawn"
            probe = probes.get(pid, {})
            if probe.get("status") != "both_complete_functions_match_upstream":
                why = "Upstream function verification failed or missing: " + probe.get("reason", "no matching check")
            if any(row[s + suffix] in old_codes for s in ("before", "after") for suffix in ("_sha256", "_ast_sha256")):
                why = "Canonical function overlaps HaPy exact text/AST"
            if any(len(a & b) / len(a | b) >= .9 for s in ("before", "after")
                   for a in (shingles(row[s]),) for b in old_shingles
                   if min(len(a), len(b)) / max(len(a), len(b)) >= .9):
                why = "Canonical function overlaps HaPy at shingle Jaccard >=0.90"
            if why:
                decision.update({"status": "quarantine", "reason": why, "inspection_reason": decision["reason"]})
            else:
                row.update({"commit_linked_cves": row["cves"], "cves": supported, "issue_group": "security_candidate",
                            "label_status": "assistant_source_advisory_supported_not_independent_human_gold",
                            "reference_validity": decision["reason"], "admission_review": decision,
                             "upstream_snapshots": probe["snapshots"], "companion_snapshots": probe.get("companion_snapshots", []), "advisory_evidence": [
                                {"cve_id": c, "record_url": records[c]["record_url"], "record_sha256": records[c]["record_sha256"]}
                                 for c in supported]})
                if "source_location_evidence" in probe:
                    row["source_location_evidence"] = probe["source_location_evidence"]
                if probe.get("context_snapshots"):
                    row["context_snapshots"] = probe["context_snapshots"]
                # Keep every source linkage for split grouping, even those not admitted as issue labels.
                row["duplicate_pair_provenance"] = row.get("duplicate_pair_provenance", []) + [{
                    "pair_id": pid, "repository": row["repository"], "fixing_commit": row["fixing_commit"],
                    "cves": row["commit_linked_cves"]}]
                row["descriptions"] = {c: row["descriptions"][c] for c in supported}
                row["commit_linked_cwes"] = row["cwes"]
                row["cwes"] = sorted({w for c in supported for w in cwe_by_cve.get(c, set())})
                row["cwe_provenance"] = "Source CVE-level metadata; not independently adjudicated function-level CWE labels"
                decision["inspected_code_sha256"] = {s: row[s + "_sha256"] for s in ("before", "after")}
                admitted.append(row)
        final.append(decision)
    assert len(final) == len(original)
    combined, keys = [], set()
    for row in hapy + admitted:
        key = (row["before_ast_sha256"], row["after_ast_sha256"])
        assert key not in keys, "Canonical AST-pair duplicate needs explicit provenance collapse"
        keys.add(key)
        combined.append(row)
    write_rows(output / "CVEFIXES_SECURITY_ADMITTED_PAIRS.jsonl", admitted)
    write_rows(output / "SECURITY_ADMISSION_FINAL_DECISIONS.jsonl", final)
    unresolved = []
    for decision in final:
        if decision["status"] != "quarantine":
            continue
        pid = decision["pair_id"]
        blocker = "source_context" if source_checks[pid]["status"] != "source_context_pass" else (
            "upstream_match" if reviewed.get(pid, {}).get("status") == "admit" else "issue_context_or_attribution")
        unresolved.append({**decision, "blocker_type": blocker})
    write_rows(output / "SECURITY_ADMISSION_UNRESOLVED_REVIEW.jsonl", unresolved)
    write_rows(output / "HAPY_CVEFIXES_ADMITTED_CANDIDATE_PAIRS.jsonl", combined)
    # Preserve unmodified full upstream files, including headers and companion-function context.
    snapshot_index, written = {}, set()
    with zipfile.ZipFile(output / "SECURITY_ADMISSION_UPSTREAM_SNAPSHOTS.zip", "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for row in admitted:
            for snapshot in (list(row["upstream_snapshots"].values()) + row.get("companion_snapshots", [])
                             + row.get("context_snapshots", [])):
                raw = fetch(snapshot["url"], cache)
                digest = hashlib.sha256(raw).hexdigest()
                assert digest == snapshot["sha256"]
                suffix = Path(snapshot["path"]).suffix if "path" in snapshot else ".py"
                member = "source/" + digest + suffix
                if member not in written:
                    info = zipfile.ZipInfo(member, date_time=(1980, 1, 1, 0, 0, 0))
                    archive.writestr(info, raw, compress_type=zipfile.ZIP_DEFLATED)
                    written.add(member)
                snapshot_index[snapshot["url"]] = {"member": member, "sha256": digest}
        archive.writestr("index.json", json.dumps(snapshot_index, indent=2))
    audit = {"input_pairs": len(original), "decision_counts": Counter(r["status"] for r in final),
             "recorded_decisions": sum(r["review_decision_recorded"] for r in final),
             "source_blocked_pairs": sum(r["status"] != "source_context_pass" for r in source_checks.values()),
             "quarantine_blockers": Counter(r["blocker_type"] for r in unresolved),
             "proposed_admissions": sum(r["status"] == "admit" for r in reviewed.values()),
             "pair_specific_inspections_recorded": sum(r["issue_relevance_inspection_recorded"] for r in final),
             "not_issue_reviewed_and_quarantined": sum(not r["issue_relevance_inspection_recorded"] for r in final),
             "additional_security_pairs": len(admitted), "additional_security_cves": len({c for r in admitted for c in r["cves"]}),
             "additional_repositories": len({r["repository"] for r in admitted}), "combined_pairs": len(combined),
             "combined_issue_groups": Counter(r["issue_group"] for r in combined),
             "combined_security_cves": len({c for r in combined for c in r["cves"]}),
             "preserved_upstream_files": len(written), "reviewer": ledger["reviewer"],
              "status": "Full-pool triage decisions recorded; contextual quarantines remain unresolved. Admitted source/advisory snapshot is not independent human adjudication.",
             "limits": ["Source/advisory inspection is assistant-generated, distinct from HaPy human line labels",
                        "No reproduced vulnerability tests or independent human adjudication", "After-code is not universally clean",
                        "Nonrandom review priority is not a population quality estimate", "No model or final evaluation protocol selected"]}
    save(output / "SECURITY_ADMISSION_AUDIT.json", audit)
    print(json.dumps(audit, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("evidence", "contexts", "packets", "queue", "progress", "upstream", "export"))
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--cache-dir", type=Path, required=True)
    parser.add_argument("--background", action="store_true")
    args = parser.parse_args()
    if not args.output_dir.is_dir() or not args.cache_dir.is_dir():
        parser.error("Existing output/cache directories required")
    if args.background:
        log = args.cache_dir / ("security-admission-" + args.stage + ".log")
        with log.open("a") as stream:
            process = subprocess.Popen([sys.executable, str(Path(__file__).resolve()), args.stage,
                                        "--output-dir", str(args.output_dir), "--cache-dir", str(args.cache_dir)],
                                       stdout=stream, stderr=stream, start_new_session=True)
        print(json.dumps({"pid": process.pid, "log": str(log)}))
    else:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", SyntaxWarning)
            {"evidence": evidence, "contexts": contexts, "packets": packets, "queue": queue, "progress": progress, "upstream": upstream, "export": export}[args.stage](args.output_dir, args.cache_dir)
