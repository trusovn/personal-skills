"""T-002.4 task-local composition evidence: fixture data, inheritance, T-005.

The composition connects authority/verification/preflight context and current
implementations/tests to discovery and decision inputs. These assertions
reject a composition that loses preflight-only context, drops an unfinished
row, copies prior gate labels, or relabels constructed records as observed
role outputs.
"""

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from review_fixture_support import (
    ACCEPTANCE_EVALS,
    ACCEPTANCE_FIXTURE,
    ACCEPTANCE_SKILL,
    DISCOVERY_EVALS,
    DISCOVERY_FIXTURE,
    DISCOVERY_SKILL,
    PREFLIGHT_EVALS,
    ROOT,
    normalized,
)

TASK_MAP = ROOT / "docs" / "task-map.json"
COMPOSITION_PATH = ROOT / "docs" / "tasks" / "T-002.4" / "composition.json"


class ComposedQualificationSetupTests(unittest.TestCase):
    """T-002.4 task-local composition of the predecessor fixtures.

    The composition connects authority/verification/preflight context and
    current implementations/tests to discovery and decision inputs. These
    assertions reject a composition that loses preflight-only context, drops
    an unfinished row, copies prior gate labels, or relabels constructed
    records as observed role outputs.
    """

    @property
    def composition(self) -> dict:
        return json.loads(COMPOSITION_PATH.read_text(encoding="utf-8"))


    def record(self, record_id: str) -> dict:
        return next(
            item for item in self.composition["records"] if item["id"] == record_id
        )


    def stage(self, fixture: Path, scenario: str) -> Path:
        temporary = TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        work = Path(temporary.name)
        env = dict(os.environ, EVAL_WORK_ROOT=str(work))
        subprocess.run(
            [sys.executable, str(fixture), scenario],
            check=True,
            env=env,
            capture_output=True,
        )
        return work


    def test_composition_is_explicitly_labeled_fixture_data(self):
        data = self.composition
        self.assertIn("fixture data", data["status"])
        self.assertIn("never observed role outputs", data["status"])
        consumers = json.dumps(data["intended_consumers"])
        for role in ("task-review-discovery", "task-acceptance-review", "task-preflight"):
            self.assertIn(role, consumers)
        self.assertIn("T-005", consumers)
        categories = json.dumps(data["evidence_categories"])
        for token in (
            "structural_tests",
            "actual_behavior",
            "semantic_contract_inspection",
            "unrun_agent_compliance",
        ):
            self.assertIn(token, categories)
        self.assertIn(
            "no actual skill-call agent", data["evidence_categories"]["unrun_agent_compliance"]
        )


    def test_preflight_only_exposure_survives_into_discovery_and_decision_inputs(self):
        record = self.record("COMP-01")
        self.assertEqual(
            "contextual-risk-blockers-decision", record["scenario"]
        )
        work = self.stage(ACCEPTANCE_FIXTURE, "contextual-risk-blockers-decision")
        root = work / "contextual-runner"
        preflight = normalized(root / "docs" / "tasks" / "INV-07" / "preflight.md")
        exposure = record["upstream_context"]["exposure_only_in_preflight"]
        self.assertIn(exposure, preflight)
        self.assertIn(exposure, record["discovery_input"]["exposure_preserved"])
        discovery = normalized(work / "task-runs" / "INV-07" / "discovery-01.md")
        self.assertNotIn(exposure, discovery)
        self.assertEqual("CHANGES_REQUESTED", record["decision_input"]["expected_route"])
        self.assertIn(
            "passing ACs do not erase material-risk decision obligations",
            json.dumps(record["decision_input"]),
        )

        out = root / "out" / "ledger.csv"
        out.parent.mkdir(parents=True)
        out.write_text("inv-9001,10.00\n")
        invoices = root / "bad-invoices.json"
        invoices.write_text(
            json.dumps([{"id": "inv-1", "amount": "5.25"}, {"id": "inv-2", "amount": "oops"}])
        )
        failed = subprocess.run(
            [sys.executable, "-m", "src.invoices.export", str(invoices), str(out)],
            cwd=root,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(failed.returncode, 0)
        self.assertEqual("", out.read_text())

        mitigated = self.stage(ACCEPTANCE_FIXTURE, "contextual-risk-mitigated-decision")
        mitigated_root = mitigated / "contextual-runner"
        mitigated_out = mitigated_root / "out" / "ledger.csv"
        mitigated_out.parent.mkdir(parents=True)
        mitigated_out.write_text("inv-9001,10.00\n")
        mitigated_invoices = mitigated_root / "bad-invoices.json"
        mitigated_invoices.write_text(
            json.dumps([{"id": "inv-1", "amount": "5.25"}, {"id": "inv-2", "amount": "oops"}])
        )
        controlled = subprocess.run(
            [
                sys.executable,
                "-m",
                "src.invoices.export",
                str(mitigated_invoices),
                str(mitigated_out),
            ],
            cwd=mitigated_root,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(controlled.returncode, 0)
        self.assertEqual("inv-9001,10.00\n", mitigated_out.read_text())


    def test_mixed_conditions_retain_ids_reasons_owners_and_both_routes(self):
        record = self.record("COMP-02")
        work = self.stage(ACCEPTANCE_FIXTURE, "mixed-conditions-authorized-decision")
        authorized = (work / "task-runs" / "JOB-05" / "discovery-01.md").read_text()
        row = record["discovery_input"]["unfinished_row"]
        self.assertEqual("JOB-PAIR", row["id"])
        self.assertEqual("blocked", row["state"])
        self.assertIn("pair_claims.py", row["reason"])
        self.assertTrue(row["next_owner"])
        self.assertIn(row["id"] + "=blocked", authorized)
        root = work / "mixed-runner"
        self.assertFalse((root / "tests" / "helpers" / "pair_claims.py").exists())

        routes = {entry["scenario"]: entry for entry in record["decision_inputs"]}
        self.assertEqual(
            "CHANGES_REQUESTED", routes["mixed-conditions-authorized-decision"]["expected_route"]
        )
        self.assertEqual(
            "INCONCLUSIVE", routes["mixed-conditions-forbidden-decision"]["expected_route"]
        )
        for entry in record["decision_inputs"]:
            self.assertIn("no advancement", entry["rule"])

        forbidden = self.stage(ACCEPTANCE_FIXTURE, "mixed-conditions-forbidden-decision")
        policy = json.loads(
            (forbidden / "task-runs" / "policies" / "local-review-mixed.json").read_text()
        )
        self.assertIn("production edits in this review cycle", policy["deny"][0])


    def test_correction_records_carry_current_evidence_and_discovery_owned_gates(self):
        record = self.record("COMP-03")
        failure = record["supplied_failure"]
        self.assertEqual("F-01", failure["finding_id"])
        self.assertEqual("P1", failure["suggested_priority"])
        self.assertEqual({"QR-R1", "QR-R2", "QR-R3"}, set(failure["coverage_rows"]))
        self.assertIn("finding F-01", failure["coverage_rows"]["QR-R2"])
        self.assertEqual("QR-R3", failure["unfinished_row"]["id"])
        prior_gate = failure["gate_record"]
        self.assertEqual("python -m unittest discover -s tests", prior_gate["command"])
        self.assertEqual("not run", prior_gate["status"])
        self.assertEqual("prior discovery", prior_gate["stage"])
        self.assertTrue(prior_gate["owner"] and prior_gate["reason"])

        correction = record["correction"]
        self.assertEqual(
            "python -m unittest tests.integration.test_run_next",
            correction["reviewer_regression"],
        )
        self.assertIn(
            "test_retry_after_completion_adds_no_duplicate",
            correction["corrected_bytes"],
        )
        self.assertEqual(
            set(failure["coverage_rows"]), set(correction["continuation_rows"])
        )
        for row_id, disposition in failure["coverage_rows"].items():
            self.assertTrue(
                correction["continuation_rows"][row_id].startswith(
                    disposition.split(" —")[0]
                ),
                row_id,
            )
        self.assertEqual("F-01 (suggested P1)", correction["continuation_finding_ids"])
        clean_gate = correction["expected_clean_discovery"]["gate_record"]
        self.assertEqual(prior_gate["command"], clean_gate["command"])
        self.assertEqual("discovery", clean_gate["owner"])
        self.assertIn(
            "without executing the aggregate again",
            correction["expected_clean_discovery"]["decision_input"],
        )

        work = self.stage(DISCOVERY_FIXTURE, "discovery-correction-gate")
        staged_report = normalized(
            work / "corrected-queue" / "docs" / "tasks" / "QR-12" / "reviews" / "discovery-01.md"
        )
        self.assertIn("F-01 [suggested P1]", staged_report)
        self.assertIn("QR-R1: AC-01 first invocation — pass", staged_report)
        self.assertIn(
            "QR-R2: AC-01 second invocation — fail (second invocation returned None; finding F-01)",
            staged_report,
        )
        self.assertIn(
            "QR-R3: AC-02 retry row — unchecked (not reached before the pass stopped)",
            staged_report,
        )
        self.assertIn(
            "not run; decisive targeted failure; owner: fresh correction discovery",
            staged_report,
        )
        continuation = normalized(work / "task-runs" / "QR-12" / "discovery-continuation.md")
        self.assertIn("QR-R1=pass; QR-R2=fail (F-01); QR-R3=unchecked", continuation)
        self.assertIn(correction["reviewer_regression"], continuation)
        self.assertIn(
            "Aggregate gate: not run after decisive targeted failure; owner: fresh correction discovery",
            continuation,
        )
        regression = subprocess.run(
            [sys.executable, "-m", "unittest", "tests.integration.test_run_next"],
            cwd=work / "corrected-queue",
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, regression.returncode, regression.stderr)
        self.assertIn("OK", regression.stderr)

        late = record["late_omission"]
        self.assertEqual({"LED-R1", "LED-R3"}, set(late["prior_report_rows"]))
        self.assertEqual("LED-R2", late["omitted_row"]["id"])
        premature = late["premature_gate_record"]
        self.assertEqual(prior_gate["command"], premature["command"])
        self.assertEqual("run, passed", premature["status"])
        self.assertIn("recorded as premature", premature["reason"])
        self.assertIn("runs before any fresh aggregate", late["ordering"])
        diagnostic = record["diagnostic_aggregate"]
        self.assertIn("discovery-02.md", diagnostic["continuation"])
        self.assertIn(
            "does not erase failed or unfinished rows", diagnostic["authorization"]
        )
        self.assertIn("record the earlier aggregate gate as premature", normalized(DISCOVERY_SKILL))
        self.assertIn(
            "only discovery owns a still-justified rerun", normalized(ACCEPTANCE_SKILL)
        )

        for scenario, boolean_exit in (
            ("discovery-late-omission-clean", 2),
            ("discovery-late-omission-fail", 0),
        ):
            with self.subTest(scenario=scenario):
                work = self.stage(DISCOVERY_FIXTURE, scenario)
                workspace = work / "late-omission"
                valid = json.loads((workspace / "cases" / "valid.json").read_text())
                case = work / "boolean.json"
                case.write_text(json.dumps(dict(valid, revision=True)))
                run = subprocess.run(
                    [sys.executable, "-m", "src.ledger.validate", str(case)],
                    cwd=workspace,
                    capture_output=True,
                )
                self.assertEqual(boolean_exit, run.returncode)


    def test_deferral_records_connect_to_relevant_and_unrelated_preflight_inputs(self):
        record = self.record("COMP-04")
        self.assertIn(
            "the human coordinator alone records", record["coordinator_record"]["writer"]
        )
        self.assertIn("never write the tracker", record["coordinator_record"]["writer"])
        work = self.stage(ACCEPTANCE_FIXTURE, "known-issue-consumption-decision")
        record_text = normalized(work / "ledger-consumer" / "docs" / "known-issues.md")
        for field in record["coordinator_record"]["fields"]:
            self.assertIn(field, record_text)
        self.assertIn(
            "Provenance: task INV-07; review acceptance-01; finding INV-M01",
            record_text,
        )
        self.assertIn("Affected consumers: `report-ledger` (informational; compatible today)", record_text)

        cases = {entry["case"]: entry for entry in record["later_preflight_inputs"]}
        for required in (
            "relevant, unchanged exposure",
            "relevant, changed exposure",
            "unrelated task",
            "priority-only change",
            "separately scoped record",
        ):
            self.assertIn(required, cases)
        self.assertEqual("RPT-12A", cases["relevant, unchanged exposure"]["consumer"])
        self.assertEqual("RPT-12B", cases["relevant, changed exposure"]["consumer"])
        self.assertEqual("WEB-02", cases["unrelated task"]["consumer"])
        self.assertEqual("ORD-04", cases["separately scoped record"]["consumer"])
        self.assertIn(
            "routes through the record's follow-up owner",
            cases["relevant, changed exposure"]["expected"],
        )
        self.assertIn(
            "no defect obligation",
            cases["unrelated task"]["expected"],
        )
        self.assertIn(
            "does not reopen task acceptance",
            cases["priority-only change"]["expected"],
        )
        self.assertIn(
            "must not be conflated with the INV-07 export-footer KI-001",
            cases["separately scoped record"]["compatibility"],
        )

        unchanged = self.stage(ACCEPTANCE_FIXTURE, "known-issue-proposed-work-decision")
        rpta_preflight = normalized(
            unchanged / "ledger-consumer" / "docs" / "tasks" / "RPT-12A" / "preflight.md"
        )
        self.assertIn("compatibility/exposure unchanged", rpta_preflight)
        self.assertIn("KI-001", rpta_preflight)
        rpta_discovery = normalized(unchanged / "task-runs" / "RPT-12A" / "discovery-01.md")
        self.assertIn("KI-RECHECK", rpta_discovery)
        self.assertIn("reassessed — unchanged", rpta_discovery)
        self.assertIn("No new confirmed findings", rpta_discovery)

        rptb_preflight = normalized(
            work / "ledger-consumer" / "docs" / "tasks" / "RPT-12B" / "preflight.md"
        )
        self.assertIn("KI-001", rptb_preflight)
        self.assertIn("requiring UTC", rptb_preflight)
        discovery = normalized(work / "task-runs" / "RPT-12B" / "discovery-01.md")
        self.assertIn("KI-REASSESS", discovery)
        self.assertIn("reassessed — changed exposure", discovery)
        self.assertIn("unrelated tasks (such as WEB-02)", discovery)
        self.assertIn("such as RPT-12A, whose footer is informational", discovery)

        web = normalized(work / "ledger-consumer" / "docs" / "tasks" / "WEB-02" / "brief.md")
        self.assertIn("Cache-bust web assets", web)
        self.assertNotIn("KI-001", web)

        correction = self.stage(ACCEPTANCE_FIXTURE, "correction-regression-decision")
        ord_known = normalized(
            correction / "correction-runner" / "docs" / "known-issues.md"
        )
        self.assertIn(
            "Provenance: task ORD-04; review acceptance-01; finding ORD-L01",
            ord_known,
        )
        self.assertIn(
            "KI-001 — ORD-04 retry log wording",
            ord_known,
        )
        for foreign in ("INV-M01", "RPT-12A", "RPT-12B", "report-ledger"):
            self.assertNotIn(foreign, ord_known, foreign)
        ord_preflight = normalized(
            correction / "correction-runner" / "docs" / "tasks" / "ORD-04" / "preflight.md"
        )
        self.assertIn("exposure is unchanged", ord_preflight)
        self.assertIn("KI-001 (retry log", ord_preflight)

        priority = self.stage(ACCEPTANCE_FIXTURE, "known-issue-priority-only-decision")
        plan = json.loads(
            (priority / "ledger-consumer" / "cases" / "follow-up.json").read_text()
        )
        self.assertEqual("next", plan["prior_priority"])
        self.assertEqual("later", plan["current_priority"])
        priority_preflight = normalized(
            priority / "ledger-consumer" / "docs" / "tasks" / "RPT-12A" / "preflight.md"
        )
        self.assertIn("scheduling label only, no material fact changed", priority_preflight)


    def test_prepared_and_direct_routes_preserve_inputs_and_provenance(self):
        record = self.record("COMP-05")
        blob = json.dumps(record)
        for token in ("brief.md", "verification.md", "preflight.md"):
            self.assertIn(token, blob)
        self.assertIn("guided direct request", blob)
        self.assertIn("SELF_CHECK_ONLY", blob)
        self.assertIn("fresh discovery call", blob)
        self.assertIn(
            "coordinator recording precedes authorized continuation", blob
        )
        discovery = normalized(DISCOVERY_SKILL)
        self.assertIn("SELF_CHECK_ONLY", discovery)
        self.assertIn("The route is always a fresh discovery call", discovery)


    def test_inherited_case_inventory_preserves_every_predecessor_case(self):
        inventory = self.composition["inherited_case_inventory"]
        kinds = {entry["kind"] for entry in inventory}
        for kind in (
            "lifecycle-repetition",
            "lifecycle-resume",
            "lifecycle-retry",
            "missing-capability",
            "index-worktree-identity",
            "ledger-cardinality-order-type",
            "workflow-tampering-replay-decision",
            "validator-valid-targeted-invalid",
            "process-resistant-descendant",
            "process-pipe",
            "process-race",
            "public-entry",
            "continuation",
            "self-check-provenance",
            "preflight-readiness",
        ):
            self.assertIn(kind, kinds)

        by_skill = {
            "task-review-discovery": {
                item["id"]: item
                for item in json.loads(DISCOVERY_EVALS.read_text(encoding="utf-8"))["evals"]
            },
            "task-acceptance-review": {
                item["id"]: item
                for item in json.loads(ACCEPTANCE_EVALS.read_text(encoding="utf-8"))["evals"]
            },
            "task-preflight": {
                item["id"]: item
                for item in json.loads(PREFLIGHT_EVALS.read_text(encoding="utf-8"))["evals"]
            },
        }
        for entry in inventory:
            source = entry["source"]
            with self.subTest(case=entry["id"]):
                self.assertIn(source["skill"], by_skill)
                self.assertIn(source["eval_id"], by_skill[source["skill"]])
                item = by_skill[source["skill"]][source["eval_id"]]
                if "scenario" in source:
                    self.assertEqual(
                        source["scenario"],
                        item["execution"]["setup"]["command"][2],
                    )
                self.assertTrue(entry["signal"])


    def test_qualification_ownership_follows_the_authoritative_task_map(self):
        data = self.composition
        task_map = json.loads(TASK_MAP.read_text(encoding="utf-8"))
        tasks = {task["id"]: task for task in task_map["tasks"]}
        self.assertIn("T-005", tasks)
        self.assertNotIn("T-002.5", tasks)
        blob = json.dumps(data)
        self.assertNotIn("T-002.5", blob)
        t005 = tasks["T-005"]
        self.assertIn("Qualify", t005["title"])
        self.assertIn("ART-012", t005["produces"])
        self.assertTrue(
            any(
                consumer.startswith("T-005 — actual separate producing/consuming role calls")
                for consumer in data["intended_consumers"]
            )
        )
        for boundary in data["t005_unrun_boundaries"]:
            self.assertEqual("T-005", boundary["owner"])


    def test_unrun_t005_boundaries_are_explicit(self):
        data = self.composition
        boundaries = data["t005_unrun_boundaries"]
        self.assertGreaterEqual(len(boundaries), 4)
        for boundary in boundaries:
            self.assertEqual("T-005", boundary["owner"])
            self.assertTrue(boundary["unrun_reason"])
        blob = json.dumps(data)
        self.assertNotIn("behavioral qualification passed", blob)
        self.assertNotIn("installed flow is qualified", blob)



if __name__ == "__main__":
    unittest.main()
