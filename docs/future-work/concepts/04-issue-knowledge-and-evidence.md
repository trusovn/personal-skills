# Issue knowledge and execution evidence — direction

**Covers:** `I-01`–`I-04`, `E-01`–`E-04`. **Status:** Candidates and conditional extensions; not a new acceptance process.

## Desired outcomes

No consequential finding is silently lost between review/correction sessions; repeated failures can be distinguished from new defects; previous deferrals are reconsidered when their safety assumptions change; and factual run evidence is accessible across repositories and execution environments without granting every agent cloud credentials or access to host Git metadata.

## Issues, dispositions and conditional risk

**I-01 — Preserve every reported issue occurrence.** Each discovery, maintainability review, acceptance, task run or other producer should be linkable to an immutable occurrence with source, time/revision, location, observed consequence, and optional candidate underlying issue identity. Do **not** collapse distinct reports automatically or pretend uncertain deduplication is fact. Correlate repeated sightings, resolved/reopened issues, regressions and correction attempts. This supports detecting cycles rather than imposing an arbitrary maximum number of reviews.

**I-02 — Make consequential deferrals self-monitoring.** A deferral records decision authority, affected behavior, reason postponement is safe **now**, active safeguards/assumptions, owner, next action and `reconsider_when` triggers. A later change to a relied-on safeguard should mark the disposition for reassessment. The existing accepted-deferral artifact continues to represent *accepted deferrals only*, not a universal issue log. Avoid a second contradictory acceptance authority.

**I-03 — Use declared mechanical risk checks first.** With validated metadata, detect (a) changed/invalid deferral assumptions, (b) multiple issues weakening one critical guarantee, (c) known hazardous combinations and (d) affected downstream dependencies. Output `reassess`, `warning`, or `block deferral` **only where a current policy explicitly supports that result**. Missing links mean `unknown`, not safe. Such checks do not select the cheapest repair among several safeguards.

**I-04 — Add selective broader-context reasoning only if it changes decisions.** A triage skill/agent may explore new relationships, cumulative maintenance burden, cross-team effects and serious trade-offs. Historical replay should show meaningful decisions beyond deterministic rules and bounded local review before adding a persistent portfolio agent or graph engine. Count recurrence and engineering effort, not only total open issues.

Conceptual deferral example:

```yaml
issue: evidence-collector-014
status: deferred
safe_while: [validator_rejects_incomplete_evidence, experimental_runner_only]
reconsider_when: [validator_behavior_changes, runner_becomes_default]
```

This is an **example of decision semantics**, not a committed schema.

## Evidence capture, portability and retrieval

**E-01 — Remove `.git` write dependency through a bounded local spike.** Keep the existing run lifecycle as the producer interface where practical, but move durable state out of repository Git metadata. Prove worktree snapshots and identities in a disposable repo first; assess export of previous Git-embedded manifests and snapshot refs. External Git object storage can keep a tree identity without `.git` writes, but Git-tree references to original repo objects are **not** automatically self-contained portable archives. Record portability honestly.

**E-02 — Central local ingestion without exposing credentials.** A host-side collector/queue can serve normal terminal agents, sandboxes and future controllers; allow offline work, idempotency, retries, separate project/worktree/run identity and bounded concurrency. Agent environments submit observations; the future controller owns authoritative task/attempt transitions. If a desktop agent cannot access capture, say so and collect from its launcher only when possible.

**E-03 — Optional durable remote archive.** Use an S3-compatible backend if actual cross-host retention or query need justifies it. Keep the local collector operational without cloud access. Apply project upload policy, redaction/exclusions, output limits, authentication separation and artifact/snapshot retention rules. Do not upload source trees, transcripts or potential secrets by default. Cloud storage is a transport choice, not evidence quality.

**E-04 — Measure recurring delivery problems.** Query evidence for repeated failure/correction loops, time spent redoing the same probes, task and verification duration, source/installed version mismatch and changed-test regressions. Only compute metrics supported by real recorded data; later dashboards are optional presentation, not the first requirement.

## Ownership and trust rules

- Evidence collector: observed facts, exact run/check/identity linkage, storage and transport; **never** acceptance authority or synthetic scores.
- Discovery and acceptance: independent evidence assessment and decision records, each under its existing policy.
- Coordinator: accepted deferral recording and authorized continuation; no implied issue-fix priority from a checker alert.
- Future orchestration: task/attempt state and control flow, not rewriting past run observations.

**First decision:** Is a minimal issue-occurrence/deferral replay enough to show a real stale decision or recurring failure? Can a local evidence store prove no `.git` write requirement and recover existing data without losing provenance? Scope implementations independently from those measured results.
