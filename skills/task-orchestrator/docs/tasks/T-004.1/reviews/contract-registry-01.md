# T-004.1 contract registry update

`REFERENCE_UPDATE: UPDATED`

The staged binary diff has SHA-256
`c3ce9704e173132cd81e7fcca7eb60a7cd8d1048f90cf0456e5b9cbde4865ba1`.
It matches the scope accepted in [maintainability-01.md](maintainability-01.md).

- `ART-003` records the controller's candidate identity and scope checks against
  the frozen baseline and current workspace.
- `ART-005` records the reserved check assignment, candidate, check plan,
  execution evidence, and replay rules.
- `ART-002` now covers current candidate identity and candidate-bound evidence
  status, including stale evidence after drift.
- `IF-003` now includes `inspect_candidate` and `check_candidate`. The
  verification boundary records direct execution under explicit frozen sbx/YOLO
  authority.

Updated `docs/contracts/task-orchestrator.json` and regenerated
`docs/contracts/index.json`. Updated the root `README.md` and the orchestrator's
`references/operator-guide.md` and `references/architecture-map.md`. These
reference edits are unstaged. The staged implementation and task plan files
are unchanged.

`python3 tools/check_contracts.py --root .` passed with 8 subsystems and 35
indexed plan references. The canonical architecture check passed all 4 tests.
`git diff --check` passed. These checks establish structural validity.

Next owner is fresh independent `task-review-discovery`. A separate
`task-acceptance-review` decision follows discovery.
