"""Package-local resource checks for the task-brief-designer package.

The designer's own policy resources and authoring route stay here and resolve
the package from this file's location, without assuming a source checkout or
any repository-test helper, so a copied or installed package can run this
suite on its own.
"""

import unittest
from pathlib import Path

CANONICAL = Path(__file__).resolve().parents[1]


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


    def test_sizing_policy_makes_the_maximum_boundary_exclusive(self):
        policy = (CANONICAL / "references/task-sizing.yaml").read_text(
            encoding="utf-8"
        )

        self.assertIn("comparison: split_only_when_greater_than_maximum", policy)


    def test_guided_readiness_routes_distinguish_packaged_from_unpackaged(self):
        designer = (CANONICAL / "SKILL.md").read_text(encoding="utf-8")
        preparation = " ".join(designer.split(
            "## Preparation and permission to start", 1
        )[1].split("## Load flow policy", 1)[0].split())
        self.assertIn(
            "A supplied executable task package always requires a derived "
            "`verification.md`, then a ready `preflight.md`, before implementation",
            preparation,
        )
        self.assertIn(
            "For an executable package, use `standalone guided preflight`",
            preparation,
        )
        self.assertIn(
            "Reserve `implementer self-preflight` for an unpackaged "
            "conversational direct edit",
            preparation,
        )



if __name__ == "__main__":
    unittest.main()
