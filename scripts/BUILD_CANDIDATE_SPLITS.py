"""Build source-linked candidate pairs, not independently adjudicated gold labels.

Inputs: original CVEfixes Python SQLite extraction and pinned PyResBugs rows.
Never executes source programs. Groups repositories, CVEs, fixes and exact/AST
duplicates before assigning splits; audits near duplicates across assigned splits.
"""

import argparse
import ast
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import random
import re
import sqlite3
import textwrap
from urllib.parse import urlparse
import warnings


def save(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def repository(url):
    parsed = urlparse(url.strip().removesuffix(".git").rstrip("/"))
    result = parsed.netloc.lower() + "/" + parsed.path.strip("/").lower()
    aliases = {"github.com/python/cpython": "github.com/python/cpython",
               "github.com/rg3/youtube-dl": "github.com/ytdl-org/youtube-dl",
               "github.com/tiangolo/fastapi": "github.com/fastapi/fastapi",
               "github.com/pydata/pandas": "github.com/pandas-dev/pandas"}
    return aliases.get(result, result)


def normalise(code, decode=False):
    if not code or code in ("None", "nan"):
        raise ValueError("missing code")
    if decode:
        code = code.replace("\\n", "\n").replace("\\t", "\t")
    code = textwrap.dedent(code).strip() + "\n"
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", SyntaxWarning)
        tree = ast.parse(code)
    functions = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    if len(functions) != 1 or len(tree.body) != 1:
        raise ValueError("not one complete function")
    function = functions[0]
    if function.name.startswith("test") or function.name in ("setUp", "tearDown"):
        raise ValueError("test helper")
    if not 3 <= len(code.splitlines()) <= 250:
        raise ValueError("outside 3–250 line context budget")
    return code, sha(ast.dump(tree, include_attributes=False)), function.name


def production(path):
    return not re.search(r"(^|/)(tests?|docs?|examples?|benchmarks?)(/|$)|(^|/)(test_[^/]*|[^/]*_test|conftest)\.py$", path.lower())


def make_pair(source, identity, repo, commit, before, after, metadata, decode=False):
    before, ast_before, name_before = normalise(before, decode)
    after, ast_after, name_after = normalise(after, decode)
    if ast_before == ast_after:
        raise ValueError("no AST change")
    return {"pair_id": source + ":" + identity, "source": source,
            "repository": repository(repo), "fixing_commit": commit,
            "function_before": name_before, "function_after": name_after,
            "before": before, "after": after,
            "before_sha256": sha(before), "after_sha256": sha(after),
            "before_ast_sha256": ast_before, "after_ast_sha256": ast_after,
            "label_status": "source_linked_candidate_not_independently_adjudicated",
            **metadata}


def candidates(database, output):
    connection = sqlite3.connect(f"file:{database}?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    summary = {"cvefixes": {}, "pyresbugs": {}, "exclusions": Counter()}
    summary["cvefixes"]["python_file_changes"] = connection.execute(
        "SELECT count(*) FROM file_change WHERE programming_language='Python'").fetchone()[0]
    summary["cvefixes"]["python_method_versions"] = connection.execute("SELECT count(*) FROM method_change").fetchone()[0]
    summary["cvefixes"]["python_fixing_commits"] = connection.execute("SELECT count(DISTINCT hash) FROM file_change").fetchone()[0]
    summary["cvefixes"]["python_cves"] = connection.execute(
        "SELECT count(DISTINCT fixes.cve_id) FROM fixes JOIN file_change USING(hash)").fetchone()[0]
    fixes, descriptions, cwes, commits = defaultdict(list), {}, defaultdict(list), {}
    for r in connection.execute("SELECT * FROM fixes"):
        fixes[r["hash"]].append({"cve_id": r["cve_id"], "repo_url": r["repo_url"]})
    for r in connection.execute("SELECT cve_id,description FROM cve"):
        descriptions[r["cve_id"]] = r["description"]
    for r in connection.execute("SELECT * FROM cwe_classification"):
        cwes[r["cve_id"]].append(r["cwe_id"])
    for r in connection.execute("SELECT hash,repo_url,msg,parents FROM commits"):
        commits[r["hash"]] = dict(r)
    pairs = []
    for file in connection.execute("SELECT * FROM file_change WHERE programming_language='Python'"):
        path = file["old_path"] if file["old_path"] not in (None, "None", "nan") else file["new_path"]
        if not path or not production(path):
            summary["exclusions"]["CVEfixes nonproduction path"] += 1
            continue
        by_name = defaultdict(lambda: defaultdict(list))
        for method in connection.execute("SELECT * FROM method_change WHERE file_change_id=?", (file["file_change_id"],)):
            by_name[method["name"]][method["before_change"]].append(dict(method))
        for name, versions in by_name.items():
            if len(versions["True"]) != 1 or len(versions["False"]) != 1:
                summary["exclusions"]["CVEfixes ambiguous/unpaired method name"] += 1
                continue
            before, after = versions["True"][0], versions["False"][0]
            linked = fixes[file["hash"]]
            if not linked:
                summary["exclusions"]["CVEfixes no linked CVE"] += 1
                continue
            try:
                pair = make_pair("CVEfixes", str(file["file_change_id"]) + ":" + before["method_change_id"],
                                 linked[0]["repo_url"], file["hash"], before["code"], after["code"], {
                    "issue_group": "security_candidate", "cves": sorted({r["cve_id"] for r in linked}),
                    "cwes": sorted({c for r in linked for c in cwes[r["cve_id"]]}),
                    "descriptions": {r["cve_id"]: descriptions.get(r["cve_id"]) for r in linked},
                    "path": path, "file_change_id": file["file_change_id"],
                    "method_change_id_before": before["method_change_id"],
                    "method_change_id_after": after["method_change_id"],
                    "before_start_line": before["start_line"], "after_start_line": after["start_line"],
                    "commit": commits.get(file["hash"]), "dataset_licence": "CC-BY-4.0",
                    "source_code_licence": "retain upstream terms; not individually audited",
                    "reference_validity": "changed production method in CVE-linked fix; issue relevance unadjudicated",
                })
                pairs.append(pair)
            except (SyntaxError, ValueError, TypeError) as error:
                summary["exclusions"]["CVEfixes " + type(error).__name__ + ": " + str(error).split(" (<unknown>")[0][:100]] += 1
    original_security_hashes = set(fixes)
    bug_records = json.loads((output / "BUGSINPY_AUDIT_RECORDS.json").read_text())
    bugsinpy_hashes = {match.group(1).lower() for row in bug_records
                      if (match := re.search(r'''fixed_commit_id\s*=\s*['"]?([a-fA-F0-9]+)''', row["content"]))}
    pyres = json.loads((output / "PYRESBUGS_AUDIT_RECORDS.json").read_text())
    security_sources = {"CVEFixes", "PySecDB", "MoreFixes", "patch-tracer"}
    for index, r in enumerate(pyres):
        if r["Bug_Type"] == "security" or r["CVE-ID"] or r["Dataset_input"] in security_sources or r["Commit_sha"] in original_security_hashes:
            summary["exclusions"]["PyResBugs known security provenance"] += 1
            continue
        if r["Dataset_input"] == "BugsInPy" or any(r["Commit_sha"].lower().startswith(h) or h.startswith(r["Commit_sha"].lower()) for h in bugsinpy_hashes):
            summary["exclusions"]["PyResBugs BugsInPy-origin metadata excluded"] += 1
            continue
        try:
            pairs.append(make_pair("PyResBugs", str(index + 1), r["Url"], r["Commit_sha"],
                                   r["Faulty Code"], r["Fault Free Code"], {
                "issue_group": "correctness_candidate", "cves": [], "cwes": [],
                "source_dataset": r["Dataset_input"], "fault_acronym": r["Fault_Acronym"],
                "reported_bug_type": r["Bug_Type"], "bug_description": r["Bug_Description"],
                "fault_description": r["Implementation-Level Description"],
                "repository_url_original": r["Url"], "commit_url_original": r["Commit_URL"],
                "candidate_commit_url": r["Url"].rstrip("/") + "/commit/" + r["Commit_sha"],
                "dataset_licence": "MIT", "source_code_licence": "retain upstream terms; not individually audited",
                "encoding": "candidate newline/tab decoding; not canonical source reconstruction",
                "reference_validity": "paired source description; actual nonsecurity issue relevance unadjudicated",
            }, decode=True))
        except (SyntaxError, ValueError, TypeError) as error:
            summary["exclusions"]["PyResBugs " + type(error).__name__ + ": " + str(error).split(" (<unknown>")[0][:100]] += 1
    unique, duplicate_pairs = {}, 0
    for pair in pairs:
        key = (pair["before_ast_sha256"], pair["after_ast_sha256"])
        if key in unique:
            unique[key].setdefault("duplicate_pair_provenance", []).append({
                "pair_id": pair["pair_id"], "repository": pair["repository"],
                "fixing_commit": pair["fixing_commit"], "cves": pair["cves"],
            })
            duplicate_pairs += 1
        else:
            unique[key] = pair
    pairs = list(unique.values())
    summary["exact_ast_pair_duplicates_collapsed"] = duplicate_pairs
    summary["candidate_pairs"] = len(pairs)
    summary["candidate_groups"] = Counter(r["issue_group"] for r in pairs)
    summary["candidate_repositories"] = len({r["repository"] for r in pairs})
    with (output / "PYTHON_COMBINED_CANDIDATE_PAIRS.jsonl").open("w") as stream:
        for pair in pairs:
            stream.write(json.dumps(pair, ensure_ascii=False) + "\n")
    save(output / "PYTHON_COMBINED_CANDIDATE_COUNTS.json", summary)
    print(json.dumps({k: v for k, v in summary.items() if k != "exclusions"}, indent=2))


class Groups:
    def __init__(self, size):
        self.parents = list(range(size))

    def root(self, node):
        while self.parents[node] != node:
            self.parents[node] = self.parents[self.parents[node]]
            node = self.parents[node]
        return node

    def join(self, a, b):
        a, b = self.root(a), self.root(b)
        self.parents[b] = a


def split(output, prefix="PYTHON_COMBINED"):
    with (output / (prefix + "_CANDIDATE_PAIRS.jsonl")).open() as stream:
        pairs = [json.loads(line) for line in stream]
    groups = Groups(len(pairs))
    seen = {}
    for index, row in enumerate(pairs):
        keys = ["repo:" + row["repository"], "commit:" + row["fixing_commit"]]
        keys.extend("cve:" + c for c in row["cves"])
        for duplicate in row.get("duplicate_pair_provenance", []):
            keys.extend(["repo:" + duplicate["repository"], "commit:" + duplicate["fixing_commit"]])
            keys.extend("cve:" + c for c in duplicate["cves"])
        keys.extend(prefix + row[field] for prefix, field in (
            ("text:", "before_sha256"), ("text:", "after_sha256"),
            ("ast:", "before_ast_sha256"), ("ast:", "after_ast_sha256")))
        for key in keys:
            if key in seen:
                groups.join(index, seen[key])
            else:
                seen[key] = index
    components = defaultdict(list)
    for index in range(len(pairs)):
        components[groups.root(index)].append(index)
    # Repository grouping can make large components. Try deterministic seeded
    # allocations and retain the best category-proportion balance, not individual-row splitting.
    targets = {"train": .7, "validation": .15, "test": .15}
    totals = Counter(r["issue_group"] for r in pairs)
    best = None
    for seed in range(200):
        rng = random.Random(seed)
        order = list(components.values())
        rng.shuffle(order)
        order.sort(key=len, reverse=True)
        assigned, counts = {}, {s: Counter() for s in targets}
        for component in order:
            addition = Counter(pairs[i]["issue_group"] for i in component)
            def cost(candidate):
                return sum(((counts[s][g] + (addition[g] if s == candidate else 0)) / max(totals[g], 1) - targets[s]) ** 2
                           for s in targets for g in totals)
            selected = min(targets, key=lambda s: (cost(s), rng.random()))
            for i in component:
                assigned[i] = selected
            counts[selected].update(addition)
        score = sum((counts[s][g] / max(totals[g], 1) - targets[s]) ** 2 for s in targets for g in totals)
        if best is None or score < best[0]:
            best = (score, seed, assigned, counts)
    _, seed, assigned, counts = best
    # Deterministic near-duplicate audit: token set Jaccard >=0.9 on 5-token
    # shingles. Exhaustive inverted-index candidate generation, not probabilistic LSH.
    code_items = []
    for i, pair in enumerate(pairs):
        for side in ("before", "after"):
            tokens = re.findall(r"\w+|[^\w\s]", pair[side])
            shingles = frozenset(tuple(tokens[j:j + 5]) for j in range(max(1, len(tokens) - 4)))
            code_items.append((i, side, shingles))
    index = defaultdict(list)
    near = []
    for n, (pair_index, side, shingles) in enumerate(code_items):
        overlaps = Counter()
        for token in shingles:
            for other in index[token]:
                if assigned[code_items[other][0]] != assigned[pair_index]:
                    overlaps[other] += 1
        for other, common in overlaps.items():
            other_pair, other_side, other_shingles = code_items[other]
            similarity = common / len(shingles | other_shingles)
            if similarity >= .9:
                near.append({"left": other_pair, "right": pair_index, "left_side": other_side,
                             "right_side": side, "jaccard": similarity})
                groups.join(other_pair, pair_index)
        for token in shingles:
            index[token].append(n)
    # Merge any cross-split near-duplicate components into the larger component's
    # existing split; keep every linked repository together. Reaudit below.
    merged = defaultdict(list)
    for i in range(len(pairs)):
        merged[groups.root(i)].append(i)
    for component in merged.values():
        chosen = Counter(assigned[i] for i in component).most_common(1)[0][0]
        for i in component:
            assigned[i] = chosen
    assert all(assigned[r["left"]] == assigned[r["right"]] for r in near)
    audit_keys = defaultdict(set)
    for i, pair in enumerate(pairs):
        pair["split"] = assigned[i]
        for key in ("repo:" + pair["repository"], "commit:" + pair["fixing_commit"],
                    *("cve:" + c for c in pair["cves"]),
                    *("text:" + pair[f"{side}_sha256"] for side in ("before", "after")),
                    *("ast:" + pair[f"{side}_ast_sha256"] for side in ("before", "after"))):
            audit_keys[key].add(assigned[i])
    violations = [key for key, values in audit_keys.items() if len(values) > 1]
    assert not violations
    manifest = {"status": "candidate splits, not approved training/evaluation gold",
                "seed": seed, "target_ratios": targets, "pair_counts": {}, "repository_counts": {},
                "group_counts": {}, "cross_split_key_violations": violations,
                "near_duplicate_definition": "5-token shingle Jaccard >=0.9; lexical tokens including identifiers/literals",
                "cross_split_near_pairs_found_and_grouped": len(near),
                "cross_split_near_pairs_remaining": 0,
                "limitations": ["No semantic-clone or exhaustive fork-identity proof", "No independent issue-level adjudication",
                                "Enough examples for model adaptation is not established by counts alone"]}
    for name in targets:
        selected = [p for p in pairs if p["split"] == name]
        manifest["pair_counts"][name] = len(selected)
        manifest["repository_counts"][name] = len({p["repository"] for p in selected})
        manifest["group_counts"][name] = Counter(p["issue_group"] for p in selected)
        with (output / f"{prefix}_{name.upper()}_CANDIDATES.jsonl").open("w") as stream:
            for p in selected:
                stream.write(json.dumps(p, ensure_ascii=False) + "\n")
    save(output / (prefix + "_SPLIT_AUDIT.json"), manifest)
    save(output / (prefix + "_NEAR_DUPLICATE_LINKS.json"), near)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("candidates", "split"))
    parser.add_argument("--database", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--prefix", default="PYTHON_COMBINED")
    args = parser.parse_args()
    if not args.output_dir.is_dir():
        parser.error("Output directory must exist")
    if args.stage == "candidates":
        candidates(args.database, args.output_dir)
    else:
        split(args.output_dir, args.prefix)
