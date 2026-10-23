# T-002.1 implementation report

Implemented: **READY_FOR_REVIEW**. No acceptance verdict is issued.
This report supersedes the incomplete checkpoint status in
`implementation-handoff.md`; that checkpoint remains unchanged as history.

Authority: [brief.md](brief.md), brief revision 1;
[verification.md](verification.md), verification revision 1;
[preflight.md](preflight.md). Implementation resumed from the supplied handoff
on 2026-10-23 at HEAD `4449a3f373af9fabdcfe0c4d4b661988c4640c7f`.
The preflight's Linux sandbox limitation was rechecked on this macOS host.

## Result and scope

Initialization freezes one prepared task's brief, verification, scope, checks
and policy. Runtime validators, schemas and current examples now require the
approved model mapping, authorization, eight stages and distinct collection and
acceptance roles. Three corrections share one budget, including environment
repair. Unknown context requires a fresh correction session. Old incompatible
runs are refused without migration and receive the required new-run action.
The implementation prompt contains frozen document content.

Executable changes are limited to:

- `scripts/controller.py`, `scripts/controller_state.py`;
- `assets/run-policy.schema.json`, `assets/flow-profile.schema.json`,
  `assets/handoff.schema.json`, `assets/step-outcome.schema.json`;
- the three current `assets/examples/*-flow.json` examples and
  `assets/examples/minimal-run-policy.json`;
- `tests/test_controller.py`, `tests/test_controller_state.py`.

These paths are relative to `skills/task-orchestrator/`. This package also
contains the updated [controller-contract.md](controller-contract.md) and this
report. User-owned `AGENTS.md`, planning packages, task index and official plans
were not edited. No installation, shared helper, worker adapter or verification
runner was changed. The development installer was inspected: task-orchestrator
is excluded from its profile, and no managed dependency changed. No commit,
network request, live model check or sbx pilot was performed.

## Implementation evidence

All commands ran from the repository root. Initial submission checks (before
the MNT-01 correction below):

| Command | Result |
|---|---|
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py` | 44 tests passed, 0.435 seconds |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py` | 76 tests passed, 24.833 seconds |
| `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/t0021-schema-check.py` | Four changed schemas and four current examples valid; 12 invalid policies and four actor claims refused by schema and runtime |
| `git diff --check` | Passed |

The schema script uses the already installed `jsonschema` package and only local
resources. It checks current examples against runtime validation and Draft
2020-12 schemas, then supplies omitted-stage, multiple-task, missing-authorization,
stale-model, changed-budget, merged-role and actor-completion inputs. It is
supplemental structural evidence. The owning behavioral suites supply real
inputs and exercise initialization, loading, process execution and persistence.
The temporary script is diagnostic evidence, not a new project dependency or
canonical gate.

The outer execution sandbox prevented nested `sandbox-exec` capability checks.
The approved escalated targeted inspection check passed, followed by the final
owning controller suite outside the outer sandbox. The verifier itself remained
sandboxed. No environment failure was masked or converted into a skip.

A valid fail-first regression was run before the mutation guard fix:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills.task-orchestrator.tests.test_controller.ControllerIntegrationTest.test_old_flow_refuses_all_mutation_entries_without_touching_run
```

It failed all four entry cases: run-next, inspect and revise-flow lacked the
required next action; update-ledger accepted the old-flow update. After the fix,
this case passed with the public initialization refusal probe, and both are in
the final owning suite. An earlier draft of this probe had incomplete inspection
setup and a direct CLI import error; those results were discarded. The final
probe supplies a real initialized run and a real fake-transport attempt for the
inspection state before replacing persisted flow bytes.

## Coverage and remaining owner

All statuses below are implementation evidence only. Fresh discovery must
corroborate every row before separate acceptance.

| Scenario | Implemented evidence and oracle | Remaining owner |
|---|---|---|
| V-01 / AC-01 / R2 | `test_frozen_authority_survives_source_edits` initializes real brief/verification files; checks exact frozen content, scope, checks and policy; separately replaces source brief, verification, policy and manifest; reloads snapshots and compares every persisted run file. Multiple active tasks are refused through public init. The transport journey checks frozen document content in the actual prompt. | Fresh discovery, then acceptance |
| V-02 / AC-02 / R1 | State validator and public-init matrix remove each of eight stages, merge collection/acceptance roles, reverse order and request an optional stage. Public CLI refuses without changing source or run files or publishing a partial run. Actor results cannot grant controller completion or turn collection into acceptance. The initial run-next path remains pending at `ready` without worker launch. Mechanical inspection remains non-accepting with collection pending. | Fresh discovery, then acceptance |
| V-03 / AC-03 / R2 | Explicit low/medium/high mapping; stale model/effort/budget refusals; missing/malformed sbx, YOLO and chat authorization; known, at-threshold, above-threshold, unknown, unreliable, non-finite and totals-only occupancy cases. Mixed correction causes consume the same three slots and the fourth stops/escalates. Current examples and changed schemas agree with runtime. No adapter-launch-policy claim. | Fresh discovery, then acceptance; T-003 applies launch policy |
| V-04 / AC-04 / R2 | Real-file old-policy version, model, optional profile and missing snapshot-reference fixtures refuse CLI continuation with the new-run action and unchanged run bytes. Independent old-flow bytes exercise run-next, inspect, revise-flow and update-ledger before mutation. The focused regression rejected the earlier implementation. | Fresh discovery, then acceptance |
| V-05 / AC-04 | Contract note matches policy/flow versions, snapshot bytes/digests, roles, actor results, correction API, compatibility and actual commands. Missing readiness/admission/completion operations are explicit. | Fresh discovery compares declarations; acceptance decides |

Existing tamper, same-size workspace drift, verification gap, crash/replay and
process-lock tests remain represented. Obsolete verify-off behavior now proves
refusal without execution. Obsolete multi-task continuation now proves
single-task selection/exhaustion while preserving accepted-workspace integrity
and drift detection. Transport and inspection fixtures explicitly seed the
implementation boundary because no readiness adapter exists in this leaf.
They are not readiness-admission evidence and cannot weaken production flow
validation.

## Review route and limits

First outstanding stage after the MNT-01 correction: fresh project-local
`task-maintainability-review`, then fresh independent `task-review-discovery`,
then a separate fresh `task-acceptance-review`. The implementer did not launch
these reviewers. No repository policy requires an architecture gate for these
bytes. No contract registry exists; the task requires the package contract note
instead of creating one.

The broader command
`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'`
was not run. The brief assigns the aggregate decision to fresh discovery; that
owner must assess transitive effects before choosing it. The two owning suites
are implementation evidence, not aggregate or independent acceptance evidence.

All V-01 through V-05 rows remain pending independent review. T-002.2 stays
blocked until T-002.1 is accepted. Reservation, whole-input revision, semantic
evidence admission, completion and applying sbx launch policy remain successor
work, as specified by this leaf's scope.

Run evidence: `run-20261023T141553Z-97473750a7f2`, project-local
`.agents/scripts/` instrumentation. The resumed dirty tree is the baseline of
this invocation; earlier checkpoint changes are not attributed to this run.


## MNT-01 correction — 2026-10-23

The fixture and contract now agree with production: `inputs.json` is canonical
JSON without a trailing newline. The fixture uses the existing production
serializer. Both the real initialization test and the fixture persistence test
assert the newline convention and SHA-256 binding to the actual stored bytes.
Production code and existing frozen records are unchanged.

Implemented: **READY_FOR_REVIEW**.

- Authority: `skills/task-orchestrator/docs/tasks/T-002.1/brief.md`, revision 1.
- Preflight/context reference:
  `skills/task-orchestrator/docs/tasks/T-002.1/preflight.md`,
  `skills/task-orchestrator/docs/tasks/T-002.1/verification.md`, revision 1,
  and `skills/task-orchestrator/docs/tasks/T-002.1/reviews/maintainability-01.md`.
  Scope, dependencies, permissions and authority remain applicable. The newly
  staged baseline was preserved; no staging or review-report edits were made.
- Preceding verdict: `CHANGES_REQUESTED`.
- Finding/scenario IDs: MNT-01; influenced V-01 / V-05 / R2. V-02, V-03 and
  V-04 retain their scenarios and require fresh review with the rest.
- Complete findings and invariant: MNT-01 confirmed a mismatch between
  production's no-newline input record, the fixture's appended newline and the
  contract's newline claim. The invariant is one documented persisted byte
  convention, with digest binding to the exact bytes. The correction preserves
  production semantics and removes the fixture's separate serialization rule.
- Influenced sibling surfaces: policy and manifest digest conventions and
  flow's trailing newline remain unchanged and are distinguished in the
  contract. The shared record serializer is unchanged, so other record formats
  receive no behavior change.
- Attempts and discarded hypotheses: the focused pair below first ran two
  tests with one expected failure at the fixture's newline assertion; real
  initialization passed. After the fixture/doc fix both passed. No abandoned
  fix or temporary production mutation remains.
- Current scoped diff: `skills/task-orchestrator/tests/test_controller_state.py`
  reuses `_canonical_record_bytes` and checks stored bytes/digest;
  `skills/task-orchestrator/tests/test_controller.py` checks real initialized
  input bytes/digest; this report and `controller-contract.md` carry the
  correction. Executable contract declarations changed: none. Actual contract
  impact: correct an explanatory byte-format statement; no persisted format,
  policy or API change.
- Coverage ledger: MNT-01 — prior status: confirmed blocker; implementation
  evidence: the focused pair and both owning suites below pass; incomplete
  reason: fresh review has not occurred; next owner: fresh maintainability
  reviewer. The preceding review verdict remains unchanged. V-01 through V-05
  in the coverage table above remain pending independent discovery and separate
  acceptance; no reviewer status is upgraded by these implementation checks.

Reviewer reproducer (implemented from the source-inspection finding):

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills.task-orchestrator.tests.test_controller_state.ControllerStateContractTest.test_rejected_controller_update_leaves_persisted_bytes_unchanged skills.task-orchestrator.tests.test_controller.ControllerIntegrationTest.test_frozen_authority_survives_source_edits
```

Result after correction: two tests passed, 0.129 seconds. The first run failed
specifically because the fixture appended a newline.

Owning suite commands and current implementation results:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py
```

Results: 44 state tests passed (0.490 seconds); 76 controller tests passed
(24.950 seconds). The controller suite ran under the previously approved
escalation so its nested macOS sandbox checks could run. `git diff --check`
also passed. No tests were added; existing cases gained the missing byte-format
and digest assertions.

The review's parallel-policy and transport-fixture warnings remain successor
maintenance cautions. The claim that the correction and authorization type
checks are redundant is incorrect: Python dictionary equality admits `1` for
`True`, and `3.0` for `3`. Those explicit checks remain. The unconditional-flow
cleanup is optional and was left outside this correction.

Broad/aggregate gate: the full discovery command recorded above remains
unrun and owned by fresh discovery. This correction changes tests and
explanatory text only; no new schema, dependency or production behavior justifies
an implementation-owned aggregate run. Remaining reviewer coverage: fresh
maintainability corroboration of MNT-01, then all V-01 through V-05 via fresh
independent discovery and separate acceptance.

Next: fresh `task-maintainability-review` → fresh `task-review-discovery` →
separate fresh `task-acceptance-review`. T-002.2 remains blocked on acceptance.
Run evidence for this correction: `run-20261023T144104Z-f9160e4b6122`.

## Discovery-01 correction — F-02

The Git wiring fixture now meets the frozen input and policy contract and
reaches its worker/Git assertions. No production behavior changed.

Implemented: READY_FOR_REVIEW

- Authority: `skills/task-orchestrator/docs/tasks/T-002.1/brief.md`, revision 1;
  the user's request to fix `reviews/discovery-01.md` authorizes its bounded
  sibling-fixture correction in `tests/test_controller_git.py`.
- Preflight/context reference: this package's `preflight.md`, `verification.md`
  revision 1, `controller-contract.md`, and `reviews/discovery-01.md`.
  The prior Linux capability limits differ on this macOS host; no dependency,
  installation, production contract, or verification scenario changed.
- Preceding verdict: discovery-01 publishes evidence only, with F-02 a
  suggested P2 blocker; it makes no acceptance decision. Maintainability-02
  previously returned ACCEPT for its reviewed scope only.
- Finding/scenario IDs: F-02; V-01, V-02, V-02a, V-03, V-03s, V-04, V-05,
  MNT-01. The report explicitly excludes pre-existing retrieval drift (F-01)
  from this implementation's findings.
- Complete findings and invariant: F-02 used a version-1 policy without
  execution authorization, causing validation to fail before the real Git
  wiring assertions. The invariant is no task-induced aggregate regression.
  The fixture now supplies version 2, explicit sbx/YOLO/active-chat policy,
  and a prepared verification document. Its existing current flow and single
  task remain. As in `test_controller.py`, explicit ledger setup starts at
  implementation because readiness admission belongs to T-002.2. This setup
  proves transport wiring, not readiness admission or actual sbx isolation.
- Influenced sibling surfaces: discovery bounded the affected sibling to
  `test_controller_git.py`; `test_codex_worker.py` does not invoke the changed
  policy validators. Existing policy validation and compatibility behavior is
  exercised by the two required owning suites below. No shared fixture
  framework or extra test cases were added.
- Attempts and discarded hypotheses: the focused reproducer failed before
  correction with `ValueError: Run policy is missing: execution_authorization`.
  After correction it passed. No abandoned fix or production mutation remains.
- Current scoped diff: `skills/task-orchestrator/tests/test_controller_git.py`
  updates the fixture and stage setup; this report records the correction.
  Existing worker launch, baseline capture, closure capture, patch content,
  and digest assertions are unchanged. All pre-existing staged work is preserved.

Coverage map recorded before editing in the implementation conversation;
current implementation evidence follows. Prior reviewer statuses below remain
historical, not new review conclusions.

| Row | Prior discovery status | Implementation evidence / limit | Next owner |
|---|---|---|---|
| V-01 | pass | Controller suite green, including frozen-authority regression | Fresh discovery |
| V-02 | pass | Controller and state suites green, including required-stage refusals | Fresh discovery |
| V-02a | blocked on Linux | Controller suite green on macOS, including all inspection regressions; prior independent gap remains until fresh review | Fresh discovery on capable host |
| V-03 | pass (runtime) | State suite and corrected Git fixture green | Fresh discovery |
| V-03s | blocked: no validator on review host | Schemas/examples unchanged by correction; Draft 2020-12 validation not rerun here | Fresh discovery with validator capability |
| V-04 | pass | Controller suite green, including old-run mutation refusals | Fresh discovery |
| V-05 | pass (static) | Contract and production declarations unchanged; no new static review claimed | Fresh discovery |
| MNT-01 | pass | Both owning suites green, retaining exact byte/digest regressions | Fresh maintainability/discovery |

Reviewer reproducer (implementation evidence):

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills.task-orchestrator.tests.test_controller_git.ControllerGitWiringTest.test_run_next_uses_controller_git_task_baseline_and_closure_evidence
```

Before correction: 1 test, 1 error at policy validation. After correction:
1 test passed (0.605 seconds), exercising the real temporary repository,
local fake worker, captured Git patch and digest oracle.

Owning suite and required task checks (implementation evidence):

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_git.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller_state.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_controller.py
```

Results: 13/13 Git tests passed (2.260 seconds), 44/44 state tests passed
(0.499 seconds), 76/76 controller tests passed (24.525 seconds).

Broad/aggregate gate:
`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'`
was not rerun: the brief assigns its decision to fresh discovery. The targeted
reproducer and complete affected sibling suite prove the correction locally;
no aggregate success is claimed. Pre-existing retrieval-surface drift is
unchanged and remains outside this correction. No live model, network, or sbx
pilot ran. Installer inspection is not required: task-orchestrator is excluded
from the development profile and this correction changes no shared dependency.

Remaining reviewer coverage: all prior rows require current discovery evidence;
V-03s retains its independent capability gap. V-02a now has successful macOS
implementation evidence, not independent corroboration. The small test-only
correction still requires the applicable maintainability stage; no architecture
gate or contract-registry stage applies.

Next: fresh `task-maintainability-review` → fresh independent
`task-review-discovery` → separate fresh `task-acceptance-review`.
T-002.2 remains blocked on acceptance. Run evidence:
`run-20261023T150213Z-e16704f62e3d`.
