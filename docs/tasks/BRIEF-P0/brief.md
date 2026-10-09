# Change task: BRIEF-P0 — Check boundary quality before decomposition

Status: `ready`
Task kind: `executable`

Update the source `task-brief-designer` so future planning chooses coherent,
economical task boundaries rather than splitting automatically on sizing alone.
Implement this change as one task in one pass; do not decompose it.

## Authority and constraints

- Authority: user request of 2026-10-09 to apply the supplied report's three P0
  recommendations to **task-brief-designer**, corrected from implementer;
  document a local change brief first and keep implementation in one pass.
- This brief captures the approved report scope: boundary-quality check,
  economical no-split choice, and shared change surfaces/contract churn.
- User-authorized local route: inline verification and implementer
  self-preflight, followed by a later independent review. No full formal artifact
  chain is required for this maintenance task. This exception does not change
  the normal packaged preparation rules established by task 01.
- Preserve [project-plan.md](../../project-plan.md),
  [task-map.json](../../task-map.json), plan review, all T-001 packages/results,
  and their requirements. The user reports task 01 implemented; do not reopen it.
- Plan sections 10 and 12 permit task-local splitting while preserving approved
  relationships and cross-task contracts. This maintenance enables better
  boundaries for the next planning section; it is not T-002 implementation.
- New direction decisions required: None.

## Scope

Primary target: `skills/task-implementation-flow/task-brief-designer/SKILL.md`.
Synchronize only affected sizing/template references, existing eval expectations,
focused package tests, and the decomposition explanation in the flow README.
Inspect `scripts/install_development_skills.py`, profile guidance, focused
installer tests, and installation documentation; change them only if this work
changes a distribution requirement. Keep existing installer ownership narrow.

Do not change `bounded-task-implementer`, other stage contracts, orchestration,
numeric thresholds, launch profiles, or mandatory preparation/review rules.
Do not add progressive child elaboration, a scoring engine, a new schema or
shared harness, threshold calibration, or an execution-cost telemetry model.
No broad adversarial-eval expansion, live model runs, or installation refresh is
required in this implementation pass.

## Acceptance criteria

- **AC-01 — Boundary decision:** Before committing to a split, assess clear
  ownership, stable handoffs, independent implementation and verification,
  shared edit/test surfaces, likely contract renegotiation, and net delivery
  benefit. Reject a poor partition by keeping coherent work together or choosing
  a better boundary. A component/layer split alone is not sufficient evidence.
- **AC-02 — Economical no-split:** Existing numeric and execution-profile triggers
  require evaluation, not automatic decomposition. A triggered task may remain
  executable when concrete coupling or coordination/rework costs favor keeping
  it whole, even without strict atomicity. Record the triggered rules, candidate
  boundary considered, concrete reason, and residual execution risk. Mere
  preference or high reasoning alone is insufficient. Respect explicit hard
  authority limits and the active policy's override permission.
- **AC-03 — Useful splitting:** Prefer a split when settled boundaries produce
  independently verifiable outcomes with cheaper coordination. Preserve complete
  child briefs, recursive estimation, AC coverage, one owning child per shared
  output, acyclic dependencies, stable plan IDs, and integration proof when needed.
  Composite parents remain non-executable; this change does not force no-split.
- **AC-04 — Consistent policy:** Align the skill, sizing policy wording/semantics,
  brief template, gap-check guidance, flow documentation, and existing eval
  expectations so none still demands automatic splitting for every trigger or
  limits no-split solely to atomicity. Keep numeric maxima and exclusive boundary
  comparisons unchanged. Prefer existing override fields; do not introduce a
  durable schema. Preserve task 01's preparation and readiness contracts.
- **AC-05 — Truthful handoff:** Report changed source paths, AC evidence, local
  checks, unrun behavioral probes, and installed-copy drift. Identify the existing
  installer command needed to refresh the project-local profile between
  invocations before the next planning task; source edits alone do not update an
  installed copy or an active session. Hand off the completed diff and this brief
  to a fresh independent reviewer, without self-acceptance.

## Verification

Use these contrasts to inspect the decision procedure and later corroborate
behavior. They are reviewer inputs/oracles, not claims that model runs occurred.

| Case | Supplied facts | Expected decision |
| --- | --- | --- |
| Coupled oversized work | 20 calls, 50 minutes, standard/medium; parsing and persistence both determine an unsettled normalized representation; each proposed child would change it and the same integration tests. | Reject that partition; justify a whole task or propose a stable alternative, retaining AC coverage and execution risk. |
| Reasoning trigger | 12 calls, 35 minutes, strong/high; one bounded reconciliation invariant, same state transition and tests; the proposed validation/persistence split needs mutual design changes. | Evaluate the profile trigger and permit reasoned no-split; high reasoning alone is not the reason. |
| Beneficial split | 24 calls, 65 minutes, standard/medium; two behavioral outcomes with separate owners/tests and a settled handoff; both leaves fit and the coordination cost is low. | Split with explicit ownership/dependencies and any required integration proof. |
| Exact limits | 15 calls, 40 minutes, strong/medium; one coherent outcome. | Numeric equality fits; strong/medium does not match strong/high. |

Run local checks sequentially:

1. Targeted package tests:
   `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-implementation-flow/task-brief-designer/tests -p 'test_package_resources.py'`.
2. If distribution changes, run the focused installer tests:
   `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_install_development_skills.py'`.
3. Inspect the final scoped diff and run `git diff --check`; confirm protected
   plan/task-01 files have no task-owned changes.

Text/configuration checks prove policy consistency, not agent compliance.
Behavioral skill probes require separate authorization for model-budget use;
record them as unrun when that authorization is absent. A later reviewer must
distinguish policy acceptance from measured behavioral effectiveness.

## Execution and handoff

```yaml
agent_tier: standard
reasoning: medium
review: immediate
budget: 15 tool calls / 40 minutes / focused context
```

Sizing: default policy v1; estimated 12 implementation calls / 35 minutes,
medium confidence; standard/medium; fits; no triggered limits or override.
Verification design: inline. Readiness: implementer self-preflight under the
user's local-flow exception. The estimate excludes independent review and live
model evaluation.

Expected contract impact: change the source designer's decomposition decision
policy; preserve existing task-package and project-plan contracts.

Stop for ambiguous authority, user-work overlap, unsafe permissions, or scope
expansion. If the single pass cannot finish safely, report partial work rather
than inventing child tasks. Next: implement this task, then end the invocation
with the scoped diff and evidence for a fresh independent review against this
brief. Keep any durable review in a separate numbered report.
