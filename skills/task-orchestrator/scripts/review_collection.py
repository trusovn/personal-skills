"""Prepare, rerun and admit independent collection evidence.

Owns collector session/rerun authority, retained collection validation and finding
history. check_collection owns the rerun transaction. Admission updates the caller
ledger under actor_lifecycle ownership; it does not persist that ledger or accept work.
Dependencies: candidate checks, authority, run records, flow policy, review
contracts, storage and verification.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

from . import run_records
from . import run_authority
from . import candidate_checks
from . import flow_policy
from . import review_contracts
from . import verification_runner
from . import run_storage as storage
from . import check_evidence


def collection_check_paths(operation):
    identity = operation['operation_id'] + '.rerun'
    return identity, f'collection-checks/{identity}.json', f'collection-checks/{identity}.intent.json'


def collection_check_unresolved(run_dir, operation):
    if operation['assignment']['stage'] != 'semantic_review':
        return False
    _, result, intent = collection_check_paths(operation)
    if not (run_dir / intent).exists():
        return False
    try:
        return 'execution_sha256' not in storage.read_json(run_dir / result)
    except (OSError, ValueError):
        return True


def collection_launch_context(run_dir, ledger, inputs, operation):
    candidate = candidate_checks.load_current_candidate(run_dir, ledger, inputs)
    check = candidate_checks.current_checks(run_dir, ledger, candidate)
    return {'run_dir': str(run_dir.resolve()), 'controller_path': str(Path(__file__).with_name('controller.py').resolve()),
            'candidate': candidate, 'check_evidence': check,
            'prior_findings': ledger.get('outstanding_findings', []),
            'review_requirements': ['requirements', 'behavior', 'code_quality'],
            'review_workflow': {
                'skill_resolution': 'Use matching project-local .agents/skills installations first; source presence is not availability. Never substitute source or refresh installations. Block unavailable mandatory review capabilities.',
                'collection': 'Fresh independent task-review-discovery gathers evidence without deciding acceptance',
                'separate_stages': ['task-maintainability-review when required', 'task-contract-registry-updater when contracts change', 'task-review-discovery', 'separate task-acceptance-review'],
                'authority': 'Frozen brief, verification and repository instructions determine applicability; collection grants no acceptance or deferral authority'},
            'rerun_callable': 'check_collection(run_dir, assignment, timeout_seconds=...)',
            'rerun_cli': 'check-collection --run-dir RUN --request ASSIGNMENT --timeout-seconds N'}


def _collection_check_context(run_dir, assignment):
    ledger, flow, policy, inputs, operation = candidate_checks.producer_context(run_dir, assignment['operation_id'])
    if not run_records.same_typed_assignment(assignment, operation['assignment']) or assignment['stage'] != 'semantic_review':
        raise ValueError('Exact collector assignment required')
    if run_records.active_actor(ledger) is not operation or operation['state'] not in {'running', 'unknown'}:
        raise ValueError('Only the active launched collector can request reruns')
    observed, _ = run_records.read_actor_observation(run_records.actor_directory(run_dir, operation), operation)
    if not observed.get('thread_id'):
        raise ValueError('Observed collector session required')
    candidate = candidate_checks.load_current_candidate(run_dir, ledger, inputs)
    if assignment['candidate_sha256'] != ledger.get('candidate_sha256'):
        raise ValueError('Collector candidate is stale')
    return ledger, flow, policy, inputs, operation, observed, candidate


def check_collection(run_dir: Path, assignment: dict[str, Any], *, timeout_seconds: float) -> dict[str, Any]:
    """Execute one collector-owned full-plan rerun; never launch another actor."""
    if type(timeout_seconds) not in {int, float} or not math.isfinite(timeout_seconds) or timeout_seconds <= 0:
        return {'status': 'refused', 'reason': 'timeout_seconds must be positive and finite'}
    try:
        with storage.RunCommandLock(run_dir):
            ledger, flow, policy, inputs, operation, observed, candidate = _collection_check_context(run_dir, assignment)
            identity, relative, intent_path = collection_check_paths(operation)
            checker = dict(operation, operation_id=identity)
            closure = candidate_checks.check_closure_identity(ledger, checker, candidate)
            if (run_dir / relative).exists():
                result = storage.read_json(run_dir / relative)
                if not run_records.same_typed_assignment(result['assignment'], assignment) or result['timeout_seconds'] != timeout_seconds or result['session_id'] != observed['thread_id']:
                    raise ValueError('Collector rerun replay conflict')
                if 'execution_sha256' in result and result['status'] != 'stale':
                    check_evidence.validate_check_evidence(run_dir, result, closure)
                return result
            if (run_dir / intent_path).exists():
                return {'status': 'blocked', 'blocker': 'Collection rerun terminality unresolved; inspect retained intent and logs; do not relaunch'}
            check_policy = json.loads(json.dumps(policy))
            check_policy['verification']['authorized_gap'] = None
            if flow_policy.flow_step(flow, 'verify')['mode'] == 'targeted':
                check_policy['verification']['repository_gate'] = None
            plan = verification_runner.build_verification_plan({'required_checks': inputs['required_checks']}, check_policy)
            result = {'operation_id': identity, 'assignment': assignment, 'session_id': observed['thread_id'],
                      'candidate_sha256': ledger['candidate_sha256'], 'timeout_seconds': timeout_seconds,
                      'path': relative, 'plan': plan, 'setup': inputs,
                      'execution_path': f'verification/{identity}.turn-001.execution.json',
                      'status': 'blocked', 'blocker': None}
            storage.publish_or_reuse_bytes(run_dir / intent_path, storage.canonical_record_bytes(result))
            (run_dir / 'verification').mkdir(exist_ok=True)
            try:
                execution, digest = verification_runner.execute_verification_plan(
                    plan=plan, repository_cwd=ledger['repository'], permissions=policy['permissions'],
                    timeout_seconds=timeout_seconds, run_directory=run_dir.resolve(),
                    execution_path=result['execution_path'], closure_identity=closure,
                    execution_authorization=policy['execution_authorization'])
                result['execution_sha256'] = digest
                result['status'] = check_evidence.execution_disposition(execution)
                if candidate_checks.producer_workspace(ledger, inputs) != candidate['workspace']:
                    result['status'] = 'stale'
            except (OSError, ValueError, RuntimeError) as error:
                result['blocker'] = str(error) + '; rerun terminality unresolved; inspect retained evidence'
            storage.publish_or_reuse_bytes(run_dir / relative, storage.canonical_record_bytes(result))
            return result
    except (OSError, ValueError, KeyError, TypeError) as error:
        return {'status': 'stale' if 'stale' in str(error).lower() else 'refused', 'reason': str(error)}


def collection_evidence(ledger, operation, status, blocker=None, path=None):
    assignment = operation['assignment']
    ledger.setdefault('evidence', {})['semantic_review'] = {
        'status': status, 'inputs_sha256': assignment['inputs_sha256'],
        'candidate_sha256': assignment['candidate_sha256'],
        'operation_id': operation['operation_id'], 'path': path, 'blocker': blocker}


def validate_current_collection(run_dir, ledger):
    evidence = run_records.evidence_view(ledger, 'semantic_review')
    if evidence.get('status') != 'passed':
        raise ValueError('Current successful collection required')
    record = run_records.retained_json(run_dir, evidence['path'], evidence.get('sha256'))
    operation = run_records.actor_operation(ledger, evidence['operation_id'])
    if (not run_records.same_typed_assignment(record['assignment'], operation['assignment'])
            or record['status'] != 'passed'
            or any(record['assignment'][key] != ledger[key] for key in ('candidate_sha256', 'inputs_sha256', 'policy_sha256', 'flow_sha256'))):
        raise ValueError('Admitted collection identity is stale or changed')
    review_contracts.validate_collection_report(record['report'])
    if record['report']['gaps'] or any(item['status'] != 'passed' for item in record['report']['coverage'].values()):
        raise ValueError('Incomplete collection')
    rerun = run_records.retained_json(run_dir, record['report']['rerun_path'], record['rerun_sha256'])
    if not run_records.same_typed_assignment(rerun['assignment'], operation['assignment']) or rerun['session_id'] != record['observed']['thread_id']:
        raise ValueError('Collection rerun provenance changed')
    candidate = candidate_checks.load_current_candidate(run_dir, ledger, run_authority.load_frozen_inputs(run_dir, ledger))
    checker = dict(operation, operation_id=rerun['operation_id'])
    check_evidence.validate_check_evidence(run_dir, rerun, candidate_checks.check_closure_identity(ledger, checker, candidate))
    return record


def _merge_collection_findings(previous, findings, assignment):
    merged = {finding['id']: json.loads(json.dumps(finding)) for finding in previous}
    for finding in findings:
        current = merged.get(finding['id'])
        history = current.get('history', []) if current else []
        disposition = current.get('disposition') if current else None
        if disposition and current and (set(current['evidence']) != set(finding['evidence']) or current['exposure'] != finding['exposure']):
            disposition = {'status': 'reopened', 'previous': disposition,
                           'reason': 'new relevant evidence or changed exposure'}
        snapshot = {**finding, 'operation_id': assignment['operation_id'],
                    'candidate_sha256': assignment['candidate_sha256'], 'disposition': disposition}
        merged[finding['id']] = {**finding, 'disposition': disposition, 'history': history + [snapshot]}
    return list(merged.values())


def admit_collection(run_dir, ledger, operation, observed, result):
    assignment = operation['assignment']
    inputs = run_authority.load_frozen_inputs(run_dir, ledger)
    if any(assignment[key] != ledger[key] for key in ('inputs_sha256', 'policy_sha256', 'flow_sha256', 'candidate_sha256')):
        raise ValueError('Collection authority or candidate is stale')
    candidate = candidate_checks.load_current_candidate(run_dir, ledger, inputs)
    producer_sessions = {item.get('transport', {}).get('outcome', {}).get('observed', {}).get('thread_id')
                         for item in ledger['actor_operations'] if item['assignment']['stage'] in {'implement', 'correction'} and item.get('transport', {}).get('outcome')}
    if observed['thread_id'] in producer_sessions:
        raise ValueError('Collection session is not independent of implementation/correction')
    if result['session_id'] != observed['thread_id']:
        raise ValueError('Collection must bind the observed session explicitly')
    if result['readiness'] is not None:
        raise ValueError('Collection cannot supply preflight readiness authority')
    report = result['collection']
    review_contracts.validate_collection_report(report)
    _, rerun_path, _ = collection_check_paths(operation)
    status, blocker = 'passed', None
    if report['rerun_path'] is None:
        status, blocker = 'not_run', 'Missing independent rerun evidence; request fresh collection checks'
    else:
        if report['rerun_path'] != rerun_path:
            raise ValueError('Fresh collector-owned rerun required; historical verifier evidence cannot cover collection')
        rerun = storage.read_json(run_dir / rerun_path)
        if not run_records.same_typed_assignment(rerun['assignment'], assignment) or rerun['session_id'] != observed['thread_id'] or rerun['candidate_sha256'] != ledger['candidate_sha256']:
            raise ValueError('Collector rerun binding mismatch')
        checker = dict(operation, operation_id=rerun['operation_id'])
        check_evidence.validate_check_evidence(run_dir, rerun, candidate_checks.check_closure_identity(ledger, checker, candidate))
        status = rerun['status']
        if status != 'passed':
            blocker = 'Independent required check failed; bounded check_failed correction required' if status == 'failed' else 'Required independent checks not run; collect missing evidence'
    if result['status'] != 'complete' or any(item['status'] == 'blocked' for item in report['coverage'].values()):
        status, blocker = 'blocked', 'Review capability or authority unresolved; inspect report and relay blocker in active chat'
    elif status == 'passed' and (report['gaps'] or any(item['status'] != 'passed' for item in report['coverage'].values())):
        status, blocker = 'not_run', 'Required collection coverage gaps; rerun or recollect missing evidence'
    record = {'assignment': assignment, 'observed': observed, 'report': report,
              'status': status, 'blocker': blocker,
              'rerun_sha256': run_records.sha256_bytes((run_dir / report['rerun_path']).read_bytes()) if report['rerun_path'] else None}
    relative = f"collections/{operation['operation_id']}.json"
    storage.publish_or_reuse_bytes(run_dir / relative, storage.canonical_record_bytes(record))
    findings = _merge_collection_findings(ledger.get('outstanding_findings', []), report['findings'], assignment)
    ledger['outstanding_findings'] = findings
    collection_evidence(ledger, operation, status, blocker, relative)
    ledger['evidence']['semantic_review']['sha256'] = run_records.sha256_bytes((run_dir / relative).read_bytes())
    if status == 'failed':
        ledger['correction_request'] = 'check_failed'
    ledger['current_step'] = 'acceptance' if status == 'passed' else 'semantic_review'
    return blocker

