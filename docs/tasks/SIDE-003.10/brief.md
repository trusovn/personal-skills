# Task Brief: SIDE-003.10 — Restructure task-preflight for conditional loading

## Outcome

`skills/task-implementation-flow/task-preflight` loads only the instructions
its current flow needs. Scenario-conditional material — high-assurance
freshness and packet mechanics, strict machine-packet reconstruction,
conversational vs packaged routing detail — moves into package references,
each with an explicit when-to-read condition and timing; the entry file keeps
the readiness contract, routing rules, and a reference loading table. Every
preserved obligation is mapped old→new; behavior is unchanged.

## Authority and scope

| Item | Contract |
|---|---|
| Authority | [SIDE-003 plan](../SIDE-003/plan.md), "Body design and mandatory loading", "Delivery sequence" phase 4, "Measurement and decision rules" layer 2; owner adjustment (2026-11-03): figure the exact split places; clear when-to-read instructions are the acceptance center |
| Dependencies | SIDE-003.1–.6 complete (baseline + this skill's description final) |
| Allowed changes | This package's `SKILL.md` body, its `references/` (`execution-packet-template.md`, new files), its `evals/` inputs, owning test expectations that assert its text, and this skill's section in `docs/tasks/SIDE-003/rollout-results.md` |
| Read-only context | The SIDE-003.1 baseline and read graph; `tests/test_task_preflight.py` (asserts this `SKILL.md`'s text), `tests/test_task_preparation_contracts.py`; `docs/contracts/measurement.json` (declares this `SKILL.md` and the packet template for starting-evidence/native-obligations/readiness authority) |
| Out of scope | The `description` frontmatter (compressed in SIDE-003.3 — do not change); any behavior change to readiness, freshness, or packet policy; the `references/execution-packet-template.md` path (bounded-task-implementer links it cross-package — keep the path stable); other skills; the active `.agents/` installation |
| Assumptions / unresolved | The exact conditional clusters are this leaf's design work; the ordinary guided readiness workflow is near-universal and stays inline |

## Work and acceptance criteria

Required work:

1. Before any edit, freeze the obligation inventory in the rollout-results
   section: every readiness rule, freshness rule, routing rule, packet
   requirement, and stop rule in the current entry file, each with its
   current authority location.
2. Identify the actual conditional paths (high-assurance freshness and packet
   mechanics; strict machine-packet reconstruction; conversational vs
   packaged entry). Do not invent profiles the skill lacks.
3. Extract conditional scenario clusters into `references/` files. Give every
   reference — new and existing — an explicit read condition and timing in
   the entry file (`execution-packet-template.md` before producing an
   execution packet; new references at their own triggers). Keep near-
   universal material inline.
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
  inventory; no readiness, freshness, routing, or packet obligation is lost
  or weakened; behavior-preservation fixtures pass unchanged before
  and after the edit; only the new loading-structure assertions (reference
  existence, explicit conditions, relocated obligations) reject the pre-edit
  layout and pass after; the stale/blocked/mismatched routing behavior
  is unchanged in the existing fixtures.
- **AC-03:** Entry-only and per-route cumulative costs are recorded
  before/after; a route that did not shrink is explained, not hidden; the
  `references/execution-packet-template.md` path and the description
  frontmatter are unchanged.

## Verification

| Evidence | Scenario and oracle | Command |
|---|---|---|
| Fail-first | Behavior-preservation fixtures pass unchanged against the pre-edit bytes; the new loading-structure assertions (reference existence, explicit conditions, relocated obligations) reject the pre-edit layout; in a disposable candidate, removing one required link or bypassing one route is detected by the relevant check | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_task_preflight.py` |
| Targeted | Readiness/routing behavior in the existing preflight fixtures (stale, blocked, mismatched, conversational, packaged) is unchanged | `… -p test_task_preflight.py` |
| Owning suite | Preparation-contract expectations for the preflight route | `… -p test_task_preparation_contracts.py` |
| Broader gate | Aggregate gate and disposable-install reference resolution at SIDE-003.18; live behavioral qualification only with separately approved budget, else recorded pending | SIDE-003.18 |

## Execution

Status: `ready`; task kind: `executable`; guided profile.
Readiness route: standalone guided preflight after derived verification —
confirm the current assertion inventory and that SIDE-003.3's description for
this skill is final before edits.
Verification-design recommendation: separate — obligation-preservation
coverage across relocation and the freshness/packet routes need designed
scenarios.

```yaml
agent_tier: standard
reasoning: high
review: immediate
budget: 17 tool calls / 50 minutes / one-package restructuring with obligation map and closure tests
```

Sizing: `default@1`; estimate 15 implementation calls / 45 minutes;
confidence medium; triggered `max_duration_minutes`.
Decomposition override: `cannot_split_safely` — candidate boundary
(packet-mechanics vs high-assurance-freshness extraction) rejected: one entry
file plus shared suites; both stages would re-edit the same readiness
contract and renegotiate the same loading table. Residual risk: a longer
single leaf, mitigated by the pre-edit obligation inventory, staged commits,
and the immediate fresh review.

Stops: an obligation that cannot be preserved by extraction (stop; do not
delete it to shrink bytes); any behavior change to readiness or freshness
policy (route back through the parent); profile drift in the active
installation (report, do not fix); missing live-eval budget (report
qualification pending).

Next action: derive `verification.md`, obtain a ready `preflight.md` through
standalone guided preflight, then implement.
Required follow-on: immediately after implementation or correction and any
applicable conditional stages, hand the completed bytes to a fresh independent
`task-review-discovery` call, and hand its report to a separate
`task-acceptance-review` decision.

Expected contract impact: `docs/contracts/measurement.json` declares this
package's `SKILL.md` and `references/execution-packet-template.md` for
starting-evidence-producer, native-obligations-handoff, and
starting-evidence-readiness-reference; extraction is expected to move
declared authority text into new reference paths. Synchronize that record
through this leaf's designated `task-contract-registry-updater` stage with the
explicit `--write-index` command, in the same change. Behavior is unchanged,
so summaries and invariants are preserved, not rewritten.