# S3-01 Result: Verification Sandbox Boundary

Status: complete
Date: 2026-07-16

## Final decision

Adopt the macOS `/usr/bin/sandbox-exec` mechanism documented in
[`../verification-sandbox-decision.md`](../verification-sandbox-decision.md)
for the version 1 verification boundary.

The approved scope is pathname-scoped write enforcement, not inode isolation.
A pre-existing hard link can alias an out-of-root inode through an in-root
pathname, so the operator owns the repository-hygiene precondition that
configured writable roots contain no cross-boundary hard-link aliases. The
runner intentionally adds no race-prone prelaunch scan. Stronger container or
microVM isolation remains deferred defense-in-depth rather than an S3-01 or
S3-07 responsibility.

Under that explicit scope reduction, the decision satisfies S3-01 AC-01 through
AC-06: it selects one exact local mechanism, exercises positive and negative
filesystem/network controls, maps or rejects the version 1 permission values,
fails closed on unsupported configurations, and adds no dependency, external
network access, model call, or production runner code.

## Verification evidence

The final focused verification was run on the supported macOS host outside the
outer Codex sandbox so the local loopback control and nested `sandbox-exec`
boundary could operate:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_verification_runner.py
.......
----------------------------------------------------------------------
Ran 7 tests in 0.151s

OK
```

The seven tests cover the supported permission matrix plus fail-closed handling
for an unsupported host and mode, a substituted unrestricted runner, missing
writable-root enforcement, unauthorized `danger-full-access`, and an
incomplete permission envelope.

## Downstream authorization

S3-01 no longer blocks S3-07. S3-07 may proceed under the approved
pathname-scoped contract and operator-owned hard-link hygiene precondition.
S3-06 still owns executable and argument preflight; S3-07 owns production
execution records, sequencing, timeout handling, and cleanup.
