"""Integrity of completed actor check evidence, independent of stage authority.

Owns execution/result digest binding, execution identity/schema, retained log
integrity and derived execution disposition. The application owns assignments,
freshness, collector session/rerun ownership, omissions, stale-workspace routing,
locks, process execution and publication. No controller or transport dependency;
execution_contracts remains the authority for execution-record structure.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any


_loader_spec = importlib.util.spec_from_file_location(
    "task_orchestrator_component_loading", Path(__file__).with_name("__init__.py"),
)
_loader = importlib.util.module_from_spec(_loader_spec)
assert _loader_spec.loader is not None
_loader_spec.loader.exec_module(_loader)
_load_component = _loader.load_component
_execution_contracts = _load_component("execution_contracts")


def execution_disposition(execution: dict[str, Any]) -> str:
    """Derive the check vocabulary from a validated completed execution record."""
    if not execution['outcomes']:
        return 'not_run'
    return 'passed' if execution['terminal_reason'] == 'complete' else 'failed'


def validate_execution_evidence(
    run_dir: Path, result: dict[str, Any], identity: dict[str, Any],
) -> dict[str, Any]:
    """Read and validate retained proof; return execution or reject without writes.

    Missing files propagate OSError; malformed or contradictory evidence raises
    ValueError (missing fields/types remain KeyError/TypeError). Callers retain
    their existing bounded refusal/recovery mapping. This does not authorize a
    result or infer terminality for an incomplete execution.
    """
    raw = (run_dir / result['execution_path']).read_bytes()
    if hashlib.sha256(raw).hexdigest() != result['execution_sha256']:
        raise ValueError('Execution record changed')
    execution = json.loads(raw)
    _execution_contracts.validate_command_execution_record(
        execution, expected_closure_identity=identity)
    for outcome in execution['outcomes']:
        for stream in ('stdout', 'stderr'):
            raw_log = (run_dir / outcome[f'{stream}_path']).read_bytes()
            if hashlib.sha256(raw_log).hexdigest() != outcome[f'{stream}_sha256']:
                raise ValueError('Execution log changed')
    return execution


def validate_check_evidence(
    run_dir: Path, result: dict[str, Any], identity: dict[str, Any],
) -> dict[str, Any]:
    """Validate execution proof and require the result's derived disposition."""
    execution = validate_execution_evidence(run_dir, result, identity)
    if result['status'] != execution_disposition(execution):
        raise ValueError('Check disposition contradicts execution')
    return execution
