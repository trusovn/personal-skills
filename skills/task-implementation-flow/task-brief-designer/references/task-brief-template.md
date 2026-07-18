# Task Brief: `<TASK-ID>` — `<imperative title>`

## Identity and artifact status

| Field | Value |
|---|---|
| Task ID | `<stable ID>` |
| Artifact status | `ready_for_preflight \| blocked_design` |
| Producing stage | `task-brief-designer` |
| Created at | `<ISO-8601 timestamp with timezone>` |
| Repository root | `<absolute path>` |
| Primary authority | `<path>#<exact section>` |
| Dependencies | `<task IDs and known state, or none>` |

## Outcome

`<One testable sentence describing the approved result, not the implementation process.>`

## Authoritative inputs and knowledge ledger

| Kind | Path or statement | Relevance |
|---|---|---|
| Authoritative input | `<repository-relative or absolute path>#<section>` | `<what it decides>` |
| Confirmed fact | `<fact>` | `<source path or supplied evidence>` |
| Frozen decision | `<decision entailed by authority>` | `<source path or section>` |
| Assumption | `<assumption or UNKNOWN>` | `<how preflight confirms it>` |
| Unresolved item | `<item or none>` | `<owner and blocking consequence>` |

For `blocked_design`, identify the missing authority and smallest next action
here, then complete only the remaining sections that can be stated truthfully.

## Scope and boundaries

| Item | Contract |
|---|---|
| Allowed paths | `<exact path>` or `<candidate path — preflight must resolve>` |
| Read-only context | `<authority/precedent path>` |
| Prohibited work | `<adjacent or speculative work>` |
| Mutation limits | `<network, dependency, commit, destructive-action, or shared-tool limits>` |
| Pre-existing user work | `Preserve; ownership remains with the user. Known paths: <paths or UNKNOWN>` |

## Entry criteria and dependencies

| Criterion | Required evidence | Current claim |
|---|---|---|
| `<dependency or baseline condition>` | `<path, tracker state, helper, or check>` | `preflight must confirm` |

## Work and acceptance criteria

Required work:

1. `<Small approved implementation outcome.>`
2. `<Small approved implementation outcome.>`

- **AC-01:** `<Observable behavior or invariant.>`
- **AC-02:** `<Observable rejection, failure, or unchanged-state behavior.>`

## AC execution matrix

| AC | Production invariant | Positive evidence | Negative evidence | Real entry-point path | Repeated or recovery path | Real boundary crossed | Verification dependency |
|---|---|---|---|---|---|---|---|
| AC-01 | `<state/behavior that remains true>` | `<success scenario and oracle>` | `<failure/rejection/unchanged-state scenario>` | `<public command/API/workflow>` | `<first + legitimate state change + next occurrence, or N/A with reason>` | `<process/filesystem/database/network/clock/concurrency/etc.>` | `<existing candidate, missing capability, or uncertainty>` |

If the matrix becomes long enough to obscure independent outcomes, split the
brief at independently verifiable boundaries.

## Legacy-assumption sweep

| Entry point or area | Search term / trace | Risk being tested | Required follow-through |
|---|---|---|---|
| `<path or public entry point>` | `<literal, guard, identifier, path, or baseline assumption>` | `<old lifecycle assumption>` | `<what preflight locates and implementation traces>` |

`N/A — <task-specific reason>` when no lifecycle extension or changed workflow
can reach a legacy assumption.

## Risk-to-evidence map

| Risk | Impact / escalation trigger | Evidence level and boundary | Scenario and oracle | Residual gap |
|---|---|---|---|---|
| `<credible failure>` | `<consequence and when to stop>` | `<unit/module/integration/system plus real boundary>` | `<positive/negative/recovery proof>` | `<gap or none>` |

## Verification-capability inventory

| Needed capability | Disposition | Owner / path | Preflight confirmation |
|---|---|---|---|
| `<fixture/helper/runner/enforcement>` | `task-local fixture \| prerequisite implementation brief \| prerequisite evaluation brief \| believed existing` | `<task ID and path, or candidate path>` | `<exact interface/existence question>` |

## Verification command candidates

| Class | Candidate command | Working directory | Evidence | Preflight must resolve |
|---|---|---|---|---|
| Targeted | `<exact candidate or UNKNOWN>` | `<path or UNKNOWN>` | `<ACs proved>` | `<syntax/env/helper uncertainty>` |
| Broader | `<owning suite/gate candidate or N/A with reason>` | `<path or UNKNOWN>` | `<blast radius covered>` | `<remaining uncertainty>` |

These are design candidates, not claims that a command exists or passes.

## Effort, budget, and escalation

| Item | Proposal |
|---|---|
| Implementation | `mechanical \| standard \| strong` agent; `low \| medium \| high` reasoning — `<why>` |
| Review | `mechanical \| milestone \| immediate` — `<why>` |
| Budget checkpoint | `<tool-call/context/time checkpoint from run policy, or UNKNOWN>` |
| Two-strike rule | `After two materially different fixes leave the same targeted behavior failing, stop and report evidence, discarded hypotheses, owning contract, and next route.` |
| Escalation triggers | `<scope/authority/concurrency/recovery/migration/auth/irreversible/compatibility triggers>` |

## Stop conditions and routing

- Stop before edits when `<entry, dependency, authority, overlap, or capability condition>` is false.
- Route missing/ambiguous authority to `<owner or user>` and keep status
  `blocked_design`.
- Route stale state, missing believed-existing helpers, invalid commands, or
  dirty overlap to `task-preflight`.
- Route wider paths or shared infrastructure back to `task-brief-designer`,
  followed by a fresh preflight.

## Implementation handoff requirements

The implementer must receive a fresh `ready` preflight packet derived from this
brief. It may change only confirmed allowed paths, must establish the named
fail-first/high-risk evidence, run exact packet commands progressively, preserve
user work, stop under the stated rules, and return the required structured
worker result. It does not approve its own work.

## Review handoff requirements

Independent review must receive this brief, its exact preflight packet, the
structured worker result, and the scoped baseline-to-current diff. It must
corroborate every AC at the required real boundary, repeat lifecycle flows when
applicable, revisit legacy assumptions, verify scope and negative behavior, and
return the staged acceptance verdict without editing reviewed files.

## Handoff summary

`<Concise next action. For ready_for_preflight: run task-preflight on this exact path. For blocked_design: identify the decision owner and required authority artifact.>`
