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


    def test_conditional_routes_load_before_actions_and_preserve_forms(self):
        skill = (CANONICAL / "SKILL.md").read_text(encoding="utf-8")
        flat = " ".join(skill.split())
        routes = {
            "references/task-sizing.yaml": "Before estimating",
            "references/task-artifact-layout.md": "Before creating or updating durable task artifacts",
            "references/task-brief-template.md": "Before assembling a durable executable brief",
            "references/decomposition.md": "After choosing a split, before writing any parent, child or structural index",
            "references/exceptional-output.md": "Before returning a direction-delta-needed or blocked-design response",
            "references/high-assurance.md": "Before assembling high-assurance fields or the addendum",
        }
        for relative, condition in routes.items():
            with self.subTest(reference=relative):
                self.assertIn(f"({relative})", skill)
                self.assertIn(condition, flat)
                self.assertTrue((CANONICAL / relative).is_file())
        self.assertIn("missing or unreadable", flat)
        self.assertIn("stop the affected action and report the exact gap", flat)
        self.assertIn("Do not read every reference at startup", flat)
        decomposition = " ".join((CANONICAL / "references/decomposition.md").read_text().split())
        for obligation in ("never a launch target", "Re-estimate every child independently",
                           "final executable integration child", "dependencies are acyclic",
                           "docs/tasks/index.json", "do not mutate `docs/task-map.json`",
                           "## Composite parent", "A composite has no launch metadata or readiness route"):
            self.assertIn(obligation, decomposition)
        exceptional = (CANONICAL / "references/exceptional-output.md").read_text()
        for obligation in ("# Direction delta needed:", "Owner action:",
                           "leave the requested task path absent or unchanged",
                           "# Design block:", "Status: `blocked_design`",
                           "Omit", "implementation handoff language"):
            self.assertIn(obligation, exceptional)
        strict = (CANONICAL / "references/high-assurance.md").read_text()
        for field in ("Artifact identity:", "Knowledge ledger:", "Verification requirements:",
                      "Legacy assumptions:", "Capability uncertainties:", "Machine/audit obligations:"):
            self.assertIn(field, strict)
        template = (CANONICAL / "references/task-brief-template.md").read_text()
        for reference in ("decomposition.md", "exceptional-output.md", "high-assurance.md"):
            self.assertIn(f"({reference})", template)
        self.assertNotIn("## Composite parent", template)
        self.assertNotIn("## Blocked design", template)
        self.assertNotIn("### High-assurance addendum", template)
        for obligation in ("never split automatically on the trigger alone",
                           "Respect explicit hard authority limits", "A risk section is optional",
                           "four scalar launch keys", "cannot imply same-session self-review"):
            self.assertIn(obligation, flat)


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
