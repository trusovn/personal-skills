import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ACCEPTANCE_SKILL = (
    ROOT
    / "skills"
    / "task-implementation-flow"
    / "task-acceptance-review"
    / "SKILL.md"
)
SENIOR_REVIEW_SKILL = ROOT / "skills" / "senior-code-review" / "SKILL.md"


def normalized(path: Path) -> str:
    return re.sub(r"\s+", " ", path.read_text(encoding="utf-8")).strip()


class ReviewerDisciplineTests(unittest.TestCase):
    def test_acceptance_review_requires_real_schema_validator_probes(self):
        text = normalized(ACCEPTANCE_SKILL)

        self.assertIn(
            "When a required/material row depends on a machine-readable schema or other executable validator contract",
            text,
        )
        self.assertIn("independently exercise that validator", text)
        self.assertIn("at least one instance that should be valid", text)
        self.assertIn("one deliberately invalid instance", text)
        self.assertIn("targets the changed or acceptance-relevant constraint", text)
        self.assertIn("schema's declared draft", text)
        self.assertIn("Draft 2020-12", text)

    def test_unexercised_required_schema_boundary_cannot_support_accept(self):
        text = normalized(ACCEPTANCE_SKILL)

        self.assertIn(
            "keep that ledger row `blocked` or `unchecked` with the concrete reason; it cannot support `ACCEPT`",
            text,
        )
        self.assertIn(
            "otherwise its row remains blocked/unchecked and cannot support `ACCEPT`",
            text,
        )

    def test_acceptance_review_rejects_static_or_producer_side_schema_substitutes(self):
        text = normalized(ACCEPTANCE_SKILL)

        self.assertIn("schema text", text)
        self.assertIn("producer-side validation", text)
        self.assertIn("deserialization", text)
        self.assertIn("unrelated passing suite", text)

    def test_senior_review_reference_read_is_an_early_mandatory_prerequisite(self):
        text = normalized(SENIOR_REVIEW_SKILL)

        self.assertIn(
            "Before substantive review reasoning, candidate-finding generation, or dimension selection",
            text,
        )
        self.assertIn("read [references/review-dimensions.md](references/review-dimensions.md)", text)
        self.assertIn("mandatory prerequisite for every invocation", text)

    def test_senior_review_completion_check_reasserts_reference_read(self):
        text = normalized(SENIOR_REVIEW_SKILL)

        self.assertIn("## Completion check", text)
        self.assertIn(
            "`references/review-dimensions.md` was read in this invocation before substantive review reasoning",
            text,
        )
        self.assertIn("every dimension relevant to the scoped change was considered", text)


if __name__ == "__main__":
    unittest.main()
