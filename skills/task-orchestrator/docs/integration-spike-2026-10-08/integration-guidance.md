# Integration guidance from the task-flow spike

This document concerns the code-guided direction in
`../code-guided-orchestration.brief.md`. It does not revise that brief or the
existing delivery plans. `run_spike.py` is a bounded experiment, not an executor
ready for unattended use.

## Entry and installation

Resolve the active project-local installation first. The development installer
uses nested paths such as
`.agents/skills/task-implementation-flow/task-preflight/SKILL.md`. Do not assume
all installed skills are immediate children of `.agents/skills/`.

An installation can differ from its source: this repository's local implementer
and acceptance copies lagged the requested source. The experiment installed the
source into its fixture and recorded installed file hashes. Do not silently
replace an active installation during a run.

The initial executor should take approved executable packages. Brief design and
verification design belong to preparation. They were included here to test all
seven skills, not to expand the first executor's scope. Reject composite parents,
legacy direct briefs, unresolved design blocks, and unavailable dependencies.

Keep task-map planning authority, structural task index, and runtime state
separate. Do not create a structural index merely to run one explicit leaf.

## Stage invocation contract

Give each actor explicit values, not a generic instruction to follow the flow:

- run, task, stage, attempt, and actor-session IDs;
- exact installed skill entry point and retained installation identity;
- profile, repository root, authority, policy, dependency source, and task package;
- input artifact paths and independently captured identities;
- writable paths, canonical output artifact, and runtime result path;
- authorized command records and check ownership;
- output schema when the stage supports a machine contract;
- preceding review report and complete coverage ledger for correction.

Launch each actor in a new bounded session except an explicitly resumed
implementation correction. A reviewer must not share production authorship with
the implementer. Record the actual transport session ID and supplied runtime
model/effort. Launch metadata is not proof of server-side model behavior.

The experiment used `gpt-5.6-terra` with `medium` effort. Literal `terra-medium`
and `terra` were not accepted by this account. Resolve display labels through the
host catalog rather than concatenating model and effort into a model identifier.

## Stage order and admission

| Operation | Required input | Successful output | Mechanical advancement rule |
|---|---|---|---|
| Brief preparation | Approved task authority and sizing/layout policy | Packaged executable `brief.md`, `ready_for_preflight` | Confirm executable leaf and sizing disposition; never launch a parent |
| Optional verification preparation | Executable brief | `verification.md`, `ready`, correct `Source brief:` | Bind derived guidance to the exact brief; preserve scenario IDs |
| Standalone preflight | Approved leaf, policy, dependencies, applicable verification | Canonical `preflight.md`, `ready` | Validate readiness plus identities, scope, commands, and attributed packet write |
| Implementation | Fresh ready packet, schema, policy | Schema-valid worker `complete` result | Treat it as submission; validate scope, task ID, effects, and check evidence |
| Deterministic checks | Current implementation bytes, authorized commands | Exit and output evidence | A failed command stops or routes correction; a green command is not semantic acceptance |
| Maintainability, when required | Current bytes and required architecture evidence | Fresh independent `ACCEPT` report | Bind verdict to current production/test/executable-contract identity |
| Registry sync, when applicable | Approved implementation and current registry | `UPDATED` or justified `NO_UPDATE_NEEDED` | Restrict effects to registry and stale explanatory references; validate registry |
| Functional acceptance, when required | Current scope, packet, worker, prior reviews, policy | Fresh independent `ACCEPT` report | Validate all required coverage and freshness; only then allow controller acceptance |
| Controller acceptance | Complete current evidence set | Accepted runtime task state | Release dependencies without rewriting plans or committing implementation implicitly |

Markdown labels were parsed only as experiment gates. That is not a safe general
protocol: templates allow code fences, inline backticks, prose, tables, and
noncanonical route explanations. Add an explicit structured sidecar while
preserving useful human artifacts. Do not use an AI to repair or interpret an
invalid sidecar.

## Effect and freshness validation

Capture content and repository state before each actor, then compare after it.
Check index and worktree separately; status text alone misses same-status edits.
Include absent/deleted states. Preserve `HEAD`, task authority, policy,
dependencies, and installed skill/helper bytes unless the selected operation
explicitly allows a change.

Preflight and review artifacts are expected writes. Allow only the exact
allocated path; do not exempt the whole task package. An acceptance report does
not authenticate itself. Allocate the next unused numbered report and preserve
prior reports. Do not require canonical artifacts to be ignored by Git.

Keep the immutable invocation baseline and each stage's current input identity
distinct. Implementation legitimately changes task files; registry sync
legitimately changes references; review reports legitimately add evidence.
Acceptance must classify those effects, rather than demanding that the worktree
still equal the original preflight snapshot. No unexplained change is allowed.

Use a manifest with exact paths rather than default untracked-directory
aggregation as a content identity. The fixture tracks a placeholder in the task
and review directories so default short status exposes individual artifacts.
The executor must also work without those placeholders.

Check commands supplied by an actor against the approved permission envelope
before execution. Store argv, cwd, environment, start/end, exit, output identity,
and covered cases. Separate producer claims from controller checks and independent
review evidence. A registry validator establishes structure/path consistency;
it cannot establish the public function's behavior.

## Routing and invalidation

| Result or effect | Owner / next operation | Evidence invalidated |
|---|---|---|
| Current-state readiness/freshness failure | Preflight, or operator for changed ownership | Ready packet and downstream claims |
| Task authority or permitted scope defect | Brief/design owner or operator | Affected preparation and downstream evidence |
| Maintainability in-scope finding | Implementation correction, gates, fresh maintainability | Prior maintainability; functional review of older bytes |
| Functional production/test/executable-contract finding | Implementation correction, gates, applicable fresh maintainability, registry sync, fresh acceptance | Both affected semantic verdicts and registry consistency claims |
| Reference-only finding | Registry updater, then fresh acceptance | Reference consistency and acceptance; retain maintainability only if relevant bytes are unchanged |
| Planned/current semantic mismatch | Planning owner | Stop; updater cannot redefine the planned ID |
| Required gate unavailable / review inconclusive | Named capability, environment, or authority owner | No advancement; no invented successful result |
| Interrupted or uncertain actor process | Transport recovery / operator | No relaunch until sole-writer ownership is established |

Use observed file effects to corroborate correction class. Free-text
`next_action` is a claim, not transition authority. The controller selects the
next stage from the pinned flow and validated result. Bound retries with explicit
run authority. Do not reuse a reviewing session to accept corrected bytes.

## Instrumentation ownership

Record launcher configuration and transport session/usage events independently
of actor prose. Feed trusted model, effort, and session metadata through the
existing runtime-context contract. The shared collector currently targets a
bounded implementer invocation; do not assume installing it instruments every
stage. Explicitly select its applicability and lifecycle owner. When the
controller owns collection, begin after entry checks and finish on a truthful
submission/interruption outcome; do not also ask the actor to start a duplicate
run. Preserve optional skip versus mandatory blocking according to run policy.
Validate real manifests and retained snapshot/check records, not just helper
availability. The experiment retained transport telemetry but did not exercise
that shared lifecycle.

## Version and upgrade boundary

Record separate identities for workflow content, protocol/flow contract, runtime
adapter, shared helpers, schemas, sizing policy, and installation layout. Retain
the actual input bytes for resume; hashes alone cannot restore an old version.
Do not change the existing fingerprint algorithm implicitly to solve this.

Before adopting an upgrade, run local contract tests and an authorized live
qualification. Required qualification includes success, justified skip,
implementation correction, reference-only correction, blocked/inconclusive
outcome, expected artifact write, interrupted-process recovery, and pinned-version
resume. This one-task experiment cannot establish all those paths.
