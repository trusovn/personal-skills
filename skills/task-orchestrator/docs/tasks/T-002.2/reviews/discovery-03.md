# Task Review Discovery Report: T-002.2

| Field | Value |
|---|---|
| Producing stage | task-review-discovery |
| Coverage completeness | complete — V-01..V-05 and R1..R3 have current targeted dispositions |
| Discovery iteration | correction 2, following discovery-02 F-02 |
| Created | 2026-10-23, Europe/Lisbon |
| Repository root | /Users/mtrusov/work/skill-sources/personal-skills |
| Durable report path | skills/task-orchestrator/docs/tasks/T-002.2/reviews/discovery-03.md |
| Task brief | skills/task-orchestrator/docs/tasks/T-002.2/brief.md, revision 1 |
| Verification/context | verification.md revision 1; preflight.md including Decision context |
| Current submission | correction-report-02.md, READY_FOR_REVIEW; implementation-report.md; correction-report-01.md; controller-contract.md |

This report publishes evidence only. It gives no acceptance verdict, approved
deferral or advancement. It applies only to the identified reviewed bytes. It
does not review or authenticate itself.

## 1. Discovery provenance

This session authored no reviewed production or test bytes. Current probes are
independent of production authorship. The project-local task-review-discovery
skill and its report template were used, with project-local testing-discipline
for test-evidence assessment. No subagents, network calls, model launches,
installation updates, fixes or commits were used.

HEAD: `1c1aff83da3cbc69ecfe6acc2235108118f2cc12`.
SHA-256 of `git diff HEAD --binary`: `2665634287b646735a4db672d1830d1c92e581beae3632d5035f5fcbb583b2db`.
SHA-256 of `git ls-files --stage -z`: `cb8ac1d12ea579699c491b965b3201f69bd69e53e0cc41d4ec6b56ad2a79bbb4`.

The worktree controller/test blobs match correction-report-02's submitted
identities. Their index blobs still contain the earlier correction and differ
from the worktree. This report qualifies the worktree, not that older staged
implementation. See the separate identities below.

## 2. Findings and continuity

No findings.

- **F-01**, prior suggested P2: discovery-01 demonstrated active assignment/current
  identity and lifecycle inconsistencies. Discovery-02 reported original cases
  rejected. Current DISC-01 again exercises all six stages, both supplied
  fast/strong profiles and all three active states against mismatched identities,
  stage, selection and parent lifecycle. DISC-02 reruns the original valid control
  and six invalid variants: valid accepted, all invalid rejected. Historical
  terminal identity remains readable/replayable in DISC-01.
- **F-02**, prior suggested P2: discovery-02 demonstrated known actor profiles that
  contradict frozen stage selection. Producer correction-report-02 claims a
  shared-context actor check. Current DISC-01 corroborates the supplied profile/
  stage/state matrix, including verify null-actor and terminal historical actor
  preservation. DISC-02 independently constructs 39 wrong-known-actor cases over
  six stages and reserved/running/unknown; status rejects and exact-request replay
  refuses without byte changes. Valid controls remain readable. These observations
  corroborate the correction; they are not an acceptance disposition.

Credible sibling surfaces remain explicit: F-01 applies to all reservable stages,
selected task/current stage/current input/flow/candidate and terminal-parent
coherence; F-02 applies to every actor stage's frozen mode, correction's
implementation mode, verify's null actor and historical terminal actor preservation.
No whole-run authentication or production outcome-admission claim follows.

## 3. Completeness ledger

The ledger retained discovery-02's V-01..V-05 identities and was reconciled with
brief/verification revision 1 before aggregate launch. Submitted evidence for
each row is the named-method map in implementation-report.md and
correction-report-02.md. Those claims guided selection; current results below
come from this discovery.

| Row | Authority | Explicit material cases / setup and oracle | Submitted evidence | Independent current probe | Result |
|---|---|---|---|---|---|
| V-01 | AC-01 | Real initialized records; status/reload identity, references, outstanding findings, count, next actions; passed/failed/stale/blocked/missing/not_run, required omission blocked and optional repository-gate omission explicit; snapshots unchanged | Read-only status method and correction matrix | DISC-01 status/CLI/matrix; DISC-02 valid and invalid current actor/status controls | pass — current state is exposed or rejected consistently, without advancement |
| V-02 | AC-02/03; R1 | First reserve, exact replay after reload, changed key/request/version; one persisted owner; reserved/running/unknown block; terminal allows next; full assignment identity/actor; competing controller processes | Replay, active states, actor matrix, terminal history and contention methods | DISC-01; DISC-02 prior F-01 plus actor siblings; DISC-03 bounded separate-process race with one winner/one refusal/one record | pass — persisted ownership, replay and frozen active assignment demonstrated |
| V-03 | AC-04; R2 | Cycle zero; mixed check/review/repair corrections 1/2/3, reload/replay, unknown launch charge, fourth unchanged/intervention; repair before implementation retained after fresh preflight; free preflight/evidence retries cannot repair | Shared-budget, pre-initial repair and free-retry methods | DISC-01 executes successive real reservations and labelled successor transitions, reloads, count/assignment and byte-snapshot oracles | pass — one charge per authorized correction and three-cycle limit retained |
| V-04 | AC-03/05; R3 | Invalid/stale version/task/role/stage/key/reason; missing/failed/stale/wrong-task/wrong-role/nonterminal readiness; weakened policy; public run-next/inspect/revise-flow/update guards; no writes on refusal | Invalid requests/readiness/legacy and CLI methods; correction matrix | DISC-01 actual entry points; DISC-02 executable valid/invalid controls and status/replay refusal | pass — no tested authority/readiness/legacy bypass |
| V-05 | AC-05 | Exact public status/reserve/replay/refusal examples and embedded assignment fields; successor seams; no public fixture/state setter | controller-contract.md and source/CLI comparison | Read controller/state diff and contract; DISC-01 public CLI tests; trace shared context, lock, atomic ledger publication, legacy guards | pass — documented interface matches implemented boundary |

R1 maps to V-02; R2 to V-03; R3 to V-04. No required/material row is blocked or
unchecked. Terminal/readiness/evidence fixtures supply explicit successor setup;
they do not prove T-003/004/005 production admission. All targeted probes finished
before the aggregate was launched.

## 4. Adversarial checks

| Invariant | Current cases / evidence |
|---|---|
| Exact ownership and order | Zero-owner initialization; one reservation; two-owner original reproducer rejected; only latest active assignment; reserved/running/unknown matrix; real process competition, DISC-01..03 |
| Parent/child and current authority | Stopped/initialized/finalizing parents, wrong selection/stage/input/policy/flow revision/digest/candidate rejected in matrix; original F-01 rerun corroborates six original variants |
| Frozen actor selection | Six stages, three active states; fast/strong permanent matrix; independent fast-profile 39 wrong-known-actor cases, including verify actor-bearing assignments |
| Terminal history | Different historical authority/candidate/actor stays readable and exact-key replayable; does not become current active operation |
| Correction lifecycle | Successive operations with legitimate fixture terminalization between real reservations; mixed reasons, pre-initial repair, replay and restart; fourth unchanged |
| Readiness | Valid terminal preflight control; absent/failed/stale/nonterminal/wrong role/task/operation rejected; repair clears readiness |
| Executable validator | No separate ledger JSON Schema. Original probe executes ledger validator on a valid assignment and six deliberately invalid records; public authority context additionally rejects wrong known actors. Schema/syntax checks were not counted as behavioral success |

No new process-lifecycle implementation is in scope. DISC-03 exercises the actual
local process boundary with observable readiness and bounded completion, group
absence and closed pipes. All fixture processes complete; no fixture process
survives. The existing contention test's unbounded initial readline remains the
prior maintainability warning; its successful run is not timeout-robustness proof.

## 5. Independent commands and results

All behavioral commands ran from the repository root with local Python and
disposable Git/run fixtures. No dependencies were installed. No reviewed files
were changed. Successor seeding is test-only. The exact commands below are
reviewer regressions; no persistent regression file was added.

### DISC-01 — current targeted reservation class

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills.task-orchestrator.tests.test_controller.ControllerReservationTest
```

Exit 0: 11 tests passed in 16.088 seconds. Covers all row-specific methods
described above, including current correction matrix and terminal actor history.
Fixtures tear down temporary repositories/runs and wait for their child processes.

### DISC-02 — original regression and independently constructed actor siblings

```sh
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
from pathlib import Path
import importlib,json,copy
old=Path('skills/task-orchestrator/docs/tasks/T-002.2/reviews/discovery-01.md').read_text()
source=old.split("python3 - <<'PROBE'\n",1)[1].split('\nPROBE',1)[0]
exec(compile(source,'discovery-01:DISC-02','exec'))
m=importlib.import_module('skills.task-orchestrator.tests.test_controller')
t=m.ControllerReservationTest();t.setUp();cases=0
try:
 for stage,prior in [('preflight',None),('implement',None),('correction',None),('verify','implement'),('semantic_review','verify'),('acceptance','semantic_review')]:
  c,r=t.create_initialized_run(name='independent-'+stage)
  if stage!='preflight':t.ready_implementation(r)
  if prior:
   b=t.read_ledger(r);t.seed_successor(r,stage=stage,candidate_sha256='a'*64,evidence={prior:{'status':'passed','inputs_sha256':b['inputs_sha256'],'candidate_sha256':'a'*64}})
  if stage=='correction':t.seed_successor(r,correction_request='environment_repair')
  assert t.reserve(r,stage,'profile','environment_repair' if stage=='correction' else 'initial')['status']=='reserved'
  base=t.read_ledger(r)
  for state in ['reserved','running','unknown']:
   valid=copy.deepcopy(base);valid['actor_operations'][-1]['state']=state
   (r/'ledger.json').write_text(json.dumps(valid));c._validate_ledger(valid)
   assert c.status_run(r)['status']=='ok'
   for actor in [{'model':'gpt-6.1-sol','reasoning':x} for x in ['low','medium','high']]:
    if actor==valid['actor_operations'][-1]['assignment']['actor']:continue
    invalid=copy.deepcopy(valid);invalid['actor_operations'][-1]['assignment']['actor']=actor
    (r/'ledger.json').write_text(json.dumps(invalid));before=t.snapshot(r)
    try:c.status_run(r)
    except ValueError:pass
    else:raise AssertionError('invalid actor status accepted')
    result=m.load_controller().reserve_operation(r,**invalid['actor_operations'][-1]['request'])
    assert result['status']=='refused' and result['reason']=='authority_or_lock_unavailable',result
    assert before==t.snapshot(r);cases+=1
 print('F-02 independent actor cases rejected:',cases)
finally:t.tearDown()
PY
```

Exit 0. Original output: valid active assignment accepted; two owners, wrong input,
wrong flow revision, wrong candidate, wrong current stage and stopped parent all
rejected. Additional output: `F-02 independent actor cases rejected: 39`.
Every actor mutation gets a status error and structured replay refusal; snapshot
equality confirms unchanged authority/task bytes. No processes are spawned by
this probe; fixture teardown removes its temporary state.

### DISC-03 — bounded contention and observable cleanup

```sh
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
from pathlib import Path
report=Path('skills/task-orchestrator/docs/tasks/T-002.2/reviews/discovery-02.md').read_text()
source=report.split("python3 - <<'PY'\n")[2].split('\nPY',1)[0]
exec(compile(source,'discovery-02:DISC-03','exec'))
PY
```

Exit 0. Executes the exact bounded DISC-03 body already preserved in discovery-02,
rather than copying a prior result. Output: `one winner, one refusal, one persisted
owner`; `all child processes/groups disappeared; pipes released; temporary state
removed`. The two children each start a new session, synchronize via readiness/
stdin, and call the real public controller. Readiness is bounded at 5 seconds,
communication at 10 seconds and reap at 5 seconds. Each child spawns no descendants;
group absence plus child exit and closed pipes are asserted.

### DISC-04 — designated aggregate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'
```

Exit 1: 198 tests, 49.554 seconds; 197 pass, one failure, no errors/skips reported.
The sole failure is `test_retrieval_surface.RetrievalSurfaceTest.test_expected_current_references_exist`,
`tests/test_retrieval_surface.py:45`. Its exact docs-directory inventory expects
four entries. Extra entries are correction-and-disposition-options.md, tasks,
project-plan-review-single-task-sbx.md, direction-single-task-sbx.md,
project-plan-review.md and project-plan-review-single-task-sbx-r2.md.

Current static baseline corroboration:

```sh
git ls-tree --name-only HEAD:skills/task-orchestrator/docs
git diff HEAD -- skills/task-orchestrator/tests/test_retrieval_surface.py
```

All six extra entries already exist in HEAD; test diff is empty. This
independently corroborates the preflight/prior-acceptance recorded baseline
failure. No baseline suite rerun or waiver was added. Aggregate fixture children
completed with the suite; no hung process/pipe prevented exit.

### Static and identity command record

Read active local skills/template, task brief/verification/preflight/submissions/
contract and discovery-01/02/maintainability-01, parent brief, predecessor contract/
acceptance-02, architecture map, direction and cited plan. Used `rg --files` for
package/instruction inventory and `rg -n` for cited plan invariants/interfaces.
Inspected `git diff HEAD --stat`, `git diff HEAD -- <controller/state/test paths>`
and unstaged correction diff with `git diff -- <controller/test paths>`.
Recorded `git rev-parse HEAD`, `git status --short --untracked-files=all`,
`git rev-parse :<path>`, `git hash-object <path>`, SHA-256 of
`git diff HEAD --binary` and `git ls-files --stage -z`. These establish
scope/identity, not behavior. An initial identity-capture attempt printed expected
missing-index diagnostics for untracked files; it was repeated with stderr
suppressed and did not change state.

## 6. Aggregate-gate record

| Field | Value |
|---|---|
| Exact command | DISC-04 above |
| Status | failed — 197/198, one established pre-existing retrieval inventory assertion |
| Owner/stage | This independent correction-2 discovery |
| Reason | Current F-01/F-02 regressions, all safely runnable V-01..V-05/R1..R3 targeted cases and bounded contention were clean; cross-module controller/state impact justified the designated aggregate |
| Reconciliation | No selected adversarial row remained, no blocked/unchecked row, no targeted failure suppressed the gate, no gate was added |
| Current evidence | DISC-01..03 clean; DISC-04 failure independently compared with HEAD inventory and unchanged assertion |

This is a failed aggregate, not a green gate or an approved baseline deferral.
Conditional review owners retain their duties.

## 7. Scope and baseline comparison

Preflight began at the same HEAD with clean implementation state. Current staged
task work and two unstaged correction files are accounted for by the implementation/
correction submissions. The Git test dispatch rename is declared reused-fixture
maintenance; original oracles remain. The untracked advisory document is
pre-existing user work outside this task and was neither reviewed nor edited.
Correction-report-02 is current producer evidence, not a reviewer-owned change.
No unexplained/inseparable overlap was found.

| Path | Index Git blob | Worktree Git blob |
|---|---|---|
| `skills/task-orchestrator/docs/tasks/T-002.2/controller-contract.md` | `5224ed8f1e895c60e6e98ce81a7b0e600987cc27` | `5224ed8f1e895c60e6e98ce81a7b0e600987cc27` |
| `skills/task-orchestrator/docs/tasks/T-002.2/correction-report-01.md` | `03b61a84a5157d774301da48f07b264072344ab4` | `03b61a84a5157d774301da48f07b264072344ab4` |
| `skills/task-orchestrator/docs/tasks/T-002.2/implementation-report.md` | `13d092ce4c83ee92bdfa7bb270b5054dcbb1137f` | `13d092ce4c83ee92bdfa7bb270b5054dcbb1137f` |
| `skills/task-orchestrator/docs/tasks/T-002.2/preflight.md` | `d7b7f740dc0d82c1fa50c779ee7cc3381c5722da` | `d7b7f740dc0d82c1fa50c779ee7cc3381c5722da` |
| `skills/task-orchestrator/docs/tasks/T-002.2/reviews/discovery-01.md` | `026622a51f89ac701b0c558446deaa5d714951d7` | `026622a51f89ac701b0c558446deaa5d714951d7` |
| `skills/task-orchestrator/docs/tasks/T-002.2/reviews/discovery-02.md` | `55b35c8525f380a1e4b202c32444b5812310a997` | `55b35c8525f380a1e4b202c32444b5812310a997` |
| `skills/task-orchestrator/docs/tasks/T-002.2/reviews/maintainability-01.md` | `6d52beeed98bcedccd968dcf6830d8280f89113b` | `6d52beeed98bcedccd968dcf6830d8280f89113b` |
| `skills/task-orchestrator/scripts/controller.py` | `e435948d4cc7a9751a694b32221d51c83de84549` | `0a21618a11b192bae891c373f0ae61caf0c0499b` |
| `skills/task-orchestrator/scripts/controller_state.py` | `a27b1367fe7370ee64defc78653c4a6bd88dd49b` | `a27b1367fe7370ee64defc78653c4a6bd88dd49b` |
| `skills/task-orchestrator/tests/test_controller.py` | `cd8ff075f2b976f38d5bf7cdea4f1ef741ae6504` | `6bf2b95a1f6ca9a398f8beccf03c9b9c4997acff` |
| `skills/task-orchestrator/tests/test_controller_git.py` | `6d3e24b2cd8e308e4cbb5d75d957f5a42531ba80` | `6d3e24b2cd8e308e4cbb5d75d957f5a42531ba80` |
| `skills/task-orchestrator/tests/test_controller_state.py` | `038ba6ff3af9a0f4257e589344303d0e719e8657` | `038ba6ff3af9a0f4257e589344303d0e719e8657` |
| `docs/advisory-code-maintainability-signals.md` | absent (untracked) | `265b0e41c531ecb821b33dbbd2a246223ca8777a` |
| `skills/task-orchestrator/docs/tasks/T-002.2/correction-report-02.md` | absent (untracked) | `dc53a6457b83b09891f02ef3d5d0023a98ec0636` |

Brief/verification, parent/plan/direction and predecessor authority have no
worktree diff in this invocation. Current active source bytes match the
correction handoff identities; index differences are explicitly retained.
Runtime fixtures are disposable and external to the repository.

Exact reviewed status immediately before report creation:

```text
A  skills/task-orchestrator/docs/tasks/T-002.2/controller-contract.md
A  skills/task-orchestrator/docs/tasks/T-002.2/correction-report-01.md
A  skills/task-orchestrator/docs/tasks/T-002.2/implementation-report.md
A  skills/task-orchestrator/docs/tasks/T-002.2/preflight.md
A  skills/task-orchestrator/docs/tasks/T-002.2/reviews/discovery-01.md
A  skills/task-orchestrator/docs/tasks/T-002.2/reviews/discovery-02.md
A  skills/task-orchestrator/docs/tasks/T-002.2/reviews/maintainability-01.md
MM skills/task-orchestrator/scripts/controller.py
M  skills/task-orchestrator/scripts/controller_state.py
MM skills/task-orchestrator/tests/test_controller.py
M  skills/task-orchestrator/tests/test_controller_git.py
M  skills/task-orchestrator/tests/test_controller_state.py
?? docs/advisory-code-maintainability-signals.md
?? skills/task-orchestrator/docs/tasks/T-002.2/correction-report-02.md
```

## 8. Questions, unchecked work and residual limits

No blocked/unchecked scenario row and no unresolved task finding from these probes.

| Item | Evidence / limit | Next owner |
|---|---|---|
| Conditional maintainability evidence | correction-report-02 requests fresh maintainability before discovery. Only maintainability-01 exists; its blobs predate both corrections. This discovery does not substitute for or waive that separate review. | Coordinator / fresh maintainability reviewer, before acceptance |
| Failed aggregate | Current sole failure established pre-existing by HEAD inventory and unchanged test; no approval or waiver recorded here | Separate acceptance reviewer evaluates the evidence; baseline maintenance remains its existing owner |
| Harness warning | Original contention test has unbounded readiness readline; independent DISC-03 supplies bounded evidence for this pass | Existing test-maintenance owner |
| Successor production behavior | Actor launch/terminal/readiness admission T-003, semantic routing T-004/005, whole-input revision T-002.3 and final completion excluded | Respective successor tasks |
| Authentication | Internally consistent whole-run rewriting is not authenticated by mutable digests | No stronger claim made |

## 9. Coverage and exact next route

Coverage is complete for this bounded discovery: every material scenario has a
current disposition, prior findings were corroborated against corrected worktree
bytes, and aggregate ownership/result is explicit.

Next: coordinator obtains the correction handoff's outstanding fresh
maintainability review, then starts a separate task-acceptance-review call. Supply
brief.md revision 1, verification.md revision 1, preflight.md including Decision
context, current scoped worktree diff and identities, this report,
controller-contract.md, implementation-report.md, correction-report-01/02.md,
discovery-01/02.md, prior/current maintainability evidence and predecessor
T-002.1 contract/acceptance-02. Supply DISC-01..03 regression commands and the
failed DISC-04 gate record. There are no blocked/unchecked scenario rows to omit.
This report makes no acceptance decision and advances no work.

## 10. Discovery continuation

- Iteration/current byte identity: correction 2; HEAD `1c1aff83da3cbc69ecfe6acc2235108118f2cc12`; tracked worktree diff SHA-256 `2665634287b646735a4db672d1830d1c92e581beae3632d5035f5fcbb583b2db`; index/worktree identities in section 7. Scope is worktree, including unstaged correction.
- Coverage rows: V-01 pass; V-02 pass (R1); V-03 pass (R2); V-04 pass (R3); V-05 pass. No blocked/unchecked scenario.
- Finding IDs: F-01 prior suggested P2, original and sibling regressions reject invalid records now; F-02 prior suggested P2, wrong actors rejected across current active-state/stage matrix, terminal history preserved. No new finding or acceptance disposition.
- Finding/scenario continuity: prior V-01/V-02/V-04 failed F-02, V-03/V-05 passed; producer correction-report-02 claims READY_FOR_REVIEW. Current DISC-01 11/11, DISC-02 original F-01 plus 39 actor mutations, DISC-03 bounded race corroborate corrected bytes. No incomplete scenario reason. Correction owner=implementer; evidence/aggregate owner=this independent discovery; authority/decision owner=separate acceptance reviewer. F-01 sibling=current authority/parent lifecycle across all six stages; F-02 sibling=all actor stages, correction implementation mode, verify null actor and historical terminal actor. Fresh maintainability evidence remains its separate owner's outstanding duty.
- Preparation/context: package brief revision 1, verification revision 1, preflight including Decision context, parent T-002 and cited plan/direction, predecessor T-002.1 contract/acceptance-02.
- Reviewer regressions: no file added; exact DISC-01 class command, DISC-02 inline independent probe and DISC-03 extraction/re-execution command in section 5. Permanent regression methods are test_active_assignment_must_match_current_ledger and test_terminal_assignment_retains_historical_authority in tests/test_controller.py.
- Aggregate gate: DISC-04 failed, 197/198, exact command in section 5; owner=this correction discovery, justified after clean targeted reconciliation. Sole unchanged inventory assertion already conflicts with HEAD docs. No waiver.
- Next: coordinator obtains fresh maintainability evidence for current correction, then invokes separate task-acceptance-review with section 9's complete packet.

## 11. Post-write scope verification

Exact expected post-write status, checked immediately after exclusive creation:

```text
A  skills/task-orchestrator/docs/tasks/T-002.2/controller-contract.md
A  skills/task-orchestrator/docs/tasks/T-002.2/correction-report-01.md
A  skills/task-orchestrator/docs/tasks/T-002.2/implementation-report.md
A  skills/task-orchestrator/docs/tasks/T-002.2/preflight.md
A  skills/task-orchestrator/docs/tasks/T-002.2/reviews/discovery-01.md
A  skills/task-orchestrator/docs/tasks/T-002.2/reviews/discovery-02.md
A  skills/task-orchestrator/docs/tasks/T-002.2/reviews/maintainability-01.md
MM skills/task-orchestrator/scripts/controller.py
M  skills/task-orchestrator/scripts/controller_state.py
MM skills/task-orchestrator/tests/test_controller.py
M  skills/task-orchestrator/tests/test_controller_git.py
M  skills/task-orchestrator/tests/test_controller_state.py
?? docs/advisory-code-maintainability-signals.md
?? skills/task-orchestrator/docs/tasks/T-002.2/correction-report-02.md
?? skills/task-orchestrator/docs/tasks/T-002.2/reviews/discovery-03.md
```

The only added entry is this report. Post-write checking compares all prior
changed/untracked worktree blobs, the full index identity, HEAD and tracked
diff identity with section 1/7. No earlier report is overwritten.

