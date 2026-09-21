---
name: task-maintainability-review
description: >
  Use after implementation or correction, before functional task-acceptance-review, when repository
  policy requires focused maintainability/architecture review or the user explicitly asks for it.
  Independently review the current changed production bytes plus the repo's deterministic architecture
  gate for concrete cohesion, coupling, change-locality, dependency, testability, duplication, or
  speculative-abstraction regressions. Return ACCEPT, CHANGES_REQUESTED, or INCONCLUSIVE. Do not
  perform full specification/functional acceptance here.
---
# Task Maintainability Review

Perform a **fresh, narrow architecture/maintainability review of the current change**.

The question is:

> Did this change introduce or materially worsen a concrete design condition that makes expected future changes unnecessarily broader, more coupled, harder to test, or easier to break?

## Review contract

Focus on six ideas:

1. **Cohesion** — does each changed module still have a clear responsibility?
2. **Coupling** — did the change create unnecessary knowledge/dependency between components?
3. **Explicit dependencies** — are important collaborators/boundaries visible rather than hidden through unrelated infrastructure/global state?
4. **Change locality** — would the next closely related variant be local to its owning subsystem, or did this change spread one behavior across unrelated modules?
5. **Testability** — can important changed logic be exercised without unnecessary external I/O/infrastructure?
6. **Proportionate abstraction** — did the change reuse existing patterns and add abstraction only where a concrete boundary, variation, or test seam justifies it?

Treat these as review questions, not slogans.

## Independence

A verdict must come from a fresh reviewer that did **not** author the production bytes being reviewed.

Session authorship is the boundary. Loading this skill or changing roles in the same session does not create independence.

If this session authored any reviewed production bytes:

- you may run the architecture gate and perform a labeled `SELF_CHECK_ONLY`;
- you may report findings to the implementer role;
- you **must not** emit `ACCEPT`, `CHANGES_REQUESTED`, or `INCONCLUSIVE` as an independent verdict for those bytes.

Every production correction invalidates the previous maintainability verdict. Review corrected bytes in a fresh reviewer session.

## Inputs

Use the smallest evidence packet that can answer the maintainability question:

Required when available:

- task/request or concise task summary
- current git diff/status and changed production files
- repo-local `AGENTS.md` / `CLAUDE.md`
- relevant project/architecture map or ADR for the changed boundary
- canonical architecture-gate command and current policy/config/tests
- `.quality/gates.yaml` or repo-equivalent command registry when present
- current architecture-gate output

Read immediate neighboring modules/interfaces only when needed to understand the changed dependency or responsibility.

Do **not** begin with a repo-wide architecture survey.

Do not require the complete product specification merely to decide maintainability. Read enough task context to distinguish intentional scope from accidental broadening; leave full AC/spec conformance to `task-acceptance-review`.

## Protocol

### 1. Establish provenance and reviewed bytes

Before judging:

- confirm this is an independent session for the production bytes;
- inspect git status/diff so the reviewed change is concrete;
- identify changed production/source files separately from tests/docs/generated output;
- note pre-existing dirty work and avoid attributing unrelated changes to this task.

If ownership/provenance makes it impossible to identify the current task bytes responsibly, return `INCONCLUSIVE` rather than guessing.

### 2. Discover and run the deterministic architecture gate first

Find the canonical architecture command from repo authority, preferably:

1. `.quality/gates.yaml` or repo-equivalent machine registry;
2. `AGENTS.md` / `CLAUDE.md`;
3. project/architecture map;
4. package/build/task-runner config only if the command is not documented elsewhere.

If repo policy says the gate is required, run it against the current bytes when feasible.

Interpret results as follows:

- **new/worsened HARD violation:** `CHANGES_REQUESTED` unless the evidence is actually a checker/config defect;
- **unchanged baselined legacy violation:** not a blocker for this task;
- **WARNING / heuristic signal:** investigate semantically; do not fail automatically;
- **required gate cannot be executed or trustworthy fresh evidence is unavailable:** normally `INCONCLUSIVE` unless the repo explicitly documents a valid exception;
- **gate passes:** continue semantic review; a green dependency graph is not a maintainability verdict.

Do not edit architecture config, exceptions, or baselines to make review pass. A baseline expansion is itself a foundation/architecture change, not reviewer cleanup.

### 3. Review responsibility / cohesion

Look for **introduced or materially worsened** mixed reasons-to-change.

Useful questions:

- What primary responsibility did this module have before the change?
- What independent reason-to-change did the new code add?
- Are orchestration, domain rules, persistence, transport, rendering, external API calls, configuration, or unrelated concerns being combined merely because the file was convenient?
- Does the changed logic depend on a different collaborator set or lifecycle than the module's existing job?

A large file is not automatically a god file. Block only when the diff gives concrete evidence of unrelated responsibility growth or similar cohesion loss.

### 4. Review coupling and dependency direction

Inspect new/changed dependency edges and immediate collaborators.

Look for:

- business/domain logic reaching directly into concrete external infrastructure when an existing boundary should own that dependency;
- reach-through into another module's private internals instead of its established public surface;
- hidden global/service-locator dependencies;
- broad dependency injection where the component needs only a narrow capability;
- new bidirectional/cyclic coupling where the repo expects one-way ownership;
- one feature change requiring knowledge of several unrelated subsystem internals.

Do not demand an interface for every concrete class. Dependency inversion is useful when it protects an actual boundary/test seam/variation, not as ritual.

### 5. Review change locality / extension shape

Ask a concrete near-future question:

> If the next **same-kind** behavior/variant were added, would it normally stay near this subsystem, or would it require editing multiple unrelated modules/dispatchers because of the structure introduced here?

Look for:

- behavior encoded in repeated type checks across unrelated files;
- a growing `switch` / `if` dispatcher where the repo already has a clear extension mechanism;
- registrations/variants that require coordinated edits in several owners without necessity;
- duplicated business policy that must stay synchronized.

Do not invent speculative plugin systems for one known case. One extra branch is not automatically an OCP violation; block only when the current change concretely worsens an already meaningful extension point or creates duplicated coordination cost.

### 6. Review testability

Focus on **important changed behavior**, not a universal mocking preference.

Block when the change unnecessarily makes important deterministic logic inseparable from:

- network calls
- database/filesystem operations
- framework runtime/global state
- clock/randomness/process environment without an existing controllable seam

and that coupling materially prevents reliable focused verification.

Do not require pure unit tests for code whose behavior is inherently an integration boundary. The question is whether avoidable coupling made verification harder.

### 7. Review duplication and abstraction cost

Look for two opposite failure modes.

#### Duplicated authority

Potential blocker when the change introduces a second copy of business/domain policy that must remain synchronized with an existing source of truth.

Mechanical code duplication is not automatically architectural duplication.

#### Speculative abstraction

Potential blocker when the change adds layers/interfaces/factories/providers/registries that:

- have no current boundary or variation to protect;
- merely forward calls without isolating dependency or policy;
- increase navigation/cognitive cost more than they localize change;
- duplicate an existing repo abstraction.

Do not penalize a small abstraction that clearly creates a required test seam or external boundary.

### 8. Use automated signals as leads, not verdicts

Examples:

```text
file LOC:             330 -> 520
cyclomatic complexity: 8 -> 16
direct dependencies:   7 -> 14
new generic helper:     yes
```

For each warning ask:

1. What concrete design change caused the delta?
2. Does it correspond to one of the review-contract problems above?
3. Was that problem introduced/worsened by this task?
4. Is there a smaller correction that preserves requested behavior?

If not, keep it in `WARNINGS` or omit it.

### 9. Keep blockers finite and actionable

Report at most **3 blockers**, ordered by architectural impact.

Each blocker must include:

- file/location or concrete dependency edge
- the exact introduced/worsened problem
- evidence
- maintainability consequence
- smallest reasonable correction direction

Do not prescribe a full implementation unless necessary to explain the boundary. Prefer directions such as:

- move deterministic fee policy out of HTTP adapter into the existing payment domain service;
- use the existing repository port instead of importing the Postgres adapter;
- keep receipt rendering behind the existing receipt boundary rather than adding it to payment orchestration.

Avoid directions such as:

- rewrite to Clean Architecture;
- split this into five classes;

### 10. Decide the verdict

#### `ACCEPT`

Use when:

- any required deterministic architecture gate passes for the current bytes;
- no concrete maintainability regression introduced/materially worsened by the task remains;
- unresolved warnings are non-blocking.

`ACCEPT` means only maintainability review accepted these bytes. It does **not** mean the task works or satisfies the specification.

#### `CHANGES_REQUESTED`

Use when at least one is true:

- current task introduces/worsens a hard architecture violation;
- semantic review finds a concrete high-impact cohesion/coupling/locality/testability/duplication/abstraction regression with actionable evidence.

Do not keep searching for minor issues after enough decisive blockers are established.

#### `INCONCLUSIVE`

Use when required evidence cannot be established responsibly, for example:

- required architecture gate cannot run and no valid fresh result exists;
- changed production-byte ownership cannot be determined;
- required architecture policy/authority is contradictory or unavailable;
- environment/tool failure prevents distinguishing implementation failure from verifier failure.

Do not use `INCONCLUSIVE` merely because you cannot prove the design is globally optimal.

## Output

Return this compact form:

```text
VERDICT: ACCEPT | CHANGES_REQUESTED | INCONCLUSIVE
ARCHITECTURE_GATE: PASS | FAIL | NOT_AVAILABLE

BLOCKERS:
1. <file/location or NONE>
   - Problem: <concrete introduced/worsened issue>
   - Evidence: <diff/dependency/gate evidence>
   - Maintainability impact: <why future change/refactor becomes riskier>
   - Smallest correction direction: <bounded direction, not redesign>

WARNINGS:
- <non-blocking evidence worth carrying forward, max 3, or NONE>

REVIEWED:
- changed production scope: <paths/summary>
- architecture command: <command or NONE>
- policy/boundary sources: <paths>
```

If this session authored reviewed production bytes, output instead:

```text
SELF_CHECK_ONLY
ARCHITECTURE_GATE: PASS | FAIL | NOT_AVAILABLE
FINDINGS:
- <finding or NONE>
```

and do not issue an independent verdict.

## Correction loop

For `CHANGES_REQUESTED`:

1. send the complete concise blocker report to the implementation/correction agent;
2. fix only the blockers without changing requested behavior unnecessarily;
3. rerun the canonical architecture gate;
4. use a **fresh** `task-maintainability-review` session on the corrected bytes;
5. only after `ACCEPT`, proceed to functional `task-acceptance-review` when that stage is required.

If functional acceptance later changes production bytes, repeat architecture gate + fresh maintainability review before fresh functional acceptance.

## Definition of Done

- Reviewer independence/provenance is explicit.
- Required deterministic architecture gate was run or a truthful reason for `INCONCLUSIVE` is recorded.
- Existing untouched debt is not relitigated as a task blocker.
- Hard failures are separated from advisory signals.
- Semantic review is limited to the changed design and immediate architectural impact.
- No more than 3 concrete blockers are reported.
- Functional/specification acceptance was left to the functional reviewer.

## Anti-patterns

- Failing solely because a file/class/function is large.
- Penalizing code because the reviewer prefers another pattern.
- Forcing interfaces, factories, repositories, or layers without a concrete need.
- Reviewing the whole repository instead of the current change.
- Blocking on pre-existing untouched debt.
- Redesigning product architecture during read-only review.
- Rechecking every acceptance criterion and starving the architecture question of context.
- Editing the architecture baseline to make the current task pass.
- Reporting ten low-value nits instead of the few material maintainability risks.


<!-- contract-registry-flow:task-maintainability-review:begin -->
## Contract-registry stage boundary

When the standard task flow includes `task-contract-registry-updater`, this review runs **before** registry/reference synchronization. Do not fail an otherwise maintainable implementation merely because `docs/contracts` or explanatory discovery references still need the dedicated post-review sync.

Still review executable/declarative contracts that are part of the implementation itself, and call out any actual reusable boundary or ownership change the registry updater will need to reconcile. If production/test/executable-contract bytes change after this review, normal review invalidation rules still apply.
<!-- contract-registry-flow:task-maintainability-review:end -->
