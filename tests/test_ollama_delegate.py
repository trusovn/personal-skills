import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "ollama_delegate.py"
SPEC = importlib.util.spec_from_file_location("ollama_delegate", SCRIPT)
ollama_delegate = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(ollama_delegate)


class OllamaDelegateTests(unittest.TestCase):
    def test_default_config_and_models_are_loadable(self):
        config = ollama_delegate.load_config(ROOT / "scripts" / "ollama-models.json")
        self.assertEqual(1, config["schema_version"])
        self.assertIn(config["default_model"], config["models"])
        self.assertTrue(all(item["model"].endswith(":cloud") for item in config["models"].values()))

    def test_skill_package_includes_references_but_excludes_tests(self):
        with tempfile.TemporaryDirectory() as tempdir:
            skill = Path(tempdir)
            (skill / "references").mkdir()
            (skill / "tests").mkdir()
            (skill / "SKILL.md").write_text("---\nname: sample\n---\nbody\n", encoding="utf-8")
            (skill / "references" / "guide.md").write_text("reference\n", encoding="utf-8")
            (skill / "tests" / "private.md").write_text("hidden\n", encoding="utf-8")

            packaged = ollama_delegate.skill_package(skill)

            self.assertIn("SKILL.md", packaged)
            self.assertIn("references/guide.md", packaged)
            self.assertNotIn("private.md", packaged)

    def test_read_only_tools_reject_path_escape(self):
        with tempfile.TemporaryDirectory() as tempdir:
            repo = Path(tempdir)
            (repo / "file.txt").write_text("hello\n", encoding="utf-8")
            tools = ollama_delegate.ReadOnlyTools(repo)

            result = json.loads(tools.execute("read_file", {"path": "../outside.txt"}))

            self.assertIn("path escapes repository", result["error"])

    def test_run_delegate_executes_read_tool_then_returns_final_message(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            scripts = root / "scripts"
            skills = root / "skills" / "sample"
            repo = root / "repo"
            scripts.mkdir()
            skills.mkdir(parents=True)
            repo.mkdir()
            fake_script = scripts / "ollama_delegate.py"
            fake_script.write_text("# placeholder\n", encoding="utf-8")
            (skills / "SKILL.md").write_text("---\nname: sample\n---\nRead evidence.\n", encoding="utf-8")
            (repo / "app.txt").write_text("evidence\n", encoding="utf-8")
            config = scripts / "ollama-models.json"
            config.write_text(json.dumps({
                "schema_version": 1,
                "endpoint": "http://127.0.0.1:11434",
                "default_model": "cloud",
                "models": {"cloud": {"model": "example:cloud"}},
            }), encoding="utf-8")
            events = [
                {"message": {"content": "", "tool_calls": [{
                    "id": "1",
                    "function": {"name": "read_file", "arguments": {"path": "app.txt"}},
                }]}},
                {"message": {"content": "review complete"}, "prompt_eval_count": 10, "eval_count": 2},
            ]

            with mock.patch.object(ollama_delegate, "ollama_complete", side_effect=events):
                result = ollama_delegate.run_delegate(
                    repo=repo,
                    skill_id="sample",
                    task="review",
                    model_alias=None,
                    config_path=config,
                    max_turns=4,
                    script_path=fake_script,
                )

            self.assertEqual("completed", result["status"])
            self.assertEqual("review complete", result["final_message"])
            self.assertEqual("read_file", result["tool_calls"][0]["tool"])
            self.assertIn("evidence", result["tool_calls"][0]["result"])

    def test_development_installer_carries_skill_runtime_and_config(self):
        installer_path = ROOT / "scripts" / "install_development_skills.py"
        installer_spec = importlib.util.spec_from_file_location("installer_for_ollama_test", installer_path)
        installer = importlib.util.module_from_spec(installer_spec)
        assert installer_spec.loader is not None
        installer_spec.loader.exec_module(installer)

        self.assertIn(("ollama-delegate", "skills/ollama-delegate"), installer.DEVELOPMENT_SKILL_SOURCES)
        self.assertIn("ollama_delegate.py", installer.SHARED_SCRIPT_FILES)
        self.assertIn("ollama-models.json", installer.SHARED_SCRIPT_FILES)


if __name__ == "__main__":
    unittest.main()
