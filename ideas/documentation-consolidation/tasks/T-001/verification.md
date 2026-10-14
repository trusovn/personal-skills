# Verification Design: T-001 — Audit preservation and retirement eligibility

Source brief: ideas/documentation-consolidation/tasks/T-001/brief.md
Source brief revision: SHA-256 `94cc2e185f1aef939a17d23db629cfef90bd33d6aca7727ad3de1ddaf65a2ebf` (current working-tree bytes)
Verification revision: 2
Authority: derived from the task brief and its cited normative sources
Status: ready

Revision 2 records the owner's 2026-10-14 clarification that standard run-evidence
instrumentation is required and its authorized effects do not fail AC-05.
Scenario IDs are unchanged. Prior preflight bindings and review dispositions
remain historical; focused preflight and renewed discovery must use revision 2.

Normative sources: [task brief](brief.md), [owner-approved direction](../../../documentation-consolidation.brief.md), [cleanup-v1 plan](../../project-plan.md) §§1–2, 4, 8 FLOW-001, 10–12, and [task map](../../task-map.json) T-001 / IF-001. The [plan review](../../project-plan-review.md) accepts planning, not current eligibility or cleanup permission.

## Coverage summary

| AC / risk row | Scenarios | Notes |
|---|---|---|
| AC-01 | V-01 | Reconcile exact membership, versions, identity, modes and Git states with real inputs; unresolved assets block affected scope. |
| AC-02 | V-02 | Original completion evidence and pending obligations determine dispositions; summaries and structural success cannot substitute. |
| AC-03 | V-03 | Trace executable input closure and classify reference carriers; retain existing evidence owners, scenarios, oracles and selectors. |
| AC-04 | V-02, V-04 | Separate candidate dispositions from global owner gates and reconcile the aggregate assessment. |
| AC-05 | V-05, V-06 | Prove read-only scope, attribute task artifacts and invalidate facts on observed drift. |
| R-01 / INV-001, INV-006 | V-01 | Cover all specified Git/version and content-boundary cases present; establish absence of remaining cases by scoped inspection. |
| R-02 / INV-004, INV-006 | V-02, V-04 | Reconcile all candidate families and present dispositions; keep future-work, stale notes and the old plan review outside retirement. |
| R-03 / INV-003 | V-03 | Independently follow real readers through setup/fixture inputs; search matches alone cannot prove closure. |
| R-04 / INV-006 | V-05, V-06 | Compare audit-start and final state; observed drift prevents stale assessment and never permits restoring user files. |

These scenarios evaluate the audit's `results.md` (ART-002), not archive recovery, migration equivalence or retirement. `Status: ready` applies to this verification design; current executability remains for preflight. An accurate blocked audit can satisfy T-001.

## Verification scenarios

### V-01 — The manifest accounts for exact originals, not just committed paths

Covers: AC-01; R-01 / INV-001, INV-006

Intent: Reject an inventory that lists only HEAD or tracked paths, collapses different index/worktree versions, or treats a Git pointer as preserved external content.

Given:
- The candidate boundary is material within `docs/tasks/`, the old `docs/project-plan.md` and old `docs/task-map.json`.
- Other relevant preservation inputs may include dirty, nontracked or ignored evidence and the untracked cleanup planning package; inclusion never grants deletion permission.

When:
- Reconcile ART-002 against scoped Git/index/filesystem reads and the relevant input closure identified by the audit.

Then:
- HEAD and scoped Git state are recorded. Every candidate and other relevant preservation asset has an exact path, byte identity/hash, file type/mode, tracked/index/worktree state, and proposed inclusion/exclusion with reason.
- Different index and worktree versions have distinct identities; deletion, type and symlink cases are represented without inventing current file bytes.
- Relevant untracked/ignored inputs are explicit. Unrelated files and secret contents are not indiscriminately collected.
- Discovered LFS, submodule or other external-content boundaries are identified with the limit of ordinary Git-object preservation. Inaccessible or unresolved assets block affected scope.
- No omitted or unreadable asset is represented as a complete preservation finding.

Oracle / boundary:
- Independently rebuild the scoped inventory from Git objects/index and actual filesystem entries, then compare path membership, versions, hashes, types, modes and decisions with ART-002. Check exclusions against their recorded reasons and scope.

Variants:
- Tracked unchanged, staged, unstaged, untracked and relevant ignored assets; index/worktree divergence; ordinary files and any discovered external-content boundary; deletion/type/symlink cases when present. Verify and record scoped absence for cases not found rather than fabricating them.

### V-02 — Eligibility preserves evidence, unfinished work and retained families

Covers: AC-02, AC-04; R-02 / INV-004, INV-006

Intent: Reject completion inferred from a task index, commit label, future catalog or structural check, and retirement that hides pending obligations or expands into retained documents.

Given:
- Original completion, review/result, qualification and pending-work records are available for inspection, or their absence is observable.
- `docs/future-work/`, including `stale/`, the old `docs/project-plan-review.md` and unrelated docs must remain outside retirement.

When:
- Reconcile every candidate's disposition and each discovered pending obligation in ART-002 with its original evidence and relevant active backlog context.

Then:
- Each candidate cites actual completion, review/result and qualification evidence, or explicitly records unknown evidence. Historical verdicts and unrun limits retain their meaning.
- Every discovered obligation identifies original evidence, proposed retained active context/next owner, and either a confirmed disposition with its source or an unresolved owner gate.
- Unfinished or unknown cases cannot be silently eligible. Unresolved dispositions block affected retirement; a confirmed disposition does not claim that historical qualification gaps were closed.
- All three candidate families are reconciled. Retained families remain outside deletion scope even if they are part of preservation.
- The audit confirms the owner's “future-tasks” terminology against `docs/future-work/`, or records a contradiction for the owner.

Oracle / boundary:
- Compare manifest rows directly with original reports, verdicts and obligation references. Challenge apparent completion against the underlying evidence and follow pending-work links through to proposed retained context and decision sources. Reconcile the full candidate inventory, not a sample alone.

Variants:
- `docs/tasks/`, old project plan and old task map; completed, unfinished and unknown dispositions where present; future-work including stale notes and the old plan review. Record absence of a disposition class rather than inventing a candidate.

### V-03 — The consumer map closes real input dependencies and classifies references

Covers: AC-03; R-03 / INV-003

Intent: Reject a top-level path search that misses embedded input pointers or setup dependencies, and a map that confuses historical mentions with live consumers.

Given:
- Candidate paths may be read by executable consumers or carried in navigation, composition records, fixtures, inventories and evidence/scenario pointers.
- Known starting points are `tests/test_review_composition.py`, `tests/review_fixture_support.py`, `tests/staging_fixture_support.py` and `tests/README.md`; these are starting points, not a complete consumer list.

When:
- Check the audit's recorded search roots/patterns and follow discovered real readers through their required source, reference and fixture/setup inputs.
- Reconcile the proposed T-003 input and verification map with existing coverage/helpers and ownership declarations.

Then:
- Each discovered live consumer has source locations, the complete necessary input closure, existing owner, decisive scenarios/oracles and narrow existing verification selectors.
- Executable dependencies, active navigation and historical-only references are distinguished. Historical mentions alone do not demand executable migration; active navigation is still recorded.
- The audit inspects existing coverage/helpers before proposing retained inputs and identifies installer coupling when managed inputs would change.
- Embedded pointers and setup/root/path calculations are included when necessary to the traced closure; recording only top-level constants is insufficient.
- Commands, observations and limits are explicit. Selecting a suite is not reported as running it; neither source inspection nor a passing structural check claims behavioral equivalence.

Oracle / boundary:
- Independently trace real reader/setup code and its referenced data, compare every required input with ART-002, and inspect search coverage for omitted carriers. Compare scenario/oracle/selector claims with their existing evidence owners. The known baseline selector is `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_review_composition.py`; additional selectors depend on discovered consumers.

Variants:
- Executable reads, transitive fixture/setup inputs, active navigation and historical-only references. Include discovered composition/evidence pointers and consumer setup such as `docs/tasks/T-005.1/setup_consumer.py`; do not assume the known examples close the search.

### V-04 — Owner gates determine the assessment without implying permission

Covers: AC-04; R-02 / INV-004, INV-006

Intent: Reject an audit that silently chooses preservation/archive settings, treats owner silence as approval, or lets eligible rows hide a global blocker.

Given:
- ART-002 contains preservation, candidate-disposition and consumer facts.
- Q-001–Q-003 decisions may be supplied or remain unresolved.

When:
- Reconcile each gate and the per-candidate/overall assessment against current facts and actual supplied owner decisions.

Then:
- Q-001 exact inclusion; Q-002 unused tag, destination, publication authorization and existing navigation location; and Q-003 completion/pending-work dispositions each have a sourced decision or a stated question, owner and affected later task.
- Every candidate has an eligibility assessment and the audit has an overall `ELIGIBLE` or `BLOCKED` assessment consistent with its facts and gates.
- Unresolved global preservation/archive choices block archive advancement. Unresolved candidate dispositions block affected retirement. Silence and plan acceptance do not settle either class of gate.
- Even `ELIGIBLE` is explicitly an assessment, not archive execution or deletion permission. A blocked audit remains a valid T-001 output when its facts and limits are complete and truthful.

Oracle / boundary:
- Compare decisions with their cited owner sources, then reconcile each blocker with candidate rows, the aggregate result and the named downstream handoff. No Git side effect or later-task execution is needed to prove this audit contract.

Variants:
- Supplied decisions and unresolved gates where present; global versus candidate-specific blockers. Inspect actual cases without making missing owner decisions to manufacture an eligible case.

### V-05 — A stable audit preserves protected state and attributes instrumentation

Covers: AC-05; R-04 / INV-006

Intent: Reject an audit that edits originals, stages inputs, changes refs outside the run-evidence namespace or counts its new output as original preservation evidence. Standard run-evidence instrumentation is required and is not itself an audit failure.

Given:
- Initial scoped input identities, Git state, index and refs are recorded before the audit output write.
- No external drift is observed during this audit occurrence.

When:
- ART-002 is written to `ideas/documentation-consolidation/tasks/T-001/results.md` and final scoped identities/state are checked.

Then:
- Audited inputs, existing user work, index and refs outside `refs/personal-skills/run-evidence/` match the initial state.
- Run-evidence metadata, snapshot objects and begin/recovery/finish refs are authorized instrumentation. Record their effects separately; namespace membership does not authorize changes to protected files, the index or other refs.
- New audit output is attributed, and preparation/review artifacts remain distinct from original preservation inputs. Preparation/review files are not overwritten as audit output.
- No archive/tag/publication, staging, deletion, migration, navigation/backlog edit, report rewrite, installation refresh or live-model eval is performed.

Oracle / boundary:
- Compare actual before/after scoped paths, contents/hashes, types/modes, status, index and refs with the recorded baseline; distinguish authorized run-evidence changes from protected-state drift and inspect the attributed change set rather than relying solely on the author's read-only claim.

Variants:
- Audit start → output write → final identity check with stable inputs. Observed drift follows V-06.
- Authorized begin/recovery/finish instrumentation changes are attributed without failing V-05; changes to protected state still fail it.

### V-06 — Observed drift invalidates affected facts until reinspection

Covers: AC-05; R-04 / INV-006

Intent: Reject reuse of an earlier assessment after its inputs change, including a later correction that retains stale identities or overwrites user work to restore the baseline.

Given:
- A scoped input identity/state differs from the audit baseline or from facts reused during a subsequent audit correction.
- The changed input supports preservation, eligibility or consumer findings.

When:
- The implementer detects the difference while checking final state or revalidating affected facts.

Then:
- The drift and affected facts are recorded; those facts are invalid until the changed inputs are reinspected.
- Any assessment relying on unrevalidated facts stops for the affected scope and cannot be presented as current eligible evidence.
- Reinspected facts are tied to current identities; untouched findings are not silently claimed to cover changed inputs.
- User files are never restored or overwritten to make the baseline match. Attribution distinguishes the audit's writes from observed input drift.

Oracle / boundary:
- Compare recorded initial/final identities and any correction evidence with actual current Git/filesystem state, then trace affected rows to their reinspection or explicit blocker. An old passing record cannot waive the difference.

Variants:
- Observed drift during the audit or a subsequent correction. If no drift occurs, record its verified absence under V-05; this design does not require modifying originals or introducing a fault-injection harness.

## Implementation handoff

- Treat this file as derived verification guidance, not a replacement for the task brief.
- Preserve stable scenario IDs across a reasoned coverage revision. A revised artifact supersedes affected readiness and evidence until focused preflight produces a ready result for the new revision.
- Implement the smallest audit and verification work that satisfies the brief. Reconcile real source inputs; syntax/schema/path searches alone do not prove these scenarios. Do not introduce production or test changes for this evidence-only task.
- Concrete inspection commands and evidence structure remain implementation choices within repository authority. T-001 selects consumer checks; running consumer suites, network checks or live models is not required to produce this audit.
- Obtain ready `preflight.md` before implementation. Route inaccessible inputs/capabilities to preflight and unsettled expected behavior to task design or the owner; do not silently weaken an oracle.
- After implementation or correction, the brief requires fresh independent discovery and a separate acceptance decision. These scenarios guide that evidence; this design does not perform either review or certify audit correctness.
