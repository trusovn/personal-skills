# Plan amendment handoff — `t-o-new-flow`

**Prepared:** 2026-10-09  
**Repository:** `trusovn/personal-skills`  
**Branch:** `t-o-new-flow`  
**Purpose:** Instructions for a local planning agent to make a **small, bounded amendment** to the existing standalone task-flow plan, informed by the recent issue-triage/invariants discussion and the possible *future* system-level test strategy.

> **Scope of this handoff:** Update the plan, **not** the skills, controller, runtime code, tests, or execution workflow. This is not permission to implement the deferred features.

## 1. Objective and decisions already made

Update the existing plan *only where the current implementation work would otherwise lock in an unnecessarily narrow contract* that will be expensive to revisit later. In particular:

1. Make approved, deferred known-issue records usable as **optional inputs to later cross-issue and portfolio reasoning** while retaining the currently planned simple, coordinator-owned record.
2. Make explicit that **task acceptance** and **portfolio backlog prioritization** are different decisions with different authority. The current acceptance stage does **not** acquire a second portfolio-review responsibility or gate.
3. Preserve a future seam for an **optional system-level verification strategy** after project-plan verification and before detailed task planning, **without adding that artifact or stage to the current workflow**.
4. Preserve the decided format policy: **Markdown for normative prose and explanations; JSON for machine-consumed contracts/outcomes/evidence; YAML is suitable for manually maintained configuration**. Do not initiate a format migration in this plan.

The user explicitly decided to **keep the current testing/qualification scope unchanged**. Do not add new T-005 scenarios, new coverage rows, new mandatory checks, test-fixture responsibilities, or a master test plan in this amendment. Earlier suggestions to add cross-issue regression cases or rebalance verification coverage were exploratory and are **not authorized in the current change**.

## 2. Repository materials to read, in order

Inspect the **actual branch state** before editing; do not use paths or excerpts below as a substitute for current content.

### Current authoritative planning package

- [docs/project-plan.md](https://github.com/trusovn/personal-skills/blob/0ad1706cecc6f7d115e510762bf74c58d732cb6a/docs/project-plan.md) — authoritative human-readable plan for **Standalone task verification and review policy**.
- [docs/task-map.json](https://github.com/trusovn/personal-skills/blob/0ad1706cecc6f7d115e510762bf74c58d732cb6a/docs/task-map.json) — machine-readable relationships among artifacts, interfaces, invariants, flows, and `T-001`–`T-005`.
- `docs/project-plan-review.md` — *historical, byte-bound* independent review; do not treat it as an approval of changed plan bytes.
- `skills/task-implementation-flow/docs/verification-and-review-policy-plan-2026-10-08.md` — dated proposal; the more recent settled decisions in [docs/project-plan.md](https://github.com/trusovn/personal-skills/blob/0ad1706cecc6f7d115e510762bf74c58d732cb6a/docs/project-plan.md) take precedence.

### Supporting context, only when needed

- `skills/task-implementation-flow/README.md`
- `skills/project-delivery-plan/SKILL.md` and `skills/project-delivery-plan/references/task-map-contract.md`
- `skills/project-plan-verification/SKILL.md`
- `skills/task-orchestrator/docs/code-guided-orchestration.brief.md`
- `skills/task-orchestrator/docs/integration-spike-2026-10-08/issues.md` and `integration-guidance.md`
- The separately supplied discussion summary: `issue_triage_portfolio_invariants_discussion_summary.md` (if accessible; this handoff carries the **only approved current-scope deltas**).
- Existing user/repository instructions (`AGENTS.md`, etc.).

**Baseline observations from review on 2026-10-09:** The branch has five tasks (`T-001`–`T-005`), eleven invariants (`INV-001`–`INV-011`), and `ART-008` for coordinator-maintained accepted deferrals. `T-002` creates discovery/decision/known-issue contracts. `T-005` qualifies the existing composed flow. The new code-guided executor, typed machine stage outputs, retained runnable versions, and telemetry remain explicitly outside this standalone plan.

## 3. Required, narrow planning changes

### A. Refine the meaning of `ART-008` (known issues)

Preserve the existing ownership and lifecycle: the **human coordinator** records acceptance-approved, nonblocking deferrals, before authorized advancement; subsequent relevant preflight/acceptance/integration consumes them. Do not change `task-review-discovery` or `task-acceptance-review` into general backlog writers.

The existing record already has: stable ID, task/review/finding provenance, trigger, consequence, evidence, impact/likelihood, affected boundary/consumers, deferral rationale, follow-up owner/action, and reconsideration conditions.

Clarify that a *consequential deferral may additionally reference, **when already known and relevant***:

- Affected **subsystem or area** (for later grouping).
- Existing **invariant, interface, contract, flow, or plan IDs** that the issue affects.
- **Related issue IDs**, distinguishing confirmed relationships from suspected similarity; absence of links means *unknown*, not *no relationship*.
- Important **safeguards or explicit assumptions** relied on for deferral, and concrete changes that should trigger reassessment.
- Relevant **planned work** (migration/refactor/replacement), with a distinction between merely proposed and approved/committed work; planned work is not automatically sufficient to justify deferral.

**Keep all additions optional and proportional.** Do not introduce a formal YAML/JSON issue schema, graph store, mandatory per-issue ontology, fixed severity score, or exhaustive relationship tracking. Do not demand metadata for trivial findings.

**Important scope distinction:** `ART-008` represents *acceptance-approved deferrals*, **not the project's entire open-issue backlog**. A future portfolio analysis may also need GitHub Issues or another authoritative tracker. Do not mislabel `ART-008` as a complete backlog or expand its writer authority.

### B. Clarify local task acceptance vs. portfolio-level action

Make this boundary explicit in the contextual-disposition section and/or `INV-006`/`INV-007`/`IF-005`/`IF-006` wording:

- The current acceptance reviewer decides whether current submitted task bytes meet **required authority, evidence and contextual material-risk obligations**. Material existing risk continues to block under the current rubric.
- An approved, bounded local deferral can later be **promoted, grouped with other issues, or scheduled earlier** at the *project/portfolio level* **without retroactively invalidating the original acceptance verdict** solely because its priority changed.
- Conversely, portfolio scheduling does **not** excuse a demonstrated current AC/gate violation, unauthorized effect, or material risk that the accepted task was required to resolve.
- New facts that invalidate actual acceptance assumptions or reveal a material violation require a focused review under existing authority. This is different from simply changing backlog priority.
- Project-wide priorities and refactoring choices remain with the relevant project/decision owner; the acceptance agent does not silently authorize refactors or create new requirements.

This is a **semantic clarification**, not a second mandatory review, a new verdict, or a new workflow branch.

### C. Preserve the future *optional* master/system verification strategy seam

Record briefly (preferably under **risks/delegated future considerations**, not a new stage) that a project may later use a **derived system-level verification allocation/strategy** after its system plan has been verified and before detailed task planning.

Its possible future purpose: allocate evidence across flows, invariants, interfaces, tasks, and final integration; identify redundant high-level tests, shared fixture/tooling needs, testability gaps, and unowned composition proofs. It may suggest plan corrections but cannot invent requirements or override the normative plan/brief.

**Do not change the present task flow because of this idea.** Specifically:

- Keep current `project-delivery-plan` section 11 / system verification map and its task-map relationships as they stand, except any incidental wording necessary for consistency.
- Keep `task-verification-designer` task-local; it must not silently become a whole-project planner.
- Do **not** require `docs/system-verification-strategy.md`, create a new master-test-plan skill, add a readiness gate or condition, extend test coverage, allocate new test scenarios, or create another mandatory artifact.
- Later experimentation may use the existing `testing-discipline` skill in a fresh, **optional** post-plan session before deciding whether a dedicated skill is justified.

The intent is to **avoid foreclosing a reasonable consumer of the plan**, not to solve the future feature now. If the current plan already supports this without a new statement, prefer a single concise note or **no change**.

### D. Preserve existing document-format boundaries

Retain [docs/project-plan.md](https://github.com/trusovn/personal-skills/blob/0ad1706cecc6f7d115e510762bf74c58d732cb6a/docs/project-plan.md) (human rationale) + [docs/task-map.json](https://github.com/trusovn/personal-skills/blob/0ad1706cecc6f7d115e510762bf74c58d732cb6a/docs/task-map.json) (structured links/IDs). Do not mechanically duplicate normative content in two author-maintained records. Maintain consistency for any IDs or relationships edited in both.

Keep task briefs, task `verification.md`, and standalone human review reports in Markdown for now. JSON/YAML conversion, machine-readable stage sidecars, and runtime protocol schemas belong to the **later orchestration integration**, already called out in spike `FLOW-01`/`FLOW-04`/`FLOW-05` and related findings. Do **not** add their implementation to `T-001`–`T-005` through this amendment.

Do not promise that YAML alone offers a reliable strict-output protocol. For later code-controlled execution, validate explicitly structured outcomes/evidence; Markdown explanations are not machine transition authority.

## 4. Concrete edit surface and alignment

Prefer the **smallest meaningful diff** in:

- [docs/project-plan.md](https://github.com/trusovn/personal-skills/blob/0ad1706cecc6f7d115e510762bf74c58d732cb6a/docs/project-plan.md) — probably `ART-008` in §4, contextual disposition in §6, and at most a brief §12 note. Adjust `IF-005`/`IF-006`, `T-002` handoff, or flow text **only if** necessary to remove a real contradiction.
- [docs/task-map.json](https://github.com/trusovn/personal-skills/blob/0ad1706cecc6f7d115e510762bf74c58d732cb6a/docs/task-map.json) — synchronize **only fields whose semantics changed**: typically `ART-008`, and possibly `INV-006`, `INV-007`, `IF-005`/`IF-006`, `T-002` planner context. Do not reformat or regenerate the whole file unnecessarily.

Do not create/change task count or dependencies. Preserve `T-001`–`T-005` boundaries and already selected proof obligations; **no additional T-005 test scenarios**.

**Do not edit** `SKILL.md` files, templates, installer, tests, runner, schemas, `task-orchestrator` code or plans, the dated proposal, or the historical spike as part of this planning pass. Do not mark independent review as complete.

If a proposed edit would require assigning a new producer/consumer, new transition or mandatory artifact, **stop and report that it exceeds this amendment** rather than silently broadening the plan.

## 5. Validation, handoff, and stopping criteria

1. Inspect branch current state and check repo instructions; preserve unrelated user changes.
2. Apply the smallest relevant changes to [docs/project-plan.md](https://github.com/trusovn/personal-skills/blob/0ad1706cecc6f7d115e510762bf74c58d732cb6a/docs/project-plan.md) and [docs/task-map.json](https://github.com/trusovn/personal-skills/blob/0ad1706cecc6f7d115e510762bf74c58d732cb6a/docs/task-map.json). If the future optional test-strategy concept is already implicitly supported, do not manufacture a requirement merely to mention it.
3. Run the repository's existing **task-map structural validation** using the command documented by `project-delivery-plan` (and any cheap relevant existing validation). This establishes reference consistency only, not semantic completeness.
4. Inspect the diff for normative inconsistencies, new mandatory gates, duplicated policy, changed T-005 test scope, and accidental conflict with the explicitly deferred code-guided executor.
5. **Request a fresh independent** `project-plan-verification` review of changed bytes. The existing `docs/project-plan-review.md` is byte-bound and cannot be automatically carried over; preserve its provenance per existing review conventions. This agent must not self-certify independent acceptance.
6. End with a concise handoff stating: changed sections/IDs; confirmed unchanged scope; validation command/result; remaining questions; next owner/action for fresh review.

### Acceptance criteria for the planning amendment

- Known-issue entries remain coordinator-owned deferrals, now optionally linkable to broader contextual facts without becoming a general tracker.
- Acceptance disposition and portfolio scheduling are unambiguously distinct; existing blocking criteria remain intact.
- Optional future whole-project test allocation can be added **without** a required new stage in this standalone flow; **current testing scope is unchanged**.
- Markdown/JSON responsibilities remain clear and no new sidecar/schema obligations are introduced.
- No new skills, execution stages, tasks, test cases, or unplanned orchestration responsibilities were added.
- Task-map references remain structurally valid; semantic approval is left to the independent reviewer.

## 6. Explicitly out of scope — point to the companion document

Use `deferred-work-after-t-o-new-flow.md` for the ideas deliberately excluded: optional portfolio assessor and deterministic cross-issue checks, automatic assumption invalidation, subsystem summaries, thread-branch batching, formal or lightweight failure trees, standalone system/master test planning, advanced invariant-based testing, and future MD+JSON execution-stage interfaces.

**Guiding principle:** make existing records and authority boundaries usable by future capabilities, without building those capabilities now.
