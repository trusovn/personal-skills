# Q-01 completion amendment and qualification handoff

Authority: on 2026-10-12, the user selected completion with verified instructions
and runnable fixtures, assigning actual reviewer trials to a named later task.

Follow-up ID: `Q-01-QUALIFICATION`.
Owner: human coordinator / qualification owner.
State: unrun; follow-up scope recorded, not an executable ready task package.
Before execution, prepare its own brief, verification and preflight and obtain
authorization for model-budget checks. This handoff authorizes no trial runs.

## Q-01 completion boundary

Q-01 requires the instructions, executable defect/control/correction fixtures,
distribution checks and this complete handoff. Actual reviewer outputs are not
Q-01 acceptance requirements. Source acceptance must not be described as proof
that the reviewer behaves correctly in real calls.

This follows T-003.2's separation of local fixture proof from actual role
compliance. T-005's existing composed installed-flow scope is unchanged;
Q-01-QUALIFICATION is a separate follow-up, not an implicit addition to T-005.
Later qualification may reuse current evidence where it proves the same boundary.

The amended brief and verification revision 2 supersede earlier evidence-allocation
rules. Keep implementation.md and reviews/discovery-01.md and
reviews/maintainability-01.md unchanged as historical reports. Their observations
may support fresh review while the underlying bytes remain current; their old
completion-gap labels do not decide the amended contract. The earlier conversational
INCONCLUSIVE verdict is not converted into ACCEPT by this amendment.

The original preflight is superseded. Next: focused preflight renewal against
the amended brief/revision 2, then fresh discovery and separate acceptance.
Carry forward the recorded repository-installation deferral in implementation.md;
this amendment changes only role-trial ownership, not AC-06 or installation
permissions. Resolve that recorded authority separately in renewed preparation.

## Preserved follow-up cases

| Existing scenario / discovery row | Later decisive evidence |
|---|---|
| V-02 / V-02-role | Blind fresh reviewer detects duplicated scenario authority despite a green suite; actionable location, evidence, consequence and correction direction. |
| V-03 / V-03-role | Same defect trial detects the distinct shared mutable fixture failure with first/next-occurrence evidence. |
| V-04 / V-04-role | Fresh control review introduces no blocker for stable text or legitimate independent fixtures, and no invented gate/registry obligation. |
| V-05 / V-05-role | Actual authoring session returns SELF_CHECK_ONLY for reviewed test/eval/harness assets; independent session has different authorship. A hypothetical authorship prompt is insufficient. |
| V-06 / V-06-role | Fresh correction review rejects stale affected evidence, retains MNT-T1 confirmed and MNT-T2 corrected, preserves unaffected current scope and prior report, and writes only the next canonical report. |
| V-07 / V-07-role | Missing required gate yields truthful INCONCLUSIVE / NOT_AVAILABLE; tests-only handoff retains the actual first outstanding stage and full ordered remainder. |
| V-08 / V-08-role | Actual reports preserve complete findings, genuine-stop rows and read-only boundaries; before/after workspace records verify permitted report-only effects. |

## Reuse and execution inputs

- Source package: skills/task-implementation-flow/task-maintainability-review/.
- Existing setup: evals/files/setup_fixture.py in that package. Invoke with an
  explicit disposable EVAL_WORK_ROOT and one scenario: test-assets,
  test-assets-control, test-assets-correction or test-assets-stop.
- Existing catalog: evals/evals.json, cases 5–8 for prepared targets; case 1
  supplies the authorship contrast. Preserve real session authorship for V-05.
- Preserve existing four-blockers, genuine-stop and correction-round inputs
  where needed for V-08; do not build a new runner or duplicate fixture setup.
- Resolve the actual skill installation for each call. If an installed package
  differs, explicitly authorize source-guided execution; do not claim source
  presence means installation or refresh an active session.
- Record source identities and fixture Git baseline/diff, task authority,
  gate policy and exact commands. Give reviewers the prepared target and chosen
  skill, withholding setup code, eval expectations and task-runs oracle files
  until raw outputs are saved. The coordinator retains the held-back material.
- Compare raw outputs with the oracles afterward. Retain scenario IDs, session
  provenance, current byte identities, findings/dispositions and report-side-effect
  records. A corrected-byte trial needs a separate fresh reviewer.
- Combine compatible cases; do not rerun the full catalog merely for completeness.
  Failed fixture setup is not reviewer-behavior evidence.

## Evidence still owed

All role trials above remain unrun. Existing local probes prove fixture facts
and instruction presence only. Follow-up results must distinguish passes, fails
and concrete blocked/unchecked cases; missing actual outputs cannot establish
qualified behavior. Keep results separate from historical Q-01 reports.
