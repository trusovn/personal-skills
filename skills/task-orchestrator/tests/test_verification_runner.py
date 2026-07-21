import copy
import hashlib
import os
import importlib.util
import json
from pathlib import Path
import shlex
import signal
import socket
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest import mock


SANDBOX_EXEC = Path("/usr/bin/sandbox-exec")
RUNNER_PATH = Path(__file__).parents[1] / "scripts" / "verification_runner.py"
def load_verification_runner():
    spec = importlib.util.spec_from_file_location(
        "task_orchestrator_verification_runner", RUNNER_PATH
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class VerificationPlanShellSyntaxTests(unittest.TestCase):
    def setUp(self):
        self.runner = load_verification_runner()

    def policy(self, checks, *, repository_gate=None, gap=None, dependency_install=False):
        return {
            "verification": {
                "targeted_checks": checks,
                "repository_gate": repository_gate,
                "authorized_gap": gap,
            },
            "permissions": {"dependency_install": dependency_install},
        }

    def test_explicit_shell_launcher_is_rejected(self):
        task = {"required_checks": []}
        policy = self.policy(["/bin/sh -c 'python3 -m unittest'"])

        with self.assertRaisesRegex(ValueError, "shell launcher"):
            self.runner.build_verification_plan(task, policy)

    def test_each_shell_launcher_is_rejected(self):
        for launcher in sorted(self.runner.SHELL_LAUNCHERS):
            with self.subTest(launcher=launcher):
                with self.assertRaisesRegex(ValueError, "shell launcher"):
                    self.runner.build_verification_plan(
                        {"required_checks": []}, self.policy([f"/bin/{launcher} -c true"])
                    )

    def test_each_prohibited_syntax_family_is_rejected(self):
        cases = {
            "empty": "   ",
            "nul": "python3\x00-m unittest",
            "newline": "python3\n-m unittest",
            "malformed quote": "python3 'unterminated",
            "leading assignment": "MODE=test python3 -m unittest",
            "env launcher": "/usr/bin/env python3 -m unittest",
            "control token": "python3 && true",
            "redirection token": "python3 2> output.log",
            "dollar substitution": "python3 $(which pytest)",
            "backtick substitution": "python3 `which pytest`",
        }
        for name, value in cases.items():
            with self.subTest(name=name):
                with self.assertRaises(ValueError):
                    self.runner.build_verification_plan(
                        {"required_checks": []}, self.policy([value])
                    )

    def test_each_supported_standalone_shell_token_is_rejected(self):
        tokens = sorted(self.runner._CONTROL_TOKENS) + [
            "<", "<<", "<<<", "1>", "2>>", "&>", "&>>", "0<&", "2>&",
        ]
        for token in tokens:
            with self.subTest(token=token):
                with self.assertRaisesRegex(ValueError, "standalone shell token"):
                    self.runner.build_verification_plan(
                        {"required_checks": []}, self.policy([f"python3 {token} output"])
                    )

    def test_quoted_arguments_and_literal_metacharacters_remain_data(self):
        plan = self.runner.build_verification_plan(
            {"required_checks": []},
            self.policy([
                "python3 -m unittest 'tests/path with spaces.py' 'name;still-data' '*'"
            ]),
        )
        self.assertEqual(
            plan["commands"][0]["argv"],
            [
                "python3", "-m", "unittest", "tests/path with spaces.py",
                "name;still-data", "*",
            ],
        )


class VerificationPlanConstructionTests(unittest.TestCase):
    def setUp(self):
        self.runner = load_verification_runner()

    def policy(self, checks, *, repository_gate=None, gap=None, dependency_install=False):
        return {
            "verification": {
                "targeted_checks": checks,
                "repository_gate": repository_gate,
                "authorized_gap": gap,
            },
            "permissions": {"dependency_install": dependency_install},
        }

    def test_order_deduplication_and_all_provenance_are_deterministic(self):
        task = {"required_checks": ["python3 -m unittest test_one", "make task"]}
        policy = self.policy(
            [" python3   -m unittest 'test_one' ", "make targeted"],
            repository_gate="make verify",
        )
        plan = self.runner.build_verification_plan(task, policy)

        self.assertEqual(
            [command["argv"] for command in plan["commands"]],
            [
                ["python3", "-m", "unittest", "test_one"],
                ["make", "task"],
                ["make", "targeted"],
                ["make", "verify"],
            ],
        )
        self.assertEqual(
            plan["commands"][0]["roles"], ["task_required", "policy_targeted"]
        )
        self.assertEqual(
            [item["original"] for item in plan["commands"][0]["provenance"]],
            ["python3 -m unittest test_one", " python3   -m unittest 'test_one' "],
        )
        self.assertEqual(
            [command["id"] for command in plan["commands"]],
            ["command-001", "command-002", "command-003", "command-004"],
        )
        self.assertEqual(plan, self.runner.build_verification_plan(task, policy))

    def test_repository_gap_is_exact_and_targeted_overlap_is_not_excusable(self):
        gap = {"reason": "legacy flakes", "owner": "tools", "follow_up": "TASK-12"}
        gate_only = self.runner.build_verification_plan(
            {"required_checks": []},
            self.policy(["make targeted"], repository_gate="make verify", gap=gap),
        )
        gate = gate_only["commands"][1]
        self.assertEqual(gate["authorized_gap"], gap)
        self.assertTrue(gate["gap_excusable"])
        self.assertIsNone(gate_only["commands"][0]["authorized_gap"])

        overlap = self.runner.build_verification_plan(
            {"required_checks": []},
            self.policy(["make verify"], repository_gate=" make 'verify' ", gap=gap),
        )
        self.assertEqual(
            overlap["commands"][0]["roles"], ["policy_targeted", "repository_gate"]
        )
        self.assertEqual(overlap["commands"][0]["authorized_gap"], gap)
        self.assertFalse(overlap["commands"][0]["gap_excusable"])

    def test_gap_without_repository_gate_is_rejected(self):
        gap = {"reason": "legacy flakes", "owner": "tools", "follow_up": "TASK-12"}
        with self.assertRaisesRegex(ValueError, "requires a repository gate"):
            self.runner.build_verification_plan(
                {"required_checks": []}, self.policy(["make targeted"], gap=gap)
            )

    def test_digests_bind_plan_contents_and_inputs_are_unchanged(self):
        task = {"required_checks": ["make task"]}
        policy = self.policy(["make targeted"], repository_gate="make verify")
        original_task = copy.deepcopy(task)
        original_policy = copy.deepcopy(policy)
        plan = self.runner.build_verification_plan(task, policy)

        self.assertEqual(task, original_task)
        self.assertEqual(policy, original_policy)
        self.assertEqual(json.loads(json.dumps(plan)), plan)
        self.assertEqual(
            plan["plan_sha256"],
            hashlib.sha256(json.dumps(
                {"version": plan["version"], "commands": plan["commands"]},
                sort_keys=True, separators=(",", ":"),
            ).encode()).hexdigest(),
        )
        for command in plan["commands"]:
            unsigned = {key: value for key, value in command.items() if key != "command_sha256"}
            self.assertEqual(
                command["command_sha256"],
                hashlib.sha256(json.dumps(
                    unsigned, sort_keys=True, separators=(",", ":")
                ).encode()).hexdigest(),
            )

        changed_argv = self.runner.build_verification_plan(
            task, self.policy(["make changed"], repository_gate="make verify")
        )
        ordered = self.runner.build_verification_plan(
            {"required_checks": []}, self.policy(["make one", "make two"])
        )
        reordered = self.runner.build_verification_plan(
            {"required_checks": []}, self.policy(["make two", "make one"])
        )
        duplicated = self.runner.build_verification_plan(
            {"required_checks": ["make same"]}, self.policy([" make 'same' "])
        )
        dropped_provenance = copy.deepcopy(duplicated)
        dropped_provenance["commands"][0]["provenance"].pop()
        recalculated = hashlib.sha256(json.dumps(
            {"version": dropped_provenance["version"], "commands": dropped_provenance["commands"]},
            sort_keys=True, separators=(",", ":"),
        ).encode()).hexdigest()
        self.assertNotEqual(plan["plan_sha256"], changed_argv["plan_sha256"])
        self.assertNotEqual(ordered["plan_sha256"], reordered["plan_sha256"])
        self.assertNotEqual(dropped_provenance["plan_sha256"], recalculated)

        task["required_checks"][0] = "make mutated-later"
        policy["verification"]["targeted_checks"][0] = "make mutated-later"
        self.assertEqual(plan["commands"][0]["argv"], ["make", "task"])


class VerificationPlanInstallDenialTests(unittest.TestCase):
    CASES = {
        "pip": "pip3 install requests",
        "easy-install": "easy_install-3.12 requests",
        "uv": "uv pip install requests",
        "poetry": "poetry add requests",
        "pipenv": "pipenv sync",
        "npm": "npm ci",
        "npx": "npx package",
        "pnpm": "pnpm dlx package",
        "pnpx": "pnpx package",
        "yarn": "yarn add package",
        "bun": "bun install",
        "bunx": "bunx package",
        "conda-family": "micromamba create -n test",
        "gem": "gem install package",
        "bundler": "bundle install",
        "cargo": "cargo install tool",
        "go": "go get example.test/module",
        "dotnet": "dotnet restore",
        "composer": "composer require package",
        "brew": "brew install package",
        "apt": "apt-get install package",
        "dnf-yum": "dnf install package",
        "apk": "apk add package",
        "pacman": "pacman -S package",
        "zypper": "zypper in package",
        "winget": "winget install package",
        "choco": "choco install package",
        "scoop": "scoop install package",
        "python-module-pip": "python3 -I -m pip install package",
        "python-module-ensurepip": "python3 -m ensurepip",
        "dotnet-add-package": "dotnet add app.csproj package Example",
    }

    def setUp(self):
        self.runner = load_verification_runner()

    def plan(self, command, *, dependency_install=False):
        return self.runner.build_verification_plan(
            {"required_checks": []},
            {
                "verification": {
                    "targeted_checks": [command],
                    "repository_gate": None,
                    "authorized_gap": None,
                },
                "permissions": {"dependency_install": dependency_install},
            },
        )

    def test_each_closed_table_row_is_denied_and_reports_the_rule(self):
        table_rules = {row[0] for row in self.runner.INSTALL_SUBCOMMAND_RULES}
        self.assertEqual(table_rules | {
            "python-module-pip", "python-module-ensurepip", "dotnet-add-package"
        }, set(self.CASES))
        for rule, command in self.CASES.items():
            with self.subTest(rule=rule, command=command):
                with self.assertRaises(self.runner.VerificationPlanError) as raised:
                    self.plan(command)
                self.assertEqual(raised.exception.matched_rule, rule)

    def test_dependency_install_true_permits_a_matched_request(self):
        plan = self.plan("python3 -m pip install package", dependency_install=True)
        self.assertEqual(
            plan["commands"][0]["argv"], ["python3", "-m", "pip", "install", "package"]
        )

    def test_near_miss_test_commands_are_not_a_substring_blacklist(self):
        for command in (
            "python3 -m unittest install_tests",
            "pip list",
            "npm test",
            "cargo test",
            "go test ./...",
            "dotnet test",
            "make reinstall-check",
        ):
            with self.subTest(command=command):
                self.assertEqual(self.plan(command)["commands"][0]["argv"][0], command.split()[0])


def _sandbox_invocation(
    argv,
    permissions,
    *,
    platform=sys.platform,
    sandbox_executable=SANDBOX_EXEC,
):
    return load_verification_runner().build_sandbox_invocation(
        argv,
        permissions,
        platform=platform,
        sandbox_executable=sandbox_executable,
    )


def _run(argv, permissions):
    invocation = _sandbox_invocation(argv, permissions)
    return subprocess.run(
        invocation,
        capture_output=True,
        text=True,
        timeout=5,
        check=False,
    )


def _permissions(sandbox, roots, *, network=False, danger_authorized=False):
    return {
        "sandbox": sandbox,
        "approval_policy": "never",
        "network": network,
        "dependency_install": False,
        "writable_roots": [str(root) for root in roots],
        "danger_full_access_authorized": danger_authorized,
    }


def _loopback_attempt(permissions=None):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        listener.bind(("127.0.0.1", 0))
        listener.listen(1)
        listener.settimeout(3)
        port = listener.getsockname()[1]
        script = (
            "import socket; "
            f"s=socket.create_connection(('127.0.0.1',{port}),timeout=2); "
            "s.sendall(b'proof'); s.close()"
        )
        argv = [sys.executable, "-I", "-c", script]
        if permissions is None:
            result = subprocess.run(
                argv,
                capture_output=True,
                text=True,
                timeout=5,
                check=False,
            )
        else:
            result = _run(argv, permissions)

        payload = None
        if result.returncode == 0:
            connection, _ = listener.accept()
            with connection:
                payload = connection.recv(5)
        return result, payload


@unittest.skipUnless(
    sys.platform == "darwin" and SANDBOX_EXEC.is_file(),
    "the adopted capability proof requires macOS /usr/bin/sandbox-exec",
)
class VerificationSandboxCapabilityTests(unittest.TestCase):
    def test_supported_host_enforces_version_1_permission_matrix(self):
        with tempfile.TemporaryDirectory(prefix="task-orchestrator-sandbox-") as temporary:
            base = Path(temporary).resolve()
            root_one = base / "root-one"
            root_two = base / "root-two"
            outside = base / "outside"
            root_one.mkdir()
            root_two.mkdir()
            outside.mkdir()

            control_file = outside / "control-write"
            control_file.write_text("control", encoding="utf-8")
            self.assertEqual(control_file.read_text(encoding="utf-8"), "control")
            control_network, control_payload = _loopback_attempt()
            self.assertEqual(control_network.returncode, 0, control_network.stderr)
            self.assertEqual(control_payload, b"proof")

            workspace = _permissions(
                "workspace-write",
                [root_one, root_two],
                network=True,
            )
            authorized = _run(["/usr/bin/true"], workspace)
            self.assertEqual(authorized.returncode, 0, authorized.stderr)
            for index, root in enumerate((root_one, root_two), start=1):
                target = root / f"inside-{index}"
                result = _run(["/usr/bin/touch", target], workspace)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertTrue(target.is_file())

            read_only_permissions = _permissions(
                "read-only", [root_one], network=False
            )
            read_only_command = _run(["/usr/bin/true"], read_only_permissions)
            self.assertEqual(read_only_command.returncode, 0, read_only_command.stderr)
            read_only_target = root_one / "read-only-denied"
            read_only = _run(
                ["/usr/bin/touch", read_only_target],
                read_only_permissions,
            )
            self.assertNotEqual(read_only.returncode, 0)
            self.assertFalse(read_only_target.exists())

            outside_target = outside / "workspace-denied"
            outside_write = _run(["/usr/bin/touch", outside_target], workspace)
            self.assertNotEqual(outside_write.returncode, 0)
            self.assertFalse(outside_target.exists())

            allowed_network, allowed_payload = _loopback_attempt(workspace)
            self.assertEqual(allowed_network.returncode, 0, allowed_network.stderr)
            self.assertEqual(allowed_payload, b"proof")
            denied_network, denied_payload = _loopback_attempt(
                _permissions("workspace-write", [root_one], network=False)
            )
            self.assertNotEqual(denied_network.returncode, 0)
            self.assertIsNone(denied_payload)

            danger_target = outside / "danger-authorized"
            danger = _run(
                ["/usr/bin/touch", danger_target],
                _permissions(
                    "danger-full-access",
                    [],
                    network=False,
                    danger_authorized=True,
                ),
            )
            self.assertEqual(danger.returncode, 0, danger.stderr)
            self.assertTrue(danger_target.is_file())


class VerificationSandboxFailClosedTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="task-orchestrator-config-")
        self.root = Path(self.temporary.name).resolve()

    def tearDown(self):
        self.temporary.cleanup()

    def test_production_builds_the_adopted_sandbox_invocation(self):
        runner = load_verification_runner()
        permissions = _permissions("read-only", [], network=False)

        invocation = runner.build_sandbox_invocation(
            ["/usr/bin/true"], permissions
        )

        self.assertEqual(invocation, _sandbox_invocation(["/usr/bin/true"], permissions))

    def test_unsupported_host_is_rejected(self):
        permissions = _permissions("read-only", [], network=False)
        with self.assertRaisesRegex(RuntimeError, "only on macOS"):
            _sandbox_invocation(["/usr/bin/true"], permissions, platform="linux")

    def test_unsupported_mode_is_rejected(self):
        permissions = _permissions("unknown", [], network=False)
        with self.assertRaisesRegex(RuntimeError, "unsupported sandbox mode"):
            _sandbox_invocation(["/usr/bin/true"], permissions)

    def test_substituted_unrestricted_runner_is_rejected(self):
        permissions = _permissions("read-only", [], network=False)
        with self.assertRaisesRegex(RuntimeError, "exact /usr/bin/sandbox-exec"):
            _sandbox_invocation(
                ["/usr/bin/true"],
                permissions,
                sandbox_executable=Path("/usr/bin/true"),
            )

    def test_missing_writable_root_enforcement_is_rejected(self):
        missing = self.root / "missing"
        permissions = _permissions("workspace-write", [missing], network=False)
        with self.assertRaisesRegex(RuntimeError, "existing absolute directory"):
            _sandbox_invocation(["/usr/bin/true"], permissions)

    def test_unauthorized_danger_full_access_is_rejected_before_launch(self):
        marker = self.root / "must-not-run"
        permissions = _permissions("danger-full-access", [], network=False)
        with self.assertRaisesRegex(RuntimeError, "lacks separate authorization"):
            _run(["/usr/bin/touch", marker], permissions)
        self.assertFalse(marker.exists())

    def test_incomplete_permission_envelope_is_rejected(self):
        permissions = _permissions("read-only", [], network=False)
        permissions.pop("network")
        with self.assertRaisesRegex(RuntimeError, "complete version 1"):
            _sandbox_invocation(["/usr/bin/true"], permissions)


class VerificationProcessGroupCleanupTests(unittest.TestCase):
    def test_group_exit_race_does_not_leak_permission_error(self):
        runner = load_verification_runner()
        process = mock.Mock(pid=43210)
        signal_calls = []
        sigkill_attempts = 0

        def group_exit_race(process_group_id, signum):
            nonlocal sigkill_attempts
            signal_calls.append((process_group_id, signum))
            if signum == signal.SIGKILL:
                sigkill_attempts += 1
                if sigkill_attempts == 1:
                    raise PermissionError(1, "Operation not permitted")
                raise ProcessLookupError
            if signum == 0 and sigkill_attempts:
                raise ProcessLookupError

        with mock.patch.object(runner.os, "killpg", side_effect=group_exit_race):
            runner._terminate_process_group(process)

        permission_error_index = signal_calls.index((process.pid, signal.SIGKILL))
        self.assertIn((process.pid, 0), signal_calls[permission_error_index + 1:])


@unittest.skipUnless(
    sys.platform == "darwin" and SANDBOX_EXEC.is_file(),
    "the adopted executor requires macOS /usr/bin/sandbox-exec",
)
class VerificationExecutorLocalProcessTests(unittest.TestCase):
    def setUp(self):
        self.runner = load_verification_runner()
        self.temporary = tempfile.TemporaryDirectory(prefix="task-orchestrator-executor-")
        self.base = Path(self.temporary.name).resolve()
        self.repository = self.base / "repository"
        self.run_directory = self.base / "run"
        self.verification_directory = self.run_directory / "verification"
        self.repository.mkdir()
        self.verification_directory.mkdir(parents=True)
        self.permissions = _permissions(
            "workspace-write", [self.repository], network=False
        )

    def tearDown(self):
        self.temporary.cleanup()

    def closure_identity(self):
        return {
            "subject": {
                "run_id": "run-1",
                "task_id": "T1",
                "attempt_id": "attempt-001",
                "turn": 1,
                "policy_sha256": "1" * 64,
                "manifest_sha256": "2" * 64,
                "prompt_sha256": "3" * 64,
                "selected_task_baseline_sha256": "4" * 64,
            },
            "stage2_git_evidence_sha256": "5" * 64,
            "post_worker_head_oid": "a" * 40,
            "post_worker_index_tree_oid": "b" * 40,
            "post_worker_status_sha256": "6" * 64,
        }

    def command(self, script):
        return shlex.join([sys.executable, "-I", "-c", script])

    def plan(self, *commands, repository_gate=None, gap=None):
        return self.runner.build_verification_plan(
            {"required_checks": list(commands)},
            {
                "verification": {
                    "targeted_checks": [],
                    "repository_gate": repository_gate,
                    "authorized_gap": gap,
                },
                "permissions": {"dependency_install": False},
            },
        )

    def execute(self, plan, **overrides):
        arguments = {
            "plan": plan,
            "repository_cwd": self.repository,
            "permissions": self.permissions,
            "timeout_seconds": 2,
            "run_directory": self.run_directory,
            "execution_path": "verification/attempt-001.turn-001.execution.json",
            "closure_identity": self.closure_identity(),
        }
        arguments.update(overrides)
        return self.runner.execute_verification_plan(**arguments)

    def assert_pid_absent(self, pid):
        deadline = time.monotonic() + 2
        while time.monotonic() < deadline:
            try:
                os.kill(pid, 0)
            except ProcessLookupError:
                return
            threading.Event().wait(0.01)
        self.fail(f"process {pid} remained alive")

    def test_two_commands_publish_exact_binary_logs_and_valid_record(self):
        marker = self.repository / "order"
        first = self.command(
            f"import os; from pathlib import Path; "
            f"Path({str(marker)!r}).write_bytes(b'1'); os.write(1,b'\\xff\\x00')"
        )
        second = self.command(
            f"import os; from pathlib import Path; p=Path({str(marker)!r}); "
            f"assert p.read_bytes()==b'1'; p.write_bytes(b'12'); os.write(2,b'\\x80')"
        )

        record, digest = self.execute(self.plan(first, second))

        self.assertEqual(marker.read_bytes(), b"12")
        self.assertEqual(record["terminal_reason"], "complete")
        self.assertEqual([item["status"] for item in record["outcomes"]], ["passed", "passed"])
        expected_streams = ((b"\xff\x00", b""), (b"", b"\x80"))
        for outcome, (stdout, stderr) in zip(record["outcomes"], expected_streams):
            self.assertEqual((self.run_directory / outcome["stdout_path"]).read_bytes(), stdout)
            self.assertEqual((self.run_directory / outcome["stderr_path"]).read_bytes(), stderr)
            self.assertEqual(outcome["stdout_sha256"], hashlib.sha256(stdout).hexdigest())
            self.assertEqual(outcome["stderr_sha256"], hashlib.sha256(stderr).hexdigest())
            self.assertEqual(outcome["effective_argv"][0], str(SANDBOX_EXEC))
        record_bytes = (
            self.verification_directory / "attempt-001.turn-001.execution.json"
        ).read_bytes()
        self.assertEqual(json.loads(record_bytes), record)
        self.assertEqual(hashlib.sha256(record_bytes).hexdigest(), digest)
        self.assertEqual(record["effective_envelope"], self.permissions)

    def test_repository_gate_failure_records_the_exact_authorized_gap(self):
        gap = {"reason": "legacy failure", "owner": "tools", "follow_up": "T2"}
        plan = self.plan(repository_gate="/usr/bin/false", gap=gap)

        record, _ = self.execute(plan)

        self.assertEqual(record["terminal_reason"], "authorized_gap")
        self.assertEqual(record["authorized_gap"], gap)
        self.assertEqual(record["outcomes"][0]["status"], "authorized_gap")
        self.assertNotEqual(record["outcomes"][0]["exit_code"], 0)

    def test_later_preflight_failure_runs_nothing_and_creates_no_artifact(self):
        marker = self.repository / "must-not-run"
        first = self.command(f"from pathlib import Path; Path({str(marker)!r}).touch()")
        plan = self.plan(first, "executable-that-does-not-exist --version")

        with self.assertRaisesRegex(RuntimeError, "not resolvable"):
            self.execute(plan)

        self.assertFalse(marker.exists())
        self.assertEqual(list(self.verification_directory.iterdir()), [])

    def test_targeted_failure_prevents_the_later_command(self):
        marker = self.repository / "must-not-run"
        later = self.command(f"from pathlib import Path; Path({str(marker)!r}).touch()")

        record, _ = self.execute(self.plan("/usr/bin/false", later))

        self.assertEqual(record["terminal_reason"], "command_failed")
        self.assertEqual(len(record["outcomes"]), 1)
        self.assertEqual(record["outcomes"][0]["status"], "failed")
        self.assertFalse(marker.exists())
        self.assertFalse((
            self.verification_directory
            / "attempt-001.turn-001.command-002.stdout.log"
        ).exists())

    def test_timeout_terminates_the_owned_child_and_grandchild(self):
        pids = self.repository / "pids"
        grandchild = "import time; time.sleep(60)"
        script = (
            "import os,subprocess,sys,time; from pathlib import Path; "
            f"child=subprocess.Popen([sys.executable,'-I','-c',{grandchild!r}]); "
            f"Path({str(pids)!r}).write_text(str(os.getpid())+' '+str(child.pid)); "
            "time.sleep(60)"
        )

        record, _ = self.execute(self.plan(self.command(script)), timeout_seconds=0.25)

        self.assertEqual(record["terminal_reason"], "timed_out")
        self.assertEqual(record["outcomes"][0]["status"], "timed_out")
        parent_pid, child_pid = map(int, pids.read_text().split())
        self.assert_pid_absent(parent_pid)
        self.assert_pid_absent(child_pid)

    def test_timeout_kills_a_grandchild_that_ignores_sigterm(self):
        pids = self.repository / "signal-resistant-pids"
        child_log = self.repository / "signal-resistant-child.log"
        grandchild = "import time; time.sleep(60)"
        script = (
            "import os,signal,subprocess,sys,time; from pathlib import Path; "
            f"sink=open({str(child_log)!r},'wb'); "
            f"child=subprocess.Popen([sys.executable,'-I','-c',{grandchild!r}],"
            "stdout=sink,stderr=sink,"
            "preexec_fn=lambda:signal.signal(signal.SIGTERM,signal.SIG_IGN)); "
            "sink.close(); "
            f"Path({str(pids)!r}).write_text(str(os.getpid())+' '+str(child.pid)); "
            "time.sleep(60)"
        )

        record, _ = self.execute(self.plan(self.command(script)), timeout_seconds=0.25)

        self.assertEqual(
            record["terminal_reason"],
            "timed_out",
            (self.run_directory / record["outcomes"][0]["stderr_path"]).read_text(),
        )
        self.assertEqual(record["outcomes"][0]["status"], "timed_out")
        parent_pid, child_pid = map(int, pids.read_text().split())
        try:
            self.assert_pid_absent(parent_pid)
            self.assert_pid_absent(child_pid)
        finally:
            for pid in (parent_pid, child_pid):
                try:
                    os.kill(pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass

    def test_exited_parent_with_open_descendant_pipe_cleans_up_process_group(self):
        pids = self.repository / "inherited-pipe-pids"
        grandchild = "import time; time.sleep(60)"
        script = (
            "import os,subprocess,sys; from pathlib import Path; "
            f"child=subprocess.Popen([sys.executable,'-I','-c',{grandchild!r}]); "
            f"Path({str(pids)!r}).write_text(str(os.getpid())+' '+str(child.pid))"
        )
        watchdog_cleanup_required = threading.Event()
        observed_pids = []

        def clean_up_if_runner_does_not():
            deadline = time.monotonic() + 2
            while not pids.exists() and time.monotonic() < deadline:
                threading.Event().wait(0.01)
            if not pids.exists():
                return
            parent_pid, child_pid = map(int, pids.read_text().split())
            observed_pids.extend((parent_pid, child_pid))
            deadline = time.monotonic() + 3
            while time.monotonic() < deadline:
                try:
                    os.kill(child_pid, 0)
                except ProcessLookupError:
                    return
                threading.Event().wait(0.01)
            watchdog_cleanup_required.set()
            try:
                os.killpg(parent_pid, signal.SIGKILL)
            except ProcessLookupError:
                pass

        watchdog = threading.Thread(target=clean_up_if_runner_does_not)
        watchdog.start()
        try:
            try:
                self.execute(self.plan(self.command(script)), timeout_seconds=2)
            except RuntimeError:
                pass
        finally:
            watchdog.join(timeout=6)
            for pid in observed_pids:
                try:
                    os.kill(pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass

        self.assertFalse(
            watchdog_cleanup_required.is_set(),
            "the runner left a grandchild alive after its group leader exited",
        )

    def test_external_interruption_terminates_the_process_group(self):
        ready = self.repository / "ready"
        script = (
            "import os,time; from pathlib import Path; "
            f"Path({str(ready)!r}).write_text(str(os.getpid())); time.sleep(60)"
        )
        interrupted = threading.Event()
        watcher_done = threading.Event()

        def interrupt_when_started():
            while not ready.exists() and not watcher_done.wait(0.01):
                pass
            if ready.exists():
                interrupted.set()

        watcher = threading.Thread(target=interrupt_when_started)
        watcher.start()
        try:
            record, _ = self.execute(
                self.plan(self.command(script)), interruption_event=interrupted
            )
        finally:
            watcher_done.set()
            watcher.join(timeout=1)

        self.assertEqual(record["terminal_reason"], "interrupted")
        self.assertEqual(record["outcomes"][0]["status"], "interrupted")
        self.assert_pid_absent(int(ready.read_text()))

    def test_existing_log_collision_is_rejected_without_overwrite_or_execution(self):
        existing = (
            self.verification_directory
            / "attempt-001.turn-001.command-002.stdout.log"
        )
        existing.write_bytes(b"owned")
        marker = self.repository / "must-not-run"
        command = self.command(f"from pathlib import Path; Path({str(marker)!r}).touch()")

        with self.assertRaisesRegex(FileExistsError, "already exists"):
            self.execute(self.plan(command, "/usr/bin/true"))

        self.assertEqual(existing.read_bytes(), b"owned")
        self.assertFalse(marker.exists())
        self.assertFalse((
            self.verification_directory / "attempt-001.turn-001.execution.json"
        ).exists())

    def test_existing_record_is_rejected_without_overwrite(self):
        record_path = (
            self.verification_directory / "attempt-001.turn-001.execution.json"
        )
        record_path.write_bytes(b"owned")

        with self.assertRaisesRegex(FileExistsError, "already exists"):
            self.execute(self.plan("/usr/bin/true"))

        self.assertEqual(record_path.read_bytes(), b"owned")
        self.assertEqual(
            sorted(path.name for path in self.verification_directory.iterdir()),
            ["attempt-001.turn-001.execution.json"],
        )

    def test_log_write_failure_cannot_publish_a_complete_record(self):
        stdout_path = (
            self.verification_directory
            / "attempt-001.turn-001.command-001.stdout.log"
        )
        original_open = Path.open

        class FailingWriter:
            def __init__(self, wrapped):
                self.wrapped = wrapped

            def __enter__(self):
                return self

            def __exit__(self, *args):
                self.wrapped.close()

            def write(self, value):
                raise OSError("injected log failure")

            def flush(self):
                self.wrapped.flush()

            def fileno(self):
                return self.wrapped.fileno()

        def fail_target(path, mode="r", *args, **kwargs):
            opened = original_open(path, mode, *args, **kwargs)
            if path == stdout_path and mode == "xb":
                return FailingWriter(opened)
            return opened

        command = self.command("import os; os.write(1,b'output')")
        with mock.patch.object(Path, "open", fail_target):
            with self.assertRaisesRegex(RuntimeError, "log streaming failed"):
                self.execute(self.plan(command))

        self.assertFalse((
            self.verification_directory / "attempt-001.turn-001.execution.json"
        ).exists())

    def test_changed_executable_is_rejected_before_launch(self):
        plan = self.plan("/usr/bin/true")
        original = self.runner._resolve_executable
        calls = 0

        def changed_on_recheck(argv, cwd):
            nonlocal calls
            calls += 1
            resolved, fingerprint = original(argv, cwd)
            if calls == 2:
                fingerprint = (*fingerprint[:-1], "0" * 64)
            return resolved, fingerprint

        with mock.patch.object(self.runner, "_resolve_executable", changed_on_recheck):
            with self.assertRaisesRegex(RuntimeError, "changed before launch"):
                self.execute(plan)

        self.assertFalse((
            self.verification_directory / "attempt-001.turn-001.execution.json"
        ).exists())

    def test_invalid_identity_timeout_and_artifact_escape_fail_before_artifacts(self):
        plan = self.plan("/usr/bin/true")
        invalid_identity = self.closure_identity()
        invalid_identity["subject"]["turn"] = 0
        cases = (
            {"closure_identity": invalid_identity},
            {"timeout_seconds": 0},
            {"execution_path": "verification/../escape.execution.json"},
        )
        for overrides in cases:
            with self.subTest(overrides=overrides), self.assertRaises((ValueError, RuntimeError)):
                self.execute(plan, **overrides)
            self.assertEqual(list(self.verification_directory.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
