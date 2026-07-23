# Task Orchestrator: Stage 3 MVP Rebaseline

Status: governing high-level plan for the remaining Stage 3 work
Date: 2026-07-21
Last updated: 2026-07-23
Historical plan: [stage-3-plan.md](history/stage-3-plan.md)
Mid-stage evidence: [stage-3-mid-review.md](history/stage-3-mid-review.md)
Parent direction: [direction.md](direction.md)

## Purpose of this document

This document answers four questions:

1. Where is the implementation now?
2. What is the shortest path from here to a useful local MVP?
3. Which evaluations prove that the MVP works for the intended task flow?
4. Which capabilities remain deliberately deferred until after the MVP?

It rebaselines the high-level plan without rewriting the original Stage 3 plan
or any existing task brief. The original plan remains implementation history.
Existing briefs for unfinished tasks must be actualized in separate sessions
before they are executed; where a brief conflicts with this document, do not
silently follow the old brief.

## Decision summary

The controller is a useful mechanical foundation, but the project has optimized
for record integrity and optional commit recovery before proving the workflow
that motivated it. The remaining work is reordered around this local MVP:

> Given an approved plan or normalized manifest, prepare and confirm the run
> inputs, then use a chosen workflow profile to process its tasks sequentially
> through preflight, implementation, optional verification and review,
> correction, and acceptance until completion or a genuine operator decision
> is required.

The MVP is not an adversarial multi-tenant service. It runs on the operator's
local machine, potentially inside a Docker or equivalent sandbox. The sandbox
is the principal containment boundary. Controller records protect against LLM
mistakes, stale state, crashes, duplicate work, and accidental corruption—not a
malicious actor who can coherently rewrite the trusted run directory.

## Current position

### Implemented foundation

- Stage 1 and Stage 2 established the safe Codex transport, immutable run
  inputs, deterministic task selection, one-worker ownership, durable attempts,
  and independent Git closure evidence.
- S3-01 through S3-07 added the local verification boundary, pure state and Git
  modules, Stage 3 record contracts, verification planning, and sandboxed
  verification execution.
- S3-08 added `inspect`, controller-run verification, Git-drift detection,
  replay of already published verification, and mechanical closure decisions.
- The public controller currently exposes `init`, `run-next`, and `inspect`.

### Closed inspection gap

S3-08 is implemented and accepted. The mid-stage review found that inspection
did not validate the complete immutable attempt record before verification.
The bounded correction now validates the supported record and its
controller-owned authority without introducing signatures, external trust
anchors, a new record framework, or generalized storage machinery. A fresh
guided acceptance review passed; the result is recorded in
[S3-08-result.md](history/stage-3-tasks/S3-08-result.md).

### Missing user workflow

The following capabilities do not yet exist as an end-to-end path:

- optional task preflight with selectable depth;
- semantic implementation review;
- automatic return of task-local findings to a continuing or freshly handed-off
  implementation session according to the persisted context threshold;
- repeated review/correction until accepted or escalation is required;
- side-effect-free task acceptance and dependency release;
- continuing to the next task without manual orchestration commands;
- preparing a confirmed manifest from a high-level task document; and
- a thin skill or command that runs the configured flow.

Mechanical inspection currently records `semantic_review: not_collected` but
can still describe a result as accepted. Until the flow explicitly omits or
completes semantic review, the accurate term is **mechanically eligible**, not
semantically accepted.

## Local trust and containment model

### Trusted

- the operator and local operating-system account;
- the repository and approved task documents at run start;
- the external run directory and controller code;
- configured local agent binaries and sandbox backend.

### In scope

- an LLM inventing authority, commands, paths, or completion claims;
- an LLM changing unrelated repository content;
- accidental duplicate workers or controller commands;
- a worker crash, timeout, interruption, or missing result;
- stale or contradictory controller artifacts;
- resuming the wrong or still-running process;
- accepting a task without the evidence required by the selected flow.

### Out of scope for the MVP

- a malicious user or process with write access to the run directory;
- signed records, an external trust anchor, or hostile forensic audit;
- multi-user, remote, or distributed controller operation;
- parallel writers or parallel worktrees; and
- building a new container, microVM, or sandbox product.

Digests remain useful for identity, stale-data detection, replay safety, and
accidental corruption. They must not be expanded merely to simulate protection
from a malicious actor who already controls all local record bytes.

## Configurable workflow model

### Separation of responsibilities

The design should have three small layers:

1. **Controller:** owns one-task-at-a-time state, process lifecycle, persisted
   authority, repository observations, and acceptance transitions.
2. **Workflow runner:** reads the persisted flow, invokes the next valid step,
   records its structured outcome, and follows the configured ordinary route.
3. **Step actor:** performs one bounded action such as preflight,
   implementation, verification, or semantic review. It cannot mutate the flow
   definition, select another task, or expand permissions.

This is a small configurable pipeline, not a general workflow engine.

### Supported MVP run steps

| Step | Required? | MVP modes | Normal result |
|---|---|---|---|
| preflight | optional | off, light, standard, strong | ready, blocked, needs input |
| implement | required | configured worker/model/reasoning | complete, needs input, failed |
| verify | optional | off, targeted, targeted plus repository gate | mechanically eligible or findings |
| semantic review | optional | off, standard, strong | accept, changes requested, inconclusive |
| accept | required | local side effects off | task accepted and dependencies released |

Plan preparation is a pre-run bootstrap operation, not an in-run step. It
creates the manifest and other authority that the operator confirms before the
run is initialized. Mechanical inspection of records, repository identity, and
allowed scope is always on; `verify: off` disables configured test-command
execution, not controller inspection.

Correction and advance are bounded runner transitions rather than freely
orderable profile steps. `CHANGES_REQUESTED` may trigger correction, and
acceptance may trigger advance, only under the persisted flow rules.

Adding or removing supported optional actor steps and changing their modes must
require only run-profile changes. Adding an entirely new actor step kind may
require a new adapter and is not promised as no-code extensibility in the MVP.

### Flow rules

- A workflow is an ordered, versioned run input and is immutable while a task
  attempt is active.
- The operator can choose a built-in profile or provide a custom sequence of
  supported actor steps within the valid phase ordering before the run.
- A mid-run workflow revision is allowed only through explicit operator action
  at a safe task boundary. The revision is recorded and never inferred from an
  agent response.
- Omitted steps are recorded as omitted by policy, not silently treated as
  passed.
- Only the review/correction loop may move backward in the MVP. It returns to
  correction and is bounded by an operator-configured cycle limit.
- `needs_input`, `inconclusive`, exhausted correction cycles, permission
  expansion, and plan/architecture questions stop or escalate according to the
  persisted run profile.
- Ordinary task-local `changes requested` findings may resume automatically
  when the profile authorizes correction and the process/session checks pass.
- Acceptance always requires a complete implementation result plus valid
  controller records, repository identity, and allowed-scope evidence. It also
  requires the configured command-verification and semantic-review evidence
  when those steps are enabled. If either is omitted explicitly, the final
  report must say so.
- Pre-MVP run directories, schemas, and CLI behavior have no compatibility or
  migration guarantee. This is the first usable product version; preserve the
  implemented safety invariants and useful tests rather than legacy interfaces.

### Example profiles

These names and exact serialization are illustrative; the flow-contract task
owns the final versioned representation.

**Fast local**

```text
implement -> targeted verify -> accept
    runner advances after acceptance
```

**Reviewed default**

```text
light preflight -> implement -> targeted verify -> semantic review
    -> correct/fresh re-review while changes are requested -> accept
    runner advances after acceptance
```

**Strong local**

```text
strong preflight -> implement -> targeted + repository verification
    -> strong independent review -> correct/fresh re-review -> accept
    runner advances after acceptance
```

The default should be `reviewed`, but choosing `fast local` must not require a
code edit.

### Actor, session, and evidence defaults

- Concrete preflight and semantic-review actors remain an MVP-4 actualization
  decision. They must support the structured outcomes and permission boundaries
  defined by the flow contract.
- Actor levels use `gpt-5.6-sol` for the MVP: `light` uses low reasoning,
  `standard` uses medium reasoning, and `strong` uses high reasoning. Semantic
  review currently exposes only `standard` and `strong`.
- Every semantic review and re-review starts in a fresh read-only session.
  It receives a compact controller-owned handoff containing prior findings and
  their status, implementation and correction summaries, changed areas,
  commands already run, their outcomes, and durable evidence references.
- The controller carries that cumulative handoff from reviewer to correction
  implementer and onward to the next reviewer, updating finding status and
  evidence references after each step.
- A fresh reviewer may reuse prior expensive evidence when the correction did
  not touch the behavior, module, dependency, shared contract, or environment
  that evidence covered. It reruns focused checks for the correction and any
  invalidated evidence. A repository-wide or other expensive regression gate
  is repeated only when the corrected behavior is materially important or the
  change can plausibly affect that gate. The reviewer records what it reused,
  reran, or skipped and why.
- For correction, reuse the implementation session only when its latest
  recorded context use is below 50% of the model context window. At 50% or
  above, or when context use is unavailable, start a fresh implementation
  session with the same compact handoff. This is a hard MVP rule; making the
  threshold configurable is a later tuning option.
- Raw transcripts stay in durable storage. Actors and the workflow runner
  exchange versioned structured outcomes and artifact references rather than
  copying transcripts between contexts.

### Non-configurable invariants

Flow flexibility must not weaken these controller rules:

- one selected task and one active implementation worker at a time;
- workers and reviewers do not change the controller ledger or workflow;
- workers do not commit unless a later post-MVP commit step is explicitly
  introduced;
- the effective sandbox and permission envelope is persisted before launch;
- no automatic permission expansion or destructive cleanup;
- task dependencies and operator-authorized task range remain controller-owned;
- recovery proves the previous process absent before resume; and
- every loop is bounded and has an explicit stop route.

## Shortest path to MVP

The following are high-level implementation increments, not executable task
briefs. Separate task-design sessions should translate them into updated or new
briefs with focused acceptance criteria.

<!-- Historic - already done:

### MVP-1 — Close the inspection correctness gap

Goal: make the current S3-08 inspection boundary internally coherent under the
trusted-local-run model.

- Validate the complete supported attempt record before verification.
- Compare operational values with persisted policy, adapter state, prompt,
  baseline, and selected task where those values are authoritative.
- Preserve the existing closure, worker-result, and workspace identity checks.
- Rename or clearly expose the current decision as mechanical eligibility.
- Obtain a fresh acceptance review for the bounded correction.

Evaluation: the current tampered-model probe fails before verification; clean
inspection and replay continue to pass; no new trust-chain abstraction appears. -->

### MVP-2 — Freeze the configurable flow contract

Goal: represent the ordered step list, modes, actors, correction limit, and
stop/escalation behavior as persisted run authority.

- Define a small versioned contract for only the supported MVP actor steps,
  controller transitions, and compact handoff/outcome envelope.
- Supply at least `fast local`, `reviewed`, and `strong local` examples.
- Validate required steps, invalid orderings, unsupported modes, duplicate
  acceptance, unbounded loops, and authority-changing revisions.
- Record current step and correction cycle in controller-owned state.
- Apply the approved model/reasoning mapping and implementation-session
  threshold without selecting concrete preflight or review actor adapters.
- Keep execution adapters out of this contract slice.

Evaluation: profile tests prove that preflight/review can be added, removed, or
change level without production-code changes, while invalid flows fail before a
worker is launched.

### MVP-3 — Complete recovery and session-aware correction

Goal: retain the useful intent of S3-09/S3-10 while making recovery serve the
workflow runner.

- Reconcile running attempts and implement explicit safe stop.
- Resume an existing thread only after process absence and thread identity are
  proven.
- Append correction turns without overwriting earlier evidence, or start a
  fresh implementation session with the compact handoff when the context rule
  requires it.
- Accept structured task-local findings as correction input without allowing
  them to change task scope, flow, or permissions.
- Return a standard step outcome to the workflow runner.

Evaluation: an interrupted fake worker is recovered; a review finding resumes
the recorded thread below the context threshold and starts a handed-off session
at or above it; a live or ambiguous process never causes a second launch.

### MVP-4 — Add optional preflight and semantic review

Goal: automate the repetitive `preflight -> implement -> review -> fix ->
review` work without making either preflight or review mandatory in every flow.

- Provide bounded adapters for the selected preflight and review actors.
- Use structured reviewer outcomes: `ACCEPT`, `CHANGES_REQUESTED`, and
  `INCONCLUSIVE`.
- Route task-local changes requested to session-aware correction when
  authorized.
- Start every review in a fresh read-only session, carrying prior findings and
  verification evidence through the compact handoff. Reuse or rerun checks
  according to evidence invalidation and material risk rather than blindly
  repeating every expensive gate.
- Escalate product, architecture, permission, scope, or contradictory-review
  questions instead of asking the implementation worker to guess.
- Preserve the distinction between mechanical evidence and semantic judgment.

Evaluation: the reviewed profile completes one task after at least one injected
`CHANGES_REQUESTED` cycle; the fast profile launches neither preflight nor
review; an inconclusive review stops with an actionable report.

### MVP-5 — Simplify acceptance, release, and advance

Goal: finish a task and continue without the external-side-effect journal that
was designed for commits and trackers.

- With commit and tracker modes off, revalidate the evidence required by the
  chosen flow and accept exactly one task in one atomic ledger update.
- Recompute dependency readiness in the same update.
- Keep acceptance free of Git history, tracker, and external writes.
- Add the runner-owned advance transition that invokes the next configured
  step/task until completion or a stop outcome.
- Keep atomic acceptance separate from launching the next worker, even if the
  workflow runner immediately follows it with `advance`.

Evaluation: a two-task dependency chain completes end to end with no manually
fabricated ledger state and no duplicate launch; replay after acceptance is a
no-op.

### MVP-6 — Prepare plans and expose the thin operator interface

Goal: make the system usable from an approved planning document rather than
requiring the operator to hand-author every controller JSON file.

- Add a pre-run preparation operation that converts a supported plan/task
  document into the normalized manifest and reports ambiguities.
- Require one explicit confirmation of the generated run inputs before an
  unattended run; do not silently invent missing scope or permission authority.
- Rewrite the skill around selecting a profile, preparing/confirming inputs,
  starting or continuing the run, and handling genuine escalations.
- Use the same versioned outcome and handoff envelope across preparation,
  actors, the runner, and the completion report so data moves by stable
  controller-owned artifacts rather than component-specific transcript parsing.
- Keep raw transcripts and future task briefs out of the normal supervisor
  context.

Evaluation: a representative Markdown plan produces a reviewable manifest,
then starts the same runner used for an already-normalized manifest. Ambiguous
dependencies or scope stop before task execution.

### MVP-7 — Evaluate and pilot

Goal: prove usefulness before resuming optional assurance and commit work.

Run required Gates 1–4 below. Gate 5 is the next confidence follow-on after MVP
exit. Fix only defects that prevent the MVP flow or violate its frozen
invariants. Record broader ideas as post-MVP candidates.
Keep the measurement mechanism small: retain raw session logs and durable
controller artifacts, then derive one versioned run-summary JSON file and one
short human-readable report after a run. Do not add a database, live telemetry
service, dashboard, or a second event pipeline for the MVP. Each session and
artifact must be attributable by run, task, attempt or correction cycle, step,
and actor role.

## Evaluation ladder

### Gate 1 — Contract and compatibility

- Existing controller state, Git, transport, and verification suites pass.
- Flow-profile validation covers omitted steps, all supported levels, invalid
  orderings, bounded correction cycles, and explicit operator revision.
- No legacy CLI or run-directory compatibility is required. Replacements retain
  the relevant controller safety invariants and have a documented operator
  route.

### Gate 2 — Synthetic flow

Use fake local actors in a disposable repository to prove:

1. a two-task dependency chain;
2. reviewed flow with one or more `CHANGES_REQUESTED` correction cycles,
   fresh re-review, and explicit reused/rerun verification evidence;
3. fast flow with no preflight or semantic-review launch;
4. strong flow selecting the configured modes and actors;
5. interruption followed by same-thread recovery;
6. correction below the context threshold reusing the implementation session,
   and correction at or above it starting a handed-off session;
7. `INCONCLUSIVE` or permission expansion stopping cleanly; and
8. no duplicate worker, duplicated acceptance, or manual ledger fabrication.

### Gate 3 — Sandbox containment smoke test

On the supported local sandbox backend, demonstrate that an agent command
cannot write outside authorized roots or use disallowed network access. This is
a capability smoke test, not a reason to expand application-level command
blacklists or build a new sandbox. One allowed in-root write, one denied
out-of-root write, and one denied network probe are sufficient for the MVP.

### Gate 4 — One real local task

With commit, tracker, and network off, run one bounded real task through the
reviewed profile. The operator may confirm inputs once, then should intervene
only for a genuine product/architecture/scope decision.

### Gate 5 — Short real task sequence follow-on

Run a small approved plan through at least two dependent tasks. At least one
task should exercise review correction. Confirm that the run can finish and
produce a concise completion report without manual controller commands between
ordinary steps. This is the next confidence gate after MVP exit, not a blocker
for the first useful MVP.

Preserve the raw session logs as diagnostic evidence, but do not make them the
only metrics interface. Correlating them across actors and retries should not
require rereading transcripts. The derived run summary should record:

- operator interventions and their reasons;
- completed, stopped, and remaining tasks;
- preflight/review/correction cycles per task;
- false stops and duplicate or unnecessary agent launches;
- elapsed time, actor, model, reasoning level, and available token/context/tool
  usage by step;
- verification commands rerun, reused, or skipped and why;
- verification and review gaps;
- changes recommended before the next pilot.

Use [execution-brief-pilot-measurement.md](execution-brief-pilot-measurement.md)
only as an additional source for comparing task-brief authoring sessions; it
does not replace the run summary.

## MVP exit criteria

The MVP is complete when all of the following are true:

- one confirmed plan or existing manifest can initialize a run;
- the operator can add/remove supported optional steps and select their levels
  without editing production code;
- the default reviewed flow performs implementation, mechanical verification,
  semantic review, session-aware correction, fresh re-review, acceptance, and
  advance;
- the fast flow proves that omitted preflight/review actors are not launched;
- ordinary task-local review findings do not require manual orchestration;
- genuine product, architecture, scope, and permission questions stop with an
  actionable escalation;
- recovery cannot launch over a live or ambiguous worker;
- acceptance and dependency release require no commit/tracker journal when
  those side effects are off;
- a synthetic two-task run and one real local task pass required Gates 1–4;
- the operator interface reports current position, next step, completed work,
  and the reason for any stop; and
- the skill documents the runnable flow rather than the historical manual
  checklist.

## Existing Stage 3 task disposition

This table is guidance for later task-actualization sessions; it does not edit
or silently redefine the existing task briefs.

| Existing work | Rebaseline disposition |
|---|---|
| S3-01 through S3-07 | Preserve implemented behavior; freeze further hardening unless an MVP evaluation exposes a defect |
| S3-08 | Complete and accepted under MVP-1; preserve the accepted behavior |
| S3-09 and S3-10 | Retain, but shape outputs for the configurable workflow and correction loop |
| S3-11 and S3-12 | Replace the mode-off prepared-operation sequence with MVP-5 simple atomic acceptance/release |
| S3-13A, S3-13B, S3-14, S3-15 | Defer as optional post-MVP controller-owned commit/finalization work |
| S3-16 | Replace its closure target with the MVP evaluation and truthful handoff described here |
| S3-T1, S3-T2, S3-T3 | Keep deferred until a real pilot demonstrates a tracker need |
| Stage 4 thin skill | Pull the minimum operator/runner interface into MVP-6 |
| Stage 5 pilot | Pull synthetic and real pilots into MVP-7 |

## Explicitly deferred beyond MVP

- controller-owned exact-path commits and commit crash reconciliation;
- human tracker mutation and tracker recovery;
- adversarial tamper resistance, signatures, and external record anchoring;
- arbitrary third-party workflow steps or a plugin SDK;
- distributed execution, remote workers, and multi-user access;
- parallel tasks or parallel worktrees;
- automatic permission expansion or destructive recovery;
- a new sandbox implementation when an existing local/Docker boundary is
  sufficient; and
- optimization work unsupported by pilot measurements.

## Stop and replan conditions

Stop task actualization or implementation if:

- configurable steps require arbitrary code execution or a general workflow
  language rather than the closed MVP step set;
- the chosen semantic reviewer cannot return stable structured outcomes;
- plan normalization would require inventing unresolved architecture, scope, or
  permission decisions;
- the local sandbox cannot enforce the minimum filesystem/process boundary;
- recovery cannot distinguish a live/ambiguous worker from an absent one;
- the first real pilot shows that exact path scope or another frozen input
  contract prevents ordinary work; or
- optional commit/tracker behavior is becoming a prerequisite before the
  side-effect-free flow is proven.

When one of these occurs, preserve the evidence, update this high-level plan or
its successor, and only then actualize the affected task briefs.

## Suggested assurance level

  | Increment | Recommended treatment |
  |---|---|
  | MVP-2 flow contract | Guided, strong reasoning, immediate independent review |
  | MVP-3 recovery/correction | High assurance because process ownership, recovery, context-threshold handoff, and duplicate-launch prevention are central |
  | MVP-4 actor adapters/review loop | Guided by default; escalate if process/thread recovery is modified |
  | MVP-5 atomic acceptance/release | High assurance for atomic state, replay, and exact dependency readiness |
  | MVP-6 preparation/interface | Guided, with ambiguity and permission stop cases |
  | MVP-7 pilots | Follow the rebaseline’s evaluation ladder; this is milestone verification, not another design framework |
