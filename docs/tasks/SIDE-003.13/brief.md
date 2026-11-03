# Task Brief: SIDE-003.13 — Restructure skill-creator for conditional loading

## Outcome

`skills/skill-creator` loads only the instructions the task at hand needs.
Scenario-conditional material — behavioral-eval and benchmark mechanics,
future-work limits, validation recipes, package-structure deep dives — moves
into package references where safely separable, each with an explicit
when-to-read condition and timing; the entry file keeps the authoring core,
quality rules, and a reference loading table. Every preserved obligation is
mapped old→new; behavior is unchanged.

## Authority and scope

| Item | Contract |
|---|---|
| Authority | [SIDE-003 plan](../SIDE-003/plan.md), "Body design and mandatory loading", "Delivery sequence" phase 4 (inspect larger packages), "Measurement and decision rules" layer 2; owner adjustment (2026-11-03): figure the exact split places; clear when-to-read instructions are the acceptance center |
| Dependencies | SIDE-003.1–.6 complete (baseline + this skill's description final) |
| Allowed changes | This package's `SKILL.md` body, its `references/` (`schemas.md`, new files), its `docs/` if instruction-bearing, its `evals/` inputs, its tests root expectations, and this skill's section in `docs/tasks/SIDE-003/rollout-results.md` |
| Read-only context | The SIDE-003.1 baseline and read graph; `skills/skill-creator/scripts/quick_validate.py`, `skills/skill-creator/scripts/run_behavior_evals.py` (skill-owned runtime scripts — architecture policy governs their imports; do not break them); `skills/skill-creator/docs/codex-behavioral-eval-runner-future-work.md` (the runner's documented limits stay accurate); the skill-creator tests root in `tools/verify.py` |
| Out of scope | The `description` frontmatter (compressed in SIDE-003.6 — do not change); any behavior change to authoring, validation, or eval-runner policy; renaming or moving the package; the runner's CLI surface; other skills; the active `.agents/` installation |
| Assumptions / unresolved | The exact conditional clusters are this leaf's design work; the entry file is the largest in the repository — inspect before assuming what is conditional |

## Work and acceptance criteria

Required work:

1. Before any edit, freeze the obligation inventory in the rollout-results
   section: every authoring rule, validation rule, eval-runner obligation,
   and quality gate in the current entry file, each with its current
   authority location.
2. Identify the actual conditional paths (benchmark generation; behavioral
   eval design/execution and grading; manual frontmatter validation recipes;
   package anatomy deep dives; schemas consultation). The authoring core
   stays inline. Do not invent profiles the skill lacks.
3. Extract qualifying clusters into `references/` files; give every reference —
   new and existing — an explicit read condition and timing in the entry file
   (`schemas.md` currently sits behind "See … for the full schema" — replace
   vague pointers with explicit conditions); keep near-universal material
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
  inventory; no authoring, validation, or runner obligation is lost or
  weakened; behavior-preservation fixtures pass unchanged before and
  after the edit; only the new loading-structure assertions (reference
  existence, explicit conditions, relocated obligations) reject the pre-edit
  layout and pass after; the runner's documented limits remain accurately described.
- **AC-03:** Entry-only and per-route cumulative costs are recorded
  before/after; a route that did not shrink is explained, not hidden; the
  description frontmatter and the runner's CLI surface are unchanged.

## Verification

| Evidence | Scenario and oracle | Command |
|---|---|---|
| Fail-first | Behavior-preservation fixtures pass unchanged against the pre-edit bytes; the new loading-structure assertions (reference existence, explicit conditions, relocated obligations) reject the pre-edit layout; in a disposable candidate, removing one required link or bypassing one route is detected by the relevant check | the skill-creator tests root via `python3 tools/verify.py` (this leaf's roots) |
| Targeted | Package structure, validation, and eval-design expectations unchanged in behavior | as above |
| Owning suite | The skill-creator tests root is a `tools/verify.py` discovery root | `python3 tools/verify.py` (this leaf's roots) |
| Broader gate | Aggregate gate and disposable-install reference resolution at SIDE-003.18; live behavioral qualification only with separately approved budget, else recorded pending | SIDE-003.18 |

## Execution

Status: `ready`; task kind: `executable`; guided profile.
Readiness route: standalone guided preflight after derived verification —
confirm the current assertion inventory and that SIDE-003.6's description for
this skill is final before edits.
Verification-design recommendation: separate — obligation-preservation
coverage across the largest entry file and the runner-accuracy obligations
need designed scenarios.

```yaml
agent_tier: standard
reasoning: high
review: immediate
budget: 22 tool calls / 60 minutes / one-package restructuring with obligation map and closure tests
```

Sizing: `default@1`; estimate 20 implementation calls / 55 minutes;
confidence low (largest entry file; conditional-cluster discovery affects
scope); triggered `max_agent_calls` and `max_duration_minutes`.
Decomposition override: `cannot_split_safely` — candidate boundary (authoring
core vs eval/benchmark mechanics extraction) rejected: one entry file plus a
shared tests root; both stages would re-edit the same file and renegotiate the
same loading table. Residual risk: a long single leaf, mitigated by the
pre-edit obligation inventory, staged commits, and the immediate fresh
review.

Stops: an obligation that cannot be preserved by extraction (stop; do not
delete it to shrink bytes); any behavior change to authoring or runner policy
(route back through the parent); profile drift in the active installation
(report, do not fix); missing live-eval budget (report qualification pending).

Next action: derive `verification.md`, obtain a ready `preflight.md` through
standalone guided preflight, then implement.
Required follow-on: immediately after implementation or correction and any
applicable conditional stages, hand the completed bytes to a fresh independent
`task-review-discovery` call, and hand its report to a separate
`task-acceptance-review` decision.

Expected contract impact: none — no registry record declares this package's
authority; its scripts' contracts are unchanged.