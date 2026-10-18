# CVEfixes security admission — full-pool triage snapshot

**18 October 2026. Research/data preparation notes, not EPP submission prose.**

## Actual result

The updated conservative admission snapshot adds **335 security function pairs covering 208 new CVEs across 151 repository identities** to the prepared HaPy-Bug base. This supersedes the previous 332-pair / 207-CVE snapshot. Each admitted before/after function, including decorators and docstrings, matches its referenced first-parent/fixing-commit source. Full source files and their hashes are preserved locally. Required companion functions, including middleware bindings, path converters, directory checks and transfer helpers, are separately matched and preserved. Essential configuration and unchanged modules can additionally be bound by explicit review-time byte hashes at the exact fixing commit. Alternate repository locations are explicit provenance, not silently substituted identities.

| Material | Function pairs | Security CVEs |
|---|---:|---:|
| HaPy-Bug prepared base | 717 (153 security, 564 general-bug-origin) | 65 |
| Admitted CVEfixes additions | 335 security | 208 |
| Combined updated snapshot | **1,052 (488 security, 564 general-bug-origin)** | **273** |

“Admitted” means accepted into this source/advisory-supported research snapshot. The CVEfixes issue-relevance decisions were made by the assistant. They are not independent human gold annotations or reproduced vulnerability tests, and should not be reported as such. HaPy-Bug's published human line-purpose references retain their separate provenance.

## Coverage of the admission work

- The entire **1,186-pair / 507-CVE candidate pool** received source/evidence processing.
- Official CVE records were retrieved for **all 507 CVEs**: all are published; no record-fetch failures. Associated OSV advisories were available for 156 CVEs. This difference is not an issue-validity classification.
- **1,146 pairs** passed released-full-source parsing, diff-hunk verification, metadata matching, qualified-function identity and executable-change checks. **40 pairs** were quarantined for source-context problems, largely historical syntax or changed qualified names.
- **All 1,186 candidates now have recorded triage decisions**. The previous 124 inspections were supplemented by a hash-bound, gap-checked queue covering the other 1,062 records. There are no missing or duplicate initial queue indices.
- Issue-level triage was possible for the **1,146 source-context-passing pairs**. The 40 source failures are recorded separately; they are not counted as successful issue-level inspections.
- **335 pairs were proposed for admission**. All 335 passed source retrieval and exact function verification. The previous five HTTP 404 blockers have been resolved.
- Final decisions: **335 admitted, 344 rejected, and 507 quarantined pairs**.
- Quarantine breakdown: **467 need further issue-context, attribution or fixing-direction evidence; 40 fail source-context verification; zero fail upstream retrieval**. Quarantine is not a claim that a function is safe, irrelevant, or invalid. Full-pool triage is complete; full contextual adjudication is not.

Rejections include unrelated Calibre-Web refactoring bundled with SSRF fixes, Python wrappers linked to native-code vulnerabilities, advisory-scanner changes rather than vulnerable application code, and attempted fixes which remain bypassable. For example, a slash-only redirect check still accepts protocol-relative targets, and an early yt-dlp quote-doubling patch is explicitly described as incomplete by the later advisory. Rejection applies to the selected pair, not automatically to the entire CVE.

Other quarantines need helper/caller/configuration context, have incomplete visible fixes, or lack precise attribution among multiple CVEs attached to the same commit. In admitted multi-CVE commits, only individually supported CVEs are issue labels; broader commit/duplicate links remain available for conservative split grouping. CWE fields remain source CVE-level metadata, not adjudicated function-level labels.

**The 467 contextual quarantines remain unresolved.** Their compact source-difference/advisory triage is not a claim that all helper/caller/template or compiler/protocol semantics have been fully traced. Some differences are explicitly truncated; those cases were not admitted from the truncated view. The 507 additional candidate CVEs and possible 572-CVE combined pool must not be substituted for the actual **208 additional / 273 combined admitted CVEs**. No population quality estimate is inferred from the admitted subset.

### Detailed contextual follow-up

- Queue 12–13: inspected the complete Horizon callers and middleware request-class binding. The new logout helper clears the cached user and calls session.flush(), replacing clear() without session-key rotation. Both pairs were admitted with preserved middleware evidence.
- Queue 18: inspected Nova's privileged injection path and realpath containment helper, including the slash-delimited root boundary. Admitted for dot-dot traversal CVE-2012-3360 only. Queue 17 and 19–21 remain quarantined with specific symlink/privilege-boundary reasons; unprivileged realpath is not certified to resolve root-only-readable links.
- Queue 27: verified that random_generator is bound to random.SystemRandom() and supplies all sixteen authenticator bytes. Attributed only CVE-2013-0294, not the separately linked packet-ID CVE.
- Queue 47: inspected the full JSON filter and actual module escape table. Both serialization branches escape ampersand, less-than and greater-than as literal Unicode escapes before mark_safe.
- Queue 935–937: the preserved MJML advisory explicitly identifies their commit as introducing the entity-unescaping vulnerability. Rejected these introducing/reversed-direction pairs as fixing examples. Queue 938 is CSS compatibility maintenance, not the vulnerable general entity-decoding function. Queue 939–940 contain the corrective removal of formatter=None; both are admitted, while their nested/enclosing overlap stays grouped.
- Queue 253: inspected the existing hostname validator, unchanged anchored regex, new Matrix-server-name validator and port parser. The selected commit broadens format support to IPv6; it does not add the missing validation/internal-address restriction described by the SSRF advisory. Rejected this compatibility pair.
- Source retrieval: corrected GitLab routing for both Mayan EDMS pairs. Located the two historical LoLLMs commits in ParisNeo/lollms_legacy and the exact MNBikeways commit in Marvin35/database. For alternate locations, additionally required matching commit SHA, first parent and complete released module text on both sides. Original repository identities are retained for grouping; the alternate source locations and full GitHub commit records are preserved explicitly. This is not a claim of ownership transfer or exhaustive fork discovery.

That earlier follow-up added seven newly supported pairs plus five previously supported pairs recovered from source retrieval, increasing admissions from 272 to 284.

### Previous contextual batch

- Queue 23–24, 26 and 28: traced Bcfg2 Trigger arguments into shell-free Popen, Nova affinity hints into one API lookup plus dictionary access, Django password-reset Host values into delimiter validation, and pyChao's advisory-named commands into parameterized SQLite queries. Four pairs admitted with exact companion evidence.
- Queue 31–32: inspected SciPy's complete directory selection, cache reuse and fallback creation chains. POSIX directory checks require ownership, exact 0700 permissions and non-symlink status; fallback creation uses tempfile.mkdtemp. Two pairs admitted without asserting equivalent Windows ACL checks or general race freedom.
- Queue 79–87: six Ansible chroot/jail/zone transfer pairs replace host-side copying with streamed dd inside the restricted environment. Three exec_command pairs were rejected because they preserve already-isolated command execution and merely extract shared helpers. Admission addresses the documented symlink namespace escape, not arbitrary shell filenames or all transfer behavior.
- Queue 91–106: sixteen Radicale path conversion/storage functions admitted after tracing direct calls, the filesystem property and multifilesystem inheritance. The converter rejects Windows drive/head components before joining below the base. These functions represent one CVE; separate filename parameters and symlink behavior are not certified safe.
- Queue 112–115: four Swauth pairs admitted after checking the SHA-512 helper and imported Swift hash-prefix/suffix binding. Local token-object URIs use concealed identifiers instead of bearer tokens. Remote-auth protocol and every possible logging site remain outside this claim.
- Queue 52, 61 and 73–75: rejected Tornado token-comparison compatibility, Galaxy's original-filename compatibility and Pulp URL-prefix/API forwarding changes. Their vulnerable response-generation, template-sanitization or certificate-retrieval operations occur elsewhere.
- Queue 6 remains quarantined: constructing an argv list while retaining shell=True does not establish a working intended POSIX CSR-generation counterpart. Queue 822–824, 830 and 832 also remain quarantined after full MLflow validation/caller tracing: the validator already rejects decoded traversal; precise accepted-input/downstream interpretation and multipart-path attribution are still needed. The public Huntr reference returned a loading shell rather than its report text.
- Fixed a concurrent source-cache publication race: complete curl responses are now published with an atomic rename. An eight-worker same-URL inert-fixture check passed. Three initially transient Radicale source lookups were rechecked against complete modules; all 316 proposed admissions then matched. No source-matching criterion was relaxed.

That batch added **32 admitted pairs and eight new CVEs**, and recorded eight additional rejections. Quarantines decreased from 653 to 613.

### Continuing review and workspace cleanup

- ZenML queue 870–890 and the original-ledger BaseArtifactStore._register pair: traced the decorator, method registration and local resolved-path checks. The new check uses startswith(root) without a component boundary, accepting a resolved sibling such as /srv/store-other/file for /srv/store. Excluded these 22 proposed fixing pairs; no endpoint exploit was run.
- Sydent queue 254–256: rejected IPv6/port-format compatibility changes, consistent with the earlier queue-253 review. Queue 259 only changes reporting of an exception raised by the actual verifier and is also rejected. Queue 257–258 remain quarantined after tracing default IP ranges, mapped-address generation, DNS resolver filtering and client construction; numeric-IP endpoint behavior and federation binding still need evidence. Queue 260 adds hostname validation to an onbind POST, while the advisory specifies induced GETs; attribution remains unresolved. Queue 261's exact-commit imported helper has a missing closing parenthesis; retain the caller outside admission rather than silently substituting a later helper.
- aiohttp queue 976–981: rejected six form-data compatibility/serialization pairs. The preserved advisory explicitly identifies the EOF update in _read_chunk_from_length as the minimum infinite-loop fix, distinguishing it from these additional handling changes.
- Nautobot queue 776, 789 and 790: admitted the rendered-string trust-boundary correction and its custom-link/job-button consumers. Inspected full grouped/error paths and HTML constants. The helper strips implicit SafeString status so format_html actually escapes user-authored rendered values; exact helper/consumer modules are preserved. This does not establish independent URL-scheme filtering.
- Zulip queue 648–651: the official CVE description and GHSA-wm83-3764-5wqh identify their commit as introducing the S3 issue, not fixing it; rejected. Queue 653–654 are forced-download API support and queue 658 is local-disk compatibility, outside the advisory's affected configuration; rejected.
- Zulip queue 655–657: admitted after tracing serving callers through S3 upload/presigning and the actual nginx header/cache configuration. Browser-supplied text/html content stored under a .png filename no longer gets a filename-derived inline override; nginx preserves S3's content-type-aware disposition. The MIME allowlist excludes text/html. Required nginx files and the unchanged MIME module are now review-hash-bound at the exact fixing commit, archived and independently checked offline. This is production-S3 scope, not a claim about every historical object or reproduced browser behavior.

This continuation resolves **45 further candidates: six admissions and 39 rejections**, adding one distinct CVE. Quarantines decrease from 613 to 568. Four additionally inspected Sydent cases retain specific evidence blockers. Full contextual adjudication remains in progress.

Workspace cleanup removed **54 obsolete project files and four obsolete temporary files**, freeing **13,242,124,837 bytes (about 13.2 GB)**. Removed superseded unselected/combined exports, old SWE-CARE trial outputs, 37 generated Markdown review views, the already-extracted original CVEfixes archive, a logically duplicate cached database and two failed extractions. The retained database passed integrity checking; selected data, source/annotation evidence, immutable queue and review histories remain available. See [README.md](README.md) for the inventory and current entry points. The numbered Markdown views are regenerable summaries, not required review evidence. A fresh original extraction would require re-downloading the removed archive using its preserved release metadata.

### Response limits, extraction paths and dependency follow-up

- Sydent queue 251–252: admitted after tracing the complete reader protocols and actual federation callers. Registration supplies a 5 KiB GET budget and signing-key retrieval 50 KiB; an omitted budget still permits unbounded reading. The no-body POST path now aborts unwanted response bodies rather than accumulating them. Exact-commit reader and notification modules are hash-bound context. Scope is outgoing response exhaustion, not incoming-request/disk limits or an exact peak-allocation guarantee.
- py7zr queue 610: admitted the entry-name traversal correction after tracing public extractall, absolute destination construction and resolve-before-relative_to. Queue 609 writes archives rather than extracting hostile archives; queue 611 and the original-ledger Worker.extract pair only forward the root to workers, so these three were rejected. Queue 612 remains quarantined: the default root None is passed to a link-target helper which calls path.is_absolute(). A later repaired helper was not substituted. Entry-name correction is not a universal symlink/race guarantee.
- HTTPie queue 337–344: inspected full session/config modules and the advisory covering both CVEs. Seven unresolved generic-config, state-construction, expiry and header-compatibility pairs were rejected; the already-rejected management-parser pair was confirmed. The lost response-cookie domain belongs to the separate cookie serialization/accessor correction, not every dependency in its commit. Legacy domainless sessions are warned about rather than automatically rebound.
- Starlette queue 692/694 and original-ledger Request._get_form: admitted after tracing request.form through finite defaults, parser callbacks and count checks before allocation. Defaults are 1000 files and 1000 fields; the exception propagates to the existing HTTP 400 boundary. Queue 689/691/693 only relocate event/state handling and were rejected. This addresses many-small/empty-parts exhaustion, not byte limits for individual parts, deliberate infinite overrides or complete exception-time cleanup.
- Tandoor queue 472–478 and original-ledger Nextcloud.get_share_link: rejected eight attempted fixing pairs after following exact-commit requirements into validators 0.19.0 and Requests 2.27.1. public=True only filters two named regex groups; IPv6 loopback is accepted by a different alternative, hostnames are not DNS-resolved, and default redirect following is unchanged. Preserved release/module hashes and source excerpts in SECURITY_ADMISSION_DEPENDENCY_REVIEW.json. These are source-based fixing-counterpart decisions, not reproduced exploits. The dependency file explicitly distinguishes excerpts from complete archived modules.

This follow-up inspected 29 candidates, resolving **27 formerly quarantined pairs: six admissions and 21 rejections**, confirming one existing rejection and retaining one specific quarantine. It adds **two distinct CVEs**, reducing quarantines from 568 to 541. Previous review history and the immutable queue fingerprint remain preserved.

### Tenant authorization, source-error reporting and outbound policy

- OneFuzz queue 285/287: admitted the endpoint gate and issuer authorization after tracing Azure-authenticated deployment, exact configured tenant issuers, typed configuration and real allowlist writers. The gate returns HTTP 401 before invoking the endpoint on an authorization error. Exact endpoint binding and authorization modules are hash-bound context. Local JWT signature verification remains disabled and the allowlist cache lasts 60 seconds; neither standalone cryptographic validation nor instantaneous revocation is claimed. Queue 286 and 288–290 are missing-config construction or deployment argument/state plumbing and were rejected.
- Docassemble queue 944–949: rejected six source-error classification/reporting pairs after complete template, choice and parsing inspection. Their DASourceError changes suppress source details for ordinary users; the linked XSS/redirect corrections occur in separate HTML validation and URL normalization operations.
- Synapse queue 209/213: admitted the key-revocation and push-client bindings after tracing actual GET/POST consumers, configured literal-IP checks, direct DNS filtering and the exact proxy implementation. These are configured-policy corrections: the commit does not give every existing deployment private-range defaults or locally filter proxy-resolved target hostnames. Queue 207/208/210/214 are accessor-renaming compatibility pairs and were rejected. Queue 211 passes the reactor as the wrapper's ip_whitelist argument; its broad exception handler can then bypass the literal-IP guard. Queue 211/212 were excluded as ineffective-helper/refactoring counterparts. Queue 205/206 remain quarantined pending actual configuration generation/migration and deployment-policy attribution.

This batch inspected 22 candidates, resolving **20 formerly quarantined pairs: four admissions and 16 rejections**, retaining two specific quarantines. It adds **two distinct CVEs**, reducing quarantines from 541 to 521. These judgments are static source/advisory inspections, not executed vulnerabilities.

### Token/session attribution and Windows template quoting

- rdiffweb queue 547/555/556/558/559/562–564: rejected eight token-activity, token/key creation and transaction-API pairs after inspecting complete functions, actual password-form commits, session loading and password-change revocation. Expired tokens were already excluded. The added SessionObject deletion in set_password is the session-expiration correction; the selected timestamp/return-value and generic persistence changes do not implement it. This does not certify unrelated token ownership or session behavior.
- yt-dlp queue 908/909 and original-ledger shell_quote: admitted three pairs for CVE-2024-22423 after tracing the actual unchanged ExecPP.parse_cmd/run through prepare_outtmpl, shell=True selection, both translation tables and Popen. The Windows shell table replaces percent with %%cd:~,% as specified by GHSA-hjq6-52gw-2g7p. Full helper modules and the exact-commit ExecPP module are preserved; the latter is bound by its reviewed byte hash. The nested/enclosing template pair remains grouped and represents one vulnerability, not two independent issues. No Windows shell or exploit was executed; arbitrary raw templates are not certified safe.
- yt-dlp queue 911/912: rejected default-mode compatibility/argument-formatting wrappers, which do not select the shell percent-escaping table. Queue 913: rejected as the selected CVE fixing pair because its new list-quoting branch is not used by the actual --exec string caller; its command-extension/newline setup is retained as companion evidence. The earlier quote-doubling fix remains excluded rather than retroactively treated as effective.

This continuation resolves **14 formerly quarantined pairs: three admissions and 11 rejections**, adding **one distinct CVE** and reducing quarantines from 521 to 507. Prior review decisions remain in the ledgers' history.

Prioritizing directly visible fixes can favour locally evident flaws over configuration-dependent or cross-function vulnerabilities. This selection bias and the two annotation sources must be reported when interpreting model results.

## Verified provisional combined splits

| Split | Security pairs | General-bug-origin pairs | Total | Distinct security CVEs |
|---|---:|---:|---:|---:|
| Train | 342 | 400 | 742 | 150 |
| Validation | 73 | 83 | 156 | 61 |
| Test | 73 | 81 | 154 | 62 |

These splits are reproducible preparation artefacts, not a frozen experimental protocol. Grouping keeps repository identity, fixing commit, CVE and duplicate provenance, exact text/AST and defined lexical near-duplicates together. The independent offline checker reconstructed **2,104 function versions**, checked **1,617 full-source/context URL snapshots** (including companion functions and required configuration) and **1,875 attached human line references**, and found zero measured cross-split provenance/text/AST or five-token-shingle Jaccard ≥0.90 violations. It also checked the preserved alternate-location commit metadata/full-module matches and the exact-commit URLs and review-time hashes of additional context files.

The provisional test set has **62 distinct security CVEs**, not 273. Rebuilding grouped splits can change their membership and per-split CVE counts; growth in the full dataset does not guarantee growth in a particular split. The test count exceeds the first combined snapshot's 28, but does not establish sufficient precision for every comparison or CWE subgroup. Repository grouping, multiple functions per CVE, nested/enclosing function overlap, label-source differences, paired outcomes and uncertainty must be reflected in the eventual analysis. For example, Spirit contributes many redirect functions for one CVE, not many independent vulnerabilities. Grouped cross-validation remains an experimental-design option, not something implemented here. These counts also do not prove that the training subset is sufficient to develop a useful model.

No semantic-clone/fork completeness or absence of public-model pretraining contamination is claimed. After-code is a documented fixing counterpart, not a universal clean-code negative. General-bug-origin code is not a verified security-negative class.

## Data and evidence to use

- `HAPY_CVEFIXES_ADMITTED_CANDIDATE_PAIRS.jsonl`: 1,052-pair combined snapshot with provenance.
- `CVEFIXES_SECURITY_ADMITTED_PAIRS.jsonl`: only the 335 admitted additions.
- `HAPY_CVEFIXES_ADMITTED_{TRAIN,VALIDATION,TEST}_CANDIDATES.jsonl`: provisional grouped splits.
- `HAPY_CVEFIXES_ADMITTED_{TRAIN,VALIDATION,TEST}_BEFORE_ONLY_INPUTS.jsonl`: opaque identifier, language and before-code only; no CVEs, after-code, commit messages or reference annotations. Original source comments/docstrings are preserved.
- `HAPY_CVEFIXES_ADMITTED_{TRAIN,VALIDATION,TEST}_REFERENCE_INDEX.jsonl`: separate identity/label provenance index. Keep reference material outside detection prompts.
- `SECURITY_ADMISSION_REVIEW_LEDGER.json`: initial 120-case inspection; four prior supported inspections are imported by exact pair ID from earlier review evidence.
- `SECURITY_ADMISSION_REMAINING_QUEUE.jsonl` and `SECURITY_ADMISSION_QUEUE_REVIEW.json`: the other 1,062 records, immutable queue indices/source hashes, decisions and explicit follow-up history. Queue SHA256 is `7c1b985fa5228f7e89f08c95ab1c96f73f42f37f398c11030c4684cdd6010f19`; reviewed source hashes must match current canonical contexts before export.
- `SECURITY_ADMISSION_FINAL_DECISIONS.jsonl`: one recorded admission/rejection/quarantine decision for every input candidate; source-blocked triage is distinguished from issue inspection.
- `SECURITY_ADMISSION_UNRESOLVED_REVIEW.jsonl`: the 507 quarantines with source or issue-context/attribution blocker types. This is the explicit remaining-work register.
- `SECURITY_ADMISSION_DEPENDENCY_REVIEW.json`: pinned external dependency URLs/hashes and excerpts supporting the Tandoor rejection; complete dependency modules are not archived in this file.
- `SECURITY_ADMISSION_CVE_EVIDENCE.jsonl`: official CVE records and retrieved advisories, URLs and hashes.
- `SECURITY_ADMISSION_SOURCE_{CONTEXTS,DECISIONS}.jsonl`: full-source reconstruction results.
- `SECURITY_ADMISSION_UPSTREAM_CHECKS.jsonl`: successful source verification of all 335 proposed additions, including full commit records for alternate repository retrieval and hash-bound additional context files.
- `SECURITY_ADMISSION_SOURCE_LOCATIONS.json`: explicit alternate retrieval locations and reasons; original dataset repository identities remain unchanged.
- `SECURITY_ADMISSION_UPSTREAM_SNAPSHOTS.zip`: 544 distinct complete source/context-file contents for admitted additions and required evidence, including headers and nginx configuration; use with the base's `HAPY_BUG_UPSTREAM_SNAPSHOTS.zip`.
- `SECURITY_ADMISSION_AUDIT.json`, `SECURITY_ADMISSION_INDEPENDENT_VERIFICATION.json`, `SECURITY_ADMISSION_RELEASE_MANIFEST.json`: measured counts, independent checks and fingerprints.
- `SECURITY_ADMISSION_REVIEW_PACKETS.jsonl`: retained review index, **not automated admission decisions**. The keyword score orders inspection only. Generated numbered Markdown views were removed during cleanup; the complete code/evidence and inspection utility remain.

Both dataset releases publish CC BY 4.0 terms. Cite HaPy-Bug v1 (`10.6084/m9.figshare.24448663.v1`) and CVEfixes v1.0.8 (`https://zenodo.org/records/13118970`); retain original repository/file terms and notices. A file-by-file licence audit has not been completed.

## Reproduction

With the existing preserved inputs, Python interpreter and curl available:

```sh
python ADMIT_SECURITY_EXPANSION.py evidence --output-dir "$OUT" --cache-dir "$CACHE"
python ADMIT_SECURITY_EXPANSION.py contexts --output-dir "$OUT" --cache-dir "$CACHE"
python ADMIT_SECURITY_EXPANSION.py packets --output-dir "$OUT" --cache-dir "$CACHE"
# Preserve the existing immutable remaining queue; do not regenerate it.
python ADMIT_SECURITY_EXPANSION.py progress --output-dir "$OUT" --cache-dir "$CACHE"
# Pair-specific decisions are explicit in the initial and queue review ledgers.
python ADMIT_SECURITY_EXPANSION.py upstream --output-dir "$OUT" --cache-dir "$CACHE"
python ADMIT_SECURITY_EXPANSION.py export --output-dir "$OUT" --cache-dir "$CACHE"
python BUILD_CANDIDATE_SPLITS.py split --prefix HAPY_CVEFIXES_ADMITTED --output-dir "$OUT"
python VERIFY_SECURITY_ADMISSION.py --output-dir "$OUT"
```

The final verifier runs offline from preserved ZIPs, without the temporary download cache. Downloaded programs, notebooks, exploits and project tests were not executed. Ruff `E9,F` checks passed for the pipeline, source-fetch utility, read-only inspection utility and verifier. The outstanding work is resolving the explicitly registered contextual/source quarantines where sufficient evidence can be obtained and independently adjudicating labels before freezing the experimental dataset; dataset-source selection remains HaPy-Bug plus original CVEfixes.
