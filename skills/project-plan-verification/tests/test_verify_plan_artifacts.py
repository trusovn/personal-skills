"""Exercise heading compatibility through the structural checker CLI."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SKILLS = Path(__file__).resolve().parents[2]
CHECKER = SKILLS / "project-plan-verification/scripts/verify_plan_artifacts.py"
TEMPLATE = SKILLS / "project-delivery-plan/references/project-plan-template.md"
HEADING_PAIRS = (
    ("Lifecycle and decision rules", "Lifecycle/state models"),
    ("End-to-end flows", "End-to-end data/process/state flows"),
    ("Risks, assumptions and delegated choices", "Risks, assumptions, and delegated choices"),
)


class PlanHeadingTests(unittest.TestCase):
    def check_plan(self, plan):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "plan.md").write_text(plan)
            task_map = {"schema_version": "1.0"}
            for section in ("capabilities", "artifacts", "interfaces", "invariants", "flows", "tasks"):
                task_map[section] = []
            (root / "map.json").write_text(json.dumps(task_map))
            return subprocess.run(
                [sys.executable, str(CHECKER), str(root / "plan.md"), str(root / "map.json")],
                capture_output=True, text=True,
            )

    def test_template_uses_preferred_headings(self):
        template = TEMPLATE.read_text()
        for preferred, _ in HEADING_PAIRS:
            self.assertIn(preferred, template)

    def test_preferred_legacy_and_mixed_headings_pass(self):
        preferred_plan = TEMPLATE.read_text()
        for preferred, legacy in HEADING_PAIRS:
            preferred_plan = preferred_plan.replace(legacy, preferred)
        variants = [preferred_plan]
        for preferred, legacy in HEADING_PAIRS:
            variants.append(preferred_plan.replace(preferred, legacy))
        legacy_plan = preferred_plan
        for preferred, legacy in HEADING_PAIRS:
            legacy_plan = legacy_plan.replace(preferred, legacy)
        variants.append(legacy_plan)
        for index, plan in enumerate(variants):
            with self.subTest(variant=index):
                result = self.check_plan(plan)
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)
                self.assertIn("PASS:", result.stdout)

    def test_missing_section_still_fails(self):
        template = TEMPLATE.read_text()
        for preferred, legacy in HEADING_PAIRS:
            with self.subTest(section=preferred):
                plan = template.replace(legacy, preferred).replace(preferred, "Unrelated section")
                result = self.check_plan(plan)
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn("project plan missing heading:", result.stdout)


if __name__ == "__main__":
    unittest.main()
