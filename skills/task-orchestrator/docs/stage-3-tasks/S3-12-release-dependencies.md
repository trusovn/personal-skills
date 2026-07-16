# S3-12: Finalize Acceptance and Release Dependencies

Status: ready after S3-11
Depends on: S3-11
Blocks: S3-16

## Outcome

Complete an effects-complete prepared operation with one atomic ledger write:
mark exactly the selected task accepted, recompute task readiness from immutable
manifest dependencies, and return the run to `ready` or terminal `stopped`
without selecting or launching another task.

## Required context

Read:

- `docs/stage-3-plan.md` — settled no-auto-launch decision
- `assets/task-manifest.schema.json`
- `scripts/controller_state.py`
- acceptance and task-selection tests

## Entry criteria

- S3-11 acceptance tests pass.
- The run is `finalizing`, the selected task remains `awaiting_inspection`, and
  the prepared operation proves all authorized side effects complete.

## Allowed changes

- `scripts/controller_state.py`
- `scripts/controller.py` only to call the pure readiness result
- `tests/test_controller_state.py`
- `tests/test_controller.py`

Do not call the transport, allocate an attempt, choose a task, or change the
manifest.

## Work

1. Revalidate the effects-complete operation and atomically move exactly its
   selected task to `accepted` in the same ledger update as readiness changes.
2. Derive completion from manifest `completed_task_ids` plus ledger task states
   equal to `accepted` after that transition.
3. In persisted policy order, move only `initialized` tasks whose dependencies
   are complete to `ready`.
4. Preserve other accepted, stopped, running, inspection, and unrelated task
   entries.
5. Set run `ready` when at least one authorized unfinished task is ready.
6. Set run `stopped` with terminal reason `complete` when no authorized
   unfinished task remains.
7. After the atomic ledger write, advance the operation from `effects_complete`
   to `complete`. A crash between those writes is an explicit recoverable state
   for S3-15, not a reason to repeat acceptance.
8. Leave selection and launch to a later explicit `run-next` invocation.

## Acceptance criteria

- **AC-01:** A task cannot become accepted unless its current effects-complete
  operation identity matches exactly.
- **AC-02:** Table-driven graphs cover linear, fan-out, fan-in,
  already-complete, unauthorized, stopped, and no-ready cases.
- **AC-03:** A task becomes ready only when every dependency is complete.
- **AC-04:** Policy order is preserved and no task is selected.
- **AC-05:** No attempt directory, prompt, worker process, closure, or decision
  is created.
- **AC-06:** Terminal completion is explicit and deterministic.
- **AC-07:** Replaying finalization, including accepted-ledger plus
  effects-complete-operation state, is idempotent and cannot accept a second
  task.

## Verification

Run one fan-in state test first, then the state module and one command-flow test
proving no fake transport invocation. Finish with the aggregate suite and
`git diff --check`.

## Exit and handoff

Report readiness cases and the no-launch oracle. Stop before changing
`run-next`; integration with its existing selection behavior belongs only to
compatibility fixes required by these state results.
