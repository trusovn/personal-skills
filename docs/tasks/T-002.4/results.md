# T-002.4 results — Close review-flow guidance and local composition

Status: implementation complete; submitted for a fresh independent
`task-acceptance-review` (after applicable conditional stages and discovery).
No installed-flow behavioral qualification or overall completion is claimed by
this document.

## Deliverables

- Composed `ART-009` guidance: the affected functional-review overviews (root
  `README.md`, `skills/README.md`, `skills/task-implementation-flow/README.md`)
  now show applicable prior conditional stages → fresh `task-review-discovery`
  → separate independent acceptance → coordinator recording/authorized
  continuation.
- Minimal discovery stage-name/reference substitutions in affected flow-child
  handoffs: `bounded-task-implementer`, `task-maintainability-review`,
  `task-contract-registry-updater` (the `task-preflight` consumer wording was
  inspected and already agrees with .1–.3; no edit was needed).
- Task-local composition fixture data: [composition.json](composition.json)
  (records COMP-01…COMP-05, inherited case inventory INV-CASE-01…24, explicit
  T-005 unrun boundaries).
- Focused tests: `tests/test_review_discipline.py`
  (`ComposedReviewFlowGuideTests`, `ComposedQualificationSetupTests`) and
  `tests/test_install_development_skills.py`
  (`test_install_projects_acceptance_review_package_and_preserves_unrelated_bytes`).

## Evidence categories (kept distinct)

### 1. Structural tests (byte/route assertions)

- Fail-first run (before guide/fixture changes), repository root:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_review_discipline.ComposedReviewFlowGuideTests tests.test_review_discipline.ComposedQualificationSetupTests tests.test_install_development_skills.DevelopmentSkillInstallerTests.test_install_projects_acceptance_review_package_and_preserves_unrelated_bytes`
  → `Ran 17 tests … FAILED (failures=8, errors=8)`. The 8 errors are the
  eight composition tests rejecting the then-absent composition artifact; the
  8 failure records are the seven route-guide tests rejecting missing
  discovery in the affected guides/sequences/child handoffs and the missing
  `reviews/discovery-01.md` layout reference (the contract-aware sequence test
  contributes two failing subtests); the 2 passing tests are the
  role-reasoning preservation test (four-key task metadata; no launcher
  adapter/fifth key/runtime claim) and the new committed-target
  acceptance-package projection, which passes immediately because `.1`
  already extended installer selection and the projection is byte-exact from
  source. This counting was re-verified during the .4 correction by re-running
  the same command against the pre-.4 sources in a disposable committed
  worktree: 17 tests, 8 failure records, 8 errors, 2 passing tests.
- After implementation, both classes pass: `Ran 16 tests … OK`.

### 2. Actual installer/probe behavior (real boundaries)

- Canonical installer into a disposable committed Git target (committed
  `app.txt`, pre-existing `AGENTS.md` text), repository root:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py`
  → `Ran 14 tests … OK`. The new test byte-projects the whole
  `task-acceptance-review` package (SKILL.md, `references/acceptance-report-template.md`,
  `references/tests-only-reproducer.md`, `evals/evals.json`,
  `evals/files/setup_fixture.py`), then adds an unrelated target file plus a
  stale managed reference and reruns: stale managed bytes are removed,
  unrelated bytes, profile-guide bytes, and AGENTS text (single marked block)
  are preserved. Source identity: `skills/` source; target identity: the
  disposable committed target staged by `init_repo` in the test.
- Real fixture probes (existing predecessor `setup_fixture.py` files, no new
  runner), executed through `ComposedQualificationSetupTests` with
  `EVAL_WORK_ROOT=<disposable work root>`:
  `python3 skills/task-implementation-flow/task-acceptance-review/evals/files/setup_fixture.py <scenario>`
  and the same for `task-review-discovery`:
  - `contextual-risk-blockers-decision` / `contextual-risk-mitigated-decision`:
    a failed risky export truncates `out/ledger.csv` to empty while the
    mitigated control keeps `inv-9001,10.00`; the INV-07 preflight-only
    exposure appears in `docs/tasks/INV-07/preflight.md` and is absent from
    the staged `discovery-01.md` (COMP-01 trace).
  - `mixed-conditions-authorized-decision` / `mixed-conditions-forbidden-decision`:
    staged discovery keeps `JOB-PAIR=blocked`, the pair-claim helper is absent,
    and the authorized/forbidden policies route CHANGES_REQUESTED vs
    INCONCLUSIVE (COMP-02).
  - `discovery-late-omission-clean` / `discovery-late-omission-fail`:
    `python3 -m src.ledger.validate <case>` — boolean-revision exit 2 (clean)
    vs 0 (fail) while older-attempt/second-running stay 2 (COMP-03 validator
    contrast).
  - `known-issue-consumption-decision`, `known-issue-proposed-work-decision`,
    `correction-regression-decision`, `known-issue-priority-only-decision`:
    staged KI-001 record fields; RPT-12B changed-exposure discovery at
    `task-runs/RPT-12B/discovery-01.md`; WEB-02 explicitly unrelated
    (brief-only, no discovery report); RPT-12A unchanged exposure;
    ORD-04 separately scoped KI-001 record; and the priority-only
    follow-up contrast (COMP-04).

### 3. Semantic contract inspection

- The composed guide routes were compared with the settled `.1`–`.3` skill
  bytes: discovery publishes without a verdict and owns justified workflow
  aggregates including correction; acceptance admits the discovery report,
  consumes the aggregate-gate record without re-execution, preserves
  mixed-condition precedence, and routes approved deferrals to the human
  coordinator; preflight reassesses known issues against its task's exposure.
- Role-reasoning guidance stays human guidance: task metadata keeps exactly
  `agent_tier`, `reasoning`, `review`, `budget`; no launcher adapter, fifth
  metadata key, or observed-runtime claim was added.
- `.agents/skills/task-implementation-flow/` (12 files stale vs source) was
  not used, edited, or refreshed; the disposable committed-target fixture
  projects from `skills/` source.

### 4. Unrun agent compliance (explicit gaps — T-005 owns)

No actual skill-call agent produced or consumed these records. Unrun, owned
by T-005 under its separate authorization:

- an actual fresh `task-review-discovery` call over a staged workspace;
- an actual fresh `task-acceptance-review` decision call consuming that report;
- an actual later `task-preflight` call reassessing the KI-001 record against
  relevant/unrelated exposure;
- installed-flow multi-call qualification against the active installation.

## Owning gates (run after targeted evidence was clean)

1. `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_review_discipline.py`
   → `Ran 70 tests in 2.079s … OK` (54 inherited + 16 new).
2. `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py`
   → `Ran 14 tests in 0.947s … OK` (13 inherited + 1 new).

No whole-repo, network, or agent-budget gate was run; none is authorized here.

## T-005 handoff (reusable setup and identities)

- Fixture commands/setup: `python3 skills/task-implementation-flow/<child>/evals/files/setup_fixture.py <scenario>`
  with `EVAL_WORK_ROOT=<disposable work root>`; scenario list and consumer
  mapping in [composition.json](composition.json) (`records`,
  `inherited_case_inventory`).
- Source identities: `skills/task-implementation-flow/task-review-discovery/…`
  and `skills/task-implementation-flow/task-acceptance-review/…` as committed
  at this change; installer projection target identity is the disposable
  committed Git target staged by the installer tests.
- Intended producers/consumers: fresh discovery session → separate acceptance
  decision call → human coordinator recording; later preflight consumes the
  recorded known issues.
- Explicit unrun gaps: the four T-005 boundaries listed above; every
  constructed report/record in `composition.json` is fixture data, never an
  observed role output.