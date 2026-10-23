# Run one prepared task inside sbx

Status: READY_FOR_PLAN_VERIFICATION

Date: 2026-10-23

Revision: single-task sbx delivery; supersedes the 2026-10-22 delivery scope

Companion: [machine-readable task map](local-harness-task-map.json)

## Intended result

The owner supplies a human-reviewed task brief and verification document, then starts a coordinator inside an existing Docker sbx machine. The system checks readiness, implements the task, collects independent evidence, obtains a separate AI acceptance decision, and corrects ordinary failures. It returns accepted local work or a precise blocker with preserved work and evidence.

The first useful proof is one prepared task inside sbx with a failed check or review finding, a real correction, repeated checks, fresh independent collection and separate acceptance. Completion does not require an automatic commit or another task. The [implementation task map](#implementation-task-map) shows how the remaining work produces this loop.

## Planning authority

The [owner-confirmed single-task direction](direction-single-task-sbx.md) governs this revision. It supersedes conflicting scope, runtime and completion requirements in the [original direction](direction-local-harness.md). The [correction and disposition notes](correction-and-disposition-options.md) distinguish approved policy from recommendations; JSON tracking and an additional repetition-stop rule remain proposals.

T-001 selected the Python-to-Codex CLI transport and recorded its limitations in [ART-008](tasks/T-001/harness-contract.md), [the follow-up](tasks/T-001/capability-follow-up.md), [discovery-03](tasks/T-001/reviews/discovery-03.md) and [acceptance-02](tasks/T-001/reviews/acceptance-02.md). Preserve those historical reports. F-01 is not fixed; its tool-exclusion requirement and the old outer-permission/inherited-tool/hook qualification gates no longer govern this delivery. The prior recovery proposal and path-to-T-002 guide are historical options, not current entry instructions.

The [previous plan review](project-plan-review.md) applies to its recorded old bytes and direction. This revision requires fresh independent plan verification. It does not declare T-002 ready or prove runtime execution.

Use the [architecture map](../references/architecture-map.md), current code and existing focused tests to establish reusable behavior. No production code, runtime configuration or active installation is changed by this plan.

## Scope

In scope: one repository, one prepared task at a time, human-reviewed inputs, actual-environment preflight, implementation, deterministic checks, independent evidence collection, separate AI acceptance, bounded correction, current-candidate evidence, small persisted status and chat intervention when blocked. Preflight, collection and acceptance are required stages of this delivery; an optional profile cannot omit them.

The owner starts work inside an existing sbx machine on a separate branch. Actors run in YOLO mode. These are operating assumptions, not verified containment or branch-protection guarantees. Role separation controls assignments and evidence admission; this delivery does not promise filesystem or tool isolation between actors. Agents must follow their assigned scope and use controller operations for state changes.

Deferred: sbx provisioning and startup automation, broader containment/tool exclusion, parallel work and parallel-writer coordination, automatic commits, multi-task dependency release, branch/PR/main handling, remote publication, a background daemon, automatic crash recovery, multi-provider support, automatic skill installation and a general workflow language. An active coordinator is required. Unknown previous-operation liveness must still stop a retry.

Priority: truthful evidence and task authority first; a small usable loop second; minimum runtime machinery third.

## Current baseline and reuse

Current public commands are `init`, `run-next`, `inspect` and `revise-flow`. The reviewed single-task loop is not implemented.

| Existing component | Intended treatment |
|---|---|
| `scripts/controller_state.py` | Reuse flow/cursor validation and persisted transitions; add only the stage, operation and evidence state this loop requires. |
| `scripts/controller_git.py` | Reuse scope, baseline and content identity; no commit/dependency implementation is required. |
| `scripts/verification_runner.py` | Reuse real check execution and records; retain generated-file treatment. |
| `scripts/controller.py` | Keep one public authority boundary for status, reservation, evidence admission and completion. |
| `scripts/codex_worker.py` | Reuse the selected subprocess transport. T-003 must adapt its current full-access refusal to the explicit sbx/YOLO run policy. |
| Schemas, profiles, examples and focused tests | Evolve with runtime validation; preserve distinct existing scenarios and avoid a second ledger. |

Current model constants and profile schema still select `gpt-5.6-sol`. T-002 owns representing/freezing the approved `gpt-6.1-sol` low/medium/high mapping and fresh-session fallback; T-003 applies the policy at launch. Preserve already frozen runs. Refuse incompatible old-run continuation with a clear next action instead of silently migrating it.

## Actors and capabilities

| Owner | Responsibility |
|---|---|
| Owner | Supplies human-reviewed brief/check requirements and execution authority; resolves missing decisions or permissions. |
| Coordinator | Follows permitted actions, routes ordinary recovery, records approved deferrals and presents blockers in the active chat. Cannot waive required evidence. |
| Controller | Owns assignments, persisted state, operation reservations, input/candidate identity, check records, correction count, evidence admission and the completion transition. |
| Harness adapter | Launches the authorized role through Codex CLI inside sbx; observes session/operation identity, records output and terminality, and supports conservative interruption handling. |
| Preflight actor | Checks actual sbx readiness under the approved inputs: tools, dependencies and required installed skills. Submits readiness evidence or a precise blocker; does not implement the task or supply acceptance. |
| Implementation actor | Implements or corrects within task authority and submits work/evidence. Cannot accept its own work. |
| Independent collector | Starts fresh, reruns relevant deterministic checks and inspects requirements, behavior and code quality. Publishes evidence/findings without final acceptance. Does not correct the candidate. |
| Separate acceptance reviewer | Starts fresh, consumes collected evidence and task authority, and decides accept, correction, missing evidence or blocker. Does not implement or take over collection. |

The controller enforces transitions from validated records; tests establish facts and reviewers supply semantic judgments. Structured records bind each result to its role, operation, task inputs and candidate. Actor prose alone cannot complete a task. Unknown context occupancy requires a fresh correction session. Reuse is allowed only under the existing reliable-occupancy rule, not terminal token-usage totals.

## Artifact and state catalog

IDs are retained for traceability. This revision deliberately narrows ART-007/IF-004/INV-006 from commit/dependency finalization to single-task completion, and separates ART-006 collection from the new ART-009 acceptance decision. These are planned changes, not new claims about implemented contracts or the historical T-001 reports.

| ID | Artifact | Producer / mutation owner | Consumers and lifecycle |
|---|---|---|---|
| ART-001 | Approved task inputs and run policy | Owner supplies brief, verification requirements and authority; controller freezes their identity | All actors receive applicable projections. Includes scope, model/effort mapping, sbx/YOLO policy and correction limit. T-002 owns authorized revisions at a safe boundary: update input/policy identity and state version atomically, invalidate readiness and affected evidence, and retain history and the correction count. Refuse unauthorized or unsafe revisions. |
| ART-002 | Task status and operation records | Controller | Coordinator and adapter. Persist run/task and input/flow identity, stage, state version, attempt/correction count, evidence locations, candidate, outstanding findings, required evidence, active operation, next action and blocker. Atomic reservations; history retained. Readiness references the admitted terminal preflight ART-004 and current ART-001 identity. |
| ART-003 | Candidate and scope identity | Controller inspection | Checks, collector, acceptance and final gate. Covers relevant tracked/untracked bytes, baseline, configuration and task-input identity. Relevant changes supersede evidence. |
| ART-004 | Assignment and actor outcome | Controller assigns; adapter captures outcome and observed provenance | Controller and actors. Bind role/task/operation/input/candidate identities. Rejected or malformed output remains diagnostic history, not completion authority. |
| ART-005 | Check evidence | Controller verification runner | Collector, acceptance and final gate. Command, setup/environment, exit result and evaluated candidate. Collector reruns use the same runner; previous results remain historical. |
| ART-006 | Independent collection report and findings | Collector via adapter; controller admits | Acceptance, coordinator and correction actor. Evidence coverage and stable finding IDs/dispositions; no final acceptance verdict. Relevant changes invalidate current coverage. |
| ART-007 | Completion and intervention records | Controller | Coordinator and later status inspection. Records gate outcome or unresolved blocker and chat relay/owner-response history. No automatic commit or dependency release. |
| ART-008 | Selected runtime contract and limitations | Historical T-001 investigation; T-003 publishes a successor supplement | Adapter implementer, preflight and operator guide. Keep old evidence limits; qualify actual sbx launch/collection behavior in its owning tasks. |
| ART-009 | Separate acceptance decision | Acceptance reviewer via adapter; controller admits | Coordinator and final gate. References current inputs/candidate, ART-005/006 and required role evidence; chooses accept/correction/missing evidence/blocker with rationale and dispositions. |
| ART-010 | Approved known-issue records, when needed | Coordinator records acceptance-approved deferrals | Acceptance, gate and later reviewers. Use the repository-declared tracker, or the active skill default. Stable IDs and provenance; idempotent recording, retained history. No tracker is required before a deferral exists. |

Keep durable evidence and controller state distinct from task edits. Use a stable controller/skill snapshot when the task changes orchestrator source; do not refresh the active installation during a run. This is an operational discipline under YOLO, not an enforced inaccessible-files guarantee. ART-010 is an explicit coordinator-owned task-tree write when required. Declare its path in scope and validate its recording separately at the final gate. A tracker-only update that records the unchanged approved disposition does not supersede implementation evidence unless that tracker is itself an implementation or configured-check input. Any change to evaluated files or task inputs requires new evidence; other drift remains rejected.

## Lifecycle/state models

Task stages: ready -> preflight -> implementation -> checks -> collection -> acceptance -> completion gate -> completed. Failed required behavior or blocking findings may route to correction, followed by checks, fresh collection and separate acceptance. Missing evidence routes to collection/checks as appropriate; it is never a pass. A broken environment routes to bounded repair within authority or intervention. Ambiguous requirements requiring a decision stop for the owner.

Preflight is an adapter-launched role implemented by T-003. It reserves an operation through IF-001, runs through IF-002 and submits an observed terminal ART-004 through IF-003. The controller admits readiness into ART-002 only for the current ART-001 identity and a complete readiness result; missing tools/dependencies/skills produce a precise blocker and prevent implementation. A preflight launch or retry consumes no correction cycle. It does not satisfy or replace any of the implementation, collection or acceptance roles in INV-004. An authorized environment repair is followed by preflight again.

Operation states: reserved -> running -> terminal; uncertain launch or liveness -> unknown. No new actor or completion is permitted while an operation may still be live. Preserve records on interruption and stop for terminality to be established before retry. Automatic crash reconciliation is not required.

The initial implementation is cycle zero. Each authorized correction launch consumes exactly one of three shared task cycles, including corrections prompted by checks or review. Replay/restart cannot increment twice or reset the count; no fourth correction. Accept as soon as requirements pass. Exhaustion preserves partial work and evidence and requests intervention; it never grants acceptance.

Invalid API requests return reasons and permitted actions without changing authoritative state/version, policy, count or task files. Separate diagnostics may be appended. Valid operational failures update their evidence and may change the next action or persist a blocker.

T-002 owns ART-001 revision through IF-001. A safe boundary has no reserved, running or unknown operation and the task is not completed. Explicit owner authority is required for a material task/policy change. An admitted revision atomically changes ART-001 identity and ART-002 state version, clears readiness and invalidates affected candidate/check/collection/acceptance eligibility while retaining historical records and the correction count. Required preflight must pass again before implementation resumes. Unauthorized, stale-version or unsafe revisions leave authoritative state and files unchanged.

## System interface map

These are logical contracts; exact command/payload spelling belongs to the owning task and must be published for successors. T-001 supplies transport evidence, not an implemented reservation/acceptance API.

| ID | Boundary | Contract |
|---|---|---|
| IF-001 | Coordinator -> controller: status/reserve/revise-inputs | Consume ART-001/002/007, expose stage and permitted actions, and produce ART-004 assignments or revised ART-001/002 records. Reserve against expected version; enforce authority, one active operation and the shared correction limit. T-002 also owns authorized ART-001 revision at a safe boundary, state-version increment and readiness/affected-evidence invalidation without resetting corrections. Invalid requests preserve authoritative state. |
| IF-002 | Controller assignment -> adapter: launch/observe/collect/stop | Consume ART-002/004/008; apply frozen policy inside sbx; return observed identity and ART-004/006/009. Same operation key cannot launch twice. Unknown status blocks retry; preserve logs and terminality evidence. |
| IF-003 | Adapter/coordinator -> controller: inspect/check/admit | Consume ART-001/002/004; inspect ART-003, execute ART-005 and admit ART-006/009. Validate role, identity, current coverage and provenance. T-003 admits terminal preflight readiness into ART-002; T-004 owns ART-006 semantic admission and T-005 owns ART-009 semantic admission. Separate collection from acceptance; malformed/stale evidence cannot advance. |
| IF-004 | Coordinator -> controller: complete/stop/intervene | Consume ART-001..010 as applicable. Require a terminal operation, approved scope, current required checks and independent role evidence, separate acceptance, no unresolved blocker and recorded approved deferrals. Publish ART-007 completion once. Otherwise expose recovery or persist a blocker for active-chat relay; owner acknowledgement is not automatically authority to resolve it. T-003 owns stop/intervene and blocker persistence; T-005 owns the completion gate and publication. |

## Cross-task invariants

| ID | Required invariant | Decisive evidence |
|---|---|---|
| INV-001 | Actor results cannot change task authority or remove required stages. | Invalid requests preserve policy/state/version/files; weaker profiles cannot omit preflight, collection or acceptance. |
| INV-002 | One active operation; unknown liveness blocks retry and completion. | Duplicate reservation/collection and interrupted subprocess tests; unknown remains stopped. This is sequential control, not tool-exclusion assurance. |
| INV-003 | Checks, collection and acceptance cover the exact current task inputs and candidate. | Relevant tracked/untracked/config/input edit supersedes evidence and blocks completion. |
| INV-004 | Collection is fresh and independent of implementation; acceptance is a separate fresh session from both. | Wrong-role, same-session, invented-provenance and stale-report records rejected; three distinct valid observed roles admitted. |
| INV-005 | At most three correction launches; replay/restart cannot reset or double-count them. | Cycle zero plus three corrections allowed; fourth refused; failure at exhaustion requests intervention. |
| INV-006 | Only current required evidence plus separate acceptance permits single-task completion. | Missing/failed/stale/inconclusive evidence or an unrecorded approved deferral blocks completion; no commit/dependency prerequisite. |
| INV-007 | Interruption preserves work, evidence, count and a precise next action. | Status after coordinator replacement exposes known/unknown operation state and preserved history; uncertain terminality stops retries. |
| INV-008 | Passed, failed, stale, blocked, missing/not-run and policy omission remain distinct. | Required stages cannot be omitted; optional extra-stage omissions and limitations appear truthfully in status/report. |

## Capability-to-flow coverage

CAP-001 (one independently accepted task) uses FLOW-001 and ART-001..010 through IF-001..004. CAP-002 (safe interruption stop/handoff) uses FLOW-002 and ART-001/002/004/007/008. CAP-003 (truthful gates and intervention) uses FLOW-001/003. The companion map assigns task and invariant coverage.

## End-to-end data/process/state flows

### FLOW-001: one prepared task through correction and acceptance

1. Controller freezes the approved brief, verification document and execution policy in ART-001. T-003 implements the preflight role: reserve through IF-001, launch through IF-002 and admit its terminal ART-004 through IF-003. It checks actual sbx tools/dependencies and required installed skills. Controller readiness in ART-002 references that result and current ART-001; only a complete ready result permits implementation. A missing decision or unavailable capability returns a precise blocker. Preflight and its retries use the single-operation guard but consume no correction cycle; INV-004 still requires independent implementation, collection and acceptance roles.
2. Coordinator reserves implementation through IF-001. Adapter launches the authorized actor via IF-002 using ART-001/002/004/008. Controller admits the terminal ART-004 through IF-003 and independently captures scope/candidate ART-003. An implementation claim is not acceptance.
3. Controller executes the configured checks into ART-005. Each claimed result must include the setup and inputs needed to exercise it. Product failures may route to correction; infrastructure failures route to authorized repair or intervention. Scope violations cannot pass.
4. Fresh independent collection consumes ART-001/003/004/005/008 and prior findings/dispositions. It reruns relevant checks through the controller runner, inspects behavior and code, and publishes ART-006 through IF-002/003. It reports gaps/findings, not final acceptance. Preserve any separately required maintainability/registry roles from the task's applicable workflow.
5. A separate fresh acceptance actor consumes the current ART-001/003/005/006/008 and any ART-010 history. IF-002/003 admits ART-009. Accept makes the candidate gate-eligible. Correction requests route to step 6; missing evidence returns to the relevant check/collection stage; unresolved authority or capability requests intervention. An inconclusive result never completes the task.
6. Authorized correction consumes ART-004/005/006/009. IF-001 counts it once and IF-002 uses a fresh session if context occupancy is unknown. After real file changes, repeat inspection, required checks, fresh collection and separate acceptance. Previous evidence remains historical. Evidence-only recollection is not a new correction unless it launches implementation changes; it cannot erase a prior failure or authorize a fourth correction.
7. Coordinator records any acceptance-approved bounded deferrals as ART-010, within approved scope, preserving IDs and history. IF-004 rechecks current identity, required evidence, terminality, authority and recording receipts. Task changes during recording invalidate affected evidence. Controller publishes ART-007 completion idempotently. Report the accepted candidate, evidence/decision references, known issues and limitations. No automatic commit or next-task release occurs.

All INV-001..008 apply. A required check or material unresolved risk cannot be waived through a known issue. Observations alone do not demand correction; reopening an approved disposition needs new relevant evidence or changed exposure. Use the available installed acceptance policy and documented tracker; this plan does not mandate the proposed JSON migration.

### FLOW-002: interruption and safe handoff

On timeout, cancellation or coordinator loss, persist ART-002/004 and retain work/evidence. IF-002 may establish terminality using supported process/session observations; an absent receipt alone does not prove that launch never occurred. A replacement coordinator reads ART-001/002/007 and exposes the next action through IF-001. It may collect a known terminal result idempotently through IF-003. Live or unknown ownership prevents another actor or completion through IF-004. If terminality cannot be established, persist intervention and stop. This proof requires conservative stop behavior and readable status, not an automatic recovery service.

### FLOW-003: refusal, missing evidence and owner intervention

Invalid requests return a structured refusal without changing authoritative state; diagnostics are separate. Admitted failed checks/findings update ART-005/006/009 and route within approved authority and the correction limit. Missing evidence is collected; broken infrastructure is distinguished from defective product behavior. A requirement ambiguity, missing permission/capability, unresolved terminality or exhausted correction budget persists a blocker in ART-007.

The coordinator presents that blocker and the exact needed decision in the active chat. Keep intervention identity and relay attempts. Relay without an owner response has unknown delivery; silence or elapsed time grants nothing. An explicit response is recorded with available provenance, and acknowledgement is distinguished from a decision authorizing recovery. If that decision authorizes a task/policy revision, use T-002's IF-001 revision path at a safe boundary, increment the state version and invalidate readiness/affected evidence before continuing; a chat reply cannot itself mutate policy. Replacement coordinators retain the same blocker/history. No external service, background notification or general delivery framework is required.

## Implementation task map

Each remaining task needs a bounded brief, verification specification and focused readiness check using the actual available installed workflow before implementation. This map is not an executable manifest. T-001 remains the historical investigation input; T-002 preparation must reconcile it with this revised direction, not require every old qualification gap to pass.

| Task | Depends on | Deliverable and observable completion |
|---|---|---|
| T-001: Establish harness boundary | None | Historical ART-008 and follow-up evidence provide the selected CLI transport and explicit limits. Preserve old acceptance/readiness decisions; this revision does not relabel qualification as passed. |
| T-002: Expose guarded single-task operations | T-001 evidence, reconciled with this revision | IF-001 and ART-001/002/004 express required stages, state/version/reservation, one active operation, frozen approved policy, authorized revision with version increment/readiness and evidence invalidation, and persistent three-correction count. Invalid requests preserve state/files. Prove locally without model launches. |
| T-003: Connect sbx actors and conservative interruption | T-002 | Implements adapter-launched preflight and readiness admission through IF-001/002/003, including precise blockers and no correction charge. IF-002 applies approved model/context and explicit sbx/YOLO policy; observed identities, collection and terminality work. Remove the adapter's incompatible full-access refusal only for authorized policy. Publish the ART-008 successor supplement, chat blocker routing and precise unknown-liveness stop. IF-004 ownership is stop/intervene/blocker persistence; ART-006/009 capture is transport-only. |
| T-004: Collect evidence and repeat bounded correction | T-003 | IF-003 creates ART-003/005/006; independent collection reruns checks and retains findings. Correction changes real failing fixture code, repeats checks/collection, and rejects stale evidence. Separate acceptance remains T-005. |
| T-005: Admit separate acceptance and complete one task | T-004 | ART-009 and IF-004 keep acceptance separate from collection, route missing evidence/correction/blockers, validate deferral recording and complete only the current eligible candidate. Owns semantic ART-009 admission and the completion/publication slice of IF-004. No automatic commit/dependency release. |
| T-006: Deliver coordinator instructions and sbx proof | T-005 | Thin coordinator skill/current references/examples and one real single-task correction/collection/acceptance proof inside sbx. Show conservative interruption status and chat intervention; distinguish deterministic evidence from unrun live checks. |

### T-002 preparation and policy ownership

Use historical transport selection without retaining isolation, inherited-tool/hook qualification, safe-commit or dependency-release proof as entry gates. Confirm current code/coverage and define the minimum state and role transitions above. Actual sbx execution belongs to T-003/006 and is not claimed by T-002's local state tests.

T-002 synchronizes policy representation, constants, schemas and focused tests for `gpt-6.1-sol` low/medium/high, the three-correction limit, fresh correction on unknown occupancy, sbx/YOLO authorization and chat intervention. T-003 applies that policy in adapter behavior and launch records. No silent migration of already frozen runs or active installations is permitted. T-002 also implements the safe-boundary ART-001 revision contract above, including refusal paths, state-version increment and readiness/affected-evidence invalidation; correction history is preserved. Exact record layout and safe old-run refusal wording are delegated to the owning task.

### T-003 through T-005 integration notes

Extend the current ledger, closed outcome families and verification identity rules. Publish exact interface/record changes for each successor. T-003 owns preflight implementation/readiness admission, observed launch identity and conservative terminality; it does not need to prove removal of every extra tool. Its IF-004 slice is stop/intervene/blocker persistence. Its ART-006/009 production means raw adapter transport capture only; it neither validates collection semantics nor admits an acceptance decision. T-004/T-005 extend the one controller admission path for those respective semantics; do not create competing validators or persistence paths. Reviewers still receive read-only assignments and must not edit the implementation, but runtime-enforced read-only access is not this delivery's guarantee.

T-004 owns collection and findings; T-005 owns separate acceptance and completion. Where applicable, keep required discovery, maintainability, registry-update and acceptance roles distinct. `review-collect` names the collection role, not an established installed skill/command. Resolve project-local installed skills first; do not substitute source-only instructions. Any required unavailable role needs explicit source-guided review authority or blocks that task profile.

Acceptance may approve bounded known issues only under applicable policy. Coordinator recording is idempotent and precedes completion; acceptance/discovery do not write the tracker. Use the declared tracker or installed default; choosing JSON storage, an extra classifier or a new repetition-stop rule is not part of this revision.

### T-006 documentation and installation

Rewrite SKILL.md around the actual status/actions, required role sequence, conservative stop, correction budget and truthful reporting. Include one normal loop and one interrupted-operation example. Document actual sbx prerequisites and implemented commands only. Do not claim that owner-supplied branch/containment assumptions were verified.

Inspect `scripts/install_development_skills.py` before any profile/dependency change. Task-orchestrator is not currently in `DEVELOPMENT_SKILL_SOURCES`; do not add it automatically. If a later implementation changes shared dependencies of installed skills, synchronize installer, profile guide, focused tests and README. Publish a usable source invocation path without refreshing an active installation.

## System verification map

Inspect existing coverage first. Fake actors may control responses; they must not replace decisive controller, file, check-runner or gate behavior. Schema/syntax checks establish record structure only.

| Coverage | Setup / observable oracle | Owner |
|---|---|---|
| FLOW-001, INV-003/004/006 | One disposable repository and prepared task; real failing check, real correction and distinct scripted implementation/collection/acceptance identities. Current checks pass after correction; collector reruns them; separate acceptance and gate complete without a commit or second task. | T-004/005/006 |
| FLOW-001-S01, INV-001/002/008 | Adapter-launched preflight with disposable tool/dependency/skill fixtures: complete ready result enables implementation; each missing prerequisite yields a precise blocker. Wrong role, stale inputs, malformed/nonterminal result or unknown liveness cannot establish readiness. Reservation prevents duplicate launch; preflight/retry leaves correction count unchanged. | T-003 |
| IF-001, INV-001/002/008 | Real records/profiles: stale version, duplicate reservation, unauthorized policy edits or attempts to omit required stages leave authority/version/files unchanged. Status gives permitted actions and truthful failure kinds. | T-002 |
| ART-001 revision, INV-001/003, IF-001 | Authorized safe-boundary revision increments state version, changes input identity, clears readiness and invalidates affected evidence; old records and correction count persist. Unauthorized, stale-version, active/unknown-operation or completed-task requests are refused unchanged. New implementation requires fresh preflight. | T-002 |
| Approved policy, IF-001/002 | Focused policy/schema tests plus adapter boundary tests verify approved mapping, recorded sbx/YOLO authority, unknown-context fresh correction and safe old-run refusal. Flags alone do not prove actual actor execution. | T-002/003 |
| FLOW-002, INV-002/007 | Existing subprocess/file fixtures interrupted before/after launch and during collection: no duplicate operation; unknown blocks; history/count/work persist; replacement status gives a precise stop/next action. | T-003/005/006 |
| IF-003, INV-003/004 | Wrong task/role/session/candidate and tracked/untracked/config/task-input edits reject evidence. Collector cannot submit acceptance; same-session acceptance is rejected; missing evidence cannot pass. | T-004/005 |
| INV-005, FLOW-003 | Cycle zero, shared failed-check/review correction routes and duplicate admission: three launches permitted, fourth refused, no count reset after restart; exhaustion preserves partial work and requests intervention. | T-002/004/005 |
| IF-004, INV-006 | Reject failed/stale/inconclusive evidence; accept current valid separate decision once. Preserve known-issue provenance/IDs on replay; failed recording blocks completion; tracker writes cannot conceal implementation drift. | T-005 |
| FLOW-003 intervention | Recoverable failure stays within authority; missing capability/decision or exhausted corrections persists a blocker. Chat relay remains unknown without response; acknowledgement grants only explicit authority. No external send is needed. | T-003/005/006 |
| Actual sbx flow | Separately authorized bounded pilot in an existing sbx: real preflight, identities, files/checks, correction, independent collection and separate acceptance; retain raw outputs and show an intervention in the active chat. | T-006 |

Start with the owning test method/module and broaden only when justified. Existing starting commands from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_codex_worker.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_verification_runner.py
```

These are task-start options, not commands to run every suite now. Local deterministic integration is not real-harness qualification. Billable/networked checks still need exact authorization. If the live pilot is unrun, report that limitation and do not claim the first useful sbx proof complete.

## Risks, assumptions, and delegated choices

The runtime choice and model/context/intervention decisions are settled. Former Q-001/Q-002 are resolved in scope by T-001 transport selection and the owner direction; actual-environment execution remains a T-003/006 proof obligation, not a new undifferentiated T-002 entry gate. No additional owner decision is needed to prepare T-002 against this revision.

Runtime availability inside the actual sbx, required skills/tools and raw live evidence remain execution risks. Preflight must identify a concrete unavailable capability; neither host-machine T-001 probes nor fake runtime tests prove sbx success. Owner-supplied branch and containment assumptions are not protection guarantees. A controller can reject inconsistent records; it cannot guarantee semantic review quality or prevent arbitrary YOLO file edits.

Delegated: local module/helper layout, exact payload/CLI spelling, fixture organization, reliable content-identity representation and concise assignment wording. Not delegated: task authority, mandatory role separation, evidence freshness, correction limit, acceptance conditions, runtime/model changes outside approved policy or permission expansion. Persisted records and a conservative stop are sufficient; do not expand this into a parallel scheduler or crash-recovery service.

## Plan-verification handoff

Run `project-plan-verification` in a fresh/separate session against this revision, its task map, the single-task direction and relevant T-001 reports. The prior review does not cover these changed contracts. Check scope fidelity, producer/consumer closure, required collection/acceptance separation, correction routing, policy ownership and absence of deferred commit/isolation gates.

After independent plan verification, prepare T-002's bounded brief, verification specification and readiness evidence. Preserve the repository soft-stop/handoff rules and write task results beside plans. This plan update does not itself accept T-002 or run the orchestrator.

Delivery is complete when the real authorized sbx loop proves correction, repeated checks, independent collection and separate acceptance; the controller rejects missing/stale evidence and refuses a fourth correction without accepting failed work; interruption leaves a precise safe stop; and current instructions match implemented behavior with applicable independent implementation reviews passed.
