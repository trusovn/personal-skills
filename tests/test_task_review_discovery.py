"""Discovery contract, inherited eval parity, and late-omission validator probes.

Fail-first checks over the discovery skill and report template, byte-level
inheritance verification between the acceptance and discovery fixtures, and
public-entry validator probes for both late-omission recovery fixtures.
"""

import ast
import json
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from review_fixture_support import (
    ACCEPTANCE_EVALS,
    ACCEPTANCE_FIXTURE,
    ACCEPTANCE_VERDICT_TOKENS,
    CONTEXTUAL_CONTRAST_SETUPS,
    DISCOVERY_EVALS,
    DISCOVERY_FIXTURE,
    DISCOVERY_REPORT_TEMPLATE,
    DISCOVERY_SKILL,
    fixture_functions,
    normalized,
)


PRESERVED_DISCOVERY_EVAL_IDS = (1, 2, 3, 4, 5, 6, 7, 8, 9)



NEW_DISCOVERY_EVAL_IDS = (11, 12, 13, 14, 15)



ACCEPTANCE_ONLY_SCENARIOS = frozenset(
    {
        "queue-defect-reproducer",
        "queue-defect-decision",
        "queue-defect-reproducer-decision",
        "exporter-accept-decision",
        "scheduler-inconclusive-decision",
        "exporter-restaged-stale-decision",
        "ledger-defects-decision",
        "workflow-matrix-defects-decision",
        "process-cleanup-defects-decision",
        "contextual-risk-blockers-decision",
        "contextual-risk-mitigated-decision",
        "mixed-conditions-authorized-decision",
        "mixed-conditions-forbidden-decision",
        "consequential-uncertainty-decision",
        "known-issue-consumption-decision",
        "correction-regression-decision",
    }
)



ACCEPTANCE_ONLY_SCENARIOS |= CONTEXTUAL_CONTRAST_SETUPS.keys()



ACCEPTANCE_ONLY_FIXTURE_FUNCTIONS = frozenset(
    {
        "discovery_report",
        "queue_defect_reproducer",
        "queue_defect_decision",
        "queue_defect_reproducer_decision",
        "exporter_accept_decision",
        "scheduler_inconclusive_decision",
        "exporter_restaged_stale_decision",
        "ledger_defects_decision",
        "workflow_matrix_defects_decision",
        "process_cleanup_defects_decision",
        "contextual_risk_blockers",
        "contextual_risk_blockers_decision",
        "contextual_risk_mitigated",
        "contextual_risk_mitigated_decision",
        "mixed_conditions",
        "mixed_conditions_authorized",
        "mixed_conditions_authorized_decision",
        "mixed_conditions_forbidden",
        "mixed_conditions_forbidden_decision",
        "consequential_uncertainty",
        "consequential_uncertainty_decision",
        "known_issue_consumption",
        "known_issue_consumption_decision",
        "correction_regression",
        "correction_regression_decision",
        "uncertainty_contrast",
        "known_issue_context",
        "repeated_review",
    }
)



NEW_DISCOVERY_SCENARIOS = (
    "discovery-prepared-ledger",
    "discovery-correction-gate",
    "discovery-late-omission-clean",
    "discovery-late-omission-fail",
    "discovery-diagnostic-aggregate",
)



NEW_DISCOVERY_FIXTURE_FUNCTIONS = (
    "discovery_correction_gate",
    "discovery_diagnostic_aggregate",
    "discovery_late_omission",
    "discovery_prepared_ledger",
)



DISCOVERY_ROLE_TOKEN_MAP = (
    ("task-acceptance-review", "task-review-discovery"),
    ("acceptance-01", "discovery-01"),
    ("Acceptance", "Discovery"),
    ("acceptance", "discovery"),
)



_QUEUE_AUTHORIZATION_BLOCK = re.compile(
    r'    test_path = "tests/integration/test_run_next\.py" if authorize_reproducer else None\n'
    r"    run_policy = policy\(test_path\)\n"
    r"    if authorize_reproducer:\n"
    r".*?"
    r"    else:\n"
    r"        fixture_rule = ",
    re.DOTALL,
)



ACCEPTANCE_FIXTURE_ADAPTATIONS = (
    (
        '"""Create staged implementations and review artifacts for discovery evals."""',
        '"""Create staged implementations and review artifacts for task-review-discovery evals."""',
    ),
    (
        "def policy(authorized_test_path: str | None = None) -> Path:",
        "def policy() -> Path:",
    ),
    (
        '    if authorized_test_path is not None:\n'
        '        allow.append(f"post-verdict tests_only_reproducer write to {authorized_test_path}")\n'
        '        deny[0] = "source edits and test edits outside the explicitly authorized path"\n',
        "",
    ),
    (
        "def queue_defect(*, authorize_reproducer: bool = False) -> None:",
        "def queue_defect() -> None:",
    ),
    ('"""Review continuation:', '"""Discovery continuation:'),
    (
        "prior review; bytes have since changed",
        "prior discovery; bytes have since changed",
    ),
    ("- Finding IDs: WF-F1\n", "- Finding IDs: WF-F1 (suggested P1)\n"),
    (
        "- Broad gate: not run after targeted failure",
        "- Aggregate gate: not run after targeted failure; owner: fresh correction discovery",
    ),
    (
        "- Next: continue independent review of the current bytes",
        "- Next: continue independent discovery of the current bytes",
    ),
    (
        "def queue_defect_reproducer() -> None:\n    queue_defect(authorize_reproducer=True)\n\n\n",
        "",
    ),
    ('    "queue-defect-reproducer": queue_defect_reproducer,\n', ""),
)



def adapt_acceptance_fixture_text(text: str) -> str:
    """Apply the authorized discovery role adaptation to acceptance fixture text.

    After this adaptation, every scenario function shared with the discovery
    fixture must be byte-identical: inherited starting states, invocations,
    signals, and cleanup survive unchanged, and only role-specific authority
    and handoff metadata differ.
    """
    for old, new in DISCOVERY_ROLE_TOKEN_MAP:
        text = text.replace(old, new)
    for old, new in ACCEPTANCE_FIXTURE_ADAPTATIONS:
        if old not in text:
            raise AssertionError(
                f"acceptance fixture no longer contains the expected fragment: {old[:60]!r}"
            )
        text = text.replace(old, new)
    text, replacements = _QUEUE_AUTHORIZATION_BLOCK.subn(
        "    run_policy = policy()\n    fixture_rule = ", text
    )
    if replacements != 1:
        raise AssertionError(f"expected one authorization block, found {replacements}")
    return text



def fixture_scenarios(text: str) -> set:
    tree = ast.parse(text)
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "SCENARIOS"
            for target in node.targets
        ):
            return {key.value for key in node.value.keys}
    raise AssertionError("SCENARIOS assignment not found in fixture")



class ReviewDiscoveryDisciplineTests(unittest.TestCase):

    def test_discovery_forbids_acceptance_verdicts_deferrals_and_advancement(self):
        text = normalized(DISCOVERY_SKILL)

        self.assertIn("Discovery has no decision authority", text)
        self.assertIn(
            "never issues or implies an acceptance verdict such as `ACCEPT`, `CHANGES_REQUESTED`, or `INCONCLUSIVE`",
            text,
        )
        self.assertIn("never records an approved deferral", text)
        self.assertIn("never advances work", text)


    def test_author_session_stays_self_check_only_and_routes_to_fresh_discovery(self):
        text = normalized(DISCOVERY_SKILL)

        self.assertIn("SELF_CHECK_ONLY", text)
        self.assertIn("Loading this skill does not reset authorship", text)
        self.assertIn("The route is always a fresh discovery call", text)
        self.assertIn(
            "must not present its rows as independently corroborated evidence", text
        )


    def test_ledger_rows_keep_states_reasons_setup_and_exact_probes(self):
        text = normalized(DISCOVERY_SKILL)

        self.assertIn(
            "pass | fail | blocked | unchecked, with reason", text
        )
        self.assertIn("setup/oracle", text)
        self.assertIn(
            "the exact probe command or the concrete reason it was not run", text
        )
        self.assertIn("Every material row named by the authority appears in the ledger", text)
        self.assertIn("cannot vanish behind green tests", text)
        self.assertIn(
            "the supplied task context (verification design, recorded ART-003 context, finite-risk matrix) selects bounded decisive material-risk probes",
            text,
        )


    def test_scope_reconstruction_detects_changed_index_blob_independently(self):
        text = normalized(DISCOVERY_SKILL)

        self.assertIn(
            "matching worktree bytes and short-status text do not prove a matching index blob",
            text,
        )
        self.assertIn(
            "publish unexplained or inseparable overlap as an explicit scope gap", text
        )
        self.assertIn(
            "never reset, restage, overwrite, or claim ownership of user state", text
        )


    def test_findings_carry_invariant_fields_and_suggested_severity(self):
        text = normalized(DISCOVERY_SKILL)

        self.assertIn("stable ID such as `F-01`", text)
        self.assertIn("suggested severity", text)
        self.assertIn("credible contract-implied sibling surface", text)
        self.assertIn("smallest invariant-level corrective direction", text)
        self.assertIn("Never leave the sibling surface implicit", text)
        self.assertIn(
            "Keep unproved questions, residual risks, and unchecked ledger rows separate from confirmed findings",
            text,
        )


    def test_discovery_preserves_lifecycle_validator_and_process_obligations(self):
        text = normalized(DISCOVERY_SKILL)

        self.assertIn(
            "independently execute the first occurrence, observe or apply its legitimate state change, then execute the next real occurrence",
            text,
        )
        self.assertIn(
            "at least one instance that should be valid and one deliberately invalid instance",
            text,
        )
        self.assertIn("targets the changed or acceptance-relevant constraint", text)
        self.assertIn("schema's declared draft", text)
        self.assertIn("Draft 2020-12", text)
        self.assertIn(
            "Continue after a finding while remaining probes are independent, safe, authorized, and affordable",
            text,
        )
        self.assertIn("observable synchronization and bounded waits", text)
        self.assertIn(
            "descendant and process-group disappearance plus inherited-pipe release", text
        )
        self.assertIn("no fixture process survives discovery", text)


    def test_gate_reconciliation_suppression_and_correction_ownership(self):
        text = normalized(DISCOVERY_SKILL)

        self.assertIn(
            "reconcile the frozen ledger against the task contract and scoped diff", text
        )
        self.assertIn(
            "do not run the broad/aggregate gate merely for completeness", text
        )
        self.assertIn("distinct authorized diagnostic purpose", text)
        self.assertIn(
            "owns one justified aggregate after clean targeted evidence", text
        )
        self.assertIn("reruns reviewer regressions", text)
        self.assertIn("record the earlier aggregate gate as premature", text)
        self.assertIn(
            "the exact command or `not run`, owner, stage, reason, and current evidence",
            text,
        )
        self.assertIn("Add no gate and add no command", text)
        self.assertIn("Required conditional gate owners retain their duties", text)
        template = normalized(DISCOVERY_REPORT_TEMPLATE)
        self.assertIn("Current evidence", template)
        self.assertIn("targeted recovery before any justified rerun", template)
        self.assertIn("separate correction/evidence/authority", template)


    def test_write_rules_allow_only_the_next_unused_discovery_report(self):
        text = normalized(DISCOVERY_SKILL)

        self.assertIn("next unused numbered discovery path", text)
        self.assertIn("reviews/discovery-NN.md", text)
        self.assertIn("Never overwrite an earlier report", text)
        self.assertIn(
            "Do not implement fixes, edit reviewed production files or tests, update task briefs/plans/trackers or prior reports",
            text,
        )
        self.assertIn("never claims its own authenticity", text)


    def test_final_handoff_carries_packaged_preparation_references(self):
        """INT-FLOW-001 I-04: complete clean guided reports still hand off
        the applicable verification/readiness/context references; unpackaged
        direct requests stay compact.
        """
        text = normalized(DISCOVERY_SKILL)
        self.assertIn(
            "Give the acceptance decision call the task brief, current "
            "scoped diff, this report, every blocked or unchecked row, "
            "reviewer regression paths/commands, and the applicable packaged "
            "preparation references",
            text,
        )
        self.assertIn(
            "the verification design with its revision, the "
            "readiness/preflight reference, and the recorded decision context",
            text,
        )
        self.assertIn(
            "for complete, clean guided reports as well as explicitly partial "
            "ones",
            text,
        )
        self.assertIn(
            "An unpackaged direct edit hands off the supplied conversational "
            "context instead",
            text,
        )
        template = normalized(DISCOVERY_REPORT_TEMPLATE)
        self.assertIn(
            "Complete clean evidence routes to the separate acceptance "
            "decision call with the applicable packaged preparation references",
            template,
        )


    def test_discovery_evals_preserve_inherited_setups_and_exercise_discovery_cases(self):
        discovery = json.loads(DISCOVERY_EVALS.read_text(encoding="utf-8"))
        acceptance = json.loads(ACCEPTANCE_EVALS.read_text(encoding="utf-8"))
        by_id = {item["id"]: item for item in acceptance["evals"]}
        discovery_text = DISCOVERY_FIXTURE.read_text(encoding="utf-8")

        self.assertEqual(
            list(PRESERVED_DISCOVERY_EVAL_IDS) + list(NEW_DISCOVERY_EVAL_IDS),
            [item["id"] for item in discovery["evals"]],
        )
        eval_scenarios = set()
        for item in discovery["evals"]:
            command = item["execution"]["setup"]["command"]
            self.assertEqual(["python3", "evals/files/setup_fixture.py"], command[:2])
            self.assertEqual(
                {"EVAL_WORK_ROOT": "{run_root}/work"}, item["execution"]["setup"]["env"]
            )
            self.assertTrue(item["execution"]["workspace"].startswith("{run_root}/work/"))
            eval_scenarios.add(command[2])
            if item["id"] in PRESERVED_DISCOVERY_EVAL_IDS:
                source = by_id[item["id"]]
                self.assertEqual(source["files"], item["files"])
                source_command = source["execution"]["setup"]["command"]
                self.assertEqual(["python3", "evals/files/setup_fixture.py"], source_command[:2])
                self.assertIn(
                    source_command[2],
                    {command[2], command[2] + "-decision"},
                    f"acceptance eval {item['id']} scenario must stay the inherited scenario or its -decision wrapper",
                )
                self.assertEqual(
                    source["execution"]["setup"]["env"], item["execution"]["setup"]["env"]
                )
                self.assertEqual(
                    source["execution"]["workspace"], item["execution"]["workspace"]
                )
            else:
                self.assertEqual(["evals/files/setup_fixture.py"], item["files"])
        self.assertEqual(fixture_scenarios(discovery_text), eval_scenarios)

        blob = json.dumps(discovery)
        self.assertIn("`runner run-next` public entry point twice", blob)
        self.assertIn("`exportctl resume`", blob)
        self.assertIn("`WF-TAMPER`", blob)
        self.assertIn("`WF-REPLAY`", blob)
        self.assertIn("`WF-DECISION`", blob)
        self.assertIn("`PROC-RESIST`", blob)
        self.assertIn("`PROC-PIPE`", blob)
        self.assertIn("`PROC-RACE`", blob)
        self.assertIn("`MIX-R1`", blob)
        self.assertIn("`MIX-R4`", blob)
        self.assertIn("AC-04", blob)
        self.assertIn("ART-003", blob)
        self.assertIn("`SELF_CHECK_ONLY`", blob)
        self.assertIn("premature", blob)
        self.assertIn("diagnostic", blob)
        self.assertIn("discovery-02.md", blob)


    def test_discovery_fixture_adapts_role_metadata_and_preserves_inherited_scenarios(self):
        acceptance_text = ACCEPTANCE_FIXTURE.read_text(encoding="utf-8")
        discovery_text = DISCOVERY_FIXTURE.read_text(encoding="utf-8")

        for token in (
            "acceptance-01",
            "task-acceptance-review",
            "Acceptance",
            "tests_only_reproducer",
            "authorize_reproducer",
            "authorized_test_path",
            "queue-defect-reproducer",
            "Broad gate",
        ):
            self.assertNotIn(token, discovery_text, token)
        self.assertNotIn(
            "acceptance", discovery_text.replace("acceptance decision call", "")
        )

        self.assertEqual(
            (fixture_scenarios(acceptance_text) - ACCEPTANCE_ONLY_SCENARIOS)
            | set(NEW_DISCOVERY_SCENARIOS),
            fixture_scenarios(discovery_text),
        )

        acceptance_functions = fixture_functions(acceptance_text)
        discovery_functions = fixture_functions(discovery_text)
        adapted_functions = fixture_functions(adapt_acceptance_fixture_text(acceptance_text))
        self.assertEqual(
            ACCEPTANCE_ONLY_FIXTURE_FUNCTIONS,
            set(acceptance_functions) - set(discovery_functions),
        )
        self.assertEqual(
            set(NEW_DISCOVERY_FIXTURE_FUNCTIONS),
            set(discovery_functions) - set(acceptance_functions),
        )
        for name in sorted(set(adapted_functions) & set(discovery_functions)):
            self.assertEqual(
                adapted_functions[name],
                discovery_functions[name],
                f"inherited scenario function changed beyond role adaptation: {name}",
            )


    def test_discovery_evals_never_demand_an_acceptance_verdict(self):
        discovery = json.loads(DISCOVERY_EVALS.read_text(encoding="utf-8"))

        for item in discovery["evals"]:
            blob = json.dumps(item)
            for token in ACCEPTANCE_VERDICT_TOKENS:
                self.assertNotIn(token, blob, f"eval {item['id']} demands a verdict")
            self.assertIn("verdict", item["expected_output"].lower())
            self.assertTrue(
                "complete" in item["expected_output"]
                or "partial" in item["expected_output"],
                f"eval {item['id']} omits coverage completeness",
            )
        self.assertIn("acceptance decision call", json.dumps(discovery))


    def test_discovery_report_template_omits_verdicts_and_keeps_ledger_fields(self):
        text = normalized(DISCOVERY_REPORT_TEMPLATE)

        self.assertNotIn("| Verdict |", text)
        self.assertNotIn("ACCEPT | CHANGES_REQUESTED | INCONCLUSIVE", text)
        self.assertIn("It contains no acceptance verdict", text)
        self.assertIn("Coverage completeness", text)
        self.assertIn("partial — <concrete reasons>", text)
        self.assertIn("Suggested severity", text)
        self.assertIn("Setup / oracle", text)
        self.assertIn(
            "the exact command or `not run`, the capability, permission, or environment blocker, and the next evidence owner",
            text,
        )
        self.assertIn("that earlier gate is recorded as premature", text)
        self.assertIn("This report does not review or authenticate itself.", text)
        self.assertIn("Discovery continuation:", text)
        self.assertIn("SELF_CHECK_ONLY", text)


    def test_guided_continuation_requires_scenario_history_and_separate_owners(self):
        text = DISCOVERY_SKILL.read_text(encoding="utf-8")
        start = text.index("Discovery continuation:")
        end = text.index("```", start)
        block = text[start:end]

        self.assertIn("Finding/scenario continuity", block)
        self.assertIn(
            "prior statuses, current producer-attributed evidence, incomplete reasons and separate correction/evidence/authority owners",
            block,
        )
        self.assertIn("influenced sibling surfaces", block)
        self.assertIn("Preparation/context", block)
        self.assertIn("brief, verification revision, preflight and context references", block)



class DiscoveryLateOmissionFixtureTests(unittest.TestCase):
    """Public-entry probes for both late-omission recovery fixtures.

    LED-05 AC-03 requires a running ledger to keep exactly one running
    selected task with its latest active attempt. Both fixtures share the
    generated validator, so the clean recovery case must satisfy every
    material validator row before its aggregate rerun, while the fail
    variant shares these checks and keeps only its intended
    boolean-revision defect.
    """

    def probe_public_entry(self, scenario: str) -> dict:
        with TemporaryDirectory() as tmp:
            work = Path(tmp)
            env = dict(os.environ, EVAL_WORK_ROOT=str(work))
            subprocess.run(
                [sys.executable, str(DISCOVERY_FIXTURE), scenario],
                check=True,
                env=env,
                capture_output=True,
            )
            workspace = work / "late-omission"
            valid = json.loads((workspace / "cases" / "valid.json").read_text())
            second_running = json.loads(json.dumps(valid))
            second_running["tasks"][1]["status"] = "running"
            cases = {
                "valid": valid,
                "boolean": dict(valid, revision=True),
                "older-attempt": dict(valid, active_attempt_id="A-1"),
                "second-running": second_running,
            }
            exits = {}
            for name, data in cases.items():
                case_path = work / f"{name}.json"
                case_path.write_text(json.dumps(data))
                run = subprocess.run(
                    [sys.executable, "-m", "src.ledger.validate", str(case_path)],
                    cwd=workspace,
                    capture_output=True,
                )
                exits[name] = run.returncode
            return exits

    def test_correction_and_diagnostic_fixtures_supply_clean_and_failed_targeted_proof(self):
        for scenario, folder, expected_claims in (
            ("discovery-correction-gate", "corrected-queue", ["TASK-1", "TASK-2"]),
            ("discovery-diagnostic-aggregate", "queue-runner", ["TASK-1", ""]),
        ):
            with self.subTest(scenario=scenario), TemporaryDirectory() as temporary:
                subprocess.run([sys.executable, str(DISCOVERY_FIXTURE), scenario],
                               env=os.environ | {"EVAL_WORK_ROOT": temporary}, check=True)
                root = Path(temporary) / folder
                state = root / "probe.json"
                state.write_text(json.dumps({"tasks": [{"id": f"TASK-{i}", "status": "ready"} for i in (1, 2)]}))
                command = [sys.executable, "-m", "src.queue.run_next", str(state)]
                claims = [subprocess.check_output(command, cwd=root, text=True).strip() for _ in range(2)]
                self.assertEqual(expected_claims, claims)
                if scenario == "discovery-diagnostic-aggregate":
                    self.assertTrue((Path(temporary) / "task-runs/QR-12/diagnostic-authorization.md").exists())


    def test_clean_recovery_fixture_satisfies_every_material_validator_row(self):
        exits = self.probe_public_entry("discovery-late-omission-clean")

        self.assertEqual(
            {"valid": 0, "boolean": 2, "older-attempt": 2, "second-running": 2},
            exits,
        )


    def test_fail_recovery_fixture_keeps_only_the_boolean_revision_defect(self):
        exits = self.probe_public_entry("discovery-late-omission-fail")

        self.assertEqual(
            {"valid": 0, "boolean": 0, "older-attempt": 2, "second-running": 2},
            exits,
        )



if __name__ == "__main__":
    unittest.main()
