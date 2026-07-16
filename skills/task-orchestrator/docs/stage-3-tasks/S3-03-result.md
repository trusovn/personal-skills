# S3-03 Result: Controller Git Observation Extraction

Status: blocked; returned to Stage 2
Date: 2026-07-16

## Outcome

Stopped before extraction because the required pre-edit unusual-path
characterization exposed an existing Stage 2 closure-evidence gap.

`capture_git_status()` preserves spaces, leading dashes, tabs, newlines, and
shell metacharacters as exact path identities by using NUL-delimited Git output
and `surrogateescape`. The closure path instead parses newline-delimited
`git ls-files --others --exclude-standard` text. Git quotes tab and newline
paths in that output, so the parsed `untracked_paths` values no longer equal the
allowed paths. Those allowed untracked files are consequently omitted from the
task-scoped patch.

The controlled shell-metacharacter path remained literal and created no side
effect. This macOS host rejected creation of a filename containing a non-UTF-8
byte with `EILSEQ`, so that case is unsupported by the host and produced no
controller compatibility result.

Per S3-03's entry criteria and AC-07, this gap must be corrected and
characterized in Stage 2 before the behavior-preserving extraction proceeds.
No production or test files were changed, and no `controller_git.py` module was
created.

## Verification

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py`
  — 39 tests passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'`
  — 73 tests passed with local loopback permission. The sandboxed run reached
  72 passing tests before the pre-existing verification-runner capability test
  was denied permission to bind loopback.
- Focused temporary-Git characterization — status identities were exact, but
  closure parsing returned `"tab\\tname.txt"` and `"line\\nname.txt"` as quoted
  strings instead of the original paths. The shell-metacharacter control had no
  side effect.

## Required next action

Return to Stage 2 and change closure untracked-path collection to the
established NUL-delimited byte-safe strategy, add pre/post regression evidence
for task-patch inclusion and exact identity, and re-close Stage 2. Then restart
S3-03 from its pre-edit gates.
