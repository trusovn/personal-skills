# T-002.3 guided preflight

Status: ready
standalone_preflight_value: material

Source brief: brief.md, revision 1
Verification: verification.md, revision 1
Scope: controller/state scripts, affected declarations and owning tests under
skills/task-orchestrator; this task's reports and ../T-002/controller-contract.md.

## Resolved readiness facts

T-002.1 acceptance-02 and T-002.2 acceptance-01 both ACCEPT their predecessor
contracts. Public status/reserve use the same RunCommandLock and atomic ledger
replacement. Existing immutable-flow publication fixtures and
ControllerReservationTest's terminal/readiness fixture provide feasible local
publication and lifecycle oracles. No shared infrastructure is required.

The worktree initially contains only unrelated untracked .DS_Store files and
docs/advisory-code-maintainability-signals.md; preserve all. No owned-path overlap.
The development installer excludes task-orchestrator and its local scripts;
this change requires no profile, README or shared-runtime changes. Project-local
workflow skills and sibling .agents/scripts resolve successfully; installations
will remain unchanged. No contract registry or mandatory architecture gate was
found. Conditional maintainability review requires repository policy or explicit
request; predecessor reviews alone do not impose it on this leaf.

## Decision context

The plan's IF-001/ART-001/002/FLOW-003 and parent P-01..06 govern a local,
single-task controller consumed next by T-003. False freshness or a reset repair
allowance could authorize work against changed requirements. Preserve durable
history and refuse uncertain ownership. Existing source-edit protection does
not authenticate a malicious coordinator or coherent whole-run tampering.
Explicit owner-response provenance is an input to the trusted controller API;
no external identity service is in scope. Future observed readiness/admission
and independent semantic evidence remain T-003/004/005 work. The recorded
retrieval inventory drift and platform-dependent historical sandbox checks may
limit aggregate evidence; they do not prevent local revision tests.

## Acceptance evidence and feasible commands

All commands use repository root, local Python stdlib/unittest and disposable
Git repositories; no network, dependency install, actor launch or permission
expansion. Future task-owned tests below have not yet run.

| Cases / authority | Setup, boundary and oracle | Command / feasibility |
|---|---|---|
| V-01, AC-01/R1 | Real initialized run + explicit bound owner revision; inspect identity/version/history/count | Focused command below; existing initialization fixtures |
| V-02, AC-01/03/R1 | Valid controls plus invalid authority/version/policy and active/completed/locked runs; compare bytes | Same; real local lock/file boundary available |
| V-03, AC-02/R2 | Explicit successor evidence fixture + revision/reload; old contents retained, eligibility stale, fresh preflight required | Same; no production admission claim |
| V-04, AC-03/R3 | Inject faults at content and ledger publication; reload and exact retry; one receipt/charge | Same; existing exclusive writer/atomic replacement can be faulted locally |
| V-05, AC-04/R1..3 | Public freeze/reserve/revise/status + labeled terminal fixtures; three shared corrections, fourth denial, legacy guards | Same; existing reservation helpers available |
| V-06, AC-05 | Reconcile actual APIs, validators and execution results with parent contract | Source/interface inspection after implementation; no behavioral claim |

Focused planned command:
`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p test_controller.py -k ControllerInputRevisionTest`

Owning command after focused checks:
`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_controller*.py'`

Independent discovery owns the brief's full aggregate command. No broad baseline
was run. Material value: verified accepted predecessor interfaces, publication
fixture reuse and actual installation/ownership boundaries before implementation.
Recommend standalone preparation for similarly stateful cross-session work.

## Implementer handoff

Implement brief revision 1 with verification revision 1 in the recorded scope.
Use immutable revision content plus one atomic authority/version publication;
retain original files and operation/evidence history. Recheck only material
changes to authority, ownership, capabilities or dependencies. Stop for those
changes, permission expansion or an oracle requiring shared infrastructure.
Run focused checks, then owning modules; write results next to the brief.
Next: bounded-task-implementer, then READY_FOR_REVIEW with fresh independent
review-discovery followed by separate task-acceptance-review. Do not launch
reviewers or run their aggregate gate in the implementation invocation.
