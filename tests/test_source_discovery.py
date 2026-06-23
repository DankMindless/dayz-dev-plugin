from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
HELPER_PATH = REPO_ROOT / "plugins/dayz-dev/skills/dayz-dev/scripts/find_dayz_source.py"
SPEC = importlib.util.spec_from_file_location("find_dayz_source", HELPER_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def create_root(path: Path) -> Path:
    for required in MODULE.REQUIRED_PATHS:
        (path / required).mkdir(parents=True, exist_ok=True)
    return path


class SourceDiscoveryTests(unittest.TestCase):
    def test_environment_variable_has_priority(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            env_root = create_root(base / "env")
            workspace_root = create_root(base / "workspace")
            result = MODULE.discover_source_root(
                start=workspace_root / "mods/example",
                env_value=str(env_root),
                standard_roots=(),
            )
            self.assertEqual(result.root, env_root.resolve())
            self.assertEqual(result.source, "DAYZ_SOURCE_ROOT")

    def test_workspace_ancestor_is_discovered(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = create_root(Path(temp) / "dayz")
            nested = root / "mods/example/scripts/4_world"
            nested.mkdir(parents=True)
            result = MODULE.discover_source_root(
                start=nested,
                env_value=None,
                standard_roots=(),
            )
            self.assertEqual(result.root, root.resolve())
            self.assertEqual(result.source, "workspace-ancestor")

    def test_standard_mapping_is_discovered(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            mapped = create_root(base / "mapped")
            unrelated = base / "unrelated"
            unrelated.mkdir()
            result = MODULE.discover_source_root(
                start=unrelated,
                env_value=None,
                standard_roots=(mapped,),
            )
            self.assertEqual(result.root, mapped.resolve())
            self.assertEqual(result.source, "standard-mapping")

    def test_explicit_root_is_last_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            explicit = create_root(base / "explicit")
            unrelated = base / "unrelated"
            unrelated.mkdir()
            result = MODULE.discover_source_root(
                start=unrelated,
                env_value=str(base / "invalid"),
                standard_roots=(base / "also-invalid",),
                explicit_root=explicit,
            )
            self.assertEqual(result.root, explicit.resolve())
            self.assertEqual(result.source, "explicit")

    def test_missing_source_returns_none(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            result = MODULE.discover_source_root(
                start=Path(temp),
                env_value=None,
                standard_roots=(),
            )
            self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
