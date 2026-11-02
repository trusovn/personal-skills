# Task brief forms

Choose the applicable form below. Place explanations in the indicated sections;
optional fields serve a concrete task need, not a checklist to fill. For an
existing adequate brief, preserve equivalent sections and make a local delta.
The skill owns routing and evidence rules; these forms suggest the reading order.
Adapt headings and omit empty fields. Preserve applicable direction decisions
where they govern outcome or authority; do not add a separate history account.

## Executable brief

Use for `ready` or `ready_for_preflight` leaves. The opening explains the work;
execution status and launch guidance come after its requirements and evidence.

```markdown
# Task Brief: `<TASK-ID>` — `<concrete result to deliver>`

## Outcome

<What completion demonstrates, who uses the result, and what it enables next.
Distinguish what this task defines, what it executes, and what later work owns.
Link to project purpose rather than retelling it.>

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

**AC-01 — <descriptive title>**

<One cohesive completion condition, or short flat bullets for independent rules.>

**AC-02 — <descriptive refusal or preservation title>**

<Required failure, boundary, lifecycle or unchanged-state behavior. Cite exact
normative sections for finite requirements rather than repeating them elsewhere.>

<Keep required values and transitions visible here or in precise authority.
Setup, observation methods and implementation choices belong to their owners.>

## Evidence boundaries

Verification-design recommendation: <inline | separate — concrete reason>

<Optional consequential risk, invariant, essential proof boundary or capability
uncertainty that adds information beyond acceptance. No risk IDs or six-field
blocks are required. Detailed scenarios, fixtures, assertions, evidence reuse,
independent probes and gate allocation belong in derived verification.md.>

## Execution and handoff

Status: `ready | ready_for_preflight`
Task kind: `executable`

Next: <first pending preparation action, or current evidence for completed prerequisites>.
The brief is prepared; derived `verification.md`, then ready `preflight.md`,
are required before implementation. Use <standalone guided | high-assurance>
preflight; name a material uncertainty here only when applicable.

Workflow: [submission route](<relative path to the active installation skills/README.md#submission-route>).
<Retain task-specific outputs, consumers, deviations and stops when relevant.
Do not repeat the default report inventory or the shared route.>

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
- Verification requirements: <precise authority for required AC/invariant,
  positive/negative, real-boundary and first/change/next proof; derived
  verification.md owns the detailed matrix and evidence/capability disposition>
- Legacy assumptions: <task-specific entry points, guards, literals, identifiers,
  paths or baselines at risk; detailed probes belong in verification>
- Capability uncertainties: <required mechanism and exact preflight question;
  distinguish task-local, prerequisite, believed-existing and blocked capability>
- Machine/audit obligations: <exact required schema, result and policy paths,
  freshness identities and downstream consumers; omit if not applicable>

<Keep exact provenance, knowledge and direction decisions required by authority.
Reference shared preflight freshness and submission rules; do not duplicate
verification matrices or generic stage instructions.>

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
direction in the parent and each affected child. Apply the same concise content
boundary to the parent and every child: titled ACs, optional informative risks,
and detailed proof in each owning leaf verification design.

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
