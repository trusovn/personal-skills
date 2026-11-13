# T-005.1 maintainability reassessment

VERDICT: CHANGES_REQUESTED
ARCHITECTURE_GATE: PASS

Review date: 2026-11-12. This report supersedes the ACCEPT decision in
[maintainability-01.md](maintainability-01.md). That report remains historical.
The same independent reviewer session authored no reviewed production, schema
or test bytes. Reassessment covers unchanged staged implementation bytes;
only review reports and ignored diagnostic evidence were written. The report
does not review itself.

## Blockers

1. **Duplicated recovery-action authority already produces conflicting routes.**
   - Location: `skills/task-orchestrator/scripts/controller.py`,
     `status_run` lines 2266–2295, `reserve_operation` lines 2356–2377,
     and `_reservation_options` lines 2209–2226.
   - Problem: the new status freshness branches select recovery actions by
     overwriting the result of `_reservation_options`. Reservation independently
     applies correction priority and current-acceptance restrictions. These
     consumers do not share a complete decision over current evidence and
     correction authority. The same freshness condition therefore needs separate
     coordination in status and reservation, and their rules already disagree.
   - Evidence: a disposable public lifecycle admitted an actual separate
     acceptance `correct` decision for finding F-01. Before evidence drift, status
     offered `reserve:correction`. Appending a newline to the retained verifier
     result then produced this sequence:

     ```text
     status.next_actions = [reserve:verify, intervene]
     status.blocker = checks_stale
     reserve(verify) = refused: stage_mismatch
     reserve(verify).next_actions = [reserve:correction]
     reserve(correction, review_findings) = refused: authority_or_lock_unavailable
     detail = Retained evidence changed: checks/operation-003.json
     correction_count = 0 throughout; authoritative ledger unchanged
     ```

     Status recommends verification, reservation redirects to correction, and
     correction rejects the stale proof. Intervention remains available, but
     the advertised actionable route is contradictory. This is a demonstrated
     authority-locality problem, not an inference from the complexity number.
   - Maintainability impact: a closely related recovery rule must be implemented
     consistently in multiple consumers with different views of freshness.
     Future changes can create further contradictions or weaken conservative
     authority checks. The disagreement is especially consequential at this
     stateful controller boundary, where callers use returned next actions to
     coordinate work and corrections consume a finite budget.
   - Smallest correction direction: collect current evidence/authority facts
     explicitly, then derive recovery actions and blocker precedence through a
     shared focused decision used by status and reservation. Keep reservation
     validation under its existing lock and preserve proof rejection, active
     operation ownership and correction-budget rules. For invalidated correction
     proof, both surfaces must agree on the authorized recovery route or explicit
     intervention; do not permit correction simply to align outputs. No new
     framework or module hierarchy is required.
   - Focused verification direction: reuse the existing lifecycle helpers to
     exercise admitted review correction followed by verifier-proof drift.
     Assert that status and reservation agree on the permitted next action or
     intervention, and that refusals preserve ledger/version/count. Cover
     correction precedence and exhaustion in the shared deterministic decision
     without duplicating actor/process setup.

## Warnings

- NONE beyond the blocker. Pending registry/capability-prose synchronization is
  still owned by the designated registry-updater stage and is not a separate
  maintainability blocker.

## Why the complexity decision changed

Retained comparison: `.quality/reports/T-005.1-before-01.json` to
`.quality/reports/T-005.1-after-05.json`. The after report records complete
complexity/Ruff measurement, no errors and a completed comparison; all four
reported Python hashes were rechecked against staged bytes. Analyzers were not
rerun. Complexity 10, statements 50 and arguments 5 remain advisory targets.

The earlier assessment accepted `status_run` CC 21 → 37 and `reserve_operation`
CC 33 → 44 because each function retained a related responsibility. That was
insufficient: cohesion within a function does not establish a single authority
for policy shared across functions. This reassessment traced the interacting
routes and reproduced an inconsistency. The blocker therefore applies now;
no additional score increase, consumer or feature is required before correction.
The earlier recommendation to defer reassessment until another stage was added
is superseded.

The new `_acceptance_route` (CC 17) and `_disposition_for_finding` (CC 13) remain
cohesive deterministic policy helpers. `_admit_acceptance` (CC 17) composes
existing context, validation, disposition and routing boundaries at one admission
point. No separate blocker was found for those functions. Lowering a number by
moving branches alone will not resolve the identified duplicated authority.

## Evidence and limits

- Canonical architecture command, freshly executed for this reassessment:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py`.
  Result: 4 passed, no skips. Raw command/output:
  `.quality/reports/T-005.1/maintainability-reassessment-architecture-01.log`.
- Behavioral witness: used existing `ActorOperationsTest` helpers with a real
  disposable Git repository, fake local actors and actual passing local checks.
  Ran preflight, implementation, candidate inspection, verification, independent
  collection and separate acceptance correction, then changed the retained check
  bytes and called public status/reservation APIs. No admission success was seeded,
  no reviewed code was mocked, and no persistent test or fixture was added.
  Raw observed result and setup:
  `.quality/reports/T-005.1/maintainability-reassessment-01.log`.
- Existing coverage inspected before the witness: acceptance integrity matrix,
  disposition/recovery cases and correction journey in
  `tests/test_actor_operations.py`. Integrity and correction routes have coverage
  individually; the demonstrated combination is missing from those cases.
- The witness diagnoses the concrete design regression. This is not a complete
  functional acceptance review, full-suite run, live-provider qualification or
  installation refresh. No behavior/production corrections were made.

## Reviewed

- Changed production scope: orchestrator `scripts/controller.py`,
  `scripts/controller_state.py`, `assets/actor-result.schema.json` and
  `assets/task-manifest.schema.json`; significant changed tests and immediate
  collaborators were also inspected.
- Policy/boundary sources: repository `AGENTS.md`, `docs/project-map.md`,
  `docs/development.md`, `tests/test_architecture.py`,
  `docs/contracts/task-orchestrator.json`, orchestrator architecture map and
  T-005.1 brief/controller contract/implementation report.
- Active skill: project-local
  `.agents/skills/task-maintainability-review/SKILL.md`.
- Next action: implement only the bounded blocker correction, rerun the
  architecture gate and appropriate focused checks, then obtain a fresh independent
  maintainability review of corrected production bytes before later review stages.

## Reviewed staged byte identities

- `skills/task-orchestrator/scripts/controller.py`: `a26826684de948299511fcb838345b72e6468c92a2bb4d97248653170874fcb5`
- `skills/task-orchestrator/scripts/controller_state.py`: `7ab6e6aa48228a441a737b26803e2e303e6d79dacf63db739853502ec180d762`
- `skills/task-orchestrator/tests/test_actor_operations.py`: `cfb612d8429752dd0497fe7213520e403d745d54675034a95f9bc69488e15871`
- `skills/task-orchestrator/tests/test_controller.py`: `c25037fcfc52ac84b3d3cfaee41bbe2027cb38bc8bb6846ae3a8716ce65a804b`
- `skills/task-orchestrator/assets/actor-result.schema.json`: `97dd82508fbf718a26e8fc5aae0ae10778d66507bd1ba1b4899c526984828825`
- `skills/task-orchestrator/assets/task-manifest.schema.json`: `12b99cb5c3b42c8e7b8c68585fcd9bb82f6997d29b2c6af1394e2e41b45fcf76`

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
?? skills/task-orchestrator/docs/tasks/T-005.1/reviews/maintainability-01.md
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
?? skills/task-orchestrator/docs/tasks/T-005.1/reviews/maintainability-02.md
```

Only this new report entry was added. The previous report, existing staged
changes and official plan documents were preserved. The report is unstaged.
