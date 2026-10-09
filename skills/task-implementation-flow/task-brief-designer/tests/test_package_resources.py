import json
import hashlib
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[4]
CANONICAL = ROOT / "skills/task-implementation-flow/task-brief-designer"
FLOW = ROOT / "skills/task-implementation-flow"
PACKAGED_RESOURCES = (
    "references/task-sizing.yaml",
    "references/task-artifact-layout.md",
)


class PreflightContractTest(unittest.TestCase):
    def fixture(self, temporary, scenario):
        setup = FLOW / "task-preflight/evals/files/setup_fixture.py"
        subprocess.run([sys.executable, str(setup), scenario], cwd=ROOT,
                       env=os.environ | {"EVAL_WORK_ROOT": temporary}, check=True)
        return Path(temporary) / scenario

    def test_readiness_fixture_supplies_independent_defects_and_feasible_future_test(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.fixture(temporary, "readiness-cases")
            tasks = root / "docs/tasks"
            self.assertFalse((root / "tests/test_future.py").exists())
            self.assertFalse((root / "tools/secure_clock.py").exists())
            self.assertFalse((tasks / "MISSING/verification.md").exists())
            self.assertIn("Source brief: docs/tasks/VALID/brief.md", (tasks / "FOREIGN/verification.md").read_text())
            self.assertNotIn("AC-02", (tasks / "OMITTED/verification.md").read_text())
            self.assertIn("remote OAuth", (tasks / "UNSUPPORTED/verification.md").read_text())
            self.assertNotIn("OAuth", (root / "docs/direction.md").read_text())
            self.assertIn("assert only that", (tasks / "WEAK/verification.md").read_text())
            for task_id, fact in (("CAPABILITY", "outside allowed scope"),
                                  ("DEPENDENCY", "not installed"),
                                  ("PERMISSION", "policy prohibits network")):
                for artifact in ("brief.md", "verification.md"):
                    self.assertIn(fact, (tasks / task_id / artifact).read_text())
            self.assertIn("inline readiness", (root / "requests/direct.md").read_text())
            baseline = subprocess.run(
                [sys.executable, "-m", "unittest", "tests.test_existing"], cwd=root,
                env=os.environ | {"PYTHONDONTWRITEBYTECODE": "1"}, capture_output=True, text=True)
            self.assertEqual(0, baseline.returncode, baseline.stderr)
            # Execute the available boundary/setup; the task-owned future test remains absent.
            boundary = subprocess.run([sys.executable, "-c",
                "from src.session import is_valid; s={'expires_at':100,'token':'keep'}; "
                "before=s.copy(); assert not is_valid(s,100); assert s==before; "
                "assert is_valid({'expires_at':101},100)"], cwd=root,
                env=os.environ | {"PYTHONDONTWRITEBYTECODE": "1"})
            self.assertEqual(0, boundary.returncode)
            self.assertEqual("", subprocess.check_output(["git", "status", "--short"], cwd=root, text=True))

    def test_revision_and_context_fixtures_preserve_supplied_contrasts(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.fixture(temporary, "revision-recovery")
            for task_id in ("FEASIBLE", "UNAVAILABLE"):
                package = root / f"docs/tasks/{task_id}"
                self.assertIn("Verification revision: 1", (package / "verification-v1.md").read_text())
                self.assertIn("Verification revision: 1", (package / "preflight.md").read_text())
                current = (package / "verification.md").read_text()
                self.assertIn("Verification revision: 2", current)
                for scenario_id in ("V-01", "V-02", "V-03"):
                    self.assertIn(scenario_id, current)
            self.assertNotIn("indispensable", (root / "docs/tasks/FEASIBLE/verification.md").read_text())
            self.assertIn("indispensable", (root / "docs/tasks/UNAVAILABLE/verification.md").read_text())
            self.assertFalse((root / "tools/secure_clock.py").exists())
            self.assertEqual({"expected-implementation", "expected-report", "authority", "prerequisite",
                              "ownership", "permission", "capability", "requirement"},
                             {path.stem for path in (root / "transitions").glob("*.md")})
            self.assertEqual("", subprocess.check_output(
                ["git", "diff", "--", "src", "tests", "docs/direction.md"], cwd=root, text=True))
            states = root / "transitions"
            self.assertFalse((states / "prerequisite/vendor/time_sdk.py").exists())
            self.assertFalse((states / "capability/tools/secure_clock.py").exists())
            self.assertIn("revoked", (states / "permission/policy.md").read_text())
            self.assertIn("revision 2", (states / "authority/docs/direction.md").read_text())
            self.assertIn("Proposed AC-03", (states / "requirement/docs/tasks/CURRENT/brief.md").read_text())
            self.assertIn("MM src/session.py", subprocess.check_output(
                ["git", "status", "--short"], cwd=states / "ownership", text=True))
            self.assertIn(" M src/session.py", subprocess.check_output(
                ["git", "status", "--short"], cwd=states / "expected-implementation", text=True))
            self.assertTrue((states / "expected-report/docs/tasks/CURRENT/result.md").exists())
            clock = subprocess.check_output([sys.executable, "tools/secure_clock.py"],
                cwd=states / "expected-report", env=os.environ | {"PYTHONDONTWRITEBYTECODE": "1"}, text=True)
            self.assertEqual("100\n", clock)
            context_root = self.fixture(temporary, "readiness-context")
            for task_id, fact in (
                ("RELEVANT", "KI-01"), ("UNRELATED", "KI-02"), ("NONE", "No recorded"),
                ("ORDINARY", "Unknown business detail"), ("DELAY-RESOLVED", "Authority resolves"),
                ("DELAY-UNRESOLVED", "Decision owner must answer"),
                ("REPAIR-RESOLVED", "Authority resolves"),
                ("REPAIR-UNRESOLVED", "Retention policy is not supplied"),
            ):
                package = context_root / f"docs/tasks/{task_id}"
                self.assertIn(fact, (package / "context.md").read_text())
                self.assertEqual(task_id in {"RELEVANT", "UNRELATED"}, (package / "known-issues.md").exists())
                self.assertIn("V-02 / AC-02", (package / "verification.md").read_text())
            for task_id in ("DELAY-UNRESOLVED", "REPAIR-UNRESOLVED"):
                package = context_root / f"docs/tasks/{task_id}"
                self.assertIn("Authority: context.md", (package / "brief.md").read_text())
                self.assertIn("not established", (package / "context.md").read_text())

    def test_freshness_fixture_has_same_status_but_different_nonpacket_bytes(self):
        with tempfile.TemporaryDirectory() as temporary:
            self.fixture(temporary, "freshness-change")
            root = Path(temporary) / "api"
            baseline = json.loads((Path(temporary) / "task-runs/freshness-baseline.json").read_text())
            status = subprocess.check_output(["git", "status", "--short"], cwd=root, text=True)
            self.assertEqual(baseline["status"], status)
            self.assertIn("MM src/auth/session.py", status)
            index = subprocess.check_output(["git", "show", ":src/auth/session.py"], cwd=root)
            self.assertEqual(baseline["index_sha256"], hashlib.sha256(index).hexdigest())
            self.assertNotEqual(baseline["worktree_sha256"], hashlib.sha256((root / "src/auth/session.py").read_bytes()).hexdigest())
            self.fixture(temporary, "queue-ready")
            root = Path(temporary) / "queue-runner"
            subprocess.run([sys.executable, "-c",
                "from pathlib import Path; from tests.helpers.queue_state import seed_queue; "
                "seed_queue(Path('state.json'))"], cwd=root,
                env=os.environ | {"PYTHONDONTWRITEBYTECODE": "1"}, check=True)
            state = root / "state.json"
            state_before = state.read_bytes()
            public = subprocess.run([sys.executable, "runner", "run-next", str(state)], cwd=root,
                env=os.environ | {"PYTHONDONTWRITEBYTECODE": "1"}, capture_output=True, text=True)
            self.assertNotEqual(0, public.returncode)
            self.assertIn("NotImplementedError", public.stderr)
            self.assertEqual(state_before, state.read_bytes())
            state.unlink()
            before = {str(p.relative_to(root)): p.read_bytes() for p in root.rglob("*")
                      if p.is_file() and ".git" not in p.relative_to(root).parts}
            packet = root / "docs/tasks/QR-12/preflight.md"
            packet.write_text("Status: ready\nFixture packet-only identity probe; not an agent readiness result.\n")
            self.assertEqual("?? docs/tasks/QR-12/preflight.md\n", subprocess.check_output(["git", "status", "--short", "--untracked-files=all"], cwd=root, text=True))
            for relative, content in before.items():
                self.assertEqual(content, (root / relative).read_bytes(), relative)

    def test_updated_existing_fixtures_keep_executable_prerequisites_and_negative_state(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.fixture(temporary, "api-routine")
            self.assertIn("Source brief: docs/tasks/API-07/brief.md",
                          (root / "docs/tasks/API-07/verification.md").read_text())
            self.assertIn("only docs/tasks/API-07/preflight.md", (root / "AGENTS.md").read_text())
            command = subprocess.run([sys.executable, "-m", "unittest",
                "tests.auth.test_session.SessionTest.test_unexpired_session_is_valid"], cwd=root,
                env=os.environ | {"PYTHONDONTWRITEBYTECODE": "1"}, capture_output=True, text=True)
            self.assertEqual(0, command.returncode, command.stderr)
            self.fixture(temporary, "queue-guided")
            root = Path(temporary) / "queue-runner"
            self.assertIn("Artifact status: ready\n", (root / "docs/tasks/QR-12/brief.md").read_text())
            self.assertTrue(os.access(root / "runner", os.X_OK))
            self.assertIn("seed_queue", (root / "tests/integration/test_run_next.py").read_text())
            self.fixture(temporary, "scheduler-missing")
            root = Path(temporary) / "scheduler"
            self.assertFalse((root / "tests/helpers/concurrent_claims.py").exists())
            self.assertIn("two real workers at a barrier", (root / "docs/tasks/SCH-09/verification.md").read_text())
            self.assertEqual("", subprocess.check_output(["git", "status", "--short"], cwd=root, text=True))

    def test_packaged_readiness_requires_complete_feasible_derived_coverage(self):
        skill = (FLOW / "task-preflight/SKILL.md").read_text(encoding="utf-8")
        guided = skill.split("### Guided", 1)[1].split("### High assurance", 1)[0]
        self.assertNotIn("Return a compact inline readiness result unless", guided)
        self.assertIn("require `verification.md`", guided)
        self.assertIn("canonical `preflight.md`", guided)
        for obligation in (
            "every material AC and scenario", "authority relationship", "setup",
            "decisive boundary", "command feasibility", "dependencies",
            "permissions", "ownership", "future test", "indispensable capability",
            "omitted AC", "unsupported scenario", "weak oracle",
        ):
            self.assertIn(obligation, skill)
        self.assertIn("does not claim that future behavior passed", skill)

    def test_context_revision_and_strict_freshness_are_distinct(self):
        skill = " ".join((FLOW / "task-preflight/SKILL.md").read_text(encoding="utf-8").split())
        packet = (FLOW / "task-preflight/references/execution-packet-template.md").read_text(encoding="utf-8")
        for obligation in (
            "operating envelope", "failure consequences", "business priorities",
            "required consumers", "planned changes", "mitigations", "unknowns",
            "relevant known issues", "no recorded deferrals", "reasonable assumptions",
            "serious consequences of delay", "materially costly later repair",
            "one focused question", "retain existing scenario IDs",
            "affected obsolete readiness", "focused preflight",
            "Expected implementation or report effects", "Changed requirements",
        ):
            self.assertIn(obligation, skill)
        for field in ("Source brief", "Verification revision", "Decision context", "Feasibility"):
            self.assertIn(field, packet)
        for unchanged in (
            "separate index-blob and worktree digests/states",
            "Any change beyond that one packet artifact",
            "any changed non-packet",
        ):
            self.assertIn(unchanged, skill)
        self.assertIn("even when short-status text is unchanged", packet)

    def test_guides_and_eval_prompts_require_durable_packaged_output(self):
        for path in (ROOT / "README.md", ROOT / "skills/README.md", FLOW / "README.md"):
            guide = path.read_text(encoding="utf-8")
            self.assertIn("verification revision", guide)
            self.assertIn("decision context", guide)
        evals = json.loads((FLOW / "task-preflight/evals/evals.json").read_text(encoding="utf-8"))["evals"]
        by_id = {case["id"]: case for case in evals}
        for case_id in (5, 6):
            prompt = by_id[case_id]["prompt"]
            package = {5: "QR-12", 6: "API-07"}[case_id]
            self.assertRegex(prompt, rf"(?i)\b(?:write|writing) only canonical docs/tasks/{package}/preflight\.md")
            self.assertIn("preflight.md", by_id[case_id]["expected_output"])
            self.assertNotIn("reports inline", " ".join(by_id[case_id]["expectations"]))
        for case in evals:
            with self.subTest(case_id=case["id"]):
                self.assertNotRegex(case["prompt"], r"(?i)\bor running (?:a )?(?:broad|aggregate) (?:test )?baseline")
        self.assertIn("running no broad test baseline", by_id[6]["prompt"])
        scenarios = {case["execution"]["setup"]["command"][-1] for case in evals if "execution" in case}
        self.assertTrue({"readiness-cases", "revision-recovery", "readiness-context", "freshness-change"} <= scenarios)


class TaskBriefDesignerPackageTest(unittest.TestCase):
    def test_canonical_package_contains_the_policy_resources_it_references(self):
        skill = (CANONICAL / "SKILL.md").read_text(encoding="utf-8")

        for relative_path in PACKAGED_RESOURCES:
            self.assertIn(f"`{relative_path}`", skill)
            resource = CANONICAL / relative_path
            self.assertTrue(resource.is_file(), resource)

    def test_readme_identifies_packaged_resources_as_authoritative(self):
        readme = (FLOW / "README.md").read_text(encoding="utf-8")

        for relative_path in PACKAGED_RESOURCES:
            self.assertIn(f"task-brief-designer/{relative_path}", readme)

    def test_sizing_policy_makes_the_maximum_boundary_exclusive(self):
        policy = (CANONICAL / "references/task-sizing.yaml").read_text(
            encoding="utf-8"
        )

        self.assertIn("comparison: split_only_when_greater_than_maximum", policy)

    def test_downstream_skills_refuse_decomposed_parents(self):
        for skill_name in (
            "bounded-task-implementer",
            "task-preflight",
            "task-verification-designer",
        ):
            skill = (FLOW / skill_name / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("Task kind: composite", skill)
            self.assertIn("Status: decomposed", skill)
            if skill_name != "task-verification-designer":
                self.assertIn("docs/tasks/index.json", skill)
                self.assertIn("dependency-ready executable leaf", skill)

    def test_verification_design_resources_are_discoverable(self):
        designer = (CANONICAL / "SKILL.md").read_text(encoding="utf-8")
        template = (CANONICAL / "references/task-brief-template.md").read_text(
            encoding="utf-8"
        )
        layout = (CANONICAL / "references/task-artifact-layout.md").read_text(
            encoding="utf-8"
        )
        implementer = (FLOW / "bounded-task-implementer" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        preflight = (FLOW / "task-preflight" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        packet_template = (
            FLOW
            / "task-preflight"
            / "references/execution-packet-template.md"
        ).read_text(encoding="utf-8")
        verification = (
            FLOW / "task-verification-designer" / "SKILL.md"
        ).read_text(encoding="utf-8")
        verification_evals = (
            FLOW / "task-verification-designer" / "evals/evals.json"
        )

        self.assertIn("task-verification-designer", designer)
        self.assertIn("Verification-design recommendation", template)
        self.assertIn("verification.md", layout)
        self.assertIn("verification.md", implementer)
        self.assertIn("verification-design bytes when present", implementer)
        self.assertIn("Require the executable package's `verification.md`", preflight)
        self.assertIn("| Verification design |", packet_template)
        self.assertIn("implementation-neutral", verification)
        self.assertIn("does **not** own verification design across sibling", verification)
        self.assertTrue(verification_evals.is_file(), verification_evals)

    def test_packaged_preparation_contract(self):
        designer = (CANONICAL / "SKILL.md").read_text(encoding="utf-8")
        template = (CANONICAL / "references/task-brief-template.md").read_text(
            encoding="utf-8"
        )
        layout = (CANONICAL / "references/task-artifact-layout.md").read_text(
            encoding="utf-8"
        )
        verification = (
            FLOW / "task-verification-designer" / "SKILL.md"
        ).read_text(encoding="utf-8")
        verification_evals = json.loads(
            (FLOW / "task-verification-designer" / "evals/evals.json").read_text(
                encoding="utf-8"
            )
        )["evals"]

        self.assertIn("A supplied executable task package always requires", designer)
        self.assertIn("derived `verification.md`,\nthen a ready `preflight.md`", designer)
        self.assertIn("derived `verification.md`, then ready", template)
        self.assertIn("For an executable task package, create derived", layout)
        self.assertIn("cannot use the conversational direct-edit exception", designer)
        self.assertIn("source brief and a revision", verification)
        self.assertIn("retain existing scenario IDs", verification)
        self.assertIn("focused preflight", verification)
        self.assertIn("routes to task design or the decision\nowner", verification)
        self.assertEqual(
            {"preparation-routes", "coverage-revision"},
            {
                case["execution"]["setup"]["command"][-1]
                for case in verification_evals
                if case["id"] in {4, 5}
            },
        )

    def test_packaged_preparation_evals_cover_every_scenario(self):
        verification = (
            FLOW / "task-verification-designer" / "SKILL.md"
        ).read_text(encoding="utf-8")
        readme = (FLOW / "README.md").read_text(encoding="utf-8")
        root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
        evals = json.loads(
            (FLOW / "task-verification-designer" / "evals/evals.json").read_text(
                encoding="utf-8"
            )
        )["evals"]
        fixture_by_id = {
            case["id"]: case["execution"]["setup"]["command"][-1]
            for case in evals
            if case["id"] in {4, 5, 6, 7, 8}
        }

        self.assertEqual(
            {
                4: "preparation-routes",
                5: "coverage-revision",
                6: "coverage-closure",
                7: "verification-conflicts",
                8: "workflow-scope",
            },
            fixture_by_id,
        )
        expectations_by_id = {
            case["id"]: "\n".join(case["expectations"])
            for case in evals
            if case["id"] in {4, 5, 6, 7, 8}
        }
        self.assertIn("ready preflight", expectations_by_id[4])
        self.assertIn("omitted AC", expectations_by_id[5])
        self.assertIn("unsupported scenario", expectations_by_id[6])
        self.assertIn("unchanged", expectations_by_id[7])
        self.assertIn("high-assurance", expectations_by_id[8])
        self.assertIn(
            "Every supplied executable task package uses this stage", verification
        )
        self.assertIn("required for a supplied executable task package", readme)
        self.assertIn("unpackaged conversational", root_readme)

    def test_packaged_preparation_fixtures_supply_discriminating_inputs(self):
        setup = FLOW / "task-verification-designer/evals/files/setup_fixture.py"
        expected_inputs = {
            "preparation-routes": ("docs/tasks/LEGACY.md", "Legacy task"),
            "coverage-revision": (
                "docs/tasks/REV-1/changed-requirement.md",
                "approved retention decision",
            ),
            "coverage-closure": (
                "docs/tasks/COV-WEAK/verification.md",
                "only that an export file exists",
            ),
            "verification-conflicts": (
                "docs/tasks/CONFLICT-FOREIGN/verification.md",
                "Preserve foreign declaration bytes.",
            ),
            "workflow-scope": (
                "requests/unpackaged-direct-edit.md",
                "Correct one heading",
            ),
        }

        with tempfile.TemporaryDirectory() as temporary:
            environment = os.environ | {"EVAL_WORK_ROOT": temporary}
            for scenario, (relative_path, expected_content) in expected_inputs.items():
                subprocess.run(
                    [sys.executable, str(setup), scenario],
                    check=True,
                    cwd=ROOT,
                    env=environment,
                )
                fixture_path = Path(temporary) / scenario / relative_path
                self.assertTrue(fixture_path.is_file(), fixture_path)
                self.assertIn(expected_content, fixture_path.read_text(encoding="utf-8"))

    def test_guided_readiness_routes_distinguish_packaged_from_unpackaged(self):
        designer = (CANONICAL / "SKILL.md").read_text(encoding="utf-8")
        guided_profile = designer.split("### Guided", 1)[1].split(
            "### High assurance", 1
        )[0]
        route_step = designer.split(
            "10. Give every durable brief one human-readable readiness route:", 1
        )[1].split("11. Explicitly classify", 1)[0]

        self.assertNotIn(
            "routine readiness route is implementer self-preflight",
            guided_profile,
        )
        self.assertIn(
            "readiness route is standalone guided preflight after derived",
            guided_profile,
        )
        self.assertIn(
            "Reserve implementer self-preflight for unpackaged", guided_profile
        )
        self.assertNotIn(
            "`implementer self-preflight` for routine guided work", route_step
        )
        self.assertIn(
            "`standalone guided preflight` for an executable task package",
            route_step,
        )
        self.assertIn(
            "`implementer self-preflight` only for an unpackaged conversational",
            route_step,
        )

    def test_active_skills_use_only_per_task_package_paths(self):
        excluded_parts = {"evaluations", "history"}
        active_files = [
            path
            for path in (ROOT / "skills").rglob("*")
            if path.is_file()
            and path != Path(__file__)
            and path.suffix in {".md", ".json", ".py"}
            and not excluded_parts.intersection(path.parts)
        ]

        violations = []
        for path in active_files:
            content = path.read_text(encoding="utf-8")
            for pattern in (
                re.compile(r"docs/tasks/verification\.md"),
                re.compile(r"docs/reviews/[A-Za-z0-9_.-]+\.md"),
                re.compile(r"beside the (?:executable )?task brief", re.IGNORECASE),
                re.compile(r"beside the brief", re.IGNORECASE),
            ):
                if pattern.search(content):
                    violations.append(f"{path.relative_to(ROOT)}: {pattern.pattern}")

        self.assertEqual([], violations, "\n".join(violations))

    def test_consumers_explicitly_refuse_direct_legacy_briefs(self):
        for skill_name in ("bounded-task-implementer", "task-preflight"):
            skill = (FLOW / skill_name / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("Refuse a direct legacy brief", skill)
            self.assertIn("even when no `verification.md` exists", skill)
            self.assertIn("task-brief-designer", skill)
            self.assertIn("package normalization", skill)

    def test_negative_behavioral_evals_cover_direct_legacy_briefs(self):
        for skill_name in ("bounded-task-implementer", "task-preflight"):
            path = FLOW / skill_name / "evals/evals.json"
            evals = json.loads(path.read_text(encoding="utf-8"))["evals"]
            matching = [case for case in evals if "docs/tasks/API-31.md" in case["prompt"]]
            self.assertEqual(1, len(matching), path)
            expectations = "\n".join(matching[0]["expectations"])
            self.assertIn("refuses", expectations)
            self.assertIn("normalization", expectations)

    def test_high_assurance_artifacts_use_package_paths(self):
        preflight = (FLOW / "task-preflight" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        packet = (
            FLOW / "task-preflight" / "references/execution-packet-template.md"
        ).read_text(encoding="utf-8")
        acceptance = (FLOW / "task-acceptance-review" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        maintainability = (
            FLOW / "task-maintainability-review" / "SKILL.md"
        ).read_text(encoding="utf-8")

        self.assertIn("package's `preflight.md`", preflight)
        self.assertIn("Post-write `git status --short`", packet)
        self.assertIn("reviews/acceptance-NN.md", acceptance)
        self.assertIn("reviews/maintainability-NN.md", maintainability)


if __name__ == "__main__":
    unittest.main()
