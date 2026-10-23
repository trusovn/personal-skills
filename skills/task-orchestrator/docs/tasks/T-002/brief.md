# Task Brief: T-002 — Guard one prepared task before connecting actors

Status: `decomposed`
Task kind: `composite`
Brief revision: 1
Date: 2026-10-23

## Outcome

Give the coordinator a controller interface that reports one task's status,
reserves permitted work and revises approved inputs safely. The controller keeps
one active operation and a persistent limit of three corrections. Invalid
requests cannot change task authority or files. T-003 uses this interface to
connect the actual sbx actors.

## Authority and scope

- Authority: [orchestration plan](../../local-harness-orchestration-plan.md),
  “T-002 preparation and policy ownership”, IF-001 and ART-001 revision;
  [task map](../../local-harness-task-map.json), T-002;
  [owner-confirmed direction](../../direction-single-task-sbx.md).
- Accepted plan review: [single-task round 2](../../project-plan-review-single-task-sbx-r2.md).
  At preparation, plan SHA-256 was
  `9e32bc96f8dad2776e94b995aaf2831ef8c788b120ebf8a218a95354a4a811e2`;
  task-map SHA-256 was
  `a669e740ee1fcb4a71b9b705d60f2b710e7619bd93ac46023f34534aed7b9082`.
  Both match the review. Recheck material authority changes during preflight.
- T-001 supplies historical [transport selection](../T-001/harness-contract.md)
  and [limitations](../T-001/capability-follow-up.md). Preserve its
  [discovery](../T-001/reviews/discovery-03.md) and
  [acceptance](../T-001/reviews/acceptance-02.md). Old isolation and commit
  qualification gaps are not T-002 entry gates under the revised direction.
- Stable refs: CAP-001/003; FLOW-001/003; ART-001/002/004; IF-001;
  INV-001/002/003/005/008. Persisted status also supports INV-007.
- Original scope: policy representation and freezing; stage/role records;
  status/version/reservation guards; correction counting; safe input revision;
  focused local behavioral tests and exact successor contracts.
- Out of scope: actor launches, runtime readiness admission, subprocess recovery,
  semantic collection/acceptance admission, final completion, commits, dependency
  release, sbx provisioning, tracker migration and active-install refresh.

## Direction trace and owner decision

This task enables the approved one-task sbx loop. T-003 needs the guarded
assignments before it can connect preflight and implementation. Use
`gpt-6.1-sol` low/medium/high, explicit sbx/YOLO authority, fresh correction
sessions when context occupancy is unknown, and active-chat intervention.
Containment and branch separation remain operating assumptions.

On 2026-10-23 the owner answered **“yes”** to the proposed rule that environment
repair consumes the shared three-correction budget. This resolves F-001 in the
accepted plan review for this task and its successors: an authorized repair
actor that can change evaluated files or the environment consumes one correction
cycle. It has no separate retry allowance. Preflight and evidence-only retries
consume none; an evidence-only assignment cannot authorize repairs. After an
environment repair, preflight must pass again before implementation resumes.
This records the decision beside the plan without rewriting reviewed history.

New direction decisions required: None.

## Execution sizing

- Active policy: project-local `task-brief-designer/references/task-sizing.yaml`,
  `default@1`.
- Original estimate: 36 agent calls, 100 implementation minutes, medium
  confidence; intended profile `strong/high`.
- Triggers: calls greater than 15, duration greater than 40 minutes, and the
  `strong/high` profile pair.
- Boundary decision: split by independently verifiable behavior. Policy freezing
  is needed before reservations; reservations are needed before safe revision.
  The same controller/state files will change sequentially, but each child
  publishes its consumed contract before the next child starts. This reduces
  the scope of each review without creating a second ledger or validator.

## Decomposition

| Child | Owned result | Depends on | Brief |
|---|---|---|---|
| T-002.1 | Frozen single-task policy and required role/stage contracts | Historical T-001 evidence under the revised direction | [brief](../T-002.1/brief.md) |
| T-002.2 | Guarded status, atomic reservations and persistent correction budget | T-002.1 | [brief](../T-002.2/brief.md) |
| T-002.3 | Safe authorized input revision and combined T-002 proof | T-002.2 | [brief](../T-002.3/brief.md) |

## Coverage and closure

| Parent requirement | Owner / proof |
|---|---|
| P-01: approved policy, required stages, frozen inputs and old-run refusal | T-002.1 AC-01..04; composed in T-002.3 AC-04 |
| P-02: status/version and one active operation | T-002.2 AC-01..03; composed in T-002.3 AC-04 |
| P-03: cycle zero plus three shared corrections, including environment repair | T-002.2 AC-04; preserved by T-002.3 AC-01/03/04 |
| P-04: authorized safe revision, atomic identity/version and evidence invalidation | T-002.3 AC-01..03 |
| P-05: invalid requests preserve authoritative state/files; required stages cannot be bypassed | All children; final public-boundary proof T-002.3 AC-04 |
| P-06: exact implemented handoff to T-003, truthful local evidence | Per-child contract notes; consolidated by T-002.3 AC-05 |

ART-001 policy and frozen-input representation belong first to T-002.1;
ART-002/004 reservations and IF-001 status/reserve belong to T-002.2;
ART-001 revision and IF-001 revise-inputs belong to T-002.3. Later children
extend these contracts through the same controller boundary. T-003 owns observed
actor outcomes/readiness; T-004/005 own semantic evidence admission/completion.

T-002.3 is the executable integration child. It proves the parent criteria
together using the real controller, persisted records and disposable files.
Missing actor stages are represented only by explicit test setup, never a
production bypass. Local tests do not qualify sbx execution or provenance.
All leaves fit the active sizing policy on their stated estimates; preflight
must report material scope growth instead of hiding it in those estimates.

## Handoff

Start with T-002.1's derived verification and standalone guided preflight.
Each leaf requires its own ready preflight, implementation and immediate fresh
independent discovery followed by a separate acceptance decision. Apply any
repository-required architecture, maintainability and contract-registry stages
before discovery/acceptance. Resolve installed skills project-locally.

Do not launch this composite parent or advance T-003 until all three children
have completed their required routes. No preflight or implementation evidence
is supplied by this planning package.
