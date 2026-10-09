# Preflight: T-001.3

Status: ready
Profile: guided
standalone_preflight_value: material
Checked: 2026-10-09
Source brief: docs/tasks/T-001.3/brief.md
Source brief revision: supplied ready executable brief at HEAD ae7f94e
Verification design: docs/tasks/T-001.3/verification.md
Verification revision: initial supplied ready design, V-01–V-08; no explicit revision label

## Readiness, scope and ownership

The package is an executable leaf. Its verification's Source brief declaration
resolves to this brief, and all AC-01–AC-04 and E-01–E-03 have scenario coverage.
The user confirmed in this preflight invocation that T-001.1 and corrected
T-001.2 were both independently accepted. This resolves the apparent conflict
between the predecessor “done” commits and T-001.2's retained pending-review
handoff. Commit labels alone were not treated as review evidence.

Initial status: `?? docs/tasks/T-001.3/verification.md`. This is pre-existing
user work and a read-only derived input. No tracked ownership overlap or
declared multi-writer signal was found. This invocation creates only this packet.

Allowed implementation: `skills/task-implementation-flow/bounded-task-implementer/`,
its eval definitions/setup, focused entry/evidence tests in the flow test area,
and implementer-specific entries in `README.md`, `skills/README.md` and
`skills/task-implementation-flow/README.md`. The closest test area is
`skills/task-implementation-flow/task-brief-designer/tests/test_package_resources.py`.
Preserve other roles, predecessor contracts, plans, installed `.agents/`,
review provenance, optional evidence rules and strict high-assurance checks.
No implementation, installation, tracker update or reviewer launch is authorized
by this preflight result.

The canonical installer already selects bounded-task-implementer, manages
`skills/README.md`, and lists the existing shared evidence/runtime helpers.
No new selection or runtime dependency is needed. Re-inspect and synchronize
the installer if implementation discovers a real managed dependency change;
scope growth returns to task design.

## Commands and capability

Working directory for commands: repository root.
Python, unittest, Git and disposable local fixture setup are available.
The focused predecessor baseline ran successfully: 7 tests, 1.167 seconds.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-implementation-flow/task-brief-designer/tests -p test_package_resources.py -k PreflightContractTest
```

For new focused entry/evidence checks, add an `ImplementerContractTest` group in
the existing test file, then run this targeted command before the owning suite:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-implementation-flow/task-brief-designer/tests -p test_package_resources.py -k ImplementerContractTest
```

This group does not exist yet. The command is prospective, not a baseline pass;
require a nonzero discovered test count and fail-first rejection of the old
optional-entry/incomplete-evidence contract before the production correction.
Its absence is feasible task-owned future work, not a missing capability.
If another test structure is selected, record the replacement exact command.

Owning suite, only after targeted checks pass:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-implementation-flow/task-brief-designer/tests -p test_package_resources.py
```

The owning suite was not run here. Both commands are cheap local source/fixture
checks; neither establishes actual agent compliance.

Existing fixture setup entry point is
`skills/task-implementation-flow/bounded-task-implementer/evals/files/setup_fixture.py`.
It supports EVAL_WORK_ROOT and deletes its named fixture directories, so always
use a fresh disposable root. For example, this unrun setup command safely
prepares the existing guided input for inspection:

```sh
task_fixture_root=$(mktemp -d /private/tmp/t0013-fixtures.XXXXXX)
EVAL_WORK_ROOT="$task_fixture_root" PYTHONDONTWRITEBYTECODE=1 python3 skills/task-implementation-flow/bounded-task-implementer/evals/files/setup_fixture.py api-guided
```

The existing api-guided eval admits a package without preflight; this is an
expected task defect to correct, not a valid-entry oracle. New fixtures must
supply valid ready preparation and each faulty input explicitly. Have the
focused fixture tests invoke setup in temporary directories and inspect actual
contents; do not run setup against `/work` or a user workspace. No dependency
installation, network, live model call or optional evidence lifecycle is needed
for these checks. Budgeted agent calls require separate authorization.

## Scenario oracles and proof limits

| Scenario | Required local observation |
| --- | --- |
| V-01 | Source permits supplied applicable ready leaf, binds authority/scope/verification and checks bounded facts; a feasible absent future test does not block. |
| V-02 | Actual faulty fixtures cover every missing, blocked, stale, foreign-source/revision/scope, composite, blocked-design and legacy input; source stops entry and names the earlier owner, including conversational relabeling. |
| V-03 | Before/after fixtures separately distinguish expected implementation/report effects from dependency, ownership, permission, capability and authority changes; source continues or routes affected readiness accordingly. |
| V-04 | Explicit reasoned verification revisions retain IDs; old/current/old ready references yield reject/permit/reject under the applicability contract. |
| V-05 | Supplied ledger accounts for every scenario and material AC, actual pass/fail results, setup/command/oracle, blocked/unchecked reasons and next owners, context reference and remaining obligations; no acceptance claim. |
| V-06 | Green partial evidence exposes omitted negative scenarios/ACs and evidence from obsolete revisions or changed bytes; gaps remain explicit until current proof is supplied. |
| V-07 | Supplied direct/guided/high-assurance contrasts preserve compact direct checks, optional versus required instrumentation, exact strict freshness and existing review/targeted-fix stops. |
| V-08 | Implementer-specific guides, eval prompts/expectations and actual prepared fixtures agree with V-01–V-07; inspect installer dependencies and preserve all existing legacy/provenance regressions. |

These observations establish source and fixture contracts only. Actual
edit/no-edit and continuation compliance remains unrun T-005 work. Full
cross-stage source/profile projection is T-001.4-owned. Do not substitute
schema/syntax checks, fixture names or aggregate green results for these oracles.

## Context, stops and next action

Context authority: `docs/project-plan.md`, sections 1, 4–7 and 10–11;
`docs/task-map.json`; `docs/tasks/T-001/brief.md`. This source maintenance leaf
protects packaged entry and current submission evidence for later review and
installed T-005 qualification. Premature package edits and omitted/stale
scenario evidence are the material failure consequences. T-001.4 composes the
sources; T-002/T-003 own wider review/correction routes. No known-issues file was
found under docs; this does not assert that no defects exist. No unresolved
product decision or missing indispensable capability was identified.

Standalone preflight added material value by resolving reviewed-predecessor
eligibility through the coordinator and distinguishing the stale guided eval
input from the valid ready fixture that implementation must supply. Recommend
standalone preflight for similar dependent packages with ambiguous completion
evidence; packaged preparation is required by this plan regardless of value.

Stop on user-work overlap, invalid entry, ambiguous authority, unsafe permission,
scope growth or missing decisive capability. Material prerequisite/authority or
verification changes require affected renewed readiness; expected task/report
effects alone do not stale this guided decision. Exact high-assurance checks
remain separate and strict. Do not refresh installed skills during this call.

Next: invoke bounded-task-implementer on `docs/tasks/T-001.3/brief.md`, consuming
this packet and the supplied verification design. Map V-01–V-08 before editing,
establish fail-first targeted source/fixture evidence, implement within scope,
then run targeted and owning checks. Finish at READY_FOR_REVIEW with a handoff
to a fresh task-acceptance-review, retaining any applicable conditional stages;
the implementer must end its invocation without launching that review.
