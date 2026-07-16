# S3-07: Implement the Sandboxed Verification Executor

Status: ready after S3-01, S3-05, and S3-06
Depends on: S3-01, S3-05, S3-06
Blocks: S3-08

## Outcome

Implement a small runner that executes an already-authorized argv plan
sequentially inside the S3-01 permission boundary and returns immutable,
identity-bound command evidence. It does not decide task acceptance.

## Required context

Read:

- `docs/verification-sandbox-decision.md`
- `docs/stage-3-plan.md` — durable verification records and constraints
- the command-plan and record validators from S3-05/S3-06
- `scripts/codex_worker.py` process cleanup only as a lifecycle precedent
- `tests/test_verification_runner.py`

## Entry criteria

- S3-01 is complete, not blocked.
- S3-05 and S3-06 focused suites pass.
- The chosen sandbox mechanism needs no unapproved dependency or network.

## Allowed changes

- new `scripts/verification_runner.py`
- `tests/test_verification_runner.py`
- `scripts/controller_state.py` only for a proven record-validator correction

Do not add `inspect`, mutate the ledger, make a closure decision, or run real
repository checks during development.

## Work

1. Accept only a validated argv plan, repository cwd, persisted permission
   envelope, positive per-command timeout, artifact directory, and identity.
2. Preflight all commands and the sandbox before running the first command.
3. Execute sequentially with `shell=False` and a new process group.
4. On timeout/interruption, terminate and reap the group with bounded polling.
5. Exclusively write stdout/stderr logs and one command outcome containing exact
   argv, cwd, envelope, timestamps, exit code, and terminal reason.
6. Stop after the first failed/timeout command unless the persisted plan
   explicitly marks the repository gate as an authorized gap.
7. Return evidence to the caller without choosing `accept`, `resume`, or `stop`.

## Acceptance criteria

- **AC-01:** The allowed-command, denied-write, and denied-network proofs from
  S3-01 pass through production code.
- **AC-02:** Preflight failure creates no command logs or partial record.
- **AC-03:** Timeout and interruption leave no live child and record one
  terminal outcome using events/bounded polling rather than sleeps.
- **AC-04:** Commands run in deterministic order and later commands do not run
  after a non-gap failure.
- **AC-05:** Existing artifact paths cannot be overwritten.
- **AC-06:** The effective envelope and exact argv appear in each outcome.
- **AC-07:** The runner has no Git, ledger, worker, tracker, commit, or acceptance
  responsibility.

## Verification

Run one production-boundary sandbox test, then:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_verification_runner.py
```

Then run the aggregate task-orchestrator suite and `git diff --check`.

## Exit and handoff

Report the supported envelope, process cleanup evidence, and record paths. Stop
before wiring the runner to controller inspection.
