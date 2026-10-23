# Project Plan Review — single-task sbx revision

Verdict: `CHANGES_REQUESTED`
Review date/session: 2026-10-23; fresh verification session, independent of the planning session. The reviewer did not author the plan or the direction.

Note on output path: the prior review (`project-plan-review.md`) covers the 2026-10-22 bytes and is cited by the current plan as a historical record to preserve. This report is written beside it rather than overwriting it.

## Reviewed bytes

- `local-harness-orchestration-plan.md` SHA-256: `f8776c011824cb70810832c7adef83de9be7c7f61c37436b4d64dfc11cf6e1ba`
- `local-harness-task-map.json` SHA-256: `3d422928391883984fa1f3acec5aabbc21b5e92eb89dcf672299ab4b335cd0ca`
- Repository revision: `7fb455a55df62723096bffa98cf5ad1ebb4aea4b` ("plan update"); worktree clean for all reviewed paths.
- These bytes supersede the reviewed 2026-10-22 bytes (`98fab11e…`, `7e6a0a37…`) covered by the prior `ACCEPT`; that verdict is stale for this revision and is not carried forward.
- Active workflow: project-local `.agents/skills/project-plan-verification/` (SKILL.md and bundled checker verified byte-identical to the session-provided skill). No global/helper substitution.

## Authoritative sources reviewed

- `direction-single-task-sbx.md` (2026-10-23 owner-confirmed delta; governs this revision and supersedes conflicting old scope).
- `direction-local-harness.md` (2026-10-22 baseline; consulted only for superseded/retained rules).
- `correction-and-disposition-options.md` (2026-10-23; approved policy vs proposals).
- Historical T-001 records the plan declares authoritative: `docs/tasks/T-001/harness-contract.md` (ART-008 v1.0), `capability-follow-up.md`, `reviews/discovery-03.md`, `reviews/acceptance-02.md`.
- Repository `AGENTS.md` (project-local skill resolution, soft-stop/handoff, installer maintenance rules).
- Current code as repository evidence: `scripts/controller_state.py` (still `gpt-5.6-sol` mapping, correction limit default 2), `scripts/codex_worker.py` (still refuses `danger-full-access`), `scripts/install_development_skills.py` (`DEVELOPMENT_SKILL_SOURCES` indeed excludes task-orchestrator), `references/architecture-map.md` headings, existing focused tests.
- No charter/AI-foundation/foundation-readiness artifacts exist for this route; none were invented as gates, consistent with the prior review.

## Independent reconstruction

### Product outcome

The owner supplies a human-reviewed task brief plus verification document, then starts a coordinator inside an existing Docker sbx machine (separate branch, YOLO actors). The system checks environment readiness in the actual sbx, implements the task, runs deterministic checks, collects fresh independent evidence, and obtains a separate AI acceptance decision. Ordinary failures are corrected within a three-correction budget; the owner is asked only for blockers via the active coordinator chat. Completion requires current evidence and separate acceptance; it does not require a commit or releasing another task. Status and evidence must remain truthful and inspectable across coordinator replacement.

### Required capabilities / critical journeys

1. Normal loop: preflight in the real sbx environment (tools, dependencies, required installed skills) → implementation → configured checks → fresh independent collection (no acceptance verdict) → separate fresh acceptance → completion gate; with at least one real failed check/finding and a real correction in between (direction requires the first proof to include a failed check or finding and a correction).
2. Interruption/coordinator loss: preserve work/evidence/correction count; distinguish live/terminal/unknown operation; unknown liveness stops retry; replacement coordinator reads a precise next action.
3. Refusal and intervention: invalid/stale/unauthorized requests change nothing; missing evidence is never a pass; unresolved blockers are persisted and relayed in the active chat; acknowledgement is not authority.

### Explicit non-goals / constraints

- No sbx provisioning/startup automation, containment/tool-exclusion qualification, parallel work, automatic commits, multi-task dependency release, background daemon, automatic crash recovery, multi-provider support, automatic skill installation, or general workflow language.
- F-01's tool-exclusion condition and the old outer-permission/inherited-tool/hook qualification gates no longer gate this delivery (owner-confirmed delta); actors run YOLO and role separation is enforced via assignments and evidence admission, not filesystem/tool isolation.
- Frozen policy: `gpt-6.1-sol` at low/medium/high; fresh correction session on unknown context occupancy; three-correction limit with initial implementation as cycle zero; chat-only intervention; controller-enforced transitions from structured records, not actor prose.
- Old frozen runs must be preserved and refused, not silently migrated; active installations must not be refreshed during a run.

## Structural checks

- Bundled verifier: `PASS` (exit 0). Command: `python3 .agents/skills/project-plan-verification/scripts/verify_plan_artifacts.py skills/task-orchestrator/docs/local-harness-orchestration-plan.md skills/task-orchestrator/docs/local-harness-task-map.json`
- Reference integrity: `PASS` for all bundled cross-references (capabilities, artifacts, interfaces, invariants, flows, tasks).
- Task dependency graph: `PASS`; strict T-001 → T-002 → T-003 → T-004 → T-005 → T-006 chain, no cycles.
- Structural pass establishes reviewability only; it is not the semantic verdict.

## Coverage summary

| Area | Result | Notes |
|---|---|---|
| Scope fidelity | PASS | Direction delta correctly supersedes commit/dependency/isolation gates; deferred list matches; model/context/intervention decisions preserved; no invented scope found. |
| End-to-end flow completeness | FAIL | FLOW-001-S01 (preflight) has no implementing task and no defined role/launch semantics; see F-001. |
| Artifact producer/consumer closure | PASS | ART-001..010 have named producers, sources of truth and consumers; conditional/historical cases are legitimate (see exceptions below). |
| State/lifecycle semantics | PASS | Stage and operation models are representable; correction, terminality and invalidation rules are explicit; preflight transition authority caveat folded into F-001. |
| Interface contracts | PASS | IF-001..004 define owners, consumers, success/rejection semantics; payload spelling delegated to owning tasks with a publication obligation. IF-004 split-ownership clarity folded into F-002. |
| Cross-task invariants | PASS | INV-001..008 each have task owners and decisive planned evidence; preflight coverage gap folded into F-001. |
| Capability/task coverage | FAIL | Every named actor role and stage except preflight is owned by a task; preflight is a required stage with no owning task (F-001). |
| Dependency/order composition | PASS | Linear chain; each successor consumes predecessor-owned contracts; provisional seams are distinguished from real runtime behavior. |
| Verification coverage | FAIL | No verification-map row owns preflight readiness/blocker behavior; only the T-006 pilot touches real preflight (F-001). |
| Planning abstraction | PASS | System semantics are concrete where tasks must compose; local layout/payload choices are delegated without forcing downstream guessing. |

## Findings

### F-001 — Required preflight stage has no implementing task and no defined role/launch semantics

Severity: `MAJOR`
Affected IDs: `FLOW-001` (S01), `ART-002` (readiness state), `ART-004` (assignment record), `INV-001`, `INV-008`; task ownership gap across `T-002`/`T-003`/`T-004`/`T-006`.

**Gap / contradiction**
Preflight is a required stage ("Preflight, collection and acceptance are required stages of this delivery; an optional profile cannot omit them"; INV-001) and FLOW-001-S01 defines a "preflight actor" that runs through IF-002/IF-003 and produces ART-004 plus readiness in ART-002. But:

- The Actors and capabilities table defines Owner, Coordinator, Controller, Harness adapter, Implementation actor, Independent collector and Separate acceptance reviewer — no preflight actor.
- No task boundary or `task_planner_context` implements preflight: T-002 only "expresses required stages"; T-003 covers launch/observe/terminality for the named roles; T-004 covers checks/collection; T-006 only pilots "real preflight". The system verification map has no preflight row; the T-006 pilot is the only mention.
- The plan is internally torn between two mechanisms: line 127 describes preflight as environment readiness checks ("tools/dependencies and available required skills") that could plausibly be controller-local (the controller runs inside the same sbx machine), while FLOW-001-S01 requires an adapter launch (IF-002) and an actor outcome record (ART-004).

**Why it matters / failure scenario**
Each of T-002..T-004 can pass its brief locally without implementing any preflight behavior, because no task's acceptance criteria require it. At T-006 the pilot must then invent the mechanism — a system-level decision the plan delegated away: controller-local check vs actor launch; whether preflight reserves an operation (INV-002) or consumes the correction budget (INV-005); whether its role session participates in INV-004's "three distinct observed roles"; what record admits readiness. Plausible divergences: (a) preflight is silently omitted, violating INV-001/INV-008; (b) preflight degrades to T-004's behavior checks, which do not detect missing tools/dependencies/skills; (c) two tasks implement overlapping preflight paths with different record semantics, so a downstream gate validates the wrong record.

**Smallest plan-level correction**
Assign preflight implementation to one owning task (e.g., T-003 beside adapter launch, or T-002 if preflight is declared controller-local) and state, at plan level: which mechanism applies; the role/provenance requirements if actor-launched (or removal of the IF-002/ART-004 references from FLOW-001-S01 if controller-local); whether preflight reserves an operation and how it interacts with the three-correction budget; which record admits readiness (ART-002 readiness state, with or without ART-004); and add a system-verification-map row with an oracle for preflight readiness and precise blocker output.

### F-002 — IF-004 and ART-006/009 ownership split between T-003 and T-005 is only implicit

Severity: `MINOR`
Affected IDs: `IF-004`, `ART-006`, `ART-007`, `ART-009`, `T-003`, `T-005`.

**Gap / contradiction**
The machine-readable map lists IF-004 for both T-003 and T-005, and lists ART-006/007/009 in T-003's `produces` alongside T-004/T-005. The plan prose does distinguish the slices — T-003 owns stop/intervene and adapter transport ("chat blocker routing and precise unknown-liveness stop"; "Distinct collection/acceptance transports are available for T-004/005"), while T-005 owns the completion half of IF-004 and the semantic acceptance decision — but the JSON carries no annotation marking T-003's ART-006/009 production as transport-level record persistence rather than semantic ownership.

**Why it matters / failure scenario**
A task planner consuming the JSON alone may write T-003 and T-005 briefs that both implement record persistence for ART-006/009 with divergent validation rules (two admission paths for the same evidence class), or may give T-003 the completion half of IF-004 that belongs to T-005. The linear dependency order prevents concurrent mutation but does not prevent duplicate or misplaced implementation.

**Smallest plan-level correction**
In the task map, name which IF-004 operations each task owns (T-003: stop/intervene/persist blocker; T-005: completion gate) and annotate T-003's `produces` entries for ART-006/009 as transport-level records whose semantic content is owned by T-004/T-005.

### F-003 — No task owns the authorized ART-001 revision path at a safe boundary

Severity: `MINOR`
Affected IDs: `ART-001`, `INV-003`, `FLOW-003`, `T-002`.

**Gap / contradiction**
ART-001's lifecycle requires: "Revisions require explicit authority at a safe boundary and invalidate affected evidence." T-002 owns freezing the approved policy, and FLOW-003-S02 notes that policy changes need explicit decisions, but no task boundary names the revision flow itself (authorize revision → state version bump → invalidate affected evidence).

**Why it matters / failure scenario**
A mid-run policy change (e.g., owner authorizes a model mapping change while a task is active) could be applied by whichever task encounters it, without the version bump and evidence invalidation, letting evidence collected under the old policy survive and masquerade as current (INV-003).

**Smallest plan-level correction**
Name ART-001 revision handling in T-002's boundary: version bump and affected-evidence invalidation on authorized revision, refusal otherwise.

### F-004 — Stage-list naming vs transition labels diverge for "checks"

Severity: `NOTE`
Affected IDs: `FLOW-001` (S03).

The lifecycle list names a `checks` stage between implementation and collection, while FLOW-001-S03's transition label reads "terminal -> collection-ready or correction/infrastructure recovery". The semantics are clear from the step's action; aligning the label would remove a small reader-side ambiguity. No coordination consequence identified.

## Producer/consumer exceptions checked

- ART-001: owner-supplied inputs plus T-002-owned policy representation; legitimate external producer combined with a named internal owner.
- ART-008: produced by historical T-001; T-003 publishes a successor supplement rather than rewriting the historical base; consumed by adapter/preflight/operator guide. Terminal historical records are intentionally preserved.
- ART-010: conditional artifact; "No tracker is required before a deferral exists" makes its absence-before-first-deferral legitimate. Coordinator is the sole writer; acceptance/discovery do not write the tracker.
- ART-006 prior findings: legitimately absent on first collection; rejected/malformed ART-004 and superseded ART-003/005/006 remain as diagnostic/audit history, never as current authority.
- ART-007: idempotent single publication; blocker records retained with relay history; no consumer needs to rewrite them.

## Open system questions

- Runtime availability inside the actual sbx (CLI, model, required skills/tools) remains an execution risk, not an unowned decision: T-003 owns the real launch/terminality proof and T-006 owns the bounded pilot with an explicit truthful-reporting obligation ("If the live pilot is unrun, report that limitation"). This does not block ACCEPT once F-001..F-003 are corrected.
- No other unresolved system question was found; the previous Q-001/Q-002 are settled by the owner delta and the T-001 transport selection, and the task map records `open_system_questions: []`.

## Verdict rationale

The revision faithfully implements the owner-confirmed delta: commit/dependency/isolation gates are correctly removed, model/context/intervention policy is frozen with correct owners, role separation is honestly scoped to assignments and evidence admission under YOLO, and the correction budget, stale-evidence and terminality rules are explicit with decisive planned oracles. One MAJOR defect prevents ACCEPT: the required preflight stage has no implementing task, no defined role or launch semantics, and no verification row, so downstream tasks could plausibly omit or reinvent it and change each other's contracts (F-001). Two MINOR items (F-002, F-003) name split-ownership and revision-path clarifications that would otherwise leave small but real coordination ambiguity. The plan was not modified during this review.

## Next action

`CHANGES_REQUESTED`: return F-001..F-003 to the planning owner/agent for correction in `local-harness-orchestration-plan.md` and `local-harness-task-map.json`. Corrected bytes require a fresh independent plan-verification pass before T-002 brief preparation proceeds. No implementation task is authorized by this review.
