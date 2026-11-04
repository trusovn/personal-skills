"""Prepare finite independent-review inputs; never simulate a reviewer decision.

Reuse the author fixture through an explicit source-distribution subprocess.
Only disposable targets are installed. Oracle records stay outside reviewer scope.
"""

import ast
import hashlib
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys


HERE = Path(__file__).resolve().parent
CASES = json.loads((HERE / 'review_cases.json').read_text())
SOURCE = Path(os.environ.get('EVAL_SOURCE_ROOT', HERE.parents[4])).resolve()
PYTHON = Path(os.environ.get('EVAL_MEASUREMENT_PYTHON', sys.executable)).absolute()
WORK = Path(os.environ.get('EVAL_WORK_ROOT', '/work'))
BASE = '.quality/reports/B.json'
SCOPES = ['src', 'tests', 'evals', 'fixtures', 'harness', 'empty']


def write(root, name, value):
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding='utf-8')


def record(root, *command, expected=0):
    result = subprocess.run([str(p) for p in command], cwd=root,
                            text=True, capture_output=True)
    history = WORK / 'task-runs/commands.jsonl'
    history.parent.mkdir(parents=True, exist_ok=True)
    with history.open('a') as stream:
        stream.write(json.dumps(dict(cwd=str(root), command=list(map(str, command)),
                                     exit_code=result.returncode, stdout=result.stdout,
                                     stderr=result.stderr)) + '\n')
    if expected is not None and result.returncode != expected:
        raise RuntimeError(f'{command}: {result.returncode}\n{result.stdout}\n{result.stderr}')
    return result


def measure(root, output, baseline=BASE, operation='compare', paths=None):
    command = [PYTHON, root / '.agents/scripts/measure_maintainability.py',
               operation, *(paths or json.loads((root / baseline).read_text())['identity']['scope_directories']),
               '--root', root, '--output', output]
    if operation == 'compare':
        command += ['--baseline', baseline]
    return record(root, *command)


def snapshot(root):
    paths = [p for name in SCOPES + ['outside'] for p in (root / name).rglob('*') if p.is_file()]
    paths += [root / '.git/index']
    paths += [p for p in (root / '.quality/reports').glob('*') if p.is_file()]
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in paths if '__pycache__' not in p.parts}


def seed(case):
    if 'legacy' in case:
        record(WORK, sys.executable, HERE / 'setup_fixture.py', case['legacy'])
        root = next(p for p in WORK.glob('maintainability*') if p.is_dir())
        record(root, sys.executable, SOURCE / 'scripts/install_development_skills.py', root)
        # Capture the actual committed before code, then restore actual submitted
        # bytes. This is labeled fixture preparation, never a reviewer recapture.
        changed = {str(p.relative_to(root)): p.read_bytes() for folder in ('src', 'tests')
                   for p in (root / folder).rglob('*.py')}
        for name in changed:
            old = record(root, 'git', 'show', f'HEAD:{name}', expected=None)
            if old.returncode == 0:
                write(root, name, old.stdout)
            else:
                (root / name).unlink()
        measure(root, BASE, operation='baseline', paths=['src', 'tests'])
        for name, data in changed.items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        if case['scenario'] in ('V-08b', 'V-08c'):
            corrected = (root / 'src/billing/pricing.py').read_text()
            write(root, 'inputs/corrected-pricing.txt', corrected)
            constants = ast.parse((HERE / 'setup_fixture.py').read_text())
            changed_pricing = next(ast.literal_eval(node.value) for node in constants.body
                                   if isinstance(node, ast.Assign)
                                   and any(isinstance(name, ast.Name) and name.id == 'PRICING_CHANGED' for name in node.targets))
            write(root, 'src/billing/pricing.py', changed_pricing)
    else:
        author = SOURCE / 'skills/task-implementation-flow/bounded-task-implementer/evals/files/setup_fixture.py'
        record(WORK, sys.executable, author, 'measurement:' + case['seed'])
        root = WORK / 'measurement-fixture'
        desired = root / 'inputs/desired.txt'
        # The author fixture's ordinary entry cases stop before the edit. Review
        # starts at the submitted bytes; fault cases already changed them.
        if case['scenario'] == 'V-01d':
            write(root, 'tests/sample.py', 'def sample():\n    assert 1 == 1\n')
        elif case['seed'].startswith(('V-03', 'V-04', 'V-07', 'V-09')):
            write(root, 'src/logic.py', desired.read_text())
        if case['scenario'] in ('V-01a', 'V-01e'):
            write(root, 'src/added.py', 'def added():\n    return 1\n')
            (root / 'src/deleted.py').unlink()
            write(root, 'harness/sample.py', 'def sample():\n    return 2\n')
        if case['id'] == 'V-04c-move':
            write(root, 'src/moved.py', (root / 'inputs/moved.txt').read_text())
        (root / 'oracle.json').unlink()  # held back, never reviewer input
    return root


def native_inputs(root, case):
    scenario, variant = case['scenario'], case['variant']
    if scenario == 'V-06a':
        path = root / 'src/billing/receipts.py'
        path.write_text('from src.billing.service import checkout\n' + path.read_text())
        record(root, PYTHON, 'scripts/check-architecture', expected=1)
    if scenario not in ('V-06b', 'V-06c', 'V-06d', 'V-06e', 'V-06f', 'V-06g', 'V-06h', 'V-06i'):
        return
    native = root / 'docs/native.md'
    if scenario == 'V-06i':
        command = f'{shlex.quote(str(PYTHON))} tools/native.py'
        scope = f'Command: `{command}`. Governed scope: src and outside, including unchanged files. Execution owner: implementer before submission.'
        write(root, 'docs/policy-a.md', f'Authority A: {scope} Policy: F401 is required and hard.\n')
        write(root, 'docs/policy-b.md', f'Authority B: {scope} Policy: F401 is optional and advisory. No precedence declared; resolution owner: task authority.\n')
    if scenario == 'V-06b' and variant == 'NA':
        write(root, 'docs/change.md', 'Documentation-only active task; Python changes are unrelated fixture control. Measurement N/A.\n')
    if scenario == 'V-06h' and variant == 'none':
        native.unlink()
        (root / 'tools/native.py').unlink()
        (root / 'tools/aggregate.py').unlink()
    if scenario == 'V-06g':
        path = root / '.quality/reports/aggregate.json'
        data = json.loads(path.read_text())
        if variant == 'constituent':
            data['constituents'] = []
        elif variant == 'scope':
            data['constituents'][0]['scope'] = ['src']
            data['constituents'][0]['checked_bytes'].pop('outside/control.py')
        elif variant == 'policy':
            data['constituents'][0]['policy'] = 'missing-policy.md'
        else:
            write(root, 'outside/control.py', 'VALUE = 2\n')
        if variant != 'bytes':
            data['origin'] = 'seeded invalid consumer claim; real control is native-history.jsonl'
            path.write_text(json.dumps(data))


def evidence_fault(root, case):
    scenario, variant = case['scenario'], case['variant']
    path = root / BASE
    if scenario in ('V-02b', 'V-02c', 'V-02d'):
        data = json.loads(path.read_text())
        if scenario == 'V-02b':
            data['identity']['root'] = '/seeded/another-logical-project'
            data['repository']['head'] = '0' * 40
            write(root, 'project-binding.md', 'Expected project is measurement-fixture at its actual HEAD. Supplied B is labeled another logical project; matching relative paths are insufficient. Original project owner must recover the before state.\n')
        elif scenario == 'V-02c':
            if variant == 'format':
                data['format_version'] = 4
            elif variant == 'tools':
                data['identity']['tools']['ruff'] = '0.0.0-seeded-incompatible'
            elif variant == 'settings':
                data['identity']['ruff_config'] += '\n# seeded incompatible settings\n'
            else:
                data['identity']['checks'] = ['complexity']
        elif variant == 'current':
            data = json.loads((root / '.quality/reports/I1.json').read_text())
            path = root / '.quality/reports/I1.json'
            data['measurement_status'] = 'incomplete'
        elif variant == 'profile':
            data['full_profile'] = False
        elif scenario == 'V-02d':
            data['measurement_status'] = 'incomplete'
            data['checks']['ruff']['status'] = 'failed'
            data['checks']['ruff']['values'] = []
        data['fixture_fault'] = case['id'] + ': seeded consumer input, not historical tool execution'
        path.write_text(json.dumps(data))
    if scenario == 'V-02h':
        # The upstream pair collision is intentionally reduced to one sibling.
        (root / f'.quality/reports/current.{"txt" if variant == "json" else "json"}').unlink()
    if scenario == 'V-02i':
        write(root, 'docs/tasks/REVIEW/reviews/maintainability-01.md', 'Occupied prior report; preserve exactly.\n')
    if scenario == 'V-06j' and variant == 'unavailable':
        (root / '.agents/scripts/run_evidence.py').unlink()


def correction_inputs(root, case):
    scenario = case['scenario']
    if scenario not in ('V-08a', 'V-08b', 'V-08c', 'V-08d'):
        return
    # Both real edits and comparisons are fixture history, not a simulated
    # independent reviewer. Agent-produced R remains a separate obligation.
    measure(root, '.quality/reports/R1-control.json')
    if scenario in ('V-08b', 'V-08c'):
        target = root / 'src/billing/pricing.py'
        target.write_text((root / 'inputs/corrected-pricing.txt').read_text())
        measure(root, '.quality/reports/I2.json')
        measure(root, '.quality/reports/R2-control.json')
    if scenario == 'V-08d':
        write(root, 'outside/control.py', 'VALUE = 2\n')
    write(root, 'finding-ledger.json', json.dumps({'origin': 'seeded finding history; no live verdict',
        'MNT-B1': 'survives', 'MNT-B2': 'corrected in supplied correction',
        'MNT-B3': 'survives', 'MNT-B4': 'survives',
        'coverage': ['policy ownership', 'persistence boundary', 'receipt seam', 'dispatch locality']}))


def report_inputs(root, case):
    if case['scenario'] not in ('V-03c', 'V-03d', 'V-03e', 'V-03f', 'V-03g', 'V-03i', 'V-03j', 'V-07a', 'V-07b', 'V-07c'):
        return
    obligations = []
    if case['scenario'].startswith('V-07'):
        for index in range(4):
            name = f'cohesive_{index}'
            write(root, f'src/{name}.py', f'def {name}(value):\n' + '    if value: pass\n' * 10 + '    return value\n')
            obligations.append(dict(id=f'RAT-{index+1}', function=name, metric='complexity',
                                    before='absent', after=11, report='.quality/reports/obligations.json',
                                    explanation='One explicit protocol walk; all decisions share its value. Extracting single branches fragments the same policy and adds navigation without a consumer.'))
        measure(root, '.quality/reports/obligations.json')
    elif case['scenario'] in ('V-03c', 'V-03d', 'V-03e', 'V-03f', 'V-03g', 'V-07c'):
        report = json.loads((root / '.quality/reports/I1.json').read_text())
        active = next(row for row in report['comparison']['complexity'] if row['symbol'] == 'active')
        obligations = [dict(id='RAT-1', function='active', metric='complexity',
                            before=active.get('before', 'absent'), after=active['value'],
                            report='.quality/reports/I1.json',
                            explanation='One bounded status conversion keeps decisions local for one caller. Extracting each branch adds navigation; a local lookup table is a useful alternative if the mapping grows, but no shared boundary requires a separate abstraction now.')]
    elif case['scenario'] == 'V-03i':
        obligations = [dict(id='RAT-1', function='active', metric='complexity',
                            before=11, after=12, report='.quality/reports/I1.json',
                            explanation=None)]
    elif case['scenario'] == 'V-03j':
        obligations = [dict(id='RAT-1', function='active', metrics=['statements', 'complexity'],
                            report='.quality/reports/I1.json',
                            explanation='One cohesive policy walk. Splitting branches adds navigation and duplicates policy context; known values must be read from I1.')]
    write(root, 'rationale.json', json.dumps({'obligations': obligations,
        'missing_explanation_owner': 'implementer' if case['scenario'] == 'V-03i' else None,
        'gap': {'id': 'GAP-1', 'status': 'owed optional advisory corroboration', 'owner': 'measurement owner'},
        'optional_warning_candidates': ['spelling preference', 'blank line preference', 'quote preference', 'local alias preference', 'comment style preference']}))


def route_inputs(root, case):
    if not case['scenario'].startswith('V-10'):
        return
    checked = snapshot(root)
    facts = {'origin': 'seeded upstream stage history; not an executed review',
             'reviewed_bytes': {p: v for p, v in checked.items() if p.startswith('src/')},
             'measurement': '.quality/reports/I1.json', 'verdict': 'ACCEPT',
             'registry_stage': case['id'] not in ('V-10b-absent', 'V-10d'),
             'registry_current': case['id'] in ('V-10b-current', 'V-10c'),
             'discovery_current': case['scenario'] == 'V-10c'}
    if case['id'] == 'V-10f-stale':
        write(root, 'src/logic.py', (root / 'src/logic.py').read_text() + '\n# after verdict\n')
    if case['id'] == 'V-10f-incomplete':
        facts['outstanding'] = {'id': 'RAT-1', 'owner': 'implementer', 'reason': 'missing alternative cost'}
    if case['id'] == 'V-10f-blocker':
        facts['blocker'] = {'id': 'MNT-B1', 'owner': 'correction agent', 'reason': 'duplicated policy authority'}
    facts['correction_policy'] = ('Significant test scenario ownership correction affects required architecture/maintainability; registry absent.'
        if case['scenario'] == 'V-10d' else 'Trivial assertion correction explicitly exempt under task policy.'
        if case['id'] == 'V-10e-exception' else 'Review scope unchanged; unrelated docs correction only.'
        if case['id'] == 'V-10e-unaffected' else 'Existing ordered route applies.')
    if case['scenario'] == 'V-10d':
        facts['reviewed_bytes'].update({p: v for p, v in checked.items() if p.startswith(('tests/', 'harness/'))})
        write(root, 'harness/sample.py', 'CASE = {"value": 1}\ndef sample():\n    return CASE\n')
        write(root, 'tests/sample.py', 'from harness.sample import sample\ndef sample_test():\n    sample().clear()\n')
    if case['id'] == 'V-10e-exception':
        write(root, 'tests/sample.py', 'def sample():\n    assert 1 == 1, "stable contract"\n')
    write(root, 'conditional-history.json', json.dumps(facts, indent=2))
    write(root, 'docs/tasks/REVIEW/reviews/maintainability-01.md',
          '# Seeded upstream maintainability history; not an actor run\n\n' + json.dumps(facts, indent=2))
    if facts['registry_current']:
        write(root, 'registry-history.json', json.dumps(dict(origin='seeded upstream record', checked_bytes=facts['reviewed_bytes'])))
    if facts['discovery_current']:
        write(root, 'discovery-history.json', json.dumps(dict(origin='seeded independent discovery input; not execution', checked_bytes=facts['reviewed_bytes'])))
    for role in ('discovery', 'acceptance'):
        write(root, f'{role}-request.md', f'Consume conditional-history.json and numbered report as {role} inputs. Validate scope/bytes, rationale/native evidence and unresolved rows. Do not repeat general maintainability review or execute downstream stages. Name first outstanding owner and full remainder; discovery and acceptance remain separate.\n')


def prepare(case_id):
    case = next(row for row in CASES if row['id'] == case_id)
    WORK.mkdir(parents=True, exist_ok=True)
    root = seed(case)
    if case['scenario'].startswith('V-03') and case['scenario'][-1] in 'cdefg':
        path = root / 'src/logic.py'
        lines = path.read_text().splitlines()
        branch = 0
        for index, line in enumerate(lines):
            if line == 'def untouched(value):':
                break
            if line == '    if value: pass':
                lines[index] = f'    if value == {branch}: return "STATUS-{branch}"'
                branch += 1
        path.write_text('\n'.join(lines) + '\n')
    if case['scenario'] == 'V-05a':
        write(root, 'src/logic.py', '''def _ready(payload):
    payload["s"]["attempts"] += 1
    return payload["s"]["v"]

def _step(payload):
    return _ready(payload)

def _forward(payload):
    return _step(payload)

def active(value):
    return _forward({"s": {"v": value, "attempts": 0}})
''')
        write(root, 'local-contract.md', 'active still returns its input. Extraction now requires tracing three forwarding hops and opaque dictionary keys; _ready increments attempts and returns a value despite its predicate-like name. No variation, consumer, boundary or test seam needs these layers. Assess actual helper responsibility/navigation, not metric reduction.\n')
    if case['scenario'] == 'V-03j':
        path = root / 'src/logic.py'
        path.write_text(path.read_text().replace('def active():', 'def active(value):\n' + '    if value: pass\n' * 10, 1))
    baseline = root / BASE
    # Create author I before injecting evidence faults. Existing fault cases keep
    # their already generated C1 or a truthful missing-I state.
    usable = baseline.exists() and (root / '.agents/scripts/measure_maintainability.py').exists()
    if usable:
        result = record(root, PYTHON, root / '.agents/scripts/measure_maintainability.py',
                        'compare', *json.loads(baseline.read_text())['identity']['scope_directories'],
                        '--root', root, '--baseline', BASE,
                        '--output', '.quality/reports/I1.json', expected=None)
        if result.returncode:
            write(root, 'comparison-gap.txt', 'I unavailable: see held-back raw command result; do not invent evidence.\n')
    if case['scenario'] == 'V-04b':
        write(root, 'attribution.json', json.dumps({'active': 'untouched (deliberately incorrect author attribution)', 'untouched': 'affected (deliberately incorrect file-wide claim)'}))
    native_inputs(root, case)
    if case['scenario'] == 'V-01b':
        write(root, 'src/logic.py', (root / 'src/logic.py').read_text() + '\n# second edit with same short status\n')
    evidence_fault(root, case)
    correction_inputs(root, case)
    report_inputs(root, case)
    route_inputs(root, case)
    task = 'MNT-42' if 'legacy' in case else 'REVIEW'
    reports = f'docs/tasks/{task}/reviews'
    if case['scenario'] == 'V-01e':
        receiver = WORK / 'receiver'
        write(root, 'transfer-paths.txt', '\n'.join(f'{root}/.quality/reports/{n} -> {receiver}/.quality/reports/{n}' for n in ('B.json','B.txt','I1.json','I1.txt')))
    request = f'''# Independent review case {case['id']}

Situation: {case['situation']}
Task: review the actual current diff under this task's maintainability contract.
Read AGENTS.md, policy, local diff, B/I, rationale.json and conditional-history.json
when present. logical project: {root.name}; HEAD/actual before snapshots establish
its original binding. Seeded faults/history are labeled and do not prove actor runs.
This is a fresh session except V-01c/V-01d: those explicitly declare this session
authored the reviewed production / tests-only bytes and require SELF_CHECK_ONLY.
Already prepared interpreter: {PYTHON}
Active target launcher: .agents/scripts/measure_maintainability.py
Original B: {BASE}, .quality/reports/B.txt; author I: .quality/reports/I1.json,
.quality/reports/I1.txt (or explicit fault/gap). Governed folders in B identity.
Review must independently compare actual affected paths with B; do not use I alone.
Scope for docs/unsupported variants is docs/change.md / frontend/change.ts;
Python files there are unrelated fixture controls. No empty successful comparison.
Report path boundary: next unused {reports}/maintainability-NN.md.
External-path variant caller requests /work/task-runs/review.md; refuse that path.
Local reads, existing cheap commands, fresh .quality/reports JSON/text and only the
next numbered durable report are authorized. No source/index/old-report edits,
setup, dependency installs, active refresh, network or downstream execution.
Use existing native policy commands/owner/scope; no invented commands or stages.
{'Explicit task authority: measurement is indispensable for advancement.' if case['scenario'] == 'V-02f' else ''}
For route cases read separate discovery-request.md and acceptance-request.md as
prepared consumer inputs, not authority to merge the independent roles.
Only this workspace is reviewer scope. Setup, case definitions and task-runs
oracles are held back until raw output/command history are saved for grading.
'''
    if case['scenario'] == 'V-09a':
        request += '\nExpansion outside governed folders is NOT authorized. Task authority owns the scope decision.\n'
    elif case['scenario'] == 'V-09b':
        request += '\nExpansion to outside is authorized. Verify preserved/outside-control.txt against committed HEAD:outside/control.py before any supplemental capture; retain B.\n'
    elif case['scenario'] == 'V-09c':
        request += '\nExpansion to outside is authorized, but outside/edited.py has no preserved pre-edit bytes. Attempt current measure, retain the historical gap.\n'
    if case['scenario'] == 'V-01e':
        request += f'\nReviewer workspace: {receiver} (the only code/task read scope, using its existing installation). Setup has transferred submitted source and task inputs before review while retaining original Git HEAD. The source workspace is read-only solely for the exact B/I source siblings listed in transfer-paths.txt; copying them to their exact receiving paths is authorized. Review reads, existing cheap commands, fresh .quality/reports JSON/text and the next numbered durable report are authorized in the receiver. No source/index/old-report edits. Submitted source transfer is complete; ignored reports remain a separate explicit transfer.\n'
    if case['scenario'] == 'V-02g':
        write(root, 'docs/change.md' if case['variant'] == 'docs' else 'frontend/change.ts', '# Active documentation change\n' if case['variant'] == 'docs' else 'export const active = 2;\n')
    write(root, 'review-request.md', request)
    brief = root / f'docs/tasks/{task}/brief.md'
    original = brief.read_text() if brief.exists() else ''
    write(root, f'docs/tasks/{task}/brief.md', original + '\n' + request + '\nStatus: ready\nTask kind: executable\nReview: immediate\n')
    if case['scenario'] == 'V-01e':
        # The clone owns original HEAD. Setup transfers all submitted/task inputs,
        # including additions and deletions; ignored report pairs travel separately.
        names = record(root, 'git', 'ls-files', '--cached', '--others', '--exclude-standard').stdout.splitlines()
        for name in names:
            source, target = root / name, receiver / name
            if source.is_file():
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, target)
            elif target.is_file():
                target.unlink()
    # All machine setup facts and complete human artifact oracles are held back.
    control = dict(case, workspace=str(root), snapshot=snapshot(root),
                   expected_evidence='Compare actual report/diff, current source hashes, invocation history, rationale obligation ledger, native checked scope/policy/result and ordered route. Keyword presence alone cannot pass. R-control is setup tool evidence, never an independent actor report.')
    write(WORK, 'task-runs/oracle.json', json.dumps(control, indent=2))
    write(WORK, 'workspace.txt', str(root))
    print(root)


if __name__ == '__main__':
    prepare(sys.argv[1])
