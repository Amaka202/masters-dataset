# Loading, verifying and reproducing

## 1. Load the prepared data

No source database or download is needed. Read `data/dataset.json` with an
ordinary JSON reader, or stream the combined JSONL file.

## 2. Verify the packaged checkpoint offline

```sh
python3 scripts/verify_package.py
```

Python 3.14 was used during preparation. Verification uses only the standard
library and the included files. It first checks `PACKAGE_MANIFEST.json`, then
checks JSON-array/JSONL equality, reconstructs the original flat file layout in
a temporary directory, and invokes the preserved offline verifier. It also
compares regenerated before-only/reference exports and the verification report
to the packaged checkpoint.

The source modules in the evidence ZIPs are decoded, sliced and parsed as data;
they are never imported or executed. The verifier confirms source identity and
the defined split checks, not independent issue-label validity.

## 3. Recreate a working preparation directory

The original scripts expect input filenames together in one directory. This
package keeps a friendlier folder layout and preserves a filename mapping in
`PACKAGE_MANIFEST.json`.

```sh
python3 scripts/stage_workspace.py --output-dir workspace
python3 scripts/INSPECT_SECURITY_CANDIDATES.py --help
python3 scripts/VERIFY_SECURITY_ADMISSION.py --output-dir workspace
```

Staging copies the mapped original files, preserving their bytes. It refuses
to overwrite differing files. `workspace/` is ignored by Git. Its README and
research notes preserve the original preparation workspace's historical
filenames and links; the main repository README describes the package layout.

### Continued source/advisory review

Inspection and parts of the admission/build pipeline require the original local
`CVEFIXES_PYTHON.sqlite` extraction, which is not stored in Git. Copy or link
that file into the staged workspace. Network stages also require `curl` and a
separate cache directory.

```sh
python3 scripts/INSPECT_SECURITY_CANDIDATES.py --output-dir workspace --indices 612 --context --advisory
python3 scripts/ADMIT_SECURITY_EXPANSION.py progress --output-dir workspace --cache-dir cache
```

The immutable remaining queue must not be regenerated. Review decisions are
explicit ledger entries; the scripts do not automatically adjudicate labels.
After supported ledger updates, the current stages are:

```sh
python3 scripts/ADMIT_SECURITY_EXPANSION.py upstream --output-dir workspace --cache-dir cache
python3 scripts/ADMIT_SECURITY_EXPANSION.py export --output-dir workspace --cache-dir cache
python3 scripts/BUILD_CANDIDATE_SPLITS.py split --prefix HAPY_CVEFIXES_ADMITTED --output-dir workspace
python3 scripts/VERIFY_SECURITY_ADMISSION.py --output-dir workspace
```

Some preserved tools also contain historical exploratory commands referring to
unselected datasets or superseded outputs. Those branches are not the selected
HaPy-Bug + CVEfixes preparation path.

### Original source extraction

`scripts/PYTHON_CORPUS_BUILD.py` preserves the CVEfixes download/extraction
tool. Official release URLs, digests, ZIP member metadata and Python extraction
validation records are in `attribution/` and `evidence/base/`. Starting from the
original release requires downloading its approximately 12.7 GB archive. The
HaPy-Bug release/reconstruction tools and published-reference processing
evidence are included as well. Reproducing those earlier stages may require
their original archives, temporary inputs and the dependencies documented by
the tools; it is separate from the self-contained offline checkpoint check.

## 4. Refresh this package from a verified preparation workspace

```sh
python3 scripts/package_dataset.py --source-dir /path/to/preparation-workspace
python3 scripts/verify_package.py
```

The packager verifies the source release manifest before copying its curated
files. It preserves original names under organised folders, creates the ordinary
JSON-array export and records file fingerprints and the source-to-package
mapping. It does not change source records, review decisions or source scripts.
When refreshing to a different snapshot, update the human-readable counts in
the README and guides before packaging and verification.
