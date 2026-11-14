"""Direct decision contracts; public actor tests own admission and persistence."""
import copy
import importlib.util
from pathlib import Path
import unittest


SPEC = importlib.util.spec_from_file_location(
    'task_orchestrator_acceptance', Path(__file__).parents[1] / 'scripts/acceptance.py')
acceptance = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(acceptance)


def proposal(kind='blocking', **changes):
    """A complete disposition with the decisive flags visible to each case."""
    item = dict(id='F-01', kind=kind, rationale='Observed calculation violates AC',
                evidence=['calculate(2) returns 0'], requirement_violation=kind == 'blocking',
                material_risk=False, correction_authorized=True, trigger='calculate(2)',
                consequence='incorrect result', boundary='product.py', impact='local result',
                likelihood='every invocation', mitigation='bounded task branch',
                compatible_consumers='existing callers', follow_up='owner: diagnostics',
                reassess_when='new evidence or exposure')
    return dict(item, **changes)


def decision(dispositions, action='accept', unfinished=None):
    return dict(action=action, rationale='Current evidence determines this route',
                evidence={'checks/current.json': 'a' * 64}, dispositions=dispositions,
                unfinished=unfinished or [])


def evaluate(findings, claim, operation='acceptance-02'):
    return acceptance.evaluate_acceptance(findings, claim, operation, 'fresh-session', 'b' * 64)


class AcceptanceDecisionTest(unittest.TestCase):
    def test_supported_blocker_proposes_correction_with_provenance_without_mutation(self):
        for flags in ({}, {'requirement_violation': False, 'material_risk': True}):
            with self.subTest(flags=flags):
                findings = [{'id': 'F-01', 'history': [{'collection': 'earlier evidence'}]}]
                claim = decision([proposal(**flags)], action='correct')
                before = copy.deepcopy((findings, claim))
                updated, actions, correction = evaluate(findings, claim)
                self.assertEqual(['reserve:correction'], actions)
                self.assertEqual('review_findings', correction)
                approved = updated[0]['disposition']
                self.assertEqual('approved', approved['status'])
                self.assertEqual('acceptance-02', approved['acceptance_operation_id'])
                self.assertEqual('fresh-session', approved['session_id'])
                self.assertEqual('b' * 64, approved['candidate_sha256'])
                self.assertEqual([{'collection': 'earlier evidence'},
                                  {'acceptance_operation_id': 'acceptance-02',
                                   'disposition': approved}], updated[0]['history'])
                self.assertEqual(before, (findings, claim))

    def test_requirement_and_material_risk_cannot_be_waived_or_labeled_resolved(self):
        cases = [(kind, flag) for kind in ('known_issue', 'observation', 'resolved')
                 for flag in ('requirement_violation', 'material_risk')]
        for kind, flag in cases:
            with self.subTest(kind=kind, flag=flag):
                with self.assertRaisesRegex(ValueError, 'waive|Unresolved'):
                    evaluate([{'id': 'F-01'}], decision([proposal(kind, **{flag: True})]))
        with self.assertRaisesRegex(ValueError, 'Preference alone'):
            evaluate([{'id': 'F-01'}], decision([proposal(requirement_violation=False)], 'correct'))

    def test_exact_finding_coverage_refuses_missing_or_extra_dispositions(self):
        for dispositions in ([], [proposal(), proposal(id='F-02')]):
            with self.subTest(dispositions=dispositions):
                findings = [{'id': 'F-01'}]
                with self.assertRaisesRegex(ValueError, 'Every retained finding'):
                    evaluate(findings, decision(dispositions))
                self.assertEqual([{'id': 'F-01'}], findings)

    def test_approved_disposition_and_history_survive_reapproval_and_reject_reopening(self):
        approved = dict(proposal('known_issue'), status='approved',
                        acceptance_operation_id='acceptance-01', session_id='prior-session',
                        candidate_sha256='c' * 64)
        findings = [{'id': 'F-01', 'disposition': approved,
                     'history': [{'acceptance_operation_id': 'acceptance-01', 'disposition': approved}]}]
        updated, actions, correction = evaluate(findings, decision([proposal('known_issue', rationale='new wording')]))
        self.assertEqual(findings, updated)
        self.assertEqual(['completion_eligible'], actions)
        self.assertIsNone(correction)
        updated[0]['disposition']['evidence'].append('caller mutation')
        self.assertEqual(['calculate(2) returns 0'], approved['evidence'])
        with self.assertRaisesRegex(ValueError, 'cannot reopen'):
            evaluate(findings, decision([proposal()], 'correct'))

    def test_reopened_finding_appends_approval_without_erasing_prior_history(self):
        history = [{'disposition': {'kind': 'known_issue', 'status': 'approved'}}]
        findings = [{'id': 'F-01', 'disposition': {'status': 'reopened', 'reason': 'new exposure'},
                     'history': history}]
        updated, _, _ = evaluate(findings, decision([proposal()], 'correct'))
        self.assertEqual(history, updated[0]['history'][:1])
        self.assertEqual(2, len(updated[0]['history']))
        self.assertEqual('approved', updated[0]['disposition']['status'])
        self.assertEqual('reopened', findings[0]['disposition']['status'])
        self.assertEqual(1, len(history))

    def test_authorized_correction_precedes_missing_proof_and_other_routes(self):
        unfinished = [{'owner': 'verify', 'reason': 'Probe not run', 'evidence': ['AC probe']}]
        findings = [{'id': 'F-01'}]
        claim = decision([proposal()], action='correct', unfinished=unfinished)
        self.assertEqual((['reserve:correction'], 'review_findings'), evaluate(findings, claim)[1:])
        for action in ('accept', 'missing_evidence', 'blocker'):
            with self.subTest(action=action):
                with self.assertRaisesRegex(ValueError, 'takes precedence'):
                    evaluate(findings, dict(claim, action=action))
        with self.assertRaisesRegex(ValueError, 'Supported authorized blocker'):
            evaluate(findings, decision([proposal(correction_authorized=False)], 'correct'))

    def test_missing_proof_routes_to_distinct_owners_and_requires_unfinished_work(self):
        rows = [{'owner': owner, 'reason': 'Missing behavioral probe', 'evidence': ['AC probe']}
                for owner in ('verify', 'semantic_review', 'verify', 'intervene')]
        findings = [{'id': 'F-01'}]
        claim = decision([proposal('missing_evidence')], 'missing_evidence', rows)
        self.assertEqual((['intervene', 'reserve:semantic_review', 'reserve:verify'], None),
                         evaluate(findings, claim)[1:])
        with self.assertRaisesRegex(ValueError, 'Missing proof requires'):
            evaluate(findings, dict(claim, unfinished=[]))

    def test_accept_requires_no_blockers_unresolved_findings_or_unfinished_proof(self):
        for kind in ('blocking', 'missing_evidence', 'blocker'):
            with self.subTest(kind=kind):
                with self.assertRaisesRegex(ValueError, 'cannot erase'):
                    evaluate([{'id': 'F-01'}], decision([proposal(kind, correction_authorized=False)]))
        for kind in ('known_issue', 'observation', 'resolved'):
            with self.subTest(kind=kind):
                self.assertEqual((['completion_eligible'], None),
                                 evaluate([{'id': 'F-01'}], decision([proposal(kind)]))[1:])
        unfinished = [{'owner': 'verify', 'reason': 'Not run', 'evidence': ['AC probe']}]
        with self.assertRaisesRegex(ValueError, 'cannot erase'):
            evaluate([], decision([], unfinished=unfinished))
        self.assertEqual((['completion_eligible'], None), evaluate([], decision([]))[1:])
        self.assertEqual((['intervene'], None), evaluate([], decision([], 'blocker', unfinished))[1:])


if __name__ == '__main__':
    unittest.main()
