from pathlib import Path
import json
import re
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

    def test_optional_verification_design_is_discoverable(self):
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
