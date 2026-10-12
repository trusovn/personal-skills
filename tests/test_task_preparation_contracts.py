"""Cross-skill preparation, resource, and legacy-path contract checks.

Designer-authored checks over shared preparation resources: package resource
authority, decomposition boundary quality, downstream refusal of decomposed
parents, verification-design discoverability, preparation contracts and evals,
per-task-package path hygiene, and direct-legacy-brief refusal.
"""

import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from review_fixture_support import FLOW, ROOT

CANONICAL = FLOW / "task-brief-designer"


PACKAGED_RESOURCES = (
    "references/task-sizing.yaml",
    "references/task-artifact-layout.md",
)



class TaskBriefDesignerPackageTest(unittest.TestCase):

    def test_readme_identifies_packaged_resources_as_authoritative(self):
        readme = (FLOW / "README.md").read_text(encoding="utf-8")

        for relative_path in PACKAGED_RESOURCES:
            self.assertIn(f"task-brief-designer/{relative_path}", readme)


    def test_decomposition_trigger_requires_boundary_quality_decision(self):
        skill = " ".join((CANONICAL / "SKILL.md").read_text(encoding="utf-8").split())
        contract = skill.split("## Sizing and decomposition contract", 1)[1].split(
            "## Finite-risk coverage contract", 1
        )[0]
        template = " ".join(
            (CANONICAL / "references/task-brief-template.md").read_text(
                encoding="utf-8"
            ).split()
        )
        policy = (CANONICAL / "references/task-sizing.yaml").read_text(encoding="utf-8")
        readme = " ".join((FLOW / "README.md").read_text(encoding="utf-8").split())
        evals = json.loads(
            (CANONICAL / "evals/evals.json").read_text(encoding="utf-8")
        )["evals"]
        by_id = {case["id"]: case for case in evals}

        self.assertNotIn("split by default", skill)
        for obligation in (
            "never split automatically on the trigger alone",
            "clear single ownership of each child outcome",
            "stable explicitly consumable handoffs",
            "independent implementation and verification per child",
            "shared edit/test surfaces",
            "likely contract renegotiation",
            "net delivery benefit including coordination and rework cost",
            "A component/layer split alone is not sufficient evidence",
            "even without strict atomicity",
            "candidate boundary considered",
            "residual execution risk",
            "Mere preference or high reasoning alone is insufficient",
            "Respect explicit hard authority limits",
        ):
            self.assertIn(obligation, contract)
        self.assertIn("candidate boundary considered", template)
        self.assertIn(
            "Do not present a trigger as automatically requiring decomposition",
            template,
        )
        self.assertIn("boundary-quality evaluation", policy)
        self.assertIn("boundary-quality gate", readme)
        self.assertIn("rather than an automatic split", readme)
        self.assertIn(
            "may remain one executable leaf when concrete coupling or "
            "coordination/rework costs favor keeping it whole",
            readme,
        )
        self.assertNotIn(
            "as requiring decomposition", " ".join(by_id[9]["expectations"])
        )
        self.assertIn(
            "triggering the boundary decision", " ".join(by_id[9]["expectations"])
        )
        self.assertIn(
            "boundary quality rather than the trigger or high reasoning alone",
            " ".join(by_id[11]["expectations"]),
        )


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


    def test_integration_leaf_composition_permission_keeps_refusal_boundaries(self):
        """INT-FLOW-001 I-05: an executable integration leaf may derive
        scenarios for its own composition ACs from supplied producer outputs;
        composite parents, invented sibling/system scope, and unavailable
        inputs/oracles stay refused. Rejects the old blanket composition
        refusal.
        """
        verification = (
            FLOW / "task-verification-designer" / "SKILL.md"
        ).read_text(encoding="utf-8")
        flat = " ".join(verification.split())
        self.assertIn(
            "An executable integration leaf is different: when its own "
            "explicit ACs require composing supplied producer outputs at "
            "stated consumer boundaries, derive task-local scenarios for "
            "exactly those composition ACs",
            flat,
        )
        self.assertIn("The leaf's brief and supplied inputs remain the authority", flat)
        self.assertIn("does **not** own verification design across sibling", flat)
        self.assertIn("route the request to its dependency-ready executable leaf", flat)
        self.assertIn(
            "do not invent or own a sibling task's requirements, system-wide "
            "integration strategy, or parent-level closure",
            flat,
        )
        self.assertIn("report the unavailable input or capability to its owner", flat)
        self.assertIn(
            "route an expected result the authority cannot settle to task "
            "design or the decision owner",
            flat,
        )
        self.assertIn("never fabricate a report or claim readiness to bypass the gap", flat)
        self.assertIn("Packaged preparation remains mandatory for that leaf", flat)
        self.assertNotIn(
            "If the supplied brief can only be verified by composing separate "
            "task outputs, report that limitation to the caller rather than "
            "inventing cross-task scenarios here",
            flat,
        )

    def test_integration_leaf_fixture_supplies_qualification_inputs(self):
        """INT-FLOW-001 I-05 / R-05: the staged integration-leaf scenario and
        eval case 9 give T-005 explicit briefs/inputs for the permission and
        refusal contrasts.
        """
        setup = FLOW / "task-verification-designer/evals/files/setup_fixture.py"
        with tempfile.TemporaryDirectory() as temporary:
            environment = os.environ | {"EVAL_WORK_ROOT": temporary}
            subprocess.run(
                [sys.executable, str(setup), "integration-leaf"],
                check=True,
                cwd=ROOT,
                env=environment,
            )
            root = Path(temporary) / "integration-leaf"
            leaf = (root / "docs/tasks/INT-9/brief.md").read_text(encoding="utf-8")
            self.assertIn("Task kind: executable", leaf)
            self.assertIn("supplied producer outputs", leaf)
            self.assertIn("AC-01", leaf)
            self.assertIn("AC-02", leaf)
            parent = (root / "docs/tasks/INT-PARENT/brief.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("Task kind: composite", parent)
            self.assertIn("Status: decomposed", parent)
            request = (root / "requests/integration-contrasts.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("Sibling requirement", request)
            self.assertIn("System-wide", request)
            self.assertIn("unavailable", request)
        evals = json.loads(
            (FLOW / "task-verification-designer" / "evals/evals.json").read_text(
                encoding="utf-8"
            )
        )["evals"]
        case = next(item for item in evals if item["id"] == 9)
        self.assertEqual(
            "integration-leaf", case["execution"]["setup"]["command"][-1]
        )
        expectations = " ".join(case["expectations"])
        self.assertIn("own composition ACs", expectations)
        self.assertIn("composite parent", expectations)
        self.assertIn("sibling", expectations)
        self.assertIn("fabricate", expectations)


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
        self.assertIn(
            "derived `verification.md`, then a ready `preflight.md`",
            " ".join(designer.split()),
        )
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
            "integration-leaf": (
                "docs/tasks/INT-9/brief.md",
                "supplied producer outputs",
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
