# S3-07 Result: Sandboxed Verification Executor

Status: complete implementation submission; reviewer correction verified and accepted
Date: 2026-07-21

## Outcome

Completed `verification_runner.py` so an S3-06 command plan is fully validated
and preflighted before artifacts or plan commands are created. The runner
canonicalizes the repository cwd and writable roots, resolves and fingerprints
every executable, constructs every effective Seatbelt argv, proves the adopted
mechanism locally, and then executes commands sequentially with `shell=False`
and a new process group.

The S3-01 Seatbelt profile construction now lives in production code. The
existing unrestricted controls and supported permission matrix call that
production implementation for `read-only`, `workspace-write`, network
allow/deny, and separately authorized `danger-full-access` behavior.

## Supported envelope and executable resolution

The executor accepts exactly the complete version 1 permission envelope:

- `sandbox`: `read-only`, `workspace-write`, or separately authorized
  `danger-full-access`;
- `approval_policy`: exactly `never`;
- boolean `network`, `dependency_install`, and
  `danger_full_access_authorized`; and
- canonicalizable existing absolute `writable_roots`, excluding `/`.

The host must be macOS with the exact executable `/usr/bin/sandbox-exec`.
Before launch, a command name is resolved through the current process `PATH`,
while an argv containing `/` is resolved relative to the canonical repository
cwd or as an absolute path. The resolved executable must be a regular
executable file. Its device, inode, mode, size, nanosecond mtime, and SHA-256
fingerprint are rechecked immediately before its command is launched.

## Records, logs, and cleanup

For attempt `attempt-001`, turn 1, the immutable output family is exactly:

```text
verification/attempt-001.turn-001.execution.json
verification/attempt-001.turn-001.command-001.stdout.log
verification/attempt-001.turn-001.command-001.stderr.log
```

Later command IDs use the same turn-qualified pattern. Paths must remain under
the canonical run directory, and every planned record/log collision is checked
before the capability probe or first command. Files use exclusive creation and
are never truncated or replaced.

Stdout and stderr are drained as byte streams into exclusive files by bounded
reader threads. The record binds the normalized plan argv, exact effective
sandbox argv, canonical cwd, complete effective envelope, timestamps, exit
code, terminal status, log paths, and SHA-256 digests. Empty and non-UTF-8
streams remain byte-exact. The canonical execution record is validated against
the S3-05 closure identity and exclusively published only after started-command
logs are flushed and synced.

Timeout or interruption sends `SIGTERM` to the owned process group and reaps
the group leader, but does not infer group cleanup from leader exit. It probes
the process group, escalates remaining descendants to `SIGKILL`, and uses
bounded polling until the group is absent. A transient `PermissionError` while
signaling remains ambiguous and proceeds to that bounded existence proof rather
than escaping or being treated as successful cleanup. Each byte-stream reader
closes its captured pipe in a `finally` block. Tests observe both ordinary child
and grandchild absence, a grandchild that ignores `SIGTERM`, and the group-leader
exit race while a descendant retains captured pipes. A log stream/write/
collection failure performs the same cleanup and cannot publish a complete
record.

## Acceptance-criteria evidence

- AC-01: the S3-01 capability matrix now delegates to
  `build_sandbox_invocation()` in production.
- AC-02: an unresolvable later executable and a later artifact collision leave
  no earlier marker, new log, or record.
- AC-03: real timeout and externally triggered interruption cases record one
  matching terminal outcome and leave child/grandchild processes absent; an
  adversarial timeout case proves a `SIGTERM`-resistant grandchild is killed.
- AC-04: two commands prove deterministic order; targeted failure prevents all
  later execution; only an exact repository-gate-only failure records
  `authorized_gap`.
- AC-05: existing log and record bytes remain unchanged.
- AC-06: the valid-record case checks effective argv/envelope, normalized argv,
  cwd, timestamps, exit code, binary logs, and exact SHA-256 values.
- AC-07: identity validation precedes execution; injected log-write failure and
  contradictory record states cannot publish a complete record.
- AC-08: the production module contains no Git inspection, ledger, worker,
  tracker, commit, or acceptance behavior.

## Verification

- Required fail-first production invocation:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills.task-orchestrator.tests.test_verification_runner.VerificationSandboxFailClosedTests.test_production_builds_the_adopted_sandbox_invocation`
  failed with `AttributeError` before implementation, then passed.
- Reviewer-correction fail-first:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills.task-orchestrator.tests.test_verification_runner.VerificationExecutorLocalProcessTests.test_timeout_kills_a_grandchild_that_ignores_sigterm`
  failed because the resistant grandchild remained alive, then passed after
  process-group polling and escalation were added.
- Process-group exit-race correction fail-first:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills.task-orchestrator.tests.test_verification_runner.VerificationProcessGroupCleanupTests.test_group_exit_race_does_not_leak_permission_error`
  failed with an uncaught `PermissionError`, then passed after ambiguous signal
  failures were routed through bounded group-existence polling.
- The inherited-pipe cleanup probe passed three consecutive runs without
  watchdog cleanup or unclosed-pipe warnings.
- Focused executor local-process class, using approved host permission: passed
  13 tests.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_verification_runner.py`,
  using approved host permission: passed 34 tests.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py`:
  passed 36 tests.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'`,
  using approved host permission: passed 139 tests.
- `git diff --check`: passed.

## Residual risks and boundary

The adopted sandbox remains the S3-01 pathname-scoped mechanism: pre-existing
cross-boundary hard links are an operator-owned repository-hygiene limitation,
and `/usr/bin/sandbox-exec` is deprecated and host-version-sensitive. Executable
fingerprinting closes detectable replacement before launch but, like any
pathname-based exec, retains the minimal operating-system race between the last
check and `execve`.

This task stops before controller inspection, Git drift collection, ledger
mutation, closure decisions, acceptance, or controller wiring. A fresh guided
acceptance review of the corrected task-scoped diff and host-boundary evidence
returned `ACCEPT` with no findings.
