# S3-06: Build the Authorized Verification Command Plan

Status: ready after S3-01 and S3-02
Depends on: S3-01, S3-02
Blocks: S3-07

```yaml
agent_tier: strong
reasoning: high
review: immediate
budget: 30 tool calls / 90 minutes / 100k context
```

## Outcome

Purely derive the exact ordered set of verification commands from persisted
authority, parse each into shell-free argv, and record every source/role that
requires it. Define an explicit, conservative version 1 meaning for
`dependency_install: false`; do not claim that argv inspection can prove what
arbitrary test code does transitively.

## Required context

Read:

- `docs/stage-3-plan.md` — command and verification decisions
- `docs/verification-sandbox-decision.md` — enforcement mapping from S3-01
- `docs/stage-3-tasks/S3-01-result.md` — adopted boundary and limitation
- `docs/stage-3-tasks/S3-02-result.md` — extracted pure boundary
- `assets/run-policy.schema.json`
- `assets/task-manifest.schema.json`
- `tests/test_verification_runner.py` — capability fixture that S3-07 will move
  behind production code

## Entry criteria

- S3-01 is complete and its pathname-scoped sandbox decision remains accepted.
- S3-02 is complete and the aggregate suite passes.
- The implementer can state one closed, testable top-level argv rule for
  explicit installation requests. If not, stop under the master-plan condition
  rather than implementing a heuristic advertised as semantic enforcement.

## Allowed changes

- new `scripts/verification_runner.py`, containing pure plan construction only
- `tests/test_verification_runner.py`
- new `docs/stage-3-tasks/S3-06-result.md`

Do not execute a command, port the S3-01 sandbox implementation yet, inspect
Git, or change policy/manifest formats. Do not add another command-plan module.

## Work

1. Build the ordered union of selected-task `required_checks`, policy
   `verification.targeted_checks`, and the non-null repository gate, in that
   source order.
2. Parse each string with `shlex.split(posix=True)`. Reject NUL/newline input,
   malformed quoting, empty argv, a leading `NAME=value`, the `env` launcher,
   explicit shell launchers, standalone shell control/redirection tokens, and
   command-substitution syntax. Because execution uses `shell=False`, ordinary
   quoted arguments containing spaces or literal wildcard/metacharacter
   characters remain data; do not add a broad character blacklist.
3. Normalize identity as the exact parsed argv tuple. De-duplicate by that
   identity, preserve its first position, and record every source plus role
   (`task_required`, `policy_targeted`, or `repository_gate`) and original
   persisted spelling.
4. Freeze a closed table for explicit install requests when
   `dependency_install` is false, including direct installer/package-manager
   entry points and supported interpreter/module subcommand forms. Reject a
   matched request before execution and record the exact matched rule. State
   explicitly that this is top-level argv preflight, not proof that arbitrary
   test code has no install side effect; S3-01 sandboxing and S3-08 Git drift
   detection remain independent controls.
5. Attach an authorized gap only to the normalized command carrying the
   `repository_gate` role. If the same normalized argv also carries a targeted
   role, failure remains a targeted failure and the gap cannot excuse it.
   A non-null gap with a null repository gate is invalid authority.
6. Return an immutable-by-convention JSON-compatible plan with stable command
   IDs, normalized argv, provenance/roles, gap metadata, and a canonical plan
   digest suitable for S3-07/S3-05 record binding. Do not mutate inputs or write
   an artifact.

## Required test evidence

Positive cases:

- Disjoint commands preserve task, policy, then repository-gate order.
  Equivalent quoted/whitespace spellings collapse to one normalized argv while
  retaining all sources and original spellings.
- Quoted ordinary arguments, paths with spaces, and literal metacharacters
  that require no shell parse into the expected argv.
- `dependency_install: true` permits a command that the closed install table
  rejects when false, without changing sandbox/network authority.
- A repository-gate-only entry carries the exact persisted gap metadata and a
  stable plan/command digest.

Negative cases:

- Empty/whitespace input, NUL/newlines, malformed quotes, leading assignments,
  `env`, each supported shell launcher, standalone control/redirection tokens,
  and command substitution are rejected independently.
- Each row of the explicit-install table has a denial test, including direct
  executable and supported interpreter/module forms; near-miss ordinary test
  commands remain allowed so the table is not a substring blacklist.
- A gap without a repository gate is rejected. A command carrying both
  targeted and repository-gate roles cannot be gap-excused.
- Reordering sources, dropping duplicate provenance, changing one argv token,
  or mutating an input after planning changes/rejects the independent oracle as
  expected; plan construction itself leaves inputs unchanged.

## Acceptance criteria

- **AC-01:** Ordering and provenance are deterministic for overlapping manifest
  and policy checks.
- **AC-02:** Quoted ordinary arguments parse correctly without a shell.
- **AC-03:** Each prohibited syntax/launcher family is rejected by a focused
  test without rejecting harmless literal argv data.
- **AC-04:** Explicit install requests matching the closed version 1 table fail
  before execution, and the documented limitation does not claim transitive
  semantic enforcement.
- **AC-05:** An authorized gap applies only to the exact repository gate and
  retains reason, owner, and follow-up; a targeted role always wins over a gap.
- **AC-06:** Plan and command identities/digests are deterministic and bind all
  normalized argv, order, provenance, roles, and gap data.
- **AC-07:** Input records remain unchanged and no command or durable artifact
  is created.

## Verification

Run the first explicit-shell-launcher denial first and show it fails for the
intended assertion. Then run:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_verification_runner.py
```

Run the aggregate task-orchestrator suite and `git diff --check` after the
focused module passes. No local process or sandbox capability test is newly
required in this pure task; the pre-existing S3-01 cases must remain green.

## Exit and handoff

Create `S3-06-result.md` and report the ordered plan shape, normalization rule,
rejected syntax/launchers, exact dependency-install table and limitation,
commands/results, and residual risks. Stop before implementing subprocess or
sandbox behavior.
