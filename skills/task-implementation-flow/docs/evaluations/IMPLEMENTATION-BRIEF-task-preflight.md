# Implementation brief: make `task-preflight` conditional and delta-focused

Status: `ready`

```yaml
agent_tier: standard
reasoning: medium
review: milestone
budget: 16 tool calls / 60 minutes / 45k context
```

This block is intended launch guidance under resolved decision `G-01`; it does
not claim an observed runtime configuration.

This brief is self-contained implementation authority for the
`task-preflight` changes derived from the 2026-07-21 flow evaluation. An
implementer may inspect the repository paths named here, but should not need to
read the source evaluation or this conversation.

## Outcome

Make standalone guided preflight spend effort only when it resolves meaningful
readiness uncertainty, return a compact delta handoff another session can use,
and leave routine readiness checking to the implementer's existing
self-preflight by default. Preserve full high-assurance preflight.

## Why this change is justified

- Preflight was accurate in the evaluated tasks: it checked ownership,
  dependencies, commands, baselines, sandbox availability, and the first
  oracle, and it caused no observed ownership accident or command failure.
- It found no blocker in S3-06, S3-07, or S3-08 and provided little observable
  incremental value for semantic correctness.
- It accounted for only 11.3% of S3-07's and 6.5% of S3-08's uncached-input plus
  output proxy. Removing it alone will not solve the flow's token problem.
- Handoff transfer was poor: two implementers did not receive the substantive
  preflight result, and passing the complete S3-08 result did not reduce review
  rounds.
- The correct metric for this skill is prevented unsafe starts and resolved
  current-state facts, not later acceptance defect count.

The important correction is not to make preflight refuse a direct user
request. A user-invoked routine preflight should still return a truthful compact
readiness result; it should label its incremental value as marginal and avoid
ceremony or broad baselines.

## Authority and scope

| Item | Contract |
|---|---|
| Primary authority | This brief, derived from `skills/task-implementation-flow/docs/evaluations/EVALUATION-2026-07-21.md` |
| Repository root | `/Users/mtrusov/work/skill-sources/personal-skills` |
| Canonical skill | `skills/task-implementation-flow/task-preflight/` |
| Active mirror | `.agents/skills/task-preflight/`, read-only during this task and updated only by post-acceptance distribution |
| Allowed canonical changes | `SKILL.md`, `references/execution-packet-template.md` only if needed for consistent terminology, `evals/evals.json`, and `evals/files/setup_fixture.py` |
| Post-acceptance distribution | Corresponding active-mirror files, owned by the separate distribution step after the canonical change receives independent `ACCEPT` |
| Read-only context | `skills/task-implementation-flow/README.md`, `bounded-task-implementer/SKILL.md`, and existing preflight evals |
| Out of scope | Active-mirror writes, removing the skill, weakening high-assurance freshness, production task-orchestrator behavior, live comparative benchmarking, and cross-skill README integration |
| Dependencies | None; `G-03` is resolved and the shared README default remains a later single-owner integration |

The canonical and mirror directories were byte-identical when this brief was
written. Recheck before editing.

## Needs to be solved before implementation

No product or architecture decision blocks the skill-local work.

Leave the active mirror unchanged. The post-acceptance distribution owner must
resolve the repository-approved canonical-to-mirror sync/install process; none
is documented in the relevant README files. This does not block canonical
implementation and review. Also preserve the pre-existing user change to
`skills/task-implementation-flow/README.md`; that shared file is not part of
this task.

Resolved `G-03` also allows `task-brief-designer` to recommend standalone
guided preflight for a named material uncertainty. Treat that recommendation as
design guidance, then classify the current facts truthfully; do not perform
ceremony solely because an old brief once recommended the route.

## Required work

1. Add an upfront standalone-value classification for guided mode.

   Classify value as `material` when at least one of these is genuinely
   uncertain or costly to discover late:

   - dirty or multi-writer ownership and separability;
   - a required environment, permission, dependency, helper, fixture, or
     real-boundary capability;
   - an exact command or oracle that is difficult, ambiguous, or expensive to
     resolve;
   - a durable freshness handoff to another process/session;
   - a high-assurance or unattended entry condition.

   Classify it as `marginal` when authority, scope, ownership, paths,
   dependencies, command, and oracle are routine and can be checked cheaply by
   `bounded-task-implementer`.

   When invoked from a task brief with a human-readable readiness route, compare
   the route and its reason with current state. Report any material change in
   the uncertainty instead of blindly preserving or rejecting the
   recommendation.

2. Define behavior for a marginal direct invocation.
   - Do not reject or ignore the user's preflight request.
   - Perform the minimum guided check needed for a truthful result: applicable
     instructions, status/ownership, bounded paths, and the targeted command
     with its oracle.
   - Avoid a broad baseline, digest ledger, repeated task summary, or
     high-assurance artifact.
   - Return normal status `ready` or `blocked`; do not add a third readiness
     status.
   - Report `standalone_preflight_value: marginal`, explain why, and recommend
     implementer self-preflight for the next similar task.

3. Preserve the full guided workflow when value is material and the complete
   high-assurance workflow when selected by existing rules. Report
   `standalone_preflight_value: material` with the exact uncertainty resolved.
   The value label is human-readable guidance, not a new required machine
   schema unless a separate schema owner later authorizes that change.

4. Make the guided output delta-focused.
   - Report only facts newly resolved for implementation: ownership exception
     or clean scope, exact targeted command and oracle, helper/capability result,
     material warning/blocker, and implementation stops.
   - When another session will consume the result, include one copyable
     `Implementer handoff` block containing those deltas and the exact next
     action. Do not repeat the task's outcome and AC prose unless necessary to
     disambiguate an oracle.
   - State whether standalone preflight added enough value to recommend it for
     the next materially similar task.

5. Tighten baseline ownership.
   - Run a cheap baseline only when it distinguishes environment readiness from
     the intended fail-first state or when authority makes freshness an entry
     criterion.
   - Do not run a broad or aggregate baseline merely to make the result look
     complete.
   - Keep all existing approval rules for slow, flaky, privileged,
     destructive, live, and networked checks.

6. Update `references/execution-packet-template.md` only if needed to keep the
   guided terminology consistent. Do not add the marginal/material label to the
   high-assurance durable schema unless a consuming schema requires it. A short
   optional row in the guided summary is sufficient.

7. Add a retrospective eval instead of overloading the existing
   `queue-guided` oracle-gap case.
   - Add an `api-routine` fixture at `/work/api-routine` with a clean Git tree,
     obvious allowed paths `src/auth/session.py` and
     `tests/auth/test_session.py`, exact targeted command
     `python -m unittest tests.auth.test_session.SessionTest.test_unexpired_session_is_valid`,
     a direct observable validity oracle, complete dependencies, and no
     real-boundary uncertainty.
   - The fixture must contain a passing targeted test that genuinely exercises
     the stated current behavior; a placeholder test is not enough.
   - Add an eval requiring guided inline preflight with no durable packet.
   - Expect `ready`, `standalone_preflight_value: marginal`, a compact
     implementer handoff, no broad test execution, and a recommendation that
     the next similar task use implementer self-preflight.
   - Preserve the existing `queue-guided` eval because it protects the distinct
     case where preflight discovers an oracle gap.
   - Preserve every other pre-existing eval unless this task explicitly
     revises its expectation. Treat the complete pre-existing-plus-new eval
     file as the owning regression set, including the existing high-assurance
     cases. If runner availability or paid/live authorization prevents
     execution, list the exact skipped eval IDs and do not claim the affected
     unchanged behavior.

8. Keep the active mirror unchanged during implementation and canonical
   acceptance. After an independent `ACCEPT`, hand the accepted canonical paths
   to the separate distribution owner, who resolves the approved sync/install
   process and proves byte identity.

## Acceptance criteria

- **AC-01 — value is classified before ceremony.** A routine clean guided task
  is labeled marginal without digest/freshness paperwork, while a task with a
  real readiness uncertainty continues through material preflight. A route
  recommended by the brief is re-evaluated against current facts.
- **AC-02 — direct requests are still fulfilled.** Marginal value does not cause
  the skill to skip requested readiness checks or return a non-contract status.
- **AC-03 — guided output is consumable.** A separate implementer can copy the
  handoff and obtain exact ownership, command/oracle, capability, stops, and
  next action without rereading a long preflight narrative.
- **AC-04 — baseline work is justified.** The routine fixture does not trigger a
  broad baseline; a baseline runs only for a named readiness distinction or
  entry criterion.
- **AC-05 — high assurance is unchanged.** Durable packet identity, freshness,
  separate index/worktree evidence, and blocker behavior retain their current
  contract.
- **AC-06 — eval evidence is behavioral.** The routine fixture supplies a real
  targeted behavior and oracle; the eval rejects outputs that merely assert
  obvious paths without resolving the command or ownership.
- **AC-07 — distribution boundary is preserved.** This task changes only the
  canonical skill and leaves the active mirror untouched; the accepted
  canonical paths and post-acceptance distribution route are explicit in the
  handoff.

## Verification

Run one command at a time, narrowest first. No canonical live skill-eval command
is documented; resolve it during self-preflight and ask before a paid/live
model run.

| Evidence | Scenario and oracle | Command |
|---|---|---|
| JSON structure | Updated eval definitions parse | `python3 -m json.tool skills/task-implementation-flow/task-preflight/evals/evals.json` |
| Fixture syntax | The setup script parses as Python without filesystem writes | `python3 -c "import ast, pathlib; ast.parse(pathlib.Path('skills/task-implementation-flow/task-preflight/evals/files/setup_fixture.py').read_text())"` |
| Routine fixture behavior | `api-routine` creates a clean repo with exact paths, executable targeted test, and direct oracle | From the canonical skill directory: `python3 evals/files/setup_fixture.py api-routine`, then run the fixture's exact targeted command |
| Existing fixture regression | Existing `queue-guided` still stages the repeated-public-flow oracle gap | From the canonical skill directory: `python3 evals/files/setup_fixture.py queue-guided` |
| Owning skill eval set | Every pre-existing and new eval is run, including high-assurance cases; the revised skill returns a compact marginal result for `api-routine` and retains material and high-assurance behavior. Any skipped eval IDs and affected unverified ACs are reported explicitly | Full owning eval-runner command discovered during self-preflight; approval required for paid/live execution |
| Mirror preservation | No task-created change appears under the active mirror relative to the self-preflight baseline | `git status --short -- .agents/skills/task-preflight` |

JSON and fixture syntax parsing do not prove skill behavior. A behavioral success claim
requires staging the fixture and running the focused skill eval. The global
medium-versus-medium cost comparison is outside this task.

## Stops and handoff

- Preserve high-assurance behavior; do not use the marginal-value change to
  weaken an explicitly durable or orchestrated preflight.
- Do not invent a new readiness status or machine schema field.
- Do not treat a task brief's readiness route as immutable current-state proof.
- Do not edit the shared README or other skills in this bounded task.
- Stop on user-work overlap. Do not edit the active mirror; unresolved
  distribution does not block canonical implementation or acceptance.
- When complete, return `READY_FOR_REVIEW`; a fresh reviewer should confirm both
  the marginal routine case and unchanged high-assurance boundaries.

Next action: guided canonical implementation, fresh acceptance review, then
post-acceptance distribution of accepted bytes.
