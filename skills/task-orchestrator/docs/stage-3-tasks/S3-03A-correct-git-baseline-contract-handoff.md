# S3-03A Handoff: Correct the Git Baseline Contract

This file is a durable handoff for the first of two S3-03 remediation tasks.
Complete this task and publish its result before starting S3-03B.

Status: ready
Date: 2026-07-16
Workspace: `/Users/mtrusov/work/skill-sources/personal-skills`
Branch baseline: `main` at `5074da4`

## Resume Prompt

```text
You are implementing S3-03A in
/Users/mtrusov/work/skill-sources/personal-skills.

Correct the Stage 2 Git-baseline contract so every pre-existing dirty path
identity, including both sides of a rename, is available when constructing the
task-scoped patch. Start with the failing pre-existing-rename characterization
described below. Make the smallest contract correction that excludes all
baseline-dirty content from the task patch without hiding the durable-record
change. Do not perform the S3-03 module-boundary cleanup; S3-03B owns that work.

Read AGENTS.md and the required context below before editing. Verify Git status
and preserve unrelated user files. Do not rewrite Git history or modify existing
plan, task, result, S3-01, or handoff documents. Write completion evidence to a
new S3-03A result document.
```

## Outcome

Establish and implement one explicit Stage 2 contract for identifying
pre-existing dirty paths during closure capture. The contract must retain both
source and destination identities for a pre-existing Git rename so none of that
rename can enter a selected task's patch merely because one side is allowed.

This is a corrective contract task, not an attempt to replay or rewrite the
historical Stage 2 and S3-03 commits.

## Why This Task Is Separate

S3-03 was specified as a behavior-preserving extraction, but its fix commit
changed the Stage 2 task-patch behavior inside the extraction. The replacement
filter is also incomplete because the existing status dictionary discards the
source half of a porcelain rename entry.

Do not combine the contract decision with the later responsibility-boundary
cleanup. S3-03B must receive a tested baseline contract rather than inventing
one while refactoring.

## Required Context

Read completely before editing:

- repository `AGENTS.md`;
- `docs/stage-2-plan.md`, especially repository-baseline and closure evidence;
- `docs/stage-2-handoff.md`;
- `docs/stage-3-plan.md`, entry contract and architecture sections;
- `docs/stage-3-tasks/S3-03-extract-controller-git.md`;
- `docs/stage-3-tasks/S3-03-result.md`;
- `scripts/controller.py`;
- `scripts/controller_git.py`;
- `scripts/controller_state.py` only for digest/record contracts used here;
- `tests/test_controller.py`; and
- `tests/test_controller_git.py`.

## Confirmed Failure

The current implementation builds patch candidates with:

```python
path for path in allowed_paths if path not in task_baseline["status"]
```

For a staged pre-existing rename `old.txt -> new.txt`, porcelain-v1 `-z`
parsing stores only `new.txt` in the status dictionary and skips `old.txt`.
With `old.txt` allowed and no worker change after the baseline:

- the pre-existing-path violation lists are empty;
- the task patch is non-empty; and
- the patch contains a deletion of `old.txt`.

This violates S3-03 AC-06 and makes closure evidence attribute pre-existing
user work to the selected task.

## Contract Decision Required

Before implementation, state the chosen representation and why it is the
smallest sufficient contract. The representation must:

- preserve exact path identity for both sides of rename/copy status entries;
- survive persistence of the task baseline and its digest;
- let closure capture distinguish baseline-dirty paths from task-created paths;
- remain deterministic for spaces, leading dashes, tabs/newlines, and raw path
  bytes supported by the existing surrogate-escape strategy;
- avoid parsing human-quoted Git output; and
- avoid changing closure JSON fields unrelated to this correction.

Do not silently claim backward compatibility if the persisted task-baseline
shape or digest changes. Record that change explicitly in the result. Do not
add a generalized Git model, class hierarchy, schema framework, migration
system, or compatibility layer unless an existing contract demonstrably
requires it.

If more than one representation remains materially plausible after reading the
existing contracts, stop and ask the user rather than choosing silently.

## Allowed Changes

- `scripts/controller_git.py` for the corrected snapshot/path contract and
  task-patch exclusion;
- `scripts/controller.py` only if required to persist or consume the corrected
  task baseline;
- `tests/test_controller_git.py` for real temporary-Git characterization;
- `tests/test_controller.py` only for affected controller compatibility or
  fake-worker closure assertions; and
- new `docs/stage-3-tasks/S3-03A-result.md` for the completion record.

Do not modify:

- any existing plan, task, handoff, or result document;
- S3-01 files;
- `controller_state.py` unless a proven digest-contract defect makes it
  unavoidable and the user approves the scope expansion;
- CLI behavior, ledger transitions, worker launch, verification execution,
  acceptance, or commit mechanics; or
- Git history, staging, or unrelated working-tree files.

## Test-First Work

1. Add the smallest temporary-Git regression that:
   - commits `old.txt`;
   - creates a staged pre-existing `old.txt -> new.txt` rename;
   - captures the task baseline;
   - makes no worker change;
   - allows the source path, the destination path, and then both paths in
     focused subcases; and
   - proves no part of the pre-existing rename appears in the task patch.
2. Run that focused test and record that it fails for the expected reason
   before production changes.
3. Implement the selected baseline contract.
4. Extend the characterization only as needed to prove:
   - both rename identities are retained exactly;
   - unchanged pre-existing rename state is not classified as task work;
   - modifying or disappearing pre-existing rename state is detected;
   - allowed tracked and untracked changes made after the baseline still enter
     the task patch; and
   - unexpected and all other pre-existing dirty content remain excluded.
5. Keep artifact content and digest assertions independent of production
   helpers wherever practical.

Do not make the test pass by merely excluding every renamed path at closure
time without proving which paths were dirty at the persisted baseline.

## Acceptance Criteria

- **AC-A01:** A persisted task baseline retains the exact identities needed to
  exclude both sides of pre-existing rename/copy entries.
- **AC-A02:** An unchanged pre-existing rename contributes no bytes to the
  task-scoped patch regardless of whether its source, destination, or both are
  allowed.
- **AC-A03:** Modified or disappeared pre-existing rename state is surfaced as
  pre-existing-path drift and is not absorbed as allowed task work.
- **AC-A04:** Tracked, staged, unstaged, deleted, renamed, and untracked changes
  created after the baseline continue to produce the intended task patch.
- **AC-A05:** Unexpected paths and all baseline-dirty content are excluded from
  the task patch when mixed with allowed task changes.
- **AC-A06:** Odd path identity remains argv-safe and byte-preserving under the
  established Stage 2 strategy; no shell is introduced.
- **AC-A07:** Any durable task-baseline record or digest change is stated
  truthfully in `S3-03A-result.md`; unrelated closure fields remain unchanged.
- **AC-A08:** Existing controller and fake-worker flows remain compatible with
  the corrected baseline contract.

## Verification

Run one gate at a time, beginning with the focused failing regression:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest <exact-new-test-id>
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_git.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'
git diff --check
```

The aggregate suite's existing verification-sandbox capability test may need
approved execution outside the outer Codex sandbox because it binds localhost.
Do not reinterpret an outer-sandbox denial as a product failure.

Inspect the final task-scoped diff and confirm every changed line belongs to
the baseline-contract correction. Do not use a broad source-shape assertion as
the evidence.

## Current Verification Evidence

The review preceding this handoff observed:

- `test_controller_git.py`: 7 tests passed;
- `test_controller.py`: 39 tests passed;
- aggregate suite: 80 tests passed outside the outer sandbox;
- `git diff --check faaeabf..5074da4`: passed; and
- the focused pre-existing-rename reproduction failed AC-06 as described above.

These results establish the starting point; rerun the required checks after
editing.

## Exit And Handoff To S3-03B

Create `docs/stage-3-tasks/S3-03A-result.md`. Do not edit this handoff or any
existing plan/result document. The result must contain:

- the selected baseline representation and rejected alternatives;
- the exact durable-record compatibility impact;
- changed files;
- the red regression and final command results;
- acceptance criteria evaluated individually;
- residual risks; and
- an explicit `ready for S3-03B` or `blocked` verdict.

S3-03B must not begin unless this task reports `ready for S3-03B` and the
targeted controller Git and controller suites pass.

## Preserved Workspace State

At handoff creation, `main` matched `origin/main`. Preserve these pre-existing
untracked files:

- repository `AGENTS.md`; and
- `skills/task-orchestrator/agent-output.analysis.md`.

No background server or process is associated with this handoff.
