"""Bounded-task-implementer entry contract and evaluation fixture checks.

Packaged guided entry, high-assurance routes, continuation semantics,
submission mapping, and the entry/evidence fixtures behind the implementer
skill.
"""

import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from review_fixture_support import FLOW, ROOT
from staging_fixture_support import stage_setup

IMPLEMENTER = FLOW / "bounded-task-implementer"

ROUTE_CASE_ROUTES = {
    "INIT-NEITHER": "discovery → acceptance",
    "INIT-MAINT-GATE": "architecture gate → fresh maintainability review → discovery → acceptance",
    "INIT-MAINT-NOGATE": "fresh maintainability review → discovery → acceptance",
    "INIT-REGISTRY": "registry updater → discovery → acceptance",
    "INIT-BOTH-GATE": "architecture gate → fresh maintainability review → registry updater → discovery → acceptance",
    "INIT-BOTH-NOGATE": "fresh maintainability review → registry updater → discovery → acceptance",
    "STATE-MAINT-GATE-COMPLETE": "fresh maintainability review → discovery → acceptance",
    "STATE-MAINT-COMPLETE": "discovery → acceptance",
    "STATE-REGISTRY-COMPLETE": "discovery → acceptance",
    "STATE-BOTH-GATE-MAINT-COMPLETE": "registry updater → discovery → acceptance",
    "STATE-BOTH-UPDATER-COMPLETE": "architecture gate → fresh maintainability review → discovery → acceptance",
    "STATE-BOTH-COMPLETE": "discovery → acceptance",
    "STATE-BOTH-INAPPLICABLE": "architecture gate → fresh maintainability review → registry updater → discovery → acceptance",
    "CORR-NEITHER": "discovery → acceptance",
    "CORR-MAINT-GATE": "architecture gate → fresh maintainability review → discovery → acceptance",
    "CORR-REGISTRY": "registry updater → discovery → acceptance",
    "CORR-BOTH-FULL": "architecture gate → fresh maintainability review → registry updater → discovery → acceptance",
    "CORR-BOTH-MIXED": "registry updater → discovery → acceptance",
    "CORR-BOTH-TESTS-ONLY": "architecture gate → fresh maintainability review → registry updater → discovery → acceptance",
}

ROUTE_STAGE_RULES = (
    ("architecture gate", "architecture gate required", "architecture gate complete", "architecture gate"),
    ("maintainability review", "maintainability review applies", "maintainability review complete", "fresh maintainability review"),
    ("registry stage", "registry stage applies", "registry updater complete", "registry updater"),
)

ROUTE_PART_TOKENS = {
    "architecture gate": "architecture gate",
    "fresh maintainability review": "`task-maintainability-review`",
    "registry updater": "`task-contract-registry-updater`",
    "discovery": "`task-review-discovery`",
    "acceptance": "`task-acceptance-review`",
}


class ImplementerContractTest(unittest.TestCase):

    def test_reading_evals_supply_authority_and_conflicting_result_records(self):
        package = ROOT / "skills/project-delivery-plan"
        evals = json.loads((package / "evals/evals.json").read_text())["evals"]
        for case in evals:
            scenario = case["execution"]["setup"]["command"][-1]
            with self.subTest(scenario=scenario):
                work = stage_setup(self, package / "evals/files/setup_fixture.py", scenario)
                docs = work / scenario / "docs"
                request = (docs / "request.md").read_text()
                self.assertIn({"small-change": "header name,status",
                               "multi-task": "Reject reassignment without writing",
                               "missing-direction": "No beneficiary"}[scenario], request)
                self.assertIn("foundation ready", (docs / "foundation-review.md").read_text())
                self.assertIn("No implementation edits", (docs / "current-report.md").read_text())
                self.assertIn("old version only", (docs / "historical-acceptance.md").read_text())
                self.assertIn("conflicts with current-report.md", (docs / "handover-note.md").read_text())
                self.assertFalse((docs / "project-plan.md").exists())

    def test_interrupted_reading_eval_exercises_a_real_failure(self):
        case = next(case for case in json.loads(
            (IMPLEMENTER / "evals/evals.json").read_text())["evals"] if case["id"] == 9)
        work = stage_setup(self, IMPLEMENTER / "evals/files/setup_fixture.py",
                           case["execution"]["setup"]["command"][-1])
        root = work / "api-immediate"
        before = (root / "src/auth/session.py").read_bytes()
        result = subprocess.run(
            [sys.executable, "-m", "unittest",
             "tests.auth.test_session.SessionTest.test_expired_session_is_invalid"],
            cwd=root, capture_output=True, text=True)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("True is not false", result.stderr)
        self.assertEqual(before, (root / "src/auth/session.py").read_bytes())
        self.assertEqual("", subprocess.check_output(
            ["git", "status", "--short"], cwd=root, text=True).strip())

    def test_correction_handoff_retains_evidence_provenance_and_separate_routes(self):
        text = " ".join((IMPLEMENTER / "SKILL.md").read_text().split())
        for obligation in (
            "Preflight/context reference", "Incomplete reason", "Attempts and discarded hypotheses",
            "Influenced sibling surfaces", "Finding/scenario IDs", "owner and stage",
            "an evidence request is not a production-fix request",
            "actual effects and current behavioral proof",
            "verification designer → focused preflight",
            "ordinary corrections and clarifications do not restart task design",
            "Preserve accepted dispositions", "no global correction-round limit",
            "serious consequences of delay", "materially costly later repair",
            "stopped work is non-complete",
        ):
            self.assertIn(obligation, text)


    def test_record_correction_preserves_all_row_states_after_target_passes(self):
        with tempfile.TemporaryDirectory() as temporary:
            self.fixture(temporary, "record-correction")
            root = Path(temporary) / "result-record"
            review = (root / "docs/tasks/REC-44/reviews/acceptance-01.md").read_text()
            for row, status in (("ROW-ORIGINAL", "passed"), ("ROW-EXACT-BYTES", "failed"),
                                ("ROW-REMOTE-ANCHOR", "blocked"), ("ROW-REPLAY-BOUNDARY", "unchecked")):
                self.assertIn(f"{row} — {status}", review)
                self.assertIn(row, (root / "docs/tasks/REC-44/verification.md").read_text())
            for field in ("F-01", "Preflight/context reference:", "Influenced sibling surfaces:",
                          "Attempts and discarded hypotheses:", "owner and stage:"):
                self.assertIn(field, review)
            command = [sys.executable, "-m", "unittest", "tests.test_record_integrity"]
            failed = subprocess.run(command, cwd=root, capture_output=True, text=True)
            self.assertNotEqual(0, failed.returncode)
            self.assertIn("AssertionError", failed.stderr)
            # Submitted correction evidence only: no fabricated reviewer output.
            (root / "src/result_integrity.py").write_text(
                "import hashlib\ndef is_anchored_result(result_bytes, anchor_digest):\n"
                "    return hashlib.sha256(result_bytes).hexdigest() == anchor_digest\n")
            passed = subprocess.run(command, cwd=root, capture_output=True, text=True)
            self.assertEqual(0, passed.returncode, passed.stderr)
            siblings = subprocess.run([sys.executable, "-c",
                "import json; from pathlib import Path; from src.result_integrity import is_anchored_result; "
                "raw=Path('authority/result.json').read_bytes(); anchor=Path('authority/result.sha256').read_text().strip(); "
                "data=json.loads(raw); "
                "assert not is_anchored_result(json.dumps(data,indent=2).encode(),anchor); "
                "data['files_changed']=[]; assert not is_anchored_result(json.dumps(data).encode(),anchor)"],
                cwd=root, capture_output=True, text=True)
            self.assertEqual(0, siblings.returncode, siblings.stderr)
            self.assertEqual(review, (root / "docs/tasks/REC-44/reviews/acceptance-01.md").read_text())
            self.assertFalse((root / "tools/remote_anchor.py").exists())
            self.assertIn("ROW-REPLAY-BOUNDARY", review.split("Remaining obligations:")[1])


    def test_effect_routes_use_actual_bytes_and_current_proof(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.fixture(temporary, "route-cases")
            cases = json.loads((root / "change-effects/cases.json").read_text())
            expected = {
                "clarification": "clarifying artifact owner → discovery → acceptance",
                "evidence": "capability owner → discovery → acceptance",
                "production": "architecture gate → fresh maintainability review → registry updater → discovery → acceptance",
                "tests-policy-exception": "registry updater → discovery → acceptance",
                "reference": "registry updater → acceptance",
                "reference-executable": "architecture gate → fresh maintainability review → registry updater → discovery → acceptance",
                "reference-missing-proof": "registry updater → discovery → acceptance",
                "scenario": "verification designer → focused preflight → revised-scenario evidence → acceptance",
                "authority": "task designer/decision owner",
            }
            self.assertEqual(set(expected), set(cases))
            for name, route in expected.items():
                with self.subTest(case=name):
                    case = cases[name]
                    self.assertEqual(route, case["route"])
                    folder = root / "change-effects" / name
                    changed = [path.relative_to(folder / "after").as_posix()
                               for path in (folder / "after").rglob("*") if path.is_file()
                               and path.read_bytes() != (folder / "before" / path.relative_to(folder / "after")).read_bytes()]
                    self.assertEqual(case["changed_paths"], sorted(changed))
                    if name.startswith("reference"):
                        probe = subprocess.run([sys.executable, "-c",
                            "from docs.contract import accepts; assert accepts(1); assert not accepts(True)"],
                            cwd=folder / "after", capture_output=True, text=True)
                        self.assertEqual(name == "reference-executable", probe.returncode != 0)
                        if name == "reference-executable":
                            self.assertIn("AssertionError", probe.stderr)
                        self.assertEqual(name != "reference-missing-proof", case["current_proof"])
            self.assertIn("explicit policy exception", cases["tests-policy-exception"]["policy"])


    def test_two_failed_fixes_keep_the_same_target_and_owned_stop(self):
        with tempfile.TemporaryDirectory() as temporary:
            self.fixture(temporary, "record-correction")
            root = Path(temporary) / "result-record"
            attempts = json.loads((root / "attempts/stop.json").read_text())
            self.assertEqual(2, len(attempts["attempts"]))
            self.assertEqual(1, len({attempt["target"] for attempt in attempts["attempts"]}))
            for attempt in attempts["attempts"]:
                result = subprocess.run([sys.executable, attempt["probe"]], cwd=root,
                                        capture_output=True, text=True)
                self.assertNotEqual(0, result.returncode)
                self.assertIn("AssertionError", result.stderr)
                self.assertTrue(attempt["hypothesis"])
            self.assertEqual("non-complete", attempts["status"])
            self.assertEqual("result-integrity owner", attempts["next_owner"])
            self.assertEqual(["ROW-EXACT-BYTES", "ROW-REMOTE-ANCHOR", "ROW-REPLAY-BOUNDARY"], attempts["unfinished_rows"])
            self.assertEqual({"passed", "failed", "blocked", "unchecked"}, set(attempts["coverage_rows"].values()))

    def fixture(self, temporary, scenario):
        setup = FLOW / "bounded-task-implementer/evals/files/setup_fixture.py"
        subprocess.run([sys.executable, str(setup), scenario], cwd=ROOT,
                       env=os.environ | {"EVAL_WORK_ROOT": temporary}, check=True)
        return Path(temporary) / scenario


    def guided_entry(self):
        skill = (IMPLEMENTER / "SKILL.md").read_text(encoding="utf-8")
        return " ".join(skill.split("### Guided inputs", 1)[1].split("## Optional run evidence", 1)[0].split())


    def assert_ready_preparation(self, brief, verification, preflight, source):
        self.assertIn("Status: ready", brief)
        self.assertIn("Task kind: executable", brief)
        self.assertIn("Outcome:", brief)
        acs = set(re.findall(r"^(AC-\d+):", brief, re.MULTILINE))
        self.assertTrue(acs)
        self.assertEqual(acs, set(re.findall(r"Covers: (AC-\d+)", verification)))
        for artifact in (verification, preflight):
            self.assertIn("Status: ready", artifact)
            self.assertIn(f"Source brief: {source}/brief.md", artifact)
            self.assertIn("Verification revision: 1", artifact)
        self.assertIn(f"Verification design: {source}/verification.md", preflight)
        scope = re.search(r"^Allowed changes: (.+?)\.?$", brief, re.MULTILINE).group(1)
        self.assertIn(f"Allowed changes: {scope}", preflight)
        for fact in ("Dependency:", "Ownership:", "Permission:", "Capability:", "Authority:"):
            self.assertIn(fact, preflight)


    def test_edit_producing_evals_supply_applicable_preparation(self):
        evals = json.loads((IMPLEMENTER / "evals/evals.json").read_text())["evals"]
        for case in (case for case in evals if case["id"] in (1, 3, 5, 6)):
            with self.subTest(case_id=case["id"]), tempfile.TemporaryDirectory() as temporary:
                setup = case["execution"]["setup"]
                subprocess.run([sys.executable, str(IMPLEMENTER / setup["command"][1]),
                                setup["command"][2]], cwd=IMPLEMENTER,
                               env=os.environ | {"EVAL_WORK_ROOT": temporary,
                                                 "PYTHONDONTWRITEBYTECODE": "1"}, check=True)
                repository = "queue-runner" if case["id"] == 1 else ""
                root = Path(case["execution"]["workspace"].replace("{run_root}/work", temporary)) / repository
                package, = (root / "docs/tasks").glob("*/brief.md")
                source = package.parent.relative_to(root).as_posix()
                for artifact in ("verification", "preflight"):
                    self.assertTrue((package.parent / f"{artifact}.md").is_file(),
                                    f"eval {case['id']} lacks {artifact} preparation")
                brief = package.read_text()
                verification = (package.parent / "verification.md").read_text()
                preflight = (package.parent / "preflight.md").read_text()
                if case["id"] == 1:
                    self.assertIn("Task kind: executable", brief)
                    self.assertIn("Status: ready", brief)
                    self.assertIn(f"Source brief: {source}/brief.md", verification)
                    self.assertIn(f"Verification design: {source}/verification.md", preflight)
                    for artifact in (verification, preflight):
                        self.assertIn("Verification revision: 1", artifact)
                    scope = re.search(r"^Allowed paths: .+$", brief, re.MULTILINE).group()
                    self.assertIn(scope, preflight)
                    for name in ("brief", "verification"):
                        digest = hashlib.sha256((package.parent / f"{name}.md").read_bytes()).hexdigest()
                        self.assertIn(digest, preflight)
                    self.assertIn("Artifact status: ready", preflight)
                    self.assertIn(f"Task brief: {source}/brief.md", preflight)
                    self.assertIn("Conditional-stage policy:", preflight)
                    self.assertIn("Conditional-stage evidence:", preflight)
                else:
                    self.assert_ready_preparation(brief, verification, preflight, source)
                self.assertIn("preflight", case["prompt"])
                self.assertIn("verification", case["prompt"])
                if case["id"] == 6:
                    command = [sys.executable, "-m", "unittest",
                               "tests.test_record_integrity.RecordIntegrityTest.test_coherent_mutation_is_rejected"]
                    result = subprocess.run(command, cwd=root, capture_output=True, text=True,
                                            env=os.environ | {"PYTHONDONTWRITEBYTECODE": "1"})
                    self.assertNotEqual(0, result.returncode)
                    self.assertIn("AssertionError", result.stderr)
                    review = (package.parent / "reviews/acceptance-01.md").read_text()
                    obligations = review.split("Remaining obligations:", 1)[1]
                    rows = set(re.findall(r"^- (ROW-\S+) — (?:failed|blocked|unchecked)", review, re.MULTILINE))
                    self.assertEqual(rows, set(re.findall(r"ROW-[A-Z-]+", obligations)))
                    for row in obligations.strip().splitlines():
                        self.assertIn("next owner:", row)


    def test_packaged_entry_requires_current_applicable_ready_preparation(self):
        guided = self.guided_entry()
        self.assertNotIn("A separate preflight packet, result schema, run directory, and tracker are not required", guided)
        self.assertNotIn("implementation may still proceed unless", guided)
        for obligation in (
            "Packaged guided entry",
            "current applicable ready `preflight.md`",
            "not the readiness owner",
            "does not repeat broad discovery",
            "task-verification-designer",
            "task-preflight",
            "task-brief-designer",
            "relabeled a conversational request",
            "no worker-result schema, exact digest chain",
            "Task kind: composite",
            "Status: decomposed",
            "docs/tasks/index.json",
            "dependency-ready executable leaf",
            "Refuse a direct legacy brief",
            "even when no `verification.md` exists",
            "package normalization",
        ):
            self.assertIn(obligation, guided)


    def test_continuation_semantics_distinguish_expected_effects_from_material_changes(self):
        guided = self.guided_entry()
        for obligation in (
            "Expected implementation or report effects alone do not stale",
            "affected obsolete readiness",
            "focused `task-preflight`",
            "dependency",
            "ownership",
            "permission",
            "capability",
            "authority",
            "feasible task-owned future test",
            "not a missing decisive capability",
        ):
            self.assertIn(obligation, guided)


    def test_submission_maps_every_scenario_with_reasons_and_context(self):
        skill = " ".join((IMPLEMENTER / "SKILL.md").read_text(encoding="utf-8").split())
        for obligation in (
            "every verification scenario ID",
            "blocked/unchecked reason and next owner",
            "Preflight/context reference",
            "Remaining obligations",
            "Green tests cannot excuse an omitted AC or scenario",
            "submission evidence, not independent acceptance",
        ):
            self.assertIn(obligation, skill)


    def test_direct_guided_and_high_assurance_routes_keep_their_limits(self):
        skill = " ".join((IMPLEMENTER / "SKILL.md").read_text(encoding="utf-8").split())
        for obligation in (
            "Conversational direct edits",
            "compact self-preflight",
            "best-effort",
            "does not invalidate an otherwise executable bounded task",
            "Missing or inconsistent high-assurance inputs",
            "Do not downgrade silently to guided mode",
            "READY_FOR_REVIEW",
            "machine contract",
            "not a high-assurance packet",
            "stays guided",
        ):
            self.assertIn(obligation, skill)


    def test_entry_fixture_supplies_valid_and_every_invalid_state(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.fixture(temporary, "entry-cases")
            tasks = root / "docs/tasks"
            valid = tasks / "VALID"
            self.assertIn("Task kind: executable", (valid / "brief.md").read_text())
            self.assertIn("AC-01:", (valid / "brief.md").read_text())
            self.assertIn("AC-02:", (valid / "brief.md").read_text())
            self.assertIn("Source brief: docs/tasks/VALID/brief.md", (valid / "verification.md").read_text())
            self.assertIn("Verification revision: 1", (valid / "verification.md").read_text())
            self.assertIn("Covers: AC-02", (valid / "verification.md").read_text())
            self.assertIn("Status: ready", (valid / "preflight.md").read_text())
            self.assertIn("Profile: guided", (valid / "preflight.md").read_text())
            self.assertIn("Verification revision: 1", (valid / "preflight.md").read_text())
            for fact in ("Dependency:", "Ownership:", "Permission:", "Capability:"):
                self.assertIn(fact, (valid / "preflight.md").read_text())
            self.assertIn("task-owned future test", (valid / "verification.md").read_text())
            self.assertTrue((root / "src/session.py").is_file())
            self.assertFalse((valid / "src").exists())
            self.assertFalse((root / "tests/test_future.py").exists())
            self.assertFalse((tasks / "NOVERIF/verification.md").exists())
            self.assertTrue((tasks / "NOVERIF/preflight.md").is_file())
            self.assertFalse((tasks / "NOPREP/preflight.md").exists())
            self.assertTrue((tasks / "NOPREP/verification.md").is_file())
            self.assertIn("Status: blocked", (tasks / "BLOCKED/preflight.md").read_text())
            self.assertIn("Brief revision: 2", (tasks / "STALE/brief.md").read_text())
            self.assertIn("Source brief revision: 1", (tasks / "STALE/preflight.md").read_text())
            self.assertNotIn("HEAD:", (tasks / "STALE/preflight.md").read_text())
            self.assertIn("Source brief: docs/tasks/OTHER/brief.md", (tasks / "FOREIGN/verification.md").read_text())
            self.assertIn("Verification revision: 2", (tasks / "REVMISMATCH/verification.md").read_text())
            self.assertIn("Verification revision: 1", (tasks / "REVMISMATCH/preflight.md").read_text())
            self.assertIn("docs/tasks/W-32/brief.md", (tasks / "WRONGSCOPE/preflight.md").read_text())
            self.assertIn("Task kind: composite", (tasks / "COMPOSITE/brief.md").read_text())
            self.assertIn("Status: decomposed", (tasks / "COMPOSITE/brief.md").read_text())
            self.assertTrue((tasks / "index.json").is_file())
            self.assertFalse((tasks / "COMPOSITE/index.json").exists())
            self.assertIn('"T-C1"', (tasks / "index.json").read_text())
            self.assertIn("Status: blocked", (tasks / "BLOCKEDDESIGN/verification.md").read_text())
            self.assertTrue((tasks / "API-31.md").is_file())
            self.assertFalse((tasks / "API-31").exists())
            self.assertFalse((tasks / "DOCS/preflight.md").exists())
            self.assertIn("conversational direct request", (root / "requests/relabel.md").read_text())
            self.assertIn("no task package", (root / "requests/direct.md").read_text())


    def test_continuation_and_revision_fixtures_supply_distinct_states(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.fixture(temporary, "entry-cases")
            states = root / "transitions"
            for name in ("expected-implementation", "expected-report", "prerequisite", "ownership", "permission", "capability", "authority"):
                package = states / name / "docs/tasks/CURRENT"
                baseline = []
                for artifact in ("brief", "verification", "preflight"):
                    baseline.append(subprocess.check_output(
                        ["git", "show", f"HEAD:transitions/{name}/docs/tasks/CURRENT/{artifact}.md"],
                        cwd=root, text=True))
                self.assert_ready_preparation(*baseline, "docs/tasks/CURRENT")
                self.assertEqual(baseline[2], (package / "preflight.md").read_text())
                if name in ("prerequisite", "capability"):
                    tool = "tools/time_sdk.py" if name == "prerequisite" else "tools/secure_clock.py"
                    self.assertIn(tool, baseline[0])
                    self.assertIn(tool, baseline[2])
                self.assertIn("Verification revision: 1", (package / "verification.md").read_text(), name)
                self.assertIn("Verification design: docs/tasks/CURRENT/verification.md",
                              (package / "preflight.md").read_text(), name)
                baseline_verification = subprocess.run(
                    ["git", "show", f"HEAD:transitions/{name}/docs/tasks/CURRENT/verification.md"], cwd=root,
                    capture_output=True, text=True)
                self.assertEqual(0, baseline_verification.returncode,
                                 f"{name}: {baseline_verification.stderr}")
                self.assertIn("Verification revision: 1", baseline_verification.stdout, name)
            self.assertIn(" M src/session.py", subprocess.check_output(
                ["git", "status", "--short"], cwd=states / "expected-implementation", text=True))
            self.assertTrue((states / "expected-report/docs/tasks/CURRENT/result.md").exists())
            self.assertIn("tools/time_sdk.py", (states / "prerequisite/docs/tasks/CURRENT/brief.md").read_text())
            baseline_prerequisite = subprocess.run(
                ["git", "show", "HEAD:transitions/prerequisite/tools/time_sdk.py"], cwd=root,
                capture_output=True, text=True)
            self.assertEqual(0, baseline_prerequisite.returncode, baseline_prerequisite.stderr)
            self.assertFalse((states / "prerequisite/tools/time_sdk.py").exists())
            self.assertIn(" D transitions/prerequisite/tools/time_sdk.py", subprocess.check_output(
                ["git", "status", "--short"], cwd=root, text=True))
            self.assertIn("MM src/session.py", subprocess.check_output(
                ["git", "status", "--short"], cwd=states / "ownership", text=True))
            self.assertIn("revoked", (states / "permission/policy.md").read_text())
            for name, path, before, after in (
                ("permission", "policy.md", "Local writes allowed", "Local writes revoked"),
                ("authority", "direction.md", "Direction revision 1", "Direction revision 2"),
            ):
                baseline = subprocess.check_output(
                    ["git", "show", f"HEAD:transitions/{name}/{path}"], cwd=root, text=True)
                self.assertIn(before, baseline)
                self.assertIn(after, (states / name / path).read_text())
                self.assertIn(path, (states / name / "docs/tasks/CURRENT/preflight.md").read_text())
            self.assertIn("tools/secure_clock.py", (states / "capability/docs/tasks/CURRENT/brief.md").read_text())
            baseline_capability = subprocess.run(
                ["git", "show", "HEAD:transitions/capability/tools/secure_clock.py"], cwd=root,
                capture_output=True, text=True)
            self.assertEqual(0, baseline_capability.returncode, baseline_capability.stderr)
            self.assertFalse((states / "capability/tools/secure_clock.py").exists())
            self.assertIn(" D transitions/capability/tools/secure_clock.py", subprocess.check_output(
                ["git", "status", "--short"], cwd=root, text=True))
            self.assertIn("Authority revision: 1", (states / "authority/docs/tasks/CURRENT/preflight.md").read_text())
            self.assertIn("revision 2", (states / "authority/direction.md").read_text())
            for name, changed in (
                ("expected-implementation", "src/session.py"),
                ("expected-report", "docs/tasks/CURRENT/result.md"),
                ("prerequisite", "tools/time_sdk.py"), ("ownership", "src/session.py"),
                ("permission", "policy.md"), ("capability", "tools/secure_clock.py"),
                ("authority", "direction.md"),
            ):
                status = subprocess.check_output(
                    ["git", "status", "--short", "--untracked-files=all", "--", f"transitions/{name}/"],
                    cwd=root, text=True)
                self.assertEqual([f"transitions/{name}/{changed}"],
                                 [line[3:] for line in status.splitlines()], name)
            revised = root / "docs/tasks/REVISED"
            for folder, verification_revision, preflight_revision in (
                ("old", "2", "1"), ("refreshed", "2", "2"), ("old-again", "2", "1"),
            ):
                baseline = [subprocess.check_output(
                    ["git", "show", f"HEAD:docs/tasks/REVISED/{folder}/{artifact}.md"], cwd=root, text=True)
                    for artifact in ("brief", "verification", "preflight")]
                self.assert_ready_preparation(*baseline, f"docs/tasks/REVISED/{folder}")
                self.assertEqual(baseline[0], (revised / folder / "brief.md").read_text())
                self.assertNotEqual(baseline[1], (revised / folder / "verification.md").read_text())
                if folder != "refreshed":
                    self.assertEqual(baseline[2], (revised / folder / "preflight.md").read_text())
                else:
                    self.assertEqual(baseline[2].replace("Verification revision: 1", "Verification revision: 2"),
                                     (revised / folder / "preflight.md").read_text())
                self.assertIn(f"Verification revision: {verification_revision}",
                              (revised / folder / "verification.md").read_text(), folder)
                self.assertIn(f"Verification revision: {preflight_revision}",
                              (revised / folder / "preflight.md").read_text(), folder)
            self.assertIn("Coverage revision under unchanged authority",
                          (revised / "refreshed/verification.md").read_text())


    def test_evidence_ledgers_supply_complete_and_defective_states(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.fixture(temporary, "entry-cases")
            boundary = subprocess.run([sys.executable, "-m", "unittest", "tests.test_boundary"], cwd=root,
                                      env=os.environ | {"PYTHONDONTWRITEBYTECODE": "1"},
                                      capture_output=True, text=True)
            self.assertEqual(0, boundary.returncode, boundary.stderr)
            negative = subprocess.run([sys.executable, "-m", "unittest", "tests.test_negative"], cwd=root,
                                      env=os.environ | {"PYTHONDONTWRITEBYTECODE": "1"},
                                      capture_output=True, text=True)
            self.assertNotEqual(0, negative.returncode)
            self.assertIn("AssertionError", negative.stderr)
            self.assertTrue((root / "docs/tasks/EVIDENCE/preflight.md").is_file())
            self.assertIn("Verification revision: 2", (root / "docs/tasks/EVIDENCE/verification.md").read_text())
            self.assertIn("Verification revision: 1", (root / "docs/tasks/EVIDENCE/verification-v1.md").read_text())
            evidence = root / "evidence"
            complete = (evidence / "ledger-complete.md").read_text()
            for marker in ("V-01 — passed", "command: python -m unittest tests.test_boundary",
                           "oracle: positive boundary assert holds", "result: ok",
                           "V-02 — failed", "command: python -m unittest tests.test_negative",
                           "oracle: negative boundary assert rejects", "result: AssertionError reproduced",
                           "V-03 — blocked", "next owner: task-preflight",
                           "V-04 — unchecked", "next owner: fresh task-review-discovery evidence, then a separate fresh task-acceptance-review decision",
                           "Context reference: docs/tasks/EVIDENCE/preflight.md",
                           "Remaining obligations:", "Verification revision: 2"):
                self.assertIn(marker, complete)
            unresolved = set(re.findall(r"^(V-\d+) — (?:failed|blocked|unchecked)", complete, re.MULTILINE))
            obligations = complete.split("Remaining obligations:", 1)[1]
            self.assertEqual({"V-02", "V-03", "V-04"}, unresolved)
            self.assertEqual(unresolved, set(re.findall(r"V-\d+", obligations)))
            self.assertNotIn("none", obligations)
            for row in obligations.strip().splitlines():
                self.assertIn("next owner:", row)
            green_gap = (evidence / "ledger-green-gap.md").read_text()
            self.assertIn("All tests green", green_gap)
            self.assertIn("Omitted negative scenario V-02", green_gap)
            self.assertNotIn("V-02 — failed", green_gap)
            self.assertIn("docs/tasks/EVIDENCE/verification.md", green_gap)
            self.assertIn("Authoritative AC mapping", green_gap)
            self.assertIn("AC-02 <- V-02", green_gap)
            obsolete = (evidence / "ledger-obsolete.md").read_text()
            self.assertIn("Evidence verification revision: 1", obsolete)
            self.assertIn("Current authoritative revision: 2", obsolete)
            self.assertIn("collected before", obsolete)
            self.assertIn("docs/tasks/EVIDENCE/verification.md", obsolete)
            self.assertIn("Authoritative AC mapping", obsolete)
            self.assertIn("AC-01 <- V-01", obsolete)


    def test_route_cases_map_supplied_policy_and_stage_state_to_expected_routes(self):
        skill = " ".join((IMPLEMENTER / "SKILL.md").read_text(encoding="utf-8").split())
        self.assertIn("Name the complete ordered submission route", skill)
        section = skill.split(
            "Name the complete ordered submission route", 1
        )[1].split("## Preserve review provenance", 1)[0]
        with tempfile.TemporaryDirectory() as temporary:
            tasks = self.fixture(temporary, "route-cases") / "docs/tasks"
            self.assertEqual(set(ROUTE_CASE_ROUTES),
                             {path.name for path in tasks.iterdir()})
            for case_id, expected in ROUTE_CASE_ROUTES.items():
                with self.subTest(case=case_id):
                    package = tasks / case_id
                    brief = (package / "brief.md").read_text(encoding="utf-8")
                    verification = (package / "verification.md").read_text(encoding="utf-8")
                    preflight = (package / "preflight.md").read_text(encoding="utf-8")
                    self.assertIn("Task kind: executable", brief)
                    self.assertIn("Status: ready", brief)
                    self.assertIn("Status: ready", verification)
                    self.assertIn(f"Source brief: docs/tasks/{case_id}/brief.md", verification)
                    self.assertIn("Verification revision: 1", verification)
                    self.assertIn("Status: ready", preflight)
                    self.assertIn(f"Source brief: docs/tasks/{case_id}/brief.md", preflight)
                    self.assertIn("Verification revision: 1", preflight)
                    policy = preflight.split("Conditional-stage policy: ", 1)[1].splitlines()[0]
                    evidence = preflight.split("Conditional-stage evidence: ", 1)[1].splitlines()[0]
                    route = preflight.split("Expected submission route: ", 1)[1].splitlines()[0]
                    self.assertEqual(expected, route)
                    self.assertTrue(
                        "current" in evidence or "stale" in evidence
                        or "no applicable" in evidence, evidence
                    )
                    for label, applies_marker, complete_marker, route_part in ROUTE_STAGE_RULES:
                        segment = next(
                            (part.strip() for part in evidence.split(";")
                             if complete_marker in part),
                            "",
                        )
                        if not segment:
                            state = "missing"
                            applicable = False
                        elif "current" in segment:
                            state = "current"
                            applicable = (
                                "inapplicable" not in segment
                                and (
                                    "applicable to the submitted scope" in segment
                                    or "for the corrected scope" in segment
                                )
                            )
                        else:
                            state = "stale"
                            applicable = False
                        applies = applies_marker in policy
                        owes = applies and not (state == "current" and applicable)
                        self.assertEqual(
                            route_part in route,
                            owes,
                            f"{case_id}: {label} ({state}, applicable={applicable}) from policy/evidence into route",
                        )
                        if state == "current":
                            self.assertTrue(
                                applies,
                                f"{case_id}: {label} claims current completion but does not apply",
                            )
                    positions = [
                        section.index(ROUTE_PART_TOKENS[part.strip()])
                        for part in route.split(" → ")
                    ]
                    self.assertEqual(positions, sorted(positions), route)
                    review = package / "reviews/acceptance-01.md"
                    if case_id.startswith("CORR-"):
                        self.assertTrue(review.is_file())
                        report = review.read_text(encoding="utf-8")
                        self.assertIn("Preceding verdict: CHANGES_REQUESTED", report)
                        self.assertIn("Changed scope:", report)
                        self.assertIn("Affected prior evidence:", report)
                        self.assertIn("first outstanding applicable conditional stage", report)
                    else:
                        self.assertFalse(review.exists())

    def test_review_condition_cases_supply_no_review_and_required_review_contrasts(self):
        skill = " ".join((IMPLEMENTER / "SKILL.md").read_text(encoding="utf-8").split())
        self.assertIn(
            "When independent functional review is not required, no route is imposed",
            skill,
        )
        self.assertIn(
            "The requirement, not the metadata label, decides the route",
            skill,
        )
        with tempfile.TemporaryDirectory() as temporary:
            tasks = self.fixture(temporary, "review-cases") / "docs/tasks"
            noreview = tasks / "MILESTONE-NOREVIEW"
            brief = (noreview / "brief.md").read_text(encoding="utf-8")
            self.assertIn("review: milestone", brief)
            self.assertIn(
                "Review condition: no independent functional review is required",
                brief,
            )
            preflight = (noreview / "preflight.md").read_text(encoding="utf-8")
            self.assertIn(
                "Review condition: no independent functional review is required",
                preflight,
            )
            self.assertIn("no submission route is imposed", preflight)
            self.assertIn(
                "existing milestone result semantics are unchanged", preflight
            )
            self.assertNotIn("READY_FOR_REVIEW", preflight)
            required = tasks / "MILESTONE-REQUIRED"
            brief = (required / "brief.md").read_text(encoding="utf-8")
            self.assertIn("review: milestone", brief)
            self.assertIn(
                "independent functional review is explicitly required", brief
            )
            preflight = (required / "preflight.md").read_text(encoding="utf-8")
            self.assertIn(
                "Review condition: independent functional review is explicitly required",
                preflight,
            )
            self.assertIn(
                "Expected submission route: architecture gate → fresh maintainability review → registry updater → discovery → acceptance",
                preflight,
            )


    def test_guides_and_evals_agree_with_packaged_entry_and_evidence_contract(self):
        evals = json.loads((IMPLEMENTER / "evals/evals.json").read_text(encoding="utf-8"))["evals"]
        by_id = {case["id"]: case for case in evals}
        for case_id in (3, 5, 6, 8):
            with self.subTest(case_id=case_id):
                prompt = " ".join(by_id[case_id]["prompt"].split())
                expectations = " ".join(by_id[case_id]["expectations"])
                self.assertNotIn("intentionally no preflight packet", prompt)
                self.assertIn("preflight", prompt)
                self.assertIn("verification", prompt)
                self.assertIn("entry", expectations)
        self.assertIn("task-preflight", " ".join(by_id[8]["expectations"]))
        for path in (ROOT / "README.md", ROOT / "skills/README.md", FLOW / "README.md"):
            with self.subTest(guide=path.name):
                guide = " ".join(path.read_text(encoding="utf-8").split())
                self.assertIn("verifies current applicable readiness", guide)
                self.assertIn("maps every verification scenario ID", guide)



if __name__ == "__main__":
    unittest.main()
