# T-005.1 correction-03: discovery-01 source closure

Implemented: READY_FOR_REVIEW (documentation correction only).

Authority: `brief.md` revision 1; `verification.md` revision 1;
`preflight.md` decision context; `controller-contract.md`.
Preceding evidence: `reviews/discovery-01.md`, partial discovery, no acceptance verdict.

## Correction and evidence

F-01 invariant: primary operating instructions must describe supported separate
acceptance admission and bounded recovery consistently with runtime.
Updated `../../../../SKILL.md` and `../../../../references/operator-guide.md`:
replaced raw-claim/future-work statements, removed the obsolete unsupported-feature
entry, documented acceptance reservation/observation, dispositions, recovery and
shared correction accounting, and linked the implemented T-005.1 contract.
Completion, automatic recovery and live qualification limits remain explicit.
No runtime, schema, test, plan, installation or index bytes were changed by this correction.

Installer inspected: task-orchestrator is not in DEVELOPMENT_SKILL_SOURCES;
no profile/shared runtime change is needed. Measurement is N/A for prose only.
Existing contract declarations/module docs already cover the implemented seam;
no reusable contract changed, so no subsystem/index regeneration is needed.
The registry owner must independently confirm G-REG closure.

Implementation checks:
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=skills/task-orchestrator/tests python3 -m unittest test_actor_operations.ActorOperationsTest.test_acceptance_v12_documented_cli_and_changed_schema_boundary -v`: 1 passed; real local actor/CLI setup. This is not Draft 2020-12 proof.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py`: 4 passed.
- `python3 tools/check_contracts.py --root .`: passed, 8 subsystems / 37 references.
- Static source trace: the four contrary F-01 surfaces are replaced by the current admission/recovery instructions, with limits checked against controller-contract.md.

Raw logs: `/tmp/T-005.1-correction-03-{v12,architecture,contracts}.log`.
No new tests were added for the prose correction. No general maintainability
review is required by discovery-01 for this prose-only delta.

Process deviation: the attempted pre-edit ledger generator matched 88 rows
(including two sub-boundaries) and failed its 86-row assertion. The source edits
then ran before the complete map was persisted. This report records that gap;
it does not claim the pre-edit gate was satisfied. The complete mapping follows.

## Preserved discovery ledger

Prior statuses remain unchanged. Passing rows are navigation only, not renewed
review evidence. Fresh discovery owns reuse/recheck; separate acceptance owns
disposition. No approved deferral is inferred.

| Row | Prior status | Correction evidence / next owner |
|---|---|---|
| V-01 | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-02a | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-02b | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-02c | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-02d | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-02e | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-02f | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-02g | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-02h | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-02i | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-02j | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-02k | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-02l | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-02m | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-02n | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-02o | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-02p | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-02q | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-02r | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-02s | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-02t | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-03a | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-03b | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-03c | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-03d | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-03e | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-03f | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-03g | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-03h | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-03i | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-03j | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-03k | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-03l | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-03m | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-03n | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-04a | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-04b | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-04c | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-04d | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-04e | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-04f | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-04g | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-04h | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-04i | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-04j | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-05a | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-05b | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-05c | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-05d | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-05e | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-05f | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-05g | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-05h | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-05i | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-05j | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-06a | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-06b | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-06c | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-06d | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-06e | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-06f | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-07a | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-07b | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-07c | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-07d | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-07e | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-07f | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-07g | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-07h | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-07i | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-08 | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-09a | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-09b | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-10a | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-10b | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-10c | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-10d | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-11a | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-11b | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-11c | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-11d | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-11e | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-11f | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-11g | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-11h | pass | Runtime/test bytes unchanged; previous probe is navigation; fresh discovery owns reuse/recheck. |
| V-12 | fail | Source reconciliation and existing V-12 test pass as implementation evidence; fresh discovery rechecks documentation/schema. |

Additional duties (prior status preserved): V-12-CLI pass (current implementation
regression passes); V-12-DOC fail (F-01 corrected, fresh source trace owed);
V-12-SCHEMA/G-SCHEMA blocked (python3 cannot import jsonschema; capability owner
supplies runnable Draft 2020-12 validator, fresh discovery executes saved positive
and negative controls); MNT-01 pass (unchanged code, navigation); G-REG blocked
closure (registry owner confirms source/reference reconciliation); G-NATIVE
unchecked (fresh discovery owns `python3 tools/verify.py`, not run here).

Next: registry closure -> fresh independent task-review-discovery completing
F-01 regression, schema controls and justified aggregate -> separate
task-acceptance-review. Preserve discovery-01, maintainability-04, correction-02,
their original evidence and all blocked/unchecked statuses for those owners.
No independent review or acceptance was executed in this correction.

## Corrected byte identities

- `skills/task-orchestrator/SKILL.md` SHA-256: `a59e3a68cf6fc8885785bb5ae319fbb0955cdbfb552e0076e4509db56b768aaa`
- `skills/task-orchestrator/references/operator-guide.md` SHA-256: `95d9e572da7e7cc85a64941abeb888c635af56b5917409b0ded70f7919a2f3a7`
