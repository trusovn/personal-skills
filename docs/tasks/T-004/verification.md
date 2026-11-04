# Verification Design: T-004 — Add independent measurement and review decisions

Check that a fresh reviewer compares the actual submitted code with the original
task baseline, checks affected responsibilities, and records every required
rationale disposition. Advisory metrics must permit justified breaches. Required
native checks retain their policy, scope and owner. Corrections must preserve
history and return through only the affected stages in the existing route.

T-004 delivers source guidance and executable eval preparation. These cases
define the decisions that the prepared evals must distinguish. Local fixture and
tool checks prove only the behavior they exercise. They do not prove reviewer
compliance. T-005 owns the complete installed handoff journey.

## Shared setup and evidence responsibilities

- Use disposable Git repositories with a bounded task, actual before/after code,
  original format-5 baseline B, implementer comparison I, affected-function
  attribution, rationale and native-obligation handoff. B and I are upstream
  inputs normally produced by preflight/self-preflight and the implementer.
  Label seeded histories and evidence. Where a case claims tool execution,
  generate its evidence through the real public CLI rather than fabricated JSON.
- Supply an installation-local runtime and already prepared pinned interpreter
  for actual measurements. Permit fresh JSON/text report writes under target
  `.quality/reports/` and, when requested, the next unused package-contained
  `reviews/maintainability-NN.md`. Keep all other reviewer paths read-only.
  Preflight confirms tools, authorized paths and budget. Do not provision tools,
  refresh this session's installation or use helpers from another installation.
- Snapshot source, real Git index, original baseline, prior report pairs and
  unrelated user work. Comparison and review must preserve them. A numbered
  review binds to actual reviewed-byte identities, not just matching status text.
  Guided colocated hashes establish provenance, not tamper resistance.
- Reuse maintainability evals 1–10 and the existing `four-blockers`,
  `genuine-stop`, `correction-round`, `test-assets*` and `semantic-*` setup
  variants. Preserve their distinct defect/control oracles. Existing measurement
  coverage proves numeric boundaries, compatibility, missing counts, report
  collisions, added/deleted files, dirty-index preservation and installed CLI
  operation. Extend existing setup only for missing reviewer evidence.
- For V-01–V-10, the implementer supplies a source-guidance trace, executable
  case inputs, allowed tool/report paths and a decisive artifact-based oracle.
  Focused local checks establish setup and exercise claimed tool boundaries.
  Prepared grading checks actual diff, report contents/identities, command
  history, rationale and ordered route; keywords alone cannot pass a case.
- Fresh independent discovery corroborates preparation, coverage and claimed
  local behavior for V-01–V-11. Separate acceptance decides T-004 advancement.
  Implementation checks supply neither independent role. Live reviewer execution
  and independent grading require separate approval and remain unqualified when
  unrun. This design does not require launching those reviewers now.

## Test cases

### V-01 — A fresh reviewer measures submitted bytes independently

**Situation:** B covers relevant production, test, eval, fixture and harness
folders. The submission changes a Python file, adds a file and deletes a captured
file. I and the native handoff are available. Other prerequisites are valid.

**Action and expected result:** Invoke maintainability review for current bytes.

| Case | Starting state | Exact expected result |
|---|---|---|
| V-01a | Fresh session; I matches current bytes | Reviewer invokes its own installation-local comparison R against B for every affected changed/added/deleted Python path. R uses new JSON/text paths and identifies actual current bytes. I alone is not independent evidence. All relevant asset groups remain in scope. |
| V-01b | Edit submitted code after I, without changing its short-status text | Reviewer detects I's stale source identity and compares actual current code. It does not adopt I's old values or a prior verdict for the edited bytes. |
| V-01c | This session authored reviewed production bytes | Output is `SELF_CHECK_ONLY`; it may carry checks/findings but no independent `ACCEPT`, `CHANGES_REQUESTED` or `INCONCLUSIVE`. Route to a fresh reviewer. |
| V-01d | Production unchanged; this session authored only reviewed test/eval/harness bytes | Same independence refusal as V-01c. A tests-only label does not create independence. |
| V-01e | Reviewer uses an isolated clone with another absolute root | Handoff names exact source and receiving paths for B/I JSON and text siblings. Transfer ignored reports explicitly, validate logical project and applicability, then compare through the receiving installation. Commits alone are not report transfer. |

**Why test this:** An apparently complete submission can describe different code
or supply only author-produced evidence.

**How to check:** Prepare real capture/edit/compare inputs and inspect report
source hashes, baseline references and invocation history. Assert snapshot/index
preservation. Reuse same-session eval 1 and portable report-transfer tests.
Different mounts are permitted provenance, not proof of logical project identity.
Local CLI success proves comparison facts; only a separately graded fresh-agent
run could prove the reviewer's independent actions.

### V-02 — Invalid comparison evidence stays explicit and recoverable

**Situation:** Start from V-01a. Change only the named prerequisite, keeping the
rest valid so the intended guard is reached. Review remains possible except for
the specified evidence gap.

**Action and expected result:** Validate evidence and attempt bounded recovery.

| Case | Decisive input | Exact expected result |
|---|---|---|
| V-02a | B is missing; current measurement is available | Measure current code at fresh paths and state the missing before-state gap. Do not capture edited code as B or claim a complete delta. |
| V-02b | B comes from another logical project with matching relative paths | Reject applicability. Path compatibility does not establish project identity. Attempt recoverable current measurement and name the before-state recovery owner. |
| V-02c | B has an incompatible format, tool version, effective settings or selected checks, varied separately | State each incompatibility. Remeasure before code only if its exact preserved pre-edit bytes are verified; otherwise record current evidence and the unresolved before gap. Do not silently change settings or recapture edited code. |
| V-02d | B or current report is incomplete, or omits required selected-profile coverage | State missing checks/scope and attempt recoverable current measurement. Partial evidence is not full-profile or clean comparison evidence. |
| V-02e | Runtime or pinned analyzer unavailable; advisory evidence is not indispensable | Record unavailable evidence, owner and recovery. Continue bounded semantic review where possible. Absence alone does not force an incomplete verdict or prove clean metrics. No installation or cross-root fallback. |
| V-02f | Same unavailable evidence, with explicit task/repo authority making it indispensable | Preserve the authority reference, missing capability and recovery owner/action. Required proof remains owed; unresolved material evidence yields an incomplete review, normally `INCONCLUSIVE`, never clean completion. |
| V-02g | Docs-only scope; separately unsupported-language scope | Record measurement N/A with its reason. Preserve applicable native-check and review duties. Do not generate empty successful Python comparison evidence. |
| V-02h | Proposed output collides with existing JSON; separately only its text sibling exists | Choose a fresh report pair. Preserve both old siblings and B; do not delete or overwrite to recover. |
| V-02i | Caller requests an external durable review path or an already occupied numbered path | Preserve the package/report-path boundary. Require the next unused `reviews/maintainability-NN.md`; do not overwrite or move durable review into runtime storage. |

**Why test this:** Missing evidence can otherwise become a false zero, a false
before state, or an unnecessary stop on advisory absence.

**How to check:** Reuse actual incompatible/missing-tool/partial-profile and
collision CLI cases; prepare reviewer recovery inputs for each distinct row.
Inspect new artifacts and preserved originals, not only failure exit codes.
V-01a is the success control. A seeded incompatible identity proves consumer
handling only; do not claim it proves execution by that historical tool version.
V-02i extends existing report-path eval 3 without weakening its refusal.

### V-03 — Rationale dispositions follow affected breaches and target equality

**Situation:** Targets remain complexity 10, statements 50 and arguments 5.
Reports and actual diffs establish the values and affected responsibilities.
All required native evidence is current and semantic review is clean except
where stated. Rationale, when supplied, identifies report, function, metric,
known before/after, cohesion and the cost of a plausible alternative.

**Action and expected result:** Review each independent row under
[plan section 5](../../project-plan.md#5-lifecycle-and-decision-rules).

| Case | Affected responsibility / measurement | Exact expected result |
|---|---|---|
| V-03a | Complexity 6 → 8; statements 40 → 49; arguments 3 → 4 | Information only. No required per-increase defense or metric-driven refactor. |
| V-03b | Complexity 9 → 10; statements 49 → 50; arguments 4 → 5 | Equality is within target. Same information-only handling as V-03a. |
| V-03c | New function at 11 complexity, 51 statements or 6 arguments | Explicitly dispose of retained-breach rationale. A justified cohesive breach can receive `ACCEPT`; exceeding target alone cannot request changes. |
| V-03d | Existing function crosses 10 → 11, 50 → 51 or 5 → 6 | Explicitly dispose of the newly crossed breach rationale, without mandatory threshold compliance. |
| V-03e | Existing breach worsens 11 → 12, 51 → 52 or 6 → 7 | Explicitly assess and dispose of the worsening rationale. A threshold alone remains insufficient for rejection. |
| V-03f | Materially edited hotspot stays 11 → 11, 51 → 51 or 6 → 6 | Consider useful bounded cleanup and explicitly dispose of the retention rationale. Equality above target does not waive the obligation. |
| V-03g | Materially edited hotspot improves 12 → 11, 52 → 51 or 7 → 6 | Retained breach still needs a disposition. Improvement alone does not waive it; reaching target is not mandatory. |
| V-03h | Materially edited hotspot reaches 11 → 10, 51 → 50 or 6 → 5 | No retained-breach rationale is required solely because the starting value was above target. Semantic review still applies. |
| V-03i | A required rationale is missing or omits its plausible alternative's cost | Recover the missing explanation. Do not treat a bare threshold as a design blocker or claim complete dispositions while rationale is owed. If indispensable proof cannot be recovered, carry the incomplete-review state and owner. |
| V-03j | One cohesive design explanation covers related breached metrics | Accept one explanation covering those metrics, with an identifiable disposition for each obligation. Do not demand duplicate defenses. |

**Why test this:** Blanket rejection over-refactors cohesive code. Blanket
acceptance misses materially edited legacy hotspots.

**How to check:** Use real native counts where available; existing numeric tests
corroborate the at/below/above boundaries. Prepare separately identifiable metric
variants for V-03a–h; no Cartesian product across metrics is needed because each
uses the same advisory decision rule. Grade retained code, rationale and explicit
agreement or counterargument. V-03c supplies an `ACCEPT` control against an
always-rejecting reviewer. A counterargument must identify concrete future
maintenance cost and the smallest reasonable correction, as in V-05.

### V-04 — Attribution follows responsibilities rather than file membership

**Situation:** Provide small hand-auditable diffs, report symbol inventories and
implementer attribution. Include an over-target sibling in the same file.

**Action and expected result:** Verify attribution before deciding dispositions.

| Case | Diff / supplied attribution | Exact expected result |
|---|---|---|
| V-04a | Another function changes; legacy sibling only shifts lines or receives formatting | Untouched sibling stays context. Reject file-wide attribution and impose no mandatory rationale, cleanup or blocker on that debt. |
| V-04b | Implementer labels a behaviorally or structurally edited hotspot untouched | Reviewer identifies the actual affected responsibility and applies V-03f/g as applicable. The implementer's label cannot waive required rationale. |
| V-04c | Function renamed; separately moved; separately extracted into helpers | Identify each relationship from diff/context and assess the original responsibility with its helpers. Unmatched symbols remain unmatched; do not invent numeric cross-symbol deltas. |
| V-04d | A native count is absent on one side, such as an exempt override method | Preserve unknown before/after and explain the evidence limit. Do not infer zero or improvement from a missing diagnostic. Other known metrics remain usable. |

**Why test this:** Mechanical attribution can punish untouched code or reward
extraction that hides responsibility and complexity.

**How to check:** Reuse symbol-interpretation and native-exemption tool coverage.
Prepared reviewer oracles compare supplied attribution against actual diffs and
immediate collaborators. Numeric reports alone cannot establish affectedness.
Each relationship in V-04c needs a visible variant, not a combined ambiguous diff.

### V-05 — Semantic cost decides findings even when metrics improve

**Situation:** Reuse working code with current required gates. The defect/control
pairs contain actual changed responsibilities, including significant test assets.

**Action and expected result:** Perform bounded semantic review.

| Case | Concrete input | Exact expected result |
|---|---|---|
| V-05a | Extraction lowers a metric but adds misleading names/navigation, opaque argument containers or speculative forwarding layers | Assess helpers with the original responsibility. Report each demonstrated material regression with diff evidence, future maintenance cost and bounded correction. Smaller metrics cannot excuse it; a preference alone cannot block. |
| V-05b | Existing `semantic-defects` reservation/recovery variant | Preserve distinct misleading query/unit contracts, scattered invalidation ownership and lost failure-context findings. Ground each in its local contract and credible future change/investigation; do not turn review into functional acceptance. |
| V-05c | Existing `semantic-control` variant with explicit protocol branches, caller-locked mutation and documented legacy wire name | Accept justified complexity and existing boundaries after required proof passes. Do not demand a framework, purity rewrite or unrelated cleanup. |
| V-05d | Existing `test-assets` defect variant; production unchanged and ordinary suite green | Review duplicated scenario authority and mutable occurrence state as distinct maintenance problems. A passing functional suite does not excuse those design regressions. |
| V-05e | Existing `test-assets-control` with independent observations and stable text assertion | No blocker merely for legitimate independent fixture construction or public text assertions. An ordinary assertion edit alone creates no mandatory review/gate/registry stage. |

**Why test this:** A metric-only reviewer misses semantic regressions. A reviewer
that rejects all abstraction or complexity creates unnecessary correction work.

**How to check:** Reuse held-back defect/control observations in maintainability
evals 5/6/9/10 and the four-blocker fixture. Check actual code and concrete future
cost, not preferred terminology. Preserve naming, coupling, explicit dependency,
locality, testability and abstraction-cost guidance. Grade bounded correction
directions; wider useful cleanup must remain authorized follow-up work.

### V-06 — Native-check duties survive metrics and evidence reuse

**Situation:** A disposable repository declares real existing static commands,
governed scope, policy, requiredness and stage owner. Supply current or deliberately
stale execution evidence with checked-byte identity, result and producer/stage.
Keep unrelated prerequisites valid. A local invocation record can establish
whether a command ran and which scope it checked.

**Action and expected result:** Review applicable native evidence beside metrics.

| Case | Native / measurement state | Exact expected result |
|---|---|---|
| V-06a | New/worsened required hard architecture violation; comparison completes successfully | `CHANGES_REQUESTED` for the applicable hard violation, with concrete gate evidence. Metric success/exit 0 does not waive it. |
| V-06b | Required native correctness check fails; metrics complete, then separately metrics N/A | Retain the failure, native policy, scope, owner and correction duty in both variants. Do not relabel it advisory or certify clean completion from metrics; leave functional investigation with its existing owner. |
| V-06c | Required proof missing; owner can supply it | Recover through the declared owner or an authorized focused run. Keep proof owed until current evidence exists. Do not broaden into general functional review. |
| V-06d | Saved pass has stale checked bytes; an authorized focused run is available | Detect staleness and recover proof on current governed bytes. Preserve historical evidence and record the new result/producer. Matching short status alone cannot validate it. |
| V-06e | Required gate unavailable; no valid current evidence or documented exception | Record exact command, gap, owner/recovery and incomplete review, normally `INCONCLUSIVE`. Static inspection or passing metrics cannot substitute for required evidence. |
| V-06f | Current aggregate establishes included commands, whole-project scope, policy and checked bytes | Reuse covered constituents without rerunning them merely for report sections. Preserve architecture run/validation authority and the reviewer's separate fresh metric comparison. |
| V-06g | Aggregate omits a required constituent, narrows whole-project scope, lacks policy coverage or has stale bytes, varied separately | Do not claim covered proof. Recover the affected native obligation under its owner and governed scope. A changed-file metric scope never narrows a whole-project gate. |
| V-06h | Commands documented without a registry; separately no native commands exist | Retain documented commands and owners without requiring a registry. In the absent-command variant record none; invent no lint/typecheck/architecture command. |
| V-06i | Policy sources conflict on requiredness or hard/advisory semantics | Route the specific conflict to its authority owner. Do not create an exception, weaken a hard rule or infer policy from tool name/exit code. |
| V-06j | Optional run-evidence wrapper captures a real comparison; separately wrapper unavailable | Do not rerun comparison solely to obtain instrumentation. Wrapper availability supplies neither missing measurement nor native proof, and its absence alone adds no measurement/native duty. |

**Why test this:** Shared tools and aggregate checks can otherwise hide hard
failures, omit whole-project coverage or cause duplicate execution.

**How to check:** Exercise the declared native command, including actual pass/fail
and recovery states. Inspect raw result and invocation records, coverage and byte
identities. Reuse mixed hard/advisory measurement coverage and the unavailable-gate
fixture. A forged "PASS" field is not proof of native execution. Seeded aggregate
records represent upstream check-owner output; actual command coverage must be
established before claiming reuse. This is not authority to rerun discovery's
aggregate or to duplicate functional review.

### V-07 — Complete reports cannot be truncated by optional warnings

**Situation:** Prepare at least four required breach rationale obligations, one
explicit evidence gap with owner, and four distinct confirmed blockers from the
existing multi-finding fixture. Include more than three optional warning candidates.
Each obligation has a stable identity in the expected coverage ledger.

**Action and expected result:** Write the next numbered maintainability report.

| Case | Review progress | Exact expected result |
|---|---|---|
| V-07a | Full bounded scope is available; an early blocker already decides the verdict | Continue bounded coverage. Retain every blocker with stable ID and every required rationale disposition/gap outside `WARNINGS`. Cap only optional warnings at three. No finding count cap or quota. |
| V-07b | Genuine permission/capability/budget stop prevents completing coverage | Retain confirmed findings, dispositions reached, all outstanding obligations/coverage, concrete stop reason and next owners. Report incomplete review; neither an early blocker nor successful metrics can imply complete or accepted coverage. |
| V-07c | All proof current, no semantic/hard blocker, justified retained breaches | `ACCEPT` is permitted with explicit rationale agreements. Measurement completion, semantic verdict and functional acceptance remain distinct. |

**Why test this:** A compact report can silently lose obligations even when its
verdict happens to be correct.

**How to check:** Grade the report against the complete input ledger. Require
measurement status; exact B and reviewer-current JSON/text references; scope/byte
identities; all rationale dispositions; native command/scope/policy/requiredness,
checked bytes/result/producer/stage; owed proof/owners; and blocker IDs/evidence.
Compare these fields with actual inputs, not only headings. Preserve existing
four-blocker and genuine-stop oracles. V-07c prevents an always-incomplete report
from passing. A maintainability `ACCEPT` certifies only its reviewed bytes/scope.

### V-08 — Corrections keep the original baseline and current finding history

**Situation:** Use the existing correction-round or tests-only correction fixture.
Stage prior reports/ledgers as labeled history, then perform two real authorized
edit occurrences. B predates both; I1/R1 describe the first submission.

**Action and expected checkpoints:**

1. **V-08a — First submission:** Compare actual first-edited code with B and obtain
   reviewer comparison R1 plus a numbered report. Save identities of B, I1/R1 and
   the reviewed assets. A seeded historical verdict alone proves no actor run.
2. **V-08b — Affected correction:** Correct one finding in the same responsibility.
   I1/R1 and the affected verdict/native proof become stale for those bytes.
   Produce new implementer/reviewer comparisons I2/R2 against B, never I1/R1.
   Update affected rationale/native evidence. Original and historical report pairs
   remain byte-identical, while current source/report identities reflect edit two.
3. **V-08c — Reconcile findings:** The fresh next numbered report preserves surviving
   IDs and records corrected IDs with current evidence. A new finding gets an unused
   ID; no resolved ID is recycled or omitted by display reordering. Carry every
   coverage row and its current status, including gaps, across correction.
4. **V-08d — Unaffected scope control:** For a separate change outside demonstrably
   unchanged reviewed scope, retain only evidence whose scope/bytes/policy still
   apply. Do not force unrelated stage re-entry or reuse stale affected proof.

**Why test this:** Comparing correction two with correction one hides accumulated
growth. Replacing histories or IDs loses evidence and correction ownership.

**How to check:** Execute both edits and real comparisons in disposable storage.
Check reports against actual source snapshots and B's immutable identity, not
only different filenames. Reuse `correction-round` and `test-assets-correction`
stable-ID oracles. Grade review actions only when separately executed. T-004
checks this review boundary; the full installed producer-to-consumer journey
remains T-005's responsibility.

### V-09 — Scope expansion cannot invent pre-edit evidence

**Situation:** A correction needs Python code outside B's governed folders.
All original evidence is preserved. Scope resolution belongs to the authorized
task owner, not the read-only reviewer.

**Action and expected result:** Handle each independent expansion state.

| Case | Expanded-scope state | Exact expected result |
|---|---|---|
| V-09a | Expansion not yet authorized | Name the scope decision and owner. Do not edit or claim the new code covered. Preserve original evidence and owed review route. |
| V-09b | Authorized expansion; exact preserved pre-edit bytes are verifiable | Use that exact evidence for compatible supplemental coverage, retain B/history and explicitly identify the expansion. Obtain fresh applicable comparison/review rather than treating old coverage as complete. |
| V-09c | Authorized expansion; exact pre-edit evidence unavailable | Attempt current measurement and record an unrecoverable before-state gap with owner/recovery limits. No edited-tree baseline or fabricated delta. Apply explicit indispensable-evidence authority as in V-02e/f. |

**Why test this:** A legitimate correction must not silently redefine the task's
starting state or the reviewer's write authority.

**How to check:** Use actual out-of-coverage paths and preserved-source variants.
Observe CLI scope refusal/current measurement, report references and source/index
preservation. An authorization note does not itself supply missing before bytes.

### V-10 — Downstream consumers retain the conditional ordered route

**Situation:** Supply current numbered maintainability evidence, submission route,
reviewed scope identities and any current registry/discovery records. The
coordinator owns stage execution. Use existing downstream fixtures only for the
new evidence-consumption boundary; preserve their independent functional probes.

**Action and expected result:** Name the outstanding route, then prepare separate
consumer inputs for discovery and acceptance.

| Case | Current obligations | Exact expected result |
|---|---|---|
| V-10a | Maintainability accepted; registry stage applies and changed durable contracts require sync | First outstanding stage is registry synchronization, then fresh discovery, then separate acceptance. Reviewer names all three and executes/delegates none. |
| V-10b | No registry stage exists; separately registry evidence is already current | First outstanding stage is fresh discovery, then separate acceptance. Do not invent or repeat registry work. |
| V-10c | Maintainability, applicable registry and discovery already current | Name only separate acceptance as the outstanding stage. Downstream consumes maintainability evidence without repeating general maintainability review. |
| V-10d | Functional correction changes significantly reviewed test/eval/harness responsibilities | Re-enter affected required architecture/maintainability duties; include registry sync only if its existing scope is affected; then fresh discovery and separate acceptance. Tests-only labeling waives no affected duty. |
| V-10e | Ordinary assertion correction fits an explicit trivial-change exception, or earlier reviewed scope is demonstrably unaffected | Apply only the authorized exception/unaffected-scope retention; preserve all remaining duties in order. Measurement warnings alone create no new required review stage. |
| V-10f | Maintainability report is stale, incomplete or has an unresolved applicable blocker | Consumer keeps the precise gap/finding and returns it to the owning stage. A prior `ACCEPT` label or passing metrics cannot close it. Do not repeat general review or execute correction as the consumer. |

**Why test this:** Evidence integration can otherwise add stages, skip owed work
or merge independent discovery with acceptance.

**How to check:** Inspect minimal downstream/README guidance changes and prepare
consumer fixtures with explicit stage applicability and current/stale identities.
Grade first outstanding stage plus complete ordered remainder. Preserve separate
evidence, correction and decision owners and the full coverage ledger. Existing
discovery owns targeted probes and its justified aggregate after clean targeted
evidence; a decisive targeted failure keeps that aggregate suppressed. Acceptance
consumes that record without rerunning it. Native aggregate reuse in V-06 cannot
override those stage duties. Prepared consumer cases are not full T-005 closure.

### V-11 — Eval preparation and distribution preserve existing boundaries

**Situation:** The changed source packages are ready for local verification.
Existing coverage/setup was inspected before extension. Installation targets are
disposable and include unrelated user files, settings, environments and reports.

**Action and expected result:** Verify preparation and managed projection.

| Case | Check | Exact expected result |
|---|---|---|
| V-11a | Reconcile V-01–V-10 with eval definitions/setup and retained existing scenarios | Every required child case has actual inputs, tool/report permissions and a decisive oracle. Preserve independence, path, multi-finding, genuine-stop, semantic/test-asset controls and correction variants. Extend/reuse existing owners rather than copy harness infrastructure. |
| V-11b | Run changed fixture checks and relevant measurement coverage | Checks establish the intended states and exercise each claimed CLI/native outcome. Reject controlled stale identity, missing disposition and wrong-route results at the intended oracle, not via unrelated harness failure. Record skips, failures and limits. Syntax/schema/keyword checks alone cannot prove success. |
| V-11c | Inspect installer/profile/shared-file declarations, focused installer coverage and README installation guidance; project changed packages into a disposable target | All changed managed package resources project correctly and relevant installed fixture entry points remain usable without source/global fallback. Synchronize only stale declarations/docs. Preserve narrow installer ownership and all unrelated target bytes. No inherently new profile member/runtime dependency and no active-install refresh. |

**Why test this:** Plausible eval metadata can lack decisive inputs, and valid
source preparation can fail when installed resources are missing.

**How to check:** Trace each case to runnable setup or explicitly prepared actor
inputs and a held-back oracle. Reuse focused installer projection/preservation
coverage and installed fixture execution. Local checks prove preparation/tool
behavior only; preserve raw outputs and label unrun actor behavior unqualified.
Implementer runs changed fixture checks first, owning measurement coverage next,
then installer coverage when affected. Run canonical architecture and contract
checks before implementation handoff; cross-cutting implementation also uses
`python3 tools/verify.py` after focused checks pass. Live/expensive checks require
their applicable approval. Fresh discovery owns its separate targeted evidence
and aggregate record; acceptance consumes it. Report active-profile drift without
refreshing this session's installation.

## Coverage summary

The brief supplies no separate risk-row IDs. Plan V-004–V-008 below identify
system obligations; local V case IDs identify this task's derived cases.

| Promise from the brief | AC / plan obligation | Required cases |
|---|---|---|
| [Independent comparison of current submitted bytes; preserved provenance and writes](brief.md#work-and-acceptance-criteria) | AC-01; V-006 | V-01a–e, V-02a–i, V-09a–c |
| [Proportionate retained-breach rationale and semantic attribution](brief.md#work-and-acceptance-criteria) | AC-02; V-005 | V-03a–j, V-04a–d, V-05a–e |
| [Current native policy, scope, owner and evidence without duplicate execution](brief.md#work-and-acceptance-criteria) | AC-03; V-008 | V-06a–j, V-10f |
| [Complete numbered review outside the optional warning cap](brief.md#work-and-acceptance-criteria) | AC-04; V-005/V-006/V-008 | V-02e–i, V-03c–j, V-06a–g, V-07a–c, V-08c |
| [Original-baseline corrections and stable identities](brief.md#work-and-acceptance-criteria) | AC-05; V-004 | V-08a–d, V-09a–c |
| [Conditional ordered downstream consumption with separate owners](brief.md#work-and-acceptance-criteria) | AC-05; V-007 | V-10a–f |
| [Decisive executable eval preparation with honest proof limits](brief.md#work-and-acceptance-criteria) | AC-06; V-004–V-008 | V-01a–e, V-02a–i, V-03a–j, V-04a–d, V-05a–e, V-06a–j, V-07a–c, V-08a–d, V-09a–c, V-10a–f, V-11a–b |
| [Managed distribution and preserved installer ownership](brief.md#authority-and-scope) | Scope obligation; AC-06 preparation support | V-11c |

## Source and revision

Source brief: docs/tasks/T-004/brief.md
Source brief revision: 1; SHA-256 `d45b174d7e3a671c1cdc2d0313e7a008683c8a1757446112e6f7a12dd693ac9d`
Verification revision: 1
Authority: derived from the task brief and its cited normative sources, especially project-plan sections 1–7, FLOW-002/FLOW-003 and V-004–V-008
Status: ready
