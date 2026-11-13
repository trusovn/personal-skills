# Task Preflight: SIDE-004

Status: `ready`
Profile: guided
standalone_preflight_value: material

## Readiness and decision context

Repository: `/Users/mtrusov/work/skill-sources/personal-skills`.
Source: [brief.md](brief.md), owner-staged 2026-11-13 revision;
[verification.md](verification.md), revision 1. T-005.1 resolves through the
orchestrator's own index to its complete [result](../../../skills/task-orchestrator/docs/tasks/T-005.1/result.md)
and independent [acceptance-02](../../../skills/task-orchestrator/docs/tasks/T-005.1/reviews/acceptance-02.md).
This prerequisite is satisfied; root T-005 is not the dependency.

The staged brief and three untracked .DS_Store files are pre-existing owner work.
Do not edit/stage them. Allowed work is the standalone policy, relevant map
routing, the two source consumers and directly affected eval/reference/profile
documentation. No runtime refactor, AGENTS.md edit, active-install refresh,
dependency provisioning, commit or live eval is authorized here.

Material uncertainty resolved: both consumers already belong to the installer
profile; entire packages and skills/README.md are projected. No membership,
shared helper or installer ownership expansion is needed. Portable consumers
must resolve target-local policy rather than the source repository's policy.
The orchestrator map's default placement wording needs reconciliation, while
its current inventory remains authoritative. Existing code stays untouched.

Implemented contract discovery: docs/contracts/index.json routes to
implementer-feedback, reviewer-feedback, installation and foundation-tools.
Policy consumption is a guidance-contract delta; its registry reconciliation
belongs to the post-maintainability updater. No future decomposition is registered.
No task-local known-issue file or approved deferral was supplied.

## Acceptance feasibility

| Cases | Oracle and feasible evidence | Entry state / permission |
|---|---|---|
| V-01 | AC-01 checklist and local-link review of policy and maps | New document is task-owned; document review pending |
| V-02–V-04 | Concrete source-guided examples in existing eval documentation, traced through both consumers | No provider required; actual agent judgment remains unqualified |
| V-05a/b | Existing no-policy eval targets plus explicit equivalent-policy resolution worked case | No missing-policy blocker or source-policy fallback permitted |
| V-06 | Existing installer suite and disposable install/check/refresh/check preserving policy and sentinel | Python/Git/local filesystem available; temporary targets only |
| V-07 | Focused suite then aggregate, architecture and registry constituents | Project .venv exists; checks do not install dependencies |

Exact focused command: `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -p test_install_development_skills.py`.
Disposable probe uses `scripts/install_development_skills.py <temporary-git-root>`
then `--check <temporary-git-root>` and verifies bytes and source projection.
These are filesystem observations, not semantic compliance proof.

## Starting evidence and native obligations

Measurement: N/A; planned changes are Markdown and eval expectation JSON only.
No Python/runtime/test/fixture/harness code changes are planned; no original
measurement pair or transfer is applicable. Adding supported Python would
require focused readiness reconsideration and pre-edit capture first.

| Native command | Scope / authority | Owner and current duty |
|---|---|---|
| `.venv/bin/python tools/verify.py` | All maintained local suites, architecture, registry and active profile drift; AGENTS.md and docs/development.md | Implementer, after focused success; pending |
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -p test_architecture.py` | Canonical CLEAN static policy | Implementer before handoff; aggregate may cover exact constituent |
| `.venv/bin/python tools/check_contracts.py --root .` | Repository registry structural agreement | Implementer before handoff; aggregate may cover exact constituent; semantic sync later updater |

Current applicability is bound to unchanged brief, verification revision 1,
prerequisite closure, separate owner changes and documentation-only scope.
Expected source/profile changes will produce active installation drift; report
it separately and never refresh that installation. Other failures remain failures.
No new linter, analyzer, review stage or live-eval capability is needed.

## Implementer handoff

Proceed with V-01–V-07 under the scope above. Stop for user-work overlap,
contradictory material authority, runtime redesign, Python scope expansion or a
missing indispensable capability. Final implementation result is READY_FOR_REVIEW;
name applicable maintainability → registry updater → fresh discovery → separate
acceptance without launching those stages from the implementer invocation.
