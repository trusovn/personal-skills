"""Known-issue and repeated-review fact fixture probes behind the rubric.

Runnable probes establish the contrasting staged facts for known-issue record
fields, consumer compatibility, correction regression, and repeated-review
blocker reasons.
"""

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from review_fixture_support import ACCEPTANCE_FIXTURE, normalized


class ContextualKnownIssueFixtureTests(unittest.TestCase):
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


    def test_known_issue_record_fields_and_consumer_compatibility_probes(self):
        work = self.stage("known-issue-consumption-decision")
        root = work / "ledger-consumer"
        record = normalized(root / "docs" / "known-issues.md")
        for field in (
            "Stable issue ID: KI-001",
            "Provenance: task INV-07; review acceptance-01; finding INV-M01",
            "Trigger:",
            "Consequence:",
            "Evidence:",
            "Impact:",
            "Likelihood/exposure:",
            "Affected boundary:",
            "Affected consumers:",
            "Deferral rationale:",
            "Follow-up owner/action:",
            "Reassessment conditions:",
        ):
            self.assertIn(field, record)
        self.assertIn("proposed, not committed", record)
        self.assertIn("safeguards", record)

        summary = subprocess.run(
            [
                sys.executable,
                "-c",
                "from src.reporting.summary import summarize; "
                "from pathlib import Path; "
                "print(summarize(Path('cases/ledger-local.csv').read_text()))",
            ],
            cwd=root,
            capture_output=True,
            text=True,
        )
        self.assertEqual(summary.returncode, 0)
        self.assertEqual(summary.stdout.strip(), "1")

        workaround = subprocess.run(
            [
                sys.executable,
                "-c",
                "from src.reporting.utc_footer import utc_generated_at; "
                "from pathlib import Path; "
                "print(utc_generated_at(Path('cases/ledger-local.csv').read_text()))",
            ],
            cwd=root,
            capture_output=True,
            text=True,
        )
        self.assertEqual(workaround.returncode, 0)
        self.assertEqual(workaround.stdout.strip(), "2026-10-09T09:30:00+00:00")
        contract = normalized(root / "cases" / "consumer-contract.md")
        self.assertIn("true UTC instant is 2026-10-09T07:30:00+00:00", contract)
        self.assertNotEqual(workaround.stdout.strip(), "2026-10-09T07:30:00+00:00")

        discovery = normalized(work / "task-runs" / "RPT-12B" / "discovery-01.md")
        self.assertIn("changed exposure", discovery)
        self.assertIn("WEB-02", discovery)
        self.assertIn("RPT-12A", discovery)


    def test_correction_regression_probe_and_preserved_deferral(self):
        work = self.stage("correction-regression-decision")
        root = work / "correction-runner"
        state = root / "state.json"
        state.write_text(json.dumps({"pending": [{"id": "ORD-1"}], "output": []}))
        subprocess.run(
            [sys.executable, "-m", "src.orders.retry", str(state)],
            cwd=root,
            check=True,
            capture_output=True,
        )
        first = json.loads(state.read_text())["output"]
        subprocess.run(
            [sys.executable, "-m", "src.orders.retry", str(state)],
            cwd=root,
            check=True,
            capture_output=True,
        )
        second = json.loads(state.read_text())["output"]
        self.assertEqual(first, ["ORD-1,processed"])
        self.assertEqual(second, ["ORD-1,processed", "ORD-1,processed"])

        self.assertIn("KI-001", normalized(root / "docs" / "known-issues.md"))
        preflight = normalized(root / "docs" / "tasks" / "ORD-04" / "preflight.md")
        self.assertIn("exposure is unchanged", preflight)
        self.assertIn("no global correction-round limit", preflight)
        prior = normalized(root / "docs" / "tasks" / "ORD-04" / "reviews" / "acceptance-01.md")
        self.assertIn("`ACCEPT`", prior)
        discovery = normalized(work / "task-runs" / "ORD-04" / "discovery-01.md")
        self.assertIn("ORD-RERUN", discovery)
        self.assertIn("duplicated every row", discovery)
        self.assertIn("regression was introduced by this correction", discovery)


    def test_prior_retry_is_reproducible_and_retained_log_defect_is_real(self):
        work = self.stage("correction-regression-decision")
        root = work / "correction-runner"
        prior_source = subprocess.run(
            ["git", "show", "HEAD~1:src/orders/retry.py"], cwd=root,
            check=True, capture_output=True, text=True,
        ).stdout
        current_source = (root / "src/orders/retry.py").read_text()
        self.assertNotEqual(prior_source, current_source)
        prior = root / "prior_retry.py"
        prior.write_text(prior_source)
        for script, expected_rows in ((prior, 1), (root / "src/orders/retry.py", 2)):
            with self.subTest(script=script.name):
                state = root / "history-state.json"
                state.write_text(json.dumps({"pending": [{"id": "ORD-1"}], "output": []}))
                for _ in range(2):
                    probe = subprocess.run(
                        [sys.executable, str(script), str(state)], cwd=root,
                        check=True, capture_output=True, text=True,
                    )
                    self.assertEqual(probe.stdout.strip(), "processed 1 orders")
                self.assertEqual(len(json.loads(state.read_text())["output"]), expected_rows)


    def test_optional_links_future_work_and_priority_only_contrasts(self):
        for scenario, status in (
            ("known-issue-proposed-work-decision", "proposed"),
            ("known-issue-committed-work-decision", "committed"),
            ("known-issue-priority-only-decision", "committed"),
            ("known-issue-no-links-decision", "proposed"),
        ):
            with self.subTest(scenario=scenario):
                work = self.stage(scenario)
                root = work / "ledger-consumer"
                plan = json.loads((root / "cases/follow-up.json").read_text())
                self.assertEqual(plan["status"], status)
                self.assertFalse(plan["deployed"])
                record = (root / "docs/known-issues.md").read_text()
                if scenario == "known-issue-no-links-decision":
                    self.assertNotIn("Optional context links:", record)
                    self.assertIn("Reassessment conditions:", record)
                if scenario == "known-issue-priority-only-decision":
                    self.assertEqual(plan["prior_priority"], "next")
                    self.assertEqual(plan["current_priority"], "later")
                probe = subprocess.run(
                    [sys.executable, "-c", "from src.reporting.summary import summarize; "
                     "from pathlib import Path; print(summarize(Path('cases/ledger-local.csv').read_text()))"],
                    cwd=root, capture_output=True, text=True,
                )
                self.assertEqual(probe.returncode, 0, probe.stderr)
                self.assertEqual(probe.stdout.strip(), "1")
                self.assertIn("# generated_at=2026-10-09T09:30:00\n", (root / "cases/ledger-local.csv").read_text())


    def test_new_risk_history_keeps_consumer_and_changes_only_available_proof(self):
        work = self.stage("repeated-review-newly-demonstrated-material-risk-decision")
        root = work / "correction-runner"
        consumer = root / "consumers/settle.py"
        prior_consumer = subprocess.run(
            ["git", "show", "HEAD~1:consumers/settle.py"], cwd=root,
            capture_output=True, text=True,
        )
        self.assertEqual(prior_consumer.returncode, 0, prior_consumer.stderr)
        self.assertEqual(prior_consumer.stdout, consumer.read_text())
        changed = subprocess.run(
            ["git", "diff", "--name-only", "HEAD~1", "HEAD"], cwd=root,
            check=True, capture_output=True, text=True,
        )
        self.assertEqual(changed.stdout.splitlines(), ["tests/helpers/replay.py"])
        prior_script = root / "prior-settle.py"
        prior_script.write_text(prior_consumer.stdout)
        state = root / "settlement-state.json"
        state.write_text(json.dumps({"pending": [{"id": "ORD-1"}], "output": []}))
        for expected_charge in ("10", "20"):
            subprocess.run(
                [sys.executable, "-m", "src.orders.retry", str(state)], cwd=root,
                check=True, capture_output=True,
            )
            for script in (prior_script, consumer):
                with self.subTest(charge=expected_charge, script=script.name):
                    settlement = subprocess.run(
                        [sys.executable, str(script), str(state)], cwd=root,
                        check=True, capture_output=True, text=True,
                    )
                    self.assertEqual(settlement.stdout.strip(), expected_charge)


    def test_non_regression_blocker_reasons_have_current_proof_and_prior_context(self):
        for reason in (
            "formerly-blocked-evidence", "missed-existing-obligation",
            "changed-context-authority", "newly-demonstrated-material-risk",
        ):
            with self.subTest(reason=reason):
                work = self.stage("repeated-review-" + reason + "-decision")
                root = work / "correction-runner"
                source = (root / "src/orders/retry.py").read_text()
                committed = subprocess.run(
                    ["git", "show", "HEAD:src/orders/retry.py"], cwd=root,
                    check=True, capture_output=True, text=True,
                ).stdout
                self.assertEqual(source, committed)
                state = root / "repeat-state.json"
                state.write_text(json.dumps({"pending": [{"id": "ORD-1"}], "output": []}))
                subprocess.run(
                    [sys.executable, "tests/helpers/replay.py", str(state)], cwd=root,
                    check=True, capture_output=True,
                )
                self.assertEqual(json.loads(state.read_text())["output"], ["ORD-1,processed"] * 2)
                context = json.loads((root / "cases/review-history.json").read_text())
                self.assertEqual(context["reason"], reason)
                self.assertFalse(context["implementation_changed"])
                self.assertIn(context["prior_ac"], (root / "cases/prior-authority.md").read_text())
                self.assertIn(context["current_ac"], (root / "docs/tasks/ORD-04/brief.md").read_text())
                prior_source = subprocess.run(
                    ["git", "show", "HEAD~1:src/orders/retry.py"], cwd=root,
                    check=True, capture_output=True, text=True,
                ).stdout
                self.assertEqual(prior_source, source)
                if reason == "formerly-blocked-evidence":
                    self.assertEqual(context["prior_row"], "blocked")
                    self.assertTrue((root / "tests/helpers/replay.py").exists())
                    prior_helper = subprocess.run(
                        ["git", "cat-file", "-e", "HEAD~1:tests/helpers/replay.py"],
                        cwd=root, capture_output=True,
                    )
                    self.assertNotEqual(prior_helper.returncode, 0)
                    self.assertIn("INCONCLUSIVE", (root / "docs/tasks/ORD-04/reviews/acceptance-01.md").read_text())
                elif reason == "missed-existing-obligation":
                    self.assertEqual(context["prior_row"], "unchecked")
                    self.assertEqual(context["prior_ac"], context["current_ac"])
                elif reason == "changed-context-authority":
                    self.assertNotEqual(context["prior_ac"], context["current_ac"])
                else:
                    self.assertEqual(context["prior_ac"], context["current_ac"])
                    self.assertTrue((root / "consumers/settle.py").exists())
                    settlement = subprocess.run(
                        [sys.executable, "consumers/settle.py", str(state)], cwd=root,
                        check=True, capture_output=True, text=True,
                    )
                    self.assertEqual(settlement.stdout.strip(), "20")



if __name__ == "__main__":
    unittest.main()
