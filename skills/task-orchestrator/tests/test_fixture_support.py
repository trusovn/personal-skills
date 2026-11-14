"""Behavioral ownership/isolation evidence for shared disposable test setup."""
import json
import unittest
from unittest import mock

from actor_fixture_support import ActorFixture
from controller_fixture_support import ControllerFixture


class FixtureOwnershipTest(unittest.TestCase):
    def test_occurrences_keep_repository_run_and_actor_configuration_independent(self):
        cleanups = []
        def own_cleanup(cleanup):
            self.addCleanup(cleanup)
            cleanups.append(cleanup)

        first = ActorFixture()
        first.initialize_fixture(own_cleanup)
        second = ActorFixture()
        second.initialize_fixture(self.addCleanup)
        _, first_run = first.create_initialized_run()
        _, second_run = second.create_initialized_run()
        first_actor = first.actor({'before_session': True})
        second_actor = second.actor({'after_session': True})
        second_ledger = (second_run / 'ledger.json').read_bytes()
        second_mode = (second_actor.parent / 'mode.json').read_bytes()

        (first.repo / 'allowed.txt').write_text('first occurrence only\n')
        self.assertEqual("reserved", first.reserve(first_run)["status"])
        first.actor({'hold': True})
        first_policy = first.policy()
        first_policy['verification']['targeted_checks'].append('first-only')

        self.assertNotEqual(first.root, second.root)
        self.assertEqual('baseline\n', (second.repo / 'allowed.txt').read_text())
        self.assertEqual(second_ledger, (second_run / 'ledger.json').read_bytes())
        self.assertEqual(second_mode, (second_actor.parent / 'mode.json').read_bytes())
        self.assertEqual({'hold': True}, json.loads((first_actor.parent / 'mode.json').read_text()))
        self.assertNotIn('first-only', second.policy()['verification']['targeted_checks'])
        self.assertNotIn('first-only', first.policy()['verification']['targeted_checks'])

        cleanups[0]()
        self.assertFalse(first.root.exists())
        self.assertTrue(second.repo.exists())
        self.assertTrue(second_run.exists())
        self.assertTrue(second_actor.exists())

    def test_unittest_cleanup_releases_occurrence_after_setup_or_assertion_failure(self):
        for boundary in ('setup', 'assertion'):
            with self.subTest(boundary=boundary):
                fixture = ControllerFixture()

                class FailingOccurrence(unittest.TestCase):
                    def setUp(self):
                        fixture.initialize_fixture(self.addCleanup)

                    def runTest(self):
                        self.fail('intentional scenario failure')

                result = unittest.TestResult()
                case = FailingOccurrence()
                if boundary == 'setup':
                    with mock.patch('controller_fixture_support.subprocess.run',
                                    side_effect=OSError('intentional git setup failure')):
                        case.run(result)
                    self.assertEqual(1, len(result.errors))
                    self.assertIn('intentional git setup failure', result.errors[0][1])
                else:
                    case.run(result)
                    self.assertEqual(1, len(result.failures))
                    self.assertIn('intentional scenario failure', result.failures[0][1])
                self.assertFalse(fixture.root.exists())
