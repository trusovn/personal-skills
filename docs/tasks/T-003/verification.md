# Verification Design: T-003 — Give implementers proportionate feedback

Check that both implementation entry paths preserve the actual starting code,
compare the final affected scope, and submit proportionate design reasoning with
current native-check evidence. Corrections must retain the original baseline.
Advisory metrics must not weaken required checks or expand review duties.

T-003 delivers source guidance and executable eval preparation. The cases below
define the behavior those evals must be able to distinguish. Preparing a case,
checking its inputs, or running the measurement CLI does not prove that an agent
followed the guidance. T-005 owns the complete installed journey.

## Shared setup and evidence responsibilities

- Use disposable Git repositories and the existing implementer entry/correction
  fixture setup. Preserve distinct existing evals 1–9 and the `entry-cases`,
  `route-cases`, and `review-cases` variants. Reuse the measurement and installer
  fixtures for runtime facts; add only missing T-003 evidence.
- Supply the bounded request or executable package, applicable ready preflight,
  verification, native-check policy, and correction ledger needed by each case.
  High-assurance cases also need the existing schema, result path, exact packet
  baseline and authorized runtime paths. Direct cases have no task package.
- Supply an installation-local format-5 measurement runtime and an already
  prepared pinned interpreter for cases claiming actual measurement. Permit
  writes to fresh JSON/text paths under target `.quality/reports/` as well as
  the bounded code paths. Do not refresh the active installation or provision
  dependencies implicitly. Preflight confirms capability and permissions.
- Snapshot source bytes, the real Git index, existing report pairs and unrelated
  user files before actions. Intentional task edits are permitted; capture and
  comparison must not themselves change source or the real index. Seeded reports
  represent tool/preflight output, and seeded ledgers represent prior review.
  Label them. Only an actual CLI run proves report generation or compatibility.
- For V-01–V-10, implementation evidence consists of a source-guidance trace,
  executable case inputs and a decisive oracle. Run focused fixture checks that
  verify the starting state and exercise any claimed tool boundary. For policy
  decisions, prepare grading against actual final artifacts, diff, report facts,
  command history and retained obligations. Keyword checks alone are insufficient.
- Fresh independent discovery corroborates the preparation, guidance, tool facts
  and coverage for V-01–V-11; separate acceptance decides T-003 advancement.
  Implementation checks cannot supply either independent role. Live execution
  and independent grading of agent decisions are not required by this task and
  remain unqualified unless separately authorized. No T-004 reviewer protocol or
  T-005 full composition result is required here.

## Test cases

### V-01 — Packaged entry validates starting evidence before editing

**Situation:** A dependency-ready executable leaf has its bound verification and
ready preflight. Supply a valid original report pair and native inventory from
the [T-002 handoff](../../../skills/task-implementation-flow/task-preflight/references/execution-packet-template.md#starting-evidence-and-native-obligations-both-profiles).
Keep every prerequisite valid except the named variant.

**Action and expected result:** Attempt implementation entry.

| Case | Starting state | Exact expected result |
|---|---|---|
| V-01a | Guided package; project, inventory, hashes, tools/settings/checks and governed folders match | Validate the supplied capture before the first code edit; consume it without replacement capture or broad readiness discovery. Remain guided. |
| V-01b | High-assurance package; all exact freshness and packet-only delta checks match | Validate capture applicability and the existing exact packet contract before editing. Preserve schema/result obligations. Measurement reports are part of the recorded pre-packet state. |
| V-01c | Different logical project despite compatible relative paths | Stop implementation entry and route focused preflight reconsideration; no code edit or silent new baseline. |
| V-01d | Captured file bytes change while short-status text stays the same | Detect the source-hash mismatch before editing; route focused preflight, without resetting user work. |
| V-01e | A relevant included file is added or removed after capture | Detect the changed inventory; route focused preflight, without accepting the old inventory as current. |
| V-01f | Change one effective tool, settings or selected-check identity at a time | Detect each material identity mismatch; route focused preflight, without a replacement capture. |
| V-01g | Planned Python edit falls outside governed folder coverage | Resolve scope/readiness before editing that scope; do not claim it is covered. |
| V-01h | High-assurance index blob changes but worktree hash and status text match | Preserve the existing exact freshness refusal and schema-valid non-complete result; no implementation edit. |

**Why test this:** A plausible report path or unchanged Git status cannot prove
that implementation starts from the recorded code.

**How to check:** Inspect entry guidance and prepare paired valid/refusal cases.
Observe command/edit order and original-report references; independently compare
inventory and hashes. V-01h reuses the existing restaged-stale eval. Existing
package refusal cases still apply; new measurement checks do not replace them.
CLI compatibility tests corroborate runtime checks, not agent entry decisions.

### V-02 — Direct self-preflight captures actual authorized code

**Situation:** A conversational request authorizes bounded Python edits. Relevant
production, test, eval, fixture and harness folders are known. Include staged
content, different unstaged content in the same file, and an untracked Python
file. Separately provide an existing empty parent for a new Python area.

**Action and expected result:** Perform self-preflight, then implement and compare.

| Case | Starting state / action | Exact expected result |
|---|---|---|
| V-02a | Capture the dirty/staged/untracked scope before the first edit | Capture actual worktree bytes, including the untracked file; preserve the staged index bytes and user work. Include all relevant asset groups under existing exclusions. Use fresh report paths and the installation-local runtime. Create no task package or formal identity solely for measurement. |
| V-02b | Capture the selected existing empty parent, then add its first Python file | Baseline records valid empty inventory. Comparison treats the added file as absent before capture, not as having numeric zero metrics. |
| V-02c | Measurement runtime or pinned tools unavailable; no indispensable-evidence requirement | Record unavailable evidence and owner/recovery; continue otherwise authorized work. Do not install tools, switch installations or invent a baseline. |
| V-02d | Same unavailable capability with explicit indispensable starting-evidence authority | Stop before editing; name the authority, capability owner and recovery action. No clean comparison claim. |

**Why test this:** Direct work must not evade starting evidence or acquire new
packaging and provisioning requirements.

**How to check:** Reuse dirty-index and empty-folder CLI coverage with actual
capture/edit/compare actions. Assert saved source bytes and index preservation,
not only exit status. Prepared agent cases additionally grade action order and
absence of invented formal artifacts. V-02a is the success control for V-02c/d.

### V-03 — Final evidence follows affected files and responsibilities

**Situation:** Use one captured folder inventory with known functions and native
counts. Provide bounded edits and a hand-auditable before/after diff. Keep an
over-target sibling in the same file, with unchanged behavior and structure.

**Action and expected result:** Compare the final task scope and prepare submission.

| Case | Final change | Exact expected result |
|---|---|---|
| V-03a | Change a function, add a file, delete a captured file; include relevant test/harness changes | Final comparison names changed, added and deleted Python paths within coverage. Submission references exact original JSON/text and current JSON/text paths, scope and measurement status. Required asset groups are not omitted. |
| V-03b | Edit one function; shift or format the untouched hotspot sibling | Only the actually changed responsibility is affected. The sibling remains context, without mandatory cleanup or rationale merely from file membership, line movement or formatting. |
| V-03c | Rename or move a function, or extract part into helpers | Explain each actual relationship from diff/context. Assess the original responsibility with its helpers. Leave unmatched numeric before/after values unknown; invent no delta or attribution analyzer. |
| V-03d | Native diagnostic/count absent on one side, such as an exempt override method | Missing value stays unknown, even if another metric is complete. Do not infer zero or numeric improvement from diagnostic disappearance. |
| V-03e | Docs-only task; separately an unsupported-language task | Record measurement N/A with its reason; native-check duties still apply. |

**Why test this:** File-wide attribution and guessed deltas can create false
cleanup demands or false evidence of improvement.

**How to check:** Reuse added/deleted, symbol-interpretation and native-exemption
runtime tests. Prepare diff-based grading for attribution and submission facts.
For V-03c, use visible rename, move and extraction examples; they share the
unknown-delta oracle but each relationship must be identifiable. Tool output
alone cannot decide affected responsibilities.

### V-04 — Rationale follows retained breaches, including equality boundaries

**Situation:** Effective advisory targets are complexity 10, statements 50 and
arguments 5. Use reports with known numeric values and code/diffs that establish
whether a function is materially edited. Do not seed invented native counts.

**Action and expected result:** Apply
[plan section 5](../../project-plan.md#5-lifecycle-and-decision-rules) to submission.
In V-04a–g, use complexity values below; also cover the corresponding boundary
for statements (49/50/51) and arguments (4/5/6) where native counts exist. Shared
metrics can use one rationale when the design reason is the same.

| Case | Affected function / values | Exact expected result |
|---|---|---|
| V-04a | Complexity 6 → 8 | Information only. No per-increase rationale or metric-driven refactor is required. |
| V-04b | Complexity 9 → 10 | Equality is within target. No breach rationale or metric-driven refactor is required. |
| V-04c | New function has complexity 11 | Explain retained structure and useful local alternatives. Exceeding the target alone does not reject the submission. |
| V-04d | Existing function 10 → 11 | Explain the newly crossed breach; the target is advisory. |
| V-04e | Existing hotspot 11 → 12 | Explicitly assess and justify worsening the breach. |
| V-04f | Materially edited hotspot 11 → 11 | Consider useful local cleanup and briefly explain retention. No obligation to reach 10. |
| V-04g | Materially edited hotspot 12 → 11 | Explain retained over-target structure despite improvement; no obligation to reach 10. |
| V-04h | Materially edited hotspot 11 → 10 | No retained breach remains. No breach rationale is required solely because the starting value exceeded target. Semantic duties still apply. |
| V-04i | Untouched hotspot remains 11 while its sibling changes | Context only; no required rationale or cleanup for the untouched function. |
| V-04j | Metric falls after extraction, but ownership, names or navigation worsen | Address the concrete semantic cost; smaller numbers do not excuse it. Assess helpers together. Do not accept splitting cohesive code, opaque argument containers or tuned exclusions as proof of better design. |
| V-04k | Required breach rationale is missing | Recover the explanation before claiming the submission complete. Each rationale identifies report, function, metric, known before/after, why decisions belong together and the cost of a plausible alternative. |

**Why test this:** Defending every increase wastes effort; ignoring edited legacy
hotspots or rewarding misleading extraction misses material design decisions.

**How to check:** Existing analyzer boundary tests prove reported numbers and
labels. Prepared agent cases grade actual retained code, diff, affected-function
attribution and rationale against every named row. A cohesive retained breach
with a complete explanation is a positive control against automatic threshold
rejection. Missing rationale is a recoverable submission obligation, not proof
of bad design. Independent reviewer acceptance/disposition belongs to T-004.
Wider useful cleanup is follow-up work, not silently expanded implementation.

### V-05 — Evidence gaps remain explicit and recover only what is possible

**Situation:** Otherwise valid bounded work encounters one of the following
measurement states. Distinguish a material entry mismatch in V-01 from evidence
discovered missing or unusable after authorized work has started.

**Action and expected result:** Recover feasible current measurement and report
the remaining gap. Apply each row under advisory policy and, separately, explicit
authority making the affected evidence indispensable.

| Case | Evidence condition | Exact expected result |
|---|---|---|
| V-05a | Original report pair missing after edits; current tools usable | Measure current code at fresh paths, disclose missing before evidence and avoid a clean or complete comparison claim. Never recapture edited code as original. |
| V-05b | Partial report, including missing native numeric evidence | Retain available facts and per-check limits. Attempt recoverable current measurement; unknown values remain unknown and partial evidence is not complete coverage. |
| V-05c | Current report is stale after a further code edit | Produce a new comparison for current bytes against the original baseline if possible. Keep the stale report as history, not current proof. |
| V-05d | Original format, tool or settings identity is incompatible | Disclose incompatibility. Use verified exact preserved pre-edit bytes for compatible remeasurement only if available; otherwise measure current code and retain the before-state gap. |
| V-05e | An edited path is outside captured coverage | Do not report it as compared. Apply the authorized added-scope recovery in V-07; disclose any unrecoverable before-state gap. |
| V-05f | Launcher/analyzers unavailable at submission | Report unavailable measurement, the actual attempted action or established capability failure, and owner/recovery. No implicit provisioning or fabricated report. |

For every row, advisory absence alone is not a new blocker. If explicit authority
makes the missing evidence indispensable, stop advancement and name that
authority, the recovery owner and useful next action. Never waive another required
check. Neither outcome claims complete comparison. V-03a supplies the full-evidence
success control.

**Why test this:** A generic “metrics unavailable” statement can hide recoverable
current evidence or silently waive required before-state proof.

**How to check:** Inspect fixture reports and capability faults independently.
Exercise real runtime error/recovery cases where tool behavior is claimed.
Prepare artifact grading for each A/R policy variant, current-attempt evidence,
preserved originals and remaining obligations. Seeded failures establish inputs;
they do not prove that an agent attempted recovery.

### V-06 — A correction compares current bytes to the same original baseline

**Situation:** A valid packaged or direct task has original pair B and initial
comparison C1. Seed a prior review ledger with passed, failed, blocked and
unchecked rows, stable finding/scenario IDs and separate owners. The prior review
requests a bounded correction; its final aggregate decision belongs to the fresh
reviewer. Reuse the existing correction fixture and report-write authority.

**Action and expected checkpoints:**

1. Before correction edits, map every supplied ledger row exactly once to planned
   implementation evidence or fresh-review coverage. Prior passes are navigation,
   not current corrected-byte proof. Preserve the failed reviewer regression.
2. Make the bounded correction. Changed bytes stale affected comparison, native
   evidence and verdicts. Keep unaffected evidence only when still applicable.
3. Run the reviewer regression first, then the nearest owning suite. Leave the
   reviewer-owned aggregate decision with its owner; report implementation checks
   separately.
4. Create C2 at new JSON/text paths, comparing corrected bytes to B, not C1.
   Update applicable rationale. B and C1 remain byte-for-byte unchanged.
5. Submit every ledger row, stable ID, incomplete reason and owner. Keep blocked
   and unchecked coverage visible. Name the first outstanding conditional stage
   and full remaining route to fresh discovery and separate acceptance. Do not
   mark reviewer rows passed or emit an independent verdict.
6. For a subsequent task, capture that task's actual starting code. Do not reuse
   B as a permanent allowance for high values.

**Why test this:** Replacing the baseline or retaining a stale verdict can erase
growth and let a partial correction advance as fully reviewed.

**How to check:** Prepare the repeated-edit eval with actual changes and distinct
report identities. Existing CLI comparison/preservation evidence corroborates
the tool boundary; grade the correction artifact and action order separately.
The ledger is seeded prior-review context, not a newly performed independent
review. T-005 owns the complete installed producer-to-reviewer sequence.

### V-07 — Scope recovery and report transfer preserve historical evidence

**Situation:** Start from a valid task baseline and otherwise usable tools.

**Action and expected result:** Exercise each separate boundary.

| Case | Boundary / action | Exact expected result |
|---|---|---|
| V-07a | Unexpected new scope; authorization resolved and exact preserved pre-edit bytes exist | Resolve authorized scope before editing it. Add coverage from verified pre-edit evidence without replacing the original covered baseline or relabeling current edits as starting code. Record original and supplemental references. |
| V-07b | Unexpected scope was edited and no exact pre-edit evidence exists | Disclose an unrecoverable before-state gap; attempt current measurement. Do not invent a clean comparison. Required-evidence policy determines whether advancement must stop, as in V-05. |
| V-07c | Requested JSON output or its sibling text path already exists | Preserve both existing files. Choose fresh output paths rather than delete or replace reports. |
| V-07d | Submit to an isolated clone that lacks ignored reports | Name exact JSON/text source files and receiving paths needed by the consumer. Supply transfer instructions; a commit is not report transfer. With transferred files, retain the same logical project and compatibility checks despite absolute-root changes. |

**Why test this:** Scope expansion, output reuse and clone boundaries can destroy
or strand the only before evidence.

**How to check:** Use real filesystem report-collision and relocated-report
coverage. Prepare artifact grading for authorization, preserved-byte provenance,
gap handling and complete transfer references. A deterministic copy/compare can
prove file usability; it does not prove an agent selected the correct reports.

### V-08 — Native-check scope, policy and execution evidence survive metrics

**Situation:** Supply existing native command policy with command, governed scope,
requiredness and declared owner/stage. Use a real disposable native static command
for failure/reuse claims. A whole-project obligation must include code outside
the metric changed-file subset. ART-008 records command, scope/policy, checked-byte
identity, result and producer/stage beside the metrics reference.

**Action and expected result:** Consume the packaged inventory, or discover the
same fields during direct self-preflight; execute or reuse evidence under its
existing ownership.

| Case | Policy or evidence state | Exact expected result |
|---|---|---|
| V-08a | Registry supplies required native commands | Preserve all inventory fields and execute applicable implementer-owned obligations at their governed scope. A changed-file metric comparison does not narrow a whole-project check. |
| V-08b | No registry; native command is documented | Discover and retain the documented command/policy/owner. Do not require a registry or invent a replacement command. |
| V-08c | No native check exists | Record none discovered. Do not invent lint/typecheck commands. |
| V-08d | Current aggregate establishes constituent command coverage, scope, policy and checked bytes | Reuse it with explicit ART-008 references. Do not run constituents again solely to fill a report section. |
| V-08e | Aggregate omits the constituent command or required scope | Do not claim constituent coverage. Recover missing required evidence through its real owner or an authorized focused execution. |
| V-08f | Checked bytes or governed policy changed | Reject stale evidence reuse; recover affected required proof through its owner. Retain unchanged applicable proof without blanket reruns. |
| V-08g | Required proof missing or command unavailable | Carry the unresolved duty and recovery owner. An entry prerequisite prevents editing; a later-stage duty remains due at that stage. Do not claim completion of a required implementer check. |
| V-08h | Native hard failure while advisory comparison completes successfully | Preserve the native failure and its policy consequence. Measurement success cannot authorize advancement past that failure. |
| V-08i | Native hard failure while measurement is N/A | Preserve the same native failure policy and owner; N/A metrics do not waive it. |
| V-08j | Correct the native failure and rerun its required check on current bytes | Record current successful native evidence with new byte identity; retain historical failure. Success can satisfy that duty without converting advisory metrics into a design verdict. |

**Why test this:** Successful metrics can conceal a hard failure, and duplicate
aggregate/constituent execution can add cost without adding proof.

**How to check:** Reuse real F401-plus-advisory coverage and aggregate/native
fixtures. Observe actual scope, command results and invocation counts for reuse
claims. Grade policy/owner retention and honest evidence status separately.
Supply successful controls before the deliberate fault and after correction, so
unavailable setup cannot pass as the intended hard failure. Preserve command
semantics even when advisory counts and hard findings use the same executable.

### V-09 — Optional run evidence remains separate from measurement

**Situation:** Use the existing optional evidence availability and lifecycle
contract, with an otherwise executable task and usable measurement runtime.

**Action and expected result:** Attempt normal instrumentation and measurement.

| Case | Instrumentation state | Exact expected result |
|---|---|---|
| V-09a | Installation-local evidence helper is available | Preserve the existing single invocation lifecycle. Wrapping the actual comparison is permitted; do not run it twice for capture or create a new lifecycle. |
| V-09b | Helper unavailable or first best-effort operation fails | Skip instrumentation for the remainder of this invocation without repeated probes. Continue otherwise authorized measurement/work; report instrumentation unavailable separately from measurement status. |
| V-09c | Explicit contract requires instrumentation; helper unavailable/fails | Retain the strict blocking/non-complete outcome. Do not downgrade to best-effort because metrics work. |
| V-09d | Instrumentation available but measurement unavailable | Report those two facts separately. An evidence-run record is not a successful comparison. |

**Why test this:** Optional capture must neither become an unsolicited blocker
nor provide false measurement success.

**How to check:** Reuse existing runtime-evidence availability coverage and
prepare implementer cases that inspect actual lifecycle/command history and final
claims. Instrumentation supplies execution facts, not model provenance or an
independent review. No new evidence store or duplicate invocation is required.

### V-10 — Measurement does not alter existing entry and review routes

**Situation:** Retain existing package-entry, provenance, significant test/harness,
trivial tests-only and correction-route fixtures. Supply their current conditional
stage policy and evidence. Include one task for which no independent review is
required and only advisory measurement warnings are present.

**Action and expected result:** Apply updated source guidance to those inputs.

| Case | Existing route condition | Exact expected result |
|---|---|---|
| V-10a | Legacy direct brief, relabeled package, missing/blocked/stale readiness, foreign verification or non-executable parent | Preserve each existing refusal and its earlier owner. Do not bypass preparation to capture measurements. |
| V-10b | Immediate review or otherwise explicitly required independent review | Guided submission stops at READY_FOR_REVIEW; machine contract retains its schema-defined submission status. Name only outstanding applicable conditional stages, then fresh discovery and separate acceptance. Do not perform or claim independent review in the implementer invocation. |
| V-10c | Review remains optional; advisory warnings only | Preserve the existing milestone/no-review result and conditional policy. Warnings alone create no new required review stage. |
| V-10d | Significant test/eval/fixture/harness change; separately a trivial tests-only change | Preserve the respective existing maintainability/registry applicability and stage order. Include affected Python assets in measurement without promoting every tests-only change into a mandatory review. |
| V-10e | Interrupted or two-strike stopped task | Preserve non-complete status, actual attempts, unfinished scenario rows and next owners. Do not claim a final comparison or completed review that did not occur. |

**Why test this:** Adding evidence fields must not weaken existing freshness and
provenance controls or broaden review applicability.

**How to check:** Preserve distinct existing eval oracles and route-case outputs;
trace additions against those oracles. Grade emitted artifacts and retained
obligations when agents are run. T-003 verifies its implementer handoff; changes
to reviewer decision protocols remain outside this task.

### V-11 — Current guidance, eval preparation and installation stay aligned

**Situation:** The changed source implementer entry, inline submission/correction
formats, flow README and advisory entry points are ready for review.

**Action and expected result:** Inspect policy references and prepare/run local
fixture checks before handoff.

| Case | Inspection or check | Exact expected result |
|---|---|---|
| V-11a | Follow current guidance and links, including superseded proposals | Current instructions lead to plan section 5 and retain targets 10/50/5. Conflicting every-increase defense/new-stage policy is clearly superseded. Historical experiment evidence remains unchanged. Naming, ownership, test/harness and abstraction duties remain intact. |
| V-11b | Reconcile eval definitions and generated inputs with V-01–V-10 | Every material row has supplied inputs, usable tools or an intentional capability fault, authorized report writes and a decisive oracle. Both entry paths, threshold decisions, correction continuity, missing evidence and native failure/reuse are reachable. Distinct original eval scenarios survive. |
| V-11c | Inspect installer membership, profile guide, shared-file list, focused tests and README installation instructions | Synchronize only entries made stale by this task. Preserve narrow managed ownership and installation-local dependencies. Use disposable installs for changed projection evidence; do not refresh this active invocation. |
| V-11d | Reconcile implementation evidence and contract changes | Register only implemented current contracts at the designated registry-updater stage. Report actual checks, skips, failures and profile drift. Do not label fixture setup, syntax checks or scripted tool runs as agent qualification. |

**Why test this:** Correct local wording can still leave conflicting public
instructions, unusable evals or stale distribution guidance.

**How to check:** Fresh discovery independently traces policy and case coverage,
inspects generated starting states and reviews the actual changed artifacts.
Run setup at disposable roots; assert required files, permissions and oracle
preconditions instead of treating setup exit 0 as behavioral proof. Reuse existing
installer projection/preservation tests if that boundary changes. Structural and
documentation evidence applies to V-11 itself; it cannot substitute for the
behavioral claims in V-01–V-10.

## Verification order and gate ownership

For T-003 implementation, run changed fixture/targeted checks first. Then use the
owning measurement suite, with its already prepared pinned interpreter where
available:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_maintainability.py
```

Run focused installer coverage when installation/projection is affected:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py
```

Before handoff, implementation owns these repository checks:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py
python3 tools/check_contracts.py --root .
```

For a cross-cutting implementation, implementation also owns
`python3 tools/verify.py` after focused checks pass. Record its actual result,
skips and active-profile drift. No passing aggregate result is inferred from
focused checks. Native analyzer skips leave that measurement boundary unproved.
Preflight resolves exact executable paths, feasibility and any approval needed;
it does not execute all native duties as a new starting baseline.

These implementation gates are separate from fresh discovery and acceptance.
V-06 preserves the seeded correction task's reviewer-owned aggregate decision;
it does not transfer T-003's implementation gate ownership to a reviewer.
Live agent eval execution needs separate runtime/budget approval. Prepared but
unrun cases remain unqualified for agent behavior. T-004 owns reviewer decisions;
T-005 owns the full installed composition proof.

## Coverage summary

No risk rows are supplied by the brief. Plan verification IDs below identify
T-003's contribution only; they are distinct from this artifact's case IDs.

| Promise from the brief | AC / plan verification | Required cases |
|---|---|---|
| [Validate packaged starting evidence and preserve profile freshness](brief.md#work-and-acceptance-criteria) | AC-01; V-003 | V-01a–h; V-10a |
| [Capture actual authorized direct-entry bytes before editing](brief.md#work-and-acceptance-criteria) | AC-01; V-003 | V-02a–d |
| [Compare final paths and actual affected responsibilities honestly](brief.md#work-and-acceptance-criteria) | AC-02; V-003/V-005 | V-03a–e |
| [Keep incomplete evidence explicit and attempt feasible recovery](brief.md#work-and-acceptance-criteria) | AC-02; V-003/V-004 | V-05a–f with both advisory/indispensable policies; V-07a–b |
| [Apply every proportionate breach and semantic rule](brief.md#work-and-acceptance-criteria) | AC-03; V-005 | V-04a–k; V-03b–d |
| [Preserve originals, correction continuity and exact transfer paths](brief.md#work-and-acceptance-criteria) | AC-04; V-004/V-007 | V-06 checkpoints 1–6; V-07a–d; V-10b/d/e |
| [Retain native scope, requiredness, ownership, reuse and failure policy](brief.md#work-and-acceptance-criteria) | AC-05; V-008 | V-08a–j; V-03e |
| [Keep optional instrumentation distinct and avoid duplicate execution](brief.md#work-and-acceptance-criteria) | AC-05; V-008 | V-09a–d |
| [Prepare decisive evals while preserving existing route/provenance cases](brief.md#work-and-acceptance-criteria) | AC-06; V-003/V-004/V-005/V-007/V-008 | V-01–V-10; V-11b/d |
| [Align current policy and managed distribution without widening scope](brief.md#authority-and-scope) | AC-06; scope/installer duties | V-10c; V-11a/c |

## Source and revision

Source brief: docs/tasks/T-003/brief.md

Source brief revision: 1

Verification revision: 1

Authority: derived from the task brief and its cited normative sources, especially
[plan sections 1–7 and T-003](../../project-plan.md#t-003--give-implementers-proportionate-feedback),
[task-map T-003](../../task-map.json), and the
[accepted T-002 producer](../T-002/reviews/acceptance-01.md).
Runtime and test references describe observation mechanisms, not new requirements.

Status: ready
