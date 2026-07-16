# S3-01: Prove the Verification Sandbox Boundary

Status: ready after Stage 2
Depends on: Stage 2 exit contract
Blocks: S3-07

## Outcome

Select and prove one local, non-model mechanism that can execute controller
verification commands while enforcing the persisted sandbox, network, and
writable-root policy. This is a bounded architecture decision and capability
proof, not production runner implementation.

## Required context

Read:

- `docs/stage-3-plan.md` — entry contract, settled decisions, architecture
- `assets/run-policy.schema.json` — permissions and verification authority
- `docs/transport-decision.md` — precedent for a local capability decision

Inspect only the local tools/platform needed for the proof. Do not browse,
install a dependency, or call a model.

## Entry criteria

- Stage 2 exit criteria are satisfied.
- No existing approved verification-sandbox decision already owns this choice.
- Local parse/capability checks are allowed.

If an entry criterion is false, stop and report it without changing files.

## Allowed changes

- Create `docs/verification-sandbox-decision.md`.
- Create or update `tests/test_verification_runner.py` with the smallest
  reproducible capability fixture.

Do not add production runner code, change policy version 1, or weaken a denied
permission into a warning.

## Work

1. Map each policy value to a concrete runner configuration and identify any
   value the mechanism cannot enforce.
2. Prove a normal authorized command can run.
3. Prove an out-of-root write is denied and creates no file.
4. Prove a network connection attempt is denied when `network` is false.
5. State how `read-only`, `workspace-write`, writable roots, and
   `danger-full-access` are represented and fail closed when unsupported.
6. State that dependency-install denial also needs S3-06 executable/argument
   preflight; a filesystem/network sandbox alone is not semantic proof.
7. Record supported platforms, exact invocation shape, cleanup behavior, and
   the decision to adopt or reject the mechanism.

## Acceptance criteria

- **AC-01:** The decision names one exact mechanism and contains no placeholder
  or unverified claim.
- **AC-02:** A deterministic local proof passes for an allowed command.
- **AC-03:** Deterministic proofs show both out-of-root write and denied-network
  attempts fail without their side effects occurring.
- **AC-04:** Every version 1 sandbox/network/writable-root value is mapped or
  explicitly rejected before execution.
- **AC-05:** Unsupported hosts or configurations fail closed.
- **AC-06:** No dependency, network access, model call, or production command is
  added.

## Verification

Run the single capability test first, then:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_verification_runner.py
git diff --check
```

## Exit and handoff

Exit `complete` only with an adopted, locally proven mechanism. Exit `blocked`
if no available boundary can enforce policy; report the smallest choices for
the user (approved dependency, versioned policy weakening, or deferral). Do not
continue to S3-07 on a blocked result.
