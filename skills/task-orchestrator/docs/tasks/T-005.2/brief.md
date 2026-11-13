# Task Brief: T-005.2 — Validate deferral recording and publish completion

## Outcome

The coordinator can complete one exact accepted candidate after all required
evidence and approved issue recording pass the final controller gate. Repeated
requests or coordinator replacement cannot publish another completion or hide
drift. The assembled local correction/collection/acceptance loop becomes the
implemented interface T-006 documents and later proves inside real sbx.

## Authority and scope

- Authority: [parent](../T-005/brief.md), P-04..06;
  [plan](../../local-harness-orchestration-plan.md), ART-002/007/009/010,
  IF-004, artifact-catalog tracker rule, FLOW-001 steps 5–7, FLOW-002/003 and
  INV-001..008; [owner-confirmed direction](../../direction-single-task-sbx.md).
- Dependency: accepted T-005.1 and its package-local `controller-contract.md`;
  consume the accepted [T-004 interface](../T-004/controller-contract.md) and
  current [registry](../../../../../docs/contracts/task-orchestrator.json).
  T-005.1's handoff is a future prerequisite, not an existing capability claim.
- Allowed: controller/state, directly affected schemas, focused local
  tests/fixtures and instructions/references inside `skills/task-orchestrator/`;
  successor handoff. Test tracker writes belong in disposable task repositories.
- Excludes: migration to JSON, a generic tracker manager, classifier, new
  correction/repetition policy, commit/dependency release, provisioning, parallel
  scheduling, automatic recovery, official-plan edits and active-install refresh.

Preserve approved sbx/YOLO/separate-branch assumptions, frozen model policy and
fresh independent collection and separate acceptance. These assumptions do not
establish containment or reviewer tool isolation. All required stages remain
mandatory. Resolve required skills project-locally; missing installed capability
blocks the applicable profile unless explicit source-guided authority is supplied.

For disposition and recording, use the approved authority in
[correction/disposition notes](../../correction-and-disposition-options.md#existing-skill-and-approved-source-update)
and the current [installed acceptance policy](../../../../../.agents/skills/task-implementation-flow/task-acceptance-review/SKILL.md#approved-deferrals-and-known-issues).
An authorized AI coordinator may record an acceptance-approved bounded deferral
without another human confirmation. Acceptance/discovery do not write the tracker;
requirement/proof waivers and unresolved material-risk decisions remain with the
owner. The notes' JSON proposal and extra repetition-stop proposal are deferred.

### Expected contract impact

Consume T-005.1 ART-009 semantics and the existing candidate/check/collection,
operation and intervention contracts. Materialize ART-010 recording validation,
the completion/publication slice of IF-004 and ART-007, and corresponding ART-002
status. Preserve IF-001/002/003 and INV-001..008. Publish the consolidated exact
T-005 interface as `../T-005/controller-contract.md` for T-006. The designated
registry-updater stage synchronizes delivered contracts only.

## Work and acceptance criteria

**AC-01 — Validate coordinator recording of approved bounded deferrals.**

Use the repository-declared tracker/format, or the active acceptance skill's
default `docs/known-issues.md`. Require no tracker before a deferral exists.
Recording is a coordinator-owned task-tree write with an explicitly declared
in-scope path. It records the unchanged acceptance-approved disposition; it
cannot invent/broaden acceptance or waive proof. Validate the actual stored
record and its binding to the current approved task/review/finding decision,
stable issue ID, provenance and history; a claimed receipt alone is insufficient.
Preserve the cited policy's trigger/consequence/evidence, impact/exposure,
affected consumers, rationale, follow-up and reassessment information. Repeated
recording reuses the same ID/provenance and retains history. Missing, failed,
mismatched or changed recording blocks completion without changing the acceptance
judgment. Do not impose a new universal tracker schema or migrate formats.

**AC-02 — Bound the tracker-only evidence exception.**

An in-scope tracker-only update that records the unchanged approved disposition
may preserve implementation evidence only when the tracker is neither an
implementation input nor a configured-check input. Revalidate its recording
separately at completion. Any evaluated-file or task-input change requires fresh
affected evidence; other scope drift is rejected. The exception cannot mask a
simultaneous code/config/untracked/index/HEAD change, altered disposition, or
unauthorized tracker path. If declaring the path requires an approved input
revision, use the existing safe-boundary revision and invalidation/preflight
rules; do not retroactively widen scope or relabel stale evidence as current.

**AC-03 — Gate the exact current candidate.**

Expose completion through the controller authority boundary. Require terminal
operations, approved scope, current task/policy/candidate identities, complete
required preflight and implementation evidence, passing current checks and fresh
independent collection, a current separately admitted accept decision, no
unresolved blocker, and validated approved-deferral recording when applicable.
Revalidate underlying required records and observed role provenance, including
collector rerun/check evidence, instead of trusting success labels or filenames.
Reject missing/failed/stale/blocked/inconclusive/not-run evidence, same-session
acceptance, unresolved findings, non-accept decisions and live/unknown operation
or check ownership. A required check or material unresolved risk cannot be waived
through a known issue. Invalid requests preserve state/version/count and task
files; retained diagnostics and actual operational blockers remain inspectable.

**AC-04 — Publish completion once and preserve safe interruption.**

Publish ART-007 once, bound to the accepted candidate, decision and required
evidence/recording references, with known issues and truthful limitations.
Completion does not commit, release another task or require either action.
Replay/reload cannot duplicate publication, reset corrections, change findings
or accept a changed candidate. Preserve admitted records, work and history across
interruption before/after record publication and state persistence; a replacement
coordinator can reconcile retained exact records or stop with a precise next
action. Unknown ownership never permits another writer or completion. Persist
unresolved authority/capability/exhaustion through the existing intervention
path for active-chat relay; acknowledgement alone is not authority. This is
conservative bounded reconciliation, not a recovery service or power-loss claim.

**AC-05 — Prove the assembled loop through public behavior.**

In a disposable repository with human-reviewed fixture inputs, use actual public
preflight, implementation, real failing behavior/check or supported review
finding, real code correction, repeated checks, fresh independent collection,
separate acceptance and the final completion operation. Do not seed success for
owned stages. Use distinct scripted observed sessions, real files/Git/checks and
the real gate; scripted actors control responses and edits only. Complete once
without a commit or next task, both with no deferral and with an approved recorded
bounded issue. Exercise missing/failed/tampered recording, allowed tracker-only
recording, tracker-as-input and concurrent relevant drift refusals. Preserve
T-005.1 shared correction/exhaustion evidence and show no completion at exhaustion
with unresolved failure. Reuse current child evidence where valid; this task owns
the additional composed gate/publication proof and affected sibling regressions.

**AC-06 — Give T-006 exact commands and qualification limits.**

Consolidate actual commands/callables, result/state/artifact schemas, acceptance
and recording interfaces, completion eligibility, drift exception, replay and
interruption semantics, status/next actions and local proof references in the
parent controller contract. Update directly affected current references; T-006
owns the full coordinator instruction delivery and separately authorized sbx
pilot. Report inherited baseline failures, skips and unrun checks; deterministic
scripted-role proof establishes neither live sbx/provider/model behavior nor
semantic review quality. Do not declare the owner's first useful sbx proof done.

## Evidence boundaries

Verification-design recommendation: **separate** — tracker recording changes the
task tree between acceptance and completion, and interruption/replay must preserve
the exact decision and candidate. Derive finite positive/refusal and first-write,
retry, changed-state and next-occurrence cases in `verification.md`. Inspect
existing actor/Git/check/state coverage and T-005.1 evidence before adding tests
under installed `testing-discipline`. Existing local filesystem/Git identity,
controller locking/publication and scripted processes provide the decisive
oracle; preflight confirms the accepted dependency interface and installed policy.
No live or reusable-harness feasibility proof is delegated to implementation.

## Execution and handoff

Status: `ready`
Task kind: `executable`
Brief revision: 1
Profile: `guided`

The brief is prepared; execution prerequisites remain. Next: after T-005.1 is
accepted, derive `verification.md`, then ready `preflight.md` through standalone
guided preflight. No orchestrated machine packet is supplied; high-assurance
reconstruction is not required. Confirm the accepted decision contract, current
tracker policy and inherited environment limits in preflight.

Workflow: [shared submission route](../../../../../.agents/skills/README.md#submission-route).
Run the focused owning gate, then the orchestrator suite after targeted success;
apply architecture/contract checks and the aggregate for cross-cutting work.
Maintainability, registry, independent discovery and separate acceptance retain
their stage ownership. Report all skips/failures and obtain applicable approval
for live/expensive checks; this brief authorizes none. After acceptance, the
coordinator closes T-005 beside its plan and hands the consolidated contract and
both accepted child results to T-006. Do not update the official plan or run T-006.

```yaml
agent_tier: strong
reasoning: medium
review: immediate
budget: 24 tool calls / 60 minutes / 80k context
```

### Execution sizing

Policy: project-local `task-brief-designer/references/task-sizing.yaml`,
`default@1`. Estimate: 24 implementation agent calls; 60 minutes; medium
confidence. Policy result: `override_cannot_split_safely`.
`decomposition_override: cannot_split_safely` — exceeds 15 calls and 40 minutes.
Considered separate recording and completion leaves. Recording validation,
tracker-only identity treatment and gate publication share one accepted-candidate
boundary; isolating them requires a provisional receipt contract and repeated
drift/interruption fixtures. A detached integration leaf would repeat the same
gate ownership. Keep this cohesive consumer together after accepted T-005.1.
Residual risk: format-specific fixtures and publication checkpoints may expand
work; budget is a soft checkpoint and material scope changes return to design.
