# Task Orchestrator: Stage 1 Handoff

Status: Stage 1 complete pending user review
Date: 2026-07-15

## Outcome

Stage 1 now has an executable local safety contract. It does not implement or run
a task queue, rewrite `SKILL.md`, commit changes, or invoke a live Codex worker.

The controller primitives define immutable policy persistence, authority-safe
prompt rendering, explicit task transitions, required attempt identity, immutable
attempt allocation, independent Git status evidence, dirty-file preservation,
and a read-only closure decision. The worker adapter preflights safe CLI syntax,
records the effective envelope, owns timeout termination and reaping, rejects
active-process resume, preserves turn artifacts, and separates attempt outcome
from task acceptance state.

## Files

- `docs/controller-contract.md` — authority, ownership, lifecycle, records,
  transport, and closure contract.
- `assets/run-policy.schema.json` — version 1 persisted policy schema.
- `scripts/controller.py` — small Stage 1 policy, prompt, transition, attempt,
  Git-evidence, and closure primitives.
- `scripts/codex_worker.py` — corrected and hardened CLI transport.
- `tests/test_controller.py` — policy/state/closure and durable-evidence tests.
- `tests/test_codex_worker.py` — safe invocation, lifecycle, recovery, and result
  tests.
- `docs/transport-decision.md` — corrected CLI selected; SDK spike deferred.
- `docs/stage-1-handoff.md` — this continuation record.

`SKILL.md`, `assets/worker-result.schema.json`, and the user-provided
`agent-output.analysis.md` were not changed.

## Failure-first evidence

Before controller implementation, all seven initial controller tests failed
because the module and enforcement were absent. Against the unchanged adapter,
the transport tests exposed the invalid flag position, missing capability
preflight, worker `complete` being treated as success, missing timeout ownership,
active-PID resume, and missing outcome separation. Later focused tests also
demonstrated that unauthorized `danger-full-access`, acceptance without a closure
decision, dirty-file replacement, and generic rather than resume-specific
preflight were rejected only after their corresponding enforcement was added.

The local subprocess timeout test uses process signals and bounded polling rather
than an arbitrary sleep as its oracle.

## Verification

The narrow modules pass independently:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_codex_worker.py
```

Final local results:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s skills/task-orchestrator/tests -p 'test_*.py'
21 tests passed

codex --version
codex-cli 0.144.4

codex --ask-for-approval never exec --sandbox workspace-write --help
exit 0

codex --ask-for-approval never exec resume \
  -c 'sandbox_mode="workspace-write"' --help
exit 0
```

Both JSON schemas parse with Python's standard library. `git diff --check`
passes, and verification created no bytecode artifacts. No full-repository suite
is needed because no shared tooling changed.

## Remaining gaps and deferrals

- No run initializer or task-manifest reader exists; those begin Stage 2.
- The closure primitive consumes caller-supplied task identity and allowed paths;
  Stage 2 must source them from the persisted selected task rather than general
  supervisor input.
- The adapter deliberately rejects `danger-full-access`; a future controller may
  pass it only from an exact persisted authorization, but no such need was shown.
- No live worker smoke test was run. The parse surface and local lifecycle are
  proven, while real model/session behavior remains an authorized pilot check.
- Semantic diff judgment, tracker mutation, controller-owned commits, and
  supervisor restriction remain in their later planned stages.

## First Stage 2 action

Add a run initializer that exclusively persists a validated run policy and a
confirmed machine-readable task manifest, creates the controller ledger in
`initialized`, and records the initial Git baseline before selecting exactly one
dependency-ready task. Keep arbitrary Markdown normalization deferred rather than
silently choosing an input format.
