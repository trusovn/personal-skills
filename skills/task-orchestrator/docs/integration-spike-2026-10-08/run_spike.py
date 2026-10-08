"""One-task, sequential integration experiment; not a production orchestrator.

Run setup, then run. All actor launches and ordinary advancement are code-owned.
No model grades, automatic corrections, commits of implementation, or publishing.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[3]
REPO = Path('/private/tmp/task-flow-spike-2026-10-08')
OUT = HERE / 'evidence'
TASK = 'docs/tasks/SYN-01'
STAGES = [
    ('brief', 'task-brief-designer', f'Create {TASK}/brief.md from authority.md using high-assurance mode. Do not create a plan. The user mandates a separate verification-design pass for this integration test. Dependencies: dependencies.json. Run policy: run-policy.json.'),
    ('verification', 'task-verification-designer', f'Read {TASK}/brief.md and write {TASK}/verification.md.'),
    ('preflight', 'task-preflight', f'High-assurance mode. Brief: {TASK}/brief.md. Verification: {TASK}/verification.md. Policy: run-policy.json. Dependencies: dependencies.json. Write the canonical {TASK}/preflight.md. Cheap baseline checks are authorized.'),
    ('implementation', 'bounded-task-implementer', f'High-assurance mode. Consume {TASK}/preflight.md and its inputs. Worker schema: worker-result.schema.json. Return exactly one schema-conforming JSON object; the transport saves it as the durable runtime result. The required maintainability and registry stages run separately before functional acceptance. Do not invoke any other stage.'),
    ('maintainability', 'task-maintainability-review', f'Independent session. Review current production bytes against {TASK}/brief.md. Policy: run-policy.json. Implementer result: {OUT}/implementation.last.txt. Write {TASK}/reviews/maintainability-01.md. Do not change other repository files.'),
    ('registry', 'task-contract-registry-updater', f'Read {TASK}/brief.md, {TASK}/reviews/maintainability-01.md, and {OUT}/implementation.last.txt. Synchronize docs/contracts/catalog.json, regenerate the index with the canonical validator, and update stale README.md discovery claims. Do not change production or tests.'),
    ('acceptance', 'task-acceptance-review', f'High-assurance independent review. Brief: {TASK}/brief.md; ready packet: {TASK}/preflight.md; policy: run-policy.json; worker result: {OUT}/implementation.last.txt. Baseline: preflight packet. Maintainability accepted the current production bytes; focus on behavior and contract consistency. Write {TASK}/reviews/acceptance-01.md. Do not change other repository files.'),
]


def command(args, cwd=REPO):
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=True).stdout


def put(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def snapshot():
    return {str(p.relative_to(REPO)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in REPO.rglob('*') if p.is_file() and '.git' not in p.relative_to(REPO).parts}


def setup():
    if REPO.exists():
        raise SystemExit(f'Refusing to overwrite {REPO}')
    REPO.mkdir()
    OUT.mkdir(exist_ok=True)
    command(['git', 'init', '-q'])
    command(['git', 'config', 'user.name', 'Synthetic Flow Spike'])
    command(['git', 'config', 'user.email', 'spike@example.invalid'])
    command(['git', 'commit', '--allow-empty', '-qm', 'Initialize synthetic Git history'])
    put(REPO / '.gitignore', '__pycache__/\n*.pyc\n.run-evidence/\n')
    put(REPO / 'catalog.py', 'def select_names(names):\n    """Return all names in input order, preserving duplicates."""\n    return list(names)\n')
    put(REPO / 'tests/__init__.py', '')
    put(REPO / 'tests/test_catalog.py', 'import unittest\nfrom catalog import select_names\n\nclass CatalogTests(unittest.TestCase):\n    def test_default(self):\n        names = ["Bee", "ant", "Bee"]\n        self.assertEqual(select_names(names), names)\n        self.assertEqual(names, ["Bee", "ant", "Bee"])\n')
    put(REPO / 'tools/check_architecture.py', 'import ast\nfrom pathlib import Path\nmodule = ast.parse(Path("catalog.py").read_text())\nassert not any(isinstance(n, (ast.Import, ast.ImportFrom)) for n in ast.walk(module)), "catalog must stay dependency-free"\nprint("Architecture gate passed")\n')
    shutil.copy2(SOURCE / 'skills/repo-foundation/scripts/check_contracts.py', REPO / 'tools/check_contracts.py')
    put(REPO / 'README.md', '# Synthetic catalog\n\nPublic API: `catalog.select_names(names)` returns all names in input order, preserving duplicates. The input list is unchanged.\n\nContract discovery: `docs/contracts/index.json`.\n')
    registry = {'schema_version': 1, 'id': 'catalog', 'owner_paths': ['catalog.py'], 'provides': [{'name': 'select_names', 'kind': 'function', 'summary': 'Return all names in input order, preserving duplicates.', 'declarations': ['catalog.py']}], 'invariants': [{'statement': 'The input list is unchanged.'}], 'module_docs': ['README.md']}
    put(REPO / 'docs/contracts/catalog.json', json.dumps(registry, indent=2)+'\n')
    put(REPO / f'{TASK}/reviews/.gitkeep', '')
    put(REPO / 'dependencies.json', '{"SYN-01": []}\n')
    put(REPO / 'AGENTS.md', '# Synthetic fixture authority\n\nUse project-local skills and sibling shared helpers. All stages are sequential and launched by code; never spawn agents. All actors use gpt-5.6-terra with medium reasoning. Implementer may change only catalog.py and tests/test_catalog.py. Independent maintainability review is required before registry update and acceptance. Architecture command: `PYTHONDONTWRITEBYTECODE=1 python3 tools/check_architecture.py`. Registry commands: `PYTHONDONTWRITEBYTECODE=1 python3 tools/check_contracts.py --root . --write-index` and the same without --write-index. These are cheap local checks, authorized. Source, tests, and executable contracts are owned by implementation. Registry updater owns docs/contracts/** and stale README.md claims. Read authority.md and run-policy.json for stage artifact permissions. Do not edit authority, policy, dependencies, skills, tools, or plans. No network, package installation, destructive actions, or actor commits.\n')
    put(REPO / 'authority.md', '# Approved synthetic task SYN-01\n\nExtend the public Python function catalog.select_names to select_names(names, prefix=""). Inputs are a list of strings and a string prefix; invalid input types are outside scope. Retain names whose value starts with prefix using case-sensitive matching. Preserve input order and duplicates; do not mutate the input. Default and empty prefix return all names; no matches and empty input return an empty list. Do not add other behavior.\n\nImplementer owns catalog.py and tests/test_catalog.py. Task brief is docs/tasks/SYN-01/brief.md. Explicitly run all seven task-flow skills for the integration experiment, including separate verification design, standalone high-assurance preflight, independent maintainability review, registry update, and independent acceptance. The public API is a durable cross-task contract, so the updater must synchronize the catalog record and stale README usage. Tests: PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_catalog -v. Owning suite: PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v. No broader suite is needed. Registry validator checks structure and paths; it does not prove API behavior. Dependencies are empty. No plan or governing product direction applies.\n')
    policy = {'id': 'synthetic-flow-spike-v1', 'profile': 'high-assurance', 'task_id': 'SYN-01', 'repository': str(REPO), 'implementation_paths': ['catalog.py','tests/test_catalog.py'], 'preparation_artifacts': [f'{TASK}/brief.md', f'{TASK}/verification.md'], 'preflight_artifact': f'{TASK}/preflight.md', 'maintainability_artifact': f'{TASK}/reviews/maintainability-01.md', 'acceptance_artifact': f'{TASK}/reviews/acceptance-01.md', 'registry_paths': ['docs/contracts/catalog.json','docs/contracts/index.json','README.md'], 'runtime_output_directory': str(OUT), 'worker_schema': 'worker-result.schema.json', 'worker_result': str(OUT/'implementation.last.txt'), 'network': False, 'dependency_installation': False, 'actor_commits': False, 'controller_preparation_commit': True, 'cheap_local_checks': True, 'instrumentation': 'optional; use same-installation helper only when applicable'}
    put(REPO / 'run-policy.json', json.dumps(policy, indent=2)+'\n')
    shutil.copy2(SOURCE / 'skills/task-orchestrator/assets/worker-result.schema.json', REPO / 'worker-result.schema.json')
    command([sys.executable, str(SOURCE / 'scripts/install_development_skills.py'), str(REPO)])
    command([sys.executable, 'tools/check_contracts.py', '--root', '.', '--write-index'])
    command(['git','add','.'])
    command(['git','commit','-qm','Synthetic fixture baseline'])
    installed = {str(p.relative_to(REPO)): hashlib.sha256(p.read_bytes()).hexdigest() for p in (REPO/'.agents').rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    put(OUT/'installed-manifest.json', json.dumps(installed,indent=2)+'\n')
    print(f'Setup complete: {REPO}', flush=True)


def check_stage(name, before, after):
    changed = sorted(p for p in set(before)|set(after) if before.get(p)!=after.get(p))
    allowed = {'brief': [f'{TASK}/brief.md'], 'verification': [f'{TASK}/verification.md'], 'preflight': [f'{TASK}/preflight.md'], 'implementation': ['catalog.py','tests/test_catalog.py'], 'maintainability': [f'{TASK}/reviews/maintainability-01.md'], 'registry': ['docs/contracts/catalog.json','docs/contracts/index.json','README.md'], 'acceptance': [f'{TASK}/reviews/acceptance-01.md']}[name]
    unexpected = [p for p in changed if p not in allowed and not p.startswith('.run-evidence/') and '__pycache__' not in Path(p).parts]
    if unexpected:
        raise ValueError(f'Unauthorized changed paths: {unexpected}')
    output = (OUT/f'{name}.last.txt').read_text()
    if name in ('brief','preflight','verification'):
        path = REPO / allowed[0]
        text = path.read_text()
        expected = 'ready_for_preflight' if name == 'brief' else 'ready'
        if not re.search(r'^Status:\s*`?'+expected+r'`?\s*$',text,re.M):
            raise ValueError(f'Cannot mechanically confirm {expected} in {path}')
    elif name == 'implementation':
        sys.path.insert(0,str(SOURCE/'skills/task-orchestrator/scripts'))
        from codex_worker import result_status
        if result_status(OUT/f'{name}.last.txt') != 'complete' or json.loads(output)['task_id'] != 'SYN-01':
            raise ValueError('Implementation did not submit a valid complete worker result for SYN-01')
    elif name == 'maintainability':
        text = (REPO/allowed[0]).read_text()
        if not re.search(r'^VERDICT:\s*ACCEPT\s*$',text,re.M):
            raise ValueError('Maintainability did not emit exact ACCEPT contract')
    elif name == 'registry':
        if not re.search(r'^REFERENCE_UPDATE:\s*(UPDATED|NO_UPDATE_NEEDED)\s*$',output,re.M):
            raise ValueError('Registry did not emit exact successful status contract')
    else:
        text = (REPO/allowed[0]).read_text()
        if not re.search(r'^\| Verdict \| `?ACCEPT`? \|\s*$',text,re.M):
            raise ValueError('Acceptance did not emit an ACCEPT report')
    return changed


def run(retry_transport=False, model='gpt-5.6-terra'):
    ledger_path = OUT/'ledger.json'
    ledger = json.loads(ledger_path.read_text()) if ledger_path.exists() else []
    if retry_transport:
        row = ledger[-1]
        if row['before'] != row['after'] or row['exit_code'] != 1:
            raise SystemExit('Transport retry requires unchanged fixture and exit 1')
        archive = OUT / f'transport-attempt-{1+len(list(OUT.glob("transport-attempt-*")))}'
        archive.mkdir()
        for suffix in ('events.jsonl','stderr.txt','prompt.txt'):
            shutil.copy2(OUT/f'{row["stage"]}.{suffix}',archive/f'{row["stage"]}.{suffix}')
        put(archive/'ledger.json',json.dumps(ledger,indent=2)+'\n')
        ledger.pop()
    if ledger and ledger[-1].get('gate') != 'passed':
        raise SystemExit('Previous gate stopped; investigate explicitly. No automatic retry.')
    for name, skill, instruction in STAGES[len(ledger):]:
        before = snapshot()
        status_before = command(['git','status','--short'])
        prompt = f'You are one bounded stage actor in an integration test. Work only in {REPO}. Read AGENTS.md, authority.md, and run-policy.json. Apply the unmodified project-local skill at .agents/skills/task-implementation-flow/{skill}/SKILL.md and its relevant references. Never use a global copy or spawn agents. {instruction} End your invocation at the skill handoff. Do not manage the next stage. Runtime model {model} and reasoning medium are supplied by the caller.'
        put(OUT/f'{name}.prompt.txt',prompt+'\n')
        args = ['codex','--ask-for-approval','never','exec','--model',model,'--config','model_reasoning_effort="medium"','--sandbox','workspace-write','--cd',str(REPO),'--json','--output-last-message',str(OUT/f'{name}.last.txt'),'-']
        if name == 'implementation':
            args[args.index('-'):args.index('-')] = ['--output-schema',str(REPO/'worker-result.schema.json')]
        print(f'START {name}: {model} / medium',flush=True)
        with (OUT/f'{name}.events.jsonl').open('w') as events, (OUT/f'{name}.stderr.txt').open('w') as err:
            result = subprocess.run(args,input=prompt,text=True,stdout=events,stderr=err,timeout=900)
        row = {'stage':name,'skill':skill,'model':model,'reasoning':'medium','launch_argv':args,'exit_code':result.returncode,'status_before':status_before,'status_after':command(['git','status','--short']),'before':before,'after':snapshot()}
        try:
            if result.returncode:
                raise ValueError(f'Actor exited {result.returncode}')
            row['changed_paths'] = check_stage(name,before,row['after'])
            row['gate'] = 'passed'
        except (ValueError,OSError,json.JSONDecodeError) as exc:
            row['gate'] = 'stopped'
            row['reason'] = str(exc)
        ledger.append(row)
        put(ledger_path,json.dumps(ledger,indent=2)+'\n')
        print(f'END {name}: {row["gate"]} {row.get("reason","")}',flush=True)
        if row['gate'] != 'passed':
            return 2
        if name == 'verification':
            command(['git','add',f'{TASK}/brief.md',f'{TASK}/verification.md'])
            command(['git','commit','-qm','Freeze approved synthetic task preparation'])
        if name == 'implementation':
            for label,cmd in [('behavior',['python3','-m','unittest','discover','-s','tests','-v']),('architecture',['python3','tools/check_architecture.py'])]:
                result = subprocess.run(cmd,cwd=REPO,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},text=True,capture_output=True)
                put(OUT/f'controller-{label}.txt',result.stdout+result.stderr)
                if result.returncode:
                    raise SystemExit(f'Controller {label} failed; stop')
    print('All seven actor stages passed the experiment gates.',flush=True)
    return 0


if __name__ == '__main__':
    if sys.argv[1:] == ['setup']:
        setup()
    elif len(sys.argv) >= 2 and sys.argv[1] == 'run':
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument('action',choices=['run'])
        parser.add_argument('--retry-transport',action='store_true')
        parser.add_argument('--model',default='gpt-5.6-terra')
        args = parser.parse_args()
        raise SystemExit(run(retry_transport=args.retry_transport,model=args.model))
    else:
        raise SystemExit('Usage: run_spike.py setup|run')
