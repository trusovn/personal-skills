"""Focused checks for the task-maintainability-review contract and fixture.

Contract checks reject the historical three-blocker cap and the
enough-blockers stop semantically and lock the preserved scope, materiality,
genuine-stop, gate, and eval expectations. Fixture checks stage the
skill-local setup in a disposable Git workspace and observe four
independently introduced blockers plus a non-blocking preference control at
the real filesystem, Git, and production boundaries.
"""

import ast
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from review_fixture_support import FLOW, ROOT

PACKAGE = FLOW / "task-maintainability-review"
SKILL = PACKAGE / "SKILL.md"
EVALS = PACKAGE / "evals" / "evals.json"
FIXTURE = PACKAGE / "evals" / "files" / "setup_fixture.py"


def normalized(path: Path) -> str:
    return re.sub(r"\s+", " ", path.read_text(encoding="utf-8")).strip()


def collapse(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


COUNT_AND_SUFFICIENCY_SHORTCUTS = (
    re.compile(
        r"(?:at most|no more than|maximum of)\s*[`*]*\d+[`*]*\s*blockers?",
        re.IGNORECASE,
    ),
    re.compile(r"do not (?:keep|continue) (?:searching|search)", re.IGNORECASE),
    re.compile(r"enough(?: decisive)? blockers", re.IGNORECASE),
)


class MaintainabilityReportingContractTest(unittest.TestCase):

    def test_every_confirmed_blocker_is_reported_without_a_count_cap(self):
        text = normalized(SKILL)
        for pattern in COUNT_AND_SUFFICIENCY_SHORTCUTS:
            self.assertIsNone(pattern.search(text), pattern.pattern)
        self.assertIn(
            "Report **every confirmed blocker** found within the bounded "
            "review scope, ordered by architectural impact",
            text,
        )
        self.assertIn(
            "Finding count or verdict sufficiency cannot end discovery, cap "
            "the output, or relegate a confirmed blocker to warnings",
            text,
        )
        self.assertIn(
            "Completeness does not authorize a wider survey or a quota of findings",
            text,
        )
        for field in (
            "file/location or concrete dependency edge",
            "the exact introduced/worsened problem",
            "evidence",
            "maintainability consequence",
            "smallest reasonable correction direction",
        ):
            self.assertIn(field, text)
        self.assertIn("one numbered entry per confirmed blocker", text)
        self.assertIn(
            "Every confirmed concrete blocker in the reviewed scope is "
            "reported; count is neither a limit nor a quota",
            text,
        )

    def test_genuine_stops_retain_outstanding_coverage(self):
        text = normalized(SKILL)
        self.assertIn(
            "A specific permission, capability, or safe-budget limit — never "
            "finding count or verdict sufficiency — is the only reason to stop "
            "before the bounded review scope is complete",
            text,
        )
        self.assertIn("retain every confirmed finding with its full evidence", text)
        self.assertIn(
            "name the outstanding coverage, the concrete stop reason, and the next owner",
            text,
        )
        self.assertIn(
            "cannot become `ACCEPT` or a claim of cleanly completed review",
            text,
        )

    def test_scope_materiality_and_safeguards_are_preserved(self):
        text = normalized(SKILL)
        for preserved in (
            "Do **not** begin with a repo-wide architecture survey",
            "introduced or materially worsened",
            "If not, keep it in `WARNINGS` or omit it",
            "new/worsened HARD violation",
            "unchanged baselined legacy violation",
            "WARNING / heuristic signal",
            "gate passes",
            "Do not edit architecture config, exceptions, or baselines to make review pass",
            "Reviewing the whole repository instead of the current change",
            "Blocking on pre-existing untouched debt",
            "Padding the blocker list with low-value nits",
            "reviews/maintainability-NN.md",
        ):
            self.assertIn(preserved, text)

    def test_existing_evals_retain_distinct_setup_facts_and_expectations(self):
        cases = {
            case["id"]: case
            for case in json.loads(EVALS.read_text(encoding="utf-8"))["evals"]
        }
        self.assertEqual([1, 2, 3], sorted(cases))
        self.assertIn("wrote the current production bytes", cases[1]["prompt"])
        first = " ".join(cases[1]["expectations"])
        self.assertIn("SELF_CHECK_ONLY", first)
        self.assertIn(
            "fresh independent `task-maintainability-review` session", first
        )
        self.assertIn("`archcheck` binary is absent", cases[2]["prompt"])
        second = " ".join(cases[2]["expectations"])
        self.assertIn("VERDICT: INCONCLUSIVE", second)
        self.assertIn("ARCHITECTURE_GATE: NOT_AVAILABLE", second)
        self.assertIn("/work/task-runs/PAY-14/maintainability.md", cases[3]["prompt"])
        third = " ".join(cases[3]["expectations"])
        self.assertIn("docs/tasks/PAY-14/reviews/maintainability-01.md", third)
        self.assertIn("does not overwrite prior reports", third)
        for case_id in (1, 2, 3):
            self.assertEqual([], cases[case_id]["files"])


class MaintainabilityFixtureTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.work = Path(tempfile.mkdtemp(prefix="maintainability-fixture-"))
        cls.addClassCleanup(shutil.rmtree, cls.work, ignore_errors=True)
        environment = os.environ | {"EVAL_WORK_ROOT": str(cls.work)}
        for scenario in ("four-blockers", "genuine-stop"):
            subprocess.run(
                [sys.executable, str(FIXTURE), scenario],
                check=True,
                cwd=ROOT,
                env=environment,
            )
        cls.repo = cls.work / "maintainability"
        cls.stop_repo = cls.work / "maintainability-stop"
        cls.run_dir = cls.work / "task-runs" / "MNT-42"

    @classmethod
    def git(cls, repo, *args):
        return subprocess.run(
            ["git", "-C", str(repo), *args],
            check=True,
            text=True,
            capture_output=True,
        ).stdout

    @classmethod
    def probe(cls, repo, code):
        directory = Path(tempfile.mkdtemp(dir=cls.work))
        completed = subprocess.run(
            [sys.executable, "-c", code],
            cwd=directory,
            capture_output=True,
            text=True,
            env=os.environ | {"PYTHONPATH": str(repo)},
        )
        return completed, directory

    def changed_source(self, relative):
        return (self.repo / relative).read_text(encoding="utf-8")

    def baseline_source(self, relative):
        return self.git(self.repo, "show", f"HEAD:{relative}")

    def test_stage_supplies_legitimate_task_baseline_and_changed_diff(self):
        brief = collapse(
            (self.repo / "docs/tasks/MNT-42/brief.md").read_text(encoding="utf-8")
        )
        self.assertIn("Status: ready", brief)
        self.assertIn("AC-01", brief)
        self.assertIn("AC-02", brief)
        self.assertIn("single source of truth", brief)
        rules = collapse((self.repo / "AGENTS.md").read_text(encoding="utf-8"))
        self.assertIn("required before a verdict", rules)
        status = self.git(self.repo, "status", "--short")
        for relative in (
            "src/billing/pricing.py",
            "src/billing/receipts.py",
            "src/billing/service.py",
            "tests/test_billing.py",
        ):
            self.assertIn(relative, status)
            self.assertTrue(self.baseline_source(relative).strip())
        diff = self.git(self.repo, "diff")
        for marker in ("LATE_RATES", "SqliteStore", "datetime", '("card", "wire")'):
            self.assertIn(marker, diff)

    def test_b1_duplicated_rate_policy_diverges_under_one_policy_edit(self):
        completed, _ = self.probe(
            self.repo,
            'from src.billing import pricing, service\n'
            'pricing.SURCHARGE_RATES["standard"] = 0.99\n'
            'print(pricing.surcharge(100, 10))\n'
            'print(service.checkout(100, 10, "card"))\n',
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        owner, copy_total = completed.stdout.splitlines()
        self.assertEqual("99.0", owner)
        self.assertIn("103.50", copy_total)
        changed = self.changed_source("src/billing/service.py")
        self.assertIn("LATE_RATES", changed)
        self.assertNotIn("pricing.surcharge", changed)
        self.assertNotIn("LATE_RATES", self.baseline_source("src/billing/service.py"))

    def test_b2_domain_policy_depends_on_concrete_sqlite_state(self):
        completed, directory = self.probe(
            self.repo,
            'from src.billing import pricing\n'
            'print(pricing.fee(100))\n',
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertEqual("2.0", completed.stdout.strip())
        self.assertTrue((directory / "billing.db").exists())
        seeded, _ = self.probe(
            self.repo,
            'import sqlite3\n'
            'from src.billing import pricing\n'
            'connection = sqlite3.connect("billing.db")\n'
            'connection.execute("create table rates (name text, value real)")\n'
            "connection.execute(\"insert into rates values ('late:standard', 0.99)\")\n"
            'connection.commit()\n'
            'print(pricing.surcharge(100, 10))\n',
        )
        self.assertEqual(0, seeded.returncode, seeded.stderr)
        self.assertEqual("99.0", seeded.stdout.strip())
        changed = self.changed_source("src/billing/pricing.py")
        self.assertIn('"standard": 0.015', changed)
        self.assertIn("from src.billing.store import SqliteStore", changed)
        self.assertIn("store.connection.execute", changed)
        self.assertNotIn("import", self.baseline_source("src/billing/pricing.py"))
        self.assertNotIn(
            "src/billing/store.py", self.git(self.repo, "status", "--short")
        )

    def test_b3_receipt_rendering_lost_its_deterministic_seam(self):
        completed, _ = self.probe(
            self.repo,
            'import inspect\n'
            'from src.billing import receipts\n'
            'first = receipts.render(50, "card")\n'
            'second = receipts.render(50, "card")\n'
            'print(first == second)\n'
            'print(list(inspect.signature(receipts.render).parameters))\n',
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        deterministic, parameters = completed.stdout.splitlines()
        self.assertEqual("False", deterministic)
        self.assertEqual("['total', 'kind']", parameters)
        changed = self.changed_source("src/billing/receipts.py")
        self.assertIn("datetime.datetime.now()", changed)
        self.assertNotIn("import datetime", self.baseline_source("src/billing/receipts.py"))

    def test_b4_kind_dispatch_is_duplicated_and_already_disagrees(self):
        completed, _ = self.probe(
            self.repo,
            'from src.billing import receipts, service\n'
            'print(receipts.render(50, "check"))\n'
            'try:\n'
            '    service.checkout(100, 0, "check")\n'
            'except ValueError:\n'
            '    print("raised")\n',
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        receipt, outcome = completed.stdout.splitlines()
        self.assertIn("card total 50.00", receipt)
        self.assertEqual("raised", outcome)
        self.assertIn('("card", "wire")', self.changed_source("src/billing/service.py"))
        self.assertIn('elif kind == "wire":', self.changed_source("src/billing/receipts.py"))
        self.assertNotIn("wire", self.baseline_source("src/billing/service.py"))
        self.assertNotIn("wire", self.baseline_source("src/billing/receipts.py"))

    def test_preference_control_is_explicitly_non_material(self):
        completed, _ = self.probe(
            self.repo,
            'from src.billing import service\n'
            'print(service.describe(10))\n',
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertEqual("subtotal 10.00", completed.stdout.strip())
        diff = self.git(self.repo, "diff")
        self.assertIn('-    return "subtotal " + format(subtotal, ".2f")', diff)
        self.assertIn('+    return f"subtotal {subtotal:.2f}"', diff)
        imports_of = lambda source: {
            node.module
            for node in ast.walk(ast.parse(source))
            if isinstance(node, ast.ImportFrom) and node.module
        }
        self.assertEqual(
            imports_of(self.baseline_source("src/billing/service.py")),
            imports_of(self.changed_source("src/billing/service.py")),
        )

    def test_changed_bytes_are_runnable_and_functionally_green(self):
        completed = subprocess.run(
            [sys.executable, "-m", "unittest", "tests.test_billing"],
            cwd=self.repo,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, completed.returncode, completed.stderr)

    def test_oracle_manifest_supplies_independent_defect_oracles(self):
        oracle = collapse(
            (self.run_dir / "maintainability-oracle.md").read_text(encoding="utf-8")
        )
        blockers = ("MNT-B1", "MNT-B2", "MNT-B3", "MNT-B4")
        for blocker in blockers:
            self.assertIn(f"### {blocker}", oracle)
        for blocker in blockers:
            section = oracle.split(f"### {blocker}", 1)[1].split("###", 1)[0]
            for heading in (
                "Location:",
                "Observation:",
                "Consequence:",
                "Smallest correction direction:",
            ):
                self.assertIn(heading, section)
        self.assertIn("Non-blocking preference control", oracle)
        self.assertIn("no confirmed material regression", oracle)
        self.assertIn("remain four", oracle)
        self.assertIn("genuine-stop", oracle)
        self.assertIn("outstanding coverage", oracle)

    def test_complete_scenario_gate_runs_green_from_policy_registry(self):
        registry = (self.repo / ".quality/gates.yaml").read_text(encoding="utf-8")
        self.assertIn("required: true", registry)
        command = next(
            line.split("command:", 1)[1].strip()
            for line in registry.splitlines()
            if line.strip().startswith("command:")
        )
        completed = subprocess.run(
            shlex.split(command),
            cwd=self.repo,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertIn("architecture gate: ok", completed.stdout)

    def test_genuine_stop_scenario_supplies_real_stop_inputs(self):
        registry = (self.stop_repo / ".quality/gates.yaml").read_text(
            encoding="utf-8"
        )
        self.assertIn("tools/archcheck verify src", registry)
        self.assertIn("required: true", registry)
        self.assertFalse((self.stop_repo / "tools" / "archcheck").exists())
        with self.assertRaises(FileNotFoundError):
            subprocess.run(
                ["tools/archcheck", "verify", "src"],
                cwd=self.stop_repo,
                capture_output=True,
            )
        fake_bin = Path(tempfile.mkdtemp(dir=self.work, prefix="fake-bin-"))
        fake_archcheck = fake_bin / "archcheck"
        fake_archcheck.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        fake_archcheck.chmod(0o755)
        with self.assertRaises(FileNotFoundError):
            subprocess.run(
                ["tools/archcheck", "verify", "src"],
                cwd=self.stop_repo,
                capture_output=True,
                env=os.environ
                | {"PATH": str(fake_bin) + os.pathsep + os.environ.get("PATH", "")},
            )
        rules = collapse((self.stop_repo / "AGENTS.md").read_text(encoding="utf-8"))
        self.assertIn(
            "Do not edit gate configuration, install tools, or substitute "
            "static inspection",
            rules,
        )
        diff = self.git(self.stop_repo, "diff")
        for marker in ("LATE_RATES", "SqliteStore", "datetime", '("card", "wire")'):
            self.assertIn(marker, diff)
        facts = collapse(
            (self.run_dir / "genuine-stop-facts.md").read_text(encoding="utf-8")
        )
        self.assertIn("tools/archcheck verify src", facts)
        self.assertIn("FileNotFoundError", facts)
        self.assertIn("independent of any host `PATH` content", facts)
        self.assertIn("outstanding coverage", facts)
        self.assertIn("next owner", facts)


if __name__ == "__main__":
    unittest.main()