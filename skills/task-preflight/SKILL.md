---
name: task-preflight
description: Prove whether one `ready_for_preflight` task brief is executable against the current repository and run policy, then produce a fresh copy-pasteable Markdown execution packet with exactly a `ready` or `blocked` status. Use when asked to preflight, readiness-check, validate, or prepare an execution packet for a specific approved task brief. Do not use for generic repository exploration, brief repair or design, implementation, acceptance review, or requests that do not supply a task brief; block instead of inventing missing commands, helpers, authority, or scope.
---

# Task Preflight

Certify current-state executability for one task brief without changing the
repository. Own factual repository inspection and the readiness verdict, not
design, implementation, or acceptance.

Repository and user instructions outrank this skill. Preserve existing user
work and never claim ownership of it.

## Required inputs

Require:

- repository root;
- path to one task brief whose status is `ready_for_preflight`;
- current dependency or tracker state and the authoritative source path;
- run policy, or explicit permission, commit, verification, and stop policy;
- durable run-directory path for the output packet.

Use `UNKNOWN` only while inspecting. If an input remains missing, the brief has
another status, or the run directory is not authorized, produce a `blocked`
packet naming the missing evidence, owner, and smallest next action. Do not
repair the input or infer policy.

## Authority and read-only boundary

You may read repository state, resolve paths and commands, perform the brief's
named searches, and run cheap local non-destructive baseline checks already
authorized by the run policy.

Do not edit source, tests, documentation, configuration, dependencies, helper
tools, tracker state, task briefs, or orchestration state. Prefer checks that do
not create caches, coverage data, snapshots, logs, or generated files. If an
authorized command creates incidental files, record the exact paths and their
ownership; the packet cannot claim a clean baseline until their disposition is
explicit.

Ask before a slow, flaky, privileged, destructive, live-networked, or otherwise
costly check unless the supplied policy already authorizes that exact class.
Declining or lacking authorization is evidence for a gap or blocker, not
permission to weaken the task contract.

## Workflow

1. Read applicable repository instructions, the entire task brief, its cited
   authority needed to interpret the contract, the dependency source, and the
   run policy. Confirm the brief status is `ready_for_preflight`; do not silently
   reinterpret or repair it.
2. Capture the freshness baseline before other checks:
   - exact brief path and lowercase SHA-256 digest of its bytes;
   - current `HEAD`, or `unborn` when no commit exists;
   - exact `git status --short` output;
   - lowercase SHA-256 content digests for every pre-existing modified, staged,
     or untracked path, recording missing/deleted paths explicitly;
   - dependency status plus the path and digest of its authoritative source;
   - every applicable instruction file plus its digest; and
   - run-policy identifier plus the path and digest of each policy source.
   Add task-specific environment or tool fingerprints when executability
   depends on facts outside Git.
3. Confirm dependency state, entry criteria, allowed paths, ownership
   boundaries, permission envelope, and commit policy. Separate pre-existing
   user work from task-owned future changes. A dirty allowed path with unknown
   or user ownership is an overlap; do not assume the implementer can merge it.
4. Resolve every cited file, public entry point, precedent, helper, fixture,
   schema, and candidate command against the current tree. Record exact paths
   and interfaces. An absent required capability is a blocker, not new
   implementation scope.
5. Perform the brief's task-specific legacy-assumption searches. Record exact
   relevant locations and what each finding means for implementation. Findings
   may expose a defective brief, but preflight does not redesign it.
6. For every acceptance criterion, confirm an executable oracle at the named
   real boundary. Use `testing-discipline` when available to assess oracle
   independence, decisive boundary coverage, negative evidence, repeated or
   recovery flows, and determinism. It does not own the readiness verdict. If
   unavailable, apply those five checks locally without copying a general test
   strategy into the packet.
7. Use `repo-foundation` when available to confirm existing test/helper
   placement and canonical command ownership. It may identify repository
   convention but does not authorize a new helper or repair a missing command.
   If unavailable, follow cited local precedent and block on material placement
   uncertainty.
8. Resolve exact targeted and broader commands. For each command record the
   copy-pasteable text, working directory, required environment, purpose,
   expected signal, cost class, authorization requirement, whether it ran, and
   its truthful result. Do not leave command families, placeholders, or syntax
   discovery to the implementer.
9. Run only authorized cheap, local, non-destructive baseline checks. Start with
   the narrowest relevant check; broaden only after it passes and when the
   policy permits. Record output sufficient to distinguish a passing baseline,
   expected fail-first behavior, environment failure, and product failure.
10. Re-read the brief bytes and recapture `HEAD`, `git status --short`, dirty-path
    content digests, dependency source, instruction files, policy sources, and
    any task-specific fingerprints. Any unexplained change makes the packet
    stale. Compare incidental command artifacts with the recorded baseline.
11. Read `references/execution-packet-template.md`, write exactly one packet in
    the authorized run directory, and assign `ready` only when every ready
    criterion below is proved.

## Ready criteria

Return `ready` only when:

- the brief is `ready_for_preflight` and stayed byte-for-byte unchanged;
- dependencies and entry criteria are true;
- repository state is explained and no dirty-path ownership overlaps the task;
- all required paths, public entry points, helpers, and oracles exist;
- every targeted command is exact and locally executable under the run policy;
- required baseline checks pass, or an explicitly authorized gap names its
  owner and follow-up without undermining executability; and
- implementation needs no unresolved requirement, authority, architecture, or
  scope decision.

Otherwise return `blocked`. A blocked packet is durable evidence, not an
execution packet.

## Output contract

Use the fixed headings and tables in
`references/execution-packet-template.md`. Produce exactly one Markdown packet
with exactly one artifact status:

- `ready`: a fresh, self-contained execution packet that an implementer may use;
- `blocked`: evidence of the failed condition, its owning stage, and the
  smallest next action. It must not instruct implementation to begin.

Link to large inputs by repository-relative or absolute path. Distinguish
confirmed facts, assumptions, decisions, gaps, and unresolved items. Include
task ID, repository root, producing stage, creation time, authoritative input
paths and digests, baseline identity, exact commands, permission and commit
envelope, stop conditions, and implementer result requirements.

## Stop and routing rules

- Route a missing or ambiguous requirement, AC, product rule, architecture, or
  authority to `task-brief-designer`, or to the user when authority is absent.
- Keep current-state failures here: stale brief digest, changed baseline, dirty
  overlap, missing path/helper, invalid command, failed entry criterion, or
  unauthorized required check all yield `blocked` with exact evidence.
- Route requested wider paths or new shared infrastructure to
  `task-brief-designer`, followed by a fresh preflight.
- Send only a fresh `ready` packet to `bounded-task-implementer`. Never mark a
  task ready because implementation could discover or repair what is missing.

Do not launch subagents, modify `task-orchestrator`, run live comparisons, start
implementation, or approve implementation as part of normal preflight.

## Definition of done

- The packet is independently usable without this conversation.
- Every freshness field is recorded and unchanged at packet creation.
- Every AC has an executable, task-appropriate oracle at its decisive boundary.
- Commands are exact, scoped, authorized, and truthful about baseline results.
- Scope, dirty ownership, dependencies, permissions, gaps, and routes are
  explicit.
- Only a fully proved packet is marked `ready`.
