# System verification and test quality — direction

**Covers:** `V-01`–`V-05`, `Q-02`; Q-01 is an existing source capability. **Status:** Remaining verification and suite-maintenance candidates, not an approved redesign.

## Desired outcomes

A multi-task project can show which critical flows, interfaces and invariants are proved; *where and when* the proof runs; who owns it; and what remains genuinely unverified. Tests and evaluation harnesses remain maintainable as the system grows. Completed tasks should not be mistaken for independently demonstrated system correctness.

## Capability direction

**V-01 — Start with an allocation pilot.** For one already accepted multi-task plan, inspect its existing system verification map (do not assume none exists). Look for material differences: unowned composed behavior, unavailable real boundaries, shared testability prerequisites, redundant E2E tests, missing negative/recovery behavior and unsupported claims. Produce an evidence-backed delta or a negative finding that a new pass adds no value. No new mandatory skill first.

**V-02 — Proportionate verification ownership, if warranted.** Where V-01 reveals a repeatable gap, give each consequential `FLOW / IF / INV` obligation one named proof owner, oracle/boundary, earliest executable point and failure/unknown disposition. Reconcile this at *draft planning* and reverify changed authoritative bytes. Avoid a second independently authored master test plan.

**V-03 — Task boundary integration evidence.** At a task's start, establish only the relevant existing baseline if needed to distinguish inherited defects from new ones. At completion, demonstrate the task's changed public/implemented boundary and its interaction with dependent components; reuse current evidence rather than re-running all tests reflexively.

**V-04 — First composed milestone and final system closure.** Demonstrate the first runnable end-to-end composition when its dependencies actually exist; close the overall project with an independent assessment of critical flows, evidence, unresolved failures, accepted gaps and remaining risks. Child task acceptance is necessary but not sufficient for a system-level conclusion.

**V-05 — Advanced techniques only when necessary.** Property-based, state-machine/model-based, fault-injection and mutation tests are options for important guarantees that lack a cheaper decisive oracle. Use risk and observability, not a technique quota, to select them.

**Q-01 — Independently review changed tests as software.** Detect introduced or worsened duplication, fragile shared fixtures, obscure ownership, false-positive structural checks and brittle harness coupling even if the suite passes. Compare only authorized changed/influenced test surfaces, preserve review independence and byte freshness, and distinguish consequential maintainability defects from personal style. This is already source-implemented in [task-maintainability-review](../../../skills/task-implementation-flow/task-maintainability-review/SKILL.md#review-contract), including tests-only submissions and significant test architecture as a reason for conditional review. It is not a future stage to add. This status records source capability, not a new independent behavioral qualification.

**Q-02 — Bounded test-suite restructuring.** Consolidate repeated setup across discovery/acceptance, improve explicit suite ownership and replace brittle text-only checks where a behavioral oracle is available. Retain legitimate independent fixtures, negative cases and stable textual contracts. Wait for flow interfaces to settle and prove regression protection before deleting checks.

## Allocation and evidence rules

- Different levels prove different things: unit/component for local logic, contract/integration for real interfaces, composed checks for state and recovery, and live-agent evaluations for model behavior. A static skill-text assertion is never described as emitted agent behavior.
- Every critical material obligation needs an owner even when the actual test must wait for an interface or environment. Mark `planned`, `observed`, `blocked`, `not run` and `accepted gap` distinctly.
- A real boundary is required where mocking would hide wiring, persistence, permissions, recovery, concurrency or dependent-system behavior; a live external service is **not** universally required.
- Tests built or changed during implementation should first reuse and update existing relevant tests/fixtures, rather than only accumulate new ones.
- Greenfield and iteratively extended projects are the default target. Brownfield inventory should be shallow until a concrete planning decision requires a deeper map.

## Decision checkpoints

1. Does V-01 find a consequential gap not already owned by the current planning and verification processes? If not, improve existing checks rather than add another stage.
2. Can V-03 demonstrate a materially new interface effect with limited extra execution cost? If not, narrow the policy.
3. Use the existing Q-01 review to identify a concrete changed-test architecture problem. Authorize only the bounded Q-02 cleanup justified by that problem and preserve its distinct oracles.
4. Does independent final closure find something not caught by accepted task packages? Distinguish a gap in product quality from simply another report.

**Already covered, not a new feature:** basic existing-test maintenance guidance in source, the current system verification map, task-local verification design, and the archived [T-004/T-005 qualification effort](https://github.com/trusovn/personal-skills/blob/0ad1706cecc6f7d115e510762bf74c58d732cb6a/docs/tasks/T-005/reassessment.md). That effort ended with incomplete qualification preserved; future issues use new work.
