# T-001.3 discovery report

Producing stage: task-review-discovery. Coverage: complete for the bounded task's
V-01–V-10 cases and R-05/R-06; no live-agent qualification. Iteration: first discovery.
Created: 2026-11-02T17:11:57.505800+00:00.
Repository: `/Users/mtrusov/work/skill-sources/personal-skills`. Report: `docs/tasks/T-001.3/reviews/discovery-01.md`.

This report supplies evidence only. It makes no acceptance decision, approved
deferral, advancement, or claim of its own authenticity.

## Provenance and preparation

This session authored no reviewed production or test bytes; its probes are
independent of implementation authorship. Reviewed HEAD: `0f747fa30e96aca7a72f86469d276cda901cf23f`.
Staged binary-diff SHA-256: `28815e8d6f60a850b5fa6c52f235dda08a0dd84874951e9a7cfbdbfc05431577`. Index/worktree matched before probes
and immediately before report creation. Exact index identities follow below.

Authority: `docs/tasks/T-001.3/brief.md`; verification design
`docs/tasks/T-001.3/verification.md`, revision 1; readiness:
`docs/tasks/T-001.3/preflight.md`. Finite-risk decision context: brief R-05/R-06
and verification V-01–V-10. Submission: `results.md`, READY_FOR_REVIEW.
User clarification supplies prior maintainability checked-pass evidence without
a separate document, and identifies staged registry synchronization as completed.
This is user-attributed stage evidence, not an independent maintainability verdict
from this discovery. The stale ordered-handoff text in results is interpreted
with that clarification. No prior discovery findings or reviewer regressions
were supplied. No new review stage was launched.

## Findings

No findings.

## Completeness ledger

D1–D7 refer to the exact commands below. Submitted evidence is the implementation
claim, not proof. Every pass below rests on current static inspection or actual
reviewer execution. Instruction cases establish documented obligations only.

| Row | AC / risk | Material cases | Setup / oracle | Submission | Current independent evidence | Result |
|---|---|---|---|---|---|---|
| V-01a | AC-01/06; R-05 | Existing registry | Carry command/scope/policy/requiredness/owner | results.md claims passing evidence | Static trace: repo-foundation 186–213; architecture-guardrails 225–253; results handoff a | pass |
| V-01b | AC-01/06; R-05 | Documented commands without registry | No new mandatory registry/runner | results.md claims passing evidence | Same guidance; results handoff b retains all five fields | pass |
| V-01c | AC-01/06; R-05 | No applicable native command | Record absence; invent no check | results.md claims passing evidence | Same guidance; results handoff c | pass |
| V-01d | AC-01/06; R-05 | Current aggregate covers constituents | Reuse only matching scope/policy/bytes | results.md claims passing evidence | Same guidance; results handoff d | pass |
| V-01e | AC-01/06; R-05 | Missing required evidence | Native owner/recovery route remains | results.md claims passing evidence | Same guidance; results handoff e | pass |
| V-01f | AC-01/06; R-05 | Stale required evidence | No waiver from advisory success | results.md claims passing evidence | Same guidance; results handoff f | pass |
| V-01g | AC-01/06; R-05 | Whole-project native, affected-path metrics | Do not narrow native scope | results.md claims passing evidence | Same guidance; results handoff g | pass |
| V-02 | AC-01/02/05 | Four source skills, template, installer/profile/README | No conflicting route; installer already selects changed resources | results.md claims passing evidence | Static inspection plus D3/D4; bootstrap/readiness no-change dispositions corroborated | pass |
| V-03 | AC-03; R-06 | Dirty/staged/untracked baseline; edit/add/delete; sibling exclusion | CC 5→7; captured worktree hashes; immutable baseline/source/index | results.md claims passing evidence | D2: test_snapshot_preserves_staged_unstaged_untracked_and_index; D7 independent CC 4→6 probe | pass |
| V-04 | AC-03; R-06 | Empty parent then new file; repeated comparison | CC 2 then 3; null before/delta; original/index preserved | results.md claims passing evidence | D2: test_empty_folder_baseline_preserves_absence_across_edits | pass |
| V-05a | AC-04; R-06 | Neither target file | Constant native values; independent targets, origin/path/hash; no policy writes | results.md claims passing evidence | D2: test_settings_select_each_target_file_independently | pass |
| V-05b | AC-04; R-06 | Maintainability only | Constant native values; independent targets, origin/path/hash; no policy writes | results.md claims passing evidence | D2: test_settings_select_each_target_file_independently | pass |
| V-05c | AC-04; R-06 | Ruff only | Constant native values; independent targets, origin/path/hash; no policy writes | results.md claims passing evidence | D2: test_settings_select_each_target_file_independently | pass |
| V-05d | AC-04; R-06 | Both target files | Constant native values; independent targets, origin/path/hash; no policy writes | results.md claims passing evidence | D2: test_settings_select_each_target_file_independently | pass |
| V-06a | AC-04; R-06 | Malformed maintainability TOML | Valid controls; exit 2, no fallback/output, target preservation | results.md claims passing evidence | D2: test_invalid_target_settings_and_unrelated_root_ruff | pass |
| V-06b | AC-04; R-06 | Malformed Ruff TOML | Valid controls; exit 2, no fallback/output, target preservation | results.md claims passing evidence | D2: test_invalid_target_settings_and_unrelated_root_ruff | pass |
| V-06c | AC-04; R-06 | Boolean target/string exclusions and typed-field matrix | Valid controls; exit 2, no fallback/output, target preservation | results.md claims passing evidence | D2: test_invalid_policy_settings_fail_before_measurement | pass |
| V-07 | AC-04; R-06 | Missing pinned tools; executable setup recipe | -S refusal; target-aware recipe; mock only package provisioning seam | results.md claims passing evidence | D2: test_missing_pins_recipe_dispatches_setup_for_selected_target; no download qualification | pass |
| V-08a | AC-03/04; R-06 | Neutral increases/decreases and successful breach | Actual values/deltas, neutral saved/console labels; exit 0 | results.md claims passing evidence | D2: test_saved_and_console_reports_use_neutral_labels | pass |
| V-08b | AC-03/04; R-06 | Native unknown count in both directions | null count/delta rather than zero; actual installed Ruff reports | results.md claims passing evidence | D2: test_ruff_missing_diagnostics_never_become_numeric_zero | pass |
| V-08c | AC-03/04; R-06 | Format 3 baseline | Explicit incompatible exit 2; original preserved | results.md claims passing evidence | D2: test_cli_rejects_incompatible_baseline_identities | pass |
| V-08d | AC-03/04; R-06 | Format 4 baseline | Explicit incompatible exit 2; original preserved | results.md claims passing evidence | D2: test_cli_rejects_incompatible_baseline_identities | pass |
| V-08e | AC-03/04; R-06 | Repeat against original with fresh names | Original and successive JSON/text pairs survive | results.md claims passing evidence | D2: test_empty_folder_baseline_preserves_absence_across_edits; test_snapshot_preserves_staged_unstaged_untracked_and_index | pass |
| V-08f | AC-03/04; R-06 | JSON-only collision for all three operations | Exit 2; sentinel survives; absent sibling stays absent; index/source intact | results.md claims passing evidence | D2: test_each_report_sibling_collision_refuses_write | pass |
| V-08g | AC-03/04; R-06 | Text-only collision for all three operations | Same refusal and preservation oracle | results.md claims passing evidence | D2: test_each_report_sibling_collision_refuses_write | pass |
| V-09 | AC-02/05; R-06 | Fresh install; changed/missing all six shared files, both skills, template, guide; repeated check/refresh | Drift exit 1 without repair; refreshed match; unrelated policy/env/reports/index/AGENTS preserved | results.md claims passing evidence | D3 focused resource journey; D4 all 36 installer tests, including all-family ownership journeys | pass |
| V-10 | AC-06; R-05 | Native whole-project F401 vs installed advisory success | Clean native 0; unused import native 1 with F401/sample.py; measure 0 CC 5; preserve prior tree | results.md claims passing evidence | D1 independently executed real subprocess case; repeated in D2; handoff retains failed native obligation | pass |

## Probe and command records

All commands ran from the repository root. `P` below is exactly
`.quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python`.
These are notation expansions, not shell variables that must already exist.
Pinned packages independently inspected: Radon 6.0.1, Ruff 0.14.2, mando 0.7.1,
colorama 0.4.6, six 1.17.0.

| ID | Exact command (expand P as above) | Purpose / observed result |
|---|---|---|
| D1 | `PYTHONDONTWRITEBYTECODE=1 P -m unittest discover -s tests -p test_maintainability.py -k native_hard -v` | Mixed real native/advisory boundary: 1 passed, 0 skips, 0.546s. |
| D2 | `PYTHONDONTWRITEBYTECODE=1 P -m unittest discover -s tests -p test_maintainability.py -v` | All 33 measurement cases passed, 0 skips, 16.001s. |
| D3 | `PYTHONDONTWRITEBYTECODE=1 P -m unittest discover -s tests -p test_install_development_skills.py -k measurement_and_discovery -v` | Expanded managed-resource drift/refresh: 1 passed, 0 skips, 8.559s. |
| D4 | `PYTHONDONTWRITEBYTECODE=1 P -m unittest discover -s tests -p test_install_development_skills.py` | All 36 installer cases passed, 0 skips, 28.862s. |
| D5 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py` | 4 passed, 0 skips. Structural architecture policy only. |
| D6 | `python3 tools/check_contracts.py --root .` | Passed: 6 subsystems, 12 indexed plan refs. Structural registry/index agreement only. |
| D7 | Reviewer-written Python heredoc, reproduced below | Fresh installed unrelated-cwd baseline/edit/compare, countable CC 4→6 (+2), old-name refusal, source/index/report preservation: 1 passed, 0 skips, 0.589s. |

D1–D4/D7 use disposable Git targets. The existing distribution helper installs
from a disposable complete source projection, then removes it before CLI runs.
`launch` strips PYTHONPATH/PYTHONHOME. Static trace confirmed launcher → adjacent
maintainability_env.py → adjacent maintainability.py, defaults and requirements.
The prepared interpreter is intentionally external. This is distribution-removal
isolation, not an OS access-denial proof against the actual checkout. No provider,
network call, package install, active installation refresh or fixture survives.
All synchronous probe commands returned and TemporaryDirectory cleanups ran.
Process-group lifecycle qualification is not a task requirement.

D7 exact command (P expanded):

```sh
PYTHONDONTWRITEBYTECODE=1 .quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python - <<'PYPROBE'
import sys, unittest, json
sys.path.insert(0,'tests')
from test_maintainability import MeasurementTests, function
class ReviewerProbe(MeasurementTests):
    def runTest(self):
        launcher,cwd=self.installed_launcher()
        self.git('add','sample.py')
        index=(self.root/'.git/index').read_bytes()
        self.source.write_text(function('reviewer',3))
        source=self.source.read_bytes()
        first=self.launch(launcher,cwd,'baseline','.', '--output','review-original.json')
        self.assertEqual(0,first.returncode,first.stderr)
        original=(self.root/'review-original.json').read_bytes()
        self.source.write_text(function('reviewer',5))
        edited=self.source.read_bytes()
        second=self.launch(launcher,cwd,'compare','sample.py','--baseline','review-original.json','--output','review-next.json')
        self.assertEqual(0,second.returncode,second.stderr)
        row,=json.loads((self.root/'review-next.json').read_text())['comparison']['complexity']
        self.assertEqual((4,6,2),(row['before'],row['value'],row['delta']))
        refused=self.launch(launcher,cwd,'compare','sample.py','--baseline','review-original.json','--output','review-original.json')
        self.assertEqual(2,refused.returncode)
        self.assertEqual(original,(self.root/'review-original.json').read_bytes())
        self.assertEqual(index,(self.root/'.git/index').read_bytes())
        self.assertEqual(edited,self.source.read_bytes())
        print('Independent probe: installed unrelated-cwd CC 4 -> 6 (+2); original-name refusal; baseline/source/index preserved.')
result=unittest.TextTestRunner().run(unittest.TestSuite([ReviewerProbe('runTest')]))
raise SystemExit(not result.wasSuccessful())
PYPROBE
```

Additional executable-validator probe (passed, no writes):

```sh
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PYPROBE'
import copy, importlib.util, json
from pathlib import Path
s=importlib.util.spec_from_file_location('contracts','tools/check_contracts.py')
m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
r=Path('.').resolve(); p=r/'docs/contracts/measurement.json'; data=json.loads(p.read_text())
e=[]; m.validate_contract(r,p,data,e); assert not e,e
bad=copy.deepcopy(data); bad['provides'][-1]['declarations']=['missing-native-policy.md']
e=[]; m.validate_contract(r,p,bad,e); assert any('path does not exist' in x for x in e),e
print('Registry validator: valid current record accepted; missing discovery declaration rejected:',e)
PYPROBE
```

This exercises the actual core-v1 validator boundary: current record accepted,
missing declaration path rejected. No changed JSON Schema draft is involved.
Metadata checks do not stand in for runtime composition evidence.

Other read-only commands: `git diff --cached --check` passed; `git diff --quiet`
passed; `git diff --cached --raw`, `git diff --cached --numstat`,
`git diff --cached --binary | shasum -a 256`, `git status --short`,
`git rev-parse HEAD` established scope and identity. Static reads covered the
scoped diff, task preparation, both changed skills/template, bootstrap/readiness,
installer declarations, helper resolution, registry authorities and test setup.
Package pins command:
`PYTHONDONTWRITEBYTECODE=1 P -c 'import importlib.metadata as m; print({n:m.version(n) for n in ("radon","ruff","mando","colorama","six")})'`.

## Aggregate-gate record

Exact gate: `P tools/verify.py` (P as above). Current discovery: **not run**.
Owner/stage: original implementer owns the initial aggregate per the brief;
this initial discovery owns the decision not to add a repeat. No targeted failure
suppressed a gate. The targeted ledger is reconciled and complete; no correction
or outstanding fresh-discovery aggregate rerun was identified. Repository-wide
execution is slower and has known sandbox/profile constraints; it was not added
merely for reporting. No claim of a current all-green aggregate is made.

Producer-attributed evidence only: results.md reports the approved host aggregate
passed 528 tests with no skips but exited 1 for four active-profile drift paths.
That historical gate is neither current independent proof nor erased by focused
passes. Current D5/D6 independently establish architecture and contract checks.
No permission waiver, drift repair, or approved deferral is recorded here.

## Scope and residual limits

All 12 staged paths fall within discovery guidance, installed-composition tests,
preparation/results or actual registry synchronization. No unstaged overlap was
present. Earlier submission references to pre-existing alternative briefs and
task-index staging do not describe the current index; those paths are absent
from the reviewed diff. They are not absorbed into this review. Current brief
is tracked unchanged; authority is supplied by the package and user clarification.

Live agent obedience, platform portability, OS-enforced source isolation,
package download/provisioning and T-005's later workflow journey remain outside
this task's qualified boundary. V-08b uses installed measurement reports with
in-process comparison semantics, as the derived verification explicitly allows.
No required scenario is blocked or unchecked. Aggregate limitation above remains
separate from these bounded scenario results.

Exact reviewed status before report write:

```text
M  docs/contracts/index.json
M  docs/contracts/measurement.json
M  docs/development.md
A  docs/tasks/T-001.3/preflight.md
A  docs/tasks/T-001.3/results.md
A  docs/tasks/T-001.3/verification.md
M  skills/README.md
M  skills/architecture-guardrails/SKILL.md
M  skills/architecture-guardrails/templates/gates.yaml
M  skills/repo-foundation/SKILL.md
M  tests/test_install_development_skills.py
M  tests/test_maintainability.py

```

Exact scoped index identities:

```text
100644 60670240cf466f75522568017d88908e065d658a 0	docs/contracts/index.json
100644 b3f816fad1bea33758cc98781a0ef1fb4e4bd3d5 0	docs/contracts/measurement.json
100644 276cc46665d56aec2fbde3764330cb4366f7d321 0	docs/development.md
100644 94d863d671df98d71e760a2b4b3b491363065806 0	docs/tasks/T-001.3/preflight.md
100644 ea09d803715786726e673f0877a8e315c9592929 0	docs/tasks/T-001.3/results.md
100644 59a95e103a28a7c893ce5ddfe9b6df247f4f4bc7 0	docs/tasks/T-001.3/verification.md
100644 c15e689a03e24298223a09901778e90d96112e93 0	skills/README.md
100644 c49a8104fc78c83a41fdad5bfc953348b7b2ac98 0	skills/architecture-guardrails/SKILL.md
100644 0c74ef5c7bada4863f1002cc5ca17ad68a0e52c7 0	skills/architecture-guardrails/templates/gates.yaml
100644 30bb9cebce5a2c7a876b21b2d1dba32c12cc9315 0	skills/repo-foundation/SKILL.md
100644 5c557b347016e57121b8dbc9cc315d0d2ca4b45a 0	tests/test_install_development_skills.py
100644 d2d3da58d10dec24a2b9ecc4636afa52b472acb1 0	tests/test_maintainability.py

```

## Discovery continuation

- Iteration / current byte identity: first independent discovery; HEAD and staged
  diff SHA-256 recorded above. Report itself is outside the reviewed bytes.
- Coverage rows: V-01a/b/c/d/e/f/g; V-02; V-03; V-04; V-05a/b/c/d;
  V-06a/b/c; V-07; V-08a/b/c/d/e/f/g; V-09; V-10 = pass, with individual
  setups/oracles and evidence in the ledger. R-05/R-06 covered by those rows.
- Finding IDs: none. Prior statuses: producer claimed pass, reviewer initially
  unchecked; now independently corroborated as scoped above. No correction owner
  or influenced defective sibling surface exists. Evidence owner: this discovery;
  authority owner: task brief/user. Prior maintainability pass remains user-attributed.
- Preparation/context: brief.md; verification.md revision 1; preflight.md;
  brief R-05/R-06; results.md plus user stage clarification.
- Reviewer regressions: no files added; D1–D4 and reproducible D7 above.
- Aggregate gate: not rerun; `P tools/verify.py`; implementer initial-gate owner;
  discovery retains historical failed drift result and current focused evidence.
- Next: separate task-acceptance-review call with the brief, current scoped staged
  diff, this report, verification revision 1, preflight, R-05/R-06 context,
  results/user clarification and D1–D7 commands. No blocked/unchecked rows to carry.

Post-report status (verified immediately after creation):

```text
M  docs/contracts/index.json
M  docs/contracts/measurement.json
M  docs/development.md
A  docs/tasks/T-001.3/preflight.md
A  docs/tasks/T-001.3/results.md
A  docs/tasks/T-001.3/verification.md
M  skills/README.md
M  skills/architecture-guardrails/SKILL.md
M  skills/architecture-guardrails/templates/gates.yaml
M  skills/repo-foundation/SKILL.md
M  tests/test_install_development_skills.py
M  tests/test_maintainability.py
?? docs/tasks/T-001.3/reviews/
```

Only the new discovery report entry differs from reviewed status.
