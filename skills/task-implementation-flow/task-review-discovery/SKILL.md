---
name: task-review-discovery
description: Independently publish current evidence and confirmed findings for one bounded implementation without deciding acceptance. Produces a complete or explicitly partial evidence report with facts, suggested severities, probe results, and a continuation block for a separate acceptance decision call. Use when a fresh session independent of production authorship must gather review evidence, especially when behavior crosses stateful, public, security, concurrency, recovery, or migration boundaries.
---

# Task Review Discovery

Publish the current evidence and confirmed findings for one bounded
implementation so a separate acceptance decision call can decide. Corroborate
the claims most likely to hide defects instead of recreating the implementer's
entire process. Account for the task's explicit finite risks before spending
the review budget on broad regression.

Repository and user instructions outrank this skill. Preserve pre-existing user
work. Ordinary review is read-only except for an authorized canonical discovery
report artifact in the task package.

Discovery has no decision authority. It never issues or implies an acceptance
verdict such as `ACCEPT`, `CHANGES_REQUESTED`, or `INCONCLUSIVE`, never records
an approved deferral, and never advances work. Those decisions belong to the
separate acceptance decision call that consumes this evidence.

## Establish discovery provenance first

Independence is a property of session authorship, not of the skill text or role
currently loaded. Before gathering evidence, determine whether this session
authored any production bytes in the reviewed diff.

- An independent session continues to the discovery workflow below.
- A session that authored reviewed production bytes may perform a clearly
  labeled `SELF_CHECK_ONLY` discovery pass, but it must not present its rows as
  independently corroborated evidence, and it must not issue any acceptance
  verdict, approved deferral, or advancement. Loading this skill does not reset
  authorship. The route is always a fresh discovery call.
- `SELF_CHECK_ONLY` is a non-verdict label, not an orchestrator status, and
  never advances work.

## Inputs

Require enough to identify:

- the authority: the user request, task brief, or acceptance criteria;
- the derived verification design and the explicit task-package context when
  present (for example the package's recorded ART-003 decision context); a
  guided direct edit may supply conversational context instead, and absence of
  a high-assurance packet alone does not prevent guided discovery;
- the current task-owned diff or changed paths;
- the current submission: implementation and verification claims, the
  implementer's scenario-to-evidence map, and any unfinished or blocked rows;
- applicable conditional evidence: prior ledgers, prior review continuations,
  correction findings, and reviewer regressions.

Treat implementer summaries and passing commands as submitted claims, not
independent proof.

## Discovery workflow

1. Establish provenance, then read applicable instructions, the task contract,
   verification design, supplied context, scoped diff, current submission, and
   any prior review continuation. Confirm the outcome, allowed scope, and
   current byte identity when available.
2. Reconstruct task ownership before behavioral probes:
   - compare changed paths with stated scope and implementation claims;
   - separate pre-existing user work, task changes, and runtime artifacts;
   - publish unexplained or inseparable overlap as an explicit scope gap; do
     not absorb it or review a guessed scope as authoritative;
   - compare recorded Git, index, and worktree identities separately when they
     are supplied; matching worktree bytes and short-status text do not prove a
     matching index blob;
   - never reset, restage, overwrite, or claim ownership of user state.
3. Build a concise completeness ledger before running any broad suite. Give
   each row a stable task-derived identity and record:
   `AC/invariant -> explicit cases -> submitted evidence -> independent probe ->
   pass | fail | blocked | unchecked, with reason`, plus the setup/oracle
   needed to reproduce the row and the exact probe command or the concrete
   reason it was not run.
   - Start with explicit contract cases and the material dimensions of selected
     high-risk invariants; the supplied task context (verification design,
     recorded ART-003 context, finite-risk matrix) selects bounded decisive
     material-risk probes.
   - Every material row named by the authority appears in the ledger. A
     material authority row omitted from the submitted tests or verification
     scenarios cannot vanish behind green tests; it stays visible with its
     current evidence state and concrete reason.
   - Consume a supplied prior ledger as continuation context. Preserve its row
     identities, but corroborate current bytes: a prior `pass` guides probe
     selection and is not current evidence.
   - Separate required/material rows from optional risks so every required row
     has a visible disposition when discovery ends.
4. Batch narrow static traces and targeted adversarial probes across the
   ledger before any aggregate gate. Review public entry points, state
   transitions, side effects, error paths, cleanup, and compatibility where
   relevant. A first defect does not imply sibling rows are clean. Continue
   after a finding while remaining probes are independent, safe, authorized,
   and affordable.
5. Check the lowest-level contract and the real public/decisive boundary when
   both matter. Passing unit tests cannot replace public wiring evidence. For
   repeated, resumed, retried, recovered, paginated, or migrated behavior,
   independently execute the first occurrence, observe or apply its legitimate
   state change, then execute the next real occurrence in authorized disposable
   state. Do not infer the second occurrence from a pure function or worker
   claim.

   When a required/material row depends on a machine-readable schema or other
   executable validator contract, independently exercise that validator rather
   than treating schema text, producer-side validation, deserialization, or an
   unrelated passing suite as proof. Use at least one instance that should be
   valid and one deliberately invalid instance that targets the changed or
   acceptance-relevant constraint, and confirm the validator accepts and
   rejects them respectively. For JSON Schema, use a validator that implements
   the schema's declared draft (for example Draft 2020-12 when the schema
   declares it). If the required validator boundary cannot be executed, keep
   that ledger row `blocked` or `unchecked` with the concrete reason; it cannot
   be reported as passed.

   For process-lifecycle rows, exercise the real local process boundary with
   observable synchronization and bounded waits, not arbitrary sleeps,
   unbounded waits, or a pure mock. After each probe, confirm bounded
   observable cleanup: descendant and process-group disappearance plus
   inherited-pipe release. Incomplete cleanup fails the probe, and no fixture
   process survives discovery.
6. Reconcile and own the aggregate-gate record:
   - Immediately before launching an aggregate gate, reconcile the frozen
     ledger against the task contract and scoped diff. Proceed only when every
     safely runnable required/material row has current targeted evidence, every
     blocked or unchecked row has a concrete non-gate blocker, and no selected
     adversarial probe remains.
   - Initial discovery runs targeted adversarial evidence first. After any
     decisive targeted failure in the current pass, do not run the
     broad/aggregate gate merely for completeness. A distinct authorized
     diagnostic purpose may run it separately and is recorded as such; it never
     erases failed or unfinished rows.
   - A fresh correction discovery pass corroborates the corrected current
     bytes, reruns reviewer regressions, completes previously blocked or
     unchecked rows, reconciles authority and scope, and owns one justified
     aggregate after clean targeted evidence. A copied prior gate or prior
     pass is not current evidence.
   - If later evidence reveals an omitted material row, record the earlier
     aggregate gate as premature rather than final evidence. Run the missing
     targeted probe first; rerun the aggregate only while targeted evidence is
     clean and the gate remains justified.
   - For every gate record: the exact command or `not run`, owner, stage,
     reason, and current evidence. Add no gate and add no command.
   - Previously blocked/unchecked rows that remain unavailable retain concrete
     non-gate reasons and evidence owners; a corrected first target cannot close
     an unfinished sibling. Required conditional gate owners retain their duties;
     this discovery aggregate record waives none of their applicable proof.
7. Validate each candidate finding against surrounding code and observed
   behavior. Assign each confirmed finding a stable ID such as `F-01`. Include
   suggested severity, location, demonstrated trigger, consequence, evidence,
   affected AC, broken invariant, an explicit credible contract-implied sibling
   surface, and the smallest invariant-level corrective direction. Never leave
   the sibling surface implicit. Do not give a patch or a
   demonstrated-field-only special case. Keep unproved questions, residual
   risks, and unchecked ledger rows separate from confirmed findings.
8. Finish every ledger row. If work stops early, mark each remaining
   required/material row `blocked` or `unchecked` with the concrete reason and
   name the next evidence owner. Stopped discovery retains all remaining rows,
   findings, regressions, and continuation context; a partial report never
   presents omitted rows as clean.
9. Publish the output: coverage is complete or explicitly partial, every
   material row and confirmed finding is present, and the report applies only
   to the identified reviewed bytes and never claims its own authenticity. Hand
   the report to the separate acceptance decision call; discovery does not
   decide.

## Adversarial checks for stateful work

Apply the relevant checks, not a generic exhaustive matrix:

- Cross product selected/current entities with non-selected entities so a
  valid primary state cannot hide an invalid sibling state.
- When the invariant says exactly one owner/active/current item, test zero, one,
  and two distinct owners.
- Verify current/active attempt ordering against the latest attempt, not merely
  membership or existence.
- Compare the exact ready/eligible set with dependency state; "at least one
  ready" is insufficient when all eligible items must be represented.
- Check terminal states against every subordinate state so stopped/complete
  parents cannot retain running children.
- Reject type confusions such as booleans accepted as integers and strings
  accepted as collections when those values cross persistence or API boundaries.
- For tamper claims, modify related evidence coherently, including recomputed
  internal digests. A digest stored with mutable evidence proves consistency,
  not immutability; stronger claims need an independent anchor.

Choose these cases because they catch interacting invariant failures that
ordinary happy-path and one-field corruption tests routinely miss.

## Output contract

For guided discovery, default to a concise human-readable inline response:

```markdown
Discovery report: complete | partial — <reasons>

Findings:
- F-01 [suggested P1] <location, trigger, consequence, evidence, affected AC, broken invariant, explicit sibling surface, direction>

Coverage:
- <stable row ID: cases, setup/oracle, submitted evidence, independent probe, pass/fail/blocked/unchecked + reason>

Aggregate gate: <run/not run, exact command or not run, owner, stage, reason>

Questions / unchecked work: <separate summary>
Scope / residual risk: <summary>
Next: <separate acceptance decision call, or the owner of a concrete blocker>

Discovery continuation:
- Iteration / current byte identity: <value when available>
- Coverage rows: <all row IDs and results>
- Finding IDs: <all stable finding IDs or none>
- Finding/scenario continuity: <prior statuses, current producer-attributed evidence, incomplete reasons and separate correction/evidence/authority owners; influenced sibling surfaces>
- Preparation/context: <brief, verification revision, preflight and context references>
- Reviewer regressions: <paths and exact commands or none>
- Aggregate gate: <status, exact command/owner, reason>
- Next: <one exact route>
```

Say `No findings.` when evidence is clean and do not manufacture a defect. A
continuation block is required for partial coverage or any review with
blocked or unchecked rows; keep it compact and copyable. Preserve every
finding/scenario ID with its prior status, current producer-attributed
evidence, incomplete reason and separate correction/evidence/authority owner
through the handoff. Do not compress away a required field in guided output.

For durable discovery, read `references/discovery-report-template.md`, write
exactly one report, and include the full scope and command records. Write it to
the next unused numbered discovery path under the task package's `reviews/`
directory (`reviews/discovery-NN.md`). Record the exact reviewed status before
the write and the status afterward; only the new report entry may differ. Never
overwrite an earlier report or redirect the durable report to an external
runtime directory.

Give the acceptance decision call the task brief, current scoped diff, this
report, every blocked or unchecked row, reviewer regression paths/commands,
and the applicable packaged preparation references — the verification design
with its revision, the readiness/preflight reference, and the recorded
decision context — for complete, clean guided reports as well as explicitly
partial ones. An unpackaged direct edit hands off the supplied
conversational context instead.

## Boundaries

Do not decide acceptance, record approved deferrals, or advance work. Do not
implement fixes, edit reviewed production files or tests, update task
briefs/plans/trackers or prior reports, commit, launch subagents, or run
unauthorized slow, flaky, destructive, privileged, live, or networked probes.
The sole repository write is the authorized durable discovery report path above.
Reports never claim their own authenticity; a report applies only to the
identified reviewed bytes and does not review or authenticate itself.

## Definition of done

- Discovery provenance is explicit; an authoring session cannot publish
  independently corroborated rows and routes to a fresh discovery call.
- Scope is safely separated from user work, or the overlap is published as an
  explicit gap with a concrete owner.
- Every required/material ledger row is `pass`, `fail`, `blocked`, or
  `unchecked` with a reason, setup/oracle, and current evidence for the
  reviewed bytes; authority omissions stay visible behind green tests.
- Any required/material executable schema boundary has current validator
  evidence from both a valid instance and a deliberately invalid instance that
  targets the relevant constraint; otherwise its row remains blocked or
  unchecked.
- Relevant lifecycle and interacting-state risks receive adversarial evidence;
  process probes leave no surviving fixture processes.
- Independent findings are batched where safe; findings name the invariant and
  bounded sibling surface, carry stable IDs and suggested severities; clean
  work gets no invented finding.
- Aggregate-gate ownership, suppression after decisive failure, and the
  premature-gate recovery rule are visible with command or `not run`, owner,
  stage, reason, and current evidence; no gate or command was added.
- Coverage is complete or explicitly partial, the output hands a complete or
  explicitly partial evidence report to the separate acceptance decision call,
  and the report never claims its own authenticity.
