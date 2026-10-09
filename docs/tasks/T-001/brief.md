# Task Brief: `T-001` — Make packaged-task preparation binding

Status: `decomposed`

Task kind: `composite`

## Outcome

Executable task packages require a separate verification design and a current
ready preflight before implementation. The implementer checks entry validity and
maps scenarios to current evidence. Small clear direct edits keep compact checks.

## Authority and scope

- Authority: [project-plan.md](../../project-plan.md), sections 1, 4–8, 10–11,
  and `T-001` in [task-map.json](../../task-map.json).
- Relevant refs: `CAP-001`; `FLOW-001`, `FLOW-003`; consumes `ART-001`,
  `ART-008`, `ART-009`; produces `ART-002`, `ART-003`, `ART-004`, `ART-009`;
  `IF-001`, `IF-002`; `INV-001/002/003/005/007/011`.
- Scope: source brief/layout, verification, preflight/packet and implementer
  entry contracts; their local tests/eval fixtures; affected profile guidance
  and installation projection. No production executor is added.
- Excluded: discovery/acceptance redesign (`T-002`), correction-stage routing
  (`T-003`), unborn install/drift checks (`T-004`), composed agent qualification
  (`T-005`), orchestration, shared enforcement infrastructure and active-session
  refresh. Do not edit official plans or historical reviews.

## Direction trace

- Contribution: binding preparation under human coordination, without a new executor.
- User-observable effect: package callers receive a valid entry or a named
  readiness/authority blocker; direct-edit callers retain a compact route.
  This enables the later installed preparation-to-implementation proof in `T-005`.
- Why now: `T-001` has no plan dependency and supplies preparation contracts
  consumed by `T-002`, `T-003` and final qualification.
- Decisions used: plan section 1, Authoritative inputs and Settled decisions;
  sections 5–7, readiness/context/authority rules; section 10, `T-001` boundary.
- New direction decisions required: None.

## Execution sizing

- Policy: `default@1`, from
  `.agents/skills/task-brief-designer/references/task-sizing.yaml`.
- Original estimated agent calls: 42.
- Original estimated implementation duration: 110 minutes.
- Original intended execution profile: `standard / high`.
- Confidence: medium; estimates include focused discovery, source edits,
  task-owned fixtures/tests and local implementation verification only.
- Triggered rules: `max_agent_calls`, `max_duration_minutes`.

## Decomposition

| Child | Responsibility / owned output | Depends on | Brief |
|---|---|---|---|
| T-001.1 | Package preparation and derived verification contract, ART-001/002 | None | [brief](../T-001.1/brief.md) |
| T-001.2 | Durable compact readiness/context and revision recovery, ART-003 | T-001.1 | [brief](../T-001.2/brief.md) |
| T-001.3 | Implementation entry validation and evidence submission, ART-004 | T-001.1, T-001.2 | [brief](../T-001.3/brief.md) |
| T-001.4 | Source/profile guidance composition and installed projection proof, ART-009 | T-001.1, T-001.2, T-001.3 | [brief](../T-001.4/brief.md) |

## Coverage and closure

| Parent requirement | Owning child / proof |
|---|---|
| P-01: Packaged executable leaves take separate verification then ready preflight; composite/blocked/legacy inputs cannot bypass entry | .1 specifies the route; .2 and .3 enforce their skill entry contracts; .4 checks composed guidance/projection |
| P-02: Brief authority is normative; every AC and scenario has justified coverage, stable identity and a decisive oracle | .1 owns design; .2 checks coverage/readiness; .3 submits current scenario evidence |
| P-03: Future tests are normal; absent indispensable capability blocks | .2 owns readiness distinction; .3 respects it |
| P-04: Material authority/dependency/ownership/permission/capability changes require readiness reconsideration; expected implementation/report effects do not | .2 owns decision; .3 checks applicability without broad rediscovery |
| P-05: Reasoned scenario revisions retain IDs and require focused renewed readiness under unchanged authority; requirement changes return to task design | .1 owns revision contract; .2 owns renewed readiness; .3 rejects obsolete entry |
| P-06: Relevant known issues and compact decision context pass through preflight; ordinary unknowns are recorded without routine prompts or invented policy | .2 owns context; .3 carries its reference in submission |
| P-07: Direct edits remain compact; guided packages do not acquire high-assurance digests, machine sidecars or controller contracts | All children preserve the boundary; .4 checks distribution consistency |
| P-08: Source and affected installation/usage guidance remain synchronized | Each source child owns its stage-specific guidance; .4 owns final cross-stage overview and installed proof |

Source-profile ownership is split by stage: .1 owns designer/verification sources
and their guide entries; .2 owns preflight/packet and its guide entry; .3 owns
implementer and its guide entry; .4 owns cross-stage overview and installer
regressions. No child introduces a new shared helper. The final executable child
owns local composition proof. Actual separate skill-call behavior remains the
explicit `T-005` obligation; structural checks cannot satisfy it.

All four leaves fit the active sizing policy without overrides. Their dependency
graph is acyclic; each consumes only source contracts supplied by earlier leaves
or existing baseline contracts. No known-issues file is required before a deferral
exists. No current contract registry was found under `docs/contracts`.

## Handoff

Start with executable `T-001.1`. Never launch this composite parent for
implementation. Every leaf must complete its own preparation, implementation
and fresh review route; .4 closes local composition. Do not mark `T-005` behavior
qualified from these leaves' local tests.
