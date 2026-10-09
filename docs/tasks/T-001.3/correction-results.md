# T-001.3 correction results

Implemented: READY_FOR_REVIEW

- Authority: `docs/tasks/T-001.3/brief.md`.
- Preceding verdict: no formal verdict supplied; the user supplied F-01–F-03
  as P2 correction findings.
- Preparation/context: `docs/tasks/T-001.3/preflight.md` and
  `docs/tasks/T-001.3/verification.md`, scenarios V-01–V-08.
- Current scoped diff: corrections are unstaged in the implementer eval JSON,
  fixture setup and `task-brief-designer/tests/test_package_resources.py`.
  This result file is new. The original staged changes remain intact.

## Complete findings and correction evidence

| Finding / prior status | Broken invariant and correction | Implementation evidence | Next owner |
| --- | --- | --- | --- |
| F-01 / reported P2 | REC-44 expected production edits without verification or preflight. It now supplies bound ready preparation, explicit ACs, material context and authorized reviewer-regression ownership. Sibling edit-producing evals 1, 3 and 5 now have explicit executable identity and applicable preparation. | `test_edit_producing_evals_supply_applicable_preparation` independently runs each eval setup, checks entry prerequisites and reproduces REC-44's intended AssertionError. Eval 6's prompt and expectation require entry validation. | Fresh task-acceptance-review; finding remains pending independent review. |
| F-02 / reported P2 | Continuation/revision states must begin with applicable readiness. All seven transition snapshots and all three revision snapshots now commit complete briefs, AC coverage, scope and material context before changing the intended fact. Permission and authority baselines are committed and cited. Revision 2 strengthens V-02 under unchanged authority: old/current/old preflights reference 1/2/1 against current verification 2. | `test_continuation_and_revision_fixtures_supply_distinct_states` reads committed preparation with `git show`, checks baseline/current facts, checks each transition changes only its intended path, and verifies old/refreshed/old revision references. | Fresh task-acceptance-review; finding remains pending independent review. |
| F-03 / reported P2 | Remaining obligations must retain unresolved rows. The complete mixed-result ledger lists V-02 failure, V-03 block and V-04 unchecked coverage with actions and next owners. REC-44's correction handoff also retains both unresolved reviewer rows. | Ledger regressions compare unresolved row identities with remaining obligations and require next owners. V-01 actually passes; V-02 actually fails with AssertionError. | Fresh task-acceptance-review; finding remains pending independent review. |

## Commands and results

All commands run from the repository root.

Reviewer regressions / targeted command:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-implementation-flow/task-brief-designer/tests -p test_package_resources.py -k ImplementerContractTest
```

Result: 9 tests passed. Before fixture correction, the added checks rejected
missing REC-44 preparation, incomplete sibling and continuation entry metadata,
and dropped ledger obligations.

Owning suite:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-implementation-flow/task-brief-designer/tests -p test_package_resources.py
```

Result: 29 tests passed, including existing package, legacy and provenance checks.
`git diff --check` passed.

## Scenario coverage and remaining work

- V-01/V-03/V-04/V-08: new preparation and baseline assertions cover the
  correction; existing source assertions remain implementation evidence.
- V-02/V-06/V-07: existing invalid-entry, incomplete/obsolete evidence and
  route-preservation checks pass in the targeted group.
- V-05: actual pass/fail fixture commands and row-to-obligation checks pass.
- Broad/aggregate gate: cross-stage projection remains T-001.4-owned; no broader
  aggregate gate was run. T-005 agent evals remain unrun and require separate
  authorization. These tests establish source/fixture contracts, not agent
  edit/no-edit or continuation compliance.
- Remaining reviewer coverage: all three corrected findings await fresh
  independent review. Fixture rows V-02/V-03/V-04 remain intentionally unresolved;
  REC-44 ROW-EXACT-BYTES/ROW-REPLAY-BOUNDARY remain failed/unchecked inputs.

Deliverables: applicable eval inputs, committed transition/revision baselines,
consistent obligation ledgers and focused regression evidence.

Actual contract impact: corrected T-001.3 ART-009 eval/fixture evidence for
implementation entry and submission; no additional skill/runtime dependency.
Canonical installer selections, profile guide and shared script list were
inspected; no installer change is needed.

Executable contract declarations changed: implementer `evals/evals.json` and
fixture setup; no worker schema or high-assurance freshness contract change.

Next: fresh `task-acceptance-review`.
