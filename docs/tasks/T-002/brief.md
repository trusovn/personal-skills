# Task Brief: T-002 — Capture and hand off the starting code

## Outcome

Preflight gives the implementation agent one named report of the actual starting
Python code and the repository's existing static-check obligations. The handoff
lets T-003 validate the starting state before editing and compare later changes
against the original baseline. This task defines and prepares that handoff;
T-003 owns implementer consumption and direct-task self-preflight, and T-004
owns independent reviewer consumption.

## Authority and scope

- Authority: [project plan, T-002](../../project-plan.md#t-002--capture-and-hand-off-the-starting-code),
  sections 1–2, 6–7, FLOW-002 and V-003/V-006/V-008; the
  [T-002 task-map entry](../../task-map.json). The
  [independent plan review](../../project-plan-review.md) accepted the plan.
- Repository: `personal-skills`; [project map](../../project-map.md),
  [development guide](../../development.md) and repository instructions govern
  placement, installation boundaries and verification.
- Dependency: T-001's portable runtime, format-5 reports, empty-folder capture
  and native-check discovery. Accepted outputs are recorded in
  [T-001.1 acceptance](../T-001.1/reviews/acceptance-01.md),
  [T-001.2 acceptance](../T-001.2/reviews/acceptance-02.md) and
  [T-001.3 acceptance](../T-001.3/reviews/acceptance-02.md).
  Preflight must confirm their current applicability; this brief does not
  certify current repository readiness.
- Allowed changes: source `skills/task-implementation-flow/task-preflight/`,
  including its instructions, execution-packet template, eval definitions and
  existing fixture setup. Extend owning shared measurement or installer tests
  only for distinct missing evidence needed by this handoff. Inspect
  `scripts/install_development_skills.py` and its profile documentation/tests
  in the same change; update only items made stale by this integration.
- Out of scope: runtime redesign, new analyzers, a check runner or evidence
  store, new stages, controller work, T-003/T-004 instruction changes and T-005's
  complete installed correction journey. Do not refresh the active installation
  or update the master plan to record completion.
- Read-only context: source preflight's current guided/high-assurance readiness
  and freshness rules, [measurement guide](../../../scripts/measure-maintainability.md),
  existing `tests/test_maintainability.py`, `tests/test_install_development_skills.py`,
  and source preflight evals. Reuse their distinct cases and setup before adding
  coverage. Source instructions are development specifications, not the active
  installed workflow.

The accepted direction keeps measurements advisory and native hard checks under
their existing policy and owner. Capture actual pre-edit bytes once, including
relevant dirty and untracked code. Do not reset, stash, stage, install tools
implicitly or claim tamper resistance from colocated hashes. Preserve existing
guided versus high-assurance readiness, scope and ownership rules.

### Expected contract impact

- Materialize preflight's producer side of starting evidence (`ART-002`,
  `IF-002`, `CAP-002`, `FLOW-002-S01`). Consume installed runtime/settings
  (`ART-001`, `IF-001`) and native-check authority (`ART-007`, `IF-004`);
  produce task-owned evidence (`ART-006`). Preserve `INV-002`, `INV-003`,
  `INV-007` and `INV-009`.
- Available dependencies: [measurement contracts](../../contracts/measurement.json)
  describe the implemented CLI, baseline report and foundation discovery;
  [installation contracts](../../contracts/installation.json) describe managed
  projection; [runtime evidence](../../contracts/runtime-evidence.json) remains
  optional evidence tooling, not a required new lifecycle.
- Expected delta: existing preflight results/packets carry a usable original
  baseline reference and native-check inventory for T-003 and T-004. The bounded
  registry-updater stage records the implemented producer contract without
  claiming later consumers or live agent compliance are complete.

## Work and acceptance criteria

**AC-01 — Capture the actual starting scope**

For supported, authorized Python work, ordinary preflight attempts baseline
capture before implementation. Select the smallest relevant folders, including
relevant production, test, eval, fixture and harness code under existing explicit
exclusions and asset groups. Folder coverage includes future files. For a new
Python area, an explicitly selected existing parent folder with an empty Python
inventory is valid before evidence, as defined in plan FLOW-002. Do not invent
numeric zero values for absent code. Capture actual worktree bytes, including
staged/unstaged differences and relevant untracked files, without changing source
or the real Git index. Preserve any earlier report and its text sibling; use a
fresh output path.

**AC-02 — Hand off an applicable original baseline**

Existing guided results and high-assurance packets carry the exact JSON report
path and text companion, governed folder scope, capture origin and identity
needed to validate applicability. Identity references cover the logical project,
captured file inventory/source hashes and effective tool/settings/scope identity;
reference report facts rather than create a separate dossier. State how a
consumer checks the starting source and covered inventory before the first edit.
A changed starting state must be detected and routed to focused readiness
reconsideration, not accepted as the recorded baseline. Preserve stronger existing
high-assurance freshness checks without imposing a full digest ledger on guided
work.

Retain the original baseline through corrections. Unexpected scope expansion
needs authorized scope resolution and exact pre-edit evidence for added coverage;
uncovered code is not compared evidence. If before evidence cannot be recovered,
current measurement must retain that gap. Never relabel edited code as the
starting state. For isolated clones, identify the exact report files to transfer:
ignored reports do not travel with commits. Plan section 7 IF-002 and FLOW-002,
and the measurement guide's capture/transfer contract govern these handoffs.

**AC-03 — Distinguish advisory gaps from readiness blockers**

Docs-only and unsupported-language scope records measurement as not applicable.
Missing tools, missing or incompatible baseline evidence and partial capture
remain visible; they do not establish a successful or complete comparison.
Default advisory-tool absence does not introduce an unsolicited readiness blocker
or implicit setup. Where explicit task/repository authority makes the evidence
indispensable, failure prevents a ready result and names the capability owner
and smallest recovery action. Otherwise retain the gap while existing readiness
assessment continues. This fallback never waives another required prerequisite.

**AC-04 — Carry native checks without changing their authority**

Use one focused discovery pass through the existing registry/equivalent, then
agent instructions, project map and native task configuration as needed. Carry
each applicable command, governed scope, policy reference, requiredness and
existing stage owner in the current handoff. Documented commands suffice without
a registry; invent no checks when none exist. Do not treat the optional gates
template as a required installed checker.

Run only a justified cheap readiness check under existing ownership, not all
static gates to create another before baseline. Preserve whole-project scope,
hard failure/unavailability semantics and existing execution duties even when
Python measurement is unavailable or not applicable. Current applicable aggregate
evidence can cover its constituents when command coverage, policy and checked
bytes are established; do not rerun them merely to fill report sections.
Missing/stale required native evidence remains owed under its existing owner's
policy. Successful advisory metrics cannot mask that obligation or a hard failure.

**AC-05 — Prepare executable evidence without claiming agent qualification**

Update the existing preflight eval setup and expectations for the material
AC-01–AC-04 outcomes, while preserving existing guided/high-assurance readiness,
ownership and preparation cases. Each claimed outcome has supplied inputs,
permissions and a decisive oracle. Fixtures must explicitly authorize baseline
report writes where capture is expected; retain unrelated-path preservation
obligations. Reuse existing real measurement/index-preservation and installed
fixtures rather than duplicate their harness. Deterministic tool or fixture
checks establish their own boundaries only. Prepared agent evals require grading
actual reports, readiness decisions and retained obligations; metadata validation
or keyword matches alone do not qualify agent behavior.

## Evidence boundaries

Verification-design recommendation: **separate — starting-state freshness,
dirty/index preservation, empty-start coverage and advisory-versus-required
failure policies need distinct observations.** Derive `verification.md` from this
brief; it owns scenario details, evidence reuse and gate allocation for the
T-002 portions of V-003/V-006/V-008.

The implemented CLI/report and existing Git fixtures provide the believed-existing
measurement and freshness observation boundary. Standalone preflight confirms
the prepared pinned interpreter, installed helper paths and feasible setup;
no new shared helper or platform proof task is assigned here. Missing essential
capability returns to its owner rather than expanding this implementation.

For implementation verification, start with the task-owned focused changes and
`tests/test_maintainability.py`, then installer tests when affected, before any
justified aggregate gate. Run the canonical architecture and contract checks
before handoff, as required by plan section 11. Native analyzer skips do not
qualify measurement. Live agent evals require separate budget/runtime approval;
if not run, state that agent behavior remains unqualified. Report active-profile
drift without refreshing this invocation's installation.

## Execution and handoff

Status: `ready`
Task kind: `executable`
Profile: `guided`
Brief revision: `1`

The brief is prepared; execution prerequisites remain. Next, run
`task-verification-designer` to create this package's `verification.md`, then
standalone guided `task-preflight` to produce a ready `preflight.md` before
implementation. High-assurance preparation is not warranted merely because the
source skill supports that mode. Current analyzer capability and prerequisite
applicability belong to preflight.

Use the [shared submission route](../../../.agents/skills/README.md#submission-route),
including fresh independent discovery and a separate acceptance decision for
`review: immediate`. Carry the accepted producer contract to T-003; do not imply
that its consumer or T-004's reviewer integration is already delivered. Stop for
unresolved ownership overlap, missing indispensable capability or a required
scope/policy change outside this authority.

```yaml
agent_tier: standard
reasoning: high
review: immediate
budget: 15 tool calls / 40 minutes / focused context
```

### Execution sizing

- Policy: active `default`, version 1, from the active designer's
  `references/task-sizing.yaml`.
- Estimate: 15 agent calls; 40 implementation minutes; confidence: medium.
  Includes focused discovery, source instructions/template changes, reused eval
  setup and task-owned verification. Excludes separate preparation and review.
- Policy result: fits for `standard` / `high`; no decomposition trigger matches.
  Capture and native-check references share one preflight handoff and fixture
  surface, so one executable leaf keeps their integration proof local.
