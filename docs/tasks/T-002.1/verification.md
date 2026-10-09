# Verification Design: T-002.1 — Publish and distribute independent discovery evidence

Source brief: docs/tasks/T-002.1/brief.md
Source brief revision: SHA-256 ddff79b2dd1f3b6c04114ed14f370b0e6a2034ad48b75a0d63bb4ce7989f9d7c
Verification revision: 1
Authority: derived from the task brief and its cited normative sources
Status: ready

## Coverage summary

| AC / risk row | Scenarios | Notes |
|---|---|---|
| AC-01 | V-01, V-02 | Independent evidence role, explicit inputs/context, complete or partial output; no decision authority. |
| AC-02 | V-01, V-02, V-04, V-05 | Authority-derived coverage, stable current evidence, all findings and bounded context-selected probes. |
| AC-03 | V-03, V-04, V-05, V-06, V-07, V-10 | Preserve public/lifecycle/validator/process evidence, continued independent probes and authenticity limits. |
| AC-04 | V-08, V-09 | Reconciliation, failure suppression, diagnostic exception, correction ownership and premature-gate recovery. |
| AC-05 | V-10, V-11 | Narrow review writes and real installation byte preservation. |
| D-01 | V-01, V-02, V-04 | Independent/author, complete/partial and all four row states; omitted AC and unfinished sibling remain visible. |
| D-02 | V-03, V-04, V-05, V-06, V-07 | Preserve acceptance evals 1–5 and 7–9, including current continuation, real boundaries and cleanup. |
| D-03 | V-08, V-09 | Ordered records for failure, clean correction and later omitted material row. |
| D-04 | V-11 | Initial committed-target installation and explicit rerun; compare managed and unmanaged bytes. |

### Evidence limits and source anchors

- Normative sources: `docs/project-plan.md`, sections 4, 6–7, 10–11;
  `docs/task-map.json`, T-002; `docs/tasks/T-002/brief.md`, P-01–03/08.
- Preservation sources: current source acceptance skill, report reference and
  supplied evals under `skills/task-implementation-flow/task-acceptance-review/`.
  Preserve their evidence obligations while changing role-specific output to
  discovery; inherited acceptance verdicts are not discovery expectations.
- This task delivers contracts, report guidance, runnable fixtures and local
  distribution proof. Contract assertions prove structure. Disposable fixture
  probes prove setup, boundary signals and cleanup. Neither proves that an agent
  follows the discovery role. Actual role calls remain explicitly unrun here
  and belong to separately authorized T-005 qualification.
- The scenarios below define task-local observations and fixture expectations.
  They do not require executing role calls, acceptance consumers or sibling-task
  composition during T-002.1. Preflight resolves capabilities and exact targeted
  selectors; missing decisive capability must remain visible.

## Verification scenarios

### V-01 — Discovery consumes context without acquiring decision authority

Covers: AC-01, AC-02, D-01

Intent: Reject a renamed acceptance skill, an author session presented as
independent, or risk selection that ignores explicit preflight context.

Given:
- A prepared task supplies authority, verification, ART-003 context, current
  submission and applicable conditional evidence.
- A material exposure is stated in ART-003 and has a bounded decisive probe.

When:
- The discovery contract, report reference and supplied role-input cases are
  checked for independent-session and production-author-session handling.

Then:
- Independent discovery reads these inputs and links the selected probe to
  supplied context, reporting facts, suggested severity and coverage completeness.
- It issues no acceptance verdict, approved deferral or advancement.
- An author session remains self-check-only and routes to fresh discovery.
- Discovery launch guidance preserves the separate-call role and its reasoning
  recommendation without introducing launcher enforcement.

Oracle / boundary:
- Inspect the source role/output contract and supplied provenance/context
  expectations. Actual session compliance is reserved for T-005.

Variants:
- Guided direct-edit context may be conversational; absence of high-assurance
  packets alone does not prevent guided discovery or require a new dossier.

### V-02 — Partial evidence cannot hide an AC or unfinished sibling

Covers: AC-01, AC-02, D-01

Intent: Reject a silently clean partial report, coverage derived only from tests
or verification scenarios, or findings compressed into an incomplete summary.

Given:
- Supplied authority includes an AC omitted from the scenario/test claims.
- Evidence inputs include pass, fail, blocked and unchecked rows, a confirmed
  finding, an unfinished sibling row and a passing submitted suite.

When:
- Coverage and finding obligations are traced through the discovery contract,
  report reference and complete/partial fixture expectations.

Then:
- Every material authority row appears with its stable identity, cases, current
  evidence state, concrete reason, setup/oracle and exact probe or unrun reason.
- The omitted AC and unfinished sibling remain visible despite green tests;
  incomplete coverage is explicitly partial.
- Every confirmed finding retains ID, suggested severity, location, trigger,
  consequence, evidence, affected AC/invariant, explicit credible bounded sibling
  surface and invariant-level corrective direction.
- Unproved questions and unfinished rows remain separate from confirmed findings;
  continuation retains all rows, findings, regressions and next evidence owner.

Oracle / boundary:
- Reconcile supplied authority and evidence inputs with all required output
  fields and fixture expectations. Text presence alone proves only structure.

Variants:
- Complete clean evidence uses no invented finding; stopped discovery retains
  remaining rows with concrete blocked/unchecked reasons.

### V-03 — Lifecycle fixtures reach the next real public occurrence

Covers: AC-03, D-02

Intent: Reject extraction that leaves lifecycle wording but removes persisted
starting state, public wiring or the second legitimate invocation.

Given:
- Runnable discovery fixtures preserve the queue and exporter starting states
  and public operations from acceptance evals 1 and 2.

When:
- In authorized disposable state, execute the first public operation, observe
  its legitimate persisted change, then execute the next occurrence.

Then:
- Queue evidence shows the first claim and the defective next invocation that
  fails to claim TASK-2.
- Exporter evidence shows checkpoint/resume and retry behavior: legitimate
  repeated positional rows survive and retry adds no duplicate rows.
- Discovery expectations require these public observations rather than worker
  claims or pure module tests as a substitute.

Oracle / boundary:
- Observe the real public entry result and persisted queue/export state across
  occurrences; retain starting state, exact invocation, signal and cleanup.

Variants:
- Queue repeated claim; exporter resume and retry.

### V-04 — Missing capability and changed index state remain explicit gaps

Covers: AC-02, AC-03, D-01, D-02

Intent: Reject green-unit-test substitution for absent concurrency proof or
freshness checks based only on matching worktree bytes and short status.

Given:
- Acceptance eval 3 supplies a removed preflight-recorded concurrency helper
  and a policy that forbids replacement or a live scheduler probe.
- Eval 4 changes a pre-existing user's index blob while worktree bytes and short
  status still match; eval 2 supplies the unchanged index/worktree comparison.

When:
- Exercise the supplied current-capability and Git-identity observations and
  trace their discovery report expectations.

Then:
- The removed helper and its recorded/current mismatch are explicit; the
  concurrency row stays blocked or unchecked with a concrete reason and owner.
- The changed index blob is detected independently from worktree identity;
  discovery does not treat an unsafe guessed scope as current proof.
- No helper is invented and no user file/index state is reset or absorbed.
- Passing submitted units do not convert either gap into a clean row.

Oracle / boundary:
- Actual fixture filesystem/helper state and separate Git index/worktree
  identities, plus the required partial-report and evidence-owner fields.

Variants:
- Missing helper; changed index blob; unchanged index/worktree control.

### V-05 — Interacting cases and prior passes receive current independent probes

Covers: AC-02, AC-03, D-02

Intent: Reject stopping after one finding, testing only the selected entity or
one corrupt field, or copying a previous pass into current evidence.

Given:
- Runnable fixtures preserve acceptance eval 5's ledger cases and evals 7–8's
  workflow defects and prior pass/fail/unchecked continuation.

When:
- Independently exercise the bounded contract cases against current fixture
  bytes, continuing through safe affordable rows after the first failure.

Then:
- Ledger probes cover selected/non-selected state, zero/one/two active owners,
  latest-attempt ordering, exact dependency-ready set, stopped-parent/running-child
  coherence, boolean-as-integer and string-as-collection type confusion.
- Workflow probes retain WF-TAMPER, WF-REPLAY and WF-DECISION, demonstrating
  coherent prompt/model tampering, replay after verifier drift and contradictory
  decision-only publication reaching execution.
- Prior rows retain their identities but receive current corroboration; prior
  WF-TAMPER pass is not reused as proof, and WF-DECISION is not dropped.
- Every independently reproduced defect is reported with its bounded sibling
  surface; unavailable remaining rows retain explicit reasons.

Oracle / boundary:
- Observe the ledger validator and persisted workflow/execution boundary, then
  reconcile all supplied cases and continuation rows with discovery expectations.

Variants:
- Initial workflow discovery and discovery with the supplied prior continuation.

### V-06 — Validator evidence includes valid and targeted-invalid instances

Covers: AC-03, D-02

Intent: Reject schema text, deserialization, producer validation or an unrelated
suite as proof of a required executable validator boundary.

Given:
- A task-material row depends on a validator; supplied setup identifies its
  relevant constraint, valid instance and deliberately invalid instance.

When:
- Independently invoke the relevant validator on both instances.

Then:
- Evidence records acceptance of the valid instance and rejection of the
  targeted-invalid instance, using the schema's declared draft when applicable.
- If the required boundary cannot run, its row stays blocked/unchecked with the
  actual capability reason; it is not reported as passed.

Oracle / boundary:
- The executable validator's results for supplied inputs, plus discovery's
  explicit proof/gap requirements. Setup without results is not behavior proof.

Variants:
- Available validator; unavailable required validator. Apply only where the
  task contract makes that boundary material.

### V-07 — All process cases produce bounded observable cleanup evidence

Covers: AC-03, D-02

Intent: Reject mock-only process proof, first-finding termination or cleanup
claims that leave a descendant, process group or inherited pipe alive.

Given:
- The discovery fixture preserves eval 9's PROC-RESIST, PROC-PIPE and PROC-RACE
  starting states, real process invocation and bounded cleanup.

When:
- Exercise each case using observable synchronization and bounded waits in
  authorized local disposable state.

Then:
- Each case exposes its resistant-descendant, exited-leader/pipe-holder or
  transient-visibility defect and retains its result in discovery expectations.
- Safe independent sibling probes continue after the first finding.
- Cleanup confirms descendant/process-group disappearance and inherited-pipe
  release after each probe; incomplete cleanup fails the probe.

Oracle / boundary:
- Real process IDs/groups, synchronization signals, runner result and pipe
  closure. Keep raw observations and verify that no fixture processes survive.

Variants:
- PROC-RESIST; PROC-PIPE; PROC-RACE.

### V-08 — Targeted failure suppresses an ordinary aggregate

Covers: AC-04, D-03

Intent: Reject running an aggregate merely to complete a checklist after decisive
failure, or recording suppression without its actual command-order basis.

Given:
- A reconciled material ledger and an already authorized owning aggregate
  command are supplied; a targeted probe produces decisive current failure.

When:
- Trace the failure case's ordered probes and expected discovery gate record.

Then:
- Independent safe affordable targeted rows continue, but the ordinary aggregate
  is not run. Its record retains exact command or not run, discovery owner/stage,
  failure reason and current evidence.
- A distinct diagnostic aggregate is permitted only with its separate authorized
  purpose recorded; it does not erase failed or unfinished rows.

Oracle / boundary:
- Supplied setup and ordered expected records distinguish suppression from
  unauthorized execution. Local record checks do not prove role compliance.

Variants:
- No distinct diagnostic authorization; explicit distinct diagnostic purpose.

### V-09 — Correction and late omissions cannot reuse a premature gate

Covers: AC-04, D-03

Intent: Reject a copied prior gate/pass, an aggregate before unfinished targeted
work, or assigning the corrected discovery aggregate to acceptance.

Given:
- Correction case: corrected current bytes, prior findings/regressions and
  unfinished rows, with setup that can now produce clean targeted evidence.
- Omission case: a reported aggregate is followed by discovery of a material row
  omitted from its reconciliation.

When:
- Trace each case's supplied state transitions and ordered expected records.

Then:
- Fresh correction discovery corroborates current bytes, reruns reviewer
  regressions, finishes unfinished rows and reconciles authority/scope before
  owning one justified aggregate after clean targeted evidence.
- Any remaining unavailable row has a concrete non-gate reason; no selected
  safely runnable material adversarial probe remains before a justified gate.
- In the omission case, the earlier gate becomes explicitly premature. The
  missing targeted proof comes first; a rerun occurs only after clean targeted
  evidence and only while still justified.
- Each record retains command or not run, owner, stage, reason and current
  evidence. No gate or command is added, and acceptance consumes this record.

Oracle / boundary:
- Ordered expected records tied to supplied current state distinguish correct
  ownership/order from premature, stale or repeated aggregates. No acceptance
  consumer call or cross-task recovery qualification is required here.

Variants:
- Clean correction; late omitted row whose probe passes; late omitted row whose
  probe fails and therefore keeps the aggregate suppressed.

### V-10 — Discovery owns only authorized output and cannot authenticate itself

Covers: AC-03, AC-05

Intent: Reject inherited repair/tracker permissions, report overwrite or a report
that treats its own assertions/digests as independent authenticity proof.

Given:
- Ordinary review inputs include production/tests/trackers and prior numbered
  discovery reports; durable mode authorizes only the next unused package path.

When:
- Check guided and durable discovery write rules, report reference and supplied
  output/scope expectations against these inputs.

Then:
- Guided output may remain inline; durable output uses only the authorized
  next-unused `reviews/discovery-NN.md` and preserves prior reports.
- Production, tests, trackers and other user work remain unchanged.
- Required before/after scope records attribute only the new report. The report
  applies to identified reviewed bytes and never claims to authenticate itself.

Oracle / boundary:
- Source permission/report contract and fixture expectations for output paths
  and before/after state. Actual role write compliance remains T-005 evidence.

Variants:
- Inline guided output; authorized durable output with prior numbers occupied.

### V-11 — Canonical installation distributes bytes within managed ownership

Covers: AC-05, D-04

Intent: Reject source-only publication, missing required references, existence-only
installation checks or replacement of unrelated target content.

Given:
- A disposable committed Git target has user AGENTS text and unrelated files.
- Source selection/guidance includes the new discovery package and references.

When:
- Run the canonical installer into that target, compare installed/source bytes,
  then explicitly rerun after stale managed content and an added unrelated file.

Then:
- Initial install and rerun project the discovery skill and all required
  references, selected guide/helpers and marked AGENTS block from current source.
- Stale managed content is replaced within existing ownership; unrelated skill,
  helper and file bytes and AGENTS text outside the marked block remain unchanged.
- DEVELOPMENT_SKILL_SOURCES, PROFILE_SKILLS_README, SHARED_SCRIPT_FILES, focused
  tests and discovery entries in root/profile/flow READMEs are synchronized.
- No shared dependency or installation feature is invented; the active
  repository's installed `.agents/` copies are not refreshed.

Oracle / boundary:
- Real canonical installer filesystem/Git boundary: byte comparison of the
  complete required package and managed projection, plus before/after unmanaged
  identities. File existence or successful exit alone is insufficient.

Variants:
- New committed-target install; explicit rerun with stale managed content and
  unrelated target content. Unborn/drift-feature qualification belongs to T-004.

## Implementation handoff

- Treat this file as derived verification guidance, not a replacement for the
  task brief. Status ready means design complete, not preflight ready or accepted.
- Preserve stable scenario IDs across a reasoned coverage revision. A revised
  artifact supersedes affected readiness and evidence until focused preflight
  produces a ready result for the new revision.
- Implement the smallest production and test changes that satisfy the brief and
  exercise these scenarios. Concrete test structure, framework usage, helpers
  and file placement remain implementation choices within the brief's scope.
- Obtain ready standalone preflight before implementation. Resolve exact
  targeted discovery/profile selectors and fixture capabilities there; reuse
  existing setup/probes rather than adding a generic harness.
- Follow the brief's fail-first route. After targeted local checks pass, run the
  owning suites one at a time from repository root:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_review_discipline.py`,
  then `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py`.
  These implementer checks are distinct from the discovery-owned gate records
  modeled by V-08/V-09. Independent review uses narrow distinct corroboration.
- Record structural checks, real fixture/installer observations and unrun role
  checks separately. Add no repository-wide, network or agent-budget check.
- If implementation discovery cannot exercise a scenario at its stated boundary,
  route the conflict to task design/preflight rather than weakening the oracle.
- After implementation or correction, preserve applicable conditional stages and
  hand completed bytes to fresh independent acceptance review; end the
  implementation invocation. Later role/composition proof remains with T-005.
