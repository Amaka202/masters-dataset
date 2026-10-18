"""Read-only review views; downloaded source is parsed as data, never executed."""

import argparse
import ast
import difflib
from pathlib import Path
import sqlite3
import warnings

from ADMIT_SECURITY_EXPANSION import read_rows
from BUILD_HAPY_SOURCE_PAIRS import functions


def inspect(output, indices, context=False, helpers=(), advisory=False, bindings=False, pair_ids=()):
    queue = read_rows(output / "SECURITY_ADMISSION_REMAINING_QUEUE.jsonl")
    rows = {r["pair_id"]: r for r in read_rows(output / "CVEFIXES_SECURITY_EXPANSION_FILTERED_CANDIDATES.jsonl")}
    rows.update({r["pair_id"]: r for r in read_rows(output / "SECURITY_ADMISSION_SOURCE_CONTEXTS.jsonl")})
    evidence = {r["cve_id"]: r for r in read_rows(output / "SECURITY_ADMISSION_CVE_EVIDENCE.jsonl")}
    db = sqlite3.connect(f"file:{output / 'CVEFIXES_PYTHON.sqlite'}?mode=ro", uri=True)
    seen = set()
    selected = [(index, queue[index - 1]) for index in indices]
    selected.extend(("pair-id", {"pair_id": pid}) for pid in pair_ids)
    for index, item in selected:
        row = rows[item["pair_id"]]
        for cve in row["cves"]:
            if cve not in seen:
                seen.add(cve)
                descriptions = evidence[cve].get("cna", {}).get("descriptions", [])
                print(cve, " ".join(d["value"] for d in descriptions if d.get("lang", "").startswith("en")))
                if advisory:
                    print("REFERENCES", evidence[cve].get("cna", {}).get("references", []))
                    for advisory_item in evidence[cve].get("advisories", []):
                        print("ADVISORY", advisory_item["url"], advisory_item["record"].get("details", ""))
        print(index, row["pair_id"], row.get("qualified_function", row["function_before"]), row["path"])
        print("COMMIT", row["fixing_commit"], row["repository"], row["commit"]["msg"])
        if helpers:
            found = set()
            for path, before, after in db.execute("SELECT new_path,code_before,code_after FROM file_change WHERE hash=?", (row["fixing_commit"],)):
                for side, source in (("before", before), ("after", after)) if context else (("after", after),):
                    if not source or not any("def " + name + "(" in source for name in helpers):
                        continue
                    try:
                        tree = ast.parse(source)
                    except SyntaxError:
                        continue
                    print(side, "IMPORTS", "; ".join(ast.unparse(n) for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))))
                    if bindings:
                        for node in tree.body:
                            if isinstance(node, (ast.Assign, ast.AnnAssign)):
                                print(side, ast.unparse(node))
                            elif isinstance(node, ast.ClassDef):
                                print(side, "CLASS", path, node.name, "BASES", [ast.unparse(base) for base in node.bases])
                    for name, fn in functions(source).items():
                        if name.split(".")[-1] in helpers:
                            found.add(name.split(".")[-1])
                            print(side, "HELPER", path, name)
                            print(fn["code"])
            print("HELPERS NOT FOUND IN CHANGED PYTHON FILES", sorted(set(helpers) - found))
            continue
        if context or bindings:
            for side in ("before", "after"):
                source = db.execute(f"SELECT code_{side} FROM file_change WHERE file_change_id=?", (row["file_change_id"],)).fetchone()[0]
                try:
                    tree = ast.parse(source)
                    print(side, "IMPORTS:", "; ".join(ast.unparse(n) for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))))
                except SyntaxError:
                    print(side, "MODULE DOES NOT PARSE")
                    continue
                if bindings:
                    for node in tree.body:
                        if isinstance(node, (ast.Assign, ast.AnnAssign)):
                            print(ast.unparse(node))
                else:
                    print(side, row[side])
        else:
            versions = {}
            try:
                for side in ("before", "after"):
                    tree = ast.parse(row[side])
                    for node in ast.walk(tree):
                        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant) and isinstance(node.body[0].value.value, str):
                            node.body.pop(0)
                    versions[side] = ast.unparse(tree)
                print("\n".join(line for line in difflib.unified_diff(versions["before"].splitlines(), versions["after"].splitlines(), n=0) if not line.startswith(("---", "+++", "@@"))))
            except SyntaxError:
                print("SOURCE BLOCKED", item.get("source_check", "Selected function does not parse"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--indices", help="Comma-separated indices or inclusive ranges")
    selection.add_argument("--pair-ids", help="Comma-separated exact pair IDs, including original-ledger cases")
    parser.add_argument("--context", action="store_true")
    parser.add_argument("--helpers", default="", help="Comma-separated companion function names at the same commit")
    parser.add_argument("--advisory", action="store_true")
    parser.add_argument("--bindings", action="store_true")
    args = parser.parse_args()
    numbers = []
    for value in args.indices.split(",") if args.indices else ():
        ends = [int(v) for v in value.split("-")]
        numbers.extend(range(ends[0], ends[-1] + 1))
    if not all(1 <= i <= 1062 for i in numbers):
        parser.error("Queue indices must be between 1 and 1062")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", SyntaxWarning)
        inspect(args.output_dir, numbers, args.context, args.helpers.split(",") if args.helpers else (), args.advisory, args.bindings,
                args.pair_ids.split(",") if args.pair_ids else ())
