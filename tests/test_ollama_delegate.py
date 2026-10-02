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
    def make_delegate_fixture(self, root: Path) -> tuple[Path, Path, Path]:
        scripts = root / "scripts"
        skills = root / "skills" / "sample"
        repo = root / "repo"
        scripts.mkdir()
        skills.mkdir(parents=True)
        repo.mkdir()
        fake_script = scripts / "ollama_delegate.py"
        fake_script.write_text("# placeholder\n", encoding="utf-8")
        (skills / "SKILL.md").write_text(
            "---\nname: sample\n---\nRead evidence.\n", encoding="utf-8"
        )
        (repo / "app.txt").write_text("evidence\n", encoding="utf-8")
        config = scripts / "ollama-models.json"
        config.write_text(json.dumps({
            "schema_version": 1,
            "endpoint": "http://127.0.0.1:11434",
            "default_model": "cloud",
            "models": {"cloud": {"model": "example:cloud"}},
        }), encoding="utf-8")
        return fake_script, config, repo

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

    def test_read_only_tools_reject_non_object_arguments(self):
        tools = ollama_delegate.ReadOnlyTools(ROOT)

        result = json.loads(tools.execute("list_files", []))

        self.assertEqual("tool arguments must be a JSON object", result["error"])

    def test_read_only_tools_bound_large_results(self):
        with tempfile.TemporaryDirectory() as tempdir:
            repo = Path(tempdir)
            for number in range(20):
                size = 1_000 if number == 0 else 100
                (repo / f"file-{number:02d}.txt").write_text(
                    "match " + "x" * size, encoding="utf-8"
                )
            tools = ollama_delegate.ReadOnlyTools(repo)

            with mock.patch.object(ollama_delegate, "MAX_TOOL_RESULT_CHARS", 300):
                listed = tools.list_files(".")
                searched = tools.search_text("match", ".")
                read = tools.read_file("file-00.txt")

            self.assertLessEqual(len(listed), 300)
            self.assertTrue(json.loads(listed)["truncated"])
            self.assertLessEqual(len(searched), 300)
            self.assertTrue(json.loads(searched)["truncated"])
            self.assertLessEqual(len(read), 300)
            self.assertIn("[truncated;", read)

    def test_read_file_can_continue_past_a_long_single_line(self):
        with tempfile.TemporaryDirectory() as tempdir:
            repo = Path(tempdir)
            (repo / "one-line.json").write_text(
                "a" * 400 + "TAIL_SENTINEL", encoding="utf-8"
            )
            tools = ollama_delegate.ReadOnlyTools(repo)

            with mock.patch.object(ollama_delegate, "MAX_TOOL_RESULT_CHARS", 120):
                chunks = []
                offset = 0
                for _ in range(10):
                    chunk = tools.read_file("one-line.json", offset=offset)
                    chunks.append(chunk)
                    if "next_offset=" not in chunk:
                        break
                    offset = int(chunk.split("next_offset=", 1)[1].split("]", 1)[0])

            self.assertTrue(all(len(chunk) <= 120 for chunk in chunks))
            self.assertIn("TAIL_SENTINEL", "".join(chunks))

    def test_search_text_centers_context_on_a_long_line_match(self):
        with tempfile.TemporaryDirectory() as tempdir:
            repo = Path(tempdir)
            (repo / "one-line.json").write_text(
                "a" * 400 + "MATCH_SENTINEL" + "z" * 400, encoding="utf-8"
            )
            tools = ollama_delegate.ReadOnlyTools(repo)

            with mock.patch.object(ollama_delegate, "MAX_SEARCH_LINE_CHARS", 120):
                result = json.loads(tools.search_text("MATCH_SENTINEL", "."))

            self.assertEqual(401, result["matches"][0]["column"])
            self.assertIn("MATCH_SENTINEL", result["matches"][0]["text"])

    def test_run_delegate_executes_read_tool_then_returns_final_message(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            fake_script, config, repo = self.make_delegate_fixture(root)
            events = [
                {"done": True, "message": {"content": "", "tool_calls": [{
                    "id": "1",
                    "function": {"name": "read_file", "arguments": {"path": "app.txt"}},
                }]}},
                {
                    "done": True,
                    "message": {"content": "review complete"},
                    "prompt_eval_count": 10,
                    "eval_count": 2,
                },
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
            self.assertEqual(len("1: evidence"), result["tool_calls"][0]["result_chars"])
            self.assertNotIn("result", result["tool_calls"][0])

    def test_run_delegate_rejects_incomplete_response(self):
        with tempfile.TemporaryDirectory() as tempdir:
            fake_script, config, repo = self.make_delegate_fixture(Path(tempdir))

            with mock.patch.object(
                ollama_delegate,
                "ollama_complete",
                return_value={"done": False, "message": {"content": ""}},
            ):
                with self.assertRaisesRegex(ollama_delegate.DelegateError, "incomplete response"):
                    ollama_delegate.run_delegate(
                        repo=repo,
                        skill_id="sample",
                        task="review",
                        model_alias=None,
                        config_path=config,
                        max_turns=4,
                        script_path=fake_script,
                    )

    def test_run_delegate_rejects_error_response(self):
        with tempfile.TemporaryDirectory() as tempdir:
            fake_script, config, repo = self.make_delegate_fixture(Path(tempdir))

            with mock.patch.object(
                ollama_delegate,
                "ollama_complete",
                return_value={"error": "model failed"},
            ):
                with self.assertRaisesRegex(ollama_delegate.DelegateError, "model failed"):
                    ollama_delegate.run_delegate(
                        repo=repo,
                        skill_id="sample",
                        task="review",
                        model_alias=None,
                        config_path=config,
                        max_turns=4,
                        script_path=fake_script,
                    )

    def test_run_delegate_rejects_malformed_tool_call(self):
        with tempfile.TemporaryDirectory() as tempdir:
            fake_script, config, repo = self.make_delegate_fixture(Path(tempdir))

            with mock.patch.object(
                ollama_delegate,
                "ollama_complete",
                return_value={
                    "done": True,
                    "message": {"content": "", "tool_calls": [None]},
                },
            ):
                with self.assertRaisesRegex(ollama_delegate.DelegateError, "invalid tool call"):
                    ollama_delegate.run_delegate(
                        repo=repo,
                        skill_id="sample",
                        task="review",
                        model_alias=None,
                        config_path=config,
                        max_turns=4,
                        script_path=fake_script,
                    )

    def test_run_delegate_preserves_non_object_tool_arguments_for_validation(self):
        with tempfile.TemporaryDirectory() as tempdir:
            fake_script, config, repo = self.make_delegate_fixture(Path(tempdir))
            events = [
                {
                    "done": True,
                    "message": {"content": "", "tool_calls": [{
                        "id": "1",
                        "function": {"name": "list_files", "arguments": []},
                    }]},
                },
                {"done": True, "message": {"content": "recovered"}},
            ]
            observed_tool_result = None

            def complete(*args, **kwargs):
                nonlocal observed_tool_result
                messages = args[2]
                if len(messages) > 2:
                    observed_tool_result = json.loads(messages[-1]["content"])
                return events.pop(0)

            with mock.patch.object(ollama_delegate, "ollama_complete", side_effect=complete):
                result = ollama_delegate.run_delegate(
                    repo=repo,
                    skill_id="sample",
                    task="review",
                    model_alias=None,
                    config_path=config,
                    max_turns=4,
                    script_path=fake_script,
                )

            self.assertEqual("recovered", result["final_message"])
            self.assertEqual(
                "tool arguments must be a JSON object", observed_tool_result["error"]
            )

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
