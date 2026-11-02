# Task Preflight: SIDE-001

Status: `ready`
Profile: guided
standalone_preflight_value: marginal

## Readiness summary

Source brief: docs/tasks/SIDE-001/brief.md
Source brief revision: SHA-256 `c96ccd82e10577e69bbdf18c2e6046708debe2c3a0d01636ef5776d60074c731`
Verification: docs/tasks/SIDE-001/verification.md
Verification revision: 1
Repository: /Users/mtrusov/work/skill-sources/personal-skills

The starting working tree was clean. Authority, paths, Python standard-library
suite and document-review oracles are routine. No overlapping user work or
required external dependency was found. Expected implementation/report edits do
not stale this readiness; changed authority, permissions or verification do.

Scope: verification-designer source instructions/evals, relevant existing tests
and directly affected guidance only. Preserve existing task artifacts, including
T-001.2 verification, and the active .agents installation. No live/model eval,
network, dependency installation, commit or destructive action is authorized.

## Decision context

The brief prioritizes readable cases with unchanged assurance. The main risk is
losing a distinct obligation while removing presentation boilerplate. Required
consumers are preflight and implementation; inspected consumer fixtures rely on
Source brief declarations and coverage, not an opening Testing approach table.
The installer maps this existing skill directory and copies its bytes. Its
source mapping, shared-script list, profile guide and README installation
references do not require changes for presentation alone. No runtime/plan
contract change is expected. See docs/project-map.md, docs/development.md and
docs/contracts/installation.json. Live generated behavior remains unqualified
unless a separate budget is approved; this is an evidence limit, not a reason
to block the bounded instruction edit.

## Acceptance evidence and commands

All commands run from the repository root.

| AC / scenario | Authority / setup and oracle | Feasibility and current evidence |
|---|---|---|
| AC-01–AC-04 / V-01 | Brief presentation; review a lifecycle example for case-first order, local methods, metadata last and absence of generic handoff/readiness text | Feasible document review; future example not yet reviewed |
| AC-02, AC-05 / V-02 | Existing lifecycle fixture and eval; trace every required boundary/refusal/resume obligation and exact result | Fixture/eval present; no live execution authorized; future example review pending |
| AC-05 / V-03 | Source/consumer diff and protected bytes; focused preparation suite, architecture and contract checks | Python/Git and local files available; no ownership conflict |

`python3 -B -m unittest discover -s tests -p test_task_preparation_contracts.py`
passed: 13 tests. This is a structural baseline, not generated-output proof.
Required final checks:
`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py`
and `python3 tools/check_contracts.py --root .`.
Run `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py`
if managed resources/references change. No broader baseline is needed.

## Warnings, blockers, and next action

No blocker. Stop if an assurance obligation must be removed or existing task
artifacts must be rewritten. Structural checks cannot qualify model behavior.
Standalone preflight added little here; for a similar unpackaged edit use the
implementer's compact self-check. Packaged tasks still require this stage.

## Implementer handoff

Implement docs/tasks/SIDE-001/brief.md against verification revision 1 within the
scope above. Update existing coverage instead of creating a parallel harness;
review the example and retain explicit evidence limits. Run the focused suite,
then architecture and contract checks. Record results beside the brief. Finish
applicable conditional stages, fresh independent task-review-discovery, then a
separate task-acceptance-review decision.
