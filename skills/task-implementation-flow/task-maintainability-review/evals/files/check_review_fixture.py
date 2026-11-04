"""Exercise supplied states/tools; no agent review or acceptance is simulated."""

import json
import os
import shlex
import shutil
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import review_fixture as fixture


class ReviewFixtureTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='T-004-check-')
        self.addCleanup(self.temporary.cleanup)
        self.work = Path(self.temporary.name)

    def prepare(self, case_id):
        work = self.work / case_id
        env = dict(os.environ, EVAL_WORK_ROOT=str(work), PYTHONDONTWRITEBYTECODE='1')
        result = subprocess.run([sys.executable, str(fixture.HERE / 'setup_fixture.py'),
                                 'review:' + case_id], env=env, text=True, capture_output=True)
        self.assertEqual(0, result.returncode, result.stderr)
        root = Path((work / 'workspace.txt').read_text())
        oracle = json.loads((work / 'task-runs/oracle.json').read_text())
        self.assertEqual(fixture.snapshot(root), oracle['snapshot'])
        self.assertFalse((root / 'oracle.json').exists())
        return root, oracle

    def compare(self, root, name='R-local.json', expected=0):
        result = subprocess.run([str(fixture.PYTHON), str(root / '.agents/scripts/measure_maintainability.py'),
                                 'compare', 'src', '--root', str(root), '--baseline', fixture.BASE,
                                 '--output', '.quality/reports/' + name], text=True, capture_output=True)
        self.assertEqual(expected, result.returncode, result.stdout + result.stderr)
        return result

    def test_every_finite_setup_supplies_real_inputs_and_preserves_history(self):
        case_ids = [row['id'] for row in fixture.CASES]
        self.assertEqual(len(case_ids), len(set(case_ids)), 'dispatch IDs must be unique')
        ids = {row['scenario'] for row in fixture.CASES}
        self.assertEqual(62, len(ids))
        for case in fixture.CASES:
            with self.subTest(case=case['id']):
                root, oracle = self.prepare(case['id'])
                request = (root / 'review-request.md').read_text()
                self.assertIn(str(fixture.PYTHON), request)
                self.assertIn('No source/index/old-report edits', request)
                self.assertEqual(case, {key: oracle[key] for key in case})
                if case['scenario'] in ('V-02e', 'V-02f'):
                    self.assertFalse((root / '.agents/scripts/measure_maintainability.py').exists())
                elif case['scenario'] == 'V-02a':
                    self.assertFalse((root / fixture.BASE).exists())
                elif case['scenario'] == 'V-02c':
                    self.compare(root, expected=2)
                elif case['scenario'] == 'V-02d':
                    target = '.quality/reports/I1.json' if case['variant'] == 'current' else fixture.BASE
                    data = json.loads((root / target).read_text())
                    self.assertTrue(data['measurement_status'] != 'complete' or not data['full_profile'])
                elif case['scenario'] == 'V-02h':
                    self.assertEqual(case['variant'] == 'json', (root / '.quality/reports/current.json').exists())
                    self.assertEqual(case['variant'] == 'text', (root / '.quality/reports/current.txt').exists())
                elif case['scenario'].startswith('V-10'):
                    self.assertTrue((root / 'discovery-request.md').is_file())
                    self.assertTrue((root / 'acceptance-request.md').is_file())
                    self.assertTrue((root / 'docs/tasks/REVIEW/reviews/maintainability-01.md').is_file())
                for name, digest in oracle['snapshot'].items():
                    self.assertEqual(digest, fixture.snapshot(root)[name])

    def test_tests_only_authorship_keeps_production_control_distinct(self):
        for case, expected in (('V-01c', ['src/logic.py']), ('V-01d', ['tests/sample.py'])):
            with self.subTest(case=case):
                root, _ = self.prepare(case)
                paths = subprocess.check_output(['git', 'diff', '--name-only', 'HEAD', '--',
                                                 *fixture.SCOPES], cwd=root, text=True).splitlines()
                self.assertEqual(expected, paths)
                baseline = json.loads((root / fixture.BASE).read_text())
                current = json.loads((root / '.quality/reports/I1.json').read_text())
                self.assertEqual('complete', current['measurement_status'])
                if case == 'V-01d':
                    self.assertEqual(baseline['files']['src/logic.py']['sha256'],
                                     current['files']['src/logic.py']['sha256'])
                    self.assertNotEqual(baseline['files']['tests/sample.py']['sha256'],
                                        current['files']['tests/sample.py']['sha256'])

    def test_partial_faults_leave_other_evidence_valid(self):
        for variant in ('baseline', 'current', 'profile'):
            with self.subTest(variant=variant):
                root, _ = self.prepare('V-02d-' + variant)
                base = json.loads((root / fixture.BASE).read_text())
                current = json.loads((root / '.quality/reports/I1.json').read_text())
                self.assertEqual('incomplete' if variant == 'baseline' else 'complete', base['measurement_status'])
                self.assertEqual('incomplete' if variant == 'current' else 'complete', current['measurement_status'])
                self.assertEqual(variant != 'profile', base['full_profile'])
                self.assertTrue(current['full_profile'])
                for report in (base, current):
                    self.assertEqual(['complexity', 'ruff'], report['identity']['checks'])
                    self.assertEqual('completed', report['checks']['complexity']['status'])
                self.assertEqual('failed' if variant == 'baseline' else 'completed', base['checks']['ruff']['status'])
                self.assertEqual('completed', current['checks']['ruff']['status'])

    def test_isolated_receiver_has_submission_and_authorized_report_transfer(self):
        root, oracle = self.prepare('V-01e')
        receiver = self.work / 'V-01e/receiver'
        self.assertEqual(subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root),
                         subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=receiver))
        names = subprocess.check_output(['git', 'ls-files', '--cached', '--others',
                                         '--exclude-standard'], cwd=root, text=True).splitlines()
        for name in names:
            with self.subTest(path=name):
                if (root / name).is_file():
                    self.assertTrue((receiver / name).is_file(), name)
                    self.assertEqual((root / name).read_bytes(), (receiver / name).read_bytes())
                else:
                    self.assertFalse((receiver / name).exists())
        self.assertTrue((receiver / 'src/added.py').is_file())
        self.assertFalse((receiver / 'src/deleted.py').exists())
        self.assertNotEqual(subprocess.check_output(['git', 'show', 'HEAD:harness/sample.py'], cwd=receiver),
                            (receiver / 'harness/sample.py').read_bytes())
        self.assertTrue((receiver / '.agents/scripts/measure_maintainability.py').is_file())
        request = (receiver / 'review-request.md').read_text()
        self.assertIn(f'Reviewer workspace: {receiver}', request)
        self.assertIn('Setup has transferred submitted source and task inputs', request)
        self.assertFalse((receiver / '.quality/reports/B.json').exists())
        transfers = (receiver / 'transfer-paths.txt').read_text().splitlines()
        self.assertEqual(4, len(transfers))
        for line, name in zip(transfers, ('B.json', 'B.txt', 'I1.json', 'I1.txt')):
            source, target = line.split(' -> ')
            self.assertEqual(str(root / '.quality/reports' / name), source)
            self.assertEqual(str(receiver / '.quality/reports' / name), target)
            Path(target).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
        self.compare(receiver)
        current = json.loads((receiver / '.quality/reports/R-local.json').read_text())
        self.assertEqual('complete', current['measurement_status'])
        self.assertEqual(fixture.snapshot(root)['src/logic.py'], current['files']['src/logic.py']['sha256'])
        self.assertEqual(oracle['snapshot'], fixture.snapshot(root))

    def test_native_policy_conflict_binds_real_command_scope_and_owner(self):
        root, _ = self.prepare('V-06i')
        command = f'{shlex.quote(str(fixture.PYTHON))} tools/native.py'
        self.assertTrue((root / 'tools/native.py').is_file())
        native = (root / 'docs/native.md').read_text()
        first = (root / 'docs/policy-a.md').read_text()
        second = (root / 'docs/policy-b.md').read_text()
        for policy in (native, first, second):
            self.assertIn(command, policy)
            self.assertIn('src and outside', policy)
            self.assertIn('implementer', policy)
        self.assertIn('required and hard', first)
        self.assertIn('optional and advisory', second)
        self.assertIn('task authority', second)
        self.assertIn('No precedence declared', second)
        self.assertTrue((root / 'tools/native.py').is_file())
        result = subprocess.run([str(fixture.PYTHON), 'tools/native.py'], cwd=root, capture_output=True)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        history = json.loads((root / '.quality/reports/native-history.jsonl').read_text().splitlines()[-1])
        self.assertEqual(['src', 'outside'], history['scope'])
        self.assertIn('outside/control.py', history['checked_bytes'])
        self.assertTrue(history['required'])
        self.assertEqual('docs/native.md', history['policy'])
        self.assertEqual(0, history['exit_code'])

    def test_independent_current_compare_rejects_stale_author_identity_and_keeps_index(self):
        root, oracle = self.prepare('V-01b')
        author = json.loads((root / '.quality/reports/I1.json').read_text())
        self.assertNotEqual(author['files']['src/logic.py']['sha256'], fixture.snapshot(root)['src/logic.py'])
        self.compare(root)
        current = json.loads((root / '.quality/reports/R-local.json').read_text())
        self.assertEqual('complete', current['measurement_status'])
        self.assertEqual(fixture.snapshot(root)['src/logic.py'], current['files']['src/logic.py']['sha256'])
        for name, digest in oracle['snapshot'].items():
            self.assertEqual(digest, fixture.snapshot(root)[name])

    def test_real_native_failure_and_recovery_keep_whole_scope_history(self):
        root, _ = self.prepare('V-06b-complete')
        report = json.loads((root / '.quality/reports/I1.json').read_text())
        self.assertEqual('complete', report['measurement_status'])
        path = root / '.quality/reports/native-history.jsonl'
        history = [json.loads(line) for line in path.read_text().splitlines()]
        self.assertEqual([0, 1], [row['exit_code'] for row in history])
        self.assertIn('outside/control.py', history[-1]['checked_bytes'])
        (root / 'outside/control.py').write_text('VALUE = 1\n')
        result = subprocess.run([str(fixture.PYTHON), 'tools/native.py'], cwd=root, capture_output=True)
        self.assertEqual(0, result.returncode, result.stderr)
        updated = [json.loads(line) for line in path.read_text().splitlines()]
        self.assertEqual(history, updated[:2])
        self.assertEqual(0, updated[-1]['exit_code'])
        self.assertNotEqual(updated[-1]['checked_bytes'], history[-1]['checked_bytes'])

    def test_two_real_comparisons_bind_to_original_and_complete_obligations_exist(self):
        root, oracle = self.prepare('V-08b')
        first = json.loads((root / '.quality/reports/R1-control.json').read_text())
        second = json.loads((root / '.quality/reports/R2-control.json').read_text())
        self.assertEqual(first['baseline_path'], second['baseline_path'])
        self.assertNotEqual(first['files']['src/billing/pricing.py']['sha256'], second['files']['src/billing/pricing.py']['sha256'])
        self.assertTrue((root / 'docs/tasks/MNT-42/reviews/maintainability-01.md').exists())
        self.assertEqual('corrected in supplied correction', json.loads((root / 'finding-ledger.json').read_text())['MNT-B2'])
        root, _ = self.prepare('V-07a')
        rationale = json.loads((root / 'rationale.json').read_text())
        self.assertEqual(4, len(rationale['obligations']))
        self.assertGreater(len(rationale['optional_warning_candidates']), 3)
        report = json.loads((root / '.quality/reports/obligations.json').read_text())
        values = {row['symbol']: row['value'] for row in report['checks']['complexity']['values']}
        for row in rationale['obligations']:
            self.assertEqual(11, values[row['function']])
        self.assertEqual('measurement owner', rationale['gap']['owner'])


    def test_controlled_candidate_claims_fail_their_artifact_oracle(self):
        root, _ = self.prepare('V-07a')
        required = {row['id'] for row in json.loads((root / 'rationale.json').read_text())['obligations']}
        root, _ = self.prepare('V-01b')
        actual = fixture.snapshot(root)['src/logic.py']
        stale = json.loads((root / '.quality/reports/I1.json').read_text())['files']['src/logic.py']['sha256']
        expected_route = ['registry synchronization', 'fresh discovery', 'separate acceptance']
        control = dict(dispositions=sorted(required), current_hash=actual, route=expected_route)
        candidates = [dict(control, dispositions=sorted(required)[1:]),
                      dict(control, current_hash=stale),
                      dict(control, route=['separate acceptance'])]
        def gaps(candidate):
            return [name for name, valid in (
                ('disposition ledger', set(candidate['dispositions']) == required),
                ('current bytes', candidate['current_hash'] == actual),
                ('ordered route', candidate['route'] == expected_route)) if not valid]
        self.assertEqual([], gaps(control))
        observations = []
        for candidate, reason in zip(candidates, ('disposition ledger', 'current bytes', 'ordered route')):
            self.assertEqual([reason], gaps(candidate))
            observations.append(dict(candidate=candidate, rejected_for=gaps(candidate)))
        # Preserve the concrete negative claims and independent input references
        # for local inspection while the test workspace exists.
        fixture.write(self.work, 'negative-grading-controls.json', json.dumps(dict(
            origin='local synthetic candidate claims, no agent run',
            control=control, actual_required=sorted(required), observations=observations), indent=2))


if __name__ == '__main__':
    unittest.main()
