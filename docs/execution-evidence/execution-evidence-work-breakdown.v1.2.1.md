# Execution Evidence v2 — Work Breakdown

**Design-pack version:** 1.2.1  
**Evidence schema target:** 2  
**Status:** Execution plan  
**Authority:** subordinate to, in order:

1. `execution-evidence-collection-contract.v1.2.1.md`
2. `execution-evidence-architecture.v1.2.1.md`
3. `execution-evidence-repo-integration.v1.2.1.md`
4. `execution-evidence-implementation-plan.v1.2.1.md`

This document does not redefine scope or architecture. It only splits the approved implementation into small, reviewable work units.

## Execution principles

- Reuse `scripts/workflow_version.py` for workflow identity.
- Reuse `scripts/runtime_context.py` for trusted runtime identity.
- Reuse the existing Git before/after snapshot mechanism in `scripts/run_evidence.py`.
- Prefer mechanically cheap collection: hashes, small JSON records, timestamps, supplied structured values, and existing Git snapshots.
- Do not add collection-time scoring, repository analysis, AST/dependency analysis, embeddings, similarity, RAG, ML, or routing.
- Evidence remains best-effort for ordinary guided execution.
- Do not add an adapter framework, query layer, database abstraction, or standalone artifact-capture subsystem.

## W0 — Baseline and execution scaffolding

**Goal:** establish the implementation baseline and lock only the few mechanics that would otherwise cause churn in W1/W2.

### W0 decisions

1. **Canonical serialization / content identity**
   - Use one canonical JSON encoding helper for content-derived IDs.
   - UTF-8 only.
   - Object keys sorted deterministically.
   - Compact separators; no insignificant whitespace in hash input.
   - Preserve list order unless a specific field is semantically defined as an unordered set and normalized before serialization.
   - Omitted and explicit `null` are different inputs unless a record constructor deliberately normalizes them before hashing.
   - Absolute local paths must never participate in logical record identity.
   - Record-specific identity payloads remain defined by the approved architecture/schema and tests; this rule defines encoding, not which fields belong in each identity.

2. **Producer invocation boundary**
   - Artifact construction remains in `scripts/evidence_records.py` using explicit-input helpers.
   - Do not add `evidence_capture.py`, an adapter framework, recursive document discovery, or a second parser/LLM.
   - If a Markdown skill needs a shell-facing entry point later, expose the smallest command surface through an already-planned evidence module while keeping construction logic in `evidence_records.py`.
   - Exact command syntax is an implementation detail for W2/W4, not a new architecture decision.

3. **Runtime dependencies**
   - Default to the Python standard library for the v2 evidence foundation and CLI.
   - Add a third-party runtime dependency only if a concrete requirement cannot reasonably be met without it; document and review that separately.

4. **Concurrency assumption**
   - Preserve the current CLI/workflow behavior of one active bounded implementation attempt per worktree.
   - Do not encode a global single-attempt restriction into `EvidenceStore`; store operations address attempts by ID.
   - Multi-agent worktree coordination/locking remains out of scope.

5. **Execution aids are non-authoritative**
   - This work breakdown and the verification matrix are operational aids below the approved four-document authority chain.
   - They may refine sequencing and checks but may not silently change scope or architecture.

### W0 baseline

- Baseline branch: `main`.
- Baseline commit: `0855a914947347516c467dc764709b54d50db5ea`.
- Existing owning test modules confirmed in the repository:
  - `tests/test_run_evidence.py`
  - `tests/test_runtime_context.py`
  - `tests/test_workflow_version.py`
- Current shared-script surface confirmed:
  - `scripts/run_evidence.py`
  - `scripts/workflow_version.py`
  - `scripts/runtime_context.py`
  - `scripts/runtime-context.schema.v1.json`
- The current workflow-version tests already contain a realistic ignored-`.agents/` installation case.
- No commit statuses/CI checks are published for the baseline commit through the connected GitHub interface.
- The current execution environment does not provide a checked-out authenticated Git worktree for this repository, so the baseline unittest commands could not be executed here. This is an explicit unverified baseline item, not a claimed pass. W1 must run the three existing suites before changing code and stop if a pre-existing failure is discovered.

### W0 exit

- Authority pack stored in the repository.
- Execution aids stored next to it.
- W0 decisions recorded without modifying the approved authority documents.
- Baseline commit and verification limitation recorded.

## W1 — Local evidence storage

Add only:

```text
scripts/evidence_store.py
tests/test_evidence_store.py
```

Implement the small persistence surface approved by the architecture:

```text
put_blob
put_immutable_record
create_attempt
update_active_attempt
finalize_attempt
get_record
record_exists
```

Initial root:

```text
<git-dir>/personal-skills/evidence/v2/
```

Keep this unit storage-only. No task planning, runtime discovery, workflow identity, review semantics, telemetry collection, feature extraction, or `run_evidence.py` migration.

## W2 — Core records, schema, and artifact helpers

Add:

```text
scripts/evidence_records.py
scripts/execution-evidence.schema.v2.json
tests/test_evidence_records.py
```

Implement only `ProjectSnapshot`, `TaskRevision`, `ExecutionAttempt`, and `Association`, plus small explicit-input artifact helpers and collector fingerprint support. Keep conditions, telemetry, checks, and collector identity inline rather than new first-class models.

## W3 — Run Evidence v2

Refactor the existing lifecycle onto W1/W2 while preserving existing repository/workflow/runtime mechanisms. Support direct/formal input, PRE-RUN freezing, inline checks, optional supplied conditions/telemetry, finish/recovery, POST-RUN repository state, relations, and generic association support. Do not add runner scraping or full diff/stat calculation.

## W4 — TaskRevision production in task-brief-designer

Best-effort capture explicit project/task artifacts, small planner context already produced by the planner, estimates, profile/reasoning recommendation, split decision, decomposition relationships, and producer provenance. Missing planner fields stay missing. Do not add a parser/LLM to backfill them.

## W5 — bounded-task-implementer integration

Wrap normal bounded execution with best-effort evidence: begin before edits, preserve direct/formal input, record canonical checks once, finish factually, and retain attempt ID for review handoff. Missing/broken optional evidence tooling remains non-fatal.

## W6 — Acceptance-review association

When a reliable attempt ID exists, add an immutable `acceptance_review` Association with factual status, durable report reference when present, provenance, and collection time. Do not guess attempt IDs or change review semantics.

## W7 — Documentation and installation

Update the root/task-flow/run-evidence/task-artifact/orchestrator-direction documentation and prove the approved `.agents/scripts/` installation, including repositories that ignore `.agents/`. Orchestrator implementation remains unchanged.

## W8 — Contract closure and regression gate

Use `execution-evidence-verification-matrix.v1.2.1.md` as the closure checklist. Run the new evidence tests, existing workflow/runtime tests, affected skill evals/tests, and realistic installation coverage.

## Recommended branch sequence

```text
evidence-v2/00-plan
evidence-v2/01-store
evidence-v2/02-records
evidence-v2/03-run-evidence
evidence-v2/04-planner
evidence-v2/05-implementer
evidence-v2/06-acceptance
evidence-v2/07-install-regression
```

Each dependent branch should start from current `main` after the preceding work is merged, rather than keeping a parallel stack of long-lived branches.

## Scope-stop rules

Treat the following as separate follow-up work if implementation pressure starts introducing them:

- runner-specific telemetry instrumentation;
- adapter framework;
- S3/object-storage backend or remote sync;
- dataset export or query/index/database layer;
- full diff/patch metrics at collection time;
- repository feature extraction, AST/dependency analysis;
- TF-IDF, embeddings, similarity, RAG, ML, scoring, routing;
- maintainability-review integration;
- legacy v1 migration/reader;
- task-orchestrator implementation redesign.

## Definition of done

The v2 implementation is done when the existing workflow can cheaply and durably preserve the approved raw PRE-RUN, EXECUTION, POST-RUN, provenance, decomposition/relation, and acceptance evidence without relying on transient conversation context. The result should remain instrumentation around the existing workflow, not a new workflow platform.
