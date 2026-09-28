# Execution Evidence v2 planning pack

This directory stores the implementation-planning material for Execution Evidence v2.

## Authority

The approved design authority remains, in order:

1. `execution-evidence-collection-contract.v1.2.1.md`
2. `execution-evidence-architecture.v1.2.1.md`
3. `execution-evidence-repo-integration.v1.2.1.md`
4. `execution-evidence-implementation-plan.v1.2.1.md`

The execution aids below are subordinate and must not redefine those documents:

- `execution-evidence-work-breakdown.v1.2.1.md`
- `execution-evidence-verification-matrix.v1.2.1.md`
- `W0-result.md`

`README.v1.2.1.md` is the design-pack overview.

## Exact source pack snapshot

The five source documents supplied for v1.2.1 are preserved byte-for-byte in:

```text
design-pack.v1.2.1.tar.xz.b64
```

To materialize them in a local checkout:

```bash
base64 --decode docs/execution-evidence/design-pack.v1.2.1.tar.xz.b64 \
  > /tmp/execution-evidence-design-pack-v1.2.1.tar.xz
mkdir -p /tmp/execution-evidence-design-pack-v1.2.1
tar -xJf /tmp/execution-evidence-design-pack-v1.2.1.tar.xz \
  -C /tmp/execution-evidence-design-pack-v1.2.1
```

The archive contains:

```text
README.v1.2.1.md
execution-evidence-collection-contract.v1.2.1.md
execution-evidence-architecture.v1.2.1.md
execution-evidence-repo-integration.v1.2.1.md
execution-evidence-implementation-plan.v1.2.1.md
```

The encoded archive exists to preserve the exact source snapshot without rewriting the approved documents during W0. Agents working on implementation should read/materialize the source pack before changing code.

## Work sequence

The implementation sequence is operationally split as:

```text
W0 baseline + small implementation decisions
W1 local evidence storage
W2 core records/schema/artifact helpers
W3 Run Evidence v2
W4 planner/decomposition integration
W5 bounded-task-implementer integration
W6 acceptance-review association
W7 documentation/installation
W8 contract closure/regression
```

The approved five implementation stages in the design pack remain authoritative; this split exists only to make each work item small enough to implement and review independently.

## Scope principle

The implementation should remain lightweight instrumentation around the existing workflow. Prefer cheap mechanical collection of exact bytes, hashes, timestamps, already-known structured values, and existing Git/runtime/workflow facts. Do not turn this work into a new workflow platform, telemetry framework, analytics pipeline, or task-scoring system.
