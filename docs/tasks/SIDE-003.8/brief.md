# Task Brief: SIDE-003.8 — Restructure task-acceptance-review for conditional loading

## Outcome

`skills/task-implementation-flow/task-acceptance-review` loads only the
instructions its current flow needs. Exact packet reconstruction and
machine/report mechanics move into package references, each with an explicit
when-to-read condition and timing; the entry contract keeps reviewer
provenance, evidence admission, separate discovery/acceptance, verdict
meanings, contextual disposition precedence, deferral authority, and required
gate ownership. Every preserved obligation is mapped old→new; behavior is
unchanged. This former pilot skill is a primary target (owner, 2026-11-03).

## Authority and scope

| Item | Contract |
|---|---|
| Authority | [SIDE-003 plan](../SIDE-003/plan.md), "Body design and mandatory loading" (acceptance entry contract, "Move exact packet reconstruction and machine/report mechanics first. Retain a clear trigger for each conditional disposition or reproducer reference."), "Measurement and decision rules" layer 2, "Verification strategy" row "Acceptance weakened"; owner adjustment (2026-11-03): figure the exact split places; clear when-to-read instructions are the acceptance center |
| Dependencies | SIDE-003.1–.6 complete (baseline + this skill's description final) |
| Allowed changes | This package's `SKILL.md` body, its `references/` (`acceptance-report-template.md`, `tests-only-reproducer.md`, new files), its `evals/` inputs, owning test/fixture expectations that assert its text, and this skill's section in `docs/tasks/SIDE-003/rollout-results.md` |
| Read-only context | The SIDE-003.1 baseline and read graph; `tests/test_task_acceptance_review.py`, `tests/test_review_composition.py`, `tests/test_task_review_discovery.py`, `tests/review_fixture_support.py`, `tests/test_task_preparation_contracts.py` |
| Out of scope | The `description` frontmatter (compressed in SIDE-003.4 — do not change); any behavior change (verdicts, admission rules, disposition precedence, deferral authority); renaming or moving the package; other skills; new shared infrastructure; the active `.agents/` installation |
| Assumptions / unresolved | The exact conditional clusters are this leaf's design work; complex decision rules used on ordinary guided cases are not high-assurance-only material and must not be moved as if they were |

## Work and acceptance criteria

Required work:

1. Before any edit, freeze the obligation inventory in the rollout-results
   section: every verdict definition, admission rule, disposition trigger,
   deferral rule, gate-ownership rule, and output requirement in the current
   entry file, each with its current authority location.
2. Identify the actual conditional paths (durable-report emission;
   tests-only reproducer; strict machine-contract packet reconstruction;
   high-assurance evidence admission). Do not invent profiles the skill
   lacks.
3. Move exact packet reconstruction and machine/report mechanics into
   `references/` files first. Give every reference — new and existing — an
   explicit read condition and timing in the entry file. Keep material that
   applies to almost every invocation (verdict meanings, ordinary guided
   disposition rules, provenance/admission basics) inline.
4. Retain a clear trigger for each conditional disposition or reproducer
   reference in the entry file, and state the missing-reference rule: a
   required reference that is missing or unreadable stops the affected
   action with the exact gap reported; no inferred bypass. Do not read every
   reference at startup.
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
  inventory; no verdict, admission rule, disposition trigger, deferral
  authority, or gate ownership is lost or weakened; behavior-preservation fixtures pass
  unchanged before and after the edit; only the new loading-structure
  assertions (reference existence, explicit conditions, relocated
  obligations) reject the pre-edit layout and pass after; behavior in the
  plan's selected cases (complete/partial discovery, missing preparation,
  unresolved finding, permitted deferral, stale conditional review) is
  unchanged, using the existing fixtures.
- **AC-03:** Entry-only and per-route cumulative costs are recorded
  before/after; a route that did not shrink is explained, not hidden; the
  description frontmatter is unchanged.

## Verification

| Evidence | Scenario and oracle | Command |
|---|---|---|
| Fail-first | Behavior-preservation fixtures pass unchanged against the pre-edit bytes; the new loading-structure assertions (reference existence, explicit conditions, relocated obligations) reject the pre-edit layout; in a disposable candidate, removing one required link or bypassing one route is detected by the relevant check | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_task_acceptance_review.py` |
| Targeted | Plan "Acceptance weakened" row: expected verdict and owner-directed evidence request match preserved policy across complete/partial discovery, missing preparation, unresolved finding, permitted deferral, and stale conditional review | `… -p test_review_composition.py`, `… -p test_task_review_discovery.py` |
| Owning suite | Preparation-contract assertions for this skill's routes; shared review fixtures keep resolving | `… -p test_task_preparation_contracts.py` |
| Broader gate | Aggregate gate and disposable-install reference resolution at SIDE-003.18; live behavioral qualification only with separately approved budget, else recorded pending | SIDE-003.18 |

## Execution

Status: `ready`; task kind: `executable`; guided profile.
Readiness route: standalone guided preflight after derived verification —
confirm the current assertion inventory and that SIDE-003.4's description for
this skill is final before edits.
Verification-design recommendation: separate — obligation-preservation
coverage across relocation and the conditional-disposition triggers need
designed scenarios mapped to the plan's "Acceptance weakened" row.

```yaml
agent_tier: standard
reasoning: high
review: immediate
budget: 21 tool calls / 60 minutes / one-package restructuring with obligation map and closure tests
```

Sizing: `default@1`; estimate 19 implementation calls / 55 minutes;
confidence low (second-largest package; packet-mechanics discovery affects
scope); triggered `max_agent_calls` and `max_duration_minutes`.
Decomposition override: `cannot_split_safely` — candidate boundary
(report-mechanics vs packet-reconstruction extraction) rejected: one entry
file plus shared owning suites; both stages would re-edit the same entry
contract and renegotiate the same disposition-trigger table. Residual risk: a
long single leaf, mitigated by the pre-edit obligation inventory, staged
commits, and the immediate fresh review.

Stops: an obligation that cannot be preserved by extraction (stop; do not
delete it to shrink bytes); any need for new shared infrastructure or a
behavior change (route back through the parent); profile drift in the active
installation (report, do not fix); missing live-eval budget (report
qualification pending).

Next action: derive `verification.md`, obtain a ready `preflight.md` through
standalone guided preflight, then implement.
Required follow-on: immediately after implementation or correction and any
applicable conditional stages, hand the completed bytes to a fresh independent
`task-review-discovery` call, and hand its report to a separate
`task-acceptance-review` decision.

Expected contract impact: none — no registry record declares this package's
authority; record any discovered exception in this leaf's results and route it
to SIDE-003.18's registry check.