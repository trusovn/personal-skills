"""Acceptance admission, contextual disposition, and decision-eval metadata.

Contract checks over the acceptance skill and report template, plus the
decision-eval metadata probes that verify guided/mixed-context registration.
"""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from review_fixture_support import (
    ACCEPTANCE_EVALS,
    ACCEPTANCE_FIXTURE,
    ACCEPTANCE_PACKAGE,
    ACCEPTANCE_SKILL,
    ACCEPTANCE_VERDICT_TOKENS,
    CONTEXTUAL_CONTRAST_SETUPS,
    ROOT,
    fixture_functions,
    normalized,
)


class ReviewerDisciplineTests(unittest.TestCase):

    def test_mixed_and_repeated_review_facts_cross_the_public_boundary(self):
        scenarios = ["mixed-conditions-authorized-decision", "mixed-conditions-forbidden-decision",
                     "correction-regression-decision"] + [
            name for name in CONTEXTUAL_CONTRAST_SETUPS if name.startswith("repeated-review")]
        for scenario in scenarios:
            with self.subTest(scenario=scenario), tempfile.TemporaryDirectory() as temporary:
                work = Path(temporary)
                subprocess.run([sys.executable, str(ACCEPTANCE_FIXTURE), scenario],
                               env=os.environ | {"EVAL_WORK_ROOT": temporary}, check=True)
                mixed = scenario.startswith("mixed")
                root = work / ("mixed-runner" if mixed else "correction-runner")
                state = root / "probe.json"
                state.write_text(json.dumps({"jobs": [{"id": f"JOB-{i}", "status": "ready"} for i in (1, 2)]}
                                            if mixed else {"pending": [{"id": "ORD-1"}], "output": []}))
                commands = [sys.executable, "-m", "src.jobs.claim" if mixed else "src.orders.retry", str(state)]
                results = [subprocess.check_output(commands, cwd=root, text=True).strip() for _ in range(2)]
                if mixed:
                    self.assertEqual(["JOB-1", ""], results)
                    self.assertFalse((root / "tests/helpers/pair_claims.py").exists())
                    policy = json.loads((work / "task-runs/policies/local-review-mixed.json").read_text())
                    self.assertEqual("authorized" in scenario,
                                     "bounded production correction by the owning implementer thread" in policy["allow"])
                else:
                    self.assertEqual(["processed 1 orders"] * 2, results)
                    self.assertEqual(["ORD-1,processed"] * 2, json.loads(state.read_text())["output"])
                    context = (root / "docs/tasks/ORD-04/preflight.md").read_text()
                    self.assertIn("unchanged", context)
                    self.assertIn("KI-001", (root / "docs/known-issues.md").read_text())
                    if scenario == "repeated-review-newly-demonstrated-material-risk-decision":
                        self.assertEqual("20", subprocess.check_output(
                            [sys.executable, "consumers/settle.py", str(state)], cwd=root, text=True).strip())


    def test_reference_shortcut_and_mixed_continuation_are_effect_bound(self):
        for path in (ACCEPTANCE_SKILL, ACCEPTANCE_PACKAGE / "references/acceptance-report-template.md"):
            text = normalized(path)
            for obligation in ("actual effects and current behavioral proof", "separate correction/evidence/authority",
                               "first outstanding", "complete ordered remainder", "old readiness"):
                self.assertIn(obligation, text)

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


    def test_guided_inputs_identify_and_read_packaged_preparation_references(self):
        """INT-FLOW-001 I-04: guided acceptance input includes and reads the
        applicable verification revision, readiness, and decision-context
        references for complete as well as partial evidence; direct edits
        stay compact without a mandatory packet.
        """
        text = normalized(ACCEPTANCE_SKILL)
        self.assertIn(
            "the applicable packaged preparation references when the task is "
            "packaged: the verification design with its revision, the "
            "readiness/preflight evidence, and the recorded decision context",
            text,
        )
        self.assertIn(
            "for complete, clean guided evidence as well as partial evidence",
            text,
        )
        self.assertIn(
            "Identify and read the references that are applicable to the "
            "decision",
            text,
        )
        self.assertIn(
            "a guided direct edit may use the supplied conversational/"
            "repository context instead",
            text,
        )
        self.assertIn(
            "a missing decision-relevant preparation reference routes to its "
            "owner with a focused request",
            text,
        )
        workflow = text.split("## Decision workflow", 1)[1].split(
            "2. Reconstruct", 1
        )[0]
        self.assertIn("the applicable packaged preparation references", workflow)


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


    def test_guided_continuation_requires_scenario_history_and_separate_owners(self):
        text = ACCEPTANCE_SKILL.read_text(encoding="utf-8")
        start = text.index("Review continuation:")
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


    def test_mixed_evals_explicitly_select_guided_profile(self):
        by_id = {item["id"]: item for item in json.loads(ACCEPTANCE_EVALS.read_text())["evals"]}
        for eval_id in (13, 14):
            self.assertIn("Use the guided profile explicitly", by_id[eval_id]["prompt"])


    def test_optional_link_grading_is_conditional(self):
        item = next(item for item in json.loads(ACCEPTANCE_EVALS.read_text())["evals"] if item["id"] == 12)
        expectation = next(text for text in item["expectations"] if "Optional context links" in text)
        self.assertIn("If included", expectation)
        self.assertIn("may be omitted", expectation)



if __name__ == "__main__":
    unittest.main()
