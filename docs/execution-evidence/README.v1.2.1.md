# Execution Evidence Design Pack

**Pack version:** 1.2.1  
**Status:** Draft for implementation  
**Date:** 2026-09-28  
**Repository:** `trusovn/personal-skills`

## Purpose

v1.2.1 is a consistency patch over v1.2. It keeps the same scope and architecture while clarifying record lifecycle, snapshot/profile semantics, identity, and provenance.

The goal remains:

> collect the smallest reproducible raw evidence set that can later support task-difficulty / execution-profile experiments without rebuilding historical context.

Authority order:

```text
execution-evidence-collection-contract.v1.2.1.md
    ↓
execution-evidence-architecture.v1.2.1.md
    ↓
execution-evidence-repo-integration.v1.2.1.md
    ↓
execution-evidence-implementation-plan.v1.2.1.md
```

A lower-level document may refine mechanics but must not silently redefine a higher-level decision.

---


## v1.2.1 consistency corrections

v1.2.1 does **not** expand the implementation scope.

It clarifies seven cross-document points:

1. `ExecutionAttempt` is lifecycle-managed until finalization:
   - PRE-RUN freezes before edits;
   - execution/check facts may accumulate while active;
   - the full attempt becomes immutable after finish/recovery finalization.

2. Project context is distinguished by role:
   - `TaskRevision.planning_project_snapshot_ref`;
   - `ExecutionAttempt.execution_project_snapshot_ref`.

3. Execution-profile concepts are distinct:
   - planner-recommended profile;
   - intended launch profile;
   - actual runtime profile.

4. The initial automatic review integration is acceptance review only.
   The generic `Association` model remains extensible to later review producers.

5. `TaskRevision` identity covers all semantically relevant task-revision content, not only raw artifact hashes.

6. Structured planning evidence records the producing planner/workflow provenance.

7. Document/pack version `1.2.1` is separate from evidence schema version `2`.

---

## v1.2 scope reductions

Compared with v1.1, v1.2 removes or defers machinery that is not needed for the first useful dataset.

### Removed from initial implementation

```text
standalone evidence_capture.py
execution_adapter.py framework
first-class ExecutionConditions record
first-class ExecutionTelemetry record
first-class CheckObservation record
first-class CollectorIdentity record
separate checks namespace
maintainability-review integration
legacy v1 compatibility reader/migration
detailed S3 key/auth/retry design
```

### Retained as simpler behavior

Artifact capture remains necessary, but is implemented as small helpers in `evidence_records.py`.

Execution conditions remain useful, but are an optional PRE-RUN section of `ExecutionAttempt`.

Telemetry remains useful, but is an optional EXECUTION section supplied only when naturally available.

Checks remain inline raw execution evidence.

Collector identity remains:

```text
schema_version
collector_fingerprint
```

inside the attempt.

The generic Association model remains capable of supporting more review types later, but initial skill integration is limited to acceptance review.

---

## Core records

The initial evidence model has four first-class concepts:

```text
ProjectSnapshot
TaskRevision
ExecutionAttempt
Association
```

Everything else is either:

- an inline section of those records;
- an existing authoritative mechanism such as runtime/workflow identity;
- or future derived analysis.

---

## Implementation stages

v1.2 reduces the implementation sequence to five bounded tasks:

1. **Evidence model + local storage + artifact snapshots**
2. **Run Evidence v2**
3. **Planner/decomposition integration**
4. **Guided execution + acceptance integration**
5. **Documentation, installation, regression closure**

`task-orchestrator` receives documentation direction only.

---

## Still explicitly out of scope

- S3 implementation;
- runner-specific telemetry instrumentation;
- maintainability-review integration;
- legacy evidence migration;
- dataset export;
- semantic similarity;
- TF-IDF;
- embeddings;
- RAG;
- ML/scoring/routing;
- repository dependency/AST metrics;
- task-orchestrator implementation redesign.

These remain follow-up consumers or integrations of the collected evidence.

---

## Versioning

Suggested document versioning:

- patch: wording clarification only;
- minor: compatible semantic/scope change;
- major: core evidence contract or architecture incompatibility.

v1.2.1 is a **patch-level consistency correction**. It does not add new evidence categories or implementation stages.
