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
