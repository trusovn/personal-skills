# Task Brief: `T-003` — Close submission and correction routes

Status: `decomposed`

Task kind: `composite`

## Outcome

Human handoffs retain every obligation and current evidence through ordered
conditional stages and correction. Bounded maintainability review reports all
confirmed blockers without a finding cap or an enough-blockers early stop.

## Authority and scope

- Authority: [project-plan.md](../../project-plan.md), sections 1, 4–8, 10
  (`T-003`) and 11; `T-003` in [task-map.json](../../task-map.json).
- Stable refs: `CAP-002`; `FLOW-002/003`; consumes
  `ART-001/002/003/004/005/006/007/009`; produces
  `ART-004/005/006/007/009`; `IF-002/003/004/005/006`;
  `INV-003/004/005/006/008/011`.
- Scope: human FLOW-02/FLOW-05 handoffs, complete bounded maintainability
  findings, correction continuity, affected usage/profile guidance and local
  fixtures. Inspect the canonical installer in each source-skill change.
- Dependencies: completed/reviewed `T-001` and `T-002` contracts. Preflight must
  confirm applicability; this brief does not certify their current readiness.
  Current test ownership is recorded in
  [TEST-STAB-001.2 results](../TEST-STAB-001.2/results.md); the historical
  `test_review_discipline.py` command no longer names a current module.
- Excluded: orchestration/controller state, machine sidecars, automatic stage
  launches or advancement, a global correction counter, new shared enforcement
  infrastructure, T-004 drift/unborn work, T-005 agent qualification, active
  `.agents/` refresh, official-plan edits and historical-result/review edits.

## Direction trace

- Contribution: reliable human-coordinated review and correction under the
  existing authority, contextual rubric and role ownership.
- User-observable effect: the caller receives the first outstanding stage and
  full remaining route, without lost findings, stale acceptance or optional-fix
  loops. The supplied fixtures enable T-005's separate-call qualification.
- Why now: T-001 preparation and T-002 discovery/decision contracts supply the
  inputs; T-004 distribution and T-005 qualification consume the completed flow.
- Decisions used: plan section 1 settled decisions; sections 5–7 correction,
  contextual disposition and interfaces; section 10 T-003 integration boundary.
- New direction decisions required: None.

## Execution sizing

- Policy: `default@1`,
  `.agents/skills/task-implementation-flow/task-brief-designer/references/task-sizing.yaml`.
- Original estimated agent calls: 55. Implementation duration: 155 minutes.
- Intended execution profile: `standard / high`. Confidence: medium.
- Triggered rules: `max_agent_calls`, `max_duration_minutes`.
- Estimates cover focused discovery, source edits, task-owned fixtures/tests and
  local verification; exclude preparation, separate review, registry work and
  agent/model-budget qualification.

## Decomposition

| Child | Owned outcome / explicit handoff | Depends on | Brief |
|---|---|---|---|
| T-003.1 | Submission protocol with first outstanding stage and full conditional route | T-001, T-002 | [brief](../T-003.1/brief.md) |
| T-003.2 | Complete bounded maintainability findings and supplied blocker fixture | T-001, T-002 | [brief](../T-003.2/brief.md) |
| T-003.3 | Correction continuation, revision recovery and current evidence under .1's protocol | T-003.1 | [brief](../T-003.3/brief.md) |
| T-003.4 | Composed routes, source/profile guidance and disposable installed projection | T-003.1, T-003.2, T-003.3 | [brief](../T-003.4/brief.md) |

The boundaries are a submission protocol, a maintainability-report contract,
correction continuation and integration proof. Each output can be consumed and
checked independently. .1 owns the route fields; .3 extends them sequentially
in the shared implementer files. .2 owns maintainability policy and its fixture.
.4 owns final guide reconciliation and composition records. Child-local guide
edits stay limited to their own obligations. This avoids parallel edits to one
continuation contract and repeated whole-flow negotiation. The final child
owns proof that these independent outputs compose; a file/layer split would
not establish that proof. Estimated combined leaf work is 51 calls / 130
minutes, including integration, with additional separate-stage overhead.

## Coverage and closure

| Parent obligation | Owner / closure |
|---|---|
| P-01: Neither/either/both conditional stages; first outstanding stage; full remainder; independent submission stop | .1 protocol; .4 composition |
| P-02: All bounded confirmed maintainability blockers, including more than three; retain safe scope/budgets | .2; .4 installed projection |
| P-03: All finding/scenario IDs, unfinished rows, reasons/owners, influenced sibling surfaces and current correction evidence | .3; .4 continuation |
| P-04: Production/test/reference/clarification/evidence/authority distinctions; fresh applicable stages; actual-effect reference shortcut | .1 stage order; .3 recovery; .4 contrast |
| P-05: Coverage-gap revision under unchanged authority, retained IDs, obsolete-ready rejection, focused readiness and new evidence; changed requirements return to task design | .3; .4 handoff inputs |
| P-06: Stable dispositions, evidenced material new blockers, mixed-condition routes, discovery-owned aggregate gate; no global counter and preserved two-failed-fixes stop | .3; .4 composition |
| P-07: Synchronized affected source/profile guidance, current local tests and reusable qualification inputs with explicit unrun gaps | Every child locally; .4 final closure |

All leaves fit `default@1`; no override. The dependency graph is acyclic.
Shared ART-004 routing is owned by .1 then extended by .3; ART-005 completeness
by .2; ART-006/007 correction consumption by .3; ART-009 composition by .4.
All stable parent refs remain covered; no new registry is required.

## Handoff

Implement dependency-ready executable leaves only, after each leaf's derived
verification and ready preflight. Never launch this composite parent. Each leaf
must finish its own independent review route; .4 must establish integration
closure. T-005 retains actual agent-call behavioral qualification.
