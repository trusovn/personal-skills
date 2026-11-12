# T-004.1 implementation evidence

Authority: [brief.md](brief.md) revision 1, [verification.md](verification.md)
revision 1, [preflight.md](preflight.md). Guided implementation submission;
independent review and acceptance remain outstanding.

The controller inspects terminal producer outcomes against actual Git and file
state, reserves verification through its existing ledger, and executes frozen
commands through the existing runner. It retains candidate and execution history,
refuses stale eligibility, and preserves unresolved ownership on interruption.
See [controller-contract.md](controller-contract.md) for actual API/CLI names,
artifact paths, authority and collector rerun semantics.

Deliverables: controller inspection, verification, status and CLI; workspace
identity and scope checks; explicit YOLO runner selection and execution-record
validation; focused tests and this producer handoff. Durable cross-task impact:
ART-003 and ART-005 producer records, current candidate/check evidence in ART-002,
and the producer slice of IF-003. Executable declarations: `scripts/controller.py`
(public dispatch and durable receipt fields), `scripts/controller_git.py`
(workspace identity), `scripts/controller_state.py` (execution-record validator),
`scripts/verification_runner.py` (execution parameter and recorded mechanism).
There is no pre-existing standalone JSON schema for these execution records;
existing actor/policy/manifest schemas are unchanged. Registry/reference
synchronization belongs to its designated stage after maintainability review.

## Scenario evidence

`actor` means `test_actor_operations.py`; `Git` means `test_controller_git.py`;
`runner` means `test_verification_runner.py`. The tests use disposable real Git
repositories, real local actor subprocesses with a fake Codex executable, and
actual commands and logs. They do not prove real Codex/sbx/provider behavior.

| Scenario | Implementation evidence and limits |
|---|---|
| V-01 | Actor `test_producer_real_check_replay_and_stale_bytes` uses an actual terminal implementation and verifies the public check's exact output/exit/replay. Git unusual-path controls cover literal path handling. Independent discovery still owes its own observed candidate-byte corroboration. |
| V-02a–d | Actor scope refusal, unchanged baseline setup and staged-owner regression; Git dirty/rename/delete controls. Dirty staging comparison covers a same-status, same-worktree-bytes change. Not every dirty and outside-scope permutation is repeated at the public boundary. |
| V-03a–f | Actor `test_producer_assignment_refusals_do_not_mutate_or_launch` checks wrong stage, operation, run/task, input/policy/flow and candidate references; drift/exclusion test holds the real lock while a second request refuses. Existing actor controls prove live/unknown upstream ownership. Partial receipt regression ensures no admission or second owner. |
| V-04a–e | Actor pass/replay/stale and correction history tests; Git same-size and untracked identity controls; accepted T-003 revision tests exercise actual frozen-input changes. New public tests do not independently vary every configuration or authority revision. |
| V-05a–c | Git `test_candidate_workspace_ignored_evaluated_input_and_visible_drift` shows generated output alone keeps identity and evaluated ignored bytes change it. Public synchronized drift and side-effect controls exercise the same pre/post comparison; no dedicated live ignored-input mutation case was run. |
| V-06 | Real public check with exact log bytes/exits and CLI replay; runner `test_explicit_yolo_uses_production_runner_without_sandbox_substitution` checks binary stdout/stderr and literal path arguments. Existing ordered multi-command runner test retains its legacy boundary. |
| V-07a–e | Runner real YOLO success, invalid authority matrix including integer-for-boolean, legacy fail-closed cases, and host containment matrix. Current checked-host results below. No platform fallback. |
| V-08a–d | Actor invalid later command refuses before any launch; existing runner shell/install tables and actual quoted argv execution. Authorized install is planning evidence only; no package install executed. |
| V-09a–f | Actor real failure, missing later executable, correction routing, and read-only replay; targeted gate omission is recorded on the public receipt. Existing planner/executor checks preserve mandatory failures and stop later commands. A generic nonzero executable exit is recorded as failure; no classifier infers arbitrary infrastructure causes from output text. |
| V-10a–e | Synchronized real command observes correct content, then tracked/untracked drift; even exit zero remains stale. Separate command side effect also produces stale. YOLO group cleanup reuses actual timeout, resistant child and open-pipe controls. Invalid timeout matrix preserves ledger and marker absence. |
| V-11a–e | Actor exact CLI/API replay; killed replacement controllers before launch, during command, and after receipt publication; no relaunch while unresolved, one execution on reconciliation. Public log collision and runner publication failure retain prior/partial evidence. |
| V-12 | Real failing check, inherited charged correction, distinct passing result and immutable failure receipt. Replaying old assignment cannot restore current pass or rerun. |
| V-13 | Producer contract documents actual call signatures, frozen authority, path/digest semantics, replay and collector rerun. Independent comparison against the public interface and raw evidence is still owed. |

Real sbx/provider qualification and the composed collection/correction workflow
remain T-006 and T-004.2 work, respectively. An evaluated ignored file must be
named in the frozen allowed paths; there is no arbitrary command-read discovery.
No tamper resistance or power-loss recovery is claimed.


## Maintainability evidence

Original JSON/text pair: `.quality/reports/T-004.1-preflight-20261110-01.json`
and `.quality/reports/T-004.1-preflight-20261110-01.txt`. The applicable final
pair is `.quality/reports/T-004.1-implementation-20261110-02.json` and
`.quality/reports/T-004.1-implementation-20261110-02.txt`. The earlier `-01`
implementation pair is retained as historical evidence. All use the same logical
repository and configured Radon/Ruff identities. The final comparison is complete
and compatible for the seven changed Python files; each report `files` entry
contains the checked source hash. No scope outside the starting folders was added.
For an isolated review, transfer the exact original/final JSON/text pairs at the
same relative paths; they are ignored locally and will not travel with commits.

Retained or new breaches in materially edited functions (final `-02` report):

| Function | Measured change | Reason and considered alternative |
|---|---|---|
| `controller.init_run` | CC 16→16, statements 66→66 | Freeze the index tree in the existing initial-baseline publication. A separate baseline transaction would split one authority bundle and add a migration boundary. |
| `controller.inspect_candidate` | New CC 24, 41 statements | Terminal authority, initial owner scope and artifact eligibility belong under the same lock. Git capture and staged-path comparison are separate Git helpers; a second admission layer would duplicate the authority decision. |
| `controller.check_candidate` | New CC 27, 62 statements | The locked sequence must keep validation, replay, intent, execution, drift and publication in order. Identity and ledger publication already have separate helpers. A separate backend or ledger would add a second lifecycle; independent review can assess local replay extraction if it improves navigation. |
| `controller._reservation_options` | CC 21→25 | Check ownership and allowed evidence actions share existing reservation precedence. A second dispatcher would obscure active-operation and correction priority. |
| `controller.status_run` | CC 10→15 | Staleness is a read-only view of one ledger snapshot. Keeping it here avoids invalidating historical receipts on a status read; an extra public status interface would duplicate authority loading. |
| `controller.reserve_operation` | CC 30→32 | Validate candidate eligibility before publishing the existing verifier reservation. An external precheck would create an unguarded gap. |
| `controller.build_parser` | Statements 45→53 | Two CLI commands share one local parser loop. Moving that loop alone would add indirection without changing parser responsibility. |
| `controller_state.validate_command_execution_record` | CC 42→44; statements 78→82 | The optional mechanism value is validated in the same record shape check. A separate record validator would duplicate outcome/log semantics. |
| `verification_runner.execute_verification_plan` | CC 53→60; statements 158→167; args 8→9 | The single explicit authority input selects invocation and adds direct-run group terminality and mechanism evidence. A parallel runner would duplicate executable preflight, logging, timeouts and cleanup. |

These are advisory findings for the maintainability reviewer, not acceptance
claims. Unchanged legacy hotspots do not justify unrelated edits.

## Verification results and retained evidence

All commands ran from the repository root. Final checked source/test bytes match
all seven `files` hashes in the final `-02` measurement report.

| Command | Result / retained output |
|---|---|
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p test_actor_operations.py -k hidden_staged` | Fail-first: one failure, because altered staging was incorrectly admitted despite unchanged status/worktree bytes. `/tmp/T-004.1-staged-before.log`. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p test_actor_operations.py -k test_producer` | Final: 15 passed, including that staged-owner regression; `/tmp/T-004.1-producer-final-02.log`. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p test_verification_runner.py -k yolo` | Six passed; actual local argv, invalid authority, timeout/descendant cleanup. `/tmp/T-004.1-yolo-final.log`; final aggregate also covers these bytes. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py` | Four passed; whole-repository CLEAN policy, no debt baseline. Captured through local run-evidence check on final code. |
| `PYTHONDONTWRITEBYTECODE=1 python3 tools/verify.py` | Final approved host-level run: 7 checks, 0 failed; orchestrator 246 passed; root 311 run, 32 skipped; other suites 3/13/4 passed. Includes real legacy containment checks. `/tmp/T-004.1-verify-final.log`. |
| `python3 tools/check_contracts.py --root .` | Final aggregate constituent: 8 subsystems / 33 references valid. Registry synchronization still owed after maintainability review. |
| `python3 scripts/install_development_skills.py --check .` | Final aggregate constituent: 112 paths compared, no drift. Active installation was not refreshed. |
| `git diff --check` | Clean. User task package/index work remains separate. |

Root skips: 31 require the dedicated pinned Radon/Ruff interpreter and one
requires real pinned dependencies. The separate final maintainability comparison
used the available pinned analyzer tools; it does not retroactively pass these
skipped tests. No real sbx/provider check was run.

Historical failures remain visible: `/tmp/T-004.1-orchestrator.log` is the
sandboxed suite (235 tests, 4 failures, 13 errors); its containment capability
was denied and an actor interruption missed a checkpoint. The first approved
host suite (`/tmp/T-004.1-orchestrator-host.log`) ran containment successfully
but failed one producer test on a partially published T-003 terminal receipt.
The controller now treats incomplete JSON as unresolved rather than admitting
it or granting another writer; the focused receipt regression and final
aggregate pass. `/tmp/T-004.1-verify-pre-index.log` is the green intermediate
gate before the staged-owner correction and is superseded for final source bytes.

Raw final local proof: `/tmp/T-004.1-final-proof-vmmal5uo/observations.json` and
its `run/` sibling preserve candidate records, a failing check, inherited
correction, a passing check with distinct logs, and stale eligibility after
subsequent drift. There were exactly two check invocations. This is retained
implementation evidence from a disposable fixture, not independent discovery.
Optional run evidence: `run-20261110T160857Z-11299d7003bf` in the local Git-metadata
run-evidence store.

## Submission route

Canonical architecture passed on final bytes. Next: fresh
`task-maintainability-review` → `task-contract-registry-updater` → fresh
independent `task-review-discovery` → separate `task-acceptance-review`.
Discovery must perform its own public candidate/check pass/fail and drift probes
and assess the partial permutations noted above. Do not start T-004.2 until the
producer is accepted. No plan, tracker, installation, commit or staging change
was made by this implementation.
