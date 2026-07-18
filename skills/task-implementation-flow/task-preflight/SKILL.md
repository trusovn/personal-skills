---
name: task-preflight
description: Check whether one bounded task is safe and executable against the current repository, then return a concise ready or blocked result. Use when asked to preflight, readiness-check, resolve task commands or ownership, or prepare a durable execution packet. Default to a lightweight guided check; use the full freshness packet only for explicit high-assurance or orchestrated work. Do not implement, redesign requirements, or treat missing stage paperwork alone as a blocker.
---

# Task Preflight

Resolve current-state uncertainty before implementation. Spend effort on facts
that can change the task or make an edit unsafe, not on artifact ceremony.

Repository and user instructions outrank this skill. Preserve existing user
work and never claim ownership of it.

## Choose the profile

Use `guided` by default.

Use `high-assurance` when explicitly requested, when the input brief has status
`ready_for_preflight`, when an orchestrator requires a durable packet, or when
exact freshness/ownership evidence is proportionate to the task's risk.

### Guided

- Accept a `ready` task brief or a bounded user request with clear authority and
  scope.
- Return a compact inline readiness result unless the user requests a file.
- Inspect only enough repository state to protect user work, confirm scope and
  dependencies, resolve the targeted command, and establish a decisive oracle.
- The standalone stage is optional; `bounded-task-implementer` may perform the
  same compact self-preflight.

### High assurance

- Require the `ready_for_preflight` brief, run policy, dependency source, and an
  authorized durable packet path.
- Capture exact baseline and content identities so another agent or process can
  safely rely on the packet later.
- Produce the complete packet from
  `references/execution-packet-template.md`.

## Guided workflow

1. Read applicable instructions and the task/request. Confirm the expected
   behavior is sufficiently clear; route a material product or architecture
   gap back to the owner rather than guessing.
2. Inspect `git status --short` and the intended change area. Identify
   pre-existing user changes and stop on ownership overlap that cannot be
   safely separated.
3. Confirm dependencies and entry conditions that matter now. Do not require a
   tracker or digest merely because high-assurance mode would record one.
4. Resolve the relevant implementation paths, closest tests, public entry
   point, and lowest-cost targeted command. Focused discovery is allowed; do
   not perform generic repository archaeology.
5. For each acceptance criterion, confirm an observable oracle. Require the
   real boundary only where unit/module evidence cannot prove wiring,
   persistence, process, database, filesystem, concurrency, recovery,
   authorization, or another material behavior.
6. Run an authorized cheap local baseline only when it distinguishes a broken
   environment from the intended fail-first state or materially lowers risk.
   Ask before slow, flaky, privileged, destructive, live, or networked checks
   unless already authorized.
7. Return `ready` with the exact targeted command, scope/ownership result,
   meaningful gaps, and implementation stops; otherwise return `blocked` with
   the evidence, owner, and smallest next action.

## Guided blockers and warnings

Block when:

- authority or an acceptance oracle is materially ambiguous;
- a required dependency or capability is absent;
- intended paths overlap user-owned work without permission to merge;
- the targeted command cannot execute and implementation depends on it;
- required work exceeds the allowed scope or permission envelope; or
- safe execution needs an unauthorized destructive, privileged, live, or
  networked action.

Do not block guided work solely because there is no external packet directory,
content-digest ledger, worker-result schema, exact broader gate, or separate
preflight artifact. Record relevant uncertainty and let implementation resolve
ordinary local details before editing.

## High-assurance workflow

1. Read the complete brief, cited authority, applicable instructions,
   dependency source, and run policy. Confirm status `ready_for_preflight`.
2. Resolve the durable packet path first. It must be outside the repository or
   already ignored and status-neutral; otherwise return blocked content without
   writing it.
3. Capture before checks:
   - brief bytes and lowercase SHA-256;
   - `HEAD` or `unborn` and exact `git status --short`;
   - separate index-blob and worktree digests/states for every pre-existing
     dirty path, including absent/deleted/not-applicable states;
   - dependency, instruction, and run-policy source digests; and
   - task-specific environment/tool fingerprints when executability depends on
     them.
4. Confirm dependencies, exact allowed paths, dirty ownership, permissions,
   commit policy, public entry points, helpers, fixtures, oracles, and legacy
   assumptions named by the brief. An absent required capability is a blocker,
   not new implementation scope.
5. Resolve every required targeted and broader command as copy-pasteable text
   with working directory, environment, purpose, expected signal, cost,
   authorization, whether it ran, and truthful result.
6. Run only authorized cheap local baselines, narrowest first. Record incidental
   artifacts and do not claim a clean baseline until their disposition is
   explicit.
7. Recapture all freshness values before and after packet creation. Any
   unexplained change or status-affecting packet write blocks readiness.
8. Write exactly one packet using
   `references/execution-packet-template.md`.

## Evidence integrity

A digest stored inside or beside mutable evidence proves consistency only. Do
not describe it as immutable or tamper-proof unless an independently protected
anchor authenticates it. If the task requires stronger immutability, block or
record the narrower approved threat model rather than overstating the oracle.

## Output contract

Use exactly one status:

- `ready`: implementation can begin under the recorded scope and policy;
- `blocked`: a concrete failed condition has an owner and smallest next action.

For guided mode, default to a short human-readable result containing:

- status and basis;
- confirmed scope and user-work ownership;
- targeted test/verification command and oracle;
- warnings or skipped stronger checks; and
- exact next action.

For high-assurance mode, use the full packet template and durable path. A
blocked packet is evidence, not authorization to implement.

## Boundaries and routing

- Route contract or authority defects to `task-brief-designer` or the user.
- Keep current-state failures—dirty overlap, dependency failure, missing path
  or helper, invalid command, environment, or permissions—here.
- Route wider scope or shared infrastructure through brief design.
- Do not edit source/tests/docs/config/dependencies, implement, approve, update
  trackers, launch subagents, or modify orchestration state.

## Definition of done

- The readiness result is proportionate to the selected profile.
- Scope, user-work ownership, dependencies, command, oracle, permissions, and
  meaningful gaps are explicit.
- Guided mode avoids freshness paperwork that no later process will consume.
- High-assurance mode remains independently reproducible and freshness-safe.
