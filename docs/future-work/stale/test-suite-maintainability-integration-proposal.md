# Test-suite maintainability: responsibility gap and integration proposal

**Date:** 2026-10-10  
**Repository:** [`trusovn/personal-skills`](https://github.com/trusovn/personal-skills)  
**Observed branch:** `t-o-new-flow` (inspected at commit `529c24a4face580fa7fd6c7032e0994a30a251c5`)  
**Status:** Proposal for reconciliation with the ongoing skill/workflow redesign; **not** a new operating policy or an authorized implementation task.

## 1. Problem statement

The implementation flow is accumulating behavioral evals, contract tests, and synthetic fixtures mainly by addition. Some increase is justified: new discovery, evidence-admission, and contextual-decision responsibilities need independent behavioral contrasts. The concern is **uncontrolled growth of the test *implementation***: duplicated scenario setups, increasingly large test modules, broad cross-skill test ownership, and tests that encode the current file/text structure rather than the intended behavior.

This is not a request to minimize test counts or weaken regression protection. The objective is **the smallest maintainable body of trustworthy evidence**, with clear ownership and low-cost incremental changes for coding agents.

### Observed signals (source inspection, not an execution benchmark)

- `task-acceptance-review/evals/files/setup_fixture.py` is approximately 126 KB; the new `task-review-discovery/evals/files/setup_fixture.py` is approximately 56 KB. Both recreate substantially overlapping synthetic workflow states. For example, the `process_cleanup_defects()` fixture implementation was duplicated verbatim across the two reviewed files.
- `tests/test_review_discipline.py` coordinates both reviewer fixtures and enforces text/function adaptations between them. This protects a meaningful relationship but also **locks a copied-fixture structure into regression checks**.
- `task-brief-designer/tests/test_package_resources.py` tests preflight, implementation entry, verification resources, and other cross-skill contracts in addition to brief-designer behavior. That centralizes edits in an unrelated skill's test module.
- Several checks assert exact wording in skills, README files, and eval definitions. Such checks can be legitimate for deliberately stable textual contracts, but they **do not establish agent behavior** and can make safe instruction refactoring costly.
- Large tests existed before this branch as well (for example, `task-orchestrator/tests/test_controller.py`), so the problem predates the current discovery/acceptance redesign.

**Evidence limit:** These are architectural observations from pushed source and branch comparison. No claim is made here about passing/failing model evals, actual runtime, fixture flakiness, or agent token savings. Recheck HEAD and local unpushed changes before implementing.

## 2. Why it happened: a gap between existing owners

The repository already has unusually explicit test-maintenance advice in [`skills/testing-discipline/SKILL.md`](https://github.com/trusovn/personal-skills/blob/t-o-new-flow/skills/testing-discipline/SKILL.md): preserve behavioral detection power; avoid duplicate evidence; prefer small legible fixtures; replace obsolete or redundant tests only after identifying remaining coverage; and review unnecessary harness complexity. **The missing piece is application of those rules within the standard task flow.**

Contributing mechanisms:

1. **Routing gap.** `skills/README.md` presents `testing-discipline` as an on-demand skill, not a reliably consumed source of policy for significant test or eval changes. `bounded-task-implementer` has a compact testing workflow but does not explicitly require maintaining *existing* coverage and fixture architecture before adding more.
2. **Review-scope gap.** `task-maintainability-review` is oriented toward *production bytes* and production architecture. Changed tests and eval harnesses are not explicitly reviewed as maintainable implementation assets, even when they are the main substance of the change.
3. **Repository contract gap.** `repo-foundation` supports testing placement, commands, and agent-facing conventions, but this repository does not state a concrete ownership rule for shared behavioral fixtures and cross-skill contract tests in its root `AGENTS.md` or a dedicated testing architecture guide.
4. **Locally rational additive behavior.** New acceptance/evidence obligations encourage new test cases. Appending a test is usually easier and safer for a bounded agent than reasoning about whether the existing test should change or disappear. Structural tests that expect a particular duplicate layout then make later extraction expensive.

A passing test suite demonstrates only that its current assertions pass. It does not mean the suite has clear ownership, nonredundant scenarios, appropriate oracles, or a sustainable extension path.

## 3. Intended responsibility map

**Do not create a new mandatory test-maintenance stage or another agent role.** Reconcile this concern with existing skill boundaries:

| Owner / stage | Appropriate responsibility | Do **not** make it own |
| --- | --- | --- |
| `repo-foundation` and repo-local instructions | Establish test/eval placement, shared fixture ownership, canonical commands, where architecture policy lives, and the narrow guidance agents need to find it | Every feature's test cases and oracles |
| `testing-discipline` | **Canonical reusable test-quality guidance:** evidence sufficiency, reuse/replacement, fixture design, duplication, flakiness, and test maintenance | Automatic extra invocation for every trivial code edit; an independent workflow verdict |
| `task-brief-designer` | Identify material cross-skill/test-infrastructure effects as scope and ownership constraints when known; avoid hiding them in a feature task | Detailed test-file layout or fixture class design |
| `task-verification-designer` | Specify semantic obligations, scenario IDs, oracles, and independent failure contrasts; keep coverage at the *behavior* level | Prescribing one test function/file per scenario, or constraining helper structure |
| `task-preflight` | Confirm relevant fixtures, tools, permissions and executable observation boundaries are feasible, including existing evidence when relevant | Broad test-suite architecture assessment |
| `bounded-task-implementer` | **Primary prevention owner:** inspect closest existing coverage before test edits; add/update/reuse/replace as appropriate; preserve each required oracle; keep helper changes local and proportionate | Revising normative requirements or silently deleting reviewer regressions |
| `task-maintainability-review` | **Independent detection owner:** inspect introduced/worsened maintainability problems in changed production **and test/eval/harness** bytes, when this review is applicable | Rerunning the functional eval catalog or deciding task-spec conformance |
| `task-review-discovery` | Independently verify current behavior, decisive boundaries, coverage ledger, and reliability of claimed evidence | Reviewing test-file architecture as a routine separate gate |
| `task-acceptance-review` | Admit discovery and applicable maintainability results; decide functional acceptance and findings | Duplicate test-maintainability review |
| `skill-creator` | During **skill/eval authoring**, keep scenarios discriminating and fixtures reusable; separate stable contract-text checks from behavior-eval outcomes | Making the behavioral eval runner itself depend on another skill's invocation |
| `architecture-guardrails` | Optional repo-native, low-false-positive hard checks plus advisory growth/duplication signals | Hard failures based solely on file length or line counts |
| `senior-code-review` | Optional holistic branch/PR review for systemic concerns when requested | A mandatory per-task gate added to the standard flow |

The authority chain should be simple: **repo-local architecture/placement rules** + **canonical `testing-discipline` principles** → implementer applies them → maintainability reviewer judges material regression → functional discovery and acceptance retain their existing, separate jobs.

## 4. Minimal policy delta to integrate into the redesign

### 4.1 Implementer: maintain coverage rather than only add coverage

Before **material** changes to tests/evals, inspect nearby existing tests and fixtures. Make a compact internal decision for each changed behavior:

- **Preserve** a still-valid test and oracle.
- **Update/extend** its owning test when the contract changes or a material variant uses the same invariant and oracle.
- **Add** a test when it distinguishes an independent failure mode or observation boundary not adequately protected elsewhere.
- **Remove or supersede** obsolete/overlapping tests only after identifying the remaining proof and preserving important regression sensitivity.
- **Reuse or extract** setup only when there is a concrete repeated construction or shared ownership boundary. Do not invent a generic fixture framework for one case.

Maintain the mapping from verification scenario IDs/ACs to evidence, but do **not** enforce a one-to-one relationship between scenario IDs and Python test functions. Distinguish deleted *test implementations* from deleted *normative scenario obligations*: changes to the latter require the established verification-revision and readiness route.

Integrate the rule into `bounded-task-implementer`'s existing local-discovery and pre-edit/verification steps; do not add a mandatory standalone document or subagent invocation. For a substantial test-infrastructure change, instruct the acting agent to apply the relevant sections of `testing-discipline` from the **same installed skill root**. Keep ordinary guided edits lightweight.

### 4.2 Maintainability review: include changed tests as code

Extend `task-maintainability-review`'s scope/provenance wording from changed production bytes to **changed implementation assets**, with test/eval/harness code explicitly included. Focus on new or materially worsened conditions:

- duplicated source-of-truth setup, scenario construction, or mutable shared state;
- cross-skill test ownership that forces unrelated future edits;
- test modules mixing independent reasons to change;
- unnecessary coupling to literal skill wording, incidental file structure, or harness internals;
- excessive new generic infrastructure relative to the concrete cases;
- material runtime/flake/debuggability regression supported by evidence.

Use file size, duplication counts, and other static indicators only as **investigation triggers**, not automatic blockers. Keep existing materiality thresholds, independence, finite findings, and no-regression behavior. Avoid rechecking whether each AC passed: functional evidence still belongs to discovery/acceptance.

**Review identity matters:** if changed test/eval assets are now in scope for maintainability, the review and correction invalidation language must bind to the **actual reviewed bytes**. A tests-only correction may invalidate the previous maintainability finding/evidence and applicable functional proof even if production source is untouched. Coordinate this with the ongoing provenance and stage-routing redesign; do not create inconsistent exceptions or an extra verdict.

### 4.3 Repo foundation: one narrow local test-architecture rule

Document an owner map for this repository, anchored from `AGENTS.md` (or a short test-architecture reference if it cannot remain concise):

- tests for one skill generally live with that skill;
- cross-skill integration/flow contracts have a deliberately shared owner;
- common fixture **scenario facts** have one authoritative definition, with separate role-specific evidence, permissions, and expectations;
- runtime eval packaging must remain independently executable in the relevant sandbox/installed skill context;
- no global source-of-truth duplication disguised as "independent" behavioral evaluation.

Let `repo-foundation` generate equivalent **project-specific** placement/ownership guidance when relevant in future repositories; do not hard-code this particular directory layout into the generic skill.

### 4.4 Skill creator: reduce eval-catalog inertia

When modifying existing skills/evals, require a light "new distinction versus existing coverage" check. Preserve contrasting decision scenarios that catch different errors. Where several evals need the same synthetic project, prefer one independently testable fixture definition with parameterized variants or generation, not copy-pasted repositories.

Do not conflate:

- **deterministic contract/fixture tests** (syntax, paths, schema, staging, setup correctness);
- **agent behavioral evals** (actual decisions, artifacts, permissions, routing);
- **cross-skill flow integration** (produced/consumed evidence across stages).

Text-presence assertions are appropriate only for stable textual contracts, not substitutes for observing agent behavior. Preserve the current `skill-creator` eval-running protocol and its prohibition on invoking another testing skill during that runner procedure; any additional authoring policy should be integrated without breaking that boundary.

## 5. Structural follow-up for existing test debt (separate from policy integration)

Once ownership is agreed and the moving flow contracts settle, perform a **bounded test-harness consolidation**, not a sweeping redesign:

1. Inventory the existing deterministic tests, behavioral eval cases, setup entry points, runtime packaging constraints, and their invariants. Record a basic *scenario → oracle → fixture owner → execution command* map; make this a short-lived migration aid, not another permanent registry unless it proves necessary.
2. Extract common scenario *construction* from acceptance/discovery fixtures into one owned source. Retain role-specific setup adapters that inject the discovery or acceptance artifacts, permissions, and evidence needed for each eval. Prefer the simplest packaging arrangement that works when skills/evals execute independently; avoid an implicit import from a sibling skill absent from the installed bundle.
3. Split cross-skill deterministic contract tests out of `task-brief-designer/tests/test_package_resources.py` and decompose `tests/test_review_discipline.py` along **ownership/invariant** boundaries, not arbitrary maximum file lengths. Preserve public test commands and discovery unless an explicit migration updates them.
4. Replace assertions that mandate copy-pasted fixture internals with assertions of **equivalent relevant starting state and distinct stage obligations**. Preserve the exact semantic contrasts (including negative, blocked, stale, repeated, and corrected-state cases).
5. Only retire/merge actual test/eval cases after a written coverage equivalence argument and, where feasible, a deliberately wrong or mutated case showing the remaining oracle still detects the defect. Historical run evidence remains historical; don't rewrite it to pretend a removed test never existed.

**Do not begin with a new shared test framework.** A few small builders and adapters may suffice; the appropriate implementation architecture should be chosen from actual fixture packaging and variation points.

## 6. Reconciliation with the active redesign

The branch is concurrently redefining verification design, preflight ownership, discovery versus acceptance, correction loops, known issues, and orchestrator handoffs. Therefore **integrate at stable responsibility boundaries, not by simultaneously editing every active skill**.

| Redesign area | Constraint for this proposal |
| --- | --- |
| Required `verification.md` and preflight | Keep scenario coverage/IDs and revision/freshness semantics; changing test functions or fixture layout must not automatically trigger a new design revision. Changing the semantic scenario contract does. |
| Discovery/acceptance split | Preserve separate agents, evidence provenance, and verdict ownership. Share synthetic starting-state construction, **not** review authority, report content, or decisions. |
| Correction/re-review loop | Keep reviewer regressions and coverage ledger rows. Implementer may consolidate tests without losing row evidence; a correction to reviewed tests/evals must receive the proper new evidence/review against current bytes. |
| Conditional maintainability stage | Broaden the existing stage's subject when it runs. Consider **significant test-harness/eval architecture change** an explicit trigger by repo policy/risk; do not impose it on every assertion change. |
| Contract registry / task orchestrator | Preserve existing artifact and state-ownership boundaries. The proposed test policy must not make the registry updater own fixtures or add a new orchestrator state/verdict. |
| Distribution / installed skills | Keep installation manifests, source references, and relevant eval assets coherent. Shared fixture code must be resolvable inside packaged/sandboxed eval runs. |
| Decomposition improvements | Recognize shared test-file edit surfaces and fixture ownership when considering task boundaries; avoid splitting a tightly coupled fixture refactor into overlapping "write tests" children. |
| Run-evidence centralization | This concerns evaluation *results*, not synthetic scenario source ownership. Keep results transport/storage migration independent of test fixture consolidation. |

### Recommended integration order

**Phase 0 — Reconcile, don't refactor (now).**

- Name the canonical test-quality owner (`testing-discipline`) and the apply/review owners (implementer / maintainability reviewer).
- Record this proposal as a delta against the current verification/review and decomposition plans; resolve any conflicting wording in those plans **before** new skill instructions are finalized.
- Inventory the current installed/root instruction routing to ensure agents can find the relevant local skill from the correct installation root.

**Phase 1 — Small contract integration (alongside flow finalization).**

- Add the compact existing-test decision to `bounded-task-implementer`.
- Extend `task-maintainability-review` to reviewed test/eval code and align independence/freshness/correction language.
- Add one repo-local test ownership/fixture reuse rule and update flow/skills routing references only where necessary.
- Update `skill-creator` only with the narrow eval-maintenance rule, respecting its eval-runner boundary.

**Phase 2 — Prove the *new policy* (before cleanup).**

Exercise discriminating examples where an agent must (a) modify an existing test instead of appending a redundant one, (b) preserve two necessary boundary-specific tests, (c) reject unnecessary fixture duplication, (d) avoid speculative helper abstraction, and (e) review a tests-only architectural regression. Include a clean small change that should not trigger extra ceremony. Check skill loading, output permissions, and review independence. Do not count mere policy-string assertions as behavioral qualification.

**Phase 3 — Consolidate the current test debt (after stable flow contracts).**

Tackle the acceptance/discovery fixtures and cross-skill contract-test modules in focused slices. Run deterministic fixture equivalence, affected behavioral evals, and selected cross-stage integration checks. Keep unrelated active implementation work out of the cleanup diff.

**Phase 4 — Calibrate rather than regulate by size.**

Observe fixture-edit locality, repeated modified files across tasks, eval setup time, test runtime, flaky failures, and agent context/tool cost where actually measurable. Treat metrics as feedback to revise the local rule, **not** as fixed global thresholds.

## 7. Acceptance criteria for the policy change

The proposal can be considered integrated when:

1. The existing `testing-discipline` is the discoverable canonical source for test maintenance; no copied multi-page policy appears in several task skills.
2. A normal implementer faced with a changed requirement explicitly considers existing tests and can reuse/update/retire them while retaining required behavior evidence.
3. The maintainability review can identify a material regression introduced **only** in changed test or eval infrastructure, without performing functional acceptance or issuing false blockers for file size alone.
4. Scenario/AC evidence mapping and reviewer regression provenance survive test consolidation; no one-to-one scenario-to-function assumption is imposed.
5. Both discovery and acceptance stay independently executable and separately authoritative after any shared fixture extraction.
6. A small routine change remains lightweight; no universal additional agent stage or harness framework has been introduced.
7. Source skill routing, installer/distribution references, repo-local guidance, and representative behavior evals agree with the redesigned workflow.

The subsequent **suite-cleanup task** has a different completion criterion: preserve meaningful behavior and historical evidence while reducing duplicated construction and cross-owner edits. Do not report policy integration itself as successful cleanup.

## 8. Non-goals and cautions

- No blanket deletion target, test-count cap, LOC hard limit, or mandatory suite rewrite.
- No demand to collapse independent discovery and acceptance scenarios into one test or one agent.
- No test implementation architecture embedded in `task-verification-designer` or detailed fixture planning forced into every task brief.
- No global "always call testing-discipline" instruction for trivial edits, and no new mandatory test-maintenance agent/stage.
- No assumption that all current growth is wasteful: some contrasting behavioral evals are essential to the redesigned flow.
- No broad refactoring while source responsibilities, scenario contracts, and installation packaging are still changing.

## 9. Authoritative sources to reconcile while implementing

- [`skills/testing-discipline/SKILL.md`](https://github.com/trusovn/personal-skills/blob/t-o-new-flow/skills/testing-discipline/SKILL.md) — existing test-maintenance principles.
- [`skills/repo-foundation/SKILL.md`](https://github.com/trusovn/personal-skills/blob/t-o-new-flow/skills/repo-foundation/SKILL.md) and [`AGENTS.md`](https://github.com/trusovn/personal-skills/blob/t-o-new-flow/AGENTS.md) — placement, repo-local rules and command discovery.
- [`skills/task-implementation-flow/bounded-task-implementer/SKILL.md`](https://github.com/trusovn/personal-skills/blob/t-o-new-flow/skills/task-implementation-flow/bounded-task-implementer/SKILL.md) — test-edit decisions and evidence handoff.
- [`skills/task-implementation-flow/task-maintainability-review/SKILL.md`](https://github.com/trusovn/personal-skills/blob/t-o-new-flow/skills/task-implementation-flow/task-maintainability-review/SKILL.md) — independent maintainability judgment and scope.
- [`skills/task-implementation-flow/task-verification-designer/SKILL.md`](https://github.com/trusovn/personal-skills/blob/t-o-new-flow/skills/task-implementation-flow/task-verification-designer/SKILL.md) — normative semantic scenario coverage.
- [`skills/skill-creator/SKILL.md`](https://github.com/trusovn/personal-skills/blob/t-o-new-flow/skills/skill-creator/SKILL.md) — skill eval authoring/running.
- [`skills/task-implementation-flow/docs/verification-and-review-policy-plan-2026-10-08.md`](https://github.com/trusovn/personal-skills/blob/t-o-new-flow/skills/task-implementation-flow/docs/verification-and-review-policy-plan-2026-10-08.md) — evolving stage/decision design.
- [`skills/task-implementation-flow/docs/task-decomposition-follow-up-2026-10-09.md`](https://github.com/trusovn/personal-skills/blob/t-o-new-flow/skills/task-implementation-flow/docs/task-decomposition-follow-up-2026-10-09.md) — shared edit/test surfaces and split economics.
- [`skills/README.md`](https://github.com/trusovn/personal-skills/blob/t-o-new-flow/skills/README.md) and [`scripts/install_development_skills.py`](https://github.com/trusovn/personal-skills/blob/t-o-new-flow/scripts/install_development_skills.py) — standard route and installed skill availability.

---

**Decision requested:** Adopt the **existing-skill responsibility integration** above, then schedule fixture consolidation as a distinct bounded refactor after the current policy contracts are stable. Avoid solving the problem by adding more mandatory planning/review stages.
