# Task Brief: `T-004` — Repair and qualify development-profile distribution

Status: `decomposed`

Task kind: `composite`

## Outcome

Explicit installation works before the first commit. A read-only profile check
reports managed-content drift or check failure. Deliberate refresh restores a
match and preserves unmanaged state.

## Authority and scope

- Authority: [project-plan.md](../../project-plan.md), sections 1–2, 4–6,
  IF-007 in section 7, FLOW-004 in section 8, and T-004 in sections 10–11;
  `T-004` in [task-map.json](../../task-map.json). The request's “T-04” resolves
  to this stable plan ID.
- Stable refs: `CAP-003`, `FLOW-004`; consumes `ART-009/010`; produces
  `ART-009/010/011`; preserves `IF-007` and `INV-009`.
- Scope: SETUP-01/02 only; canonical installer, exercised workflow identity and
  availability boundaries, managed-profile comparison, focused local tests,
  affected distribution guidance and integration evidence.
- Depends on completed/reviewed `T-001`, `T-002`, `T-003` source contracts.
  Preflight confirms their current applicability; brief design does not certify
  dependency completion. Existing package/index entries supply discovery paths.
- Excluded: controller/runtime orchestration, full unborn evidence-collector
  lifecycle, fingerprint reframing, fabricated commits, retained active-run
  versions, generic package management, automatic refresh, active `.agents/`
  refresh, live/model-budget qualification, official-plan and historical edits.

## Direction trace

- Direction contribution: reliable human-coordinated distribution under the
  installer's existing narrow ownership boundary.
- User-observable effect: a maintainer can install into a genuine unborn repo,
  inspect drift without mutation, then explicitly refresh between invocations.
  This enables T-005 to qualify the installed skills and sibling helpers it calls.
- Why now: T-001–003 supply the completed source flow; the plan puts distribution
  before T-005's installed-flow qualification.
- Direction decisions used: plan section 1 settled decisions; section 2
  exclusions; `ART-009/010/011`, `IF-007`, `INV-009`, FLOW-004 and T-004's
  integration boundary. Exact check CLI/result and comparison code are local design.
- New direction decisions required: None.

## Execution sizing

- Sizing policy: `default@1`,
  `.agents/skills/task-implementation-flow/task-brief-designer/references/task-sizing.yaml`.
- Original estimated agent calls: 37. Original implementation duration: 95 minutes.
- Intended execution profile: `standard / high`. Estimate confidence: medium.
- Triggered limits: `max_agent_calls`, `max_duration_minutes`.
- Estimates cover implementation discovery, edits, task-owned tests and local
  verification; exclude preparation, independent review and T-005 role calls.

## Decomposition

| Child | Responsibility / owned output | Depends on | Brief |
|---|---|---|---|
| T-004.1 | Genuine unborn identity, availability and installation with committed/detached compatibility | T-001, T-002, T-003 | [brief](../T-004.1/brief.md) |
| T-004.2 | Explicit read-only managed-profile check and documented match/drift/failure interface | T-004.1 | [brief](../T-004.2/brief.md) |
| T-004.3 | Install → check → drift → explicit refresh → recheck proof, preservation and final guidance | T-004.1, T-004.2 | [brief](../T-004.3/brief.md) |

These are behavioral boundaries with consumable outputs: usable installed
identity, an explicit qualification interface, then lifecycle closure. .1 and
.2 may touch the installer/tests, so they are sequential; .2 consumes .1's
Git-state contract rather than renegotiating it. .3 consumes the documented
check and existing reinstall entry point. It owns composed proof and only
minimal refresh/preservation repairs. Splitting comparison by file family or
separating tests would repeat one oracle and force coordination back together.
The three leaves total 37 calls / 95 minutes; the benefit is bounded independent
verification and review, with preparation/review overhead outside that estimate.

## Coverage and closure

| Parent requirement | Owner / closure |
|---|---|
| P-01: Real unborn install and installed availability; committed/detached compatibility; non-unborn errors stay failures | .1; .3 lifecycle |
| P-02: Complete managed comparison; skill/reference/guide/helper/block drift, missing and extra managed files | .2; .3 composed drift |
| P-03: Match/drift/check failure are distinguishable; check writes nothing and ignores unmanaged files/text | .2; .3 snapshots |
| P-04: Explicit refresh restores match, removes stale managed bytes and preserves unmanaged bytes | .3 |
| P-05: Selection, profile guide, shared helpers, focused tests and READMEs stay synchronized; unchanged fingerprint framing and narrow ownership | Each leaf locally; .3 final reconciliation |
| P-06: Exact local evidence and installed identities enable T-005 without claiming collector lifecycle or agent-call qualification | .3 results |

All leaves fit `default@1`; no override. Dependencies are acyclic. .1 owns the
exercised ART-010 identity/availability repair; .2 owns ART-011 and its CLI;
.3 owns refresh closure and the final ART-009 guidance. No registry exists at
`docs/contracts`; no registry creation is required. Every stable parent ref is
preserved across these owners.

## Handoff

Prepare dependency-ready leaves only: derived `verification.md`, then ready
`preflight.md`, before implementation. Never launch this composite parent.
Each leaf must complete its independent review route; .3 must complete the
composed proof. T-005 retains installed skill-call behavioral qualification.
