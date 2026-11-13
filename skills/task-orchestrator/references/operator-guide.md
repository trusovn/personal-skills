# Task Orchestrator Operator Guide

Status: operator reference
Freshness: 2026-11-13

Use the controller from inside an existing owner-approved Docker sbx on a
separate branch. This is an operating assumption, not a containment guarantee.
Start with the [run policy](../assets/examples/minimal-run-policy.json),
[manifest](../assets/examples/minimal-task-manifest.json) and their schemas.
Confirm one task, human-reviewed brief and verification, allowed paths, required
checks and explicit `execution_authorization` (sbx, YOLO, active-chat intervention).
Use commit mode `off`; actors never commit. No command provisions sbx.

## Initialize and reserve

Place the run directory outside the repository. Replace every placeholder:

```sh
python3 <skill-dir>/scripts/controller.py init --run-dir <run> --policy <policy.json> --manifest <manifest.json> --repository <repo>
python3 <skill-dir>/scripts/controller.py status --run-dir <run>
python3 <skill-dir>/scripts/controller.py reserve --run-dir <run> --expected-version <current-version> --task-id <task> --stage preflight --role preflight --operation-key <unique-key>
```

Save the returned `assignment` object, without the surrounding response, as
`assignment.json`. Inputs are frozen; mutable source documents do not replace
them. A permitted `revise-inputs --request <owner-request.json>` requires an
explicit owner decision bound to the entire revision and invalidates readiness.
See the [current predecessor revision contract](../docs/tasks/T-002/controller-contract.md).

## Launch and observe

```sh
python3 <skill-dir>/scripts/controller.py launch --run-dir <run> --request <assignment.json> --timeout-seconds 300
python3 <skill-dir>/scripts/controller.py observe --run-dir <run> --operation-id <operation-NNN>
```

Launch returns after starting a detached supervisor. `observe` admits a complete
terminal preflight bound to current inputs and the observed session. Preflight
checks the tools, dependencies and installed skills required by the frozen task;
source presence is not skill installation. Results attest completeness with
explicit inventories and evidence. Admission validates that structured claim;
it does not independently infer every prerequisite from prose or authenticate
an actor's statements. Missing reported prerequisites block implementation.

After readiness, reserve `--stage implement --role implementer` at the current
version, save its assignment, launch and observe it. The first implementation
is cycle zero. After a complete terminal implementation or correction, use
`inspect-candidate` with the producer operation ID. Reserve `verify` as
`verifier` for the current candidate, then pass the saved assignment and a
timeout to `check-candidate`. Checks run in the supplied environment under the
frozen sbx/YOLO authority. See the
[T-004.1 producer contract](../docs/tasks/T-004.1/controller-contract.md) for
commands, evidence paths, replay and drift handling.

After passed current checks, reserve `semantic_review` as `review_collector`,
save its assignment, then launch and observe it. The fresh collector requests
`check-collection` with its exact assignment and a timeout to rerun the frozen
checks through the controller. Terminal collection admission requires the current
candidate, observed independent session, fresh rerun evidence and explicit
coverage, gaps and findings. Complete current coverage enables a separate
acceptance assignment. See the
[T-004 controller contract](../docs/tasks/T-004/controller-contract.md) for
collection payloads and rerun protocol.

Reserve `--stage acceptance --role acceptance_reviewer` at the current version,
save the returned assignment, then launch and observe it using the same commands
above. Required conditional maintainability/registry receipts must already exist
when declared by the frozen manifest. Admission requires a fresh observed
reviewer, current candidate/evidence and a disposition for every retained finding.
The [T-005.1 controller contract](../docs/tasks/T-005.1/controller-contract.md)
defines receipts, decision payloads, evidence digests and replay rules.

Read `status` for `acceptance_decision`, `outstanding_findings` and `next_actions`.
An authorized blocking finding enables review-driven correction; reservation
charges one of the three shared check/review/repair corrections after cycle zero.
Missing evidence routes to verify, recollect or intervene without charging a
correction. Prevented correction or missing authority requires intervention;
environment repair requires fresh preflight. Follow the retained route rather
than inferring authority from raw actor output. A current `accept` with valid
proof and no active actor yields `completion_eligible=true`; this is a consumer
signal, not a command. It does not record known issues, publish completion,
commit, release dependencies or advance tasks. Local scripted actors do not
qualify live sbx/provider/model execution or semantic reviewer judgment.

Every actor uses a fresh session and frozen `gpt-6.1-sol` low/medium/high mapping.
The authorized bridge passes approval-never and danger-full-access inside sbx.
Configured model identity is not observed provider identity. Assignments prohibit
reviewer implementation edits; runtime read-only enforcement is not claimed.

Repeated launch with the exact assignment/configuration returns the original
operation. Changed replay configuration or stale authority refuses. `observe`
retains raw output and terminal observations once; repeated collection cannot
charge another correction or replace the recorded outcome.

## Interruption and recovery

```sh
python3 <skill-dir>/scripts/controller.py stop --run-dir <run> --operation-id <operation-NNN>
python3 <skill-dir>/scripts/controller.py observe --run-dir <run> --operation-id <operation-NNN>
python3 <skill-dir>/scripts/controller.py status --run-dir <run>
```

A stop request is a file the supervisor observes, not terminality proof. Only
an adapter receipt recording a reaped actor and absent process group allows
terminal admission. A dead/unpublished supervisor without that receipt leaves
unknown ownership and prohibits retry or another writer. Preserve work and
all records; an owner must resolve liveness. There is no automatic recovery,
PID-based kill shortcut, same-thread continuation or power-loss guarantee.
A reserved operation stopped before launch is known unlaunched and terminal.

## Active-chat intervention

Blocked/unknown outcomes retain blocker, evidence location, unresolved operation
and required coordinator action in the ledger. Status exposes the records and
relay action. Relay the precise blocker in the active coordinator chat; no
external message tool is required. Record observed relay/response through:

```sh
python3 <skill-dir>/scripts/controller.py intervene --run-dir <run> --request <intervention.json>
```

The request has string fields `key`, `blocker`, `evidence`, `operation_id`,
`required_action`, `event`, `text`. `event` is `opened`, `relayed` or `response`;
empty `operation_id` represents a blocker without a reserved operation. Preserve
the same subject fields when appending an event to a key. Absent relay/response
means unknown, not delivered or approved. Acknowledgement and silence grant no
repair, revision, retry or completion authority. Environment repair uses the
existing shared three-correction budget and requires a fresh preflight afterward.

## Historical boundary and current stop report

`scripts/controller.py run-next` remains a refusal/reporting stub for the former
pipeline. `inspect` and `revise-flow` preserve older mechanical primitives; they
do not collect or admit new actor outcomes. Do not call `codex_worker.py` directly
or use its legacy resume command to bypass controller ownership.

Report run/task/operation, stage/version, blocker, correction count, exact retained
paths, current readiness and next permitted action. The
[T-003 successor contract](../docs/tasks/T-003/controller-contract.md) documents
payloads, raw handoffs and the ART-008 runtime supplement. Local fake actors prove
control flow only. Real sbx/provider launch qualification remains unrun until
separate approval; historical T-001 isolation limits remain historical limits.
