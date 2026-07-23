# S3-08: Implement Inspection and Closure Decisions

Status: ready after S3-03 and S3-07
Depends on: S3-03 including S3-03A/S3-03B corrections, S3-07
Blocks: S3-11

```yaml
agent_tier: strong
reasoning: high
review: immediate
budget: 30 tool calls / 90 minutes / 100k context
```

## Outcome

Add `controller.py inspect` for a run in `awaiting_inspection`. It revalidates
the Stage 2 closure, runs independent verification, detects verification-created
repository drift, and idempotently publishes an immutable final verification
record, decision, and ledger references. These are ordered exclusive writes,
not a falsely atomic multi-file transaction. It performs no acceptance side
effect.

## Required context

Read:

- `docs/stage-3-plan.md` — records, authority, stop conditions
- `docs/controller-contract.md` — closure gate
- `docs/stage-3-tasks/S3-03B-result.md` — corrected observational Git boundary
- `docs/stage-3-tasks/S3-04-result.md` — state and command-lock contract
- `docs/stage-3-tasks/S3-05-result.md` — record/identity chain
- `docs/stage-3-tasks/S3-07-result.md` — production executor record
- `scripts/controller.py`, `controller_state.py`, `controller_git.py`, and
  `verification_runner.py`
- focused tests for those modules

## Entry criteria

- S3-03 and S3-07 suites pass.
- A Stage 2 fake run can reach `awaiting_inspection` with immutable closure
  evidence.
- No live/ambiguous worker is recorded.
- The implementer accepts that existing closure files lacking an exact
  canonical status-map digest cannot be upgraded in place; they fail closed and
  a new fake run is required.

## Allowed changes

- `scripts/controller.py`
- `scripts/controller_state.py` only for task-local decision wiring defects
- `scripts/controller_git.py` only for task-local observation support
- `tests/test_controller.py`
- owning focused tests only when their boundary contract changes
- new `docs/stage-3-tasks/S3-08-result.md`

Do not add acceptance, resume, tracker, commit, or next-task behavior.

## Work

1. Add one read-only `controller_git.py` workspace-identity operation returning
   exact HEAD OID, index tree, and SHA-256 of the canonical status mapping. It
   writes no closure artifact and interprets no policy.
2. Extend newly produced Stage 2 closure evidence to bind that exact
   post-worker workspace identity. Include it in the closure evidence digest
   and add focused compatibility tests. Never rewrite or infer the missing
   fingerprint for an existing closure; reject it before verification.
3. Add `inspect --run-dir ... --timeout-seconds <positive>` valid only from
   `awaiting_inspection`. Hold the S3-04 per-run lock for the full operation and
   reject contention before command execution or mutation.
4. Validate the ledger; persisted policy/manifest/baseline; selected task;
   attempt/turn record, prompt, adapter state, and structured result; closure
   JSON and every referenced artifact/digest; and the complete S3-05 identity
   chain. Treat worker result/checks as claims, never controller evidence.
5. Capture the pre-verification workspace identity and require an exact match
   with the closure. A same-path, same-size content change must be detected by
   the canonical status digest, not only by name/status or diff statistics.
6. Derive the S3-06 plan and invoke S3-07 only when no valid turn-qualified
   command-execution record already exists. If one exists, validate its exact
   closure identity and bytes and reuse it without rerunning any command;
   mismatch stops.
7. Capture post-verification workspace identity and exclusively publish the
   final turn-qualified verification record referencing the immutable execution
   record. Any HEAD, index, tracked content, untracked content/path, modified or
   disappeared pre-existing dirty path, or other status-map drift is a closure
   violation. If a final record already exists, validate and reuse it or stop;
   never overwrite it.
8. Compute and exclusively publish the turn-qualified decision bound to the
   final verification digest. `accept` is offered only when the worker result is
   complete/matching, every targeted role passed, the repository gate passed or
   has its exact non-targeted gap, closure scope/integrity is clean, and no
   blocking question or unresolved risk remains. `resume` is offered only when
   acceptance failed, a durable thread ID exists, the process is recorded
   absent, and persisted stop policy permits escalation; `stop` remains valid.
   Record `semantic_review: not_collected` and never imply semantic approval.
9. If the decision already exists, require exact bytes/identity and reuse it.
   Finally update the verification/decision ledger references in one locked
   ledger write while leaving run/task `awaiting_inspection`. A crash after any
   earlier publication is recovered by validation/reuse on the next `inspect`.

Use this denial-to-action mapping. Integrity/tamper failures are always
stop-only. For multiple ordinary findings, `resume` is offered only when every
applicable policy entry is `escalate` and the thread/process prerequisites also
hold.

| Finding | Policy entry governing resume eligibility |
|---|---|
| `needs_input` or blocking question | `stop_policy.on_needs_input` |
| `blocked` or unresolved worker risk | `stop_policy.on_blocked` |
| failed/timed-out targeted verification | `stop_policy.on_failed` |
| unexpected, pre-existing-dirty, or verifier-created Git drift | `stop_policy.on_unexpected_changes` |
| identity, digest, artifact, adapter, HEAD, or index tampering/ambiguity | never resumable; `stop` only |

## Required test evidence

Positive cases:

- A full fake Stage 2 run produces a closure with exact post-worker HEAD, index,
  and canonical status digest. Clean `inspect` executes real local harmless
  commands through S3-07, publishes execution/verification/decision records in
  order, sets ledger references, offers `accept`, and leaves the task
  `awaiting_inspection`.
- A repository-gate-only failure with the exact authorized gap is retained as a
  gap and may still offer `accept`; the same command carrying a targeted role
  may not.
- Crash/replay fixtures cover: execution exists without final verification,
  final verification exists without decision, and both records exist without
  ledger references. Re-running validates/reuses bytes, runs no command twice,
  and completes only the missing publication/reference step.
- Non-accepting decisions exercise the exact resume/stop matrix for thread and
  stop-policy combinations.

Negative cases:

- Every run state other than `awaiting_inspection`, run-lock contention, and an
  invalid timeout reject without command execution, record creation, or ledger
  mutation.
- Tampering each persisted policy, manifest, baseline, prompt, attempt/turn,
  adapter state, worker result, closure field, closure artifact, or digest stops
  before command execution and leaves bytes unchanged.
- Worker-claimed passing verification with missing/failed controller execution
  cannot offer `accept`.
- Failed/timeout targeted checks, unexpected paths, modified/disappeared
  pre-existing dirty paths, worker HEAD/index drift, blocking questions, and
  non-empty unresolved risks each deny `accept` with a specific reason.
- Before-verification drift covers HEAD, index, tracked content, untracked
  content, and a same-path/same-size content substitution. None runs a command.
- A verifier-created tracked file, untracked file, content change, deletion,
  staging/index change, or commit/HEAD change appears in post identity and
  prevents `accept`.
- Existing execution/verification/decision bytes with any mismatch cannot be
  overwritten, supplemented with a contradictory record, or referenced by the
  ledger.

## Acceptance criteria

- **AC-01:** `inspect` rejects every state except `awaiting_inspection` without
  mutation.
- **AC-02:** Stale or tampered Stage 2 evidence prevents command execution and
  record publication.
- **AC-03:** Worker-claimed passing checks cannot substitute for controller
  verification.
- **AC-04:** Failed/timeout checks, unexpected paths, pre-existing dirty-path
  changes, HEAD/index drift, questions, or unresolved risks prevent `accept`.
- **AC-05:** Exact pre-verification HEAD/index/status identity must match the
  closure; a verification-created tracked, untracked, index, or HEAD change is
  recorded and prevents `accept`.
- **AC-06:** An exact authorized repository-gate gap is recorded but never
  converts a failed targeted check.
- **AC-07:** Decision identity includes the verification digest and matches the
  current closure identity.
- **AC-08:** Re-running after each publication boundary reuses exact immutable
  evidence, performs no command twice, and cannot overwrite or create a
  contradictory record.
- **AC-09:** Execution, final verification, decision, and ledger-reference
  publication order is crash-recoverable without claiming cross-file
  atomicity.
- **AC-10:** No ledger task state becomes `accepted` in this task.

## Verification

Run the same-path/same-size pre-verification drift denial first and show it
fails for the intended assertion. Then run the focused Git identity test,
inspect integration tests, and owning state/runner modules one command at a
time. Finish with the aggregate suite and `git diff --check`. No live model or
external network check is authorized.

## Exit and handoff

Create `S3-08-result.md` and report the closure compatibility change, identity
and publication sequence, each denial reason tested, action matrix,
commands/results, and residual risks. Stop before implementing any action
returned by the decision.
