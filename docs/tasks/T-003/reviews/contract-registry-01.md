REFERENCE_UPDATE: UPDATED

## Authority and reviewed state

- Task: `docs/tasks/T-003/brief.md`, revision 1; T-003 in
  `docs/task-map.json`; project-plan section 5 and T-003 boundary.
- Inputs: implementation submission `../results.md`, current staged diff and
  source declarations, contract index/records, and `maintainability-01.md`.
- The maintainability report records ACCEPT and architecture PASS. Its seven
  implementation index blobs still match the current index; no unstaged
  implementation changes were present. This synchronization changes references
  only and does not decide task acceptance.
- Applied the project-local registry-updater skill and the project-local
  repo-foundation registry model. Source skill guidance is distinct from the
  active installation; no active installation was refreshed.

## Reconstructed contract delta

The source implementer now validates packaged starting evidence or captures it
during direct self-preflight, compares affected code against one original
baseline, and carries proportionate rationale plus native-check evidence in
existing initial/correction formats. Corrections preserve prior reports and
baseline identity, disclose coverage gaps and retain existing stage owners.
Prepared eval inputs/checks expose the finite scenario setup and grading
boundary. These are reusable guidance and handoff contracts for downstream
tasks. They do not implement the independent reviewer protocol or qualify live
agent behavior or the complete installed journey.

No material mismatch with the planned T-003 semantics was found during this
contract reconstruction. No runtime CLI, result schema, installer membership,
shared dependency or optional instrumentation lifecycle changed.

## Registry changes and stable IDs

- Added `docs/contracts/implementer-feedback.json`: owns implementer guidance,
  submission/correction references, native evidence references and eval
  preparation. Dependencies point to measurement, installation and runtime
  evidence. Declarations route to source instructions and actual eval assets.
- Regenerated `docs/contracts/index.json` with the canonical command.
- Newly indexed existing plan IDs: CAP-003, ART-003, ART-004, ART-008, IF-003
  (explicitly the implementer side), INV-005 and INV-008.
- Preserved all 15 prior index mappings. ART-002, ART-006, IF-002, IF-004 and
  shared invariants retain measurement ownership; their implementer consumption
  is described in the new record without duplicating single-owner plan-ID
  mappings. No plan IDs were invented or redefined.

The first regeneration attempt rejected duplicate plan-ID ownership between
the new record and measurement. Removing duplicate mappings while preserving
their described consumption resolved that structural error. Final validation
passed with seven subsystems and 22 indexed plan references.

## Discovery closure

Checked the owning registry records, `skills/task-implementation-flow/README.md`,
the implementer eval README, `skills/README.md`, root `AGENTS.md`, root README,
`scripts/measure-maintainability.md`, and `docs/project-map.md`. There are no
nearer scoped AGENTS/CLAUDE files in the affected source tree. Also checked
`docs/development.md` and the installation declaration/profile lists.

No further explanatory or routing edits were needed. The submitted root/flow
README and measurement-guide changes already explain the new policy and proof
limits. Root instructions route through the generated index, and the project
map's topology/ownership remains accurate. The existing measurement record
continues to describe runtime and standalone producer guidance; the separate
implementer record supplies the downstream guidance without claiming behavioral
qualification. Installation membership/dependencies remain unchanged.

## Verification

- `python3 tools/check_contracts.py --root . --write-index` — PASS after
  resolving duplicate mappings: seven subsystems, 22 indexed plan references.
- `python3 tools/check_contracts.py --root .` — PASS with the same counts;
  structural/path/index validation only.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py`
  — PASS, four tests, no skips.
- `git diff --check` — PASS.

No behavioral suites, live evals or aggregate checks were rerun for these
reference-only changes. The implementation submission's aggregate drift failure
remains a reported limitation; this stage does not clear it or qualify skipped
analyzer cases, agent behavior or installed composition.

## Next owner

First outstanding owner: fresh independent `task-review-discovery`.
Full remainder: fresh discovery evidence, then a separate fresh
`task-acceptance-review` decision. This report completes registry synchronization
only; it does not claim either review stage executed.
