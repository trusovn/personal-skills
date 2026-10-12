# T-003.3 correction handoff — F-01 guided continuity

Implemented: READY_FOR_REVIEW

- Authority: `docs/tasks/T-003.3/brief.md`
- Preceding verdict: `CHANGES_REQUESTED` (independent guided review of commit
  `3f3d7ab426f5352bc089db60c7fe26d4b2677b56`).
- Complete findings and invariant: only F-01 [P2] — default guided discovery
  can lose correction history. Broken invariant: AC-01 / INV-008 — every
  finding/scenario ID and unfinished pass/fail/blocked/unchecked row survives
  correction with prior status, current implementation evidence, incomplete
  reason, and separate correction/evidence/authority owners. The guided
  continuation blocks recorded only row identities and current results; the
  continuity obligations existed only in the durable templates, which guided
  discovery does not load. The guided acceptance continuation was the named
  sibling surface.
- Current scoped diff: `skills/task-implementation-flow/task-review-discovery/SKILL.md`
  (guided `Discovery continuation` block gains `Finding/scenario continuity`
  and `Preparation/context` fields matching its durable template; output-contract
  prose now requires preserving prior status, current producer-attributed
  evidence, incomplete reason, and separate owners through the handoff);
  `skills/task-implementation-flow/task-acceptance-review/SKILL.md` (same two
  fields added to the guided `Review continuation` block, plus an explicit
  preservation sentence); `tests/test_task_review_discovery.py` and
  `tests/test_task_acceptance_review.py` (one focused contract test each that
  extracts the guided continuation block and asserts the continuity fields).
  Durable templates were already correct and are untouched.
- Coverage ledger:
  - V-01 — prior status: Fail (F-01); implementation evidence: corrected
    guided discovery continuation + new block-extraction contract test
    (`test_guided_continuation_requires_scenario_history_and_separate_owners`,
    discovery module 16 OK); next owner/status: fresh review (reviewer status unchanged).
  - V-02 — prior status: Fail (F-01); implementation evidence: corrected
    guided acceptance continuation + sibling contract test (acceptance module
    24 OK); authorized/forbidden mixed-policy fixtures untouched; next
    owner/status: fresh review (reviewer status unchanged).
  - V-03 — prior status: Pass (reviewer); implementation evidence: none (navigation
    context only; affected routing surfaces untouched); next owner/status: fresh review.
  - V-04 — prior status: Pass (reviewer); implementation evidence: none; next
    owner/status: fresh review.
  - V-05 — prior status: Pass (reviewer); implementation evidence: none; next
    owner/status: fresh review.
  - V-06 — prior status: Pass (reviewer); implementation evidence: none; next
    owner/status: fresh review.
  - V-07 — prior status: Pass (reviewer); implementation evidence: none; next
    owner/status: fresh review.
  - V-08 — prior status: Pass (reviewer); implementation evidence: none; next
    owner/status: fresh review.
- Reviewer reproducer: no exact command was supplied with the review (F-01 was
  established by guided propagation audit). The two new contract tests
  reproduce the defect surface: on pre-correction bytes the asserted continuity
  phrases occur nowhere inside the guided continuation blocks, so both tests
  fail there and pass on corrected bytes.
- Owning suite:
  - `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_task_review_discovery.py` — 16 tests OK
  - `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_task_acceptance_review.py` — 24 tests OK
- Broad/aggregate gate: skipped (brief forbids a whole-repo gate; no applicable
  conditional architecture/maintainability gate exists and there is no current
  contract registry). Local blast-radius check run as implementation evidence:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_review_composition.py` — 9 tests OK
  (module unedited, unchanged). Fresh discovery owns any justified aggregate for
  the review; acceptance consumes without duplication.
- Remaining reviewer coverage: none — V-01 and V-02 failed rows are both
  addressed by this correction; the supplied ledger has no unchecked or blocked
  rows. Prior Pass rows remain reviewer-owned and are not claimed as corrected-byte
  evidence.
- Next: fresh independent `task-review-discovery` evidence for the corrected
  bytes, then a separate fresh `task-acceptance-review` decision. End this
  implementer invocation here; no self-acceptance.
