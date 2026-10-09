# Project Plan — Standalone task verification and review policy

Status: `READY_FOR_PLAN_VERIFICATION`  
Plan version: `2026-10-08 / standalone-v1`

## 1. Planning authority

### Product outcome

Deliver a reliable human-coordinated task flow: binding preparation, independent evidence discovery, contextual acceptance, complete correction handoffs, and qualified installed skills. This is maintenance of the existing toolkit, not a new executor.

### Authoritative inputs

- User scope: plan what matters outside `task-orchestrator`; do not implement it now.
- User decisions: require separate verification design and preflight for executable task packages; allow compact artifacts; add no global correction-round limit. Acceptance must fix material operational, business and later-refactoring risk while avoiding an endless additional-fix loop. Continue through ordinary uncertainty; prompt only for unresolved serious consequences of delay or materially costly later repair.
- [Dated proposal](../skills/task-implementation-flow/docs/verification-and-review-policy-plan-2026-10-08.md): upstream intent and confirmed explicit-AC-failure rule. User decisions above resolve or narrow its proposals. Leave it unchanged.
- Root `AGENTS.md` and supplied repository instructions: bounded changes, truthful verification, narrow installer ownership, and separate task results from existing plans.
- [Current flow](../skills/task-implementation-flow/README.md), its source skills/references/eval fixtures, [root README](../README.md), [profile guide](../skills/README.md), [installer](../scripts/install_development_skills.py), and focused local tests.

No charter or readiness artifact was supplied for this maintenance change. The existing source/installer/test foundation is the planning baseline; this plan claims no new foundation review. The project-local delivery-plan skill is the active planning authority. Source task skills are future edit targets.

### Settled decisions

Packaged executable leaves take separate verification design and preflight before implementation. Composite/blocked tasks cannot enter. Small clear direct edits retain compact inline verification and a safety check; material uncertainty routes to its owner. The exception cannot bypass a task package.

The brief and cited authority remain normative. Scenarios are binding evidence obligations frozen at ready preflight, not a second requirements source. Preflight owns readiness; implementer checks entry validity. Discovery and acceptance are separate calls when functional review is required, independent of production authorship. Keep `ACCEPT`, `CHANGES_REQUESTED`, and `INCONCLUSIVE`.

Confirmed AC failures always block. Contextual material risk also blocks even when ACs pass. Other confirmed findings may be deferred with reasons. The human coordinator records deferrals before authorized advancement. Keep existing task-specific stops, including two materially different fixes failing the same targeted behavior; add no global round counter.

## 2. Scope

### In scope

Binding packaged preparation; scenario/evidence mapping; readiness ownership; `task-review-discovery` split from acceptance; contextual risk judgment; known issues; human submission/correction routes; complete bounded maintainability findings; unborn-HEAD installation repair; explicit read-only profile qualification; supplied standalone qualification fixtures and evidence.

### Non-goals

No controller, manifest/worker-result redesign, machine transition/evidence enforcement, automatic dependency release, unattended retry/recovery, retained runnable versions, parallel-worktree guarantees, telemetry or launcher/provider adapters. Leave spike FLOW-01/03/04/06, machine FLOW-05/LIVE-01 and TELEMETRY-01 with orchestration work. Include human FLOW-02/FLOW-05, reproducible-evidence lessons and SETUP-01/02 only. Profile matching does not prove retained versions or full unborn collector lifecycle support. No implementation or live eval is part of this planning task.

## 3. Actors and capabilities

The human coordinator launches stages and owns advancement/deferral recording. Task owners define requirements; verification designer derives scenarios; preflight owns readiness; implementer owns changes and submitted claims. Conditional gate, maintainability and registry owners retain their duties. Discovery corroborates evidence; acceptance decides. Source maintainer owns distribution; qualification author supplies runnable fixtures/results.

| ID | Capability | Observable outcome | Flows |
| --- | --- | --- | --- |
| CAP-001 | Prepare executable packages | Valid entry or named readiness/authority blocker; compact direct-edit route | FLOW-001 |
| CAP-002 | Review, decide and correct | Independent evidence, contextual disposition and complete continuation | FLOW-002/003 |
| CAP-003 | Install and qualify | Unborn/committed install, truthful drift check and explicit refresh | FLOW-004 |
| CAP-004 | Qualify composition | Reproducible claims and explicit unrun behavioral gaps | FLOW-005 |

## 4. Artifact and state catalog

IDs are local to this plan; spike issue names are separate upstream references. These are intended contracts, not proof of implementation. [task-map.json](task-map.json) retains the complete catalog and task relationships.

| ID / artifact | Source of truth; producer -> consumers | Durability / mutation / invalidation |
| --- | --- | --- |
| ART-001 Task authority | Brief and cited user/project/repo authority; task owner -> all stages | Durable packaged brief.md; only authority owner changes requirements. Changes supersede affected derived readiness/evidence. Qualification supplies explicit fixture authority. |
| ART-002 Verification | Verification designer under ART-001 -> preflight, implementation, discovery, decision | Durable verification.md with stable scenario IDs and source revision; freeze at ready. Reasoned revision supersedes affected readiness/evidence. |
| ART-003 Readiness/context | Preflight -> implementer and reviewers | Compact durable preflight.md: ready/blocked, source/scope/scenario revision, capabilities, permissions, commands and referenced decision context. Material fact changes make ready stale; expected task/report effects alone do not. |
| ART-004 Submission/continuation | Implementer; code/tests/observations underlie claims -> next stage, coordinator | Scoped changes, current scenario evidence, finding IDs, unfinished rows and ordered next obligations. Guided summary may be conversational. Changed reviewed bytes invalidate affected evidence. |
| ART-005 Conditional evidence | Gate runner, fresh maintainability reviewer, registry updater -> discovery/decision | Each producer owns its facts/handoff. Durable reports are numbered history. Applicable stages need current scoped evidence after relevant corrections. |
| ART-006 Discovery | Fresh independent discovery session -> acceptance/correction/coordinator | Complete or explicitly partial ledger, confirmed findings and reproducible probes. Next unused reviews/discovery-NN.md when durable. Changed bytes need current corroboration; no verdict/approved deferral. |
| ART-007 Decision | Separate independent acceptance call -> coordinator/correction/evidence owner | Current authority/revision/byte-bound decision and every finding's disposition; numbered durable reports preserve history. Old verdict cannot accept changed bytes. |
| ART-008 Known issues | Coordinator records approved ART-007 deferrals -> relevant preflight/decision/integration | Default docs/known-issues.md, subject to repo authority. Stable IDs, review provenance, trigger/consequence/evidence, risk rationale, affected consumers, follow-up owner and reassessment conditions. Coordinator updates resolution/context changes. |
| ART-009 Source profile | Editable source packages, canonical installer selection/guide/helpers -> installer/check | Versioned; source maintainers update only affected surfaces and synchronize distribution in the same change. Source edits never refresh an active session. |
| ART-010 Installed profile | Explicit installer projection of ART-009 -> skill calls/checks | Selected .agents/skills, sibling scripts, guide and marked AGENTS block only. Refresh between calls/runs; preserve unmanaged bytes. No retained-version guarantee. |
| ART-011 Profile result | Read-only source/target comparison -> maintainer/qualification | Matched, drifted/missing, or check failure with precise scope/reasons. Point-in-time output, optionally retained; source/target changes make it stale. No target mutation or run start. |
| ART-012 Qualification evidence | Supplied setup and observed results -> maintainer/later planners/reviewer | New results document beside dated proposal; exact probes, available evidence, qualified installation and unrun gaps. Source/installation changes invalidate current claims; history remains. |

## 5. Lifecycle/state models

```text
executable brief -> verification designed -> preflight ready -> implementation -> submitted
                         |-> authority owner       |-> blocked/stale -> owning stage
submitted -> applicable conditional stages -> discovery complete/partial -> decision
ACCEPT -> coordinator records deferrals -> authorized human advancement
CHANGES_REQUESTED -> authorized correction -> applicable fresh review -> new decision
INCONCLUSIVE -> evidence/capability/authority owner -> current evidence -> new decision
installed -> read-only check -> matched / drifted / check failure
drifted -> explicit refresh between calls/runs -> recheck
```

Authority revision supersedes affected verification/readiness. Scenario revisions require recorded reason and focused preflight. Expected task/report changes are attributed effects, not automatic readiness invalidation. Material prerequisite, authority, ownership, permission or required-capability changes require a new readiness decision. Exact high-assurance identity checks remain conditional.

An evidence request is not a production-fix request. Production corrections invalidate applicable semantic verdicts. Reference-only registry corrections keep the narrow updater-to-fresh-acceptance route only when actual effects and existing behavioral proof justify it; otherwise repeat affected discovery/gates. Ordinary fixes do not restart task design unless requirements change.

Each writer owns only its artifact/authorized scope. Durable reviews use unused numbers; reports do not authenticate themselves. No new transaction/concurrency protocol is added. Cancellation, unavailable capability or budget stops preserve incomplete rows, attempts and next owner; they cannot grant acceptance or release dependent work. Resume using current evidence, not inferred success.

## 6. Cross-task invariants

| ID | Must remain true | Intended proof |
| --- | --- | --- |
| INV-001 | Brief/authority are normative; scenarios cannot add requirements or excuse omitted AC failures. | T-001/002/005: omission, unjustified scenario, AC failure despite green tests. |
| INV-002 | Packaged executable leaves require verification and ready preflight; direct edits remain compact. | T-001/005: leaf/composite/blocked/doc-task/direct-edit cases. |
| INV-003 | Preflight owns readiness; entry checks current relevant facts without rediscovery. Expected task/report effects alone do not invalidate it. | T-001/003/005: stale versus expected changes, absent future test versus missing capability. |
| INV-004 | Discovery and decision are separate calls independent of production authorship; neither assumes the other's mandate. | T-002/005: provenance, discovery-only output, decision without broad rediscovery. |
| INV-005 | Required rows have current decisive pass/fail/blocked/unchecked evidence and reasons, including setup/oracle and relevant validator behavior. | T-002/005: weak oracle, missing evidence, stale bytes, valid/invalid validator probes. |
| INV-006 | AC/gate/unauthorized failures and confirmed material operating/business/contract/architecture/refactoring risk block; non-material findings may be deferred. | T-002/005: all rubric branches and context-dependent decisions. |
| INV-007 | Coordinator owns known issues; relevant later preflight reassesses them without hidden consumer workarounds. | T-002/005: record deferral, affected-next-task compatibility, unrelated task. |
| INV-008 | Handoffs name first outstanding stage and complete remainder; corrections preserve IDs/unfinished rows and get applicable fresh review. New blockers need material reasons. | T-003/005: conditional-route matrix, regressions, reference-only case, more than three maintainability blockers. |
| INV-009 | Install/refresh stays within managed ownership; qualification is read-only; unborn claims stop at exercised boundaries. | T-004: real Git fixtures, drift/refresh, unmanaged preservation, unchanged fingerprint semantics. |
| INV-010 | Qualification claims use supplied runnable setup and observed evidence; structure is not agent behavior proof. | T-005: fixture/raw-output audit, explicit unrun expensive checks. |
| INV-011 | Acceptance uses context/materiality; ordinary uncertainty continues with a recorded assumption. User questions are exceptional for serious consequences of delay or costly later repair that current authority cannot resolve. Required proof remains binding; optional fixes cannot restart correction. | T-002/005: contrasting contexts, no routine prompt, serious/costly-later exception, stable deferral and genuine regression. |

### Context and material-risk disposition

Carry a compact context summary in existing task/preflight evidence: intended use and operating envelope, important failure consequences, relevant business priorities, required consumers, credible same-kind maintenance/planned changes, mitigations and decision-relevant unknowns. Link task/project direction, architecture and current/planned contracts; do not invent business policy or create a second specification. A direct edit uses its request and relevant repo context. Record ordinary unknowns and reasonable assumptions, then continue. Do not require a complete context dossier or ask the user to classify every issue.

Each confirmed finding needs trigger, consequence, affected boundary, impact, likelihood/exposure, existing mitigation and a fix-now/deferral rationale. Assess impact and likelihood separately. Low likelihood cannot erase catastrophic data, security or irreversible-state consequences. Materiality follows supplied context, not reviewer taste.

| Condition | Disposition and rationale |
| --- | --- |
| Demonstrated AC/gate violation or unauthorized effect | Block; cite authority/current evidence even when design omitted the case. |
| Confirmed material operating/business risk with passing ACs | Fix now; show credible exposure/consequence and why mitigation or deferral is inadequate. |
| Confirmed material maintainability/refactoring risk | Fix now; identify introduced/worsened coupling, duplicated authority, locality or testability, and a credible maintenance/planned-change consequence. No formal future ticket is required; speculative redesign is insufficient. A hard-rule breach is sufficient, not necessary. |
| Bounded non-material confirmed defect; required evidence passes | ACCEPT with known issue may be justified; explain bounded effect, compatible consumers, follow-up and reassessment conditions. |
| Preference, polish or speculative improvement | Observation; not a new correction obligation. |
| Missing decisive required evidence | INCONCLUSIVE; route a focused request to discovery/capability owner. Do not routinely prompt the user or assume a production fix. |
| Ordinary uncertainty or unproved minor concern | Continue under a stated reasonable assumption; record an observation. Uncertainty alone is not a confirmed defect or new blocker. |
| Unresolved uncertainty with credible serious consequences of delay or materially costly later repair | Resolve within current authority first. If that cannot settle the decision, raise one focused question with the consequence and needed fact. |

The agent makes routine dispositions and authorized bounded correction/evidence requests without a new user confirmation. Continuing under ordinary uncertainty never waives a demonstrated AC failure, required gate or decisive proof obligation. Do not invent missing facts; distinguish an assumption from evidence.

Discovery supplies facts and suggested severity; acceptance owns judgment. Applicable maintainability review still goes first; acceptance consumes its evidence instead of repeating general design review, while retaining accountability for demonstrated contextual risk.

Correction review checks regressions, unfinished rows and changed/influenced surfaces. Preserve accepted dispositions unless relevant context/exposure changes. A new blocker needs proof, materiality and an explanation: correction regression, earlier blocked evidence, missed existing obligation, changed context/authority, or newly demonstrated material risk. Optional improvements never restart correction; real material risks still block.

## 7. System interface map

These are human/artifact boundaries, not runtime APIs. IDs, inputs/outputs and full contracts are indexed in task-map.json.

| ID | Producer -> consumer; inputs -> outputs | Success / rejection boundary |
| --- | --- | --- |
| IF-001 | Designer/verification/preflight -> implementer; ART-001/008 -> ART-002/003 | AC-to-scenario and scenario-to-authority closure; feasible setup/boundary/commands/permissions; relevant known issues/context. Future tests need not exist. Missing authority/capability routes to owner; readiness never claims behavior passed. |
| IF-002 | Implementer -> next stage; ART-001/002/003 -> ART-004 | Validate ready entry; map scenarios to current evidence. Required review means submission stop with first outstanding stage/full remainder. No reviewer launch or same-session acceptance. |
| IF-003 | Conditional stage owners -> discovery; ART-001/004 -> ART-005 | Required architecture/maintainability then applicable registry sync. Report all confirmed blockers from bounded safe review; remove three-blocker cap and enough-blockers stop. Missing required proof stays incomplete. |
| IF-004 | Discovery -> acceptance; ART-001/002/004/005 -> ART-006 | Corroborate complete/partial ledger, stable findings, exact reproducible probes. Relevant validators need valid/invalid cases. Batch independent safe affordable checks despite findings; suppress aggregate gate after decisive failure unless distinct authorized purpose. No verdict/deferral. |
| IF-005 | Acceptance -> coordinator/owning stage; ART-001/002/003/004/005/006/008 -> ART-007 | Admit current evidence, apply contextual rubric, classify every finding. Missing required proof routes to its evidence owner; ordinary context uncertainty continues. User escalation is reserved for unresolved serious consequences or costly later repair, not routine disposition. No routine broad search/full-suite repeat. |
| IF-006 | Coordinator -> continuation/next preflight; ART-001 through ART-008 -> ART-004/008 | Record accepted deferrals before authorized advancement. Route evidence, authority, scenario, production and reference defects to their separate owners; preserve complete IDs/current evidence. No automatic release. |
| IF-007 | Installer/check -> maintainer/users; ART-009 -> ART-010/011 | Explicit narrow install/refresh; genuine unborn HEAD is explicit, other Git failures remain failures. Read-only full managed-content comparison distinguishes match/drift/failure; no fingerprint shortcut or auto-refresh. Exact CLI is delegated. |
| IF-008 | Qualified profile/eval roles -> maintainer; ART-009/010/011 -> ART-012 | Local checks first; agent/model-budget evals need separate authorization and supplied runnable setup. Record exact tested profile, probes/results/gaps; never refresh active calls. |

## 8. End-to-end data/process/state flows

Artifact ownership is defined in section 4; each step below names reads/writes, crossed boundary and meaningful state/failure semantics. Complete step IDs and invariant references are in task-map.json.

### FLOW-001 — Prepare and enter implementation

Trigger: executable package or small clear direct edit. Terminal: valid implementation entry or named blocker.

1. Task owner validates executable leaf/ACs and relevant known issues (ART-001/008, IF-001); composite/blocked/ambiguous authority returns to owner. Clear direct edits take a compact check.
2. Verification designer derives ART-002 from ART-001, with stable scenarios and revision; unclear expected behavior returns to authority owner (INV-001/002).
3. Preflight reads ART-001/002/008, checks coverage, feasibility, ownership/permissions, commands/context and produces ready/blocked ART-003. Ready freezes scenarios (INV-003/007/011).
4. Implementer checks ready applicability, implements and submits ART-004 with scenario evidence (IF-002, INV-005/008). Stale material facts return to preflight; missing ACs return to authority owner.

### FLOW-002 — Review and decide

Trigger: required-review submission. Terminal: current disposition and complete human next route.

1. Implementer hands ART-004 to first outstanding conditional stage and ends its invocation (IF-002, INV-004/008).
2. Applicable architecture/maintainability and registry owners produce ART-005 in order (IF-003); blockers/unavailable proof return to their correction/evidence owners.
3. Fresh discovery reads ART-001/002/004/005 and produces complete/partial ART-006, with all rows/findings/probes (IF-004, INV-005). Partial is not clean.
4. Separate acceptance reads authority, ART-003 context, current submission/conditional/discovery proof and relevant known issues; writes ART-007 using the rubric (IF-005, INV-006/011). Ordinary context uncertainty continues with recorded assumptions; serious-delay/costly-later uncertainty is escalated only if current authority cannot resolve it.
5. Coordinator records approved ART-008 deferrals before authorized advancement, or routes correction/evidence/authority gaps (IF-006, INV-007). Reviewers do not acquire tracker authority.

### FLOW-003 — Continue after findings or gaps

Trigger: stage blocker/evidence request/corrected submission. Terminal: fresh decision or explicit unresolved stop.

1. Coordinator carries all IDs/rows, owner/reason, current evidence and affected/sibling surfaces; distinguishes clarification, production, reference, scenario and authority changes (ART-001 through ART-007, IF-006).
2. Correct owner clarifies ART-006 or updates authorized ART-004/005. Scenario coverage gaps get reasoned ART-002 revision and focused ART-003 readiness; changed requirements return to task design (IF-001/002/006).
3. Production corrections repeat applicable conditional stages, fresh correction discovery and separate acceptance (ART-005/006/007; IF-003/004/005). Check current obligations/regressions/unfinished and influenced surfaces. Reference-only updates keep the narrow route only when actual effects justify it.
4. Coordinator continues within existing authority/budgets/stops, batches clarification, preserves justified deferrals, and requires proof/materiality for new blockers (INV-008/011). Stops record gaps/attempts/next owner and do not release dependent work.

### FLOW-004 — Install, check drift, refresh

Trigger: explicit installation/check/refresh. Terminal: qualified managed projection or precise drift/failure with unmanaged state intact.

1. Maintainer synchronizes source packages, selection, guide/helpers/docs (ART-009, IF-007).
2. Canonical installer stages/replaces only managed surfaces and exercises installation availability on committed/unborn targets; produces ART-010 or explicit failure (INV-009).
3. Read-only check compares complete managed contents/references/guide/helpers/expected AGENTS block; produces ART-011 match/drift/failure. Unrelated target files/text are ignored, unexpected managed files are reported.
4. Maintainer explicitly refreshes between calls/runs if needed and rechecks. Matching supports a new invocation/qualification, not retained active-run versions.

### FLOW-005 — Qualify composition

Trigger: source and distribution tasks complete. Terminal: new reproducible results and explicit remaining gaps.

1. Qualification author supplies disposable Git repos, authority/context, good/wrong implementations, tests and ledgers; checks ART-009/010/011 and narrow local tests first (IF-008, INV-009/010).
2. Separately authorized role calls exercise preparation, disposition, conditional correction routes, contrasting risk contexts and relevant next-task known-issue consumption. Without authorization/capability, record an unrun gap (INV-001 through INV-011).
3. Author writes ART-012 beside the proposal with exact setup/probes, observed outputs and available evidence; distinguishes structural/local runtime/agent behavior claims. Existing plans stay unchanged.

### Producer/consumer closure

Authority and fixture authors supply legitimate inputs. Every derived artifact has a named stage producer/downstream reader; known issues return to relevant preflight and integration. Source produces installed copies, comparison produces qualification results, and runnable checks produce preserved results. Historical reviews retain audit value after staleness. No report proves itself or substitutes for a decisive observation.

## 9. Capability-to-flow coverage

| Capability | Artifacts | Interfaces / invariants | Completion |
| --- | --- | --- | --- |
| CAP-001 / FLOW-001 | ART-001/002/003/004/008 | IF-001/002; INV-001/002/003/005/007/011 | Valid packaged entry or owned blocker; direct edit remains compact. |
| CAP-002 / FLOW-002/003 | ART-001 through ART-008 | IF-002 through IF-006; INV-001/003/004/005/006/007/008/011 | Current independent evidence, disposition and complete continuation. |
| CAP-003 / FLOW-004 | ART-009/010/011 | IF-007; INV-009 | Unborn/committed install, non-mutating drift check, deliberate refresh. |
| CAP-004 / FLOW-005 | ART-009/010/011/012 | IF-008 and exercised interfaces; INV-001 through INV-011 | Reproducible qualified outcomes with unrun gaps explicit. |

## 10. Implementation task map

[task-map.json](task-map.json) is the authoritative machine index, including each task's consumes/produces/interfaces/invariants and detailed planning context. Planners may split behavioral slices while preserving relationships; record implementation results separately.


| Task / outcome | Depends on / flows | Consumes -> produces | Interfaces / invariants |
| --- | --- | --- | --- |
| T-001 — Binding packaged preparation and compact entry checks; preserve direct edits. | None; FLOW-001, FLOW-003 | ART-001, ART-008, ART-009 -> ART-002, ART-003, ART-004, ART-009 | IF-001, IF-002; INV-001, INV-002, INV-003, INV-005, INV-007, INV-011 |
| T-002 — Independent discovery/decision with contextual material-risk disposition and coordinator-owned known issues. | T-001; FLOW-002, FLOW-003 | ART-001, ART-002, ART-004, ART-005, ART-008, ART-009, ART-003 -> ART-006, ART-007, ART-008, ART-009 | IF-004, IF-005, IF-006; INV-001, INV-004, INV-005, INV-006, INV-007, INV-011 |
| T-003 — Complete ordered handoffs/correction evidence and all bounded confirmed maintainability blockers. | T-001, T-002; FLOW-002, FLOW-003 | ART-001, ART-002, ART-003, ART-004, ART-005, ART-006, ART-007, ART-009 -> ART-004, ART-005, ART-006, ART-007, ART-009 | IF-002, IF-003, IF-004, IF-005, IF-006; INV-003, INV-004, INV-005, INV-006, INV-008, INV-011 |
| T-004 — Unborn installation plus explicit read-only drift qualification and safe refresh. | T-001, T-002, T-003; FLOW-004 | ART-009, ART-010 -> ART-009, ART-010, ART-011 | IF-007; INV-009 |
| T-005 — Reproducible installed-flow qualification or explicit unrun gaps. | T-001, T-002, T-003, T-004; FLOW-001, FLOW-002, FLOW-003, FLOW-004, FLOW-005 | ART-001, ART-002, ART-003, ART-004, ART-005, ART-006, ART-007, ART-008, ART-009, ART-010, ART-011 -> ART-012 | IF-001, IF-002, IF-003, IF-004, IF-005, IF-006, IF-007, IF-008; INV-001, INV-002, INV-003, INV-004, INV-005, INV-006, INV-007, INV-008, INV-009, INV-010, INV-011 |

### Integration boundaries and task-planning handoff

- **T-001:** A packaged leaf cannot enter without justified current verification/readiness. Own brief/layout, verification, preflight/packet and implementer-entry contracts. Future tests are normal; absent indispensable capability blocks. Record compact context and distinguish expected correction/report effects from stale approval. Synchronize affected usage/profile guidance.
- **T-002:** AC-compliant material operation/business/refactoring risk blocks; bounded minor issues may be deferred; missing required evidence routes to its owner; ordinary contextual uncertainty continues without a user prompt. Carefully design the contextual rubric, autonomous disposition and both over-permissive and repeated-fix/prompt cases. Escalate only unresolved credible serious-delay or costly-later risk outside current decision authority. Move current lifecycle/public-boundary/schema/continuation obligations to discovery without losing them. Keep distinct role reasoning guidance, narrow writes and numbered reports. Add discovery to the installer/guide/tests/docs in this same change; do not postpone distribution ownership to T-004.
- **T-003:** Immediate review/correction routes choose the first outstanding stage for neither/either/both conditional stages, retain all finding/coverage IDs, and get fresh applicable review. Remove the maintainability cap/early stop without widening review scope. Preserve actual-effect reference-only routing and accepted dispositions unless context changes. Add no global round limit; keep existing targeted-fix stop rules.
- **T-004:** Real unborn install works; deliberate managed drift is detected without writes; explicit refresh restores match and preserves unmanaged files. Synchronize installer selection, profile guide, helpers, tests and READMEs. Do not fabricate HEAD, change fingerprint framing, claim full collector lifecycle, broaden ownership or add active-run retained versions. Exact check CLI/comparison code is local design.
- **T-005:** Qualified installed copies exercise packaged completion, inadequate-evidence/real-AC-failure rejection, material-risk and minor-deferral decisions, relevant next-task consumption, and correction-stage continuity. Supply actual inputs/setup and contrasting contexts; preserve existing continuation/public-boundary cases. Behavioral evals need separate authorization; unrun evals mean incomplete behavioral qualification. Write a new results document beside the dated proposal.

## 11. System verification map

This planning task runs only the project-local task-map validator and local scope/link checks: structural proof, not semantic/behavioral certification. Implementation starts with cheap focused local checks. Existing installer, workflow-version, availability, review-discipline and skill package/eval fixtures are relevant. Wording assertions prove text presence, not agent behavior.

| Flow / interfaces / invariants | Decisive cases / oracle | Owners |
| --- | --- | --- |
| FLOW-001; IF-001/002; INV-001/002/003/007/011 | Omitted AC, unjustified scenario, weak oracle, absent fixture versus valid future test; stale authority/design/permission versus expected effects; relevant known issue; compact documentation package/direct edit. Supply task and preparation artifacts, observe actual ready/entry result. | T-001; composed installed eval T-005 |
| FLOW-002; IF-003 through IF-006; INV-004/005/006/007/008/011 | Wrong implementation with green tests; partial/weak evidence; actual independent provenance; material operating/business/refactoring risk; minor defect, catastrophic consequence, required consumer breach, speculative preference; ordinary uncertain concern without prompt versus unresolved serious/costly-later escalation; missing required proof to evidence owner; no broad rediscovery. Observe separate reports, reasons and writes. | T-002/003; T-005 |
| FLOW-003; IF-001 through IF-006; INV-001/003/005/008/011 | Conditional-stage matrix; production/test/reference-only corrections; regression/unfinished evidence; more than three observable maintainability blockers; stable deferral versus changed exposure; new material blocker versus optional fix; stopped continuation. Observe IDs, current proof and next owner. | T-003; T-005 |
| FLOW-004; IF-007; INV-009 | Real unborn/committed/detached Git fixtures; non-unborn Git failure; skill/reference/guide/helper/managed-block drift, missing/extra managed files; refresh; unmanaged preservation; read-only before/after file/Git snapshots; unchanged fingerprint semantics. | T-004 local installer/identity/availability tests |
| FLOW-005; IF-008; INV-010 plus exercised invariants | All claimed success/failure paths get authority/context, starting state, actual implementation/tests and exact probes. Relevant validator boundary gets valid and targeted invalid instances. Audit raw evidence and installation qualification; record unavailable/unrun cases. | T-005 integration qualification |

Local deterministic tests can prove installer behavior. They cannot prove semantic skill-call compliance. Agent/model-budget evals require separate authorization; plan approval alone does not authorize them. T-005 needs its required behavior evidence or an explicit owner revision to its scope. Coding-agent use alone does not trigger a product AI foundation. Intended role reasoning settings are human guidance, distinct from observed runtime settings; no launcher integration is added.

## 12. Risks, assumptions, and delegated choices

### Blocking/open system questions

None for plan verification: the user resolved mandatory-stage scope and the proposed global correction limit. Behavioral-eval authorization is a later execution prerequisite. Independent verification may find new system questions.

### Risks and assumptions

The existing foundation is adequate for planning, without a new readiness claim. Compact preparation limits mandatory-stage overhead. Splitting review risks losing existing evidence obligations; T-002 must preserve them. Stale installed copies risk mixed-policy calls; qualify and explicitly refresh between invocations. Risk judgment may become permissive or chase optional fixes; T-002/T-005 must test contextual materiality, correction stability and absence of routine issue prompts. Known issues can become consumer blockers; reassess relevant changed exposure, without hypothetical future-use proof or hidden workarounds. Existing authority/budgets and bounded discovery govern corrections without a new global counter. Ordinary uncertainty must not become repeated human approval requests.

### Intentionally delegated task-local choices

- `DELEGATED:` Check CLI/result field names and comparison implementation, preserving match/drift/failure and ownership semantics.
- `DELEGATED:` Compact report formatting and per-role reasoning recommendations, preserving required context/evidence and separate calls.
- `DELEGATED:` Concrete tests/helpers/fixtures, correction implementation and task splitting. The cross-task contracts and material-risk rubric above remain fixed.

## 13. Plan-verification handoff

Review [project-plan.md](project-plan.md), [task-map.json](task-map.json), the unchanged dated proposal, source flow/installer contracts and recorded user decisions together. Reconstruct scope, producer/consumer closure, role authority, stage routes, correction invalidation, contextual risk/deferral and qualification semantics.

Run `project-plan-verification` in a fresh/separate agent invocation. This session does not self-certify semantic completeness or claim implementation complete.

`READY_FOR_PLAN_VERIFICATION`
