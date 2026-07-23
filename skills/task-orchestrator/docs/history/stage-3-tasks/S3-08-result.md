# S3-08 Result: Inspection and Closure Decisions

Status: complete; fresh guided acceptance review passed
Date: 2026-07-21

The first guided acceptance pass found and corrected one AC-01 issue: a fresh
`ready` run could create `controller.lock` before wrong-state rejection. A
later adversarial review found two further defects: a coherently changed worker
result with a mismatching `task_id` reached verification, and replay after
verification-created drift applied the original pre-verification identity gate
before consulting the final records. Both are corrected and covered by
regressions. A subsequent review found that a coherent non-`task_id` result and
closure rewrite could still reach verification because neither file's exact
bytes had an independent anchor. The ledger now anchors the closure digest, and
the anchored closure binds the exact worker-result digest. The final deferred
issue is now corrected: newly produced closure evidence also binds the exact
attempt-record bytes, and inspection validates the fixed transport/model
contract before verification. A fresh guided acceptance review passed the
focused and aggregate behavioral gates with no findings.

## Outcome

Implemented `controller.py inspect --run-dir ... --timeout-seconds ...` for a
run in `awaiting_inspection`. The command holds the per-run controller lock for
the complete operation, validates the persisted authority and immutable Stage
2 evidence, requires an exact pre-verification workspace identity, executes or
reuses S3-07 verification, records post-verification drift, exclusively
publishes the final verification and decision, and finally updates only the
ledger references. It does not execute any returned `accept`, `resume`, or
`stop` action and never changes the run or task from `awaiting_inspection`.

## Closure compatibility and identity

New Stage 2 closures now bind `post_worker_status_sha256`, the SHA-256 of the
canonical content-hashed status mapping, into the existing Git evidence digest.
Together with `head_after` and `index_tree`, this supplies the S3-05 closure
identity fields:

- `post_worker_head_oid`
- `post_worker_index_tree_oid`
- `post_worker_status_sha256`

Historical closures without the canonical status digest are rejected before
verification and are not rewritten or migrated. The focused real-Git oracle
proves that a same-path, same-size content substitution changes only the status
digest and is denied without command execution or run-file mutation.

## Validation and publication sequence

`inspect` validates, in order, the ledger and state; policy and manifest bytes
and digests; repository and selected-task authority; selected-task baseline;
the exact attempt-record bytes anchored by the closure, its fixed
`codex-cli`/null-model contract, and both prompt copies; adapter and terminal state; exact
structured-worker-result bytes including its selected-task identity; the exact
closure bytes anchored by the ledger; closure identity and worker claims; every
closure artifact and digest; the Stage 2 evidence digest; and the complete
S3-05 closure identity.

Without a final verification record, inspection first requires the exact Stage
2 pre-verification identity, then publication is:

1. reuse a validated canonical command-execution record, or invoke S3-07 once;
2. capture post-verification HEAD, index, and canonical status identities;
3. exclusively publish or exactly reuse the turn-qualified verification;
4. exclusively publish or exactly reuse the digest-bound decision; and
5. atomically set the verification and decision ledger references.

An injected crash after step 1 left only the execution family. The retry
validated and reused those exact bytes, did not call the executor, completed
steps 2–5, and a subsequent full replay left every run-file byte unchanged.
When the final verification already exists, replay instead validates the
execution and final records and requires the live workspace to match the
recorded post-verification identity before validating or reusing the decision.
This permits recorded verifier-created drift to replay without rerunning a
command while still rejecting later workspace changes.

## Decision behavior and denial evidence

- Clean controller verification offers `accept` and `stop`.
- A repository-gate-only failure carrying the exact persisted authorized gap
  remains accepting and retains the gap in the decision.
- The same failing command with a task or policy targeted role is not excused
  and cannot offer `accept`.
- Failed targeted verification offers `resume` only with a durable thread,
  absent worker process, and `stop_policy.on_failed: escalate`; otherwise it is
  stop-only.
- Worker or verifier HEAD, index, tracked/untracked content, or path drift
  prevents `accept`; focused evidence exercises verifier-created content drift.
- Historical closure identity gaps, authority/digest mismatches, wrong run
  state, invalid timeout, and lock contention stop before execution and retain
  existing run bytes.
- A worker result whose `task_id` does not match the selected task stops before
  execution or publication, even when the closure claim is changed coherently.
- Worker verification entries remain claims. Only the S3-07 execution record
  contributes controller verification evidence.
- Every decision records `semantic_review: not_collected`.

## Changed files

- `scripts/controller.py`
- `scripts/controller_state.py`
- `scripts/controller_git.py`
- `tests/test_controller.py`
- `tests/test_controller_state.py`
- `tests/test_controller_git.py`
- `docs/stage-3-tasks/S3-08-result.md`

The pre-existing untracked `.gitignore` was not read, edited, removed, or added.

## Acceptance correction

The deferred AC-02 issue is resolved. Newly produced Stage 2 closures contain
`attempt_record_sha256`, computed from the exact immutable record bytes and
covered by the ledger-anchored closure digest. Inspection requires that digest
to match before verification, so any coherent or isolated attempt-record byte
change fails closed. It also rejects a non-`codex-cli` transport or non-null
model at the state-contract boundary. The regression changes `model` to
`tampered-model` and proves zero executor calls, no execution record, and
byte-identical run evidence after rejection. Historical closures without the
new binding fail closed rather than being upgraded.

A fresh guided acceptance review on 2026-07-21 returned `ACCEPT` with no
findings.

## Test-first and verification evidence

The required fail-first command reached the intended drift assertion after a
valid fake-worker closure was created. It failed because `inspect` was not yet a
CLI command; the marker executable remained absent and the recursive run-byte
snapshot was valid. After implementation the same command passed and proved
zero verification execution plus unchanged run bytes.

- Same-path/same-size decisive oracle: passed, 1 test.
- Focused clean crash/replay inspection: passed, 1 test using a real harmless
  local command through `/usr/bin/sandbox-exec`.
- Focused compatibility, gap, targeted-failure, verifier-drift, resume-policy,
  timeout, lock, wrong-state, coherent worker-result tamper, and drift-replay
  cases: passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_git.py`
  — passed, 13 tests.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py`
  — passed, 60 tests in the fresh acceptance review.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py`
  — passed, 37 tests.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_verification_runner.py`
  — passed, 34 tests.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'`
  — passed, 159 tests in the fresh acceptance review.
- `git diff --check` — passed after the result update.

## Acceptance criteria

- **AC-01:** satisfied by state, timeout, and lock rejection with zero executor
  calls and byte preservation.
- **AC-02:** satisfied. The ledger-anchored closure binds the exact attempt
  record and worker result bytes; state validation rejects the known immutable
  transport/model tamper; historical unanchored closures and all identity
  mismatches fail before verification.
- **AC-03:** satisfied because decisions consume only the controller execution
  record, never worker-reported checks.
- **AC-04:** satisfied by targeted failure, closure observation, question/risk,
  and verifier-drift denial logic.
- **AC-05:** satisfied by exact pre/post HEAD, index, and content-hashed status
  identities, including same-size substitution and verifier-created drift.
- **AC-06:** satisfied by both repository-only gap acceptance and targeted-role
  non-excusability integration tests.
- **AC-07:** satisfied by S3-05 validation of the closure identity and exact
  verification digest in every decision.
- **AC-08:** satisfied by exclusive publication, canonical byte validation,
  crash recovery, executor non-reentry, byte-identical full replay, and replay
  against the recorded post-verification identity after verifier-created drift.
- **AC-09:** satisfied by execution, verification, decision, then ledger
  publication with recovery from the execution and completed-record boundaries.
- **AC-10:** satisfied; all inspection outcomes retain run and task state
  `awaiting_inspection`.

## Residual risks and handoff

The S3-07 pathname-scoped Seatbelt limitations remain unchanged. Inspection is
single-host and depends on the existing advisory run lock. Verification can
legitimately leave repository drift on failure; the immutable verification and
decision record that drift and deny acceptance but do not roll it back.

No lifecycle action returned by a decision was performed. The fresh acceptance
review found no remaining S3-08 blocker; this task did not start S3-11.
