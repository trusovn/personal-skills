# Task Review Discovery Report: `<TASK-ID>` — `<brief title>`

| Field | Value |
|---|---|
| Producing stage | `task-review-discovery` |
| Coverage completeness | `complete \| partial — <concrete reasons>` |
| Discovery iteration | `<first discovery pass or correction number>` |
| Created at | `<ISO-8601 timestamp with timezone>` |
| Repository root | `<absolute path>` |
| Durable report path | `<task-package>/reviews/discovery-NN.md` |
| Task brief | `<exact path>` |
| Verification design / task context | `<exact paths when present, or conversational context>` |
| Current submission | `<implementer result or summary and status>` |

This report publishes evidence only. It contains no acceptance verdict, no
approved deferral, and no advancement. The separate acceptance decision call
consumes it. It applies only to the reviewed bytes and artifacts identified
below; any correction requires a new discovery report. This report does not
review or authenticate itself.

## 1. Discovery provenance

| Question | Evidence |
|---|---|
| Did this session author any reviewed production bytes? | `no — independent \| yes — SELF_CHECK_ONLY` plus `<session/diff evidence>` |
| Independent evidence authority | `yes \| no — fresh discovery call required` |
| Current byte identity | `<HEAD plus scoped diff identity when available>` |

Independence follows session authorship, not the currently loaded skill. When
the answer is `yes`, label the output `SELF_CHECK_ONLY`, mark its rows as not
independently corroborated, and route to a fresh discovery call. Do not
describe missing independence as an environment, permission, or freshness
blocker.

## 2. Findings, ordered by suggested severity P0 through P3

Use `No findings.` when no concrete defect exists. Suggested severity informs
the decision call; it is not a verdict.

### F-01 [suggested P1] `<consequence-focused title>`

| Field | Evidence |
|---|---|
| Finding ID | `F-01` |
| Suggested severity | `P0 \| P1 \| P2 \| P3` |
| Current location | `<repository-relative path:line>` |
| Triggering state/input | `<specific reproducible precondition and action>` |
| Consequence | `<user, data, system, contract, or operational impact>` |
| Evidence | `<trace, independent probe, command result, or code fact>` |
| Affected AC | `<AC-ID>` |
| Broken invariant | `<task-authorized property that does not hold>` |
| Credible sibling surface | `<contract-implied cases sharing that invariant>` |
| Smallest corrective direction | `<invariant-level bounded direction; no patch or field-local special case>` |

Keep confirmed findings separate from unproved questions and from unchecked
coverage rows. Continue through independent safe rows after the first finding.

## 3. Completeness ledger

Use stable task-derived row IDs. Consume a supplied prior ledger without
renaming rows, but rerun enough evidence for the current bytes; a prior `pass`
guides discovery and is not current proof.

| Row ID | AC / invariant | Explicit material cases | Setup / oracle | Submitted evidence | Independent probe / current evidence | Result / reason |
|---|---|---|---|---|---|---|
| `<stable ID>` | `<observable contract>` | `<finite values/state transitions>` | `<starting state, invocation, and expected signal>` | `<worker claim or N/A>` | `<entry point, boundary, observed result or exact gap>` | `pass \| fail \| blocked \| unchecked — <reason>` |

Every material row named by the authority appears here. A material authority
row omitted from the submitted tests or verification scenarios cannot vanish
behind green tests. Every required/material row must have one of the four
results before discovery ends; a partial ledger is reported as explicitly
partial and never presents omitted rows as clean.

## 4. Adversarial state and evidence checks

Include only rows relevant to this task.

| Ledger row / invariant | Cases exercised | Result and evidence |
|---|---|---|
| Selected versus non-selected state coherence | `<cross-product cases>` | `<result>` |
| Exact cardinality | `<zero, one, and two owners/items>` | `<result>` |
| Latest/current ordering | `<older, latest, missing, duplicated>` | `<result>` |
| Exact ready/eligible set | `<missing, exact, extra>` | `<result>` |
| Parent/child terminal coherence | `<running child under stopped/complete parent>` | `<result>` |
| Persisted type strictness | `<boolean/int, string/collection, other relevant confusions>` | `<result>` |
| Coherent tampering | `<related bytes and internal digests rewritten together>` | `<consistency-only, independently anchored, or defect>` |

## 5. Independent probes and command results

| ID | Exact command / probe | Working directory / environment | Purpose / ACs | Result and observed signal | Side effects / cleanup | Independence / gap |
|---|---|---|---|---|---|---|
| `DISC-01` | `<exact command or reproducible probe>` | `<cwd and disposable state>` | `<claim>` | `<exit and observation>` | `<none or paths/cleanup>` | `<independent evidence or limitation>` |

Record required-but-unrun checks with the exact command or `not run`, the
capability, permission, or environment blocker, and the next evidence owner.
Never copy a worker's `passed` label as discovery evidence. Confirm bounded
cleanup after each process probe: no descendant, process group, or inherited
pipe survives.

## 6. Aggregate-gate decision

| Field | Value |
|---|---|
| Gate / exact command | `<command or N/A>` |
| Status | `passed \| failed \| not run \| blocked` |
| Owner and stage | `<initial discovery \| correction discovery \| fresh discovery after late omission>` |
| Reason | `<why justified, decisive targeted failure that suppressed it, or distinct authorized diagnostic purpose>` |
| Current evidence | `<current targeted rows, observed aggregate result, or concrete not-run state>` |

Initial discovery suppresses the aggregate gate after any decisive targeted
failure; it does not run the gate merely for completeness. A fresh correction
discovery pass corroborates current bytes, reruns reviewer regressions,
finishes unfinished rows, and owns one justified aggregate after clean targeted
evidence. If a material row is later found omitted from an earlier
reconciliation, that earlier gate is recorded as premature. Add no gate and add
no command. Record targeted recovery before any justified rerun; conditional
gate owners retain their applicable proof duties. Unavailable rows keep concrete
non-gate reasons and owners. The acceptance decision call consumes this record; it does not
re-own it.

## 7. Scope and baseline comparison

| Item | Recorded baseline | Current reviewed state | Classification / evidence |
|---|---|---|---|
| `HEAD` | `<SHA or unborn>` | `<SHA or unborn>` | `<expected or unexplained>` |
| Exact `git status --short` | `<recorded snapshot>` | `<exact reviewed state before this report>` | `<task, user, packet, unexplained>` |
| Dirty path index/worktree identities | `<separate states/digests>` | `<separate states/digests>` | `<ownership/separability; a changed index blob is detected independently from matching worktree bytes>` |
| Task-owned paths | `<allowed paths>` | `<scoped diff and worker files_changed>` | `<in scope or mismatch>` |
| Durable package artifacts | `<brief, verification, context paths>` | `<observed paths>` | `<canonical/current or mismatch>` |
| Authority / policy / dependencies | `<recorded identities>` | `<current comparison>` | `<unchanged or invalidation>` |

After completing the report, record the post-report `git status --short` and
confirm that the new `reviews/discovery-NN.md` entry is the only change from
the reviewed state. Do not absorb pre-existing user work; publish an unsafe or
unexplained scope as an explicit gap instead.

## 8. Questions, unchecked work, and residual risks

| Type / row ID | Evidence or reason unverified | Blocking? | Owner / follow-up |
|---|---|---|---|
| `question \| blocked \| unchecked \| residual risk` | `<observed limit>` | `yes \| no` | `<owner/action>` |

A failed required behavior is a finding, not residual risk. A missing required
oracle is a blocked row with a concrete owner, not a clean row.

## 9. Coverage completeness and next route

| Field | Value |
|---|---|
| Coverage completeness | `complete \| partial — <concrete reasons>` |
| Basis | `<rows, findings, probes, commands, questions>` |
| Next owner | `<separate acceptance decision call, or the owner of a concrete blocker>` |
| Exact next action | `<one smallest action>` |

- Complete clean evidence routes to the separate acceptance decision call with
  no invented finding.
- A blocked or unchecked required row keeps its concrete reason and next
  evidence owner; discovery records no verdict and no approved deferral.
- A scope or capability blocker routes to its owning stage (`task-preflight`,
  brief design, or the user) before any renewed discovery.

## 10. Discovery continuation

Copy this compact block intact into the next discovery or acceptance context:

```markdown
Discovery continuation:
- Iteration / current byte identity: <iteration; HEAD/scoped diff identity>
- Coverage rows: <every stable row ID = pass/fail/blocked/unchecked + reason>
- Finding IDs: <all IDs with suggested severities, or none>
- Finding/scenario continuity: <prior statuses, current producer-attributed evidence, incomplete reasons and separate correction/evidence/authority owners; influenced sibling surfaces>
- Preparation/context: <brief, verification revision, preflight and context references>
- Reviewer regressions: <paths and exact focused commands, or none>
- Aggregate gate: <status, exact command/owner, reason>
- Next: <one exact route>
```

The next consumer must also receive the task brief, current scoped diff, this
report, reviewer regressions, and all blocked or unchecked rows. Prior row
results are navigation context, not proof for corrected bytes.
