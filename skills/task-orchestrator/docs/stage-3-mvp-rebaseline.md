# Task Orchestrator: Stage 3 MVP Rebaseline

Status: governing high-level plan for the remaining Stage 3 work
Date: 2026-07-21
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

> Given an approved plan or normalized manifest and a chosen workflow profile,
> process its tasks sequentially through configurable preparation,
> implementation, verification, review, correction, and acceptance steps until
> completion or a genuine operator decision is required.

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

### Immediate gap

S3-08 is implemented but not accepted. Its latest review found that inspection
does not validate the complete immutable attempt record before verification.
This is a bounded correctness and provenance problem, not evidence that the
local run directory needs an adversarial cryptographic trust chain.

The correction should validate the complete supported attempt-record shape and
compare its values with persisted or controller-derived authority before
verification. It should not introduce signatures, external trust anchors, a
new record framework, or more generalized storage machinery.

### Missing user workflow

The following capabilities do not yet exist as an end-to-end path:

- optional task preflight with selectable depth;
- semantic implementation review;
- automatic return of task-local findings to the same worker thread;
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

### Supported MVP step kinds

| Step | Required? | MVP modes | Normal result |
|---|---|---|---|
| task preparation | optional | existing manifest, normalize plan | confirmed task manifest |
| preflight | optional | off, light, standard, strong | ready, blocked, needs input |
| implement | required | configured worker/model/reasoning | complete, needs input, failed |
| verify | optional | off, targeted, targeted plus repository gate | mechanically eligible or findings |
| semantic review | optional | off, standard, strong | accept, changes requested, inconclusive |
| correct | conditional | same-thread resume | revised implementation result |
| accept | required | local side effects off | task accepted and dependencies released |
| advance | required for unattended runs | next ready task | next step or run complete |

Adding or removing these supported steps and changing their modes must require
only run-profile changes. Adding an entirely new step kind may require a new
adapter and is not promised as no-code extensibility in the MVP.

### Flow rules

- A workflow is an ordered, versioned run input and is immutable while a task
  attempt is active.
- The operator can choose a built-in profile or provide a custom sequence of
  supported steps before the run.
- A mid-run workflow revision is allowed only through explicit operator action
  at a safe task boundary. The revision is recorded and never inferred from an
  agent response.
- Omitted steps are recorded as omitted by policy, not silently treated as
  passed.
- Only the review/correction loop may move backward in the MVP. It returns to
  same-thread correction and is bounded by an operator-configured cycle limit.
- `needs_input`, `inconclusive`, exhausted correction cycles, permission
  expansion, and plan/architecture questions stop or escalate according to the
  persisted run profile.
- Ordinary task-local `changes requested` findings may resume automatically
  when the profile authorizes correction and the process/thread checks pass.
- Acceptance derives from the evidence required by the selected profile. If
  semantic review is omitted explicitly, the final report must say so.

### Example profiles

These names and exact serialization are illustrative; the flow-contract task
owns the final versioned representation.

**Fast local**

```text
implement -> targeted verify -> accept -> advance
```

**Reviewed default**

```text
light preflight -> implement -> targeted verify -> semantic review
    -> correct/re-review while changes are requested -> accept -> advance
```

**Strong local**

```text
strong preflight -> implement -> targeted + repository verification
    -> strong independent review -> correct/re-review -> accept -> advance
```

The default should be `reviewed`, but choosing `fast local` must not require a
code edit.

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

- Define a small versioned contract for only the supported MVP step kinds.
- Supply at least `fast local`, `reviewed`, and `strong local` examples.
- Validate required steps, invalid orderings, unsupported modes, duplicate
  acceptance, unbounded loops, and authority-changing revisions.
- Record current step and correction cycle in controller-owned state.
- Keep execution adapters out of this contract slice.

Evaluation: profile tests prove that preflight/review can be added, removed, or
change level without production-code changes, while invalid flows fail before a
worker is launched.

### MVP-3 — Complete recovery and same-thread correction

Goal: retain the useful intent of S3-09/S3-10 while making recovery serve the
workflow runner.

- Reconcile running attempts and implement explicit safe stop.
- Resume only after process absence and thread identity are proven.
- Append correction turns without overwriting earlier evidence.
- Accept structured task-local findings as correction input without allowing
  them to change task scope, flow, or permissions.
- Return a standard step outcome to the workflow runner.

Evaluation: an interrupted fake worker is recovered; a review finding resumes
the recorded thread; a live or ambiguous process never causes a second launch.

### MVP-4 — Add optional preflight and semantic review

Goal: automate the repetitive `preflight -> implement -> review -> fix ->
review` work without making either preflight or review mandatory in every flow.

- Provide bounded adapters for the selected preflight and review actors.
- Use structured reviewer outcomes: `ACCEPT`, `CHANGES_REQUESTED`, and
  `INCONCLUSIVE`.
- Route task-local changes requested to same-thread correction when authorized.
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
- Add an `advance` or equivalent runner action that invokes the next configured
  step/task until completion or a stop outcome.
- Keep atomic acceptance separate from launching the next worker, even if the
  workflow runner immediately follows it with `advance`.

Evaluation: a two-task dependency chain completes end to end with no manually
fabricated ledger state and no duplicate launch; replay after acceptance is a
no-op.

### MVP-6 — Prepare plans and expose the thin operator interface

Goal: make the system usable from an approved planning document rather than
requiring the operator to hand-author every controller JSON file.

- Add a preparation step that converts a supported plan/task document into the
  normalized manifest and reports ambiguities.
- Require one explicit confirmation of the generated run inputs before an
  unattended run; do not silently invent missing scope or permission authority.
- Rewrite the skill around selecting a profile, preparing/confirming inputs,
  starting or continuing the run, and handling genuine escalations.
- Keep raw transcripts and future task briefs out of the normal supervisor
  context.

Evaluation: a representative Markdown plan produces a reviewable manifest,
then starts the same runner used for an already-normalized manifest. Ambiguous
dependencies or scope stop before task execution.

### MVP-7 — Evaluate and pilot

Goal: prove usefulness before resuming optional assurance and commit work.

Run the evaluation ladder below. Fix only defects that prevent the MVP flow or
violate its frozen invariants. Record broader ideas as post-MVP candidates.

## Evaluation ladder

### Gate 1 — Contract and compatibility

- Existing controller state, Git, transport, and verification suites pass.
- Flow-profile validation covers omitted steps, all supported levels, invalid
  orderings, bounded correction cycles, and explicit operator revision.
- Existing `init`, `run-next`, and `inspect` behavior remains available or has a
  documented compatibility route.

### Gate 2 — Synthetic flow

Use fake local actors in a disposable repository to prove:

1. a two-task dependency chain;
2. reviewed flow with one or more `CHANGES_REQUESTED` correction cycles;
3. fast flow with no preflight or semantic-review launch;
4. strong flow selecting the configured modes and actors;
5. interruption followed by same-thread recovery;
6. `INCONCLUSIVE` or permission expansion stopping cleanly; and
7. no duplicate worker, duplicated acceptance, or manual ledger fabrication.

### Gate 3 — Sandbox containment smoke test

On the supported local sandbox backend, demonstrate that an agent command
cannot write outside authorized roots or use disallowed network access. This is
a capability smoke test, not a reason to expand application-level command
blacklists or build a new sandbox.

### Gate 4 — One real local task

With commit, tracker, and network off, run one bounded real task through the
reviewed profile. The operator may confirm inputs once, then should intervene
only for a genuine product/architecture/scope decision.

### Gate 5 — Short real task sequence

Run a small approved plan through at least two dependent tasks. At least one
task should exercise review correction. Confirm that the run can finish and
produce a concise completion report without manual controller commands between
ordinary steps.

Use [execution-brief-pilot-measurement.md](execution-brief-pilot-measurement.md)
as the starting measurement note. At minimum record:

- operator interventions and their reasons;
- completed, stopped, and remaining tasks;
- preflight/review/correction cycles per task;
- false stops and duplicate or unnecessary agent launches;
- elapsed time and model/tool usage by step;
- verification and review gaps; and
- changes recommended before the next pilot.

## MVP exit criteria

The MVP is complete when all of the following are true:

- one confirmed plan or existing manifest can initialize a run;
- the operator can add/remove supported optional steps and select their levels
  without editing production code;
- the default reviewed flow performs implementation, mechanical verification,
  semantic review, same-thread correction, re-review, acceptance, and advance;
- the fast flow proves that omitted preflight/review actors are not launched;
- ordinary task-local review findings do not require manual orchestration;
- genuine product, architecture, scope, and permission questions stop with an
  actionable escalation;
- recovery cannot launch over a live or ambiguous worker;
- acceptance and dependency release require no commit/tracker journal when
  those side effects are off;
- a synthetic two-task run and one real local task pass the evaluation ladder;
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
| S3-08 | Correct narrowly under MVP-1 and obtain fresh acceptance review |
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
  | MVP-3 recovery/resume | High assurance because process ownership, recovery, and duplicate-launch prevention are central |
  | MVP-4 actor adapters/review loop | Guided by default; escalate if process/thread recovery is modified |
  | MVP-5 atomic acceptance/release | High assurance for atomic state, replay, and exact dependency readiness |
  | MVP-6 preparation/interface | Guided, with ambiguity and permission stop cases |
  | MVP-7 pilots | Follow the rebaseline’s evaluation ladder; this is milestone verification, not another design framework |