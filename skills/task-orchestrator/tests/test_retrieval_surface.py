import importlib.util
import json
from pathlib import Path
import re
import tempfile
import unittest


SKILL_ROOT = Path(__file__).parents[1]
LINK_PATTERN = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def load_controller_state():
    path = SKILL_ROOT / "scripts" / "controller_state.py"
    spec = importlib.util.spec_from_file_location("task_orchestrator_controller_state", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class RetrievalSurfaceTest(unittest.TestCase):
    def test_expected_current_references_exist(self):
        expected = (
            "references/index.md",
            "references/operator-guide.md",
            "references/architecture-map.md",
            "assets/examples/minimal-run-policy.json",
            "assets/examples/minimal-task-manifest.json",
            "docs/stage-3-retrieval-surface-follow-up.md",
        )

        missing = [path for path in expected if not (SKILL_ROOT / path).is_file()]

        self.assertEqual([], missing)

    def test_skill_routes_through_controller_and_matches_commit_policy(self):
        skill = (SKILL_ROOT / "SKILL.md").read_text()

        self.assertIn("scripts/controller.py init", skill)
        self.assertIn("scripts/controller.py run-next", skill)
        self.assertIn("scripts/controller.py inspect", skill)
        self.assertNotIn("scripts/codex_worker.py start", skill)
        self.assertIn("`off` or `controller_exact_paths`", skill)
        self.assertNotIn("`per-task`", skill)

    def test_current_markdown_links_resolve(self):
        markdown_files = [SKILL_ROOT / "SKILL.md"]
        markdown_files.extend(sorted((SKILL_ROOT / "references").glob("*.md")))
        markdown_files.extend(sorted((SKILL_ROOT / "docs").glob("*.md")))
        missing = []

        for markdown_path in markdown_files:
            for raw_target in LINK_PATTERN.findall(markdown_path.read_text()):
                target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
                target = target.split("#", 1)[0]
                if not target or "://" in target or target.startswith("mailto:"):
                    continue
                resolved = (markdown_path.parent / target).resolve()
                if not resolved.exists():
                    missing.append(
                        f"{markdown_path.relative_to(SKILL_ROOT)} -> {raw_target}"
                    )

        self.assertEqual([], missing)

    def test_minimal_examples_pass_runtime_validation(self):
        controller_state = load_controller_state()
        policy = json.loads(
            (SKILL_ROOT / "assets" / "examples" / "minimal-run-policy.json").read_text()
        )
        manifest = json.loads(
            (SKILL_ROOT / "assets" / "examples" / "minimal-task-manifest.json").read_text()
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            repository = Path(temp_dir)
            brief_path = repository / manifest["tasks"][0]["brief_path"]
            brief_path.parent.mkdir(parents=True)
            brief_path.write_text("# T1\n")
            policy["repository"] = str(repository)
            policy["permissions"]["writable_roots"] = [str(repository)]

            controller_state.validate_run_policy(policy)
            validated = controller_state.validate_task_manifest(
                policy, manifest, repository
            )

        self.assertEqual(["T1"], [task["id"] for task in validated["task_entries"]])

    def test_evals_cover_current_retrieval_routes(self):
        evals = json.loads((SKILL_ROOT / "evals" / "evals.json").read_text())["evals"]
        prompts = "\n".join(item["prompt"] for item in evals)
        expectations = "\n".join(
            expectation
            for item in evals
            for expectation in item.get("expectations", [])
        )

        self.assertIn("start a run", prompts.lower())
        self.assertIn("interrupted", prompts.lower())
        self.assertIn("Git drift detection", prompts)
        self.assertIn("scripts/controller.py", expectations)
        self.assertIn("scripts/controller_git.py", expectations)
        self.assertIn("tests/test_controller_git.py", expectations)
        self.assertIn("docs/history/", expectations)


if __name__ == "__main__":
    unittest.main()
