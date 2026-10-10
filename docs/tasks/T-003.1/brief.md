# Task Brief: `T-003.1` — Name the complete ordered submission route

Status: `ready`

Task kind: `executable`

```yaml
agent_tier: standard
reasoning: high
review: immediate
budget: 14 tool calls / 35 minutes / 45k context
```

## Execution sizing

- Policy: `default@1`, `.agents/skills/task-implementation-flow/task-brief-designer/references/task-sizing.yaml`.
- Estimated agent calls: 14. Duration: 35 minutes. Confidence: medium.
- Intended profile: `standard / high`. Policy result: fits; triggered limits:
  none; decomposition override: none. Implementation work only.

## Readiness route

standalone guided preflight — confirm T-001/T-002 contracts and current test
selectors. Derive `verification.md`, then obtain ready `preflight.md`.

## Verification-design recommendation

separate — four conditional-stage combinations, already completed stages and
correction applicability can produce plausible stage-skipping handoffs.
Existing implementer fixture setup and guide tests are believed available;
no new harness or runtime routing mechanism is needed.

## Outcome and direction trace

Every required-review submission names the first outstanding applicable stage
and complete remainder, then ends the implementer invocation.

- Contribution: `CAP-002`, `FLOW-002/003`, `ART-004/005/009`, `IF-002/003`;
  preserve `IF-004/005/006`, `INV-003/004/005/006/008/011`.
- Effect: a human caller can launch required stages without inferring omitted
  conditional obligations. Enables .3 correction continuation and .4/T-005 proof.
- Why now: consumes T-001 entry and T-002 separate discovery/decision contracts.
- Decisions: plan sections 1, 5, 7 and 10 T-003; parent P-01/P-04/P-07.
- New direction decisions required: None.

## Authority and scope

- Authority: [plan](../../project-plan.md), cited sections and section 11;
  `T-003` [task-map entry](../../task-map.json); [parent](../T-003/brief.md).
- Repository: `/Users/mtrusov/work/skill-sources/personal-skills`.
- Dependencies: completed/reviewed T-001 and T-002. Consumes
  `ART-001/002/003/004/005/006/007/009`; produces ART-004 routing and ART-009.
- Allowed: source `skills/task-implementation-flow/bounded-task-implementer/`
  skill/evals/fixture; its route wording in `skills/task-implementation-flow/README.md`,
  `skills/README.md`, root `README.md`; focused existing
  `tests/test_bounded_task_implementer.py` and `tests/test_task_flow_guides.py`.
  Inspect `scripts/install_development_skills.py` selection/guide/helpers;
  change only a stale declaration caused by this task.
- Read-only: conditional-stage/discovery/decision skills, existing fixture
  helpers and T-001/T-002 packages. Current `.agents/` copies are not edit targets.
- Excluded: maintainability cap, .3 recovery policy, new output schema or stage
  executor, installer ownership changes, plan/history edits and agent eval runs.
- Assumption: current contracts support these human routes; preflight confirms
  interfaces. No unresolved product decision.

## Work and acceptance criteria

1. Repair initial and correction handoff templates, provenance instructions and
   output guidance where they hard-code discovery as the next stage.
2. Extend existing route cases with complete supplied preparation and stage
   state; retain existing preparation, lifecycle and provenance coverage.

- **AC-01:** For neither conditional stage, route discovery → separate fresh
  acceptance. Maintainability only routes required architecture gate/fresh
  maintainability → discovery → acceptance; registry only routes updater →
  discovery → acceptance; both route architecture/maintainability → registry
  updater → discovery → acceptance. Include a gate only when required by policy.
- **AC-02:** Name the first outstanding stage and all remaining obligations;
  completed stages count only with applicable current evidence. Production
  correction re-enters affected conditional stages before fresh discovery and
  acceptance. Do not infer a tests-only exception absent repository authority.
- **AC-03:** `review: immediate` ends at `READY_FOR_REVIEW`; naming routes does
  not launch reviewers or allow same-session acceptance. Carry preparation/context
  references, all scenario evidence or incomplete reasons/owners, and full
  remaining obligations. Preserve no-review/milestone semantics.

### Finite-risk coverage contract

| Invariant | Material dimensions/cases | Decisive oracle/boundary | Implementation evidence | Independent review probe | Gate owner |
|---|---|---|---|---|---|
| R-01 / INV-008 | Neither, maintainability only, registry only, both; outstanding versus currently satisfied stage; initial submission → production correction → next submission | Supplied policy/stage evidence maps to exact first owner and ordered full remainder in public handoff guidance | Existing fixture extended with all four policies, current/stale conditional evidence and expected routes; fail-first contract checks reject hard-coded discovery-next | Trace the both-stage correction with stale prior acceptance and a current completed conditional stage | .1 implementer: focused/owning local checks; .4: composition; T-005: actual emitted routes |
| R-02 / INV-004/005 | Required immediate review; milestone/no-review; incomplete scenario row | Submission ends with truthful evidence/next owner, without reviewer invocation or verdict | Supplied executable preparation and failed/unchecked row retain separate implementation claims | Inspect whether a listed next stage was treated as already accepted | Fresh reviewer: independent corroboration; T-005: observed role stop |

## Verification

- Run fail-first focused changed cases, then sequential owning gates from root:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_bounded_task_implementer.py`
  and `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_task_flow_guides.py`.
  Derived verification resolves narrower selectors first.
- Reuse existing fixture setup; assertions on guidance prove contract structure,
  not emitted agent handoffs. Preserve explicit T-005 unrun behavior gaps.
- No broad/network/model gate here; .4 owns composed local/profile checks.

## Expected contract impact

- Change ART-004 / IF-002 ordered human handoff; preserve IF-003–006 ownership.
- Dependencies: T-001 preparation and T-002 discovery/decision; no current
  `docs/contracts` registry. Do not create one for this task.
- Delta: first outstanding conditional stage and full route replace unconditional
  discovery-next guidance; .3 consumes these fields without a new machine schema.

## Stops and handoff

Stop for conflicting stage authority, user-work overlap, material scope growth,
unsafe permissions or unavailable decisive capability. Budget is a soft checkpoint.
Next: derived verification → ready standalone preflight → bounded implementation.
Required follow-on: immediately after implementation or correction, hand completed
bytes to a fresh independent acceptance reviewer through the first outstanding
conditional stage, fresh discovery and separate acceptance. End the implementer
invocation. Supply .3 with route fields and .4 with reusable policy/stage cases.
