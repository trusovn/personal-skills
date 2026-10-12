# Preflight: T-004.1

Status: `ready`
Profile: guided
standalone_preflight_value: `material`
Checked: 2026-10-12
Source brief: docs/tasks/T-004.1/brief.md
Source brief revision: ready brief at Git blob `0744c01b6db8ece290e7dcdc527821de7ca144a2`
Verification design: docs/tasks/T-004.1/verification.md (revision 1)

## Readiness route

The brief's named route — standalone guided preflight confirming reviewed
T-001–003 applicability, current identity consumers, installed availability
commands, and new case selectors — was executed. All named uncertainties were
real before discovery and are now resolved with evidence below; the durable
preflight.md is required by the brief before implementation. Classification:
`material` (cross-task dependency applicability, exact consumer locations and
the installed availability command form, plus new-selector mechanics were not
visible from the brief alone and would have cost an implementer discovery).

- Executable leaf package; brief `Status: ready`, `Task kind: executable`.
  Parent `T-004` is a decomposed composite and was not preflighted.
- `verification.md` `Source brief:` resolves to this package's `brief.md`;
  its declared blob revision matches the current brief bytes. V-01–V-08 cover
  AC-01–AC-04 and R-01/R-02 with no blocked scenarios.

## Scope, dependencies and ownership

- HEAD `677904cc4df61292677e1876f1bafd06d412c693`.
- Allowed change paths are clean (no user work, no overlap):
  `scripts/workflow_version.py`, `scripts/run_evidence.py`,
  `scripts/install_development_skills.py`,
  `tests/test_workflow_version.py`, `tests/test_run_evidence.py`,
  `tests/test_install_development_skills.py`, root `README.md`,
  `skills/README.md`, flow README.
- Pre-existing dirty work outside this task's write scope — preserve, do not
  touch: `M docs/tasks/index.json` (listed read-only in the brief), untracked
  `docs/tasks/T-004*/` packages, `.DS_Store` files.
- Dependencies: T-001–003 source contracts are present in `scripts/` and their
  owning tests pass (see below). The parent brief requires applicability
  confirmation only; this preflight does not certify dependency completion.
- Capabilities: decisive mechanisms exist — Git subprocess CLIs and disposable
  temp-repo fixtures are already exercised by the existing owning tests.
  `DEVELOPMENT_SKILL_SOURCES`, `PROFILE_SKILLS_README`, `SHARED_SCRIPT_FILES`
  exist in the installer and are inspected per the brief.
- No shared harness prerequisite; no whole-repo, network, or model-budget gate.

## Current identity consumers / availability commands (confirmed)

- `scripts/workflow_version.py`: `_git(... "rev-parse", "HEAD")` supplies
  `repository_commit` (line ~228); `_git` raises `WorkflowVersionError` on any
  non-zero Git exit.
- `scripts/run_evidence.py`: `--repo` CLI; `evidence_availability()` calls
  `_get_workflow_version(repo_root, WORKFLOW_ID)` and fails on Git errors;
  further `rev-parse`/`read-tree HEAD` consumers at lines ~109/114/281/289.
- `scripts/install_development_skills.py`: target validation via
  `rev-parse --show-toplevel` (line ~82); staged gate
  `_run_availability` invokes `<stage>/scripts/run_evidence.py --repo <target>
  availability`; final installed form is
  `<target>/.agents/scripts/run_evidence.py --repo <target> availability`.
- Fail-first state is genuine: current identity/availability paths require a
  resolved HEAD, so a real unborn target fails on the task defect, not on
  missing fixture inputs or a broken environment (committed-state suite is
  green).

## Commands (run, all green)

| Command (cwd repo root) | Result |
|---|---|
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py` | 15 tests OK |
| same with `-p test_workflow_version.py` | 13 tests OK |
| same with `-p test_run_evidence.py` | 15 tests OK |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_install_development_skills test_workflow_version test_run_evidence` | 43 tests OK |

New-case selectors: the discover `-p <module>.py -k <NewCasePattern>` form and
the `PYTHONPATH=tests` top-level module form both work; concrete new case names
remain implementation-local design.

## Oracles (per AC)

- AC-01: canonical installer exit 0 on real `git init` target with complete
  profile inputs; final installed `run_evidence.py --repo <target>
  availability` prints `available: true`; independent `git symbolic-ref HEAD`
  and object inventory unchanged; no commit created.
- AC-02: identity output distinguishes unborn / resolved commit / Git error;
  committed and detached HEAD keep actual commit identities; invalid Git target
  remains a reported failure.
- AC-03: fingerprint equality and `sha256:` framing invariants via the
  existing identity/fingerprint entry point; reference must pre-date the
  changed algorithm.
- AC-04: independent byte comparison of projected selection/helpers against
  source; unmanaged bytes preserved; guidance states unborn boundaries without
  claiming collector lifecycle support.

## Warnings

- `docs/tasks/index.json` is modified in the worktree. It is outside this
  task's write scope: implementers must not stage, amend, or commit it.
- V-01 fail-first evidence must be recorded against a properly supplied unborn
  target; a missing-profile-input failure is not a valid reproducer.

## Stops and next action

- Stops unchanged: changed authority, user-work overlap in allowed paths,
  unsafe permissions, missing decisive capability, or scope expansion into
  collector lifecycle.
- Next action: implement T-004.1 (fail-first V-01 record first, then targeted
  changed cases, then owning modules one command at a time). After
  implementation and any applicable conditional stages, hand to fresh
  `task-review-discovery`, then a separate `task-acceptance-review`.

## Implementer handoff

Status: ready. Scope: narrow changes in `scripts/workflow_version.py`,
`scripts/run_evidence.py`, `scripts/install_development_skills.py` for
installer/identity/availability only, their owning tests, and affected
install/identity guidance in root `README.md`, `skills/README.md`, flow
README. Ownership: all allowed paths clean; preserve dirty
`docs/tasks/index.json` and untracked task packages untouched. Targeted
commands: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p
<test_workflow_version.py|test_run_evidence.py|test_install_development_skills.py>`
(new cases via `-k <name>`); discovery-owned aggregate:
`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest
test_install_development_skills test_workflow_version test_run_evidence` (43/43
green today). Oracle: per-AC above; V-01 fail-first must fail only for the
HEAD/availability defect. Exact next action: record the V-01 fail-first unborn
CLI result, then implement the repair and add only missing unborn boundary
coverage.
