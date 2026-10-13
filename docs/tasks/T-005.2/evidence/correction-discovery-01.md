# T-005.2 correction record — discovery-01 F-01 (raw-retention claim)

Author: `bounded-task-implementer` correction invocation (evidence run
`run-20261013T145730Z-4d9df458d8aa`). This file is implementation evidence
for the correction; it is not an acceptance verdict. It corrects the reviewed
submission bytes (`results.md`, `evidence/run-log.md`,
`evidence/preparation-and-recovery-observations.md`,
`evidence/unrun-role-boundaries.md`) in the worktree only — nothing staged.

- Authority: `docs/tasks/T-005.2/brief.md`
  (SHA-256 `794247bc…91c77`), parent `docs/tasks/T-005/brief.md` evidence
  rules 1–7, `docs/tasks/T-005.2/verification.md` revision 1
  (SHA-256 `85f58c81…4431b`), `docs/tasks/T-005.2/preflight.md` (ready).
- Preceding verdict: `docs/tasks/T-005.2/reviews/discovery-01.md` — coverage
  partial; F-01 confirmed (suggested P2); V-07 `fail`; V-01/02/03/04/05/06 and
  V-07-Q `blocked`; V-01-A, V-05-H, V-06-F, V-07-U, SCOPE `pass`. Correction
  owner for F-01 = implementer.
- Finding/scenario IDs: F-01; ledger rows V-01, V-01-A, V-02, V-03, V-04,
  V-05, V-05-H, V-06, V-06-F, V-07, V-07-U, V-07-Q, SCOPE.

## Broken invariant

Parent evidence rule 3 and V-07: raw producer output must be preserved before
grading and consumed by reference; a summary, hash, or begin/finish snapshot
does not replace the actual capture. The submission claimed
"verbatim bytes retained in `evidence/run-log.md`" (P2), "captured-before-
grading control bytes" (AC-04 deliverable), and "Observed pass" for V-01 and
V-07, while both `/tmp/opencode/t0052*` raw roots were removed and the full
control bytes are absent from every retained file. The historical capture
cannot be recovered; recreating the deterministic fixtures would establish
new observations, not preservation of the earlier run's raw output.

## Credible sibling surfaces corrected (complete)

- `results.md` P2 row: "verbatim bytes retained" → corrected gap statement.
- `results.md` AC-04 deliverable: "captured-before-grading control bytes" →
  not-retained statement.
- `results.md` AC-01 deliverable: added retained-proof-level caveat
  (artifact identity only; raw invocation outputs not retained).
- `results.md` AC-01/V-01 row: "Observed pass" → "Corrected (F-01) —
  artifact-level evidence only, no observed pass for the chain".
- `results.md` AC-03/V-05 row: "captured verbatim" → "regenerable
  deterministically … not retained, F-01"; "observed T-005.2 chain" →
  "artifact-level, F-01 provenance gap".
- `results.md` AC-04/V-07 row: "Observed pass" → "Corrected (F-01) — no
  observed pass for raw retention", with retained vs not-retained split.
- `results.md` INT-FLOW-001 I-04 note: "observed preparation-reference chain"
  → "artifact-level … raw consumer-read records not retained — F-01".
- `results.md` filesystem/Git paragraph: "receipts retained identities and
  decisive bytes" → truthful split + pointer to this file.
- `evidence/run-log.md` probe 2: "captured verbatim" heading and body →
  "capture NOT retained (F-01 correction)" + regenerability note; final
  removal paragraph corrected.
- `evidence/preparation-and-recovery-observations.md` V-01: added
  retained-proof-level caveat; V-05: "captured verbatim in `run-log.md`" →
  not-retained; V-05 "Observed:" paragraph → "Structural (regenerable;
  F-01 correction)" with the artifact-level package-chain caveat.
- `evidence/unrun-role-boundaries.md`: observed-level definition and the
  workspace-removal sentence corrected (staged control bytes not retained).

Unchanged honest content: staging identities table, exit codes, the eight
transition Git boundaries, the P1 freshness-probe values (genuinely retained
in `run-log.md` probe 1 — discovery V-06-F pass), the complete unrun ledger
(V-07-U), and all structural/owner-test claims.

## Coverage ledger — row-to-evidence map (pre-edit gate)

| Row | Prior status (discovery-01) | This correction's evidence | Next owner / status |
|---|---|---|---|
| V-01 | blocked | Claim-strength corrected in `results.md` + `preparation-and-recovery-observations.md`; no role call run by this correction (no authorization) | Coordinator supplies call records; fresh discovery corroborates. Reviewer status unchanged (blocked) |
| V-01-A | pass | Navigation only; artifact hashes unchanged and independently confirmed by discovery | Fresh discovery |
| V-02 | blocked | Navigation only; staged control claims unchanged structurally, capture claims corrected | Coordinator role calls; reviewer status unchanged |
| V-03 | blocked | Navigation only | Coordinator; reviewer status unchanged |
| V-04 | blocked | Navigation only | Coordinator; reviewer status unchanged |
| V-05 | blocked | Sibling capture claim corrected (results.md, observations V-05) | Coordinator + preparation/proof/decision owners; reviewer status unchanged |
| V-05-H | pass | Navigation only | Fresh discovery |
| V-06 | blocked | Navigation only; P1 values retained and untouched | Coordinator; reviewer status unchanged |
| V-06-F | pass | Navigation only | Fresh discovery |
| V-07 | fail (F-01) | **Corrected:** every unsupported retention/observed-pass claim downgraded to an explicit gap; retained set documented honestly; correction record added | Fresh discovery re-audits (reviewer regression DISC-02); acceptance decides |
| V-07-U | pass | Navigation only | Fresh discovery |
| V-07-Q | blocked | Navigation only; qualification receipts remain preflight/coordinator owned | task-preflight/coordinator; reviewer status unchanged |
| SCOPE | pass | Correction confined to the four reviewed files + this new `evidence/` record; unstaged per user instruction; `git diff --check` clean | Fresh discovery |

No blocked/unchecked row is silently dropped. Prior passes are navigation
context, not acceptance evidence for the corrected bytes.

## Attempts and discarded hypotheses

- Hypothesis (discarded): re-run the 16 stagings to re-capture the control
  bytes. Discarded because discovery F-01 states regeneration establishes new
  observations, not preservation of the earlier run's raw output; the claim
  strength must be corrected regardless, and no new role-call campaign is
  authorized (parent rule 4).
- Confirmed fact: `/tmp/opencode/t0052` and `/tmp/opencode/t0052-raw` are
  absent; the original run manifest
  `.git/personal-skills/run-evidence/runs/run-20261013T143605Z-d20d1908061f/manifest.json`
  has `checks: []` and no captured evidence. Historical capture is
  unrecoverable; the gap declaration is the only truthful correction.

## Current scoped diff

Worktree-only edits (not staged, per user instruction):

- `docs/tasks/T-005.2/results.md` — 9 claim corrections (P2, AC-01/AC-04
  deliverables, V-01/V-05/V-07 rows, I-04 note, filesystem paragraph,
  run-log description).
- `docs/tasks/T-005.2/evidence/run-log.md` — probe-2 heading/body and removal
  paragraph corrected.
- `docs/tasks/T-005.2/evidence/preparation-and-recovery-observations.md` —
  V-01 caveat, V-05 capture/observed corrections.
- `docs/tasks/T-005.2/evidence/unrun-role-boundaries.md` — observed-level
  definition and removal sentence corrected.
- `docs/tasks/T-005.2/evidence/correction-discovery-01.md` — this record
  (new).

No production, test, fixture, harness, installer, source-skill, or
active-installation byte changed.

## Verification performed

- Reviewer regression DISC-01 (six focused fixture tests): ran, all OK.
- Reviewer regression DISC-02 variant (retention/provenance audit): ran —
  raw roots absent; corrected reports now declare the gap explicitly and no
  longer claim verbatim retention; fixture regeneration confirms the staged
  history/intact original bytes (same as discovery).
- `git diff --check` / status: clean; only the corrected files differ from
  the staged index, plus this new record; the three untracked `.DS_Store`
  user files untouched.

## Next

Fresh independent `task-review-discovery` evidence over these corrected
bytes, then a separate fresh `task-acceptance-review` decision. Naming this
route does not execute it; this implementer invocation ends without a
verdict.
