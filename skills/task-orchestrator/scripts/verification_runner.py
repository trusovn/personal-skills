"""Pure construction of authorized verification command plans."""

from __future__ import annotations

import hashlib
import json
import re
import shlex
from pathlib import PurePath
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


class VerificationPlanError(ValueError):
    """Persisted verification authority cannot produce a safe argv plan."""

    def __init__(self, message: str, *, matched_rule: str | None = None):
        super().__init__(message)
        self.matched_rule = matched_rule


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
