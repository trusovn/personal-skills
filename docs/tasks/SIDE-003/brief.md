# Task Brief: SIDE-003 — Reduce skill loading cost while preserving behavior

Status: `decomposed`
Task kind: `composite`

## Outcome

Agent sessions load fewer skill instructions. Discovery descriptions for all
26 source packages are compressed to the job, positive trigger, and
consequential exclusions. Restructured entry files load detailed procedures
only when the flow at hand needs them, through explicit when-to-read
conditions for every reference, with safely separable scenario clusters split
into their own instruction files. Activation boundaries, output contracts,
safeguards, and quality gates are preserved unchanged. The driver is the
owner's token-consumption reduction goal; the authority is
[the SIDE-003 plan](plan.md).

## Direction trace

- Direction contribution: the plan's outcome and scope; the owner's session
  adjustments of 2026-11-03 recorded under Authority.
- User-observable effect: smaller rendered skill catalogs and smaller
  selected-skill instruction loads; no behavior change in any skill.
- Why now: the owner is reducing token consumption across many loaded skills;
  the plan freezes a measured baseline before any edit.
- Direction decisions used: plan "Outcome and scope", "Description design",
  "Body design and mandatory loading", "Delivery sequence", "Measurement and
  decision rules", "Verification strategy", "Completion and rollback"
  (completion side only); owner adjustments (2026-11-03): the pilot experiment
  framing is skipped and its two skills (bounded-task-implementer,
  task-acceptance-review) are restructured directly as primary targets; clear
  when-to-read instructions are the acceptance center, and scenario clusters
  that can be safely split into separate instructions should be; no rollback
  functionality is built now — Git history is the revert path.
- New direction decisions required: None.

## Authority and scope

- Authority: [SIDE-003 plan](plan.md), all sections; the owner's session
  instructions of 2026-11-03; this decomposition.
- Repository root: this repository; editable source under `skills/` only.
- Original scope: the plan's phases minus the pilot experiment framing, with
  bounded-task-implementer and task-acceptance-review restored as direct
  restructuring targets.
- Out of scope (plan): user-global skills, refreshing this repository's active
  `.agents/` installation, host context settings, separate public
  guided/high-assurance skills, loader frameworks, workflow-policy changes,
  gate removal, prose-to-executable-helper conversion, new tokenizer
  dependencies, provider spending without separate approval.
- The plan document is never overwritten. Leaf results are written beside it
  in this package directory; execution history never edits the plan.

## Execution sizing

- Sizing policy: `default@1` (max 15 agent calls / 40 implementation minutes;
  `strong`+`high` execution profile disallowed; overrides require reason).
- Original estimate: ~230 agent calls / ~700 implementation minutes as one
  task; original execution profile `standard` / `high`; confidence medium.
- Triggered rules: `max_agent_calls`, `max_duration_minutes`.
- Boundary decision: split at plan-phase and package-ownership boundaries —
  one baseline leaf, five description leaves aligned to the plan's
  boundary-group table, one restructuring leaf per skill package, two
  conditional-loading leaves for the remaining reference-bearing skills, one
  closing validation leaf. Each leaf owns disjoint files and a consumed artifact
  (measurements, compressed descriptions, restructured packages, results) and
  is independently verifiable against its own suites.

## Decomposition

| Child | Responsibility / owned output | Depends on | Brief |
|---|---|---|---|
| SIDE-003.1 | Reproducible loading-cost baseline: measurement command, per-file hashes/bytes/description characters, 20-skill subset, file-level read graph, representative-route inventories with summed sizes, command-prerequisites map; verifies the plan's table | — | [brief](../SIDE-003.1/brief.md) |
| SIDE-003.2 | Descriptions for boundary groups 1–2 (6 profile skills) | .1 | [brief](../SIDE-003.2/brief.md) |
| SIDE-003.3 | Descriptions for boundary groups 3–4 (5 profile skills) | .1 | [brief](../SIDE-003.3/brief.md) |
| SIDE-003.4 | Descriptions for boundary groups 5–6 (5 profile skills) | .1 | [brief](../SIDE-003.4/brief.md) |
| SIDE-003.5 | Descriptions for boundary groups 7–8 (4 profile skills) | .1 | [brief](../SIDE-003.5/brief.md) |
| SIDE-003.6 | Descriptions for boundary groups 9–10 (6 remaining source skills) | .1–.5 | [brief](../SIDE-003.6/brief.md) |
| SIDE-003.7 | Restructure bounded-task-implementer for conditional loading | .1–.6 | [brief](../SIDE-003.7/brief.md) |
| SIDE-003.8 | Restructure task-acceptance-review for conditional loading | .1–.6 | [brief](../SIDE-003.8/brief.md) |
| SIDE-003.9 | Restructure task-brief-designer for conditional loading | .1–.6 | [brief](../SIDE-003.9/brief.md) |
| SIDE-003.10 | Restructure task-preflight for conditional loading | .1–.6 | [brief](../SIDE-003.10/brief.md) |
| SIDE-003.11 | Restructure task-maintainability-review for conditional loading | .1–.6 | [brief](../SIDE-003.11/brief.md) |
| SIDE-003.12 | Restructure testing-discipline for conditional loading | .1–.6 | [brief](../SIDE-003.12/brief.md) |
| SIDE-003.13 | Restructure skill-creator for conditional loading | .1–.6 | [brief](../SIDE-003.13/brief.md) |
| SIDE-003.14 | Restructure repo-foundation for conditional loading | .1–.6 | [brief](../SIDE-003.14/brief.md) |
| SIDE-003.15 | Restructure project-delivery-plan for conditional loading | .1–.6 | [brief](../SIDE-003.15/brief.md) |
| SIDE-003.16 | Conditional loading for architecture-guardrails, foundation-readiness-review, project-direction, project-plan-verification: explicit read-conditions; safe extraction or justified no-op; no read introduced for background/unused resources | .1–.6 | [brief](../SIDE-003.16/brief.md) |
| SIDE-003.17 | Conditional loading for idea-brief, senior-code-review, task-review-discovery, task-verification-designer, task-orchestrator: explicit read-conditions; safe extraction or justified no-op; no read introduced for background/unused resources | .1–.6 | [brief](../SIDE-003.17/brief.md) |
| SIDE-003.18 | Disposable-install validation, aggregate gates, published results | .1–.17 | [brief](../SIDE-003.18/brief.md) |

## Coverage and closure

| Plan obligation | Owning leaf(s) |
|---|---|
| Phase 1 baseline (inventory, hashes, read graph, representative-route inventories, prerequisites) | .1; snapshot/rollback machinery dropped per owner — hashes exist for before/after attribution only |
| Phase 2 description compression — all 26, profile subset first, trigger boundaries and group distinctions preserved | .2–.6 |
| Phase 3 pilot experiment framing | Dropped per owner 2026-11-03; its two skills are restructured directly by .7 and .8, with the plan's pilot obligations (entry-file keep-visible list, proposed conditional references and their loading conditions) as their contract |
| Phase 4 selective restructuring, instruction maps, no-op decisions | .7–.15 |
| Explicit when-to-read conditions and conditional loading for the remaining reference-bearing skills | .16–.17 (extraction where genuinely conditional, justified no-op otherwise; no read introduced for background or unused resources) |
| Phase 5 distribution validation, contract authorities, results | .18; rollback units dropped per owner; the deliberately-unrefreshed active installation's expected drift is reported separately, and the fresh disposable targets are the validation surface |
| Measurement layer 1 (catalog) and layer 2 (loaded instructions) | .1 defines the reproducible basis and representative-route inventories; .2–.6 and .7–.17 record per-change deltas; .18 aggregates |
| Measurement layer 3 (session use), live routing/behavioral qualification | Designed by the owning leaves and .18; executed only with separately approved budget; otherwise reported pending |
| Per-skill behavior preservation cases from the plan's risk table | Each restructuring leaf's derived verification (via `task-verification-designer`), reusing the plan's named fixtures and suites |

Shared artifacts: `description-results.md` is appended in leaf order by .2–.6;
`rollout-results.md` is appended by .7–.17; `baseline.md`, the measurements
record, and `results.md` live beside the plan in this package directory.
Leaves that share a results file or touch the same `SKILL.md` must not run
concurrently; serialize them through the task flow. The description phase
completes before any restructuring leaf begins (same-file serialization and
the plan's phase order).

All parent acceptance closes through the leaves; .18 owns the final aggregate
proof. Nine leaves (.1, .7, .8, .9, .10, .13, .14, .16, .17) carry recorded
`cannot_split_safely` overrides: single skill packages that are one entry
file plus shared owning suites (.7, .8, .9, .10, .13, .14); one measurement
record whose route inventories reuse the same per-file reads and counting
basis (.1); and two multi-skill clusters whose per-skill micro-leaves would
multiply preparation and review stages for units sharing one results section
and measurement basis (.16, .17). Every other leaf fits the active envelope.

## Handoff

Implement dependency-ready executable leaves only. Never hand this composite
parent to `bounded-task-implementer`. The parent is complete only when every
leaf has completed its own preparation, implementation, and immediate
independent review route (fresh `task-review-discovery` evidence, then a
separate `task-acceptance-review` decision). Do not update the plan document,
`docs/project-plan.md`, or `docs/task-map.json` to track this work.

## Expected contract impact

- Plan refs: none — side task (`source_plan_task: null`, like SIDE-002).
- Current contract dependencies: `docs/contracts/implementer-feedback.json`
  declares bounded-task-implementer's `SKILL.md`;
  `docs/contracts/measurement.json` declares task-preflight's `SKILL.md`
  and packet template, repo-foundation's `SKILL.md`, and
  architecture-guardrails' `SKILL.md`. Leaves .7, .10, and .14 are expected
  to move declared authority text, and .16 may move architecture-guardrails'
  declared authority; each synchronizes through its designated
  `task-contract-registry-updater` stage with the explicit `--write-index`
  command, in the same change. .17's task-orchestrator declarations cite
  scripts and tests and its module_docs paths are unchanged; no registry
  change is expected there — record any exception and route it to
  SIDE-003.18's registry check.
- Expected durable delta: instruction-location changes inside skill packages
  with unchanged behavior; wholesale installer copying carries new references
  automatically, and .18 proves that in a disposable installation.