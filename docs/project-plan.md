# Make development understandable to the project owner

Status: `READY_FOR_PLAN_VERIFICATION` — proposed implementation plan, not independently verified.
Plan version: 2026-10-21.

## What we will change

You should be able to open a plan or the latest work report and understand what
is being built, why the current work matters, what has been demonstrated, and
what needs your decision. Detailed records remain available through links.

Today, project direction explains the goal, but later documents often lead
with internal workflow details. A task can have an accurate technical report
without giving you an understandable account of the result.

For example, instead of opening with “D-05 / task accepted,” a report should
say: “Plans now begin with a plain-language explanation of the intended result.
We tried it on a small project and an interrupted task. You still need to judge
whether the explanation is clear enough.” It must link the supporting results
and must not claim those trials happened until they actually did.

### Delivery sequence

1. **Try one understandable example.** Use this documentation change to show
   the proposed plan opening, task explanation, and work report. Ask you what
   remains unclear before applying the format more widely.
2. **Connect plans and tasks to the goal.** Improve existing planning guidance
   and templates, reusing the task brief's existing direction explanation.
3. **Make work reports explain the result.** Add a short opening to existing
   implementation and acceptance records, preserving their different roles.
4. **Check the complete experience.** Try the changed guidance on supplied
   examples, check accuracy against the evidence, and let you assess clarity.

The first useful result is the example in step 1. We can stop or revise there
without rewriting the rest of the workflow. This plan does not claim that any
of these changes have been implemented.

### What each step gives you

1. **An example you can judge before we change the workflow.** You can read a
   sample explanation of this documentation work and say what is clear or
   missing. We use your feedback before changing the other documents.
2. **A plan that explains what the work will give you.** You can see the
   intended result and read a short description of each task in everyday
   language. You can understand why a task matters and what it enables without
   opening its technical instructions.
3. **A report that makes progress understandable.** After work finishes or
   stops, you can tell what changed, what was checked, what remains uncertain,
   and who needs to act next. You can follow links when you want the evidence.
4. **Confidence that the explanation is useful and accurate.** You can try
   the resulting documents on concrete examples. We check their claims against
   the actual records, and you judge whether they help you understand the work.

These describe the same four tasks in the delivery sequence. Their detailed
scope and checks are in [Implementation tasks](#5-implementation-tasks).

## 1. Authority, priorities, and scope

**Confirmed direction:** the owner finds it hard to understand what is being
developed. Agent-oriented documentation is insufficient. The owner approved
planning an understandable project overview connected to authoritative sources.
This conversation is the direction authority; another direction document is
not required for this maintenance change.

Priority order: understandable purpose and result; factual accuracy and visible
uncertainty; preserved execution/review safeguards; less duplicated prose.
If brevity would hide a limitation or decision, retain the limitation or
decision and move supporting technical detail behind a link.

Sources:

- [Documentation candidates](future-work/concepts/03-documentation-and-task-planning.md):
  a narrow D-01 ownership pass and the human-facing part of D-05. This plan
  proposes that bounded selection; it does not authorize the whole family.
- [Portfolio](future-work/FEATURE-MAP.md): source ownership and experiment gates.
- [Direction skill](../skills/project-direction/SKILL.md) and its existing
  [template](../skills/project-direction/references/direction-template.md).
- [Planning template](../skills/project-delivery-plan/references/project-plan-template.md),
  [brief template](../skills/task-implementation-flow/task-brief-designer/references/task-brief-template.md),
  and [acceptance template](../skills/task-implementation-flow/task-acceptance-review/references/acceptance-report-template.md).
- Repository `AGENTS.md`, [test guidance](../tests/README.md), and the canonical
  [installer](../scripts/install_development_skills.py).

In scope: source guidance, existing templates, navigation in existing guides,
focused evaluation inputs and checks, and disposable installation qualification.
The task map is [task-map.json](task-map.json); it indexes work and dependencies,
not runtime status. This plan owns cross-task meaning; the map references it.

Non-goals: dashboards, status collectors, a new skill or required workflow
stage, a new mandatory overview file for every project, automatic summaries,
general document compression, plan/JSON schema redesign, historical document
rewrites, or weaker independent review. Existing D-02 experiments remain the
gate for broader D-03/D-04 simplification.

Assumption: Markdown in existing documents is sufficient for the first useful
result. The proposed format and four-task sequence are implementation
recommendations. The owner clarity checkpoint remains an actual open decision,
not presumed approval from this planning request.

## 2. The reading experience and information ownership

### What the opening must explain

Use natural prose, a small list, or a table as appropriate. These are questions
to answer, not five mandatory headings on every document:

- What are we building, for whom, and what problem does it solve?
- What concrete situation will improve when it works?
- How does this task or result contribute, and why is it being done now?
- What is planned, reported as done, independently supported, or still unknown?
- What happens next, who acts, and does the owner need to decide anything?

A planning document can say that behavior has not yet been demonstrated and
link to the current report for progress. A task with no immediate visible
effect must explain which useful later outcome it enables. Do not invent an
end-user feature for internal maintenance.

| Information | Authoritative writer | Where the owner reads it |
|---|---|---|
| Purpose, priorities, boundaries | Owner-confirmed direction or direct request | Plan opening, linked to that authority |
| Intended system result and sequence | Project planner | Existing project plan |
| Task's contribution and scope | Task designer | Existing brief's outcome/direction trace |
| Changes and checks actually performed | Implementer | Existing result record's opening; explicitly reported claims |
| Independent findings | Discovery reviewer | Existing discovery record, referenced by acceptance |
| What may advance and unresolved limitations | Acceptance reviewer | Existing acceptance record's opening and detailed verdict |
| Current navigation | Existing guide maintained by the coordinator | Links to plan and current report; no duplicate status ledger |

Normal use: read purpose in the plan, follow the task's contribution, then read
the current report's result and next action. After interruption: open the latest
identified report, see the last checked scope and remaining gaps, then follow
the authoritative evidence. If sources disagree or are stale: show the conflict,
identify who resolves it, and do not present a current success claim.

## 3. Shared artifacts, boundaries, and safeguards

| ID | Artifact | Producer / owner | Consumer and lifecycle |
|---|---|---|---|
| ART-001 | Existing direction, briefs, source records and reviewed identities | Existing owning roles | All tasks read; newer observations do not rewrite historical decisions |
| ART-002 | Pilot example and compact ownership decisions | T-001 | Owner and T-002/T-003; proposed until owner clarity checkpoint passes |
| ART-003 | Updated planning/brief guidance and examples | T-002 | Planners/task designers; source changes require later installed qualification |
| ART-004 | Updated reporting guidance and navigation | T-003 | Implementer/reviewers/owner; summaries remain attached to their own report scope |
| ART-005 | Qualification evidence and owner feedback | T-004 | Owner and independent reviewers; identifies exact candidate and unrun gaps |

ART-002 and ART-005 use the relevant task's normal result/evidence records,
not new permanent project-wide artifact types.

| ID | Interface | Producer → consumer | Contract |
|---|---|---|---|
| IF-001 | Authority → plain-language explanation | Planner/designer → owner | ART-001 becomes ART-002/003; preserve meaning and distinguish proposals from decisions; flag conflicts |
| IF-002 | Evidence → result explanation | Implementer/acceptance reviewer → owner | ART-001 becomes ART-004; distinguish reported checks from independent disposition; missing/stale evidence remains visible |
| IF-003 | Candidate source → disposable installation | Source maintainer → fresh consuming session | ART-003/004 become ART-005 through the canonical installer; qualify copied bytes without refreshing this active session |

| ID | Invariant | Proof owner |
|---|---|---|
| INV-001 | An owner can understand the opening without decoding IDs or reading technical appendices | T-001 example feedback; T-004 final owner check |
| INV-002 | Summaries preserve authority, source identity, limitations, and planned/reported/independently supported distinctions | T-002/T-003 guidance; T-004 contrast cases |
| INV-003 | Existing mandatory preparation, discovery, acceptance, and correction duties remain intact; accepted plan bytes are not used as a mutable progress tracker | T-002/T-003 regression checks; T-004 independent evidence |
| INV-004 | No duplicate required overview, status ledger, or independent narrative of the same contract is introduced | All tasks; guide and output review |
| INV-005 | Qualification identifies its source/installed version and never refreshes the active installation mid-run | T-004 disposable install and evidence |

Explanations inherit their source scope and age. An old acceptance opening is
historical after relevant bytes change; it cannot certify the new version.
The next report records new observations and points to prior evidence where
still applicable. If a latest report cannot be established, navigation says so.

## 4. Flows and capability coverage

| Flow | Trigger and steps | Observable outcome | Capability |
|---|---|---|---|
| FLOW-001 | Owner asks what is being built → planner reads ART-001 through IF-001 → task contribution links to purpose → owner reads example and later revised plan/brief | Owner explains intended result, current contribution, and next useful proof | CAP-001: understand intent |
| FLOW-002 | Work completes or is interrupted → implementer reports scoped observations → independent discovery supplies findings → separate acceptance explains disposition through IF-002 → coordinator links the current record | Owner sees supported result, remaining gap, and next actor/decision | CAP-002: understand progress |
| FLOW-003 | Candidate guidance ready → maintainer installs into disposable target through IF-003 → fresh consumers produce outputs from supplied inputs → evidence compared with sources → owner assesses clarity | Qualified candidate or explicit correction route with gaps retained | CAP-003: establish usefulness |

Failure branches: missing direction produces an explicit unknown and required
decision, not invented purpose; stale/conflicting evidence prevents a current
success claim; unclear owner explanation returns to T-001 or its producing
task; missing installed capability leaves qualification incomplete. Corrections
follow existing affected-stage review rules. No automatic acceptance follows
from document existence, schema success, or owner readability approval.

## 5. Implementation tasks

### T-001 — Try an example the owner can understand

Consumes ART-001; produces ART-002. No predecessor. Advances FLOW-001/002.

Use this change as the pilot topic. Show the intended plan opening, task
contribution, and result opening in its normal task evidence. Any illustrative
completion text is explicitly hypothetical. Record the minimal ownership table
and which existing sections it replaces or reuses. Compare with the current
templates rather than creating a universal writing standard.

**Acceptance:** the owner can explain purpose, practical change, current work,
known versus unknown progress, and next decision using the example. Record
specific feedback; unresolved confusion blocks wider template adoption.
Fresh readers can provide supporting evidence but cannot substitute for the owner.

### T-002 — Make planning explain purpose and task contribution

Consumes ART-001/002; produces ART-003. Depends on T-001's clarity checkpoint.
Advances FLOW-001 and IF-001; preserves INV-001–004.

Update the project-delivery-plan source guidance and template, and the
task-brief-designer guidance/template only where needed. Reuse the existing
direction trace. Inspect project-direction and project-plan-verification for
compatibility; change them only for a concrete required producer/consumer gap.
Keep agent detail below the opening. Plans link to current progress records
instead of restating mutable status. Preserve technical proof and source roles.
For multi-task plans, include a short human-language view of what each task
gives the owner or enables next, linked to its detailed scope. Reuse task
outcomes rather than maintaining a separate set of requirements or statuses.

**Acceptance:** small and multi-task examples explain the result and contribution;
internal work describes its enabling effect; absent direction remains unknown;
the multi-task example lets the owner understand each task without reading its
technical instructions; existing technical sections and required preparation
remain usable.

### T-003 — Make reports explain results and next action

Consumes ART-001/002/003; produces ART-004. Depends on T-002 so terms and links
agree. Advances FLOW-002 and IF-002; preserves INV-001–004.

Update bounded-task-implementer and task-acceptance-review source output
guidance/templates as applicable. Put the short owner explanation before dense
metadata while retaining required identity and verdict fields. Discovery remains
independent evidence; acceptance consumes it and owns the advancement decision.
Change discovery output guidance only if a required input is genuinely missing.
Update the existing root/profile/flow guide links and explanation as needed.

**Acceptance:** successful, interrupted, rejected, and evidence-incomplete reports
plainly distinguish changes, proof, limits, next actor, and owner decisions.
An implementer summary never calls its own work independently accepted. A report
does not mutate the approved plan or erase outstanding findings.

### T-004 — Qualify the complete reading experience

Consumes ART-001/003/004; produces ART-005. Depends on T-003. Advances all flows
and IF-003; verifies all invariants.

Reuse and extend relevant existing evals and fixture helpers after inspecting
their setup. Supply actual source documents and result evidence to consumers;
metadata-only prompts do not establish success. Include a small change and a
multi-task example, with interruption, stale/conflicting evidence, and missing
direction variants where they exercise distinct risks. Check that the rubric
rejects an opening with a planted unsupported completion claim.

Inspect DEVELOPMENT_SKILL_SOURCES, PROFILE_SKILLS_README, SHARED_SCRIPT_FILES,
focused installer tests, and README installation guidance together. Existing
skill names/dependencies should normally suffice; do not change lists without
need. Install only in a disposable repository, preserve installer ownership
limits, and use fresh consuming sessions for candidate behavior.

**Acceptance:** emitted documents meet the questions in section 2, match supplied
evidence, and preserve the existing flow; owner feedback confirms comprehension.
Record actual outputs, candidate identities, corrections and unrun checks.
Independent discovery and separate acceptance remain required where the
bounded-task workflow requires them. No qualification run is claimed by this plan.

## 6. Verification plan

| Risk / boundary | Supplied scenario and oracle | Owner / evidence |
|---|---|---|
| Clear-looking text is still incomprehensible | Owner reads pilot opening and answers the five section-2 questions in their own words; record unresolved confusion | T-001, repeated on integrated outputs in T-004; human validation |
| Task loses connection to intended result | Small and multi-task source packages; compare emitted plan/brief contribution with actual direction, dependencies and next proof | T-002/T-004; output-level evaluation |
| Unsupported success or hidden uncertainty | Reports with unfinished work, missing direction, superseded acceptance or conflicting evidence; summary must retain limitation and correct next actor; planted wrong summary must fail rubric | T-003/T-004; contrast evaluation |
| Writing changes weaken safeguards | Existing preparation, discovery and acceptance fixtures; preserve independent decisions and required evidence while changing presentation | T-002/T-003; relevant local regression modules |
| Works in source but not when installed | Canonical installer in disposable target; fresh consumer receives complete runnable scenario inputs; inspect actual emitted output and version | T-004; installation + behavior evidence |
| More documents and competing status | Compare required outputs and guide navigation before/after; one owner per fact, no mandatory parallel overview/status store | T-001 design and T-004 output review |

Cheap local gates come first, one at a time: task-map validator for this plan;
then, during implementation, the changed skill's package checks and relevant
modules listed in tests/README.md. Likely selectors include
test_task_preparation_contracts.py, test_bounded_task_implementer.py,
test_task_acceptance_review.py, test_task_flow_guides.py, and
test_install_development_skills.py. Select by actual changed contracts; do not
run the whole list merely because it is listed here.

Structural checks prove references and packaging only. They cannot prove owner
comprehension or skill behavior. Obtain permission before model-consuming,
slow, live-networked or external-review checks unless that exact check class
has since been approved. Lack of permission leaves that evidence unrun, not passed.

## 7. Risks, delegated choices, and next action

Main risks: another redundant summary; persuasive text hiding incomplete proof;
changes across too many skills; a readability rubric mistaken for actual owner
understanding. The pilot, ownership rules, narrow task boundaries, and final
owner check address these risks without a dashboard or universal registry.

No unresolved system-design choice blocks independent plan review. The future
owner clarity decision blocks T-002 adoption, not creation of the T-001 example.
Exact wording, task-local test cases and narrow section placement are delegated
within the contracts above. A new artifact type, stage, status service, or weaker
proof requirement requires a separate scope decision.

**Next action:** run project-plan-verification in a fresh session against this
plan and task-map.json. The existing project-plan-review.md is historical and
does not approve these files; write the new result beside it as
documentation-clarity-plan-review.md. Then brief T-001 under the normal bounded
task workflow. Keep implementation results beside their tasks; do not update
this plan into a progress ledger.
