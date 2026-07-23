# S3-01: Prove the Verification Sandbox Boundary

Status: ready after Stage 2
Depends on: Stage 2 exit contract
Blocks: S3-07

```yaml
agent_tier: strong
reasoning: high
review: immediate
estimated_budget: 30 tool calls / 90 minutes / 100k context
```

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
2. Establish local controls before testing denials: prove the selected
   out-of-root temporary directory is host-writable and a local loopback
   listener is reachable without the corresponding restriction. Do not use an
   external network endpoint.
3. Prove a normal authorized command and an in-root `workspace-write` command
   can run with their expected side effects.
4. Prove `read-only` denies a write to an otherwise writable root and
   `workspace-write` denies an out-of-root write, with no denied file created.
5. Prove the loopback connection succeeds with `network: true` and the same
   connection is denied with `network: false`.
6. State how `read-only`, `workspace-write`, writable roots, and
   `danger-full-access` are represented and fail closed when unsupported.
   Exercise `danger-full-access` only in an isolated temporary directory and
   only when its separate authorization is present; reject it before launch
   otherwise.
7. State that dependency-install denial also needs S3-06 executable/argument
   preflight; a filesystem/network sandbox alone is not semantic proof.
8. Record supported platforms, exact invocation shape, cleanup behavior, and
   the decision to adopt or reject the mechanism.

## Required test evidence

Positive cases:

- The unrestricted control write and loopback connection succeed, proving the
  denial probes are capable of observing a side effect on this host.
- An authorized command runs; `workspace-write` writes inside each configured
  root; `network: true` reaches only the local loopback fixture.
- Authorized `danger-full-access`, if supported, writes to the isolated control
  path and cleans it up.

Negative cases:

- `read-only` cannot write to a control-proven writable root.
- `workspace-write` cannot write to a control-proven writable path outside all
  configured roots, and no file appears there.
- `network: false` cannot reach the same control-proven loopback listener.
- Unsupported modes, missing writable-root enforcement, and unauthorized
  `danger-full-access` are rejected before command execution.

The fixture must fail if the mechanism is replaced by an unrestricted process
or if a control probe cannot demonstrate that its side effect is otherwise
possible.

## Acceptance criteria

- **AC-01:** The decision names one exact mechanism and contains no placeholder
  or unverified claim.
- **AC-02:** Deterministic local controls prove the write and loopback probes can
  succeed, and positive proofs pass for every supported permission mode.
- **AC-03:** Deterministic proofs show both out-of-root write and denied-network
  attempts fail without their side effects occurring; `read-only` also denies
  a write to an otherwise writable configured root.
- **AC-04:** Every version 1 sandbox/network/writable-root value is mapped or
  exercised by the positive/negative matrix or explicitly rejected before
  execution.
- **AC-05:** Unsupported hosts or configurations fail closed.
- **AC-06:** No dependency, external network access, model call, or production
  command is added.

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
