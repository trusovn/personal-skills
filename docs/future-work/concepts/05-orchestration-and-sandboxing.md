# Orchestration and sandboxed delivery — direction

**Covers:** `O-01`–`O-05`. **Status:** Later architecture and experiments, not a current executor project.

## Desired outcomes

A trusted controller can automate repetitive handoffs and recovery while preserving independent decisions and auditable evidence. Eventually, implementation and verification may happen in restricted, reproducible repository clones, and the original repository is updated only with the exact independently qualified candidate.

## Existing baseline

The source already contains an experimental `task-orchestrator` with `init`,
`run-next` and `inspect` for supplied manifests and policies. The
[repository status](../../../README.md#task-orchestrator-status) describes its
limits: semantic correction loops, safe recovery, atomic acceptance/dependency
release and unattended end-to-end execution are not supplied. The capabilities
below are extensions to evaluate, not a claim that no controller exists or that
its current implementation is qualified for unattended use.

## Orchestration capabilities

**O-01 — Machine-admissible stage outcomes.** Define minimal typed outcomes and trusted evidence about invoked versions, file effects, completed checks, unresolved rows and reviewer independence. A structured agent claim is not by itself a trusted observation: collect filesystem/repository/command facts across the proper boundary.

**O-02 — Controller-owned transitions.** Encode the currently approved conditional stages, blockers, incomplete evidence, correction routing, authorization and dependency release as deterministic state transitions. A controller can say which stage is permitted next; independent reviewers still judge semantic quality, risk and acceptance.

**O-03 — Retained runnable workflow versions and recovery.** Bind active attempts to actual runnable skill/policy bundles, not only a version label or digest of unavailable bytes. Interrupted and resumed runs must not silently mix incompatible instructions, test capability or authority. Recovery should respect external changes since the captured baseline.

**O-04 — Native execution telemetry.** Instrument stage boundaries and correlate task, attempt, run and evidence IDs without reading agent transcripts as the source of truth. Decide whether the launcher/controller or collector owns each observation; prevent duplicate competing records.

**O-05 — Sandbox, independent verification and controlled promotion.** Introduce as a later selectable execution mode, not a replacement for the human-coordinated flow now.

## O-05 conceptual trust flow

1. **Trusted preparation.** Controller pins the intended target repository revision, task authority, writable scope, policy version and permitted test capabilities.
2. **Isolated implementation.** The implementer works in a clone or equivalent isolated filesystem with default-deny host writes, scoped network and no unnecessary secrets. It submits a candidate commit/patch plus observed checks; it cannot update the protected original.
3. **Fresh independent verification.** A distinct verifier receives the immutable candidate and a trusted target baseline. It examines the **exact proposed change**, including tests, workflows, dependencies and instructions, and executes tests using an appropriately isolated environment with only the required capabilities. Verification must not trust mutable implementation workspace state.
4. **Trusted promotion.** Controller checks candidate/review identity, authorization and target revision. If the base has changed or merge resolution alters the candidate, re-evaluate the new resulting bytes; do not silently apply an old green result. Only the controller may update the original repository.
5. **Durable outcome.** Retain accepted/rejected candidate IDs, proof limits, merge effects and correction/retry lineage. A rejected candidate returns to bounded correction, not automatic self-approval.

## Repo-specific verification access

Per-repository instructions should declare supported test entry points, fixtures, externally required services, sensitive resources, approved network destinations and forbidden operations. Those instructions may inform a capability profile, but **sandbox enforcement must be controlled by trusted configuration**, not rewritten by an untrusted candidate. A verifying sandbox may need broader test access than an implementing sandbox; keep its credentials scoped, ephemeral and inaccessible to the candidate where possible. Treat generated code, dependency install scripts and test commands as potentially untrusted execution.

The architecture may use Docker `sbx` or another runner. Feasibility, permission granularity, mounted secrets, filesystem/network containment, cross-platform development workflows and the security of Git promotion need a small practical test before choosing one technology.

## Earliest useful experiment

Use a disposable repository with a known baseline and two candidate changes: one valid and one with a forbidden file edit, stale target, unsafe merge or intentionally failing cross-boundary test. Require independent verification of staged resulting bytes; only a trusted simulated promoter decides what could enter the protected base. Record whether repository test access works without giving implementers full host access.

## Key cautions

- Sandbox restrictions can replace some long agent-facing **don't** instructions, but not the obligation to understand scope, tests and truthful reporting.
- A sandbox is not a guarantee against exfiltration if network, credentials, file mounts, dependency execution or output paths are permissive.
- Verification of an isolated candidate does not prove a *different* conflict-resolved merge result.
- Do not make O-05 or cloud evidence services a prerequisite to early system-verification pilots.
- Full production orchestration should follow a stable independent standalone workflow; start with one narrow trusted boundary at a time.
