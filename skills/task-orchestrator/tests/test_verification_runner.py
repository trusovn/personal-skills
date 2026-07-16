import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import unittest


SANDBOX_EXEC = Path("/usr/bin/sandbox-exec")
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
