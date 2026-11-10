# Task Brief: T-003 — Connect sbx actors and stop safely on uncertain execution

## Outcome

Let the coordinator launch a reserved actor inside the existing sbx environment,
observe its identity and outcome, and admit a complete preflight result before
implementation. After interruption, a replacement coordinator can inspect the
preserved operation and its next action without starting a duplicate actor.
This enables T-004 to connect checks, collection and correction, then T-005 to
admit separate acceptance. It does not demonstrate the complete accepted-task loop.

## Authority and scope

- Authority: [owner-confirmed direction](../../direction-single-task-sbx.md);
  [plan](../../local-harness-orchestration-plan.md), T-003, lifecycle models,
  IF-002, IF-003 preflight slice, IF-004 stop/intervention slice, and FLOW-001/002/003;
  [accepted plan review](../../project-plan-review-single-task-sbx-r2.md).
- Dependencies: accepted T-002.1, T-002.2 and T-002.3; consume the
  [consolidated controller contract](../T-002/controller-contract.md) and their
  latest acceptance reports. Its READY_FOR_REVIEW header is historical;
  [T-002.3 acceptance-02](../T-002.3/reviews/acceptance-02.md) is the decision.
- Allowed changes: actor transport and controller/state code, affected schemas,
  examples and focused tests inside `skills/task-orchestrator/`; task-local
  implementation evidence and a successor contract here. Update only directly
  affected runtime references. Use existing module boundaries and storage patterns.
- Excludes: provisioning sbx, parallel execution, automatic recovery service,
  semantic collection/acceptance admission, candidate/check pipeline ownership,
  task completion, commits, dependency release, tracker migration, official plan
  edits and active-install refresh. T-006 owns the complete live pilot and final
  coordinator documentation.

The owner starts the coordinator inside an existing Docker sbx on a separate
branch. Actors use explicitly authorized YOLO policy. These are operating
assumptions, not containment guarantees. Do not restore tool exclusion, hooks,
outer-system protection or runtime-enforced reviewer read-only access as entry
gates. Review assignments still prohibit implementation edits.

### Expected contract impact

Consume the controller, state and transport boundaries registered in
[`docs/contracts/task-orchestrator.json`](../../../../../docs/contracts/task-orchestrator.json),
resolved through the registry index. That record describes older primitives;
use the accepted T-002 contract and executable authorities for current details.
Materialize IF-002 and ART-004 observed outcomes; extend ART-002 with admitted
preflight readiness and IF-004/ART-007 with stop/blocker records. Publish an
ART-008 runtime supplement. ART-006/009 capture is raw transport only; T-004/005
own their semantic admission through the same controller path. Preserve
INV-001/002/003/004/005/007/008. Route actual registry synchronization through
the installed registry-updater stage after implementation review.

## Work and acceptance criteria

**AC-01 — Launch only the reserved operation.**

Use current immutable authority through the T-002 loaders, including revised
inputs. Apply the frozen `gpt-6.1-sol` low/medium/high mapping, context/session
policy and explicit sbx/YOLO authorization at the actual transport boundary.
Remove the adapter's full-access refusal only for that authorized policy.
Missing authorization, incompatible old runs, stale bindings and wrong roles
refuse without launching or changing authority. Unknown or unreliable correction
occupancy requires a fresh session. Preserve the shared three-correction count,
cycle-zero rule and reservation replay behavior; transport cannot grant another
free implementation or fourth correction. A repeated operation key must never
launch twice, including after reload or interrupted launch publication.

**AC-02 — Observe identity and retain outcomes.**

Bind run, task, operation, role, current input/policy/flow and applicable candidate
identity to adapter-observed process/session identity. Preserve assignments,
launch configuration, events, stderr, raw result and terminality observations.
Configured model identity must remain distinguishable from observed identity.
Actor prose cannot invent provenance, change policy or declare acceptance.
Missing, malformed, wrong-role, stale or nonterminal output cannot advance a
stage. Capture collector and acceptance output without admitting their semantics.
Use fresh independent collection and acceptance assignments; do not treat a
preflight session as either role. An implementation outcome remains a claim.

**AC-03 — Admit actual preflight readiness.**

Reserve preflight through IF-001, launch through IF-002 and admit its observed
terminal outcome through IF-003. Check the prepared task's required tools,
dependencies and installed skills in the execution environment. Admit readiness
only for a complete ready result bound to the current frozen inputs and terminal
preflight operation. Each missing prerequisite produces a precise blocker and
prevents implementation. Wrong task/role/session, stale inputs, malformed or
nonterminal results and unknown liveness cannot establish readiness. Preflight
and retries consume no correction cycle. After authorized environment repair or
input revision, require new preflight; old readiness cannot become current by
repointing a reference. A valid admitted result permits the next legitimate
implementation reservation and launch, without supplying future semantic evidence.

**AC-04 — Interrupt and stop conservatively.**

Handle interruption before launch, after launch and during output collection.
Persist reserved/running/unknown/terminal status coherently and retain work,
evidence, operation history and correction count. Unknown liveness blocks retry,
another writer and completion. A stop request is not terminality proof: observe
the actual process outcome or retain unknown status. Reloaded status supplies a
precise permitted next action. Repeated observation/collection/stop must not
duplicate launch, overwrite historical outcomes or charge another correction.
No automatic recovery service or power-loss guarantee is required.

**AC-05 — Persist intervention for the active chat.**

Record the precise blocker, evidence location, unresolved operation and required
owner action. Expose it for relay in the active coordinator chat, preserving
relay/response history and unknown delivery/response where unobserved. No external
message send is required. Acknowledgement or silence does not authorize repair,
policy revision, retry or completion. Bounded authorized repair follows the
existing correction budget and fresh-preflight rule; exhausted budget remains
blocked with partial work retained.

**AC-06 — Publish the successor interface and truthful proof limits.**

Create `controller-contract.md` here with actual callable/CLI names, payloads,
record paths, identity/terminality rules, refusal and replay examples, readiness
admission, stop/intervention behavior and exact local results. Include the
ART-008 supplement: selected CLI bridge, supported sbx launch configuration,
observed evidence and unproved runtime claims. Preserve historical T-001 limits.
Specify the single admission path T-004/005 will extend and their raw-output
handoffs. Do not describe seeded future records as production admission or fake
executables as real sbx/model qualification.

## Evidence boundaries

Verification design: **separate** — launch/publication interruption, process
liveness, readiness and replay need behavioral scenarios with real filesystem
and child-process observations. Reuse existing controller/transport fixtures;
inspect coverage before adding cases under `testing-discipline`. Include valid
controls as well as refusal cases, and the first successful launch after fresh
preflight. Syntax, schemas and planned argv alone do not prove actor execution.

Local fake-Codex and disposable prerequisite fixtures can prove control flow;
actual sbx/provider qualification must be reported separately. Verification design
must identify a bounded actual-sbx launch/terminality check for the ART-008
supplement and its approval/environment requirements. No live/model check is
authorized by this brief. If unrun, preserve that explicit qualification gap for
T-006; do not invent live success or substitute historical macOS containment proof.

## Execution and handoff

Status: `ready`
Task kind: `executable`
Brief revision: 1
Profile: `guided`

The brief is prepared; execution prerequisites remain. Next: derive
`verification.md`, then obtain ready `preflight.md` through standalone guided
preflight. Confirm current predecessor interfaces and available process fixtures.
Do not implement from this brief alone.

Follow the [submission route](../../../../../.agents/skills/README.md#submission-route),
including independent discovery and a separate acceptance decision after
implementation/correction. Stop for changed authority, material predecessor
mismatch, new shared infrastructure needs or required permission expansion.
Inspect the canonical installer if shared runtime dependencies change; do not
auto-add the orchestrator to the development profile.

Implementation verification starts with the changed transport/state/controller
tests, then the owning orchestrator suite after targeted success. Report known
baseline failures and platform skips separately. Apply repository architecture
and contract checks; run the aggregate repository gate for cross-cutting changes
subject to live/expensive-check approval rules. T-004 consumes this task's accepted
contract and preserved raw records; T-006 consumes its runtime supplement and
remaining live proof obligations.

```yaml
agent_tier: strong
reasoning: medium
review: immediate
budget: 30 tool calls / 80 minutes / 80k context
```

### Execution sizing

Policy: project-local `task-brief-designer/references/task-sizing.yaml`,
`default@1`. Estimate: 30 implementation agent calls; 80 minutes; medium
confidence. Intended profile: `strong/medium`.

Policy result: `override_cannot_split_safely`.
`decomposition_override: cannot_split_safely` — exceeds 15 calls and 40 minutes.
Considered separating launch/observation from preflight/stop admission. Both
would change the same operation ledger, terminality publication and controller
admission path; a transport-only child would need provisional state contracts
that the second child must renegotiate. One cohesive task proves reservation,
launch, terminal observation and readiness at their shared public boundary.
Residual risk: interruption cases can expand execution time. Use the budget as
a checkpoint; return material scope expansion to brief design rather than
adding recovery infrastructure.
