# S3-04 Result: Stage 3 State Model

Status: complete
Date: 2026-07-16

## Outcome

Extended the pure controller state model with executable Stage 3 run/task
transitions, per-state ledger coherence, dependency-ready task release, and
optimistic revision checks. Added one non-blocking `fcntl.flock` lock per run
and split `run-next` around the worker wait so only the owning command can
publish terminal reconciliation.

New runs now publish `ready` rather than `initialized`. Exactly the authorized
tasks whose dependencies are satisfied by the immutable manifest-supplied
completion set are marked `ready`; selection uses persisted ready state in
policy order. Later readiness calculations also count task entries in
`accepted` without modifying `completed_task_ids`.

## Transition and coherence contracts

Allowed run transitions:

- `initialized` -> `ready`, `stopped`
- `ready` -> `running`, `stopped`
- `running` -> `awaiting_inspection`, `resumable`, `stopped`
- `awaiting_inspection` -> `resumable`, `finalizing`, `stopped`
- `resumable` -> `running`, `stopped`
- `finalizing` -> `ready`, `stopped`
- `stopped` -> none

The approved task transition table remains unchanged and now includes all
Stage 3 task states, including terminal `accepted` and `stopped` states.
Exhaustive table tests exercise every listed and unlisted run/task pair.

Ledger validation now enforces:

- one selected task and its latest active attempt while `running`;
- one selected task/current attempt but no active process while
  `awaiting_inspection`, `resumable`, or `finalizing`;
- a closure reference for terminal worker states;
- a closure -> verification -> decision -> active-operation reference chain
  while `finalizing`, with the selected task still `awaiting_inspection`;
- no selection or active attempt for `initialized`, `ready`, or `stopped`;
- at least one dependency-valid persisted ready task in a `ready` run;
- unique task IDs and globally unique attempt ownership;
- immutable task identity, order, title, brief, dependencies, allowed paths,
  required checks, and manifest-supplied completion IDs;
- append-only attempt histories and monotonically incremented revisions; and
- stale expected revisions rejected before persistence.

The nullable Stage 3 ledger references initialized for every new run are
`last_closure_path`, `last_verification_path`, `last_decision_path`, and
`active_operation_path`.

## Lock ownership and lifetime

Each existing run uses `<run-dir>/.controller.lock` with a non-blocking local
exclusive `flock`. `run-next` holds it through validation, selection, baseline
and attempt allocation, and the revision-checked durable `running` update. It
then releases the lock while waiting for the owned worker. Before any terminal
evidence or ledger update, it reacquires the lock and revalidates the exact
ledger revision, run state, selected task, active attempt, task state, and
latest attempt identity.

The integration race proves that lock contention leaves ledger/baseline bytes
and attempt allocation unchanged, a second `run-next` launches no worker after
the first has durably entered `running`, and a competing revision cannot be
overwritten by the first command's stale terminal reconciliation.

## Verification

- Entry baseline state suite: 12 tests passed.
- Entry Stage 2 fake-flow integration: 1 test passed.
- Test-first demonstration: the new incoherent-ledger test failed in eight
  intended subcases before implementation.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py`
  — 17 tests passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py`
  — 40 tests passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'`
  — 90 tests passed.
- Parsed all 4 task-orchestrator JSON files and the 4 changed Python files with
  the standard library without generating bytecode.
- `git diff --check` passed.

## Residual risk

The command lock is intentionally a single-host filesystem lock; distributed
controller ownership remains out of scope. Verification, decision, and
operation record schemas and identity binding remain deferred to S3-05.
