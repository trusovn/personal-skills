# Verification Design: T-003.2 — Report every confirmed bounded maintainability blocker

Source brief: docs/tasks/T-003.2/brief.md
Source brief revision: SHA-256 9ef8e1459b99fab8deca899d21bf20215f9c5942ac6a081f5e93b3f51c98d88c
Verification revision: 1
Authority: derived from the task brief and its cited normative sources
Status: ready

The brief has no declared revision number; its digest identifies the source
bytes. Normative sources are `docs/project-plan.md` (sections 1, 7/IF-003,
10/T-003 and 11), `docs/task-map.json` (T-003), and
`docs/tasks/T-003/brief.md` (P-02/P-07 within this leaf's scope).
Ready describes this design, not repository executability or passing behavior.

## Coverage summary

| AC / risk row | Scenarios | Notes |
|---|---|---|
| AC-01 | V-01, V-02 | No count-based output or discovery stop; four independently evidenced defects, complete actionable finding fields and impact ordering. |
| AC-02 | V-03, V-04, V-05 | Changed/influenced scope, safe probes, truthful interrupted coverage and preserved gate/verdict/independence rules. |
| AC-03 | V-02, V-03, V-05 | Non-blocking preference control, no quota or speculative redesign, and all three existing eval expectations retained. |
| R-01 / IF-003 / INV-008 | V-01, V-02, V-03, V-04 | Four distinct blockers versus preference; complete inspection versus a genuine permission/capability/budget stop. |

## Evidence boundary and setup

This leaf owns source guidance and reusable qualification inputs. Local policy
checks must inspect the meaning of the review protocol, verdict rules, output,
definition of done, eval expectations and any stale maintainability guide
entries. A new sentence permitting all blockers cannot compensate for a cap or
verdict-sufficiency stop elsewhere. Demonstrate that focused checks reject the
current three-blocker cap and enough-blockers stop for those reasons, rather
than because fixture setup fails. These are contract checks, not observed agent
compliance.

Fixture evidence must cross the real filesystem/Git and changed-production
boundaries: stage the task-owned setup in a disposable Git workspace, identify
its baseline and actual diff, and execute its supplied local operations/probes.
Supply a legitimate task, authorized changed/influenced scope, maintainability
policy and applicable architecture-gate inputs. Each of the four defects needs
an independent location, introduced/worsened condition, decisive code/dependency
or runtime observation, concrete maintenance consequence and bounded correction
direction. Runnable code alone or four labels in eval metadata are insufficient.
Maintainability defects need not cause incorrect functional output; observe the
actual coupling, duplicated authority, locality or other stated design condition
when that is the decisive boundary.

Reuse relevant existing coverage and stdlib setup conventions. Existing evals
1–3 cover self-check, unavailable gate and invalid report path; current report
path coverage also exists in `tests/test_task_preparation_contracts.py`.
Preflight resolves fixture selectors, commands and the focused test owner; do
not assume the historical reviewer module exists or introduce a shared runner.

Local evidence proves policy and fixture properties. It does not prove that an
agent discovered or reported the fourth blocker, respected a stop, or emitted a
correct verdict. Live agent evals require separate authorization and remain
unrun here; T-005 owns actual role compliance. T-003.4 owns composed guidance
and installed projection. Neither adds a cross-task scenario to this design.

## Verification scenarios

### V-01 — A sufficient verdict does not truncate bounded findings

Covers: AC-01, R-01

Intent: Reject an unchanged three-blocker cap, a relocated reporting cap, or
discovery ending merely because a verdict is already justified.

Given:
- V-02's four distinct material defects are within authorized review scope.
- Inspection of that scope and affordable safe probes can complete without a
  genuine permission, capability or budget stop.
- Earlier defects already suffice for `CHANGES_REQUESTED`; the fourth remains
  a separate required inspection, not another symptom of those defects.

When:
- Audit the complete source review/report contract and supplied case
  expectations for the discovery and reporting obligations in this state.

Then:
- Finding count and verdict sufficiency cannot end discovery or cap output.
- All four confirmed blockers remain separately identifiable in the required
  correction set; none is omitted, merged away or relegated to warnings to fit
  a count limit.
- Every finding has stable identity/location, the introduced/worsened problem,
  evidence, concrete maintenance consequence and smallest correction direction.
- Findings remain ordered by architectural impact. Completeness does not
  authorize wider review or a quota of findings.

Oracle / boundary:
- Compare protocol, verdict, output and completion instructions plus fixture
  expectations against the four-defect inventory. Each defect must have a
  distinct mapping to a required actionable finding, including the fourth.
- Focused contract checks reject both old shortcuts independently. Inspect
  semantics as well as text so a paraphrased cap cannot pass.

Variants:
- Output truncation at three; discovery stop after verdict sufficiency.

### V-02 — The fixture exposes four independent production defects

Covers: AC-01, AC-03, R-01

Intent: Reject a prompt-only fixture, four assertions of the same underlying
defect, or a preference counted as the fourth material blocker.

Given:
- The supplied small setup can create a disposable Git workspace with a
  legitimate task/policy, baseline, changed production and non-blocking
  preference control.
- The supplied defect inventory identifies four distinct locations/conditions
  and explains the observable evidence and concrete maintenance cost of each.

When:
- Stage the setup, inspect the real baseline/diff, run its local production
  operations and apply each supplied defect/control probe.

Then:
- Changed production is runnable, and each claimed defect is independently
  observable in the actual changed bytes or behavior.
- Baseline comparison establishes that each defect was introduced or worsened
  by the change; untouched debt does not supply a missing blocker.
- Four independent problems remain four. A shared symptom, label, source-string
  assertion or successful startup alone cannot establish that inventory.
- Each defect has a concrete expected-maintenance consequence and smallest
  correction direction supported by task/policy context.
- The preference control has no demonstrated material regression and is
  explicitly non-blocking.

Oracle / boundary:
- Record the baseline/diff, executed operations, and four separate decisive
  observations at the actual production/code/dependency boundary. Trace each
  observation to its own consequence and correction direction.
- Audit the preference control against the same materiality standard. Neither
  setup success nor eval metadata proves that a reviewer reported any finding.

Variants:
- Each of the four supplied defects and the non-blocking preference control.

### V-03 — Completeness preserves scope and materiality

Covers: AC-02, AC-03, R-01

Intent: Reject replacing a cap with exhaustive repository review, a required
finding quota, or speculative preference blockers.

Given:
- The task authorizes its changed production and immediate influenced surfaces.
- V-02 supplies material defects and a preference control, with task/policy
  context sufficient to distinguish them.

When:
- Audit scope, probe and materiality instructions and supplied expectations
  against that authorized boundary and the defect/control evidence.

Then:
- The contract requires all confirmed blockers found through bounded safe
  inspection, without expanding into a repository-wide survey or unsafe probes.
- Blockers require an introduced/worsened condition, evidence and concrete
  maintenance impact; unchanged unrelated debt does not become a task blocker.
- The preference control remains a warning/observation or is omitted. No quota,
  style preference, speculative redesign or demand for global optimality
  creates a correction obligation.
- Automated warnings remain investigation leads, not automatic blockers.

Oracle / boundary:
- Inspect published scope/materiality rules and fixture expectations against
  the authorized surfaces and supplied evidence. Reject any rule that requires
  extra findings or makes the preference control blocking merely to reach four.

Variants:
- Four confirmed material defects; supplied non-material preference control.

### V-04 — A genuine stop retains outstanding coverage

Covers: AC-02, R-01

Intent: Reject claiming clean completion from an interrupted review, hiding
unfinished proof, or disguising count-based stopping as a safe-budget stop.

Given:
- Required bounded inspection or proof is still outstanding.
- A specific permission, capability or safe-budget limit genuinely prevents
  the remaining work; the reviewed subset and unreviewed remainder are known.
- Contrast this with V-01's affordable complete inspection after enough
  blockers already justify a verdict.

When:
- Audit the stopping and report/handoff contract for both states.

Then:
- A genuine stop retains confirmed findings and identifies outstanding
  coverage, the concrete stop reason and next owner.
- Required missing proof cannot become `ACCEPT` or a claim of clean completed
  review. Disposition follows the existing gate/verdict rules; the stop does
  not erase a confirmed blocker or fabricate evidence.
- Finding count or verdict sufficiency is not a stop reason when authorized
  inspection remains affordable and safe.

Oracle / boundary:
- Trace the source instructions and supplied complete/partial expectations from
  starting scope and known stop facts to retained findings and explicit
  unfinished coverage/reason/owner. Missing proof must remain visible.
- Audit the stop justification against authority and budget, rather than
  accepting a generic label such as "enough findings" or "partial".

Variants:
- Genuine permission, capability and safe-budget stops; no genuine stop despite
  an already sufficient blocker set.

### V-05 — Existing gate, independence and report-path safeguards survive

Covers: AC-02, AC-03

Intent: Reject weakening an existing safeguard while removing the cap, or
discarding distinct eval cases as redundant with the new four-blocker case.

Given:
- Current gate, verdict, provenance and durable-report contracts, with
  task-scoped changed bytes and the relevant policy/evidence for each case.
- Existing evals 1–3 retain their distinct setup facts: same-session authorship
  with a passing gate; missing `archcheck` with no fresh evidence/exception;
  and an external durable-report request for packaged `PAY-14`.

When:
- Compare the changed source contract and existing eval expectations against
  the following decision cases.

Then:

| Case | Required retained outcome |
|---|---|
| New/worsened hard gate violation, not a checker/config defect | `CHANGES_REQUESTED`; gate policy/baselines are not edited to pass review. |
| Unchanged baselined legacy violation | Not a task blocker merely because it exists. |
| Gate warning/heuristic | Semantic investigation, not automatic failure. |
| Passing gate | Continue semantic review; passing the gate alone is not a maintainability verdict. |
| Eval 1: reviewer authored the production bytes in the same session | `SELF_CHECK_ONLY`, gate `PASS`, no independent verdict; route to a fresh reviewer. |
| Eval 2: required gate cannot execute, no trustworthy fresh evidence or valid exception | `INCONCLUSIVE`, gate `NOT_AVAILABLE`; name command/missing capability, without editing policy, installing tools or substituting static review for required proof. |
| Eval 3: external durable report path for `PAY-14` | `INCONCLUSIVE` path-contract result before semantic review/write; refuse the invalid path and identify `docs/tasks/PAY-14/reviews/maintainability-01.md` as the canonical next path, preserving prior reports. |

- Existing independence and fresh-review invalidation after production
  correction remain binding. This stage still does not perform functional
  acceptance.

Oracle / boundary:
- Inspect policy branches and the retained eval prompts/expectations for every
  distinct outcome above. Reuse existing focused coverage, including numbered
  report-path checks, without claiming those checks executed a reviewer role.
- Changes to blocker completeness must not contradict another preserved branch
  or overwrite a prior durable report.

Variants:
- All decision-table rows; existing evals 1–3 remain distinct.

## Implementation handoff

- Treat this file as derived guidance, not a replacement for the brief.
- Preserve stable scenario IDs across a reasoned coverage revision. A revision
  supersedes affected readiness/evidence until focused preflight produces a
  ready result for the new revision.
- Implement the smallest production and test changes that satisfy the brief
  and exercise these scenarios. Concrete test structure, helpers and file
  placement remain implementation choices within the authorized ownership.
- Run targeted changed checks first, then the resolved focused owner. Stage and
  inspect the disposable fixture; keep structural checks, observed fixture
  behavior and unrun agent compliance separate in the evidence record.
- Inspect the canonical installer selection/guide/helpers without broadening
  ownership or changing selection. Hand T-003.4 exact task-owned setup inputs
  and packaging implications; it owns composed installer/guide checks.
- Hand T-003.4/T-005 exact fixture inputs, independent defect/control oracles
  and explicit unrun complete/partial reporting gaps. Do not run live agent
  evals without separate authorization or refresh active `.agents/` copies.
- If discovery cannot exercise a scenario at its stated boundary, route the
  conflict to task design/preflight rather than weakening the oracle. Readiness,
  implementation and independent acceptance are subsequent stages.
