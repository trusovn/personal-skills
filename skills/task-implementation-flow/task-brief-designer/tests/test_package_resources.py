from pathlib import Path
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
        for skill_name in ("bounded-task-implementer", "task-preflight"):
            skill = (FLOW / skill_name / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("Task kind: composite", skill)
            self.assertIn("Status: decomposed", skill)
            self.assertIn("docs/tasks/index.json", skill)
            self.assertIn("dependency-ready executable leaf", skill)


if __name__ == "__main__":
    unittest.main()
