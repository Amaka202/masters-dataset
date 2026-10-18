# Dataset decision for EPP planning

**Decision date:** 17 October 2026; admission update 18 October 2026  
**Selected base dataset:** HaPy-Bug, official version 1, using the locally reconstructed and filtered function-pair subset.  
**Selected security-expansion source:** Original CVEfixes v1.0.8, admitting issue-relevant reviewed records.  
**Status:** Following the user's request to increase security coverage, the source plan is HaPy-Bug plus a vetted CVEfixes extension. Final expanded counts and evaluation splits are not yet frozen.

## Decision

Use **HaPy-Bug as the mixed-issue base and expand its security portion with original CVEfixes**. HaPy-Bug's official release is https://doi.org/10.6084/m9.figshare.24448663.v1 ; CVEfixes v1.0.8 is https://zenodo.org/records/13118970 . Both publish CC BY 4.0 dataset terms. Applicable upstream source-code terms remain relevant.

The [updated verified admission snapshot](SECURITY_ADMISSION_FINDINGS.md) adds **335 security function pairs covering 208 new CVEs**. The combined snapshot contains **1,052 pairs: 488 security-linked and 564 general-bug-origin pairs, covering 273 security CVEs**. All admitted additions match complete referenced before/after functions. Alternate source locations are explicitly recorded and additionally checked against commit, first-parent and full-module identity. Required additional configuration/unchanged modules are bound to reviewed byte hashes at the exact fixing commit and checked offline. Their issue labels are assistant source/advisory inspections, distinct from HaPy-Bug's published human line-purpose annotations; they are not independently adjudicated gold labels.

The broader [security expansion audit](SECURITY_EXPANSION_FINDINGS.md) identified **1,186 candidate pairs linked to 507 additional CVEs**. All now have explicit triage decisions: **335 admitted, 344 rejected, 507 quarantined**. Issue-level triage covers 1,146 source-context-passing pairs; 40 source failures are separately recorded. Quarantines comprise 467 unresolved issue-context/attribution cases and 40 source-context failures. All five previous upstream retrieval blockers were resolved. Full-pool triage is complete, but contextual resolution and independent label adjudication remain unfinished. The possible 572-CVE pool is not a validated dataset count.

The prepared HaPy-Bug base contains **717 function pairs from 458 source cases across 63 repositories**: 153 security-linked pairs and 564 general-bug-benchmark-origin pairs. Retained functions intersect changed lines identified as programming/bug-fix by at least two confident manual reviewers. Source reconstruction and export checks have passed.

The following are **verified provisional combined splits**, not the frozen evaluation protocol:

| Split | Security-linked pairs | General-bug-origin pairs | Total pairs | Security CVEs |
|---|---:|---:|---:|---:|
| Training | 342 | 400 | 742 | 150 |
| Validation | 73 | 83 | 156 | 61 |
| Test | 73 | 81 | 154 | 62 |

## Basis

- It meets the intended Python security-plus-correctness scope within one existing mixed dataset.
- Published human line-purpose annotations provide a stronger basis for selecting relevant changes than assigning a commit's issue label to every changed function.
- The release has explicit reuse terms, and the actual subset, source context, grouped splits and duplicate checks have been prepared.

**CVEfixes supplies the selected security-expansion pool. PyResBugs remains supporting research and is not part of this source plan.** The combined snapshot has grouped splits and an independent offline integrity check. Defined cross-split provenance/exact/AST/lexical-near-duplicate violations are zero. Additional admissions require rebuilding these artefacts; the cross-validation suggestion remains provisional.

## Interpretation and planning boundary

The provisional combined test split includes 73 security pairs from **62 distinct CVEs**, compared with 28 CVEs in the first combined snapshot and 15 in the earlier HaPy-only test. The full combined count of 273 is not a held-out test count or a claim of adequate statistical power. Rebuilding grouped splits can change membership and per-split counts. Multiple functions can represent one vulnerability. The after-version is a counterpart intended to fix the referenced change, not certified free of every issue. General-bug provenance is not proof that a function has no security issue.

Model-development method, final input context, target issue definitions and evaluation protocol remain experimental-design decisions. Dataset selection itself is settled for planning; these outstanding decisions do not justify reopening the dataset shortlist by default.

## Evidence and files

- Detailed build evidence: `PYTHON_DATASET_BUILD_VERDICT.md`.
- Current combined data: `HAPY_CVEFIXES_ADMITTED_CANDIDATE_PAIRS.jsonl` and `HAPY_CVEFIXES_ADMITTED_{TRAIN,VALIDATION,TEST}_CANDIDATES.jsonl`.
- Admission findings and limitations: `SECURITY_ADMISSION_FINDINGS.md`.
- Admission decisions and verification: `SECURITY_ADMISSION_FINAL_DECISIONS.jsonl`, `SECURITY_ADMISSION_INDEPENDENT_VERIFICATION.json`, `HAPY_CVEFIXES_ADMITTED_SPLIT_AUDIT.json`.
- HaPy base: `HAPY_BUG_CANDIDATE_PAIRS.jsonl` and its independent verification report.
- Release metadata and fingerprints: `HAPY_BUG_OFFICIAL_RELEASE_METADATA.json` and `HAPY_BUG_RELEASE_MANIFEST.json`.

This document records a technical planning decision. It is not EPP submission prose; the course brief restricts generative-AI use for that assessment to proofreading.
