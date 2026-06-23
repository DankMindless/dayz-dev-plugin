#!/usr/bin/env python3
"""Create a deterministic Codex plugin ZIP and SHA-256 checksum."""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = REPO_ROOT / "plugins/dayz-dev"
MANIFEST_PATH = PLUGIN_ROOT / ".codex-plugin/plugin.json"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expected-tag", help="Require a v-prefixed tag to match plugin.json.")
    parser.add_argument("--output-dir", type=Path, default=REPO_ROOT / "dist")
    args = parser.parse_args()

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    version = manifest["version"]
    expected_tag = f"v{version}"
    if args.expected_tag and args.expected_tag != expected_tag:
        parser.error(f"tag {args.expected_tag!r} does not match plugin version {version!r}")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    archive = args.output_dir / f"dayz-dev-codex-{expected_tag}.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
        for path in sorted(PLUGIN_ROOT.rglob("*")):
            if not path.is_file() or "__pycache__" in path.parts:
                continue
            relative = Path("dayz-dev") / path.relative_to(PLUGIN_ROOT)
            info = zipfile.ZipInfo(relative.as_posix(), date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, path.read_bytes())

    checksum = hashlib.sha256(archive.read_bytes()).hexdigest()
    checksum_path = archive.with_suffix(archive.suffix + ".sha256")
    checksum_path.write_text(f"{checksum}  {archive.name}\n", encoding="ascii")
    print(archive)
    print(checksum_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
