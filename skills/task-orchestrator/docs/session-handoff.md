# Session Handoff

This file is a durable companion to the copy/paste handoff. The copy/paste packet is still the primary resume context.

Generated: 2026-07-16 00:01 WEST

Workspace: `/Users/mtrusov/work/skill-sources/personal-skills`

Branch: `main`

Primary goal: implement Stage 2 of the `task-orchestrator` redesign so one run,
one dependency-ready task, one worker attempt, the controller ledger, and the
closure packet are deterministic and durable.

Latest user request: review the Stage 1 implementation against the direction and
plan, create a detailed Stage 2 implementation plan, and refresh this handoff for
another agent.

## Resume Prompt

Paste this into the next session:

```text
You are continuing the task-orchestrator redesign in `/Users/mtrusov/work/skill-sources/personal-skills`.

Start by reading, in order:
1. `skills/task-orchestrator/docs/direction.md`
2. `skills/task-orchestrator/docs/stage-1-handoff.md`
3. `skills/task-orchestrator/docs/stage-2-plan.md`
4. `skills/task-orchestrator/docs/session-handoff.md`
5. the Stage 1 contract, policy schema, controller, worker adapter, and tests referenced by the Stage 2 plan.

Treat `stage-2-plan.md` as the execution plan. Its Stage 1 review verdict is CHANGES REQUESTED, so start with the two first failing tests named under “First implementation action”: strict nested run-policy validation and rejection of worker-claimed verification when independent controller evidence is missing. Do not start the manifest or initializer until those targeted tests pass.

Implement only Stage 2: close the listed dispatch-safety prerequisites, add strict manifest validation, atomically initialize one run outside the repository, select and launch exactly one dependency-ready task through a strict fake transport in tests, persist the ledger, and emit a closure packet. Stop at awaiting_inspection. Do not accept, resume, update trackers, commit, select a second task, rewrite SKILL.md, install dependencies, use the network, or invoke a live Codex model unless the user separately authorizes it.

Before editing, verify the dirty worktree and preserve every existing Stage 1 change plus the untracked user analysis. Do not load `/Users/mtrusov/work/.task-run/tmp/agent-output.md`; the dedicated analysis file is the approved evidence source. State assumptions and the narrow verification plan, then work test-first one behavior at a time.
```

## Current State

- The architectural direction and staged roadmap are recorded in
  `docs/direction.md`.
- Stage 1 implementation exists in the dirty worktree and its 21 local tests
  pass.
- A senior review found three P1 and three P2 contract gaps. The detailed
  findings, evidence, severities, and required corrections are in
  `docs/stage-2-plan.md`.
- The most important defect is that `decide_closure()` currently accepts
  verification copied from the worker result as if it were independent
  controller evidence.
- The worker adapter owns timeout cleanup, but interruption and exceptional exit
  paths can still leave a worker alive and state marked running.
- Runtime run-policy validation is materially weaker than the JSON schema.
- Stage 2 has not been implemented. No task-manifest schema, initializer,
  dependency selector, controller ledger, one-task dispatch, or closure-packet
  writer exists yet.
- `SKILL.md`, the current evaluations, and the worker-result schema remain
  intentionally unchanged.
- No live worker, networked check, dependency install, SDK spike, commit, or
  full-repository suite was run in this review session.

## Decisions

- Stage 1 is a useful foundation but is not a closed safety gate; preserve its
  historical handoff and close the reviewed gaps before Stage 2 dispatch.
- Stage 2 stops at `awaiting_inspection`. Acceptance, independent verification
  execution, resume/recovery policy, tracker mutation, commits, and the next task
  remain Stage 3.
- Keep worker verification under `worker_claims`. Missing controller-owned
  verification evidence must deny future acceptance.
- Keep the task manifest explicit JSON. Do not normalize arbitrary Markdown or
  infer confirmation, task scope, dependencies, or completion.
- Version 1 manifest paths are exact repository-relative files; do not invent
  glob or directory-prefix semantics.
- Require the Stage 2 run directory to live outside the repository to avoid
  self-contaminating Git evidence.
- Use the existing corrected Codex CLI transport. Tests use strict local fakes;
  no real model call is authorized.
- Preserve the single-worktree, single-active-attempt design. Parallelism is
  still deferred.

## Files And Artifacts

- `skills/task-orchestrator/docs/stage-2-plan.md` — created in this session;
  contains the Stage 1 review, Stage 2 contracts, data layout, execution order,
  risk-to-evidence matrix, verification, stop conditions, and exit criteria.
- `skills/task-orchestrator/docs/session-handoff.md` — updated in this session;
  this continuation packet.
- `skills/task-orchestrator/docs/stage-1-handoff.md` — existing staged Stage 1
  record; preserved as historical evidence, but its completion claim is
  qualified by the new review.
- `skills/task-orchestrator/docs/controller-contract.md` — existing staged Stage
  1 authority/state/closure contract.
- `skills/task-orchestrator/assets/run-policy.schema.json` — existing staged
  policy schema; runtime validation does not yet match it.
- `skills/task-orchestrator/scripts/controller.py` — existing staged Stage 1
  primitives; contains the verification-trust and closure-binding findings.
- `skills/task-orchestrator/scripts/codex_worker.py` — existing staged changes;
  safe CLI/timeout work is present, interruption and full-result validation are
  not.
- `skills/task-orchestrator/tests/test_controller.py` and
  `tests/test_codex_worker.py` — existing staged Stage 1 tests; 21 pass.
- `skills/task-orchestrator/agent-output.analysis.md` — user-provided untracked
  prior-run analysis; preserve it.
- `/Users/mtrusov/work/.task-run/tmp/agent-output.md` — intentionally not read.

## Commands And Verification

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'` — passed, 21 tests in 4.145 seconds.
- Focused diagnostic against `decide_closure()` — returned
  `worker_claim_only_accepted=True` and accepted a closure object that omitted
  `accepted` from its allowed transitions.
- Focused diagnostic against `result_status()` — returned `complete` for a
  schema-invalid result with malformed nested values.
- `git status --short --branch` — confirmed existing staged Stage 1 files, the
  preserved untracked analysis, and the new untracked Stage 2 plan.
- A bytecode cache created by one diagnostic was removed; subsequent Python
  diagnostics used `PYTHONDONTWRITEBYTECODE=1`.
- Not run: live Codex execution, network, dependency install, SDK spike,
  parse-only current CLI check, full-repository tests, or commits.

## Open Threads

- Stage 1 P1: independent verification evidence is absent from the closure-gate
  API. This is the first implementation blocker.
- Stage 1 P1: runtime policy validation does not enforce the schema. This is the
  other first implementation blocker.
- Stage 1 P1: interruption/exception cleanup does not always terminate and reap
  the worker group or persist terminal state. Close before Stage 2 dispatch.
- Stage 1 P2: resume accepts non-resumable states. Fix if the change stays small;
  otherwise carry it explicitly as the first Stage 3 prerequisite.
- Stage 1 P2: worker-result validation is shallow. Close before treating a
  result as complete in a Stage 2 closure packet.
- Stage 1 P2: acceptance is bound only to a boolean, not run/task/attempt and
  evidence digests. Tighten the pure boundary now; the mutating acceptance action
  remains Stage 3.
- Stage 3 must choose and implement independent verification execution semantics
  before acceptance. Stage 2 records `controller_verification: not_collected`.

## Next Actions

1. Re-read `docs/stage-2-plan.md` and verify the current dirty worktree.
2. Add one failing test for strict nested run-policy validation; make it pass.
3. Add one failing test showing worker-claimed verification cannot satisfy the
   closure gate without controller evidence; make it pass.
4. Add the interruption and full result-contract regressions, then make the
   worker adapter fail closed.
5. Proceed through manifest validation, atomic initialization, deterministic
   selection, one fake dispatch, ledger persistence, and closure-packet evidence
   in the plan's order.
6. Run the verification progression and create `docs/stage-2-handoff.md`.

## Guardrails For The Next Agent

- Preserve all existing staged and untracked changes; do not reset or clean the
  worktree.
- Do not load the full 3,829-line prior-run transcript without specific user
  approval.
- Do not treat passing Stage 1 tests as proof that the reviewed contracts hold.
- Do not use worker self-report as independent verification evidence.
- Do not use `--dangerously-bypass-approvals-and-sandbox` or broaden permissions
  as compatibility recovery.
- Do not let workers commit, update the controller ledger, select another task,
  or edit installed/cached skill copies.
- Do not add acceptance, resume, tracker, commit, second-task, skill-rewrite,
  parallelism, SDK/MCP, live-model, network, or dependency behavior during Stage
  2.
- Run one targeted verification command at a time and leave no bytecode or test
  artifacts in the repository.
