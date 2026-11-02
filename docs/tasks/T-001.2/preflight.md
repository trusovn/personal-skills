# T-001.2 preflight

Status: **ready**

## Readiness summary

- Profile: guided. Standalone preflight value: **material**; it resolved the
  accepted dependency and availability of the actual pinned interpreter and
  analyzers, which the real-boundary scenarios require.
- Authority: [brief](brief.md), status ready, SHA-256
  `4163de695ba4b43c16f15ba3ef7b1de4e37068c5956331c7f0a08d6068451f38`;
  [verification](verification.md), revision 1, declares that same brief and
  revision. Its scenarios are derived guidance, not independent authority.
- Dependency: [T-001.1 acceptance](../T-001.1/reviews/acceptance-01.md)
  is ACCEPT. [Measurement contract](../../contracts/measurement.json) records
  the current partial IF-001 and invariants; [installation contract](../../contracts/installation.json)
  governs distribution. The brief links the parent direction and plan.
- Scope: measurement adapter under `scripts/`, relevant
  `tests/test_maintainability.py` cases and `scripts/measure-maintainability.md`;
  inspect installer and profile references and synchronize only stale references.
  Registry synchronization is a separate designated post-implementation stage.
- Ownership: initial status showed untracked `docs/tasks/SIDE-001/` and
  `docs/tasks/T-001.2/verification.md`; preserve both. No existing dirty source
  or test path overlaps the allowed implementation scope. This packet is new.
- Applicability: valid for the current brief and verification revision and the
  stated dependency, ownership and capabilities. Reassess material changes to
  those facts or revised verification before implementing.

## Decision context

The CLI supplies advisory evidence to later T-002/T-003 workflows. A false
numeric history, silent format conversion or overwritten pre-edit evidence can
mislead those consumers. Keep native unknowns, captured folder coverage and
original reports; hashes provide provenance, not tamper resistance. T-001.3
owns aggregate installed composition. No new product decision is delegated to
preflight; the exact new format number remains an implementation choice.

## Acceptance evidence and feasibility

All commands below run from the repository root. Existing tests and fixture
conventions in `tests/test_maintainability.py` exercise real CLI, analyzer,
filesystem and Git boundaries. Future task-owned cases have not run. No network
or installation is needed: the accepted environment's Python 3.14.6 imports
Radon 6.0.1 and Ruff 0.14.2, matching the pinned runtime. The existing adapter
contains format 4 and old labels; existing tests assert them, providing a
fail-first starting point. The worktree and temporary Git fixtures are available
within the normal local test environment.

| Authority and scenarios | Required decisive observation and feasibility |
|---|---|
| AC-01, R-03; V-01a–q, V-02a–e, V-04 | Known native counts and matched identities yield factual signed changes, distinct threshold/interpretation labels, saved JSON/text and console, with successful CLI exit. Extend existing native and output cases; demonstrate changed label assertions fail before correction. |
| AC-02, R-03; V-05a–j, V-10 | Real CLI refuses independently seeded incompatible format, tools, settings, scope and incomplete evidence; compatible controls succeed. Documentation review specifies safe pre-edit recovery and checks installer references. |
| AC-03, R-04; V-06, V-07a–d | Disposable existing empty folder baseline, two real edits and original saved baseline prove covered absence; ordinary empty measure, missing/excluded paths and uncovered additions fail. Existing filesystem fixtures can be extended. |
| AC-04, R-03/R-04; V-02a–e, V-03a–i, V-08 | Real native exemptions and unknown transitions, symbol identity and real dirty Git capture/subset/deletion retain correct before evidence. Existing analyzer and Git fixture patterns provide the boundary. |
| AC-05, R-04; V-06, V-08, V-09a–f | Compare real source/index and prior report bytes; each JSON or sibling-text collision fails without creating or overwriting its sibling. Existing no-overwrite and snapshot cases provide starting coverage. |

Run changed cases first, then the owning suite:

```sh
.quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python -B -m unittest discover -s tests -p test_maintainability.py
```

Oracle: all required scenarios pass with real pinned analyzers and no analyzer
skips; inspect outputs and preservation bytes as specified in verification.
Neither this suite nor the future scenarios ran in preflight. Run installer
tests if managed references change; run architecture and contract checks before
handoff. Current architecture check passed 4 tests and contract check passed
with 6 subsystems; these are structural checks, not behavioral qualification.

## Stops and next action

Stop for material policy changes, unsupported recovery evidence, arbitrary empty
success, unavailable real boundaries, overlapping user work, or a changed
authority requiring redesign. Do not install dependencies or run live checks
without applicable authorization. Preserve separate independent discovery and
acceptance stages after implementation. Standalone preflight is recommended for
similar tasks that depend on an accepted external runtime and real analyzers.

## Implementer handoff

Implement T-001.2 under `brief.md` and `verification.md` revision 1, preserving
the untracked user artifacts identified above. Use the pinned Python and owning
suite command above; add focused fail-first and real-boundary evidence for every
V-01–V-10 case, then apply the required review and registry stages. Begin with
existing measurement tests and adapter; stop on the conditions above.
