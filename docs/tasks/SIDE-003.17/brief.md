# Task Brief: SIDE-003.17 — Conditional loading for flow, idea, and runtime skills

## Outcome

idea-brief, senior-code-review, task-review-discovery, task-verification-designer,
and task-orchestrator load only what their flows need. Every
workflow-participating reference — including task-verification-designer's
cross-package link into task-brief-designer's references — has an explicit
when-to-read condition and timing in its `SKILL.md`; genuinely conditional
sections are extracted into references where safely separable, or the
per-skill decision is a justified no-op recorded with reason; a reference
established as background or unused gains no new mandatory read. Behavior is
unchanged; per-skill instruction maps and measured deltas are recorded in
this leaf's section of `docs/tasks/SIDE-003/rollout-results.md`.

## Authority and scope

| Item | Contract |
|---|---|
| Authority | [SIDE-003 plan](../SIDE-003/plan.md), "Body design and mandatory loading" (conditional extraction, no invented profiles, near-universal material stays inline, missing-reference rule), "Delivery sequence" phase 4, "Measurement and decision rules" layer 2; owner instruction (2026-11-03): clear when-to-read instructions are the acceptance center, and safe extraction is allowed rather than deferred; [parent brief](../SIDE-003/brief.md) |
| Dependencies | SIDE-003.1–.6 complete (baseline, route inventories, and these skills' descriptions final) |
| Allowed changes | The five packages' `SKILL.md` bodies, their `references/` (new and existing), their `evals/` inputs, owning test expectations that assert their text, and this leaf's section in `rollout-results.md` |
| Read-only context | The SIDE-003.1 read graph and route inventories; idea-brief: `vision-template.md`; senior-code-review: `review-dimensions.md` (already the mandatory-read pattern — verify, do not rewrite); task-review-discovery: `discovery-report-template.md`; task-verification-designer: the cross-package layout reference (`task-brief-designer/references/task-artifact-layout.md` — owned by SIDE-003.9, keep the path stable); task-orchestrator: `index.md`, `operator-guide.md`, `architecture-map.md`; `tests/test_senior_review_discipline.py`, `tests/test_task_review_discovery.py`, `tests/review_fixture_support.py`, the task-orchestrator tests root; `docs/contracts/task-orchestrator.json` |
| Out of scope | The `description` frontmatter (compressed in SIDE-003.3–.6 — do not change); any behavior change; deleting or renaming existing references; task-orchestrator's scripts and runtime orchestration state (only its `SKILL.md` body and `references/` are in scope); other skills' references (in particular task-brief-designer's — SIDE-003.9 owns them); the active `.agents/` installation; introducing mandatory reads for resources established as background or unused |
| Assumptions / unresolved | Whether task-orchestrator's three references already carry adequate start-with/initialize/inspect conditions (discover; verify rather than assume); each reference's existing purpose is established before any condition or extraction decision |

## Work and acceptance criteria

Required work:

1. Per skill, freeze a proportionate obligation inventory (scope rules, gates,
   output requirements, stop rules) with current authority locations,
   recorded in the rollout-results section.
2. Enumerate every owned or consumed reference and establish its existing
   purpose first (`SKILL.md` mentions, tests, evals, package history). Add
   explicit read conditions and timing only for references that participate
   in a workflow — for task-verification-designer, the condition governs when
   to follow the cross-package layout reference; record the disposition of
   background or unused resources instead of adding reads.
3. Where genuinely conditional sections exist, extract them into
   `references/` files with explicit conditions and timing (safe
   extraction); otherwise record a justified no-op. Keep near-universal
   material inline; do not invent profiles.
4. State the missing-reference rule where references exist after this work:
   a required reference that is missing or unreadable stops the affected
   action with the exact gap reported; no inferred bypass. Do not read every
   reference at startup.
5. Update owning assertions: behavior-preservation assertions pass unchanged
   before and after the edit; new loading-structure assertions (condition
   presence, reference existence, relocated obligations) reject the pre-edit
   layout. Keep the cross-suite assertions resolving.
6. Record per reference: condition and timing, verified-or-clarified status;
   per skill: extraction or no-op decision with reason, instruction map for
   any moved obligation, and the measured delta (entry-only and route sums,
   before/after, from the SIDE-003.1 baseline record's file table and route
   inventories).

- **AC-01:** Every workflow-participating reference of the five skills has
  an explicit when-to-read condition and timing reachable from its
  `SKILL.md`; dispositions are recorded for background or unused resources;
  no read is introduced merely because a file exists.
- **AC-02:** No behavior change; for any extraction, the instruction map
  covers every moved obligation, behavior-preservation assertions pass
  unchanged before and after the edit, and new loading-structure assertions
  reject the pre-edit layout; senior-code-review's mandatory-read semantics
  are preserved; task-orchestrator's declared scripts and tests and its
  module_docs paths (`references/architecture-map.md`,
  `references/operator-guide.md`) keep their meaning and paths; owning
  suites pass.
- **AC-03:** This leaf's `rollout-results.md` section records per-reference
  results, per-skill extraction/no-op decisions with reasons, instruction
  maps for moved obligations, and measured deltas; the description frontmatter
  and the cross-package reference path are unchanged.

## Verification

| Evidence | Scenario and oracle | Command |
|---|---|---|
| Fail-first | New loading-structure assertions (condition presence; reference existence where added or moved) reject the pre-edit layout; behavior-preservation assertions pass unchanged before and after; where references were added or moved, removing one required link or bypassing one route in a disposable candidate is detected by the relevant check | derived verification owns the concrete fixture/command pair |
| Targeted | Per-reference condition matches actual applicability (the reviewer probes one condition per skill against its workflow); measured deltas reproduce from the SIDE-003.1 record | read of the five `SKILL.md` files plus the SIDE-003.1 record |
| Owning suite | Assertions quoting changed lines, from the SIDE-003.1 prerequisites map (senior-review, discovery, and orchestrator suites) | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p test_controller_state.py` |
| Broader gate | Aggregate gate at SIDE-003.18 (profile members resolve in the disposable installer installation; idea-brief and task-orchestrator validate through disposable package copies); live behavioral qualification only with separately approved budget, else recorded pending | SIDE-003.18 |

## Execution

Status: `ready`; task kind: `executable`; guided profile.
Readiness route: standalone guided preflight after derived verification —
confirm the current read graph, route inventories, and description-phase
state of the five files.
Verification-design recommendation: separate — obligation-preservation
coverage applies wherever extraction happens; the derived verification also
owns the per-reference applicability probes and the background/unused
disposition checks.

```yaml
agent_tier: standard
reasoning: high
review: immediate
budget: 16 tool calls / 45 minutes / five packages, conditions, possible extraction, results section
```

Sizing: `default@1`; estimate 14 implementation calls / 42 minutes;
confidence medium; triggered `max_duration_minutes`.
Decomposition override: `cannot_split_safely` — candidate boundary
(per-skill leaves, or task-orchestrator alone) rejected: the five skills
share one results section, one measurement basis, and one review route;
per-skill micro-leaves of 2–4 calls would multiply preparation and review
stages beyond the work itself. Residual risk: scope discovery on
task-orchestrator; mitigated by the proportionate obligation inventory and
the immediate fresh review.

Stops: a reference whose purpose or correct condition cannot be established
without a policy decision (stop and report); an obligation that cannot be
preserved by extraction (stop; do not delete it to shrink bytes); runtime
orchestration state or scripts (never touch); behavior changes (never);
profile drift in the active installation (report, do not fix).

Next action: derive `verification.md`, obtain a ready `preflight.md` through
standalone guided preflight, then implement.
Required follow-on: immediately after implementation or correction and any
applicable conditional stages, hand the completed bytes to a fresh independent
`task-review-discovery` call, and hand its report to a separate
`task-acceptance-review` decision.

Expected contract impact: none expected — `task-orchestrator.json`
declarations cite scripts and tests, and its module_docs paths are unchanged;
no registry record declares the other four packages. Record any exception in
this leaf's results and route it to SIDE-003.18's registry check.