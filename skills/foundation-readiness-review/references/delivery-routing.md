# Delivery Routing After Foundation

Choose the **cheapest route that adequately controls risk**.
## PERSONAL_FLOW — default

Use the personal task flow when most are true:

- the high-level goal is stable enough to derive bounded tasks
- one or two modules own most changes
- existing interfaces/architecture constrain the solution
- no major schema/API/UI contract must be jointly designed
- a task can be expressed with explicit scope, acceptance, and verification
- hidden-test risk is primarily implementation/edge-case risk
- time/token pressure is high

Recommended flow:

```text
task-brief-designer
  -> task-preflight when needed
  -> bounded-task-implementer
  -> architecture gate + task-maintainability-review when repo policy requires it
  -> task-acceptance-review when task risk/metadata requires functional acceptance
```

The maintainability stage is orthogonal to SDD depth. If the repository requires it, keep it in the bounded flow even for otherwise small tasks. It is a focused quality gate, not evidence that the task needs broader specification ceremony.

Use repeated bounded tasks rather than one giant implementation task.

Exact next skill: `task-brief-designer`.
## SDD_QUICK — targeted spec/design protection

Use when at least one is true:

- externally observable behavior has several acceptance conditions that are easy to misread
- a new architectural boundary/interface is required
- AI behavior introduces a nontrivial contract between model output and deterministic code
- feature touches multiple layers and a short design artifact will prevent rework
- you need durable AC-to-implementation traceability for a critical feature

Prefer easy interview depth and quick route. Skip N/A stages.

This is usually the maximum SDD depth justified for a bounded feature.
## SDD_STANDARD — cross-cutting system change

Use when several are true:

- multiple modules/services/surfaces change
- schema + API + workflow behavior must evolve together
- there are competing architectural approaches with meaningful blast radius
- state ownership or persistence semantics are non-obvious
- concurrency/idempotency/recovery semantics matter
- several dependent features/tasks require a shared design
- the project is large enough that rework would cost more than planning

Still skip irrelevant stages.
## SDD_FULL — rare escalation

Use only when the project behaves more like a substantial product than a bounded change:

- many user stories / surfaces
- new persistent domain model plus API plus UI/process flows
- multiple irreversible architecture choices
- safety/security/compliance constraints with traceability requirements
- substantial parallel implementation lanes depend on a shared formal design
- the planning overhead is justified by the expected rework avoided

Do not select `SDD_FULL` merely because:
- the task is hard
- AI is involved
- the repo is unfamiliar
- you want more confidence
- the repo has an architecture/maintainability gate

Hard implementation can still be a bounded task after a good foundation.
## Resolve the recommendation to an available next step

Before finalizing the recommendation, confirm that its entry skill or command is actually available
in the current skill catalog or repository instructions. A document that merely mentions an SDD
stage is not availability evidence.

When `sdd-specify` is available, map the SDD recommendations as follows:
| Recommendation | Exact next skill | Direction to carry into that skill |
|---|---|---|
| `SDD_QUICK` | `sdd-specify` | Prefer easy interview depth and the quick route; skip N/A stages. |
| `SDD_STANDARD` | `sdd-specify` | Preserve the cross-cutting risks that justify standard-depth specification and design. |
| `SDD_FULL` | `sdd-specify` | Preserve the formal traceability and shared-design risks that justify the full route. |

Do not invent an SDD command, stage, or parameter beyond what the available SDD workflow documents.

If `sdd-specify` or another explicitly documented SDD entry point is unavailable:
1. If the work can still be decomposed into safe bounded tasks, change the recommendation to
   `PERSONAL_FLOW` and name `task-brief-designer` as the exact next skill.
2. If that downgrade would discard necessary cross-cutting design or traceability, retain the
   preferred SDD route as unavailable and make the exact next stage `USER_DECISION`: provide/install
   an SDD workflow, or explicitly accept the `PERSONAL_FLOW` fallback. Do not pretend the missing
   route can be executed.
## Route escalation during execution

Start lighter.

Escalate from PERSONAL_FLOW to SDD when preflight discovers:

- unresolved architecture ownership
- contradictory requirements
- a task brief expanding across multiple system boundaries
- repeated implementation rework caused by missing design
- acceptance criteria that cannot be localized to a bounded change

Escalation is allowed mid-project; starting with full ceremony is not required.
