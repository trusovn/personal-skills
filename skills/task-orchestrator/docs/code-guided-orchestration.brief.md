# Idea Brief: Code-Guided Task Orchestration

## Status

- Source: user request and six clarification answers; examination of the current `skills/task-orchestrator` and `skills/task-implementation-flow` source trees.
- Output: `skills/task-orchestrator/docs/code-guided-orchestration.brief.md`.
- Depth: standard.
- Created: 2026-10-08.
- Examined repository commit: `b5564477d81bba384c9cddb35cfd78fc91548f64`; working tree was clean before this brief.
- Downstream target: focused architecture/integration spike, then direction and delivery planning.
- Authority: discovery brief for a proposed direction. It does not replace current plans, contracts, or operating instructions.
- Evidence limit: local source and document examination. No behavioral tests, live agent runs, or external research were performed for this brief.

## Raw Idea

> $idea-brief examine current skills/task-orchestrator skill. The original intent was to have it AI-guided. But I want it to be code-guided instead. I'd also  want it to be integrated (heavily using) with skills form skills/task-implementation-flow in their current state (with the ability to easily upgrade the flow according to the update of the flow here).

The user clarified:

1. Write the brief at the proposed output path above.
2. Code owns stage order, gates, retries, recovery, and advancement. AI performs each skill stage.
3. Upgrade explicitly to a tested flow version. Active runs retain their original version.
4. The first useful version starts from existing approved task packages/index and automates execution through acceptance.
5. The primary improvement is reliable completion and resume with the prescribed stages, without an AI coordinator.
6. Use the current skills directly. Preserve their conditional stages, artifacts, and correction routes.

## One-Paragraph Vision

Make `task-orchestrator` a code-operated executor of the current task implementation flow. Once the operator supplies approved task packages and run authority, code selects the eligible task, launches bounded skill actors, checks their results and repository effects, routes corrections, and advances only when the required evidence is present. AI retains the judgment needed to implement and review a task, but does not choose the workflow or grant authority. The flow remains maintained with `task-implementation-flow`; explicit tested upgrades bring its changes into new runs while existing runs retain their original flow version.

## Problem And Context

- **Problem:** The operator wants prescribed task execution and recovery to depend on code rather than an AI coordinator remembering stage rules. Whether existing runs have suffered particular failures was not established in this interview.
- **Trigger:** A set of approved tasks is ready to execute, potentially across interruptions and several review/correction cycles.
- **Current alternative:** An operator or AI session coordinates separate implementation skills. The experimental orchestrator provides a mechanical foundation but cannot yet execute the complete flow.
- **Why now:** The reusable implementation flow has evolved beyond the orchestrator's current stage model. Completing that older model alone would not satisfy direct integration with today's skills.

### Current-State Findings

These findings describe examined source, not freshly demonstrated runtime behavior.

| Finding | Local evidence | Implication |
| --- | --- | --- |
| The orchestrator already has deterministic task selection, run authority, Git observations, verification execution, and flow state. | `scripts/controller.py`, `scripts/controller_state.py`, `scripts/controller_git.py`, and `scripts/verification_runner.py` under `skills/task-orchestrator`. | The proposed direction can build on existing code. It is not a change from an entirely prompt-operated system. |
| The parser exposes `init`, `run-next`, `inspect`, and `revise-flow`. Flow revisions and stage cursors have been implemented. | `controller.py:build_parser`, `revise_flow`, and `docs/stage-3-mvp-tasks/MVP-2-result.md`. | The skill entry point and architecture/index references, dated 2026-07-23, lag this source. The result document reports `READY_FOR_REVIEW`; it is not evidence of completed independent acceptance. |
| The public launch path handles implementation and reports other unowned stages as pending. End-to-end recovery, semantic actors, correction, acceptance/release, and unattended advance remain missing. | `controller.py:_cli_run_next`, the CLI parser, and the MVP-2 result. | Persisted flow contracts are groundwork, not a working unattended executor. |
| The closed flow order is `preflight -> implement -> verify -> semantic_review -> accept`; it freezes actor mappings and a 50% implementation-session reuse threshold. | `controller_state.py:FLOW_STEP_ORDER`, `ACTOR_LEVELS`, and `validate_flow_profile`. | This representation does not express the current separated maintainability, registry-update, and functional-review routes. |
| The implementation prompt names the brief, scope, checks, and dependencies without an explicit binding to the implementation-flow skills. | `controller.py:render_worker_prompt` and `_cli_run_next`. | Direct skill use is not established by the current prompt construction. Incidental skill selection in a worker is insufficient as an integration contract. |
| The current flow has seven skills, executable-leaf decomposition, task packages, optional verification design, and conditional review/registry stages. Explicit orchestrated flows require standalone preflight. | `skills/task-implementation-flow/README.md`, the seven `SKILL.md` files, and the brief designer's artifact-layout reference. | Integration must preserve both required stages and justified omissions. “Heavily using” does not mean invoking every skill on every task. |
| The minimal orchestrator manifest points to `tasks/T1.md`; current flow skills reject direct legacy durable briefs and require `<task-package>/brief.md`. | `assets/examples/minimal-task-manifest.json` and current preflight/implementer instructions. | Existing examples cannot be treated as flow-compatible launch inputs without normalization. |
| Workflow fingerprinting and a rerunnable development-profile installer already exist. The development profile installs all seven flow skills and selected shared helpers; the orchestrator is a separate install. | `scripts/workflow_version.py`, `scripts/install_development_skills.py`, and root `README.md`. | Reuse existing identity/distribution conventions. They do not yet provide a tested compatibility contract or a retained, runnable flow version for old runs. |

## Users And Stakeholders

| Group | Goal | Friction Today | Notes |
| --- | --- | --- | --- |
| Repository operator | Start, inspect, interrupt, and resume approved work with predictable results. | The complete task flow still needs external coordination. | Primary user implied by the request. |
| Flow maintainer | Improve the seven skills once and make compatible updates easy to adopt. | Orchestrator-specific copies of flow rules could diverge. | Current source repository remains the flow's maintenance source. |
| Implementation and review actors | Receive one bounded role, valid inputs, and a clear handoff. | Generic stage models can omit current role boundaries and evidence rules. | AI judgment remains necessary within stages. |
| Repository owner | Preserve user work, required gates, and planning authority. | Automatic runs must distinguish expected artifacts from unauthorized changes. | Repository and user authority constrain every actor. |

## Desired Outcomes

- **Primary outcome:** Reliable task completion and resume under code-owned orchestration, without an AI coordinator.
- **Secondary outcomes:** Direct reuse of current skill behavior; clear reasons for stopping; compatible upgrades without changing active runs; less repeated coordination.
- **Success signals:** Ordinary stage progression requires no conversational choice of the next stage; interruptions preserve task/actor/evidence identity; correction follows the right owner; required review applies to current bytes; new runs can adopt a tested flow update while earlier runs remain reproducible.
- **Non-goals:** Replacing AI implementation or semantic review with deterministic algorithms; executing composite parents; treating a passing command as functional acceptance; duplicating the skills into a separate process; making all seven stages mandatory for all tasks.

## Scope Sketch

### First Useful Version

- Begin with approved task packages and their structural index, plus explicit run authority. Validate their compatibility with the selected flow before launch.
- Execute eligible leaf tasks through current preflight, bounded implementation, applicable gates, applicable semantic reviews and registry synchronization, correction, controller acceptance, and dependency advancement.
- Invoke the actual selected skill packages and their relevant references. Actors own their bounded work; code owns transitions, permissions, evidence validation, and process lifecycle.
- Preserve the distinction between a submitted implementation, mechanical eligibility, semantic verdicts, and controller task acceptance.
- Resume interrupted work safely and stop at unresolved authority, ambiguous process ownership, inconclusive review, or exhausted authorized loops.
- Allow explicit adoption of a tested flow version for new runs. Keep existing runs bound to the version they started with.

### Explicitly Out Of Scope

- Automatic conversion of high-level plans into briefs, estimates, and decomposed task packages in the first useful version. `task-brief-designer` remains the preparation/normalization owner when needed.
- Automatically importing the latest flow into an active run.
- An AI supervisor deciding ordinary progression, silently repairing authority, or broadening permissions.
- A general workflow platform or arbitrary no-code support for unknown future actor kinds.

### Boundary Notes

- “Use the skills directly” means their current instructions, artifacts, independence rules, and correction semantics remain operative. Code still needs explicit structured outcomes and validated transitions; it cannot execute prose as a state machine.
- Separate verification design remains conditional and task-local. Existing applicable `verification.md` artifacts must be carried through preflight and implementation.
- High-assurance orchestrated execution currently requires standalone preflight. It cannot inherit the guided profile's optional self-preflight shortcut without a deliberate flow-contract change.
- Architecture gates and maintainability review follow repository authority. Registry synchronization applies when implemented-contract discovery and actual contract/reference impact require it. Profiles cannot bypass mandatory repository rules.
- Keep `docs/task-map.json` planning authority, `docs/tasks/index.json` structural discovery, and the runtime ledger distinct. Runtime advancement does not rewrite plans or the structural index.
- The prior local/sequential trust model and side-effect-free acceptance are sensible starting assumptions, recorded below rather than new confirmed product requirements.

### Current Skill Integration Surface

| Skill or operation | Intended relationship to the executor |
| --- | --- |
| `task-brief-designer` | Prepare, size, decompose, or normalize tasks before entry. Launch executable leaves; return authority/design defects to the proper owner. |
| `task-verification-designer` | Optional preparation when recommended or required. Its output is derived guidance under the brief, not new requirements authority. |
| `task-preflight` | Establish readiness and a fresh canonical packet for orchestrated execution. Stale inputs return here. |
| `bounded-task-implementer` | Implement or correct bounded work; submit a machine-contracted result and handoff. Submission does not accept the task or launch reviewers. |
| Deterministic checks | Code executes authorized commands and enforces applicable architecture/verification gates. Passing checks do not supply semantic verdicts. |
| `task-maintainability-review` | Fresh independent design review when required; precedes functional acceptance. Production corrections invalidate its verdict. |
| `task-contract-registry-updater` | Synchronize eligible registry/reference changes after structural/maintainability approval and before functional acceptance. It cannot repair executable contracts or redefine planned semantics. |
| `task-acceptance-review` | Fresh independent functional review. Implementation defects return through implementation and applicable gates/reviews; reference-only defects return through registry update and fresh acceptance. |
| Controller acceptance and advance | Validate the selected flow's current evidence, accept the leaf, release dependencies, and select the next eligible task. These are code operations, not AI skill verdicts. |

## Scenario Map

| Scenario Type | Scenario | Why It Matters |
| --- | --- | --- |
| Happy path | Approved leaf tasks complete all applicable stages, and acceptance of one releases its dependent leaf. | Proves the intended complete workflow rather than isolated actor launches. |
| Conditional path | A task has obvious verification, no required maintainability review, and no contract delta. | Skipped stages need a valid reason; unnecessary stages consume time and tokens. |
| Preparation boundary | An approved index contains a decomposed parent or a legacy direct brief. | The executor must select valid leaves or return for normalization, not launch an invalid task. |
| Implementation correction | Functional findings require production changes after maintainability acceptance. | Current bytes need new gate evidence and fresh applicable reviews before acceptance. |
| Reference correction | Functional review finds only stale registry/routing references; production, test, and executable-contract bytes are unchanged. | The narrow route is updater then fresh acceptance, without unnecessary implementation/maintainability work. |
| Operational interruption | A process dies, times out, or has uncertain liveness before a result is recorded. | Recovery must not launch a second writer or promote partial work into acceptance. |
| Artifact lifecycle | Preflight or review writes its authorized canonical artifact, changing Git status. | The expected artifact delta must not look like unauthorized drift or invalidate its own freshness evidence. |
| Failure path | A required command, helper, environment, or decisive review oracle is unavailable. | A blocked/inconclusive result must remain visible; retries cannot manufacture evidence. |
| Misuse or bad input | An actor supplies `ACCEPT` for the wrong task, obsolete bytes, wrong role, or requested authority expansion. | Structured output is a claim; code must validate identity, provenance, and allowed consequences. |
| Upgrade | The operator updates installed skills while a run is interrupted. | A recorded fingerprint alone cannot restore old executable skill bytes or shared dependencies. |
| Contract change | A flow update adds a stage, changes an outcome, or changes correction ownership. | Updating instructions alone may leave routing incompatible and needs an explicit tested upgrade. |
| Human decision | A reviewer identifies a planned/current semantic mismatch or a scope/permission question. | Escalate to the decision owner; ordinary correction cannot silently redesign the task. |

## Critical Assumptions

| Assumption | Why It Matters | How To Validate | If False |
| --- | --- | --- | --- |
| A trusted local, sequential executor in one working tree remains sufficient. | Existing controller safety boundaries fit this model. | Confirm during direction planning. | Concurrency/distributed operation needs separate ownership and isolation work. |
| Existing controller, transport, Git, and verification code is worth retaining. | The request calls for completing and integrating the flow, not an unqualified rewrite. | Focused code assessment and cheap existing tests during the spike. | Replace only components whose limitations are demonstrated. |
| Current skill outputs and artifacts can be adapted into small explicit machine contracts without changing their substantive behavior. | Direct reuse depends on deterministic handling of AI-produced claims. | Exercise representative preflight, review, and updater outcomes. | Update the flow-owned contracts with the skills before automation can be reliable. |
| Flow maintainers can keep executable integration rules synchronized with skill instructions. | Prose alone does not provide a code-readable transition authority. | Identify one maintenance owner and check a representative flow update. | The executor will duplicate policy and upgrades will require recurring manual reconciliation. |
| Side-effect-free acceptance, with commits and external trackers deferred, is a suitable initial boundary. | This matches the current MVP direction and limits unrelated lifecycle complexity. | Confirm before delivery planning. | Finalization side effects need their own authorized scope and recovery design. |
| Approved packages provide adequate initial task authority. | Plan preparation was explicitly excluded from the first useful version. | Check current readiness statuses, decomposition, scope, and dependency representation. | Stop for normalization/preparation; do not infer missing authority. |

## Risk Register

| Risk | Likely Consequence | Early Signal | Mitigation Or Next Check |
| --- | --- | --- | --- |
| Skill prose and code routing become separate sources of flow policy. | Updates appear successful while stages or corrections follow obsolete semantics; later rework spans both packages. | One rule is copied into several actor prompts and controller branches. | Establish a small explicit integration contract maintained with the flow; determine its ownership in the spike. |
| “Easy upgrade” is interpreted as arbitrary instruction changes requiring no adapter changes. | New outcome/stage/permission behavior breaks runs or silently weakens gates. | An upgrade has no declared compatibility check. | Distinguish content changes from structural contract changes and reject unsupported versions. |
| Pinning records only a digest, not retrievable bytes and dependencies. | An interrupted run cannot reproduce its original actors after installation refresh. | Resume reads the latest installed skill despite an older recorded identity. | Resolve retained-version availability and dependency coverage before implementation. |
| A generic semantic stage replaces distinct roles. | Maintainability, functional acceptance, or registry ownership is skipped or conflated. | A single actor both edits and independently accepts the same work. | Preserve fresh-session provenance and separate verdict/effect contracts. |
| Expected artifacts conflict with existing repository-drift checks. | Valid preflight/review work stops repeatedly, or drift checks are weakened too broadly. | Writing `preflight.md` or a numbered report invalidates the next stage. | Exercise exact authorized artifact deltas and unchanged non-artifact bytes. |
| Correction routing depends on unvalidated AI labels. | Production changes retain stale verdicts, or reference-only issues trigger full unnecessary loops. | “Docs only” is accepted without checking changed bytes and executable declarations. | Corroborate effect classification and route ambiguity to the proper owner. |
| Record integrity work grows before end-to-end usefulness is proved. | More contracts accumulate while the operator still performs manual coordination. | Another schema milestone without a complete task/correction/recovery path. | Prioritize a small public-path integration proof with disposable state and controlled actors. |

### Challenge Pass

- **Strongest upside:** Code removes ordinary workflow coordination from AI attention while retaining the current specialized implementation and review discipline.
- **Most likely failure path:** Hard-code today's flow separately from the skills, then discover that each skill update needs scattered controller/prompt edits.
- **Assumption most likely to be false:** Every skill update is compatible merely because the skill name or output wording still looks familiar. Artifact ownership and routes can change without obvious naming changes.
- **Scenario most likely to be missed:** A suspended run resumes after installation refresh, or an authorized report write changes the freshness baseline expected by the next stage.
- **Decision most likely to become expensive:** Ownership of the executable flow contract and the boundary between versioned skill behavior and durable run state.
- **Assessment:** Continue. The mechanical foundation already supports the direction. The next uncertainty is integration and lifecycle compatibility, not whether ordinary stage transitions need an AI supervisor.

## Architecture-Affecting Unknowns

These are questions for later work, not selected architecture.

- **Source of truth:** Where will machine-readable stage conditions, result mappings, correction routes, and compatibility rules live so flow updates do not require duplicated policy?
- **Identity, roles, and permissions:** How will a run prove reviewer independence and enforce stage-specific writes, including canonical reports and narrow registry updates?
- **Data lifecycle, retention, import, and export:** Which skill packages, references, shared helpers, and controller compatibility information must remain available to resume a pinned run? When can retained versions be removed?
- **Integrations:** How can version retention honor project-local skill precedence and same-installation-root helper resolution? Fingerprinting currently covers a selected skill package, not an aggregate compatibility guarantee for the whole flow and shared runtime.
- **Human review and accountability:** How are semantic/authority ambiguities presented to the operator, and what operator input can resume a stopped run without silently changing its authority?
- **Collaboration and handoff:** How are prior findings, finite review rows, current byte identity, and implementation-session reuse decisions carried through corrections without transcript duplication?
- **Scale, cost, latency, and availability:** What bounds apply to correction and transport retries, context reuse, and retained versions? The primary priority is reliability; exact budgets remain undecided.
- **Privacy and safety:** Does the existing trusted-local/sandbox model remain the governing boundary? No additional remote or multi-user requirements were established.

## Open Questions

| Question | Why It Matters | Blocks Or Influences | Owner | Due |
| --- | --- | --- | --- | --- |
| Where is the executable flow/compatibility contract maintained, and who updates it with the skills? | Prevents competing policy sources. | Integration design and upgrade maintenance. | Flow/orchestrator maintainer | Integration spike |
| Which stage results need adapters, and which can use supplied schemas without changing current skill behavior? | Current preflight, updater, and reviewer contracts are not one uniform machine interface. | Direct actor integration. | Spike owner | Integration spike |
| How are original skill bytes and shared dependencies retained for active runs after an install update? | A fingerprint identifies content but does not preserve it. | Upgrade and resume design. | Orchestrator maintainer | Integration spike |
| Which existing controller components can accommodate stage artifacts and narrowed actor write sets? | Current drift/scope logic must remain strict while allowing legitimate flow outputs. | Reuse versus bounded replacement. | Spike owner | Integration spike |
| How are required stage predicates and ambiguous correction effects made deterministic? | Profiles must preserve repository requirements and invalidate the right evidence. | Routing and policy validation. | Flow maintainer | Before delivery planning |
| What exact approval/readiness state is accepted from existing task packages/index? | Guided `ready` and high-assurance `ready_for_preflight` have different entry requirements. | Launch boundary and normalization. | Flow/orchestrator maintainer | Before delivery planning |
| Are local sequential execution and deferred commits/trackers accepted initial boundaries? | These are inherited planning assumptions, not new interview decisions. | Product direction and task scope. | User | Direction planning |
| What operator interface and stopping/retry budgets are sufficient? | Reliable unattended work still needs explicit limits and a practical recovery surface. | UX, lifecycle, and operational cost. | User and planner | Delivery planning |

## Planning Handoff

- **Recommended next step:** A focused architecture/integration spike using the current skill packages and existing controller boundaries.
- **Rationale:** The code/AI ownership boundary is settled. The material unknown is how to integrate current artifacts, conditional stages, outcomes, and pinned upgrades without maintaining a second copy of flow policy.
- **Spike focus:** Compare the existing flow model with today's seven skills; demonstrate one complete leaf-task path, an implementation correction, a reference-only correction, an interruption, and an install update while an old run remains resumable. Start with local disposable fixtures and controlled actors; any live or expensive checks need separate authorization.
- **After the spike:** Establish the revised governing direction, then prepare and independently verify a bounded delivery plan. Keep new results beside existing plans rather than rewriting them during this brief task.
- **Suggested project or feature slug:** `code-guided-task-orchestration`.

### Seed For Next Planning Step

Build a code-guided executor for approved executable task packages that completes the current `task-implementation-flow` through applicable checks, independent review, correction, acceptance, and dependency advancement. Code owns workflow order, gates, retries, recovery, and authority; AI performs bounded work by directly using the current skills. Preserve conditional stages, canonical task artifacts, fresh reviewer provenance, and distinct implementation versus reference-only correction routes. Prioritize reliable completion and resume without an AI coordinator, and support explicit tested flow upgrades while active runs retain their original version. Resolve executable-flow ownership, structured actor compatibility, authorized artifact effects, and retained-version availability before choosing a detailed implementation design.
