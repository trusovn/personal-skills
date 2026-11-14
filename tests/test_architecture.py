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
WORKFLOWS = {
    'run_records': {'ledger', 'record_validation', 'run_storage'},
    'run_authority': {'controller_git', 'flow_policy', 'ledger', 'record_serialization', 'run_policy', 'run_records', 'run_storage', 'task_manifest'},
    'candidate_checks': {'check_evidence', 'controller_git', 'flow_policy', 'record_serialization', 'run_authority', 'run_records', 'run_storage', 'verification_runner'},
    'review_collection': {'candidate_checks', 'check_evidence', 'flow_policy', 'review_contracts', 'run_authority', 'run_records', 'run_storage', 'verification_runner'},
    'acceptance_workflow': {'acceptance', 'candidate_checks', 'review_collection', 'review_contracts', 'run_authority', 'run_records', 'run_storage'},
    'operation_scheduling': {'acceptance_workflow', 'candidate_checks', 'flow_policy', 'ledger', 'review_collection', 'run_authority', 'run_records', 'run_storage'},
    'actor_lifecycle': {'acceptance_workflow', 'codex_worker', 'review_collection', 'run_authority', 'run_records', 'run_storage'},
    'input_revision': {'flow_policy', 'ledger', 'record_serialization', 'run_authority', 'run_records', 'run_storage', 'task_manifest'},
    'legacy_attempts': {'codex_worker', 'controller_git', 'execution_contracts', 'flow_policy', 'ledger', 'record_serialization', 'run_authority', 'run_policy', 'run_records', 'run_storage', 'task_manifest'},
    'legacy_inspection': {'codex_worker', 'controller_git', 'execution_contracts', 'flow_policy', 'ledger', 'record_serialization', 'run_authority', 'run_records', 'run_storage', 'task_manifest', 'verification_runner'},
}
DOMAIN_RULES = {
    'execution_contracts': {'flow_policy', 'record_serialization', 'record_validation', 'run_policy'},
    'flow_policy': {'record_validation'},
    'ledger': {'flow_policy', 'record_serialization', 'record_validation', 'run_policy', 'task_manifest'},
    'record_serialization': set(),
    'record_validation': set(),
    'review_contracts': {'record_validation'},
    'run_policy': {'flow_policy', 'record_validation'},
    'task_manifest': {'record_validation'},
}
SIBLINGS = {
    **WORKFLOWS,
    **DOMAIN_RULES,
    'controller': {'acceptance_workflow', 'actor_lifecycle', 'candidate_checks', 'check_evidence', 'codex_worker', 'controller_git', 'controller_state', 'input_revision', 'legacy_attempts', 'legacy_inspection', 'operation_scheduling', 'review_collection', 'run_authority', 'run_records', 'run_storage', 'verification_runner'},
    'controller_git': {'record_serialization'},
    'verification_runner': {'execution_contracts', 'record_serialization'},
    'controller_state': {'execution_contracts', 'flow_policy', 'ledger', 'record_serialization', 'record_validation', 'review_contracts', 'run_policy', 'task_manifest'},
    'acceptance': set(),
    'run_storage': set(),
    'check_evidence': {'execution_contracts'},
    'codex_worker': set(),
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
            if name in {"spec_from_file_location", "import_module", "__import__", "_load_component", "load_component"}:
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
            (f"{ORCHESTRATOR}/check_evidence.py", "import controller", "forbidden orchestrator"),
            (f"{ORCHESTRATOR}/check_evidence.py", "import verification_runner", "forbidden orchestrator"),
            (f"{ORCHESTRATOR}/check_evidence.py", "import codex_worker", "forbidden orchestrator"),
            (f"{ORCHESTRATOR}/controller_state.py", "import check_evidence", "forbidden orchestrator"),
            (f"{ORCHESTRATOR}/run_storage.py", "import controller", "forbidden orchestrator"),
            (f"{ORCHESTRATOR}/run_storage.py", "import codex_worker", "forbidden orchestrator"),
            (f"{ORCHESTRATOR}/codex_worker.py", "import run_storage", "forbidden orchestrator"),
            (f"{ORCHESTRATOR}/acceptance.py", "import controller", "forbidden orchestrator"),
            (f"{ORCHESTRATOR}/controller_state.py", "import acceptance", "forbidden orchestrator"),
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
        for owner in {*WORKFLOWS, *DOMAIN_RULES}:
            with self.subTest(owner=owner):
                self.assertTrue(violations(f"{ORCHESTRATOR}/{owner}.py", "from . import controller"))
        for owner, dependency in (
            ("run_records", "run_authority"),
            ("candidate_checks", "actor_lifecycle"),
            ("acceptance_workflow", "operation_scheduling"),
            ("controller_state", "candidate_checks"),
            ("flow_policy", "run_policy"),
            ("review_contracts", "execution_contracts"),
            ("review_contracts", "task_manifest"),
            ("execution_contracts", "ledger"),
            ("ledger", "controller_state"),
            ("record_serialization", "flow_policy"),
            ("controller_git", "controller_state"),
        ):
            with self.subTest(owner=owner, dependency=dependency):
                self.assertTrue(violations(f"{ORCHESTRATOR}/{owner}.py", f"from . import {dependency}"))

    def test_declared_orchestrator_directions_are_acyclic(self):
        def visit(owner, ancestors):
            self.assertNotIn(owner, ancestors, f"dependency cycle: {ancestors + [owner]}")
            for dependency in SIBLINGS[owner]:
                visit(dependency, ancestors + [owner])
        for owner in SIBLINGS:
            visit(owner, [])

    def test_permitted_imports_and_non_import_text(self):
        self.assertEqual([], violations(
            f"{ORCHESTRATOR}/controller_git.py",
            'importlib.util.spec_from_file_location("state", Path(__file__).with_name("record_serialization.py"))',
        ))
        self.assertEqual([], violations("scripts/example.py", 'import json\nmessage = "tests.fixture"'))
        self.assertEqual({"candidate_checks"}, declared_imports('_load_component("candidate_checks")'))

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
