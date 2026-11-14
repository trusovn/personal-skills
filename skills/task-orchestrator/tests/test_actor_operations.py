"""T-003 public boundary proof with local actors; no sbx/provider qualification."""
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
import unittest
from unittest import mock

from jsonschema import Draft202012Validator, ValidationError

import controller_fixture_support as fixtures
from actor_fixture_support import ActorFixture

load_controller = fixtures.load_controller
flow_profile = fixtures.flow_profile


class RecoveryDecisionTest(unittest.TestCase):
    def test_correction_ownership_and_budget_precede_evidence_recovery(self):
        controller = load_controller()
        identity = {key: 'a' * 64 for key in ('inputs_sha256', 'policy_sha256', 'flow_sha256')}
        assignment = dict(identity, stage='preflight', role='preflight', task_id='T1', can_repair=False)
        ready = dict(identity, status='ready', operation_id='preflight', task_id='T1')
        current = {'correction_request': 'review_findings'}
        cases = [
            ('review-current', 'review_findings', 0, True, None, set(), current,
             ['reserve:correction'], None),
            ('review-stale', 'review_findings', 0, True, None, {'verify'}, None,
             ['intervene'], 'correction_authority_stale'),
            ('review-missing', 'review_findings', 0, True, None, set(), None,
             ['intervene'], 'correction_authority_stale'),
            ('review-needs-preflight', 'review_findings', 0, False, None, set(), current,
             ['reserve:preflight'], 'current_preflight_readiness_required'),
            ('check-correction', 'check_failed', 0, True, None, {'verify'}, None,
             ['reserve:correction'], None),
            ('repair-correction', 'environment_repair', 0, False, None, {'candidate'}, None,
             ['reserve:correction'], None),
            ('budget-exhausted', 'review_findings', 3, True, None, {'semantic_review'}, None,
             ['intervene'], 'corrections_exhausted'),
            ('active-owner', 'review_findings', 3, True, 'implement', {'verify'}, None,
             ['launch_operation', 'stop_operation', 'intervene'], 'operation_reserved'),
            ('active-verifier', 'review_findings', 3, True, 'verify', {'verify'}, None,
             ['check_candidate', 'intervene'], 'check_operation_reserved'),
        ]
        for name, correction, count, readiness, active_stage, stale, decision, actions, blocker in cases:
            with self.subTest(case=name):
                operations = [{'operation_id': 'preflight', 'state': 'terminal', 'assignment': assignment}]
                if active_stage:
                    operations.append({'state': 'reserved', 'assignment': {'stage': active_stage}})
                ledger = dict(identity, state='ready', correction_request=correction,
                              correction_cycle=count, selected_task_id='T1',
                              readiness=ready if readiness else None, actor_operations=operations)
                before = json.dumps(ledger, sort_keys=True)
                self.assertEqual((actions, blocker), controller.operation_scheduling._reservation_options(
                    ledger, stale=stale, decision=decision))
                self.assertEqual(before, json.dumps(ledger, sort_keys=True))


class ActorOperationsTest(ActorFixture, unittest.TestCase):
    def setUp(self):
        self.initialize_fixture(self.addCleanup)


    def launch(self, controller, run_dir, reservation, fake, timeout=5):
        result = controller.launch_operation(run_dir, reservation['assignment'], codex_bin=str(fake), timeout_seconds=timeout)
        self.assertEqual('launched', result['status'], result)
        return result

    def terminal(self, controller, run_dir, operation_id):
        deadline = time.monotonic()+8
        while time.monotonic() < deadline:
            result = controller.observe_operation(run_dir, operation_id)
            if result['status'] in {'terminal','replayed'}:
                return result
            if result['status'] == 'refused' and 'owns this run' in result.get('detail',''):
                time.sleep(0.02)
                continue
            self.assertNotEqual('refused', result['status'], result)
            time.sleep(0.02)
        self.fail(f'No terminal outcome: {result}')

    def wait_file(self, path):
        deadline = time.monotonic()+5
        while time.monotonic()<deadline:
            if path.exists(): return
            time.sleep(0.01)
        self.fail(f'Missing synchronization file {path}')

    def invocations(self, fake):
        path = fake.parent/'invocations.jsonl'
        return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []

    def preflight(self, controller, run_dir, fake, key='preflight'):
        r = self.reserve(run_dir, key=key)
        self.assertEqual('reserved',r['status'],r)
        self.launch(controller, run_dir, r, fake)
        outcome = self.terminal(controller, run_dir, r['assignment']['operation_id'])
        self.assertIsNone(outcome.get('blocker'),outcome)
        self.assertTrue(controller.status_run(run_dir)['readiness_current'])
        return r

    def test_v01_v06_frozen_models_readiness_and_first_implementation(self):
        for level, effort in [('light','low'),('standard','medium'),('strong','high')]:
            with self.subTest(level=level):
                flow=flow_profile()
                for step in flow['steps']:
                    if step['role'] in {'preflight','implementer'}: step['mode']=level
                controller, run_dir=self.create_initialized_run(flow=flow,name=level)
                fake=self.actor()
                (self.repo/'tasks/T1.md').write_text('mutable replacement')
                self.preflight(controller,run_dir,fake)
                first=self.reserve(run_dir,'implement','first-implementation')
                self.launch(controller,run_dir,first,fake)
                self.terminal(controller,run_dir,first['assignment']['operation_id'])
                records=self.invocations(fake)[-2:]
                for record in records:
                    self.assertIn('gpt-6.1-sol',record['argv'])
                    self.assertIn('model_reasoning_effort="'+effort+'"',record['argv'])
                    self.assertIn('danger-full-access',record['argv'])
                    self.assertEqual('# T1\n',record['prompt']['frozen_inputs']['documents']['brief']['content'])
                status=load_controller().status_run(run_dir)
                self.assertEqual(0,status['correction_count'])
                self.assertEqual('local implementation marker\n',(self.repo/'allowed.txt').read_text())
                self.assertNotEqual('completed',status['state'])
                self.assertEqual('missing',status['evidence']['implement']['status'])
                self.assertEqual('refused',self.reserve(run_dir,'implement','second-free')['status'])

    def test_v02_invalid_assignment_guards_do_not_launch_or_mutate(self):
        controller,run_dir=self.create_initialized_run()
        fake=self.actor()
        reservation=self.reserve(run_dir)
        before=(run_dir/'ledger.json').read_bytes()
        cases = [(field, 'wrong') for field in ('task_id','role','inputs_sha256','policy_sha256','flow_sha256')]
        cases += [('flow_revision', True), ('flow_revision', 1.0),
                  ('correction_count', False), ('correction_count', 0.0),
                  ('can_change_files', 0), ('can_repair', 0)]
        for field, value in cases:
            with self.subTest(field=field, value=value):
                bad=dict(reservation['assignment']);bad[field]=value
                result=controller.launch_operation(run_dir,bad,codex_bin=str(fake))
                self.assertEqual('refused',result['status'],result)
                self.assertEqual(before,(run_dir/'ledger.json').read_bytes())
        self.assertEqual([],self.invocations(fake))
        self.launch(controller,run_dir,reservation,fake)
        self.terminal(controller,run_dir,reservation['assignment']['operation_id'])

    def test_v04_replay_retains_outcome_and_configuration(self):
        controller,run_dir=self.create_initialized_run(); fake=self.actor()
        reservation=self.reserve(run_dir)
        self.launch(controller,run_dir,reservation,fake)
        self.assertEqual('replayed',load_controller().launch_operation(run_dir,reservation['assignment'],codex_bin=str(fake),timeout_seconds=5)['status'])
        self.terminal(controller,run_dir,reservation['assignment']['operation_id'])
        before=(run_dir/'ledger.json').read_bytes()
        self.assertEqual('replayed',controller.observe_operation(run_dir,reservation['assignment']['operation_id'])['status'])
        self.assertEqual('refused',controller.launch_operation(run_dir,reservation['assignment'],codex_bin='/other',timeout_seconds=5)['status'])
        self.assertEqual(before,(run_dir/'ledger.json').read_bytes())
        self.assertEqual(1,len(self.invocations(fake)))

    def test_v05_v07_invalid_results_retain_raw_evidence_without_readiness(self):
        cases=[{'missing':True},{'malformed':True},{'session':True},{'incomplete':True},
               {'before_session':True},{'after_session':True}]
        cases += [{'field':field} for field in ('role','task_id','operation_id','inputs_sha256','policy_sha256','flow_sha256','candidate_sha256')]
        cases += [{'field':field, 'value':value} for field,value in (
            ('flow_revision', True), ('flow_revision', 1.0),
            ('correction_count', False), ('correction_count', 0.0),
            ('can_change_files', 0), ('can_repair', 0))]
        for index,mode in enumerate(cases):
            with self.subTest(mode=mode):
                controller,run_dir=self.create_initialized_run(name=f'invalid-{index}'); fake=self.actor(mode)
                r=self.reserve(run_dir);self.launch(controller,run_dir,r,fake)
                outcome=self.terminal(controller,run_dir,r['assignment']['operation_id'])
                self.assertIsNotNone(outcome['blocker'],outcome)
                status=controller.status_run(run_dir)
                self.assertFalse(status['readiness_current'])
                self.assertEqual('refused',self.reserve(run_dir,'implement','invalid-implementation')['status'])
                directory=run_dir/'actors'/r['assignment']['operation_id']
                for name in ('launch.json','prompt.txt','events.jsonl','stderr.log','result.state.json'):
                    self.assertTrue((directory/name).exists(),name)
                observed=outcome['operation']['transport']['outcome']['observed']
                self.assertEqual('gpt-6.1-sol',observed['configured_model'])
                self.assertIsNone(observed['observed_model'])
                self.assertEqual(not mode.get('before_session',False),bool(observed['thread_id']))

    def test_f01_malformed_observation_binding_cannot_admit_readiness(self):
        controller,run_dir=self.create_initialized_run()
        fake=self.actor()
        reservation=self.reserve(run_dir)
        self.launch(controller,run_dir,reservation,fake)
        operation_id=reservation['assignment']['operation_id']
        receipt=run_dir/'actors'/operation_id/'result.state.json'
        self.wait_file(receipt)
        original=receipt.read_bytes()
        before=(run_dir/'ledger.json').read_bytes()
        for field,value in (('flow_revision', True), ('flow_revision', 1.0),
                            ('correction_count', False), ('correction_count', 0.0),
                            ('can_change_files', 0), ('can_repair', 0)):
            with self.subTest(field=field,value=value):
                observed=json.loads(original)
                observed['assignment'][field]=value
                malformed=json.dumps(observed).encode()
                receipt.write_bytes(malformed)
                outcome=controller.observe_operation(run_dir,operation_id)
                self.assertEqual('refused',outcome['status'],outcome)
                self.assertEqual(before,(run_dir/'ledger.json').read_bytes())
                self.assertEqual(malformed,receipt.read_bytes())
                self.assertFalse(controller.status_run(run_dir)['readiness_current'])
                self.assertEqual('refused',self.reserve(run_dir,'implement','invalid-observation')['status'])
        receipt.write_bytes(original)
        self.assertIsNone(self.terminal(controller,run_dir,operation_id)['blocker'])
        self.assertTrue(controller.status_run(run_dir)['readiness_current'])
        self.assertEqual(1,len(self.invocations(fake)))

    def test_v07_missing_each_prerequisite_reaches_specific_blocker(self):
        for index,missing in enumerate(('tool','dependency.py','skill')):
            with self.subTest(missing=missing):
                controller,run_dir=self.create_initialized_run(name=f'missing-{index}');fake=self.actor()
                path=self.repo/'.agents/skills/required/SKILL.md' if missing=='skill' else fake.parent/missing
                path.unlink()
                r=self.reserve(run_dir); self.launch(controller,run_dir,r,fake)
                outcome=self.terminal(controller,run_dir,r['assignment']['operation_id'])
                self.assertIsNotNone(outcome['blocker'])
                self.assertIn('Missing',outcome['blocker'])
                self.assertFalse(controller.status_run(run_dir)['readiness_current'])
                self.assertEqual(0,controller.status_run(run_dir)['correction_count'])
                self.assertEqual('refused',self.reserve(run_dir,'implement','denied')['status'])
                self.assertEqual(index+1,len(self.invocations(fake)))

    def test_v05g_v10_nonterminal_result_cannot_admit_and_stop_is_observed(self):
        controller,run_dir=self.create_initialized_run();fake=self.actor({'wait':True,'child':True})
        r=self.reserve(run_dir);self.launch(controller,run_dir,r,fake)
        self.wait_file(fake.parent/'waiting')
        operation_id=r['assignment']['operation_id']
        self.assertEqual('running',controller.observe_operation(run_dir,operation_id)['status'])
        self.assertFalse(controller.status_run(run_dir)['readiness_current'])
        self.assertEqual('refused',self.reserve(run_dir,key='duplicate')['status'])
        controller.stop_operation(run_dir,operation_id)
        outcome=self.terminal(controller,run_dir,operation_id)
        self.assertIsNotNone(outcome['blocker'])
        observed=outcome['operation']['transport']['outcome']['observed']
        self.assertTrue(observed['stop_requested'])
        self.assertTrue(observed['terminal_observed'])
        self.assertTrue(observed['group_absent'])
        self.assertEqual('absent',controller._worker_module.process_liveness(observed['observed_process_pid']))
        before=(run_dir/'ledger.json').read_bytes()
        self.assertEqual('replayed',controller.stop_operation(run_dir,operation_id)['status'])
        self.assertEqual(before,(run_dir/'ledger.json').read_bytes())

    def test_v10_timeout_is_failure_and_before_launch_stop_is_terminal(self):
        controller,run_dir=self.create_initialized_run();fake=self.actor({'wait':True})
        r=self.reserve(run_dir);self.launch(controller,run_dir,r,fake,timeout=0.3)
        outcome=self.terminal(controller,run_dir,r['assignment']['operation_id'])
        self.assertIsNotNone(outcome['blocker'])
        self.assertEqual('timed_out',outcome['operation']['transport']['outcome']['observed']['attempt_outcome'])
        r=self.reserve(run_dir,key='cancelled')
        self.assertEqual('terminal',controller.stop_operation(run_dir,r['assignment']['operation_id'])['status'])
        self.assertEqual('replayed',controller.observe_operation(run_dir,r['assignment']['operation_id'])['status'])
        self.assertEqual('refused',controller.launch_operation(run_dir,r['assignment'],codex_bin=str(fake))['status'])
        self.assertEqual(1,len(self.invocations(fake)))

    def test_v12_intervention_history_does_not_authorize_work(self):
        controller,run_dir=self.create_initialized_run();self.reserve(run_dir)
        request=dict(key='owner-1',blocker='unknown actor',evidence='actors/operation-001',operation_id='operation-001',required_action='owner resolve process identity',event='opened',text='')
        self.assertEqual('recorded',controller.record_intervention(run_dir,request)['status'])
        status=load_controller().status_run(run_dir)
        self.assertEqual(['opened'],[r['event'] for r in status['interventions']])
        self.assertEqual('opened',status['interventions'][0]['event'])
        self.assertEqual('refused',self.reserve(run_dir,key='pending')['status'])
        for event,text in [('relayed','fixture chat relay'),('response','acknowledged')]:
            self.assertEqual('recorded',controller.record_intervention(run_dir,{**request,'event':event,'text':text})['status'])
        status=controller.status_run(run_dir)
        self.assertEqual(3,len(status['interventions']))
        self.assertEqual('refused',self.reserve(run_dir,'correction','ack-repair','environment_repair')['status'])
        self.assertEqual('refused',self.reserve(run_dir,key='ack-retry')['status'])
        self.assertEqual(0,status['correction_count'])
        revision=self.revision_request(run_dir)
        revision['authorization']['decision']='acknowledged'
        self.assertEqual('refused',controller.revise_inputs(run_dir,revision)['status'])
        self.assertNotEqual('completed',controller.status_run(run_dir)['state'])

    def test_v14_public_cli_launch_and_observe(self):
        controller,run_dir=self.create_initialized_run();fake=self.actor()
        r=self.reserve(run_dir)
        request=self.root/'cli-assignment.json';request.write_text(json.dumps(r['assignment']))
        result=subprocess.run([sys.executable,str(fixtures.CONTROLLER_PATH),'launch','--run-dir',str(run_dir),'--request',str(request),'--codex-bin',str(fake),'--timeout-seconds','5'],capture_output=True,text=True)
        self.assertEqual(0,result.returncode,result.stderr)
        self.assertEqual('launched',json.loads(result.stdout)['status'])
        self.terminal(controller,run_dir,r['assignment']['operation_id'])
        observed=subprocess.run([sys.executable,str(fixtures.CONTROLLER_PATH),'observe','--run-dir',str(run_dir),'--operation-id',r['assignment']['operation_id']],capture_output=True,text=True)
        self.assertEqual(0,observed.returncode,observed.stderr)
        self.assertEqual('replayed',json.loads(observed.stdout)['status'])
        self.assertTrue(controller.status_run(run_dir)['readiness_current'])
        self.assertEqual(1,len(self.invocations(fake)))

    def test_v02_authorization_and_old_policy_are_refused_at_launch(self):
        for index,change in enumerate(({'execution_authorization':None},{'execution_authorization':{'transport':'sbx','yolo':False,'intervention':'active_chat'}},{'version':1})):
            controller,run_dir=self.create_initialized_run(name=f'policy-{index}');fake=self.actor()
            r=self.reserve(run_dir)
            # Deliberately incompatible persisted fixture, not a revision path.
            policy=json.loads((run_dir/'run-policy.json').read_text());policy.update(change)
            (run_dir/'run-policy.json').write_text(json.dumps(policy))
            before=(run_dir/'ledger.json').read_bytes()
            result=controller.launch_operation(run_dir,r['assignment'],codex_bin=str(fake))
            self.assertEqual('refused',result['status'],result)
            self.assertEqual(before,(run_dir/'ledger.json').read_bytes())
            self.assertEqual([],self.invocations(fake))

    def test_acceptance_v09_mixed_budget_revision_and_eligibility_at_limit(self):
        fail = self.root/'required-failure'
        setup=f"\nif Path({str(fail)!r}).exists(): raise AssertionError('required behavior failed')\n"
        controller,run_dir,producer,counter=self.producer_run(setup,implementation_mode={'product':'real defect\n','edits':{'product.py':'def calculate(x):\n    return 0\n'}},
            allowed_paths=['product.py'],task_documents={'brief':'# T1\nAC behavior: product.calculate(2) must return 4.\n',
            'verification':'Source brief: T1.md\nFrozen checks and independent calculate(2)==4 probe.\n'})
        self.assertEqual('passed',controller.inspect_candidate(run_dir,producer)['status'])
        first=self.reserve(run_dir,'verify','real-failure')
        self.assertEqual('failed',controller.check_candidate(run_dir,first['assignment'],timeout_seconds=5)['status'])
        first_fix=self.correct_and_recheck(controller,run_dir,'check-fix',reason='check_failed')
        self.assertIsNone(self.collect(controller,run_dir,{'findings':[self.finding()]},key='budget-collection')[0]['blocker'])
        review,_,_=self.accept(controller,run_dir,{'decision':{'action':'correct','dispositions':[self.disposition()]}},key='budget-review')
        self.assertIsNone(review['blocker'],review)
        second_fix=self.correct_and_recheck(controller,run_dir,'review-fix',{'edits':{'product.py':'def calculate(x):\n    return x*2\n'}})
        # An owner-authorized revision changes inputs, policy and flow without resetting history/count.
        request=self.revision_request(run_dir)
        request['payload']['policy']['flow']=flow_profile('strong-local')
        request['payload']['policy']['verification']['repository_gate']='python3 -m unittest test_targeted'
        self.bind_owner(request)
        self.assertEqual('revised',controller.revise_inputs(run_dir,request)['status'])
        self.assertEqual(2,load_controller().status_run(run_dir)['correction_count'])
        self.assertFalse(controller.status_run(run_dir)['readiness_current'])
        before=(run_dir/'ledger.json').read_bytes()
        self.assertEqual('refused',controller.launch_operation(run_dir,second_fix['assignment'],codex_bin=str(self.actor()),timeout_seconds=5)['status'])
        self.assertEqual(before,(run_dir/'ledger.json').read_bytes())
        # Explicit upstream repair authority is the only seeded route. ART-009 is never seeded.
        self.seed_successor(run_dir,stage='correction',correction_request='environment_repair')
        repair=self.reserve(run_dir,'correction','authorized-repair',reason='environment_repair')
        self.assertEqual('reserved',repair['status'],repair)
        fake=self.actor();self.launch(controller,run_dir,repair,fake)
        self.assertIsNone(self.terminal(controller,run_dir,repair['assignment']['operation_id'])['blocker'])
        self.assertFalse(controller.status_run(run_dir)['readiness_current'])
        self.assertEqual(['reserve:preflight'], controller.status_run(run_dir)['next_actions'])
        self.assertEqual('refused',self.reserve(run_dir,'implement','premature-after-repair')['status'])
        # Negative evidence: a repointed old readiness receipt cannot bypass repair.
        preserved=(run_dir/'ledger.json').read_bytes();ledger=json.loads(preserved)
        old=ledger['actor_operations'][0]['assignment']
        ledger['readiness']={field:old[field] for field in ('task_id','operation_id','inputs_sha256','policy_sha256','flow_sha256')}
        ledger['readiness']['status']='ready';(run_dir/'ledger.json').write_text(json.dumps(ledger))
        self.assertFalse(controller.status_run(run_dir)['readiness_current'])
        (run_dir/'ledger.json').write_bytes(preserved)
        self.preflight(controller,run_dir,fake,key='fresh-after-repair')
        self.assertEqual('passed',controller.inspect_candidate(run_dir,repair['assignment']['operation_id'])['status'])
        check=self.reserve(run_dir,'verify','third-cycle-check')
        self.assertEqual('passed',controller.check_candidate(run_dir,check['assignment'],timeout_seconds=5)['status'])
        resolved_finding=self.finding(evidence='current requirements pass after third correction')
        self.assertIsNone(self.collect(controller,run_dir,{'findings':[resolved_finding]},key='third-cycle-collection')[0]['blocker'])
        result,_,_=self.accept(controller,run_dir,{'decision':{'dispositions':[self.disposition('resolved',evidence=resolved_finding['evidence'])]}},key='at-limit')
        self.assertIsNone(result['blocker'],result)
        self.assertTrue(controller.status_run(run_dir)['completion_eligible'])
        self.assertEqual(3,controller.status_run(run_dir)['correction_count'])
        for reserved in (first_fix,second_fix,repair):
            operation=next(op for op in self.read_ledger(run_dir)['actor_operations'] if op['operation_id']==reserved['assignment']['operation_id'])
            before=(run_dir/'ledger.json').read_bytes()
            self.assertEqual('replayed',load_controller().reserve_operation(run_dir,**operation['request'])['status'])
            self.assertEqual('replayed',controller.observe_operation(run_dir,operation['operation_id'])['status'])
            self.assertEqual(before,(run_dir/'ledger.json').read_bytes())
        # At count three a genuinely failing required check authorizes no fourth correction.
        fail.touch()
        fourth_check=self.reserve(run_dir,'verify','failure-after-three')
        self.assertEqual('failed',controller.check_candidate(run_dir,fourth_check['assignment'],timeout_seconds=5)['status'])
        before=(run_dir/'ledger.json').read_bytes();calls=len(self.invocations(fake))
        refusal=self.reserve(run_dir,'correction','fourth',reason='check_failed')
        self.assertEqual('corrections_exhausted',refusal['reason'],refusal)
        self.assertEqual(before,(run_dir/'ledger.json').read_bytes())
        self.assertEqual(calls,len(self.invocations(fake)))
        self.assertFalse(controller.status_run(run_dir)['completion_eligible'])
        self.assertEqual('refused',self.reserve(run_dir,'implement','second-cycle-zero')['status'])
        self.assertIn('active chat',controller.status_run(run_dir)['chat_relay_action'])
        for occupancy,reliable,expected in ((None,True,'fresh'),(0.1,False,'fresh'),('invalid',True,'fresh'),(0.499,True,'reuse'),(0.5,True,'fresh'),(0.501,True,'fresh')):
            self.assertEqual(expected,controller._load_component("flow_policy").correction_session_policy(occupancy=occupancy,reliable=reliable))


    def test_v08_revision_rejects_stale_launch_and_repointed_readiness(self):
        controller,run_dir=self.create_initialized_run();fake=self.actor()
        original=self.preflight(controller,run_dir,fake)
        old_readiness=self.read_ledger(run_dir)['readiness']
        request=self.revision_request(run_dir)
        self.assertEqual('revised',controller.revise_inputs(run_dir,request)['status'])
        self.assertFalse(controller.status_run(run_dir)['readiness_current'])
        self.assertEqual('refused',controller.launch_operation(run_dir,original['assignment'],codex_bin=str(fake),timeout_seconds=5)['status'])
        ledger=self.read_ledger(run_dir);ledger['readiness']=old_readiness
        (run_dir/'ledger.json').write_text(json.dumps(ledger))
        self.assertFalse(controller.status_run(run_dir)['readiness_current'])
        fake=self.actor({'field':'inputs_sha256','value':original['assignment']['inputs_sha256']})
        bad=self.reserve(run_dir,key='stale-output');self.launch(controller,run_dir,bad,fake)
        self.assertIsNotNone(self.terminal(controller,run_dir,bad['assignment']['operation_id'])['blocker'])
        fake=self.actor()
        self.preflight(controller,run_dir,fake,key='revised-preflight')
        new_input=self.invocations(fake)[-1]['prompt']['frozen_inputs']['documents']['brief']['content']
        self.assertIn('Owner-approved requirement',new_input)
        self.assertEqual(0,controller.status_run(run_dir)['correction_count'])
        r=self.reserve(run_dir,'implement','after-revision');self.launch(controller,run_dir,r,fake)
        self.terminal(controller,run_dir,r['assignment']['operation_id'])

    def test_acceptance_v01_fresh_current_decision_without_completion(self):
        controller,run_dir,counter=self.checked_collection_run()
        self.assertIsNone(self.collect(controller,run_dir)[0]['blocker'])
        fake=self.actor({'prose':True})
        reserved=self.reserve(run_dir,'acceptance','acceptance')
        self.assertFalse(reserved['assignment']['can_change_files'])
        self.launch(controller,run_dir,reserved,fake)
        outcome=self.terminal(controller,run_dir,reserved['assignment']['operation_id'])
        self.assertIsNone(outcome['blocker'])
        status=controller.status_run(run_dir)
        self.assertEqual('passed',status['evidence']['semantic_review']['status'])
        self.assertEqual('passed',status['evidence']['acceptance']['status'],status)
        self.assertTrue(status['completion_eligible'],status)
        self.assertNotEqual('completed',status['state'])
        sessions=[op['transport']['outcome']['observed']['thread_id'] for op in status['operation_history'] if op.get('transport')]
        self.assertEqual(4,len(set(sessions)))
        self.assertEqual(b'xx',counter.read_bytes())
        invocation=self.invocations(fake)[-1]
        self.assertIn('gpt-6.1-sol',invocation['argv'])
        self.assertIn('model_reasoning_effort="medium"',invocation['argv'])
        context=invocation['prompt']['collection_context']
        self.assertEqual(str(run_dir.resolve()),context['run_dir'])
        self.assertEqual(status['acceptance_decision']['decision']['evidence'],context['evidence'])
        self.assertIn('sbx',context['runtime_limits'])
        prompt=(run_dir/'actors'/reserved['assignment']['operation_id']/'prompt.txt').read_text()
        self.assertIn('do not implement, correct, collect evidence or write the tracker',prompt)
        self.assertFalse((self.repo/'docs/known-issues.md').exists())

    def launch_process(self, run_dir, fake, reservation, boundary=None, gate=None):
        request=self.root/(run_dir.name+'-assignment.json')
        request.write_text(json.dumps(reservation['assignment']))
        source=r'''
import json,sys,time
from pathlib import Path
sys.path.insert(0,sys.argv[1])
import controller
run=Path(sys.argv[2]); assignment=json.loads(Path(sys.argv[3]).read_text())
fake=sys.argv[4]; boundary=sys.argv[5]; gate=sys.argv[6]
if gate:
    Path(gate+'.'+str(__import__('os').getpid())).touch()
    while not Path(gate).exists(): time.sleep(0.01)
original=controller.run_records.save_actor_ledger
calls=0
def save(root,ledger):
    global calls
    calls+=1
    pause=(boundary=='intent' and calls==1) or (boundary=='published' and calls==2) or (boundary=='terminal' and ledger['actor_operations'][-1]['state']=='terminal')
    if boundary=='spawn' and calls==2:
        (run/'checkpoint').touch()
        while True: time.sleep(0.01)
    original(root,ledger)
    if pause:
        (run/'checkpoint').touch()
        while True: time.sleep(0.01)
controller.run_records.save_actor_ledger=save
if boundary in {'collection-report','acceptance-record'}:
    publish=controller._storage_module.publish_or_reuse_bytes
    def publish_report(path,content):
        publish(path,content)
        if path.parent.name==('collections' if boundary=='collection-report' else 'decisions'):
            (run/'checkpoint').touch()
            while True: time.sleep(.01)
    controller._storage_module.publish_or_reuse_bytes=publish_report
result=controller.launch_operation(run,assignment,codex_bin=fake,timeout_seconds=5)
if boundary in {'terminal','collection-report','acceptance-record'}:
    while True:
        observed=controller.observe_operation(run,assignment['operation_id'])
        if observed['status']=='refused' and 'owns this run' not in observed.get('detail',''): raise RuntimeError(observed)
        time.sleep(0.01)
print(json.dumps(result),flush=True)
'''
        return subprocess.Popen([sys.executable,'-c',source,str(fixtures.CONTROLLER_PATH.parent),str(run_dir),str(request),str(fake),boundary or '',str(gate) if gate else ''],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)

    def test_v04_real_launch_contention_has_one_invocation(self):
        controller,run_dir=self.create_initialized_run();fake=self.actor()
        r=self.reserve(run_dir);gate=self.root/'launch-go'
        processes=[self.launch_process(run_dir,fake,r,gate=gate) for _ in range(2)]
        for p in processes:self.wait_file(Path(str(gate)+'.'+str(p.pid)))
        gate.touch()
        results=[]
        for p in processes:
            stdout,stderr=p.communicate(timeout=8)
            self.assertEqual(0,p.returncode,stderr)
            results.append(json.loads(stdout))
        self.assertEqual(1,sum(r['status']=='launched' for r in results),results)
        self.terminal(controller,run_dir,r['assignment']['operation_id'])
        self.assertEqual(1,len(self.invocations(fake)))

    def test_v09_publication_interruption_never_relaunches(self):
        for index,boundary in enumerate(('intent','spawn','published','terminal')):
            with self.subTest(boundary=boundary):
                controller,run_dir=self.create_initialized_run(name=boundary)
                fake=self.actor({} if boundary=='terminal' else {'wait':True})
                for marker in ('waiting',):
                    (fake.parent/marker).unlink(missing_ok=True)
                r=self.reserve(run_dir)
                process=self.launch_process(run_dir,fake,r,boundary=boundary)
                self.wait_file(run_dir/'checkpoint')
                if boundary in {'spawn','published'}:self.wait_file(fake.parent/'waiting')
                process.kill();process.communicate(timeout=5)
                replay=load_controller().launch_operation(run_dir,r['assignment'],codex_bin=str(fake),timeout_seconds=5)
                self.assertEqual('replayed',replay['status'],replay)
                self.assertEqual('refused',self.reserve(run_dir,key='duplicate')['status'])
                if boundary=='intent':
                    self.assertEqual('unknown',controller.observe_operation(run_dir,r['assignment']['operation_id'])['status'])
                    stopped=controller.stop_operation(run_dir,r['assignment']['operation_id'])
                    self.assertEqual('unknown',stopped['status'])
                    self.assertEqual(index,len(self.invocations(fake)))
                elif boundary in {'spawn','published'}:
                    self.assertFalse(controller.status_run(run_dir)['readiness_current'])
                    controller.stop_operation(run_dir,r['assignment']['operation_id'])
                    self.terminal(controller,run_dir,r['assignment']['operation_id'])
                    self.assertEqual(index,len(self.invocations(fake)))
                else:
                    self.assertEqual('replayed',controller.observe_operation(run_dir,r['assignment']['operation_id'])['status'])
                    self.assertTrue(controller.status_run(run_dir)['readiness_current'])
                    self.assertEqual(3,len(self.invocations(fake)))


    def producer_run(self, check_setup="", extra_checks=None, implementation_mode=None, allowed_paths=None, required_reviews=None, task_documents=None):
        counter = self.root / 'check-count'
        (self.repo / 'test_targeted.py').write_text(
            "from pathlib import Path\n"
            f"p=Path({str(counter)!r}); p.write_bytes(p.read_bytes()+b'x' if p.exists() else b'x')\n"
            "PRODUCT = Path('allowed.txt').read_text()\n"
            "import unittest\nclass ProductTest(unittest.TestCase):\n"
            "    def test_content(self):\n"
            "        self.assertEqual('local implementation marker\\n', PRODUCT)\n"
            "print('real-check-output')\n" + check_setup)
        (self.repo / '.gitignore').write_text('__pycache__/\n')
        fake = self.actor(implementation_mode)
        policy = self.policy()
        policy['verification']['targeted_checks'].extend(extra_checks or [])
        controller=load_controller()
        original_init=controller.init_run
        def initialize(run,policy_path,manifest_path,repository):
            if allowed_paths or required_reviews or task_documents:
                manifest=json.loads(manifest_path.read_text())
                manifest['tasks'][0]['allowed_paths'].extend(allowed_paths or [])
                if required_reviews: manifest['tasks'][0]['required_reviews']=required_reviews
                manifest_path.write_text(json.dumps(manifest))
                if task_documents:
                    brief=self.repo/manifest['tasks'][0]['brief_path']
                    for name,content in task_documents.items():
                        (brief if name=='brief' else brief.with_name('verification.md')).write_text(content)
            return original_init(run,policy_path,manifest_path,repository)
        with mock.patch.object(self, 'policy', return_value=policy), mock.patch.object(controller,'init_run',side_effect=initialize), mock.patch.object(fixtures,'load_controller',return_value=controller):
            controller, run_dir = self.create_initialized_run()
        self.preflight(controller, run_dir, fake)
        reserved = self.reserve(run_dir, 'implement', 'implementation')
        self.launch(controller, run_dir, reserved, fake)
        self.terminal(controller, run_dir, reserved['assignment']['operation_id'])
        return controller, run_dir, reserved['assignment']['operation_id'], counter

    def test_producer_real_check_replay_and_stale_bytes(self):
        controller, run_dir, operation_id, counter = self.producer_run()
        candidate = controller.inspect_candidate(run_dir, operation_id)
        self.assertEqual('passed', candidate['status'], candidate)
        self.assertEqual(0, controller.status_run(run_dir)['correction_count'])
        reserved = self.reserve(run_dir, 'verify', 'check')
        self.assertEqual('reserved', reserved['status'], reserved)
        assignment = reserved['assignment']
        result = controller.check_candidate(run_dir, assignment, timeout_seconds=5)
        if result['status'] != 'passed':
            record = json.loads((run_dir / result['execution_path']).read_text())
            self.fail(str(record) + '\n' + ''.join((run_dir / o['stderr_path']).read_text() for o in record['outcomes']))
        self.assertEqual(b'x', counter.read_bytes())
        execution = json.loads((run_dir / result['execution_path']).read_text())
        self.assertEqual('sbx_yolo', execution['execution_mechanism'])
        self.assertEqual(0, execution['outcomes'][0]['exit_code'])
        self.assertIn(b'real-check-output', (run_dir / execution['outcomes'][0]['stdout_path']).read_bytes())
        request = self.root / 'completed-check.json'
        request.write_text(json.dumps(assignment))
        cli = subprocess.run([sys.executable, str(fixtures.CONTROLLER_PATH), 'check-candidate', '--run-dir', str(run_dir), '--request', str(request), '--timeout-seconds', '5'], capture_output=True, text=True)
        self.assertEqual(0, cli.returncode, cli.stderr)
        self.assertEqual(result, json.loads(cli.stdout))
        before = (run_dir / 'ledger.json').read_bytes()
        self.assertEqual(result, controller.check_candidate(run_dir, assignment, timeout_seconds=5))
        self.assertEqual(before, (run_dir / 'ledger.json').read_bytes())
        self.assertEqual(b'x', counter.read_bytes())
        # Replaying retained proof must validate it without rerunning commands.
        proof = run_dir / result['execution_path']
        log = run_dir / execution['outcomes'][0]['stdout_path']
        for path in (proof, log):
            with self.subTest(tampered=path.name):
                raw = path.read_bytes()
                path.write_bytes(raw + b'changed proof')
                replay = controller.check_candidate(run_dir, assignment, timeout_seconds=5)
                self.assertEqual('refused', replay['status'], replay)
                self.assertEqual(before, (run_dir / 'ledger.json').read_bytes())
                self.assertEqual(b'x', counter.read_bytes())
                path.write_bytes(raw)
        # Owner decision: ordinary replay rejects inconsistent dispositions.
        result_path = run_dir / result['path']
        raw_result = result_path.read_bytes()
        for status in ('failed', 'not_run', 'blocked', 'stale'):
            with self.subTest(contradictory_status=status):
                result_path.write_bytes(controller._storage_module.canonical_record_bytes(dict(result, status=status)))
                replay = controller.check_candidate(run_dir, assignment, timeout_seconds=5)
                self.assertEqual('refused', replay['status'], replay)
                self.assertIn('contradicts', replay['reason'])
                self.assertEqual(before, (run_dir / 'ledger.json').read_bytes())
                self.assertEqual(b'x', counter.read_bytes())
                result_path.write_bytes(raw_result)
        (self.repo / 'allowed.txt').write_text('changed after checking\n')
        status = controller.status_run(run_dir)
        self.assertEqual('stale', status['evidence']['verify']['status'])
        self.assertEqual('stale', controller.check_candidate(run_dir, assignment, timeout_seconds=5)['status'])
        self.assertEqual(b'x', counter.read_bytes())

    def test_check_evidence_owner_rejects_changed_proof_and_disposition(self):
        controller, run_dir, producer, counter = self.producer_run()
        self.assertEqual('passed', controller.inspect_candidate(run_dir, producer)['status'])
        reserved = self.reserve(run_dir, 'verify', 'check-integrity')
        result = controller.check_candidate(run_dir, reserved['assignment'], timeout_seconds=5)
        self.assertEqual('passed', result['status'], result)
        owner = controller._check_evidence_module
        execution_path = run_dir / result['execution_path']
        raw = execution_path.read_bytes()
        execution = json.loads(raw)
        identity = execution['closure_identity']
        self.assertEqual(execution, owner.validate_check_evidence(run_dir, result, identity))
        before = (run_dir / 'ledger.json').read_bytes()
        execution_path.write_bytes(raw + b'\n')
        with self.assertRaisesRegex(ValueError, 'Execution record changed'):
            owner.validate_check_evidence(run_dir, result, identity)
        execution_path.write_bytes(raw)
        wrong_identity = json.loads(json.dumps(identity))
        wrong_identity['subject']['attempt_id'] = 'another-operation'
        with self.assertRaisesRegex(ValueError, 'closure identity'):
            owner.validate_check_evidence(run_dir, result, wrong_identity)
        for stream in ('stdout', 'stderr'):
            with self.subTest(stream=stream):
                path = run_dir / execution['outcomes'][0][f'{stream}_path']
                original = path.read_bytes()
                path.write_bytes(original + b'changed log')
                with self.assertRaisesRegex(ValueError, 'Execution log changed'):
                    owner.validate_check_evidence(run_dir, result, identity)
                path.write_bytes(original)
        for status in ('failed', 'not_run', 'blocked', 'stale'):
            with self.subTest(status=status):
                with self.assertRaisesRegex(ValueError, 'disposition contradicts'):
                    owner.validate_check_evidence(run_dir, dict(result, status=status), identity)
        # An empty retained execution is not proof that any required check ran.
        omitted = dict(execution, plan=[], outcomes=[], terminal_reason='omitted_by_policy')
        omitted_raw = controller._storage_module.canonical_record_bytes(omitted)
        execution_path.write_bytes(omitted_raw)
        omitted_result = dict(result, status='not_run', execution_sha256=controller.run_records.sha256_bytes(omitted_raw))
        self.assertEqual(omitted, owner.validate_check_evidence(run_dir, omitted_result, identity))
        with self.assertRaisesRegex(ValueError, 'disposition contradicts'):
            owner.validate_check_evidence(run_dir, dict(omitted_result, status='passed'), identity)
        execution_path.write_bytes(raw)
        self.assertEqual(before, (run_dir / 'ledger.json').read_bytes())
        self.assertEqual(b'x', counter.read_bytes())

    def checked_collection_run(self, check_setup='', implementation_mode=None, allowed_paths=None, required_reviews=None, task_documents=None):
        controller, run_dir, producer, counter = self.producer_run(check_setup, implementation_mode=implementation_mode, allowed_paths=allowed_paths, required_reviews=required_reviews, task_documents=task_documents)
        self.assertEqual('passed', controller.inspect_candidate(run_dir, producer)['status'])
        check = self.reserve(run_dir, 'verify', 'initial-check')
        outcome = controller.check_candidate(run_dir, check['assignment'], timeout_seconds=5)
        self.assertEqual('passed', outcome['status'], outcome)
        return controller, run_dir, counter

    def collect(self, controller, run_dir, mode=None, key='collect'):
        fake = self.actor(mode)
        reserved = self.reserve(run_dir, 'semantic_review', key)
        self.assertEqual('reserved', reserved['status'], reserved)
        self.launch(controller, run_dir, reserved, fake)
        return self.terminal(controller, run_dir, reserved['assignment']['operation_id']), fake, reserved

    def acceptance_ready(self, findings=None, **producer_options):
        controller, run_dir, counter = self.checked_collection_run(**producer_options)
        outcome, _, _ = self.collect(controller, run_dir, {'findings': findings or []})
        self.assertIsNone(outcome['blocker'], outcome)
        return controller, run_dir, counter

    def accept(self, controller, run_dir, mode=None, key='accept'):
        fake = self.actor(mode)
        reserved = self.reserve(run_dir, 'acceptance', key)
        self.assertEqual('reserved', reserved['status'], reserved)
        self.launch(controller, run_dir, reserved, fake)
        return self.terminal(controller, run_dir, reserved['assignment']['operation_id']), fake, reserved

    def finding(self, evidence='behavior probe: defective result', exposure='prepared task consumer'):
        return {'id':'F-01','evidence':[evidence], 'requirement':'AC behavior',
                'context':'Calling calculate(2) returns 0 rather than 4; bounded product function', 'exposure':exposure}

    def disposition(self, kind='blocking', **changes):
        item = {'id':'F-01','kind':kind,'rationale':'Current contextual evidence supports this disposition',
                'evidence':['behavior probe: defective result'], 'requirement_violation':kind=='blocking',
                'material_risk':False, 'correction_authorized':True,
                'trigger':'calculate(2)', 'consequence':'incorrect returned value', 'boundary':'product.py',
                'impact':'bounded local result', 'likelihood':'each invocation', 'mitigation':'local task branch',
                'compatible_consumers':'existing local consumers unaffected', 'follow_up':'owner: improve diagnostic',
                'reassess_when':'consumer/exposure or requirement changes'}
        item.update(changes)
        return item

    def test_acceptance_v02_identity_terminality_matrix(self):
        controller, run_dir, _ = self.acceptance_ready()
        fields = ('run_id','task_id','operation_id','operation_key','role','stage','inputs_sha256',
                  'policy_sha256','flow_sha256','flow_revision','candidate_sha256')
        values={'role':'implementer','stage':'implement','flow_revision':2}
        cases = [(field, {'field':field,'value':values.get(field,'b'*64 if field.endswith('_sha256') else 'wrong')}) for field in fields]
        cases += [('collector-role',{'field':'role','value':'review_collector'}),
                  ('no-session',{'result_extra':{'session_id':None}}),('wrong-session',{'session':True}),
                  ('no-observation',{'before_session':True}),('malformed',{'malformed':True}),
                  ('missing',{'missing':True}),('typed',{'field':'flow_revision','value':True}),
                  ('failed-process',{'after_session':True}),
                  ('nonterminal-claim',{'result_extra':{'status':'blocked'}})]
        history=self.read_ledger(run_dir)['actor_operations']
        for op in history:
            if op.get('transport'):
                cases.append(('reuse-'+op['assignment']['stage'],{'observed_session':op['transport']['outcome']['observed']['thread_id']}))
        for index,(name,mode) in enumerate(cases):
            with self.subTest(case=name):
                result,_,_=self.accept(controller,run_dir,mode,key='identity-'+str(index))
                self.assertIsNotNone(result['blocker'],result)
                self.assertFalse(load_controller().status_run(run_dir)['completion_eligible'])
                self.assertEqual(0,self.read_ledger(run_dir)['correction_cycle'])
        result,_,_=self.accept(controller,run_dir,key='fresh-after-refusals')
        self.assertIsNone(result['blocker'],result)
        session=result['operation']['transport']['outcome']['observed']['thread_id']
        # A new evidence-only collection opens another assignment; prior acceptance is not a fresh session.
        self.assertIn('reserve:semantic_review', controller.status_run(run_dir)['next_actions'])
        self.assertIsNone(self.collect(controller,run_dir,key='repeat-collection')[0]['blocker'])
        result,_,_=self.accept(controller,run_dir,{'observed_session':session},key='reused-acceptance')
        self.assertIsNotNone(result['blocker'],result)

    def test_acceptance_v03_retained_artifact_integrity_matrix(self):
        controller,run_dir,_=self.acceptance_ready()
        ledger=self.read_ledger(run_dir)
        check=json.loads((run_dir/ledger['evidence']['verify']['path']).read_text())
        collection=json.loads((run_dir/ledger['evidence']['semantic_review']['path']).read_text())
        rerun=json.loads((run_dir/collection['report']['rerun_path']).read_text())
        execution=json.loads((run_dir/check['execution_path']).read_text())
        paths=[ledger['candidate_path'],ledger['evidence']['verify']['path'],ledger['evidence']['semantic_review']['path'],
               check['execution_path'],execution['outcomes'][0]['stdout_path'],collection['report']['rerun_path'],rerun['execution_path']]
        for index,relative in enumerate(paths):
            path=run_dir/relative; raw=path.read_bytes()
            for mutation in ('missing','replaced','appended'):
                with self.subTest(path=relative,mutation=mutation):
                    if mutation=='missing':path.unlink()
                    else:path.write_bytes(raw+b'\n' if mutation=='appended' else b'{}')
                    before=(run_dir/'ledger.json').read_bytes()
                    reservation=self.reserve(run_dir,'acceptance',f'tamper-{index}-{mutation}')
                    self.assertEqual('refused',reservation['status'],reservation)
                    self.assertEqual(before,(run_dir/'ledger.json').read_bytes())
                    path.write_bytes(raw)
        path=run_dir/check['path'];raw=path.read_bytes();path.unlink()
        status=controller.status_run(run_dir)
        self.assertEqual('stale',status['evidence']['verify']['status'])
        self.assertIn('reserve:verify',status['next_actions']);path.write_bytes(raw)
        # After an otherwise valid launch, the same integrity checks still run at admission.
        fake=self.actor({'wait':True}); reserved=self.reserve(run_dir,'acceptance','late-tamper')
        self.launch(controller,run_dir,reserved,fake);self.wait_file(fake.parent/'waiting')
        path=run_dir/check['execution_path']; raw=path.read_bytes();path.write_bytes(b'{}')
        (fake.parent/'finish').touch()
        result=self.terminal(controller,run_dir,reserved['assignment']['operation_id'])
        self.assertIsNotNone(result['blocker'],result);path.write_bytes(raw)
        self.assertFalse(controller.status_run(run_dir)['completion_eligible'])

    def test_acceptance_v03_required_status_and_unsupported_claims(self):
        controller,run_dir,_=self.acceptance_ready()
        original=(run_dir/'ledger.json').read_bytes()
        for stage,status in [('verify','failed'),('verify','blocked'),('verify','not_run'),
                             ('semantic_review','blocked'),('semantic_review','missing'),
                             ('semantic_review','omitted_by_policy')]:
            with self.subTest(stage=stage,status=status):
                ledger=json.loads(original);ledger['evidence'][stage]['status']=status
                (run_dir/'ledger.json').write_text(json.dumps(ledger))
                before=(run_dir/'ledger.json').read_bytes()
                result=self.reserve(run_dir,'acceptance',stage+'-'+status)
                self.assertEqual('refused',result['status'],result)
                self.assertEqual(before,(run_dir/'ledger.json').read_bytes())
        (run_dir/'ledger.json').write_bytes(original)
        for index,decision in enumerate(({'rationale':''},{'evidence':{}},{'action':'ACCEPT'})):
            result,_,_=self.accept(controller,run_dir,{'decision':decision},key='unsupported-'+str(index))
            self.assertIsNotNone(result['blocker'],result)
            self.assertFalse(controller.status_run(run_dir)['completion_eligible'])

    def test_acceptance_v04_drift_matrix_and_replay(self):
        # Each row starts from valid prerequisites; restore exact files/index/HEAD after refusal.
        controller,run_dir,_=self.acceptance_ready()
        head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=self.repo,text=True).strip()
        product=self.repo/'allowed.txt';raw=product.read_bytes()
        mutations=[('tracked',lambda:product.write_text('drift'),lambda:product.write_bytes(raw)),
                   ('untracked',lambda:(self.repo/'new.py').write_text('value=1'),lambda:(self.repo/'new.py').unlink()),
                   ('configuration',lambda:(self.repo/'config.toml').write_text('enabled=false'),lambda:(self.repo/'config.toml').unlink()),
                   ('index',lambda:subprocess.run(['git','add','allowed.txt'],cwd=self.repo,check=True),lambda:subprocess.run(['git','reset','-q',head,'--','allowed.txt'],cwd=self.repo,check=True)),
                   ('head',lambda:subprocess.run(['git','-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','--allow-empty','-qm','drift'],cwd=self.repo,check=True),lambda:subprocess.run(['git','reset','--soft',head],cwd=self.repo,check=True))]
        for document in self.read_ledger(run_dir)['tasks'][0]['brief_path'], 'tasks/verification.md':
            path=self.repo/document
            if path.exists():
                content=path.read_bytes()
                mutations.append((document,lambda p=path:p.write_text('changed authority'),lambda p=path,c=content:p.write_bytes(c)))
        for name,mutate,restore in mutations:
            with self.subTest(case=name):
                before=(run_dir/'ledger.json').read_bytes()
                mutate()
                try:
                    self.assertEqual('refused',self.reserve(run_dir,'acceptance','drift-'+name)['status'])
                    self.assertEqual(before,(run_dir/'ledger.json').read_bytes())
                finally:restore()
        result,_,reserved=self.accept(controller,run_dir,key='valid-after-restores')
        self.assertIsNone(result['blocker'],result)
        self.assertTrue(controller.status_run(run_dir)['completion_eligible'])
        product.write_text('post-admission drift')
        self.assertEqual('replayed',load_controller().observe_operation(run_dir,reserved['assignment']['operation_id'])['status'])
        self.assertFalse(controller.status_run(run_dir)['completion_eligible'])
        product.write_bytes(raw)

    def test_acceptance_v04_in_review_drift_and_irrelevant_output(self):
        controller,run_dir,_=self.acceptance_ready()
        fake=self.actor({'wait':True});reserved=self.reserve(run_dir,'acceptance','during-review')
        self.launch(controller,run_dir,reserved,fake);self.wait_file(fake.parent/'waiting')
        product=self.repo/'allowed.txt';raw=product.read_bytes();product.write_text('during review')
        (fake.parent/'finish').touch()
        outcome=self.terminal(controller,run_dir,reserved['assignment']['operation_id'])
        self.assertIsNotNone(outcome['blocker'],outcome)
        product.write_bytes(raw)
        (self.repo/'__pycache__').mkdir(exist_ok=True)
        (self.repo/'__pycache__/generated.pyc').write_bytes(b'irrelevant output')
        result,_,_=self.accept(controller,run_dir,key='irrelevant-output')
        self.assertIsNone(result['blocker'],result)
        self.assertTrue(controller.status_run(run_dir)['completion_eligible'])

    def test_acceptance_v05_disposition_policy_and_v07_routes(self):
        controller,run_dir,_=self.acceptance_ready([self.finding()])
        cases=[('AC-failure',self.disposition(),'correct',[],True),
               ('operating-risk',self.disposition(requirement_violation=False,material_risk=True),'correct',[],True),
               ('maintenance-risk',self.disposition(requirement_violation=False,material_risk=True,boundary='coupled validation authority'),'correct',[],True),
               ('waived-AC',self.disposition('known_issue',requirement_violation=True),'accept',[],False),
               ('waived-material',self.disposition('known_issue',material_risk=True,impact='catastrophic irreversible data loss',likelihood='rare'),'accept',[],False),
               ('preference-correction',self.disposition('observation'),'correct',[],False),
               ('material-observation',self.disposition('observation',material_risk=True),'accept',[],False),
               ('unaccounted',None,'accept',[],False)]
        # Independent histories keep approved dispositions from one row out of other rows.
        for index,(name,disposition,action,unfinished,valid) in enumerate(cases):
            with self.subTest(case=name):
                # Reopen via new relevant collection evidence, preserving actual decisions and history.
                if index:
                    finding=self.finding(evidence='current proof '+str(index))
                    self.assertIsNone(self.collect(controller,run_dir,{'findings':[finding]},key='policy-collect-'+str(index))[0]['blocker'])
                decision={'action':action,'dispositions':[disposition] if disposition else [],'unfinished':unfinished}
                result,_,_=self.accept(controller,run_dir,{'decision':decision},key='policy-'+str(index))
                if valid:
                    self.assertIsNone(result['blocker'],result)
                    self.assertEqual('review_findings',self.read_ledger(run_dir)['correction_request'])
                    # Requesting the wrong reason must preserve authoritative bytes/count.
                    before=(run_dir/'ledger.json').read_bytes()
                    self.assertEqual('refused',self.reserve(run_dir,'correction','wrong-reason-'+str(index),reason='check_failed')['status'])
                    self.assertEqual(before,(run_dir/'ledger.json').read_bytes())
                    # Consume the real decision and produce a fresh candidate before the next row.
                    self.correct_and_recheck(controller,run_dir,'policy-fix-'+str(index))
                else:self.assertIsNotNone(result['blocker'],result)
        self.assertFalse(controller.status_run(run_dir)['completion_eligible'])

    def correct_and_recheck(self, controller, run_dir, key, mode=None, reason='review_findings'):
        reserved=self.reserve(run_dir,'correction',key,reason=reason)
        self.assertEqual('reserved',reserved['status'],reserved)
        fake=self.actor(mode)
        self.launch(controller,run_dir,reserved,fake)
        self.assertIsNone(self.terminal(controller,run_dir,reserved['assignment']['operation_id'])['blocker'])
        self.assertEqual('passed',controller.inspect_candidate(run_dir,reserved['assignment']['operation_id'])['status'])
        check=self.reserve(run_dir,'verify',key+'-check')
        self.assertEqual('passed',controller.check_candidate(run_dir,check['assignment'],timeout_seconds=5)['status'])
        return reserved

    def test_acceptance_v05_v06_approved_known_issue_continuity(self):
        tracker=self.repo/'docs/known-issues.md';tracker.parent.mkdir();tracker.write_text('Existing issue K-01: bounded diagnostic limitation\n')
        finding=self.finding(evidence='optional diagnostic newline omitted')
        finding.update(requirement='Diagnostic quality; no required AC violation',context='Optional newline omitted; existing local consumers compatible')
        controller,run_dir,_=self.acceptance_ready([finding])
        proposal=self.disposition('known_issue',trigger='optional diagnostic output',consequence='missing trailing newline',boundary='diagnostics')
        result,_,_=self.accept(controller,run_dir,{'decision':{'dispositions':[proposal]}})
        self.assertIsNone(result['blocker'],result)
        approved=controller.status_run(run_dir)['outstanding_findings'][0]['disposition']
        prompt=self.invocations(self.root/'actor-fixture/codex')[-1]['prompt']['collection_context']
        self.assertEqual(tracker.read_text(),prompt['known_issue_tracker']['content'])
        self.assertTrue(controller.status_run(run_dir)['completion_eligible'])
        for index,findings in enumerate(([finding],[],[finding])):
            self.assertIsNone(self.collect(controller,run_dir,{'findings':findings},key='continuity-'+str(index))[0]['blocker'])
            current=controller.status_run(run_dir)['outstanding_findings']
            self.assertEqual(1,len(current));self.assertEqual(approved,current[0]['disposition'])
            mode={'decision':{'dispositions':[proposal]}}
            result,_,_=self.accept(controller,run_dir,mode,key='continued-'+str(index))
            self.assertIsNone(result['blocker'],result)
            self.assertEqual(approved,controller.status_run(run_dir)['outstanding_findings'][0]['disposition'])
        self.assertIsNone(self.collect(controller,run_dir,key='unchanged-approved')[0]['blocker'])
        waiver,_,_=self.accept(controller,run_dir,{'decision':{'dispositions':[self.disposition('known_issue',material_risk=True)]}},key='contradictory-approval')
        self.assertIsNotNone(waiver['blocker'],waiver)
        # A preference to reopen unchanged approval cannot create correction authority.
        self.assertIsNone(self.collect(controller,run_dir,key='omitted-again')[0]['blocker'])
        result,_,_=self.accept(controller,run_dir,{'decision':{'action':'correct','dispositions':[self.disposition()]}},key='unjustified-reopen')
        self.assertIsNotNone(result['blocker'],result)
        for index,changed in enumerate((self.finding(evidence='new concrete proof'),self.finding(evidence='new concrete proof',exposure='new consumer'))):
            self.assertIsNone(self.collect(controller,run_dir,{'findings':[changed]},key='new-proof-'+str(index))[0]['blocker'])
            current=controller.status_run(run_dir)['outstanding_findings'][0]
            self.assertEqual('reopened',current['disposition']['status'])
            self.assertIn('reason',current['disposition'])
            result,_,_=self.accept(controller,run_dir,{'decision':{'dispositions':[proposal]}},key='reapproved-'+str(index))
            self.assertIsNone(result['blocker'],result)
        self.assertEqual(0,controller.status_run(run_dir)['correction_count'])
        self.assertFalse((self.repo/'known-issues.md').exists())
        self.assertEqual('Existing issue K-01: bounded diagnostic limitation\n',tracker.read_text())

    def test_acceptance_v05_observations_and_v07_evidence_only_recovery(self):
        controller,run_dir,counter=self.acceptance_ready([self.finding()])
        for index,owner in enumerate(('verify','semantic_review','intervene')):
            disposition=self.disposition('missing_evidence')
            unfinished=[{'owner':owner,'reason':'Required behavioral probe has not been demonstrated','evidence':['AC behavior']}]
            result,_,_=self.accept(controller,run_dir,{'decision':{'action':'missing_evidence','dispositions':[disposition],'unfinished':unfinished}},key='missing-'+str(index))
            self.assertIsNone(result['blocker'],result)
            status=controller.status_run(run_dir)
            self.assertFalse(status['completion_eligible']);self.assertEqual(0,status['correction_count'])
            self.assertIsNone(self.read_ledger(run_dir).get('correction_request'))
            self.assertEqual('refused',self.reserve(run_dir,'correction','not-a-fix-'+str(index),reason='review_findings')['status'])
            product=(self.repo/'allowed.txt').read_bytes()
            if owner=='verify':
                r=self.reserve(run_dir,'verify','recover-check')
                self.assertEqual('reserved',r['status'],r)
                self.assertEqual('passed',controller.check_candidate(run_dir,r['assignment'],timeout_seconds=5)['status'])
            if owner!='intervene':
                self.assertIsNone(self.collect(controller,run_dir,{'findings':[self.finding(evidence='recovered '+str(index))]},key='recover-collection-'+str(index))[0]['blocker'])
            self.assertEqual(product,(self.repo/'allowed.txt').read_bytes())
        # Blocker remains a blocker after a chat acknowledgement.
        ledger=self.read_ledger(run_dir)
        request={'key':'missing-capability','blocker':'required installed reviewer unavailable', 'evidence':'decisions',
                 'operation_id':'','required_action':'install capability in next invocation or authorize fresh source-guided review',
                 'event':'response','text':'acknowledged'}
        self.assertEqual('recorded',controller.record_intervention(run_dir,request)['status'])
        self.assertFalse(controller.status_run(run_dir)['completion_eligible'])
        self.assertEqual('refused',self.reserve(run_dir,'correction','ack-is-not-authority',reason='environment_repair')['status'])

    def test_acceptance_v08_actual_review_driven_code_correction(self):
        controller,run_dir,counter=self.acceptance_ready([self.finding()],
            implementation_mode={'edits':{'product.py':'def calculate(x):\n    return 0\n'}},allowed_paths=['product.py'],
            task_documents={'brief':'# T1\nAC behavior: product.calculate(2) must return 4. Preserve existing owner work.\n',
                            'verification':'Source brief: T1.md\nRun frozen checks and independently probe product.calculate(2)==4.\n'})
        def probe():
            result=subprocess.run([sys.executable,'-c','from product import calculate; assert calculate(2)==4'],cwd=self.repo,capture_output=True)
            return result.returncode
        self.assertNotEqual(0,probe())
        self.assertEqual(b'xx',counter.read_bytes())
        self.assertEqual('refused',self.reserve(run_dir,'correction','collection-is-not-authority',reason='review_findings')['status'])
        unfinished=[{'owner':'semantic_review','reason':'new branch behavior needs separate probe','evidence':['AC behavior']}]
        result,_,_=self.accept(controller,run_dir,{'decision':{'action':'correct','dispositions':[self.disposition()], 'unfinished':unfinished}})
        self.assertIsNone(result['blocker'],result)
        self.assertEqual(0,controller.status_run(run_dir)['correction_count'])
        correction=self.correct_and_recheck(controller,run_dir,'real-fix',{'edits':{'product.py':'def calculate(x):\n    return x*2\n'}})
        self.assertEqual('fresh',correction['assignment']['session_policy'])
        self.assertEqual(0,probe())
        self.assertEqual(1,controller.status_run(run_dir)['correction_count'])
        finding=self.finding(evidence='calculate(2)==4 after correction')
        self.assertIsNone(self.collect(controller,run_dir,{'findings':[finding]},key='corrected-collection')[0]['blocker'])
        resolved=self.disposition('resolved',evidence=finding['evidence'])
        correction_session=self.read_ledger(run_dir)['actor_operations'][-3]['transport']['outcome']['observed']['thread_id']
        refused,_,_=self.accept(controller,run_dir,{'observed_session':correction_session,'decision':{'dispositions':[resolved]}},key='reused-correction')
        self.assertIsNotNone(refused['blocker'],refused)
        result,_,_=self.accept(controller,run_dir,{'decision':{'dispositions':[resolved]}},key='corrected-acceptance')
        self.assertIsNone(result['blocker'],result)
        status=load_controller().status_run(run_dir)
        self.assertTrue(status['completion_eligible'],status)
        self.assertEqual(1,status['correction_count']);self.assertNotEqual('completed',status['state'])
        self.assertGreaterEqual(len(status['outstanding_findings'][0]['history']),4)
        self.assertEqual(b'xxxx',counter.read_bytes())

    def test_review_correction_proof_drift_requires_consistent_intervention(self):
        controller, run_dir, _ = self.acceptance_ready([self.finding()])
        result, _, _ = self.accept(controller, run_dir, {
            'decision': {'action': 'correct', 'dispositions': [self.disposition()]}})
        self.assertIsNone(result['blocker'], result)
        status = controller.status_run(run_dir)
        self.assertEqual(['reserve:correction'], status['next_actions'])
        ledger = self.read_ledger(run_dir)
        paths = [ledger['evidence'][stage]['path']
                 for stage in ('verify', 'semantic_review', 'acceptance')]
        paths.append(ledger['candidate_path'])
        before = (run_dir / 'ledger.json').read_bytes()
        for relative in paths:
            with self.subTest(proof=relative):
                path = run_dir / relative
                raw = path.read_bytes()
                try:
                    path.write_bytes(raw + b'\n')
                    status = controller.status_run(run_dir)
                    self.assertEqual(['intervene'], status['next_actions'])
                    self.assertEqual('correction_authority_stale', status['blocker'])
                    self.assertFalse(status['completion_eligible'])
                    self.assertEqual(0, status['correction_count'])
                    for stage, reason in (('verify', 'initial'), ('correction', 'review_findings')):
                        refusal = self.reserve(run_dir, stage, 'drift-' + stage, reason=reason)
                        self.assertEqual('refused', refusal['status'], refusal)
                        self.assertEqual(status['next_actions'], refusal['next_actions'])
                        self.assertEqual(status['blocker'], refusal['reason'])
                        self.assertEqual(status['state_version'], refusal['state_version'])
                        self.assertEqual(before, (run_dir / 'ledger.json').read_bytes())
                finally:
                    path.write_bytes(raw)
        self.assertEqual(['reserve:correction'], controller.status_run(run_dir)['next_actions'])

    def test_acceptance_v10_replay_ignores_replaced_raw_decision(self):
        controller,run_dir,_=self.acceptance_ready()
        result,fake,reserved=self.accept(controller,run_dir)
        self.assertIsNone(result['blocker'],result)
        before=(run_dir/'ledger.json').read_bytes()
        raw=run_dir/'actors'/reserved['assignment']['operation_id']/'result.json'
        raw.write_text(json.dumps({'decision':{'action':'correct'}}))
        replay=load_controller().observe_operation(run_dir,reserved['assignment']['operation_id'])
        self.assertEqual('replayed',replay['status']);self.assertEqual(before,(run_dir/'ledger.json').read_bytes())
        status=controller.status_run(run_dir)
        self.assertTrue(status['completion_eligible']);self.assertEqual('accept',status['acceptance_decision']['decision']['action'])
        self.assertEqual(4,len(self.invocations(fake)))
        # Losing admitted proof invalidates eligibility but does not lock out a fresh reviewer.
        decision_path=run_dir/status['evidence']['acceptance']['path'];decision_path.unlink()
        status = controller.status_run(run_dir)
        self.assertFalse(status['completion_eligible'])
        self.assertIn('reserve:acceptance', status['next_actions'])
        restored,_,_=self.accept(controller,run_dir,key='recover-missing-decision')
        self.assertIsNone(restored['blocker'],restored)
        self.assertTrue(controller.status_run(run_dir)['completion_eligible'])

    def test_acceptance_v11_live_owner_and_invalid_requests(self):
        controller,run_dir,_=self.acceptance_ready()
        for kwargs in ({'expected_version':1},{'role':'implementer'}):
            before=(run_dir/'ledger.json').read_bytes()
            self.assertEqual('refused',self.reserve(run_dir,'acceptance','invalid',**kwargs)['status'])
            self.assertEqual(before,(run_dir/'ledger.json').read_bytes())
        fake=self.actor({'wait':True});reserved=self.reserve(run_dir,'acceptance','live')
        before=(run_dir/'ledger.json').read_bytes()
        self.assertEqual('refused',self.reserve(run_dir,'acceptance','live',reason='retry')['status'])
        self.assertEqual(before,(run_dir/'ledger.json').read_bytes())
        self.launch(controller,run_dir,reserved,fake);self.wait_file(fake.parent/'waiting')
        try:
            observation=controller.observe_operation(run_dir,reserved['assignment']['operation_id'])
            self.assertEqual('running',observation['status'])
            self.assertFalse(controller.status_run(run_dir)['completion_eligible'])
            self.assertEqual('refused',self.reserve(run_dir,'semantic_review','while-live')['status'])
            self.assertEqual('replayed',load_controller().launch_operation(run_dir,reserved['assignment'],codex_bin=str(fake),timeout_seconds=5)['status'])
        finally:(fake.parent/'finish').touch()
        self.assertIsNone(self.terminal(controller,run_dir,reserved['assignment']['operation_id'])['blocker'])
        self.assertEqual(4,len(self.invocations(fake)))

    def test_acceptance_v03_conditional_stages_cannot_be_omitted_or_weakened(self):
        controller,run_dir,_=self.acceptance_ready(required_reviews=['maintainability','registry'])
        ledger=self.read_ledger(run_dir)
        references={ledger['candidate_path']:controller.run_records.sha256_bytes((run_dir/ledger['candidate_path']).read_bytes())}
        for stage in ('maintainability','registry'):
            before=(run_dir/'ledger.json').read_bytes()
            self.assertEqual('refused',self.reserve(run_dir,'acceptance','missing-'+stage)['status'])
            self.assertEqual(before,(run_dir/'ledger.json').read_bytes())
            record={key:ledger[key] for key in ('inputs_sha256','policy_sha256','flow_sha256','candidate_sha256')}
            report=run_dir/'reviews'/(stage+'-report.md');report.parent.mkdir(exist_ok=True);report.write_text('Independent scoped review: passed\n')
            bound=dict(references,**{str(report.relative_to(run_dir)):controller.run_records.sha256_bytes(report.read_bytes())})
            record.update(stage=stage,status='passed',session_id='external-independent-'+stage,
                          rationale='separate required stage completed',evidence=bound)
            path=run_dir/'reviews'/ledger['candidate_sha256']/(stage+'.json')
            path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(record))
        # Weaker task manifest bytes are not an authorized profile revision.
        manifest=run_dir/'task-manifest.json';raw=manifest.read_bytes()
        value=json.loads(raw);value['tasks'][0]['required_reviews']=[];manifest.write_text(json.dumps(value))
        self.assertEqual('refused',self.reserve(run_dir,'acceptance','weaker-profile')['status']);manifest.write_bytes(raw)
        for status in ('failed','blocked','not_run','inconclusive'):
            path=run_dir/'reviews'/ledger['candidate_sha256']/'maintainability.json';raw=path.read_bytes()
            value=json.loads(raw);value['status']=status;path.write_text(json.dumps(value))
            self.assertEqual('refused',self.reserve(run_dir,'acceptance','stage-'+status)['status']);path.write_bytes(raw)
        result,fake,_=self.accept(controller,run_dir,key='conditional-complete')
        self.assertIsNone(result['blocker'],result)
        self.assertEqual(['maintainability','registry'],self.invocations(fake)[-1]['prompt']['collection_context']['conditional_reviews'])
        self.assertTrue(controller.status_run(run_dir)['completion_eligible'])

    def test_acceptance_v05_observation_uncertainty_and_prevented_correction(self):
        for index,(kind,action,overrides,eligible) in enumerate((
            ('observation','accept',{},True),('observation','accept',{'rationale':'Ordinary uncertainty; assume local use'},True),
            ('blocker','blocker',{'material_risk':True,'correction_authorized':False},False),
            ('blocking','blocker',{'correction_authorized':False},False))):
            case=self.independent_case()
            finding=case.finding()
            if kind=='observation':
                finding.update(requirement='No required behavior violated',context='Optional diagnostic polish or unproved minor concern',evidence=['Preference or ordinary uncertainty only'])
            controller,run_dir,_=case.acceptance_ready([finding])
            proposal=case.disposition(kind,**overrides)
            unfinished=[{'owner':'intervene','reason':'owner authority needed','evidence':['current boundary']}] if action=='blocker' else []
            result,_,_=case.accept(controller,run_dir,{'decision':{'action':action,'dispositions':[proposal],'unfinished':unfinished}})
            self.assertIsNone(result['blocker'],result)
            self.assertEqual(eligible,controller.status_run(run_dir)['completion_eligible'])
            self.assertIsNone(case.read_ledger(run_dir).get('correction_request'))
            self.assertEqual(0,controller.status_run(run_dir)['correction_count'])
            if not eligible:
                self.assertIn('intervene',controller.status_run(run_dir)['next_actions'])
                self.assertEqual('refused',case.reserve(run_dir,'correction','not-authorized',reason='review_findings')['status'])

    def test_acceptance_v04_explicit_ignored_input_and_each_task_document(self):
        controller,run_dir,_=self.acceptance_ready(allowed_paths=['__pycache__/evaluated.py'])
        path=self.repo/'__pycache__/evaluated.py';path.parent.mkdir(exist_ok=True);path.write_text('evaluated')
        before=(run_dir/'ledger.json').read_bytes()
        self.assertEqual('refused',self.reserve(run_dir,'acceptance','ignored-evaluated')['status'])
        self.assertEqual(before,(run_dir/'ledger.json').read_bytes());path.unlink()
        inputs=json.loads((run_dir/'inputs.json').read_text())
        for name,document in inputs['documents'].items():
            path=self.repo/document['source_path'];raw=path.read_bytes();path.write_text('unauthorized task input')
            self.assertEqual('refused',self.reserve(run_dir,'acceptance','task-drift-'+name)['status']);path.write_bytes(raw)
        self.assertIsNone(self.accept(controller,run_dir,key='restored-inputs')[0]['blocker'])

    def test_acceptance_v10_real_publication_interruptions(self):
        for boundary in ('intent','acceptance-record','terminal'):
            with self.subTest(boundary=boundary):
                case=self.independent_case();controller,run_dir,_=case.acceptance_ready()
                fake=case.actor();reserved=case.reserve(run_dir,'acceptance','interrupted-acceptance')
                process=case.launch_process(run_dir,fake,reserved,boundary=boundary)
                try:case.wait_file(run_dir/'checkpoint')
                finally:process.kill();process.communicate(timeout=5)
                replay=load_controller().launch_operation(run_dir,reserved['assignment'],codex_bin=str(fake),timeout_seconds=5)
                self.assertEqual('replayed',replay['status'],replay)
                if boundary=='intent':
                    outcome=controller.observe_operation(run_dir,reserved['assignment']['operation_id'])
                    self.assertEqual('unknown',outcome['status'],outcome)
                    self.assertFalse(controller.status_run(run_dir)['completion_eligible'])
                    self.assertEqual('refused',case.reserve(run_dir,'acceptance','retry-unknown')['status'])
                    self.assertEqual(3,len(case.invocations(fake)))
                else:
                    outcome=case.terminal(controller,run_dir,reserved['assignment']['operation_id'])
                    self.assertIsNone(outcome.get('blocker'),outcome)
                    self.assertTrue(load_controller().status_run(run_dir)['completion_eligible'])
                    self.assertEqual(4,len(case.invocations(fake)))
                    before=(run_dir/'ledger.json').read_bytes()
                    self.assertEqual('replayed',controller.observe_operation(run_dir,reserved['assignment']['operation_id'])['status'])
                    self.assertEqual(before,(run_dir/'ledger.json').read_bytes())

    def test_acceptance_v11_real_launch_contention_has_one_actor(self):
        controller,run_dir,_=self.acceptance_ready();fake=self.actor()
        reserved=self.reserve(run_dir,'acceptance','competing-acceptance');gate=self.root/'launch-acceptance'
        processes=[self.launch_process(run_dir,fake,reserved,gate=gate) for _ in range(2)]
        for process in processes:self.wait_file(Path(str(gate)+'.'+str(process.pid)))
        gate.touch();results=[]
        for process in processes:
            stdout,stderr=process.communicate(timeout=8);self.assertEqual(0,process.returncode,stderr)
            results.append(json.loads(stdout))
        self.assertEqual(1,sum(result['status']=='launched' for result in results),results)
        self.assertIsNone(self.terminal(controller,run_dir,reserved['assignment']['operation_id'])['blocker'])
        self.assertEqual(4,len(self.invocations(fake)))

    def test_acceptance_v12_documented_cli_and_changed_schema_boundary(self):
        controller,run_dir,_=self.acceptance_ready()
        version=controller.status_run(run_dir)['state_version']
        command=[sys.executable,str(fixtures.CONTROLLER_PATH)]
        result=subprocess.run(command+['reserve','--run-dir',str(run_dir),'--expected-version',str(version),
                                     '--task-id','T1','--stage','acceptance','--role','acceptance_reviewer',
                                     '--operation-key','cli-acceptance'],capture_output=True,text=True)
        self.assertEqual(0,result.returncode,result.stderr);reserved=json.loads(result.stdout)
        request=self.root/'acceptance-assignment.json';request.write_text(json.dumps(reserved['assignment']))
        fake=self.actor()
        launched=subprocess.run(command+['launch','--run-dir',str(run_dir),'--request',str(request),
                                        '--codex-bin',str(fake),'--timeout-seconds','5'],capture_output=True,text=True)
        self.assertEqual(0,launched.returncode,launched.stderr)
        self.wait_file(run_dir/'actors'/reserved['assignment']['operation_id']/'result.state.json')
        observed=subprocess.run(command+['observe','--run-dir',str(run_dir),'--operation-id',reserved['assignment']['operation_id']],capture_output=True,text=True)
        self.assertEqual(0,observed.returncode,observed.stderr)
        self.assertIsNone(json.loads(observed.stdout)['blocker'])
        output=subprocess.run(command+['status','--run-dir',str(run_dir)],capture_output=True,text=True)
        self.assertEqual(0,output.returncode,output.stderr)
        status=json.loads(output.stdout);self.assertTrue(status['completion_eligible'])
        evidence=status['evidence']['acceptance'];raw=(run_dir/evidence['path']).read_bytes()
        self.assertEqual(evidence['sha256'],controller.run_records.sha256_bytes(raw))
        claim=json.loads((run_dir/'actors'/reserved['assignment']['operation_id']/'result.json').read_text())
        controller._load_component("review_contracts").validate_acceptance_decision(claim['decision'])
        invalid_claim=dict(claim);invalid_claim.pop('decision')
        manifest=json.loads((run_dir/'task-manifest.json').read_text())
        manifest['tasks'][0]['required_reviews']=['maintainability','registry']
        invalid_manifest=dict(manifest,tasks=[dict(manifest['tasks'][0],required_reviews=['unsupported'])])
        for name,valid,invalid_instance,rule in (
            ('actor-result',claim,invalid_claim,'required'),
            ('task-manifest',manifest,invalid_manifest,'enum'),
        ):
            with self.subTest(schema=name):
                schema=json.loads((fixtures.CONTROLLER_PATH.parents[1]/'assets'/f'{name}.schema.json').read_text())
                self.assertEqual('https://json-schema.org/draft/2020-12/schema',schema['$schema'])
                Draft202012Validator.check_schema(schema)
                validator=Draft202012Validator(schema)
                validator.validate(valid)
                with self.assertRaises(ValidationError) as rejected:
                    validator.validate(invalid_instance)
                self.assertEqual(rule,rejected.exception.validator)
        invalid=dict(claim['decision'],action='complete_task')
        with self.assertRaises(ValueError):controller._load_component("review_contracts").validate_acceptance_decision(invalid)
        self.assertNotEqual('completed',status['state'])

    def test_collection_v01_current_independent_rerun_and_handoff(self):
        controller, run_dir, counter = self.checked_collection_run()
        product = (self.repo/'allowed.txt').read_bytes()
        result, fake, reserved = self.collect(controller, run_dir)
        self.assertIsNone(result['blocker'], result)
        status = load_controller().status_run(run_dir)
        self.assertEqual('passed', status['evidence']['semantic_review']['status'], status)
        self.assertIn('reserve:acceptance', status['next_actions'])
        self.assertEqual('missing', status['evidence']['acceptance']['status'])
        self.assertEqual(0, status['correction_count'])
        self.assertEqual(b'xx', counter.read_bytes())
        self.assertEqual(product, (self.repo/'allowed.txt').read_bytes())
        prompt = self.invocations(fake)[-1]['prompt']
        self.assertEqual(['requirements','behavior','code_quality'], prompt['collection_context']['review_requirements'])
        self.assertEqual([], prompt['collection_context']['prior_findings'])
        workflow=prompt['collection_context']['review_workflow']
        self.assertIn('project-local',workflow['skill_resolution'])
        self.assertIn('separate task-acceptance-review',workflow['separate_stages'])
        self.assertIn('task-review-discovery',workflow['collection'])
        self.assertEqual(reserved['assignment']['candidate_sha256'], status['candidate_sha256'])
        report = json.loads((run_dir/status['evidence']['semantic_review']['path']).read_text())
        rerun = json.loads((run_dir/report['report']['rerun_path']).read_text())
        self.assertEqual(reserved['assignment']['operation_id']+'.rerun', rerun['operation_id'])
        self.assertNotEqual(prompt['collection_context']['check_evidence']['execution_path'], rerun['execution_path'])
        self.assertEqual(result['operation']['transport']['outcome']['observed']['thread_id'], rerun['session_id'])
        before = (run_dir/'ledger.json').read_bytes()
        raw = run_dir/'actors'/reserved['assignment']['operation_id']/'result.json'
        raw.write_text('changed raw claim after admission')
        self.assertEqual('replayed', controller.observe_operation(run_dir,reserved['assignment']['operation_id'])['status'])
        self.assertEqual(before,(run_dir/'ledger.json').read_bytes())
        self.assertEqual(b'xx',counter.read_bytes())

    def test_collection_v02_identity_and_authority_matrix(self):
        controller, run_dir, counter = self.checked_collection_run()
        producer = self.read_ledger(run_dir)['actor_operations'][1]
        reused = producer['transport']['outcome']['observed']['thread_id']
        cases = [(field, {'field':field,'value':'implementer' if field=='role' else 'b'*64 if field.endswith('_sha256') else 'wrong'}) for field in
                 ('task_id','operation_id','role','candidate_sha256','inputs_sha256','policy_sha256','flow_sha256')]
        cases += [('acceptance-role',{'field':'role','value':'acceptance_reviewer'}),
                  ('session',{'session':True}),('invented-provenance',{'result_extra':{'observed':{'thread_id':'invented'}}}),
                  ('implementation-session',{'observed_session':reused}),
                  ('malformed',{'malformed':True}),('missing',{'missing':True}),
                  ('acceptance-decision',{'result_extra':{'decision':'ACCEPT'}})]
        for index,(label,mode) in enumerate(cases):
            with self.subTest(label=label):
                outcome, _, _ = self.collect(controller,run_dir,mode,key=f'bad-{index}')
                self.assertIsNotNone(outcome['blocker'],outcome)
                status = load_controller().status_run(run_dir)
                self.assertNotEqual('passed',status['evidence']['semantic_review']['status'])
                self.assertNotIn('reserve:acceptance',status['next_actions'])
                self.assertEqual('missing',status['evidence']['acceptance']['status'])
                self.assertEqual(0,status['correction_count'])
                self.assertNotEqual('completed',status['state'])
        self.assertEqual(b'x'*(len(cases)+1),counter.read_bytes())

    def test_collection_v03_missing_replayed_wrong_bound_and_incomplete_coverage(self):
        controller, run_dir, counter = self.checked_collection_run()
        cases = [('implementer-pass',{'skip_rerun':True,'report':{'rerun_path':'checks/operation-003.json'}}),
                 ('replayed-verify',{'replay_verify':True}),
                 ('wrong-candidate',{'rerun_assignment':{'candidate_sha256':'b'*64}}),
                 ('wrong-input',{'rerun_assignment':{'inputs_sha256':'b'*64}}),
                 ('missing-rerun',{'skip_rerun':True}),
                 ('gap',{'report':{'gaps':['required behavior not inspected']}})]
        cases += [('omit-'+field,{'omit':[field]}) for field in ('coverage','gaps','findings')]
        for index,(label,mode) in enumerate(cases):
            with self.subTest(label=label):
                before_count=len(counter.read_bytes())
                outcome, fake, _ = self.collect(controller,run_dir,mode,key=f'coverage-{index}')
                self.assertIsNotNone(outcome['blocker'],outcome)
                status=load_controller().status_run(run_dir)
                self.assertNotEqual('passed',status['evidence']['semantic_review']['status'])
                self.assertNotIn('reserve:acceptance',status['next_actions'])
                self.assertEqual(0,status['correction_count'])
                if label in {'implementer-pass','replayed-verify','wrong-candidate','wrong-input','missing-rerun'}:
                    self.assertEqual(before_count,len(counter.read_bytes()))
                if label=='replayed-verify':
                    self.assertEqual('passed',json.loads((fake.parent/'verify-replay.json').read_text())['status'])

    def test_collection_v03e_real_failed_rerun_overrides_pass_claim(self):
        flag=self.root/'fail-independent-check'
        setup=f"\nProductTest.test_content = lambda self: self.assertFalse(Path({str(flag)!r}).exists(), 'independent product assertion')\n"
        controller, run_dir, counter=self.checked_collection_run(setup)
        flag.touch()
        outcome,_,_=self.collect(controller,run_dir)
        self.assertIn('failed',outcome['blocker'])
        status=load_controller().status_run(run_dir)
        self.assertEqual('failed',status['evidence']['semantic_review']['status'])
        self.assertIn('reserve:correction',status['next_actions'])
        self.assertEqual('check_failed',self.read_ledger(run_dir)['correction_request'])
        self.assertEqual(b'xx',counter.read_bytes())
        self.assertEqual(0,status['correction_count'])

    def test_collection_v04_finding_history_preserves_and_reopens_approval(self):
        controller,run_dir,counter=self.checked_collection_run()
        finding={'id':'F-1','evidence':['allowed.txt:1'],'requirement':'AC-product','context':'content inspection','exposure':'current product'}
        self.assertIsNone(self.collect(controller,run_dir,{'findings':[finding]},key='finding-1')[0]['blocker'])
        ledger=self.read_ledger(run_dir)
        # Test-only upstream ART-009 disposition fixture: collection never approves it.
        approved={'status':'approved','decision':'defer','authority':'future acceptance-owned fixture'}
        ledger['outstanding_findings'][0]['disposition']=approved
        (run_dir/'ledger.json').write_text(json.dumps(ledger))
        for index,change in enumerate(({}, {'evidence':['allowed.txt:1','behavior assertion']}, {'exposure':'new consumer'}),2):
            if index>2:
                ledger=self.read_ledger(run_dir);ledger['outstanding_findings'][0]['disposition']=approved
                (run_dir/'ledger.json').write_text(json.dumps(ledger))
            current=dict(finding,**change)
            if index==4:
                current['evidence']=self.read_ledger(run_dir)['outstanding_findings'][0]['evidence']
            result,fake,_=self.collect(controller,run_dir,{'findings':[current]},key=f'finding-{index}')
            self.assertIsNone(result['blocker'],result)
            history=load_controller().status_run(run_dir)['outstanding_findings']
            self.assertEqual(1,len(history))
            self.assertEqual(index,len(history[0]['history']))
            supplied=self.invocations(fake)[-1]['prompt']['collection_context']['prior_findings']
            self.assertEqual(index-1,len(supplied[0]['history']))
            if index==2:self.assertEqual(approved,history[0]['disposition'])
            else:self.assertEqual('reopened',history[0]['disposition']['status'])
            self.assertIsNone(self.read_ledger(run_dir).get('correction_request'))
        bad=dict(finding,disposition={'status':'approved','decision':'defer'})
        prior=load_controller().status_run(run_dir)['outstanding_findings']
        result,_,_=self.collect(controller,run_dir,{'findings':[bad]},key='invented-deferral')
        self.assertIsNotNone(result['blocker'])
        self.assertEqual(prior,load_controller().status_run(run_dir)['outstanding_findings'])
        self.assertEqual(0,controller.status_run(run_dir)['correction_count'])

    def test_collection_v05_real_failed_code_correction_and_v09_evidence_retry(self):
        controller,run_dir,producer,counter=self.producer_run(implementation_mode={'product':'actual defective product\n'})
        self.assertEqual(b'actual defective product\n',(self.repo/'allowed.txt').read_bytes())
        old_candidate=controller.inspect_candidate(run_dir,producer)
        reserved=self.reserve(run_dir,'verify','defect-check')
        failure=controller.check_candidate(run_dir,reserved['assignment'],timeout_seconds=5)
        self.assertEqual('failed',failure['status'],failure)
        original=(run_dir/failure['path']).read_bytes()
        self.assertEqual(0,controller.status_run(run_dir)['correction_count'])
        correction=self.reserve(run_dir,'correction','fix-defect','check_failed')
        fake=self.actor()
        self.launch(controller,run_dir,correction,fake)
        self.assertIsNone(self.terminal(controller,run_dir,correction['assignment']['operation_id'])['blocker'])
        self.assertEqual(b'local implementation marker\n',(self.repo/'allowed.txt').read_bytes())
        current=controller.inspect_candidate(run_dir,correction['assignment']['operation_id'])
        self.assertNotEqual(old_candidate['candidate_sha256'],current['candidate_sha256'])
        check=self.reserve(run_dir,'verify','corrected-check')
        self.assertEqual('passed',controller.check_candidate(run_dir,check['assignment'],timeout_seconds=5)['status'])
        # Reusing an observed correction session is independently refused.
        correction_session=self.read_ledger(run_dir)['actor_operations'][-2]['transport']['outcome']['observed']['thread_id']
        self.assertIsNotNone(self.collect(controller,run_dir,{'observed_session':correction_session},key='reused-correction')[0]['blocker'])
        gap,_,_=self.collect(controller,run_dir,{'skip_rerun':True},key='missing-independent')
        self.assertIsNotNone(gap['blocker'])
        product=(self.repo/'allowed.txt').read_bytes()
        self.assertIsNone(self.collect(controller,run_dir,key='fresh-independent')[0]['blocker'])
        status=load_controller().status_run(run_dir)
        self.assertEqual(1,status['correction_count'])
        self.assertIn('reserve:acceptance',status['next_actions'])
        self.assertEqual('missing',status['evidence']['acceptance']['status'])
        self.assertEqual(original,(run_dir/failure['path']).read_bytes())
        self.assertEqual(product,(self.repo/'allowed.txt').read_bytes())
        self.assertEqual(b'xxxx',counter.read_bytes())
        # The same composed task later changes again: old checks and collection
        # must lose current eligibility without erasing their historical records.
        (self.repo/'allowed.txt').write_text('later relevant product edit\n')
        status=load_controller().status_run(run_dir)
        self.assertEqual('stale',status['evidence']['verify']['status'])
        self.assertEqual('stale',status['evidence']['semantic_review']['status'])
        self.assertNotIn('reserve:acceptance',status['next_actions'])
        self.assertEqual('stale',controller.check_candidate(run_dir,check['assignment'],timeout_seconds=5)['status'])
        self.assertEqual(b'xxxx',counter.read_bytes())

    def independent_case(self):
        case = ActorOperationsTest('runTest')
        self.addCleanup(case.doCleanups)
        case.setUp()
        return case

    def assert_collection_stale(self, controller, run_dir, operation_id, counter, previous_count):
        status=load_controller().status_run(run_dir)
        self.assertEqual('stale',status['evidence']['semantic_review']['status'],status)
        self.assertNotIn('reserve:acceptance',status['next_actions'])
        before=(run_dir/'ledger.json').read_bytes()
        self.assertEqual('refused',self.reserve(run_dir,'acceptance','stale-acceptance')['status'])
        self.assertEqual(before,(run_dir/'ledger.json').read_bytes())
        # Replaying an observed outcome never repoints it to a new candidate.
        self.assertEqual('replayed',controller.observe_operation(run_dir,operation_id)['status'])
        self.assertEqual('stale',controller.status_run(run_dir)['evidence']['semantic_review']['status'])
        self.assertEqual(previous_count,len(counter.read_bytes()))

    def test_collection_v07_files_configuration_index_head_and_repointing(self):
        variants=('tracked-same-size','untracked-add','untracked-modify','untracked-remove',
                  'configuration','ignored-evaluated','index','head','repoint-report','repoint-digest')
        for variant in variants:
            with self.subTest(variant=variant):
                case=self.independent_case()
                ignored=case.repo/'__pycache__/evaluated.json'
                ignored.parent.mkdir();ignored.write_text('{"value":1}\n')
                controller,run_dir,counter=case.checked_collection_run(allowed_paths=['__pycache__/evaluated.json'])
                result,_,reserved=case.collect(controller,run_dir)
                self.assertIsNone(result['blocker'],result)
                admitted=controller.status_run(run_dir)['evidence']['semantic_review']
                raw=(run_dir/admitted['path']).read_bytes()
                if variant=='tracked-same-size':
                    product=case.repo/'allowed.txt';before=product.read_bytes()
                    product.write_bytes(b'L'+before[1:]);self.assertEqual(len(before),product.stat().st_size)
                elif variant=='untracked-add':(case.repo/'visible-input').write_text('new input')
                elif variant=='untracked-modify':
                    path=case.repo/'test_targeted.py';path.write_text(path.read_text()+'\n# relevant edit\n')
                elif variant=='untracked-remove':(case.repo/'test_targeted.py').unlink()
                elif variant=='configuration':(case.repo/'.gitignore').write_text('__pycache__/\nother/\n')
                elif variant=='ignored-evaluated':ignored.write_text('{"value":2}\n')
                elif variant=='index':subprocess.run(['git','-C',str(case.repo),'add','allowed.txt'],check=True)
                elif variant=='head':subprocess.run(['git','-C',str(case.repo),'commit','--allow-empty','-qm','head drift'],check=True)
                elif variant=='repoint-digest':
                    (case.repo/'allowed.txt').write_text('drifted product\n')
                    ledger=case.read_ledger(run_dir);ledger['candidate_sha256']='c'*64
                    ledger['evidence']['semantic_review']['candidate_sha256']='c'*64
                    (run_dir/'ledger.json').write_text(json.dumps(ledger))
                else:
                    # Deliberately repoint an admitted report path to a different artifact.
                    ledger=case.read_ledger(run_dir)
                    ledger['evidence']['semantic_review']['path']='checks/operation-003.json'
                    (run_dir/'ledger.json').write_text(json.dumps(ledger))
                case.assert_collection_stale(controller,run_dir,reserved['assignment']['operation_id'],counter,2)
                self.assertEqual(raw,(run_dir/admitted['path']).read_bytes())

    def test_collection_v07d_revision_bindings_cannot_restore_old_reports(self):
        for variant in ('task-input','policy','flow'):
            with self.subTest(variant=variant):
                case=self.independent_case()
                controller,run_dir,counter=case.checked_collection_run()
                _,_,reserved=case.collect(controller,run_dir)
                old=case.read_ledger(run_dir)
                request=case.revision_request(run_dir)
                if variant in {'policy','flow'}:
                    request['payload']['documents']={k:v['content'] for k,v in controller.load_frozen_inputs(run_dir,old)['documents'].items()}
                    if variant=='policy':request['payload']['policy']['verification']['targeted_checks'].append('python3 -m unittest test_policy')
                    else:request['payload']['policy']['flow']=flow_profile('strong-local')
                    case.bind_owner(request)
                revision=controller.revise_inputs(run_dir,request)
                self.assertEqual('revised',revision['status'],revision)
                # Test-only repointing must not restore old input-bound coverage.
                ledger=case.read_ledger(run_dir)
                ledger['evidence']['semantic_review']=old['evidence']['semantic_review']
                (run_dir/'ledger.json').write_text(json.dumps(ledger))
                case.assert_collection_stale(controller,run_dir,reserved['assignment']['operation_id'],counter,2)
                self.assertFalse(controller.status_run(run_dir)['readiness_current'])

    def test_collection_v08_drift_during_live_collection(self):
        for variant in ('product','configuration','approved-source'):
            with self.subTest(variant=variant):
                case=self.independent_case()
                controller,run_dir,counter=case.checked_collection_run()
                fake=case.actor({'wait':True})
                reserved=case.reserve(run_dir,'semantic_review','live-collection')
                case.launch(controller,run_dir,reserved,fake)
                case.wait_file(fake.parent/'waiting')
                operation_id=reserved['assignment']['operation_id']
                rerun=controller.check_collection(run_dir,reserved['assignment'],timeout_seconds=5)
                self.assertEqual('passed',rerun['status'],rerun)
                request=case.root/'rerun-request.json';request.write_text(json.dumps(reserved['assignment']))
                replay=subprocess.run([sys.executable,str(fixtures.CONTROLLER_PATH),'check-collection','--run-dir',str(run_dir),'--request',str(request),'--timeout-seconds','5'],capture_output=True,text=True)
                self.assertEqual(0,replay.returncode,replay.stderr)
                self.assertEqual(rerun,json.loads(replay.stdout))
                self.assertEqual(b'xx',counter.read_bytes())
                self.assertEqual('running',controller.observe_operation(run_dir,operation_id)['status'])
                self.assertNotEqual('passed',controller.status_run(run_dir)['evidence']['semantic_review']['status'])
                self.assertEqual('refused',case.reserve(run_dir,'acceptance','while-live')['status'])
                path=case.repo/({'product':'allowed.txt','configuration':'.gitignore','approved-source':'tasks/T1.md'}[variant])
                path.write_text(path.read_text()+'changed during collection\n')
                # End the scripted actor normally, preserving its successful old report.
                gate=fake.parent/'finish'
                gate.touch()
                outcome=case.terminal(controller,run_dir,operation_id)
                self.assertIn('stale',outcome['blocker'].lower(),outcome)
                self.assertEqual('stale',controller.status_run(run_dir)['evidence']['semantic_review']['status'])
                self.assertEqual(b'xx',counter.read_bytes())
                self.assertIn('changed during collection',path.read_text())

    def test_collection_replay_rejects_changed_execution_logs_and_disposition(self):
        controller, run_dir, counter = self.checked_collection_run()
        fake = self.actor({'wait': True})
        reserved = self.reserve(run_dir, 'semantic_review', 'integrity-replay')
        self.launch(controller, run_dir, reserved, fake)
        self.wait_file(fake.parent / 'waiting')
        assignment = reserved['assignment']
        rerun = controller.check_collection(run_dir, assignment, timeout_seconds=5)
        self.assertEqual('passed', rerun['status'], rerun)
        result_path = run_dir / rerun['path']
        execution_path = run_dir / rerun['execution_path']
        execution = json.loads(execution_path.read_bytes())
        log_path = run_dir / execution['outcomes'][0]['stdout_path']
        mutations = [(result_path, controller._storage_module.canonical_record_bytes(dict(rerun, status='failed'))),
                     (execution_path, execution_path.read_bytes() + b'\n'),
                     (log_path, log_path.read_bytes() + b'changed collector log')]
        before = (run_dir / 'ledger.json').read_bytes()
        for path, changed in mutations:
            with self.subTest(path=path.name):
                original = path.read_bytes()
                path.write_bytes(changed)
                replay = controller.check_collection(run_dir, assignment, timeout_seconds=5)
                self.assertEqual('refused', replay['status'], replay)
                self.assertEqual(before, (run_dir / 'ledger.json').read_bytes())
                self.assertEqual(b'xx', counter.read_bytes())
                path.write_bytes(original)
        self.assertEqual(rerun, controller.check_collection(run_dir, assignment, timeout_seconds=5))
        (fake.parent / 'finish').touch()
        admitted = self.terminal(controller, run_dir, assignment['operation_id'])
        self.assertIsNone(admitted['blocker'], admitted)
        self.assertEqual(b'xx', counter.read_bytes())

    def test_collection_v11_capability_blocker_and_public_request_refusals(self):
        controller,run_dir,counter=self.checked_collection_run()
        mode={'report':{'coverage':{key:{'status':'blocked' if key=='code_quality' else 'passed','evidence':'required installed review capability unavailable' if key=='code_quality' else 'inspected'} for key in ('requirements','behavior','code_quality')}}}
        outcome,fake,reserved=self.collect(controller,run_dir,mode)
        self.assertIn('capability',outcome['blocker'])
        status=load_controller().status_run(run_dir)
        self.assertEqual('blocked',status['evidence']['semantic_review']['status'])
        self.assertTrue(status['interventions'])
        self.assertIn('active',status['chat_relay_action'])
        before=(run_dir/'ledger.json').read_bytes()
        for field in ('task_id','operation_id','role','candidate_sha256','inputs_sha256','policy_sha256','flow_sha256'):
            bad=dict(reserved['assignment'],**{field:'wrong'})
            self.assertEqual('refused',controller.check_collection(run_dir,bad,timeout_seconds=5)['status'])
            self.assertEqual(before,(run_dir/'ledger.json').read_bytes())
        self.assertEqual(b'xx',counter.read_bytes())

    def corrected_checked_run(self, check_setup=''):
        controller,run_dir,producer,counter=self.producer_run(check_setup,implementation_mode={'product':'real defective product\n'})
        self.assertEqual('passed',controller.inspect_candidate(run_dir,producer)['status'])
        verify=self.reserve(run_dir,'verify','failed')
        self.assertEqual('failed',controller.check_candidate(run_dir,verify['assignment'],timeout_seconds=5)['status'])
        correction=self.reserve(run_dir,'correction','correct','check_failed')
        fake=self.actor()
        self.launch(controller,run_dir,correction,fake)
        self.terminal(controller,run_dir,correction['assignment']['operation_id'])
        self.assertEqual('passed',controller.inspect_candidate(run_dir,correction['assignment']['operation_id'])['status'])
        verify=self.reserve(run_dir,'verify','corrected')
        self.assertEqual('passed',controller.check_candidate(run_dir,verify['assignment'],timeout_seconds=5)['status'])
        return controller,run_dir,counter

    def test_collection_v10_publication_interruptions_replay_once(self):
        for boundary in ('intent','published','collection-report','terminal'):
            with self.subTest(boundary=boundary):
                case=self.independent_case()
                controller,run_dir,counter=case.corrected_checked_run()
                mode={'findings':[{'id':'F-interrupt','evidence':['allowed.txt:1'],'requirement':'AC-product','context':'interruption proof','exposure':'current'}]}
                if boundary=='published':mode['wait']=True
                fake=case.actor(mode)
                reserved=case.reserve(run_dir,'semantic_review','interrupted-collection')
                process=case.launch_process(run_dir,fake,reserved,boundary=boundary)
                try:
                    case.wait_file(run_dir/'checkpoint')
                finally:
                    process.kill();process.communicate(timeout=5)
                operation_id=reserved['assignment']['operation_id']
                self.assertEqual(1,load_controller().status_run(run_dir)['correction_count'])
                if boundary=='intent':
                    outcome=load_controller().observe_operation(run_dir,operation_id)
                    self.assertEqual('unknown',outcome['status'])
                    status=load_controller().status_run(run_dir)
                    self.assertTrue(status['interventions'])
                    self.assertEqual('refused',case.reserve(run_dir,'semantic_review','overlap')['status'])
                    self.assertEqual('replayed',controller.launch_operation(run_dir,reserved['assignment'],codex_bin=str(fake),timeout_seconds=5)['status'])
                    self.assertEqual(b'xx',counter.read_bytes())
                    continue
                if boundary=='published':
                    case.wait_file(fake.parent/'waiting')
                    self.assertEqual('running',load_controller().observe_operation(run_dir,operation_id)['status'])
                    self.assertEqual('refused',case.reserve(run_dir,'acceptance','live-acceptance')['status'])
                    (fake.parent/'finish').touch()
                result=case.terminal(load_controller(),run_dir,operation_id)
                self.assertIsNone(result.get('blocker'),result)
                status=load_controller().status_run(run_dir)
                self.assertEqual('passed',status['evidence']['semantic_review']['status'])
                self.assertEqual(1,status['correction_count'])
                self.assertEqual(1,len(status['outstanding_findings']))
                self.assertEqual(1,len(status['outstanding_findings'][0]['history']))
                before=(run_dir/'ledger.json').read_bytes()
                (run_dir/'actors'/operation_id/'result.json').write_text('replaced raw claim after admitted publication')
                self.assertEqual('replayed',load_controller().observe_operation(run_dir,operation_id)['status'])
                self.assertEqual(before,(run_dir/'ledger.json').read_bytes())
                self.assertEqual(b'xxx',counter.read_bytes())
                self.assertEqual(4,len(case.invocations(fake)))

    def test_collection_v10c_live_rerun_serializes_and_unresolved_terminal_blocks(self):
        waiting=self.root/'rerun-waiting';gate=self.root/'release-rerun';enabled=self.root/'enable-rerun-wait'
        setup=(f"\nif Path({str(enabled)!r}).exists():\n"
               f"    Path({str(waiting)!r}).touch()\n"
               "    import time\n"
               f"    while not Path({str(gate)!r}).exists(): time.sleep(.01)\n")
        controller,run_dir,counter=self.corrected_checked_run(setup)
        enabled.touch()
        fake=self.actor()
        reserved=self.reserve(run_dir,'semantic_review','live-rerun')
        self.launch(controller,run_dir,reserved,fake)
        self.wait_file(waiting)
        try:
            before=(run_dir/'ledger.json').read_bytes()
            self.assertEqual('refused',self.reserve(run_dir,'semantic_review','overlap-rerun')['status'])
            self.assertEqual('refused',controller.check_collection(run_dir,reserved['assignment'],timeout_seconds=5)['status'])
            self.assertEqual(before,(run_dir/'ledger.json').read_bytes())
            self.assertNotIn('reserve:acceptance',load_controller().status_run(run_dir)['next_actions'])
            # Kill the collector's actual coordinator while it owns the rerun.
            pid=self.invocations(fake)[-1]['pid']
            os.kill(pid,signal.SIGKILL)
        finally:
            gate.touch()
        self.wait_file(run_dir/'actors'/reserved['assignment']['operation_id']/'result.state.json')
        outcome=controller.observe_operation(run_dir,reserved['assignment']['operation_id'])
        self.assertEqual('unknown',outcome['status'],outcome)
        status=load_controller().status_run(run_dir)
        self.assertEqual('blocked',status['evidence']['semantic_review']['status'])
        self.assertIn('terminality',status['blocker'])
        self.assertTrue(status['interventions'])
        self.assertEqual(1,status['correction_count'])
        self.assertEqual('refused',self.reserve(run_dir,'acceptance','after-unknown')['status'])
        self.assertEqual('blocked',load_controller().check_collection(run_dir,reserved['assignment'],timeout_seconds=5)['status'])
        self.assertEqual(b'xxx',counter.read_bytes())

    def test_collection_v11b_missing_executable_retains_infrastructure_blocker(self):
        required=self.root/'required-check'
        required.write_text('#!/bin/sh\nexit 0\n');required.chmod(0o755)
        controller,run_dir,producer,counter=self.producer_run(extra_checks=[str(required)])
        self.assertEqual('passed',controller.inspect_candidate(run_dir,producer)['status'])
        verify=self.reserve(run_dir,'verify','available-executable')
        self.assertEqual('passed',controller.check_candidate(run_dir,verify['assignment'],timeout_seconds=5)['status'])
        required.unlink()
        fake=self.actor()
        reserved=self.reserve(run_dir,'semantic_review','missing-executable')
        self.launch(controller,run_dir,reserved,fake)
        self.wait_file(run_dir/'actors'/reserved['assignment']['operation_id']/'result.state.json')
        self.assertEqual('unknown',controller.observe_operation(run_dir,reserved['assignment']['operation_id'])['status'])
        status=load_controller().status_run(run_dir)
        self.assertEqual('blocked',status['evidence']['semantic_review']['status'])
        self.assertIn('executable',status['blocker'])
        self.assertIn('terminality',status['blocker'])
        self.assertTrue(status['interventions'])
        self.assertEqual(0,status['correction_count'])
        self.assertEqual(b'x',counter.read_bytes())

    def assert_dirty_owner_identity_protected(self, *, allowed, change):
        owner = self.repo / 'owner.txt'
        referent = (self.repo / '__pycache__' if allowed else self.root) / 'owner-referent'
        referent.parent.mkdir(exist_ok=True)
        referent.write_text('owner content\n')
        referent.chmod(0o644)
        if change == 'mode':
            owner.write_text('base\n')
            owner.chmod(0o644)
        else:
            owner.symlink_to(self.root / 'original-referent')
        subprocess.run(['git', '-C', str(self.repo), 'add', 'owner.txt'], check=True)
        subprocess.run(['git', '-C', str(self.repo), 'commit', '-qm', 'owner'], check=True)
        if change == 'mode':
            owner.write_text('dirty owner content\n')
        else:
            owner.unlink()
            owner.symlink_to(referent)
        controller = load_controller()
        original_init = controller.init_run

        def initialize(run, policy, manifest, repo):
            if allowed:
                data = json.loads(manifest.read_text())
                data['tasks'][0]['allowed_paths'].append('owner.txt')
                manifest.write_text(json.dumps(data))
            return original_init(run, policy, manifest, repo)

        with mock.patch.object(controller, 'init_run', side_effect=initialize), mock.patch.object(fixtures, 'load_controller', return_value=controller):
            controller, run_dir, operation_id, counter = self.producer_run()
        self.assertEqual('passed', controller.inspect_candidate(run_dir, operation_id)['status'])
        before_status = controller.capture_git_status(self.repo)
        if change == 'mode':
            owner.chmod(0o755)
        elif change == 'referent_mode':
            referent.chmod(0o755)
        else:
            referent.write_text('changed owner content\n')
        self.assertEqual(before_status, controller.capture_git_status(self.repo))
        ledger_before = (run_dir / 'ledger.json').read_bytes()
        result = controller.inspect_candidate(run_dir, operation_id)
        self.assertEqual('blocked', result['status'], result)
        self.assertIn('owner.txt', result['paths'])
        self.assertEqual(ledger_before, (run_dir / 'ledger.json').read_bytes())
        self.assertFalse(counter.exists())

    def test_producer_dirty_owner_mode_outside_scope(self):
        self.assert_dirty_owner_identity_protected(allowed=False, change='mode')

    def test_producer_dirty_owner_mode_inside_scope(self):
        self.assert_dirty_owner_identity_protected(allowed=True, change='mode')

    def test_producer_dirty_owner_symlink_referent_outside_scope(self):
        self.assert_dirty_owner_identity_protected(allowed=False, change='referent')

    def test_producer_dirty_owner_symlink_referent_inside_scope(self):
        self.assert_dirty_owner_identity_protected(allowed=True, change='referent')

    def test_producer_dirty_owner_symlink_executable_referent(self):
        self.assert_dirty_owner_identity_protected(allowed=True, change='referent_mode')

    def test_producer_scope_and_invalid_timeout_preserve_state(self):
        controller, run_dir, operation_id, counter = self.producer_run()
        (self.repo / 'outside.txt').write_text('outside scope')
        self.assertEqual('blocked', controller.inspect_candidate(run_dir, operation_id)['status'])
        self.assertFalse(counter.exists())
        (self.repo / 'outside.txt').unlink()
        self.assertEqual('passed', controller.inspect_candidate(run_dir, operation_id)['status'])
        reserved = self.reserve(run_dir, 'verify', 'check')
        before = (run_dir / 'ledger.json').read_bytes()
        for timeout in (0, -1, float('nan'), float('inf'), '5', True):
            with self.subTest(timeout=timeout):
                self.assertEqual('refused', controller.check_candidate(run_dir, reserved['assignment'], timeout_seconds=timeout)['status'])
                self.assertEqual(before, (run_dir / 'ledger.json').read_bytes())
        self.assertFalse(counter.exists())

    def test_producer_failed_product_does_not_pass(self):
        controller, run_dir, operation_id, counter = self.producer_run()
        (self.repo / 'allowed.txt').write_text('incorrect product\n')
        self.assertEqual('passed', controller.inspect_candidate(run_dir, operation_id)['status'])
        reserved = self.reserve(run_dir, 'verify', 'check')
        result = controller.check_candidate(run_dir, reserved['assignment'], timeout_seconds=5)
        self.assertEqual('failed', result['status'], result)
        self.assertEqual(b'x', counter.read_bytes())
        self.assertEqual(0, controller.status_run(run_dir)['correction_count'])

    def test_producer_check_side_effect_cannot_publish_pass(self):
        controller, run_dir, operation_id, counter = self.producer_run(
            "\nPath('allowed.txt').write_text('check changed product\\n')\n")
        self.assertEqual('passed', controller.inspect_candidate(run_dir, operation_id)['status'])
        unchanged_product = (self.repo / 'allowed.txt').read_bytes()
        reserved = self.reserve(run_dir, 'verify', 'check')
        result = controller.check_candidate(run_dir, reserved['assignment'], timeout_seconds=5)
        self.assertEqual('stale', result['status'], result)
        self.assertEqual(b'x', counter.read_bytes())
        self.assertEqual(0, controller.status_run(run_dir)['correction_count'])
        # A legitimate recorded divergence stays stale even if the owner restores
        # the candidate bytes; replay must not execute the side-effecting check.
        (self.repo / 'allowed.txt').write_bytes(unchanged_product)
        before = (run_dir / 'ledger.json').read_bytes()
        self.assertEqual(result, controller.check_candidate(run_dir, reserved['assignment'], timeout_seconds=5))
        self.assertEqual(before, (run_dir / 'ledger.json').read_bytes())
        self.assertEqual(b'x', counter.read_bytes())

    def test_producer_unknown_check_intent_does_not_relaunch(self):
        controller, run_dir, operation_id, counter = self.producer_run()
        self.assertEqual('passed', controller.inspect_candidate(run_dir, operation_id)['status'])
        reserved = self.reserve(run_dir, 'verify', 'check')
        with mock.patch.object(controller._verification_module, 'execute_verification_plan', side_effect=RuntimeError('execution interrupted')):
            result = controller.check_candidate(run_dir, reserved['assignment'], timeout_seconds=5)
        self.assertEqual('blocked', result['status'])
        self.assertEqual('unknown', controller.status_run(run_dir)['operation']['state'])
        result = load_controller().check_candidate(run_dir, reserved['assignment'], timeout_seconds=5)
        self.assertEqual('blocked', result['status'])
        self.assertFalse(counter.exists())
        self.assertEqual('refused', self.reserve(run_dir, 'verify', 'overlap')['status'])
    def test_producer_assignment_refusals_do_not_mutate_or_launch(self):
        controller, run_dir, operation_id, counter = self.producer_run()
        before = (run_dir / 'ledger.json').read_bytes()
        for bad_id in ('operation-001', 'operation-999'):
            self.assertEqual('refused', controller.inspect_candidate(run_dir, bad_id)['status'])
            self.assertEqual(before, (run_dir / 'ledger.json').read_bytes())
        self.assertEqual('passed', controller.inspect_candidate(run_dir, operation_id)['status'])
        reserved = self.reserve(run_dir, 'verify', 'check')
        before = (run_dir / 'ledger.json').read_bytes()
        for field in ('run_id', 'task_id', 'operation_id', 'inputs_sha256', 'policy_sha256', 'flow_sha256', 'candidate_sha256', 'stage'):
            with self.subTest(field=field):
                bad = dict(reserved['assignment'], **{field: 'wrong'})
                self.assertEqual('refused', controller.check_candidate(run_dir, bad, timeout_seconds=5)['status'])
                self.assertEqual(before, (run_dir / 'ledger.json').read_bytes())
        self.assertFalse(counter.exists())

    def test_producer_failed_product_correction_retains_history(self):
        controller, run_dir, operation_id, counter = self.producer_run()
        (self.repo / 'allowed.txt').write_text('incorrect product\n')
        candidate = controller.inspect_candidate(run_dir, operation_id)
        first = self.reserve(run_dir, 'verify', 'first-check')
        failure = controller.check_candidate(run_dir, first['assignment'], timeout_seconds=5)
        self.assertEqual('failed', failure['status'])
        original = (run_dir / failure['path']).read_bytes()
        correction = self.reserve(run_dir, 'correction', 'fix-product', reason='check_failed')
        self.assertEqual('reserved', correction['status'], correction)
        fake = self.actor()
        self.launch(controller, run_dir, correction, fake)
        self.terminal(controller, run_dir, correction['assignment']['operation_id'])
        corrected = controller.inspect_candidate(run_dir, correction['assignment']['operation_id'])
        self.assertNotEqual(candidate['candidate_sha256'], corrected['candidate_sha256'])
        second = self.reserve(run_dir, 'verify', 'second-check')
        success = controller.check_candidate(run_dir, second['assignment'], timeout_seconds=5)
        self.assertEqual('passed', success['status'], success)
        self.assertEqual(b'xx', counter.read_bytes())
        self.assertEqual(original, (run_dir / failure['path']).read_bytes())
        self.assertEqual(1, controller.status_run(run_dir)['correction_count'])
        self.assertNotEqual('passed', controller.check_candidate(run_dir, first['assignment'], timeout_seconds=5)['status'])
        self.assertEqual(b'xx', counter.read_bytes())

    def test_producer_real_interruption_after_result_reuses_one_execution(self):
        controller, run_dir, operation_id, counter = self.producer_run()
        self.assertEqual('passed', controller.inspect_candidate(run_dir, operation_id)['status'])
        reserved = self.reserve(run_dir, 'verify', 'check')
        request = self.root / 'check-assignment.json'
        request.write_text(json.dumps(reserved['assignment']))
        source = r'''
import json,sys,time
from pathlib import Path
sys.path.insert(0,sys.argv[1]); import controller
run=Path(sys.argv[2]); assignment=json.loads(Path(sys.argv[3]).read_text())
original=controller._storage_module.publish_or_reuse_bytes
def publish(path,content):
    original(path,content)
    if path.parent.name=='checks' and not path.name.endswith('.intent.json'):
        (run/'checkpoint').touch()
        while True: time.sleep(.01)
controller._storage_module.publish_or_reuse_bytes=publish
controller.check_candidate(run,assignment,timeout_seconds=5)
'''
        process = subprocess.Popen([sys.executable, '-c', source, str(fixtures.CONTROLLER_PATH.parent), str(run_dir), str(request)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            self.wait_file(run_dir / 'checkpoint')
            self.assertEqual(b'x', counter.read_bytes())
            self.assertEqual('refused', controller.inspect_candidate(run_dir, operation_id)['status'])
        finally:
            process.kill(); process.communicate(timeout=5)
        result = load_controller().check_candidate(run_dir, reserved['assignment'], timeout_seconds=5)
        self.assertEqual('passed', result['status'], result)
        self.assertEqual(b'x', counter.read_bytes())
        self.assertIsNone(controller.status_run(run_dir)['operation'])


    def test_producer_drift_during_real_check_and_exclusion(self):
        import threading
        gate = self.root / 'release-check'
        waiting = self.root / 'check-waiting'
        setup = (f"\nimport time\nPath({str(waiting)!r}).touch()\n"
                 f"while not Path({str(gate)!r}).exists(): time.sleep(.01)\n")
        controller, run_dir, operation_id, counter = self.producer_run(setup)
        self.assertEqual('passed', controller.inspect_candidate(run_dir, operation_id)['status'])
        reserved = self.reserve(run_dir, 'verify', 'check')
        results = []
        worker = threading.Thread(target=lambda: results.append(controller.check_candidate(run_dir, reserved['assignment'], timeout_seconds=5)))
        worker.start()
        try:
            self.wait_file(waiting)
            self.assertEqual('refused', load_controller().check_candidate(run_dir, reserved['assignment'], timeout_seconds=5)['status'])
            self.assertEqual('refused', controller.inspect_candidate(run_dir, operation_id)['status'])
            (self.repo / 'allowed.txt').write_text('changed while checking\n')
            (self.repo / 'new-untracked').write_text('new evaluated workspace input')
        finally:
            gate.touch(); worker.join(timeout=8)
        self.assertFalse(worker.is_alive())
        self.assertEqual('stale', results[0]['status'], results)
        self.assertEqual(b'x', counter.read_bytes())
        record = json.loads((run_dir / results[0]['execution_path']).read_text())
        self.assertEqual('passed', record['outcomes'][0]['status'])


    def test_partial_terminal_receipt_remains_unresolved_until_complete(self):
        controller, run_dir = self.create_initialized_run()
        fake = self.actor()
        reserved = self.reserve(run_dir)
        self.launch(controller, run_dir, reserved, fake)
        directory = run_dir / 'actors' / reserved['assignment']['operation_id']
        self.wait_file(directory / 'result.state.json')
        path = directory / 'result.state.json'
        controller.actor_lifecycle._ACTOR_SUPERVISORS[str(directory.resolve())].wait(timeout=8)
        raw = path.read_bytes()
        path.write_bytes(b'{')
        observation = controller.observe_operation(run_dir, reserved['assignment']['operation_id'])
        self.assertIn(observation['status'], {'running', 'unknown'})
        self.assertFalse(controller.status_run(run_dir)['readiness_current'])
        self.assertEqual('refused', self.reserve(run_dir, key='overlap')['status'])
        path.write_bytes(raw)
        self.assertEqual('terminal', self.terminal(controller, run_dir, reserved['assignment']['operation_id'])['status'])
        self.assertTrue(controller.status_run(run_dir)['readiness_current'])
        self.assertEqual(1, len(self.invocations(fake)))

    def test_producer_invalid_later_command_plans_before_launch(self):
        controller, run_dir, operation_id, counter = self.producer_run(extra_checks=["/bin/sh -c 'touch unauthorized'"])
        self.assertEqual('passed', controller.inspect_candidate(run_dir, operation_id)['status'])
        reserved = self.reserve(run_dir, 'verify', 'check')
        before = (run_dir / 'ledger.json').read_bytes()
        result = controller.check_candidate(run_dir, reserved['assignment'], timeout_seconds=5)
        self.assertEqual('refused', result['status'], result)
        self.assertEqual(before, (run_dir / 'ledger.json').read_bytes())
        self.assertFalse(counter.exists())
        self.assertFalse((self.repo / 'unauthorized').exists())

    def test_producer_missing_later_executable_blocks_before_any_command(self):
        controller, run_dir, operation_id, counter = self.producer_run(extra_checks=['/nonexistent/task-orchestrator-check'])
        self.assertEqual('passed', controller.inspect_candidate(run_dir, operation_id)['status'])
        reserved = self.reserve(run_dir, 'verify', 'check')
        result = controller.check_candidate(run_dir, reserved['assignment'], timeout_seconds=5)
        self.assertEqual('blocked', result['status'], result)
        self.assertIn('executable', result['blocker'].lower())
        self.assertFalse(counter.exists())
        self.assertEqual('unknown', controller.status_run(run_dir)['operation']['state'])

    def test_producer_log_collision_preserves_evidence_without_launch(self):
        controller, run_dir, operation_id, counter = self.producer_run()
        self.assertEqual('passed', controller.inspect_candidate(run_dir, operation_id)['status'])
        reserved = self.reserve(run_dir, 'verify', 'check')
        log = run_dir / 'verification' / (reserved['assignment']['operation_id']+'.turn-001.command-001.stdout.log')
        log.parent.mkdir(exist_ok=True)
        log.write_bytes(b'existing evidence')
        result = controller.check_candidate(run_dir, reserved['assignment'], timeout_seconds=5)
        self.assertEqual('blocked', result['status'], result)
        self.assertEqual(b'existing evidence', log.read_bytes())
        self.assertFalse(counter.exists())
    def interrupted_check(self, boundary):
        gate = self.root / 'release'
        done = self.root / 'child-done'
        waiting = self.root / 'waiting'
        setup = ''
        if boundary == 'during':
            setup = (f"\nimport time\nPath({str(waiting)!r}).touch()\n"
                     f"while not Path({str(gate)!r}).exists(): time.sleep(.01)\n"
                     f"Path({str(done)!r}).touch()\n")
        controller, run_dir, operation_id, counter = self.producer_run(setup)
        self.assertEqual('passed', controller.inspect_candidate(run_dir, operation_id)['status'])
        reserved = self.reserve(run_dir, 'verify', 'check')
        request = self.root / 'check-request.json'
        request.write_text(json.dumps(reserved['assignment']))
        source = r'''
import json,sys,time
from pathlib import Path
sys.path.insert(0,sys.argv[1]); import controller
run=Path(sys.argv[2]); assignment=json.loads(Path(sys.argv[3]).read_text())
if sys.argv[4]=='before':
    original=controller.run_records.save_actor_ledger
    def save(root,ledger):
        original(root,ledger)
        if ledger['actor_operations'][-1]['state']=='unknown':
            (run/'checkpoint').touch()
            while True: time.sleep(.01)
    controller.run_records.save_actor_ledger=save
controller.check_candidate(run,assignment,timeout_seconds=5)
'''
        process = subprocess.Popen([sys.executable, '-c', source, str(fixtures.CONTROLLER_PATH.parent), str(run_dir), str(request), boundary], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            self.wait_file(waiting if boundary == 'during' else run_dir / 'checkpoint')
            self.assertEqual('unknown', controller.status_run(run_dir)['operation']['state'])
        finally:
            process.kill(); process.communicate(timeout=5)
            gate.touch()
        if boundary == 'during':
            self.wait_file(done)
            self.assertEqual(b'x', counter.read_bytes())
        else:
            self.assertFalse(counter.exists())
        before = (run_dir / 'ledger.json').read_bytes()
        replay = load_controller().check_candidate(run_dir, reserved['assignment'], timeout_seconds=5)
        self.assertEqual('blocked', replay['status'], replay)
        self.assertEqual(before, (run_dir / 'ledger.json').read_bytes())
        self.assertEqual('refused', self.reserve(run_dir, 'verify', 'overlap')['status'])

    def test_producer_real_interruption_before_launch_stays_stopped(self):
        self.interrupted_check('before')

    def test_producer_real_interruption_during_command_stays_stopped(self):
        self.interrupted_check('during')

    def test_producer_refuses_hidden_staged_owner_change(self):
        owner = self.repo / 'owner.txt'
        owner.write_text('committed baseline\n')
        subprocess.run(['git', '-C', str(self.repo), 'add', 'owner.txt'], check=True)
        subprocess.run(['git', '-C', str(self.repo), 'commit', '-qm', 'owner baseline'], check=True)
        owner.write_text('owner staged\n')
        subprocess.run(['git', '-C', str(self.repo), 'add', 'owner.txt'], check=True)
        owner.write_text('owner worktree\n')
        controller, run_dir, operation_id, counter = self.producer_run()
        status_before = controller.capture_git_status(self.repo)['owner.txt']
        owner.write_text('changed staging\n')
        subprocess.run(['git', '-C', str(self.repo), 'add', 'owner.txt'], check=True)
        owner.write_text('owner worktree\n')
        self.assertEqual(status_before, controller.capture_git_status(self.repo)['owner.txt'])
        result = controller.inspect_candidate(run_dir, operation_id)
        self.assertEqual('blocked', result['status'], result)
        self.assertIn('owner.txt', result['paths'])
        self.assertFalse(counter.exists())

if __name__=='__main__':
    unittest.main()
