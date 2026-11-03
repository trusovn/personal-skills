# Task Preflight: SIDE-003.2

Status: `ready`
Profile: `guided`
standalone_preflight_value: `marginal`

Source brief: [brief.md](brief.md), working-tree revision read 2026-11-03.
Verification: [verification.md](verification.md), revision 1.
Repository: `/Users/mtrusov/work/skill-sources/personal-skills`.

The named baseline and consumer uncertainties resolved through cheap local
checks. A standalone stage is required for this package; for similar direct
edits, implementer self-preflight would suffice.

## Scope and current applicability

HEAD: `0ecbdc95c1aaeea9a36623373c65999de42a71ad`. The initial working tree
was clean. Only this task's new verification artifact was added during
preparation. No other description leaf is active. The six source skill rows
(and all other 20 rows) exactly match the saved SIDE-003.1 baseline, including
hashes and counts, using `python3 tools/baseline_measure.py`; the current
output is `/tmp/side0032-before.json`. SIDE-003.1 has an independent ACCEPT
in `../SIDE-003.1/reviews/acceptance-01.md`.

Allowed implementation: only six description scalars, the SIDE-003.2 section
of `../SIDE-003/description-results.md`, and any owning assertion that quotes
changed description text. Preparation and independent review artifacts belong
in this package. Bodies, names, paths, active installation, baseline, plan,
and unrelated files stay unchanged. Stop on overlapping writers, stale
baseline, changed authority, or scope expansion.

## Decision context

Authority: brief and SIDE-003 plan Description design, boundary groups 1–2,
phase 2, and measurement layer 1. The owner wants lower catalog cost while
preserving valid activation routes. The consumers are catalog selection and
whole-package installation. Wrong routing is the main risk; preserve all
routes even above the advisory length range, record omitted detail's existing
body authority, and leave model routing qualification pending. The contract
index points to body declarations; none moves here. No deferral is needed.

## Acceptance evidence and feasibility

| AC / cases | Setup, oracle, and exact local check | Readiness result |
|---|---|---|
| AC-01/02, V-01a–f E/P/N/B | Compare complete old descriptions and the plan group rows with each candidate; record every trigger and exclusion in results. All 24 future routing inputs are in verification revision 1. | Editorial evidence feasible. Live runs not authorized; pending qualification is permitted by the brief. |
| AC-02, V-02 | Inspect the six read-only bodies for each removed detail; retain and flag anything absent. | Existing bodies accessible; no body edits permitted. |
| AC-03, V-03 | Compare Git originals and candidate bytes with description replaced by a sentinel; inspect `git diff --stat` and `git diff -- skills`. | Git/Python available, initial tree clean. Planned check has not run on candidate bytes. |
| AC-01, V-04 | `python3 tools/baseline_measure.py`; sum the six deltas against all-26/profile-20 totals; unchanged body bytes. | Baseline reproduces 14,448/10,809 description characters and 388,640/320,123 body bytes. |
| AC-03, V-05 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py`; validator for all six packages. | Installer assertion at line 404 quotes `coding agents will develop or maintain`, currently description-only. Preserve this wording or synchronize that assertion. PyYAML imports successfully. |
| Required gates | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py`; `python3 tools/check_contracts.py --root .` | Cheap local checks feasible. SIDE-003.18 owns aggregate verification. |

Installer constants, managed profile guide, and installation README were
inspected. They select/copy whole packages and do not quote the descriptions;
no synchronization change is needed there. Shared runtime is unchanged.
Installed run-evidence helper set exists; availability reports available from
`.agents/scripts/`, so use that installation only. Do not refresh it.

## Warnings and next action

No blocking condition. No dependency install, external reviewer, live eval,
commit, or network operation is required. The separately approved live-eval
budget remains absent. No tokenizer or observed session saving is claimed.

Implementer handoff: consume verification revision 1, recheck these material
facts, edit only the allowed descriptions, record V-01–V-05 evidence and
measurements, then submit READY_FOR_REVIEW. After implementation checks,
the coordinator starts fresh independent task-review-discovery and then a
separate task-acceptance-review decision. No maintainability or registry-update
stage applies to description-only edits with unchanged body authorities.
