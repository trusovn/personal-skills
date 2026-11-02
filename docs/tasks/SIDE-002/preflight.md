# SIDE-002 preflight

Status: `ready`  
Profile: guided  
standalone_preflight_value: material

## Readiness and applicability

Source brief: `docs/tasks/SIDE-002/brief.md`, SHA-256
`f92313465887e2aa977056f54991bdb76bcf28e2771c42fe2a4e8eb8f6debdb5`.
Verification: `verification.md`, revision 1; its singular source declaration
resolves to this brief and its source revision matches the current bytes.

Scope is the brief's allowed source skill packages and stale downstream
assumptions, with installer changes only if resources/references change. The
staged brief is pre-existing user work; preserve it. At inspection the only
other dirty path was the newly authored verification document. Neither overlaps
implementation source. This invocation writes only this preflight.

The standalone stage resolved the named consumer and presentation uncertainties:
SIDE-001's results, current verification-designer instructions, its evals and
preparation-contract tests agree on readable cases, methods beside cases, then
coverage and singular source/revision metadata. Preserve these. Preflight and
implementer consume packaged verification; discovery and acceptance already
reason about material obligations rather than a fixed heading inventory. The
brief template and finite-risk eval still require the six-field risk format;
these are intended change targets, not missing prerequisites. Consumer wording
about finite rows must become conditional without losing coverage.

The installer already selects both changed skills and copies package resources.
No new runtime dependency or profile member is expected. Installation and
foundation-tool contracts were inspected through `docs/contracts/index.json`;
their registered authority need not change for editorial output contracts alone.
Reassess if implementation changes a registered surface.

## Decision context

The owner needs readable contracts that preserve requirements through verification,
implementation and independent review. Loss of a refusal, legal state, audit
obligation or stage owner is a material failure even if a document is shorter.
The brief and its cited historical T-001.3 examples govern the design; examples
are read-only. SIDE-001 governs verification presentation. Repository placement
and checks follow `docs/project-map.md` and `docs/development.md`.

Assumption: worked outputs are illustrative source-guided reviews, not generated
skill qualification. No provider/model evaluation is needed or authorized here.
Finite-risk fixture observer uncertainty concerns the hypothetical implementation
task; SIDE-002 must preserve that uncertainty and its preparation route, not
implement an observer. No decision-critical gap remains for this documentation
change. Recommend standalone preflight again when consumer boundaries or dirty
ownership are uncertain, rather than for routine single-template edits.

## Coverage and feasibility

All commands below use the repository root. No baseline test was needed: source,
fixtures and standard-library test entry points are present; future changed
behavior is not claimed to pass.

| AC / scenario | Authority, setup and decisive oracle | Feasibility and planned proof |
|---|---|---|
| AC-01–03 / V-01 | Existing verification-designer small API fixture retains nonblank success, `blank_display_name` refusal and unchanged stored name. Compare a source-guided pair with those obligations and one authoritative home per fact; no risk section is required. | Fixture exists in `task-verification-designer/evals/files/setup_fixture.py`; local document review is feasible. Owning structural tests use C1/C2 below. Pair not yet produced. |
| AC-01–04,06 / V-02 | Brief-designer eval 5, `finite-risk-matrix`, and its `EVD-12` authority define five evidence families, four ordered publications, five legal prefixes and four named orphan states. Map every exact value to acceptance or precise authority and identifiable verification cases. Preserve pre-side-effect refusal, byte reuse, next-stage publication, targeted-first corrections and final reviewer aggregate ownership. | Fixture and existing eval expectations exist. Revise existing expectations rather than replace distinct obligations. Source-guided pair and mapping are feasible; no actual resume runtime or observer execution is required. C1/C2 protect source contracts only. |
| AC-05–06 / V-03 | Trace both pairs into preflight, implementer, discovery and acceptance. Check package preparation, four launch keys, sizing, conditional stages and separate fresh discovery/acceptance through precise shared references. Preserve SIDE-001 presentation and metadata. | All four source consumers and templates exist. Focused stale-assumption edits and a consumer/input map are in scope. C1/C2 plus document review; not yet run. |
| AC-01,05–06 / V-04a | Existing brief-designer split-task fixture supplies TASK-40 boundaries. Inspect parent plus every child/verification pair for coverage, producer ownership, dependencies, independent sizing and integration-proof ownership. | Existing fixture and sizing/package tests available. Source-guided output review is feasible without changing thresholds or runtime policy. C1/C2; not yet run. |
| AC-01–02,05–06 / V-04b | Existing `queue-runner` high-assurance fixture supplies public `runner run-next`, persisted state and repeated-selection obligations. Preserve exact provenance/freshness and applicable machine/audit requirements in the pair. | Existing fixture and high-assurance template guidance exist. Local worked review is feasible; no live runner/model execution. C1/C2; not yet run. |
| AC-04 / V-05 | Contrast complete no-risk small task with verification-designer ambiguous-retention fixture. Complete authority permits derivation; missing deletion policy must route to its owner and preserve existing artifact. | Both fixtures and eval expectations exist. Preserve refusal/preservation cases; do not invent retention rules. Source-guided outcome review plus C1; not yet run. |
| AC-06 / V-06 | Inspect instructions, templates, examples, completion checks and eval expectations; compare installer-managed membership/resources and registry authority. Existing artifacts and active install remain unchanged. | C1/C2 first, C3 if affected, then C4. C5/C6 may be covered by current aggregate evidence. Commands are local; no dependencies or provider credentials needed. Expected active-install drift must be reported, never repaired during this run. |

Planned exact commands, narrowest first:

```sh
# C1: owning cross-skill structural contracts
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_task_preparation_contracts.py
# C2: skill package resources
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-implementation-flow/task-brief-designer/tests -p 'test_*.py'
# C3: installer coverage, if affected
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py
# C4: required cross-skill aggregate; report skips/failures and drift
python3 tools/verify.py
# C5/C6: required final architecture/contracts, unless current aggregate covers them
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py
python3 tools/check_contracts.py --root .
```

A zero exit with reported assertions supports structural/local regression claims
only. Worked-output obligation maps provide document evidence; neither proves
model compliance. C4 can encounter host containment restrictions or installed
drift. Report these precisely and use the approved escalation path for an
execution denial; do not refresh the active install. No checks ran at preflight.

## Stops and implementer handoff

No blocker. Stop for a new authority decision, lost assurance boundary, changes
outside allowed scope, or a need to rewrite historical task artifacts. Any
material source/verification revision or ownership change requires focused
readiness reconsideration. No live or expensive checks without approval.

> Implementer handoff: Read SIDE-002 brief and verification revision 1, preserve
> the staged brief and historical task artifacts, and implement editable source
> only. Start with existing six-field requirements and owning coverage; maintain
> SIDE-001 cases/metadata. Produce simple, finite-risk, split and high-assurance
> source-guided paired outputs with obligation and consumer maps. Run C1 then C2,
> applicable C3, and C4; report C5/C6 coverage, skips, drift and unqualified model
> behavior. Keep any applicable maintainability/registry stages, then fresh
> independent discovery and a separate acceptance decision. Exact next action:
> invoke bounded-task-implementer against this ready package.
