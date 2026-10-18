# Expanding security coverage: HaPy-Bug plus original CVEfixes

**Date:** 17 October 2026  
**Purpose:** Measured research/data-preparation evidence, not EPP submission prose.

**18 October admission update:** [The updated verified admission snapshot](SECURITY_ADMISSION_FINDINGS.md) contains **335 admitted additional pairs / 208 new CVEs**, yielding **1,052 combined pairs and 273 security CVEs**. All 1,186 candidates now have recorded triage decisions: 335 admitted, 344 rejected, 507 quarantined. The quarantines include 467 unresolved issue-context/attribution cases and 40 source failures; they are not completed contextual adjudications or confirmed negatives. All five previous upstream retrieval blockers were resolved with exact source checks and explicit alternate-location provenance where needed. The historical four-case and candidate-pool figures below describe the earlier audit, not the current admitted count. Superseded bulk exports referenced below were removed during [workspace cleanup](README.md#cleanup--18-october-2026); the filtered pool and current evidence remain. The provisional combined test has 62 distinct security CVEs; the experimental protocol is not frozen.

## Decision and answer

**Keep HaPy-Bug as the prepared mixed-issue base and use a reviewed subset of original CVEfixes to expand security coverage.** No further source shortlist is needed for this expansion.

The available material is substantially larger than the initial 65-CVE HaPy-Bug subset. After overlap filtering and exclusions identified in the first source/advisory review, the expansion pool contains **1,186 candidate function pairs associated with 507 additional distinct CVE IDs**. Combined with the base, this represents **up to 572 security CVEs**, subject to issue-relevance validation. This is a measured candidate pool, not 572 validated evaluation vulnerabilities.

Four sampled additional function pairs already have source/advisory support for their relevance. The rest have not all been reviewed. The final retained count and final held-out evaluation size remain unestablished.

## What was measured

| Stage | Function pairs | Distinct CVEs | Meaning |
|---|---:|---:|---|
| Existing HaPy-Bug security subset | 153 | 65 | Published human line-purpose references and reconstructed source context |
| Initial original-CVEfixes production-function candidate pool | 1,354 | 578 | Changed methods linked to security fixes; not automatically vulnerable methods |
| Additional candidates after overlap/structural filtering | 1,189 | 508 | Beyond HaPy-Bug, before the ten-case source/advisory review |
| Additional candidates after known review exclusions | **1,186** | **507** | Remaining expansion review pool |
| Four source/advisory-supported sampled additions | 4 | 4 | Preliminary assistant inspection, not independent human gold adjudication |

The 1,189-pair initial expansion pool spans 297 repository identities. Within it, 1,090 pairs / 467 CVEs are in repositories outside the retained HaPy-Bug base. The larger candidate pool is therefore not merely additional examples of the same 65 CVEs.

There are **1,903 candidate pairs across both issue groups** in the combined research export: 717 HaPy-Bug base pairs plus 1,186 expansion candidates. The general-bug portion remains the base's 564 pairs. These totals must not be reported as a fully validated final dataset.

## Overlap and quality filtering

The audit compares original CVEfixes candidates against:

- All **296 distinct CVE identities** found anywhere in the official HaPy-Bug case metadata, not just the 65 surviving in the prepared subset.
- Available recorded fixing hashes across the whole HaPy-Bug release.
- Both versions of every retained HaPy-Bug function, using exact source/AST hashes and lexical five-token-shingle Jaccard similarity of at least 0.90.
- Additional provenance attached to identical AST-pair records.

It excludes docstring-only AST changes and the known Copyparty `set_k304` change whose author explicitly says it is unnecessary to the vulnerability fix. It also checks that retained CVEfixes before/after method IDs link to the expected file-change record.

These controls establish new candidate CVE identities and defined code-overlap exclusions. They are not a proof of semantic independence, complete fork detection or correct issue-level labels.

## Ten-case upstream/source review

Selection was fixed and nonrandom: the first ten lexical distinct repositories/CVE groups with before-functions of at most 60 lines. Both function bodies matched their upstream first-parent/fix snapshots for **all ten pairs**, when ignoring docstrings. Nine cases had a corresponding advisory returned by GitHub's advisory API. The missing API result for the tenth is not evidence that its vulnerability is invalid.

| CVE | Review outcome | Evidence/reason |
|---|---|---|
| CVE-2024-34359, llama-cpp-python | Source/advisory-supported candidate | Advisory names the unsandboxed template environment; the selected constructor introduces an immutable sandbox. |
| CVE-2024-37301, document-merge-service | Source/advisory-supported candidate | Publisher identifies template-injection RCE; the selected environment factory switches to a sandbox in the referenced patch. |
| CVE-2019-25066, Ajenti | Source/advisory-supported candidate | Advisory references the patch; author identifies shell injection; selected authentication method quotes the interpolated username. |
| CVE-2024-4340, sqlparse | Source/advisory-supported candidate | Advisory's stack trace reaches `flatten`; the selected patch converts uncontrolled recursion errors to the library's exception. This does not certify elimination of every resource-exhaustion issue. |
| CVE-2024-26134, cbor2 | Excluded from this Python expansion | The advisory says the recorded commit introduced the crash, not fixed it; the reported corruption concerns the native decoder. Python methods changed in that commit are not valid vulnerability/fix labels for this issue. |
| CVE-2015-6240, Ansible | Selected function excluded | The selected `connect` method changes a docstring and diagnostic message, not the reported symlink-escape behaviour. |
| CVE-2024-30251, aiohttp | Needs additional context | Advisory's minimal security fix is in `_read_chunk_from_length`; sampled `_get_part_reader` only propagates parameters. |
| CVE-2021-4041, ansible-runner | Needs additional context | Sampled documentation-command builder is not established as the vulnerable shell-execution function. |
| CVE-2018-1000089, django-anymail | Needs additional context | The security effect depends on Django's settings-name redaction and configuration. |
| CVE-2024-31451, DocsGPT | Needs additional context | Source change restricts URLs before writing files; complete route/write context and detailed reference need tracing. |

The review removed three candidate pairs: all candidates tied to the cbor2 CVE above and the sampled Ansible diagnostic-only function. It did not discard all Ansible records for that CVE. The four context-dependent sampled functions remain review candidates and are not admitted as validated evaluation references.

**Review provenance:** These decisions are assistant inspection of source/advisory evidence. No downloaded programs, exploits or project tests were executed. They are not a new independent human annotation exercise. The nonrandom sample does not establish a 40% population acceptance rate.

## Licensing

Original CVEfixes v1.0.8 and HaPy-Bug v1 both publish their datasets under **CC BY 4.0**. The original CVEfixes archive checksum and licence were already verified and preserved. Attribution and applicable upstream code terms must be retained; dataset licensing does not override repository/file licences. This expansion does not rely on the unresolved standalone BugsInPy framework licence or on PyResBugs.

## Implication for final evaluation

The project is not restricted to the initial 65 security CVEs. There is a concrete, already-extracted expansion pool to curate. However:

- 507 additional CVE identities are a candidate count, not an admission count or guarantee of statistical independence.
- Source matching alone does not establish that the selected function contains the reported issue, as the rejected examples demonstrate.
- HaPy-Bug human line references and CVEfixes source/advisory-derived references have different annotation provenance. Preserve and report that difference; researcher confirmation is needed before treating new references as gold evaluation labels.
- Once the admissible additions are fixed, construct the combined evaluation groups by repository, CVE, fixing history and duplicate code. Existing HaPy-only splits or the earlier cross-validation suggestion are not a locked final protocol for this expanded corpus.
- Report final evaluation size in distinct CVEs and repository/code groups as well as function counts. Neither a particular held-out CVE count nor a final training method has been established by this source audit.

## Reproduction and artefacts

Run with the existing prepared inputs in the project directory:

```sh
python SECURITY_EXPANSION_AUDIT.py audit --output-dir "$OUT"
python SECURITY_EXPANSION_AUDIT.py probe --output-dir "$OUT" --cache-dir "$CACHE"
python SECURITY_EXPANSION_AUDIT.py review --output-dir "$OUT"
```

- `CVEFIXES_SECURITY_EXPANSION_AUDIT.json` — structural/overlap counts and exclusions.
- `CVEFIXES_SECURITY_EXPANSION_CANDIDATES.jsonl` — initial 1,189 additional candidates.
- `CVEFIXES_SECURITY_EXPANSION_FILTERED_CANDIDATES.jsonl` — 1,186 candidates after known review exclusions.
- `CVEFIXES_SECURITY_EXPANSION_REVIEW_SAMPLE.md` — sampled descriptions, commit messages and source diffs.
- `CVEFIXES_SECURITY_EXPANSION_UPSTREAM_PROBES.json` — source URLs/hashes and retrieved advisory evidence.
- `CVEFIXES_SECURITY_EXPANSION_REVIEW_RESULTS.json` — explicit decisions, rationales and remaining candidate counts.
- `CVEFIXES_SECURITY_EXPANSION_SUPPORTED_SAMPLE.jsonl` — four source/advisory-supported candidates, with review provenance.
- `HAPY_CVEFIXES_EXPANSION_CANDIDATE_PAIRS.jsonl` — combined candidate pool; annotation quality is not uniform and this is not a frozen training/evaluation release.

The script passed Ruff `E9,F` checks. Original release sources: https://zenodo.org/records/13118970 and https://doi.org/10.6084/m9.figshare.24448663.v1 . Specific advisory URLs are recorded per sample in the upstream probe evidence.
