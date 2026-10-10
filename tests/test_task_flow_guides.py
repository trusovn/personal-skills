"""Composed flow-guide checks: discovery before separate acceptance decisions.

Every affected overview must show fresh discovery before the separate
independent acceptance decision, coordinator recording before authorized
continuation, and no wording that lets one session accept itself or skip
discovery. Role-reasoning guidance adds no launcher adapter, fifth metadata
key, or observed-runtime claim.
"""

import json
import unittest

from review_fixture_support import ROOT, normalized

ROOT_README = ROOT / "README.md"
PROFILE_GUIDE = ROOT / "skills" / "README.md"
FLOW_README = ROOT / "skills" / "task-implementation-flow" / "README.md"
BOUNDED_IMPLEMENTER_SKILL = (
    ROOT / "skills" / "task-implementation-flow" / "bounded-task-implementer" / "SKILL.md"
)
MAINTAINABILITY_SKILL = (
    ROOT / "skills" / "task-implementation-flow" / "task-maintainability-review" / "SKILL.md"
)
REGISTRY_UPDATER_SKILL = (
    ROOT / "skills" / "task-implementation-flow" / "task-contract-registry-updater" / "SKILL.md"
)
DESIGNER_SKILL = (
    ROOT / "skills" / "task-implementation-flow" / "task-brief-designer" / "SKILL.md"
)
DESIGNER_TEMPLATE = (
    ROOT
    / "skills"
    / "task-implementation-flow"
    / "task-brief-designer"
    / "references"
    / "task-brief-template.md"
)
IMPLEMENTER_EVALS = (
    ROOT / "skills" / "task-implementation-flow" / "bounded-task-implementer" / "evals" / "evals.json"
)
IMPLEMENTER_FIXTURE = (
    ROOT
    / "skills"
    / "task-implementation-flow"
    / "bounded-task-implementer"
    / "evals"
    / "files"
    / "setup_fixture.py"
)


def fenced_blocks(text: str) -> list:
    blocks: list = []
    current: list | None = None
    for line in text.splitlines():
        if current is None:
            if line.lstrip().startswith("```"):
                current = []
        elif line.lstrip().startswith("```"):
            blocks.append("\n".join(current))
            current = None
        else:
            current.append(line)
    return blocks



class ComposedReviewFlowGuideTests(unittest.TestCase):
    """Fail-first checks for the composed functional-review route guidance.

    Every affected overview must show fresh discovery before the separate
    independent acceptance decision, coordinator recording before authorized
    continuation, and no wording that lets one session accept itself or skip
    discovery. Role-reasoning guidance adds no launcher adapter, fifth
    metadata key, or observed-runtime claim.
    """

    def test_root_readme_route_shows_discovery_before_separate_acceptance(self):
        text = ROOT_README.read_text(encoding="utf-8")
        route = next(
            block
            for block in fenced_blocks(text)
            if "bounded-task-implementer" in block and "task-acceptance-review" in block
        )
        self.assertIn("task-review-discovery", route)
        self.assertLess(
            route.index("task-review-discovery"),
            route.index("task-acceptance-review"),
        )
        self.assertIn("coordinator recording", route)
        self.assertNotIn("admits discovery evidence when the flow splits it", text)


    def test_root_readme_contract_sequence_includes_independent_review_discovery(self):
        text = ROOT_README.read_text(encoding="utf-8")
        block = next(
            block
            for block in fenced_blocks(text)
            if "contract-registry synchronization" in block
        )
        self.assertIn("independent review discovery", block)
        self.assertLess(
            block.index("independent review discovery"),
            block.index("acceptance review"),
        )


    def test_profile_guide_task_route_requires_discovery_evidence(self):
        text = PROFILE_GUIDE.read_text(encoding="utf-8")
        route = next(
            block
            for block in fenced_blocks(text)
            if "bounded-task-implementer" in block and "task-acceptance-review" in block
        )
        self.assertIn("task-review-discovery", route)
        self.assertLess(
            route.index("task-review-discovery"),
            route.index("task-acceptance-review"),
        )
        self.assertIn("coordinator recording", route)
        self.assertNotIn("when evidence is published separately", text)


    def test_flow_readme_guided_route_and_layout_include_discovery(self):
        text = FLOW_README.read_text(encoding="utf-8")
        guided = next(
            block
            for block in fenced_blocks(text)
            if "required task-verification-designer for an executable task package"
            in block
        )
        self.assertIn("task-review-discovery", guided)
        self.assertLess(
            guided.index("task-review-discovery"),
            guided.index("functional acceptance"),
        )
        self.assertIn("coordinator recording", guided)
        layout = next(
            block for block in fenced_blocks(text) if "docs/tasks/" in block
        )
        self.assertIn("discovery-01.md", layout)


    def test_flow_readme_maintainability_gated_route_shows_discovery(self):
        text = FLOW_README.read_text(encoding="utf-8")
        gated = next(
            block
            for block in fenced_blocks(text)
            if "canonical deterministic architecture gate" in block
        )
        self.assertIn("task-review-discovery", gated)
        self.assertLess(
            gated.index("task-review-discovery"),
            gated.index("acceptance review"),
        )
        flat = normalized(FLOW_README)
        self.assertIn(
            "fresh maintainability reviewer before re-entering fresh discovery evidence and functional acceptance",
            flat,
        )
        self.assertNotIn("when discovery published its evidence separately", flat)
        self.assertIn("hand the fresh discovery report to the decision call", flat)


    def test_contract_aware_sequences_route_discovery_before_acceptance(self):
        for path in (FLOW_README, REGISTRY_UPDATER_SKILL):
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path):
                block = next(
                    block
                    for block in fenced_blocks(text)
                    if "task-contract-registry-updater" in block and "task brief" in block
                )
                self.assertIn("-> task-review-discovery", block)
                self.assertLess(
                    block.index("task-review-discovery"),
                    block.index("task-acceptance-review"),
                )


    def test_child_handoffs_name_discovery_before_the_acceptance_decision(self):
        implementer = normalized(BOUNDED_IMPLEMENTER_SKILL)
        self.assertIn(
            "Completed work routes to fresh independent `task-review-discovery` evidence and a separate fresh `task-acceptance-review` decision when independent review is requested or required",
            implementer,
        )
        self.assertIn(
            "Loading, quoting, or following `task-review-discovery` or `task-acceptance-review` in the current session",
            implementer,
        )
        self.assertIn(
            "exactly name fresh independent `task-review-discovery` evidence and the separate fresh `task-acceptance-review` decision as next owner",
            implementer,
        )
        self.assertNotIn("route to a fresh `task-acceptance-review`.", implementer)

        maintainability = normalized(MAINTAINABILITY_SKILL)
        self.assertIn(
            "proceed to fresh independent `task-review-discovery` evidence and the separate functional `task-acceptance-review` decision when that stage is required",
            maintainability,
        )
        self.assertIn(
            "repeat architecture gate + fresh maintainability review before fresh discovery evidence and fresh functional acceptance",
            maintainability,
        )


    def test_discovery_is_mandatory_whenever_independent_functional_review_runs(self):
        text = FLOW_README.read_text(encoding="utf-8")
        flat = normalized(FLOW_README)
        self.assertNotIn(
            "The flow does not split discovery from the acceptance decision", text
        )
        self.assertNotIn("When the flow splits evidence from the decision", flat)
        self.assertNotIn("when metadata or risk calls for it", flat)
        self.assertIn("Whenever independent functional review is required", flat)
        self.assertIn("never runs without that discovery evidence", flat)
        # The legitimate skip is functional review itself not being required.
        self.assertIn(
            "does not need independent functional review under its metadata or risk",
            text,
        )


    def test_brief_designer_follow_on_prescribes_discovery_then_acceptance(self):
        follow_on = (
            "hand the completed bytes to a fresh independent "
            "`task-review-discovery` call, and hand its report to a separate "
            "`task-acceptance-review` decision"
        )
        designer = normalized(DESIGNER_SKILL)
        self.assertIn("any applicable conditional stages", designer)
        self.assertIn(follow_on, designer)
        self.assertIn(
            "through applicable conditional stages and fresh independent "
            "`task-review-discovery` evidence to the separate "
            "`task-acceptance-review` decision",
            designer,
        )
        self.assertIn("does not state independent acceptance", designer)
        template = normalized(DESIGNER_TEMPLATE)
        self.assertIn("any applicable conditional stages", template)
        self.assertIn(follow_on, template)
        self.assertIn(
            "Do not use same-session self-review as that discovery or acceptance step",
            template,
        )
        self.assertNotIn("fresh independent acceptance reviewer", designer + template)


    def test_implementer_eval_mirrors_route_discovery_before_acceptance(self):
        evals = json.loads(IMPLEMENTER_EVALS.read_text(encoding="utf-8"))["evals"]
        by_id = {case["id"]: case for case in evals}
        for case_id in (1, 5):
            blob = json.dumps(by_id[case_id])
            self.assertIn("task-review-discovery", blob)
            self.assertLess(
                blob.index("task-review-discovery"),
                blob.index("task-acceptance-review"),
            )
        fixture = IMPLEMENTER_FIXTURE.read_text(encoding="utf-8")
        for stale in (
            "Next route after complete: task-acceptance-review.",
            "hand the current bytes to a fresh acceptance reviewer",
            "names fresh task-acceptance-review as next owner",
            "next owner: fresh task-acceptance-review",
            "then fresh task-acceptance-review.",
        ):
            self.assertNotIn(stale, fixture)
        self.assertIn(
            "Next route after complete: fresh task-review-discovery evidence, "
            "then a separate fresh task-acceptance-review decision",
            fixture,
        )


    def test_role_reasoning_guidance_adds_no_adapter_fifth_key_or_runtime_claim(self):
        text = FLOW_README.read_text(encoding="utf-8")
        metadata = next(
            block for block in fenced_blocks(text) if "agent_tier:" in block
        )
        keys = {
            line.split(":")[0].strip()
            for line in metadata.splitlines()
            if ":" in line and "->" not in line
        }
        self.assertEqual({"agent_tier", "reasoning", "review", "budget"}, keys)
        flat = normalized(FLOW_README)
        self.assertIn(
            "A high reasoning tier is recommended for discovery",
            flat,
        )
        self.assertIn(
            "an equally high tier is recommended for the separate acceptance decision",
            flat,
        )
        self.assertIn(
            "launch tooling enforces neither the separate-call roles nor the reasoning recommendations",
            flat,
        )
        self.assertIn(
            "intended launch guidance, not claims about the eventual runtime configuration",
            flat,
        )



if __name__ == "__main__":
    unittest.main()
