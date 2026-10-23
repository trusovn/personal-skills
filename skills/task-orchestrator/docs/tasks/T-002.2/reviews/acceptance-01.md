# T-002.2 acceptance review 01

The reviewed worktree satisfies this leaf's read-only status, atomic reservation
and persistent shared-correction contract. Current independent discovery closes
all required rows and both prior findings; the current maintainability review
accepts the correction. The coordinator may hand the accepted contract to
T-002.3. This report performs no advancement.

Verdict: **ACCEPT**

Provenance: independent acceptance session; no reviewed production or test bytes
authored. Guided profile, using the project-local installed acceptance skill.
No tests, discovery probes, aggregate gates, subagents or live services were run
by acceptance. Only this report was written.

## Authority, preparation and scope

Read [brief.md](../brief.md) revision 1, [verification.md](../verification.md)
revision 1, [preflight.md](../preflight.md) including Decision context, parent
T-002 brief and cited IF-001/ART-002/004/invariants/flows, predecessor contract
and T-002.1 acceptance-02. The prerequisite is accepted and the preparation
references remain applicable: authority, dependency and verification revisions
are unchanged. Expected implementation changes do not invalidate readiness.

Submission claims are [implementation-report.md](../implementation-report.md)
and [correction-report-01.md](../correction-report-01.md) /
[correction-report-02.md](../correction-report-02.md). Their named-method maps
were reconciled with current source and the admitted independent evidence,
not counted as independent proof.

The task owns controller.py, controller_state.py, their owning controller/state
tests, the declared one-line private dispatch rename in test_controller_git.py,
and this package's contract/reports. The Git fixture change preserves its
baseline/closure assertions and is within reused-fixture scope. Staged original
work and unstaged correction work are separately accounted for. The untracked
`docs/advisory-code-maintainability-signals.md` is unrelated user work, excluded
and preserved. No inseparable overlap was found.

## Admitted discovery and conditional evidence

[discovery-03.md](discovery-03.md), correction 2, is the complete current
independent publication and continuation. discovery-01/02 are historical finding
and command records, not current passes. DISC-01 ran 11 reservation tests;
DISC-02 independently accepted the valid validator control, rejected the six
original invalid records, and rejected 39 wrong-known-actor mutations through
public status/replay with byte-preserving refusals. DISC-03 supplies bounded
real-process contention and cleanup evidence. This includes both valid and
deliberately invalid instances of the acceptance-relevant executable validator
boundary; no separate ledger JSON Schema exists.

[maintainability-02.md](maintainability-02.md) accepts current correction bytes
and reconciles the original scope with maintainability-01. It resolves the
conditional-evidence gap that discovery-03 recorded before that report existed.
Its later publication did not change executable bytes. No applicable canonical
architecture gate is recorded; NOT_AVAILABLE is not a failed required gate.

Contract reconciliation: EXPECTED IF-001 status/reserve and ART-002/004 assignment
semantics match ACTUAL shared authority/eligibility checks, locked reservation,
atomic embedded history/count publication and conservative active-owner guards.
DECLARED CLI/library and state validators describe those interfaces.
DISCOVERABLE [controller-contract.md](../controller-contract.md) matches the
request/result fields, exact replay semantics, refusals, counting and successor
admission seams. No registry exists or is required by the brief; no registry
stage or new foundation is imposed. The architecture map still routes controller
and durable-state work to the correct owners. No stale routing claim requiring
an adjacent documentation change was identified. Installer-selected skills and
shared dependencies are unchanged.

## Findings and dispositions

No findings remain open. Approved deferrals: none.

- **F-01 [P2], resolved.** Location: controller_state.py active assignment and
  parent lifecycle validation, exposed by controller status/replay. Trigger:
  mismatched current input/policy/flow revision/candidate/task/stage or stopped
  parent while retaining an active assignment. Consequence/boundary: a successor
  coordinator could consume contradictory current authority; AC-01/02/03 and
  V-01/V-02/V-04 would fail. Impact: material persisted-authority error.
  Exposure: deliberately inconsistent persisted records, not normal producer
  output; successor writers make consistent validation necessary. Prior
  mitigation only checked partial identity. Current mitigation checks full
  active/current identity, latest-owner ordering and permitted parent states.
  DISC-01/02 now reject the original cases and siblings across six stages and
  reserved/running/unknown while preserving terminal history. Fix-now rationale
  was the explicit AC violation; current evidence establishes resolution.
- **F-02 [P2], resolved.** Location: controller.py `_reservation_context`, with
  structural profile validation in controller_state.py. Trigger: substitute a
  known actor profile inconsistent with the frozen stage mode. Consequence:
  status/replay could expose unauthorized actor selection; AC-01/02/03 and
  V-01/V-02/V-04 would fail. Impact: material frozen-policy violation. Exposure:
  inconsistent active persisted assignments, including correction implementation
  mode and verify's null actor; ordinary producer selection was already correct.
  Known-profile membership was insufficient mitigation. Current shared context
  binds the active actor to the authoritative frozen flow. DISC-01's both-profile
  matrix and DISC-02's 39 independent cases reject mutations without writes;
  historical terminal actors remain valid. Fix-now rationale was the explicit
  policy-bound assignment obligation; current evidence establishes resolution.

Observations: the existing contention test's initial readiness `readline()` has
no deadline. Impact is a possible hung test if its child stalls; exposure is
conditional on that fixture failure. The later communicate timeout does not
cover readiness. Independent DISC-03 provides bounded synchronization, process
completion/group absence and pipe-release evidence for this decision. Preserve
the prior maintainability warning as optional fixture maintenance; no new runtime
or timeout-hardening requirement is introduced, and no deferral is needed.

## Reconciled coverage

Submitted evidence in each row is the implementation/correction named-method
map. Current independent evidence comes only from discovery-03's commands and
source reconciliation; acceptance did not execute them.

| Stable row | Material cases and submitted evidence | Admitted evidence and current result |
|---|---|---|
| V-01 / AC-01 | Status/reload identity, evidence/references/findings/count/actions, passed/failed/stale/blocked/missing/not_run and required/optional omission; read-only status/CLI and correction matrix | **pass** — DISC-01 status/CLI/matrix, DISC-02 valid/invalid status controls; snapshots unchanged |
| V-02 / AC-02/03 / R1 | First reserve, exact replay/reload, conflicting key/request/version, reserved/running/unknown/terminal, assignment identity/actor and process race; replay/ownership/matrix/history/contention methods | **pass** — DISC-01, DISC-02 original and actor siblings, DISC-03 bounded separate-process race; one winner, one refusal, one persisted owner |
| V-03 / AC-04 / R2 | Cycle zero, mixed check/review/repair charges 1/2/3, fourth unchanged/intervention, replay/reload/uncertain charge, pre-initial repair retained after preflight, free evidence/preflight retries; budget/repair/retry methods | **pass** — DISC-01 real sequential reservations and labelled successor setup, assignment/count and byte-snapshot oracles |
| V-04 / AC-03/05 / R3 | Stale/invalid task/version/role/stage/key/reason, absent/failed/stale/wrong/nonterminal readiness, weak authority, run-next/inspect/revise-flow/update guards; invalid-request/readiness/legacy/CLI/matrix methods | **pass** — DISC-01 public entry points and DISC-02 executable valid/invalid controls, structured replay refusal and unchanged bytes |
| V-05 / AC-05 | Exact public contract, record fields, embedded publication/replay/count and successor seams, no generic public setter; contract and CLI map | **pass** — discovery source/contract trace plus DISC-01 CLI; current source/contract reconciliation agrees |

R1=pass through V-02; R2=pass through V-03; R3=pass through V-04.
No required/material row is blocked or unchecked. Prior V-01/V-02/V-04 failed
F-01, then F-02; their current passes use corrected-byte evidence. V-03/V-05
were previously passing and have current corroboration rather than inherited
passes.

## Aggregate gate (consumed)

Exact command:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'
```

Owner/stage: independent correction-2 discovery, DISC-04. Command order:
DISC-01 targeted class, DISC-02 independent validator/actor regressions,
DISC-03 bounded contention/cleanup, then DISC-04 aggregate. Shared controller/
state impact justified it after clean targeted reconciliation; no omitted
failing or unchecked targeted row was cleared by aggregate execution.

Result: **failed**, 198 tests, 197 pass, one failure, 49.554 seconds. The sole
failure is `test_retrieval_surface.RetrievalSurfaceTest.test_expected_current_references_exist`
at tests/test_retrieval_surface.py:45. Discovery independently compared HEAD's
docs inventory and unchanged test. Acceptance's static HEAD tree/test-diff check
corroborates that attribution: all six extra entries already exist in HEAD;
the assertion has no task diff. Preflight and predecessor acceptance-02 already
record this same baseline issue. The aggregate is not green.

This unchanged inventory failure is outside the task's correction authority and
does not violate a global-green requirement in this brief. No owning task check
or AC is waived. Baseline maintenance remains with its existing documentation/
retrieval owner, not an acceptance-approved task deferral. Impact: red aggregate
can obscure later regressions; exposure: deterministic at aggregate execution.
Mitigation: exact failure isolated against HEAD and all task rows/current sibling
checks independently qualified. Acceptance adds no command or rerun.

## Identity, limits and next route

HEAD: `1c1aff83da3cbc69ecfe6acc2235108118f2cc12`.
Tracked binary diff SHA-256: `2665634287b646735a4db672d1830d1c92e581beae3632d5035f5fcbb583b2db`.
Index SHA-256: `cb8ac1d12ea579699c491b965b3201f69bd69e53e0cc41d4ec6b56ad2a79bbb4`.
All match discovery-03 and maintainability-02. This decision qualifies the
**worktree**, not the older staged correction bytes.

| Implementation path | Index Git blob | Worktree Git blob |
|---|---|---|
| scripts/controller.py | e435948d4cc7a9751a694b32221d51c83de84549 | 0a21618a11b192bae891c373f0ae61caf0c0499b |
| scripts/controller_state.py | a27b1367fe7370ee64defc78653c4a6bd88dd49b | a27b1367fe7370ee64defc78653c4a6bd88dd49b |
| tests/test_controller.py | cd8ff075f2b976f38d5bf7cdea4f1ef741ae6504 | 6bf2b95a1f6ca9a398f8beccf03c9b9c4997acff |
| tests/test_controller_git.py | 6d3e24b2cd8e308e4cbb5d75d957f5a42531ba80 | 6d3e24b2cd8e308e4cbb5d75d957f5a42531ba80 |
| tests/test_controller_state.py | 038ba6ff3af9a0f4257e589344303d0e719e8657 | 038ba6ff3af9a0f4257e589344303d0e719e8657 |

Questions / unchecked work: none within this leaf. Successor fixture states do
not prove production actor launch, observed terminal/readiness admission,
semantic evidence admission, input revision or final completion. Those remain
T-003/004/005 and T-002.3 work. Mutable digests do not authenticate a coherent
whole-run rewrite. No stronger claim is made.

Next: coordinator hands this decision, controller-contract.md and discovery-03
plus current conditional evidence to T-002.3 for its own preflight. Preserve the
reviewed worktree correction when preparing any later staged delivery. No plan,
tracker, known-issues file, orchestration state or commit was changed here.

## Review continuation

- Iteration/current identity: acceptance 01 after correction 2; HEAD/diff/index
  and separate worktree/index blobs above. No preceding acceptance verdict for
  this leaf; discovery-01/02 remain historical evidence.
- Coverage rows: V-01=pass; V-02=pass; V-03=pass; V-04=pass; V-05=pass;
  R1=pass; R2=pass; R3=pass. No incomplete reason or blocked/unchecked row.
- Finding IDs: F-01=resolved; F-02=resolved, with contextual fields above.
  Prior V-01/V-02/V-04 failures are closed by discovery-03 DISC-01/02;
  producer claims remain attributed to correction-report-01/02.
- Owners: correction=none outstanding (original implementer owns future fixes);
  evidence=discovery-03; authority/next route=coordinator. Influenced siblings:
  all six reservation stages and three active states; correction's implementation
  mode, verify null actor and terminal historical authority/actor preservation.
- Preparation/context: brief revision 1, verification revision 1, preflight
  Decision context; parent/plan and predecessor contract/acceptance-02.
- Reviewer regressions: none added or run by acceptance. Permanent regression
  methods `test_active_assignment_must_match_current_ledger` and
  `test_terminal_assignment_retains_historical_authority` are in
  tests/test_controller.py. Exact DISC-01 class command and DISC-02/03 inline
  probe commands remain in discovery-03 section 5; DISC-03 extracts the preserved
  bounded body from discovery-02. Supply these records to any fresh reviewer.
- Aggregate consumed: DISC-04 failed 197/198 after clean DISC-01..03; established
  unchanged retrieval inventory failure, no waiver or new acceptance gate.
- Next: coordinator handoff to T-002.3 preflight; no extra review rerun is required
  for unchanged accepted bytes.

## Exact status audit

Before report creation:

```text
A  skills/task-orchestrator/docs/tasks/T-002.2/controller-contract.md
A  skills/task-orchestrator/docs/tasks/T-002.2/correction-report-01.md
A  skills/task-orchestrator/docs/tasks/T-002.2/implementation-report.md
A  skills/task-orchestrator/docs/tasks/T-002.2/preflight.md
A  skills/task-orchestrator/docs/tasks/T-002.2/reviews/discovery-01.md
A  skills/task-orchestrator/docs/tasks/T-002.2/reviews/discovery-02.md
A  skills/task-orchestrator/docs/tasks/T-002.2/reviews/maintainability-01.md
MM skills/task-orchestrator/scripts/controller.py
M  skills/task-orchestrator/scripts/controller_state.py
MM skills/task-orchestrator/tests/test_controller.py
M  skills/task-orchestrator/tests/test_controller_git.py
M  skills/task-orchestrator/tests/test_controller_state.py
?? docs/advisory-code-maintainability-signals.md
?? skills/task-orchestrator/docs/tasks/T-002.2/correction-report-02.md
?? skills/task-orchestrator/docs/tasks/T-002.2/reviews/discovery-03.md
?? skills/task-orchestrator/docs/tasks/T-002.2/reviews/maintainability-02.md
```

After report creation:

```text
A  skills/task-orchestrator/docs/tasks/T-002.2/controller-contract.md
A  skills/task-orchestrator/docs/tasks/T-002.2/correction-report-01.md
A  skills/task-orchestrator/docs/tasks/T-002.2/implementation-report.md
A  skills/task-orchestrator/docs/tasks/T-002.2/preflight.md
A  skills/task-orchestrator/docs/tasks/T-002.2/reviews/discovery-01.md
A  skills/task-orchestrator/docs/tasks/T-002.2/reviews/discovery-02.md
A  skills/task-orchestrator/docs/tasks/T-002.2/reviews/maintainability-01.md
MM skills/task-orchestrator/scripts/controller.py
M  skills/task-orchestrator/scripts/controller_state.py
MM skills/task-orchestrator/tests/test_controller.py
M  skills/task-orchestrator/tests/test_controller_git.py
M  skills/task-orchestrator/tests/test_controller_state.py
?? docs/advisory-code-maintainability-signals.md
?? skills/task-orchestrator/docs/tasks/T-002.2/correction-report-02.md
?? skills/task-orchestrator/docs/tasks/T-002.2/reviews/acceptance-01.md
?? skills/task-orchestrator/docs/tasks/T-002.2/reviews/discovery-03.md
?? skills/task-orchestrator/docs/tasks/T-002.2/reviews/maintainability-02.md
```

Verification: exact status compared before/after; only this new report entry
may differ. HEAD, full index bytes, tracked binary diff and every pre-existing
changed/untracked file's SHA-256 were compared and preserved. These checks prove
review scope/identity only; behavioral results above are consumed independent
discovery evidence. No prior report was overwritten.
