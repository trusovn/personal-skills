# Verification and review policy change proposal

Date: 2026-10-08

Status: proposal for discussion, not an operating instruction or executable task brief.

Purpose: make the generic task implementation flow converge before continuing
code-guided orchestration work. No existing skill or plan is changed by this
document.

Sources:

- [Integration spike issues](../../task-orchestrator/docs/integration-spike-2026-10-08/issues.md)
- [Code-guided orchestration brief](../../task-orchestrator/docs/code-guided-orchestration.brief.md)
- [Current flow](../README.md)
- The seven source skills, their report/packet references, existing eval cases,
  and the canonical development-profile installer.

Evidence limit: source and preserved issue-report inspection. This proposal
does not claim a new behavioral reproduction or a successful agent eval.

## Recommendation and decisions

Require separate verification design and preflight for executable task packages
that enter this flow, including manually coordinated packages outside an
orchestrator. Keep small direct edits on the lightweight guided path. Required
stages may produce compact artifacts; they do not imply the full high-assurance
freshness chain. This boundary is a recommendation for discussion.

Make verification scenarios binding evidence obligations under the original
brief. Keep the brief and its cited authority normative. Freeze the scenario
set at ready preflight, then require an explicit reason and recorded revision
for changes. A verification design must not silently add product requirements.

Separate contract verification from disposition of additional findings. Passing
tests alone cannot prove that their assertions, setup, and observation boundary
actually establish the ACs.

Confirmed user decision: demonstrated explicit AC failures block acceptance;
additional non-critical findings may be recorded as known issues. A missing
scenario cannot excuse an AC failure. A change to an AC requires the proper
authority owner and must not be disguised as a passed AC.

Still proposed: the mandatory-stage boundary and automatic correction limit.

Proposed loop limit: at most two automatic correction rounds for a task across
the applicable review stages, followed by a decision stop. This is a proposed
default, not an existing limit. Exhausting it never grants acceptance. Separate
environment/transport retries from correction rounds.

## Generic spike issues to fix first

| Issue | Generic reason | Bounded change and proof |
|---|---|---|
| FLOW-02 | A human following the implementer handoff can skip maintainability or registry synchronization. | Stop implementation at submission; name the first applicable outstanding stage and remaining obligations. Verify immediate-review routes with neither, either, and both conditional stages, including corrections. |
| SETUP-01 | New Git repositories need the development profile before their first implementation commit. | Support an explicit unborn-HEAD state in installation availability and affected identity handling. Test installation in a real unborn temporary repository and preservation of unmanaged files. Do not claim full collector lifecycle support unless exercised. |
| SETUP-02 | A local run can use stale installed instructions while a maintainer thinks it uses current source. | Add an explicit read-only profile qualification/check operation covering managed skills, references, profile guide, and helpers. Reuse the existing installer for explicit refresh. Test deliberate drift, refresh, and unchanged unmanaged files. Never auto-refresh an active session/run. |

The policy work also needs the human-facing portion of FLOW-05: finding IDs,
correction owner/reason, affected surface, and complete continuation evidence.
It needs the generic evidence lesson from LIVE-01: exact reproducible probes,
available evidence references, and explicit applicable validator cases.
Neither partial change resolves the full machine-contract issue.

Leave FLOW-01, FLOW-03, FLOW-04, FLOW-06, machine enforcement of FLOW-05/LIVE-01,
and TELEMETRY-01 with the orchestration integration work. They remain required
where the proposed executor depends on them. In particular, profile checking
does not supply retained runnable versions for active runs.

## Verification gate

Each required scenario carries a stable ID, AC/authority mapping, starting
state, action, expected result, decisive observation boundary, material
variants, and the credible wrong behavior it distinguishes. Include required
negative, unchanged-state, lifecycle, and finite cases. Use inspection evidence
where it is decisive for a documentation task; do not force executable tests
for every kind of change.

Preflight checks both directions: every AC is covered, and every required
scenario is justified by authority. It also checks fixture/setup feasibility,
commands, permissions, boundary capability, required repository gates, and
known-issue compatibility with this task. A not-yet-written test is normal;
a missing indispensable verification capability is a blocker. Preflight does
not claim the unimplemented behavior passed.

The implementer maps scenario IDs to concrete tests/probes and current results.
The proposed discovery reviewer independently checks the meaning and evidence
of each scenario, rather than merely counting passing tests. The acceptance
decision checks that this evidence establishes the required obligations.
Missing required evidence remains blocked/unchecked and cannot support
acceptance.

A new review finding does not silently expand the frozen gate. Classify it as:

1. a demonstrated violation of existing authority, including an AC omitted by
   verification design: block, report the coverage gap, and make a narrow
   scenario correction under the same authority;
2. an additional confirmed defect: apply the advancement policy below; or
3. an unproved concern or suggested improvement: report separately, without
   presenting it as a confirmed defect or a new requirement.

Changed requirements return to the brief/decision owner. Changed scenarios
return through verification design and focused preflight. Ordinary production
corrections do not restart task design when authority and verification remain
valid.

Cross-task testing stays with an explicit integration task when needed. The
verification designer may capture this task's declared output obligations to
later consumers without taking ownership of sibling implementation.

## Readiness ownership and implementer entry check

Move the implementer's task-readiness assessment to required task-preflight
for work on this path. Preflight owns prerequisite and dependency readiness,
scope/ownership assessment, verification capabilities, commands, permissions,
and the decision that implementation may start. Remove the duplicate semantic
self-preflight and missing-AC derivation on this path; missing ACs return to
task design.

Keep a small entry check in the implementer. It confirms that ready preflight
applies to this task, authority, scope, and verification revision, and that
relevant ownership, permissions, and recorded capability facts remain valid.
High-assurance work retains exact recorded-identity checks. This check does not
rerun readiness discovery, baseline suites, or scenario design. A stale approval
returns to preflight; a newly discovered authority gap returns to its owner.

The entry check must distinguish expected implementation/report effects from
unexplained changes. A correction does not repeat full preflight solely because
the implementation changed; changed prerequisites, authority, ownership, or
required capability require a focused new readiness decision. The optional
small-direct-edit path still needs a compact safety check if it remains outside
the required-preflight flow.

## Separate discovery from the acceptance decision

Recommend splitting the current acceptance skill into task-review-discovery
(working name) and task-acceptance-review, invoked separately. The user clarified
that the primary goals are role focus and independent reasoning-effort settings
for the calls. The split is proposed design, not a completed source change.

Neither role may issue independent review evidence/verdicts for production bytes
authored in its own session. Separate calls add a launch and evidence handoff;
keep the handoff compact and reuse evidence references instead of copying logs.

The discovery skill owns independent execution/corroboration of the agreed
verification gate, bounded behavioral investigation, and a complete evidence
ledger. It reports all confirmed findings from the bounded pass, plus separate
questions and unchecked rows. Each finding states authority/AC relation,
trigger, consequence, evidence, affected surface, and credible sibling cases.
Suggested severity is input to judgment, not a final advancement decision.
Discovery reports complete or partial coverage; it does not issue ACCEPT or
CHANGES_REQUESTED, approve deferral, launch correction, or advance a task.

The acceptance skill owns evidence admission and go/no-go judgment. It consumes
the brief, verification revision, current reviewed-byte identity, discovery
ledger/findings, applicable architecture/maintainability and registry evidence,
relevant downstream contracts, and known issues. It classifies every finding as
blocking, deferred-known, or an observation, with reasons. It applies the
confirmed AC-failure rule and existing verdict vocabulary. Missing evidence or
a concrete unresolved classification question cannot become acceptance by
default.

Acceptance must not start a second broad bug search or repeat the complete test
suite routinely. It may request or perform a focused, authorized clarification
needed to decide a specific claim. If essential evidence is missing, return an
explicit evidence request to discovery; that is not yet an implementation fix
request. Newly demonstrated blockers cannot be ignored to preserve the split.
The decision stage remains accountable for detecting a ledger that contradicts
the brief or relies on inadequate evidence.

Batch evidence clarification requests and bound those retries within the task's
authorized budget. They must not create an unlimited discovery-to-decision
ping-pong loop merely because no production correction occurred.

Assign launch reasoning effort separately by role and task risk. Discovery
effort serves adversarial coverage and evidence quality; decision effort serves
impact, likelihood, authority, and downstream compatibility. A clean complete
report may allow a short decision call, while disputed findings may need more
reasoning. Do not assume either role is always cheaper. Carry role-specific
launch guidance separately from the brief's existing scalar implementation
metadata; distinguish intended settings from observed runtime settings.

Correction re-enters applicable architecture/maintainability and registry stages,
then discovery in correction mode, then acceptance. Correction-mode discovery
uses current required evidence, regressions, unfinished rows, and affected
surfaces. Neither old discovery evidence nor an old acceptance verdict applies
automatically to changed bytes.

Proposed route:

```text
brief -> verification design -> preflight -> implementation
  -> applicable architecture/maintainability -> applicable registry sync
  -> review discovery -> acceptance decision -> authorized advancement
```

The split alone does not guarantee convergence. It depends on fixed coverage,
batched discovery, a shared disposition policy, and explicit retry limits. The
future controller executes admitted decisions under its authority; it does not
replace AI risk judgment with an unvalidated severity label.

## Acceptance and known issues

Keep the existing verdicts. An independent ACCEPT may carry non-blocking known
issues; a new ACCEPT_WITH_ISSUES status is unnecessary.

| Condition | Disposition |
|---|---|
| Demonstrated required AC/scenario failure, broken required gate, or unauthorized effects | Block. Use CHANGES_REQUESTED when bounded correction is authorized; otherwise route the authority/ownership problem. |
| Missing decisive required evidence, ambiguous authority, or stale inseparable inputs | INCONCLUSIVE; route to the owner rather than inventing proof. |
| Additional defect that breaks a required downstream contract, a hard architecture rule, or creates critical behavioral risk | Block and identify the contract, architecture rule, or credible trigger and consequence. |
| Additional confirmed defect with bounded non-critical impact, no required architecture breach, and no incompatible downstream obligation | ACCEPT with a recorded known issue when all required evidence passes. |
| Unproved concern, optional enhancement, or unsupported design preference | Separate observation; no automatic correction. |

Assess impact and likelihood separately using evidence and plausible operating
conditions. Do not use a low estimated probability to erase catastrophic data,
security, or irreversible-state consequences. Severity labels alone do not
decide advancement.

For downstream impact, cite the affected output/consumer contract or relevant
planned task IDs. A concrete unresolved compatibility concern prevents automatic
deferral; absence of proof of every hypothetical future use does not. Known
issues must not impose an undeclared workaround on the next task.

Maintain a separate project known-issues list, with task reviews as provenance.
Proposed default: docs/known-issues.md, subject to repository authority. Each
entry has a stable project ID, source task/review/finding, trigger, consequence,
evidence, impact and likelihood rationale, affected boundary/tasks, deferral
basis, follow-up owner/action, and conditions that require reassessment.

Acceptance may write authorized task review evidence. The human coordinator or
later controller records accepted deferrals in the project list before advancing;
the reviewer does not gain general tracker-writing authority. Preflight consumes
relevant entries. Reassess when the affected contract, usage, or dependency
changes, and at an applicable integration review; do not reopen every entry
for every unrelated task.

## Prevent repeated discovery rounds

Freeze required coverage before implementation. In the first review, complete
the bounded, safe, affordable discovery pass even after independent failures;
batch findings and explicitly retain blocked/unchecked rows. Suppress an
aggregate gate after decisive failure unless it has a distinct purpose.

Remove maintainability's cap of three reported blockers and its instruction to
stop after enough decisive blockers. Limit discovery scope and budget instead.
Group findings by invariant where useful, but report all confirmed blockers
found in that pass. Do not imply unreviewed areas are clean.

Fresh correction review checks current required evidence, known regressions,
previously blocked rows, and changed/influenced surfaces. It should not restart
an unrestricted search for unrelated improvements. A newly discovered blocker
must state why it was not previously resolved: correction regression, earlier
blocked evidence, missed existing obligation, changed authority, or newly
demonstrated critical risk. This explanation cannot suppress a real blocker.

Production corrections still invalidate applicable semantic verdicts. Retain
independent fresh review and required architecture gates. Reference-only
corrections retain the existing narrow updater-to-acceptance route when actual
effects support it.

At the correction limit, report unresolved blockers, coverage gaps, attempts,
and the smallest proposed decision. Dependent tasks remain unavailable.
Unrelated tasks may proceed only when their authority and shared state permit
it; a loop limit is not a dependency waiver.

## Ordered implementation plan

1. **Agree the policy.** Preserve the confirmed AC-failure rule; resolve
   mandatory-stage scope and the correction limit. Define the advancement
   rubric before changing skill text.
   Verification: walk through a passing task with a minor issue, an omitted AC
   failure, a downstream blocker, and a correction regression.
2. **Make verification and preflight binding.** Update the flow README,
   task-brief-designer and its template/layout, task-verification-designer,
   task-preflight and packet template, and bounded-task-implementer. Add source
   identity/revision and complete scenario evidence mapping without duplicating
   requirements. Move readiness assessment to preflight and retain only the
   implementer's entry validity check. Verification: AC omission, unjustified
   scenario, weak oracle, missing fixture, valid future test implementation,
   stale design/approval, expected correction effects, and minimal
   documentation-task cases.
3. **Split review and implement disposition/convergence.** Add the discovery
   skill and evidence contract; narrow acceptance to evidence admission and
   disposition. Update report templates, maintainability review, implementer
   correction/handoff, registry routing where needed, and the flow README.
   Define separate role-specific reasoning guidance, the known-issues artifact,
   and narrow writing ownership. Resolve FLOW-02 across human and
   machine-contracted handoffs. Verification: AC failure with green tests,
   minor additional issue accepted, architecture/downstream/critical blockers,
   incomplete discovery returned for evidence, no broad rediscovery in decision,
   more than three independently observable maintainability blockers, complete
   correction continuation, and loop-limit stop without acceptance.
4. **Repair and qualify distribution.** Fix SETUP-01 and SETUP-02 with focused
   installer/identity tests. Synchronize scripts/install_development_skills.py,
   DEVELOPMENT_SKILL_SOURCES, PROFILE_SKILLS_README, SHARED_SCRIPT_FILES,
   tests/test_install_development_skills.py, skills/README.md, and root README
   wherever affected, including installation of the new discovery skill and
   its references. Keep the installer's existing ownership boundary.
5. **Qualify the changed flow before orchestration implementation.** Use local
   disposable setup and narrow deterministic tests first. Then run separately
   authorized behavior evals for preparation, review disposition, correction,
   and next-task known-issue consumption using qualified installed copies.
   Add a new results document beside existing plans; do not rewrite them.

Syntax, schema, link, and wording checks prove structural properties only.
Behavior evals must supply the task, implementations, fixtures, and evidence
needed to exercise each claimed outcome. Existing acceptance continuation and
public-boundary cases should remain, with expectations updated only for the
agreed policy. Live/model-budget checks require separate authorization.

Resume orchestration design after generic policy behavior is qualified and its
remaining machine integration requirements are explicit. The existing brief's
optional-verification assumptions will need a separate recorded policy delta.
Completing this proposal does not complete retained-version, transition,
evidence-admission, or telemetry requirements for the executor.
