# Task Brief: SIDE-003.9 — Restructure task-brief-designer for conditional loading

## Outcome

`skills/task-implementation-flow/task-brief-designer` loads only the
instructions its current flow needs. Scenario-conditional material — the
high-assurance profile and its addendum, the direction-delta output form,
composite/decomposition handling, blocked-design output — moves into
package references, each with an explicit when-to-read condition and timing;
the entry file keeps the workflow, guided defaults, sizing gate, output
contract, stop/route rules, and a reference loading table. Every preserved
obligation is mapped old→new; briefs produced by the skill remain
SIDE-002-conformant; behavior is unchanged.

## Authority and scope

| Item | Contract |
|---|---|
| Authority | [SIDE-003 plan](../SIDE-003/plan.md), "Body design and mandatory loading", "Delivery sequence" phase 4, "Measurement and decision rules" layer 2; [SIDE-002 brief](../SIDE-002/brief.md) (the brief presentation contract this skill must keep producing); owner adjustment (2026-11-03): figure the exact split places; clear when-to-read instructions are the acceptance center |
| Dependencies | SIDE-003.1–.6 complete (baseline + this skill's description final) |
| Allowed changes | This package's `SKILL.md` body, its `references/` (`task-sizing.yaml`, `task-artifact-layout.md`, `task-brief-template.md`, new files), its `evals/` inputs, its `tests/` expectations, owning cross-suite expectations that assert its text, and this skill's section in `docs/tasks/SIDE-003/rollout-results.md` |
| Read-only context | The SIDE-003.1 baseline and read graph; `skills/task-implementation-flow/task-brief-designer/tests/test_package_resources.py`, `tests/test_task_preparation_contracts.py`, `tests/test_task_flow_guides.py` |
| Out of scope | The `description` frontmatter (compressed in SIDE-003.3 — do not change); any behavior change to brief, sizing, decomposition, or artifact policy; renaming or moving the package; the `references/task-artifact-layout.md` path (task-verification-designer links it cross-package — keep the path stable); other skills; the active `.agents/` installation |
| Assumptions / unresolved | The exact conditional clusters are this leaf's design work; the always-loaded path (workflow steps 1–11, sizing gate, output contract) is near-universal and stays inline |

## Work and acceptance criteria

Required work:

1. Before any edit, freeze the obligation inventory in the rollout-results
   section: every workflow step, profile rule, sizing rule, output form,
   stop/route rule, and preservation rule in the current entry file, each
   with its current authority location.
2. Identify the actual conditional paths (high-assurance profile and
   addendum; direction-delta output; composite/decomposition contract and
   output; blocked-design output; finite-risk coverage contract). Do not
   invent profiles the skill lacks.
3. Extract conditional scenario clusters into `references/` files. Give every
   reference — new and existing — an explicit read condition and timing in the
   entry file (`task-sizing.yaml` before estimating; `task-artifact-layout.md`
   when creating or updating durable task artifacts; the template when
   assembling a durable brief; new references at their own triggers). Keep
   near-universal material inline.
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
  inventory; no workflow step, sizing gate, output form, or stop rule is
  lost or weakened; behavior-preservation fixtures pass unchanged
  before and after the edit; only the new loading-structure assertions
  (reference existence, explicit conditions, relocated obligations) reject
  the pre-edit layout and pass after; worked outputs remain SIDE-002-conformant.
- **AC-03:** Entry-only and per-route cumulative costs are recorded
  before/after; a route that did not shrink is explained, not hidden; the
  `references/task-artifact-layout.md` path and the description frontmatter
  are unchanged.

## Verification

| Evidence | Scenario and oracle | Command |
|---|---|---|
| Fail-first | Behavior-preservation fixtures pass unchanged against the pre-edit bytes; the new loading-structure assertions (reference existence, explicit conditions, relocated obligations) reject the pre-edit layout; in a disposable candidate, removing one required link or bypassing one route is detected by the relevant check | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-implementation-flow/task-brief-designer/tests -p "test_*.py"` |
| Targeted | Package-resource expectations (references resolve, conditions present); preparation-contract expectations for the designer/verification-designer pair; flow-guide expectations for this skill's routes | `… discover -s tests -p test_task_preparation_contracts.py`, `… -p test_task_flow_guides.py` |
| Owning suite | This package's own tests root (a `tools/verify.py` discovery root) | `python3 tools/verify.py` (this leaf's roots) |
| Broader gate | Aggregate gate and disposable-install reference resolution at SIDE-003.18; live behavioral qualification only with separately approved budget, else recorded pending | SIDE-003.18 |

## Execution

Status: `ready`; task kind: `executable`; guided profile.
Readiness route: standalone guided preflight after derived verification —
confirm the current assertion inventory and that SIDE-003.3's description for
this skill is final before edits.
Verification-design recommendation: separate — obligation-preservation
coverage across relocation and worked-output conformance need designed
scenarios; this skill governs every future brief, so regressions here
propagate.

```yaml
agent_tier: standard
reasoning: high
review: immediate
budget: 19 tool calls / 55 minutes / one-package restructuring with obligation map and closure tests
```

Sizing: `default@1`; estimate 17 implementation calls / 50 minutes;
confidence medium; triggered `max_agent_calls` and `max_duration_minutes`.
Decomposition override: `cannot_split_safely` — candidate boundary
(high-assurance extraction vs output-form extraction) rejected: one entry
file plus shared suites; both stages would re-edit the same workflow and
renegotiate the same loading table. Residual risk: a long single leaf,
mitigated by the pre-edit obligation inventory, staged commits, and the
immediate fresh review.

Stops: an obligation that cannot be preserved by extraction (stop; do not
delete it to shrink bytes); any behavior change to brief/sizing/artifact
policy (route back through the parent); profile drift in the active
installation (report, do not fix); missing live-eval budget (report
qualification pending).

Next action: derive `verification.md`, obtain a ready `preflight.md` through
standalone guided preflight, then implement.
Required follow-on: immediately after implementation or correction and any
applicable conditional stages, hand the completed bytes to a fresh independent
`task-review-discovery` call, and hand its report to a separate
`task-acceptance-review` decision.

Expected contract impact: none — no registry record declares this package's
authority; the task-flow artifact policy itself is unchanged.