# Task Brief: SIDE-003.2 — Compress descriptions: boundary groups 1–2

## Outcome

The six profile-skill descriptions in plan boundary groups 1–2 —
project-direction, project-bootstrap, ai-flow-foundation, repo-foundation,
architecture-guardrails, foundation-readiness-review — are shortened to the
job, positive trigger, and consequential exclusions, with old/new wording,
preserved trigger boundaries, and catalog measurements recorded in this
leaf's section of `docs/tasks/SIDE-003/description-results.md`. Bodies are
unchanged in this phase.

## Authority and scope

| Item | Contract |
|---|---|
| Authority | [SIDE-003 plan](../SIDE-003/plan.md), "Description design" (targets, boundary-group table rows for groups 1–2, exclusions), "Delivery sequence" phase 2, "Measurement and decision rules" layer 1; [parent brief](../SIDE-003/brief.md); [SIDE-003.1 baseline](../SIDE-003/baseline.md) |
| Allowed changes | The `description` frontmatter field of the six named `SKILL.md` files; this leaf's section in `description-results.md`; owning assertions that quote the changed description text (if any) |
| Read-only context | The six skills' bodies and references; every other skill; `tests/test_install_development_skills.py` (reads project-bootstrap, ai-flow-foundation, repo-foundation, architecture-guardrails `SKILL.md` — inspect whether it asserts description text) |
| Out of scope | Body text of any kind (frontmatter `description` only); names, folder paths, invocation identities; other groups' skills; the profile guide and installation README unless they quote description text (inspect; synchronize only if so) |
| Assumptions / unresolved | Which owning surfaces assert these description strings (discover from the SIDE-003.1 prerequisites map) |

## Work and acceptance criteria

Required work:

1. For each skill, derive a trigger checklist from its current description
   and its group's distinction. Group 1: owner direction vs initial
   engineering foundation vs model behavior in the product itself —
   agent-maintained code alone does not trigger AI foundation. Group 2:
   repository structure/tooling vs deterministic boundary enforcement vs
   independent readiness review before product work.
2. Draft and apply a compressed description (~150–300 characters where
   sufficient — an editorial starting point that cannot override accurate
   routing), retaining the job, positive trigger, and consequential
   exclusions.
3. Append this leaf's section to `description-results.md`: per skill old/new
   wording, character counts, preserved boundaries, and the catalog
   measurement delta from re-running the SIDE-003.1 command (all-26 and
   profile-20 totals).

- **AC-01:** Each of the six descriptions retains its job, positive trigger,
  and consequential exclusions; old/new wording and preserved boundaries are
  recorded; before/after catalog measurements are recorded.
- **AC-02:** No valid current use case or activation route is dropped to
  reach a length; each group's nearest-neighbor distinction survives
  compression; procedural detail removed from a description is either already
  present in that skill's body or is kept in place and flagged in the results
  section — never silently dropped.
- **AC-03:** Only the six `description` values change: `git diff` shows
  description-line-only changes under `skills/`; names/paths/identities are
  unchanged; description-quoting assertions are synced or verified absent;
  `quick_validate.py` runs for the touched packages if the optional PyYAML
  environment is available, otherwise the skip is recorded.

## Verification

| Evidence | Scenario and oracle | Command |
|---|---|---|
| Fail-first | Infeasible for editorial compression; the decisive negative oracle is the body-unchanged guard — the diff must contain no non-description changes — plus the per-skill boundary checklist | `git diff --stat` + targeted `git diff` per file |
| Targeted | Per-skill trigger checklist against the plan's boundary-group row; catalog measurement re-run records the expected reduction | SIDE-003.1 measurement command |
| Owning suite | Assertions quoting changed text, from the SIDE-003.1 prerequisites map (installer suite for the four skills it reads) | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py` |
| Broader gate | Aggregate gate at SIDE-003.18; fresh-model routing evals (explicit, implicit positive, clear negative, nearest-neighbor catalog prompts) only with separately approved budget, else reported pending | SIDE-003.18 |

## Execution

Status: `ready`; task kind: `executable`; guided profile.
Readiness route: standalone guided preflight after derived verification —
confirm SIDE-003.1's record is current and description-quoting assertions are
known before edits.
Verification-design recommendation: separate — the decisive evidence is the
per-skill trigger-boundary case set (positive, negative, neighbor), and the
approval-gated routing-eval inputs should be designed now so they are ready
when a budget exists.

```yaml
agent_tier: standard
reasoning: medium
review: immediate
budget: 15 tool calls / 40 minutes / six description edits, results section, measurements
```

Sizing: `default@1`; estimate 13 implementation calls / 38 minutes;
confidence medium; fits.

Stops: do not narrow activation to hit the character range; do not touch
bodies; do not run concurrently with another active description leaf (shared
results file, per-group attribution); missing or stale SIDE-003.1 baseline
(stop and report).

Next action: derive `verification.md`, obtain a ready `preflight.md` through
standalone guided preflight, then implement.
Required follow-on: immediately after implementation or correction and any
applicable conditional stages, hand the completed bytes to a fresh independent
`task-review-discovery` call, and hand its report to a separate
`task-acceptance-review` decision.

Expected contract impact: none — descriptions are not registered contract
authority; `measurement.json` and `implementer-feedback.json` declarations
cite bodies, which this leaf does not touch.