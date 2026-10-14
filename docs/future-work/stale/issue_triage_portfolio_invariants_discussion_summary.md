# Issue Triage, Portfolio Risk, and System Invariants

**Prioritized synthesis of the discussion · 9 October 2026**  
**Purpose:** Capture ideas worth carrying into future design work—not an implementation plan or a decision to build everything described.

## Central conclusion

The most valuable direction is **connecting local issue decisions to the health, history, and guarantees of the wider system**, without making every issue trigger a large investigation.

A local triage decision and a portfolio-level decision answer different questions:

- **Local disposition:** Must this issue interrupt or block the current task?
- **Portfolio disposition:** Considering other open issues, historical decisions, architectural guarantees, and upcoming work, should it be scheduled, grouped with other issues, investigated, or deliberately deferred?

Both decisions can be valid simultaneously. An issue can be safe to defer from the *current implementation* yet still need attention *before a release or milestone*. Conversely, an apparently urgent local fix may be unnecessary if an approved near-term replacement eliminates the relevant code path and temporary risk is controlled.

The architectural preference throughout the discussion was **explicit, versioned project knowledge plus bounded reasoning**, rather than a long-running agent that implicitly remembers the project. Deterministic checks should surface known relationships and changes; agents should interpret ambiguous trade-offs. A “no warning” result is never proof that a deferral is safe.

---

## 1. Worth doing now / adds substantial value

### 1.1 Separate local triage from broader backlog assessment

Introduce two conceptual responsibilities, even if initially performed through one workflow:

- **Local issue triage** assesses immediate impact, reproducibility, severity, workarounds, current-task risk, and whether the issue blocks progress.
- **Portfolio assessment** considers cumulative technical debt, recurring causes, relationships to prior deferrals, strategic priorities, planned refactors or replacements, and consequences for cross-cutting system guarantees.

The broader assessment should not merely repeat the first agent's judgment. It should ask whether the conclusion changes when the surrounding subsystem and its history are considered. Its useful recommendations include accepting deferral, promoting the issue, consolidating related fixes, requesting investigation, identifying a bounded refactor candidate, or deferring to an already approved change.

**Scope limit:** Do not require two full agent reviews for every issue. Routine issues should pass through a cheap contextual check; only meaningful signals justify deeper portfolio reasoning. The broader assessor advises on portfolio priority—it does not silently override task-level or human decision authority.

### 1.2 Make consequential deferrals explainable and revisitable

A deferred issue should preserve more than a status and short justification. Where consequences matter, record:

- Why deferral is acceptable **in the present context**.
- Which existing safeguards, conditions, or assumptions make it acceptable.
- What event would invalidate the decision (for example, a failing validator, a runner becoming the default, a release approaching, or a planned replacement slipping).
- Any related issues, affected guarantees, and relevant approved work.

This allows older decisions to be revisited for an actual reason rather than relying on an agent's memory. In particular, “a refactor is coming” should not become an indefinite excuse: distinguish a **proposed** refactor from an **approved and scheduled** one, and reassess if its scope or timing changes.

Apply this rigor mainly to meaningful deferrals; requiring elaborate records for trivial defects would create more work than value.

### 1.3 Detect accumulation and relevant cross-issue context cheaply

On issue intake or status change, look for known contextual signals:

- Several unresolved issues affecting the same subsystem or system guarantee.
- Repeated symptoms or suspected shared root causes.
- High churn: recurring regressions, fixes, or maintenance cost in one area.
- A new issue undermining the safeguard used to justify an earlier deferral.
- Relationships to an upcoming milestone, migration, replacement, or architectural refactor.

The goal is **better questions**, not automatic refactor decisions. Ten unrelated cosmetic issues are not equivalent to three recurring defects that repeatedly compromise an important flow. Co-location is not causation; counts and thresholds are prompts to inspect, not verdicts.

A deterministic check can gather explicit relationships and flag changed assumptions. A broader-context agent can then examine whether a group of issues warrants one shared fix, a targeted refactor, or continued deferral. This is a high-value, relatively low-ceremony use of automation.

### 1.4 Treat critical system guarantees as durable planning constraints

Capture a *small, deliberately chosen* set of important cross-task guarantees (invariants) that future features and refactors must preserve. Useful categories include:

- **Business integrity:** e.g., fulfillment cannot be authorized before the required payment is verified.
- **State/lifecycle integrity:** invalid or stale state transitions do not silently succeed.
- **Authorization and isolation:** users, tenants, or agents cannot cross prohibited boundaries.
- **Side-effect safety:** retries do not duplicate irreversible operations.
- **Evidence and provenance:** decisions are tied to the correct run, inputs, and versions.
- **Acceptance authority:** implementation self-reporting cannot substitute for the designated independent acceptance decision.
- **Failure handling:** failed required checks cannot be converted to successful outcomes.
- **Structural architecture:** critical module/dependency boundaries remain enforceable.

Differentiate domain invariants, architecture rules, safety properties, liveness expectations, and performance objectives. Do not treat them as identical kinds of checks. The often-mentioned **5–10 guarantees** is only a sensible *initial focus* for the highest-risk cross-cutting properties, not a required catalog size.

A guarantee should say **what must remain true and in which circumstances**, not how a particular class implements it. Scope matters: for Personal Skills, ordinary best-effort evidence collection is not the same as a workflow where a separate contract makes evidence mandatory. An invariant must not accidentally turn one mode's requirement into a universal rule.

### 1.5 Connect guarantees to task planning and meaningful tests

The useful lifecycle is:

**System guarantee → affected tasks/flows → verification scenarios → executable evidence → maintenance and issue-triage context.**

Define high-level non-negotiables during product direction; clarify cross-component and lifecycle invariants during architecture/system planning, *before* independently implemented tasks diverge. Task briefs should reference applicable guarantees, and verification design should derive observable scenarios without inventing new requirements.

A good invariant produces tests beyond the happy path: rejection and unchanged-state behavior, retries, duplicate/out-of-order events, stale inputs, authorization failures, recovery, and forbidden side effects. Choose the lowest test level that genuinely proves the property, adding integration or end-to-end checks only where the real boundary matters. A returned error alone may be insufficient if an irreversible side effect already happened.

Track the distinction between **specified**, **enforced**, **tested**, **observed passing**, and **not yet verified**. Merely having a test or a prose instruction does not establish system-level protection. Passing tests also do not prove unmodeled behavior.

This can build on existing Personal Skills roles: `project-delivery-plan`, `project-plan-verification`, `architecture-guardrails`, `task-brief-designer`, `task-verification-designer`, `testing-discipline`, and `task-contract-registry-updater`. Prefer reinforcing their existing handoffs over creating a competing invariant-authoring workflow or duplicate catalog.

### 1.6 Keep the review bounded and authoritative

A sensible boundary for the overall process is **one local decision, one inexpensive contextual check, and at most one broader review when warranted**. If evidence is insufficient, record uncertainty or request a focused investigation; do not recurse into agents checking agents indefinitely.

Project files, accepted specifications, issue records, and evidence remain authoritative. An agent's implicit conversation history does not. Preserve the distinction between *verified false*, *known true*, and *unknown*: absence of a reported problem is not evidence that a safeguard works.

---

## 2. Worth considering for the future

### 2.1 A broader-context portfolio-review agent

A separate read-only assessor could periodically—or when meaningful changes occur—review an entire subsystem's open and deferred issues. Its specific value is recognizing that individually acceptable local decisions collectively create risk, recurring rework, or an opportunity for consolidation. It can also reach the opposite conclusion: fixing a soon-to-be-retired component may waste effort if a controlled deferral is safer and cheaper.

The agent should receive curated, up-to-date project facts and produce traceable recommendations. It need not be permanently running or maintain its own private, authoritative project memory.

### 2.2 Subsystem-health summaries

A derived, compact view of each subsystem could collect open issues, trends, recurrent causes, affected guarantees, known safeguards, and planned work. This provides context for triage and periodic reviews without rereading the entire backlog every time.

Avoid turning a raw issue count into a health score or refactor mandate. The most useful summaries distinguish **issue concentration**, **shared cause**, **rate of new problems**, **maintenance burden**, and **strength of supporting evidence**.

### 2.3 Thread branching as an execution optimization

When several portfolio reviews need substantial shared context, prepare a parent context at a known repository/backlog snapshot and fork isolated threads for individual cases. This could reduce repeated research, exploit prompt-prefix caching where the runtime supports it, and avoid contamination among issue-specific discussions.

This is an **optional runtime optimization**, not part of triage correctness. Forks inherit context but do not automatically learn one another's decisions. They therefore need a later reconciliation of newly deferred issues and any emergent combined risks. Large shared contexts may be less efficient than fresh sessions with targeted retrieval; caching savings should not be assumed.

Subsystem-scoped batches may be more useful than a single huge project-wide parent. Context should remain reproducible and not consist primarily of stale exploratory conversation.

### 2.4 A small number of explicit compound-failure rules

Some defects are individually tolerable but dangerous in combination. For example, incomplete evidence becomes a serious acceptance risk when the safeguards intended to reject it also fail or can be bypassed.

For a few **high-consequence, well-understood guarantees**, explicit AND/OR failure conditions could alert when known combinations occur or a relied-upon safeguard is weakened. This borrows the useful insight of fault-tree analysis without adopting a full safety-engineering framework.

Such rules evaluate **declared relationships**; they cannot deterministically discover all possible interactions among software defects. Keep unknown separate from false, and avoid demanding manual review whenever any field is unknown. The cost of noisy alerts may exceed the benefit if rules are added indiscriminately.

### 2.5 Advanced verification derived from invariants

Where an invariant spans complex states or event sequences, future verification might include property-based testing, state-machine/model-based testing, controlled failure injection, or mutation checks showing that the test fails when the protected behavior is broken.

These techniques make sense for high-risk logic, retries, concurrency, event ordering, or durable side effects—not as a blanket requirement for every feature. Reuse the contract and its test oracle when implementation details change.

### 2.6 Learning from confirmed relationships

A reasoning agent may propose a previously unseen relationship between issues or guarantees. Once independently supported, it could become an explicit backlog link, deferral condition, regression scenario, or narrow deterministic rule. Keep proposed links visibly distinct from verified ones. The goal is gradual capture of genuinely reusable knowledge, not unchecked growth of a rule engine.

---

## 3. Investigate before implementing

### 3.1 Does broader review actually change worthwhile decisions?

Replay a modest set of historical issues and compare local-only triage against contextual backlog review. Look for decisions that would genuinely change: an invalidated deferral, an overlooked combined risk, a useful consolidation, a justified refactor candidate, or a wasted fix avoided. Also count irrelevant alerts and time spent on analysis. A richer explanation is not itself an improvement.

If these gains are rare, a simpler issue process is preferable to a standing second agent.

### 3.2 Which context is actually necessary—and what does it cost?

Compare fresh sessions with targeted retrieval, one sequential review session, and forked branches from a shared context. Include the cost of preparing the shared context, repeated tool calls, cached versus uncached input where observable, latency, and—above all—decision quality. Test on several related issues and some unrelated ones.

Do not assume persistent or larger context is more accurate; outdated assumptions, anchoring, and implicit memory drift can make it worse. This study should inform execution strategy, not change the semantics of backlog decisions.

### 3.3 Is the issue history sufficiently structured to support useful alerts?

Check whether existing records distinguish confirmed relationships from speculative similarities; track issue closure/reopening; identify affected areas or guarantees; and preserve why earlier decisions were made. Determine the least additional metadata that materially improves retrieval. Avoid requiring exhaustive tagging or turning every issue into a miniature architecture review.

### 3.4 What makes a planned refactor a valid reason to defer?

Clarify how to distinguish a proposal from committed work, whether the planned change truly removes the defect, whether existing safeguards are sufficient in the meantime, and what happens if the work slips or is cancelled. Similarly, a cluster of issues should justify a refactor investigation—not automatically a rewrite. Compare the shared fix against bounded local repairs and the expected ongoing maintenance burden.

### 3.5 Where can guarantees actually be enforced and observed?

Audit a small end-to-end workflow before expanding the catalog. Separate requirements implemented as code/validation from instructions that merely ask an agent to behave correctly. Check that tests exercise the decisive boundary, not a mocked substitute that would miss bypasses or side effects. Identify gaps without silently changing product policy.

For Personal Skills, acceptance authority, mandatory-versus-best-effort evidence semantics, and run-evidence provenance are promising cases to examine first.

### 3.6 What signals warrant escalation, and when does review stop?

Study whether accumulation, repeated root causes, weakened safeguards, roadmap changes, or failing verification are sufficiently selective triggers. Prefer one meaningful portfolio review to repeated recursive checks. Unknown or incomplete information should lead to a bounded investigation only when it could change an important decision.

### 3.7 Is formal fault-tree analysis ever justified here?

Not as a default investment. Its modeling and maintenance burden is substantial, and an incomplete model can create false confidence. First determine whether simpler related-issue checks, explicit deferral assumptions, and contextual agent reasoning miss consequential compound failures. Only that evidence would justify exploring formal failure trees, probabilities, graph infrastructure, or extensive automated hazard modeling.

---

## Suggested starting scope

A narrow experiment would use **one existing workflow**—for example, bounded implementation → execution evidence → independent acceptance—and a small sample of its historical issues. Identify a few critical guarantees, attach meaningful issue/deferral reasoning to them, and test whether a contextual review surfaces something local triage missed. Reuse the current planning, verification, and contract-discovery capabilities wherever possible.

**Success is not a larger number of checks or agents. Success is better engineering decisions and stronger verification, at a cost low enough that the process is used consistently.**

## Explicit non-goals for now

- No permanent portfolio agent or second source of project truth.
- No universal two-agent approval requirement for every issue.
- No exhaustive formal fault-tree model or graph database.
- No rule that issue counts alone mandate a refactor.
- No automatic promotion of agent-suggested relationships into authoritative policy.
- No blanket conversion of advisory invariants or best-effort workflows into mandatory hard gates.
- No recursive reviews with no defined stopping condition.
