# Preflight: T-002.2 — Make acceptance admit discovery evidence and decide

Status: `ready`
Profile: standalone guided
Brief: `docs/tasks/T-002.2/brief.md` (SHA-256 `2913f3e8…bb700`)
Verification design: `docs/tasks/T-002.2/verification.md`, revision 1
  (SHA-256 `229c7562…dd2b43`; `Source brief:` resolves to the package brief;
  source-revision digest matches current brief bytes)

## Standalone preflight value

`standalone_preflight_value: material`

The brief's named uncertainty — "confirm .1's completed evidence interface and
current review fixtures" — was genuinely material before this check and is now
resolved:

- T-002.1 is accepted: `HEAD 4a4b771 "T-002.1 done (accepted)"` contains the
  complete discovery evidence interface (`skills/task-implementation-flow/
  task-review-discovery/` SKILL, `references/discovery-report-template.md`,
  `evals/evals.json` ids 1–9/11–15, `evals/files/setup_fixture.py`).
- Acceptance review fixtures are current: `task-acceptance-review/evals/
  evals.json` ids 1–10 and its `setup_fixture.py` exist and are committed.
- The owning gate executes green on current bytes (19 tests, 0.17s, OK), so
  fail-first updates have a clean baseline to redden.

Residual facts are routine; no further standalone preflight is needed.

## Scope and ownership

- Confirmed scope: acceptance `SKILL.md`, `references/acceptance-report-template.md`
  and existing eval definitions/setup under
  `skills/task-implementation-flow/task-acceptance-review/`; discovery-evidence
  and decision assertions in `tests/test_review_discipline.py`; stage entries in
  root README, profile guide, flow README. Discovery sources read-only.
- Ownership clean: no tracked modifications; working tree has only untracked
  `.DS_Store` files (root/docs/skills) and the pipeline artifact
  `docs/tasks/T-002.2/verification.md`. No user work overlaps the edit area.
  `__pycache__` files are gitignored. Do not touch the `.DS_Store` files or
  verification.md.
- Installer: `scripts/install_development_skills.py` already installs both
  `task-acceptance-review` and `task-review-discovery`; no selection/helper
  change expected. No `docs/contracts` registry exists.
- Dependency: T-002.2 leaf `executable`, depends on accepted T-002.1 (index.json).

## Command and oracle

Targeted owning gate (from repository root, after focused fail-first pass):

```
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_review_discipline.py
```

- Ran at preflight: OK, 19 tests pass, 0.17s (baseline before change).
- Oracle: scenario coverage V-01–V-10 in verification.md maps each AC and
  finite-risk row (A-01–A-04) to contract/fixture assertions in
  `test_review_discipline.py`. Local assertions prove contract agreement; they
  cannot prove live agent behavior — actual separate-call and write compliance
  remains the separately authorized T-005 qualification and must be recorded
  as unrun. Do not label text/schema/setup checks as behavioral.

## Warnings

- Budget 12 tool calls / 32 min / 45k context is a soft checkpoint.
- Preserve original eval signals while moving public/process probing
  expectations to discovery inputs and decision expectations to acceptance;
  update old schema obligations rather than deleting them.
- Explicit omitted-AC violations must still block (green tests cannot waive).

## Implementation stops

Stop for ambiguous authority, incomplete .1, incompatible report contract,
inseparable user work, unsafe permissions, widened scope, or missing decisive
capability.

## Next action

Hand this ready preflight to bounded implementation; after implementation or
correction, hand completed bytes to a fresh independent acceptance reviewer and
end the implementation invocation. .3 consumes the admission contract next.

## Implementer handoff

```text
Task: T-002.2 — Make acceptance admit discovery evidence and decide.
Status: preflight READY (guided). Brief SHA-256 2913f3e8…bb700 matches verification.md revision 1.

Edit scope (confirmed, ownership clean):
- skills/task-implementation-flow/task-acceptance-review/SKILL.md
- skills/task-implementation-flow/task-acceptance-review/references/acceptance-report-template.md
- skills/task-implementation-flow/task-acceptance-review/evals/ (existing defs/setup)
- tests/test_review_discipline.py (discovery-evidence + decision assertions)
- Stage entries: root README.md, profile guide, skills/task-implementation-flow/README.md
Read-only: task-review-discovery sources, T-001 sources, plans, .agents/ copies, docs/tasks/T-002.2/verification.md, .DS_Store files.

Command (repo root, after focused fail-first pass):
  PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_review_discipline.py
Preflight baseline: 19 tests OK (0.17s).

Oracle: verification.md scenarios V-01–V-10; local checks prove contract agreement only;
live role compliance is T-005 (record as unrun). Missing discovery routes to its owner;
verdicts remain exactly ACCEPT / CHANGES_REQUESTED / INCONCLUSIVE; SELF_CHECK_ONLY is a
non-verdict label. Durable decisions use next unused reviews/acceptance-NN.md; no tracker
writes or advancement. Preserve the tests-only exception exactly.

Stops: authority ambiguity, incomplete .1, incompatible report contract, user-work overlap,
unsafe permissions, widened scope, missing decisive capability. Budget is a soft checkpoint.
After implementation/correction: hand to fresh independent acceptance reviewer, end invocation.
```
