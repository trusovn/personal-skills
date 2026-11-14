"""Local actor executable construction for one controller fixture occurrence.

ActorFixture adds synthetic actor configuration/tool/dependency/skill files to
ControllerFixture. This fake exercises local protocol mechanics, not live model
judgment or sbx containment. Assertions and actor workflow orchestration remain
in test_actor_operations; this module never imports a test-case module.
"""
import json

from controller_fixture_support import ControllerFixture


class ActorFixture(ControllerFixture):
    """Build actor files under the occurrence root; mode values stay at call sites."""

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
    def after_run_lock_release(check, assignment):
        # Launch/observation can still own the lock after recording the session.
        # Other refusals are scenario outcomes and must propagate immediately.
        deadline = time.monotonic()+4
        while True:
            outcome = check(run, assignment, timeout_seconds=5)
            if outcome['status']!='refused' or 'owns this run' not in outcome.get('reason','') or time.monotonic()>=deadline:
                return outcome
            time.sleep(.01)
    rerun = None
    if mode.get('replay_verify'):
        replay=after_run_lock_release(controller.check_candidate,context['check_evidence']['assignment'])
        (root/'verify-replay.json').write_text(json.dumps(replay))
    if not mode.get('skip_rerun') and not mode.get('replay_verify'):
        rerun_assignment = dict(a,**mode.get('rerun_assignment',{}))
        rerun=after_run_lock_release(controller.check_collection,rerun_assignment)
        (root/'rerun.json').write_text(json.dumps(rerun))
    report={'coverage':{key:{'status':'passed','evidence':'inspected frozen '+key} for key in context['review_requirements']},'gaps':[],'findings':mode.get('findings',[]),'rerun_path':rerun.get('path') if rerun else None}
    if mode.get('replay_verify'): report['rerun_path']=context['check_evidence']['path']
    report.update(mode.get('report',{}))
    for key in mode.get('omit',[]): report.pop(key,None)
    result['collection']=report
    (root/'collected').touch()
if a['stage']=='acceptance':
    context = prompt['collection_context']
    decision = {'action':'accept','rationale':'Required evidence passes; no unresolved material risk',
                'evidence':context['evidence'],'dispositions':[], 'unfinished':[]}
    decision.update(mode.get('decision',{}))
    result['decision'] = decision
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
    for name,content in mode.get('edits',{}).items(): (Path.cwd()/name).write_text(content)
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

