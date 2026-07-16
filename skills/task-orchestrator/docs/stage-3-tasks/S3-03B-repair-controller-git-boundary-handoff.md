# S3-03B Handoff: Repair the Controller Git Boundary

This file is a durable handoff for the second of two S3-03 remediation tasks.
Do not start until S3-03A has published a passing result.

Status: blocked until S3-03A
Date: 2026-07-16
Workspace: `/Users/mtrusov/work/skill-sources/personal-skills`
Branch baseline at handoff creation: `main` at `5074da4`

## Resume Prompt

```text
You are implementing S3-03B in
/Users/mtrusov/work/skill-sources/personal-skills.

First read docs/stage-3-tasks/S3-03A-result.md and verify that it says
"ready for S3-03B" and that its targeted suites pass. If the file is missing,
blocked, or its contract is unclear, stop without editing.

Repair the S3-03 module boundary against that corrected Git-baseline contract.
Keep controller_git.py observational: it may execute Git, parse snapshots,
compare values, and publish immutable text artifacts, but controller.py must
own the policy decision that a changed HEAD or index violates the current
worker operation. Preserve closure JSON/artifact behavior established by
S3-03A, strengthen closure-path unusual-name and wiring coverage, and remove no
unrelated files.

Read AGENTS.md and the required context below before editing. Preserve user
changes. Do not rewrite history or modify existing plan, task, result, S3-01,
or handoff documents. Write completion evidence to a new S3-03B result file.
```

## Dependency And Entry Criteria

All of the following are required before editing:

- `docs/stage-3-tasks/S3-03A-result.md` exists and reports
  `ready for S3-03B`;
- the result states the exact corrected task-baseline representation and any
  compatibility impact;
- the focused controller Git suite passes;
- the controller suite passes; and
- no overlapping user edits exist in `controller.py`, `controller_git.py`, or
  their owning tests.

If any entry criterion is false, stop and report the blocker. Do not repair or
reinterpret S3-03A inside this task.

## Outcome

Finish the functional Git extraction so:

- `controller_git.py` owns Git command execution, parsing, raw observations,
  deterministic comparison data, and immutable closure text artifacts;
- `controller.py` owns worker-operation policy, violation reasons, closure
  decisions, ledger mutation, transitions, and worker launch;
- Stage 2 closure fields, artifact bytes, and digests match the corrected
  S3-03A contract; and
- tests prove the controller uses both the task-baseline and closure-evidence
  functions from the Git boundary.

Do not redesign the controller, introduce classes or dependency-injection
machinery, add commit mechanics, or expand into later Stage 3 tasks.

## Required Context

Read completely before editing:

- repository `AGENTS.md`;
- `docs/stage-3-plan.md`, entry contract and architecture sections;
- `docs/stage-3-tasks/S3-03-extract-controller-git.md`;
- `docs/stage-3-tasks/S3-03-result.md`;
- `docs/stage-3-tasks/S3-03A-correct-git-baseline-contract-handoff.md`;
- `docs/stage-3-tasks/S3-03A-result.md`;
- `scripts/controller.py`;
- `scripts/controller_git.py`;
- `scripts/controller_state.py` only for existing record/digest contracts;
- `tests/test_controller.py`; and
- `tests/test_controller_git.py`.

## Confirmed Boundary Defect

The current Git module computes policy-specific violation messages:

```python
if head_changed:
    mechanical_violations.append("worker changed HEAD despite commit prohibition")
if index_changed:
    mechanical_violations.append("worker changed the Git index")
```

This violates S3-03 AC-03. Whether an observed identity change is prohibited
depends on the controller operation. Later controller-owned commit operations
must not inherit worker-specific policy from an observation module.

The smallest intended repair is for `controller_git.py` to return raw
comparison facts such as `head_changed` and `index_changed`, while
`controller.py` converts those facts into the existing closure violation
messages for `run-next`. Preserve the public closure packet unless S3-03A
explicitly establishes a related correction.

## Allowed Changes

- `scripts/controller.py` for operation-specific policy and closure assembly;
- `scripts/controller_git.py` for raw observation records and artifact
  publication;
- `tests/test_controller_git.py` for Git-boundary and unusual-path coverage;
- `tests/test_controller.py` only for controller policy and full fake-worker
  integration assertions; and
- new `docs/stage-3-tasks/S3-03B-result.md` for the completion record.

Do not modify:

- S3-03A implementation semantics or its result;
- any existing plan, task, handoff, or result document;
- S3-01 files;
- CLI behavior, record schemas unrelated to S3-03A, worker transport,
  verification execution, acceptance, recovery, or commit creation;
- Git history or staging; or
- unrelated working-tree files.

## Work

1. Establish the post-S3-03A targeted baseline before editing.
2. Add or adjust a controlled test proving the Git boundary returns raw HEAD
   and index comparison facts without choosing worker-policy consequences.
3. Move construction of worker-specific mechanical-violation reasons to
   `controller.py` while preserving their closure JSON location and text.
4. Keep Git argv and parsing logic out of `controller.py`; its only remaining
   subprocess execution may be the worker adapter launch.
5. Strengthen `run-next` wiring evidence so a test fails if the controller
   bypasses either:
   - `capture_task_baseline`; or
   - `capture_closure_evidence`.
6. Exercise the complete closure-evidence path, not only status capture, for:
   - spaces;
   - a leading dash;
   - tabs and newlines;
   - shell metacharacters; and
   - non-UTF-8 bytes where the established filesystem/surrogate-escape strategy
     supports them.
7. For unusual paths, assert exact identity, literal argv behavior, artifact
   readability, and matching digests. Keep the non-UTF-8 limitation explicit
   if the execution sandbox still prevents direct filesystem creation.
8. Inspect the final task-scoped diff for duplicate Git observation/parsing
   logic and responsibility leakage.

Do not satisfy wiring coverage with a broad source-text assertion. Use a
controlled boundary substitution or observable fake-worker flow.

## Acceptance Criteria

- **AC-B01:** `controller_git.py` returns observations and comparison facts but
  no worker-policy violation messages, ledger mutations, transitions, worker
  launch, acceptance, or commit decisions.
- **AC-B02:** `controller.py` applies the worker commit/index prohibition and
  preserves the existing closure reason text and packet location.
- **AC-B03:** Git subprocess and parsing logic are not duplicated in
  `controller.py`.
- **AC-B04:** Closure JSON fields, artifact bytes, and digests remain compatible
  with the corrected S3-03A contract.
- **AC-B05:** A fake-worker `run-next` flow proves both Git-boundary entry points
  are used and preserves the complete closure packet.
- **AC-B06:** Controlled nonzero Git commands surface failure and cannot return
  complete evidence or publish an apparently complete closure record.
- **AC-B07:** Required unusual paths retain exact identity through the closure
  evidence and artifact path, with no shell interpretation or side effect.
- **AC-B08:** The controller Git, controller, and aggregate suites pass, and the
  final diff contains only allowed files.

## Verification

Run one gate at a time. Start with the post-S3-03A baseline, then the narrowest
new or changed test:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_git.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest <exact-new-or-changed-test-id>
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_git.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'
git diff --check
```

The aggregate suite's verification-sandbox capability test may require
approved execution outside the outer Codex sandbox because it binds localhost.
Do not reinterpret an outer-sandbox denial as a product failure.

Use task-scoped inspection to confirm `controller.py` contains no Git argv or
parsing implementation. Record exact command counts and results; do not copy
historical counts into the result.

## Review Evidence Available At Handoff Creation

The preceding read-only review established:

- commits reviewed: `faaeabf..5074da4`;
- the controller Git suite passed 7 tests;
- the controller suite passed 39 tests;
- the aggregate suite passed 80 tests outside the outer sandbox;
- `git diff --check faaeabf..5074da4` passed;
- Git parsing/subprocess code was removed from `controller.py`; and
- the current Git module still creates worker-specific mechanical violations.

Treat these as historical evidence only. The authoritative starting point for
this task is the completed S3-03A result and current filesystem state.

## Exit

Create `docs/stage-3-tasks/S3-03B-result.md`. Do not edit this handoff, S3-03A's
result, or the original S3-03 result. The new result must report:

- Git operations and raw records owned by `controller_git.py`;
- policy decisions retained by `controller.py`;
- changed files;
- acceptance criteria evaluated individually;
- exact verification commands and results;
- task-scoped duplicate-logic inspection;
- residual risks; and
- one verdict: `complete` or `blocked`.

Stop before verification execution, acceptance, recovery, commit creation, or
cleanup of the unrelated S3-01 commit history.

## Preserved Workspace State

At handoff creation, `main` matched `origin/main`. Preserve these pre-existing
untracked files:

- repository `AGENTS.md`; and
- `skills/task-orchestrator/agent-output.analysis.md`.

No background server or process is associated with this handoff.
