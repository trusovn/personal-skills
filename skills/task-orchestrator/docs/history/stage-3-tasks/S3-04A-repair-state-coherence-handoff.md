# S3-04A Handoff: Repair State Coherence And Stale-Revision Evidence

This file is a durable companion to the copy/paste handoff. It defines one
bounded corrective task for the two findings from the S3-04 review.

Status: ready
Date: 2026-07-16
Workspace: `/Users/mtrusov/work/skill-sources/personal-skills`
Branch baseline at handoff creation: `main` at `30fa947`

## Resume Prompt

```text
You are implementing the S3-04A correction in
/Users/mtrusov/work/skill-sources/personal-skills.

Repair the Stage 3 ledger-coherence contract so only the selected task may be
in an ownership-bearing state (`running`, `awaiting_inspection`, or
`resumable`). Add the missing controller-level evidence that a stale revision
leaves persisted ledger bytes unchanged. Start by adding and running the exact
fail-first multi-active-task regression described in this handoff. Make the
smallest correction in controller_state.py; do not redesign the state model or
implement S3-05/S3-09 behavior.

Read repository AGENTS.md and every required-context file below before editing.
Inspect Git status and preserve unrelated user files. Do not edit existing
plans, task briefs, handoffs, or result documents. Publish completion evidence
in a new S3-04A-result.md.
```

## Primary Goal

Close the two review findings that prevent S3-04 from being a complete,
executable foundation for S3-05 and S3-09:

1. reject ledgers and ledger updates containing a second non-selected task in
   `running`, `awaiting_inspection`, or `resumable`; and
2. prove at the controller/filesystem boundary that a stale expected revision
   cannot change persisted ledger bytes.

This correction is intentionally small enough for one agent session. It should
change one production validator, two existing test modules, and create one
result document. Do not split it unless an entry criterion fails or the repair
requires a contract decision outside the boundaries below.

## Current State

- S3-04 is implemented in commit `30fa947` and its existing 18 state tests, 42
  controller tests, and 93 aggregate task-orchestrator tests pass.
- The transition tables, nullable ledger references, initial and repeated
  selection, immutable completion authority, expected revisions, run lock, and
  stale terminal-reconciliation checks are present.
- S3-04 is not yet complete because the ledger validator accepts multiple
  ownership-bearing task states and one required stale-persistence test is
  absent.
- No source or test repair has been made by the review/handoff agent.
- No background server or process is associated with this handoff.

## Required Context

Read completely before editing:

- repository `AGENTS.md`;
- `docs/controller-contract.md`, especially the task lifecycle and ownership
  boundaries;
- `docs/stage-3-plan.md`, especially the settled single-worktree ownership and
  locking rules;
- `docs/stage-3-tasks/S3-04-stage-3-state-model.md`;
- `docs/stage-3-tasks/S3-04-result.md`;
- this handoff;
- `scripts/controller_state.py`, especially `validate_ledger()` and
  `apply_ledger_update()`;
- `scripts/controller.py`, only to understand `update_ledger()` and the lock
  boundary;
- `tests/test_controller_state.py`; and
- `tests/test_controller.py`.

Do not treat the existing passing suites as proof that the reviewed defect is
absent. The decisive case is not represented in those suites.

## Entry Criteria

Before editing:

1. Run `git status --short --branch` and confirm that no user change overlaps
   `controller_state.py`, `test_controller_state.py`, or `test_controller.py`.
2. Preserve the pre-existing untracked repository `AGENTS.md` and
   `skills/task-orchestrator/agent-output.analysis.md`.
3. Confirm `main` still contains commit `30fa947`, or record the newer baseline
   and inspect intervening changes before proceeding.
4. Run the existing state suite as the behavioral baseline:

   ```text
   PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py
   ```

5. Confirm no later task has already changed the relevant state contract. If
   S3-05 or S3-09 edits overlap these files or depend on the defective behavior,
   stop and ask for scope/order guidance rather than silently adapting them.

If any overlapping user edit exists, stop without modifying it. Do not try to
discover or infer the user's intended merge.

## Confirmed Defect

`validate_ledger()` currently validates the selected task for `running`,
`awaiting_inspection`, `resumable`, and `finalizing`, but it does not reject a
second non-selected task in one of the ownership-bearing states.

The following state was accepted during review:

```text
run: running
selected_task_id: T1
active_attempt_id: attempt-001
tasks:
  T1: running, attempts=[attempt-001]
  T2: running, attempts=[attempt-002]
```

Both `validate_ledger()` and `apply_ledger_update()` accepted this state. The
update used a valid task transition for T2 (`ready -> running`), so transition
table enforcement does not repair the ledger-level ownership violation.

Consequences:

- the ledger can claim two logical attempts are running in a sequential
  single-worktree controller;
- later commands can receive contradictory ownership state even though the
  selected task and active attempt look locally valid; and
- S3-04 AC-02 and AC-07, plus the required negative mismatched-state evidence,
  are not fully satisfied.

## Contract Decision

Use this minimal invariant:

- ownership-bearing task states are `running`, `awaiting_inspection`, and
  `resumable`;
- if a task is in one of those states, it must be the task named by
  `selected_task_id`;
- therefore a run with no selected task has no ownership-bearing task, and a
  run with a selected task has at most one;
- existing run-specific checks continue to decide which ownership-bearing
  state the selected task must have and whether an active/current attempt or
  closure/finalization reference is required.

Do not replace the existing run-specific checks with a generalized state
machine. A small additional validation condition after task discovery is the
expected implementation shape.

Preserve these legitimate states:

- other dependency-ready tasks may remain `ready` while one selected task is
  `running`, `awaiting_inspection`, `resumable`, or `finalizing`;
- previously accepted tasks remain `accepted`;
- a stopped run may retain unrelated `ready`, `initialized`, `accepted`, or
  `stopped` tasks as currently permitted; and
- `finalizing` continues to keep only the selected task in
  `awaiting_inspection`; the task does not become `accepted` until the final
  ledger update.

Do not add validation of record contents, digests, process liveness, retry
authority, or same-thread resume mechanics. S3-05 and S3-09 own those contracts.

## Allowed Changes

- `scripts/controller_state.py` for the minimal non-selected ownership-state
  rejection;
- `tests/test_controller_state.py` for fail-first pure validation/update
  coverage and positive non-regression coverage;
- `tests/test_controller.py` for the stale expected-revision persisted-byte
  check; and
- new `docs/stage-3-tasks/S3-04A-result.md` for completion evidence.

Do not modify:

- `scripts/controller.py` unless the new stale-revision test exposes a real
  implementation defect; if it does, stop and report the evidence before
  expanding scope;
- any existing plan, task brief, review, handoff, or result document;
- transition tables or version-1 policy/manifest semantics;
- CLI commands, worker transport, Git evidence, verification/decision/operation
  records, recovery, resume, acceptance, or commit behavior;
- repository architecture or top-level structure; or
- Git history, staging, and unrelated working-tree files.

## Test-First Work

### 1. Add the decisive fail-first state regression

In `test_controller_state.py`, start from a valid two-task ledger:

- the run is `running`;
- T1 is selected and `running` with `attempt-001`;
- T2 is non-selected and `ready` with no attempt;
- T1 and T2 have distinct identities and valid authority fields.

Create an update that moves T2 to `running` and appends `attempt-002`, while
leaving T1 selected and the run active on `attempt-001`.

Assert that `apply_ledger_update()` raises `ValueError` and that the original
ledger object remains byte-for-byte/equality unchanged. Run this exact test
before changing production code and record its failure. The expected pre-fix
failure is that no exception is raised.

The test should exercise observable state validity; do not assert source shape
or copy the production algorithm into the test.

### 2. Cover direct ledger validation without overfitting

Add a compact table of invalid ledgers proving that a non-selected task cannot
be any of:

- `running`;
- `awaiting_inspection`; or
- `resumable`.

Exercise representative selected-run states, including `running` and
`finalizing`, and at least one no-selection state such as `initialized`.
Attempt IDs must be unique so the cases fail for ownership-state coherence,
not duplicate-attempt validation.

Avoid a Cartesian test matrix if a smaller table proves the same invariant.
Use a stable error category or short substring rather than coupling every test
to full prose.

### 3. Preserve legitimate non-selected tasks

Add or extend a positive case proving validation still permits:

- T1 selected and `running` with its current attempt; and
- independent T2 remaining `ready`.

If the finalizing fixture is naturally extended to include another `ready`
task, confirm that remains valid too. Do not force every task to `initialized`
or `stopped` merely because another task is selected.

### 4. Add the missing stale-persistence evidence

In `test_controller.py`, add a controller/filesystem test that:

1. writes a coherent ledger to a temporary run directory;
2. captures the exact `ledger.json` bytes and an unchanged updater/input value;
3. calls `controller.update_ledger(..., expected_revision=<stale>)`;
4. asserts `ValueError` identifies a stale ledger revision;
5. asserts the updater/input is unchanged;
6. asserts `ledger.json` bytes are exactly unchanged; and
7. asserts no attempt or closure artifact was created.

The controller lock file may be created by lock acquisition; do not incorrectly
require the whole run directory to remain byte-identical. The required oracle
is unchanged input, unchanged authoritative ledger bytes, and no command
artifacts.

This test is expected to pass on the current implementation. Its purpose is to
close explicitly required integration evidence, not justify extra production
changes.

### 5. Implement the smallest validator correction

Change only `validate_ledger()` unless the fail-first test demonstrates a
different root cause. Reuse the selected task discovered during the existing
task loop. Reject any ownership-bearing task that is not the selected task,
then retain the existing state-specific checks.

Do not add a class, dependency injection, new module, schema framework, or
public API. Do not change allowed transition tables.

## Risk-To-Evidence Map

| Risk or contract | Lowest decisive evidence | Required oracle |
|---|---|---|
| A second logical task becomes running | Pure update regression | Update raises and source ledger is unchanged |
| A forged ledger contains a non-selected ownership state | Pure validator table | Every representative ledger is rejected for ownership coherence |
| The fix rejects valid parallel readiness | Pure positive validation | Selected active T1 plus ready T2 validates |
| Stale controller revision writes bytes | Temporary-filesystem controller test | Exact ledger bytes and input unchanged; no attempt/closure artifact |
| Lock/reconciliation behavior regresses | Existing controller suite | All process/lock tests continue to pass |
| Transitive controller behavior regresses | Aggregate suite | All task-orchestrator tests pass |

No network, live model, dependency installation, performance test, or new
test framework is needed.

## Verification Order

Run one gate at a time. Do not run broader suites until the new fail-first test
has failed for the expected reason and then passed after the correction.

1. Existing baseline before edits:

   ```text
   PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py
   ```

2. Exact new multi-active-task test before production editing. Record the
   expected failure (`ValueError` not raised):

   ```text
   PYTHONDONTWRITEBYTECODE=1 python3 -m unittest <exact-multi-active-test-id>
   ```

3. After the validator correction, run the exact new tests individually:

   ```text
   PYTHONDONTWRITEBYTECODE=1 python3 -m unittest <exact-multi-active-test-id>
   PYTHONDONTWRITEBYTECODE=1 python3 -m unittest <exact-direct-coherence-table-test-id>
   PYTHONDONTWRITEBYTECODE=1 python3 -m unittest <exact-stale-persisted-bytes-test-id>
   ```

4. Run the owning modules:

   ```text
   PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py
   PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py
   ```

5. Run the aggregate regression suite:

   ```text
   PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'
   ```

6. Run static and scope checks:

   ```text
   git diff --check
   git status --short
   git diff -- skills/task-orchestrator/scripts/controller_state.py skills/task-orchestrator/tests/test_controller_state.py skills/task-orchestrator/tests/test_controller.py skills/task-orchestrator/docs/stage-3-tasks/S3-04A-result.md
   ```

Inspect the final diff manually. Every changed line must trace to one of the two
findings. If a test creates `__pycache__`, remove only that generated artifact
before final status; do not delete user files.

## Acceptance Criteria

- **AC-A01:** A ledger with no selected task rejects any task in `running`,
  `awaiting_inspection`, or `resumable`.
- **AC-A02:** A ledger with a selected task rejects every non-selected task in
  `running`, `awaiting_inspection`, or `resumable`.
- **AC-A03:** A valid selected task retains all existing state-specific current
  attempt, closure, decision, and operation requirements.
- **AC-A04:** Non-selected `ready`, `initialized`, `accepted`, and `stopped`
  tasks remain permitted wherever the existing S3-04 contract permits them;
  independent ready work is not collapsed merely because one task is selected.
- **AC-A05:** The valid `ready -> running` transition for a non-selected task
  cannot be applied while another task owns the run; the rejected update leaves
  the source ledger unchanged.
- **AC-A06:** A stale controller update leaves the updater/input and exact
  persisted ledger bytes unchanged and creates no attempt or closure artifact.
- **AC-A07:** Existing transition, selection, run-lock, second-`run-next`, and
  stale terminal-reconciliation tests remain green.
- **AC-A08:** The state, controller, and aggregate suites pass; `git diff
  --check` passes; only allowed files changed.

## Stop Conditions

Stop and ask the user instead of expanding the task if:

- the minimal invariant conflicts with a later approved task or persisted
  compatibility contract;
- fixing the state defect requires changing a transition table, policy,
  manifest, CLI, or record schema;
- the stale persisted-byte test fails for a reason requiring changes outside
  `controller_state.py` and the allowed tests;
- an overlapping user change exists in an allowed file;
- verification needs network access, a dependency install, live Codex, or a
  destructive Git operation; or
- the aggregate suite exposes an unrelated pre-existing failure.

Do not reinterpret an unrelated failure as authority to repair it. Record it
as a blocker or residual risk.

## Completion Result

Create `docs/stage-3-tasks/S3-04A-result.md`. Do not edit this handoff,
`S3-04-result.md`, the S3-04 task brief, or the master plan.

The result must include:

- status: `complete` or `blocked`;
- exact baseline commit and workspace status;
- concise root cause and the invariant implemented;
- every changed file and why it changed;
- the exact fail-first test ID and expected pre-fix failure;
- acceptance criteria AC-A01 through AC-A08 evaluated individually;
- exact commands and observed test counts/results, including `git diff
  --check`;
- confirmation that no existing plan/result/handoff was edited;
- preserved user files and any generated artifacts removed;
- residual risks; and
- one exit verdict: `S3-04 corrected; ready for dependent tasks` or `blocked`.

Do not copy historical test counts into the result. Report the counts produced
after the correction.

## Current Verification Evidence

The read-only review and handoff preparation observed:

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py`
  — 18 tests passed;
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py`
  — 42 tests passed;
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'`
  — 93 tests passed;
- `git diff 30fa947^ 30fa947 --check` and current `git diff --check` passed; and
- the controlled multi-active-task probe was accepted, confirming the defect.

Treat these as starting evidence only. Rerun the prescribed gates after
editing.

## Preserved Workspace State

At handoff creation, `main` matched `origin/main` at `30fa947`. Preserve these
pre-existing untracked files:

- repository `AGENTS.md`; and
- `skills/task-orchestrator/agent-output.analysis.md`.

The handoff creator added only this new handoff document. No source, test,
existing plan, existing result, or existing handoff file was modified.
