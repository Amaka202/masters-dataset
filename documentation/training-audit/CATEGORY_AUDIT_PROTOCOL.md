# C1 category and independence audit

Started 22 October 2026. This is a separate, resumable audit layer over the
released 1,052 candidate pairs. It is not an independently adjudicated gold set.

## Evidence and scope

- Preserve every canonical record, original ID and existing split. Read retained
  sources as inert text; never execute downloaded code/tests/notebooks/exploits.
- Develop category definitions from training evidence, not model predictions or
  held-out examples. Freeze the training-derived taxonomy before applying it to
  validation/test references. Unsupported held-out cases stay unresolved; no
  moving examples or changing definitions to meet the screening floor.
- Inspect the before/after function, relevant full-file context and commit/issue
  or advisory evidence. Verify source archive hashes and reconstructed function
  spans. Separate the local fix mechanism from the full reported issue.
- HaPy votes concern changed-line purpose, not semantic function-level truth.
  General-bug origin does not prove non-security status. CVE linkage alone does
  not establish the selected function's relevance. Fixed code is negative only
  for the specified mechanism, never generally clean.
- Record whether the issue is inferable under function-only inputs. Findings
  requiring unavailable caller/configuration context remain conditional. Source
  context used for adjudication must not silently enter model inputs; patches,
  IDs, advisories and answers stay outside detection prompts.

## Persistent records and review status

- `CATEGORY_AUDIT_INPUTS.json`: original release-manifest verification plus
  input fingerprints. A changed input fails refresh; never overwrite the lock.
- `CATEGORY_AUDIT_CATEGORIES.json`: versioned, training-derived draft definitions,
  inclusion/exclusion boundaries and ambiguity notes.
  Draft mechanism labels are discovery notes, not a commitment to that many
  final evaluation categories. Consolidate or refine only from training evidence,
  with a dated revision and preserved meaning/history, never just to reach 30.
- `CATEGORY_AUDIT_LEDGER.jsonl`: append-only per-candidate review events. Include
  original pair ID, increasing revision, exact inspected code hashes, provisional
  fix-family ID, category or null, evidence, reasoning, function-only limitations,
  reviewer, review date and unresolved researcher questions. Latest revision wins.
- `assistant_supported` means an assistant inspected a plausible mechanism;
  `assistant_ambiguous` means unresolved evidence/category/eligibility;
  `assistant_proposed_exclusion` is a proposal, not a final removal. Every current
  event has `researcher_status: pending`. These are not researcher approvals or
  reproduced behavioural results. Retain ambiguous cases in the checkpoint.
- Researcher confirmation and any confirmed independence merges need explicit
  dated evidence and a protocol/tool extension before approved counts can appear.
  Current code intentionally cannot create approved independent counts.

## Counting and dependence

`issue_group` in the source export is a domain bucket, not an issue identity.
Function pairs, issue/fix groups and repository/provenance groups are different
units and must all be reported.

1. Provisional fix families join known same-repository fixing commits, shared
   CVEs/commit-linked CVEs, duplicate provenance and identical AST pairs. Each
   linked family counts once per category/split, irrespective of function count
   or before/after versions. Families may still require merges for aliases,
   backports or common root causes. A commit can cover several issues; retain the
   conservative family until explicit adjudication supports a different unit.
2. Provenance components additionally join repository identities and exact/AST
   versions. These describe dependence and split integrity, not independent
   experimental observations. No exhaustive fork/semantic-clone proof is claimed.
3. CSV provisional-family/repository/provenance counts cover assistant-supported
   cases only; ambiguous and proposed-exclusion pairs have separate columns.
   Categories may share families, so category rows must not be summed to infer
   a global number of independent issues.
4. `audited_independent_issue_count` stays blank while independence/eligibility is
   unadjudicated. Zero reviewed held-out cases means unreviewed, not zero final
   support. Test flags remain `not_assessable_incomplete_audit` until completed
   held-out category/independence adjudication permits a genuine count.
5. Flag fewer than **30 distinct audited issue/fix groups in held-out test** for
   descriptive reporting/review. This is a project-specific screening floor,
   not automatic exclusion, a training-sufficiency claim, a universal MSc rule
   or proof of precision/F1/comparison power. Repository dependence also matters.

## Deterministic continuation

Alternate lexicographically sorted training correctness/security IDs, starting
with correctness; exhaust the longer bucket after the other ends. This is a
convenience review order, not a random or representative sample. Finish the
selected small batch; record each review before moving on. Do not preferentially
skip difficult cases. Append a new revision to revisit a case, preserving history.
Following the researcher's latest 23 October preference, use **50 candidate pairs
per batch**, retaining candidate-by-candidate decisions and refresh checks, and
verify/save the reproducible checkpoint at each batch boundary.

Run from this directory:

```sh
python3 CATEGORY_AUDIT.py refresh
python3 CATEGORY_AUDIT.py check
python3 CATEGORY_AUDIT.py queue --limit 50
python3 CATEGORY_AUDIT.py inspect --pair-id "<exact queued ID>" --context 15
# Optional same-file helper inspection from hash-verified archived source:
python3 CATEGORY_AUDIT.py inspect --pair-id "<exact queued ID>" --helpers _urljoin
```

After each completed review, save its ledger event and run `refresh`. It checks
released input hashes, exact split content, ledger identities/code hashes,
inspected source spans and observed cross-split provenance links, then regenerates
the CSV and exact next-batch checkpoint. It does not rerun the exhaustive lexical
near-duplicate search; that remains the original release verification evidence.

## Decision log

- 2026-10-23: Researcher increased batches from 20 to **50 candidate pairs** at
  144 completed training reviews. This is a checkpoint/work-unit size, not a
  statistical error-detection guarantee. Retain full per-candidate inspection,
  append-only decisions, hash/split/source checks after each saved decision and
  reproducibility verification at the batch boundary. Record unresolved evidence
  explicitly rather than skipping hard cases or guessing to complete a batch.

- 2026-10-22: Initial training-only audit; all assistant decisions provisional.
  Preserve published data and splits; count mechanical families separately from
  researcher-adjudicated independent issues. Freeze taxonomy before held-out work.
- 2026-10-22: First eight queued training candidates inspected. Draft v0.1 has
  five mechanism categories, one seeded by an unresolved HTML-escaping case.
  Seven mechanisms are assistant-supported; one remains ambiguous. Three banner
  functions share one family; two reviewed Spirit redirect functions share another.
  Unresolved caller/sink context must not become a function-level XSS gold label.
- 2026-10-22: Combined repository count verified as **204**, matching the sum of
  repository-disjoint split counts 92/55/57. The historical **151** figure is
  `additional_repositories` in `SECURITY_ADMISSION_AUDIT.json`, not the combined
  dataset's repository total. Source records and releases are unchanged.
- 2026-10-22: Second batch completed the next 12 queued training candidates,
  bringing the checkpoint to **20 reviewed**: **16 assistant-supported**,
  **3 ambiguous**, **1 proposed exclusion**. Draft taxonomy v0.2 adds ten
  training-derived mechanism labels; the original five definitions are retained.
  The first eight ledger events use implicit v0.1; new events explicitly record
  v0.2. All labels/eligibility/independence still await researcher verification.
- 2026-10-22: Explicitly linked nested `guest_only.wrapper` to its already
  reviewed outer function; source-span containment is checked on refresh.
  Source-overlapping representations remain in the canonical release and count
  as one provisional fix family. Any eventual one-representation selection is
  a separate researcher-approved experimental-subset decision.
- 2026-10-22: `LookupModule.run` remains ambiguous without runtime/encoding
  context. EOS state/VRF command generation remains ambiguous because the old
  VRF branch already emits a state command; pre/post-VRF semantics need evidence.
  `GalaxyCLI.execute_init` is a proposed eligibility exclusion: changed wording
  and placeholder text alone do not yet establish an in-scope correctness defect.
  No canonical removal/relabeling is authorised or performed by this proposal.
- 2026-10-22: Retained yt-dlp advisory describes CVE-2024-22423 as an incomplete
  fix related to CVE-2023-40581. Record both IDs as an open root-cause relationship;
  mechanically different CVE/commit families must not become independent counts
  without checking this lineage. Neither a shell exploit nor any dataset program
  was executed. Same-file helper inspection parses inert source ASTs only.
- 2026-10-22: Third batch completed the next 12 queued training candidates,
  bringing the checkpoint to **32 reviewed**: **25 assistant-supported**,
  **5 ambiguous**, **2 proposed exclusions**. Draft taxonomy v0.3 adds six
  training-derived discovery labels (incomplete case handling, CSRF credential
  source, metadata normalization, caller-context propagation, SQL parameterization
  and path confinement), retaining the prior 15 definitions. New ledger events
  record v0.3; the validator accepts the explicitly declared previous versions.
  These 21 draft labels are not a frozen evaluation taxonomy or evidence of
  category sufficiency. Every decision still awaits researcher verification.
- 2026-10-22: The outer yt-dlp `prepare_outtmpl` contains its already-reviewed
  nested `create_key`. Inverse outer-to-inner source containment is now checked
  as well as inner-to-outer links. Both remain in one provisional fix family.
- 2026-10-22: Saleor `get_refresh_token` supports the cookie/CSRF selection
  mismatch through inspected caller context. `clean_refresh_token` already rejects
  empty tokens and is proposed for exclusion from that security-positive subset:
  its change affects missing/invalid-token classification rather than independently
  fixing the bypass. Both functions retain the same conservative issue family.
- 2026-10-22: Sorting Ansible missing-argument names remains an ambiguous
  diagnostic-contract/eligibility case. Nautobot filter-error HTML rendering remains
  ambiguous until error-object escaping and the message-template path are traced;
  the broad unsafe-markup advisory alone cannot settle this selected function.
- 2026-10-22: Three Ansible collection-resolver functions support different
  components of one repair: unknown-version case handling, metadata normalization
  and preserving actual caller parent context. Keep their shared family even when
  displayed in different category rows. The VLAN conflicting-command case supports
  the existing transition category without resolving the earlier ambiguous VRF case.
- 2026-10-22: bottle-auth support is conditional on the trust/constraints of stored
  user IDs and database binding semantics; do not claim direct group-name injection.
  Nova support concerns guest-root path confinement, not shell injection or a
  race-free filesystem guarantee. Record CVE-2012-3361 and the cited maintenance
  fix as lineage questions before any independent counting.
- 2026-10-22: Fourth batch completed the next 12 queued training candidates,
  bringing the checkpoint to **44 reviewed**: **34 assistant-supported**,
  **8 ambiguous**, **2 proposed exclusions**. Draft v0.4 retains the prior 21
  definitions and adds seven training-derived discovery labels: path normalization,
  TLS peer verification, omitted-option defaults, secret-argument exposure,
  coordinate units, redaction-key matching and upload disposition policy.
  These 28 draft labels remain discovery notes, not frozen evaluation classes.
- 2026-10-22: Ansible's UNC join loses leading root separators; the retained
  regression expectation establishes a concrete path contract despite the
  changelog's minor-change classification. Two subscription functions jointly
  preserve omitted quantity so server-side automatic selection can occur; they
  remain one family, not two independent issues or standalone complete fixes.
- 2026-10-22: Sydent support concerns non-verifying SMTP TLS defaults, conditional
  on affected runtime and TLS configuration. It does not imply that plaintext
  modes were removed. Sentry download support concerns globally retrieving a file
  ID after authorization against a different, route-scoped project; rate-limit
  status-code changes are ancillary to this binding defect.
- 2026-10-22: Operator secret-set/add place contents in argv; the inspected runner
  chains CalledProcessError into ModelError, retaining arguments for uncaught
  diagnostic logging. Both belong to one disclosed family. The temporary-file
  repair is mechanism-specific and does not establish confidentiality of all
  metadata, stderr or files readable by the same account.
- 2026-10-22: Black's prefix helper mixes raw-character indent lengths with a
  four-per-tab count. Local mechanism is supported, but demonstrated comment
  indentation and non-style task eligibility remain ambiguous. Black's type-comment
  split guard also remains ambiguous pending actual rendering/type-tool semantics
  and existing-contract evidence; do not automatically exclude meaningful type
  comments as style. The separate bracket-tracker case supports an invalid state
  transition: a nested membership `in` prematurely ends a for-target region and
  corrupts closing-bracket lookup. This supplies a failure mechanism beyond output
  presentation, conditional on inspected caller/state context.
- 2026-10-22: cloud-init's selected normalization-only change remains ambiguous.
  The caller exposes a potential public-file sink, but actual mixed-case sensitive
  input is not established; policy expansion outside the function also performs
  causal work. Do not borrow the commit's log-permission repair as evidence that
  this function itself logs secrets.
- 2026-10-22: Zulip S3 serving support concerns mismatched Content-Type/disposition
  sources, not generic missing escaping. The parent already includes CSP mitigation,
  so browser support matters. After-code safety depends on coordinated signed-URL,
  upload-metadata, nginx-header and cache-key behaviour; these remain explicit
  context/lineage questions. Archived source and SQLite evidence were read only;
  no dataset code, regression fixture or exploit was executed.
- 2026-10-22: Fifth batch completed the next 12 queued training candidates,
  bringing the checkpoint to **56 reviewed**: **42 assistant-supported**,
  **11 ambiguous**, **3 proposed exclusions**. Draft v0.5 retains the prior 28
  definitions and adds input-work amplification, frame-embedding policy and regex
  backtracking. These **31** training-derived discovery labels remain provisional;
  no held-out category review or researcher approval has occurred.
- 2026-10-22: Black-12 decrement helpers support depth-qualified state termination;
  the two increment helpers remain ambiguous because their representation changes
  support a coordinated repair without establishing separate local faulty decisions.
  All four stay in one family. Black-13 async-for tokenization remains ambiguous
  pending the old supported-language contract: feature adoption is not automatically
  an existing correctness defect. Black-14 future-import alias handling supports
  missed grammar cases/assertion failure, conditional on inspected parser context.
- 2026-10-22: Nova affinity support concerns repeated expensive lookups, not every
  linear loop or a constant-time repair. pyLoad support concerns an omitted
  anti-framing response policy; effective proxy/CSP/browser behaviour remains open.
  Black CVE-2024-21503 support uses the actual overlapping regex and failure path;
  the module-level pattern is missing from function-only input, and no exact
  complexity exponent or reproduced timing result is claimed.
- 2026-10-22: Black-15 DebugVisitor.show is proposed for exclusion as an incidental
  debugging API extension without an established violated old string-input contract.
  Other same-commit formatter functions still require individual inspection; no
  canonical record is deleted or relabelled by this proposal.
- 2026-10-22: Rasa model unpacking supports the existing path-confinement mechanism:
  untrusted archive members reach affected tarfile extraction without a boundary
  check. A temporary destination does not contain member paths. The TarSafe
  substitution's precise negative semantics require pinned dependency/member-link
  checks; neither universal archive safety nor safe model deserialization follows.
- 2026-10-23: Sixth batch completed the next 12 queued training candidates,
  bringing the checkpoint to **68 reviewed**: **47 assistant-supported**,
  **18 ambiguous**, **3 proposed exclusions**. This batch contributes five supported
  security mechanisms and seven ambiguous candidates. All researcher statuses
  remain pending. Validation and test category review remain unstarted.
- 2026-10-23: Draft v0.6 adds four training-derived discovery labels: authorization
  subject race, redirect credential stripping, session invalidation and template
  sandboxing. The last has an ambiguous seed because lower-trust template provenance
  is unresolved. These **35** draft labels are not frozen evaluation categories.
  SEC-SHELL-QUOTING now explicitly includes absent as well as inadequate quoting:
  reNgine interpolates URL directly into os.system command text. Its prior v0.5
  inclusion wording was: "Untrusted data is quoted for a shell using rules that do
  not neutralize that shell's expansion/special-character semantics; platform,
  helper and command-use evidence must support the mechanism." Existing inclusion
  cases and platform-specific exclusions retain their meaning; argv transport is
  not a guarantee about the invoked program's own argument handling.
- 2026-10-23: Six further Black-15 functions remain ambiguous. Removal of old line
  classes, exception protocols and helper dispatch is coordinated repair evidence,
  not six independently established local defects. The original bracket-only
  preprocessing domain matters when interpreting the new ENDMARKER guard.
  generate_ignored_nodes revision 2 withdraws the tentative null-boundary category:
  an existing ENDMARKER token is not an absent neighbour, and both loops already
  guard None. Revision 1 is preserved; there are 69 events for 68 unique candidates.
- 2026-10-23: Querybook's request error reaches a direct HTML response before OAuth
  authentication; inspected route registration and exact advisory support escaping,
  with effective CSP/browser conditions explicit. Back In Time's polkit helper
  authorizes a PID-derived subject with zero start-time, permitting identity reuse
  before policy evaluation. The replacement uses the authenticated bus-name subject;
  privileged caller and deployed policy semantics remain verification questions.
- 2026-10-23: urllib3's differently cased Authorization key can survive the old
  cross-origin removal loop. Inspected pinned Retry source shows the matching fix
  also lowercases policy entries; do not assess the after function with the old
  Retry implementation. CVE-2018-25091 is an incomplete-fix lineage of
  CVE-2018-20060 and must not imply independent root causes merely from distinct IDs.
- 2026-10-23: Horizon's invalid-session branch replaces data-only clear with the
  shared logout helper; pinned middleware calls flush and deletes cached identity.
  Django 1.4 reference source distinguishes clear from delete/create in flush, but
  is not proof of the deployed backend/version. Support remains conditional on
  session lifecycle and old-key reuse, not a reproduced fixation attack. Supplemental
  pinned upstream files are identified in ledger evidence but are not hash-locked
  retained snapshots; retain them before final researcher approval.
- 2026-10-23: MLflow's ordinary-to-sandboxed Jinja change is not HTML escaping.
  CardTab accepts template source through add_tab, but no lower-trust ingestion path
  or privilege boundary was established. Values passed to add_html are context, not
  automatically template source. The referenced Huntr page returned only a site
  loading shell, so it provides no additional exploit evidence. Keep this candidate
  ambiguous instead of inferring arbitrary code execution from the CVE alone.
- 2026-10-23: Generated checkpoint date now derives deterministically from the latest
  recorded ledger review date, replacing a hard-coded 22 October header. Regeneration
  remains independent of the wall-clock date. No dataset source was executed.
- 2026-10-23: Seventh batch completed the next 12 queued training candidates,
  bringing the checkpoint to **80 reviewed**: **54 assistant-supported**,
  **23 ambiguous**, **3 proposed exclusions**. This batch adds seven supported
  mechanisms and five ambiguous candidates; there are 81 append-only ledger events
  because the prior generate_ignored_nodes revision is preserved. Researcher
  approval and held-out category adjudication remain pending.
- 2026-10-23: Draft v0.7 adds expected-exception recovery, empty-sequence indexing,
  URL authority boundary and newline round-trip preservation, retaining the prior
  definitions. These **39** discovery labels remain training-derived and provisional;
  newline round-trip seeds are ambiguous pending non-style eligibility. No category
  sufficiency or independent held-out counts follow from this inventory.
- 2026-10-23: Black-15 split_line only removes the obsolete UnformattedLines
  exemption; no wrong local split is established. It remains ambiguous with the
  coordinated representation changes reviewed earlier. Black-16 discovery supports
  a recoverable outside-root symlink ValueError that aborts source enumeration;
  the repair skips symlinks and rethrows other ValueErrors. It is not evidence that
  old code followed the external link and wrote outside root or that the new check
  is race-free. Black-17 supports direct empty-string indexing failure in the parser,
  separately from the same commit's byte-decoder repair; no dataset test was run.
- 2026-10-23: Both Gerapy parse and configure support shell-data separation failures
  on authenticated request paths. The retained advisory specifically names configure;
  parse has independent local source-to-shell evidence but remains in the same CVE
  family. Configure's character denylist leaves shell syntax; argv with shell=False
  removes this sink's shell interpretation without proving all project names or
  invoked-command arguments safe. Authentication and route/platform prerequisites
  remain explicit researcher questions.
- 2026-10-23: LangChain's raw base-URL prefix admits a different authority whose
  hostname extends the base hostname. Actual returned-link recursion is corroborated
  by pinned upstream caller text and the exact retained advisory. New parsed netloc
  checking is a bounded policy repair, not universal SSRF prevention: redirects,
  DNS, same-host and path-prefix concerns remain distinct. Supplemental caller text
  is not a retained hash-locked snapshot and should be retained before approval.
- 2026-10-23: MindsDB connect remains ambiguous despite removal of verify=False.
  Constructor hard-codes http:// in both revisions; connection/query consumers do
  not establish a supported HTTPS path. A reachable HTTPS redirect or base_url
  override could make verification relevant, but neither is demonstrated. The
  after function does not make the ordinary plaintext login encrypted. Avoid
  treating a security-API flag or broad advisory as proof of an effective pair fix.
- 2026-10-23: Black-18 file/stdin newline transport remains ambiguous pending an
  in-scope byte-preservation contract beyond presentation. The parser append change
  is coordinated normalization without an established independent local defect.
  New prepare_input selects one initial newline convention and indexes lines[0]
  without an empty guard; fixed versions are not generally clean. Black-18 parser
  after hash equals Black-17 parser before hash. Preserve shared code/lineage when
  evaluating independence rather than summing function pairs or category rows.
- 2026-10-23: Spirit topic update and publish add two supported source-to-redirect
  paths under the already-reviewed CVE-2022-0869 family. Publish's unsafe destination
  is in the duplicate-post branch, not ordinary successful creation. Authentication,
  valid forms, limiter/hash state and helper semantics constrain reachability; no
  anonymous exploit or CSRF bypass is inferred. Both views count with moderation
  and guest-only changes as one conservative issue family.
- 2026-10-23: Researcher requested 2-4 candidates per task rather than a continuous
  662-candidate run. Default queue and generated next-batch checkpoint now contain
  four candidates; original ordering, records and split membership are unchanged.
- 2026-10-23: Eighth batch completed four queued candidates, bringing the checkpoint
  to **84 reviewed**: **57 assistant-supported**, **23 ambiguous**, **4 proposed
  exclusions**. Batch outcomes: three supported mechanisms and one proposed
  exclusion; 85 ledger events preserve the prior revision. All decisions still
  await researcher approval; held-out category review remains unstarted.
- 2026-10-23: Draft v0.8 adds dynamic Python code evaluation and untrusted config
  discovery, retaining prior discovery labels, for **41** provisional mechanism
  definitions. Expected-exception recovery now explicitly includes supported
  execution-environment conditions as well as input conditions. Prior v0.7 inclusion
  wording was: "A supported input condition raises a specific exception which should
  be handled locally to skip/recover and continue; source, caller and contract
  evidence establish recoverability." No held-out evidence informed this extension.
- 2026-10-23: Black reformat_many supports recovery from optional process-pool
  construction OSError. None selects the event loop's default executor, ordinarily
  a thread pool in one process, not necessarily serial execution. The DIFF path
  still constructs multiprocessing.Manager, so the repair is not universal support
  for restricted multiprocessing environments. schedule_formatting changes only
  its type annotation; its unchanged body already forwards the executor. Propose
  excluding this annotation-only runtime-positive pair, preserving the canonical
  record and shared family pending researcher confirmation.
- 2026-10-23: Eve's AST visitor rebuilds ObjectId call source from a decoded string
  and evaluates it. An allowlist of outer names does not secure the interpolated
  arguments. Direct constructor calls remove this second interpretation; AST parsing
  itself is not the execution sink. Blanket exception swallowing and residual query
  state are outside the supported negative mechanism. No expression was evaluated.
- 2026-10-23: Jupyter config_file_paths implicitly prioritizes CWD, then the app
  passes those paths to inherited configuration loading during initialization.
  Exact advisory corroborates the lower-trust executable-config boundary. Removal
  of implicit CWD insertion does not secure every explicit/environment config path
  or import path; inherited loader/version and launch context still need researcher
  verification. No Jupyter configuration or dataset code was executed.
- 2026-10-23: Researcher superseded the four-candidate preference with larger batches;
  default is now **20 candidate pairs**. This changes checkpoint/queue length, not
  review depth, deterministic order, per-candidate decisions or input protection.
  Persist each decision and refresh as reviewed; verify reproducibility at each
  completed batch. Current review count remains 84; this setting change adds no
  candidate findings or researcher approvals.
- 2026-10-23: Ninth batch completed the next **20** queued training candidates,
  bringing the checkpoint to **104 reviewed**: **68 assistant-supported**,
  **32 ambiguous**, **4 proposed exclusions**. Batch outcomes are eleven supported
  and nine ambiguous; 105 ledger events preserve the prior revision. **638**
  training candidates remain. All researcher statuses remain pending; validation
  and test category adjudication remain unstarted.
- 2026-10-23: Draft v0.9 retains prior labels and adds predictable security
  randomness and security-status lifecycle for **43** provisional discovery
  definitions. These are not frozen evaluation classes. Text-encoding inclusion
  now explicitly covers writing as well as reading/conversion; prior v0.8 wording
  was: "Text containing supported non-ASCII characters is read or converted using
  incompatible runtime/encoding assumptions; the failure path and runtime must be
  established." Black's temporary diagnostic writer can raise UnicodeEncodeError
  under a non-UTF-8 default codec, masking its intended diagnostic. This supports
  a runtime failure mechanism conditional on platform/input, not merely wording.
- 2026-10-23: Session-invalidation scope now includes other-session revocation at
  password changes. Prior v0.8 name was "Authentication teardown preserves a
  reusable session identity" and inclusion was: "A logout/invalid-authentication
  path clears data without required session-key invalidation or rotation; inspect
  the session backend and surrounding authentication lifecycle." Prior notes were:
  "Horizon invalid-session branch delegates to middleware logout/flush; backend
  semantics, key reuse and other login/logout paths remain contextual." The new
  rdiffweb evidence does not change Horizon's provisional reasoning or imply that
  those projects share an issue family. rdiffweb's password update previously left
  username-bound database sessions intact; the fix deletes other sessions and a
  coordinated caller commits. Current session is deliberately retained. Concurrent
  loaded-session resaves, access tokens and alternate backends remain outside the
  supported negative claim.
- 2026-10-23: Black-20 diff labels lose directory identity before the fix; retained
  evidence establishes the display change but not a task-eligible downstream
  consumer failure. It remains ambiguous. Eight Black-22 methods also remain
  ambiguous: renderer, append/attachment/classification, comma removal and three
  split consumers jointly adapt standalone comments and indexed storage. Old
  merged entries can retain several comments as text; one mapped entry does not
  prove deleted comments. New comma-index maintenance and mixed-leaf predicates
  must not be evaluated against an invented old representation. New delimiter
  prefix normalization lives in a decorator. Preserve one shared family and
  establish a concrete non-style or accepted stability-contract failure before
  approving component-level positives. The next queued Black-22 split_line was
  read as caller context only and has no new ledger decision in this batch.
- 2026-10-23: pyrad uses ordinary random.randrange for a sixteen-byte RADIUS
  authenticator consumed by password hiding/reply checking; the replacement is
  module-bound SystemRandom. Function-only after input omits that binding.
  No random bytes, exploit or entropy measurements were generated. Resolve
  wichert/pyrad versus pyradius/pyrad identity before independent counting.
- 2026-10-23: Four Spirit private views add supported redirect paths to the
  existing CVE-2022-0869 family. Private publish is vulnerable in the duplicate-post
  branch, join_in requires a valid owner-rejoin flow, delete_access uses the unsafe
  branch only for another access entry, and create_access redirects after either
  form outcome. Authentication/authorization and user interaction remain explicit
  prerequisites; no anonymous exploit or CSRF bypass follows. Synapse send_join and
  send_leave likewise join the already-reviewed exchange-invite family: lookup uses
  URI identity while event/ACL use body identity before the fix, then standardizes
  on body room_id. The reported federation DoS is not reproduced or local XSS.
- 2026-10-23: qutebrowser's reset per-load SSL flag forgets a previously accepted
  certificate exception, making a reload report HTTPS success. Persistent process
  host history repairs a security assurance indicator, not certificate enforcement.
  A prior override/non-strict policy is required. Host-only memory can retain
  warnings conservatively, and the after-code unreachable elif ok is not a separate
  repair. Listed maintenance backports must remain one root-cause lineage.
- 2026-10-23: Nautobot custom_links has direct editable-value-to-HTML evidence,
  unlike earlier ambiguous filter-error rendering cases. Replacing whole-result
  mark_safe with value-wise format_html requires the coordinated render_jinja2
  helper change that removes implicit SafeString marking; conditional_escape
  otherwise honors __html__. HTML escaping is not URL-scheme validation or template
  sandboxing. New-window attribute formatting and remaining browser/CSP behaviour
  need separate review. All same-CVE methods/backports stay in the existing family.
- 2026-10-23: Supplemental pinned upstream patches/helpers for Synapse, qutebrowser,
  Nautobot, Django reference semantics and rdiffweb were read only as text. They are
  explicitly identified as web evidence, not original hash-locked retained inputs;
  retain them before final researcher approval. No dataset program, fixture,
  configuration or downloaded regression test was executed.
- 2026-10-23: Tenth batch completed the next **20** queued training candidates,
  bringing the checkpoint to **124 reviewed**: **81 assistant-supported**,
  **38 ambiguous**, **5 proposed exclusions**. Batch outcomes are thirteen
  supported, six ambiguous and one proposed exclusion. **125 ledger events**
  preserve the previous revision; **618 training candidates remain**. All
  researcher statuses remain pending. Validation/test adjudication is unstarted.
- 2026-10-23: Draft **v0.10** adds five training-derived mechanism definitions:
  outbound IP-policy enforcement, CSRF token/initiator binding, machine-observable
  error classification, authorization-regex injection and HTTP submission-method
  restriction. There are **48 provisional discovery definitions**, not frozen
  evaluation categories or a claim of adequate independent support. The last two
  additions distinguish regex interpretation from backtracking and GET mutation
  from token/origin-based CSRF protection.
- 2026-10-23: Context-propagation inclusion now explicitly covers incomplete as
  well as substituted context. Previous wording was: "A helper receives a
  substituted identity/context instead of the actual caller context, changing an
  established branch or required operation; both caller and consumer must be
  inspected." Previous notes were: "An installed collection is passed as its own
  parent instead of preserving parent=None for a top-level requirement. Shared
  resolver family, not another independent issue." Black-6 forwards grammar but
  omits the target-dependent tokenizer mode needed for already-supported Python
  3.7 await-containing generators in ordinary def contexts. New configuration
  selection and Driver consumers jointly repair that flow while preserving
  older identifier semantics. The constructor itself only adds a configuration
  holder/API: it remains ambiguous as a repair-only component, rather than being
  judged against a new caller that did not exist before. Both share one family;
  an immutable configuration default is not evidence of a mutable-default bug.
- 2026-10-23: Synapse FederationHandler and HttpPusher constructors select an
  unrestricted client before the fix; inspected downstream key-revocation/push
  consumers use lower-trust destinations. Both share family
  fix-family:851c75f30ade809e3e9b. The exact IP-policy-client fix has no default
  private-network range list apart from unspecified addresses unless configured;
  deprecated federation-only configuration does not automatically cover these
  consumers. Support is conditional on effective configuration, resolver and
  routing, not a claim that a client getter substitution eliminates SSRF.
  Later configuration/default improvements require lineage inspection.
- 2026-10-23: MSS create_app contains its separately exported code route; exact
  source containment is recorded and checked. The route's joined filename reaches
  text reads or direct download opening; safe_join rejection repairs lexical
  traversal, not symlink/realpath or race-free confinement. These two overlapping
  pairs are one issue family, not independent factory and route defects. Markdown
  transforms text; do not claim every binary file can be returned unchanged.
- 2026-10-23: Black-23 assert_equivalent changes diagnostics/chaining while both
  versions already reject input unsupported by the runtime AST parser; propose
  excluding that runtime-positive pair. The same commit's lib2to3_parse does
  repair an established modern-language case: exec as an ordinary identifier is
  rejected by the old keyword grammar. Python-2 feature additions elsewhere do
  not automatically establish an old defect in each changed function. Both
  parser versions still retain a separate empty-input indexing issue.
- 2026-10-23: Black-22 split_line remains ambiguous with its previously reviewed
  coordinated comment-representation family. Black-2 fmt:on scanning within
  decorated structures remains an unresolved formatter-control eligibility case.
  Black-5 comma removal/body building likewise remains ambiguous: retained
  fixtures establish optional-comma normalization, not a demonstrated old
  non-style failure for both exported functions. Do not describe scanning all
  leaves for commas as exact top-level parameter counting. By contrast Black-4
  initial empty-line state has an inspected stability assertion consumer that
  raises after the second formatting pass; its supported mechanism is beyond
  a blank-line preference, conditional on exact parser prefix/state context.
- 2026-10-23: Black-3 main already rejects a missing explicit config through
  Click FileError (exit 1). New Path existence validation classifies it as an
  invalid parameter (exit 2), matching the retained regression expectation.
  This supports a machine-observable error contract, not a claim that the old
  code silently accepted missing configuration. The decorator is runtime code;
  bounded-input policy must not silently omit it from the long selected function.
- 2026-10-23: Bcfg2's two certificate verification functions interpolate paths
  derived from metadata.hostname into shell commands. Key verification adds
  POSIX pipes.quote; CA verification replaces shell text with argv. Both are
  supported conditional on admitted hostname characters and existing cached-file
  branches; key verification also follows a successful CA check. build_cert
  remains ambiguous: its signing operands are server configuration and temporary
  filenames, not an established client-controlled command argument. Do not borrow
  the sibling request-builder's hostname provenance for that function. Keep the
  shared CVE-2011-3211 family and maintenance-fix lineage unresolved for independence.
- 2026-10-23: qutebrowser qute_settings uses request URL option/value to persist
  privileged settings. Token checking, matching template and backend initiator
  checks jointly bind the request. Reachability depends on the affected backend;
  changing editor.command does not itself establish that a command executed.
  Token lifecycle, QUrl password/None semantics and multi-tab behaviour remain
  explicit researcher questions.
- 2026-10-23: Radicale's owner templates interpolate raw login into an anchored
  collection regex before permission evaluation. Authenticated metacharacter
  usernames broaden ownership matches; escaping login/path defaults repairs
  that interpretation boundary. Backend username admission and effective rights
  policy are prerequisites. Later captured-group format substitution is outside
  this negative claim. Resolve Unrud/Kozea repository aliases and backports before
  counting independent issues. No regular expression or exploit was executed.
- 2026-10-23: rdiffweb AdminPage.users already validates deletion fields in its
  helper, but lacks the submission-method guard used by add/edit branches.
  CherryForm binds request.params and validate_on_submit checks membership in
  POST/PUT/PATCH/DELETE before validating. The fix blocks evidenced GET deletion;
  the new guard does not add a token or origin check and is not proof of complete
  CSRF prevention. Admin authorization and browser/cookie reachability remain
  contextual. User/repository deletion share one fix family, distinct from the
  previously reviewed password-session revocation fix.
- 2026-10-23: Supplemental pinned upstream patches/helpers and reference semantics
  for this batch were read as inert text and identified in ledger evidence. They
  are not original hash-locked retained inputs; retain them before researcher
  approval. No dataset code, tests, shell commands from source, configuration,
  certificates, HTTP requests or exploits were executed. Continue at
  HaPy-Bug:bugs-in-py_black-6:0:blib2to3/pgen2/driver.py:Driver.parse_stream_raw.
- 2026-10-23: Eleventh batch completed the next **20** queued training candidates,
  bringing the checkpoint to **144 reviewed**: **96 assistant-supported**,
  **42 ambiguous**, **6 proposed exclusions**. Batch outcomes are fifteen
  supported, four ambiguous and one proposed exclusion. **145 ledger events**
  retain the previous revision; **598 training candidates remain**. All researcher
  statuses remain pending; validation/test category adjudication is unstarted.
- 2026-10-23: Draft **v0.11** retains previous labels and adds workspace-directory
  trust, for **49 provisional discovery definitions**. SciPy weave supplies the
  training evidence: pre-existing predictable writable build/catalog directories
  are accepted without required trust checks. This is distinct from path traversal
  and is not a commitment to 49 evaluation categories or adequate independence.
  First three batch events use v0.10, subsequent events use v0.11; both versions
  remain explicitly accepted by the ledger validator.
- 2026-10-23: Deserialization-allowlist scope now includes object constructors as
  well as global/class resolution. Prior name was "Overbroad global/class resolution
  during deserialization"; prior inclusion was: "Deserialization resolves
  attacker-selected globals through an overbroad namespace exception instead of
  the intended explicit module/name allowlist; caller/advisory supports untrusted
  serialization input." Prior notes were: "Fix removes a shinken.* prefix bypass;
  it is not a universal safety proof for pickle or the remaining allowed globals."
  New YAML evidence does not resolve pystemon's lower-trust configuration boundary
  or change the Shinken seed's original reasoning/family. Runtime-specific unsafe
  constructors require evidence rather than generic yaml.load spelling rules.
- 2026-10-23: Black-6 stream/string tokenization consumers now forward the selected
  tokenizer configuration. String parsing is on the inspected formatter call path;
  a concrete stream-entry trace remains a researcher question. Tokenizer itself
  omits await-in-generator keyword recognition outside async-def state before the
  fix; modern mode repairs that case and defaults still preserve legacy semantics.
  Consumers and tokenizer join the previously reviewed parser/config holder in
  one family, not independent issues. Support concerns concrete forwarding and
  token-selection decisions; constructor-only holder eligibility remains ambiguous.
  The long tokenizer's bounded input must not silently discard necessary context.
- 2026-10-23: Zulip multiuse-invite entry accepts a valid key without binding its
  realm to request realm. New early mismatch rejection and coordinated removal of
  accounts_home's realm override address the shared tenant boundary. Key validity
  does not authorize another organization; multiple organizations and a valid
  invite are prerequisites. Reconcile earlier invitation-binding fixes/backports
  before independence approval; the local function does not independently establish
  every advisory claim about elevated roles or domain restriction bypass.
- 2026-10-23: SciPy default_dir's mode-0700 creation does not validate an existing
  writable directory, and its cached return likewise lacks trust checks. Inspected
  catalog search/load consumers establish artifact use. New helpers check POSIX
  owner/mode and final symlink, choosing another path when needed. intermediate_dir
  similarly stops reusing an unchecked predictable shared-temp root, validating or
  atomically creating a random root. Reused inner interpreter directory is only
  checked with isdir. Neither repair proves race-free use, every nested artifact's
  integrity or Windows ACL security; POSIX checks are skipped on Windows. Both
  function exports remain one CVE-2013-4251 family.
- 2026-10-23: Black-7 long tuple-target wrapping remains ambiguous: retained fixture
  establishes formatting but not an old non-style failure; new equivalence/stability
  assertions do not by themselves prove they failed before. Black-8 differs: checking
  last leaf mistakes a standalone comment for the last code token, adding another
  comma after an already-comma-terminated import. Inspected comment splitting and
  append_safe consumers expose a stray second separator/invalid-output trace.
  New backward scan skips comments and inserts/preserves the last code comma.
  Confirm exact tree/rendering under bounded context before approval. Its after hash
  equals Black-5 builder's before hash, preserving cross-case source lineage.
- 2026-10-23: Black-9's target-restricted grammar list omits future print_function
  for supported Python 2.7 code; new no-print grammar followed by legacy fallback
  repairs keyword-argument print calls. Unspecified targets already try all grammars.
  Correcting the all-Python3 branch comment is incidental; no Python-2 fixture was
  executed. Different parser commits require lineage review, not automatic merging
  or independent counting based only on module/function identity.
- 2026-10-23: MNBikeways RouterAjax.get directly concatenates GET bid/eid into
  pgr_dijkstra SQL arguments; str() is not validation. Separate placeholders and
  parameter tuple repair that SQL-data boundary. Advisory id1/id2 names are local
  variables, not the request keys. Fixed inner query text is distinct from injected
  outer arguments. Database adapter, route exposure and privileges remain contextual;
  malformed values may still fail. No SQL or application request was executed.
- 2026-10-23: django-wiki snippet keyword is raw regex source before escaping.
  Inspected search view/template show GET query and article.render as inputs.
  The literal keyword must occur in content before regex compilation, and search
  selection/snippet extraction must retain suitable text. Word count does not bound
  word length. Support concerns injected regex operators, conditional on a feasible
  guarded input family and actual engine; no reproduced timing/exact exponent or
  universal linear-cost claim. Other Markdown/macro fixes in the same merge do not
  automatically establish selected-function relevance. HTML safety is separate.
- 2026-10-23: Ansible jail fetch/put lexically prepend jail root then call host
  shutil.copyfile before the fix. Jail-controlled symlinks resolve in host namespace,
  enabling host read/overwrite on authorized transfer paths. New dd execution via
  jexec moves the jail-side resolution inside the jail. Keep both directions and
  zone/chroot maintenance commits in one CVE-2015-6240 lineage. After fetch's single
  BUFSIZE read/iteration does not establish transfer completeness, and shell path
  interpolation inside jail is outside this negative mechanism. No transfer,
  jail command, filesystem attack or source shell snippet was executed.
- 2026-10-23: Cookiecutter-1 decodes UTF-8 context JSON through a platform-default
  text stream before; explicit UTF-8 repairs non-ASCII defaults on non-UTF-8 systems.
  JSON parsing cannot recover intended characters after incorrect text decoding.
  Cookiecutter-2 finder/runner remain ambiguous: whole commit adds simultaneous
  shell/Python hooks and changes scalar-to-list interface, but prior multi-hook
  contract is unresolved. Stale dict/all-scripts docstring conflicts with single-path
  return documentation. Do not test old runner conceptually against only new producer.
  Cookiecutter-3 is proposed for exclusion: show_choices=False removes duplicate
  display, while choice validation/default/returned value remain unchanged under
  inspected Click 7.0 semantics. No established non-style consumer contract appears.
- 2026-10-23: Querybook Okta callback reflects raw error into HTML before token
  exchange/login; a valid OAuth code is not needed for that early branch. Markup.escape
  addresses HTML text context, conditional on actual callback response and CSP.
  Next-URL handling is unchanged and separate. pystemon YAML changes remain ambiguous:
  inspected caller loads explicit local config/includes, without established lower-trust
  control or privilege boundary. FullLoader/default-load behaviours vary by PyYAML
  version; major>=5 AND minor>=1 is not a correct general >=5.1 predicate. Safe
  constructors do not establish include confinement or resource-bounded parsing.
- 2026-10-23: Askbot paginator now escapes base_url. Inspected tags view puts raw GET
  sort into that URL even though database ordering selects a fixed supported field;
  separate variable uses must not be conflated. List-mode paginated template passes
  context into a macro's quoted href without explicit escaping. This supports the
  selected attribute-escaping mechanism under affected renderer semantics, not a
  diagnosis borrowed from same-commit user-search/subscription changes. Retain/pin
  supplemental caller/templates and confirm effective autoescape/CSP before approval.
- 2026-10-23: Supplemental upstream django-wiki/Askbot sources and Click reference
  were read as inert text, identified in ledger evidence, and are not original
  hash-locked retained inputs. Retain them before researcher approval. No dataset
  function, fixture, configuration, template, regex, SQL, hook or exploit executed.
  Next queued candidate is
  HaPy-Bug:bugs-in-py_cookiecutter-4:0:cookiecutter/generate.py:generate_files.
- 2026-10-23: Twelfth batch completed **50** queued training candidates, from
  **144 to 194 unique reviews**: **30 assistant-supported**, **20 ambiguous**,
  **0 new proposed exclusions**. Cumulative totals are **126 supported**,
  **62 ambiguous**, **6 proposed exclusions**, with **548 training candidates
  remaining** and **196 append-only ledger events**. All researcher statuses remain
  pending. The batch touches 18 repository identities; supported batch cases span
  21 mechanical fix families, including families reviewed in earlier batches.
  Neither figure is an approved independent issue count or a representative sample.
- 2026-10-23: Draft taxonomy advances through v0.12–v0.16, retaining the 49 prior
  definitions and adding six training-derived discovery labels: sensitive log-file
  permissions, log-record delimiter injection, tensor-axis/shape handling,
  null-token availability, CSV record separation and security-policy case
  normalization. There are now **55 draft definitions**, not 55 final evaluation
  classes or adequately supported categories. Existing category inclusion/exclusion
  boundaries were not broadened by this batch. Null-token seed/notes were corrected
  during review to point to the actual recursive consumer rather than an already
  None-tolerant entry path; that correction does not alter its inclusion boundary.
- 2026-10-23: Cookiecutter-4 generate_files leaves a newly created project directory
  on pre-hook failure; exception-based cleanup addresses that state transition.
  run_script, run_script_with_context and run_hook remain ambiguous repair/API
  components: old status-return signalling is coherent with the matching old caller.
  New exceptions do not prove that old helpers violated a required exception
  contract. Keep all four functions in one family. Cleanup is not arbitrary hook
  rollback, and deleting pre-existing overwritten content is not established safe.
- 2026-10-23: ZenML update_user's old permissions helper is ineffective when RBAC
  is disabled. New no-RBAC administrator gate and protected-field handling address
  cross-user mutation under the inspected store/authentication chain. Admin fields
  are introduced by this fix: do not claim old callers could set fields absent from
  the old model. cloud-init redirect_output gains restricted subprocess umask and
  optional adm group for newly created pipe-sink logs; coordinated password writer
  stops sending passwords to stderr. Existing-file modes, direct redirection,
  filesystem ACLs and other secrets are outside this negative. Retain/pin sink
  configuration and sensitive writers before researcher approval.
- 2026-10-23: Seven more Spirit views retain the existing open-redirect family:
  favorite create/delete, flag creation, comment update/delete/publish/move. Preserve
  actual GET-versus-POST next provenance and login/moderator/form/rate prerequisites.
  Delete mutates on POST but reads next from GET. Favorite creation/move redirect
  after invalid as well as valid forms. Publish has duplicate-hash and saved-comment
  outcomes, not two issues. Same-fix safe_redirect validates host/scheme and supports
  callable defaults; its supplemental text still needs retained evidence. No extra
  independent issue is counted for these sibling functions.
- 2026-10-23: Keras-10 standardize_weights indexes shape[1] on supported rank-one
  class labels; the rank-aware branch repairs that omitted case. Same-fix joint
  class/sample-weight multiplication replaces an old documented warning/ignore
  policy and is not independently labelled an old bug. Keras-11 fit/evaluate/predict
  use nominal Sequence checks that miss compatible preprocessing producers; new
  marker/structural predicate changes train/validation/evaluation/prediction routing.
  Pin foreign producer/dependency contract. Attribute presence does not prove every
  accepted object is a valid Sequence; three functions remain one family.
- 2026-10-23: Keras-12 unconditional flatten collapses sample/time axes while argmax
  predictions retain them; rank-aware singleton squeeze preserves the comparison
  shape. Its (6,3,1) regression predicts (6,3,1,7), so it is not by itself a test of
  equal-rank trailing-singleton squeeze. Keras-14 and Keras-17 instead repair max
  reduction of rank-one sparse targets, which had collapsed the sample labels into
  one maximum class. Keras-17 after is exactly Keras-12 before: a scoped negative
  for one mechanism can retain another defect. Reconcile this source chain and
  related max/flatten roots before independent counting. No tensors were evaluated.
- 2026-10-23: Keras-13 workers=0 Sequence validation iterates the training source
  and omits validation length; new val_data/length forwarding matches the worker
  branch. Keras-15 file opening allows Python-3 Windows text translation to duplicate
  CSV record boundaries when csv.excel already emits CRLF. Coordinated newline='\n'
  prevents that translation; retained tests establish physical row/column counts,
  not just newline preference. Constructor settings transport and Python-2 fieldname
  Unicode conversion remain ambiguous old-defect/repair-only cases. Python-2 Windows
  already selected binary mode before; do not generalize the Python-3 diagnosis.
- 2026-10-23: Keras-18 old docs explicitly permit Session.run options/run_metadata,
  yet constructor rejects those residual kwargs. Constructor supports an omitted
  valid-case defect. _call metadata forwarding remains ambiguous as an independent
  old positive because matching old constructor prevents that state from reaching
  it. New constructor plus old consumer is not an old reachable failure. Keras-19
  adds independent output_size and changes default stacked-state order. Five
  selected methods remain ambiguous: old first-state output dimension and reversed
  state unpacking match the old documented API. New cells/order cannot establish old
  defects by representation mismatch. CNTK first-to-last state change also needs
  backend semantics; the new differing-output/state test explicitly skips CNTK.
- 2026-10-23: Keras-1 print/update/update_add remain runtime/eligibility ambiguous.
  Old assignment APIs already represent or perform mutation in normal contexts;
  explicit dependencies alone do not prove an old missing update. Inspected eval
  uses .numpy when available in TF2, so pinned assignment-return type and graph/eager
  semantics are essential. Legacy print already attaches an effect when evaluated
  under supported APIs; TF2 symbol/scope compatibility and diagnostic-output scope
  must be distinguished. Broad commit also changes seeded initializers; its single
  conservative family may cover multiple roots and needs explicit reconciliation.
- 2026-10-23: MLflow experiment handler accepts artifact-location fragments into
  stored metadata despite query validation. New fragment rejection and coordinated
  source local-URI check address the disclosed local-read bypass. Handler is not a
  direct file-open sink; retain exact patch and trace pinned downstream conversion
  before approval. Reconcile CVE-2023-6909 lineage. Nautobot job-button composition
  supports the existing escaping family with coordinated removal of rendered-text
  SafeString marking; not URL-scheme protection or Jinja sandboxing. Mayan option
  label escaping remains ambiguous: supplemental template includes ordinary Django
  select_option; actual safe-label/frontend reinterpretation needs explanation.
- 2026-10-23: pyLoad API login embeds request username in failure/success log text;
  replacing CR/LF prevents line-oriented record forgery under the affected handler.
  Authentication success is not required for failure logging. Advisory's example
  targets sibling UI login, not direct proof of API route behaviour. qutebrowser
  WebKit handler gains operation/origin checks before settings dispatch; inspected
  network manager supplies current tab URL or empty URL. Together with previously
  reviewed token consumer this is one CSRF family; setting editor.command is not
  itself evidence of command execution. URL canonicalization/backend limits remain.
- 2026-10-23: markdown-it-py recursive renderInlineAsText asserts children exist for
  nested images, while inspected producer can assign children=None; guarded recursion
  repairs the concrete nested-empty-image failure. Top-level render remains ambiguous
  because ordinary core inline pass initializes children to a list. **Revision 2**
  of image explicitly withdraws revision 1's incorrect None-iteration inference:
  old text renderer already iterates tokens or []. Thus entry image guard is
  repair/hardening, not an established old None-consumption defect; ordinary producer
  also supplies alt, leaving removed attrs assertion reachability unresolved. Keep
  all three exports in one family, retain history, and distinguish per-render failure
  from process-wide service denial. Supplemental parser/fixture text needs retention.
- 2026-10-23: Nova EC2 protocol validation is case-insensitive but persists original
  spelling. Inspected firewall's lowercase-only branches then omit port/type limits
  from otherwise selected protocol rules. New producer lowercases and coordinated
  consumer handles existing records; pin network driver/IPTables semantics and
  permissions. Bcfg2 get_ipcache_entry interpolates metadata hostname/alias into
  shell getent only after uncached DNS failure. New argv removes shell interpretation;
  metadata admission, DNS failure and option parsing remain distinct prerequisites.
  Same SSLCA/cache family and maintenance lineage, not another independent issue.
- 2026-10-23: LangChain LocalFileStore character allowlist admits parent segments
  and absolute paths reaching read/write/delete consumers. New abspath/commonpath
  plus absolute-root constructor checks lexical boundaries, not symlinks or races.
  xmpp-http-upload get_paths remains ambiguous as a selected old-defect pair: suffix
  helper previously receives a path from flawed caller sanitized_join; new root/path
  API moves validation into this helper. GET requires readable paired .data/.meta
  files; PUT requires valid HMAC and exclusive creation. Do not claim arbitrary
  unrestricted file access or independent defects from a moved repair boundary.
- 2026-10-23: Shuup command dispatcher directly reflects unknown POST command into
  Problem, unlike earlier constant-reason provenance. Inspected supplemental
  middleware renders exception.message for non-AJAX and JSON otherwise; ordinary
  template interpolation still leaves effective autoescape/alternate-template
  interpretation unresolved. It remains ambiguous rather than borrowing CVE-level
  XSS. yt-dlp shell_quote likewise remains ambiguous: disclosed old q-format path
  calls compat_shlex_quote directly, and this fix introduces shell_quote(shell=True)
  there. An actual old shell consumer of the selected wrapper is still needed;
  default shell=False does not promise cmd percent-expansion protection. Reconcile
  previous q-format review and incomplete-fix CVE lineage as one root issue.
- 2026-10-23: Ansible chroot fetch/put confirms earlier jail diagnosis: lexical root
  prefix then host copyfile follows guest-controlled symlinks outside root. Root-only
  constructor and new chroot command helper establish actual namespace/privilege
  context. New dd guest-side resolution repairs that boundary, not all streaming
  correctness or guest-shell quoting. Both directions and jail/zone maintenance
  commits remain one CVE-2015-6240 family. No transfer or filesystem attack executed.
- 2026-10-23: Supplemental upstream patches/templates/parser/middleware sources
  were inspected as inert text and identified in ledger evidence; they are not
  additions to the original hash-locked retained inputs. Retention/pinning remains
  a prerequisite to researcher approval where relied upon. No dataset function,
  fixture, template, configuration, regex, SQL, hook, browser request, backend or
  exploit was executed. Next queued candidate is
  HaPy-Bug:bugs-in-py_keras-1:0:keras/backend/tensorflow_backend.py:update_sub.
- 2026-10-23: Thirteenth batch completed **50** queued training candidates, from
  **194 to 244 unique reviews**: **33 assistant-supported**, **17 ambiguous**, and
  **0 new proposed exclusions**. Cumulative totals are **159 supported**,
  **79 ambiguous**, **6 proposed exclusions**, with **498 training candidates
  remaining** and **246 append-only ledger events**. All researcher statuses remain
  pending. This batch touches 15 repository identities; its supported cases span
  25 mechanical fix families, including previously reviewed families. Overall there
  are 128 reviewed mechanical families and 101 with a supported assessment. These
  are provisional bookkeeping counts, not researcher-approved independent issues.
  The reviewed ID set is exactly the first 244 candidates in the training queue.
- 2026-10-23: Draft taxonomy advances through **v0.17–v0.20**, adding four
  training-derived discovery labels: validation-secret logging, XML entity
  expansion, KDF output-length accounting, and inclusive-range boundaries. There
  are **59 draft definitions**, not final evaluation classes. The existing
  SEC-LOG-FILE-PERMISSIONS boundary was explicitly broadened in v0.19 to include
  retained file modes as well as creation permissions. Previous name was
  "Sensitive log output is created with excessive read permissions"; previous
  inclusion was "Sensitive process output reaches a file readable by principals
  outside its intended audience because file-creation permissions or log-sink
  process identity are insufficient; inspect sensitive writers, sink configuration
  and creation semantics." New definition covers file-creation **or retained**
  permissions and effective file-mode enforcement. Rationale: a separate training
  cloud-init fix enforces mode on an existing log, which a creation-only umask
  cannot repair. This does not retroactively expand the scoped negative of the
  earlier pipe-sink case. No held-out data or predictions informed these changes.
- 2026-10-23: Keras-1 update_sub remains ambiguous for the same pinned TF
  graph/eager assignment-return question as update/update_add. RandomNormal,
  RandomUniform, TruncatedNormal and VarianceScaling seed increments also remain
  ambiguous: a seed description alone does not establish required variation on
  repeated use of the same initializer under the matching old backend. No security
  entropy claim is made. These share a broad conservative fix family that may
  contain multiple actual roots and still needs reconciliation.
- 2026-10-23: Keras-20's six selected methods remain ambiguous feature/repair
  components: CNTK/TensorFlow/Theano conv2d_transpose, TensorFlow input preprocessing,
  layer get_config and deconv_length. New dilation_rate/output geometry is absent
  from matching old layer/backend APIs; ordinary dilation=1 remains unchanged.
  A new dilated caller plus old helper is not an old supported-input defect.
  CNTK GPU/test limitations remain. Keras-21 restore_best_weights is likewise a
  new opt-in capability defaulting False; retaining last-epoch weights was the old
  behaviour, not established erroneous merely because restoration was added.
- 2026-10-23: Keras-23 Sequential.add prematurely reads batch_input_shape/dtype
  from a nested deferred model's deepest layer before its existing lazy hasattr
  path; removing those eager reads repairs an accepted deferred case. Keras-24
  TensorBoard histogram setup treats list-valued layer.output as one tensor;
  regression supplies differently ranked outputs, supporting callback setup
  failure rather than a histogram-label preference. Keras-26 masked symbolic RNN
  reuses output-width tiled mask for differently sized additional states; per-state
  tiling mirrors the already-correct unrolled branch. Pin backend conversion/where
  contracts and prerequisites; no tensor, model or callback was executed.
- 2026-10-23: Keras-28 __getitem__ and __len__ omit an inclusive final target:
  constructor defaults end_index to len(data)-1 but range/high and count exclude
  that endpoint. Both methods support CORR-INCLUSIVE-RANGE-BOUNDARY as one root,
  including the singleton remaining-target case. Complete normal iteration needs
  both range and length changes; neither selected negative promises all stride or
  generation behaviour. Keras-29 fit/test/evaluate_generator resets raw metrics
  configuration, whose dictionary iteration yields output names rather than
  registered stateful metric functions. Coordinated compile registration plus
  consumers repairs cross-epoch/evaluation accumulation. Same-fix test_on_batch
  was inspected subsequently and does not itself reset state, supporting the
  evaluate_generator lifecycle concern; retain that context for adjudication.
- 2026-10-23: Keras-30 native-tensor generator handling remains ambiguous as
  established-input repair versus generator API extension. Array-loop support
  alone does not establish prior generator acceptance of x=None/empty inputs.
  Its evaluate_generator after bytes equal Keras-29 before bytes, so the native
  tensor scoped negative can still contain the later metric-reset defect.
  Keras-31 unqualified squeeze removes the batch axis when lengths have documented
  shape (1,1); axis=-1 preserves vectors required by sparse-label scan and CTC.
  Keras-32 tests wait before counting current non-improvement and increments again
  after resetting on a reduction; moving increment repairs patience transitions,
  separate from epsilon/min_delta API rename. Keras-33 multi-character split
  breaks equal-length maketrans construction on Python3/Python2 byte text while
  old Python2 Unicode mapping already handles it. Keras-34 evaluate_generator
  supports Sequence/workers=0 but calls next on the Sequence rather than iter;
  coordinated Sequence.__iter__ supplies repeated traversal. Its retained new
  regression covers sibling training, not a direct evaluation assertion.
- 2026-10-23: cloud-init schema validation can log sensitive user-data fragments
  into a lower-trust log. New log_details=False is selected by a coordinated boot
  caller; default True, strict exceptions and privileged CLI details remain.
  A separate cloud-init existing-log initialization uses preserve_mode=True,
  preserving an excessively readable mode despite requesting 0640; False enforces
  mode before ownership attempts. Neither later chmod nor ownership changes undo
  prior disclosure. Keep creation-mode, retained-mode and diagnostic suppression
  submechanisms distinct and reconcile the cloud-init CVE lineage explicitly.
- 2026-10-23: Solara nbextensions request dir shifts the trusted send_from_directory
  root; a parent segment can move it outside the intended extension directory.
  New fixed root/combined relative-path check repairs this lexical boundary, not
  symlink safety. HTTP fragments are not transmitted despite advisory wording.
  Nova's image path realpath runs without the privileged writer's visibility;
  privileged readlink canonicalization repairs root-only symlink resolution before
  mkdir/tee. Old code already checks a lexical prefix; no race-free guarantee.
  Reconcile CVE-2012-3361 incomplete-fix lineage. MSS uploads similarly shifts a
  trusted download root using request name; fixed-root safe_join repairs it.
  MSS create_app is in another file and does not overlap uploads' source span.
- 2026-10-23: Nautobot repository lookup has a global change permission but lacks
  object-restricted UUID lookup; restrict(user, "change") restores scoped lookup,
  subject to worker/caller access. Protected-delete error composition also formats
  ordinary object strings into mark_safe markup. Same-fix generic deletion callers
  and Device name/display/__str__ establish a stored-name route, conditional on
  name admission, writer permissions, a protected relation and actual message
  template sink. New format_html protects ordinary strings; get_absolute_url and
  SafeString/URL-scheme cases are not generally clean. Same existing HTML family.
- 2026-10-23: Four more Spirit views (config_basic, notification create/update/
  mark-all-read) join the existing open-redirect family. Preserve successful admin
  POST reading GET next for config_basic; notification routes read POST next and
  retain login/POST/ownership/form gates. No additional independent issue inferred.
  OAuthenticator GitLab whitelist confuses all-available group visibility with
  membership for non-admins; explicit members/user_id requests repair admission.
  Authenticate caller binds returned GitLab user id and checks configured whitelist;
  this is not access to another user's account or a defect in every authenticator.
- 2026-10-23: LangChain nonstreaming XML parser and async stream support a shared
  entity-expansion availability mechanism. Nonstreaming preprocessing can retain
  declarations; old async parser directly feeds raw chunks. Sync streaming remains
  ambiguous because existing prefix filtering removes pre-root declarations in
  ordinary input, requiring a distinct viable chunk/declaration path. Defusedxml
  entity rejection needs pinned Python/Expat limits and lower-trust completion
  influence. ElementTree use is not automatic external-file XXE, and the repair is
  not universal depth/memory safety. All three methods remain one fix family.
- 2026-10-23: cryptography HKDFExpand divides byte digest_size by eight and counts
  initial empty output as a generated block. Small positive requests up to the
  inspected digest_size//8 boundary can return empty; larger requests can perform
  excess block work. Fix uses byte units and excludes empty accumulator from block
  count. Advisory shorthand "less than digest_size" is broader than this loop's
  inspected empty-output boundary. Constructor maximum/default-salt changes are
  separate, and downstream acceptance of short keys must be pinned.
- 2026-10-23: pyLoad curl initialization explicitly disables SSL_VERIFYPEER; enabling
  it restores chain verification for HTTPS handles retaining that option. User-agent
  edit is unrelated; later overrides, trust stores and hostname checks remain
  contextual. UI login CR/LF logging confirms the advisory's actual failed-login
  route and shares the earlier API logging family; valid credentials are not
  needed for the failure log. Horizon logout clears data without rotating/discarding
  session id under the matching old login lifecycle. New middleware helper flushes
  session/cached user; same fix separately cycles login keys. One logout change
  alone is not complete fixation prevention; pin historical backend semantics.
- 2026-10-23: QAnything check_kb_exist supports SQL-parameterization repair:
  supplemental request callers supply kb_ids before validation and safe_get does
  not sanitize SQL. Post-query set rejection cannot prevent query interpretation.
  check_file_exist_by_name is also supported conditionally on pinned MySQL/connector
  mode: apostrophe-only backslash escaping fails to account for existing backslashes
  and NO_BACKSLASH_ESCAPES; upload name cleaning does not remove ASCII SQL syntax.
  get_knowledge_base_name remains ambiguous because its actual lower-trust caller
  was not located. delete_knowledge_base remains ambiguous because known request
  caller checks valid ids and performs vector-store partition deletion first.
  Sibling SQL injection does not prove these gates permit an id to this update.
  Importantly, its after version reuses [user_id]+kb_ids for a second query whose
  placeholders occur kb_ids then user_id: parameterization removes SQL syntax
  interpretation but introduces a separate argument-order correctness problem.
  Do not treat this fixed function as generally clean. All four are one provisional
  SQL family, not four independent issues.
- 2026-10-23: Starlette _get_form passes HTTP multipart content into an old parser
  retaining unbounded fields and file objects. New default max_fields/max_files=1000
  are explicitly forwarded and enforced by coordinated header counters. Parser's
  new defaults also protect old-style constructor calls: selected wrapper exposes
  customization, with contextual eligibility still requiring researcher approval.
  Application request.form use and python-multipart installation are prerequisites.
  Counts do not bound total bytes/single-field size, and cached forms are not
  retroactively constrained. Same parser/root/alias family needs reconciliation.
  Shuup get_current_phase stays ambiguous: formatting a request-like identifier
  into Http404 is not an HTML sink. Phase exhaustion, input route and actual unsafe
  error template must be established rather than borrowing a broad XSS advisory or
  assuming ordinary autoescaped Django 404 rendering is unsafe.
- 2026-10-23: Supplemental pinned QAnything source read as inert text:
  https://raw.githubusercontent.com/netease-youdao/QAnything/35753b892c2c4361b318d68dfa3e251c85ce889c/qanything_kernel/qanything_server/handler.py
  and
  https://raw.githubusercontent.com/netease-youdao/QAnything/35753b892c2c4361b318d68dfa3e251c85ce889c/qanything_kernel/utils/general_utils.py.
  These and earlier supplemental sources are not additions to the 45 original
  hash-locked inputs; retain/hash before researcher approval where relied upon.
  No dataset function, test, tensor, template, configuration, regex, SQL, hook,
  browser request, backend, partition operation or exploit was executed.
  Next queued candidate is
  HaPy-Bug:bugs-in-py_keras-34:0:keras/engine/training.py:Model.predict_generator,
  followed by CVEfixes:264881774460682:62477479055333. Training taxonomy and
  independence reconciliation remain unfinished; validation/test adjudication
  remains unstarted, with no training or evaluation run authorized by this audit.

### Fourteenth batch: 244 to 294 provisional training reviews (2026-10-23)

- Completed the next 50 queued candidates: 30 assistant-supported, 19 ambiguous
  and one proposed exclusion, across 15 repository identities and 20 mechanical
  families with supported assessments in this batch. Overall: 294/742 training
  pairs reviewed, 189 supported, 98 ambiguous and seven proposed exclusions;
  448 remain. The ledger has 296 append-only events including prior revisions.
  All researcher statuses remain pending. Reviewed IDs equal exactly the first
  294 deterministic training-queue IDs. The 152 reviewed mechanical families and
  119 containing supported assessments are not approved independent issue counts.
- Training-only draft taxonomy advanced from v0.20 to v0.24, adding five
  definitions (59 to 64): v0.21 SEC-CORS-ORIGIN-BOUNDARY, v0.22
  SEC-SENSITIVE-ACTION-REAUTH, v0.23 SEC-INTERNAL-REQUEST-OPTION-INJECTION,
  and v0.24 CORR-CONFIGURATION-PRECEDENCE / CORR-ZERO-DENOMINATOR. These
  distinguish credentialed origin delimiters, sensitive-action step-up checks,
  internal request controls, established configuration precedence and empty-mask
  numerical normalization. Existing definitions were not broadened this batch.
  Definitions and older assignments still need consolidation before approval;
  in particular Progbar's absent target comparison is not a neighbour-dereference
  example despite its current provisional CORR-NULL-BOUNDARY assignment.
- Keras-34 prediction corroborates the Sequence/workers=0 next-versus-iter defect
  from the previous evaluation sibling; the coordinated iterator is essential.
  Keras-36 separable_conv1d has inconsistent spatial stride components relative
  to historical TensorFlow requirements. Keras-38 stacked cells construct rank-3
  next-cell input instead of (batch, output_dim). Keras-40 output shapes repeat
  the first state width for heterogeneous states; preserve existing reversal
  rather than conflate this with the later output_size feature family.
- Keras-35 remains ambiguous: callback relocation addresses documented ordering
  but passes PIL where the old contract says rank-3 NumPy array. The resize
  regression only checks shape. Removing the standardize callback is coordinated
  relocation, not a demonstrated old local defect. Keras-37 RNN predicate change
  lacks an established differing supported tensor; Bidirectional.call's list
  guard removal coordinates a new upstream __call__, not an old list failure.
- Keras-39 target=None can reach a Python-3 comparison TypeError in throttled
  verbose progress reporting; this is machine-visible failure rather than display
  preference. Keras-3 clone uses a one-element None mask list for a multi-output
  layer, truncating tensor_map construction through zip. The regression's .all
  comparison is weak, but construction still exercises the missing-output path.
- Keras-41 GeneratorEnqueuer worker faults previously stop the producer without
  conveying the original failure to its consumer. Tagged success/error transport
  and draining/rethrow repair that machine-observable exception path. Nested
  data_generator_task overlaps start: ledger overlap annotations preserve one
  family, not independent functions. stop's Queue.close versus Manager.shutdown
  is coordinated representation change, so remains ambiguous. OrderedEnqueuer.get
  is proposed for exclusion: the selected change retains StopIteration(e) and
  adds explicit cause chaining, a diagnostic change rather than the sibling's
  exception transport repair. Pin Python/PEP479/process serialization semantics.
- Keras-42 base evaluation/prediction and three Sequential wrappers remain
  ambiguous feature/repair-only API changes: old supplied-step forwarding is
  coherent, old Sequence policy explicitly ignored supplied steps, and new None
  defaults plus custom step overrides do not alone establish old contract failure.
  Keras-4's keyword var_list fixes a concrete custom override that only accepts
  loss and **kwargs, but ordinary TensorFlow already binds the second argument
  to var_list. Establish prior subclass interoperability promise before admission.
- Keras-45 implementation=1 adds None biases despite documented use_bias=False
  and build's explicit absent slices; guarded bias_add handles that supported case.
  Keras-5 downloader ignores already-established KERAS_HOME while backend honours
  it; new selection keeps explicit cache_dir priority and existing unwritable-base
  fallback. Keras-6 all-zero masks yield 0/0, repaired with positive backend epsilon;
  unchanged all-zero sample-weight denominator and nonfinite inputs remain outside
  the scoped negative. Keras-7 unrestricted squeeze collapses one sample to rank
  zero instead of documented (1,); axis=-1 preserves the sample axis. Empty-batch
  regression coverage is not a separate established old defect.
- Sentry's credentialed CORS check accepts unrelated suffix hostnames because
  endswith(basehost) omits hostname boundaries. Nested wrapper and outer decorator
  overlap and are one family; empty default basehost/browser credential policy
  remain prerequisites. ZenML permits an active session to change its own password
  without current-password verification. New reauthentication is distinct from
  the separate ban on changing other users' passwords; not unauthenticated takeover.
- yt-dlp Vimeo forwards arbitrary smuggled http_headers to requests, whose
  clean_proxies consumes Ytdl-Request-Proxy as a privileged routing option.
  Referer-only transfer removes that internal-option boundary. Generic extractor
  arbitrary-target advisory paths are not automatically Vimeo paths, and TLS/
  secure-cookie rules prevent unconditional credential-disclosure claims. This
  family differs from the earlier shell-quoting family.
- Kohya group_images interpolates GUI paths/extensions into shell command text.
  Switching shell=False removes that shell interpretation but retains one command
  string, which generally fails executable lookup on POSIX: repaired security
  mechanism does not establish functional correctness. py7zr retains parent
  segments in lexical paths reaching extraction writes; resolved sanitizer/root
  normalization repairs that boundary, not race-free filesystem safety. The
  trailing-slash 404 redirect can retain a double-leading slash and generate a
  network-path Location; pin request-path/proxy normalization. qutebrowser history
  returns json.dumps under text/html, so JSON encoding does not neutralize HTML
  in stored titles/URLs; victim history navigation/frontend/CSP remain context.
- Five additional Spirit views join the existing redirect family. Resend-activation,
  custom_login and register have authenticated early GET-next redirects; custom_logout
  has an anonymous early GET-next redirect. Admin user edit requires authorization,
  successful POST and both valid forms, but then also reads GET next. Preserve
  those branch-specific gates instead of copying the advisory's generic privileges.
- MLflow is_local_uri's remote file authority change remains ambiguous: matching
  registration caller already rejects file sources unless an explicit environment
  setting permits them, then applies relative-path checks. Saleor's new JWT setup
  guard does not identify a selected secret-bearing exception producer; generic
  internal error formatting is fixed elsewhere. markdown-it typographer's top-level
  inline guard needs a producer of absent children; nested image None does not
  prove that distinct loop. Nautobot regex validation messages and Shuup's generic
  extract_messages still need actual unsafe HTML consumers, admitted writers and
  safe-string/exception formatting traces; ordinary autoescape may already apply.
- Radicale Windows storage consumers share fix-family:60cad649b336e770141b.
  Raw logical-path joins can escape the backend root through drive/root components;
  coordinated inherited _filesystem_path uses checked component translation.
  remove, content text, directory creation and collection delete provide actual
  mutation/read consumers. Content getter serializes parsed calendar/contact data,
  not every arbitrary byte stream. is_node, last_modified and is_leaf remain
  ambiguous pending request/classification or observable metadata consequences.
  Fixed is_leaf still checks original logical path + '.props', inconsistent with
  its translated directory path; do not claim a generally clean classifier.
  Collection delete's unchanged _props_path consumer is protected only through the
  coordinated property's own change. No symlink/race guarantee is inferred.
- Supplemental backend source read as inert text:
  https://raw.githubusercontent.com/keras-team/keras/e11c48d9ce3ee47bb8a966549b14cbd5b10ee70d/keras/backend/__init__.py
  and the same URL with commit suffix %5E for its parent. Both honour KERAS_HOME.
  Retain/hash-pin this and previously used Spirit helper before approval. They
  are not additions to the 45 protected original inputs. Read-only SQLite source
  inspection and audit helper execution never execute dataset source, fixtures,
  model/tensor operations, configurations, callbacks, regexes, SQL from examples,
  requests or exploits. No training/evaluation has been performed.
- Resume at HaPy-Bug:bugs-in-py_keras-8:0:keras/engine/network.py:Network.from_config,
  followed by CVEfixes:30027234712539:48657133368461. The next 50-candidate
  checkpoint would be 344 reviews. Training consolidation and independence
  adjudication remain unfinished; held-out inspection waits for a frozen protocol.

### Fifteenth batch: 294 to 344 provisional training reviews (2026-10-24)

- Completed the next 50 queued training candidates: 45 assistant-supported, four
  ambiguous and one proposed exclusion, across 18 repository identities and 37
  mechanical families with supported assessments in this batch. Overall: 344/742
  training pairs reviewed, 234 supported, 102 ambiguous and eight proposed
  exclusions; 398 remain. The ledger has 346 events including prior revisions.
  Reviewed IDs equal exactly the first 344 deterministic training-queue IDs, and
  all researcher statuses remain pending. The 184 reviewed mechanical families
  and 150 containing supported assessments are not approved independent counts.
- Training-only draft taxonomy advanced from v0.24 to v0.29, adding seven
  definitions (64 to 71): v0.25 SEC-INPUT-SIZE-BOUND; v0.26
  CORR-LABEL-ALIGNMENT; v0.27 SEC-REDIRECT-BODY-DISCLOSURE,
  SEC-INPUT-DECODE-AVAILABILITY and CORR-DTYPE-PRESERVATION; v0.28
  SEC-CREDENTIAL-GUESS-THROTTLE; v0.29 CORR-SORTED-INPUT-PRECONDITION.
  Existing definitions were not broadened. These remain provisional mechanism
  definitions, requiring consolidation and researcher approval before held-out
  adjudication. Correctness assignments still require non-security screening.
- Keras-8 shared-layer reconstruction requeues an unavailable node but continues
  later calls of that layer, changing inbound-node numbering. Nested process_node
  signals failure and the coordinated outer loop retains the ordered pending
  suffix. Outer/nested source overlap is recorded; neither counts independently,
  and the new helper cannot be transplanted into the old caller as a full repair.
- Pandas-100 pct_change wrongly deduplicates already-positionally-computed results
  when freq=None, then broadcasts retained results over duplicate labels. Pandas-104
  quantile confuses integer level names with positional reordering arguments.
  Pandas-110 categorical slices take a positional shortcut in .loc; Pandas-118
  melt coerces mixed label types during NumPy flattening; Pandas-11 duplicate
  concat keys produce non-scalar get_loc results where integer codes are required.
  These are distinct label/position contracts, not independent counts inferred
  merely from the common category.
- Pandas-102 extension-dtype ndarray construction fails the established per-column
  vector shape contract. Pandas-105 transpose, Pandas-107 appended Series rows and
  Pandas-116 merge-key extraction lose semantic extension/timezone dtype. Pandas-119
  margins can truncate a fractional grand mean through forced integer casting,
  changing values rather than presentation alone. Fixed transpose's
  dict(zip(self.index, new_values)) can collapse duplicate source labels; its
  unique-label regression does not establish general fixed-version correctness.
- Pandas-10 putmask omits full-length ExtensionArray filtering for a partial mask;
  Pandas-113 nullable-integer comparisons require array/NotImplemented handling
  instead of scalar fallback; Pandas-117 missing-value dispatch omits extension
  arrays. Pandas-106 invalid datetime-index drop raises an inappropriate exception
  because a non-datetime target lacks the assumed representation. Pandas-115 feeds
  unsorted reference positions to np.interp despite its increasing-x precondition;
  reference x and y must be sorted together without reordering requested output.
- Pandas-111 base Index._convert_scalar_indexer is proposed for exclusion: removing
  return before an always-raising helper does not change matching-version
  behaviour. The categorical subclass .loc delegation is the actual supported
  same-commit repair. Keep the original pair and split pending researcher decision.
  Pandas-114 Index.get_value remains ambiguous: retained test forces __array__ to
  fail and demonstrates avoided conversion, not a concrete old accepted-operation
  failure. Pandas-123 generic Index constructor remains ambiguous compatibility
  plumbing: dropping an integer dtype prevents failure under newly strict numeric
  constructor validation; direct numeric-index regressions do not establish a
  pre-existing failure of the selected fallback.
- Pandas-120 count, nunique and size omit required unobserved categorical output
  combinations under observed=False. Coordinated reindexing adds zero-valued
  combinations. Confirm the pre-existing Series contract rather than assume every
  newly advertised aggregation behaviour was previously promised. The shared
  _reindex_output helper remains ambiguous: its new optional fill_value supports
  those consumers, which previously bypassed it; default NaN remains appropriate
  for existing non-count aggregates. All four stay in one mechanical family.
- Sydent's character allowlist has no secret-length bound; the new 255-character
  limit addresses field-size availability, not catastrophic regex backtracking.
  Starlette multipart constructor, callback and parser share one count-limit root:
  old parser allocates parts without bounds, while coordinated callback counters
  enforce finite defaults. Constructor support is contextual configuration-to-sink
  evidence; researcher must apply a consistent repair-component eligibility rule
  across this and ambiguous helpers, not equate every changed initializer with a
  local vulnerability. Synapse response readers require coordinated finite caller
  caps; default max_size=None remains unbounded, and chunk-before-check handling
  does not prove an exact peak-memory limit. Its discard-body sibling can retain
  one chunk even with zero cap. Strict malformed-text decoding in the CLI case
  establishes bounded conversion failure, not process-wide server denial of service.
- urllib3's selected 303 branch changes method to GET but retains body in recursive
  request arguments; explicitly clearing body repairs that disclosure mechanism.
  Broader advisory 301/302 wording is not evidence for this selected branch.
  yt-dlp Generic forwards smuggled internal proxy controls through arbitrary
  http_headers, extending the earlier Vimeo consumer evidence under the same root.
  Nova API producer and firewall consumer disagree about protocol case: mixed-case
  stored protocols skip lowercase-only port/type restrictions. Consumer normalization
  repairs existing records; unconditional .lower() still needs a non-null protocol
  contract. API/consumer/backport examples are one policy family.
- Zulip's delegated bot administrator may not be a realm administrator, permitting
  improper bot-role promotion; a separate stream existence/autosubscribe path
  improperly joins invite-only resources despite existing realm binding. Sentry's
  artifact download checks route-project permission but retrieves a globally
  identified File without ownership binding. New artifact bundles use project
  membership, whereas release files use organization membership; do not describe
  both as same-project isolation. Typed identifiers require matching callers and
  malformed split input can still fail. Keep with the earlier debug endpoint under
  the same CVE/GHSA/PYSEC family.
- authentik PKCE verification is incorrectly gated by submitted code_verifier rather
  than stored challenge; omitting verifier bypasses proof for a challenged code,
  but a valid unexpired code/provider/redirect is still required. Password-change
  guess throttling counts current-password failures per session and invalidates it
  at five; the old helper already checks current password, so this is neither
  missing reauthentication nor a global timed account lockout.
- Shuup extra-view dispatch has a concrete reflected HTML response sink, unlike
  generic message extraction siblings. The selected invalid-command error case
  remains ambiguous because AJAX JSON or a rethrown exception needs an actual
  unsafe frontend/middleware sink. Notebook Jinja defaults omit autoescaping but
  explicit environment options/settings can override the fix. Nautobot renderer
  removes implicit SafeString status for user-authored output; matching escaping
  consumers and pinned django-jinja/string semantics are essential. Old unsafe
  string-format/mark_safe consumers remain unsafe if only this helper changes.
- Two Spirit like/delete handlers require authenticated successful non-AJAX POST
  branches before unchecked next redirects; ownership and form checks remain.
  Staff switch-user redirects also occur on denied/missing-user branches without
  a successful switch. pyLoad validates a normalized joined URL but returns raw
  next/referrer to a redirect sink, allowing parser/browser disagreement; the new
  endpoint-name policy needs matching fallback callers. Pin actual framework and
  browser normalization before approving effective exploitability. Nova image
  manifest download permits lower-trust filenames to select unconfined local
  staging paths; basename limits that local target but is not a race/symlink proof.
- Inspection used hash-verified before/after snapshots, retained diffs/advisories
  and inert read-only SQLite/AST context. Supplemental web context recorded in
  individual ledger evidence still needs retention/hash pinning before approval.
  No dataset function, fixture, template, configuration, regex, payload, network
  request or example command was executed. No training or evaluation performed.
  Protected original inputs and canonical pairs/splits remain unchanged.
- Resume at HaPy-Bug:bugs-in-py_pandas-123:0:pandas/core/indexes/numeric.py:NumericIndex.__new__,
  followed by CVEfixes:48590208344136:28955515216088. The next 50-candidate
  checkpoint is 394 reviews. Training review, taxonomy consolidation, unresolved
  eligibility and issue-independence reconciliation remain before the first
  researcher approval stage; validation/test adjudication waits for protocol freeze.

### Sixteenth batch: 344 to 394 provisional training reviews (2026-10-24)

- Completed 50 further queued training candidates: 39 assistant-supported, ten
  ambiguous and one proposed exclusion, across 15 repository identities and 30
  mechanical families with supported assessments in this batch. Overall: 394/742
  training pairs reviewed, 273 supported, 112 ambiguous and nine proposed
  exclusions; 348 remain. The ledger contains 396 events including earlier
  revisions. Reviewed IDs equal exactly the first 394 deterministic queue IDs;
  all researcher statuses remain pending. The 212 reviewed mechanical families
  and 177 containing supported assessments are not approved independent counts.
- Training-only draft taxonomy advanced v0.29 to v0.32, adding four definitions
  (71 to 75): v0.30 SEC-SECRET-COMPARISON-TIMING; v0.31
  SEC-BUFFER-COPY-CAPACITY; v0.32 CORR-METADATA-PRESERVATION and
  SEC-TEMPLATE-SOURCE-INJECTION. Existing definitions were not broadened.
  Consolidation must distinguish ordinary metadata loss, normalization, caller
  context and dtype preservation; these draft labels are not final evaluation
  categories. Correctness assignments retain pending non-security screening.
- Pandas-123 NumericIndex actually omits invalid explicit dtype validation,
  unlike its previous generic-Index sibling's compatibility adjustment.
  Pandas-126 append indexes other[0] on an admitted empty list; guarded handling
  preserves an equal but distinct frame. Pandas-12 correlation and covariance
  convert nullable integers through object arrays containing pd.NA; column-aware
  float conversion before NumPy extraction supplies required NaN representation.
  Correlation/covariance share one family, not separate independent null defects.
- Pandas-131 constructor compresses categorical datetimes to unique categories;
  method delegates consequently lose duplicate values. Full-value conversion
  repairs that path. Property delegate already expands old category results by
  original codes; removing expansion coordinates the new producer and remains
  ambiguous without an old property-local failure. Pandas-132 nanvar fails to
  reject unsupported timedelta variance. nanstd normalization preserves allowed
  timedelta standard deviation under the newly strict helper and remains
  ambiguous repair-only compatibility rather than inheriting the variance defect.
- Pandas-133 named axes bypass numeric interpolation branches and use unassigned
  ax; early normalization admits existing aliases. Pandas-135 extension group
  aggregation fails to recover expected fast-path ndarray TypeError into its
  existing Python path. Message-substring recovery is not perfect discrimination
  of callback errors. Pandas-136 tolerance validation accepts only int64 instead
  of all supported integer widths/signs; numerical and positivity checks remain.
- Pandas-139 drops group index name during categorical reconstruction, affecting
  reset_index column identity, not just display. New structural regression lacks
  the categorical cast, so named categorical index expectations and the selected
  constructor provide stronger branch evidence. Pandas-140 loops by column
  position but uses label-sensitive dtypes[idx]; iloc preserves correspondence.
- Pandas-13 consolidates two helpers: the selected old normal-mode helper already
  handles extension arrays, while the deleted infinity-mode helper does not.
  Combined helper pair remains ambiguous due to this old/new mapping. Normal-mode
  _isna_new is proposed for exclusion: explicit old=False is default-equivalent.
  Infinity-mode _isna_old has a concrete broken consumer and is provisionally
  supported with coordinated extension-aware helper. These are one family, not
  three independent missing-value defects. Preserve canonical records and splits.
- Pandas-141 decreasing-range reversal assumes excluded stop is phase-aligned;
  actual reversed range corrects wrong membership/positions. Pandas-143 separately
  omits limit in general delegation, causing excessive forward fills. Its after
  function hash equals Pandas-141 before hash, so record successive-version
  lineage and do not treat family IDs as proof of independence. Its after still
  contains the decreasing-range defect, reinforcing mechanism-scoped negatives.
- Pandas-144 bar ticks overwrite an already-supported explicit xticks setting
  with defaults. Existing constructor/common subplot processing and coordinate
  regression support ignored-configuration mechanism, but chart-presentation
  task eligibility needs a researcher decision consistent with formatter cases.
  Pandas-145 timedelta NaT scalar extraction loses required timedelta identity;
  dtype-specific array extraction repairs that dispatch without general lossy
  extension conversion. Pandas-148 empty apply returns fixed NaN instead of actual
  empty reduction identity/count. Matching constructor already curries args/kwargs,
  supporting removal of duplicate forwarding; bundled mechanisms need reconciliation
  rather than independently counting every line change. New inferred callback
  evaluation can occur twice; no purity or side-effect equivalence is claimed.
- Pandas-146 direct equivalence helper should recover expected tz-awareness
  mismatch as False, not raise; default branch also needs coordinated Cython
  comparator change. Index.equals already catches that failure and returns False;
  removing its broad catch lacks an established old required-propagation failure,
  so remains ambiguous. Pandas-147 timezone constructor must check None after
  truthy string normalization, not only in the original elif chain. Factory catch
  narrowing/chaining remains ambiguous: invalid unit/timezone errors were already
  TypeError, and new invalid-dateutil regression depends on constructor's guard.
- Oppia compares reconstructed CSRF token using ordinary equality; compare_digest
  repairs the conditional timing primitive under coordinated nonce/SHA256 format.
  No practical remote timing oracle was reproduced. Advisory's claimed one-second
  limit conflicts with simply inferring from issuance frequency: old verifier
  recomputes using submitted issued_on plus an age check. Pin runtime, request
  exposure, stable comparison window and future timestamp handling before approval.
- DRF long comma-separated headers are joined into HTML and marked safe without
  escaping original text; selected filter has concrete unsafe composition.
  Lower-trust header producer/template sink and SafeString semantics still need
  pinning. Different DRF linkifier remains ambiguous: old ordinary-input branches
  already escape when autoescape=True; final mark_safe principally avoids double
  escaping under enabled templates. Retained autoescape-off regression deliberately
  keeps markup, so broad default-template XSS advisory does not prove this selected
  function corrects an old unsafe-text path. Shuup EditorView unknown command is
  placed in Problem exception text; actual unescaped middleware/frontend sink
  remains missing, consistent with earlier generic-error siblings.
- Saleor nested/outer user-order resolver filters drafts but fails to require
  ownership for non-managers. Root.id loader and new root/context equality gate
  support scoped authorization mechanism, conditional on reachable user roots and
  app/user permissions. Source overlap annotations preserve one representation
  decision and one family. django-s3file middleware accepts arbitrary bucket keys
  as uploaded files; signed upload-folder parent checks bind selection to intended
  folder, with matched form signature producer. Existing AWS_LOCATION already
  limits storage scope; this is not unrestricted host-path traversal. New helper
  debug prints expose paths and generated signatures to stdout, so no generally
  clean after-code claim. Signature secrecy/folder uniqueness/view permissions
  and downstream file move/publication remain explicit prerequisites.
- Vyper concat allocates logical length but byte-offset copies can write full
  32-byte words into neighbouring EVM memory. Extra capacity covers primitive
  padding while return type retains logical length. This is generated contract
  memory corruption, not Python-host buffer overflow; actual length/layout and
  live-neighbour preconditions matter. Supplemental core.py states rounded writes;
  allocator bytes/layout and introducing-copy lineage still require pinning.
- yt-dlp native redirect forwards ordinary Cookie without scope regeneration;
  new title-case removal fixes that and entity-header case matching. Different
  base downloader wrapper filters Cookie before real_download, requiring matching
  native/external cookiejar handling. Redirect/fragment paths share one disclosed
  family despite separate commits; Authorization and every external tool are not
  automatically covered. LangChain SQL result wrapper applies unrestricted eval
  to returned cells through _try_eval; exception handling cannot undo side effects.
  Returning raw result removes that evaluation but changes representation and
  does not repair arbitrary SQL authority or establish return-type compatibility.
- psiTurk consent/advertisement pass raw query mode into insert_mode, which splices
  it into trusted HTML before template evaluation. Fixed helper emits a constant
  placeholder and callers bind mode as data. Three selected functions share one
  source/data root; no sandbox or arbitrary host-execution proof is implied.
  Advertisement requires allowed browser/IDs and suitable participant-state branch;
  completed-state render_template branch differs. Peering Manager's unrestricted
  user-template renderer changes to sandbox and docs warn about third-party code,
  but actual writer/caller permission and context-capability boundary remains
  untraced. Keep ambiguous; custom filters/extensions and traceback return also
  prevent broad sandbox-clean claims.
- Two Spirit poll views join existing redirect family. Owner close/open is POST
  but reads next from GET; authenticated vote redirects on both valid and invalid
  POST forms, while anonymous branch uses poll-generated login destination. rdiffweb
  mutating-method Origin prefix accepts a different authority sharing base prefix;
  exact equality repairs supplied-origin case. Origin absence still allowed and
  SameSite/browser/base/proxy semantics bound effective CSRF consequences. This is
  distinct from credentialed CORS response matching.
- Ansible zone fetch/put host-copy follows zone-tree symlinks despite lexical root
  prefix; zlogin dd resolves within zone. Same jail/zone/chroot family as earlier
  candidates. Unquoted shell path interpolation and fetch's single-chunk iteration
  remain limitations; do not claim generally correct/safe after transfer. Radicale
  maintenance save and directory creation supply actual outside-root Windows write
  consumers with checked pathutils translation after fix. is_node and last_modified
  remain ambiguous without request/classification or observable metadata-security
  consequences. Same earlier Radicale CVE/fix family; no symlink/race guarantee.
- Supplemental inert web text used this batch, not retained/hash-locked inputs:
  https://raw.githubusercontent.com/vyperlang/vyper/55e18f6d128b2da8986adbbcccf1cd59a4b9ad6f/vyper/codegen/core.py
  and https://github.com/peering-manager/peering-manager/commit/8a865fb596c11ad7caf45aef317d8fcbce7f85ff.patch.
  Retain/pin them and prior Spirit helper before approval. A guessed Peering
  Manager models.py URL returned 404 and supplies no caller evidence. Inspection
  otherwise used verified snapshots, retained diffs/advisories and read-only
  SQLite/AST. No dataset functions, callbacks, reducers, templates, configurations,
  regexes, payloads, requests, filesystem operations from examples or tests were
  executed. No training/evaluation occurred; 45 original protected inputs remain
  unchanged. Adjudication context is not silently added to model inputs.
- Resume at HaPy-Bug:bugs-in-py_pandas-149:0:pandas/io/parquet.py:FastParquetImpl.write,
  followed by CVEfixes:7561542198959:193930065357334. Next 50-candidate checkpoint:
  444 reviews. First researcher approval stage is not yet ready: finish training
  review, consolidate taxonomy, reconcile unresolved eligibility/context and issue
  independence, then verify/freeze before validation/test adjudication.

### Seventeenth batch: 394 to 444 provisional training reviews (2026-10-24)

- Completed 50 further training candidates: 38 assistant-supported, 11 ambiguous
  and one proposed exclusion, across 15 repository identities and 30 mechanical
  families with supported assessments in this batch. Overall: 444/742 training
  pairs reviewed, 311 supported, 123 ambiguous and ten proposed exclusions;
  298 training pairs remain. The ledger contains 446 events including historical
  revisions. Reviewed IDs equal exactly the first 444 deterministic queue IDs;
  all researcher statuses remain pending. The 243 reviewed mechanical families
  and 206 containing supported assessments are not approved independent counts.
- Training-only draft taxonomy advanced v0.32 to v0.35 (75 to 82 categories).
  v0.33 adds CORR-TEXT-CAPACITY and SEC-AUTHENTICATION-ID-COLLATION;
  v0.34 adds CORR-ARITHMETIC-ZERO-SEMANTICS and SEC-TOKEN-URI-LOGGING;
  v0.35 adds CORR-MASK-TARGET-PREDICATE, CORR-OPTION-PROPAGATION and
  SEC-TOKEN-CHAINING-POLICY. No held-out evidence or model predictions informed
  these definitions. Consolidate the growing leaf taxonomy before freeze,
  including option/context/default precedence, dtype/metadata, scalar/vector
  predicates, input mutability and arithmetic dispatch. Supported correctness
  mechanisms retain pending non-security/task-eligibility screening.
- Pandas-149 cloud write branch covers S3 but omits existing GCS support; generic
  lookup opens a nonexistent destination in read mode before writing. Retained
  new-file regression rejects non-write mock opens, supporting wb/open_with for
  GCS. Pandas-150 strict object equivalence tests array-valued inequality as a
  scalar truth value; np.any reduces nested-row/element mismatch. Testing helper's
  removed broad catch is coordinated, not another independent equality issue.
- Pandas-151 scalar strings go directly to np.result_type, whose dtype-like
  argument semantics do not implement ordinary string value assignment. Converting
  against current ndarray dtype supports valid strings and required integer-string
  rejection instead of broad promotion. No generally lossless casting guarantee.
  Pandas-152 explicitly admits tuple input but list-plus-tuple assembly fails;
  list.extend repairs tuple-of-Series assembly without changing concat options.
- Pandas-153 infers fixed Unicode width before inserting na_rep, truncating a
  longer null marker. Retained nullable-Int64/mynull regression is stronger than
  loose release-note wording about shorter na_rep. New allocation from marker
  width repairs the evidenced null representation but can truncate longer original
  nonmissing values; require mixed-value/short/empty-marker review and scoped
  negatives, not universal lossless CSV claims. New word_len helper is coordinated.
- Pandas-154 grouped shift/ffill/bfill obtain generic NumPy obj.values, losing
  timezone-bearing dtype before indexed reconstruction. Manager internal values
  preserve metadata through take/mask/preprocessing; operations share one family.
  Unchanged post_processing/pre_processing validation typo is not certified clean.
  Pandas-155 omitted-on rolling always selects row index even for axis=1 datetime
  columns; axis-aware selection repairs the existing window coordinate contract.
- Pandas-156 column combination forces complex scalar through float, rejecting
  or losing imaginary data depending on historical scalar/runtime semantics.
  Forwarding original scalar is supported by explicit dense/sparse arithmetic
  regression. Row combination's raw-values-to-Series dispatch remains ambiguous:
  old selected function does not force float and new regression explicitly targets
  column sibling. Shared fix/release wording is not old row-path failure proof.
- Pandas-157 temporal tolerance checks omit timedelta keys, while pd.Timedelta
  tolerance is already supported by contract. Any-datetimelike predicate fixes the
  missing case; native datetime.timedelta remains explicitly xfailed. Record
  successive-function lineage with earlier Pandas-136 integer-tolerance fix;
  remaining int64-only restriction demonstrates mechanism-specific negatives.
  Pandas-158 scalar/listlike classification misroutes accepted custom non-callable,
  non-mapping name objects into remapping. Mapper-first dispatch preserves name
  identity for inplace and returned Series, as constructor contract requires.
- Pandas-159 raw-array reverse floor division omits operation-specific zero-result
  normalization, yielding wrong NaN versus Inf under aligned fill_value arithmetic.
  Retained numerical regression establishes more than warning suppression; errstate
  alone is not a correctness fix. Pin dispatch_fill_zeros, function direction and
  original versus filled operand semantics before approval. Pandas-160 large-input
  numexpr eligibility treats Series.dtypes as per-column Series and invokes missing
  value_counts. Dimension-aware frame/Series handling repairs valid-input failure,
  not mere speed. Axis=1 floor division remains explicitly xfailed.
- Pandas-15 Index frequency override differs from backing array frequency and
  fails required pickle roundtrip after clear. Matching array view plus _simple_new
  stores frequency in reconstructed data and preserves name. Array helper itself
  deliberately mutates self under old documented contract; its new view contract
  coordinates newly calling Index wrapper, with no old helper-local alias failure
  established. Keep array pair ambiguous and one family. No pickle was executed.
- Pandas-161 Series fillna selects nonmissing replacement codes rather than missing
  target positions, overwriting valid originals. Target -1 mask repairs selection;
  unchanged self._codes aliasing still needs caller-copy review. Pandas-162 label
  selection/drop of margins mishandles hierarchical axes; positional final margins
  plus full-axis restoration preserve expected MultiIndex crosstab normalization.
  Requires producer's last-margin ordering; new substring/name guard is not general
  validation of arbitrary label types. Pandas-163 unconditional masked infinity
  assignment fails even on read-only input with no infinities. Guarded allocating
  where avoids that write; regression explicitly marks backing array read-only.
- Pandas-165 add/sub defer to Series/DataFrame but omit higher-priority Index,
  returning wrong container/metadata. Early NotImplemented permits matched Index
  reflected dispatch. Reverse subtraction's datetime-only gate also omits timezone
  dtype, reaching invalid reversed timedelta-minus-datetime fallback; widened gate
  restores valid datetime-minus-timedelta. Public reflected route and wrapping must
  be pinned; three selected functions share one family, not three approved issues.
- Pandas-166 list join unique-index concat path drops sort, unlike direct-frame
  branch. Although release note stresses FutureWarning, retained regression checks
  functional unsorted index order for sort=False, supporting option-propagation
  mechanism. Duplicate-index iterative merge still omits sort. Pandas-168 computes
  requested axis but omits it from ambiguity/level-reference helper calls; defaults
  use row context and reject named column levels for axis=1. Forwarding axis repairs
  flat/MultiIndex regression; unchanged index-name/item branches are not certified.
- Pandas-167 two selected capability-predicate substitutions remain ambiguous.
  Actual new regression is flat DatetimeIndex loc year,column, fixed in separate
  _is_scalar_access gate. MultiIndex-only timestamp match helper cannot establish
  that failure; bracket-getitem sliceability helper likewise has no demonstrated
  failing old path. Need concrete old/new predicate divergence and reachable local
  defect, rather than inheriting scalar-access failure from the shared commit.
- Radicale is_leaf and children join prior Windows path family. Classification or
  directory enumeration may escape root, but public metadata/content/permission
  consequence remains untraced; keep ambiguous consistently with earlier metadata
  siblings. Properties path has concrete JSON open read/write consumers and text
  returns complete content; both provisionally support confinement defect. Delete
  removes unsafe target and properties; consequence is deletion, not verbatim
  advisory content read. New checked component translation must match every caller;
  no symlink/race or whole-backend authorization guarantee. One existing family.
- ihatemoney get filters unrelated Project.id instead of Person.project_id,
  allowing authenticated project member to obtain another project's person for
  actual API/web mutation; DELETE deactivates, not hard-deletes. Retained advisory
  explicitly says get_by_name is unused and non-exploitable despite same faulty
  filter and possible MultipleResultsFound. Propose selected get_by_name exclusion
  from security subset; preserve canonical ID/split and do not automatically relabel
  as non-security. New project creation eases credentials, not absence of required
  authentication. Both remain one mechanical fix family.
- social-app-django database get may conflate distinct case-sensitive external
  uids under MySQL/MariaDB collation. Filtering candidates then exact Python uid
  equality removes that collision, conditional on provider identity/schema policy;
  not general case normalization or every database's behaviour. Invenio publish
  checks permission without draft context; retained advisory pins RecordOwners(None)
  to any authenticated user. Resolve then record=draft restores target ownership.
  Requires known draft ID and validation success; not arbitrary data editing or
  restricted-to-public conversion.
- markdown-it smartquotes assertion removal remains ambiguous: typographer must be
  enabled and quoted inline token must acquire children=None from lower-trust text.
  Known nested-image render failure does not establish that core inline producer;
  retained fixture diff adds print, not selected-path null regression. MJML parse
  formatter=None converts escaped text entities into active component content;
  default formatter preserves text boundary under matched BeautifulSoup/component
  semantics. Outer applyAttributes and nested parse overlap annotations identify one
  representation/family. Later htmlAttributes decode_contents(formatter=None),
  includes and client policies prevent broad HTML/email sanitization claims.
- Mayan jstree_data raw label becomes JSON-like text; actual joined template and
  jsTree HTML/text policy remain missing. HTML escaping is not general JS/JSON
  encoding, so selected XSS/effective repair stays ambiguous. Nautobot list error
  uses mark_safe but standard ErrorDict/ErrorList may already escape/mark safe;
  format_html honours SafeData too. Need actual unsafe error producer. Generic
  import success composition has possible unsafe object text/link, but concrete
  admitted model/form/__str__/URL and shared message template remain unpinned.
  Both Nautobot pairs ambiguous; broad advisory examples do not settle them.
- Swauth live candidate GET and new-token PUT expose raw bearer in logged Swift
  storage URI; validator and local non-S3 cache-miss group lookup also expose it.
  Matched SHA512-derived object names, issuer/readers and migration remove raw
  bearer from that backend path, not inbound/remote validation URLs, headers,
  metadata, memcache or historical logs. User-deletion DELETE remains ambiguous:
  successful revocation makes logged token unusable; failed-delete/window exposure
  needs evidence rather than inheriting live-GET replay. Four functions one family;
  exact configuration/log reader/validity conditions remain explicit.
- pyLoad session SameSite=None permits accepted ambient cookie on cross-site
  state-changing GET API; Strict restricts delivery. Retained advisory pins admin
  add_user route. Attacker need not authenticate but victim must hold admin session;
  modern browsers may already reject insecure HTTP SameSite=None. Pin actual
  extension/browser/TLS/equivalent controls, not universal CSRF protection or safe
  methods. MLflow unexpected Content-Type is reflected into Flask HTML error string;
  constant allowed-types response removes it. Pin response MIME/CSP/decorator and
  victim-browser custom-header delivery/CORS, not arbitrary signup/auth bypass.
- Sydent authenticated invite ignores returned identity and accepts arbitrary
  claimed sender for token/email substitutions. New account.userId comparison and
  verified-sender field establish authenticated sender binding, conditional on
  updated branded/custom templates. require_auth=False still allows unverified
  invitations; display fields remain user-controlled. Matching sendEmail also
  randomizes multipart boundary, a distinct sibling mechanism. No claim selected
  binding fixes every arbitrary-email/phishing path.
- Keystone successive authenticate versions share CVE-2012-3426/family. First
  rechecks current account-enabled state before token-derived issuance, unlike old
  embedded user and password-only check. Revocation backend may not enumerate old
  tokens; new issue gate does not by itself revoke/directly reject every old token.
  Next patch carries parent's expires instead of obtaining renewed default life.
  First after hash equals next before hash: code is negative for disable-chaining
  but still positive for expiry-chaining. Backend validation/default expiry and
  separate disable/password/expiry mechanisms require explicit issue adjudication,
  not mechanical count inflation. Password error-status change alone is not bypass.
- Horizon request next reaches two successful-login redirect sinks. Absolute-URI
  same-origin comparison restricts foreign scheme/host/port with local fallback;
  pin historical Django/default ports and trusted host/proxy semantics. Retained
  CVE-2012-3540 describes phishing redirect, not token forwarding/session fixation.
- Inspected inert verified before/after snapshots, complete function bodies/diffs,
  retained HaPy commits/regressions/CVE summaries and retained CVE/advisory records;
  read-only SQLite supplied matching changed helpers. No supplemental web evidence
  was fetched in this batch. No dataset functions, operators, callbacks, fixtures,
  templates, configurations, regexes, payloads, request examples, filesystem examples,
  key/hash generation, pickle or tests were executed. No training/evaluation occurred.
  The 45 protected inputs remain unchanged; adjudication context stays outside model
  inputs unless later protocol explicitly defines an identical bounded context.
- Resume at HaPy-Bug:bugs-in-py_pandas-16:0:pandas/core/indexes/datetimelike.py:DatetimeIndexOpsMixin._get_addsub_freq,
  followed by HaPy-Bug:cve_CVE-2012-4406:0:swift/common/memcached.py:MemcacheRing.__init__.
  Next 50-candidate checkpoint: 494 reviews. First researcher approval stage is not
  yet ready: finish training review, consolidate taxonomy and unresolved eligibility,
  reconcile issue independence and verify/freeze before validation/test adjudication.

## 2026-10-24: twentieth batch, 544 to 594 training reviews

- Completed the next 50 deterministic training candidates: **28 assistant-supported**,
  **7 ambiguous**, **15 proposed exclusions**. Totals: **594 / 742** training pairs
  reviewed (**596** append-only ledger events), **413 supported**, **153 ambiguous**,
  **28 proposed exclusions**; **148** training pairs remain. Reviewed IDs equal exactly
  queue positions 0 through 593. All researcher statuses remain pending. Reviewed
  candidates span **327** mechanical fix families; supported candidates span **277**.
  These are not audited independent issue counts or sums of independent categories.
- Training-only draft v0.39 adds four definitions, taking 91 to **95** discovery labels:
  indexer dimensionality validation, token algorithm/flow policy, RSA padding oracle
  and subclass result construction. Earlier definitions retain their meaning/history.
  Consolidate validation, type/representation, option and exception leaves before freeze;
  neither held-out evidence nor model predictions informed these additions.
- Pandas-5 ignores return_indexers=False on the two-MultiIndex branch; correct Index
  versus triple return is a functional contract. Pandas-61 raw extraction catches
  ValueError then returns a multidimensional ndarray where the retained regression
  requires rejection. Pandas-64 validates selected Excel columns but still exports the
  whole frame; reindex passes the actual subset to the writer. Pandas-65 get_handle
  and CParserWrapper omit RawIOBase decoding, including resetting downstream encoding
  without wrapping raw binary input; both functions remain one issue/fix family.
- OpenAPI CVE-2020-15142 List/Union get_type_string additions are compatibility-only
  proposed exclusions, like the previously reviewed Enum helper. group_title fixes a
  casing-regex hyphen range but does not demonstrate selected security sanitization.
  Retain all same-fix functions and shared 15141/15142 lineage for later independence
  review; no CVE-level label is transferred automatically to these selected functions.
- OIDC CVE-2020-26244 _verify_id_token adds rejection of alg=none outside the exact
  code response flow. Consumer.parse_authz adds invocation of client verification
  before returning a present token. Upstream JWS parsing, algorithm registration,
  trusted saved request/state and prior session-update side effects remain contextual.
  Client.verify_id_token forwarding is ambiguous: it enables the new guard's allowed
  code-flow exception rather than independently fixing old wrapper validation.
  Message-level verify_id_token is a proposed security-subset exclusion: its selected
  edit exempts none from token/code-hash calculation and relies on the Client check.
  All four selected functions are one provisional family, not four independent issues.
- Pandas-66 xs boxes stored object-dtype numpy.datetime64 into Timestamp; direct
  extraction preserves type. SingleBlockManager.fast_xs retirement is a proposed
  exclusion: old extraction is not the caller's boxing defect, and new helper
  deliberately raises after caller retirement. Reconcile related pandas-56 lineage.
  Pandas-69 adds valid floating-index integer-label admission; its after hash equals
  pandas-63 before hash. Pandas-63 exception-consistency change remains ambiguous
  because earlier tests expect ValueError and news identifies an API-breaking change.
- tlslite-ng CVE-2020-26263 decrypt supports secret-dependent padding-failure/scan
  exposure. Full scanning plus deterministic implicit rejection changes explicit
  failure behavior, but both patch and advisory disclaim CPython side-channel
  resistance. Do not approve its after-version as constant-time or universally
  oracle-free. Seven selected key-parser/backend/signing/public-operation siblings
  are proposed security-positive exclusions: shared bytes adapters and interface
  migration do not establish the private decrypted-padding mechanism in each one.
  All eight selected functions remain one family; backend/runtime/TLS/API observation
  and the adequacy of mechanism-specific negatives still need adjudication.
- Pandas-6 handles expected PeriodIndex probe ValueError so valid level grouping
  continues. Pandas-70 type-incompatible extension cast-back changes aggregate values;
  scalar-type guard supports categorical count/nunique preservation, not heterogeneous
  or NA-complete behavior (one retained NA regression is explicitly xfailed).
  Pandas-72 constructs a categorical block for exact-match single-row assignment;
  early-return transpose/alias behavior beyond that witness remains unconfirmed.
- Pandas-73 arithmetic dispatcher omits required zero-result normalization, producing
  a floor-division mismatch with columnwise Series operations. Shared mask helper's
  flattening-to-shaped-assignment change remains ambiguous without an isolated old
  layout failure. Same family. Pandas-74 array fast path bypasses explicit frequency
  consistency validation. Pandas-75 exact lookup wrongly admits finer-resolution
  strings; resolution checking fixes witnessed containment. Its sibling get_value
  overflow catch has no supported successful overflow-fallback witness and stays
  ambiguous. Pandas-76 speculative integer cast misses OverflowError and should
  retain unconvertible strings; forced-dtype branches are outside this negative.
- urllib3 CVE-2020-7212 has a proposed mislinked-fix exclusion: selected a74c9cf adds
  _encode_invalid_chars and invalid-character handling, but does not implement the
  advisory-described repeated percent-normalization dedup repair. This added helper
  version lacks that later quadratic normalization loop; do not call it the actual
  vulnerable/fixed pair. Locate/pin correct lineage before any relabeling. By contrast,
  CVE-2021-33503 directly replaces ambiguous many-@ authority regex splitting with
  rpartition plus host/port parsing; it supports existing regex-backtracking category.
- CairoSVG CVE-2021-21236 surrounding RGB/RGBA definitions repair overlapping regex
  repetitions, but selected color function only adds post-match strip. Mark ambiguous
  for function-only pair eligibility: expensive patterns are outside its input and
  post-match stripping is not a pre-match complexity repair. Decide common bounded
  global context or compatibility-component exclusion before approving a negative.
- Synapse CVE-2021-21274 resolver buffers an untrusted .well-known response without
  a cap; the bounded reader/50 KiB limit and dedicated non-retry failure handling
  support the missing-size-bound mechanism. Shared protocol writes each chunk before
  threshold checking, so this is not an exact memory cap. Both get_file siblings
  already forward an enforced max_size before; reader rename/error adaptation is
  proposed for exclusion from the named positive subset. Their after handlers
  construct SynapseError without raising it and may then read unassigned length.
  Preserve this introduced-error concern rather than treating after as generally clean.
- Pandas-77 passes 2D arrays to a 1D vector fallback; flatten/reshape preserves the
  witnessed logical-result shape. Pandas-78 hardcodes Series instead of established
  subclass result constructor; numeric/boolean regressions support class preservation,
  not all metadata propagation. Pandas-79 two consumer catch additions remain ambiguous
  because producer simultaneously changes TypeError to InvalidIndexError: old consumers
  already catch TypeError, so new-interface compatibility is not proof of old defect.
- Synapse CVE-2021-29471 matcher switches from ambiguous repeated wildcard expansion
  to contiguous wildcard-run simplification. Caching does not eliminate match work;
  removed character-class support and separated runs remain scoped. Zope
  CVE-2021-32674 two traversal functions add per-member authorization when fallback
  traversal bypasses security manager policy. Explicit unrestricted mode and '_'
  compatibility remain exceptions. Untrusted template-edit permissions are a deployment
  precondition; advisory extends GHSA-5pr9-v234-jw36, requiring common-lineage review.
- Pandas-7 nearest lookup loses timezone representation via ndarray coercion;
  Index-native arithmetic preserves the witnessed reindex result. Pandas-80 inversion
  loses mixed/extension dtypes through whole-frame coercion; blockwise dispatch plus
  coordinated extension methods repairs witnessed cases. Pandas-82 wrong integer
  missing sentinel conflicts with datetime64 merge-result dtype; typed NaT repairs the
  retained left-merge case. No all-layout/extension/sentinel or copy-safety claim.
- Websockets CVE-2021-33880 built-in password callbacks use ordinary equality;
  compare_digest addresses that secret comparison. Unknown users still return early,
  custom callbacks are unchanged and non-ASCII/type behavior needs review: no uniform
  whole-request timing guarantee. Keep outer/nested representations and backports
  c91b4c2a/dfecbd03 in the same disclosed issue lineage before independent counting.
- Every selected source/function hash/span was reverified, and established refresh
  ran after each appended decision. All 45 protected inputs match the lock/release;
  canonical contents, splits and input lock remain unchanged. Only own audit tooling
  ran; dataset functions/tests/parsers/regexes/templates/callbacks/configuration and
  payloads were never executed. No training/evaluation or paid compute/API work ran.
  Context above is adjudication-only and cannot silently enter model inputs.
- Resume at HaPy-Bug:bugs-in-py_pandas-83:0:pandas/core/indexes/api.py:_get_combined_index,
  followed by HaPy-Bug:cve_CVE-2021-37678:0:tensorflow/python/keras/engine/training.py:Model.to_yaml.
  Next 50-candidate checkpoint: **644** reviews. First researcher approval stage is
  still not ready: finish training review, consolidate taxonomy/eligibility/context,
  reconcile independence and verify/freeze before validation/test adjudication.

### Eighteenth batch: 444 to 494 provisional training reviews (2026-10-24)

- Completed 50 further training candidates: 39 assistant-supported, 11 ambiguous
  and no new proposed exclusions, across five repository identities and 22 mechanical
  families with supported assessments in this batch. Overall: 494/742 training pairs
  reviewed, 350 supported, 134 ambiguous and ten proposed exclusions; 248 training
  pairs remain. The ledger contains 496 events including historical revisions.
  Reviewed IDs equal exactly the first 494 deterministic queue IDs; all researcher
  statuses remain pending. The 269 reviewed mechanical families and 228 containing
  supported assessments are not approved independent issue counts.
- Training-only draft taxonomy advanced v0.35 to v0.37 (82 to 86 categories).
  v0.36 adds CORR-SEMANTIC-TYPE-VALIDATION. v0.37 adds CORR-LOOKUP-VALIDATION,
  CORR-METADATA-INVALIDATION and SEC-CREDENTIAL-DIAGNOSTIC-DISCLOSURE. Existing
  definitions were not broadened. No held-out evidence or predictions informed these
  additions. Consolidate semantic type/dtype, context/normalization, metadata
  preservation/invalidation and diagnostic/redaction leaves before freeze. Supported
  correctness assessments retain pending non-security and task-eligibility screening;
  supported mechanisms do not settle API-transition eligibility automatically.
- Pandas-16 frequency helper assumes Period input implies Period result even when
  subtraction produces all-missing TimedeltaIndex. Result-aware branch returns None;
  enclosing arithmetic wrapper must forward actual result. Retained regression checks
  freq separately from values. Helper and nested wrapper are one coordinated family,
  not independent arithmetic issues or standalone interchangeable snippets.
- Swift CVE-2012-4406 get and get_multi unconditionally unpickle flagged cache bytes.
  Single get checks requested key, while multi-get deserializes VALUE rows before
  requested-key output mapping; neither exception handling nor later mapping undoes
  construction. Supported security boundary remains conditional on hostile cache
  value/response access and process privileges. New readers refuse pickle under
  effective allow_unpickle=False; explicit legacy modes deliberately remain unsafe.
  JSON substitution does not establish cache authenticity or resource safety.
- Swift constructor, middleware initializer and set/set_multi remain ambiguous
  producer/compatibility components. They introduce new policy state/options and JSON
  writing, while the concrete unsafe loads are in readers. No independent old writer
  or constructor-local vulnerability is established by shared patch/CVE. Historical
  middleware compares ConfigParser/string configuration to integer mode constants;
  retain exact Python-2 effective semantics before claiming documented migration
  modes work. Construction-only tests do not establish that policy. Five selected
  MemcacheRing functions plus middleware share one mechanical family.
- Pandas-17 insertion validator lets unsupported nonmissing semantic types fall
  through; Index.insert then .view(int64) can reinterpret compatible NumPy scalar
  bits as temporal labels instead of required TypeError. Exhaustive validation and
  matched scalar unboxing repair that acceptance. Recognized-scalar compatibility
  check moves from caller, not a separately absent overall check. Early string path
  preserves prior object fallback under the stricter validator. Concrete subclass
  unboxing/recognized types remain contextual; both functions are one family.
- Pandas-18 rolling _apply tests normalized integer window for BaseIndexer rather
  than original self.window. New branch forwards indexer.window_size, but witnessed
  skew case was explicitly unsupported by old allowlist and newly enabled in same
  patch. Keep ambiguous pending an affected previously supported operation and exact
  calculate_min_periods semantics. Pandas-22 count/base-count likewise add count to
  support allowlist and remove explicit NotImplemented regression: new routing and
  base assertion are not independently established old supported-path defects.
- Pandas-19 flat MultiIndex list keys are wrapped into nested tuples, bypassing
  ordinary iterable missing-label rejection. Removal restores validator route;
  retained tests distinguish empty requests from missing labels. Pandas-21 non-list
  label containers instead use permissive reindex while equivalent lists use loc.
  Unified loc removes silent missing-value insertion. Both mechanisms are supported,
  but changed formerly permissive tests/API history need explicit eligibility
  reconciliation. Integer positional fallback and nested tuple semantics remain
  distinct, and the two fixes are not automatically one independent issue.
- Pandas-1 nested string-dtype exclusion omits categorical object-kind dtype;
  retained enclosing predicate and categorical regression establish false positive.
  Generic object acceptance remains deliberate. Imported predicates and bounded
  enclosing context must be pinned before function-only claims.
- Pandas-20 month/quarter/year shifts copy input freq into unvalidated result even
  when calendar transformation destroys spacing. Omission invalidates stale metadata;
  retained regression explicitly asserts freq is None. Three offset functions share
  one family. Imported apply_index_wraps was not defined in retained selected file;
  exact wrapper/constructor context remains to pin. Pandas-24 tz_localize similarly
  copies freq across DST transformation; regression establishes invalid inferred
  spacing with shift_forward. New conservative invalidation preserves only explicit
  UTC/nonmissing-singleton/naive-no-op cases, not optimal inference for every offset.
- Glance v1 CVE-2012-4573 deletes/schedules backend data before registry mutation
  enforces target authorization. Generic action policy and readable image metadata
  do not authorize deletion. Registry-first ordering prevents effect before denial;
  regression checks image bytes survive failed DELETE. CVE-2012-5482 repairs same
  ordering in v2 after incomplete v1 fix. Separate mechanical families/CVEs still
  require lineage adjudication. Unchanged v2 builtin id passed instead of image_id,
  rollback, delayed-delete semantics and all-store authorization are not certified.
- Keystone CVE-2012-5571 valid EC2 credentials can issue tenant token after user's
  current tenant roles are removed. New nonempty role gate precedes catalog/token
  creation. Pin metadata backend, downstream no-role privileges, role validity and
  inherited S3 route; this is post-auth membership binding, not passwordless identity
  compromise or repair of unchanged signature fallback.
- Glance CVE-2013-0212 single-tenant location URI includes configured user/key;
  conflict/not-found exceptions propagate it into diagnostics under affected error/log
  audience conditions. Percent quoting does not redact. Constant messages remove
  selected URI sinks, while successful credential-bearing location returns and other
  exceptions remain outside negative scope. Mainline, Folsom and Essex functions
  are one mechanical disclosure family; different bodies, severities, releases and
  nested stream helpers do not multiply issues. Exact Location.get_store_uri wrapper,
  API/log forwarding, effective mode and unauthorized read access remain to pin.
- Glance parse_uri variants directly log raw malformed URI/credential fragments
  at DEBUG or ERROR; omitting live values repairs these validation diagnostics,
  conditional on credential-bearing input and log access. Literal user:pass guidance
  is not a live leak. MultiTenantStore.set_acls and Folsom guarded Store.set_acls
  remain ambiguous: normal multi-tenant producer lacks/clears key and uses token
  outside URI, so single-tenant password disclosure cannot simply transfer to these
  paths. Need actual admitted credential-bearing location or other sensitive boundary.
- Pandas-23 fast temporal intersection loses timezone dtype/freq in empty constructor
  and public-values reconstruction; explicit dtype/freq and internal values preserve
  required representation. Generic/nonanchored paths retain their separate inference
  policy. Pandas-25 ISO calendar uses UTC storage instead of local timestamps near
  year/week/day boundary; local conversion restores actual field values, not merely
  display formatting. Native helper/runtime semantics remain contextual.
- Pandas-26 ordered categorical min/max on nonempty all-missing input filter to empty
  codes then reduce, unlike required NaN. good.any guards empty-after-filter case;
  min/max share one family. Pandas-27 alias lookup overwrites available inferred
  stride-bearing frequency with None; base/stride fallback restores omitted-argument
  conversion as witnessed against explicit 5min. No general alias guarantee.
- Pandas-28 other Index values are mistaken for alignment labels in str.cat; inherited
  caller index restores positional concatenation instead of NaNs. Actual cat alignment
  and missing-mask consumer inspected. Old helper comment/API history still needs
  reconciliation; Series/DataFrame label alignment remains a separate contract.
- Pandas-29 integer interval NaN setter deliberately upcasts under old tests; new
  BUG/API policy rejects dtype change and modifies successful fixtures. Keep ambiguous
  pending prior stable-dtype contract, or a concrete public-values/internal-values
  temporal defect. Unchanged assignment swaps left before right may fail, so source
  comment does not prove atomicity and after-code is not generally clean.
- Pandas-2 scalar setter rejects raw multi-component tuple as too many axes before
  matched At converter can wrap it as one Series label. Reordered arity validation
  plus converter repairs tuple-index/MultiIndex regressions; one-line reordering alone
  against old converter would not. Pandas-30 speculative date inference fails valid
  JSON boolean Series with unhandled TypeError; narrow recovery preserves original
  data through inspected fallback, not blanket error suppression.
- Pandas-31 quantile preprocessor forwards nullable integer/boolean ExtensionArray
  directly to native float-values consumer; to_numpy(float,na_value=NaN) supplies
  omitted representation while original values separately produce missing mask.
  Nested callback, enclosing quantile and consumer inspected; large-integer precision,
  all interpolation and unchanged post-processing validation remain outside guarantee.
- Keystone CVE-2013-2006 options admin_token/LDAP password omit secret metadata used
  by DEBUG configuration diagnostics. register_str forwards new secret=True into
  cfg.StrOpt. Actual versioned dump/masking implementation and unauthorized log-reader
  conditions remain to retain; selected configure is a contextual policy producer,
  not a local log sink. Default ADMIN, other secret options and file permissions
  are not repaired by these markers.
- Pandas-32 binary stream read returns bytes, so unnecessary .encode raises
  AttributeError outside UnicodeEncodeError catch. Retained GCS rationale and binary
  file regression establish supported Python-3 failure. Retaining binary stream
  repairs this representation mismatch; header seek, ownership/closing and arbitrary
  text/nonseekable input remain contextual, not a universal stream guarantee.
- PyMongo CVE-2013-2132 names native _cbsonmodule.c NULL dereference. Selected Python
  _get_object instead raises KeyError for $ref without $id; pop default coordinates
  native repaired DBRef fallback. Complete native/Python diff and regression do not
  prove Python process crash or service availability boundary. Keep unresolved/null
  category pending native-dispatch/fallback, input reachability and exception-consumer
  evidence; do not automatically transfer C defect or relabel correctness/security.
- Inspected inert hash/span-verified before/after source, full selected functions/diffs,
  enclosing helpers/consumers and retained HaPy fixes/regressions/CVE summaries;
  read-only SQLite metadata confirmed available changed files. No supplemental web
  evidence was fetched. No dataset functions, operations, callbacks, configurations,
  templates, regexes, fixtures, request examples, parsers, serialization, hashing,
  database/store operations or tests were executed. No training/evaluation occurred.
  Adjudication context remains outside model inputs unless a later protocol explicitly
  defines identical bounded context. The 45 protected inputs remain unchanged.
- Resume at HaPy-Bug:bugs-in-py_pandas-33:0:pandas/core/arrays/integer.py:IntegerArray._values_for_argsort,
  followed by HaPy-Bug:cve_CVE-2016-10149:0:src/saml2/__init__.py:create_class_from_xml_string.
  Next 50-candidate checkpoint: 544 reviews. First researcher approval stage is not
  yet ready: finish training review, consolidate taxonomy and unresolved eligibility,
  reconcile issue independence and verify/freeze before validation/test adjudication.
### Nineteenth batch: 494 to 544 provisional training reviews (2026-10-24)

- Completed 50 further training candidates: 35 assistant-supported, 12 ambiguous
  and three proposed exclusions, across eight repository identities and 29 reviewed
  mechanical families (24 with supported assessments in this batch). Overall:
  544/742 training pairs reviewed, 385 supported, 146 ambiguous and 13 proposed
  exclusions; 198 training pairs remain. Ledger contains 546 events, including
  historical revisions. Reviewed IDs equal exactly the first 544 deterministic queue
  IDs; every researcher status remains pending. The 298 reviewed mechanical families
  and 252 containing supported assessments are not approved independent issue counts.
- Training-only taxonomy advanced v0.37 to v0.38: 86 to 91 draft categories.
  Five additions: CORR-EMPTY-REDUCTION, CORR-AXIS-POSITION-REMAP,
  SEC-PREDICTABLE-FILE-TARGET, SEC-HTTP-FRAMING-DISAGREEMENT and
  SEC-GENERATED-SOURCE-INJECTION. Existing definitions were not broadened. Consolidate
  empty-input, semantic-type/dtype, coordinate/context and incomplete-case leaves
  using training evidence before freeze. No held-out evidence or predictions defined
  categories. Supported correctness mechanisms retain pending non-security and
  task-eligibility screens; API changes and new features do not automatically qualify.
- Pandas-33 nullable integer sorting helper computes min even for admitted empty data
  with no missing positions to fill. Mask guard avoids empty reduction; retained
  empty value_counts regression establishes result contract. Inherited consumer must
  still be pinned; nonempty sentinel ordering and overflow are outside negative scope.
  Pandas-34 ambiguous-midnight resampling selects DST side explicitly where inference
  fails; historical localization/runtime and policy eligibility remain contextual.
- SAML CVE-2016-10149: six XML entry points parse with standard ElementTree before
  class/tag/SOAP validation. Exception translation after parse cannot prevent expansion
  work. Retained defusedxml EntitiesForbidden/XmlParseError regressions support entity
  rejection, not the advisory's arbitrary-file-read claim for these ElementTree paths
  or separate xmlsec/signature defects. Exact Expat/ElementTree/defusedxml versions,
  runtime limits and lower-trust transport callers remain to pin. Six functions share
  fix-family:ed04d36ee6a0591bdc00; wrappers are not six independent issues.
- Pandas-35 engine callback changes weakref(Index) to weakref(PeriodArray). The native
  PeriodEngine callback/dereference/lifetime contract is unavailable in selected file;
  recreation/is_monotonic regression alone does not locate the defect. Keep ambiguous.
  Pandas-38 unstack adjusts remaining level positions against iteration i rather than
  removed coordinate val; ordered/sequential-unstack regressions support axis-remap
  repair. Empty-list truthiness edit is incidental. Pandas-39 inplace arithmetic needs
  cacher reset before updating a Series whose former parent column was dropped;
  retained regression checks unexpected parent mutation, beyond warning behavior.
- Pandas-3 to_period/to_timestamp replace assert with explicit TypeError. Unsupported
  indexes already fail normally; new tests assert a new exception API, while news
  describes an old AttributeError inconsistent with selected assertion source. Keep
  both ambiguous pending existing consumer contract or concrete optimized-runtime
  functional impact; two methods share one family.
- Keycloak CVE-2017-15111 default predictable /tmp/program.log reaches link-following
  RotatingFileHandler under local permissions/process-identity preconditions. Moving
  default to relative filename removes that shared path, but unchanged configure_logging
  calls os.makedirs on empty dirname for a bare filename. Functioning after-code is
  not certified; hostile CWD, explicit paths and links remain outside negative scope.
  CVE-2017-15112 removes plaintext password argv transport, conditional on process/history
  audiences. New password-file branch references keycloak_admin_password_file rather
  than declared admin_password_file; do not certify file/stdin operation. Password fix
  after hash equals logging fix before hash: review version dependence while retaining
  distinct mechanisms, not automatic issue merging.
- Pandas-40 right-merge order repair forwards how through both factorization stages
  and adds right-oriented labels. Caller omission is supported by row-order regression;
  factorizer is ambiguous because old helper fulfills old interface and does not know
  merge mode. Native join order/prior API contract still need pinning. Pandas-41
  ExtensionBlock.set rebinds values instead of mutating shared array, violating retained
  inplace alias contract; slice assignment coordinates compatible-dtype should_store.
- Confire CVE-2017-16763 changes yaml.load to safe_load, but concrete lower-trust config
  access across privilege boundary is unresolved; ordinary authorized editable config
  is insufficient. Keep ambiguous with affected PyYAML version/discovery trust pending.
  Sydent CVE-2019-11340 forwards raw instead of parsed email address, but selected
  after-code lacks equality rejection promised by commit message. SMTP may normalize
  again. Policy/storage and affected smtplib.sendmail/mail/rcpt/quoteaddr need pinning;
  no approved repaired security negative. CPython CVE-2019-16056 getaddrspec propagates
  empty-domain failure from coordinated getdomain rejection for multi-@ input; security
  consequence needs policy consumer. Reconcile Sydent/parser common-root lineage across
  different mechanical families and stale commit example versus actual regressions.
- Pandas-43 shared-column optimization omits power's null semantics: discarded columns
  can still produce one. Arithmetic wrapper forwards op and predicate excludes pow/rpow;
  both are coordinated, not independent issues. Pandas-44 base/Period lookup sends
  incompatible semantic dtypes into integer backing lookup, permitting raw-storage
  false matches; comparability checks/overrides coordinate repair. Existing no_matches
  and missing array representation for unequal lengths is not certified.
- Waitress CVE-2019-16785 start-line, header-line and end-marker helpers accept bare LF
  differently from a relevant CRLF-only frontend. Strict CRLF/embedded-CR-LF rejection
  repairs witnessed header boundary ambiguity, conditional on deployment and channel
  consumed-byte/pipelining behavior. CVE-2019-16786 parse_header treats TE as one exact
  string, ignores lists/folding and falls back to Content-Length; parsed list/unsupported
  coding rejection repairs that framing disagreement. Same before parser hash and
  fix-family:213a673d664e955ece74 do not settle independent issue identity.
- Both Waitress ChunkedReceiver representations remain ambiguous: maintainer expressly
  doubts chunk-only security impact and TE policy is elsewhere. Earlier after-version
  chunk-end validation needs fragmented-CRLF buffering review; later version differs.
  HTTPRequestParser.received mainly adds completed-header limits and new exception
  translation. Separate preexisting resource-limit bypass needs impact/eligibility
  adjudication; adding cumulative header index to previous byte count may double count
  fragmented input. ErrorTask.execute is a proposed exclusion: before already closes
  connection, edit announces Connection: close consistently, not TE framing repair.
- Waitress CVE-2019-16789 stricter HEADER_FIELD grammar removes permissive colon/strip
  header handling under frontend disagreement conditions. Before hash equals 16786
  fixed parser hash: successive residual/incomplete-fix lineage across mechanical
  families, not automatic independent security issue credit. Exact grammar, deployment
  and connection lifecycle remain contextual. No universal smuggling-negative label.
- Pandas-46 cartesian_product unconditionally coerces Index to ndarray and loses
  timezone-bearing representation; Index repeat/take helper preserves timezone in
  direct and pivot_table regressions. Pandas-48 speculative Int64 aggregate cast-back
  catches ValueError but misses expected TypeError for fractional results; narrow
  recovery retains float result. Pandas-50 categorical comparison masks every missing
  comparison False, including inequality; operation-specific handling restores retained
  missing != contract. Scalar/array-other branches remain outside guarantee.
- Pandas-53 scalar validator rejects valid integer labels in mixed object indexes;
  dtype-based admission restores retained actual-value regression, beyond changed error
  classes. Series strict-label getter removes helper's positional fallback, but old
  validation may mask public paths; pin old reachable caller versus coordinated
  prevention before approval. Both one family. Pandas-55 scalar predicate and extraction
  helper remain ambiguous: regression checks internal predicate, not public value,
  dtype/copy/alias difference. Need distinguish fast-path optimization/enabling helper
  from old functional defect. Pandas-56 separately removes unconditional datetimelike
  boxing that changes stored object type/identity in iat; related cache lineage needs
  reconciliation without automatic merging of distinct commits.
- OpenAPI CVE-2020-15141 title retains path separators/dot segments in project/package
  path producer, reaching build writes and update rmtree outside intended CWD under
  filesystem preconditions. Sanitized kebab-case default addresses title path; explicit
  overrides, links and other generated source contexts remain outside negative scope.
  CVE-2020-15142 Enum values producer forwards raw keys/literals to concrete enum
  template, supporting generated-source injection only with later execution/import.
  New quote helper escapes double quotes only: backslash/newline contexts, duplicate
  checks before sanitization, empty strings and default/value matching remain unresolved.
  DateTimeProperty.get_imports and EnumProperty.get_type_string are proposed exclusions:
  constant import compatibility and new option interface do not establish selected
  preexisting injection defect. Enum initializer remains ambiguous pending actual
  default-validation/reference/template flow. All four 15142 functions one family;
  reconcile overlapping 15141/15142 path/source fixes before issue counts.
- Supplemental source retained as CATEGORY_AUDIT_EVIDENCE_019_ENUM_TEMPLATE.txt:
  https://raw.githubusercontent.com/openapi-generators/openapi-python-client/f7a56aae32cba823a77a84a1f10400799b19c19a/openapi_python_client/templates/enum.pyi
  Retained UTF-8 text SHA256:
  f47c28c06937f64170129f75ca8a4c63d609b65deca4032039e9948a54983d98.
  Scope: exact-commit enum assignment template, showing raw key and double-quoted value
  interpolation; repository owner is a redirect/rename relative to dataset identity.
  This supplemental fingerprint covers this retained text, not the whole upstream
  checkout or licence. It is adjudication evidence, not an added model input or a
  modification to the protected release/input lock.
- Pandas-57 list-like categorical replacement incorrectly uses scalar membership;
  per-entry normalization repairs retained Series list/tuple-to-scalar results. Self
  replacement and all category collisions remain outside guarantee. Pandas-58 nullable
  integer codes coerce to object and falsely fail integer validation; explicit nonmissing
  integer conversion repairs witnessed constructor equivalence. Width/unsigned and NA
  policies remain scoped. Pandas-59 rolling corr passes normalized nanoseconds as fresh
  row-count window; original frequency preserves time units and avoids witnessed wrong
  window/memory failure. Generic-bug origin does not establish non-security eligibility;
  availability impact/native allocation would require separate adjudication.
- Full selected before/after functions, retained fixes/regressions/advisories and
  relevant available helpers/consumers were inspected as inert text/AST, with read-only
  SQLite evidence where applicable. All 50 pair source hashes/spans were reverified.
  No dataset functions, tests, payloads, parsers, regexes, templates, configuration,
  generation/update operations or hooks were executed; no training/evaluation occurred.
  Adjudication evidence remains outside model inputs pending a common bounded-context
  protocol. Protected inputs/splits remain immutable; refresh/check verify audit outputs.
- Resume at HaPy-Bug:bugs-in-py_pandas-5:0:pandas/core/indexes/base.py:Index._join_multi,
  followed by HaPy-Bug:cve_CVE-2020-15142:0:openapi_python_client/parser/properties.py:ListProperty.get_type_string.
  Next 50-candidate checkpoint: 594 reviews. First researcher approval stage is not
  yet ready: finish training review, consolidate taxonomy and unresolved eligibility,
  reconcile issue independence and verify/freeze before validation/test adjudication.

## 2026-10-24: twenty-first batch, 594 to 644 training reviews

- Completed 50 deterministic training candidates: **28 assistant-supported**,
  **19 ambiguous**, **3 proposed exclusions**. Overall: **644 / 742** training pairs,
  **646** append-only ledger events, **441 supported**, **172 ambiguous** and
  **31 proposed exclusions**; **98** training pairs remain. Reviewed IDs equal exactly
  queue positions 0 through 643, with two historical revision events retained. All
  researcher statuses are pending. Reviewed candidates span **352** mechanical fix
  families; supported candidates span **298**. Neither is an independently audited
  issue count. Validation/test adjudication remains unstarted.
- Training-only draft v0.40 adds five definitions, taking 95 to **100** discovery
  labels: credential destination scope, non-reentrant-lock deadlock, content-filter
  early bypass, active image-data-URI policy and subprocess operand option injection.
  Earlier definitions/history are preserved. Consolidation of validation, semantic
  type, dtype, option/context and metadata leaves remains necessary before freeze.
  Definitions derive from selected training mechanisms, not model predictions.
- Pandas-83 concat dispatcher drops its existing copy policy, permitting axis-object
  identity reuse. Support dispatcher option propagation; both helpers add a previously
  absent copy interface and remain ambiguous for standalone old-defect eligibility.
  Index.copy object identity is not deep buffer isolation. One shared fix family.
- TensorFlow CVE-2021-37678 model_from_yaml calls unsafe YAML object constructors
  before layer deserialization; custom_objects does not constrain this first load.
  After unconditionally retires loading, a narrowly mechanism-specific negative whose
  lost functionality requires eligibility adjudication. Model.to_yaml is a proposed
  security-positive exclusion: producer retirement does not demonstrate its own old
  unsafe-load sink. JSON/H5/custom layers are not certified safe by this fix.
- Scrapy CVE-2021-41125 automatically attaches Basic credentials to unrelated request
  destinations. Explicit domain or first-request domain limits future attachment;
  falsey domain deliberately keeps unrestricted mode and existing headers are untouched.
  Pinned url_is_from_any_domain matches lowercase netloc/domain suffix, allowing
  subdomains, not an exact scheme/host/port origin. First-request trust and
  port/userinfo matching remain questions; no live request or credential was used.
- TensorFlow CVE-2021-41213 three lock-allocation functions share a recursive tracing
  deadlock mechanism: caller holds Lock while graph creation invokes Python callback,
  and same-thread recursion reacquires it. Constructor and restored-state pairs require
  consumer context; RLock repairs reacquisition, not unbounded recursion, model safety
  or cross-thread lock ordering. A retained recursive regression expects RecursionError.
  Do not count two tracing layers/state restoration as three independent vulnerabilities.
- Pandas-87 crosstab repairs extra dummy column hierarchy for tuple-named Series.
  Pandas-88 skips inappropriate unstack for columns-only multi-key pivots, but removed
  prior Series-result expectation remains API-history context. Pandas-89 forwards
  fill_value to hierarchical-column unstack; earlier pandas-38 coordinate lineage and
  unchanged remaining level remapping prevent a universal unstack negative.
- Pandas-8 no-match replace early return bypasses conversion after recursive list
  replacement has already cast to object, retaining incorrect dtype. Pandas-90
  read_pickle/to_pickle remain ambiguous: news and versionchanged docs describe new
  URL support, not a demonstrated old supported-path defect. Buffer/ownership history
  needs adjudication; unrestricted pickle.load remains, so no security-clean negative.
- Filtering CVE-2021-41250 any URL triggers an early clean result before prohibited
  tokens are checked. Removing the unrelated-URL bypass repairs configured moderation;
  actual enforcement depends on enabled filters/channel paths. clean_input does not
  remove URLs. This does not establish complete moderation or regex complexity safety.
- Synapse CVE-2021-41281 twelve selected functions remain one provisional family.
  Four remote storage/thumbnail path helpers have supported lower-trust server_name
  propagation through request/download, FileInfo, storage and cached-origin cleanup.
  Original/thumbnail write, legacy read fallback and recursive removal are different
  lifecycle sinks, not automatically independent issues. Random file-ID suffixes limit
  target selection; do not claim attacker-chosen arbitrary full filenames. Federation
  allowlists, successful fetch/thumbnail, existing fallback files and filesystem
  permissions remain conditions. Component/jail checks are lexical, not symlink or
  TOCTOU protection; remote_media_thumbnail_dir has component checks, no jail decorator.
- The other seven local/URL-cache Synapse path helpers remain ambiguous. Unchecked joins
  are structurally visible, but inspected producers use local random or date/random IDs
  and some request paths are database-gated; the remote-origin advisory does not prove
  lower-trust control of these different arguments. Dynamic thumbnail encoder acceptance,
  alternate/legacy ID producers, persisted ID trust and deletion callers need tracing.
  Server-name validator is also ambiguous: its old bracket bypass is visible, but the
  vulnerable media parser did not previously invoke it. Newly added call plus stricter
  syntax does not establish a preexisting selected validator-to-filesystem defect.
- Supplemental evidence is pinned in CATEGORY_AUDIT_EVIDENCE_021_CONTEXT.json, SHA256
  **1f150f0e0247e26f812344ea9a2e353af3fd7483c6e9b6f49ab4dfe88e3c2fea**.
  Synapse fix resolves to 91f2bd0907f1d05af67166846988e49644eb650c, parent
  9f9d82aa846332189e818f51d49daf2335780014. Retained exact-parent media_repository,
  preview_url_resource, media_storage, thumbnail_resource, _base and download_resource
  files show producers/routing/sinks. Scrapy url.py is retained at exact fixing commit
  b01d69a1bf48060daec8f751368622352d8b85a6. Each source has full URL/text/SHA256.
  This separate evidence pin does not alter the protected release/input lock and is
  adjudication-only, not model input or proof of the entire upstream checkout.
- Pandas-91/92 searches reject incompatible semantic operands previously admitted by
  representation coercion. API tightening/changed old expectations need eligibility
  adjudication. Pandas-92 asof has a concrete Period query-name type-loss witness;
  string-slice and resampling wrappers merely adapt intentional internal ordinals to
  the changed typed search interface and remain ambiguous. All four share one family.
- Pandas-93 where checks semantic dtype rather than indiscriminate i8 conversion;
  old aware/naive accepted-test changes remain pending policy history. _round is a
  proposed refactor-only exclusion: removed shared helpers are re-expressed without
  an isolated old rounding failure. Pandas-94 repeat/take remain ambiguous because the
  retained regression fixes shared _shallow_copy frequency handling directly; selected
  old functions already explicitly reset frequency. Shared helper error is not proof
  of two independently defective selected wrappers. Pandas-95 integer comparison also
  changes explicit old coercion expectations, so retain eligibility ambiguity.
- Pandas-96 whole-day business-hour optimization drops custom calendar/holidays by
  using BusinessDay rather than configured CustomBusinessDay. Pandas-97 _union drops
  sort on the fast path; helper adds the new interface and remains ambiguous for
  standalone eligibility. Pandas-98 requested PeriodDtype falls through constructor
  dispatch to object casting; retained Period regression supports preservation, not
  every modified Interval path. Pandas-99 nullable IntegerArray needs native ndarray
  plus missing mask; unit=ns conversion is witnessed, other native mutation/precision
  paths remain scoped. Pandas-9 categorical membership incorrectly conflates semantically
  incompatible missing temporal scalars; dtype-aware admission repairs that witness.
- lxml CVE-2021-43818 exempts any image data URI before malicious-scheme checks,
  including active SVG/XML. New MIME subtype filtering rejects retained XML/SVG forms;
  active execution still depends on later embedding/browser policy. Scheme/image
  regex globals and Cleaner consumer are required context, not complete sanitizer proof.
- Twisted CVE-2022-21712 selected RedirectAgent constructor only adds policy state for
  new cross-origin filtering in _handleRedirect. Keep ambiguous as a coordinated
  constructor component; it is not itself the old header transmission sink. Cookiecutter
  CVE-2022-24065 hg checkout needs -- before lower-trust operand: argv transport alone
  does not prevent option interpretation. Git/repository URL/hooks are outside negative
  scope; mocked argv regressions are not execution reproduction.
- Waitress CVE-2022-24761 header and chunk parsers permissively accept non-RFC numeric
  forms, creating conditional frontend/backend framing disagreement. Added digit/hex
  and extension checks reject retained signed/prefixed/space/malformed cases. Regex $
  versus strict terminal-anchor semantics and error-close lifecycle remain questions;
  no universal RFC/complexity/proxy safety negative. undquote is a proposed exclusion:
  equivalent quoted-string globals move/rename without selected mechanism repair.
  Preserve earlier Waitress framing/incomplete-fix lineage for independence review.
- All selected before/after hashes, archived full-source hashes and reconstructed
  spans were verified before append. Refresh ran after each decision; resumable
  recorder continued byte-identical events after a tool timeout, without duplicate
  revisions. Only own audit tooling and inert source inspection ran; no dataset
  functions/tests/parsers/regexes/templates/configurations/callbacks, payloads, hooks
  or examples were executed. No training/evaluation, paid API or GPU work occurred.
  Canonical records, splits and 45 protected inputs remain locked; full refresh/check
  verifies this checkpoint and reproducible audit outputs after this protocol update.
- Resume at HaPy-Bug:bugs-in-py_pandas-9:0:pandas/core/indexes/category.py:CategoricalIndex.__contains__,
  followed by HaPy-Bug:cve_CVE-2022-24787:0:vyper/codegen/expr.py:Expr.parse_Compare.
  Next 50-candidate checkpoint: **694**. First researcher approval stage is not yet
  ready: complete training review, consolidate taxonomy/eligibility/context, reconcile
  independence and verify/freeze before validation/test adjudication.

## 2026-10-25: twenty-second batch, 644 to 694 training reviews

- Completed 50 deterministic training candidates: **30 assistant-supported**,
  **8 ambiguous**, **12 proposed exclusions**. Overall: **694 / 742** training pairs,
  **696** append-only ledger events, **471 supported**, **180 ambiguous** and
  **43 proposed exclusions**; **48** training pairs remain. Reviewed IDs equal exactly
  queue positions 0 through 693, retaining two historical revision events. All
  researcher statuses remain pending. Reviewed candidates span **377** mechanical
  fix families; supported candidates span **321**. These are not audited independent
  issue counts. Validation/test adjudication remains unstarted.
- Training-only draft v0.41 preserves earlier definitions/history and adds six
  discovery labels, taking 100 to **106**: generated bytestring comparison,
  external ABI return validation, socket lifecycle race, partial-buffer recovery
  replay, bytes/text interface contract and scalar serializer contract. These
  distinguish evidenced mechanisms rather than expanding existing definitions to
  absorb incompatible cases. Consolidate representation/encoding, validation,
  option/context, configuration and metadata leaves before taxonomy freeze; 106
  discovery labels are not 106 promised evaluation categories or independent issues.
- Pandas-9 CategoricalIndex membership has the same incompatible missing-temporal
  scalar shortcut already found in Categorical at position 642. Dtype-aware admission
  repairs the retained false membership; retain both functions in one family.
  Separately pinned is_valid_nat_for_dtype establishes recognized scalar rules,
  without certifying every dtype/hashability/empty categorical path.
- Vyper CVE-2022-24787 short equal-capacity bytestring comparisons load a whole
  backing word without logical length. Dirty padding can make equal values unequal;
  trailing zero bytes can make different values equal. Logical-length hash comparison
  addresses retained witnesses under hash assumptions, not every contract/security
  property. This is Python compiler logic emitting EVM IR, not Python interpreter
  string equality. Initial AST reparsing does not itself prove duplicate runtime
  side effects. keccak256_helper is a proposed exclusion: it already hashes buf+32
  for mload(buf) bytes after ensuring memory and evaluating the pointer once; new
  helpers/cache builder express the same span. Two functions remain one family.
- Scrapy-10 Location handling stops decoding all raw bytes as Latin1 before URL
  normalization. Byte-preserving percent encoding avoids changed Latin1 octets and
  double-encoded UTF8. Retained old tests are revised, so API-history policy remains
  an explicit question. This is destination byte identity, not redirect permission,
  credential stripping or request-body confidentiality. Later source already
  includes scrapy-27's per-request status-policy repair; reconcile successive versions.
- Scrapy-11 gunzip recovery appends an entire retained gzip buffer, replaying consumed
  bytes. CPython 2.7.12 source records unread count separately; suffix recovery
  addresses positive extrasize. **-0 slicing still selects the full buffer**, and
  private attributes/runtime compatibility remain unresolved. Binary fixtures were
  not decompressed. Scrapy-14 recognizes gzip MIME types with charset parameters and
  case variation; its regex word boundary is not complete media-type validation.
- Twisted CVE-2022-24801 headerReceived's broad strip removes non-OWS characters
  before framing interpretation. SP/HTAB-only stripping plus strict decoder consumers
  prevents the evidenced normalization route. Chunk-length state rejects permissive
  int hexadecimal forms and illegal extension characters before consuming state;
  error caller returns 400/disconnects. Extension character allowlist is explicitly
  not complete grammar. Relevant frontend/backend disagreement remains a deployment
  condition; advisory excludes HTTP2 and client parser. No universal smuggling negative.
- Twisted lineReceived remains ambiguous: retained regression changes obs-fold spacing
  but does not isolate an old folded-header-to-desync route beyond companion fixes.
  Standalone fromChunk also remains ambiguous: strict hexadecimal utility behavior is
  real, but inspected server uses _ChunkedTransferDecoder and a vulnerable production
  caller for the utility is not established. Tests alone do not establish that route;
  it still does not support chunk extensions. Keep all four functions one family,
  and reuse framing category without automatically merging distinct projects' issues.
- Scrapy-15 tolerates IDNA UnicodeError for missing/overlong labels while canonicalizing
  other URL components; this does not make retained hostname valid or safe. Scrapy-16
  canonicalizer and _unquotepath preserve nonUTF8 percent octets rather than replacement
  decoding and propagate component encoding. parse_url is ambiguous: conversion is
  equivalent on Python3, while Python2 representation migration supports the larger
  canonicalizer without an isolated selected old failure. The three functions share
  one family; scrapy-15 later repairs the helper introduced by scrapy-16, requiring
  successive-version dependence review rather than automatic independence.
- Scrapy-17 nonstandard status fallback prevents None reaching string conversion,
  supporting the stated retry/description nonfailure contract rather than wording
  alone. Scrapy-18 Latin1 header decode tolerates nonUTF8 disposition octets for
  extension classification; it is not semantic decoding of every legacy filename or
  complete Content-Disposition grammar. Scrapy-1 skips tolerated None allowed-domain
  entries before regex matching; no complete offsite security boundary follows,
  especially for empty/all-invalid host policies and dont_filter paths.
- Vyper CVE-2022-24845 strict _unpack_returndata decoding at external-call time
  addresses complex-expression paths that previously relied on downstream clamps.
  Accurate call.func return type and make_setter emit scalar/dynamic bounds checks
  before use. needs_clamp's JSON_ABI dynamic-size exemption is also removed with
  coordinated ABI tagging. Full commit explicitly names both complex-expression
  validation and JSON dynamic-data bounds; retain **one conservative family** pending
  explicit root-cause adjudication rather than manufacturing issues per function.
  skip_contract_check still disables minimum-size checking; _pack_arguments still
  sizes using contract_sig. No universal offset/buffer/return safety certification.
- Four Vyper siblings are proposed security-positive exclusions: _dynarray_make_setter,
  _get_element_ptr_array and _get_element_ptr_tuplelike only retire enum references
  while preserving surviving encoding behavior; _register_function_args replaces
  equivalent _should_decode with needs_clamp(ABI) and already validates incoming
  calldata. External-call helper is ambiguous as coordinated expr/representation
  plumbing to the repaired unpacker. Tuple type converter is ambiguous for security
  attribution: commit calls its recursion/compiler-panic repair an additional minor
  fix. Do not silently relabel that canonical security pair as general correctness.
- Scrapy-20 robots helper expects text; response.body supplies bytes and fails on
  Python3, while response.text matches the retained TextResponse contract. Plain
  Response.text availability remains outside scope. Scrapy-22 converts accepted
  float/bool/int/datetime scalar leaves before XML text writing; bytes/custom object
  semantics and XML security remain unproven. Scrapy-23 fixes text to base64 then
  text-prefix/byte-credential concatenation; both functions are one family, with
  earlier failure masking the later branch before repair. Scrapy-24 builds CONNECT
  bytes for byte-only transport; retained timeout test is not successful TLS/auth
  reproduction. Former Python3 test ignores/support history remain eligibility
  questions for compatibility cases, not automatic feature or defect decisions.
- Scrapy-25 _get_form passes response URL instead of effective document base, producing
  a wrong relative action target. Effective base context repairs retained different-
  origin base-tag regression. _get_form_url is a proposed redundant-change exclusion:
  pinned lxml 3.4.4 action getter already joins action to base_url, and joining again
  is idempotent on the inspected normal path. Dependency tag is comparison evidence,
  not proof of deployed version; revisit if another supported form contract differs.
  get_base_url's bounded scan and lxml/parsel versions constrain broader negatives.
- Waitress CVE-2022-31015 is a **socket lifecycle race**, distinct from earlier framing
  CVEs. Worker response flushing can synchronously handle_close on disconnected send,
  invalidating a descriptor already collected by the main-loop select path. poll
  catches EINTR, not every invalid-descriptor error. write_soon and high-watermark
  worker caller pass do_close=False; guarded send suppresses worker closure while
  main-loop handle_write retains ownership. These three selected functions have
  supported conditional mechanism evidence, not three independent vulnerabilities.
- Waitress _flush_exception and _flush_some are ambiguous new-interface forwarding
  components: default True preserves old behavior without worker policy selection.
  _flush_some_if_lockable is a proposed exclusion: inspected caller is the main-loop
  path where closure is intended, while worker entries directly use _flush_some.
  Verify any other callers before approval. Flag defaults alone do not fix the race;
  no all-concurrency/cleanup guarantee or race reproduction is claimed. Six selected
  functions remain one family; select/poll/runtime and eventual-close progress matter.
- Scrapy-26 filters default-priority entries out of legacy _BASE composition to
  preserve explicit base replacement and project overrides; changed old expectations
  require backward-compatibility history. Scrapy-27 honors existing per-request status
  list/all policies before redirect. Scrapy-29 normalizes absent hostname only for a
  **reference representation**, explicitly not wire bytes. Its regression requires
  nonfailure, not meaningful HTTP for file URLs. Scrapy-2 handles constructor's
  default unlimited None limit; zero/negative/existing-key eviction are not certified.
- Scrapy-30 uses values rather than Python2-only itervalues for actual command
  discovery on Python3; distinguish selected production failure from separate
  testproc byte fixes. Scrapy-31 header_items remains ambiguous: invalid response
  cookie regression flows through WrappedResponse.get_all in inspected CPython3.4,
  not the selected request-header enumeration. Find a real consumer/adapter contract
  before selected eligibility; replacement decoding is not octet fidelity.
- Scrapy-32 passes canonical self.settings after superclass dict normalization to
  log_scrapy_info; original sparse dict lacks required default keys. Initialization
  failure is functional despite occurring in logging setup. Conversely all five
  selected scrapy-33 functions are proposed diagnostic/refactor-only exclusions:
  migrate contextual Failure to exc_info while preserving work/deferred/signal flow.
  Logger propagation can affect traceback availability, so these may be revisited
  with an established machine-consumed logging contract; no blanket exclusion of
  all logging defects. Retain selected and remaining siblings in one fix family.
- Supplemental text is separately pinned in CATEGORY_AUDIT_EVIDENCE_022_CONTEXT.json,
  SHA256 **7108d5a1d03015dc0c301a7ec2f092d9e348c8373fd6f6d2ac611c33b12d7cfe**.
  Ten source entries retain URL/ref/path/text/SHA256: exact-fix Scrapy conversion,
  sitemap, logging and response-base helpers; Vyper logical-data/IR-cache helpers;
  pandas missing-value validator; versioned CPython 2.7.12 gzip, CPython3.4.3 cookiejar
  and lxml3.4.4 form action. Tags are versioned comparison context, not resolved
  deployed dependencies. Evidence hash/per-source hashes are checked before append;
  the protected release/input lock is unchanged. This is adjudication context only,
  not silently added model input or an entire-checkout attestation.
- Full selected function hashes, archived full-file hashes and reconstructed spans
  were verified before append. Recorder preflight validates exact IDs/prefix/categories,
  source commits, supplemental pin and existing byte-identical events; refresh runs
  after each appended decision. No old review event was overwritten. Only own audit
  tooling and inert text/AST inspection ran; AST parsing warnings are not source
  execution. No dataset functions/tests/parsers/regexes/templates/configurations,
  callbacks, hooks, payloads or examples were executed; no model training/evaluation,
  paid API or GPU work occurred. Full refresh/check after protocol update verifies
  45 protected inputs, immutable canonical splits and reproducible audit outputs.
- Resume at HaPy-Bug:bugs-in-py_scrapy-33:0:scrapy/core/scraper.py:Scraper.handle_spider_error,
  followed by HaPy-Bug:bugs-in-py_scrapy-33:0:scrapy/downloadermiddlewares/robotstxt.py:RobotsTxtMiddleware._logerror.
  The next batch has the final **48** training candidates and ends at **742**;
  do not pad it with held-out cases. First researcher approval stage is not yet
  ready: finish training discovery, consolidate taxonomy/eligibility/context,
  reconcile independence and verify/freeze before validation/test adjudication.

## 2026-10-25: twenty-third batch, 694 to 742 training reviews

- Completed exactly the final **48** training candidates at queue positions
  **694–741**. Training discovery is complete at **742 / 742**, with **744 ledger
  events** including the two historical revisions. No validation/test candidate was
  substituted to fill a fifty-pair batch. Latest provisional totals are **494
  assistant-supported**, **191 ambiguous**, **57 proposed exclusions**. This batch
  contributes **23 supported**, **11 ambiguous**, **14 proposed exclusions**.
- Reviewed training spans **412 mechanical fix families**; supported candidates
  span **343**. These are not independently audited issue counts. All researcher
  statuses remain **pending**; validation **156** and test **154** remain unreviewed.
  Complete discovery does not make provisional mechanisms gold labels, prove
  non-security cleanliness or establish issue independence.
- Draft taxonomy **v0.42 / 113 labels** adds seven training-derived discovery
  definitions, preserving previous meanings/history: CORR-INPUT-GRAMMAR-VALIDATION,
  CORR-URL-NORMALIZATION, CORR-SCALAR-REPRESENTATION-CONTRACT,
  CORR-ERROR-REPORTING-PROTOCOL, CORR-COMMAND-ARGUMENT-REWRITE,
  CORR-RULE-APPLICABILITY and CORR-SHORT-SEQUENCE-ACCESS. These are narrow mechanism
  notes for consolidation, not 113 promised evaluation categories. Existing
  delimiter, context, precedence, empty-input and incomplete-case definitions are
  reused where their inclusion boundaries fit.
- Remaining eight scrapy-33 functions are proposed diagnostic/refactor-only
  exclusions, consistent with positions 689–693. handle_spider_error retains close,
  signal and stats behavior; robots error filtering is unchanged; feed storage,
  media cache/download/waiter flows and returned item/deferred/failure identities
  are retained. Changes move Failure context to standard exc_info after removing
  FailureFormatter. All **thirteen** selected functions belong to one shared fix
  family, including nested signal callback. Revisit if an established functional
  machine-consumed traceback/logging contract is demonstrated; this is not a rule
  that all observability defects are cosmetic.
- Scrapy-34 metaclass is ambiguous: fresh fields overwrites an explicitly declared
  fields mapping and DictItem then rejects its key, but new regressions may establish
  a new declaration feature. Retaining an inherited mapping can also mutate shared
  metadata while scanning Field attributes. Confirm API history and alias isolation
  before an inheritance-wide negative. Scrapy-35 is supported precedence repair:
  populated SPIDER_LOADER_CLASS default previously masks explicit deprecated
  SPIDER_MANAGER_CLASS. Pinned Settings.get/defaults establish that branch; behavior
  when both options are explicitly supplied remains a policy question.
- Scrapy-36 create_instance remains ambiguous: rejecting a None factory result is
  a new documented validation policy, motivated by confusing extension logs. The
  mock establishes that policy, not an old failing valid factory or a functional
  downstream manager consumer. Do not infer a missing invariant solely from the
  helper's name. Scrapy-37 rejects /foo:bar instead of mistaking any colon for a
  scheme. The after substring/data check still is not complete parsed/anchored URL
  grammar, and assignment before validation is unchanged. No destination security
  assurance or universal nonhierarchical-scheme rejection policy follows.
- Scrapy-38 image clickables are supported: ordinary input collection already
  excludes image controls, while clickable selection omits them, dropping the
  retained image name/value entirely. Adding image selection repairs that witness,
  not HTML image-coordinate semantics or arbitrary clickdata XPath construction.
  Scrapy-39 is proposed warning-only exclusion: class-versus-instance method identity
  repairs false deprecation warning on the witnessed runtime; default hook and direct
  branch produce equivalent requests, and genuine overrides are still called.
  Warning-as-error contracts and Python descriptor differences can justify revisiting.
- Scrapy-3 triple-leading-slash redirect is ambiguous: code chooses authority-style
  tolerance by stripping leading slashes and restoring request scheme. Existing
  browser-compatibility policy versus a new interpretation is unresolved; ordinary
  RFC-style resolution need not interpret ///host as a new authority. Scrapy-7 form
  action boundary-space trimming is supported under HTML5 URL-attribute whitespace
  semantics. Read raw action, trim defined boundary whitespace, then join; absent
  action returns base. Versioned lxml action getter already resolves action but
  does not establish the required trimming. Reconcile same-function lineages with
  scrapy-10/27 redirect and scrapy-25 form fixes, not automatic independent counts.
- Scrapy-40 Python exporter preserves native scalar leaves; converters explicitly
  reject boolean/int/float/datetime, so unconditional text conversion aborts its
  advertised native-value export contract. This differs from scrapy-22 XML writer,
  which requires textual scalar conversion: do not merge labels by surface word
  'serializer' without preserving interface direction. Binary dictionary-key rules,
  arbitrary custom values and downstream serializers remain outside the witness.
- Scrapy-4 errback swaps exception type/value in a required sys.exc_info-style tuple.
  Real TextTestResult regression and pinned unittest consumer establish functional
  error-result recording, unlike the logging-filter-only migrations. Nested closure
  context and actual dependency version matter; no callback/formatter was executed.
- Thefuck-11 upstream generator duplicates old explicit upstream option/repository
  when inserting Git's suggested command. Removing old option/operand repairs
  retained cases but mutates cached command tokens and rejoins without shell quoting.
  **Its after function exactly equals thefuck-9 before**: second pop fails on
  terminal -u, and later narrow IndexError recovery repairs that admitted short
  correction input. This is an introduced-regression/successive-fix chain requiring
  dependence adjudication, not independent evidence merely because commits differ.
- Thefuck-12 suppresses no-command rule when which finds existing executable;
  incidental not-found text otherwise yields an inapplicable correction. New code
  loses old nonempty-token guard; aliases/functions and PATH lookup limitations
  remain outside scope. Thefuck-5 similarly rejects successful Bitbucket branch
  output containing set-upstream, avoiding a generator expecting absent git-push
  instruction. More specific substring is not a complete structured-output parser.
- Thefuck-13 checkout applicability, -14 additive Fish alias exclusions, -15 newer-Git
  no-hint pathspec support and -25 prefixed HDFS mkdir correction remain ambiguous
  existing-contract versus expansion/policy changes. For -25, old broad matcher
  already admits prefixed mkdir while anchored generator cannot repair it; this
  mismatch is evidence, but not proof HDFS was supported. For -15 old tests explicitly
  expected no-hint failure not to match. Do not infer all changed tests are bug fixes.
- Thefuck-16 Bash/Zsh templates move alias/encoding/current-alias context directly
  onto the correction subprocess inside substitution. Supported mechanisms are
  conditional on each shell's assignment/export semantics; string assertions are
  not shell reproduction. Thefuck-17 Bash reader is supported caller-context repair:
  a fresh interactive shell cannot represent runtime aliases of invoking shell.
  Its template producer remains ambiguous coordinated new-interface plumbing, and
  Zsh absent-environment fallback needs a supported direct-invocation contract.
  **Thefuck-17 Bash template after exactly equals -16 Bash template before.** Keep
  sibling functions grouped and reconcile the later scope repair explicitly.
- Thefuck-19 force-to-force-with-lease is proposed policy-change exclusion: old
  optional rule explicitly offers unconditional force, and new option reduces
  stale-remote overwrite risk without demonstrating an old violated contract.
  Neither unconditional force harmlessness nor all-lease safety is claimed.
  Thefuck-26 adds all-machine alternatives while preserving targeted first choice;
  untargeted extra space is semantically redundant. Thefuck-28 adds optional column
  templates to code explicitly ignoring columns before; companion parser repairs
  do not establish selected generator defect. Both are proposed feature-only
  exclusions subject to earlier API evidence.
- Thefuck-20 shell-aware tokens preserve quoted/escaped-space archive operands;
  companion destination quoting is a separate component within the same family.
  Archive contents, path confinement and side-effect deletion are not certified.
  Thefuck-21 plain git has no token 1 and should decline rather than raise. Thefuck-22
  legitimate empty correction stream reaches cached[0]; guard repairs realization,
  not direct empty indexing or nonempty deduplication. Thefuck-23 uses closing around
  Python2 shelf, which has close but lacks context-manager methods. Cache location,
  pickle trust, keys and concurrency are not made safe by context compatibility.
- Thefuck-24 selected helpers are proposed exclusions. First-two uniqueness already
  compared script/side_effect while ignoring priority; new equality is equivalent.
  Old dedup dict already keys by that pair and excludes cached first. New filter
  compares **command.script string to cached CorrectedCommand object**, failing the
  intended cached-first exclusion; sorted set construction also does not establish
  required retained-priority behavior. A shared commit title/equality regression does
  not establish a repaired selected pair. Preserve canonical source/labels, record
  residual after error, and reconcile later snapshots rather than silently fixing it.
- Thefuck-29 precedence is supported specifically through existing wrap_settings
  defaults-only contract: decorator defaults formerly overwrite user values. Reverse
  merge preserves explicit values. Direct Settings.update docstring/tests change,
  so other callers expecting replacement still need inventory. Thefuck-2 platform
  PATH splitting uses os.pathsep instead of colon; mocks establish selected component
  grammar, not actual Windows execution or executable-permission checks. Thefuck-31
  puts --staged before filename as Git diff requires; unrestricted replacement does
  not establish arbitrary quoting/argument correctness.
- Thefuck-3 Fish info remains ambiguous, not a blanket diagnostic exclusion. Avoiding
  initialization can prevent real recursion, but affected Fish startup mode/plugin
  and actual hook-to-info call chain are unverified by version-output/argv mock.
  Thefuck-4 equal-sign alias handling and empty/invalid-line recovery are supported;
  trying space before equals can still misparse name=value containing spaces.
  Thefuck-6 generator admits internal apostrophe in diagnostic capture, avoiding
  missing-match IndexError, and escapes that witnessed apostrophe. This is not full
  shell-injection mitigation: greedy diagnostics, other metacharacters and shell
  context need screening. Its matcher sibling already accepted the retained error,
  so narrowed closing-quote suffix remains ambiguous without a separate old false
  match witness. Thefuck-7 handles preceding PHP options under app guard; removal
  of requires_output=False needs actual rule dispatch review beyond direct tests.
- Fifteen supplemental sources are pinned in CATEGORY_AUDIT_EVIDENCE_023_CONTEXT.json,
  SHA256 **6d9584cf0184899a2ea954b1091f58994d5b39c162b87ed99f7eb856aaf0a9b3**:
  exact-fix Scrapy settings/defaults and scalar conversions; Thefuck token/cache,
  substitution, decorator, Git guard, alias environment and logging consumers;
  CPython2.7.10 shelf/closing, CPython3.6.6 unittest result and w3lib1.17 HTML whitespace.
  URLs/ref/path/text/per-source hashes are retained and asserted. Prior batch022 lxml
  pin is reused unchanged. Version tags are comparison context, not proof of deployed
  dependencies. Failed URL lookup wrote no partial pin; protected input lock unchanged.
  Evidence remains adjudication-only, not model input or an entire-checkout attestation.
- Recorder preflight validates all 48 exact IDs/commits, selected hashes, archived
  source hashes/spans, exact existing694 prefix, category IDs, pinned evidence and
  successor hash links. Every decision appends then refreshes; old events remain
  unchanged. Final prefix is all742 training IDs and744 events; all researcher statuses
  pending. Own audit tooling and inert text/AST inspection only: no dataset functions,
  tests, regexes, parsers, templates, callbacks, hooks, payloads or generated commands
  executed; no models trained/evaluated or paid API/GPU work. Checkpoint generation now
  emits a consolidation handoff when training queue is empty rather than an empty
  'next batch' and unusable ID placeholder. Final refresh/check verifies45 protected
  inputs and reproduces generated CSV/checkpoint.

## Consolidation handoff after complete training discovery

**Next stage: training-only consolidation. First researcher approval stage is not
yet ready.** The queue is empty because all training candidates have discovery
reviews, not because eligibility, categories and independent issue identities are
settled. Continue autonomously with the following preparation; notify the researcher
when a coherent approval package is actually ready.

1. **Build a training-derived taxonomy crosswalk.** Read all113 definitions and their
   training evidence; propose parent/leaf consolidation with explicit include/exclude
   boundaries, precedence for overlapping mechanisms and unresolved mappings. Keep
   original discovery labels and dated history; never relabel ledger history in
   place. Initial clusters worth examining are representation/encoding/serialization,
   context/options/configuration, validation/lookup/rule applicability, sequence/empty
   boundaries, metadata/index/shape preservation, credentials/tokens/authorization,
   source/template/shell/SQL injection, protocol parsing and availability mechanisms.
   These are work areas, not approved final categories or a fixed target count.
2. **Resolve eligibility consistently.** Start with191 ambiguous and57 proposed
   exclusions, then reassess supported cases against the same rule. Separate existing
   contract repairs from features, intentional policy revisions, diagnostics/style,
   refactors, shared-fix ancillary changes and residual after-code failures. Require
   explicit non-security screening for generic-bug provenance; preserve genuine
   security ambiguity. Produce proposed experimental subsets retaining canonical
   IDs/splits, with reason and evidence for each decision; no canonical deletion.
3. **Choose a common bounded input protocol.** Inventory functions needing caller,
   closure, helper, dependency/runtime or configuration context. Decide function-only
   eligibility versus an explicitly common deterministic bounded-context condition.
   Do not silently grant any model/static condition adjudication evidence. Keep
   patches, after-code, advisories, issue IDs, labels and answers out of detection
   input, and separate mechanism-local after negatives from universal clean labels.
4. **Reconcile issue and version dependence.** Review412 mechanical training families
   and their cross-links, not just343 supported-family count. Reconcile multiple
   functions/nested spans, CVE aliases, backports/forks, common commits/root causes,
   overlapping sources and introduced regressions. Explicit priority chains include
   thefuck-11→9 and -17→16, sequence -24→22 snapshots, Scrapy URL/form/redirect helpers,
   pandas migration/follow-up fixes and earlier security incomplete-fix/backport
   chains recorded in ledger questions. Preserve conservative grouping until a
   dated adjudication supports a split; repository/provenance groups remain separate
   units. Current tool intentionally cannot create approved independent counts;
   extend records/validation explicitly before claiming such counts.
5. **Prepare a researcher approval package and freeze proposal.** Summarize final
   proposed category definitions/crosswalk, eligibility/context rules, unresolved
   exceptions, candidate/issue/repository units and evidence pins. Verify consistency
   and45 protected input hashes, immutable splits, append-only history and generated
   checkpoints. Request researcher confirmation of this coherent package; do not
   misdescribe provisional reviews as approval. Record accepted changes and a versioned
   freeze before applying taxonomy to validation/test references.
6. **Only after freeze, adjudicate held-out references.** Validation156/test154 remain
   unreviewed. Apply fixed definitions without moving pairs or using held-out support
   to tune taxonomy. Independently count eligible issue groups, report repository
   dependence and flag test categories below30 for descriptive review, not automatic
   exclusion or a claim of inferential power. No model predictions inform reference
   adjudication.

## 2026-10-25: first training-only consolidation proposal, v0.1

- Created CATEGORY_AUDIT_CONSOLIDATION_PLAN.json with **113 discovery leaves mapped
  exactly once to25 proposed reporting parents**, with domain-specific boundaries.
  This is an assistant hierarchy proposal, not25 established evaluation classes or
  a frozen replacement for discovery taxonomy0.42. Original definitions, seeds,
  labels, ledger events and candidate identities are retained.
- CATEGORY_AUDIT_CONSOLIDATE.py builds and checks six deterministic artifacts:
  CATEGORY_AUDIT_CONSOLIDATION_CROSSWALK.json,
  CATEGORY_AUDIT_CONSOLIDATION_REVIEW_QUEUE.jsonl,
  CATEGORY_AUDIT_CONSOLIDATION_DEPENDENCE.json,
  CATEGORY_AUDIT_CONSOLIDATION_COUNTS.csv,
  CATEGORY_AUDIT_CONSOLIDATION_REPORT.md and
  CATEGORY_AUDIT_CONSOLIDATION_MANIFEST.json. All substantive derivation uses the
  training projection; protected held-out bytes are read only for integrity checks.
- The exhaustive queue preserves **all742 training IDs**, latest event digests,
  evidence, reasons, questions and mechanism-local negative scope. It routes191
  ambiguous,57 proposed-exclusion and494 supported cases to consistent review.
  Security provenance routing was checked against the actual training values:
  **342 security_candidate /400 correctness_candidate**. Correctness-origin cases
  require explicit non-security screening; provenance is not the conclusion.
  Literal retrieval excerpts are aids, including possible negations, not decisions.
- Parent counts use unions of supported families/repositories, never sums of leaf
  counts. **126 candidates have no discovery category**:70 ambiguous and56 proposed
  exclusions. CORR-NEWLINE-ROUNDTRIP, SEC-TEMPLATE-SANDBOX and SEC-REDACTION-KEY-MATCH
  have no currently supported training cases. Parent support cannot promote them.
  All eligibility/context/paired-negative/independent-issue decisions remain pending;
  empty eligible and independent count fields remain unknown, not zero.
- The dependence inventory retains **412 mechanical training families** and gives
  **369 connected review blocks** through explicit evidence links:21 shared-exact
  version,22 shared-AST version,61 same-function revision-history,8 same-fix source
  overlap,1 introduced-regression follow-up and1 coordinated-handoff/scope-repair
  link. Link types can overlap; these are pair links, not distinct issues. An
  independent side-specific path/span calculation reproduced all8 overlap links.
  Curated thefuck-11→9 and -17→16 chains verify the shared after/before exact hash.
  Blocks are conservative review units, not approved issue merges or independence
  claims; disconnected blocks can remain dependent through their repository.
- CATEGORY_AUDIT_CONSOLIDATION_REVIEW.md specifies separate contract, selected
  relevance, security, function-only context, paired-negative, representation and
  issue-identity decisions. It proposes a common before-only bounded-function
  condition; numerical budget, deterministic over-budget policy, actual dependency
  assumptions and faithful static-tool representation still need resolution.
- The consolidation manifest also fingerprints four separately retained supplemental
  evidence files without changing the immutable45-input lock. Build/check verifies
  their previously recorded full-file hashes, **32 embedded source-text hashes**
  across batches021–023 and the standalone batch019 enum template. Hash integrity
  does not establish deployed dependency versions or complete caller contracts.
  Focused negative checks rejected altered file hashes, altered embedded source
  text and held-out records supplied to the dependence helper.
- Build/check reproduced all six consolidation artifacts. The discovery audit
  refresh/check reproduced its CSV/checkpoint and verified45 protected inputs.
  No new ledger decisions or revisions were added during proposal preparation;
  all744 events,113 discovery definitions and researcher-pending statuses remain.

## 2026-10-25: first evidence-based consolidation pass, eight Scrapy cases

- Reviewed every Scrapy training candidate assigned to CORR-INCOMPLETE-CASE-HANDLING,
  CORR-STATE-TRANSITION or CORR-CONTEXT-PROPAGATION at this checkpoint: **eight cases**
  (none in the state-transition leaf). Authored proposals are retained in
  CATEGORY_AUDIT_CONSOLIDATION_BATCH_001.json. The generated
  CATEGORY_AUDIT_CONSOLIDATION_CASE_REVIEWS.json preserves independent mechanism,
  contract, selected relevance, context, security, negative, subset and dependence
  dimensions. These are assistant proposals, not approved experimental eligibility.
- Narrowed each mechanism in text instead of forcing a misleading existing leaf:
  gzip media-type identity is not the delimiter-format leaf; a tolerant unknown
  status fallback is not missing-label rejection; optional None elements/capacity
  are not the structural-neighbour NULL-BOUNDARY leaf; an omitted HTML control is
  not a command-correction applicability rule. The two context-propagation cases
  retain their evidenced upstream producer/consumer cause, rather than being
  relabelled merely by their eventual URL or configuration symptom. Discovery
  taxonomy remains **v0.42 /113**; the parent hierarchy remains proposal **v0.1 /25**.

| Case | Narrow mechanism | Strict before-only subset proposal |
|---|---|---|
| scrapy-14 is_gzipped | Whole-field comparison misses media-type case/parameters | Conditional retain under a uniform ordinary-API policy |
| scrapy-17 response_status_message | Partial table lookup passes None to a string-only converter before retry | Defer: converter/table contract outside selected function |
| scrapy-1 get_host_regex | None is matched before the same function's None filter | Defer: local witness visible, policy security boundary unresolved |
| scrapy-25 _get_form | Wrong document-base context is passed to the form tree | Defer: root-builder/action/helper contracts outside selected function |
| scrapy-2 LocalCache.__setitem__ | Optional capacity sentinel reaches an ordered numeric comparison | Defer: constructor's None invariant outside selected function |
| scrapy-30 _iter_command_classes | Python2-only dict method in a proposed Python3 condition | Defer: pre-existing runtime-support obligation unresolved |
| scrapy-32 CrawlerProcess.__init__ | Raw sparse dict forwarded after canonical settings construction | Defer: superclass normalization and consuming key contract omitted |
| scrapy-38 _get_clickable | Clickable enumeration omits image submit controls | Conditional retain for local omitted-control finding under ordinary HTML/XPath semantics |

- **One appended discovery revision:** scrapy-30 revision2 changes supported to
  ambiguous. New exact first-parent setup.py advertises Python2/2.7, and installation
  documentation assumes Python2.7; the fix re-enables ignored Python3 tests. The
  local Python3 AttributeError remains evident, but a prior supported-runtime
  obligation is not established. Missing classifiers alone do not prove unsupported
  status, so do not replace this ambiguity with an automatic feature exclusion.
  Existing Python3 commitment or an explicit experimental-runtime policy is needed.
- Latest discovery totals are **742 unique /745 events**, **493 supported /192
  ambiguous /57 proposed exclusions**. Supported candidates span **342 mechanical
  families**, not independently adjudicated issues. Original744-event discovery
  prefix is byte-identical with SHA256
  **e3f957277307f3bac985d041c3406cde8b00478842921860352a87389b1077d4**;
  complete745-event ledger SHA256 is
  **5c0df95cf68c31786c3581a8a2d4d746070da308e9bc1476992091654aaa7389**.
  Consolidation tooling now derives current status/event counts rather than fixing
  them to the original checkpoint, while verifying the original prefix.
- New CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_001.json pins four exact first-parent
  sources: scrapy-17's converter and retry middleware plus scrapy-30's setup and
  installation documentation. File SHA256
  **8b025086e85bae1dffa40cd776f553c8f95b49591d932e369d2b43cc231530a8**.
  The retry consumer and both converter runtime branches now have retained evidence;
  actual Twisted response mapping/version remains unresolved. Supplemental evidence
  verification covers **five files /36 embedded sources plus the enum template**,
  separate from the unchanged45-input release lock.
- All eight records have hash-verified archived before/after functions and **41
  unique source/fix/supplement anchors** with exact excerpts, source hashes and line
  ranges. Anchors initially matching multiple locations were made specific rather
  than accepted ambiguously. The fixed745-event checkpoint binds each proposal to
  its discovery revision. Later revisions make previous proposals visibly stale;
  stale proposals retain their history but do not count as current review coverage.
- Context sufficiency and security are explicitly separate. In particular,
  offsite dont_filter bypass and missing deployment trust promises prevent treating
  a crawler navigation filter as an established security sandbox. Correct base-tag
  resolution is not SSRF prevention. Unchanged clickdata XPath interpolation is a
  separate provenance question, not a clean-security result. The two conditional
  retain proposals certify neither numerical input budget nor tool feasibility.
- CATEGORY_AUDIT_CONSOLIDATE_TEST.py checks valid coverage, ledger-checkpoint
  tampering, nontraining IDs, contradictory retain/missing-context proposals, stale
  review handling and unique exact evidence anchors. **Six own-tool tests pass.**
  The consolidation generator builds/checks seven artifacts and links the eight
  proposals from the exhaustive742-case queue. Discovery refresh/check reproduces
  the checkpoint and verifies45 protected inputs. No retained dataset source,
  setup file, regex, selector, test, request or command was executed.

## 2026-10-25: second evidence-based consolidation pass, nine Thefuck cases

- CATEGORY_AUDIT_CONSOLIDATION_BATCH_002.json records every Thefuck training case
  in the three broad discovery leaves at its fixed checkpoint: **nine cases**.
  Source, complete fix diffs, consumers and linked versions were read as inert
  evidence. The pass records precise mechanisms rather than forcing runtime API,
  optional-environment and coordinated-protocol cases into incompatible leaves.
  Taxonomy remains draft **v0.42 /113**; the reporting hierarchy remains **v0.1 /25**.

| Case | Narrow mechanism | Strict before-only subset proposal |
|---|---|---|
| thefuck-13 git_branch_exists.match | Branch substring guard excludes new checkout cases | Defer: prior support contract and actual command/error witness unresolved |
| thefuck-15 git_add.match | Optional Git hint required in addition to pathspec error | Defer: old explicit no-hint negative and changed README policy need reconciliation |
| thefuck-16 Bash.app_alias | Invocation variables attached to wrong lifetime/scope | Defer: environment consumer and shell premises omitted |
| thefuck-16 Zsh.app_alias | Variables placed outside correction substitution | Defer: Zsh-specific export/option semantics and consumer omitted |
| thefuck-17 Bash.app_alias | New alias-list producer for simultaneously replaced reader | Defer: selected old component not independently attributed |
| thefuck-17 Bash.get_aliases | Fresh-shell aliases substitute for invoking-shell state | Defer: current-shell caller/producer contract omitted |
| thefuck-17 Zsh.get_aliases | Absent optional environment key indexed on direct CLI path | Defer: supported contextual witness, missing caller invariant in selected input |
| thefuck-23 cache._cache | Python2 shelf used without context-manager protocol | Defer: resource trust/permissions and pickle boundary unresolved |
| thefuck-7 php_s.match | Valid preceding options defeat an adjacency matcher | Defer: correction/app contract omitted; distinguish None-output dispatch |

- **One appended discovery revision:** thefuck-17 Zsh.get_aliases revision2 changes
  ambiguous to supported. Exact pre-fix main.py accepts a direct command, shell
  selection recognizes a Zsh parent, Command._prepare_script calls shell.from_shell,
  and inherited Generic._expand_aliases unconditionally calls get_aliases before
  testing even an ordinary non-alias binary. This establishes a valid absent-key
  caller previously missing from the record; the fallback avoids its KeyError.
  Support is contextual, not a certification of strict function-only admission,
  complete alias recovery or downstream correction/execution safety.
- **Existing Python2 support resolved for thefuck-23:** pre-fix setup.py explicitly
  permits Python2.7 and separately gates supported Python3 versions. The retained
  CPython2.7.10 Shelf has close but no context-manager methods; closing supplies
  those methods. A generic new-runtime feature interpretation is no longer needed
  for this mechanism. The actual deployed patch/backend is still not established.
  Its predictable shared temporary cache and retained Shelf unpickling code leave
  lower-trust write reachability/ownership/permissions unresolved; no shelf or pickle
  was opened and no security-clean after label was inferred.
- **PHP dispatch distinction resolved:** the retained exact pre-fix Rule loader
  defaults requires_output to True and Rule.is_match rejects **output is None**,
  not empty output. Removing requires_output=False therefore does not itself
  contradict blank-string regression inputs. Missing-output/timeout paths remain
  a separate live-dispatch question. The existing matcher/generator contract and
  app guard still require context outside the three-line selected function.
- **Coordinated attribution remains separate:** thefuck-17 Bash.app_alias adds a key
  not consumed by the old reader. Do not manufacture a positive by pairing old
  producer code with only the new consumer. Its after function is exactly the later
  thefuck-16 Bash before function, whose scope repair remains a distinct mechanism.
  Bash/Zsh scope templates share one family; the three thefuck-17 functions share
  another. Neither function counts nor version links prove independent issues.
- New supplemental files are separately pinned without altering the45-input lock:
  CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_002.json contains10 exact pre-fix sources,
  SHA256 **8aa4103ce89005694c2884f46ba52ec0aa26826c69ddbd1fd7975851968f380b**;
  CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_002_CALLER.json retains the inherited generic
  shell caller, SHA256 **d5fa05ab08fb29a57504af44114d784e37a9b534e67dba35fe2a9eb9b93106a3**.
  Supplemental verification now covers **seven files /47 embedded sources plus the
  standalone enum template**. The second batch has **47 unique evidence anchors**;
  together with the first batch,88 source/fix/supplement anchors are verified.
- The proposal validator now handles unresolved existing behavioral contracts,
  coordinated selected-component deferral and unestablished paired negatives.
  Conditional retain requires a mechanism-local negative as well as consistent
  contract/context/security/relevance dimensions. Supplemental paths with multiple
  retained revisions require an explicit matching ref; an ambiguous path cannot
  silently select a convenient version. Nine own-tool tests pass, including these
  cases and earlier checkpoint/nontraining/staleness/anchor-integrity checks.
- Latest discovery totals: **742 unique /746 events**, **494 supported /191 ambiguous
  /57 proposed exclusions**;342 supported mechanical families, not independent issue
  counts. Complete ledger SHA256
  **99fbf502ffa451b97cbacc690167816af516d3b4544d4d9c2691f3478dd78e5b**.
  The earlier745-event prefix and original744-event discovery history remain exact.
  Build/check regenerates seven reproducible artifacts, links all17 current reviews
  from the exhaustive742-case queue and verifies the immutable45 protected inputs.
  Discovery refresh/check reproduces its CSV/checkpoint. No dataset shell, command,
  setup file, module, test, regex, parser, alias, callback or payload was executed.

## 2026-10-25: third evidence-based consolidation pass, five Ansible cases

- CATEGORY_AUDIT_CONSOLIDATION_BATCH_003.json records all **five Ansible candidates**
  in the three broad discovery leaves. Paired selected functions, complete retained
  fixes and exact caller/state/dataflow context were inspected as inert evidence.
  Companion functions remain context, not extra reviewed pairs or independent issues.

| Case | Narrow mechanism | Strict before-only subset proposal |
|---|---|---|
| ansible-15 map_obj_to_commands | Missing global enabling when VRF change suppresses root block; later identical text is VRF-scoped | Defer: critical device hierarchy and starting-state context omitted |
| ansible-3 parse_distribution_file_Debian | Kali admission restricted to legacy path despite existing os-release routing | Defer: supported platform/layout and file-selection context omitted |
| ansible-6 _meets_requirements | Top-level unknown sentinel bypassed for explicit versus implicit equality | Conditional retain under common ordinary operator/comparator and runtime semantics |
| ansible-6 _get_collection_info | Own collection name substituted for actual parent, including top-level None | Defer: old producer/consumer contract omitted |
| ansible-7 generate_commands | Desired setting followed by deletion for overlapping maps | Conditional retain for non-None desired values under a uniform ordinary CLI/API policy |

- **EOS discovery revision2, ambiguous→supported:** retained upstream issue51144
  distinguishes global eAPI no shutdown from the same command under a VRF. The
  reported missing global enablement is not explained by saying the old code emits
  a state command elsewhere: that other command acts in a different scope. Exact
  archived parse_state reads global enabled, and the custom-VRF/unconfigured
  regression supplies the simultaneous state/VRF change. The supported witness is
  conditional global-stopped→desired-started plus VRF change. The historical issue
  is not a hardware reproduction of this exact fix or independent device documentation;
  exact client/version/hierarchy and strict function-only eligibility stay explicit.
  The v0.42 seed note remains historical until a dated taxonomy revision updates it.
- **Collection discovery revision2, supported mechanism narrowed:** the selected
  function documents equality operators and defaults a bare requirement to eq.
  With top-level parent=None and unknown version '*', the bare form uses the sentinel
  continue path while explicit == reaches LooseVersion comparison. That local
  syntax inconsistency is the supported mechanism. Separately, the fix replaces an
  old explicit parented-unknown rejection test with warning/continue: do not call
  that policy relaxation an automatically established bug or version verification.
  Runtime-specific comparison failures are contextual; no comparator/regex ran.
- **Parent-context attribution checked against the old interface:** pre-fix
  _build_dependency_map passes None for top-level requirements and the real parent
  for dependencies; from_path already creates unknown installed versions. Substituting
  the collection's own name causes the old consumer's parent-only rejection and
  skip-path error for an otherwise accepted top-level bare constraint. Unlike the
  deferred Thefuck producer, this selected caller has an old-interface failing
  witness without mixing it with only the new consumer. All three collection
  functions remain one conservative family, not independently counted issues.
- **VLAN overlap reachability pinned:** exact pre-fix dict_diff returns changed
  scalar keys in both directions. The replaced/overridden caller therefore passes
  intersecting set/remove maps for a changed existing attribute. The selected function
  visibly emits set then no for that key; after code skips deletion and emits remaining
  removals first. The negative is restricted to non-None desired values. A None-valued
  key can suppress deletion while also being skipped by the set loop; broader
  device/client behavior remains unresolved. Ordinary CLI/API knowledge must be
  specified uniformly before conditional retention becomes eligibility.
- **Kali scope kept narrow:** the pre-fix caller already routes both release-file
  paths to Debian parsing and already recognizes Kali. The path repair concerns
  identification, not every future release or all version facts. Its retained
  DISTRIB_RELEASE regex does not itself establish VERSION/VERSION_CODENAME extraction
  for the new fixture; prepopulated facts and the existing guess pipeline stay separate.
- New CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_003.json pins the exact pre-fix network
  dict_diff helper, CPython3.8.1/2.7.17 comparator text and an attributed issue51144
  snapshot. File SHA256
  **892abaf17617b669f093ff9fdcbcecfd2f7f8b5ce805a641d6a4dffe30631e1d**.
  The issue body and full gh API response have separate digests, retained timestamps
  and explicit mutable-snapshot limitations; verifier checks matching body, URL,
  title and created/updated dates. Version tags are comparison context only.
  Supplemental integrity now covers **eight files /51 embedded texts**, the retained
  API response and the standalone enum template, outside the unchanged45-input lock.
- Third-pass records verify **33 unique evidence anchors**, for **121 total** across
  all three passes. Ambiguous table/helper excerpts were made specific instead of
  silently selecting a match. Snapshot limitations remain attached to generated
  evidence proofs. **Eleven own-tool tests pass**, including issue/API consistency
  and preservation of mutable-source qualifications alongside prior integrity,
  context/attribution/negative, nontraining and stale-record checks.
- Current discovery is **742 unique /748 events**, **495 supported /190 ambiguous
  /57 proposed exclusions**;343 supported mechanical families, not independent
  issue counts. Ledger SHA256
  **247df4d0d7602a49d4348fc456df664c852aca5eaaae43c5b2a23c4ed9f4a695**.
  Earlier746-,745- and744-event prefixes remain exact. Discovery taxonomy remains
  **v0.42 /113**, parent proposal **v0.1 /25**. Seven consolidation artifacts reproduce;
  discovery refresh/check reproduces the CSV/checkpoint and verifies45 protected inputs.
  All researcher statuses stay pending. No dataset/device commands, callbacks,
  modules, tests, regexes, parsers, installations or model runs were executed.

## 2026-10-25: fourth evidence-based consolidation pass, three Cookiecutter cases

- CATEGORY_AUDIT_CONSOLIDATION_BATCH_004.json records all **three Cookiecutter
  candidates** in the three broad discovery leaves. Exact selected functions,
  matching old/new interfaces, same-family hook chains, directory creation/reuse
  and complete retained fixes were inspected as inert text.

| Case | Existing-contract finding | Strict before-only subset proposal |
|---|---|---|
| cookiecutter-2 find_hook | Scalar path/None becomes list discovery for newly added mixed hook support | Proposed feature exclusion; reversible pending researcher decision |
| cookiecutter-2 run_hook | Matching old scalar consumer becomes list iteration with its new producer | Proposed coordinated-feature exclusion; no mixed-version failure |
| cookiecutter-4 generate_files | Old code already stops; prior cleanup guarantee remains unestablished | Defer existing contract; directory ownership and residual error handling unresolved |

- **Two discovery revisions, ambiguous→proposed exclusion:** exact pre-fix hook docs
  illustrate Python or Shell alternatives, while issue973 asks to add both and
  PR974 explicitly adds simultaneous support. Old find_hook's specific path/None
  return contract agrees with its implementation and matching old run_hook. Its
  stale dict/all-scripts header conflicts with that contract and remains unchanged
  even after the list conversion. The combined evidence supports a feature proposal,
  not a label-only exclusion or an inference that first-match selection is always
  wrong. Mixing only the new producer with the old runner invents a failure.
- **Cleanup discovery revision, supported→ambiguous:** old generate_files already
  checks the status returned through the matching old hook chain and stops before
  template traversal. The directory survives, but the exact pre-fix docs establish
  no cleanup guarantee. Issue464/PR549 request halting, and the Oct17 author comment
  describes adding cleanup. The next day's review requests re-raising rather than
  returning None. Those attributed snapshots explain the change without proving a
  prior cleanup obligation. Later 2020 docs and later merged PR corrections cannot
  retrospectively define the retained intermediate 2015 function.
- The selected after branch still returns None after catching FailedHookException.
  Its conditional cleanup negative requires a newly created output directory and
  successful rmtree. ignore_errors can suppress failures; the pre-fix creation
  helper permits reusing an existing directory under overwrite_if_exists, which
  the after cleanup can recursively delete. Post-hook cleanup is absent. Full
  failure propagation, transactional rollback, directory ownership and security
  placement remain separate questions. Companion hook functions remain evidence
  within the existing four-function family, not additional consolidated candidates.
- CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_004.json retains **nine new texts**: two exact
  pre-fix docs, six attributed issue/PR/comment bodies with full API responses and
  the selected cleanup commit's PR association response. File SHA256
  **18acb528b7cee3fafa866bfaafc64ae807d82b4bdb01f420ada5e1bf6a60a492**.
  Supplemental integrity covers **nine files /60 embedded texts**, seven full
  body-snapshot API responses and the standalone enum template outside the unchanged
  45-input lock. Mutable-source identity, timestamps and qualifications remain in
  generated proofs; title/label/body/URL/date consistency is checked.
- Fourth-pass records verify **28 unique evidence anchors**, for **149 total**.
  **Sixteen own-tool tests pass**, including comment/PR identity/body/date/title/label
  agreement, required complete API snapshots/qualifications, consistent reversible
  feature exclusions and rejection of a conditional retain that contradicts discovery.
  The original checkpoint, context/negative, nontraining, staleness, explicit ref and
  unique-anchor checks remain covered.
- Discovery now has **742 unique /751 events**, **494 supported /189 ambiguous
  /59 proposed exclusions**;342 supported mechanical families, not independent
  issue counts. Complete ledger SHA256
  **beed6ad670007f2213aa14867075968218a74d461c5f5d30ee3f4e8ec7bf54f5**.
  The748-event checkpoint and all earlier ledger prefixes remain exact. Taxonomy
  **v0.42 /113** and hierarchy proposal **v0.1 /25** are unchanged. Seven consolidation
  artifacts reproduce; discovery refresh/check reproduces its CSV/checkpoint and
  verifies45 protected inputs. All researcher statuses remain pending.

## 2026-10-25: fifth evidence-based consolidation pass, twenty Black cases

- CATEGORY_AUDIT_CONSOLIDATION_BATCH_005.json records all **20 Black candidates**
  in the three broad discovery leaves, with **102 unique exact evidence anchors**.
  Each record separates the mechanism, prior contract, selected relevance, missing
  function-only context, security screening, conditional after scope and dependence.
  Coverage is now **45 /742**; these are current assistant proposals, not approvals.

| Cases | Detailed finding | Primary subset proposal |
|---|---|---|
| black-12 two terminating helpers | Nested membership/colon closes virtual region early and corrupts bracket-match depth | Two missing-context deferrals |
| black-12 two increment helpers | Correct old counter producers become depth-stack producers for repaired consumers | Two selected-attribution deferrals |
| black-14 get_future_imports | Single alias node is rejected; nested aliases are skipped | Missing grammar/CST context |
| black-23 lib2to3_parse | Existing modern exec identifier rejected by retained statement keyword | Missing grammar/keyword/contract context |
| black-4 maybe_empty_lines | Initial prefix newlines make a second pass differ and safe mode raise | Missing helper/state/stability context |
| black-8 bracket_split_build_line | Extra comma after standalone comments can split into an invalid import separator | Missing mixed-leaf/rendering context |
| black-9 get_grammars | PY27 selection omits future print_function grammar | Missing target/keyword/retry context |
| black-6 generate_tokens | Supported modern await-valued/filter generators receive NAME outside async-def state | Missing target/config/grammar context and unfrozen long-input budget |
| black-6 parser, constructor and two entry forwarders | Newly introduced config plumbing is not an old dropped configuration | Four selected-attribution deferrals |
| black-11, black-13, two black-5 functions, black-7 | Type comments, new input-language support or layout witnesses need a prior eligible contract | Five existing-contract deferrals |
| black-2 generate_ignored_nodes | Old explicit fmt:on control contract exists; non-style task scope remains unresolved | Task-scope deferral, with missing tree/progress context also recorded |

- **Three discovery revisions, supported→ambiguous:** Black-6 lib2to3_parse,
  Driver.parse_stream_raw and Driver.parse_string adopt/forward a newly introduced
  tokenizer configuration. Old Driver has no config argument/field and old tokenizer
  accepts only readline, so there is no old supplied config these edges dropped.
  The real string-entry failure establishes reachability, not isolated selected
  attribution; the stream edge is not directly exercised by that retained regression.
  Frozen TokenizerConfig defaults false, preserving legacy mode unless the coordinated
  producer selects modern behavior. No missing-attribute/mutable-default or deliberately
  mixed-version failure is invented. The actual tokenizer decision stays supported,
  and all five components remain one mechanical family.
- **State-consumer traces:** old mark applies region decrement before closing-bracket
  lookup. A nested in or default-dictionary colon can lower virtual depth before the
  corresponding real bracket closes. The depth-stack guards repair those consumer
  decisions; the producers' old increments were consistent with their old counter
  representation. Manual traces establish conditional source-level consequences,
  not executed parser states or independently reproduced failures.
- **Grammar/CST and output evidence:** pinned alias grammar plus pytree single-child
  collapse explain actual alias nodes; meaningful unicode_literals is separated from
  parser-only fixture names. Pinned exact historical keyword maps/grammars/classifiers
  support modern exec-identifier and PY27 print-function refusals. The Black-4 helper,
  lstrip caller and assert_stable consumer distinguish safe-mode failure from blank-line
  taste. Black-8 append/comment/split consumers distinguish malformed output from
  optional comma layout; comment deletion is not inferred from list position alone.
- **Unknown scope remains explicit:** per-parameter type-comment meaning is not proved
  by ordinary AST equivalence. Python3.6+ runtime support and references to running on
  Python3.7 do not establish every new input-language promise. Optional signature commas
  and long tuple wrapping do not inherit old runtime/stability failures from new tests.
  In contrast, the fmt:on stopping duty is explicit in its old docstring; unresolved
  non-style task eligibility is recorded separately as defer_task_scope. Tree prefix
  delegation and column invariants must be respected; the new scan's non-advancing
  child branch is a qualified progress question, not a claimed reproduced infinite loop.
- **Exact shared versions verified:** Black-13 tokenizer after equals Black-6 tokenizer
  before; Black-8 builder after equals Black-5 builder before. These already inventoried
  version/history links connect distinct follow-up mechanisms. They do not establish
  chronological ancestry, an automatic issue merge or independent observations.
- Two new supplemental files pin **13 inert texts**: exact pre-fix manuals, grammar
  productions, keyword classifiers and CST conversion/prefix helpers. Pins:
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_005.json:
    **e249902c1f1b390e702b05957cbbc775b3e1b849eda85feae7154e7d20ae8f3f**.
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_005_GRAMMARS.json:
    **68db664a38b4691007d496d12c2f3dae0fbdcc64ec157dda56e39711ce79f94d**.
  Supplemental verification now covers **11 files /73 embedded texts**, seven complete
  discussion-body API snapshots and the standalone enum template. All **251 total
  evidence anchors** resolve uniquely; duplicated fixture/stub excerpts were made
  specific instead of selecting a convenient match.
- **19 own-tool bookkeeping tests pass**, including explicit task-scope separation,
  required scope reasons and rejection of silently incomplete repository batches.
  Discovery totals: **742 unique /754 events**, **491 supported /192 ambiguous /59
  proposed exclusions**;342 supported mechanical families, not independent issues.
  Complete ledger SHA256
  **eaa4791bbadd525598b380a23254c45c26fd4f091b5670aa81399f592f030f3d**.
  The751-event checkpoint and all earlier prefixes remain exact; original744-event
  discovery prefix, taxonomy v0.42/113, hierarchy proposal v0.1/25 and45 protected
  release inputs are preserved. Seven consolidation artifacts and discovery progress
  regenerate reproducibly. All researcher statuses remain pending.
- The user reiterated that this is a work laptop. All dataset/downloaded code,
  security examples, parsers, tokenizers, regexes, formatters, templates, hooks and
  dataset tests remain **inert text**. Only separately authored audit bookkeeping,
  hash verification, evidence retrieval and its own validation tests run.

## Consolidation batch006: Keras — 25 October 2026

- Recorded all **31 Keras training candidates** in the broad incomplete-case,
  state-transition and context-propagation leaves. Detailed coverage is now
  **76 /742**, with **666 remaining**. All proposals and researcher statuses remain
  pending; this is not an eligibility approval or an independent-issue count.
- Batch006 proposals: **14 missing-context deferrals**, **13 existing-contract or
  runtime deferrals**, **2 selected-attribution deferrals**, **1 conditional retain**
  and **1 paired-negative deferral**. Cumulative proposals:5 conditional retain,
  34 missing-context,22 existing-contract,9 selected-attribution,2 security-boundary,
  1 task-scope,1 paired-negative and2 proposed feature exclusions.
- Contextually supported mechanisms retain their critical premises: rank-one target
  indexing; wrong no-worker validation source/steps; rejection of documented session
  kwargs; nested lazy-build probing; heterogeneous activation outputs; three metric
  reset consumers; patience counting; two nominal Sequence iterator consumers;
  multi-output mask arity; optional LSTM bias; ordered shared-layer reconstruction.
  Companion constructors, helpers, layer/build state and dependency semantics remain
  adjudication context, not silently enlarged detection inputs.
- **Four append-only discovery revisions**: three Keras-11 foreign-Sequence consumers
  and the Keras-8 nested process_node helper change supported→ambiguous. Exact old
  image.py declares local Sequence adapters but ImageDataGenerator inherits flow
  from its external parent: adapter existence does not prove actual returned type.
  Old docs restrict automatic step inference to keras.utils.Sequence; a supported
  foreign-producer inference contract is unestablished. The nested helper correctly
  requeues under the old no-result interface; the incorrect continuation lives in
  the enclosing factory. New exception signal and outer break must remain matched.
- TensorFlow printing/assignment compatibility needs exact version/mode/variable
  contracts. A backend name or setup range is not a runtime pin. Seed increments
  introduce successive-call state without a retained prior distinct-samples promise.
  A kwargs-only optimizer override does not prove old positional var_list misbinding.
  Native-tensor generator parity remains a prior-contract question.
- **Paired-negative dimension:** old image callback ordering is explicitly promised,
  but the selected after passes a PIL image before img_to_array despite the unchanged
  rank-three NumPy input/output contract. The new PIL resize fixture does not repair
  that tensor contract. Added explicit defer_paired_negative with supported old
  contract, unestablished negative, unresolved_contract_regression assessment and
  required reason; validation rejects hiding this as context-only or retention.
- Conditional text-separator retain assumes ordinary Python maketrans/translate API
  knowledge under a common policy still awaiting approval. Empty split markers and
  Python2 cascading replacements remain residuals. No tokenization is executed.
- Verified Keras-30 evaluate_generator after equals Keras-29 before: native input
  support leaves the later metric-reset fault present. Exact test_on_batch has no
  hidden reset. Shared source versions and enclosing/nested overlap are dependence
  evidence, not automatic identical roots or independent counts.
- New supplemental evidence retains **9 exact pre-fix texts**, including image/API,
  Sequence, mask/to_list and setup contexts. It is separately pinned at
  **a92e0507e0a78dcb7fe540cfef718c07386d3c19004b32c65f26cd4503cd99ee**.
  All **380 evidence anchors** resolve uniquely, including129 in batch006.
  Supplemental inventory: **12 files /82 embedded texts** plus the enum template.
  Batch006 SHA256:
  **5e3f06b96b878d9a22eedce049fbd40c0c0bb7a770b1f1a5323afa33c86550a0**.
- **22 own-tool validation tests pass**. Discovery: **742 unique /758 events**,
  **487 supported /196 ambiguous /59 proposed exclusions**,341 supported mechanical
  families. Complete ledger SHA256:
  **5472506d5a8be9e1c3173cd299cef9f920fe00b2e6cdcdfc5abf0fd03bd86a91**.
  The754-event prefix and all earlier checkpoints are preserved. Taxonomy v0.42/113,
  hierarchy proposal v0.1/25 and all45 protected release inputs remain unchanged.
  Discovery and seven consolidation artifacts are reproducible.
- All dataset/downloaded code, TensorFlow/Keras imports, setup, models, callbacks,
  initializers, images, tokenizers, generators, fixtures and dataset tests remain
  **inert text** on the work laptop. Only separately authored evidence retrieval,
  hashing, audit bookkeeping and its own tests run. No held-out adjudication or
  model evaluation has started.

## Consolidation batch007: pandas — 25 October 2026

- Recorded all **58 pandas training candidates** in the three broad discovery
  leaves. All **134 broad-leaf candidates now have current proposals**; total
  consolidation coverage is **134 /742**, with **608 remaining**. Researcher
  approval remains not ready and every proposal/status is pending.
- Batch007: **42 missing-context deferrals**, **8 prior-contract/runtime
  deferrals**, **5 selected-attribution deferrals**, **2 feature-exclusion
  proposals**, and **1 conditional retain**. The latter is Series.append's
  locally documented tuple input reaching ordinary Python list-plus-tuple failure.
- Exact old groupby docs promise the unobserved categorical cartesian product;
  count/nunique/size omission is contextual support, with matching reindex/zero-fill
  helper still needed. Exact old custom-window whitelist explicitly excludes count;
  its newly admitted public route and base assertion implement support expansion.
- Appended **five revision2 discovery events**, preserving all earlier bytes:
  pandas-13 _isna_old, pandas-16 frequency wrapper and pandas-43 arithmetic wrapper
  change supported→ambiguous for correct-old-interface component attribution;
  the two pandas-22 count components change ambiguous→proposed exclusion because
  count was explicitly unsupported. Helper defects and shared families remain.
- Exact native source exposes PeriodEngine's vgetter dereference and nullable
  datetime helper's ndarray contract. Engine cache-sharing/lifetime still needs
  a complete matched trace. Nullable unit=ns has a narrower value/nonmutation
  witness; non-ns copy=False backing-storage mutation is not certified away.
  Internal iloc fast-path classification alone does not prove wrong public output.
  Pivot removed return-shape expectations, rename custom-name admission, numeric
  constructor rejection and ambiguous-midnight policy retain prior-contract questions.
- Preserved successive missing-value dispatch, asof tolerance, RangeIndex and scalar
  conversion lineages. Shared versions/commits and multiple dtype/method tests are
  not independent issue counts. No taxonomy leaf or crosswalk meaning changed.
- Separately retained **18 exact pre-fix source/doc texts** in
  CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_007.json; SHA256
  **739e4037d19e05f474816d032472226fe2e005ba5e4fff804d235024877ff8fb**.
  Supplemental inventory: **13 files /100 embedded texts**, plus the enum template.
  **525 unique evidence anchors** resolve, including **145 in batch007**.
- Batch007 SHA256:
  **74f265c2ecf8810cd932f366879d0cc988dae2798d5ab8f0a221348ff184530a**.
  Ledger: **763 events /742 unique**, **484 supported /197 ambiguous /61 proposed
  exclusions**; **340 supported mechanical-family union**, not independent issues.
  Ledger SHA256:
  **19ab3f4ea6d88b3224b2ec1b31f2a27b08432080ac095e29ac7732e08ccb70a6**.
  The original744-event prefix and previous758-event checkpoint remain intact.
- **22 own-tool validation tests pass**. Discovery refresh/check reproduces the
  checkpoint and verifies all **45 protected inputs**; consolidation build/check
  reproduces all **seven artifacts**, including the exhaustive134-case broad-leaf
  coverage assertion. All approval and independently adjudicated counts remain pending.
- All dataframe/index/array/native/parser/callback/source/test/dependency material
  remains **inert text**. Only own retrieval/bookkeeping/hash/validation tooling runs.
  No held-out substantive review, model training or evaluation has started.

## Consolidation batch008: pandas dtype and semantic types — 25 October 2026

- Recorded all **34 pandas training candidates** in dtype-preservation and
  semantic-type-validation. Coverage is **168 /742** current consolidation
  proposals, **574 remaining**; all researcher decisions remain pending.
- Batch008: **22 missing-context**, **5 prior-contract**, **4 selected-attribution**
  and **3 paired-negative** deferrals. No new conditional retain or feature exclusion.
  Exact inherited nullable-array conversion and the actual re-exported cast helper
  strengthen contextual support without adding helper code to detection input.
- Homogeneous extension transpose uses a dictionary keyed by source row labels,
  which can collapse duplicate rows into one output column. Matched temporal lookup
  repairs return source-sized -1 arrays even though old docs/native code require
  target-sized indexers and target positions for missing labels. The Period mismatch
  pattern already existed for incompatible frequencies; its expanded after-side
  failure is not universally claimed introduced by this commit. New tests expecting
  -1 missing positions cannot replace that documented old output contract.
- Paired-negative validation now also accepts an explicit
  `unresolved_contract_failure` assessment, preserving an old supported duty without
  inventing regression chronology. Like `unresolved_contract_regression`, it requires
  the separate deferral, unestablished paired negative and nonempty reason.
- Appended **four revision2 discovery events**: Timedelta searchsorted, Period
  searchsorted and temporal where become ambiguous for prior-policy uncertainty;
  two patches replace old acceptance assertions. Block.replace becomes ambiguous
  for selected attribution: its no-match early return cannot itself cast an unchanged
  numeric block. A complete caller/intermediate-block/normalization trace is needed.
  Correct old Period slice/bin producers remain coordinated components; concrete
  asof label loss and categorical aggregate value loss retain contextual support.
- Retained **23 additional exact training source/doc/test texts** across three new
  separately pinned files. Supplemental inventory is **16 files /123 embedded
  texts**, plus the enum template. **613 unique evidence anchors**, **88 in batch008**,
  resolve; both archived selected spans are verified for all 168 proposals.
  Evidence008 SHA256:
  **b9e49558ce18f9267433ee2551ed001871382039512dc59fba5ffac3cb755baa**;
  helper re-export/inheritance file:
  **9b43c3c8b037b75398eafae62236be6394c2599e9e59ea20670ab5f6178775b7**;
  actual cast helper:
  **0b1700597551534daaa0e5a71223bab951943cc7fd23ccf1e3dd6797d6ba6645**.
- Batch008 SHA256:
  **ae56f2ffc2b1bb923de3cd83eff5449da2c9462c52d108b892c41114618bafac**.
  Ledger: **767 events /742 unique**, **480 supported /201 ambiguous /61 proposed
  exclusions**; **337 supported mechanical-family union**, not independent issues.
  Ledger SHA256:
  **eea3f5e60a1bbd7403498a5ef32a87d10a3ec2c535573181f7d671d0e3759e77**.
  Original744-event and prior763-event prefixes remain intact. Taxonomy v0.42 /113
  leaves and the v0.1 /25-parent proposal retain their meanings.
- **26 own-tool validation tests pass**, including explicit carried-forward
  after-failure deferral, preserved revision history and exhaustive batch selection.
  Discovery refresh/check and consolidation build/check reproduce the checkpoint
  and all **seven artifacts**, verifying the immutable **45 protected inputs**.
- All pandas/NumPy/native/dependency/parser/callback/source/test material remains
  **inert text**. Only own retrieval, hashing, bookkeeping and validator tests run.
  No model training/evaluation or held-out substantive adjudication has started.

## Consolidation batch009: pandas alignment, recovery and transport — 25 October 2026

- Recorded all **50 pandas training candidates** in the nine queued alignment,
  recovery, option, metadata, error, shape, lookup and encoding leaves. Coverage is
  **218 /742** current proposals, **524 remaining**; researcher decisions stay pending.
- Batch009 has **31 missing-context**, **9 prior-contract**, **8 selected-attribution**
  and **2 paired-negative** deferrals. No new conditional retain or feature exclusion.
  Exact old right-merge and union docs establish ordering duties despite API-change
  framing. Native buffer and integer-cast texts establish specific helper contracts
  without supplying those helpers as detection input.
- Appended **seven revision2 discovery events**, supported to ambiguous: duration
  variance rejection, MultiIndex missing-list enforcement, Series non-list rejection,
  Index string-concatenation alignment, finer-string Period containment, concat axis
  identity and strict Series retrieval. Six have unresolved historical policy duties;
  the last needs an isolated matched-old reachable selected-consumer witness. Old
  acceptance tests/docs and intentional old helper interfaces cannot be overridden
  by new assertions, consistency goals or BUG labels alone.
- Categorical datetime construction now preserves multiplicity but still omits the
  original custom index; its unchanged method delegate uses the new parent's index.
  Normalized-margin after validation compares a scalar margin name to a tuple column
  margin for multiple factors and rejects it. The actual values-bearing margin route
  builds a dummy-value-prefixed tuple, then pivot_table removes that dummy level.
  Both after-contract failures preserve supported old duties and use explicit
  `unresolved_contract_failure` deferrals without asserting new introduction.
- Unique-index join and array-array logical negatives stay narrow: duplicate-index
  sort forwarding and scalar native dimensionality remain uncertified. Policy-less
  fast union, new-exception consumers, temporal repeat/take refactors and a widened
  Period overflow catch are not automatically separate old selected defects.
  Successive range, unstack and scalar-converter histories retain dependence.
- Retained **13 additional exact old training source/doc/test texts**, separately
  pinned in two files. Inventory: **18 supplemental files /136 embedded texts**, plus
  the standalone enum template and seven full mutable body-snapshot API responses.
  **730 evidence anchors**, including **117 in batch009**, resolve uniquely within
  their retained texts; both selected archived spans are verified for all218 proposals.
  Evidence009 SHA256:
  **f329189b9478c00d354f478215f30297e595ae04af6962eaef17b91e07c8baca**;
  additional helpers/contracts:
  **93f57b2f080ad9ef814a75dd5d866ff3c1ab0febd8e4eb841df036dc3e9eefb2**.
- Batch009 SHA256:
  **09275482d571bcc337983243cf8d9f10e2d938bdb64561c98171f21537c1d48e**.
  Ledger: **774 events /742 unique**, **473 supported /208 ambiguous /61 proposed
  exclusions**, **331 supported mechanical-family union**, not independent issues.
  Ledger SHA256:
  **ce2e46f82dd898d4a274ad2e5e928f7f0b74e32b58de6f51f2122da6afe7fab1**.
  The original744-event and prior767-event prefixes remain intact. Taxonomy
  **v0.42 /113 leaves** and the **v0.1 /25-parent** proposal retain their meanings.
- **30 own-tool validation tests pass**. Discovery refresh/check and consolidation
  build/check reproduce the checkpoint and all **seven outputs**, verifying all
  **45 protected inputs**. All prior authored batches remain retained as history.
- All pandas/NumPy/native/parser/callback/dependency/source/test programs stay
  **inert text**. Only own retrieval, hashing, bookkeeping and validator tests run.
  No model training/evaluation or substantive held-out adjudication has started.

## Consolidation batch010: remaining pandas candidates — 25 October 2026

- Recorded all **32 remaining pandas training candidates**, including **19
  unclassified** cases and 13 across the remaining twelve assigned leaves. All
  **174 pandas candidates** now have current consolidation proposals. Overall
  coverage is **250 /742**, **492 remaining**; researcher decisions stay pending.
- Batch010: **11 missing-context**, **2 prior-contract**, **16 selected-attribution**
  and **1 paired-negative** deferrals, plus **2 proposed feature exclusions**.
  New option, empty-input/reduction, null-normalization, missing-target, coordinate,
  subclass-result and zero-arithmetic evidence retains contextual support. No new
  conditional retain is proposed while the common API/runtime/context budget is open.
- Appended **three revision2 discovery events**. Series multidimensional getitem
  becomes ambiguous: the exact old test deliberately accepts several index domains
  with a DeprecationWarning, and the patch newly requires ValueError. Both pickle
  URL-admission discoveries become proposed feature exclusions: old docs promise
  paths, new docs explicitly versionchange URL support. Canonical records remain
  intact; a demonstrated earlier guarantee can reverse these proposals.
- Missing-marker capacity is an established old export duty, but the repair sizes
  every non-object/unquoted cast from `word_len(na_rep)` alone. IntBlock inherits it;
  default `na_rep="nan"` narrows nonmissing integer text such as 12345 to U3, whereas
  the old inferred-width cast preserves it. This source-deduced introduced truncation
  uses explicit `defer_paired_negative` / `unresolved_contract_regression`, rather
  than silently becoming a missing-context note. No CSV/NumPy reproduction is run.
- Correct old category-property expansion, normal-NA forwarding, duration std,
  in-place frequency helpers and default-fill/merge/copy interfaces are distinguished
  from new coordinated requirements. Retired scalar extraction is separate from
  the actual caller-side boxing failure. Exact old tests and matching old interfaces
  cannot be overridden by new assertions or synthetic mixed-version failures.
- Retained **9 additional exact old training source/doc/test texts**, separately
  pinned in CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_010.json; SHA256
  **8ddfd4a7f830e596df885a721c381beb6ef0b0c00c53019ffe1b5e5d7fbb8a5d**.
  Inventory: **19 supplemental files /145 embedded texts**, plus the standalone enum
  template and seven full mutable body-snapshot API responses. **806 evidence
  anchors**, including **76 in batch010**, resolve uniquely; both archived selected
  spans are verified for all250 current proposals.
- Batch010 SHA256:
  **110eb31d6f10779dfae460d025faaa482eca4508e835ed140d8b65a7d082afe8**.
  Ledger: **777 events /742 unique**, **472 supported /207 ambiguous /63 proposed
  exclusions**, **330 supported mechanical-family union**, not independent issues.
  Ledger SHA256:
  **88b984675aacade9e41696e6577c4dd7d3deaad9a38f65d2ae6f336b8a63167b**.
  The original744-event and prior774-event prefixes remain intact. Taxonomy
  **v0.42 /113 leaves** and the **v0.1 /25-parent** proposal retain their meanings;
  dependence remains412 families/369 connected review blocks, not independent issues.
- **33 own-tool validation tests pass**. Discovery refresh/check and consolidation
  build/check reproduce the checkpoint and all **seven outputs**, verifying all
  **45 protected inputs**. Prior authored batches remain retained as history.
- All pandas/NumPy/native/parser/callback/dependency/source/test programs remain
  **inert text**. Only own retrieval, hashing, bookkeeping and validator tests run.
  No model training/evaluation or substantive held-out adjudication has started.

## Retained batch010 continuation checkpoint: 25 October 2026

Current checkpoint: **742 /742 training discovery reviews**, **0 remaining**,
**777 events**, **472 supported /207 ambiguous /63 proposed exclusions**, draft
**v0.42 /113 discovery labels**. First consolidation proposal **v0.1 /25 reporting
parents**, exhaustive742-case work queue and412-family/369-block dependence review
inventory are reproducible. **250 /742 candidates have separate current consolidation
proposals;492 remain.** Proposals:6 conditional retain,140 missing-context deferrals,
2 unresolved security-boundary deferrals,46 existing-contract deferrals,42
selected-component attribution deferrals,1 task-scope deferral,7 paired-negative
deferrals and6 proposed feature exclusions. Final
decision dimensions and researcher statuses remain pending. Researcher approval is
not yet ready; held-out category adjudication has not started.

Start with CATEGORY_AUDIT_CONSOLIDATION_REPORT.md and
CATEGORY_AUDIT_CONSOLIDATION_REVIEW.md. Next perform evidence-based refinement of
the207 ambiguities/63 exclusion proposals and priority exact-version/source-overlap
links. The three broad incomplete-case/state/context leaves are fully covered by
current proposals, as do all174 pandas training candidates (58 overlap those broad
leaves). Next inspect all **42 remaining Keras training candidates** outside its
completed broad-leaf batch, including every discovery status and unclassified case.
Preserve exact historical backend/API admission, dtype/shape/state and callback
contracts. Do not assume constructor support, execution order or runtime promises
from the new tests alone.
Preserve matched producer/consumer, metadata, option, shape, recovery and label
contracts, functional fast-path effects and source-version dependence. Distinguish
support expansions and coordinated components from established selected defects;
keep paired-negative regressions explicit. Do not execute pandas, NumPy, models, fixtures,
downloaded modules or dependency setup. Then continue the remaining eligibility queues.
All substantive evidence remains training-only.
Read exact source/consumer evidence and version links before deciding each dimension;
do not copy the earlier repository outcomes automatically. Apply the same rules to supported
cases. Resolve actual caller/dependency
contracts and missing pins; verified retained hashes alone do not settle them.
Record changed consolidation proposals in a new dated batch retaining per-case
review history; append a discovery-ledger revision for any changed discovery
decision. Version changed crosswalk meaning with its rationale. Prepare researcher confirmation only
after coherent eligibility/context/negative/issue proposals exist.

Run `python3 CATEGORY_AUDIT.py refresh` and `python3 CATEGORY_AUDIT.py check` to
reproduce the discovery checkpoint. Run `python3 CATEGORY_AUDIT_CONSOLIDATE.py check`
to verify the consolidation artifacts without rewriting them; after intentional
changes to fingerprinted sources, run `build` and then `check`. The discovery
`queue --limit 50` correctly returns an empty queue; use the exhaustive consolidation
review queue for the next pass. Run `python3 -m unittest CATEGORY_AUDIT_CONSOLIDATE_TEST.py`
when changing the own-tool evidence/proposal validator.

## Consolidation batch011: remaining Keras candidates — 25 October 2026

- Recorded all **42 remaining Keras training candidates** outside the completed
  broad-leaf batch, including every status and null category. All **73 Keras** and
  **174 pandas** training candidates now have current proposals. Coverage is
  **292 /742**, **450 remaining**; researcher approval remains pending.
- Batch011: **14 missing-context**, **4 old-contract**, **9 selected-attribution**
  deferrals and **15 proposed feature exclusions**. Explicit output_size/state-order
  evolution, transposed-convolution dilation, optional best-weight restoration and
  optional Sequence step inference change the old API/admission policy. Fifteen
  ambiguous discoveries become proposed exclusions; the source pairs remain intact.
- **19 revision2 discovery events appended**, retaining all previous bytes. Three
  worker-error discoveries become ambiguous because exact old FaultSequence tests
  explicitly expect StopIteration; newly preserving the original error class needs
  an established old obligation. Downloader KERAS_HOME becomes ambiguous because
  backend configuration support does not alone prove a historical download-cache
  environment promise; exact old downloader/FAQ describe the default dataset path.
- Temporal sparse-label axes, singleton CTC/regressor sample dimensions,
  heterogeneous recurrent state masking/shapes, stacked per-step build dimensions,
  inclusive time-series endpoints, Windows CSV record separation, unknown-target
  progress and finite all-masked loss retain contextual support. Old state order,
  caller/helper shape admission and platform/backend semantics remain critical
  before-only questions. New helpers must not be mixed with old callers as witnesses.
  Earlier sparse-accuracy flattening still loses temporal axes; all-zero weights
  still have a separate denominator. Batch006's image callback after failure stays
  explicit. No universal backend, Unicode, queue race or archive-security negative.
- Six exact old training source/doc/test texts retained in
  CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_011.json, SHA256
  **3df64f8f44fd989803ab4ba2ce0c5b9fe99d1854491f75ac7e30d1656048bd37**.
  Inventory: **20 supplemental files /151 embedded texts**, plus the standalone
  enum template and seven full mutable body-snapshot API responses. **913 evidence
  anchors**, including **107 in batch011**, resolve uniquely; both archived selected
  spans are verified for all292 current proposals.
- Batch011 SHA256:
  **4342901d90df9a2cf0a2adc6f7ae820a7d75ce7bdcea5ddae94876bb6aa55c15**.
  Ledger: **796 events /742 unique**, **468 supported /196 ambiguous /78 proposed
  exclusions**, **328 supported mechanical-family union**, not independent issues.
  Ledger SHA256:
  **8b01d57c1114ecc51f49d8c2b5ef38de9a02c50e4aff46ffe41150b0f8860388**.
  The original744-event and prior777-event prefixes remain intact. Taxonomy
  **v0.42 /113 leaves**, **v0.1 /25-parent** proposal and dependence inventory
  **412 families /369 connected review blocks** retain their meanings.
- **36 own-tool validation tests pass**. Discovery refresh/check reproduces the
  checkpoint and verifies all **45 protected inputs**. Consolidation build/check
  reproduces all **seven outputs** with protected inputs unchanged.
  Prior authored batches remain retained as history.
- Keras/TensorFlow/CNTK/Theano/NumPy/model/callback/generator/download/dataset/
  dependency programs and upstream tests remain **inert text**. Only own retrieval,
  hashing, bookkeeping and validator tests run. No model training/evaluation or
  substantive held-out adjudication has started.

## Consolidation batch012 and security metadata correction013 — 25 October 2026

- Recorded all **40 remaining Scrapy training candidates** outside its completed
  broad-leaf batch: **10 missing-context**, **13 old-contract**, **16 selected-attribution**
  and **1 paired-negative** deferral. All **48 Scrapy**, **73 Keras** and **174 pandas**
  candidates now have current proposals. Coverage: **332 /742**, **410 remaining**.
- Appended **nine revision2 discovery events**. Old installation docs advertise
  Python2.7 and explicitly skip proxy modules/tests on Python3; conditional Python3
  failures do not establish prior supported-runtime obligations. Old Latin1 redirect
  expectations and newly tolerated invalid DNS labels also leave historical policy
  unresolved. Preserve the matched old proxy producer failure before blaming its
  downstream setter; never substitute a repaired producer as an old witness.
- Thirteen logging callers correctly supply the old failure field. A parent logger
  filter misses propagated child records, supporting a shared traceback-routing
  problem without isolating thirteen local algorithm defects. Diagnostic non-style
  duty and attribution remain separate. The form URL helper already receives a
  resolved lxml action; its document-base producer repair is not local helper blame.
- Gzip's old recovery duty is supported, but after uses extrabuf[-extrasize:].
  Retained CPython2.7.12 transitions can leave consumed extrabuf with extrasize=0
  before a caught footer error; [-0:] replays that buffer. Recorded explicitly as
  **unresolved_contract_failure**, a conditional residual source deduction rather
  than a reproduced or newly introduced failure. No compressed input executes.
- The credential-destination review describes a genuine confidentiality boundary,
  but batch012 initially retained the generic functional security-screen enum.
  **Batch013 preserves batch012 and records review_revision2** with
  demonstrated_security_boundary, matching its already explicit trace. Discovery
  judgment, missing-context proposal and explicit-nonempty-domain negative remain
  unchanged. **333 historical review records /332 current candidates**; no new
  eligible or independent issue count follows from this metadata correction.
- Retained **24 texts** in CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_012.json: 22 exact
  historical Scrapy source/doc/test texts and CPython2.7.12 gzip/3.5.1 logging
  comparison sources. SHA256:
  **cd9b53f55329cc85e0561d075178820e85f2fbe6cd58ded40c607182e70b5da2**.
  Comparison tags do not prove installed/deployed versions. Inventory:
  **21 supplemental files /175 embedded texts**, the standalone enum template and
  seven full mutable body-snapshot API responses. **1,059 current evidence anchors**
  each resolve uniquely; both selected source spans remain hash-verified.
- Batch012 SHA256:
  **2d9e8a169eecdf2d72c00d5ac4f7c4ecf0348f6d6b46431f86a7146780b50d6d**.
  Batch013 SHA256:
  **712b76e276cfeb9aa320bdc662df46905bc060c0958c5889b3dce61225f5380a**.
  Ledger: **805 events /742 unique**, **459 supported /205 ambiguous /78 proposed
  exclusions**, **321 supported mechanical-family union**, not independent issues.
  Ledger SHA256:
  **01d082abd0bde3518a4bc6ce51e94593afae71533c1fc02592869171d946c2f6**.
  All796 prior event bytes remain unchanged; taxonomy v0.42/113 leaves and pending
  v0.1/25-parent hierarchy remain intact. Dependence remains **412 families /369 blocks**.
- **40 own-tool tests pass**. Validation covers append-only history, exhaustive Scrapy selection, retained
  gzip after-failure deferral and explicit security-screen correction history.
  Discovery refresh/check and consolidation build/check pass, reproducing all seven
  outputs and verifying all **45 protected inputs**. The release lock remains unchanged.
  Dataset/dependency programs and upstream tests remain inert; no substantive
  held-out adjudication, model training/evaluation or publication takes place.

## Consolidation batch014: remaining Black candidates — 25 October 2026

- Recorded all **30 remaining Black training candidates**, every status and null
  category, including one CVEfixes source. All **50 Black**, **48 Scrapy**, **73 Keras**
  and **174 pandas** candidates now have current proposals. Coverage is **362 /742**,
  **380 remaining**, with **363 historical review records**. Researcher approval remains pending.
- Batch014: **4 missing-context**, **4 old-contract**, **17 selected-attribution**,
  **2 non-style task-scope** deferrals, **1 feature exclusion** and **2 nonrepair exclusions**.
  The latter use explicit no_selected_runtime_repair/propose_nonrepair_exclusion
  fields: scheduler annotation documentation and AST error guidance do not repair
  established runtime behavior, without being mislabeled as feature expansion.
  DebugVisitor's new Leaf/Node admission is a separate feature-expansion proposal.
- Appended **two revision2 discovery events**, preserving all prior805 event bytes.
  ProcessPoolExecutor construction fails in restricted environments, but old docs
  do not establish support/fallback there; default None executor may create a thread
  pool, not serial execution. Missing config already raises an explicit FileError;
  early Path validation changes status1 to2 without establishing an old usage-status
  promise. Both findings become ambiguous pending prior support/policy evidence.
- Raw-coordinate tab counting and diff basename identity retain local duties but
  unresolved non-style task eligibility. Seventeen pragma/comment edits remain
  selected-attribution deferrals: matched old exception/subclass/dictionary/comment
  producers and consumers are not faulty merely because representation changes.
  Do not test old comma removal against new indexed comments or old classification
  against newly admitted mixed comment/code leaves.
- Old newline byte-preservation obligation remains unresolved. Separately, both
  file/stdin after routes call new prepare_input before NothingChanged. Retained
  CPython3.6.5 detect_encoding returns [] for empty bytes; helper lines[0] then
  raises while matching old empty text returned False. Explicit additional_after_concerns
  records this **introduced empty-input regression** without manufacturing a
  supported old newline-positive. This is source deduction only, not reproduction.
- CVE-2024-21503's exact leading-tab function has a contextual availability boundary
  under untrusted source; its omitted regex contains overlapping whitespace/tab
  repeats. Removal of that matcher is a bounded negative, not total formatter
  resource safety. CVEfixes archived spans are verified from their actual security
  snapshot archive; the validator no longer assumes every source has HaPy metadata.
  Fix anchors still require real retained HaPy commit metadata, never an unrelated fix.
- Retained **12 source/doc texts** in CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_014.json:
  seven exact old READMEs and five CPython/Click comparison texts. SHA256:
  **77485ed79e372051c8d4b0955937b24deee78fa0a82aa140b048e1c4a127f977**.
  Comparison tags are not deployed-version proof. Inventory: **22 supplemental files
  /187 embedded texts**, standalone enum template and seven full mutable snapshot
  API responses. **1,143 current evidence anchors**, including **84 in batch014**,
  each resolve uniquely; before/after selected spans remain verified.
- Batch014 SHA256:
  **55746bd77e3bab585c14dd85f7f3fc79c8b0e69420ca1bf5dfa56059df9b1a0e**.
  Ledger: **807 events /742 unique**, **457 supported /207 ambiguous /78 proposed
  exclusions**, **319 supported mechanical-family union**, not independent issues.
  Ledger SHA256:
  **7a3bae6bdb33eccbbb4d19dc40f1e2f6f2a99f15dd94827f6fc607a72e57bf65**.
  Taxonomy v0.42/113 leaves, pending v0.1/25-parent hierarchy and dependence inventory
  **412 families /369 connected review blocks** retain their meanings.
- **45 own-tool tests pass**, including source-specific CVEfixes proof handling,
  exhaustive Black coverage, append-only correction history, nonrepair/feature
  separation and explicit after-side empty-input concerns. Reproduce with discovery
  refresh/check and consolidation build/check after fingerprinted edits. The
  **45 protected inputs** and release lock
  remain unchanged. All formatter/parser/tokenizer/regex/CLI/process-pool programs,
  fixtures, upstream tests and dataset/dependency code remain inert. No model
  training/evaluation, substantive held-out adjudication or publication occurs.

## Consolidation batch015: Spirit redirect candidates — 25 October 2026

- Recorded all **29 Spirit training candidates**, every status and selected outer/
  nested span. All share CVE-2022-0869, fixing commit8f32f89654d6c30d56e0dd167059d32146fb32ef
  and fix-family:16a6f2362e44482de4e9. This is one conservative mechanical family,
  not29 independent observations or an approved issue count. Coverage: **391 /742**,
  **351 remaining**, **392 historical review records**; researcher approval remains pending.
- **Four missing-context deferrals** cover wired auth-entry early returns with
  direct query-link witnesses: authenticated login/register/activation-resend and
  unauthenticated logout. **Twenty-five security-boundary deferrals** preserve the
  conditional dangerous source-to-Location mechanism while leaving realistic victim
  POST delivery unresolved for23 gated outcomes, and installed-consumer evidence
  unresolved for the overlapping guest_only factory/wrapper. An uninvoked closure
  definition alone does not establish a route. Common context admission is still pending.
- **Nineteen POST parameter sources /ten GET sources**. Four GET-next paths still
  require POST operation: comment moderation, admin config/user edit, poll-owner
  open/close. New structured redirect_analysis records source separately from the
  operation gate. Validation checks it against the retained selected source and
  explicit POST helper selection rather than equating GET provenance with GET execution.
- Preserve duplicate-only topic/private publishing, both comment publish/vote
  outcomes, valid-form-only branches, invalid-form convergence, non-AJAX like
  branches, fixed own-access deletion and anonymous login redirects. Moderator,
  administrator, owner, form, limiter, duplicate-hash and CSRF gates are not removed
  by an unsafe redirect parameter. No anonymous access, CSRF bypass, SSRF, credential
  disclosure or repaired poll-authorization claim follows from these selected edits.
- Same-fix safe_redirect matches admitted companion SHA256
  **63561b34e59a36fa34fae07fc84a1d38897f40554582f2cce0bdd3197867e52b**.
  It validates the selected mapping; falsey/missing next resolves the supplied
  default lazily. An unsafe nonempty value goes to **`/`**, not the supplied fallback.
  allowed_hosts=None becomes an empty set; current host/ALLOWED_HOSTS admission and
  require_https are not enabled. The negative is ordinary external-HTTPS rejection
  on a reached branch, not complete parser/browser/authorization/session security.
- Old requirements advertise **Django>=2.2,<3.2**. Retained2.2.27/3.1.14 text covers
  both legacy and modern matcher imports within that range; retained3.2.12 text is
  outside it and comparison only. Tags are not installed/deployed-version proof.
  Old templates show CSRF-protected POST forms, not a demonstrated arbitrary victim
  delivery chain. Helper/route/patch/test text stays adjudication-only context.
- Retained **24 source/template/test/patch texts in two new evidence files**:
  CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_015.json SHA256
  **7f8b2c6b29b6185c8c44e57bd4ad07630f8b2eb1d42fc73e819741caeee1ecd7**;
  CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_015_FRAMEWORK.json SHA256
  **3c0a3546a3d8df081202d115b89de636115d474f3a82d7d92de26ccb61c1a99e**.
  Inventory: **24 supplemental files /211 embedded texts**, standalone enum template
  and seven full mutable snapshot API responses. **1,419 current evidence anchors**,
  including **276 in batch015**, each resolve uniquely; both selected spans remain verified.
- Batch015 SHA256:
  **6b7ee75af85b2fc89900c6288b94996e81da6b24db83828da39fd7336f7406d0**.
  **No new discovery events**: all source-to-sink findings remain supported under
  recorded conditions, while final eligibility is explicitly deferred. Ledger remains
  **807 events /742 unique**, **457 supported /207 ambiguous /78 proposed exclusions**,
  SHA256 **7a3bae6bdb33eccbbb4d19dc40f1e2f6f2a99f15dd94827f6fc607a72e57bf65**.
  Supported mechanical-family union remains319; taxonomy v0.42/113 leaves, pending
  v0.1/25-parent hierarchy and **412 families /369 dependence blocks** are unchanged.
- **49 own-tool tests pass**, covering exhaustive Spirit selection, GET-parameter/
  POST-operation separation, victim-boundary deferrals, nested-source overlap and
  preserved ledger bytes. Reproduce with discovery refresh/check and consolidation
  build/check after fingerprinted edits. All45 protected inputs and the release lock remain
  unchanged. No view, ORM, request, redirect/URL helper, browser payload, framework,
  application/dependency program or upstream test executes. No substantive held-out
  adjudication, model training/evaluation or publication occurs.

## Consolidation batch016: remaining Thefuck candidates — 25 October 2026

- Recorded all **21 remaining Thefuck training candidates**, including null-category
  cases and every discovery status; all **30 Thefuck** now have current proposals.
  Coverage: **412 /742**, **330 remaining**, **413 historical review records**.
  Batch016: **9 missing-context /3 existing-contract /2 selected-attribution
  /2 paired-negative deferrals /3 feature-policy /2 nonrepair exclusions**.
  Researcher approval remains pending; no independent issue count is inferred.
- Append-only correction: **Settings.update supported→ambiguous**, revision2.
  Its exact old docstring/direct test promise kwargs overwrite; the wrapper docstring
  instead promises defaults only, while its old test also expects overwrite. The
  selected helper follows its advertised old API. Reversing global update semantics
  changes that API to satisfy the caller interpretation, not an isolated old helper
  defect. Preserve caller/helper attribution and unresolved old-policy conflict.
- First-two uniqueness already ignores priority using script/side_effect fields;
  matched new equality uses those same fields. The old duplicate mapping already
  excludes cached first and retains the smaller numeric priority by overwrite.
  These selected routines are nonrepair exclusions, not positives because class
  equality changed. New comparison of command.script with cached CorrectedCommand
  fails to exclude cached first: in the coherent new [ls@100,git@100,ls@200] trace,
  realization prepends ls again. Record this introduced after concern; never mix old
  namedtuple and new consumer. Descending sorted set insertion also changes priority
  retention from old mapping overwrite. No class/set behavior is executed.
- Explicit upstream correction removes existing -u origin duplication, but newly
  joining shell-split tokens loses quoted option protection and mutates cached state.
  Its after exactly equals the later terminal-option repair's before. New second pop
  raises for terminal -u. The initial metadata assumption that the old trailing
  -u output was necessarily incorrect is superseded by batch017 below. Quoting loss is an
  **unresolved_contract_regression**; the later catch's unchanged quoting failure is
  **unresolved_contract_failure**, not attributed to the catch. Existing curated
  introduced-regression/follow-up dependence link is preserved, not duplicated.
- Preserve intentional interfaces: opt-in/advertised --force, replacing custom Fish
  exclusions, targeted Vagrant start and line-only editor default. Safer lease policy,
  additive exclusions, extra start-all choice and optional column templates do not
  retroactively establish old duties. HDFS-prefixed mkdir remains ambiguous: broad
  old matching plus new support tests is not a settled old correction promise.
- Exact old AppVeyor Windows test configuration supports platform PATH-separator
  duty; source/CI intent is not a CI run or deployment proof. Exact old app-version
  dispatch reaches Fish.info, but startup hook/runtime callback remains unestablished.
  Selected **fish -c is noninteractive**; informal commit wording is not -i evidence.
  Do not exclude an informational routine automatically or promote a mock to a loop trace.
- Bounded contextual repairs retain omitted contracts: plain-git stash, empty-cache
  realization, quoted archive operands, empty aliases, Git filename-option ordering
  and incidental set-upstream output. Installed-vim false match can emit an unchanged
  command, not necessarily an unrelated one. New falsey-token dereference is a
  direct-rule concern; empty CLI construction is rejected and Rule.is_match catches
  exceptions. No whole-app crash is claimed. Apostrophe capture repair does not
  transfer blame to the already-admitting sibling guard; apostrophe replacement is
  neither full shell quoting nor a demonstrated injection repair.
- Retained **40 exact old helper/contract/test/CI texts in three new files**:
  CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_016.json SHA256
  **f48191a4227faff6aba6fc3194c8ff8f4d2eb02dd3b654fa17545872e230403e**;
  CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_016_CONTRACTS.json SHA256
  **87c053618b3a822fe9b5ebd7d5d59f6fae8ed1f09dad4cf5e3dee464b6b29278**;
  CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_016_TOKENIZERS.json SHA256
  **480e402ce45077136387885278c7f87530e399274527dc58661df83411f7d518**.
  Supplemental inventory: **27 files /251 embedded texts**, standalone enum template
  and seven full mutable snapshot API responses. **1,531 current anchors**, **112 new**,
  resolve uniquely; both selected spans remain verified. Historical source stays
  adjudication-only, never selectively injected into detection input.
- Batch016 SHA256:
  **153301634ff350389f79929aac6664d2a21a0435cacde018bfdeab062050866a**.
  Ledger: **808 events /742 unique**, **456 supported /208 ambiguous /78 proposed
  exclusions**, supported mechanical-family union **318**, not independent issues.
  Ledger SHA256 **590e37fbe1828b68634fccc089589b9abba27a909946a53f7a789a0a72410642**.
  First807-event bytes remain unchanged, SHA256
  **7a3bae6bdb33eccbbb4d19dc40f1e2f6f2a99f15dd94827f6fc607a72e57bf65**.
  Taxonomy v0.42/113 leaves, pending v0.1/25-parent hierarchy and mechanical
  **412 families /369 dependence blocks** remain unchanged.
- Verify own audit-tool tests and discovery refresh/check plus consolidation
  build/check after final fingerprinted edits. All45 protected inputs and release
  lock remain unchanged. No shell, executable lookup, Git, editor, archive operation,
  process, parser/tokenizer, dependency/application program or upstream test executes.
  No substantive held-out adjudication, training/evaluation or publication occurs.

## Consolidation batch017: Boolean Git flag metadata clarification — 25 October 2026

- Re-reviewed the complete **three-case Thefuck command-argument-rewrite leaf**,
  preserving authored batch016. One review corrects the old terminal-option grammar
  assumption; HDFS mkdir and staged diff proposals are revalidated unchanged.
  **No new candidate, discovery event, eligibility decision or dependence edge.**
  Current coverage stays **412 /742**, **330 remaining**, now **416 historical records**.
- Historical Git v2.9.3 declares -u/--set-upstream as **OPT_BIT with PARSE_OPT_NOARG**.
  Positive occurrences bitwise-OR the same flag; builtin push passes parser flags0,
  and that parser continues collecting positional operands rather than stopping
  at the first non-option. Thus old git push --set-upstream origin master -u can
  retain the intended remote/refspec and redundantly set the same bit. New second
  pop in the explicit-repository repair instead raises: a source-deduced **introduced
  terminal-option regression**, not merely another failure on an already-broken
  old suggestion. It is distinct from duplication of a positional origin refspec
  for -u origin; origin is not an option argument consumed by the Boolean flag.
- Quoted receive-pack argument preservation remains a second introduced concern;
  the later terminal catch retains earlier quoting/cached-state failures. No whole
  negative, actual push/network result or reproduced behavior is claimed. Historical
  Git source/docs establish comparison grammar, **not the installed/deployed version**.
- New evidence CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_017_GIT.json has four inert
  Git source/documentation texts, SHA256
  **7c1c968948efd1a36eb8a1db7a975b64f312d7e476990496ee0d3d302863e830**.
  Batch017 SHA256
  **cd023be6042b0ab8a1b2976a82c95249a7a02249d65005d259a2dbbb69b77539**.
  Totals: **28 supplemental files /255 embedded texts /1,536 current anchors**;
  five added anchors supersede metadata without changing selected source proof.
- Ledger remains808 events, SHA256
  **590e37fbe1828b68634fccc089589b9abba27a909946a53f7a789a0a72410642**,
  **456 supported /208 ambiguous /78 proposed exclusions**,318 supported mechanical
  families. Taxonomy v0.42/113 leaves, pending v0.1/25-parent hierarchy,412 mechanical
  families/369 dependence blocks and all current proposal counts are unchanged.
  Review revisions are historical records, not independent observations or new votes.
- **55 own audit-tool tests pass**, including exhaustive null-category coverage,
  selected-helper attribution/history preservation, introduced-versus-retained after
  failures, nonrepair boundaries and immutable Boolean-flag metadata correction.
  Reproduce with discovery refresh/check and consolidation build/check after final
  fingerprinted edits. All45 protected inputs/release lock stay unchanged.
  Git, option parser, shell, dependency/application programs and upstream tests remain
  inert text; no substantive held-out adjudication, evaluation or publication occurs.

## Consolidation batch018: complete Synapse contract/security review — 25 October 2026

- All **21 Synapse training candidates** now have current proposals across **five
  mechanical fix families**. Outcomes: **10 missing-context**, **7 security-boundary**,
  **1 selected-attribution**, **1 paired-negative** deferral and **2 proposed nonrepair
  exclusions**. Both null-category downloader exclusions are included. Coverage becomes
  **433 /742**, **309 remaining**, **437 historical records**. All remain unapproved.
- No discovery decision changes: ledger remains **808 events /742 unique**, **456
  supported /208 ambiguous /78 proposed exclusions**, SHA256
  **590e37fbe1828b68634fccc089589b9abba27a909946a53f7a789a0a72410642**.
  Taxonomy v0.42/113 leaves, pending v0.1/25-parent hierarchy,318 supported mechanical
  families and412 mechanical families/369 dependence blocks are unchanged.
- Federation joins/leaves/invite exchange now use the **body room ID as authoritative**
  for room-version semantics and event construction. Removing the URI argument is not
  universal URI/body rejection, XSS evidence or a complete cross-room auth repair.
  Matched signed transport, version/event helpers and actual ACL/auth gates remain essential.
- Exact outbound policy defaults are **[] plus0.0.0.0/::**, not the sample private-network
  ranges. Deprecated federation-only ranges do not populate the new push/key-revocation
  policy. Literal-IP and direct DNS enforcement are bounded; HTTP proxies receive the URI
  and HTTPS CONNECT receives the hostname, leaving proxy-side destination resolution/policy
  outside the local resolver. Retain actual authenticated push and invitation consumers,
  constrained methods/bodies and deployment configuration instead of universal SSRF claims.
- Well-known resolution gains50*1024 bounded streaming and no retry on size failure;
  chunk writes precede threshold checks, so no exact total-memory ceiling. Its two sibling
  downloaders already enforced supplied optional limits before. Their reader/error migration
  introduces **missing raise → unassigned length** after concerns; preserve both nonrepair
  exclusions and do not transfer their error path to the independently handled resolver.
- Push wildcard compression mitigates contiguous runs only. Old explicit bracket-class
  matching becomes literal bracket text under the new converter; a retained [ab]* /apple
  source witness supports **unresolved_contract_regression**, with final grammar/eligibility
  pending. Keep this paired-negative deferral separate from omitted helper context.
  Custom rules require authentication and the bulk evaluator skips own-sender events;
  real triggering needs an applicable other-sender event. No regex or timing test runs.
- Remote media placement/fetch/fallback/cleanup uses request or persisted origins and
  locally generated random filesystem suffixes. No attacker-selected complete filename or
  unrestricted overwrite/read/delete claim. Local-media random IDs, DB/admin lookup gates,
  encoder types and date/random URL-cache IDs do not inherit the remote advisory's delivery.
  Legacy reads need existing cache/provider files; cleanup needs a persisted origin and later
  cleanup. The server-name validator is newly installed in the media parser, not the old
  enforcement operation there. Component/jail checks are lexical/POSIX, not symlink/race proof.
- Retained **34 new inert texts in three files**:
  CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_018.json SHA256
  **06042beef14765eaef9902fc4eb94aeec3657846bcac81a4467aa2595188065a**;
  CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_018_POLICY.json SHA256
  **ec4392e00e37b8e5941dccd4222eefa925d3753e1f46abf212de0ffccbf4b1da**;
  CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_018_ADVISORIES.json SHA256
  **38c76d8fcad31ef14c2e2571d0e7f0a4778ada1cb34c834eee181224487f2c2f**.
  Complete advisory JSON snapshots are hashed collection-time context, not immutable
  historical/deployed-version proof. Total **31 supplemental files /289 embedded texts**,
  standalone enum template and seven full mutable snapshot API responses.
- Batch018 SHA256 **1d8d4acc3888fe59a403772093acaf82158b3306dc4e7f4746cb183a001f8884**.
  **1,697 current anchors**, including161 new anchors, resolve uniquely. Both selected
  spans remain verified; all prior batches and the complete ledger remain unchanged.
- **58 own audit-tool tests pass**, including exhaustive null-category coverage and
  rejection of clean-negative promotion for missing-raise paths or the glob feature loss.
  Reproduce discovery refresh/check and consolidation build/check after final fingerprinted
  edits. All45 protected release inputs remain unchanged. No Synapse,
  Twisted, network/DNS/proxy request, event/URL/path/regex parser, media/storage/cleanup
  operation, dataset/dependency program or upstream test executes. No substantive held-out
  review, training/evaluation or publication occurs.

## Historical verified continuation: 25 October 2026, batch018

Training discovery remains complete at **742 /742**, **0 remaining**. The current
append-only ledger has **808 events**, **456 supported /208 ambiguous /78 proposed
exclusions**, draft **v0.42 /113 leaves**. The reporting hierarchy remains the
pending **v0.1 /25-parent** proposal. All **433 current consolidation proposals**
remain unapproved; **309 training candidates** still need deeper review:

- 6 conditional retain proposals;
- 191 missing-context deferrals;
- 70 existing-contract deferrals;
- 87 selected-attribution deferrals;
- 11 explicit paired-negative deferrals;
- 34 security-boundary and 3 non-style task-scope deferrals;
- 25 proposed feature exclusions and 6 proposed nonrepair exclusions.

All broad incomplete-case/state/context leaves, all pandas, all Keras, all Scrapy,
all Black, all Spirit, all Thefuck and all Synapse candidates have current proposals.
Next inspect all **20 remaining Ansible training candidates**, including every status
and unclassified case, alongside its five already-reviewed broad-leaf cases. Establish
matched old module/platform/configuration duties, selected effects and actual lower-trust
delivery; advisory/fix labels are not issue counts.
Preserve selected attribution, bounded negatives and dependence. Read exact old contracts
before inferring defects from new tests, API consistency or security provenance.

Use CATEGORY_AUDIT_CONSOLIDATION_REPORT.md and CATEGORY_AUDIT_CONSOLIDATION_REVIEW.md.
Retain the common bounded before-only detection proposal; numerical budget and
runtime/API knowledge policy remain unfrozen. Adjudication sources, helpers, tests,
after code and answers must not become selectively injected detection inputs.
Continue the same checks for supported candidates; preserve all prior reviews and
append changed discovery decisions. Researcher approval is not ready, and independent
issue counts and held-out category adjudication remain pending.

Reproduce with `python3 CATEGORY_AUDIT.py refresh` / `check`, then
`python3 CATEGORY_AUDIT_CONSOLIDATE.py build` / `check`. The discovery queue is
correctly empty; use the exhaustive consolidation queue for continuation.

## Consolidation batch019: complete Ansible contract review — 25 October 2026

- All20 remaining Ansible training candidates now have current proposals in12
  mechanical families: **9 missing-context /2 existing-contract /8 paired-negative
  /1 nonrepair exclusion**. With the earlier five broad-leaf cases all25 are covered.
  Current coverage is **453 /742**, **289 remaining**, **457 historical records**.
- Six chroot/jail/zone rows share the established guest-symlink→host-file boundary.
  Guest dd moves path resolution into isolation for ordinary safe names, but all new
  shell operands are unquoted, breaking accepted space-containing paths. Fetch reads
  only one buffer and discards the remaining stdout drained by communicate, truncating
  larger ordinary files. Keep bounded security repair and introduced functional
  failures distinct. Do not invent attacker control of the host-shell command.
- PAM tail deletion retains a singleton head failure; record residual failure, not
  supported introduction. Banner parser retains a framing newline that the desired
  object need not contain, breaking an old no-change fixture's idempotence. Do not
  assign this parser concern independently to every companion function.
- Three append-only revisions preserve all808 old events: Python2 UTF-8 env lookup
  becomes supported under exact wrapper/rendering context; collection version becomes
  ambiguous because old schema requires string semver rather than promising malformed
  metadata tolerance; supported CLI delimiter duty is narrowed to documented existing
  local archives, without claiming old direct positional URL support from new tests.
  Ledger **811 events /742 unique**, **456 supported /208 ambiguous /78 exclusions**,
  SHA256 **a8458c2712f92ddee97ecf55a8c85c861a310552b024ceb487949d2f4e3cfb11**.
- API pagination needs origin-rooted API-prefixed continuation links and exact base
  mutation. POWER CPU fixtures establish old platform support/counts; architecture
  must be supplied. UNC joining preserves roots but old CLIXML tests do not establish
  a UNC promise. Bare subscription quantity is optional; old docs, matched main/helper
  and attributed two-socket report establish its contextual witness. Placeholder
  wording is nonrepair; alphabetical diagnostics lack an established old contract.
- Batch019 SHA256 **3b68636cf5c41bcaf42a6330866e289e3fdce5be3967d83c0e5a6ab755a81d95**.
  Separately pinned supplemental files (the45 released-input lock is unchanged):
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_019.json:
    **165f8df6d74c5e8efebae48ce6da5922507d1d196f45ea3760e05b679ad1b170**;
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_019_RUNTIME.json:
    **5b6df00e394bf71acac94e1347debdaa8aadd8bb36f53c5f41ca2c711464f1f4**;
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_019_CONTRACTS.json:
    **df17ec119f3f01562fca95ea2f815c5cefab1e96fa6d9ad891b8e941f52010e9**;
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_019_FACTS.json:
    **00b59b9f166d2ea87620bb566d5c7b1d5f300b9452e1eb86e924ce0a99c8fe0d**;
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_019_ISSUES.json:
    **19311fe5bfb6c42fd9798b1b41ff62b3b4f8d3c9e44bde8e5bfcf0897fa4cc12**.
- Current evidence: **1,832 unique-resolving anchors /36 supplemental files /321
  embedded texts**, standalone enum template and nine complete mutable API-response
  snapshots. Collection-time reports and historical dependency tags are not deployment
  proof; helper/test/source context stays adjudication-only.
- All Ansible/dependency programs, shells/transfers/isolation, PAM/device, rendering/
  environment, archive/collection, facts/subscription, parsers and upstream tests stay
  inert. Own audit tooling alone executes; no failures above are runtime reproductions.
- Own validator suite: **61 tests passed**, including exhaustive null-category
  coverage, eight explicit after-failure deferrals and append-only contract revisions.
  Run refresh/check/build/check after the final fingerprinted documentation changes.

## Historical continuation: 25 October 2026, batch019

Training discovery remains **742 /742**, **0 remaining**; draft **v0.42 /113 leaves**
and pending **v0.1 /25-parent** hierarchy are unchanged. The811-event ledger has456
supported /208 ambiguous /78 proposed exclusions. Current consolidation proposals:

- 6 conditional retain;
- 200 missing-context;
- 72 existing-contract;
- 87 selected-attribution;
- 19 paired-negative;
- 34 security-boundary and3 non-style task-scope deferrals;
- 25 feature and7 nonrepair exclusion proposals.

All **453 current proposals** remain unapproved; **289 candidates** need deeper review.
All broad incomplete-case/state/context leaves and all pandas, Keras, Scrapy, Black,
Spirit, Thefuck, Synapse and Ansible training candidates have current proposals.
Next inspect all **18 Waitress training candidates**, including every status and null
category. Establish exact old HTTP/parser/server contracts, lower-trust delivery and
selected attribution; fix/advisory names and mechanical groups are not issue counts.

The common before-only input proposal remains unfrozen for numerical budget and
ordinary API/runtime/tool knowledge. After code, helpers/callers, labels, tests,
advisories and answers stay adjudication-only. Preserve all prior authored batches,
ledger prefixes, canonical bytes/splits and45 protected inputs. No held-out substantive
review, publication, model training/evaluation or approval occurs.

Reproduce: `python3 CATEGORY_AUDIT.py refresh` / `check`, then
`python3 CATEGORY_AUDIT_CONSOLIDATE.py build` / `check`; run the own
`CATEGORY_AUDIT_CONSOLIDATE_TEST.py` validator suite. Use the consolidation queue,
not the correctly empty discovery queue, for continuation.

## Consolidation batches020–021: complete Waitress review — 25 October 2026

- Batch020 covers all **18 Waitress training candidates**, including eight null-category
  components, across **four mechanical families**. Proposals: **7 security-boundary
  /3 missing-context /3 paired-negative /2 selected-attribution /3 nonrepair**.
  Batch021 revalidates the full three-case socket leaf after finding a residual worker
  path: current Waitress totals are **7 security-boundary /2 missing-context /4 paired-
  negative /2 selected-attribution /3 nonrepair**. No newly adjudicated independent issue
  count or approved eligibility follows.
- RFC-permitted LF acceptance is security-relevant only with differential frontend
  forwarding/reuse. Exact old backend consumed-offset/queue behavior is retained;
  actual frontend configuration and victim/cache/auth consequences stay unsettled.
  Chunk-only LF hardening does not inherit header or TE exploitability. Early after
  rejects valid chunk CR/LF split across reads; a different-after sibling buffers it.
  Same-before source does not make that early after regression a prior defect here.
- Old configured max-header docs establish functional limit duty separately from TE
  selection. New completed-header accounting adds the full accumulated index to an
  already counted prefix:100-byte header,60+40 split,limit150 becomes160 and returns431.
  Record an **introduced** under-limit valid-stream failure. Default recv/limits and
  actual resource impact prevent inventing unbounded input or a separate proven DoS.
- Stricter16789 field grammar rejects malformed ASCII controls but permits OBS_TEXT.
  Matched Python3 Latin1→Unicode plus unrestricted TE strip still removes U+0085,
  choosing chunked where a relevant frontend may choose CL. This is a **residual**
  failure of the broader framing/whitespace contract, not an introduced grammar defect.
- New2022 hex/extension regexes use dollar anchors: a terminal bare LF in a chunk line
  can pass match and int whitespace handling on the real body path. Preserve residual
  failure, not a universal numeric-grammar negative. The analogous CL terminal-LF
  hypothesis is blocked upstream by get_header_lines; no reachable bypass is claimed
  there merely from isolated regex semantics. Historical CPython tag is comparison,
  not installed-version proof. No regex/numeric/parser program executes.
- Default select-based main loop snapshots numeric fds and only recovers EINTR; old
  worker send may close a disconnected socket before select and terminate availability.
  Full-response-reading proxies reduce exposure. NewFalse worker eager/high-watermark
  calls are repaired with the coherent helpers/sink. New defaultTrue forwarding alone
  is enabling plumbing, not an old dropped-policy defect or another independent issue.
- Subsequent caller review found **service→send_continue→_flush_some()→send(defaultTrue)**
  remains after. A completed first request plus following partial Expect:100-continue
  headers in one read can defer continuation until the service worker finishes, without
  assuming nondefault lookahead. That worker can still close under the same disconnect/
  select interleaving. Batch021 changes send to an explicit **residual paired-negative
  deferral**; the two correctlyFalse-controlled entries retain narrow missing-context
  proposals. Preserve batch020 and do not inherit sibling call-site blame.
- Equivalent quote-regex relocation retains explicit matches.end checking. ErrorTask
  already closes; new announcement is not TE repair and no old consumer failure is
  established here. Main-loop-only lock-wrapper forwarding is likewise nonrepair.
- All discovery decisions and complete ledger remain **811 events /742 unique**, **456
  supported /208 ambiguous /78 exclusions**, SHA256
  **a8458c2712f92ddee97ecf55a8c85c861a310552b024ceb487949d2f4e3cfb11**.
  Batch020 SHA256 **83efd9d9de1ad79d6d8c48c513c266110ad6c84e2e723e2f909e71df059d7bf6**;
  batch021 SHA256 **3e98f948f607c0f4f53df8393479b5703dfc77bbd19d5768b406b3b1b51f73d7**.
- Four separately pinned evidence files,35 texts:
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_020.json:
    **c8a400168464d6f5a0a35a5aa9a2d86568d5a88540f99f47573e90b1ac05fa4d**;
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_020_ADVISORIES.json:
    **47be06709cee7e59f2986006ba72323a41c5b36ca1c2c23e307684d699616292**;
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_020_RUNTIME.json:
    **72166ca7549e83b021c507a66068c9f7bd96001a631afd2824fc29b7c15e00c7**;
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_020_LIFECYCLE.json:
    **b53b455f8d55f77188fd5b69990584ab48297c82822f963101dae7dcdc961094**.
- Current inventory: **1,977 unique-resolving anchors /40 supplemental files /356
  embedded texts**, standalone enum template, plus preserved complete API-response
  snapshots. All Waitress/parser/regex/numeric/socket/server/proxy/network/thread,
  dependency/application programs, payloads and upstream tests stay inert. Source
  deductions are not reproduced results. No held-out substantive review occurs.
- Own validator suite: **66 tests passed**, including exhaustive eight-null-case
  coverage, after-failure deferrals, preserved authored history and complete socket-leaf
  revalidation. Run refresh/check/build/check after final fingerprinted edits.

## Latest continuation: 25 October 2026, batches020–021

Training discovery remains complete: **742 /742**, **0 remaining**; draft **v0.42 /113
leaves** and pending **v0.1 /25-parent** hierarchy are unchanged. All **471 current
consolidation proposals** remain unapproved; **271 candidates** need deeper review;
**478 historical records** preserve all authored metadata revisions. Current proposals:

- 6 conditional retain;
- 202 missing-context;
- 72 existing-contract;
- 89 selected-attribution;
- 23 paired-negative;
- 41 security-boundary and3 non-style task-scope deferrals;
- 25 feature and10 nonrepair exclusion proposals.

All broad incomplete-case/state/context leaves and all pandas, Keras, Scrapy, Black,
Spirit, Thefuck, Synapse, Ansible and Waitress training candidates have current proposals.
Next inspect all **17 Radicale training candidates**, including every status and null
category. Establish old storage/path/authentication/request duties, lower-trust delivery
and selected attribution. Preserve bounded negatives and source-version dependence.

The common bounded before-only proposal is unfrozen for numerical budget and ordinary
runtime/API/tool knowledge. Adjudication helpers/callers/globals, after, labels, tests,
advisories and answers never become selectively injected detection inputs. Independent
issue identities, final eligibility and researcher approval remain pending. Preserve all
prior authored batches, complete ledger, canonical bytes/splits and45 protected inputs.

Run own `CATEGORY_AUDIT_CONSOLIDATE_TEST.py` validator tests, then
`python3 CATEGORY_AUDIT.py refresh` / `check` and
`python3 CATEGORY_AUDIT_CONSOLIDATE.py build` / `check` after final fingerprinted edits.
Continue from the consolidation queue; the discovery queue is correctly empty.

## Consolidation batch022: complete Radicale review — 25 October 2026

- All **17 Radicale training candidates /two mechanical families** receive proposals:
  **5 missing-context /11 selected-attribution /1 paired-negative**. There are no null
  categories in this repository. Sixteen storage rows share the Windows conversion
  family; the login-regex row is another family. These are not independent issue counts.
- Exact old owner regex templates, htpasswd literal login admission and request rights
  filtering establish a conditional cross-owner grant boundary for a successfully
  authenticated, already provisioned metacharacter login under owner policy. Escaping
  interpolation data repairs that narrow route. Default-none rights, all custom capture
  substitutions, anonymous access and actual deployment do not inherit that claim.
- Five selected node/leaf/children functions directly convert logical DAV paths using raw
  platform joins. Matched old sanitize/from_path/exists and XML resourcetype/href consumers
  establish Windows classification/name effects and justify five ambiguous→supported
  discovery revisions. Historical CPython2.7.10/3.4.3 path text is comparison, not runtime
  deployment proof. Configuration, backend, OS access, rights and response gates matter.
- Eleven selected consumers instead use an inherited absolute filepath API. Nine supported
  discoveries become ambiguous for selected attribution; two ambiguous timestamp getters
  stay ambiguous despite traced conditional Last-Modified output. The bad logical-to-host
  conversion is in the producer, not every correct old mkdir/read/write/delete/suffix/stat
  operation. Preserve contextual project security without manufacturing local bug counts.
- Multifilesystem after is_leaf checks the validated directory but original relative
  `path + ".props"`; CWD!=FOLDER can misclassify an ordinary valid stored leaf. Record an
  **introduced contract regression** and explicit paired-negative deferral. Do not claim
  universal path confinement, symlink/race protection or all HTTP error handling.
- Matched inherited `_parse` returns a dict; multifilesystem text accumulates string keys
  then sorts them as Items. This **pre-existing residual** obstructs nonempty recognized
  calendar serialization/disclosure and item deletion. Empty/unrecognized-component
  directory witnesses support narrower GET metadata or collection mutation. DELETE still
  evaluates `item.etag` in its tuple even when If-Match is absent/default `*`; no bypass of
  that scan is assumed. Separate item-name admission and other output paths remain open.
- Fourteen appended discovery revisions preserve all811 old events. Ledger now **825
  events /742 unique**, **452 supported /212 ambiguous /78 exclusions**, SHA256
  **82a7ed0370f99633102502587bb7f84cfd867aee911c754570fb24bfffa40229**.
  First811 events retain
  **a8458c2712f92ddee97ecf55a8c85c861a310552b024ceb487949d2f4e3cfb11**.
  Batch022 SHA256 **682db03073182664483cd5a5d08a00b99948bb7adb660c4c89b445d311c0d856**.
- Five new separately pinned evidence files,33 texts:
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_022.json:
    **a26133a1fda0cd1594f4b54b97b9678b91429513db9abaffcbdf2a29d9748bfc**;
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_022_DELIVERY.json:
    **e19243f9c2c258181a67d660299090546e3aa22ee0b783e07e6fec285440fb45**;
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_022_STORAGE.json:
    **db80340fdf86d46a528d507af6b913e74a4d92a392887ecbea40e56fb87107be**;
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_022_ADVISORIES.json:
    **997c3e7ccffe5260d3aed4d17cecb7f089a759987fda37296755a6c24ca8cb87**;
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_022_POLICY.json:
    **b8617d57846197b4d275e414eeb62f1ab2fa394a94e3110d412c29c88ce95590**.
- Inventory: **2,237 unique-resolving historical anchors /2,187 current anchors /45
  supplemental files /389 embedded texts**, plus the standalone enum template. All
  Radicale/authentication/regex/ConfigParser, HTTP/DAV/XML/calendar/path/Windows/filesystem/
  storage, dependency/application programs, payloads and upstream tests stay inert.
  Findings are source deductions, not reproduced results. No held-out substantive review.
- Own validation adds exhaustive mixed-source selection, CVEfixes evidence isolation,
  explicit after-failure deferral, append-only ledger/source/category preservation and
  residual-consumer negative checks. **71 own-tool tests passed** in208.598s. Run final
  refresh/check/build/check after these fingerprinted report edits.

## Latest continuation: 25 October 2026, batch022

Training discovery is **742 /742**, **0 remaining**; draft **v0.42 /113 leaves** and
pending **v0.1 /25-parent** hierarchy remain unchanged. Current consolidation coverage
is **488 /742**, with **254 remaining** and **495 historical records**. Proposals:

- 6 conditional retain;
- 207 missing-context;
- 72 existing-contract;
- 100 selected-attribution;
- 24 paired-negative;
- 41 security-boundary and3 non-style task-scope deferrals;
- 25 feature and10 nonrepair exclusion proposals.

All broad incomplete-case/state/context leaves and all pandas, Keras, Scrapy, Black,
Spirit, Thefuck, Synapse, Ansible, Waitress and Radicale candidates have current proposals.
Next inspect all **16 OpenStack Glance training candidates**, including every discovery
status and null category. Establish old API/authorization/image/storage/request duties,
realistic lower-trust delivery and exact selected attribution; preserve bounded negatives
and source-version dependence.

The uniform bounded before-only numerical budget and ordinary runtime/API/tool-knowledge
policy remain unfrozen. Adjudication helpers/callers/globals, after, labels, tests,
advisories and answers never become selectively injected detection inputs. All
researcher decisions, eligibility and independently adjudicated issue identities remain
pending; approval is not ready. Preserve all prior authored batches/evidence, complete
ledger history, canonical bytes/splits and45 protected released inputs.

## Consolidation batch023: complete OpenStack Glance review — 25 October 2026

- All **16 Glance training candidates /three mechanical families** receive proposals:
  **7 missing-context /8 security-boundary /1 paired-negative**. No null categories exist
  here. Shared CVEs/backports and API versions do not establish independent issue counts.
- Exact old DB visibility permits public/shared images while mutation requires admin or
  owner. The mutating decorator checks read_only, not ownership; generic action policy
  uses an empty target/permissive defaults. v1/v2 backend deletion precedes the registry/DB
  owner check. A readable non-protected image and authenticated nonowner with action-policy
  admission establish the immediate destructive route; the after places DB/registry
  mutations first. No anonymous admission, protected-image bypass or deployed configuration
  is inferred from advisory language.
- v2 before and after pass builtin **id**, not image_id, to store helpers. Immediate
  deletion ignores that argument and still deletes by URI, so the typo does not prevent
  the old authorization witness. Delayed work is named by str(image_id): two pending
  authorized operations in one process collide on the wrong work filename, which the
  scrubber then uses as registry image ID. Record an explicit **residual contract failure**,
  not an introduced ordering regression or a clean paired negative.
- Six Swift add/get rows across three versions have matched client-error propagation:
  backend409 inside the object/chunk PUT try becomes HTTP409 with Duplicate text;
  backend404 for an active readable nonzero-size image becomes HTTP404 with NotFound text.
  Single-tenant service user/key are serialized in the private URI; quoting is not
  redaction. Exact get_store_uri delegates to the private store URI despite its docstring.
  Earlier registry duplicate rejection, pre-try container setup, zero-size GETs and denied
  images are not these witnesses. Backend failure state is required, not arbitrary
  attacker ability to cause it. Essential producer/caller context still defers retention.
- Three delete diagnostics instead pass to immediate wrappers that absorb NotFound and
  log their own raw URI. Those raw caller sinks remain after the selected error becomes
  constant. An actual unauthorized log/exception audience remains unresolved; do not
  borrow GET response delivery or certify end-to-end redaction.
- Two multi-tenant ACL-only paths normally omit passwords/use a separate context token;
  single-tenant sibling credentials do not establish admitted secret input there. Three
  parser-log rows require malformed private URI provenance and unauthorized readership;
  mainline DEBUG must be enabled, while older ERROR is not automatically public. Attacker-
  supplied already-known credentials and literal user:pass guidance are not disclosures
  of service secrets. Keep both audience and backend/provenance questions explicit.
- All14 Swift rows remain one CVE-linked family. The v2 public record calls its issue an
  incomplete v1 fix, so separate API/CVE identities are not statistical independence.
  Preserve the three mechanical families and all source-version dependence; independently
  adjudicated issue counts remain unknown.
- No discovery revision: **825 events /742 unique**, **452 supported /212 ambiguous /78
  exclusions**, SHA256 **82a7ed0370f99633102502587bb7f84cfd867aee911c754570fb24bfffa40229**.
  All prior events and authored batches/evidence remain unchanged.
  Batch023 SHA256 **c13bb5c6de6463a448ccc4aabe4e1b9e0b3981d44937d188a5798d13465fd5b5**.
- Three new separately pinned evidence files,51 texts:
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_023.json:
    **42ff7f5ebfa9e01488a7f465383c2c3bb1fce9b503d430ebd61438fbde72c1e4**;
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_023_DELIVERY.json:
    **4b81328339765f31c97d8df56336e3ba2908b5a7e5e2ab005cde70600eb65918**;
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_023_CONTRACTS.json:
    **538de89512cfd8b5b09134e8c6696c41b1fabd309a474665d2bc7b5ed57c98b0**.
- Inventory: **2,411 unique-resolving historical anchors /2,361 current anchors /48
  supplemental files /440 embedded texts**, plus the standalone enum template. Public
  CVE JSON snapshots are complete retained mutable records, not deployed-version proof.
  All Glance/auth/policy, DB/SQL, Swift/backend/storage, HTTP/WSGI/URL/parser, application/
  dependency programs, requests, payloads and upstream tests stay inert. Source deductions
  are not reproduced results; held-out data receives integrity checks only.
- Own validation adds exhaustive authorization/ACL/parser selection, explicit residual
  delayed-delete deferral, unresolved-log-audience retention rejection and after-caller
  raw-URI negative checks. **75 own-tool tests passed** in237.254s. Run final
  refresh/check/build/check after these fingerprinted report edits.

## Continuation checkpoint: 25 October 2026, batch023

Training discovery is **742 /742**, **0 remaining**; draft **v0.42 /113 leaves** and
pending **v0.1 /25-parent** hierarchy are unchanged. Consolidation coverage is **504 /742**,
with **238 remaining** and **511 historical records**. Current proposals:

- 6 conditional retain;
- 214 missing-context;
- 72 existing-contract;
- 100 selected-attribution;
- 25 paired-negative;
- 49 security-boundary and3 non-style task-scope deferrals;
- 25 feature and10 nonrepair exclusion proposals.

All broad incomplete-case/state/context leaves and all pandas, Keras, Scrapy, Black,
Spirit, Thefuck, Synapse, Ansible, Waitress, Radicale and Glance candidates have current
proposals. Next inspect all **11 Vyper training candidates**, including every status and
null category. Establish old compiler/type/ABI/runtime contracts, realistic lower-trust
delivery, exact selected attribution and bounded paired negatives.

The uniform bounded before-only numerical budget and ordinary runtime/API/tool-knowledge
policy remain unfrozen. Adjudication helpers/callers/globals, after, labels, tests,
advisories and answers never become selectively injected detection inputs. All researcher
decisions, eligibility and independent issue identities remain pending; approval is not
ready. Preserve all prior authored history, canonical bytes/splits and45 protected inputs.

## Consolidation batch024: complete Vyper review — 25 October 2026

- All **11 training candidates /three mechanical families** are reviewed, including all
  statuses and six null categories (five exclusions and one ambiguous tuple converter).
  Proposals: **3 missing-context /5 nonrepair exclusions /1 selected-attribution /1
  security-boundary /1 paired-negative**. Every825 discovery event remains unchanged;
  ledger SHA256 **82a7ed0370f99633102502587bb7f84cfd867aee911c754570fb24bfffa40229**.
- Concat's byte-offset full-word copy can overrun its old logical allocation into live
  EVM memory in supported caller/frame layouts. After reserves an extra physical word
  without increasing logical type capacity. Establish this with the exact old copy API,
  type-size rounding, allocator and internal-function/return consumers, rather than a
  new fixture or advisory alone. Not all uses corrupt live data; no deployed victim or
  host-process memory corruption is claimed.
- Short equal-capacity bytes equality ignores length and includes dirty padding. After
  uses hashing over logical data/length; the ordinary collision-resistance assumption
  bounds this negative. The old hash helper already uses that logical span, so its
  refactor is not a separate old defect. Three retired-encoding edits preserve surviving
  pointer/setter behavior; incoming-argument decoding already clamps supported types.
  These five rows retain nonrepair exclusions and null categories.
- The old dynamic JSON_ABI clamp suppression and raw-return-pointer exposure are genuine
  local validation duties under lower-trust external returndata. Their exact setter,
  type, JSON-signature and complex-expression consumers are essential adjudication
  context. Passing new expression metadata/native convention through the wrapper does
  not establish another selected old-wrapper defect.
- **Explicit paired-negative deferral:** after `_unpack_returndata` uses expression-inferred
  bounds for the CALL/STATICCALL output length, while `_pack_arguments` still allocates
  from the legacy JSON output bound1. For no arguments and inferred Bytes[96], the
  legacy ABI output bound96 plus method-id padding allocates128 bytes; the new ABI
  output size is160. Consecutive internal expansion places the native128-byte tuple
  buffer at rawbuf+128. Its length store precedes copying source data ending at
  rawbuf+159, overwriting the third source word. Exact source arithmetic and store order
  support `unresolved_contract_failure`, not an unqualified clean negative. Since old
  JSON dynamic-return handling already truncated/left data unchecked, do not assert an
  established introduced regression. No compiler, EVM, callee or contract executes.
- Tuple member conversion repairs the helper's old/native representation mismatch,
  but accepted preexisting tuple-converter caller reachability and a lower-trust security
  effect remain unresolved. A newly added strict-decoder caller is not an old duty or
  old reachability witness. Keep its null category, ambiguous discovery and explicit
  security-boundary deferral; no consequence-only relabelling or new leaf follows.
- Preserve eleven rows/three mechanical families as review units, not independent issues.
  No canonical IDs, bytes, splits, earlier events or authored batches are rewritten.
  Batch024 SHA256 **3422321ccfa23bb9e4c4fdd504e76c6e8be4682ba678d1abe1ee82ce3a371e7c**.
- New supplemental pins, separate from the protected release-input lock:
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_024.json:
    **e5b907ca61e5422122cd070281b24bc8c6fb994282dcb12a9c740fa650ec93ec**;
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_024_DELIVERY.json:
    **c7c1731e04c6ab482c427313e3337b16d28c767c0cb1a62cc85be1830a8d2ffc**;
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_024_PEERS.json:
    **b4a05c3287da867f77c1d302016e5286700b203e2fef3faa86c3b4f7006ba13e**.
- Inventory: **2,496 unique-resolving historical anchors /2,446 current anchors /51
  supplemental files /506 embedded texts**, plus the standalone enum template. The
  new66 texts include12 verified training archive peers and three complete mutable CVE
  snapshots, not deployed-version proof. All compiler/ABI/AST/IR/type/memory/crypto/EVM/
  contract, parser, dependency/application programs and upstream tests stay inert.
- **79 own-tool tests passed** in287.983s. Focused checks reject omitted CVEfixes/null
  rows, hiding the explicit after-capacity failure, promoting equivalent refactors and
  borrowing sibling security delivery for the tuple converter. Run final
  refresh/check/build/check after these fingerprinted documentation edits.

## Continuation checkpoint: 25 October 2026, batch024

Training discovery remains **742 /742**, **0 remaining**; draft **v0.42 /113 leaves** and
pending **v0.1 /25-parent** hierarchy are unchanged. Consolidation coverage is **515 /742**,
with **227 remaining** and **522 historical records**. Current proposals:

- 6 conditional retain;
- 217 missing-context;
- 72 existing-contract;
- 101 selected-attribution;
- 26 paired-negative;
- 50 security-boundary and3 non-style task-scope deferrals;
- 25 feature and15 nonrepair exclusion proposals.

All broad incomplete-case/state/context leaves and all pandas, Keras, Scrapy, Black,
Spirit, Thefuck, Synapse, Ansible, Waitress, Radicale, Glance and Vyper candidates have
current proposals. Next inspect all **nine Nautobot training candidates**, including
every status and null category. Establish matched old permission/model/API/runtime
contracts, realistic lower-trust delivery, exact selected attribution and bounded
paired negatives. Remaining largest queues then include openapi-python-client8,
tlslite-ng8 and Nova7; repository size is not an independent-issue target.

The uniform bounded before-only numerical budget and ordinary runtime/API/tool-knowledge
policy remain unfrozen. Adjudication helpers/callers/globals, after, labels, tests,
advisories and answers never become selectively injected detection inputs. Researcher
decisions, eligibility and independent issue identities remain pending; approval is not
ready. Preserve prior authored history, canonical bytes/splits and45 protected inputs.

## Consolidation batch025: complete Nautobot review — 25 October 2026

- Review all **nine training candidates /two mechanical families**, including every
  status; this repository has no null categories. Proposals: **3 missing-context /4
  selected-attribution /2 paired-negative**. Eight HTML rows share one coordinated
  fix/CVE family; the repository authorization row is a second family. Neither nine
  functions nor two families are independent issue counts.
- Matched django-filter23.1 returns an ErrorDict. In lockfile-matched Django3.2.23,
  ErrorDict/ErrorList already conditionally escape ordinary field/error data; the two
  filter-message mark_safe replacements do not isolate old XSS on that standard route.
  Likewise RegexValidator always supplies a truthy value-params dictionary, causing
  ValidationError iteration to percent-format a SafeString into ordinary text before
  standard ErrorList/form rendering. Custom alternate unsafe producers/sinks need
  actual old admission contracts. No regex or dependency execution is used to infer it.
- Custom-link and job-button editor data crosses into other object-page readers.
  Plain group names give direct old HTML witnesses; disabled job buttons are still
  rendered. Correct value-wise escaping requires the coordinated plain-render helper,
  not an after consumer combined with an old SafeString-producing backend.
- **Paired negative1, introduced supported new-window regression:** ordinary literal
  ` target="_blank"` is escaped as a format_html operand in a fragment slot. HTML
  unquoted-attribute character-reference handling makes decoded quotes part of the
  target name. It is not reserved _blank; repeated activations can reuse the named
  context instead of forcing a new window. The old Boolean new_window contract and
  grouped/ungrouped true paths supply the previously-correct witness. Record
  `unresolved_contract_regression` and explicit `defer_paired_negative`; no browser ran.
- **Paired negative2, introduced optional-URL regression:** old protected-error handling
  explicitly accepts dependency objects without get_absolute_url and renders a string
  fallback. Django ProtectedError imposes no URL-method requirement. New unconditional
  generator calls raise AttributeError for that accepted helper-domain case before the
  error message is delivered. This is separate from the concrete Manufacturer-name
  security witness: an allowed writer changes a plain name, an existing DeviceType
  PROTECT reference blocks another authorized user's deletion, and the root name is
  marked safe in the resulting flash. The normal built-in witness has URLs and is not
  falsely claimed to exercise the distinct after failure. No plugin or deletion executes.
- The repository helper is not an anonymous-access witness. Exact old permission backend
  treats no-object has_perm as permission for some objects. A normal active user with
  change constrained to repositoryA can identify readable-but-not-changeableB, pass the
  coarse gate and enqueueB if a worker/registered admitted job is available. Matched
  queryset constraints, enqueue and sync/dry-run consumers support the missing target
  restriction. After restrict(user,"change") precedes lookup/func; preserve POST/CSRF,
  worker/job/task-admission and actual operation prerequisites, not arbitrary Git effects.
- Append two discovery revision2 events only:
  - Renderer helper **supported→ambiguous**: backend SafeString downgrade is needed for
    newly changed conditional-escaping consumers, but old link/button sinks ignore its
    marker and old computed fields unconditionally escape(value). No independently
    isolated old helper bypass follows from new consumer duty.
  - Import success message **ambiguous→supported**: concrete DeviceType importer/form/
    model string, permission checks and message-SafeData serialization/template display
    are now pinned. Old JSON/YAML external-library-compatible data can originate with
    a less-trusted file/catalog author and reach a different importing operator/browser.
    The flash belongs to that operator, not automatically another user's session;
    self-authored markup alone is not a security boundary. Require all add permissions,
    accepted data and successful object admission.
- Preserve all825 previous ledger events byte-for-byte, every earlier authored batch,
  categories/families/selected hashes, canonical bytes/splits and45 protected inputs.
  Current ledger: **827 events /742 unique /452 supported /212 ambiguous /78 exclusions**,
  SHA256 **8b0f0e74c6a9a96b62ac9ca15164b9eeaceb87d10e5b070fc1d8c52fa3a6f359**.
  Batch025 SHA256 **7e7a68511699ef27bedd097da6f462fa7c2edc07bcda7fc7a54a90dce897a1f1**.
- Six new supplemental pins, separate from the protected release-input lock:
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_025.json:
    **3d51bb5070cbf54194ba53296b65c58bdda01d948e0052b381500518bd315692**;
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_025_PEERS.json:
    **466a49dc6029cf8449e374ea71d8e594d28fa078d1d980ea5038ab858fa672c7**;
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_025_RUNTIME.json:
    **11eda7246670dfd5838b4c6cca6076c561b792926d42eaa9378a23513b07fb90**;
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_025_DELIVERY.json:
    **a677644d078ed63c737f7edc22e886ffa7223f439e938936e77361673efacf0a**;
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_025_ACTIONS.json:
    **056f356428cae0ceaf814808a225b1cc773d860a4ee412444de017fd80c179eb**;
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_025_MESSAGES.json:
    **cd366bb6256290ad127da412171e4b0f53d2acfd21e83d86f9febc0af828dcf7**.
- Inventory: **2,596 unique-resolving historical anchors /2,546 current anchors /57
  supplemental files /595 embedded texts**, plus the standalone enum template. New89
  texts include16 verified training peers and two complete mutable CVE snapshots, not
  deployed-version proof. Retained dependency text matches the historical lockfile;
  CPython3/HTML source contracts remain explicit semantic comparisons, not executed
  interpreter/browser tests. No Nautobot/Django/Jinja/filter/HTML/browser/regex/auth/
  ORM/DB/Git/Celery/dependency/application program, request, payload or upstream test ran.
- **84 own-tool tests passed** in310.879s, covering exhaustive selection, explicit
  introduced after failures, attribution promotion rejection, two append-only revisions
  with unchanged source/category/family identities and the file-author/operator boundary.
  Run final refresh/check/build/check after these fingerprinted report edits.

## Previous checkpoint: 25 October 2026, batch025

Training discovery remains **742 /742**, **0 remaining**; draft **v0.42 /113 leaves** and
pending **v0.1 /25-parent** hierarchy are unchanged. Consolidation coverage is **524 /742**,
with **218 remaining** and **531 historical records**. Current proposals:

- 6 conditional retain;
- 220 missing-context;
- 72 existing-contract;
- 105 selected-attribution;
- 28 paired-negative;
- 50 security-boundary and3 non-style task-scope deferrals;
- 25 feature and15 nonrepair exclusion proposals.

All broad incomplete-case/state/context leaves and all pandas, Keras, Scrapy, Black,
Spirit, Thefuck, Synapse, Ansible, Waitress, Radicale, Glance, Vyper and Nautobot candidates
have current proposals. Next inspect all **eight openapi-python-client training candidates**,
including every status and null category, using matched old generator/schema/template/
runtime contracts, realistic lower-trust delivery, selected attribution and bounded
paired negatives. Largest subsequent queues include tlslite-ng8 and Nova7; counts do
not optimize an independent-issue target.

The uniform bounded before-only numerical budget and ordinary runtime/API/tool-knowledge
policy remain unfrozen. Adjudication helpers/callers/globals, after, labels, tests,
advisories and answers never become selectively injected detection inputs. Researcher
decisions, eligibility and independent issue identities remain pending; approval is not
ready. Preserve prior authored history, canonical bytes/splits and45 protected inputs.

## Consolidation batch026: openapi-python-client — 25 October 2026

All **eight openapi-python-client training candidates /two mechanical families** now have
current proposals, including **six null-category rows**: **1 missing-context /1
selected-attribution /1 paired-negative /5 nonrepair-exclusion**. No discovery revision.

- The old unconstrained title flows through GeneratorData and default Project paths
  into actual create/write/update-delete consumers. A less-trusted spec author can
  influence a different developer's filesystem paths, subject to appropriate existing
  parents, permissions and target existence conditions. After sanitization/casing
  removes title-only lexical separators/dot segments. Explicit operator overrides and
  filesystem symlink/race behavior remain outside that bounded negative.
- Old enum key/value strings occupy an unchanged Python assignment/literal template
  and a concrete source writer. A later developer/application import/use of the
  generated client supplies the code-execution delivery prerequisite; generation and
  formatting alone are not a demonstrated import/execution of the generated client.
- **Introduced after contract regression:** ordered string values `"A"` and `"A\u0301"`
  (second is A plus combining acute) had valid, distinct normalized old Python member
  names and distinct unchanged wire values. After checks duplicate raw keys but inserts
  sanitized keys, so removing the combining mark makes the second overwrite the first.
  The generated enum loses valid wire value A, violating its existing constructor/value
  round-trip contract. Preserve explicit `unresolved_contract_regression` and
  `defer_paired_negative`; do not rely on collisions whose old names were already invalid.
- Residual accepted-string failures remain: spaces/hyphens in assignment names, empty
  member indexing and incomplete quote/backslash/newline literal encoding. In particular,
  prefixing an already-backslash-preceded quote changes escape parity and can expose
  following data as syntax. No payload is compiled/evaluated/imported or regex executed.
- Initializer delegation needs a reference before new virtual default validation, but
  does not independently sanitize its old inverse mapping. Datetime imports match the
  same-version annotations/templates. Optional opt-outs preserve old annotation calls
  and serve a changed union runtime consumer, not an invented old getter duty. Acronym
  range correction is casing, not the old caller's separate source whitelist. Preserve
  six null categories and five explicit nonrepair exclusion proposals.
- The path-fix after helper text equals the subsequent source-fix before helper text.
  This establishes a shared version context, not equality of different selected functions,
  an approved family merge or independent issue counts. Eight rows/two families remain
  mechanical review units. Existing taxonomy/source bytes/splits/prior batches and all
  **45 protected inputs** are preserved; the entire827-event ledger hash is unchanged.
- Batch026 SHA256 **492e058b29429772f731492b8c09b1d9bb04409ae5720c60035aff53861a439e**.
  Four new supplemental pins, separate from the release-input lock:
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_026.json:
    **35bda94234ff3242f27763f530c8deb5191e0420aa63ff6f41c1c6fdcc1fe19c**;
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_026_PEERS.json:
    **080a85d0df873c1e9d994714cd709d4712b0a6250731071ddae93fca73436961**;
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_026_RUNTIME.json:
    **5ef27926a842fe5e306dab29fb8dbe71908a0f66f9b8f05437e56a88586faeec**;
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_026_DELIVERY.json:
    **52e267d0e467b057a2b378a053de0e108f0f237610588ca4d38d6390eb14a1d0**.
- New56 inert texts include six verified archive peers, matched schema/templates/writers/
  consumers, historical dependency/runtime contracts and a stringcase1.2.0 archive member
  read without extraction/installation/import. These are comparisons, not deployed-version
  proof. Inventory: **2,684 historical anchors /2,634 current anchors /61 supplemental
  files /651 embedded texts**, plus the standalone enum template.
- **89 own-tool tests passed** in350.389s. Focused validator checks cover complete selection, explicit after-regression
  deferral, nonrepair/initializer promotion rejection, unchanged ledger/shared helper
  versions and explicit old/new template references. Findings are source deductions,
  not reproduced results. All generator/schema/parser/template/regex/filesystem/compiler/
  import/formatter/dependency/application/generated programs and upstream tests stay inert.

## Previous checkpoint: 25 October 2026, batch026

Discovery remains **742 /742**, **0 remaining**; draft **v0.42 /113 leaves** and pending
**v0.1 /25-parent** hierarchy are unchanged. Ledger remains **827 events /742 unique**,
**452 supported /212 ambiguous /78 exclusions**, SHA256
**8b0f0e74c6a9a96b62ac9ca15164b9eeaceb87d10e5b070fc1d8c52fa3a6f359**.
Consolidation coverage is **532 /742**, with **210 remaining** and **539 historical
records**. Current proposals:

- 6 conditional retain;
- 221 missing-context;
- 72 existing-contract;
- 106 selected-attribution;
- 29 paired-negative;
- 50 security-boundary and3 non-style task-scope deferrals;
- 25 feature and20 nonrepair exclusion proposals.

All broad incomplete-case/state/context leaves and all pandas, Keras, Scrapy, Black,
Spirit, Thefuck, Synapse, Ansible, Waitress, Radicale, Glance, Vyper, Nautobot and
openapi-python-client training candidates have current proposals. Next inspect all
**eight tlslite-ng training candidates**, including every status and null category,
using matched old protocol/parser/crypto/runtime contracts, realistic lower-trust delivery,
selected attribution and bounded paired negatives. Subsequent large queues include
Nova7, Zulip7 and Shuup7; counts do not optimize an independent-issue target.

The common bounded before-only numerical budget and ordinary runtime/API/tool-knowledge
policy remain unfrozen. Adjudication helpers/callers/globals, after, labels, tests,
advisories and answers never become selectively injected detection inputs. Researcher
decisions, eligibility and independent issue identities remain pending; approval is not
ready. Preserve prior authored history, canonical bytes/splits and45 protected inputs.

## Consolidation batch027: tlslite-ng — 26 October 2026

All **eight training candidates /one mechanical family**, including **seven null-category
rows**, now have current proposals: **4 paired-negative /3 existing-contract /1 nonrepair
exclusion**.

- Matched old TLSKeyExchange processing already randomizes failed, wrong-length and
  invalid-version premaster results. The selected old private decrypt still performs
  secret-dependent prefix/separator work, with actual client-ciphertext admission through
  negotiated static-RSA TLS. Internal None is not itself a network error oracle. Keep
  interpreter/backend, negotiation/admission and measurable observation prerequisites;
  neither remotely exploitable timing nor a recovered key is reproduced or asserted.
- After full scanning/implicit rejection removes only a bounded explicit branch/return
  mechanism. CPython side-channel limitations appear in both selected source and the
  full retained advisory; do not certify constant time or general oracle freedom.
- **Four explicit introduced after-regression deferrals:**
  - PSS sign rejects a valid `k-1` byte encoded message because the new byte adapter
    insists on `k` bytes. At1025 modulus bits, valid EM is128 bytes and signature129.
    Old constructor/importer admission and RFC8017 support this existing input domain.
  - PSS verify instead retains a zero prefix and supplies129 bytes to the128-byte
    maskedDB/H decoder. Preserve the encoded-width contract violation without claiming
    an executed signature or rejection of every possible shifted encoding.
  - Native PKCS1 verify loses its explicit signature-width check: unlike the Python
    base adapter, the native override delegates directly to M2Crypto/OpenSSL. Retained
    compatible native source intentionally accepts leading-zero-shortened signatures.
    Conditional on a valid signature starting with zero, after accepts an encoding old
    code rejected. This is public canonicality, not a new-message forgery or padding oracle.
  - Freshly generated OpenSSL private keys lack d, which after decrypt now reads to
    initialize its rejection PRF. Only PEM parse attaches d; generation does not.
    A valid raw operation can therefore be followed by AttributeError instead of a
    plaintext/rejection result. Parsed native/Python keys have different state.
- The factory helper itself is a nonrepair proposal: old native keys lacked d and were
  already returned intact; new native keys parsed from PEM acquire d but not the other
  conversion fields, so the changed preservation branch adapts to a **new** producer.
- Append four **proposed-exclusion→ambiguous revision2** events, leaving all seven null
  categories unchanged:
  - Python PEM parser: conflicting old private-only versus general factory public-or-
    private format promises require per-backend API-scope resolution. The old static
    rebinding already worked; generic delegation adds public SPKI input.
  - PSS verification: new base helper adds s<n rejection absent from old Python modulo
    processing. The s+n witness requires it still to fitk bytes. A public representative
    standard/admission repair is distinct from the advisory's private-padding mechanism.
  - Raw PKCS1 signing and encryption: exact encoded-block width changes oversized-input
    admission even where the old numeric guard passes. Whether strict invalid-input
    rejection is a supported raw API duty needs actual caller/format scope. Do not force
    a nonrepair exclusion, a new leaf or an after-format failure on an unresolved domain.
- Preserve all827 earlier ledger events byte-for-byte, prior authored batches, original
  selected/category/family identities, canonical bytes/splits and **45 protected inputs**.
  Ledger: **831 events /742 unique /452 supported /216 ambiguous /74 exclusions**;
  SHA256 **9ca57ede950e4495ca81ef3c279a6ff7d312196473e270b47ad37fb68886c5c3**.
  Batch027 SHA256 **8e43cc9c7e4877eb8bd32c71813edab48045cf271d1614a234420d7698a3167c**.
- Four new separately registered supplemental pins:
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_027.json:
    **0cf271f33841bedf22b9de17592ea1835cbb017753e0f32cfc2885982c8284ff**;
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_027_PEERS.json:
    **4998fec9842d68cb17a456f9df0d5773c70ccd594f5e8101cae132d22c4b0b7c**;
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_027_CONTRACTS.json:
    **a786cb7cd989805af98c65a985a733d697a973f20f01ac89f6eb62ee8dfac705**;
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_027_BACKEND.json:
    **7afb56a3867f0452f7a105d8431c2c829fa28ed7368c33ccde71e8fa4fa1b443**.
- New38 inert texts include six verified archive peers, matched old/after TLS/key/helper/
  backend sources, predating RSA/TLS standards, a full mutable advisory API snapshot
  and historical M2Crypto0.27.0/OpenSSL1.1.0l comparisons. Sdist members are read without
  extraction/installation/import; these are not deployed-version proof. Inventory:
  **2,771 historical anchors /2,721 current anchors /65 supplemental files /689 embedded
  texts**, plus the standalone enum template. Four rows/three after integration mechanisms
  and one mechanical family are not independently adjudicated issue counts.
- **95 own-tool tests passed** in297.208s. Validator checks cover exhaustive selection, explicit after-regression deferrals,
  contract/nonrepair promotion rejection, four append-only revisions with unchanged
  identities/prefix, native override reference matching and the full advisory/TLS
  randomization distinction. All inspected TLS/network/crypto/RSA/PSS/padding/PRF/hash/key/
  PEM/ASN1/parser/backend/compiler/dependency/application programs, payloads, timing
  experiments and upstream tests remain inert; deductions are not reproduced results.

## Previous checkpoint: 26 October 2026, batch027

Training discovery remains **742 /742**, **0 remaining**; draft **v0.42 /113 leaves** and
pending **v0.1 /25-parent** hierarchy are unchanged. Consolidation coverage is **540 /742**,
with **202 remaining** and **547 historical records**. Current proposals:

- 6 conditional retain;
- 221 missing-context;
- 75 existing-contract;
- 106 selected-attribution;
- 33 paired-negative;
- 50 security-boundary and3 non-style task-scope deferrals;
- 25 feature and21 nonrepair exclusion proposals.

All broad incomplete-case/state/context leaves and all pandas, Keras, Scrapy, Black,
Spirit, Thefuck, Synapse, Ansible, Waitress, Radicale, Glance, Vyper, Nautobot,
openapi-python-client and tlslite-ng training candidates have current proposals. Next
inspect all **seven OpenStack Nova training candidates**, including every status and null
category, using matched old API/policy/state/runtime contracts, realistic lower-trust
delivery, selected attribution and bounded paired negatives. Other large queues include
Zulip7 and Shuup7; counts do not optimize an independent-issue target.

The common bounded before-only numerical budget and ordinary runtime/API/tool-knowledge
policy remain unfrozen. Adjudication helpers/callers/globals, after, labels, tests,
advisories and answers never become selectively injected detection inputs. Researcher
decisions, eligibility and independent issue identities remain pending; approval is not
ready. Preserve prior authored history, canonical bytes/splits and45 protected inputs.

## Consolidation batch028: OpenStack Nova — 26 October 2026

- All **seven training candidates /five mechanical families** now have proposals:
  **three missing-context /four paired-negative deferrals**. All seven supported
  discovery events/categories remain unchanged; no null categories exist here.
- First injection repair closes ordinary dot-dot traversal but retains the permission
  mismatch between unprivileged realpath and root mkdir/tee. Historical CPython2.7.3
  islink catches failed lstat and may leave a root-only-searchable symlink unresolved.
  This is an explicit **residual after-contract failure**, conditional on lower-trust
  image, service/root privilege difference and accessible outside target.
- Later root readlink `-nm` resolves at writer privilege under retained rootwrap,
  execute and GNU tool contracts. Stable path state and actual tool/configuration
  availability remain prerequisites; no race-free or whole-filesystem certification.
  Earlier helper-after equals later selected-before, but the earlier selected injector
  is a different function. Preserve helper history and original mechanical families.
- DifferentHostFilter removes repeated individual API/DB gets for repeated hint UUIDs;
  it still scans hints and bulk-loads visible instances per invocation. Do not call one
  bulk API call a fixed SQL count or one query per whole scheduling request. Matched
  request delivery, enabled filters, context and get/get_all policy/state matter.
- S3 manifest filenames reach local downloads before decrypt/untar. Basename confines
  the lexical local name and preserves the remote key. This is not the tarball repair,
  host-root authority, an executed exploit or complete registration safety. The old
  fresh-directory caller did not create nested parents, so new flattened collisions
  alone do not prove an introduced loss on an old supported nested-path domain.
- Protocol normalization repairs new producer/consumer case mismatch but changes
  legacy state matching. EC2 exact-case revoke can no longer match an existing uppercase
  row after request normalization; OpenStack exact-repeat duplicate rejection can also
  miss that row. These are **introduced legacy-state regressions**, conditional on
  unmigrated/unrepaired persisted rules, not new case-insensitive deduplication duties.
  The source fix changes only the two producers and firewall, with no DB migration.
- The firewall's unconditional `.lower()` also fails on admitted **protocol=None**
  source-group rules that old conditional generation supported: an **introduced null
  state regression**. IPv6 `icmp` becomes `icmpv6` before later `icmp` type/code dispatch
  in both versions, leaving a **residual** omission. Packet widening still needs actual
  downstream parser/chain/attachment conditions; no fail-open deployment is asserted.
- Preserve the complete **831-event /742-unique** ledger, **452 supported /216 ambiguous
  /74 exclusions**, SHA256 **9ca57ede950e4495ca81ef3c279a6ff7d312196473e270b47ad37fb68886c5c3**.
  Batch028 SHA256 **f55a138ad1578e51f57b8c6c1ec76f56d4aec864318afcc9b68d2872f0586adf**.
- Three new separately registered supplemental pins:
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_028.json:
    **2f32e42c5e84dfb10e84afcadd28562a8dd8d5cdce25a25d15354ed6b60a3e87**;
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_028_PEERS.json:
    **f8a0e967e51bfc46ac587ccdb123d88807d5f074c58f92c1970d941e989bcf35**;
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_028_DELIVERY.json:
    **60c38916bde57133ffea256807c0ed1ab30c864a3768d13b14d92b142b762c89**.
- New **56 inert texts** include14 verified archive peers; six404s are explicitly
  recorded, without inferring contracts from absence. URL-less archive peers resolve
  the original retained URL only after training identity/full text/hash/span/ref
  verification. Other supplements still require their retained URL. Authored batch and
  evidence files are preserved. Inventory: **2,849 historical anchors /2,799 current
  anchors /68 supplemental files /745 embedded texts**, plus the standalone template.
- All **101 own-tool tests passed** in321.502s, including exhaustive selection,
  introduced/residual after-deferral gates, helper versus selected-pair history,
  explicit historical refs and verified archive-peer identity/text/hash/span/ref.
- All Nova/libvirt/mount/filesystem/realpath/readlink/rootwrap/privileged command,
  scheduler/SQL/DB/policy, firewall/iptables/network, S3/boto/XML/archive/decryption,
  dependency/application programs, payloads and upstream tests remain inert. Findings
  are source deductions, not reproduced results or deployed-version proof.

## Previous checkpoint: 26 October 2026, batch028

Training discovery remains **742 /742**, **0 remaining**; draft **v0.42 /113 leaves** and
pending **v0.1 /25-parent** hierarchy are unchanged. Consolidation coverage is **547 /742**,
with **195 remaining** and **554 historical records**. Current proposals:

- 6 conditional retain;
- 224 missing-context;
- 75 existing-contract;
- 106 selected-attribution;
- 37 paired-negative;
- 50 security-boundary and3 non-style task-scope deferrals;
- 25 feature and21 nonrepair exclusion proposals.

All broad incomplete-case/state/context leaves and all pandas, Keras, Scrapy, Black,
Spirit, Thefuck, Synapse, Ansible, Waitress, Radicale, Glance, Vyper, Nautobot,
openapi-python-client, tlslite-ng and Nova training candidates have current proposals.
Next inspect all **seven Zulip training candidates**, including every status and null
category, under matched old API/policy/state/runtime contracts, lower-trust delivery,
selected attribution and bounded after negatives. Other large queues include Shuup7
and yt-dlp7; counts do not optimize an independent-issue target.

The common bounded before-only numerical budget and ordinary runtime/API/tool-knowledge
policy remain unfrozen. Adjudication helpers/callers/globals, after, labels, tests,
advisories and answers never become selectively injected detection inputs. Researcher
decisions, eligibility and independent issue identities remain pending; approval is not
ready. Preserve prior authored history, canonical bytes/splits and45 protected inputs.

## Consolidation batch029: Zulip — 26 October 2026

- All **seven training candidates /four mechanical families** have current proposals:
  **four missing-context /three security-boundary deferrals**. All seven supported
  discovery statuses/categories remain unchanged; no null categories exist here.
- Invitation key type/expiry validity is not tenant authorization. Old form validation
  adopts invite realmA while a fresh preregistration record uses request subdomainB;
  invitation status skips invite_required and invited_as reaches account creation.
  Successful external authentication or email verification and other account gates
  still matter. **Final signup rechecks B's email-domain policy**: the supported trace
  uses an email permitted byB and crosses invitation admission, without certifying
  universal domain bypass or every advertised elevated-role/stream consequence.
- Both after entries compare request/invite realms before using the invite; the
  matched accounts_home replaces its realm override with an equality assertion.
  Open-realm invalid/expired-key fallback remains separately subject to the ordinary
  form policy. get_realm_from_request prefers authenticated user realm, otherwise
  subdomain; the anonymous signup trace does not certify all session/routing states.
  Prior confirmation/preregistration records are outside the narrow new-entry negative.
- Three upload rows share filename-versus-stored-type disposition mismatch. Multipart
  content type is retained in S3 and already controls stored attachment safety; old
  nginx hides that disposition while the application chooses inline from a filename.
  The exact **before already adds CSP**, so actual active-script/session delivery needs
  a nonenforcing browser/configuration and real production S3/proxy/cache/object state.
  These three proposals explicitly defer security delivery. The affected interval was
  main-only, not every numbered release; no script or browser behavior was executed.
- After uses stored Content-Type/Disposition, forces attachment only through a signed
  URL argument, and includes that argument in nginx's cache key. Local-disk policy is
  recomputed inside serve_local; development redirects are distinct. Token access is
  signed and60-second-limited, not unrestricted public reads; url_only precedes header
  selection. No legacy-object/custom-config/all-browser/universal negative is certified.
- Bot object-management delegation permits ordinary owners but must not authorize
  granting administrator role. The selected old branch reaches a role-persisting helper;
  after adds explicit global administrator gating while preserving owner restrictions
  and unrelated bot metadata edits. Bound the witness to an authenticated member with
  an owned same-realm bot, not arbitrary human/cross-realm promotion.
- Private-stream existence validation is same-realm only; old autosubscribe invokes
  a helper that creates/reactivates private membership without invitation authorization.
  After skips invite-only mutation but preserves public autosubscribe and membership
  reporting. Do not infer private-existence secrecy, old-membership revocation or every
  history/message access outcome. No supported after-contract failure is established.
- Preserve the **831-event /742-unique** ledger, **452 supported /216 ambiguous /74
  exclusions**, SHA256 **9ca57ede950e4495ca81ef3c279a6ff7d312196473e270b47ad37fb68886c5c3**.
  Batch029 SHA256 **f5c14c0db6947a585f08b3b913e588357284c383897bddae0a0d022ede3a3568**.
- Four new separate supplemental pins:
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_029.json:
    **91205dc9547b0d61195ee83e4d04cb646d08fdb1549046c8aa74d90e84f7b49d**;
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_029_PEERS.json:
    **69ba0a70095c60d9e054407dad479cde2c4642efae9297cd12ae99435a1ac1cf**;
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_029_DELIVERY.json:
    **7b9b5f839d3545663eb0e61109592d136b108f3a5f4200759d0bba43a892a58f**;
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_029_ROUTES.json:
    **94e01714a93673a98ce1c110387b14dbe0770d68e9e9649ff9f7bfd021126b84**.
- New **68 inert texts** include ten deduplicated verified training archive peers and
  matched old/after admission/mutation/upload/routing/nginx/cache sources. Sixteen404s
  are explicitly recorded without inferring a contract from absence. After nginx/cache/
  allowlist hashes agree with prior retained admission evidence. Inventory: **2,926
  historical anchors /2,876 current anchors /72 supplemental files /813 embedded texts**,
  plus the standalone template. Seven functions/four families are not independent issues.
- All **105 own-tool tests passed** in366.241s. New checks cover exhaustive overlapping
  upload selection, unresolved-security retain rejection, explicit historical config
  refs and nginx/cache/allowlist hashes preserved from the prior admission review.
- All Zulip/Django/auth/session/registration/confirmation/OTP/role/stream/ORM/DB, upload/
  S3/boto/signing/nginx/cache/browser/HTML/JavaScript/regex/parser/filesystem/dependency/
  application programs, requests, payloads and upstream tests remain inert. Findings
  are conditional source deductions, not reproduced results or deployed-version proof.

## Continuation checkpoint: 26 October 2026, batch029

Training discovery remains **742 /742**, **0 remaining**; draft **v0.42 /113 leaves** and
pending **v0.1 /25-parent** hierarchy are unchanged. Consolidation coverage is **554 /742**,
with **188 remaining** and **561 historical records**. Current proposals:

- 6 conditional retain;
- 228 missing-context;
- 75 existing-contract;
- 106 selected-attribution;
- 37 paired-negative;
- 53 security-boundary and3 non-style task-scope deferrals;
- 25 feature and21 nonrepair exclusion proposals.

All broad incomplete-case/state/context leaves and all pandas, Keras, Scrapy, Black,
Spirit, Thefuck, Synapse, Ansible, Waitress, Radicale, Glance, Vyper, Nautobot,
openapi-python-client, tlslite-ng, Nova and Zulip training candidates have current
proposals. Next inspect all **seven Shuup training candidates**, including every status
and null category, under matched old API/policy/state/runtime contracts, lower-trust
delivery, selected attribution and bounded after negatives. yt-dlp also has7 remaining;
counts do not optimize an independent-issue target.

The common bounded before-only numerical budget and ordinary runtime/API/tool-knowledge
policy remain unfrozen. Adjudication helpers/callers/globals, after, labels, tests,
advisories and answers never become selectively injected detection inputs. Researcher
decisions, eligibility and independent issue identities remain pending; approval is not
ready. Preserve prior authored history, canonical bytes/splits and45 protected inputs.

## Consolidation batch030: Shuup — 26 October 2026

- All **seven training candidates /one mechanical family** have current proposals:
  **one missing-context /two existing-contract /four security-boundary deferrals**.
  Preserve six ambiguous/one supported discovery statuses and the existing category;
  no null categories or discovery revisions occur here.
- Setup pins django-jinja2.5.0/Jinja2.8.1; the backend defaults autoescape=True.
  Workbench selects it and XthemeEnvironment without changing that setting, and default
  Problem templates interpolate normally. Exception reflection alone is not XSS. Actual
  unsafe custom themes/templates/environments need retained evidence, not assumptions.
- Admin reasons are fixed or route-configured permissions, not arbitrary user/group
  display names. Its earlier JSON-shaped forbidden response lacks explicit JSON content
  type, but is unchanged and has no established lower-trust reason producer. Generic
  extract_messages has a fixed-message product visibility consumer plus an unproven
  signal-extension producer; its normal Problem sink autoescapes. Both defer old duty.
- Xtheme command, basket and editor error reflection need an unsafe consumer before
  asserting XSS. AJAX uses JsonResponse, and the retained basket error consumer uses
  text insertion. Basket is csrf_exempt; Xtheme command/editor are not. Workbench CSRF
  middleware remains relevant, and editor checks editing authority and valid layout
  setup before POST. Do not infer anonymous access or a forged privileged POST.
- Checkout Http404 needs exhaustion; an earlier invalid phase may return first.
  Ordinary installed Shuup404 handling discards its exception message and renders a
  fixed page. The compared Django2.2.24 fallback is also fixed. The404 referrer script
  is unrelated and unchanged. Unsafe custom exception rendering remains unresolved.
- Extra-view dispatch is different: an enabled broad URL capture supplies missing-view
  text directly to an ordinary text/html404 body, bypassing template escaping. After
  encodes view before composition. Trusted theme identifier, decoded WSGI path, lookup,
  browser/CSP and route/runtime conditions remain bounded. The supported local security
  repair still needs omitted project context under the uniform before-only protocol.
- Pre-encoding can alter JSON/plain-text or already-autoescaped display. No independent
  non-style fidelity duty or supported after-contract failure is established. All
  negatives are mechanism-local; no universal XSS-negative approval follows.
- Preserve the **831-event /742-unique** ledger, **452 supported /216 ambiguous /74
  exclusions**, SHA256 **9ca57ede950e4495ca81ef3c279a6ff7d312196473e270b47ad37fb68886c5c3**.
  Batch030 SHA256 **12e595f4a0d1e186eba6548efaa54b4e85208c55fb254a39034b631bb75cea70**.
- Six supplemental pins remain separate from the45-input lock:
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_030_SEARCH.json:
    **7522ba145a28007d09d1115e1a0a85bb9c516eae12fe5ce41552bf07899bcb4a**;
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_030_CONTEXT.json:
    **17c60a3d1eb4e95fa85b1424fb59300c7726a20c2df70c27b5f8022be8b2f5db**;
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_030_PEERS.json:
    **29471ac62222c20626ab70f31b4a626a9753ea04b7fc2f0c7b38ba7af2a93717**;
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_030_DELIVERY.json:
    **9788c1da138f00848060499eede949d7492ce01cdfffe90850ee093afa166218**;
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_030_CONTRACTS.json:
    **3a3a4018e251d7a1762264aa1d7c677458656dd1fd25f703aa5948de3f055361**;
  - CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_030_ROUTING.json:
    **1231c21a83b4748c56b55be7ab9b360cd27f59797aaf136859e6dae1a7b11f0f**.
- New **130 inert texts** include14 verified full training archive peers, source-corpus
  search results and exact historical contracts. Four explicit404s do not establish old
  duties. Django2.2.24 is a comparison inside the declared >=1.11,<2.3 range, not deployed
  version proof or whole-range certification. Archive members stay inert without
  filesystem extraction/import/install. Inventory: **3,000 historical anchors /2,950
  current anchors /78 supplemental files /943 embedded texts**, plus the standalone
  template. New own-validator checks cover complete mixed-status selection, corpus/
  archive agreement and explicit refs even where old/after template bytes are identical.
- All **108 own-tool tests passed** in376.569s. Final refresh/check/build/check
  verifies the reproducible checkpoint and all45 protected inputs.
- All retained Shuup/framework/dependency/application/ORM/DB/HTML/browser/JavaScript/
  template/regex/parser programs, requests, payloads and upstream tests remain inert.
  Only independently authored retrieval/view/hash/bookkeeping/audit-validator tools
  execute. Findings are source deductions, not reproduced results or independent issues.

## Continuation checkpoint: 26 October 2026, batch030

Training discovery remains **742 /742**, **0 remaining**; draft **v0.42 /113 leaves** and
pending **v0.1 /25-parent** hierarchy are unchanged. Consolidation coverage is **561 /742**,
with **181 remaining** and **568 historical records**. Current proposals:

- 6 conditional retain;
- 229 missing-context;
- 77 existing-contract;
- 106 selected-attribution;
- 37 paired-negative;
- 57 security-boundary and3 non-style task-scope deferrals;
- 25 feature and21 nonrepair exclusion proposals.

All broad incomplete-case/state/context leaves and all pandas, Keras, Scrapy, Black,
Spirit, Thefuck, Synapse, Ansible, Waitress, Radicale, Glance, Vyper, Nautobot,
openapi-python-client, tlslite-ng, Nova, Zulip and Shuup training candidates have current
proposals. Next inspect all **seven yt-dlp training candidates**, including every status
and null category, under matched old API/policy/state/runtime contracts, lower-trust
delivery, selected attribution and bounded after negatives. Preserve the recorded
incomplete-fix lineage; counts do not optimize an independent-issue target.

The common bounded before-only numerical budget and ordinary runtime/API/tool-knowledge
policy remain unfrozen. Adjudication helpers/callers/globals, after, labels, tests,
advisories and answers never become selectively injected detection inputs. Researcher
decisions, eligibility and independent issue identities remain pending; approval is not
ready. Preserve prior authored history, canonical bytes/splits and45 protected inputs.

## Consolidation batch031: yt-dlp — 26 October 2026

- Record all seven repository candidates across three mechanical families: six
  missing-context deferrals and one selected-attribution deferral. Preserve all831
  discovery events and this repository's six supported/one ambiguous statuses.
- Nested/enclosing q-format spans are one Windows percent-expansion repair. Old
  documented argument-quoting duty and matched ExecPP shell execution support the
  mechanism, while after shell-aware transforms require matching Popen environment
  and cmd flags. Earlier CVE-2023-40581 double-quote repair survives into the later
  vulnerable helper; the attributed CVE-2024-22423 advisory explicitly calls it a
  bypass. Separate lineage, representation overlap and independent issue identity.
- Old selected shell_quote production uses format diagnostics; the old vulnerable
  q branch calls compat_shlex_quote directly. New shell=True consumers do not
  establish an old selected-wrapper sink. Preserve that attribution deferral.
- Preexisting smuggled URL headers override internal referrer additions and reach
  privileged per-request proxy selection in Vimeo/Generic. After consumes flat
  referer metadata and migrates producers. Vimeo target restrictions differ from
  Generic arbitrary destinations; TLS verification/Secure-cookie conditions prevent
  a universal plaintext credential-theft claim from routing control alone.
- Native redirect filtering precedes the downloader-boundary repair. The latter
  before already blocks native redirect Cookie copy but still forwards raw parent
  Cookie on fragment first requests/external paths. Scoped-cookie producers and
  matching adapters are coordinated; no whole-advisory negative follows from the
  wrapper. Keep the after None-header/fragment-copy admission question explicit:
  its incompatible shape is conditional, an old standalone admission duty remains
  unestablished, and a complete standalone paired negative is withheld.
- Batch031 SHA256 **cf1301480e126a41f67820af454b9a98710ef45df4c881ab038acb2540b91bf6**.
  Five separately pinned files add85 inert texts/12 exact training archive peers:
  -031_CONTEXT **89a344d9f3092885fe2e5e0c0a72cf4d2cc1d593378fb416057b65fdc8d868a8**;
  -031_PEERS **658f7edaf3fbf221c86f90ebdf98463252d576d4446b5c66dd4edd9c847fabe3**;
  -031_SEARCH **5b6528aa33e352351037736fb8735c9b11dbc17a874d56766a91d322767bc47c**;
  -031_CONTRACTS **bf51c82a08327dae5dd1b10a1141eefad71b7dcbb318a8f1360ecbed2729d65b**;
  -031_LINEAGE **44bf2effa2bbf250d52badc0c0d42c338e0e029004fb4860c5058fe5d6d8616b**.
  Full advisory/commit API responses retain attributed snapshot qualifications.
  CPython3.11.4 is a comparison, not deployed-version or whole-range proof.
- Inventory: **3,081 historical anchors /3,031 current anchors /83 supplemental files /
  1,028 embedded texts**, plus the standalone enum template. Own-validator coverage
  adds complete nested/successive/mixed-status selection, archive/context agreement
  and explicit quoting-version refs. All retained programs, requests, payloads and
  upstream tests remain inert; only own audit/retrieval/view/hash tooling executes.
- All **111 own-tool tests passed** in442.662s after correcting the stale-review
  fixture's previous-batch totals. Final refresh/check/build/check verifies the
  reproducible checkpoint and all45 protected inputs.

## Continuation checkpoint: 26 October 2026, batch031

Discovery remains **742 /742**,0 remaining, draft **v0.42 /113 leaves**, with the
pending **v0.1 /25-parent** hierarchy unchanged. Consolidation covers **568 /742**,
with **174 remaining /575 historical records**. Current proposals: **6 conditional
retain /235 missing-context /77 existing-contract /107 selected-attribution /
37 paired-negative /57 security-boundary /3 task-scope /25 feature /21 nonrepair**.
All prior complete repositories plus all seven yt-dlp candidates have proposals.
Next inspect all **six remaining Cookiecutter candidates**, including every discovery
status and null category, preserving the three batch004 proposals and all history.
Other six-row queues include Swift, pysaml2, Sydent, pyload, markdown-it-py and LangChain;
queue counts do not optimize an independent-issue target.

Researcher decisions, eligibility and issue identities remain pending; approval is
not ready. The common bounded before-only numerical budget and ordinary runtime/API/
tool-knowledge policy remain unfrozen. Helpers/callers/globals, after, labels, tests,
advisories and answers never become selectively injected detection inputs. Preserve
canonical bytes/splits, prior authored history, append-only ledger and45 protected inputs.

## Consolidation batch032: remaining Cookiecutter — 26 October 2026

- Record all six remaining candidates, including four null categories, across four
  mechanical families: **two missing-context /three selected-attribution /one
  paired-negative** deferrals. All nine repository rows/five families now have
  current proposals. Preserve all three batch004 proposals unchanged.
- JSON/default-value duties and Python3.6+/Windows support justify portable Unicode
  context preservation. Old builtin open uses the effective locale before json.load
  receives text; after explicitly decodes UTF-8. Bound the negative to valid non-BOM
  UTF-8 contexts, retaining actual bytes/codec and downstream context as external facts.
- The prompt display change introduces a Click7-only show_choices keyword despite
  exact old/after setup retaining click>=5.0. Retained Click5.0/6.7 signatures reject
  the call before valid interactive selection; Click7 documents the parameter's
  introduction. This violates an old non-style return/default/dependency duty.
  Explicitly defer the paired negative, while not inventing an old non-style duplicate
  display positive. Append one ambiguous revision2, null category unchanged, withdrawing
  the blanket exclusion and preserving all831 previous event bytes.
- Hook subprocess status was correctly returned through old matching wrappers and
  checked by the pre-hook caller; post-hook ignored status is a caller policy question.
  Exception migration does not establish three isolated old producer defects, an old
  exception API, rollback guarantee or comprehensive execution safety. Preserve the
  batch004 cleanup-contract question and distinguish unchanged tempfile/encoding paths.
- Hg checkout operand data is exposed to global config/debugger options despite argv
  usage. Historical Mercurial6.1 early parser/dispatch/hooks support the mechanism;
  real lower-trust API admission and successful Hg clone/version remain conditional.
  After -- bounds this single revision operand, not Git/clone URL/all template safety.
  Later Cookiecutter accept_hooks control is not protection for earlier VCS checkout.
- Batch032 SHA256 **01301bc538917c876b2a679de3a4eb4d44b46ded2354fcd4685ec5c8f71892ce**.
  Four separately pinned files add63 inert texts/eight exact training archive peers:
  -032_CONTEXT **8a6fcd2dbf8b63f7b2e18734bfb6fbfbe349acae1e9ef2e52395a341d9432fef**;
  -032_PEERS **e7296e4e45fdb3392565e5145e657a6e0d9526ec4a223e3321b4c72abe78cf4c**;
  -032_CONTRACTS **850399d1e64cbb875e514babf9c75f9bcf48e6b6c8f7a356f7063992677f6527**;
  -032_DELIVERY **77516f384050aa1fa0aca8570bb9d0b4f747c2c9562442910bbbf6d775116783**.
  Missing requested archive members are explicit inventory absences, not HTTP404s
  or old duties. Click/CPython/Mercurial comparisons are not deployment/range proofs;
  Mercurial sdist SHA256 matches retained PyPI metadata without install/extraction.
- Ledger: **832 events /742 unique /452 supported /217 ambiguous /73 exclusions**;
  SHA256 **77d3003fbedadf6b27134179e2da0b0164693a1eb7ee572a1850a8d9ba10771c**.
  The831-event prefix remains
  **9ca57ede950e4495ca81ef3c279a6ff7d312196473e270b47ad37fb68886c5c3**.
- Inventory: **3,135 historical anchors /3,085 current anchors /87 supplemental files /
  1,091 embedded texts**, plus standalone enum template. Own-validator coverage adds
  exhaustive null-component selection, append-only revision/prefix/identity, after
  failure promotion rejection and archive/parent-context agreement. All retained
  programs, requests, payloads and upstream tests stay inert; only own tools execute.
- All **115 own-tool tests passed** in414.778s. Final refresh/check/build/check
  verifies the reproducible checkpoint and all45 protected inputs.

## Consolidation batch033: OpenStack Swift — 26 October 2026

- Record all **six candidates /one family**: **two missing-context /three selected-
  attribution /one paired-negative** deferrals. Preserve the two supported/four
  ambiguous discovery decisions and original deserialization categories.
- Flagged network cache bytes reach cPickle object construction in get/get_multi.
  Exact protocol flags are opaque client metadata; CPython2.6.8 construction resolves
  globals/callables. Requires actual cache write/response control and reader use,
  not merely tenant object upload. Single get checks the hashed key; bulk decodes
  rows before key filtering. Complete literal retrieval over55 production modules
  at each ref finds only bulk definitions. Existing public API tests do not establish
  a deployed bulk service route or dynamic-call completeness. After negatives cover
  only effective pickle-deny policy, not authentic cache data or metadata integrity.
- Constructor state and trusted-value writers coordinate the new reader policy;
  shared CVE membership/new consumer requirements do not establish three isolated
  old security violations. Preserve selected-attribution uncertainty rather than
  borrowing the reader sink or middleware parsing failure.
- New middleware compares text serialization modes with integers. Retained
  ConfigParser/PasteDeploy routes supply strings; advertised Python2.6 ordering
  makes textual0/1 disable both flags, defeating documented legacy-cache migration.
  Old valid tempauth cached sequences become misses; new JSON writes under text0
  can reach old readers without decoded structure. Explicit rollout compatibility
  preserves the old cached-value/consumer duty. Record an introduced after-contract
  regression and defer the paired negative. Missing settings use actual integer2
  correctly; programmatic integer0/1 intentionally remain insecure. No Python3
  crash, permissive deserialization bypass or old middleware loads sink is claimed.
- Batch033 SHA256 **852cd2406ad7f2ba56e52497fdaf48670ef1de97e7b68c591156cbcb30733afe**.
  Four separately pinned files add64 inert texts/four exact archive peers:
  -033_CONTEXT **b081c1187a36cb8f7bd0ecee24d754cd4c199eda505289011d00b7eb5758c636**;
  -033_PEERS **b48b6918d3b1bdcfce569f904cd4a0e7dfe5c7471888988cb68a590d989eab02**;
  -033_CONTRACTS **5d12faa9a4084669e7d61e72d0421dce2ef273adb39cc8ce05bc919454752300**;
  -033_RUNTIME **a762cc339d26aac1abec014f47308792cd7366d9f20c705669bb475e1d755708**.
  Runtime/protocol comparisons are not deployment or whole-range proof. Exact
  PasteDeploy/simplejson sdists match retained PyPI SHA256 without install/extraction.
- Ledger832-event SHA remains
  **77d3003fbedadf6b27134179e2da0b0164693a1eb7ee572a1850a8d9ba10771c**;
  categories, source bytes, splits and45 protected inputs remain preserved.
- Inventory: **3,193 historical anchors /3,143 current anchors /91 supplemental files /
  1,155 embedded texts**, plus standalone enum template. Added own-validator checks
  cover exhaustive ambiguous-component selection, after-failure promotion rejection
  and deduplicated archive/parent-context agreement. All **118 own-tool tests passed**
  in568.859s. Final refresh/check/build/check verifies reproducibility and all45
  protected inputs.
- All retained programs, cache/socket/parser operations, payloads, vulnerability
  requests and upstream tests stay inert. Only own tools execute; findings are
  conditional source deductions and six functions are not independent issues.

## Consolidation batch034: pysaml2 — 26 October 2026

- Record all **six candidates /one family**: **three missing-context /three security-
  delivery** deferrals. Preserve all six supported discovery decisions/categories.
- XML parsing precedes target-tag/SOAP/assertion/class/signature checks. Historical
  CPython2.7.12/3.5.2 comparisons support internal entity expansion/resource risk;
  ElementTree external-entity/file-read capability is not established by those
  bindings. A later rejection does not reverse earlier parse work. Actual runtime/
  Expat limits and input admission remain contextual, not execution/reproduction.
- Matched generated SAML wrappers reach create_class_from_xml_string before signature
  checks; Entity.unravel SOAP type wrappers reach parse_soap_enveloped_saml_thingy
  before response loading. Class-instance/ECP paths consume HTTP200 IdP/SP response
  text through parse_soap_message. Conditional resource boundaries are supported,
  without a universal unauthenticated endpoint or unrelated-website delivery claim.
- Raw extension and pack parser literal src/example hits are definitions only;
  ordinary SAML extension-tree conversion is a different helper. Envelope opener
  has unpack_soap_message wrapper evidence but no retained production wrapper caller.
  ECP's parse_soap_message is not that wrapper. Defer selected security delivery for
  these three rather than borrowing sibling paths. Literal inventories are not
  dynamic-call completeness or proof APIs are unused.
- Retained defusedxml0.4.1/0.5.0 default entity/external handlers reject declared
  entities before feed; two selected functions wrap rejection in XmlParseError.
  forbid_dtd=False does not reject every DTD or establish complete SOAP compliance;
  SOAP1.1's DTD prohibition alone is not a pre-parse guard. Unversioned dependency,
  entity-free resource consumption, signatures and separate xmlsec paths remain
  qualified. Ordinary tree interfaces/tostring aliasing do not establish a backend
  regression; no supported independent admitted entity-free after failure is found.
- Batch034 SHA256 **f156d3c6b5f492b991e951c5e42e8321cd1e230797155932d324d1cde4bd7988**.
  Four separately pinned files add136 inert texts/six exact archive peers:
  -034_CONTEXT **072d194bf4736f11a0a49d52117244a0655a8444e06b6aca4f6dca534e130556**;
  -034_PEERS **087f22ac4e8fc622b55c97ef2cd4b46cc23ceac4fcdf00915ce56735328b6f0b**;
  -034_CONTRACTS **d1f887e54cbe431b97a83afcf55c9240afcae4ab6c852a32a7138368451bf240**;
  -034_DELIVERY **ebfbdbec25baf21ab1e28bf318930d880ee9f9e4a10d470e9dccb3e1c0e0a43e**.
  Full commit metadata resolves the parent and selected files match archives.
  Package sdists match retained PyPI SHA256 without install/extraction. Runtime,
  protocol and package comparisons are not deployed/whole-range proof; explicit
  missing archive members are not old duties.
- Ledger832-event SHA remains
  **77d3003fbedadf6b27134179e2da0b0164693a1eb7ee572a1850a8d9ba10771c**.
  Inventory: **3,265 historical anchors /3,215 current anchors /95 supplemental files /
  1,291 embedded texts**, plus standalone enum template. Added own-validator checks
  cover complete-family selection, unresolved delivery blocking retain even with
  ordinary context, and three-file archive/parent agreement. All **121 own-tool tests
  passed** in666.699s. Final refresh/check/build/check verifies reproducibility and
  all45 protected inputs.
- All retained programs/XML payloads/vulnerability requests/upstream tests stay
  inert. Only own tools execute; findings are conditional source deductions and six
  functions/three files/one family are not independently adjudicated issue counts.

## Consolidation batch035: Sydent — 26 October 2026

- Record all **six candidates /five families**: **four missing-context /two paired-
  negative** deferrals. Distinguish both HTTP response representations from the four
  other mechanisms; six rows/five families are not independent issue counts.
- Configured SMTP_SSL/STARTTLS old defaults do not authenticate the peer before
  login/mail delivery. After default SERVER_AUTH context verifies certificate and
  hostname under retained runtime comparisons. Actual TLS/network-position/trust
  policy is conditional; plaintext fallback remains outside the negative.
- Old accepted client-secret regex lacks length bounds before session/validation-link
  consumers. After<=255 is a post-parse field admission bound, not a request-buffer/
  rate limit, catastrophic-backtracking repair or proof of an old255-byte contract.
- GET registration/key-fetch responses are accumulated before identity/signature
  checks. Matched5KiB/50KiB caller caps and bounded helper coordinate the repair;
  defaultNone stays unbounded. Onbind POST only needs response metadata after admitted
  ownership/binding; zero-size reader avoids repeated whole-body accumulation.
  Chunk writes precede>=limit checking, and known oversize discard fails/aborts on
  data/connectionLost. No zero-transient-bytes, exact peak-memory, immediate timeout/
  close or universal lifecycle guarantee is made.
- Invite sender was not bound to returned Account.userId. After equality gates the
  authenticated mode, but default matrix-org/vector-im HTML templates request
  bracketed_verified_sender_for_html while renderer derives _forhtml. Ordinary valid
  requests without that extra misspelled key raise KeyError before SMTP, violating
  the existing default-template invitation-delivery duty. Record an **introduced
  after integration regression** and defer paired-negative use; custom/corrected
  templates can differ. Unauthenticated mode/display fields/MIME randomization stay
  separate from this selected binding witness.
- The2019 selected after forwards raw recipient text, but CPython2.7.16 smtplib
  sendmail→rcpt→quoteaddr calls parseaddr again. That parser truncates at a second@,
  while matched validation-session/HTTP consumers retain raw identity. Synapse0.99.3
  raw-domain restrictions are a consumer comparison, not a Sydent setting or proof
  of deployed versions. Record a **residual after-contract failure**, not regression;
  later2.7.17 parser rejection and2021 parsed/raw equality guard are not backfilled.
  Append one ambiguous→supported revision2 resolving previous runtime/consumer
  uncertainty while explicitly deferring the after negative. Preserve original
  category, source hashes/family and all832 prior event bytes.
- Batch035 SHA256 **4fb13064020b1fef3c6a99814c1447db55434a506d013fbf899fded97b788771**.
  Four separately pinned files add145 inert texts/ten exact archive peers:
  -035_CONTEXT **3511f71422f9f209c7bc55c7e9fead30f68692e29fc7a8d75d1654ea8f375a2e**;
  -035_PEERS **bb5b4b3a65e54c37c4308f1b4c2e18472241566867751641623f0bf9633af854**;
  -035_CONTRACTS **d30d6ac994416cd77b16a6fd05e100a739aa5e757cd61ba1cc173b27b14fa6f1**;
  -035_DELIVERY **399490eca609404575cd41f9517c7e2dec322112d6de9e153afbbb1d7e69567b**.
  Five commit APIs resolve parents and selected source files match archives.
  Explicit requested-member/HTTP404 absences are not old duties. Historical runtime,
  Twisted and Synapse comparisons are not installed/whole-range certification.
- Ledger: **833 events /742 unique /453 supported /216 ambiguous /73 exclusions**;
  SHA256 **e9d9086397f5b960af9df2784a0e0073bf7afeaa9b5edceca61b382bc9e8744a**.
  The832-event prefix remains
  **77d3003fbedadf6b27134179e2da0b0164693a1eb7ee572a1850a8d9ba10771c**.
- Inventory: **3,329 historical anchors /3,279 current anchors /99 supplemental files /
  1,436 embedded texts**, plus standalone enum template. Own-validator checks add
  exhaustive selection, append-prefix/identity, introduced/residual failure promotion
  rejection and mixed-origin archive/parent agreement. All **125 own-tool tests passed**
  in693.502s. Final refresh/check/build/check verifies reproducibility and all45
  protected inputs.
- All retained programs/messages/payloads/vulnerability requests/upstream tests stay
  inert. Only own tools execute; findings are conditional source deductions.

## Consolidation batch036: pyload — 26 October 2026

- Record all **six candidates /five families**: **four missing-context /one selected-
  attribution /one paired-negative** deferrals. API/UI login are two representations
  of one log-record repair, not two independently adjudicated issues.
- Old selected framing method registers error handlers only. A live new global DENY
  hook establishes the policy insertion, not old selected ownership of anti-framing
  or a concrete consequential framed action. Retain effective proxy/browser/session
  delivery and selected attribution as unresolved.
- Both login routes pass failed-authentication usernames into configured line-oriented
  handlers. Parameterized DB lookup returns an empty mapping for unknown users;
  credentials are unnecessary for that log branch. After escapes CR/LF only in the
  selected failure/success messages. Do not claim all-control-character/log safety.
- Old curl initializer disables origin peer-chain verification. After default enables
  it, coordinated factory/configuration supplies ssl_verify=True by default, and
  configured False deliberately restores disabled verification. Unchanged HTTPS-proxy
  verification is a distinct boundary. Actual HTTPS/network-position/trust-store and
  later overrides remain conditional; user-agent change is separate.
- Old redirect selector validates a normalized joined URL but returns raw next/referrer.
  Retained CPython/Werkzeug/WHATWG comparisons support conditional authority disagreement
  through a login/session redirect. New caller correctly supplies fallback endpoint
  app.dashboard: **no ordinary fallback BuildError is established**. However new
  login_required retains only endpoint suffix, dropping required path arguments.
  For /files/get/<path:path>, get_file cannot build without path; the helper catches
  BuildError and successful login goes to dashboard rather than the requested file.
  Old request.url, matching selector/caller and action-empty login forms preserve that
  normal same-origin destination. Record an **introduced after integration regression**
  of protected-destination return and defer paired-negative use. Parameter-free routes
  can work; no universal login crash is claimed.
- Old SameSite=None can carry ambient admin session to GET API add_user under accepted
  TLS/Secure/browser policy. Matching authorization grants admin authority and DB
  mutation; it does not bind cross-site intent. After Strict blocks that cross-site
  cookie delivery under the retained extension/browser comparison, not same-site
  attackers, unsafe GET itself or general CSRF. Modern browsers may reject old None
  without Secure; do not infer vulnerable plaintext/default deployments.
- Batch036 SHA256 **83ddfd6b550e195b94e8646aebc26aaf42fc99efa252143c0cfeef6a3090911f**.
  Seven pinned files add **199 inert texts /twelve exact archive peers**:
  -036_CONTEXT **71fdb91c5435be00bb57ef9644b9fcc04852af7a79a7a52007df46d56c0da9be**;
  -036_PEERS **3e9d5a23b17ae19213d7cd29acd0fbe8b939d57fe8337be4ae95c639f84b95e0**;
  -036_CONTRACTS **410f483d5d7429e7f6ab75a4fd3624bdf0dea2e3a051b9485ba98d4ee54d5e84**;
  -036_DELIVERY **a1784ee56e505ee84145238a80652dce3a74cd9f750f8b40f8909ef4a4a685bc**;
  -036_SESSION **547a066c00508d1c00c0341727e883b683d8499d354906225705ffc8ebdf158a**;
  -036_ROUTING **0d662c8460b26d4cd9766670832efc57a46498fd73dc165058c215d226a91989**;
  -036_CONFIG **96355b72feed7e2b5e80778c195671db6586364e71ae26f2c4c49f275a51f799**.
  Five commit APIs resolve parents and ten archive inventories retain literal retrieval
  and explicit absent paths. Three failed extension-path requests remain explicit404s;
  corrected src paths are retained separately. Dependency/RFC/SameSite/current mutable
  WHATWG comparisons are not installed/browser-version or whole-range certification.
- All **833 discovery events /742 candidates /453 supported /216 ambiguous /73 exclusions**
  remain byte-identical; ledger SHA256
  **e9d9086397f5b960af9df2784a0e0073bf7afeaa9b5edceca61b382bc9e8744a**.
  Inventory: **3,394 historical anchors /3,344 current anchors /106 supplemental files /
  1,635 embedded texts**, plus standalone enum template. All **128 own-tool tests
  passed** in741.269s. Final refresh/check/build/check verifies reproducibility and
  all45 protected inputs.
- All retained programs/payloads/vulnerability-target requests/upstream tests remain
  inert. Only own retrieval/view/hash/bookkeeping/audit-validator tools execute;
  findings are conditional source deductions, not reproduced outcomes.

## Consolidation batch037: markdown-it-py — 26 October 2026

- Record all **six candidates /two families**: **one missing-context /four selected-
  attribution /one paired-negative** deferrals. Five null-token functions share
  one fix/family; only the recursive alt-text helper has the matched standard
  nested-image failure witness. Six rows/two families are not independent issues.
- Standard block/inline producers populate top-level inline child lists before
  rendering or optional typography. Nested image children=None lives inside that
  list, not as a top-level inline token in state.tokens. Top-level render,
  replacements and smartquotes guards do not inherit the recursive failure.
  Typography additionally needs enabled components/typographer and quote gating.
  Generic custom-token/plugin extensibility is not proof every constructed null
  state is an admitted old contract. Preserve selected attribution as unresolved.
- Ordinary image producer always supplies attrs/alt. Old renderInlineAsText entry
  already accepts None through tokens or []; the prior superseded image iterable-
  failure inference remains withdrawn. Changing only the selected image entry guard
  leaves the recursive nested-child assertion. This is coordinated hardening, not
  another isolated old selected failure.
- For a standard outer description containing an empty nested image, image producer
  stores that nested token's children as None. Outer alt extraction reaches the
  recursive assertion with assertions enabled. CommonMark0.30 permits nested image
  descriptions and recommends plain-string alt content, independently of the new
  fixture. After skips absent/empty nested children while preserving text/softbreaks.
  Bound the negative to this assertion, not all Markdown/HTML/resource availability.
  Actual lower-trust consumer/exception containment remains conditional; -O removes
  the old assertion and changes the failure path.
- CLI main→convert→convert_file uses a strict locale/default text reader before
  rendering. UnicodeDecodeError escapes OSError catch and stops the current batch,
  but a local user selecting a file is not itself an external security boundary.
  Do not infer an old obligation to tolerate all malformed bytes from the CVE.
- **Introduced after data-preservation regression:** old advertised file-to-HTML
  conversion declares no UTF-8-only input policy, and the chosen reader uses the
  effective locale. Under a supported cp1252 default/UTF-8-mode-off environment,
  ordinary valid text containing byte0xE9 preserves U+00E9 before. After forces
  utf8/errors=ignore, silently discarding that valid-old-encoding character. Require
  stdout representability and otherwise ordinary Markdown; UTF-8-default environments
  can be unaffected. This differs from intentionally dropping genuinely malformed
  UTF-8. CommonMark specifies characters rather than a mandated encoding and does
  not itself impose all-encoding support. Defer paired-negative use without turning
  the after regression into a new old security positive.
- CLI parent already contains the earlier renderer guards. Keep the two fix snapshots
  separate; shared file/context history is not selected-function equality or a family
  merger. Preserve all833 discovery events/statuses/categories/hashes/families unchanged,
  ledger SHA256 **e9d9086397f5b960af9df2784a0e0073bf7afeaa9b5edceca61b382bc9e8744a**.
- Batch037 SHA256 **2715cb9046242d1bbc2505aa0e16f5a035575b4d5d072fecbc93c6ae96f7da3b**.
  Three pinned files add **134 inert texts /eight exact archive peers**:
  -037_CONTEXT **ecaf03bcc4cad087b1342c4a3d9a618e71b573dfbb0bca1286dd710e3d80be67**;
  -037_PEERS **82864cdb978d8544e7167989425e559c6c52486f572dfdc63fd5cbe7bee55178**;
  -037_CONTRACTS **4b026368da84e3ce448010a9719a634d47e23aca52aaa995c8784eafe73c9d06**.
  Two resolved parents/four archive inventories retain literal source retrieval and
  explicit absent paths. CommonMark0.30/CPython3.9.16 comparisons are not installed
  runtime, custom-plugin completeness or whole-range certification.
- Inventory: **3,447 historical anchors /3,397 current anchors /109 supplemental files /
  1,769 embedded texts**, plus standalone enum template. All **131 own-tool tests
  passed** in800.552s. Final refresh/check/build/check verifies reproducibility and
  all45 protected inputs.
- All retained programs/payloads/vulnerability-target requests/upstream tests remain
  inert. Only own retrieval/view/hash/bookkeeping/audit-validator tools execute;
  findings are conditional source deductions, not reproduced outcomes.

## Continuation through batch037 — 26 October 2026

Discovery remains **742 /742**,0 remaining, draft **v0.42 /113 leaves**, with pending
**v0.1 /25-parent** hierarchy unchanged. Consolidation covers **604 /742**, with **138
remaining /611 historical records**. Current proposals: **6 conditional retain /
251 missing-context /77 existing-contract /118 selected-attribution /43 paired-negative /
60 security-boundary /3 task-scope /25 feature /21 nonrepair**. All previously complete
repositories plus all six markdown-it-py rows have current proposals.
Next inspect all **six LangChain training candidates**, including every discovery
status and null category. TensorFlow, Twisted and Saleor each have five remaining;
counts do not optimize an independent-issue target.

Researcher decisions, eligibility and issue identities remain pending; approval is not
ready. The common bounded before-only numerical budget and ordinary runtime/API/tool-
knowledge policy remain unfrozen. Helpers/callers/globals, after, labels, tests,
advisories and answers never become selectively injected detection inputs. Preserve
canonical bytes/splits, prior authored history, append-only ledger and45 protected inputs.

## Consolidation batch038: LangChain — 27 October 2026

- All **six training rows /four mechanical families**, across every discovery status,
  now have proposals: **two missing-context /one selected-attribution /three paired-
  negative** deferrals. No discovery revision, category/family/source change or new
  approved eligibility/independent-issue count is introduced.
- Old recursive loader consumes extracted HTML links through actual requests/aiohttp
  fetches. Raw base-prefix validation can admit a different parsed authority under
  certain base shapes. After adds netloc equality, but path-only relative joining
  loses query-only pagination and can resolve a distinct child to an already visited
  page: **introduced crawl-completeness regression**. Negative is authority-mechanism
  local, not redirect/DNS/universal SSRF protection; fragment dropping predates this fix.
- Old LocalFileStore allowed key characters include separators/parent segments and
  actual consumers read/write/delete outside root under raw-key control and process
  permissions. Cached document text is hashed, not automatically an unrestricted key.
  After Path.absolute retains root parent segments while abspath normalizes the child;
  retained POSIX commonpath semantics then reject ordinary keys under legitimate roots
  such as ../cache: **introduced root-form compatibility regression**. No unsupported
  symlink/race residual is promoted without a matched producer/control path.
- Old XML parse and async stream can deliver internal declarations to ElementTree.
  Resource amplification depends on Expat protections and actual completion/chunk
  control; Expat2.4.1+ mitigates the cited expansion forms. Standard ElementTree is
  not evidence for arbitrary external-file XXE. Old sync stream already strips ordinary
  pre-root declarations and remains selected-attribution deferred. After defusedxml
  supplies entity rejection; async additionally gains pre-root filtering. Distinguish
  these effects, preserve mechanism-local negatives and omit universal XML resource
  claims. No independent ordinary entity-free after regression is established.
- Old SQL wrapper maps fetched row values through unrestricted Python eval. Matched
  SQLDatabase/chain consumers establish the concrete data-to-code path, conditional
  on query/result influence and process authority. After returns raw rows without eval,
  also removing dictionary conversion required by the documented native/direct-return
  retriever. Admitted SQLAlchemy2.0.23 Python/C Row indexes tuples, not named strings;
  the retriever's named content lookup fails for ordinary nonempty results: **introduced
  result-shape integration regression**. Do not substitute a later dict-returning DB
  helper or confuse this mechanism with repaired SQL injection.
- Three introduced after-contract failures each require paired-negative deferral;
  after-only correctness failures do not invent old security positives. Shared XML
  source/fix does not equate selected old flows; six functions/four mechanical families
  are not independently adjudicated issues or automatic family mergers.
- Batch038 SHA256 **726c725275761785dd75b91f2c6e0510b2ce100dc9e2216b7d4c2668dffe9dc8**.
  Four pinned files add **120 inert texts /eight exact archive peers**:
  -038_CONTEXT **98cf0e8877dcd652080ff8cdec65fd40dd14ae3b00fda1ea089314d9bd39c735**;
  -038_PEERS **49b8341f772057164b0b389d7728345b63c45d89e041ae86ef79a5ad553c8769**;
  -038_CONTRACTS **7eadf06f4e37f108a1a29935afe0db6626d8878b20d89d9303c2602285eaf970**;
  -038_DELIVERY **811ea57702d602d280ef6cc927a045cf1bfa2cfda36e8455bae92d0a1f5a35b8**.
  Four resolved parents/eight archive inventories retain literal production/docs
  searches and explicit absent paths. Historical CPython3.8.10/3.11.8, defusedxml0.7.1,
  SQLAlchemy2.0.23 and notebooks are contract comparisons, not installed/provider/
  all-version proof. Notebook code and recorded outputs remain inert.
- Preserve all833 discovery events/statuses/categories/hashes/families unchanged,
  ledger SHA256 **e9d9086397f5b960af9df2784a0e0073bf7afeaa9b5edceca61b382bc9e8744a**.
  Inventory: **3,506 historical anchors /3,456 current anchors /113 supplemental files /
  1,889 embedded texts**, plus standalone enum template. All **134 own-tool tests
  passed** in616.910s. These verify exhaustive mixed-status selection, rejection of
  after-regression promotion and resolved shared-file archive-peer agreement.
  Final refresh/check/build/check passed: all seven generated artifacts are reproducible
  and all45 protected inputs remain unchanged; researcher approval is pending/not ready.
- All retained programs/notebooks/payloads/vulnerability-target requests/upstream
  tests remain inert. Only own retrieval/view/hash/bookkeeping/audit-validator tools
  execute; findings are conditional source deductions, not reproduced outcomes.

## Continuation through batch038 — 27 October 2026

Discovery remains **742 /742**,0 remaining, draft **v0.42 /113 leaves**, with pending
**v0.1 /25-parent** hierarchy unchanged. Consolidation covers **610 /742**, with **132
remaining /617 historical records**. Current proposals: **6 conditional retain /
253 missing-context /77 existing-contract /119 selected-attribution /46 paired-negative /
60 security-boundary /3 task-scope /25 feature /21 nonrepair**. All previously complete
repositories plus all six LangChain rows have current proposals.
Next inspect the **five-row TensorFlow, Twisted and Saleor queues**, including every
discovery status and null category, then the four-row queues. Counts do not optimize
an independent-issue target.

Researcher decisions, eligibility and issue identities remain pending; approval is not
ready. The common bounded before-only numerical budget and ordinary runtime/API/tool-
knowledge policy remain unfrozen. Helpers/callers/globals, after, labels, tests,
advisories and answers never become selectively injected detection inputs. Preserve
canonical bytes/splits, prior authored history, append-only ledger and45 protected inputs.

## Consolidation batch039: TensorFlow — 27 October 2026

- All **five training rows /two mechanical families**, including the null-category
  serializer exclusion, now have proposals: **one nonrepair exclusion /one task-scope /
  three security-boundary** deferrals or exclusions. No discovery revision, category,
  family/source change or approved eligibility/independent-issue count is introduced.
- Model.to_yaml serializes existing configuration; it is not the separate reader's
  unsafe-load sink. Preserve coordinated producer nonrepair exclusion. Old reader
  unsafe_load/legacy load invokes Python constructors before the Keras custom_objects
  mapping under retained PyYAML5.4.1/3.13 comparisons, conditional on lower-trust YAML
  supply and process authority. Arbitrary-model sandbox safety is not inferred.
- Both actual after APIs raise RuntimeError unconditionally, despite the safe_load-
  oriented commit title. Release Breaking Changes explicitly retire YAML roundtrip.
  Reader has a mechanism-local retired-route negative and **task-scope deferral**:
  researcher decide full-API retirement admission to the repair/negative task. This
  declared policy is not an unintended after regression or universal JSON/H5 safety.
- Upper Function construction/restoration install primitive locks held during first
  tracing and callback invocation. Lower Function holds its own lock during cache-
  miss tracing before insertion. Supported finite recursive Python callable reentry
  can block on the same held lock. Old pickle-state producer/consumer/test establish
  legitimate restoration conditionally on recursive lookup targeting restored wrapper;
  this does not establish unsafe-pickle repair or every restored-object failure.
- After coordinated RLock allocations permit owning-thread reacquisition under
  CPython3.9.7 semantics, with corresponding release counts. Negative is local to that
  mechanism; no recursion/work bound, cross-thread deadlock freedom or model/graph/
  pickle safety is certified. One after regression test expects RecursionError for
  an unbounded tracing form; no independent after failure is established under the
  supported finite-recursion duty.
- **Three security-delivery deferrals:** arbitrary callback code is already program
  authority under historical TensorFlow security policy. A lower-trust data-to-trusted-
  recursive-callback/worker path remains unestablished. Matched SavedModel wrapper lacks
  original Python code and dispatches concrete graphs via constructor, not pickle
  __setstate__. Do not equate graph cycles with this callback/lock path or borrow
  model loading as selected restored-lock delivery. Preserve conditional functional
  findings and missing before-only project context.
- Batch039 SHA256 **9a31b24166239036f140781b40013ba49573b5c4d933055f8f9a0b1792c17b56**.
  Three pinned files add **56 inert texts /eight exact archive peers**:
  -039_CONTEXT **64b268afdec94ad270d49a387b9022630a999ff9556d76cb63340e40b74e0ee3**;
  -039_PEERS **b3396be6c950c98ad6ea36ed1cd0d846c9f71e8e3b4c82cae174bdd5f17309e0**;
  -039_CONTRACTS **a576437e0bdae61df1931fa8d66643d1d9e240a30c9f93f57cf5029140f59b1c**.
  Two resolved parents/two explicit404 requests retain missing-path provenance.
  Explicit paths/all commit-changed files are not exhaustive repository/dynamic
  integration search. Runtime/PyYAML/security-policy comparisons are not installed/
  all-version proof; absent paths do not establish old duties.
- Five functions/two mechanical families are not independently adjudicated issues.
  Preserve all833 ledger events/statuses/categories/hashes/families and prior authored
  batches unchanged, ledger SHA256
  **e9d9086397f5b960af9df2784a0e0073bf7afeaa9b5edceca61b382bc9e8744a**.
  Inventory: **3,553 historical anchors /3,503 current anchors /116 supplemental files /
  1,945 embedded texts**, plus standalone enum template. All **137 own-tool tests
  passed** in664.490s, checking exhaustive mixed-status/null selection, scope/security
  promotion rejection and resolved shared-file archive-peer agreement.
  Final refresh/check/build/check verifies seven-artifact reproducibility and all45
  protected inputs. Researcher approval remains pending/not ready.
- Retained programs/models/callbacks/locks/threads/pickle/YAML/dependency code,
  payloads, vulnerability-target requests and upstream tests remain inert. Only own
  retrieval/view/hash/bookkeeping/audit-validator tools execute; conditional source
  deductions are not reproduced outcomes.

## Checkpoint: 27 October 2026, batch039

Discovery remains **742 /742**,0 remaining, draft **v0.42 /113 leaves**, with pending
**v0.1 /25-parent** hierarchy unchanged. Consolidation covers **615 /742**, with **127
remaining /622 historical records**. Current proposals: **6 conditional retain /
253 missing-context /77 existing-contract /119 selected-attribution /46 paired-negative /
63 security-boundary /4 task-scope /25 feature /22 nonrepair**. All previously complete
repositories plus all five TensorFlow rows have current proposals.
Next inspect the **five-row Twisted and Saleor queues**, including every discovery
status and null category, then the four-row queues. Counts do not optimize an
independent-issue target.

Researcher decisions, eligibility and issue identities remain pending; approval is not
ready. The common bounded before-only numerical budget and ordinary runtime/API/tool-
knowledge policy remain unfrozen. Helpers/callers/globals, after, labels, tests,
advisories and answers never become selectively injected detection inputs. Preserve
canonical bytes/splits, prior authored history, append-only ledger and45 protected inputs.

## Consolidation batch040: Twisted — 27 October 2026

- All **five candidates /two mechanical families**: **two missing-context /two
  selected-attribution /one security-boundary** deferrals. Discovery history unchanged.
- Redirect constructor adds coordinated sensitive-header policy; actual cross-origin
  transmission/filtering is a separate handler. New custom `ETag` canonicalization
  mismatches Headers special output, whereas lowercase `etag` works: retain as a new
  option limitation, not an old selected custom-policy regression.
- Header strip hides non-OWS bytes before framing; after SP/HTAB-only normalization
  and strict CL/TE consumers reject those forms. Old chunk int16 accepts non-HEXDIG
  syntax/unchecked extensions; after strict checks precede buffer/state use and malformed
  server requests terminate400/disconnect. Actual multiple-parser forwarding/competing
  consumption remains necessary for a smuggling consequence. RFC rejection alone is
  not that delivery witness. Obs-fold lacks isolated meaning-changing old selected
  evidence; standalone fromChunk lacks an identified production caller. Keep sibling
  attribution and bounded negatives separate; no complete HTTP/stream guarantee.
- Batch040 SHA256 **9e0899dd7589379ee018732184b30ab15ebf57e6cfe04f4a980a92f8a986581c**.
  Four supplemental pins retain52 inert texts/four peers/two parents/four inventories:
  -040_CONTEXT **49b20c825eb11397ddb8b4f3b55158b316998f319fb1d418391642e38dd8b6c4**;
  -040_PEERS **039fe86175723ce0f92b6f7caf0b632a36f6f096dca00d599e1110f4b5853c12**;
  -040_CONTRACTS **153eb561db818eacfa44c647be13f4b4a11f5ef08b7e70b878f2bc24b8558b1c**;
  -040_RFC **ccb662456a61d41c5e906c446a4d7bc41a5e1a9634a3a1de095ac5ee374c39e0**.
  Initial CONTRACTS source0 is HTTP301 HTML only; separately retained TLS-verified
  redirect-following RFC7230 is actual grammar evidence. Preserve both immutable files
  and absent-member provenance. CPython3.10.2 comparison is not deployed-version proof.

## Consolidation batch041: Saleor — 27 October 2026

- All **five candidates /three families**, including two null categories: **three
  missing-context /one nonrepair exclusion /one security-boundary** proposals.
- Explicit empty optional Graphene String triggers old cookie fallback while caller
  skips CSRF. Matched csrf_exempt/form-POST route and non-DEBUG Secure/SameSite=None
  setter establish conditional ambient-credential action; DEBUG Lax/third-party cookie
  policies qualify delivery. Token response readability is separate: no automatic
  exfiltration/account-takeover claim. After None-only fallback matches caller CSRF
  predicate and explicit empty text is JWT-rejected. Old cleaner already rejects
  empty actual tokens and cannot recover original credential source; changed missing/
  invalid classification is coordinated ancillary behavior, preserving null nonrepair.
- JWT lazy-user setup catches a real InvalidTokenError boundary, but retained producer
  messages do not establish another-user secret. Do not inherit generic formatter
  disclosure from a companion fix. New generic typed response is not all-subclass
  serialization certification: token code is absent from ProductErrorCode and code
  normalization preserves it. Public error-enum compatibility remains a question,
  without an established old typed-envelope duty or supported after regression.
- MANAGE_USERS-only actor can retrieve another customer root; old root-ID orders
  loader/callback supplies non-draft orders without owner/order permission. After
  non-manager branch requires root==context.user or denies. Actual role grants/root
  state are prerequisites; no anonymous/all-field claim. Nested/outer selections
  overlap one disclosure path, not two independent issues.
- Batch041 SHA256 **0951c0891b281876f6a9f7c05d97e45f5b5670e37303540182491130f64a245d**.
  Four supplemental pins retain149 inert texts/six peers/three parents/six context
  inventories plus three old delivery searches and explicit absent paths:
  -041_CONTEXT **5582672c13957e15e6481d957dfa541cf5b904975c74f6bb8fff740140bd6d2a**;
  -041_PEERS **a04191fc261d88a5b0dfb98cfa9b99c6c8c2cb36d0da8c10377380d73e7b5d2a**;
  -041_DELIVERY **6e6c68f8e04052089b9fe786333cfc1ce63fd04bcdf4af4eacb4cabfe132dfe8**;
  -041_CONTRACTS **317f6a6d94f292566002859b6f7075349798b84ced076504047efdc6e27a13ec**.
  Historical PyJWT2.5.0/Graphene2.1.9/Django3.2.18/3.2.25 are semantic comparisons,
  not installed/all-version/browser proof. Absence does not establish old duty.

## Checkpoint: 27 October 2026, batches040–041

Discovery remains742/742, draftv0.42/113 leaves and pendingv0.1/25-parent hierarchy.
Current consolidation: **625 /742 /117 remaining /632 historical records**. Proposals:
**6 conditional retain /258 missing-context /77 existing-contract /121 selected-attribution /
46 paired-negative /65 security-boundary /4 task-scope /25 feature /23 nonrepair**.
All five Twisted and all five Saleor rows join previously complete repository queues.
Inventory: **3,631 historical anchors /3,581 current anchors /124 supplemental files /
2,146 embedded texts**, plus standalone enum template. **141 own-tool tests passed**
in864.275s, including exhaustive/null selection, promotion rejection and exact peer/
parent archive agreement. Final refresh/check/build/check verifies seven-artifact
reproducibility and all45 protected inputs.

All833 ledger events unchanged, SHA256
**e9d9086397f5b960af9df2784a0e0073bf7afeaa9b5edceca61b382bc9e8744a**.
Preserve prior authored batches/evidence, canonical bytes/splits, discovery statuses/
categories/hashes/families and45 protected inputs. Researcher approval remains pending/
not ready; functions/families/overlaps are not independent issues. The numerical
before-only budget and ordinary runtime/API/tool-knowledge policy remain unfrozen;
helpers/callers/globals/after/labels/tests/advisories/answers are adjudication-only.
No retained programs, payloads, vulnerability-target requests or upstream tests execute.
Findings are conditional source deductions, not reproduced outcomes.

Next inspect four-row repository queues with all discovery statuses/null categories;
counts do not optimize an independent-issue target. Resolve eligibility/context/issue
proposals before requesting confirmation, freezing rules or held-out adjudication.

## Consolidation batch042: Keystone — 27 October 2026

- All **four candidates /three mechanical families**, no null categories: **two
  missing-context /one residual paired-negative /one security-boundary** deferrals.
- Old disabled-user update leaves stored token snapshots; public token-derived
  authentication does not recheck current enabled state. After current-user lookup
  rejects disabled accounts and companion update attempts token deletion, with an
  explicit unsupported-listing caveat. Direct existing-token use is a different scope.
- That after-selected function exactly equals the next candidate's vulnerable before:
  omitted expires still causes matched creators to issue a fresh default lifetime.
  Repeated valid-before-deadline delegation can exceed a finite parent's bound. Retain
  an explicit `unresolved_contract_failure` paired-negative deferral, not an invented
  introduction or full-function clean negative. Selected equality is not full-file
  equality/direct commit-parent adjacency. Next after carries old expires; KVS/SQL
  preserve explicit fields and enforce that deadline. Existing None is old nonexpiry
  policy. Backend/configuration/clock/tenant contracts remain external before-only facts.
- Old last-role removal drops membership and revokes issued tokens, while still-valid
  EC2 credentials can reissue a scope token with empty roles. Keystone validation accepts
  stored tenant identity; downstream operation policies may still reject. After denies
  empty roles before catalog/token creation. S3 inherits authenticate with separate
  signature override: same mechanism, not another issue or unsigned/arbitrary-user claim.
- Old register_str forwards cfg.StrOpt kwargs; DEBUG startup calls log_opt_values.
  Admitted oslo.config1.1.0 defaults secret=False, documents redaction and masks both
  root/group values only with that flag. After admin_token/ldap.password flags repair
  that path. Actual unauthorized log readership remains unresolved despite a concrete
  is_admin credential consumer. Do not certify other secrets, default ADMIN, existing
  log files, secret lengths or all dependency versions.
- Batch042 SHA256 **e1dfb0b340967e41c145efc3cd90c8ce778d7c96150b7c98414dbcc8099d1596**.
  Three supplemental pins retain219 inert texts/eight peers/four parents/eight archive
  inventories, plus explicit absent-path provenance:
  -042_CONTEXT **ab70c395666ffd12e654e1c7df049ff5bceac49995313ce66aa32b313de287ac**;
  -042_PEERS **10df8f480d96fbb6dd9d614bfd8504f66513520e6859e857353cfcd089021c84**;
  -042_CONTRACTS **3b8b8227c545195759c7a3459b099fa38f85f12dcbed8669fd01a4e66f6028bc**.
  Dependency sdist digest matches retained package metadata; members read in memory,
  never extracted/imported/installed. Comparison is not deployed/all-version proof.

## Checkpoint: 27 October 2026, batch042

Discovery remains742/742, draftv0.42/113 leaves and pendingv0.1/25-parent hierarchy.
Consolidation: **629 /742 /113 remaining /636 historical records**. Proposals:
**6 conditional retain /260 missing-context /77 existing-contract /121 selected-attribution /
47 paired-negative /66 security-boundary /4 task-scope /25 feature /23 nonrepair**.
Inventory: **3,672 historical anchors /3,622 current anchors /127 supplemental files /
2,365 embedded texts**, plus standalone enum template. **145 own-tool tests passed**
in609.562s. Initial full attempt reached its20-minute timeout without reported failures
before termination; subsequent full suite passed after reusing decoded supplemental
files within each validation call only, preserving every source/anchor check and
fresh validation snapshots. Final refresh/check/build/check verifies seven generated
artifacts and all45 protected inputs.

Preserve all833 ledger events, SHA256
**e9d9086397f5b960af9df2784a0e0073bf7afeaa9b5edceca61b382bc9e8744a**,
prior authored evidence, canonical bytes/splits, statuses/categories/hashes/families.
Approval remains pending/not ready; functions/families/version links are not independent
issues. Before-only numerical budget and ordinary runtime/API/tool-knowledge policy
remain unfrozen; no selective helper/caller/global/after/label/test/advisory injection.
No retained program, payload, vulnerability-target request or upstream test executes.
Next inspect all four pyoidc candidates/all statuses/null categories, then remaining
four-row repository queues; counts do not optimize an independent-issue target.

## Consolidation batch043: pyoidc — 27 October 2026

- All **four candidates /one mechanical family**, including one null category and
  supported/ambiguous/exclusion discovery statuses: **one security-boundary /one
  selected-attribution /one residual paired-negative /one nonrepair exclusion**.
- Old parser skips none signature verification absent expected algorithm. Private
  claim verifier adds flow-specific none rejection, but old installed lower-trust
  invocation is not established by the newly added Consumer call. Public wrapper
  forwards response_type to a new guard; old callee had no such argument/check.
  Missing new context rejects conservatively. Keep separate attribution/delivery
  deferrals, not four inherited CVE positives.
- Consumer after adds expected algs/final verifier, yet `_parse_authz` drops kwargs.
  A saved [code] request permits none at final checking without binding actual Token
  Endpoint provenance. Otherwise admissible unsigned callback ID claims with known
  request state/nonce can still return. Bare-ID-token/no-companion acceptance already
  existed, so record residual `unresolved_contract_failure`, not introduced regression.
  OIDC1.0 errata1-2014 predates the patch, requires signatures outside direct Token
  Endpoint exception, and requires explicit registration/no Authorization Endpoint
  ID token for none. Returned-claim acceptance is not universal application takeover:
  later valid-code requirements can stop login. Writes before final check are not an
  atomic rollback guarantee.
- Message helper instead relaxes none hash checks and delegates policy. Admitted
  pyjwkest1.4.2 left_hash falls through for HSone rather than proving a crash. No
  established old front-channel none+hash acceptance duty; preserve null nonrepair.
  Adjacent claim-time checks and separate RP callback algorithm gate are different
  selected methods/paths. Flow request type alone is not trusted channel/registration.
- Batch043 SHA256 **cd99ac726b9f9fd373a16edad52b512d20d849b355c73d1fe9a40cf5a763701e**.
  Three supplemental pins retain54 inert texts/six peers/one resolved first parent/
  two complete archive inventories plus explicit absent-path provenance:
  -043_CONTEXT **b3ce08114d9b364dad6774aa66f28a4c13c243249f63a644e087ad4d276f8640**;
  -043_PEERS **741a70fe9f44f5a50599b0cf82f8d2b03e4aefdf0bc70cd0d515aaf32a3b1f3f**;
  -043_CONTRACTS **200ef7182f7826813cad5b0efd38736d3a1b92c2cf604b5941237e5b460231b2**.
  Protocol retrieved with ordinary TLS-verified curl after Python key-usage validation
  rejected the certificate chain; no verification bypass. Pyjwkest sdist digest agrees
  with retained package metadata; read in memory without extraction/import/install.
  Historical comparisons are not deployed/all-version proof; merge/URL redirects do
  not create new issue identities or rewrite canonical repository IDs.

## Previous continuation: 27 October 2026, batch043

Discovery remains742/742, draftv0.42/113 leaves and pendingv0.1/25-parent hierarchy.
Consolidation: **633 /742 /109 remaining /640 historical records**. Proposals:
**6 conditional retain /260 missing-context /77 existing-contract /122 selected-attribution /
48 paired-negative /67 security-boundary /4 task-scope /25 feature /24 nonrepair**.
Inventory: **3,706 historical anchors /3,656 current anchors /130 supplemental files /
2,419 embedded texts**, plus standalone enum template. **149 own-tool tests passed**
in569.928s, covering exhaustive mixed-status/null selection, invalid promotion rejection
and exact archive-peer/parent agreement. Final refresh/check/build/check verifies seven
generated artifacts and all45 protected inputs.

Preserve all833 ledger events, SHA256
**e9d9086397f5b960af9df2784a0e0073bf7afeaa9b5edceca61b382bc9e8744a**,
prior authored evidence, canonical bytes/splits, statuses/categories/hashes/families.
Approval remains pending/not ready; four functions/one family are not independent issues.
Before-only numerical budget and ordinary runtime/API/tool-knowledge policy remain
unfrozen; no selective helper/caller/global/after/label/test/advisory injection. No
retained program, payload, vulnerability-target request or upstream test executes.
Next inspect all four urllib3 candidates/all statuses/null categories, then remaining
four-row repositories; counts do not optimize an independent-issue target.

## Consolidation batch044: urllib3 — 27 October 2026

- All **four candidates /four mechanical families**, including the null percent pair:
  **two missing-context /one residual paired-negative /one nonrepair exclusion**.
- Matched Retry defaults/configuration and origin/mapping/transport contracts support
  the casing repair. Exact 2018 after still changes 303 to GET while retaining a
  private reusable byte body through recursion; matched pool/CPython3.6.6 sends it.
  Under allowed cross-origin redirection this is residual content disclosure, not a
  casing-introduced regression. Record `unresolved_contract_failure` and explicitly
  defer the selected paired negative. Later 2023 body clearing is a distinct mechanism,
  without selected-string equality or direct-parent adjacency between these versions.
- The 2023 manager repair sets body=None and copies/prepares content-specific headers
  via matched HTTPHeaderDict. RFC7231/9110 give retrieval-transition semantics; actual
  private bytes, redirect budget, destination control and application URL restrictions
  qualify delivery. Bound the 303 body mechanism; do not certify every status/header,
  framing option or arbitrary policy. Helper/transport context remains outside selected text.
- The selected CVE-2020-7212 pair introduces a component-encoding helper and has no
  repeated percent-match/full-string replace loop on either side. Resolved 1.25.7 has
  the later loop and 1.25.8 uses one subn callback, not advisory-hypothetical deduplication.
  Keep null mislinked-fix/nonrepair exclusion; comparisons do not identify the exact
  intervening fix or authorize replacing canonical sources. Pre-fix tests already
  require Python3 binary-URL TypeError; no invented supported-input after regression.
- The distinct 2021 greedy optional userinfo/host ambiguity revisits long authority
  suffixes across many candidate @ delimiters. rpartition plus host-only regex removes
  that repeated partitioning. Named CPython3.9.5 supports conditional backtracking
  semantics, not measured performance/all-regex linearity. Standard redirect joining
  may reject unmatched brackets before parse_url; direct initial PoolManager parsing
  is a separate admitted source path. Application caps/delivery remain conditional.
- Batch044 SHA256 **8538d07c3fc3a71bb46719069714e2502800c4cb077be3bfc37a76696028cb1d**;
  **41 unique anchors /186 inert texts /eight exact peers /four resolved first parents /
  eight archive inventories**, plus missing-path provenance. Four supplemental pins:
  -044_CONTEXT **5c19136aebce68ab402afa5b30fe0c06164646a991576bd3f33b2ab86508245a**;
  -044_PEERS **c207f64f8790565afa3013e211e750a9d20e59ec578a3f2dabda5bcbca3b949e**;
  -044_CONTRACTS **e997ac7a9f77bbb8d224d8aeb74c51d071f71b0b5574adced5eb810be923365b**;
  -044_RUNTIME **628a3b95583ebc7e0c32475bbcb9787388d50fe7f37fa11534cf9590cacf390f**.
  Historical protocol/runtime/version comparisons are not installed/all-version proof.

## Previous continuation: 27 October 2026, batch044

Discovery remains742/742, draftv0.42/113 leaves and pendingv0.1/25-parent hierarchy.
Consolidation: **637 /742 /105 remaining /644 historical records**. Proposals:
**6 conditional retain /262 missing-context /77 existing-contract /122 selected-attribution /
49 paired-negative /67 security-boundary /4 task-scope /25 feature /25 nonrepair**.
Inventory: **3,747 historical anchors /3,697 current anchors /134 supplemental files /
2,605 embedded texts**, plus standalone enum template. All **153 own-tool tests passed**
in583.602s, covering exhaustive mixed-status/null selection, invalid promotion rejection
and exact archive-peer/parent agreement.
Final refresh/check/build/check verifies seven generated artifacts and all45 protected
inputs.

Preserve all833 ledger events, SHA256
**e9d9086397f5b960af9df2784a0e0073bf7afeaa9b5edceca61b382bc9e8744a**,
prior authored evidence, canonical bytes/splits and45 protected inputs. Approval remains
pending/not ready; four functions/four mechanical families are not independent issues.
Before-only budget/ordinary-knowledge policy remains unfrozen; no selective helper/
caller/global/after/label/test/advisory injection. No retained program, payload,
vulnerability-target request or upstream test executes. Next inspect all four bcfg2
candidates/all statuses/null categories, then remaining four-row repository queues.

## Consolidation batch045: bcfg2 — 28 October 2026

- All **four candidates /one mechanical family**, retaining all discovery statuses:
  **one missing-context /one security-boundary /two paired-negative deferrals**.
- Signing shell operands are server-config/temp-derived, not direct client hostname
  syntax; preserve ambiguous old selected security attribution. Matched after helper
  changes to argv but retains shell=True. CPython2.7.2 POSIX semantics invoke bare
  openssl, not the intended request command; named OpenSSL1.0.0d enters interactive
  mode. Ordinary EOF leaves no CSR and waiting stdin can wait for input. Record an
  introduced generation-integration regression before selected signing, supported by
  old documentation/callers, without inventing an old selected injection positive.
- Key verification quotes complete paths in fixed pipelines but follows successful
  CA verification. Do not borrow prior sibling execution/output spoofing to establish
  an independent selected lower-trust invocation; security delivery remains deferred.
- Cached CA verifier has a hostname-derived operand before its validity/output gate.
  Actual Basic-auth username/global-password/default-profile/session metadata flow
  establishes conditional name influence without a DNS-character grammar. Existing
  cache/key/plugin/configuration prerequisites remain; no anonymous root or universal
  first-time request claim. Shell-free argv bounds selected interpretation, not all
  certificate, filesystem or process-status semantics; context eligibility deferred.
- SSHbase only reaches shell getent on cache miss/caught DNS error. After argv removes
  shell interpretation but keeps list output; get_skn set.add fails and catches it,
  omitting successful fallback address. Named IPv4-only Python and IPv6-capable glibc
  getent establish an ordinary AAAA-only alias witness. This is residual before/after,
  not introduced or a new admitted security issue; names/other aliases can still render.
- Batch045 SHA256 **e68c18a110f3f13aff90b6716817a7a499f41fe40ba1b0e0889052dd0b65f7d5**;
  **45 unique anchors /60 inert texts /four exact full-file peers /one resolved first
  parent /two archive inventories**, including missing-path provenance. Four pins:
  -045_CONTEXT **3e0c374fc8fccfcb4191f08f6a1b43893910e14e80c6490af4c0bdca46eac22b**;
  -045_PEERS **4f6fb0aedaf3acd1b3ae7f7f5b60eb703d10958ce4d7c801d0623b6146c07a2b**;
  -045_CONTRACTS **d2e8365c511e1cc9415caefaac5a9af6167b2f169e605c629b7733aa8befb29d**;
  -045_DELIVERY **e277a69343f4a256a161cb59744da159613fc643fac2422aa991a613f0700c94**.
  Named runtime/utilities are semantic comparisons, not installed/all-version proof.
  Maintenance backport omits SSLCA and does not establish identical repair/alias
  equivalence. Batch qualifies inherited advisory ref/date label as collected28 October.

## Previous continuation: 28 October 2026, batch045

Discovery remains742/742, draftv0.42/113 leaves and pendingv0.1/25-parent hierarchy.
Consolidation: **641 /742 /101 remaining /648 historical records**. Proposals:
**6 conditional retain /263 missing-context /77 existing-contract /122 selected-attribution /
51 paired-negative /68 security-boundary /4 task-scope /25 feature /25 nonrepair**.
Inventory: **3,792 historical anchors /3,742 current anchors /138 supplemental files /
2,665 embedded texts**, plus standalone enum template. All **157 own-tool tests passed**
in624.070s, covering exhaustive mixed-status selection, introduced/residual paired-negative
and other promotion rejection, and exact archive-peer/parent agreement. Final
refresh/check/build/check verifies seven generated artifacts and all45 protected inputs.

Preserve all833 ledger events, SHA256
**e9d9086397f5b960af9df2784a0e0073bf7afeaa9b5edceca61b382bc9e8744a**,
prior authored evidence, canonical bytes/splits and45 protected inputs. Approval
remains pending/not ready; four functions/one family are not independent issues.
Before-only budget/ordinary-knowledge policy remains unfrozen; no selective helper/
caller/global/after/label/test/advisory injection. No retained program, payload,
vulnerability-target request or upstream test executes. Next inspect all four OpenStack
swauth candidates/all statuses/null categories, then remaining four-row repositories.

## Consolidation batch046: OpenStack swauth — 28 October 2026

- All **four candidates /one mechanical family**, preserving all discovery statuses:
  **three missing-context /one paired-negative deferrals**. Exact fix
  **70af7986265a3defea054c46efc82d0698917298**, first parent
  **54ac16ad670d8586acb668ac31ac4e2655831747**; one full file shared by all functions.
- Old normal issuance, local group cache-miss lookup and external token validation
  embed live bearer names in backing-object URIs. Named Swift2.15.0 request propagation
  and object logging retain full object paths, independently of header truncation.
  Actual log access, live token/cache and configuration/runtime are conditional;
  bounded before text alone does not establish them. After uses the shared salted
  prefix:token:suffix SHA512 name and digest-derived shard consistently across all
  four operations. Intended response bearer and user metadata remain distinct.
- Admin user deletion has a concrete conditional old DELETE-log live-token witness:
  prior ordinary use caches unexpired groups; both deletion handlers omit auth-cache
  invalidation. Matched readers still authorize cached groups after successful token
  object/user deletion, until expiry/eviction. Existing forced-new-token issuance
  explicitly invalidates the same key, supporting the old lifecycle duty. Record this
  residual **unresolved_contract_failure/defer_paired_negative** without rewriting the
  ambiguous discovery event or inventing an introduction, failed-delete race,
  anonymous log access or universal cross-cluster persistence.
- Incoming/remote validation APIs and auth-service posthook path logs still contain
  raw bearer text. swob.path preserves popped segments through SCRIPT_NAME; path
  popping is not redaction. Those surfaces are outside the backend-object-name
  negative; no complete secret-log confidentiality claim. The fix explicitly warns
  of old-token logout without memcached: intentional naming transition, not an
  accidental regression or automatic old-object migration. Historical Python2.7
  support/string hashing avoids an invented Python3 byte-API regression.
- Batch046 SHA256 **8e50f7278fcd83f09989fd163008fdc113dd199358f5619b3780aeeb01547903**;
  **67 unique anchors /47 inert texts /two exact full-file peers /one resolved first
  parent /two archive inventories**, retaining requested-missing provenance. Four pins:
  -046_CONTEXT **5f3a778d497ea1c8481ce7145d7730408f234f37558cbb7054a9ad63a3758458**;
  -046_PEERS **f7d749d856758a31f989efe4e7a9bce567d76ab9f761326ee0289acae1ee2797**;
  -046_CONTRACTS **dec9754896b4306c33e2b21f032301452c33b404628d14f330e6bf2fcdc9ea82**;
  -046_DELIVERY **56e25c06716fe91d3c640cec5efa5c1540168fc942e3133b57933bf4a3caf4e7**.
  Named Swift/Python comparisons are not installed/all-version/deployed proof. Four
  functions remain one mechanical family pending independent issue adjudication.
  All retained programs/payloads/vulnerability requests/upstream tests remain inert.

## Previous continuation: 28 October 2026, batch046

Discovery remains742/742, draftv0.42/113 leaves and pendingv0.1/25-parent hierarchy.
Consolidation: **645 /742 /97 remaining /652 historical records**. Proposals:
**6 conditional retain /266 missing-context /77 existing-contract /122 selected-attribution /
52 paired-negative /68 security-boundary /4 task-scope /25 feature /25 nonrepair**.
Inventory: **3,859 historical anchors /3,809 current anchors /142 supplemental files /
2,712 embedded texts**, plus standalone enum template. All **161 own-tool tests passed**
in634.527s, covering exhaustive mixed-status selection, residual paired-negative and
other promotion rejection, and shared full-file/parent agreement for all four functions.
Final refresh/check/build/check verifies seven generated artifacts and all45 protected
inputs.

Preserve all833 ledger events, SHA256
**e9d9086397f5b960af9df2784a0e0073bf7afeaa9b5edceca61b382bc9e8744a**,
prior authored evidence, canonical bytes/splits and45 protected inputs. Approval remains
pending/not ready; four functions/one family are not independent issues. Before-only
budget/ordinary-knowledge policy remains unfrozen; no selective helper/caller/global/
after/label/test/advisory injection. No retained program, payload, vulnerability-target
request or upstream test executes. Next inspect all four qutebrowser candidates/all
statuses/null categories, then remaining four-row repositories.

## Consolidation batch047: qutebrowser — 29 October 2026

- All **four candidates /three mechanical families**, preserving discovery history:
  **one missing-context /three paired-negative deferrals**. The settings handler and
  WebKit guard share one CVE/fix/parent and remain one coordinated request-binding
  family, not two independent issues.
- Old certificate-error flag/reset/callback and status/UI consumer support conditional
  reload warning loss after an accepted exception/session reuse. After host history
  fixes remembered top-level errors but loses the old warning for accepted errors on
  a different-host HTTPS subresource: callback records B, status tests unremembered
  top-level A and emits success_https. Matched WebKit reply/ignore paths and named Qt
  signals/controller support this ordinary introduced indicator regression. No silent
  first-visit TLS bypass, strict-trust override or universal backend behavior is claimed.
- Old settings GET mutation converts/applies/persists configuration without request
  binding under affected backend admission. After guards add binding, but every page
  render overwrites the sole global CSRF token; earlier still-open pages retain their
  literal token URL and ordinary edits fail. Old tab/template/configuration paths
  establish multi-page duty. This is an introduced token-lifetime availability failure,
  not a missing-password/None bypass or immediate command execution.
- WebKit caller/new signature match; current_url comes from tab.url or empty fallback.
  Canonical method/current-tab gate and coordinated token check are locally bounded,
  with actual backend/frame/redirect/canonicalization context deferred. Attribute the
  downstream global-token regression to its settings owner; do not certify whole-flow
  multi-page correctness or invent another independent origin-guard failure.
- History title reaches actual innerHTML through stored data/JSON/frontend, supporting
  the local escaping repair. After also HTML-escapes URL assigned directly to DOM href;
  valid query & becomes literal &amp; and changes navigation. Named HTML5.2 setter
  stores the supplied attribute value rather than HTML-parsing it. Record introduced
  URL-preservation failure, not another XSS positive or an unsupported None-title crash.
- All three failures require **unresolved_contract_regression/defer_paired_negative**
  and an unestablished selected-component negative. Four functions/three mechanical
  families remain pending independent issue adjudication; original IDs/hashes/splits,
  discovery events/statuses/categories and protected inputs remain unchanged.
- Batch047 SHA256 **1b92d1d51e04135fcdd0de35f0eba292184c1ac877b19cf08b1820e4e9564f41**;
  **51 unique anchors /228 inert texts /eight exact full-file peers /three resolved
  first parents /six archive inventories**, with missing/redirect provenance. Four pins:
  -047_CONTEXT **0052da0222df744fac4c4955e6d21d5fc5fff00dfad7e17bb891faeaf5147c4e**;
  -047_PEERS **b020e31ae6e687cb10222848270f0915b9fd15de0a1ed89c01c505b76c756bc0**;
  -047_CONTRACTS **bd3a5f11d52f5547e50183cc1fbf80bed6b379c5fc6fd636c4d2ae446168041b**;
  -047_DELIVERY **95e3271c7bca3788727b68baaf7659d3ddad9c17c7e5f009d769501f98ec4910**.
  Named Qt/Python/HTML comparisons are not installed/all-version/deployed proof. W3C
  historical HTTPS text uses TLS-verified curl after Python CA key-usage validation
  failure; retained note records that provenance and verification is not disabled.
  No retained browser/Qt/JS/HTML/program/payload/vulnerability request/upstream test
  executes; evidence is adjudication-only, never selective detection context.

## Previous continuation: 29 October 2026, batch047

Discovery remains742/742, draftv0.42/113 leaves and pendingv0.1/25-parent hierarchy.
Consolidation: **649 /742 /93 remaining /656 historical records**. Proposals:
**6 conditional retain /267 missing-context /77 existing-contract /122 selected-attribution /
55 paired-negative /68 security-boundary /4 task-scope /25 feature /25 nonrepair**.
Inventory: **3,910 historical anchors /3,860 current anchors /146 supplemental files /
2,940 embedded texts**, plus standalone enum template. All **165 own-tool tests passed**
in936.985s, covering exhaustive selection/shared-family preservation, all three introduced
paired-negative and other promotion rejection, and exact archive-peer/parent agreement.
Final refresh/check/build/check verifies seven generated artifacts and all45 protected
inputs.

Preserve all833 ledger events, SHA256
**e9d9086397f5b960af9df2784a0e0073bf7afeaa9b5edceca61b382bc9e8744a**,
prior authored evidence, canonical bytes/splits and45 protected inputs. Approval remains
pending/not ready; four functions/three families are not independent issues. Before-only
budget/ordinary-knowledge policy remains unfrozen; no selective helper/caller/global/
after/label/test/advisory injection. No retained program, payload, vulnerability-target
request or upstream test executes. Next inspect all four cloud-init candidates/all
statuses/null categories, then remaining four-row repositories.

## Consolidation batch048: cloud-init — 29 October 2026

- All **four candidates /three mechanical families**, preserving discovery history:
  **three missing-context /one selected-attribution deferrals**. Metadata classifier
  and filesystem initializer share the2023 fix/CVE but have different causal sinks;
  four functions/three families are not independently adjudicated issues.
- Old datasource policy/redaction/public JSON establishes privacy duty, but actual
  lower-case Vultr user/vendor fields require new policy entries rather than proving
  an old case-normalization miss. No retained actual mixed-case old-protected field
  isolates that selected defect. Preserve ambiguous classifier discovery and defer
  attribution. After preserves original paths, LXD extends defaults while retaining
  dotted keys, and JSON-roundtripped keys are strings; no invented policy-loss or
  integer-key regression.
- Old RANDOM/R passwords are applied then written to stderr and the default tee
  output pipe. Named tee/fopen/service contracts support conditional new0644 logs
  readable by a non-root/non-adm account. After pipe-child umask0037/optional adm GID
  bounds ordinary new-file mode to0640; the companion writer separately uses console.
  Existing-file permissions, direct-open branches and arbitrary pipeline/ACL/ownership
  behavior are outside that negative. Configured shell text is not itself injection.
- Old exact boot validation is non-strict; real chpasswd schema and named
  jsonschema3.2.0/4.6.0 repr-bearing oneOf errors support conditional secret-value
  warning disclosure through a readable main log. After the exact boot caller selects
  log_details=False; API defaults and strict/CLI details remain intentional. Negative
  is only the suppressed boot warning, not all diagnostics or validation behavior.
- Main setupLogging precedes initialization. Default FileHandler can create0644;
  old preserve_mode=True keeps it despite requested0640, and root:adm ownership does
  not remove other-read. Same-ref Vultr DEBUG output is a concrete conditional secret
  writer. After False enforces0640 through empty append/chmod without log truncation;
  privacy before initialization, other handlers/ACLs and races remain unestablished.
  Output-log creation, main-log mode and public JSON policy are distinct mechanisms
  across the2021/2022/2023 version histories, not automatic independent issues.
- Batch048 SHA256 **e60898c976aa7bd2cd3e4153d54fd2f9268dc74bf38fc97e9bacdddf538dd1f5**;
  **52 unique anchors /359 inert texts /eight exact full-file peers /three resolved
  first parents /six archive inventories**, with requested-missing provenance. Three pins:
  -048_CONTEXT **4a413a6029537a4fa483eb7c2a11e6c180eef3c1233a80b0e98e3ec218443934**;
  -048_PEERS **623c7c14693bbb0541ff6efc833921d768d7ed858372baaaa213dd39a5c6a7e4**;
  -048_CONTRACTS **489ab1a379a4a11bd6273aa6f3071d5efcc27d89099043459a1552f484be14b7**.
  Historical Python/validator/service/utility/POSIX comparisons are not installed/
  all-version/deployed proof. No retained program, payload, vulnerability-target
  request or upstream test executes; evidence is adjudication-only.

## Previous continuation: 29 October 2026, batch048

Discovery remains742/742, draftv0.42/113 leaves and pendingv0.1/25-parent hierarchy.
Consolidation: **653 /742 /89 remaining /660 historical records**. Proposals:
**6 conditional retain /270 missing-context /77 existing-contract /123 selected-attribution /
55 paired-negative /68 security-boundary /4 task-scope /25 feature /25 nonrepair**.
Inventory: **3,962 historical anchors /3,912 current anchors /149 supplemental files /
3,299 embedded texts**, plus standalone enum template. All **169 own-tool tests passed**
in915.545s, covering exhaustive cloud-init selection/shared-family preservation,
ambiguous classifier attribution versus contextual log repairs, promotion rejection,
and exact archive-peer/parent agreement. Final refresh/check/build/check verifies seven
generated artifacts and all45 protected inputs.

Preserve all833 ledger events, SHA256
**e9d9086397f5b960af9df2784a0e0073bf7afeaa9b5edceca61b382bc9e8744a**,
prior authored evidence, canonical bytes/splits and45 protected inputs. Approval remains
pending/not ready. Before-only budget/ordinary-knowledge policy remains unfrozen;
no selective helper/caller/global/after/label/test/advisory injection. No retained program,
payload, vulnerability-target request or upstream test executes. Next inspect all four
rdiffweb candidates/all statuses/null categories, then remaining four-row repositories.

## Consolidation batch049: rdiffweb — 29 October 2026

- All **four candidates /four mechanical families**, preserving supported discovery
  history: **three missing-context /one residual paired-negative deferrals**. Separate
  password/session revocation, authenticated reauthentication guesses, admin method
  admission and supplied-Origin authority from related shared security terminology;
  functions/families are not independently adjudicated issues.
- Old password update changes hash without revoking username-bound sessions. Actual
  configured DbSession loader/auth/currentuser and matched after explicit form commit
  establish both old boundary and persisted deletion. But a distinct already-loaded
  session can be reinserted after deletion: per-ID locks do not synchronize user-wide
  revocation, and unchanged save-on-missing copies old auth data into a new row with
  the old ID and commits. Named CherryPy18.8.0 save hooks, SQLAlchemy1.4.41 and
  CPython3.10.8 no-SELECT-BEGIN pysqlite contracts admit a conditional SQLite schedule
  with no earlier DML in the stale request. Record **unresolved_contract_failure /
  defer_paired_negative /not_established_for_selected_component**, not an introduced
  regression, all-isolation/deployed claim or executed race.
- Admin deletion old GET proxy/username validation reaches real store DELETEs despite
  no submission gate; existing admin/self/configured-admin restrictions still apply.
  External top-level GET can carry Lax session cookies and bypass the mutating-method
  Origin check. After submission/validation rejects GET; actual old/new POST modal
  remains admitted. This is a local method negative, not universal CSRF protection.
- Earlier current-password form already validates required current/new/confirm and
  calls a real old password check. After counts five failures per session, clears/
  regenerates auth and redirects to login. Correct-password path and admin caller
  match the new helper API. No invented empty-required-field/keyword failure, anonymous
  password oracle or global time-based lockout. Later route limiter is not backfilled.
- Origin prefix admits distinct authority. Matched hook/root/profile POST/base/proxy
  and named browser contracts support a same-site hostile delegated-prefix-host case
  where Lax cookies remain attached; arbitrary cross-site POST may lack credentials.
  After exact equality bounds supplied-Origin mismatch, not missing Origin, safe
  methods, unimplemented Referer check, proxy canonicalization or complete CSRF/CORS.
- Batch049 SHA256 **d06fec6f4048e824f139bea5407af19f2e04cce0462de303f57c00f4940dd783**;
  **64 unique anchors /373 inert texts /eight exact full-file peers /four resolved
  first parents /eight archive inventories**, retaining nine missing-path requests
  separately from properly resolved helpers. Five pins:
  -049_CONTEXT **a5ac6a52fe9fccd6221687dc039566e8a55ba6b8c2ab1b77c7bb63b3b22f6bf4**;
  -049_PEERS **9d3231deac9e74692c13e02ee46f4ceac93274dd7222251a3b6ba77dcb720f71**;
  -049_CONTRACTS **e6ec381af692970ea9df7022b480fccec3efcf1ee18f9e3352c5f6c8a30d4bf6**;
  -049_DELIVERY **65b91080b12bc3709eed9d732dde315d2169e1e50f4a97b59f1fa8d907dfb465**;
  -049_UI **8f8c1baec7e466d1de47e0036180a43e66ced44f1d4fb601b9d1e2e86bb4c900**.
  Named historical contracts are not installed/all-version/deployed proof; IETF
  HTTPS text uses TLS-verified curl after Python CA validation failure, retaining the
  provenance note. No retained program, payload, vulnerability-target request or
  upstream test executes; evidence remains adjudication-only.

## Previous continuation: 29 October 2026, batch049

Discovery remains742/742, draftv0.42/113 leaves and pendingv0.1/25-parent hierarchy.
Consolidation: **657 /742 /85 remaining /664 historical records**. Proposals:
**6 conditional retain /273 missing-context /77 existing-contract /123 selected-attribution /
56 paired-negative /68 security-boundary /4 task-scope /25 feature /25 nonrepair**.
Inventory: **4,026 historical anchors /3,976 current anchors /154 supplemental files /
3,672 embedded texts**, plus standalone enum template. All **173 own-tool tests passed**
in954.498s, covering exhaustive rdiffweb selection/family preservation, mandatory
residual paired-negative deferral, promotion rejection and exact archive-peer/parent
agreement. Final refresh/check/build/check verifies seven generated artifacts and
all45 protected inputs.

Preserve all833 ledger events, SHA256
**e9d9086397f5b960af9df2784a0e0073bf7afeaa9b5edceca61b382bc9e8744a**,
prior authored evidence, canonical bytes/splits and45 protected inputs. Approval remains
pending/not ready. Before-only budget/ordinary-knowledge policy remains unfrozen;
no selective helper/caller/global/after/label/test/advisory injection. No retained program,
payload, vulnerability-target request or upstream test executes. Next inspect all four
MLflow candidates/all statuses/null categories, then remaining four-row repositories.

## Consolidation batch050: MLflow — 30 October 2026

- All four candidates/four families, including both supported and both ambiguous
  discovery findings. One missing-context and three security-boundary deferrals.
- Card context data is not recursively compiled template source. Matched fixed
  producers, executable recipe Python and pre-render card unpickling leave a distinct
  lower-trust rendering boundary unresolved. Named Jinja sandbox limits private/internal
  attribute access, not HTML output, pickle execution or resource consumption.
- Actual experiment/store/run/URI/model-registry/artifact-reader contracts support a
  conditional POSIX fragment-to-false-local-root read chain. Selected handler rejects
  nonempty fragments; companion scheme check separately fixes nonlocal run-root use.
  Do not attribute sibling effects to selected handler or certify old stored metadata.
- Earlier remote-file classifier has a matched default-deny model-source guard and
  deliberately dangerous opt-out warning of arbitrary file access. POSIX authority
  stripping is real but opt-out enablement alone does not demonstrate an unauthorized
  default-policy bypass. Windows UNC behavior differs. After rejection and opt-out
  removal are intentional safety tightening, not automatic compatibility regression.
- Unsupported Content-Type reflection reaches named Flask HTML error response, but
  exact user-creation route is authenticated/admin-only. Constant after text bounds
  this reflection; arbitrary custom-header requests do not alone establish victim
  document rendering or unauthenticated XSS. Browser delivery remains unresolved.
- Batch050 SHA256 **9f5a5f6ece6c5009f52f9f31f27ef28e92f35a10fe6c2a1b04fb3c0c24af885c**.
  **64 anchors /four pins /515 inert texts /eight peers /four first parents /eight
  archive inventories**. Supplemental SHA256 pins:
  -050_CONTEXT **e34b52f8c79684e70d194e51eee2c91ddd14885479591460c177718f24f31cfc**;
  -050_PEERS **0d3ecf4d554cda06c9ca434f11d8c2995d9d0bcbfb00398b5c30fa83b4e4a65f**;
  -050_CONTRACTS **819b8a8924654eee5e8d8121b853bf05be58438b413bacbc503ae9af0e10563b**;
  -050_DELIVERY **d9b707e7997f4efe077892fa36634b2cbc6f385e325212052e6146c38b7dab4d**.
  Missing-path provenance remains retained. Named versions are comparisons, not
  installed/all-version/deployed certification; all retained text remains inert.

## Previous continuation: 30 October 2026, batch050

Discovery remains742/742, draftv0.42/113 leaves and pendingv0.1/25-parent hierarchy.
Consolidation: **661 /742 /81 remaining /668 historical records**. Proposals:
**6 conditional retain /274 missing-context /77 existing-contract /123 selected-attribution /
56 paired-negative /71 security-boundary /4 task-scope /25 feature /25 nonrepair**.
Inventory: **4,090 historical anchors /4,040 current anchors /158 supplemental files /
4,187 embedded texts**, plus standalone enum template. All **177 own-tool tests passed**
in856.851s, covering exhaustive mixed-status MLflow selection, deferral promotion
rejection, distinct historical URI guards and exact archive-peer/parent agreement.
The first run exposed stale expected totals in the simulated discovery-revision test;
those expectations were corrected before the full passing rerun. Final
refresh/check/build/check verifies seven generated artifacts and all45 protected inputs.

Preserve all833 ledger events, SHA256
**e9d9086397f5b960af9df2784a0e0073bf7afeaa9b5edceca61b382bc9e8744a**,
prior authored evidence, canonical bytes/splits and45 protected inputs. Approval remains
pending/not ready. Before-only budget/ordinary-knowledge policy remains unfrozen;
no selective helper/caller/global/after/label/test/advisory injection. No retained program,
payload, vulnerability-target request or upstream test executes. Next inspect all four
Starlette candidates/all statuses/null categories, then remaining four-row repositories.

## Previous continuation: 30 October 2026, batch051 — requested batches of10

Operational schedule `CATEGORY_AUDIT_CONSOLIDATION_BATCH_PLAN_051_059.json`
(SHA256 `4e3ac55537b81febeb642123f9d9b3daa63acc59ee2779d66a704bd58c79a98a`)
groups remaining81 as **eight tens plus one singleton**, retaining whole repository
queues/dependence. Scheduling establishes no adjudication, approval or issue count.
Batch051 completes Starlette4/Horizon3/MSS3, four mechanical families:
**3 missing-context /4 selected-attribution /2 security-boundary /1 paired-negative**.
Preserve nested MSS overlap and coordinated Starlette count-policy attribution.
MSS upload repair introduces invalid-path404-to-TypeError via safe_join None forwarded
to os.fspath. Horizon earlier signed-cookie default differs from later cache sessions;
default fixation/cookie replay claims remain bounded. Later login redirect has the
matched hidden-next/form/Location chain, separate from preexisting key cycling.
Batch SHA256 `539179db2d6984d45d6d71a493831e37b908570100b49544d1333cf1218d1b40`;
122 anchors/four pins/150 inert texts/20 peers/four parents/eight archive inventories.

**671/742 consolidation /71 remaining /678 historical records**. Proposals:
**6 retain /277 missing-context /77 existing-contract /127 selected-attribution /
57 paired-negative /73 security-boundary /4 task-scope /25 feature /25 nonrepair**.
Inventory **4,212 historical anchors /4,162 current anchors /162 pins /4,337 embedded
texts**, plus enum template. **183 own-tool tests passed in807.959s**; generated and
protected-input verification passed. Preserve ledger833 SHA256
`e9d9086397f5b960af9df2784a0e0073bf7afeaa9b5edceca61b382bc9e8744a`, source bytes,
splits,45 protected inputs and immutable evidence. Approval/before-only context policy
remain pending. Next10: Sentry4/QAnything4/SciPy2. No retained program, payload,
vulnerability-target request or upstream test executes.

## Previous continuation: 30 October 2026, batch052 — Sentry/QAnything/SciPy

Batch052 records all **Sentry4/QAnything4/SciPy2** training candidates, four mechanical
families: **7 missing-context /1 selected-attribution /1 security-boundary /1
paired-negative**. SHA256
`8c784833d8f5d2ad518f2158d7a425e884f4165e5461a3084d38ade6eefff702`;
**142 anchors/four pins/227 inert texts/20 exact peers/four parents/eight inventories**.
QAnything deletion's second after UPDATE reuses user-first arguments for id-first
placeholders, introducing ordinary child soft-delete failure; explicit after regression
and unresolved selected old UPDATE gates remain separate. Name-query helper lacks a
retained caller; actual existence/filename producers support distinct local findings.
Connector8.2.0 client-side substitution is not universal SQL-mode certification; preserve
wrong-path404 provenance and separately retained corrected paths.

Sentry CORS distinguishes Python cookie setting None from literal SameSite=None and
same-site from same-origin. Conditional readable credentialed response requires actual
host control, basehost, cookies and endpoint permission. Outer/nested overlap remains
one representation family. Download negatives distinguish project artifact bundles
from organization release files; no universal project-isolation claim. SciPy trusted
root selection is tied to actual old shelve/compiler consumers and POSIX assumptions,
not all-platform/race-free/inner-symlink certification. IETF text retrieved using
TLS-verified curl fallback, without disabling verification.

**681/742 consolidation /61 remaining /688 historical records**. Proposals:
**6 retain /284 missing-context /77 existing-contract /128 selected-attribution /
58 paired-negative /74 security-boundary /4 task-scope /25 feature /25 nonrepair**.
Inventory: **4,354 historical anchors /4,304 current anchors /166 supplemental files /
4,564 embedded texts**, plus enum template. **187 own-tool tests passed in897.269s**;
final refresh/check/build/check passed: seven generated artifacts reproducible and
all45 protected inputs unchanged. Preserve ledger833 SHA256
`e9d9086397f5b960af9df2784a0e0073bf7afeaa9b5edceca61b382bc9e8744a`, source bytes,
splits,45 protected inputs and immutable evidence. Approval/common before-only policy
remain pending. Next10: operator2/django-s3file2/DRF2/mjml-python2/Gerapy2. No retained
program, payload, vulnerability-target request or upstream test executes.

## Previous continuation: 31 October 2026, batch053 — operator/Gerapy/DRF/s3file/MJML

All ten planned training candidates are recorded across six mechanical families:
**4 missing-context /3 selected-attribution /1 security-boundary /2 paired-negative**.
Batch SHA256 `178b823b807494b6e8a7bc6fe188d9951c68d6dc8d73400562a50b4bbb821b95`;
**125 anchors/four pins/241 inert texts/20 exact peers/six parents/12 inventories**.
Operator secret argv reaches the matched chained-exception logging hook; after uses
private temporary files and named Juju file transport. Gerapy parse removes the shell
but retains shell-only apostrophes around literal JSON argv, dropping ordinary options
in the matched CLI converter. S3file helper prints a computed valid folder capability
before rejecting the submitted token: disclosure remains conditional on lower-trust
stdout/log access. Both introduced regressions require paired-negative deferral.
DRF linkifier is coordinated with sibling autoescape policy; long-header escaping lacks
a retained lower-trust header writer. MJML preserves entity-escaped text through the
matched component consumer, not arbitrary HTML sanitization. Preserve nested/outer
overlap and the distinction between selected local repair and application delivery.

**691/742 consolidation /51 remaining /698 historical records**. Proposals:
**6 retain /288 missing-context /77 existing-contract /131 selected-attribution /
60 paired-negative /75 security-boundary /4 task-scope /25 feature /25 nonrepair**.
Inventory: **4,479 historical anchors /4,429 current anchors /170 supplemental files /
4,805 embedded texts**, plus enum template. **192 own-tool tests passed in1263.771s**;
final refresh/check/build/check passed: seven generated artifacts reproducible and
all45 protected inputs unchanged. Preserve ledger833 SHA256
`e9d9086397f5b960af9df2784a0e0073bf7afeaa9b5edceca61b382bc9e8744a`, source bytes,
splits,45 protected inputs and immutable evidence. Approval/common before-only policy
remain pending. Next10: keycloak-httpd-client-install2/querybook2/ihatemoney2/zenml2/Zope2.
No retained program, payload, vulnerability-target request or upstream test executes.

## Latest continuation: 31 October 2026, batch054 — five two-row queues

All keycloak-httpd-client-install2/querybook2/ihatemoney2/zenml2/Zope2 candidates recorded
across seven mechanical families: **5 missing-context /1 security-boundary /4
paired-negative**. Querybook actual callback exemption/string HTML response and escaping
contracts retained; CSP/browser/backend assumptions remain conditional. ihatemoney used
get reaches mutations, whereas get_by_name lacks a retained production caller. Zope
matches pinned traversal4.4.1/AccessControl5.0 and preserves trusted/single-underscore
exceptions. No all-application authorization/sandbox claim.

Keycloak log default feeds empty dirname into unchanged makedirs, introducing startup
failure; password-file/stdin branch dereferences undeclared Namespace attribute,
introducing advertised replacement-transport failure. ZenML ordinary SQL get_user projects
activation_token as default None; unconditional update assignment explicitly persists
that None through exclude_unset, invalidating a pending invitation on permitted profile
updates. Introduced in earlier candidate, residual in later password candidate. Do not
claim absent old is_admin was writable or project new reauth policy onto old requirements.

Original authored batch054 SHA256
`b93b5e369aa4b26097ecb4200d368017b6262b5dcca400886be458bba1e811a0` could not validate
three identical Keycloak ref/path duplicates in collected context. Preserve that file
and all evidence unchanged. Current `CATEGORY_AUDIT_CONSOLIDATION_BATCH_054_CORRECTED.json`
SHA256 `d26f07fafbd0affcb688444ef449a6d2bfe442f055c309ad8dcf19dce6cbdbd4`
uses a separately pinned445-source unique lookup view; all448 original entries and
fourteen archive inventories remain pinned. No validator relaxation or source-byte edit.
Original never entered validated review history; current review revision1 is explicit.
133 anchors/six pins/946 embedded texts including the duplicated lookup view, not946
independent sources;20 exact peers/seven first parents/fourteen archive inventories.

**701/742 consolidation /41 remaining /708 historical records**. Proposals:
**6 retain /293 missing-context /77 existing-contract /131 selected-attribution /
64 paired-negative /76 security-boundary /4 task-scope /25 feature /25 nonrepair**.
Inventory **4,612 historical anchors /4,562 current anchors /176 supplemental files /
5,751 embedded texts**, plus enum template. After correcting lookup provenance,
**196 own-tool tests passed in1291.132s**; final refresh/check/build/check passed:
seven generated artifacts reproducible and all45 protected inputs unchanged.
Ledger833 SHA256 `e9d9086397f5b960af9df2784a0e0073bf7afeaa9b5edceca61b382bc9e8744a`,
canonical bytes/splits and45 protected inputs preserved. Approval/common before-only
policy pending. Next planned055: psiturk3/mayan-edms2 plus five singletons. All retained
programs, payloads, vulnerability-target requests and upstream tests remain unexecuted.
