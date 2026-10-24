"""CLEAN architecture policy for declared runtime imports; no debt baseline.

These narrow source checks cover static imports and literal dynamic-load paths.
Computed imports, filesystem reads and semantic ownership still need review.
"""

import ast
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
ORCHESTRATOR = "skills/task-orchestrator/scripts"
# Existing dependency direction from the orchestrator architecture map.
SIBLINGS = {
    "controller": {"controller_state", "controller_git", "verification_runner", "codex_worker"},
    "controller_git": {"controller_state"},
    "verification_runner": {"controller_state"},
    "controller_state": set(),
    "codex_worker": set(),
}


def declared_imports(source: str) -> set[str]:
    tree = ast.parse(source)
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            names.add(node.module or "")
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.Call):
            function = node.func
            name = function.attr if isinstance(function, ast.Attribute) else getattr(function, "id", "")
            if name in {"spec_from_file_location", "import_module", "__import__"}:
                names.update(
                    value.value for value in ast.walk(node)
                    if isinstance(value, ast.Constant) and isinstance(value.value, str)
                )
    return names


def violations(path: str, source: str) -> list[str]:
    names = declared_imports(source)
    components = {
        part for name in names
        for part in name.removesuffix(".py").replace("/", ".").split(".")
    }
    errors = []
    if any(part == "tests" or part.startswith("test_") or part.endswith("_fixture_support")
           for part in components):
        errors.append("runtime imports test-only code; keep fixtures in the owning test suite")
    if Path(path).parts[0] in {"scripts", "tools"} and "skills" in components:
        errors.append("shared runtime imports a skill package; keep reusable dependencies in shared tooling")
    if str(Path(path).parent) == ORCHESTRATOR:
        owner = Path(path).stem
        forbidden = (components & SIBLINGS.keys()) - SIBLINGS.get(owner, set()) - {owner}
        if forbidden:
            errors.append(f"{owner} imports forbidden orchestrator siblings: {', '.join(sorted(forbidden))}")
    return errors


class ArchitectureTests(unittest.TestCase):
    def test_runtime_boundaries(self):
        files = set((ROOT / "scripts").glob("*.py"))
        files.update((ROOT / "tools").glob("*.py"))
        for skill in (ROOT / "skills").rglob("SKILL.md"):
            files.update((skill.parent / "scripts").rglob("*.py"))
        self.assertTrue(files, "runtime scope must not be empty")
        for path in sorted(files):
            relative = path.relative_to(ROOT).as_posix()
            with self.subTest(path=relative):
                self.assertEqual([], violations(relative, path.read_text()), relative)

    def test_forbidden_import_sentinels(self):
        cases = (
            ("scripts/example.py", "from tests import fixture", "test-only"),
            ("tools/example.py", "import skills.example", "skill package"),
            (f"{ORCHESTRATOR}/controller_state.py", "import controller", "forbidden orchestrator"),
            (f"{ORCHESTRATOR}/codex_worker.py",
             'importlib.util.spec_from_file_location("state", Path(__file__).with_name("controller_state.py"))',
             "forbidden orchestrator"),
        )
        for path, source, expected in cases:
            with self.subTest(source=source):
                self.assertTrue(any(expected in error for error in violations(path, source)))

    def test_permitted_imports_and_non_import_text(self):
        self.assertEqual([], violations(
            f"{ORCHESTRATOR}/controller_git.py",
            'importlib.util.spec_from_file_location("state", Path(__file__).with_name("controller_state.py"))',
        ))
        self.assertEqual([], violations("scripts/example.py", 'import json\nmessage = "tests.fixture"'))

    def test_cli_rejects_forbidden_import_and_passes_after_removal(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "tests").mkdir()
            (root / "scripts").mkdir()
            policy = root / "tests/test_architecture.py"
            policy.write_text(Path(__file__).read_text())
            source = root / "scripts/example.py"
            source.write_text("from tests import fixture\n")
            def run():
                return subprocess.run(
                    [sys.executable, str(policy), "ArchitectureTests.test_runtime_boundaries"],
                    text=True, capture_output=True, check=False,
                )
            rejected = run()
            self.assertNotEqual(0, rejected.returncode)
            self.assertIn("runtime imports test-only code", rejected.stderr)
            source.write_text("import json\n")
            passed = run()
            self.assertEqual(0, passed.returncode, passed.stderr)


if __name__ == "__main__":
    unittest.main()
