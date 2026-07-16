# S3-06: Build the Authorized Verification Command Plan

Status: ready after S3-05
Depends on: S3-05
Blocks: S3-07

## Outcome

Purely derive the exact ordered set of verification commands from persisted
authority, parse each into safe argv, record why each command is required, and
reject command forms that would create shell or dependency-install authority.

## Required context

Read:

- `docs/stage-3-plan.md` — command and verification decisions
- `docs/verification-sandbox-decision.md` — enforcement mapping from S3-01
- `assets/run-policy.schema.json`
- `assets/task-manifest.schema.json`
- `scripts/controller_state.py`

## Entry criteria

- S3-05 record contracts pass.
- S3-01 has recorded how dependency-install denial is enforced or has blocked
  the stage.

## Allowed changes

- `scripts/controller_state.py` or one narrowly named pure command-plan module
- `tests/test_controller_state.py` or its matching focused test module

Do not execute a command, inspect Git, or change policy/manifest formats.

## Work

1. Build the de-duplicated ordered union of selected task
   `required_checks`, policy `verification.targeted_checks`, and the non-null
   repository gate.
2. Preserve first occurrence and record every source that required a duplicate.
3. Parse with `shlex.split()` and execute nothing.
4. Reject empty argv, newlines, shell operators, redirection, command
   substitution, glob-dependent shell syntax, and leading environment
   assignments.
5. Apply the exact dependency-install denial decided in S3-01 when policy says
   installation is false; do not invent a permissive fallback.
6. Permit a repository-gate gap only when the persisted gap matches that exact
   gate. Never skip or convert a failed targeted check.

## Acceptance criteria

- **AC-01:** Ordering and provenance are deterministic for overlapping manifest
  and policy checks.
- **AC-02:** Quoted ordinary arguments parse correctly without a shell.
- **AC-03:** Each prohibited syntax family is rejected by a focused test.
- **AC-04:** Commands conflicting with dependency-install denial fail before
  execution according to the S3-01 decision.
- **AC-05:** An authorized gap applies only to the exact repository gate and
  retains reason, owner, and follow-up.
- **AC-06:** Input records remain unchanged and no durable artifact is written.

## Verification

Run the first prohibited-command case, then the owning pure test module. Run
`git diff --check` after the module passes.

## Exit and handoff

Report the ordered plan shape, rejected syntax, and dependency-install rule.
Stop before implementing subprocess or sandbox behavior.
