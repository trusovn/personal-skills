# Results: TEST-STAB-001.1 — Assign clear test owners without changing evidence

Status: implementation complete; handed to review (not independently reviewed).

## Baseline (pre-edit, all green, sequential from repository root)

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_review_discipline.py              # 74 OK
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-implementation-flow/task-brief-designer/tests -p test_package_resources.py  # 30 OK
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py      # 14 OK
```

Baseline collected inventory: 74 ids from `tests/test_review_discipline.py`
(9 classes) and 30 ids from `test_package_resources.py` (3 classes), recorded
with scenario/subtest distinctions: the fixture classes carry subprocess
probes (validator exits, export/consumer runs, git index/worktree contrasts)
and subTest distinctions (4 known-issue link statuses, 2 serious-delay
resolutions, 4 repeated-review reasons, 2 prior-retry scripts, per-charge
settlement checks); text checks in contract classes are metadata-only.

## Old-to-new ownership map

Repository modules `tests/test_review_discipline.py` and
`skills/task-implementation-flow/task-brief-designer/tests/test_package_resources.py`
were the two edited sources. All 104 baseline tests map 1:1 to 104 collected
post-move tests; no test was added, dropped, skipped, or discovered twice.

### From `tests/test_review_discipline.py` (74)

| Old class (old owner) | New owner module | New class | Tests |
|---|---|---|---|
| `ReviewerDisciplineTests` acceptance checks (7) | `tests/test_task_acceptance_review.py` | `ReviewerDisciplineTests` | 7 |
| `ReviewerDisciplineTests` senior-review prerequisites (2) | `tests/test_senior_review_discipline.py` | `ReviewerDisciplineTests` | 2 |
| `ReviewDiscoveryDisciplineTests` (12) | `tests/test_task_review_discovery.py` | unchanged | 12 |
| `DiscoveryLateOmissionFixtureTests` (2) | `tests/test_task_review_discovery.py` | unchanged | 2 |
| `AcceptanceAdmissionEvalTests` (2) | `tests/test_task_acceptance_review.py` | unchanged | 2 |
| `ContextualDispositionContractTests` (8) | `tests/test_task_acceptance_review.py` | unchanged | 8 |
| `ContextualDispositionEvalTests` (2) | `tests/test_task_acceptance_review.py` | unchanged | 2 |
| `ContextualRiskFixtureTests` eval-metadata checks (2) | `tests/test_task_acceptance_review.py` | added to `ContextualDispositionEvalTests` | 2 |
| `ContextualRiskFixtureTests` export/consumer probes (6) | `tests/test_contextual_export_risks.py` | `ContextualExportRiskFixtureTests` | 6 |
| `ContextualRiskFixtureTests` uncertainty/mixed-context probes (5) | `tests/test_contextual_uncertainty_inputs.py` | `ContextualUncertaintyFixtureTests` | 5 |
| `ContextualRiskFixtureTests` known-issue/repeated-review probes (6) | `tests/test_contextual_known_issues.py` | `ContextualKnownIssueFixtureTests` | 6 |
| `ComposedReviewFlowGuideTests` (11) | `tests/test_task_flow_guides.py` | unchanged | 11 |
| `ComposedQualificationSetupTests` (9) | `tests/test_review_composition.py` | unchanged | 9 |

The three fixture module names (`test_contextual_export_risks.py`,
`test_contextual_uncertainty_inputs.py`, `test_contextual_known_issues.py`)
are the implementer choices recorded above.

### From `test_package_resources.py` (30)

| Old class | New owner module | Tests |
|---|---|---|
| `PreflightContractTest` (7) | `tests/test_task_preflight.py` | 7 |
| `ImplementerContractTest` (9) | `tests/test_bounded_task_implementer.py` | 9 |
| `TaskBriefDesignerPackageTest` cross-skill checks (11) | `tests/test_task_preparation_contracts.py` | 11 |
| `TaskBriefDesignerPackageTest` designer-local (3) | kept in `skills/task-implementation-flow/task-brief-designer/tests/test_package_resources.py` | 3 |

The mixed tests named in the brief moved as required:
`test_readme_identifies_packaged_resources_as_authoritative` and
`test_decomposition_trigger_requires_boundary_quality_decision` are in
`tests/test_task_preparation_contracts.py`; the two eval-metadata tests
(`test_mixed_evals_explicitly_select_guided_profile`,
`test_optional_link_grading_is_conditional`) are in
`tests/test_task_acceptance_review.py`.

### Preservation evidence

- Assertion bodies, scenario inputs, subTest distinctions, and boundary probes
  are byte-identical to the baseline (moved via AST source-segment extraction;
  only imports, paths, and class organization changed).
- No skip, no mock of a decisive boundary, no relaxed expected failure, no
  duplicate discovery: executed collection bijection 104 → 104, method-name
  multiset identical.
- Validator contrast retained: clean recovery fixture yields
  `{valid: 0, boolean: 2, older-attempt: 2, second-running: 2}`; fail fixture
  yields `{valid: 0, boolean: 0, older-attempt: 2, second-running: 2}` — both
  pass in `test_task_review_discovery.py` (real subprocess probes).
- Index/worktree and git-history contrasts (`git show`, `git diff`, `git
  status` inside disposable fixture repos) unchanged and green in the fixture
  modules.
- Source-parity guard retained in `test_task_review_discovery.py`
  (`test_discovery_fixture_adapts_role_metadata_and_preserves_inherited_scenarios`),
  labeled as structural protection of inherited scenario bytes.
- Designers local suite resolves its package from its own file location
  (`CANONICAL = Path(__file__).resolve().parents[1]`) and imports no
  repository-test helper.

## Verification evidence

Focused runs (fresh invocation per owning module, repository root), all green:

```sh
for m in test_task_acceptance_review test_task_review_discovery test_senior_review_discipline \
         test_task_flow_guides test_review_composition test_contextual_export_risks \
         test_contextual_uncertainty_inputs test_contextual_known_issues test_task_preflight \
         test_bounded_task_implementer test_task_preparation_contracts; do
  PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p $m.py   # OK
done
```

Collected totals per module: acceptance 21, discovery 14, senior 2, flow
guides 11, composition 9, export 6, uncertainty 5, known issues 6, preflight 7,
implementer 9, preparation 11, designer package 3 → 104 collected, 104 passed.

Aggregate and remaining gates, sequential, all green:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests                                                 # 172 OK
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-implementation-flow/task-brief-designer/tests -p test_package_resources.py  # 3 OK
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py            # 14 OK
```

The 172 includes the 104 mapped tests plus the unchanged sibling modules
(installer 14, ollama delegate, run-evidence, runtime-context, workflow-version).

Isolated-cwd checks:

```sh
cd /tmp && PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s /Users/mtrusov/work/skill-sources/personal-skills/tests -p test_task_review_discovery.py   # 14 OK
```

Copied-package check (V-05; pre-move state was 29/30 errors):

```sh
cp -r skills/task-implementation-flow/task-brief-designer /tmp/opencode/stab_copy
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s /tmp/opencode/stab_copy/tests -p test_package_resources.py   # 3 OK
```

Eval-setup independence (V-05): discovery and acceptance `setup_fixture.py`
invoked from an unrelated cwd with only `EVAL_WORK_ROOT` supplied stage their
workspaces (`late-omission`, `contextual-runner`) — no repository helper or
source-checkout cwd required.

## Scope and unchanged surfaces

Changed/added only: the ten owning modules above, the three fixture modules,
`tests/review_fixture_support.py` (import support), the retained
`test_package_resources.py`, `tests/README.md`, and this file. Deleted:
`tests/test_review_discipline.py` (emptied; no forwarding classes).
Source skills/guides, eval JSON/programs, installer, shared scripts, plans,
historical packages/reviews/results, and active `.agents/` are untouched
(their historical command references to the old module names remain history).

## Residual gaps

- Local Git object store is missing the HEAD tree object (`git status` /
  `git diff HEAD` fail); `git diff` (index vs worktree) is clean for
  pre-existing files and shows only this task's surfaces. Out of scope to
  repair; fixture-local git probes are unaffected.
- Best-effort run-evidence instrumentation (`scripts/run_evidence.py`)
  reported `available: false` for the same reason; this invocation recorded
  evidence above directly.
- `.DS_Store` files were not touched.

## Next

Fresh independent `task-review-discovery`, then a separate fresh
`task-acceptance-review` decision, per the brief's follow-on sequence.
