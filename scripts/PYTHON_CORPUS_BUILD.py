"""Extract and audit published corpora as inert data; never execute project code."""

import argparse
from collections import Counter
import gzip
import hashlib
import io
import json
from pathlib import Path
import re
import sqlite3
import subprocess
import sys
import time
import zipfile


ORIGINAL_URL = "https://zenodo.org/records/13118970/files/CVEfixes_v1.0.8.zip?download=1"
ORIGINAL_MD5 = "4586a358977acfa4c60b1a2cdd096221"
ORIGINAL_SIZE = 12708711268


def digest(path, algorithm="sha256"):
    result = hashlib.new(algorithm)
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            result.update(block)
    return result.hexdigest()


def save(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def download(cache, output):
    archive = cache / "CVEfixes_v1.0.8.zip"
    if not archive.exists():
        partial = cache / "CVEfixes_v1.0.8.zip.partial"
        subprocess.run([
            "curl", "-fLsS", "--retry", "3", "--retry-delay", "3", "--connect-timeout", "30",
            "--max-time", "1800", "--continue-at", "-", "--output", str(partial),
            "--write-out", "Downloaded %{size_download} bytes at %{speed_download} bytes/sec\n",
            ORIGINAL_URL,
        ], check=True)
        if digest(partial, "md5") != ORIGINAL_MD5:
            raise ValueError("Original Zenodo MD5 mismatch; partial file retained for investigation")
        partial.rename(archive)
    if digest(archive, "md5") != ORIGINAL_MD5:
        raise ValueError("Cached original archive MD5 mismatch")
    with zipfile.ZipFile(archive) as source:
        members = [{"path": m.filename, "compressed_bytes": m.compress_size,
                    "uncompressed_bytes": m.file_size} for m in source.infolist()]
    report = {"url": ORIGINAL_URL, "zenodo_record": "13118970", "version": "v1.0.8",
              "bytes": archive.stat().st_size, "md5": ORIGINAL_MD5,
              "sha256": digest(archive), "members": members}
    save(output / "CVEFIXES_ORIGINAL_ARCHIVE.json", report)
    print(json.dumps(report, indent=2))


def start_download(cache, output):
    log = cache / "original-download.log"
    with log.open("a") as stream:
        process = subprocess.Popen([
            sys.executable, str(Path(__file__).resolve()), "download",
            "--cache-dir", str(cache), "--output-dir", str(output),
        ], stdout=stream, stderr=stream, start_new_session=True)
    save(cache / "download-job.json", {"pid": process.pid, "log": str(log)})
    status(cache, output)


def status(cache, output):
    files = ("CVEfixes_v1.0.8.zip.partial", "CVEfixes_v1.0.8.zip")
    report = {name: (cache / name).stat().st_size for name in files if (cache / name).exists()}
    if (cache / "download-job.json").exists():
        report["job"] = json.loads((cache / "download-job.json").read_text())
    if (cache / "original-download.log").exists():
        report["recent_log"] = (cache / "original-download.log").read_text()[-3000:]
    if (cache / "original-extract.log").exists():
        report["extraction_log"] = (cache / "original-extract.log").read_text()[-3000:]
    if (output / "CVEFIXES_EXTRACTION_PROGRESS.json").exists():
        report["extraction"] = {k: v for k, v in json.loads(
            (output / "CVEFIXES_EXTRACTION_PROGRESS.json").read_text()).items() if k != "schemas"}
    print(json.dumps(report, indent=2))


def archive_index(cache, output):
    result = subprocess.run([
        "curl", "-fLsS", "--range", "-65536", "--max-filesize", "1048576",
        "--max-time", "90", ORIGINAL_URL,
    ], capture_output=True, check=True)
    (cache / "zip-tail.bin").write_bytes(result.stdout)
    with zipfile.ZipFile(io.BytesIO(result.stdout)) as archive:
        info = [{"path": m.filename, "compressed_bytes": m.compress_size,
                 "uncompressed_bytes": m.file_size} for m in archive.infolist()]
    save(output / "CVEFIXES_ORIGINAL_ZIP_INDEX.json", info)
    print(json.dumps(info, indent=2))


class GrowingArchive(io.RawIOBase):
    """Read completed local ranges and the ZIP footer while download continues."""

    def __init__(self, cache):
        self.cache = cache
        self.position = 0
        self.tail = (cache / "zip-tail.bin").read_bytes()

    def seekable(self):
        return True

    def readable(self):
        return True

    def tell(self):
        return self.position

    def seek(self, offset, whence=0):
        self.position = offset + (0 if whence == 0 else self.position if whence == 1 else ORIGINAL_SIZE)
        return self.position

    def read(self, size=-1):
        size = min(size if size >= 0 else ORIGINAL_SIZE, ORIGINAL_SIZE - self.position)
        if size <= 0:
            return b""
        if self.position >= ORIGINAL_SIZE - len(self.tail):
            start = self.position - (ORIGINAL_SIZE - len(self.tail))
            result = self.tail[start:start + size]
        else:
            deadline = time.monotonic() + 1800
            while True:
                path = self.cache / "CVEfixes_v1.0.8.zip"
                if not path.exists():
                    path = self.cache / "CVEfixes_v1.0.8.zip.partial"
                try:
                    available = path.stat().st_size - self.position
                except FileNotFoundError:
                    # The verified downloader atomically renamed partial to final.
                    continue
                if available >= size:
                    try:
                        with path.open("rb") as stream:
                            stream.seek(self.position)
                            result = stream.read(size)
                    except FileNotFoundError:
                        continue
                    break
                if time.monotonic() > deadline:
                    raise TimeoutError("Download did not supply the requested archive range")
                time.sleep(2)
        self.position += len(result)
        return result


def peek_sql(cache, output):
    with zipfile.ZipFile(GrowingArchive(cache)) as archive:
        with archive.open("CVEfixes_v1.0.8/Data/CVEfixes_v1.0.8.sql.gz") as compressed:
            with gzip.GzipFile(fileobj=compressed) as sql:
                prefix = sql.read(50000).decode()
    (cache / "sql-prefix.txt").write_text(prefix)
    print(prefix[:6000])


def peek_rows(cache, output):
    results = {}
    with zipfile.ZipFile(GrowingArchive(cache)) as archive:
        with archive.open("CVEfixes_v1.0.8/Data/CVEfixes_v1.0.8.sql.gz") as zipped:
            with gzip.GzipFile(fileobj=zipped) as compressed:
                with io.TextIOWrapper(compressed, encoding="utf-8") as lines:
                    parts = []
                    for line in lines:
                        parts.append(line)
                        if not line.rstrip().endswith(";"):
                            continue
                        statement = "".join(parts)
                        if not sqlite3.complete_statement(statement):
                            continue
                        parts = []
                        for table in ("file_change", "method_change"):
                            if table not in results and statement.startswith("INSERT INTO " + table):
                                results[table] = {"prefix": statement[:300], "suffix": statement[-500:]}
                        if len(results) == 2:
                            print(json.dumps(results, indent=2))
                            return


def extract(cache, output):
    """Stream the original SQL dump, retaining metadata and Python file/method rows."""
    database = cache / "cvefixes-python.sqlite.partial"
    if database.exists():
        raise FileExistsError("Partial extraction exists; inspect it before starting a new extraction")
    connection = sqlite3.connect(database)
    connection.execute("PRAGMA journal_mode=OFF")
    connection.execute("PRAGMA synchronous=OFF")
    connection.execute("PRAGMA trusted_schema=OFF")
    connection.execute("PRAGMA cache_size=-65536")
    allowed = {"fixes", "cve", "commits", "repository", "file_change", "method_change", "cwe_classification", "cwe"}
    retained, seen, schemas = Counter(), Counter(), {}
    python_ids = set()
    started = time.monotonic()
    def progress():
        connection.commit()
        save(output / "CVEFIXES_EXTRACTION_PROGRESS.json", {
            "elapsed_seconds": round(time.monotonic() - started),
            "rows_seen": seen, "rows_retained": retained, "schemas": schemas,
            "complete": False,
        })
    with zipfile.ZipFile(GrowingArchive(cache)) as archive:
        with archive.open("CVEfixes_v1.0.8/Data/CVEfixes_v1.0.8.sql.gz") as zipped:
            with gzip.GzipFile(fileobj=zipped) as compressed:
                with io.TextIOWrapper(compressed, encoding="utf-8") as lines:
                    parts = []
                    for line in lines:
                        parts.append(line)
                        if not line.rstrip().endswith(";"):
                            continue
                        statement = "".join(parts)
                        if not sqlite3.complete_statement(statement):
                            continue
                        parts = []
                        create = re.match(r'CREATE TABLE(?: IF NOT EXISTS)? "?(\w+)"?\s*\(', statement)
                        if create and create.group(1) in allowed:
                            table = create.group(1)
                            schemas[table] = statement
                            connection.execute(statement)
                            progress()
                            continue
                        insert = re.match(r'INSERT INTO "?(\w+)"? VALUES\(', statement)
                        if not insert or insert.group(1) not in allowed:
                            continue
                        table = insert.group(1)
                        seen[table] += 1
                        keep = True
                        if table == "file_change":
                            keep = statement.rstrip().endswith(",'Python');")
                        elif table == "method_change":
                            ids = re.match(r"INSERT INTO \"?method_change\"? VALUES\('(\d+)','(\d+)',", statement)
                            if not ids:
                                raise ValueError("Unexpected method identifiers: " + statement[:120])
                            keep = ids.group(2) in python_ids
                        if keep:
                            connection.execute(statement)
                            retained[table] += 1
                            if table == "file_change":
                                first = re.match(r"INSERT INTO \"?file_change\"? VALUES\('(\d+)',", statement)
                                if not first:
                                    raise ValueError("Unexpected file identifier")
                                python_ids.add(first.group(1))
                        if seen[table] % 1000 == 0:
                            progress()
    connection.execute("CREATE INDEX IF NOT EXISTS python_file_hash ON file_change(hash)")
    connection.execute("CREATE INDEX IF NOT EXISTS python_method_file ON method_change(file_change_id)")
    connection.commit()
    counts = {t: connection.execute(f'SELECT count(*) FROM "{t}"').fetchone()[0] for t in schemas}
    connection.close()
    database.rename(cache / "cvefixes-python.sqlite")
    save(output / "CVEFIXES_EXTRACTION_PROGRESS.json", {
        "elapsed_seconds": round(time.monotonic() - started), "rows_seen": seen,
        "rows_retained": retained, "database_counts": counts, "schemas": schemas,
        "complete": True, "archive_md5_verification": "Check CVEFIXES_ORIGINAL_ARCHIVE.json before final adoption",
    })
    print(json.dumps(counts, indent=2))


def start_extract(cache, output):
    log = cache / "original-extract.log"
    with log.open("a") as stream:
        process = subprocess.Popen([
            sys.executable, str(Path(__file__).resolve()), "extract",
            "--cache-dir", str(cache), "--output-dir", str(output),
        ], stdout=stream, stderr=stream, start_new_session=True)
    save(cache / "extract-job.json", {"pid": process.pid, "log": str(log)})
    print(json.dumps({"extraction_pid": process.pid, "log": str(log)}))


def restart_extract(cache, output):
    partial = cache / "cvefixes-python.sqlite.partial"
    previous = cache / ("cvefixes-python.sqlite.failed-" + time.strftime("%Y%m%d%H%M%S"))
    if previous.exists():
        raise FileExistsError("Previous diagnostic database already exists")
    partial.rename(previous)
    start_extract(cache, output)


def preserve(cache, output):
    manifest = json.loads((output / "CVEFIXES_ORIGINAL_ARCHIVE.json").read_text())
    if manifest["md5"] != "4586a358977acfa4c60b1a2cdd096221":
        raise ValueError("Original release checksum is not verified")
    progress = json.loads((output / "CVEFIXES_EXTRACTION_PROGRESS.json").read_text())
    if not progress["complete"]:
        raise ValueError("Original extraction is incomplete")
    source = sqlite3.connect(f"file:{cache / 'cvefixes-python.sqlite'}?mode=ro", uri=True)
    integrity = source.execute("PRAGMA integrity_check").fetchall()
    if integrity != [("ok",)]:
        raise ValueError(integrity)
    queries = {
        "python_file_changes": "SELECT count(*) FROM file_change",
        "non_python_file_changes": "SELECT count(*) FROM file_change WHERE programming_language != 'Python'",
        "python_method_versions": "SELECT count(*) FROM method_change",
        "orphan_methods": "SELECT count(*) FROM method_change m LEFT JOIN file_change f USING(file_change_id) WHERE f.file_change_id IS NULL",
        "python_fixing_commits": "SELECT count(DISTINCT hash) FROM file_change",
        "python_cves": "SELECT count(DISTINCT cve_id) FROM fixes JOIN file_change USING(hash)",
        "python_repositories": "SELECT count(DISTINCT repo_url) FROM fixes JOIN file_change USING(hash)",
    }
    checks = {key: source.execute(query).fetchone()[0] for key, query in queries.items()}
    if checks["non_python_file_changes"] or checks["orphan_methods"]:
        raise ValueError(checks)
    target = output / "CVEFIXES_PYTHON.sqlite"
    if target.exists():
        raise FileExistsError("Preserved database exists; inspect it before replacing")
    destination = sqlite3.connect(target)
    source.backup(destination)
    destination.close()
    source.close()
    with zipfile.ZipFile(cache / "CVEfixes_v1.0.8.zip") as archive:
        for member, filename in (
            ("LICENSE.txt", "CVEFIXES_UPSTREAM_LICENSE.txt"),
            ("README.md", "CVEFIXES_UPSTREAM_README.md"),
            ("Doc/DataDictionary.md", "CVEFIXES_UPSTREAM_DATA_DICTIONARY.md"),
        ):
            (output / filename).write_bytes(archive.read("CVEfixes_v1.0.8/" + member))
    save(output / "CVEFIXES_PYTHON_VALIDATION.json", {
        "archive_verified_md5": manifest["md5"], "archive_sha256": manifest["sha256"],
        "sqlite_integrity_check": "ok", "checks": checks,
        "preserved_database": str(target), "label_status": "Original provenance retained; issue-level method labels not independently validated",
    })
    print(json.dumps(checks, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("download", "start-download", "status", "archive-index", "peek-sql", "peek-rows", "extract", "start-extract", "restart-extract", "preserve"))
    parser.add_argument("--cache-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    if not args.cache_dir.is_dir() or not args.output_dir.is_dir():
        parser.error("cache and output directories must already exist")
    {"download": download, "start-download": start_download,
     "status": status, "archive-index": archive_index,
     "peek-sql": peek_sql, "extract": extract,
     "peek-rows": peek_rows, "start-extract": start_extract,
     "restart-extract": restart_extract, "preserve": preserve}[args.stage](args.cache_dir, args.output_dir)
