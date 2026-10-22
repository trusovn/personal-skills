# Project Direction: Local task orchestration

Status: owner-confirmed baseline
Date: 2026-10-22
Source: owner decisions from the direction interview and local harness follow-up.

This is the complete governing direction for this delivery. It describes desired
behavior; implemented capabilities are documented in the operator and architecture
references.

## Direction at a glance

- Problem: defined tasks still require the owner to copy prompts, findings, and
  results between agents and supervise ordinary implementation work.
- Desired experience: approve well-defined tasks and their authority once, then
  let an agent coordinate implementation, checks, independent review, bounded
  correction, and completion in order on the local machine.
- First useful proof: one task needs correction, then passes current checks,
  fresh independent review, and the final code-enforced gate. Accepted work is
  committed locally when safely supported. A dependent task stays blocked until
  that completion boundary is satisfied. Report missing harness qualification.

## How this should work in practice

| Situation | What should happen | When the owner must step in |
|---|---|---|
| Normal | Confirm scope, outcomes, permissions and stop conditions once. Coordinate implementation, checks, review and correction; pass the final gate; commit accepted work when supported; advance to the next approved task. Keep concise durable status. | No routine intervention. Successful completion does not require active notification. |
| Recovery | Preserve partial work, findings and evidence. Establish whether a worker still runs before launching another. Reuse useful implementation context or provide a compact handoff. A refused action returns a reason so the coordinator can recover within existing authority. | Recovery needs a missing decision, permission or capability, or writer ownership cannot be established. |
| Must stop | Preserve the reason and request help when safe recovery is unavailable, intent is unclear or conflicting, scope or permissions must change, or three correction-and-review cycles have failed for the task. | Notify the owner and preserve durable status; the owner resolves the blocker. |

## Priorities and conflict rule

1. Deliver trustworthy, independently reviewed work inside approved authority.
2. Complete ordinary work without further owner involvement.
3. Recover safely and preserve useful work, findings and evidence.
4. Make progress and requests for intervention easy to inspect.
5. Keep the first delivery small and practical.

Trustworthy readiness and approved authority take priority over continued
progress. Within those boundaries, recover without routine owner prompts.

## Scope

### In scope

- One local repository, well-defined ordered tasks, explicit scope and permissions.
- One dependable reviewed path: implement, check, independently review, correct
  when needed, obtain fresh review, and complete or request intervention.
- An agent coordinates execution, interprets findings and handles recovery.
  Code checks the decisive facts before committing accepted work and advancing.
- The final gate requires configured checks and independent reviews to pass,
  evidence to match current files, scope to remain approved, and no unresolved
  blocking findings. Agent completion claims alone cannot pass it. Code validates
  evidence; independent reviewers supply semantic judgment.
- Two early guards: no worker launch while another writer may still run, and no
  fourth correction after three unsuccessful correction-and-review cycles for
  the same task. Initial implementation is cycle zero. Persist the count across
  interruption and agent replacement.
- Automatic local commits containing only accepted task work, when the harness
  safely supports them. Report unavailable capability and keep advancement
  blocked; do not silently skip the commit boundary or claim a commit occurred.
- Structured machine-readable results for code-interpreted decisions. Markdown
  may explain work to people; prose alone cannot authorize acceptance.

### Not in scope

- Turning rough ideas or incomplete plans into ready tasks during a run.
- Multiple owner-facing workflow styles for ordinary work, a general recovery
  framework, or a deterministic controller for every conversational step.
- Automatic root-cause diagnosis of repeatedly unproductive approaches.
- Remote pushes, publication, permission expansion, parallel task writers,
  remote workers, multiple operators, or malicious-host defense.
- A background daemon or promised continuation after the harness session ends.

## Boundaries

### Trust

The local owner, machine, repository and approved task documents are trusted.
Agents are fallible. Check their claims, scope and completion judgments. A
reviewer must not accept its own implementation. Use approved sandbox boundaries
where available; establish required permissions before starting. Preserve user
work and durable evidence. Keep active controller and skill installations stable.

### Intervention and decision ownership

- May proceed: supported implementation choices, checks, task-local correction,
  safe recovery, context handoff, authorized local commit and advancement.
- Must ask or stop: missing or conflicting intent, unsupported decisions, scope
  expansion, missing permissions or capabilities, unsafe recovery, exhausted
  corrections, or inability to establish trustworthy readiness.
- Owner controls: scope, outcomes, authority, intervention boundaries and the
  meaning of ready. Technical work must not waive independent review, increase
  the three-correction limit, grant permissions or add remote effects.

## Direction ledger

- Confirmed: the hybrid model, final gate, early writer/correction guards,
  persistent three-correction limit per task, local commits when safely supported,
  intervention-only notifications, structured results, sequential execution,
  independent review and safe context handoff.
- Recommendations awaiting approval: none.
- Assumptions: task documents are sufficient for ordinary decisions; accepted
  task work can be committed without unrelated owner work; the harness can
  establish worker status, perform safe commits and notify the owner. The
  capability investigation must establish support or expose the limitation.
- Unresolved direction questions: none. Exact interfaces, message formats and
  notification mechanisms remain technical choices within these boundaries.

## Contract for technical planning

Cite this direction and the outcome or boundary each task advances. Technical
work may choose mechanisms inside it. Do not silently change readiness, review
independence, scope, trust, correction or intervention rules. Return a plain-language
direction change for owner approval if those choices need to change.
