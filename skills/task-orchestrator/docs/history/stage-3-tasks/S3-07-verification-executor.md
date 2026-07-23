# S3-07: Implement the Sandboxed Verification Executor

Status: ready after S3-01, S3-05, and S3-06
Depends on: S3-01, S3-05, S3-06
Blocks: S3-08

```yaml
agent_tier: strong
reasoning: high
review: immediate
budget: 30 tool calls / 90 minutes / 100k context
```

## Outcome

Complete `verification_runner.py` so it executes an already-authorized argv
plan sequentially inside the S3-01 permission boundary and publishes one
immutable, identity-bound command-execution record plus exact command logs. It
does not inspect Git, publish the final verification record, or decide task
acceptance.

## Required context

Read:

- `docs/verification-sandbox-decision.md`
- `docs/stage-3-plan.md` — durable verification records and constraints
- `docs/stage-3-tasks/S3-01-result.md`
- `docs/stage-3-tasks/S3-05-result.md`
- `docs/stage-3-tasks/S3-06-result.md`
- the command-plan and record validators produced by S3-05/S3-06
- `scripts/codex_worker.py` process cleanup only as a lifecycle precedent
- `tests/test_verification_runner.py`

## Entry criteria

- S3-01 is complete, not blocked.
- S3-05 and S3-06 focused suites pass.
- The chosen sandbox mechanism needs no unapproved dependency or network.

## Allowed changes

- `scripts/verification_runner.py`
- `tests/test_verification_runner.py`
- `scripts/controller_state.py` only for a proven record-validator correction
- new `docs/stage-3-tasks/S3-07-result.md`

Do not add `inspect`, mutate the ledger, make a closure decision, or run real
repository checks during development.

## Work

1. Accept only an S3-06-validated plan, canonical repository cwd, complete
   persisted permission envelope, positive per-command timeout, run-contained
   turn-qualified artifact paths, and S3-05 closure identity.
2. Move the exact S3-01 sandbox invocation/profile construction into production
   code and make the existing capability tests call it. Keep the accepted
   pathname-scoped/hard-link limitation unchanged.
3. Before creating any log or starting the first command, validate the complete
   plan and identity, canonicalize cwd/writable roots, resolve every executable
   to the exact executable that will be invoked, prove the sandbox mechanism is
   available, and construct every effective sandbox argv. Reject any mismatch
   or collision for any command up front.
4. Execute sequentially with `shell=False`, the canonical repository cwd, and a
   new process group. Stream stdout/stderr as bytes to exclusive files so output
   size is not accumulated in controller memory and byte digests remain exact.
5. On timeout, interruption, or write/collection failure, terminate and reap
   the owned process group with events/bounded polling. Record exactly one
   terminal outcome for a started command; never infer cleanup from wrapper
   exit alone.
6. Stop at the first failed, timed-out, or interrupted targeted command. The
   repository gate is last by S3-06 construction: if it alone fails with its
   exact authorized gap, record `authorized_gap` rather than `passed`; there is
   no later command to continue.
7. After all started outcomes and log digests are complete, exclusively publish
   one turn-qualified `*.execution.json` record. An unexpected crash may leave
   diagnosable exclusive logs but must not leave an apparently complete record.
   Existing record or log paths are a collision and are never truncated or
   replaced.
8. Return the validated record/digest to the caller without reading Git,
   mutating the ledger, or choosing `accept`, `resume`, or `stop`.

## Required test evidence

Positive cases:

- The S3-01 unrestricted controls and supported permission matrix run through
  production invocation code, including normal execution, in-root write,
  `read-only`, `workspace-write`, local network allow/deny, and isolated
  separately authorized `danger-full-access`.
- Two local commands run in deterministic order and produce exact byte logs,
  SHA-256 values, argv/effective invocation, cwd, envelope, timestamps, exit
  code, and terminal reason in one valid record.
- A failing repository-gate-only command with the exact persisted gap records
  `authorized_gap`; it is not reported as passed.
- Empty stdout/stderr and non-UTF-8 output are preserved and digest-bound.

Negative cases:

- An invalid or unresolvable later command, unsupported sandbox, invalid root,
  bad identity, non-positive timeout, artifact escape, or any pre-existing
  output path fails preflight: no earlier command marker, log, or record exists.
- A failed targeted command prevents every later command; marker files prove
  non-execution.
- Timeout and externally triggered interruption each leave no live child or
  grandchild and publish one matching terminal outcome, using process events or
  bounded polling rather than sleeps.
- Out-of-root writes and denied loopback connections fail with no side effect;
  substituting an unrestricted runner makes the denial tests fail.
- Existing logs/record, a resolved executable changed before launch, partial
  log-write failure, or contradictory outcome data cannot publish or overwrite
  a complete command-execution record.

## Acceptance criteria

- **AC-01:** The allowed-command, denied-write, and denied-network proofs from
  S3-01 pass through production code rather than a test-only implementation.
- **AC-02:** Full-plan preflight failure runs no command and creates no command
  log or partial record.
- **AC-03:** Timeout and interruption leave no live child and record one
  terminal outcome using events/bounded polling rather than sleeps.
- **AC-04:** Commands run in deterministic order and later commands do not run
  after a targeted failure; only the repository-gate role can record an exact
  authorized gap.
- **AC-05:** Existing artifact paths cannot be overwritten.
- **AC-06:** The effective envelope, normalized and effective argv, exact log
  bytes/digests, cwd, timing, exit code, and terminal reason appear in each
  started outcome.
- **AC-07:** A complete command-execution record is published only after every
  started outcome is durable and validates against the S3-05 identity contract.
- **AC-08:** The runner has no Git, ledger, worker, tracker, commit, or acceptance
  responsibility.

## Verification

Run one test that fails while the S3-01 mechanism is still test-only, then:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_verification_runner.py
```

Then run the local-process timeout/interruption class, the aggregate
task-orchestrator suite, and `git diff --check`. The capability test may require
the same approved local loopback/nested-sandbox host permission recorded by
S3-01; it must not use external network access.

## Exit and handoff

Create `S3-07-result.md` and report the supported envelope, executable
resolution, process cleanup evidence, exact record/log paths, commands/results,
and residual risks. Stop before wiring the runner to controller inspection.
