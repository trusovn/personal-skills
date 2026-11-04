# Verification Design: SIDE-003.4 — Boundary groups 5–6

Shorten the five discovery descriptions of plan boundary groups 5–6 while
preserving every activation route, group distinction, exclusion, and every
non-description byte. The five descriptions are the only changed source bytes.

## Shared setup

Use the five source packages named in [brief.md](brief.md) —
bounded-task-implementer, task-maintainability-review,
task-contract-registry-updater, task-review-discovery, task-acceptance-review
(all under `skills/task-implementation-flow/`) — the SIDE-003 plan boundary
rows 5–6, and the saved SIDE-003.1 measurement record. Capture
`python3 tools/baseline_measure.py` output before edits (family convention:
`/tmp/side0034-before.json`) and confirm the five rows still equal the frozen
baseline rows, including SHA-256. Current counts: 515 / 640 / 279 / 494 / 599
characters, sum 2,527; running totals all-26 = 11,815 and profile-20 = 8,176
description characters; body bytes 388,640 / 320,123. A missing or stale
baseline stops work. Existing SIDE-003.2 and SIDE-003.3 results are the current
catalog starting point; they must remain unchanged. Serialize with any other
active description leaf. One of the five scalars (task-maintainability-review)
uses folded `>` frontmatter; masks and measurement must cover the whole folded
block.

## Cases

### V-01 — Preserve each routing boundary

For each row, compare old/new wording and record an editorial checklist in the
results. `E` (explicit invocation) uses “Use $<skill-name> for its stated job”
and must retain that identity and job; record E results separately from the
implicit variants. P/N/B use the exact prompts below; V-01a adds the distinct
machine-contract variant M defined after the table. No model execution is
implied by review.

| Case / skill | P prompt and expected route | N prompt and expected exclusion | B prompt and expected neighbor |
|---|---|---|---|
| V-01a bounded-task-implementer | Execute this ready bounded task: apply the change, add the missing tests, verify progressively, preserve my uncommitted work, and report evidence. → implementer, guided default (a ready package alone stays guided) | Redesign this product's overall architecture across every module. → no activation (not one bounded task) | Repository policy requires an independent maintainability/architecture review of the changed implementation assets before functional acceptance. → task-maintainability-review |
| V-01b task-maintainability-review | After this bounded task's implementation, repository policy requires a focused maintainability review of the changed assets, including the new test harness, before functional acceptance. → maintainability review | Perform the full specification/functional acceptance decision for this submitted bounded task. → no activation (explicit exclusion; functional acceptance belongs elsewhere) | Implement this bounded task: apply the change, add tests, verify, and report evidence. → bounded-task-implementer |
| V-01c task-contract-registry-updater | This bounded implementation passed structural and maintainability review and may have changed a durable cross-task contract; before acceptance, update the current-state contract registry and stale discovery references. → registry updater | Register the planned capability and its subsystem record now, before anything is implemented. → no activation (current-state synchronization only; never planned capability) | A fresh session, independent of production authorship, must gather and publish the current review evidence for this bounded implementation; no verdict. → task-review-discovery |
| V-01d task-review-discovery | A fresh session independent of production authorship must gather review evidence for this bounded implementation, which crosses public API and recovery boundaries; publish confirmed findings without deciding acceptance. → discovery | Issue the final ACCEPT or CHANGES_REQUESTED verdict for this bounded implementation yourself. → no activation (never decides acceptance) | The independent evidence report is published; decide whether this bounded implementation is safe to advance. → task-acceptance-review |
| V-01e task-acceptance-review | The independent discovery report is published for this bounded implementation. Decide whether it is safe to advance and return the verdict. → acceptance review, concise guided decision | Re-probe the repository and gather new evidence before deciding this bounded implementation. → no activation (admits current evidence; new evidence belongs to discovery) | Before the acceptance decision, update the current-state contract registry for the durable contracts this implementation changed. → task-contract-registry-updater |

**V-01a-M — supplied machine contract without a high-assurance request.**
An orchestrated caller supplies a ready task packet plus a machine output
contract (worker-result JSON schema with a durable result path); the request
never says “high-assurance”. The implementer's strict-freshness/raw-JSON
high-assurance route must still activate through the supplied contract, and the
compressed description must keep that route visible by naming supplied machine
contracts (or equivalent) — wording that only says “explicitly requested
high-assurance” fails this case (AC-02). The current body already holds the
route in “Choose the profile”; no body edit is allowed or needed here — the
obligation is description visibility only.

Expected result: every old activation route remains available, including
request/brief/packet inputs; execute, resume, and correct; guided default;
the supplied-machine-contract high-assurance route (V-01a-M); the
policy-or-explicit-request review trigger; after-structural-review
synchronization timing; fresh-session independence; discovery-without-verdict;
and decision-after-discovery with guided/high-assurance profiles. Group 5
retains authoring scoped implementation vs independent structural review when
policy or the user requires it. Group 6 retains synchronizing current contracts
vs independent evidence without a verdict vs a separate acceptance decision
after discovery (AC-01, AC-02).

Beyond the representative prompts, each skill has a full-description case
V-01a-FULL … V-01e-FULL: review the complete original description clause by
clause and require every trigger, input, and exclusion to remain discoverable
in the candidate. Trigger preservation, not length, is the oracle — the
SIDE-003.3 F-01 correction shows a representative-prompt check alone can miss a
silently dropped trigger. Procedural detail removed from a description must be
already present in that skill's body (for example: implementer — “Choose the
profile”, “High-assurance additions”, “Correct at the invariant level”;
maintainability — “Review contract”, Protocol steps, “Independence”;
registry-updater — “What belongs in the registry”, “Hard boundaries”;
discovery — “Discovery workflow”, “Output contract”; acceptance — “Choose the
profile”, “Verdict and routing rules”) or kept in place and flagged in the
results — never silently dropped (AC-02). The 150–300-character range is an
editorial starting point: a per-skill light edit or no-op is acceptable where
the current wording already preserves routing (task-contract-registry-updater
at 279 characters is already in range); never narrow activation to hit the
range.

Live routing, if separately approved: give a fresh model only the relevant
catalog (names plus descriptions, identical unrelated entries, no bodies) for
each prompt, ask for the selected skill and reason, and record E, P, N, B and
V-01a-M separately; record the implementer's explicit high-assurance invocation
as its own input, distinct from V-01a-M, per the brief's broader-gate row. No
live routing budget is approved by this artifact; pending cases are not
behavioral passes.

### V-02 — Keep all non-description bytes

Compare each changed package to Git HEAD `b7b3337` after replacing only its
description scalar with a sentinel (for task-maintainability-review, mask the
entire folded `>` block). Expect byte-identical remainders, exactly five
changed skill paths under `skills/`, unchanged names/folder paths/invocation
identities, and no changes to other packages, references, installer, tests, or
prior results beyond this leaf's results section and preparation artifacts.
Inspect `git diff --stat` plus the targeted diff per file. This is the decisive
negative oracle for editorial changes; fail-first functional tests are
infeasible (AC-03).

### V-03 — Measure the exact catalog reduction

Run `python3 tools/baseline_measure.py` before and after. Expect 26 source and
20 profile entries; all body bytes unchanged at 388,640 / 320,123; the all-26
and profile-20 character reductions each equal the sum of the five per-skill
reductions (all five are profile skills, so both totals move by the same
amount); the other 21 rows unchanged, including the accepted SIDE-003.2 and
SIDE-003.3 descriptions. Record old/new wording, per-skill counts, and catalog
deltas in this leaf's results section without modifying the saved baseline
record or measurement tool. Counts are normalized description characters, not
tokens, rendered catalog visibility, or session savings (AC-01, AC-03).

### V-04 — Preserve owning consumers

Re-verify editorially, before and after edits, that no owning assertion quotes
changed description text: inspect the suites that read these five skills —
`tests/test_bounded_task_implementer.py`,
`tests/test_task_maintainability_review.py`, `tests/test_review_composition.py`,
`tests/test_task_review_discovery.py`, `tests/review_fixture_support.py`,
`tests/test_run_evidence_availability.py`,
`tests/test_task_acceptance_review.py`, and the remaining prerequisites-map
suites below. The prior ~450-literal scan found no description-only literal;
only “preflight” (implementer) and “acceptance decision call” (discovery)
overlap a description, and both also appear in the unchanged bodies. Sync an
assertion only if it truly quotes changed description text.

After edits, run the union of the five skills' focused suites from the
SIDE-003.1 prerequisites map:
`test_bounded_task_implementer.py`, `test_run_evidence.py`,
`test_run_evidence_availability.py`, `test_maintainability.py`,
`test_review_composition.py`, `test_task_preparation_contracts.py`,
`test_task_flow_guides.py`, `test_task_maintainability_review.py`,
`test_task_review_discovery.py`, `test_task_acceptance_review.py`,
`test_contextual_export_risks.py`, `test_contextual_known_issues.py`,
`test_contextual_uncertainty_inputs.py`
(each as `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p <pattern>`).
Run optional `python3 skills/skill-creator/scripts/quick_validate.py <package>`
on the five packages with the available PyYAML, or record the skip. Finish with
the required checks `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py`
and `python3 tools/check_contracts.py --root .`. These prove local
text/package consistency, not model routing (AC-03).

## Coverage and gate ownership

| AC | Cases |
|---|---|
| AC-01 | V-01a–e (E/P/N/B, M for V-01a, FULL per skill); V-03 |
| AC-02 | V-01a-M; V-01a–e B neighbor distinctions; V-01a–e-FULL and the removed-detail body map |
| AC-03 | V-02, V-03, V-04 |

Implementer owns local checks, required architecture/contract checks, and the
results section. Fresh independent task-review-discovery corroborates all
cases; a separate task-acceptance-review owns the decision. No maintainability
stage applies (no implementation assets change) and no registry stage applies
(the brief's expected contract impact is none: descriptions are not registered
contract authority, and `implementer-feedback.json` declarations cite the
implementer's body and evals, which this leaf does not touch). SIDE-003.18 owns
the aggregate `python3 tools/verify.py` gate and distribution qualification.
Live fresh-model routing remains pending separate budget approval.

## Source and revision

Source brief: docs/tasks/SIDE-003.4/brief.md
Source brief revision: Git HEAD b7b3337 (unchanged task brief)
Verification revision: 1
Authority: derived from brief AC-01–03 and cited SIDE-003 plan/baseline
Status: ready