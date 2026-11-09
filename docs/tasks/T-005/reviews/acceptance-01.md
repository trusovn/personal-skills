# T-005 acceptance review

The installed journey has current independent evidence for original baseline B,
separate I/R comparisons, correction against B, preserved source/index/history,
and real required native failure followed by recovery. Prepared agent cases
remain preparation only. Advancement is blocked by missing current independent
maintainability evidence for the significant test/harness addition. Supply the
existing review record, or obtain that review if it was not performed, then
return for a separate fresh acceptance decision. No production repair is requested.

Verdict: **INCONCLUSIVE**

Provenance: independent acceptance session; this session authored no reviewed
production, test or preparation bytes. Guided profile. The only intentional
write is this report. No subagents, reproducer, aggregate rerun, live probe,
installation refresh, tracker update or advancement was performed.

## Authority, identity and ownership

- Authority: [brief](../brief.md), AC-01–AC-05 and submission route;
  [verification](../verification.md), revision 1;
  [preflight and decision context](../preflight.md);
  [project plan](../../../project-plan.md), T-005 and section 11.
- Submission: [results](../results.md), READY_FOR_REVIEW, including the
  scenario-to-evidence map, retained producer archives and live-qualification limits.
- Active instructions: project-local `.agents/skills/task-implementation-flow/task-acceptance-review/SKILL.md`
  and `.agents/skills/README.md`. The latter requires current independent
  maintainability evidence for significant harness changes; the brief and
  verification design explicitly retain that stage.
- HEAD: `9883a7966308ff9cd556dd9edf99530d39cee0d2`.
- Current staged tree: `3aa40b2146b6472e69b92dd598cba9f4236d60f8`.
  Discovery reviewed `1038977b7494af481130cc0fd44977ed05f9809d`.
  Comparing those trees shows only the added discovery report. All ten
  discovery-reviewed paths retain their exact index bytes. Worktree equality
  was checked separately with `git diff --quiet`; matching status alone was
  not used as byte proof.
- Brief and task-index edits are pre-existing user preparation, as recorded in
  readiness/discovery. Implementation is the added measurement test; the
  remaining changes are preparation, results and scoped discovery references.
  No production runtime, official plan or task map changed. No unexplained
  overlap was identified.

## Findings and conditional evidence

No findings. There is no confirmed in-scope production or test defect requiring
bounded correction. No deferral or known-issue record is proposed.

**E-MNT-01 — blocked conditional evidence.** Discovery says the user reported a
maintainability pass, but explicitly does not authenticate that stage. The current
invocation supplies no such review record, and results still names fresh
maintainability review as the next stage. A secondhand pass does not establish
review scope, reviewed byte identity, independent R evidence, rationale
dispositions or outstanding findings. This is an evidence gap, not proof that
the review failed or never occurred. Evidence owner: maintainability reviewer,
through the coordinator. Correction owner: none unless that review finds a defect.
Authority owner: task owner; no authority change is requested.

Provide the current independent maintainability decision/continuation tied to
`tests/test_maintainability.py` as staged, including its own comparison and the
retained-breach rationale dispositions, native-evidence admission and remaining
findings. Reuse an existing current record; do not rerun review merely because
the result was omitted from this package. Acceptance does not perform that
specialist review itself.

## Admitted discovery and reconciled coverage

Admitted [discovery-01](discovery-01.md), including its continuation and P1–P9
command record. Independent discovery is complete for the bounded behavioral
scope; it supplies no authenticated maintainability decision. Producer logs and
the result map remain claims corroborated only to the extent of those probes.

| Stable row | Cases and submitted evidence | Admitted evidence and reconciliation |
|---|---|---|
| V-01 | AC-01; journey.log/captured-journey.log, B→I→R→C | **pass**: P1/P2 plus current test trace; removed distribution, unrelated cwd, installation-local tools, separate I/R invocations, exact report pairs/scope/settings/hashes and 5→7→6 values. |
| V-02 | AC-02; measurement-final.log, immutable report/native history | **pass**: P1/P2/P5 and preservation assertions; staged/unstaged/untracked start, real index bytes and prior reports preserved; owning empty/add/delete/settings/unknown/collision/unavailable/incompatible cases independently rerun. |
| V-03 | AC-03; journey native JSON and command history | **pass**: P1/P2; same whole-project required Ruff F401 command returns 1 on edited input and 0 on corrected input, alongside complete advisory comparison; checked hashes, producer/stage and failure history retained. |
| V-04 | AC-04; prepared qualification map and fixture logs | **pass for preparation only**: P3/P4 and catalog/README trace; all plan V-001–V-008 allocations retained, including finite V-005 judgment, V-006 policy/gap, V-007 re-entry and V-008 native/reuse/no-check variants. Fresh agent judgment remains unrun. |
| V-05 | AC-05; results, interpreter/pins and focused/aggregate logs | **pass for truthful publication**: P1–P9 and current result trace; real pinned suite has no skips, aggregate failure/skips remain explicit. This row does not assert an aggregate pass or discharge E-MNT-01. |
| E-MNT-01 | Required conditional stage for significant test/harness changes | **blocked**: secondhand pass only; current independent review, R comparison and disposition record not supplied. Evidence owner: maintainability reviewer/coordinator; no correction currently requested. |

All discovery row IDs are preserved. Discovery reported no finding IDs or
unfinished behavioral rows. P6 independently rejected deliberately wrong
correction complexity; its command was `P -B /tmp/T-005-evidence/fault_control.py`,
where P is the pinned interpreter named in discovery. No reviewer regression
files were added by discovery or acceptance. No acceptance-relevant executable
schema constraint changed; registry shape checks are structural evidence only.

## Contract reconciliation

Expected ART-006 composition evidence maps to the actual new public-CLI test
and result record. There is no runtime CLI, schema, export, configuration or
migration delta. Measurement now declares that test/results authority; implementer
and reviewer records route to measurement and retain live-compliance limits.
The flow README removes its obsolete composition limitation without claiming
agent qualification. Existing index ownership/plan mappings remain applicable;
only summaries/declarations changed, so generated index contents need not change.
No declared/current routing mismatch was found. Registry consistency does not
authenticate a maintainability review or substitute for behavioral evidence.

Installer membership, managed guide and shared-file lists were inspected.
The changed nested flow README is not the managed `skills/README.md`; no
profile-owned runtime dependency or installed skill bytes changed. No installer
list or installation-documentation synchronization is needed for this delta.

## Aggregate gate consumed, and acceptance checks

Discovery owner/stage: initial independent task-review-discovery. Its command
order is P1 focused journey → P2 owning suite → P3 implementer fixtures → P4
reviewer fixtures → P5 installer → P6 mutation control → P7 architecture → P8
contracts → P9 aggregate. Targeted material evidence was clean before P9.

Consumed exact aggregate command:
`python3 tools/verify.py > /tmp/T-005-discovery-aggregate.log 2>&1`.
Reason: required cross-cutting integration after clean targeted evidence;
discovery records explicit user approval for cost and native execution.
Result: **FAILED**, exit 1; seven checks, one failed, solely active-profile drift
(112 compared paths; ten differences: four changed, six missing). Five suites
ran 537 tests with 32 analyzer skips; contracts passed. Independent pinned P2
ran all 34 measurement cases without skips. It does not turn the aggregate green.

Disposition: AC-05 and readiness explicitly require reporting active-profile drift
as a failed diagnostic and prohibit refreshing this active installation. T-005
requires real disposable installed proof, which P1/P2 supplies. The diagnostic
therefore remains FAIL and does not qualify the active profile; it is not an
unresolved requirement to make source and active installation equal in this run.
No hard native obligation is waived. Historical T-004 acceptance supports context
only; it is not current T-005 proof. Live qualification remains outside completion.

Acceptance did not rerun discovery's probes or aggregate. Higher-priority
repository instructions require the canonical architecture and contract checks
before handoff; these narrow structural checks were run and passed:

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py`: four tests, OK.
- `python3 tools/check_contracts.py --root .`: eight subsystems, 26 indexed refs, OK.
- `git diff --cached --check`: pass; `git diff --quiet`: pass before report write.

These checks supply no missing independent maintainability judgment.

## Scope preservation

Exact status before this report:

```text
M  docs/contracts/implementer-feedback.json
M  docs/contracts/measurement.json
M  docs/contracts/reviewer-feedback.json
A  docs/tasks/T-005/brief.md
A  docs/tasks/T-005/preflight.md
A  docs/tasks/T-005/results.md
A  docs/tasks/T-005/reviews/discovery-01.md
A  docs/tasks/T-005/verification.md
M  docs/tasks/index.json
M  skills/task-implementation-flow/README.md
M  tests/test_maintainability.py
```

Exact status afterward is the same eleven lines plus:

```text
?? docs/tasks/T-005/reviews/acceptance-01.md
```

The report remains unstaged. The index tree remains the current tree above.

## Questions, residual limits and next route

No user policy question or production-fix request. The sole unresolved admission
item is E-MNT-01. Live agent judgment, routing compliance and tamper resistance
remain unqualified by design; temporary producer archives are local evidence,
not guaranteed durable storage. No approved deferrals.

Next: coordinator obtains the current independent maintainability record from
its reviewer, then supplies it with this report and the unchanged staged scope
to a separate fresh acceptance session. If that stage requires correction,
implementation must instead re-enter affected conditional stages and fresh
discovery before fresh acceptance. No automatic repeat of unaffected gates.

## Review continuation

- Iteration/identity: acceptance-01; independent guided decision; HEAD and
  staged tree above. Only discovery report differs from discovery-reviewed tree.
- Coverage: V-01 pass; V-02 pass; V-03 pass; V-04 pass for preparation;
  V-05 pass for truthful publication, aggregate FAILED; E-MNT-01 blocked.
- Finding IDs: none. Evidence item E-MNT-01 is not a confirmed defect.
- Continuity: all discovery statuses retained; P1–P9 are discovery-owned
  current evidence, producer result/log claims remain separately attributed.
  Missing conditional review does not erase behavioral passes. Incomplete reason:
  no current independent maintainability record supplied. Evidence owner:
  maintainability reviewer/coordinator; correction owner: none pending findings;
  authority owner: task owner. Influenced siblings: submission/re-entry route,
  retained-breach rationale and R comparison; no sibling production defect found.
- Preparation/context: brief AC-01–AC-05; verification revision 1;
  ready preflight/decision context; results; discovery-01 and continuation.
- Reviewer regressions: no repository files; discovery P6 command above;
  acceptance added none.
- Aggregate consumed: P9 FAILED solely on diagnostic active drift, after P1–P8;
  no rerun, refresh, pass claim or waiver.
- Next: recover current maintainability evidence → separate fresh acceptance
  on unchanged bytes, or affected correction route if that review finds defects.
