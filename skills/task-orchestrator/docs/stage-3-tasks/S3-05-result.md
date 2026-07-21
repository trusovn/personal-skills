# S3-05 result — Immutable record and identity contracts

Status: complete implementation submission; the immediate acceptance verdict is
reported separately in the implementation handoff.

## Implemented contracts

- Attempt/turn subject: exact run, task, attempt, positive turn, policy,
  manifest, prompt, and selected-task-baseline identities.
- Closure identity: the exact subject plus Stage 2 Git evidence digest and the
  post-worker HEAD, index tree, and canonical-status SHA-256 identities.
- Command execution: ordered canonical command IDs, argv/provenance/role,
  ordered outcomes, turn-qualified stdout/stderr references and digests,
  effective envelope, timestamps, terminal reason, and authorized-gap result.
- Final verification: exact closure identity, immutable execution record path
  and digest, pre/post-verification Git identities, drift findings, and outcome.
- Closure decision: exact closure identity, immutable verification path and
  digest, mechanical verdict/reasons, allowed actions/transitions, optional gap
  details, and `semantic_review: not_collected`.
- Finalization operation: exact closure and decision identities, immutable
  prepared acceptance intent, append-only effect evidence, and mismatch
  evidence.

Every record rejects unknown fields. SHA-256 values are canonical lowercase
64-character hex; Git object IDs are canonical lowercase 40- or 64-character
hex. Run-relative artifact paths reject absolute, backslash, empty, dot, and
parent segments and must match the record's exact attempt and turn family.
Validators and the operation update function are pure and preserve inputs.

## Identity chain

```text
attempt/turn subject
  -> closure identity
  -> command execution digest
  -> final verification digest
  -> closure decision digest
  -> finalization operation
```

No record contains or validates its own digest. Canonical JSON digests are
computed externally and consumed only by the next record.

## Operation transitions

```text
prepared -> effects_complete -> complete
    |              |
    +-> mismatch <-+
```

`complete` and `mismatch` are terminal. Exact same-state replay returns an equal
detached value when the caller supplies the current expected state. Stale
expected state, skipped/reversed transitions, prepared-intent changes, evidence
removal/alteration, and effect additions after `effects_complete` are rejected.

## Verification evidence

- Baseline before S3-05: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py` — passed 26 tests.
- Required fail-first: the mismatched-turn test failed because turn 2 was
  accepted instead of raising `identity does not match expected subject`.
- Focused after implementation: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills.task-orchestrator.tests.test_controller_state.Stage3RecordContractTest.test_attempt_turn_identity_rejects_mismatched_turn` — passed 1 test.
- Task suite after implementation: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py` — passed 36 tests.
- Immediate review correction: an independent probe first showed that distinct
  IDs with duplicate normalized argv and a mismatched `resume`/`stopped` pair
  were accepted. After correction, the same probe rejected both cases; the
  focused suite again passed 36 tests.
- Broader gate: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'` — passed 112 tests.

## Writer-boundary handoff

This task intentionally does not read or publish artifacts. The owning writer
tasks must still prove real run-directory containment, referenced-file
existence, content digest matching, exclusive creation, exact existing-record
reuse, contradictory-record rejection, and crash/replay behavior:

- S3-07 owns execution logs and command-execution publication.
- S3-08 owns closure compatibility, final verification/decision publication,
  and ledger references.
- S3-11 owns acceptance-operation publication and recovery-facing journal
  behavior.

No command parsing, process execution, Git inspection, ledger mutation, tracker
action, or artifact publication was added in S3-05.
