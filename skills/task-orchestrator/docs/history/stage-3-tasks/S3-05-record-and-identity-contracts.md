# S3-05: Add Immutable Record and Identity Contracts

Status: ready after S3-04
Depends on: S3-04
Blocks: S3-07, S3-09, S3-13

```yaml
agent_tier: strong
reasoning: high
review: immediate
budget: 30 tool calls / 90 minutes / 100k context
```

## Outcome

Define pure, strict validators for Stage 3 verification records, closure
decisions, and acceptance-operation journals. Use a small acyclic identity
chain that prevents stale or cross-turn evidence from being replayed without
requiring any record to contain or validate its own digest.

## Required context

Read:

- `docs/stage-3-plan.md` — durable record layout and settled decisions
- `docs/controller-contract.md` — authority and closure gate
- `docs/stage-3-tasks/S3-04-result.md` — actual state/ledger contract
- `scripts/controller_state.py`
- `tests/test_controller_state.py`

## Entry criteria

- S3-04 state and ledger tests pass.
- Stage 2 closure provides all identity inputs named in the master entry
  contract except the exact post-worker canonical status digest, whose producer
  and compatibility handling are explicitly assigned to S3-08.

## Allowed changes

- `scripts/controller_state.py`
- `tests/test_controller_state.py`
- a JSON schema only if runtime validation uses the same contract in this task
- new `docs/stage-3-tasks/S3-05-result.md`

Do not read or publish artifacts, inspect Git, or wire CLI commands. This task
validates record structure and identity links; the task that owns each writer
must prove file existence, content digests, and exclusive publication.

## Work

1. Define an exact attempt/turn identity containing run ID, task ID, attempt ID,
   positive turn number, policy digest, manifest digest, prompt digest, and
   selected-task baseline digest.
2. Define a closure identity that extends that subject with the Stage 2 Git
   evidence digest and exact post-worker Git identity: HEAD OID, index tree,
   and SHA-256 of the canonical status mapping.
3. Validate command-execution records that reference the closure identity and
   contain the ordered normalized plan/provenance, command outcomes, log
   references/digests, effective envelope, timestamps, terminal reasons, and
   authorized-gap outcome. Validate final verification records that reference
   the immutable execution-record digest and add exact pre/post-verification
   Git identities plus drift findings. Neither record contains its own digest.
4. Validate closure decisions that reference the immutable verification-record
   digest and contain mechanical verdict, reasons, allowed actions/transitions,
   gap details, and explicit `semantic_review: not_collected`. The decision
   does not contain its own digest.
5. Validate finalization operations that reference the immutable decision
   digest. Define the minimal state progression `prepared -> effects_complete
   -> complete`, with a terminal mismatch transition only where later recovery
   can prove a contradiction. Preserve prepared intent exactly and make effect
   evidence append-only across pure operation updates.
6. Validate digest syntax and run-relative artifact-reference syntax, including
   rejection of absolute paths, empty/dot/parent segments, and wrong artifact
   families. Leave actual containment resolution, file reads, digest matching,
   and exclusive creation to S3-07, S3-08, and S3-11.
7. Reject unknown fields, wrong JSON types (including booleans accepted as
   integers), invalid enums, duplicate command identities, and non-canonical
   identity variants. Keep validators and update functions side-effect free and
   input-preserving.

## Required test evidence

Positive cases:

- Exact fixtures validate for an attempt/turn identity, closure identity,
  successful and failed command-execution records, final verification records,
  accepting and non-accepting decisions, and every allowed operation
  transition.
- Canonical JSON produces stable externally computed verification and decision
  digests, and those digests bind the next record in the chain.
- Exact replay of a pure operation update is either an explicit no-op or returns
  the same value without mutating either input.
- Valid run-relative log/artifact references include the attempt and turn
  identity expected for their record family.

Negative cases:

- For every identity link, changing run, task, attempt, turn, policy, manifest,
  prompt, baseline, Git evidence/status, execution digest, verification digest,
  or decision digest rejects the consuming record.
- Missing/unknown fields, truthy wrong types, malformed SHA-256 values,
  duplicate command IDs, reversed timestamps, and outcome/terminal-reason
  contradictions are rejected.
- Absolute paths, `..`, empty/dot segments, wrong attempt/turn filenames, and a
  verification record pointing into `decisions/` are rejected structurally.
- An operation cannot skip a state, change prepared intent, remove or alter
  recorded effect evidence, reuse a stale expected state, or return from a
  terminal state.
- A controlled test demonstrates the chain is acyclic: adding a record's own
  digest as a required payload field is rejected rather than becoming part of
  canonical validation.

Filesystem existence, digest mismatch, exclusive-create, and crash/replay
integration cases are deliberately not mocked here; they are mandatory at the
real writer boundaries in S3-07, S3-08, and S3-11.

## Acceptance criteria

- **AC-01:** Removing, adding, or changing any identity field rejects the
  record.
- **AC-02:** A decision from another run, task, attempt, turn, prompt, baseline,
  Git observation/status, or verification result cannot authorize a
  transition.
- **AC-03:** Unknown fields and truthy wrong types are rejected.
- **AC-04:** Artifact traversal, absolute paths, malformed digests, wrong
  artifact families, and wrong attempt/turn names are rejected structurally.
- **AC-05:** Operation updates reject a stale expected state or any change to
  prior intent/effect evidence; exact replay is handled only where explicitly
  idempotent.
- **AC-06:** The identity chain has no self-digest or other circular dependency.
- **AC-07:** Pure validators perform no filesystem, Git, process, tracker,
  ledger, or publication side effect and do not mutate their inputs.

## Verification

Run one mismatched-turn identity test first and show it fails for the intended
assertion, then:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py
```

## Exit and handoff

Create `S3-05-result.md` and report each record type, identity link, operation
transition, commands/results, and the file-integrity cases explicitly handed
to writer tasks. Stop before command parsing, execution, or artifact creation.
