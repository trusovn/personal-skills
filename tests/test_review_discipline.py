import ast
import json
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[1]
ACCEPTANCE_SKILL = (
    ROOT
    / "skills"
    / "task-implementation-flow"
    / "task-acceptance-review"
    / "SKILL.md"
)
ACCEPTANCE_PACKAGE = ROOT / "skills" / "task-implementation-flow" / "task-acceptance-review"
DISCOVERY_PACKAGE = ROOT / "skills" / "task-implementation-flow" / "task-review-discovery"
DISCOVERY_SKILL = DISCOVERY_PACKAGE / "SKILL.md"
DISCOVERY_REPORT_TEMPLATE = (
    DISCOVERY_PACKAGE / "references" / "discovery-report-template.md"
)
ACCEPTANCE_EVALS = ACCEPTANCE_PACKAGE / "evals" / "evals.json"
DISCOVERY_EVALS = DISCOVERY_PACKAGE / "evals" / "evals.json"
DISCOVERY_FIXTURE = DISCOVERY_PACKAGE / "evals" / "files" / "setup_fixture.py"
ACCEPTANCE_FIXTURE = ACCEPTANCE_PACKAGE / "evals" / "files" / "setup_fixture.py"
PRESERVED_DISCOVERY_EVAL_IDS = (1, 2, 3, 4, 5, 6, 7, 8, 9)
NEW_DISCOVERY_EVAL_IDS = (11, 12, 13, 14, 15)
CONTEXTUAL_CONTRAST_SETUPS = {
    "consequential-uncertainty-resolved-decision": "uncertainty_contrast",
    "serious-delay-uncertainty-decision": "uncertainty_contrast",
    "serious-delay-uncertainty-resolved-decision": "uncertainty_contrast",
    "known-issue-proposed-work-decision": "known_issue_context",
    "known-issue-committed-work-decision": "known_issue_context",
    "known-issue-priority-only-decision": "known_issue_context",
    "known-issue-no-links-decision": "known_issue_context",
    "repeated-review-formerly-blocked-evidence-decision": "repeated_review",
    "repeated-review-missed-existing-obligation-decision": "repeated_review",
    "repeated-review-changed-context-authority-decision": "repeated_review",
    "repeated-review-newly-demonstrated-material-risk-decision": "repeated_review",
}
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
# The discovery fixture must preserve every inherited scenario byte-for-byte
# except these documented role-specific authority/handoff adaptations.
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
ACCEPTANCE_VERDICT_TOKENS = ("`ACCEPT`", "`CHANGES_REQUESTED`", "`INCONCLUSIVE`")
SENIOR_REVIEW_SKILL = ROOT / "skills" / "senior-code-review" / "SKILL.md"

ROOT_README = ROOT / "README.md"
PROFILE_GUIDE = ROOT / "skills" / "README.md"
FLOW_README = ROOT / "skills" / "task-implementation-flow" / "README.md"
BOUNDED_IMPLEMENTER_SKILL = (
    ROOT / "skills" / "task-implementation-flow" / "bounded-task-implementer" / "SKILL.md"
)
MAINTAINABILITY_SKILL = (
    ROOT / "skills" / "task-implementation-flow" / "task-maintainability-review" / "SKILL.md"
)
REGISTRY_UPDATER_SKILL = (
    ROOT / "skills" / "task-implementation-flow" / "task-contract-registry-updater" / "SKILL.md"
)
PREFLIGHT_EVALS = (
    ROOT / "skills" / "task-implementation-flow" / "task-preflight" / "evals" / "evals.json"
)
DESIGNER_SKILL = (
    ROOT / "skills" / "task-implementation-flow" / "task-brief-designer" / "SKILL.md"
)
DESIGNER_TEMPLATE = (
    ROOT
    / "skills"
    / "task-implementation-flow"
    / "task-brief-designer"
    / "references"
    / "task-brief-template.md"
)
IMPLEMENTER_PACKAGE = (
    ROOT / "skills" / "task-implementation-flow" / "bounded-task-implementer"
)
IMPLEMENTER_EVALS = IMPLEMENTER_PACKAGE / "evals" / "evals.json"
IMPLEMENTER_FIXTURE = (
    IMPLEMENTER_PACKAGE / "evals" / "files" / "setup_fixture.py"
)
TASK_MAP = ROOT / "docs" / "task-map.json"
COMPOSITION_PATH = ROOT / "docs" / "tasks" / "T-002.4" / "composition.json"


def fenced_blocks(text: str) -> list:
    blocks: list = []
    current: list | None = None
    for line in text.splitlines():
        if current is None:
            if line.lstrip().startswith("```"):
                current = []
        elif line.lstrip().startswith("```"):
            blocks.append("\n".join(current))
            current = None
        else:
            current.append(line)
    return blocks


def normalized(path: Path) -> str:
    return re.sub(r"\s+", " ", path.read_text(encoding="utf-8")).strip()


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


def fixture_functions(text: str) -> dict:
    tree = ast.parse(text)
    return {
        node.name: ast.get_source_segment(text, node)
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
    }


def fixture_scenarios(text: str) -> set:
    tree = ast.parse(text)
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "SCENARIOS"
            for target in node.targets
        ):
            return {key.value for key in node.value.keys}
    raise AssertionError("SCENARIOS assignment not found in fixture")


class ReviewerDisciplineTests(unittest.TestCase):
    def test_acceptance_admits_discovery_evidence_and_routes_missing_discovery(self):
        text = normalized(ACCEPTANCE_SKILL)

        self.assertIn("Admit the discovery evidence", text)
        self.assertIn("acceptance does not merge the roles", text)
        self.assertIn(
            "request the missing evidence from the discovery owner with the exact gap", text
        )
        self.assertIn("guided evidence gap", text)
        self.assertIn(
            "does not trigger an orchestrator-packet requirement", text
        )
        self.assertIn(
            "Packaging alone does not require high-assurance digests or machine results", text
        )
        self.assertIn("Do not return `INCONCLUSIVE` merely because no preflight packet", text)

    def test_acceptance_reconciles_rows_against_current_bytes(self):
        text = normalized(ACCEPTANCE_SKILL)

        self.assertIn(
            "stays `blocked` or `unchecked` with its exact missing proof and owner", text
        )
        self.assertIn("despite green tests, static schema checks, or producer self-validation", text)
        self.assertIn(
            "Summaries, old passes, report self-claims, and green tests do not substitute for decisive evidence",
            text,
        )
        self.assertIn(
            "matching worktree bytes or short-status text do not prove a matching index blob", text
        )
        self.assertIn(
            "an old pass does not prove changed bytes", text
        )
        self.assertIn(
            "Explicit AC violations block even when submitted tests are green", text
        )
        self.assertIn(
            "does not become a second general maintainability reviewer", text
        )

    def test_acceptance_requires_admitted_validator_evidence(self):
        text = normalized(ACCEPTANCE_SKILL)

        self.assertIn(
            "admitted discovery evidence must include independent validator results", text
        )
        self.assertIn("at least one instance that should be valid", text)
        self.assertIn("one deliberately invalid instance", text)
        self.assertIn("targets the changed or acceptance-relevant constraint", text)
        self.assertIn("schema text", text)
        self.assertIn("producer-side validation", text)
        self.assertIn("deserialization", text)
        self.assertIn("unrelated passing suite", text)

    def test_unexercised_required_schema_boundary_cannot_support_accept(self):
        text = normalized(ACCEPTANCE_SKILL)

        self.assertIn(
            "keep that ledger row `blocked` or `unchecked` with the concrete reason; it cannot support `ACCEPT`",
            text,
        )
        self.assertIn(
            "otherwise its row remains blocked/unchecked and cannot support `ACCEPT`",
            text,
        )

    def test_acceptance_consumes_aggregate_gate_without_reexecution(self):
        text = normalized(ACCEPTANCE_SKILL)

        self.assertIn("Consume the discovery-owned aggregate-gate record without executing it", text)
        self.assertIn(
            "exact command or `not run`, owner/stage, reason, and current evidence", text
        )
        self.assertIn(
            "Suppression after a decisive targeted failure is retained", text
        )
        self.assertIn(
            "a copied pre-correction pass cannot replace a clean corrected discovery record", text
        )
        self.assertIn("a premature gate does not clear an omitted row", text)
        self.assertIn("only discovery owns a still-justified rerun", text)
        self.assertIn("Acceptance adds no gate and adds no command", text)
        self.assertIn("does not routinely rerun public probes, broad searches, or suites", text)

    def test_acceptance_preserves_verdict_vocabulary_and_provenance(self):
        text = normalized(ACCEPTANCE_SKILL)

        self.assertIn("exactly `ACCEPT`, `CHANGES_REQUESTED`, or `INCONCLUSIVE`", text)
        self.assertIn("`SELF_CHECK_ONLY` is a non-verdict", text)
        self.assertIn("Loading this skill does not reset authorship", text)
        self.assertIn("The route is always a fresh reviewer", text)
        self.assertIn("Missing discovery routes to the discovery owner with the exact gap", text)
        self.assertIn(
            "missing or contradictory discovery evidence", text
        )

    def test_acceptance_preserves_tests_only_exception_and_numbered_reports(self):
        text = normalized(ACCEPTANCE_SKILL)

        self.assertIn("`tests_only_reproducer`", text)
        self.assertIn("names the exact writable owning test file", text)
        self.assertIn(
            "Task scope, an allowed test path, or `review: immediate` is not write permission",
            text,
        )
        self.assertIn("next unused numbered acceptance path", text)
        self.assertIn("Never overwrite an earlier review", text)
        self.assertIn(
            "Even `ACCEPT` records a decision/route without authorizing tracker mutation",
            text,
        )

    def test_senior_review_reference_read_is_an_early_mandatory_prerequisite(self):
        text = normalized(SENIOR_REVIEW_SKILL)

        self.assertIn(
            "Before substantive review reasoning, candidate-finding generation, or dimension selection",
            text,
        )
        self.assertIn("read [references/review-dimensions.md](references/review-dimensions.md)", text)
        self.assertIn("mandatory prerequisite for every invocation", text)

    def test_senior_review_completion_check_reasserts_reference_read(self):
        text = normalized(SENIOR_REVIEW_SKILL)

        self.assertIn("## Completion check", text)
        self.assertIn(
            "`references/review-dimensions.md` was read in this invocation before substantive review reasoning",
            text,
        )
        self.assertIn("every dimension relevant to the scoped change was considered", text)


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


class AcceptanceAdmissionEvalTests(unittest.TestCase):
    """Decision evals consume staged discovery evidence instead of re-probing."""

    def test_decision_evals_consume_discovery_reports_without_reexecution(self):
        acceptance = json.loads(ACCEPTANCE_EVALS.read_text(encoding="utf-8"))
        functions = fixture_functions(ACCEPTANCE_FIXTURE.read_text(encoding="utf-8"))

        for item in acceptance["evals"]:
            blob = json.dumps(item)
            scenario = item["execution"]["setup"]["command"][2]
            if item["id"] == 6:
                continue
            self.assertIn("discovery-01.md", blob, f"eval {item['id']} lacks discovery input")
            self.assertNotIn(
                "Independently execute", item["prompt"], f"eval {item['id']} re-probes"
            )
            self.assertNotIn(
                "Independently exercise", item["prompt"], f"eval {item['id']} re-probes"
            )
            self.assertTrue(
                any(token in item["expected_output"] for token in ACCEPTANCE_VERDICT_TOKENS),
                f"eval {item['id']} does not demand a decision",
            )
            if scenario.endswith("-decision"):
                if scenario in CONTEXTUAL_CONTRAST_SETUPS:
                    setup = functions[CONTEXTUAL_CONTRAST_SETUPS[scenario]]
                    self.assertTrue(
                        "discovery_report(" in setup or "consequential_uncertainty_decision()" in setup,
                        f"contrast {scenario} does not supply discovery publication",
                    )
                    continue
                wrapper = scenario.replace("-", "_")
                self.assertIn(wrapper, functions, scenario)
                inherited = wrapper[: -len("_decision")]
                self.assertIn(
                    inherited + "()",
                    functions[wrapper],
                    f"wrapper {wrapper} does not stage the inherited scenario",
                )

    def test_acceptance_report_template_is_a_decision_admission_contract(self):
        template = ROOT / "skills" / "task-implementation-flow" / "task-acceptance-review" / "references" / "acceptance-report-template.md"
        text = normalized(template)

        self.assertIn("| Discovery report |", text)
        self.assertIn("Admitted evidence ledger and reconciliation", text)
        self.assertIn("Admitted discovery probes and command records", text)
        self.assertIn("Admitted aggregate-gate record", text)
        self.assertIn("admitted without re-execution", text)
        self.assertIn("Acceptance consumes these records; it does not routinely re-execute", text)
        self.assertIn("`SELF_CHECK_ONLY`", text)
        self.assertIn("`ACCEPT | CHANGES_REQUESTED | INCONCLUSIVE | none — SELF_CHECK_ONLY`", text)
        self.assertIn("Preserve the discovery report's stable finding IDs", text)


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


class ContextualDispositionContractTests(unittest.TestCase):
    """Fail-first contract checks for the contextual rubric and recording rules.

    These assertions reject an unconditional ACCEPT-on-green-tests rubric,
    routine ordinary-unknown prompts, dropped mixed-condition rows, and
    reviewer-owned tracker writes; they fail against guidance that lacks the
    contextual disposition contract.
    """

    def test_green_evidence_cannot_excuse_demonstrated_material_risk(self):
        text = normalized(ACCEPTANCE_SKILL)

        self.assertIn("## Contextual disposition and coordinator-owned deferrals", text)
        self.assertIn("Materiality follows supplied context, not reviewer taste", text)
        self.assertIn(
            "separate impact and likelihood/exposure, existing mitigation, and a contextual fix-now or deferral rationale",
            text,
        )
        self.assertIn("Assess impact and likelihood separately", text)
        self.assertIn(
            "Low likelihood cannot erase catastrophic data, security, or irreversible-state consequences",
            text,
        )
        self.assertIn(
            "Green tests, passing ACs, producer self-claims, and suggested-severity labels cannot excuse a demonstrated material risk",
            text,
        )

    def test_rubric_table_covers_every_disposition_branch(self):
        text = normalized(ACCEPTANCE_SKILL)

        for token in (
            "Demonstrated AC/gate violation or unauthorized effect",
            "Confirmed material operating or business risk with passing ACs",
            "Confirmed material maintainability/refactoring risk",
            "Bounded non-material confirmed defect; all required evidence passes",
            "Preference, polish, or speculative improvement",
            "Missing decisive required evidence, without a confirmed blocker eligible for bounded correction",
            "Ordinary uncertainty or unproved minor concern",
            "Unresolved uncertainty with credible serious consequences of delay or materially more costly later repair",
            "A hard-rule breach is sufficient, not necessary",
            "speculative redesign is insufficient",
        ):
            self.assertIn(token, text)

    def test_mixed_condition_precedence_and_retained_rows(self):
        text = normalized(ACCEPTANCE_SKILL)

        self.assertIn(
            "yields `CHANGES_REQUESTED` even when another required row is blocked or unchecked or a separate material-context question is unresolved",
            text,
        )
        self.assertIn("Retain every finding and unfinished row with its reason and owner", text)
        self.assertIn(
            "Route correction, evidence recovery, and any necessary authority question separately through the coordinator",
            text,
        )
        self.assertIn("an evidence request is not a production-fix request", text)
        self.assertIn("return `INCONCLUSIVE` while retaining the confirmed blocker", text)
        self.assertIn("ordinary uncertainty alone does not force either verdict", text)
        self.assertIn("Neither `CHANGES_REQUESTED` nor `INCONCLUSIVE` permits advancement", text)
        self.assertIn("unfinished rows are never treated as clean", text)

    def test_ordinary_uncertainty_continues_without_routine_prompts(self):
        text = normalized(ACCEPTANCE_SKILL)

        self.assertIn(
            "Continue under a stated reasonable assumption; record an observation", text
        )
        self.assertIn(
            "Make routine dispositions and authorized bounded correction or evidence requests without a new user confirmation",
            text,
        )
        self.assertIn("Resolve within current authority first", text)
        self.assertIn(
            "ask one focused question naming the consequence and the needed fact", text
        )
        self.assertIn("Do not ask the user to classify every issue", text)
        self.assertIn("required proof is never waived", text)

    def test_deferrals_are_coordinator_recorded_with_complete_provenance(self):
        text = normalized(ACCEPTANCE_SKILL)

        self.assertIn(
            "the human coordinator alone records it, before authorized advancement, using `docs/known-issues.md` by default",
            text,
        )
        self.assertIn("No known-issues file is required before a deferral exists", text)
        self.assertIn(
            "never write the tracker or acquire backlog or portfolio scheduling authority", text
        )
        self.assertIn(
            "a stable project issue ID; task/review/finding provenance; trigger, consequence, and evidence; impact and likelihood; affected boundary and consumers; deferral rationale; follow-up owner and action; and reassessment conditions",
            text,
        )
        self.assertIn("distinguishing confirmed relationships from suspected similarity", text)
        self.assertIn("Missing links mean unknown relationships, not their absence", text)
        self.assertIn("Planned work alone is not existing mitigation", text)
        self.assertIn("imposes no hidden consumer workaround", text)

    def test_portfolio_priority_change_alone_cannot_reopen_acceptance(self):
        text = normalized(ACCEPTANCE_SKILL)

        self.assertIn(
            "without invalidating acceptance solely because its priority changed", text
        )
        self.assertIn("A priority change alone does not reopen acceptance", text)
        self.assertIn(
            "changed material facts that invalidate an actual acceptance assumption or reveal a material violation can require focused review under existing authority",
            text,
        )
        self.assertIn(
            "Acceptance acquires no portfolio review gate, new verdict, refactoring authority, or power to create requirements",
            text,
        )
        self.assertIn(
            "Portfolio choices cannot excuse a demonstrated current AC/gate violation, unauthorized effect, or material risk this task was required to resolve",
            text,
        )

    def test_stable_dispositions_and_new_blocker_reasons(self):
        text = normalized(ACCEPTANCE_SKILL)

        self.assertIn(
            "Preserve an accepted disposition while its exposure is unchanged", text
        )
        self.assertIn(
            "optional improvements create no new correction obligation and never restart correction",
            text,
        )
        for reason in (
            "correction regression",
            "formerly blocked evidence",
            "a missed existing obligation",
            "changed context/authority",
            "newly demonstrated material risk",
        ):
            self.assertIn(reason, text)
        self.assertIn(
            "A stale severity label or a prior acceptance alone cannot supply or suppress a new blocker",
            text,
        )
        self.assertIn(
            "Add no global correction-round limit; the task's existing task-specific stop rules remain in force",
            text,
        )

    def test_report_template_carries_contextual_fields_and_recording_instructions(self):
        template = (
            ACCEPTANCE_PACKAGE / "references" / "acceptance-report-template.md"
        )
        text = normalized(template)

        self.assertIn("### Accepted deferrals and coordinator recording", text)
        self.assertIn(
            "the human coordinator alone records it, before authorized advancement, in `docs/known-issues.md`",
            text,
        )
        self.assertIn("no known-issues file is required before a deferral exists", text)
        self.assertIn("Impact (assessed separately from likelihood)", text)
        self.assertIn("Likelihood / exposure", text)
        self.assertIn("Existing mitigation", text)
        self.assertIn("Fix-now / deferral rationale", text)
        self.assertIn("Affected boundary", text)
        self.assertIn("planned work alone is not existing mitigation", text)
        self.assertIn(
            "Preferences, polish, and unproved minor concerns are recorded as observations, never as known issues",
            text,
        )


class ContextualRiskFixtureTests(unittest.TestCase):
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

    def test_material_exposure_is_stated_only_in_the_readiness_context(self):
        work = self.stage("contextual-risk-blockers-decision")
        root = work / "contextual-runner"
        preflight = normalized(root / "docs" / "tasks" / "INV-07" / "preflight.md")
        discovery = normalized(work / "task-runs" / "INV-07" / "discovery-01.md")
        self.assertIn("must not destroy yesterday's paid-invoice ledger", preflight)
        self.assertIn("the reporting consumer's timezone is not specified", preflight)
        self.assertIn("gains a mandatory `tax` field next sprint", preflight)
        self.assertIn("requires the CSV header row `invoice_id,amount`", preflight)
        self.assertNotIn("must not destroy yesterday's paid-invoice ledger", discovery)
        self.assertIn("readiness decision context", discovery)

    def test_mixed_conditions_stage_a_real_blocker_blocked_row_and_constraint(self):
        work = self.stage("mixed-conditions-authorized-decision")
        root = work / "mixed-runner"
        state = root / "state.json"
        state.write_text(
            json.dumps(
                {"jobs": [{"id": "JOB-1", "status": "ready"}, {"id": "JOB-2", "status": "ready"}]}
            )
        )
        first = subprocess.run(
            [sys.executable, "-m", "src.jobs.claim", str(state)],
            cwd=root,
            capture_output=True,
            text=True,
        )
        second = subprocess.run(
            [sys.executable, "-m", "src.jobs.claim", str(state)],
            cwd=root,
            capture_output=True,
            text=True,
        )
        self.assertEqual(first.stdout.strip(), "JOB-1")
        self.assertEqual(second.stdout.strip(), "")
        self.assertFalse((root / "tests" / "helpers" / "pair_claims.py").exists())
        policy = json.loads(
            (work / "task-runs" / "policies" / "local-review-mixed.json").read_text()
        )
        self.assertIn(
            "bounded production correction by the owning implementer thread", policy["allow"]
        )
        self.assertIn(
            "strictly ordered across state files",
            normalized(root / "docs" / "tasks" / "JOB-05" / "preflight.md"),
        )
        authorized_discovery = (work / "task-runs" / "JOB-05" / "discovery-01.md").read_text()
        self.assertIn("JOB-PAIR=blocked", authorized_discovery)

        forbidden = self.stage("mixed-conditions-forbidden-decision")
        forbidden_policy = json.loads(
            (forbidden / "task-runs" / "policies" / "local-review-mixed.json").read_text()
        )
        self.assertIn("production edits in this review cycle", forbidden_policy["deny"][0])

    def test_retention_horizon_is_configurable_but_the_region_fact_is_unresolved(self):
        from datetime import datetime, timedelta

        work = self.stage("consequential-uncertainty-decision")
        root = work / "retention-runner"
        old = (datetime.now() - timedelta(days=1460)).isoformat()
        recent = (datetime.now() - timedelta(days=365)).isoformat()
        state = root / "state.json"

        state.write_text(
            json.dumps(
                {"invoices": [{"id": "INV-OLD", "date": old}, {"id": "INV-NEW", "date": recent}]}
            )
        )
        subprocess.run(
            [sys.executable, "-m", "src.retention.purge", str(state)],
            cwd=root,
            env=dict(os.environ, RETENTION_YEARS="3"),
            check=True,
            capture_output=True,
        )
        kept = [invoice["id"] for invoice in json.loads(state.read_text())["invoices"]]
        self.assertEqual(kept, ["INV-NEW"])

        state.write_text(
            json.dumps(
                {"invoices": [{"id": "INV-OLD", "date": old}, {"id": "INV-NEW", "date": recent}]}
            )
        )
        subprocess.run(
            [sys.executable, "-m", "src.retention.purge", str(state)],
            cwd=root,
            env=dict(os.environ, RETENTION_YEARS="7"),
            check=True,
            capture_output=True,
        )
        kept = [invoice["id"] for invoice in json.loads(state.read_text())["invoices"]]
        self.assertEqual(kept, ["INV-OLD", "INV-NEW"])

        preflight = normalized(root / "docs" / "tasks" / "RET-03" / "preflight.md")
        self.assertIn("Region A requires 7 years; Region B requires 3 years", preflight)
        self.assertIn("not specified in any supplied authority", preflight)
        brief = normalized(root / "docs" / "tasks" / "RET-03" / "brief.md")
        self.assertNotIn("Region", brief)

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

    def test_authorized_resolution_and_serious_delay_have_decisive_inputs(self):
        work = self.stage("consequential-uncertainty-resolved-decision")
        root = work / "retention-runner"
        authority = json.loads((root / "cases/deployment-policy.json").read_text())
        self.assertEqual(authority, {"region": "B", "retention_years": 3})
        self.assertIn("may read", normalized(root / "AGENTS.md"))
        probe = subprocess.run(
            [sys.executable, "-m", "unittest", "tests.test_purge"], cwd=root,
            env=dict(os.environ, RETENTION_YEARS=str(authority["retention_years"])),
            capture_output=True,
        )
        self.assertEqual(probe.returncode, 0, probe.stderr)

        delayed = self.stage("serious-delay-uncertainty-decision")
        delayed_root = delayed / "retention-runner"
        deadline = json.loads((delayed_root / "cases/deadline.json").read_text())
        self.assertLess(deadline["remaining_hours"], deadline["authority_response_hours"])
        self.assertFalse((delayed_root / "cases/deployment-policy.json").exists())
        context = normalized(delayed_root / "docs/tasks/RET-03/preflight.md")
        self.assertIn("serious contractual delay", context)
        self.assertIn("no supplied authority can settle", context)

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

    def test_serious_delay_resolves_locally_only_with_supplied_authority(self):
        for resolved in (False, True):
            with self.subTest(resolved=resolved):
                scenario = "serious-delay-uncertainty" + ("-resolved" if resolved else "") + "-decision"
                work = self.stage(scenario)
                root = work / "retention-runner"
                deadline = json.loads((root / "cases/deadline.json").read_text())
                self.assertEqual(deadline, {"remaining_hours": 2, "authority_response_hours": 8})
                context = normalized(root / "docs/tasks/RET-03/preflight.md")
                report = normalized(work / "task-runs/RET-03/discovery-01.md")
                self.assertIn("serious contractual delay", context)
                policy = root / "cases/deployment-policy.json"
                self.assertEqual(policy.exists(), resolved)
                if resolved:
                    authority = json.loads(policy.read_text())
                    self.assertEqual(authority, {"region": "B", "retention_years": 3})
                    self.assertIn("may read cases/deployment-policy.json", normalized(root / "AGENTS.md"))
                    self.assertNotIn("no supplied authority can settle", context)
                    self.assertNotIn("route one expedited region question", report)
                    self.assertIn("authorized local read settles", report)
                    probe = subprocess.run(
                        [sys.executable, "-m", "unittest", "tests.test_purge"], cwd=root,
                        env=dict(os.environ, RETENTION_YEARS=str(authority["retention_years"])),
                        capture_output=True,
                    )
                    self.assertEqual(probe.returncode, 0, probe.stderr)
                else:
                    self.assertIn("no supplied authority can settle", context)
                    self.assertIn("route one expedited region question", report)

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

    def test_mixed_evals_explicitly_select_guided_profile(self):
        by_id = {item["id"]: item for item in json.loads(ACCEPTANCE_EVALS.read_text())["evals"]}
        for eval_id in (13, 14):
            self.assertIn("Use the guided profile explicitly", by_id[eval_id]["prompt"])

    def test_optional_link_grading_is_conditional(self):
        item = next(item for item in json.loads(ACCEPTANCE_EVALS.read_text())["evals"] if item["id"] == 12)
        expectation = next(text for text in item["expectations"] if "Optional context links" in text)
        self.assertIn("If included", expectation)
        self.assertIn("may be omitted", expectation)


class ContextualDispositionEvalTests(unittest.TestCase):
    NEW_CONTEXTUAL_EVALS = {
        11: ("contextual-risk-blockers-decision", "`CHANGES_REQUESTED`"),
        12: ("contextual-risk-mitigated-decision", "`ACCEPT`"),
        13: ("mixed-conditions-authorized-decision", "`CHANGES_REQUESTED`"),
        14: ("mixed-conditions-forbidden-decision", "`INCONCLUSIVE`"),
        15: ("consequential-uncertainty-decision", "`INCONCLUSIVE`"),
        16: ("known-issue-consumption-decision", "`CHANGES_REQUESTED`"),
        17: ("correction-regression-decision", "`CHANGES_REQUESTED`"),
        18: ("consequential-uncertainty-resolved-decision", "`ACCEPT`"),
        19: ("serious-delay-uncertainty-decision", "`INCONCLUSIVE`"),
        20: ("known-issue-proposed-work-decision", "`ACCEPT`"),
        21: ("known-issue-committed-work-decision", "`ACCEPT`"),
        22: ("known-issue-priority-only-decision", "`ACCEPT`"),
        23: ("known-issue-no-links-decision", "`ACCEPT`"),
        24: ("repeated-review-formerly-blocked-evidence-decision", "`CHANGES_REQUESTED`"),
        25: ("repeated-review-missed-existing-obligation-decision", "`CHANGES_REQUESTED`"),
        26: ("repeated-review-changed-context-authority-decision", "`CHANGES_REQUESTED`"),
        27: ("repeated-review-newly-demonstrated-material-risk-decision", "`CHANGES_REQUESTED`"),
        28: ("serious-delay-uncertainty-resolved-decision", "`ACCEPT`"),
    }

    def test_new_contextual_evals_are_registered_with_expected_verdicts(self):
        acceptance = json.loads(ACCEPTANCE_EVALS.read_text(encoding="utf-8"))
        by_id = {item["id"]: item for item in acceptance["evals"]}
        for eval_id, (scenario, verdict) in self.NEW_CONTEXTUAL_EVALS.items():
            item = by_id[eval_id]
            self.assertEqual(scenario, item["execution"]["setup"]["command"][2])
            self.assertEqual(
                ["python3", "evals/files/setup_fixture.py"],
                item["execution"]["setup"]["command"][:2],
            )
            self.assertEqual(
                {"EVAL_WORK_ROOT": "{run_root}/work"}, item["execution"]["setup"]["env"]
            )
            self.assertTrue(
                item["execution"]["workspace"].startswith("{run_root}/work/")
            )
            self.assertIn("discovery-01.md", json.dumps(item))
            self.assertIn(verdict, item["expected_output"])

    def test_contextual_evals_reject_permissive_decisions(self):
        acceptance = json.loads(ACCEPTANCE_EVALS.read_text(encoding="utf-8"))
        by_id = {item["id"]: item for item in acceptance["evals"]}

        blob11 = json.dumps(by_id[11])
        self.assertIn("despite the passing AC rows", blob11)
        self.assertIn("likelihood does not erase", blob11)
        self.assertIn("without requiring a hard-rule breach", blob11)
        self.assertIn("no routine user prompt", blob11)
        self.assertIn("no known-issues record is created", blob11)

        blob12 = json.dumps(by_id[12])
        self.assertIn(
            "planned work alone is not treated as existing mitigation", blob12
        )
        self.assertIn("stable issue ID", blob12)
        self.assertIn(
            "human coordinator recording the approved deferral before authorized advancement",
            blob12,
        )

        blob13 = json.dumps(by_id[13])
        self.assertIn("even though the JOB-PAIR row is blocked", blob13)
        self.assertIn("separate next owners", blob13)

        blob14 = json.dumps(by_id[14])
        self.assertIn("prevents the bounded production-correction route", blob14)
        self.assertIn("Ordinary uncertainty alone did not force this verdict", blob14)

        blob15 = json.dumps(by_id[15])
        self.assertIn("exactly one focused question", blob15)
        self.assertIn("does not invent or assume the applicable region", blob15)

        blob16 = json.dumps(by_id[16])
        self.assertIn("hidden workaround", blob16)
        self.assertIn("no broad issue search", blob16)

        blob17 = json.dumps(by_id[17])
        self.assertIn("new blocker", blob17)
        self.assertIn("exposure is unchanged", blob17)
        self.assertIn("No global correction-round limit", blob17)


class ComposedReviewFlowGuideTests(unittest.TestCase):
    """Fail-first checks for the composed functional-review route guidance.

    Every affected overview must show fresh discovery before the separate
    independent acceptance decision, coordinator recording before authorized
    continuation, and no wording that lets one session accept itself or skip
    discovery. Role-reasoning guidance adds no launcher adapter, fifth
    metadata key, or observed-runtime claim.
    """

    def test_root_readme_route_shows_discovery_before_separate_acceptance(self):
        text = ROOT_README.read_text(encoding="utf-8")
        route = next(
            block
            for block in fenced_blocks(text)
            if "bounded-task-implementer" in block and "task-acceptance-review" in block
        )
        self.assertIn("task-review-discovery", route)
        self.assertLess(
            route.index("task-review-discovery"),
            route.index("task-acceptance-review"),
        )
        self.assertIn("coordinator recording", route)
        self.assertNotIn("admits discovery evidence when the flow splits it", text)

    def test_root_readme_contract_sequence_includes_independent_review_discovery(self):
        text = ROOT_README.read_text(encoding="utf-8")
        block = next(
            block
            for block in fenced_blocks(text)
            if "contract-registry synchronization" in block
        )
        self.assertIn("independent review discovery", block)
        self.assertLess(
            block.index("independent review discovery"),
            block.index("acceptance review"),
        )

    def test_profile_guide_task_route_requires_discovery_evidence(self):
        text = PROFILE_GUIDE.read_text(encoding="utf-8")
        route = next(
            block
            for block in fenced_blocks(text)
            if "bounded-task-implementer" in block and "task-acceptance-review" in block
        )
        self.assertIn("task-review-discovery", route)
        self.assertLess(
            route.index("task-review-discovery"),
            route.index("task-acceptance-review"),
        )
        self.assertIn("coordinator recording", route)
        self.assertNotIn("when evidence is published separately", text)

    def test_flow_readme_guided_route_and_layout_include_discovery(self):
        text = FLOW_README.read_text(encoding="utf-8")
        guided = next(
            block
            for block in fenced_blocks(text)
            if "required task-verification-designer for an executable task package"
            in block
        )
        self.assertIn("task-review-discovery", guided)
        self.assertLess(
            guided.index("task-review-discovery"),
            guided.index("functional acceptance"),
        )
        self.assertIn("coordinator recording", guided)
        layout = next(
            block for block in fenced_blocks(text) if "docs/tasks/" in block
        )
        self.assertIn("discovery-01.md", layout)

    def test_flow_readme_maintainability_gated_route_shows_discovery(self):
        text = FLOW_README.read_text(encoding="utf-8")
        gated = next(
            block
            for block in fenced_blocks(text)
            if "canonical deterministic architecture gate" in block
        )
        self.assertIn("task-review-discovery", gated)
        self.assertLess(
            gated.index("task-review-discovery"),
            gated.index("acceptance review"),
        )
        flat = normalized(FLOW_README)
        self.assertIn(
            "fresh maintainability reviewer before re-entering fresh discovery evidence and functional acceptance",
            flat,
        )
        self.assertNotIn("when discovery published its evidence separately", flat)
        self.assertIn("hand the fresh discovery report to the decision call", flat)

    def test_contract_aware_sequences_route_discovery_before_acceptance(self):
        for path in (FLOW_README, REGISTRY_UPDATER_SKILL):
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path):
                block = next(
                    block
                    for block in fenced_blocks(text)
                    if "task-contract-registry-updater" in block and "task brief" in block
                )
                self.assertIn("-> task-review-discovery", block)
                self.assertLess(
                    block.index("task-review-discovery"),
                    block.index("task-acceptance-review"),
                )

    def test_child_handoffs_name_discovery_before_the_acceptance_decision(self):
        implementer = normalized(BOUNDED_IMPLEMENTER_SKILL)
        self.assertIn(
            "Completed work routes to fresh independent `task-review-discovery` evidence and a separate fresh `task-acceptance-review` decision when independent review is requested or required",
            implementer,
        )
        self.assertIn(
            "Loading, quoting, or following `task-review-discovery` or `task-acceptance-review` in the current session",
            implementer,
        )
        self.assertIn(
            "exactly name fresh independent `task-review-discovery` evidence and the separate fresh `task-acceptance-review` decision as next owner",
            implementer,
        )
        self.assertNotIn("route to a fresh `task-acceptance-review`.", implementer)

        maintainability = normalized(MAINTAINABILITY_SKILL)
        self.assertIn(
            "proceed to fresh independent `task-review-discovery` evidence and the separate functional `task-acceptance-review` decision when that stage is required",
            maintainability,
        )
        self.assertIn(
            "repeat architecture gate + fresh maintainability review before fresh discovery evidence and fresh functional acceptance",
            maintainability,
        )

    def test_discovery_is_mandatory_whenever_independent_functional_review_runs(self):
        text = FLOW_README.read_text(encoding="utf-8")
        flat = normalized(FLOW_README)
        self.assertNotIn(
            "The flow does not split discovery from the acceptance decision", text
        )
        self.assertNotIn("When the flow splits evidence from the decision", flat)
        self.assertNotIn("when metadata or risk calls for it", flat)
        self.assertIn("Whenever independent functional review is required", flat)
        self.assertIn("never runs without that discovery evidence", flat)
        # The legitimate skip is functional review itself not being required.
        self.assertIn(
            "does not need independent functional review under its metadata or risk",
            text,
        )

    def test_brief_designer_follow_on_prescribes_discovery_then_acceptance(self):
        follow_on = (
            "hand the completed bytes to a fresh independent "
            "`task-review-discovery` call, and hand its report to a separate "
            "`task-acceptance-review` decision"
        )
        designer = normalized(DESIGNER_SKILL)
        self.assertIn("any applicable conditional stages", designer)
        self.assertIn(follow_on, designer)
        self.assertIn(
            "through applicable conditional stages and fresh independent "
            "`task-review-discovery` evidence to the separate "
            "`task-acceptance-review` decision",
            designer,
        )
        self.assertIn("does not state independent acceptance", designer)
        template = normalized(DESIGNER_TEMPLATE)
        self.assertIn("any applicable conditional stages", template)
        self.assertIn(follow_on, template)
        self.assertIn(
            "Do not use same-session self-review as that discovery or acceptance step",
            template,
        )
        self.assertNotIn("fresh independent acceptance reviewer", designer + template)

    def test_implementer_eval_mirrors_route_discovery_before_acceptance(self):
        evals = json.loads(IMPLEMENTER_EVALS.read_text(encoding="utf-8"))["evals"]
        by_id = {case["id"]: case for case in evals}
        for case_id in (1, 5):
            blob = json.dumps(by_id[case_id])
            self.assertIn("task-review-discovery", blob)
            self.assertLess(
                blob.index("task-review-discovery"),
                blob.index("task-acceptance-review"),
            )
        fixture = IMPLEMENTER_FIXTURE.read_text(encoding="utf-8")
        for stale in (
            "Next route after complete: task-acceptance-review.",
            "hand the current bytes to a fresh acceptance reviewer",
            "names fresh task-acceptance-review as next owner",
            "next owner: fresh task-acceptance-review",
            "then fresh task-acceptance-review.",
        ):
            self.assertNotIn(stale, fixture)
        self.assertIn(
            "Next route after complete: fresh task-review-discovery evidence, "
            "then a separate fresh task-acceptance-review decision",
            fixture,
        )

    def test_role_reasoning_guidance_adds_no_adapter_fifth_key_or_runtime_claim(self):
        text = FLOW_README.read_text(encoding="utf-8")
        metadata = next(
            block for block in fenced_blocks(text) if "agent_tier:" in block
        )
        keys = {
            line.split(":")[0].strip()
            for line in metadata.splitlines()
            if ":" in line and "->" not in line
        }
        self.assertEqual({"agent_tier", "reasoning", "review", "budget"}, keys)
        flat = normalized(FLOW_README)
        self.assertIn(
            "A high reasoning tier is recommended for discovery",
            flat,
        )
        self.assertIn(
            "an equally high tier is recommended for the separate acceptance decision",
            flat,
        )
        self.assertIn(
            "launch tooling enforces neither the separate-call roles nor the reasoning recommendations",
            flat,
        )
        self.assertIn(
            "intended launch guidance, not claims about the eventual runtime configuration",
            flat,
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
