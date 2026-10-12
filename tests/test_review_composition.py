"""T-002.4 task-local composition evidence: fixture data, inheritance, T-005.

The composition connects authority/verification/preflight context and current
implementations/tests to discovery and decision inputs. These assertions
reject a composition that loses preflight-only context, drops an unfinished
row, copies prior gate labels, or relabels constructed records as observed
role outputs.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from review_fixture_support import (
    ACCEPTANCE_EVALS,
    ACCEPTANCE_FIXTURE,
    ACCEPTANCE_SKILL,
    CONTEXTUAL_CONTRAST_SETUPS,
    DISCOVERY_EVALS,
    DISCOVERY_FIXTURE,
    DISCOVERY_SKILL,
    PREFLIGHT_EVALS,
    ROOT,
    normalized,
)
from staging_fixture_support import stage_setup

TASK_MAP = ROOT / "docs" / "task-map.json"
COMPOSITION_PATH = ROOT / "docs" / "tasks" / "T-002.4" / "composition.json"

T0034_COMPOSITION_PATH = ROOT / "docs" / "tasks" / "T-003.4" / "composition.json"
T0034_RESULTS_PATH = ROOT / "docs" / "tasks" / "T-003.4" / "results.md"
FLOW_README = ROOT / "skills" / "task-implementation-flow" / "README.md"
IMPLEMENTER_SKILL = (
    ROOT / "skills" / "task-implementation-flow" / "bounded-task-implementer" / "SKILL.md"
)
IMPLEMENTER_FIXTURE = (
    ROOT
    / "skills"
    / "task-implementation-flow"
    / "bounded-task-implementer"
    / "evals"
    / "files"
    / "setup_fixture.py"
)
MAINTAINABILITY_FIXTURE = (
    ROOT
    / "skills"
    / "task-implementation-flow"
    / "task-maintainability-review"
    / "evals"
    / "files"
    / "setup_fixture.py"
)


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
        return stage_setup(self, fixture, scenario)


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

        # Malformed-invoice export behavior is not restaged here: the same
        # inputs, failures and persisted-state oracles belong to the canonical
        # probes in tests/test_contextual_export_risks.py
        # (test_failed_risky_export_destroys_the_existing_ledger,
        # test_failed_mitigated_export_preserves_the_existing_ledger). This
        # test keeps only the COMP-01 composition-specific assertions.


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



class T0034ComposedHandoffTests(unittest.TestCase):
    """T-003.4 composed handoff continuity and installed source projection.

    These assertions reconcile the reviewed T-003.1-.3 child-owned cases with
    the public route guidance and this task's compact composition record. They
    reject a composition that drops a confirmed finding, loses a row identity,
    merges distinct conditional routes, rescues stale readiness with current
    proof, copies a premature gate label, or relabels constructed records as
    observed role outputs. T-002.4 history stays owned by the predecessor
    class above; these cases reference child-owned setup instead of restaging it.
    """

    @classmethod
    def setUpClass(cls):
        cls.implementer_work = Path(tempfile.mkdtemp(prefix="t0034-implementer-"))
        cls.addClassCleanup(
            shutil.rmtree, cls.implementer_work, ignore_errors=True
        )
        cls.maintainability_work = Path(
            tempfile.mkdtemp(prefix="t0034-maintainability-")
        )
        cls.addClassCleanup(
            shutil.rmtree, cls.maintainability_work, ignore_errors=True
        )
        for fixture, root, scenario in (
            (IMPLEMENTER_FIXTURE, cls.implementer_work, "route-cases"),
            (IMPLEMENTER_FIXTURE, cls.implementer_work, "record-correction"),
            (MAINTAINABILITY_FIXTURE, cls.maintainability_work, "four-blockers"),
            (MAINTAINABILITY_FIXTURE, cls.maintainability_work, "genuine-stop"),
        ):
            subprocess.run(
                [sys.executable, str(fixture), scenario],
                check=True,
                cwd=ROOT,
                env=os.environ | {"EVAL_WORK_ROOT": str(root)},
            )

    @property
    def composition(self) -> dict:
        return json.loads(T0034_COMPOSITION_PATH.read_text(encoding="utf-8"))

    def record(self, record_id: str) -> dict:
        return next(
            item for item in self.composition["records"] if item["id"] == record_id
        )

    def staged_route(self, case_id: str) -> str:
        preflight = (
            self.implementer_work
            / "route-cases"
            / "docs"
            / "tasks"
            / case_id
            / "preflight.md"
        ).read_text(encoding="utf-8")
        return preflight.split("Expected submission route: ", 1)[1].splitlines()[0]

    def test_composition_labels_and_child_references_resolve(self):
        data = self.composition
        self.assertIn("fixture data", data["status"])
        self.assertIn("never observed role outputs", data["status"])
        consumers = json.dumps(data["intended_consumers"])
        for role in (
            "task-review-discovery",
            "task-acceptance-review",
            "task-preflight",
            "T-005",
        ):
            self.assertIn(role, consumers)
        categories = json.dumps(data["evidence_categories"])
        for token in (
            "structural_tests",
            "actual_behavior",
            "semantic_contract_inspection",
            "unrun_agent_compliance",
        ):
            self.assertIn(token, categories)
        self.assertIn(
            "no actual skill-call agent",
            data["evidence_categories"]["unrun_agent_compliance"],
        )

        by_skill = {
            "task-acceptance-review": {
                item["id"]: item
                for item in json.loads(
                    ACCEPTANCE_EVALS.read_text(encoding="utf-8")
                )["evals"]
            },
            "task-review-discovery": {
                item["id"]: item
                for item in json.loads(
                    DISCOVERY_EVALS.read_text(encoding="utf-8")
                )["evals"]
            },
            "task-preflight": {
                item["id"]: item
                for item in json.loads(PREFLIGHT_EVALS.read_text(encoding="utf-8"))[
                    "evals"
                ]
            },
        }
        for entry in data["child_case_references"]:
            with self.subTest(reference=entry["id"]):
                self.assertTrue((ROOT / entry["owner_test"]).is_file(), entry["owner_test"])
                self.assertTrue((ROOT / entry["fixture"]).is_file(), entry["fixture"])
                self.assertTrue(entry["signal"])
                for reference in entry.get("evals", []):
                    item = by_skill[reference["skill"]][reference["eval_id"]]
                    self.assertEqual(
                        reference["scenario"],
                        item["execution"]["setup"]["command"][2],
                    )
                if entry.get("owner_test_confirms_scenarios"):
                    owner = (ROOT / entry["owner_test"]).read_text(encoding="utf-8")
                    for scenario in entry["scenarios"]:
                        self.assertIn(scenario, owner, scenario)
                if entry.get("scenario_inventory") == (
                    "review_fixture_support.CONTEXTUAL_CONTRAST_SETUPS"
                ):
                    for scenario in entry["scenarios"]:
                        self.assertIn(scenario, CONTEXTUAL_CONTRAST_SETUPS, scenario)

    def test_route_matrix_reconciles_supplied_cases_with_public_overviews(self):
        record = self.record("ROUTE-01")
        tasks = self.implementer_work / "route-cases" / "docs" / "tasks"
        case_ids = {path.name for path in tasks.iterdir()}
        for prefix in ("INIT-", "STATE-", "CORR-"):
            self.assertTrue(
                any(case_id.startswith(prefix) for case_id in case_ids), prefix
            )
        for row in record["policy_matrix"]:
            self.assertEqual(
                row["full_route"], self.staged_route(row["case"]), row["case"]
            )
        for case_id, expected in record["currentness_and_reentry_examples"].items():
            self.assertEqual(expected, self.staged_route(case_id), case_id)

        for doc, tokens in (
            (
                ROOT / "README.md",
                (
                    "names the first outstanding applicable stage and the complete ordered remainder",
                    "a conditional stage counts only with evidence current for the submitted bytes",
                    "a production correction re-enters the stages it affected before fresh discovery and acceptance",
                ),
            ),
            (
                ROOT / "skills" / "README.md",
                (
                    "names the first outstanding applicable stage and the complete ordered remainder",
                    "A conditional stage counts only with evidence current for the submitted bytes",
                    "production corrections re-enter the stages they affected before fresh discovery and acceptance",
                ),
            ),
            (
                FLOW_README,
                (
                    "name the first outstanding applicable stage and the complete ordered remainder",
                    "Current applicable evidence for the corrected bytes keeps an unaffected stage out of the route",
                    "re-enters every conditional stage whose reviewed scope the correction affected",
                ),
            ),
        ):
            text = normalized(doc)
            for token in tokens:
                self.assertIn(token, text, str(doc))

        implementer = normalized(IMPLEMENTER_SKILL)
        self.assertIn("Name the complete ordered submission route", implementer)

    def test_four_confirmed_findings_reach_the_correction_input_without_loss(self):
        record = self.record("FIND-01")
        oracle = normalized(
            self.maintainability_work
            / "task-runs"
            / "MNT-42"
            / "maintainability-oracle.md"
        )
        self.assertEqual(
            ["MNT-B1", "MNT-B2", "MNT-B3", "MNT-B4"], record["findings"]
        )
        for finding in record["findings"]:
            self.assertIn(f"### {finding}", oracle)
            section = oracle.split(f"### {finding}", 1)[1].split("###", 1)[0]
            for heading in record["finding_fields"]:
                self.assertIn(heading, section, finding)
        for token in tuple(record["oracle_integrity_tokens"]) + (
            "Non-blocking preference control",
            "no confirmed material regression",
        ):
            self.assertIn(token, oracle)
        correction_input = record["correction_input"]
        self.assertEqual(record["findings"], correction_input["carried_findings"])
        self.assertEqual(4, len(correction_input["carried_findings"]))
        self.assertIn("no cap", correction_input["integrity_rule"])

    def test_rows_stop_history_and_mixed_routes_survive_composition(self):
        record = self.record("ROWS-01")
        root = self.implementer_work / "result-record"
        review = normalized(
            root / "docs" / "tasks" / "REC-44" / "reviews" / "acceptance-01.md"
        )
        for row, state in record["row_states"].items():
            self.assertIn(f"{row} — {state}", review, row)
        self.assertIn(
            "ROW-REPLAY-BOUNDARY", review.split("Remaining obligations:")[1]
        )

        attempts = json.loads(
            (root / "attempts" / "stop.json").read_text(encoding="utf-8")
        )
        self.assertEqual(record["stop_record"]["attempts"], len(attempts["attempts"]))
        self.assertEqual(
            record["stop_record"]["distinct_targets"],
            len({attempt["target"] for attempt in attempts["attempts"]}),
        )
        self.assertEqual(record["stop_record"]["status"], attempts["status"])
        self.assertEqual(record["stop_record"]["next_owner"], attempts["next_owner"])
        self.assertEqual(
            record["stop_record"]["unfinished_rows"], attempts["unfinished_rows"]
        )
        self.assertEqual(
            set(record["stop_record"]["coverage_states"]),
            set(attempts["coverage_rows"].values()),
        )
        for attempt in attempts["attempts"]:
            result = subprocess.run(
                [sys.executable, attempt["probe"]],
                cwd=root,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(0, result.returncode, attempt["probe"])
            self.assertIn("AssertionError", result.stderr)
            self.assertTrue(attempt["hypothesis"])

        self.assertEqual(
            "CHANGES_REQUESTED",
            record["mixed_condition_routes"]["mixed-conditions-authorized-decision"],
        )
        self.assertEqual(
            "INCONCLUSIVE",
            record["mixed_condition_routes"]["mixed-conditions-forbidden-decision"],
        )
        blob = json.dumps(record)
        for token in (
            "unfinished siblings",
            "permits advancement",
            "silent third ordinary fix",
        ):
            self.assertIn(token, blob)

    def test_effect_routes_and_revision_recovery_stay_distinct(self):
        record = self.record("EFF-01")
        cases = json.loads(
            (
                self.implementer_work / "route-cases" / "change-effects" / "cases.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(set(record["case_routes"]), set(cases))
        for name, route in record["case_routes"].items():
            self.assertEqual(route, cases[name]["route"], name)
        for name, fails in (
            ("reference", False),
            ("reference-missing-proof", False),
            ("reference-executable", True),
        ):
            folder = (
                self.implementer_work / "route-cases" / "change-effects" / name / "after"
            )
            probe = subprocess.run(
                [sys.executable, "-c", record["reference_probe"]],
                cwd=folder,
                capture_output=True,
                text=True,
            )
            self.assertEqual(fails, probe.returncode != 0, name)
            if fails:
                self.assertIn("AssertionError", probe.stderr)
        self.assertTrue(cases["reference"]["current_proof"])
        self.assertFalse(cases["reference-missing-proof"]["current_proof"])
        self.assertIn(
            record["tests_only_rule"], cases["tests-policy-exception"]["policy"]
        )

        revision = self.record("REV-01")
        flow = normalized(FLOW_README)
        for token in revision["source_guidance_tokens"]:
            self.assertIn(token, flow)

    def test_gate_records_and_dispositions_keep_their_owners_and_visibility(self):
        gate = self.record("GATE-01")
        self.assertEqual(
            ["command", "status", "owner", "stage", "reason"],
            gate["gate_record_fields"],
        )
        flow = normalized(FLOW_README)
        for token in gate["source_guidance_tokens"]:
            self.assertIn(token, flow)

        disposition = self.record("DISP-01")
        self.assertEqual(6, len(set(disposition["reopening_reasons"])))
        for token in disposition["source_guidance_tokens"]:
            self.assertIn(token, flow)
        for scenario in disposition["repeated_review_scenarios"]:
            self.assertIn(scenario, CONTEXTUAL_CONTRAST_SETUPS, scenario)

    def test_installer_projection_record_and_t005_handoff_stay_truthful(self):
        data = self.composition
        projection = data["installer_projection"]
        self.assertEqual(
            ["bounded-task-implementer"],
            projection["changed_families_by_child"]["T-003.1"],
        )
        self.assertEqual(
            ["task-maintainability-review"],
            projection["changed_families_by_child"]["T-003.2"],
        )
        self.assertEqual(
            ["task-acceptance-review", "task-review-discovery"],
            projection["changed_families_by_child"]["T-003.3"],
        )
        ownership = projection["projection_ownership"]
        self.assertIn("tests/test_install_development_skills.py", json.dumps(ownership))
        for family in projection["affected_families"]:
            self.assertIn(family, ownership, family)
        self.assertIn("unchanged", projection["declarations"])
        self.assertIn(
            "no refresh of the active repository .agents",
            projection["active_installation"],
        )

        boundaries = data["t005_unrun_boundaries"]
        self.assertGreaterEqual(len(boundaries), 6)
        for boundary in boundaries:
            self.assertEqual("T-005", boundary["owner"])
            self.assertTrue(boundary["unrun_reason"])
        inventory = json.dumps(boundaries)
        for topic in (
            "bounded-task-implementer",
            "task-maintainability-review",
            "task-contract-registry-updater",
            "task-review-discovery",
            "task-acceptance-review",
            "correction re-entry",
            "focused preflight",
            "mixed correction/evidence/authority",
        ):
            self.assertIn(topic, inventory, topic)
        blob = json.dumps(data)
        self.assertNotIn("behavioral qualification passed", blob)
        self.assertNotIn("installed flow is qualified", blob)

        results = normalized(T0034_RESULTS_PATH)
        for token in (
            "Contract structure",
            "Real fixture",
            "Unrun agent behavior",
            "fixture data",
            "PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_review_composition.py",
            "PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py",
            "T-005",
        ):
            self.assertIn(token, results, token)


if __name__ == "__main__":
    unittest.main()
