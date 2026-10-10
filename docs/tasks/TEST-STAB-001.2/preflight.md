# Preflight: TEST-STAB-001.2 — Consolidate test setup and incidental assertions

Status: **ready** (guided)

`standalone_preflight_value: material` — resolved two genuinely uncertain and
late-costly facts: the current runnable baseline together with correctness of
the brief's aggregate and isolated commands, and a pre-existing Git object-store
corruption that breaks `git status`/`git diff HEAD` and therefore changes how
ownership and any diff-based review must be established. The brief-named
standalone route was validated from current repository state, not merely
accepted.

## Verification-design resolution

`docs/tasks/TEST-STAB-001.2/verification.md` — `Source brief:` resolves to this
package's `brief.md`; declared brief SHA-256
`4ae8ce1d11be7f1ac484f1afae108a0e9a390ba97687aaa6df5bbede913f3389` matches
current brief bytes. Treated as derived guidance under the brief, not as
requirements authority. Scenario IDs V-01–V-08 preserved; none blocked.

## Confirmed scope and ownership

- Authority: parent brief (`../TEST-STAB-001/brief.md`), user request, root
  `AGENTS.md` and active project-local `testing-discipline`. Branch
  `t-o-new-flow`. Leaf is `executable` with `Status: ready`; parent
  TEST-STAB-001 is decomposed and must not be launched.
- Dependency: TEST-STAB-001.1 accepted per commit `fc295da` ("task
  TEST-STAB-001.1 done (accepted)"); its fixed owner/evidence map is present at
  `docs/tasks/TEST-STAB-001.1/results.md`. Keep its ownership decisions fixed.
- Intended change surfaces: the `.1` contextual/composition fixture modules, a
  small repository-only support module under `tests/`, the relocated
  preparation-contract test, `tests/README.md`, and new evidence in this leaf.
  The helper may encapsulate temporary-workspace lifecycle, environment and
  setup subprocess execution repeated in `ContextualRiskFixtureTests.stage` and
  `ComposedQualificationSetupTests.stage`; scenario choices, paths, data and
  assertions stay with the tests.
- Read-only: all skill eval generators/JSON, source guidance/references,
  installer, shared scripts, installation docs, active installation, official
  planning and all prior task packages/reviews/results including `.1`'s map.
- Ownership result: no user-work overlap. `git diff-files` (index vs worktree)
  is clean for tracked files; untracked entries are the prior-stage
  `docs/tasks/TEST-STAB-001.2/verification.md` and `.DS_Store` noise. Do not
  edit `brief.md`, `verification.md`, or any `.1` artifact.

## Targeted commands and observable oracles

All commands run from repository root with `PYTHONDONTWRITEBYTECODE=1`.

Focused first gates (each green now, one fresh invocation per module):

```sh
python3 -m unittest discover -s tests -p test_contextual_export_risks.py            # 6 OK
python3 -m unittest discover -s tests -p test_contextual_uncertainty_inputs.py      # 5 OK
python3 -m unittest discover -s tests -p test_contextual_known_issues.py            # 6 OK
python3 -m unittest discover -s tests -p test_review_composition.py                 # 9 OK
python3 -m unittest discover -s tests -p test_task_preparation_contracts.py         # 11 OK
```

Aggregate mapped union (verified now — 101 tests OK):

```sh
PYTHONPATH=tests python3 -m unittest test_task_acceptance_review test_task_review_discovery \
  test_senior_review_discipline test_task_flow_guides test_review_composition \
  test_contextual_export_risks test_contextual_uncertainty_inputs \
  test_contextual_known_issues test_task_preflight test_bounded_task_implementer \
  test_task_preparation_contracts
```

Closure gates:

```sh
python3 -m unittest discover -s skills/task-implementation-flow/task-brief-designer/tests -p test_package_resources.py
python3 -m unittest discover -s tests -p test_install_development_skills.py
```

Independent-package boundary (V-07; verified now, unrelated cwd, `-I`, no
`PYTHONPATH` supplied):

```sh
EVAL_WORK_ROOT="$WORK" python3 -I skills/task-implementation-flow/task-acceptance-review/evals/files/setup_fixture.py <SCENARIO>
EVAL_WORK_ROOT="$WORK" python3 -I skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py <SCENARIO>
```

Verified this run: `contextual-risk-mitigated-decision` → rc=0, stages
`contextual-runner` and `task-runs`.

Oracles per acceptance criterion:

- AC-01: distinct per-invocation `TemporaryDirectory` roots, no state survival
  after cleanup, setup failure surfaces scenario + subprocess exit/stderr.
- AC-02: two canonical public CLI probes with malformed invoices and a seeded
  ledger — nonzero exit plus empty (risky) vs preserved (mitigated) bytes;
  composition keeps COMP-01 preflight-only exposure, report omission and
  decision obligations.
- AC-03: `test_packaged_preparation_contract` line 168 newline coupling —
  whitespace reflow passes; missing/reversed stages fail for the intended
  assertion.
- AC-04: every `.1` evidence-map row has an owner or justified consolidation in
  a new `docs/tasks/TEST-STAB-001.2/results.md` delta map.
- AC-05: aggregate union, designer suite and installer suite pass; copied eval
  setup runs without source/test-helper access.

## Capability result

`tests/review_fixture_support.py` exists as the shared repository-test support
root; a new adjacent helper module is available for the staging operation. Source
skill eval setup fixtures support the `contextual-*` scenarios used by the
contextual owners and composition tests.

## Warnings (not blockers)

1. Local Git object store is missing the HEAD tree object: `git status`,
   `git diff HEAD` and `git show HEAD` fail. This is pre-existing and already
   recorded in `.1/results.md` residual gaps. Determine changes via explicit
   path lists plus `git diff-files` and `git ls-files --others`. If any
   downstream review or commit stage requires a HEAD-relative diff, escalate as
   environment; repair is out of scope here.
2. `.1` publishes only `reviews/discovery-01.md`; there is no formal acceptance
   review artifact, though `results.md` self-declares "not independently
   reviewed" and the commit marks it accepted. Treat `.1` as accepted authority
   per the brief and commit; the missing artifact is a process gap only.
3. The active `.agents/` acceptance fixture is a divergent older copy (rejects
   `contextual-*`), while tests target the `skills/` source path. Active
   installation is read-only and out of scope; do not refresh or "fix" it here.

## Implementation stops

Stop for a red baseline, unknown surviving failure oracle, changed scenario
meaning, cross-skill packaging need, production-contract change, or user-work
overlap. Do not weaken the inherited source-parity guard, repair unfinished
T-004 features, edit `brief.md`/`verification.md`/`.1` artifacts, or add a
configurable fixture framework or shared mutable staged state.

## Standalone value and next action

The standalone stage added enough value to recommend it for the next materially
similar task: it surfaced the Git-corruption constraint and confirmed the exact
current selectors and baseline before any edit.

Next: `bounded-task-implementer` on `docs/tasks/TEST-STAB-001.2/brief.md` —
confirm the baseline above, apply the three bounded cleanups within `tests/` and
`tests/README.md`, maintain the delta map in a new
`docs/tasks/TEST-STAB-001.2/results.md`, then run focused gates → aggregate
union → designer suite → installer suite, followed by fresh
`task-review-discovery` and a separate `task-acceptance-review`. No T-003–T-005
acceptance criterion is satisfied by this cleanup.
