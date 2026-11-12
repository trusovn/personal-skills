# Task Brief: T-004.2 — Admit independent collection and prove bounded correction

## Outcome

The coordinator can obtain fresh independent collection for the actual checked
candidate, correct a real failure and repeat checks and collection with current
evidence. T-005 receives an acceptance-ready evidence handoff; this task does
not decide acceptance or complete the task.

## Authority and scope

- Authority: [parent](../T-004/brief.md), P-03..06;
  [plan](../../local-harness-orchestration-plan.md), ART-006, IF-003,
  FLOW-001 steps 2–6, FLOW-002/003 and INV-001..008;
  [owner-confirmed direction](../../direction-single-task-sbx.md).
- Dependency: accepted T-004.1 and its `controller-contract.md`; consume
  [T-003's contract](../T-003/controller-contract.md) for observed actor outcomes
  and [T-002's contract](../T-002/controller-contract.md) for correction accounting.
- Allowed: collection/result schemas, controller/state wiring, focused tests,
  assignments and directly affected references under `skills/task-orchestrator/`;
  integration fixes to the T-004.1 interface within its accepted contract.
- Excludes: semantic ART-009 admission, acceptance decisions, completion,
  tracker writes/migration, commits, dependency release, new correction limits,
  provisioning/recovery services, official-plan edits and installation refresh.

Use owner-supplied sbx/separate-branch/YOLO authority. Collection is a read-only
assignment, not runtime-enforced filesystem isolation. `review-collect` names
a role, not an installed command. Resolve applicable installed review skills
project-locally; do not substitute source instructions for unavailable skills.
Preserve separately required discovery, maintainability, registry and acceptance
roles. An unavailable required role needs explicit source-guided authority or
blocks that task profile. No new direction decision is needed for this scope.

### Expected contract impact

Consume the [current registry](../../../../../docs/contracts/task-orchestrator.json)
and accepted T-004.1 producer contract. Materialize ART-006 and IF-003 collection
semantics by extending the existing `observe_operation` admission/publication
path. Extend ART-002 with current coverage, findings and truthful next actions;
preserve inherited IF-001/002 counting and terminality. Consolidate the actual
T-004 interface into `../T-004/controller-contract.md` for T-005. The installed
registry-updater stage records implemented deltas only; ART-009/IF-004 completion
remain future capability.

## Work and acceptance criteria

**AC-01 — Launch fresh independent collection with current inputs.**

After controller inspection/checking, reserve and launch a fresh collector via
the existing actor bridge. Its assignment includes frozen authority, candidate,
check evidence, prior findings/dispositions and applicable review requirements.
Bind its report to adapter-observed task, operation, role, session, inputs and
candidate. Reject wrong-task/role/session/candidate, invented provenance,
nonterminal/malformed results and reuse of an implementation/correction session.
Preserve the future separate-acceptance requirement; a collector cannot submit
acceptance authority. Missing/failed evidence cannot be relabeled a pass.

**AC-02 — Rerun checks and retain independent findings.**

The collector reruns relevant deterministic checks through T-004.1's controller
runner and inspects requirements, behavior and code quality. A reference to the
implementer's pass is insufficient. Admit ART-006 only with current bound rerun
evidence and explicit coverage, gaps and findings; collection can report failure
or missing evidence without becoming successful coverage. Retain stable finding
IDs, evidence, requirement/context, dispositions and history. Preserve approved
dispositions unless new relevant evidence or changed exposure justifies reopening.
Do not make observations automatic correction obligations or invent new deferral
authority. Collection produces evidence, not a final acceptance verdict.

**AC-03 — Correct real work within the inherited budget.**

Connect failed-check correction to the existing controller authorization,
reservation and actor launch. Correction changes the real failing fixture code,
then repeats candidate capture, required checks and fresh independent collection.
Relevant changes invalidate prior coverage while keeping historical evidence.
Initial implementation is cycle zero; each authorized correction consumes exactly
one of the three shared cycles, regardless of check/review/environment-repair
origin. Unknown occupancy uses a fresh correction session. Repeated reservation,
observation, reload or input revision cannot reset or double-charge the count.
Evidence-only reruns/recollection do not consume a correction unless they launch
implementation changes. Environment repair follows the inherited fresh-preflight
rule. Separate acceptance may later request review-driven correction; do not
implement its semantic admission in this task.

**AC-04 — Reject drift and preserve safe interruption.**

Tracked/untracked/configuration/task-input changes, including changes during
collection, prevent stale report admission. Do not restore eligibility by
repointing a digest or report path. Repeated observation replays the same admitted
outcome without overwriting findings or logs. Unknown/live operation ownership
blocks another actor and acceptance progression. Preserve files, records, count
and precise next action after interruption/reload; persist intervention when
terminality or authority cannot be established. Invalid requests leave
authoritative state/version, count and task files unchanged.

**AC-05 — Prove the composed loop and correction exhaustion.**

In one disposable repository/prepared task, use actual public preflight and
implementation operations, a real failed check, a correction actor that changes
code, real passing checks and a distinct fresh collector that reruns them.
Exercise a later relevant edit and reject old check/collection evidence. Also
prove cycle zero plus three shared corrections, duplicate/reload behavior and
fourth-correction refusal with partial work/evidence retained and a precise
active-chat intervention. Distinguish product failure, infrastructure failure,
missing evidence, stale evidence and unresolved authority in persisted status.
Show the handoff to the acceptance stage without admitting acceptance/completion.

Use scripted local actors only to control role responses and edits; do not seed
candidate/check/collection success where this task now owns production admission.
For the not-yet-implemented ART-009 review-driven correction route, use an explicit
test-only successor-decision fixture through the inherited state seam. Label it
as such and keep it separate from the unseeded failed-check correction proof.
No production bypass for an acceptance decision is allowed.

**AC-06 — Publish the exact T-005 handoff and limits.**

Consolidate actual callable/CLI names, schemas, artifact paths, collection rerun
requests, finding/disposition rules, refusal/replay behavior and correction
transitions in the parent controller contract. Identify the single semantic
admission path T-005 must extend, raw acceptance transport inputs it can consume,
and missing-evidence/correction routing seams. Supply exact local proof results
and retained baseline/qualification limits. No local fake actor proves real
sbx/provider/model behavior; T-006 retains that live pilot.

## Evidence boundaries

Verification design: **separate** — the correction lifecycle, independent reruns,
finite identity tampering and exhausted-budget behavior need distinct positive
and refusal controls. Inspect existing controller/state/actor-operation tests
and accepted T-004.1 coverage under installed `testing-discipline`; extend reusable
fixtures instead of copying setup. Give the future ART-009 fixture a clear
boundary. Schema validation or a seeded ledger alone cannot prove this loop.
No live/model/networked verification is authorized by this brief.

## Execution and handoff

Status: `ready`
Task kind: `executable`
Brief revision: 1
Profile: `guided`

The brief is prepared; execution prerequisites remain. Next: after T-004.1 is
accepted, derive `verification.md`, then ready `preflight.md` through standalone
guided preflight. Follow the
[submission route](../../../../../.agents/skills/README.md#submission-route),
including applicable maintainability/registry stages, fresh independent discovery
and a separate acceptance decision. Stop for authority changes, material producer
mismatch, unavailable required review capability, permission expansion or a new
shared harness need. Inspect installer ownership if shared runtime dependencies
change; do not refresh installed skills during this run.

Start implementation verification with changed collection/correction test methods,
then owning modules; run the orchestrator suite after targeted success. Run
repository architecture and contract checks; use the aggregate gate for
cross-cutting changes. Report baseline failures/skips and seek applicable approval
for live/expensive checks. After acceptance, hand the consolidated contract and
accepted child results to T-005; do not run T-005 from this package.

```yaml
agent_tier: strong
reasoning: medium
review: immediate
budget: 26 tool calls / 65 minutes / 80k context
```

### Execution sizing

Policy: project-local `task-brief-designer/references/task-sizing.yaml`,
`default@1`. Estimate: 26 implementation calls; 65 minutes; medium confidence.
Policy result: `override_cannot_split_safely`.
`decomposition_override: cannot_split_safely` — exceeds 15 calls and 40 minutes.
Considered separate collection and correction-integration children. Both must
settle findings/history, current coverage invalidation and the same observed
outcome transition; splitting would require provisional correction/report
contracts plus repeated lifecycle fixtures and review. Keep the collector and
its correction-loop integration together, consuming the already accepted check
producer. Residual risk: finite tamper/replay cases can expand work; use the
budget as a checkpoint and return material scope growth to task design.
