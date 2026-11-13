# T-005.1 independent maintainability review

VERDICT: ACCEPT
ARCHITECTURE_GATE: PASS

Review date: 2026-11-12. This reviewer session authored none of the reviewed
production, schema or test bytes. Scope is the staged implementation; unrelated
untracked `.DS_Store` files are excluded. This report consolidates the review and
its subsequent focused complexity assessment. The report does not review itself.

## Blockers

NONE.

## Warnings

- `controller.status_run` cyclomatic complexity increased from 21 to 37.
  Evidence freshness checks and recovery-action precedence are harder to follow
  as a result. This is a non-blocking maintenance concern: the branches still
  implement one status projection, reuse current-evidence validators, and do not
  add unrelated responsibilities or dependencies. If another evidence stage or
  recovery rule is added, reassess extracting freshness projection and action
  precedence into focused helpers that consume the same ledger snapshot. A new
  consumer is not a prerequisite for such an extraction.
- The dedicated registry-updater stage must reconcile acceptance admission,
  dispositions, eligibility and retained-proof binding with registry and capability
  prose that still describes acceptance as a raw claim. Pending synchronization
  is not a blocker at this stage.

## Reviewed scope and evidence

Changed production scope: `controller.py`, `controller_state.py`,
`actor-result.schema.json` and `task-manifest.schema.json` inside
`skills/task-orchestrator/`. Also inspected the changed actor/controller tests,
T-005.1 brief and implementation report, and task-local controller contract.
Parent/successor task packages and the task index supply context, not implemented
capability.

Canonical architecture command, rerun immediately before writing this report:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py
```

Result: 4 tests passed, no skips. This is static architecture evidence, not
behavioral qualification. The earlier structural contract-registry check passed
with 8 subsystems and 36 indexed plan references; it does not establish semantic
registry currency. Functional acceptance and full behavioral verification remain
separate; no behavioral suites or analyzers were rerun for this report.

Policy/boundary sources: repository `AGENTS.md`, `docs/project-map.md`,
`docs/development.md`, `tests/test_architecture.py`,
`docs/contracts/task-orchestrator.json`, orchestrator
`references/architecture-map.md`, and the T-005.1 package. The active review skill
was resolved from `.agents/skills/task-maintainability-review/SKILL.md`.

## Complexity assessment

Inspected retained measurements `.quality/reports/T-005.1-before-01.json` and
`.quality/reports/T-005.1-after-05.json` through their comparison and implementation
report. Verified that the after report's hashes match all four staged Python
files. The saved after report records complete measurement, no errors and a
completed comparison. These are retained analyzer results, not a fresh analyzer
execution. Targets (complexity 10, statements 50, arguments 5) are advisory.

The reviewer, rather than the score or the implementer's justification, owns the
following maintainability judgment:

| Changed hotspot | Independent assessment |
|---|---|
| `status_run`, CC 21 → 37 | Added branching projects candidate/check/collection/acceptance freshness and recovery from one ledger snapshot. Ordering increases reading cost, but validators own proof checking and no separate domain concern was introduced. Accept with the warning above. |
| `reserve_operation`, CC 33 → 44 | Added prerequisite and retained-decision checks guard the existing locked reservation and recovery path. This remains reservation authority; no competing admission path or new dependency edge was introduced. Non-blocking. |
| `_acceptance_route`, new CC 17 | Four decision routes and correction precedence form one deterministic policy function, callable without external I/O. Splitting by action could disperse cross-action precedence; the current structure is proportionate. |
| `_disposition_for_finding`, new CC 13 | Contradictory claims and preserved approvals are checked in one deterministic finding-disposition boundary. No duplicated policy implementation or unnecessary infrastructure dependency was identified. |
| `_admit_acceptance`, new CC 17 | Provenance and current-context checks feed one publication transaction. Context, shape validation, dispositions and routing already have focused helpers; transport remains separate. |
| `_validate_current_collection`, CC 7 → 11; `_admit_collection`, CC 25 → 26 | Added retained-rerun validation and digest publication belong to the existing collection evidence boundary and reuse shared evidence/check helpers. |

Acceptance admission extends the existing observe/admit/publish path. State
retains record-shape validation; the controller owns orchestration and authority.
Immediate collaborators preserve the established dependency direction. Test
changes reuse the existing fake actor and real local Git/check setup; routine
setup is shared, while the longer correction journey supplies distinct lifecycle
composition evidence. No concrete high-impact cohesion, coupling, locality,
testability, duplicated-authority or speculative-abstraction regression was found.

Complexity warnings therefore do not change the verdict to CHANGES_REQUESTED.
ACCEPT applies only to maintainability of the identified bytes, not functional
correctness, live-runtime qualification or permission to complete the task.

## Reviewed staged byte identities

- `skills/task-orchestrator/scripts/controller.py`: `a26826684de948299511fcb838345b72e6468c92a2bb4d97248653170874fcb5`
- `skills/task-orchestrator/scripts/controller_state.py`: `7ab6e6aa48228a441a737b26803e2e303e6d79dacf63db739853502ec180d762`
- `skills/task-orchestrator/assets/actor-result.schema.json`: `97dd82508fbf718a26e8fc5aae0ae10778d66507bd1ba1b4899c526984828825`
- `skills/task-orchestrator/assets/task-manifest.schema.json`: `12b99cb5c3b42c8e7b8c68585fcd9bb82f6997d29b2c6af1394e2e41b45fcf76`
- `skills/task-orchestrator/tests/test_actor_operations.py`: `cfb612d8429752dd0497fe7213520e403d745d54675034a95f9bc69488e15871`
- `skills/task-orchestrator/tests/test_controller.py`: `c25037fcfc52ac84b3d3cfaee41bbe2027cb38bc8bb6846ae3a8716ce65a804b`

## Exact Git status around report creation

Before (`git status --porcelain=v1 --untracked-files=all`):

```text
M  skills/task-orchestrator/assets/actor-result.schema.json
M  skills/task-orchestrator/assets/task-manifest.schema.json
A  skills/task-orchestrator/docs/tasks/T-005.1/brief.md
A  skills/task-orchestrator/docs/tasks/T-005.1/controller-contract.md
A  skills/task-orchestrator/docs/tasks/T-005.1/implementation-report.md
A  skills/task-orchestrator/docs/tasks/T-005.1/preflight.md
A  skills/task-orchestrator/docs/tasks/T-005.1/verification.md
A  skills/task-orchestrator/docs/tasks/T-005.2/brief.md
A  skills/task-orchestrator/docs/tasks/T-005/brief.md
M  skills/task-orchestrator/docs/tasks/index.json
M  skills/task-orchestrator/scripts/controller.py
M  skills/task-orchestrator/scripts/controller_state.py
M  skills/task-orchestrator/tests/test_actor_operations.py
M  skills/task-orchestrator/tests/test_controller.py
?? .DS_Store
?? docs/.DS_Store
?? skills/.DS_Store
```

After (same command):

```text
M  skills/task-orchestrator/assets/actor-result.schema.json
M  skills/task-orchestrator/assets/task-manifest.schema.json
A  skills/task-orchestrator/docs/tasks/T-005.1/brief.md
A  skills/task-orchestrator/docs/tasks/T-005.1/controller-contract.md
A  skills/task-orchestrator/docs/tasks/T-005.1/implementation-report.md
A  skills/task-orchestrator/docs/tasks/T-005.1/preflight.md
A  skills/task-orchestrator/docs/tasks/T-005.1/verification.md
A  skills/task-orchestrator/docs/tasks/T-005.2/brief.md
A  skills/task-orchestrator/docs/tasks/T-005/brief.md
M  skills/task-orchestrator/docs/tasks/index.json
M  skills/task-orchestrator/scripts/controller.py
M  skills/task-orchestrator/scripts/controller_state.py
M  skills/task-orchestrator/tests/test_actor_operations.py
M  skills/task-orchestrator/tests/test_controller.py
?? .DS_Store
?? docs/.DS_Store
?? skills/.DS_Store
?? skills/task-orchestrator/docs/tasks/T-005.1/reviews/maintainability-01.md
```

Only the new report entry was added. Existing staged changes were not modified
and the report was not staged.
