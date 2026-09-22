# Task implementation artifact layout

This document defines the durable repository locations used by
`task-implementation-flow`. Every durable task uses one dedicated task package
directory. Repository or user authority may declare a different package root
or directory naming convention, but it must preserve that one-directory-per-task
structure and the fixed artifact names below.

## Planning authority remains separate

The lightweight project-planning flow owns:

```text
docs/project-plan.md
docs/task-map.json
docs/project-plan-review.md
```

`docs/project-plan.md` and `docs/task-map.json` describe the intended
coordinated system. `docs/project-plan-review.md` is separate review evidence.
Task decomposition must not rewrite any of these merely because one plan task is
too large for one implementation agent.

## Default task package

When no repository-specific task location exists, use:

```text
docs/tasks/
  index.json
  TASK-017/
    brief.md
    verification.md
    preflight.md
    reviews/
      maintainability-01.md
      acceptance-01.md
  TASK-017.1/
    brief.md
    reviews/
      acceptance-01.md
  TASK-017.2/
    brief.md
```

Only create `verification.md` when a separate `task-verification-designer`
pass is actually used. Do not create an empty placeholder when verification
design stays inline.

Only create `preflight.md` when standalone/high-assurance preflight actually
produces a durable artifact. Guided review remains conversational unless the
user, repository, or high-assurance route requires a report.

High-assurance freshness does not require these canonical files to be ignored
or Git-status-neutral. The producing stage records exact status before and
after its write, attributes only the new or modified artifact, and confirms
that every non-artifact path and content identity is unchanged. A later stage
matches the recorded post-write state before acting.

When a review is durable, keep it separate from the brief. Use numbered
immutable review names such as `maintainability-01.md`,
`maintainability-02.md`, `acceptance-01.md`, and `acceptance-02.md`.
Corrections make prior verdicts stale; do not overwrite or append acceptance to
the task brief or project plan.

## Structural task index

`docs/tasks/index.json` is a discovery/decomposition index, not a runtime
ledger and not a replacement for `docs/task-map.json`. It should contain only
stable task structure and artifact locations. The brief designer owns creating
or updating the entries it designs.

Minimal shape:

```json
{
  "version": 1,
  "tasks": {
    "TASK-017": {
      "kind": "composite",
      "source_plan_task": "TASK-017",
      "brief": "docs/tasks/TASK-017/brief.md",
      "parent": null,
      "children": ["TASK-017.1", "TASK-017.2"],
      "depends_on": []
    },
    "TASK-017.1": {
      "kind": "executable",
      "source_plan_task": "TASK-017",
      "brief": "docs/tasks/TASK-017.1/brief.md",
      "parent": "TASK-017",
      "children": [],
      "depends_on": []
    },
    "TASK-017.2": {
      "kind": "executable",
      "source_plan_task": "TASK-017",
      "brief": "docs/tasks/TASK-017.2/brief.md",
      "parent": "TASK-017",
      "children": [],
      "depends_on": ["TASK-017.1"]
    }
  }
}
```

Do not put attempt status, controller state, worker ownership, timestamps, or
review verdicts in this index. Those belong to the active orchestrator/controller
or the review artifacts themselves.

Do not create or consume direct task briefs at
`docs/tasks/<TASK-ID>.md`. Normalize every durable task to a package at
`docs/tasks/<TASK-ID>/brief.md`. A surgical gap-check does not require creating
the index unless the repository already uses it. When one task is decomposed
into multiple durable briefs and no equivalent repository index exists, create
this index so agents have one predictable discovery point.

## Task identity and decomposition

Use the plan task ID for the original task. A split original becomes a
`composite` parent with status `decomposed`. Child IDs use numeric suffixes:

```text
TASK-017
TASK-017.1
TASK-017.2
TASK-017.2.1
```

Nested suffixes are reserved for genuine recursive decomposition.

Composite parents are never implementation launch targets. Every executable
leaf has its own complete brief. If sibling work must be wired together or a
parent-level criterion can only be proven after composition, create a final
executable integration child and make its dependencies explicit. This keeps the
ordinary implementation and acceptance-review contracts intact instead of
inventing a special parent implementation/review stage.

## Ownership summary

- `project-delivery-plan`: owns `docs/project-plan.md` and
  `docs/task-map.json`.
- `project-plan-verification`: owns `docs/project-plan-review.md`.
- `task-brief-designer`: owns task brief design, decomposition, and structural
  `docs/tasks/index.json` entries it creates.
- `task-verification-designer`: owns a durable `verification.md` in the
  executable task package only when the optional stage is used.
- `task-preflight`: owns a durable `preflight.md` only when its invocation
  requires one.
- semantic reviewers: own separate numbered review artifacts only when a durable
  report is required.
- runtime orchestration: owns execution state elsewhere; workers/reviewers do
  not mutate the structural index as a status tracker.
