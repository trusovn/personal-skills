# Repository test ownership and commands

Owners and focused selectors for the preparation/review-flow regression tests.
All commands run from the repository root with `PYTHONDONTWRITEBYTECODE=1`
unless noted; each module passes alone in a fresh invocation. The aggregate
selector covers the mapped union plus the remaining designer suite, then the
unchanged installer suite, sequentially.

Shared support: `tests/review_fixture_support.py` holds the repository root,
the acceptance/discovery package paths, and the `normalized`/`fixture_functions`
text helpers used by several owning modules. Skill eval setup programs remain
self-contained and never import repository-test helpers.

| Module | Owner (purpose) | Fixture dependency |
|---|---|---|
| `test_task_acceptance_review.py` | Acceptance admission, contextual disposition contract, and decision-eval metadata | `task-acceptance-review` skill, report template, `evals/evals.json`, and `evals/files/setup_fixture.py` scenarios |
| `test_task_review_discovery.py` | Discovery contract, inherited acceptance/discovery fixture parity, late-omission validator probes | `task-review-discovery` skill, report template, both discovery/acceptance `evals.json` and setup fixtures |
| `test_senior_review_discipline.py` | Senior-review mandatory reference-read prerequisites | `senior-code-review` skill |
| `test_task_flow_guides.py` | Composed flow-guide checks: discovery before a separate acceptance decision | root/profile/flow READMEs, implementer/maintainability/registry-updater/designer skills, implementer evals |
| `test_review_composition.py` | T-002.4 composition evidence: fixture data, inherited case inventory, T-005 unrun boundaries | `docs/tasks/T-002.4/composition.json`, acceptance/discovery/preflight evals and fixtures, `docs/task-map.json` |
| `test_contextual_export_risks.py` | Export/consumer risk fixture probes (destructive/mitigated export, consumer contract, duplicated parsing) | acceptance `setup_fixture.py` export scenarios |
| `test_contextual_uncertainty_inputs.py` | Uncertainty/mixed-context input fixture probes (readiness-only exposure, mixed conditions, retention/region) | acceptance `setup_fixture.py` uncertainty/mixed scenarios |
| `test_contextual_known_issues.py` | Known-issue/repeated-review fact fixture probes (record fields, regression, repeated-review reasons) | acceptance `setup_fixture.py` known-issue/repeated-review scenarios |
| `test_task_preflight.py` | Preflight stage contract and packaged durable output | `task-preflight` skill, evals, `evals/files/setup_fixture.py` scenarios |
| `test_bounded_task_implementer.py` | Bounded-task-implementer entry contract and evaluation fixtures | `bounded-task-implementer` skill, evals, `evals/files/setup_fixture.py` scenarios |
| `test_task_preparation_contracts.py` | Cross-skill preparation, resource, and legacy-path checks | `task-brief-designer` package resources, verification-designer/preflight/implementer skills and evals, `skills/**` path hygiene |
| `skills/task-implementation-flow/task-brief-designer/tests/test_package_resources.py` | Brief designer's own packaged resources and authoring route; resolves the package from its file location | designer package `references/` only |

Focused commands (one fresh invocation per owning module):

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_task_acceptance_review.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_task_review_discovery.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_senior_review_discipline.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_task_flow_guides.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_review_composition.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_contextual_export_risks.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_contextual_uncertainty_inputs.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_contextual_known_issues.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_task_preflight.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_bounded_task_implementer.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_task_preparation_contracts.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-implementation-flow/task-brief-designer/tests -p test_package_resources.py
```

Aggregate (mapped union plus remaining designer suite, then the unchanged
installer suite, sequentially):

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-implementation-flow/task-brief-designer/tests -p test_package_resources.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py
```

All selectors require no inherited cwd beyond the repository root shown above;
an unrelated starting directory works when the `-s` path is absolute, e.g.
`python3 -m unittest discover -s /path/to/personal-skills/tests -p test_task_review_discovery.py`.

The old mixed modules `tests/test_review_discipline.py` and the preflight/
implementer contract classes in `test_package_resources.py` were relocated with
assertions, inputs, and failure signals unchanged; see
`docs/tasks/TEST-STAB-001.1/results.md` for the old-to-new evidence map.
