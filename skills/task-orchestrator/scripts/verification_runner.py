"""Construction and sandboxed execution of authorized verification plans."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import os
import re
import shutil
import shlex
import signal
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path, PurePath
from typing import Any


SHELL_LAUNCHERS = frozenset(
    {"bash", "csh", "dash", "fish", "ksh", "sh", "tcsh", "zsh"}
)

# Version 1 recognizes only these explicit, top-level installation requests.
# It does not infer side effects of arbitrary programs launched by a check.
INSTALL_SUBCOMMAND_RULES = (
    ("pip", r"pip(?:\d+(?:\.\d+)*)?", (("install",), ("download",), ("wheel",))),
    ("easy-install", r"easy_install(?:-\d+(?:\.\d+)*)?", ((),)),
    ("uv", r"uv", (("add",), ("sync",), ("pip", "install"), ("pip", "sync"),
                    ("tool", "install"), ("tool", "upgrade"))),
    ("poetry", r"poetry", (("add",), ("install",), ("sync",), ("update",))),
    ("pipenv", r"pipenv", (("install",), ("sync",), ("update",))),
    ("npm", r"npm", (("add",), ("ci",), ("i",), ("install",), ("update",),
                       ("upgrade",), ("exec",))),
    ("npx", r"npx", ((),)),
    ("pnpm", r"pnpm", (("add",), ("dlx",), ("i",), ("install",), ("up",),
                         ("update",))),
    ("pnpx", r"pnpx", ((),)),
    ("yarn", r"yarn", (("add",), ("dlx",), ("install",), ("up",), ("upgrade",))),
    ("bun", r"bun", (("add",), ("install",), ("update",), ("upgrade",), ("x",))),
    ("bunx", r"bunx", ((),)),
    ("conda-family", r"(?:conda|mamba|micromamba)",
     (("create",), ("install",), ("update",), ("upgrade",))),
    ("gem", r"gem", (("install",), ("update",))),
    ("bundler", r"(?:bundle|bundler)", (("install",), ("update",))),
    ("cargo", r"cargo", (("add",), ("install",))),
    ("go", r"go", (("get",), ("install",))),
    ("dotnet", r"dotnet", (("restore",), ("tool", "install"), ("tool", "restore"),
                             ("tool", "update"))),
    ("composer", r"composer", (("install",), ("require",), ("update",))),
    ("brew", r"brew", (("bundle",), ("install",), ("reinstall",), ("upgrade",))),
    ("apt", r"(?:apt|apt-get)", (("install",), ("reinstall",))),
    ("dnf-yum", r"(?:dnf|yum)", (("install",), ("reinstall",), ("upgrade",))),
    ("apk", r"apk", (("add",), ("upgrade",))),
    ("pacman", r"pacman", (("-s",), ("-u",))),
    ("zypper", r"zypper", (("in",), ("install",), ("update",))),
    ("winget", r"winget", (("install",), ("upgrade",))),
    ("choco", r"choco", (("install",), ("upgrade",))),
    ("scoop", r"scoop", (("install",), ("update",))),
)

_LEADING_ASSIGNMENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*=")
_PYTHON = re.compile(r"python(?:\d+(?:\.\d+)*)?")
_REDIRECTION = re.compile(r"(?:\d+)?(?:<|<<|<<<|<>|>|>>|>\||<&|>&|&>|&>>)")
_CONTROL_TOKENS = frozenset({";", "&&", "||", "|", "&", "(", ")"})
SANDBOX_EXEC = Path("/usr/bin/sandbox-exec")
REQUIRED_PERMISSION_KEYS = frozenset({
    "sandbox", "approval_policy", "network", "dependency_install",
    "writable_roots", "danger_full_access_authorized",
})


class VerificationPlanError(ValueError):
    """Persisted verification authority cannot produce a safe argv plan."""

    def __init__(self, message: str, *, matched_rule: str | None = None):
        super().__init__(message)
        self.matched_rule = matched_rule


class UnsupportedSandbox(RuntimeError):
    """The adopted local verification boundary cannot be applied."""


class VerificationExecutionError(RuntimeError):
    """An authorized plan could not be executed or published safely."""


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value).encode()).hexdigest()


def _executable_name(value: str) -> str:
    return PurePath(value).name.lower()


def _install_rule(argv: tuple[str, ...]) -> str | None:
    executable = _executable_name(argv[0])
    lowered_args = tuple(argument.lower() for argument in argv[1:])

    if _PYTHON.fullmatch(executable):
        for index, argument in enumerate(lowered_args[:-1]):
            if argument == "-m":
                module = lowered_args[index + 1]
                module_args = lowered_args[index + 2:]
                if module == "ensurepip":
                    return "python-module-ensurepip"
                if re.fullmatch(r"pip(?:\d+(?:\.\d+)*)?", module):
                    if module_args and module_args[0] in {"download", "install", "wheel"}:
                        return "python-module-pip"
                break

    if executable == "dotnet" and lowered_args[:1] == ("add",):
        if "package" in lowered_args[1:]:
            return "dotnet-add-package"

    for rule, executable_pattern, prefixes in INSTALL_SUBCOMMAND_RULES:
        if re.fullmatch(executable_pattern, executable) is None:
            continue
        for prefix in prefixes:
            if lowered_args[:len(prefix)] == prefix:
                return rule
    return None


def parse_verification_command(command: str, *, dependency_install: bool) -> tuple[str, ...]:
    """Parse one persisted command into shell-free argv and apply v1 preflight."""

    if not isinstance(command, str):
        raise VerificationPlanError("verification command must be a string")
    if "\x00" in command or "\n" in command or "\r" in command:
        raise VerificationPlanError("verification command contains NUL or newline input")
    if "$(" in command or "`" in command:
        raise VerificationPlanError("verification command contains command substitution syntax")
    try:
        argv = tuple(shlex.split(command, posix=True))
    except ValueError as exc:
        raise VerificationPlanError(f"verification command has malformed quoting: {exc}") from exc
    if not argv:
        raise VerificationPlanError("verification command must not be empty")
    if _LEADING_ASSIGNMENT.match(argv[0]):
        raise VerificationPlanError("verification command cannot start with NAME=value")

    executable = _executable_name(argv[0])
    if executable == "env":
        raise VerificationPlanError("verification command cannot use the env launcher")
    if executable in SHELL_LAUNCHERS:
        raise VerificationPlanError(f"verification command cannot use shell launcher {executable!r}")
    for token in argv:
        if token in _CONTROL_TOKENS or _REDIRECTION.fullmatch(token):
            raise VerificationPlanError(
                f"verification command contains standalone shell token {token!r}"
            )

    if not dependency_install:
        matched_rule = _install_rule(argv)
        if matched_rule is not None:
            raise VerificationPlanError(
                f"dependency installation request denied by v1 rule {matched_rule!r}",
                matched_rule=matched_rule,
            )
    return argv


def build_verification_plan(
    selected_task: dict[str, Any], policy: dict[str, Any]
) -> dict[str, Any]:
    """Build a deterministic JSON-compatible plan without executing or persisting it."""

    verification = policy["verification"]
    repository_gate = verification["repository_gate"]
    authorized_gap = verification["authorized_gap"]
    if authorized_gap is not None and repository_gate is None:
        raise VerificationPlanError("authorized gap requires a repository gate")

    sources = []
    for index, command in enumerate(selected_task.get("required_checks", [])):
        sources.append((command, "task_required", f"selected_task.required_checks[{index}]"))
    for index, command in enumerate(verification["targeted_checks"]):
        sources.append((command, "policy_targeted", f"policy.verification.targeted_checks[{index}]"))
    if repository_gate is not None:
        sources.append((repository_gate, "repository_gate", "policy.verification.repository_gate"))

    dependency_install = policy["permissions"]["dependency_install"]
    commands: list[dict[str, Any]] = []
    by_argv: dict[tuple[str, ...], dict[str, Any]] = {}
    for original, role, source in sources:
        argv = parse_verification_command(
            original, dependency_install=dependency_install
        )
        command = by_argv.get(argv)
        provenance = {"source": source, "role": role, "original": original}
        if command is None:
            command = {
                "id": f"command-{len(commands) + 1:03d}",
                "argv": list(argv),
                "roles": [],
                "provenance": [],
                "authorized_gap": None,
                "gap_excusable": False,
            }
            commands.append(command)
            by_argv[argv] = command
        command["provenance"].append(provenance)
        if role not in command["roles"]:
            command["roles"].append(role)
        if role == "repository_gate" and authorized_gap is not None:
            command["authorized_gap"] = dict(authorized_gap)

    for command in commands:
        command["gap_excusable"] = command["roles"] == ["repository_gate"] and (
            command["authorized_gap"] is not None
        )
        command["command_sha256"] = _digest(command)

    plan = {"version": 1, "commands": commands}
    plan["plan_sha256"] = _digest(plan)
    return plan


def _normalize_permissions(permissions: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(permissions, dict) or set(permissions) != REQUIRED_PERMISSION_KEYS:
        raise UnsupportedSandbox("the complete version 1 permission envelope is required")
    if permissions["approval_policy"] != "never":
        raise UnsupportedSandbox("verification cannot request approval while running")
    for field in ("network", "dependency_install", "danger_full_access_authorized"):
        if type(permissions[field]) is not bool:
            raise UnsupportedSandbox(f"{field} must be boolean")

    sandbox = permissions["sandbox"]
    if sandbox not in {"read-only", "workspace-write", "danger-full-access"}:
        raise UnsupportedSandbox(f"unsupported sandbox mode: {sandbox!r}")
    if sandbox == "danger-full-access" and not permissions["danger_full_access_authorized"]:
        raise UnsupportedSandbox("danger-full-access lacks separate authorization")

    roots = permissions["writable_roots"]
    if not isinstance(roots, list) or any(
        not isinstance(root, str) or not root for root in roots
    ):
        raise UnsupportedSandbox("writable_roots must be a list of non-empty paths")
    normalized_roots: list[str] = []
    for root in roots:
        path = Path(root)
        if not path.is_absolute() or not path.is_dir():
            raise UnsupportedSandbox("every writable root must be an existing absolute directory")
        normalized = Path(os.path.realpath(path))
        if normalized == Path("/"):
            raise UnsupportedSandbox("workspace-write cannot use the filesystem root")
        value = str(normalized)
        if value not in normalized_roots:
            normalized_roots.append(value)

    return {
        "sandbox": sandbox,
        "approval_policy": "never",
        "network": permissions["network"],
        "dependency_install": permissions["dependency_install"],
        "writable_roots": normalized_roots,
        "danger_full_access_authorized": permissions["danger_full_access_authorized"],
    }


def build_sandbox_invocation(
    argv: list[str | os.PathLike[str]] | tuple[str | os.PathLike[str], ...],
    permissions: dict[str, Any],
    *,
    platform: str = sys.platform,
    sandbox_executable: Path = SANDBOX_EXEC,
) -> list[str]:
    """Build the exact adopted Seatbelt argv for one already-resolved command."""

    if platform != "darwin":
        raise UnsupportedSandbox("sandbox-exec verification is supported only on macOS")
    if (
        Path(sandbox_executable) != SANDBOX_EXEC
        or not SANDBOX_EXEC.is_file()
        or not os.access(SANDBOX_EXEC, os.X_OK)
    ):
        raise UnsupportedSandbox("the exact /usr/bin/sandbox-exec mechanism is unavailable")
    normalized_argv = [os.fspath(item) for item in argv]
    if not normalized_argv or any(not isinstance(item, str) or not item for item in normalized_argv):
        raise UnsupportedSandbox("verification argv must contain non-empty strings")

    normalized = _normalize_permissions(permissions)
    profile = ["(version 1)", "(allow default)"]
    definitions: list[str] = []
    if not normalized["network"]:
        profile.append("(deny network*)")

    if normalized["sandbox"] == "read-only":
        profile.append("(deny file-write*)")
    elif normalized["sandbox"] == "workspace-write":
        roots = normalized["writable_roots"]
        if not roots:
            profile.append("(deny file-write*)")
        else:
            exclusions = []
            for index, root in enumerate(roots):
                name = f"WRITABLE_ROOT_{index}"
                definitions.extend(["-D", f"{name}={root}"])
                exclusions.append(f'(require-not (subpath (param "{name}")))')
            profile.append(
                "(deny file-write* (require-all " + " ".join(exclusions) + "))"
            )

    return [
        str(SANDBOX_EXEC), *definitions, "-p", " ".join(profile), *normalized_argv
    ]


def _validate_plan(plan: dict[str, Any], *, dependency_install: bool) -> None:
    if not isinstance(plan, dict) or set(plan) != {"version", "commands", "plan_sha256"}:
        raise VerificationExecutionError("a complete S3-06 plan is required")
    if (
        type(plan["version"]) is not int or plan["version"] != 1
        or not isinstance(plan["commands"], list) or not plan["commands"]
    ):
        raise VerificationExecutionError("a non-empty version 1 plan is required")
    if plan["plan_sha256"] != _digest({"version": 1, "commands": plan["commands"]}):
        raise VerificationExecutionError("verification plan digest mismatch")

    identities = []
    for index, command in enumerate(plan["commands"], 1):
        required = {
            "id", "argv", "roles", "provenance", "authorized_gap",
            "gap_excusable", "command_sha256",
        }
        if not isinstance(command, dict) or set(command) != required:
            raise VerificationExecutionError("verification plan command has invalid fields")
        if command["id"] != f"command-{index:03d}":
            raise VerificationExecutionError("verification plan command IDs are not canonical")
        unsigned = {key: value for key, value in command.items() if key != "command_sha256"}
        if command["command_sha256"] != _digest(unsigned):
            raise VerificationExecutionError("verification command digest mismatch")
        argv = command["argv"]
        if not isinstance(argv, list) or not argv or any(
            not isinstance(item, str) or not item for item in argv
        ):
            raise VerificationExecutionError("verification command argv is invalid")
        identity = tuple(argv)
        if identity in identities:
            raise VerificationExecutionError("verification plan contains duplicate argv")
        identities.append(identity)

        roles = command["roles"]
        if (
            not isinstance(roles, list) or not roles
            or len(roles) != len(set(roles))
            or any(role not in {"task_required", "policy_targeted", "repository_gate"}
                   for role in roles)
        ):
            raise VerificationExecutionError("verification command roles are invalid")
        provenance = command["provenance"]
        if not isinstance(provenance, list) or not provenance:
            raise VerificationExecutionError("verification command provenance is invalid")
        observed_roles = []
        for source in provenance:
            if not isinstance(source, dict) or set(source) != {"source", "role", "original"}:
                raise VerificationExecutionError("verification command provenance is invalid")
            if not all(isinstance(source[name], str) and source[name] for name in source):
                raise VerificationExecutionError("verification command provenance is invalid")
            parsed = parse_verification_command(
                source["original"], dependency_install=dependency_install
            )
            if parsed != identity or source["role"] not in roles:
                raise VerificationExecutionError("verification command provenance mismatch")
            if source["role"] not in observed_roles:
                observed_roles.append(source["role"])
        if observed_roles != roles:
            raise VerificationExecutionError("verification command role order mismatch")
        if "repository_gate" in roles and index != len(plan["commands"]):
            raise VerificationExecutionError("repository gate must be the final command")
        gap = command["authorized_gap"]
        if gap is not None and (
            not isinstance(gap, dict) or set(gap) != {"reason", "owner", "follow_up"}
            or any(not isinstance(value, str) or not value for value in gap.values())
        ):
            raise VerificationExecutionError("authorized gap is invalid")
        if gap is not None and "repository_gate" not in roles:
            raise VerificationExecutionError("authorized gap requires repository gate role")
        expected_excusable = roles == ["repository_gate"] and gap is not None
        if type(command["gap_excusable"]) is not bool or (
            command["gap_excusable"] != expected_excusable
        ):
            raise VerificationExecutionError("authorized gap semantics are invalid")


def _load_controller_state():
    path = Path(__file__).with_name("controller_state.py")
    spec = importlib.util.spec_from_file_location("task_orchestrator_controller_state", path)
    if spec is None or spec.loader is None:
        raise VerificationExecutionError("controller record validator is unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _canonical_directory(value: str | Path, field: str) -> Path:
    path = Path(value)
    if not path.is_absolute() or not path.is_dir():
        raise VerificationExecutionError(f"{field} must be an existing absolute directory")
    canonical = Path(os.path.realpath(path))
    if path != canonical:
        raise VerificationExecutionError(f"{field} must already be canonical")
    return canonical


def _resolve_executable(argv: list[str], cwd: Path) -> tuple[list[str], tuple[Any, ...]]:
    requested = argv[0]
    if "/" in requested:
        candidate = Path(requested)
        if not candidate.is_absolute():
            candidate = cwd / candidate
        resolved = Path(os.path.realpath(candidate))
    else:
        found = shutil.which(requested)
        if found is None:
            raise VerificationExecutionError(f"verification executable is not resolvable: {requested}")
        resolved = Path(os.path.realpath(found))
    if not resolved.is_file() or not os.access(resolved, os.X_OK):
        raise VerificationExecutionError(f"verification executable is not executable: {requested}")
    stat = resolved.stat()
    fingerprint = (
        stat.st_dev, stat.st_ino, stat.st_mode, stat.st_size, stat.st_mtime_ns,
        _sha256_file(resolved),
    )
    return [str(resolved), *argv[1:]], fingerprint


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _process_group_exists(process_group_id: int) -> bool:
    try:
        os.killpg(process_group_id, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        # EPERM does not prove that an owned group is empty.
        return True
    return True


def _wait_for_process_group_exit(process_group_id: int, timeout: float) -> None:
    deadline = time.monotonic() + timeout
    exited = threading.Event()
    while _process_group_exists(process_group_id):
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise VerificationExecutionError("verification process group did not terminate")
        exited.wait(min(0.01, remaining))


def _terminate_process_group(process: subprocess.Popen[bytes]) -> None:
    process_group_id = process.pid
    try:
        os.killpg(process_group_id, signal.SIGTERM)
    except (ProcessLookupError, PermissionError):
        pass
    try:
        process.wait(timeout=1)
    except subprocess.TimeoutExpired:
        pass
    if _process_group_exists(process_group_id):
        try:
            os.killpg(process_group_id, signal.SIGKILL)
        except (ProcessLookupError, PermissionError):
            pass
    try:
        process.wait(timeout=1)
    except subprocess.TimeoutExpired as exc:
        raise VerificationExecutionError("verification process group did not terminate") from exc
    _wait_for_process_group_exit(process_group_id, 1)


def _artifact_path(run_directory: Path, relative: str) -> Path:
    if (
        not relative or relative.startswith("/") or "\\" in relative
        or any(part in {"", ".", ".."} for part in relative.split("/"))
    ):
        raise VerificationExecutionError("artifact path must be a safe run-relative path")
    path = run_directory.joinpath(*relative.split("/"))
    if Path(os.path.realpath(path.parent)) != run_directory.joinpath(*relative.split("/")[:-1]):
        raise VerificationExecutionError("artifact path escapes the canonical run directory")
    return path


def execute_verification_plan(
    *,
    plan: dict[str, Any],
    repository_cwd: str | Path,
    permissions: dict[str, Any],
    timeout_seconds: float,
    run_directory: str | Path,
    execution_path: str,
    closure_identity: dict[str, Any],
    interruption_event: threading.Event | None = None,
) -> tuple[dict[str, Any], str]:
    """Preflight, execute, and exclusively publish one command-execution record."""

    if (
        type(timeout_seconds) not in {int, float}
        or not math.isfinite(timeout_seconds)
        or timeout_seconds <= 0
    ):
        raise VerificationExecutionError("timeout_seconds must be positive")
    cwd = _canonical_directory(repository_cwd, "repository_cwd")
    run_dir = _canonical_directory(run_directory, "run_directory")
    normalized_permissions = _normalize_permissions(permissions)
    _validate_plan(plan, dependency_install=normalized_permissions["dependency_install"])
    state = _load_controller_state()
    state.validate_closure_identity(closure_identity)

    subject = closure_identity["subject"]
    stem = f"{subject['attempt_id']}.turn-{subject['turn']:03d}"
    expected_execution_path = f"verification/{stem}.execution.json"
    if execution_path != expected_execution_path:
        raise VerificationExecutionError(
            f"execution_path must be {expected_execution_path}"
        )
    record_path = _artifact_path(run_dir, execution_path)

    prepared = []
    artifact_paths = [record_path]
    for command in plan["commands"]:
        resolved_argv, fingerprint = _resolve_executable(command["argv"], cwd)
        effective_argv = build_sandbox_invocation(resolved_argv, normalized_permissions)
        stdout_relative = f"verification/{stem}.{command['id']}.stdout.log"
        stderr_relative = f"verification/{stem}.{command['id']}.stderr.log"
        stdout_path = _artifact_path(run_dir, stdout_relative)
        stderr_path = _artifact_path(run_dir, stderr_relative)
        artifact_paths.extend((stdout_path, stderr_path))
        prepared.append({
            "command": command,
            "resolved_argv": resolved_argv,
            "fingerprint": fingerprint,
            "effective_argv": effective_argv,
            "stdout_relative": stdout_relative,
            "stderr_relative": stderr_relative,
            "stdout_path": stdout_path,
            "stderr_path": stderr_path,
        })
    if len(artifact_paths) != len(set(artifact_paths)):
        raise VerificationExecutionError("verification artifact paths collide")
    if any(path.exists() for path in artifact_paths):
        raise FileExistsError("verification artifact path already exists")
    if not record_path.parent.is_dir():
        raise VerificationExecutionError("verification artifact directory does not exist")

    capability = build_sandbox_invocation(["/usr/bin/true"], normalized_permissions)
    capability_result = subprocess.run(
        capability, cwd=cwd, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL, check=False, timeout=5,
    )
    if capability_result.returncode != 0:
        raise UnsupportedSandbox("the sandbox mechanism failed its local capability preflight")

    record_started = _utc_now()
    outcomes = []
    terminal_reason = "complete"
    authorized_gap = None
    stop_event = interruption_event or threading.Event()
    installed_handlers = threading.current_thread() is threading.main_thread()
    previous_handlers: dict[int, Any] = {}

    def request_interruption(signum: int, frame: Any) -> None:
        stop_event.set()

    if installed_handlers:
        for signum in (signal.SIGINT, signal.SIGTERM):
            previous_handlers[signum] = signal.getsignal(signum)
            signal.signal(signum, request_interruption)
    try:
        for item in prepared:
            if stop_event.is_set():
                raise VerificationExecutionError("verification interrupted before command start")
            current_argv, current_fingerprint = _resolve_executable(
                item["command"]["argv"], cwd
            )
            if current_argv != item["resolved_argv"] or current_fingerprint != item["fingerprint"]:
                raise VerificationExecutionError("resolved executable changed before launch")

            started_at = _utc_now()
            process: subprocess.Popen[bytes] | None = None
            stream_errors: list[BaseException] = []
            stdout_digest = hashlib.sha256()
            stderr_digest = hashlib.sha256()
            stdout_thread = None
            stderr_thread = None
            timed_out = False
            interrupted = False
            try:
                with item["stdout_path"].open("xb") as stdout_file, item[
                    "stderr_path"
                ].open("xb") as stderr_file:
                    process = subprocess.Popen(
                        item["effective_argv"], cwd=cwd, stdin=subprocess.DEVNULL,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False,
                        start_new_session=True,
                    )

                    def stream_bytes(source, destination, digest) -> None:
                        try:
                            for chunk in iter(lambda: source.read(64 * 1024), b""):
                                destination.write(chunk)
                                digest.update(chunk)
                        except BaseException as exc:
                            stream_errors.append(exc)
                        finally:
                            source.close()

                    assert process.stdout is not None and process.stderr is not None
                    stdout_thread = threading.Thread(
                        target=stream_bytes,
                        args=(process.stdout, stdout_file, stdout_digest), daemon=True,
                    )
                    stderr_thread = threading.Thread(
                        target=stream_bytes,
                        args=(process.stderr, stderr_file, stderr_digest), daemon=True,
                    )
                    stdout_thread.start()
                    stderr_thread.start()
                    deadline = time.monotonic() + float(timeout_seconds)
                    while process.poll() is None:
                        if stream_errors:
                            _terminate_process_group(process)
                            raise VerificationExecutionError(
                                f"verification log streaming failed: {stream_errors[0]}"
                            )
                        if stop_event.is_set():
                            interrupted = True
                            _terminate_process_group(process)
                            break
                        remaining = deadline - time.monotonic()
                        if remaining <= 0:
                            timed_out = True
                            _terminate_process_group(process)
                            break
                        try:
                            process.wait(timeout=min(0.05, remaining))
                        except subprocess.TimeoutExpired:
                            pass
                    for thread in (stdout_thread, stderr_thread):
                        thread.join(timeout=1)
                    if stdout_thread.is_alive() or stderr_thread.is_alive():
                        _terminate_process_group(process)
                        for thread in (stdout_thread, stderr_thread):
                            thread.join(timeout=1)
                            if thread.is_alive():
                                raise VerificationExecutionError(
                                    "verification log streamer did not terminate"
                                )
                    process.stdout.close()
                    process.stderr.close()
                    if stream_errors:
                        raise VerificationExecutionError(
                            f"verification log streaming failed: {stream_errors[0]}"
                        )
                    stdout_file.flush()
                    stderr_file.flush()
                    os.fsync(stdout_file.fileno())
                    os.fsync(stderr_file.fileno())
            except BaseException:
                if process is not None:
                    _terminate_process_group(process)
                for thread in (stdout_thread, stderr_thread):
                    if thread is not None and thread.is_alive():
                        thread.join(timeout=1)
                if process is not None:
                    if (
                        process.stdout is not None
                        and (stdout_thread is None or not stdout_thread.is_alive())
                    ):
                        process.stdout.close()
                    if (
                        process.stderr is not None
                        and (stderr_thread is None or not stderr_thread.is_alive())
                    ):
                        process.stderr.close()
                raise

            ended_at = _utc_now()
            if interrupted:
                status = "interrupted"
                exit_code = None
                terminal_reason = "interrupted"
            elif timed_out:
                status = "timed_out"
                exit_code = None
                terminal_reason = "timed_out"
            else:
                assert process is not None
                exit_code = process.returncode
                if exit_code == 0:
                    status = "passed"
                elif item["command"]["gap_excusable"]:
                    status = "authorized_gap"
                    terminal_reason = "authorized_gap"
                    authorized_gap = dict(item["command"]["authorized_gap"])
                else:
                    status = "failed"
                    terminal_reason = "command_failed"
            outcomes.append({
                "id": item["command"]["id"],
                "status": status,
                "exit_code": exit_code,
                "started_at": started_at,
                "ended_at": ended_at,
                "effective_argv": list(item["effective_argv"]),
                "stdout_path": item["stdout_relative"],
                "stdout_sha256": stdout_digest.hexdigest(),
                "stderr_path": item["stderr_relative"],
                "stderr_sha256": stderr_digest.hexdigest(),
            })
            if status != "passed":
                break
    finally:
        if installed_handlers:
            for signum, handler in previous_handlers.items():
                signal.signal(signum, handler)

    record = {
        "version": 1,
        "closure_identity": json.loads(json.dumps(closure_identity)),
        "plan": [{
            "id": item["command"]["id"],
            "argv": list(item["command"]["argv"]),
            "sources": [source["source"] for source in item["command"]["provenance"]],
            "role": (
                "repository_gate"
                if item["command"]["roles"] == ["repository_gate"] else "targeted"
            ),
        } for item in prepared],
        "outcomes": outcomes,
        "effective_envelope": normalized_permissions,
        "started_at": record_started,
        "ended_at": _utc_now(),
        "terminal_reason": terminal_reason,
        "authorized_gap": authorized_gap,
    }
    state.validate_command_execution_record(
        record, expected_closure_identity=closure_identity
    )
    serialized = state.canonical_json(record).encode()
    digest = hashlib.sha256(serialized).hexdigest()
    with record_path.open("xb") as output:
        output.write(serialized)
        output.flush()
        os.fsync(output.fileno())
    return json.loads(serialized), digest
