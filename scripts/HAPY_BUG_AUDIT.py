"""Audit the official CC BY 4.0 HaPy-Bug release without executing source code."""

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import tarfile
import re

from BUILD_CANDIDATE_SPLITS import save
from PROBE_CANDIDATE_SOURCES import fetch


def inventory(cache, output):
    path = cache / "HaPy-Bug.tar.gz"
    with path.open("rb") as stream:
        md5 = hashlib.file_digest(stream, "md5").hexdigest()
    if md5 != "a97ea8d7027fcbbbfdd891de2faaa48b":
        raise ValueError("Official archive MD5 mismatch")
    with tarfile.open(path, "r:gz") as archive:
        members = archive.getmembers()
        metadata = [{"name": m.name, "bytes": m.size} for m in members
                    if m.isfile() and ("/annotated_data/" in m.name or "/collective/" in m.name)]
        report = {"url": "https://ndownloader.figshare.com/files/52129358",
                  "doi": "10.6084/m9.figshare.24448663.v1", "dataset_licence": "CC-BY-4.0",
                  "verified_md5": md5, "bytes": path.stat().st_size,
                  "archive_members": len(members), "annotation_members": metadata,
                  "top_directories": Counter("/".join(m.name.split("/")[:3]) for m in members)}
        save(output / "HAPY_BUG_RELEASE_INVENTORY.json", report)
        sample = {}
        for m in members:
            if m.isfile() and m.name.endswith(".json") and "/annotated_data/" in m.name:
                data = json.load(archive.extractfile(m))
                sample[m.name] = {"type": type(data).__name__, "records": len(data),
                                  "first_record": data[0] if isinstance(data, list) and data else data}
                if len(sample) == 2:
                    break
        save(output / "HAPY_BUG_ANNOTATION_SCHEMA_PROBE.json", sample)
    print(json.dumps({k: v for k, v in report.items() if k != "top_directories"}, indent=2))


def inspect(cache, output):
    with tarfile.open(cache / "HaPy-Bug.tar.gz", "r:gz") as archive:
        data = json.load(archive.extractfile("HaPy-Bug/collective/collective.json"))
        first = data[0] if isinstance(data, list) else {key: next(iter(value.values())) if isinstance(value, dict) else value
                                                      for key, value in data.items()}
        manual = [i for i in data["id"] if not data["auto"][i]]
        summary = {"line_annotation_rows": len(data["id"]), "manual_line_annotation_rows": len(manual),
                   "manual_cases": len({data["id"][i] for i in manual}),
                   "manual_case_sources": Counter(data["ds"][i] for i in manual),
                   "manual_users": Counter(data["user"][i] for i in manual),
                   "manual_labels": Counter(data["annotation"][i] for i in manual)}
        save(output / "HAPY_BUG_COLLECTIVE_SCHEMA_PROBE.json", {
            "type": type(data).__name__, "records": len(data["id"]) if isinstance(data, dict) else len(data), "first_record": first,
            "raw_metadata_members": [{"path": m.name, "bytes": m.size} for m in archive.getmembers()
                                     if m.isfile() and "/raw_data/" in m.name and m.name.endswith(".json")][:100],
            "summary": summary,
            "example_case_files": [m.name for m in archive.getmembers() if m.isfile() and "/matplotlib-3/" in m.name],
            "example_diff": json.load(archive.extractfile("HaPy-Bug/raw_data/bugsinpy-dataset/matplotlib-3/generated/2a3707d9c3472b1a010492322b6946388d4989ae.diff.json")),
        })
    print(json.dumps(summary, indent=2))


def catalogue(cache, output):
    metadata, patch_hashes, collective = {}, defaultdict(list), None
    votes, patch_by_diff = defaultdict(dict), {}
    conflicts = 0
    with tarfile.open(cache / "HaPy-Bug.tar.gz", "r|gz") as archive:
        for member in archive:
            if not member.isfile():
                continue
            if member.name == "HaPy-Bug/collective/collective.json":
                collective = json.load(archive.extractfile(member))
            if "/raw_data/" in member.name and "/patches/" in member.name and member.name.endswith(".diff"):
                case = member.name.split("/")[3]
                commit = Path(member.name).stem
                if re.fullmatch(r"[0-9a-f]{7,40}", commit):
                    patch_hashes[case].append(commit)
                    diff = archive.extractfile(member).read().decode()
                    patch_by_diff[(case, hashlib.sha256(diff.strip().encode()).hexdigest())] = commit
            if "/annotated_data/" not in member.name or not member.name.endswith(".json") or "/model annotations" in member.name:
                continue
            for row in json.load(archive.extractfile(member)):
                data = row["data"]
                source = data["datasetName"]
                case = data["projectName"] if source == "bugs-in-py" else data.get("cve", {}).get("id")
                identity = source + "_" + case
                if identity not in metadata:
                    metadata[identity] = {"case_id": identity, "dataset_source": source, "original_case": case,
                                          "data": data, "annotator_confidence": []}
                for annotation in row.get("annotations", []):
                    if annotation.get("was_cancelled"):
                        continue
                    choices = {a.get("from_name"): a["value"].get("choices") for a in annotation["result"] if a["type"] == "choices"}
                    metadata[identity]["annotator_confidence"].append({"bundle": Path(member.name).stem, "choices": choices})
                    bundle = Path(member.name).stem
                    if bundle.startswith("A_"):
                        user = {"1": "E1", "4": "E1", "7": "E1", "2": "E2", "5": "E2", "3": "E3", "6": "E3"}[bundle.split("_")[1]]
                    else:
                        user = {"B": "U1", "C": "U2", "D": "U3"}[bundle[0]]
                    confident = choices.get("reviewer-is-sure") == ["yes"] and choices.get("annotations-were-problematic") == ["no"]
                    for result in annotation["result"]:
                        if result["type"] != "cve":
                            continue
                        for commit_index, files in enumerate(result["value"]["diffsFiles"]):
                            for file in files:
                                for side, lines in file["lines"].items():
                                    for line in lines:
                                        key = (identity, commit_index, file["fileName"], side, line["lineNumber"])
                                        vote = (line["category"], file["category"], confident)
                                        if user in votes[key] and votes[key][user] != vote:
                                            conflicts += 1
                                            votes[key][user] = ("conflict", "conflict", False)
                                        else:
                                            votes[key][user] = vote
    auto_rows = 0
    for i, identity in collective["id"].items():
        if collective["auto"][i]:
            auto_rows += 1
    references = []
    for (identity, commit_index, filename, side, line), by_user in sorted(votes.items()):
        agreement = sum(annotation in ("bug(fix)", "bug(fix) + refactoring") and category == "programming" and confident
                        for annotation, category, confident in by_user.values())
        if filename.endswith(".py") and agreement >= 2:
            references.append({"case_id": identity, "commit_index": commit_index, "path": filename, "side": side, "line": line,
                               "bugfix_programming_votes": agreement, "manual_votes": by_user})
    for row in metadata.values():
        row["recorded_patch_hashes"] = patch_hashes[row["original_case"]]
        row["commits"] = [{"index": i, "fixing_commit": patch_by_diff.get((row["original_case"], hashlib.sha256(c["diff"].strip().encode()).hexdigest())),
                           "diff": c["diff"], "message": c["message"]} for i, c in enumerate(row["data"]["gitCommits"])]
    save(output / "HAPY_BUG_CASE_METADATA.json", list(metadata.values()))
    save(output / "HAPY_BUG_MAJORITY_PROGRAMMING_LINES.json", references)
    cases = {r["case_id"] for r in references}
    summary = {"metadata_cases": len(metadata), "metadata_sources": Counter(r["dataset_source"] for r in metadata.values()),
               "manual_line_vote_keys": len(votes), "excluded_auto_line_rows": auto_rows,
               "same_user_conflicts": conflicts, "majority_python_programming_bugfix_lines": len(references),
               "cases_with_majority_python_programming_bugfix": len(cases),
               "majority_case_sources": Counter(identity.split("_", 1)[0] for identity in cases),
               "reference_rule": "At least two distinct manual reviewers, confident and unproblematic, mark a .py line programming and bug(fix) or bug(fix)+refactoring; commit index preserved from raw exports",
               "notes": ["Automated initial annotations are excluded", "Line-purpose annotation is not a proof of program-wide cleanliness",
                         "HaPy-Bug publishes its derived dataset CC BY 4.0; this does not resolve BugsInPy framework licence"]}
    save(output / "HAPY_BUG_MAJORITY_AUDIT.json", summary)
    examples = {}
    for row in metadata.values():
        source = row["dataset_source"]
        if source not in examples:
            examples[source] = {k: v for k, v in row.items() if k != "data"}
            examples[source]["data"] = {k: v for k, v in row["data"].items() if k not in ("gitCommits", "initialAnnotation")}
            examples[source]["hyperlinks"] = row["data"]["initialAnnotation"].get("hyperlinks")
    save(output / "HAPY_BUG_CASE_METADATA_EXAMPLES.json", examples)
    print(json.dumps(summary, indent=2))


def protocol(cache, output):
    with tarfile.open(cache / "HaPy-Bug.tar.gz", "r:gz") as archive:
        notebook = json.load(archive.extractfile("HaPy-Bug/Paper.ipynb"))
        cells = ["".join(cell.get("source", [])) for cell in notebook["cells"]]
        relevant = [c for c in cells if any(word in c for word in ("auto", "U1", "E1", "collective", "annotated_data"))]
        (output / "HAPY_BUG_PUBLISHED_PROCESSING_EXCERPTS.txt").write_text("\n\n--- CELL ---\n\n".join(relevant))
    print(json.dumps({"relevant_notebook_cells": len(relevant)}))


def release(cache, output):
    metadata = json.loads(fetch("https://api.figshare.com/v2/articles/24448663/versions/1", cache))
    if metadata["license"]["name"] != "CC BY 4.0":
        raise ValueError("Unexpected official release licence")
    save(output / "HAPY_BUG_OFFICIAL_RELEASE_METADATA.json", metadata)
    print(json.dumps({"doi": metadata["doi"], "licence": metadata["license"], "citation": metadata["citation"]}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("inventory", "inspect", "catalogue", "protocol", "release"))
    parser.add_argument("--cache-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    {"inventory": inventory, "inspect": inspect, "catalogue": catalogue, "protocol": protocol, "release": release}[args.stage](args.cache_dir, args.output_dir)
