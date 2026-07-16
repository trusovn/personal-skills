# S3-04: Extend the Stage 3 State Model

Status: ready after S3-02
Depends on: S3-02
Blocks: S3-05, S3-09

## Outcome

Make Stage 3 run/task transitions and ledger state coherence executable, pure
contracts before any new CLI command uses them.

## Required context

Read:

- `docs/controller-contract.md` — approved task lifecycle
- `docs/stage-3-plan.md` — settled decisions and durable records
- `scripts/controller_state.py`
- `tests/test_controller_state.py`

## Entry criteria

- S3-02 is complete and pure state tests pass.
- No Stage 3 CLI command has been added ahead of its state contract.

## Allowed changes

- `scripts/controller_state.py`
- `tests/test_controller_state.py`

Do not wire CLI commands or change policy/manifest version 1.

## Work

1. Define allowed run states: `initialized`, `ready`, `running`,
   `awaiting_inspection`, `finalizing`, and `stopped`.
2. Define allowed task states: `initialized`, `ready`, `running`,
   `awaiting_inspection`, `resumable`, `accepted`, and `stopped`.
3. Encode every allowed transition and reject every unlisted transition.
4. Validate selected task, active attempt, closure, decision, and prepared
   operation fields required or forbidden in each run state.
5. Derive accepted task IDs from task states; reject a second mutable accepted
   list as authority.
6. Preserve append-only attempt histories and policy-order task identity.

## Acceptance criteria

- **AC-01:** Table-driven tests cover every allowed transition and a sample of
  invalid cross-state transitions.
- **AC-02:** `running` requires one selected task and one active attempt owned by
  that task.
- **AC-03:** `awaiting_inspection` requires one selected task, no active process,
  and a closure reference.
- **AC-04:** `finalizing` requires a current decision and prepared operation and
  does not mark the task accepted.
- **AC-05:** `ready` and terminal `stopped` cannot retain an active attempt.
- **AC-06:** Invalid coherence is rejected before ledger persistence, leaving
  prior bytes unchanged.

## Verification

Run the new state-transition test first, then:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py
```

## Exit and handoff

Report the state/coherence table implemented. Stop before adding verification,
decision, or operation record validators; S3-05 owns them.
