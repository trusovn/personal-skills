# Direction delta: run one prepared task in sbx

Status: owner-confirmed decisions, with implementation recommendations below.
Date: 2026-10-23.
Source: owner discussion following the T-001 capability-recovery proposal.

## What changed

The immediate goal is a small working task loop. The owner supplies a brief and
a verification document, both reviewed by a human before execution starts.
The system runs preflight, implementation, evidence collection and independent
acceptance. It corrects ordinary failures and asks the owner only when blocked.

The execution target is Codex inside a Docker sbx machine. The owner starts the
tasks from inside it. Agents run in YOLO mode. Outer-system protection and
per-agent tool isolation are not assurance goals for this change. Work is assumed
to happen on a separate branch with no direct effect on main. Branch protection,
PR evaluation and merging are handled separately and are outside this change.
These are owner-supplied operating assumptions, not verified sandbox guarantees.

Parallel work and parallel-writer coordination are deferred. The current design
must not grow a parallel execution framework. Completing a task must not depend
on proving that every unwanted runtime tool has disappeared.

Why: the previous capability qualification placed too much work ahead of the
first usable loop. Prefer a small set of stages with clear entry and exit
conditions and repeatable checks. Keep known limitations visible.

## What remains unchanged

- Agents can make mistakes. An implementation claim is not acceptance evidence.
- Independent review must check whether the task was actually fulfilled.
- Required checks must exercise the claimed behavior; syntax/schema checks alone
  do not prove functional success.
- Scope and verification requirements come from the human-reviewed task inputs.
  An agent must not quietly weaken them to get a pass.
- The previously approved model is `gpt-6.1-sol` at low/medium/high reasoning.
  Unknown correction-context occupancy means use a fresh correction session.
- The existing three unsuccessful correction-and-review cycle limit remains.
  Intervention uses the active coordinator chat.

## Practical impact

The intended normal flow is:

1. Preflight checks that the prepared task can be executed in the actual sbx
   environment, including required tools and dependencies. A real blocker stops
   execution with a precise next action.
2. Implementation uses the brief, verification document, available deterministic
   checks and applicable skills/guides. It submits work and evidence.
3. Independent review collection reruns the relevant deterministic checks and
   examines behavior, requirements and code quality. It publishes evidence and
   findings, without deciding final acceptance.
4. A separate AI acceptance reviewer decides the next action: accept the current
   work, request bounded correction, request missing evidence, or report a blocker.
   The owner is involved only when needed to resolve a blocker.
5. Corrected work is checked and independently reviewed again. Evidence from the
   previous version does not establish that changed work passes.

Deterministic checks establish facts such as command results, required artifacts
and whether evidence refers to current work. Agent review supplies judgments
that tests cannot fully decide, including whether the result meets the brief.
The controller enforces the permitted transition from those facts and decisions.

The first useful proof is one prepared task run through this loop inside sbx,
including a failed check or finding, a correction, and independent acceptance.
PR handling and publication do not belong to that proof. Automatic commit and
dependency-release requirements from the larger plan need a focused scope review;
do not silently make either a prerequisite for this single-task proof.

## Downstream plans to review

- [Original direction](direction-local-harness.md) and
  [orchestration plan](local-harness-orchestration-plan.md): align the immediate
  delivery scope, runtime assumptions and completion boundary with this delta.
  Do not rewrite historical documents merely to record this discussion.
- [T-001 acceptance-02](tasks/T-001/reviews/acceptance-02.md): preserve its truthful
  historical INCONCLUSIVE decision under the old isolation requirements.
  F-01 is not fixed. Its tool-exclusion condition is no longer an entry requirement
  for the newly approved single-task direction. The same applies to outer-system
  permission, inherited-tool and hook-isolation qualification as prerequisites.
- [Capability-recovery proposal](tasks/T-001/capability-recovery-proposal.md) and
  [path to T-002](tasks/T-001/path-to-unblock-T-002.md): preserve as prior proposals;
  their control-first sequence does not govern this revised delivery route.
- T-002 preparation: recheck the smallest state/transition contract against this
  direction. Actual task execution and required checks in sbx still need proof
  when connected. Do not retain the six old capability-evidence gaps as an
  undifferentiated entry gate. This delta alone is not a T-002 acceptance report.

## Decision status and threads to retain

Confirmed: human-reviewed inputs; sbx execution target; YOLO actors; one task at
a time; independent collection and separate AI acceptance; owner involvement only
when blocked; outer protection, parallel execution and PR/main handling deferred.

Recommendations for the smallest implementation:

- Bind check and review results to the exact task inputs and files evaluated.
  A simple revision identifier is sufficient if it reliably covers those files.
- Keep a small persisted status: current stage, attempt, evidence locations and
  next action. On interruption, preserve work and stop before retrying if the
  previous operation might still be running. No automatic crash-recovery service
  is required for the first proof.
- Distinguish a product failure from missing/broken test infrastructure and an
  ambiguous requirement. Route each to the actor that can fix it; missing evidence
  is not a pass. Apply the existing correction limit instead of retrying forever.
- Review collection may reuse applicable independent review skills. The owner's
  name `review-collect` describes the role here; no installation or callable
  command with that name has been established by this discussion.

Deferred threads: additional code-quality tools/guides; automatic commit policy;
multi-task dependency release; sbx startup/persistence and resume details; branch
and PR integration; broader containment and tool restrictions; parallel work.
These are later targeted work, not reasons to rebuild a general framework now.

This document records direction only. It neither provisions sbx nor changes
runtime configuration, production code, installed skills or existing reports.
