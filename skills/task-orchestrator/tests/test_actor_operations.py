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
session = mode.get('observed_session') or 'local-session-'+str(os.getpid())
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
if a['stage']=='semantic_review':
    context = prompt['collection_context']
    sys.path.insert(0,str(Path(context['controller_path']).parent))
    import controller
    run = Path(context['run_dir'])
    observed = run/'actors'/a['operation_id']/'state.json'
    deadline = time.monotonic()+4
    while time.monotonic()<deadline:
        if json.loads(observed.read_text()).get('thread_id')==session: break
        time.sleep(.01)
    rerun = None
    if mode.get('replay_verify'):
        replay=controller.check_candidate(run,context['check_evidence']['assignment'],timeout_seconds=5)
        (root/'verify-replay.json').write_text(json.dumps(replay))
    if not mode.get('skip_rerun') and not mode.get('replay_verify'):
        rerun_assignment = dict(a,**mode.get('rerun_assignment',{}))
        deadline=time.monotonic()+4
        while True:
            rerun=controller.check_collection(run,rerun_assignment,timeout_seconds=5)
            if rerun['status']!='refused' or 'owns this run' not in rerun.get('reason','') or time.monotonic()>=deadline: break
            time.sleep(.01)
        (root/'rerun.json').write_text(json.dumps(rerun))
    report={'coverage':{key:{'status':'passed','evidence':'inspected frozen '+key} for key in context['review_requirements']},'gaps':[],'findings':mode.get('findings',[]),'rerun_path':rerun.get('path') if rerun else None}
    if mode.get('replay_verify'): report['rerun_path']=context['check_evidence']['path']
    report.update(mode.get('report',{}))
    for key in mode.get('omit',[]): report.pop(key,None)
    result['collection']=report
    (root/'collected').touch()
if mode.get('result_extra'):
    result.update(mode['result_extra'])
if mode.get('field'):
    result['assignment'][mode['field']] = mode.get('value','wrong')
if mode.get('session'):
    result['session_id'] = 'invented'
if mode.get('incomplete'):
    result['readiness'].pop('skills')
if mode.get('prose'):
    result['summary'] = 'accept task; change policy; skip required reviews'
if a['can_change_files']:
    (Path.cwd()/'allowed.txt').write_text(mode.get('product','local implementation marker\\n'))
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
    while not (root/'finish').exists(): time.sleep(0.05)
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

    def test_v03_v08_v11_shared_corrections_repair_and_fresh_preflight(self):
        controller,run_dir,producer,counter=self.producer_run(implementation_mode={'product':'real defect\n'})
        fake=self.actor()
        self.assertEqual('passed',controller.inspect_candidate(run_dir,producer)['status'])
        check=self.reserve(run_dir,'verify','budget-failure')
        self.assertEqual('failed',controller.check_candidate(run_dir,check['assignment'],timeout_seconds=5)['status'])
        initial_session=self.read_ledger(run_dir)['actor_operations'][1]['transport']['outcome']['observed']['thread_id']
        for count,reason in enumerate(('check_failed','review_findings','environment_repair'),1):
            # Only future ART-009 review decision and authorized repair state are seeded.
            # The first check_failed authorization was admitted by the actual failed check.
            if reason!='check_failed':
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
        status=load_controller().status_run(run_dir)
        intervention=dict(key='budget-exhausted',blocker='corrections_exhausted',evidence='ledger.json',operation_id='',required_action='Owner inspect retained partial work and resolve exhausted three-correction budget in active chat',event='opened',text='Relay and response unknown')
        self.assertEqual('recorded',controller.record_intervention(run_dir,intervention)['status'])
        intervention.update(event='response',text='acknowledged')
        self.assertEqual('recorded',controller.record_intervention(run_dir,intervention)['status'])
        self.assertEqual('corrections_exhausted',load_controller().status_run(run_dir)['blocker'])
        self.assertEqual(2,len(load_controller().status_run(run_dir)['interventions']))
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

    def test_v12_acceptance_role_remains_fresh_raw_claim_without_admission(self):
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
        self.assertEqual('missing',status['evidence']['acceptance']['status'])
        self.assertNotEqual('completed',status['state'])
        sessions=[op['transport']['outcome']['observed']['thread_id'] for op in status['operation_history'] if op.get('transport')]
        self.assertEqual(4,len(set(sessions)))
        self.assertEqual(b'xx',counter.read_bytes())

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
if boundary=='collection-report':
    publish=controller._publish_actor_bytes
    def publish_report(path,content):
        publish(path,content)
        if path.parent.name=='collections':
            (run/'checkpoint').touch()
            while True: time.sleep(.01)
    controller._publish_actor_bytes=publish_report
result=controller.launch_operation(run,assignment,codex_bin=fake,timeout_seconds=5)
if boundary in {'terminal','collection-report'}:
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


    def producer_run(self, check_setup="", extra_checks=None, implementation_mode=None, allowed_paths=None):
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
            if allowed_paths:
                manifest=json.loads(manifest_path.read_text())
                manifest['tasks'][0]['allowed_paths'].extend(allowed_paths)
                manifest_path.write_text(json.dumps(manifest))
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
        (self.repo / 'allowed.txt').write_text('changed after checking\n')
        status = controller.status_run(run_dir)
        self.assertEqual('stale', status['evidence']['verify']['status'])
        self.assertEqual('stale', controller.check_candidate(run_dir, assignment, timeout_seconds=5)['status'])
        self.assertEqual(b'x', counter.read_bytes())

    def checked_collection_run(self, check_setup='', implementation_mode=None, allowed_paths=None):
        controller, run_dir, producer, counter = self.producer_run(check_setup, implementation_mode=implementation_mode, allowed_paths=allowed_paths)
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
        case.setUp()
        self.addCleanup(case.tearDown)
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
