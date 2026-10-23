# Correction limits and issue disposition

Date: 2026-10-23. Recommendations, with the source-policy update recorded below.
Companion: [single-task direction](direction-single-task-sbx.md).

## Two separate decisions

Acceptance answers whether the current work meets the required checks and has
no unresolved blocking issue. A bounded known issue can remain when the
acceptance policy permits it. Acceptance does not require zero observations.

The execution budget answers whether the system should keep trying on its own.
Reaching a limit stops execution with partial work and evidence; it never turns
failed work into accepted work. Conversely, three attempts must not be a minimum
before acceptance. Accept as soon as the conditions are met.

Recommendation: retain a finite per-task correction/spend budget as a backstop.
Do not increase it merely because reviewers keep producing new suggestions.
First fix the disposition rules and preserve accepted dispositions. A later
budget change needs an owner decision; the existing three-cycle rule remains
until changed.

## Evidence before severity

For a proposed blocker, ask for a concrete trigger, observed or demonstrated
consequence, the relevant approved requirement or operating context, and evidence
that the consequence matters in that context. A reproduced failed required check
can supply this directly. A serious untested concern may instead justify a focused
evidence request; it is not automatically a confirmed defect.

For the current sbx direction, do not elevate outer-system containment, parallel
execution or PR integration concerns into current blockers. Those are deferred
unless new facts change the approved scope and the owner revises that decision.

Use three practical outcomes for findings:

- Block: a required behavior fails, or evidence shows a material consequence
  within the approved use. State what correction or proof would resolve it.
- Known issue: a confirmed, bounded defect fits the approved deferral policy.
  Record why the task remains usable and what would require reassessment.
- Observation: preference, polish or an unsupported improvement suggestion.
  It does not create a correction obligation.

Required evidence that is missing remains unresolved; it is not an observation
or an accepted defect. Keep issue IDs stable. Reopening a disposition requires
new relevant evidence or changed exposure, not a fresh reviewer preference.

## Minimal tooling recommendation

Start with a small deterministic check of review records: each blocker needs
its requirement/context reference, trigger, consequence and evidence; each
deferral needs its rationale and reassessment condition. Reject contradictory
results, such as an acceptance with an unresolved required check. This validates
the record and routing, not the truth of the reviewer's judgment.

The independent acceptance reviewer evaluates the evidence and makes the
contextual decision. A separate non-LLM classifier is deferred: without agreed
rules and representative labeled examples it has no established basis for better
severity decisions. If calibration remains a problem, retain real disputed cases
for later evaluation before adding another model or service.

Stop unproductive repetition before spending the whole budget when the same
blocker returns without new evidence or a materially different correction plan.
This is a proposed progress check, not an implemented or approved extra stop rule.

## Existing skill and approved source update

The [source acceptance skill](../../task-implementation-flow/task-acceptance-review/SKILL.md)
and the active project-local installation both permit bounded known
issues, reject preference-only correction obligations and preserve stable
dispositions. They do not set a new global correction limit; task-specific stop
rules still apply.

The owner subsequently approved updating the source skill: an AI coordinator
acting within approved task authority may record acceptance-approved bounded
deferrals without another human confirmation. Requirement/proof waivers and
unresolved material-risk decisions remain with the owner. Recording reuses stable
IDs and preserves provenance/history; failure to record blocks advancement.
Acceptance and discovery do not write the tracker. The active project-local
installation has not been refreshed and retains the older human-recorder rule.

## Tracking recommendation for the automated flow

Use one repository-local `docs/known-issues.json` file as the proposed canonical
tracker for the initial single-task flow. Keep full review evidence in its owning
reports and reference it from issue records. Do not maintain a second hand-edited
Markdown copy. The existing skill still defaults to Markdown unless the project
declares a different tracker and format; this recommendation does not migrate it.

Each issue needs a stable ID, current status, acceptance-report/task/finding
references, affected area/consumers, trigger/consequence, impact and exposure,
deferral rationale, evidence links, follow-up owner/action and reassessment
conditions. Preserve resolution evidence and history instead of deleting records.
The coordinator checks an existing provenance match before adding an issue, so
retrying a recording does not create another ID. The tracker records an approved
decision; it cannot itself grant acceptance or waive a requirement.

When implemented, use one writer and write a complete validated replacement
through a temporary file and rename. Validate record shape, unique IDs and
required decision references. These checks cannot establish that a deferral is
semantically justified. A small local reader/writer is sufficient; no database,
issue service or generic tracking framework is needed for the first version.

Keep Jira or another external issue service as later integration if a human team
needs it. Choose one authority and link or synchronize deliberately then; do not
make external-service setup or availability a gate for the first local loop.

No numeric severity score, new model, mandatory review stage, tracker executable
or runtime change is introduced by these notes. JSON storage remains a proposal.
