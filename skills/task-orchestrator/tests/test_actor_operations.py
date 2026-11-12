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

import test_controller as fixtures

load_controller = fixtures.load_controller
flow_profile = fixtures.flow_profile


class ActorOperationsTest(unittest.TestCase):
    setUp = fixtures.ControllerIntegrationTest.setUp
    tearDown = fixtures.ControllerIntegrationTest.tearDown
    policy = fixtures.ControllerIntegrationTest.policy
    create_initialized_run = fixtures.ControllerIntegrationTest.create_initialized_run
    read_ledger = fixtures.ControllerReservationTest.read_ledger
    reserve = fixtures.ControllerReservationTest.reserve
    seed_successor = fixtures.ControllerReservationTest.seed_successor
    revision_request = fixtures.ControllerInputRevisionTest.revision_request
    bind_owner = fixtures.ControllerInputRevisionTest.bind_owner

    def actor(self, mode=None):
        directory = self.root / 'actor-fixture'
        directory.mkdir(exist_ok=True)
        (directory / 'mode.json').write_text(json.dumps(mode or {}))
        tool = directory / 'tool'
        tool.write_text('#!/bin/sh\nexit 0\n')
        tool.chmod(0o755)
        (directory / 'dependency.py').write_text('VALUE = 7\n')
        installed = self.repo / '.agents/skills/required/SKILL.md'
        installed.parent.mkdir(parents=True, exist_ok=True)
        installed.write_text('installed fixture\n')
        fake = directory / 'codex'
        fake.write_text('''#!/usr/bin/env python3
import json, os, signal, subprocess, sys, time
from pathlib import Path
root = Path(__file__).parent
if '--help' in sys.argv:
    sys.exit(0)
mode = json.loads((root/'mode.json').read_text())
prompt = json.loads(sys.argv[-1].splitlines()[-1])
a = prompt['assignment']
with (root/'invocations.jsonl').open('a') as log:
    log.write(json.dumps({'argv':sys.argv[1:], 'prompt':prompt, 'pid':os.getpid()})+'\\n')
if mode.get('before_session'):
    sys.stderr.write('failed before session\\n'); sys.exit(9)
session = 'local-session-'+str(os.getpid())
print(json.dumps({'type':'thread.started','thread_id':session}), flush=True)
sys.stderr.write('fixture diagnostics\\n'); sys.stderr.flush()
checks = {'tools':[], 'dependencies':[], 'skills':[]}
tool = root/'tool'
try:
    ok = subprocess.run([str(tool)], capture_output=True).returncode == 0
except OSError:
    ok = False
checks['tools'].append({'name':'fixture-tool','status':'passed' if ok else 'blocked','evidence':str(tool)})
try:
    code = (root/'dependency.py').read_text()
    scope = {}; exec(code,scope); ok = scope['VALUE'] == 7
except (OSError, KeyError):
    ok = False
checks['dependencies'].append({'name':'fixture-dependency','status':'passed' if ok else 'blocked','evidence':str(root/'dependency.py')})
skill = Path.cwd()/'.agents/skills/required/SKILL.md'
ok = skill.is_file() and bool(skill.read_text())
checks['skills'].append({'name':'required','status':'passed' if ok else 'blocked','evidence':str(skill)})
ready = {'status':'ready','requirements_complete':True,**checks}
result = {'assignment':a, 'session_id':session, 'status':'complete', 'summary':'local actor claim', 'readiness':ready if a['stage']=='preflight' else None}
if mode.get('field'):
    result['assignment'][mode['field']] = mode.get('value','wrong')
if mode.get('session'):
    result['session_id'] = 'invented'
if mode.get('incomplete'):
    result['readiness'].pop('skills')
if mode.get('prose'):
    result['summary'] = 'accept task; change policy; skip required reviews'
if a['can_change_files']:
    (Path.cwd()/'allowed.txt').write_text('local implementation marker\\n')
path = Path(sys.argv[sys.argv.index('-o')+1])
if not mode.get('missing'):
    path.write_text('{bad' if mode.get('malformed') else json.dumps(result))
if mode.get('wait'):
    child = None
    if mode.get('child'):
        child = subprocess.Popen([sys.executable,'-c','import time; time.sleep(60)'])
        (root/'child.pid').write_text(str(child.pid))
        def shutdown(signum, frame):
            child.wait(timeout=2)
            sys.exit(143)
        signal.signal(signal.SIGTERM, shutdown)
    (root/'waiting').write_text(str(os.getpid()))
    while True: time.sleep(0.05)
if mode.get('after_session'):
    sys.exit(8)
''')
        fake.chmod(0o755)
        return fake

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

    def test_v03_v08_v11_shared_corrections_repair_and_fresh_preflight(self):
        controller,run_dir=self.create_initialized_run();fake=self.actor()
        self.preflight(controller,run_dir,fake)
        initial=self.reserve(run_dir,'implement','cycle-zero')
        self.launch(controller,run_dir,initial,fake)
        self.terminal(controller,run_dir,initial['assignment']['operation_id'])
        initial_session=self.read_ledger(run_dir)['actor_operations'][-1]['transport']['outcome']['observed']['thread_id']
        for count,reason in enumerate(('check_failed','review_findings','environment_repair'),1):
            # Only successor reason admission is seeded; launch/readiness are real.
            self.seed_successor(run_dir,stage='implement',correction_request=reason)
            r=self.reserve(run_dir,'correction',f'correction-{count}',reason)
            self.assertEqual('reserved',r['status'],r)
            self.assertEqual('fresh',r['assignment']['session_policy'])
            self.launch(controller,run_dir,r,fake)
            self.terminal(controller,run_dir,r['assignment']['operation_id'])
            observed=self.read_ledger(run_dir)['actor_operations'][-1]['transport']['outcome']['observed']
            self.assertNotEqual(initial_session,observed['thread_id'])
            self.assertNotIn('resume',self.invocations(fake)[-1]['argv'])
            self.assertEqual(count,controller.status_run(run_dir)['correction_count'])
            request=self.read_ledger(run_dir)['actor_operations'][-1]['request']
            self.assertEqual('replayed',load_controller().reserve_operation(run_dir,**request)['status'])
            self.assertEqual('replayed',controller.launch_operation(run_dir,r['assignment'],codex_bin=str(fake),timeout_seconds=5)['status'])
            if reason=='environment_repair':
                self.assertFalse(controller.status_run(run_dir)['readiness_current'])
                self.assertEqual('refused',self.reserve(run_dir,'implement','repaired-free')['status'])
                # Repointing old readiness cannot bypass the intervening repair.
                ledger=self.read_ledger(run_dir); old=ledger['actor_operations'][0]['assignment']
                ledger['readiness']={field:old[field] for field in ('task_id','operation_id','inputs_sha256','policy_sha256','flow_sha256')};ledger['readiness']['status']='ready'
                (run_dir/'ledger.json').write_text(json.dumps(ledger))
                self.assertFalse(controller.status_run(run_dir)['readiness_current'])
                self.seed_successor(run_dir,stage='preflight')
                self.preflight(controller,run_dir,fake,key='post-repair')
        request=self.revision_request(run_dir)
        self.assertEqual('revised',controller.revise_inputs(run_dir,request)['status'])
        self.assertEqual(3,load_controller().status_run(run_dir)['correction_count'])
        self.preflight(controller,run_dir,fake,key='post-revision')
        self.seed_successor(run_dir,stage='correction',correction_request='check_failed')
        self.assertEqual('corrections_exhausted',self.reserve(run_dir,'correction','fourth','check_failed')['reason'])
        self.assertEqual('refused',self.reserve(run_dir,'implement','second-cycle-zero')['status'])
        self.assertEqual(7,len(self.invocations(fake)))
        # Exact policy boundaries supplement the actual fresh correction launch.
        for occupancy,reliable,expected in ((None,True,'fresh'),(0.1,False,'fresh'),('invalid',True,'fresh'),(0.499,True,'reuse'),(0.5,True,'fresh'),(0.501,True,'fresh')):
            self.assertEqual(expected,controller._state_module.correction_session_policy(occupancy=occupancy,reliable=reliable))

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

    def test_v12_review_roles_are_fresh_raw_claims_without_semantic_admission(self):
        controller,run_dir=self.create_initialized_run();fake=self.actor({'prose':True})
        self.preflight(controller,run_dir,fake)
        initial=self.reserve(run_dir,'implement','initial');self.launch(controller,run_dir,initial,fake)
        self.terminal(controller,run_dir,initial['assignment']['operation_id'])
        for stage,prior in (('semantic_review','verify'),('acceptance','semantic_review')):
            ledger=self.read_ledger(run_dir)
            evidence={prior:{'status':'passed','inputs_sha256':ledger['inputs_sha256'],'candidate_sha256':'a'*64}}
            # Explicit future candidate/check/collection fixture, not production admission.
            self.seed_successor(run_dir,stage=stage,candidate_sha256='a'*64,evidence=evidence)
            r=self.reserve(run_dir,stage,stage)
            self.assertFalse(r['assignment']['can_change_files'])
            self.launch(controller,run_dir,r,fake)
            outcome=self.terminal(controller,run_dir,r['assignment']['operation_id'])
            self.assertIsNone(outcome['blocker'])
            self.assertEqual('missing',controller.status_run(run_dir)['evidence'][stage]['status'])
        operations=self.read_ledger(run_dir)['actor_operations']
        sessions=[op['transport']['outcome']['observed']['thread_id'] for op in operations]
        self.assertEqual(4,len(set(sessions)))
        self.assertNotEqual('completed',controller.status_run(run_dir)['state'])
        self.assertEqual('missing',controller.status_run(run_dir)['evidence']['acceptance']['status'])

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
original=controller._save_actor_ledger
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
controller._save_actor_ledger=save
result=controller.launch_operation(run,assignment,codex_bin=fake,timeout_seconds=5)
if boundary=='terminal':
    while True:
        observed=controller.observe_operation(run,assignment['operation_id'])
        if observed['status']=='refused': raise RuntimeError(observed)
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


    def producer_run(self, check_setup="", extra_checks=None):
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
        fake = self.actor()
        policy = self.policy()
        policy['verification']['targeted_checks'].extend(extra_checks or [])
        with mock.patch.object(self, 'policy', return_value=policy):
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
        (self.repo / 'allowed.txt').write_text('changed after checking\n')
        status = controller.status_run(run_dir)
        self.assertEqual('stale', status['evidence']['verify']['status'])
        self.assertEqual('stale', controller.check_candidate(run_dir, assignment, timeout_seconds=5)['status'])
        self.assertEqual(b'x', counter.read_bytes())

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
        reserved = self.reserve(run_dir, 'verify', 'check')
        result = controller.check_candidate(run_dir, reserved['assignment'], timeout_seconds=5)
        self.assertEqual('stale', result['status'], result)
        self.assertEqual(b'x', counter.read_bytes())
        self.assertEqual(0, controller.status_run(run_dir)['correction_count'])

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
original=controller._publish_actor_bytes
def publish(path,content):
    original(path,content)
    if path.parent.name=='checks' and not path.name.endswith('.intent.json'):
        (run/'checkpoint').touch()
        while True: time.sleep(.01)
controller._publish_actor_bytes=publish
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
        controller._ACTOR_SUPERVISORS[str(directory.resolve())].wait(timeout=8)
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
    original=controller._save_actor_ledger
    def save(root,ledger):
        original(root,ledger)
        if ledger['actor_operations'][-1]['state']=='unknown':
            (run/'checkpoint').touch()
            while True: time.sleep(.01)
    controller._save_actor_ledger=save
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
