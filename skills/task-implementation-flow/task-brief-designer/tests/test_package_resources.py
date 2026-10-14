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



if __name__ == "__main__":
    unittest.main()
