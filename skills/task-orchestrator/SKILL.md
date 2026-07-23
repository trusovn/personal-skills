---
name: task-orchestrator
description: Operate and reason about the task-orchestrator's controller-backed local run flow for an approved task manifest. Use when the user wants to initialize, run, inspect, diagnose, or modify a sequential Codex-worker run; retrieve the current controller contract or module owner; or assess recovery and future MVP work. Do not use it to invent product requirements or imply that the unfinished automatic acceptance, recovery, plan-preparation, or advance flow already exists.
compatibility: Requires Python 3, Git, repository access, and a Codex CLI compatible with the bundled internal adapter.
---

# Task Orchestrator

Use the deterministic controller as the public operating surface. Treat
`scripts/codex_worker.py` as an internal transport adapter; do not invoke it
directly to operate or recover a controller-owned run.

Freshness: 2026-07-23. The current public commands are `init`, `run-next`, and
`inspect`.

## Read the smallest current reference

- Start with the [current-information index](references/index.md).
- Read the [operator guide](references/operator-guide.md) to initialize or
  inspect a run.
- Read the [architecture map](references/architecture-map.md) before changing
  implementation behavior or selecting tests.
- Read the [controller contract](docs/controller-contract.md) for persisted
  authority, state, and ownership rules.
- Read the [Stage 3 MVP rebaseline](docs/stage-3-mvp-rebaseline.md) and its
  [retrieval-surface follow-up](docs/stage-3-retrieval-surface-follow-up.md)
  when planning unfinished work.

Do not search or load `docs/history/` during ordinary operation or planning.
Use it only when a current reference explicitly requires historical evidence.

## Respect authority

Use this order when sources appear to conflict:

1. persisted run policy, manifest, ledger, and controller records for one run;
2. current schemas and the controller contract;
3. current operator and architecture references;
4. the governing current MVP plan for unfinished behavior; and
5. historical documents only as non-authoritative implementation evidence.

Workers and reviewers do not create authority, mutate the controller ledger,
select another task, broaden permissions, or commit.

## Confirm inputs before initialization

Require an approved, normalized manifest and an explicit run policy. Current
code does not yet convert a planning document into these inputs.

Confirm:

- the Git repository and authorized task IDs;
- task dependencies, brief paths, and exact allowed paths;
- targeted verification and any repository gate;
- sandbox, writable roots, network, and dependency-install policy;
- stop or escalation behavior; and
- commit mode: `off` or `controller_exact_paths`.

The worker never commits under either mode. The current public flow does not
yet complete controller-owned exact-path finalization, so prefer `off` unless a
separate current contract explicitly authorizes and exposes that path.

Use the [minimal run policy](assets/examples/minimal-run-policy.json) and
[minimal task manifest](assets/examples/minimal-task-manifest.json) as starting
points. The schemas remain authoritative:
[run policy](assets/run-policy.schema.json),
[task manifest](assets/task-manifest.schema.json), and
[worker result](assets/worker-result.schema.json).

## Operate through the controller

Initialize an immutable run directory outside the repository:

```bash
python3 <skill-dir>/scripts/controller.py init \
  --run-dir <external-run-dir> \
  --policy <run-policy.json> \
  --manifest <task-manifest.json> \
  --repository <repository>
```

Select and launch exactly one dependency-ready task:

```bash
python3 <skill-dir>/scripts/controller.py run-next \
  --run-dir <external-run-dir> \
  --timeout-seconds <seconds>
```

Inspect a completed worker attempt and run controller-owned verification:

```bash
python3 <skill-dir>/scripts/controller.py inspect \
  --run-dir <external-run-dir> \
  --timeout-seconds <seconds>
```

Before every mutating command, inspect the repository and run records for
pre-existing or unexpected changes. Keep the run sequential in one working
tree. Do not launch another worker over a live or ambiguous attempt.

## Interpret current outcomes truthfully

Read structured controller records and task-scoped diffs before raw event logs.
Open worker JSONL or stderr only to diagnose missing or contradictory structured
evidence.

An accepting current inspection decision means the task is mechanically
eligible under the configured command-verification policy. It does not yet
mean semantic review, atomic task acceptance, dependency release, or automatic
advance occurred.

Current public commands do not yet provide:

- safe stop and same-thread recovery;
- semantic review and correction loops;
- atomic acceptance, dependency release, and advance;
- plan-to-manifest preparation; or
- an unattended end-to-end runner.

If one of these is required, report the current state and route the work to the
corresponding MVP increment. Do not bypass the controller by calling the
transport adapter directly.

## Make only bounded judgments

Resolve a worker question without the user only when the answer is directly
entailed by explicit authority, local and reversible, and does not change a
public contract, architecture, persistence meaning, security posture,
user-visible rule, cost, scope, or permission envelope.

Otherwise stop with the options, relevant authority, impact, and a
recommendation. Never ask a worker to invent the missing decision.

## Report

State:

- the run, task, attempt, and current controller state;
- commands run and durable evidence paths;
- mechanical verification and semantic-review status separately;
- unexpected changes, unanswered questions, and skipped checks;
- the next command that currently exists, or the MVP gap preventing it; and
- whether the operator must decide anything.

## Avoid

- invoking `codex_worker.py` as the public run interface;
- treating `docs/history/` as current authority;
- claiming inspection completed semantic acceptance;
- relaunching over a live or ambiguous process;
- modifying the ledger or workflow from a worker session;
- inventing commit, network, dependency, or destructive permissions; and
- combining tasks or reading all briefs and transcripts into one context.
