# Task Preflight: SIDE-003.3

Status: ready
Profile: guided
standalone_preflight_value: marginal

## Readiness summary

Source brief: docs/tasks/SIDE-003.3/brief.md, HEAD 2504f1f (unchanged).
Verification: docs/tasks/SIDE-003.3/verification.md, revision 1.
Repository: /Users/mtrusov/work/skill-sources/personal-skills.

Initial Git status was clean. Only this invocation's verification artifact now
exists. No other active description writer is declared. The five source rows
match SIDE-003.1 exactly, including hashes. The baseline script and machine
record are unchanged since 0ecbdc9. Current totals reflect the accepted .2 leaf:
13,030 all-26 and 9,391 profile-20 description characters. The saved baseline
is current for the five unchanged target packages; prior .2 deltas are expected.

Scope: only the five brief-named description scalars and this leaf's section in
SIDE-003/description-results.md, with separate preparation/review artifacts.
Bodies, identities, paths, other descriptions and the saved baseline stay fixed.

## Decision context and current applicability

Authority: brief AC-01–03, SIDE-003 plan description groups 3–4, and parent brief.
Priority: preserve routing over achieving the 150–300 character starting range.
The consumer is the source discovery catalog; installed copies stay unchanged.
The contract index identifies no description scalar as registered authority.
No maintainability stage is applicable to metadata-only changes. Registry
synchronization is unnecessary unless bodies/declared contracts change.

The standalone stage was routine: baseline/capabilities and text consumers can
be checked cheaply. Recommend the same compact mandatory package preparation
for similar leaves, without broader baseline or environment provisioning.

## Acceptance evidence and feasibility

| Cases / AC | Setup and oracle | Command / feasibility |
|---|---|---|
| V-01a–e E/P/N/B; AC-01/02 | Compare full old descriptions and group rows; preserve job/positive routes/exclusions; map removed details to bodies | Local editorial review and results table; all authorities available. Live fresh-model routing is designed, pending separate approval. |
| V-02; AC-03 | Git HEAD originals; replace only description with a sentinel; expect identical remaining bytes and exactly five changed skill paths | Python byte comparison plus targeted Git diff; local tools available. |
| V-03; AC-01/03 | Before JSON is /tmp/side0033-before.json; recompute totals; expect body invariance and reduction equal to five per-skill deltas | python3 tools/baseline_measure.py; baseline successfully reproduced for targets. |
| V-04; AC-03 | Existing assertions and package paths; unchanged consumer expectations | PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_task_preparation_contracts.py; then test_task_flow_guides.py. Python/Git available; no download required. |
| V-04; AC-03 | Five package frontmatters | python3 skills/skill-creator/scripts/quick_validate.py <package>; PyYAML already available. Structural evidence only. |

The preparation suite checks `implementation-neutral` in verification-designer's
entry; preserve that wording. The other apparent description match, `A supplied
executable task package always requires`, checks brief-designer's unchanged body.
No assertion edit is needed. The flow-guide suite quotes no changed scalar.
Installer constants, shared-file list, profile guide and README use unchanged
package identities and whole-package copying; no distribution edits are needed.

Required final checks: architecture unittest command from AGENTS.md and
python3 tools/check_contracts.py --root .; local and feasible. Aggregate verification
belongs to SIDE-003.18. Fail-first is infeasible for editorial compression; byte
preservation and full boundary review provide the negative oracles.

## Limits, stops, and next action

No blocker. Do not refresh installations or run live routing without separate
approval. Stop on concurrent description ownership, a material baseline mismatch,
new authority ambiguity, or a need to alter bodies/contracts. Expected description
and report edits do not invalidate this readiness.

Next: implement the five scalars, record results, run local checks, then fresh
independent task-review-discovery and a separate task-acceptance-review decision.
