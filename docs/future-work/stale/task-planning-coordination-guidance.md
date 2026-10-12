# Task Planning Coordination — Guidance Update

## Purpose

Clarify how the **project-delivery-plan** workflow identifies tasks that need coordinated decisions or planning, while retaining **just-in-time task brief creation** as the default.

The goal is to avoid incompatible task-level decisions without generating detailed briefs for the entire project before implementation begins.

## Why this is needed

A verified project plan already defines cross-task artifacts, interfaces, invariants, ownership, and dependencies. Most tasks should therefore be briefed individually, when they become ready for implementation, using both the plan and the repository's current implemented contracts.

However, some tasks share decisions or responsibilities that cannot safely be made in isolation. Without explicit guidance, planning agents may either:

- prepare many detailed briefs prematurely to force coordination; or
- defer a shared decision to separate task agents, producing incompatible assumptions.

Coordinated **decisions** do not necessarily require simultaneous creation of detailed **briefs**.

## Proposed changes

### 1. Update `project-delivery-plan` guidance — required

Add a task-planning independence check when defining the implementation task map.

The plan author should:

- Determine whether each task can be briefed independently once its dependencies are satisfied.
- Identify decisions that affect multiple tasks and distinguish **system-level contracts** from **task-local implementation choices**.
- Resolve shared system semantics in the project plan instead of leaving separate agents to rediscover them.
- For a legitimate task-owned decision with downstream impact, identify its owner, dependency, and handoff expectations.
- Reconsider task boundaries when splitting work would require impractical coordination or leave an indivisible outcome without an owner.
- Record exceptional planning coordination needs in existing task handoff context (`task_planner_context`), with a concrete reason—not merely because tasks reference the same interface or flow.
- State the default: generate detailed briefs **just in time**, after relevant predecessors have been implemented and their contracts can be inspected.

**Reason:** Preserve coherent system design while avoiding stale briefs, duplicated planning effort, and unnecessary process.

### 2. Tighten `project-plan-verification` guidance — small complementary change

Make the existing task-order and handoff review explicitly check that:

- No independently planned tasks must invent the same unresolved cross-task decision.
- Shared decisions have a clear system-plan resolution or a single owning task with an explicit handoff.
- Any exceptional need for coordinated task planning has a concrete justification.
- Dependencies and stable contracts are sufficient for normal rolling brief creation.

A discovered gap should be routed back to project planning; the verifier should not resolve it itself.

**Reason:** Catch coordination defects before they surface as conflicting implementation briefs. This extends existing composition checks rather than adding a separate review process.

## Cases to distinguish

| Situation | Expected handling |
| --- | --- |
| Producer and consumer of a shared API | Settle shared behavior in the project plan; brief separately |
| Several tasks depend on one unresolved shared decision | Resolve it at system level, or designate one task as owner and order dependent work |
| A single oversized task is decomposed into children | Design the related child briefs together under the existing `task-brief-designer` decomposition contract |
| A cross-task invariant needs final integration proof | Assign verification/integration ownership; do not automatically batch briefs |
| Independent tasks use established contracts | Brief individually, close to implementation |

## Out of scope

- No new planning stage, coordination skill, or batch-brief workflow.
- No new `task-map.json` fields such as `plan_together_with`.
- No changes to the default `task-brief-designer` decomposition behavior.
- No requirement to generate all project task briefs upfront.
- No task-status tracking or implementation scheduling added to planning artifacts.

## Expected outcome

The updated guidance should make it clear that **system-level coordination belongs in the project plan**, **task decomposition belongs in task brief design**, and **ordinary detailed briefs are prepared incrementally**. Only a genuine shared decision or indivisible responsibility should prompt special coordination, and its owner and rationale should be explicit.
