# Preflight: T-002.3 — Apply contextual risk and coordinator-owned deferrals

Status: `ready`
Profile: standalone guided
Brief: `docs/tasks/T-002.3/brief.md` (SHA-256 `5c8ae611…00ec2`)
Verification design: `docs/tasks/T-002.3/verification.md`, revision 1
  (SHA-256 `aa35a93a…15cf7f`; `Source brief:` resolves to the package brief;
  source-revision digest `5c8ae611…00ec2` matches current brief bytes)

## Standalone preflight value

`standalone_preflight_value: material`

The brief's named uncertainty — "confirm .2 admission fields and T-001's current
context/known-issue consumption" — was genuinely material before this check and
is now resolved:

- T-002.2 is accepted: `HEAD 2a71e4c "task T-002.2 done (accepted)"` contains the
  admission contract in the source tree
  (`skills/task-implementation-flow/task-acceptance-review/references/
  acceptance-report-template.md`: finding Disposition field, section 3 admitted
  evidence ledger with the four reconciled results, continuation block).
- T-001's context/known-issue consumption is present in the source preflight
  skill (`skills/task-implementation-flow/task-preflight/SKILL.md`): compact
  decision context, "Reassess relevant known issues against this task's exposure
  and obligations", missing known-issues file means no recorded deferrals.
- A further material fact surfaced by this check: the installed projection
  `.agents/skills/task-implementation-flow/…/acceptance-report-template.md`
  is stale (lacks the .2 admitted-ledger sections) and must not be used or
  edited by this task (see Warnings).

Residual facts are routine; no further standalone preflight is needed.

## Scope and ownership

- Confirmed scope: contextual rubric/guidance and coordinator deferral-record
  guidance in `skills/task-implementation-flow/task-acceptance-review/` (SKILL,
  report template, evals), flow/stage entries (root README, profile guide, flow
  README), and fixture/contract assertions in `tests/test_review_discipline.py`.
  Minimal preflight skill packet reference/eval updates only if implemented
  T-001 consumer wording omits an approved ART-008 obligation.
- Ownership clean: no tracked modifications. Untracked: `.DS_Store` files
  (root/docs/skills, user junk — do not touch) and
  `docs/tasks/T-002.3/verification.md` (pipeline artifact). No user work
  overlaps the edit area.
- Installer: `scripts/install_development_skills.py` — inspect constants when
  editing selected-skill guidance; no new selected skill or shared helper
  expected. `.agents/` copies are read-only for this task.
- Dependency: T-002.3 leaf `executable`, depends on accepted T-002.2 (index.json).

## Command and oracle

Targeted owning gate (from repository root, after focused fail-first pass):

```
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_review_discipline.py
```

- Ran at preflight: OK, 25 tests pass, 0.19s (baseline before change; the
  fail-first assertions do not exist yet, so the suite is expected to stay
  green only after they are added and satisfied).
- Oracle: scenario coverage V-01–V-08 in verification.md maps every AC-01–06
  and finite-risk row R-01–R-04 to contract/fixture assertions in
  `test_review_discipline.py`, with contrasting supplied inputs and setup
  probes. Local assertions prove contract agreement; they cannot prove an
  agent made the decision, asked a question, or obeyed writer permissions —
  those behavioral gaps stay visible as T-005's ownership and must be recorded
  as unrun. Run a changed preflight fixture's local setup check only if that
  source changes.

## Warnings

- `.agents/skills/` installed projections are stale versus `skills/` source
  (acceptance-report-template.md differs: no .2 admitted ledger/Disposition).
  This task edits only the source tree and treats `.agents/` as read-only;
  the installer/projection refresh is T-002.4's composition ownership. A fresh
  acceptance reviewer must review the `skills/` source bytes, not the stale
  installed copy.
- Budget 15 tool calls / 40 minutes / 50k context is a soft checkpoint.
- No real `docs/known-issues.md` record may be created without an
  acceptance-approved deferral and coordinator authority; acceptance has no
  portfolio scheduling/backlog-write authority.

## Implementation stops

Stop for missing material direction, incompatible admission/context interface,
user-work overlap, unavailable decisive capability, unsafe permission, or scope
expansion. Do not resolve missing business policy by invention. No live,
agent-budget, or repository-wide gate; no `.agents/` refresh.

## Next action

Hand this ready preflight to bounded implementation (fail-first assertions for
ACCEPT-on-green-tests, ordinary-unknown prompts, dropped mixed rows, then the
targeted gate). After implementation or correction, hand completed bytes to a
fresh independent acceptance reviewer and end the implementation invocation.

## Implementer handoff

```text
Task: T-002.3 — Apply contextual risk and coordinator-owned deferrals.
Status: preflight READY (guided). Brief SHA-256 5c8ae611…00ec2 matches verification.md revision 1.

Edit scope (confirmed, ownership clean):
- skills/task-implementation-flow/task-acceptance-review/SKILL.md
- skills/task-implementation-flow/task-acceptance-review/references/acceptance-report-template.md
- skills/task-implementation-flow/task-acceptance-review/evals/ (existing defs/setup)
- tests/test_review_discipline.py (contextual rubric + record/consumer fixture assertions)
- Stage entries: root README.md, profile guide, skills/task-implementation-flow/README.md
- Minimal preflight skill packet update only if implemented T-001 consumer wording omits an
  approved ART-008 obligation; inspect scripts/install_development_skills.py constants.
Read-only: discovery contract, unrelated preparation, plans, historical reviews, .agents/
copies, docs/tasks/T-002.3/verification.md, .DS_Store files. No real known-issues records.

Command (repo root, after focused fail-first pass):
  PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_review_discipline.py
Preflight baseline: 25 tests OK (0.19s).

Oracle: verification.md scenarios V-01–V-08; local checks prove contract agreement only;
live role compliance (decisions, prompts, writer permissions) is T-005 — record as unrun.
Coordinator alone records approved deferrals in docs/known-issues.md before advancement;
no tracker writes. Ordinary unknowns continue under stated assumptions; required proof is
never waived; neither CHANGES_REQUESTED nor INCONCLUSIVE permits advancement.

Stops: missing material direction, incompatible admission/context interface, user-work
overlap, unavailable decisive capability, unsafe permission, scope expansion. Budget is a
soft checkpoint. After implementation/correction: hand to fresh independent acceptance
reviewer, end invocation.
```
