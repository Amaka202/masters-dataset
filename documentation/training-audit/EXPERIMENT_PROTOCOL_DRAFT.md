# Controlled function-only experiment — protocol draft v0.1

**Prepared:** 1 November 2026  
**Basis:** [Student-approved selection principles](EXPERIMENT_SELECTION_DECISIONS.md).  
**Status:** Concrete implementation proposal, not a frozen protocol or approved
experimental subset. Numerical limits below are proposed engineering choices; the
student's earlier agreement established the principles, not these new numbers.

## 1. Question and comparison

Evaluate detection of genuine Python correctness and security problems from one
selected function. Compare the developed model, the specified OpenAI model, static
analysis alone, and each model supplied with identical static-analysis findings.
Use the unchanged base model as a control for the effect of adaptation. Keep both
security and correctness; a category need not be supported by the tools to qualify.

Model names, versions, prompts, decoding settings, tool versions/rules, inference
limits, hardware, costs and random seeds must be recorded in the eventual run
manifest. Model training, paid inference and target-program execution are not part
of this documentation/preflight step.

## 2. Proposed input contract

- One whole selected Python function per primary detection request, from its
  **before** version, preserving exact source text, comments and docstrings.
- A uniform instruction and output schema, language=Python, and an opaque example
  identifier. The identifier must not contain repository names, CVEs or original
  benchmark IDs. Identifiers are bookkeeping, not evidence.
- **Proposed code cap: 16,384 UTF-8 bytes per whole function.** This deterministic,
  tokenizer-independent cap is a preflight proposal, not a claim that bytes equal
  tokens or that every model can accommodate the resulting prompt.
- Do not crop/truncate oversized functions. Mark them outside this proposed input
  contract and retain their IDs/reason. Inspect training-only size counts first;
  verify total prompt/token capacity with the chosen model tokenizers before freeze.
  If the cap changes, version it and reapply it to all training examples before
  examining held-out suitability or results.
- No per-case callers, helpers, imports from elsewhere in the module, configuration,
  tests, advisory text, filenames, repository metadata, labels or fixes in primary
  detection inputs. Lexical nested functions already inside the selected function
  remain part of its unchanged text; they are not independently counted by default.
- Do not selectively add runtime-version hints. If a finding depends critically on
  a version/platform not established in the supplied code under the common knowledge
  rule, defer it from the main function-only subset.
- In augmentation conditions, supply the identical findings from the frozen
  static-analysis pipeline to both corresponding models. Tools get the same selected
  function in a minimal uniform wrapper if necessary, not access to hidden project
  files or fixes. Record incomplete parsing and unsupported checks separately.

## 3. Proposed ordinary-knowledge rule

Allow Python language semantics and ordinary, well-established semantics of an
unambiguously identified standard-library or public API. Do not require models to
infer private project-specific policies or undocumented helper behaviour.

For each candidate, record which knowledge is necessary. Imported-name spelling,
variable names or an advisory alone do not establish the actual binding, a deployed
configuration, a supported input or an attacker's authority. A security finding may
state explicit preconditions, but the label cannot rely on inventing an essential
caller, lower-trust source or security policy that the function does not establish.

Unknown method semantics, external producer/consumer requirements and historical
version-specific behaviour must be resolved at admission, not supplied as special
hints to individual models. Evidence used to determine reference truth remains
adjudication-only even when the conclusion is that a case is not eligible.

## 4. Eligibility record and approval

Each original training ID needs a separate versioned decision with:

1. Established old requirement and actual defect; exclude feature-only, deliberate
   policy/API change or nonrepair components unless a separate old defect is proven.
2. Selected-function attribution, including coordinated/moved responsibility.
3. Security boundary or explicit non-security screening for a correctness label.
4. Necessary knowledge and whether the function-only contract supplies enough.
5. Exact fixed-counterpart scope and any residual/new after failure.
6. Source hashes, evidence, detailed mechanism and proposed reporting parent.
7. Issue identity, overlapping representations and chosen representative.
8. Include/defer/proposed exclusion, decision author/date and unresolved conditions.

All gates must pass before inclusion. Policy approval does not automatically turn
assistant-supported discovery findings or conditional retains into approved cases.
Do not replace missing evidence with confidence scores. Preserve canonical records,
split membership and all historical proposals; later approvals are separate records.

## 5. Fixed counterparts and negative controls

Check the after-version separately for the specified mechanism and admitted
behaviour. Residual failures or introduced regressions defer paired-negative use.
The 70 currently flagged pairs are review dispositions, not 70 independently
confirmed failures or automatically new training examples.

The primary finding task remains before-only. If paired after-controls are used,
define a separate, uniformly administered single-version control condition before
evaluation: only that control function is shown, with a new opaque ID and no before
code, pairing clue, fix label or expected answer. Never show a before/after diff as
part of primary detection. Calling an after-control negative means the reference
mechanism is absent under its checked scope, not that the function has no other bug.

Do not derive a global false-positive rate by assuming every after-version is
universally clean. Negative-control construction and scoring require their own
approved reference scope before running that condition.

## 6. Proposed responses and scoring

Request structured findings containing local line range, broad category, mechanism,
relevant preconditions and explanation. Allow an empty finding list and an explicit
insufficient-information response. Store raw responses as well as parsed output;
do not turn malformed output or service errors into correct predictions.

A target detection requires the same causal mechanism, affected operation/location
and materially correct preconditions as the approved reference. Matching only an
exception name, advisory consequence or broad category is insufficient. An invented
essential assumption does not make an answer correct. Define matching examples and
ambiguous-output handling using training data before scoring held-out predictions.

Use issue-group detection recall as a primary measure after groups are adjudicated.
For precision, independently assess reported findings; an unmatched report is not
automatically false merely because the benchmark references one known bug. Record
unresolved reports separately and disclose how they affect denominators. Report
abstentions, invalid responses and tool/model failures alongside detection results.
Fix matching/review rules before looking at comparative test performance. Record who
reviews outputs; do not imply a second reviewer exists unless one participates.

Report pair-level results as supplementary, with issue/repository dependence stated.
Broad categories summarize results while detailed mechanisms remain traceable.
Categories below30 independently adjudicated test groups receive descriptive
reporting. Do not change categories or sample membership to improve scores/support.

## 7. Freeze and feasibility gates

1. Complete training-only eligibility and issue/representation decisions under one
   version of this protocol; measure usable counts and security/correctness coverage.
2. Confirm dataset adequacy with the student/supervisor. If insufficient, record a
   revised design decision rather than silently weakening the agreed admission rules.
3. Freeze category boundaries, input/scoring rules and eligibility process before
   applying them to held-out validation/test. Use validation for declared development
   choices; do not use test labels/content or results to redesign the experiment.
4. Prepare versioned subset/grouping/reference manifests with source/split hashes.
5. Confirm budget and model/tokenizer feasibility, then run an authorized pilot.
6. Finalize the experiment run manifest before substantive training/evaluation.

Measure theoretical time/space considerations and observed runtime, memory and
resource/API costs. Report public-benchmark exposure and dependence limitations;
do not claim split checks prove a pretrained model never saw public examples.

## Immediate deliverable

A **training-only preflight**, not a final subset: measure whole-function byte sizes
against the proposed cap, preserve current review dispositions and enumerate the
six conditional-retain proposals for priority gate resolution. No semantic labels,
case approvals or independent issue counts are inferred from the mechanical check.
