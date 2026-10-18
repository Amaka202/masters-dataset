# MSc project workspace

## Start here

- [Agreed project idea](REVISED_INITIAL_PROJECT_IDEA.md)
- [Assessment guidance](UNIT_4_EPP_GUIDANCE_NOTES.md)
- [Dataset decision](DATASET_DECISION.md)
- [Current dataset findings and unresolved work](SECURITY_ADMISSION_FINDINGS.md)

## Current dataset

The selected sources are **HaPy-Bug v1 + reviewed original CVEfixes v1.0.8**.
The current snapshot has **1,052 function pairs: 488 security-linked and 564
general-bug-origin pairs**, covering **273 security CVEs**. It is preparation
material, not a frozen experimental dataset or independently adjudicated gold.

| Use | Files |
|---|---|
| Combined before/after pairs | `HAPY_CVEFIXES_ADMITTED_CANDIDATE_PAIRS.jsonl` |
| Provisional grouped splits | `HAPY_CVEFIXES_ADMITTED_{TRAIN,VALIDATION,TEST}_CANDIDATES.jsonl` |
| Detection inputs | `HAPY_CVEFIXES_ADMITTED_{TRAIN,VALIDATION,TEST}_BEFORE_ONLY_INPUTS.jsonl` |
| Separate references | `HAPY_CVEFIXES_ADMITTED_{TRAIN,VALIDATION,TEST}_REFERENCE_INDEX.jsonl` |
| Remaining review work | `SECURITY_ADMISSION_UNRESOLVED_REVIEW.jsonl` |
| Verification and fingerprints | `SECURITY_ADMISSION_INDEPENDENT_VERIFICATION.json`, `SECURITY_ADMISSION_RELEASE_MANIFEST.json` |

Keep reference labels and fixing code outside detection prompts. Preserve the
`HAPY_BUG_*` source/annotation evidence, admission ledgers, immutable review
queue, filtered candidate pool, CVE evidence, source snapshots and
`CVEFIXES_PYTHON.sqlite`: these support continued review and verification.

### Continue and verify

With `OUT` set to this directory and `CACHE` to the existing download cache:

```sh
python INSPECT_SECURITY_CANDIDATES.py --output-dir "$OUT" --indices 612 --context --advisory
python ADMIT_SECURITY_EXPANSION.py progress --output-dir "$OUT" --cache-dir "$CACHE"
# After recording pair-specific decisions:
python ADMIT_SECURITY_EXPANSION.py upstream --output-dir "$OUT" --cache-dir "$CACHE"
python ADMIT_SECURITY_EXPANSION.py export --output-dir "$OUT" --cache-dir "$CACHE"
python BUILD_CANDIDATE_SPLITS.py split --prefix HAPY_CVEFIXES_ADMITTED --output-dir "$OUT"
python VERIFY_SECURITY_ADMISSION.py --output-dir "$OUT"
```

The verifier runs offline using the retained evidence ZIPs. Source files,
configuration and notebooks are treated as inert data. Do not regenerate the
immutable remaining queue. Numbered Markdown review views are optional generated
summaries; use the inspection utility and structured review records instead.

## Cleanup — 18 October 2026

Removed **54 obsolete project files (127,721,153 bytes)**:

- The unselected PyResBugs bulk audit records and superseded `PYTHON_COMBINED_*`
  exports, counts, source-fidelity probes, duplicate links and splits.
- `PYTHON_SOURCE_VERIFIED_SAMPLE.jsonl`, the old unfiltered
  `CVEFIXES_SECURITY_EXPANSION_CANDIDATES.jsonl`, and the unvalidated
  `HAPY_CVEFIXES_EXPANSION_CANDIDATE_PAIRS.jsonl`. The current filtered review
  input remains available.
- Five old SWE-CARE trial outputs: sample, results, static analysis, tool summary
  and review index. Historical findings and source-comparison summaries remain.
- All 37 generated `SECURITY_ADMISSION_REMAINING_BATCH_*.md` and
  `SECURITY_ADMISSION_REVIEW_BATCH_*.md` views. Their structured source data,
  review decisions and immutable queue remain available.

Also removed four obsolete files from the project-specific temporary cache
`msc-combined-dataset-audit` (**13,114,403,684 bytes**):

- `CVEfixes_v1.0.8.zip`: removed after verified extraction; original release URL,
  version, archive digests and member index remain in the project.
- `cvefixes-python.sqlite`: all eight table contents were compared in row order
  and matched the retained project database; physical file hashes differed.
- `cvefixes-python.sqlite.failed-20261017181941` and
  `cvefixes-python.sqlite.failed-initial`: failed extraction attempts.

**Total removed: 58 files, 13,242,124,837 bytes (about 13.2 GB).** The retained
database passed SQLite integrity checking and contains 2,753 Python file changes
and 7,568 method versions. Current dataset verification does not need the removed
archive or obsolete exports. Repeating the original extraction from scratch
requires downloading the original archive again. Historical research scripts and
reports may reference deleted exploratory outputs; those are not inputs to the
current admission/export/verification workflow.
