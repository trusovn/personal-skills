"""Independent, local post-run audit; does not alter the live fixture."""
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
REPO = Path('/private/tmp/task-flow-spike-2026-10-08')
OUT = HERE / 'evidence'


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ledger = json.loads((OUT / 'ledger.json').read_text())
assert [row['stage'] for row in ledger] == [
    'brief', 'verification', 'preflight', 'implementation',
    'maintainability', 'registry', 'acceptance']
assert all(row['gate'] == 'passed' for row in ledger)
assert all(row['model'] == 'gpt-5.6-terra' and row['reasoning'] == 'medium' for row in ledger)
sessions = []
commands = {}
for row in ledger:
    events = [json.loads(line) for line in (OUT / f'{row["stage"]}.events.jsonl').read_text().splitlines()]
    sessions.append(next(e['thread_id'] for e in events if e['type'] == 'thread.started'))
    commands[row['stage']] = [{'command': e['item']['command'], 'exit_code': e['item']['exit_code']}
                              for e in events if e['type'] == 'item.completed'
                              and e.get('item', {}).get('type') == 'command_execution']
assert len(set(sessions)) == 7, 'Actors must have separate sessions'
for left, right in zip(ledger, ledger[1:]):
    assert left['after'] == right['before'], 'Unexpected between-stage file changes'
maint = next(row for row in ledger if row['stage'] == 'maintainability')
accept = ledger[-1]
for path in ('catalog.py', 'tests/test_catalog.py'):
    assert maint['before'][path] == accept['after'][path], 'Reviewed bytes changed after maintainability'

api = load(REPO / 'catalog.py', 'synthetic_catalog')
cases = [
    (['Bee', 'ant', 'Bee'], None, ['Bee', 'ant', 'Bee']),
    (['Bee', 'ant', 'Bee'], '', ['Bee', 'ant', 'Bee']),
    (['xBee', 'Bee', 'beetle', 'Beech', 'Bee'], 'Bee', ['Bee', 'Beech', 'Bee']),
    (['Bee', 'beetle', 'BEe'], 'be', ['beetle']),
    (['Bee', 'ant'], 'z', []),
    ([], '', []),
    ([], 'Bee', []),
    (['', 'Bee', ''], '', ['', 'Bee', '']),
]
for names, prefix, expected in cases:
    original = names.copy()
    actual = api.select_names(names) if prefix is None else api.select_names(names, prefix)
    assert actual == expected and names == original

validator_results = []
with tempfile.TemporaryDirectory(prefix='task-flow-validator-audit-') as temp:
    probe = Path(temp)
    (probe / 'docs').mkdir()
    shutil.copytree(REPO / 'docs/contracts', probe / 'docs/contracts')
    shutil.copy2(REPO / 'catalog.py', probe / 'catalog.py')
    shutil.copy2(REPO / 'README.md', probe / 'README.md')
    for expected_exit in (0, 1):
        if expected_exit:
            path = probe / 'docs/contracts/catalog.json'
            data = json.loads(path.read_text())
            data['provides'][0]['summary'] = False
            path.write_text(json.dumps(data))
        result = subprocess.run(['python3', str(REPO / 'tools/check_contracts.py'), '--root', str(probe)], text=True, capture_output=True)
        assert result.returncode == expected_exit, result.stdout + result.stderr
        validator_results.append({'case': 'invalid summary type' if expected_exit else 'valid registry', 'exit_code': result.returncode, 'output': result.stdout + result.stderr})

driver = load(HERE / 'run_spike.py', 'spike_driver')
with tempfile.TemporaryDirectory(prefix='task-flow-parser-audit-') as temp:
    probe = Path(temp)
    driver.REPO = probe / 'repo'
    driver.OUT = probe / 'out'
    driver.OUT.mkdir()
    result = json.loads((OUT / 'implementation.last.txt').read_text())
    for alteration in ('wrong_task', 'missing_field', 'unexpected_path'):
        candidate = dict(result)
        before = {}
        after = {}
        if alteration == 'wrong_task':
            candidate['task_id'] = 'OTHER'
        elif alteration == 'missing_field':
            del candidate['next_action']
        else:
            after = {'tools/unauthorized.py': 'unexpected'}
        (driver.OUT / 'implementation.last.txt').write_text(json.dumps(candidate))
        try:
            driver.check_stage('implementation', before, after)
        except ValueError:
            pass
        else:
            raise AssertionError(f'Failed to reject {alteration}')

report = {'stage_order': 'passed', 'unique_actor_sessions': sessions,
          'requested_runtime': 'gpt-5.6-terra / medium', 'between_stage_content_continuity': 'passed',
          'maintainability_to_acceptance_byte_identity': 'passed', 'public_api_cases': len(cases),
          'validator_probes': validator_results, 'invalid_worker_or_effect_rejections': 3,
          'actor_commands': commands}
(OUT / 'audit.json').write_text(json.dumps(report, indent=2) + '\n')
print('PASS: 7 sequential independent actor sessions; 8 public API cases; valid/invalid registry probes; 3 invalid worker/effect rejections.')
