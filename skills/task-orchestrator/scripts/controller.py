#!/usr/bin/env python3
"""Small Stage 1 policy, prompt, attempt, and closure primitives."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any

# Import atomic_write_json from the worker adapter for ledger persistence
_worker_spec = importlib.util.spec_from_file_location(
    "task_orchestrator_worker",
    Path(__file__).parents[1] / "scripts" / "codex_worker.py",
)
_worker_module = importlib.util.module_from_spec(_worker_spec)
assert _worker_spec.loader is not None
_worker_spec.loader.exec_module(_worker_module)
atomic_write_json = _worker_module.atomic_write_json

_state_spec = importlib.util.spec_from_file_location(
    "task_orchestrator_controller_state",
    Path(__file__).with_name("controller_state.py"),
)
_state_module = importlib.util.module_from_spec(_state_spec)
assert _state_spec.loader is not None
_state_spec.loader.exec_module(_state_module)

# Compatibility imports: pure state rules live in controller_state.py.
ATTEMPT_REQUIRED_FIELDS = _state_module.ATTEMPT_REQUIRED_FIELDS
ALLOWED_TASK_TRANSITIONS = _state_module.ALLOWED_TASK_TRANSITIONS
canonical_json = _state_module.canonical_json
sha256_text = _state_module.sha256_text
validate_run_policy = _state_module.validate_run_policy
transition_task = _state_module.transition_task
validate_attempt_record = _state_module.validate_attempt_record
build_attempt_record = _state_module.build_attempt_record
_validate_task_manifest_schema = _state_module._validate_task_manifest_schema
_detect_dependency_cycles = _state_module._detect_dependency_cycles
_is_valid_repo_relative_path = _state_module._is_valid_repo_relative_path
validate_task_manifest = _state_module.validate_task_manifest
select_task = _state_module.select_task
_validate_ledger = _state_module.validate_ledger


def atomic_write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(value)
    temporary.replace(path)


def persist_run_policy(path: Path, policy: dict[str, Any]) -> str:
    validate_run_policy(policy)
    serialized = json.dumps(policy, indent=2, sort_keys=True) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x") as stream:
        stream.write(serialized)
    return sha256_text(canonical_json(policy))


def render_worker_prompt(
    *,
    task_id: str,
    brief_path: str,
    task_instructions: str,
    policy: dict[str, Any],
) -> str:
    validate_run_policy(policy)
    return "\n".join(
        (
            f"Task: {task_id}",
            f"Authoritative brief: {brief_path}",
            "",
            task_instructions.rstrip(),
            "",
            "Worker boundary:",
            "- Work only on the selected task and its allowed paths.",
            "- Do not commit, even if the controller policy permits a later controller-owned commit.",
            "- Do not update the orchestration ledger or select another task.",
            "- Do not change the controller, installed skills, or permission envelope.",
            "- Return the required structured result; it is a claim pending independent inspection.",
            "",
        )
    )


def capture_git_status(repository: Path) -> dict[str, str]:
    result = subprocess.run(
        ["git", "-C", str(repository), "status", "--porcelain=v1", "-z", "--untracked-files=all"],
        check=True,
        capture_output=True,
    )
    entries = result.stdout.decode(errors="surrogateescape").split("\0")
    status: dict[str, str] = {}
    index = 0
    while index < len(entries):
        entry = entries[index]
        if not entry:
            index += 1
            continue
        code = entry[:2]
        path = entry[3:]
        worktree_path = repository / path
        if worktree_path.is_symlink():
            content = str(worktree_path.readlink()).encode()
        elif worktree_path.is_file():
            content = worktree_path.read_bytes()
        else:
            content = b"<missing>"
        status[path] = f"{code}:{hashlib.sha256(content).hexdigest()}"
        if "R" in code or "C" in code:
            index += 1
        index += 1
    return status


def decide_closure(
    *,
    policy: dict[str, Any],
    task_id: str,
    allowed_paths: set[str],
    baseline_status: dict[str, str],
    current_status: dict[str, str] | None,
    result: dict[str, Any] | None,
    controller_verification: dict[str, str] | None = None,
    run_id: str | None = None,
    attempt_id: str | None = None,
    prompt_sha256: str | None = None,
    evidence_digest: str | None = None,
    stage2_mode: bool = True,
) -> dict[str, Any]:
    """Decide closure with identity/digest binding.

    When stage2_mode is True (default), acceptance is blocked and only
    inspect/stop transitions are allowed. When False, the legacy behavior
    (acceptance based on verification evidence) is restored.
    """
    validate_run_policy(policy)
    reasons: list[str] = []
    unexpected_paths: list[str] = []

    if current_status is None:
        reasons.append("independent Git inspection is missing")
    else:
        unexpected_paths = sorted(set(current_status) - set(baseline_status) - allowed_paths)
        if unexpected_paths:
            reasons.append("unexpected changed paths: " + ", ".join(unexpected_paths))
        lost_dirty_paths = sorted(set(baseline_status) - set(current_status))
        if lost_dirty_paths:
            reasons.append("pre-existing dirty paths disappeared: " + ", ".join(lost_dirty_paths))
        changed_dirty_paths = sorted(
            path
            for path in set(baseline_status) & set(current_status)
            if baseline_status[path] != current_status[path]
        )
        if changed_dirty_paths:
            reasons.append("pre-existing dirty paths changed: " + ", ".join(changed_dirty_paths))

    if result is None:
        reasons.append("structured worker result is missing")
    else:
        if result.get("status") != "complete":
            reasons.append("worker result is not complete")
        if result.get("task_id") != task_id:
            reasons.append("worker result task id does not match")
        required = list(policy["verification"]["targeted_checks"])
        repository_gate = policy["verification"].get("repository_gate")
        if repository_gate:
            required.append(repository_gate)
        if controller_verification is None:
            reasons.append(
                "independent controller verification evidence is missing; "
                "worker-claimed verification alone cannot satisfy the verification gate"
            )
        else:
            for command in required:
                if controller_verification.get(command) == "passed":
                    continue
                if command == repository_gate and policy["verification"].get("authorized_gap"):
                    continue
                reasons.append(f"required verification did not pass: {command}")
        if any(question.get("blocking") for question in result.get("questions", [])):
            reasons.append("worker result contains a blocking question")
        if result.get("risks"):
            reasons.append("worker result contains unresolved risks")

    accepted = not reasons
    if stage2_mode:
        accepted = False
        allowed_transitions = ["resumable", "stopped"]
        allowed_actions = ["inspect", "stop"]
    else:
        # Legacy mode: acceptance based on verification evidence
        allowed_transitions = ["accepted"] if accepted else ["resumable", "stopped"]
        allowed_actions = ["record_acceptance"] if accepted else ["inspect", "resume", "stop"]
        if accepted and policy["commit_policy"]["mode"] == "controller_exact_paths":
            allowed_actions.append("commit_exact_paths")
    # Bind the decision to run/task/attempt identity
    identity_fields = {
        "run_id": run_id,
        "task_id": task_id,
        "attempt_id": attempt_id,
    }
    if prompt_sha256:
        identity_fields["prompt_sha256"] = prompt_sha256
    if evidence_digest:
        identity_fields["evidence_digest"] = evidence_digest
    return {
        "accepted": accepted,
        "reasons": reasons,
        "unexpected_paths": unexpected_paths,
        "observed_paths": sorted(current_status or {}),
        "allowed_transitions": allowed_transitions,
        "allowed_actions": allowed_actions,
        "identity": identity_fields,
    }


def create_attempt(run_dir: Path, record: dict[str, Any]) -> Path:
    validate_attempt_record(record)
    attempts_dir = run_dir / "attempts"
    attempts_dir.mkdir(parents=True, exist_ok=True)
    attempt_number = 1
    while (attempts_dir / f"attempt-{attempt_number:03d}").exists():
        attempt_number += 1
    attempt_dir = attempts_dir / f"attempt-{attempt_number:03d}"
    attempt_dir.mkdir()
    persisted = dict(record)
    prompt = persisted.pop("prompt", "")
    persisted["attempt_number"] = attempt_number
    with (attempt_dir / "record.json").open("x") as stream:
        stream.write(json.dumps(persisted, indent=2, sort_keys=True) + "\n")
    with (attempt_dir / "prompt.txt").open("x") as stream:
        stream.write(prompt)
    return attempt_dir


# ── Manifest validation ──────────────────────────────────────────────


# ── Git baseline ─────────────────────────────────────────────────────


def capture_initial_baseline(repository: Path) -> dict[str, Any]:
    """Capture HEAD OID, porcelain status, and untracked paths."""
    head_result = subprocess.run(
        ["git", "-C", str(repository), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    )
    head_oid = head_result.stdout.strip()
    if not head_oid:
        raise ValueError("Repository has no HEAD (unborn repository)")
    status = capture_git_status(repository)
    return {
        "head_oid": head_oid,
        "status": status,
    }


# ── Run initialization ────────────────────────────────────────────────


def init_run(
    run_dir: Path,
    policy_path: Path,
    manifest_path: Path,
    repository: Path,
) -> dict[str, Any]:
    """Initialize an immutable run from validated policy and manifest."""
    policy = json.loads(policy_path.read_text())
    validate_run_policy(policy)
    manifest = json.loads(manifest_path.read_text())

    # Resolve and verify repository is Git top-level
    resolved_repo = repository.resolve()
    try:
        top_result = subprocess.run(
            ["git", "-C", str(resolved_repo), "rev-parse", "--show-toplevel"],
            check=True,
            capture_output=True,
            text=True,
        )
        actual_top = Path(top_result.stdout.strip()).resolve()
        if actual_top != resolved_repo:
            raise ValueError(
                f"Provided repository {resolved_repo} is not the Git top-level "
                f"(actual: {actual_top})"
            )
    except subprocess.CalledProcessError:
        raise ValueError(
            f"{resolved_repo} is not a Git repository or has no HEAD"
        )

    policy_repo = Path(policy["repository"])
    if resolved_repo != policy_repo.resolve():
        raise ValueError(
            f"Policy repository {policy['repository']} does not match "
            f"provided repository {repository}"
        )

    # Validate manifest cross-policy
    validated = validate_task_manifest(policy, manifest, resolved_repo)

    # Enforce run directory is outside the repository
    if run_dir.resolve().is_relative_to(resolved_repo):
        raise ValueError(
            f"Run directory {run_dir} must be outside the repository {resolved_repo}"
        )

    # Capture baseline
    baseline = capture_initial_baseline(resolved_repo)
    baseline_ref = f"run-initial.json"
    baseline_path = run_dir / "baselines" / baseline_ref

    # Build temporary directory and atomically publish
    temp_dir = run_dir.parent / f".tmp-run-{run_dir.name}-{hashlib.sha256(str(run_dir.name).encode()).hexdigest()[:8]}"
    try:
        # Copy canonical policy and manifest
        policy_digest = persist_run_policy(temp_dir / "run-policy.json", policy)
        manifest_content = manifest_path.read_text()
        manifest_digest = sha256_text(canonical_json(json.loads(manifest_content)))
        (temp_dir / "task-manifest.json").write_text(manifest_content)
        manifest_digest = sha256_text(canonical_json(manifest))

        # Create baselines directory
        (temp_dir / "baselines").mkdir()
        baseline_data = {
            "head_oid": baseline["head_oid"],
            "status": baseline["status"],
        }
        baseline_path = temp_dir / "baselines" / baseline_ref
        baseline_path.write_text(json.dumps(baseline_data, indent=2, sort_keys=True) + "\n")

        # Build ledger
        ledger = {
            "version": 1,
            "run_id": policy["run_id"],
            "repository": str(resolved_repo),
            "created_at": _now_iso(),
            "updated_at": _now_iso(),
            "revision": 1,
            "policy_path": "run-policy.json",
            "policy_sha256": policy_digest,
            "manifest_path": "task-manifest.json",
            "manifest_sha256": manifest_digest,
            "initial_baseline_path": str(baseline_ref),
            "initial_baseline_digest": sha256_text(
                canonical_json(baseline_data)
            ),
            "completed_task_ids": validated["completed_task_ids"],
            "state": "initialized",
            "selected_task_id": None,
            "active_attempt_id": None,
            "last_closure_path": None,
            "tasks": validated["task_entries"],
        }
        _validate_ledger(ledger)
        (temp_dir / "ledger.json").write_text(
            json.dumps(ledger, indent=2, sort_keys=True) + "\n"
        )

        # Atomic rename
        run_dir.parent.mkdir(parents=True, exist_ok=True)
        if run_dir.exists():
            raise FileExistsError(f"Run directory already exists: {run_dir}")
        temp_dir.rename(run_dir)

    except BaseException:
        # Clean up temp directory on failure
        if temp_dir.exists():
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)
        raise

    return {
        "run_id": policy["run_id"],
        "state": "initialized",
        "ledger_path": str(run_dir / "ledger.json"),
        "baseline_path": str(run_dir / "baselines" / baseline_ref),
    }


# ── Deterministic task selection ──────────────────────────────────────


def _now_iso() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()


# ── Ledger update helpers ─────────────────────────────────────────────


def update_ledger(run_dir: Path, updater: dict[str, Any]) -> dict[str, Any]:
    """Read, update, validate, and atomically write the ledger."""
    ledger_path = run_dir / "ledger.json"
    ledger = json.loads(ledger_path.read_text())
    ledger = _state_module.apply_ledger_update(ledger, updater, _now_iso())
    atomic_write_json(ledger_path, ledger)
    return ledger


# ── CLI entry points ─────────────────────────────────────────────────


def build_parser() -> "argparse.ArgumentParser":  # type: ignore[name-defined]
    import argparse
    parser = argparse.ArgumentParser(
        description="Task orchestrator controller."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Initialize an immutable run")
    init_parser.add_argument("--run-dir", required=True, help="Run directory (outside repo)")
    init_parser.add_argument("--policy", required=True, help="Run policy JSON path")
    init_parser.add_argument("--manifest", required=True, help="Task manifest JSON path")
    init_parser.add_argument("--repository", required=True, help="Repository root")
    init_parser.set_defaults(handler=_cli_init)

    runnext_parser = subparsers.add_parser("run-next", help="Select and launch one task")
    runnext_parser.add_argument("--run-dir", required=True)
    runnext_parser.add_argument("--timeout-seconds", type=float, required=True)
    runnext_parser.add_argument("--codex-bin", default="codex", help=argparse.SUPPRESS)
    runnext_parser.set_defaults(handler=_cli_run_next)

    return parser


def _cli_init(args: "argparse.Namespace") -> int:  # type: ignore[name-defined]
    import argparse
    result = init_run(
        run_dir=Path(args.run_dir).resolve(),
        policy_path=Path(args.policy).resolve(),
        manifest_path=Path(args.manifest).resolve(),
        repository=Path(args.repository).resolve(),
    )
    print(json.dumps(result, sort_keys=True))
    return 0


def _cli_run_next(args: "argparse.Namespace") -> int:  # type: ignore[name-defined]
    import argparse
    import codex_worker
    if args.timeout_seconds <= 0:
        raise ValueError("timeout must be greater than zero")
    run_dir = Path(args.run_dir).resolve()
    ledger_path = run_dir / "ledger.json"
    ledger = json.loads(ledger_path.read_text())
    _validate_ledger(ledger)
    policy = json.loads((run_dir / "run-policy.json").read_text())
    manifest = json.loads((run_dir / "task-manifest.json").read_text())

    # Validate persisted digests
    persisted_policy = json.loads((run_dir / "run-policy.json").read_text())
    if sha256_text(canonical_json(persisted_policy)) != ledger["policy_sha256"]:
        raise ValueError("Persisted policy digest mismatch")
    persisted_manifest = json.loads((run_dir / "task-manifest.json").read_text())
    if sha256_text(canonical_json(persisted_manifest)) != ledger["manifest_sha256"]:
        raise ValueError("Persisted manifest digest mismatch")

    # Compare current HEAD and status with initial baseline before any mutation
    repo = Path(ledger["repository"]).resolve()
    initial_baseline = json.loads(
        (run_dir / "baselines" / ledger["initial_baseline_path"]).read_text()
    )
    current_head = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if current_head != initial_baseline["head_oid"]:
        raise ValueError(
            f"HEAD has changed since initialization: {current_head} != {initial_baseline['head_oid']}"
        )
    current_status = capture_git_status(repo)
    initial_status = initial_baseline["status"]
    if current_status != initial_status:
        changed = sorted(set(current_status) ^ set(initial_status))
        raise ValueError(
            f"Repository state has changed since initialization. "
            f"Changed paths: {', '.join(changed)}"
        )

    # Validate initial-baseline digest before proceeding
    persisted_baseline_path = run_dir / "baselines" / ledger["initial_baseline_path"]
    persisted_baseline_content = persisted_baseline_path.read_text()
    computed_baseline_digest = sha256_text(canonical_json(json.loads(persisted_baseline_content)))
    if computed_baseline_digest != ledger["initial_baseline_digest"]:
        raise ValueError(
            f"Initial baseline digest mismatch: persisted={computed_baseline_digest}, "
            f"expected={ledger['initial_baseline_digest']}"
        )

    # Preflight the exact Codex start command shape before any durable mutation.
    worker_script = Path(__file__).parents[1] / "scripts" / "codex_worker.py"
    _worker_module.preflight_codex(
        args.codex_bin,
        repo,
        sandbox=policy["permissions"]["sandbox"],
    )

    # Selection is pure. Durable mutation begins only after exact preflight.
    task = select_task(ledger, policy)

    # Capture task baseline
    task_baseline = capture_git_status(repo)
    task_baseline_ref = "task-001.json"
    task_head = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    task_index_tree = subprocess.run(
        ["git", "-C", str(repo), "write-tree"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    task_baseline_data = {
        "head_oid": task_head,
        "index_tree": task_index_tree,
        "status": task_baseline,
    }
    task_baseline_digest = sha256_text(canonical_json(task_baseline_data))
    atomic_write_json(run_dir / "baselines" / task_baseline_ref, task_baseline_data)

    # Build prompt
    prompt = render_worker_prompt(
        task_id=task["id"],
        brief_path=task["brief_path"],
        task_instructions=f"Implement task {task['id']}: {task['title']}.\n"
                         f"Allowed paths: {task['allowed_paths']}\n"
                         f"Required checks: {task['required_checks']}\n"
                         f"Dependencies satisfied: {task['dependencies']}",
        policy=policy,
    )

    # Allocate attempt
    attempt_record = build_attempt_record(
        task_id=task["id"],
        brief_path=task["brief_path"],
        prompt=prompt,
        policy=policy,
        baseline_ref=task_baseline_ref,
    )
    expected_attempt_dir = run_dir / "attempts" / "attempt-001"
    adapter_invocation = [
        sys.executable, str(worker_script), "start",
        "--run-dir", str(expected_attempt_dir),
        "--cwd", str(repo),
        "--prompt-file", str(expected_attempt_dir / "prompt.txt"),
        "--codex-bin", args.codex_bin,
        "--timeout-seconds", str(args.timeout_seconds),
        "--sandbox", policy["permissions"]["sandbox"],
    ]
    attempt_record.update({
        "adapter_invocation": adapter_invocation,
        "codex_bin": args.codex_bin,
        "timeout_seconds": args.timeout_seconds,
        "effective_permission_envelope": policy["permissions"],
        "baseline_digest": task_baseline_digest,
    })
    attempt_dir = create_attempt(run_dir, attempt_record)
    attempt_id = attempt_dir.name
    if attempt_dir != expected_attempt_dir:
        raise ValueError("Stage 2 permits exactly one immutable attempt")

    running_tasks = [dict(entry) for entry in ledger["tasks"]]
    selected_task = next(entry for entry in running_tasks if entry["id"] == task["id"])
    selected_task["state"] = "running"
    selected_task["attempt_ids"] = [*selected_task["attempt_ids"], attempt_id]
    ledger = update_ledger(run_dir, {
        "state": "running",
        "selected_task_id": task["id"],
        "active_attempt_id": attempt_id,
        "selected_task_baseline_ref": task_baseline_ref,
        "selected_task_baseline_digest": task_baseline_digest,
        "tasks": running_tasks,
    })

    def stop_active_attempt(reason: str) -> int:
        print(reason, file=sys.stderr)
        stopped_tasks = [dict(entry) for entry in ledger["tasks"]]
        next(entry for entry in stopped_tasks if entry["id"] == task["id"])["state"] = "stopped"
        update_ledger(run_dir, {
            "state": "stopped",
            "selected_task_id": None,
            "active_attempt_id": None,
            "tasks": stopped_tasks,
        })
        return 1

    # Launch through worker adapter
    result = subprocess.run(
        adapter_invocation,
        text=True,
        capture_output=True,
    )

    if result.returncode != 0:
        return stop_active_attempt(f"Worker error: {result.stderr}")

    # Parse the adapter's terminal output and durable state.
    try:
        output = json.loads(result.stdout)
        state_path = Path(output["state_path"]).resolve()
        expected_state_path = (attempt_dir / "state.json").resolve()
        if state_path != expected_state_path or not state_path.is_file():
            raise ValueError("adapter state path is missing or outside the active attempt")
        adapter_state = json.loads(state_path.read_text())
    except (KeyError, OSError, ValueError, json.JSONDecodeError) as error:
        return stop_active_attempt(f"Invalid adapter terminal output: {error}")

    terminal_statuses = {"awaiting_inspection", "resumable", "stopped"}
    if (
        adapter_state.get("status") not in terminal_statuses
        or output.get("status") != adapter_state.get("status")
        or adapter_state.get("process_pid") is not None
        or not isinstance(adapter_state.get("exit_code"), int)
        or not isinstance(adapter_state.get("ended_at"), str)
        or adapter_state.get("prompt_sha256") != attempt_record["prompt_sha256"]
    ):
        return stop_active_attempt("Invalid or non-terminal adapter state")

    # Collect closure evidence
    current_status = capture_git_status(repo)
    task_baseline = json.loads(
        (run_dir / "baselines" / task_baseline_ref).read_text()
    )
    if sha256_text(canonical_json(task_baseline)) != task_baseline_digest:
        return stop_active_attempt("Selected task baseline digest mismatch")

    # Read result if it exists
    result_path = Path(output.get("result_path", "")).resolve()
    expected_result_path = (attempt_dir / "turn-001.result.json").resolve()
    recorded_result_path = Path(adapter_state.get("result_path", "")).resolve()
    terminal_record_path = expected_result_path.with_suffix(".state.json")
    if (
        result_path != expected_result_path
        or recorded_result_path != expected_result_path
        or not result_path.is_file()
        or not terminal_record_path.is_file()
    ):
        return stop_active_attempt("Adapter result is missing or outside the active attempt")
    try:
        worker_result = json.loads(result_path.read_text())
        terminal_record = json.loads(terminal_record_path.read_text())
    except (OSError, json.JSONDecodeError) as error:
        return stop_active_attempt(f"Adapter result is invalid: {error}")
    validated_outcome = _worker_module.result_status(result_path)
    if (
        terminal_record != adapter_state
        or validated_outcome is None
        or validated_outcome != adapter_state.get("attempt_outcome")
    ):
        return stop_active_attempt("Adapter result and terminal state do not match")

    closure_dir = run_dir / "closure"
    closure_dir.mkdir(exist_ok=True)

    # Compute full Git evidence
    head_before = task_baseline["head_oid"]
    head_after = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    staged_result = subprocess.run(
        ["git", "-C", str(repo), "diff", "--cached", "--name-status"],
        check=True,
        capture_output=True,
        text=True,
    )
    unstaged_result = subprocess.run(
        ["git", "-C", str(repo), "diff", "--name-status"],
        check=True,
        capture_output=True,
        text=True,
    )
    staged_stat_result = subprocess.run(
        ["git", "-C", str(repo), "diff", "--cached", "--stat"],
        check=True,
        capture_output=True,
        text=True,
    )
    unstaged_stat_result = subprocess.run(
        ["git", "-C", str(repo), "diff", "--stat"],
        check=True,
        capture_output=True,
        text=True,
    )
    untracked_result = subprocess.run(
        ["git", "-C", str(repo), "ls-files", "--others", "--exclude-standard"],
        check=True,
        capture_output=True,
        text=True,
    )
    untracked_paths = (
        sorted(untracked_result.stdout.rstrip("\n").split("\n"))
        if untracked_result.stdout.strip()
        else []
    )
    task_patch_result = subprocess.run(
        [
            "git", "-C", str(repo), "diff", "--binary", head_before, "--",
            *task["allowed_paths"],
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    task_patch = task_patch_result.stdout
    for untracked_path in sorted(set(untracked_paths) & set(task["allowed_paths"])):
        untracked_patch = subprocess.run(
            [
                "git", "-C", str(repo), "diff", "--no-index", "--binary", "--",
                os.devnull, untracked_path,
            ],
            capture_output=True,
            text=True,
        )
        if untracked_patch.returncode not in {0, 1}:
            raise ValueError(
                f"Could not capture patch for untracked allowed path {untracked_path}"
            )
        task_patch += untracked_patch.stdout
    # Compute index tree identity for reconciliation
    index_tree = subprocess.run(
        ["git", "-C", str(repo), "write-tree"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()

    artifact_contents = {
        "staged_name_status": staged_result.stdout,
        "unstaged_name_status": unstaged_result.stdout,
        "staged_stat": staged_stat_result.stdout,
        "unstaged_stat": unstaged_stat_result.stdout,
        "task_patch": task_patch,
    }
    artifact_paths = {
        "staged_name_status": closure_dir / f"{attempt_id}.staged.name-status.txt",
        "unstaged_name_status": closure_dir / f"{attempt_id}.unstaged.name-status.txt",
        "staged_stat": closure_dir / f"{attempt_id}.staged.stat.txt",
        "unstaged_stat": closure_dir / f"{attempt_id}.unstaged.stat.txt",
        "task_patch": closure_dir / f"{attempt_id}.diff.patch",
    }
    artifact_digests: dict[str, str] = {}
    for name, content in artifact_contents.items():
        atomic_write_text(artifact_paths[name], content)
        artifact_digests[name] = sha256_text(content)

    staged_digest = artifact_digests["staged_name_status"]
    unstaged_digest = artifact_digests["unstaged_name_status"]
    patch_digest = artifact_digests["task_patch"]
    index_tree_digest = sha256_text(index_tree)
    head_changed = head_before != head_after
    index_changed = task_baseline["index_tree"] != index_tree
    mechanical_violations = []
    if head_changed:
        mechanical_violations.append("worker changed HEAD despite commit prohibition")
    if index_changed:
        mechanical_violations.append("worker changed the Git index")
    adapter_state_digest = sha256_text(canonical_json(adapter_state))
    evidence_record = {
        "policy_sha256": ledger["policy_sha256"],
        "manifest_sha256": ledger["manifest_sha256"],
        "baseline_sha256": task_baseline_digest,
        "prompt_sha256": attempt_record["prompt_sha256"],
        "head_before": head_before,
        "head_after": head_after,
        "index_tree_before": task_baseline["index_tree"],
        "index_tree_after": index_tree,
        "artifact_digests": artifact_digests,
        "untracked_paths": untracked_paths,
        "adapter_state_digest": adapter_state_digest,
    }
    evidence_digest = sha256_text(canonical_json(evidence_record))
    baseline_status = task_baseline["status"]
    current_paths = set(current_status)
    baseline_paths = set(baseline_status)
    allowed_paths = set(task["allowed_paths"])
    allowed_changed_paths = sorted(
        path
        for path in current_paths
        if path in allowed_paths
        and (path not in baseline_status or current_status[path] != baseline_status[path])
    )
    unexpected_paths = sorted(current_paths - baseline_paths - allowed_paths)
    disappeared_preexisting_paths = sorted(baseline_paths - current_paths)
    modified_preexisting_paths = sorted(
        path
        for path in baseline_paths & current_paths
        if baseline_status[path] != current_status[path]
    )

    # Build the complete closure packet
    closure_packet = {
        "run_id": policy["run_id"],
        "task_id": task["id"],
        "attempt_id": attempt_id,
        "policy_sha256": ledger["policy_sha256"],
        "manifest_sha256": ledger["manifest_sha256"],
        "baseline_sha256": task_baseline_digest,
        "prompt_sha256": attempt_record.get("prompt_sha256"),
        "head_before": head_before,
        "head_after": head_after,
        "index_tree": index_tree,
        "index_tree_digest": index_tree_digest,
        "staged_changes": staged_result.stdout.strip(),
        "staged_digest": staged_digest,
        "unstaged_changes": unstaged_result.stdout.strip(),
        "unstaged_digest": unstaged_digest,
        "untracked_paths": untracked_paths,
        "task_patch": task_patch,
        "task_patch_digest": patch_digest,
        "staged_stat_digest": artifact_digests["staged_stat"],
        "unstaged_stat_digest": artifact_digests["unstaged_stat"],
        "evidence_digest": evidence_digest,
        "adapter_state_digest": adapter_state_digest,
        "evidence_artifacts": {
            name: {
                "path": str(path.relative_to(run_dir)),
                "sha256": artifact_digests[name],
            }
            for name, path in artifact_paths.items()
        },
        "worker_claims": {
            "status": worker_result.get("status") if worker_result else None,
            "result_path": output.get("result_path"),
            "terminal_state": adapter_state.get("status"),
            "attempt_outcome": adapter_state.get("attempt_outcome"),
            "exit_code": adapter_state.get("exit_code"),
            "thread_id": adapter_state.get("thread_id"),
            "state_path": str(state_path),
            "effective_command": adapter_state.get("effective_command"),
            "result": worker_result,
        },
        "controller_observations": {
            "head_changed": head_changed,
            "index_changed": index_changed,
            "mechanical_violations": mechanical_violations,
            "allowed_changed_paths": allowed_changed_paths,
            "unexpected_paths": unexpected_paths,
            "disappeared_preexisting_paths": disappeared_preexisting_paths,
            "modified_preexisting_paths": modified_preexisting_paths,
            "staged_changes": staged_result.stdout.strip(),
            "staged_digest": staged_digest,
            "unstaged_changes": unstaged_result.stdout.strip(),
            "unstaged_digest": unstaged_digest,
            "untracked_paths": untracked_paths,
            "index_tree": index_tree,
            "index_tree_digest": index_tree_digest,
        },
        "controller_verification": "not_collected",
    }

    # Decide before publication so the complete packet is written atomically once.
    closure = decide_closure(
        policy=policy,
        task_id=task["id"],
        allowed_paths=set(task["allowed_paths"]),
        baseline_status=task_baseline["status"],
        current_status=current_status,
        result=worker_result,
        controller_verification=None,  # Stage 2: not_collected
        run_id=policy["run_id"],
        attempt_id=attempt_id,
        prompt_sha256=attempt_record.get("prompt_sha256"),
        evidence_digest=evidence_digest,
    )
    if mechanical_violations:
        closure["accepted"] = False
        closure["reasons"].extend(mechanical_violations)

    closure_packet.update(closure)
    closure_json_path = closure_dir / f"{attempt_id}.json"
    atomic_write_json(closure_json_path, closure_packet)

    awaiting_tasks = [dict(entry) for entry in ledger["tasks"]]
    next(entry for entry in awaiting_tasks if entry["id"] == task["id"])["state"] = "awaiting_inspection"
    update_ledger(run_dir, {
        "state": "awaiting_inspection",
        "selected_task_id": task["id"],
        "active_attempt_id": None,
        "last_closure_path": str(closure_json_path.relative_to(run_dir)),
        "tasks": awaiting_tasks,
    })

    print(json.dumps({
        "status": "awaiting_inspection",
        "task_id": task["id"],
        "closure_path": str(closure_json_path),
    }, sort_keys=True))
    return 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.handler(args)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        parser.error(str(error))
    return 2


if __name__ == "__main__":
    sys.exit(main())
