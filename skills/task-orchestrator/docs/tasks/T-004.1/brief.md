# Task Brief: T-004.1 — Produce candidate-bound scope and check evidence

## Outcome

After a terminal implementation or correction, the coordinator can inspect the
actual task files and run the approved checks through the controller. Evidence
identifies the exact candidate evaluated and cannot pass after relevant drift.
T-004.2 uses these operations for independent collection and correction.

## Authority and scope

- Authority: [parent](../T-004/brief.md), P-01/02/06;
  [plan](../../local-harness-orchestration-plan.md), ART-003/005, IF-003,
  INV-001/002/003/007/008 and FLOW-001 steps 2–4;
  [owner-confirmed direction](../../direction-single-task-sbx.md).
- Dependency: accepted T-003; use its [contract](../T-003/controller-contract.md)
  and [acceptance](../T-003/reviews/acceptance-02.md). Implementation results are
  raw claims today; legacy `inspect` is not the new loop's admission authority.
- Allowed: existing controller/Git/verification/state modules, affected schemas,
  focused tests and directly affected runtime references under
  `skills/task-orchestrator/`. Reuse existing lock, identity and record patterns.
- Excludes: collection semantics, acceptance/completion, new review policy,
  generic execution backends, automatic repair/install, official-plan edits and
  installation refresh. T-004.2 owns the composed correction/collection proof.

Use the owner-supplied sbx/separate-branch/YOLO assumptions. Scope and task
authority remain mandatory. These assumptions do not establish runtime isolation.
Do not silently migrate frozen runs or weaken required checks.

### Expected contract impact

Consume the current controller, observed outcomes and verification contracts in
[`docs/contracts/task-orchestrator.json`](../../../../../docs/contracts/task-orchestrator.json).
Materialize ART-003/005 and the inspect/check slice of IF-003; extend ART-002
with their current identities and statuses. Publish `controller-contract.md`
here for T-004.2: actual API/CLI names, payloads, evidence paths, check invocation
and replay rules, candidate identity inputs and generated-file treatment.
Route registry synchronization through the installed registry-updater stage.

## Work and acceptance criteria

**AC-01 — Inspect the actual implementation candidate.**

Through public controller operations, consume an admitted terminal implementation
or correction outcome, inspect the real repository and produce ART-003. Bind
run/task, operation, approved input/policy/flow, baseline, relevant tracked and
untracked bytes and configuration. Preserve existing owner work and reject
out-of-scope changes. An actor's claimed digest, check pass or summary cannot
replace controller inspection. Live/unknown operations cannot establish a stable
candidate or permit an overlapping check operation.

**AC-02 — Refuse stale evidence and preserve history.**

Relevant tracked/untracked/configuration/task-input changes supersede candidate
and dependent check eligibility. Check identity before and after execution;
changes during a check cannot produce a current pass. Preserve historical
records and distinguish stale from failed or missing. Honor the existing
generated-file rules without ignoring evaluated inputs. Invalid/stale requests
preserve authoritative state/version, count and task files; operational failures
may publish truthful evidence/blockers. Replay/reload must not rerun a completed
check under the same operation identity or overwrite its evidence. Uncertain
execution remains stopped under the existing operation guard.

**AC-03 — Execute approved checks in the target environment.**

Use the existing verification planner/runner for actual argv execution and
durable logs. Add the minimum explicit sbx/YOLO-authorized execution path needed
by this loop: the current runner requires macOS `/usr/bin/sandbox-exec` and
cannot execute unchanged inside Linux sbx. Select that path only from frozen
explicit execution authority, not from platform detection or a failed sandbox
launch. Preserve restrictive/legacy behavior and refusals for unsupported or
unauthorized policies. Record the effective execution mechanism and its limits;
do not claim network/filesystem enforcement in the YOLO path. Retain authorized
command parsing, dependency-install restrictions, timeouts, process terminality
and log publication. No silent unrestricted fallback or new provider is allowed.

**AC-04 — Publish truthful check results and next actions.**

ART-005 records the commands, setup/inputs, environment, current evaluated
candidate, outputs, exits and execution status. Passed, failed, stale, blocked,
missing/not-run and policy omission remain distinct. Required checks cannot be
omitted or excused as a known issue. A real product failure can request bounded
correction through the inherited controller policy; missing/broken infrastructure
routes to authorized repair or a precise intervention. Evidence-only checking
does not charge correction count. Status exposes the next permitted stage and
evidence without granting collection, acceptance or completion prematurely.

**AC-05 — Publish a usable producer handoff.**

Document actual candidate/check operations and schemas in the local contract,
including how a future collector requests its own rerun through the same runner.
Include real-file failing/passing controls, drift/refusal/replay behavior and
exact local verification outcomes. T-004.2 must not need a second check runner,
ledger or actor-admission path. Report local subprocess proof separately from
unrun real sbx/provider qualification, which remains T-006 work.

## Evidence boundaries

Verification design: **separate** — identity drift, check side effects,
interruption and execution-policy selection require real filesystem/subprocess
observations. Inspect `test_controller_git.py`, `test_verification_runner.py`,
`test_controller.py` and T-003's `test_actor_operations.py` setup before adding
coverage under installed `testing-discipline`. Reuse existing unusual-path,
same-size content-change, dirty-baseline, timeout and publication cases.
Schema/syntax or mocked argv alone cannot prove check execution.

The existing subprocess mechanism can exercise portable local commands. No new
shared harness or feasibility project is authorized. Preflight confirms the
available local fixtures and exact frozen policy projection. A material authority
or enforcement-design gap returns to task design; it is not permission for an
implicit fallback. No live/model/networked check is authorized by this brief.

## Execution and handoff

Status: `ready`
Task kind: `executable`
Brief revision: 1
Profile: `guided`

The brief is prepared; execution prerequisites remain. Next: derive
`verification.md`, then ready `preflight.md` through standalone guided preflight.
Follow the [submission route](../../../../../.agents/skills/README.md#submission-route),
including required maintainability/registry stages, fresh independent discovery
and a separate acceptance decision. Stop for changed authority, material
predecessor mismatch, permission expansion or new shared infrastructure needs.
Inspect the canonical installer if shared runtime dependencies change; do not
auto-add the orchestrator or refresh this run's installed skills.

Implementation verification starts with the changed owning test methods/modules,
then the orchestrator suite when focused checks pass. Run repository architecture
and contract checks; use the aggregate gate for cross-cutting changes. Preserve
baseline failures and platform skips as limits, not successes. Live/expensive
checks need their applicable approval. Publish the accepted producer contract
before T-004.2 starts.

```yaml
agent_tier: strong
reasoning: medium
review: immediate
budget: 24 tool calls / 60 minutes / 80k context
```

### Execution sizing

Policy: project-local `task-brief-designer/references/task-sizing.yaml`,
`default@1`. Estimate: 24 implementation calls; 60 minutes; medium confidence.
Policy result: `override_cannot_split_safely`.
`decomposition_override: cannot_split_safely` — exceeds 15 calls and 40 minutes.
Considered separating candidate capture from check execution. Both must settle
the same pre/post-execution identity, generated-file treatment, reservation and
evidence-publication contract; separating them would duplicate transitional
identity fixtures and require contract rework before checks are usable. Keep
this producer boundary cohesive. Residual risk: runner-policy and drift cases
may expand execution; stop at the budget checkpoint for material scope growth.
