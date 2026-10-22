# T-001 — Final acceptance decision

T-001 meets its investigation brief. ART-008 selects Codex CLI 0.163.0 through
Python subprocesses and records the missing capabilities without claiming runtime
qualification. The investigation is accepted. Affected successor implementation
remains blocked by the capability dispositions in ART-008.

Verdict: **ACCEPT**

Review date: 2026-10-22. Profile: guided.
Provenance: independent acceptance session; this session authored none of the
reviewed implementation, preparation or discovery bytes. This document records
the decision already delivered in the conversation; it does not advance work.

## Authority and evidence

- [Task brief](../brief.md), AC-01..05 and finite risks R1..R3.
- [Verification design](../verification.md), revision 1.
- [Ready preflight](../preflight.md), including Decision context.
- [ART-008 submission](../harness-contract.md), version 1.0, and
  [task-local Git probe](../probe_local.py).
- [Independent discovery-02](discovery-02.md), complete for this investigation;
  [discovery-01](discovery-01.md) supplies historical continuity only.
- Governing direction, plan, task map and accepted plan review referenced by the brief.

Discovery-02 closes discovery-01's unavailable-CLI evidence gap. Its current
independent observations, source traces and validator results support the decision.
Implementer E1–E7 remain producer-attributed claims, reconciled with discovery
C1–C12 and D1–D3. Acceptance reran no behavioral probes or aggregate gates.

## Findings and dispositions

No findings. No approved deferrals. No unresolved acceptance questions or
unchecked investigation rows remain. A passing investigation row does not qualify
a capability that ART-008 marks unsupported or unverified.

## Reconciled coverage

| Stable row | Submitted evidence | Admitted independent evidence | Result and limit |
|---|---|---|---|
| V-01 | E1/E2/E6; selection section | C1–C4 and callable-source traces | pass; prior CLI blocker closed; version/parser support only |
| V-02 / R1 | E3/E4; proposed envelope and recovery cases | C5–C7, A1 and spawn/receipt source traces | pass; wrapper behavior corroborated; idempotent service and real recovery unsupported |
| V-03 / R2 | E1/E2/E6; frozen-policy sources | C1–C4/C9; policy and context-source traces | pass; valid policy accepted and three relevant invalid policies rejected by schema/runtime validators; actual actor enforcement and context measurement unverified |
| V-04 / R3 | E5; commit support and limits | C8 disposable Git assertions and source trace | pass at primitive boundary; integrated crash/index and accepted-path owner-overlap qualification pending |
| V-05 / R3 | E7/docs; proposed notifier | C10/D3 and report trace | pass for honest unsupported disposition; real delivery remains unverified |
| V-06 | Capability dispositions, consumer handoff and submission ledger | Cross-row reconciliation and authority trace | pass; Q-001/Q-002 and T-002..006 effects explicit; no policy change or successor release |
| R1-trace | Duplicate/missing-receipt case table | Worker source: state-path refusal is not atomic idempotency; PID persists after spawn | pass; unknown liveness blocks relaunch; provenance cannot come from actor claims |
| R2-level | Evidence-level labels and missing-proof statement | Selected-boundary trace; fake argv and separate verification-runner policy excluded | pass; no enforcement claim inferred from configuration |
| R3-assume | E5 and explicit limitations | C8 and commit/delivery source/report trace | pass; primitive simulation is not real crash/fsync proof; unknown commit blocks release and delivery failure remains visible |

C11/A3 additionally supplies independent result-validator evidence: a valid
complete result is accepted, while invalid status, collection type and summary
are rejected by both schema validation and the worker result boundary.

## Aggregate gate consumed

- Gate: ART-008 documentary reconciliation. Shell aggregate command: `not run`.
- Status: passed evidence reconciliation in discovery-02 after targeted evidence.
- Owner/stage: independent continuation discovery, iteration 2.
- Reason: verification revision 1 requires report reconciliation rather than a
  repository-wide suite. No required investigation row remained failed or unchecked.
- Current evidence: C1–C12, D1–D3, source traces and byte identities. C5 and C6
  precede C7, the owning transport module check; C8/C9/C11 supply focused Git and
  validator evidence before final reconciliation. No earlier gate substitutes
  for this current record.

## Scope, identity and report publication

Reviewed HEAD: `8efffca9e38855e8229764851d570a72aa7a857b`.
Implementation ownership is limited to `harness-contract.md` and `probe_local.py`.
Brief, preparation and discovery publications are separate existing artifacts.
No production, executable contract, installer or live run record changed.
No maintainability or registry-update stage applies to this task-local report
and probe; the brief expressly excludes creating a registry. Proposed operations
remain labeled as proposed, with current executable declarations unchanged.

At the original decision, task paths were untracked, tracked diffs were empty,
and the index hash matched discovery-02. Before publication, all 16 recorded
file SHA-256 identities and HEAD still matched discovery-02. The seven task
files had since been staged. Each staged blob was compared with its worktree
file and matched exactly. This is staging-only drift; the original decision
applies to unchanged reviewed bytes. Existing staging was preserved.

Pre-publication index SHA-256: `d51517ec88d153a273287918b8de1773c266199051b8cff6051b12ba7983da73`.
Exact pre-publication expanded status:

```text
A  skills/task-orchestrator/docs/tasks/T-001/brief.md
A  skills/task-orchestrator/docs/tasks/T-001/harness-contract.md
A  skills/task-orchestrator/docs/tasks/T-001/preflight.md
A  skills/task-orchestrator/docs/tasks/T-001/probe_local.py
A  skills/task-orchestrator/docs/tasks/T-001/reviews/discovery-01.md
A  skills/task-orchestrator/docs/tasks/T-001/reviews/discovery-02.md
A  skills/task-orchestrator/docs/tasks/T-001/verification.md
```

Publication verification: all seven existing file hashes and the index hash
remain unchanged. The only new status entry is the untracked
`skills/task-orchestrator/docs/tasks/T-001/reviews/acceptance-01.md`.
This scope check verifies report publication, not runtime behavior.

## Residual capability blockers and next route

- Capability owner: prove role/protected-root permissions under the effective
  actor policy and enabled tools; establish frozen-model availability and a
  reliable context occupancy source. Only the owner can approve policy changes.
- T-002/003: qualify reservation, process-start identity, receipt provenance and
  ambiguous-launch recovery before affected execution can proceed.
- T-005: qualify integrated durable commit intent/receipt, exact index
  reconciliation, overlap/layout cases and crash recovery before dependency release.
- Owner, then T-003/006: select and authorize a notification channel/test; prove
  delivery and visible failure/unknown outcomes.
- T-006: separately authorize and prove real independent sessions and the full
  correction, review, commit, dependency and intervention loop.

Next: coordinator hands ART-008 and these blockers to the capability owner for
focused evidence recovery. T-002..006 retain ART-008's implementation gates.
Acceptance of this investigation waives none of those gates. This review makes
no tracker change, commit, dependency release or authorization for a live pilot.
