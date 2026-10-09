# Preflight: T-001.1

Status: ready
Profile: guided
standalone_preflight_value: marginal
Checked: 2026-10-09
Source brief: docs/tasks/T-001.1/brief.md
Source brief revision: supplied ready brief; no explicit revision label declared
Verification design: docs/tasks/T-001.1/verification.md
Verification revision: 1

## Scope and ownership

The brief is an executable leaf with no prerequisites. Its cited project plan
and composite parent confirm this leaf's source-contract ownership. The design's
single Source brief declaration resolves to this package's brief. All material
ACs and both finite-risk rows have derived scenario coverage.

Initial `git status --short` was empty. No dirty overlap or multi-writer signal
was observed. Implementation may change only the two source packages
`skills/task-implementation-flow/task-brief-designer/` and
`skills/task-implementation-flow/task-verification-designer/`, plus their
stage-specific entries in root `README.md`, `skills/README.md` and
`skills/task-implementation-flow/README.md`. Installed `.agents/`, other stages,
official plans and historical reviews remain read-only.

The canonical installer selects both source packages, projects `skills/README.md`,
and has an explicit shared-script list. No selection or shared-helper change is
needed for the stated work. Keep guide updates synchronized; any newly required
runtime dependency requires immediate installer synchronization or scope routing.
Installer composition proof remains T-001.4. No install refresh is authorized.

## Commands and capability

Run from `/Users/mtrusov/work/skill-sources/personal-skills`. Python unittest and
local Git fixture creation are available without dependency installation.

The existing focused baseline passed (one test):

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-implementation-flow/task-brief-designer/tests -p test_package_resources.py -k test_optional_verification_design_is_discoverable
```

Add the focused regression method `test_packaged_preparation_contract` to the
existing `TaskBriefDesignerPackageTest`, then run this exact targeted command:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=skills/task-implementation-flow/task-brief-designer/tests python3 -m unittest test_package_resources.TaskBriefDesignerPackageTest.test_packaged_preparation_contract
```

The new method does not exist yet. This is expected implementation work, not a
missing capability. Preserve an assertion failure against the current optional
route and inadequate coverage/revision contract, then a pass after source edits.
A missing-method error is not fail-first evidence. The test must distinguish
the V-01–V-07 source obligations below, rather than merely parse artifacts.

After targeted checks pass, run the owning suite:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-implementation-flow/task-brief-designer/tests -p test_package_resources.py
```

The existing verification fixture's `lifecycle` setup was run in a fresh temporary
`EVAL_WORK_ROOT`. It successfully created a clean Git repository with the actual
brief, cited import policy, three ACs and no verification output. Temporary data
was removed. This proves local setup capability only. For each added fixture case,
use a new disposable root and the setup's declared scenario argument, for example:

```sh
EVAL_WORK_ROOT="$(mktemp -d /private/tmp/T-001.1-eval.XXXXXX)" PYTHONDONTWRITEBYTECODE=1 python3 skills/task-implementation-flow/task-verification-designer/evals/files/setup_fixture.py lifecycle
```

Inspect the generated inputs and expectations for each new case. Never use an
existing user workspace: setup helpers remove their named fixture directory.
The brief-designer sibling helper uses the same environment contract and local
Git setup. Extend these skill-local fixtures; do not add a shared harness.

## Observable coverage and qualifications

| Scenario | Implementation oracle |
| --- | --- |
| V-01 | Both executable package routes require verification then ready preflight; conversational edits retain inline checks; supplied documentation package cannot bypass preparation. |
| V-02 | Actual composite, blocked-design and legacy inputs identify rejection and correct next owner. |
| V-03 | Valid and contrasting fixtures expose complete AC coverage, unsupported obligations, omitted AC despite green evidence and a weak oracle; source rules close authority in both directions. |
| V-04 | Actual preserved verification files cover missing, malformed, duplicate and foreign source declarations, plus a valid control; expectations require unchanged conflicting content. |
| V-05 | Supplied unchanged brief, revision-1 scenarios, readiness and evidence support reasoned revision, stable IDs, affected invalidation and focused renewed preflight. |
| V-06 | Actual changed-result and unresolved-decision inputs route to task design rather than scenario repair. |
| V-07 | Scoped diff and stage-specific guides preserve sizing, decomposition, ownership, compact artifacts and independent review; installer inspection introduces no hidden dependency. |

V-01/V-02/V-07 cover AC-01/04 and D-01. V-03/V-04 cover AC-02;
V-05/V-06 cover AC-03, with V-03–V-06 covering D-02. Every scenario is retained.
No implementation scenario has been claimed passing by this preflight.

Deterministic regressions prove instruction contracts; fixture inspection proves
supplied starting state. Neither proves semantic agent compliance or actual
overwrite protection. Behavioral invocation and composed recovery qualification
remain with separately authorized T-005. No model-budget eval, broader projection
gate or whole-repository suite ran.

## Context, stops and next action

This is a human-coordinated skill workflow maintenance task. The material failure
is allowing packaged implementation with incomplete or authority-changing
verification, or reusing obsolete readiness/evidence. Later leaves consume this
source contract; do not change their enforcement here. No new product decision,
known-issue dependency or external capability is needed under current authority.

Stop on authority ambiguity, inseparable user-work overlap, unsafe permissions,
scope expansion or missing decisive capability. Requirement changes return to
task design; a derived coverage repair retains IDs and requests focused preflight.
Ordinary source/test/report effects do not alone invalidate this readiness result.

Standalone inspection resolved routine source/profile and fixture facts. Prefer
implementer self-preflight for materially similar work when governing authority
allows it; this plan still explicitly requires separate durable preflight.

Implementer handoff:

```text
Next: invoke bounded-task-implementer on docs/tasks/T-001.1/brief.md.
Use verification revision 1, V-01–V-07, and this ready guided preflight.
Add the named focused regression and capture a genuine assertion failure before
changing source contracts. Then pass the targeted command, inspect every new
disposable fixture's inputs, and run the owning package suite.
Keep T-001.4 projection and T-005 behavioral qualification visibly unrun here.
After implementation/correction, end the implementer invocation and hand the
completed bytes to fresh independent acceptance through the required route.
```
