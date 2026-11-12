# T-004.1 preflight

Status: `ready`
Profile: `guided`
standalone_preflight_value: `material`

## Readiness summary

- Source: [brief.md](brief.md), revision 1, ready executable leaf; derived
  [verification.md](verification.md), revision 1, declares this exact source.
- Repository: `/Users/mtrusov/work/skill-sources/personal-skills`.
- Dependency: T-003 [acceptance-02](../T-003/reviews/acceptance-02.md) is ACCEPT;
  consume its [controller contract](../T-003/controller-contract.md).
- Allowed implementation: existing controller/Git/verification/state modules,
  affected schemas, focused tests and directly affected runtime references inside
  `skills/task-orchestrator/`, plus the task-local producer handoff. Collection,
  acceptance/completion, generic backends, automatic repair/install, plan edits,
  commits and active-install refresh are excluded.
- Pre-existing work: modified `skills/task-orchestrator/docs/tasks/index.json`
  and untracked T-004, T-004.1 and T-004.2 packages. Preserve these inputs; only
  this new canonical readiness file is added here. Runtime/test paths are clean.
- Permission envelope: local disposable Git/filesystem/process checks permitted;
  no live provider, network, package installation or real sbx qualification.
  Privileged or expensive checks require their applicable approval.
- Material uncertainty resolved: the frozen version-2 policy requires exactly
  `execution_authorization = {"transport":"sbx","yolo":true,"intervention":"active_chat"}`
  (`controller_state.validate_run_policy`). The existing verification runner takes
  only a permission envelope and unconditionally calls `build_sandbox_invocation`.
  Adding the brief-authorized explicit policy projection is feasible in these
  owners; platform detection or sandbox failure must never authorize it. Legacy
  permission validation and refusal remain independent obligations.
- Current applicability: revision-1 scope and verification are coherent with the
  accepted predecessor. No runtime implementation changed during preflight.
  Repeat focused readiness if authority, ownership, required capability or scope
  changes. Future candidate/check tests are planned proof, not passing evidence.

## Decision context

The [owner direction](../../direction-single-task-sbx.md) prioritizes one prepared
human-reviewed task on an owner-supplied sbx/separate branch with YOLO actors.
Outer isolation is an assumption, not an enforcement claim. T-004.2 needs a single
candidate/check producer and fresh-rerun interface; T-005 owns acceptance and
completion; T-006 owns real sbx/provider qualification. Incorrect identity or
replay can falsely admit changed work or launch overlapping processes. Mitigations
are actual file identities, pre/post checks, existing lock/no-relaunch records,
retained history and explicit mechanism authority.

Current capability discovery: `docs/contracts/index.json` →
`docs/contracts/task-orchestrator.json` → architecture map and executable owners.
ART-003/005 and candidate/check IF-003 are planned additions, not current capability.
T-003 admits preflight only; implementation output is a bound raw claim. Extend
its existing lifecycle path rather than inventing a second admission authority.
T-003 acceptance records legacy platform failures/skips and unrun live proof;
these do not waive this task's required local evidence. No new deferral is made.

## Acceptance evidence and commands

All rows derive from brief AC-01–05 and verification revision 1. Commands run
from the repository root. For each named test module below, use:
`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p <module>`.
Existing fixtures require only Python, Git, disposable directories and local
child processes; those capabilities were exercised successfully below.

| Coverage | Boundary and decisive oracle | Owner / feasible proof command | Current evidence / gap |
|---|---|---|---|
| AC-01; V-01, V-02a–d | Real terminal actor followed by actual tracked/untracked inspection; independently compare bytes, scope and unchanged dirty owner work; distrust summary | `test_actor_operations.py`, `test_controller_git.py`, `test_controller.py` | Actor helper executes local fake Codex, actual tools/dependency/skill and implementation; Git dirty/rename/delete/unusual-path helpers exist. New producer proof not run. |
| AC-01/02/04; V-03a–f | Invalid run/task/operation/authority and live/unknown/check contention refuse without launch or authoritative mutation; real competing processes use same lock | `test_actor_operations.py`, `test_controller.py` | Existing reservation/launch/reload/interrupt fixtures reusable; new candidate/check guards not run. |
| AC-02; V-04a–e, V-05a–c | Real tracked, untracked, config, task-input and evaluated ignored-input drift; same-size byte change removes current eligibility while irrelevant generated output preserves it | `test_controller_git.py`, `test_controller.py` | Git identity baseline passed. Implementation must identify evaluated inputs explicitly; no blanket generated exclusion is authorized. Future drift cases not run. |
| AC-03/04; V-06, V-07a–e | Production policy selection and runner actually execute portable argv, reload durable logs/exits/environment/candidate; invalid authority refuses; legacy host failure never falls back | `test_verification_runner.py`, `test_controller.py` | Planner available; new explicit execution path is required work, not a missing external capability. Real sbx unrun. Restrictive host tests must report actual execution denial/failure or unsupported-host skip truthfully. |
| AC-03; V-08a–d | All commands planned before launch; parser/install denials leave marker absent; quoted literal argv actually executes; authorized install tested by planning only | `test_verification_runner.py`, `test_controller.py` | 12 planner baseline tests pass; future public wiring proof not run. No package download needed. |
| AC-04; V-09a–f | Actual product failure versus missing executable/broken infrastructure; reload distinct failed/blocked/missing/not-run/omitted statuses; required failure never waived; later marker absent after failure | `test_controller.py`, `test_verification_runner.py` | Local product and prerequisite controls feasible; new result/status behavior not run. Existing authorized-gap legacy behavior is not authority to waive new required checks. |
| AC-02/03/04; V-10a–e | Synchronized real file changes and side effects prevent zero-exit pass; finite timeout kills owned group including descendant; invalid timeout refuses before launch | `test_verification_runner.py`, `test_controller.py` | Existing runner has timeout, open-pipe/exited-parent and resistant-child precedents; new pre/post candidate and group proof not run. |
| AC-02/03/04; V-11a–e | Controlled controller interruption before/after launch/publication, actual invocation counter, retained partial logs, exclusive record collisions; replay never relaunches or overwrites; unknown stays stopped | `test_controller.py`, `test_actor_operations.py`, `test_verification_runner.py` | Existing interruption/exclusive-publication helpers feasible. Future check-operation persistence proof not run. |
| AC-01/02/04; V-12 | Actual failed product then inherited terminal correction and new passing execution; different identities/history; checking adds no correction charge | `test_actor_operations.py`, `test_controller.py` | Existing correction reservation/admission fixture reusable; producer sequence not run. Full collection/correction composition belongs to T-004.2. |
| AC-05; V-13 | Compare actual callable/CLI payloads, schemas, replay and fresh collector rerun interface to producer contract and raw V-01–12 evidence | `test_controller.py`, `test_controller_state.py`, contract/document inspection | Future `controller-contract.md` is in scope. Independent discovery and separate acceptance remain owed, not performed here. |

Cheap readiness baselines, all exit 0:

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p test_controller_git.py`: 13 tests, no skips.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p test_verification_runner.py -k VerificationPlan`: 12 tests, no skips.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p test_actor_operations.py -k test_v01_v06`: 1 test, no skips; actual local actor prerequisites and implementation path.

## Starting evidence and native obligations

Measurement: complete, full_profile=true, advisory only. Original pair:

- `.quality/reports/T-004.1-preflight-20261110-01.json`
- `.quality/reports/T-004.1-preflight-20261110-01.txt`

Captured actual pre-edit worktree for logical project/repository root above:
`skills/task-orchestrator/scripts` and `skills/task-orchestrator/tests`, covering
future files as well as 12 current Python files (5 implementation, 7 test).
Use report `files` for source hashes/inventory and `identity` for scope,
settings/tool/check identity. CPython 3.14.6, complexity 6.0.1, Ruff 0.14.2;
complexity and Ruff completed with existing target `.quality` settings/exclusions.
No eval/harness Python outside these folders is authorized by this task.
Highlights are advisory, not functional defects or permission for unrelated cleanup.

Before first edit verify logical project, exact included inventory/current hashes,
folder coverage and effective tools/settings against this original report.
A mismatch requires focused reconsideration with cause/owner, not silent recapture.
Retain this pair through corrections; fresh later reports must use new names.
Expanded coverage needs authorized preserved pre-edit bytes; current measurement
cannot reconstruct lost history. No clone transfer is planned. If moved, copy both
files to the same explicit relative paths in the receiving repository; ignored
reports do not travel in commits. Colocated hashes prove consistency only.

| Native command | Scope / policy / stage owner | Current evidence and owed duty |
|---|---|---|
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py` | Whole repository; AGENTS CLEAN policy; implementer then maintainability review | Preflight: 4 tests pass. Rerun after implementation. |
| `python3 tools/check_contracts.py --root .` | Whole registry; repository policy; designated registry-updater after maintainability | Preflight: 8 subsystems / 33 refs pass. Updater must register only implemented contracts, explicitly regenerate index, then validate. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'` | Owning suite; brief execution route; implementer | Owed after changed focused modules pass. No complete suite run or all-green claim here. |
| `python3 tools/verify.py` | Whole repository; cross-cutting repository policy; implementer | Owed for cross-cutting change after focused suite; preserve constituent failures/skips. Historical T-003 aggregate is not current success evidence. |
| `python3 scripts/install_development_skills.py --check .` | Development profile; installer ownership; implementer if shared dependencies change; aggregate also checks drift | No profile/shared runtime dependency change planned. Inspect canonical installer if that changes; never refresh active install. |

## Warnings, stops and next action

No blocking prerequisite found. Implementation must stop for changed authority,
material predecessor mismatch, overlapping owner work, permission/scope expansion,
new shared infrastructure, uncertain process terminality or implementation-budget
checkpoint requiring scope resolution. Missing future tests are owed proof, not
waived acceptance. Real containment and real provider/sbx qualification remain
unrun. Existing advisory complexity does not authorize cleanup.

Standalone preflight is recommended for another task crossing this execution
policy/persistence boundary: it resolved the frozen authorization projection and
confirmed that real local fixtures can reach the required boundaries. Routine
subsequent mechanical edits can use implementer self-preflight.

## Implementer handoff

```text
Use T-004.1 brief revision 1 + verification revision 1 + this ready guided packet.
Preserve existing task-package/index work. Edit only the authorized orchestrator
producer owners. Before first edit validate inventory/hashes/project/settings in
.quality/reports/T-004.1-preflight-20261110-01.json and retain its .txt sibling.
Consume accepted T-003 lifecycle and explicit frozen sbx/YOLO authorization;
project that authority to the existing runner without weakening legacy refusal.
Use actual file/process evidence for V-01–13; new producer behavior is not yet tested.
Start with installed bounded-task-implementer and testing-discipline, add focused
fail-first producer proof using existing fixtures, then run changed modules and
owning suite. Complete native duties above and publish controller-contract.md.
Follow maintainability → registry updater → fresh independent discovery → separate
acceptance. Do not implement collection/completion or refresh installed skills.
```
