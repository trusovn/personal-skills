# Project Plan Review

Verdict: `ACCEPT`
Review date/session: 2026-10-22; independent reviewer `/root/plan_review`.

## Reviewed bytes

- `local-harness-orchestration-plan.md` SHA-256: `98fab11ed34846bbe7c0596ea293be5908b763573ac8b0b988f3f4f5441452fd`
- `local-harness-task-map.json` SHA-256: `7e6a0a379c360c373934cfa88ee03dcdf32175aae4cc8ac1286cb7a73f9ad440`
- Repository revision: `3957689fe95f29f9253002140e303e8814a31a41`.
- Worktree: reviewed staged additions of the plan, map and direction, with existing staged documentation cleanup, orchestrator guidance/eval/test changes and an unrelated project-direction fixture change. The verdict applies to the working-tree bytes above, not the committed revision alone. No planning artifact was changed by this review.
- Independence: this reviewer was delegated verification in a separate agent and did not author the plan. No planner explanation was used as evidence.
- Active workflow: project-local `.agents/skills/project-plan-verification/SKILL.md` and its bundled report template/checker.

## Authoritative sources reviewed

- `direction-local-harness.md`: complete owner-confirmed direction for this delivery.
- Repository `AGENTS.md` and the session-provided global instructions.
- `../references/architecture-map.md`, `../references/operator-guide.md`, `../SKILL.md`, and `README.md`: current behavior and limits, read as repository evidence rather than a second direction.
- Current `../scripts/controller_state.py`, `controller.py`, `controller_git.py`, `codex_worker.py`, and `verification_runner.py`: inspected flow/cursor, evidence, transport, Git and containment seams.
- `../assets/step-outcome.schema.json` and focused existing controller/state/transport test cases, including correction envelopes, pending review, drift/publication recovery, live-process rejection and protected installation scope.

This lightweight planning route does not declare separate charter, AI-foundation or foundation-readiness artifacts as prerequisites. None were invented as entry gates.

## Independent reconstruction

### Product outcome

The owner should approve sufficiently defined local tasks and authority once. An agent then handles ordinary implementation, checks, separate review and bounded correction. Code must prevent false completion and unsafe advancement. Accepted work must cross a safe local commit boundary before a dependent task can start. If recovery cannot stay within authority, the owner receives a durable reason and a request for help.

### Required capabilities / critical journeys

- Execute one task, receive a substantive review finding, correct real files, rerun checks, obtain fresh review and complete through a deterministic gate and proven local commit; then release a dependent task.
- Recover after interrupted work or coordinator replacement without duplicating a possible writer, losing findings or resetting the correction count.
- Refuse invalid authority or stale evidence without changing authoritative state; admit real operational failures separately and recover or request intervention.
- Keep status, policy omissions, evidence, commit identity and limitations inspectable without requiring chat history. Notify actively when intervention is needed.

### Explicit non-goals / constraints

- One local repository, sequential tasks, no remote publication, parallel writers, background continuation, plan generation or general workflow engine.
- Fallible agents cannot grant authority, approve their own work or write the controller ledger. Required review roles remain separate.
- Initial implementation is cycle zero; no fourth correction. Approved scope, current evidence, no unresolved blocking findings and established writer terminality constrain completion.
- Preserve unrelated owner work and historical evidence. Keep active runtime/skill installations stable and outside worker-writable scope.
- Harness support must be demonstrated or reported unavailable; neither prompt wording nor fake integration results establish real runtime qualification.

## Structural checks

- Bundled verifier: `PASS` (exit 0).
- Command: `python3 .agents/skills/project-plan-verification/scripts/verify_plan_artifacts.py skills/task-orchestrator/docs/local-harness-orchestration-plan.md skills/task-orchestrator/docs/local-harness-task-map.json`.
- Reference integrity: `PASS` for the bundled structural checks and the planning authority/current-reference links inspected during review.
- Task dependency graph: `PASS`; the six tasks form a strict T-001 through T-006 chain.
- These checks establish structural reviewability only. No application test, live harness pilot, model run or network check was run or claimed.

## Coverage summary

| Area | Result | Notes |
|---|---|---|
| Scope fidelity | PASS | CAP-001..003 implement the direction's reviewed execution, recovery and enforced gates. Local commit, three corrections and intervention-only notification are preserved. |
| End-to-end flow completeness | PASS | FLOW-001 reaches completion only after commit; FLOW-002 resolves terminal/live/unknown; FLOW-003 separates refusal from operational failure/intervention. |
| Artifact producer/consumer closure | PASS | ART-001..008 have named sources, owners and consumers. Initial inputs, absent prior findings and retained history are legitimate external/optional/terminal cases. |
| State/lifecycle semantics | PASS | Reservation, ambiguous launch, correction, evidence supersession, pending commit and completion have explicit authority and outcomes. |
| Interface contracts | PASS | IF-001..004 settle version checks, reservation, observed provenance, evidence admission and finalization. T-001 settles transport spelling before dependent implementation. |
| Cross-task invariants | PASS | INV-001..008 have task owners and decisive planned negative/positive evidence. |
| Capability/task coverage | PASS | All three capabilities have flows and tasks; all six tasks advance the resulting system. |
| Dependency/order composition | PASS | Each successor consumes a predecessor-owned contract; provisional seams are distinguished from complete runtime behavior. |
| Verification coverage | PASS | Real Git/files/checks/controller behavior anchor the fake-actor loop; interruption, stale evidence, commit reconciliation and notification failures have explicit oracles. |
| Planning abstraction | PASS | System semantics are concrete; local layouts and payload details remain delegated without requiring downstream guessing. |

### Flow tracing

- **FLOW-001:** approved ART-001 enters IF-001; the controller selects/reserves and creates ART-002/004. IF-002 executes the authorized actor and obtains observed provenance. IF-003 inspects ART-003 and runs configured checks into ART-005. A stable candidate enters separate review into ART-006. Failed checks or findings share one persisted correction budget; each new candidate invalidates previous verification/review and repeats enabled stages. IF-004 checks scope, evidence, outstanding findings and terminality, records ART-007 commit intent, proves or reconciles the exact task commit, and only then publishes completion/release. Omitted stages remain explicit; unavailable commit cannot become success.
- **FLOW-002:** persisted operation/commit state plus adapter observations distinguish live, terminal and unknown. Terminal results are collected idempotently; a live actor is observed/cancelled; unknown launch or liveness blocks another launch. A reservation without a receipt is explicitly insufficient to infer no launch. A replacement coordinator uses the same ledger, findings and count. Pending commit recovery must precede retry/release.
- **FLOW-003:** wrong subject/role, stale state/evidence, scope or permission expansion produces a structured refusal with unchanged authoritative phase/version/counter/policy/workspace. Actual failed checks or inconclusive reviews may change evidence/eligibility. Ordinary correction stays autonomous; missing authority/capability, uncertain ownership or exhaustion produces durable intervention and attempted notification with truthful delivery failure. No branch releases a dependent prematurely.

### Task order and contract-discovery trace

| Task | Inputs and handoff checked |
|---|---|
| T-001 | Investigates actual current harness/transport capabilities and publishes ART-008 with identity, permission, lifecycle, commit and notifier contracts. Unsupported requirements explicitly block successors. |
| T-002 | Consumes ART-001/008; publishes guarded IF-001 and ART-002/004 reservation/version/counter semantics. It does not need a real launch to prove refusal/ownership guards. |
| T-003 | Consumes the reservation/assignment contract; connects IF-002 and recovery using adapter-owned receipts, real lifecycle/provenance and notification behavior. Review transport is a seam for later review content. |
| T-004 | Builds on actor lifecycle to admit evidence through IF-003 and complete separate review/correction. ART-003/005/006 become current candidate/check/finding contracts; existing Git/verification machinery supplies the reusable inspection source. |
| T-005 | Consumes those current contracts and ART-007 recovery records to implement IF-004 final approval, exact task commit, reconciliation and atomic release. |
| T-006 | Consumes the assembled system, publishes the coordinator instructions/current examples and tests restart/completion reporting. Installer inspection does not authorize automatic profile addition or active-install refresh. |

Stable ART/IF/INV identities provide downstream lookup anchors. The requirement to publish exact record/interface changes after each task gives contract discovery a concrete implementation handoff. No successor must infer contracts from private modules, and the plan does not invent implementation paths for future records.

### Invariants and verification trace

- INV-001/008: T-002/004/005 own authority and explicit evidence states; real invalid-action/profile fixtures check unchanged authority and truthful omissions.
- INV-002/007: T-002/003/005 own reservation, launch and reconciliation; real subprocess/filesystem interruption and replacement-coordinator evidence cover uncertain ownership and durable recovery.
- INV-003/004: T-003/004/005 own observed reviewer identity, candidate binding and final drift checks; wrong task/thread/candidate receipts plus tracked/untracked edits must be rejected.
- INV-005: T-002 guards the persisted counter; T-004 covers failed-check and review routes, three corrections, fourth refusal, replay and restart.
- INV-006: T-005 owns commit intent/proof and atomic completion/release; crash/retry probes include owner staged/unstaged changes and blocked/unknown commits. T-006 composes this with the two-task proof.

The P0 loop requires a real failing check, real changed fixture code and a fresh review response. Fake actors do not replace the decisive controller, filesystem, check runner or gate. The separate P1 pilot tests actual runtime wiring; pending pilot authorization must be reported and cannot be described as full harness qualification.

## Findings

None.

## Producer/consumer exceptions checked

- ART-001 originates with the owner and current initialization; plan-to-manifest generation is explicitly outside delivery scope.
- ART-002 and ART-007 may be absent/empty before initialization or first finalization/intervention. Their ownership is not circular: the controller initializes state and later appends finalization/intervention evidence.
- ART-003 can be produced and consumed within T-004 using existing Git inspection. It does not require a missing predecessor task.
- ART-006 prior findings are absent on first review and become historical input after review. T-003's provenance/transport output is explicitly distinguished from T-004's semantic payload.
- Superseded ART-003/005/006 and rejected ART-004 results are historical evidence, not alternative current authority. Commit/intervention records have recovery, dependency/status and audit consumers.
- ART-008 is produced by T-001 and consumed by all dependent integration work and the operator documentation. Its concrete transport details are an explicit first-task discovery output.

## Open system questions

- Q-001: selected harness capabilities remain unproven. This is the bounded deliverable of T-001, with explicit criteria and a stop path. It does not block starting T-001; it blocks dependent implementation until the contract is concrete. This verdict does not assert that the runtime is feasible or qualified.
- Q-002: compatibility with frozen actor/context rules remains subject to that investigation. T-001 must preserve them or obtain the owner's decision; unavailable usage measurement cannot become zero. Successors cannot silently choose new policy.

Neither question leaves an unowned system decision that downstream implementation may guess. They are executable discovery gates, not permission to implement against assumptions.

## Verdict rationale

No BLOCKER or MAJOR coordination defect was identified. The plan preserves the governing direction and defines the authority, failure, freshness, recovery and commit boundaries needed for composing tasks. It acknowledges real capability uncertainty and assigns it to a prerequisite investigation instead of claiming it solved. Current code inspection supports the stated reuse seams and confirms that present mechanical inspection is not the proposed finished acceptance flow.

## Next action

Prepare the bounded T-001 brief and verification specification through the available installed workflow. Resolve its capability contract before dependent implementation. A material change to either reviewed planning artifact requires a fresh review; this verdict does not authorize a live pilot or waive independent implementation reviews.
