"""Package a verified preparation workspace without changing its source files."""

import argparse
import hashlib
import json
from pathlib import Path
import shutil

from package_training_audit import audit_files


PREFIX = "HAPY_CVEFIXES_ADMITTED"
PACKAGE_FILES = (
    ".gitignore", "README.md", "LICENSE.md", "attribution/README.md",
    "documentation/DATASET_GUIDE.md", "documentation/REPRODUCING.md",
    "scripts/package_dataset.py", "scripts/stage_workspace.py", "scripts/verify_package.py",
    "scripts/package_training_audit.py", "documentation/training-audit/README.md",
    "scripts/test_package_training_audit.py",
    "documentation/research/README.md", "evidence/verification/SECURITY_ADMISSION_RELEASE_MANIFEST.json",
    "data/dataset.json",
)
EXTRA_FILES = (
    "SECURITY_ADMISSION_RELEASE_MANIFEST.json",
    "CVEFIXES_SECURITY_EXPANSION_FILTERED_CANDIDATES.jsonl",
    "CVEFIXES_SECURITY_EXPANSION_REVIEW_RESULTS.json",
    "HAPY_BUG_CANDIDATE_PAIRS.jsonl",
    "HAPY_BUG_CASE_METADATA.json",
    "HAPY_BUG_MAJORITY_PROGRAMMING_LINES.json",
    "HAPY_BUG_MAJORITY_AUDIT.json",
    "HAPY_BUG_SOURCE_BUILD_AUDIT.json",
    "HAPY_BUG_SOURCE_RECONSTRUCTION_LOG.jsonl",
    "HAPY_BUG_INDEPENDENT_EXPORT_VERIFICATION.json",
    "HAPY_BUG_OFFICIAL_RELEASE_METADATA.json",
    "HAPY_BUG_PUBLISHED_PROCESSING_EXCERPTS.txt",
    "HAPY_BUG_RELEASE_INVENTORY.json",
    "HAPY_BUG_RELEASE_MANIFEST.json",
    "CVEFIXES_ORIGINAL_ARCHIVE.json",
    "CVEFIXES_ORIGINAL_ZIP_INDEX.json",
    "CVEFIXES_EXTRACTION_PROGRESS.json",
    "CVEFIXES_PYTHON_VALIDATION.json",
    "CVEFIXES_UPSTREAM_DATA_DICTIONARY.md",
    "CVEFIXES_UPSTREAM_README.md",
    "PYTHON_CORPUS_BUILD.py",
    "HAPY_BUG_AUDIT.py",
    "VERIFY_CORPUS_ARTIFACTS.py",
)


def fingerprint(path):
    raw = path.read_bytes()
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def destination(name):
    if name.endswith(".py"):
        folder = "scripts"
    elif name.startswith(("CATEGORY_AUDIT", "EXPERIMENT_")):
        folder = "documentation/training-audit" if name.endswith(".md") else "evidence/training-audit"
    elif name == "README.md" or name in (
        "DATASET_DECISION.md", "SECURITY_ADMISSION_FINDINGS.md", "SECURITY_EXPANSION_FINDINGS.md"
    ):
        folder = "documentation/research"
    elif name.endswith(".zip"):
        folder = "evidence/sources"
    elif name.startswith(PREFIX) and any(
        f"_{split}_" in name for split in ("TRAIN", "VALIDATION", "TEST")
    ):
        folder = "splits"
    elif name in (
        f"{PREFIX}_CANDIDATE_PAIRS.jsonl", "HAPY_BUG_CANDIDATE_PAIRS.jsonl",
        "CVEFIXES_SECURITY_ADMITTED_PAIRS.jsonl"
    ):
        folder = "data"
    elif name.startswith("CVEFIXES_UPSTREAM_") or name in (
        "HAPY_BUG_OFFICIAL_RELEASE_METADATA.json", "CVEFIXES_ORIGINAL_ARCHIVE.json",
        "CVEFIXES_ORIGINAL_ZIP_INDEX.json"
    ):
        folder = "attribution"
    elif name.startswith("HAPY_BUG_") or name in (
        "CVEFIXES_EXTRACTION_PROGRESS.json", "CVEFIXES_PYTHON_VALIDATION.json"
    ):
        folder = "evidence/base"
    elif name.startswith("SECURITY_ADMISSION_") and name not in (
        "SECURITY_ADMISSION_AUDIT.json", "SECURITY_ADMISSION_INDEPENDENT_VERIFICATION.json",
        "SECURITY_ADMISSION_RELEASE_MANIFEST.json", "SECURITY_ADMISSION_SOURCE_AUDIT.json",
        "SECURITY_ADMISSION_EVIDENCE_AUDIT.json"
    ):
        folder = "evidence/review"
    elif name.startswith("CVEFIXES_SECURITY_EXPANSION_"):
        folder = "evidence/review"
    else:
        folder = "evidence/verification"
    return f"{folder}/{name}"


def package(source, root):
    release = json.loads((source / "SECURITY_ADMISSION_RELEASE_MANIFEST.json").read_text())
    for name, expected in release["files"].items():
        if Path(name).name != name or fingerprint(source / name) != expected:
            raise ValueError(f"Source release fingerprint mismatch: {name}")
    audit_names, audit_status = audit_files(source)
    mapping = {name: destination(name) for name in sorted(set(release["files"]) | set(EXTRA_FILES) | audit_names)}
    if audit_status is not None:
        # The audit lock includes a later workspace README relocation. Preserve the
        # published base README/release manifest and stage the audit-era copies.
        for name in ('README.md', 'SECURITY_ADMISSION_RELEASE_MANIFEST.json'):
            mapping[name] = 'evidence/training-audit/protected-inputs/'+name
    previous_path = root / "PACKAGE_MANIFEST.json"
    previous_manifest = json.loads(previous_path.read_text()) if previous_path.exists() else {}
    previous = previous_manifest.get("files", {})
    if previous_manifest.get("training_audit") and audit_status is None:
        raise ValueError("Refreshing this package requires its training-audit source workspace")
    for relative in list(mapping.values()) + ["data/dataset.json"]:
        target = root / relative
        if target.exists() and (relative not in previous or fingerprint(target) != previous[relative]):
            raise ValueError(f"Refusing to overwrite an untracked or modified package file: {relative}")
    for name, relative in mapping.items():
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source / name, target)
    records = [json.loads(line) for line in (root / "data" / f"{PREFIX}_CANDIDATE_PAIRS.jsonl").read_text().splitlines()]
    (root / "data/dataset.json").write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    audit = json.loads((source / "SECURITY_ADMISSION_AUDIT.json").read_text())
    # Explicit files only: unrelated local files must never enter the package.
    paths = sorted(root / relative for relative in set(mapping.values()) | set(PACKAGE_FILES))
    manifest = {
        "status": "Packaged preparation checkpoint; not independent issue-label adjudication",
        "snapshot_date": "2026-10-18",
        "combined_pairs": audit["combined_pairs"],
        "security_pairs": audit["combined_issue_groups"]["security_candidate"],
        "general_bug_origin_pairs": audit["combined_issue_groups"]["correctness_candidate"],
        "security_cves": audit["combined_security_cves"],
        "unresolved_candidates_excluded": audit["decision_counts"]["quarantine"],
        "source_files": mapping,
        "files": {path.relative_to(root).as_posix(): fingerprint(path) for path in paths},
    }
    if audit_status is not None:
        manifest["training_audit"] = audit_status
    (root / "PACKAGE_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({key: value for key, value in manifest.items() if key not in ("source_files", "files")}, indent=2))
    print(f"Packaged {len(paths)} files; {sum(item['bytes'] for item in manifest['files'].values()):,} bytes")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, required=True)
    args = parser.parse_args()
    package(args.source_dir.resolve(), Path(__file__).resolve().parents[1])
