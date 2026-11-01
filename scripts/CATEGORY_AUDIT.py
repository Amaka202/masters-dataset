"""Resumable category audit. Dataset/source text is data, never executable code.

Only init/refresh/check write files, and only CATEGORY_AUDIT_* audit artefacts.
Queue order: alternate sorted correctness/security training IDs, starting with
correctness. Revisions are appended to the ledger; latest revision wins.
"""

import argparse
import ast
from collections import Counter, defaultdict
import csv
import difflib
import hashlib
import json
from pathlib import Path
import textwrap
import zipfile


ROOT = Path(__file__).resolve().parent
PREFIX = "HAPY_CVEFIXES_ADMITTED"
SPLITS = ("train", "validation", "test")
REVIEW_BATCH_SIZE = 50


def sha(value):
    return hashlib.sha256(value if isinstance(value, bytes) else value.encode()).hexdigest()


def file_sha(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load(name):
    return json.loads((ROOT / name).read_text())


def rows(name):
    return [json.loads(line) for line in (ROOT / name).read_text().splitlines() if line.strip()]


def save(name, value):
    (ROOT / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def protected_inputs():
    release = load("SECURITY_ADMISSION_RELEASE_MANIFEST.json")
    protected = {}
    for name, item in release["files"].items():
        path = ROOT / name
        actual = file_sha(path)
        if actual != item["sha256"]:
            raise ValueError(f"Released input changed: {name}")
        protected[name] = actual
    for name in ("SECURITY_ADMISSION_RELEASE_MANIFEST.json", "HAPY_BUG_CASE_METADATA.json"):
        protected[name] = file_sha(ROOT / name)
    return dict(sorted(protected.items()))


def dataset():
    canonical = rows(PREFIX + "_CANDIDATE_PAIRS.jsonl")
    master = {r["pair_id"]: r for r in canonical}
    assert len(master) == len(canonical) == 1052
    selected = {}
    for split in SPLITS:
        for row in rows(f"{PREFIX}_{split.upper()}_CANDIDATES.jsonl"):
            pid = row["pair_id"]
            assert pid not in selected and row["split"] == split
            assert {k: v for k, v in row.items() if k != "split"} == master[pid]
            selected[pid] = row
    assert selected.keys() == master.keys()
    return selected


def components(data, provenance=False):
    """Mechanical families, NOT independently adjudicated issue identities."""
    parent = {pid: pid for pid in data}

    def root(pid):
        while parent[pid] != pid:
            parent[pid] = parent[parent[pid]]
            pid = parent[pid]
        return pid

    seen = {}
    for pid, row in sorted(data.items()):
        records = [row] + row.get("duplicate_pair_provenance", [])
        keys = []
        for item in records:
            keys.append("commit:" + item["repository"] + ":" + item["fixing_commit"])
            keys.extend("cve:" + c for c in item.get("cves", []) + item.get("commit_linked_cves", []))
            if provenance:
                keys.append("repo:" + item["repository"])
        keys.append("pair:" + row["before_ast_sha256"] + ":" + row["after_ast_sha256"])
        if provenance:
            keys.extend(kind + ":" + row[side + suffix]
                        for side in ("before", "after")
                        for kind, suffix in (("text", "_sha256"), ("ast", "_ast_sha256")))
        for key in keys:
            if key in seen:
                parent[root(pid)] = root(seen[key])
            else:
                seen[key] = pid
    families = defaultdict(list)
    for pid in data:
        families[root(pid)].append(pid)
    return {pid: ("provenance:" if provenance else "fix-family:") + sha("\n".join(sorted(members)))[:20]
            for members in families.values() for pid in members}


def queue(data):
    buckets = [[pid for pid, row in sorted(data.items())
                if row["split"] == "train" and row["issue_group"] == domain]
               for domain in ("correctness_candidate", "security_candidate")]
    return [bucket[i] for i in range(max(map(len, buckets))) for bucket in buckets if i < len(bucket)]


def ledger(data, families):
    path = ROOT / "CATEGORY_AUDIT_LEDGER.jsonl"
    events = rows(path.name) if path.exists() else []
    latest = {}
    definitions = load("CATEGORY_AUDIT_CATEGORIES.json")
    assert definitions["status"] == "draft_training_only_not_frozen"
    categories = {c["category_id"] for c in definitions["categories"]}
    assert len(categories) == len(definitions["categories"])
    assert all(data[c["training_seed"]]["split"] == "train" for c in definitions["categories"])
    for event in events:
        pid = event["pair_id"]
        row = data[pid]
        assert row["split"] == "train", "Held-out audit requires a frozen training taxonomy/protocol update"
        assert event["revision"] == latest.get(pid, {}).get("revision", 0) + 1
        assert event["category_id"] in categories | {None}
        assert event["issue_family_id"] == families[pid]
        assert event["inspected_code_sha256"] == {side: row[side + "_sha256"] for side in ("before", "after")}
        assert event["review_status"] in ("assistant_supported", "assistant_ambiguous", "assistant_proposed_exclusion")
        assert event["researcher_status"] == "pending", "Researcher adjudication needs an explicit protocol extension"
        assert event["reviewer"] == "assistant" and event["evidence"] and event["reason"] and event["open_questions"]
        assert event["function_only_observability"] and event["negative_scope"] and event["review_date"]
        assert event.get("taxonomy_version", "0.1") in {definitions["version"], *definitions.get("previous_versions", [])}
        if "overlaps_pair_id" in event:
            outer = data[event["overlaps_pair_id"]]
            assert (row["repository"], row["fixing_commit"], row["path"]) == (
                outer["repository"], outer["fixing_commit"], outer["path"])
            for side in ("before", "after"):
                assert outer[side + "_start_line"] <= row[side + "_start_line"]
                assert row[side + "_end_line"] <= outer[side + "_end_line"]
        for inner_pid in event.get("contains_pair_ids", []):
            inner = data[inner_pid]
            assert (row["repository"], row["fixing_commit"], row["path"]) == (
                inner["repository"], inner["fixing_commit"], inner["path"])
            for side in ("before", "after"):
                assert row[side + "_start_line"] <= inner[side + "_start_line"]
                assert inner[side + "_end_line"] <= row[side + "_end_line"]
        latest[pid] = event
    return events, latest


def source(row, side):
    if row["source"] == "HaPy-Bug":
        name = "HAPY_BUG_UPSTREAM_SNAPSHOTS.zip"
        member = "sources/" + sha(row["source_urls"][side]) + ".py"
        expected = row["full_file_sha256"][side]
    else:
        name = "SECURITY_ADMISSION_UPSTREAM_SNAPSHOTS.zip"
        snapshot = row["upstream_snapshots"][side]
        with zipfile.ZipFile(ROOT / name) as archive:
            item = json.loads(archive.read("index.json"))[snapshot["url"]]
        member, expected = item["member"], snapshot["sha256"]
    with zipfile.ZipFile(ROOT / name) as archive:
        raw = archive.read(member)
    assert sha(raw) == expected
    lines = raw.decode("utf-8-sig").splitlines(keepends=True)
    start, end = row[side + "_start_line"], row[side + "_end_line"]
    assert textwrap.dedent("".join(lines[start - 1:end])).strip() + "\n" == row[side]
    return lines, {"archive": name, "member": member, "sha256": expected, "start": start, "end": end}


def inspect(data, pid, context, helpers=()):
    row = data[pid]
    if row["split"] != "train":
        raise ValueError("Taxonomy is training-only and not frozen; held-out inspection disabled")
    fields = ("pair_id", "repository", "fixing_commit", "issue_group", "cves", "qualified_function", "path",
              "before_sha256", "after_sha256", "commit_message", "commit", "reference_lines", "descriptions")
    print(json.dumps({k: row[k] for k in fields if k in row}, indent=2))
    if row["source"] == "HaPy-Bug":
        case = next(c for c in load("HAPY_BUG_CASE_METADATA.json") if c["case_id"] == row["hapy_case_id"])
        commit = next(c for c in case["commits"] if c["index"] == row["hapy_commit_index"])
        print("CASE COMMIT", json.dumps(commit, indent=2))
    else:
        evidence = {r["cve_id"]: r for r in rows("SECURITY_ADMISSION_CVE_EVIDENCE.jsonl")}
        print("CVE EVIDENCE", json.dumps([
            {"cve_id": c, "record_url": evidence[c]["record_url"], "record_sha256": evidence[c]["record_sha256"],
             "cna": {k: evidence[c]["cna"].get(k) for k in ("title", "descriptions", "problemTypes", "references")},
             "advisories": [{"url": a["url"], "sha256": a["sha256"],
                             "details": a["record"].get("details"), "aliases": a["record"].get("aliases")}
                            for a in evidence[c].get("advisories", [])]} for c in row["cves"]], indent=2))
    for side in ("before", "after"):
        lines, proof = source(row, side)
        print(side.upper(), json.dumps(proof))
        if helpers:
            tree = ast.parse("".join(lines))
            found = set()
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in helpers:
                    found.add(node.name)
                    start = min([node.lineno] + [d.lineno for d in node.decorator_list])
                    print(f"HELPER {node.name} {start}-{node.end_lineno}")
                    print("".join(f"{i}: {lines[i - 1]}" for i in range(start, node.end_lineno + 1)))
            print("HELPERS NOT FOUND IN THIS SNAPSHOT", sorted(set(helpers) - found))
            continue
        if context:
            lo, hi = max(1, proof["start"] - context), min(len(lines), proof["end"] + context)
            print("".join(f"{i}: {lines[i - 1]}" for i in range(lo, hi + 1)))
        else:
            print(row[side])
    print("DIFF\n" + "\n".join(difflib.unified_diff(row["before"].splitlines(), row["after"].splitlines())))


def refresh(data, protected):
    assert protected == load("CATEGORY_AUDIT_INPUTS.json")["sha256"], "Audit inputs changed"
    families, provenance = components(data), components(data, True)
    events, latest = ledger(data, families)
    # Every currently observed provenance component must remain within one split.
    grouped = defaultdict(set)
    for pid, group in provenance.items():
        grouped[group].add(data[pid]["split"])
    assert all(len(splits) == 1 for splits in grouped.values())
    for pid in latest:
        for side in ("before", "after"):
            source(data[pid], side)
    categories = load("CATEGORY_AUDIT_CATEGORIES.json")["categories"]
    fields = ["category_id", "split", "reviewed_pairs", "assistant_supported_pairs", "ambiguous_pairs",
              "proposed_exclusions", "distinct_provisional_fix_families", "repository_identities",
              "provenance_components", "researcher_approved_pairs", "audited_independent_issue_count",
              "heldout_screening_floor", "thin_category_status"]
    with (ROOT / "CATEGORY_AUDIT_COUNTS.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for category in [c["category_id"] for c in categories] + ["UNRESOLVED"]:
            for split in SPLITS:
                chosen = [pid for pid, e in latest.items()
                          if (e["category_id"] or "UNRESOLVED") == category and data[pid]["split"] == split]
                supported = [pid for pid in chosen if latest[pid]["review_status"] == "assistant_supported"]
                writer.writerow(dict(zip(fields, [category, split, len(chosen), len(supported),
                    sum(latest[p]["review_status"] == "assistant_ambiguous" for p in chosen),
                    sum(latest[p]["review_status"] == "assistant_proposed_exclusion" for p in chosen),
                    len({families[p] for p in supported}), len({data[p]["repository"] for p in supported}),
                    len({provenance[p] for p in supported}), 0, "", 30,
                    "not_assessable_incomplete_audit" if split == "test" else "not_applicable"])))
    pending = [pid for pid in queue(data) if pid not in latest]
    totals = {split: sum(r["split"] == split for r in data.values()) for split in SPLITS}
    supported = [p for p, e in latest.items() if e["review_status"] == "assistant_supported"]
    statuses = Counter(e["review_status"] for e in latest.values())
    checkpoint_date = max((event["review_date"] for event in events), default="2026-10-22")
    progress = ["# Category audit checkpoint", "", f"Checkpoint (latest recorded review): {checkpoint_date}. Taxonomy: draft, training-only.",
                "", f"- Unique candidates provisionally reviewed: **{len(latest)} / {len(data)}** ({len(events)} ledger events).",
                f"- Assistant-supported mechanisms: **{statuses['assistant_supported']}**; ambiguous: **{statuses['assistant_ambiguous']}**; proposed exclusions: **{statuses['assistant_proposed_exclusion']}**.",
                f"- Reviewed candidates span **{len({families[p] for p in latest})} provisional fix families**; supported candidates span **{len({families[p] for p in supported})}**. Neither is an audited independent count.",
                f"- Training remaining: **{len(pending)} / {totals['train']}**.",
                f"- Validation unreviewed: **{totals['validation']}**; test unreviewed: **{totals['test']}**.",
                "- Researcher-approved labels and independently confirmed issue groups: **none yet**.",
                "- Empty independent-count cells mean unknown, not zero; no test thin-category determination yet.",
                "- Released inputs match their original manifest; split membership/content verified.", "",
                f"- Draft taxonomy version **{load('CATEGORY_AUDIT_CATEGORIES.json')['version']}**: **{len(categories)}** mechanism labels, not a final evaluation taxonomy.",
                "",
                "## Mechanical inventory (not audited independent counts)", "",
                "| Split | Pairs | Repository identities | Provisional fix families | Provenance components |",
                "|---|---:|---:|---:|---:|"]
    for split in SPLITS:
        ids = [p for p in data if data[p]["split"] == split]
        progress.append(f"| {split} | {len(ids)} | {len({data[p]['repository'] for p in ids})} | "
                        f"{len({families[p] for p in ids})} | {len({provenance[p] for p in ids})} |")
    progress += ["", f"Across all splits: **{len({r['repository'] for r in data.values()})}** repository identities.",
                 "The previously quoted 151 is the CVEfixes additional-repository count (SECURITY_ADMISSION_AUDIT.json), not the combined total.",
                 "Provenance components join known repository/CVE/fix/exact/AST links; they are not a proof of statistical independence."]
    if pending:
        progress += ["", "## Exact next training batch", "", "Continue these original IDs in order (completed IDs are skipped):", ""]
        progress += [f"{i}. `{pid}`" for i, pid in enumerate(pending[:REVIEW_BATCH_SIZE], 1)]
    else:
        progress += ["", "## Training discovery complete — consolidation next", "",
                     "All training candidates have provisional reviews. The training queue is empty.",
                     "Researcher approval is not ready: consolidate the training-derived taxonomy, resolve eligibility/context decisions and reconcile issue/version dependence first.",
                     "The first hierarchy proposal and exhaustive review queues are in CATEGORY_AUDIT_CONSOLIDATION_REPORT.md and CATEGORY_AUDIT_CONSOLIDATION_REVIEW.md.",
                     "Use the consolidation handoff in CATEGORY_AUDIT_PROTOCOL.md; verify and freeze the resulting protocol before held-out category adjudication."]
    progress += ["", "## Open decisions", ""]
    progress += [f"- `{pid}`: {question}" for pid, event in latest.items() for question in event["open_questions"]]
    progress += ["- Finish training evidence review and researcher verification; freeze taxonomy before held-out category review." if pending else
                 "- Consolidate taxonomy, eligibility and bounded context; reconcile independence, then prepare researcher verification and freeze before held-out category review.",
                 "- Resolve aliases/backports/common root causes before claiming independent issue counts.",
                 "- Record general-bug security ambiguity and function-only observability; no provenance-only negatives.",
                 "", "## Resume", "", "```sh", "python3 CATEGORY_AUDIT.py refresh"]
    if pending:
        progress += [f"python3 CATEGORY_AUDIT.py queue --limit {REVIEW_BATCH_SIZE}",
                     'python3 CATEGORY_AUDIT.py inspect --pair-id "<exact ID above>" --context 15']
    else:
        progress += ["python3 CATEGORY_AUDIT.py check", "python3 CATEGORY_AUDIT_CONSOLIDATE.py check"]
    progress += ["```",
                 "", "See CATEGORY_AUDIT_PROTOCOL.md for decisions, counts and append-only revision rules.",
                 "", "## Checkpoint fingerprints", ""]
    progress += [f"- `{name}`: `{file_sha(ROOT / name)}`" for name in (
        "CATEGORY_AUDIT_LEDGER.jsonl", "CATEGORY_AUDIT_CATEGORIES.json", "CATEGORY_AUDIT_PROTOCOL.md",
        "CATEGORY_AUDIT_INPUTS.json", "CATEGORY_AUDIT.py", "CATEGORY_AUDIT_COUNTS.csv")]
    progress.append("")
    (ROOT / "CATEGORY_AUDIT_PROGRESS.md").write_text("\n".join(progress))
    print(json.dumps({"reviewed": len(latest), "training_remaining": len(pending), "protected_files_verified": len(protected),
                      "review_statuses": Counter(e["review_status"] for e in latest.values()), "next": pending[:2]}, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("init", "refresh", "check", "queue", "inspect"))
    parser.add_argument("--limit", type=int, default=REVIEW_BATCH_SIZE)
    parser.add_argument("--pair-id")
    parser.add_argument("--context", type=int, default=0)
    parser.add_argument("--helpers", default="", help="Comma-separated helper names in the same pinned full-file snapshot")
    args = parser.parse_args()
    data = dataset()
    if args.command == "init":
        path = ROOT / "CATEGORY_AUDIT_INPUTS.json"
        if path.exists():
            raise ValueError("Input lock already exists; use refresh")
        save(path.name, {"created": "2026-10-22", "sha256": protected_inputs()})
    elif args.command in ("refresh", "check"):
        generated = ("CATEGORY_AUDIT_COUNTS.csv", "CATEGORY_AUDIT_PROGRESS.md")
        before = {name: file_sha(ROOT / name) for name in generated} if args.command == "check" else None
        refresh(data, protected_inputs())
        if before is not None:
            assert before == {name: file_sha(ROOT / name) for name in generated}, "Generated checkpoint was stale; refreshed"
            print("Generated CSV/checkpoint are reproducible; all validation checks passed.")
    elif args.command == "queue":
        families = components(data)
        _, latest = ledger(data, families)
        pending = [pid for pid in queue(data) if pid not in latest]
        print(json.dumps([{"pair_id": p, "issue_family_id": families[p],
                           "repository": data[p]["repository"], "lines": len(data[p]["before"].splitlines())}
                          for p in pending[:args.limit]], indent=2))
    else:
        if not args.pair_id:
            parser.error("inspect requires --pair-id")
        inspect(data, args.pair_id, args.context, args.helpers.split(",") if args.helpers else ())


if __name__ == "__main__":
    main()
