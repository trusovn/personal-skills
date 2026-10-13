# Task Brief: `T-005.2` — Exercise preparation and readiness recovery

Status: `ready`

Task kind: `executable`

```yaml
agent_tier: standard
reasoning: high
review: immediate
budget: 15 tool calls / 40 minutes / 50k context
```

## Outcome and direction trace

Record whether actual installed preparation outputs reach valid implementation
entry and whether reasoned scenario revision recovers readiness without reusing
obsolete approval or changing requirements.

- Direction contribution: FLOW-001/003/005, IF-001/002/004/005/008,
  INV-001/002/003/005/010/011; consumes ART-001/002/003/004 and produces ART-012 inputs.
- User-observable effect: evidence distinguishes valid entry/recovery from an
  owned refusal and enables T-005.5's correction closure.
- Why now: T-005.1 supplies qualified copies and reproducible inputs.
- Direction decisions used: plan settled decisions, FLOW-001/003 and section 11.
- New direction decisions required: None.

## Authority and scope

- Authority: [project-plan.md](../../project-plan.md), sections 8, 10–11;
  [parent brief](../T-005/brief.md), evidence rules and P-02.
- Repository: `/Users/mtrusov/work/skill-sources/personal-skills`; dependency: T-005.1.
- Allowed: `docs/tasks/T-005.2/results.md`, `evidence/` and missing task-local
  case adapters in this package; disposable fixture files within supplied authority.
- Read-only inputs: T-005.1 `fixtures.md`/receipts; verification-designer
  `preparation-routes`, `coverage-revision`, `coverage-closure`,
  `verification-conflicts`, `integration-leaf`; preflight `readiness-cases`,
  `revision-recovery`, `freshness-change`; implementer `entry-cases` setup/evals.
  Preserve `INV-CASE-05/19–24`, `REV-01`, `CCR-07` and INT-FLOW-001 I-04/I-05.
- Excluded: source-policy fixes, broader system verification strategy, active
  installation refresh, new runner, master-plan/history edits.
- UNKNOWN: authorized role-call method/budget and current fixture paths. Without
  that execution permission, produce setup and explicit unrun records only.

## Execution sizing

- Policy: `default@1`; calls: 15; duration: 40 minutes; confidence: medium.
- Intended profile: `standard / high`; policy result: `fits` (equality fits).
- Triggered limits: none. Decomposition override: none. Estimate is one bounded
  composed attempt plus reused controls; a larger campaign needs a new checkpoint.

## Readiness route

Standalone guided preflight after derived verification — confirm current source
qualification, readiness inputs and authorization envelope for proposed calls.

## Verification-design recommendation

Separate — readiness revisions, missing capability versus future tests and
authority changes have distinct owners. Derived `verification.md`, then ready
`preflight.md`, are mandatory before implementation.

## Work and acceptance criteria

1. Supply a minimal executable package whose verification designer produces
   actual `verification.md`; preflight consumes it and produces actual readiness;
   implementer consumes those exact references and submits current scenario proof.
2. Carry forward the existing refusal/direct-edit controls and their evidence.
   Under unchanged authority, exercise a coverage gap, reasoned revision with
   retained IDs, focused preflight and current revised evidence/new decision.
   Contrast changed requirements returning to task design.

- **AC-01:** Each claimed preparation handoff points to actual producer bytes
  and a separate consumer call; implementation cannot precede derived verification
  and ready preflight. A compact documentation package has the same entry rule.
- **AC-02:** Existing omitted-AC, unjustified-scenario, weak-oracle, missing-fixture/
  capability versus valid future-test, stale-authority/permission versus expected
  effects, composite/blocked/legacy and compact direct-edit cases remain mapped
  to evidence or explicit gaps. Integration-leaf permission does not authorize
  composite-parent implementation or invented sibling requirements.
- **AC-03:** In the recovery chain, original IDs and revision reason survive;
  affected obsolete readiness is rejected both before and after focused recovery.
  New readiness precedes current revised proof and a separate new decision.
  Changed requirements route to task design; expected report effects do not.
- **AC-04:** Raw calls, permissions, identities and case results are retained;
  unrun calls stay unrun and no staged readiness is called an observed role output.

### Finite-risk coverage contract

| Invariant | Material dimensions/cases | Decisive oracle/boundary | Implementation evidence | Independent review probe | Gate owner |
|---|---|---|---|---|---|
| P-01 / INV-001/002/003 | Package → derived design → ready → entry; compact doc package; direct edit; composite/blocked/legacy refusal | Actual files and entry output honor package status/authority without invented requirements | Existing setup/control evidence; authorized separate producing/consuming calls or explicit gaps | Trace one readiness reference to bytes actually read by implementation; inspect refusal control | Qualification implementer: case evidence; fixture discovery: any justified aggregate; leaf discovery: changed-owner aggregate |
| P-02 / INV-003/005/008 | Coverage gap → retained-ID revision → obsolete-ready rejection → focused ready → revised proof/decision; reintroduced obsolete ready; changed requirements | Current revision/ID/decision chain rejects stale approval despite a later passing proof | `revision-recovery`/coverage fixtures with actual role outputs | Substitute old readiness in recovered case; confirm rejection/owner and preserved prior artifacts | Same owners; acceptance never duplicates discovery aggregate |

## Verification

Reuse T-005.1 inputs and run the focused staging/probes for selected cases first.
Nearest owners, only when affected evidence needs renewal:
`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p
test_task_preparation_contracts.py`, then `test_task_preflight.py` and
`test_bounded_task_implementer.py` sequentially as needed. Role calls require
separate concrete authorization; preflight resolves their entry point, isolated
workspace and raw-output capture. Wrong-ready and wrong-authority contrasts must
reject for the intended reason. Check `git diff --check` and protected state.
Fresh discovery owns a justified changed-owner aggregate after targeted rows
are clean; acceptance consumes it. No default full-suite/live/model gate.

## Expected contract impact

None: preserve ART-001/002/003/004 and preparation interfaces; add case-local
ART-012 evidence. No registry exists or is introduced.

## Stops and handoff

Apply parent evidence rules. Stop for authority/scope conflict, unsafe permission,
unavailable decisive capability or required new shared mechanism. Unapproved evals
become explicit gaps. Preserve user work; budget is a soft checkpoint.
Next: verification design → standalone guided preflight → bounded implementation.
Immediately after implementation/correction and applicable conditional stages,
fresh independent `task-review-discovery` receives completed bytes; a separate
`task-acceptance-review` receives its report. End the implementer invocation.
Reviewed recovery evidence feeds T-005.5 and the final audit.
