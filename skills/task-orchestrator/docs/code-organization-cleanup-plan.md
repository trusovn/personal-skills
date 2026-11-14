# Orchestrator code organization cleanup

Status: `READY_FOR_PLAN_VERIFICATION`  
Date: 2026-11-13  
Scope: the four high-priority findings from the repository organization review,
plus a conditional removal of the private legacy launcher.

Maintainers should be able to change acceptance rules, evidence checks, storage,
or test setup through a clear owner without navigating unrelated controller
behavior. The first useful proof is acceptance rules exercised through their
owning module while the public workflow produces the same decisions and records.
This is a behavior-preserving cleanup of implemented capabilities.

## Authority and boundaries

- Owner request: plan the four high-priority cleanup items; check whether legacy
  code can simply be removed instead of reorganized.
- [Code organization policy](../../../docs/code-organization.md),
  [project map](../../../docs/project-map.md), and
  [development instructions](../../../docs/development.md).
- [Current architecture map](../references/architecture-map.md),
  [operator guide](../references/operator-guide.md), and
  [implemented contracts](../../../docs/contracts/task-orchestrator.json).
- [Owner-confirmed direction](direction-local-harness.md) bounds authority and
  recovery. Desired completion features in that direction are outside this cleanup.
- Resolve the available `testing-discipline` installation for test maintenance.
  Source presence alone does not establish an installed skill.

Existing source, schemas, and meaningful tests establish the compatibility
baseline. Establish a fresh passing baseline before each implementation task;
prior review results are not execution readiness. No separate foundation rebuild
or live provider qualification is needed to plan this local refactor.

The planned capabilities are explicit runtime responsibility owners (**CAP-001**,
FLOW-001/002), independent reusable test setup (**CAP-002**, FLOW-003), and a
bounded legacy removal decision (**CAP-003**, FLOW-004). Maintainers consume
these capabilities; application commands and independent actors retain their
existing runtime authority.

Out of scope: broader state-module decomposition, reservation-policy extraction,
eval-package cleanup, new recovery/completion features, changing persisted formats,
or reducing metrics to numerical targets. Preserve public commands and retained
run compatibility. Do not refresh the active installation during implementation.

## Delivery order

The companion [task map](code-organization-cleanup-task-map.json) contains the
machine-readable dependencies. Task IDs are local to this plan, separate from
the main orchestrator delivery plan.

| Task | Priority / dependency | Useful result |
|---|---|---|
| [T-001 — Decide legacy removal](#t-001--decide-legacy-removal) | Cheap check first; independent | Remove the private launcher only if surviving behavior already has suitable coverage or a small replacement. Otherwise record a bounded deferral and continue. |
| [T-002 — Give shared test setup an owner](#t-002--give-shared-test-setup-an-owner) | High; after T-001 disposition | Subsequent extractions reuse explicit fixture builders rather than borrowing methods from test classes. |
| [T-003 — Extract acceptance decisions](#t-003--extract-acceptance-decisions) | High; after T-002 | Maintainers change disposition and routing policy through its owning module and direct tests. |
| [T-004 — Establish run storage ownership](#t-004--establish-run-storage-ownership) | High; after T-003 | Controller persistence no longer depends on the worker adapter; write guarantees and lock ownership are explicit. |
| [T-005 — Consolidate check evidence validation](#t-005--consolidate-check-evidence-validation) | High; after T-004 | Verifier replay, collection, and acceptance consume one authoritative integrity validator. |

Use separate, reviewable changes. The serial order avoids concurrent edits to
the same controller and test setup; it is not a claim that every concern has a
runtime dependency on its predecessor. A legacy deferral satisfies T-001 and
must not block the four high-priority tasks.

## Intended ownership and dependencies

Place runtime owners within `skills/task-orchestrator/scripts/` and reusable
test setup within its `tests/` directory. Module names and signatures are
delegated to each task; the responsibility boundaries below are settled.

| Boundary | Owns / public operation | Excludes / allowed dependencies |
|---|---|---|
| Acceptance decisions, IF-001 | Evaluate finding dispositions and acceptance routing from explicit validated facts; return decisions and proposed finding/history updates. | No filesystem reads, process control, locks, or ledger persistence. May depend on domain validation/record rules, never the controller. |
| Run storage, IF-002 | Named read, replacement, exclusive publication, and exact replay operations; lock resource lifecycle. Each operation documents its actual durability and conflict guarantees. | No acceptance or launch policy. Application commands retain transaction scope and ordering. No import of controller or worker transport. |
| Check evidence integrity, IF-003 | Validate retained execution identity, execution/result binding, log digests, and derived disposition; return validated facts or a bounded rejection. | No process launch or ledger mutation. May use state validators and storage. Stage authorization remains with the application. |
| Test setup, IF-004 | Create explicit per-occurrence repository/run/actor fixtures and expose shared builders and cleanup. | No imports from test-case modules, no shared mutable scenario state, no runtime imports of fixtures. |

CLI/application composition calls these operations. Extracted modules must not
import the controller or receive its module/global namespace through a context
bag. Keep the current worker adapter responsible for process/session mechanics.
Do not require a class for stateless policy or introduce callback chains merely
to hide effects. A lock can remain a stateful class.

The application remains the transaction owner: acquire the run lock, load and
validate authority, gather current facts, evaluate policy, publish the governing
artifacts in order, update the ledger, release the lock. Storage primitives do
not independently decide when a transition is authorized. Existing read-only
status behavior must not acquire mutation authority through the extraction.

## State and artifacts that cross tasks

| ID | Artifact / authority | Producer, consumers, mutation and lifecycle |
|---|---|---|
| ART-001 | Frozen inputs, assignments, ledger and retained run records | Existing initialization/application commands produce them. Application commands alone authorize mutations; new owners consume validated facts. Keep current schema, paths, digests, revisions and supersession semantics. |
| ART-002 | Execution records, logs and check outcomes | Verification runner produces execution/log evidence; application publishes outcomes. Verifier replay, collection and acceptance validate it. Changed bytes invalidate current eligibility; history remains intact. |
| ART-003 | Findings, proposed dispositions and admitted decisions | Collection produces findings; acceptance supplies a proposal; deterministic rules evaluate it; the application publishes admitted records and ledger updates. An agent claim alone grants no authority. |
| ART-004 | Disposable test repositories, runs and actor configuration | Fixture builders produce these for one test occurrence. Each occurrence owns mutations and cleanup; shared facts do not imply shared mutable state. |
| ART-005 | Legacy caller/coverage decision | T-001 records keep/remove/defer and the surviving coverage mapping. It is implementation evidence, not runtime authority. |

## Invariants and observable flows

- **INV-001 — Authorization and identity:** preserve exact assignment typing,
  frozen input/policy/flow/candidate bindings, independent observed sessions,
  and refusal of stale or altered evidence.
- **INV-002 — Single transaction owner:** preserve lock scope and no-relaunch
  intent before spawn/execution. Uncertain terminality never permits another
  writer or a second uncertain execution.
- **INV-003 — Publication and replay:** preserve existing file bytes, identities,
  required durability, exact replay and conflict rejection. Helpers must not
  substitute atomic replacement for exclusive publication or vice versa.
- **INV-004 — Acceptance:** preserve approved dispositions/history, precedence
  of authorized blocking correction, missing-evidence routes, and shared
  correction-budget behavior. Eligibility is not completion or tracker mutation.
- **INV-005 — Verification ownership:** common evidence rules have one owner;
  per-stage authorization remains distinct. Tests exercise decisive logic rather
  than replacing it with mocks; each fixture occurrence owns mutable state.
- **INV-006 — Removal safety:** remove only retired behavior or behavior whose
  surviving contract has named meaningful coverage; retain public compatibility.

**FLOW-001 — Acceptance:** a reserved independent actor consumes current frozen
inputs and candidate/check/collection evidence; its terminal proposal is read
under application authority; IF-003 validates evidence and IF-001 evaluates the
proposal; IF-002 publishes the decision and ledger transition under the existing
transaction. Output is eligibility, correction, missing-evidence recovery, or an
intervention. Invalid identities or changed proof retain the existing refusal or
blocker without granting eligibility. INV-001 through INV-005 apply.

**FLOW-002 — Checks and replay:** a reserved verifier or active collector consumes
its own authorized assignment and check plan; the application publishes intent,
executes through the existing runner, and publishes retained ART-002 evidence.
Replay and downstream admission use IF-003. A digest, identity or disposition
contradiction rejects the evidence; uncertainty preserves no-relaunch behavior.
Collector reruns retain their separate identity and ownership. INV-001 through
INV-003 and INV-005 apply.

**FLOW-003 — Independent test occurrence:** IF-004 creates a fresh ART-004 fixture;
the test performs explicit mutations and exercises the real owning rule or
integration boundary; assertions check observable decisions/artifacts; cleanup
releases the occurrence's resources even after failure. INV-005 applies.

**FLOW-004 — Legacy removal gate:** T-001 consumes caller and coverage evidence,
publishes ART-005, and either removes an eligible private path or defers it.
The terminal outcome is a justified removal or explicit bounded deferral;
INV-006 applies. This gate does not authorize removal of other legacy APIs.

## Task contracts

### T-001 — Decide legacy removal

The initial static audit on 2026-11-13 found:

- `_legacy_run_next` is defined in `scripts/controller.py`; no production caller
  was found in the repository. Public `run-next` dispatches to `_cli_run_next`,
  a separate pending/reporting operation.
- `tests/test_controller.py` substitutes the private launcher using
  `LEGACY_CONTROLLER`. References occur in 14 test methods and in
  `ControllerInspectionIntegrationTest.create_clean_inspection_run`; that helper
  indirectly supplies many additional inspection tests.
- `tests/test_controller_git.py` invokes the private launcher directly in
  `test_run_next_uses_controller_git_task_baseline_and_closure_evidence`.
- Some `runner run-next` references elsewhere are synthetic eval fixtures,
  not consumers of this orchestrator. Search by symbol and dispatch, not only
  the command's text. Historical plan references do not establish live use.

Therefore deletion is not currently established as a cheap change. Recheck
callers and map the affected assertions to retained contracts: authority refusal,
locking and interrupted execution, Git identity/drift, inspect replay and record
integrity. Remove obsolete tests only after identifying remaining distinct
coverage. A small explicit inspection-record fixture is permissible if it proves
setup validity and retains the tested integration behavior; copied success labels
or mocked decisive validation are not substitutes.

If removal needs broad inspection migration, record the consumers and defer it.
Do not build a new legacy execution subsystem to avoid deleting the function.
Keep public `run-next`, `inspect`, and `revise-flow`, and the worker adapter's
start/resume paths outside this removal unless separately authorized after their
own caller/contract analysis. Update current guidance only if affected; leave
historical plans/results intact. The audit cannot prove absence of external
Python users; the private symbol is not a supported public entry point.

### T-002 — Give shared test setup an owner

Replace method borrowing across `ControllerIntegrationTest`,
`ControllerReservationTest`, `ControllerInputRevisionTest`, and
`ActorOperationsTest` with cohesive support owned by the orchestrator test suite.
Separate reusable setup from assertions. Keep decisive scenario values visible
and resource ownership explicit. Move existing cases by concern where this
improves ownership; do not split files by arbitrary size or inherit unrelated
test methods. Preserve discovery behavior and each distinct failure oracle.

### T-003 — Extract acceptance decisions

Start with disposition evaluation, history preservation and routing currently
in `_disposition_for_finding`, `_acceptance_dispositions`, and `_acceptance_route`.
Expose IF-001 and exercise it directly. The application still gathers current
evidence, checks observed identity, publishes decisions, and mutates the ledger.
Use typed/validated facts or narrow explicit values; do not pass controller
internals into the new owner. Existing acceptance, recovery, stale-evidence and
correction-budget integration cases must continue to establish the same results.

### T-004 — Establish run storage ownership

Move controller storage infrastructure to IF-002 and remove ledger-persistence
dependence on `codex_worker.atomic_write_json`. Inventory existing replace,
exclusive and replay semantics before consolidating implementations. Retain
required flush/fsync and directory-sync behavior at the same observable
publication boundaries. Preserve ordinary replacement semantics where that is
the existing contract; this task does not silently strengthen/change every
write protocol. Transport-local files may remain adapter-owned. If transport
needs a shared primitive, declare that narrow dependency and update its guardrail.
Exercise interrupted publication, conflict/replay and contention with real local
filesystem/process evidence; retain application transaction order.

### T-005 — Consolidate check evidence validation

Reconcile verifier replay validation in `check_candidate` with
`_validate_check_artifacts` and the evidence consumers in collection/acceptance.
Define IF-003 once and route shared integrity checks through it. Classify checks
as common integrity, stage-specific authorization, or legitimate boundary
validation before removing duplication. Preserve existing outcome vocabulary,
collector freshness and separate rerun identity, authorized omissions, and
staleness/recovery routes. Conflicting existing policies require an explicit
behavior decision rather than silently choosing the weaker implementation.

Every extraction updates the existing architecture map, relevant module
responsibility descriptions, import allow-list/sentinels, and affected contract
record authorities in the same change. Use the bounded flow's registry-updater
stage when applicable; regenerate the index only with `--write-index` after
editing subsystem records. Do not register planned modules as implemented.
The orchestrator is currently absent from `DEVELOPMENT_SKILL_SOURCES`; inspect
the installer if a shared installed dependency changes, but do not add the skill
to the development profile as part of this cleanup.

## Verification and completion

| Contract / task | Intended evidence |
|---|---|
| IF-001 / INV-004 / T-003 | Existing or migrated direct decision cases: supported blocker, invalid deferral, preserved approved disposition, exact finding coverage, correction precedence and missing proof; public actor integration proves admission and persistence. |
| IF-002 / INV-002–003 / T-004 | Existing interruption/replay/conflict and process-contention cases establish publication order, no duplicate launch, byte preservation and ledger revision behavior. Add a focused fault only for a concrete uncovered contract. |
| IF-003 / INV-001, INV-005 / T-005 | Actual retained records/logs exercise changed execution bytes, changed logs, wrong identity, inconsistent disposition, verifier replay and collector-owned rerun. Preserve per-consumer authorization evidence. |
| IF-004 / INV-005 / T-002 | Existing cases pass under normal discovery and selected independent execution; separate fixture occurrences cannot affect each other's repository, run or actor configuration. |
| FLOW-004 / INV-006 / T-001 | Caller/coverage mapping plus retained relevant tests; if removal proceeds, no symbol references remain and retained command behavior passes. A grep result alone is not behavioral proof. |

Use `.venv/bin/python` with the existing development dependencies. Start with
the touched owner/test module and its meaningful scenarios. Before and after
each runtime extraction, run the orchestrator suite:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover \
  -s skills/task-orchestrator/tests -p 'test_*.py'
```

For cross-cutting implementation, run `.venv/bin/python tools/verify.py` and
report skips/failures separately. Before handoff, also run the canonical checks:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py
python3 tools/check_contracts.py --root .
```

Keep raw logs on disk. Schema/import/JSON checks establish structural evidence,
not successful workflow behavior. Live/expensive qualification still requires
its applicable approval; local fake actors cannot qualify provider judgment or
actual sbx isolation. Do not add tests just to mirror the extracted functions.

Completion requires all four high-priority outcomes, a recorded legacy
disposition, preserved meaningful behavioral coverage and public compatibility,
current ownership/contract documentation, and passing applicable checks with
explicit limitations. Record task results beside this plan; do not update this
plan or existing delivery plans as a progress ledger.

## Risks, delegated choices and review handoff

The main risks are splitting a transaction, weakening integrity validation during
deduplication, or losing integration preconditions while removing legacy setup.
Storage and acceptance extractions must be assessed with their consumers, not
only the resulting file sizes. Exact module names, function signatures, fixture
factory form and local test grouping are delegated within the above contracts.
There are no unresolved owner-level scope decisions for planning. A discovered
semantic conflict or a required public compatibility break returns to the owner.

Run `project-plan-verification` in a fresh/separate agent before implementation,
reviewing this plan, its companion task map and the authorities above together.
Structural map validation does not constitute independent plan verification.
