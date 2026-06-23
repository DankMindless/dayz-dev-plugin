#!/usr/bin/env python3
"""Synchronize upstream knowledge directories into the Codex skill."""

from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
from pathlib import Path


REFERENCE_DIRS = ("scripting", "systems", "frameworks", "config", "compatibility")
REPO_ROOT = Path(__file__).resolve().parents[1]
DESTINATION = REPO_ROOT / "plugins/dayz-dev/skills/dayz-dev/references"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): digest(path)
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def differences() -> list[str]:
    issues: list[str] = []
    for directory in REFERENCE_DIRS:
        source = REPO_ROOT / directory
        destination = DESTINATION / directory
        source_files = inventory(source)
        destination_files = inventory(destination) if destination.exists() else {}
        for name in sorted(source_files.keys() | destination_files.keys()):
            if name not in destination_files:
                issues.append(f"missing from plugin: {directory}/{name}")
            elif name not in source_files:
                issues.append(f"stale in plugin: {directory}/{name}")
            elif source_files[name] != destination_files[name]:
                issues.append(f"content differs: {directory}/{name}")
    return issues


def synchronize() -> None:
    DESTINATION.mkdir(parents=True, exist_ok=True)
    for directory in REFERENCE_DIRS:
        source = REPO_ROOT / directory
        destination = DESTINATION / directory
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(source, destination)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail instead of copying when references differ.")
    args = parser.parse_args()
    if not args.check:
        synchronize()
    issues = differences()
    if issues:
        print("Reference synchronization failed:", file=sys.stderr)
        for issue in issues:
            print(f"- {issue}", file=sys.stderr)
        return 1
    print(f"Codex references synchronized across {len(REFERENCE_DIRS)} directories.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
