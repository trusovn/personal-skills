# Stage 3 MVP Task-Actualization Map

Status: planning index; not implementation authority and not a commitment to
ten briefs

Primary authority:
[stage-3-mvp-rebaseline.md](stage-3-mvp-rebaseline.md)

## Use of this map

Each row is a candidate briefing unit. A row becomes executable only through a
separate task-actualization brief. Keep an implementation session at or below
the pilot boundary of 35 tool calls and 90 minutes; split a row at a coherent
behavioral and review boundary when preflight shows that it will exceed either
limit. Do not combine rows merely to reduce the brief count.

Draft only `MVP-2` now. After its implementation is independently accepted,
actualize the `MVP-3` increment, starting with `MVP-3A`. Do not draft downstream
briefs against an unaccepted flow contract.

## Candidate index

| Proposed task and outcome | Dependencies | Old S3 disposition | Material decision required before briefing | Intended review | Evaluation gate enabled |
|---|---|---|---|---|---|
| **MVP-2 — Flow contract, profiles, validation, and persisted cursor.** Persist the versioned supported step order, actor modes, stop/escalation rules, correction limit, current step, and correction cycle; reject invalid or authority-changing flows before actor launch. | Accepted S3-08 foundation; no new MVP task. | New contract slice. Preserve S3-01–S3-08; ignore deferred S3-13A–S3-15 and S3-T1–S3-T3 behavior. | None at plan level: immutable flow authority, controller-owned cursor/cycle, the hard 50% correction threshold, and no pre-MVP compatibility guarantee are frozen. The brief may choose the smallest serialization that satisfies them. | `immediate` — guided, strong reasoning, fresh independent acceptance. | Gate 1 flow-contract and profile-validation portion. |
| **MVP-3A — Recovery and safe stop.** Reconcile an interrupted running attempt or stop an owned worker without launching or resuming; refuse mutation or signalling when process identity is live or ambiguous; return a structured runner outcome. | MVP-2 accepted. | **Actualizes [S3-09](history/stage-3-tasks/S3-09-recover-running-and-stop.md)** around the persisted flow and outcome envelope. | Decide whether safe stop is exposed as an operator command, a runner transition, or both; one process-ownership oracle must serve every surface. | `immediate` — high assurance for process ownership, bounded cleanup, replay, and no-duplicate-launch behavior. | Gate 2 cases 5, 7, and 8 recovery/clean-stop prerequisites. |
| **MVP-3B — Same-thread resume and correction.** Consume structured task-local findings, append correction evidence to the recorded thread below 50% context use, or start a fresh handed-off implementation session at or above 50% or when context use is unavailable, without changing scope, flow, or permissions. | MVP-2 and MVP-3A accepted. | **Actualizes [S3-10](history/stage-3-tasks/S3-10-same-thread-resume.md)**; replaces caller-authored clarification prompts with controller-owned structured correction input. | Confirm the durable context-use source and oracle. If no believed-existing source can enforce the threshold, create a proof-only prerequisite rather than letting the implementation brief invent one. | `immediate` — high assurance for thread identity, append-only evidence, threshold routing, and process absence. | Gate 2 cases 5 and 6. |
| **MVP-4A — Preflight/review adapters and structured outcomes.** Add bounded adapters for the selected preflight and semantic-review actors; every review runs fresh and read-only and returns `ACCEPT`, `CHANGES_REQUESTED`, or `INCONCLUSIVE` through the versioned envelope. | MVP-2 and MVP-3B accepted. | No direct old S3 brief. Preserve S3-08 as the mechanical evidence layer; ignore deferred commit/tracker briefs. | Select the concrete preflight and review actor surfaces, their allowed permission envelopes, and the adapter source of structured outcomes. | `immediate` — guided by default; escalate to high assurance if adapter work changes recovery or process ownership. | Gate 2 cases 3, 4, and 7 actor-selection/omission outcomes. |
| **MVP-4B — Review/correction workflow loop.** Route reviewed profiles through implementation, mechanical verification, fresh semantic review, authorized correction, and fresh re-review until acceptance eligibility or a bounded stop/escalation. | MVP-3B and MVP-4A accepted. | No direct old S3 brief. Replaces the historical terminal assumption `semantic_review: not_collected` only when review is enabled; does not reopen S3-08. | Freeze the minimum finding identity/status model and evidence reuse/invalidation rules carried between fresh reviewers and correction implementers. | `immediate` — guided, with fresh independent acceptance; high assurance only if it changes recovery/session ownership. | Gate 2 cases 2, 3, and 7. |
| **MVP-5A — Atomic acceptance and dependency release.** Revalidate the evidence required by the persisted flow, atomically accept exactly the selected task and recompute dependency readiness, and make replay a no-op with commit/tracker effects off. | MVP-4B accepted. | **Replaces [S3-11](history/stage-3-tasks/S3-11-acceptance-operation.md) and [S3-12](history/stage-3-tasks/S3-12-release-dependencies.md)** for the MVP; no prepared-operation/finalizing journal when external side effects are off. | None if the mode-off/no-journal decision remains frozen. Stop briefing if commit, tracker, legacy-run migration, or another external side effect is reintroduced. | `immediate` — high assurance for atomic state, replay, and exact dependency readiness. | Gate 2 cases 1 and 8 acceptance/dependency prerequisites. |
| **MVP-5B — Advance loop and operator reporting.** After a separate successful acceptance transition, invoke the next valid step/task until completion or a real stop, without duplicate selection or launch, and report current position, next step, completed work, and stop reason. | MVP-4B and MVP-5A accepted. | Replaces only S3-12's old operator-driven no-auto-launch end state; preserves the invariant that acceptance itself never launches a worker. Contributes to the replacement of S3-16. | Choose the smallest public runner surface for start/continue/advance and the versioned run-summary boundary; keep presentation work in MVP-6. | `immediate` — high assurance because the loop crosses acceptance, task selection, and process launch boundaries. | Completes Gate 2 cases 1 and 8 and supplies reporting needed by Gates 2–4. |
| **MVP-6 — Plan preparation, confirmation, and thin interface.** Normalize one supported plan/task-document form into reviewable run inputs, stop on material ambiguity, require one explicit confirmation, and start the same runner used by a normalized manifest through a thin skill/command surface. | MVP-5B accepted; MVP-2 supplies the input/outcome contracts. | No direct old S3 brief. Pulls forward the minimum Stage 4 interface and continues to ignore S3-13A–S3-15 and S3-T1–S3-T3. | Approve the supported source-document subset, ambiguity rules, and confirmation surface. These choices define how much authority normalization may derive versus require from the operator. | `immediate` — guided, with focused independent review of ambiguity, scope, and permission stop cases. | Gate 4 bootstrap path and the plan/manifest MVP exit criteria. |
| **MVP-7A — Synthetic and containment evaluation.** Execute Gates 1–3 against disposable repositories and the supported sandbox, then derive one versioned run-summary JSON artifact and one short findings report from controller records and raw logs. | MVP-6 and all prior behavior tasks accepted. | **Replaces the applicable closure target in [S3-16](history/stage-3-tasks/S3-16-stage-3-closure.md)** with Gates 1–3; ignores optional commit/tracker closure. | Name the supported sandbox backend and decide whether failed evaluation returns to the owning task or permits a tightly bounded same-brief correction. Do not mix broad production fixes into an evaluation brief silently. | `milestone` — independent evaluation, not routine implementation acceptance. | Executes Gates 1, 2, and 3. |
| **MVP-7B — Real-task pilot and findings.** Run one operator-approved bounded local task through the reviewed profile with commit, tracker, and network off; record interventions, cycles, evidence reuse/reruns, cost/context data, stops, and changes recommended before the next pilot. | MVP-7A passes. | Replaces the remaining MVP closure target of S3-16 and pulls forward the required Stage 5 real-task pilot. The Gate 5 short task sequence remains a post-MVP follow-on. | Operator must select the real task and approve its repository/run roots, normalized inputs, permission envelope, and genuine-decision intervention rules before briefing. | `milestone` — fresh pilot findings review. | Executes Gate 4 and supplies the final evidence for MVP exit; enables but does not commit Gate 5. |

## Boundary adjustments

Keep the ten rows as the initial map, with these explicit split triggers:

- Split `MVP-2` into contract/validation and cursor integration only if its
  preflight estimate exceeds the pilot boundary; both parts must be accepted
  before `MVP-3A` is briefed.
- Split `MVP-4A` by adapter only if preflight and review use materially
  different transports, permissions, or verification boundaries.
- Split `MVP-6` into preparation/confirmation and interface wiring if the
  normalizer or its ambiguity cases consume the pilot budget independently.
- Split `MVP-7A` between synthetic flow and containment only when the supported
  sandbox requires a distinct environment, permission, or review session.

Do not combine `MVP-3A` with `MVP-3B`, `MVP-5A` with `MVP-5B`, or `MVP-7A` with
`MVP-7B`: each pair separates a state-changing safety boundary from its next
consumer or from externally authorized pilot work. Reassess the remaining
boundaries after the first three implementation/review measurements rather
than pre-writing downstream briefs.
