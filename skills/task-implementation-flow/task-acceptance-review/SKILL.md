---
name: task-acceptance-review
description: Decide whether one bounded implementation is safe to advance by admitting the current independent discovery evidence, submission claims, and applicable conditional evidence, then return ACCEPT, CHANGES_REQUESTED, or INCONCLUSIVE. Use after an independent discovery pass published its report, or with equivalent current evidence, especially when task metadata requires immediate review or behavior crosses stateful, public, security, concurrency, recovery, or migration boundaries. Default to a concise guided decision; require full packet/report reconstruction only for explicit high-assurance work.
---

# Task Acceptance Review

Decide whether one bounded implementation is safe to advance. Admit and
reconcile the current evidence published by the independent discovery pass
instead of recreating its probes or the implementer's process. Decide every
finding against current authority and reviewed bytes, and route exact evidence
gaps to their owners. Account for the task's explicit finite risks before
spending the decision budget on further review.

Repository and user instructions outrank this skill. Preserve pre-existing user
work. Ordinary acceptance is read-only except for an authorized canonical report
artifact in the task package.

## Establish reviewer provenance first

Independence is a property of session authorship, not of the skill text or role
currently loaded. Before reviewing evidence or issuing a verdict, determine
whether this session authored any production bytes in the reviewed diff.

- An independent session continues to the decision workflow below.
- A session that authored reviewed production bytes may perform a clearly
  labeled `SELF_CHECK_ONLY`, but it must not issue `ACCEPT`,
  `CHANGES_REQUESTED`, or `INCONCLUSIVE`. Loading this skill does not reset
  authorship. The route is always a fresh reviewer.
- `SELF_CHECK_ONLY` is a non-verdict conversational/report label, not an
  orchestrator status and never advances work.
- If an independent reviewer later writes an authorized tests-only reproducer,
  its pre-write verdict remains final for that session. Corrected production
  bytes require a new reviewer; the reproducer-writing session cannot accept
  them.

## Choose the profile

Use `guided` by default. Use `high-assurance` when explicitly requested or when
the decision is given a package-contained preflight packet, machine worker
result, run policy, and durable acceptance path from an orchestrated flow.

### Guided inputs

Require enough to identify:

- the authority: the user request, task brief, or acceptance criteria;
- the current task-owned diff or changed paths;
- the current submission: implementation and verification claims, the
  implementer's scenario-to-evidence map, and any unfinished or blocked rows;
- the current discovery evidence: the independent discovery report and its
  continuation block, or an equivalent complete or explicitly partial evidence
  publication;
- applicable conditional evidence: maintainability review, registry records,
  and any prior review continuation;
- repository instructions and permissions for the decision.

Do not return `INCONCLUSIVE` merely because no preflight packet, digest ledger,
worker JSON, or report path exists. Reconstruct the relevant scope from current
Git state and the task conversation/artifact when it is safely separable.
Packaging alone does not require high-assurance digests or machine results. A
guided evidence gap (for example, no independent discovery publication) does not
trigger an orchestrator-packet requirement; it routes to the discovery owner
with the exact missing evidence.

### High-assurance inputs

Require the exact packaged `brief.md`, its ready `preflight.md`, worker result,
recorded baseline, run policy, the current independent discovery report, and the
next unused `<task-package>/reviews/acceptance-NN.md` report path. A direct
legacy brief or an external/noncanonical preflight or report path is a contract
error; inconsistency, stale authority, or an inseparable baseline is
`INCONCLUSIVE`. Do not downgrade silently.

Treat implementer summaries and passing commands as submitted claims, not
independent proof in either profile.

## Decision workflow

1. Establish provenance, then read applicable instructions, the task contract,
   scoped diff, current submission, the independent discovery report (or its
   absence), applicable conditional evidence, and any prior review
   continuation. Confirm the outcome, allowed scope, profile, and current byte
   identity when available.
2. Reconstruct task ownership before deciding:
   - compare changed paths with stated scope and implementation claims;
   - separate pre-existing user work, task changes, and runtime artifacts;
   - treat unexplained or inseparable overlap as `INCONCLUSIVE`.
   In high-assurance mode, also compare every recorded Git, index/worktree,
   authority, policy, dependency, and environment identity.
3. Admit the discovery evidence. When no independent discovery publication
   exists, acceptance does not merge the roles: request the missing evidence
   from the discovery owner with the exact gap, keep the affected rows
   `blocked` or `unchecked`, and decide `INCONCLUSIVE` until it arrives.
   Acceptance neither performs the missing discovery itself nor treats an
   implementer summary, a green suite, or a report self-claim as the missing
   independent evidence.
4. Reconcile the admitted ledger and findings against current authority and
   reviewed bytes:
   - Compare every required/material ledger row with the authority, the
     submitted scenario-to-evidence map, and current bytes. A row marked
     passing without decisive current evidence stays `blocked` or `unchecked`
     with its exact missing proof and owner, despite green tests, static schema
     checks, or producer self-validation. Summaries, old passes, report
     self-claims, and green tests do not substitute for decisive evidence.
   - Preserve every stable row identity and finding ID from the discovery
     report and any prior continuation. A prior `pass` guides the decision and
     is not current evidence for changed bytes.
   - Check stale-sensitive claims against separate identities: matching
     worktree bytes or short-status text do not prove a matching index blob,
     and an old pass does not prove changed bytes. Missing indispensable
     capability or an unexplained index state yields `INCONCLUSIVE` and routes
     to fresh `task-preflight` or the prerequisite owner; acceptance neither
     invents helpers nor absorbs or resets user work. Affected obsolete
     readiness or verification-revision evidence routes to focused preflight
     and current evidence ownership; acceptance does not revise requirements or
     scenarios.
   - Explicit AC violations block even when submitted tests are green or the
     violation is absent from the submitted scenarios. They yield
     `CHANGES_REQUESTED` with authorized bounded correction, preserving the
     exact finding/row IDs and correction ownership.
   - Consume the applicable conditional evidence (maintainability review,
     registry records). A consistent record is an input to the decision; a
     missing applicable record or a demonstrated contract mismatch receives a
     focused request to its owning stage and remains actionable — an earlier
     conditional pass cannot erase a demonstrated mismatch. Acceptance retains
     authority to identify a demonstrated contract mismatch; it does not
     become a second general maintainability reviewer and does not run broad
     archaeology.
5. Consume the discovery-owned aggregate-gate record without executing it.
   Record the exact command or `not run`, owner/stage, reason, and current
   evidence as consumed fields in the decision. Suppression after a decisive
   targeted failure is retained; a copied pre-correction pass cannot replace a
   clean corrected discovery record; a premature gate does not clear an omitted
   row. Focused missing proof returns to discovery; after clean targeted
   evidence, only discovery owns a still-justified rerun, and a failing omitted
   row keeps the ordinary aggregate suppressed. Acceptance adds no gate and
   adds no command. Missing required proof cannot support `ACCEPT`.
6. Verify decisive boundary obligations through the admitted evidence. When a
   required/material row depends on a machine-readable schema or other
   executable validator contract, the admitted discovery evidence must include
   independent validator results from at least one instance that should be
   valid and one deliberately invalid instance that targets the changed or
   acceptance-relevant constraint; schema text, producer-side validation,
   deserialization, or an unrelated passing suite is not proof. If decisive
   validator evidence is missing, keep that ledger row `blocked` or `unchecked`
   with the concrete reason; it cannot support `ACCEPT`. Request the exact
   missing valid/invalid evidence from the discovery owner. Acceptance does not
   routinely rerun public probes, broad searches, or suites to repair the
   report within the decision call.
7. Finish every admitted row. If work stops early, mark each remaining
   required/material row `blocked` or `unchecked` with the concrete reason.
   `CHANGES_REQUESTED` never means unreported areas are clean. Every stable
   finding/row remains visible with its current result and evidence, or its
   incomplete reason and owner, separate from questions and residual risk.
   Full contextual and mixed-condition judgment rules arrive with a later
   stage; this skill establishes admission, reconciliation, and ledger/finding
   preservation.
8. Decide one verdict under the rules below, using exactly
   `ACCEPT`, `CHANGES_REQUESTED`, or `INCONCLUSIVE` when independent, or
   `SELF_CHECK_ONLY` when provenance requires it. State the broad-gate
   admission record and one exact next route. Write a durable report only when
   requested or required by high-assurance mode.
9. Reconcile the final output before returning. Confirm that every finding has
   its stable ID and required fields, the continuation names every finding ID
   and reviewer regression separately, all admitted rows are present, and the
   consumed aggregate-gate record matches the discovery report's command
   order. Do not compress away a required field in guided output.

## Verdict and routing rules

An independent reviewer uses exactly one verdict:

- `ACCEPT`: all required ACs and justified gates are independently satisfied by
  admitted current evidence, scope is clean, and no blocking finding, question,
  or unverified required boundary remains.
- `CHANGES_REQUESTED`: a concrete in-scope production or test defect can be
  corrected without changing authority, scope, dependencies, permissions, or
  required infrastructure.
- `INCONCLUSIVE`: ambiguous authority, inseparable scope, missing decisive
  capability, stale high-assurance inputs, missing or contradictory discovery
  evidence, environment/permission failure, or an unverified required boundary
  prevents a truthful decision.

`SELF_CHECK_ONLY` sits outside these verdicts. Use it only when the current
session authored reviewed production bytes; do not mislabel missing
independence as `INCONCLUSIVE` or a clean acceptance.

Missing discovery routes to the discovery owner with the exact gap; acceptance
does not silently do both roles in one call. Missing/contradictory focused
proof is requested from the owning stage; it is not a generic user question.

Route `CHANGES_REQUESTED` to the same implementation thread when possible.
After any correction, run fresh discovery evidence and a fresh acceptance
decision against the corrected bytes; never reuse or append acceptance to the
prior verdict as if it still applied.

Route contract defects to the user or `task-brief-designer`; current-state or
high-assurance freshness failures to `task-preflight`; and wider scope/shared
infrastructure back through brief design. Only an `ACCEPT` verdict may advance
an orchestrated task.

## Output contract

For guided decision, default to a concise human-readable response:

```markdown
Verdict: ACCEPT | CHANGES_REQUESTED | INCONCLUSIVE
or
SELF_CHECK_ONLY — not an independent verdict

Findings:
- F-01 [P1] <location, trigger, consequence, evidence, affected AC, broken invariant, explicit sibling surface, direction>

Admitted discovery: <report/continuation path or absence, coverage completeness>
Coverage:
- <stable row ID: cases, submitted evidence, admitted discovery evidence, reconciled pass/fail/blocked/unchecked + reason>

Aggregate gate (consumed): <command or not run, owner/stage, reason, current evidence>
Questions / unchecked work: <separate summary>
Scope / residual risk: <summary>
Next: <one exact route>

Review continuation:
- Iteration / current byte identity: <value when available>
- Coverage rows: <all row IDs and results>
- Finding IDs: <all stable finding IDs or none>
- Reviewer regressions: <paths and exact commands or none>
- Aggregate gate (consumed): <status and reason>
- Next: <exact route>
```

Say `No findings.` when evidence is clean. Do not create a report file unless
the user requested one. A continuation block is required for
`CHANGES_REQUESTED`, `INCONCLUSIVE`, `SELF_CHECK_ONLY`, or any decision with
blocked/unchecked rows; keep it compact and copyable.

For high-assurance decision, read
`references/acceptance-report-template.md`, write exactly one report, and
include the full baseline/freshness, admission, and consumed command records.
The report is the only intentional write during the verdict phase; the
separately authorized post-verdict tests-only protocol is the sole later
exception.

Write that report to the next unused numbered acceptance path under the task
package's `reviews/` directory. Record the exact reviewed status before the
write and the status afterward; only the new report entry may differ. Never
overwrite an earlier review or redirect the durable report to an external
runtime directory. Even `ACCEPT` records a decision/route without authorizing
tracker mutation or performing advancement.

Give a fresh reviewer the task brief, current scoped diff, preceding verdict and
continuation block, reviewer regression paths/commands, and every
blocked/unchecked row. Do not invent a new machine schema before an orchestrator
owns it. Only an independent `ACCEPT` advances work.

## Conditional post-verdict tests-only reproducer

`tests_only_reproducer` is an optional mode of this same review session, not a
production-writing role. It is available only after all of these are true:

1. the independent verdict is fixed and already reported as
   `CHANGES_REQUESTED`;
2. the current user or exact review invocation explicitly authorizes
   `tests_only_reproducer`; and
3. that authorization names the exact writable owning test file or bounded test
   area.

Task scope, an allowed test path, or `review: immediate` is not write
permission. If any precondition is absent, remain read-only and do not load the
procedure. When all are satisfied, read
`references/tests-only-reproducer.md` and follow it without loading
`bounded-task-implementer`. The verdict stays `CHANGES_REQUESTED`; production
repair and same-session acceptance remain prohibited.

When this mode runs, keep the authorization source, exact allowed path, exact
pre-write status, exact post-write status, and diff side effects as distinct
reported fields. The final audit must compare those records rather than merely
state that scope was preserved.

## Boundaries

Do not implement fixes, edit reviewed files, update task briefs/plans/trackers,
advance orchestration, commit, launch subagents, or run unauthorized slow,
flaky, destructive, privileged, live, or networked probes. Do not routinely
rerun discovery's public probes, broad searches, or aggregate suites. The sole
repository write exception is the explicit post-verdict tests-only protocol
above.

## Definition of done

- Reviewer provenance is explicit; an authoring session cannot issue an
  independent verdict.
- Scope is safely separated from user work.
- Current discovery evidence is admitted; missing discovery routes to its
  owner rather than merging the roles.
- Every required/material ledger row is `pass`, `fail`, `blocked`, or
  `unchecked` with a reason, reconciled against current authority and reviewed
  bytes; summaries, old passes, report self-claims, and green tests do not
  substitute for decisive evidence.
- Any required/material executable schema boundary has admitted validator
  evidence from both a valid instance and a deliberately invalid instance that
  targets the relevant constraint; otherwise its row remains blocked/unchecked
  and cannot support `ACCEPT`.
- The consumed aggregate-gate record names the command or `not run`, owner,
  stage, reason, and current evidence, without re-executing the gate.
- Every stable finding and unfinished row survives the decision with its
  result or incomplete reason and owner.
- Exactly one justified verdict or `SELF_CHECK_ONLY`, residual-risk statement,
  continuation when required, and next route are present.


<!-- contract-registry-flow:task-acceptance-review:begin -->
## Contract and discovery-reference acceptance

For contract-bearing tasks, independently reconstruct contract impact. Do not trust either the implementer handoff or the registry-updater handoff as proof.

Reconcile four layers:

```text
EXPECTED
  task brief / relevant stable plan IDs
      <->
ACTUAL
  implementation + behavior
      <->
DECLARED
  OpenAPI / schemas / public types / package exports / CLI/config / migrations as applicable
      <->
DISCOVERABLE
  docs/contracts + required local/routing references
```

Check, as applicable:

1. the implementation really added/changed/removed the claimed durable surface;
2. existing executable/declarative authorities were updated by implementation;
3. the owning subsystem contract record represents current implemented semantics;
4. `docs/contracts/index.json` is current and the canonical validator passes;
5. materialized stable plan IDs map to the correct current contract without semantic drift;
6. an affected module README was updated if its existing explanation became stale;
7. root/scoped `AGENTS.md` / `CLAUDE.md`, root README, or project/architecture map were updated only when claims they already make became stale.

Missing, stale, contradictory, or aspirational current-state discovery that affects later task routing is `CHANGES_REQUESTED`, not merely residual risk.

Route failures narrowly:

- production/test/executable-contract defect -> `bounded-task-implementer`;
- registry/module/reference-only defect -> `task-contract-registry-updater`;
- planned/current semantic mismatch -> appropriate task/project planning owner;
- missing or unclear registry foundation -> `repo-foundation`.

After a reference-only correction, run fresh acceptance. Do not require a maintainability rerun when production, test, and executable-contract bytes are unchanged.
<!-- contract-registry-flow:task-acceptance-review:end -->
