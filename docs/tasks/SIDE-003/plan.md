# SIDE-003 — Reduce skill loading cost while preserving behavior

Status: proposed implementation plan. Created 2026-11-03.

## Outcome and scope

Reduce the instructions loaded in agent sessions by shortening skill discovery
metadata and loading detailed procedures only when they apply. Preserve current
activation boundaries, output contracts, safeguards, and quality gates.

This plan covers the current editable packages under `skills/`. The development
profile's 20 skills are the first delivery group. The other six source skills
remain in the description audit; body restructuring outside the pilot requires
evidence that it reduces a real loading path. Source presence does not establish
installation or activation. Do not modify user-global skills, refresh this
repository's active `.agents/` installation, or change host context settings.

This document authorizes planning only. It is not an executable task brief,
ready preflight, completed review, or claim of behavioral qualification. Prepare
bounded task packages from the phases below before implementation. Keep future
results beside this plan; do not overwrite it with execution history.

## Basis and recommendation

Official OpenAI guidance says discovery starts with metadata, full `SKILL.md`
is loaded on selection, and descriptions should be concise with clear scope and
boundaries. It also says hosts may shorten descriptions or omit skills when the
initial catalog exceeds its budget. Front-load the distinguishing trigger.
See [Build skills](https://learn.chatgpt.com/docs/build-skills), accessed
2026-11-03. The page supports the approach, but does not establish the supplied
September 2026 publication attribution.

Proceed in two separate experiments: description compression, then conditional
body extraction. Shorter descriptions can reduce startup context and improve
catalog visibility. Body extraction can reduce selected-skill context. Neither
proves lower total session usage: additional reads, repeated instructions,
retries, or missed routing can erase the gain.

Use one skill identity with explicit internal routes. Do not create separate
public guided/high-assurance skills: they would add discovery metadata and
another activation decision. Do not add a loader framework, change workflow
policy, remove gates, or convert prose to executable helpers in the first pass.
Existing helpers remain authoritative where already used.

## Current source baseline

Measured from clean working-tree source at commit
`aa94e28eaf170b68b30300b3f7cb183943698076` on 2026-11-03.
There are 26 `SKILL.md` files, totaling 404,992 bytes. Their bodies total
388,640 bytes. These are UTF-8 byte counts, not tokens. The supplied older file
sizes are historical context and are not the experimental baseline.

Body bytes below are everything after the closing frontmatter delimiter,
including its following whitespace. Description characters count the normalized
scalar text, excluding other frontmatter fields. Phase 1 must retain a
reproducible inventory and exact per-file hashes.

| Skill | Development profile | File bytes | Body bytes | Description characters |
|---|---|---:|---:|---:|
| ai-flow-foundation | yes | 8,634 | 7,994 | 580 |
| architecture-guardrails | yes | 17,306 | 16,708 | 533 |
| ask-user-questions | no | 5,345 | 4,559 | 720 |
| foundation-readiness-review | yes | 9,196 | 8,684 | 445 |
| idea-brief | no | 8,097 | 7,439 | 620 |
| idea-challenger | no | 6,735 | 5,890 | 797 |
| idea-investigator | no | 10,937 | 10,344 | 548 |
| ollama-delegate | yes | 6,124 | 5,610 | 339 |
| project-bootstrap | yes | 11,663 | 10,941 | 659 |
| project-delivery-plan | yes | 17,935 | 17,199 | 687 |
| project-direction | yes | 7,936 | 7,299 | 573 |
| project-plan-verification | yes | 14,058 | 13,356 | 649 |
| repo-foundation | yes | 22,269 | 21,649 | 563 |
| senior-code-review | yes | 9,387 | 8,584 | 638 |
| session-handoff | yes | 8,307 | 7,578 | 515 |
| skill-creator | no | 34,440 | 34,080 | 319 |
| bounded-task-implementer | yes | 41,936 | 41,369 | 515 |
| task-acceptance-review | yes | 32,281 | 31,632 | 599 |
| task-brief-designer | yes | 26,051 | 25,433 | 571 |
| task-contract-registry-updater | yes | 6,998 | 6,661 | 279 |
| task-maintainability-review | yes | 21,497 | 20,786 | 640 |
| task-preflight | yes | 22,142 | 21,647 | 453 |
| task-review-discovery | yes | 16,195 | 15,652 | 494 |
| task-verification-designer | yes | 15,620 | 15,079 | 487 |
| task-orchestrator | no | 7,005 | 6,205 | 635 |
| testing-discipline | yes | 16,898 | 16,262 | 590 |

Inspect source through [the project map](../../project-map.md),
[development commands](../../development.md), and
[implemented contracts](../../contracts/index.json). The
[installer](../../../scripts/install_development_skills.py) selects the 20-skill
profile and copies whole selected packages, including references. The installed
copies and available session catalog can differ from these source bytes.

## Description design

For all 26 descriptions, retain the job, positive trigger, and consequential
exclusions. Move procedure, field inventories, preservation details, freshness
mechanics, and report formatting into the body or its conditional references.
Aim for roughly 150–300 characters where sufficient; this is an editorial
starting point, not a limit that can override accurate routing. Start with the
20 profile skills, then the six remaining source packages.

Candidate implementer description:

> Implement, resume, or correct one bounded coding task with tests and
> verification. Use for scoped implementation, including ready task packages
> and supplied machine contracts. Defaults to guided execution.

The user's shorter example is also viable, but “explicitly requested
high-assurance” alone could hide activation through a supplied machine contract.
Preserve that route in the entry instructions and exercise it in routing evals.

Use these boundary groups to review candidates against their nearest neighbors:

| Skills | Distinction that must survive compression |
|---|---|
| project-direction; project-bootstrap; ai-flow-foundation | Owner direction vs initial engineering foundation vs model behavior in the product itself; agent-maintained code alone does not trigger AI foundation. |
| repo-foundation; architecture-guardrails; foundation-readiness-review | Repository structure/tooling vs deterministic boundary enforcement vs independent readiness review before product work. |
| project-delivery-plan; project-plan-verification | Composing multi-task delivery plan vs a separate reviewer checking that plan; neither implements features. |
| task-brief-designer; task-verification-designer; task-preflight | Task contract vs derived scenario/evidence design vs current execution readiness; preflight does not implement. |
| bounded-task-implementer; task-maintainability-review | Authoring scoped implementation vs independent structural review when policy or user requires it. |
| task-contract-registry-updater; task-review-discovery; task-acceptance-review | Synchronize current contracts vs independent evidence without verdict vs a separate acceptance decision after discovery. |
| senior-code-review; testing-discipline | Requested general code review vs risk-based test design/maintenance, also during behavioral implementation. |
| ollama-delegate; session-handoff | Bounded read-only model delegation through the configured runtime vs preserving a session for continuation. |
| idea-brief; idea-investigator; idea-challenger | Stabilize early ideas vs research viability/validation vs proportional premise challenge; avoid making every small edit a research task. |
| ask-user-questions; skill-creator; task-orchestrator | Needed clarification vs skill authoring/evaluation vs explicitly requested orchestration only; generic task execution must not activate the orchestrator. |

Do not “narrow activation” by dropping valid current use cases. Shorten wording
and remove accidental ambiguity. Any deliberate behavior change needs separate
authority. Names, folder paths, and public invocation identities stay stable.

## Body design and mandatory loading

Pilot `bounded-task-implementer` and `task-acceptance-review` first. Both already
have guided and high-assurance routes. Use `references/` inside each package,
reuse existing references, and keep routing one level deep where practical.
A reference name below is proposed, not a new implemented contract.

| Resource | Required loading condition and timing |
|---|---|
| `SKILL.md` | Always on activation: scope, authority precedence, profile selector, core workflow, mandatory gates, stop/route rules, and reference loading table. |
| `references/high-assurance.md` | Read before validating or acting on explicit high-assurance or supplied strict machine contracts; exact inputs, freshness, output schema obligations, and recovery restrictions. |
| `references/run-evidence.md` (implementer) | Read before the first evidence operation when the existing guided availability path applies or instrumentation is required; full lifecycle and recovery procedure. |
| `references/correction-protocol.md` (implementer) | Read before acting on a correction, resuming incomplete work, or producing a correction handoff; preserved identities, original baseline, affected evidence, and re-entry order. |
| Existing report/output references | Read before emitting the applicable report or machine result. A template does not replace decision rules. |

Keep these obligations visible in the implementer entry file:

- Guided is default; a ready package alone does not select high-assurance.
  Direct requests and packaged work keep their distinct prerequisites.
- Packaged work requires applicable verification and ready preflight. Composite,
  stale, mismatched, or legacy inputs route to their existing owner before edits.
- Preserve user work and one original baseline. Required native checks retain
  scope, policy, ownership, and failure consequences. Advisory measurement
  cannot waive them.
- Keep the existing cheap installation-local run-evidence availability check,
  attempt, and skip-once rule. Available tooling still activates best-effort
  instrumentation in guided mode; mandatory instrumentation remains strict.
  Missing tooling does not trigger cross-installation fallback or provisioning.
- Preserve the conditional submission order, reviewer independence, and stale
  evidence rules. Corrections load their procedure before edits.

Keep reviewer provenance, evidence admission, separate discovery/acceptance,
verdict meanings, contextual disposition precedence, deferral authority, and
required gate ownership in the acceptance entry contract. Complex decision
rules used on ordinary guided cases are not high-assurance-only material.
Move exact packet reconstruction and machine/report mechanics first. Retain a
clear trigger for each conditional disposition or reproducer reference.

Treat references as required instructions once their condition applies, not as
optional background. Check applicability before the first dependent action.
If a required reference is missing or unreadable, stop the affected action and
report the exact gap; do not infer permission to bypass it. Do not read every
reference at startup. If a procedure applies to almost every invocation,
count it in the normal path and consider keeping it inline.

After the pilot, consider extraction from `task-brief-designer`, `task-preflight`,
`task-maintainability-review`, and `testing-discipline`. Also inspect larger
`skill-creator`, `repo-foundation`, and `project-delivery-plan` packages. Use
actual conditional paths rather than inventing guided/high-assurance profiles
for skills that lack them. In particular, the testing core applies during
ordinary implementation; specialized test catalogs can remain conditional.

## Delivery sequence

| Phase | Work and output under SIDE-003 | Depends on / completion evidence |
|---|---|---|
| 1 — Freeze baseline | `baseline.md` plus compact machine-readable measurements: source hashes, 26-skill inventory, 20-skill subset, existing read graph, trigger cases, selected behavioral cases, and command prerequisites. Map every pilot obligation to its current authority. | Before edits. Reproduce counts and identify existing coverage and missing scenarios. Snapshot complete old packages and shared dependencies needed for comparison. |
| 2 — Compress descriptions | Edit descriptions in small coherent groups; record old/new wording, preserved trigger boundaries, and catalog measurements in `description-results.md`. Bodies remain unchanged in this phase. | Phase 1; positive, negative, and neighboring-skill trigger evidence. Keep explicit and implicit invocation results separate. |
| 3 — Extract pilot references | Restructure implementer and acceptance packages. `instruction-map.md` maps each old obligation to its new location, loading condition, and proving scenario; `pilot-results.md` records per-route costs and outcomes. | Phase 1; keep description versions controlled when comparing body layouts. Required branches and gates remain reachable; no behavioral regression in selected cases. |
| 4 — Extend selectively | Apply only successful patterns to other packages. Record per-skill decisions and measured paths in `rollout-results.md`; allow no-op decisions for already compact or always-needed instructions. | Phases 2 and 3 accepted against their evidence. Each changed package retains focused scenario coverage. |
| 5 — Validate distribution and close | Validate disposable installations, reference resolution, updated contract authorities, and local regression checks. Publish `results.md` with measured savings, gaps, and rollback units. | Prior phases; inspect installer ownership, update only affected surfaces, finish independent review required by the resulting task contracts. |

Split phases into bounded briefs if needed; do not create one 26-skill executable
rewrite. Keep description and body commits separately reversible. A failed
pilot stops expansion, not unrelated established workflows.

## Measurement and decision rules

Record three distinct layers for baseline and candidate:

1. **Discovery catalog:** normalized description characters and tokenizer counts
   for all 26 and for the 20-skill profile. Include names, paths, and host wrapping
   when measuring a rendered catalog. Record visible/truncated/omitted entries
   if observable; source description reduction alone cannot prove catalog savings.
2. **Loaded instructions:** entry file plus every applicable reference, template,
   and sibling skill actually read. Report entry-only cost and cumulative cost
   separately for direct guided, packaged guided, high-assurance, corrections,
   optional evidence available/unavailable, and representative acceptance paths.
   Count repeated reads in observed traces; unique-file totals are only a static
   estimate. Include command output from discovery/probing in session analysis.
3. **Session use:** comparable runs' input/output usage, cached input where
   exposed, duration, tool/read count, retries, completion and quality results.
   Separate cached and uncached usage; do not equate context size with billing.
   Use actual reported usage when available. Missing telemetry is unknown.

Use the same tokenizer/encoding and version for both sides. Do not install a
new tokenizer without need and approval for dependency/network work; byte and
character counts are a valid initial baseline labeled as such. No bytes/4
conversion may be presented as measured token savings.

The experimental target is **40–60% less default loaded body** for the pilot's
ordinary guided path, including references required on that path. Report the
reduction separately per pilot skill and route. This is a target, not a claim
about every skill or overall sessions. Missing it permits a smaller demonstrated
win; it does not justify removing obligations or hiding required reads.

For promotion: all preserved critical obligations must pass selected behavioral
cases; activation must retain expected routes and exclusions; applicable guided
paths must show lower measured instruction cost. High-assurance and correction
costs must be reported even if unchanged or larger. A material session-cost or
quality regression requires investigation before rollout. Report repeated paired
runs and variation before claiming overall session savings. A single pair is a
smoke comparison, not statistical equivalence. No live evidence means behavioral
and session-saving qualification remain pending.

## Verification strategy

Use [testing-discipline](../../../skills/testing-discipline/SKILL.md) as source
context for future test work; execution must resolve the actual available
installation. Existing `tests/test_bounded_task_implementer.py`,
`test_task_acceptance_review.py`, `test_task_preflight.py`,
`test_task_preparation_contracts.py`, `test_review_composition.py`,
`test_run_evidence_availability.py`, and `test_install_development_skills.py`
provide relevant local coverage. Inspect their fixtures before extending them.
Some assertions read `SKILL.md` directly; update these to inspect the applicable
instruction closure and required route, rather than deleting obligations to
accommodate relocation. Text presence is structural evidence only.

| Risk / priority | Scenario, input, and decisive observation | Evidence level |
|---|---|---|
| Wrong activation — critical | Use catalog-only prompts for explicit invocation, implicit positive, clear negative, and nearest-neighbor ambiguity for each changed description. Compare selected skill sets with reviewed expectations; body content must not leak the expected choice. | Fresh model routing eval, baseline/candidate catalogs with identical unrelated skills. Existing explicit-skill runner alone cannot prove implicit matching. |
| Gate bypass — critical | Reuse direct edit, ready package, missing/mismatched verification, stale/blocked preflight, composite parent, and strict machine-contract fixtures. Expected proceed/refusal, route, and output remain unchanged. | Existing setup checks plus agent runs; inspect effects and reports, not exit code alone. |
| Lost optional evidence — critical | Available helper set, missing helper, failed first operation, strict required instrumentation, and interrupted open run. Observe attempt/skip-once/block/recovery, same installation resolution, and no duplicate lifecycle. | Local helper/fixture tests plus traced agent behavior. |
| Correction/provenance loss — critical | Existing correction fixtures with an original baseline and stale affected evidence. Verify baseline preservation, conditional re-entry order, and fresh reviewer requirement. Self-authored review cannot issue an independent verdict. | Existing correction/composition cases plus agent artifacts and read trace. |
| Acceptance weakened — critical | Complete and partial discovery, missing preparation, unresolved finding, permitted deferral, and stale conditional review. Expected verdict and owner-directed evidence request match preserved policy. | Selected acceptance/discovery fixtures with independent grading against authority. |
| Missing installed reference — critical | Install into a disposable Git repository using the canonical installer; read and resolve each moved reference there, including nested flow paths. Check unmanaged sentinels survive. | Real filesystem installation tests; never refresh this session's installation. |
| Apparent savings only — high | Run paired tasks from identical fixture bytes and separate fresh sessions, with fixed model, reasoning, permissions, tools, and catalog. Inspect read events and actual usage; repeat selected pairs to expose variation. | Approved model-backed benchmark plus static instruction accounting. |

Reuse existing eval inputs/setup from the owning `evals/` directories. Add only
missing distinct loading/trigger cases. Give every selected case real setup,
expected behavior, observed artifacts, and a grading oracle established before
candidate runs. Preserve negative and failure scenarios when consolidating tests.
For extraction checks, temporarily remove a required link or bypass a route in
a disposable candidate and show the relevant check detects it.

The existing
[`run_behavior_evals.py`](../../../skills/skill-creator/scripts/run_behavior_evals.py)
accepts selected `--ids`, `--baseline-skill`, `--output-dir`, `--model`, and
`--reasoning`. Inspect selected eval execution metadata before using it. It is
an execution tool, not automatic semantic grading, implicit-trigger testing,
or proof that usage telemetry and freshness-aware resume are implemented.
See its [future-work limits](../../../skills/skill-creator/docs/codex-behavioral-eval-runner-future-work.md).
Snapshot full packages, preserve raw outputs, and grade artifacts independently.
Do not build a general benchmark platform for this task.

Run narrow local suites first, then relevant flow/installer suites, then the
aggregate gate for the cross-cutting implementation. Validate packages with the
existing validator only when its dependency is already prepared. Finish with:

```sh
python3 tools/verify.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py
python3 tools/check_contracts.py --root .
```

Inspect `DEVELOPMENT_SKILL_SOURCES`, `PROFILE_SKILLS_README`,
`SHARED_SCRIPT_FILES`, installer tests, and README installation instructions in
the same implementation change. Whole-package copying should already carry new
references; prove that in a disposable target instead of broadening ownership.
Do not add repository-only measurement tools to shared runtime dependencies.
If moved declarations change registered authority paths, update the affected
subsystem records through the task flow's registry-updater stage and regenerate
the index with the explicit `--write-index` command. Do not register planned
capability now. Profile drift in the active installation is reported, not fixed
mid-session.

Local/schema/link checks establish structure and fixture behavior only. Obtain
approval for a concrete bounded model-eval budget before live runs: selected
skills, cases, paired repetitions, model/reasoning, maximum calls, timeout, and
stop condition. This plan does not approve provider spending or external review.
If that approval is absent, finish local work and report live qualification as
pending. Do not claim task outcomes are equivalent from static checks.

## Completion and rollback

Completion requires shorter metadata with preserved activation boundaries,
reachable conditional instructions, a complete pilot obligation map, passing
applicable local gates and installed-package checks, and approved behavioral
comparison evidence with no unresolved critical regression. Report actual
instruction savings and session usage separately, including failures and gaps.
The plan's numerical target is advisory; an unqualified result is labeled so.

Rollback reverts the smallest description group or complete extraction unit,
including its tests, references, and affected registry authority paths. Do not
leave an entry file pointing to removed instructions. Re-test the affected route
and distribute the restored package only in a new authorized installation/session.
