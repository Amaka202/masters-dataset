# Dataset guide

## The main file

`data/dataset.json` contains an ordinary JSON array of 1,052 objects. Its JSONL
counterpart contains the same objects in the same order, one per line. Python
code is stored as string values, including newlines; it is not executable data
to import as modules.

The two additional source-subset files in `data/` contain 717 HaPy-Bug pairs
and 335 CVEfixes additions. They are provenance subsets of the combined file,
not extra examples to append to it.

## Important fields

| Field | Meaning |
|---|---|
| `pair_id` | Source-linked record identifier |
| `source` | `HaPy-Bug` or `CVEfixes` |
| `repository`, `fixing_commit`, `path` | Original source provenance |
| `before`, `after` | Complete function source on each side of the change |
| `qualified_function` | Function identity, including enclosing scopes |
| `before_sha256`, `after_sha256` | Exact function-text fingerprints |
| `before_ast_sha256`, `after_ast_sha256` | Python AST fingerprints |
| `issue_group` | `security_candidate` or `correctness_candidate` |
| `cves` | Supported security CVE attribution, where present |
| `cwes` | Source CVE-level metadata, not independently assigned function labels |
| `label_status`, `reference_validity` | Annotation/review provenance |
| `reference_lines` | Attached HaPy-Bug human line-purpose evidence, where present |

Additional fields retain source snapshots, companion/context evidence,
duplicate provenance and broader commit-linked CVEs where needed. Field
availability varies by source. The original full records are preserved rather
than flattened into one simplified label schema.

## Splits and model inputs

In `splits/`, `*_CANDIDATES.jsonl` files are the grouped before/after records
with a `split` field. The before-only files contain exactly `input_id`,
`language` and `code`. Their paired reference index contains `input_id`,
`pair_id`, `issue_group`, `cves` and `label_status`.

Use before-only inputs for detection. Keep the after-code, source-linked IDs,
advisories and reference labels outside detection prompts. Before-code retains
original comments/docstrings; the export is not guaranteed free of all possible
in-source hints.

## Interpretation

- 488 security-linked pairs cover 273 distinct CVEs. Multiple functions and
  nested/enclosing functions may represent the same vulnerability.
- HaPy-Bug references are published human line-purpose annotations. CVEfixes
  relevance judgments are assistant source/advisory reviews, not independent
  human adjudication or reproduced exploit tests.
- The 564 general-bug-origin pairs are not certified security negatives.
- After-code is a scoped fixing counterpart, not universally clean code.
- The 507 unresolved candidates are outside the admitted data and splits;
  quarantine is not a negative label.
- Splits are provisional. No model-development method, final taxonomy or final
  evaluation protocol is selected by these files.

The preserved detailed findings in `research/` describe selection biases,
configuration-dependent limits and individual decisions.
