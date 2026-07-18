# Task implementation flow

These four skills provide a reusable implementation discipline without making
every task carry an orchestration-grade artifact chain. The default is a
lightweight guided flow. A high-assurance profile remains available for work
that benefits from durable handoffs, exact freshness evidence, and
machine-readable results.

## Goals

- Make bounded implementation more consistent without repeatedly prompting an
  agent to define acceptance criteria, add tests, verify progressively, preserve
  user work, and report evidence.
- Spend tokens on the task and its highest-risk behavior rather than repeated
  stage paperwork.
- Scale assurance with risk instead of treating every task as mission-critical.
- Preserve an orchestrator-compatible path for unattended or audited work.

## Skills

| Skill | Use it for | Skip it when |
|---|---|---|
| `task-brief-designer` | Create or tighten a bounded task contract. It defaults to a delta check when a useful brief already exists. | The user request already gives an unambiguous outcome, scope, and acceptance criteria for a small task. |
| `task-preflight` | Check readiness, ownership, commands, and decisive evidence before implementation. | A routine task can perform the same compact self-check inside the implementer. |
| `bounded-task-implementer` | Implement one bounded task with risk-based tests, progressive verification, and a useful handoff. | The request is planning, review-only, or too ambiguous to implement safely. |
| `task-acceptance-review` | Independently assess the scoped result and return `ACCEPT`, `CHANGES_REQUESTED`, or `INCONCLUSIVE`. | The task does not need independent review under its metadata or risk. |

## Guided profile: default

Use guided mode for most ordinary bounded tasks, especially when a person is
launching the skill directly.

```text
existing request or brief
        ↓
fill only meaningful contract gaps
        ↓
compact readiness/self-preflight
        ↓
implement + risk-based tests + progressive verification
        ↓
human-readable result
        ↓
review when metadata or risk calls for it
```

Guided mode carries these defaults so the user does not need to repeat them:

1. State or infer the smallest testable outcome and bounded scope. Ask only
   when a missing decision could materially change the implementation.
2. Define concise acceptance criteria when they are absent. Include positive
   behavior and the most credible negative, unchanged-state, or lifecycle case.
3. Preserve pre-existing user work and stop on ownership overlap.
4. Add or update the lowest-level reliable tests. For a bug, establish
   fail-first evidence when feasible. Cross the real boundary when lower-level
   tests cannot prove wiring, persistence, concurrency, recovery, or another
   material risk.
5. Run the targeted check first, then the nearest owning suite, then only the
   broader gate justified by blast radius and authorization.
6. Finish with a concise human summary: outcome, changed files, verification,
   residual risks, and next action.

The brief designer and standalone preflight are optional in guided mode. Use
them when they reduce ambiguity or risk; do not create artifacts merely to
satisfy the diagram.

## High-assurance profile

Use high-assurance mode when explicitly requested, when an orchestrator or
machine output schema is supplied, or when durable evidence is proportionate
to the risk. Typical signals include:

- security, authorization, privacy, or credential boundaries;
- migrations, irreversible writes, recovery, or destructive state;
- concurrency or multi-process coordination;
- multiple independent writers or agents in one worktree;
- complex staged/unstaged user work that must remain separable;
- audited or unattended execution requiring resumable machine contracts.

High-assurance mode uses the complete chain:

```text
task brief (`ready_for_preflight`)
        ↓
fresh preflight packet (`ready`)
        ↓
bounded implementation + structured worker result
        ↓
independent acceptance report
        ↓
orchestrator or human advancement
```

It may require exact digests, durable external artifacts, a supplied result
schema, and strict entry/exit statuses. A guided run that encounters one of
these needs should pause and recommend the smallest escalation rather than
silently rebuilding the entire chain.

## Task metadata

Durable briefs put this compact block near the top:

```yaml
agent_tier: strong
reasoning: high
review: immediate
budget: 30 tool calls / 90 minutes / 100k context
```

- `agent_tier`: `mechanical`, `standard`, or `strong`.
- `reasoning`: `low`, `medium`, or `high`.
- `review`: `mechanical`, `milestone`, or `immediate`.
- `budget`: a soft checkpoint unless the user or repository explicitly calls it
  a hard limit.

Metadata guides execution; it does not replace the task's outcome, scope,
acceptance criteria, or verification commands.

## Review rules worth keeping

Independent review should spend effort where implementation evidence is most
likely to be misleading:

- exercise the real public path when unit evidence can miss wiring;
- for repeated or recovered behavior, perform the first state change and the
  next real occurrence;
- test interacting state rules across selected and non-selected entities;
- check exact cardinality with zero, one, and two owners where “exactly one” is
  an invariant;
- check exact ready sets and latest/current ordering rather than only presence;
- test coherent tampering when evidence files can be rewritten together.

A digest stored beside mutable bytes proves internal consistency, not
immutability. Claims of immutability require an independently protected anchor
or an explicitly narrower threat model.

Every `CHANGES_REQUESTED` correction requires a fresh acceptance review. A
previous verdict never applies to corrected bytes.
