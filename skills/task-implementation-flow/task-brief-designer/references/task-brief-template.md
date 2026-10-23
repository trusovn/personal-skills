# Task brief forms

Choose the applicable form below. Place explanations in the indicated sections;
optional fields serve a concrete task need, not a checklist to fill. For an
existing adequate brief, preserve equivalent sections and make a local delta.
The skill owns routing and evidence rules; these forms own the reading order.

## Executable brief

Use for `ready` or `ready_for_preflight` leaves. The opening explains the work;
execution status and launch guidance come after its requirements and evidence.

```markdown
# Task Brief: `<TASK-ID>` — `<concrete result to deliver>`

## Outcome

<What completion demonstrates, who uses the result, and what it enables next.
Distinguish what this task defines, what it executes, and what later work owns.
Link to project purpose rather than retelling it.>

## Direction trace

<Include only when governing direction was supplied. Use concise references to
Outcome where fields concern the same fact rather than paraphrasing it.>

- Direction contribution: <approved outcome, scenario, priority, or boundary advanced>
- User-observable effect: <direct effect, or "No direct effect; enables <next demonstrable outcome>">
- Why now: <approved sequence or real dependency>
- Direction decisions used: <exact source sections or decision IDs>
- New direction decisions required: None

## Authority and scope

- Authority: <precise request, issue, or plan/spec sections; required baseline identity>
- Repository: <repository identity; absolute checkout path only if needed>
- Dependencies: <prerequisite IDs and required outputs/states, or none>
- Allowed changes: <exact known paths, or bounded area for focused discovery>
- Out of scope: <adjacent work whose exclusion affects execution>
- Read-only context: <necessary authority, precedent, and owning tests>
- Assumptions: <non-blocking UNKNOWN facts and discovery owner, if any>

<State governing operating rules here with exact source references. Retain
history only where it establishes precedence, freshness, or an audit contract.>

<!-- contract-registry-flow:task-brief-template:begin -->
### Expected contract impact

- Plan refs: <stable ART/IF/INV refs — materialize | change | preserve>
- Current contract dependencies: <available capability -> docs/contracts/<subsystem>.json>
- Expected durable delta: <interface, artifact, ownership, state, or invariant the next task can use>

<Use these fields when relevant; otherwise write `Expected contract impact: none`.
For a task-local handoff, name its consumer and exact artifact here.>
<!-- contract-registry-flow:task-brief-template:end -->

## Work and acceptance criteria

- **AC-01:** <observable required behavior and completion result>
- **AC-02:** <distinct credible failure, refusal, or unchanged-state behavior>

<Add criteria for distinct approved outcomes. When an AC contains several rules,
use a short subordinate list under its stable ID. Keep work steps only when they
add necessary ordering or ownership beyond the criteria. A brief concrete example
can clarify an abstract rule without choosing an unapproved mechanism.>

### Finite-risk cases

<Include only for finite, material cases identified by the skill. Repeat the
following block per stable risk ID. A short-cell table is also suitable.>

#### R-01 — <plain-language risk; related AC IDs>

- Invariant: <property that must remain true>
- Material cases: <exact finite values, dimensions, or state transitions>
- Observable result and boundary: <decisive oracle at the real entry point>
- Implementation evidence: <fail-first, targeted, or owning evidence>
- Independent review probe: <distinct corroboration, or N/A with reason>
- Gate owner and stage: <who runs the owning/broad gate and when>

<Shared gate ownership may be stated once with explicit risk IDs.>

## Verification

Verification-design recommendation: <inline | separate — concrete reason>

| Evidence | Scenario/result or case reference | Command and owner |
|---|---|---|
| Fail-first / regression | <fault the test rejects, or why infeasible> | <command or focused discovery owner> |
| Targeted | <lowest reliable behavior/boundary, or R-ID> | <command or focused discovery owner> |
| Owning suite | <nearby regression protection> | <command> |
| Broader gate, if needed | <blast radius; gate stage or reference to shared ownership> | <command, owner, and any approval need> |

<Include applicable rows. Refer to case IDs for detailed scenarios and shared
gate ownership. Repeated flows need the first occurrence, its legitimate state
change, and the next real occurrence at the boundary that carries the risk.>

## Execution and handoff

Status: `ready | ready_for_preflight`
Task kind: `executable`

<Explain the status in ordinary language: the brief is prepared; name pending
execution prerequisites, or cite current evidence that they passed.>

Readiness route: <standalone guided preflight [— material uncertainty] | high-assurance preflight>

For an executable task package, derived `verification.md`, then ready
`preflight.md`, are required before implementation.

Launch guidance:

<Insert the four-key YAML block shown below. These are intended settings, not
claims about observed runtime configuration.>

### Execution sizing

- Sizing policy: <active-profile>@<config-version>
- Estimate: <integer agent calls>; <integer implementation minutes>
- Estimate confidence: <low | medium | high>
- Policy result: <fits | override_cannot_split_safely>
- Override, only when triggered and permitted: `decomposition_override: cannot_split_safely`
  — <triggered limits; candidate boundary considered; concrete coupling or
  coordination/rework reason; residual execution risk>

### Stops and next action

- Stops: <task-specific authority, ownership, scope, permission, or capability limits>
- Next action: <first pending preparation stage, then implementation; cite passed prerequisites>
- Required follow-on, when review is immediate: <ordered independent-review route from the skill>

<The follow-on applies after implementation or correction and any applicable
conditional stages. Do not use same-session self-review as that discovery or
acceptance step.>
```

Insert only this launch block at the indicated position:

```yaml
agent_tier: mechanical | standard | strong
reasoning: low | medium | high
review: mechanical | milestone | immediate
budget: <tool calls> / <time> / <context>
```

Sizing evaluates implementation-agent work using this launch pair. Policy
thresholds stay in `task-sizing.yaml`; record triggered limits for a split or
override. Do not present a trigger as automatically requiring decomposition.

### High-assurance addendum

Include only for the high-assurance profile or a named need for durable evidence.
Reference existing AC/risk IDs and authority entries instead of copying them.

- Artifact identity: <task ID, producing stage `task-brief-designer`, timestamp with timezone,
  exact primary authority, policy identity or UNKNOWN for preflight>
- Knowledge ledger: <confirmed facts with sources, frozen decisions, provisional
  assumptions and confirmation owners; unresolved blockers use the blocked form>
- AC execution matrix: <for every AC, record or reference its production invariant,
  positive and negative evidence, real entry point/boundary, first + state change
  + next occurrence where relevant, and verification dependency/disposition>
- Legacy-assumption checks: <entry points, guards, literals, identifiers, paths,
  or baselines at risk; focused search/test and required follow-through>
- Risk checks: <credible failure, consequence/escalation trigger, evidence,
  and residual gap; reference finite-risk cases where they already supply this>
- Verification-capability inventory: <each required fixture/helper/runner/oracle;
  task-local | prerequisite task | believed existing | blocked;
  owner/path and exact preflight confirmation question>
- Stage handoffs: <preflight confirms exact paths, dependencies, ownership,
  permissions, command syntax, oracles, and required freshness; implementation
  stays within confirmed scope and records commands and the supplied structured
  result; independent discovery reconstructs the scoped diff and corroborates
  every AC at the required boundary before a separate fresh acceptance decision,
  including after corrections>

## Composite parent

```markdown
# Task Brief: `<TASK-ID>` — `<concrete result delivered by the child set>`

## Outcome

<Original testable outcome, its user or next consumer, and why it is needed.>

## Child outcomes and sequence

<Explain how the pieces build on each other in ordinary language. State the
substantive boundary reason once; keep exact ownership and dependencies below.>

| Child | Outcome / owned output | Depends on | Brief |
|---|---|---|---|
| <TASK-ID.1> | <independently verifiable result and its consumer> | <IDs or none> | <path> |

## Authority and scope

- Authority: <exact approved sources and necessary baseline identity>
- Parent plan task / stable refs: <task, FLOW/ART/IF/INV refs>
- Original scope: <bounded work preserved across children>
- Out of scope: <exclusions that affect execution>
- Governing decisions: <applicable direction decisions and exact references>

## Coverage and closure

- Parent requirement / AC coverage: <every parent requirement or AC -> owning children>
- Shared artifacts/interfaces/invariants: <one owning child for each shared surface>
- Integration closure: <final executable integration child, or why child-local proof suffices>
- Leaf sizing: <all leaves fit the policy, or references to exact permitted overrides>

## Execution and handoff

Status: `decomposed`
Task kind: `composite`

This parent coordinates the work. Implement dependency-ready executable leaves;
the parent itself is not an implementation target. Completion requires every
mapped leaf, including integration closure, to finish its implementation and
required review route.

### Execution sizing

- Sizing policy: <active-profile>@<config-version>
- Original estimate: <integer agent calls>; <integer implementation minutes>
- Original required execution profile: <agent_tier>/<reasoning>
- Estimate confidence: <low | medium | high>
- Triggered decomposition rules: <configured rule names>
```

A composite has no launch metadata or readiness route. Preserve approved
direction in the parent and each affected child.

## Blocked design

Use only the abbreviated form below; direction gaps use the skill's
conversation-only direction-delta response instead.

```markdown
# Design block: <requested outcome as stated>

Status: `blocked_design`

## Missing decisions or authority

- <decision or authority gap; why it materially changes the task>

## Owner and smallest next action

- Owner: <user or decision owner>
- Next: <smallest planning/approval action; proof-task dependency if required>
```
