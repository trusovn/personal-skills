# Session Handoff

This file is a durable companion to the copy/paste handoff. The copy/paste
packet is still the primary resume context.

Generated: 2026-07-16 18:31 WEST

Workspace: `/Users/mtrusov/work/skill-sources/personal-skills`

Branch: `task-04-high` at `135d5c4`

Primary goal: correct the incomplete S3-04 Stage 3 state-model implementation
so its ledger coherence, transition authority, immutable state, optimistic
revision, and regression-test contracts fully match the approved plan.

Latest user request: hand this corrective work to another agent with detailed
implementation and verification instructions.

## Resume Prompt

Paste this into the next session:

```text
You are continuing S3-04 corrective work in `/Users/mtrusov/work/skill-sources/personal-skills` on branch `task-04-high`.

Treat `skills/task-orchestrator/docs/session-handoff.md` as the operational brief. Verify the branch and dirty state before editing. Read the repository `AGENTS.md`, the S3-04 task brief, the current S3-04 result, and the exact implementation/tests listed in the handoff.

Fix the four confirmed review findings using test-first, surgical changes. Start with a regression test proving that a `ready` ledger containing an unselected `running` task is rejected; run it and record the intended pre-fix failure before changing production code. Then complete the remaining regression tests and minimal implementation described in the handoff.

Do not copy or cherry-pick the sibling S3-04 implementation from `main`; it is a different implementation and is not the reviewed scope. Do not edit the Stage 3 master plan, the S3-04 task brief, or `S3-04-result.md`. Write the correction outcome to a new adjacent `S3-04-correction-result.md` after all checks pass. Preserve unrelated untracked files and do not use the network, install dependencies, invoke a live model, commit, reset, or clean.
```

## Current State

- Commit `135d5c4` implements S3-04 on top of parent `541c558`.
- A read-only review found one high-severity ledger-coherence defect and three
  material state/update/test-contract gaps. The result is not ready to be
  considered complete.
- Existing verification is green:
  - 17 `test_controller_state.py` tests pass.
  - 40 `test_controller.py` tests pass.
  - 90 aggregate task-orchestrator tests pass.
  - Four task-orchestrator JSON files parse.
  - The four S3-04 Python implementation/test files parse with `ast.parse`.
  - `git diff --check 541c558..135d5c4` passes.
- No corrective source or test changes have been made yet.
- This handoff replaces the previous generic session handoff. Do not restore
  the obsolete Stage 2 handoff content.
- The current branch and `main` diverge after `541c558`. `main` contains sibling
  commit `30fa947`, also titled `Task 04: Extend the Stage 3 State Model`. It is
  not the reviewed implementation and must not be used as an implicit patch.
- No background server, worker, or monitoring process is running.

## Sources Of Truth

Read these before editing, in this order:

1. `AGENTS.md`
2. `skills/task-orchestrator/docs/stage-3-plan.md`
   - Focus on settled decisions, controller-lock lifetime, durable records,
     task execution contract, and Stage 3 stop conditions.
3. `skills/task-orchestrator/docs/stage-3-tasks/S3-04-stage-3-state-model.md`
4. `skills/task-orchestrator/docs/controller-contract.md`
5. `skills/task-orchestrator/docs/stage-3-tasks/S3-04-result.md`
6. `skills/task-orchestrator/scripts/controller_state.py`
7. `skills/task-orchestrator/scripts/controller.py`
8. `skills/task-orchestrator/tests/test_controller_state.py`
9. `skills/task-orchestrator/tests/test_controller.py`

The S3-04 task brief and controller contract outrank claims in
`S3-04-result.md`. Do not weaken those contracts merely to preserve current
tests.

## Confirmed Findings To Fix

### 1. Reject unselected active task states

Current problem:

- `validate_ledger` validates the state of the selected task but does not reject
  active states on other tasks.
- A `ready` ledger can therefore contain one `ready` task and another
  unselected `running` task with an attempt history.
- `apply_ledger_update` accepts this state. A subsequent `run-next` can select
  the ready task and launch another worker, violating the single-worker
  invariant.

Confirmed reproduction output:

```text
unselected_active_task_accepted= ['ready', 'running']
```

Required correction:

- Define and enforce the per-run compatibility of all task states, not only the
  selected task.
- For `running`, `awaiting_inspection`, `resumable`, and `finalizing`, exactly
  one task may occupy the corresponding active lifecycle position, and it must
  be the selected task:
  - run `running` -> selected task `running`;
  - run `awaiting_inspection` -> selected task `awaiting_inspection`;
  - run `resumable` -> selected task `resumable`;
  - run `finalizing` -> selected task remains `awaiting_inspection`.
- No unselected task may be `running`, `awaiting_inspection`, or `resumable`.
- Runs `initialized`, `ready`, and `stopped` must contain no task in one of
  those active lifecycle states.
- Preserve legitimate non-active entries such as `initialized`, `ready`,
  `accepted`, and `stopped`; do not require every task to share the run state.

Required regression cases:

- A `ready` run with one ready task and another unselected `running` task is
  rejected.
- A `running` run with the selected running task plus a second running task is
  rejected.
- A `stopped` run retaining a running, awaiting-inspection, or resumable task is
  rejected.
- A `finalizing` run with any second active-state task is rejected.
- Existing coherent fixtures for every run state continue to validate.

### 2. Preserve the acceptance transition guard

Current problem:

- `apply_ledger_update` checks task transitions directly against
  `ALLOWED_TASK_TRANSITIONS` instead of calling `transition_task`.
- This bypasses the existing rule that `awaiting_inspection -> accepted`
  requires an accepting decision with the expected identity.
- A finalizing ledger can be moved to ready while accepting its selected task
  without supplying any acceptance evidence.

Confirmed reproduction output:

```text
accept_without_decision_guard= ['accepted', 'ready']
```

Required correction:

- Route every changed task state through `transition_task` rather than
  duplicating only its table-membership check.
- Extend `apply_ledger_update` only as needed to pass the existing
  `closure_decision` and `expected_identity` inputs to `transition_task`.
- Do not invent S3-05 record schemas or S3-11/S3-12 effects-complete operation
  validation in this correction. Those later tasks strengthen the authority
  chain. This correction must at least avoid bypassing the already-approved
  transition guard.

Required regression cases:

- The finalizing-to-ready update that changes the selected task from
  `awaiting_inspection` to `accepted` fails when no accepting decision is
  supplied.
- The same transition fails for a stale/mismatched expected identity.
- A positive case with the currently required accepting decision and exact
  identity succeeds, so the allowed transition remains executable.
- Rejected pure updates leave the original input object unchanged.

### 3. Make revision and top-level ledger authority immutable

Current problem:

- `expected_revision` defaults to `None` in both `apply_ledger_update` and the
  controller's `update_ledger` wrapper.
- Omitting it successfully advances the ledger, even though the master plan
  requires every existing-run mutation phase to pair the lock with an expected
  revision.
- The update dictionary can also replace controller-owned run authority such
  as `run_id`, `repository`, policy/manifest identity, and initial-baseline
  identity.

Confirmed reproduction output:

```text
update_without_expected_revision= 2
authority_rewrite_accepted= different-run replacement
```

Required correction:

- Make `expected_revision` a required keyword argument in
  `controller_state.apply_ledger_update`.
- Make `expected_revision` required in `controller.update_ledger`.
- Update every production and test call site. Do not retain a compatibility
  default that defeats the executable contract.
- Reject changes to these top-level immutable fields:
  - `version`
  - `run_id`
  - `repository`
  - `created_at`
  - `policy_path`
  - `policy_sha256`
  - `manifest_path`
  - `manifest_sha256`
  - `initial_baseline_path`
  - `initial_baseline_digest`
- Continue treating `completed_task_ids` as separately immutable.
- Keep `updated_at` and `revision` controller-managed.
- Preserve the existing immutable task identity, order, authority fields, and
  append-only attempt-history checks.
- Perform all validation before the atomic persistence wrapper writes bytes.

Required regression cases:

- The function cannot be called without `expected_revision`.
- A stale revision rejects the update and leaves input/persisted bytes
  unchanged.
- Table-driven mutations of each immutable top-level field are rejected and
  leave the input unchanged.
- An updater-supplied `revision` remains rejected.
- Valid controller transitions still advance the revision by exactly one.

### 4. Freeze the planned transition tables independently in tests

Current problem:

- `test_all_run_and_task_transitions_are_explicit` iterates
  `RUN_STATES`/`TASK_STATES` and uses the implementation's own allowed maps as
  its oracle.
- If a state or transition is accidentally removed from both implementation
  structures, the test remains green.

Required correction:

- Define the exact expected run and task transition maps literally in the
  test, matching the S3-04 brief.
- Assert equality between those expected maps and the production maps.
- Exercise every state pair using the literal expected maps as the oracle.
- Keep the special positive acceptance arguments for the one allowed
  `awaiting_inspection -> accepted` task transition.
- Explicitly prove no transitions leave task `accepted` or `stopped`, and no
  transitions leave run `stopped`.
- Do not add a generalized transition-testing abstraction; one small explicit
  table test is sufficient.

## Implementation Sequence

Use this order to preserve test-first evidence and keep failures attributable:

1. Inspect `git status --short` and record the existing unrelated untracked
   files. Do not modify them.
2. Add only the first unselected-active-task regression test.
3. Run that one test and confirm it fails because the incoherent ledger is
   accepted, not because of import, fixture, or syntax failure.
4. Add the remaining focused state regression tests described above.
5. Make the minimal `controller_state.py` changes for global state coherence,
   task transition routing, required revisions, and immutable ledger authority.
6. Adjust the controller wrapper signature and every current call site. The
   three production `run-next` updates already pass expected revisions; verify
   rather than broadly refactor them.
7. Run the state module. Fix only failures caused by the corrected contract.
8. Run the controller module. Preserve the existing lock/contention test and
   its process-event or bounded-polling approach.
9. Run the aggregate suite and static/artifact checks.
10. Inspect the complete task-scoped diff and confirm every changed line traces
    to a finding or its verification.
11. Create
    `skills/task-orchestrator/docs/stage-3-tasks/S3-04-correction-result.md`
    with changed files, each finding resolved, fail-first evidence, exact
    commands/results, and residual risks. Do not edit the master plan, task
    brief, or original result document.

## Allowed Change Scope

- `skills/task-orchestrator/scripts/controller_state.py`
- `skills/task-orchestrator/scripts/controller.py` only for the required
  revision/transition wrapper and call-site compatibility
- `skills/task-orchestrator/tests/test_controller_state.py`
- `skills/task-orchestrator/tests/test_controller.py` only where controller
  wrapper or persisted-byte behavior requires integration evidence
- New
  `skills/task-orchestrator/docs/stage-3-tasks/S3-04-correction-result.md`

Do not edit:

- `skills/task-orchestrator/docs/stage-3-plan.md`
- `skills/task-orchestrator/docs/stage-3-tasks/S3-04-stage-3-state-model.md`
- `skills/task-orchestrator/docs/stage-3-tasks/S3-04-result.md`
- Policy or manifest schemas
- `controller_git.py`, `codex_worker.py`, verification-runner files, or other
  Stage 3 task briefs

## Success Criteria

The correction is complete only when all of these are true:

- Every S3-04 run/task transition map exactly matches the literal plan-owned
  table and every unlisted pair is rejected.
- A valid ledger cannot contain an unselected active-state task.
- `running` has exactly one selected running task and its latest active attempt.
- `awaiting_inspection`, `resumable`, and `finalizing` each retain exactly the
  intended selected task/attempt/reference shape and no second active task.
- `initialized`, `ready`, and `stopped` contain no active task state and retain
  no selected task or active attempt.
- No task becomes `accepted` through `apply_ledger_update` while bypassing the
  existing transition authority check.
- Every pure or persisted ledger update requires the caller's exact expected
  revision.
- Top-level run, repository, policy, manifest, and baseline authority cannot be
  rewritten through the updater.
- Rejected updates do not mutate their input object or persisted ledger bytes.
- Existing readiness, post-acceptance selection, lock contention, duplicate
  launch prevention, and stale terminal reconciliation behavior still pass.
- No public CLI command, dependency, network behavior, live-model behavior, or
  later-stage record validator is added.

## Verification Commands

Run one command at a time in this order. Replace the `-k` substring with the
actual focused regression-test name if it differs.

1. Required fail-first proof before production edits:

   ```text
   PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -k unselected_active_task skills/task-orchestrator/tests/test_controller_state.py
   ```

   Expected before the fix: one assertion failure proving the invalid ledger
   was accepted. Record the exact failure in the correction result.

2. Focused state module:

   ```text
   PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py
   ```

3. Controller integration module:

   ```text
   PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py
   ```

4. Aggregate task-orchestrator suite:

   ```text
   PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'
   ```

5. Parse all task-orchestrator JSON files with the Python standard library.

6. Parse every changed Python file using `ast.parse` with
   `PYTHONDONTWRITEBYTECODE=1`.

7. Whitespace and conflict-marker check:

   ```text
   git diff --check
   ```

8. Final scope and preservation checks:

   ```text
   git status --short
   git diff --name-only
   git diff -- skills/task-orchestrator/scripts/controller_state.py skills/task-orchestrator/scripts/controller.py skills/task-orchestrator/tests/test_controller_state.py skills/task-orchestrator/tests/test_controller.py skills/task-orchestrator/docs/stage-3-tasks/S3-04-correction-result.md
   ```

Report actual test counts; do not copy the current 17/40/90 counts after adding
tests. Do not claim a command passed unless it was run in the correcting
session.

## Files And Artifacts

- `skills/task-orchestrator/docs/session-handoff.md` — this newly replaced
  corrective handoff; created by the review/handoff session.
- `skills/task-orchestrator/docs/stage-3-tasks/S3-04-stage-3-state-model.md` —
  authoritative S3-04 brief; read-only.
- `skills/task-orchestrator/docs/stage-3-tasks/S3-04-result.md` — original
  implementation report; read-only and currently overstates completion.
- `skills/task-orchestrator/scripts/controller_state.py` — primary corrective
  implementation target.
- `skills/task-orchestrator/scripts/controller.py` — expected-revision wrapper
  and call-site target only.
- `skills/task-orchestrator/tests/test_controller_state.py` — primary
  regression-test target.
- `skills/task-orchestrator/tests/test_controller.py` — integration evidence
  target only where necessary.
- `skills/task-orchestrator/docs/stage-3-tasks/S3-04-correction-result.md` — new
  completion artifact to create after verification.

## Commands And Evidence Already Collected

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py`
  — passed, 17 tests.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py`
  — passed, 40 tests.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'`
  — passed, 90 tests.
- Focused read-only reproductions confirmed all three implementation-level
  bypasses described above.
- Four JSON files parsed and four changed Python files passed `ast.parse`.
- `git diff --check 541c558..135d5c4` passed.
- The S3-04 commit changed exactly the five files allowed by the original task.
- Not run: live Codex/model, networked checks, dependency installation,
  external review service, destructive Git commands, commit/push, or later
  Stage 3 command flows.

## Dirty Worktree And Ownership

Before this handoff was created, the worktree contained these unrelated
untracked files:

- `AGENTS.md` — user-provided repository instructions; preserve unchanged.
- `skills/task-orchestrator/agent-output.analysis.md` — pre-existing untracked
  analysis; preserve unchanged and do not use as authority unless the user
  explicitly requests it.

This session replaced only:

- `skills/task-orchestrator/docs/session-handoff.md`

The correcting agent must re-run `git status --short` because filesystem state
may have changed after this handoff was written.

## Decisions And Guardrails

- One corrective task is preferable to multiple handoffs because all findings
  share `controller_state.apply_ledger_update`, `validate_ledger`, and the same
  state test fixture. Parallel or independent edits would conflict.
- Stay Python standard-library-only and preserve the functional split already
  established by S3-02.
- Keep changes surgical. Do not introduce classes, storage abstractions,
  generalized workflow machinery, or another module.
- Preserve the current `resumable` contract from the S3-04 brief: one selected
  task/current attempt in history, no active process, and therefore no
  `active_attempt_id`.
- Do not weaken finalizing coherence: the selected task remains
  `awaiting_inspection` and closure, verification, decision, and prepared
  operation references remain required.
- Do not redesign readiness or append accepted IDs to
  `completed_task_ids`; accepted completion remains derived from task entries.
- Keep the command lock non-blocking and preserve the existing release/reacquire
  lifetime around the worker wait.
- Do not update existing plan documents or the original result. Create the new
  correction result next to them.
- Stop and ask the user if the correction requires policy/manifest version 1
  changes, a new dependency, network access, live-model behavior, or files
  outside the allowed scope.

## Expected Handoff From The Correcting Agent

Return a concise completion report containing:

1. Changed files.
2. Each of the four findings and the exact behavior now enforcing it.
3. The fail-first test and its intended pre-fix failure.
4. Exact focused and aggregate commands with actual counts/results.
5. Static/artifact check results.
6. Residual risks or `none known`.
7. A clear `ready for repeat S3-04 review` or `blocked` verdict.
