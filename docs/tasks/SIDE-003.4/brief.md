# Task Brief: SIDE-003.4 — Compress descriptions: boundary groups 5–6

## Outcome

The five profile-skill descriptions in plan boundary groups 5–6 —
bounded-task-implementer, task-maintainability-review,
task-contract-registry-updater, task-review-discovery, task-acceptance-review
— are shortened to the job, positive trigger, and consequential exclusions,
with old/new wording, preserved trigger boundaries, and catalog measurements
recorded in this leaf's section of
`docs/tasks/SIDE-003/description-results.md`. Bodies are unchanged in this
phase.

## Authority and scope

| Item | Contract |
|---|---|
| Authority | [SIDE-003 plan](../SIDE-003/plan.md), "Description design" (targets, boundary-group table rows for groups 5–6, the candidate implementer description and its activation-route caveat), "Delivery sequence" phase 2; [parent brief](../SIDE-003/brief.md); [SIDE-003.1 baseline](../SIDE-003/baseline.md) |
| Allowed changes | The `description` frontmatter field of the five named `SKILL.md` files; this leaf's section in `description-results.md`; owning assertions that quote the changed description text (if any) |
| Read-only context | The five skills' bodies and references; `tests/test_bounded_task_implementer.py`, `tests/test_task_maintainability_review.py`, `tests/test_review_composition.py`, `tests/test_task_review_discovery.py`, `tests/review_fixture_support.py`, `tests/test_run_evidence_availability.py` (read these files — inspect whether they assert description text) |
| Out of scope | Body text of any kind (frontmatter `description` only); names, folder paths, invocation identities; other groups' skills; the entry-instruction retention of the implementer's machine-contract route (owned by SIDE-003.7) |
| Assumptions / unresolved | Which owning surfaces assert these description strings (discover from the SIDE-003.1 prerequisites map) |

## Work and acceptance criteria

Required work:

1. For each skill, derive a trigger checklist from its current description
   and its group's distinction. Group 5: authoring scoped implementation vs
   independent structural review when policy or the user requires it.
   Group 6: synchronizing current contracts vs independent evidence without
   a verdict vs a separate acceptance decision after discovery.
2. Draft and apply a compressed description (~150–300 characters where
   sufficient — an editorial starting point that cannot override accurate
   routing), retaining the job, positive trigger, and consequential
   exclusions. The plan's candidate implementer description may be adapted;
   "explicitly requested high-assurance" alone must not hide activation
   through a supplied machine contract — the compressed description keeps
   that route visible.
3. Append this leaf's section to `description-results.md`: per skill old/new
   wording, character counts, preserved boundaries, and the catalog
   measurement delta from re-running the SIDE-003.1 command (all-26 and
   profile-20 totals).

- **AC-01:** Each of the five descriptions retains its job, positive trigger,
  and consequential exclusions; old/new wording and preserved boundaries are
  recorded; before/after catalog measurements are recorded.
- **AC-02:** No valid current use case or activation route is dropped to
  reach a length — in particular the implementer's supplied-machine-contract
  activation remains explicit; each group's nearest-neighbor distinction
  survives; procedural detail removed from a description is either already
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
| Owning suite | Assertions quoting changed text, from the SIDE-003.1 prerequisites map (implementer, review-composition, and discovery suites read these files) | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_bounded_task_implementer.py` |
| Broader gate | Aggregate gate at SIDE-003.18; fresh-model routing evals only with separately approved budget, else reported pending — the routing design must exercise the implementer's machine-contract activation route separately from the explicit high-assurance route | SIDE-003.18 |

## Execution

Status: `ready`; task kind: `executable`; guided profile.
Readiness route: standalone guided preflight after derived verification —
confirm SIDE-003.1's record is current and description-quoting assertions are
known before edits.
Verification-design recommendation: separate — the decisive evidence is the
per-skill trigger-boundary case set, including the implementer's
machine-contract activation case kept separate from explicit invocation.

```yaml
agent_tier: standard
reasoning: medium
review: immediate
budget: 14 tool calls / 38 minutes / five description edits, results section, measurements
```

Sizing: `default@1`; estimate 12 implementation calls / 35 minutes;
confidence medium; fits.

Stops: do not narrow activation to hit the character range (especially the
machine-contract route); do not touch bodies; do not run concurrently with
another active description leaf; missing or stale SIDE-003.1 baseline (stop
and report).

Next action: derive `verification.md`, obtain a ready `preflight.md` through
standalone guided preflight, then implement.
Required follow-on: immediately after implementation or correction and any
applicable conditional stages, hand the completed bytes to a fresh independent
`task-review-discovery` call, and hand its report to a separate
`task-acceptance-review` decision.

Expected contract impact: none — descriptions are not registered contract
authority; `implementer-feedback.json` declarations cite the implementer's
body and evals, which this leaf does not touch.