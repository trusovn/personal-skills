import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import textwrap
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

    def write_fake_codex(self, *, exit_code=0, emit_thread=True, status="complete"):
        fake = self.root / "codex"
        fake.write_text(
            textwrap.dedent(
                f"""\
                #!/usr/bin/env python3
                import json
                from pathlib import Path
                import sys

                args = sys.argv[1:]
                Path({str(self.root / 'argv.json')!r}).write_text(json.dumps(args))
                if {emit_thread!r}:
                    print(json.dumps({{"type": "thread.started", "thread_id": "thread-123"}}), flush=True)
                if "-o" in args:
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
        self.assertEqual("complete", state["status"])
        self.assertEqual(1, state["turn"])
        self.assertTrue((self.run_dir / "turn-001.events.jsonl").exists())
        self.assertTrue((self.run_dir / "turn-001.result.json").exists())

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
        argv = json.loads((self.root / "argv.json").read_text())
        self.assertEqual(["exec", "resume"], argv[:2])
        self.assertIn("thread-123", argv)
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
        self.assertEqual("interrupted", state["status"])
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
        self.assertEqual("failed_to_start", state["status"])


if __name__ == "__main__":
    unittest.main()
