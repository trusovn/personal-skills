# Q-01 maintainability review 01

Fresh independent `task-maintainability-review` of the Q-01 staged submission,
run from the repository's own skill source
(`skills/task-implementation-flow/task-maintainability-review/SKILL.md`).
This reviewer session authored none of the reviewed bytes.

VERDICT: ACCEPT
ARCHITECTURE_GATE: NOT_AVAILABLE

BLOCKERS:
NONE

WARNINGS:

- Duplicated scenario-value knowledge across test owners. The new installed-fixture
  probe in `tests/test_install_development_skills.py` hard-codes baseline scenario
  facts owned by `setup_fixture.py::SCENARIO_BASELINE` (expected second line
  `(100, 'total 102.00')` for the defects variant, `(200, 'total 204.00')` for
  control), while the parallel probe in
  `tests/test_task_maintainability_review.py` only asserts the probe-updated owner
  value and relative divergence. A one-owner baseline change in the fixture
  leaves the fixture test adapting but breaks the installer test's literal
  expectation — an observable one-owner divergence. Non-blocking: these are
  legitimate separate observation boundaries (source-staged fixture versus
  installed package with no repository helpers, per R-04) and the owning suite
  catches the drift. Carry-forward direction: compute expected values from the
  target's scenario module inside the probe instead of hard-coding them.

- Stringly-coupled variant derivation. `setup_fixture.py::test_assets()` builds its
  four variants with `.replace()` on source-literal strings (assertion line,
  `return dict(STANDARD)`, the import line). An edit to `RECEIPT_TEST`,
  `SCENARIO_BASELINE` or `TRANSPORT_TEST` silently no-ops the replacement and
  changes scenario semantics (for example an empty control diff) rather than
  failing loudly. The owning fixture checks detect the resulting shape, so the
  failure mode is caught, but scenario meaning is coupled to fixture prose. This
  technique is new to this module (existing scenarios write files directly).
  Non-blocking; direction: derive variants from a small per-variant diff table
  and assert each replacement actually changed the text.

REVIEWED:

- changed implementation scope: staged Q-01 submission (working tree equals
  index for all reviewed files):
  - `skills/task-implementation-flow/task-maintainability-review/SKILL.md`
  - `skills/task-implementation-flow/task-maintainability-review/evals/evals.json`
  - `skills/task-implementation-flow/task-maintainability-review/evals/files/setup_fixture.py`
  - `tests/test_task_maintainability_review.py`
  - `tests/test_task_flow_guides.py`
  - `tests/test_install_development_skills.py`
  - aligned guides: `README.md`, `skills/README.md`,
    `skills/task-implementation-flow/README.md`
  - `docs/tasks/Q-01/implementation.md` is the submission report and is not a
    reviewed byte; this report does not review itself.
- reviewed-byte identities: SHA-256 of every reviewed file matches the
  identities recorded in `docs/tasks/Q-01/implementation.md` exactly.
- pre-existing dirty work: untracked `.DS_Store` files (root, `docs/`,
  `skills/`); unrelated to this task and not attributed to it.
- architecture command: NONE. This repository declares no canonical
  deterministic architecture command (no `.quality/gates.yaml`, empty `tools/`,
  precedent in `docs/tasks/INT-FLOW-001/results.md`). Per skill protocol no gate
  was created where policy does not require one.
- policy/boundary sources:
  - `AGENTS.md` (repository root)
  - `docs/tasks/Q-01/brief.md` (authority, AC-01..AC-06, R-01..R-04)
  - `docs/tasks/Q-01/preflight.md`, `docs/tasks/Q-01/verification.md` (context)
  - `docs/tasks/INT-FLOW-001/results.md` (no-canonical-gate precedent)

Next route (named, not executed by this review): no `docs/contracts` registry
exists, so the contract-registry stage is absent, not skipped; the first
outstanding stage is a fresh independent `task-review-discovery` (including the
small Q-01 qualification on pre-staged fixtures with held-back oracles),
followed by the separate fresh `task-acceptance-review` decision.
