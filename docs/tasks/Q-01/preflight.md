# Preflight: Q-01 — Review significant changed test assets for maintainability

Status: `ready`
Profile: guided (brief routes `standalone guided preflight`)
Standalone preflight value: `material`

## Resolved uncertainties (from the brief's named route)

1. T-003 ownership of overlapping surfaces — resolved. Git history shows
   T-003.1/2/3/4 all `done (accepted)` (`9faec6c`, `6bf933c`, `bcd0ad6`,
   `9a11faf`), and no worktree changes touch Q-01's implementation surfaces.
   The surfaces T-003.2 created (`skills/task-implementation-flow/
   task-maintainability-review/`, `tests/test_task_maintainability_review.py`)
   are committed at HEAD and free of in-flight edits. No unfinished T-003
   overlap to resolve with an owner.
2. Existing fixture commands — confirmed executable. Targeted command run:
   `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_task_maintainability_review.py`
   → 18 tests OK in 0.2s. `tests/staging_fixture_support.py` and the owning
   guide/installer tests exist. Environment is not broken; fail-first
   rejection of the old production-only contract remains implementation work.
3. Installation repair boundary — confirmed. `scripts/install_development_skills.py`
   exists. Installed projection `.agents/skills/task-implementation-flow/
   task-maintainability-review/` still lacks `evals/files/setup_fixture.py`
   (only `SKILL.md`, `evals/evals.json`), matching the brief's design-time
   drift observation at `1c3b2c96`. AC-06's canonical-install repair step
   (`python3 scripts/install_development_skills.py .`) is the authorized
   boundary; no active-session refresh may be claimed.

## Verification design check

- `verification.md` `Source brief:` resolves to `docs/tasks/Q-01/brief.md`;
  declared blob `425a8d379f367ccbda2e6cc8e76778e6836fbe45` matches the
  current brief blob. Read as derived guidance only; brief remains authority.
- All six ACs map to scenarios V-01–V-09. Fresh-reviewer detection (AC-05,
  V-02/03/05/06) is a real boundary owned by fresh discovery after
  implementation, with held-back oracle; not exercisable in preflight and not
  blocked — the design already routes it and requires asking before
  costly/live-networked model evals.

## Ownership

- Implementation surfaces are clean: `skills/task-implementation-flow/
  task-maintainability-review/`, `tests/test_task_maintainability_review.py`,
  `README.md`, `skills/README.md`, `skills/task-implementation-flow/README.md`,
  `tests/test_task_flow_guides.py`, `tests/test_install_development_skills.py`,
  `scripts/install_development_skills.py` — none dirty.
- Pre-existing user-owned changes are outside Q-01's edit scope and must be
  preserved: `M AGENTS.md`, `M docs/tasks/index.json`, untracked `.DS_Store`
  files. Q-01 must not edit `AGENTS.md` or `index.json` directly; the
  installer manages its marked AGENTS.md block and preserves unmanaged text.

## Frozen selectors

- Targeted: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_task_maintainability_review.py`
- Then only if surfaces changed: `test_task_flow_guides.py`, then
  `test_install_development_skills.py` (projection/preservation).
- Disk projection: `python3 scripts/install_development_skills.py .`, then
  compare full managed inventory/bytes against source, excluding existing
  installer transient patterns. No whole-repository suite.

## Warnings

- `AGENTS.md` and `index.json` carry user edits; keep implementation clear of
  them and run the installer only through its managed boundary.
- The installed-projection drift persists until AC-06's projection step; do
  not treat it as a Q-01 blocker — it is the pre-existing drift the brief
  explicitly does not repair before implementation verification.
- AC-05 fresh-reviewer qualification cannot run during implementation
  self-verification; it is fresh discovery's evidence. Unrun behavioral proof
  is a gap to record, not silent completion.

## Stops (none triggered)

Unresolved overlapping ownership, changed authority, user-work overlap,
unsafe permissions, new infrastructure, missing decisive capability — none
currently apply.

## Next action

`ready` describes the designed contract; it does not authorize implementation.
Obtain the separate Q-01 execution authorization, then run bounded
implementation with the frozen selectors; hand completed bytes to fresh
independent acceptance review — do not self-accept.

## Implementer handoff

```text
Task: docs/tasks/Q-01/brief.md (Status ready, kind executable)
Verification design: docs/tasks/Q-01/verification.md (derived; brief is authority)
Preflight: ready (guided, material). T-003 accepted; surfaces clean; environment OK.

Scope: edit skills/task-implementation-flow/task-maintainability-review/
(SKILL.md, evals/evals.json, evals/files/setup_fixture.py) and
tests/test_task_maintainability_review.py; minimal alignment only in
skills/task-implementation-flow/README.md, skills/README.md, root README.md,
tests/test_task_flow_guides.py, tests/test_install_development_skills.py.
Inspect scripts/install_development_skills.py; keep its declarations and
managed AGENTS.md block boundary. Do NOT edit AGENTS.md, index.json, plan
docs, or claim active-session refresh.

Commands (repository root):
1. PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_task_maintainability_review.py
2. (only for changed guide/routing surfaces)
   PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_task_flow_guides.py
3. PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py
4. python3 scripts/install_development_skills.py .   # then byte-compare managed
   skill files and profile guide vs source; run installed setup without
   repository-only helpers (AC-06).

Oracle: verification.md V-01–V-09 map every AC; fail-first must reject the old
production-only contract; AC-05 fresh-reviewer detection is fresh discovery's
evidence with held-back oracle (ask before costly/live-networked model evals).

Warnings: preserve user-owned AGENTS.md/index.json edits; installed-projection
drift is pre-existing and repaired only via the canonical installer; record
any unrun behavioral proof as a gap.

Next: separate Q-01 execution authorization → implement → fresh independent
acceptance review. Do not self-accept.
```
