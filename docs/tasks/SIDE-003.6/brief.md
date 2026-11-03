# Task Brief: SIDE-003.6 — Compress descriptions: boundary groups 9–10

## Outcome

The six remaining source-skill descriptions in plan boundary groups 9–10 —
idea-brief, idea-investigator, idea-challenger, ask-user-questions,
skill-creator, task-orchestrator — are shortened to the job, positive trigger,
and consequential exclusions, with old/new wording, preserved trigger
boundaries, and catalog measurements recorded in this leaf's section of
`docs/tasks/SIDE-003/description-results.md`. Bodies are unchanged in this
phase. This leaf completes description coverage for all 26 source packages.

## Authority and scope

| Item | Contract |
|---|---|
| Authority | [SIDE-003 plan](../SIDE-003/plan.md), "Description design" (targets, boundary-group table rows for groups 9–10, exclusions, "Start with the 20 profile skills, then the six remaining"), "Delivery sequence" phase 2; [parent brief](../SIDE-003/brief.md); [SIDE-003.1 baseline](../SIDE-003/baseline.md) |
| Dependencies | SIDE-003.1–.5 complete (profile descriptions first, per plan) |
| Allowed changes | The `description` frontmatter field of the six named `SKILL.md` files; this leaf's section in `description-results.md`; owning assertions that quote the changed description text (if any) |
| Read-only context | The six skills' bodies and references; the six skills' `evals/` inputs (trigger-case reuse); `docs/contracts/task-orchestrator.json` (declares scripts/tests, not the description; module_docs cite its references, which do not change) |
| Out of scope | Body text of any kind (frontmatter `description` only); names, folder paths, invocation identities; other skills |
| Assumptions / unresolved | Which owning surfaces assert these description strings (discover from the SIDE-003.1 prerequisites map); these six are outside the 20-skill development profile — the installed catalog differs from source, so results are recorded as source-description reduction |

## Work and acceptance criteria

Required work:

1. For each skill, derive a trigger checklist from its current description
   and its group's distinction. Group 9: stabilize early ideas vs research
   viability/validation vs proportional premise challenge — avoid making
   every small edit a research task. Group 10: needed clarification vs skill
   authoring/evaluation vs explicitly requested orchestration only —
   generic task execution must not activate the orchestrator.
2. Draft and apply a compressed description (~150–300 characters where
   sufficient — an editorial starting point that cannot override accurate
   routing), retaining the job, positive trigger, and consequential
   exclusions.
3. Append this leaf's section to `description-results.md`: per skill old/new
   wording, character counts, preserved boundaries, and the catalog
   measurement delta from re-running the SIDE-003.1 command (all-26 and
   profile-20 totals; the profile-20 total is unchanged by this leaf).

- **AC-01:** Each of the six descriptions retains its job, positive trigger,
  and consequential exclusions; old/new wording and preserved boundaries are
  recorded; before/after catalog measurements are recorded.
- **AC-02:** No valid current use case or activation route is dropped to
  reach a length — in particular the orchestrator remains
  explicitly-requested-only and the idea skills' proportionality boundary
  survives; each group's nearest-neighbor distinction survives; procedural
  detail removed from a description is either already present in that skill's
  body or is kept in place and flagged in the results section — never
  silently dropped.
- **AC-03:** Only the six `description` values change: `git diff` shows
  description-line-only changes under `skills/`; names/paths/identities are
  unchanged; description-quoting assertions are synced or verified absent;
  `quick_validate.py` runs for the touched packages if the optional PyYAML
  environment is available, otherwise the skip is recorded.

## Verification

| Evidence | Scenario and oracle | Command |
|---|---|---|
| Fail-first | Infeasible for editorial compression; the decisive negative oracle is the body-unchanged guard plus the per-skill boundary checklist | `git diff --stat` + targeted `git diff` per file |
| Targeted | Per-skill trigger checklist against the plan's boundary-group row; catalog measurement re-run records the expected reduction | SIDE-003.1 measurement command |
| Owning suite | Assertions quoting changed text, from the SIDE-003.1 prerequisites map; task-orchestrator's own suite for its package | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p test_controller_state.py` |
| Broader gate | Aggregate gate at SIDE-003.18; fresh-model routing evals only with separately approved budget, else reported pending | SIDE-003.18 |

## Execution

Status: `ready`; task kind: `executable`; guided profile.
Readiness route: standalone guided preflight after derived verification —
confirm SIDE-003.1's record is current, SIDE-003.2–.5 results sections exist,
and description-quoting assertions are known before edits.
Verification-design recommendation: separate — the decisive evidence is the
per-skill trigger-boundary case set; the approval-gated routing-eval inputs
should be designed now.

```yaml
agent_tier: standard
reasoning: medium
review: immediate
budget: 15 tool calls / 40 minutes / six description edits, results section, measurements
```

Sizing: `default@1`; estimate 13 implementation calls / 38 minutes;
confidence medium; fits.

Stops: do not narrow activation to hit the character range; do not touch
bodies; do not run concurrently with another active description leaf; missing
prerequisite results or a stale SIDE-003.1 baseline (stop and report).

Next action: derive `verification.md`, obtain a ready `preflight.md` through
standalone guided preflight, then implement.
Required follow-on: immediately after implementation or correction and any
applicable conditional stages, hand the completed bytes to a fresh independent
`task-review-discovery` call, and hand its report to a separate
`task-acceptance-review` decision.

Expected contract impact: none — descriptions are not registered contract
authority; `task-orchestrator.json` declarations cite scripts and tests,
which this leaf does not touch.