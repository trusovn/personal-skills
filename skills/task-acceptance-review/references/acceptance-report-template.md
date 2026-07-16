# Task Acceptance Report: `<TASK-ID>` — `<brief title>`

| Field | Value |
|---|---|
| Task ID | `<stable ID>` |
| Artifact status / verdict | `ACCEPT \| CHANGES_REQUESTED \| INCONCLUSIVE` |
| Producing stage | `task-acceptance-review` |
| Created at | `<ISO-8601 timestamp with timezone>` |
| Repository root | `<absolute path>` |
| Durable report path | `<absolute or repository-relative runtime path>` |
| Task brief | `<exact path and preflight-recorded SHA-256>` |
| Preflight packet | `<exact path>` |
| Implementer result | `<exact path and status>` |
| Run policy | `<identifier and path>` |

## 1. Findings, ordered P0 through P3

Use `No findings.` when no concrete defect exists. Do not manufacture findings
to justify the review.

### [P1] `<imperative, consequence-focused title>`

| Field | Evidence |
|---|---|
| Current location | `<repository-relative path:line>` |
| Triggering state/input | `<specific reproducible precondition and action>` |
| Consequence | `<user, data, system, contract, or operational impact>` |
| Evidence | `<trace, independent probe, command result, or code fact>` |
| Affected AC | `<AC-ID>` |
| Smallest corrective direction | `<bounded direction only; do not write the patch>` |

## 2. AC evidence matrix

| AC | Required invariant and oracle | Function/state/module evidence | Real public-entry and decisive-boundary evidence | Negative / unchanged-state evidence | Repeated / recovery evidence | Result and gap |
|---|---|---|---|---|---|---|
| `<AC-ID>` | `<observable contract and independent oracle>` | `<evidence or N/A with reason>` | `<entry point, boundary, observed result>` | `<evidence>` | `<first occurrence + legitimate state change + next occurrence, or N/A with task-specific reason>` | `pass \| fail \| unverified — evidence/owner` |

Passing submitted tests or worker claims are not independent evidence until
corroborated. Pure-function evidence is insufficient when the AC names a real
workflow.

## 3. Independent probes and command results

| ID | Exact command or probe | Working directory / environment | Purpose and ACs | Result and observed signal | Side effects / disposition | Independence or gap |
|---|---|---|---|---|---|---|
| `REV-01` | `<exact command or reproducible manual probe>` | `<absolute cwd; disposable state and required environment>` | `<claim corroborated>` | `<exit status and concise observation>` | `<none, or exact authorized runtime paths and cleanup>` | `<independent evidence, limitation, or reason not run>` |

Record required-but-unrun checks with their exact authorization, capability, or
environment blocker. Never copy the worker's `passed` result as the reviewer's
own result.

## 4. Scope and baseline comparison

| Item | Preflight baseline | Current state | Classification and evidence |
|---|---|---|---|
| `HEAD` | `<SHA or unborn>` | `<SHA or unborn>` | `<expected task state \| unexplained change>` |
| Exact `git status --short` | `<verbatim baseline or clean>` | `<verbatim current snapshot or clean>` | `<task-owned, pre-existing user, runtime, or unexplained>` |
| Dirty path index/worktree digests/states | `<path, index sha256/state, worktree sha256/state>` | `<current index and worktree sha256/state>` | `<ownership, separability, and exact mismatch>` |
| Task-owned paths | `<packet allowed paths>` | `<scoped diff and worker files_changed>` | `<in scope \| unauthorized/missing>` |
| Runtime artifacts | `<packet-declared paths>` | `<observed paths>` | `<authorized/disposition>` |
| Authority and policy | `<brief, instructions, dependency, policy digests>` | `<current comparison>` | `<unchanged \| exact invalidation>` |

State the exact diff/range/files reviewed. Separate task changes from
pre-existing user work; do not claim ownership of the latter.

## 5. Open questions

- `<Only a question whose answer could change the verdict, severity, scope, or route; include owner and why evidence cannot resolve it.>`

Use `None.` when no such question remains.

## 6. Residual risks and unverified boundaries

| Risk or boundary | Evidence / reason unverified | Blocking? | Owner / follow-up |
|---|---|---|---|
| `<specific risk, skipped stronger check, or none>` | `<observed limit>` | `yes \| no` | `<owner and bounded action>` |

Do not disguise a failed requirement as residual risk. Any gap that prevents a
required AC or gate from being proved is blocking and requires `INCONCLUSIVE`
unless an evidenced in-scope defect already requires `CHANGES_REQUESTED`.

## 7. Verdict and next route

| Field | Value |
|---|---|
| Verdict | `ACCEPT \| CHANGES_REQUESTED \| INCONCLUSIVE` |
| Basis | `<findings, AC evidence, scope, commands, and questions that determine it>` |
| Next owner | `<task-orchestrator \| same bounded-task-implementer thread \| task-preflight \| task-brief-designer \| user>` |
| Exact next action | `<one smallest action; do not perform it during review>` |

- `ACCEPT` routes only to `task-orchestrator` for any authorized advancement.
- `CHANGES_REQUESTED` routes to the same implementer thread and requires a new
  acceptance review after correction.
- `INCONCLUSIVE` routes to the earlier stage or user who owns the stated
  authority, freshness, capability, environment, or policy blocker.
