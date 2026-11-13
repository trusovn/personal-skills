# Task Brief: T-005.1 — Admit separate acceptance and route recovery

## Outcome

The coordinator receives a current, independently produced acceptance decision
and an authorized next action. A review finding can cause real correction and
fresh evidence; missing proof returns to its evidence owner. An accept decision
makes the candidate eligible for T-005.2's completion gate. It does not complete
the task or write the known-issue tracker.

## Authority and scope

- Authority: [parent](../T-005/brief.md), P-01..03 and P-06;
  [plan](../../local-harness-orchestration-plan.md), ART-009, IF-003,
  FLOW-001 steps 5–6, FLOW-002/003 and INV-001..008;
  [owner-confirmed direction](../../direction-single-task-sbx.md).
- Dependencies: accepted T-004, its [closure](../T-004/result.md),
  [controller contract](../T-004/controller-contract.md), and both child
  acceptances cited in the parent. Use the current
  [registry](../../../../../docs/contracts/task-orchestrator.json) to resolve
  implemented lifecycle, identity, checks, collection and correction contracts.
- Allowed: controller/state, actor-result and directly affected schemas,
  focused tests/fixtures, acceptance assignment/prompt, and affected references
  inside `skills/task-orchestrator/`; task-local successor contract.
- Excludes: completion/publication, tracker writes or migration, commits,
  dependency release, new stop/budget policies, provisioning, automatic recovery,
  official-plan edits, live checks and installation refresh.

Use the approved single-task sbx/YOLO/separate-branch assumptions, frozen model
mapping and required role sequence. Review is an edit-prohibited assignment,
not enforced filesystem isolation. Resolve installed skills project-locally;
source presence is not an available skill. Preserve separately applicable
maintainability, registry, discovery and acceptance roles. An unavailable required
role needs explicit source-guided review authority or blocks that profile.

Disposition authority is the approved policy in
[correction/disposition notes](../../correction-and-disposition-options.md#existing-skill-and-approved-source-update)
and the current [installed acceptance skill](../../../../../.agents/skills/task-implementation-flow/task-acceptance-review/SKILL.md#contextual-disposition-and-coordinator-owned-deferrals).
No new direction decision is needed. Recommendations for a classifier, JSON
tracker or extra repetition-stop rule are not requirements.

### Expected contract impact

Materialize ART-009 and IF-003 semantic acceptance by extending the existing
observe → admit → publish path. Extend ART-002 with current decision,
dispositions and routes; preserve ART-003/005/006 and IF-001/002 accounting.
Publish exact schema/API/artifact and replay semantics in
`controller-contract.md` in this package for T-005.2. The registry-updater stage
records only this implemented slice; completion remains absent.

## Work and acceptance criteria

**AC-01 — Launch a fresh separate acceptance reviewer.**

After current passed checks and complete independent collection, reserve and
launch acceptance through the existing controller/adapter. Supply frozen task
and verification authority, current candidate/check/collection records, runtime
limitations, applicable conditional review evidence, findings/dispositions and
known-issue history when present. The reviewer consumes collection; it does not
implement, take over collection or write the tracker. Bind the decision to the
exact assignment, task, operation, input/policy/flow, candidate and explicitly
adapter-observed session. Reject wrong roles, invented provenance, malformed or
nonterminal output, and any implementation/correction or collector session reused
as acceptance. Fresh assignments use fresh sessions.

**AC-02 — Admit a decision only against current required evidence.**

Validate ART-009 through the single existing admission path. Distinguish accept,
correction, missing evidence and blocker with rationale and referenced evidence.
Check actual retained candidate/check/collection artifacts and provenance, not
only reviewer prose or ledger labels. Reject stale or replaced records and
relevant tracked/untracked/configuration/index/HEAD/task-input changes, including
drift during acceptance. Required missing, failed, blocked, not-run or inconclusive
evidence cannot become eligible through an accept claim or a weaker profile.
Inconsistent claims cannot erase failures, findings or required stages.

**AC-03 — Retain justified finding dispositions.**

Preserve stable IDs and prior history, and account for retained unresolved
findings even when a later collector omits them. Decisions distinguish confirmed
blocking failures, acceptance-approved bounded known issues, observations and
unresolved evidence. Apply the cited acceptance policy: missing required proof
is not a defect deferral; preference alone creates no correction obligation;
bounded deferrals waive no AC, required check or material unresolved risk.
Retain acceptance provenance, rationale, compatible consumers, follow-up and
reassessment conditions for approved deferrals. Only the coordinator later records
them. Unchanged relevant evidence/exposure preserves an approved disposition;
reopening needs new relevant evidence or changed exposure and its reason.

**AC-04 — Route recovery within existing authority and budget.**

A supported blocking review decision authorizes bounded `review_findings`
correction. Missing evidence routes to checks/collection as appropriate without
an implementation launch or correction charge. Product failures, broken
infrastructure, stale evidence and missing authority/capability remain distinct.
Use inherited repair authority/fresh-preflight rules and the active-chat
intervention path; acknowledgement alone grants no authority. Initial work is
cycle zero; every authorized correction reservation charges exactly one of the
three shared cycles across check/review/repair routes. Replay/reload/revision
cannot reset or double-charge. Unknown occupancy requires a fresh correction.
Accept as soon as requirements pass; three corrections are not a minimum.
No fourth correction; exhaustion preserves work/evidence and a precise blocker.

**AC-05 — Prove review-driven correction and conservative replay.**

Use the public local lifecycle in a disposable prepared task: real implementation,
passing real checks, independent collector finding, separate correction decision,
actual code correction, new candidate/checks, fresh collection and fresh separate
acceptance. Observe changed behavior as well as file changes. Do not seed owned
acceptance/admission success or use the old test-only successor decision as proof
of this route. Exercise shared check/review counting through the third correction
and fourth refusal, with replay/reload and retained history. Admission replay
returns the retained decision without reinterpreting replaced raw actor output.
Unknown/live operation ownership stops retry or progression; invalid requests
preserve authoritative state/version/count and task files. Diagnostic failure
records may be retained separately. An eligible accept still cannot complete.

**AC-06 — Publish the completion consumer contract.**

Document actual callable/CLI spelling, assignment/result schemas, decision and
disposition paths/digests, eligibility checks, missing-evidence/correction routes,
idempotency/refusals and the exact seam for T-005.2. Identify remaining recording
and completion work. Report local results, skips/failures and inherited limits;
local scripted roles do not qualify real sbx/provider/model execution or semantic
review quality. T-006 retains that live proof.

## Evidence boundaries

Verification-design recommendation: **separate** — finite session/identity
tampering, disposition continuity, actual review-driven correction and shared
budget/replay states need derived scenarios with positive and refusal controls.
Inspect existing actor-operation/state coverage and reusable fixtures before
adding cases under installed `testing-discipline`. Existing collection and
transport are believed available; preflight confirms their current interface and
installed review capabilities. No new proof harness or feasibility prerequisite
is needed: real local Git/files, check runner and scripted actor processes provide
the decisive controller oracle. They do not establish model judgment quality.

## Execution and handoff

Status: `ready`
Task kind: `executable`
Brief revision: 1
Profile: `guided`

The brief is prepared; execution prerequisites remain. Next: derive
`verification.md`, then obtain ready `preflight.md` through standalone guided
preflight. This is a human-readable preparation chain, not an orchestrated
machine packet; high-assurance reconstruction is not required. Check current
dependency interfaces, installed roles and inherited environment limits there.

Workflow: [shared submission route](../../../../../.agents/skills/README.md#submission-route).
Run the owning focused gate first, then the orchestrator suite when targeted
checks pass. Apply architecture and contract checks and the repository aggregate
when cross-cutting. Separate maintainability/registry/discovery/acceptance stages
retain their gate ownership. Report failures and skips truthfully; no live,
networked or expensive verification is authorized. After acceptance, hand the
current controller contract and accepted results to T-005.2; do not execute it.

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
Considered separate decision-validation and correction-routing leaves. Both own
the same disposition/current-evidence transition and replay semantics; separating
them would expose a provisional admitted decision without its safe next action
and duplicate lifecycle fixtures/review. The completion consumer is already
separate. Residual risk: finite identity and history cases may grow; the budget
is a soft checkpoint and material scope changes return to task design.
