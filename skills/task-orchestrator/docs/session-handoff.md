# Session Handoff

This file is a durable companion to the copy/paste handoff. The copy/paste packet is still the primary resume context.

Generated: 2026-07-15 23:07 WEST

Workspace: `/Users/mtrusov/work/skill-sources/personal-skills`

Branch: `main`

Primary goal: redesign `skills/task-orchestrator` so unattended task execution is enforced by a deterministic controller rather than prolonged supervisor-model reasoning.

Latest user request: preserve the agreed direction and prepare an execution-ready Stage 1 for a fresh session.

## Resume Prompt

Paste this into the next session:

```text
You are continuing the task-orchestrator redesign in `/Users/mtrusov/work/skill-sources/personal-skills`.

Start by reading:
1. `skills/task-orchestrator/docs/direction.md`
2. `skills/task-orchestrator/docs/stage-1-plan.md`
3. `skills/task-orchestrator/docs/session-handoff.md`
4. `skills/task-orchestrator/agent-output.analysis.md`
5. the current `SKILL.md`, wrapper, schema, and tests referenced by the Stage 1 plan.

Treat the direction document as the agreed architecture and execute only Stage 1. Do not rewrite `SKILL.md`, build the full task queue, commit, install dependencies, use the network, or launch a live/paid Codex worker unless the user separately authorizes it. Do not load `/Users/mtrusov/work/.task-run/tmp/agent-output.md`; the user intentionally commissioned the analysis file to avoid spending context on the 3,829-line transcript.

Before editing, verify the worktree and state your assumptions and the narrow verification plan. Implement failure-first tests and the minimum contract/transport enforcement needed to satisfy Stage 1. Preserve the user's untracked analysis file and unrelated work.
```

## Current State

- The current task-orchestrator skill is unchanged.
- The worktree has no tracked modifications; the user analysis and the three new planning documents are untracked.
- The user accepted the recommendation to move toward a deterministic controller with a thin skill and optional bounded Qwen judgment.
- The destination architecture and staged roadmap are recorded in `direction.md`.
- Stage 1 is specified in `stage-1-plan.md`; it has not been implemented.
- The full prior-run transcript was not loaded. Transcript-specific findings come from `agent-output.analysis.md`.
- No model worker, networked check, SDK install, or full-repository test was run.

## Decisions

- Do not treat this as a wording-only skill revision. Safety-critical policy and state move into code.
- Workers never commit. Any authorized commit is controller-owned and exact-path.
- The worker result is a claim; independent closure evidence gates acceptance.
- The inexpensive supervisor becomes optional and bounded rather than the control-plane authority.
- Start with the corrected CLI transport unless Stage 1 proves a concrete need for an SDK spike.
- Keep transport choice separate from controller policy/state.
- Keep Stage 1 narrow: contract, failure tests, transport lifecycle, and transport decision; no queue execution or skill rewrite.

## Files And Artifacts

- `skills/task-orchestrator/docs/direction.md` — created; agreed target architecture, invariants, stages, and deferred decisions.
- `skills/task-orchestrator/docs/stage-1-plan.md` — created; execution-ready Stage 1 scope, risk-to-evidence matrix, verification, stop conditions, and exit criteria.
- `skills/task-orchestrator/docs/session-handoff.md` — created; this continuation packet.
- `skills/task-orchestrator/agent-output.analysis.md` — user-provided, untracked analysis; preserve it.
- `skills/task-orchestrator/SKILL.md` — read only; prompt-level policy currently exceeds wrapper enforcement.
- `skills/task-orchestrator/scripts/codex_worker.py` — read only; current subprocess transport.
- `skills/task-orchestrator/tests/test_codex_worker.py` — read only; four permissive fake-CLI tests.
- `skills/task-orchestrator/assets/worker-result.schema.json` — read only; worker self-report schema.
- `/Users/mtrusov/work/.task-run/tmp/agent-output.md` — intentionally not read.

## Commands And Verification

- `python3 -m unittest skills/task-orchestrator/tests/test_codex_worker.py` — four existing tests passed. The generated `__pycache__` was removed afterward.
- `codex --version` — `codex-cli 0.144.4` in this session.
- `codex exec --ask-for-approval never --help` — exit 2; the flag is invalid after the `exec` subcommand.
- `codex --ask-for-approval never exec --help` — exit 0; global flag position accepted.
- `codex exec -c 'approval_policy="never"' --help` — exit 0; scoped config override accepted.
- Official Codex manual fetched on 2026-07-15; it documents workspace-write with approval-never, the Codex SDK, and Codex-as-MCP.
- Not run: live Codex execution, timeout integration test, full repository suite, SDK spike, skill evals.

## Open Threads

- The exact controller data shapes and state names are intentionally left for Stage 1 contract work.
- Semantic diff-review ownership remains deferred: Qwen, separate read-only Codex, or human by risk tier.
- Qwen cannot be a hard security boundary while it retains unrestricted shell/write tools; typed tools or command restriction are a later design decision.
- CLI remains the provisional transport. SDK adoption requires a demonstrated lifecycle or compatibility advantage.
- Arbitrary Markdown task-list normalization is deferred until controller contracts are stable.

## Next Actions

1. Verify `git status --short` and read the three continuation documents.
2. Re-run the baseline test command from `stage-1-plan.md` with bytecode generation disabled.
3. Write the controller contract and P0 failure-first tests before production changes.
4. Make each P0 scenario pass with the minimum policy/state and transport changes.
5. Record the transport decision and hand off Stage 2.

## Guardrails For The Next Agent

- Do not load the full prior-run transcript without specific user approval.
- Do not use `--dangerously-bypass-approvals-and-sandbox` as compatibility recovery.
- Do not let workers commit or update the controller ledger.
- Do not edit installed or cached skill copies.
- Do not rewrite `SKILL.md` during Stage 1.
- Do not install dependencies, use the network, launch a paid/live worker, or commit without explicit authorization.
- Do not touch unrelated files or remove the user's untracked analysis.
- Keep failed-attempt evidence; never delete it to make a retry look clean.
