#!/usr/bin/env python3
"""Validate the public Codex marketplace and content-only DayZ plugin."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE_PATH = REPO_ROOT / ".agents/plugins/marketplace.json"
PLUGIN_ROOT = REPO_ROOT / "plugins/dayz-dev"
MANIFEST_PATH = PLUGIN_ROOT / ".codex-plugin/plugin.json"
SKILL_PATH = PLUGIN_ROOT / "skills/dayz-dev/SKILL.md"
SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
FORBIDDEN_TEXT = {
    r"D:\DZProject": "private DayZ source path",
    "C:\\Users\\": "private Windows profile path",
    "allowed-tools:": "Claude-only skill frontmatter",
    "WebFetch(": "Claude-only WebFetch control token",
    ".claude-plugin": "Claude plugin metadata",
}
FORBIDDEN_SUFFIXES = {".c", ".cpp", ".cc", ".h", ".hpp", ".pem", ".key", ".pfx", ".p12"}


def load_json(path: Path, errors: list[str]) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid JSON at {path.relative_to(REPO_ROOT)}: {exc}")
        return {}


def validate_manifests(errors: list[str]) -> None:
    marketplace = load_json(MARKETPLACE_PATH, errors)
    if marketplace.get("name") != "dayzghost-dayz":
        errors.append("marketplace name must be dayzghost-dayz")
    plugins = marketplace.get("plugins", [])
    if len(plugins) != 1 or plugins[0].get("name") != "dayz-dev":
        errors.append("marketplace must expose exactly dayz-dev")
    source = plugins[0].get("source", {}) if plugins else {}
    if source.get("source") != "local" or source.get("path") != "./plugins/dayz-dev":
        errors.append("marketplace source must be ./plugins/dayz-dev")

    manifest = load_json(MANIFEST_PATH, errors)
    for field in ("name", "version", "description", "author", "license", "skills"):
        if not manifest.get(field):
            errors.append(f"plugin manifest missing {field}")
    if manifest.get("name") != "dayz-dev":
        errors.append("plugin manifest name must be dayz-dev")
    if not SEMVER.fullmatch(str(manifest.get("version", ""))):
        errors.append("plugin version must be semantic versioning")
    if manifest.get("license") != "GPL-3.0":
        errors.append("plugin license must be GPL-3.0")
    if manifest.get("repository") != "https://github.com/DayZGhost/dayz-dev-plugin":
        errors.append("plugin repository must point to the upstream project")
    for forbidden_key in ("mcpServers", "apps", "hooks"):
        if forbidden_key in manifest:
            errors.append(f"content-only plugin cannot define {forbidden_key}")


def validate_skill(errors: list[str]) -> None:
    text = SKILL_PATH.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        errors.append("SKILL.md must start with YAML frontmatter")
        return
    parts = text.split("---", 2)
    if len(parts) != 3:
        errors.append("SKILL.md frontmatter is not closed")
        return
    frontmatter = parts[1]
    if not re.search(r"(?m)^name:\s*dayz-dev\s*$", frontmatter):
        errors.append("SKILL.md frontmatter name must be dayz-dev")
    if not re.search(r"(?m)^description:\s*.+$", frontmatter):
        errors.append("SKILL.md frontmatter needs a description")
    if "TODO" in text:
        errors.append("SKILL.md contains TODO placeholder text")

    for markdown in PLUGIN_ROOT.rglob("*.md"):
        content = markdown.read_text(encoding="utf-8")
        for target in MARKDOWN_LINK.findall(content):
            clean = target.split("#", 1)[0].strip()
            if not clean or clean.startswith(("http://", "https://", "mailto:")):
                continue
            if not (markdown.parent / clean).resolve().exists():
                errors.append(
                    f"broken link in {markdown.relative_to(REPO_ROOT)}: {target}"
                )


def validate_content(errors: list[str]) -> None:
    for path in PLUGIN_ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            errors.append(f"forbidden bundled file: {path.relative_to(REPO_ROOT)}")
        if path.suffix.lower() not in {".md", ".txt", ".json", ".yaml", ".yml", ".py"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for token, description in FORBIDDEN_TEXT.items():
            if token in text:
                errors.append(f"{description} in {path.relative_to(REPO_ROOT)}")

    license_text = (PLUGIN_ROOT / "LICENSE.txt").read_text(encoding="utf-8")
    if "GNU GENERAL PUBLIC LICENSE" not in license_text or "Version 3" not in license_text:
        errors.append("plugin LICENSE.txt is not GPL-3.0")
    notice = (PLUGIN_ROOT / "NOTICE.txt").read_text(encoding="utf-8")
    if "https://github.com/DayZGhost/dayz-dev-plugin" not in notice:
        errors.append("plugin NOTICE.txt is missing upstream attribution")


def main() -> int:
    errors: list[str] = []
    validate_manifests(errors)
    validate_skill(errors)
    validate_content(errors)
    if errors:
        print("Codex plugin validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    reference_count = len(list((PLUGIN_ROOT / "skills/dayz-dev/references").rglob("*.md")))
    print(f"Codex plugin validation passed with {reference_count} bundled references.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
