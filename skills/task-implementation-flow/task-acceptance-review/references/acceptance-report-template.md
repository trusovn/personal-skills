# Task Acceptance Report: `<TASK-ID>` — `<brief title>`

| Field | Value |
|---|---|
| Verdict | `ACCEPT | CHANGES_REQUESTED | INCONCLUSIVE` |
| Producing stage | `task-acceptance-review` |
| Review iteration | `<first review or correction number>` |
| Created at | `<ISO-8601 timestamp with timezone>` |
| Repository root | `<absolute path>` |
| Durable report path | `<authorized runtime path>` |
| Task brief | `<exact path and preflight-recorded SHA-256>` |
| Preflight packet | `<exact path>` |
| Implementer result | `<exact corrected/current path and status>` |
| Run policy | `<identifier and path>` |

This report applies only to the reviewed bytes and artifacts identified below.
Any correction requires a new report and verdict.

## 1. Findings, ordered P0 through P3

Use `No findings.` when no concrete defect exists.

### [P1] `<consequence-focused title>`

| Field | Evidence |
|---|---|
| Current location | `<repository-relative path:line>` |
| Triggering state/input | `<specific reproducible precondition and action>` |
| Consequence | `<user, data, system, contract, or operational impact>` |
| Evidence | `<trace, independent probe, command result, or code fact>` |
| Affected AC | `<AC-ID>` |
| Smallest corrective direction | `<bounded direction; no patch>` |

## 2. AC evidence matrix

| AC | Required invariant / oracle | Module evidence | Real entry point / decisive boundary | Negative / unchanged evidence | Repeated / recovery evidence | Result / gap |
|---|---|---|---|---|---|---|
| `<AC-ID>` | `<observable contract>` | `<evidence or N/A>` | `<entry point, boundary, observed result>` | `<evidence>` | `<first state change + next occurrence, or N/A with reason>` | `pass | fail | unverified — owner/evidence` |

Passing worker tests are submitted claims until independently corroborated.

## 3. Adversarial state and evidence checks

Include only rows relevant to this task.

| Invariant / claim | Cases exercised | Result and evidence |
|---|---|---|
| Selected versus non-selected state coherence | `<cross-product cases>` | `<result>` |
| Exact cardinality | `<zero, one, and two owners/items>` | `<result>` |
| Latest/current ordering | `<older, latest, missing, duplicated>` | `<result>` |
| Exact ready/eligible set | `<missing, exact, extra>` | `<result>` |
| Parent/child terminal coherence | `<running child under stopped/complete parent>` | `<result>` |
| Persisted type strictness | `<boolean/int, string/collection, other relevant confusions>` | `<result>` |
| Coherent tampering | `<related bytes and internal digests rewritten together>` | `<consistency-only, independently anchored, or defect>` |

## 4. Independent probes and command results

| ID | Exact command / probe | Working directory / environment | Purpose / ACs | Result and observed signal | Side effects / disposition | Independence / gap |
|---|---|---|---|---|---|---|
| `REV-01` | `<exact command or reproducible probe>` | `<cwd and disposable state>` | `<claim>` | `<exit and observation>` | `<none or paths/cleanup>` | `<independent evidence or limitation>` |

Record required-but-unrun checks with the exact capability, permission, or
environment blocker. Never copy a worker's `passed` label as reviewer evidence.

## 5. Scope and baseline comparison

| Item | Preflight baseline | Current reviewed state | Classification / evidence |
|---|---|---|---|
| `HEAD` | `<SHA or unborn>` | `<SHA or unborn>` | `<expected or unexplained>` |
| Exact `git status --short` | `<verbatim baseline or clean>` | `<verbatim current>` | `<task, user, runtime, unexplained>` |
| Dirty path index/worktree identities | `<separate states/digests>` | `<separate states/digests>` | `<ownership/separability>` |
| Task-owned paths | `<allowed paths>` | `<scoped diff and worker files_changed>` | `<in scope or mismatch>` |
| Runtime artifacts | `<declared paths>` | `<observed paths>` | `<authorized/disposition>` |
| Authority / policy / dependencies | `<recorded identities>` | `<current comparison>` | `<unchanged or invalidation>` |

State the exact diff/range/files reviewed. Do not absorb pre-existing user work.

## 6. Questions and residual risks

| Question / risk | Evidence or reason unverified | Blocking? | Owner / follow-up |
|---|---|---|---|
| `<none or specific item>` | `<observed limit>` | `yes | no` | `<owner/action>` |

A failed required behavior is a finding, not residual risk. A missing required
oracle is blocking and normally yields `INCONCLUSIVE`.

## 7. Verdict and next route

| Field | Value |
|---|---|
| Verdict | `ACCEPT | CHANGES_REQUESTED | INCONCLUSIVE` |
| Basis | `<findings, evidence, scope, commands, questions>` |
| Next owner | `<orchestrator, same implementer thread, preflight, brief designer, or user>` |
| Exact next action | `<one smallest action>` |

- `ACCEPT` may route to authorized advancement.
- `CHANGES_REQUESTED` routes to correction followed by a fresh review.
- `INCONCLUSIVE` routes to the owner of the authority, freshness, capability,
  environment, permission, or scope blocker.
