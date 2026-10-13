# Task Brief: `T-005.6` — Publish audited standalone qualification results

Status: `ready`

Task kind: `executable`

```yaml
agent_tier: standard
reasoning: medium
review: immediate
budget: 12 tool calls / 30 minutes / 45k context
```

## Outcome and direction trace

Publish one new ART-012 report beside the dated proposal that reconciles current
fixture/setup evidence, actual composed role results and every remaining gap.

- Direction contribution: CAP-004, FLOW-005, IF-008, INV-010 and exercised
  INV-001–011; consumes ART-001–011 observations, produces ART-012.
- User-observable effect: the maintainer can reproduce each qualification claim
  and see whether required installed behavior remains unqualified.
- Why now: .1–.5 own the setup and composed observations this audit consumes.
- Direction decisions used: plan ART-012, FLOW-005, T-005 and section 11's
  separation of structural, local runtime and semantic role evidence.
- New direction decisions required: None.

## Authority and scope

- Authority: [project-plan.md](../../project-plan.md), sections 4, 8, 10–11;
  [parent brief](../T-005/brief.md), evidence rules and P-01–P-07 closure.
- Repository: `/Users/mtrusov/work/skill-sources/personal-skills`.
- Dependencies: reviewed T-005.1–.5 outputs. Explicit unrun observations are
  consumable limitations, never behavioral passes or fixture advancement.
- Allowed: `docs/tasks/T-005.6/results.md`/`evidence/` and the new
  `skills/task-implementation-flow/docs/standalone-policy-qualification-results-T-005.md`.
- Read-only: all upstream fixture inventories/raw evidence/results/reviews;
  official plans, dated proposal, installed receipts and current source identities.
- Excluded: rewriting the proposal/plans/old history; role evals or new production
  repairs; source/profile refresh; runtime orchestration state or automatic release.
- UNKNOWN: downstream evidence completeness/currentness. Evaluate it from the
  submitted artifacts; do not invent passing results or silently reuse stale proof.

## Execution sizing

- Policy: `default@1`; calls: 12; duration: 30 minutes; confidence: medium.
- Intended profile: `standard / medium`; result: `fits`; triggered limits: none.
- Decomposition override: none. Audit reuses current receipts; it is not a new eval campaign.

## Readiness route

Standalone guided preflight after derived verification — confirm reviewed child
outputs, final report path ownership and current evidence identities.

## Verification-design recommendation

Separate — a complete-looking report can conceal staged outputs, stale identity
or an unrun transition. Derived `verification.md`, then ready `preflight.md`, are required.

## Work and acceptance criteria

1. Reconcile P-01–P-07 and inherited case IDs against child evidence. Audit actual
   producer/consumer links, preparation/context references, current correction
   bytes, role independence, finding/row continuity and aggregate ownership.
2. Write the new report with exact setup/probes, observed output links, source/
   installation identities, evidence level, verdict versus qualification result,
   and unrun/failed gaps with reasons/owners. Preserve dated inputs unchanged.

- **AC-01:** Every parent requirement and inherited material case is traced to
  current decisive evidence or an explicit gap. No constructed intermediate report
  is counted as an actual role output and no schema/text check certifies behavior.
- **AC-02:** Every claimed composed pass links actual producer bytes to a separate
  consumer invocation using the qualified installation/sibling helpers. Preflight
  context, revised readiness, stable IDs and required stage/gate ownership remain
  visible through the relevant chains; incompatible identities limit claims.
- **AC-03:** The final report is beside the unchanged proposal. It gives reproducible
  commands/setup, observed outcomes and precise evidence limits. Source/installation
  changes mark affected current claims stale while preserving historical observations.
- **AC-04:** Required unrun/failed role boundaries mean incomplete behavioral
  qualification. Documentation completion alone cannot label the overall flow
  qualified or release orchestration/dependencies. Further eval authorization or
  explicit owner scope revision is stated as the next action where needed.

### Finite-risk coverage contract

| Invariant | Material dimensions/cases | Decisive oracle/boundary | Implementation evidence | Independent review probe | Gate owner |
|---|---|---|---|---|---|
| Q-01 / INV-010 | P-01–07; all retained case IDs; structural, local runtime, actual role, unrun, failed, stale evidence | Report claim resolves to supplied setup and raw boundary observation or explicit gap | Complete trace/link/identity audit; reject a staged-output or missing-gap claim | Reconstruct one composed claim and one unrun public-boundary case from raw evidence | Implementer: report audit; fresh discovery: current evidence corroboration; acceptance: separate decision |
| Q-02 / INV-004/005/008/010 | Actual preparation/recovery; discovery/decision; coordinator/preflight; failure/correction/clean review | Producer identities, consumer inputs, retained IDs/revisions and aggregate records agree across children | Cross-child composition audit without fabricating missing outputs | Follow one preflight-only context fact and one corrected finding through separate calls | Same owners; reuse current gate records, no duplicate aggregate |

## Verification

Audit links, inventories, protected-file hashes and actual input/output identities
first; check `git diff --check`. Use T-005.1's current local evidence and child
gate records rather than rerunning suites for a documentation-only closure.
Demonstrate that the audit rejects a controlled staged-output/currentness/gap
misclassification when feasible without modifying history. No owning code suite
is required if only this report changes; focused command syntax for link/identity
checks belongs to preflight. Fresh discovery reconstructs decisive claim links
and records why another aggregate is unnecessary, or owns one narrowly justified
check if a material gap requires it. Acceptance consumes that record. No role,
live, full-suite or model-budget eval is authorized by this leaf.

## Expected contract impact

Materialize planned ART-012 qualification evidence; preserve IF-008/INV-010 and
all exercised contracts. No reusable interface/runtime/ownership contract changes;
`docs/contracts` is absent, so no registry stage is introduced.

## Stops and handoff

Apply parent evidence rules. Stop for authority conflict, user overlap, unsafe
permissions, missing decisive evidence mechanism or new scope. Missing/unrun
observations stay explicit; do not repair source policy during report closure.
Budget is a soft checkpoint. Next: verification design → standalone guided
preflight → bounded implementation. Immediately after implementation/correction
and applicable conditional stages, hand completed bytes to fresh independent
`task-review-discovery`, then its report to separate `task-acceptance-review`.
End the implementer invocation. Coordinator assesses remaining qualification
gaps separately; the parent is never a launch or acceptance target.
