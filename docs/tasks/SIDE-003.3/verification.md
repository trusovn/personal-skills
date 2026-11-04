# Verification Design: SIDE-003.3 — Boundary groups 3–4

Shorten five discovery descriptions while preserving their activation routes,
neighbor distinctions, exclusions, and every non-description byte.

## Shared setup

Use the five source packages named in [brief.md](brief.md), the SIDE-003 plan
boundary rows 3–4, and the saved SIDE-003.1 measurement record. Capture the
current measurement before edits. Existing SIDE-003.2 changes are the current
catalog starting point; they must remain unchanged.

## Cases

### V-01 — Preserve each routing boundary

For each row below, compare old/new wording and record an editorial checklist
in the results. Each row has four independently identified variants: E (explicit
invocation), P (implicit positive), N (negative), and B (nearest neighbor).
E uses “Use $<skill-name> for its stated job”; it must retain that identity and
job. P/N/B use the exact prompts below. No model execution is implied by review.

| Case / skill | P prompt and expected route | N prompt and expected exclusion | B prompt and expected neighbor |
|---|---|---|---|
| V-01a project-delivery-plan | Foundation is ready. Plan the flows and task inputs/outputs for several tasks that must compose. → delivery plan | Implement the checkout feature. → no activation | Independently check this existing lightweight plan. → plan verification |
| V-01b project-plan-verification | Independently check completeness and task composition of this equivalent lightweight plan before implementation. → fresh plan reviewer | Repair the plan or implement features. → no authoring | Create the system plan and task map. → delivery plan |
| V-01c task-brief-designer | Tighten this issue into an implementation-ready task, define acceptance/verification, assess splitting, and prepare a handoff. → task contract design | Decide unresolved product architecture or certify current execution readiness. → no decision/readiness certification | Derive concrete evidence scenarios from this ready brief. → verification designer |
| V-01d task-verification-designer | Derive verification for this executable package; also assess an unpackaged edit with non-obvious lifecycle/failure cases. → scenario/evidence design | Write production code/tests or redesign requirements. → no implementation/redesign | Check current commands, ownership and execution prerequisites. → preflight |
| V-01e task-preflight | Readiness-check this bounded task, resolve commands and ownership, and prepare an execution packet. → current readiness check | Implement the task or redesign requirements. → no implementation/redesign | Repair this task contract. → brief designer |

Expected result: every old activation route remains available, including issue,
request, approved plan/specification/existing brief inputs; conditional splitting;
equivalent lightweight plans; packaged and appropriate direct-request verification;
and guided/high-assurance readiness. Removed procedures must be mapped to existing
body sections, or retained and flagged. Review each complete original description,
not just these representative prompts (AC-01, AC-02).

Live routing, if separately approved: give a fresh model only the relevant catalog
for each prompt, ask for selected skill and reason, and record E/P/N/B separately
against these expected routes. Do not load bodies before selection. No live routing
budget is approved by this artifact; pending cases are not behavioral passes.

### V-02 — Keep all non-description bytes

Compare each changed package to Git HEAD after replacing only its description
scalar with a sentinel. Expect byte-identical results, exactly five changed skill
paths, unchanged names/paths and no changes to other packages. Inspect the diff.
This is the decisive negative oracle for editorial changes; fail-first functional
tests are infeasible (AC-03).

### V-03 — Measure the exact catalog reduction

Run `python3 tools/baseline_measure.py` before and after. Expect 26 source and
20 profile entries; all body bytes unchanged; the all/profile character reductions
equal the sum of the five per-skill reductions. Explain prior accepted baseline
deltas separately. Record old/new text, counts and totals in this leaf's results
section without modifying the saved baseline (AC-01, AC-03).

### V-04 — Preserve owning consumers

Inspect existing preparation-contract and flow-guide assertions before editing.
Run both suites after edits. Update an assertion only if it actually quotes a
changed description. Inspect the canonical installer, profile guide, shared-file
list, tests and README; expect no identity or distribution change. Run optional
`quick_validate.py` on each package with existing PyYAML, or record its absence.
These checks prove local text/package consistency, not model routing (AC-03).

## Coverage and gate ownership

| AC | Cases |
|---|---|
| AC-01 | V-01a–e E/P/N/B; V-03 |
| AC-02 | V-01a–e E/P/N/B and removed-detail body map |
| AC-03 | V-02, V-03, V-04 |

Implementer owns local checks, required architecture/contract checks and results.
Fresh independent discovery corroborates all cases; a separate acceptance reviewer
owns the decision. No maintainability or registry stage is needed for metadata-only
edits with no changed registered authority. SIDE-003.18 owns the aggregate gate.
Live routing remains pending separate budget approval.

## Source and revision

Source brief: docs/tasks/SIDE-003.3/brief.md
Source brief revision: Git HEAD 2504f1f (unchanged task brief)
Verification revision: 1
Authority: derived from brief AC-01–03 and cited SIDE-003 plan/baseline
Status: ready
