# Task Brief: SIDE-002 — Make task briefs concise contracts and move verification detail to its owner

## Outcome

Update the task-design skills so briefs help the owner judge the work and help
the next agent execute it. Each obligation has one authoritative home. Acceptance
criteria remain easy to check; detailed risk verification belongs in the separate
`verification.md`. Generated briefs carry only the execution information needed
for that task.

## Authority and scope

The owner requested this separate task after reviewing T-001.3's three brief
versions and discussing their document design. The agreed direction is to reduce
reading and maintenance burden, preserve useful lists, separate requirements
from verification methods, and remove repeated workflow instructions. This is a
side task, independent of the maintainability delivery plan. No new direction
decision is required.

Read-only design context:

- [Original T-001.3 brief](../T-001.3/brief.md): the task obligations to preserve.
- [First alternative](../T-001.3/brief-alternative.md): useful AC titles and
  bullets, but repeated requirements across sections.
- [Second alternative](../T-001.3/brief-alternative-2.md): improved content
  ownership, but dense AC paragraphs and too much verification detail in risks.
- [T-001.3 verification design](../T-001.3/verification.md): the separate home
  for detailed cases; it is not evidence that those cases passed.

Neither alternative is a target format to copy wholesale. The owner confirmed
the design principles above, not every editorial choice in those examples.

| Area | Permitted changes |
|---|---|
| `skills/task-implementation-flow/task-brief-designer/` | Instructions, brief template, and owning tests/evals for the new brief contract. |
| `skills/task-implementation-flow/task-verification-designer/` | Instructions and owning evals for deriving the detailed risk cases removed from briefs. |
| Flow README, artifact-layout guidance, preflight/implementer/review instructions and their templates/tests | Correct only assumptions made stale by the new content boundary or optional headings/risk rows. |
| Development installer, focused installer tests, profile guide and installation README | Inspect as required by repository policy; synchronize only affected references or resources. |

[SIDE-001](../SIDE-001/brief.md) owns verification-document presentation. Preserve
its readable test-case format and metadata rules; this task changes how the
brief and verification design divide responsibility.

Do not rewrite existing task briefs, verification documents, plans, or review
history. Do not refresh the active installation, add a generic document checker,
or change runtime orchestration, sizing thresholds, or review policy. Treat
editable source as the implementation target, separately from installed skills.

Expected contract impact: the two skills' document-output contract changes.
Check downstream consumers before removing required structure. Current
[installation](../../contracts/installation.json) and
[foundation-tool](../../contracts/foundation-tools.json) contracts remain in
force; update registry records only for an actual change to registered authority.

## Acceptance

**AC-01 — Briefs explain the task without repeating it.**

- Lead with the observable outcome, its user or consumer, and what it enables.
  Follow with scope/constraints, acceptance, necessary evidence boundaries, and
  task-specific execution information.
- Give each fact one home. Use precise references for shared authority and
  workflow policy; keep critical local boundaries explicit. Do not require the
  reader to reconstruct the task from a broad parent-document reading list.
- Allow sections and formatting to match the task. Remove mandatory repeated
  summaries, empty fields, process commentary, and separate direction/history
  accounts when their necessary facts already have a clear home. Preserve exact
  provenance or direction decisions where they affect authority or freshness.
- Use short sentences and concrete terms. No fixed word limit, heading count,
  or formatting quota substitutes for readability and complete obligations.

**AC-02 — Acceptance criteria expose independent completion conditions.**

- Use stable AC IDs and descriptive titles. A single cohesive condition can use
  prose; several independently testable obligations use short, preferably flat
  bullets or a clear comparison table.
- Keep required behavior, refusals, boundaries, lifecycle rules, and unchanged
  state in acceptance or its precise cited authority. Do not hide obligations
  inside dense paragraphs or remove them as apparent verification detail.
- Leave test setup, observation methods, and implementation choices to their
  owners unless the task authority requires a particular boundary or mechanism.

**AC-03 — Risk notes add information instead of duplicating acceptance.**

- A brief's risk section is optional. Include a consequential failure, invariant,
  or essential proof boundary only when it adds information needed to interpret
  or safely execute the contract. Do not require R IDs or a six-field risk block
  merely to satisfy a template.
- Move detailed scenario enumeration, case matrices, fixtures, assertions,
  measurement methods, evidence reuse, reviewer probes, and verification gate
  allocation to verification design. Do not reproduce those details in the brief
  under another heading.
- Preserve any finite values or allowed transitions that define the requirement.
  For example, requiring malformed settings to fail without fallback stays in
  acceptance; the malformed inputs and assertions used to prove it belong in
  verification design.

**AC-04 — Verification design closes coverage without redefining the task.**

- Derive finite material cases and decisive observations from acceptance and
  cited authority even when the brief has no risk rows. Absence of an R section
  is neither missing authority nor permission to check only the happy path.
- Own detailed cases, real inputs/setup, expected observations, implementation
  evidence, independent corroboration, and gate ownership/stage. Preserve
  negative, boundary, lifecycle, preservation, and interaction coverage where
  required; avoid speculative catalogs and unnecessary Cartesian products.
- Retain traceability to ACs and any supplied risk IDs. Support for older brief
  formats is not required; existing task artifacts remain unchanged.
- Route an unresolved expected behavior back to task design or the owner.
  Verification may derive cases; it cannot invent requirements or settle scope.

**AC-05 — Execution and handoff contain only actionable task information.**

- Keep status/task kind, the first pending preparation action, the four launch
  keys, required sizing evidence, and task-specific stops, outputs, consumers,
  or deviations. Explain readiness once; do not imply that a prepared brief
  authorizes implementation.
- Remove repeated next-action lists, generic status definitions, standard
  permission reminders, default report inventories, and full default workflow
  recitations from generated briefs when the consuming workflow already supplies
  them. Required default routes must remain available through a precise shared
  reference; retain local exceptions and any explicit machine/audit obligations.
- Preserve derived verification then ready preflight before packaged execution,
  sizing/decomposition decisions, conditional stage order, and fresh discovery
  followed by a separate acceptance decision when required. Shorter documents
  must not waive, reorder, or silently transfer these responsibilities.

**AC-06 — Instructions, consumers, and evidence agree.**

- Skill instructions, templates, examples, completion checks, and relevant
  tests/eval expectations follow the new boundary. Inspect existing coverage
  before changing it; preserve distinct scenarios when replacing format checks.
- Downstream stages accept the new compact format. They obtain verification
  detail from `verification.md` rather than requiring
  every brief to carry risk matrices or fixed section headings.
- Apply the content boundary to single executable tasks and split tasks. Keep
  parent/child coverage, dependencies, and integration-proof ownership clear;
  each executable child retains enough information to execute its own task.
  Preserve required audit and freshness information in high-assurance briefs
  without repeating verification detail.
- Worked outputs show readable ACs, appropriate optional risks, and a concise
  execution section while retaining all source obligations. Smaller word counts
  or successful syntax checks alone do not establish this result.

## Evidence

Verification-design recommendation: separate — this changes the responsibility
boundary between two authoring stages and must preserve coverage through their
consumers. That invocation owns detailed cases and the coverage comparison.

Start with existing preparation-contract coverage in
`tests/test_task_preparation_contracts.py`, brief-designer package tests, and both
skills' evals/fixtures. In particular, revise the existing finite-risk eval's
expectation that all six risk fields appear in the brief; preserve its distinct
artifact, lifecycle, and failure obligations across the brief/verification pair.
Use `testing-discipline`; update existing facilities rather than add a harness.

Use a simple task and an existing finite-risk task to inspect paired worked
outputs. Compare their requirements with the source authority, including the
case with no brief risk section. Check that the compact brief and its verification
design supply what preflight, implementation evidence mapping, discovery, and
acceptance need. Include split-task and high-assurance forms in the output review
to check the obligations in AC-06; older-format compatibility is not required.
Keep illustrative/source-guided output review
distinct from an executed skill eval. Live/model evaluation requires a separately
approved budget; if absent, report generated behavior as unqualified.

Run the owning focused suites first, then installer coverage if affected and
`python3 tools/verify.py` for the cross-skill change. Establish the repository's
architecture and contract checks before handoff; applicable current aggregate
evidence can cover them. Report failures, skips, and active-installation drift.

## Execution

Status: `ready` — brief prepared; execution prerequisites remain pending.
Task kind: `executable`; guided profile.

Next: derive this task's `verification.md`, then obtain a ready `preflight.md`
through standalone guided preflight. Confirm consumer assumptions and current
SIDE-001 presentation before implementation. Stop if simplification requires a
new authority decision, removes a required assurance boundary, or requires
rewriting existing task artifacts.

After implementation or correction and applicable maintainability review and
registry synchronization, immediately use fresh independent
`task-review-discovery`, then a separate `task-acceptance-review` decision.
Publish results and separate review artifacts in this task package.

```yaml
agent_tier: standard
reasoning: medium
review: immediate
budget: 15 tool calls / 40 minutes / brief and verification ownership with focused coverage
```

Sizing: `default@1`; estimate 15 implementation-agent calls / 40 minutes;
confidence medium; fits. Reuses existing templates, tests, and finite-risk evals;
excludes separate preparation/review stages and live evaluation.
