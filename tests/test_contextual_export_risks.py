"""Export/consumer risk fixture probes behind the contextual rubric.

Runnable probes establish the contrasting staged facts for the destructive
export, mitigated export, consumer-contract, and duplicated-parsing scenarios.
"""

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from review_fixture_support import ACCEPTANCE_FIXTURE, normalized


class ContextualExportRiskFixtureTests(unittest.TestCase):
    """Runnable probes establish the contrasting staged facts behind the rubric."""

    def stage(self, scenario: str) -> Path:
        temporary = TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        work = Path(temporary.name)
        env = dict(os.environ, EVAL_WORK_ROOT=str(work))
        subprocess.run(
            [sys.executable, str(ACCEPTANCE_FIXTURE), scenario],
            check=True,
            env=env,
            capture_output=True,
        )
        return work


    def run_export(self, root: Path, invoices: Path, out: Path, *extra: str):
        return subprocess.run(
            [sys.executable, "-m", "src.invoices.export", str(invoices), str(out), *extra],
            cwd=root,
            capture_output=True,
            text=True,
        )


    def test_failed_risky_export_destroys_the_existing_ledger(self):
        work = self.stage("contextual-risk-blockers-decision")
        root = work / "contextual-runner"
        out = root / "out" / "ledger.csv"
        out.parent.mkdir(parents=True)
        out.write_text("inv-9001,10.00\n")
        invoices = root / "bad-invoices.json"
        invoices.write_text(
            json.dumps([{"id": "inv-1", "amount": "5.25"}, {"id": "inv-2", "amount": "oops"}])
        )
        failed = self.run_export(root, invoices, out)
        self.assertNotEqual(failed.returncode, 0)
        self.assertEqual(out.read_text(), "")


    def test_failed_mitigated_export_preserves_the_existing_ledger(self):
        work = self.stage("contextual-risk-mitigated-decision")
        root = work / "contextual-runner"
        out = root / "out" / "ledger.csv"
        out.parent.mkdir(parents=True)
        out.write_text("inv-9001,10.00\n")
        invoices = root / "bad-invoices.json"
        invoices.write_text(
            json.dumps([{"id": "inv-1", "amount": "5.25"}, {"id": "inv-2", "amount": "oops"}])
        )
        failed = self.run_export(root, invoices, out)
        self.assertNotEqual(failed.returncode, 0)
        self.assertEqual(out.read_text(), "inv-9001,10.00\n")


    def test_risky_export_breaches_the_declared_consumer_contract(self):
        work = self.stage("contextual-risk-blockers-decision")
        root = work / "contextual-runner"
        out = root / "out" / "ledger.csv"
        out.parent.mkdir(parents=True)
        invoices = root / "invoices.json"
        invoices.write_text(json.dumps([{"id": "inv-1", "amount": "12.75"}]))
        subprocess.run(
            [sys.executable, "-m", "src.invoices.export", str(invoices), str(out)],
            cwd=root,
            check=True,
            capture_output=True,
        )
        consumer = subprocess.run(
            [sys.executable, str(root / "consumers" / "report_ledger.py"), str(out)],
            capture_output=True,
            text=True,
        )
        self.assertEqual(consumer.returncode, 2)
        self.assertIn("missing required header row", consumer.stdout)


    def test_mitigated_export_satisfies_the_declared_consumer_contract(self):
        work = self.stage("contextual-risk-mitigated-decision")
        root = work / "contextual-runner"
        out = root / "out" / "ledger.csv"
        out.parent.mkdir(parents=True)
        invoices = root / "invoices.json"
        invoices.write_text(json.dumps([{"id": "inv-1", "amount": "12.75"}]))
        subprocess.run(
            [sys.executable, "-m", "src.invoices.export", str(invoices), str(out)],
            cwd=root,
            check=True,
            capture_output=True,
        )
        consumer = subprocess.run(
            [sys.executable, str(root / "consumers" / "report_ledger.py"), str(out)],
            capture_output=True,
            text=True,
        )
        self.assertEqual(consumer.returncode, 0)
        self.assertIn("report-ledger: ok", consumer.stdout)


    def test_clean_flag_destroys_unrelated_ledgers_only_in_the_risky_variant(self):
        work = self.stage("contextual-risk-blockers-decision")
        root = work / "contextual-runner"
        out = root / "out" / "ledger.csv"
        yesterday = root / "out" / "yesterday.csv"
        yesterday.parent.mkdir(parents=True)
        yesterday.write_text("inv-9000,9.00\n")
        invoices = root / "invoices.json"
        invoices.write_text(json.dumps([{"id": "inv-1", "amount": "12.75"}]))
        subprocess.run(
            [
                sys.executable,
                "-m",
                "src.invoices.export",
                str(invoices),
                str(out),
                "--clean",
            ],
            cwd=root,
            check=True,
            capture_output=True,
        )
        self.assertFalse(yesterday.exists())

        mitigated = self.stage("contextual-risk-mitigated-decision")
        mitigated_source = (
            mitigated / "contextual-runner" / "src" / "invoices" / "export.py"
        ).read_text()
        self.assertNotIn("rmtree", mitigated_source)


    def test_duplicated_parsing_authority_diverges_only_in_the_risky_variant(self):
        work = self.stage("contextual-risk-blockers-decision")
        root = work / "contextual-runner"
        probe = subprocess.run(
            [
                sys.executable,
                "-c",
                "from src.invoices.amount import parse_amount; "
                "from src.invoices.export import _parse_amount; "
                "print(parse_amount('12.75'), _parse_amount('12.75'))",
            ],
            cwd=root,
            capture_output=True,
            text=True,
        )
        self.assertEqual(probe.returncode, 0)
        self.assertEqual(probe.stdout.strip(), "12.75 12")

        mitigated = self.stage("contextual-risk-mitigated-decision")
        mitigated_root = mitigated / "contextual-runner"
        duplicated = subprocess.run(
            [
                sys.executable,
                "-c",
                "from src.invoices.amount import parse_amount; "
                "from src.invoices.export import _parse_amount; print('dup')",
            ],
            cwd=mitigated_root,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(duplicated.returncode, 0)
        single = subprocess.run(
            [
                sys.executable,
                "-c",
                "from src.invoices.amount import parse_amount; print(parse_amount('12.75'))",
            ],
            cwd=mitigated_root,
            capture_output=True,
            text=True,
        )
        self.assertEqual(single.returncode, 0)
        self.assertEqual(single.stdout.strip(), "12.75")



if __name__ == "__main__":
    unittest.main()
