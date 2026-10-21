---
name: bounded-task-implementer
description: Implement one bounded task from a clear user request, ready task brief, or high-assurance preflight packet. Use whenever asked to execute, resume, or correct a scoped implementation and the agent should automatically define missing acceptance criteria, add risk-based tests, verify progressively, preserve user work, and report evidence. Default to a lightweight guided flow with a human-readable result; require strict freshness and raw JSON only when an orchestrated packet or machine output contract is supplied.
---

# Bounded Task Implementer

Implement one bounded outcome with enough evidence to trust it. Carry the
routine implementation discipline so the user does not need to repeat “define
ACs, add tests, verify, and report” on every task.

Repository and user instructions outrank this skill. Preserve pre-existing user
work and never claim ownership of it.

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

Do not create a task brief, task ID, task package, runtime identity, or other
formal artifact solely for evidence collection. Pass task metadata only when it
already exists. Runtime identity is optional and must come through the shared
runtime-context contract, never model self-identification.

After the compact self-preflight and before the first implementation edit, when
evidence remains available:

- query the current worktree for an active evidence run;
- when taking over an open run whose original invocation never finished,
  recover that run before starting a new one, preserving the recovery boundary
  as uncertain rather than attributing all intervening changes to the prior
  agent;
- begin one new evidence run for this implementer invocation; and
- if any best-effort evidence operation fails in guided mode, apply the
  invocation-local skip above and continue the task.

On normal completion, close the evidence run with outcome `completed`. When
intentionally stopping or handing off before completion, close it with
`reported_interrupted` or `failed` as factually appropriate. A killed agent
may leave the run open; a later invocation may recover it before editing.

When the flow already requires one canonical deterministic architecture command
and an evidence run is active, that command may be executed once through
`run_evidence.py check ... --kind architecture -- <command>` so raw command,
timing, exit status, stdout, and stderr are captured. Do not add a duplicate
architecture execution only for evidence.

### High-assurance inputs

Require:

- one fresh preflight packet with status `ready`;
- its referenced packaged `brief.md` and run policy; a packet that references a
  direct legacy brief routes to `task-brief-designer` for normalization and
  then fresh `task-preflight`;
- its referenced verification-design artifact when the packet records one;
- the supplied worker-result schema and durable result path; and
- for correction, the acceptance findings and prior checkpoint/result.

Missing or inconsistent high-assurance inputs return the schema-valid
non-complete result required by the caller. Do not downgrade silently to guided
mode.

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

## High-assurance additions

Before editing, require the packet at the task package's `preflight.md` and
recalculate every packet freshness field exactly: brief bytes,
verification-design bytes when present, `HEAD`, the recorded post-packet short
status, separate
index/worktree identities for dirty paths, dependency/instruction/policy
digests, and task-specific environment fingerprints. Any unexplained mismatch
routes to fresh `task-preflight`.

The packet's own creation is the one expected baseline delta: its recorded
post-write status must equal current status before implementation, and all
non-packet paths and identities must still match the pre-write baseline. Do not
require the canonical packet to be ignored or status-neutral.

Treat the packet as the discovery and permission boundary:

- inspect and change only declared paths and cited context;
- map every recorded verification scenario to planned implementation evidence
  before editing, preserving blocked or unchecked coverage explicitly;
- establish the packet's highest-risk fail-first evidence;
- run its exact commands in order and record every attempted or required-but-
  skipped command truthfully;
- save logs and results only at authorized runtime paths; and
- validate the result against the supplied schema.

On a same-thread `CHANGES_REQUESTED` correction, preserve the bounded partial
diff and apply only in-scope findings. Changed contract, scope, helpers,
dependencies, permissions, or authority route through the owning earlier stage.

## Correct at the invariant level

For each reviewer finding, state the broken invariant before editing. Enumerate
only credible sibling cases already implied by that invariant, the task
contract, or an explicit finite matrix. Preserve the reviewer regression and
make the smallest correction that protects the invariant instead of adding a
field-specific, input-specific, or interleaving-specific exception. When
several explicit values share one oracle, prefer a local table-driven or
parameterized test over a reusable test framework.

When a prior review supplies a coverage ledger, consume it completely and
preserve every row identity and status. Prior passes are navigation context,
not acceptance evidence for corrected bytes; leave unchecked and blocked rows
for the fresh reviewer.

Before any correction edit, write a concise row-to-evidence map for the complete
supplied ledger. Include every row identity exactly once with its prior status,
planned implementation evidence or navigation use, and next owner. Map failed
rows to reviewer regressions and planned correction evidence; map unchecked or
blocked rows to explicit fresh-review coverage; keep prior passes as navigation
context only. This is a pre-edit gate: do not modify production or test bytes
until the map is complete, and do not silently omit rows that implementation
will not exercise.

The correction handoff must carry:

- the authoritative brief reference and preceding verdict;
- the applicable verification revision and preflight/context references;
- the first outstanding applicable conditional stage and the complete remaining
  route;
- the complete coverage ledger and complete findings;
- stable finding/scenario IDs, incomplete reasons and separate correction,
  evidence/capability and authority owners, including influenced sibling surfaces;
- attempts, exact results and discarded hypotheses when correction has stopped;
- the current scoped diff and reviewer reproducer commands;
- correction evidence attached to the failed rows, separately from reviewer
  row status;
- the broad-gate decision and owner; and
- every remaining unchecked or blocked row.

Run reviewer regressions first and the nearest owning suite after they pass.
Determine broad-gate ownership from the authority before editing. When it
assigns a final reviewer, leave that reviewer's aggregate decision untouched.
Run a broader or aggregate gate during correction only when the authority or
blast radius assigns it to implementation, or when no final reviewer is
assigned to own it. Report it only as implementation evidence. Never replace
implementation checks with an acceptance pass.

### Correction handoff format

For guided correction work, use this explicit final structure. Preserve the
labels and fill every field from the supplied review state; do not replace an
exact authority path or command with prose such as “the task” or “the reviewer
regression passed.”

```markdown
<Explain the correction's practical result, current evidence limits, and next actor in plain language.>

Implemented: READY_FOR_REVIEW

- Authority: <exact authoritative brief path>
- Preflight/context reference: <exact readiness, verification revision and context paths>
- Preceding verdict: <verdict>
- Finding/scenario IDs: <complete stable inventories>
- Complete findings and invariant: <findings and broken invariant>
- Influenced sibling surfaces: <contract-implied cases and current evidence or remaining owner>
- Attempts and discarded hypotheses: <exact probes/results and retained partial diff, or none>
- Current scoped diff: <changed paths and concise diff summary>
- Coverage ledger:
  - <row identity> — prior status: <status>; implementation evidence: <command, setup/oracle and result, or none>; Incomplete reason: <reason or none>; next owner/status: <owner and unchanged reviewer status>
- Reviewer reproducer: `<exact command>` — <implementation outcome>
- Owning suite: `<exact command>` — <implementation outcome>
- Broad/aggregate gate: <exact command, run-or-skipped decision, reason, owner and stage, current evidence>
- Remaining reviewer coverage: <unchecked or blocked rows, or none>
- Next: the first outstanding applicable stage and complete ordered remainder
  through fresh independent `task-review-discovery` evidence to a fresh
  `task-acceptance-review` decision
```

Report implementation outcomes separately from reviewer row status. Do not
mark a row accepted, passed, or checked for the corrected bytes unless a fresh
reviewer does so in a separate invocation.

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
approved plan. This also applies to the correction handoff above.

Return a concise human-readable summary, not raw JSON:

```markdown
<Practical change and why it matters; checked scope and material limits; next actor/action or owner decision.>

Implemented: <outcome, READY_FOR_REVIEW, or non-complete status>

- Changed: <paths or none>
- Verified: <exact commands and results>
- AC evidence: <every verification scenario ID mapped to its current command, setup/oracle, and result, or an explicit blocked/unchecked reason and next owner>
- Preflight/context reference: <exact paths of the consumed readiness and context artifacts>
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

### Machine-contracted invocation

When the caller explicitly supplies an output schema or requires a machine-only
response, return exactly one schema-conforming JSON object and no prose. When a
conversational caller asks for a JSON artifact at a path, write and validate the
artifact, then return the human summary with a link to it.

Keep the JSON `summary` useful to a human: describe the implemented outcome and
evidence. Do not prefix it with the skill name, timestamp, packet path, or other
transport metadata unless the supplied schema explicitly requires that text.

For the existing worker-result schema:

- `status`: `complete`, `needs_input`, `blocked`, or `failed`; `complete` is a
  submission, not acceptance. Keep `complete` for successful immediate-review
  submissions; do not add `READY_FOR_REVIEW` or invent a machine field.
- `files_changed`: task-owned repository-relative paths only.
- `verification`: every run or required-but-unrun command with exact outcome.
- `decisions`: local reversible task choices only.
- `questions`: unresolved input/authority issues and whether they block.
- `risks`: residual gaps or skipped stronger evidence.
- `next_action`: one exact route. For immediate review, route to the first
  outstanding applicable conditional stage and the complete ordered remainder
  through fresh independent `task-review-discovery` evidence to the separate
  fresh `task-acceptance-review` decision.

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
