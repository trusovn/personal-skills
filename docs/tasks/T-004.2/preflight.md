# Preflight: T-004.2

Status: `ready`
Profile: guided
standalone_preflight_value: `material`
Checked: 2026-10-12
Source brief: docs/tasks/T-004.2/brief.md
Source brief revision: ready brief, SHA-256 `ecf57bb5cb33dda3405269c3f6adf05628248d2a4510fe34358d98d8e027512e`
Verification design: docs/tasks/T-004.2/verification.md (revision 1, untracked, pre-existing)

## Readiness route

The brief's named route — standalone guided preflight confirming the reviewed
.1 interface, managed projection, and current source/target validation — was
executed. All named uncertainties were real and are now resolved:

- Reviewed .1 interface: T-004.1 is committed at HEAD `93cd0e4` ("4.1 done");
  its owning installer suite is green at current HEAD (17 tests OK, 1.7s).
- Managed projection: `DEVELOPMENT_SKILL_SOURCES`, `PROFILE_SKILLS_README`,
  `SHARED_SCRIPT_FILES`, and `TRANSIENT_PATTERNS` (`__pycache__`, `*.pyc`,
  `.DS_Store`, `node_modules`) are present in
  `scripts/install_development_skills.py`.
- Current source/target validation: the CLI is positional install-only;
  `--check` is rejected (exit 2, "unrecognized arguments") — the old
  missing-check behavior is real, so AC-01's fail-first state is live.

Classification: `material` — the brief mandates a ready `preflight.md` as an
implementation gate (durable cross-session handoff), and the .1-interface/HEAD
state plus fail-first encoding were not visible from the brief alone.

`verification.md` `Source brief:` resolves to this package's `brief.md` and its
declared SHA-256 matches the current brief bytes. Scenarios V-01–V-07 cover
AC-01–AC-05 and R-01–R-03 with observable CLI oracles; no blocked scenarios.
Exact CLI/result encoding stays implementer-local design per the brief
("no missing product decision"); this preflight records the grant, not a design.

## Scope, dependencies and ownership

- HEAD `93cd0e4ab17d5a26c7b38c56b4b60fbd149e6acd`; branch `t-o-new-flow`.
- Allowed change paths are clean (no user work, no overlap):
  `scripts/install_development_skills.py`,
  `tests/test_install_development_skills.py`, root `README.md`,
  `skills/README.md` (all exist and are unmodified).
- Pre-existing untracked files — preserve, do not touch: `.DS_Store`,
  `docs/.DS_Store`, `skills/.DS_Store`, and `docs/tasks/T-004.2/verification.md`
  (required derived artifact from the verification-design stage).
- Dependency T-004.1: committed, suite green. Note: no separate acceptance
  report is recorded in `docs/tasks/T-004.1/reviews/` (discovery-01/02 only);
  the plan-level close is commit "4.1 done" and the brief declares the
  dependency completed/reviewed. Not a blocker; route plan-state questions to
  the owner.

## Commands and oracles

- Owning targeted command (ran, green at HEAD `93cd0e4`):
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py`
  → 17 tests OK in 1.7s. Python 3.14.4.
- Fail-first probe (ran): `python3 scripts/install_development_skills.py --check <target>`
  → exit 2, `unrecognized arguments: --check`. Targeted cases must reject this
  old behavior (brief Verification section).
- Reusable fixture helpers exist in `tests/test_install_development_skills.py`:
  `init_repo`, `run_installer`, `collect_package_files`, `git` (lines 161–218);
  unborn/committed temp-repo tests already pass there. No new harness required.
- Oracle mapping: V-01–V-05/AC-01–03 → public CLI output/exit classes vs
  independent fixture path/byte deltas; V-06/AC-04 → before/after source/target/
  Git/evidence snapshots in real temp repos (Git status alone is insufficient);
  V-07/AC-05 → positional install from unrelated CWD plus guidance-doc
  inspection. Unit/module evidence in real temp filesystems suffices; brief
  bars whole-repo/live/model gates.

## Warnings

- T-004.1's independent acceptance decision is not separately recorded in its
  package (see above); .2's fresh discovery/acceptance routing should not
  assume such a report exists.
- V-05 read-failure oracles: prefer real filesystem/process failures; only if
  a read failure cannot be made deterministic may a controlled
  filesystem-boundary failure exercise the actual error path (brief R-02).
- `docs/tasks/T-004.2/verification.md` is untracked and pre-existing; this
  packet's only new artifact is this `preflight.md`.

## Stops and next action

- Stops: changed authority, user-work overlap in allowed paths, unsafe
  permission needs, missing decisive evidence, required scope expansion; budget
  is a soft checkpoint; preserve the two-materially-different-failed-fixes stop.
- Next: implement the smallest production/test change per brief + verification
  scenarios, run targeted rows then the owning suite; then hand completed bytes
  to fresh independent `task-review-discovery` and its report to a separate
  `task-acceptance-review`.
