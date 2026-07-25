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
| `task-preflight` | Check readiness, ownership, commands, and decisive evidence when dirty ownership, dependencies, environment, permissions, helpers, fixtures, real-boundary capability, or a durable handoff creates material uncertainty. | A routine guided task can perform the same compact self-check inside the implementer. |
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
implementer self-preflight
        ↓
implement + risk-based tests + progressive verification
        ↓
human-readable result
        ↓
fresh-session acceptance review when metadata or risk calls for it
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
   residual risks, and next action. When independent review is required, end at
   `READY_FOR_REVIEW` and route the completed bytes to a fresh reviewer.

The brief designer and standalone preflight are optional in guided mode. Use
them when they reduce ambiguity or risk; do not create artifacts merely to
satisfy the diagram.

### When standalone preflight adds value

Use the implementer's compact self-preflight for routine guided work. Use
standalone `task-preflight` when a separate readiness pass can resolve a named
material uncertainty, such as:

- dirty or multi-writer ownership;
- a required environment, permission, dependency, helper, or fixture;
- real-boundary capability or an unresolved command and observable oracle; or
- a durable handoff between sessions.

A directly requested standalone preflight still returns a truthful readiness
result even when its incremental value is marginal. It should stay compact,
avoid broad baseline work without a named readiness reason, and recommend
implementer self-preflight for the next materially similar task. Explicit
high-assurance and orchestrated flows continue to require standalone
preflight.

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

`agent_tier`, `reasoning`, and `review` are intended launch guidance, not claims
about the eventual runtime configuration. Authors should choose the economical
values the task actually calls for. `review: immediate` means an immediate
handoff after implementation or correction to a fresh independent reviewer; it
never instructs the implementer to accept its own work. Metadata does not
replace the task's outcome, scope, acceptance criteria, or verification
commands.

## Review rules worth keeping

Independent review should spend effort where implementation evidence is most
likely to be misleading:

- account for every explicit finite task row and selected material risk
  dimension, keeping blocked or unchecked areas visible without promising to
  find every latent defect;
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

Independence is based on session authorship. Loading another skill, quoting its
instructions, or changing roles in the same session does not reset provenance.
A session that authored reviewed production bytes may perform a labeled
`SELF_CHECK_ONLY` and fix defects it finds, but it cannot issue an independent
verdict. Only a fresh reviewer may return `ACCEPT`, `CHANGES_REQUESTED`, or
`INCONCLUSIVE` for those bytes.

Every `CHANGES_REQUESTED` correction requires a fresh acceptance review. A
previous verdict never applies to corrected bytes.

### Verification gate ownership

- Initial implementer: fail-first evidence, targeted checks, the nearest owning
  suite, and a broader gate only when authority or blast radius justifies it.
- Discovery reviewer: targeted adversarial probes first; after a decisive
  failure, skip the broad gate unless it has a distinct authorized diagnostic
  purpose.
- Correction implementer: reviewer regressions followed by the nearest owning
  suite; leave an assigned final reviewer's aggregate gate untouched.
- Fresh final reviewer: rerun reviewer regressions, complete the finite review
  ledger against corrected bytes, and run one justified aggregate gate after
  adversarial evidence is clean.

### Optional tests-only reproducer

After fixing and reporting an independent `CHANGES_REQUESTED` verdict, the
reviewer may add a failing test only when the current user or exact review
invocation explicitly authorizes `tests_only_reproducer` and names the exact
writable test file or bounded test area. Task scope, `review: immediate`, or an
allowed test path is not write permission.

The reviewer must not change production code, shared test infrastructure,
dependencies, plans, or result artifacts, and must not stage or commit the
test. It must prove the focused intended failure and report status and diff side
effects. The verdict remains `CHANGES_REQUESTED`, and corrected production
bytes always require a fresh reviewer; the reproducer-writing session cannot
accept them.

## Recommended agent session usage for context reuse

- Keep the implementer session alive.
- Run review in a separate, independent session.
- Feed the reviewer’s complete findings and failing tests back to the implementer session.
- Run final acceptance in a new reviewer session.

If the implementer session becomes very long or confused, start a fresh correction session using the reviewer’s concise findings and tests. Context reuse is an optimization, not a requirement.

### A practical heuristic for the implementer context

  - Below 50%: normally resume the implementer.
  - 50–70%: resume for one focused correction if the session stayed clean.
  - Above 70%: prefer a fresh correction session with the findings and tests.
  - At any percentage: restart if the agent repeats work, relies on stale state, confuses roles, or loses track of findings.
