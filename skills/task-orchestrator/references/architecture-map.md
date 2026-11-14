# Task Orchestrator Architecture Map

Status: operator reference

Freshness: 2026-11-14

Read only the row that owns the requested behavior, then inspect its primary
test. Use `controller.py` integration coverage when a public command or
cross-module flow changes.

For source development in this repository, apply the
[code organization policy](../../../docs/code-organization.md) before choosing
placement. This map records current ownership. The [SIDE-004 controller discussion](../../../docs/tasks/SIDE-004/organization-context.md#controller-discussion-candidates-for-later-investigation)
provides historical context; use the current owners below for implementation.

| Concern | Source | Primary tests |
|---|---|---|
| CLI parsing, composition and Python compatibility entry points | `scripts/controller.py`, `scripts/__init__.py` | `tests/test_controller.py`, including copied-installation dependency isolation |
| Initialization, frozen authority, flow revision and legacy ledger updates | `scripts/run_authority.py` | `tests/test_controller.py`: initialization, frozen inputs, revision and interruption cases |
| Shared application records, observed identity and ledger projections | `scripts/run_records.py` | `tests/test_controller.py`, `tests/test_actor_operations.py`: identity, readiness, retained-byte and publication evidence |
| Read-only status, current recovery actions and atomic reservations | `scripts/operation_scheduling.py` | `tests/test_controller.py`: reservation/revision cases; `tests/test_actor_operations.py`: recovery decisions |
| Actor launch, observation, stop, readiness admission and interventions | `scripts/actor_lifecycle.py` | `tests/test_actor_operations.py`: actor lifecycle, contention, interruption and no-relaunch cases |
| Candidate inspection and reserved verifier checks | `scripts/candidate_checks.py` | `tests/test_actor_operations.py`: producer, check, scope and retained-evidence cases |
| Independent collection, collector reruns, report admission and findings | `scripts/review_collection.py` | `tests/test_actor_operations.py`: collection cases |
| Current acceptance context, conditional reviews and decision admission | `scripts/acceptance_workflow.py` | `tests/test_actor_operations.py`: acceptance and recovery cases |
| Owner-authorized input replacement and replay | `scripts/input_revision.py` | `tests/test_controller.py`: input-revision cases; actor revision/freshness cases |
| Retained private attempt execution, prompt and closure preparation | `scripts/legacy_attempts.py` | `tests/test_controller.py`: legacy transport cases; `tests/test_controller_git.py`: Git composition |
| Public inspection of retained legacy attempts | `scripts/legacy_inspection.py` | `tests/test_controller.py`: inspection, drift, replay and publication cases |
| State API compatibility exports | `scripts/controller_state.py` | `tests/test_controller_state.py`: direct/file-based compatibility aliases |
| Closed flow profiles, actor mapping, cursor/session policy and step envelopes | `scripts/flow_policy.py` | `tests/test_controller_state.py`: flow/cursor/envelope cases |
| Run permissions, verification configuration and explicit policy | `scripts/run_policy.py` | `tests/test_controller_state.py`: policy/authorization cases |
| Manifest graph/path validation and ready-task selection | `scripts/task_manifest.py` | `tests/test_controller_state.py`: manifest, graph/path and selection cases |
| Attempt/execution identities, verification, closure and finalization records | `scripts/execution_contracts.py` | `tests/test_controller_state.py`: `Stage3RecordContractTest` and attempt cases |
| Collection, conditional review, findings and acceptance record validation | `scripts/review_contracts.py` | `tests/test_actor_operations.py`: collection/acceptance validation and admission cases |
| Ledger consistency, ownership, actor/revision history and authorized updates | `scripts/ledger.py` | `tests/test_controller_state.py`: coherence, transitions, immutable authority and update cases; actor/revision integration |
| Canonical JSON/text digests and shared record predicates | `scripts/record_serialization.py`, `scripts/record_validation.py` | `tests/test_controller_state.py`: exact bytes/digests and consuming contract boundary cases |
| Git status, identity, scope, and drift evidence | `scripts/controller_git.py` | `tests/test_controller_git.py` |
| Verification command planning and execution | `scripts/verification_runner.py` | `tests/test_verification_runner.py` |
| Retained actor check integrity and derived disposition | `scripts/check_evidence.py` | `tests/test_actor_operations.py`: owner, verifier/collector replay and acceptance tamper cases |
| Acceptance dispositions, approved history and decision routing | `scripts/acceptance.py` | `tests/test_acceptance.py`; actor integration proves admission and persistence |
| Run-file reads, replacement, exclusive publication, exact replay and command-lock lifecycle | `scripts/run_storage.py` | `tests/test_run_storage.py`; controller/actor interruption and process-contention integration |
| Disposable controller/run fixtures and local actor setup | `tests/controller_fixture_support.py`, `tests/actor_fixture_support.py` | `tests/test_fixture_support.py`; controller and actor integration tests consume the builders |
| Codex CLI transport and thread records | `scripts/codex_worker.py` | `tests/test_codex_worker.py` |
| Current retrieval surface and examples | `SKILL.md`, `references/`, `assets/examples/` | `tests/test_retrieval_surface.py` |

Fixture support owns per-occurrence construction and cleanup registration, with
no test-case imports or behavioral assertions. Tests keep scenario orchestration
and oracles; fixture support is never a runtime dependency. Register cleanup
before initialization so failed setup also releases the occurrence's resources.

`acceptance.evaluate_acceptance` consumes validated findings/decision and explicit
operation, session and candidate identity values. It returns proposed finding
updates, next actions and a correction reason without I/O or input mutation.
`acceptance_workflow` calls this standard-library-only policy owner; identity
checks and evidence collection remain in that workflow, while `actor_lifecycle`
owns the enclosing observation transaction and ledger commit.

Application dependencies point downward: scheduling and actor lifecycle consume
acceptance and collection operations; acceptance consumes collection and candidate
checks; collection consumes candidate checks. These workflows use `run_authority`
and `run_records`, then the explicit domain-rule and infrastructure owners above.
`input_revision` and both legacy workflows use authority/records directly. No
component imports the controller or receives its namespace. The explicit import
allow-list in `tests/test_architecture.py` enforces these directions.

`scripts/__init__.py:load_component` binds a relative-import package to its
resolved installation path, without changing `sys.path`. Controller, state
compatibility, retained-check and verification entry points use this loader.
Repeated loads of that installation share its components and actor supervisor handles; a copied installation has separate module
identities. Existing public Python functions are direct aliases to their owners.
The private legacy launcher retains a CLI wrapper because its inspection fixtures
still need real attempt evidence; its application operation returns facts rather
than printing CLI output. Other private workflow helpers are addressed at their owner.

`controller_state` retains the existing public API and private compatibility
aliases; runtime consumers import the actual rule owners. Flow and review
contracts depend only on shared record predicates. Run policy uses flow policy;
execution contracts use flow/run policy, serialization and record predicates.
Manifest validation uses record predicates and the supplied repository's path and
brief facts. `validate_task_manifest_structure` exposes only structural validation
for owner-authorized revision requests, without weakening full manifest checks.

`ledger.validate_ledger` remains the consistency composition point. Actor
reservation/transport ownership, input-revision receipts, selected task/attempt
ownership and finalization references remain adjacent under this owner;
`apply_ledger_update` retains validation order, immutable authority, append-only
history and transition checks without mutating its input. Application workflows
retain locks and durable publication. Domain owners never import the state
compatibility facade, controller or application workflows. The existing CLEAN
allow-list enforces this acyclic direction. Git consumes only serialization;
verification and retained-check validation consume execution contracts directly.
The small shared predicate module owns shape/scalar/path checks, with no record
families or workflow policy. Canonical serialization does not own publication.

`run_storage` owns JSON-object reads, canonical record bytes, ordinary atomic
JSON replacement, durable exclusive byte publication, exact byte/validated-record
replay and `RunCommandLock`. It depends only on the standard library. The
controller retains public compatibility names for existing Python callers.
Application workflows call storage directly; fault injection targets the owning
record/storage boundary. Each mutation command retains lock scope, authorization,
publication order and ledger transitions. Collection/acceptance admission prepares
ledger changes inside the actor observation transaction; neither commits that
ledger independently. Initialization-directory assembly and attempt setup remain
application operations. Transport-local files keep their adapter-owned helpers;
neither storage nor transport imports the other.

Publication guarantees are deliberately distinct: replacement uses pretty JSON
with a newline and an atomic rename, without fsync or guaranteed temp cleanup.
Durable exclusive publication flushes/fsyncs a temp file, links without overwrite,
syncs its parent, and removes the temp; a post-link failure may leave published
bytes. Exact actor replay reuses identical bytes without resyncing and rejects
conflicts. Legacy inspection-record publication uses compact canonical JSON,
exclusive direct creation and file fsync only; replay validates existing records
and requires exact bytes. Caller-supplied validators retain schema authority;
failed/partial records are never repaired by storage. These primitives grant no
transaction authority or power-loss guarantees beyond their stated sync protocol.

`check_evidence` owns execution/result digest binding, execution structure and
exact closure identity (through `execution_contracts`), retained stdout/stderr log
digests and derived check disposition. `validate_execution_evidence` returns
validated execution facts; `validate_check_evidence` also rejects contradictory
result status; `execution_disposition` supplies the shared producer derivation.
It reads proof without process launch, publication or ledger mutation. Its only
sibling dependency is execution contracts; candidate and collection workflows call it for
verifier replay, collector rerun replay/admission and retained proof validation.
Acceptance consumes those validated application operations.

Ordinary verifier replay now rejects disposition contradictions. Genuine verifier
`stale` replay requires recorded post-check workspace divergence and validates
execution facts without replacing the application's stale outcome. Collector
stale/incomplete replay retains its existing application exception; it cannot
supply passed downstream proof. Assignment/configuration authority, independent
collector session and separate rerun identity, authorized omissions, current
workspace, recovery, uncertainty/no-relaunch, locks and publication remain with
the application command owners. Legacy inspection validates its distinct pre-check-result
envelope at its existing boundary.

## Public entry points

```text
controller.py init
controller.py status / reserve / launch / observe / stop / intervene
controller.py revise-inputs
controller.py inspect-candidate / check-candidate / check-collection
# Legacy primitives: run-next (refusal stub), inspect, revise-flow
```

`codex_worker.py` is an internal adapter. Route new operator actions through
public application/CLI composition, with responsibility placement determined by
the organization policy. Current entry points live in the controller; that fact
does not make it the default destination for a distinct new concern. Operator
prompts must not bypass application authority by calling the adapter directly.

## Verification commands

Run the owning module first:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_git.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_verification_runner.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_codex_worker.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_retrieval_surface.py
```

After targeted checks pass, run the full local suite when the change crosses
modules or affects the skill's public guidance:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s skills/task-orchestrator/tests -p 'test_*.py'
```

## Authority and existing records

Repository and system instructions bound the explicit persisted run policy,
manifest and task brief. Actor prompts, results and recommendations cannot grant
permissions, commit authority or ownership of the ledger. A worker reports claims;
`inspect` independently checks records, repository identity, task scope, existing
owner changes and configured verification before recording mechanical eligibility.
It does not complete semantic acceptance or release dependencies.

The application workflows above own authority, task/attempt transitions, prompt
rendering, Git inspection and verification composition. Domain rules live in
the owners above; `controller_state.py` retains compatibility exports. The internal
transport owns process/session mechanics. Workers edit only authorized task paths; they cannot commit, select
another task, edit controller records or broaden permissions. Keep the run
directory and active controller/skill installation outside worker-writable scope.

Run inputs and attempt artifacts bind policy, task identity, process/session,
effective permissions, Git baseline, results and diagnostics. Preserve prior
attempts when retrying. Missing results, process failure and an ambiguous/live
worker do not prove completion or authorize a new writer. Consult
the owning domain modules above and the JSON schemas for exact record/state
contracts.

Flow/cursor validation, closed profiles, handoff/outcome envelopes and safe-boundary
`revise-flow` exist. Actor-level mappings and the 0.5 implementation-context reuse
threshold are currently fixed in `flow_policy.py` and `flow-profile.schema.json`;
these are implementation constraints to investigate, not new owner requirements.
A profile or cursor record alone does not provide a runnable reviewed workflow.

## Verification containment

`verification_runner.py` currently requires macOS and the exact executable
`/usr/bin/sandbox-exec`. It builds argv directly, enforces configured filesystem
and network restrictions, and rejects unsupported configurations before launch;
there is no unrestricted fallback. The mechanism is deprecated and its profile
interface is private, so capability must be checked on the target host.

Writes are restricted by accessed pathname, not by inode. The operator must
supply writable roots without hard links that alias files outside those roots;
the runner does not scan for them. Canonical writable roots must be existing
absolute directories other than `/`. `danger-full-access` requires separate
explicit policy authorization, and approval policy must be `never`. Command
planning separately enforces dependency-install policy. Current containment does
not establish permissions or lifecycle support for a future harness adapter.

## Current limitations

The public controller provides conservative stop requests and terminal observation,
not automatic recovery or same-thread continuation. Separate acceptance and
review-driven correction admission are implemented; task commit finalization,
known-issue recording, atomic completion and dependency release, automatic advance, and
plan preparation. See the
[current development documents](../docs/README.md) for the desired behavior and
proposed delivery. Inspect current code and useful tests before extending it.

## Actor lifecycle boundary

`controller.py` reserves under its lock, publishes no-relaunch intent before
spawning the detached `codex_worker.py actor` supervisor, and owns one admission
path (`observe_operation` → `_admit_actor_outcome`). The adapter records process
and session observations and an exclusive terminal receipt. Missing receipt or
unresolved group liveness blocks another actor. Stop requests do not signal a
recorded PID. This path admits preflight readiness and current independent
collection while retaining terminal producer outcomes. The controller separately
inspects candidate scope and publishes candidate-bound checks. The active
collector requests one fresh controller-run rerun through `check_collection`;
its intent, observed session and separate execution identity preserve sole actor
ownership. Collection retains coverage, gaps and stable finding history; failed
checks and authorized review-driven corrections use the inherited shared correction
budget. Separate acceptance validates current evidence and independent observed
sessions, retains dispositions, and exposes eligibility and recovery routes.
Optional frozen `required_reviews` requires coordinator-supplied conditional-stage
receipts; it does not launch those stages. Completion remains unimplemented. See the
[T-003 lifecycle contract](../docs/tasks/T-003/controller-contract.md) and
[consolidated T-004 contract](../docs/tasks/T-004/controller-contract.md), and
[T-005.1 acceptance contract](../docs/tasks/T-005.1/controller-contract.md).

The verification runner retains its legacy macOS containment path. The
candidate check path uses the same runner with explicit frozen sbx/YOLO
authority to execute in the supplied environment.
