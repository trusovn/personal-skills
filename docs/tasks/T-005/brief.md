# Task Brief: `T-005` — Qualify standalone policy composition

Status: `decomposed`

Task kind: `composite`

## Outcome

A reproducible fixture set and a new results report establish which standalone
installed-flow behaviors were exercised and identify every unrun qualification
gap. Full behavioral qualification requires observed producer-to-consumer role
calls; local tests and staged reports alone cannot establish it.

## Authority and scope

- Authority: [project-plan.md](../../project-plan.md), sections 1–2, 4–8,
  T-005 in section 10, and section 11, including its additional-proof table;
  `T-005` in [task-map.json](../../task-map.json); root `AGENTS.md`.
- Stable refs: `CAP-004`; `FLOW-001` through `FLOW-005`; consumes `ART-001`
  through `ART-011`, produces `ART-012`; preserves `IF-001` through `IF-008`
  and `INV-001` through `INV-011`.
- Dependencies: completed/reviewed T-001–004 contracts and applicable
  [INT-FLOW-001](../INT-FLOW-001/brief.md) corrections. Their current acceptance
  and relevance belong to preflight; source/results presence is not completion.
- Scope: disposable Git fixtures, narrow local evidence, qualified installed
  copies and sibling helpers, separately authorized role calls, actual output
  handoffs, evidence audit and a new report beside the dated proposal.
- Preserve the T-002.4 `COMP-01`–`COMP-05` / `INV-CASE-01`–`INV-CASE-24`
  inventory, T-003.4 `CCR-01`–`CCR-08` / composition records, and INT-FLOW-001
  qualification inputs. Reuse current owning tests; historical command names
  in old results are not current selectors. `tests/README.md` names the owners.
- Out of scope: production policy repairs, a reusable role runner, new shared
  infrastructure, controller/provider/launcher integration, machine stage
  sidecars, automatic advancement, retained runnable versions, active-session
  refresh, and official-plan or historical-report edits. A discovered policy
  defect returns to its source owner rather than expanding qualification work.
- Assumptions: existing fixtures, installer and separate manual skill calls
  can establish the approved oracles. Current launch interface/permissions and
  exact fixture paths are preflight facts, not new architecture decisions.

## Direction trace

- Direction contribution: reliable human-coordinated preparation, independent
  evidence and contextual decisions with complete correction routes.
- User-observable effect: the maintainer can reproduce each supported claim
  and see the remaining gaps before later orchestration work.
- Why now: FLOW-005 follows source-policy and distribution tasks; section 11
  assigns T-005 the additional proof at actual stage handoffs.
- Direction decisions used: plan section 1 settled decisions; section 2
  exclusions; `IF-004/005/008`, `INV-010/011`, FLOW-005 and section 11.
- New direction decisions required: None.

## Execution sizing

- Sizing policy: `default@1` from the active project-local designer's
  `references/task-sizing.yaml`.
- Original estimated agent calls: 100. Implementation duration: 270 minutes.
- Intended execution profile: `standard / high`. Confidence: medium.
- Triggered limits: `max_agent_calls`, `max_duration_minutes`.
- Estimates include setup/discovery, task-owned edits, local checks and an
  authorized bounded role-call attempt. Separate preparation/review is excluded;
  authorization does not follow from the estimate. Unavailable calls become
  explicit gaps, never inferred passes. A larger approved eval campaign requires
  a new budget/boundary check before execution.

## Decomposition

| Child | Responsibility / owned output | Depends on | Brief |
|---|---|---|---|
| T-005.1 | Reusable fixture inventory, qualified projection receipts and local baseline | T-001, T-002, T-003, T-004, INT-FLOW-001 | [brief](../T-005.1/brief.md) |
| T-005.2 | Actual preparation/entry and verification-revision recovery evidence | T-005.1 | [brief](../T-005.2/brief.md) |
| T-005.3 | Actual discovery-to-decision evidence with contextual and mixed-condition contrasts | T-005.1 | [brief](../T-005.3/brief.md) |
| T-005.4 | Coordinator-recorded deferral consumed by later relevant/unrelated preflight | T-005.3 | [brief](../T-005.4/brief.md) |
| T-005.5 | Actual conditional/correction continuity, finding IDs and aggregate ownership | T-005.2, T-005.3 | [brief](../T-005.5/brief.md) |
| T-005.6 | Final cross-child evidence audit and ART-012 results beside the proposal | T-005.1, T-005.2, T-005.3, T-005.4, T-005.5 | [brief](../T-005.6/brief.md) |

These boundaries deliver consumable setup, case-scoped role evidence, a real
accepted-deferral input, correction history, then one audited report. Splitting
by skill or into separate test-writing tasks would sever the handoffs being
qualified. Each leaf owns its case workspace and evidence directory; no sibling
appends to another's results. .1 owns the shared fixture inventory; .6 alone
owns the final report. Dependencies are acyclic. .3 and .5 retain permitted,
reasoned no-split overrides for their coupled multi-call comparisons; the other
leaves fit the active policy.

## Evidence rules carried by every leaf

1. Every claimed case supplies authority/context, starting Git/filesystem
   state, actual good/wrong implementations and tests, setup/probe commands,
   expected oracle, output identity, result and next owner. Preserve stable
   plan and inherited case IDs. Map an inherited case to existing evidence or
   an explicit gap; do not rerun every isolated case for ceremony.
2. Install only into disposable targets using the canonical installer. Record
   the source revision, full managed-projection comparison and matching
   `--check` result. A workflow fingerprint alone omits eval/setup content.
   Recheck before calls; changed source/installation invalidates affected
   claims. Use target-local skills and sibling `.agents/scripts/` only.
3. Actual stage calls use separate invocations where the plan requires them.
   Preserve the producer's raw output before grading. Feed the actual report
   to the consumer, with preparation references and current identities; a
   staged report is input history, never an observed producer result. Keep
   setup code, expected answers and grading oracles outside reviewer inputs.
4. No live/network/model-budget eval is authorized by this brief. Before such
   work, obtain authorization for concrete cases, call method, cost/time limit
   and permissions. Without it, supply reproducible setup and mark that
   boundary `unrun` with reason/owner. Local structural/runtime results may
   pass while behavioral qualification remains incomplete. Never accept an
   unrun required boundary or describe the overall flow as qualified.
5. Qualification observations have their own `pass/fail/blocked/unchecked`
   status; a fixture's expected verdict is a separate field. A correct
   CHANGES_REQUESTED observation can pass an eval; it cannot advance the
   fixture task. Preserve failures, unfinished rows and stops. Source defects
   route to their owner; do not weaken an oracle to make a result green.
6. Existing local tests first, new distinct evidence only where missing. Use
   project-local `testing-discipline`; reuse `tests/staging_fixture_support.py`
   for repository tests. Skill setup remains self-contained. Run targeted
   checks before owning suites, sequentially. Prove intended rejection with a
   wrong variant/controlled fault where feasible, and leave no mutation behind.
7. In fixture reviews, discovery owns the justified aggregate after clean
   targeted rows; acceptance consumes it without rerunning. Record command,
   owner, stage, reason and current evidence. The review of each qualification
   leaf follows the same policy; no whole-repository or live aggregate is added.

## Coverage and closure

| Parent requirement | Owning child / composed proof |
|---|---|
| P-01: Reproducible supplied fixtures; current qualified installed copies/helpers; retained public/continuation cases | .1; every call leaf rechecks identity |
| P-02: Packaged preparation reaches implementation; direct/refusal contrasts; unchanged-authority revision recovery versus changed requirements | .2 |
| P-03: Actual independent discovery/decision, wrong-green/weak evidence rejection, preflight-only material exposure, contextual risk and prompt behavior, mixed-condition precedence | .3 |
| P-04: Accepted bounded issue recorded by coordinator and consumed by later preflight; unchanged/changed/unrelated exposure | .3 produces decision; .4 records/consumes it |
| P-05: Conditional-stage matrix, actual-effect routing, complete IDs/rows, four blockers, genuine stops and fresh correction proof | .5; .2 supplies revision recovery |
| P-06: Failure → correction → clean discovery → decision; one justified aggregate per clean review without acceptance duplication | .5 |
| P-07: New ART-012 report, reproducible current claims, distinction between structure/runtime/role behavior, explicit unrun gaps | .6 audits .1–.5 |

ART-001/002/003/004 preparation proof is owned by .2; ART-006/007 disposition
proof by .3; ART-008 recording/consumption proof by .4; corrected ART-004/005/006/007
proof by .5; ART-009/010/011 qualification receipts by .1; ART-012 by .6.
These are task-local observations of existing contracts, not new runtime
ownership. No `docs/contracts` registry exists; expected contract impact is
none beyond the planned qualification evidence. Preserve all listed stable refs.

## Handoff

Prepare dependency-ready executable leaves only: derived `verification.md`,
then ready standalone guided `preflight.md`, before implementation. Never launch
this composite parent. Each leaf requires its own immediate independent review
route; .6 closes evidence composition. Finishing documentation with unrun gaps
does not authorize orchestration implementation or certify behavioral qualification.
