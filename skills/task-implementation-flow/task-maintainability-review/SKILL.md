---
name: task-maintainability-review
description: >
  Use after implementation or correction, before functional task-acceptance-review, when repository
  policy requires focused maintainability/architecture review or the user explicitly asks for it.
  Independently review current changed implementation assets, including significant tests, evaluations,
  fixtures and harness code, plus any required deterministic architecture
  gate for concrete regressions in semantic clarity, state/rule ownership, cohesion, coupling,
  change locality, testability, diagnosability, or abstraction cost. Return ACCEPT, CHANGES_REQUESTED, or INCONCLUSIVE. Do not
  perform full specification/functional acceptance here.
---
# Task Maintainability Review

Perform a **fresh, narrow architecture/maintainability review of the current change**.

The question is:

> Did this change introduce or materially worsen a concrete design condition that makes future changes, investigation, or verification unnecessarily difficult, expensive, or risky for human developers or agents?

## Review contract

Reviewed implementation assets include production code, tests, evaluations,
fixture/setup code and harness code, including tests-only submissions. Significant
test architecture is a risk reason to use this existing conditional review;
an ordinary assertion edit alone does not require this review. Significance
follows changed ownership, dependencies, scenario authority, isolation, oracle
structure or harness behavior, not file size or assertion counts.

For test assets, use relevant [testing-discipline](../../testing-discipline/SKILL.md)
guidance from the same installation root. Review introduced or materially worsened design
conditions; leave functional conformance and test adequacy to discovery/acceptance.

Focus on six ideas:

1. **Cohesion** — do responsibilities and names convey the behavior, state, units and contracts a caller must understand?
2. **Coupling** — did the change create unnecessary knowledge/dependency between components, fixtures or harness internals?
3. **Explicit dependencies** — can a reader trace decisions, data, collaborators and mutations without reconstructing hidden execution order or mutable setup?
4. **Change locality** — do important invariants, state transitions and scenario facts retain a clear owner, without duplicated authority or scattered coordinated edits?
5. **Testability** — can important changed behavior be exercised independently and repeatedly, and can failures be traced to useful causes and context?
6. **Proportionate abstraction** — do layers and helpers earn their navigation cost through a concrete boundary, variation, or test seam?

Treat these as review questions, not slogans.

## Independence

A verdict must come from a fresh reviewer that did **not** author any reviewed implementation assets, including test/eval/harness bytes.

Session authorship is the boundary. Loading this skill or changing roles in the same session does not create independence.

If this session authored any reviewed implementation assets:

- you may run the architecture gate and perform a labeled `SELF_CHECK_ONLY`;
- you may report findings to the implementer role;
- you **must not** emit `ACCEPT`, `CHANGES_REQUESTED`, or `INCONCLUSIVE` as an independent verdict for those bytes.

Every confirmed finding keeps a stable identity across reports. A correction,
including a tests-only correction, that changes bytes inside this review's reviewed scope invalidates
this verdict for the corrected bytes. Re-entry follows actual affected
reviewed scope and current evidence: demonstrably unaffected scope retains
this review as current evidence while that evidence stays applicable to the
submitted bytes. Stale, missing, or inapplicable proof never counts as a
completed stage — a prior verdict's label alone is not current evidence, and
the affected stage stays owed in its ordered position. Review affected
corrected bytes in a fresh reviewer session.

## Inputs

Use the smallest evidence packet that can answer the maintainability question:

Required when available:

- task/request or concise task summary
- current git diff/status and changed implementation assets
- repo-local `AGENTS.md` / `CLAUDE.md`
- relevant project/architecture map or ADR for the changed boundary
- canonical architecture-gate command and current policy/config/tests
- `.quality/gates.yaml` or repo-equivalent command registry when present
- current architecture-gate output

When a durable task brief is supplied, require the package form
`<task-package>/brief.md`; route a direct legacy brief to
`task-brief-designer` for normalization. When a durable maintainability report
is requested, write only the next unused
`<task-package>/reviews/maintainability-NN.md`. Never overwrite a prior report
or use an external runtime directory as the durable report location.

Read immediate neighboring modules/interfaces only when needed to understand the changed dependency or responsibility.

Do **not** begin with a repo-wide architecture survey.

Review is read-only except the permitted new durable report. Do not edit
production, test/eval/fixture/harness assets, install tools, or execute downstream
stages as reviewer actions.

Do not require the complete product specification merely to decide maintainability. Read enough task context to distinguish intentional scope from accidental broadening; leave full AC/spec conformance to `task-acceptance-review`.

## Protocol

### 1. Establish provenance and reviewed bytes

Before judging:

- confirm this is an independent session for the actual reviewed assets;
- inspect git status/diff so the reviewed change is concrete;
- identify changed production, test/eval/fixture/harness assets and necessary immediate neighbors; distinguish docs/generated output and record the actual reviewed scope;
- note pre-existing dirty work and avoid attributing unrelated changes to this task.

If ownership/provenance makes it impossible to identify the current task bytes responsibly, return `INCONCLUSIVE` rather than guessing.

### 2. Discover and run the deterministic architecture gate first

Find the canonical architecture command from repo authority, preferably:

1. `.quality/gates.yaml` or repo-equivalent machine registry;
2. `AGENTS.md` / `CLAUDE.md`;
3. project/architecture map;
4. package/build/task-runner config only if the command is not documented elsewhere.

If repo policy says the gate is required, run it against the current bytes when feasible.
Do not create a gate when policy does not require one.

Interpret results as follows:

- **new/worsened HARD violation:** `CHANGES_REQUESTED` unless the evidence is actually a checker/config defect;
- **unchanged baselined legacy violation:** not a blocker for this task;
- **WARNING / heuristic signal:** investigate semantically; do not fail automatically;
- **required gate cannot be executed or trustworthy fresh evidence is unavailable:** normally `INCONCLUSIVE` unless the repo explicitly documents a valid exception;
- **gate passes:** continue semantic review; a green dependency graph is not a maintainability verdict.

Do not edit architecture config, exceptions, or baselines to make review pass. A baseline expansion is itself a foundation/architecture change, not reviewer cleanup.

### 3. Review responsibility and semantic clarity

Trace a representative changed path through decisions, transformations,
mutations and failures. Compare with the baseline and established contracts:
what must the next developer or agent reconstruct to change it safely?

Look for mixed reasons-to-change or names that materially misrepresent a
responsibility, unit, state, result or side effect: e.g. a query-like helper
consuming state or seconds-named values carrying milliseconds. Show the mismatch
and credible modification it risks, even when current outputs are correct.
Check local definitions and external contracts; unfamiliar or short names alone
are not findings.

Inspect unnecessary indirection, hidden mutations, order-dependent helpers and
decision logic that obscures the determining rule. Explain the extra navigation
or execution knowledge needed and a bounded correction. Branch count, nesting
and file length alone prove nothing; explicit protocol branches can be justified.

### 4. Review coupling and dependency direction

Inspect changed edges and immediate collaborators for private reach-through,
hidden global/service-locator dependencies, unnecessarily broad injected
capabilities, or bidirectional/cyclic coupling against established ownership.
Check whether domain rules now reach into concrete infrastructure instead of
using the existing boundary. Identify the unnecessary knowledge a caller must
acquire or keep synchronized.

For test assets, inspect fragile mutable fixtures, unclear/cross-owner coupling,
and harness-internal dependencies. Show the introduced isolation, repeatability
or ownership consequence rather than blocking merely because setup is shared.

Do not demand an interface for every concrete class. Dependency inversion is useful when it protects an actual boundary/test seam/variation, not as ritual.

### 5. Review change locality and state/rule ownership

Ask a concrete near-future question:

> If the next **same-kind** behavior/variant were added, would it normally stay near this subsystem, or would it require editing multiple unrelated modules/dispatchers because of the structure introduced here?

Locate the owner of each important changed invariant and state transition.
Look for duplicated business policy, scattered writes/invalidation rules,
repeated dispatch or registrations that now require coordinated edits without
necessity. Trace reads and writes of the affected state: a rule can become
scattered across partial updates without any text being copied. Name the
concrete rule change that would require finding and updating those sites.

For tests/evals, inspect duplicated scenario authority: one scenario fact now
requires synchronized edits across owners. A one-owner change divergence is
concrete evidence. Repeated construction at legitimate separate observation
boundaries does not alone establish a blocker.

Mechanical code duplication is not automatically duplicated authority. Separate
validation at trust boundaries, derived projections and explicit transitions
can be justified. Do not invent a plugin system for one case or demand one
writer for every field; establish avoidable coordination cost in this change.

### 6. Review testability and diagnosability

Focus on **important changed behavior**, not a universal mocking preference.

Block when the change unnecessarily makes important deterministic logic inseparable from:

- network calls
- database/filesystem operations
- framework runtime/global state
- clock/randomness/process environment without an existing controllable seam

and that coupling materially prevents reliable focused verification.

Do not require pure unit tests for code whose behavior is inherently an integration boundary. The question is whether avoidable coupling made verification harder.

Inspect incidental text/layout assertions that couple a scenario to unrelated
formatting instead of its observation contract. Stable textual contracts remain
legitimate; explain the concrete maintenance consequence before blocking.

Trace relevant changed failures to available diagnostic evidence. Does a wrapper,
fallback or translation discard cause, operation identity or state context with
no usable alternative? Show the lost distinction and investigation cost. Do not
mandate logging, expose sensitive data, or reject public error boundaries that
retain appropriate internal evidence. Functional failure behavior and test
adequacy remain discovery/acceptance responsibilities.

### 7. Review abstraction cost and calibrate findings

Inspect speculative abstraction, including fixture/harness helpers: layers that
merely forward calls, duplicate an existing abstraction, or add navigation cost
without localizing policy, a current variation, dependency boundary or test seam.
Respect abstractions that serve those purposes.

Connect each candidate's diff evidence to a credible future change, investigation
or verification task and avoidable cost/risk. Respect repo conventions and
justified trade-offs; reject preferences and speculative redesigns. Report each
root cause once across dimensions. A small rename can resolve a material
contract trap; correction size does not determine impact.

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

### 9. Report every confirmed blocker

Report **every confirmed blocker** found within the bounded review scope, ordered by architectural impact.

Give every confirmed finding a **stable finding ID** such as `MNT-01`,
independent of display order. Identity is a producer obligation, not a
fixture convention: prior reports remain unchanged, a resolved ID is never
recycled, and a newly confirmed finding receives an identity no earlier
report or resolved finding already used. After a correction round, the next
report keeps the surviving findings' IDs and the corrected finding's ID with
its current disposition and evidence.

Finding count or verdict sufficiency cannot end discovery, cap the output, or relegate a confirmed blocker to warnings to keep the list short. Completeness does not authorize a wider survey or a quota of findings; scope and materiality still decide what belongs in the blocker list.

Each blocker must include:

- its stable finding ID (for example `MNT-01`)
- file/location or concrete dependency edge
- the exact introduced/worsened problem
- evidence
- maintainability consequence
- smallest reasonable correction direction

Give a bounded direction, such as using the existing repository port or keeping
fee policy in its domain owner. Do not prescribe a full implementation,
architecture rewrite or arbitrary class split.

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
- semantic review finds a concrete high-impact regression under the review contract with actionable evidence.

#### `INCONCLUSIVE`

Use when required evidence cannot be established responsibly, for example:

- required architecture gate cannot run and no valid fresh result exists;
- changed implementation-asset ownership cannot be determined;
- required architecture policy/authority is contradictory or unavailable;
- environment/tool failure prevents distinguishing implementation failure from verifier failure.

Do not use `INCONCLUSIVE` merely because you cannot prove the design is globally optimal.

#### Genuine stops

A specific permission, capability, or safe-budget limit — never finding count or verdict sufficiency — is the only reason to stop before the bounded review scope is complete. On a genuine stop, retain every confirmed finding with its full evidence, its stable ID, and its current disposition, name the outstanding coverage, the concrete stop reason, and the next owner, and treat missing required proof as an incomplete review; it cannot become `ACCEPT` or a claim of cleanly completed review.

## Output

Return this compact form:

```text
VERDICT: ACCEPT | CHANGES_REQUESTED | INCONCLUSIVE
ARCHITECTURE_GATE: PASS | FAIL | NOT_AVAILABLE

BLOCKERS:
<one numbered entry per confirmed blocker, ordered by architectural impact, or NONE>
1. MNT-01 — <file/location>
   - Problem: <concrete introduced/worsened issue>
   - Evidence: <diff/dependency/gate evidence>
   - Maintainability impact: <concrete future change, investigation or verification made harder/riskier>
   - Smallest correction direction: <bounded direction, not redesign>
   - Current disposition: <confirmed, or resolved/corrected with current evidence>

WARNINGS:
- <non-blocking evidence worth carrying forward, max 3, or NONE>

REVIEWED:
- changed implementation scope: <production/test/eval/fixture/harness paths and reviewed-byte identities>
- architecture command: <command or NONE>
- policy/boundary sources: <paths>
```

If this session authored reviewed implementation assets, output instead:

```text
SELF_CHECK_ONLY
ARCHITECTURE_GATE: PASS | FAIL | NOT_AVAILABLE
FINDINGS:
- <MNT-NN finding or NONE>
REVIEWED:
- <actual implementation assets and reviewed-byte identities>
```

and do not issue an independent verdict.

When repository/user authority requires a durable report, store this output at
the canonical numbered path above. Record exact Git status before and after the
write and permit only the new report entry; the report does not review itself.

## Correction loop

For `CHANGES_REQUESTED`:

1. send the complete concise blocker report to the implementation/correction agent;
2. the implementation/correction agent fixes only the blockers without changing requested behavior unnecessarily;
3. rerun the canonical architecture gate when required and affected;
4. use a **fresh** `task-maintainability-review` session on the corrected bytes;
5. only after `ACCEPT`, name the first outstanding stage and the complete
   ordered remainder of the submission route: applicable
   `task-contract-registry-updater` synchronization when the flow includes a
   registry stage and the change added, changed, or removed a durable
   cross-task contract, then fresh independent `task-review-discovery`
   evidence, then the separate functional `task-acceptance-review` decision
   when that stage is required.

Naming the route hands off the next owners without executing any named
stage; this review never launches, delegates to, or waits for them. Include
a stage only when it is required and still outstanding for the submitted
bytes: current applicable evidence for a completed stage leaves it out of
the outstanding remainder, applicable registry work cannot be dropped, and
an absent registry stage cannot be invented.

If functional acceptance later changes reviewed implementation assets, re-enter only the
conditional stages whose reviewed scope the correction affected — the
required architecture gate and a fresh maintainability review when their
reviewed scope changed, and applicable registry synchronization when the
registry stage applied and the correction affected its scope — before fresh
discovery evidence and fresh functional acceptance.

A tests-only label alone never waives an affected required review. Explicit
policy-authorized trivial-change exceptions apply only within their authorized
scope; carry all remaining obligations in order. Do not invent a gate or
registry work for every test change.

## Definition of Done

- Reviewer independence/provenance is explicit.
- Required deterministic architecture gate was run or a truthful reason for `INCONCLUSIVE` is recorded.
- Existing untouched debt is not relitigated as a task blocker.
- Hard failures are separated from advisory signals.
- Semantic review is limited to the changed design and immediate architectural impact.
- Every confirmed concrete blocker in the reviewed scope is reported; count is neither a limit nor a quota.
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
- Padding the blocker list with low-value nits, preferences, or speculative redesigns instead of the confirmed material maintainability risks.


<!-- contract-registry-flow:task-maintainability-review:begin -->
## Contract-registry stage boundary

When the standard task flow includes `task-contract-registry-updater`, this review runs **before** registry/reference synchronization. Do not fail an otherwise maintainable implementation merely because `docs/contracts` or explanatory discovery references still need the dedicated post-review sync.

Still review executable/declarative contracts that are part of the implementation itself, and call out any actual reusable boundary or ownership change the registry updater will need to reconcile. If production/test/executable-contract bytes change after this review, normal review invalidation rules still apply.
<!-- contract-registry-flow:task-maintainability-review:end -->
