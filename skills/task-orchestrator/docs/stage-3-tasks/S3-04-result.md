# S3-04 Result: Stage 3 State Model

Status: complete
Date: 2026-07-16

## Outcome

Implemented the Stage 3 run/task transition and ledger-coherence contracts,
dependency-aware repeated selection, expected-revision updates, and one
non-blocking local command lock per run.

## Transition contracts

Run transitions:

- `initialized` -> `ready`, `stopped`
- `ready` -> `running`, `stopped`
- `running` -> `awaiting_inspection`, `resumable`, `stopped`
- `awaiting_inspection` -> `resumable`, `finalizing`, `stopped`
- `resumable` -> `running`, `stopped`
- `finalizing` -> `ready`, `stopped`
- `stopped` -> none

Task transitions retain the approved controller contract, including terminal
`accepted` and `stopped` states. Exhaustive table tests accept every listed
transition and reject every unlisted state pair.

## Ledger compatibility and coherence

New ledgers initialize these nullable references:

- `last_closure_path`
- `last_verification_path`
- `last_decision_path`
- `active_operation_path`

Initialization publishes the run as `ready` and marks exactly the authorized
tasks whose dependencies are already satisfied as `ready`. Selection considers
the immutable manifest-supplied `completed_task_ids` plus task entries already
in `accepted`, without changing the manifest-supplied list.

Validation now binds selected task state, current attempt ownership, closure
and finalization references, dependency readiness, unique attempt ownership,
and terminal-state cleanup. Updates require the expected ledger revision and
preserve task identity/order/authority, append-only attempt histories, and the
manifest-supplied completion set.

## Command ownership

Each mutation phase uses a non-blocking `fcntl.flock` on
`.controller.lock`. `run-next` holds the lock through validation, attempt
allocation, and the durable `running` update; releases it while the worker is
active; then reacquires it and verifies the exact revision, run state, selected
task, and attempt before publishing terminal evidence or changing the ledger.

Process-level tests prove that lock contention changes no ledger bytes or
attempt artifacts, a second `run-next` cannot launch while the first worker is
waiting, and a competing terminal update cannot be overwritten by stale
reconciliation.

## Verification

- Fail-first coherence case: rejected the pre-change implementation because
  `resumable` and `finalizing` were unknown and `ready` did not require a ready
  task.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py`
  - 18 tests passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py`
  - 42 tests passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'`
  - 93 tests passed.

## Residual boundary

S3-04 does not validate verification, decision, or operation record contents or
their digests. S3-05 owns those immutable record and identity contracts.
