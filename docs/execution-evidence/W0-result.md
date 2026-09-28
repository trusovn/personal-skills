# Execution Evidence v2 — W0 Result

**Work item:** W0 — Baseline and execution scaffolding  
**Branch:** `evidence-v2/00-plan`  
**Baseline:** `main` at `0855a914947347516c467dc764709b54d50db5ea`  
**Status:** Complete, with one explicitly unverified baseline item

## What W0 changed

W0 intentionally made no production-code, schema, skill, or runtime behavior changes.

It added:

- the Execution Evidence v1.2.1 pack overview;
- an exact byte-preserving archive of the five supplied authority documents;
- an execution work breakdown;
- a contract-to-verification matrix;
- this result record;
- repository discoverability for the planning pack.

The approved authority chain is unchanged.

## Source-pack integrity

The exact supplied source documents are stored in `design-pack.v1.2.1.tar.xz.b64`.

Original SHA-256 digests:

```text
README.v1.2.1.md
6c272db2ad80288626dcf1713c993b32db3b43e9d5eabc74f60c9b1e2a35d5e9

execution-evidence-collection-contract.v1.2.1.md
4858ebb2cfe95ace7a59f8f964dd144ccdeb77c4248df1dcde5566478f5af1f1

execution-evidence-architecture.v1.2.1.md
aa99ef5b5187f3a4f48e6517783e0b42b00781311aa193a26a0d4871a83a792b

execution-evidence-repo-integration.v1.2.1.md
abe399aab6f3f95c23b736090808dea600bbd8de80f6aa70d30d06f7b11fd843

execution-evidence-implementation-plan.v1.2.1.md
0865b87493115048ce4737f3077bc67715163db5adc9dc7ecea504716492e472
```

Agents may materialize the archive with the commands in `docs/execution-evidence/README.md` and verify the hashes if needed.

## Small implementation decisions locked by W0

These are implementation mechanics only and do not expand the approved architecture.

### Canonical serialization

Use one canonical JSON encoding for content-derived identities:

- UTF-8;
- sorted object keys;
- compact deterministic separators;
- list order preserved unless a field is explicitly normalized as unordered;
- omitted and explicit `null` remain distinct unless deliberately normalized by the record constructor;
- absolute local paths never participate in logical record identity.

The record/schema work still owns which fields belong in each identity payload.

### Producer invocation boundary

- Keep artifact construction in `scripts/evidence_records.py` using explicit-input helpers.
- Do not add `evidence_capture.py`, recursive artifact discovery, an execution-adapter framework, or an evidence-specific parser/LLM.
- If a skill later needs a shell-facing entry point, expose the smallest interface through an already-planned evidence module and keep record construction logic in `evidence_records.py`.

### Runtime dependencies

Use the Python standard library by default. A new third-party runtime dependency requires a concrete need and separate justification.

### Concurrency

Preserve one-active-bounded-attempt-per-worktree behavior at the CLI/workflow level for this implementation series. Do not make that a storage invariant in `EvidenceStore`. Multi-agent locking/coordination remains out of scope.

## Baseline inspection

Confirmed on `main`:

```text
scripts/run_evidence.py
scripts/workflow_version.py
scripts/runtime_context.py
scripts/runtime-context.schema.v1.json

tests/test_run_evidence.py
tests/test_runtime_context.py
tests/test_workflow_version.py
```

The existing workflow-version tests include project-local `.agents/` discovery and an ignored-`.agents/` installation case.

The baseline commit publishes no GitHub commit-status checks through the connected repository interface.

## Baseline test limitation

The intended W0 baseline commands are:

```bash
python3 -m unittest tests/test_run_evidence.py -v
python3 -m unittest tests/test_runtime_context.py -v
python3 -m unittest tests/test_workflow_version.py -v
```

They were **not executed in this W0 session** because the available repository connection supports GitHub repository reads/writes but does not expose an authenticated local checkout or command-execution surface for that checkout, and the isolated local container cannot reach GitHub to clone it.

This is recorded as **UNVERIFIED**, not PASS.

Before W1 changes production code, the W1 agent must run those three baseline suites in its actual checkout. If any fail before W1 edits, the agent must record the failure as pre-existing and avoid hiding it inside W1 changes.

## W0 scope check

W0 did not introduce:

- evidence storage/model code;
- schema v2;
- `run_evidence.py` changes;
- skill changes;
- telemetry instrumentation;
- adapters;
- analytics/features/scoring;
- S3/remote storage;
- legacy migration;
- orchestrator implementation changes.

## Next work item

Proceed with **W1 — Local evidence storage only**.

W1 should add `scripts/evidence_store.py` and `tests/test_evidence_store.py`, keep the implementation standard-library-only unless a real blocker appears, and avoid pulling W2 record semantics or W3 collector migration into the branch.
