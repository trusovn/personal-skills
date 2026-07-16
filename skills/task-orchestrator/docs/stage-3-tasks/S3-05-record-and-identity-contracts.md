# S3-05: Add Immutable Record and Identity Contracts

Status: ready after S3-04
Depends on: S3-04
Blocks: S3-06, S3-07, S3-09, S3-13

## Outcome

Define pure, strict validators for Stage 3 verification records, closure
decisions, and acceptance-operation journals, including one reusable identity
binding that prevents stale or cross-attempt evidence from being replayed.

## Required context

Read:

- `docs/stage-3-plan.md` — durable record layout and settled decisions
- `docs/controller-contract.md` — authority and closure gate
- `scripts/controller_state.py`
- `tests/test_controller_state.py`

## Entry criteria

- S3-04 state and ledger tests pass.
- Stage 2 closure provides all identity inputs named in the master entry
  contract.

## Allowed changes

- `scripts/controller_state.py`
- `tests/test_controller_state.py`
- a JSON schema only if runtime validation uses the same contract in this task

Do not publish artifacts or wire CLI commands.

## Work

1. Define one exact identity containing run ID, task ID, attempt ID, turn,
   policy digest, manifest digest, prompt digest, baseline digest, Git-evidence
   digest, and verification digest where applicable.
2. Validate verification records, including ordered commands, outcomes, log
   references, effective envelope, timestamps, and pre/post Git identities.
3. Validate closure decisions, including reasons, allowed actions/transitions,
   gap details, and explicit `semantic_review` status.
4. Validate finalization operations and their `prepared`, side-effect-recorded,
   `complete`, or terminal mismatch states.
5. Validate referenced paths are contained under the run directory and their
   recorded digests match.
6. Make verification and decision publication exclusive/immutable. Permit an
   operation to advance only through compare-and-swap state transitions while
   preserving prepared intent and already recorded effect evidence.

## Acceptance criteria

- **AC-01:** Removing, adding, or changing any identity field rejects the
  record.
- **AC-02:** A decision from another run, task, attempt, turn, prompt, baseline,
  Git observation, or verification result cannot authorize a transition.
- **AC-03:** Unknown fields and truthy wrong types are rejected.
- **AC-04:** Artifact traversal, absolute paths, missing files, and digest
  mismatches are rejected.
- **AC-05:** Immutable record re-publication with different bytes fails. An
  operation rejects a stale expected state or any change to prior intent/effect
  evidence; exact replay is handled only where explicitly idempotent.
- **AC-06:** Pure validators perform no Git, process, tracker, or ledger side
  effect.

## Verification

Run one mismatched-identity test first, then:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py
```

## Exit and handoff

Report each record type and required identity field. Stop before command
parsing, execution, or artifact creation.
