# Personal Skills — Consolidated Roadmap for System-Level Verification and Automation

**Prepared:** 2026-10-10  
**Status:** Proposed roadmap and reconciliation; **not** a modification of an accepted plan, approved task scope, or implementation authority.  
**Repository inspected:** [`trusovn/personal-skills`](https://github.com/trusovn/personal-skills), branch `t-o-new-flow`, GitHub HEAD [`520476b1377eedab97c7730f6162dfd8a84b59d3`](https://github.com/trusovn/personal-skills/commit/520476b1377eedab97c7730f6162dfd8a84b59d3) at inspection.  
**Progress baseline:** User reports **T-002 complete**, with T-003 next. The repository's [docs/tasks/index.json](https://github.com/trusovn/personal-skills/blob/0ad1706cecc6f7d115e510762bf74c58d732cb6a/docs/tasks/index.json) showed T-001/T-002 children and did not yet declare T-003 children. [docs/tasks/T-002.4/results.md](https://github.com/trusovn/personal-skills/blob/0ad1706cecc6f7d115e510762bf74c58d732cb6a/docs/tasks/T-002.4/results.md) remains an earlier submission-for-review record; it is historical and does not override the user's more recent completion update.\
**Primary goal:** Improve the actual ability to **plan, exercise, independently judge, and increasingly automate system-level verification**, without making routine development depend on a heavyweight process.

---

## 1. Decision in brief

**Do not merge the future proposals into the current T-001–T-005 plan.** That plan is a deliberately bounded stabilization of the *human-coordinated standalone task flow*, with an accepted independent project-plan review. Let T-003, T-004, and T-005 finish under the authority they already have. The immediate two-file test-maintenance guardrail proposed for after T-002.4 is already present in the live source commit above; do not schedule it again.

**Next substantial investment:** pilot a small **system verification allocation + closure** workflow on a real multi-task example using the existing planning and testing skills. Prove that it detects unowned cross-task behavior, weak real-boundary evidence, unnecessary duplicate tests, or missing testability prerequisites that today's project verification map does not catch. If the pilot delivers actionable improvements, institutionalize the *smallest* reusable contract and workflow.

**Then** connect this planning layer to task-local baseline/regression evidence, milestone integration, and independent final-system closure. Develop orchestration, trustworthy runtime evidence, and central storage as *automation enablers*, not as substitutes for knowing what system behavior must be demonstrated.

The organizing loop should be:

> **Approved system behavior / guarantees → selected real observation boundaries → owned proof obligations → task implementation and targeted regression → composed-flow execution → independent system closure → durable evidence and known gaps.**

**Default:** small/localized work stays light. Larger brownfield discovery, exhaustive schemas, portfolio agents, graph models, and full unattended orchestration are not prerequisites.

## 2. Authority and status rules

Keep four different kinds of documents separate:

1. **Committed current delivery contract:** [[docs/project-plan.md](https://github.com/trusovn/personal-skills/blob/0ad1706cecc6f7d115e510762bf74c58d732cb6a/docs/project-plan.md)](https://github.com/trusovn/personal-skills/blob/0ad1706cecc6f7d115e510762bf74c58d732cb6a/docs/project-plan.md), [[docs/task-map.json](https://github.com/trusovn/personal-skills/blob/0ad1706cecc6f7d115e510762bf74c58d732cb6a/docs/task-map.json)](https://github.com/trusovn/personal-skills/blob/0ad1706cecc6f7d115e510762bf74c58d732cb6a/docs/task-map.json), their **byte-bound** independent [`docs/project-plan-review.md`](https://github.com/trusovn/personal-skills/blob/0ad1706cecc6f7d115e510762bf74c58d732cb6a/docs/project-plan-review.md), and authorized task briefs/reviews. They govern T-001–T-005. The plan header still uses a planning handoff status; the separate review report records an `ACCEPT` for specified bytes. Revalidate if authoritative plan bytes have changed; do not infer perpetual approval from the report filename.
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
| `ART-008` coordinator-owned known-issue deferrals | Later relevant consumers can reassess accepted residual issues | A complete, prioritized project issue backlog |
| T-003 complete correction/conditional-stage handoffs | Findings, failed checks, and unfinished evidence survive repairs | Automatic state transitions or trusted machine admission |
| T-004 installer/drift/refresh checks | The actual profile invoked can be identified and deliberately refreshed | Retained runnable bundle versions and safe mid-run upgrades |
| Section 11 verification map and T-005 qualification | Critical *standalone policy flows* have allocated local and composed behavioral proof | A general reusable system-verification strategy or independent final review for arbitrary projects |

The existing `project-delivery-plan` already specifies flows, interfaces, invariants, task dependencies and a **system verification coverage map**. `project-plan-verification` already rejects plans where task-local success could leave a critical journey unproven. `testing-discipline` already defines risk-based test selection, real-boundary proof, oracle quality, fixtures and maintenance. Avoid duplicating these capabilities in another master testing manual.

**Observed source change since the urgent proposal:** HEAD `520476b` adds test/eval maintenance guidance to root `AGENTS.md` and `bounded-task-implementer/SKILL.md`. This satisfies the proposed *source policy wiring* in the urgent two-file guardrail. It does **not** establish installed-profile freshness, executed checks, agent behavioral compliance, reviewer-side test-only maintainability scope, or fixture-debt reduction. Qualify only what has actually been exercised.

## 4. Document-by-document disposition

| Source | Status for roadmap | Reconciled disposition |
| --- | --- | --- |
| [docs/project-plan.md](https://github.com/trusovn/personal-skills/blob/0ad1706cecc6f7d115e510762bf74c58d732cb6a/docs/project-plan.md) + [docs/task-map.json](https://github.com/trusovn/personal-skills/blob/0ad1706cecc6f7d115e510762bf74c58d732cb6a/docs/task-map.json) | **Current committed baseline** | Complete T-003–T-005 unchanged. Do not retroactively import later ideas into T-005 or mutate reviewed IDs/cases as a convenience. |
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
| Recent run-evidence centralization discussion | **Separate infrastructure candidate** | Address cross-repository storage/access and eventual analysis, but keep *result storage* separate from *test fixture source ownership* and from semantic qualification. Verify actual `.git` collector/export behavior before deciding storage/migration details. |

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

## 6. Dependency-aware delivery roadmap

These are **new roadmap IDs** (`R-*`), deliberately not `T-*`; they do not change [docs/task-map.json](https://github.com/trusovn/personal-skills/blob/0ad1706cecc6f7d115e510762bf74c58d732cb6a/docs/task-map.json). Priority means engineering value and dependency, **not** permission to modify the current plan.

| ID / order | Work package | Primary deliverable | Priority / dependency | Explicit stop or promotion condition |
| --- | --- | --- | --- | --- |
| **R0 — Finish current authority** | T-003 → T-004 → T-005 as already approved | Qualified standalone task flow; honest installed/eval evidence | **P0 / current work** | No extra scope; T-005 records unrun behaviors instead of claiming them |
| **R0a — Confirm prevention patch** | Check `520476b` guardrail and its runtime projection without editing its contract again | Focused source/installation checks and a concise current-version note | **P0 / small**, alongside next authorized preparation | If equivalent checks already recorded, do not rerun merely for paperwork |
| **R1 — System-verification pilot** | Apply `testing-discipline` as a fresh optional allocation pass on a verified multi-task plan + one small extension | Risk→boundary→owner→runnable-point→evidence/gap matrix; comparison to Section 11 baseline | **P0 next**, independent of a full executor | Stop if no material missed gap or duplication reduction and effort exceeds value |
| **R2 — Minimum planning contract** | Implement only R1-proven changes to cross-task evidence allocation and plan review | Conditional verification strategy approach; exact ownership/inputs/reconciliation behavior | **P1**, only if R1 justifies | No duplicate normative specification or mandatory trivial-project document |
| **R3 — Task-boundary evidence** | Implement scoped baseline before edits and targeted real-boundary regression after edits | Relevant current-system references, executed command/output metadata, truthful pending system obligations | **P1**, after R2 semantics or using existing plan map if sufficient | No full repository/whole-suite rerun by default; no claiming sibling composition from local tests |
| **R4 — Composed milestone & final closure** | Give first-runnable cross-task paths an owner and an independent final-system review | Actual composed-flow evidence, bounded correction tasks, final gap/coverage report | **P1**, after enough R2/R3 use to prove interfaces | No `VERIFIED` when a required journey lacks current decisive proof |
| **R5 — Evidence/runner automation** | Minimal code-guided executor and trustworthy shared evidence interfaces | Typed outcomes, pinned flow rules, trusted snapshots, resumable/admitted evidence; optional central store | **P1/P2 enabler**, parallel investigation after R0 | Do not let code executor decide product semantics or silently admit prose verdicts |
| **R6 — Test architecture health** | Scoped reviewer expansion if approved; then bounded fixture/test ownership cleanup | Changed-test architectural judgment; less duplicated setup without weakened regression | **P1/P2**, when flow source stabilizes | No LOC/count quota or blanket “share all fixtures” framework |
| **R7 — Planning decomposition quality** | Small F0 naming/rationale + F1 adversarial evals, then F2/F4 if warranted | Better decomposition decisions, not more child tasks | **P2 / independent small work** | F3 lifecycle and F5 threshold tuning only after demonstrated need/data |
| **R8 — Contextual issue/portfolio pilot** | Replay a sample of real deferred/open issues with vs without broader context | Evidence whether priorities/risks meaningfully change | **P2 / experiment** after stable ART-008 | No default second review agent, auto-refactor or general fault-tree infrastructure |
| **R9 — Advanced test techniques / large brownfield** | Selective state/property/fault/mutation probes; optional survey for big systems | Better proof at demonstrably risky boundaries | **P3 / conditional** | Need real oracle and observed benefit, not technique quotas |

### R0: protect the near-term finishing line

- Treat the user's “T-002 complete” as the current progress report. Confirm normal independent acceptance/continuation and active installed skill versions before starting another packaged task. The T-002.4 results file is an earlier point-in-time submission, **not** evidence either way about later acceptance.
- The committed guardrail in `AGENTS.md` and `bounded-task-implementer` makes **existing tests/fixtures inspection** routine. Check it through already-available focused tests and chosen installation; do not confuse structure checks with behavioral adoption.
- Prepare T-003 just in time through its planned brief/verification/preflight path. Preserve original T-003 ownership: complete stage handoffs, correction, aggregate ownership and maintainability blocker-cap removal. Do **not** add test-only reviewer expansion, portfolio checks, master verification strategy, broad fixture refactoring or machine transitions.
- T-004 remains the distribution/drift/refresh qualification boundary. T-005 is the separate installed-agent flow qualification with real setup and separate calls. Live/model evals are subject to their separate authorization; explicitly recorded unrun claims are gaps, not passing tests.
- `repo-foundation`, `foundation-readiness-review`, `project-bootstrap`, `architecture-guardrails` and `project-plan-verification` do **not** need wholesale reruns merely because the two-file rule changed. Use narrow source/installed checks. Repeat plan verification only when the plan itself materially changes.

### R1: pilot that measures incremental value, not ceremony

Use **two representative contexts**: (a) the existing five-task standalone review policy, and (b) a genuinely small greenfield or extension project whose integration boundaries will become runnable. For each, start with authoritative behavior/flow/invariant IDs and known actual test commands.

Produce **one concise matrix** (working document, not a required schema):

| Meaning | Example record |
| --- | --- |
| Protected behavior/guarantee | `INV-004`: fresh discovery and acceptance are different authorities |
| Where evidence is decisive | Two real independent calls consuming the same current report; not merely a text assertion mentioning two stages |
| Test architecture | Local contract/fixture checks + one composed behavior evaluation for the distinct cross-call failure mode |
| Owner and first runnable point | Current T-005 composition; available when prior stage artifacts and qualified install exist |
| Actual evidence vs intention | Command, result and raw artifact references; explicitly `not_run` if no agent call took place |
| Missing/testability prerequisite | Fresh-session invocation, installed-skill identity, and controlled output permissions |

Challenge the current Section 11 map: does the additional pass uncover a **critical** unowned integration, a mocked decisive boundary, an unreliable oracle, a shared fixture prerequisite or materially redundant E2E allocation? Record only deltas. A merely nicer document is insufficient evidence for another skill or mandatory stage.

**Pilot decision:** (1) no further feature—just improve a few examples in existing planning guidance, or (2) optional `testing-discipline`-backed strategy mode, or (3) a small dedicated `system-verification-strategy` skill for repeated multi-task need. Start with the lightest successful option.

### R2: conditional planning integration (W0–W2 adapted)

Retain owner boundaries:

| Decision/evidence | Owner |
| --- | --- |
| Approved product direction/requirements | User/project authority |
| Cross-task flows, guarantees, interface meanings, task order and integration owner | `project-delivery-plan` |
| Risk-based test boundary/oracle allocation, fixture/environment prerequisites, pending proof | Optional strategy derived from the plan and `testing-discipline` |
| Structural/system verification coherence of reconciled planning package | Independent `project-plan-verification` |
| Task-local semantic scenarios and scenario IDs | `task-verification-designer` |
| Real implemented contracts, commands and source of current behavior | Repository/foundation/contract registry and executable observations |

Keep strategy output small: mapping of critical flow/invariant → real observation boundary → obligation/evidence type → owner → runnable milestone → gap/exception. If stable `SV-*` IDs turn out useful for machine carry-forward, add the **smallest link field** to the task map, not a second separately maintained copy of the requirement. Shared fixture ownership may justify enabling tasks only for a real prerequisite, never by default.

For substantial future multi-task projects, a possible standardized route is:

```text
existing authority + shallow implemented-context orientation
    → draft delivery plan / Section 11
    → conditional derived system-verification allocation
    → targeted reconcile task owners and testability
    → independent verification of the whole reconciled package
    → just-in-time next-task brief and task-local verification
```

A preapproved plan getting a **new** optional strategy result can only be revised by the plan owner and must receive a **fresh review** if its actual commitments change.

### R3: task-by-task baseline and regression (W3)

- At task entry, identify **affected implemented contracts**, existing tests, commands, and known baseline failures. Run a proportionate available **pre-change** check, or record why impossible; the first greenfield slice can have only a build/smoke baseline.
- Task verification specifies falsifiable *local* cases. Implementer inspects existing coverage and chooses reuse/update/new/retire with maintained oracle. Use real integration tests when serialization, persistence, process, filesystem, auth or external service behavior is the decisive property.
- After edits, exercise the changed boundary and nearby contracts. Report exact commands/results, environment and state prerequisites, skipped stronger evidence, and links to any project-level obligation IDs.
- Independent discovery/acceptance judge the **current task** and its relevant existing-context regression; they **do not** give a completed-system verdict when siblings are absent. The composed proof remains assigned to its future milestone owner.
- Do not automatically run complete UI E2E for each task; reserve a few end-to-end paths for genuine wiring and user-journey failures lower levels cannot prove.

### R4: milestone integration and independent final closure (W4)

- The delivery plan or strategy identifies **when** a critical cross-task flow first becomes runnable and **who** must demonstrate it. That event triggers focused integration evidence; a final review later checks its currency and full-system context.
- Final review reconstructs critical journeys from **implemented reality**, approved contracts and actual run evidence. It can discover unplanned risks; `SV-*` coverage is a navigation aid, not an exhaustive universe of correctness.
- A separate independent review context tests applicable composed boundaries and checks false confidence: stale results, weak oracles, omitted required behavior, mocks at the decisive boundary, skipped/manual evidence and interaction failures.
- Corrections or missing tests become separately scoped implementation/test tasks. The fresh reviewer does not write fixes and approve its own changes. Re-review affected final evidence after correction.
- Outcomes should distinguish `VERIFIED`, `VERIFIED_WITH_ACCEPTED_LIMITATIONS` (explicitly authorized, quantified omissions), and `INCOMPLETE/BLOCKED`. The reviewer **cannot self-authorize** a consequential omission merely to obtain closure.

### R5: automate the proven process (orchestrator + evidence)

Do **not** require a finished orchestrator to experiment with system strategy/closure. Once responsibilities and reports are stable, the code-guided controller can automate stage sequencing and evidence admission:

- typed outcome/ledger/finding ownership, separate from human explanations;
- a declarative/versioned flow policy with explicit stage applicability and correction/invalidation routes;
- trusted capture of HEAD/index/worktree, exact file effects, command argv/cwd/env/exit/output, task/run/attempt/session, actual installed workflow identity;
- pinned retained runnable bundles and interruption/recovery rules;
- separation between **agent claims**, **trusted observations**, and **independent judgments**;
- release of dependent task execution only after *actual admitted evidence* and authority;
- lifecycle instrumentation of the selected run mode (best-effort optional vs required), without duplicate actor/controller collectors.

**Evidence centralization is a transport/storage subproject**, not the test architecture and not a new verification verdict. Consider a project-neutral event/evidence envelope plus local spool/export first, then a central location if remote Docker sandboxes, desktop runs and multiple repositories genuinely need access. An object store can suit immutable large artifacts; a lightweight index can support querying. Provider, identity, credential/security boundaries, offline retries, cost and retention must be chosen for actual run environments. Existing `.git` evidence should be **inspected and exported/mapped with provenance**, not rewritten or presumed to match a new schema. Do not start with a complex cloud platform or a duplicate run collector.

### R6–R9: bounded improvements, separately authorized

**R6 test/eval maintainability:** After source and behavioral contracts stabilize, expand independent maintainability review to *introduced/worsened test/eval/harness source regressions* only if separately approved. Test-only corrections need accurate byte provenance and repeat-review invalidation. Preserve role-specific independent discovery/acceptance evidence while extracting truly shared **scenario construction**, not merging stage authorities or silently relying on unavailable sibling-skill imports. Split overly cross-owned deterministic tests by invariant/owner, not line-count thresholds. Check fixture equivalence and meaningful negative scenarios before deleting duplicates.

**R7 decomposition:** F0 fix names such as `unsplittable_override` that now also mean “split is safe but uneconomic” and record why a chosen boundary won. F1 adds adversarial **behavioral** evals where the skill must pick the partition itself. F2/F4 strengthen qualitative total handoff/rework cost and shared contract churn. F3 planned-only child brief lifecycle is a conditional redesign, **not** a quick copy change. F5 adjusts thresholds only after measured outcomes.

**R8 portfolio reasoning:** Replay historical cases with relevant known issues, issue tracker records, changing deferral safeguards and planned refactors. Retain only if contextual review changes important decisions more often than it adds noisy alerts/cost. Portfolio advice cannot make a failing AC pass or create a new acceptance gate.

**R9 advanced techniques:** Apply property/state-model, fault injection or mutation tests to particular high-risk invariants (retries, stale state, auth/isolation, side effects, evidence provenance) when a reliable oracle exists. Larger brownfield pre-survey is an opt-in later development mode.

## 7. Automation maturity ladder and outcome measures

| Level | Meaning | Best first proof |
| --- | --- | --- |
| A0 — Human-directed evidence | Approved flow and owned proof obligations; human invokes stages | Every material system-level guarantee has an owner or explicit known gap |
| A1 — Agent-executable targeted checks | Real pre-change/post-change/first-runnable integration commands | A previously missed cross-boundary regression is caught without a manual interpretation loophole |
| A2 — Independently executable system closure | Final fresh review reconstructs real journeys and reports actual gaps | It rejects a system whose task checks pass but whose composed flow fails |
| A3 — Code-admitted reproducible evidence | Controller validates stage results, freshness, commands, version and authority | Replay/resume demonstrates that stale or invented evidence cannot advance |
| A4 — Efficient continuous verification | Tested impact-based test selection, central evidence querying, repeated release checks | No important drop in detection with lower observed cost/flakiness, not merely fewer tests |

Pilot evaluation should measure **new critical gaps detected before coding**, **unowned composition obligations**, **integration defects caught**, **false claims about what was executed**, **redundant tests/fixtures avoided**, **change locality**, **review/correction churn**, and **total wall-clock/model/tool cost**. Separate structural lint/contract tests from real agent behavior evaluation. Counts of tests, line coverage, document size, or a plausible reviewer summary alone do not establish improved assurance.

## 8. Expected dependencies and concurrency

```text
                  CURRENT COMMITTED TRACK
T-002 accepted (reported) → T-003 → T-004 → T-005
                              │                 │
                              │                 └── R1 optional system-proof pilot
                              │                           │
                     optional R6 reviewer patch          ▼
                     separately authorized          R2 planning allocation
                                                         │
                                                         ▼
                                                  R3 task-boundary proof
                                                         │
                                                         ▼
                                                  R4 system closure
                                                         │
                                                         ▼
                                                  R5 automate repeated proof

Parallel, bounded: R7 decomposition F0/F1; R5 executor *design* and evidence-store
spike; R8 issue-triage experiment (after relevant data exists).
```

The diagram expresses the **preferred path**, not a rigid gate. R1 can run **read-only** on stable approved artifacts before T-005 completes if it does not mutate their scope or consume the same active working files. R5 executor architecture can progress in parallel once its owners and versioned contracts are understood; do not ship an executor that treats unqualified prose as accepted proof.

**Avoid competing edits:** changes to `project-delivery-plan`/verifier, `task-maintainability-review`, shared fixture builders, installer/profile sources, and runtime evidence scripts should each have a named owner and a bounded integration/qualification window. When multiple proposals touch the same source contract, fold their compatible requirements into **one future task brief** rather than having separate agents rewrite it repeatedly.

## 9. Decisions to explicitly defer

- Mandatory `docs/system-verification-strategy.md` for every project; large `SV` schema before a concrete consumer exists.
- A global always-run “master test planner,” “test-maintenance reviewer,” second portfolio assessor, or recursive agent-review system.
- Reopening already accepted T-003/T-005 task scopes just because new strategy ideas are valuable.
- Whole-suite refactoring, common fixture framework, or file-length test policy while discovery/acceptance/installer contracts are still changing.
- Full-system discovery before planning a small project; mandatory dedicated brownfield survey.
- Automatic model-driven test generation as a substitute for independent oracles and real-boundary execution.
- Global coverage quotas, universal property/mutation tests, fault-tree engine, architectural health score or formal issue graph.
- A cloud orchestration/analytics platform before local evidence envelopes, provenance and replay are proven.
- Full machine execution schemas stuffed into the human `verification.md`; mechanical Markdown parsing as a trusted controller protocol.
- Progressively planned child statuses before testing whether a cheap launch-time brief delta check fixes the actual churn.

## 10. First actionable handoff

**Recommended immediate next task:** continue preparing **T-003** from the current approved task-flow plan; use the already landed test-maintenance rules, after confirming proper source/installed skill resolution. Do **not** re-run the urgent two-file patch or expand T-003's ACs. Keep R1 as a separate **read-only pilot brief** using the existing `testing-discipline` and project plan, not as an implementation dependency.

Suggested bounded agent work, when ready for R1:

> Review the current approved delivery plan and its Section 11 system verification map as the baseline. Using `testing-discipline`, identify *only* missing or weak cross-task proof obligations, misleading mocked boundaries, unowned first-runnable integration, shared fixture/testability prerequisites, or material duplicate high-level evidence. Trace each finding to existing `FLOW/IF/INV` authority, state its decisive real boundary, first runnable point and likely owner, and compare against what Section 11 already specifies. Do not modify the reviewed plan, task map, T-003–T-005 cases, or existing skills. Return a compact delta/evidence-allocation matrix and a recommendation: no change, improve existing planning guidance, optional strategy mode, or dedicated strategy skill. Do not treat structural checks as agent behavior proof.

**After R1:** authorize at most one coherent R2 planning change if the value is demonstrated. Let its detailed scope be designed just-in-time against the then-current repository, and independently verify any altered normative project plan. Treat later R3/R4 as staged, independently qualified functionality; do not implement the whole roadmap in one large branch.

---

## Source index

**Inspected repository authorities:**
- [[docs/project-plan.md](https://github.com/trusovn/personal-skills/blob/0ad1706cecc6f7d115e510762bf74c58d732cb6a/docs/project-plan.md)](https://github.com/trusovn/personal-skills/blob/0ad1706cecc6f7d115e510762bf74c58d732cb6a/docs/project-plan.md), [[docs/task-map.json](https://github.com/trusovn/personal-skills/blob/0ad1706cecc6f7d115e510762bf74c58d732cb6a/docs/task-map.json)](https://github.com/trusovn/personal-skills/blob/0ad1706cecc6f7d115e510762bf74c58d732cb6a/docs/task-map.json), [`docs/project-plan-review.md`](https://github.com/trusovn/personal-skills/blob/0ad1706cecc6f7d115e510762bf74c58d732cb6a/docs/project-plan-review.md), [[docs/tasks/index.json](https://github.com/trusovn/personal-skills/blob/0ad1706cecc6f7d115e510762bf74c58d732cb6a/docs/tasks/index.json)](https://github.com/trusovn/personal-skills/blob/0ad1706cecc6f7d115e510762bf74c58d732cb6a/docs/tasks/index.json), [docs/tasks/T-002.4/results.md](https://github.com/trusovn/personal-skills/blob/0ad1706cecc6f7d115e510762bf74c58d732cb6a/docs/tasks/T-002.4/results.md).
- `skills/project-delivery-plan/SKILL.md`, `skills/project-plan-verification/SKILL.md`, `skills/testing-discipline/SKILL.md`, `skills/task-implementation-flow/README.md`, `skills/task-implementation-flow/task-verification-designer/SKILL.md`, `skills/task-implementation-flow/bounded-task-implementer/SKILL.md`, `skills/task-implementation-flow/task-maintainability-review/SKILL.md`.
- `skills/task-implementation-flow/docs/verification-and-review-policy-plan-2026-10-08.md`, `skills/task-implementation-flow/docs/task-decomposition-follow-up-2026-10-09.md`.
- `skills/task-orchestrator/docs/code-guided-orchestration.brief.md` and `skills/task-orchestrator/docs/integration-spike-2026-10-08/{issues.md,integration-guidance.md}`.

**Uploaded documents reconciled:**
`task-planning-coordination-guidance(1).md`; `t-o-new-flow-plan-amendment-handoff(1).md`; `system-verification-workflow-implementation-plan(1).md`; `issue_triage_portfolio_invariants_discussion_summary(1).md`; `deferred-work-after-t-o-new-flow(1).md`; `urgent-test-suite-guardrail-after-T-002.4(1).md`; `test-suite-maintainability-integration-proposal(1).md`.

**Evidence limits:** This is documentary/contract/source review, **not** an execution of repo tests, agent evals, current `.agents` installation, controller lifecycle or external system integration. The attached proposals contain observations from earlier revisions; specific test sizes, runner performance and fixture debt are not re-benchmarked here. No repository files were modified by this roadmap.
