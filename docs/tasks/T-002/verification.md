# Verification Design: T-002 — Capture and hand off the starting code

Preflight must hand off the actual starting Python code and the repository's
existing native-check obligations. The report must remain usable through later
edits. Missing advisory evidence must stay visible without changing readiness
policy or weakening a required check.

## Shared setup and evidence boundaries

Use disposable Git repositories and the existing installed measurement fixture.
Supply a packaged executable brief, source-matched verification, resolved
dependencies, explicit work ownership and the selected readiness profile. Unless
a case changes one prerequisite, all other readiness prerequisites are satisfied.
Use the prepared pinned interpreter and helpers from one installation. Do not
install tools implicitly or refresh the active profile.

Where capture is expected, fixture instructions and run policy must explicitly
permit fresh JSON/text report writes as well as canonical `preflight.md`.
Snapshot source, real index, existing reports and unrelated paths before the
action. Fixture preparation can seed dirty code, earlier reports and prior
readiness; it is not evidence that preflight produced those states.

There are three distinct evidence boundaries:

- **Tool behavior:** reuse real CLI/filesystem/Git checks in
  `tests/test_maintainability.py`, including its installed fixture, and installer
  preservation tests. These prove capture and report behavior, not agent choices.
- **Workflow preparation:** inspect source preflight instructions, packet template,
  eval prompts, setup and grading expectations against the cases below. Exercise
  local setup where needed to establish that decisive inputs exist. This proves
  that an eval is executable, not that an agent follows the instructions.
- **Agent behavior:** only an approved live eval can qualify preflight decisions.
  Grade the actual reports, packet, command history and retained obligations.
  Exit codes, metadata validation and keyword matches alone are insufficient.

For V-01–V-11, the implementer supplies task-owned evidence and explicit gaps.
Fresh independent discovery corroborates changed guidance, setup and decisive
tool boundaries; separate acceptance decides whether that evidence is sufficient.
Independent live-agent corroboration is N/A unless separately approved: no live
qualification is required by this brief. T-003 consumer execution, T-004 reviewer
execution and T-005's complete correction journey remain outside this task.

## Test cases

### V-01 — Capture governed folders and preserve actual dirty bytes

**Situation:** Authorized Python work affects production, tests, evals, fixtures
and harness code. Include a tracked file with different HEAD, staged and worktree
bytes, relevant untracked Python, an unrelated sibling and an explicitly excluded
directory. Ownership permits measuring the dirty scope; it does not permit
changing those bytes or the index.

**Action:** Perform ordinary guided preflight and attempt capture before edits.

**Expected result:** Select the smallest relevant folders covering all affected
asset groups and future files. Respect explicit exclusions and retain asset-group
distinctions. A named complete report contains the actual worktree inventory,
source bytes/hashes and folder coverage, including relevant untracked code.
Neither HEAD nor index content substitutes for worktree content. Source, real
index and unrelated paths are unchanged. No reset, stash, staging or implicit
installation occurs.

**Why test this:** A clean-commit or production-only baseline can hide the real
starting changes and omit task-owned test or harness complexity.

**How to check:** Compare report snapshots and hashes with independently saved
input bytes, and compare the real index before/after. Reuse the existing
`test_snapshot_preserves_staged_unstaged_untracked_and_index` and folder/exclusion
coverage. Inspect prepared preflight inputs and the produced handoff if a live
eval is approved; the CLI fixture alone cannot prove agent scope selection.

### V-02 — An empty existing parent captures known absence

**Situation:** A new Python area has an explicitly selected existing parent with
no included Python files. Tools, settings and permissions are valid.

**Action and expected result:**

| Case | Action | Decisive result |
|---|---|---|
| V-02a | Preflight captures that parent before creation. | Valid empty inventory with named folder coverage; no invented numeric zeros. |
| V-02b | After capture, create a Python file under the parent and compare through the existing CLI. | File is covered and classified as new; numeric before/delta remain unknown. Original reports and index are unchanged. |
| V-02c | Attempt capture with a missing parent. | No usable baseline is claimed; report the evidence gap under V-08 policy. Do not create a parent to pretend it existed before work. |
| V-02d | Attempt capture with an explicitly excluded parent. | No usable baseline is claimed; exclusion is preserved and the gap follows V-08 policy. |

**Why test this:** A new area needs legitimate before evidence without treating
absence as a measured zero or expanding the tool's empty-measure contract.

**How to check:** Reuse
`test_empty_folder_baseline_preserves_absence_across_edits` and existing excluded
scope checks. Observe saved report contents and actual added source. V-02b is a
tool-level probe of the producer's coverage, not delivery of T-003's workflow.

### V-03 — Fresh capture paths preserve both report siblings

**Situation:** Otherwise valid capture scope has prior report files. Test these
independent occupied destinations: V-03a JSON only, V-03b text only, V-03c both.

**Action:** Prepare a new capture and handoff while retaining the earlier reports.

**Expected result:** Use a fresh output name and identify its exact JSON/text
pair. Every old report remains byte-identical. A direct CLI attempt to use an
occupied name refuses overwrite, including when only the text sibling exists.
The handoff never relies on a mutable `latest` alias. A fresh-path control
succeeds; refusal alone is not sufficient proof.

**Why test this:** Replacing either sibling can erase the task's original history.

**How to check:** Reuse `test_each_report_sibling_collision_refuses_write` and the
installed successful capture control. Compare sentinel bytes and inspect the
prepared fresh-name rule. Agent path choice requires actual eval output.

### V-04 — Both readiness profiles carry one applicable report reference

**Situation:** Use a successful capture from V-01 in two separate invocations:
V-04a guided packaged readiness and V-04b high-assurance packaged readiness with
its required authority, dependency source and run policy.

**Action:** Prepare the existing result/packet for the next implementation session.

**Expected result:** Each handoff identifies the exact JSON path and text sibling,
governed folders, capture origin, logical project and report facts for captured
inventory/source hashes and effective tool/settings/scope identity. It explains
how to check starting bytes and covered inventory before the first edit. These
are compact references to report facts, not a second dossier. Guided work keeps
its compact revision/scope applicability rules. High-assurance work keeps all
existing exact digests, separate dirty index/worktree identities and packet-only
freshness requirements. Colocated hashes are consistency/provenance evidence,
not a tamper-resistance claim.

**Why test this:** A path alone cannot tell a later session whether it is the
right report; adding measurement must not silently change readiness profiles.

**How to check:** Trace instructions and both template branches to a real report.
Resolve every handoff reference and check it against the saved facts. Preserve
the existing `queue-ready` and `queue-guided` eval distinctions and strict
freshness observations. Review high-assurance capture sequencing against its
existing freshness contract; expected report writes do not waive that contract.

### V-05 — Changed starting state cannot pass as the recorded baseline

**Situation:** Seed an earlier valid capture and applicable readiness. Change only
the indicated dimension before handing off current readiness; keep unrelated
prerequisites valid. V-05a is the success control.

| Case | Current starting state | Expected result |
|---|---|---|
| V-05a | Same logical project, included inventory, source and effective identity. | Baseline remains applicable. |
| V-05b | Worktree bytes change while `MM` status text remains the same. | Detect source-hash mismatch; old readiness/baseline applicability is not accepted. |
| V-05c | An included Python file is added under a covered folder. | Detect changed captured inventory before editing. Folder coverage does not prove unchanged starting inventory. |
| V-05d | A captured file is deleted. | Detect changed captured inventory before editing. |
| V-05e | A report from a different logical project has the same relative scope. | Reject project applicability; matching paths are insufficient. |
| V-05f | Effective tool identity changes incompatibly. | Report incompatible evidence; do not claim a usable original baseline. |
| V-05g | Effective settings contents change incompatibly. | Report incompatible evidence; do not accept old settings as current. |
| V-05h | Intended scope includes code outside captured folders. | Expose uncovered scope and use V-06 resolution; do not label it compared evidence. |

**Action:** Reconsider current readiness and specify the consumer's pre-edit
applicability check.

**Why test this:** Unchanged Git status, matching filenames or a valid JSON shape
can conceal a false starting state.

**How to check:** Use real source edits/inventory changes and existing incompatible
identity/report cases, plus the `freshness-change` fixture. Compare observations
with the report's saved facts, not status text alone. Every mismatch routes to
focused readiness reconsideration with its cause and next owner. V-08 governs
whether the remaining advisory gap blocks. This tests producer detection and
instructions; T-003 owns actual implementer consumption. One controlled change
per identity dimension avoids an unnecessary Cartesian matrix.

### V-06 — Corrections and scope recovery retain the original history

**Situation:** Seed an original capture and later task-owned edited code. These
later states are supplied upstream inputs, not preflight-authored corrections.

| Case | Action / supplied history | Expected handoff rule |
|---|---|---|
| V-06a | Prepare a correction within original folder coverage. | Keep the original JSON/text reference and historical reports; later measurements use fresh names. Never recapture edited code as the starting state. |
| V-06b | Work unexpectedly requires another folder with exact recoverable pre-edit bytes. | Require authorized scope resolution and exact pre-edit evidence for added coverage before claiming a comparison. Preserve the original capture and name the additional coverage/evidence. |
| V-06c | Added coverage has no recoverable pre-edit bytes. | Keep the gap explicit; current measurement may describe current code but cannot establish a before comparison for uncovered code. Apply V-08 readiness policy. |

**Why test this:** A convenient replacement baseline can hide growth or falsely
claim coverage of work that was never captured.

**How to check:** Inspect correction/recovery guidance and prepared histories;
use existing repeated-comparison and uncovered-scope CLI evidence to check report
preservation and refusal. Do not build T-005's full installed correction journey
here. Recovery instructions must match the measurement guide's requirement for
verified exact preserved pre-edit bytes; an edited checkout is not that input.

### V-07 — Isolated clones receive the exact ignored report pair

**Situation:** Capture in one logical project checkout. A separate clone has
matching source and compatible runtime/settings but lacks the ignored reports.

**Action:** Prepare the transfer handoff, then copy only the named JSON/text pair
to the receiving repository and probe the report reference with the existing CLI.

**Expected result:** Name both report files and their receiving paths. Explain
that commits do not transfer ignored reports. The reference resolves after
explicit transfer despite a different absolute root. Missing files remain a gap;
no silent recapture occurs. The original reports are unchanged.

**Why test this:** A valid host path can be unusable in a separate agent clone.

**How to check:** Reuse mount-path and target-root report-handoff tests. Inspect
the transfer instruction against the actual pair, project identity and compatible
report. This proves local transfer usability, not execution by a later agent.

### V-08 — Advisory gaps and indispensable evidence have different decisions

**Situation:** Establish all unrelated readiness prerequisites. For the unavailable
cases below, reuse the same decisive fault with two explicit policies: suffix
`-A` means default advisory evidence; suffix `-R` means task/repository authority
requires that evidence before readiness. Supply the policy reference and named
capability owner. V-01/V-04 provide successful ready controls.
With the stated satisfied prerequisites, V-08a/b and each `-A` row can be ready
with the explicit not-applicable status or evidence gap. Each `-R` row is blocked.

| Case | Input / action | Expected result |
|---|---|---|
| V-08a | Docs-only scope. | Measurement is not applicable; no Python capture is claimed. Other prerequisites remain binding. |
| V-08b | Unsupported-language-only scope. | Measurement is not applicable; native obligations remain binding. |
| V-08c-A / V-08c-R | Required analyzer capability is absent; attempt the supported capture. | A: visible unavailable evidence, no unsolicited blocker or setup. R: blocked, with capability owner and smallest recovery action. |
| V-08d-A / V-08d-R | Referenced original baseline is missing. | A: visible missing evidence and continued readiness assessment. R: blocked with owner/recovery. Neither claims comparison success or silently replaces history. |
| V-08e-A / V-08e-R | Baseline is incompatible with effective tool/settings identity. | A: retain incompatibility and assess remaining prerequisites. R: blocked with owner/recovery. Neither claims usable comparison evidence. |
| V-08f-A / V-08f-R | Capture is incomplete, with one requested analyzer failing. | A: retain partial evidence and assess remaining prerequisites. R: blocked with owner/recovery. Neither labels the partial run complete. |

**Why test this:** Both always-blocking and always-ready shortcuts violate the
brief's conditional evidence policy.

**How to check:** Reuse missing-tool, partial-completion and incompatible-report
tool checks. Prepared evals must stage actual missing/incompatible/partial inputs
and policy variants; grade the packet decision and gaps against those inputs.
Do not infer the `-R` requirement from a tool's presence or exit code. This small
decision matrix covers the distinct failure types without multiplying them by
every readiness profile. V-10 checks that advisory fallback cannot waive a native
prerequisite.

### V-09 — Native discovery carries existing policy without inventing checks

**Situation:** Supply three independent discovery inputs with otherwise valid
readiness: V-09a an existing registry/equivalent; V-09b documented commands in
instructions/project map/native configuration but no registry; V-09c no existing
native check. The optional gates template is not an installed checker.

**Action:** Perform one focused discovery pass and prepare the check inventory.

**Expected result:** V-09a/V-09b carry each applicable exact command, governed
scope, policy reference, requiredness and existing stage owner. A whole-project
gate retains whole-project scope even when Python capture covers fewer folders.
V-09b needs no new registry. V-09c records absence without inventing commands.
No case runs all static gates to create another before baseline. Only an
authorized, justified cheap readiness check runs when useful under existing
ownership; no new checker, runner, evidence store or stage is introduced.

**Why test this:** Discovery can otherwise narrow hard-check scope, transfer
ownership or turn optional infrastructure into a new prerequisite.

**How to check:** Inspect the discovery sequence and inventory/template fields.
Prepared evals supply actual command/policy files; grade inventory values and
command history against them. Use the existing whole-project native F401 fixture
as a real command reference instead of creating another analyzer harness.

### V-10 — Native evidence keeps its owner and cannot be waived by metrics

**Situation:** Declare a native whole-project command, policy and stage owner.
For reuse cases supply its exact constituent coverage and checked-byte identity;
do not seed only a success sentence. In V-10a–d the existing execution owner is
the later implementation stage; these checks are not preflight entry conditions,
so otherwise valid preflight can be ready while retaining missing duties. In
V-10e–g explicit policy requires native success before readiness. Change one
condition per row.

| Case | Input / action | Expected result |
|---|---|---|
| V-10a | Current applicable aggregate evidence covers the command, scope, policy and checked bytes. | Carry the valid evidence; no constituent rerun solely to fill a report section. |
| V-10b | Required evidence is absent and belongs to a later existing stage. | Keep it owed to that owner/stage; do not invent a preflight blocker or silently mark it satisfied. |
| V-10c | Supplied required evidence has stale checked bytes. | Do not reuse as current; retain the existing owner's recovery duty and policy. |
| V-10d | Aggregate evidence omits the command or does not establish its governed scope/policy. | Do not claim constituent coverage; retain the missing evidence and owner. |
| V-10e | Native command has a real F401 hard failure while advisory measurement succeeds. | Result is blocked under the stated entry policy. Report both results separately; retain hard failure and its recovery route. Advisory success cannot waive it. |
| V-10f | Native capability is unavailable and policy requires it before readiness; advisory measurement is also unavailable. | Result is blocked by the native prerequisite with owner/recovery; advisory fallback changes nothing. |
| V-10g | Native capability is unavailable and policy requires it before readiness; measurement is not applicable. | Same native blocker and recovery duty; docs-only/unsupported scope grants no exemption. |

**Why test this:** Metrics can falsely authorize progress or cause unnecessary
duplicate native execution.

**How to check:** Reuse the real native-hard-failure/installed-advisory-success
test for V-10e. For V-10a–d, use recorded local command coverage and actual
before/after source identities, then inspect whether the handoff preserves or
rejects reuse correctly. For V-10f/g stage the missing command plus explicit
entry policy. Prepared agent grading observes decisions, obligations and run
history. Do not run gates at preflight merely to manufacture evidence for this
matrix; seeded owner evidence is upstream input whose admission is being checked.

### V-11 — Prepared evals reach their oracles and preserve earlier readiness rules

**Situation:** Existing preflight evals include high-assurance targeted invocation,
missing capability, dirty ownership overlap, noncanonical path refusal, guided
material/marginal cases, package preparation, context and revision recovery.

**Action:** Update those evals and setup only where this integration requires it;
inspect the installer and affected profile documentation/tests in the same change.

**Expected result:** Every claimed V-01–V-10 outcome has supplied input state,
permission and a decisive grading oracle. Capture cases explicitly authorize
report writes; unrelated paths remain protected. Preserve these existing cases:

| Existing eval IDs | Required preserved distinction |
|---|---|
| 1, 5, 6 | High-assurance exact invocation/freshness versus guided material/marginal readiness; seed-only tests do not prove repeated public behavior. |
| 2, 3, 4 | Missing indispensable helper, unauthorized user overlap and noncanonical packet path prevent ready; no helper creation, user-work edit or wrong-path write. |
| 7, 8, 12 | Legacy durable briefs are refused; packages need source-matched complete verification and canonical readiness; unpackaged direct work can stay inline. |
| 9 | Relevant context is assessed; ordinary unknowns do not invent blockers; unresolved decision-critical facts retain their owner. |
| 10, 11 | Verification revision and material fact changes need focused reconsideration; unchanged status text cannot waive high-assurance identity mismatch. |

No existing negative input is repaired to obtain green evidence. Reuse measurement
and installed fixture setup. Installer changes are limited to items made stale
by this integration and preserve its managed ownership boundary. Source guidance
and prepared evals do not claim T-003/T-004 delivery or live-agent qualification.

**Why test this:** New capture instructions can make previously runnable evals
contradict their write policy or erase a readiness regression.

**How to check:** Inspect eval setup, prompts, run policy and grading together.
Exercise changed setup locally with disposable roots and confirm actual inputs,
permissions and sentinel preservation. Review grading against real report content,
readiness decisions and native obligations; package/schema checks are structural
only. Reuse installer projection/preservation checks if affected. Record live
evals as unrun unless approved and actually graded.

## Verification ownership and order

The implementer first checks changed task-owned guidance/eval setup and relevant
measurement cases, then the owning `tests/test_maintainability.py` suite. Use the
prepared pinned interpreter; analyzer skips do not qualify measurement. Run
`tests/test_install_development_skills.py` when installer/projection evidence is
affected. Resolve targeted failures before broader checks. Fresh discovery checks
current evidence independently; separate acceptance consumes that report.

Before implementation handoff, run the canonical architecture check and
`python3 tools/check_contracts.py --root .`. The canonical architecture command is
`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py`.
For cross-cutting implementation, the implementer owns `python3 tools/verify.py`
after focused checks pass, subject to applicable cost/permission approval.
Discovery may consume current aggregate evidence with established coverage,
policy and checked bytes; do not rerun solely for duplicate report sections.
Report active-profile drift without refreshing the active installation. None of
these structural checks establishes live preflight behavior.

## Coverage summary

| Promise from the brief | AC / plan verification | Required cases |
|---|---|---|
| [Actual folder scope, dirty/untracked bytes and preserved history](brief.md#work-and-acceptance-criteria) | AC-01; V-003 | V-01, V-02a–d, V-03a–c |
| [Exact applicable baseline, profile freshness, correction and transfer references](brief.md#work-and-acceptance-criteria) | AC-02; V-003/V-006 | V-04a/b, V-05a–h, V-06a–c, V-07 |
| [Not-applicable, advisory and indispensable evidence decisions](brief.md#work-and-acceptance-criteria) | AC-03; V-006 | V-08a/b, V-08c-A/d-A/e-A/f-A, V-08c-R/d-R/e-R/f-R, V-10f/g |
| [Native command discovery, scope, owner and current evidence](brief.md#work-and-acceptance-criteria) | AC-04; V-008 | V-09a–c, V-10a–g |
| [Executable eval inputs, preserved readiness and honest qualification limits](brief.md#work-and-acceptance-criteria) | AC-05; T-002 portions of V-003/V-006/V-008 | V-01–V-10 prepared outcomes, V-11 |

No risk rows are supplied in the brief. These cases derive the finite material
states from AC-01–AC-05 and their cited authority; they do not add requirements.

## Source and revision

Source brief: docs/tasks/T-002/brief.md
Source brief revision: 1; SHA-256 `9a9cfea7ec024f90dd033100bf68410806fee5d50fad5ac74eb97e159177ca63`
Verification revision: 1
Authority: derived from the task brief and its cited normative sources, especially project plan sections 1–2, 6–7, FLOW-002, T-002 and V-003/V-006/V-008; measurement guide capture/transfer contract
Status: ready
