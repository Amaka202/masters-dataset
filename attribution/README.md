# Sources, citations and preparation changes

## HaPy-Bug

- Title: **HaPy-Bug: Human Annotated Python Bug Resolution Dataset**.
- Version: **1**, DOI: <https://doi.org/10.6084/m9.figshare.24448663.v1>.
- Official metadata: <https://api.figshare.com/v2/articles/24448663/versions/1>.
- The complete original author list and licence metadata are preserved in
  `HAPY_BUG_OFFICIAL_RELEASE_METADATA.json`.
- Archive: <https://ndownloader.figshare.com/files/52129358>.
- Archive MD5: `a97ea8d7027fcbbbfdd891de2faaa48b`.

Preparation selected confident, agreeing published human programming/bug-fix
line references, reconstructed complete before/after functions from their
commits, checked executable changes and applied the documented size and source
identity filters. The resulting base has 717 pairs, not the whole release.

## CVEfixes

- Version: **v1.0.8**, release: <https://zenodo.org/records/13118970>.
- Original collection code: <https://github.com/secureIT-project/CVEfixes>.
- Original authors' requested paper citation:

  Bhandari, G., Naseer, A. and Moonen, L. (2021). *CVEfixes: Automated Collection
  of Vulnerabilities and Their Fixes from Open-Source Software*. Proceedings of
  the 17th International Conference on Predictive Models and Data Analytics in
  Software Engineering (PROMISE '21). ACM.
  <https://doi.org/10.1145/3475960.3475985>.

- Release archive SHA256:
  `6acd55aaeb7ffcfc20fdcebf7df88d206f9892ef64b0f2a2e06864d5b44b3a83`.

Preparation extracted Python-related records into a local SQLite database,
excluded whole-release HaPy-Bug CVE/fix overlap, reconstructed function pairs,
inspected source/advisory relevance and retained 335 supported additions.
Admissions, rejections and unresolved cases are recorded separately. Assistant
judgments are distinct from HaPy-Bug's human line-purpose annotations.

## This combined package

The admitted source subsets were combined, grouped into provisional splits and
checked for the defined provenance, exact-code, AST and lexical-near-duplicate
leakage. `data/dataset.json` is a formatting-only array export of the combined
JSONL records; it does not add or relabel cases.

Full records retain source repository identities, paths, CVEs, commit and source
URLs, hashes, label provenance and supporting context. Original software terms
remain relevant: see [licensing](../LICENSE.md). Consult the original release
metadata for authoritative author/version details when preparing academic
references.
