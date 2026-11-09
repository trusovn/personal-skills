# Verification Design: T-005 — Installed handoff

The installed CLI must preserve one original baseline through two edits and
separate implementer/reviewer invocations. Native failure remains binding.

## Cases

- V-01 (AC-01): Install in a disposable Git target, remove its distribution,
  prepare local pinned dependencies without downloads, and invoke from unrelated
  cwd. Capture B, edit, compare I, compare R separately, correct, compare C to B.
  Assert exact JSON/text paths, complete status, compatible tool/settings/scope,
  actual source hashes, distinct invocations and expected 5 → 7 → 6 complexity.
- V-02 (AC-02): Start staged/unstaged/untracked. At every CLI/native boundary
  compare source and real index bytes; permit only explicit edits and evidence
  writes. Preserve every prior report pair. Reuse owning settings, unknown-value,
  collision, empty/add/delete and incompatible/unavailable cases in the full suite.
- V-03 (AC-03): Declare whole-project required Ruff F401 policy and implementer
  owner. Edited input must fail F401 while comparison succeeds. Correction must
  pass the same command. Retain both outputs with checked hashes and producer.
- V-04 (AC-04): Inspect and execute existing implementer/reviewer fixture
  checkers. Map plan V-001–V-008 to owning tests and prepared actor cases.
  Preserve below-target, cohesive breach, touched legacy/untouched sibling,
  misleading extraction, missing/incompatible advisory/required, correction,
  conditional re-entry, native recovery/reuse/no-check variants. Setup success
  proves preparation only. Fresh actors and independent diff/history grading
  remain separately authorized.
- V-05 (AC-05): Save focused, architecture, contracts and aggregate logs.
  Report actual failures/skips, interpreter/pins and proof limits in results.
  Active drift stays a failed diagnostic; never refresh this active profile.

## Coverage and responsibility

V-01–03 use real filesystem/Git/process boundaries; syntax alone is insufficient.
V-04 separates deterministic setup from unrun agent judgment. V-05 records
implementation evidence. Fresh maintainability, registry updater, discovery and
separate acceptance own independent corroboration after submission.

Source brief: brief.md
Source brief revision: initial working-tree brief, 2026-11-04
Verification revision: 1
Authority: derived from brief and project-plan section 11
Status: ready
