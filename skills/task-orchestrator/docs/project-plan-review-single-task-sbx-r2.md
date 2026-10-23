# Project Plan Review — single-task sbx revision, round 2

Verdict: `ACCEPT`
Review date/session: 2026-10-23; fresh independent verification session. The reviewer did not author the plan, the direction, or any prior review.

Note on output path: `project-plan-review.md` covers the 2026-10-22 bytes and is cited by the current plan as a historical record to preserve. `project-plan-review-single-task-sbx.md` covers the intermediate 2026-10-23 bytes (`f8776c11…`) and returned `CHANGES_REQUESTED`; its F-001..F-004 drove the revision now under review. Both are preserved; this report is written beside them for the current working-tree bytes.

## Reviewed bytes

- `local-harness-orchestration-plan.md` SHA-256: `9e32bc96f8dad2776e94b995aaf2831ef8c788b120ebf8a218a95354a4a811e2`
- `local-harness-task-map.json` SHA-256: `a669e740ee1fcb4a71b9b705d60f2b710e7619bd93ac46023f34534aed7b9082`
- Repository revision: `7fb455a` ("plan update"); both planning artifacts are modified in the working tree (uncommitted); the prior single-task review file is staged as an addition. This verdict applies to the working-tree bytes above, not the committed revision alone.
- These bytes supersede the intermediate bytes (`f8776c11…`, `3d422928…`) covered by the prior `CHANGES_REQUESTED` review and the 2026-10-22 bytes covered by the prior `ACCEPT`. Neither prior verdict is carried forward.
- Active workflow: project-local `.agents/skills/project-plan-verification/` resolved per repository installation rules (AGENTS.md). Its `SKILL.md` and bundled checker were read from the project-local installation; content matched the session-invoked skill including the contract-discovery appendix. No user-global substitution.
- Independence: this reviewer started fresh, did not author the planning artifacts or directions, and reconstructed expected scope from upstream authority before consulting the plan's own flow/task mapping.

## Authoritative sources reviewed

- `direction-single-task-sbx.md` (2026-10-23 owner-confirmed delta; governs this revision and supersedes conflicting old scope).
- `direction-local-harness.md` (2026-10-22 baseline; consulted only for superseded/retained rules and boundaries).
- `correction-and-disposition-options.md` (2026-10-23; approved policy vs recommendations).
- Historical T-001 records the plan declares authoritative: `docs/tasks/T-001/harness-contract.md` (Python-to-Codex CLI transport selection), `capability-follow-up.md`, `reviews/discovery-03.md`, `reviews/acceptance-02.md`.
- Repository `AGENTS.md` (project-local skill resolution, soft-stop/handoff, installer maintenance rules).
- Current code as repository evidence: `scripts/controller_state.py` (still selects `gpt-5.6-sol` low/medium/high, matching the plan's baseline claim), `scripts/controller.py` (public commands `init`, `run-next`, `inspect`, `revise-flow` confirmed), `scripts/codex_worker.py`, `scripts/controller_git.py`, `scripts/verification_runner.py`, `scripts/install_development_skills.py` (`DEVELOPMENT_SKILL_SOURCES` indeed excludes task-orchestrator), installed `.agents/skills/task-implementation-flow/task-acceptance-review/SKILL.md`, and the four focused test modules named in the plan's starting commands (all present).
- No charter/AI-foundation/foundation-readiness artifacts exist for this route; none were invented as entry gates, consistent with both prior reviews.

## Independent reconstruction

### Product outcome

The owner supplies a human-reviewed task brief plus verification document, then starts a coordinator inside an existing Docker sbx machine (separate branch, YOLO actors, owner-supplied operating assumptions). The system checks actual-environment readiness, implements the task, runs deterministic checks, collects fresh independent evidence, and obtains a separate AI acceptance decision. Ordinary failures are corrected within a persistent three-correction budget; the owner is asked only for blockers via the active coordinator chat, and acknowledgement is never authority. Completion requires current required evidence plus separate acceptance; no automatic commit or dependent-task release is a prerequisite. Status and evidence must remain truthful and inspectable across coordinator replacement, and a live pilot that was never run must be reported as unrun.

### Required capabilities / critical journeys

1. Normal loop: preflight in the real sbx (tools, dependencies, required installed skills) → implementation → configured checks → fresh independent collection (no acceptance verdict) → separate fresh acceptance → completion gate, with at least one real failed check or finding and a real correction in between (the direction requires the first proof to include a failed check or finding and a correction).
2. Interruption/coordinator loss: preserve work/evidence/correction count; distinguish live/terminal/unknown operation; unknown liveness stops retry; a replacement coordinator reads a precise next action from durable status.
3. Refusal and intervention: invalid/stale/unauthorized requests change nothing; missing evidence is never a pass; unresolved blockers are persisted and relayed in the active chat; policy changes require the owner-authorized safe-boundary revision path with state-version bump and evidence invalidation.

### Explicit non-goals / constraints

- No sbx provisioning/startup automation, containment/tool-exclusion qualification, parallel work or parallel-writer coordination, automatic commits, multi-task dependency release, background daemon, automatic crash recovery, multi-provider support, automatic skill installation, or general workflow language.
- F-01's tool-exclusion condition and the old outer-permission/inherited-tool/hook qualification gates no longer gate this delivery (owner-confirmed); role separation is enforced via assignments and evidence admission, not filesystem/tool isolation, and this is stated honestly rather than claimed as protection.
- Frozen policy: `gpt-6.1-sol` at low/medium/high; fresh correction session on unknown context occupancy; three-correction limit with initial implementation as cycle zero; chat-only intervention; controller-enforced transitions from structured records, not actor prose.
- Old frozen runs are preserved and refused rather than silently migrated; active installations are not refreshed during a run; installer inspection does not authorize automatic profile additions.

## Structural checks

- Bundled verifier: `PASS` (exit 0). Command: `python3 .agents/skills/project-plan-verification/scripts/verify_plan_artifacts.py skills/task-orchestrator/docs/local-harness-orchestration-plan.md skills/task-orchestrator/docs/local-harness-task-map.json`
- Reference integrity: `PASS`. Bundled cross-references (capabilities, artifacts, interfaces, invariants, flows, tasks) check out, and every repository file cited by the plan (T-001 records, architecture map, operator guide, scripts, tests, examples, installer) was confirmed to exist.
- Task dependency graph: `PASS`; strict T-001 → T-002 → T-003 → T-004 → T-005 → T-006 chain, no cycles. The only runtime loop (correction consumes ART-009 produced by the acceptance stage) is bridged by an explicit seam: T-004 uses admission fixtures until T-005 lands.
- Structural pass establishes reviewability only; it is not the semantic verdict.

## Coverage summary

| Area | Result | Notes |
|---|---|---|
| Scope fidelity | PASS | Direction delta correctly supersedes commit/dependency/isolation gates; deferred list matches; model/context/intervention decisions preserved; no invented scope found. |
| End-to-end flow completeness | PASS | FLOW-001 reaches completion only through current evidence plus separate acceptance; FLOW-002 resolves terminal/live/unknown with idempotent collection of known results; FLOW-003 separates refusal from operational failure and requires the revision path for policy changes. |
| Artifact producer/consumer closure | PASS | ART-001..010 have named producers, sources of truth, consumers and lifecycles; conditional/historical cases are legitimate (see exceptions below). |
| State/lifecycle semantics | PASS | Stage and operation models are representable; correction accounting, terminality, invalidation, revision and completion rules have explicit authority; one MINOR ambiguity about environment-repair budget interaction (F-001). |
| Interface contracts | PASS | IF-001..004 define owners, consumers, inputs/outputs, success and rejection semantics; version/reservation/idempotency covered where material; payload spelling delegated to owning tasks with a publication obligation. |
| Cross-task invariants | PASS | INV-001..008 each have task owners and decisive planned negative/positive evidence, including real-file, real-subprocess and real-runner oracles rather than schema-only checks. |
| Capability/task coverage | PASS | All three capabilities map to flows and tasks; every actor role is owned (preflight now explicitly implemented by T-003); the prior MAJOR ownership gap is resolved in these bytes. |
| Dependency/order composition | PASS | Each successor consumes a predecessor-owned contract; provisional seams (fixtures for ART-009, transport-only capture for ART-006/009) are distinguished from completed runtime behavior. |
| Verification coverage | PASS | Local deterministic integration covers the e2e loop, interruption, refusal, revision and gate; the actual-sbx bounded pilot (T-006) is the real-boundary oracle with an explicit truthful-reporting obligation if unrun. |
| Planning abstraction | PASS | System semantics are concrete where tasks must compose; local layout/payload/fixture choices are delegated without forcing downstream guessing. |

### Flow tracing (reviewer's own reconstruction)

- **FLOW-001:** owner-approved inputs are frozen in ART-001; T-003's adapter-launched preflight reserves via IF-001, runs via IF-002 and admits terminal ART-004 into ART-002 readiness bound to the current ART-001 identity; missing prerequisites produce precise blockers and prevent implementation, and preflight consumes no correction cycle. Implementation is a counted-cycle-zero launch whose claim is not acceptance. The controller's runner executes configured checks into ART-005, distinguishing product from infrastructure failure. Fresh independent collection reruns checks through the same runner and publishes ART-006 without a verdict. A separate fresh acceptance session consumes current ART-001/003/005/006/008/010 and emits ART-009 (accept/correction/missing evidence/blocker); inconclusive never completes. Each authorized correction counts once against the shared three-cycle budget, uses a fresh session on unknown occupancy, and forces repeated inspection, checks, fresh collection and separate acceptance with previous evidence retained only as history. Approved bounded deferrals are recorded idempotently by the coordinator (ART-010); IF-004 rechecks terminality, scope, current evidence and recording receipts and publishes ART-007 completion once, with no commit or dependency release.
- **FLOW-002:** persisted ART-002/004 records plus adapter observations distinguish live/terminal/unknown; an absent receipt is not proof of no launch; a replacement coordinator reads durable status, collects a known terminal result idempotently, and stops while liveness is uncertain. Terminality that cannot be established persists intervention.
- **FLOW-003:** invalid requests return structured refusals with unchanged authority/version/count/files; admitted failures update evidence and route product correction, missing evidence or infrastructure repair within authority; ambiguity, missing permission, unresolved terminality or exhaustion persists a blocker with relay history; acknowledgement is explicitly not recovery authority, and a chat reply cannot mutate policy — only T-002's safe-boundary ART-001 revision can.

### Task order and contract-discovery trace

| Task | Inputs and handoff checked |
|---|---|
| T-001 | Historical; supplies selected CLI transport and truthful limits (ART-008). Preserved as history, not relabeled as passed qualification. |
| T-002 | Consumes T-001 evidence; publishes guarded IF-001, ART-001/002/004 reservation/version/counter semantics, and owns the safe-boundary ART-001 revision (atomic identity + state-version bump, readiness/affected-evidence invalidation, retained history and count). Proves locally without model launches — correctly scoped, since launches are T-003's. |
| T-003 | Consumes T-002's record contracts; implements adapter-launched preflight and readiness admission, applies frozen model/sbx/YOLO policy, observes operation/session identity and terminality, owns stop/intervene/blocker persistence (its IF-004 slice), and publishes the ART-008 successor supplement. ART-006/009 production is raw transport capture only. |
| T-004 | Builds on actor lifecycle; owns ART-006 semantic admission, collection/findings, and evidence-bound correction routing with the shared budget; uses admission fixtures for ART-009 until T-005 lands. |
| T-005 | Owns ART-009 semantic admission and the completion/publication slice of IF-004; consumes T-004's collection contract; extends the single controller admission path rather than creating competing validators. |
| T-006 | Consumes the assembled system; publishes coordinator instructions matching implemented behavior, and runs the separately authorized bounded sbx pilot with truthful limitation reporting. |

Stable ART/IF/INV/CAP/FLOW IDs were retained across this revision and narrowed deliberately (ART-007/IF-004/INV-006 from commit/dependency finalization to single-task completion), so downstream contract discovery does not need to invent new identity. The requirement that each task publish exact interface/record changes for successors gives implemented contracts a concrete discovery handoff. The plan does not prescribe implementation paths for contracts that do not yet exist.

## Findings

### F-001 — Environment-repair launches have no stated budget interaction

Severity: `MINOR`
Affected IDs: `FLOW-001` (S03 route), `FLOW-003-S02`, `ART-002`, `INV-005`, `IF-001`, `T-002`, `T-004`

**Gap / contradiction**
The plan bounds environment repair ("A broken environment routes to bounded repair within authority or intervention") and explicitly carves preflight out of the correction budget, but never states whether an authorized environment-repair launch consumes one of the three shared correction cycles or a separately bounded repair allowance, nor who enforces that bound. The general counting rule ("Each authorized correction launch consumes exactly one of three shared task cycles, including corrections prompted by checks or review") can be read either way, because a repair launch corrects the environment rather than the candidate.

**Why it matters / failure scenario**
T-002 owns the reservation counter and T-004 owns failure routing; they meet at this rule. If T-004 routes repeated infrastructure failures to repair launches as "not corrections" (mirroring the preflight carve-out) while T-002 counts only correction-kind reservations, an unproductive repair loop could outrun the direction's "apply the existing correction limit instead of retrying forever" unless each planner independently invents a bound — and two planners could pick different bounds, diverging in gate/status semantics.

**Smallest plan-level correction**
One clarifying sentence at plan level, e.g.: "An authorized environment-repair launch that can change evaluated files or the environment consumes a correction cycle like any other authorized launch, or is bounded by a separate stated limit enforced by T-002's counter; exhaustion routes to intervention." No implementation detail is needed.

### F-002 — Planning-authority note's claim about the installed acceptance skill is outdated

Severity: `NOTE`
Affected IDs: `ART-010`, `T-005` (context only)

`correction-and-disposition-options.md` states the active project-local acceptance installation "retains the older human-recorder rule", but the installed `.agents/skills/task-implementation-flow/task-acceptance-review/SKILL.md` was verified byte-identical to the source skill on this point and already permits an AI coordinator to record an acceptance-approved bounded deferral without another human confirmation, defaulting to `docs/known-issues.md` unless the repository declares a tracker. The plan's ART-010 matches the installed bytes, so there is no coordination break; downstream planners should not act on the stale claim (e.g., by adding an unnecessary owner-confirmation step).

### F-003 — "No production code … is changed by this plan" wording could be misread

Severity: `NOTE`
Affected IDs: none (plan prose, Planning authority section)

The sentence refers to the planning act itself; the tasks this plan defines do change production scripts (`controller_*.py`, `codex_worker.py`) and instructions. A task planner reading it as a constraint against code changes would contradict T-002..T-006. Clarify the sentence's referent when the plan is next touched.

### F-004 — No calibration strategy for the AI acceptance decision itself

Severity: `NOTE`
Affected IDs: `ART-009`, `T-005`, `T-006`

The loop requires an AI acceptance decision, and the plan validates its *records* deterministically but plans no calibration/eval for the judgment's quality — consistent with the approved direction (deterministic checks plus independent review supply trustworthiness; the classifier is explicitly deferred), and the plan honestly states the controller cannot guarantee semantic review quality. Non-blocking; the disposition notes' recommendation to retain real disputed decisions for later evaluation would be a useful T-006 pilot practice.

## Producer/consumer exceptions checked

- ART-001: owner-supplied human-reviewed inputs plus T-002-owned policy representation; a legitimate external producer combined with a named internal owner of authorized revision.
- ART-008: produced by historical T-001; T-003 publishes a successor supplement rather than rewriting the historical base; consumed by adapter implementer, preflight and operator guide. Terminal historical records (old acceptance/discovery decisions) are intentionally preserved.
- ART-010: conditional artifact; "No tracker is required before a deferral exists" makes its absence-before-first-deferral legitimate. Coordinator is the sole writer; acceptance/discovery do not write the tracker.
- ART-006 prior findings: legitimately absent on first collection; rejected/malformed ART-004 and superseded ART-003/005/006 remain as diagnostic/audit history, never as current authority.
- ART-007: idempotent single publication; blocker records retained with relay history; no consumer needs to rewrite them.
- ART-005: produced only by the controller's verification runner; collector reruns use the same runner, preserving one check-execution source of truth while collection remains independently fresh.

## Open system questions

- Runtime availability inside the actual sbx (CLI, model, required skills/tools) remains an execution risk, not an unowned decision: T-003 owns the real launch/terminality proof and T-006 owns the bounded pilot with an explicit truthful-reporting obligation ("If the live pilot is unrun, report that limitation and do not claim the first useful sbx proof complete"). This does not block ACCEPT.
- No other unresolved system question was found; the task map records `open_system_questions: []`, and the former Q-001/Q-002 are settled by the T-001 transport selection and the owner-confirmed delta without silently importing old qualification gates.

## Verdict rationale

The current bytes address every finding of the prior `CHANGES_REQUESTED` review, verified independently: preflight is now an adapter-launched role with a named actor, T-003 ownership, reservation/record-admission semantics, no correction charge, explicit non-participation in INV-004's independence roles, and a system-verification-map row with decisive fixtures (prior F-001); the IF-004 and ART-006/009 ownership split is annotated in both plan prose and task-map integration boundaries (prior F-002); T-002 owns the safe-boundary ART-001 revision path with version bump and affected-evidence invalidation (prior F-003); the S03 transition label now names the checks stage (prior F-004). Independently reconstructed scope matches the owner-confirmed direction with no missing or invented behavior, and all baseline reuse claims were confirmed against the repository. No BLOCKER or MAJOR finding was identified; the single MINOR finding does not currently threaten correct composition, and no unresolved system question blocks a critical flow. The planning artifacts were not modified during this review.

## Next action

`ACCEPT`: feed the verified plan/task map into downstream task planning. Prepare T-002's bounded brief, verification specification and readiness check through the available installed workflow, per the plan's handoff. This verdict does not authorize the live sbx pilot (T-006 requires its own separate authorization) and does not waive independent implementation reviews. A material change to either reviewed planning artifact requires a fresh independent plan-verification pass on the new bytes.
