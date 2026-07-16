---
name: task-acceptance-review
description: Independently review one staged task implementation against its task brief, fresh preflight packet, worker result, baseline, and run policy, then write a read-only acceptance report with exactly ACCEPT, CHANGES_REQUESTED, or INCONCLUSIVE. Use whenever asked to accept, independently verify, or re-review work produced by bounded-task-implementer. Do not use for ordinary PR/branch/file review without staged task artifacts, implementation or fixes, brief repair, preflight, tracker advancement, or orchestration; use senior-code-review directly for generic code review.
---

# Task Acceptance Review

Decide whether one bounded implementation is safe to advance by independently
checking it against the staged task contract. Own acceptance evidence and the
review verdict, not fixes, task design, repository readiness, or orchestration.

Repository and user instructions outrank this skill. Preserve pre-existing user
work and never claim ownership of it.

## Required inputs

Require:

- repository root and applicable instruction paths;
- path to one task brief and the exact preflight packet that cites it;
- path to the implementer JSON result;
- preflight baseline identity and the current implementation diff/state;
- run policy, including probe permissions and stop policy; and
- an authorized durable path for the acceptance report.

The packet must have status `ready`, identify the same task and brief, and
contain enough baseline evidence to separate task changes from pre-existing
user work. Treat worker verification and summaries as claims, not proof.

If a required input is missing, inconsistent, unreadable, stale beyond expected
same-thread task changes, or lacks authority for decisive evidence, stop broad
review work. Produce an `INCONCLUSIVE` report at the authorized path, or return
it inline when that path itself is missing. Name the blocker, owner, and
smallest next action; do not infer or repair the missing contract.

## Authority and read-only boundary

You may:

- inspect the task artifacts, current scoped diff, allowed surrounding code,
  tests, public entry points, and legacy-assumption locations;
- run proportionate independent probes and exact checks already authorized by
  the run policy; and
- write exactly one acceptance report at the supplied runtime path.

Do not modify production code, tests, fixtures, documentation, task artifacts,
dependencies, tracker state, or orchestration state. Do not write a patch or
fix a finding. Keep probe effects out of the reviewed repository unless the
policy explicitly provides disposable task-owned runtime paths and cleanup.
Record every authorized side effect and its disposition. If decisive evidence
would require an unauthorized, destructive, privileged, flaky, slow, or live
operation, do not run it; report the gap and use `INCONCLUSIVE` when that gap
prevents a truthful verdict.

## Workflow

1. Read applicable repository instructions, the complete brief and preflight
   packet, the implementer result, the run policy, and only the cited authority
   needed to interpret the acceptance contract. Confirm task IDs, paths,
   digests, artifact statuses, permissions, and result status agree.
2. Reconstruct exact review scope from the preflight baseline to current state:
   - compare `HEAD`, exact `git status --short`, and recorded dirty-path
     digests or deletion states;
   - identify task-owned changes, pre-existing user work, runtime artifacts,
     and unexplained changes separately;
   - compare task-owned paths with the packet's allowed paths and the worker
     result's `files_changed`; and
   - treat unexplained overlap, changed authority, or an inseparable baseline
     as `INCONCLUSIVE`, not as permission to review a guessed diff.
   Expected changes attributed to the same bounded implementation thread do not
   alone invalidate the packet.
3. Apply `senior-code-review` when available to the scoped diff. Reuse its risk
   map, end-to-end tracing, candidate-finding validation, severity rules, and
   read-only judgment. This skill retains task-artifact traceability and the
   three acceptance verdicts. If unavailable, locally trace changed entry
   points, state and side effects, failure paths, callers, and compatibility;
   report only concrete, evidenced defects.
4. Apply `testing-discipline` when available to evidence adequacy. Reuse its
   contract/oracle analysis, lowest reliable test level, decisive real-boundary
   evidence, negative behavior, determinism, and progressive verification.
   This skill retains acceptance and routing authority. If unavailable, apply
   those six checks locally without creating a generic test strategy.
5. Build one evidence row for every brief AC. Check both applicable levels:
   - the pure function, state, or module contract; and
   - behavior through the real public entry point and decisive wiring.
   Record positive, negative or unchanged-state evidence, the independent
   oracle, commands or probes, and any gap. Passing unit tests cannot substitute
   for required public-flow evidence.
6. For each new repeated, resumed, retried, recovered, paginated, or migrated
   flow, independently execute the first occurrence in an authorized disposable
   environment, observe or apply its legitimate state change, then execute the
   next occurrence and assert its externally meaningful result. Do not infer
   the second occurrence from unit/state tests or the worker's claim. If this
   decisive probe cannot be run safely and no equivalent independent evidence
   exists, use `INCONCLUSIVE`.
7. Revisit every preflight legacy-assumption finding. Trace the changed flow
   through the exact old guards, literals, fixed identifiers/paths, baseline
   comparisons, and cleanup or compatibility behavior. Search narrowly for
   reachable assumptions the implementation may have missed.
8. Run the narrowest authorized independent probe or targeted command that can
   corroborate each material claim. Run broader gates only after targeted
   evidence passes and when blast radius and policy justify them. Record exact
   commands, working directories, environment, exit status, observed signal,
   side effects, and gaps. Never report a submitted or unrun command as passed.
9. Validate candidate findings against surrounding code, tests, and observed
   behavior. Each finding must identify a current file location, triggering
   input/state, consequence, evidence, affected AC, and smallest corrective
   direction without writing the patch. Put unproved concerns under open
   questions or residual risks. A clean review is valid; do not manufacture a
   finding.
10. Read `references/acceptance-report-template.md`, write exactly one report,
    and select exactly one verdict under the rules below. Recheck that the
    report itself is the only intentional write and that it does not advance
    the tracker or invoke another task.

## Verdict and routing rules

Use exactly one verdict:

- `ACCEPT`: every required AC and gate is independently satisfied, task scope
  is clean, negative and lifecycle behavior are proved where required, and no
  blocking finding or question remains. State any non-blocking residual risk.
- `CHANGES_REQUESTED`: an evidenced in-scope production or test defect can be
  corrected without changing the brief, baseline authority, allowed paths,
  helpers, dependencies, or permissions. Route to the same
  `bounded-task-implementer` thread, then require a new acceptance review.
- `INCONCLUSIVE`: missing or ambiguous authority, an invalid/stale preflight,
  unexplained baseline or dirty overlap, missing verification capability,
  environment failure, unauthorized decisive probe, or ambiguous contract
  prevents a truthful decision. Route to the owning earlier stage or user.

Route contract defects or missing product/architecture authority to
`task-brief-designer` or the user. Route current-state failures such as changed
baseline authority, absent paths/helpers, invalid commands, dependencies, or
permissions to `task-preflight`. A request for wider paths or shared
infrastructure goes through task-brief design and then fresh preflight. Only an
`ACCEPT` verdict routes to `task-orchestrator`, which alone may advance state or
perform an authorized commit.

Do not send an unclear requirement to implementation as if it were a coding
defect. After any correction, review again; never reuse the prior verdict.

## Output contract

Use the seven fixed headings and tables in
`references/acceptance-report-template.md`. The report must identify the task,
repository root, producing stage, creation time, artifact status/verdict,
authoritative input paths, baseline, exact scope, findings, per-AC evidence,
independent commands/probes, questions, residual risks, and one next route.

Order findings P0 through P3 using `senior-code-review` severity meanings. Use
`No findings.` when the evidence is clean. Link large inputs by path instead of
copying them. Distinguish confirmed facts, decisions inherited from authority,
assumptions, questions, and unverified boundaries.

Do not launch subagents, modify `task-orchestrator`, run live comparisons,
implement corrections, mark the task complete, or invoke the next task as part
of normal execution.

## Definition of done

- Scope is reconstructed from the recorded baseline without absorbing user
  work or unexplained changes.
- Every AC has independent evidence or an explicit blocking gap at both
  applicable contract and public-entry levels.
- Every relevant lifecycle extension proves the first state change and the next
  real occurrence.
- Findings are concrete, located, severity-ordered, and correction-directed
  without patches; clean work receives no invented findings.
- Commands and submitted claims are reported truthfully, including side effects
  and unverified boundaries.
- Exactly one justified verdict and owner-specific next route is present, and
  only the acceptance report was intentionally written.
