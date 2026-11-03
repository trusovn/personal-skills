# Task Brief: SIDE-003.7 — Restructure bounded-task-implementer for conditional loading

## Outcome

`skills/task-implementation-flow/bounded-task-implementer` loads only the
instructions its current flow needs. Scenario-conditional material — explicit
high-assurance and supplied strict machine contracts; the run-evidence
lifecycle; corrections and resume — moves into package references, each
carrying an explicit when-to-read condition and timing; the entry file keeps
the guided default, mandatory gates, stop/route rules, and a reference
loading table. Every preserved obligation is mapped old→new; behavior is
unchanged. This former pilot skill is a primary target (owner, 2026-11-03).

## Authority and scope

| Item | Contract |
|---|---|
| Authority | [SIDE-003 plan](../SIDE-003/plan.md), "Body design and mandatory loading" (SKILL.md always-on list; the proposed conditional references `references/high-assurance.md`, `references/run-evidence.md`, `references/correction-protocol.md` and their loading conditions — names are proposals, not contracts; the keep-visible obligation list), "Measurement and decision rules" layer 2, "Verification strategy" rows "Gate bypass", "Lost optional evidence", "Correction/provenance loss"; owner adjustment (2026-11-03): figure the exact split places; scenario clusters that can be safely split into separate instruction files should be; clear when-to-read instructions are the acceptance center |
| Dependencies | SIDE-003.1–.6 complete (baseline + this skill's description final) |
| Allowed changes | This package's `SKILL.md` body, its `references/` (new and existing), its `evals/` inputs, owning test/fixture expectations that assert its text, and this skill's section in `docs/tasks/SIDE-003/rollout-results.md` |
| Read-only context | The SIDE-003.1 baseline and read graph; `tests/test_bounded_task_implementer.py`, `tests/test_task_preparation_contracts.py`, `tests/test_task_flow_guides.py`, `tests/test_run_evidence_availability.py`, `tests/test_review_composition.py`, `tests/review_fixture_support.py`; `docs/contracts/implementer-feedback.json` |
| Out of scope | The `description` frontmatter (compressed in SIDE-003.4 — do not change); any behavior change (activation, gates, routes, output contracts); renaming the skill or moving its folder; the `../task-preflight/references/execution-packet-template.md` target (owned by SIDE-003.10 — keep this skill's cross-link valid); other skills; new shared runtime dependencies or harnesses; the active `.agents/` installation |
| Assumptions / unresolved | The exact conditional clusters and split points are this leaf's design work; inspect existing eval fixtures before extending them |

## Work and acceptance criteria

Required work:

1. Before any edit, freeze the obligation inventory in the rollout-results
   section: every gate, profile rule, stop/route rule, preservation rule, and
   output requirement in the current entry file, each with its current
   authority location.
2. Identify the actual conditional paths (guided default; explicit
   high-assurance and supplied strict machine contracts; run-evidence
   availability/attempt/skip-once; corrections and resume). Do not invent
   profiles the skill lacks.
3. Extract conditional scenario clusters into `references/` files. Give every
   reference — new and existing — an explicit read condition and timing in
   the entry file (a loading table or per-reference statements), e.g. "before
   the first evidence operation when…", "before acting on a correction…".
   Keep material that applies to almost every invocation inline.
4. Keep the plan's keep-visible obligations in the entry file: guided is the
   default (a ready package alone does not select high-assurance; direct vs
   packaged prerequisites stay distinct); packaged work requires applicable
   verification and ready preflight, with composite/stale/mismatched/legacy
   inputs routed to their owner before edits; preserve user work and one
   original baseline; required native checks keep scope, policy, ownership,
   and failure consequences; the cheap installation-local run-evidence
   availability check, attempt, and skip-once rule (available tooling still
   activates best-effort instrumentation in guided mode; mandatory
   instrumentation stays strict; missing tooling never triggers
   cross-installation fallback or provisioning); the conditional submission
   order, reviewer independence, and stale-evidence rules.
5. State the missing-reference rule: a required reference that is missing or
   unreadable stops the affected action with the exact gap reported; no
   inferred bypass. Do not read every reference at startup.
6. Update the owning assertions to assert the applicable instruction closure
   and required route rather than deleted literal text. Preserve distinct
   existing scenarios; extend fixtures only for missing loading-condition
   cases.
7. Record the instruction map (each old obligation → new location, loading
   condition, proving scenario), the per-route measured cost (entry-only and
   cumulative, before/after, from the SIDE-003.1 baseline record's file table
   and route inventories), and any no-op
   decisions with reasons.

- **AC-01:** Every reference this package owns or consumes has an explicit
  when-to-read condition and timing in the entry file; a reader following
  only the entry file knows, before each dependent action, whether a
  reference applies.
- **AC-02:** The instruction map covers every obligation from the pre-edit
  inventory; no gate, route, stop rule, or preservation rule is lost or
  weakened; behavior-preservation fixtures pass unchanged before and
  after the edit; only the new loading-structure assertions (reference
  existence, explicit conditions, relocated obligations) reject the pre-edit
  layout and pass after; behavior in the plan's selected cases (gate bypass, lost
  optional evidence, correction/provenance) is unchanged, using the existing
  fixtures.
- **AC-03:** Entry-only and per-route cumulative costs are recorded
  before/after; a route that did not shrink is explained, not hidden; the
  `../task-preflight/…` cross-link and the description frontmatter are
  unchanged.

## Verification

| Evidence | Scenario and oracle | Command |
|---|---|---|
| Fail-first | Behavior-preservation fixtures pass unchanged against the pre-edit bytes; the new loading-structure assertions (reference existence, loading conditions, keep-visible obligations in their new locations) reject the pre-edit layout; in a disposable candidate, removing one required link or bypassing one route is detected by the relevant check | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_bounded_task_implementer.py` |
| Targeted | Plan risk rows: direct edit, ready package, missing/mismatched verification, stale/blocked preflight, composite parent, strict machine contract — expected proceed/refusal and route unchanged; run-evidence available/missing/failed-first-operation/interrupted-run keeps attempt/skip-once/block/recovery with the same installation resolution; correction fixtures keep baseline preservation, conditional re-entry order, and the fresh-reviewer requirement | `… -p test_task_preparation_contracts.py`, `… -p test_run_evidence_availability.py`, `… -p test_review_composition.py` |
| Owning suite | Flow-guide assertions for this skill's routes | `… -p test_task_flow_guides.py` |
| Broader gate | Aggregate gate and disposable-install reference resolution at SIDE-003.18; live behavioral qualification only with separately approved budget, else recorded pending | SIDE-003.18 |

## Execution

Status: `ready`; task kind: `executable`; guided profile.
Readiness route: standalone guided preflight after derived verification —
confirm the current assertion inventory and that SIDE-003.4's description for
this skill is final before edits.
Verification-design recommendation: separate — obligation-preservation
coverage across relocation, conditional-branch reachability, and the
missing-reference stop rule need designed scenarios; the derived verification
must map the plan's three risk rows to concrete fail-first cases.

```yaml
agent_tier: standard
reasoning: high
review: immediate
budget: 26 tool calls / 75 minutes / one-package restructuring with obligation map and closure tests
```

Sizing: `default@1`; estimate 24 implementation calls / 70 minutes;
confidence low (largest package; conditional-cluster discovery affects
scope); triggered `max_agent_calls` and `max_duration_minutes`.
Decomposition override: `cannot_split_safely` — candidate boundary (staged
extraction per conditional reference) rejected: the package is one entry file
plus shared owning suites; each stage would re-edit the same entry file and
renegotiate the same loading table and obligation map. Residual risk: a long
single leaf, mitigated by the pre-edit obligation inventory, per-reference
staged commits, and the immediate fresh review.

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

Expected contract impact: `docs/contracts/implementer-feedback.json` declares
this package's `SKILL.md` for five provides/artifacts; extraction is expected
to move declared authority text into new reference paths. Synchronize that
record through this leaf's designated `task-contract-registry-updater` stage
with the explicit `--write-index` command, in the same change. Behavior is
unchanged, so summaries and invariants are preserved, not rewritten.