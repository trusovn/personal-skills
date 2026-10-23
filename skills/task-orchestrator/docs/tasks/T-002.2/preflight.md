# Task Preflight: T-002.2 — Reserve one operation and retain its correction count

Status: `ready`
Profile: `guided`
standalone_preflight_value: `material`

## Readiness summary

| Item | Result and evidence |
|---|---|
| Source | [brief.md](brief.md), ready executable, revision 1 |
| Verification | [verification.md](verification.md), revision 1; `Source brief: brief.md` resolves correctly |
| Repository | `/Users/mtrusov/work/skill-sources/personal-skills`; HEAD `1c1aff8` (`T-002.1 done`) |
| Ownership | Initial and pre-write `git status --short` empty; no overlapping owner work or declared parallel writer |
| Dependency | T-002.1 implemented contract present; [acceptance-02](../T-002.1/reviews/acceptance-02.md) explicitly ACCEPTs and permits handoff to T-002.2 |
| Scope | Controller/state scripts, affected schemas, owning `test_controller_state.py`/`test_controller.py` and reused fixtures under `skills/task-orchestrator/`; this package's reports and contract note |
| Permissions | Local Python/Git/temp-file/process checks feasible. No network, model, sbx launch, dependency installation, active-skill refresh, plan edits or repository commits needed |
| Value | Resolved predecessor acceptance, actual ledger/lock interfaces and reusable persisted/process fixtures. Reservation ownership does not yet exist; it is this task's work, not a missing prerequisite |
| Applicability | Bound to brief/verification revision 1 and current predecessor contract. Reconsider changed authority, dependencies, ownership, permissions or capability; expected implementation changes alone do not require full rediscovery |

## Decision context

Authority is the [parent](../T-002/brief.md), including its owner decision that
environment repair shares the correction budget, the [single-task direction](../../direction-single-task-sbx.md),
and [plan](../../local-harness-orchestration-plan.md) IF-001, ART-002/004,
INV-001/002/005/007/008 and FLOW-001/003. The operating envelope is one prepared
task under frozen authority. Duplicate work, lost counts or false readiness can
authorize unsafe continuation. Persisted guards, conservative unknown-operation
handling and byte-preserving refusals mitigate these risks.

The current [controller contract](../T-002.1/controller-contract.md) provides
frozen inputs/policy, stage roles, ledger revision checking, a command lock and
pure correction transitions. Its introductory “submitted” label is historical;
the later acceptance-02 decision controls dependency completion. Current
`active_operation_path` is restricted to finalization; extend the existing
controller/ledger validation deliberately for reservations rather than assume
that field already supports actor ownership. No public status/reserve API is
required to exist before implementation.

T-002.3 consumes the persisted reservation contract; T-003 consumes assignments
and owns real observed outcome/readiness admission. T-004/005 own semantic
prerequisites and completion. Explicit successor records in tests are feasible
setup, not proof of those future production paths. No unresolved direction
decision was found. No dedicated known-issues file was found in the scoped docs.
Acceptance-02 records one pre-existing retrieval inventory failure in the
aggregate suite; it does not affect these local reservation fixtures, must stay
visible, and does not waive any owning test or task criterion.

## Acceptance evidence and commands

All commands below run from the repository root above with
`PYTHONDONTWRITEBYTECODE=1`. Future scenarios have not run and are not claimed
to pass. The existing owning module is the concrete initial command until the
implementer selects an actual focused test method; run that method first, then
the two owning modules progressively.

| AC / scenario / risk | Authority and planned decisive proof | Feasibility / command / result |
|---|---|---|
| AC-01 / V-01 | Brief AC-01, INV-007/008: public status against persisted records; reload, explicit evidence variants and unchanged authoritative bytes | Existing temporary Git repo and initialized-run setup in `test_controller.py` supports real records. Add status cases in scope. `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py`; future proof not run |
| AC-02/03 / V-02 / R1 | IF-001, INV-002: first/replayed/competing keys and versions; reserved/running/unknown versus test-seeded terminal records; one authoritative assignment across reload and separate controller processes | `RunCommandLock`, `update_ledger`, real filesystem fixtures and synchronized child-process lock setup exist. Same controller module command; future reservation cases not run |
| AC-04 / V-03 / R2 | Parent P-03 and owner repair decision: cycle zero, mixed corrections 1–3, fourth refusal, replay/restart/route changes, free evidence/preflight retries, uncertain charge retention and repair before initial implementation | Existing policy/cursor helpers and real ledger fixtures permit labelled successor setup. Add persisted accounting cases, not just pure transition tests. Same controller command, then `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py`; future proof not run |
| AC-03/05 / V-04 / R3 | INV-001/002 and AC-05: stale/wrong task-role-stage, weak profile, missing/stale/wrong/nonterminal readiness and unknown operation; public reserve plus `run-next`, `inspect`, `revise-flow` refuse without authority/task-file changes | Public CLI/library paths and initialized policy/input fixtures exist. Seed readiness only in labelled test setup. Reuse owning modules above; no live transport needed. Future guard cases not run |
| AC-05 / V-05 | Parent P-06: exact status/reserve requests, assignments, replay/refusal semantics and single successor admission seam match implemented behavior; no generic public state setter | Package `controller-contract.md` is an allowed future artifact. Source/public-example inspection plus V-01–04 results is feasible; documentation shape alone is insufficient. Not run |

Executed narrow capability baseline:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py -k test_direct_update_ledger_obeys_run_lock
```

Result: exit 0, one test passed in 0.108 seconds. The test initializes actual
frozen records in a temporary Git repository, holds `controller.lock` in another
process, confirms public ledger mutation refuses and compares unchanged ledger
bytes. This proves usable local lock/process/persistence setup, not the future
reservation behavior. No broad baseline was needed or run.

## Warnings, stops and next action

Stop for changed authority, incompatible predecessor contract, unsafe permission
needs, overlapping owner work or scope growth. Preserve required evidence
distinctions; pending successor behavior cannot become success. Runtime admission,
actor launch, input revision and final completion remain excluded. Ask before
slow, live, networked or privileged verification. Independent discovery owns the
broader aggregate decision; subsequent independent acceptance remains separate.

Standalone preflight added material value for this dependency handoff. Recommend
it again when a similar task consumes a newly accepted persisted interface;
routine edits with already established interfaces can use implementer self-checks.

## Implementer handoff

```text
Implement T-002.2 from brief revision 1 and verification revision 1.
T-002.1 prerequisite is ACCEPTed by reviews/acceptance-02.md; consume its
controller-contract.md. Baseline is clean at HEAD 1c1aff8 except this new packet.
Change only brief-allowed controller/state/schema/owning-test/fixture paths and
package reports/contract. Extend existing persistence and lock boundaries;
active_operation_path currently means finalization, not general actor ownership.
Real Git/temp-record and synchronized process fixtures are available; the narrow
public ledger-lock test passes. Future V-01..V-05 behavior has not been tested.
First add/select one focused fail-first public-controller case. Run that exact
method, then test_controller_state.py and test_controller.py using the recorded
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest commands, one gate at a time.
Preserve all scenario/risk rows, including repair before initial implementation.
Use labelled test-only successor states; do not add production state injection.
Stop on authority/contract/ownership/permission/scope changes. Publish the exact
implemented contract and follow the required independent review route.
Next action: invoke bounded-task-implementer on this package with this packet.
```
