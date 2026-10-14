# Task decomposition — P0 review and remaining improvements

**Date:** 2026-10-09  
**Repository:** `trusovn/personal-skills`  
**Reviewed branch:** `t-o-new-flow`  
**P0 reference commit:** `892a67d767b6a766674a1859d3ad528f02d9f10e` (`[TBD] improved splitting. P0s.`)  
**Status:** Review and follow-up plan. This document does not change implementation policy.

## Goal

Choose implementation-task boundaries that reduce **total delivery effort and rework**, while preserving reliability and adequate independent verification. The target is not the smallest possible task or the fewest calls in a single implementation session.

Optimize the decomposition decision across:

- coherent behavior and single outcome ownership;
- stable consumed/produced interfaces and state;
- independent implementation and meaningful task-local verification;
- repeated edits to shared code/tests and likely contract renegotiation;
- context reset, handoff, review, integration, and correction costs;
- operational risk when one task remains large.

Keep this lightweight and qualitative. Do not introduce an automatic scorer, new orchestration phase, or large planning schema without evidence.

## P0 verdict

**Directionally correct; not yet behaviorally established.**

The P0 commit changes the sizing trigger from an automatic split rule into a mandatory **boundary-quality decision**. It adds explicit checks for ownership, stable handoffs, independent verification, shared change surfaces, contract churn, and net coordination/rework benefit. A triggered task may stay whole even when splitting is technically possible, provided the policy permits an override and the reason and residual risk are recorded. Explicit hard authority limits remain binding.

This is the intended conceptual behavior. Retain it rather than replacing the skill or adding another planner.

### Implemented in P0

| Source | Confirmed change |
| --- | --- |
| `task-brief-designer/SKILL.md` | Boundary-quality check; no automatic split; reasoned keep-whole outcome |
| `references/task-brief-template.md` | No-split explanation in executable task sizing |
| `references/task-sizing.yaml` | Clarifies triggers versus required decomposition, preserving numeric thresholds |
| `task-implementation-flow/README.md` | Documents boundary-aware decision |
| `evals/evals.json` | Revises existing decomposition expectations (cases 9 and 11) |
| `tests/test_package_resources.py` | Adds contract-text assertions for the new rule |

Existing composite parent / executable child structure, recursive sizing, single owner per cross-child artifact, integration-closure child, plan-ID preservation, and separation of plan versus task artifacts are retained.

### Evidence limitation

This review inspected the pushed commit, current branch policy/template, and the evaluation definitions. **The Python test suite and live model skill evaluations were not executed here.** The added Python test asserts the presence of required policy language; it does **not** prove the skill selects good boundaries in practice. Evals 9 and 11 still describe the intended split in their fixtures, so they do not strongly discriminate between intelligent boundary choice and following a supplied partition.

## Remaining work

### F0 — Small P0 follow-ups: correct misleading contract language and make split decisions auditable

**F0.1 — Disambiguate the no-split outcome.**

The current names `unsplittable_override`, `override_cannot_split_safely`, and `decomposition_override: cannot_split_safely` now include cases where a split is *safe but uneconomical*. This is a semantic mismatch.

- Prefer a truthfully named no-split reason/category, distinguishing **atomic/unsafe-to-split** from **coordination-cost-dominates** where a consumer needs that distinction.
- First inspect known consumers of the current metadata and sizing keys; preserve compatibility or deliberately version/migrate the contract. Do not rename an externally consumed key blindly.
- Maintain the hard-limit rule. A cost-based no-split decision must not silently waive explicit hard budgets or a required independently verifiable boundary.
- For a large retained task, identify its residual execution risk and the smallest checkpoint/escalation approach; do not pretend the sizing trigger disappeared.

**F0.2 — Record *why this split* as well as *why no split*.**

The parent template currently documents child ownership/coverage but lacks a compact, explicit rationale for preferring one partition over another.

- Add a short boundary-decision statement to a decomposed parent: chosen boundary, main reason it is stable, and the material rejected alternative or coupling risk if relevant.
- Keep it to a few lines for routine work, not a numeric score or separate report.
- The executable no-split path already records its rationale; avoid duplicating the same information in a new artifact.

**Completion:** split and keep-whole outcomes both have truthful, reviewable rationales, without breaking downstream consumers or increasing guided-task ceremony.

### F1 — High priority: adversarial decomposition evaluations

Add a small set of behavior-focused fixtures to `task-brief-designer/evals`. The agent should have to **choose** the boundary; the prompt/fixture must not preselect the correct child set.

| Case | Decisive expectation |
| --- | --- |
| Oversized but tightly coupled vertical change | Keeps coherent work together with a concrete, policy-permitted no-split reason; does not create artificial layer tasks |
| Two genuine independent outputs with a stable handoff | Splits on the real ownership boundary, maps parent ACs, and names dependent verification |
| Several changes repeatedly touching one shared interface and its tests | Rejects a superficially neat but high-churn partition, or changes the partition to avoid renegotiation |
| Two plausible partitions of one flow | Selects the partition with lower expected cross-child changes and integration effort, explaining the tradeoff |
| Strong/high profile but small coherent task | Treats the profile as a decision trigger, not sufficient evidence that splitting improves delivery |
| Explicit hard limit or unresolved shared contract | Does not misuse an economic override; routes to bounded redesign or the decision owner |

Test the output semantics and artifacts, not just the presence of preferred sentences in `SKILL.md`. Preserve current structural tests and existing evals. A baseline or counterexample response that splits solely on threshold, or keeps work whole with generic preference, should fail the new evaluation.

**Completion:** behavior evaluations discriminate good split, bad split, and justified no-split decisions. Record which evals actually ran; do not equate static assertions with live skill performance.

### F2 — P1: judge whole-task versus split **total cost**, without a numeric optimizer

The existing numeric estimates intentionally cover *implementation-agent work only*. Keep them for execution sizing. Add a **separate qualitative boundary comparison** of the unchanged task versus the strongest plausible split:

- implementation complexity/context load and likelihood of losing local coherence;
- additional brief/preflight/reviewer runs and context reloads;
- shared editing/test surfaces and expected interface churn;
- integration work and probability of repeated corrections;
- whether a child can produce a stable, independently provable result.

Use a short verdict such as `keep whole`, `split at <boundary>`, or `reconsider boundary` with one concrete reason. Do not require exact token-cost estimates, a cost matrix on every brief, or automatic model-tier optimization.

**Completion:** the skill can justify keeping a 50-minute cohesive task whole over two expensive 25-minute handoffs, and splitting a larger task when meaningful independence reduces correction risk.

### F3 — P1: progressive child-brief elaboration (separate design step)

Today a decomposition produces **full executable briefs for all children upfront**. This may freeze speculative local details before predecessor implementation establishes an actual contract.

Investigate a minimal distinction between:

1. **Decomposition structure:** durable parent coverage, child intent/ownership, consumes/produces, dependencies, and integration closure.
2. **Executable brief:** complete task-local scope, acceptance, verification, current contract context, and sizing for the next dependency-ready child.

Allow an unready dependent child to remain *planned but not executable* until its upstream interface/artifact becomes stable. Its future elaboration must preserve approved project-plan IDs and parent coverage. The project plan/task map remain the system-level authority, not a writable progress ledger.

**Do not silently implement this now:** it affects task-index semantics, readiness, status/launch filtering, and the assumption that every child is an executable leaf. First specify compatibility with `docs/tasks/index.json`, `bounded-task-implementer`, preflight, and any orchestrator that consumes child briefs. Consider a smaller alternative: keep full child briefs but require a focused delta check before launching downstream children. Adopt a new child status only if it demonstrates enough value.

**Completion:** downstream tasks do not require speculative contracts or expensive broad replanning; no planned-only child can accidentally launch as executable.

### F4 — P1: cross-child contract stability and edit ownership

Strengthen the decomposition check with a concrete counterfactual:

> If child A makes a reasonable local design choice, will child B need to reopen A's code/tests or negotiate a different public contract?

If yes, either keep the coupled behavior together, establish one owning task and a sufficiently stable handoff, or put necessary integration/contract finalization at an explicit boundary. Repeated edits to one file are not automatically wrong; treat *semantic ownership and expected churn*, not file count, as the deciding factor.

Preserve the existing producer/consumer IDs, current implemented-contract reconciliation, non-overlapping authority, and parent-AC closure.

**Completion:** each shared contract has one change owner; dependency order represents real readiness; neither child assumes another will repair its incomplete local behavior.

### F5 — P2: evidence-based sizing and outcome calibration

After several real tasks, compare retained versus decomposed work using already available execution evidence where possible:

- actual calls/duration and observable token use (if available);
- number of brief/preflight/review/acceptance runs;
- repeated edits/corrections at cross-child surfaces;
- integration failures and review rounds;
- how often a no-split override was justified and whether the retained task finished reliably.

Avoid new compulsory telemetry or invented precision. Use a small retrospective sample and a documented calibration decision before changing the current **15 calls / 40 minutes / strong+high** triggers. Optimise for delivery throughput and correctness, not a lower average task size.

**Completion:** thresholds are retained or modified for a defensible observed reason, not because one arbitrary split looked attractive.

## Suggested execution order

1. **F0.1–F0.2:** tiny contract/template cleanup; check downstream compatibility.
2. **F1:** behavior-focused tests and counterexamples, before more policies are added.
3. **F2 + F4:** minimal qualitative cost and interface-churn decision procedure, informed by eval failures.
4. **F3:** only if actual downstream-task replanning cost justifies a new lifecycle; otherwise use a just-in-time brief delta check.
5. **F5:** retrospective calibration after enough execution data exists.

## Non-goals / guardrails

- No new full planning framework, numerical optimization algorithm, scoring schema, or dedicated splitter skill by default.
- No arbitrary split by files, layers, equal estimated durations, or detached testing phases.
- No silent changes to `docs/project-plan.md` or `docs/task-map.json` by task decomposition.
- No bypass of owner-approved behavior, hard authority limits, independent acceptance, or material verification.
- No requirement to plan every future implementation detail before the next dependency-ready task can begin.
- No claim of measured speed/cost improvement without comparative execution evidence.

## Bottom line

P0 is conceptually aligned with the goal: **sizing triggers a reasoned boundary decision; boundary quality and coordination cost determine whether to split**.

The next highest-value work is **making those decisions observable and falsifiable**, not adding more thresholds. Fix the ambiguous override terminology and split-rationale gap; then test whether the agent actually rejects poor partitions. Implement progressive child planning and threshold calibration only when the smaller changes and real observations justify them.
