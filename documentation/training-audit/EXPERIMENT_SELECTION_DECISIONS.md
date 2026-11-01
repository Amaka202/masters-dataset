# Experiment selection decisions — supervisor discussion note

**Decision date:** 1 November 2026  
**Decision maker:** Chiamaka Umeh (student/researcher)  
**Status:** Selection principles approved by the student; application to individual
examples, detailed protocol and final experimental subset remain to be completed.

## Short explanation for my supervisor

> I have completed a source-based review of all 742 training pairs in the combined
> Python dataset. I have chosen a conservative main experiment: compare the models
> on genuine existing bugs that can reasonably be identified from the function
> alone, using credible reference labels. A fixed counterpart will only be used as
> a negative for the specified problem when the evidence supports that use. I will
> avoid counting several functions or versions of the same bug as independent
> successes. The original dataset will remain available, with a separate record of
> which examples qualify and why. The next task is to apply these rules and establish
> whether the resulting subset is large and varied enough for the planned study.

This is a working discussion note, not submitted assessment prose. These decisions
were confirmed by the student in conversation; supervisor endorsement is not implied.

## The six approved choices

| Choice | Plain-English decision | How it will be applied |
|---|---|---|
| 1. Equal, function-only information | Both models get the same function to inspect. A model should not be marked wrong for missing a problem that needs hidden project information. | Use a common before-only selected-function input for the main detection task. Defer examples that critically require unavailable callers, configuration or other project facts. Set one numerical input limit and one explicit ordinary API/runtime-knowledge rule before final admission. |
| 2. Genuine existing bugs | Include failures of something that was already supposed to work, rather than treating every code change as a bug fix. | Require evidence for the pre-existing behaviour/requirement and the selected function's contribution. Keep new features, intentional policy changes, unrelated refactors and unresolved duties outside the main scored subset unless further evidence resolves them. |
| 3. Credible security labels | A crash or a CVE number alone does not make this particular function a proven security example. | Require a credible path from a lower-trust input or actor to an affected permission, confidentiality, integrity or availability boundary. Keep unresolved security cases pending. Review general-bug examples for security implications too; source provenance is not a non-security label. |
| 4. Defensible fixed counterparts | Do not call a supposedly fixed example clean if the relevant problem remains or a new problem makes it unsuitable. | Admit an after-version as a paired negative only for its explicitly checked mechanism and scope. Defer pairs with unresolved residual failures or introduced regressions; do not claim universal bug-free code. |
| 5. Count underlying problems fairly | Several functions or versions of one bug must not inflate the apparent evidence. | Reconcile aliases, backports, follow-up fixes and overlapping/nested functions. Choose a consistent, nonduplicated experimental representation and report/count by supported underlying issue groups, retaining repository/dependence information separately. |
| 6. Explain results with sensible categories | Use understandable broad headings while preserving the detailed explanation of each problem. Do not merge categories just to make sample sizes look better. | Use broader reporting parents and retain detailed mechanism labels for traceability. The current 113-leaf/25-parent hierarchy remains a proposal requiring a definition/boundary check; approval of this approach is not blanket approval of every label assignment. |

**Overall admission rule approved:** the main experiment should use genuine bugs
that can be fairly identified from the function alone, with credible labels and a
usable fixed counterpart. Unresolved examples stay outside that main scored subset
until their eligibility is established. Preserve them and their reasons for review;
do not delete or silently relabel the canonical release.

The function-only rule governs the code context in the controlled model comparison.
The planned static-analysis-augmentation conditions still supply the same tool
findings to each corresponding model under a common protocol. Categories do not have
to be detectable by the chosen static-analysis tools to qualify. This decision does
not remove either the security or correctness part of the project, or the model
development/OpenAI/static-analysis comparisons.

## What is complete, and what these choices do not yet settle

- Original combined source pool: **1,052 pairs**; provisional split membership is
  **742 training /156 validation /154 test**.
- Training discovery and consolidation coverage: **742/742**, with 0 remaining or
  stale consolidation proposals. Held-out validation/test examples have not received
  substantive category adjudication in this audit.
- All 742 consolidation records are still case-level assistant proposals. This
  approval confirms the selection rules, not every label, exclusion or issue group.
- Current proposals comprise 6 conditional retain, 318 missing-context, 80 existing-
  contract, 134 selected-attribution, 70 paired-negative, 80 security-boundary, 4 task-scope,
  25 feature-exclusion and 25 nonrepair-exclusion cases. These are primary review
  dispositions, not automatically final eligibility or independent sample counts.
- **Six conditional retain proposals do not mean a six-example final dataset.**
  Their conditions still need checking, and other cases may become eligible after
  consistent protocol application and evidence resolution. The final size is unknown;
  adequacy for training and evaluation has not been demonstrated.
- The numerical function-input limit, ordinary-knowledge rule, detailed category
  boundaries, selected representations, issue identities, final labels and subset
  membership remain to be finalized. A smaller trustworthy subset is preferable to
  unsupported labels, but its limits must be reported honestly.

## Next steps, in order

1. **Write the precise common input and scoring rules.** Specify the input limit,
   permitted ordinary language/API/runtime knowledge, treatment of oversized
   functions, expected findings, and what counts as a correct detection. Avoid
   selectively adding project context to rescue particular examples. Keep answers,
   fixes, identifiers, advisory titles and labels out of detection inputs.
2. **Apply the approved rules to the training review.** Produce a versioned eligibility
   table for every original training ID: include/defer/proposed exclusion, reasons,
   evidence and unresolved conditions. Check the six conditional retains first;
   distinguish fixable review gaps from genuinely unobservable function-only cases.
   Record later case approvals separately from immutable assistant proposals.
3. **Resolve grouping and category boundaries.** Identify common underlying issues,
   pick representative functions consistently and check the proposed broad/detailed
   category definitions. Preserve original source bytes and split membership.
4. **Measure the viable subset before committing to the experiment.** Count usable
   examples and issue groups, category coverage and security/correctness coverage.
   If too few qualify, discuss feasibility with the supervisor rather than quietly
   loosening the rules or promising model training on an inadequate sample. Any
   necessary scope/context change requires a new explicit decision.
5. **Freeze the training-derived rules, then apply them to held-out data.** Apply the
   same admission and reference-label process to validation/test examples without
   using test content or performance to redesign the taxonomy or tune the models.
   Report categories with fewer than 30 independently adjudicated test groups
   descriptively; do not pad or merge categories to meet that floor.
6. **Publish a versioned experimental package and run a feasibility pilot.** Create
   reproducible subset manifests, issue-group maps, before-only inputs and separate
   reference answers, preserving traceability to the original dataset. Confirm the
   compute/API budget and protocol before model training or paid evaluation. Final
   training, evaluation and resource measurements follow a successful feasibility
   decision, not simply completion of the source audit.

## Does the GitHub dataset repository need another push?

**Yes, it will need an additive update if it is to document and reproduce the final
experiment. The existing source-data release does not need to be replaced.**

Pre-update read-only verification on 1 November 2026 found
<https://github.com/Amaka202/masters-dataset> at main commit
`6a01f3cbfc6c42977450c04423ed8ebe64dfc6e6`, dated 18 October, with 77 tracked files.
That original snapshot contains the source-data/admission package and earlier
research documentation, without CATEGORY_AUDIT files from the subsequent training
audit. The authorized additive update publishes that later material separately.

Recommended publishing sequence:

- Add these decisions and the audited methodology/status documentation as a clearly
  labelled documentation update when publishing is requested.
- Add a separately versioned experimental subset, eligibility/grouping records,
  references and reproducibility checks once those are finalized. Update package
  manifests and guidance to distinguish the original pool from the experimental
  subset, preserving the original source-data release and split provenance.
- Keep reference answers and audit evidence separate from the model-facing inputs;
  document public-benchmark exposure/contamination limits without claiming that
  separation guarantees a model has never seen the public examples.

The student subsequently said "ok go ahead" in response to this publishing/next-step
plan. That authorizes the additive documentation/audit update. The final experimental
subset remains a separate later deliverable, rather than an approved replacement
of the original data release.

## Questions to take to the supervisor

- Does this controlled function-only task support the intended research question,
  with project-context limitations stated clearly?
- After the eligibility count is available, is there enough independent evidence
  for the proposed training and evaluation, including both security and correctness?
- Are the proposed reporting categories and descriptive-only treatment of thin
  categories suitable for the dissertation?

## Supporting audit records

- [Detailed review and approval handoff](CATEGORY_AUDIT_CONSOLIDATION_REVIEW.md)
- [Concrete input/scoring protocol proposal](EXPERIMENT_PROTOCOL_DRAFT.md)
- [Generated consolidation report](CATEGORY_AUDIT_CONSOLIDATION_REPORT.md)
- `CATEGORY_AUDIT_CONSOLIDATION_CASE_REVIEWS.json`: case-level assistant proposals.
- `CATEGORY_AUDIT_CONSOLIDATION_MANIFEST.json`: reproducibility/source fingerprints.
- `DATASET_DECISION.md`: preserved earlier source-selection decision; this note records
  the subsequent experimental-selection choices without rewriting that release input.
