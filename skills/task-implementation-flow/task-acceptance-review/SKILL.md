---
name: task-acceptance-review
description: Independently review one bounded implementation against its request or task brief, scoped diff, tests, and material risks, then return ACCEPT, CHANGES_REQUESTED, or INCONCLUSIVE. Use for direct manual implementations as well as orchestrated worker results, especially when task metadata requires immediate review or behavior crosses stateful, public, security, concurrency, recovery, or migration boundaries. Default to a concise guided review; require full packet/digest reconstruction only for explicit high-assurance work.
---

# Task Acceptance Review

Decide whether one bounded implementation is safe to advance. Corroborate the
claims most likely to hide defects instead of recreating the implementer's
entire process.

Repository and user instructions outrank this skill. Preserve pre-existing user
work and keep the review read-only except for an authorized report artifact.

## Choose the profile

Use `guided` by default. Use `high-assurance` when explicitly requested or when
the review is given a preflight packet, machine worker result, run policy, and
durable acceptance path from an orchestrated flow.

### Guided inputs

Require enough to identify:

- the user request, task brief, or acceptance criteria;
- the current task-owned diff or changed paths;
- implementation and verification claims, if available; and
- repository instructions and permissions for independent checks.

Do not return `INCONCLUSIVE` merely because no preflight packet, digest ledger,
worker JSON, or report path exists. Reconstruct the relevant scope from current
Git state and the task conversation/artifact when it is safely separable.

### High-assurance inputs

Require the exact task brief, ready preflight packet, worker result, recorded
baseline, run policy, and authorized report path. Inconsistency, stale authority,
or an inseparable baseline is `INCONCLUSIVE`; do not downgrade silently.

Treat implementer summaries and passing commands as submitted claims, not
independent proof in either profile.

## Review workflow

1. Read applicable instructions, the task contract, the scoped diff, and the
   implementation evidence. Confirm the intended outcome, allowed scope, and
   profile.
2. Reconstruct task ownership:
   - compare changed paths with stated scope and implementation claims;
   - separate pre-existing user work, task changes, and runtime artifacts;
   - treat unexplained or inseparable overlap as `INCONCLUSIVE`.
   In high-assurance mode, also compare every recorded Git, index/worktree,
   authority, policy, dependency, and environment identity.
3. Review the changed behavior end to end. Trace public entry points, callers,
   state transitions, side effects, error paths, cleanup, and compatibility
   where relevant. Report only concrete defects with a triggering condition and
   consequence.
4. Build concise evidence for each AC. Check the lowest-level contract and the
   real public/decisive boundary when both matter. Passing unit tests cannot
   replace public wiring evidence.
5. For repeated, resumed, retried, recovered, paginated, or migrated behavior,
   independently execute the first occurrence, observe or apply its legitimate
   state change, then execute the next real occurrence in authorized disposable
   state. Do not infer the second occurrence from a pure function or worker
   claim.
6. Run the narrowest authorized independent probe that can corroborate each
   material claim. Run broader gates only after targeted evidence passes and
   when blast radius justifies the cost. Record exact commands, results, side
   effects, and unverified boundaries.
7. Validate each candidate finding against surrounding code and observed
   behavior. Include location, trigger, consequence, evidence, affected AC, and
   smallest corrective direction. Keep unproved concerns as questions or risks.
8. Return one verdict and next route. Write a durable report only when requested
   or required by high-assurance mode.

## Adversarial checks for stateful work

Apply the relevant checks, not a generic exhaustive matrix:

- Cross product selected/current entities with non-selected entities so a
  valid primary state cannot hide an invalid sibling state.
- When the invariant says exactly one owner/active/current item, test zero, one,
  and two distinct owners.
- Verify current/active attempt ordering against the latest attempt, not merely
  membership or existence.
- Compare the exact ready/eligible set with dependency state; “at least one
  ready” is insufficient when all eligible items must be represented.
- Check terminal states against every subordinate state so stopped/complete
  parents cannot retain running children.
- Reject type confusions such as booleans accepted as integers and strings
  accepted as collections when those values cross persistence or API
  boundaries.
- For tamper claims, modify related evidence coherently, including recomputed
  internal digests. A digest stored with mutable evidence proves consistency,
  not immutability; stronger claims need an independent anchor.

Choose these cases because they catch interacting invariant failures that
ordinary happy-path and one-field corruption tests routinely miss.

## Verdict and routing rules

Use exactly one verdict:

- `ACCEPT`: all required ACs and justified gates are independently satisfied,
  scope is clean, and no blocking finding or question remains.
- `CHANGES_REQUESTED`: a concrete in-scope production or test defect can be
  corrected without changing authority, scope, dependencies, permissions, or
  required infrastructure.
- `INCONCLUSIVE`: ambiguous authority, inseparable scope, missing decisive
  capability, stale high-assurance inputs, environment/permission failure, or
  an unverified required boundary prevents a truthful decision.

Route `CHANGES_REQUESTED` to the same implementation thread when possible.
After any correction, run a fresh acceptance review against the corrected bytes;
never reuse or append acceptance to the prior verdict as if it still applied.

Route contract defects to the user or `task-brief-designer`; current-state or
high-assurance freshness failures to `task-preflight`; and wider scope/shared
infrastructure back through brief design. Only an `ACCEPT` verdict may advance
an orchestrated task.

## Output contract

For guided review, default to a concise human-readable response:

```markdown
Verdict: ACCEPT | CHANGES_REQUESTED | INCONCLUSIVE

Findings:
- <severity, location, trigger, consequence, evidence, affected AC, direction>

Evidence:
- <AC or risk: independent probe and result>

Scope / residual risk: <summary>
Next: <one exact route>
```

Say `No findings.` when evidence is clean. Do not create a report file unless
the user requested one.

For high-assurance review, read
`references/acceptance-report-template.md`, write exactly one report, and
include the full baseline/freshness and command records. The report must be the
only intentional write.

## Boundaries

Do not implement fixes, edit reviewed files, update task briefs/plans/trackers,
advance orchestration, commit, launch subagents, or run unauthorized slow,
flaky, destructive, privileged, live, or networked probes.

## Definition of done

- Scope is safely separated from user work.
- Every AC has independent evidence or an explicit blocking gap at the level
  needed to prove the behavior.
- Relevant lifecycle and interacting-state risks receive adversarial evidence.
- Findings are concrete and severity-ordered; clean work gets no invented
  finding.
- Exactly one justified verdict, residual-risk statement, and next route are
  present.
