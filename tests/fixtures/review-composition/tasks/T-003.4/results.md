# T-003.4 Results — Verify composed handoffs and installed source projection

Status: implemented; submission state `READY_FOR_REVIEW`. Every composed
intermediate artifact in this task is fixture data, never observed role
outputs.

## Contract structure (audit)

- Authority: [docs/tasks/T-003.4/brief.md](https://github.com/trusovn/personal-skills/blob/0ad1706cecc6f7d115e510762bf74c58d732cb6a/docs/tasks/T-003.4/brief.md) (SHA-256
  `5834ac29048b28f5cc22e62adf8cbcd2ed0c7b6e104af48cc5aa5e2e90445313`),
  derived `verification.md` (V-01–V-10) and ready `preflight.md` in the same
  package. Reviewed child outputs consumed: T-003.1 `9faec6c`,
  T-003.2 `6bf933c`, T-003.3 `bcd0ad6`.
- New composition record: `tests/fixtures/review-composition/tasks/T-003.4/composition.json` — fixture
  data composed from child-owned cases (CCR-01–08) with records ROUTE-01,
  FIND-01, ROWS-01, REV-01, EFF-01, GATE-01, DISP-01. It references
  child-owned setup instead of copying it and does not rewrite T-002.4
  history.
- Overview routes reconciled with the reviewed child contracts: `README.md`,
  `skills/README.md`, and `skills/task-implementation-flow/README.md` already
  agree on the four conditional combinations, first outstanding stage/full
  remainder, conditional-stage currentness, and production correction
  re-entry (the reviewed T-003.1 output updated them); agreement is asserted
  structurally against the staged route cases, so no stale route/usage entry
  remained to edit.
- Installer declarations inspected: `DEVELOPMENT_SKILL_SOURCES`,
  `PROFILE_SKILLS_README`, and `SHARED_SCRIPT_FILES` stay unchanged — no
  reviewed .1–.3 output renamed, moved, added, or removed a selected skill and
  no shared runtime dependency changed, so no installer synchronization was
  demanded. This repository has no `docs/contracts` registry, so no
  contract-registry stage applies here.
- No plan, task-map, index, or prior task/review artifact was edited.

## Real fixture, filesystem, and Git observations

Exact commands from the repository root:

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_review_composition.py`
  — 16 tests OK (9 predecessor T-002.4 cases preserved + 7 new T-003.4
  composed-handoff cases).
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py`
  — 15 tests OK (14 predecessor cases preserved + 1 new maintainability/
  registry-updater projection case).

Observed behavior behind those commands:

- Child fixture probes were re-exercised in disposable workspaces: the
  implementer `route-cases` staging supplies 19 route cases (INIT-/STATE-/
  CORR- families) whose `Expected submission route:` lines match the composed
  six-row conditional matrix and the currentness/re-entry examples; the
  implementer `record-correction` staging keeps four row states
  (ROW-ORIGINAL passed, ROW-EXACT-BYTES failed, ROW-REMOTE-ANCHOR blocked,
  ROW-REPLAY-BOUNDARY unchecked), and both recorded failed-fix probes of the
  same target still exit non-zero with `AssertionError` while `stop.json`
  preserves two attempts, one target, `non-complete` status, unfinished rows,
  and the `result-integrity owner`; the maintainability `four-blockers`/
  `genuine-stop` staging supplies oracle sections MNT-B1–MNT-B4 (Location,
  Observation, Consequence, Smallest correction direction), the non-blocking
  preference control, and the genuine-stop outstanding-coverage facts; the
  change-effect cases route by actual changed bytes, the genuine reference
  contract probe rejects the boolean revision (exit 0) while the
  executable-reference defect exits non-zero despite its label, and
  `reference-missing-proof` carries no current proof.
- Canonical installer (`scripts/install_development_skills.py`) projected the
  full development profile into a disposable committed Git target twice. The
  `task-maintainability-review` family (including
  `evals/files/setup_fixture.py`) and the `task-contract-registry-updater`
  family are byte-equal to source; the installed profile guide equals
  `skills/README.md` and carries the composed route semantics. On rerun, the
  stale managed file inside the maintainability package disappeared, managed
  bytes were restored, and unmanaged sentinels (`.agents/unmanaged-note.md`,
  `notes/unrelated.txt`) plus the AGENTS text outside the managed block
  survived. Existing preparation/implementer, discovery, and acceptance
  family projection cases remain green and were not duplicated. The active
  repository `.agents/` installation was not refreshed.

## Unrun agent behavior (T-005 handoff)

Separate role calls remain unrun; fixture execution cannot prove semantic
role compliance. T-005 receives:

- Exact setup: the fixture commands in `composition.json` (`python3
  <fixture> <scenario>` with `EVAL_WORK_ROOT`), the installer command
  (`python3 scripts/install_development_skills.py <committed Git target>`),
  and this task's targeted unittest commands above.
- Current source/projected package identities: the affected families are
  `bounded-task-implementer` (T-003.1), `task-maintainability-review`
  (T-003.2), `task-acceptance-review` and `task-review-discovery` (T-003.3),
  plus `task-contract-registry-updater` as the verification-named affected
  family; the installed profile guide is the projected `skills/README.md`.
- Intended producers/consumers: fresh discovery consumes the composed
  evidence; a separate acceptance decision consumes discovery's report;
  later preflight reassesses route/recovery facts; T-005 performs the actual
  producing/consuming role calls.
- Every unrun separate-call boundary with reason and owner is enumerated in
  `composition.json` `t005_unrun_boundaries`: implementer submission mapping,
  conditional stage calls (architecture gate when required, fresh
  maintainability review, registry updater when applicable), fresh discovery
  including the justified aggregate union named in `verification.md`,
  separate acceptance without duplicate execution, correction re-entry,
  revised verification → focused preflight → new decision, mixed
  correction/evidence/authority continuation, and installed-flow
  multi-call qualification.

## Skipped stronger checks and their owners

- The justified affected-module aggregate union
  (`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest
  test_review_composition test_task_flow_guides test_bounded_task_implementer
  test_task_maintainability_review test_task_preflight test_task_review_discovery
  test_task_acceptance_review test_contextual_uncertainty_inputs
  test_contextual_known_issues test_install_development_skills`) was not run
  by the implementer: under plan IF-004 it is owned by fresh discovery after
  the targeted rows/probes are clean.
- No whole-repository, live-network, or model-budget gate was run (excluded by
  the brief); no behavioral qualification of the installed flow is claimed —
  that belongs to T-005.

## Review handoff

Per `review: immediate`, completed bytes are handed to a fresh independent
acceptance reviewer through the applicable conditional stages; the implementer
invocation ends here without a self-issued verdict.