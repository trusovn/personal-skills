# Task Orchestrator: Revised Direction

Status: approved

Sources:

- [direction.md](direction.md)
- [stage-3-mvp-rebaseline.md](stage-3-mvp-rebaseline.md)
- Owner decisions recorded in the direction interview on 2026-07-29

## Direction at a glance

- **Problem:** Once tasks are defined, coordinating implementation still
  requires repeatedly copying prompts, findings, and results between agents.
  This prevents the owner from leaving the work to run.
- **Desired experience:** Give the system a set of well-defined tasks, approve
  its authority once, and leave. The system should implement, check, review,
  correct, and finish each task in order without routine owner involvement.
- **First useful proof:** Launch the system on one well-defined task document.
  Without further owner intervention, it implements the task, checks the work,
  sends it to a separate reviewer, corrects any findings, obtains fresh
  acceptance, creates a local commit, and clearly reports that the task is
  ready.

## How this should work in practice

| Situation | What should happen | When the owner must step in |
|---|---|---|
| Normal | Before the run, the system presents the approved work's scope and intended outcomes, any permissions still needed, and any stop conditions that differ between tasks. After one confirmation, it carries each task through implementation, checks, independent review, correction, fresh review, acceptance, and a local commit. It reports “ready” and, in the full experience, continues to the next approved task. | No further intervention is needed for ordinary work. |
| Recovery | The system recovers from an interruption, crash, timeout, or failed agent when it can safely continue within the same task and authority. It keeps using the same implementation agent while the existing context remains useful. When accumulated context would reduce reliability or waste tokens, it gives a concise, complete handoff to a fresh implementation agent. | The owner steps in only when the system cannot establish a safe state, repeated recovery fails, or recovery would require new authority. |
| Must stop | The system stops instead of guessing when requirements are unclear or conflict, a decision cannot be inferred from the task and its supporting documents, required authority is missing, the work has moved outside the approved scope, or progress has become persistently unproductive. By default, three unsuccessful fix-and-review cycles on the same issue trigger a stop. | The owner resolves the ambiguity, changes the authority or stop rule, or decides whether the approach should be reconsidered. |

Both “ready” and “needs attention” must produce an active notification and a
durable, concise status that the owner can inspect later if the notification is
missed.

## Priorities and conflict rule

1. Produce a trustworthy, independently reviewed result that is genuinely
   ready.
2. Complete ordinary work without owner intervention after startup.
3. Stay within the task, supporting documents, and authority granted upfront.
4. Recover automatically from interruptions and correct review findings.
5. Make completion or required intervention unmistakable.

Conflict rule: trustworthy readiness and the approved task boundary take
priority over uninterrupted progress. The system stops rather than guesses
when either is threatened. Within those boundaries, it continues autonomously
instead of asking for routine confirmation.

## Scope

### In scope

- Accept a set of already well-defined, ordered tasks.
- Present the scope, intended outcome, required permissions, and applicable
  stop conditions before work begins, then obtain one confirmation and grant
  of authority.
- Follow one dependable path for every task: implement, check, independently
  review, correct when needed, review again, and either accept or stop.
- Use a separate reviewer that did not implement the work.
- Let the implementer and reviewer use different capabilities when that
  improves the quality of review. Their exact setup may be fixed initially.
- Recover from ordinary interruptions without losing completed work or
  repeating it unnecessarily.
- Reuse an implementation agent's context while it remains helpful, and hand
  the work to a fresh agent before accumulated context harms reliability or
  wastes tokens.
- Bound every correction loop. Initially, the default is three unsuccessful
  fix-and-review cycles on the same issue, with a different limit allowed when
  the owner chooses it upfront.
- After independent acceptance, create a local commit that contains the
  accepted task work. For a set of tasks, continue to the next approved task.
- Notify the owner clearly when work is ready or needs attention, and preserve
  a status that can be checked later.

### Not in scope

- Turning rough ideas or an inadequately defined plan into ready tasks. The
  first version may require this preparation to happen before the run.
- Choosing among multiple workflow styles for ordinary tasks. The initial
  owner experience uses the same reviewed path every time.
- Automatically diagnosing that a poor architecture choice is the root cause
  of repeated problems. The initial protection is a bounded stop with useful
  evidence; smarter diagnosis will come later.
- Pushing commits, publishing changes, or making other remote changes.
- Automatically granting broader permissions after startup.
- Parallel task execution, remote workers, or multiple operators.
- Defending against a malicious person or process that already controls the
  trusted local machine and project files.

## Boundaries

### Trust

- The owner, local machine, repository, and approved task documents are
  trusted at the start of a run.
- Agents are fallible. Their claims, chosen scope, and completion judgments
  must be checked rather than accepted on trust.
- Review is independent: an agent that changed the project cannot accept its
  own work.
- Agent actions should run inside an approved sandbox—a restricted environment
  that limits what they can change or access. When that is unavailable, all
  required permissions must be requested before starting.
- Protection against a malicious actor with control of the trusted local
  environment is not a design target.

### Intervention and decision ownership

- **May proceed without asking:** ordinary implementation choices supported by
  the task, checks, review, task-local corrections, safe recovery, context
  handoff, local commit after acceptance, and advancement to the next approved
  task.
- **Must ask or stop:** unclear or conflicting intent, a decision not supported
  by the supplied documents, scope expansion, new permissions, unsafe or
  ambiguous recovery, repeated failure, exhausted correction cycles, or
  inability to establish trustworthy readiness.
- **Owner-controlled changes:** task scope and intended outcome, granted
  authority, stop conditions, correction-cycle limit, the requirement for
  independent review, the meaning of “ready,” permission expansion, and any
  remote or publishing action.

## Direction ledger

### Confirmed decisions

- The full goal is to submit several defined tasks and let the system complete
  them one after another.
- The first useful proof is one task completed end to end without intervention
  after startup.
- “Ready” requires completed implementation, the required checks, acceptance
  by a separate reviewer, and no unresolved question.
- The initial experience uses the same reviewed path for every task.
- Startup confirmation covers the run's scope and intended outcomes,
  permissions still needed, any stop conditions that differ between tasks, and
  the authority to proceed.
- Recoverable failures and ordinary review corrections do not require owner
  involvement.
- Unclear or conflicting requirements, decisions unsupported by the supplied
  documents, and failures that cannot be safely recovered require owner
  intervention.
- Three unsuccessful fix-and-review cycles on the same issue are the initial
  default stop point; the owner may choose a different bounded limit upfront.
- Existing implementation context should be reused while helpful, then
  transferred through a concise handoff before it becomes harmful or wasteful.
- The reviewer is independent from the implementer. Reviewer capability may
  differ from implementer capability and may use a fixed initial setup.
- Accepted task work is committed locally before the full flow advances. The
  system does not push remotely.
- Completion and stops produce both an active notification and durable status.
- The local owner, repository, and task documents are trusted; agents are
  fallible and should operate inside a sandbox where possible.

### Recommendations awaiting approval

- None.

### Assumptions

- Supplied task documents contain enough context, scope, and expected outcome
  for ordinary implementation decisions.
- The local repository can be brought to a state where each accepted task can
  be committed without including unrelated owner work.
- A local notification mechanism is available or can be connected; the exact
  notification method is an implementation choice.

### Unresolved direction questions

- None currently block downstream planning.

## Contract for technical planning

- Technical work must cite the direction outcome, situation, priority, or
  boundary it advances.
- Technical work may choose implementation details inside this direction.
- Technical work may not silently change what “ready” means, weaken independent
  review, add routine owner prompts, widen authority, make correction
  unbounded, remove the local task commit, add remote effects, or treat an
  optional internal mechanism as an owner requirement.
- If a useful technical approach requires a new owner-visible behavior,
  priority, trust assumption, intervention rule, or scope decision, planning
  must return a plain-language direction change for owner approval first.

## Source notes and downstream review

This document replaces the technical emphasis of `direction.md` with the
owner's desired experience and boundaries. The controller design, records,
commands, workflow representation, agent transport, and other mechanisms in
the source documents are possible ways to serve this direction; they are not
direction merely because they have already been planned or implemented.

The following parts of `stage-3-mvp-rebaseline.md` need review against this
direction:

- The plan treats fast, reviewed, and strong workflow selection as an MVP
  owner capability. The confirmed initial need is one dependable reviewed
  path. Already implemented configurability may remain, but it should not
  complicate or redefine the owner experience.
- The plan defers controller-owned commits until after the MVP and runs its
  first real proof with commits off. This direction requires a local commit
  after acceptance and before advancing through the full task flow, including
  the first useful end-to-end proof unless the owner approves a direction
  change.
- The plan uses a fixed context threshold for choosing between reuse and a
  fresh implementation session. The governing need is the practical result:
  reuse context while it helps, then hand off without losing authority, work,
  findings, or evidence. The exact threshold remains a technical choice that
  should be validated against reliability and token cost.
- The plan already supports bounded correction and independent fresh review;
  those choices align with this direction. Its later automated diagnosis of a
  failing approach should remain subordinate to the confirmed initial rule:
  stop after bounded unproductive correction and give the owner useful
  evidence.
