"""Check packaged exports and run preserved offline verification on copied evidence."""

from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from stage_workspace import check_manifest, stage


PREFIX = "HAPY_CVEFIXES_ADMITTED"


def verify(root):
    manifest = check_manifest(root)
    records = json.loads((root / "data/dataset.json").read_text(encoding="utf-8"))
    jsonl = [json.loads(line) for line in (root / "data" / f"{PREFIX}_CANDIDATE_PAIRS.jsonl").read_text().splitlines()]
    assert isinstance(records, list) and records == jsonl, "JSON/JSONL exports differ"
    assert len(records) == manifest["combined_pairs"]
    assert len({row["pair_id"] for row in records}) == len(records)
    counts = Counter(row["issue_group"] for row in records)
    assert counts["security_candidate"] == manifest["security_pairs"]
    assert counts["correctness_candidate"] == manifest["general_bug_origin_pairs"]
    assert len({cve for row in records for cve in row["cves"]}) == manifest["security_cves"]
    queue_path = root / manifest["source_files"]["SECURITY_ADMISSION_REMAINING_QUEUE.jsonl"]
    assert hashlib.sha256(queue_path.read_bytes()).hexdigest() == "7c1b985fa5228f7e89f08c95ab1c96f73f42f37f398c11030c4684cdd6010f19"
    unresolved_path = root / manifest["source_files"]["SECURITY_ADMISSION_UNRESOLVED_REVIEW.jsonl"]
    unresolved = [json.loads(line) for line in unresolved_path.read_text().splitlines()]
    assert len(unresolved) == manifest["unresolved_candidates_excluded"]
    assert not {row["pair_id"] for row in unresolved} & {row["pair_id"] for row in records}
    # Copies isolate regenerated outputs from the version-controlled checkpoint.
    with tempfile.TemporaryDirectory(prefix="masters-dataset-verification-") as temporary:
        workspace = Path(temporary)
        stage(root, workspace)
        subprocess.run([sys.executable, str(root / "scripts/VERIFY_SECURITY_ADMISSION.py"),
                        "--output-dir", str(workspace)], check=True)
        report_name = "SECURITY_ADMISSION_INDEPENDENT_VERIFICATION.json"
        expected_report = json.loads((root / manifest["source_files"][report_name]).read_text())
        assert json.loads((workspace / report_name).read_text()) == expected_report
        for split in ("TRAIN", "VALIDATION", "TEST"):
            for suffix in ("BEFORE_ONLY_INPUTS", "REFERENCE_INDEX"):
                name = f"{PREFIX}_{split}_{suffix}.jsonl"
                expected = root / manifest["source_files"][name]
                assert (workspace / name).read_bytes() == expected.read_bytes(), name
    print(f"Package verified: {len(records)} records, {manifest['security_cves']} security CVEs; "
          f"{len(manifest['files'])} file fingerprints match. JSON and JSONL are identical records.")


if __name__ == "__main__":
    verify(Path(__file__).resolve().parents[1])
