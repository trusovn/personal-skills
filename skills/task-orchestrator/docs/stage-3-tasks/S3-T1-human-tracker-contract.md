# S3-T1: Freeze a Human-Tracker Contract

Status: conditional; not ready without user request and a concrete tracker
Depends on: S3-05 plus explicit user authority
Blocks: S3-T2

## Outcome

Approve one versioned human-tracker adapter contract with enough persisted
authority for deterministic mutation. This task makes the decision and contract
only; it does not edit a tracker or implement an adapter.

## Required context

Read:

- `docs/stage-3-plan.md` — conditional tracker decision
- `assets/run-policy.schema.json`
- `scripts/controller_state.py` — operation records
- the concrete tracker file and its owning repository instructions

## Entry criteria

- The user explicitly requests human-tracker support.
- The exact tracker exists or a complete representative fixture is supplied.
- The user can approve whether the tracker is inside/outside the repository and
  whether its change belongs in the task commit.

If any item is absent, stop and ask; do not infer it from Markdown appearance.

## Allowed changes

- create `docs/human-tracker-contract.md`
- update/create a versioned policy schema only after its exact semantics are
  explicitly approved
- focused schema/validator tests required by that approved record

Do not write production adapter code or mutate a tracker.

## Required decisions

Freeze all of these:

1. adapter name and version;
2. canonical tracker path and containment rules;
3. exact file format and encoding;
4. task-ID-to-record mapping and duplicate/unknown handling;
5. allowed old/new states and exact field/value mutation;
6. pre-update digest and concurrency assumptions;
7. atomic-write and idempotency semantics;
8. whether the tracker is committed, and in which controller operation;
9. recovery evidence distinguishing intended update from external mutation.

## Acceptance criteria

- **AC-01:** Every required decision has one approved value and no `TBD`.
- **AC-02:** A concrete before/after tracker example changes exactly one mapped
  record and no unrelated bytes/data.
- **AC-03:** Persisted policy can authorize the exact adapter/path/semantics and
  omission remains denial.
- **AC-04:** Mismatch, duplicate ID, unexpected old state, and concurrent change
  behavior fail closed.
- **AC-05:** Commit and interrupted-finalization treatment are explicit.
- **AC-06:** The contract is specific; it does not promise arbitrary Markdown
  or arbitrary tracker formats.

## Verification

Parse any changed JSON schema/fixtures and run its focused validator tests, then
`git diff --check`.

## Exit and handoff

Report the user's approved choices and exact adapter scope. S3-T2 remains
blocked until there are no unresolved contract fields.
