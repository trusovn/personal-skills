# Task Review Discovery Report: T-003 — Give implementers proportionate feedback

| Field | Value |
|---|---|
| Producing stage | task-review-discovery; independent session |
| Coverage completeness | partial — registry synchronization remains outstanding (V-11d); confirmed preparation defect F-01 |
| Discovery iteration | 1; 2026-11-03 |
| Repository | /Users/mtrusov/work/skill-sources/personal-skills |
| Brief / verification | docs/tasks/T-003/brief.md revision 1; verification.md revision 1 |
| Readiness / decision context | docs/tasks/T-003/preflight.md, including Decision context and applicability |
| Submission | docs/tasks/T-003/results.md; READY_FOR_REVIEW claim |

This report publishes evidence only. It gives no acceptance verdict, approved deferral or advancement. It applies to the bytes below and does not review or authenticate itself.

## 1. Provenance and reviewed scope

This session authored none of the reviewed production, test or guidance bytes. It used the project-local discovery skill. No subagents, live models, dependency installs, active-profile refresh, staging or production edits occurred.

Reviewed staged implementation: implementer SKILL.md, eval definitions/README, measurement case data and builder/check, setup integration, flow README, measurement guide, root README and two proposal precedence notices. The brief, verification, preflight and task index are pre-existing preparation, per submission; they are authority/context rather than claimed implementation. The existing untracked maintainability-01.md is separate prior-stage evidence, not this session's work. No unstaged tracked difference exists, so fixture execution used the staged bytes. Scope is separable; no unexplained production overlap observed.

HEAD: `1844d3bada600c1d702f580550a4f5b42a4354a0`
Staged binary diff SHA-256: `a51a27099a8a689f6f262949d02b424f45db31a393491fd9b9db6d941fa7b11a`

Exact index identities (worktree has no tracked delta from index):

```text
100644 c107f0bdf455bb3f12b6f094c178b1495b6d8356 0	README.md
100644 bed8bf6551d1d2fab6fc1d442b07302f68ada3bc 0	docs/advisory-code-maintainability-signals.md
100644 10cb61553167c294d597b5bc60f65e6f6c7a1880 0	docs/future-maintainability-signals-integration.md
100644 c4716128cd4357ee5045206c334ed42264ede31a 0	docs/tasks/T-003/brief.md
100644 017275f3e961ec7b63ee963a1195f5d3f34374b8 0	docs/tasks/T-003/preflight.md
100644 d5c3b58858200ac60325367aed5539f9bd74b165 0	docs/tasks/T-003/results.md
100644 07c2162747691cd5f794afa44d80eea7cd0c74c8 0	docs/tasks/T-003/verification.md
100644 525fc18ddb57a2e1a627e98f0948b7d66649e28a 0	docs/tasks/index.json
100644 9fb0b5dd212ccd6d7ac7358ac677c9b33258b554 0	scripts/measure-maintainability.md
100644 d66327ab2090546f80512e4bcc9c05749ecf1d5b 0	skills/task-implementation-flow/README.md
100644 495a48b43387bdaa0ab4493e99b12685c966226f 0	skills/task-implementation-flow/bounded-task-implementer/SKILL.md
100644 4b8686eb72f92cc0bbaca574d860f163d8d46ece 0	skills/task-implementation-flow/bounded-task-implementer/evals/README.md
100644 dcd206c16e1c487ae1600c72278a8fa822bba4c9 0	skills/task-implementation-flow/bounded-task-implementer/evals/evals.json
100644 f3962ab69d9265a754d1a2f25be2f5e15f18baad 0	skills/task-implementation-flow/bounded-task-implementer/evals/files/check_measurement_fixture.py
100644 985d9e28b6668329559d384d60634364df6ea1e2 0	skills/task-implementation-flow/bounded-task-implementer/evals/files/measurement_cases.json
100644 76d2c8ae06974bb1fe813e621099ab4d74ee8fe4 0	skills/task-implementation-flow/bounded-task-implementer/evals/files/measurement_fixture.py
100644 0e955be55d7fb436c007d99afc79da8ee8b0c236 0	skills/task-implementation-flow/bounded-task-implementer/evals/files/setup_fixture.py
```

## 2. Confirmed findings

### F-01 [suggested P2] Same-status hash-mismatch eval changes Git status

- Location: `skills/task-implementation-flow/bounded-task-implementer/evals/files/measurement_fixture.py:151–152`; relevant checker branch in `check_measurement_fixture.py:52–53`.
- Trigger: construct V-01d with `basic`, then apply `change_start`. `src/logic.py` is clean at capture and is then changed by appending a comment.
- Observed before status: `AM src/user.py`, `?? harness/untracked.py`, `?? inputs/`. After status additionally includes ` M src/logic.py`. The statuses are different.
- Consequence: an agent that checks status alone can refuse this input correctly. The eval cannot distinguish that faulty implementation from the required source-hash validation despite its unchanged-status oracle. The focused checker passes because it asserts only unequal hashes.
- Affected AC: AC-01 and AC-06; V-01d and V-11b. Broken invariant: the decisive input must isolate byte identity from status text.
- Credible sibling surface: other freshness cases intended to isolate one identity while preserving other entry prerequisites, particularly V-01h's index/worktree contrast and V-01f's effective identity variants. V-01h's checker does verify the index contrast; no sibling defect is asserted.
- Smallest corrective direction: make the same-status case preserve the complete before/after status while changing captured bytes, and verify both conditions as independent setup properties. Keep the distinct index and inventory cases.

## 3. Completeness ledger

Evidence boundary for all pass rows: **source guidance and eval preparation only**, as required by this task. No row qualifies agent execution. Submitted evidence is results.md's scenario map (F plus owning-suite claims). Independent evidence: P1 (actual supplied-state check), P2 (adversarial same-status probe), P3 (real runtime suite), and static trace of the new skill section, request construction and finite case oracle. The case ID selects setup via `setup_fixture.py measurement:<ID>` with the README's source-root and pinned-interpreter prerequisites. Each oracle below is from verification revision 1 and is checked against available setup/guidance, not treated as an observed agent decision. Relevant flags, missing capability and deliberately altered reports are seeded inputs, not actual agent recovery evidence.

| Row ID | AC | Explicit case and setup/oracle | Submitted evidence | Independent probe / result |
|---|---|---|---|---|
| V-01a | AC-01 | Guided package; project, inventory, hashes, tools/settings/checks and governed folders match; oracle: Validate the supplied capture before the first code edit; consume it without replacement capture or broad readiness discovery. Remain guided. | results.md, V-01a | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-01b | AC-01 | High-assurance package; all exact freshness and packet-only delta checks match; oracle: Validate capture applicability and the existing exact packet contract before editing. Preserve schema/result obligations. Measurement reports are part of the recorded pre-packet state. | results.md, V-01b | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-01c | AC-01 | Different logical project despite compatible relative paths; oracle: Stop implementation entry and route focused preflight reconsideration; no code edit or silent new baseline. | results.md, V-01c | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-01d | AC-01 | Captured file bytes change while short-status text stays the same; oracle: Detect the source-hash mismatch before editing; route focused preflight, without resetting user work. | results.md, V-01d | fail — P2 demonstrates changed status; F-01 |
| V-01f-tools | AC-01 | Change one effective tool, settings or selected-check identity at a time; oracle: Detect each material identity mismatch; route focused preflight, without a replacement capture. | results.md, V-01f | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-01f-settings | AC-01 | Change one effective tool, settings or selected-check identity at a time; oracle: Detect each material identity mismatch; route focused preflight, without a replacement capture. | results.md, V-01f | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-01f-checks | AC-01 | Change one effective tool, settings or selected-check identity at a time; oracle: Detect each material identity mismatch; route focused preflight, without a replacement capture. | results.md, V-01f | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-01g | AC-01 | Planned Python edit falls outside governed folder coverage; oracle: Resolve scope/readiness before editing that scope; do not claim it is covered. | results.md, V-01g | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-01h | AC-01 | High-assurance index blob changes but worktree hash and status text match; oracle: Preserve the existing exact freshness refusal and schema-valid non-complete result; no implementation edit. | results.md, V-01h | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-02a | AC-01 | Capture the dirty/staged/untracked scope before the first edit; oracle: Capture actual worktree bytes, including the untracked file; preserve the staged index bytes and user work. Include all relevant asset groups under existing exclusions. Use fresh report paths and the installation-local runtime. Create no task package or formal identity solely for measurement. | results.md, V-02a | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-02b | AC-01 | Capture the selected existing empty parent, then add its first Python file; oracle: Baseline records valid empty inventory. Comparison treats the added file as absent before capture, not as having numeric zero metrics. | results.md, V-02b | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-02c | AC-01 | Measurement runtime or pinned tools unavailable; no indispensable-evidence requirement; oracle: Record unavailable evidence and owner/recovery; continue otherwise authorized work. Do not install tools, switch installations or invent a baseline. | results.md, V-02c | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-02d | AC-01 | Same unavailable capability with explicit indispensable starting-evidence authority; oracle: Stop before editing; name the authority, capability owner and recovery action. No clean comparison claim. | results.md, V-02d | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-03a | AC-02 | Change a function, add a file, delete a captured file; include relevant test/harness changes; oracle: Final comparison names changed, added and deleted Python paths within coverage. Submission references exact original JSON/text and current JSON/text paths, scope and measurement status. Required asset groups are not omitted. | results.md, V-03a | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-03b | AC-02 | Edit one function; shift or format the untouched hotspot sibling; oracle: Only the actually changed responsibility is affected. The sibling remains context, without mandatory cleanup or rationale merely from file membership, line movement or formatting. | results.md, V-03b | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-03c-rename | AC-02 | Rename or move a function, or extract part into helpers; oracle: Explain each actual relationship from diff/context. Assess the original responsibility with its helpers. Leave unmatched numeric before/after values unknown; invent no delta or attribution analyzer. | results.md, V-03c | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-03c-move | AC-02 | Rename or move a function, or extract part into helpers; oracle: Explain each actual relationship from diff/context. Assess the original responsibility with its helpers. Leave unmatched numeric before/after values unknown; invent no delta or attribution analyzer. | results.md, V-03c | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-03c-extract | AC-02 | Rename or move a function, or extract part into helpers; oracle: Explain each actual relationship from diff/context. Assess the original responsibility with its helpers. Leave unmatched numeric before/after values unknown; invent no delta or attribution analyzer. | results.md, V-03c | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-03d | AC-02 | Native diagnostic/count absent on one side, such as an exempt override method; oracle: Missing value stays unknown, even if another metric is complete. Do not infer zero or numeric improvement from diagnostic disappearance. | results.md, V-03d | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-03e-docs | AC-02 | Docs-only task; separately an unsupported-language task; oracle: Record measurement N/A with its reason; native-check duties still apply. | results.md, V-03e | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-03e-unsupported | AC-02 | Docs-only task; separately an unsupported-language task; oracle: Record measurement N/A with its reason; native-check duties still apply. | results.md, V-03e | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-04a-complexity | AC-03 | Complexity 6 → 8; oracle: Information only. No per-increase rationale or metric-driven refactor is required. | results.md, V-04a | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-04a-statements | AC-03 | Complexity 6 → 8; oracle: Information only. No per-increase rationale or metric-driven refactor is required. | results.md, V-04a | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-04a-arguments | AC-03 | Complexity 6 → 8; oracle: Information only. No per-increase rationale or metric-driven refactor is required. | results.md, V-04a | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-04b-complexity | AC-03 | Complexity 9 → 10; oracle: Equality is within target. No breach rationale or metric-driven refactor is required. | results.md, V-04b | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-04b-statements | AC-03 | Complexity 9 → 10; oracle: Equality is within target. No breach rationale or metric-driven refactor is required. | results.md, V-04b | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-04b-arguments | AC-03 | Complexity 9 → 10; oracle: Equality is within target. No breach rationale or metric-driven refactor is required. | results.md, V-04b | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-04c-complexity | AC-03 | New function has complexity 11; oracle: Explain retained structure and useful local alternatives. Exceeding the target alone does not reject the submission. | results.md, V-04c | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-04c-statements | AC-03 | New function has complexity 11; oracle: Explain retained structure and useful local alternatives. Exceeding the target alone does not reject the submission. | results.md, V-04c | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-04c-arguments | AC-03 | New function has complexity 11; oracle: Explain retained structure and useful local alternatives. Exceeding the target alone does not reject the submission. | results.md, V-04c | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-04d-complexity | AC-03 | Existing function 10 → 11; oracle: Explain the newly crossed breach; the target is advisory. | results.md, V-04d | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-04d-statements | AC-03 | Existing function 10 → 11; oracle: Explain the newly crossed breach; the target is advisory. | results.md, V-04d | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-04d-arguments | AC-03 | Existing function 10 → 11; oracle: Explain the newly crossed breach; the target is advisory. | results.md, V-04d | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-04e-complexity | AC-03 | Existing hotspot 11 → 12; oracle: Explicitly assess and justify worsening the breach. | results.md, V-04e | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-04e-statements | AC-03 | Existing hotspot 11 → 12; oracle: Explicitly assess and justify worsening the breach. | results.md, V-04e | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-04e-arguments | AC-03 | Existing hotspot 11 → 12; oracle: Explicitly assess and justify worsening the breach. | results.md, V-04e | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-04f-complexity | AC-03 | Materially edited hotspot 11 → 11; oracle: Consider useful local cleanup and briefly explain retention. No obligation to reach 10. | results.md, V-04f | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-04f-statements | AC-03 | Materially edited hotspot 11 → 11; oracle: Consider useful local cleanup and briefly explain retention. No obligation to reach 10. | results.md, V-04f | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-04f-arguments | AC-03 | Materially edited hotspot 11 → 11; oracle: Consider useful local cleanup and briefly explain retention. No obligation to reach 10. | results.md, V-04f | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-04g-complexity | AC-03 | Materially edited hotspot 12 → 11; oracle: Explain retained over-target structure despite improvement; no obligation to reach 10. | results.md, V-04g | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-04g-statements | AC-03 | Materially edited hotspot 12 → 11; oracle: Explain retained over-target structure despite improvement; no obligation to reach 10. | results.md, V-04g | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-04g-arguments | AC-03 | Materially edited hotspot 12 → 11; oracle: Explain retained over-target structure despite improvement; no obligation to reach 10. | results.md, V-04g | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-04h | AC-03 | Materially edited hotspot 11 → 10; oracle: No retained breach remains. No breach rationale is required solely because the starting value exceeded target. Semantic duties still apply. | results.md, V-04h | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-04i | AC-03 | Untouched hotspot remains 11 while its sibling changes; oracle: Context only; no required rationale or cleanup for the untouched function. | results.md, V-04i | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-04j | AC-03 | Metric falls after extraction, but ownership, names or navigation worsen; oracle: Address the concrete semantic cost; smaller numbers do not excuse it. Assess helpers together. Do not accept splitting cohesive code, opaque argument containers or tuned exclusions as proof of better design. | results.md, V-04j | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-04k | AC-03 | Required breach rationale is missing; oracle: Recover the explanation before claiming the submission complete. Each rationale identifies report, function, metric, known before/after, why decisions belong together and the cost of a plausible alternative. | results.md, V-04k | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-05a-advisory | AC-02 | Original report pair missing after edits; current tools usable; oracle: Measure current code at fresh paths, disclose missing before evidence and avoid a clean or complete comparison claim. Never recapture edited code as original. | results.md, V-05a | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-05a-required | AC-02 | Original report pair missing after edits; current tools usable; oracle: Measure current code at fresh paths, disclose missing before evidence and avoid a clean or complete comparison claim. Never recapture edited code as original. | results.md, V-05a | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-05b-advisory | AC-02 | Partial report, including missing native numeric evidence; oracle: Retain available facts and per-check limits. Attempt recoverable current measurement; unknown values remain unknown and partial evidence is not complete coverage. | results.md, V-05b | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-05b-required | AC-02 | Partial report, including missing native numeric evidence; oracle: Retain available facts and per-check limits. Attempt recoverable current measurement; unknown values remain unknown and partial evidence is not complete coverage. | results.md, V-05b | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-05c-advisory | AC-02 | Current report is stale after a further code edit; oracle: Produce a new comparison for current bytes against the original baseline if possible. Keep the stale report as history, not current proof. | results.md, V-05c | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-05c-required | AC-02 | Current report is stale after a further code edit; oracle: Produce a new comparison for current bytes against the original baseline if possible. Keep the stale report as history, not current proof. | results.md, V-05c | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-05d-advisory | AC-02 | Original format, tool or settings identity is incompatible; oracle: Disclose incompatibility. Use verified exact preserved pre-edit bytes for compatible remeasurement only if available; otherwise measure current code and retain the before-state gap. | results.md, V-05d | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-05d-required | AC-02 | Original format, tool or settings identity is incompatible; oracle: Disclose incompatibility. Use verified exact preserved pre-edit bytes for compatible remeasurement only if available; otherwise measure current code and retain the before-state gap. | results.md, V-05d | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-05e-advisory | AC-02 | An edited path is outside captured coverage; oracle: Do not report it as compared. Apply the authorized added-scope recovery in V-07; disclose any unrecoverable before-state gap. | results.md, V-05e | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-05e-required | AC-02 | An edited path is outside captured coverage; oracle: Do not report it as compared. Apply the authorized added-scope recovery in V-07; disclose any unrecoverable before-state gap. | results.md, V-05e | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-05f-advisory | AC-02 | Launcher/analyzers unavailable at submission; oracle: Report unavailable measurement, the actual attempted action or established capability failure, and owner/recovery. No implicit provisioning or fabricated report. | results.md, V-05f | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-05f-required | AC-02 | Launcher/analyzers unavailable at submission; oracle: Report unavailable measurement, the actual attempted action or established capability failure, and owner/recovery. No implicit provisioning or fabricated report. | results.md, V-05f | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-07a | AC-04 | Unexpected new scope; authorization resolved and exact preserved pre-edit bytes exist; oracle: Resolve authorized scope before editing it. Add coverage from verified pre-edit evidence without replacing the original covered baseline or relabeling current edits as starting code. Record original and supplemental references. | results.md, V-07a | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-07b | AC-04 | Unexpected scope was edited and no exact pre-edit evidence exists; oracle: Disclose an unrecoverable before-state gap; attempt current measurement. Do not invent a clean comparison. Required-evidence policy determines whether advancement must stop, as in V-05. | results.md, V-07b | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-07c | AC-04 | Requested JSON output or its sibling text path already exists; oracle: Preserve both existing files. Choose fresh output paths rather than delete or replace reports. | results.md, V-07c | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-07d | AC-04 | Submit to an isolated clone that lacks ignored reports; oracle: Name exact JSON/text source files and receiving paths needed by the consumer. Supply transfer instructions; a commit is not report transfer. With transferred files, retain the same logical project and compatibility checks despite absolute-root changes. | results.md, V-07d | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-08a | AC-05 | Registry supplies required native commands; oracle: Preserve all inventory fields and execute applicable implementer-owned obligations at their governed scope. A changed-file metric comparison does not narrow a whole-project check. | results.md, V-08a | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-08b | AC-05 | No registry; native command is documented; oracle: Discover and retain the documented command/policy/owner. Do not require a registry or invent a replacement command. | results.md, V-08b | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-08c | AC-05 | No native check exists; oracle: Record none discovered. Do not invent lint/typecheck commands. | results.md, V-08c | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-08d | AC-05 | Current aggregate establishes constituent command coverage, scope, policy and checked bytes; oracle: Reuse it with explicit ART-008 references. Do not run constituents again solely to fill a report section. | results.md, V-08d | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-08e | AC-05 | Aggregate omits the constituent command or required scope; oracle: Do not claim constituent coverage. Recover missing required evidence through its real owner or an authorized focused execution. | results.md, V-08e | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-08f | AC-05 | Checked bytes or governed policy changed; oracle: Reject stale evidence reuse; recover affected required proof through its owner. Retain unchanged applicable proof without blanket reruns. | results.md, V-08f | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-08g | AC-05 | Required proof missing or command unavailable; oracle: Carry the unresolved duty and recovery owner. An entry prerequisite prevents editing; a later-stage duty remains due at that stage. Do not claim completion of a required implementer check. | results.md, V-08g | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-08h | AC-05 | Native hard failure while advisory comparison completes successfully; oracle: Preserve the native failure and its policy consequence. Measurement success cannot authorize advancement past that failure. | results.md, V-08h | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-08i | AC-05 | Native hard failure while measurement is N/A; oracle: Preserve the same native failure policy and owner; N/A metrics do not waive it. | results.md, V-08i | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-08j | AC-05 | Correct the native failure and rerun its required check on current bytes; oracle: Record current successful native evidence with new byte identity; retain historical failure. Success can satisfy that duty without converting advisory metrics into a design verdict. | results.md, V-08j | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-09a | AC-05 | Installation-local evidence helper is available; oracle: Preserve the existing single invocation lifecycle. Wrapping the actual comparison is permitted; do not run it twice for capture or create a new lifecycle. | results.md, V-09a | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-09b | AC-05 | Helper unavailable or first best-effort operation fails; oracle: Skip instrumentation for the remainder of this invocation without repeated probes. Continue otherwise authorized measurement/work; report instrumentation unavailable separately from measurement status. | results.md, V-09b | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-09c | AC-05 | Explicit contract requires instrumentation; helper unavailable/fails; oracle: Retain the strict blocking/non-complete outcome. Do not downgrade to best-effort because metrics work. | results.md, V-09c | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-09d | AC-05 | Instrumentation available but measurement unavailable; oracle: Report those two facts separately. An evidence-run record is not a successful comparison. | results.md, V-09d | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-10a | AC-06 | Legacy direct brief, relabeled package, missing/blocked/stale readiness, foreign verification or non-executable parent; oracle: Preserve each existing refusal and its earlier owner. Do not bypass preparation to capture measurements. | results.md, V-10a | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-10b | AC-06 | Immediate review or otherwise explicitly required independent review; oracle: Guided submission stops at READY_FOR_REVIEW; machine contract retains its schema-defined submission status. Name only outstanding applicable conditional stages, then fresh discovery and separate acceptance. Do not perform or claim independent review in the implementer invocation. | results.md, V-10b | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-10c | AC-06 | Review remains optional; advisory warnings only; oracle: Preserve the existing milestone/no-review result and conditional policy. Warnings alone create no new required review stage. | results.md, V-10c | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-10d-significant | AC-06 | Significant test/eval/fixture/harness change; separately a trivial tests-only change; oracle: Preserve the respective existing maintainability/registry applicability and stage order. Include affected Python assets in measurement without promoting every tests-only change into a mandatory review. | results.md, V-10d | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-10d-trivial | AC-06 | Significant test/eval/fixture/harness change; separately a trivial tests-only change; oracle: Preserve the respective existing maintainability/registry applicability and stage order. Include affected Python assets in measurement without promoting every tests-only change into a mandatory review. | results.md, V-10d | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-10e | AC-06 | Interrupted or two-strike stopped task; oracle: Preserve non-complete status, actual attempts, unfinished scenario rows and next owners. Do not claim a final comparison or completed review that did not occur. | results.md, V-10e | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-11a | AC-06 | Follow current guidance and links, including superseded proposals; oracle: Current instructions lead to plan section 5 and retain targets 10/50/5. Conflicting every-increase defense/new-stage policy is clearly superseded. Historical experiment evidence remains unchanged. Naming, ownership, test/harness and abstraction duties remain intact. | results.md, V-11a | pass — current policy links/precedence and advisory table traced; historical observations retained |
| V-11b | AC-06 | Reconcile eval definitions and generated inputs with V-01–V-10; oracle: Every material row has supplied inputs, usable tools or an intentional capability fault, authorized report writes and a decisive oracle. Both entry paths, threshold decisions, correction continuity, missing evidence and native failure/reuse are reachable. Distinct original eval scenarios survive. | results.md, V-11b | fail — F-01 leaves one required decisive input invalid; other cases constructed by P1 |
| V-11c | AC-06 | Inspect installer membership, profile guide, shared-file list, focused tests and README installation instructions; oracle: Synchronize only entries made stale by this task. Preserve narrow managed ownership and installation-local dependencies. Use disposable installs for changed projection evidence; do not refresh this active invocation. | results.md, V-11c | pass — installer constants/profile guide/test inventory inspected; P1 performs disposable canonical installs; no new shared dependency or membership change |
| V-11d | AC-06 | Reconcile implementation evidence and contract changes; oracle: Register only implemented current contracts at the designated registry-updater stage. Report actual checks, skips, failures and profile drift. Do not label fixture setup, syntax checks or scripted tool runs as agent qualification. | results.md, V-11d | blocked — registry-updater has not run; registry still excludes implemented implementer contract; owner: task-contract-registry-updater |
| V-06-1 | AC-04 | Seeded prior CHANGES_REQUESTED; original B and C1; complete four-state ledger.; oracle: Before correction edits, map every supplied ledger row exactly once to planned implementation evidence or fresh-review coverage. Prior passes are navigation, not current corrected-byte proof. Preserve the failed reviewer regression. | results.md, V-06 | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-06-2 | AC-04 | Seeded prior CHANGES_REQUESTED; original B and C1; complete four-state ledger.; oracle: Make the bounded correction. Changed bytes stale affected comparison, native evidence and verdicts. Keep unaffected evidence only when still applicable. | results.md, V-06 | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-06-3 | AC-04 | Seeded prior CHANGES_REQUESTED; original B and C1; complete four-state ledger.; oracle: Run the reviewer regression first, then the nearest owning suite. Leave the reviewer-owned aggregate decision with its owner; report implementation checks separately. | results.md, V-06 | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-06-4 | AC-04 | Seeded prior CHANGES_REQUESTED; original B and C1; complete four-state ledger.; oracle: Create C2 at new JSON/text paths, comparing corrected bytes to B, not C1. Update applicable rationale. B and C1 remain byte-for-byte unchanged. | results.md, V-06 | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-06-5 | AC-04 | Seeded prior CHANGES_REQUESTED; original B and C1; complete four-state ledger.; oracle: Submit every ledger row, stable ID, incomplete reason and owner. Keep blocked and unchecked coverage visible. Name the first outstanding conditional stage and full remaining route to fresh discovery and separate acceptance. Do not mark reviewer rows passed or emit an independent verdict. | results.md, V-06 | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-06-6 | AC-04 | Seeded prior CHANGES_REQUESTED; original B and C1; complete four-state ledger.; oracle: For a subsequent task, capture that task's actual starting code. Do not reuse B as a permanent allowance for high values. | results.md, V-06 | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-01e-added | AC-01 | A relevant included file is added or removed after capture; oracle: Detect the changed inventory; route focused preflight, without accepting the old inventory as current. | results.md, V-01e | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |
| V-01e-removed | AC-01 | A relevant included file is added or removed after capture; oracle: Detect the changed inventory; route focused preflight, without accepting the old inventory as current. | results.md, V-01e | pass — P1 setup execution plus source/request/oracle trace; agent behavior unrun |

The 94 rows include metric-specific boundaries, both V-05 policies, relationship variants, and all six correction checkpoints. Original evals 1–9 and entry/route/review setup functions remain; setup integration only introduces guarded dispatch/import. Correction guidance preserves ledger IDs/owners and reviewer-owned decisions. Native fixtures invoke real Ruff over src/outside and preserve failure history/current hashes. P1 checks the successful/reused, stale, incomplete and failure/correction controls. P3 supplies actual runtime empty-folder, collision, relocation, unknown-count and dirty-index behavior. No runtime or validator contract changed. Existing high-assurance worker schema is reused; no agent result was produced or schema-valid completion claimed here.

## 4. Adversarial evidence

P2 independently contradicts the same-status precondition while P1 stays green. P1 separately exercises V-01h index contrast, all three metric boundaries, original-report preservation, dirty worktree/index distinction and real native failure/correction. No task process-lifecycle invariant is changed; synchronous fixture subprocesses returned, temporary roots were context-managed, and no server or long-lived fixture process was launched.

## 5. Independent command records

All commands ran from the repository root. Disposable fixtures use temporary directories; no dependencies or network are used.

- P1: `EVAL_MEASUREMENT_PYTHON="$PWD/.quality/venv/bin/python" .quality/venv/bin/python -B skills/task-implementation-flow/bounded-task-implementer/evals/files/check_measurement_fixture.py` — exit 0, 1 table-driven test, all 94 variants, 47.859 seconds. This does not prove the assertions cover every oracle (F-01 is a counterexample).
- P2: exact reproducer below — exit 0, `same_status: false`, before/after status as recorded in F-01. Independent of the checker assertion.
- P3: `.quality/venv/bin/python -B -m unittest discover -s tests -p test_maintainability.py` — exit 0, 33 tests, 16.506 seconds, no skips.
- P4: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py` — exit 0, 4 tests. Canonical structural architecture evidence only.
- P5: `python3 tools/check_contracts.py --root .` — exit 0, 6 subsystems / 15 indexed references. Structural consistency only; does not close V-11d semantic synchronization.
- Scope probes: `git status --short`; `git status --porcelain=v1 --untracked-files=all`; `git diff --name-only`; `git diff --cached --stat`; `git diff --cached --binary | shasum -a 256`; `git rev-parse HEAD`; index identities via `git ls-files --stage` for all staged paths. Read-only traces covered installed discovery/template, brief/verification/preflight/results, existing maintainability report, project-map/development, contract index/measurement record, source changes, installer constants/profile/test references.
- Installer full suite: not run; no installer implementation changed, P1 already executes canonical disposable projection. Submitted 36-test result is producer evidence only.

P2 exact reproducer (also the reviewer regression; run after correction expecting `same_status` true and unequal source hashes):

```sh
EVAL_MEASUREMENT_PYTHON="$PWD/.quality/venv/bin/python" .quality/venv/bin/python -B - <<'PYPROBE'
import sys,tempfile,json
from pathlib import Path
sys.path.insert(0,'skills/task-implementation-flow/bounded-task-implementer/evals/files')
import measurement_fixture as m
import setup_fixture as f
with tempfile.TemporaryDirectory() as d:
 f.WORK=Path(d);f.RUNS=f.WORK/'task-runs'; f.RUNS.mkdir();f.SCHEMA=f.WORK/'contracts/worker-result.schema.json'
 c=next(c for c in m.CASES if c['id']=='V-01d');r=f.WORK/'measurement-fixture'
 m.basic(r,c); before=f.git(r,'status','--short');m.change_start(r,c);after=f.git(r,'status','--short')
 print(json.dumps({'case':c['id'],'before':before,'after':after,'same_status':before==after},indent=2))
PYPROBE
```

## 6. Aggregate-gate record

`python3 tools/verify.py`: **not run**, owner this independent initial discovery pass, suppressed after decisive targeted F-01 failure. P3 is a focused runtime corroboration, P4/P5 are required structural handoff checks, not substitute aggregates. Submission's host/sandbox aggregate outcomes remain implementation-attributed: host exit 1 from active-profile drift, with behavioral suites claimed passed. No copied green gate is claimed; installed composition remains unqualified. No new gate or command is required.

## 7. Scope and exact status comparison

Prior maintainability report identities match the staged implementation blobs. Registry stage is explicitly outstanding in both submission and maintainability report. This pass does not perform it or waive it. Existing ignored implementation report pairs are submission references, not independently regenerated task measurements. They must travel explicitly to an isolated consumer per results.md.

Exact status before report write:

```text
M  README.md
M  docs/advisory-code-maintainability-signals.md
M  docs/future-maintainability-signals-integration.md
A  docs/tasks/T-003/brief.md
A  docs/tasks/T-003/preflight.md
A  docs/tasks/T-003/results.md
A  docs/tasks/T-003/verification.md
M  docs/tasks/index.json
M  scripts/measure-maintainability.md
M  skills/task-implementation-flow/README.md
M  skills/task-implementation-flow/bounded-task-implementer/SKILL.md
A  skills/task-implementation-flow/bounded-task-implementer/evals/README.md
M  skills/task-implementation-flow/bounded-task-implementer/evals/evals.json
A  skills/task-implementation-flow/bounded-task-implementer/evals/files/check_measurement_fixture.py
A  skills/task-implementation-flow/bounded-task-implementer/evals/files/measurement_cases.json
A  skills/task-implementation-flow/bounded-task-implementer/evals/files/measurement_fixture.py
M  skills/task-implementation-flow/bounded-task-implementer/evals/files/setup_fixture.py
?? docs/tasks/T-003/reviews/
```

Expanded untracked-path status before write:

```text
M  README.md
M  docs/advisory-code-maintainability-signals.md
M  docs/future-maintainability-signals-integration.md
A  docs/tasks/T-003/brief.md
A  docs/tasks/T-003/preflight.md
A  docs/tasks/T-003/results.md
A  docs/tasks/T-003/verification.md
M  docs/tasks/index.json
M  scripts/measure-maintainability.md
M  skills/task-implementation-flow/README.md
M  skills/task-implementation-flow/bounded-task-implementer/SKILL.md
A  skills/task-implementation-flow/bounded-task-implementer/evals/README.md
M  skills/task-implementation-flow/bounded-task-implementer/evals/evals.json
A  skills/task-implementation-flow/bounded-task-implementer/evals/files/check_measurement_fixture.py
A  skills/task-implementation-flow/bounded-task-implementer/evals/files/measurement_cases.json
A  skills/task-implementation-flow/bounded-task-implementer/evals/files/measurement_fixture.py
M  skills/task-implementation-flow/bounded-task-implementer/evals/files/setup_fixture.py
?? docs/tasks/T-003/reviews/maintainability-01.md
```

Expected status afterward (`--short` collapses this pre-existing reviews directory, so it remains identical):

```text
M  README.md
M  docs/advisory-code-maintainability-signals.md
M  docs/future-maintainability-signals-integration.md
A  docs/tasks/T-003/brief.md
A  docs/tasks/T-003/preflight.md
A  docs/tasks/T-003/results.md
A  docs/tasks/T-003/verification.md
M  docs/tasks/index.json
M  scripts/measure-maintainability.md
M  skills/task-implementation-flow/README.md
M  skills/task-implementation-flow/bounded-task-implementer/SKILL.md
A  skills/task-implementation-flow/bounded-task-implementer/evals/README.md
M  skills/task-implementation-flow/bounded-task-implementer/evals/evals.json
A  skills/task-implementation-flow/bounded-task-implementer/evals/files/check_measurement_fixture.py
A  skills/task-implementation-flow/bounded-task-implementer/evals/files/measurement_cases.json
A  skills/task-implementation-flow/bounded-task-implementer/evals/files/measurement_fixture.py
M  skills/task-implementation-flow/bounded-task-implementer/evals/files/setup_fixture.py
?? docs/tasks/T-003/reviews/
```

Expanded status afterward adds only:

```text
?? docs/tasks/T-003/reviews/discovery-01.md
```

## 8. Questions, unchecked work and residual risks

- V-11d blocked: required registry synchronization has not occurred. Correction/evidence owner: task-contract-registry-updater; authority: brief AC-06 and repository contract policy. P5 success does not waive it.
- Live agent decisions and full installed composition are deliberately unrun, outside T-003 qualification; T-005 owns the latter. No budget approval for live evals was requested or inferred.
- Source-distribution and pinned-interpreter prerequisites are documented. Eval execution metadata alone does not supply them; runners must use the documented environment.
- Source guidance is aligned with the proportionate rationale table and native owner/policy separation. Fixture preparation success cannot substitute for the failed adversarial setup property.

## 9. Coverage and next route

Coverage is partial due to V-11d, with F-01 confirmed. Send this report and all preparation/context plus staged diff to the separate acceptance decision call. Discovery makes no decision. Any correction requires current-byte discovery, reviewer regression and applicable earlier-stage re-entry; no report is overwritten.

## 10. Discovery continuation

- Iteration / current byte identity: initial independent pass; HEAD and staged diff SHA-256 in section 1; exact index blobs retained there.
- Coverage rows: all 94 case IDs in section 3; V-01d and V-11b fail; V-11d blocked; all remaining rows pass for source/eval preparation only.
- Finding IDs: F-01, suggested P2; no prior discovery finding IDs supplied.
- Finding/scenario continuity: producer claimed all prepared; current independent P1 passes but P2 disproves unchanged-status input. Correction owner: implementer; fresh evidence owner: independent discovery; decision/authority owner: separate acceptance under brief/verification revision 1. Sibling identity cases named in F-01. V-11d incomplete reason: updater stage absent; updater owns correction/evidence, acceptance owns disposition. Maintainability-01 is prior-stage evidence only.
- Preparation/context: docs/tasks/T-003/brief.md revision 1; verification.md revision 1; preflight.md including Decision context and applicability; results.md; reviews/maintainability-01.md.
- Reviewer regressions: P2 exact inline command, plus P1 exact fixture command; no repository regression file added.
- Aggregate gate: not run, `python3 tools/verify.py`, independent initial discovery owner; suppressed after F-01.
- Next: separate task-acceptance-review consumes this report, staged diff, brief, verification, preflight/context, submission, maintainability report, F-01 and blocked V-11d. No advancement is implied.
