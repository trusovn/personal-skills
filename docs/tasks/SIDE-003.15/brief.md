# Task Brief: SIDE-003.15 — Restructure project-delivery-plan for conditional loading

## Outcome

`skills/project-delivery-plan` loads only the instructions the task at hand
needs. Scenario-conditional material — plan-template details, task-map
contract mechanics — moves into package references where safely separable,
each with an explicit when-to-read condition and timing; the entry file keeps
the planning workflow, scope rules, and a reference loading table. Every
preserved obligation is mapped old→new; behavior is unchanged.

## Authority and scope

| Item | Contract |
|---|---|
| Authority | [SIDE-003 plan](../SIDE-003/plan.md), "Body design and mandatory loading", "Delivery sequence" phase 4 (inspect larger packages), "Measurement and decision rules" layer 2; owner adjustment (2026-11-03): figure the exact split places; clear when-to-read instructions are the acceptance center |
| Dependencies | SIDE-003.1–.6 complete (baseline + this skill's description final) |
| Allowed changes | This package's `SKILL.md` body, its `references/` (`project-plan-template.md`, `task-map-contract.md`, new files), its `evals/` inputs, owning test expectations that assert its text, and this skill's section in `docs/tasks/SIDE-003/rollout-results.md` |
| Read-only context | The SIDE-003.1 baseline and read graph; the package's `evals/evals.json` (trigger/setup reuse); `docs/tasks/index.json` shape (produced, not owned, by this skill family) |
| Out of scope | The `description` frontmatter (compressed in SIDE-003.3 — do not change); any behavior change to plan or task-map policy; renaming or moving the package; other skills; the active `.agents/` installation |
| Assumptions / unresolved | The exact conditional clusters are this leaf's design work; the two references are currently listed without read conditions ("references/project-plan-template.md", "references/task-map-contract.md") — explicit conditions and timing are mandatory here |

## Work and acceptance criteria

Required work:

1. Before any edit, freeze the obligation inventory in the rollout-results
   section: every workflow step, artifact rule, task-map rule, and stop/route
   rule in the current entry file, each with its current authority location.
2. Identify the actual conditional paths (assembling `docs/project-plan.md`
   from the template; populating `docs/task-map.json` against the contract;
   any distinct delta/plan-review cluster). The planning workflow core stays
   inline. Do not invent profiles the skill lacks.
3. Extract qualifying clusters into `references/` files; give every reference —
   new and existing — an explicit read condition and timing in the entry file
   (e.g. read the plan template before assembling the plan document; read the
   task-map contract before populating the map); keep near-universal material
   inline.
4. State the missing-reference rule: a required reference that is missing or
   unreadable stops the affected action with the exact gap reported; no
   inferred bypass. Do not read every reference at startup.
5. Update the owning assertions to assert the applicable instruction closure
   and required route rather than deleted literal text. Preserve distinct
   existing scenarios; extend fixtures only for missing loading-condition
   cases.
6. Record the instruction map (each old obligation → new location, loading
   condition, proving scenario), the per-route measured cost (entry-only and
   cumulative, before/after, from the SIDE-003.1 baseline record's file table
   and route inventories), and any no-op
   decisions with reasons.

- **AC-01:** Every reference this package owns has an explicit when-to-read
  condition and timing in the entry file; a reader following only the entry
  file knows, before each dependent action, whether a reference applies.
- **AC-02:** The instruction map covers every obligation from the pre-edit
  inventory; no workflow, artifact, or task-map obligation is lost or
  weakened; behavior-preservation fixtures pass unchanged before and
  after the edit; only the new loading-structure assertions (reference
  existence, explicit conditions, relocated obligations) reject the pre-edit
  layout and pass after.
- **AC-03:** Entry-only and per-route cumulative costs are recorded
  before/after; a route that did not shrink is explained, not hidden; the
  description frontmatter is unchanged.

## Verification

| Evidence | Scenario and oracle | Command |
|---|---|---|
| Fail-first | Behavior-preservation fixtures pass unchanged against the pre-edit bytes; the new loading-structure assertions (reference existence, explicit conditions, relocated obligations) reject the pre-edit layout; in a disposable candidate, removing one required link or bypassing one route is detected by the relevant check | derived verification owns the concrete fixture/command pair (this package has no local test root) |
| Targeted | Plan/task-map behavior in the package's eval inputs is unchanged; the loading-condition presence check passes per reference | SIDE-003.1 measurement command + eval inputs |
| Owning suite | No package-local test root; owning assertions are discovered from the SIDE-003.1 prerequisites map | per the map |
| Broader gate | Aggregate gate and disposable-install reference resolution at SIDE-003.18; live behavioral qualification only with separately approved budget, else recorded pending | SIDE-003.18 |

## Execution

Status: `ready`; task kind: `executable`; guided profile.
Readiness route: standalone guided preflight after derived verification —
confirm the current assertion inventory and that SIDE-003.3's description for
this skill is final before edits.
Verification-design recommendation: separate — this package has no local test
root, so the decisive closure evidence must be designed (per-reference
conditions, fail-first disposable-candidate checks) rather than assumed.

```yaml
agent_tier: standard
reasoning: medium
review: immediate
budget: 15 tool calls / 42 minutes / one-package restructuring with obligation map and closure evidence
```

Sizing: `default@1`; estimate 13 implementation calls / 38 minutes;
confidence medium; fits.

Stops: an obligation that cannot be preserved by extraction (stop; do not
delete it to shrink bytes); any behavior change to plan or task-map policy
(route back through the parent); profile drift in the active installation
(report, do not fix); missing live-eval budget (report qualification pending).

Next action: derive `verification.md`, obtain a ready `preflight.md` through
standalone guided preflight, then implement.
Required follow-on: immediately after implementation or correction and any
applicable conditional stages, hand the completed bytes to a fresh independent
`task-review-discovery` call, and hand its report to a separate
`task-acceptance-review` decision.

Expected contract impact: none — no registry record declares this package's
authority; `docs/project-plan.md` and `docs/task-map.json` policy is
unchanged.