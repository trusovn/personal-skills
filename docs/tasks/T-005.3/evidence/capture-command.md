# Local capture command

Implementation evidence only. No reviewer call, role runner, or aggregate gate.
Run from the source repository root with `python3 /tmp/opencode/t0053/capture_local.py`.
The script refuses to overwrite staged roots. The retained script below reproduces
the final capture in fresh roots; the initial probes were rerun after moving their
state inputs outside the fixture Git roots. The rerun used the definitions before
`records = []`, read records from `staging.json`, then executed from `probes = []`.
The snapshots were not overwritten. Final `public-probes.json` is the rerun output.

```python
import hashlib, json, os, subprocess, tarfile
from pathlib import Path

repo = Path.cwd()
evidence = repo / 'docs/tasks/T-005.3/evidence'
work = Path('/tmp/opencode/t0053/cases')
flow = 'skills/task-implementation-flow/'
plans = {
    'task-review-discovery': ['queue-defect', 'discovery-correction-gate', 'exporter-accept', 'exporter-restaged-stale', 'discovery-late-omission-clean', 'discovery-late-omission-fail', 'authored-production-self-check', 'discovery-prepared-ledger'],
    'task-acceptance-review': ['contextual-risk-blockers-decision', 'contextual-risk-mitigated-decision', 'mixed-conditions-authorized-decision', 'mixed-conditions-forbidden-decision', 'consequential-uncertainty-decision', 'consequential-uncertainty-resolved-decision', 'serious-delay-uncertainty-decision', 'serious-delay-uncertainty-resolved-decision', 'known-issue-proposed-work-decision', 'known-issue-committed-work-decision', 'known-issue-no-links-decision', 'correction-regression-decision', 'repeated-review-formerly-blocked-evidence-decision', 'repeated-review-missed-existing-obligation-decision', 'repeated-review-changed-context-authority-decision', 'repeated-review-newly-demonstrated-material-risk-decision'],
}

def run(args, cwd=repo, env=None):
    r = subprocess.run(args, cwd=cwd, env=env, capture_output=True, text=True)
    return {'argv': args, 'cwd': str(cwd), 'exit': r.returncode, 'stdout': r.stdout, 'stderr': r.stderr}

def identity(root):
    return {name: run(['git', *args], root) for name, args in [('head', ['rev-parse', 'HEAD']), ('status', ['status', '--short']), ('index', ['ls-files', '--stage']), ('diff', ['diff']), ('cached_diff', ['diff', '--cached'])]}

records = []
for role, scenarios in plans.items():
    fixture = flow + role + '/evals/files/setup_fixture.py'
    for scenario in scenarios:
        target = work / scenario
        if target.exists():
            raise RuntimeError('refuse to overwrite ' + str(target))
        env = dict(os.environ, EVAL_WORK_ROOT=str(target), PYTHONDONTWRITEBYTECODE='1')
        setup = run(['python3', fixture, scenario], env=env)
        record = {'scenario': scenario, 'fixture': fixture, 'environment': {'EVAL_WORK_ROOT': str(target), 'PYTHONDONTWRITEBYTECODE': '1'}, 'setup': setup, 'role_calls': 'unrun; coordinator owns separate sessions'}
        records.append(record)
        if setup['exit']:
            (evidence / 'staging.json').write_text(json.dumps(records, indent=2)+'\n')
            raise RuntimeError(setup)
        roots = sorted(p.parent for p in target.rglob('.git') if p.is_dir())
        record['identities'] = {str(p.relative_to(target)): identity(p) for p in roots}
        record['files'] = {str(p.relative_to(target)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(target.rglob('*')) if p.is_file()}
        archive = evidence / (scenario + '.tar.gz')
        with tarfile.open(archive, 'w:gz') as tar:
            tar.add(target, arcname=scenario)
        record['snapshot'] = {'path': str(archive.relative_to(repo)), 'sha256': hashlib.sha256(archive.read_bytes()).hexdigest(), 'timing': 'after setup, before implementation probes; includes Git history/index'}
        (evidence / 'staging.json').write_text(json.dumps(records, indent=2)+'\n')
        print(scenario, 'staged and captured', flush=True)

probes = []
for scenario, folder, expected in [('queue-defect', 'queue-runner', ['TASK-1', '']), ('discovery-correction-gate', 'corrected-queue', ['TASK-1', 'TASK-2'])]:
    root = work / scenario / folder
    state = work / scenario / 'implementation-probe.json'
    initial = {'tasks': [{'id': 'TASK-1', 'status': 'ready'}, {'id': 'TASK-2', 'status': 'ready'}]}
    state.write_text(json.dumps(initial))
    calls = []
    for _ in range(2):
        r = run(['python3', '-m', 'src.queue.run_next', str(state)], root, dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
        r['state_after'] = json.loads(state.read_text())
        calls.append(r)
    passed = all(r['exit'] == 0 for r in calls) and [r['stdout'].strip() for r in calls] == expected
    probes.append({'scenario': scenario, 'boundary': 'two actual public invocations with persisted state', 'initial': initial, 'expected_claims': expected, 'calls': calls, 'qualification_probe_pass': passed, 'fixture_defect': scenario == 'queue-defect'})
    state.unlink()
for scenario, expected in [('discovery-late-omission-clean', {'valid':0, 'boolean':2, 'older-attempt':2, 'second-running':2}), ('discovery-late-omission-fail', {'valid':0, 'boolean':0, 'older-attempt':2, 'second-running':2})]:
    root = work / scenario / 'late-omission'
    valid = json.loads((root / 'cases/valid.json').read_text())
    second = json.loads(json.dumps(valid)); second['tasks'][1]['status'] = 'running'
    variants = {'valid':valid, 'boolean':dict(valid,revision=True), 'older-attempt':dict(valid,active_attempt_id='A-1'), 'second-running':second}
    calls = {}
    for name, data in variants.items():
        state = work / scenario / 'implementation-probe.json'; state.write_text(json.dumps(data))
        calls[name] = {'input':data, **run(['python3','-m','src.ledger.validate',str(state)], root, dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))}
        state.unlink()
    probes.append({'scenario':scenario,'boundary':'public validator exits for valid and targeted invalid instances','expected_exits':expected,'calls':calls,'qualification_probe_pass':{n:r['exit'] for n,r in calls.items()}==expected,'fixture_defect':scenario.endswith('-fail')})
(evidence / 'public-probes.json').write_text(json.dumps(probes,indent=2)+'\n')
assert all(p['qualification_probe_pass'] for p in probes), probes
for record in records:
    target = work / record['scenario']
    after = {str(p.relative_to(target)):hashlib.sha256(p.read_bytes()).hexdigest() for p in target.rglob('*') if p.is_file()}
    assert after == record['files'], record['scenario']
print('24 immutable staged snapshots; 4 public probe contrasts matched; disposable bytes restored')
```
