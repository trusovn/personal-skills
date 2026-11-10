# T-003 preflight

Status: `ready`
Profile: guided
standalone_preflight_value: material

## Readiness summary and applicability

Repository: /Users/mtrusov/work/skill-sources/personal-skills.
Source: brief.md revision 1; verification.md revision 1 (`Source brief: brief.md`).
Allowed scope: orchestrator actor transport/controller/state, directly affected
schemas/references/examples/tests, and task-local evidence/successor contract.
Existing task-package files and task index changes belong to the user; preserve
them. Existing .DS_Store files are unrelated. Production/test paths are clean.
Dependencies: T-002.1 acceptance-02, T-002.2 acceptance-01 and T-002.3
acceptance-02 ACCEPT. T-002/controller-contract.md supplies the current authority
loaders, reservations, revision and shared-budget behavior. Registry routing is
docs/contracts/task-orchestrator.json; its older summary is not a replacement
for that accepted contract. Native Python/Git/filesystem/child-process capabilities
are available. Existing controller and fake-Codex fixtures can be reused.

## Decision context

Use the owner-confirmed direction-single-task-sbx.md, accepted plan review and
brief's cited plan interfaces. One prepared task in an existing Docker sbx;
explicit YOLO authorization, fixed model mapping, separate reviewer sessions.
Duplicate writers or stale readiness are material failures: publish conservative
unknown state before launching and never infer terminality from a stop request.
T-004/005 consume raw output through one admission boundary; T-006 owns remaining
live qualification. No provisioning, migration, auto recovery or completion.
Historical sandbox and retrieval failures reported in predecessor acceptance are
outside required local T-003 proof and must remain visible if reproduced.

## Acceptance evidence and commands

All rows derive from the corresponding brief AC and verification revision 1.
Future cases have not run; readiness is feasibility, not successful behavior.

| AC / cases | Feasible setup and decisive oracle | Planned command |
|---|---|---|
| AC-01 V-01/02a..e/03 | Existing frozen authority/revision helpers, real fake actor argv/input log; invalid single-field controls launch nothing; fresh correction session | PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p test_actor_operations.py |
| AC-01/04 V-04/09a..d | Disposable Git/run directories, competing real controllers, synchronized publication interruption; invocation count <=1, reload blocks unknown | same focused command |
| AC-02 V-05a..i | Child events, result and stderr; independent observed session, terminal snapshot; invalid output never advances | same focused command |
| AC-03 V-06/07a..g/08 | Disposable tool/dependency/installed-skill prerequisites; actual actor checks, first successful implementation marker; repair/revision invalidates readiness | same focused command |
| AC-04 V-10 | Waiting child/group, stop/timeout/interruption; terminal observation distinct from unknown; retained files/count/history | same focused command |
| AC-01/05 V-11 | Existing budget fixtures seed only successor correction reasons; actual launches/reload/replay retain shared count | same focused command |
| AC-02/05 V-12a..f | Seed only successor prerequisites; fresh review sessions, raw output, persisted chat relay/response without authorization | same focused command |
| AC-02/06 V-13 | Actual existing sbx/provider credentials and separate approval required; NOT RUN is explicitly permitted by brief, T-006 owns follow-up | No live command authorized |
| AC-06 V-14 | Reconcile successor contract with executable interfaces and local evidence | Focused tests plus document reconciliation |

All local setups are in scope, use stdlib and existing fixtures, and require no
network/provider permissions. Standalone preflight resolved the predecessor and
process-fixture boundary; recommend it for materially similar interruption work.

## Starting evidence and native obligations

Original pair: .quality/reports/T-003-start-20261109-01.json and
.quality/reports/T-003-start-20261109-01.txt. Complete actual pre-edit worktree
capture, logical root above; folders skills/task-orchestrator/scripts and
skills/task-orchestrator/tests cover future files. Report files inventory/hash,
identity/settings/check selections, measurement_status and full_profile are the
authorities. Installed .agents/scripts/measure_maintainability.py succeeded with
both pinned analyzers. Before editing verify exact inventory/current hashes,
logical project/tool/settings identity and folder coverage. Retain this original
through corrections; no replacement baseline. Reports share this worktree;
isolated consumers must copy both exact files to identical relative paths.

Native duties, all later implementer checks, not entry baselines:
- Focused command above, then changed transport/state/controller suites and full
  orchestrator suite: brief and verification evidence ownership.
- PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py:
  whole-project mandatory CLEAN gate under AGENTS.md.
- python3 tools/check_contracts.py --root .: whole-registry structural duty;
  synchronization belongs to later registry updater.
- python3 tools/verify.py: whole-project aggregate for cross-module changes,
  retain skips/failures, no live checks. Existing installation must not refresh.
No entry baseline needed: missing launch/admission is intended new behavior,
not an environment failure. All final native evidence remains owed.

## Warnings and exact next action

V-13 NOT RUN: no live permission; no claim of sbx/provider qualification.
Stop for authority/scope change, inseparable user overlap, missing decisive local
capability or new permission needs. No external messaging, installs or commits.
Next: bounded-task-implementer consumes this packet, validates baseline and
implements V-01..12/V-14, preserving explicit V-13 qualification gap. Immediate
review ends implementation at READY_FOR_REVIEW; no self-acceptance.
