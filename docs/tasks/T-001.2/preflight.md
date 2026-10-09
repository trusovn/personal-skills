# Preflight: T-001.2

Status: ready
Profile: guided
standalone_preflight_value: marginal
Checked: 2026-10-09
Source brief: docs/tasks/T-001.2/brief.md
Source brief revision: supplied ready brief; no explicit revision label declared
Verification design: docs/tasks/T-001.2/verification.md
Verification revision: 1

## Scope and ownership

The brief is an executable leaf (`index.json`) with one dependency: completed
`T-001.1`, whose source contracts are committed (b1b257f "T-001.1 done", preflight
ready). The design's single `Source brief:` declaration resolves to this package's
brief. All material ACs and all three finite-risk rows have derived scenario
coverage (V-01–V-08).

Initial `git status --short` shows no dirty tracked files; only pre-existing
untracked `.DS_Store` entries at repo root, `docs/` and `skills/`, which lie
outside the allowed change area and must be left untouched. No multi-writer or
user-work signal was observed.

Allowed: `skills/task-implementation-flow/task-preflight/` (SKILL.md, references,
evals) plus preflight-specific guide entries in root `README.md`,
`skills/README.md` and `skills/task-implementation-flow/README.md`. The canonical
installer already selects `task-preflight`; no selection, shared-file or new
helper change is expected or authorized. Keep any guide update synchronized and
re-inspect installer constants only if a runtime dependency changes. Read-only:
`.1` sources, official plans/reviews, installed `.agents/` and other stage sources.

## Commands and capability

Python 3.14.4 and local unittest discovery are available without dependency
installation. The owning suite from the brief was run and passes (13 tests,
0.13s), so the environment can execute the required gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-implementation-flow/task-brief-designer/tests -p test_package_resources.py
```

`skills/task-implementation-flow/task-preflight/evals/evals.json` and
`evals/files/setup_fixture.py` exist and support `EVAL_WORK_ROOT`; skill-local
fixture oracles are present. Use a fresh disposable `EVAL_WORK_ROOT` per added
fixture case and never touch a user workspace (setup helpers remove their named
fixture directory).

The brief declares focused new command names UNKNOWN for preflight. Resolving the
exact new targeted test and safe disposable fixture commands is expected
implementation work, not a missing capability: the fail-first source checks and
fixture setup audit are defined by V-01–V-08 and the local test area exists.

## Observable coverage and qualifications

| Scenario | Implementation oracle |
| --- | --- |
| V-01 | Packaged route requires canonical durable `preflight.md`, source-matched verification and per-AC feasibility; inline-only or optional verification cannot be ready; readiness never claims behavior passed. |
| V-02 | Concrete verification defects (missing, foreign source, omitted AC, unjustified scenario, weak oracle) each falsify ready independently; other green evidence cannot close them. |
| V-03 | Feasible absent future test stays ready with planned proof; missing indispensable capability/dependency/permission or inseparable user-work overlap blocks with owner and smallest route. |
| V-04 | Supplied issue/uncertainty variants reassess only relevant known issues; ordinary unknowns stay stated assumptions; serious-delay/costly-later facts resolve from authority first or one focused question; no invented policy. |
| V-05 | Supplied old/new revisions with stable IDs make affected readiness obsolete; focused re-check records current ready without full rediscovery; non-artifact files unchanged. |
| V-06 | Expected implementation/report effects do not force rediscovery; material fact changes require reconsideration; requirement changes route to task design. |
| V-07 | High-assurance identity checks remain strict: separate index/worktree digests, attributed packet-only delta; equal short-status text cannot justify changed non-packet bytes. |
| V-08 | Small direct requests may return inline readiness; supplied package cannot bypass packaged requirements; preflight-specific guides and eval prompts agree with the changed contract. |

V-01–V-03/V-07 cover AC-01/02; V-01/V-04 cover AC-03; V-05–V-07 cover AC-04;
V-01/V-08 cover AC-05. Every scenario is retained; none is claimed passing here.
Deterministic source-contract regressions and fixture setup audits prove
instruction and input facts, not semantic agent behavior. Actual role-call proof
remains with separately authorized `T-005`; broader projection gates with `.4`.

## Context, stops and next action

Skill-workflow maintenance under a human coordinator. Material failure modes:
readiness that ignores verification defects, misroutes missing capability, reuses
obsolete readiness, or applies guided allowances to high-assurance identity
checks. No new product decision or external capability is needed under current
authority; no known-issues file means no recorded deferrals, not a blocker.

Note: `.1` acceptance-review evidence is not recorded in its package; `.1`'s
brief states completed contracts feed `.2`, and `.2`'s preflight does not gate on
`.1`'s acceptance stage. Not a blocker.

Stop on authority ambiguity, inseparable user-work overlap, unsafe permissions,
scope expansion or missing decisive capability. Requirement changes return to
task design; a reasoned coverage revision retains IDs and requests focused
preflight. Ordinary source/test/report effects do not invalidate this readiness.

Standalone inspection resolved routine dependency, fixture, installer and command
facts cheaply; the named route's uncertainty was procedural rather than material.
For materially similar work prefer implementer self-preflight where authority
allows it; this plan section still requires a durable packet for this package.

Implementer handoff:

```text
Next: invoke bounded-task-implementer on docs/tasks/T-001.2/brief.md.
Scope: skills/task-implementation-flow/task-preflight/ plus preflight-specific
  guide entries in root README.md, skills/README.md and skills/task-implementation-flow/README.md.
Command: PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-implementation-flow/task-brief-designer/tests -p test_package_resources.py
Oracle: fail-first source-contract regression and disposable fixture setup audit
  distinguish each V-01..V-08 outcome; owning suite must still pass after targeted checks.
Warnings: leave untracked .DS_Store files; no new helper or shared-file change;
  no installed .agents/ refresh (installer composition is .4's gate).
```
