---
name: task-preflight
description: Check whether one bounded task is safe and executable against the current repository, then return a concise ready or blocked result. Use when asked to preflight, readiness-check, resolve task commands or ownership, or prepare a durable execution packet. Require derived verification and compact durable readiness for executable packages; keep direct requests inline and exact freshness for high-assurance work. Do not implement or redesign requirements.
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
- When the caller supplies a durable task brief, require the package form
  `<task-package>/brief.md`. Refuse a direct legacy brief such as
  `docs/tasks/API-31.md`, even when no `verification.md` exists, and route it to
  `task-brief-designer` for package normalization. A bounded conversational
  request is not a durable brief.
- For every supplied executable package, require `verification.md` beside
  `brief.md` and require its `Source brief:` declaration to resolve to that
  brief. Read it as derived guidance under the brief and cited authority.
  Missing or mismatched verification cannot produce ready readiness; route
  the defect to `task-verification-designer` after any needed package repair.
- Write compact durable readiness to the canonical `preflight.md` beside
  `brief.md`, including for routine packages. Use the guided sections of
  `references/execution-packet-template.md`; no separate context artifact,
  digest ledger, tracker, machine schema or instrumentation is required merely
  because a package exists. A request for inline output cannot bypass this rule.
  An unpackaged conversational request may receive inline readiness.
- Inspect the minimum current state needed to protect ownership and identify
  concrete readiness uncertainty, then classify the standalone preflight's
  value before doing broader readiness work. This classification guides
  effort; it is not a readiness status or a required machine-schema field.
- Standalone preflight is required for an executable package. For an unpackaged
  direct request, `bounded-task-implementer` may perform the compact self-check.
- Before preflighting a task brief, reject it as non-executable when it declares
  `Task kind: composite` and `Status: decomposed`. Read `docs/tasks/index.json`
  when present to identify its dependency-ready executable leaf, then reroute
  the caller to that leaf (or report that no dependency-ready leaf is
  available). Never preflight a decomposed parent.

Classify `standalone_preflight_value` as:

- `material` when dirty or multi-writer ownership, a required environment,
  permission, dependency, helper, fixture, or real-boundary capability, an
  ambiguous or expensive command/oracle, a durable cross-session handoff, or a
  high-assurance/unattended entry condition is genuinely uncertain or costly
  to discover late; or
- `marginal` when authority, scope, ownership, paths, dependencies, command,
  and oracle are routine and `bounded-task-implementer` can check them cheaply.

If a brief recommends standalone guided preflight for a named uncertainty,
compare that reason with current repository state. Reclassify when later
focused discovery resolves or reveals a material fact, and report the final
classification with the exact uncertainty resolved. Do not preserve or reject
the route merely because the brief named it.

### High assurance

- Require the packaged `ready_for_preflight` `brief.md`, run policy, dependency
  source, and an authorized durable packet path. Refuse a direct legacy brief
  and route it to `task-brief-designer` for package normalization. The packet
  path must be `preflight.md` beside the package's `brief.md`.
- Require the executable package's `verification.md` as a derived packet input:
  require its `Source brief:` declaration to resolve to the package's
  `brief.md`, preserve its scenario/AC coverage, and record its exact path and
  digest and revision. Missing or mismatched verification prevents ready.
- Capture exact baseline and content identities so another agent or process can
  safely rely on the packet later.
- Produce the complete packet from
  `references/execution-packet-template.md`.

## Guided workflow

1. Read applicable instructions, the task/request, and any applicable
   task-local verification design (required for a supplied package). Confirm
   the expected behavior is
   sufficiently clear; route a material product or architecture gap back to the
   owner rather than guessing.
2. Inspect `git status --short`, the intended change area, and any declared
   multi-writer ownership signal. Identify pre-existing user changes and stop
   on ownership overlap that cannot be safely separated.
3. Make a provisional standalone-value classification from the named route,
   current ownership facts, and the criteria above before doing baseline or
   freshness work. Reclassify as focused discovery resolves dependencies,
   commands, or oracles. In the result, record the final classification and
   exact uncertainty resolved when value is material, or why the final facts
   are routine when it is marginal.
4. Confirm dependencies and entry conditions that matter now. Do not require a
   tracker or digest merely because high-assurance mode would record one.
5. Resolve the relevant implementation paths, closest tests, public entry
   point, and lowest-cost targeted command. Focused discovery is allowed; do
   not perform generic repository archaeology.
6. For every material AC and scenario, confirm the authority relationship,
   coverage, setup, decisive boundary, command feasibility, dependencies,
   permissions and ownership. An omitted AC, unsupported scenario or weak oracle
   prevents ready even when other evidence is green. Keep each gap visible with
   evidence, owner and smallest correction route; never invent requirements or
   drop a required row. Verification defects route to `task-verification-designer`;
   unclear requirements route to task design or the authority owner.
   An absent task-owned future test is allowed when its fixture, tool and boundary
   are feasible within scope: name the planned proof and command, and record that
   it has not run. An unavailable indispensable capability blocks with concrete
   evidence and its prerequisite owner; it is not new implementation scope.
   Readiness does not claim that future behavior passed. Require the real
   boundary only where unit/module evidence
   cannot prove wiring, persistence, process, database, filesystem,
   concurrency, recovery, authorization, or another material behavior.
7. Run an authorized cheap local baseline only when it distinguishes a broken
   environment from the intended fail-first state or freshness is an entry
   criterion. Do not run a broad or aggregate baseline to make the result look
   complete.
   Ask before slow, flaky, privileged, destructive, live, or networked checks
   unless already authorized.
8. Record compact decision context and current applicability as described below.
   Write `ready` or `blocked` to the package's canonical `preflight.md`; for a
   noncanonical requested path, return blocked content without writing there.
   Direct requests may return inline. Include the exact targeted command and
   oracle, scope/ownership and capability results, warnings/stops and next action.
   Blocked output includes evidence, owner and smallest next action.

## Decision context and current applicability

Bind packaged readiness to the source brief and its revision (use a supplied
revision/reference; exact digests are only required in high-assurance mode),
allowed scope and verification revision. Link relevant task/project direction,
architecture and current/planned contracts. Carry compact decision context:
intended use and operating envelope, important failure consequences, relevant
business priorities, required consumers, credible same-kind maintenance/planned changes,
mitigations and decision-relevant unknowns. Use supplied facts; do not invent
business policy or require a complete context dossier.

Reassess relevant known issues against this task's exposure and obligations.
Unrelated issues do not trigger broad rediscovery. A missing known-issues file
means no recorded deferrals, not a preparation blocker. Record ordinary unknowns
as reasonable assumptions and continue without routine questions or automatic
blockers. Required proof, capability, permissions and ownership remain binding.
For credible serious consequences of delay or materially costly later repair,
resolve uncertainty within current authority first. Only a still unresolved
decision-critical fact calls for one focused question explaining the consequence
and needed fact; preserve the unresolved condition and its decision owner.
Do not mark readiness ready while that decision-critical condition is unresolved.

Under unchanged authority, a reasoned verification revision must
retain existing scenario IDs and state why coverage changed. Reject
affected obsolete readiness even when IDs are unchanged. Perform focused
preflight on added/revised obligations and affected
feasibility, reuse unchanged relevant facts, and record a current decision bound
to the new revision. Do not restart task design or full discovery for a justified
coverage revision. Preserve non-artifact repository files.

Material authority, prerequisite/dependency, ownership, permission or capability
changes require reconsideration and a current readiness decision on affected facts.
Expected implementation or report effects alone do not force full rediscovery.
Changed requirements return to `task-brief-designer` or the decision owner;
derived scenarios cannot settle them. These guided applicability rules do not
relax exact high-assurance freshness checks.

For a marginal direct invocation, still perform steps 1-8 sufficiently to give
a truthful `ready` or `blocked` result. Limit the check to applicable
instructions, status/ownership, bounded paths, and the targeted command with
its oracle. Do not create a broad baseline, digest ledger, repeated task
summary, or high-assurance artifact. Recommend implementer self-preflight for
the next materially similar task.

## Guided blockers and warnings

Block when:

- authority or an acceptance oracle is materially ambiguous;
- a required dependency or capability is absent;
- intended paths overlap user-owned work without permission to merge;
- the targeted command cannot execute and implementation depends on it;
- required work exceeds the allowed scope or permission envelope; or
- safe execution needs an unauthorized destructive, privileged, live, or
  networked action.

Do not require a content-digest ledger, worker-result schema or exact broader
gate for guided work. Direct requests need no durable artifact. Packages require
verification and canonical readiness; missing verification is a coverage gap,
not optional paperwork. Record relevant uncertainty and let implementation resolve
ordinary in-scope details, including feasible future tests.

## High-assurance workflow

1. Read the complete brief, required packaged task-local verification design,
   cited authority, applicable instructions, dependency source, and run policy.
   Confirm status `ready_for_preflight`. Treat verification design as derived
   guidance under the brief rather than independent requirements authority.
   Apply the same complete coverage, feasibility and context checks as guided
   packages; feasible absent future tests never waive required capabilities or
   the exact freshness checks below.
2. Resolve the durable packet path first. It must be the executable task
   package's `preflight.md`. A different path is a contract error: return
   blocked content without writing it and route package normalization or a
   corrected invocation to the owner.
3. Capture before checks:
   - brief bytes and lowercase SHA-256;
   - applicable verification-design path and lowercase SHA-256, or explicit
     `none`;
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
   authorization, whether it ran, and truthful result. When verification design
   applies, map its scenario IDs to those commands/oracles and leave any blocked
   or not-yet-executable scenario visible rather than silently dropping it.
6. Run only authorized cheap local baselines, narrowest first. Record incidental
   artifacts and do not claim a clean baseline until their disposition is
   explicit.
7. Recapture all freshness values before and after packet creation. Record both
   exact status snapshots and attribute the new/modified `preflight.md` entry.
   Any change beyond that one packet artifact, or any changed non-packet
   identity, blocks readiness. The packet need not be ignored or status-neutral.
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

For guided mode, use a compact canonical package packet or inline direct-request
result containing:

- status and `standalone_preflight_value: marginal | material`, including the
  routine basis or exact uncertainty resolved;
- only implementation deltas: confirmed scope and user-work ownership,
  targeted command and observable oracle, relevant helper/capability result,
  material warnings or blockers, and implementation stops;
- source brief/scope/verification revision, per-AC/scenario authority and
  feasibility conclusions, referenced decision context and current applicability;
- whether the standalone stage added enough value to recommend it for the next
  materially similar task; and
- the exact next action.

When another session will consume the guided result, include one copyable
`Implementer handoff` block containing those deltas and the exact next action.
Do not repeat the task outcome or acceptance prose unless needed to
disambiguate the oracle.

For high-assurance mode, use the full packet template and durable path. A
blocked packet is evidence, not authorization to implement.

## Boundaries and routing

- Route contract or authority defects to `task-brief-designer` or the user.
- Keep current-state failures—dirty overlap, dependency failure, missing path
  or helper, invalid command, environment, or permissions—here.
- Route wider scope or shared infrastructure through brief design.
- Write only canonical readiness for packages or an explicitly requested direct
  readiness artifact. Do not edit other source/tests/docs/config/dependencies,
  implement, approve, update
  trackers, launch subagents, or modify orchestration state.

## Definition of done

- The readiness result is proportionate to the selected profile.
- Guided standalone value is classified before ceremony and explained from
  current facts.
- Scope, user-work ownership, dependencies, command, oracle, permissions, and
  meaningful gaps are explicit.
- Guided output is delta-focused, and marginal direct requests still receive a
  truthful readiness check without freshness paperwork or broad baselines.
- Every supplied executable package has source-matched justified verification
  and compact canonical readiness with complete feasibility and decision context.
- High-assurance mode remains independently reproducible and freshness-safe.
