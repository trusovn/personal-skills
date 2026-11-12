# T-004.2 preflight

Status: `ready`
Profile: `guided`
standalone_preflight_value: `material`

## Readiness summary

- Repository: `/Users/mtrusov/work/skill-sources/personal-skills`.
- Source: [brief.md](brief.md), ready executable leaf, brief revision 1;
  [verification.md](verification.md), verification revision 1, already declares
  this root-relative source and its revision at the end. All 385 lines were read.
  The staged artifact is preserved unchanged; no metadata correction was needed.
- Dependency: T-004.1 [acceptance-02](../T-004.1/reviews/acceptance-02.md)
  explicitly ACCEPTS and supersedes historical acceptance-01. Current HEAD is
  `9afc120029ed85e10e56d4ac2fcce926db129d01` (`T-004.1 done`), containing that
  accepted producer. Its controller-contract's older submission-status sentence
  does not supersede the separate acceptance decision.
- Allowed implementation: collection/result schemas, controller/state wiring,
  assignments, focused tests and directly affected references within
  `skills/task-orchestrator/`, integration fixes within the accepted producer
  contract, and consolidated `../T-004/controller-contract.md`. Affected current
  registry records are handled later by the designated registry-updater stage.
- Pre-existing work: staged new `verification.md` above; untracked `.DS_Store`,
  `docs/.DS_Store`, `skills/.DS_Store`. Runtime/test paths were clean at capture.
  Preserve these artifacts and the real index. Preparation adds this packet and
  fresh ignored reports only; it neither stages nor changes the existing index.
- Permissions: local disposable Git/filesystem/process checks authorized. No
  live/model/network check, dependency installation, commit, official-plan edit,
  active-install refresh, provisioning, recovery service or ART-009/completion.
- Material uncertainty resolved: actual process/filesystem/check execution and
  required installed review stages are available. A live collector cannot simply
  reserve an ordinary verify operation while owning the sole actor slot. A bounded
  collection-owned rerun protocol using the existing runner, command lock, fresh
  check IDs/logs and exact frozen/candidate binding is feasible within directly
  affected producer integration. Preserve ordinary check semantics and the single
  semantic publication path; do not add parallel-writer coordination. This is
  implementation work, not a missing host capability or a claim of proof.
- Applicability: bound to brief/verification revision 1 and the original pre-edit
  report below. Reconsider affected facts if authority, scope, ownership, producer
  semantics, required capabilities or verification revision changes. Expected
  implementation/report effects alone do not require full rediscovery.

## Decision context

The [owner direction](../../direction-single-task-sbx.md) prioritizes one prepared
human-reviewed task in an owner-supplied sbx/separate branch with explicit YOLO
actors. Incorrect identity or replay can admit obsolete work or start overlapping
actors. Retain actual identities, one operation owner, pre/post drift checks,
observed terminality and historical evidence. Collection is instructed read-only;
filesystem isolation, provider identity and outer protection are not proved here.

Current discovery follows `docs/contracts/index.json` →
`docs/contracts/task-orchestrator.json` → architecture map, producer contract and
code/test authorities. Candidate/check production and observed actor transport
exist; semantic collection is this task's addition. Consume
[T-004.1](../T-004.1/controller-contract.md),
[T-003](../T-003/controller-contract.md) and
[T-002](../T-002/controller-contract.md), extend
`observe_operation` → `_admit_actor_outcome` → `_publish_actor_outcome`.
T-005 consumes the consolidated contract and owns separate semantic acceptance
and completion; T-006 owns the real sbx/provider pilot. No `docs/known-issues.md`
exists, so no recorded deferrals are inferred. Historical Linux sandbox failures
and earlier inconclusive acceptance are not current local qualification or waivers.

## Acceptance evidence and commands

All ACs derive from brief revision 1, parent P-03–06 and cited plan
ART-006/IF-003/FLOW-001–003/INV-001–008. All scenario child rows listed below
remain required. Commands run from the repository root. Reuse
`ActorOperationsTest`, `producer_run`, `seed_successor`, actual subprocess/check
counters, lock/interruption helpers and controller-state cases. Future collection
cases have not run and must be implemented; existing green tests prove only the
inherited boundary.

Exact module command (replace only MODULE with the listed filename):
`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p MODULE`.
For a changed method first use that same command with `-k METHOD`.

| AC / scenarios | Setup / decisive boundary / oracle | Feasible owner command / present capability | Current gap |
|---|---|---|---|
| AC-01/02; V-01 | Public preflight/implementation, actual checked candidate, distinct observed collector and new rerun IDs/logs; explicit coverage/findings, no acceptance | `test_actor_operations.py`; real fake-actor subprocess and producer fixture exercised | New collection admission/rerun protocol unimplemented |
| AC-01/04; V-02a–k | Vary one task/operation/role/session/candidate/input/policy/flow/provenance binding or terminality; preserve state on invalid API requests; live result bytes never terminal proof | `test_actor_operations.py`, `test_controller_state.py`; actual session receipts and synchronization helpers available | New collector identity/role matrix unrun |
| AC-02; V-03a–f | Actual controller reruns and command counter distinguish old/replayed/wrong-bound/failing/missing coverage from a fresh pass | `test_actor_operations.py`; producer actual command/log replay paths exist | New current independent coverage admission unrun |
| AC-02; V-04a–e | Recollect/reload stable IDs/evidence/context/history, explicit upstream approved disposition; reopen only with new evidence/exposure; no manufactured authority | `test_actor_operations.py`, `test_controller_state.py`; disposable persistent ledgers and test-only successor seam available | New finding/disposition semantics unrun; seeded approval proves consumption only |
| AC-03/05; V-05 | One unseeded public journey: real product defect → failing check → correction actor changes code → passing new check → distinct collector reruns → acceptance handoff | `test_actor_operations.py`; existing failed-product correction changes actual code and preserves history | Full collection composition unrun; cannot seed success |
| AC-03/05; V-06 | Real shared reservations/launches/reload/revision; cycle zero plus three counts; fourth exhaustion after valid prerequisites; retain partial work and intervention | `test_actor_operations.py`, `test_controller_state.py`; existing shared budget, repair/preflight, context threshold and successor seam | Extend exact three-origin proof; review decision fixture is test-only future ART-009 consumption |
| AC-04/05; V-07a–f | Actual tracked/untracked/config/evaluated ignored/task/policy/flow/index/HEAD drift and reference repointing reject current eligibility, retain history | `test_actor_operations.py`, `test_controller_git.py`; candidate hashes and relevant/irrelevant ignored controls available | New collection invalidation matrix unrun |
| AC-04; V-08 | Synchronize actual live collector, edit product/evaluated config/source authority, finish old report; reject stale admission | `test_actor_operations.py`; real process checkpoint helpers available | New in-flight collection guard unrun |
| AC-03; V-09 | Nonzero count, fresh rerun and recollection with no product change; new evidence leaves count/history unchanged and launches no implementer | `test_actor_operations.py`; existing operation/accounting inspection available | New evidence-only retry proof unrun |
| AC-02/04; V-10a–e | Real interruption at intent/live/terminal/publication boundaries, replacement controller, lock contention and replaced raw claim on replay; one outcome or precise conservative stop | `test_actor_operations.py`; existing real process contention/interruption fixtures available | Collection publication/reload proof unrun; no power-loss claim |
| AC-01/05; V-11a–e | Establish other prerequisites; actual product assertion, absent executable/evidence, stale input, unavailable review authority yield distinct persisted categories and next actions | `test_actor_operations.py`, `test_controller_state.py`; local faults require no network | New collection category/status proof unrun |
| AC-06; V-12 | Cross-check actual public responses/schema/artifacts, semantic extension seam and exact local proof against consolidated parent contract; keep ART-009 future | Contract/document inspection plus exercised cases above; `test_controller.py` for CLI deltas | Handoff and designated registry update owed after implementation; structural checks are not behavior |

Focused inherited baseline: actor suite 37 tests PASS, state suite 45 tests PASS,
no skips in either. These exercise actual local actor prerequisites, implementation,
checks, correction, persistence and process interruption. No new T-004.2 behavior
is claimed. Exact commands/exit codes and complete raw output are in
`/Users/mtrusov/work/skill-sources/personal-skills/.quality/reports/T-004.2-preflight-20261112T165634690085Z/outcomes.json`, `actors.log`, `state.log`.

## Starting evidence and native obligations

Measurement: `complete`, `full_profile=true`, advisory only. Original pair:

- `/Users/mtrusov/work/skill-sources/personal-skills/.quality/reports/T-004.2-preflight-20261112T165634690085Z/starting.json`
- `/Users/mtrusov/work/skill-sources/personal-skills/.quality/reports/T-004.2-preflight-20261112T165634690085Z/starting.txt`

Capture: actual pre-edit worktree at the logical repository root above, including
relevant staged/unstaged/untracked Python without modifying the real index.
Governed folders: `skills/task-orchestrator/scripts`,
`skills/task-orchestrator/tests`, `skills/task-orchestrator/evals` (existing empty
Python parent). Report inventory contains 12 Python files. These folders cover
future runtime, test, fixture/harness and eval Python within scope. No uncovered
new Python parent may silently acquire a before measurement.

Use report `files` for exact inventory/source hashes and `identity` for project,
scope, effective settings and tool/check identities. Report facts: CPython 3.14.4,
Radon 6.0.1, Ruff 0.14.2; complexity and Ruff completed under target
`.quality/maintainability.toml` and `.quality/ruff.toml`, including existing
exclusions and asset groups. The installed launcher was
`.agents/scripts/measure_maintainability.py`; no alternate helper or setup ran.
Complexity highlights remain advisory, not failure or unrelated cleanup authority.

Before first edit, the implementer must compare logical project, exact included
inventory and current hashes, tool/check/settings identity and intended folder
coverage with this pair. Changed bytes/inventory, wrong project, incompatible
identity or uncovered scope require focused reconsideration with cause and owner;
never replace the original with edited-code evidence. Retain both originals
through corrections, use fresh names later, and preserve exact pre-edit bytes for
authorized added scope or disclose the before-evidence gap. For a clone transfer,
copy the original JSON and text explicitly to the identical repository-relative
`.quality/reports/T-004.2-preflight-20261112T165634690085Z/starting.json` and `starting.txt`; ignored evidence
does not travel in a commit. Receiving absolute paths must be recorded if relocated.

| Native command | Scope / policy / owner | Current evidence / owed duty |
|---|---|---|
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p test_actor_operations.py` | Owning process/lifecycle baseline; implementer/discovery | PASS 37, no skips; `/Users/mtrusov/work/skill-sources/personal-skills/.quality/reports/T-004.2-preflight-20261112T165634690085Z/actors.log`. Repeat changed methods first, then owning modules after edits. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p test_controller_state.py` | Owning state baseline; implementer/discovery | PASS 45, no skips; `/Users/mtrusov/work/skill-sources/personal-skills/.quality/reports/T-004.2-preflight-20261112T165634690085Z/state.log`. New collection semantics owed. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'` | Whole orchestrator after targeted success; brief execution policy; implementer then independent discovery | Not run during preflight; report actual host failures/skips, do not inherit historical green as current evidence. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py` | Whole repository CLEAN policy, AGENTS.md; implementer/maintainability before handoff | PASS 4, no skips for pre-edit bytes; `/Users/mtrusov/work/skill-sources/personal-skills/.quality/reports/T-004.2-preflight-20261112T165634690085Z/architecture.log`. Required again after implementation. |
| `python3 tools/check_contracts.py --root .` | Whole registry structural policy, AGENTS.md; registry-updater/discovery | PASS 8 subsystems / 35 refs; `/Users/mtrusov/work/skill-sources/personal-skills/.quality/reports/T-004.2-preflight-20261112T165634690085Z/contracts.log`. Current implemented delta update and regeneration owed to designated registry stage. |
| `python3 tools/verify.py` | Whole repository aggregate for cross-cutting changes, AGENTS.md; implementer/discovery | Not run during preflight; owed after targeted/owning success for cross-cutting change. Profile drift is read-only; never refresh active installation. Skips are not behavioral qualification. |

## Warnings, stops, and next action

All required workflow roles resolve project-locally: testing-discipline and nested
maintainability, registry-updater, discovery and acceptance skills exist. Their
availability is not completed review. Preserve fresh independent maintainability
for significant production/test/harness changes, designated registry update,
fresh discovery, and a separate fresh acceptance decision in that order. No
source-guided substitution is needed now; unavailable required capability later
is an implementation stop with the precise owner action.

Stop for authority/scope change, unresolved owner overlap, material producer
mismatch, unavailable required review capability, permission expansion, or a new
shared harness dependency. Missing advisory measurement alone would not create a
new gate; native hard failures and indispensable proof gaps remain binding.
No live/provider/sbx qualification ran; T-006 owns it. No runtime or test edits
were performed by preparation. Standalone preflight added material value by
exercising the inherited real process/correction boundary and resolving active
review-stage and collection-rerun feasibility; retain it for similar stateful
handoffs with those uncertainties.

### Implementer handoff

Start with installed `.agents/skills/task-implementation-flow/bounded-task-implementer/SKILL.md`
and `.agents/skills/testing-discipline/SKILL.md`. Preserve staged verification and
untracked owner files. Verify the original measurement pair's applicability before
the first edit, then implement AC-01–06 using all V-01–V-12 cases and reusable
fixtures, beginning with focused collection/correction methods. Publish only the
consolidated T-005 interface/evidence handoff, then complete the independent review
route; do not run T-005, semantic acceptance, completion, commits or live checks.
