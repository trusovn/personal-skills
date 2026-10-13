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


T0051_PACKAGE = ROOT / "docs" / "tasks" / "T-005.1"
T0051_FIXTURES = T0051_PACKAGE / "fixtures.md"
T0051_EVIDENCE = T0051_PACKAGE / "evidence"
TASKS_INDEX = ROOT / "docs" / "tasks" / "index.json"
INT_FLOW_RESULTS = ROOT / "docs" / "tasks" / "INT-FLOW-001" / "results.md"

T0051_RECORD_CASE_SOURCE = {
    "ROUTE-01": "CCR-01",
    "FIND-01": "CCR-04",
    "ROWS-01": "CCR-03",
    "REV-01": "CCR-07",
    "EFF-01": "CCR-02",
    "GATE-01": "CCR-06",
    "DISP-01": "CCR-08",
}
T0051_FIXTURE_SUFFIX = {
    "acceptance": "task-acceptance-review/evals/files/setup_fixture.py",
    "discovery": "task-review-discovery/evals/files/setup_fixture.py",
}


def t0051_inventory() -> dict:
    """Load the machine-readable T-005.1 case inventory from fixtures.md."""
    text = T0051_FIXTURES.read_text(encoding="utf-8")
    start = text.index("```json\n") + len("```json\n")
    end = text.index("\n```", start)
    return json.loads(text[start:end])


def t0051_expected_ids() -> set:
    """Every inherited or declared identity the inventory must carry."""
    t0024 = json.loads(COMPOSITION_PATH.read_text(encoding="utf-8"))
    t0034 = json.loads(T0034_COMPOSITION_PATH.read_text(encoding="utf-8"))
    ids = {entry["id"] for entry in t0024["inherited_case_inventory"]}
    ids |= {record["id"] for record in t0024["records"]}
    ids |= {ref["id"] for ref in t0034["child_case_references"]}
    ids |= {record["id"] for record in t0034["records"]}
    ids |= {"IFQ-01", "IFQ-02", "IFQ-03"}
    return ids


def t0051_audit_problems(inventory: dict, expected_ids: set) -> list:
    """Audit one inventory against inherited records and current selectors.

    Returns the complete problem list; an empty list means the audit passes.
    Shared by the passing audit and the wrong control so the discrimination
    is proven against the same oracle.
    """
    problems: list = []
    entries = inventory.get("case_inventory", [])
    seen = [entry.get("id") for entry in entries]
    for cid in sorted(expected_ids - set(seen)):
        problems.append(f"{cid}: missing from inventory")
    for cid in sorted(set(seen) - expected_ids):
        problems.append(f"{cid}: not an inherited or declared identity")
    duplicates = sorted({cid for cid in seen if seen.count(cid) > 1})
    for cid in duplicates:
        problems.append(f"{cid}: duplicate inventory entry")

    t0024 = json.loads(COMPOSITION_PATH.read_text(encoding="utf-8"))
    t0034 = json.loads(T0034_COMPOSITION_PATH.read_text(encoding="utf-8"))
    t0024_cases = {entry["id"]: entry for entry in t0024["inherited_case_inventory"]}
    t0024_records = {record["id"]: record for record in t0024["records"]}
    t0034_refs = {ref["id"]: ref for ref in t0034["child_case_references"]}
    t0034_records = {record["id"]: record for record in t0034["records"]}
    registered = set(json.loads(TASKS_INDEX.read_text(encoding="utf-8"))["tasks"])
    intflow_text = " ".join(INT_FLOW_RESULTS.read_text(encoding="utf-8").split())
    allowed_levels = {"structural_tests", "actual_behavior", "unrun_agent_compliance"}
    required_fields = (
        "kind",
        "inherited_from",
        "setup",
        "workspace",
        "authority",
        "expected_oracle",
        "producer_consumer",
        "owning_leaf",
        "evidence_level",
        "current_evidence",
        "role_boundary",
    )
    for entry in entries:
        cid = entry.get("id", "<no-id>")
        for field in required_fields:
            if not entry.get(field):
                problems.append(f"{cid}: empty {field}")
        if entry.get("owning_leaf") not in registered:
            problems.append(
                f"{cid}: owning_leaf {entry.get('owning_leaf')!r} is not a registered task"
            )
        if entry.get("evidence_level") not in allowed_levels:
            problems.append(
                f"{cid}: unknown evidence_level {entry.get('evidence_level')!r}"
            )
        owner = entry.get("owner_test")
        if owner and not (ROOT / owner).is_file():
            problems.append(f"{cid}: owner test {owner} does not exist")
        fixture = entry.get("fixture")
        fixture_text = None
        if fixture:
            if not (ROOT / fixture).is_file():
                problems.append(f"{cid}: fixture {fixture} does not exist")
            else:
                fixture_text = (ROOT / fixture).read_text(encoding="utf-8")
        scenarios = list(entry.get("scenarios") or [])
        if entry.get("scenario"):
            scenarios.append(entry["scenario"])
        if fixture_text is not None:
            for scenario in scenarios:
                if f'"{scenario}":' not in fixture_text:
                    problems.append(
                        f"{cid}: scenario {scenario!r} is not dispatched by {fixture}"
                    )
        if cid in t0024_cases:
            source = t0024_cases[cid]["source"]
            if entry.get("skill") != source["skill"]:
                problems.append(f"{cid}: skill does not match T-002.4 inventory")
            if entry.get("eval_id") != source["eval_id"]:
                problems.append(f"{cid}: eval_id does not match T-002.4 inventory")
            if entry.get("scenario") != source.get("scenario"):
                problems.append(
                    f"{cid}: scenario does not match T-002.4 inventory selector"
                )
        if cid in t0024_records:
            record = t0024_records[cid]
            expected_scenarios = (
                [record["scenario"]] if "scenario" in record else list(record["scenarios"])
            )
            if entry.get("scenarios") != expected_scenarios:
                problems.append(
                    f"{cid}: scenarios do not match T-002.4 record"
                )
            if not str(entry.get("fixture", "")).endswith(
                T0051_FIXTURE_SUFFIX[record["fixture"]]
            ):
                problems.append(f"{cid}: fixture does not match T-002.4 record")
        if cid in t0034_refs:
            ref = t0034_refs[cid]
            if entry.get("owner_test") != ref["owner_test"]:
                problems.append(
                    f"{cid}: owner_test does not match T-003.4 reference"
                )
            if entry.get("fixture") != ref["fixture"]:
                problems.append(f"{cid}: fixture does not match T-003.4 reference")
            if entry.get("scenarios") != list(ref["scenarios"]):
                problems.append(
                    f"{cid}: scenarios do not match T-003.4 reference"
                )
        if cid in T0051_RECORD_CASE_SOURCE:
            ref = t0034_refs[T0051_RECORD_CASE_SOURCE[cid]]
            if (
                entry.get("fixture") != ref["fixture"]
                or entry.get("scenarios") != list(ref["scenarios"])
            ):
                problems.append(
                    f"{cid}: does not match its case_source "
                    f"{T0051_RECORD_CASE_SOURCE[cid]}"
                )
            if cid not in t0034_records:
                problems.append(f"{cid}: missing from T-003.4 records")
        if cid.startswith("IFQ-"):
            provenance = entry.get("intflow_provenance")
            if not provenance or " ".join(provenance.split()) not in intflow_text:
                problems.append(
                    f"{cid}: INT-FLOW-001 provenance is not quoted from "
                    "docs/tasks/INT-FLOW-001/results.md"
                )
        for pointer in entry.get("current_evidence", "").split(";"):
            candidate = pointer.split(" (")[0].strip()
            if candidate.startswith(("docs/", "tests/", "skills/")) and not (
                ROOT / candidate
            ).exists():
                problems.append(
                    f"{cid}: evidence pointer {candidate!r} does not resolve"
                )
    return problems


T0051_MANIFEST_HEADING = "## Consumer-visible handoff input manifests"
T0051_HANDOFF_LEAVES = ("T-005.2", "T-005.3", "T-005.4", "T-005.5", "T-005.6")
# Held-back records and answer keys that must never enter a consumer input
# set: the maintainability fixture's own contract keeps its oracle and the
# correction-round facts outside the reviewer workspace, and the route-cases
# change-effect key holds the expected submission routes.
T0051_REQUIRED_EVALUATOR_ONLY = {
    "four-blockers": {
        "task-runs/MNT-42/maintainability-oracle.md": "expected answers",
    },
    "correction-round": {
        "task-runs/MNT-42/correction-round-facts.md": "expected answers",
    },
    "route-cases": {
        "route-cases/change-effects/cases.json": "expected answers",
    },
}
# Producer-output positions the placeholder table claims that no staging
# supplies; only the named actual role call fills them.
T0051_REQUIRED_NOT_STAGED = {
    "queue-defect": {"task-runs/QR-12/discovery-01.md"},
    "integration-leaf": {"integration-leaf/docs/tasks/INT-9/verification.md"},
    "four-blockers": {
        "maintainability/docs/tasks/MNT-42/reviews/maintainability-01.md"
    },
    "correction-round": {
        "maintainability-correction/docs/tasks/MNT-42/reviews/maintainability-02.md"
    },
}
# The staged input sets each claimed handoff must identify.
T0051_REQUIRED_HANDOFF_STAGINGS = {
    "T-005.2": {"queue-defect", "integration-leaf"},
    "T-005.3": {
        "queue-defect",
        "mixed-conditions-authorized-decision",
        "contextual-risk-blockers-decision",
    },
    "T-005.4": {"known-issue-consumption-decision"},
    "T-005.5": {
        "four-blockers",
        "correction-round",
        "route-cases",
        "record-correction",
        "discovery-late-omission-clean",
    },
    "T-005.6": {"t0051-package"},
}


def t0051_manifests() -> dict:
    """Load the machine-readable handoff input manifests from fixtures.md."""
    text = T0051_FIXTURES.read_text(encoding="utf-8")
    start = text.index(T0051_MANIFEST_HEADING)
    start = text.index("```json\n", start) + len("```json\n")
    return json.loads(text[start : text.index("\n```", start)])


def t0051_manifest_problems(manifest: dict, roots: dict) -> list:
    """Audit the handoff input manifests against real staged input sets.

    ``roots`` maps staging ids to the directory the entry's paths must
    resolve against (a staged disposable workspace or the repository root);
    ids absent from ``roots`` get structural checks only. Returns the
    complete problem list; an empty list means the audit passes. Shared by
    the passing audit and the wrong control so the discrimination is proven
    against the same oracle.
    """
    problems: list = []
    registered = set(json.loads(TASKS_INDEX.read_text(encoding="utf-8"))["tasks"])
    inventory_ids = t0051_expected_ids()
    sets_by_id: dict = {}
    set_ids: list = []
    for staged in manifest.get("staged_input_sets", []):
        sid = staged.get("staging_id", "<no-set>")
        set_ids.append(sid)
        if sid in sets_by_id:
            problems.append(f"{sid}: duplicate staged input set")
            continue
        sets_by_id[sid] = staged
    handoffs = manifest.get("handoff_manifests", [])
    claimed = {
        ref for handoff in handoffs for ref in handoff.get("staging_refs", [])
    }
    leaves = [handoff.get("owning_leaf") for handoff in handoffs]
    for leaf in T0051_HANDOFF_LEAVES:
        if leaf not in leaves:
            problems.append(f"{leaf}: missing handoff manifest")
    for leaf in sorted(set(leaves) - set(T0051_HANDOFF_LEAVES)):
        problems.append(f"{leaf}: not a claimed handoff leaf")
    for leaf in sorted({leaf for leaf in leaves if leaves.count(leaf) > 1}):
        problems.append(f"{leaf}: duplicate handoff manifest")
    for handoff in handoffs:
        leaf = handoff.get("owning_leaf", "<no-leaf>")
        for field in (
            "staged_placeholder",
            "replaced_by",
            "staging_refs",
            "preparation_references",
        ):
            if not handoff.get(field):
                problems.append(f"{leaf}: empty {field}")
        if handoff.get("owning_leaf") not in registered:
            problems.append(f"{leaf}: owning leaf is not a registered task")
        for ref in handoff.get("staging_refs", []):
            if ref not in sets_by_id:
                problems.append(f"{leaf}: staging ref {ref!r} has no staged input set")
        for ref in handoff.get("preparation_references", []):
            if ref not in inventory_ids and not (ROOT / ref).exists():
                problems.append(f"{leaf}: preparation reference {ref!r} does not resolve")
        for ref in sorted(
            T0051_REQUIRED_HANDOFF_STAGINGS.get(leaf, ())
            - set(handoff.get("staging_refs", []))
        ):
            problems.append(
                f"{leaf}: staged input set {ref!r} is missing from the claimed handoff"
            )
    for staged in manifest.get("staged_input_sets", []):
        sid = staged.get("staging_id", "<no-set>")
        root = roots.get(sid)
        fixture = staged.get("fixture")
        scenario = staged.get("scenario")
        if sid not in claimed:
            problems.append(f"{sid}: staged input set is not claimed by any handoff")
        if fixture:
            if not (ROOT / fixture).is_file():
                problems.append(f"{sid}: fixture does not exist")
            elif scenario and f'"{scenario}":' not in (
                ROOT / fixture
            ).read_text(encoding="utf-8"):
                problems.append(
                    f"{sid}: scenario {scenario!r} is not dispatched by its fixture"
                )
        for ref in staged.get("inventory_refs", []):
            if ref not in inventory_ids:
                problems.append(f"{sid}: inventory ref {ref!r} is not an audited identity")
        consumer = list(staged.get("consumer_visible_inputs") or [])
        if not consumer:
            problems.append(f"{sid}: no consumer-visible inputs")
        evaluator = staged.get("evaluator_only") or []
        evaluator_paths = {entry.get("path") for entry in evaluator}
        for path in consumer:
            if path in evaluator_paths:
                problems.append(
                    f"{sid}: {path} is listed as both consumer-visible and evaluator-only"
                )
            if root is not None and not (root / path).exists():
                problems.append(
                    f"{sid}: consumer-visible input {path} does not resolve in staging"
                )
        for entry in evaluator:
            if not entry.get("reason"):
                problems.append(f"{sid}: evaluator-only {entry.get('path')!r} has no reason")
            if root is not None and not (root / entry.get("path", "")).exists():
                problems.append(
                    f"{sid}: evaluator-only {entry.get('path')!r} does not resolve in staging"
                )
        positions = staged.get("not_staged_positions") or []
        declared = {position.get("path") for position in positions}
        for position in positions:
            if not position.get("filled_by"):
                problems.append(
                    f"{sid}: unstaged position {position.get('path')!r} has no producing role"
                )
            if root is not None and (root / position.get("path", "")).exists():
                problems.append(
                    f"{sid}: {position.get('path')} is staged but declared unstaged"
                )
        for path in T0051_REQUIRED_EVALUATOR_ONLY.get(sid, {}):
            if path not in evaluator_paths:
                problems.append(f"{sid}: {path} must stay evaluator-only (expected answers)")
        for entry in evaluator:
            token = T0051_REQUIRED_EVALUATOR_ONLY.get(sid, {}).get(entry.get("path"))
            if token and token not in entry.get("reason", ""):
                problems.append(
                    f"{sid}: evaluator-only reason for {entry.get('path')} must name {token!r}"
                )
        for path in T0051_REQUIRED_NOT_STAGED.get(sid, ()):
            if path not in declared:
                problems.append(
                    f"{sid}: unstaged position {path} must be declared with its producing role"
                )
    return problems


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
                    "an implementation correction, including a tests-only correction, re-enters the stages it affected before fresh discovery and acceptance",
                ),
            ),
            (
                ROOT / "skills" / "README.md",
                (
                    "names the first outstanding applicable stage and the complete ordered remainder",
                    "A conditional stage counts only with evidence current for the submitted bytes",
                    "implementation corrections, including tests-only corrections, re-enter the stages they affected before fresh discovery and acceptance",
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


class T0051QualificationInputTests(unittest.TestCase):
    """T-005.1 supplied qualification inputs: inventory/link and handoff audits.

    The audit reconciles docs/tasks/T-005.1/fixtures.md against the inherited
    T-002.4/T-003.4 composition records, the INT-FLOW-001 qualification
    inputs and current owner/fixture declarations. It rejects an inventory
    that omits an inherited case, invents an identity, keeps a stale owner
    test or fixture scenario, or points at evidence that does not resolve.
    The handoff input manifests (V-06 preparation) are staged and audited at
    the real fixture boundary: every claimed consumer-visible input, held-back
    evaluator record and unstaged producer-output position must resolve (or
    provably not exist) in a fresh disposable workspace. The wrong controls
    prove the audits identify deliberately degraded copies rather than
    accepting the remaining green rows.
    """

    def test_inventory_covers_every_inherited_identity(self):
        problems = t0051_audit_problems(
            t0051_inventory(), t0051_expected_ids()
        )
        self.assertEqual([], problems)

    def test_audit_rejects_an_omitted_mapping_and_stale_selectors(self):
        real = t0051_inventory()
        expected = t0051_expected_ids()
        degraded = json.loads(json.dumps(real))
        entries = degraded["case_inventory"]
        entries[:] = [entry for entry in entries if entry["id"] != "CCR-04"]
        for entry in entries:
            if entry["id"] == "INV-CASE-09":
                entry["scenario"] = "discovery-late-omission-superseded"
            if entry["id"] == "INV-CASE-01":
                entry["current_evidence"] = (
                    "docs/tasks/T-005.1/evidence/nonexistent-receipt.md"
                )
        problems = t0051_audit_problems(degraded, expected)
        self.assertTrue(
            any("CCR-04: missing from inventory" in problem for problem in problems),
            problems,
        )
        self.assertTrue(
            any(
                "INV-CASE-09" in problem and "scenario" in problem
                for problem in problems
            ),
            problems,
        )
        self.assertTrue(
            any("INV-CASE-01" in problem and "nonexistent-receipt" in problem
                for problem in problems),
            problems,
        )
        # the real inventory stays clean while the degraded copy fails: the
        # audit discriminates instead of accepting green-looking rows
        self.assertEqual([], t0051_audit_problems(real, expected))

    def test_unrun_role_boundaries_and_receipt_references_stay_visible(self):
        text = T0051_FIXTURES.read_text(encoding="utf-8")
        self.assertIn("never an observed role output", text)
        self.assertIn("staged records are supplied history", text.lower())
        for entry in t0051_inventory()["case_inventory"]:
            with self.subTest(case=entry["id"]):
                self.assertIn("unrun", entry["role_boundary"])
                self.assertIn(entry["owning_leaf"], entry["role_boundary"])
        for receipt in (
            "V-02-setup-reconstruction.md",
            "V-03-install-projection.md",
            "V-04-drift-contrast.md",
        ):
            self.assertTrue((T0051_EVIDENCE / receipt).is_file(), receipt)
            self.assertIn(receipt, text)

    def test_handoff_manifests_resolve_exact_consumer_visible_inputs(self):
        manifests = t0051_manifests()
        roots = {}
        for staged in manifests["staged_input_sets"]:
            if staged.get("fixture"):
                roots[staged["staging_id"]] = stage_setup(
                    self, ROOT / staged["fixture"], staged["scenario"]
                )
            else:
                roots[staged["staging_id"]] = ROOT
        self.assertEqual([], t0051_manifest_problems(manifests, roots))

        # Directory inputs expose Git objects as well as worktree paths.
        # Inspect every object, including index-only and unreachable blobs.
        for staged in manifests["staged_input_sets"]:
            root = roots[staged["staging_id"]]
            for held_back in staged["evaluator_only"]:
                answer = (root / held_back["path"]).read_bytes()
                for visible in staged["consumer_visible_inputs"]:
                    consumer = root / visible
                    if not consumer.is_dir():
                        self.assertNotEqual(answer, consumer.read_bytes())
                        continue
                    for path in consumer.rglob("*"):
                        if path.is_file() and ".git" not in path.relative_to(consumer).parts:
                            self.assertNotEqual(answer, path.read_bytes(), str(path))
                    if not (consumer / ".git").exists():
                        continue
                    objects = subprocess.run(
                        ["git", "cat-file", "--batch-all-objects",
                         "--batch-check=%(objectname) %(objecttype)"],
                        cwd=consumer, check=True, capture_output=True, text=True,
                        timeout=10,
                    ).stdout.splitlines()
                    for obj in objects:
                        oid, kind = obj.split()
                        if kind == "blob":
                            blob = subprocess.run(
                                ["git", "cat-file", "blob", oid], cwd=consumer,
                                check=True, capture_output=True, timeout=10,
                            ).stdout
                            self.assertNotEqual(answer, blob, (staged["staging_id"], oid))

    def test_route_consumer_excludes_answers_and_preserves_review_context(self):
        staged = next(s for s in t0051_manifests()["staged_input_sets"]
                      if s["staging_id"] == "route-cases")
        work = stage_setup(self, ROOT / staged["fixture"], staged["scenario"])
        original = work / "route-cases"
        consumer = work / staged["consumer_visible_inputs"][0]
        key = "change-effects/cases.json"
        answer = (original / key).read_bytes()
        # Reviewer reproducer remains a wrong control against raw staging.
        (original / key).unlink()
        for ref in ("HEAD:" + key, ":" + key):
            raw = subprocess.run(["git", "show", ref], cwd=original,
                                 capture_output=True, timeout=10)
            self.assertEqual(0, raw.returncode)
            self.assertEqual(answer, raw.stdout)
            safe = subprocess.run(["git", "show", ref], cwd=consumer,
                                  capture_output=True, timeout=10)
            self.assertNotEqual(0, safe.returncode)
        self.assertFalse((consumer / key).exists())
        for tree in (original, consumer):
            files = {p.relative_to(tree): p.read_bytes() for p in tree.rglob("*")
                     if p.is_file() and ".git" not in p.relative_to(tree).parts}
            if tree == original:
                expected = files
            else:
                self.assertEqual(expected, files)
        status = subprocess.run(["git", "status", "--porcelain"], cwd=consumer,
                                check=True, capture_output=True, timeout=10)
        self.assertEqual(b"", status.stdout)

    def test_manifest_audit_rejects_degraded_handoff_manifests(self):
        real = t0051_manifests()
        degraded = json.loads(json.dumps(real))
        handoffs = degraded["handoff_manifests"]
        handoffs[:] = [item for item in handoffs if item["owning_leaf"] != "T-005.4"]
        for handoff in handoffs:
            if handoff["owning_leaf"] == "T-005.3":
                handoff["staging_refs"].append("undeclared-staging")
            if handoff["owning_leaf"] == "T-005.5":
                handoff["preparation_references"].append("FIND-99")
        for staged in degraded["staged_input_sets"]:
            if staged["staging_id"] == "queue-defect":
                staged["consumer_visible_inputs"].append(
                    "queue-runner/docs/tasks/QR-12/nonexistent-input.md"
                )
            if staged["staging_id"] == "correction-round":
                staged["evaluator_only"] = []
            if staged["staging_id"] == "integration-leaf":
                staged["scenario"] = "integration-leaf-superseded"
        roots = {
            "queue-defect": stage_setup(
                self,
                ROOT
                / "skills"
                / "task-implementation-flow"
                / "task-review-discovery"
                / "evals"
                / "files"
                / "setup_fixture.py",
                "queue-defect",
            )
        }
        problems = t0051_manifest_problems(degraded, roots)
        self.assertTrue(
            any("T-005.4: missing handoff manifest" in problem for problem in problems),
            problems,
        )
        self.assertTrue(
            any("undeclared-staging" in problem for problem in problems), problems
        )
        self.assertTrue(
            any("FIND-99" in problem for problem in problems), problems
        )
        self.assertTrue(
            any(
                "queue-defect" in problem and "nonexistent-input" in problem
                for problem in problems
            ),
            problems,
        )
        self.assertTrue(
            any(
                "correction-round" in problem and "must stay evaluator-only" in problem
                for problem in problems
            ),
            problems,
        )
        self.assertTrue(
            any(
                "integration-leaf" in problem and "superseded" in problem
                for problem in problems
            ),
            problems,
        )
        self.assertTrue(
            any(
                "known-issue-consumption-decision" in problem
                and "not claimed by any handoff" in problem
                for problem in problems
            ),
            problems,
        )
        # the real manifests stay clean under the same oracle and the same
        # staged queue-defect root: the audit discriminates instead of
        # accepting green-looking manifests. Full-resolution proof for every
        # staged set is owned by the resolving test above.
        self.assertEqual([], t0051_manifest_problems(real, roots))


if __name__ == "__main__":
    unittest.main()
