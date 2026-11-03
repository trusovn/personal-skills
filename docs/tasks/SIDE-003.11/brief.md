# Task Brief: SIDE-003.11 — Restructure task-maintainability-review for conditional loading

## Outcome

`skills/task-implementation-flow/task-maintainability-review` loads only the
instructions its current flow needs. Scenario-conditional material — verdict
routes, architecture-gate ownership, profile-specific review scope — moves
into package references where safely separable, each with an explicit
when-to-read condition and timing; the entry file keeps the review contract,
scope rules, and a reference loading table. Every preserved obligation is
mapped old→new; behavior is unchanged.

## Authority and scope

| Item | Contract |
|---|---|
| Authority | [SIDE-003 plan](../SIDE-003/plan.md), "Body design and mandatory loading", "Delivery sequence" phase 4 ("Use actual conditional paths rather than inventing guided/high-assurance profiles for skills that lack them"), "Measurement and decision rules" layer 2; owner adjustment (2026-11-03): figure the exact split places; clear when-to-read instructions are the acceptance center |
| Dependencies | SIDE-003.1–.6 complete (baseline + this skill's description final) |
| Allowed changes | This package's `SKILL.md` body, its `references/` (currently none — new files), its `evals/` inputs, owning test expectations that assert its text, and this skill's section in `docs/tasks/SIDE-003/rollout-results.md` |
| Read-only context | The SIDE-003.1 baseline and read graph; `tests/test_task_maintainability_review.py` (also asserts `../../testing-discipline/SKILL.md` content — coordinate with SIDE-003.12), `tests/test_task_flow_guides.py` |
| Out of scope | The `description` frontmatter (compressed in SIDE-003.4 — do not change); any behavior change to verdicts, scope, or gate ownership; renaming or moving the package; other skills (in particular do not edit testing-discipline — SIDE-003.12 owns it); the active `.agents/` installation |
| Assumptions / unresolved | The exact conditional clusters are this leaf's design work; a no-op decision (no extraction) is acceptable with recorded reason if the body is already compact or near-universal |

## Work and acceptance criteria

Required work:

1. Before any edit, freeze the obligation inventory in the rollout-results
   section: every scope rule, verdict definition, gate-ownership rule, and
   stop/route rule in the current entry file, each with its current authority
   location.
2. Identify the actual conditional paths. Do not invent profiles the skill
   lacks; a scenario cluster may be split only if it is genuinely separable
   and conditionally applicable.
3. Extract qualifying clusters into `references/` files with an explicit read
   condition and timing in the entry file; keep near-universal material
   inline; a reasoned no-op is acceptable.
4. State the missing-reference rule (if any references exist after this
   work): a required reference that is missing or unreadable stops the
   affected action with the exact gap reported; no inferred bypass.
5. Update the owning assertions to assert the applicable instruction closure
   and required route rather than deleted literal text. Preserve distinct
   existing scenarios; extend fixtures only for missing loading-condition
   cases.
6. Record the instruction map (each old obligation → new location, loading
   condition, proving scenario), the per-route measured cost (entry-only and
   cumulative, before/after, from the SIDE-003.1 baseline record's file table
   and route inventories), and any no-op
   decision with reason.

- **AC-01:** Every reference this package owns has an explicit when-to-read
  condition and timing in the entry file; a reader following only the entry
  file knows, before each dependent action, whether a reference applies.
- **AC-02:** The instruction map covers every obligation from the pre-edit
  inventory; no scope rule, verdict, or gate-ownership obligation is lost or
  weakened; behavior-preservation fixtures pass unchanged before and
  after the edit; only the new loading-structure assertions (reference
  existence, explicit conditions, relocated obligations) reject the pre-edit
  layout and pass after; the cross-suite assertion on testing-discipline content
  still resolves (coordinate the update with SIDE-003.12 if its change lands
  first).
- **AC-03:** Entry-only and per-route cumulative costs are recorded
  before/after; a route that did not shrink is explained, not hidden; the
  description frontmatter is unchanged.

## Verification

| Evidence | Scenario and oracle | Command |
|---|---|---|
| Fail-first | Behavior-preservation fixtures pass unchanged against the pre-edit bytes; the new loading-structure assertions (reference existence, explicit conditions, relocated obligations) reject the pre-edit layout; in a disposable candidate, removing one required link or bypassing one route is detected by the relevant check (skip with reason if no references exist after a no-op decision) | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_task_maintainability_review.py` |
| Targeted | Review-scope/verdict behavior in the existing fixtures is unchanged | `… -p test_task_maintainability_review.py` |
| Owning suite | Flow-guide assertions for this skill's routes | `… -p test_task_flow_guides.py` |
| Broader gate | Aggregate gate and disposable-install reference resolution at SIDE-003.18; live behavioral qualification only with separately approved budget, else recorded pending | SIDE-003.18 |

## Execution

Status: `ready`; task kind: `executable`; guided profile.
Readiness route: standalone guided preflight after derived verification —
confirm the current assertion inventory and that SIDE-003.4's description for
this skill is final before edits.
Verification-design recommendation: separate — obligation-preservation
coverage across relocation and the verdict routes need designed scenarios,
including the no-op branch if extraction is declined.

```yaml
agent_tier: standard
reasoning: high
review: immediate
budget: 16 tool calls / 45 minutes / one-package restructuring with obligation map and closure tests
```

Sizing: `default@1`; estimate 14 implementation calls / 40 minutes;
confidence medium; fits.

Stops: an obligation that cannot be preserved by extraction (stop; do not
delete it to shrink bytes); any behavior change to review policy (route back
through the parent); profile drift in the active installation (report, do not
fix); missing live-eval budget (report qualification pending).

Next action: derive `verification.md`, obtain a ready `preflight.md` through
standalone guided preflight, then implement.
Required follow-on: immediately after implementation or correction and any
applicable conditional stages, hand the completed bytes to a fresh independent
`task-review-discovery` call, and hand its report to a separate
`task-acceptance-review` decision.

Expected contract impact: none — no registry record declares this package's
authority.