"""Static instruction routes; runner behavior remains in test_run_behavior_evals."""
from pathlib import Path
import re
import unittest


PACKAGE = Path(__file__).resolve().parents[1]


def required_routes(package):
    entry = (package / "SKILL.md").read_text(encoding="utf-8")
    rows = {}
    for path, condition, timing in re.findall(
        r"^\| \[[^\]]+\]\(([^)]+)\) \| ([^|]+) \| ([^|]+) \|$",
        entry,
        re.MULTILINE,
    ):
        rows[path] = (condition, timing)
    return entry, rows


class PackageResourceTest(unittest.TestCase):
    def test_all_owned_instruction_resources_have_pre_action_routes(self):
        entry, rows = required_routes(PACKAGE)
        expected = {
            "references/evaluation.md": "behavioral/artifact skill-output test cases",
            "references/description-optimization.md": "Description optimization is accepted",
            "references/environments.md": "Claude.ai or Cowork",
            "references/schemas.md": "Authoring or changing evals.json",
            "agents/grader.md": "Evaluating assertions",
            "agents/analyzer.md": "Analyzing benchmark",
            "agents/comparator.md": "blind A/B comparison",
            "assets/eval_review.html": "user review",
            "docs/codex-behavioral-eval-runner-future-work.md": "Planning extensions",
        }
        self.assertEqual(set(expected), set(rows))
        owned = {
            str(path.relative_to(PACKAGE))
            for directory in ("references", "agents", "docs")
            for path in (PACKAGE / directory).glob("*.md")
        }
        self.assertLessEqual(owned, set(rows))
        for path, trigger in expected.items():
            with self.subTest(path=path):
                condition, timing = rows[path]
                self.assertIn(trigger, condition)
                self.assertTrue(timing.startswith("Before"), timing)
                self.assertTrue((PACKAGE / path).read_text(encoding="utf-8"))
        self.assertIn("Do not read all references at startup", entry)
        self.assertIn("missing or unreadable, stop that action", entry)
        self.assertIn("report the exact path and gap", entry)
        self.assertIn("not implemented capability or a prerequisite", rows[
            "docs/codex-behavioral-eval-runner-future-work.md"
        ][1])

    def test_authoring_core_stays_inline_and_eval_policy_is_reachable(self):
        entry, rows = required_routes(PACKAGE)
        for core in ("### Capture Intent", "### Interview and Research",
                     "#### Principle of Lack of Surprise", "### Writing Style",
                     "### How to think about improvements", "### The iteration loop",
                     "present_files"):
            self.assertIn(core, entry)
        evaluation = (PACKAGE / "references/evaluation.md").read_text()
        self.assertNotIn("### Choose the evaluation runner", entry)
        for obligation in (
            "Before a live, model-backed run, show the exact command",
            "obtain approval unless that class of run is already authorized",
            "A zero Codex exit is", "execution evidence only",
            "Do not also spawn those runs", "--baseline-skill",
            "--output-dir", "Optional `--model` and `--reasoning`",
            "same turn", "snapshot the skill", "timing.json",
            "`text`, `passed`, and `evidence`", "mean ± stddev",
            "with_skill version before", "--previous-workspace",
            "--static <output_path>", "feedback.json", "kill $VIEWER_PID",
        ):
            with self.subTest(obligation=obligation):
                self.assertIn(obligation, evaluation)
        self.assertIn("Before designing prompts", rows["references/evaluation.md"][1])

    def test_conditional_optimization_and_platform_contracts(self):
        entry, rows = required_routes(PACKAGE)
        self.assertIn("evals/evals.json", rows["references/evaluation.md"][0])
        self.assertIn("Description-trigger queries and run_loop use only the optimization route", entry)
        self.assertIn("load both routes when both workflows are requested", entry)
        optimization = (PACKAGE / "references/description-optimization.md").read_text()
        for obligation in ("Create 20 eval queries", "near-misses", "60% train",
                           "40% held-out test", "query 3 times", "--max-iterations 5",
                           "best_description", "before/after", "assets/eval_review.html"):
            self.assertIn(obligation, optimization)
        environments = (PACKAGE / "references/environments.md").read_text()
        for obligation in ("Skip the baseline runs", "Skip the quantitative benchmarking",
                           "Preserve the original name", "Copy to a writeable location",
                           "stage in `/tmp/` first", "GENERATE THE EVAL VIEWER *BEFORE*",
                           "user agrees it's in good shape"):
            self.assertIn(obligation, environments)


if __name__ == "__main__":
    unittest.main()
