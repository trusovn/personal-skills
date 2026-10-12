# T-004.2 Results — Add explicit read-only development-profile checking

Status: implemented and corrected after three independent discovery passes;
submission state `READY_FOR_REVIEW`. This file records the implementer's
submission evidence for the completed bytes; each correction was applied in a
separate invocation from the original implementation. No independent review
has accepted these bytes. Created per the repository rule that finished tasks
write results next to their plan documents (the `bounded-task-implementer`
skill itself does not mandate a document).

Provenance: one session authored the original production, test, and guidance
bytes; later separate sessions authored the F-01, F-02, and F-03 correction
bytes. Everything here is submission evidence, not an acceptance verdict.

## Contract structure (audit)

- Authority: `docs/tasks/T-004.2/brief.md` (SHA-256
  `ecf57bb5cb33dda3405269c3f6adf05628248d2a4510fe34358d98d8e027512e`),
  derived `verification.md` (V-01–V-07, revision 1, SHA-256
  `4966f69350e20d8563532d172e26acb6a8536e0c64635a62be0fb11f393c24b8`) and
  ready `preflight.md` (SHA-256
  `8f8af39476e7d6d7960b9f3f0e14efe766383dee54d64db784445ee882c40d1b`) in the
  same package; all three hashes re-verified current before the correction
  edit. Consumed dependency: reviewed T-004.1 output at HEAD `93cd0e4`.
- Correction contexts: `reviews/discovery-01.md` (first independent discovery,
  2026-10-12) supplied finding F-01 and the V-01–V-07 ledger;
  `reviews/discovery-02.md` (correction discovery 1, 2026-10-12) supplied
  finding F-02, the current V-01–V-07/R-01–R-03 ledger, and the reviewer
  regressions; `reviews/discovery-03.md` (correction discovery 2, 2026-10-12)
  supplied finding F-03 and the current V-01–V-07/R-01–R-03 ledger with its
  D-01–D-05 regressions. All three preparation hashes were re-verified current
  before the F-03 correction edit. All review reports were consumed read-only
  and were not edited.
- No plan, task-map, index, prior task, or review artifact was edited. No
  `docs/contracts` registry exists, so no contract-registry stage applies.
- Evidence runs: `run-20261012T191504Z-8e8f36015ec3` (original implementation,
  begin → finish `completed`);
  `run-20261012T194231Z-248cc0fff192` (F-01 correction invocation);
  `run-20261012T200339Z-e0230c6c43a0` (F-02 correction invocation, availability
  green before begin);
  `run-20261012T202141Z-d5afd6836886` (F-03 correction invocation, availability
  green, no open run, begin → finish `completed`).

## Deliverables

- `scripts/install_development_skills.py`: explicit read-only `--check` mode.
  Exit 0 = managed projection matches; exit 1 = managed drift or a missing
  installation; exit 2 = check failure (unusable source/target, required
  content that cannot be read, classified, or enumerated, malformed/ambiguous
  `AGENTS.md` markers — never a match). Success/drift prints one sorted JSON
  object on stdout with `checked`, `match`, `profile`, `source_repo`,
  `target_repo`, `compared_paths`, and `differences` entries
  `{category: changed|missing|unexpected, path}`; failures print
  `error: …` on stderr only. Positional install invocation and all existing
  ownership/refusals are unchanged.
- `scripts/install_development_skills.py` (correction): `_collect_projection_files`
  now walks managed trees with error-propagating enumeration instead of
  `Path.rglob`, which silently skipped unreadable directories. Enumeration
  denial (scandir failure) and metadata failure (stat failure, including
  dangling managed symlinks) raise precise scoped diagnostics —
  `cannot enumerate source/installed skill directory: <path>`,
  `cannot access source/installed skill directory|content: <path>` —
  and exit 2 rather than shrinking the comparison. True absence still yields
  missing-drift; transient directories are pruned before descent exactly
  like install-time copying, so unreachable transient content stays excluded.
  Both the source and installed sides use the corrected collector.
- `tests/test_install_development_skills.py`: `DevelopmentProfileCheckTests`
  (15 tests, 11 original + 4 correction: 2 for F-01, 2 for F-02) plus
  module-level `run_check`/
  snapshot/expected-projection helpers; the class-method `installed_identity`
  helper consolidated to module level (3 existing call sites updated,
  behavior unchanged). Correction additions:
  `test_check_reports_unreadable_managed_directories_as_failures` (F-01
  regression: denied expected and unexpected subtrees at the public CLI,
  repeated invocation, bytes/state restoration),
  `test_check_reports_unreadable_source_directories_as_failures` (source-side
  enumeration failure via the existing mocked-`SOURCE_REPO` pattern), and a
  dangling-managed-symlink metadata-failure case added to
  `test_check_reports_unreadable_required_content_as_failure`.
- Root `README.md` and `skills/README.md`: "Checking the installed profile"
  guidance — comparison scope, transient exclusions, result/exit semantics
  for human and subprocess callers, source resolution from the installer
  location (not caller CWD), deliberate between-invocation refresh, and no
  retained-version guarantee. Correction: the exit-2 failure description now
  states that required content that cannot be read or whose directory cannot
  be enumerated is a check failure. F-02 correction: the comparison-scope
  guidance now states that source-side enumeration follows directory symlinks
  exactly as install-time copying does and that installed trees are never
  traversed through inner symlinks.
- `scripts/install_development_skills.py` (F-02 correction):
  `_collect_projection_files` gained `follow_directory_symlinks`; source-side
  enumeration follows directory symlinks exactly as install-time
  `shutil.copytree` dereferences them, so the expected projection covers
  every file the installer materializes, including linked content. The
  installed side is unchanged and never traversed through inner symlinks;
  top-level target symlink refusals are preserved. A directory reached a
  second time (a linked or mounted cycle) fails precisely —
  `cannot enumerate … directory: <path>: directory cycle`, exit 2 — instead
  of hanging the walk.
- `tests/test_install_development_skills.py` (F-02 correction):
  `build_relocated_source_distribution` helper plus
  `test_check_covers_directory_linked_source_content_the_installer_copies`
  (real relocated-CLI install from a complete distribution containing a
  directory symlink inside a selected package → fresh check exit 0 /
  `match: true` with `compared_paths` covering the linked file; an inner
  installed symlink → exact missing drift without traversal; deletion of the
  copied linked subtree → exact missing drift) and
  `test_check_fails_precisely_on_cyclic_source_directory_symlinks`
  (relocated CLI against a self-referencing linked source package →
  exit 2, empty stdout, scoped `directory cycle` diagnostic, no created
  `.agents`).
- `scripts/install_development_skills.py` (F-03 correction):
  `_collect_projection_files` now distinguishes recursive ancestor cycles from
  independent acyclic paths to the same directory. The flat per-package
  `visited` identity set was replaced with a per-path ancestor-chain check:
  a directory fails with `directory cycle` only when its identity is one of
  its own ancestors along the walked root path; acyclic aliases — several
  links to one directory, or a link to an existing sibling directory — are
  enumerated and compared at every linked path, exactly as install-time
  `shutil.copytree` materializes them. Transient pruning, enumeration and
  metadata error propagation, target inner-symlink non-traversal, existing
  refusals, and bounded true-cycle failure are unchanged.
- `tests/test_install_development_skills.py` (F-03 correction):
  `test_check_matches_acyclic_directory_aliases_the_installer_copies`
  (real relocated-CLI install from a distribution with two links to one
  external directory plus a real `references` directory aliased by a link →
  fresh check exit 0 / `match: true` with `compared_paths` covering every
  aliased copy; repeated check identical; deleting one aliased copy → exact
  per-path missing drift, never a match through the surviving alias), and
  `CHECK_GUIDE_REQUIRED_PHRASES` now locks the documented alias semantics
  ("Acyclic directory aliases", "one of its own ancestors") in both guides.
- Root `README.md` and `skills/README.md` (F-03 correction): the
  comparison-scope guidance now states that acyclic directory aliases are
  copied by the installer and compared at every linked path, and that only a
  link closing a directory cycle back to one of its own ancestors fails with
  the `directory cycle` diagnostic and exit 2.

Actual contract impact: materialized ART-011 (the documented non-mutating
match/drift/failure interface consumed by T-004.3 and T-005) and extended
ART-009's installer CLI with `--check`. ART-010 ownership, IF-007, INV-009,
and FLOW-004 preserved. Executable contract declarations changed: none —
the extension is CLI behavior documented in prose; no schema/export
declarations exist for it.

## Exact commands and results

From the repository root (all commands `PYTHONDONTWRITEBYTECODE=1`; Python
3.14.4, non-root uid 1000 in the correction environment):

| ID | Exact command | Result |
|---|---|---|
| F | `python3 scripts/install_development_skills.py --check <target>` (fail-first, recorded in `preflight.md` at HEAD `93cd0e4`) | exit 2: `unrecognized arguments: --check` — the old missing-check behavior the targeted cases must reject |
| T | `python3 -m unittest discover -s tests -p test_install_development_skills.py -k check_` | original run: 11 tests OK (3.2s); correction rerun: 13 tests OK (3.5s), no skips |
| I | `python3 -m unittest discover -s tests -p test_install_development_skills.py` | original run: 28 tests OK (4.8s); correction rerun: 30 tests OK (5.1s) — 17 pre-existing install cases green (compatibility intact) + 13 check cases |
| RA | discovery-01 Appendix A reviewer regression, `python3 -` with the report's probe body (fixture steps byte-identical; only the observation print was made failure-tolerant because the original print assumed the defective JSON shape) | pre-fix (reviewer): denied extra → exit 0 false match; denied required directory → exit 1 wrong `missing`. Post-fix (corrected oracle): `unreadable-owned-extra` exit 2, empty stdout, `cannot enumerate installed skill directory: <path>`; `unreadable-required-directory` exit 2, same scoped diagnostic; readable contrast still exit 1 `unexpected`; restored baseline matches; fixture cleaned |
| RB | discovery-01 Appendix B sibling probe, `python3 -` with the report's probe body | V-02: exact changed/missing diagnostics for all 26 managed SKILL.md/shared-file paths; V-05: 14 symlink/wrong-type refusal cases with unchanged target/outside snapshots; V-06: all 8 result/repository combinations twice with unchanged file/Git/evidence/source snapshots; exit 0 |
| RA2 | discovery-02 Appendix A reviewer regression (F-02), `python3 -` with the report's probe body extracted by heading | `fresh-install-linked-source` exit 0, `match: true`, empty differences, `compared_paths` 87 covering the linked file; `omitted-copied-subtree` exit 1 with the exact `missing` difference `.agents/skills/project-direction/linked-reference/copied.txt`; fixtures cleaned |
| RB2 | discovery-02 Appendix B sibling probe, `python3 -` with the report's probe body (executes the discovery-01 Appendix B probe against current bytes) | exit 0: changed/missing exact diagnostics for 26 paths (20 packages, 6 shared files); 14 refusal cases with unchanged snapshots; 8 result/repository combinations twice with unchanged snapshots |
| RC2 | discovery-02 Appendix C denial-oracle regression, `python3 -` with the report's probe body | both F-01 regressions exit 2 with scoped `cannot enumerate installed skill directory` diagnostics and repeated agreement; relocated missing-source CLI exits 2 with unchanged source/target; restored baseline matches |
| T2 | `python3 -m unittest discover -s tests -p test_install_development_skills.py -k check_` | 15 tests OK (3.9s), no skips — 13 prior check cases + 2 F-02 regressions |
| I2 | `python3 -m unittest discover -s tests -p test_install_development_skills.py` | 32 tests OK (5.7s) — 17 install cases + 15 check cases |
| RA3-pre | discovery-03 Appendix A reviewer regression (F-03), `python3 -` with the report's probe body, pre-fix fail-first | two external aliases: exit 2 false `directory cycle` at the first aliased path; real directory plus `references-alias` link: exit 2 false `directory cycle` — the reviewer's finding reproduced on current bytes |
| RA3 | discovery-03 Appendix A reviewer regression (F-03), `python3 -` with the report's probe body | two acyclic aliases: exit 0, `match: true`, 88 `compared_paths`, empty differences; single-alias contrast exit 0; real-directory-plus-alias: exit 0, `match: true`, 88 paths; fixtures cleaned |
| RB3 | discovery-02 Appendix A, Appendix C and discovery-01 Appendix B replays (D-02/D-04/D-05 selector bodies), `python3 -` each | D-02: fresh linked-source exit 0/87 paths, deleted subtree exact missing; D-04: both F-01 regressions exit 2 with scoped diagnostics and repeated agreement, missing relocated source unchanged; D-05: 52 exact changed/missing mutations, 14 refusals, 8 repeated snapshot combinations — all clean |
| T3 | `python3 -m unittest discover -s tests -p test_install_development_skills.py -k check_` | 16 tests OK (4.1s), no skips — 15 prior check cases + 1 F-03 regression |
| I3 | `python3 -m unittest discover -s tests -p test_install_development_skills.py` | 33 tests OK (5.8s) — 17 install cases + 16 check cases |

No whole-repository, live-network, or model-budget gate exists for this task
(excluded by the brief).

## Correction record (discovery-01 finding F-01)

- Finding: F-01 [suggested P2] — unreadable managed directories silently
  disappeared from comparison: `Path.rglob` skipped directories it could not
  enumerate, so an unreadable unexpected subtree produced a false match and
  an unreadable expected subtree was misreported as ordinary `missing` drift.
- Broken invariant: a match requires complete managed-content comparison;
  required enumeration failures must remain distinguishable from ordinary
  missing-content drift (AC-01/02/03; R-01, R-02 / INV-009).
- Fix at the invariant level: one correction in the shared collector covering
  both sides (source and installed) and both subtree kinds (expected and
  unexpected), plus metadata-failure propagation for entries whose stat fails
  (dangling managed symlinks). No field-specific or input-specific exception;
  true absence, transient exclusions, existing refusal boundaries, and the
  documented three-result-class encoding are preserved.
- Credible sibling surfaces covered: unreadable reference/eval/setup
  subdirectories and selected-skill roots in every source or target package,
  additional owned target subtrees with no expected counterpart, unreadable
  ancestor directories (surface-level `cannot access` failure), and
  stat-failing entries. Sibling coverage retained green via Appendix B
  (52 changed/missing mutations, 14 refusals, 8 repeated read-only
  combinations).
- Ledger consumption (prior status → correction evidence → next owner):
  V-01 pass → targeted rerun (navigation only) → fresh discovery; V-02 fail
  → RA denied-extra case + new CLI regression test → fresh discovery;
  V-03 pass → targeted rerun, transient pruning mirrors copy exclusions →
  fresh discovery; V-04 pass → targeted rerun (navigation) → fresh discovery;
  V-05 fail → RA denied-references case + new directory/source/metadata tests
  → fresh discovery; V-06 pass → targeted rerun (navigation; no code-path
  change to result-class handling) → fresh discovery; V-07 pass → targeted
  rerun + guide-wording update → fresh discovery; R-01 fail → via V-01–V-04
  evidence; R-02 fail → via V-01–V-05 evidence; R-03 pass → via V-06
  evidence. No row was blocked or unchecked; prior passes were used as
  navigation context, not as acceptance evidence for corrected bytes.

## Correction record (discovery-02 finding F-02)

- Finding: F-02 [suggested P2] — install-time `shutil.copytree` dereferences
  directory symlinks inside selected source packages, while the check's
  `os.walk`-based collector (default `followlinks=False`) did not descend into
  them: a fresh installation from a distribution containing a linked source
  subtree reported its copied files as `unexpected` drift, and deleting the
  required copied subtree then reported a false `match: true` with a shrunk
  `compared_paths` count.
- Broken invariant: the expected projection must cover every file the
  canonical installer copies, under its existing distribution contract
  (AC-01, AC-02; V-01, V-02; R-01, R-02 / INV-009).
- Fix at the invariant level: one shared-collector change —
  `follow_directory_symlinks=True` on the source side of
  `_projection_differences` only — makes source enumeration follow directory
  symlinks exactly as install-time copying dereferences them. No per-path or
  per-package exception; transient pruning stays before descent, true absence
  stays missing drift, existing enumeration/metadata failures and target
  refusals are preserved, and the installed side is unchanged (never
  traversed through inner symlinks, so unsafe target shapes are never
  trusted). Revisited directories (linked or mounted cycles) fail precisely
  with the existing exit-2 failure class and a scoped `directory cycle`
  diagnostic instead of hanging the walk.
- Credible sibling surfaces covered: directory-linked reference/eval/setup
  subtrees in any selected source package (the collector change is generic
  per package; the new regression exercises project-direction and the
  fresh-install/missing oracles cover the generic behavior), cyclic linked
  source directories (dedicated regression), transient-named linked
  directories (pruned before following, existing transient test), and inner
  installed symlinks (contrast step: expected real files report missing
  drift, no traversal).
- Ledger consumption (prior status → correction evidence → next owner):
  V-01 fail F-02 → linked-source fresh-install match and deletion missing
  regression (RA2, new test) → fresh discovery; V-02 fail F-02 → same linked
  coverage plus family/sibling probes (RB2, targeted rerun) → fresh
  discovery; V-03 pass → transient-pruning navigation, targeted rerun →
  fresh discovery; V-04 pass → marker navigation, targeted rerun → fresh
  discovery; V-05 pass → RC2 denial oracles green, no refusal change →
  fresh discovery; V-06 pass → reads-only change, snapshot rows rerun via
  RB2 → fresh discovery; V-07 pass → guide wording extended and locked by
  a new required phrase → fresh discovery; R-01 fail F-02 → via V-01–V-04;
  R-02 fail F-02 → via V-01–V-05; R-03 pass → via V-06. Prior passes were
  navigation context, not acceptance evidence for the corrected bytes; no
  row was blocked or unchecked.

## Correction record (discovery-03 finding F-03)

- Finding: F-03 [suggested P2] — acyclic source aliases were falsely
  rejected as cycles: the collector's flat per-package `visited` identity
  set treated any repeated directory identity as a cycle, so a fully
  installed distribution with two links to one external directory, or a real
  directory plus a link to it, reported check failure (exit 2, empty stdout)
  with a false `directory cycle` diagnostic even though the installer
  successfully materialized every copy.
- Broken invariant: check enumeration must describe the complete projection
  accepted and materialized by the canonical installer; a repeated directory
  identity at a different acyclic source path is valid copied content, not a
  recursion cycle (AC-01, AC-02, AC-05; V-01/V-02/V-07; R-01/R-02 / INV-009).
- Fix at the invariant level: one shared-collector change — an ancestor-chain
  cycle check replacing the flat identity set — fails only when a directory's
  identity is one of its own ancestors along the walked root path and
  enumerates independent acyclic aliases at each of their linked paths. No
  per-path or per-package exception; transient pruning, enumeration and
  metadata error propagation, target inner-symlink non-traversal, existing
  refusals, and bounded true-cycle failure are preserved (the true-cycle
  regression stays green). True cycles remain precisely `directory cycle`
  exit 2; both source and installed sides share the corrected collector.
- Credible sibling surfaces covered: multiple links to one shared subtree and
  a regular subtree plus a link to it (the collector change is generic per
  package; the regression exercises project-direction with both layouts and
  the per-path missing-drift oracle rejects one-alias-suffices shrinkage);
  aliased reference/eval/setup trees in any selected source package
  (generic per-package behavior); true ancestor cycles (retained regression
  and Appendix A single-alias contrast).
- Ledger consumption (prior status → correction evidence → next owner):
  V-01 fail F-03 → RA3 acyclic-alias fresh-install match evidence + new
  regression → fresh discovery; V-02 fail F-03 → same alias coverage plus
  per-path missing drift and RB3 family/sibling probes → fresh discovery;
  V-03 pass → transient-pruning navigation, targeted rerun → fresh
  discovery; V-04 pass → marker navigation, targeted rerun → fresh
  discovery; V-05 pass → denial/refusal navigation, RA3/RB3 denials and
  refusal rows rerun → fresh discovery; V-06 pass → reads-only change,
  RB3 snapshot rows rerun, regression asserts repeated-check agreement →
  fresh discovery; V-07 fail F-03 → guide wording now states acyclic
  aliases compare as copied content and only ancestor-closing links are
  cycles, locked by new required phrases → fresh discovery; R-01 fail F-03
  → via V-01–V-04 evidence; R-02 fail F-03 → via V-01–V-05 evidence;
  R-03 pass → via V-06 evidence. No row was blocked or unchecked; prior
  passes were used as navigation context, not as acceptance evidence for
  corrected bytes.

## Scenario and finite-risk evidence

Implementation checks, not independent acceptance evidence. Every
verification scenario ID is accounted for; none blocked or unchecked.

| Scenario | Evidence (test, oracle, result) |
|---|---|
| V-01 | `test_check_reports_match_after_fresh_install_in_committed_and_unborn_repos`: real installs in committed and unborn targets → check exit 0, `match: true`, empty `differences`, and `compared_paths` equal to an independently enumerated managed projection (rejects partial comparators) — OK; Appendix B match rows rerun; F-02: a relocated linked-source distribution installs and matches with `compared_paths` covering the linked file, and deleting the copied linked subtree reports exact missing drift (new regression + discovery-02 Appendix A corrected oracle) — OK; F-03: two links to one external directory and a real-directory-plus-alias distribution install and match with `compared_paths` covering every aliased copy (new regression + discovery-03 Appendix A corrected oracle) — OK |
| V-02 | `…changed_bytes_for_every_managed_family` / `…missing_bytes_for_every_managed_family` (SKILL.md, reference, eval/setup, profile guide, shared script/config/schema; exact per-path category vs recorded fixture deltas), `…every_file_of_a_missing_selected_skill_directory` (full expected missing list), `…detects_managed_drift_that_the_workflow_fingerprint_excludes` (installed `evals/evals.json` mutated: workflow fingerprint and `workflow_dirty` unchanged, check still reports the changed path) — all OK; `…unreadable_managed_directories_as_failures` keeps the unexpected-subtree case a distinct exit-2 failure when enumeration is denied (F-01) — OK; Appendix B reran changed/missing for all 20 packages and all 6 shared files; F-02: linked source content is a covered expected path with an exact `missing` category oracle (new regression) — OK; F-03: aliased copies are covered expected paths with exact per-path `missing` drift (new regression) — OK |
| V-03 | `…ignores_unmanaged_content_and_installer_transient_files`: unselected skill, non-selected script, other `.agents` content, AGENTS text outside the block, and all four transient patterns (`__pycache__`, `*.pyc`, `.DS_Store`, `node_modules`) → match; contrast extra owned non-transient file → `unexpected` drift — OK; transient directories are pruned before descent, mirroring install-time copying |
| V-04 | `…agents_block_drift_and_precise_marker_failures`: changed valid block → drift `AGENTS.md`; missing block and missing file → drift; unmatched/duplicate/reversed markers → exit 2 with precise `malformed`/`reversed` diagnostics, stdout empty, never match — OK |
| V-05 | `…failures_retain_existing_refusals_and_stay_distinct_from_drift`: nonexistent/non-Git/non-root targets, symlinked `.agents` (refused, outside content preserved), wrong-type shared script, unusable source (mocked, mirrors the existing install test) → exit 2, distinct from drift's exit 1 — OK; `…reports_unreadable_required_content_as_failure`: chmod-000 managed file → exit 2, path in diagnostic, bytes unchanged, plus the dangling-managed-symlink metadata-failure case → exit 2 `cannot access installed skill content` — OK; `…unreadable_managed_directories_as_failures` (F-01): denied expected and unexpected subtrees → exit 2 `cannot enumerate installed skill directory`, repeated checks agree, bytes and result classes restored — OK; `…unreadable_source_directories_as_failures`: denied source subtree → `cannot enumerate source skill directory`, target untouched — OK; Appendix B reran all 14 refusal cases |
| V-06 | `…results_and_repeated_checks_leave_all_state_unchanged`: full recursive before/after snapshots (path/type/bytes, including `.git` metadata and the installer-written evidence storage) identical for match/drift/failure/absent fixtures in committed and unborn repos, check run twice with identical results; drift canary keeps reporting identical drift (rejects hidden repair) and absent installation stays absent; source projection snapshot unchanged — OK; Appendix B independently reran all 8 combinations twice; the new denied-directory test additionally proves repeated exit-2 checks leave denied subtrees untouched |
| V-07 | `…matches_install_from_unrelated_cwd_and_guides_document_semantics`: positional install and `--check` from an unrelated empty CWD → match with unmanaged bytes and outside-block AGENTS text preserved, `source_repo` = installer location; both guides carry the required semantics (whitespace-normalized phrase assertions), now including enumeration-failure wording and the F-03 alias-cycle semantics — OK |

Risk rows: R-01 / INV-009 → V-01–V-04; R-02 / INV-009 → V-01–V-05;
R-03 / INV-009 → V-06. AC mapping: AC-01 → V-01/02/04/05; AC-02 →
V-01/02/03 (+ `compared_paths` oracle); AC-03 → V-02/03/04/05; AC-04 →
V-06; AC-05 → V-01/07.

Local design decisions (reversible): malformed/ambiguous markers are
classified as check failure (exit 2) — the documented non-match
classification V-04 allows; `compared_paths` added to the JSON result as a
subprocess-callable coverage oracle; marker diagnostics reuse the installer's
existing error strings; enumeration/metadata failures reuse the existing
exit-2 failure class with new scope-specific diagnostics rather than a new
result class (the V-04 design note permits the implementation to choose the
non-match classification).

## Skipped stronger checks and their owners

- The justified current aggregate remains owned by the next fresh
  `task-review-discovery`: this correction pass reran the owning installer
  suite (command I3, 33 OK) as implementation evidence, which fresh discovery
  may consume or rerun per its workflow.
- The chmod-based read-failure oracles (V-05 unreadable file/directory
  cases, V-06 failure-class fixture, source-side enumeration case) skip
  under a root user (`os.geteuid() == 0`); all ran for real in this
  environment (non-root).
- V-06 snapshots cannot disprove a write that fully cleans up after itself;
  mitigated by the behavioral canaries (repeated identical drift, denied
  subtrees restored to prior result classes, absent installation stays
  absent) and by the check code path containing no install/stage/
  availability/run-start calls; the correction adds reads only.
- The brief's soft budget (15 calls) was crossed in the original
  implementation (~13 at discovery completion, ~25 total); the F-01
  correction invocation stayed bounded (~20 calls); the F-02 correction
  invocation also stayed bounded (~25 calls including reviewer regressions);
  the F-03 correction invocation stayed bounded (~22 calls including
  pre-fix fail-first and reviewer regressions).

## Interface notes for T-004.3

- CLI: `install_development_skills.py --check <target>`; positional install
  unchanged. Exit 0/1/2 and JSON result shape as in Deliverables; drift
  differences are sorted deterministically for subprocess comparison.
- Failure diagnostics: unusable source/target and existing path-shape
  refusals keep their existing messages; unreadable required content reports
  `cannot read required … content`; unenumerable managed directories report
  `cannot enumerate source|installed skill directory`; unreachable managed
  entries report `cannot access source|installed skill directory|content`,
  all with the exact failing path, on stderr with exit 2.
- Comparison scope: every non-transient file in each selected skill package,
  each managed shared script/config/schema, the installed profile guide, and
  the marked `AGENTS.md` block. Only the installer's transient copy
  exclusions apply — workflow fingerprint exclusions do not define profile
  equivalence. Unselected skills, non-selected scripts, other `.agents`
  content, and AGENTS text outside the block never cause drift; unexpected
  files count only inside selected skill directories. Source enumeration
  follows directory symlinks exactly as install-time copying dereferences
  them, so linked source content is compared like any other copied file, and
  acyclic directory aliases are compared at every linked path; installed
  trees are never traversed through inner symlinks, and only a link that
  closes a directory cycle back to one of its own ancestors reports
  `cannot enumerate source skill directory: <path>: directory cycle` on
  stderr with exit 2.
- Remaining gaps for .3: the check retains no versions (refresh is a
  deliberate installer rerun between invocations); refresh composition and
  drift→restoration proof belong to T-004.3; installed-flow skill-call
  qualification belongs to T-005.

## Review handoff

Per `review: immediate`: the F-03 corrected bytes (the four changed paths
above) re-enter every applicable conditional stage whose reviewed scope this
production correction affected, then go to fresh independent
`task-review-discovery`, and its report to a separate fresh
`task-acceptance-review`. No repository policy declares a conditional
architecture gate for these bytes and no contract registry exists. The prior
maintainability-01 ACCEPT covered the original collector and test scope;
each subsequent correction (F-01, F-02, F-03) touches that same shared
collector and adds tests, so a fresh `task-maintainability-review` pass owns
that stage first. Fresh
discovery then owns the justified aggregate after clean targeted rows. The
implementer invocation ends here without a self-issued verdict.