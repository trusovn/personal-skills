# Preflight: Q-01 — Review significant changed test assets for maintainability

Status: `ready` — focused renewal under the owner amendment / verification
revision 2 (2026-10-12), on the staged submission

Profile: guided (brief routes `standalone guided preflight`)
Standalone preflight value: `material`

This renewal supersedes the revision-1 preflight below. The user amended Q-01's
completion boundary on 2026-10-12: actual reviewer trials belong to
Q-01-QUALIFICATION. See [the amended brief](brief.md),
[verification revision 2](verification.md),
[qualification handoff](qualification-handoff.md),
[implementation](implementation.md) and the review reports. The original
preflight is retained below as history.

## Resolved uncertainties (renewal against revision 2)

1. **Staged identity vs recorded identities.** All 16 tracked changes are
   staged; zero unstaged changes. All 9 SHA-256 source identities recorded in
   `implementation.md` match the current bytes exactly; the staged submission
   is byte-for-byte what the implementer verified. `HEAD` `40b36321` matches
   the recorded baseline.
2. **Verification design binding.** `verification.md` revision 2 declares
   `Source brief: docs/tasks/Q-01/brief.md`; current brief blob
   `be80cdf7c8116ab74d8abdc5f3828de469d2e9c7` equals its declared
   `Source brief revision`. Read as derived guidance only; brief remains
   authority. V-01–V-09 map every AC and R-01–R-04.
3. **Ownership.** The staged set is entirely within Q-01 scope (primary
   skill/test surfaces, minimal guide alignment, task-package docs).
   `AGENTS.md` and `docs/tasks/index.json` are no longer dirty, resolving the
   original preflight's user-work warning. Only untracked files are
   `.DS_Store` at root, `docs/`, `skills/` — outside scope; preserve, do not
   stage.
4. **Handoff completeness.** `qualification-handoff.md` records all unrun role
   cases (V-02–V-08 role) with owner Q-01-QUALIFICATION, held-back oracle
   protocol, and states the follow-up is unrun and not executable-ready.
   Discovery ledger retains all V-01–V-09 and R-01–R-04.
5. **Executability of staged bytes.** The brief-frozen selectors reran on the
   staged tree: 23 tests OK (maintainability), 14 OK (guides), 15 OK
   (installer). Environment is not broken.

## Ownership

- `git status --short`: 16 staged, 0 unstaged, 3 untracked `.DS_Store`.
- Q-01 surfaces only; no overlap with user-owned work. Preserve the untracked
  files and keep the installer within its managed AGENTS.md boundary.

## Frozen selectors (reran on staged bytes)

- Targeted: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_task_maintainability_review.py` → 23 OK.
- Guides: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_task_flow_guides.py` → 14 OK.
- Installer: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py` → 15 OK.
- Repository disk projection (`python3 scripts/install_development_skills.py .`):
  deferred by recorded user override — see warnings.

## Warnings

- **AC-06 repository disk projection is deferred by recorded user override.**
  `implementation.md` records `Operation not permitted` on
  `.agents/.development-install-*` and escalation canceled by the user.
  Disposable-install evidence exists (installer suite), but the repository
  on-disk projection clause is unverified by instruction, not by failure.
  Acceptance must consume this override explicitly; fresh discovery should
  corroborate disposable evidence only and not claim disk projection.
- **`git diff --cached --check`** flags `reviews/discovery-01.md:291: new
  blank line at EOF` — cosmetic, in a review report; note that
  `implementation.md`'s "`git diff --check` passed" predates staging the
  review reports. The staged tree is not whitespace-clean.
- **Carry-forward from `reviews/maintainability-01.md`** (ACCEPT, no
  blockers): duplicated scenario-value knowledge across test owners and
  stringly-coupled variant derivation in `setup_fixture.py` are recorded as
  non-blocking with directions. Future fixture maintenance concern, not a
  Q-01 acceptance blocker.

## Stops (none triggered)

Unresolved overlapping ownership, changed authority, user-work overlap,
unsafe permissions, new infrastructure, missing decisive capability — none
currently apply. The changed authority (amendment + install deferral) is
recorded in the brief and implementation report.

## Next action

Proceed to **fresh discovery under revision 2**, then **separate acceptance**;
acceptance decides the AC-06 disk-projection clause against the recorded user
override. Q-01-QUALIFICATION owns the role trials and must prepare its own
brief/verification/preflight before any model-budget runs. Existing
discovery-01/maintainability-01 remain historical evidence.

## Implementer handoff

```text
Task: docs/tasks/Q-01/brief.md (ready, executable; owner amendment 2026-10-12)
Verification: docs/tasks/Q-01/verification.md revision 2 (derived; brief blob matches)
Preflight renewal: ready (guided, material). 16 staged, 0 unstaged.
  All 9 recorded source identities match; brief blob == verification declaration.
  Frozen selectors green on staged bytes: 23 / 14 / 15 OK.

Scope/ownership: only Q-01 surfaces staged. AGENTS.md + index.json clean.
  Untracked .DS_Store x3: preserve, do not stage.

Warnings: (1) AC-06 repo disk projection deferred by user override — acceptance
  consumes it explicitly; (2) diff --cached --check: blank line at EOF in
  reviews/discovery-01.md:291 (cosmetic); (3) maintainability-01 carry-forward
  warnings are non-blocking fixture notes.

Next: fresh discovery under revision 2 -> separate acceptance; Q-01-QUALIFICATION
  owns unrun role trials (V-02..V-08 role) and must prepare its own package first.
```

Standalone renewal value was `material` (identity binding and
override-resolution entry conditions); recommend the same focused renewal for
the next materially similar amended-contract handoff.

---

## Original preflight (historical)

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
