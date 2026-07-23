# Codex behavioral eval runner: possible future work

This document records ideas intentionally excluded from
`SC-EVAL-01`. It is not implementation authority and does not expand the MVP
brief.

The MVP succeeds when agents developing `task-implementation-flow` skills have
one discoverable command that stages portable fixtures and launches selected
evals against Codex with inspectable outputs.

## Consider after the MVP is used

### 1. Migrate the remaining task-implementation-flow evals

Add structured `execution` metadata to:

- `bounded-task-implementer`;
- `task-preflight`; and
- `task-acceptance-review`.

Do this incrementally when each skill is next developed. Avoid a bulk rewrite
until the pilot schema has survived real use.

### 2. Connect runs to grading and the existing viewer

Translate runner results into the workspace layout consumed by the existing
grader, benchmark aggregator, and eval viewer. Prefer deterministic checks for
files and structured output, with a fresh semantic grader only where prose
expectations require judgment.

Do not allow an executor's successful exit or self-claim to become a passing
grade.

### 3. Add resumability and selective reruns

Persist a suite manifest that can skip completed eval/configuration pairs and
rerun only failures. Add this when interrupted suites remain a recurring
problem after the runner reduces agent-level tool calls.

### 4. Add repetitions and variance reporting

Support multiple runs per configuration and feed their results into
`aggregate_benchmark.py`. Keep a single run as the cheap default; repetitions
are useful only when stochastic variance affects a decision.

### 5. Capture richer diagnostics on demand

Optional diagnostics could include:

- Codex JSONL events or a fuller transcript;
- duration and token usage;
- exact skill/source digests;
- generated patch files; and
- detailed fixture and CLI environment metadata.

Do not make these mandatory until a concrete debugging, comparison, or
freshness use case needs them.

### 6. Add an eval doctor

A read-only check could flag:

- setup commands embedded in user prompts;
- absolute `/work` assumptions;
- unknown placeholders or escaping workspaces;
- unavailable commands;
- missing declared outputs; and
- expectations that cannot be inspected from preserved artifacts.

Prompt-answer leakage and assertion quality still require judgment; treat any
heuristic warning as review guidance, not a failure verdict.

### 7. Add controlled concurrency

Parallel execution may reduce wall-clock time for independent evals, but it
also complicates approval, logs, resource use, and fixture isolation. Add it
only after sequential execution is stable.

### 8. Consider provider adapters

If the same behavioral workflow is needed for another agent runtime, extract a
small executor boundary after the second real provider exists. Do not design a
provider framework in advance.

### 9. Promote the runner to repository-level tooling if ownership changes

Keep the MVP under `skills/skill-creator/scripts/`. If the command later serves
CI or non-skill workflows, consider moving testable CLI code to a repository
`tools/skill-eval/` package while leaving `skill-creator` as a consumer.

## Explicitly not a goal

The runner should not become an autonomous acceptance system. Skill behavior
can be subjective, fixtures can be incomplete, and model graders can ratify
the same misunderstanding as the executor. The durable division should remain:

- the runner executes and preserves evidence;
- deterministic checks establish objective facts;
- graders assess declared expectations; and
- a human or fresh acceptance reviewer owns consequential release decisions.
