# T-002.3 — F-03 / F-05 correction handoff

Implemented: READY_FOR_REVIEW

- Authority: `docs/tasks/T-002.3/brief.md`.
- Preflight/context reference: `docs/tasks/T-002.3/preflight.md` (guided ready),
  `docs/tasks/T-002.3/verification.md` (revision 1; source brief matches).
  No material dependency, permission, ownership, scope or authority change.
- Preceding verdict: **CHANGES_REQUESTED**. Reviewer baseline HEAD:
  `ae7c7bb105b56ee78ebfffd77afa848446907f65`; submitted scoped diff SHA-256:
  `7dbf3e0acf623ebe0f7ecc3f3575979197ffd56bf471ee46bd124e7d1927f13e`.
- Complete findings and invariant:
  - **F-03 [P2], partially unresolved:** the serious-delay setup had a deadline
    but no contrasting authorized local resolution. V-03 requires both
    serious-delay and costly-later cases with and without resolving authority.
    Eval 28 now supplies the same 2-hour deadline and 8-hour response as eval 19,
    plus an authoritative local Region B / 3-year policy and read permission.
    Its context and discovery establish local resolution before escalation;
    the unresolved sibling retains its focused coordinator question. Evals
    15/18 retain the unresolved/resolved costly-later contrast.
  - **F-05 [P2], new finding:** eval 27 introduced the settlement consumer after
    the prior review despite claiming unchanged operating context. Newly
    demonstrated risk must change proof, not the consumer or exposure. The
    consumer now exists identically at HEAD~1 and HEAD in the disposable fixture.
    Only `tests/helpers/replay.py` changes between those snapshots. Both consumer
    versions charge $10 after one retry and $20 after two for one order. The
    changed-context/authority sibling remains distinct and retains its changed AC.
  - Prior **F-01, F-02, F-04** are resolved in the supplied independent review;
    their corrections are preserved as navigation context, not newly accepted.
- Current scoped diff:
  - `skills/task-implementation-flow/task-acceptance-review/evals/files/setup_fixture.py`:
    independent resolution/deadline options, resolved-delay registration, and
    settlement consumer created before the prior snapshot commit.
  - `skills/task-implementation-flow/task-acceptance-review/evals/evals.json`:
    new eval 28 for locally resolved serious-delay uncertainty.
  - `tests/test_review_discipline.py`: two regression tests and registration
    coverage. Tests probe deadlines, policy, authority, purge behavior, both
    committed consumers, snapshot changes and sequential settlement behavior.
  - `docs/tasks/T-002.3/correction-result-02.md`: this handoff.
  - Existing staged task paths are preserved: `README.md`, `skills/README.md`,
    `skills/task-implementation-flow/README.md`, acceptance `SKILL.md`, acceptance
    report template, the three source/test paths above, and
    `docs/tasks/T-002.3/correction-result.md`. New corrections are unstaged;
    the index and earlier result file are unchanged.

## Coverage ledger

The supplied reviewer statuses remain unchanged. All current implementation
evidence is submission evidence; a fresh reviewer owns acceptance of these bytes.

| Row | Prior status | Implementation evidence | Next owner/status |
|---|---|---|---|
| V-01 | pass | Existing destructive-export, mitigation, consumer and parser-maintenance probes rerun in the owning suite | Fresh acceptance reviewer; prior pass is navigation only |
| V-02 | pass | Existing bounded footer, compatible consumer and disposition checks rerun in the owning suite | Fresh acceptance reviewer; prior pass is navigation only |
| V-03 | fail | New resolved/unresolved delay probe checks identical deadline facts, local policy/read authority, report route and configured-horizon purge; existing costly-later contrasts rerun | Fresh acceptance reviewer; prior fail unchanged |
| V-04 | pass | Existing guided-profile, repeated-claim, missing-helper and correction-authority checks rerun | Fresh acceptance reviewer; prior pass is navigation only |
| V-05 | pass | Existing record fields, coordinator ownership and advancement-order checks rerun | Fresh acceptance reviewer; prior pass is navigation only |
| V-06 | pass | Existing conditional links, future-work, priority-only and no-links checks rerun | Fresh acceptance reviewer; prior pass is navigation only |
| V-07 | pass | Existing row-count and incorrect UTC consumer probes rerun | Fresh acceptance reviewer; prior pass is navigation only |
| V-08 | fail | New consumer-history probe confirms identical consumer, only added replay proof and $10/$20 sequential charges; existing regression/log and other new-blocker contrasts rerun | Fresh acceptance reviewer; prior fail unchanged |

## Verification

- Fail-first:
  `PYTHONDONTWRITEBYTECODE=1 python3 tests/test_review_discipline.py ContextualRiskFixtureTests.test_serious_delay_resolves_locally_only_with_supplied_authority ContextualRiskFixtureTests.test_new_risk_history_keeps_consumer_and_changes_only_available_proof`
  — initially rejected the missing resolved-delay scenario and absent prior
  consumer; after correction, both tests passed.
- Reviewer reproducer:
  `PYTHONDONTWRITEBYTECODE=1 python3 tests/test_review_discipline.py ContextualRiskFixtureTests`
  — 19 tests passed.
- Reviewer reproducer:
  `PYTHONDONTWRITEBYTECODE=1 python3 tests/test_review_discipline.py ContextualDispositionContractTests ContextualDispositionEvalTests`
  — 10 tests passed.
- Owning suite:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_review_discipline.py`
  — 54 tests passed; assigned to the implementer by the brief.
- `git diff HEAD --check` — passed. Final status contains only the pre-existing
  staged task paths, the three intended unstaged source/test corrections and
  this new handoff.
- Broad/aggregate gate: no repository-wide or live command is authorized by the
  brief; skipped. The reviewer's independent aggregate decision remains owned
  by a fresh acceptance reviewer. This owning-suite result does not replace it.
- Optional run-evidence sidecar: unavailable (`git_metadata_unwritable`); no
  lifecycle operation started or retried.

## Deliverables and continuation

Deliverables:
- Resolved serious-delay fixture/eval and decisive regression probes.
- Consistent unchanged-consumer history and settlement regression probe.
- Separate correction handoff preserving prior review provenance.

Actual contract impact:
- No additional durable cross-task contract change in this correction. Existing
  staged ART-007 / ART-008 guidance remains unchanged by this invocation.

Executable contract declarations changed:
- None; eval registration is task-local verification setup.

Installer constants were inspected; selected skills, shared runtime dependencies
and installation ownership do not change. No installer refresh is needed.

Remaining reviewer coverage: all V-01–V-08 need fresh review of current bytes.
No supplied row was unchecked or blocked; V-03/V-08 retain their prior failing
status until fresh review. Fixture/runtime checks do not demonstrate actual
agent decisions, prompts or writer behavior. Those remain assigned to T-005;
cross-stage composition and installed-projection refresh remain assigned to
T-002.4. No live or cross-stage checks were run here.

Next: fresh `task-acceptance-review` against the source tree and full scoped diff
from HEAD, including these unstaged corrections. No independent verdict is
issued by this implementation invocation.
