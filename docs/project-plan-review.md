# Project Plan Review

Verdict: `ACCEPT`
Review date/session: `2026-10-09 / /root/plan_reviewer`

The reviewer is a fresh, separate agent that did not author the plan. This review used the project-local `.agents/skills/project-plan-verification/SKILL.md` and its report template. Planner explanations were checked against the dated proposal and current repository contracts. This is plan verification, not implementation acceptance or behavioral qualification.

## Reviewed bytes

- `docs/project-plan.md` SHA-256: `84168fadfc6d0f8b604f0357ef0c29ab01552b10795df70c3d258e430a4f5299`
- `docs/task-map.json` SHA-256: `2453a8470d0229bbac4b739cceb59e6480b7001c12116130b9141c2c39268e7a`
- Repository revision: `d2e045144fb2cd186c3ae8c9e64a5a029eb5afa7`.
- Starting `git status --short`: staged deletion of `docs/project-plan-review.md`; staged modifications to `docs/project-plan.md` and `docs/task-map.json`. The current filesystem bytes were reviewed. The report was absent and was recreated without staging. Neither planning artifact was edited.

## Authoritative sources reviewed

- Supplied repository/user instructions and root `AGENTS.md`.
- `skills/task-implementation-flow/docs/verification-and-review-policy-plan-2026-10-08.md`, including its confirmed explicit-AC-failure rule. The plan's recorded later user decisions settle the mandatory packaged stages and reject the proposal's global correction limit.
- `skills/task-orchestrator/docs/integration-spike-2026-10-08/issues.md` for the human FLOW-02/FLOW-05, reproducible-evidence and SETUP-01/02 boundaries.
- `skills/task-orchestrator/docs/code-guided-orchestration.brief.md` for the separate executor direction and deferred machine/retained-version work; it is a discovery brief, not authority to expand this maintenance plan.
- Root `README.md`, `skills/README.md`, and `skills/task-implementation-flow/README.md`.
- Source contracts for `task-brief-designer`, `task-verification-designer`, `task-preflight`, `bounded-task-implementer`, `task-maintainability-review`, `task-contract-registry-updater`, and `task-acceptance-review`; relevant artifact-layout and acceptance-report references.
- `scripts/install_development_skills.py`; relevant workflow identity/availability seams in `scripts/workflow_version.py` and `scripts/run_evidence.py`.
- Focused installer, workflow-version, availability and review-discipline test definitions; existing task-skill eval cases and relevant fixture setup definitions. These were inspected as planning context, not executed as behavior evidence.

No charter, AI foundation or foundation-readiness report is required by this maintenance route. The plan names an optional `deferred-work-after-t-o-new-flow.md` companion without a location. It was unavailable at `docs/`, and no alternate path was supplied. No critical contract relies on it; the proposal and plan state the deferral boundary directly. No additional search was performed.

## Independent reconstruction

### Product outcome

The existing toolkit should support a dependable task flow coordinated by a person. A packaged task must enter implementation with justified verification and a current readiness decision. Fresh review must establish what the evidence proves before a separate call decides whether the submitted work may advance. Corrections must preserve outstanding obligations and return through the required stages. Maintainers must be able to install the intended profile in a new Git repository, detect drift without changing the target, and refresh it deliberately.

### Required capabilities / critical journeys

- Prepare an executable leaf: map authority to discriminating scenarios, establish feasible evidence and readiness, and admit only a current implementation entry. A small clear direct edit retains a compact route.
- Submit and independently review: retain conditional architecture/maintainability and registry duties, produce a complete or explicitly partial discovery ledger, then decide from current evidence and relevant context.
- Correct or recover evidence: retain every finding and unfinished row, distinguish evidence/authority/scenario/production/reference changes, obtain the affected current proof, and stop without advancement when obligations remain unresolved.
- Defer a bounded non-material finding: acceptance supplies the disposition, the coordinator records it, and a relevant later task reassesses the affected contract without an undeclared workaround.
- Install and qualify distribution: exercise genuine unborn and committed repositories, compare the managed projection, refresh explicitly between calls, and preserve unmanaged state.
- Qualify the composed workflow: supply runnable good/wrong fixtures and actual stage outputs, invoke qualified installed copies in separate consuming calls, and report observed outcomes and unrun gaps honestly.

### Explicit non-goals / constraints

- This plan does not deliver a code executor, typed stage sidecars, automatic advancement, retained runnable versions, telemetry, parallel worktree guarantees or unattended recovery.
- Brief/user/repository authority stays normative. Scenarios cannot add requirements or excuse an omitted AC failure.
- Discovery supplies facts; acceptance decides; the coordinator owns advancement and known-issue writes. Role changes in an authoring session do not create independence.
- Current required evidence is mandatory. Passing ACs cannot excuse demonstrated material operating, business, consumer or maintainability risk; speculative preferences cannot prolong correction.
- Ordinary uncertainty permits a recorded assumption. A decision-critical unresolved serious consequence or costly later repair follows its owner route, with a focused user question only when existing authority cannot resolve it.
- Existing task stops and budgets remain; there is no new global correction counter. Expensive/live agent evals need separate authorization.
- Installer ownership, same-installation-root helper resolution and fingerprint framing remain compatibility constraints.

## Structural checks

- Bundled verifier: `PASS` — `python3 .agents/skills/project-plan-verification/scripts/verify_plan_artifacts.py docs/project-plan.md docs/task-map.json`, exit `0`, reported `PASS: planning artifacts are structurally reviewable` and the digests above.
- Reference integrity: `PASS` for checked plan/task-map IDs and required named repository inputs. The optional companion limitation is recorded above.
- Task dependency graph: `PASS`; no cycle. The intended order is T-001 → T-002 → T-003 → T-004 → T-005.

These checks establish structural reviewability only. The verdict also relies on the semantic traces below. No live/model eval, installer mutation, or broad test suite was run.

## Coverage summary

| Area | Result | Notes |
|---|---|---|
| Scope fidelity | PASS | CAP-001 through CAP-004 preserve the standalone proposal scope and recorded amendments; executor requirements stay deferred. |
| End-to-end flow completeness | PASS | FLOW-001 through FLOW-005 have a trigger, stage ownership, observable terminal outcome and explicit non-success routes. |
| Artifact producer/consumer closure | PASS | ART-001 through ART-012 have sources, writers, readers and lifecycle rules; external authority and fixture producers are intentional. |
| State/lifecycle semantics | PASS | Ready/stale, complete/partial, correction/evidence recovery, historical reports and matched/drifted/failure states cannot grant inferred success. |
| Interface contracts | PASS | IF-001 through IF-008 define the cross-role behavior while leaving formatting, CLI fields and test implementation local. |
| Cross-task invariants | PASS | INV-001 through INV-011 have affected surfaces, task owners and intended discriminating evidence. |
| Capability/task coverage | PASS | Every capability has a realizing flow and completion boundary; all five tasks contribute to those flows. |
| Dependency/order composition | PASS | Shared source edits are ordered; current conditional-stage contracts are legitimate baseline seams, not missing future producers. |
| Verification coverage | PASS | Section 11 separates task-level proof from actual composed handoffs, real filesystem/Git checks and authorized agent behavior evidence. |
| Planning abstraction | PASS | The plan settles coordination semantics without choosing private helpers, classes or unnecessary schemas. |

### Critical flow traces

| Flow / capability | Trace and non-success boundary |
|---|---|
| FLOW-001 / CAP-001 | ART-001/008 → IF-001 → justified ART-002 → feasible ready/blocked ART-003 → IF-002 → ART-004. Composite/blocked authority, unjustified coverage, missing indispensable capability and stale material facts return to named owners. Future tests and expected report effects do not become false blockers. |
| FLOW-002 / CAP-002 | ART-004 → first outstanding IF-003 stage → ART-005 → fresh IF-004 discovery using ART-003 context → ART-006 → separate IF-005 decision → ART-007 → coordinator IF-006 recording of ART-008 before advancement. Partial proof cannot become clean; confirmed bounded blockers take correction precedence while unfinished proof and authority questions retain their own routes. |
| FLOW-003 / CAP-002 | Existing IDs/rows → owner classification → clarification or authorized correction → current conditional evidence/discovery/decision. A scenario coverage revision retains IDs, invalidates affected readiness and needs focused preflight plus revised evidence. Changed requirements return to task design. Production corrections invalidate semantic verdicts; a reference-only shortcut needs actual-effect proof and still gets fresh acceptance. Cancellation, budget or repeated-fix stops preserve attempts and gaps. |
| FLOW-004 / CAP-003 | ART-009 → explicit IF-007 installation → ART-010 → read-only complete managed comparison → ART-011. Genuine unborn identity is separate from Git failure. Drift needs deliberate refresh and recheck between calls; match is a point-in-time projection claim, not retained-version or collector-lifecycle proof. |
| FLOW-005 / CAP-004 | Supplied authority/implementations/tests and qualified ART-009/010/011 → IF-008 local checks and separately authorized role calls → ART-012 with exact setup, outputs and gaps. Actual preparation, discovery and correction outputs must reach separate consumers; fabricated reports or wording checks cannot prove composition. |

### Ownership, identity and handoff checks

- ART-001 is owner-supplied authority. ART-002 and ART-003 are derived under it, with stable scenarios and distinguishable revisions. ART-004 is a submission claim supported by current code/tests/observations, not a competing requirements source.
- ART-005 preserves each conditional producer's authority. ART-006 contains current corroboration and the discovery-owned aggregate-gate record. ART-007 admits that evidence without routine duplicate execution. A later omitted material row makes the earlier aggregate premature; targeted proof precedes any justified rerun.
- ART-008 has a coordinator writer and a specific return path into relevant preflight/acceptance/integration. Optional context links do not grant portfolio authority or turn proposed future work into mitigation. A priority change alone cannot invalidate acceptance; changed material facts can.
- ART-009 is the versioned source/manifest authority. ART-010 is its explicitly refreshed managed projection. ART-011 compares the full managed contents, guide, helpers and AGENTS block rather than treating runtime fingerprints as profile equivalence.
- ART-012 preserves observed qualification and its inputs. Changed relevant source or installation makes current claims stale without rewriting history.
- Stable ART/IF/INV/FLOW/T IDs, scenario/finding IDs, task-package names and numbered reports provide sufficient downstream identity. Future implemented-contract discovery can map these IDs without inventing private implementation paths or demanding registry records for unborn contracts.
- T-001 can use an empty known-issue set until T-002 introduces deferral production. T-002 consumes existing conditional-stage contracts; T-003 closes their ordered handoffs. These are safe baseline dependencies, not a circular reliance on future behavior. T-002 installs the new discovery package in its own change. T-004 follows source-contract changes, then T-005 qualifies the resulting installed composition.

## Findings

None.

## Producer/consumer exceptions checked

- Task owners and qualification fixture authors are legitimate external producers of ART-001 and initial test state; they need no separate product task.
- Existing architecture/maintainability and registry stages legitimately supply ART-005 before their routing refinements in T-003.
- Historical submissions, numbered ART-005/006/007 reports and ART-012 results retain audit/provenance value after supersession. They are not current acceptance evidence.
- ART-011 may be transient point-in-time output or retained evidence. Its consumer value is the explicit match/drift/failure result, not durable transition authority.
- No ART-008 file is required before a deferral exists. Its optional portfolio use is a future consideration, with no new current consumer or stage.

## Open system questions

- No unresolved question blocks downstream task planning.
- T-005's behavioral-eval authorization is a later execution prerequisite. Unrun evals may be reported as incomplete qualification; they cannot satisfy required behavior evidence or permit a completed-qualification claim. The plan requires that evidence or an explicit owner revision of scope.
- The optional companion location remains unavailable. This does not affect scope or composition because the governing documents state the deferred boundary directly.

## Verdict rationale

The plan has no identified BLOCKER or MAJOR defect. It preserves the proposal's applicable standalone goals, settles the cross-role authority and correction semantics, closes artifact ownership and dependencies, and assigns intended evidence at boundaries that can distinguish plausible wrong behavior. The amended preflight-context, aggregate ownership, revision recovery and mixed-condition rules are consistent across prose, task-map interfaces, flows, invariants and planning context. Local implementation choices remain delegated without forcing another task to guess a critical contract.

## Next action

Feed these reviewed plan/task-map bytes into downstream task planning. Obtain separate authorization before behavior evals and retain their gaps until actual qualification evidence exists. Material changes to either planning artifact require a fresh review.
