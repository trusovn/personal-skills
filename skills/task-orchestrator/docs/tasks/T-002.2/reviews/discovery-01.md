# Task Review Discovery Report: T-002.2

| Field | Value |
|---|---|
| Producing stage | task-review-discovery |
| Coverage completeness | complete — all V-01..V-05 and R1..R3 have current dispositions; one confirmed finding |
| Iteration | first discovery |
| Created | 2026-10-23T16:49:17.761704+01:00 |
| Repository | /Users/mtrusov/work/skill-sources/personal-skills |
| Report | skills/task-orchestrator/docs/tasks/T-002.2/reviews/discovery-01.md |
| Authority | brief.md revision 1; verification.md revision 1 |
| Preparation/context | preflight.md, including Decision context; parent T-002 brief; local-harness-orchestration-plan.md IF-001 and INV-001/002/005/007/008 |
| Submission | implementation-report.md, READY_FOR_REVIEW; controller-contract.md; maintainability-01.md |

This report publishes evidence only. It gives no acceptance verdict, approved deferral, or advancement. It applies only to the reviewed bytes below and does not review or authenticate itself.

## 1. Provenance and scope

This session authored no reviewed production or test bytes. Evidence is independent of implementation authorship. Active instructions were the project-local task-review-discovery skill and its report template, the supplied repository instructions, and project-local testing-discipline for assessment of test evidence. No subagents were launched.

HEAD: `1c1aff83da3cbc69ecfe6acc2235108118f2cc12`. The preflight baseline is the same commit. The five implementation/test index blobs match maintainability-01.md. Every staged path is accounted for by the submission. The controller Git test change is the declared reused-fixture dispatch rename. The preflight and prior maintainability report are preparation/prior evidence, not reviewer-owned implementation. No unexplained overlap was found. No unstaged tracked changes exist. No source skill was substituted for the installed skill.

Index and worktree Git blob identities, separately measured:

| Path | Index | Worktree |
|---|---|---|
| `skills/task-orchestrator/docs/tasks/T-002.2/controller-contract.md` | `5224ed8f1e895c60e6e98ce81a7b0e600987cc27` | `5224ed8f1e895c60e6e98ce81a7b0e600987cc27` |
| `skills/task-orchestrator/docs/tasks/T-002.2/implementation-report.md` | `13d092ce4c83ee92bdfa7bb270b5054dcbb1137f` | `13d092ce4c83ee92bdfa7bb270b5054dcbb1137f` |
| `skills/task-orchestrator/docs/tasks/T-002.2/preflight.md` | `d7b7f740dc0d82c1fa50c779ee7cc3381c5722da` | `d7b7f740dc0d82c1fa50c779ee7cc3381c5722da` |
| `skills/task-orchestrator/scripts/controller.py` | `e435948d4cc7a9751a694b32221d51c83de84549` | `e435948d4cc7a9751a694b32221d51c83de84549` |
| `skills/task-orchestrator/scripts/controller_state.py` | `4133cb2228e29aed278df6a055d620d604335617` | `4133cb2228e29aed278df6a055d620d604335617` |
| `skills/task-orchestrator/tests/test_controller.py` | `de87f65ad8e8422ca616af004fe41ed6311097aa` | `de87f65ad8e8422ca616af004fe41ed6311097aa` |
| `skills/task-orchestrator/tests/test_controller_git.py` | `6d3e24b2cd8e308e4cbb5d75d957f5a42531ba80` | `6d3e24b2cd8e308e4cbb5d75d957f5a42531ba80` |
| `skills/task-orchestrator/tests/test_controller_state.py` | `038ba6ff3af9a0f4257e589344303d0e719e8657` | `038ba6ff3af9a0f4257e589344303d0e719e8657` |

SHA-256 of `git diff HEAD --binary`: `36b3269cf6e845712b83109902c2caf19c10272c541d79bac0652a2ddc9336d0`.

Exact status before report creation:

```text
A  skills/task-orchestrator/docs/tasks/T-002.2/controller-contract.md
A  skills/task-orchestrator/docs/tasks/T-002.2/implementation-report.md
A  skills/task-orchestrator/docs/tasks/T-002.2/preflight.md
M  skills/task-orchestrator/scripts/controller.py
M  skills/task-orchestrator/scripts/controller_state.py
M  skills/task-orchestrator/tests/test_controller.py
M  skills/task-orchestrator/tests/test_controller_git.py
M  skills/task-orchestrator/tests/test_controller_state.py
?? skills/task-orchestrator/docs/tasks/T-002.2/reviews/
```

Expanded untracked inventory before creation:

```text
A  skills/task-orchestrator/docs/tasks/T-002.2/controller-contract.md
A  skills/task-orchestrator/docs/tasks/T-002.2/implementation-report.md
A  skills/task-orchestrator/docs/tasks/T-002.2/preflight.md
M  skills/task-orchestrator/scripts/controller.py
M  skills/task-orchestrator/scripts/controller_state.py
M  skills/task-orchestrator/tests/test_controller.py
M  skills/task-orchestrator/tests/test_controller_git.py
M  skills/task-orchestrator/tests/test_controller_state.py
?? skills/task-orchestrator/docs/tasks/T-002.2/reviews/maintainability-01.md
```

## 2. Findings

### F-01 [suggested P2] Active actor records can contradict current run identity and terminal state

- Location: `skills/task-orchestrator/scripts/controller_state.py:1201` (active assignment checks) and `:1211` (pointer/state check); exposed by `controller.py` status and replay.
- Trigger: create a real initialized run, reserve preflight, seed its terminal readiness using the existing labelled successor fixture, then reserve implementation. Independently alter (a) the active assignment's flow revision, (b) its candidate digest, (c) the ledger current stage, or (d) the parent to stopped with null selected task/cursor. Keep the active actor and pointer intact. Each resulting record passes the executable ledger validator. Public status returns `ok`, and replay returns the contradictory assignment as `replayed`.
- Consequence: a replacement coordinator receives internally contradictory current authority/operation information as a valid snapshot. A stopped parent can retain a reserved child and return that child's assignment. This weakens the persisted guard boundary consumed by successor tasks.
- Affected authority: AC-01 truthful status, AC-02 bound assignment identity, AC-03 preserved operation identity/no bypass; V-01/V-02/V-04 and R1/R3.
- Broken invariant: the active operation must agree with current run/task/stage/flow/candidate identity and cannot remain active beneath a terminal stopped parent. Current validation compares only three authority digests, position, and pointer, and excludes only `finalizing` as a parent state.
- Credible sibling surfaces: running and unknown active records; candidate-bound verify/collection/acceptance assignments; selected-task identity and current-stage coherence. These share the active-operation validation boundary. The probe directly demonstrates reserved implementation; sibling cases require correction regressions, not an assertion that all were executed.
- Smallest corrective direction: validate the complete active-operation/current-ledger relationship, including permitted parent lifecycle states, before status or replay exposes it; preserve historical terminal records without requiring them to match current authority.
- Limits: these are deliberately inconsistent persisted records, not a claim that the normal reservation producer emits them, and not an authentication/tamper-resistance claim. T-003 outcome admission remains outside this task; the present finding concerns this task's executable persisted validator and public readers.

## 3. Completeness ledger

The ledger was derived from the brief and verification design before aggregate consideration. Submitted evidence for every row is the named method map in implementation-report.md; it is not treated as independent proof. DISC-01 independently reran all nine reservation methods. DISC-02 added adversarial current-state checks.

| Row | AC / risk | Cases and setup/oracle | Current independent evidence | Disposition |
|---|---|---|---|---|
| V-01 | AC-01 | Real ledger/status/reload; passed, failed, stale, blocked, missing, not_run, mandatory omission, optional repository-gate omission; compare all run/task bytes and identities | DISC-01 status test passed; DISC-02 status accepts contradictory current identity/parent | fail — F-01; ordinary evidence/read-only cases pass |
| V-02 | AC-02/03, R1 | First/replay/reload; changed key/request; competing version/process; reserved/running/unknown vs terminal; exact one assignment; real lock and records | DISC-01 replay, active states, process contention and CLI tests passed. DISC-02 rejects two owners/wrong input, accepts inconsistent active/current identity and stopped parent | fail — F-01; normal reservation/cardinality cases pass |
| V-03 | AC-04, R2 | Cycle zero; check/review/repair charges 1/2/3; fourth unchanged; uncertainty; repair before implementation and preflight again; free preflight/evidence retries; real reload between requests | DISC-01 shared budget, pre-initial repair and free-retry tests passed, with byte snapshots and assignment/count oracles | pass — selected finite budget cases independently exercised |
| V-04 | AC-03/05, R3 | Invalid/stale version/task/role/stage/reason; weak policy; absent/failed/stale/wrong/nonterminal readiness; public run-next, inspect, revise-flow and generic-update refusal; unchanged bytes | DISC-01 invalid requests, active states and public CLI tests passed; DISC-02 shows invalid persisted state still read/replayed | fail — F-01; ordinary request/readiness/legacy guard cases pass |
| V-05 | AC-05 | Compare exact status/reserve/assignment/replay/refusal contract with public CLI, implementation and successor seams; no public fixture setter | Static source/contract comparison plus DISC-01 CLI results; embedded record fields and request examples agree, production outcome/readiness admission explicitly deferred | pass — documented interface and boundaries match; validator defect tracked separately |

No required row is blocked or unchecked. R1 maps to V-02, R2 to V-03, R3 to V-04; none disappear behind the green class result.

## 4. Adversarial checks and commands

Working directory for all commands: repository root above. Environment: local Python, no network/models/sbx. Existing temporary Git repositories and run records were removed by fixture teardown. No repository tests or fixtures were edited.

**DISC-01**

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills.task-orchestrator.tests.test_controller.ControllerReservationTest
```

Exit 0: nine tests passed in 3.032 seconds. This exercises real status/reserve CLI and library calls, lock/publication, reloaded persisted history and synchronized separate controller processes. The two contention children only import/controller-reserve and do not launch descendants; both `communicate(timeout=10)` calls completed, released inherited pipes, and `wait()` completed in cleanup. No actor or fixture process remains. The initial readiness `readline()` is unbounded in the existing fixture, as already noted by maintainability-01; this successful run is not proof of timeout robustness.

**DISC-02 — executable validator and public boundary regression**

Exact reproducible command:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PROBE'
import importlib,json,copy
m=importlib.import_module('skills.task-orchestrator.tests.test_controller')
t=m.ControllerReservationTest(); t.setUp()
try:
 c,r=t.create_initialized_run(); t.ready_implementation(r)
 x=t.reserve(r,'implement','initial'); assert x['status']=='reserved'
 base=t.read_ledger(r); c._validate_ledger(base); print('valid active assignment: accepted')
 for name in ['two owners','wrong input','wrong flow revision','wrong candidate','wrong current stage','stopped parent']:
  v=copy.deepcopy(base)
  if name=='two owners': v['actor_operations'][0]['state']='unknown'
  elif name=='wrong input': v['actor_operations'][-1]['assignment']['inputs_sha256']='b'*64
  elif name=='wrong flow revision': v['actor_operations'][-1]['assignment']['flow_revision']+=1
  elif name=='wrong candidate': v['actor_operations'][-1]['assignment']['candidate_sha256']='a'*64
  elif name=='wrong current stage': v['current_step']='verify'
  else: v.update(state='stopped',selected_task_id=None,current_step=None)
  (r/'ledger.json').write_text(json.dumps(v))
  try:
   c._validate_ledger(v); status=c.status_run(r)
   replay=c.reserve_operation(r,**v['actor_operations'][-1]['request'])
   print(name,': ACCEPTED status=',status['status'],'replay=',replay['status'])
  except ValueError as e: print(name,': rejected',str(e))
finally: t.tearDown()
PROBE
```

Executed equivalent loop used `(name, None)` pairs instead of the name-only list; all setup, mutations and checks were identical. Exit 0 is probe completion, not a behavioral success claim. Observed output:

```text
valid active assignment: accepted
two owners : rejected Active assignment authority mismatch
wrong input : rejected Active assignment authority mismatch
wrong flow revision : ACCEPTED status= ok replay= replayed
wrong candidate : ACCEPTED status= ok replay= replayed
wrong current stage : ACCEPTED status= ok replay= replayed
stopped parent : ACCEPTED status= ok replay= replayed
```

The valid instance and deliberately invalid wrong-input/two-owner controls exercise the actual validator. F-01 cases show additional invalid instances it fails to reject. No separate JSON schema exists for these fields. DISC-02 uses labelled successor setup only; it does not assert production outcome admission. No fixture worker processes are spawned by this probe.

Static commands inspected `git diff HEAD` for both scripts, current tests and the package documents; `git ls-files -s`, `git diff --name-only`, `git rev-parse HEAD`, and status snapshots establish scope/index/worktree identity. The state test delta preserves distinct zero-correction and over-limit rejection while allowing retained repair charges. No aggregate or owning module suite was copied from the implementer as current discovery evidence.

## 5. Aggregate record

- Exact designated command: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'`.
- Status: **not run**.
- Owner/stage: this independent initial discovery.
- Reason: decisive DISC-02 failure; the skill suppresses an aggregate after targeted failure. No diagnostic aggregate was authorized or added. All material rows have targeted evidence, with failures retained above.
- Prior baseline: preflight records an existing retrieval-inventory aggregate failure. That claim was not requalified and does not excuse F-01. A fresh correction discovery owns any justified aggregate after current targeted evidence is clean.

## 6. Residual risks and next route

No production actor launch, terminal/readiness admission, semantic outcome routing, input revision, or completion publication is claimed; those are excluded successor tasks. No live/networked/slow checks were run. Prior maintainability evidence is context only. No previous discovery finding or acceptance disposition exists for this package.

Coverage is complete for the selected task-derived finite cases, with F-01 unresolved. Next: a separate task-acceptance-review call consumes brief.md revision 1, verification.md revision 1, preflight.md including Decision context, current scoped diff, implementation-report.md, controller-contract.md, maintainability-01.md and this report. There are no blocked/unchecked rows. No acceptance decision is made here.

## 7. Discovery continuation

- Iteration/current bytes: first discovery; HEAD `1c1aff83da3cbc69ecfe6acc2235108118f2cc12`; exact index/worktree identities above.
- Coverage: V-01 fail F-01; V-02 fail F-01; V-03 pass; V-04 fail F-01; V-05 pass. R1/R3 fail via their affected rows; R2 pass. No blocked/unchecked rows.
- Findings: F-01 suggested P2, new and unresolved; no prior finding status or approved deferral.
- Continuity: producer claims all scenarios pass; independent DISC-01 confirms nine ordinary tests, DISC-02 demonstrates the persisted coherence gap. Correction owner: implementer after separate decision; evidence owner: fresh discovery on corrected bytes; authority/decision owner: separate acceptance reviewer. Siblings: running/unknown assignments, candidate-bound later stages and selected/current identity.
- Preparation/context: brief and verification revision 1; preflight.md Decision context; accepted predecessor T-002.1 controller-contract.md and reviews/acceptance-02.md as recorded by preflight.
- Reviewer regressions: no test file added; reproduce DISC-02 from this report and rerun the exact DISC-01 command. Correction review must cover the named siblings.
- Aggregate: not run; designated command in section 5, initial discovery owner, suppressed after targeted failure.
- Next: separate task-acceptance-review with the complete input set listed in section 6.

## 8. Post-write scope verification

The post-write short status is unchanged (the reviews directory was already untracked). Expanded status adds only:

```text
?? skills/task-orchestrator/docs/tasks/T-002.2/reviews/discovery-01.md
```

All prior index/worktree bytes and the prior untracked maintainability report remain unchanged.
