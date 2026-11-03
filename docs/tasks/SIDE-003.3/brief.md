# Task Brief: SIDE-003.3 — Compress descriptions: boundary groups 3–4

## Outcome

The five profile-skill descriptions in plan boundary groups 3–4 —
project-delivery-plan, project-plan-verification, task-brief-designer,
task-verification-designer, task-preflight — are shortened to the job,
positive trigger, and consequential exclusions, with old/new wording,
preserved trigger boundaries, and catalog measurements recorded in this
leaf's section of `docs/tasks/SIDE-003/description-results.md`. Bodies are
unchanged in this phase.

## Authority and scope

| Item | Contract |
|---|---|
| Authority | [SIDE-003 plan](../SIDE-003/plan.md), "Description design" (targets, boundary-group table rows for groups 3–4, exclusions), "Delivery sequence" phase 2, "Measurement and decision rules" layer 1; [parent brief](../SIDE-003/brief.md); [SIDE-003.1 baseline](../SIDE-003/baseline.md) |
| Allowed changes | The `description` frontmatter field of the five named `SKILL.md` files; this leaf's section in `description-results.md`; owning assertions that quote the changed description text (if any) |
| Read-only context | The five skills' bodies and references; every other skill; `tests/test_task_preparation_contracts.py` and `tests/test_task_flow_guides.py` (read these skills' `SKILL.md` — inspect whether they assert description text) |
| Out of scope | Body text of any kind (frontmatter `description` only); names, folder paths, invocation identities; other groups' skills |
| Assumptions / unresolved | Which owning surfaces assert these description strings (discover from the SIDE-003.1 prerequisites map) |

## Work and acceptance criteria

Required work:

1. For each skill, derive a trigger checklist from its current description
   and its group's distinction. Group 3: composing a multi-task delivery
   plan vs a separate reviewer checking that plan — neither implements
   features. Group 4: task contract vs derived scenario/evidence design vs
   current execution readiness — preflight does not implement.
2. Draft and apply a compressed description (~150–300 characters where
   sufficient — an editorial starting point that cannot override accurate
   routing), retaining the job, positive trigger, and consequential
   exclusions.
3. Append this leaf's section to `description-results.md`: per skill old/new
   wording, character counts, preserved boundaries, and the catalog
   measurement delta from re-running the SIDE-003.1 command (all-26 and
   profile-20 totals).

- **AC-01:** Each of the five descriptions retains its job, positive trigger,
  and consequential exclusions; old/new wording and preserved boundaries are
  recorded; before/after catalog measurements are recorded.
- **AC-02:** No valid current use case or activation route is dropped to
  reach a length; each group's nearest-neighbor distinction survives
  compression; procedural detail removed from a description is either already
  present in that skill's body or is kept in place and flagged in the results
  section — never silently dropped.
- **AC-03:** Only the five `description` values change: `git diff` shows
  description-line-only changes under `skills/`; names/paths/identities are
  unchanged; description-quoting assertions are synced or verified absent;
  `quick_validate.py` runs for the touched packages if the optional PyYAML
  environment is available, otherwise the skip is recorded.

## Verification

| Evidence | Scenario and oracle | Command |
|---|---|---|
| Fail-first | Infeasible for editorial compression; the decisive negative oracle is the body-unchanged guard plus the per-skill boundary checklist | `git diff --stat` + targeted `git diff` per file |
| Targeted | Per-skill trigger checklist against the plan's boundary-group row; catalog measurement re-run records the expected reduction | SIDE-003.1 measurement command |
| Owning suite | Assertions quoting changed text, from the SIDE-003.1 prerequisites map (preparation-contract and flow-guide suites read these files) | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_task_preparation_contracts.py` |
| Broader gate | Aggregate gate at SIDE-003.18; fresh-model routing evals only with separately approved budget, else reported pending | SIDE-003.18 |

## Execution

Status: `ready`; task kind: `executable`; guided profile.
Readiness route: standalone guided preflight after derived verification —
confirm SIDE-003.1's record is current and description-quoting assertions are
known before edits.
Verification-design recommendation: separate — the decisive evidence is the
per-skill trigger-boundary case set, and the approval-gated routing-eval
inputs should be designed now.

```yaml
agent_tier: standard
reasoning: medium
review: immediate
budget: 14 tool calls / 38 minutes / five description edits, results section, measurements
```

Sizing: `default@1`; estimate 12 implementation calls / 35 minutes;
confidence medium; fits.

Stops: do not narrow activation to hit the character range; do not touch
bodies; do not run concurrently with another active description leaf; missing
or stale SIDE-003.1 baseline (stop and report).

Next action: derive `verification.md`, obtain a ready `preflight.md` through
standalone guided preflight, then implement.
Required follow-on: immediately after implementation or correction and any
applicable conditional stages, hand the completed bytes to a fresh independent
`task-review-discovery` call, and hand its report to a separate
`task-acceptance-review` decision.

Expected contract impact: none — descriptions are not registered contract
authority; the bodies this leaf does not touch hold the declared authority.