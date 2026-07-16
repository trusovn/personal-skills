# S3-04A Result: Repair State Coherence And Stale-Revision Evidence

Status: complete
Date: 2026-07-16
Baseline: `main` at `30fa947`

## Outcome

Repaired the Stage 3 ledger-coherence contract. A task in `running`,
`awaiting_inspection`, or `resumable` must now be the task named by
`selected_task_id`. Existing run-specific checks continue to enforce the
selected task's exact state, attempt ownership, and required references.

The root cause was that `validate_ledger()` checked only the selected task's
coherence. It did not inspect other tasks for ownership-bearing states, so a
valid task transition could create a second logical owner.

## Changed Files

- `scripts/controller_state.py` rejects any non-selected task in an
  ownership-bearing state.
- `tests/test_controller_state.py` adds the fail-first update regression, a
  compact direct-validation table, and positive coverage for independent ready
  work.
- `tests/test_controller.py` proves a stale expected revision preserves the
  updater and exact persisted ledger bytes and creates no command artifacts.
- `docs/stage-3-tasks/S3-04A-result.md` records this completion evidence.

No existing plan, task brief, handoff, review, or result document was edited.

## Fail-First Evidence

Exact test ID:

`skills.task-orchestrator.tests.test_controller_state.ControllerStateContractTest.test_non_selected_task_cannot_transition_to_running_while_run_is_owned`

Before the production correction, the isolated test ran one test and failed
with `AssertionError: ValueError not raised`. This was the expected failure:
the update moved non-selected T2 from `ready` to `running`, appended its unique
`attempt-002`, and was incorrectly accepted while selected T1 retained
`attempt-001`.

## Acceptance Criteria

- **AC-A01: satisfied.** The direct table rejects `running` with no selected
  task in an `initialized` run.
- **AC-A02: satisfied.** The direct table rejects non-selected `running`,
  `awaiting_inspection`, and `resumable` tasks across representative run
  states.
- **AC-A03: satisfied.** The correction is additive; existing selected-task
  state, attempt, closure, decision, and operation checks remain in place and
  their suites pass.
- **AC-A04: satisfied.** Positive cases permit an independent `ready` task
  while the selected task is running and while the run is finalizing. Existing
  initialized, accepted, and stopped cases remain green.
- **AC-A05: satisfied.** The fail-first regression now rejects a non-selected
  `ready -> running` update and proves the source ledger remains unchanged.
- **AC-A06: satisfied.** The controller/filesystem test proves a stale
  revision leaves the updater and exact `ledger.json` bytes unchanged and
  creates neither attempt nor closure artifacts.
- **AC-A07: satisfied.** Existing transition, selection, run-lock, repeated
  `run-next`, and stale terminal-reconciliation coverage remains green.
- **AC-A08: satisfied.** The state, controller, and aggregate suites pass;
  `git diff --check` passes; only allowed files changed.

## Verification

- Baseline:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py`
  — 18 tests passed.
- Fail-first isolated regression, before production editing:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills.task-orchestrator.tests.test_controller_state.ControllerStateContractTest.test_non_selected_task_cannot_transition_to_running_while_run_is_owned`
  — 1 test ran and failed as expected because `ValueError` was not raised.
- Corrected isolated update regression, same command — 1 test passed.
- Direct coherence table:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills.task-orchestrator.tests.test_controller_state.ControllerStateContractTest.test_non_selected_task_rejects_every_ownership_bearing_state`
  — 1 test passed with three subcases.
- Stale persisted-byte evidence:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills.task-orchestrator.tests.test_controller.ControllerContractTest.test_stale_revision_leaves_persisted_ledger_bytes_unchanged`
  — 1 test passed.
- State module:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py`
  — 21 tests passed.
- Controller module:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py`
  — 43 tests passed.
- Aggregate suite:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'`
  — 97 tests passed.
- `git diff --check` — passed.

## Workspace And Residual Risk

The pre-existing staged
`docs/stage-3-tasks/S3-04A-repair-state-coherence-handoff.md` and untracked
`AGENTS.md` and `skills/task-orchestrator/agent-output.analysis.md` were
preserved unchanged. `PYTHONDONTWRITEBYTECODE=1` prevented generated Python
artifacts; none required removal.

No known residual risk remains within S3-04A. Record validation, process
liveness, recovery, and resume behavior remain intentionally outside this
correction under S3-05 and S3-09.

Exit verdict: **S3-04 corrected; ready for dependent tasks**.
