# T-001.2 correction handoff

Implemented: READY_FOR_REVIEW

- Authority: `docs/tasks/T-001.2/brief.md`; derived verification:
  `docs/tasks/T-001.2/verification.md`, revision 1.
- Preceding verdict: CHANGES_REQUESTED.
- Complete findings and invariant: F-01 (P2), AC-05/V-08. Eval case 6 at
  `skills/task-implementation-flow/task-preflight/evals/evals.json:130` dropped
  the negation and offered "or running a broad test baseline" as an alternative
  to the canonical write. This contradicted guided step 7 and the case's own
  no-broad-baseline expectation, so a literal compliant prompt response could
  fail the eval. The focused check inspected expected output/expectations but
  omitted prompt text. Broken invariant: supplied eval prompts must encode the
  same contract as the skill source. Explicit siblings: case 5 (reported clean)
  and every prompt/expectation pair in that file. Requested correction: restore
  the negation and guard packaged guided canonical writes and broad-baseline
  authorization in prompt text. No other finding was supplied.
- Current scoped diff: correction changes only
  `skills/task-implementation-flow/task-preflight/evals/evals.json` (case 6
  wording) and
  `skills/task-implementation-flow/task-brief-designer/tests/test_package_resources.py`
  (seven assertion/setup lines). Existing staged implementation files and index
  remain intact. This separate correction handoff is the only new document.

## Coverage ledger and sibling audit

No complete reviewer coverage ledger was supplied. The table below preserves
the supplied F-01 and case-5 dispositions; absent dispositions are explicitly
unreported. Local checks do not change reviewer status for corrected bytes.
The pre-edit map assigned F-01 to regression/correction evidence, case 5 to
navigation plus sibling coverage, and all remaining pairs to local audit and
fresh reviewer coverage. Broad-gate ownership remained with T-001.4.

| Row identity | Prior reviewer status | Implementation evidence / navigation | Next owner / unchanged reviewer status |
|---|---|---|---|
| F-01 / case 6 / AC-05 / V-08 | failed; CHANGES_REQUESTED | Regression rejected the old authorization; corrected text and prompt assertions pass. | Fresh task-acceptance-review; finding remains pending fresh disposition. |
| case 5 | verified clean, as supplied | Prior result is navigation only; canonical-write prompt assertion and sibling audit cover current text. | Fresh task-acceptance-review; prior clean result is not acceptance of corrected bytes. |
| cases 1, 2, 3, 4 | not supplied | Each prompt/expectation pair audited; no additional broad-baseline authorization conflict found; all included in regression scan. | Fresh task-acceptance-review; unreported. |
| case 7 | not supplied | Legacy-package refusal pair audited and included in regression scan. | Fresh task-acceptance-review; unreported. |
| cases 8, 9, 10, 11, 12 | not supplied | Each prompt/expectation pair audited and included in regression scan; no additional broad-baseline authorization conflict found. | Fresh task-acceptance-review; unreported. |

## Commands and results

Reviewer reproducer / implementation regression:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-implementation-flow/task-brief-designer/tests -p test_package_resources.py -k test_guides_and_eval_prompts_require_durable_packaged_output
```

The review supplied no executable reproducer command. This derived regression
failed before the prompt correction on case 6's authorization and absent
prohibition; after correction it passed (1 test).

Owning suite:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-implementation-flow/task-brief-designer/tests -p test_package_resources.py
```

Passed: 20 tests. `git diff --check` also passed. These are local source/fixture
implementation checks, not semantic agent-call compliance or independent review.

Broad/aggregate gate: skipped; the authority assigns the projection gate to
T-001.4 and specifies no aggregate command for this invocation. No full repository
suite or reviewer-owned gate was run. Actual role calls remain unrun, owned by T-005.

Optional evidence: `active` returned no open run; `begin` failed on the sandbox's
`.git` snapshot-write restriction. No active run was created; best-effort fallback
was used.

Remaining reviewer coverage: F-01's corrected bytes and sibling prompt agreement
require fresh review. All coverage not supplied in the reviewer report remains
unreported; prior implementation checks in `result.md` are navigation/evidence,
not a reviewer pass.

Deliverables: corrected case-6 prompt, prompt-level regression and this handoff.
Actual contract impact: none beyond restoring the existing AC-05 prompt contract.
Executable contract declarations changed: none.

Next: fresh `task-acceptance-review` on `docs/tasks/T-001.2/brief.md`.
