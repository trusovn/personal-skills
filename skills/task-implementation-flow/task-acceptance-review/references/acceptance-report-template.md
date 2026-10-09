# Task Acceptance Report: `<TASK-ID>` — `<brief title>`

| Field | Value |
|---|---|
| Verdict | `ACCEPT | CHANGES_REQUESTED | INCONCLUSIVE | none — SELF_CHECK_ONLY` |
| Non-verdict provenance label | `N/A | SELF_CHECK_ONLY` |
| Producing stage | `task-acceptance-review` |
| Review iteration | `<first review or correction number>` |
| Created at | `<ISO-8601 timestamp with timezone>` |
| Repository root | `<absolute path>` |
| Durable report path | `<task-package>/reviews/acceptance-NN.md` |
| Task brief | `<exact path and preflight-recorded SHA-256>` |
| Preflight packet | `<exact path>` |
| Implementer result | `<exact corrected/current path and status>` |
| Discovery report | `<exact path and coverage completeness; or absence and routed gap>` |
| Run policy | `<identifier and path>` |

This report applies only to the reviewed bytes and artifacts identified below.
Any correction requires a new report and verdict.

## 1. Reviewer provenance

| Question | Evidence |
|---|---|
| Did this session author any reviewed production bytes? | `no — independent | yes — SELF_CHECK_ONLY` plus `<session/diff evidence>` |
| Independent verdict authority | `yes | no — fresh reviewer required` |
| Current byte identity | `<HEAD plus scoped diff identity when available>` |

Independence follows session authorship, not the currently loaded skill. When
the answer is `yes`, label the report `SELF_CHECK_ONLY`, set the summary and
detailed verdict fields to `none — SELF_CHECK_ONLY`, and route to a fresh
reviewer. Do not use `INCONCLUSIVE` to describe missing independence.

## 2. Findings, ordered P0 through P3

Use `No findings.` when no concrete defect exists. Preserve the discovery
report's stable finding IDs; do not rename, merge, or drop them.

### F-01 [P1] `<consequence-focused title>`

| Field | Evidence |
|---|---|
| Finding ID | `F-01` |
| Current location | `<repository-relative path:line>` |
| Triggering state/input | `<specific reproducible precondition and action>` |
| Consequence | `<user, data, system, contract, or operational impact>` |
| Evidence | `<admitted discovery trace, probe result, or code fact>` |
| Affected AC | `<AC-ID>` |
| Broken invariant | `<task-authorized property that does not hold>` |
| Credible sibling surface | `<contract-implied cases sharing that invariant>` |
| Smallest corrective direction | `<invariant-level bounded direction; no patch or field-local special case>` |
| Disposition | `<confirmed and routed to correction | retained as unresolved with reason and owner>` |

Keep confirmed findings separate from unproved questions and from unchecked
coverage rows. Every confirmed finding and unfinished row from the admitted
discovery report survives the decision with its current result and evidence,
or its incomplete reason and owner.

## 3. Admitted evidence ledger and reconciliation

Use the discovery report's stable task-derived row IDs. Consume a supplied
prior ledger without renaming rows, but reconcile every row against current
authority and reviewed bytes; a prior `pass` guides the decision and is not
current proof.

| Row ID | AC / invariant | Explicit material cases | Submitted evidence | Admitted discovery evidence | Reconciled result / reason |
|---|---|---|---|---|---|
| `<stable ID>` | `<observable contract>` | `<finite values/state transitions>` | `<worker claim or N/A>` | `<reported probe, boundary, observed result or exact gap>` | `pass | fail | blocked | unchecked — <reason>` |

Implementer summaries, report self-claims, and green tests are submitted claims
until admitted evidence reconciles them against current bytes. Every
required/material row must have one of the four results before the decision
ends. `CHANGES_REQUESTED` does not imply that unlisted areas passed.

## 4. Admitted adversarial evidence

Consumed from the discovery report; include only rows relevant to this task.

| Ledger row / invariant | Cases exercised | Admitted result and evidence |
|---|---|---|
| Selected versus non-selected state coherence | `<cross-product cases>` | `<result>` |
| Exact cardinality | `<zero, one, and two owners/items>` | `<result>` |
| Latest/current ordering | `<older, latest, missing, duplicated>` | `<result>` |
| Exact ready/eligible set | `<missing, exact, extra>` | `<result>` |
| Parent/child terminal coherence | `<running child under stopped/complete parent>` | `<result>` |
| Persisted type strictness | `<boolean/int, string/collection, other relevant confusions>` | `<result>` |
| Coherent tampering | `<related bytes and internal digests rewritten together>` | `<consistency-only, independently anchored, or defect>` |

## 5. Admitted discovery probes and command records

| ID | Exact command / probe (from discovery) | Working directory / environment | Purpose / ACs | Admitted result and observed signal | Admission status |
|---|---|---|---|---|---|
| `DISC-01` | `<exact command or reproducible probe>` | `<cwd and disposable state>` | `<claim>` | `<exit and observation>` | `current | stale | copied pre-correction | not run — <reason>` |

Record required-but-unrun checks with the exact missing evidence and its next
owner. Acceptance consumes these records; it does not routinely re-execute
public probes, broad searches, or suites. Never copy a worker's `passed` label
as decision evidence.

## 6. Admitted aggregate-gate record

| Field | Value |
|---|---|
| Gate / exact command | `<command or N/A>` |
| Status | `passed | failed | not run | blocked` |
| Owner and stage | `<initial discovery | correction discovery | fresh discovery after late omission>` |
| Reason | `<why justified, decisive targeted failure that suppressed it, or distinct authorized diagnostic purpose>` |
| Current evidence | `<what the gate observed at run time>` |
| Consumed by acceptance | `admitted without re-execution | re-execution refused — discovery owns it` |

Acceptance admits this record without executing the command again. Suppression
after a decisive targeted failure is retained; a copied pre-correction pass
cannot replace a clean corrected discovery record; a premature gate does not
clear an omitted row. Acceptance adds no gate and adds no command.

## 7. Scope and baseline comparison

| Item | Preflight baseline | Current reviewed state | Classification / evidence |
|---|---|---|---|
| `HEAD` | `<SHA or unborn>` | `<SHA or unborn>` | `<expected or unexplained>` |
| Exact `git status --short` | `<preflight post-write snapshot>` | `<exact reviewed state before this report>` | `<task, user, packet, unexplained>` |
| Dirty path index/worktree identities | `<separate states/digests>` | `<separate states/digests>` | `<ownership/separability>` |
| Task-owned paths | `<allowed paths>` | `<scoped diff and worker files_changed>` | `<in scope or mismatch>` |
| Durable package artifacts | `<brief, verification, and preflight paths>` | `<observed paths>` | `<canonical/current or mismatch>` |
| Authority / policy / dependencies | `<recorded identities>` | `<current comparison>` | `<unchanged or invalidation>` |

After completing the verdict, record the post-report `git status --short` and
confirm that the new `reviews/acceptance-NN.md` entry is the only change from
the reviewed state. The report does not review or authenticate itself.

State the exact diff/range/files reviewed. Do not absorb pre-existing user work.

## 8. Questions, unchecked work, and residual risks

| Type / row ID | Evidence or reason unverified | Blocking? | Owner / follow-up |
|---|---|---|---|
| `question | blocked | unchecked | residual risk` | `<observed limit>` | `yes | no` | `<owner/action>` |

A failed required behavior is a finding, not residual risk. A missing required
oracle is blocking and normally yields `INCONCLUSIVE`. Missing discovery or
missing decisive validator evidence routes to the discovery owner with the
exact gap.

## 9. Verdict and next route

| Field | Value |
|---|---|
| Verdict | `ACCEPT | CHANGES_REQUESTED | INCONCLUSIVE | none — SELF_CHECK_ONLY` |
| Basis | `<findings, admitted evidence, scope, consumed commands, questions>` |
| Next owner | `<orchestrator, same implementer thread, preflight, brief designer, discovery, or user>` |
| Exact next action | `<one smallest action>` |

- `ACCEPT` may route to authorized advancement.
- `CHANGES_REQUESTED` routes to correction followed by fresh discovery and a
  fresh decision.
- `INCONCLUSIVE` routes to the owner of the authority, freshness, capability,
  environment, permission, scope, or evidence blocker.
- `SELF_CHECK_ONLY` is not a verdict and always routes to a fresh reviewer.
- Only an independent `ACCEPT` may advance work.

## 10. Review continuation

Copy this compact block intact into the next decision context:

```markdown
Review continuation:
- Iteration / current byte identity: <iteration; HEAD/scoped diff identity>
- Coverage rows: <every stable row ID = pass/fail/blocked/unchecked + reason>
- Finding IDs: <all IDs or none>
- Reviewer regressions: <paths and exact focused commands, or none>
- Aggregate gate (consumed): <status, exact command/owner, reason>
- Next: <one exact route>
```

A fresh reviewer must also receive the task brief, current scoped diff,
preceding verdict/report, discovery report, reviewer regressions, and all
blocked/unchecked rows. Prior row results are navigation context, not proof for
corrected bytes.

## 11. Post-verdict reproducer (optional)

Include this section only when the fixed independent verdict is
`CHANGES_REQUESTED` and the current invocation explicitly authorized
`tests_only_reproducer` for the exact path or bounded area. Read
`tests-only-reproducer.md` before writing.

| Field | Evidence |
|---|---|
| Authorization source | `<current user/invocation text>` |
| Exact writable test path/area | `<allowlisted path>` |
| Changed tests | `<exact paths only>` |
| Focused command / result | `<command, exit, intended assertion failure>` |
| Intended failure signal | `<contract violation, not harness/import/setup failure>` |
| Pre-write `git status --short` | `<verbatim status>` |
| Post-write `git status --short` | `<verbatim status>` |
| Diff side effects | `<authorized test diff, production unchanged, cleanup>` |
| Next route | `authorized correction, then fresh independent review` |

The verdict remains exactly `CHANGES_REQUESTED`. This session may not repair
production or accept corrected bytes.
