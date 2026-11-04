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
