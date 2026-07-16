# S3-15: Reconcile Interrupted Finalization

Status: ready after S3-14
Depends on: S3-14
Blocks: S3-16

## Outcome

Extend `recover` for a run in `finalizing`. Reconcile a prepared acceptance
operation against actual Git and ledger state, continue an authorized missing
step idempotently, finalize a proven completed operation, or stop without
mutation when external state is ambiguous.

## Required context

Read:

- `docs/stage-3-plan.md` — finalization recovery rules
- `scripts/controller.py`, `controller_state.py`, `controller_git.py`
- S3-11/S3-14 acceptance and commit tests

## Entry criteria

- S3-14 commit finalization tests pass.
- A valid prepared operation is required by every `finalizing` ledger state.
- Human tracker mode remains off for the core path.

## Allowed changes

- `scripts/controller.py`
- `scripts/controller_state.py`
- `scripts/controller_git.py` only for read-only reconciliation evidence
- `tests/test_controller.py`
- focused owning tests only for contract changes

Do not add tracker recovery or infer acceptance from a worker result, commit
message alone, or task title.

## Work

1. On every command, route `finalizing` through operation reconciliation before
   allowing other work.
2. If no optional side effect is intended, finish the exact prepared operation
   and ledger transition idempotently.
3. If no commit side effect is present and current HEAD/index still equal the
   prepared preconditions, continue the authorized commit step.
4. If the exact intended deterministic commit is already at HEAD, verify its
   OID, parent, tree, diff paths, message, authoring inputs, real index, and
   unrelated worktree state before recording it.
5. If actual state differs from both pre-effect and exact post-effect intent,
   persist/report a stopped reconciliation mismatch without further mutation.
6. If all effects are recorded but ledger is stale, complete the acceptance
   transition once.

## Acceptance criteria

- **AC-01:** Fault injection after every S3-11/S3-14 durable boundary either
  completes exactly once or stops without an additional side effect.
- **AC-02:** The same recovery command is idempotent after completion.
- **AC-03:** An exact commit at HEAD can be recognized from prepared evidence;
  a lookalike message or partial match cannot.
- **AC-04:** External HEAD/index/worktree mutation prevents continuation and
  leaves user state untouched.
- **AC-05:** Acceptance is never inferred from worker output or an unbound
  artifact.
- **AC-06:** Recovery never launches a worker or auto-selects a task.

## Verification

Run one post-HEAD/pre-operation-record crash case first, then the finalization
fault matrix. Finish with controller/Git modules, the aggregate suite, and
`git diff --check`.

## Exit and handoff

Report each crash point and recovery oracle. Name tracker recovery as explicitly
unimplemented unless S3-T1/S3-T2 were separately authorized and completed.
