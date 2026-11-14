"""Inspect producer candidates and execute reserved verifier checks.

Owns candidate freshness, scope checks, check identity, replay and no-relaunch
publication. Public operations inspect_candidate/check_candidate own transactions;
load_current_candidate/current_checks supply validated proof to review consumers.
Dependencies: authority, run records, flow policy, serialization, Git, storage
and verification evidence.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any

from . import run_records
from . import run_authority
from . import flow_policy
from . import record_serialization
from . import controller_git as git
from . import verification_runner
from . import run_storage as storage
from . import check_evidence


def producer_workspace(ledger, inputs):
    return git.capture_candidate_workspace(Path(ledger['repository']), inputs['allowed_paths'])


def producer_context(run_dir, operation_id):
    ledger, flow = run_authority.load_run_context(run_dir)
    policy, manifest, inputs = run_authority.load_input_authority(run_dir, ledger)
    operation = run_records.actor_operation(ledger, operation_id)
    assignment = operation['assignment']
    if any(assignment[k] != ledger[k] for k in ('inputs_sha256', 'policy_sha256', 'flow_sha256')):
        raise ValueError('Stale operation authority')
    if assignment['task_id'] != inputs['task_id']:
        raise ValueError('Task identity mismatch')
    return ledger, flow, policy, inputs, operation


def inspect_candidate(run_dir: Path, operation_id: str) -> dict[str, Any]:
    """Inspect an admitted terminal producer, never an actor's content claims."""
    try:
        with storage.RunCommandLock(run_dir):
            ledger, flow, policy, inputs, operation = producer_context(run_dir, operation_id)
            if run_records.active_actor(ledger):
                raise ValueError('An operation is active or unknown')
            if operation['state'] != 'terminal' or operation['assignment']['stage'] not in {'implement', 'correction'}:
                raise ValueError('Terminal implementation/correction required')
            producers = [item for item in ledger['actor_operations'] if item['assignment']['stage'] in {'implement', 'correction'}]
            if operation is not producers[-1]:
                raise ValueError('Historical producer cannot replace current candidate')
            outcome = operation.get('transport', {}).get('outcome')
            if not outcome or outcome['blocker']:
                raise ValueError('Admitted terminal outcome required')
            raw = storage.read_json(Path(outcome['raw_result_path']))
            run_records.validate_observed_result(operation['assignment'], outcome['observed'], raw)
            if raw['status'] != 'complete':
                raise ValueError('Producer did not complete')
            baseline = storage.read_json(run_dir / 'baselines' / ledger['initial_baseline_path'])
            if record_serialization.sha256_text(record_serialization.canonical_json(baseline)) != ledger['initial_baseline_digest']:
                raise ValueError('Initial baseline identity mismatch')
            if 'index_tree' not in baseline or set(baseline.get('dirty_files', {})) != set(baseline['status']):
                raise ValueError('Frozen baseline lacks owner/index identity; initialize a new reviewed run')
            workspace = producer_workspace(ledger, inputs)
            status = workspace['status']
            dirty = baseline['status']
            violations = sorted(p for p in set(dirty) | set(status)
                                if (p in dirty and (status.get(p) != dirty[p]
                                                   or workspace['files'].get(p) != baseline['dirty_files'][p]))
                                or (p not in dirty and p not in inputs['allowed_paths']))
            staged_paths = git.capture_index_changed_paths(
                Path(ledger['repository']), baseline['index_tree'], workspace['index_tree_oid'])
            violations = sorted(set(violations) | {p for p in staged_paths if p in dirty or p not in inputs['allowed_paths']})
            if workspace['head_oid'] != baseline['head_oid']:
                violations.append('HEAD changed')
            if violations:
                return {'status': 'blocked', 'reason': 'scope_or_owner_work_violation', 'paths': violations}
            candidate = {'operation_id': operation_id, 'assignment': operation['assignment'],
                         'baseline_sha256': ledger['initial_baseline_digest'], 'workspace': workspace}
            digest = record_serialization.sha256_text(record_serialization.canonical_json(candidate))
            relative = f'candidates/{digest}.json'
            storage.publish_or_reuse_bytes(run_dir / relative, storage.canonical_record_bytes(candidate))
            if ledger.get('candidate_sha256') != digest:
                ledger.update(candidate_sha256=digest, candidate_path=relative, current_step='verify')
                ledger.setdefault('evidence', {})['implement'] = {
                    'status': 'passed', 'inputs_sha256': ledger['inputs_sha256'],
                    'candidate_sha256': digest, 'operation_id': operation_id, 'path': relative}
                run_records.save_actor_ledger(run_dir, ledger)
            return {'status': 'passed', 'candidate_sha256': digest, 'path': relative}
    except (OSError, ValueError, KeyError, TypeError) as error:
        return {'status': 'refused', 'reason': str(error)}


def load_current_candidate(run_dir, ledger, inputs):
    raw = (run_dir / ledger['candidate_path']).read_bytes()
    candidate = json.loads(raw)
    if run_records.sha256_bytes(raw) != ledger['candidate_sha256']:
        raise ValueError('Candidate artifact identity mismatch')
    if candidate['workspace'] != producer_workspace(ledger, inputs):
        raise ValueError('Candidate is stale')
    if any(candidate['assignment'][k] != ledger[k] for k in ('inputs_sha256', 'policy_sha256', 'flow_sha256')):
        raise ValueError('Candidate authority is stale')
    return candidate


def check_closure_identity(ledger, operation, candidate):
    assignment = operation['assignment']
    workspace = candidate['workspace']
    return {
        'subject': {'run_id': ledger['run_id'], 'task_id': assignment['task_id'],
                    'attempt_id': operation['operation_id'], 'turn': 1,
                    'policy_sha256': ledger['policy_sha256'], 'manifest_sha256': ledger['manifest_sha256'],
                    'prompt_sha256': ledger['inputs_sha256'],
                    'selected_task_baseline_sha256': ledger['initial_baseline_digest']},
        'stage2_git_evidence_sha256': ledger['candidate_sha256'],
        'post_worker_head_oid': workspace['head_oid'],
        'post_worker_index_tree_oid': workspace['index_tree_oid'],
        'post_worker_status_sha256': record_serialization.sha256_text(record_serialization.canonical_json(workspace['status']))}


def _publish_check_outcome(run_dir, ledger, operation, result):
    operation['state'] = 'terminal'
    ledger['active_operation_path'] = None
    ledger.setdefault('evidence', {})['verify'] = {
        'status': result['status'], 'inputs_sha256': ledger['inputs_sha256'],
        'candidate_sha256': operation['assignment']['candidate_sha256'],
        'operation_id': operation['operation_id'], 'path': result['path'],
        'sha256': run_records.sha256_bytes((run_dir / result['path']).read_bytes())}
    ledger['actor_blocker'] = result.get('blocker')
    if result['status'] == 'failed':
        ledger.update(correction_request='check_failed')
    elif result['status'] == 'passed':
        ledger['current_step'] = 'semantic_review'
    run_records.save_actor_ledger(run_dir, ledger)


def check_candidate(run_dir: Path, assignment: dict[str, Any], *, timeout_seconds: float) -> dict[str, Any]:
    """Run one reserved check once; uncertain interrupted execution never relaunches."""
    if type(timeout_seconds) not in {int, float} or not math.isfinite(timeout_seconds) or timeout_seconds <= 0:
        return {'status': 'refused', 'reason': 'timeout_seconds must be positive and finite'}
    try:
        with storage.RunCommandLock(run_dir):
            ledger, flow, policy, inputs, operation = producer_context(run_dir, assignment['operation_id'])
            if not run_records.same_typed_assignment(assignment, operation['assignment']) or assignment['stage'] != 'verify':
                raise ValueError('Exact verifier assignment required')
            if assignment['candidate_sha256'] != ledger.get('candidate_sha256'):
                raise ValueError('Historical candidate cannot become current')
            candidate = load_current_candidate(run_dir, ledger, inputs)
            relative = f"checks/{operation['operation_id']}.json"
            path = run_dir / relative
            if path.exists():
                result = storage.read_json(path)
                if not run_records.same_typed_assignment(result['assignment'], assignment) or result['timeout_seconds'] != timeout_seconds:
                    raise ValueError('Check identity/configuration conflict')
                if result['status'] == 'blocked' and 'execution_sha256' not in result:
                    return result
                identity = check_closure_identity(ledger, operation, candidate)
                if result['status'] == 'stale':
                    # Workspace drift is an application outcome, independent of
                    # the completed execution's derived check disposition.
                    post_workspace = result.get('post_workspace')
                    if not isinstance(post_workspace, dict) or post_workspace == candidate['workspace']:
                        raise ValueError('Check disposition contradicts recorded workspace')
                    check_evidence.validate_execution_evidence(run_dir, result, identity)
                else:
                    check_evidence.validate_check_evidence(run_dir, result, identity)
                if operation['state'] != 'terminal':
                    _publish_check_outcome(run_dir, ledger, operation, result)
                return result
            if operation['state'] != 'reserved':
                return {'status': 'blocked', 'blocker': 'Check execution uncertain; inspect retained evidence and resolve terminality before retry'}
            if run_records.active_actor(ledger) is not operation:
                raise ValueError('Check does not own active operation')
            selected = {'required_checks': inputs['required_checks']}
            check_policy = json.loads(json.dumps(policy))
            check_policy['verification']['authorized_gap'] = None
            omitted = []
            if flow_policy.flow_step(flow, 'verify')['mode'] == 'targeted':
                if check_policy['verification']['repository_gate']:
                    omitted.append('repository_gate')
                check_policy['verification']['repository_gate'] = None
            plan = verification_runner.build_verification_plan(selected, check_policy)
            identity = check_closure_identity(ledger, operation, candidate)
            execution_path = f"verification/{operation['operation_id']}.turn-001.execution.json"
            intent = {'assignment': assignment, 'timeout_seconds': timeout_seconds, 'plan': plan,
                      'candidate_sha256': ledger['candidate_sha256']}
            storage.publish_or_reuse_bytes(run_dir / f"checks/{operation['operation_id']}.intent.json", storage.canonical_record_bytes(intent))
            operation['state'] = 'unknown'
            run_records.save_actor_ledger(run_dir, ledger)
            (run_dir / 'verification').mkdir(exist_ok=True)
            result = {'assignment': assignment, 'timeout_seconds': timeout_seconds, 'path': relative,
                      'execution_path': execution_path, 'policy_omissions': omitted, 'plan': plan,
                      'mechanism_limits': 'YOLO does not enforce filesystem or network restrictions',
                      'environment': {'cwd': ledger['repository'], 'platform': sys.platform},
                      'setup': inputs, 'status': 'blocked', 'blocker': None}
            try:
                execution, digest = verification_runner.execute_verification_plan(
                    plan=plan, repository_cwd=ledger['repository'], permissions=policy['permissions'],
                    timeout_seconds=timeout_seconds, run_directory=run_dir.resolve(), execution_path=execution_path,
                    closure_identity=identity, execution_authorization=policy['execution_authorization'])
                result['execution_sha256'] = digest
                result['status'] = check_evidence.execution_disposition(execution)
                result['post_workspace'] = producer_workspace(ledger, inputs)
                if result['post_workspace'] != candidate['workspace']:
                    result['status'] = 'stale'
            except (OSError, ValueError, RuntimeError) as error:
                # No completed record means terminality cannot be inferred. Keep
                # the operation unknown, even for a truthful infrastructure error.
                ledger['actor_blocker'] = str(error) + '; inspect retained check evidence before retry'
                result['blocker'] = ledger['actor_blocker']
                storage.publish_or_reuse_bytes(path, storage.canonical_record_bytes(result))
                ledger.setdefault('evidence', {})['verify'] = {
                    'status': 'blocked', 'inputs_sha256': ledger['inputs_sha256'],
                    'candidate_sha256': ledger['candidate_sha256'],
                    'operation_id': operation['operation_id'], 'path': relative}
                run_records.save_actor_ledger(run_dir, ledger)
                return result
            storage.publish_or_reuse_bytes(path, storage.canonical_record_bytes(result))
            _publish_check_outcome(run_dir, ledger, operation, result)
            return result
    except (OSError, ValueError, KeyError, TypeError) as error:
        return {'status': 'stale' if 'stale' in str(error).lower() else 'refused', 'reason': str(error)}


def current_checks(run_dir, ledger, candidate):
    evidence = run_records.evidence_view(ledger, 'verify')
    if evidence['status'] != 'passed':
        raise ValueError('Current passed required checks required')
    result = run_records.retained_json(run_dir, evidence['path'], evidence.get('sha256'))
    operation = run_records.actor_operation(ledger, evidence['operation_id'])
    if (not run_records.same_typed_assignment(result['assignment'], operation['assignment'])
            or any(result['assignment'][key] != ledger[key] for key in
                   ('candidate_sha256', 'inputs_sha256', 'policy_sha256', 'flow_sha256'))
            or result['status'] != 'passed'):
        raise ValueError('Required check identity mismatch')
    check_evidence.validate_check_evidence(run_dir, result, check_closure_identity(ledger, operation, candidate))
    return result

