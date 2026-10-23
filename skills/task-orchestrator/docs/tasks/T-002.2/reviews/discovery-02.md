# Task Review Discovery Report: T-002.2 — correction discovery

| Field | Value |
|---|---|
| Producing stage | task-review-discovery |
| Coverage completeness | complete — V-01..V-05 and R1..R3 have current dispositions; new F-02 |
| Iteration | correction 1, second discovery |
| Created | 2026-10-23T16:59:23.753299+01:00 |
| Repository | /Users/mtrusov/work/skill-sources/personal-skills |
| Durable report | skills/task-orchestrator/docs/tasks/T-002.2/reviews/discovery-02.md |
| Authority | brief.md revision 1; verification.md revision 1 |
| Preparation/context | preflight.md including Decision context; parent T-002 brief; local-harness-orchestration-plan.md IF-001 and INV-001/002/005/007/008; accepted T-002.1 contract |
| Submission | implementation-report.md and correction-report-01.md, READY_FOR_REVIEW; controller-contract.md |

Evidence only: no acceptance verdict, approved deferral or advancement. This report applies only to the identified reviewed bytes. It does not review or authenticate itself.

## 1. Provenance and scope identity

This session authored no reviewed production or test bytes. Evidence is independent of implementation authorship. Applied the project-local task-review-discovery skill/template and testing-discipline. No subagents, installs, live/network/model probes or active-skill refresh occurred.

HEAD is `1c1aff83da3cbc69ecfe6acc2235108118f2cc12`, matching preflight. SHA-256 of `git diff HEAD --binary` is `37967712998327168f349737c9d09b809b0affb78c01ecce86b3c88025d1894b`. No unstaged tracked changes exist. All changed paths match the submission, preparation and prior review artifacts. The Git wiring test change is declared fixture reuse. No unexplained user-work overlap was found.

The correction report describes its then-unstaged changes. They are now staged: the index and worktree both match its recorded state blob `a27b1367fe7370ee64defc78653c4a6bd88dd49b` and controller-test blob `cd8ff075f2b976f38d5bf7cdea4f1ef741ae6504`. This is an index-state change from the earlier handoff, not identical earlier index evidence. Other implementation blobs match discovery-01. No index mutation was performed by this session.

| Path | Index Git blob | Worktree Git blob |
|---|---|---|
| `skills/task-orchestrator/docs/tasks/T-002.2/controller-contract.md` | `5224ed8f1e895c60e6e98ce81a7b0e600987cc27` | `5224ed8f1e895c60e6e98ce81a7b0e600987cc27` |
| `skills/task-orchestrator/docs/tasks/T-002.2/correction-report-01.md` | `03b61a84a5157d774301da48f07b264072344ab4` | `03b61a84a5157d774301da48f07b264072344ab4` |
| `skills/task-orchestrator/docs/tasks/T-002.2/implementation-report.md` | `13d092ce4c83ee92bdfa7bb270b5054dcbb1137f` | `13d092ce4c83ee92bdfa7bb270b5054dcbb1137f` |
| `skills/task-orchestrator/docs/tasks/T-002.2/preflight.md` | `d7b7f740dc0d82c1fa50c779ee7cc3381c5722da` | `d7b7f740dc0d82c1fa50c779ee7cc3381c5722da` |
| `skills/task-orchestrator/docs/tasks/T-002.2/reviews/discovery-01.md` | `026622a51f89ac701b0c558446deaa5d714951d7` | `026622a51f89ac701b0c558446deaa5d714951d7` |
| `skills/task-orchestrator/docs/tasks/T-002.2/reviews/maintainability-01.md` | `6d52beeed98bcedccd968dcf6830d8280f89113b` | `6d52beeed98bcedccd968dcf6830d8280f89113b` |
| `skills/task-orchestrator/scripts/controller.py` | `e435948d4cc7a9751a694b32221d51c83de84549` | `e435948d4cc7a9751a694b32221d51c83de84549` |
| `skills/task-orchestrator/scripts/controller_state.py` | `a27b1367fe7370ee64defc78653c4a6bd88dd49b` | `a27b1367fe7370ee64defc78653c4a6bd88dd49b` |
| `skills/task-orchestrator/tests/test_controller.py` | `cd8ff075f2b976f38d5bf7cdea4f1ef741ae6504` | `cd8ff075f2b976f38d5bf7cdea4f1ef741ae6504` |
| `skills/task-orchestrator/tests/test_controller_git.py` | `6d3e24b2cd8e308e4cbb5d75d957f5a42531ba80` | `6d3e24b2cd8e308e4cbb5d75d957f5a42531ba80` |
| `skills/task-orchestrator/tests/test_controller_state.py` | `038ba6ff3af9a0f4257e589344303d0e719e8657` | `038ba6ff3af9a0f4257e589344303d0e719e8657` |

Exact reviewed status before report creation:

```text
A  skills/task-orchestrator/docs/tasks/T-002.2/controller-contract.md
A  skills/task-orchestrator/docs/tasks/T-002.2/correction-report-01.md
A  skills/task-orchestrator/docs/tasks/T-002.2/implementation-report.md
A  skills/task-orchestrator/docs/tasks/T-002.2/preflight.md
A  skills/task-orchestrator/docs/tasks/T-002.2/reviews/discovery-01.md
A  skills/task-orchestrator/docs/tasks/T-002.2/reviews/maintainability-01.md
M  skills/task-orchestrator/scripts/controller.py
M  skills/task-orchestrator/scripts/controller_state.py
M  skills/task-orchestrator/tests/test_controller.py
M  skills/task-orchestrator/tests/test_controller_git.py
M  skills/task-orchestrator/tests/test_controller_state.py
```

## 2. Findings

### F-01 — prior finding: original demonstrated cases now rejected

Prior suggested severity P2; prior V-01/V-02/V-04 failed. DISC-02 reran the exact earlier reproducer body: valid active assignment accepted; two owners, wrong input, flow revision, candidate, current stage and stopped parent rejected. DISC-01 independently reran the correction's six-stage by three-active-state regression and terminal-history preservation. These observations corroborate the correction for the demonstrated F-01 invariant; they are not an acceptance decision. Historical terminal assignments remain replayable. The sibling actor-policy gap below is a distinct finding, not hidden behind these passing regressions.

### F-02 [suggested P2] Active assignments can expose an actor that contradicts frozen policy

| Field | Evidence |
|---|---|
| Location | `skills/task-orchestrator/scripts/controller_state.py:1182` (known-profile membership check); `controller.py:1510` reservation context, `:1598` status and `:1649` replay path |
| Trigger | Initialize a real fast-local run, establish test-only terminal preflight/readiness, reserve implementation. Change only the active assignment actor from `gpt-6.1-sol/medium` to the known `gpt-6.1-sol/low`; retain frozen policy, flow, digests, request and every other identity. |
| Observed consequence | Executable ledger validation succeeds; public status returns `ok`; exact-key replay returns the weaker actor assignment as `replayed`. A replacement coordinator receives an assignment inconsistent with the frozen stage-to-actor mapping. |
| Evidence | DISC-02: same behavior for implement, correction, semantic_review and acceptance (medium to low), and preflight (low to medium), each in reserved/running/unknown states. Before/after snapshots unchanged by reads/replays. Ordinary reservation originally emitted the correct actor. |
| Affected AC | AC-01 truthful status, AC-02 frozen-policy-bound assignment, AC-03 current authority/no bypass; V-01/V-02/V-04; R3 |
| Broken invariant | Current active assignment actor must equal the actor selected by its frozen flow stage mode. Membership in the global known profiles does not establish that relationship. T-002.1 fixes light/standard/strong mapping; T-002.2 contract says actual assignment resolves stage mode through the frozen flow. |
| Credible sibling surface | All actor-bearing reservable stages and all three active states, directly exercised. Verify has actor null and remains a separate control in DISC-01. Historical terminal assignments must retain their historical actor identity rather than be rebound to current policy. |
| Smallest corrective direction | Validate the complete active assignment's actor selection against the loaded authoritative flow before public status/replay exposes it, while preserving historical terminal assignments. No generic membership-only check or demonstrated-stage special case. |

This is deliberate persisted-record inconsistency, not proof that normal reservation emits a wrong profile, a production actor was launched, or whole-run tampering can be authenticated. Like F-01 it concerns the executable consistency boundary consumed by successors. The immutable policy and flow remain unchanged; no internal digest recomputation is needed because the embedded assignment has no digest of its own.

## 3. Completeness ledger

Ledger frozen from brief revision 1, verification revision 1 and discovery-01 before probes/aggregate consideration. Submitted evidence in each row is the implementation/correction reports' named-test map, not independent proof.

| Row | AC / risk | Explicit cases, setup and oracle | Current independent evidence | Result / reason |
|---|---|---|---|---|
| V-01 | AC-01 | Real status/reload; identity, version, operation/count, references/findings; passed/failed/stale/blocked/missing/not_run; mandatory omission blocked, optional repository-gate omission explicit; unchanged run/task bytes | DISC-01 read-only/status cases pass; F-01 status regressions pass; DISC-02 wrong active actor reported as valid | fail — F-02; ordinary evidence/status cases pass |
| V-02 | AC-02/03, R1 | First reserve/replay/reload, exact original request, changed key/version, separate-process contention; reserved/running/unknown block, terminal allows next; assignment identity and frozen authority | DISC-01 all lifecycle/replay tests pass; DISC-03 bounded real contention one winner; DISC-02 original F-01 regressions reject invalid records but wrong active actor replays | fail — F-02; R1 one-owner cases pass |
| V-03 | AC-04, R2 | Initial zero; mixed check/review/repair charges 1/2/3; replay/reload/uncertain launch; fourth unchanged/intervention; repair before implementation retains count after new preflight; free evidence/preflight retries cannot repair | DISC-01 shared-budget, pre-initial repair and free-retry methods pass against real persisted records with snapshot/count oracles | pass — current finite-risk budget evidence |
| V-04 | AC-03/05, R3 | Stale/invalid version/task/role/stage/key/reason, absent/stale/failed/wrong-task/wrong-role/nonterminal readiness; weak authority; run-next/inspect/revise-flow/update guards; unchanged authority/task bytes | DISC-01 negative requests/CLI/legacy guards pass; original F-01 invalid current-state cases rejected; DISC-02 known but unauthorized actor accepted | fail — F-02; ordinary refusal/legacy cases pass |
| V-05 | AC-05 | Exact status/reserve/replay/refusal fields and CLI; embedded assignment/count publication; successor seams; no generic public fixture/state setter | Source/contract comparison plus DISC-01 public CLI tests. Outcome/readiness admission stays T-003; semantic routing stays T-004/005; revision stays T-002.3 | pass — interface documented; actor consistency defect separately tracked above |

R1 is covered by V-02; R2 by V-03; R3 by V-04. No required row is blocked or unchecked. Coverage complete means all selected cases have dispositions, not that behavior is clean.

## 4. Commands and current probe evidence

All commands ran from `/Users/mtrusov/work/skill-sources/personal-skills` with local Python and disposable fixture Git repositories. No reviewed source/tests were changed. Fixtures supply labelled successor state only; they do not prove production admission or launches.

### DISC-01 — current targeted cases

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills.task-orchestrator.tests.test_controller.ControllerReservationTest
```

Exit 0: 11 tests, 8.756 seconds. Includes both new correction regressions, existing V-01..V-04 behavior and public CLI wiring. The existing contention test has an unbounded readiness readline; its successful completion does not prove timeout robustness. DISC-03 supplies separately bounded synchronization and cleanup evidence. All test children completed and fixture temporary state was torn down.

### DISC-02 — exact prior regression and actor-policy siblings

```sh
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import importlib,json,copy
from pathlib import Path
old=Path('skills/task-orchestrator/docs/tasks/T-002.2/reviews/discovery-01.md').read_text()
source=old.split("python3 - <<'PROBE'\n",1)[1].split('\nPROBE',1)[0]
exec(compile(source,'discovery-01:DISC-02','exec'))
m=importlib.import_module('skills.task-orchestrator.tests.test_controller')
t=m.ControllerReservationTest();t.setUp()
try:
 for stage,prior in [('preflight',None),('implement',None),('correction',None),('semantic_review','verify'),('acceptance','semantic_review')]:
  c,r=t.create_initialized_run(name='actor-'+stage)
  if stage!='preflight':t.ready_implementation(r)
  if prior:
   b=t.read_ledger(r);t.seed_successor(r,stage=stage,candidate_sha256='a'*64,evidence={prior:{'status':'passed','inputs_sha256':b['inputs_sha256'],'candidate_sha256':'a'*64}})
  if stage=='correction':t.seed_successor(r,correction_request='environment_repair')
  result=t.reserve(r,stage,'profile','environment_repair' if stage=='correction' else 'initial');assert result['status']=='reserved',result
  v=t.read_ledger(r);original=copy.deepcopy(v['actor_operations'][-1]['assignment']['actor'])
  replacement={'model':'gpt-6.1-sol','reasoning':'low' if original['reasoning']!='low' else 'medium'}
  for state in ['reserved','running','unknown']:
   v['actor_operations'][-1]['state']=state;v['actor_operations'][-1]['assignment']['actor']=replacement
   (r/'ledger.json').write_text(json.dumps(v));before=t.snapshot(r)
   c._validate_ledger(v);status=c.status_run(r);replay=c.reserve_operation(r,**v['actor_operations'][-1]['request'])
   assert status['status']=='ok' and replay['status']=='replayed';assert replay['assignment']['actor']==replacement
   assert before==t.snapshot(r)
  print(stage,original,'->',replacement,': status/replay accepts all 3 active states')
finally:t.tearDown()
PY
```

Exit 0 indicates probe completion, not clean behavior. The prior reproducer accepted its valid control and rejected all six invalid variants. For five actor stages, all three active states accepted and replayed a different actor: preflight low to medium; implementation, correction, collection and acceptance medium to low. This supplies valid/invalid executable-validator evidence, public reader/replay evidence and F-02's demonstrated failure. No separate ledger JSON Schema exists. Temporary state removed by teardown; no worker processes spawned.

An earlier exploratory inline loop used the same implementation setup, original six mutations and a single medium-to-low actor mutation. It observed the same F-02 outcome and unchanged bytes. DISC-02 above supersedes its reproduction with complete bounded sibling evidence; it is not a separate gate.

### DISC-03 — bounded real contention and cleanup

```sh
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import importlib,json,subprocess,sys,selectors,os
m=importlib.import_module('skills.task-orchestrator.tests.test_controller');t=m.ControllerReservationTest();t.setUp();ps=[]
try:
 c,r=t.create_initialized_run()
 script="import sys,json;from pathlib import Path;sys.path.insert(0,sys.argv[3]);import controller;print('ready',flush=True);sys.stdin.readline();print(json.dumps(controller.reserve_operation(Path(sys.argv[1]),expected_version=1,task_id='T1',stage='preflight',role='preflight',operation_key=sys.argv[2])))"
 for key in ('one','two'):
  ps.append(subprocess.Popen([sys.executable,'-B','-c',script,str(r),key,str(m.CONTROLLER_PATH.parent)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,start_new_session=True))
 for p in ps:
  with selectors.DefaultSelector() as sel:
   sel.register(p.stdout,selectors.EVENT_READ);assert sel.select(5),'ready timeout'
  assert p.stdout.readline()=='ready\n'
 for p in ps:p.stdin.write('go\n');p.stdin.flush()
 results=[]
 for p in ps:
  out,err=p.communicate(timeout=10);assert p.returncode==0,err;results.append(json.loads(out))
 assert sorted(x['status'] for x in results)==['refused','reserved'],results
 assert len(t.read_ledger(r)['actor_operations'])==1
 print('one winner, one refusal, one persisted owner')
finally:
 for p in ps:
  if p.poll() is None:os.killpg(p.pid,9)
  p.wait(timeout=5)
  try:os.killpg(p.pid,0)
  except ProcessLookupError:pass
  else:raise AssertionError('process group survives')
  assert p.stdout.closed and p.stderr.closed,'inherited pipes not released'
 t.tearDown()
print('all child processes/groups disappeared; pipes released; temporary state removed')
PY
```

Exit 0. Output: `one winner, one refusal, one persisted owner`; `all child processes/groups disappeared; pipes released; temporary state removed`. Each child is its own process-group/session leader and only imports/reserves; it spawns no descendants. Readiness bounded by 5 seconds; communication by 10 seconds; reap by 5 seconds. Group absence and pipe closure asserted after both children complete. No fixture process survives.

Static scope/source commands: `git diff --cached --` for both scripts; `git diff HEAD --stat`; `git diff --name-only`; `git rev-parse HEAD`; `git status --short --untracked-files=all`; `git rev-parse :<path>` and `git hash-object <path>` for each path in section 1; SHA-256 of `git diff HEAD --binary`. Read current task package, prior discovery/maintainability, predecessor contract, parent brief and cited plan invariants. These are scope/interface evidence, not behavioral tests.

## 5. Aggregate-gate record

| Field | Value |
|---|---|
| Exact designated command | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'` |
| Status | not run |
| Owner/stage | This independent correction discovery |
| Reason | DISC-02 decisive targeted F-02 failure suppresses aggregate. No diagnostic aggregate or additional gate was added. |
| Reconciliation | V-01..V-05/R1..R3 all have current targeted dispositions; original reviewer regression and named siblings exercised; no blocked/unchecked rows. Green DISC-01 does not erase F-02. |

Owning modules and broader aggregate were not rerun for completeness after the decisive failure. Prior implementation results and the preflight retrieval-inventory issue are historical claims, not current discovery gates. A future correction discovery owns the justified aggregate after current targeted evidence is clean.

## 6. Questions, residual limits and next route

No blocked/unchecked discovery row. Production actor launch, observed outcome/readiness admission, semantic routing, input revision and completion remain excluded successor work. No authenticated whole-run tamper guarantee is inferred.

The correction handoff requests refreshed maintainability review. Only maintainability-01 is present and covers earlier bytes; it is not current correction evidence. This discovery does not waive or perform that separate owner's conditional duty. Separate acceptance must account for that record and F-02. No authority change was needed to gather this evidence.

Next: a separate task-acceptance-review call consumes this report, brief.md revision 1, verification.md revision 1, preflight.md including Decision context, current scoped diff/identities, implementation-report.md, correction-report-01.md, controller-contract.md, discovery-01.md and maintainability-01.md. Reviewer regression commands are DISC-01, DISC-02 and DISC-03 above. There are no blocked/unchecked rows to omit. No advancement is performed here.

## 7. Discovery continuation

- Iteration/current bytes: correction 1; HEAD `1c1aff83da3cbc69ecfe6acc2235108118f2cc12`; diff SHA-256 `37967712998327168f349737c9d09b809b0affb78c01ecce86b3c88025d1894b`; separate index/worktree identities in section 1.
- Coverage rows: V-01 fail F-02; V-02 fail F-02 (R1 ownership passes); V-03 pass (R2); V-04 fail F-02 (R3); V-05 pass. No blocked/unchecked rows.
- Finding IDs: F-01 prior suggested P2, original demonstrated defects now rejected with current independent evidence; F-02 new suggested P2, demonstrated and unresolved. No acceptance disposition or approved deferral recorded.
- Finding/scenario continuity: prior V-01/V-02/V-04 failed F-01, V-03/V-05 passed. Producer claims correction ready and all scenarios passing. DISC-01 corroborates 11 tests, DISC-02 rejects original F-01 cases but demonstrates actor-policy siblings across five stages/three active states, DISC-03 corroborates bounded contention/cleanup. No incomplete discovery reason. Correction owner: implementer; evidence/aggregate owner: fresh discovery; authority/decision owner: separate acceptance reviewer. Refreshed conditional maintainability evidence remains its separate review owner's duty.
- Preparation/context: package brief/verification revision 1; preflight.md including Decision context; parent T-002 and cited plan; predecessor T-002.1 contract/acceptance-02 as recorded in preflight.
- Reviewer regressions: no file added; exact DISC-01 class command, DISC-02 inline reproducer and DISC-03 bounded contention command in section 4. Preserve F-01 six-stage/three-state and terminal-history tests; F-02 siblings include historical terminal actor preservation.
- Aggregate gate: not run; exact command and correction discovery owner in section 5; suppressed after decisive targeted F-02 failure.
- Next: separate task-acceptance-review with the complete input set in section 6.

## 8. Post-write scope verification

Expected exact post-write status (verified immediately after exclusive creation):

```text
A  skills/task-orchestrator/docs/tasks/T-002.2/controller-contract.md
A  skills/task-orchestrator/docs/tasks/T-002.2/correction-report-01.md
A  skills/task-orchestrator/docs/tasks/T-002.2/implementation-report.md
A  skills/task-orchestrator/docs/tasks/T-002.2/preflight.md
A  skills/task-orchestrator/docs/tasks/T-002.2/reviews/discovery-01.md
A  skills/task-orchestrator/docs/tasks/T-002.2/reviews/maintainability-01.md
M  skills/task-orchestrator/scripts/controller.py
M  skills/task-orchestrator/scripts/controller_state.py
M  skills/task-orchestrator/tests/test_controller.py
M  skills/task-orchestrator/tests/test_controller_git.py
M  skills/task-orchestrator/tests/test_controller_state.py
?? skills/task-orchestrator/docs/tasks/T-002.2/reviews/discovery-02.md
```

Only this new report entry differs. All pre-existing changed-path bytes and the index remain unchanged. No previous report was overwritten.
