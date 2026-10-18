# Master's research dataset: HaPy-Bug + CVEfixes

Prepared Python function pairs for research into LLM-based security and
correctness analysis. Maintained by Chiamaka Umeh.

**Snapshot: 18 October 2026.** This is a research preparation checkpoint;
the experimental protocol and issue labels have not been independently frozen
or adjudicated.

## Start with the dataset

**[`data/dataset.json`](data/dataset.json) is the complete dataset as one JSON
array containing 1,052 objects.** Each object contains a function's before/after
code, its source and associated reference metadata.

[`data/HAPY_CVEFIXES_ADMITTED_CANDIDATE_PAIRS.jsonl`](data/HAPY_CVEFIXES_ADMITTED_CANDIDATE_PAIRS.jsonl)
contains exactly the same records, one JSON object per line, for streaming and
model pipelines. The JSON-array export preserves every field and the record order.

```python
import json
from pathlib import Path

pairs = json.loads(Path("data/dataset.json").read_text(encoding="utf-8"))
print(len(pairs))  # 1052
print(pairs[0]["before"])
```

| Material | Function pairs | Distinct security CVEs |
|---|---:|---:|
| HaPy-Bug base | 717: 153 security-linked, 564 general-bug-origin | 65 |
| Reviewed CVEfixes additions | 335 security-linked | 208 |
| **Combined** | **1,052: 488 security-linked, 564 general-bug-origin** | **273** |

Several functions can belong to one CVE. The 488 security-linked pairs do not
represent 488 independent vulnerabilities. General-bug-origin records are not
verified security negatives, and after-code is not certified universally clean.

## What's in each folder?

| Folder | Contents |
|---|---|
| `data/` | Complete JSON/JSONL dataset and its two source subsets |
| `splits/` | Grouped train/validation/test pairs, before-only inputs and separate references |
| `scripts/` | Preparation, inspection, packaging and offline verification tools |
| `documentation/` | Dataset guide, reproduction instructions and detailed research findings |
| `attribution/` | Original source information, release metadata and licence notices |
| `evidence/` | Review history, audits, source snapshots and excluded/unresolved candidate records |

The **507 unresolved CVEfixes candidates are excluded from `data/dataset.json`
and all experiment splits**. They remain in `evidence/review/` for continued
research. That folder is evidence, not additional admitted training data.

## Provisional grouped splits

| Split | Security pairs | General-bug-origin pairs | Total | Security CVEs |
|---|---:|---:|---:|---:|
| Train | 342 | 400 | 742 | 150 |
| Validation | 73 | 83 | 156 | 61 |
| Test | 73 | 81 | 154 | 62 |

Grouping keeps repository, fix, CVE and defined duplicate provenance together.
For detection prompts, use the `*_BEFORE_ONLY_INPUTS.jsonl` files. They contain
only opaque IDs, language and before-code. Keep `*_REFERENCE_INDEX.jsonl` and
before/after pair files outside detection prompts. Original source comments and
docstrings remain in the before-code.

## Verify the package

Using Python 3.14 (the preparation environment; no third-party Python packages
are required for this command):

```sh
python3 scripts/verify_package.py
```

This checks package fingerprints, JSON/JSONL equivalence and runs the preserved
offline source/provenance/split verifier in a temporary workspace. It uses the
included source ZIPs and makes no network requests. Dataset code is treated as
data and is never imported or executed.

The source verification covered **2,104 function versions, 1,617 source/context
URL snapshots and 1,875 human line references**. These are integrity and
provenance checks, not independent validation of the vulnerability judgments.

## Sources and label provenance

- **HaPy-Bug, official v1:** <https://doi.org/10.6084/m9.figshare.24448663.v1>.
  Published human line-purpose annotations support the prepared base.
- **CVEfixes, v1.0.8:** <https://zenodo.org/records/13118970>.
  Added pairs were inspected by the assistant against source and advisories;
  those judgments are not independently adjudicated human gold labels.

Both dataset releases use **CC BY 4.0**. Individual upstream source-code terms
also apply. See [attribution](attribution/README.md) and [licensing](LICENSE.md).

The large local Python-only SQLite extraction is retained in the original
research workspace rather than this Git repository. It is not needed to load
the dataset or run the packaged offline verification. The small, selected
source-evidence archives are included for reproducibility.

Further details: [dataset guide](documentation/DATASET_GUIDE.md),
[reproduction](documentation/REPRODUCING.md), and
[review findings](documentation/research/SECURITY_ADMISSION_FINDINGS.md).
