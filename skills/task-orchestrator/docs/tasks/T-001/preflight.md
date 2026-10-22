# Task Preflight: T-001 — Local runtime investigation

Status: ready
Profile: guided
Standalone preflight value: material — resolved executable/version, ownership and
plan-review freshness; runtime feasibility remains the investigation output.
Source brief: brief.md
Source brief revision: SHA-256 3eaa6df3972c254764c1b92992a52dfdbc832f637abb8c89826ea56a994462c2
Verification: verification.md
Verification revision: 1

## Readiness summary

- Repository: /Users/mtrusov/work/skill-sources/personal-skills.
- Scope: new task-local ART-008 and minimal evidence; brief and official plans unchanged.
- Existing owner work: `?? skills/task-orchestrator/docs/tasks/`, containing brief.md
  only at inspection. New distinct files do not overwrite owner content.
- Accepted plan/map hashes match project-plan-review.md exactly (2026-10-22).
- Python standard library, Git and /opt/homebrew/bin/codex are available.
  `codex --version` reports `codex-cli 0.163.0`; exec help works with a PATH-alias
  permission warning. No dependency install or active-install update is needed.
- No live actor/model, network smoke, notification, project commit, permission
  expansion or run-state mutation. Disposable local fixtures are authorized.

## Decision context

Authority: ../../direction-local-harness.md, ../../local-harness-orchestration-plan.md,
../../local-harness-task-map.json, ../../project-plan-review.md and
../../../references/architecture-map.md. This report feeds T-002..006. False support
could create duplicate writers, false review provenance or unsafe dependency release.
Trustworthy gates outrank progress. No broader runtime qualification is assumed.
Current applicability: same authority/scope; expected report additions do not stale
readiness. A material permission, ownership or scenario change needs focused recheck.

## Acceptance evidence and commands

All commands run from the repository root. All future conclusions allow an explicit
unsupported/unverified disposition under AC-05; unavailable qualification is not an
entry prerequisite for this investigation.

| AC / scenario / risk | Setup / command and oracle | Feasibility / baseline |
|---|---|---|
| AC-01 / V-01 | `codex --version`; `codex exec --help`; inspect adapter | Local executable available; version/help observed; no launch claimed |
| AC-02 / V-02 / R1 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_codex_worker.py -k test_start_persists_thread_and_structured_result`; then owning module if passed | Existing fake executable uses disposable fixtures and real subprocess/files; not run yet |
| AC-03 / V-03 / R2 | Read controller_state.py, flow-profile.schema.json and installed CLI help; `codex sandbox --help` | Local source/help available; actual denied-write proof may remain pending |
| AC-04 / V-04 / R3 | `PYTHONDONTWRITEBYTECODE=1 python3 skills/task-orchestrator/docs/tasks/T-001/probe_local.py` (future task-owned fixture) | Standard library and disposable Git objects feasible; integrated finalization remains downstream |
| AC-04 / V-05 / R3 | Inspect CLI notification interface and existing operator guide | No actual notification allowed; record exact delivery-proof gap |
| AC-05 / V-06 | Report maps V-01..06 and R1..3 to sources/results/gaps | Feasible documentary trace; aggregate gate belongs to fresh reviewer |

## Warnings, stops and next action

Stop for authority conflict, owner overlap, production/shared changes, permission
expansion or unauthorized live/billable probes. Missing runtime support must be
reported rather than implemented around. Recommend standalone preflight for the
next similar capability investigation because ownership and runtime facts can change.

## Implementer handoff

Consume brief.md plus verification revision 1 under this scope. Run the focused
transport case first, then the existing owning module; inspect the installed local
interface and publish harness-contract.md plus reproducible task-local evidence.
Do not modify live run records for optional instrumentation: task scope forbids it.
Finish at READY_FOR_REVIEW and hand off to fresh task-review-discovery, then a
separate task-acceptance-review decision. No registry or executable change is planned.
