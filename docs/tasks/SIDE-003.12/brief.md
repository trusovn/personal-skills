# Task Brief: SIDE-003.12 — Restructure testing-discipline for conditional loading

## Outcome

`skills/testing-discipline` loads only the instructions the task at hand
needs. The testing core that applies during ordinary implementation stays
inline; specialized catalog material remains conditional behind an explicit
when-to-read condition and timing; every reference the package owns carries
one. Any further safely separable scenario clusters move into references.
Every preserved obligation is mapped old→new; behavior is unchanged.

## Authority and scope

| Item | Contract |
|---|---|
| Authority | [SIDE-003 plan](../SIDE-003/plan.md), "Body design and mandatory loading" ("the testing core applies during ordinary implementation; specialized test catalogs can remain conditional"), "Delivery sequence" phase 4, "Measurement and decision rules" layer 2; owner adjustment (2026-11-03): figure the exact split places; clear when-to-read instructions are the acceptance center |
| Dependencies | SIDE-003.1–.6 complete (baseline + this skill's description final) |
| Allowed changes | This package's `SKILL.md` body, its `references/` (`test-catalog.md`, new files), its `evals/` inputs, owning test expectations that assert its text, and this skill's section in `docs/tasks/SIDE-003/rollout-results.md` |
| Read-only context | The SIDE-003.1 baseline and read graph; `tests/test_task_maintainability_review.py` (asserts this skill's `SKILL.md` content cross-package — keep that assertion valid or coordinate its update with SIDE-003.11) |
| Out of scope | The `description` frontmatter (compressed in SIDE-003.5 — do not change); any behavior change to test-design authority (levels, determinism, gate ownership); renaming or moving the package; other skills; the active `.agents/` installation |
| Assumptions / unresolved | The exact conditional clusters are this leaf's design work; the existing `test-catalog.md` condition ("Read when defining a test strategy, reviewing broad coverage, preparing a release, or selecting specialized evidence") is the baseline pattern — verify, tighten if needed, and record |

## Work and acceptance criteria

Required work:

1. Before any edit, freeze the obligation inventory in the rollout-results
   section: every test-level rule, determinism rule, gate-ownership rule, and
   preservation rule in the current entry file, each with its current
   authority location.
2. Identify the actual conditional paths (specialized functional and
   non-functional catalogs; release-preparation material; any distinct
   review-mode cluster). The ordinary implementation core stays inline. Do
   not invent profiles the skill lacks.
3. Extract qualifying clusters into `references/` files; give every
   reference — new and existing — an explicit read condition and timing in
   the entry file; keep near-universal material inline; a reasoned no-op is
   acceptable where material is already compact or always-needed.
4. State the missing-reference rule: a required reference that is missing or
   unreadable stops the affected action with the exact gap reported; no
   inferred bypass. Do not read every reference at startup.
5. Update the owning assertions to assert the applicable instruction closure
   and required route rather than deleted literal text; keep the
   cross-package assertion in `tests/test_task_maintainability_review.py`
   resolving.
6. Record the instruction map (each old obligation → new location, loading
   condition, proving scenario), the per-route measured cost (entry-only and
   cumulative, before/after, from the SIDE-003.1 baseline record's file table
   and route inventories), and any no-op
   decision with reason.

- **AC-01:** Every reference this package owns has an explicit when-to-read
  condition and timing in the entry file; a reader following only the entry
  file knows, before each dependent action, whether a reference applies.
- **AC-02:** The instruction map covers every obligation from the pre-edit
  inventory; no test-level, determinism, or gate-ownership obligation is lost
  or weakened; behavior-preservation fixtures pass unchanged before and
  after the edit; only the new loading-structure assertions (reference
  existence, explicit conditions, relocated obligations) reject the
  pre-edit layout and pass after; the during-implementation trigger is unchanged.
- **AC-03:** Entry-only and per-route cumulative costs are recorded
  before/after; a route that did not shrink is explained, not hidden; the
  description frontmatter is unchanged.

## Verification

| Evidence | Scenario and oracle | Command |
|---|---|---|
| Fail-first | Behavior-preservation fixtures pass unchanged against the pre-edit bytes; the new loading-structure assertions (reference existence, explicit conditions, relocated obligations) reject the pre-edit layout; in a disposable candidate, removing one required link or bypassing one route is detected by the relevant check | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_task_maintainability_review.py` |
| Targeted | The catalog's condition and the during-implementation core remain correctly split in the existing expectations | `… -p test_task_maintainability_review.py` |
| Owning suite | No package-local test root exists; the cross-suite above owns this skill's assertions (from the SIDE-003.1 prerequisites map) | as above |
| Broader gate | Aggregate gate and disposable-install reference resolution at SIDE-003.18; live behavioral qualification only with separately approved budget, else recorded pending | SIDE-003.18 |

## Execution

Status: `ready`; task kind: `executable`; guided profile.
Readiness route: standalone guided preflight after derived verification —
confirm the current assertion inventory and that SIDE-003.5's description for
this skill is final before edits.
Verification-design recommendation: separate — obligation-preservation
coverage and the catalog/ core split need designed scenarios.

```yaml
agent_tier: standard
reasoning: medium
review: immediate
budget: 14 tool calls / 38 minutes / one-package restructuring with obligation map and closure tests
```

Sizing: `default@1`; estimate 12 implementation calls / 32 minutes;
confidence medium; fits.

Stops: an obligation that cannot be preserved by extraction (stop; do not
delete it to shrink bytes); any behavior change to test-design authority
(route back through the parent); profile drift in the active installation
(report, do not fix); missing live-eval budget (report qualification pending).

Next action: derive `verification.md`, obtain a ready `preflight.md` through
standalone guided preflight, then implement.
Required follow-on: immediately after implementation or correction and any
applicable conditional stages, hand the completed bytes to a fresh independent
`task-review-discovery` call, and hand its report to a separate
`task-acceptance-review` decision.

Expected contract impact: none — no registry record declares this package's
authority.