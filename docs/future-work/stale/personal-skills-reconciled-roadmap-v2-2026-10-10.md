# Personal Skills — Reconciled Roadmap for System Verification, Issue Knowledge, and Automation

**Prepared:** 2026-10-10  
**Revision:** 2 — reconciles new issue-triage, correction-history, review-status, and run-evidence upgrade notes. Replaces the initial roadmap version; preserves its underlying planning decisions.  
**Status:** Proposed roadmap and reconciliation; **not** a modification of an accepted plan, approved task scope, or implementation authority.  
**Repository inspected:** [`trusovn/personal-skills`](https://github.com/trusovn/personal-skills), branch `t-o-new-flow`, GitHub HEAD [`520476b1377eedab97c7730f6162dfd8a84b59d3`](https://github.com/trusovn/personal-skills/commit/520476b1377eedab97c7730f6162dfd8a84b59d3) at inspection.  
**Progress baseline:** User reports **T-002 complete**, with T-003 next. The repository's `docs/tasks/index.json` showed T-001/T-002 children and did not yet declare T-003 children. `docs/tasks/T-002.4/results.md` remains an earlier submission-for-review record; it is historical and does not override the user's more recent completion update.  
**Primary goal:** Improve the actual ability to **plan, exercise, independently judge, and increasingly automate system-level verification**, without making routine development depend on a heavyweight process.

---

## 1. Decision in brief

**Do not merge the future proposals into the current T-001–T-005 plan.** That plan is a deliberately bounded stabilization of the *human-coordinated standalone task flow*, with an accepted independent project-plan review. Let T-003, T-004, and T-005 finish under the authority they already have. The immediate two-file test-maintenance guardrail proposed for after T-002.4 is already present in the live source commit above; do not schedule it again.

**Next substantial investment:** pilot a small **system verification allocation + closure** workflow on a real multi-task example using the existing planning and testing skills. Prove that it detects unowned cross-task behavior, weak real-boundary evidence, unnecessary duplicate tests, or missing testability prerequisites that today's project verification map does not catch. If the pilot delivers actionable improvements, institutionalize the *smallest* reusable contract and workflow.

**Then** connect this planning layer to task-local baseline/regression evidence, milestone integration, and independent final-system closure. Develop orchestration, trustworthy runtime evidence, and central storage as *automation enablers*, not as substitutes for knowing what system behavior must be demonstrated.

The organizing loop should be:

> **Approved system behavior / guarantees → decisive observation boundaries → owned proof obligations → targeted implementation/regression → composed verification → independent closure → durable observations/issues/deferrals → reassessment when relevant facts change.**

The added distinction is that **issue observations, approved deferrals, and trustworthy execution evidence are different records**. Each has separate ownership and can share stable task/run/contract identities without being merged into one universal registry. Mechanical checks should perform known, objective work; agents should reason about genuinely ambiguous consequences and repair choices.

**Default:** small/localized work stays light. Larger brownfield discovery, exhaustive schemas, portfolio agents, graph models, and full unattended orchestration are not prerequisites.

## 2. Authority and status rules

Keep four different kinds of documents separate:

1. **Committed current delivery contract:** [`docs/project-plan.md`](https://github.com/trusovn/personal-skills/blob/t-o-new-flow/docs/project-plan.md), [`docs/task-map.json`](https://github.com/trusovn/personal-skills/blob/t-o-new-flow/docs/task-map.json), their **byte-bound** independent [`docs/project-plan-review.md`](https://github.com/trusovn/personal-skills/blob/t-o-new-flow/docs/project-plan-review.md), and authorized task briefs/reviews. They govern T-001–T-005. The plan header still uses a planning handoff status; the separate review report records an `ACCEPT` for specified bytes. Revalidate if authoritative plan bytes have changed; do not infer perpetual approval from the report filename.
2. **Current executable/source behavior:** the *actual versioned source* under `skills/`, `AGENTS.md`, scripts, and tests. `src` changes do **not** automatically refresh `.agents/skills`; selected installed skill copies and their sibling helpers govern invocations, and may lag source.
3. **Design proposals and follow-ups:** the uploaded documents and dated files under `skills/.../docs/`. They document intent, problems, alternatives, and rejected scope. Newer, explicitly settled user decisions and reviewed plans win over older suggestions.
4. **This roadmap:** a **planning candidate** for work after the current scope, with optional low-impact follow-ups. It creates no new required artifact, gate, task-map row, or agent authority in the current flow.

Future decisions should explicitly label an item **implemented / accepted plan / proposed / experiment / deferred / superseded**, rather than treating every promising section of every proposal as a backlog item.

## 3. Baseline: what the current work already supplies

T-001–T-005, under the current plan, collectively own:

| Already planned | Why it matters to the larger objective | What it does **not** prove |
| --- | --- | --- |
| Binding task verification and ready preflight | Requirements cannot silently disappear between task design and execution | Project-wide integration, test architecture, and final system closure |
| Separate `task-review-discovery` and `task-acceptance-review` | Evidence corroboration and authorized decision are independent, with scoped risk judgment | That a multi-task system actually composes |
| `ART-008` coordinator-owned known-issue deferrals | Later relevant consumers can reassess accepted residual issues; consequential deferrals already permit safeguards/assumptions and triggers | A complete issue-occurrence history, machine-evaluable conditions, or complete open-issue backlog |
| T-003 complete correction/conditional-stage handoffs | Findings, failed checks, previous review reports, and unfinished evidence survive repairs | A cross-run recurrence/oscillation index, automatic state transitions, or trusted machine admission |
| T-004 installer/drift/refresh checks | The actual profile invoked can be identified and deliberately refreshed | Retained runnable bundle versions and safe mid-run upgrades |
| Section 11 verification map and T-005 qualification | Critical *standalone policy flows* have allocated local and composed behavioral proof | A general reusable system-verification strategy or independent final review for arbitrary projects |

The existing `project-delivery-plan` already specifies flows, interfaces, invariants, task dependencies and a **system verification coverage map**. `project-plan-verification` already rejects plans where task-local success could leave a critical journey unproven. `testing-discipline` already defines risk-based test selection, real-boundary proof, oracle quality, fixtures and maintenance. Avoid duplicating these capabilities in another master testing manual.

**Observed source change since the urgent proposal:** HEAD `520476b` adds test/eval maintenance guidance to root `AGENTS.md` and `bounded-task-implementer/SKILL.md`. This satisfies the proposed *source policy wiring* in the urgent two-file guardrail. It does **not** establish installed-profile freshness, executed checks, agent behavioral compliance, reviewer-side test-only maintainability scope, or fixture-debt reduction. Qualify only what has actually been exercised.

## 4. Document-by-document disposition

| Source | Status for roadmap | Reconciled disposition |
| --- | --- | --- |
| `docs/project-plan.md` + `docs/task-map.json` | **Current committed baseline** | Complete T-003–T-005 unchanged. Do not retroactively import later ideas into T-005 or mutate reviewed IDs/cases as a convenience. |
| `skills/task-implementation-flow/docs/verification-and-review-policy-plan-2026-10-08.md` | **Historical / partially superseded** | Preserve as provenance. Current plan resolves stage mandates, separate reviews, deferrals, continuation and no global correction limit. Do not build from the older ordered steps independently. |
| `t-o-new-flow-plan-amendment-handoff(1).md` | **Applied design clarification / historical handoff** | Its optional ART-008 links, acceptance-vs-portfolio boundary, and future system-strategy seam are visible in the current plan. No new amendment needed on that account. |
| `urgent-test-suite-guardrail-after-T-002.4(1).md` | **Immediate source patch implemented; proof status distinct** | Two-file patch already landed in `520476b`; avoid duplicate task. Its optional separate reviewer expansion and behavioral qualification remain future decisions. |
| `test-suite-maintainability-integration-proposal(1).md` | **Partly implemented; remainder useful** | Keep prevention in implementer; consider independently authorized test/eval maintainability review after T-003, preferably without disrupting T-004/T-005. Defer fixture consolidation until the flow contract stabilizes. |
| `task-planning-coordination-guidance(1).md` | **Small proposed planning-policy improvement** | Add a bounded independence/shared-decision check to `project-delivery-plan` and corresponding verifier, when those skills next change. Do **not** make every project's task briefs batch-generated or invent `plan_together_with`. |
| `skills/task-implementation-flow/docs/task-decomposition-follow-up-2026-10-09.md` | **Existing P0 plus proposed follow-ups** | Preserve implemented boundary-quality approach. F0 and discriminating F1 evals are worthwhile standalone quality work; F2/F4 later, F3 only after demonstrating costly stale child briefs, F5 after real execution observations. |
| `system-verification-workflow-implementation-plan(1).md` | **Best target-state design, not yet committed** | Preserve its W0–W5 concepts, progressive discovery, baseline/post-change checks and independent system closure. Insert an **experiment/decision gate** before standardizing W1–W2, and avoid a mandatory duplicate artifact for projects already adequately mapped. |
| `deferred-work-after-t-o-new-flow(1).md` | **Useful options/dependency register** | Respect deferrals of structured execution outputs, portfolio reasoning, advanced invariants and optional master strategy. Some orchestration work is already known future scope; optional features remain conditional. |
| `issue_triage_portfolio_invariants_discussion_summary(1).md` | **Ideas, not an approved release plan** | Reuse current invariant IDs and ART-008 context; broader issue aggregation/compound risks require a replay experiment. Its “worth doing now” language must not override the later narrower amendment/deferral decision. |
| `skills/task-orchestrator/docs/code-guided-orchestration.brief.md` + `integration-spike-2026-10-08/*` | **Separate future executor direction** | Typed outcomes, flow authority, effect/freshness evidence, correction ownership, retained runnable bundles and actual collector lifecycle require a **separate orchestrator plan**. Not T-003–T-005. |
| `Run Evidence Upgrade` (new pasted note) | **Specific proposed infrastructure direction; not yet implemented here** | Bring the `.git`-write constraint, external Git-object snapshot experiment, local collector, sandbox ingestion, portability/retention/privacy, and later S3/R2 archive into their own prioritized lane. Do not confuse a reported prototype with a qualified production migration. |
| Additional issue/triage/convergence notes (new) | **Concept proposals; some already partially satisfied** | Separate every issue *occurrence* from its project issue identity and from coordinator-approved deferrals; prefer deterministic known-condition checks. Track correction cycles without new universal loop limits. Reject automatic reviewer mutation of reviewed plans. |

## 5. Reconciliation decisions that prevent rework

### D1. Verification-map extension, not replacement

**Collision:** The existing project plan already has a Section 11 system verification map; the system-verification proposal also wants `docs/system-verification-strategy.md`, `SV-*` IDs and a new skill.

**Decision:** Start with the present map as baseline. Add a separate compact **derived evidence-allocation view only when it solves a real multi-task decision**: which real boundary proves each critical risk, who owns the composed proof, when it becomes runnable, and what remains untestable. Do not create a second normative requirements source or force a stand-alone plan for trivial tasks. `SV-*` IDs are optional until a durable consumer genuinely needs them. Even then, each obligation references authoritative `FLOW/IF/INV` IDs rather than restating their meaning.

### D2. Experiment after approved plans; eventual strategy feedback before approval

**Collision:** The deferred proposal suggests an *optional pass after project-plan verification*; the larger design shows *draft plan → strategy → reconcile → independent plan verification*.

**Decision:** Both can be true at different adoption stages:

- **Pilot now/next:** perform a **read-only optional strategy experiment on an approved example plan**. If it finds a material missing task owner or testability problem, return it to the planner for a focused plan amendment and **fresh independent review of the changed bytes**. The experiment does not rewrite an accepted plan itself.
- **If promoted as a standard for substantive multi-task projects:** derive the strategy from a **draft** delivery plan, reconcile only meaningful shared decisions, and verify the **reconciled planning package** independently before task briefs. The strategy remains conditional on project complexity.
- **Already-running projects:** do not impose a new retroactive stage. Attach focused incremental obligations through authorized future plans/tasks, or record gaps until a normal decision point.

Avoid circular “planning review of review” iterations: one initial allocation/reconciliation pass plus focused resolution of material conflicts.

### D3. Plan-level coordination is not decomposition

**Collision:** `task-planning-coordination-guidance` recommends just-in-time briefs, whereas decomposition F3 notes that one oversized task currently creates complete briefs for all children.

**Decision:** They operate at different scales:

- `project-delivery-plan` resolves **shared system decisions and task dependencies**. Independent top-level tasks get **just-in-time** detailed briefs.
- `task-brief-designer` chooses whether **one oversized task** should have children, with stable child ownership and an integration-closure owner. The current full-brief-on-decomposition behavior is a separate lifecycle concern.
- Prefer an inexpensive downstream brief freshness/delta check before inventing “planned but not executable” child statuses. Only adopt F3 if a few real projects show costly contract churn from eager child briefing.

Neither planning problem warrants a new universal coordinating agent or mandatory batch brief creation.

### D4. Test maintainability now vs changing accepted T-003 scope

**Collision:** The broad proposal would widen `task-maintainability-review` to tests/evals during flow integration, while accepted T-003 explicitly says **remove the blocker cap without widening review scope**.

**Decision:** Keep the two-file preventive patch (already present). **Do not silently expand T-003.** A small reviewer-side scope extension is a separately approved task after T-003, with tests-only provenance, independence and correction invalidation; implement before T-004 only if its benefit outweighs disruption, otherwise after T-005. Large fixture extraction is later, after role/report/package boundaries stop moving. Do not interpret `testing-discipline`'s existing guidance as proof reviewers presently inspect test architecture.

### D5. Local acceptance vs portfolio scheduling

**Collision:** Earlier triage notes propose contextual portfolio review “now,” but the settled amendment keeps the local task decision separate.

**Decision:** Keep the current material-risk rubric and explicit coordinator-owned deferrals. `ART-008` is **only approved deferrals**, not a complete open-issue tracker. Portfolio analysis may later combine it with GitHub Issues and migration plans, but is advisory, triggered and separately owned. A changed portfolio priority alone is not a retroactive task-acceptance failure; actual invalidated safety assumptions or demonstrated violations can require focused review.

### D6. Runtime truth vs documentary claims

**Collision:** Current artifacts are largely Markdown; later code-guided execution needs machine-enforced transitions and trustworthy evidence; central storage is also proposed.

**Decision:** Keep Markdown for rationale and task-local normative guidance. Add schema-validated JSON/JSONL **only** for genuinely machine-consumed stage outcomes, evidence indexes and state transitions. Version policy separately from content identity. Trusted code must capture/validate command exits, Git/filesystem effects, session/runner identity and artifact hashes; an agent-written `success` field is a claim, not evidence. Central storage transports retained evidence; it does not itself establish that a system property passed.

### D7. Current-state inventory vs planned architecture

**Collision:** The broader verification proposal mentions a `system-context.json`-like artifact. Repo foundation and implemented-contract discovery already record real system facts.

**Decision:** Prefer **references to current executable contracts, commands and foundation records**. Only add a lightweight context index where important existing boundaries or data/state flows cannot otherwise be located; mark `observed / verified / assumed / unknown` with provenance/freshness. Shallow pre-planning orientation, focused deeper investigation driven by the plan. No full brownfield survey or second authoritative contract registry in V1.

### D8. Every issue occurrence is observable; not every occurrence deserves a model call

**New decision:** Preserve **each reported occurrence** of a possible issue, including re-reports in later discovery/acceptance/correction cycles. Link occurrences to a stable project issue when the relationship is confirmed; distinguish `new`, `same issue recurring`, `regression`, `related but distinct`, and `unconfirmed`. A repeated finding is an important event even if the backlog already contains the issue. Do not make a new duplicate backlog ticket for every report, silently discard repeated reports, or assume identical text means the same root cause.

Initially, **reuse numbered existing review reports and their finding/continuation IDs as source evidence**. Add a tiny mechanically generated *observation index or append-only event feed* only when a consumer needs cross-report querying or dashboards. The index must carry provenance (source report/line or artifact hash, stage, task, attempt/run, observed bytes, timestamp if captured, reporter/verification state); its issue correlations are revisable without rewriting historical occurrences. GitHub Issues or another explicit chosen tracker remains the owner of open-item status/assignment; `ART-008` remains the **subset of independently acceptance-approved deferrals**. No dual authoritative backlog.

A new `issue-triage` capability can be thin: mechanical policy/contract and evidence checks first; agent reasoning for ambiguous impact, novel relationships and fix-versus-defer trade-offs. Do not create an agent invocation for straightforward missing required evidence, failed required gate, or declared hard-contract breach; these already have deterministic owner routes. Preserve the current mixed-condition acceptance precedence—triage infrastructure does not invent a fourth acceptance verdict.

### D9. Deferral conditions before a broad risk graph

**New decision:** Put *consequential* deferral validity earlier than a portfolio-analysis agent. `ART-008` already allows rationale, safeguards, assumptions and reconsideration triggers. Build the smallest **machine-observable conditional guard** for explicitly declared, important assumptions only. Example: a deferred collector finding relies on `validator rejects incomplete evidence` and `runner remains experimental`; a relevant validator or rollout change must flag the old deferral for reassessment. Track the truth of a condition as **verified / violated / unknown**, with provenance; unknown is not automatically safe or automatically a blocker.

Three increasing levels are distinct:

1. **Conditional deferral validity:** detect when a documented assumption has changed or can no longer be established; request focused re-evaluation by the authorized owner.
2. **Declared cross-issue dependencies:** warnings for issues affecting the same important `INV-*`/boundary; exact known hazardous conjunctions can block *deferral* only if an approved policy makes them binding, with cited current facts.
3. **Executable system guarantees:** real integration/state/property/failure-injection evidence at decisive boundaries. This is the system-verification program, not a promise that a metadata graph proves safety.

Do not adopt full fault-tree methodology or presume a checklist can infer **unexpected** compound failures. A checker surfaces known facts, relationships, and triggers; the coordinator/project owner selects among acceptable repairs. An alert does not itself decide that every affected issue must be fixed. Start by replaying prior consequential deferrals before adding a rule engine or second agent.

### D10. Correction-loop observability is not a retry-limit policy

**New decision:** Reconstruct the full report/correction history using immutable numbered review reports, stable finding IDs, affected scenario/guarantee IDs, source/probe evidence, changed-byte identities, correction attempts and next-stage routes. Detect mechanically when a failing probe recurs after a correction, when fixes oscillate between states, or when a previously resolved issue regresses. These should trigger **a change in diagnosis/verification approach** (e.g., independent root-cause probe), not an automatic additional broad review.

Preserve existing task-specific stop rules and the deliberate **absence of a global correction-round cap**. Do not mistake “same category reported again” for proof of ineffective correction until observations and current bytes support it. No new persistent agent is needed; use bounded history retrieval and focused reasoning when the sequence is genuinely ambiguous. Existing review artifacts remain authoritative; any derived occurrence ledger must cite them.

### D11. Independent approval is a report, not a self-edited plan flag

**New note requiring rejection as written:** “Make review skills update existing plan docs to accepted by default.” On inspected `t-o-new-flow` source, `project-plan-verification` explicitly requires an independent `docs/project-plan-review.md` verdict and **forbids changing the reviewed planning artifacts**. The review is byte-bound; editing `docs/project-plan.md` after approval can invalidate its own recorded hash. `task-preflight` checks executable `brief.md`/`verification.md` and ready status; it does **not** simply require a project-plan header of `accepted`. The note appears to conflate separate authorities or describes a stale consumer problem; confirm the concrete failing consumer before changing skills.

If a downstream launcher insists on a plan-level `accepted` marker, fix it to **resolve the current independent approval report against exact plan and task-map identities**, or let a separate authorized coordinator/controller write an explicit *derived* readiness/status record. The reviewer must not mutate artifacts it just reviewed, and a status update must not masquerade as a renewed independent review. Do not introduce this into current T-003–T-005 unexamined.

### D12. Evidence data plane is separable from cloud and orchestration

**New decision:** Prioritize evidence collection *independently* of the full code-guided executor. The current `run_evidence.py` interface stores metadata under Git metadata and creates Git trees/refs. The new note reports a disposable experiment using `GIT_OBJECT_DIRECTORY`, `GIT_ALTERNATE_OBJECT_DIRECTORIES` and a temporary index to capture trees without writing `.git`; this is **a promising experiment, not yet this roadmap's revalidated implementation**. Object-store references to the original repository can remain nonportable.

Preserve the existing producer's `begin / check / finish / recover` contract and best-effort-vs-required distinction while delivering in separable slices: **E1 external local state/snapshots** (including migration of `.git` history without altering it), **E2 host-side durable ingest for multiple repos/TUIs/sandboxes**, and **E3 optional S3-compatible remote archive and query**. A sandbox submits bounded facts over permitted host access rather than receiving cloud credentials; desktop sessions without tools rely on launcher/controller observation and must declare gaps. Keep one authoritative task/attempt controller; collector records observations, not acceptance verdicts.

Snapshots must disclose `local / portable / unavailable`; “uploaded JSON manifest” must not imply that all referenced Git objects were exported. Explicitly constrain captured stdout/stderr, credentials, PII, code and snapshot uploads. Retain exact historical provenance when mapping old `.git` manifests/refs to the new index. Centralization is useful before the orchestrator; cloud hosting remains a separate cost/security decision.

## 6. Dependency-aware delivery roadmap (revised)

IDs below are roadmap labels, **not additions to `docs/task-map.json`**. There are three streams: trustworthy system verification (**R**), mechanically durable issue decisions (**I**), and evidence transport (**E**). A controller (**O**) can automate them later. Relative order is governed by output contracts, not strict calendar sequencing. Priorities do not authorize changes to the current plan.

| Work package | Outcome and owner boundary | Timing / promotion gate |
| --- | --- | --- |
| **R0 — Finish T-003–T-005** | Stabilized standalone flow and truthful installed behavioral qualification | **Current committed work. No imported requirements.** |
| **R0a — Verify landed test guardrail** | Confirm source-vs-installed consistency and targeted evidence of `520476b` | Cheap, bounded; do not rerun an already documented check without reason |
| **I1 — Issue occurrence and correction history** | Every report has provenance; repeated findings/oscillations discoverable from numbered reviews; no duplicate backlog authority | **Early, read-only replay now; small machine index later** after stable report contracts |
| **I2 — Conditional deferral contracts** | Consequential `ART-008` decisions expose stated safeguards/triggers and can be flagged when known facts change | **High-value next**, initially pilot a handful of real records; do not require metadata for every trivial issue |
| **R1 — System-verification allocation pilot** | Compare existing Section 11 with a fresh risk → real boundary → owner → runnable-point → gap pass | **Highest verification-domain experiment**, can be read-only alongside stable current work |
| **E1 — Evidence outside `.git`** | Same producer contract, external local run state/tree-object handling, migration/replay evidence | **Infrastructure P1**, separate ownership from T-004/005 installer; prototype in isolation now if useful |
| **E2 — Central local ingest** | One host collector with durable queue, idempotent submissions, sandbox/local clients, offline recovery | After E1 interface and identity are sound; no mandatory cloud |
| **R2 — Conditional system verification plan** | R1-proven minimum cross-task allocation, plan reconciliation and independent plan-package review | Only if pilot detects material additional defects or savings |
| **R3 — Targeted before/after task proof** | Relevant implemented baseline, current real-boundary regression, explicit pending system obligations | After R2 ownership semantics are settled; existing plan map may suffice |
| **R4 — First-runnable integration + final closure** | Real composed proofs, independently executable final review and honest gap disposition | After a meaningful multi-task pilot; not equal to local task acceptance |
| **I3 — Deterministic risk-dependency checks** | Known invalidated deferrals, explicit hazardous combinations and impacted guarantees surfaced cheaply | Start with approved condition rules; broader checks only after enough reliable I1/I2 data |
| **I4 — Optional portfolio reasoning pilot** | Compare decisions on historical issues with and without accumulated context; one bounded advisory pass if triggered | After I1/I2; abandon if mostly alerts/explanations without better outcomes |
| **E3 — Optional cloud archive + analytics** | S3-compatible durable snapshots/events, retrieval and simple cross-project queries | After E2 and explicit confidentiality/retention decisions; no dashboard prerequisite |
| **O1 — Code-guided executor** | Typed outcomes, versioned flow policy, trusted evidence admission, interruption/continuation, authorized dependency release | Separate orchestration plan; exploit R/I/E contracts once stable, without owning semantic decisions |
| **R6 — Test/eval maintainability** | Separately approved test-only reviewer scope; later bounded fixture/test-owner consolidation | Optional reviewer patch after T-003 if safe, else after T-005; no blanket fixture rewrite |
| **R7 — Better task decomposition** | F0 naming/split rationale; F1 adversarial behavioral tests; F2/F4 only if warranted | Independent small task, avoiding parallel edits to active flow skills |
| **R9 — Advanced system evidence** | Selective property/state-model/fault-injection/mutation probes; optional larger brownfield discovery | Only for specific high-risk guarantees with reliable oracles |

### 6.1 R0 — Preserve the finishing line

- Treat T-002 complete as the user's latest progress; verify the normal acceptance/continuation/active installation before T-003. The older T-002.4 `results.md` is historical submission evidence, not current approval status.
- Keep T-003 scoped to handoffs, conditional-stage routes, corrections and removal of maintainability's three-blocker cap; maintainability *scope expansion* needs separate authorization.
- T-004 owns installer/drift checks. T-005 owns installed composition qualification, subject to actual model-eval authorization. Neither gains an issue-ledger engine, global verification strategy, or cloud collector by implication.
- Preserve the implemented two-file test-maintenance guardrail, but distinguish source policy, installed copies, structural tests and actual agent compliance.
- Do not rerun wholesale foundation/bootstrap/architecture/plan skills merely because a small rule was added. Re-run project-plan verification only for changed normative planning bytes.

### 6.2 R1 → R4 — System-verification outcomes

**R1:** Use a reviewed multi-task plan and a genuine small project extension. Start with existing `FLOW/IF/INV` IDs and Section 11. Compare current intended proof against a compact matrix: *protected behavior, real observation boundary/oracle, evidence layer, named owner, first runnable point, environment/testability prerequisite, and planned-versus-actually-run status*. Find only material gaps: unowned composed paths, mocked decisive boundary, weak oracle, duplicate expensive high-level tests, or missing shared fixture/integration prerequisite. Record the extra agent/review cost. Possible outcomes: **no new artifact**, improved existing guidance, optional strategy mode, or a dedicated small strategy skill—chosen by observed marginal value.

**R2:** If R1 proves value, preserve one source of product requirements: `project-delivery-plan` owns cross-task contracts/invariants/task order; `testing-discipline` guides proof selection; optional derived system strategy owns evidence allocation only; `project-plan-verification` checks the reconciled package; `task-verification-designer` remains task-local. A draft plan may receive a strategy challenge *before* independent verification once this becomes established. Approved plans can be challenged read-only, but changes to committed meaning require plan-owner amendment and fresh review of changed bytes. `SV-*` obligation IDs are conditional on an actual downstream consumer, not mandatory ontology.

**R3:** At task entry, establish targeted passing/failing existing context for touched contracts, and record unavailable baselines. After implementation, run relevant real-boundary and neighbor checks rather than automatic whole-suite regression. The implementer decides whether tests should be reused, modified, added or carefully retired. Discovery and acceptance report what the task and its current neighbors demonstrate, **not** system closure for incomplete sibling tasks.

**R4:** Assign each critical composed path a first-runnable task/milestone owner. Execute it when available, then independently inspect current evidence and implemented behavior at final closure. Missing/weak/stale evidence routes to bounded test/implementation corrections and a new fresh review. Distinguish `VERIFIED`, explicitly authorized `VERIFIED_WITH_ACCEPTED_LIMITATIONS`, and `INCOMPLETE/BLOCKED`. No accept-by-assertion.

### 6.3 I1 → I4 — Issue evidence, convergence and contextual risk

**I1 minimal observation contract, preferably derived from existing reports:**

```text
observation ID; source report + exact finding ID/path/hash; source stage;
project/task + optional run/attempt/session; observed bytes/revision;
reported symptom + triggering probe; certainty (confirmed/suspected/unknown);
issue correlation ID (if confirmed); occurred_at (if independently captured)
```

An observation is immutable historical evidence. A single project issue can accumulate **many** observations; a suspected relation is not silently promoted to identity. Preserve *every reported occurrence* as requested, but avoid a model call for dedup/counter updates. If the same issue is mentioned in multiple independent reports, retain all reports, not just an incremented count. The issue tracker keeps current status/owner; do not force `ART-008` to hold every unresolved finding. Offer a simple query: *what appeared before correction, after correction, and on the next iteration?* Track recurrence and correction effort over time, not crude unresolved issue counts alone.

**I1 convergence checks:** correlate failing scenario/observable effect, attempted corrections, and repeated observed bytes. Surface `unresolved`, `recurred after correction`, `regressed`, or `newly observed`. When evidence suggests oscillation or repeated ineffective edits, ask for targeted root-cause investigation rather than another broad review. Never create a global retry ceiling; keep the current task-specific stop/authority routes. Store actual time/call costs only when supplied by trusted instrumentation, not invented agent estimates.

**I2 conditional deferral contract:** for *material* accepted deferrals, capture specific safeguards, bounded rationale, owner/follow-up and **observable conditions that should trigger reconsideration**. Example: `validator still rejects incomplete evidence`; `runner remains experimental`; `required workflow version unchanged`. Prefer referencing existing `INV-*`, interface IDs, architecture rules, task or deployment facts. Ordinary low-impact deferrals need no mandatory formal rule. In V1, a coordinator-readable record and a small explicit condition table can suffice; introduce machine-readable fields only where checks will execute them. Keep accepted deferral authority with the human coordinator, not triage or acceptance agents writing the general backlog.

**I3 known-condition checker:** check change events against known deferral predicates and critical guarantee links. Missing mandatory evidence or a declared hard contract is already a direct gate/route, not material for an agent to re-decide. Same-guarantee concentration is **warning**, not causal proof. A hazardous conjunction yields a deterministic *deferral block* only with a versioned policy and verified inputs. Invalidated prior assumptions cause **reassessment** rather than retroactively overwriting the original task's verdict. Unknown relationships and unsupported checks must remain explicit. A checker does not dictate which of several possible safeguards to repair.

**I4 reasoning only when warranted:** replay a representative small backlog and compare local-only vs enriched context, measuring decision changes (bad deferral found, merged root causes, avoided unnecessary fix, correct prioritization), alert noise, model/tool cost and manual record burden. Call a read-only portfolio adviser only after meaningful deterministic triggers or an explicit user decision. No persistent agent, fault-tree program, unbounded cross-issue graph or repeat reviewer chain by default.

**Important overlap:** I3 guarantees metadata can later support R1/R4 evidence targeting, and R4's actual failed system probes become I1 issue occurrences. These are links **by reference**, not a new global requirements or verdict source.

### 6.4 E1 → E3 — Evidence transport, snapshot portability and archival

**E1 — local external storage:** keep `run_evidence.py` producer CLI/semantics and best-effort-vs-required contract. Establish stable project/repository/worktree/run identities and a local external storage boundary. Prototype external Git-object capture using a temporary index/alternates; qualify unchanged HEAD/index/worktree and Git-metadata writes, tracked/untracked snapshots, absent worktree/permissions, restart/recovery, and objects available only in the original repository. Record snapshot state `local / portable / unavailable`. Export the old `.git` manifests and retained refs into a new format preserving hashes and provenance; test representative historical run replay, and do **not** mutate historical logs to fit a new story.

**E2 — cross-environment local ingestion:** host-side collector with durable queue, idempotent submissions and retry/recovery. Terminal/TUI agents call the producer; Docker `sbx` submits over explicitly allowed host networking, without mounting storage or distributing S3 credentials; desktop or external tools emit only what their launchers can actually capture. One open `active.json` per worktree must not become a global concurrency rule; do not claim concurrent safe writes to the **same worktree**. One lifecycle owner per run; no duplicate actor/controller begin/finish. Keep observables separate from task-state transitions.

**E3 — remote archive:** choose S3 or a compatible R2 adapter only after local collection is useful and retention, cost, deletion, privacy, and upload-scope policy are settled. Immutable event/artifact objects plus a reconstructable local query index are preferable to constantly rewriting one global status JSON. Export full source snapshots only by explicit policy; S3 manifest presence does not make Git trees portable. Add data minimization and stdout/stderr redaction/size limits before any cloud upload. DuckDB/SQLite may later support analysis, but not a general dashboard platform by default.

Evidence references can join **issue observations** and **verification outcomes** through stable IDs, but a collector cannot award `ACCEPT`, infer unobserved process compliance, or turn a skipped check into proof. Snapshot externalization should not silently weaken Git provenance or expand access to code/private data.

### 6.5 O1, R6, R7 and R9 — Parallel bounded work

**O1:** Existing code-guided-orchestration spike already owns typed outcome/coverage/finding references, versioned stages and correction/invalidation, independently captured Git/command/session facts, retained runnable installation bundles, interruption recovery, and authorized dependency release. Use stable R/I/E interfaces; design can proceed in parallel, but do not make executor delivery prerequisite to the first system-verification pilot.

**R6:** After accepted flow contracts stabilize, a separately authorized maintainability reviewer may cover introduced/worsened test/eval/harness code changes with proper byte-bound independence. Then consolidate duplicated synthetic scenario construction and misplaced cross-skill tests in bounded chunks. Do not collapse independent discovery and acceptance evidence, create a universal fixture framework, or count file length as a blocker.

**R7:** Preserve decomposition P0. F0 fixes ambiguous no-split terms and records *why this partition*; F1 adds adversarial evals where the model must choose a boundary. F2/F4 compare qualitative end-to-end coordination cost and cross-child contract churn. Adopt F3 “planned-only” children only if the cheap downstream freshness check actually fails; adjust thresholds in F5 only after real observations.

**R9:** When a particular guarantee justifies it, use stateful/property-based testing, controlled fault injection or targeted mutation sensitivity to prove retry/stale/side-effect/isolation failures at the decisive boundary. Do not create a technique quota or mandatory full brownfield survey.

## 7. Outcome measures and automation levels

| Capability | Smallest useful measure | False-confidence trap to avoid |
| --- | --- | --- |
| System verification | Material integration gaps discovered; first-runnable composed journeys independently executed | Test counts and passing task checks masquerading as system proof |
| Issue history | Report occurrences with reliable provenance; repeat failures found and correlated | One issue count without time, source, recurrence, or root-cause distinction |
| Deferral monitoring | Known invalidated/uncertain assumptions surfaced and authoritatively reconsidered | Treating “no alert” as safety, or inferred links as verified |
| Review convergence | Repeat corrective cycles, recurring probes, actual time/model cost when captured | Automatically counting any repeated label as failure or imposing arbitrary limits |
| Evidence collection | Cross-repo capture without `.git` write rights, trusted identity, replayable local snapshots | JSON upload taken as full Git snapshot portability |
| Agent/test automation | Independently observed correct decisions, exact tests/probes, measured maintenance costs | Presence of skill wording/test scaffolds substituted for live behavior |

**Maturity path:** A0 human-coordinated honest evidence → A1 repeatable targeted/first-runnable integration checks → A2 independent final-system closure → A3 code-admitted retained evidence and status transitions → A4 selective continuous verification optimized from observed results. The **I/E foundations can advance in parallel**, but don't confuse the existence of a collector with a guarantee being proven.

## 8. Dependencies and integration points

```text
                  CURRENT COMMITTED SCOPE (no imported features)
T-002 done (user report) → T-003 → T-004 → T-005
                             │                 │
                             └── R6 optional    └── R1 read-only system pilot
                                 reviewer patch        │
                                                       ▼
                                                  R2 planning allocation
                                                       │
                                                       ▼
                                                R3 targeted proof
                                                       │
                                                       ▼
                                                R4 composed closure

INDEPENDENT DATA/ISSUE LANE:  I1 report/recurrence index → I2 deferral validity
                                      │                       │
                                      └───────────────────────┴→ I3 declared checks
                                                                  │
                                                                  ▼
                                                        I4 optional advisory pilot

EVIDENCE LANE:              E1 external local evidence → E2 host ingestion
                                                           → E3 optional cloud

LATER CONTROLLER:           O1 versioned executor consumes stable R / I / E
                           contracts, without replacing their authority.
```

The arrows are dependency preferences, **not** permission to edit current source contracts concurrently. I1 can begin as an offline replay of existing review reports before T-005; E1 can be prototyped in a disposable repository. Production integration of I/E touches shared skill, script or installer contracts and should be separately sequenced to avoid collisions with T-003–T-005. R1 need not wait for the collector. R3/R4 need not wait for S3 or the executor.

There are **four distinct integrity authorities** to avoid duplicate maintenance: approved plan/brief (intended behavior), review/evidence artifacts (observed findings and independent decisions), accepted-deferral record and chosen backlog tracker (residual risk and issue state), and trusted collector/controller (observed facts and transition admission). Reuse stable IDs across these, not a universal writer.

## 9. Explicit deferrals and anti-scope-creep

- No new mandatory stages, issue engine, evidence backend or changed test scope in approved T-003–T-005.
- No requirement to invoke an agent on every reported issue or every unchanged condition; objective contract/evidence checks are deterministic.
- No rewriting approved plans to mark them accepted from inside an independent reviewer; approval is a current review verdict bound to exact artifact identity.
- No complete global issue graph, fixed risk-score formula, fault-tree program or status duplication with GitHub Issues.
- No automatic conclusion that multiple issues on one invariant share a cause or all need repair.
- No per-run secret capture or complete source snapshot uploads by default; no credentials handed to sandboxed agents for cloud storage.
- No storage of all conversations or transcripts to manufacture “observability”; preserve bounded factual provenance and separate limitations.
- No global correction-round limit; no infinite repeated model reviews either—use history and targeted probes to improve diagnosis.
- No mandatory whole-project master strategy, heavyweight project survey, universal property/mutation checks, all-green dashboard or exhaustive scenario registry.
- No schema-valid agent outcome treated as self-proving truth, no duplicate acceptance authority for an issue checker or evidence service.
- No automatic implementation of F3 planned-only child states or broad suite cleanup while skill/report/packaging semantics change.

## 10. Immediate handoff and next design decisions

**In the active work:** Continue T-003 under its existing brief/verification/preflight route, preserving the already-landed implementer test-maintenance guardrail and normal independent review/coordinator authority. Do not expand T-005. Check installed source consistency at the normal boundary rather than refreshing an active agent's skill copies.

**Parallel, non-invasive pilots that will inform the next actual plan:**

1. **R1 proof-allocation pilot:** On one approved multi-task plan and one genuine extension, use `testing-discipline` to identify only material missing/weak real-boundary system proof, unowned composition, early fixture/environment prerequisites or expensive duplicate higher-level evidence. Return a gap/delta matrix and marginal value/overhead comparison; no plan/source mutation.
2. **I1/I2 issue-history pilot:** Read a small sequence of accepted numbered discovery/acceptance reports and correction handoffs plus `ART-008` records, if present. Produce a temporary *occurrence → candidate issue ID → correction attempt → observed status* table. Test one known safeguard invalidation and distinguish verified change from unknown. No new tracker/schema/agent role just to generate the pilot.
3. **E1 external-evidence spike:** In disposable Git fixtures, reproduce and qualify the externally stored Git-tree experiment and demonstrate old `.git` JSON/ref extraction with truthful local-versus-portable status. Scope down before touching distributed installer/runtime sources.

These three experiments **need not wait for each other**, but their actual implementation plans should align common project/task/run/attempt/verification IDs and explicit ownership. If only one pilot gets attention first, **R1 has the strongest direct connection to the user's top-level goal**. If correction loops are already consuming significant effort, I1/I2 may produce the fastest operational improvement.

**Decision to validate before code:** The note “review skills should mark existing plan docs accepted” is not supported as a direct change by the inspected plan-verification/preflight contracts. Capture an exact failing invocation and consumer condition before authorizing a fix. Prefer reading the independent review's `ACCEPT` plus current artifact digests; add a coordinator-owned derived status only if necessary.

**Definition of done for this roadmap:** An implementation planner can select the next bounded objective without (a) expanding current tasks, (b) duplicating existing skill ownership, (c) confusing issue reporting with accepted deferrals, (d) conflating real evidence with captured agent claims, or (e) presuming a sophisticated new agent is required for deterministic safeguards.

---

## Source index

**Inspected repository authorities:**
- [`docs/project-plan.md`](https://github.com/trusovn/personal-skills/blob/t-o-new-flow/docs/project-plan.md), [`docs/task-map.json`](https://github.com/trusovn/personal-skills/blob/t-o-new-flow/docs/task-map.json), [`docs/project-plan-review.md`](https://github.com/trusovn/personal-skills/blob/t-o-new-flow/docs/project-plan-review.md), [`docs/tasks/index.json`](https://github.com/trusovn/personal-skills/blob/t-o-new-flow/docs/tasks/index.json), `docs/tasks/T-002.4/results.md`.
- `skills/project-delivery-plan/SKILL.md`, `skills/project-plan-verification/SKILL.md`, `skills/testing-discipline/SKILL.md`, `skills/task-implementation-flow/README.md`, `skills/task-implementation-flow/task-verification-designer/SKILL.md`, `skills/task-implementation-flow/bounded-task-implementer/SKILL.md`, `skills/task-implementation-flow/task-maintainability-review/SKILL.md`.
- `skills/task-implementation-flow/docs/verification-and-review-policy-plan-2026-10-08.md`, `skills/task-implementation-flow/docs/task-decomposition-follow-up-2026-10-09.md`.
- `skills/task-orchestrator/docs/code-guided-orchestration.brief.md` and `skills/task-orchestrator/docs/integration-spike-2026-10-08/{issues.md,integration-guidance.md}`.

**Uploaded documents reconciled:**
`task-planning-coordination-guidance(1).md`; `t-o-new-flow-plan-amendment-handoff(1).md`; `system-verification-workflow-implementation-plan(1).md`; `issue_triage_portfolio_invariants_discussion_summary(1).md`; `deferred-work-after-t-o-new-flow(1).md`; `urgent-test-suite-guardrail-after-T-002.4(1).md`; `test-suite-maintainability-integration-proposal(1).md`; added user notes on issue triage, recurrence and acceptance status; pasted `Run Evidence Upgrade` note (`Вставлений текст markdown.md`).

**Evidence limits:** This is documentary/contract/source review, **not** an execution of repo tests, agent evals, current `.agents` installation, controller lifecycle or external system integration. The attached proposals and new pasted notes contain observations or reported experiments from earlier revisions; specific test sizes, runner performance and fixture debt are not re-benchmarked here. No repository files were modified by this roadmap.
