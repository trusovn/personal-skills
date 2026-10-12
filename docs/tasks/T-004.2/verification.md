# Verification Design: T-004.2 — Add explicit read-only development-profile checking

Source brief: docs/tasks/T-004.2/brief.md
Source brief revision: SHA-256 `ecf57bb5cb33dda3405269c3f6adf05628248d2a4510fe34358d98d8e027512e`
Verification revision: 1
Authority: derived from the task brief and its cited normative sources
Status: ready

Normative references: `docs/project-plan.md` (ART-009–011, IF-007,
INV-009, FLOW-004, sections 10–11), `docs/task-map.json` (T-004), and
`docs/tasks/T-004/brief.md`. T-004.1 supplies the installation boundary;
its current reviewed applicability remains a preflight check.

## Coverage summary

| AC / risk row | Scenarios | Notes |
|---|---|---|
| AC-01 | V-01, V-02, V-04, V-05 | Real installed match, precise drift/missing, and actual failure; documented output and exit classes. |
| AC-02 | V-01, V-02, V-03 | Complete selected projection, exact drift paths, and copy exclusions rather than fingerprint exclusions. |
| AC-03 | V-02, V-03, V-04, V-05 | Owned extras versus unmanaged bytes, block boundaries, and existing unsafe-path refusals. |
| AC-04 | V-06 | Source/target/Git/evidence snapshots for every result class and repeated checks; absent installation stays absent. |
| AC-05 | V-01, V-07 | Positional install compatibility, narrow ownership, source resolution, and complete usage guidance. |
| R-01 / INV-009 | V-01, V-02, V-03, V-04 | All selected packages and shared files; changed/missing families; unexpected owned files; fingerprint-excluded drift. |
| R-02 / INV-009 | V-01, V-02, V-03, V-04, V-05 | Distinct outcomes, unmanaged changes, marker cases, and unsafe/unreadable inputs. |
| R-03 / INV-009 | V-06 | Every result class in unborn/committed repos, absent installation, and repeated unchanged input. |

## Verification scenarios

### V-01 — A real installed projection matches through the public check

Covers: AC-01, AC-02, AC-05, R-01, R-02

Intent: Reject a missing check interface, a check that always reports drift,
or a check that needs a committed HEAD despite a valid unborn installation.

Given:
- Disposable real Git targets exist in genuinely unborn and committed states.
- The canonical positional install invocation has successfully installed the
  complete profile into each target using valid canonical source inputs.
- An independently enumerated expected projection accounts for every copied
  file in every selected skill, the profile guide, every selected shared
  script/config/schema, and the expected managed AGENTS block.

When:
- The documented explicit check invocation compares each target with that source.

Then:
- Each result is the documented match class with its documented exit semantics.
- No expected managed path is reported as changed, missing, or unexpected.
- The result is distinguishable from the drift and failure cases below.

Oracle / boundary:
- Observe stdout/stderr and process exit at the canonical public CLI, against
  independent fixture contents and real Git state. Install success alone is
  not evidence of check success.

Variants:
- Unborn and committed targets.

### V-02 — Managed content changes, omissions, and extras are reported precisely

Covers: AC-01, AC-02, AC-03, R-01, R-02

Intent: Reject partial selection, SKILL.md-only comparison, omitted shared
files, and workflow-fingerprint-only equivalence.

Given:
- A complete installed fixture and its independently enumerated source projection
  are available, with a clean matching baseline.
- Separate cases deliberately change or remove owned files from these families:
  SKILL.md, reference, eval/setup, profile guide, and shared script/config/schema.
- The cases cover every selected skill package and every explicitly managed
  shared file without requiring a Cartesian product of families and operations.
- At least one changed eval/setup file is copied by the installer but excluded
  from the workflow fingerprint; that mutation leaves the fingerprint unchanged.
- Another case adds a non-transient file inside a selected skill directory.

When:
- The public check runs on each deliberately modified fixture.

Then:
- Each result is the documented drift/missing class.
- The diagnostic identifies the exact owned changed, missing, or unexpected
  paths and their applicable category, consistent with the fixture delta.
- Fingerprint-excluded managed drift is still detected.

Oracle / boundary:
- Compare public CLI diagnostics and exit semantics with independently recorded
  fixture path/byte deltas. Corroborate the excluded-file case at the existing
  fingerprint boundary; a fingerprint alone cannot establish profile equivalence.

Variants:
- Changed and missing content across the named families; missing selected skill
  directory; unexpected non-transient selected-directory file.
- Shared helper, config, and schema files are each represented where selected.

### V-03 — Unmanaged bytes and copy-excluded transients do not cause drift

Covers: AC-02, AC-03, R-01, R-02

Intent: Reject blanket `.agents` comparison, whole-AGENTS comparison, and
comparison rules that ignore either too much or too little content.

Given:
- A matching installed profile includes an additional unselected skill,
  non-selected script, other unmanaged `.agents` content, and AGENTS text
  before and after its valid managed block.
- These unmanaged bytes are changed or extended while owned content stays equal.
- Installer-copy transient patterns (`__pycache__`, `*.pyc`, `.DS_Store`,
  `node_modules`) are represented within selected source/target skill trees.

When:
- The public check compares the fixture, then compares a contrast fixture with
  an extra non-transient file inside a selected skill directory.

Then:
- Unmanaged changes and installer-excluded transients do not cause drift.
- The contrast fixture reports its unexpected managed file as drift.
- The expected managed block is compared independently of surrounding text.

Oracle / boundary:
- Observe public CLI outcomes against the fixture ownership inventory and the
  installer's existing copy exclusions, rather than workflow fingerprint rules.

Variants:
- Each named unmanaged surface and each existing transient pattern.

### V-04 — AGENTS block changes, absence, and invalid markers cannot match

Covers: AC-01, AC-02, AC-03, R-01, R-02

Intent: Reject checks that only look for marker presence or silently choose
one block from ambiguous content.

Given:
- Otherwise matching fixtures contain separately: a valid block with changed
  managed content, no managed block, or malformed/ambiguous managed markers.

When:
- The public check compares each fixture.

Then:
- Changed managed content and a missing block report drift at `AGENTS.md`.
- Malformed/ambiguous markers never report match; diagnostics identify the
  marker defect under the documented non-match result semantics.
- Outside-block text alone remains irrelevant as demonstrated by V-03.

Oracle / boundary:
- Observe CLI output/exit and the known marker/content fixture. This design does
  not assign malformed markers to a new result class: the implementation must
  document its chosen non-match classification within the brief's contract.

Variants:
- Missing AGENTS file; existing AGENTS file without markers; unmatched begin/end;
  duplicate marker pairs; reversed markers; changed valid block content.

### V-05 — Unusable or unsafe inputs produce precise non-success diagnostics

Covers: AC-01, AC-03, R-02

Intent: Reject treating validation/read failures as an empty matching projection
or trusting an installation through an already forbidden path shape.

Given:
- Cases supply unusable source inputs, unusable target inputs, or required
  content that cannot be read.
- Separate target cases exercise existing installer refusals for symlinks and
  wrong path types at installation roots, selected skill destinations, managed
  shared files, the profile guide, and `AGENTS.md`.
- Symlink fixtures point at disposable outside content whose state is recorded.

When:
- The explicit check attempts each comparison.

Then:
- Actual source/target validation or read failures report the documented check
  failure class, distinguishable from ordinary missing installed content.
- Diagnostics identify the failed scope/path and reason; no case reports match.
- Existing unsafe-path refusals are retained, without traversing refused paths
  as trusted installations.

Oracle / boundary:
- Use real filesystem/process failure cases where deterministic. If a read
  failure cannot be made deterministic, a controlled filesystem-boundary failure
  must exercise the actual check error path and output mapping, rather than
  returning a fabricated check result. Preflight owns capability resolution.
- Observe CLI outcome/diagnostic and preservation of outside symlink content.

Variants:
- Missing required source input; nonexistent/non-Git/non-root target; unreadable
  required content; each existing target refusal family and applicable wrong type.

### V-06 — All results and repeated checks leave state unchanged

Covers: AC-04, R-03

Intent: Reject checks that install or repair, stage copies, invoke a writing
availability probe, refresh, or create evidence/probe artifacts.

Given:
- Real unborn and committed fixtures are prepared for match, deliberate managed
  drift, and actual check failure, plus a valid target with no installation.
- Managed/unmanaged bytes and evidence storage are present where applicable;
  the absent-installation case has no `.agents` directory.
- Immediately before checking, source and target snapshots record path existence,
  type and content, relevant Git metadata/state, and evidence storage. Setup writes
  are complete; snapshot collection must not itself create the state under test.

When:
- The public check runs twice on each unchanged input, with snapshots after
  each invocation.

Then:
- Each post-check snapshot equals its pre-check snapshot for source and target,
  including managed/unmanaged bytes, Git state/metadata, and evidence storage.
- The missing installation reports drift/missing both times; `.agents` remains
  absent, with no stage/probe artifacts or new run/evidence state.
- Repeated checks agree on result class and managed differences/failure reason.
- No check calls install, stages copies, refreshes, or starts a run.

Oracle / boundary:
- Compare real filesystem and Git/evidence snapshots surrounding the CLI; Git
  status alone is insufficient because ignored files and Git probe metadata can
  change without appearing there. Snapshots cannot prove a forbidden operation
  that cleans up after itself; supplement them with observation at the install,
  staging, refresh, and run-start boundaries if needed to reject that shortcut.

Variants:
- Match, drift, failure, and absent installation in unborn and committed repos;
  repeat each invocation without intervening fixture changes.

### V-07 — Existing install usage and documented check semantics stay coherent

Covers: AC-05

Intent: Reject breaking positional installation, resolving source from caller
CWD, or documenting a check that implies auto-refresh or retained active versions.

Given:
- A disposable target includes unmanaged skills/scripts and outside-block
  AGENTS text whose bytes are recorded.
- The canonical installer and source distribution are available; caller CWD is
  different from the source repository and contains no canonical profile inputs.
- Root README and `skills/README.md` contain the completed check guidance.

When:
- The existing positional install command runs from that unrelated CWD.
- The documented explicit check command runs from that CWD against the result.
- The two guidance documents are compared with the exercised interface.

Then:
- Positional installation succeeds and preserves its existing narrow ownership;
  unmanaged bytes remain intact and the subsequent check reports match.
- Both operations use source resolved from the installer location under the
  existing distribution contract, independent of caller CWD.
- Guidance states the comparison scope, match/drift/failure output and exit
  semantics for human/subprocess callers, source resolution, and deliberate
  refresh between invocations, without a retained-version guarantee.

Oracle / boundary:
- Observe subprocess results and independent installed/unmanaged bytes; inspect
  both guidance documents against that behavior. Text inspection establishes
  documentation accuracy only, not installed skill-call qualification.

Variants:
- None. Refresh lifecycle closure belongs to T-004.3.

## Implementation handoff

- Treat this file as derived verification guidance, not a replacement for the
  task brief. `Status: ready` means verification design is complete; it does not
  certify dependency readiness or implementation behavior.
- Preserve stable scenario IDs across a reasoned coverage revision. A revised
  artifact supersedes affected readiness and evidence until focused preflight
  produces a ready result for the new revision.
- Implement the smallest production and test changes that satisfy the brief and
  exercise these scenarios. Reuse existing installer fixtures and setup; follow
  `testing-discipline` for test maintenance.
- Concrete test structure, framework usage, helpers, and file placement remain
  implementation choices unless already fixed by repository authority.
- Preflight resolves the new CLI, output/exit encoding, targeted selectors,
  deterministic failure setup, and current reviewed T-004.1 interface. Exact
  numeric exit codes and syntax are intentionally not invented here.
- Run targeted evidence first, then the owning installer suite:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py`.
  Fresh discovery owns its justified current aggregate after clean targeted
  rows/probes, including after correction; acceptance consumes that record
  without repeating execution. No whole-repository, live, or model-budget gate.
- If implementation discovery shows that a scenario cannot be exercised at its
  stated boundary, route the conflict back to task design/preflight rather than
  silently weakening the oracle.
- This file does not own T-004.3 refresh composition, parent-level closure,
  full unborn collector lifecycle, or T-005 installed skill-call qualification.
