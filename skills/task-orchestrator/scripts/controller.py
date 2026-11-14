#!/usr/bin/env python3
"""Task orchestrator CLI, application composition and compatibility entry points."""

from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path
import sys
from typing import Any


_loader_spec = importlib.util.spec_from_file_location(
    "task_orchestrator_component_loading", Path(__file__).with_name("__init__.py"),
)
_loader = importlib.util.module_from_spec(_loader_spec)
assert _loader_spec.loader is not None
_loader_spec.loader.exec_module(_loader)
_load_component = _loader.load_component


_state_module = _load_component("controller_state")
_git_module = _load_component("controller_git")
_worker_module = _load_component("codex_worker")
_verification_module = _load_component("verification_runner")
_storage_module = _load_component("run_storage")
_check_evidence_module = _load_component("check_evidence")
run_records = _load_component("run_records")
run_authority = _load_component("run_authority")
candidate_checks = _load_component("candidate_checks")
review_collection = _load_component("review_collection")
acceptance_workflow = _load_component("acceptance_workflow")
operation_scheduling = _load_component("operation_scheduling")
actor_lifecycle = _load_component("actor_lifecycle")
input_revision = _load_component("input_revision")
legacy_attempts = _load_component("legacy_attempts")
legacy_inspection = _load_component("legacy_inspection")

# Existing Python entry points delegate to their responsibility owner.
ATTEMPT_REQUIRED_FIELDS = _state_module.ATTEMPT_REQUIRED_FIELDS
ALLOWED_TASK_TRANSITIONS = _state_module.ALLOWED_TASK_TRANSITIONS
ALLOWED_RUN_TRANSITIONS = _state_module.ALLOWED_RUN_TRANSITIONS
canonical_json = _state_module.canonical_json
sha256_text = _state_module.sha256_text
validate_run_policy = _state_module.validate_run_policy
validate_flow_profile = _state_module.validate_flow_profile
resolve_flow_profile = _state_module.resolve_flow_profile
validate_flow_cursor = _state_module.validate_flow_cursor
transition_flow_cursor = _state_module.transition_flow_cursor
transition_task = _state_module.transition_task
transition_run = _state_module.transition_run
validate_attempt_record = _state_module.validate_attempt_record
build_attempt_record = _state_module.build_attempt_record
validate_task_manifest = _state_module.validate_task_manifest
select_task = _state_module.select_task
_validate_task_manifest_schema = _state_module._validate_task_manifest_schema
_detect_dependency_cycles = _state_module._detect_dependency_cycles
_is_valid_repo_relative_path = _state_module.is_valid_repo_relative_path
_validate_ledger = _state_module.validate_ledger
capture_git_status = _git_module.capture_git_status
capture_initial_baseline = _git_module.capture_initial_baseline
atomic_write_json = _storage_module.atomic_write_json
RunCommandLock = _storage_module.RunCommandLock
persist_run_policy = run_authority.persist_run_policy
load_input_authority = run_authority.load_input_authority
load_frozen_inputs = run_authority.load_frozen_inputs
init_run = run_authority.init_run
update_ledger = run_authority.update_ledger
revise_flow = run_authority.revise_flow
inspect_candidate = candidate_checks.inspect_candidate
check_candidate = candidate_checks.check_candidate
check_collection = review_collection.check_collection
status_run = operation_scheduling.status_run
reserve_operation = operation_scheduling.reserve_operation
launch_operation = actor_lifecycle.launch_operation
observe_operation = actor_lifecycle.observe_operation
stop_operation = actor_lifecycle.stop_operation
record_intervention = actor_lifecycle.record_intervention
revise_inputs = input_revision.revise_inputs
render_worker_prompt = legacy_attempts.render_worker_prompt
decide_closure = legacy_attempts.decide_closure
create_attempt = legacy_attempts.create_attempt
inspect_run = legacy_inspection.inspect_run


def _legacy_run_next(args: Any) -> int:
    """Private compatibility launcher retained for legacy inspection callers."""
    result = legacy_attempts.run_next(
        Path(args.run_dir), timeout_seconds=args.timeout_seconds, codex_bin=args.codex_bin,
    )
    if result["status"] == "stopped":
        print(result["reason"], file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


def _cli_actor(args: Any) -> int:
    run_dir = Path(args.run_dir).resolve()
    if args.command == "launch":
        result = launch_operation(run_dir, _storage_module.read_json(Path(args.request)),
                                  codex_bin=args.codex_bin, timeout_seconds=args.timeout_seconds)
    elif args.command == "intervene":
        result = record_intervention(run_dir, _storage_module.read_json(Path(args.request)))
    else:
        handler = observe_operation if args.command == "observe" else stop_operation
        result = handler(run_dir, args.operation_id)
    print(json.dumps(result, sort_keys=True))
    return int(result["status"] == "refused")


def _cli_revise_inputs(args: Any) -> int:
    result = revise_inputs(Path(args.run_dir), json.loads(Path(args.request).read_text()))
    print(json.dumps(result, sort_keys=True))
    return 1 if result["status"] == "refused" else 0


def _cli_status(args: Any) -> int:
    print(json.dumps(status_run(Path(args.run_dir).resolve()), sort_keys=True))
    return 0


def _cli_reserve(args: Any) -> int:
    result = reserve_operation(Path(args.run_dir).resolve(), expected_version=args.expected_version,
                               task_id=args.task_id, stage=args.stage, role=args.role,
                               operation_key=args.operation_key, reason=args.reason)
    print(json.dumps(result, sort_keys=True))
    return 0 if result["status"] != "refused" else 1


def _cli_run_next(args: Any) -> int:
    if not math.isfinite(args.timeout_seconds) or args.timeout_seconds <= 0:
        raise ValueError("timeout must be greater than zero")
    result = status_run(Path(args.run_dir).resolve())
    print(json.dumps({"status": "pending", "task_id": result["task_id"],
                      "current_step": result["stage"], "reason": result["blocker"] or "successor_launch_pending",
                      "next_actions": result["next_actions"]}, sort_keys=True))
    return 0


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

    runnext_parser = subparsers.add_parser("run-next", help="Report pending successor launch work")
    runnext_parser.add_argument("--run-dir", required=True)
    runnext_parser.add_argument("--timeout-seconds", type=float, required=True)
    runnext_parser.add_argument("--codex-bin", default="codex", help=argparse.SUPPRESS)
    runnext_parser.set_defaults(handler=_cli_run_next)

    inspect_parser = subparsers.add_parser(
        "inspect", help="Independently verify one completed worker attempt"
    )
    inspect_parser.add_argument("--run-dir", required=True)
    inspect_parser.add_argument("--timeout-seconds", type=float, required=True)
    inspect_parser.set_defaults(handler=_cli_inspect)

    revise_parser = subparsers.add_parser(
        "revise-flow", help="Publish a flow revision at a safe task boundary"
    )
    revise_parser.add_argument("--run-dir", required=True)
    revise_parser.add_argument("--flow", required=True)
    revise_parser.set_defaults(handler=_cli_revise_flow)

    status_parser = subparsers.add_parser("status", help="Read current task and operation status")
    status_parser.add_argument("--run-dir", required=True)
    status_parser.set_defaults(handler=_cli_status)
    reserve_parser = subparsers.add_parser("reserve", help="Reserve one permitted operation")
    reserve_parser.add_argument("--run-dir", required=True)
    reserve_parser.add_argument("--expected-version", type=int, required=True)
    for field in ("task-id", "stage", "role", "operation-key"):
        reserve_parser.add_argument(f"--{field}", required=True)
    reserve_parser.add_argument("--reason", default="initial")
    reserve_parser.set_defaults(handler=_cli_reserve)
    inputs_parser = subparsers.add_parser("revise-inputs", help="Publish an explicit owner-authorized input revision")
    inputs_parser.add_argument("--run-dir", required=True)
    inputs_parser.add_argument("--request", required=True, help="JSON request including bound owner response")
    inputs_parser.set_defaults(handler=_cli_revise_inputs)
    for command in ("launch", "observe", "stop", "intervene"):
        actor_parser = subparsers.add_parser(command)
        actor_parser.add_argument("--run-dir", required=True)
        if command in {"launch", "intervene"}:
            actor_parser.add_argument("--request", required=True)
        else:
            actor_parser.add_argument("--operation-id", required=True)
        if command == "launch":
            actor_parser.add_argument("--codex-bin", default="codex")
            actor_parser.add_argument("--timeout-seconds", type=float, default=300)
        actor_parser.set_defaults(handler=_cli_actor)
    for command in ('inspect-candidate', 'check-candidate', 'check-collection'):
        producer = subparsers.add_parser(command)
        producer.add_argument('--run-dir', required=True)
        if command == 'inspect-candidate':
            producer.add_argument('--operation-id', required=True)
        else:
            producer.add_argument('--request', required=True)
            producer.add_argument('--timeout-seconds', type=float, required=True)
        producer.set_defaults(handler=_cli_producer)
    return parser


def _cli_producer(args):
    run_dir = Path(args.run_dir).resolve()
    if args.command == 'inspect-candidate':
        result = inspect_candidate(run_dir, args.operation_id)
    else:
        runner = check_collection if args.command == 'check-collection' else check_candidate
        result = runner(run_dir, _storage_module.read_json(Path(args.request)), timeout_seconds=args.timeout_seconds)
    print(json.dumps(result, sort_keys=True))
    return 0 if result['status'] in {'passed', 'failed', 'stale'} else 1


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


def _cli_inspect(args: "argparse.Namespace") -> int:  # type: ignore[name-defined]
    result = inspect_run(Path(args.run_dir).resolve(), args.timeout_seconds)
    print(json.dumps(result, sort_keys=True))
    return 0


def _cli_revise_flow(args: "argparse.Namespace") -> int:  # type: ignore[name-defined]
    result = revise_flow(
        Path(args.run_dir).resolve(),
        Path(args.flow).resolve(),
    )
    print(json.dumps(result, sort_keys=True))
    return 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.handler(args)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"status": "refused", "reason": str(error), "next_actions": ["intervene"]}, sort_keys=True), file=sys.stderr)
    return 2



if __name__ == "__main__":
    sys.exit(main())
