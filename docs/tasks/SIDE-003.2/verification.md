# Verification Design: SIDE-003.2 — Compress boundary groups 1–2

Shorter descriptions must still expose the same jobs and activation boundaries.
The six skill bodies, names, paths, and invocation identities must stay unchanged.
Local checks establish editorial and structural evidence. They do not prove that
a model selects the same skills from the catalog.

## Shared setup

Use the six source packages named in [the brief](brief.md). Preserve the
SIDE-003.1 baseline and use `python3 tools/baseline_measure.py` for both sides.
Before edits, compare current skill hashes and counts with
`../SIDE-003/baseline-measurements.json`; a missing or stale baseline stops work.
Keep the baseline file unchanged. Serialize work with other description leaves.

Existing evidence inspected: `tests/test_install_development_skills.py` reads
foundation skills and checks AI routing wording; project-direction evals 1–3
cover creation, extraction/audit, and a direction delta, while eval 4 covers
research exclusion. Architecture-guardrails evals cover proportional deferral
and a legacy no-regression baseline. These evals are not catalog-only routing
tests. Reuse their relevant expectations; no new runtime test harness is needed.

## Test cases

### V-01 — Preserve the six jobs and their routing boundaries

Review each old/new pair against its complete old description and the plan's
boundary-group rows. The following cases define the minimum concrete routing
inputs. Each row has stable child cases: `E` explicit, `P` implicit positive,
`N` clear negative, and `B` nearest neighbor. For `E`, use the exact prompt
`Use $<skill-name> for its documented job.` and expect that named skill. For
the other cases use the prompts below; the oracle concerns selection of the
target skill, not an exhaustive set of all potentially applicable skills.

| Case stem / target | P: select target | N: do not select target | B: select named neighbor for this job |
|---|---|---|---|
| V-01a / project-direction | Our plans are too technical for me to govern. Extract an owner-editable direction and clarify priorities and trust boundaries. | Research competitors and commercial demand before I decide whether to proceed; do not write a direction. | We have an agreed objective and scaffold. Establish the initial engineering charter and foundation plan before product planning. → project-bootstrap |
| V-01b / project-bootstrap | We have an objective and scaffold. Establish the minimum project charter and engineering-foundation plan before specification or implementation. | Plan the next user-facing feature in this established product. | Clarify the owner's desired experience, ordered priorities, and decision ownership; do not choose engineering setup. → project-direction |
| V-01c / ai-flow-foundation | Before detailed design, establish testable boundaries for a product whose runtime calls an LLM. | Coding agents maintain our app, but the product never calls a model. Do we need AI-flow foundation? | Set up agent-readable repository maps, commands, and placement rules for a deterministic app. → repo-foundation |
| V-01d / repo-foundation | Standardize module placement, repository tools, generated-code flows, CI commands, and agent instructions. | Fix this isolated arithmetic bug using the existing structure and commands. | Enforce the chosen rule that domain modules cannot import infrastructure; add deterministic boundary checks. → architecture-guardrails |
| V-01e / architecture-guardrails | Repair deterministic import and cycle guardrails and their canonical command; preserve known legacy debt without allowing new violations. | Redesign our product architecture and make a heuristic file-size target a universal hard failure. | Create the repository layout, commands, module map, and agent guidance. → repo-foundation |
| V-01f / foundation-readiness-review | Independently check the materialized foundation before product planning: can an unfamiliar agent navigate, bootstrap, run, test, inspect failures, and follow persisted rules? Recommend the next delivery route. | Review whether the implemented checkout feature works correctly. | Materialize the planned repository layout and tools; this is implementation, not independent readiness review. → repo-foundation |

**Expected result:** All six targets keep their jobs, positive routes, and
consequential exclusions. Group 1 separates owner direction, initial engineering
foundation, and model behavior inside the product. Coding-agent maintenance
alone does not activate AI-flow foundation. Group 2 separates materialization,
deterministic enforcement, and independent readiness before product work.

**How to check:** Record an editorial checklist per skill in
`../SIDE-003/description-results.md`. Review all original activation routes,
including project-direction create/extract/audit/rebaseline and mid-project
deltas; bootstrap timing and scaffold prerequisites; AI pre-planning timing and
prompt/agent-design exclusions; repo creation/restructuring/standardization and
placement decisions; guardrail repair, baselines, and agent contract; and
readiness timing and independent scope. A shorter description must not remove
a valid route to meet the suggested character range.

For future behavioral evidence, give fresh sessions the baseline or candidate
catalog containing only names and descriptions, with all unrelated entries
identical. Run E separately from P/N/B. Do not supply skill bodies, this table,
or expected choices in the model input. Record selected sets and grade against
the row oracle. These 24 inputs are designed, not authorized live runs; obtain
separate approval for the model, reasoning, repetitions, call cap, timeout, and
stop condition. The existing explicit-skill eval runner alone cannot prove
implicit selection. Until approved runs occur, mark model routing pending.

### V-02 — Removed procedural detail remains available

For each old/new pair, identify omitted procedure, output paths, field lists,
or workflow detail. Locate its existing body authority and record that location
in the results. If a detail has no body authority, retain it in the description
and flag it. No body edits are allowed. This rejects compression that silently
removes an obligation even if the new text still appears to describe the job.

### V-03 — Only the six description values change under skills

Compare each touched package with its original Git bytes. After replacing the
description scalar with a common sentinel, the remaining bytes must match
exactly. The diff under `skills/` must contain only the six description changes;
all other packages, names, paths, and identities remain unchanged. Inspect
`git diff --stat` and targeted diffs. There is no useful fail-first editorial
test; exact preservation and the V-01 checklist are the negative oracles.

### V-04 — Record reproducible catalog reduction

Run `python3 tools/baseline_measure.py` after the edits. Record normalized
old/new description characters for each skill and before/after totals for all
26 skills and the 20-skill profile. Both catalog totals must decrease and their
delta must equal the six individual deltas. Body-byte totals must remain
388,640 and 320,123 respectively. Record actual results without a hard
per-description length limit. These are character/byte counts, not measured
tokens, rendered catalog visibility, billing, or session savings.

### V-05 — Existing consumers and package checks remain valid

Inspect the installer constants, managed profile guide, installation README,
and the SIDE-003.1 prerequisites map for quoted descriptions. Update only owning
assertions that quote changed text, or record that none need synchronization.
In particular, the installer suite asserts `coding agents will develop or
maintain` in the AI skill's full text; preserve its routing assertion if the
description changes. Run the owning installer suite first:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py
```

Run `skills/skill-creator/scripts/quick_validate.py` for each touched package
if the optional PyYAML environment is already available; otherwise record the
skip. This validates package structure, not model behavior. Do not install a
dependency or refresh the active installation for this task.

## Gate ownership and evidence limits

Implementation owns V-01–V-05 local evidence, the canonical architecture check,
and `python3 tools/check_contracts.py --root .`. No contract authority moves.
The fresh independent discovery reviewer corroborates the final descriptions,
preservation, counts, and reported checks; a separate acceptance reviewer
decides acceptance from that report. SIDE-003.18 owns the aggregate gate.
Live routing remains pending without its separate budget approval. Existing
local tests and text review cannot substitute for that qualification.

## Coverage summary

| Promise from the brief | AC | Required cases |
|---|---|---|
| Job, triggers, exclusions, old/new wording, counts | AC-01 | V-01a–f (E/P/N/B), V-04 |
| No valid activation route or procedural obligation lost | AC-02 | V-01a–f (E/P/N/B), V-02 |
| Description-only scope, synchronized consumers, optional validation | AC-03 | V-03, V-05 |

## Source and revision

Source brief: docs/tasks/SIDE-003.2/brief.md
Source brief revision: working-tree brief read on 2026-11-03
Verification revision: 1
Authority: derived from the brief, its cited SIDE-003 plan sections, parent brief, and SIDE-003.1 baseline
Status: ready
