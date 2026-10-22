# Local harness-led task orchestration

Status: READY_FOR_PLAN_VERIFICATION  
Date: 2026-10-22  
Companion: [machine-readable task map](local-harness-task-map.json)

## Intended result

A user starts a local coordinator with an approved task manifest and explicit run policy. The coordinator uses the host agent harness to launch bounded implementation and independent review sessions. It interprets findings and coordinates corrections. A small deterministic controller records progress and rejects invalid transitions. The user receives accepted local changes or a precise stop report with evidence and a resumable next action.

The first useful proof is one task that needs a correction: implementation, an independent review finding, correction, new verification, fresh review, and acceptance. A second dependent task must remain unavailable until the first passes the final gate and its task-scoped commit is proven. The final gate must permit a task-scoped local commit before dependency release. If safe commits are unavailable, report the limitation and keep advancement blocked. No GitHub issues, PRs or cloud service are needed.

## Planning authority

The [owner-confirmed direction](direction-local-harness.md) governs this plan.
It selects agent coordination, a deterministic final gate, early writer and
correction-limit guards, local commits when safely supported, and notifications
only when owner intervention is needed. This proposal does not change runtime
policy or claim that the new flow exists.

Use the [architecture map](../references/architecture-map.md), current code and
focused tests to establish reusable behavior. Validate reused flow/cursor code
inside its owning task; completed task paperwork is not an entry gate.

## Scope

In scope: one repository, sequential tasks, one active actor operation, approved normalized manifest, the existing closed flow representation, local durable records, independent review, bounded correction, safe interruption recovery, acceptance, safe local commit and dependency release. The reviewed profile is the principal proof; optional stages remain governed by explicit policy. Repository-required stages cannot be disabled through a weaker profile.

Deferred: plan-to-manifest generation, GH integration, remote publication, distributed operation, parallel writers, multi-provider framework, automatic skill installation, adversarial tamper resistance, a background daemon, and a general workflow language. Coordinator continuation requires an active harness session; unattended operation after that session ends is not promised.

Code enforces the early writer/correction guards and the final completion gate.
The coordinator owns conversational scheduling and recovery judgment; this plan
does not require a deterministic engine for every intermediate choice.

Priority: preserve authority and truthful evidence first; prove a small usable loop second; minimize custom runtime machinery third. Do not replace missing enforcement with stronger prompt wording.

## Current baseline and reuse

Current controller CLI commands are `init`, `run-next`, `inspect`, and `revise-flow`. Flow/cursor validation exists; the complete reviewed runner and finalization do not. Inspect source and owning tests before reuse.

| Existing component | Intended treatment |
|---|---|
| `scripts/controller_state.py` | Reuse flow validation, persisted cursor, bounded transitions and outcome validation; extend only for new lifecycle evidence. |
| `scripts/controller_git.py` | Reuse scope, baseline and candidate identity checks. |
| `scripts/verification_runner.py` | Reuse controller-owned execution and verification records. |
| `scripts/controller.py` | Keep the public authority boundary; add operation and acceptance use cases. |
| `scripts/codex_worker.py` | Inspect for useful transport behavior. Retain only the necessary supported adapter path; avoid a second competing orchestrator. |
| `assets/*schema.json`, profiles and examples | Evolve together with runtime validation; no parallel state format. |
| Existing controller/state/Git/transport/verification tests | Reuse fixtures and preserved scenarios; add missing behavioral evidence. |

## Actors and capabilities

| Owner | Responsibility |
|---|---|
| User | Approves manifest, scope, policy, permissions and material changes to them. |
| Coordinator agent | Reads controller status; chooses a permitted action; prepares task-local explanations; launches through the supported adapter; waits; requests corrections; reports results. It cannot waive gates. |
| Harness adapter | Converts a controller-authorized operation into harness calls, obtains real session/operation identity, captures outcomes, and exposes wait/cancel/reconcile behavior. |
| Host harness | Executes agent sessions and tools with its supported permission and lifecycle controls. Capabilities must be verified in T-001. |
| Controller | Owns workflow state, operation reservations, authoritative assignments, evidence identity, verification, scope checks, correction counters, final gate, commit evidence and dependency release. It need not dictate every conversational recovery step. |
| Implementation actor | Changes only allowed task files, reports outcome and unresolved questions, and never accepts or commits. |
| Review actor | Starts fresh with read-only access to the candidate and authoritative brief; supplies findings and a structured verdict. Cannot correct its own reviewed candidate. |

Code-interpreted assignments, results, refusals and gate decisions use versioned structured messages; prose cannot authorize completion. Active notifications are reserved for intervention: T-001 establishes the mechanism, T-003 connects it, and T-006 proves it. Successful progress and completion remain in durable status.

The coordinator repeatedly asks for status, follows a permitted operation, and returns the outcome through the adapter. On completion, its report names the accepted task/candidate, verification and review evidence, policy omissions, commit identity or unavailable capability, remaining tasks, and any stop reason. On context loss, another coordinator reconstructs progress from records rather than chat history.

Status must expose run/task identity, flow revision, current phase, candidate identity, active operation, correction count/limit, outstanding findings, required evidence, permitted actions and stop reason. It must not dump raw transcripts by default.

## Artifact and state catalog

The identifiers below are scoped to this plan and its task map.

| ID | Artifact | Producer / sole mutation owner | Consumers and lifecycle |
|---|---|---|---|
| ART-001 | Approved manifest and run policy | User-authorized initialization; controller persists | All actors receive bounded projections. Immutable during active work; explicit revision only at a safe boundary. |
| ART-002 | Run/task state and operation records | Controller | Coordinator and adapter. Atomic state updates; durable reserved/running/terminal/unknown operation identity; historical attempts retained. |
| ART-003 | Candidate identity and scope evidence | Controller Git inspection | Verifier, reviewer, acceptance. Includes relevant tracked and untracked content and task baseline, not only HEAD; any relevant edit supersedes the candidate. |
| ART-004 | Assignment and actor outcome | Controller creates assignment; adapter captures actor output and provenance | Controller validates subject, role, operation and artifacts. Actor claims are evidence inputs, never authority. Malformed output remains diagnostic history. |
| ART-005 | Verification evidence | Controller verification runner | Acceptance and reviewer. Binds command, environment/policy identity, exit outcome and candidate. Superseded evidence remains historical. |
| ART-006 | Review findings and verdict | Independent reviewer via adapter; controller admits records | Coordinator, correction worker and acceptance. Findings retain identity and disposition across cycles; fresh review owns resolution verdict. |
| ART-007 | Acceptance, commit/finalization and intervention records | Controller | Coordinator, dependency selection and future resume. Finalization releases dependencies only after a proven task-scoped local commit; intervention preserves evidence without releasing. Commit intent and receipt support crash reconciliation. |
| ART-008 | Supported harness contract | T-001 capability investigation | Adapter implementer and operator guide. Versioned documentation of tested capabilities, limitations, selected transport, safe commits and intervention notifications. |

All durable run artifacts live outside the task working tree. Workers receive only needed read access and cannot write controller records through supported operations. The coordinator uses the controller API, not file edits. This is an accidental-error boundary under the existing trusted-local-user model, not protection against a malicious user with host access.

## Lifecycle/state models

Operation lifecycle: reserved -> running -> terminal, with unknown launch or
liveness requiring reconciliation before another worker. Task lifecycle: ready
-> implementation -> checks/review -> correction or acceptance-eligible ->
accepted/pending-commit -> committed/completed. Only completed releases dependent
work. Correction returns through checks and fresh review; it never skips the gate.

The initial attempt is cycle zero. Each authorized correction launch consumes
one of three cycles exactly once. Failed checks and review findings share the
same task counter. A replay, crash or coordinator change cannot reset it.

Invalid API requests return structured reasons and permitted alternatives without
changing the authoritative phase, state version, policy, counter or workspace.
Append-only diagnostics may be retained separately. A valid operational outcome
may update task state; request owner intervention only when recovery within
existing authority is unavailable or the correction limit is exhausted.

## System interface map

These are logical operations, not promises of existing CLI names. T-001 fixes the public spelling and transport before dependent implementation.

| ID | Boundary | Contract |
|---|---|---|
| IF-001 | Coordinator -> controller: status/reserve | Read ART-001/002/007; return status and optionally a controller-owned ART-004 assignment. Reservation atomically claims one operation and checks the caller's expected state version. Reject stale state, unauthorized requests, exhausted corrections or another possible writer before launch. Persist the three-cycle counter; recovery judgment otherwise remains with the coordinator. |
| IF-002 | Controller-authorized assignment -> harness adapter | Consume ART-002/004/008; launch/wait/cancel/reconcile and collect ART-004/006 with observed identity. Reusing an operation key must not cause another launch. Unknown launch outcome blocks further work until reconciled. Connect the selected intervention notifier and report delivery failure. |
| IF-003 | Adapter -> controller: collect/inspect/verify | Validate outcome and provenance, inspect ART-003, execute configured verification into ART-005 and admit ART-006. Reject mismatched subject/candidate, stale state, invalid role and unauthorized scope. |
| IF-004 | Coordinator -> controller: accept/recover/advance | Consume ART-001..008. Acceptance requires all configured current evidence and no active operation. Run the final evidence gate, persist commit intent, create/reconcile the exact-path local commit, then publish completion and dependency release atomically. Unavailable or uncertain commit keeps release blocked. Recovery reconciles ownership before allowing a new operation. |

## Cross-task invariants

| ID | Required invariant | Decisive evidence |
|---|---|---|
| INV-001 | Agents cannot change task authority, policy or required stages through outcomes or requests. | Invalid requests leave authoritative state/version and workspace unchanged; separate append-only diagnostics may record reasons. |
| INV-002 | At most one active actor operation; uncertain liveness blocks new launches and finalization; reconciliation remains permitted. | Duplicate/resume/crash boundary tests with real operation records. |
| INV-003 | Verification and review apply to the exact candidate being accepted. | Edit tracked or untracked content after evidence; acceptance rejects it. |
| INV-004 | Enabled review is fresh and separate from implementation and prior review; provenance comes from adapter observations. | Same-thread or invented-session result rejected; separate recorded reviewer admitted. |
| INV-005 | Failed checks and changes-requested findings can enter correction only within the persisted shared correction limit. | Initial attempt uses cycle zero; three correction launches increment once each; replay does not increment; a fourth launch is refused. |
| INV-006 | Final-gate approval plus a proven local commit is the only dependency-release boundary; absent, stale or inconclusive evidence cannot pass. | Pending review, failed verification or missing/uncertain commit blocks dependents; crash/retry cannot duplicate a commit or release. |
| INV-007 | Interrupted operations and historical evidence remain reconstructible after coordinator loss. | Fresh coordinator reconstructs permitted next action from records without a transcript. |
| INV-008 | Omitted-by-policy, passed, failed, stale, blocked and not-run remain distinct. | Profile tests and terminal reports preserve these distinctions. |

Native session identity does not itself prove sandbox enforcement or review quality. T-001 must show how required permissions are applied. If the chosen harness cannot enforce the needed read/write boundary, retain the existing safe transport where possible or mark the capability blocked; do not silently weaken it.

## Capability-to-flow coverage

CAP-001 (reviewed local execution) uses FLOW-001; CAP-002 (durable recovery) uses
FLOW-002; CAP-003 (enforced gates) uses FLOW-001/003. The task map carries task
ownership and artifact/interface references for each capability.

## End-to-end data/process/state flows

### FLOW-001: reviewed local task, correction, acceptance, next task

1. Controller validates ART-001, selects a dependency-ready task, and exposes ART-002 through IF-001. Required preparation runs first; `blocked` or `needs_input` returns to the coordinator for recovery or owner intervention when necessary.
2. Coordinator requests implementation. Controller reserves the operation and produces ART-004; adapter launches through IF-002. The assignment includes exact scope, resolved skill entrypoints, policy, result contract and relevant task inputs.
3. Adapter collects the terminal result. Controller uses IF-003 to validate it and independently inspect ART-003. A complete actor report does not imply acceptance. Scope or authority violations cannot pass the final gate. The coordinator may recover only within approved scope and permissions; otherwise request intervention.
4. Controller executes configured checks, producing ART-005. A task-local check failure may route to correction under policy. Environment/permission failures return a blocker for bounded recovery; missing authority requires intervention. If verification is omitted, mandatory scope/state inspection still runs.
5. Controller permits a fresh reviewer only for a stable candidate. The reviewer receives brief, diff, verification evidence and prior findings as evidence, with no coordinator-supplied desired verdict. IF-002/003 admit ART-006. `INCONCLUSIVE` or `needs_input` requires resolution before acceptance; `CHANGES_REQUESTED` permits bounded correction; `ACCEPT` makes acceptance eligible, not complete.
6. Correction consumes ART-004/005/006 and increments the counter exactly once at authorized start. The implementer may continue its own session if supported and valid, or receive a fresh compact handoff. On correction completion, always repeat mechanical inspection and every enabled verification/review stage for the new candidate. Conservatively invalidate prior verification/review; selective invalidation is deferred.
7. IF-004 rechecks current candidate, scope, operation terminality and required evidence. Controller records gate approval and commit intent in ART-007, creates or reconciles a local commit containing only accepted task work, and records the proven commit. Only then publish completion and dependency release atomically. Preserve unrelated staged and unstaged owner work. A crash or uncertain commit result requires reconciliation before any retry; never blindly commit twice. An unavailable safe commit capability requires intervention and keeps dependents blocked. Coordinator may then request the next ready task. No remote publication occurs.

All INV-001..008 apply. If all tasks are completed through the commit boundary, finish successfully with durable status. If remaining tasks have no eligible dependency order, report blocked dependencies; do not declare completion. Existing optional profile omissions must be reported truthfully. This delivery proves one independently reviewed path; repository-required review cannot be omitted.

### FLOW-002: interruption and coordinator replacement

After launch timeout, cancellation, coordinator loss or a crash, IF-004 consults ART-002 and the adapter's IF-002 status. A completed operation with valid artifacts is collected idempotently. A live operation is observed or cancelled through the harness; it is never duplicated. Unknown status remains stopped/unknown. A stopped operation with missing artifacts can authorize a new attempt only after terminality is established. A replacement coordinator reads ART-001/002/007 and resumes the permitted phase. No counter, previous failure or finding is erased.

A reservation without a known launch receipt is not proof that no launch occurred. The adapter must reconcile by operation identity. If the harness cannot do that, require an operator to establish terminality; do not guess or relaunch automatically.

### FLOW-003: policy or evidence failure

Invalid requests (stale state/evidence, wrong role, permission expansion or an
unauthorized launch) return a structured refusal with a reason and permitted
next action. They leave authoritative phase, version, counter, policy and workspace
unchanged; separate append-only diagnostics do not publish ART-007 or stop a task.

Admitted operational outcomes, such as failed checks or inconclusive review,
update their evidence and eligibility in ART-002/005/006. The coordinator may
recover within existing authority and the three-correction limit. Only when
recovery requires a missing decision, permission or capability, writer ownership
cannot be established, or three cycles fail does the controller persist an
intervention record in ART-007 and the coordinator notify the owner. No refusal
or stop releases dependencies. Ordinary authorized correction needs no new
permission.

## Implementation task map

Each task must produce a bounded brief and verification specification using the available installed workflow before implementation. Read actual code and existing coverage again at task start. The map defines dependencies and cross-task contracts; it is not a directly executable run manifest.

| Task | Depends on | Deliverable and observable completion |
|---|---|---|
| T-001: Establish harness boundary | None | ART-008 and a chosen minimal adapter contract for IF-001/002/004. Show how local sessions, role permissions, identities, outputs, recovery, safe local commits and intervention notifications work, or identify the exact blocked capability. |
| T-002: Expose guarded operations | T-001 | IF-001 and operation state in ART-002/004. Status/reservation enforce authority, writer ownership and the persistent three-correction limit; invalid requests preserve state/version; no new actor launch is needed to prove the gate. |
| T-003: Connect local actors and recovery | T-002 | IF-002 with real lifecycle/provenance collection and IF-004 recovery. One implementation/preflight operation can be launched, collected and reconciled through the chosen harness without bypassing the controller. Connect intervention notifications and truthful delivery-failure reporting. |
| T-004: Complete evidence and correction loop | T-003 | IF-003 plus independent review, stable findings and bounded correction. A rejected candidate is corrected, reverified and independently rereviewed; stale evidence is refused. |
| T-005: Gate, commit and release dependencies | T-004 | IF-004 acceptance with ART-007. Required evidence gates the exact candidate; safe task-scoped commit precedes release; crash/retry cannot duplicate commits, absorb owner work or release partially. |
| T-006: Deliver coordinator skill and local proof | T-005 | Thin coordinator instructions, synchronized current references/examples, and full local flow evidence. A fresh coordinator resumes without reconstructing chat history. |

### T-001 scope and decisions

Inspect local interfaces and official documentation when needed. Separate capabilities actually available to an interactive coordinator from capabilities exposed to a Python controller; a tool available in one does not imply a callable API in the other. Prefer the existing safe adapter if it is the smallest supported bridge. Native harness delegation is preferred only when it satisfies identity, permissions and recovery contracts. Do not build multiple backends for hypothetical portability.

Record the selected API/transport, supported version, operation identity and duplicate handling, role-specific sandbox enforcement, durable result collection, cancellation/terminality evidence, behavior after coordinator replacement, safe task-scoped commit/reconciliation, and an intervention notification mechanism. Resolve exact operation names and how adapter-owned receipts cannot be confused with actor-authored fields. Dependent implementation is blocked until these contracts are concrete. Local introspection is allowed; billable model runs or networked smoke tests need explicit authorization under repository policy.

Existing frozen model/reasoning and context-threshold rules remain in effect unless capability evidence proves a required change. Document such a conflict for an owner decision; do not silently choose new models or treat an unavailable token meter as zero usage.

### T-002 through T-005 integration notes

Extend current controller records and tests rather than creating a second ledger. T-002 owns state-version/reservation semantics; T-003 owns the observable launch handshake and reconciliation; T-004 owns outcome admission, freshness and correction routing; T-005 owns the final gate, safe commit/reconciliation and atomic completion/dependency release. T-003 connects intervention notifications; T-006 checks their delivery and truthful failure reporting. Each publishes its exact record/interface changes for its successor.

Reuse the closed outcome families in `assets/step-outcome.schema.json`. Add a versioned review payload with stable finding identity, severity/blocking status, evidence location and disposition. Preserve unresolved findings across attempts; a worker saying “fixed” does not resolve them. Repository-required discovery, maintainability, registry-update and acceptance roles must remain distinct when applicable. Resolve available installed skills; never pretend source-only skills are installed. Any required unavailable role blocks the affected profile unless a source-guided review is explicitly authorized.

Candidate identity covers the bytes relevant to the task and configured checks, including relevant untracked files, configuration and baseline. Preserve existing verification treatment of generated files. No actor may mutate the workspace between review and acceptance; final drift checks still apply. Reuse existing identity rules where adequate and document any change.

The run directory and active controller/skill installation must remain outside worker-writable scope. For tasks modifying orchestrator source itself, run from a stable installed/snapshotted controller, not the files under implementation. Do not refresh active installations during a run.

### T-006 documentation and installation

Rewrite SKILL.md around status, permitted actions, bounded judgment, delegation, reconciliation and reporting. Include one normal loop and one interrupted-run example. Clearly label current versus deferred capabilities and name only implemented commands. Update operator/index/architecture references and examples with the same contract.

Inspect `scripts/install_development_skills.py` before any profile change. Task-orchestrator is not currently in `DEVELOPMENT_SKILL_SOURCES`; this plan does not authorize adding it automatically. Preserve installer ownership boundaries. If implementation changes dependencies of existing installed skills, synchronize the installer, profile guide, focused tests and README as repository policy requires. Publish a usable source invocation path without modifying the active installation.

## System verification map

Use existing fixtures first. Fake actors may control actor responses, but must not replace the decisive controller, filesystem, verification runner or acceptance logic. The fake correction must change real fixture code and the configured check must actually fail before correction and pass afterward.

| Priority / coverage | Setup and level | Observable oracle | Owner |
|---|---|---|---|
| P0: FLOW-001, INV-003/005/006 | Temporary Git repository with two dependent tasks, runnable failing check, scripted implementation/reviewer outputs and real corrected file bytes; local integration | First review requests a concrete correction; new candidate passes real check and fresh review; only final-gate approval plus the task-scoped local commit releases task two | T-004/005/006 |
| P0: INV-001/008, IF-001 | Real profile/record fixtures, reviewed and review-disabled cases, direct invalid action requests | Missing review blocks reviewed flow; explicit omission stays omission; invalid authority requests leave state/version and workspace unchanged; valid operational failures can record intervention | T-002/004/005 |
| P0: INV-002/007, FLOW-002 | Adapter contract fake plus real subprocess/filesystem interruption tests at reservation, launch, collection and acceptance publication | No duplicate writer; unknown stays blocked; restart gives the same valid next action | T-003/005 |
| P0: INV-003/004, IF-002/003 | Review receipts for wrong task/thread/candidate; edits after checks to tracked and relevant untracked content | Evidence rejected and no acceptance; valid separate reviewer is admitted | T-003/004 |
| P0: INV-005, FLOW-003 | Three-cycle task limit; failed-check and review-findings routes; duplicate collection | Initial attempt uses zero; three corrections allowed; fourth refused; replay/restart cannot reset or add a cycle; exhausted failure requires intervention | T-004 |
| P0: INV-006, IF-004 | Crash/retry before/after local commit and completion publication, with dependent tasks and unrelated staged/unstaged owner changes | No release before proven commit; no duplicate commit; owner work preserved; absent/unknown commit remains blocked | T-005 |
| P0: FLOW-003 intervention | Recoverable refused request, recoverable check failure, exhausted corrections and unavailable commit capability; controlled notifier | Recoverable cases return reasons without owner notification; required intervention persists reason and attempts notification; unavailable delivery is reported truthfully | T-003/005/006 |
| P1: actual harness wiring | Explicitly approved bounded local pilot using selected runtime and independent sessions | Real identities, permission configuration, artifacts and one complete correction loop are recorded | T-006 |

Start with the owning test module or exact method, then broaden after it passes. Relevant existing commands from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_codex_worker.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_verification_runner.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'
```

These are starting commands, not instructions to run every suite for each task. Reuse existing cursor, correction-limit, pending-review, verification-drift and publication-crash cases. Schema checks supplement behavioral tests; they do not prove a successful loop. Final claims distinguish deterministic integration evidence from real harness qualification. If pilot authorization is absent, report “local deterministic flow verified; real harness pilot pending.”

## Risks, assumptions, and delegated choices

Q-001: Which installed local harness interface meets IF-002 and recovery/permission requirements? T-001 owns evidence and selection; T-003 onward cannot assume native tools are programmatically accessible. If no safe path exists, stop with the smallest missing capability and owner options.

Q-002: Do current frozen actor/context rules require revision for that interface? T-001 checks. Only the owner can approve a material policy change; dependent tasks remain blocked if a conflict exists.

Delegated: local helper/module structure, exact JSON payload layout within the versioned contracts, test fixture organization and concise prompt wording. Not delegated: authority, review independence, scope, retry limits, freshness, acceptance requirements or permission expansion.

No claim is made that the coordinator can never become confused. The required guarantee is that supported controller operations cannot accept missing/stale evidence or skip required stages. Human semantic review quality and harness reliability still need evidence.

## Plan-verification handoff

Run `project-plan-verification` in a fresh session against this document and its map before detailed implementation. That review is separate from this authoring session. It must inspect authority conflicts, producer/consumer closure, harness feasibility, stage separation and the task dependency order.

After verification, begin with T-001. Write task outcomes beside these plans rather than updating old task plans. Preserve repository soft-stop/handoff rules. This document's creation does not run the orchestrator or install it.

The implementation is complete when the supported local harness executes the first useful proof, recovery works from durable state, required stages cannot be bypassed, the final gate and proven local commit release dependencies exactly once, current documentation matches executable behavior, and the applicable independent implementation reviews pass. Record any unrun real-harness pilot explicitly instead of claiming full qualification.
