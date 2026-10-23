# Verification Design: T-002.2 — Guard status, reservations and correction counting

Source brief: brief.md
Source brief revision: 1
Verification revision: 1
Authority: derived from the task brief and its cited normative sources
Status: ready

This design requires the accepted T-002.1 interface before ready preflight.
It supplies no readiness or executed-test result.

## Coverage summary

| AC / risk row | Scenarios | Notes |
|---|---|---|
| AC-01 | V-01 | Status is truthful and cannot advance state |
| AC-02, R1 | V-02 | Real reservation/lock/persistence boundary |
| AC-03, R1/R3 | V-02, V-04 | Unknown ownership and legacy bypasses |
| AC-04, R2 | V-03 | First implementation, three corrections, replay/reload/fourth |
| AC-05, R3 | V-04, V-05 | Unchanged refusals and implemented handoff |

## Verification scenarios

### V-01 — Replacement status preserves the actual next action

- **Covers:** AC-01.
- **Intent:** reject a status view that resets state or presents absent evidence as passed.
- **Given:** real run records at relevant stages, with explicit evidence states,
  an operation, correction count and historical findings as applicable.
- **When:** read status, discard controller memory, reload and read again.
- **Then:** run/task/input/flow identity, version, stage, operation/count and
  evidence references remain consistent. Required evidence and permitted next
  actions reflect the records. Reads cannot advance the stage or consume budget.
- **Oracle / boundary:** public status output against real persisted fixtures
  and unchanged authoritative bytes.
- **Variants:** passed, failed, stale, blocked, missing/not-run, and a permitted
  optional omission. Required-role omission cannot be rendered as success.

### V-02 — Only one reservation survives replay and contention

- **Covers:** AC-02, AC-03, R1.
- **Intent:** reject check-then-write races and restart duplication.
- **Given:** a valid policy, a permitted stage and a current expected version.
- **When:** reserve, repeat that key, reload and repeat it; separately submit
  competing reservations from separate controller processes against the same version.
- **Then:** exactly one operation/assignment is authoritative. Its subject,
  policy/input identity and applicable candidate match the frozen run. Replays
  do not allocate or charge again. Losers receive structured refusal/permitted
  actions. A possibly live operation blocks another actor and completion.
- **Oracle / boundary:** real public operations, lock and filesystem records;
  control contention with existing local synchronization fixtures, not model actors.
- **Variants:** reserved/running/unknown active states; explicit test-only
  terminal state permits the next otherwise valid operation. Missing receipt
  alone never permits that transition.

### V-03 — Corrections and environment repair share exactly three cycles

- **Covers:** AC-04, R2.
- **Intent:** reject per-route counters, double charges and reset through retry.
- **Given:** cycle-zero implementation authorized under current readiness;
  test setup provides valid later-stage prerequisites/terminal records.
- **When:** authorize three successive correction operations using failed-check,
  review and environment-repair reasons; replay a key, reopen the controller
  between operations, and request a fourth. Exercise preflight/evidence-only retries separately.
- **Then:** initial count is zero; new corrections produce counts 1, 2 and 3;
  replay does not change them. Fourth correction is refused without changing
  authority/files and status requests intervention. Free retries do not charge
  and cannot authorize repairs. Environment repair requires preflight again.
- **Oracle / boundary:** public reservation/status plus real persisted counts,
  assignments and file comparisons. Test-only successor records are labelled;
  this scenario does not prove their production admission or actor launches.
- **Variants:** route changes and reload before fourth request; uncertain launch
  keeps its reservation charge and prevents duplicate work. Separately authorize
  environment repair before initial implementation, repeat preflight, then
  authorize initial implementation: the repair charge remains and only the
  remaining shared correction allowance is available.

### V-04 — Invalid requests and legacy paths cannot weaken authority

- **Covers:** AC-03, AC-05, R3.
- **Intent:** reject guarding the new command while leaving an old bypass open.
- **Given:** frozen policy, known authoritative/task bytes and each invalid request below.
- **When:** invoke public reservation or an applicable existing `run-next`,
  `inspect` or `revise-flow` path using that request/state.
- **Then:** structured refusal explains the reason and permitted next action;
  policy/state/version/count/task files remain unchanged. New-policy tasks
  cannot skip readiness or complete through legacy behavior. Unimplemented
  successor behavior is exposed as pending/unavailable, never success.
- **Oracle / boundary:** actual public entry paths and real before/after bytes.
- **Variants:** stale version; wrong task/role/stage; absent readiness; readiness
  bound to old inputs or nonterminal/wrong-role preflight; weak profile; unknown operation.

### V-05 — The assignment contract gives successors one admission boundary

- **Covers:** AC-05.
- **Intent:** reject undocumented replay/count behavior or a public test bypass.
- **Given:** implemented controller and package `controller-contract.md`.
- **When:** compare exact public examples, records and refusal/replay semantics
  to the code and local behavioral evidence.
- **Then:** T-002.3/T-003 can consume the actual interface; observed outcome and
  readiness admission remain assigned to T-003; semantic routing remains assigned
  to T-004/005. No generic public setter injects eligible evidence/stages.
- **Oracle / boundary:** public-interface/source inspection and existing behavioral
  results. Documentation shape alone proves no reservation property.
- **Variants:** none.

## Implementation handoff

Use existing lock, temporary-repository and ledger fixtures. Keep the real
controller/persistence/counting logic in the test path. Successor states may be
seeded only as explicit test setup. Preserve these IDs and the brief's owning
gate/review assignments. Concrete test structure remains an implementation
choice. Route changed requirements to task design and executability to preflight.
