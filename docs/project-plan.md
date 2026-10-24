# Maintainability feedback in the bounded task flow

## Product outcome

Help implementation agents produce code that later agents can locate, understand,
test, and change. Capture the starting code once, give the implementer useful
feedback, and let an independent reviewer assess retained complexity and design.
Measurements guide attention. They do not decide whether a design is acceptable.

The first useful proof is an installed command capturing a target repository,
comparing changed files, and preserving its source and Git index. The complete
delivery adds the skill handoffs and evidence described below.

| Task | What it enables next |
|---|---|
| [T-001 — Distribute usable measurement tooling](#t-001--distribute-usable-measurement-tooling) | Installed skills can measure a separate target repository without this source checkout. |
| [T-002 — Capture and hand off the starting code](#t-002--capture-and-hand-off-the-starting-code) | Implementation receives a named baseline and the existing repository check obligations from preflight. |
| [T-003 — Give implementers proportionate feedback](#t-003--give-implementers-proportionate-feedback) | Implementers compare their changes and explain material threshold decisions. Direct tasks also capture before editing. |
| [T-004 — Add independent measurement and review decisions](#t-004--add-independent-measurement-and-review-decisions) | Reviewers assess actual submitted files and carry their decisions into the existing downstream route. |
| [T-005 — Verify the complete installed handoff](#t-005--verify-the-complete-installed-handoff) | Local integration evidence and prepared agent evals establish what is proved and what remains unqualified. |

Status: `READY_FOR_PLAN_VERIFICATION`  
Plan version: `2026-10-24 / 1`

## 1. Planning authority

The owner accepted the direction in the preceding conversation on 2026-10-24:
one task baseline, implementer feedback, and reviewer-owned independent
comparison; increases within limits are information; retained breaches need
reasoning; touched legacy hotspots invite bounded cleanup, not mandatory
threshold compliance. This plan persists that accepted direction.

Repository instructions, [project map](project-map.md), and
[development guide](development.md) govern placement and verification. Current
implementation is described by the [tool guide](../scripts/measure-maintainability.md),
[highlights update](maintainability-tool-highlights-change.md), and
[zero-limit collection update](ruff-zero-collection-update.md). The
[contract index](contracts/index.json), particularly installation and runtime
evidence, describes implemented reusable surfaces.

The owner's follow-up also requires integration with existing foundation-defined
static checks. Current source confirms that project-bootstrap plans relevant
lint/typecheck/build capability, repo-foundation documents commands, and
architecture-guardrails defines native hard rules and optional command discovery.
Task-maintainability-review already discovers and runs/validates the architecture
gate; it does not currently define general lint/typecheck ownership. Preserve
that work and close the handoff gap rather than replace it.

This direction supersedes the policy in
[the advisory proposal](advisory-code-maintainability-signals.md) requiring a
response and preferred refactor for every increase, including below limits.
It also replaces the separate deterministic stage and warning-for-every-increase
approach in [the older integration proposal](future-maintainability-signals-integration.md).
Historical experiment results remain evidence of their own snapshots, not
current workflow policy. Existing semantic-review source remains the starting
point; its recent improvements must be preserved.

This is an integration change in an existing repository. Missing project-wide
charter/readiness documents do not require a new bootstrap exercise. Source
skills are development specifications. Installed skills remain distinct and
must not be refreshed during an active invocation.

## 2. Scope

Include Python complexity, native statement counts, and native argument counts;
preflight and self-preflight capture; implementation and independent-review
comparisons; correction handoffs; installation; focused regression evidence;
and prepared agent-behavior evals. Keep provisional advisory targets at 10/50/5.
Include relevant production, test, eval, fixture, and harness code, with existing
explicit exclusions and separate asset groups.
Reuse repository-defined lint, typecheck and architecture commands, their current
requiredness, policy and stage owners. Integrate discovery and evidence consumption
with the new metrics without inventing a new static-analysis stack.

Do not add analyzers, a quality score, a new agent stage, a generic check runner,
automatic refactoring, mandatory live evals, or controller/orchestrator changes.
Do not add correctness lint rules to this measurement command or merge existing
hard architecture gates into it. Do not broaden review applicability: a
measurement warning alone does not require a previously optional review stage.

## 3. Actors and capabilities

| ID | Actor / capability | Outcome | Flows |
|---|---|---|---|
| CAP-001 | Installer / portable measurement | Complete runtime and explicit setup work in a target repository. | FLOW-001 |
| CAP-002 | Preflight or implementer self-preflight / starting evidence | Starting bytes and scope reach later stages without recapture. | FLOW-002 |
| CAP-003 | Implementer / feedback | Changes receive proportional measurement and design reasoning. | FLOW-002, FLOW-003 |
| CAP-004 | Independent reviewer / disposition | Actual submitted code receives semantic review and a current decision. | FLOW-002, FLOW-003 |
| CAP-005 | Existing check owners / coordinated static evidence | Required repository gates remain effective, while advisory metrics and duplicate execution stay distinct. | FLOW-002, FLOW-003 |

## 4. Artifact and state catalog

| ID | Artifact | Authority / producer | Consumers | Lifecycle and permitted changes |
|---|---|---|---|---|
| ART-001 | Installed runtime and effective settings | Installer projects managed source; target owner owns explicit target settings. | All measurement callers | Versioned inputs. An installation/settings change may invalidate comparison compatibility. No active-run refresh. |
| ART-002 | Task baseline and capture reference | Preflight, or self-preflight before the first edit; tool owns captured measurement facts. | Implementer, reviewer | One original baseline per task. New report path; source snapshots/hashes, scope and measurement identity retained. Never replace during corrections. |
| ART-003 | Current comparison report | Measurement tool, invoked by implementer or independently by reviewer | Implementer, reviewer | New named report for each run. Applies only to captured current bytes and compatible baseline/settings. Historical reports remain unchanged. |
| ART-004 | Implementation rationale | Implementer, in its existing submission/correction artifact | Reviewer | References report, function and metric; corrected submissions supersede applicability, not history. |
| ART-005 | Maintainability review and dispositions | Fresh reviewer in the existing numbered review artifact | Implementer, registry updater, discovery, acceptance as applicable | Current verdict binds reviewed bytes and dispositions. Affected corrections stale it; stable finding IDs survive. |
| ART-006 | Verification evidence | Local tests and, only when authorized, fresh agent evals | Task reviewers and owner | Records command, inputs/setup, actual result, skips and limits. Structural, deterministic and agent-behavior evidence remain distinct. |
| ART-007 | Existing repository check policy | Repository authority: command registry, agent instructions, native configs/tests and task-runner definitions | Preflight, implementer, reviewer, existing check owner | Existing source of truth; discovery references it without copying policy or changing requiredness. |
| ART-008 | Existing check execution evidence | Declared stage/check owner executes the native command; existing evidence tooling may record it | Implementer, reviewer and downstream owner | Command, governed scope, policy, checked-byte identity, result and producer/stage; stale when relevant inputs change. No new evidence store is required. |

Report files live under the measured repository's ignored `.quality/reports/`.
Carry explicit relative paths, not a mutable `latest`. Transfer reports when
using isolated clones; commits alone do not transfer ignored files. Reuse
existing preflight/submission/review artifacts for references and explanations;
do not add a parallel exception registry or evidence lifecycle.

## 5. Lifecycle and decision rules

```text
before edits -> captured baseline -> implementation comparison + rationale
                                  -> fresh reviewer comparison + semantic review
                                      -> ACCEPT -> existing outstanding stages
                                      -> CHANGES_REQUESTED -> correction -> fresh review
                                      -> INCONCLUSIVE -> recover required evidence
```

The correction path retains the original baseline and creates new comparisons.
At the next accepted task, measure its actual starting code; an older high value
does not grant a permanent allowance. Measurement execution has complete,
incomplete and incompatible outcomes separate from semantic review verdicts.
Exit 0 continues to mean successful measurement/comparison, not acceptance.

| Condition in an affected function | Implementer and reviewer handling |
|---|---|
| Value grows but stays at or below its target | Information only. No required per-increase rationale or metric-driven refactor. Semantic problems remain reviewable. |
| New function exceeds a target, or existing function crosses above it | Explain retained structure and useful local alternatives; reviewer explicitly agrees or identifies a concrete maintenance problem. |
| Existing over-target function gets worse | Explicitly assess and justify the increase. |
| Over-target function is materially edited but equal or improved | Consider a local cleanup; briefly explain retaining the hotspot. Reaching the target is not mandatory. |
| Legacy hotspot is untouched | Context only, even if another function in its file changed. |
| Metric falls but ownership, names or navigation worsen | Review the concrete semantic cost; smaller numbers do not excuse it. |
| Symbol is renamed, moved or extracted, or a native count is missing | Explain relevant relationships; retain unknown values and do not invent deltas. |

An affected function has an actual behavioral, structural or responsibility
change. File membership, line shifts and formatting alone do not make every
function affected. Use the diff and local context; do not build a new custom
change-attribution analyzer. The reviewer checks the implementer's attribution.
For extracted code, assess the original responsibility together with its helpers.

A rationale names the report, function, metric, before/after when known, why the
decisions belong together, and the cost of a plausible alternative. Group related
metrics when one explanation applies. Below-target growth requires no such row.
The reviewer records agreement or an evidence-based counterargument. A missing
required rationale must be recovered; a bare threshold is never a design blocker.
Unresolved material required evidence follows existing `INCONCLUSIVE` rules.
`CHANGES_REQUESTED` needs a concrete introduced/worsened maintenance problem or
an existing applicable hard architecture violation. Unchanged legacy debt cannot
be promoted into a blocker merely because cleanup was possible.

Cleanup must remain local, authorized and verifiable. Explain a useful wider
cleanup as follow-up work rather than silently expanding scope. Do not split
cohesive code, hide arguments in opaque containers, or tune targets/exclusions
to obtain smaller numbers.

## 6. Cross-task invariants

| ID | Invariant | Applies to | Intended evidence |
|---|---|---|---|
| INV-001 | Measurement increases and breaches are advisory; hard architecture rules retain their separate authority. | ART-003, ART-005; FLOW-002 | Threshold boundary tests and justified-breach/rejected-split evals. |
| INV-002 | Baseline captures actual pre-edit worktree bytes, including relevant dirty/untracked code; corrections never replace it. | ART-002; FLOW-002, FLOW-003 | Dirty-index preservation and correction journey. |
| INV-003 | Consumers use compatible settings/tool/scope identities and exact report paths; unknown is never zero or clean evidence. | ART-001, ART-002, ART-003; IF-001, IF-002 | Incompatible, missing-tool, native-exemption and report-transfer cases. |
| INV-004 | Changed bytes stale affected reports/verdicts; reviewer owns fresh comparison and semantic judgment independently of authorship. | ART-003, ART-005; IF-003; FLOW-003 | Stale submission and correction cases; fresh reviewer eval. |
| INV-005 | Attention follows actually affected responsibilities; below-target growth and untouched debt create no mandatory refactor. | ART-004, ART-005; FLOW-002 | Decision table, touched/untouched and extraction evals. |
| INV-006 | Installation is complete, uses its own runtime dependencies, and preserves unrelated target bytes and ownership boundaries. | ART-001; FLOW-001 | Real installed CLI and installer preservation/drift tests. |
| INV-007 | Measurement does not alter source/index, automatically install tools, or claim tamper resistance from colocated hashes. | ART-001, ART-002, ART-003; FLOW-001, FLOW-002 | Index/source checks, explicit setup and provenance limits. |
| INV-008 | Existing conditional stage order and affected-scope re-entry remain authoritative; no duplicated general review or new stage. | ART-005; IF-003; FLOW-003 | Existing route evals with measurement handoff additions. |
| INV-009 | Existing static-check policy and ownership are preserved. Advisory metric success cannot waive a hard failure; shared tools/aggregate commands are not executed twice merely to fill two report sections. | ART-007, ART-008, ART-005; IF-004; FLOW-002, FLOW-003 | Mixed hard/advisory fixture, current-evidence reuse and stale-evidence recovery. |

## 7. System interface map

| ID | Boundary / owner -> consumer | Inputs -> outputs | Success and failure semantics |
|---|---|---|---|
| IF-001 | Installed measurement CLI -> preflight, implementer, reviewer | ART-001 -> ART-002 or ART-003 | Existing `baseline`/`compare`/`measure`, `--root`, scopes and `--output` remain public. Settings/dependencies resolve as below. Complete measurements may include breaches and exit 0. Invalid/incomplete/incompatible runs remain distinct from design verdicts. |
| IF-002 | Preflight/self-preflight -> implementer/reviewer | ART-001 -> ART-002 | Carry report path, governed folders, capture origin and identity in existing handoff. Verify applicability before editing. Unsupported or unavailable evidence is explicit; never silently capture a replacement after editing. |
| IF-003 | Submission -> independent review -> existing downstream route | ART-002, ART-003, ART-004 -> ART-005 | Reviewer independently invokes comparison on submitted bytes; records coverage and dispositions. Downstream stages consume this report without repeating general maintainability review. Corrections follow affected-scope routing. |
| IF-004 | Repository check authority/owner -> preflight, implementer and reviewer | ART-007 -> ART-008 -> ART-005 | Discover exact existing command, scope, policy, requiredness and stage owner. Execute under existing ownership, or validate applicable current evidence. Missing/stale required evidence remains owed. Record hard failures separately from metric observations. |

### Existing lint, typecheck and architecture checks

Use one discovery pass through the existing registry/equivalent, then agent
instructions, project map and native task-runner configuration as needed. Carry
compact references in the current preflight/submission/review artifacts. This is
a check inventory, not a second policy registry or a new runner. If no registry
exists, documented commands remain sufficient.

| Stage | Existing static checks | New advisory measurements |
|---|---|---|
| Foundation setup | Preserve native tools, policy, commands and declared owners. Where this feature is enabled, add a discoverable advisory comparison command/reference alongside them. | Document the installed command, effective target settings and setup; no duplicated thresholds in a registry. |
| Preflight / self-preflight | Resolve applicable lint/typecheck/architecture obligations and capability; run only a justified cheap readiness check, not every gate as a new baseline. | Capture pre-edit folder baseline once. |
| Implementation | Run required applicable native checks under existing scope rules and retain current evidence. | Compare affected Python files and supply proportionate rationale. |
| Maintainability review | Keep architecture gate run/validation. Consume applicable current lint/typecheck evidence; recover missing/stale required evidence through its owner or an authorized focused run. | Independently compare actual submitted files and decide design tradeoffs. |
| Downstream stages | Consume current evidence; preserve existing functional ownership and required gate duties. | Consume the current maintainability report. |

A linter's name or exit code does not determine whether every rule is advisory
or hard. For example, native correctness findings and complexity counts may come
from the same executable. Preserve the repository's declared rule semantics;
this feature never promotes its heuristic metrics to hard rules or silently
waives a required repository check. Contradictory local policy goes to its
authority owner for focused resolution, not an agent-created exception. Keep
native correctness analysis with its existing owner rather than turning
maintainability review into another functional review.

Respect native check scope: a changed-file metric comparison does not narrow
a whole-project typecheck or dependency gate. A current applicable aggregate
result can cover constituent checks when its included commands and policy are
established; do not repeat them solely for reporting. The reviewer still owns
its fresh metric comparison, and reruns native checks when their scope/policy,
review authority or stale evidence requires it. Use existing run-evidence wrapping
when available, without a second execution just to obtain a capture.

When an existing linter already reports the same metric, reuse its observations
as context and make the selected comparable analyzer authoritative for the delta.
Do not compare scores from different formulas or require two justifications for
one function/metric decision. Keep the new tool limited to its pinned measurement
rules, separate from the repository's regular lint configuration and command.

### Installation and settings contract

Shared runtime belongs under source `scripts/` and installed `.agents/scripts/`,
following existing distribution ownership. Move the measurement adapter and
environment helper out of repo-only `tools/`; preserve the public
`scripts/measure_maintainability.py` command. Ship pinned requirements and default
settings as explicitly managed shared files beside the runtime. Keep one source
for shipped defaults; the source repository's `.quality/` files are its deliberate
target policy, not an undeclared installed dependency. Document the old/new
placement map in the owning implementation change.

Resolve each effective target settings file from the measured repository's
`.quality/maintainability.toml` and `.quality/ruff.toml` when present; otherwise
use the corresponding shipped default. Record effective settings identity and
origin. Invalid present settings fail visibly rather than falling back. Do not
inherit an unrelated root Ruff config or overwrite target policy during install.
Analyzer dependency pins remain installation-owned; target code cannot select
arbitrary packages through its measurement settings.

Keep platform-native environments and reports in target-owned `.quality/` so
installer refresh does not remove them. Setup must select the same target root
as measurement, with `setup --root <target>` available. Setup alone may install
dependencies and requires applicable approval for network use. Measurement
does not provision packages. Normal runs resolve helpers from the active skill's
installation, never from a global fallback or the original source checkout.

Replace evaluative highlight names `got_worse`/`improved` with neutral
`increased`/`decreased` in JSON and human output. Treat existing reports as
versioned evidence: document the format transition and reject incompatible
baselines. Fresh baselines precede edits; verified exact preserved pre-edit
bytes may be remeasured when required. Relocation is not permission to reset
a task's baseline to its current implementation.

## 8. End-to-end flows

### FLOW-001 — Install and prepare measurement

Trigger: a target repository receives the development profile. Terminal outcome:
the installed command measures that target independently of this source tree.

| Step | Owner / action | Reads -> writes | Interface / state / invariants |
|---|---|---|---|
| 1 | Installer projects explicit runtime files, defaults and skill instructions. | Managed source -> ART-001 | IF-001; absent -> installed; INV-006 |
| 2 | Caller resolves target policy and invokes explicit setup when authorized. | ART-001 -> target-native environment | IF-001; unprepared -> prepared; INV-003, INV-007 |
| 3 | Test/caller invokes installed measurement on target code. | ART-001 -> ART-006 | IF-001; usable or unavailable; INV-006, INV-007 |

Missing tools yield actionable unavailable evidence and the installed setup
command. Do not repair by switching installations. Tests may use an already
prepared pinned interpreter; they must not silently download dependencies.

### FLOW-002 — Capture, implement and review

Trigger: a supported Python task is ready to begin. Terminal outcome: current
maintainability disposition reaches the existing next required stage.

| Step | Owner / action | Reads -> writes | Interface / state / invariants |
|---|---|---|---|
| 1 | Preflight discovers existing native check obligations and captures smallest relevant folders; for direct tasks self-preflight owns this step. | ART-001, ART-007 -> ART-002 + check references | IF-001, IF-002, IF-004; uncaptured -> captured; INV-002, INV-007, INV-009 |
| 2 | Implementer checks capture applicability, edits, runs applicable required native checks and compares affected files, including added/deleted paths. | ART-002, ART-007 + submitted code -> ART-003, ART-008 | IF-001, IF-004; captured -> compared; INV-002, INV-003, INV-009 |
| 3 | Implementer attributes affected responsibilities and explains decisions under section 5. | ART-003 -> ART-004 | IF-003; compared -> submitted; INV-001, INV-005 |
| 4 | Fresh reviewer compares submitted files, runs/validates required architecture evidence, consumes or recovers applicable native-check evidence, and reviews semantics. | ART-001..ART-004, ART-007, ART-008 -> ART-003, ART-005 | IF-001, IF-003, IF-004; submitted -> accepted, correction owed, or incomplete; INV-001, INV-004, INV-009 |
| 5 | Existing stage owner consumes review evidence and follows the outstanding route. | ART-005 -> downstream handoff | IF-003; INV-008 |

Folder baselines cover future files inside those folders. For an entirely new
Python area, capture an explicitly selected existing parent folder with a valid
empty Python inventory; new files then have known absence before editing.
This narrowly extends baseline capture, not arbitrary empty `measure` success.
Compare only task-affected files inside baseline coverage; include deleted paths.
An unexpected scope expansion needs authorized scope resolution and exact
pre-edit evidence for added coverage; do not label uncovered code as compared.
Without recoverable before evidence, measure current code and record the gap.

Default integration attempts measurement for supported, authorized Python scope.
Docs-only/unsupported-language tasks record not applicable. Missing tooling,
baseline or comparison evidence is visible and semantic review continues where
possible. It blocks readiness/review only when explicit task/repo authority makes
that evidence indispensable; then name the capability owner and recovery path.
No passing or complete comparison is claimed for a skipped/partial profile.
This fallback concerns the advisory measurement capability only. Existing
required native checks retain their original failure/unavailable policy even
when the task has no Python scope or the metrics tool is absent.

### FLOW-003 — Correct or recover evidence

Trigger: a correction, changed submission or failed comparison. Terminal outcome:
fresh applicable evidence and a fresh affected-stage decision, or an explicit
unresolved evidence gap with its owner.

| Step | Owner / action | Reads -> writes | Interface / state / invariants |
|---|---|---|---|
| 1 | Implementer/capability owner resolves the bounded finding or evidence failure and identifies affected native checks. | ART-002, ART-005, ART-007, ART-008 -> corrected code or restored capability | IF-002, IF-003, IF-004; prior evidence -> affected evidence stale; INV-002, INV-004, INV-009 |
| 2 | Implementer compares against original baseline, updates rationale and reruns affected required native checks under existing ownership. | ART-002, ART-007 -> new ART-003, ART-004, ART-008 | IF-001, IF-003, IF-004; INV-002, INV-003, INV-009 |
| 3 | Fresh reviewer independently compares and reconciles surviving/resolved findings and dispositions. | ART-002..ART-004 -> new ART-005 | IF-003; INV-004, INV-008 |
| 4 | Coordinator follows current affected-scope route. | ART-005 -> downstream handoff | IF-003; INV-008 |

Report overwrite refusal leads to a fresh filename, not deletion/replacement.
Unknown native counts, ambiguous symbols and partial analyzer failures remain
unknown. Transfer the baseline to isolated reviewers and verify logical project
and source applicability; path compatibility alone proves neither. Guided
snapshots/hashes are provenance, not a protected anchor against a malicious
writer. Reuse an existing protected coordinator anchor when high-assurance
authority requires one; building that infrastructure is outside this plan.

## 9. Capability-to-flow coverage

| Capability | Artifacts / interfaces | Invariants | Completion |
|---|---|---|---|
| CAP-001 / FLOW-001 | ART-001, ART-006 / IF-001 | INV-003, INV-006, INV-007 | Installed command runs without source-tree access. |
| CAP-002 / FLOW-002 | ART-002 / IF-002 | INV-002, INV-003 | Before bytes and applicable reference reach implementation. |
| CAP-003 / FLOW-002, FLOW-003 | ART-003, ART-004 / IF-001, IF-003 | INV-001, INV-002, INV-005 | Current comparison and proportional rationale are submitted. |
| CAP-004 / FLOW-002, FLOW-003 | ART-005 / IF-003 | INV-001, INV-004, INV-005, INV-008 | Independent current disposition and route are explicit. |
| CAP-005 / FLOW-002, FLOW-003 | ART-007, ART-008 / IF-004 | INV-003, INV-008, INV-009 | Native gate duties and current evidence reach the responsible reviewer without redundant runs. |

## 10. Implementation task map

[task-map.json](task-map.json) is the machine-readable dependency and contract
index. The opening table owns the readable task outcomes. Execute T-001 ->
T-002 -> T-003 -> T-004 -> T-005; these tasks share contracts and need no parallel
implementation. Detailed task briefs and verification designs come after
independent plan verification.

### T-001 — Distribute usable measurement tooling

Own IF-001 and ART-001. Move runtime dependencies into the shared installation
boundary and implement section 7's settings/environment contract. Preserve
current analyzer semantics, source snapshots, affected-file comparisons and
non-mutating behavior. Add neutral labels and explicit empty folder baselines.
Do not add a generic resource installer: flat, explicitly managed shared files
fit the present installer contract. Extend its existing preservation, refresh
and drift cases; run a real installed CLI from an unrelated working directory
against a disposable target with source checkout access unnecessary.

Acceptance: installed baseline/compare succeeds with actual pinned analyzers;
custom target settings win over shipped defaults; malformed settings do not
silently fall back; missing tools produce a target-aware setup instruction;
legitimate breaches return execution success; unrelated files and real index
are preserved. Old report compatibility and empty-start behavior are explicit.

Update affected guide/README/project-map paths and installer selections/tests
together. At the bounded-flow registry stage, register implemented measurement
contracts and synchronize installation records; do not register this intended
capability now. Use the new runtime for self-check only after preserving exact
pre-edit source; label the comparison unavailable if that cannot be established.
Add the smallest discovery/handoff guidance to source repo-foundation and
architecture-guardrails, including the existing optional registry template where
useful. Explain advisory command discovery separately from native policy and
required gates. Inspect project-bootstrap/foundation-readiness guidance for
conflicts; change only references made stale by this integration. Do not make
the bootstrap choose a linter or require a new registry for every repository.

### T-002 — Capture and hand off the starting code

Own preflight's IF-002 producer and ART-002. Update source task-preflight
instructions, applicable packet/result templates and existing eval setup. Name
the supported scope, capture reference, identity and unavailable/not-applicable
handling without creating a separate dossier. Preserve guided versus
high-assurance distinctions and existing readiness/scope ownership.
For IF-004, carry applicable native check commands, scope/policy references,
requiredness and existing stage owners. Do not run all static gates merely to
create a preflight baseline or treat the optional registry template as a required
installed checker.

Acceptance: ordinary preflight supplies an applicable pre-edit folder baseline;
dirty and untracked source is captured without changing the index; explicit
required evidence failure cannot masquerade as ready; default advisory-tool
absence does not create an unsolicited blocker. A changed starting state is
detected before implementation rather than accepted as the recorded baseline.
Existing hard check prerequisites retain their current readiness semantics even
when new advisory measurement is unavailable.

### T-003 — Give implementers proportionate feedback

Consume IF-002; own ART-004 and the implementer side of IF-003. Update source
bounded-task-implementer, its submission/correction templates and relevant
fixtures. Direct execution uses self-preflight for the same capture contract.
Preserve optional run-evidence behavior: wrapping an actual comparison is
allowed when appropriate, but no duplicate run or new lifecycle is required.

Acceptance: baseline precedes edits in both entry paths; final changed-file
comparison includes relevant test/harness and deleted paths; below-limit
growth needs no individual defense; retained breaches and materially edited
legacy hotspots carry the section 5 rationale. Corrections keep the original
baseline. Missing, stale or uncovered evidence is explicit. The source
flow README and relevant advisory entry points point to the new policy without
rewriting historical experiments or retaining conflicting current instructions.
Required native lint/typecheck/architecture checks remain due under their real
scope and owner. Carry current ART-008 evidence beside the metrics reference;
reuse an applicable aggregate rather than invoking its constituents again just
for reporting. A metrics success cannot mask a failed required static check.

### T-004 — Add independent measurement and review decisions

Own ART-005 and reviewer/downstream IF-003. Update source
task-maintainability-review's inputs, protocol, report format and correction
instructions. Keep a compact measurement status/report reference and a complete
set of relevant rationale dispositions outside any capped optional-warning list.
Preserve recent naming, ownership, test/harness and abstraction-cost guidance.
Add a compact existing-check evidence section that preserves each native
command's policy, scope and owner. Validate freshness and required coverage;
recover missing proof without repeating general functional review. Keep native
gate failures, unavailable evidence and advisory metric dispositions separate.

Acceptance: reviewer runs its own comparison for submitted bytes and verifies
affected-function attribution. Justified breaches can receive ACCEPT; threshold
values alone cannot cause CHANGES_REQUESTED. A concrete counterargument names
the future maintenance cost and bounded correction. Mandatory missing proof
cannot disappear. Discovery/acceptance routing notes consume current review
evidence without duplicating general review; corrections keep existing stable
finding IDs and conditional stage order. Update downstream guidance only where
necessary to express this handoff.
Acceptance also covers a required native check failing while metrics complete,
a current aggregate supplying reusable check evidence, and stale evidence that
must be recovered. Do not invent lint/typecheck commands where none exist.

### T-005 — Verify the complete installed handoff

Own ART-006 and final composition proof. Reuse existing measurement/installer
tests and task-flow eval fixtures before adding new setup. Exercise installed
baseline -> actual target edit -> implementer comparison -> independent
comparison -> correction comparison against the same baseline, asserting source
identities, reports, labels and index preservation. A scripted invocation proves
tool composition; it cannot prove an agent followed its skill.
Include an existing native static check in that journey. Prove its actual hard
failure remains visible alongside successful advisory measurement, then correct
the input and recover current native evidence without changing either policy.

Acceptance: focused suites and required architecture/contracts checks pass with
truthful skips; the installed journey uses real pinned analyzers and a separate
review invocation; prepared eval scenarios cover section 11. Publish results
beside this plan in a new task/results file, with deterministic evidence separate
from agent-behavior results. No live model result is claimed without authorized
execution and independent grading. Remaining live qualification is explicit.

Every task changing a development-profile skill/shared dependency inspects and
synchronizes installer membership, managed-file list, profile guide, focused
installer tests and README instructions as applicable. Never refresh the active
installation to test the change; use disposable installations. Every task uses
the existing applicable independent review/registry/discovery/acceptance route.

## 11. System verification map

| ID / flow and risk | Cheapest decisive evidence and oracle | Owner |
|---|---|---|
| V-001 / FLOW-001, IF-001; incomplete distribution | Install into disposable repo; invoke installed CLI with real tools, unrelated cwd, and no dependency on original checkout. Verify reports and untouched target bytes. | T-001, T-005 |
| V-002 / INV-003; wrong settings or misleading highlights | Existing native Radon/Ruff cases plus target/default precedence, invalid settings, neutral labels, old-format rejection, and at/below/above targets. | T-001 |
| V-003 / FLOW-002, IF-002; false before state | Dirty staged/unstaged/untracked fixture; capture then edit; assert preserved baseline bytes/index and added/deleted/empty-start behavior. Exercise stale capture handling. | T-001, T-002, T-003 |
| V-004 / FLOW-003; correction erases growth or reuses stale review | Installed journey makes two real edits and compares both against original baseline; report identities differ and baseline does not. Existing routing evals assert affected-stage re-entry. | T-003, T-004, T-005 |
| V-005 / INV-001, INV-005; metric-driven over-refactoring | Prepared agent scenarios: 6 -> 8 below limit; justified cohesive breach; touched unchanged legacy hotspot plus untouched sibling; extraction with misleading names/navigation. Grade actual diff, rationale and reviewer disposition, not keywords alone. | T-003, T-004, T-005 |
| V-006 / INV-003, INV-004; false clean evidence | Prepared missing-tool/incompatible-baseline scenario and actual deterministic error cases; required and advisory evidence policies have distinct expected outcomes. Fresh reviewer must run current comparison. | T-002, T-004, T-005 |
| V-007 / INV-008; handoff changes review scope | Extend existing entry/correction route fixtures, including significant test/harness changes and trivial tests-only distinctions. Verify downstream guidance preserves conditional stage order. | T-003, T-004 |
| V-008 / CAP-005, IF-004, INV-009; duplicate or weakened native checks | Use a disposable repo with a real existing static command and declared policy. Assert hard failure plus successful metrics, unavailable/stale required evidence, reusable aggregate coverage and no invented checks when absent. Prepared agent eval grades policy/owner retention and absence of redundant runs. | T-001..T-005 |

Start with `tests/test_maintainability.py`, then the installer suite when affected.
Reuse the native pinned environment already available; repair/install only with
the applicable authorization. Native analyzer skips do not qualify measurement.
Before each task handoff run:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py
python3 tools/check_contracts.py --root .
```

For cross-cutting implementation, run `python3 tools/verify.py` after focused
checks pass. Report active-profile drift rather than refreshing this session's
installation. Report structural fixture/package checks as structural evidence,
not agent behavior. Live agent evals require a separate approved budget and
runtime; select the smallest cases above, stage all decisive inputs, use fresh
independent reviewers, and grade retained design quality and correction behavior.
If not run, delivery evidence must say agent behavior remains unqualified.

## 12. Risks, assumptions and delegated choices

No unresolved owner-level question blocks plan verification. The accepted
direction governs policy; current 10/50/5 targets remain provisional.

Main risks are hidden source-checkout dependencies, incompatible old baselines,
overbroad affected-file attention, missing native counts, and tests that merely
match instruction text. Section 11 assigns evidence for each. Scope expansion
and malicious concurrent writers are not solved by report hashes.

`DELEGATED`: internal runtime/helper decomposition; exact managed resource
filenames; compact reference/rationale field layout in existing artifacts;
minimal existing fixture extensions; report format revision number. These
choices must preserve the settled CLI, settings, provenance, handoff and review
contracts. Do not introduce a registry, schema framework or exception manager
solely to implement them.

## 13. Plan-verification handoff

Review [this plan](project-plan.md) and [task-map.json](task-map.json) together
against section 1's authority and the accepted conversation. Run
`project-plan-verification` in a fresh separate session before detailed task
briefs or implementation. The installed planning skill assigns that invocation
to the user; this planning session does not issue an independent verdict.

Structural validation checks references and dependency cycles only. It does
not prove semantic plan completeness, measurement behavior or agent quality.
Do not update this plan to track task completion; write results beside it.
