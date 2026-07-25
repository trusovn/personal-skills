import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import textwrap
import unittest


RUNNER = (
    Path(__file__).parents[1] / "scripts" / "run_behavior_evals.py"
).resolve()
PILOT = (
    RUNNER.parents[2]
    / "task-implementation-flow"
    / "task-brief-designer"
)


class BehaviorEvalRunnerTest(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.bin = self.root / "bin"
        self.bin.mkdir()
        self.write_fake_codex()

    def tearDown(self):
        self.temporary_directory.cleanup()

    def write_fake_codex(self):
        codex = self.bin / "codex"
        codex.write_text(
            textwrap.dedent(
                f"""\
                #!{sys.executable}
                import os
                from pathlib import Path
                import sys

                arguments = sys.argv[1:]
                if arguments[arguments.index("--sandbox") + 1] != "workspace-write":
                    print("workspace-write sandbox missing", file=sys.stderr)
                    raise SystemExit(8)
                workspace = Path(arguments[arguments.index("-C") + 1])
                output = Path(arguments[arguments.index("-o") + 1])
                prompt = arguments[-1]
                (workspace / "codex-ran.txt").write_text(prompt, encoding="utf-8")
                output.write_text("fake final response\\n", encoding="utf-8")
                if "FAIL_CODEX" in prompt:
                    print("fake codex failure", file=sys.stderr)
                    raise SystemExit(7)
                """
            ),
            encoding="utf-8",
        )
        codex.chmod(0o755)

    def make_skill(self, name="current", evals=None):
        skill = self.root / name
        (skill / "evals").mkdir(parents=True)
        (skill / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: test\n---\n", encoding="utf-8"
        )
        (skill / "evals" / "evals.json").write_text(
            json.dumps({"skill_name": name, "evals": evals or []}),
            encoding="utf-8",
        )
        return skill

    def run_runner(self, skill, *arguments, with_codex=True):
        output = self.root / f"output-{len(list(self.root.glob('output-*')))}"
        env = os.environ.copy()
        env["PATH"] = (
            f"{self.bin}{os.pathsep}{env['PATH']}" if with_codex else "/missing"
        )
        completed = subprocess.run(
            [
                sys.executable,
                str(RUNNER),
                str(skill),
                "--output-dir",
                str(output),
                *arguments,
            ],
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        return completed, output

    def test_setup_substitution_preserves_prompt_and_evidence(self):
        skill = self.make_skill(
            evals=[
                {
                    "id": 1,
                    "prompt": "Create the requested artifact.",
                    "execution": {
                        "setup": {
                            "command": [
                                sys.executable,
                                "-c",
                                (
                                    "import os,pathlib,subprocess;"
                                    "p=pathlib.Path(os.environ['EVAL_WORK_ROOT'])/'repo';"
                                    "p.mkdir(parents=True);"
                                    "subprocess.run(['git','init','-q',str(p)],check=True)"
                                ),
                            ],
                            "env": {"EVAL_WORK_ROOT": "{run_root}/work"},
                        },
                        "workspace": "{run_root}/work/repo",
                    },
                }
            ]
        )

        completed, output = self.run_runner(
            skill, "--ids", "1", "--model", "test-model", "--reasoning", "low"
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        run = output / "current" / "eval-1"
        effective_prompt = (run / "effective-prompt.txt").read_text()
        self.assertTrue(effective_prompt.endswith("Create the requested artifact."))
        self.assertNotIn("EVAL_WORK_ROOT", effective_prompt)
        self.assertEqual(
            (run / "final-response.txt").read_text(), "fake final response\n"
        )
        result = json.loads((run / "result.json").read_text())
        self.assertEqual(result["setup_exit_code"], 0)
        self.assertEqual(result["codex_exit_code"], 0)
        self.assertEqual(result["model"], "test-model")
        self.assertEqual(result["reasoning"], "low")
        self.assertIn("codex-ran.txt", result["git_status_paths"])

    def test_eval_without_execution_uses_fresh_empty_workspace(self):
        skill = self.make_skill(evals=[{"id": 3, "prompt": "Work from scratch."}])

        completed, output = self.run_runner(skill)

        self.assertEqual(completed.returncode, 0, completed.stderr)
        run = output / "current" / "eval-3"
        self.assertTrue((run / "work" / "codex-ran.txt").is_file())
        result = json.loads((run / "result.json").read_text())
        self.assertIsNone(result["setup_exit_code"])
        self.assertEqual(result["git_status_paths"], [])

    def test_baseline_reuses_setup_but_has_an_isolated_workspace(self):
        setup = self.root / "setup.py"
        setup.write_text(
            (
                "import os\nfrom pathlib import Path\n"
                "workspace=Path(os.environ['TARGET'])\n"
                "workspace.mkdir(parents=True)\n"
                "(workspace/'fixture.txt').write_text('fixture')\n"
            ),
            encoding="utf-8",
        )
        skill = self.make_skill(
            evals=[
                {
                    "id": 4,
                    "prompt": "Same task.",
                    "execution": {
                        "setup": {
                            "command": [sys.executable, str(setup)],
                            "env": {"TARGET": "{run_root}/work/repo"},
                        },
                        "workspace": "{run_root}/work/repo",
                    },
                }
            ]
        )
        baseline = self.make_skill(name="baseline")

        completed, output = self.run_runner(
            skill, "--baseline-skill", str(baseline)
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        current = output / "current" / "eval-4"
        old = output / "baseline" / "eval-4"
        self.assertTrue((current / "work/repo/fixture.txt").is_file())
        self.assertTrue((old / "work/repo/fixture.txt").is_file())
        current_prompt = (current / "effective-prompt.txt").read_text()
        baseline_prompt = (old / "effective-prompt.txt").read_text()
        self.assertEqual(
            current_prompt.split("\n\n", 1)[1],
            baseline_prompt.split("\n\n", 1)[1],
        )
        self.assertIn(str(skill / "SKILL.md"), current_prompt)
        self.assertIn(str(baseline / "SKILL.md"), baseline_prompt)
        self.assertNotEqual(
            json.loads((current / "result.json").read_text())["workspace"],
            json.loads((old / "result.json").read_text())["workspace"],
        )

    def test_codex_failure_is_recorded_and_later_evals_continue(self):
        skill = self.make_skill(
            evals=[
                {"id": 1, "prompt": "FAIL_CODEX"},
                {"id": 2, "prompt": "Still run this."},
            ]
        )

        completed, output = self.run_runner(skill)

        self.assertEqual(completed.returncode, 1)
        failed = output / "current" / "eval-1"
        later = output / "current" / "eval-2"
        result = json.loads((failed / "result.json").read_text())
        self.assertEqual(result["codex_exit_code"], 7)
        self.assertEqual(result["error"], "codex exited with code 7")
        self.assertEqual((failed / "stderr.txt").read_text(), "fake codex failure\n")
        self.assertEqual(
            json.loads((later / "result.json").read_text())["codex_exit_code"], 0
        )

    def test_failed_setup_and_invalid_workspace_do_not_invoke_codex(self):
        skill = self.make_skill(
            evals=[
                {
                    "id": 1,
                    "prompt": "Never run.",
                    "execution": {
                        "setup": {
                            "command": [
                                sys.executable,
                                "-c",
                                "import sys; sys.exit(9)",
                            ]
                        },
                        "workspace": "{run_root}/work/repo",
                    },
                },
                {
                    "id": 2,
                    "prompt": "Never run either.",
                    "execution": {
                        "setup": {"command": [sys.executable, "-c", "pass"]},
                        "workspace": "{run_root}/../escape",
                    },
                },
            ]
        )

        completed, output = self.run_runner(skill)

        self.assertEqual(completed.returncode, 1)
        first = json.loads(
            (output / "current/eval-1/result.json").read_text()
        )
        second = json.loads(
            (output / "current/eval-2/result.json").read_text()
        )
        self.assertEqual(first["setup_exit_code"], 9)
        self.assertIsNone(first["codex_exit_code"])
        self.assertIn("inside the run directory", second["error"])
        self.assertFalse((output / "current/eval-1/work/repo/codex-ran.txt").exists())

    def test_missing_codex_is_a_failed_result(self):
        skill = self.make_skill(evals=[{"id": 1, "prompt": "Try to run."}])

        completed, output = self.run_runner(skill, with_codex=False)

        self.assertEqual(completed.returncode, 1)
        result = json.loads(
            (output / "current/eval-1/result.json").read_text()
        )
        self.assertIsNone(result["codex_exit_code"])
        self.assertIn("codex", result["error"])

    def test_pilot_metadata_stages_all_declared_workspaces(self):
        completed, output = self.run_runner(PILOT)

        self.assertEqual(completed.returncode, 0, completed.stderr)
        expected = {
            1: "queue-runner",
            2: "verification-runner",
            3: "work",
            4: "api",
            5: "evidence-flow",
        }
        for eval_id, workspace_name in expected.items():
            result = json.loads(
                (output / f"current/eval-{eval_id}/result.json").read_text()
            )
            self.assertEqual(Path(result["workspace"]).name, workspace_name)
            self.assertTrue(Path(result["workspace"], "codex-ran.txt").is_file())

    def test_unknown_and_modified_placeholders_are_rejected(self):
        skill = self.make_skill(
            evals=[
                {
                    "id": 1,
                    "prompt": "Never run.",
                    "execution": {
                        "setup": {
                            "command": [sys.executable, "-c", "pass"],
                            "env": {"TARGET": "{unknown}/work"},
                        },
                        "workspace": "{run_root}/work",
                    },
                },
                {
                    "id": 2,
                    "prompt": "Never run either.",
                    "execution": {
                        "setup": {"command": [sys.executable, "-c", "pass"]},
                        "workspace": "{run_root!r}/work",
                    },
                },
                {
                    "id": 3,
                    "prompt": "Missing command.",
                    "execution": {
                        "setup": {},
                        "workspace": "{run_root}/work",
                    },
                },
            ]
        )

        completed, output = self.run_runner(skill)

        self.assertEqual(completed.returncode, 1)
        first = json.loads(
            (output / "current/eval-1/result.json").read_text()
        )
        second = json.loads(
            (output / "current/eval-2/result.json").read_text()
        )
        third = json.loads(
            (output / "current/eval-3/result.json").read_text()
        )
        self.assertIn("unknown placeholders", first["error"])
        self.assertIn("literal {run_root}", second["error"])
        self.assertIn("non-empty argument array", third["error"])

    def test_setup_created_workspace_symlink_cannot_escape_run_directory(self):
        outside = self.root / "outside"
        skill = self.make_skill(
            evals=[
                {
                    "id": 1,
                    "prompt": "Never run outside.",
                    "execution": {
                        "setup": {
                            "command": [
                                sys.executable,
                                "-c",
                                (
                                    "import os,pathlib;"
                                    "outside=pathlib.Path(os.environ['OUTSIDE']);"
                                    "outside.mkdir();"
                                    "link=pathlib.Path(os.environ['LINK']);"
                                    "link.parent.mkdir();"
                                    "link.symlink_to(outside, target_is_directory=True)"
                                ),
                            ],
                            "env": {
                                "LINK": "{run_root}/work/repo",
                                "OUTSIDE": str(outside),
                            },
                        },
                        "workspace": "{run_root}/work/repo",
                    },
                }
            ]
        )

        completed, output = self.run_runner(skill)

        self.assertEqual(completed.returncode, 1)
        result = json.loads(
            (output / "current/eval-1/result.json").read_text()
        )
        self.assertEqual(result["setup_exit_code"], 0)
        self.assertIsNone(result["codex_exit_code"])
        self.assertIn("remain inside the run directory", result["error"])
        self.assertFalse((outside / "codex-ran.txt").exists())

    def test_boolean_eval_id_is_rejected_as_invalid_metadata(self):
        skill = self.make_skill(evals=[{"id": True, "prompt": "Never run."}])

        completed, output = self.run_runner(skill)

        self.assertEqual(completed.returncode, 2)
        self.assertIn("integer id", completed.stderr)
        self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
