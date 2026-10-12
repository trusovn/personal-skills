# Verification Design: T-004.1 — Install the development profile in genuine unborn repositories

Source brief: docs/tasks/T-004.1/brief.md
Source brief revision: Git blob 0744c01b6db8ece290e7dcdc527821de7ca144a2
Verification revision: 1
Authority: derived from the task brief and its cited normative sources
Status: ready

This is verification-design readiness, not repository readiness or evidence of
passing behavior. Authority is the leaf brief, the cited project-plan sections
1–2, IF-007, FLOW-004, T-004 integration boundary and section 11, and the parent
brief/task-map entry. Parent checker and refresh-composition requirements remain
outside this leaf.

## Coverage summary

| AC / risk row | Scenarios | Notes |
|---|---|---|
| AC-01 | V-01 | Real unborn canonical installation, staged/final availability and unchanged unborn HEAD. |
| AC-02 | V-01, V-02, V-03, V-06 | Explicit unborn identity, actual attached/detached commit identities, genuine Git failures and the first commit transition. |
| AC-03 | V-04, V-05, V-06 | Existing framing/selection/order, layout equivalence, ignored installed bytes and independence from Git commits. |
| AC-04 | V-07, V-08 | Managed selection, source helper projection, ownership preservation and accurate guidance. |
| R-01 / INV-009 | V-01, V-02, V-03 | All four required Git cases; real install/installed availability where success is required. |
| R-02 / INV-009 | V-04, V-05, V-06 | Source/installed layouts, included/excluded changes, deterministic ordering and unrelated commits, including the first commit. |

## Verification scenarios

### V-01 — Installation succeeds without creating a commit

Covers: AC-01, AC-02, R-01

Intent: Reject a fix that needs a fixture commit, substitutes a fabricated commit,
or repairs source identity while the copied availability tools still fail.

Given:
- A disposable target initialized by real `git init`, with no commit and all
  required source profile inputs present.
- Git confirms a symbolic HEAD naming a branch with no commit. Record its ref
  and existing Git objects before installation. The existing installer
  `init_repo` fixture commits and cannot supply this state unchanged.

When:
- Run `python3 scripts/install_development_skills.py <target>` at the canonical
  CLI, then invoke `<target>/.agents/scripts/run_evidence.py --repo <target>
  availability` and the copied workflow identity entry point.

Then:
- Installation exits successfully and reports installation and availability
  success; its staged availability gate and final installed availability pass.
- The explicit final availability invocation exits successfully and reports
  `available: true` from the target's installed tools.
- Workflow identity explicitly represents unborn state and does not claim a
  resolved commit. Its exact representation remains a local design choice.
- HEAD still names the original unborn branch. No commit or fake Git object
  was created by installation or availability.

Oracle / boundary:
- Real installer and installed subprocess results, reported installation root,
  identity output, and independent Git ref/object observations before/after.
- Before repair, record the same properly supplied unborn CLI setup failing for
  the HEAD/availability defect. Missing source inputs are not a valid reproducer.

Variants:
- none

### V-02 — Attached and detached commits retain their identities

Covers: AC-02, R-01

Intent: Reject blanket missing-commit handling or a repair that changes existing
committed installation behavior.

Given:
- A real disposable Git target with a known commit and complete profile inputs.
- Record the actual HEAD commit and whether HEAD is attached or detached.

When:
- Install through the canonical CLI, invoke final installed availability, and
  read workflow identity through the installed identity entry point.

Then:
- Installation and final availability succeed in each variant.
- Identity reports the actual HEAD commit, agrees with attached/detached branch
  behavior, and does not identify either target as unborn.
- HEAD remains at the recorded commit and retains its attachment state.

Oracle / boundary:
- Canonical installer and copied tool subprocess results contrasted with real
  Git HEAD and branch observations. Existing detached behavior reports a null
  branch; attached behavior reports the actual branch.

Variants:
- Attached committed HEAD.
- Detached HEAD at a real commit.

### V-03 — A genuine Git failure cannot become unborn success

Covers: AC-02, R-01

Intent: Reject catching every Git error and treating it as a missing first commit.

Given:
- An actual invalid Git target, with otherwise usable installed tooling and
  package inputs so missing profile files cannot mask the Git failure.
- For a Git-boundary error not reachable through target validation, a valid
  committed target and a controlled non-unborn Git failure with a known cause.

When:
- Attempt the canonical installation on the invalid target and request
  identity/availability at the affected observable boundary.
- Exercise the controlled Git failure through the owning identity/availability
  interface when needed to distinguish error classification.

Then:
- Invalid-target installation reports failure.
- Identity reports the Git failure, and availability reports failure rather
  than `available: true`.
- Neither outcome is represented as successful unborn identity.

Oracle / boundary:
- Real invalid-target CLI failure and identity/availability error results.
  Controlled faults may exercise only the Git boundary; replacing identity or
  availability itself would not prove classification. Preserve the actual error
  cause in the evidence, without requiring incidental diagnostic wording.

Variants:
- Actual invalid Git target.
- Non-unborn Git-command failure in an otherwise valid committed target, where
  needed to expose broad error suppression.

### V-04 — Fingerprints retain framing, selection and ordering

Covers: AC-03, R-02

Intent: Reject a consistent but incompatible new hash format, omitted included
bytes, inclusion of development files, or discovery-order-dependent output.

Given:
- A small known workflow package with included files and a trusted pre-change
  fingerprint tied to its exact relative paths and bytes.
- Separate included and excluded file changes and an alternate discovery order
  for the same package. Keep unrelated inputs fixed for each comparison.

When:
- Obtain fingerprints through the existing identity/fingerprint entry point for
  the unchanged package and each isolated transformation.

Then:
- Unchanged bytes retain the pre-change fingerprint and `sha256:` format.
- Included file changes change the fingerprint; excluded file changes do not.
- Reordering discovery does not change the fingerprint.
- Existing skill-relative POSIX paths, UTF-8 path encoding, sorted order,
  eight-byte big-endian path/content length framing and SHA-256 remain intact.

Oracle / boundary:
- Fingerprint values against the fixed pre-change reference and transformation
  relations. A reference derived from the changed production algorithm is not
  independent evidence of framing compatibility.

Variants:
- Included tracked file edit and an included untracked Unicode filename.
- Excluded root `evals`/`tests`, nested `__pycache__`/`node_modules`, `.DS_Store`
  and `.pyc` content, under the existing selection contract.
- Repeated unchanged read and reversed discovery order.

### V-05 — Equivalent source and installed bytes retain one fingerprint

Covers: AC-03, R-02

Intent: Reject dependence on absolute paths, source layout, or application Git
ignore policy that produces an empty fingerprint for installed packages.

Given:
- Equivalent included workflow relative paths and bytes in the source layout
  and a disposable installed layout, confirmed independently of fingerprinting.
- Copied identity tooling beside the installed skills, in a different repository
  location; excluded files may differ without changing included package bytes.

When:
- Read source and copied installed workflow identities.

Then:
- Equivalent packages have equal, non-empty-package fingerprints despite their
  different repository roots and layout.
- Ignoring `.agents/` does not omit installed included package bytes.

Oracle / boundary:
- Independent package path/byte comparison and source/installed identity outputs
  from their respective tools. Equality alone cannot prove equivalence if both
  results hash no included files.

Variants:
- Standalone copied `skills/` package with sibling `scripts/`.
- Project-local `.agents/skills/` package with sibling `.agents/scripts/`, both
  with and without `.agents/` ignored by the target repository.

### V-06 — The first and later unrelated commits change identity only

Covers: AC-02, AC-03, R-02

Intent: Reject a fingerprint tied to HEAD or an unborn identity that persists
after the first real commit.

Given:
- A successfully installed unborn target from V-01, with its installed package
  bytes and fingerprint recorded.
- Unrelated application content that can be committed without changing the
  included workflow package bytes.

When:
- Create the target's first real commit, then read installed workflow identity
  and availability again.
- Create another unrelated commit and repeat the observations.

Then:
- Each identity reports the current actual commit; the first read after commit
  no longer represents unborn state.
- Availability remains successful.
- The workflow fingerprint is unchanged across unborn, first-commit and later
  committed states, while the commit identity tracks real Git HEAD.

Oracle / boundary:
- Real Git commits and HEAD observations, installed identity/availability
  subprocess results, and independent unchanged package bytes.

Variants:
- First unrelated commit and subsequent unrelated commit, in sequence.

### V-07 — Installation projects only the existing managed profile

Covers: AC-04

Intent: Reject broadening ownership or shipping stale helpers while source-only
checks pass.

Given:
- A disposable target containing unrelated application files, custom skills,
  custom scripts, other `.agents/` files and AGENTS text outside the managed
  block, with their bytes recorded.
- The existing selected profile, guide and shared-script list, including the
  task's changed helper bytes.

When:
- Install through the canonical CLI and inspect the resulting target files.

Then:
- Managed package selection remains the existing development profile.
- Selected package contents, the managed profile guide and shared helpers match
  the source projection under existing transient-file exclusions; changed
  helpers reach sibling `.agents/scripts/`.
- Unmanaged files and AGENTS text outside the marked block retain their bytes.
- Installation ownership remains limited to selected skill directories, the
  managed guide, listed scripts and the marked AGENTS block.

Oracle / boundary:
- Independent before/after filesystem bytes and managed selection comparisons
  against source, not only installer-reported success or list equality.

Variants:
- none; preserve existing focused ownership cases rather than duplicating them.

### V-08 — Guidance describes the exercised unborn boundary accurately

Covers: AC-04

Intent: Reject undocumented usable interfaces or guidance that turns successful
availability into a claim of full unborn collector lifecycle support.

Given:
- Current scenario evidence and any directly affected installation/identity
  guidance in root README, `skills/README.md` and the flow README.

When:
- Compare the affected guidance with the exercised CLI and identity/availability
  results.

Then:
- Guidance states genuine unborn installation and identity/availability support
  at the tested boundaries and exposes the usable interfaces for follow-on work.
- It does not claim unborn collector begin/resume lifecycle support.
- Distribution guidance agrees with the unchanged managed selection, guide and
  shared dependencies actually projected by the installer.

Oracle / boundary:
- Semantic document review against current observed interfaces and scope.
  Wording checks can support document consistency, but prove no runtime or skill
  behavior.

Variants:
- none

## Evidence execution and ownership

- Reuse the relevant existing cases in `tests/test_workflow_version.py`,
  `tests/test_install_development_skills.py` and `tests/test_run_evidence.py`.
  Existing coverage includes included/Unicode/excluded changes, dirty worktree
  bytes, unrelated commits, ordering, standalone/project-local/ignored layouts,
  final installed availability, source projection and unmanaged preservation.
  Preserve distinct evidence; add only missing task-local behavior.
- Implementer: establish the V-01 fail-first result, run new/changed targeted
  cases, then affected owning modules one command at a time. Preflight resolves
  concrete new selectors and confirms dependencies/capabilities. Owning commands
  are `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p
  test_install_development_skills.py`, with the same form for
  `test_workflow_version.py` and `test_run_evidence.py` as applicable.
- Fresh independent discovery: independently initialize an unborn target,
  inspect HEAD before/after, contrast an actual invalid Git target, and compare
  installed fingerprints across the first unrelated commit. These probes may
  reuse scenario inputs but require independent observations.
- Discovery owns the justified affected-module aggregate after current targeted
  rows and selected probes are clean:
  `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest
  test_install_development_skills test_workflow_version test_run_evidence`.
  Preflight confirms this local module invocation. Record its exact command or
  not-run reason, owner/stage and current evidence. A decisive targeted failure
  suppresses the aggregate unless a distinct diagnostic purpose is authorized.
  Correction implementers run targeted/owning checks; acceptance consumes the
  discovery record without duplicating the aggregate.
- No whole-repository, network, model-budget, checker/refresh composition or
  unborn collector lifecycle gate belongs to this design. Record unavailable
  evidence explicitly; scenario design does not claim execution or acceptance.

## Implementation handoff

- Treat this file as derived verification guidance, not a replacement for the
  task brief. Obtain ready standalone guided preflight before implementation.
- Preserve stable scenario IDs across a reasoned coverage revision. A revised
  artifact supersedes affected readiness and evidence until focused preflight
  produces a ready result for the new revision.
- Implement the smallest production and test changes that satisfy the brief and
  exercise these scenarios.
- Concrete test structure, framework usage, helpers and file placement remain
  implementation choices unless already fixed by repository authority.
- If implementation discovery shows that a scenario cannot be exercised at its
  stated boundary, route the conflict back to task design/preflight rather than
  silently weakening the oracle.
- Hand completed bytes and current scenario evidence through applicable
  conditional stages, then fresh independent discovery and a separate acceptance
  decision, as required by the brief. This design performs none of those reviews.
