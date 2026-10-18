"""Copy packaged original artifacts to the flat layout expected by preparation tools."""

import argparse
import hashlib
import json
from pathlib import Path
import shutil


def checked_path(root, relative):
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"Invalid package path: {relative}")
    target = (root / path).resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError(f"Path leaves package: {relative}")
    return target


def check_manifest(root):
    manifest = json.loads((root / "PACKAGE_MANIFEST.json").read_text())
    for relative, expected in manifest["files"].items():
        raw = checked_path(root, relative).read_bytes()
        actual = {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
        if actual != expected:
            raise ValueError(f"Package fingerprint mismatch: {relative}")
    return manifest


def stage(root, output):
    manifest = check_manifest(root)
    copies = []
    for name, relative in manifest["source_files"].items():
        if Path(name).name != name or relative not in manifest["files"]:
            raise ValueError(f"Invalid source-file mapping: {name}")
        source = checked_path(root, relative)
        target = output / name
        if target.exists() and target.read_bytes() != source.read_bytes():
            raise ValueError(f"Refusing to overwrite differing workspace file: {target}")
        copies.append((source, target))
    output.mkdir(parents=True, exist_ok=True)
    for source, target in copies:
        shutil.copyfile(source, target)
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    manifest = stage(Path(__file__).resolve().parents[1], args.output_dir.resolve())
    print(f"Staged {len(manifest['source_files'])} files in {args.output_dir}")
