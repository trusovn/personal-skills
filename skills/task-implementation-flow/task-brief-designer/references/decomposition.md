# Decomposition package

Read after choosing a split, before writing any parent, child or structural index.
Apply the entry sizing gate first. The original clause numbers below preserve
links to the sizing contract; its estimate, boundary and no-split rules stay inline.

4. The original task becomes a `composite` parent with status `decomposed`.
   It is a coordination/coverage contract and is never a launch target for
   `bounded-task-implementer`. Give child IDs stable numeric suffixes such as
   `TASK-017.1`, `TASK-017.2`, and nested suffixes only when recursive
   decomposition is actually needed.
5. Give every child the same executable-brief contract as an ordinary task:
   authority, applicable direction decisions, bounded scope, consumes/produces
   relationships, interfaces/invariants, acceptance criteria, verification,
   stops, launch metadata, and sizing evidence. Preserve relevant stable
   project-plan IDs rather than inventing child-local replacements for flows,
   artifacts, interfaces, or invariants.
6. Re-estimate every child independently and recursively apply the active sizing
   profile. Only leaf tasks may be handed to implementation. A decomposition is
   not successful merely because the parent was renamed: it must reduce the
   triggering work and leave each leaf within the active envelope, unless the
   permitted no-split override in the entry sizing contract applies.
7. If a parent-level acceptance criterion can only be proven after sibling work
   composes, create a final executable integration child that owns that proof
   and any required wiring. Do not invent a special composite-parent
   implementation or acceptance-review stage.
9. Before writing the decomposition package, verify:
   - children collectively cover the parent outcome and every parent AC;
   - no approved requirement, invariant, interface, or contract impact
     disappeared during splitting;
   - every produced shared artifact/state/interface has one clear owning child;
   - dependencies are acyclic and do not require a child to consume unavailable
     work; and
   - each leaf fits the active profile or carries the permitted explicit
     override.
10. For a multi-brief decomposition, use the artifact layout's composite/child
    paths and create or update its structural `docs/tasks/index.json` unless
    repository authority declares an equivalent index. This index describes
    task structure only; do not mutate `docs/task-map.json`,
    `docs/project-plan.md`, review history, or runtime orchestration state.


## Composite parent

```markdown
# Task Brief: `<TASK-ID>` — `<concrete result delivered by the child set>`

## Outcome

<Original testable outcome, its user or next consumer, and why it is needed.>

## Child outcomes and sequence

<Explain how the pieces build on each other in ordinary language. State the
substantive boundary reason once; keep exact ownership and dependencies below.>

| Child | Outcome / owned output | Depends on | Brief |
|---|---|---|---|
| <TASK-ID.1> | <independently verifiable result and its consumer> | <IDs or none> | <path> |

## Authority and scope

- Authority: <exact approved sources and necessary baseline identity>
- Parent plan task / stable refs: <task, FLOW/ART/IF/INV refs>
- Original scope: <bounded work preserved across children>
- Out of scope: <exclusions that affect execution>
- Governing decisions: <applicable direction decisions and exact references>

## Coverage and closure

- Parent requirement / AC coverage: <every parent requirement or AC -> owning children>
- Shared artifacts/interfaces/invariants: <one owning child for each shared surface>
- Integration closure: <final executable integration child, or why child-local proof suffices>
- Leaf sizing: <all leaves fit the policy, or references to exact permitted overrides>

## Execution and handoff

Status: `decomposed`
Task kind: `composite`

This parent coordinates the work. Implement dependency-ready executable leaves;
the parent itself is not an implementation target. Completion requires every
mapped leaf, including integration closure, to finish its implementation and
required review route.

### Execution sizing

- Sizing policy: <active-profile>@<config-version>
- Original estimate: <integer agent calls>; <integer implementation minutes>
- Original required execution profile: <agent_tier>/<reasoning>
- Estimate confidence: <low | medium | high>
- Triggered decomposition rules: <configured rule names>
```

A composite has no launch metadata or readiness route. Preserve approved
direction in the parent and each affected child. Apply the same concise content
boundary to the parent and every child: titled ACs, optional informative risks,
and detailed proof in each owning leaf verification design.

