# Description results

## SIDE-003.2 — Boundary groups 1–2

Implemented: `READY_FOR_REVIEW`. Authority: [brief](../SIDE-003.2/brief.md); [verification revision 1](../SIDE-003.2/verification.md); [ready preflight](../SIDE-003.2/preflight.md).

Only the six source description scalars changed. Bodies, names, paths, invocation identities, baseline and active installation remain unchanged. The 150–300-character range is advisory: direction, bootstrap and guardrails remain longer to preserve valid activation routes.

### Wording and retained triggers

#### project-direction

Characters: 573 → 392 (−181).

Old: Create, extract, audit, or rebaseline a plain-language governing direction for a project, product, feature, system, or workflow before or during technical planning. Use when the user wants to decide or clarify the desired experience, ordered priorities, first useful proof, scope, non-goals, trust boundaries, intervention boundaries, or decision ownership; when existing plans are too technical for the owner to govern; or when a mid-project change needs a direction delta. Produce an owner-editable direction, not research, architecture, a PRD, or an implementation plan.

New: Create, extract, audit, or rebaseline owner-editable direction for a project, product, feature, system, or workflow before/during technical planning or mid-project change. Clarify experience, priorities, first proof, scope/non-goals, trust/intervention boundaries and decision ownership; translate plans too technical to govern. Excludes research, architecture, PRDs and implementation plans.

V-01 trigger checklist: Create/extract/audit/rebaseline; project/product/feature/system/workflow; before/during technical planning; mid-project delta; experience, priorities, first proof, scope/non-goals, trust/intervention, decision ownership; plans too technical to govern. Research, architecture, PRD and implementation-plan exclusions remain.

V-02 existing body authority: `skills/project-direction/SKILL.md` — No procedural obligation removed. The expanded meaning of owner-editable direction remains in Boundary, Choose the mode, Workflow and Planning contract.

#### project-bootstrap

Characters: 659 → 311 (−348).

Old: Use at the very beginning of a software project, after a high-level objective and repository/scaffold are available but BEFORE detailed product specification, architecture design, roadmap creation, task decomposition, or implementation. Establish the minimum project charter and engineering-foundation plan another agent needs to work effectively. Produces docs/project-charter.md and docs/foundation-plan.md. When the product or runtime itself includes model-dependent behavior, route through ai-flow-foundation before handing repo-level materialization to repo-foundation; otherwise route directly to repo-foundation. Do not use this skill to plan features.

New: Establish the initial project charter and engineering-foundation plan once an objective and repository/scaffold exist, before specification, architecture, roadmap, task planning or implementation. For product/runtime AI, route via ai-flow-foundation to repo-foundation; otherwise directly. Not feature planning.

V-01 trigger checklist: Initial engineering foundation only; objective plus repository/scaffold required; before specification, architecture, roadmap, task planning and implementation; AI product/runtime routes via ai-flow-foundation to repo-foundation, other projects directly; feature planning excluded.

V-02 existing body authority: `skills/project-bootstrap/SKILL.md` — Output paths docs/project-charter.md and docs/foundation-plan.md remain in Outputs. Protocol 7, Route the foundation handoff, retains AI ordering and agent-maintained deterministic-repository routing.

#### ai-flow-foundation

Characters: 580 → 300 (−280).

Old: Use during pre-planning foundation work when the product or runtime itself will call an AI/LLM/model as part of its data or process flow. Establish testable boundaries, deterministic validation, fake/provider seams, eval/trace locations, retry/idempotency constraints, and safe side-effect boundaries BEFORE detailed prompt/workflow/feature design. Produces docs/ai-foundation.md. Do not use merely because coding agents will develop or maintain the repository; repo-foundation owns agent-legible repository setup. Do not use to optimize prompts or design detailed agent behavior.

New: Establish testable AI boundaries during pre-planning when the product/runtime calls a model in its data/process flow, before prompt, workflow or feature design. Not prompt optimization or detailed agent design; not merely because coding agents will develop or maintain the repo (use repo-foundation).

V-01 trigger checklist: Pre-planning product/runtime model calls in data/process flow; before prompt/workflow/feature design. Prompt optimization and detailed agent design excluded. Coding-agent development/maintenance alone excluded and routed to repo-foundation.

V-02 existing body authority: `skills/ai-flow-foundation/SKILL.md` — Deterministic validation remains in Protocol 3, Establish input/output contracts; provider/fake seams in Protocol 2 and 4; eval and trace locations in Protocol 5 and 6; retry/idempotency and safe side effects in Protocol 7. Output and Protocol 8 retain docs/ai-foundation.md.

#### repo-foundation

Characters: 563 → 300 (−263).

Old: Use this skill when creating, restructuring, or standardizing repository architecture, top-level project layout, module boundaries, repo-local tools, scripts, lint/test/typecheck commands, CI gates, repo-local agent instructions, architecture/project maps, ADRs, module docs, or "where should this live?" decisions. Use it when an implementation needs new top-level folders, modules, tooling, generated-code flows, or durable placement rules. This skill is especially important when future LLM agents will maintain the repo and token-efficient navigation matters.

New: Create, restructure or standardize repository architecture, layout, module boundaries, tools/scripts, lint/test/typecheck commands, CI, agent instructions, maps, ADRs and module docs. Use for new folders/modules/tooling, generated-code flows or placement rules, especially for future LLM maintainers.

V-01 trigger checklist: Create/restructure/standardize repository architecture, layout and module boundaries; tools/scripts, lint/test/typecheck, CI, agent instructions, maps, ADRs and module docs; new folders/modules/tooling, generated flows and placement decisions; future LLM maintenance remains a positive route.

V-02 existing body authority: `skills/repo-foundation/SKILL.md` — No procedural obligation removed. Top-level layout/placement detail remains in Module structure and Where things live; architecture/project map details in Documentation roles; generated-code policy in Dependency, migration, and generated-code policy. Token-efficient navigation is represented by concise maps and agent-facing guidance in Core stance and Quick protocol.

#### architecture-guardrails

Characters: 533 → 341 (−192).

Old: Use when a repository needs new or repaired deterministic architecture/maintainability guardrails: dependency-direction rules, forbidden imports, cycle/boundary checks, a canonical architecture command, legacy no-regression baselines, or a short agent-facing maintainability contract. Usually invoked during repo-foundation materialization or an explicit foundation change. Encode existing or deliberately chosen invariants; do not redesign product architecture or turn heuristic size/complexity metrics into universal hard failures.

New: Create or repair deterministic architecture/maintainability guardrails: dependency/import/cycle/boundary rules, a canonical command, legacy no-regression baselines or an agent contract. Use during repo-foundation or explicit foundation changes for chosen invariants; exclude product redesign and universal heuristic size/complexity failures.

V-01 trigger checklist: New or repaired deterministic architecture/maintainability enforcement; dependency/import/cycle/boundary rules, canonical command, legacy no-regression baselines, agent contract; repo-foundation materialization or explicit foundation change; chosen invariants only; product redesign and universal heuristic size/complexity failures excluded.

V-02 existing body authority: `skills/architecture-guardrails/SKILL.md` — No procedural obligation removed. Existing or deliberately chosen invariants remain in Core contract and Ownership boundary; canonical command in Protocol 5; short agent-facing maintainability contract in Protocol 7; baselines and freshness in Protocol 8. Heuristic policy remains in Protocol 3.

#### foundation-readiness-review

Characters: 445 → 291 (−154).

Old: Use after repo-level foundation changes are materialized and BEFORE detailed product planning or implementation. Independently verify that an unfamiliar agent can navigate, bootstrap, run, test, inspect failures, and follow repo rules from persisted artifacts. Also recommend the cheapest safe next delivery route: PERSONAL_FLOW, SDD_QUICK, SDD_STANDARD, or SDD_FULL. Produces docs/foundation-review.md. Do not review product functionality here.

New: Independently review materialized repo foundations before detailed product planning or implementation: can an unfamiliar agent navigate, bootstrap, run, test, inspect failures and follow persisted rules? Recommend the cheapest safe next delivery route. Excludes product functionality review.

V-01 trigger checklist: Independent review after repo foundation materialization, before detailed product planning/implementation; unfamiliar agent navigation/bootstrap/run/test/failure diagnosis/persisted rules; cheapest safe delivery route; product functionality excluded.

V-02 existing body authority: `skills/foundation-readiness-review/SKILL.md` — Output path docs/foundation-review.md and named PERSONAL_FLOW/SDD_QUICK/SDD_STANDARD/SDD_FULL routes remain in Output; cheapest safe route selection in Protocol 6. No procedure or obligation lost.

### Evidence and limits

| Case | Local evidence and oracle | Outcome |
|---|---|---|
| V-01a–f, each E/P/N/B | Old/new editorial check against all original scopes/actions above and verification revision 1 prompts. Explicit names unchanged; implicit positives retained; stated exclusions and named neighbor distinctions retained. | All 24 cases covered editorially; model selection remains pending. |
| V-02 | Existing body sections cited per skill for omitted output paths, field inventories and procedural detail. | No obligation silently dropped; no body edits. |
| V-03 | Exact Git-original comparison after replacing only each description scalar with one sentinel; changed skill path set equals exactly the six packages. Targeted diff inspected. | PASS; every non-description byte identical. |
| V-04 | `python3 tools/baseline_measure.py`; saved baseline skill rows equal pre-edit rows, including hashes; all26/profile20 character delta equals six deltas; body totals unchanged. | PASS; counts below. |
| V-05 | Existing installer suite and six `quick_validate.py` checks with already available PyYAML; installer constants, profile guide and installation README inspected. | Final suite and validator outcomes below; no consumer synchronization needed. |

Measurements use normalized description characters and UTF-8 body bytes; they do not measure tokens, billing, rendered catalog visibility or observed session savings.

| Catalog | Before characters | After characters | Reduction | Before/after body bytes |
|---|---:|---:|---:|---:|
| All 26 | 14,448 | 13,030 | 1,418 | 388,640 |
| Profile 20 | 10,809 | 9,391 | 1,418 | 320,123 |

Raw measurement JSON: `/tmp/side0032-before.json`, `/tmp/side0032-after.json`. Sum of six reductions: 1,418. Source hashes initially matched all 26 baseline rows.

Installer/profile consumers copy whole selected packages and quote no changed descriptions. The sole owning routing assertion at `tests/test_install_development_skills.py:404` still finds `coding agents will develop or maintain` contiguously in the AI description. No test, installer, guide or README edit was required.

The first installer run failed two tests (`/tmp/side0032-installer.log`): the AI phrase assertion because line wrapping split its exact phrase, and the committed/mixed-line-ending installer check (return 1, no stderr). The phrase wrapping was corrected. The other failure occurred while description files were being rewritten during that run; its exact cause was not independently established. The stable final-tree rerun is reported separately; no assertion was weakened.

Final local outcomes:

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py` — PASS, 36 tests, 27.648 seconds; `/tmp/side0032-installer-final.log`.
- `python3 skills/skill-creator/scripts/quick_validate.py skills/<name>` for all six named packages — PASS; `/tmp/side0032-validate-final.log`. Package structure only, not routing behavior.
- Exact final scope/body and measurement guards — PASS; `/tmp/side0032-guard.log`.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py` — PASS, 4 tests, through installed run-evidence check wrapper; `/tmp/side0032-architecture.log`.
- `python3 tools/check_contracts.py --root .` — PASS, 7 subsystems, 22 indexed plan references; `/tmp/side0032-contracts.log`.
- `git diff --check` — PASS; `/tmp/side0032-diff-check.log`. Final diff contains only six description changes plus this results section and the separate task preparation artifacts.

No new tests/evals/harnesses or dependencies were needed. No installation refresh occurred. Fail-first editorial execution is infeasible; exact preservation plus the complete trigger checklist supply the negative oracles. Live catalog-only routing for all 24 designed cases remains pending separate budget approval. Local tests and editorial evidence do not qualify model routing.

### Submission route

Implemented: `READY_FOR_REVIEW`. The required architecture gate is complete.
Maintainability review and registry update do not apply: no implementation or
contract body changed. First outstanding stage: fresh independent
`task-review-discovery`, then a separate fresh `task-acceptance-review` decision.
The coordinator owns both calls. SIDE-003.18 owns the deferred aggregate
`python3 tools/verify.py` gate. No acceptance verdict is claimed here.

Optional evidence run: `run-20261103T231652Z-5d355a356d07`, using only
`.agents/scripts/` from the active project-local installation.


## SIDE-003.3 — Boundary groups 3–4

Implemented from clean HEAD `2504f1f` on 2026-11-04. Source descriptions only; installed skills were not refreshed. Preparation: [verification revision 1](../SIDE-003.3/verification.md) and [ready guided preflight](../SIDE-003.3/preflight.md).

### Old/new descriptions and trigger checklist

Every skill below covers V-01 E/P/N/B through editorial comparison: explicit invocation identity, implicit positive route, exclusion, and nearest-neighbor distinction. These are editorial results, not observed model selections. The 150–300 character target is advisory; 302–366 characters preserve the routes and consequential exclusions.

#### project-delivery-plan

Old (687 characters):

> Use after the project foundation is ready and before detailed task planning/implementation when a small-to-medium project needs a coherent delivery plan without full SDD. Produce an end-to-end system plan plus a machine-readable task map that makes data/process/state flows, system interfaces, artifacts, invariants, producer/consumer relationships, and task placement explicit. Use this whenever multiple implementation tasks must compose into one working product, especially when downstream agents need to know what each task consumes and produces. Do not use this skill to implement features or to over-specify task-internal design that a strong reasoning agent can determine locally.

New (302 characters; reduction 385):

> Plan a small-to-medium project after foundation readiness and before task planning/implementation when multiple tasks must compose. Produce a lightweight system plan and machine-readable task map with explicit flows and cross-task contracts. Do not implement features or over-specify task-local design.

Preserved checklist: After foundation readiness; before task planning/implementation; small-to-medium lightweight planning; multiple tasks compose; flow/task inputs and outputs remain covered by cross-task contracts. No feature implementation or task-local overspecification.

Removed detail already in `skills/project-delivery-plan/SKILL.md`: Opening, Core stance, Position in the workflow, Required outputs, Planning depth rule, and Protocol 2–9 already hold data/process/state flows, interfaces, artifacts, invariants, producer/consumer closure and task placement. The lightweight route remains distinct from full SDD.

#### project-plan-verification

Old (649 characters):

> Use after `project-delivery-plan` (or an equivalent lightweight project plan) and before task implementation to independently verify that the plan is complete, coherent, and executable as a set of composing tasks. Run this as a fresh/separate reviewer agent. Reconstruct the required end-to-end data/process/state flows from authoritative project inputs, then check scope coverage, artifact producer/consumer closure, interfaces, lifecycle/state semantics, invariants, task placement/dependencies, and verification coverage. Emit a separate review report with ACCEPT, CHANGES_REQUESTED, or INCONCLUSIVE. Do not edit or repair the plan in this skill.

New (307 characters; reduction 342):

> Independently verify a delivery plan or equivalent lightweight plan before implementation, using a fresh reviewer. Check completeness, coherence and executable task composition against authoritative inputs; report ACCEPT, CHANGES_REQUESTED or INCONCLUSIVE. Do not edit/repair the plan or implement features.

Preserved checklist: Delivery plans and equivalent lightweight plans; before implementation; fresh independent reviewer; completeness/coherence/executable composition; three verdicts. No plan editing/repair or feature implementation.

Removed detail already in `skills/project-plan-verification/SKILL.md`: Opening and Independence requirement preserve separate reviewer context; Inputs, Output, Verdicts, and Protocol reconstruct authoritative scope/flows, producer/consumer closure, interfaces, lifecycle semantics, invariants, dependencies and verification coverage. Separate report and exact report path remain in Output.

#### task-brief-designer

Old (571 characters):

> Create, tighten, or gap-check one bounded implementation task from a user request, issue, approved plan, specification, or existing brief. Use when asked to make work implementation-ready, define acceptance criteria and verification, estimate oversized work and split it into bounded child briefs only when coherent boundaries justify the split, prepare an agent handoff, or repair a task contract. Prefer a lightweight delta over rewriting an adequate brief. Do not implement, certify current repository readiness, or invent unresolved product or architecture decisions.

New (331 characters; reduction 240):

> Create, tighten or gap-check a bounded task from a request, issue, approved plan, specification or brief. Use for implementation readiness, acceptance/verification, sizing, justified splitting, handoff or contract repair. Prefer small deltas. Do not implement, certify repository readiness or invent product/architecture decisions.

Preserved checklist: Requests, issues, approved plans, specifications and existing briefs; create/tighten/gap-check; implementation readiness; acceptance and verification; sizing and justified splitting; handoff/repair; small deltas. No implementation, repository readiness certification or invented product/architecture decisions.

Removed detail already in `skills/task-implementation-flow/task-brief-designer/SKILL.md`: Guided inputs preserve lightweight additions to adequate briefs. Workflow 2–6 and Sizing and decomposition contract retain bounded child briefs only at coherent boundaries, acceptance/evidence definition, handoffs and repair. Preparation and permission to start separates contract readiness from execution readiness.

#### task-verification-designer

Old (487 characters):

> Design a compact, implementation-neutral verification specification for one executable task brief before implementation. A supplied executable task package always requires this stage; an unpackaged direct edit uses it when non-obvious acceptance or failure semantics, state/lifecycle behavior, finite material cases, or test-design burden justify it. Produce a separate verification.md in the task folder. Do not write tests or production code, invent requirements, or redesign the task.

New (366 characters; reduction 121):

> Design implementation-neutral verification scenarios/evidence for an executable task brief before implementation. Required for supplied executable packages; use for direct edits with non-obvious acceptance/failure, lifecycle behavior, finite material cases or test-design needs. Write verification.md, not tests/code; do not invent requirements or redesign the task.

Preserved checklist: Implementation-neutral scenario/evidence design before implementation; required for every supplied executable package; direct edits with non-obvious acceptance/failure, lifecycle behavior, finite material cases or test-design needs. verification.md output. No tests/code, invented requirements or redesign.

Removed detail already in `skills/task-implementation-flow/task-verification-designer/SKILL.md`: The description retains unpackaged finite material cases explicitly. When this stage adds value elaborates these triggers and test-design burden. Authority, coverage, and revision plus Workflow enumerate every material scenario; Artifact location and Output contract retain the separate verification.md path. Compactness and exact case/proof procedure remain in the body.

#### task-preflight

Old (453 characters):

> Check whether one bounded task is safe and executable against the current repository, then return a concise ready or blocked result. Use when asked to preflight, readiness-check, resolve task commands or ownership, or prepare a durable execution packet. Require derived verification and compact durable readiness for executable packages; keep direct requests inline and exact freshness for high-assurance work. Do not implement or redesign requirements.

New (326 characters; reduction 127):

> Check current execution readiness of one bounded task. Use for preflight, readiness checks, commands/ownership or execution packets. Require derived verification and durable readiness for packages; keep direct requests inline and high-assurance freshness exact. Return ready/blocked; do not implement or redesign requirements.

Preserved checklist: One bounded task against current state; preflight/readiness, commands/ownership and execution packet routes; derived verification and durable package readiness; inline direct requests and exact high-assurance freshness. Ready/blocked result; no implementation or requirements redesign.

Removed detail already in `skills/task-implementation-flow/task-preflight/SKILL.md`: Choose the profile and Guided/High assurance retain derived verification, canonical durable preflight.md, direct-request inline route and strict freshness. Guided workflow, Decision context and current applicability, and Output contract retain safe execution/readiness facts, ownership and compact results.

### Group distinctions and evidence

Group 3 retains authoring a composing plan vs independently reviewing an existing plan; neither implements features. Group 4 retains defining the task contract vs deriving its verification scenarios vs checking current execution readiness; preflight does not implement. No valid route was intentionally dropped. No removed obligation needed a body edit.

| Case | Evidence | Outcome |
|---|---|---|
| V-01a–e E/P/N/B | Original/full candidate descriptions, boundary checklist above, and prompts in verification revision 1 | All 20 variants covered editorially; live selection pending. |
| V-02 | Exact HEAD byte comparison after masking only description, plus changed-path set | PASS: exactly five changed skill files; all remaining bytes and all other source inventory rows identical. |
| V-03 | Before/after `python3 tools/baseline_measure.py` JSON records | PASS: catalog delta equals sum of five reductions; all bodies unchanged. |
| V-04 | Preparation and flow-guide suites; five package validators; installer/guide consumer inspection | PASS as detailed below; structural/local evidence only. |

| Catalog | Before characters | After characters | Reduction | Before/after body bytes |
|---|---:|---:|---:|---:|
| All 26 | 13,030 | 11,815 | 1,215 | 388,640 |
| Profile 20 | 9,391 | 8,176 | 1,215 | 320,123 |

Before counts include accepted SIDE-003.2 reductions of 1,418 from the frozen 14,448/10,809 totals. Cumulative reduction is now 2,633 characters. The five touched rows matched the saved baseline exactly before edits; the baseline and measurement tool remain unchanged. Raw JSON: `/tmp/side0033-before.json` and `/tmp/side0033-after-final.json`. Counts are normalized description characters and UTF-8 bytes, not tokens, billing, rendered catalog visibility or observed session savings.

Local outcomes:

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_task_preparation_contracts.py` — PASS, 16 tests (`/tmp/side0033-preparation.log`).
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_task_flow_guides.py` — PASS, 14 tests (`/tmp/side0033-guides.log`).
- `python3 skills/skill-creator/scripts/quick_validate.py <package>` — PASS for all five packages using available PyYAML; structural only.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py` — PASS, 4 tests (`/tmp/side0033-architecture.log`).
- `python3 tools/check_contracts.py --root .` — PASS, 7 subsystems, 22 plan references (`/tmp/side0033-contracts.log`).

The preparation suite quotes `implementation-neutral` from verification-designer; the candidate retains it. Other checked wording is present in unchanged bodies. No assertion edit is needed. The canonical installer copies whole packages by stable identity. `DEVELOPMENT_SKILL_SOURCES`, `PROFILE_SKILLS_README`, `SHARED_SCRIPT_FILES`, focused installer tests and README need no synchronization for these scalar-only edits.

No tests/evals/fixtures or dependencies were added. Fail-first is infeasible for editorial compression; byte preservation and the full old/new boundary comparison provide negative oracles. Live fresh-model catalog routing remains pending separate budget approval. SIDE-003.18 owns `python3 tools/verify.py` and distribution qualification. Metadata compression does not qualify model routing.

### Submission route

Implemented: `READY_FOR_REVIEW`. Architecture and contract checks are complete. Maintainability and registry-updater stages are not applicable: no implementation assets, bodies or registered authority changed. First outstanding stage is fresh independent `task-review-discovery`, followed by a separate fresh `task-acceptance-review` decision. Coordinator owns both calls; no acceptance verdict is claimed here. Reports belong in `docs/tasks/SIDE-003.3/reviews/`.

Optional evidence run: `run-20261104T000007Z-6d5d2883801b`, using installed `.agents/scripts/` only.

### F-01 correction plan (recorded before source correction)

Preceding verdict: [CHANGES_REQUESTED](../SIDE-003.3/reviews/acceptance-01.md).
Broken invariant: every original activation route must remain discoverable from
the description. Finite material cases are an independent trigger; body retention
alone is insufficient. Correct only this trigger and its results/counts. Sibling
cases are direct enum/cardinality edits with obvious outputs and no lifecycle
complexity. Preparation revision 1 and ready preflight remain applicable: no
scope, authority, capability or verification scenario changed.

This complete pre-edit map retains every discovery/acceptance ledger identity.
Prior reviewer statuses are historical; corrected bytes need fresh corroboration.
No required row was previously blocked/unchecked. Optional live routing remains
pending approval; the aggregate stays with SIDE-003.18.

| Row | Prior status | Planned evidence or navigation use | Next owner |
|---|---|---|---|
| V-01a-E | pass | Prior pass is navigation only; fresh reviewer compares complete corrected submission | Fresh discovery |
| V-01a-P | pass | Prior pass is navigation only; fresh reviewer compares complete corrected submission | Fresh discovery |
| V-01a-N | pass | Prior pass is navigation only; fresh reviewer compares complete corrected submission | Fresh discovery |
| V-01a-B | pass | Prior pass is navigation only; fresh reviewer compares complete corrected submission | Fresh discovery |
| V-01a-FULL | pass | Prior pass is navigation only; fresh reviewer compares complete corrected submission | Fresh discovery |
| V-01b-E | pass | Prior pass is navigation only; fresh reviewer compares complete corrected submission | Fresh discovery |
| V-01b-P | pass | Prior pass is navigation only; fresh reviewer compares complete corrected submission | Fresh discovery |
| V-01b-N | pass | Prior pass is navigation only; fresh reviewer compares complete corrected submission | Fresh discovery |
| V-01b-B | pass | Prior pass is navigation only; fresh reviewer compares complete corrected submission | Fresh discovery |
| V-01b-FULL | pass | Prior pass is navigation only; fresh reviewer compares complete corrected submission | Fresh discovery |
| V-01c-E | pass | Prior pass is navigation only; fresh reviewer compares complete corrected submission | Fresh discovery |
| V-01c-P | pass | Prior pass is navigation only; fresh reviewer compares complete corrected submission | Fresh discovery |
| V-01c-N | pass | Prior pass is navigation only; fresh reviewer compares complete corrected submission | Fresh discovery |
| V-01c-B | pass | Prior pass is navigation only; fresh reviewer compares complete corrected submission | Fresh discovery |
| V-01c-FULL | pass | Prior pass is navigation only; fresh reviewer compares complete corrected submission | Fresh discovery |
| V-01d-E | pass | Prior pass is navigation only; fresh reviewer compares complete corrected submission | Fresh discovery |
| V-01d-P | pass | Prior pass is navigation only; fresh reviewer compares complete corrected submission | Fresh discovery |
| V-01d-N | pass | Prior pass is navigation only; fresh reviewer compares complete corrected submission | Fresh discovery |
| V-01d-B | pass | Prior pass is navigation only; fresh reviewer compares complete corrected submission | Fresh discovery |
| V-01d-FULL | fail F-01 | Restore explicit finite material cases; repeat enum/cardinality-only editorial regression | Fresh discovery |
| V-01e-E | pass | Prior pass is navigation only; fresh reviewer compares complete corrected submission | Fresh discovery |
| V-01e-P | pass | Prior pass is navigation only; fresh reviewer compares complete corrected submission | Fresh discovery |
| V-01e-N | pass | Prior pass is navigation only; fresh reviewer compares complete corrected submission | Fresh discovery |
| V-01e-B | pass | Prior pass is navigation only; fresh reviewer compares complete corrected submission | Fresh discovery |
| V-01e-FULL | pass | Prior pass is navigation only; fresh reviewer compares complete corrected submission | Fresh discovery |
| V-02 | pass | Repeat exact non-description byte guard | Fresh discovery |
| V-03 | pass | Recompute catalog and synchronize counts | Fresh discovery |
| V-04 | pass | Rerun preparation suite; validate corrected package; unchanged guide evidence remains applicable | Fresh discovery |
| AC-01 | fail F-01 | Explicit finite-case checklist and corrected measurements | Fresh discovery |
| AC-02 | fail F-01 | Full route comparison including finite-case-only siblings | Fresh discovery |
| AC-03 | pass | Byte guard and affected local checks | Fresh discovery |

### F-01 correction evidence and resubmission

The initial scalar omitted finite material cases. The first independent decision
requested changes; it did not accept the initial checklist's preservation claim.
The corrected scalar now explicitly lists `finite material cases` as an alternative
to non-obvious acceptance/failure, lifecycle behavior and test-design needs. The
old/new and measurement tables above describe these final submitted bytes.
The initial measurement remains at `/tmp/side0033-after.json` for review history;
its 1,246-character reduction is superseded by the final 1,215-character reduction.

Reviewer regression: finite-case-only direct edits, including three configuration
modes and enum/cardinality cases with obvious oracles, now have an explicit catalog
trigger. Editorial comparison PASS; no live selector response is claimed.
`test_task_preparation_contracts.py` rerun PASS, 16 tests, no skips
(`/tmp/side0033-preparation-final.log`); corrected package validator PASS. Final
masked-description guard and five-row sum PASS; all body bytes and other 21 skill
rows remain unchanged. Final measurement: `/tmp/side0033-after-final.json`.
Unchanged flow-guide evidence remains applicable. Architecture/contract handoff
checks and diff whitespace guard are repeated before this resubmission. No broader
suite is added: SIDE-003.18 retains aggregate ownership.

Implemented: `READY_FOR_REVIEW`. F-01's local correction evidence does not change
reviewer statuses in the pre-edit ledger. Every row next belongs to fresh discovery,
then a separate fresh acceptance decision. No required row is left unaccounted for;
optional live routing remains unexecuted. Correction evidence run:
`run-20261104T094010Z-5b6239a1f6dc` (installed shared tooling).


## SIDE-003.4 — Boundary groups 5–6

Implemented from clean HEAD `b7b3337` on 2026-11-04. Source descriptions only; installed skills were not refreshed. Preparation: [verification revision 1](../SIDE-003.4/verification.md) and [ready guided preflight](../SIDE-003.4/preflight.md). The 150–300-character target is advisory: 365–413 characters preserve the routes here, and the acceptance scalar keeps the most required trigger content at 483; no activation was narrowed to hit the range. `task-contract-registry-updater` (279) is a recorded deliberate no-op — its wording is already job, positive trigger and consequential exclusions.

### Old/new descriptions and trigger checklist

Every skill below covers V-01 E/P/N/B through editorial comparison: explicit invocation identity, implicit positive route, exclusion, and nearest-neighbor distinction, plus the V-01a–e-FULL clause-by-clause pass. These are editorial results, not observed model selections.

#### bounded-task-implementer

Old (515 characters; reduction 150):

> Implement one bounded task from a clear user request, ready task brief, or high-assurance preflight packet. Use whenever asked to execute, resume, or correct a scoped implementation and the agent should automatically define missing acceptance criteria, add risk-based tests, verify progressively, preserve user work, and report evidence. Default to a lightweight guided flow with a human-readable result; require strict freshness and raw JSON only when an orchestrated packet or machine output contract is supplied.

New (365 characters; corrected after [acceptance-02 F-01](../SIDE-003.4/reviews/acceptance-02.md) — see the F-01 correction plan and correction evidence subsections below):

> Implement, resume, or correct one bounded task from a request, ready task brief, or preflight packet — define missing acceptance criteria, add risk-based tests, verify progressively, preserve user work, report evidence. Guided by default; strict freshness and raw JSON for explicit high-assurance requests or supplied machine contracts; a packet alone stays guided.

The first submitted scalar was 334 characters and made the strict obligations exclusive to "supplied machine contracts"; acceptance-02 F-01 found that exclusive condition dropped the explicit high-assurance request route (AC-02). The corrected scalar names both of the body's high-assurance triggers non-exclusively, and nothing else in it changed. The initial 334-character scalar and its measurement remain at `/tmp/side0034-after.json` for review history; superseded by the F-01 measurement `/tmp/side0034-after-final.json` and then the verdict-literal follow-up measurement below.

Preserved checklist: request, ready task brief and preflight packet inputs; execute/resume/correct; automatically define missing acceptance criteria, add risk-based tests, verify progressively, preserve user work, report evidence; guided default; strict freshness and raw JSON for explicit high-assurance requests or supplied machine contracts — the two-trigger profile clause agreeing with body lines 19–22. V-01a-M passes editorially: the supplied-machine-contract high-assurance route stays visible by naming supplied machine contracts without requiring the high-assurance phrase. V-01a-FULL and V-01a-EXPLICIT-HA pass editorially after the correction: the explicit high-assurance request route is discoverable again, and the strictness clause no longer contradicts the body's user-request trigger. "A packet alone stays guided" keeps the packaged guided route distinct from high-assurance. N: product-wide architecture redesign is not one bounded task — no activation. B: policy-required maintainability review of changed assets routes to `task-maintainability-review`.

Removed detail already in `skills/task-implementation-flow/bounded-task-implementer/SKILL.md`: "Choose the profile" holds the high-assurance triggers (user request; worker-result schema with a durable result path, orchestrator invocation, or another strict freshness/result contract) and the packet-alone-stays-guided rule; "High-assurance additions" holds the fresh high-assurance preflight packet; "Guided inputs" holds the request/brief/package entry routes; "Guided workflow" steps 3 and 5–7 plus the Output contract hold the lightweight guided human-readable flow.

#### task-maintainability-review

Old (640 characters, one folded `>` scalar, shown normalized; reduction 227):

> Use after implementation or correction, before functional task-acceptance-review, when repository policy requires focused maintainability/architecture review or the user explicitly asks for it. Independently review current changed implementation assets, including significant tests, evaluations, fixtures and harness code, plus any required deterministic architecture gate for concrete regressions in semantic clarity, state/rule ownership, cohesion, coupling, change locality, testability, diagnosability, or abstraction cost. Return ACCEPT, CHANGES_REQUESTED, or INCONCLUSIVE. Do not perform full specification/functional acceptance here.

New (413 characters; the folded block became one plain scalar like the other four — a description-scalar-only change):

> Use after implementation or correction, before functional acceptance, when repository policy requires focused maintainability/architecture review or the user explicitly asks for it. Independently review changed implementation assets, including significant tests, evaluations, fixtures and harness code, plus any required deterministic architecture gate. Do not perform full specification or functional acceptance.

Preserved checklist: after implementation or correction and before functional acceptance (ordering); repository-policy OR explicit-user-request trigger; independence; changed implementation assets including significant tests, evaluations, fixtures and harness code; any required deterministic architecture gate; never full specification/functional acceptance. P: policy-required focused review of changed assets including the test harness. N: the full specification/functional acceptance decision is excluded. B: "Implement this bounded task" routes to `bounded-task-implementer`.

Removed detail already in `skills/task-implementation-flow/task-maintainability-review/SKILL.md`: the three verdict definitions remain in the unchanged body (the verdict sections and output contract); the concrete regression dimensions remain enumerated in "Review contract" (cohesion, coupling, explicit dependencies, change locality, testability, proportionate abstraction) and Protocol steps 3 (responsibility and semantic clarity), 5 (change locality and state/rule ownership), 6 (testability and diagnosability) and 7 (abstraction cost); the functional-acceptance stage name remains at "leave full AC/spec conformance to `task-acceptance-review`".

#### task-contract-registry-updater

Deliberate no-op (279 characters; reduction 0) — unchanged:

> Synchronize the machine-readable current-state contract registry and stale discovery references after a bounded implementation has passed structural and maintainability review. Use before task acceptance when work may have added, changed, or removed durable cross-task contracts.

Preserved checklist: current-state synchronization of the machine-readable contract registry and stale discovery references (never planned capability); after structural and maintainability review passed; before task acceptance; when work may have added, changed, or removed durable cross-task contracts. P: registry update after the reviews, before acceptance. N: registering planned capability before implementation — no activation (current state only). B: fresh-session evidence gathering without a verdict routes to `task-review-discovery`.

#### task-review-discovery

Old (494 characters; reduction 120):

> Independently publish current evidence and confirmed findings for one bounded implementation without deciding acceptance. Produces a complete or explicitly partial evidence report with facts, suggested severities, probe results, and a continuation block for a separate acceptance decision call. Use when a fresh session independent of production authorship must gather review evidence, especially when behavior crosses stateful, public, security, concurrency, recovery, or migration boundaries.

New (374 characters):

> From a fresh session independent of production authorship, gather and publish current evidence and confirmed findings for one bounded implementation without deciding acceptance — a complete or explicitly partial report for the separate acceptance decision call. Use especially when behavior crosses stateful, public, security, concurrency, recovery, or migration boundaries.

Preserved checklist: fresh session independent of production authorship; gather and publish current evidence and confirmed findings; without deciding acceptance (the no-verdict exclusion is the core group-6 distinction); complete or explicitly partial report; the separate acceptance decision call; stateful, public, security, concurrency, recovery, migration boundaries. P: fresh-session evidence across public API and recovery boundaries. N: issuing the final verdict — no activation, discovery never decides acceptance. B: deciding safe advancement routes to `task-acceptance-review`.

Removed detail already in `skills/task-implementation-flow/task-review-discovery/SKILL.md`: "Discovery workflow" step 7 holds facts, stable finding IDs and suggested severities; step 9 and "Output contract" hold the complete-or-explicitly-partial publication, the probe results (coverage rows) and the required continuation block for the acceptance decision call.

#### task-acceptance-review

Old (599 characters; reduction 116):

> Decide whether one bounded implementation is safe to advance by admitting the current independent discovery evidence, submission claims, and applicable conditional evidence, then return ACCEPT, CHANGES_REQUESTED, or INCONCLUSIVE. Use after an independent discovery pass published its report, or with equivalent current evidence, especially when task metadata requires immediate review or behavior crosses stateful, public, security, concurrency, recovery, or migration boundaries. Default to a concise guided decision; require full packet/report reconstruction only for explicit high-assurance work.

New (483 characters):

> Decide whether one bounded implementation is safe to advance by admitting current independent discovery evidence, submission claims, and conditional evidence. Use after discovery published its report or with equivalent current evidence, especially for immediate-review metadata or behavior crossing stateful, public, security, concurrency, recovery, or migration boundaries. Concise guided decision by default; full packet/report reconstruction only for explicit high-assurance work.

Preserved checklist: decide safe advancement by admitting current independent discovery evidence, submission claims and conditional evidence (never performing discovery itself); trigger after discovery published its report or with equivalent current evidence; immediate-review metadata; the stateful, public, security, concurrency, recovery, migration boundary list; concise guided decision by default with full packet/report reconstruction only for explicit high-assurance work. P: decide after the discovery report — concise guided decision. N: re-probing and gathering new evidence — no activation; acceptance admits current evidence, new evidence belongs to discovery. B: registry synchronization before the decision routes to `task-contract-registry-updater`.

Removed detail already in `skills/task-implementation-flow/task-acceptance-review/SKILL.md`: the three verdict definitions remain in the unchanged body (the verdict sections and output contract); "Guided inputs" holds "applicable conditional evidence" (maintainability review, registry records, prior review continuations); "Decision workflow" step 3 ("Acceptance neither performs the missing discovery itself"), step 6 ("does not routinely rerun public probes, broad searches, or suites") and "Verdict and routing rules" ("acceptance does not silently do both roles in one call") hold the never-performs-discovery rule that the admission framing implies; "Choose the profile" and "High-assurance inputs" hold the guided/high-assurance split and its packaged inputs.

### Group distinctions and evidence

Group 5 retains authoring scoped implementation (implementer: guided default, explicit-high-assurance and supplied-machine-contract high-assurance routes, a packet alone stays guided) versus independent structural review when policy or the user requires it (maintainability review: changed implementation assets including significant test/eval/fixture/harness code, any required deterministic architecture gate, never functional acceptance). The B-neighbor cycle holds: the implementer's policy-required-review neighbor routes to maintainability review and maintainability review's implementation neighbor routes back to the implementer; architecture-wide redesign and functional acceptance activate neither.

Group 6 retains synchronizing current contracts (registry updater: current state only, after structural and maintainability review, before acceptance) versus independent evidence without a verdict (discovery: fresh session independent of production authorship, complete or explicitly partial, never decides acceptance) versus a separate acceptance decision after discovery (acceptance: admits current independent discovery evidence, submission claims and conditional evidence, returns the verdict, concise guided by default). The cycle holds: the updater's evidence neighbor routes to discovery, discovery's decision neighbor to acceptance, and acceptance's registry neighbor back to the updater; issuing a verdict does not activate discovery, re-probing does not activate acceptance, and planned capability does not activate the updater.

| Case | Evidence | Outcome |
|---|---|---|
| V-01a–e E/P/N/B, V-01a-M, V-01a–e-FULL | Full old/new clause-by-clause comparison above against plan boundary rows 5–6 and verification revision 1 prompts | All 26 variants covered editorially; live selection pending |
| V-02 | Sentinel-mask byte guard vs HEAD `b7b3337` (the whole folded block masked for the maintainability scalar), `git diff --stat`, targeted per-file diff | PASS: masked remainders byte-identical for all five; exactly four changed skill paths (the fifth target is the recorded no-op); description-scalar-only changes |
| V-03 | Before/after `python3 tools/baseline_measure.py` JSON records | PASS: catalog delta equals the sum of the five per-skill reductions; all bodies unchanged |
| V-04 | 13 focused suites plus editorial re-scan of description-quoting assertions | PASS as detailed below; structural/local evidence only. Latest follow-up validated all five packages; the initial submission recorded a PyYAML skip |

| Catalog | Before characters | After characters | Reduction | Before/after body bytes |
|---|---:|---:|---:|---:|
| All 26 | 11,815 | 11,202 | 613 | 388,640 |
| Profile 20 | 8,176 | 7,563 | 613 | 320,123 |

Before counts include the accepted SIDE-003.2 (1,418) and SIDE-003.3 (1,215) reductions; cumulative reduction across .2/.3/.4 is now 3,246 characters from the frozen 14,448/10,809 totals. All five target rows matched the saved baseline exactly before edits, including `file_bytes` and `sha256`; the baseline record and measurement tool remain unchanged. Raw JSON: `/tmp/side0034-before.json`, `/tmp/side0034-after.json` (initial submission, superseded by the F-01 correction) and `/tmp/side0034-after-final.json` (F-01 correction) and `/tmp/side0034-status-removal/after.json` (current verdict-literal follow-up). Counts are normalized description characters and UTF-8 body bytes, not tokens, billing, rendered catalog visibility or observed session savings.

Initial submission local outcomes (historical; current follow-up results below):

- 13 focused suites — all PASS: `test_bounded_task_implementer.py` 17 tests, `test_run_evidence.py` 18, `test_run_evidence_availability.py` 5, `test_maintainability.py` 33 (31 skipped by its pre-existing `HAS_TOOLS` gate — "real Radon and Ruff required"; environment-gated, unrelated to description edits), `test_review_composition.py` 22, `test_task_preparation_contracts.py` 16, `test_task_flow_guides.py` 14, `test_task_maintainability_review.py` 26, `test_task_review_discovery.py` 17, `test_task_acceptance_review.py` 25, `test_contextual_export_risks.py` 6, `test_contextual_known_issues.py` 6, `test_contextual_uncertainty_inputs.py` 5; logs at `/tmp/side0034-test_<pattern>.log`.
- `python3 skills/skill-creator/scripts/quick_validate.py <package>` — SKIPPED for all five packages: PyYAML is not available in this environment (`python3 -c "import yaml"` → ModuleNotFoundError; the pinned `.quality` venv is unusable here). Recorded per AC-03; nothing was installed.
- Sentinel-mask guard and targeted diff — PASS; `/tmp/side0034-guard.log`.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py` — PASS, 4 tests, executed once through the run-evidence check wrapper; `/tmp/side0034-architecture.log`.
- `python3 tools/check_contracts.py --root .` — PASS, 7 subsystems, 22 indexed plan references; `/tmp/side0034-contracts.log`.
- `git diff --check` — PASS; `/tmp/side0034-diff-check.log`.

Editorial assertion re-check before and after edits: no owning assertion quotes changed description text. The only literals that overlap a description — "preflight" (implementer) and "acceptance decision call" (discovery) — remain present in the new scalars and in the unchanged bodies. No assertion sync was needed. No tests, evals, fixtures or dependencies were added. Fail-first is infeasible for editorial compression; the byte guard and the full old/new boundary comparison supply the negative oracles. Live fresh-model catalog routing remains pending separate budget approval; pending cases are not behavioral passes. SIDE-003.18 owns `python3 tools/verify.py` and distribution qualification.

### Submission route

Implemented: `READY_FOR_REVIEW`. The required architecture gate is complete. Maintainability review and registry update do not apply: no implementation assets, bodies or registered contract authority changed (descriptions are not registered contract authority; the brief's expected contract impact is none). First outstanding stage: fresh independent `task-review-discovery`, then a separate fresh `task-acceptance-review` decision. The coordinator owns both calls; reports belong in `docs/tasks/SIDE-003.4/reviews/`. SIDE-003.18 owns the deferred aggregate `python3 tools/verify.py` gate. No acceptance verdict is claimed here.

Optional evidence run: `run-20261104T122300Z-439d693e6bc2`, using only `.agents/scripts/` from the active project-local installation.

### F-01 correction plan (recorded before source correction)

Preceding verdict: [CHANGES_REQUESTED](../SIDE-003.4/reviews/acceptance-02.md) (decision 02; the prior ACCEPT in acceptance-01 is historical). Broken invariant: compression must not narrow a valid profile activation route. The submitted implementer scalar conditions strict freshness and raw JSON exclusively on supplied machine contracts ("only for supplied machine contracts"); the unchanged body (lines 19–22) selects high assurance when the user requests it **or** the caller supplies a machine contract, and the old 515-character scalar kept the explicit-request route visible through its "high-assurance preflight packet" input. The exclusive condition therefore drops the explicit high-assurance activation route from the catalog surface — an AC-02 violation (discovery-02 §2 F-01, confirmed blocking by acceptance-02; ledger rows V-01a-FULL and V-01a-EXPLICIT-HA fail).

Authorized correction scope (acceptance-02 "Next"): rewrite the implementer description scalar — line 3 of `skills/task-implementation-flow/bounded-task-implementer/SKILL.md` only — so its profile conditions agree with the body's complete trigger set: strict freshness and raw JSON for an explicit high-assurance request **or** a supplied machine contract, retaining the packet-alone-stays-guided distinction and the V-01a-M machine-contract visibility; remove the exclusive "only for supplied machine contracts" condition. No body change, no other scalar, no test change; the advisory character range may not narrow the correction. Preparation revision 1 and the ready guided preflight remain applicable: the correction changes no scope, authority, capability, or verification scenario; the decisive rows remain V-01a-M and FULL plus the separate EXPLICIT-HA row. Ownership fact preserved: the working tree contains user-owned staged artifacts (task preparation/review files staged by the user); this correction makes worktree edits only and leaves the index exactly as it is. Planned corrected scalar — exactly 365 characters, computed before the edit with the measurement tool's counting rule:

> Implement, resume, or correct one bounded task from a request, ready task brief, or preflight packet — define missing acceptance criteria, add risk-based tests, verify progressively, preserve user work, report evidence. Guided by default; strict freshness and raw JSON for explicit high-assurance requests or supplied machine contracts; a packet alone stays guided.

Sibling cases implied by the invariant, each rechecked after the edit: (a) explicit high-assurance execute/resume/correct requests without a machine contract — the strict route must stay visible; (b) supplied-machine-contract activation without the high-assurance phrase — V-01a-M visibility must survive; (c) an ordinary ready package alone stays guided.

This complete pre-edit map consumes discovery-02 §3 and acceptance-02's continuation block — every row identity appears exactly once. Prior passes are navigation context only, never acceptance evidence for corrected bytes. The two failing rows map to the correction and its reviewer regressions; every other row maps to fresh discovery-03 next; the two AGG rows keep their external owners and are carried forward as pending, not as evidence.

| Row | Prior status | Planned evidence or navigation use | Next owner |
|---|---|---|---|
| V-01a-E | pass | Navigation only — the correction touches only the strictness clause; E identity/job wording unchanged, rechecked inside the post-edit FULL recheck | Fresh discovery-03 |
| V-01a-P | pass | Navigation only — request/ready task brief/packet inputs and execute/resume/correct wording unchanged | Fresh discovery-03 |
| V-01a-N | pass | Navigation only — product-wide-redesign exclusion and bounded scoping untouched | Fresh discovery-03 |
| V-01a-B | pass | Navigation only — maintainability-neighbor routing untouched | Fresh discovery-03 |
| V-01a-M | pass | Correction must retain machine-contract visibility; planned sibling case (b) recheck — machine contracts named without requiring the high-assurance phrase | Fresh discovery-03 |
| V-01a-FULL | fail F-01 (prior pass not corroborated) | Corrected scalar clause-by-clause recheck against the old 515-character inventory — the explicit high-assurance route becomes discoverable again | Fresh discovery-03 |
| V-01a-EXPLICIT-HA | fail F-01 | Sibling case (a) recheck — strict route visible for explicit high-assurance execute/resume/correct without a machine contract | Fresh discovery-03 |
| V-01b-E | pass | Navigation only — maintainability scalar untouched by this correction; masked byte guard proves its bytes unchanged | Fresh discovery-03 |
| V-01b-P | pass | Navigation only; byte guard | Fresh discovery-03 |
| V-01b-N | pass | Navigation only; byte guard | Fresh discovery-03 |
| V-01b-B | pass | Navigation only; byte guard | Fresh discovery-03 |
| V-01b-FULL | pass | Navigation only; byte guard | Fresh discovery-03 |
| V-01c-E | pass | Navigation only — registry-updater path is the recorded deliberate no-op, byte-identical to HEAD; byte guard | Fresh discovery-03 |
| V-01c-P | pass | Navigation only; byte guard | Fresh discovery-03 |
| V-01c-N | pass | Navigation only; byte guard | Fresh discovery-03 |
| V-01c-B | pass | Navigation only; byte guard | Fresh discovery-03 |
| V-01c-FULL | pass | Navigation only; byte guard | Fresh discovery-03 |
| V-01d-E | pass | Navigation only — discovery scalar untouched; byte guard | Fresh discovery-03 |
| V-01d-P | pass | Navigation only; byte guard | Fresh discovery-03 |
| V-01d-N | pass | Navigation only; byte guard | Fresh discovery-03 |
| V-01d-B | pass | Navigation only; byte guard | Fresh discovery-03 |
| V-01d-FULL | pass | Navigation only; byte guard | Fresh discovery-03 |
| V-01e-E | pass | Navigation only — acceptance scalar untouched (the verdict-literal question is an acceptance-02 observation, outside this correction); byte guard | Fresh discovery-03 |
| V-01e-P | pass | Navigation only; byte guard | Fresh discovery-03 |
| V-01e-N | pass | Navigation only; byte guard | Fresh discovery-03 |
| V-01e-B | pass | Navigation only; byte guard | Fresh discovery-03 |
| V-01e-FULL | pass | Navigation only; byte guard | Fresh discovery-03 |
| V-G5-DIST | pass | Navigation only — authoring vs independent structural review distinction unaffected by the strictness-clause fix; rechecked in the group-distinction reread | Fresh discovery-03 |
| V-G6-DIST | pass | Navigation only — all group-6 scalars unchanged | Fresh discovery-03 |
| V-02 | pass | Rerun sentinel-mask byte guard vs HEAD `b7b3337` for all five sources (whole folded block masked for the maintainability scalar at HEAD); modified tracked path set still exactly {4 changed SKILL.md + description-results.md}; registry-updater remains the recorded no-op | Fresh discovery-03 |
| V-03-BASE | pass | Frozen baseline record and measurement tool remain untouched; before-edit rows still equal the frozen record | Fresh discovery-03 |
| V-03-MEAS | pass | Fresh measurement to `/tmp/side0034-after-final.json`; expected implementer row 515→365 (reduction 150), per-skill reductions 150/185/0/120/65 = 520, all-26 11,295, profile-20 7,656, bodies 388,640/320,123 unchanged, other 21 rows unchanged — tool output is the recorded authority | Fresh discovery-03 |
| V-04-SUITES | pass | Rerun all 13 focused suites (owning implementer suite first); logs at `/tmp/side0034-final-<pattern>.log` | Fresh discovery-03 |
| V-04-LITERALS | pass | Quick literal rescan that no owning assertion quotes changed description text (old-only literals: none expected) | Fresh discovery-03 |
| V-04-VALIDATE | pass | Remains skipped here — PyYAML unavailable in this environment, nothing installed; discovery-02's session (PyYAML available) validated all five pre-correction packages exit 0; the corrected byte's validation belongs to the next session that can run it | Fresh discovery-03 |
| GATE-ARCH | pass | Rerun once through the evidence check wrapper | Fresh discovery-03 |
| GATE-CONTRACT | pass | Rerun `python3 tools/check_contracts.py --root .` | Fresh discovery-03 |
| AGG-VERIFY | not run — owner SIDE-003.18 | Unchanged: this leaf is forbidden by its verification design from running the aggregate; no aggregate claim is made from the correction | SIDE-003.18 (external); carried forward as pending |
| AGG-LIVE | not run — owner SIDE-003.18/coordinator after separately approved budget | Unchanged: must exercise the explicit high-assurance route separately from V-01a-M; pending cases are not behavioral passes | SIDE-003.18/coordinator (external); carried forward as pending |
| AC-01 | constituent rows pass; shared V-01a-FULL failed F-01 — implicated secondarily per acceptance-02 | Corrected scalar restores explicit high-assurance visibility; corrected counts re-recorded | Fresh discovery-03 |
| AC-02 | fail F-01 | Corrected scalar carries both body triggers non-exclusively; sibling cases (a)/(b)/(c) rechecked | Fresh discovery-03 |
| AC-03 | pass | Byte guard, corrected measurement, 13-suite rerun, validate-skip record | Fresh discovery-03 |

### F-01 correction evidence and resubmission

What changed and why: the implementer description's strictness clause no longer conditions strict freshness and raw JSON exclusively on supplied machine contracts. The corrected clause — "strict freshness and raw JSON for explicit high-assurance requests or supplied machine contracts" — names both of the body's high-assurance triggers non-exclusively ("Choose the profile", lines 19–22: the user requests it **or** the caller supplies a machine contract), so the explicit high-assurance activation route that acceptance-02 F-01 found dropped is discoverable in the catalog description again and the description no longer contradicts the body. Nothing else in the scalar changed — the diff against the initial submitted scalar is that one clause — and the packet-alone-stays-guided distinction and V-01a-M machine-contract visibility are retained. No body text, other scalar, test, or tool byte changed; the advisory character range did not narrow the correction.

Sibling-case regression outcomes (editorial; no live routing claimed): (a) explicit high-assurance execute/resume/correct request without a machine contract — the strict route is visible in the description through "for explicit high-assurance requests"; PASS. (b) supplied-machine-contract activation without the high-assurance phrase (V-01a-M) — "supplied machine contracts" remains named as an independent trigger and no "only" remains anywhere in the scalar; PASS. (c) an ordinary ready package alone — "a packet alone stays guided" is retained verbatim and agrees with the body's packet-alone rule; PASS. Full V-01a-FULL clause-by-clause recheck against the old 515-character inventory: request, ready task brief and preflight packet inputs; implement/resume/correct; define missing acceptance criteria; add risk-based tests; verify progressively; preserve user work; report evidence; guided default; strict freshness and raw JSON; both high-assurance triggers; the packet-alone exclusion — every trigger, input and exclusion is discoverable; PASS editorially.

Reviewer regressions after the edit — all PASS: sentinel-mask byte guard vs HEAD `b7b3337` for all five sources (whole folded block masked for the maintainability scalar at HEAD; masked remainders byte-identical; bodies and non-description frontmatter lines unchanged; registry-updater still byte-identical to HEAD), and the modified tracked path set is still exactly the four changed `SKILL.md` files plus this results file (`/tmp/side0034-final-guard.log`). Fresh measurement — implementer 515→365 (reduction 150), per-skill reductions 150/185/0/120/65 = 520, all-26 11,815→11,295, profile-20 8,176→7,656, body bytes 388,640/320,123 unchanged, other 21 rows unchanged (the 11 differing from the frozen record are the accepted SIDE-003.2/.3 reductions); `/tmp/side0034-after-final.json`. All 13 focused suites — 210 tests, no failures (31 pre-existing environment-gated skips in `test_maintainability.py`), owning implementer suite first; logs at `/tmp/side0034-final-<pattern>.log`. Literal re-scan — no owning assertion quotes changed description text; the overlapping "preflight" literal remains present in the corrected scalar (`/tmp/side0034-final-literal-scan.log`). quick_validate — SKIPPED: PyYAML is unavailable in this environment (`python3 -c "import yaml"` → ModuleNotFoundError); nothing was installed; discovery-02's session (where PyYAML was available) validated all five pre-correction packages exit 0, and the corrected byte's validation belongs to the next session that can run it — recorded per AC-03's conditional branch. Architecture gate — 4 tests, exit 0, run once through the run-evidence check wrapper (`/tmp/side0034-final-architecture.log`). Contract check — exit 0, 7 subsystems, 22 indexed plan references (`/tmp/side0034-final-contracts.log`). `git diff --check` and `git diff HEAD --check` — exit 0 (`/tmp/side0034-final-diff-check.log`).

Implemented: `READY_FOR_REVIEW`. The F-01 correction does not change reviewer statuses in the pre-edit ledger. Every ledger row next belongs to fresh independent `task-review-discovery` (discovery-03) and then a separate fresh `task-acceptance-review` decision (acceptance-03) against the corrected bytes; prior verdicts remain historical and neither is reused or appended. Conditional stages remain inapplicable — a metadata-only correction with no registered contract authority and no implementation assets — and the architecture-gate rerun above is implementation evidence, not a review stage. No required row is left unaccounted for; AGG-VERIFY and AGG-LIVE keep their external owners (SIDE-003.18; live-routing budget) and optional live routing remains unexecuted. Correction evidence run: `run-20261104T130939Z-75ba38bbe2c7` (installed shared tooling, `.agents/scripts/`).


### User-requested follow-up — omit verdict literals from descriptions

On 2026-11-04 the user requested removal of the status lists from
`task-maintainability-review` and `task-acceptance-review`. This extends the
prior F-01-only correction scope by explicit user instruction. The implementer
correction was already present at this invocation's start and is unchanged.
Prior reviews and F-01 correction evidence above remain historical.

The two descriptions now describe their jobs and activation boundaries without
`ACCEPT`, `CHANGES_REQUESTED`, or `INCONCLUSIVE`. Those output definitions remain
in the unchanged bodies: maintainability's verdict sections and output contract,
and acceptance's Verdict and routing rules and output contract. Timing,
policy-or-user review triggers, independence, reviewed assets, functional-acceptance
exclusion, discovery/equivalent-evidence inputs, risk boundaries, and the existing
profile wording are unchanged. V-01b/E/P/N/B/FULL and V-01e/E/P/N/B/FULL were
rechecked editorially; removal concerns output mechanics, not routing triggers.
No live model behavior is claimed.

Measurements: maintainability 455→413 (42 fewer); acceptance 534→483 (51 fewer).
This follow-up removes another 93 characters. Current five-skill counts are
365/413/279/374/483, totaling a 613-character reduction from this leaf's original
baseline. Catalog totals are 11,202 (all 26) and 7,563 (profile 20), with body
bytes unchanged at 388,640/320,123. The current descriptions and primary results
table above reflect these values. Measurement records:
`/tmp/side0034-status-removal/before.json` and `after.json`.

Verification: description-line-only comparison against invocation-start copies
passed; both bodies and the existing implementer correction are byte-identical;
no test string literal was lost. All 13 revision-1 focused suites ran successfully:
210 tests, no failures, 31 existing Radon/Ruff-dependent skips. Five package
quick_validate invocations passed (PyYAML is available here). The architecture
check passed (4 tests); the contract check passed (7 subsystems, 22 refs).
The optional evidence check wrapper rejected the argument order before executing
any check; the architecture command then ran directly, once, successfully.
Logs for the other 12 focused suites and five validations are in
`/tmp/side0034-status-removal/`; the first focused suite (maintainability),
architecture and contract output are retained in the tool transcript. No tests,
fixtures, installer files, installed skills, or prior review artifacts changed;
the index was preserved.

Implemented: `READY_FOR_REVIEW`. These are implementation/editorial checks,
not fresh independent acceptance evidence. First outstanding stage: fresh
independent discovery for the current descriptions, then a separate acceptance
decision, with the brief, verification revision 1, ready preflight, prior reports,
F-01 correction and this follow-up supplied as context. Prior ledger statuses
are navigation context only; the two review-skill FULL rows need to confirm that
verdict mechanics remain in the bodies. No registry or maintainability stage
applies to these metadata-only edits. SIDE-003.18 retains `python3 tools/verify.py`
and live-routing qualification; no live-model budget was spent here.
