---
name: task-orchestrator
description: Use only for explicit task-orchestration requests or named task-orchestrator invocation. Operate, inspect, diagnose or modify its controller-backed local run flow for approved manifests; initialize runs, retrieve controller contracts/module owners, assess recovery or planned local harness work. Excludes generic run/implement/finish-task requests and inventing product requirements. Do not imply unfinished automatic acceptance, recovery, plan-preparation or advance flows exist.
compatibility: Requires Python 3, Git, repository access, and a Codex CLI compatible with the bundled internal adapter.
---

# Task Orchestrator

Use the deterministic controller as the public operating surface. Treat
`scripts/codex_worker.py` as an internal transport adapter; do not invoke it
directly to operate or recover a controller-owned run.

Freshness: 2026-11-12. Current commands are `init`, `status`, `reserve`,
`launch`, `observe`, `stop`, `intervene`, `revise-inputs`, `inspect-candidate`,
`check-candidate`, and `check-collection`. Legacy `inspect`
and `revise-flow` retain mechanical primitives; `run-next` reports pending work.

## Read the smallest current reference

- Start with the [current-information index](references/index.md).
- Read the [operator guide](references/operator-guide.md) to initialize or
  inspect a run.
- Read the [architecture map](references/architecture-map.md) before changing
  implementation behavior or selecting tests.
- Read the [current development documents](docs/README.md) when planning
  unfinished work. The confirmed local harness direction governs the proposed
  plan and its accepted review; implemented interfaces remain distinct from plans.

## Respect authority

Use this order when sources appear to conflict:

1. persisted run policy, manifest, ledger, and controller records for one run;
2. current schemas and executable validation for supported behavior;
3. current operator and architecture references; and
4. the owner-confirmed direction and proposed plan for unfinished behavior.

System and repository instructions bound every source. Plans do not make a
capability available or override the owner-confirmed direction.

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

Reserve the permitted preflight using the version returned by status. Save the
returned assignment object to a file, then launch and observe it:

```bash
python3 <skill-dir>/scripts/controller.py status --run-dir <external-run-dir>
python3 <skill-dir>/scripts/controller.py reserve --run-dir <external-run-dir> --expected-version <version> --task-id <task> --stage preflight --role preflight --operation-key <key>
python3 <skill-dir>/scripts/controller.py launch --run-dir <external-run-dir> --request <assignment.json> --timeout-seconds 300
python3 <skill-dir>/scripts/controller.py observe --run-dir <external-run-dir> --operation-id <operation-NNN>
```

A complete, observed current preflight permits the first implementation
reservation. Inspect terminal implementation/correction with `inspect-candidate`,
reserve `verify`, and execute its exact assignment with `check-candidate`.
Reserve and launch `semantic_review` for fresh independent collection; that
collector calls `check-collection` with its exact assignment to rerun the frozen
checks. Terminal collection is admitted only for the current candidate and observed
independent session, with explicit coverage, gaps and findings. A real failed check
authorizes a correction within the shared three-cycle budget. Complete collection
enables a separate acceptance assignment; acceptance output remains a raw claim.
See the [T-004 contract](docs/tasks/T-004/controller-contract.md) for payloads
and limits. Follow the operator guide for stop, revision and active-chat intervention. The legacy
`scripts/controller.py run-next` command does not launch this flow;
`scripts/controller.py inspect` does not admit these actor outcomes.

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

- automatic recovery or same-thread continuation;
- semantic acceptance admission or review-driven correction decisions;
- atomic acceptance, dependency release, and advance;
- plan-to-manifest preparation; or
- an unattended end-to-end runner.

If one of these is required, report the current state and route the work to the
proposed local harness plan. Do not bypass the controller by calling the
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
- the next command that currently exists, or the missing capability preventing it; and
- whether the operator must decide anything.

## Avoid

- invoking `codex_worker.py` as the public run interface;
- claiming inspection completed semantic acceptance;
- relaunching over a live or ambiguous process;
- modifying the ledger or workflow from a worker session;
- inventing commit, network, dependency, or destructive permissions; and
- combining tasks or reading all briefs and transcripts into one context.


<!-- contract-registry-flow:task-orchestrator:begin -->
## Contract-registry stage when enabled

When the repository uses machine-readable implemented-contract discovery, place `task-contract-registry-updater` after deterministic architecture/maintainability checks and before `task-acceptance-review`. Do not ask the bounded implementation agent to perform this synchronization in the same attention-heavy implementation pass.

A reference-only acceptance correction returns directly to the registry updater and then fresh acceptance when production/test/executable-contract bytes did not change.
<!-- contract-registry-flow:task-orchestrator:end -->
