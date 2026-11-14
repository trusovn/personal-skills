"""Prepare and admit separate acceptance against current evidence.

Owns conditional-review binding, launch context, independent decision admission
and current-decision revalidation. The acceptance policy evaluates dispositions;
actor_lifecycle owns the enclosing lock and ledger commit. No completion/tracker writes.
Dependencies: authority, run records, candidate checks, collection, policy and storage.
"""

from __future__ import annotations

import json
from pathlib import Path

from . import run_records
from . import run_authority
from . import candidate_checks
from . import review_collection
from . import review_contracts
from . import acceptance
from . import run_storage as storage


def _conditional_reviews(run_dir, ledger, inputs):
    records = {}
    for stage in inputs.get('required_reviews', []):
        relative = f"reviews/{ledger['candidate_sha256']}/{stage}.json"
        raw = (run_dir / relative).read_bytes()
        record = json.loads(raw)
        review_contracts.validate_conditional_review(record)
        if (record['stage'] != stage or record['status'] != 'passed'
                or any(record[key] != ledger[key] for key in
                       ('candidate_sha256', 'inputs_sha256', 'policy_sha256', 'flow_sha256'))):
            raise ValueError('Missing current required conditional review: ' + stage)
        sessions = {item.get('transport', {}).get('outcome', {}).get('observed', {}).get('thread_id')
                    for item in ledger['actor_operations'] if item['assignment']['stage'] in {'implement', 'correction'}}
        if record['session_id'] in sessions:
            raise ValueError('Conditional review is not independent')
        for path, digest in record['evidence'].items():
            run_records.retained_bytes(run_dir, path, digest)
        records[relative] = run_records.sha256_bytes(raw)
    return records


def acceptance_context(run_dir, ledger, inputs):
    candidate = candidate_checks.load_current_candidate(run_dir, ledger, inputs)
    for document in inputs['documents'].values():
        source = Path(ledger['repository']) / document['source_path']
        if run_records.sha256_bytes(source.read_bytes()) != document.get('source_sha256', document['sha256']):
            raise ValueError('Frozen task source changed; explicit revision and fresh preflight required')
    if not run_records.current_readiness(ledger):
        raise ValueError('Current preflight required')
    checks = candidate_checks.current_checks(run_dir, ledger, candidate)
    collection = review_collection.validate_current_collection(run_dir, ledger)
    references = {ledger['candidate_path']: run_records.sha256_bytes((run_dir / ledger['candidate_path']).read_bytes())}
    for stage in ('verify', 'semantic_review'):
        item = ledger['evidence'][stage]
        references[item['path']] = item['sha256']
    references.update(_conditional_reviews(run_dir, ledger, inputs))
    tracker = Path(ledger['repository']) / 'docs/known-issues.md'
    known_issues = {'path': 'docs/known-issues.md', 'content': tracker.read_text(),
                    'sha256': run_records.sha256_bytes(tracker.read_bytes())} if tracker.is_file() else None
    return {'run_dir': str(run_dir.resolve()), 'candidate': candidate, 'checks': checks, 'collection': collection,
            'known_issue_tracker': known_issues,
            'evidence': references, 'findings': ledger.get('outstanding_findings', []),
            'conditional_reviews': inputs.get('required_reviews', []),
            'conditional_review_records': {path: storage.read_json(run_dir / path)
                                           for path in references if path.startswith('reviews/')},
            'known_issue_history': [finding for finding in ledger.get('outstanding_findings', [])
                                    if finding.get('disposition')],
            'runtime_limits': 'Scripted local roles do not qualify sbx, provider/model identity, edit isolation or semantic judgment; no completion or tracker write is authorized.'}


def acceptance_launch_context(run_dir, ledger, inputs, operation):
    context = acceptance_context(run_dir, ledger, inputs)
    relative = f"acceptance-inputs/{operation['operation_id']}.json"
    storage.publish_or_reuse_bytes(run_dir / relative, storage.canonical_record_bytes(context))
    return context


def admit_acceptance(run_dir, ledger, operation, observed, result):
    assignment = operation['assignment']
    if (result['status'] != 'complete' or result['readiness'] is not None
            or result['session_id'] != observed['thread_id']):
        raise ValueError('Acceptance requires a complete explicitly observed separate session')
    if any(assignment[key] != ledger[key] for key in
           ('inputs_sha256', 'policy_sha256', 'flow_sha256', 'candidate_sha256', 'flow_revision')):
        raise ValueError('Acceptance authority is stale')
    prior_sessions = {item.get('transport', {}).get('outcome', {}).get('observed', {}).get('thread_id')
                      for item in ledger['actor_operations'] if item is not operation}
    if observed['thread_id'] in prior_sessions:
        raise ValueError('Acceptance must use a fresh independent session')
    inputs = run_authority.load_frozen_inputs(run_dir, ledger)
    context = acceptance_context(run_dir, ledger, inputs)
    launched = storage.read_json(run_dir / f"acceptance-inputs/{operation['operation_id']}.json")
    if context != launched:
        raise ValueError('Acceptance evidence changed during review')
    if observed['thread_id'] in {review['session_id'] for review in context['conditional_review_records'].values()}:
        raise ValueError('Acceptance must be separate from conditional reviewers')
    decision = result['decision']
    review_contracts.validate_acceptance_decision(decision)
    if decision['evidence'] != context['evidence']:
        raise ValueError('Decision must reference exact current required evidence')
    findings, actions, correction = acceptance.evaluate_acceptance(
        ledger.get('outstanding_findings', []), decision, assignment['operation_id'],
        observed['thread_id'], assignment['candidate_sha256'])
    relative = f"decisions/{operation['operation_id']}.json"
    record = {'assignment': assignment, 'observed': observed, 'decision': decision,
              'findings': findings, 'next_actions': actions, 'correction_request': correction}
    storage.publish_or_reuse_bytes(run_dir / relative, storage.canonical_record_bytes(record))
    ledger['outstanding_findings'] = findings
    ledger['evidence']['acceptance'] = {
        'status': 'passed' if decision['action'] == 'accept' else 'failed' if correction else 'not_run' if decision['action'] == 'missing_evidence' else 'blocked',
        'inputs_sha256': assignment['inputs_sha256'], 'candidate_sha256': assignment['candidate_sha256'],
        'operation_id': assignment['operation_id'], 'path': relative,
        'sha256': run_records.sha256_bytes((run_dir / relative).read_bytes())}
    ledger['correction_request'] = correction
    ledger['current_step'] = 'acceptance'
    if decision['action'] == 'blocker':
        ledger.setdefault('interventions', []).append({
            'key': assignment['operation_id'] + ':acceptance', 'blocker': decision['rationale'],
            'evidence': relative, 'operation_id': assignment['operation_id'],
            'required_action': 'Coordinator relay decision blocker and unfinished owner requests in active chat; acknowledgement grants no authority',
            'event': 'opened', 'text': 'Relay and response unknown'})
    return None


def current_acceptance(run_dir, ledger):
    evidence = run_records.evidence_view(ledger, 'acceptance')
    if evidence['status'] in {'missing', 'stale'} or not evidence.get('path'):
        return None
    record = run_records.retained_json(run_dir, evidence['path'], evidence['sha256'])
    operation = run_records.actor_operation(ledger, evidence['operation_id'])
    if not run_records.same_typed_assignment(record['assignment'], operation['assignment']):
        raise ValueError('Acceptance assignment changed')
    # A subsequent evidence operation supersedes the old decision before checking
    # the new evidence against it. It must not lock evidence recovery out.
    if any(item['assignment']['stage'] in {'verify', 'semantic_review', 'acceptance'}
           for item in ledger['actor_operations'][ledger['actor_operations'].index(operation) + 1:]):
        return None
    context = acceptance_context(run_dir, ledger, run_authority.load_frozen_inputs(run_dir, ledger))
    launched = storage.read_json(run_dir / f"acceptance-inputs/{operation['operation_id']}.json")
    if record['decision']['evidence'] != context['evidence'] or launched['known_issue_tracker'] != context['known_issue_tracker']:
        raise ValueError('Acceptance proof is stale')
    return record

