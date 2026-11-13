# Task Brief: SIDE-004 — Define code-organization guidance and route implementation and review to it

## Outcome

Give implementation and maintainability-review agents explicit code-organization
rules before the next refactoring effort. Keep the rules in a standalone document,
outside `AGENTS.md`, and make the two skills find and apply the relevant project
guidance. Completion establishes instructions and their consumption; it does not
modularize the current orchestrator.

## Authority and scope

Authority: the owner's 2026-11-13 request following inspection of staged Python
changes and controller growth. The owner approved a separate SIDE task after
T-005.1, standalone instructions routed from the two skills, and a separate later
effort to rework existing code against those instructions.

**Execution dependency:** orchestrator
[T-005.1](../../../skills/task-orchestrator/docs/tasks/T-005.1/brief.md) must be
completed with applicable acceptance evidence before this task starts. Resolve
that task through its own
[structural index](../../../skills/task-orchestrator/docs/tasks/index.json), not
the unrelated root-plan T-005. This cross-index prerequisite is recorded here;
the root index's local `depends_on` list does not establish execution readiness.

Allowed changes:

- New repository guidance at `docs/code-organization.md`; update the existing
  project/module maps only to route readers to it or reconcile actual authority.
- Source `bounded-task-implementer` and `task-maintainability-review` instructions
  and directly affected references under `skills/task-implementation-flow/`.
- Owning tests/eval expectations and installation documentation/profile support
  only as needed to distribute and resolve the new instructions correctly.

Do not change `AGENTS.md`, refactor runtime code, prescribe an unimplemented
module layout as current fact, rewrite existing task/review history, or refresh
the active skill installation. This brief does not authorize the later code
refactoring task. No new linter, architecture analyzer, review stage or live eval
is required.

### Expected contract impact

Current dependencies are recorded in `docs/contracts/implementer-feedback.json`,
`reviewer-feedback.json`, `installation.json`, and `foundation-tools.json`.
Preserve existing measurement, independence and submission-route contracts.
Expected delta: implementation and review consume a shared project-owned
organization policy and report relevant placement/boundary decisions. Route
actual registered-contract changes through the existing registry-updater stage;
do not register a future runtime decomposition as implemented capability.

## Work and acceptance criteria

**AC-01 — Standalone guidance gives agents concrete organization rules.**

Create `docs/code-organization.md` as the authoritative repository organization
policy, linked to existing maps rather than duplicating their inventories.
Cover responsibility-based modules and names, dependency direction, explicit
inputs/collaborators, ownership of state and invariants, separation of decisions
from filesystem/process effects, coherent transaction boundaries, proportionate
use of functions/classes, and placement of focused versus integration tests.
Apply the rules to production, test/eval, fixture and harness assets.

Distinguish mandatory rules from advisory investigation triggers. Include brief
examples showing a cohesive extension, a new responsibility that merits a module,
and a harmful mechanical split. Size and complexity should trigger assessment of
accumulated responsibilities; neither smaller functions nor a bare retention
claim proves good organization. Do not invent numerical hard limits or require
an interface/class per component. Clearly distinguish current structure from
guidance for new changes and later refactoring.

**AC-02 — Implementation makes placement decisions before editing.**

Update `bounded-task-implementer` to read the target repository's
`docs/code-organization.md` when present, plus directly relevant module guidance,
before choosing placement. Keep this generic and target-repository-relative;
never read this source checkout's policy as the policy of another repository.
Honor equivalent guidance explicitly routed by task/repository authority.
Absence of a standalone policy alone must not block unrelated repositories or
cause the skill to manufacture one.

For structural additions or material growth, identify the responsibility owner,
proposed placement and necessary dependency changes in a concise explanation.
Apply local policy during implementation and final self-check. A new file is not
forbidden solely by a surgical-change preference when it is the smallest coherent
way to implement authorized behavior. Wider legacy cleanup or a material
architecture/scope decision still returns to the owner.

**AC-03 — Independent review checks policy and accumulated structure.**

Update `task-maintainability-review` to resolve the same target-project policy
and examine actual ownership, placement and dependency changes against it.
Assess the affected responsibility cluster with its helpers and consumers;
function-level metric explanations alone cannot justify retaining unrelated
responsibilities in one module. A cohesive extension may remain in place, and
an extraction must improve ownership or comprehension rather than merely move
lines or create callbacks into the controller.

Findings cite the applicable rule, changed evidence, concrete maintenance
consequence and bounded correction. Preserve independent review, advisory metric
policy and protection against blocking on untouched debt. Policy must govern new
or materially worsened structure without imposing retroactive repository-wide
cleanup. Distinguish mandatory local-policy violations from advisory concerns;
make their treatment consistent with existing verdict rules.

**AC-04 — Source, distribution and evidence agree.**

Inspect `scripts/install_development_skills.py`, its selected sources/profile
guide/shared files, focused installer coverage and README installation guidance.
Synchronize only affected resources and routing. Keep project-owned policy in
the target repository; do not copy this repository's policy into arbitrary
projects or broaden the installer's ownership. Validate disposable installations
when distribution changes; never refresh the active installation in this run.

Inspect and reuse existing preparation, implementer/review and installer coverage
before changing tests/evals. Check a cohesive in-place extension, a distinct new
responsibility, an extraction with reverse dependencies, and a repository with no
standalone policy. Evidence must distinguish document/reference checks and
source-guided worked cases from actual executed agent behavior. No claim of
behavioral qualification follows from string assertions or valid links alone.

## Evidence boundaries

Verification-design recommendation: separate — policy must be consumed by two
roles without weakening bounded scope, advisory metrics, independence or portable
installation. Derive focused cases from the acceptance criteria using existing
test/eval facilities; no new general harness is authorized. Live/model evaluation
requires separately approved budget; report its absence as unqualified behavior.

Run the owning focused suites first, installer checks if affected, then the
cross-cutting `python3 tools/verify.py`. Establish the canonical architecture
gate and `python3 tools/check_contracts.py --root .` before handoff; current
applicable aggregate evidence may cover them. Report skips and installation
drift separately from successful evidence.

## Execution and handoff

Status: `ready` — brief prepared; dependency and execution preparation remain pending.
Task kind: `executable`; guided profile.

Next: after T-005.1 completion is established, derive `verification.md`, then
obtain a ready `preflight.md` through standalone guided preflight. Recheck the
source/installed-skill distinction at execution time. Missing or contradictory
architecture authority returns to the owner rather than becoming an implicit
permission to redesign runtime code.

Workflow: [shared submission route](../../../skills/task-implementation-flow/README.md#submission-route).
Use applicable maintainability review and registry synchronization, then fresh
independent discovery and the separate acceptance decision. Publish results and
numbered review evidence in this package. The later code-reorganization effort
consumes the accepted guidance; it is not launched or implemented by this task.

```yaml
agent_tier: standard
reasoning: medium
review: immediate
budget: 15 tool calls / 40 minutes / policy, two skill consumers and focused evidence
```

Sizing: `default@1`; estimate 15 implementation-agent calls / 40 minutes;
confidence medium; fits. Existing guidance and coverage provide the starting
point; separate preparation/review stages and live evaluation are excluded.
