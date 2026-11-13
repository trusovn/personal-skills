# T-005.1 — correction for maintainability-02

Implemented: READY_FOR_REVIEW

Status and reservation now consume the same current-proof facts and the same
recovery decision. Invalidated review-correction authority requires intervention;
neither surface advertises an evidence retry or permits correction against stale
proof. Active operation ownership and the shared correction budget retain
precedence. This is implementation evidence, not an independent review verdict.

- Authority: [brief.md](brief.md), revision 1;
  [reviews/maintainability-02.md](reviews/maintainability-02.md), blocker 1.
- Preflight/context reference: [preflight.md](preflight.md) and
  [verification.md](verification.md), revision 1; current staged implementation
  and [controller-contract.md](controller-contract.md).
- Preceding verdict: CHANGES_REQUESTED.
- Finding/scenario IDs: maintainability-02 blocker 1; associated V-03 retained
  proof integrity, V-07 recovery, V-08 correction and V-09 budget behavior.
- Complete findings and invariant: duplicated recovery authority let status offer
  verification, reservation redirect to correction, and correction reject stale
  verifier proof. For identical retained evidence, both surfaces must derive the
  same authorized recovery actions; refusals preserve ledger/version/count.
- Influenced sibling surfaces: candidate, verifier, collection and acceptance
  proof drift; active writer/verifier ownership; correction exhaustion; ordinary
  check correction and environment repair; fresh preflight after repair; renewed
  collection after acceptance; fresh acceptance after losing its retained record.
  No correction authority is seeded in the lifecycle regression.
- Attempts and discarded hypotheses: the new regression rejected the original
  staged implementation on all four artifact-drift assertions. An initial shared
  decision over-restricted evidence retries after acceptance and preflight after
  repair. The first owning run caught four failures; those routes were corrected
  and existing tests strengthened. Both failed logs remain retained. No working
  tree mutation or alternate implementation remains.
- Current scoped diff: `scripts/controller.py` collects evidence in
  `_reservation_evidence`, selects actions in `_reservation_options`, and shares
  both between status and locked reservation, including refusal responses.
  `tests/test_actor_operations.py` adds the lifecycle regression and one pure
  decision table, and strengthens existing recovery assertions. Earlier staged
  implementation, reports, schemas, plan and tracker bytes are preserved.

## Implementation evidence

Raw logs are in `.quality/reports/T-005.1/` (repository-relative, ignored):

| Coverage / command | Implementation outcome |
|---|---|
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p test_actor_operations.py -k test_review_correction_proof_drift` | Original staged code: 1 test, 4 intended assertion failures in `correction-02-regression-before.log`. Initial correction: passes in `correction-02-regression-after.log`; included in final owning run. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p test_actor_operations.py` | 69 tests pass, no skips; `correction-02-actors-final.log`. Actual disposable Git/task lifecycle, fake local actor processes, real passing local checks, independent collection and separate acceptance correction, followed by retained-proof drift. |
| Pure `RecoveryDecisionTest` in that owning suite | Nine cases cover current/stale/missing review authority, readiness, check correction, repair, exhaustion and active implementer/verifier ownership. The table exercises deterministic facts directly without duplicating actor setup or claiming lifecycle admission. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py` | 4 pass, no skips, via installed run-evidence; `correction-02-architecture-final.log`. Structural evidence only. |
| `python3 tools/check_contracts.py --root .` | Pass, 8 subsystems / 36 indexed refs; `correction-02-contracts.log`. Structural evidence only. |
| `python3 tools/verify.py` | 7 checks, 1 failed; `correction-02-aggregate.log`. Orchestrator: 283 tests, 6 failures, 7 errors, 20 skips. All 13 failure identities match the prior implementation aggregate; no new identities. Other suites, registry and installer-profile drift check pass. Whole owning suite reused from this aggregate rather than repeated separately. |

- Coverage ledger: no independent row ledger accompanied maintainability-02.
  Blocker 1 remains CHANGES_REQUESTED in that historical review; the current
  regression and decision-table results above are correction evidence for fresh
  reassessment. No reviewer row is self-approved. Remaining reviewer coverage is
  fresh inspection of corrected production/test bytes and the broader task's
  outstanding discovery/acceptance work.
- Reviewer reproducer: the focused `-k test_review_correction_proof_drift` command
  above reuses `acceptance_ready`, `accept` and `reserve`. Appended bytes invalidate
  each retained artifact. Both surfaces require intervention, correction stays at
  zero, returned version is unchanged, and the ledger is byte-identical after
  each refusal. Restoring the proof restores the offered correction route.
- Native evidence producer/stage: this bounded correction invocation, under
  repository `AGENTS.md` and `docs/development.md`. Current checked-byte identities
  are recorded in `correction-02-checked-bytes.json` beside the logs. Full aggregate
  failure/skip reconciliation is implementation-owned; independent discovery
  must assess its limits separately.

The aggregate remains failed. Failure identities were reconciled against the
retained prior `aggregate-final.log` in `correction-02-failure-comparison.log`;
this is historical identity reconciliation, not a newly executed baseline or
successful host qualification. The 20 owning-suite skips and 32 root-suite skips
are not behavioral qualification. No live-provider checks were run. Current
runtime/schema/test hashes were rechecked unchanged after all executions.

## Measurement and retained structure

Original baseline pair remains `.quality/reports/T-005.1-before-01.json` and
`.txt`. Current comparison is `.quality/reports/T-005.1-correction-02-final.json`
and `.txt`: complete complexity/Ruff measurement and completed comparison for
controller, state and the two previously changed test files. All 12 baseline
source snapshots match their recorded hashes and original HEAD; all four current
measured files match worktree bytes (`correction-02-baseline-validation.log`).
Earlier `after-01` through `after-05` and correction comparisons are preserved.
The prepared macOS interpreter symlink is unavailable on this host; the installed
helper succeeded through system Python using existing Radon 6.0.1 and Ruff 0.14.2,
matching the baseline tool versions. No setup or installation occurred.

| Materially changed function | Retention rationale against the original baseline |
|---|---|
| `_reservation_options`: CC 29 → 40 | Recovery precedence now has one authority for both consumers. Correction eligibility, active ownership, budget and evidence freshness interact and must be ordered together. Separate action selectors would recreate the demonstrated disagreement. An explicit decision table could shorten branching but would still need ordered guards and add a second representation of policy; the direct deterministic function stays local and has table-driven evidence. Statements 26 → 34 and arguments 1 → 3 remain below advisory targets. |
| `_reservation_evidence`: new CC 11 | Collects candidate/check/collection/acceptance proof facts and a copied status view, without selecting recovery actions or writing authority. This is a real shared boundary replacing status-only validation. Splitting each exception handler into a wrapper would disperse the evidence dependencies without adding a consumer. Statements 29 and arguments 3 remain below targets; original numeric value is unknown, not zero. |
| `status_run`: CC 21 → 15 | Status projects the shared facts and computes completion eligibility. Remaining branches concern its public response projection; separating eligibility or response fields adds one-use navigation and no new authority boundary. The reviewed staged value was 37. |
| `reserve_operation`: CC 33 → 34; arguments 7 → 7 | One locked transaction preserves validation, idempotency, reason authorization, operation publication and budget charging. Shared facts/actions replace independent recovery routing. Keeping mutation checks at this boundary avoids dispersing transaction order; signature packing would obscure existing callers. Statements 39 → 48 remain below target. The reviewed staged CC was 44. |

Unchanged staged hotspots retain the prior implementation report's context;
they were not reworked in this correction. Metrics remain advisory and do not
approve the corrected shared policy.

- Report transfer: shared repository paths above. Isolated reviewers need the
  original `T-005.1-before-01.json`/`.txt`, current
  `T-005.1-correction-02-final.json`/`.txt`, and cited raw logs copied at those same
  relative paths; ignored evidence does not travel with commits.
- Deliverables: the two corrected Python files and this correction record.
- Actual contract impact: status and reservation now agree on stale review-proof
  intervention (`correction_authority_stale`). Status also advertises already
  supported renewed evidence/review after acceptance and fresh acceptance when
  its retained record is lost. Preflight after repair takes precedence over stale
  candidate inspection. No schema, role, correction budget or completion grant is
  added. Discovery/capability prose remains the designated updater's work.
- Executable contract declarations changed: controller Python API/action routing;
  no schema changes in this correction.
- Next: fresh independent `task-maintainability-review` of corrected bytes, then
  `task-contract-registry-updater`, fresh independent `task-review-discovery`, and
  separate `task-acceptance-review`. No independent review was performed by this
  implementation invocation. Official plans, tracker and prior reviews were not
  updated.
