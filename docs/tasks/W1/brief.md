# Task Brief: `W1` — Implement local evidence storage

Status: `ready`

Task kind: `executable`

```yaml
agent_tier: standard
reasoning: medium
review: immediate
budget: 15 tool calls / 40 minutes / 32k context
```

## Execution sizing

- Sizing policy: `default@1`
- Estimated agent calls: `15`
- Estimated implementation duration: `40 minutes`
- Estimate confidence: `medium`
- Policy result: `fits`
- Triggered limits: `none`
- Decomposition override: `none`

These estimates cover implementation-agent work only. They include the required
baseline self-preflight, focused repository discovery, production and test
edits, and targeted verification. They exclude the fresh acceptance review.

## Readiness route

`implementer self-preflight`

Before changing code, run the three baseline suites recorded by W0. Stop and
report any pre-existing failure rather than absorbing it into W1:

```bash
python3 -m unittest tests/test_run_evidence.py -v
python3 -m unittest tests/test_runtime_context.py -v
python3 -m unittest tests/test_workflow_version.py -v
```

## Verification-design recommendation

`separate — atomic replacement, immutable conflict behavior, namespace isolation,
and the active-to-finalized attempt lifecycle admit multiple plausible but
incorrect implementations; a focused verification design can pin the negative
and failure-path oracles before production code is written`

This recommendation is advisory. If no separate pass is used, the implementer
must preserve every scenario and oracle below in `tests/test_evidence_store.py`.

## Outcome

The repository provides a standard-library-only local `EvidenceStore` that
stores blobs and JSON records under Git metadata, rejects conflicting immutable
writes, manages attempts from creation through irreversible finalization, and
can retrieve or test the existence of stored records without exposing partial
writes.

## Direction trace

- Direction contribution: Materialize the approved local persistence boundary
  needed by later record construction and run-evidence integration.
- User-observable effect: No direct workflow effect; enables W2 to persist core
  records and W3 to move the existing run-evidence lifecycle onto the v2 store.
- Why now: The approved work breakdown orders W1 before the W2 record layer and
  the W3 producer migration, both of which consume this storage boundary.
- Direction decisions used:
  `docs/execution-evidence/execution-evidence-collection-contract.v1.2.1.md`
  §11.13;
  `docs/execution-evidence/execution-evidence-architecture.v1.2.1.md`
  §§4–5, §§10 and 22;
  `docs/execution-evidence/execution-evidence-repo-integration.v1.2.1.md`
  §3;
  `docs/execution-evidence/execution-evidence-implementation-plan.v1.2.1.md`
  Task 1 / Storage;
  `docs/execution-evidence/execution-evidence-work-breakdown.v1.2.1.md`
  W0 decisions and W1;
  `docs/execution-evidence/W0-result.md`.
- New direction decisions required: `None`

## Authority and scope

| Item | Contract |
|---|---|
| Authority | In descending order: collection contract v1.2.1; architecture v1.2.1; repo integration v1.2.1; implementation plan v1.2.1. The W1 work breakdown, verification matrix, and W0 result refine execution without overriding that chain. |
| Repository root | `/Users/mtrusov/work/skill-sources/personal-skills` |
| Dependencies | W0 complete; its three baseline suites remain explicitly unverified and are a pre-edit stop gate. The extracted authority documents under `docs/execution-evidence/` are the readable source pack. |
| Allowed changes | Add `scripts/evidence_store.py` and `tests/test_evidence_store.py` only. |
| Read-only context | The v1.2.1 authority and execution-aid documents under `docs/execution-evidence/`; `scripts/run_evidence.py` and its tests only as local style/atomic-write precedent. |
| Out of scope | Record constructors/schema (W2); `run_evidence.py` migration and PRE-RUN/execution/POST-RUN semantics (W3); skill integrations; task planning; review semantics; workflow/runtime discovery; telemetry; feature extraction; adapters; remote/S3 storage; query/database layers; legacy migration; multi-agent/worktree locking; changes to authority or plan documents. |
| Assumptions / unresolved decisions | Exact Python signatures and internal logical-reference representation are bounded implementation choices. They must expose only the seven approved operations and must not encode W2 record semantics. No unresolved product or architecture decision blocks W1. |

## Required interface and invariants

Implement one small persistence boundary, `EvidenceStore`, with an initial local
backend named `GitMetadataEvidenceStore` and only these public operations:

```text
put_blob
put_immutable_record
create_attempt
update_active_attempt
finalize_attempt
get_record
record_exists
```

The implementation must preserve these constraints:

- Resolve the initial root beneath the repository's absolute Git directory as
  `<git-dir>/personal-skills/evidence/v2/`; do not store v2 evidence in the
  worktree.
- Store blob bytes by SHA-256 content identity in the approved
  `blobs/sha256/<prefix>/<hash>` layout. Filenames and absolute source paths do
  not affect the blob reference.
- Keep project snapshots, task revisions, associations, attempts, and blobs in
  distinct logical namespaces consistent with the architecture's layout.
- Treat blobs and generic immutable records as create-once values: an identical
  repeat is idempotent, while the same logical reference with different bytes
  or JSON content fails without changing the stored value.
- Treat attempt data as opaque JSON at this layer. W1 owns storage lifecycle,
  not W2/W3 field semantics: create exactly once, permit replacement/update
  only while active, finalize exactly once, and reject all later mutation.
- Use atomic local replacement so a reader observes either the previous
  complete value or the next complete value, never a partial JSON record.
- Use only the Python standard library unless a concrete blocker is reported
  and separately approved.
- Do not impose the CLI/workflow assumption of one active attempt per worktree
  as a store invariant; operations address attempts by ID.

## Work and acceptance criteria

Required work:

1. Add the minimal store and Git-metadata backend in
   `scripts/evidence_store.py`, including deterministic blob references,
   namespace mapping, JSON read/write helpers, immutable conflict detection,
   and the attempt lifecycle operations.
2. Add focused real-filesystem tests in `tests/test_evidence_store.py` for the
   complete W1 surface and its failure paths.
3. Run targeted verification, then the nearest affected existing suites. Do not
   change `run_evidence.py` or introduce W2 record/schema behavior to make the
   tests pass.

- **AC-01:** In a temporary Git repository, the resolved store root is exactly
  under its absolute Git directory at `personal-skills/evidence/v2/`, not under
  the worktree.
- **AC-02:** Writing identical blob bytes more than once yields one stable
  SHA-256 content reference and stored value; changing the bytes changes the
  reference, while changing a filename or absolute source location does not.
- **AC-03:** For every supported immutable-record namespace, the first write is
  retrievable, an identical repeat is idempotent, and a conflicting repeat
  raises a store-specific error while preserving the original value.
- **AC-04:** `create_attempt` creates one active attempt; a second conflicting
  create fails; `update_active_attempt` changes only an existing active attempt;
  and separate attempt IDs may be active concurrently at the storage layer.
- **AC-05:** `finalize_attempt` persists the supplied final value and
  irreversibly closes the attempt. Update, conflicting re-finalization, and any
  other later mutation, including an identical re-finalization, fail while the
  finalized value remains retrievable.
- **AC-06:** `get_record` and `record_exists` distinguish existing records from
  missing records without crossing namespaces or aliasing equal IDs in
  different namespaces.
- **AC-07:** A forced write failure before atomic replacement leaves an existing
  target byte-for-byte unchanged (or leaves a new target absent), so no partial
  record becomes visible.
- **AC-08:** The implementation and tests use only the standard library and the
  scoped files; no task-planning, runtime/workflow discovery, record-model,
  review, telemetry, migration, remote-backend, query, or locking behavior is
  introduced.

### Finite-risk coverage contract

| Invariant | Material dimensions/cases | Decisive oracle/boundary | Implementation evidence | Independent review probe | Gate owner |
|---|---|---|---|---|---|
| Immutable content never changes in place | first write; identical repeat; conflicting repeat for blob and generic immutable JSON | Real temporary filesystem: stored bytes/ref remain stable and conflict raises | Focused tests covering the three transitions and reading bytes back after conflict | Re-run one conflict with a nested JSON value whose serialization order differs but semantic content is equal, then with one changed value | Implementer owns targeted suite; fresh reviewer owns probe |
| Attempt lifecycle is one-way | absent→active; active→updated; active→finalized; finalized→update rejected; finalized→conflicting finalize rejected; two distinct active IDs | Public store operations plus persisted `attempt.json` on a real temporary filesystem | Focused lifecycle tests execute each transition and confirm unchanged persisted state after rejection | Start two attempts, finalize one, verify the other remains independently updateable and the finalized one is unchanged | Implementer owns targeted suite; fresh reviewer owns probe |
| Namespace mapping cannot alias records | blob; project snapshot; task revision; attempt; association, including equal logical IDs where applicable | Public lookup/existence operations and distinct on-disk paths | Parameterized or subtests prove writes/readbacks remain distinct | Inspect/probe equal IDs in two record namespaces and confirm neither overwrites the other | Implementer owns targeted suite; fresh reviewer owns probe |
| Atomic failure exposes no partial target | new target; replacement/conflict path | Real filesystem with a forced failure before `os.replace`: target absent or prior bytes unchanged | Failure-path test controls the replacement boundary and reads target bytes afterward | Inspect the atomic helper and repeat failure probe against an existing target | Implementer owns targeted suite; fresh reviewer owns probe |

## Verification

| Evidence | Scenario and oracle | Command |
|---|---|---|
| Fail-first / regression | Before production implementation, the new focused tests should fail because `scripts/evidence_store.py` or its required behavior is absent. Record that expected failure; do not weaken imports/assertions to manufacture red. | `python3 -m unittest tests/test_evidence_store.py -v` |
| Targeted | All W1 storage, immutable-write, namespace, atomicity, and attempt-lifecycle tests pass against real temporary filesystem state. | `python3 -m unittest tests/test_evidence_store.py -v` |
| Owning suite | Existing run-evidence behavior remains unchanged, including its current Git-metadata and atomic-write behavior. | `python3 -m unittest tests/test_run_evidence.py -v` |
| Broader gate | Runtime-context and workflow-version suites remain green; implementer runs these after the targeted and owning suites. | `python3 -m unittest tests/test_runtime_context.py tests/test_workflow_version.py -v` |

The pre-edit baseline results and post-edit results must be reported separately.
A pre-existing baseline failure is a stop condition, not a W1 regression to fix.

## Expected contract impact

- Plan refs: architecture §§4–5 and 22, repo integration §3, implementation
  plan Task 1 / Storage, and work-breakdown W1 — `materialize`; collection
  contract §11.13 lifecycle semantics — `preserve` at the storage boundary.
- Current contract dependencies: none under `docs/contracts`; W1 consumes the
  checked-in v1.2.1 authority documents and the W0 serialization/dependency/
  concurrency decisions.
- Expected durable delta: a new local `EvidenceStore` /
  `GitMetadataEvidenceStore` API and on-disk namespace/lifecycle contract for
  W2–W6 consumers. W1 does not register record-schema or producer semantics.

## Stops and handoff

- Stop before edits if any W0 baseline suite fails; report the exact command and
  failure as pre-existing.
- Stop for ambiguous authority, overlap with user changes in either scoped
  file, unsafe permission needs, a required third-party dependency, material
  scope expansion, or inability to prove atomicity and lifecycle behavior at a
  real filesystem boundary.
- Treat the metadata budget as a checkpoint. If W1 cannot remain within it,
  return to task-brief design for decomposition rather than broadening scope.
- Preserve all pre-existing user work and leave the authority/work-breakdown
  documents unchanged.
- Next action: guided implementation after implementer self-preflight (and,
  optionally, the recommended focused verification-design pass).
- Required follow-on: immediately after implementation or correction, hand the
  completed bytes to a fresh independent acceptance reviewer.
