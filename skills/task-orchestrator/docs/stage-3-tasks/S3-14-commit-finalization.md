# S3-14: Integrate Controller-Owned Commit Finalization

Status: ready after S3-12 and S3-13B
Depends on: S3-12, S3-13B
Blocks: S3-15

## Outcome

Extend prepared acceptance for policy mode `controller_exact_paths`. Persist
deterministic commit intent before invoking the S3-13 primitive, record verified
commit evidence, and mark the task accepted only after the commit side effect is
proven complete.

## Required context

Read:

- `docs/stage-3-plan.md` — acceptance/commit authority
- `assets/run-policy.schema.json` — commit modes
- `scripts/controller.py`, `controller_state.py`, `controller_git.py`
- S3-12 acceptance finalizer and S3-13A/S3-13B temporary-Git tests

## Entry criteria

- S3-12 mode-off acceptance finalizer and S3-13B publication primitive pass.
- Current immutable decision offers `accept` and policy mode is
  `controller_exact_paths`.
- Exact accepted changed paths and expected HEAD/index identities are known.

## Allowed changes

- `scripts/controller.py`
- `scripts/controller_state.py`
- `scripts/controller_git.py` only for an integration defect in its public
  primitive
- `tests/test_controller.py`
- focused owning tests only when their contract changes

Do not implement recovery yet or add tracker behavior.

## Work

1. Put exact paths, expected identities, commit parent/tree/message, and fixed
   author/committer policy/timestamps in the prepared operation before mutation.
2. Enter `finalizing`, build the exact S3-13A candidate, and publish it only
   through S3-13B.
3. Independently verify returned commit OID/evidence against prepared intent.
4. Atomically record the commit side effect in the operation.
5. Only then mark the operation effects complete and call the exact S3-12
   acceptance/readiness finalizer.
6. On a pre-HEAD failure, keep the task unaccepted and operation recoverable.
   On an exception after possible HEAD mutation, leave `finalizing` for S3-15;
   do not guess or roll back.

## Acceptance criteria

- **AC-01:** Commit mode off still invokes no commit code.
- **AC-02:** Exact-path mode cannot accept before prepared intent exists.
- **AC-03:** Commit evidence matches operation identity, accepted paths, parent,
  tree, message, and authoring policy.
- **AC-04:** A primitive denial/failure never marks the task accepted.
- **AC-05:** A simulated crash at each boundary leaves either no side effect or
  a durable `finalizing` state that S3-15 can distinguish.
- **AC-06:** No broad staging, shell command, tracker mutation, or destructive
  cleanup is introduced.

## Verification

Run one primitive-failure/no-accept test first, then controller commit
integration tests and the temporary-Git module. Finish with the aggregate suite
and `git diff --check`.

## Exit and handoff

Report the prepared intent fields, ledger/operation write order, and injected
crash points. Do not implement their reconciliation in this task.
