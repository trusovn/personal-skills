---
name: bounded-task-implementer
description: Implement, resume, or correct one bounded task from a request, ready task brief, or preflight packet — define missing acceptance criteria, add risk-based tests, verify progressively, preserve user work, report evidence. Guided by default; strict freshness and raw JSON for explicit high-assurance requests or supplied machine contracts; a packet alone stays guided.
---

# Bounded Task Implementer

Implement one bounded outcome with enough evidence to trust it. Carry the
routine implementation discipline so the user does not need to repeat “define
ACs, add tests, verify, and report” on every task.

Repository and user instructions outrank this skill. Preserve pre-existing user
work and never claim ownership of it.

## Required reference loading

Check applicability before the first dependent action. These references are
required instructions when their condition applies. If a required reference is
missing or unreadable, stop the affected action and report the exact gap;
do not infer permission to bypass it. Do not read every reference at startup.

| Reference | Loading condition and timing |
|---|---|
| [High-assurance and machine contracts](references/high-assurance.md) | Before validating or acting on an explicit high-assurance request or supplied strict machine contract; also before emitting a machine-contracted result or requested JSON artifact. |
| [Run-evidence lifecycle and recovery](references/run-evidence.md) | Before the first evidence lifecycle operation when the installation-local availability path below succeeds, or before any evidence operation when instrumentation is explicitly required; includes interrupted-run recovery and closure. The cheap availability check stays inline. |
| [Correction, resume and handoff](references/correction-protocol.md) | Before acting on a correction, resuming incomplete work, or preparing a correction handoff; before any correction production/test edit or ledger mapping. |
| [Preflight starting-evidence handoff](../task-preflight/references/execution-packet-template.md#starting-evidence-and-native-obligations-both-profiles) | For packaged guided and high-assurance work, before consuming packaged starting evidence and before the first implementation edit. |
| [Testing discipline](../../testing-discipline/SKILL.md) | For either profile, before adding or changing tests, evals or fixtures; inspect existing coverage and use its applicable guidance. |

## Choose the profile

Use `guided` by default.

Use `high-assurance` when the user requests it or the caller supplies a machine
contract: a worker-result schema with a durable result path, an orchestrator
invocation, or another strict freshness/result contract. Supplying a ready task
package alone — including its canonical `preflight.md` — is compact guided
readiness, not a high-assurance packet; such an invocation stays guided and
never selects the high-assurance profile. If guided work discovers security,
migration, destructive-state, concurrency, multi-writer, or audit requirements
that the current inputs cannot safely support, pause and recommend the smallest
escalation rather than silently building the full artifact chain.

### Guided inputs

Two entry routes share the guided profile; they never merge.

#### Conversational direct edits

A bounded conversational user request with no durable task package may be
implemented directly. Require enough to identify the repository, bounded
outcome, and authority; a small clear request is sufficient when it makes the
intended behavior clear. No preflight packet, result schema, run directory, or
tracker is required for these requests; the compact self-preflight and
verification discipline still apply.

#### Packaged guided entry

A durable task brief is only accepted as the `brief.md` inside one dedicated
task package. Refuse a direct legacy brief such as `docs/tasks/API-31.md` even when no `verification.md` exists, and route it to `task-brief-designer` for
package normalization. A package cannot be relabeled a conversational request
to bypass these prerequisites.

Before accepting a task brief, reject it as non-executable when it declares
`Task kind: composite` and `Status: decomposed`. Read `docs/tasks/index.json`
when present to identify its dependency-ready executable leaf, then reroute the
caller to that leaf (or report that no dependency-ready leaf is available).
Never implement a decomposed parent.

Before any package implementation edit, check entry applicability against the
current package state. For the executable leaf, entry requires:

- a `verification.md` whose `Source brief:` declaration resolves to the
  package's `brief.md`, at a verification revision the readiness references;
  missing or mismatched derived verification routes to
  `task-verification-designer` and then current `task-preflight`;
- a current applicable ready `preflight.md` bound to the same brief,
  verification revision, authority, and scope; missing, blocked, or stale
  readiness routes to `task-preflight` as the readiness owner; and
- matching authority and scope. Composite or blocked-design tasks, legacy
  direct briefs, and readiness naming another task, revision, or scope route to
  `task-brief-designer` or the authority owner, followed by affected
  preparation.

The implementer is not the readiness owner and does not repeat broad
discovery. Within the bounded preflight context, re-check only the recorded
current material facts: dependency availability, ownership overlaps,
permissions, decisive capabilities, and authority revisions. Expected
implementation or report effects alone do not stale guided readiness; a
material dependency, ownership, permission, capability, or authority change,
or a verification scenario revision, prevents reuse of affected obsolete
readiness and routes to focused `task-preflight`. A feasible task-owned future
test whose setup, tools, and observation boundary stay within scope may be
implemented; its absence is not a missing decisive capability. Packaged guided
entry requires no worker-result schema, exact digest chain, run directory, or
tracker; optional evidence instrumentation stays best-effort.

When the executable task folder contains `verification.md`, or the caller
supplies a verification-design artifact, require its `Source brief:` declaration
to resolve to the package's `brief.md`, then read it before inventing task-local
tests. Treat it as derived guidance under the brief: preserve its scenario/AC
coverage unless repository facts make a scenario infeasible, but do not let it
override the brief or constrain concrete test structure unnecessarily. A package
whose brief recommends a separate verification-design pass but has no artifact
routes to `task-verification-designer` before entry.

Use focused local discovery to resolve relevant paths, nearby tests, commands,
and current Git state. Ask only when a missing product, architecture,
compatibility, scope, ownership, or permission decision could materially change
the result.

## Starting evidence, final comparison and native duties

Use one original code baseline for this bounded task. Measurement is advisory;
it neither replaces required native checks nor adds an otherwise optional review
stage. Preserve the profile-specific entry/freshness rules above and below.

### Before the first implementation edit

For packaged guided and high-assurance work, consume the preflight's
[starting-evidence and native-obligation handoff](../task-preflight/references/execution-packet-template.md#starting-evidence-and-native-obligations-both-profiles).
Validate the supplied baseline against the logical project, exact included file
inventory and current source hashes, effective tool/settings/selected-check
identities, and governed folder coverage. Check actual bytes, including dirty
and untracked code; matching short-status text is insufficient. Material changes
to those facts route to focused `task-preflight` reconsideration before editing.
Do not silently capture a replacement or repeat broad readiness discovery.
High-assurance report preparation precedes the exact packet baseline; preserve
all separate index/worktree and packet-only-delta checks.

For conversational direct work, perform the same capture during self-preflight
after resolving authorized scope and report-write permission. Use the active
installation's sibling `scripts/measure_maintainability.py` and an already
prepared pinned interpreter; never borrow another installation or run setup
implicitly. Attempt `baseline <folders> --root <repo> --output <fresh-json>`
before edits to supported Python. Cover relevant production, tests, evals,
fixtures and harness folders under existing exclusions/asset groups. An existing
empty parent can cover future Python files; do not create a parent to manufacture
before evidence. Capture actual worktree bytes, including staged/unstaged
differences and untracked code, without resetting, stashing, staging or refreshing
the real index. Create no task package or formal identity solely for measurement.
Keep the exact JSON/text pair, scope, project binding and capture origin.

Consume the packaged native inventory; direct self-preflight discovers the same
exact commands, governed scope, policy reference, requiredness and existing
owner/stage from a registry/equivalent or documented commands. Record none when
none exists; invent no lint/typecheck command. Required entry evidence must be
usable before editing; later-stage duties remain with their existing owner.

### Before submission and after corrections

Compare final changed, added and deleted Python paths within original folder
coverage, including relevant tests/harnesses, using
`compare <affected-paths> --root <repo> --baseline <original-json> --output <fresh-json>`.
Use the diff and local context to identify actual behavioral, structural or
responsibility changes. File membership, formatting and line movement alone do
not make untouched siblings affected. Explain rename/move/extraction relationships;
assess extracted responsibilities with their helpers. Unmatched symbols and
missing native counts remain unknown, never invented numeric deltas or zeros.
Do not build a change-attribution analyzer.

Apply proportionate reasoning using effective targets (provisionally complexity
10, statements 50, arguments 5):

| Affected function condition | Required response |
|---|---|
| Growth remains at or below target, including equality | Information only; no individual defense or metric-driven refactor. |
| New function exceeds target or existing function newly crosses it | Explain retained structure and useful local alternatives. |
| Existing breach worsens | Explicitly assess and justify the increase. |
| Materially edited hotspot remains above target, equal or improved | Consider useful local cleanup and briefly explain retention; reaching target is not mandatory. |
| Hotspot reaches target or is untouched | No retained-breach rationale; untouched legacy debt is context only. |
| Numbers fall but ownership, names or navigation worsen | Address the semantic cost; assess helpers together. |

Each required rationale names report, function, metric, known before/after,
why the decisions belong together and the cost of a plausible alternative.
Group related metrics when one explanation suffices. Recover missing required
rationale before claiming completion. A bare threshold is not an automatic
rejection. Do not split cohesive code, hide arguments, tune exclusions/targets
or expand cleanup scope to improve numbers. Preserve existing semantic duties.

Keep original baseline B and all prior comparisons through corrections. Compare
corrected bytes to B at new paths, never to the preceding comparison. Changed
bytes stale affected reports/native evidence/verdicts; retain unaffected proof
only when applicable. Subsequent tasks capture their own actual starting code.
Unexpected scope expansion needs authorized scope resolution and verified exact
preserved pre-edit evidence for supplemental coverage, or an explicit
unrecoverable before-state gap. Never relabel edited code as the original.
Check both JSON and sibling text paths for collisions; choose fresh names,
never delete/replace reports. For isolated consumers name exact JSON/text source
files and receiving paths to transfer: ignored reports do not travel with commits.

Record docs-only/unsupported measurement as N/A. Missing, partial, stale,
incompatible or uncovered evidence cannot claim a clean/complete comparison.
Attempt recoverable current measurement at fresh paths before declaring evidence
absent; if the original is lost, measure current code and disclose the before gap.
Compatible remeasurement of before code requires verified exact preserved bytes.
Unavailable tools do not authorize provisioning. Advisory absence blocks only
when explicit authority makes that evidence indispensable; name the authority,
recovery owner and next action. Other required checks keep their failure policy.

Execute applicable required native checks under existing ownership and governed
scope, including whole-project checks outside the measured subset. Carry current
native evidence (ART-008) beside metrics: exact command, scope/policy,
checked-byte identity, result and producer/stage. Reuse aggregate evidence only
when constituent coverage, scope, policy and current bytes are established;
do not rerun constituents solely for reporting. Missing/stale required evidence
remains owed to its real owner. Native hard failures keep their consequences
even when metrics succeed or are N/A. Record corrected successful evidence with
new checked-byte identity while retaining historical failure.

Measurement availability is separate from optional instrumentation availability.
An actual comparison may use the existing run-evidence wrapper once; do not
duplicate measurement or create another lifecycle. The availability, skip-once
and strict-contract rules below remain unchanged.

## Optional run evidence

When the canonical run-evidence shared tooling for this skill installation is
available, ordinary guided execution uses it as best-effort sidecar instrumentation.
Resolve the active installation before invoking evidence tooling. Repository-local `.agents/skills/` takes precedence over user-global skill installations for work in that repository. When a matching `bounded-task-implementer` exists under the
repository's `.agents/skills/` tree, read and use that copy and resolve shared
tooling only from the sibling `.agents/scripts/` directory. Do not probe a
user-global skill path after a repository-local matching skill has been found.

For this source repository, the equivalent installation root is the repository
itself: skills live under `skills/` and shared tooling under `scripts/`. Do not
assume shared tooling lives at an application's repository root and do not mix a
skill from one installation root with helper scripts from another.

Before the first evidence lifecycle operation, perform one cheap availability
check for the resolved installation:

1. confirm that the resolved shared-scripts directory contains
   `run_evidence.py`, `workflow_version.py`, `runtime_context.py`, and
   `runtime-context.schema.v1.json`;
2. if they are present, run
   `python3 <resolved-scripts>/run_evidence.py --repo <worktree> availability`;
3. treat a successful `available: true` result as permission to use the normal
   evidence lifecycle for this invocation.

If the helper set is incomplete, the availability probe reports unavailable, or
the first best-effort evidence operation still fails, mark optional evidence as
unavailable for the remainder of this guided implementer invocation. Continue
the task and do not retry evidence operations during this invocation. Report the
missing instrumentation truthfully when useful. This skip-once behavior is
invocation-local only; it does not create repository state or disable evidence
for later invocations.

Evidence collection does not invalidate an otherwise executable bounded task
when tooling is missing or fails. An explicit repository, user, or machine
contract that requires instrumentation remains strict: an unavailable or failed
availability check is then a blocking instrumentation failure rather than a
best-effort skip.

When evidence remains available, follow the required lifecycle reference:
attempt instrumentation before edits, recover an open run before beginning a
new one, and close the run with its factual outcome. Do not create formal
artifacts solely for instrumentation. Unavailable tooling never authorizes
provisioning or cross-installation fallback.

## Test and eval maintenance

For either profile, use [testing-discipline](../../testing-discipline/SKILL.md)
as the authority when adding or changing tests, evals, or fixtures. Before adding
coverage, inspect relevant existing cases, setup helpers, and fixture generators
for gaps and overlap. Prefer updating, reusing, or consolidating them over
appending cases or copying setup infrastructure; add coverage for distinct
behavioral evidence that is missing. Before removing obsolete or redundant
tests or evals, identify the remaining coverage and preserve distinct scenarios,
failure modes, and boundary evidence. Keep maintenance within the task's scope;
ordinary small changes need no separate report or workflow stage.

## Guided workflow

1. Read applicable instructions, the task authority, and any task-local
   `verification.md` supplied or present in the executable task package. State
   a brief verification plan before editing.
2. Perform a compact self-preflight:
   - inspect `git status --short` and preserve user-owned work;
   - identify the bounded change area and prohibited adjacent work;
   - inspect the relevant entry point, closest tests, and local conventions;
   - resolve the narrowest meaningful test command; and
   - confirm required permissions and dependencies.
3. If acceptance criteria are absent, derive the smallest observable set from
   the request and state them briefly. Include the positive behavior and the
   most credible failure, unchanged-state, compatibility, or lifecycle case.
   Do not invent a materially ambiguous requirement.
4. When a task-local verification design is present, map its scenario IDs to
   planned evidence before editing and preserve coverage of every material AC.
   When the authority also supplies a finite high-risk matrix or named universal
   cases, map every row or case to existing or planned evidence before editing.
   Keep this concise for guided work and do not expand it into a generic risk
   inventory. Make omitted, unchecked, or blocked rows visible in the final AC
   evidence.
5. Choose the lowest reliable evidence:
   - reproduce a bug before fixing it when feasible;
   - for new behavior, add or update a focused test that could reject the old or
     faulty behavior;
   - cross the real boundary only where lower-level evidence cannot prove
     wiring, persistence, filesystem/database/process behavior, concurrency,
     recovery, authorization, or another material risk.
6. Implement the minimum code and test change. Match local style and do not
   create shared infrastructure, dependencies, or public contracts unless the
   task authorizes them.
7. Verify progressively: run the changed/targeted test first, then the nearest
   owning suite, then only the broader gate justified by blast radius. Ask
   before slow, flaky, privileged, destructive, live, networked, or otherwise
   expensive checks unless already authorized.
8. Inspect the final diff and status. Confirm every changed path belongs to the
   task, user work remains separable, and temporary artifacts created by this
   run are handled safely.
9. Return the guided human-readable result described below and apply the review
   handoff rules. Review is required when task metadata says `immediate`, the
   user requested it, or risk warrants independent corroboration.

For correction or resume, load the correction procedure before acting. Preserve
one original baseline and all prior reports; changed bytes stale affected
reports, native evidence and verdicts. Complete any supplied ledger's pre-edit
row-to-evidence map before changing production or tests. A fresh reviewer owns
reviewer row status; implementation checks do not replace independent review.

## Name the complete ordered submission route

Every required-review submission names the first outstanding applicable stage
and the complete ordered remainder, then ends the implementer invocation. When
independent functional review is required, the applicable route is, in order:

1. the canonical deterministic architecture gate, only when repository policy
   requires it for the changed bytes;
2. fresh `task-maintainability-review`, when maintainability review applies;
3. `task-contract-registry-updater`, when a registry stage applies;
4. fresh independent `task-review-discovery` evidence; then
5. the separate fresh `task-acceptance-review` decision.

The conditional policies produce these routes:

- neither conditional stage: discovery → acceptance;
- maintainability review only: architecture gate (when required) → fresh
  maintainability review → discovery → acceptance;
- registry stage only: registry updater → discovery → acceptance;
- both: architecture gate (when required) → fresh maintainability review →
  registry updater → discovery → acceptance.

Include the architecture gate only when repository policy requires it, and a
conditional stage only when it applies to the current submission; never invent
an obligation and never drop one. A conditional stage counts as completed only
when its evidence is applicable and current for the submitted bytes, including
its reviewed scope: stale, missing, or superseded evidence leaves that stage
owed in its ordered position, and a prior verdict's label alone is not current
evidence. Name the first outstanding applicable stage and every remaining stage
behind it; discovery is the first owner only when every applicable conditional
stage already has current evidence.

A production correction re-enters every conditional stage whose reviewed scope
the correction affected, before fresh discovery and the separate fresh
acceptance decision; current evidence for the corrected scope keeps an
unaffected stage out of the route. A tests-only correction still re-enters
applicable conditional stages unless repository authority explicitly authorizes
skipping them. Apply an explicit exception only to its authorized scope and
retain the remaining route. Choose correction routes by actual effects and current behavioral proof,
not by filenames or category labels:

- Clarification returns to the clarifying artifact owner; an evidence request is not a production-fix request
  and returns to discovery/capability ownership before a separate current decision.
- A genuine reference-only correction may use registry updater → fresh acceptance
  only when actual unchanged executable/behavioral effects and applicable current
  behavioral proof justify it. Otherwise repeat affected discovery/gates and
  obtain a separate current decision.
- A material coverage gap under unchanged requirements returns to
  verification designer → focused preflight → current revised-scenario evidence
  → new acceptance decision. Retain scenario IDs and the revision reason;
  affected old readiness/evidence is superseded. New proof cannot admit revised
  work under old readiness, even if old readiness is substituted after recovery.
- Changed requirements return to task design/decision ownership;
  ordinary corrections and clarifications do not restart task design, and
  expected implementation/report effects alone do not stale readiness.

For mixed conditions, preserve acceptance's precedence: an authorized bounded
blocker correction yields `CHANGES_REQUESTED` despite other unfinished proof;
prevented correction or missing decisive proof without an eligible blocker yields
`INCONCLUSIVE`. Neither permits advancement. Carry every finding and unfinished
row, reason and separate owner through the coordinator rather than collapsing routes.

Preserve accepted dispositions while relevant exposure/context is unchanged.
Optional improvements never restart correction. New blockers require current
proof, contextual materiality and an explicit reason: regression, formerly blocked
evidence, missed obligation, changed context/authority or newly demonstrated
material risk. Changed authority returns to its owner; add no global correction-round limit.

Naming the route never launches, delegates to, or waits for any
of those reviewers in the implementer invocation. When independent functional
review is not required, no route is imposed and the existing milestone or
no-review result semantics are unchanged. The requirement, not the metadata
label, decides the route: `review: milestone` or no-review metadata alone
neither imposes a route nor excuses the outstanding conditional stages and
fresh discovery when independent functional review is explicitly required.

## Preserve review provenance

`review: immediate` means finish implementation checks, emit the handoff, and
end the implementer invocation at `READY_FOR_REVIEW`. Here, "route" means name
the first outstanding applicable stage and the complete ordered remainder from
"Name the complete ordered submission route" as the next owners, ending in
fresh independent `task-review-discovery` evidence and the separate fresh
`task-acceptance-review` decision; it does not mean invoke or manage those
calls. A same-session self-check is useful when labeled as
implementation evidence, and its defects may be fixed, but it is not an
independent review.

Loading, quoting, or following `task-review-discovery` or
`task-acceptance-review` in the current session
does not reset provenance. If the current session authored any production bytes
under review, it must not emit `ACCEPT` or describe those bytes as independently
reviewed. Do not load the review skill, spawn or delegate to a reviewer, wait
for a verdict, run reviewer-owned gates, or continue after the handoff in this
invocation. Reviewer availability does not change the stop: the caller or
coordinator starts the fresh review separately. Never degrade to same-session
acceptance.

## Stops and budget behavior

Stop on ambiguous authority, user-work overlap, unsafe permissions, material
scope expansion, missing decisive capability, unexpected changed paths, or a
required check that cannot run within the authorized environment.

After two materially different fixes fail the same targeted behavior, stop
ordinary editing. Record the failure, discarded hypotheses, owning component or
contract, and one recommended next approach. Retain the partial diff, every
unfinished row/finding, exact attempt probes/results, reasons and next owners;
stopped work is non-complete and cannot advance. This same-target stop is not a
global correction-round counter. Task/user budgets, cancellation and genuine
capability stops retain these continuation obligations.

Continue through ordinary uncertainty under a stated reasonable assumption
within current authority; it alone does not create a blocker, design restart or
routine user prompt. Resolve credible serious consequences of delay or
materially costly later repair within current authority first. An unresolved
decision-critical exception retains one focused authority question naming the
consequence, needed fact and decision owner. Required proof is never waived.

Treat the brief's tool/time/context budget as a soft checkpoint by default. At
the checkpoint, summarize progress and continue while the task remains bounded
and there is enough context to finish safely. Stop or hand off only when the
user/repository made the limit hard, continued work would cross authority, or a
context boundary prevents reliable completion.

## Output contract

### Guided or ordinary interactive invocation

Open with the practical result and its contribution to the requested outcome,
what the checks support, material limits, and the next actor/action or owner
decision. For interrupted work, identify what was last checked and what remains
unfinished. Use ordinary language before task IDs and execution metadata.
Inspect the existing explanation first: retain clear prose, move or rewrite it
in place, and add only missing information. Keep detailed evidence in its owning
record and link to it; do not create a parallel progress ledger or update the
approved plan. This also applies to the required correction handoff reference.

Return a concise human-readable summary, not raw JSON:

```markdown
<Practical change and why it matters; checked scope and material limits; next actor/action or owner decision.>

Implemented: <outcome, READY_FOR_REVIEW, or non-complete status>

- Changed: <paths or none>
- Verified: <exact commands and results>
- AC evidence: <every verification scenario ID mapped to its current command, setup/oracle, and result, or an explicit blocked/unchecked reason and next owner>
- Preflight/context reference: <exact paths of the consumed readiness and context artifacts>
- Measurement: <original JSON/text and current comparison JSON/text; governed/affected scope, status or N/A reason, gaps/recovery owner, affected functions/relationships and required retained-breach rationale>
- Native evidence: <command, governed scope/policy, checked-byte identity, result and producer/stage; aggregate coverage/reuse or owed duties/owner; none discovered when applicable>
- Report transfer: <exact source and receiving JSON/text paths for isolated consumers, or shared paths>
- Remaining obligations: <unfinished task obligations carried forward, or none>
- Residual risks / skipped checks: <none or specifics>
- Next: <the first outstanding applicable stage and complete ordered remainder through fresh task-review-discovery evidence to the separate task-acceptance-review decision, user decision, fresh preflight, or complete>
```

Omit empty bullets when prose is clearer. Link to created artifacts rather than
embedding their serialized contents. Green tests cannot excuse an omitted AC or
scenario. Every scenario ID of the consumed verification design must be
accounted for with current evidence or an explicit blocked/unchecked reason and
next owner; implementer claims remain submission evidence, not independent
acceptance. For guided `review: immediate` work, use
`READY_FOR_REVIEW` as the submission state and name the first outstanding
applicable conditional stage — including a policy-required architecture gate —
and the complete ordered remainder through fresh independent
`task-review-discovery` evidence and the separate fresh `task-acceptance-review`
decision as next owner, then end the response without a review
verdict. Retain the existing human result semantics for milestone or no-review
work.

## Boundaries and routing

- Current-state executability failures route to `task-preflight` when a durable
  re-check is needed.
- Missing product/architecture authority or wider scope routes to the user or
  `task-brief-designer`.
- Completed work routes through the first outstanding applicable conditional
  stage and the complete ordered remainder to fresh independent
  `task-review-discovery` evidence and the separate fresh
  `task-acceptance-review` decision when independent review is requested or
  required; this invocation ends with the handoff and the next owner is started
  separately. Otherwise return it to the user.
- Do not approve your own work, update an official plan/tracker, commit/push,
  install dependencies, use the network, launch subagents, or modify
  orchestration state unless explicitly authorized.

## Definition of done

- Outcome and ACs are satisfied with proportionate behavioral evidence.
- Changes are minimal, in scope, and separable from pre-existing user work.
- Targeted and justified broader checks have truthful results.
- Guided output is useful to a person; machine output is emitted only under an
  explicit machine contract.
- The next owner can act without reading the implementation transcript.


<!-- contract-registry-flow:bounded-task-implementer:begin -->
## Contract-aware discovery and handoff

When `docs/contracts/index.json` exists, use it before broad repository discovery:

```text
task authority
  -> stable/current contract refs
  -> docs/contracts/index.json
  -> relevant subsystem contract
  -> module/executable authority
  -> focused code discovery as needed
```

This registry is current-state routing, not a substitute for reading the implementation needed for the task.

The implementer owns changes to executable/declarative contracts that are part of the implementation, including OpenAPI/GraphQL/protobuf/JSON Schema, public types/package exports, CLI/config definitions, migrations, and event/schema declarations.

When the standard flow includes `task-contract-registry-updater`, do not spend the implementation role's attention synchronizing `docs/contracts` or explanatory discovery references. Report the actual delta instead. If no such updater stage exists, follow the repository's normal stale-reference ownership rule.

Add these fields to the implementation handoff:

```text
Deliverables:
- <concrete task outputs>

Actual contract impact:
- added/changed/removed <durable cross-task surface>
- ...
OR
- none

Executable contract declarations changed:
- <paths or none>
```

Treat `Actual contract impact` as a factual claim for downstream verification. If implementation materially differs from an expected stable cross-task contract, report the mismatch instead of silently reinterpreting the plan.
<!-- contract-registry-flow:bounded-task-implementer:end -->
