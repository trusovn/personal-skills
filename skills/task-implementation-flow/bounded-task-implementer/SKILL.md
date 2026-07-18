---
name: bounded-task-implementer
description: Implement exactly one bounded task from a fresh preflight execution packet whose verdict is `ready`, including packet-authorized code, task-local tests, fail-first evidence, progressive verification, and a schema-valid worker result for independent review. Use whenever asked to execute, resume, or correct work from such a packet. Do not use for plans or task briefs without a ready packet, repository discovery, task design, preflight, acceptance review, orchestration, or work that requires undeclared paths, infrastructure, authority, permissions, or architecture.
---

# Bounded Task Implementer

Implement one ready execution packet and submit evidence for independent
review. Own the task-scoped code and tests, not the task contract, repository
readiness, orchestration state, or acceptance verdict.

Repository and user instructions outrank this skill. Preserve pre-existing user
work and never claim ownership of it.

## Required inputs

Require:

- repository root;
- path to one execution packet with artifact status `ready`;
- task-brief path referenced by that packet;
- path to `worker-result.schema.json`, or equivalent output-schema enforcement;
- durable result path and packet-declared verification-log locations; and
- for a resumed correction, the acceptance report or exact findings plus the
  prior implementation checkpoint.

If any input is absent, inconsistent, or not readable, do not inspect broadly
or edit. Return `needs_input` with `files_changed: []`, name the missing input in
`questions`, and make obtaining it the `next_action`. When the schema or result
path itself is missing, return the same schema-shaped JSON inline so the caller
can persist it after supplying the contract.

## Authority and mutation boundary

You may:

- inspect the packet, cited brief and authority, applicable instructions, exact
  allowed files, and closest precedents named by the packet;
- edit only packet-authorized production, test, fixture, and task-result paths;
- make small reversible implementation choices entailed by the packet and
  established repository precedent; and
- run only the exact commands authorized by the packet and run policy.

Do not edit the task brief, execution packet, official plan, tracker,
orchestration state, or pre-existing user work. Do not change an undeclared
path for cleanup or convenience. Do not create a public contract, shared
harness, canonical runner, dependency, or architecture boundary unless the
packet explicitly authorizes that exact change.

Do not commit, push, install dependencies, access the network, expand the
sandbox, use credentials, or run expensive, destructive, privileged, flaky, or
live checks unless the supplied policy explicitly authorizes that action.

## Workflow

1. Read applicable repository instructions, the entire ready packet, the
   referenced task brief sections needed for execution, the result schema, and
   any resumed acceptance findings. Treat the packet as the discovery budget;
   do not rediscover the repository.
2. Before the first edit, recalculate every packet freshness field and compare
   it exactly:
   - task-brief bytes and lowercase SHA-256 digest;
   - `HEAD`, or `unborn`;
   - exact `git status --short` snapshot;
   - separate lowercase SHA-256 index-blob and worktree digests for every
     pre-existing modified, staged, or untracked path, including each recorded
     `absent`, `deleted`, or `not_applicable` state;
   - dependency source and status digest;
   - applicable instruction and run-policy digests; and
   - task-specific environment or tool fingerprints.
   Any unexplained difference, including a changed index blob hidden by the
   same short-status text and unchanged worktree bytes, makes the packet stale.
   Stop without editing and route to `task-preflight`.
3. On a resumed correction, preserve the partial diff and validate against the
   prior implementation checkpoint. Changes already attributed to this same
   implementation thread are expected and do not alone stale the packet;
   unexplained external changes, changed authority, or widened findings do.
4. Confirm the packet's allowed paths do not overlap new user changes. Inspect
   only those paths, their named public entry points, tests, helpers, and closest
   precedents. Stop rather than merging around unclear ownership.
5. Establish the highest-risk fail-first evidence from the AC execution plan.
   Prefer the packet's existing targeted probe; otherwise add only a
   packet-authorized task-local test or one-use fixture. Run it before the
   production change and confirm it fails because the intended behavior is
   missing, not because the harness, command, or environment is broken.
6. Use `testing-discipline` when available for the fail-first proof, observable
   oracle, decisive boundary, negative behavior, deterministic fixture, and
   progressive verification. It does not expand scope or decide completion. If
   unavailable, apply those principles locally without writing a general test
   strategy.
7. Implement the minimum production and task-local test change that satisfies
   the packet. Trace each new repeated, resumed, retried, recovered, paginated,
   or migrated path through the packet's named legacy-assumption locations.
8. Use `repo-foundation` when available only to follow an already-authorized
   placement or canonical command convention. It cannot authorize a new path,
   shared helper, command, or structural refactor. If placement remains
   ambiguous, stop and route to task-brief design followed by fresh preflight.
9. Run exact targeted checks first. After they pass, run the owning suite and
   broader gate in the packet's order, only within its permission envelope.
   Record every command attempted, including fail-first runs, and its truthful
   outcome. Save required logs only at packet-declared runtime locations. Do not
   substitute an easier check for a required one.
10. Compare the final changed paths with the preflight baseline and allowed-path
    list. Separate task changes from pre-existing user changes, remove only
    temporary artifacts created by this implementation when safe, and record
    any unexplained or residual state as a blocker or risk.
11. Write the worker result to the durable result path and validate it against
    the supplied schema. A `complete` result is a submission to
    `task-acceptance-review`, never self-acceptance.

## Operational stops and routes

Stop immediately on stale inputs, dirty-path overlap, missing authority,
unexpected changed paths, scope expansion, an absent declared capability,
undeclared shared infrastructure, or a required check outside the permission
envelope.

After two materially different fixes leave the same targeted behavior failing,
stop ordinary editing. Preserve the bounded diff and record the observed
failure, both discarded hypotheses, the contract or component that owns the
failure, and one recommended next approach. Do not try a third fix silently.

At 30 tool calls, write a checkpoint to the packet-declared runtime location
with ACs proved, the failing gate, current hypothesis, estimated remaining work,
and whether narrow high-effort consultation is justified. Continue only when
the task remains bounded and the run policy allows it. Obey any earlier
repository context, time, or tool-call soft stop.

Route outcomes as follows:

- changed baseline, stale digest, missing path/helper/command, dependency
  change, or permission/environment executability failure: `blocked`, routed to
  `task-preflight`;
- missing artifact, user decision, or product/architecture/authority choice:
  `needs_input`, routed to the user or `task-brief-designer` as appropriate;
- exhausted in-scope fixes or an unrecoverable task-local execution failure:
  `failed`, with evidence and the smallest diagnostic or recovery action;
- requested wider paths or shared infrastructure: `needs_input`, routed to
  `task-brief-designer` and then fresh preflight;
- all required behavior and checks complete: `complete`, routed to independent
  `task-acceptance-review`.

An in-scope `CHANGES_REQUESTED` correction resumes this same implementation
thread. Do not restart from scratch. If the correction changes the contract,
scope, baseline authority, helpers, permissions, or dependencies, stop and
route through the owning earlier stage.

## Worker-result contract

Return exactly one JSON object conforming to the supplied
`worker-result.schema.json`; add no fields. Use every field semantically:

Record only confirmed evidence. Put unknown or unresolved facts in `questions`
or `risks` with their owner instead of guessing.

- `status`: exactly `complete`, `needs_input`, `blocked`, or `failed` under the
  routing rules above. `complete` never means accepted.
- `task_id`: copy the packet's task ID exactly.
- `summary`: begin with `bounded-task-implementer`, UTC creation time, and the
  task-brief and packet paths; then concisely map each AC to the implemented
  behavior and evidence without claiming acceptance.
- `files_changed`: exact repository-relative paths changed by this task only,
  including authorized new files; exclude unchanged and pre-existing user
  paths.
- `verification`: include every command run or required but not run. Preserve
  exact command text, use only `passed`, `failed`, or `not_run`, and summarize
  the observed signal or the precise reason it was skipped.
- `decisions`: record only local reversible choices entailed by authority, with
  their reason and `scope: task`. Do not manufacture a `plan` decision; leave
  the array empty when no implementation choice was needed.
- `questions`: record each missing input or authority issue, a concrete
  recommendation, and whether it blocks. A `complete` result has no blocking
  question.
- `risks`: list residual gaps, skipped stronger evidence, environmental limits,
  or known follow-up risk without disguising a failed requirement as risk.
- `next_action`: name one exact route or action, such as independent acceptance
  review, fresh preflight, brief redesign, a user decision, or a bounded
  diagnostic step.

Validate the JSON after writing it. If schema validation fails, correct only
the result artifact and validate again; do not describe an invalid result as
complete.

## Reuse and independence boundaries

This skill specializes implementation and reuses only the narrow evidence and
placement roles described above. It does not absorb `testing-discipline` or
`repo-foundation`, and it does not invoke `senior-code-review` to approve its
own work. Independent acceptance owns review findings and the verdict;
`task-orchestrator` alone owns stage transitions, tracker updates, acceptance,
and authorized commits.

Do not launch subagents, modify `task-orchestrator`, run live comparisons, or
advance another task as part of normal execution.

## Definition of done

- Freshness and dirty ownership were validated before the first edit.
- Every changed path is authorized and traces directly to the packet.
- Highest-risk fail-first evidence failed for the intended reason before the
  production change when feasible.
- Packet-required targeted and broader checks have truthful recorded outcomes.
- The result validates against the supplied schema and distinguishes task work
  from pre-existing user changes.
- `complete` routes to independent review with no self-acceptance claim.
