# Training audit and experiment-selection decisions

**Documentation update: 1 November 2026.** The original 18 October data/split release
is preserved. These records document the later review and agreed selection principles;
they are not an approved replacement experimental dataset.

## Start here

- [Decisions and supervisor discussion note](EXPERIMENT_SELECTION_DECISIONS.md)
- [Detailed input/scoring protocol proposal](EXPERIMENT_PROTOCOL_DRAFT.md)
- [Completed consolidation report](CATEGORY_AUDIT_CONSOLIDATION_REPORT.md)
- [Detailed review history and remaining case decisions](CATEGORY_AUDIT_CONSOLIDATION_REVIEW.md)
- [Original discovery protocol](CATEGORY_AUDIT_PROTOCOL.md)

All **742 training pairs** have current assistant consolidation proposals, with no
remaining or stale reviews. The student approved conservative selection principles:
equal function-only information, genuine existing bugs, credible security labels,
defensible fixed counterparts, underlying-issue grouping, and broad reporting
categories retaining detailed traceability. Individual labels/eligibility, issue
identities, category boundaries and the numerical protocol remain unfinished.

The 113 detailed mechanisms and 25 reporting parents are still a proposed hierarchy.
The six conditional-retain proposals are priority reviews, not a six-example final
dataset. No held-out substantive category review or model experiment has been run
as part of this audit. Existing split files are the original candidate pool, not
the final eligible experimental subset.

## Included evidence

`evidence/training-audit/` contains the discovery ledger and definitions, all registered
consolidation proposal batches, retained supplementary sources, generated case reviews,
counts, dependence inventories and manifests. Original source material remains inert
data; published upstream code terms still apply. References and evidence must stay
outside model-facing inputs. The manifest's original flat filenames are resolved by
`PACKAGE_MANIFEST.json` and `scripts/stage_workspace.py`.

Historical manifests, notes and source snapshot text preserve their recorded dates,
URLs, missing-source qualifications and original provenance. Some historic unregistered
drafts or unrelated exploratory workspace files are not packaged. The registered
corrected054 proposal is active; historical source digests and notes preserve its
correction history. The explicit package allowlist is derived from the verified
consolidation manifest, plus the discovery checkpoint/protocol, immutable tail
schedule and preflight files.

The audit-era workspace had relocated its README after the original publication.
Its corresponding README/release-manifest pair is preserved separately under
`evidence/training-audit/protected-inputs/` and used when staging the audit's exact
45-input lock. The original published research README and admission release manifest
remain unchanged in their original repository locations. No dataset records or split
bytes differ between those documentation checkpoints.

## Reproduce offline

From the repository root:

```sh
python3 scripts/verify_package.py --audit
```

This checks package/source fingerprints and original admission integrity, stages the
mapped original bytes in a temporary flat workspace, then runs the audit tools'
discovery, consolidation and preflight reproducibility checks. It executes only the
project's verification/bookkeeping programs, not retained dataset/dependency code,
payloads or upstream tests. It requires no network or third-party Python packages.
The original audit-tool regression suite passed 202 tests before publication.

To inspect or run the own-tool suite separately in a persistent workspace:

```sh
python3 scripts/stage_workspace.py --output-dir workspace
python3 workspace/CATEGORY_AUDIT.py check
python3 workspace/CATEGORY_AUDIT_CONSOLIDATE.py check
python3 workspace/EXPERIMENT_PREFLIGHT.py check
python3 -m unittest discover -s workspace -p CATEGORY_AUDIT_CONSOLIDATE_TEST.py
```

Discovery progress is a preserved historical ledger checkpoint. Its pending label
counts are distinct from the subsequently approved selection principles. Neither
an empty review queue nor passing hashes certifies case-level eligibility.

## Preflight result and next step

The proposed whole-function cap is 16,384 UTF-8 bytes, with no truncation. All 742
training before/after pairs fit it; the largest before-function is 10,442 bytes.
This is size bookkeeping only, not a token-capacity guarantee or proof that a model
has enough information to identify each bug. The proposed limit must be confirmed
against actual prompt/tokenizer constraints before protocol freeze.

Next, resolve conditional cases and apply the same explicit admission gates to
the training pool. Establish viable security/correctness and independent-group counts
before deciding that planned model training/evaluation is feasible. Final subset
manifests and held-out reference adjudication follow the agreed freeze process.
