# Task Brief: `T-002` — Separate discovery, decision and known-issue ownership

Status: `decomposed`

Task kind: `composite`

## Outcome

A standalone discovery call supplies current corroborated evidence. A separate
acceptance call admits it, decides every finding using the approved contextual
rubric, and routes accepted deferrals to the human coordinator. Both skills and
their references are available through the development-profile installer.

## Authority and scope

- Authority: [project-plan.md](../../project-plan.md), sections 1, 4–8, 10–12;
  `T-002` in [task-map.json](../../task-map.json). “T-02” in the request is
  interpreted as the plan's `T-002`.
- Stable refs: `CAP-002`; `FLOW-002/003`; consumes `ART-001/002/003/004/005/008/009`;
  produces `ART-006/007/008/009`; `IF-004/005/006`;
  `INV-001/004/005/006/007/011`.
- Scope: discovery package; acceptance skill/report/eval contracts; known-issue
  guidance and relevant preflight consumption; distribution and local fixtures.
- Excluded: `T-003`'s conditional-stage matrix and maintainability-cap removal;
  `T-004`'s unborn/drift work; `T-005`'s composed agent qualification; orchestration,
  machine sidecars, new shared enforcement tooling, active-profile refresh,
  portfolio decisions, official-plan edits and historical-review edits.
- Dependency: completed/reviewed `T-001` source contracts. Its final
  [T-001.4 brief](../T-001.4/brief.md) records acceptance; preflight confirms
  current applicability rather than relying on that label alone.

## Direction trace

- Contribution: reliable human-coordinated evidence, contextual decisions and
  complete continuation, with independent production/discovery/decision roles.
- User-observable effect: callers receive a supported disposition and an exact
  next owner, without routine issue prompts or repeated optional-fix loops.
  The installed contracts enable `T-005`'s actual separate-call proof.
- Why now: consumes `T-001` preparation/context and supplies review contracts
  needed by `T-003` correction routing and later installed qualification.
- Decisions used: plan section 1 settled decisions; sections 4–7 artifact
  ownership, rubric and interfaces; section 10 `T-002` integration boundary.
- New direction decisions required: None.

## Execution sizing

- Policy: `default@1`,
  `.agents/skills/task-implementation-flow/task-brief-designer/references/task-sizing.yaml`.
- Original estimated agent calls: 52. Duration: 140 minutes.
- Intended execution profile: `standard / high`. Confidence: medium.
- Triggered rules: `max_agent_calls`, `max_duration_minutes`.
- Estimates cover focused discovery, source changes, task-owned tests/fixtures
  and local implementation checks; exclude preparation, separate reviews,
  registry synchronization and agent/model-budget qualification.

## Decomposition

| Child | Owned outcome / handoff | Depends on | Brief |
|---|---|---|---|
| T-002.1 | ART-006 discovery contract, runnable probe fixtures and distribution of the new skill | T-001 | [brief](../T-002.1/brief.md) |
| T-002.2 | ART-007 evidence admission and decision-only acceptance boundary | T-002.1 | [brief](../T-002.2/brief.md) |
| T-002.3 | Contextual disposition and coordinator-owned ART-008 contract | T-002.2 | [brief](../T-002.3/brief.md) |
| T-002.4 | Source/profile composition, consumer handoff fixtures and installed projection proof | T-002.1, T-002.2, T-002.3 | [brief](../T-002.4/brief.md) |

The boundaries are evidence publication, evidence admission, contextual judgment,
and composed distribution. Each has an independently inspectable output and
owns its corresponding tests. Acceptance files are shared sequentially by .2
and .3; .2 establishes the admission interface before .3 extends disposition.
Guide edits are restricted to child-owned entries until .4 reconciles the full
route. This avoids renegotiating report fields across concurrent edits. Splitting
by files or separating all tests would not provide these stable handoffs.

## Coverage and closure

| Parent requirement | Owner / closure |
|---|---|
| P-01: Separate independent discovery and decision; narrow writes; numbered reports; distinct launch reasoning guidance | .1 discovery; .2 admission/decision; .4 composed route |
| P-02: Preserve complete current evidence, public/lifecycle/validator/process probes, stable findings and continuation | .1 evidence contract/fixtures; .2 admission; .4 preservation audit |
| P-03: ART-003 context informs probes; discovery owns justified aggregate gate, including correction | .1 gate/probe selection; .2 consumes record without duplication; .4 handoff setup |
| P-04: Explicit AC failure blocks despite green tests; passing ACs cannot excuse material operating/business/contract/refactoring risk | .2 authority/evidence admission; .3 contextual rubric |
| P-05: Mixed blocker/missing-proof precedence, every unfinished row and its separate owner retained | .2 ledger admission; .3 verdict precedence; .4 composition fixtures |
| P-06: Minor deferral, speculative observation, ordinary-unknown continuation and exceptional serious/costly-later escalation | .3 contrasting contexts, routine autonomy and stable dispositions |
| P-07: Coordinator records deferrals before advancement; relevant next preflight reassesses; optional links confer no portfolio authority | .3 record/consumer contract; .4 consumer fixtures |
| P-08: New discovery installs in its own change; synchronized manifest/guide/tests/docs and unmanaged preservation | .1 adds distribution; each child updates its entry; .4 final projection |

Shared outputs have one owner: .1 owns ART-006 and discovery installation
selection; .2 owns ART-007 admission/provenance; .3 owns its contextual decision
fields and ART-008 instructions; .4 owns final cross-stage guidance/local
composition. No child writes real known issues on behalf of a coordinator.

All four leaves fit the active sizing envelope without overrides. Dependencies
are acyclic and require completed/reviewed predecessor outputs. .4 is the final
executable integration child; the parent has no implementation or acceptance
stage. No current registry exists under `docs/contracts`; use implemented source
contracts and predecessor evidence, without inventing registry infrastructure.

## Handoff

Prepare dependency-ready `T-002.1`: derive `verification.md`, obtain ready
`preflight.md`, then implement and hand off to fresh independent review.
Never launch this parent for implementation. Each child must complete its own
preparation and review route. Local structural/runtime evidence does not close
`T-005`'s separately authorized actual agent-call qualification.
