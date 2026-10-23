# How to unblock T-002

Date: 2026-10-23. Owner guide; current readiness remains INCONCLUSIVE.

## What we are building

You give the system a prepared task and permission to do it. It implements the
work, runs checks, gets an independent review, corrects problems, and commits
accepted changes. If it cannot continue safely, it preserves the work and tells
you what decision is needed. The current plan requires an active coordinator
session; it does not promise to keep working after that session ends.

The [plan](../../local-harness-orchestration-plan.md) covers that goal. T-001
checks whether the chosen agent runtime can support it. T-002 builds the
controller's records and guards: who may work, whether another worker may still
be running, and how many correction attempts have been used. Later tasks connect
agents, review, correction, commits and the complete working loop.

T-002 itself needs no new agent launch to test its bookkeeping. Its current
block is the agreed prerequisite gate: establish a usable runtime contract
before dependent implementation. This is the current project decision, not a
claim that writing controller code is technically impossible.

## 1. First, keep workers under the controller's control

The controller needs to know which agent is working. A worker that can start
extra agents creates a route outside that tracking. We therefore required those
extra-agent tools to be unavailable to workers and reviewers.

In the tested Codex CLI configuration, those tools are still offered even when
the relevant settings say they are disabled. This was reproduced independently.
Nobody used them to start another agent. The confirmed problem is exposure of
the tools; successful misuse or damage has not been proved.

**Next action:** inspect supported controls in the installed runtime, then test
a concrete candidate locally without paying for a model call. The result must
show that extra-agent tools are gone while normal shell and file editing still
work. Test both worker and reviewer settings.

If that works, continue to step 2. If it does not, stop and bring you one concrete
runtime-change option, with its expected benefit and test method. Changing the
runtime requires your approval. Do not change backend, remove required tools,
or replace enforcement with an instruction asking agents to behave.

You do not need to approve another paid session to start this local investigation.
A new runtime option must be verified before we claim it solves the problem.

## 2. Check the other ways a worker could act outside its role

After step 1 passes, test that inherited plugins, connected services, browser
tools and automatic startup commands cannot bypass the selected restrictions.
Use harmless disposable examples, with a control showing that each example
would work when enabled. An empty tool list or a setting alone is insufficient.

**Done when:** both worker and reviewer launches suppress the tested unwanted
tools and startup actions, with recorded observations. An untestable required
surface remains an explicit blocker.

## 3. Close the missing evidence from earlier successful checks

Earlier checks reportedly passed. Keep those results; the problem is that the
review packet lacks the raw output needed to corroborate them independently.

- Model settings: recover the outputs for the chosen model at low, medium and
  high reasoning, or request approval for exact replacement checks.
- File permissions: independently inspect retained observations or repeat the
  local non-model check. Workers must be able to edit task files; reviewers and
  workers must be unable to edit the relevant protected files.
- Native file editing: retain the actual rejected edit requests and runtime
  rejection messages, together with filesystem checks. A file being absent
  does not prove that an attempted edit was rejected.

**Done when:** a fresh reviewer has evidence to corroborate each claim. Do not
search personal session stores without an owner-supplied evidence location.

## 4. Confirm that the real service behaves like the local checks

A local simulated service can test the CLI's tool assembly. It cannot prove
that the selected live model service exposes the same tools or enforces the
same worker/reviewer configuration.

**Next action:** once local checks pass, present one bounded paid qualification
request with the exact sessions, settings, checks and budget. Combine compatible
checks where useful. All five previously approved live sessions are consumed;
new paid sessions require your approval.

**Done when:** real worker and reviewer evidence supports the same restrictions,
required editing behavior and approved model settings. Keep the raw output.

## 5. Have new evidence checked, then make the readiness decision

First, a fresh independent reviewer gathers and checks the evidence. Then a
separate fresh reviewer decides whether T-002 may start. Both previously approved
review sessions are consumed; authorize these two sessions separately from the
live qualification checks. This guide is not either review.

**Done when:** the separate acceptance report explicitly releases T-002, or
identifies the remaining blocker and its next action. The earlier accepted
investigation remains valid throughout; it did not certify runtime readiness.

## What to do now

Start only step 1. Use the existing installed runtime, local inspection and
non-billable disposable probes. Retain output. Return either a tested control
that works, or a concrete explanation of the missing runtime capability and
the smallest change that needs your decision. Do not spend on steps 3–5 while
the decisive control is unresolved. Recoverable existing evidence can be supplied
without new paid checks.

The technical scope and stop conditions are in the
[bounded recovery proposal](capability-recovery-proposal.md). The current facts
come from [acceptance-02](reviews/acceptance-02.md) and
[discovery-03](reviews/discovery-03.md). No official plan, accepted report,
production code or active installation is changed by this guide.
