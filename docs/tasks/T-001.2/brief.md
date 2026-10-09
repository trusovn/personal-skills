# Task Brief: `T-001.2` — Own compact packaged readiness and revision recovery

Status: `ready`

Task kind: `executable`

```yaml
agent_tier: standard
reasoning: high
review: immediate
budget: 14 tool calls / 38 minutes / 50k context
```

## Execution sizing

- Policy: `default@1`, `.agents/skills/task-brief-designer/references/task-sizing.yaml`.
- Estimated agent calls: 14. Estimated implementation duration: 38 minutes.
- Confidence: medium. Intended profile: `standard / high`.
- Policy result: fits. Triggered limits: none. Decomposition override: none.
- Covers implementation work only, including local fixtures/tests and checks.

## Readiness route

standalone guided preflight — confirm .1's source contract, readiness fixture
oracles and bounded profile edits. Separate verification and durable compact
preflight are required for this package by plan section 1, even when routine.

## Verification-design recommendation

separate — future tests versus absent capability, context and stale/revised
readiness have distinct failure semantics. Required by the packaged-stage rule.

## Outcome and direction trace

Preflight callers receive durable compact ready/blocked evidence bound to the
brief, scope and verification revision, with relevant context and concrete
capability/permission/ownership conclusions. This enables the entry check in .3
and `T-005`'s actual preparation-to-implementation handoff.

- Authority: [project-plan.md](../../project-plan.md), sections 1, 4–7, 10–11;
  `T-001` in [task-map.json](../../task-map.json);
  parent [T-001](../T-001/brief.md), P-01/02/03/04/05/06/07/08.
- Contribution: `FLOW-001/003`, `IF-001`, `INV-001/002/003/005/007/011`.
- Why now: consumes [T-001.1](../T-001.1/brief.md)'s packaged verification contract.
- Decisions used: plan section 5 invalidation/revision rules and section 6 compact
  context, relevant known issues and ordinary uncertainty; section 10 T-001 boundary.
- New direction decisions required: None.

## Authority and scope

- Repository: `/Users/mtrusov/work/skill-sources/personal-skills`.
- Depends on completed/reviewed `T-001.1`; consumes `ART-001/002/008/009`;
  produces the `ART-003` source contract and its `ART-009` slice.
- Allowed: `skills/task-implementation-flow/task-preflight/`, including packet
  reference and existing eval definitions/setup; stage-specific preflight tests
  in the flow's package test area when needed. Update preflight-specific guide
  entries in `skills/README.md`, flow README and root README.
- Inspect canonical installer selection, guide and shared-file constants in the
  same change; synchronize a required dependency now if one changes. No new
  helper or selected skill is authorized or expected.
- Read-only: .1 sources, implementer, official plans/review and installed `.agents/`.
- Excluded: broad rediscovery, behavior implementation, deferral tracking or rubric
  redesign, machine sidecars, shared harness and high-assurance fingerprint redesign.
- Unresolved decisions: none. Missing known-issues file means no recorded deferrals,
  not a preparation blocker. Focused new command names remain UNKNOWN for preflight.

## Work and acceptance criteria

1. Require packaged derived verification and produce canonical `preflight.md`
   in guided mode; retain compact direct-request and strict high-assurance routes.
2. Specify complete readiness/context and focused revision recovery; update
   supplied skill-local eval inputs and focused source checks.

- **AC-01:** Packaged readiness checks every material AC/scenario and its authority
  relationship, setup, decisive boundary, command feasibility and required
  dependencies/permissions/ownership. Missing or mismatched verification cannot
  produce ready. Readiness does not claim that future behavior already passed.
- **AC-02:** A task-owned future test may be absent while readiness is ready if
  its fixture/tool/boundary is feasible in scope. An indispensable unavailable
  capability blocks with evidence, owner and smallest route; it is not silently
  assigned to implementation. Existing high-assurance freshness checks remain strict.
- **AC-03:** Durable compact readiness identifies brief/scope/scenario revision,
  commands/oracles and referenced decision context: intended use/operating envelope,
  important consequences, relevant priorities/consumers/planned maintenance,
  mitigations and unknowns. Reassess relevant known issues only; ordinary unknowns
  are stated assumptions, not automatic blockers or routine questions. Preserve
  the plan's serious-delay/costly-later exception without inventing business policy.
- **AC-04:** Under unchanged authority, initial ready revision → reasoned scenario
  revision → focused new preflight rejects affected obsolete readiness and records
  a current decision. Material authority/prerequisite/ownership/permission/capability
  changes require reconsideration; expected implementation/report changes alone
  do not force full rediscovery. Requirement changes return to task design.
- **AC-05:** Packaged guided output is compact and durable; a small clear direct
  request can still return inline readiness. Do not require digests, a tracker,
  machine schema or instrumentation merely because a package exists. Guidance
  and supplied fixture prompts agree with the changed contract.

### Finite-risk coverage contract

| Invariant | Material dimensions/cases | Decisive oracle/boundary | Implementation evidence | Independent review probe | Gate owner |
|---|---|---|---|---|---|
| R-01 / INV-001/002/003: coverage and capability determine ready | Valid verification; omitted AC; unjustified scenario; weak oracle; absent future test with feasible setup; absent indispensable capability; wrong source brief | Source readiness contract plus actual supplied Git/authority/fixture inputs; later invocation must distinguish ready from owned blocker | Focused source regression and disposable fixture setup audit, preserving negative states | Compare future-test and missing-capability cases with otherwise identical readiness inputs | Implementer: targeted/package suite; T-005: actual role-call oracle |
| R-02 / INV-003: readiness is current without rediscovery | Initial ready → expected task/report effect; material authority/dependency/ownership/permission/capability change; coverage revision retaining IDs → focused readiness; requirement change | Revision/source references and explicit routing in readiness contract/fixtures; preserve non-artifact files | Fixtures supply both readiness versions and changed facts; source checks reject indiscriminate staleness | Challenge reuse of obsolete readiness after a newly added scenario | Implementer: targeted/package suite; .4: projection gate |
| R-03 / INV-007/011: compact context neither invents facts nor waives obligations | Relevant known issue; unrelated known issue; no recorded issue; ordinary unknown; unresolved serious-delay/costly-later uncertainty | Referenced context and ownership rules in source and fixture expected outputs | Supply realistic context/issue inputs; preserve uncertainty and explicit next owner | Check that ordinary missing business detail cannot erase a required proof row | Implementer: targeted; T-005: authorized contrasting-context calls |

## Verification

- Fail-first: focused source checks reject optional packaged verification/inline-only
  readiness and missing capability/revision/context distinctions.
- Targeted: preflight resolves exact new test and safe disposable fixture commands.
  Existing setup supports `EVAL_WORK_ROOT`; preserve fixture inputs and test
  executable local prerequisites without claiming semantic preflight behavior.
- Owning suite: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-implementation-flow/task-brief-designer/tests -p test_package_resources.py`
  from repo root, after targeted checks pass.
- .4 owns the broader local projection gate after composition; no full repo suite.
  Separately authorized agent calls belong to `T-005`; record unrun behavior proof.

## Expected contract impact

- Materialize/change `ART-003/009`, `IF-001`, `INV-003/007/011`; preserve
  `ART-001/002/008`, `INV-001/002/005`, `FLOW-001/003` and high-assurance checks.
- Dependencies: .1 source contract, existing preflight packet/eval fixtures and
  current known-issue input when present; no current `docs/contracts` registry.
- Durable delta: preflight owns compact package readiness and context, with
  explicit scenario revision and material-fact applicability. No new context artifact.

## Stops and handoff

Stop for ambiguous authority, user-work overlap, unsafe permission, widened scope
or missing decisive capability; return to its owner. Preserve user work and existing
strict freshness. Budget is a soft checkpoint.
Next: separate verification design, standalone guided preflight, then bounded
implementation once .1 is complete. Required follow-on: immediately after
implementation or correction, hand completed bytes to a fresh independent
acceptance reviewer, preserving applicable prior conditional stages; end the
implementer invocation. Its ready/context contract feeds `T-001.3`.
