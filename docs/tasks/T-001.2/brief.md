# Task Brief: T-001.2 — Make report labels neutral and support empty-start baselines

## Outcome

Callers receive factual increase/decrease labels and can capture known absence
before adding Python to an existing folder. Old-format baselines fail clearly.
These report semantics let T-002 capture new Python areas without inventing
before values or accepting arbitrary empty measurements.

## Direction trace

- Direction contribution: plan sections 5 and 7–8 distinguish measured changes
  from design decisions and require a genuine pre-edit capture.
- User-observable effect: JSON/text use `increased`/`decreased`; an explicitly
  selected existing empty parent can precede a real added-file comparison.
- Why now: report semantics must settle before T-002 consumes the capture contract.
- Direction decisions used: plan sections 5–8 and T-001 in section 10.
- New direction decisions required: None.

## Authority and scope

- Authority: [parent authority and reviewed identities](../T-001/brief.md#authority-and-scope),
  particularly plan section 7's format transition and FLOW-002's empty-parent rule.
- Repository: `personal-skills`; follow repository instructions and development guide.
- Dependency: T-001.1 accepted; consume its installed runtime, effective settings,
  pinned dependencies and existing measurement behavior (ART-001/IF-001).
- Allowed changes: the relocated measurement adapter under `scripts/`, relevant
  `tests/test_maintainability.py` cases and `scripts/measure-maintainability.md`.
  Inspect installer selections/tests and profile/README documentation; synchronize
  only references made stale by this report change.
- Out of scope: settings-resolution redesign, further runtime relocation,
  foundation discovery, T-002–T-005 skill changes and parent exclusions.
- Read-only context: T-001.1's accepted outputs; existing threshold, zero-limit
  native Ruff, new/deleted-file, compatibility and output-preservation tests.
- Assumptions: exact new format revision is delegated by plan section 12;
  preflight confirms the implemented path and available pinned interpreter.

Reports remain new named JSON/text files under target `.quality/reports/`.
Never overwrite a report, infer zero from a missing diagnostic, guess a symbol
move, or capture a post-edit replacement baseline. Colocated hashes establish
provenance, not tamper resistance. Existing measure/compare failure semantics,
native exemptions and source/index preservation remain authoritative.

### Expected contract impact

- Change ART-001/IF-001's versioned report contract; implement the tool portion
  of ART-002 empty-start capture. Preserve INV-001/INV-002/INV-003/INV-007.
- Current dependencies: T-001.1's implemented measurement contract, discovered
  through `docs/contracts/index.json` and its owning subsystem record after
  registry synchronization; existing [installation](../../contracts/installation.json).
- Expected delta: neutral report fields/output, explicit incompatible prior
  formats, and folder-baseline known absence consumed by T-002/T-003. Registry
  synchronization belongs to the designated stage after implementation.

## Work and acceptance criteria

- **AC-01:** Replace `got_worse`/`improved` with `increased`/`decreased` in saved
  JSON and human output, including any evaluative classification labels. Preserve
  distinct crossing, new-hotspot and interpretation information. At/below-target
  growth and over-target values complete with exit 0 when measurement succeeds.
- **AC-02:** Version the changed evidence format and document migration. Reject
  old-format baselines and incompatible settings/tools/scope visibly; do not
  reinterpret them as clean current reports. Recovery uses a fresh pre-edit
  baseline or verified exact preserved pre-edit bytes, never the edited tree.
- **AC-03:** `baseline` accepts an explicitly selected existing parent folder
  with a valid empty Python inventory. Add a Python file inside that coverage,
  then compare it with known prior absence. Ordinary empty `measure`, missing
  or excluded scopes still fail; uncovered additions do not claim comparison.
- **AC-04:** Existing non-empty folder capture and affected-subset comparison
  still handle new/deleted files, dirty/staged/untracked code, ambiguous or
  renamed symbols and native missing counts. Retain unknown values and original
  baselines, including after a second real edit and fresh comparison filename.
- **AC-05:** Each saved JSON or sibling text collision refuses overwrite.
  Measurement and comparisons preserve source/index and previously saved reports.

### Finite-risk cases

#### R-03 — Labels or compatibility imply a false verdict; AC-01–AC-02

- Invariant: INV-001/INV-003; observations do not decide acceptance or invent data.
- Material cases: below/at/above target for complexity, native statements and
  arguments; numeric increase/decrease; threshold crossing; new/removed/ambiguous
  symbols; Ruff diagnostic appearance/disappearance and exemption; old format;
  incompatible tools/settings/scope; incomplete baseline.
- Oracle/boundary: actual native values, neutral JSON/text labels and CLI exit
  status; incompatible evidence never yields a successful comparison.
- Implementation evidence: update existing real-analyzer/compatibility cases;
  show old evaluative output fails changed assertions before correcting it.
- Independent review probe: choose different native counts and an old-format
  report; inspect emitted text as well as JSON and unknown values.
- Gate owner/stage: implementer owns targeted/measurement suite; fresh discovery
  probes submitted bytes. T-001.3 owns aggregate composition proof.

#### R-04 — Empty capture or repeated comparison fabricates before state; AC-03–AC-05

- Invariant: INV-002/INV-003/INV-007; absence must be inside captured coverage.
- Material cases: explicit existing empty parent -> add file -> compare -> edit
  again -> new comparison using original baseline; ordinary empty measure;
  missing/excluded parent; uncovered file; deleted captured file; JSON collision;
  text-only collision. Include real staged/unstaged/untracked source preservation.
- Oracle/boundary: real CLI reports show captured folder coverage and known
  absence, separate current identities after edits, unchanged baseline/report
  bytes and real index; invalid paths/overwrites return failure.
- Implementation evidence: extend folder-baseline and no-overwrite tests using
  their existing Git/filesystem setup. No generic empty-success shortcut.
- Independent review probe: repeat one comparison after deleting a captured file
  and attempt a sibling-text collision; verify before bytes remain intact.
- Gate owner/stage: same ownership as R-03.

## Verification

Verification-design recommendation: separate — empty inventories, repeated edits,
compatibility and native unknowns admit plausible false-success implementations.

Derive `verification.md` before preflight. Run changed cases first and then
`<pinned-python> -B -m unittest discover -s tests -p test_maintainability.py`.
Inspect existing coverage before extending it; preserve distinct native exemption
and boundary scenarios. Analyzer skips cannot qualify AC-01–AC-04. Run installer
tests if its managed resources/references change; run required architecture and
contract checks before handoff. T-001.3 owns the final aggregate gate.

## Execution and handoff

Status: `ready`
Task kind: `executable`

Guided profile. Brief prepared; execution prerequisites still required.
Readiness route: standalone guided preflight after derived `verification.md`,
then a ready `preflight.md`. Confirm accepted T-001.1 contract and pinned tools.

```yaml
agent_tier: standard
reasoning: medium
review: immediate
budget: 12 tool calls / 30 minutes / focused report and capture context
```

### Execution sizing

- Sizing policy: `default@1`, active project-local `references/task-sizing.yaml`.
- Estimate: 12 agent calls; 30 implementation minutes. Confidence: medium.
- Policy result: fits; no active trigger matches the estimate or launch pair.

### Stops and next action

- Stop if new report fields require a material policy change, pre-edit bytes
  cannot support a claimed recovery, or scope needs an arbitrary empty success.
- Next: verification design, preflight, implementation; hand the format revision,
  compatibility rules and empty-start interface to T-001.3 and later T-002.
- After implementation or correction, apply maintainability review and registry
  synchronization as required, then immediately use fresh independent
  `task-review-discovery` followed by a separate `task-acceptance-review` decision.
  Preserve existing conditional stage order; author self-checks are not acceptance.
