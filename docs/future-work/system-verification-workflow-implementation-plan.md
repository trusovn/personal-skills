# System Verification Planning and Closure — Implementation Plan

**Status:** Proposed design / implementation roadmap  
**Date:** 2026-10-09  
**Primary target:** New projects and small-to-medium existing projects under continuous, agent-assisted development  
**Future compatibility:** Larger brownfield systems, without requiring their discovery/assurance machinery in V1

## 1. Intent

Improve the Personal Skills planning and implementation workflow so independently executed tasks contribute to an **explicit, executable system-level verification strategy**. The main goal is not to produce more test cases at planning time. It is to decide **which risks and behaviors need proof, at which real boundary, with which testing approach, and who will supply that proof**.

The resulting workflow should:

- Connect project-wide verification decisions to individual task briefs, task verification designs, implementation and independent acceptance.
- Check relevant existing integrations **before** a task changes them, and relevant existing/new integrations **after** the task, without routinely rerunning the whole product.
- Ensure critical journeys composed from multiple tasks are verified when they become runnable and again at final system closure where appropriate.
- Distinguish intended test coverage from *actually executed, current* evidence.
- Report missing, unavailable or non-automatable verification explicitly at the end of planning and at project completion.
- Increase the proportion of completion evidence that an agent can produce without human participation, while preserving independent acceptance and truthful limitations.

**Non-goal:** Build a heavy master test management system or fully investigate an existing repository before a project can be planned.

## 2. Starting point and boundaries

The current repository already provides useful foundations:

| Existing capability | Preserve / extend |
| --- | --- |
| `project-delivery-plan` and `docs/task-map.json` | Continue to own intended system flows, interfaces, invariants, tasks and dependencies. Its existing system verification map is the starting signal, not the complete strategy. |
| `testing-discipline` | Remain the reusable source of test selection, test design, oracle quality, determinism, test data and risk-based evidence guidance. Do not duplicate a test methodology manual in the new skill. |
| `project-plan-verification` | Remain a fresh, independent review of planned system coherence; extend it to examine the verification strategy and its fit with the delivery plan. |
| `task-brief-designer` / `task-verification-designer` | Continue to own bounded task contracts and implementation-neutral, task-local verification scenarios. Do not assign sibling-task integration closure to the task verification designer. |
| `bounded-task-implementer` / `task-acceptance-review` | Continue to implement and independently evaluate a bounded task, with relevant existing-context regression/integration evidence. |
| `repo-foundation`, `architecture-guardrails`, implemented contract registry | Remain authorities for real test commands, test placement, hard architectural constraints and currently implemented contract discovery. |

This work is an **extension across existing ownership boundaries**, not a replacement of the existing workflow or a requirement that every project use every skill.

## 3. Design principles

1. **Progressive discovery.** Use existing project maps, foundation artifacts, implemented-contract records, code declarations and previous plans first. Before planning, inspect only enough to identify material system components, boundaries, data flows and obvious uncertainty. Perform deeper investigation only when a flow, proposed task, test oracle or integration obligation makes it necessary.
2. **Current state is not planned state.** Existing system information describes what is implemented or observed; the delivery plan describes proposed future behavior. Neither should silently substitute for the other.
3. **One owner per decision.** Product behavior belongs to approved direction/requirements; cross-task behavior and task structure belong to the delivery plan; test architecture belongs to the verification strategy; task-specific scenarios belong to task verification design; current runnable commands and real contracts belong to the repository.
4. **Evidence at the cheapest decisive boundary.** Prefer unit/component evidence for local semantics, real integration/contract evidence for decisive external boundaries, and a small number of UI/API/system E2E journeys for cross-component behavior and runtime wiring. A label such as “API test” is insufficient: record what is real versus substituted.
5. **Testability is a planning constraint.** If required behavior cannot be observed or exercised, raise a design or dependency issue while the plan can still change. Do not turn ordinary test convenience into unjustified architecture mandates.
6. **Test techniques are selected, not assigned by quota.** Include example-based, property-based, stateful/model-based, fuzz/metamorphic and other methods where their oracles and cost justify them. Property-based testing complements, rather than universally replaces, explicit examples.
7. **Separation of authorship and acceptance.** Implementers can design, execute and fix tests; an independent review context must make the acceptance claim. A reviewer should not silently fix missing tests and approve its own changes.
8. **Small first.** Avoid compulsory full scans, elaborate registries, universal CI jobs, mandatory standalone plans for trivial changes and broad brownfield modernization.

## 4. Artifacts and source-of-truth rules

### 4.1 Lightweight current-system context

Introduce a **small common context contract**, not an exhaustive system inventory. For a new project with adequate existing foundation artifacts, there may be very little to add. For extensions, prefer updating/referencing previously established information.

The logical schema should capture only what later planning or test design needs:

- **System elements:** implemented components/services/modules and their responsibility.
- **Dependencies:** important internal and external dependencies; note which are real, replaceable, unavailable or not yet understood.
- **Boundaries:** public interfaces, persistence/process/network boundaries and references to implemented contracts or executable declarations.
- **Data/state flows:** key *currently implemented* paths and state transitions at high level, not every function call.
- **Verification capabilities:** canonical test/smoke commands, runnable environments, fixtures, determinism controls and known limitations.
- **Provenance and certainty:** source links/paths, `observed | verified | assumed | unknown` classification, and enough freshness information to avoid treating stale notes as live proof.

Prefer a compact machine-readable **context index/manifest** with stable references when the repository does not already provide a suitable equivalent. A possible default is `docs/system-context.json`, but do not require that exact file or an additional full registry if existing repository artifacts can express the same contract. The index is a navigation and planning aid, **not** a duplicated authoritative implementation specification. It should link to existing project/architecture maps, schemas, contract registry entries and commands instead of copying them wholesale.

**Acquisition policy:**

- Start with existing artifacts and a bounded repository orientation pass.
- Mark unknowns honestly; do not block high-level planning solely to catalog unrelated subsystems.
- Deepen only the subset implicated by a planned flow, changed dependency or intended verification boundary.
- Update a record when work changes that implemented fact; do not regenerate the whole map after each task.
- Keep intended-to-implemented links explicit when plan IDs such as `FLOW-*`, `IF-*` and `INV-*` become real, without marking planned behavior as implemented prematurely.

**Later brownfield extension:** An optional pre-planning survey skill may populate the same contract through wider discovery, baseline characterization and legacy-risk inventory. **Do not implement that specialist skill in V1.**

### 4.2 System verification strategy

Create a compact, separately reviewable artifact, by default `docs/system-verification-strategy.md` (or a repository-declared equivalent), for projects whose cross-task verification decisions benefit from separation.

It should contain:

1. Scope, system context references, assurance priorities and meaningful exclusions.
2. Critical behavior/risk map referencing existing capability, flow, interface and invariant IDs.
3. **Test architecture:** selected unit, component, real integration, contract, API/system E2E, browser/UI E2E, smoke and specialized evidence; decisive real boundaries and oracles; rationale for distinct layers.
4. **Technique policy:** where examples, boundaries, properties, state models and other generators add value; minimum semantic anchors and conditions under which a technique is unsuitable.
5. **System verification obligations** with stable IDs (e.g. `SV-001`), the behavior/risk they prove, intended observation boundary, evidence kind, required/optional classification, owning task or milestone, prerequisites and point at which they become runnable.
6. Test environment/data/diagnostic dependencies and how automated agents can start, stimulate, observe, isolate and clean up critical flows.
7. Known gaps: missing oracle, unavailable environment, manual judgment, accepted exclusions, and proposed prerequisite work or decision owner.
8. Completion criteria: what must be proven by task acceptance, milestone integration and final system closure.

**Keep it strategic.** No giant BDD case list, premature test file design, mandatory framework choices or complete per-task test specifications. Task-level `verification.md` remains the place for falsifiable scenarios.

If the work is a truly small localized change with no meaningful cross-task decision, its verification intent can stay inline in existing planning/brief artifacts. The separate document becomes the default for multi-task projects with real integration or system-level risks, not an unconditional requirement.

### 4.3 Verification obligations and gap status

A verification obligation is **not a test case**. It says what evidence must eventually exist, where, why and who owns its completion.

Maintain stable links among:

`CAP/FLOW/IF/INV -> SV obligation -> task/milestone owner -> actual evidence -> final disposition`.

Use simple planning and execution states, without building a new task-tracking platform:

- **Planning:** `planned`, `needs_prerequisite`, `explicitly_deferred` (with reason/owner).
- **Execution/review:** `proven`, `failed`, `blocked`, `not_run`, `not_applicable` (with evidence or reason).

Avoid silently converting `blocked`/`not_run` into success. A changed strategy does not retroactively establish evidence. Final reporting must show what was planned, what actually ran, and what remains unverified.

## 5. Target workflow

```text
Existing project authority + foundation + available current-state artifacts
  -> Bounded context orientation (no full-system scan)
  -> Project delivery plan, draft
       (flows, interfaces, invariants, tasks, preliminary verification concerns)
  -> System verification strategy
       (real test boundaries, oracles, techniques, ownership, constraints)
  -> Reconcile delivery plan with verification strategy
       (task dependencies, enabling work, integration ownership)
  -> Independent project-plan verification of the whole planning package
  -> For each task:
       task brief + relevant strategy references
       -> optional task verification design
       -> targeted existing-context/baseline verification
       -> implementation + task-local tests
       -> targeted post-change integration/regression
       -> independent task acceptance
       -> implemented-context / contract synchronization when relevant
  -> Milestone integration verification when composed paths become runnable
  -> Final independent system verification and closure
       -> bounded correction/test tasks, if necessary -> fresh re-review
       -> final coverage/evidence/gap report
```

### 5.1 Discovery before and during planning

Before draft planning, answer only: what important pieces already exist, what crosses their boundaries, what commands/evidence are available and what facts are uncertain? If prior artifacts answer this, **reuse them without a fresh survey**.

The delivery plan then drives focused investigation. Examples: a new flow crosses an existing database contract; an intended E2E path depends on a background job; an old API adapter may lack a realistic test substitute. Investigate these precisely when they become relevant, not as a prerequisite to planning every feature.

### 5.2 Planning and reconciliation

Keep the `project-delivery-plan` author responsible for planned system behavior and task placement. Use a separate `system-verification-strategy` pass to challenge the proposed allocation of proof. That pass may discover missing testability infrastructure or an unowned integration obligation; it **reports the need**, rather than silently redesigning application behavior or rewriting approved direction.

The planning owner reconciles the two artifacts. Introduce enabling/integration tasks **only** for a real shared dependency or an otherwise unowned critical proof. Every critical multi-task journey must have a specified time and owner for its composed verification. The independent plan reviewer checks the reconciled package, not just the original implementation plan.

Avoid infinite planning loops: one initial strategy pass and focused reconciliation is the standard route. Repeat only for a material unresolved conflict or consequential plan change.

### 5.3 Task start: targeted baseline

Before changing code, determine which **already implemented** contracts and integrations this task could affect. Run appropriate available checks where practical, or record why none exist or cannot run. A baseline establishes what was already passing or failing; it is **not** a mandate to run a full regression suite for every task.

For first greenfield slices, the baseline may consist only of build/smoke/foundation commands. A dependent component that is not yet implemented cannot be claimed as verified; its composed proof stays assigned to the future owning milestone/task.

### 5.4 Task completion: targeted integration

After task-local tests, verify the real boundary the task newly supplies or changes, plus important neighboring contracts. Existing integration tests may be reused; add a focused test when the boundary is material and lacks decisive evidence. Record commands, fixtures/state, actual observations, impacted obligation IDs and any skipped stronger check.

The independent acceptance reviewer must distinguish:

- task-local behavior proven;
- integration with existing context proven;
- cross-task/system obligations still pending because the whole path is not yet runnable.

A task should not claim system-level completion merely because isolated tests pass. Conversely, do not block a task on unrelated future components when its planned handoff and deferred integration owner are explicit.

### 5.5 Milestone and final system closure

Verify composed flows **as soon as they become runnable**, rather than accumulating all integration risk until the final review. The completion pass then independently examines the **actual implemented system** against approved direction, delivery plan, verification strategy and evidence, including newly discovered risks not enumerated by the strategy.

Closure work must:

1. Reconstruct critical user/system journeys and identify real boundaries exercised.
2. Validate required `SV-*` obligations against current tests, commands and independent probes.
3. Execute justified system-wide E2E, integration, contract, smoke and other release-relevant gates in permitted environments.
4. Identify missing, weak, stale or incorrectly passing tests and unimplemented requirements.
5. Route in-scope corrections/missing evidence into bounded implementation or test tasks; after their completion obtain a fresh independent review of changed bytes.
6. Report all blocked, omitted, externally dependent, manual-only and consciously excluded evidence, with consequence and disposition.

This is a **distinct independent system review/closure responsibility**. In V1 it can be introduced as a lean, explicit skill or narrowly defined review mode; do not overload `task-verification-designer` or allow same-context self-acceptance. Choose the smallest interface that remains independently executable and produces a durable final report.

Suggested final conclusions: `VERIFIED`, `VERIFIED_WITH_ACCEPTED_LIMITATIONS`, or `INCOMPLETE/BLOCKED`. Acceptance of a material limitation requires an explicit authorized decision; the reviewer cannot grant it just to close the plan.

## 6. Test design guidance to propagate

### Test-level allocation

- Use unit/component evidence for deterministic local logic and interaction semantics.
- Use integration tests when real persistence, process execution, serialization, concurrency, filesystem or framework wiring is decisive.
- Use contract tests for independently changing producer/consumer compatibility; do not treat them as a substitute for functional integration.
- Distinguish API tests of a mocked handler from API E2E against a running integrated application.
- Reserve browser E2E for a small set of critical user journeys and browser-specific/wiring risks; use component/API tests for most fine-grained cases.
- Avoid duplicating the same scenario across layers unless each layer protects a genuinely distinct failure mode.

### Property-based, model-based and TDD guidance

- Evaluate property opportunity for material invariant-rich areas; do not set test-count quotas.
- Keep explicit semantic anchors for business rules and known examples. Add generated properties only with valid domains, trustworthy independent oracles, reproducible seeds/shrinking and acceptable runtime.
- Prefer stateful/model-based testing for meaningful workflow and lifecycle invariants where generated operation sequences expose interaction defects.
- Use test-first or demonstrate intended test failure before relying on new behavior when practical; preserve characterization behavior where legacy constraints require it.
- Treat mutation/fault-sensitivity checks selectively as validation of important tests, not universal ceremony.
- Let testability guide legitimate seams and dependency boundaries; use deterministic architecture checks only for enforceable decided rules. Complexity and coupling metrics are typically **review signals**, not automatic correctness proof or hard gates.

## 7. Implementation work packages

Work items below are ordered for incremental adoption. They specify **outcomes and acceptance conditions**, not concrete code edits or prompt wording. Keep changes compatible with skills currently being refined.

### W0 — Establish baseline and compatibility boundaries

**Why:** Avoid changing several skill contracts blindly and duplicating capabilities that already exist.

**Work:** Confirm current skill responsibilities, authoritative artifact paths, installed development-profile/distribution rules, and any in-progress incompatible refinements. Capture two representative workflows for later comparison: (a) greenfield multi-task vertical development; (b) a small extension to an existing implemented system. Identify existing plan, task-map and contract-registry references that the change can reuse.

**Done when:** A concise ownership/delta map identifies what is reused, what must change, and what new capability cannot fit cleanly in existing skills. No broad refactoring or application-code changes.

### W1 — Define minimum shared contracts and the strategy skill

**Why:** Provide a stable project-level evidence-allocation artifact before modifying downstream consumers.

**Work:** Define the lightweight current-system context logical schema, provenance rules, fallback to existing artifacts and bounded-discovery policy. Define `SV-*` obligation semantics, source links, gap/disposition vocabulary and concise strategy template. Implement the `system-verification-strategy` skill as a consumer of `testing-discipline` and existing plan/system authority; clarify when a standalone strategy is justified versus inline guidance.

**Done when:** An agent can produce a proportionate, non-case-heavy strategy for a greenfield project or extension, identify real verification boundaries and owners, and visibly report unknown/untestable evidence without a full repository scan. It cannot invent new product requirements or duplicate the implemented contract registry.

### W2 — Integrate with delivery planning and independent plan review

**Why:** Testing decisions must affect task structure **before** implementation, and missing system coverage must be detected independently.

**Work:** Add draft-plan -> strategy -> targeted reconciliation guidance to `project-delivery-plan` and recommended workflow docs. Extend `project-plan-verification` to inspect strategy alignment, ownership, runnable points, prerequisite evidence and blocking gaps; preserve the existing independence requirement. Make the `task-map` refer to verification owners/obligations with the smallest compatible extension, avoiding duplication of the full strategy in JSON.

**Done when:** A plan cannot receive an unqualified independent acceptance with an unowned critical E2E obligation, no credible oracle for a critical boundary, or a silent conflict between implementation and verification plans. Low-risk small projects still use the light route.

### W3 — Make task boundary integration explicit

**Why:** Local acceptance must not mask regressions against previously implemented behavior.

**Work:** Ensure `task-brief-designer` and `task-verification-designer` consume **relevant** strategy obligations and implemented-system context by reference; do not copy the master plan into every task. Add targeted pre-change baseline and post-change integration decisions/evidence to `bounded-task-implementer`, `task-preflight` where relevant, and independent `task-acceptance-review`. Preserve existing separation of implementer/reviewer and ownership of the broad aggregate gate.

**Done when:** For a task touching an established API/database/UI boundary, the workflow identifies what previously worked, selects a proportionate real-boundary regression check, reports results and cleanly distinguishes verified task behavior from deferred sibling-task composition. For a mechanical task it explains why no additional integration run is warranted.

### W4 — Add composed-flow milestones and final system closure

**Why:** Individual accepted tasks do not automatically establish system completeness.

**Work:** Define how a milestone becomes integration-verifiable, when its owner must run the composed journey, and how pending `SV-*` obligations carry forward. Add a lightweight independent final review capability and concise final evidence/gap report. Keep detection/review and test implementation/correction as separate roles; allow bounded correction loops and fresh re-review. Specify blocking vs explicitly accepted residual-risk outcomes.

**Done when:** A multi-task example cannot be marked `VERIFIED` while an important composed flow lacks real execution evidence. Missing tests are surfaced as bounded corrective work. The report says what was planned, what ran, what passed/failed, and what remains unproven or manual.

### W5 — Validate, distribute and refine the workflow

**Why:** The design should prove additional defect detection and automation feasibility without excessive ceremony.

**Work:** Evaluate representative cases and deliberate failure fixtures (below). Update source skill guidance, `skills/README.md`, top-level workflow references, installer/development-profile lists and relevant installation tests **only as required** for new skills or dependencies. Add small structural validators only if they eliminate concrete reference/ownership errors; never claim semantic completeness from schema validation. Preserve compatibility with existing repositories and task packets.

**Done when:** The workflow works from a fresh context, old lightweight usage still works, new skills ship through the repository's canonical installation path, and evaluations demonstrate useful new detection at tolerable planning/execution cost.

## 8. Evaluation scenarios and expected failure handling

| Scenario | What the workflow should demonstrate |
| --- | --- |
| Fresh greenfield project with 3–5 vertical tasks | A small strategy allocates unit/API/integration/UI E2E proof, assigns cross-task ownership and identifies when the first complete journey can run. |
| Subsequent feature added to that project | Existing context/contract artifacts are reused; only affected flow/boundaries receive deeper inspection; baseline and post-change integration evidence are recorded. |
| Small localized/mechanical task | No standalone strategy rewrite or full integration suite; proportionate task-local evidence suffices. |
| System flow whose pieces all pass task tests but do not compose | Planning or milestone/final review detects the unverified journey and assigns a real integration obligation. |
| Required test depends on unavailable environment/provider | Planning records a prerequisite or explicit gap; execution cannot silently report success; final report preserves the limitation. |
| Existing integration suite already failing before change | Failure is baselined and not misattributed; new regressions can be distinguished from pre-existing defects. |
| Property tests with weak/circular oracle | Strategy/test review identifies insufficient semantic evidence and requires examples or an independent model where material. |
| Stale current-system context | Agent follows more authoritative executable/current information, marks stale index entries, and updates only affected references. |
| First slice with no runnable integrated product yet | Task can pass bounded acceptance; composed-system obligation remains assigned and pending until runnable. |

Measure a few simple outcomes against the prior process: **material verification gaps caught before code**, unowned system obligations, missing/failed integration caught after tasks, independently runnable final journeys, and additional planning/maintenance overhead. Do not use test counts or line coverage as the primary measure.

## 9. Explicitly postponed work

Do **not** include the following in initial delivery unless a pilot demonstrates a compelling dependency:

- Full brownfield archaeology or an automatic comprehensive pre-planning survey.
- A heavyweight current-state graph database, detailed mandatory JSON schema for every artifact, or a second authoritative contract registry.
- Automatic generation of large E2E suites, arbitrary test impact analysis, new distributed test orchestration, mandatory live provider testing or universal environment provisioning.
- Generic static complexity thresholds as hard architecture gates; enforced TDD proof for every file.
- Universal property-based tests, mutation testing everywhere, exhaustive browser permutations or extensive scenario cataloguing at master-plan time.
- Fully automated interpretation of subjective user experience or external acceptance as if it were deterministic proof.

The current-system context contract and obligation IDs should **leave an extension path** for these later capabilities without prematurely depending on them.

## 10. End-to-end definition of done for this change

The improvement is ready for ordinary use when a fresh agent can:

1. Begin with existing artifacts and at most a shallow context orientation, not a full investigation.
2. Draft a multi-task delivery plan, create a compact verification strategy and reconcile genuine testability/task-ownership conflicts.
3. Obtain independent verification of the complete planning package, including explicit planning-stage gaps.
4. Derive one implementation-ready task and task verification guidance without duplicating whole-system plans.
5. Establish a relevant pre-task baseline and produce targeted post-task integration evidence, or explicitly justify why a run was not possible/necessary.
6. Preserve cross-task verification obligations until their associated boundaries become runnable.
7. Run an independent final system review, assign bounded corrections for missing tests/behavior and produce a truthful final evidence/gap report.
8. Preserve the low-ceremony route for small work and the existing skill ownership boundaries.

**Recommended first delivery slice:** W0–W2. They establish the strategy and planning feedback loop. Then deliver W3 (task-boundary regression), W4 (system closure) and W5 (evaluation/distribution), validating each stage on a small greenfield/extension example before expanding toward larger brownfield projects.
