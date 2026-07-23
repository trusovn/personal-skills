# Task Brief: `S3-04` — Extend the Stage 3 state model

## Identity and artifact status

| Field | Value |
|---|---|
| Task ID | `S3-04` |
| Artifact status | `ready_for_preflight` |
| Producing stage | `task-brief-designer` |
| Created at | `2026-07-17T11:03:14+01:00` |
| Repository root | `/Users/mtrusov/work/skill-sources/personal-skills` |
| Primary authority | `skills/task-orchestrator/docs/stage-3-plan.md#Task index and dependency graph` (`S3-04` row), together with `#Settled decisions and constraints` and `#Architecture assessment after S3-01 through S3-03` |
| Dependencies | `S3-02` — complete per `skills/task-orchestrator/docs/stage-3-tasks/S3-02-result.md`; blocks `S3-05` and `S3-09` |

## Outcome

Stage 3 run/task transitions, ledger coherence, repeated dependency-ready
selection, monotonic expected-revision updates, and one non-blocking per-run
mutation lock are executable contracts before later CLI commands depend on
them.

## Authoritative inputs and knowledge ledger

| Kind | Path or statement | Relevance |
|---|---|---|
| Authoritative input | Repository `AGENTS.md` instructions supplied for `/Users/mtrusov/work/skill-sources/personal-skills` in the design request | Requires explicit assumptions, surgical scope, progressive behavioral verification, preservation of user work, and the 25–35-call soft stop. |
| Authoritative input | `skills/task-orchestrator/docs/stage-3-plan.md#Entry contract` | Defines the Stage 2 evidence and baseline that must exist before Stage 3 implementation. |
| Authoritative input | `skills/task-orchestrator/docs/stage-3-plan.md#Settled decisions and constraints` | Freezes sequential, single-worktree, standard-library-only operation, explicit selection, no retry command, and no automatic next-task launch. |
| Authoritative input | `skills/task-orchestrator/docs/stage-3-plan.md#Architecture assessment after S3-01 through S3-03` | Assigns pure state rules to `controller_state.py`, CLI/use cases and the per-run lock to `controller.py`, and specifies lock/revalidation lifetime. |
| Authoritative input | `skills/task-orchestrator/docs/stage-3-plan.md#Durable Stage 3 records` | Requires append-only attempt/turn history and nullable closure, verification, decision, and operation references without rewriting earlier records. |
| Authoritative input | `skills/task-orchestrator/docs/stage-3-plan.md#Task execution contract` and `#Stage-wide verification progression` | Defines implementation authority, fail-first evidence, progressive commands, and forbidden live/network/destructive work. |
| Authoritative input | `skills/task-orchestrator/docs/controller-contract.md#State model` | Defines the task states and allowed task transitions, including terminal `accepted` and `stopped`. |
| Authoritative input | `skills/task-orchestrator/docs/stage-3-tasks/stage-3-tasks-04-08-review.md#Pre-edit verdict` and `#Test-planning result` | Requires exhaustive state/selection evidence and a real two-process lock/stale-reconciliation boundary. |
| Confirmed fact | `S3-02` extracted state, selection, attempt, and ledger rules while keeping controller compatibility names and atomic persistence ownership. | `skills/task-orchestrator/docs/stage-3-tasks/S3-02-result.md` |
| Confirmed fact | Existing focused tests live in `tests/test_controller_state.py` and command-flow tests in `tests/test_controller.py`. | Limited read-only discovery of the two cited files; preflight must confirm current contents and helper interfaces. |
| Frozen decision | Allowed run transitions are `initialized -> {ready, stopped}`, `ready -> {running, stopped}`, `running -> {awaiting_inspection, resumable, stopped}`, `awaiting_inspection -> {resumable, finalizing, stopped}`, `resumable -> {running, stopped}`, `finalizing -> {ready, stopped}`, and none from `stopped`. | Entailed by the Stage 3 plan's lifecycle, inspection, resume, finalization, and terminal-completion contracts. |
| Frozen decision | A run in `finalizing` retains its selected task in `awaiting_inspection`; only the final ledger update moves that task to `accepted` and the run to `ready` or `stopped`. | `skills/task-orchestrator/docs/stage-3-plan.md#Settled decisions and constraints`; task index entries `S3-11` and `S3-12`. |
| Frozen decision | `completed_task_ids` remains the immutable manifest-supplied set; in-run completion is derived from task entries in `accepted`. | `skills/task-orchestrator/docs/stage-3-plan.md` task `S3-04` approved detail and task `S3-12` exit contract. |
| Frozen decision | The lock is local, non-blocking, per run, held by file descriptor for each mutation phase; distributed locking is out of scope. | `skills/task-orchestrator/docs/stage-3-plan.md#Architecture assessment after S3-01 through S3-03`. |
| Assumption | Candidate lock implementation is a run-contained lock file using the platform standard-library advisory exclusive/non-blocking file-lock facility (expected `fcntl.flock` with `LOCK_EX` plus `LOCK_NB` on the supported local platform). | Preflight must confirm availability, lock-file placement, release semantics, and that the test uses separate processes rather than same-process descriptors. |
| Assumption | Existing fake-worker/process helpers can be extended locally in `tests/test_controller.py`; no shared harness is needed. | Preflight must confirm the closest helper and that deterministic events or bounded polling can expose the waiting boundary. |
| Assumption | The two documented focused `unittest` commands and aggregate discovery command remain canonical. | Preflight must run/confirm exact syntax and baseline state; this brief does not claim they pass now. |
| Unresolved item | None. Current-path/helper/mechanism claims above are preflight questions, not missing product or architecture authority. | If any requires wider scope or a new shared facility, route back to `task-brief-designer`. |

## Scope and boundaries

| Item | Contract |
|---|---|
| Allowed paths | `skills/task-orchestrator/scripts/controller_state.py`; `skills/task-orchestrator/scripts/controller.py` only for initialization/readiness, repeated `run-next` compatibility, expected-revision persistence, and the per-run command-lock boundary; `skills/task-orchestrator/tests/test_controller_state.py`; `skills/task-orchestrator/tests/test_controller.py` only for the corresponding command-flow integrations; new `skills/task-orchestrator/docs/stage-3-tasks/S3-04-result.md` |
| Read-only context | Repository instructions supplied for this root; `skills/task-orchestrator/docs/controller-contract.md`; `skills/task-orchestrator/docs/stage-3-plan.md`; `skills/task-orchestrator/docs/stage-3-tasks/S3-02-result.md`; the four allowed existing source/test files |
| Prohibited work | New public CLI commands; retry/resume/recover/stop/inspect/accept implementations; policy or manifest version changes; verification/decision/operation record validators; Git-observation redesign; generalized storage/workflow/locking abstractions; unrelated cleanup or formatting |
| Mutation limits | Standard-library-only; no network, dependency install, live Codex/model call, destructive Git operation, commit, tracker mutation, installed/cached skill edit, or change to the master plan/task brief during implementation |
| Pre-existing user work | Preserve; ownership remains with the user. Known path from design-time status: untracked `.gitignore`. Preflight must refresh status and stop on overlap with any allowed path. |

The run-transition table frozen by authority is:

| From | Allowed next run states |
|---|---|
| `initialized` | `ready`, `stopped` |
| `ready` | `running`, `stopped` |
| `running` | `awaiting_inspection`, `resumable`, `stopped` |
| `awaiting_inspection` | `resumable`, `finalizing`, `stopped` |
| `resumable` | `running`, `stopped` |
| `finalizing` | `ready`, `stopped` |
| `stopped` | none |

The task-transition table remains:

| From | Allowed next task states |
|---|---|
| `initialized` | `ready`, `stopped` |
| `ready` | `running`, `stopped` |
| `running` | `awaiting_inspection`, `resumable`, `stopped` |
| `awaiting_inspection` | `accepted`, `resumable`, `stopped` |
| `resumable` | `running`, `stopped` |
| `accepted` | none |
| `stopped` | none |

State/reference coherence must implement these minimum invariants:

| Run state | Selection and task coherence | Attempt/process coherence | Minimum reference coherence |
|---|---|---|---|
| `initialized` | No selected task; authorized task identities/order remain fixed. | No active attempt. | All four Stage 3 ledger references are null. |
| `ready` | No selected task; at least one authorized unfinished task is `ready`; no task is implicitly selected. | No active attempt. | `active_operation_path` is null; historical `last_*` references may remain after a completed acceptance but must preserve their dependency order. |
| `running` | Exactly one selected task is `running`. | Exactly one active attempt, owned by and present in the selected task's append-only history; no other task owns it. | `active_operation_path` is null. Earlier-turn `last_*` references may remain during same-thread lifecycle extension. |
| `awaiting_inspection` | Exactly one selected task is `awaiting_inspection`. | The current attempt is the selected task's latest attempt; no active process/attempt. | `last_closure_path` is required. Verification and decision references are nullable during ordered publication, but decision implies verification and verification implies closure. No active operation. |
| `resumable` | Exactly one selected task is `resumable`. | Exactly one current attempt is retained in that task's history; no active process/attempt. | No active operation. Existing last-evidence references, if any, retain dependency order. |
| `finalizing` | Exactly one selected task remains `awaiting_inspection`, never `accepted`. | No active process/attempt. | Closure, verification, current decision, and prepared active operation references are all required in dependency order. |
| `stopped` | No selected task. Terminal task states and earlier audit evidence are preserved. | No active process/attempt. | No new evidence is inferred; retained references must preserve dependency order. |

## Entry criteria and dependencies

| Criterion | Required evidence | Current claim |
|---|---|---|
| S3-02 complete | `skills/task-orchestrator/docs/stage-3-tasks/S3-02-result.md` says complete; focused pure-state baseline command succeeds in fresh preflight. | preflight must confirm |
| Stage 2 fake flow remains intact | Existing `init` + fake `run-next` integration reaches `awaiting_inspection` before edits. | preflight must confirm |
| No later Stage 3 CLI is present ahead of its state contract | Parser/public-command inspection limited to `controller.py`. | preflight must confirm |
| Allowed files and local test helpers exist with no overlapping user edits | Fresh `git status --short`, path inspection, and helper/interface check. | preflight must confirm |
| Local standard-library non-blocking process lock is enforceable | Minimal read-only/platform capability confirmation; no new reusable harness. | preflight must confirm |

## Work and acceptance criteria

Required work:

1. Add explicit run-state constants/transition enforcement while retaining the
   approved task-transition contract; reject every unlisted transition.
2. Extend pure ledger validation to enforce the state, selection, task,
   attempt-ownership, reference-dependency, task-identity/order, immutable
   authority, append-only history, and monotonic revision invariants above.
3. Initialize new ledgers with all four nullable Stage 3 references and mark
   exactly dependency-ready authorized tasks plus the run `ready` without
   selecting or launching work.
4. Make selection choose only persisted `ready` tasks in policy order, using
   manifest `completed_task_ids` plus task entries in `accepted` for dependency
   satisfaction, without mutating the manifest-supplied completion list.
5. Require an expected ledger revision for each pure/persisted update; reject a
   stale revision before replacement and leave both caller input and persisted
   bytes unchanged.
6. Add one run-contained, non-blocking controller lock around mutation phases.
   `run-next` holds it through validation, attempt allocation/artifact writes,
   and the durable `running` transition; it may release only while waiting for
   the owned worker, then must reacquire, reread, and match the exact
   run/task/attempt/revision before terminal reconciliation.
7. Preserve controller compatibility names and the current functional module
   boundary; do not create a shared lock/storage framework for this one owner.
8. Create `S3-04-result.md` with transition/coherence tables, reference
   compatibility, lock ownership/lifetime, commands/results, and residual risk.

- **AC-01:** Table-driven tests cover every allowed run/task transition and
  reject every unlisted transition, including all transitions out of terminal
  task states and terminal run `stopped`.
- **AC-02:** `running` requires exactly one selected `running` task and one
  active attempt owned by and present in that task's append-only history.
- **AC-03:** `awaiting_inspection` requires exactly one selected task, no active
  process/attempt, and a closure reference; later references obey their
  dependency order.
- **AC-04:** `finalizing` requires the current closure, verification, decision,
  and prepared operation references while the selected task remains
  `awaiting_inspection`, not `accepted`.
- **AC-05:** `resumable` retains exactly one selected task/current attempt and
  no active process; `ready` and `stopped` retain neither selection nor active
  attempt.
- **AC-06:** Initial and post-acceptance selection choose the first persisted
  `ready` task in policy order, derive dependencies from immutable manifest
  completion plus accepted task entries, and never rewrite
  `completed_task_ids`.
- **AC-07:** Invalid, authority-changing, history-truncating, or stale-revision
  updates are rejected before persistence, leaving inputs and previous ledger
  bytes unchanged.
- **AC-08:** A second controller process cannot enter the same mutation phase,
  allocate another attempt, launch another fake worker, or let stale terminal
  reconciliation overwrite a competing state change.

## AC execution matrix

| AC | Production invariant | Positive evidence | Negative evidence | Real entry-point path | Repeated or recovery path | Real boundary crossed | Verification dependency |
|---|---|---|---|---|---|---|---|
| AC-01 | Only the two frozen transition tables are legal. | Iterate every listed run and task edge and assert the requested state. | Cartesian-product every unlisted edge; explicitly retry transitions from run `stopped` and task `accepted`/`stopped` and assert rejection. | Direct import of public state transition functions from `scripts/controller_state.py`; retained controller compatibility names are also sampled. | Execute one legal edge, then attempt the next illegal/terminal edge against its returned state. | Pure module boundary. | Task-local table data in `tests/test_controller_state.py`. |
| AC-02 | One selected running task exclusively owns the one active attempt. | A coherent running fixture with the attempt in the selected task history validates. | Missing/wrong selection, state mismatch, absent history membership, or the same attempt in another task is rejected without input mutation. | `validate_ledger` / pure update API in `controller_state.py`. | Append an attempt, enter `running`, then validate the persisted next occurrence; a second owner is rejected. | Pure state/ownership boundary. | Task-local coherent-ledger fixture. |
| AC-03 | Inspection has selection and closure evidence but no active process. | Coherent closure-only, closure+verification, and closure+verification+decision publication-prefix fixtures validate. | Missing closure, active attempt, wrong task state, verification without closure, decision without verification, or active operation is rejected. | State validator through `controller_state.py`; existing fake `run-next` flow through `controller.py` reaches the first prefix. | First worker occurrence publishes closure; the next validation accepts only ordered reference advancement. | Pure state plus real run-directory ledger/closure integration boundary. | Existing fake-worker flow believed present in `tests/test_controller.py`. |
| AC-04 | Finalization never implies task acceptance before the final ledger update. | A finalizing fixture with selected task `awaiting_inspection` and all four ordered references validates. | Missing, misordered, or state-incompatible decision/operation references, or an already-`accepted` selected task, are rejected unchanged. | `validate_ledger` and expected-revision update interface. | Apply the prepared-operation state once, then validate the next repeated read without changing task acceptance. | Pure state boundary; paths are structural references only in S3-04. | Task-local finalizing fixture; record-byte validation remains S3-05. |
| AC-05 | Resumable retains identity without liveness; ready/stopped clear active ownership. | Coherent `running -> resumable -> running` fixtures retain selected/latest attempt; coherent ready/stopped fixtures have no selection/active attempt. | Resumable with no selected/latest attempt or any live active attempt, and ready/stopped with selection/active attempt, are rejected. | Pure transitions/ledger validator; command-flow sample for ready `run-next`. | Execute first running occurrence, terminal resumable state, then the next running occurrence for the same selected attempt. | Pure lifecycle boundary plus fake local process entry point for ready launch. | Task-local fixtures and believed-existing fake adapter. |
| AC-06 | Dependency readiness and selection are deterministic without duplicating completion authority. | Initialize a multi-task graph; assert exact ready set and first policy-ordered choice, then legitimately mark one task accepted/recompute readiness and select the next ready task. | Ready run with no ready unfinished task, selection of initialized/accepted/stopped task, incomplete dependency, or attempted `completed_task_ids` rewrite is rejected. | Public `controller.py init`/`run-next` for initial workflow plus pure selection/update API for the simulated post-acceptance ledger. | First selection, legitimate accepted-state change, recomputation, then next selection; no automatic launch between occurrences. | Filesystem ledger plus fake local worker process for command-flow coverage. | Existing temp run/policy/manifest and fake-worker helpers; no shared harness. |
| AC-07 | Ledger authority is immutable, histories append, and revision comparison precedes replacement. | Valid update with exact expected revision increments revision once and preserves immutable fields/input object. | Reordered tasks, changed identity/dependencies/allowed paths/checks/completed IDs, truncated history, duplicate ownership, or stale revision leaves input and exact ledger bytes unchanged. | Pure `apply_ledger_update` and controller-owned persisted `update_ledger` path. | Apply revision N once, replay expected revision N against N+1, and assert rejection/no replacement. | Real run-directory filesystem and atomic replacement boundary. | Existing temporary-directory fixture; exact byte oracle kept in `tests/test_controller_state.py`/`test_controller.py`. |
| AC-08 | Only one controller owns a mutation phase and reconciliation is compare-before-write. | Process A acquires lock, creates one attempt, persists `running`, releases while its event-controlled fake worker waits, then reacquires and reconciles only the unchanged revision/state. | Process B loses lock during the held phase; after release its `run-next` sees `running` and cannot allocate/launch. A controlled lock-owning competing update while A waits causes A's stale reconciliation to stop without overwrite. | Real `controller.py run-next` subprocesses against one run directory. | First command reaches durable running/wait; second command and then stale first reconciliation exercise the next occurrences. | OS advisory file lock, process scheduling, local subprocess, run-directory filesystem. | Task-local event/bounded-polling fake worker and platform lock candidate; preflight confirms exact interface. |

## Legacy-assumption sweep

| Entry point or area | Search term / trace | Risk being tested | Required follow-through |
|---|---|---|---|
| `scripts/controller_state.py` transitions and validator | `ALLOWED_TASK_TRANSITIONS`, literal state sets, `selected_task_id`, `active_attempt_id`, `last_closure_path` | Stage 2 state literals omit run transitions, `accepted`, `resumable`, `finalizing`, and new references. | Preflight locates every literal/guard; implementation centralizes the frozen tables and tests every state rather than leaving divergent sets. |
| `scripts/controller_state.py::select_task` | `ledger["state"] != "initialized"`, dependency checks, `completed_task_ids` | First-selection-only logic can reject post-acceptance `ready` runs or select a non-`ready` task; mutable completion authority can diverge. | Trace selection from initial ready and post-acceptance ready; require persisted task state `ready` and derived accepted IDs without altering the manifest list. |
| `scripts/controller_state.py::apply_ledger_update` and `scripts/controller.py::update_ledger` | `revision`, unconditional read/update/replace, task key comparison | Monotonic increment without caller-supplied expected revision permits stale writes; task authority fields can change while IDs remain fixed. | Add exact expected-revision proof and compare every immutable task field/order plus append-only histories before persistence. |
| `scripts/controller.py::init_run` | `state: initialized`, task entries initialized, reference-field construction | New runs may expose no dependency-ready task and omit Stage 3 nullable fields. | Assert exact ready/initialized task partition and all four initialized references in persisted bytes/output. |
| `scripts/controller.py::_cli_run_next` | `attempt-001`, `task-001.json`, `Stage 2 permits exactly one immutable attempt`, original-run baseline comparison | Fixed identifiers and first/only-attempt assumptions can break a second selected task or duplicate ownership; an initial-baseline-only guard may be incompatible with legitimate later state. | Trace every fixed name/guard. Make only the minimum S3-04 compatibility change. If safe repeated selection requires new Git-evidence fields or authority beyond the allowed state/lock scope, stop and route back to brief design rather than weakening drift checks. |
| Every controller ledger/artifact mutation path in scope | `atomic_write_json`, `create_attempt`, closure write, ledger write | Atomic replacement/revision validation alone does not serialize processes, and locking only the final write leaves duplicate side effects. | Preflight enumerates the in-scope mutation sequence; implementation holds one run lock across validation through durable running and reacquires/revalidates before reconciliation. |
| Cleanup/compatibility behavior | controller compatibility aliases and exact persisted JSON fields | Moving/renaming public helpers or silently rewriting legacy artifacts can break Stage 2 callers. | Preserve compatibility names; add fields only to newly initialized ledgers; do not migrate or rewrite existing immutable artifacts in this task. |

## Risk-to-evidence map

| Risk | Impact / escalation trigger | Evidence level and boundary | Scenario and oracle | Residual gap |
|---|---|---|---|---|
| Two controller processes act on one revision | Duplicate worker/attempt or stale overwrite; stop if the local supported lock cannot enforce exclusion. | Integration/system at real OS-process, advisory-lock, subprocess, and filesystem boundaries. | Event-controlled process A and competing process B; assert one attempt/worker, exact bytes, and stale reconciliation refusal. | Local single-host lock only, explicitly accepted by the plan. |
| State/reference combinations authorize later commands incorrectly | Invalid inspection/finalization/resume path; escalate if later authority requires a combination absent from the frozen table. | Exhaustive unit/module state-transition and coherence tables. | One valid fixture per run state plus focused single-field corruptions; oracle is accept/reject and unchanged input. | Artifact containment/digest correctness is deliberately deferred to S3-05 and each writer. |
| Completion authority diverges | Wrong dependency release or task selection. | Unit graph/selection tests plus command-flow filesystem boundary. | Manifest-complete + ledger-accepted graph, initial and next choice, attempted list rewrite; oracle is exact ready set/order and immutable list. | Full acceptance release remains S3-12. |
| Stale update replaces newer ledger | Data loss or contradictory reconciliation. | Pure expected-revision test plus real persisted-byte integration test. | Apply N -> N+1, replay N, compare exact prior bytes and caller object. | Cross-host/distributed writers are out of scope. |
| Tests pass without proving contention timing | False concurrency confidence. | Deterministic two-process integration using events or bounded polling, no sleeps. | Observe durable `running`/lock ownership before competitor action; retain diagnostics on deadline. | Platform-specific lock availability must be confirmed by preflight. |
| Repeated selection weakens original Git drift protection | Unobserved external change could launch work. Stop if satisfying repeat selection requires bypassing checks or adding an uncited evidence model. | Legacy trace plus narrow fake-flow integration; no pure-function-only claim. | Stable legitimate first occurrence, accepted-state update, and next `run-next`; assert existing safety gates are not silently removed. | Dirty accepted-work integration is owned by later inspection/finalization tasks unless existing authority supports it within this slice. |

## Verification-capability inventory

| Needed capability | Disposition | Owner / path | Preflight confirmation |
|---|---|---|---|
| Exhaustive transition and coherent-ledger fixtures | task-local fixture | `skills/task-orchestrator/tests/test_controller_state.py` | Confirm existing fixture shape can be extended without a shared builder and every AC state has a row. |
| Exact persisted-byte and stale-revision oracle | believed existing | `skills/task-orchestrator/tests/test_controller_state.py` and `skills/task-orchestrator/tests/test_controller.py` | Confirm current byte-preservation test and update interfaces; identify the fail-first stale/coherence case. |
| Fake `run-next` worker with controllable wait/release | believed existing, extended task-locally | `skills/task-orchestrator/tests/test_controller.py` | Confirm closest fake-worker helper and add only one-use event/bounded-polling controls inside this file. |
| Real two-process lock contention | task-local fixture | `skills/task-orchestrator/tests/test_controller.py` | Confirm separate subprocess invocation, observable lock/running boundary, bounded deadline, and cleanup. |
| Canonical test runner/shared helper | believed existing | Standard-library `unittest` commands in the Stage 3 plan | Confirm exact commands collect the intended classes; no new runner or CI wiring. |

No prerequisite implementation or evaluation brief is justified: all evidence
is one-task use inside existing owning test files, and the plan already
authorizes the local standard-library lock boundary. A failed platform/helper
assumption routes to preflight rather than authorizing new infrastructure.

## Verification command candidates

| Class | Candidate command | Working directory | Evidence | Preflight must resolve |
|---|---|---|---|---|
| Fail-first | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py` with the newly added coherent `resumable` or stale-revision case selected first | Repository root | Demonstrates the new test rejects pre-change behavior or a controlled fault for the intended assertion. | Exact test selector/name after test design; ensure failure is assertion-specific and no temporary mutation remains. |
| Targeted | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py` | Repository root | AC-01 through AC-07 pure/state evidence. | Current baseline and exact collection. |
| Targeted | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py` | Repository root | AC-03, AC-05 through AC-08 command/filesystem/process evidence and Stage 2 compatibility. | Current baseline, platform permissions, and bounded concurrency helper. |
| Broader | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'` | Repository root | Task-orchestrator transitive regression coverage. | Whether local sandbox/loopback permission is needed; request approval instead of silently retrying if the sandbox blocks an established capability. |
| Hygiene | `git diff --check` | Repository root | Whitespace integrity for task-scoped changes. | None beyond inspecting both tracked and permitted new result file. |

These are design candidates, not claims that a command exists or passes.

## Effort, budget, and escalation

| Item | Proposal |
|---|---|
| Implementation | `strong` agent; `high` reasoning — exhaustive lifecycle coherence plus deterministic process locking/stale-reconciliation evidence has a narrow but concurrency-sensitive blast radius. |
| Review | `immediate` — independently inspect the transition/reference tables, lock lifetime, two-process oracle, immutable authority, and exact diff before dependent tasks proceed. |
| Budget checkpoint | At 24 tool calls, 70 minutes, or 80k current-context input, whichever comes first, assess remaining ACs and prepare a structured handoff if completion will cross the repository soft stop; do not exceed the approved `30 tool calls / 90 minutes / 100k context` without user direction. |
| Two-strike rule | After two materially different fixes leave the same targeted behavior failing, stop and report evidence, discarded hypotheses, owning contract, and next route. |
| Escalation triggers | Lock unavailable/unenforceable on the supported local platform; contention test cannot deterministically observe ownership; repeated selection requires weakening Git drift checks or new evidence fields; a later lifecycle needs an unlisted transition/reference combination; migration of existing ledgers is required; shared infrastructure, wider paths, new dependency, network, permission, destructive, commit, tracker, or compatibility authority is needed; user edits overlap allowed paths. |

## Stop conditions and routing

- Stop before edits when S3-02/baseline tests, the Stage 2 fake flow, supported
  local lock capability, allowed-path cleanliness, or required local helpers
  cannot be confirmed.
- Stop during implementation if exact run/task/reference coherence cannot be
  expressed without contradicting the controller contract or later Stage 3
  finalization/resume contracts.
- Stop rather than bypass the initial-baseline/Git drift guard if repeated
  `run-next` compatibility needs authority or fields outside this state/lock
  slice.
- Route missing/ambiguous authority to the user/Stage 3 plan owner and keep
  status `blocked_design` in a repaired brief.
- Route stale state, missing believed-existing helpers, invalid commands, or
  dirty overlap to `task-preflight`.
- Route wider paths or shared infrastructure back to `task-brief-designer`,
  followed by a fresh preflight.
- Stop at the S3-04 boundary before verification, decision, or operation record
  validation (S3-05), recovery/stop commands (S3-09), or any later command.

## Implementation handoff requirements

The implementer must receive a fresh `ready` preflight packet derived from this
exact brief. It may change only confirmed allowed paths, must preserve the
frozen transition/reference tables and compatibility names, establish the
named fail-first coherence/revision evidence, and run commands one at a time
from focused state tests through command/process integration and then the
justified aggregate gate. It must use deterministic process events or bounded
polling, preserve user work, stop under the stated rules, create
`S3-04-result.md`, and return the schema-required structured worker result. It
does not approve its own work and must not edit this brief or the master plan.

## Review handoff requirements

Independent review must receive this brief, its exact fresh preflight packet,
the structured worker result, `S3-04-result.md`, and the scoped
baseline-to-current diff. It must corroborate all eight ACs, enumerate both
transition tables, validate every state/reference fixture, repeat initial and
post-acceptance selection, rerun stale-revision byte preservation, and observe
real two-process contention and stale reconciliation at the run-directory
boundary. It must revisit every named legacy assumption, verify no public CLI,
policy/manifest, Git-evidence, shared-infrastructure, or unrelated change
escaped scope, and return the staged acceptance verdict without editing the
reviewed files.

## Handoff summary

Run `task-preflight` on
`skills/task-orchestrator/docs/stage-3-tasks/S3-04-stage-3-state-model.md` and
produce a fresh execution packet; `ready_for_preflight` is a design-complete
contract, not a claim that the current repository is executable.
