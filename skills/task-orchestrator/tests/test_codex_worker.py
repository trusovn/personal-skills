import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import textwrap
import time
import unittest


SCRIPT = Path(__file__).parents[1] / "scripts" / "codex_worker.py"


class CodexWorkerTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.run_dir = self.root / "run"
        self.prompt = self.root / "prompt.txt"
        self.prompt.write_text("Implement the bounded task.\n")

    def tearDown(self):
        self.temp_dir.cleanup()

    def write_fake_codex(
        self,
        *,
        exit_code=0,
        emit_thread=True,
        status="complete",
        preflight_exit=0,
        write_result=True,
    ):
        fake = self.root / "codex"
        fake.write_text(
            textwrap.dedent(
                f"""\
                #!/usr/bin/env python3
                import json
                from pathlib import Path
                import sys

                args = sys.argv[1:]
                log_path = Path({str(self.root / 'argv.json')!r})
                log = json.loads(log_path.read_text()) if log_path.exists() else []
                log.append(args)
                log_path.write_text(json.dumps(log))
                if "--help" in args:
                    raise SystemExit({preflight_exit})
                if {emit_thread!r}:
                    print(json.dumps({{"type": "thread.started", "thread_id": "thread-123"}}), flush=True)
                if {write_result!r} and "-o" in args:
                    result_path = Path(args[args.index("-o") + 1])
                    result_path.write_text(json.dumps({{
                        "status": {status!r},
                        "task_id": "T1",
                        "summary": "Implemented the task.",
                        "files_changed": ["lib/example.rb"],
                        "verification": [],
                        "decisions": [],
                        "questions": [],
                        "risks": [],
                        "next_action": "Inspect the diff."
                    }}))
                raise SystemExit({exit_code})
                """
            )
        )
        fake.chmod(0o755)
        return fake

    def write_sleeping_fake_codex(self):
        fake = self.root / "codex"
        fake.write_text(
            textwrap.dedent(
                f"""\
                #!/usr/bin/env python3
                import json
                from pathlib import Path
                import signal
                import subprocess
                import sys

                args = sys.argv[1:]
                if "--help" in args:
                    raise SystemExit(0)
                print(json.dumps({{"type": "thread.started", "thread_id": "thread-timeout"}}), flush=True)
                child = subprocess.Popen([sys.executable, "-c", "import signal; signal.pause()"])
                Path({str(self.root / 'child.pid')!r}).write_text(str(child.pid))
                signal.pause()
                """
            )
        )
        fake.chmod(0o755)
        return fake

    def run_worker(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_start_persists_thread_and_structured_result(self):
        fake = self.write_fake_codex()

        result = self.run_worker(
            "start",
            "--run-dir", str(self.run_dir),
            "--cwd", str(self.root),
            "--prompt-file", str(self.prompt),
            "--codex-bin", str(fake),
        )

        self.assertEqual(0, result.returncode, result.stderr)
        state = json.loads((self.run_dir / "state.json").read_text())
        self.assertEqual("thread-123", state["thread_id"])
        self.assertEqual("awaiting_inspection", state["status"])
        self.assertEqual("complete", state["attempt_outcome"])
        self.assertEqual(1, state["turn"])
        self.assertEqual("never", state["approval_policy"])
        self.assertEqual("codex-cli", state["transport"])
        self.assertIn("started_at", state)
        self.assertIn("ended_at", state)
        self.assertEqual(
            ["--ask-for-approval", "never", "exec"],
            state["effective_command"][1:4],
        )
        self.assertEqual(64, len(state["prompt_sha256"]))
        self.assertTrue((self.run_dir / "turn-001.events.jsonl").exists())
        self.assertTrue((self.run_dir / "turn-001.result.json").exists())
        self.assertTrue((self.run_dir / "turn-001.result.state.json").exists())

    def test_resume_reuses_saved_thread_instead_of_starting_over(self):
        fake = self.write_fake_codex(status="needs_input")
        first = self.run_worker(
            "start",
            "--run-dir", str(self.run_dir),
            "--cwd", str(self.root),
            "--prompt-file", str(self.prompt),
            "--codex-bin", str(fake),
        )
        self.assertEqual(0, first.returncode, first.stderr)

        follow_up = self.root / "follow-up.txt"
        follow_up.write_text("Use transport-neutral before/after strings.\n")
        resumed = self.run_worker(
            "resume",
            "--run-dir", str(self.run_dir),
            "--prompt-file", str(follow_up),
            "--codex-bin", str(fake),
        )

        self.assertEqual(0, resumed.returncode, resumed.stderr)
        invocations = json.loads((self.root / "argv.json").read_text())
        self.assertEqual(
            [
                "--ask-for-approval", "never", "exec", "resume",
                "-c", "sandbox_mode=\"workspace-write\"", "--help",
            ],
            invocations[-2],
        )
        argv = invocations[-1]
        self.assertEqual(["--ask-for-approval", "never", "exec", "resume"], argv[:4])
        self.assertIn("thread-123", argv)
        self.assertNotIn("--sandbox", argv)
        self.assertIn("sandbox_mode=\"workspace-write\"", argv)
        self.assertNotIn("--dangerously-bypass-approvals-and-sandbox", argv)
        state = json.loads((self.run_dir / "state.json").read_text())
        self.assertEqual(2, state["turn"])

    def test_failed_turn_keeps_thread_id_for_recovery(self):
        fake = self.write_fake_codex(exit_code=75)

        result = self.run_worker(
            "start",
            "--run-dir", str(self.run_dir),
            "--cwd", str(self.root),
            "--prompt-file", str(self.prompt),
            "--codex-bin", str(fake),
        )

        self.assertEqual(75, result.returncode)
        state = json.loads((self.run_dir / "state.json").read_text())
        self.assertEqual("thread-123", state["thread_id"])
        self.assertEqual("resumable", state["status"])
        self.assertEqual("interrupted", state["attempt_outcome"])
        self.assertEqual(75, state["exit_code"])

    def test_failure_before_thread_start_is_not_resumable(self):
        fake = self.write_fake_codex(exit_code=2, emit_thread=False)

        result = self.run_worker(
            "start",
            "--run-dir", str(self.run_dir),
            "--cwd", str(self.root),
            "--prompt-file", str(self.prompt),
            "--codex-bin", str(fake),
        )

        self.assertEqual(2, result.returncode)
        state = json.loads((self.run_dir / "state.json").read_text())
        self.assertIsNone(state["thread_id"])
        self.assertEqual("stopped", state["status"])
        self.assertEqual("failed_to_start", state["attempt_outcome"])

    def test_safe_command_uses_global_approval_flag_and_no_bypass(self):
        fake = self.write_fake_codex()

        result = self.run_worker(
            "start",
            "--run-dir", str(self.run_dir),
            "--cwd", str(self.root),
            "--prompt-file", str(self.prompt),
            "--codex-bin", str(fake),
        )

        self.assertEqual(0, result.returncode, result.stderr)
        invocations = json.loads((self.root / "argv.json").read_text())
        self.assertEqual(
            [
                "--ask-for-approval", "never", "exec",
                "--sandbox", "workspace-write", "--help",
            ],
            invocations[0],
        )
        self.assertEqual(["--ask-for-approval", "never", "exec"], invocations[1][:3])
        self.assertIn("workspace-write", invocations[1])
        self.assertNotIn("--dangerously-bypass-approvals-and-sandbox", invocations[1])

    def test_unsupported_safe_cli_fails_before_run_creation(self):
        fake = self.write_fake_codex(preflight_exit=2)

        result = self.run_worker(
            "start",
            "--run-dir", str(self.run_dir),
            "--cwd", str(self.root),
            "--prompt-file", str(self.prompt),
            "--codex-bin", str(fake),
        )

        self.assertEqual(2, result.returncode)
        self.assertFalse(self.run_dir.exists())
        self.assertEqual(1, len(json.loads((self.root / "argv.json").read_text())))

    def test_timeout_terminates_process_group_and_records_terminal_state(self):
        fake = self.write_sleeping_fake_codex()

        result = self.run_worker(
            "start",
            "--run-dir", str(self.run_dir),
            "--cwd", str(self.root),
            "--prompt-file", str(self.prompt),
            "--codex-bin", str(fake),
            "--timeout-seconds", "0.2",
        )

        self.assertEqual(124, result.returncode, result.stderr)
        state = json.loads((self.run_dir / "state.json").read_text())
        self.assertEqual("resumable", state["status"])
        self.assertEqual("timed_out", state["attempt_outcome"])
        self.assertIsNone(state["process_pid"])
        child_pid = int((self.root / "child.pid").read_text())
        deadline = time.monotonic() + 2
        child_alive = True
        while time.monotonic() < deadline:
            try:
                os.kill(child_pid, 0)
            except ProcessLookupError:
                child_alive = False
                break
            time.sleep(0.01)
        self.assertFalse(child_alive, f"child process {child_pid} remained alive")

    def test_signal_interruption_terminates_process_group_and_records_terminal_state(self):
        fake = self.write_sleeping_fake_codex()
        wrapper = subprocess.Popen(
            [
                sys.executable, str(SCRIPT), "start",
                "--run-dir", str(self.run_dir),
                "--cwd", str(self.root),
                "--prompt-file", str(self.prompt),
                "--codex-bin", str(fake),
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        state_path = self.run_dir / "state.json"
        deadline = time.monotonic() + 3
        while time.monotonic() < deadline:
            if state_path.exists() and (self.root / "child.pid").exists():
                state = json.loads(state_path.read_text())
                if state.get("status") == "running" and state.get("thread_id"):
                    break
            time.sleep(0.01)
        else:
            wrapper.kill()
            wrapper.wait(timeout=2)
            self.fail("wrapper did not reach a recorded running state")

        wrapper.send_signal(signal.SIGTERM)
        stdout, stderr = wrapper.communicate(timeout=3)
        self.assertNotEqual(0, wrapper.returncode, stdout + stderr)
        state = json.loads(state_path.read_text())
        self.assertEqual("resumable", state["status"])
        self.assertEqual("interrupted", state["attempt_outcome"])
        self.assertIsNone(state["process_pid"])
        terminal_path = self.run_dir / "turn-001.result.state.json"
        self.assertEqual(state, json.loads(terminal_path.read_text()))

        child_pid = int((self.root / "child.pid").read_text())
        deadline = time.monotonic() + 2
        while time.monotonic() < deadline:
            try:
                os.kill(child_pid, 0)
            except ProcessLookupError:
                break
            time.sleep(0.01)
        else:
            self.fail(f"child process {child_pid} remained alive")

    def test_resume_rejects_live_recorded_process_without_starting_another(self):
        fake = self.write_fake_codex()
        process = subprocess.Popen([sys.executable, "-c", "import signal; signal.pause()"])
        self.run_dir.mkdir()
        (self.run_dir / "state.json").write_text(json.dumps({
            "version": 1,
            "thread_id": "thread-live",
            "turn": 1,
            "cwd": str(self.root),
            "status": "running",
            "process_pid": process.pid,
        }))
        follow_up = self.root / "follow-up.txt"
        follow_up.write_text("Continue safely.\n")
        try:
            result = self.run_worker(
                "resume",
                "--run-dir", str(self.run_dir),
                "--prompt-file", str(follow_up),
                "--codex-bin", str(fake),
            )
        finally:
            process.terminate()
            process.wait(timeout=2)

        self.assertEqual(2, result.returncode)
        self.assertIn("still alive", result.stderr)
        self.assertFalse((self.run_dir / "turn-002.events.jsonl").exists())
        self.assertFalse((self.root / "argv.json").exists())

    def test_danger_full_access_is_rejected_without_persisted_authorization(self):
        fake = self.write_fake_codex()

        result = self.run_worker(
            "start",
            "--run-dir", str(self.run_dir),
            "--cwd", str(self.root),
            "--prompt-file", str(self.prompt),
            "--codex-bin", str(fake),
            "--sandbox", "danger-full-access",
        )

        self.assertEqual(2, result.returncode)
        self.assertIn("persisted authorization", result.stderr)
        self.assertFalse(self.run_dir.exists())
        self.assertFalse((self.root / "argv.json").exists())

    def test_zero_exit_without_result_is_missing_result_not_success(self):
        fake = self.write_fake_codex(write_result=False)

        result = self.run_worker(
            "start",
            "--run-dir", str(self.run_dir),
            "--cwd", str(self.root),
            "--prompt-file", str(self.prompt),
            "--codex-bin", str(fake),
        )

        self.assertEqual(3, result.returncode)
        state = json.loads((self.run_dir / "state.json").read_text())
        self.assertEqual("stopped", state["status"])
        self.assertEqual("missing_result", state["attempt_outcome"])

    def test_zero_exit_with_invalid_result_status_is_missing_result(self):
        fake = self.write_fake_codex(status="not-a-contract-status")

        result = self.run_worker(
            "start",
            "--run-dir", str(self.run_dir),
            "--cwd", str(self.root),
            "--prompt-file", str(self.prompt),
            "--codex-bin", str(fake),
        )

        self.assertEqual(3, result.returncode)
        state = json.loads((self.run_dir / "state.json").read_text())
        self.assertEqual("stopped", state["status"])
        self.assertEqual("missing_result", state["attempt_outcome"])

    def test_malformed_nested_result_fields_are_not_complete(self):
        """Malformed nested values (integer summary, string question entries, null next_action)
        must not be treated as complete."""
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "task_orchestrator_worker",
            SCRIPT,
        )
        mod = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(mod)

        # Construct a result with correct top-level keys but invalid nested values.
        malformed = {
            "status": "complete",
            "task_id": "T1",
            "summary": 42,  # should be a string
            "files_changed": ["src/main.py"],
            "verification": [
                {"command": "make verify", "outcome": "passed", "summary": "ok"},
            ],
            "decisions": [
                {"decision": "used X", "reason": "faster", "scope": "task"},
            ],
            "questions": ["this is a string not an object"],  # should be objects
            "risks": ["some risk"],
            "next_action": None,  # should be a string
        }
        result_path = self.run_dir / "turn-001.result.json"
        self.run_dir.mkdir(parents=True)
        result_path.write_text(json.dumps(malformed))

        status = mod.result_status(result_path)
        self.assertIsNone(status, "Malformed nested values must not return 'complete'")

    def test_missing_required_nested_fields_are_not_complete(self):
        """Verification items missing required fields (command, outcome, summary)
        must not be treated as complete."""
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "task_orchestrator_worker",
            SCRIPT,
        )
        mod = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(mod)

        # Verification items missing required fields.
        malformed = {
            "status": "complete",
            "task_id": "T1",
            "summary": "Done.",
            "files_changed": [],
            "verification": [
                {"command": "make verify"},  # missing "outcome" and "summary"
            ],
            "decisions": [],
            "questions": [],
            "risks": [],
            "next_action": "Inspect.",
        }
        result_path = self.run_dir / "turn-001.result.json"
        self.run_dir.mkdir(parents=True)
        result_path.write_text(json.dumps(malformed))

        status = mod.result_status(result_path)
        self.assertIsNone(status, "Missing required nested fields must not return 'complete'")

    def test_valid_result_returns_complete(self):
        """A fully valid result must return 'complete'."""
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "task_orchestrator_worker",
            SCRIPT,
        )
        mod = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(mod)

        valid = {
            "status": "complete",
            "task_id": "T1",
            "summary": "Done.",
            "files_changed": ["src/main.py"],
            "verification": [
                {"command": "make verify", "outcome": "passed", "summary": "ok"},
            ],
            "decisions": [
                {"decision": "used X", "reason": "faster", "scope": "task"},
            ],
            "questions": [
                {"question": "any?", "recommendation": "none", "blocking": False},
            ],
            "risks": [],
            "next_action": "Inspect.",
        }
        result_path = self.run_dir / "turn-001.result.json"
        self.run_dir.mkdir(parents=True)
        result_path.write_text(json.dumps(valid))

        status = mod.result_status(result_path)
        self.assertEqual("complete", status)
