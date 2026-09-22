import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "runtime_context.py"
SCHEMA_PATH = Path(__file__).resolve().parents[1] / "scripts" / "runtime-context.schema.v1.json"
SPEC = importlib.util.spec_from_file_location("runtime_context", MODULE_PATH)
runtime_context = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(runtime_context)


class RuntimeContextTests(unittest.TestCase):
    def write_context(self, root: Path, name: str, value: dict) -> Path:
        path = root / name
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def test_valid_complete_context(self):
        value = {
            "schema_version": 1,
            "runner": "codex",
            "provider": "openai",
            "model": "gpt-5.6-sol",
            "variant": None,
            "effort": "medium",
            "session_id": "thread-123",
            "identity_source": "launcher",
        }

        self.assertEqual(value, runtime_context.validate_runtime_context(value))

    def test_partial_context_allows_unknown_model(self):
        value = {
            "schema_version": 1,
            "runner": "opencode",
            "provider": "ollama",
            "model": None,
            "variant": None,
            "effort": None,
            "session_id": "session-456",
            "identity_source": "adapter",
        }

        self.assertEqual(value, runtime_context.validate_runtime_context(value))

    def test_no_context_is_normalized_unavailable(self):
        expected = {
            "schema_version": 1,
            "runner": None,
            "provider": None,
            "model": None,
            "variant": None,
            "effort": None,
            "session_id": None,
            "identity_source": "unavailable",
        }

        self.assertEqual(expected, runtime_context.load_runtime_context())
        with tempfile.TemporaryDirectory() as tempdir:
            missing = Path(tempdir) / "not-created.json"
            self.assertEqual(expected, runtime_context.load_runtime_context(missing))

    def test_invalid_or_unsupported_schema_fails_clearly(self):
        unsupported = runtime_context.unavailable_runtime_context()
        unsupported["schema_version"] = 2
        with self.assertRaisesRegex(runtime_context.RuntimeContextError, "Unsupported.*schema_version"):
            runtime_context.validate_runtime_context(unsupported)

        with tempfile.TemporaryDirectory() as tempdir:
            malformed = Path(tempdir) / "malformed.json"
            malformed.write_text("{ definitely not json", encoding="utf-8")
            with self.assertRaisesRegex(runtime_context.RuntimeContextError, "Invalid runtime-context JSON"):
                runtime_context.load_runtime_context(malformed)

    def test_contract_has_no_llm_self_identification_field(self):
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        self.assertEqual(set(runtime_context.CONTEXT_FIELDS), set(schema["properties"]))
        self.assertNotIn("self_identified_model", schema["properties"])
        self.assertNotIn("llm_identity", schema["properties"])
        self.assertNotIn("self_report", schema["properties"])

        invalid = runtime_context.unavailable_runtime_context()
        invalid["self_identified_model"] = "I am GPT-5"
        with self.assertRaisesRegex(runtime_context.RuntimeContextError, "unexpected fields"):
            runtime_context.validate_runtime_context(invalid)

    def test_self_report_is_not_a_valid_identity_source(self):
        invalid = runtime_context.unavailable_runtime_context()
        invalid["identity_source"] = "llm_self_report"
        with self.assertRaisesRegex(runtime_context.RuntimeContextError, "identity_source"):
            runtime_context.validate_runtime_context(invalid)

    def test_invalid_identity_source_type_fails_clearly(self):
        invalid = runtime_context.unavailable_runtime_context()
        invalid["identity_source"] = []
        with self.assertRaisesRegex(runtime_context.RuntimeContextError, "identity_source"):
            runtime_context.validate_runtime_context(invalid)

        with tempfile.TemporaryDirectory() as tempdir:
            path = self.write_context(Path(tempdir), "runtime.json", invalid)
            result = subprocess.run(
                [sys.executable, str(MODULE_PATH), "validate", str(path)],
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertEqual(2, result.returncode)
        self.assertEqual(False, json.loads(result.stderr)["valid"])

    def test_runner_independent_consumer_loads_codex_and_opencode(self):
        examples = [
            {
                "schema_version": 1,
                "runner": "codex",
                "provider": "openai",
                "model": "gpt-5.6-sol",
                "variant": None,
                "effort": "high",
                "session_id": "thread-codex",
                "identity_source": "runner_event",
            },
            {
                "schema_version": 1,
                "runner": "opencode",
                "provider": "ollama",
                "model": "qwen3-coder",
                "variant": "local",
                "effort": None,
                "session_id": "session-opencode",
                "identity_source": "adapter",
            },
        ]

        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            loaded = [
                runtime_context.load_runtime_context(
                    self.write_context(root, f"runtime-{index}.json", value)
                )
                for index, value in enumerate(examples)
            ]

        self.assertEqual(examples, loaded)

    def test_unavailable_source_cannot_claim_identity_values(self):
        invalid = runtime_context.unavailable_runtime_context()
        invalid["runner"] = "guessed-runner"
        with self.assertRaisesRegex(runtime_context.RuntimeContextError, "requires all runtime identity values"):
            runtime_context.validate_runtime_context(invalid)

    def test_cli_validate_emits_normalized_json(self):
        value = {
            "schema_version": 1,
            "runner": "codex",
            "provider": "openai",
            "model": None,
            "variant": None,
            "effort": "medium",
            "session_id": "thread-123",
            "identity_source": "launcher",
        }
        with tempfile.TemporaryDirectory() as tempdir:
            path = self.write_context(Path(tempdir), "runtime.json", value)
            result = subprocess.run(
                [sys.executable, str(MODULE_PATH), "validate", str(path)],
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(value, json.loads(result.stdout))

    def test_cli_load_missing_is_non_fatal(self):
        with tempfile.TemporaryDirectory() as tempdir:
            missing = Path(tempdir) / "missing.json"
            result = subprocess.run(
                [sys.executable, str(MODULE_PATH), "load", str(missing)],
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("unavailable", json.loads(result.stdout)["identity_source"])


if __name__ == "__main__":
    unittest.main()
