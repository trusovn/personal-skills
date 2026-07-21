import copy
import hashlib
import os
import importlib.util
import json
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import unittest


SANDBOX_EXEC = Path("/usr/bin/sandbox-exec")
RUNNER_PATH = Path(__file__).parents[1] / "scripts" / "verification_runner.py"
REQUIRED_PERMISSION_KEYS = {
    "sandbox",
    "approval_policy",
    "network",
    "dependency_install",
    "writable_roots",
    "danger_full_access_authorized",
}


class UnsupportedSandbox(RuntimeError):
    pass


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
    if platform != "darwin":
        raise UnsupportedSandbox("sandbox-exec verification is supported only on macOS")
    if (
        Path(sandbox_executable) != SANDBOX_EXEC
        or not SANDBOX_EXEC.is_file()
        or not os.access(SANDBOX_EXEC, os.X_OK)
    ):
        raise UnsupportedSandbox("the exact /usr/bin/sandbox-exec mechanism is unavailable")
    if not argv:
        raise UnsupportedSandbox("verification argv must not be empty")
    if set(permissions) != REQUIRED_PERMISSION_KEYS:
        raise UnsupportedSandbox("the complete version 1 permission envelope is required")
    if permissions["approval_policy"] != "never":
        raise UnsupportedSandbox("verification cannot request approval while running")
    if type(permissions["network"]) is not bool:
        raise UnsupportedSandbox("network must be boolean")
    if type(permissions["dependency_install"]) is not bool:
        raise UnsupportedSandbox("dependency_install must be boolean")
    if type(permissions["danger_full_access_authorized"]) is not bool:
        raise UnsupportedSandbox("danger_full_access_authorized must be boolean")

    sandbox = permissions["sandbox"]
    if sandbox not in {"read-only", "workspace-write", "danger-full-access"}:
        raise UnsupportedSandbox(f"unsupported sandbox mode: {sandbox!r}")
    if sandbox == "danger-full-access" and not permissions["danger_full_access_authorized"]:
        raise UnsupportedSandbox("danger-full-access lacks separate authorization")

    roots = permissions["writable_roots"]
    if not isinstance(roots, list) or any(not isinstance(root, str) or not root for root in roots):
        raise UnsupportedSandbox("writable_roots must be a list of non-empty paths")
    normalized_roots = []
    for root in roots:
        path = Path(root)
        if not path.is_absolute() or not path.is_dir():
            raise UnsupportedSandbox("every writable root must be an existing absolute directory")
        normalized = Path(os.path.realpath(path))
        if normalized == Path("/"):
            raise UnsupportedSandbox("workspace-write cannot use the filesystem root")
        if normalized not in normalized_roots:
            normalized_roots.append(normalized)

    profile = ["(version 1)", "(allow default)"]
    definitions = []
    if not permissions["network"]:
        profile.append("(deny network*)")

    if sandbox == "read-only":
        profile.append("(deny file-write*)")
    elif sandbox == "workspace-write":
        if not normalized_roots:
            profile.append("(deny file-write*)")
        else:
            exclusions = []
            for index, root in enumerate(normalized_roots):
                name = f"WRITABLE_ROOT_{index}"
                definitions.extend(["-D", f"{name}={root}"])
                exclusions.append(f'(require-not (subpath (param "{name}")))')
            profile.append(
                "(deny file-write* (require-all " + " ".join(exclusions) + "))"
            )

    return [
        str(SANDBOX_EXEC),
        *definitions,
        "-p",
        " ".join(profile),
        *map(str, argv),
    ]


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

    def test_unsupported_host_is_rejected(self):
        permissions = _permissions("read-only", [], network=False)
        with self.assertRaisesRegex(UnsupportedSandbox, "only on macOS"):
            _sandbox_invocation(["/usr/bin/true"], permissions, platform="linux")

    def test_unsupported_mode_is_rejected(self):
        permissions = _permissions("unknown", [], network=False)
        with self.assertRaisesRegex(UnsupportedSandbox, "unsupported sandbox mode"):
            _sandbox_invocation(["/usr/bin/true"], permissions)

    def test_substituted_unrestricted_runner_is_rejected(self):
        permissions = _permissions("read-only", [], network=False)
        with self.assertRaisesRegex(UnsupportedSandbox, "exact /usr/bin/sandbox-exec"):
            _sandbox_invocation(
                ["/usr/bin/true"],
                permissions,
                sandbox_executable=Path("/usr/bin/true"),
            )

    def test_missing_writable_root_enforcement_is_rejected(self):
        missing = self.root / "missing"
        permissions = _permissions("workspace-write", [missing], network=False)
        with self.assertRaisesRegex(UnsupportedSandbox, "existing absolute directory"):
            _sandbox_invocation(["/usr/bin/true"], permissions)

    def test_unauthorized_danger_full_access_is_rejected_before_launch(self):
        marker = self.root / "must-not-run"
        permissions = _permissions("danger-full-access", [], network=False)
        with self.assertRaisesRegex(UnsupportedSandbox, "lacks separate authorization"):
            _run(["/usr/bin/touch", marker], permissions)
        self.assertFalse(marker.exists())

    def test_incomplete_permission_envelope_is_rejected(self):
        permissions = _permissions("read-only", [], network=False)
        permissions.pop("network")
        with self.assertRaisesRegex(UnsupportedSandbox, "complete version 1"):
            _sandbox_invocation(["/usr/bin/true"], permissions)


if __name__ == "__main__":
    unittest.main()
