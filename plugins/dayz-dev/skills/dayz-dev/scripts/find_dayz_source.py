#!/usr/bin/env python3
"""Locate a DayZ script source root without modifying it."""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


REQUIRED_PATHS = (
    Path("scripts/1_core"),
    Path("scripts/3_game"),
    Path("scripts/4_world"),
)


@dataclass(frozen=True)
class Discovery:
    root: Path
    source: str


def is_dayz_source_root(path: Path) -> bool:
    """Return whether path contains the minimum vanilla script modules."""
    try:
        return path.is_dir() and all((path / required).is_dir() for required in REQUIRED_PATHS)
    except OSError:
        return False


def ancestors(start: Path) -> Iterable[Path]:
    """Yield start (or its parent for a file) followed by its ancestors."""
    current = start.expanduser()
    try:
        current = current.resolve(strict=False)
    except OSError:
        current = current.absolute()
    if current.is_file():
        current = current.parent
    yield current
    yield from current.parents


def discover_source_root(
    *,
    start: Path,
    env_value: str | None,
    standard_roots: Iterable[Path],
    explicit_root: Path | None = None,
) -> Discovery | None:
    """Resolve in public contract order: env, ancestry, standard roots, explicit."""
    candidates: list[tuple[str, Path]] = []
    if env_value:
        candidates.append(("DAYZ_SOURCE_ROOT", Path(env_value)))
    candidates.extend(("workspace-ancestor", candidate) for candidate in ancestors(start))
    candidates.extend(("standard-mapping", candidate) for candidate in standard_roots)
    if explicit_root is not None:
        candidates.append(("explicit", explicit_root))

    seen: set[str] = set()
    for source, candidate in candidates:
        expanded = candidate.expanduser()
        try:
            normalized = expanded.resolve(strict=False)
        except OSError:
            normalized = expanded.absolute()
        key = os.path.normcase(str(normalized))
        if key in seen:
            continue
        seen.add(key)
        if is_dayz_source_root(normalized):
            return Discovery(root=normalized, source=source)
    return None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Find a directory containing scripts/1_core, scripts/3_game, and scripts/4_world."
    )
    parser.add_argument("--start", type=Path, default=Path.cwd(), help="Workspace path used for ancestor discovery.")
    parser.add_argument("--root", type=Path, help="Explicit fallback root supplied by the user.")
    parser.add_argument("--json", action="store_true", help="Print the root and discovery source as JSON.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    discovery = discover_source_root(
        start=args.start,
        env_value=os.environ.get("DAYZ_SOURCE_ROOT"),
        standard_roots=(Path("P:/"),) if os.name == "nt" else (),
        explicit_root=args.root,
    )
    if discovery is None:
        print(
            "DayZ source root not found. Set DAYZ_SOURCE_ROOT or provide --root PATH; "
            "the root must contain scripts/1_core, scripts/3_game, and scripts/4_world.",
            file=sys.stderr,
        )
        return 2
    if args.json:
        print(json.dumps({"root": str(discovery.root), "source": discovery.source}))
    else:
        print(discovery.root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
