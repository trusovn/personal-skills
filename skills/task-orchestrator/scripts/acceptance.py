"""Acceptance disposition/history and routing policy over validated JSON facts.

``evaluate_acceptance`` returns proposed finding updates, next actions and a
correction reason without mutating its inputs. The controller owns validation,
current evidence/identity, locks, publication and ledger mutation. This module
uses only the standard library and performs no I/O. Admission stays with the
application.
"""

import json


def evaluate_acceptance(current_findings, decision, operation_id, session_id, candidate_sha256):
    """Evaluate a schema-validated decision and retained findings.

    Identity values must already be admitted by the application. The returned
    findings preserve approved history; callers alone may publish these updates.
    Correction-budget and recovery eligibility remain application policy.
    """
    findings = _acceptance_dispositions(
        current_findings, decision, operation_id, session_id, candidate_sha256)
    actions, correction = _acceptance_route(decision, findings)
    return findings, actions, correction


def _disposition_for_finding(finding, proposal, operation_id, session_id, candidate_sha256):
    if proposal['kind'] == 'known_issue' and (proposal['requirement_violation'] or proposal['material_risk']):
        raise ValueError('Deferral cannot waive a requirement or material risk')
    if proposal['kind'] == 'blocking' and not (proposal['requirement_violation'] or proposal['material_risk']):
        raise ValueError('Preference alone cannot authorize correction')
    if proposal['kind'] in {'observation', 'resolved'} and (proposal['requirement_violation'] or proposal['material_risk']):
        raise ValueError('Unresolved violation/material risk cannot become an observation or resolution')
    previous = finding.get('disposition')
    if previous and previous['status'] == 'approved':
        if previous['kind'] != proposal['kind']:
            raise ValueError('Unchanged approved disposition cannot reopen without new evidence/exposure')
        return previous
    return {**proposal, 'status': 'approved', 'acceptance_operation_id': operation_id,
            'session_id': session_id, 'candidate_sha256': candidate_sha256}


def _acceptance_dispositions(current_findings, decision, operation_id, session_id, candidate_sha256):
    findings = json.loads(json.dumps(current_findings))
    proposals = {item['id']: item for item in decision['dispositions']}
    if set(proposals) != {finding['id'] for finding in findings}:
        raise ValueError('Every retained finding must have exactly one disposition')
    for finding in findings:
        proposal = proposals[finding['id']]
        disposition = _disposition_for_finding(finding, proposal, operation_id, session_id, candidate_sha256)
        if disposition != finding.get('disposition'):
            finding.setdefault('history', []).append({'acceptance_operation_id': operation_id,
                                                      'disposition': disposition})
        finding['disposition'] = disposition
    return findings


def _acceptance_route(decision, findings):
    blockers = [item['disposition'] for item in findings if item['disposition']['kind'] == 'blocking']
    unresolved = any(item['disposition']['kind'] in {'missing_evidence', 'blocker'} for item in findings)
    action = decision['action']
    if action == 'correct':
        if not any(item['correction_authorized'] for item in blockers):
            raise ValueError('Supported authorized blocker required for review_findings')
        return ['reserve:correction'], 'review_findings'
    if any(item['correction_authorized'] for item in blockers):
        raise ValueError('Authorized blocking correction takes precedence')
    if action == 'accept':
        if blockers or unresolved or decision['unfinished']:
            raise ValueError('Accept cannot erase outstanding findings or required evidence')
        return ['completion_eligible'], None
    if action == 'missing_evidence':
        if not decision['unfinished']:
            raise ValueError('Missing proof requires its reason and evidence owner')
        return sorted({('reserve:' + row['owner']) if row['owner'] != 'intervene' else 'intervene'
                       for row in decision['unfinished']}), None
    return ['intervene'], None


