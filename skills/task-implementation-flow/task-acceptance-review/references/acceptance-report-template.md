# Task Acceptance Report: `<TASK-ID>` — `<brief title>`

<In plain language, explain the change's contribution to the requested outcome,
what current admitted evidence supports, whether work may advance, and any
material limitation. Name the next actor/action and any owner decision. Derive
this opening from the verdict and evidence below, linking supporting records
rather than repeating their ledgers. Keep reported checks, independent findings,
and historical acceptance distinct; missing/stale evidence remains visible.
Reuse an existing explanation where possible.>

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
| Affected boundary | `<interface, consumer, state, or subsystem boundary>` |
| Evidence | `<admitted discovery trace, probe result, or code fact>` |
| Impact (assessed separately from likelihood) | `<materiality under supplied decision context, not severity label or reviewer taste>` |
| Likelihood / exposure | `<credible exposure or next-change horizon; low likelihood cannot erase catastrophic data/security/irreversible-state consequences>` |
| Existing mitigation | `<existing safeguard actually in effect; planned work is not mitigation>` |
| Affected AC | `<AC-ID>` |
| Broken invariant | `<task-authorized property that does not hold>` |
| Credible sibling surface | `<contract-implied cases sharing that invariant>` |
| Smallest corrective direction | `<invariant-level bounded direction; no patch or field-local special case>` |
| Fix-now / deferral rationale | `<contextual reason tied to supplied operating/business/consumer/maintenance context; passing ACs do not excuse demonstrated material risk>` |
| Disposition | `<block-fix-now | accepted-deferral candidate | observation | retained as unresolved with reason and owner>` |

Keep confirmed findings separate from unproved questions and from unchecked
coverage rows. Every confirmed finding and unfinished row from the admitted
discovery report survives the decision with its current result and evidence,
or its incomplete reason and owner.

### Accepted deferrals and coordinator recording

A bounded non-material confirmed finding may be accepted with a proposed
known issue only when all required evidence passes, the effect is bounded,
consumers are compatible, and the deferral waives no required AC, proof, or
demonstrated material risk and imposes no hidden consumer workaround. This
report proposes the deferral; the coordinator (human or AI acting within the
approved task authority) alone records it, before authorized advancement, in
`docs/known-issues.md` or the repository's declared tracker and format. The AI
coordinator needs no extra human confirmation for an acceptance-approved bounded
deferral. Requirement/proof waivers and unresolved material-risk decisions stay
with the owner. Reuse the stable issue ID and preserve acceptance provenance and
history on repeat recording. Recording failure blocks advancement, not the
acceptance judgment. The acceptance review never creates or edits the tracker, and no
known-issues file is required before a deferral exists.

The proposed record carries: a stable project issue ID; task/review/finding
provenance; trigger, consequence, and evidence; impact and likelihood;
affected boundary and consumers; deferral rationale; follow-up owner and
action; and reassessment conditions. Optional proportional context links may
add subsystem/area, existing invariant/contract/flow/plan IDs, related issue
IDs distinguishing confirmed relationships from suspected similarity,
safeguards or explicit assumptions with reassessment triggers, and relevant
migration/refactor/replacement work distinguishing proposed from committed
work. Missing links mean unknown relationships, not their absence; planned
work alone is not existing mitigation. Preferences, polish, and unproved
minor concerns are recorded as observations, never as known issues. A later
priority change alone does not reopen an accepted deferral; changed material
facts that invalidate an actual acceptance assumption can require focused
review under existing authority.

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
| `question | blocked | unchecked | residual risk | observation / assumption` | `<observed limit or stated reasonable assumption>` | `yes | no` | `<owner/action>` |

A failed required behavior is a finding, not residual risk. A missing required
oracle is blocking and normally yields `INCONCLUSIVE`. Missing discovery or
missing decisive validator evidence routes to the discovery owner with the
exact gap. Ordinary uncertainty continues under a stated reasonable assumption
recorded here as an observation; unresolved decision-critical uncertainty with
credible serious-delay or materially-costlier-later consequences is escalated
as one focused question naming the consequence and the needed fact.

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

Preserve separate correction/evidence/authority owners through the coordinator
for every finding and unfinished row. Name the first outstanding applicable
conditional stage and complete ordered remainder before fresh discovery and
the separate decision; tests-only exceptions require explicit policy authority.
Clarification/evidence requests do not imply production changes. A genuine
reference-only updater → fresh acceptance shortcut requires actual effects and current behavioral proof;
otherwise repeat affected discovery/gates. Unchanged-authority coverage revision
returns to verification design → focused ready preflight → revised-scenario
proof → new decision. New proof cannot excuse old readiness, including its
substitution after recovery. Changed requirements return to their authority owner.

## 10. Review continuation

Copy this compact block intact into the next decision context:

```markdown
Review continuation:
- Iteration / current byte identity: <iteration; HEAD/scoped diff identity>
- Coverage rows: <every stable row ID = pass/fail/blocked/unchecked + reason>
- Finding IDs: <all IDs or none>
- Finding/scenario continuity: <prior statuses, current producer-attributed evidence, incomplete reasons and separate correction/evidence/authority owners; influenced siblings>
- Preparation/context: <brief, verification revision, preflight and context references>
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
