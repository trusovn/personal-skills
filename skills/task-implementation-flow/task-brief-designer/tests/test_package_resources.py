import json
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
        self.assertIn("verification-design artifact", preflight)
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
