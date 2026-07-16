# S3-04: Extend the Stage 3 State Model

Status: ready after S3-02
Depends on: S3-02
Blocks: S3-05, S3-09

```yaml
agent_tier: strong
reasoning: high
review: immediate
budget: 30 tool calls / 90 minutes / 100k context
```

## Outcome

Make Stage 3 run/task transitions and ledger state coherence executable before
any new CLI command uses them. Also serialize ledger/artifact mutation phases
with one per-run command lock; pure validation alone cannot prevent two
processes from acting on the same ledger revision.

## Required context

Read:

- `docs/controller-contract.md` — approved task lifecycle
- `docs/stage-3-plan.md` — settled decisions and durable records
- `docs/stage-3-tasks/S3-02-result.md` — extracted state boundary
- `scripts/controller.py` — run initialization, `run-next`, and ledger writes
- `scripts/controller_state.py`
- `tests/test_controller.py`
- `tests/test_controller_state.py`

## Entry criteria

- S3-02 is complete and pure state tests pass.
- No Stage 3 CLI command has been added ahead of its state contract.
- The current Stage 2 fake-flow integration test passes before state changes.

## Allowed changes

- `scripts/controller_state.py`
- `scripts/controller.py` only for initial readiness, repeated `run-next`
  compatibility, and the per-run command-lock boundary
- `tests/test_controller_state.py`
- `tests/test_controller.py` only for those command-flow integrations
- new `docs/stage-3-tasks/S3-04-result.md`

Do not add a new public CLI command or change policy/manifest version 1.

## Work

1. Define allowed run states: `initialized`, `ready`, `running`,
   `awaiting_inspection`, `resumable`, `finalizing`, and `stopped`, with an
   explicit run-transition table. `resumable` is not an alias for `ready`:
   it retains one selected task/attempt for same-thread resume.
2. Define allowed task states: `initialized`, `ready`, `running`,
   `awaiting_inspection`, `resumable`, `accepted`, and `stopped`.
3. Encode every allowed run and task transition and reject every unlisted
   transition. Keep the accepted task in `awaiting_inspection` while the run is
   `finalizing`; only the final ledger write moves that task to `accepted`.
4. Define the minimal nullable ledger references used later:
   `last_closure_path`, `last_verification_path`, `last_decision_path`, and
   `active_operation_path`. Initialize them for newly created runs and require
   the appropriate selected task, active attempt, and references in each state.
5. Make new runs expose dependency-ready tasks as `ready`, and make pure
   selection work both for the first task and after an accepted task returns
   the run to `ready`. Select only a task whose persisted state is `ready`, in
   policy order.
6. Preserve `completed_task_ids` as the immutable manifest-supplied completion
   set. Derive in-run accepted IDs only from task entries whose state is
   `accepted`; never append them to a second mutable completion list.
7. Preserve append-only attempt histories, fixed task identity/order, immutable
   dependency/allowed-path/check fields, and monotonic ledger revisions.
8. Add one non-blocking per-run controller lock using the supported local
   standard-library mechanism and pair updates with an expected ledger
   revision. `run-next` holds it through validation, attempt allocation, and the
   durable `running` transition; it may release while waiting for the owned
   worker, then must reacquire and revalidate the exact run/task/attempt and
   revision before reconciliation. This permits the later `stop` command while
   preventing a second launch or stale terminal overwrite.

## Required test evidence

Positive cases:

- A table covers every allowed run transition and every allowed task
  transition.
- One coherent ledger fixture validates for each run state. The `resumable`
  fixture retains exactly one selected task and no active process; the
  `finalizing` fixture retains an unaccepted selected task plus decision and
  operation references.
- Initialization marks exactly the dependency-ready authorized tasks `ready`.
  Selection chooses the first ready task in policy order both before the first
  attempt and after a prior task is accepted.
- Manifest-supplied completed IDs plus accepted task states satisfy dependency
  calculations without mutating the manifest-supplied list.
- A controller process holding the run lock excludes a second mutation phase;
  after a durable `running` transition, a second `run-next` is still rejected
  even while the first waits without the lock.

Negative cases:

- Exhaustive table tests reject every run/task state pair not present in the
  allowed transition tables, including all transitions out of `accepted` and
  `stopped`.
- Missing/wrong selected task, mismatched task/run state, an active attempt not
  in the selected task history, duplicate attempt ownership, or decision/
  operation references in an incompatible state are rejected.
- A `ready` run with no ready unfinished task, a `resumable` run with no
  selected attempt, and a `finalizing` run whose task is already accepted are
  rejected.
- Reordering tasks, changing immutable task authority, changing
  `completed_task_ids`, truncating attempt history, or applying a stale
  revision leaves the input and persisted ledger bytes unchanged.
- Lock contention cannot create an attempt, run a second fake worker, or change
  ledger bytes. If a controlled competing update wins while the first command
  waits, the first command's terminal reconciliation detects the changed
  revision/state and cannot overwrite it. Use process events or bounded
  polling, not sleeps.

## Acceptance criteria

- **AC-01:** Table-driven tests cover every allowed run/task transition and
  every unlisted transition.
- **AC-02:** `running` requires one selected task and one active attempt owned by
  that task.
- **AC-03:** `awaiting_inspection` requires one selected task, no active process,
  and a closure reference.
- **AC-04:** `finalizing` requires a current decision and prepared operation and
  does not mark the task accepted.
- **AC-05:** `resumable` retains exactly one selected task/current attempt and no
  active process; `ready` and terminal `stopped` retain neither selection nor
  active attempt.
- **AC-06:** Selection works for initial and post-acceptance ready tasks without
  rewriting manifest-supplied completion authority.
- **AC-07:** Invalid or stale updates are rejected before persistence, leaving
  input objects and prior bytes unchanged.
- **AC-08:** A second controller process cannot enter the same mutation phase,
  launch another worker, or let a stale terminal reconciliation overwrite a
  competing state change.

## Verification

Run one currently invalid coherence case first and show it fails for the
intended assertion. Then run:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py
```

Then run the aggregate task-orchestrator suite and `git diff --check`.

## Exit and handoff

Create `S3-04-result.md` and report the transition/coherence tables, ledger
field compatibility, lock ownership/lifetime, commands/results, and residual
risks. Stop before adding verification, decision, or operation record
validators; S3-05 owns them.
