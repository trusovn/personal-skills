"""Senior-review discipline prerequisites shared by every review invocation.

The mandatory reference-read prerequisite and the completion-check
re-assertion of that read, read from the senior-review skill source.
"""

import unittest

from review_fixture_support import SENIOR_REVIEW_SKILL, normalized


class ReviewerDisciplineTests(unittest.TestCase):

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
