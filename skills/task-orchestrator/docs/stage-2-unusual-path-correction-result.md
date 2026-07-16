# Stage 2 Result: Unusual Untracked Path Correction

Status: complete; Stage 2 re-closed
Date: 2026-07-16
Source plan: [stage-2-plan.md](stage-2-plan.md)
Trigger: [S3-03-result.md](stage-3-tasks/S3-03-result.md)

## Outcome

Corrected the Stage 2 closure path to collect untracked Git paths with
NUL-delimited byte output and `surrogateescape`, matching the established
`capture_git_status()` identity handling.

The task-scoped closure patch now includes allowed untracked files whose names
contain spaces, a leading dash, tabs, newlines, or shell metacharacters. The
shell-metacharacter case remains literal and creates no side effect.

The host does not support creating a filename containing a non-UTF-8 byte, so
that case remains uncharacterized rather than claimed as compatible.

## Files

- `../scripts/controller.py` — changed closure untracked-path collection from
  newline-delimited text to NUL-delimited byte parsing.
- `../tests/test_controller.py` — extended the fake-worker closure flow to
  assert exact unusual path identities, patch inclusion, and literal shell
  handling.

No Stage 3 extraction or production behavior was added. The historical S3-03
result remains unchanged; S3-03 can restart from its pre-edit gates.

## Verification

- The focused regression failed against the old parser because the tab and
  newline files were absent from the task patch, then passed after the fix.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py`
  — 39 tests passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_codex_worker.py`
  — 15 tests passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'`
  — 73 tests passed with local loopback permission. The sandboxed run reached
  72 passing tests before the verification-runner capability test was denied
  permission to bind loopback.
- All four task-orchestrator JSON files parsed with `jq`.
- The changed Python files parsed with `ast.parse` without bytecode generation.
- `git diff --check` and `git diff --cached --check` passed.
