# F-02 correction submission — T-005.1

Implemented: READY_FOR_REVIEW

- Authority: [docs/tasks/T-005.1/brief.md](https://github.com/trusovn/personal-skills/blob/0ad1706cecc6f7d115e510762bf74c58d732cb6a/docs/tasks/T-005.1/brief.md) and parent [docs/tasks/T-005/brief.md](https://github.com/trusovn/personal-skills/blob/0ad1706cecc6f7d115e510762bf74c58d732cb6a/docs/tasks/T-005/brief.md), evidence rule 3.
- Preflight/context reference: [docs/tasks/T-005.1/preflight.md](https://github.com/trusovn/personal-skills/blob/0ad1706cecc6f7d115e510762bf74c58d732cb6a/docs/tasks/T-005.1/preflight.md); [docs/tasks/T-005.1/verification.md](https://github.com/trusovn/personal-skills/blob/0ad1706cecc6f7d115e510762bf74c58d732cb6a/docs/tasks/T-005.1/verification.md) revision 1; [docs/tasks/T-005.1/reviews/discovery-02.md](https://github.com/trusovn/personal-skills/blob/0ad1706cecc6f7d115e510762bf74c58d732cb6a/docs/tasks/T-005.1/reviews/discovery-02.md); `reviews/discovery-01.md` and the historical results below. Authority/revision/scope are unchanged; the recorded dependency override remains applicable.
- Preceding verdict: no acceptance verdict supplied. Discovery-02 reports V-06 fail / F-02 suggested P2; F-01 is independently corroborated as corrected.
- Finding/scenario IDs: F-01 (prior corrected), F-02 (current correction); V-01, V-02, V-03, V-04, V-05, V-06; S-01/INV-010 and S-02/INV-009/010. All 47 inherited inventory identities and P-01–P-07 remain in fixtures.md, unchanged.
- Complete findings and invariant: F-02 exposed excluded `change-effects/cases.json` through consumer Git history after worktree deletion. Evaluator bytes must remain outside every accessible consumer worktree/index/Git-object surface. F-01's full managed-file/block comparison receipt is preserved without changes.
- Influenced sibling surfaces: directory-based consumer handoffs, Git index and unreachable objects, and T-005.5 manifest reuse. The existing eleven-set assembly check now inspects worktree bytes and every Git blob for each declared held-back record. Route setup preserves all other review files exactly and supplies a new clean Git baseline; later callers must record its new current identities.
- Attempts and discarded hypotheses: reproduced raw staging leak (history retrieval exit 0 before/after deletion; identical JSON). No failed correction attempts or discarded implementation hypotheses. Original evaluator Git data is deliberately retained outside the consumer root. Unsafe original-workspace and unreachable-blob controls are rejected. Exact controls and commands are in `evidence/V-06-consumer-git-exclusion.md`.
- Current scoped diff: `fixtures.md` selects the separate consumer setup/root and defines the access boundary; new `setup_consumer.py` stages the existing fixture and builds that root without original Git data or the key; `tests/test_review_composition.py` extends existing assembly coverage and adds history/index/context-preservation regression; this `results.md` and new V-06 receipt record evidence. All pre-existing staged work, review reports, source skills, installer and active installation remain untouched. No staging, dependency installation, network, role call or reviewer invocation performed.
- Coverage ledger (pre-edit map was stated before correction; prior reviewer statuses are retained):
  - V-01 — prior status: pass; implementation evidence: six focused checks and owning module pass; inventory identity/link/owner and degraded-inventory controls; Incomplete reason: none for implementation checks; next owner/status: fresh discovery / prior pass, navigation only.
  - V-02 — prior status: pass; implementation evidence: none newly run; unchanged `evidence/V-02-setup-reconstruction.md` and discovery-02 DISC-02 are navigation; Incomplete reason: representative public runtime/handoff not renewed in this correction; next owner/status: fresh discovery / prior pass.
  - V-03 — prior status: pass (F-01 corrected); implementation evidence: none newly run; unchanged corrected `evidence/V-03-install-projection.md` is navigation; Incomplete reason: installation unchanged, renewal not needed for this fix; next owner/status: fresh discovery / prior pass.
  - V-04 — prior status: pass; implementation evidence: none newly run; unchanged `evidence/V-04-drift-contrast.md` is navigation; Incomplete reason: installation drift probe not renewed in this correction; next owner/status: fresh discovery / prior pass.
  - V-05 — prior status: pass for bounded local checks; implementation evidence: six focused tests and 22-test owning module pass; inventory/manifest wrong controls plus original-workspace and unreachable-Git-blob controls reject; Incomplete reason: role calls remain unrun by authority; next owner/status: fresh discovery / prior pass, role owners T-005.2–.5.
  - V-06 — prior status: fail / F-02; implementation evidence: eleven input sets stage/resolve, held-back byte retrieval fails in consumer worktrees and all Git objects; raw evaluator history/index retrieval succeeds as wrong control, clean consumer retrieval fails, all remaining review bytes match; Incomplete reason: independent corroboration owed; next owner/status: fresh discovery / prior fail, correction evidence attached separately.
- Reviewer reproducer: discovery-02 DISC-03 exact command is retained in that report; its raw `route-cases` root still returns `0 0 True` as evaluator-only control. Consumer counterpart: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_review_composition.T0051QualificationInputTests.test_route_consumer_excludes_answers_and_preserves_review_context` — 1 test OK, history/index denied in `route-consumer`, review context preserved.
- Owning suite: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_review_composition.py` — 22 tests OK. Targeted class: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_review_composition.T0051QualificationInputTests` — 6 tests OK. These are implementation evidence.
- Broad/aggregate gate: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_review_composition.py` remains owned by fresh independent discovery as a reviewer aggregate; the required implementation owning-suite execution above does not close it. No wider aggregate run. Installer module not rerun: no installer/source/receipt change. No canonical architecture command or contract registry exists.
- Remaining reviewer coverage: no prior unchecked/blocked ledger rows; all six rows require fresh applicability judgment. F-02 corroboration and conditional maintainability evidence are owed. Dependency dispositions remain owed to coordinator/per-package acceptance owners before the T-005.6 audit. All role qualification remains unrun with T-005.2–.5; T-005.6 owns final ART-012 audit.
- Next: fresh separate `task-maintainability-review` → fresh independent `task-review-discovery` → separate fresh `task-acceptance-review`. Significant new task-local setup/test bytes re-enter the owed maintainability stage; no registry/architecture stage applies. This invocation names the route and ends without executing review or issuing acceptance.

Deliverables:
- Task-local route consumer setup, corrected manifest, adversarial Git visibility/context checks and V-06 implementation receipt.

Actual contract impact:
- None: existing shared fixture/installer and ART-009/010/011 contracts preserved; task-local consumer root changes from `route-cases` to `route-consumer` for later qualification leaves.

Executable contract declarations changed:
- None.

Evidence run: `run-20261013T134313Z-d9d654421b26` (project-local sidecar).

The following sections retain earlier submissions as history. Their statements
about remaining coverage and current routes are superseded by this submission.

---

# Implementation results: T-005.1 — Supply reproducible qualification inputs

Submission state: `READY_FOR_REVIEW` (brief metadata `review: immediate`). No
independent review has accepted these bytes; this file records the
implementer's submission evidence only. It now carries the correction round
for `reviews/discovery-01.md` (finding F-01 plus the V-06 preparation owed
by the task owner); the original submission evidence is retained below it.

Evidence runs (shared run-evidence sidecar; availability probe green, begin
at entry, finish at completion): original submission
`run-20261013T124140Z-6d0d923c323d`; correction round
`run-20261013T132116Z-d9e53d04fcf8`.

## Changed paths (corrected submission)

- `tests/fixtures/review-composition/tasks/T-005.1/fixtures.md` — the case inventory (machine-readable
  JSON block: 47 entries), setup conventions, the P-01–P-07 owning-leaf
  table, placeholder-replacement instructions, retained-receipt references,
  and (correction round) the machine-auditable consumer-visible handoff
  input manifests (V-06 preparation).
- `tests/fixtures/review-composition/tasks/T-005.1/evidence/V-02-setup-reconstruction.md` — unchanged
  this round.
- `tests/fixtures/review-composition/tasks/T-005.1/evidence/V-03-install-projection.md` — corrected this
  round for discovery-01 F-01: the independent full managed-projection
  comparison now covers the complete managed file set, all 85 copied file
  bytes and the marked `AGENTS.md` block, records the exact reproducible
  invocation, and demonstrates the marked-block replacement recheck on an
  existing target.
- `tests/fixtures/review-composition/tasks/T-005.1/evidence/V-04-drift-contrast.md` — unchanged this
  round (its drift observation names the changed file via the same
  independent comparison procedure recorded in the corrected V-03 receipt).
- `tests/fixtures/review-composition/tasks/T-005.1/results.md` — this corrected submission record.
- `tests/test_review_composition.py` — the original submission's
  stale-token repair plus the `T0051QualificationInputTests` inventory
  audit; this round adds the handoff-manifest loader/audit
  (`t0051_manifests`, `t0051_manifest_problems`) and two manifest checks
  that stage the claimed input sets and reject a degraded manifest copy.

Inspected and unchanged, with reason: every other path. The user-owned
T-005 registration in `tests/fixtures/review-composition/tasks/index.json` (committed by the user as
`58f5179 T-005 docs`), the pre-existing untracked `.DS_Store` files and the
reviewer's [docs/tasks/T-005.1/reviews/discovery-01.md](https://github.com/trusovn/personal-skills/blob/0ad1706cecc6f7d115e510762bf74c58d732cb6a/docs/tasks/T-005.1/reviews/discovery-01.md) are untouched; the
active `.agents/` installation, source skills, installer declarations and
shared scripts are unchanged (no install/check ran against this repository;
the corrected V-03 probe installed only into a fresh disposable target);
`git diff --check` is clean.

## Deliverables

- **Case inventory (AC-01):** `fixtures.md` enumerates all 24 inherited
  `INV-CASE-01`–`INV-CASE-24` (from the T-002.4 composition), `COMP-01`–`05`,
  `CCR-01`–`08`, the T-003.4 records `ROUTE-01`, `FIND-01`, `ROWS-01`,
  `REV-01`, `EFF-01`, `GATE-01`, `DISP-01`, and the three applicable
  INT-FLOW-001 qualification inputs `IFQ-01`–`03`. Each entry carries setup
  command/environment, disposable workspace, authority, expected oracle,
  inherited identity, producer/consumer, owning T-005 leaf, current owner
  test, evidence level and an explicit unrun role boundary. Parent
  requirements P-01–P-07 are represented with their owning leaves.
- **Current focused test owners (AC-01):** owner tests were resolved after
  TEST-STAB-001 maintenance from the T-002.4/T-003.4 composition records and
  `tests/README.md`; existing staging and result inputs were reused and no
  new composition setup was needed.
- **Disposable installation receipts (AC-02):** fresh disposable Git-target
  install with canonical `--check`, an independent full managed-projection
  comparison covering every managed surface (complete managed file set, all
  85 copied file bytes and the marked `AGENTS.md` block — corrected per
  F-01), a marked-block replacement recheck on the existing target,
  target-local sibling-helper availability, and workflow identity recorded
  as workflow-identity evidence only, distinct from full projection
  identity; plus the fingerprint-excluded drift contrast with byte-exact
  restoration.
- **Consumer-visible handoff input manifests (AC-04, correction round):**
  `fixtures.md` now supplies, for every claimed staged
  producer-to-consumer handoff (T-005.2–.6), the exact consumer-visible
  input set per staged workspace, the evaluator-only exclusions (the
  maintainability grading oracle, the correction-round facts carrying
  expected next-report identity obligations, and the route-cases
  change-effect answer key), the unstaged producer-output positions filled
  only by actual role-call outputs, and the placeholder→raw-actual-output
  mapping with provenance. Staged records remain labeled supplied history;
  evaluator setup code, expected answers and grading oracles stay outside
  the consuming role's inputs.
- **Placeholder replacement instructions (AC-04):** per owning leaf, which
  staged producer placeholder is replaced by which raw actual producer
  output, with preparation references; the machine-auditable manifests above
  make each claimed input set exact.

## Exact commands and results — original submission

All commands ran from the repository root.

| ID | Exact command | Result |
|---|---|---|
| F | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_review_composition.py` (pre-edit fail-first) | FAILED (failures=1, 16 tests): `test_route_matrix_reconciles_supplied_cases_with_public_overviews` asserts the stale token "a production correction re-enters…" against the current Q-01-accepted README bytes — the preflight-recorded pre-existing committed failure, reproduced before any edit |
| T | whitespace-normalized token probe over the three asserted README tuples (root `README.md`, `skills/README.md`, flow README) | exactly two stale tokens: root `README.md` and `skills/README.md` third tuple; all three flow-README tokens verified present in current bytes |
| C | the two stale tuples updated in `tests/test_review_composition.py` to the current committed authority text (Q-01 `677904c`, verdict ACCEPT recorded in [docs/tasks/Q-01/reviews/acceptance-01.md](https://github.com/trusovn/personal-skills/blob/0ad1706cecc6f7d115e510762bf74c58d732cb6a/docs/tasks/Q-01/reviews/acceptance-01.md)) | tokens now byte-exact against current committed README text; flow tuple unchanged |
| N | `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_review_composition.T0051QualificationInputTests` (new inventory checks first, per the brief's verification order) | 3 tests OK |
| M | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_review_composition.py` | 19 tests OK (16 existing incl. the repaired one + 3 new) |
| P1 | `EVAL_WORK_ROOT=/tmp/opencode/t0051-v02-public python3 skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py queue-defect`, then two consecutive public invocations of the staged `src/queue/run_next.py` CLI over disposable probe state | staging exit 0; first invocation stdout `TASK-1` exit 0; second invocation stdout `` exit 0 with `TASK-2` ready (the staged QR-12 defect reproduced at the public CLI boundary); state persisted; no repository bytes written; receipt retained |
| P2 | `EVAL_WORK_ROOT=/tmp/opencode/t0051-v02-handoff python3 skills/task-implementation-flow/task-maintainability-review/evals/files/setup_fixture.py correction-round` | staging exit 0; 57 staged input files (prior durable report with `MNT-B1`–`MNT-B4` + `CHANGES_REQUESTED`, corrected `pricing.py`, correction facts); role call NOT launched; reason and owner (T-005.5) retained; receipt retained; disposable workspaces removed afterwards |
| P3 | canonical `python3 scripts/install_development_skills.py <fresh disposable committed Git target>` + `--check`, then the independent managed-projection byte comparison and target-local helper/identity probes | install exit 0; check exit 0 `match=True compared=86 differences=[]`; independent comparison 85/85 copied managed files byte-identical; helper availability `available: true`; workflow fingerprint equal (workflow identity only); receipt retained — **superseded this round by command C2, which independently compares the complete projection including the marked block (F-01)** |
| P4 | in that target only, append one newline to `.agents/skills/task-implementation-flow/bounded-task-implementer/evals/evals.json`; recheck; restore byte-exactly; recheck | workflow fingerprint still equal (fingerprint-excluded drift); `--check` exit 1 naming exactly that path; check repaired nothing; snapshots unchanged across the read-only checks; restored → check exit 0 `match=True`; no fault left; disposable target removed; receipt retained |
| S | `git diff --check` | clean |

## Exact commands and results — correction round (discovery-01)

All commands ran from the repository root.

| ID | Exact command | Result |
|---|---|---|
| E2 | staging enumeration: `EVAL_WORK_ROOT=/tmp/opencode/t0051-correction-manifest/<scenario> python3 <fixture> <scenario>` for `queue-defect`, `integration-leaf`, `mixed-conditions-authorized-decision`, `contextual-risk-blockers-decision`, `known-issue-consumption-decision`, `four-blockers`, `correction-round`, `route-cases`, `record-correction`, `discovery-late-omission-clean` | all 10 stagings exit 0; complete file trees enumerated and classified into consumer-visible inputs, evaluator-only records and unstaged producer-output positions (the exactness basis for the manifests; discovery-01's V-06 preparation direction) |
| C2 | the corrected V-03 independent full managed-projection comparison probe — the exact reproducible invocation recorded in `evidence/V-03-install-projection.md` (canonical install + read-only `--check`, independent managed file-set equality, 85-file byte comparison, independent marked-block extraction/comparison, unmanaged-prefix/suffix preservation, block-drift check, block replacement recheck, target-local helper availability, workflow identity) | ALL OK (16 reported steps, zero failures): expected 86 = actual 86 managed paths, missing=[] extra=[]; 85/85 byte-identical; extracted block equals `installer.AGENTS_BLOCK.rstrip()`; unmanaged prefix incl. terminal trailing whitespace preserved; tampered block → `--check` exit 1 naming `AGENTS.md` → reinstall → replaced block independently equals canonical again → recheck `match=True`; helper `available: true` from the target's own `.agents/scripts`; installed fingerprint equals source (workflow identity only); disposable target removed; this is the F-01 reviewer-regression direction (rerun of the discovery probe's full independent block/file comparison) over the corrected receipt |
| N2 | `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_review_composition.T0051QualificationInputTests` (changed/new checks first) | 5 tests OK (3 original inventory checks + 2 new manifest checks; the resolving check stages all 10 fixture-backed input sets and verifies every consumer-visible input, evaluator-only record and unstaged position against real staged trees) |
| M2 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_review_composition.py` (nearest owning suite) | 21 tests OK (19 previous + 2 new) |
| S2 | `git diff --check` | clean |

Fail-first/discrimination evidence retained from the original submission
(command F/T/C plus the inventory audit's wrong control), and extended this
round: the manifest audit's wrong control (dropped T-005.4 handoff row,
undeclared staging ref, unresolvable preparation reference, nonexistent
consumer input path, reclassified held-back correction facts, stale fixture
scenario, orphaned staged set) is rejected problem-by-problem while the
real manifests stay clean against the same oracle and the same staged
roots.

## Correction record (reviews/discovery-01.md)

- **F-01 [suggested P2] — broken invariant:** retained full-projection
  receipts must cover every canonical managed surface with independent
  byte/file-set evidence, separately from a matching CLI check and workflow
  identity. The V-03 receipt compared only the 85 copied files independently
  and attributed the marked `AGENTS.md` block to `--check`, and recorded no
  reproducible invocation for the independent comparison.
- **Correction:** command C2 re-ran the disposable installation evidence
  with a complete independent comparison — managed file-set equality (86
  paths), byte equality for all 85 copied files, and independent
  marked-block extraction compared with `installer.AGENTS_BLOCK.rstrip()` —
  and the corrected receipt records the exact reproducible invocation and
  complete results, keeping `--check`, unmanaged-preservation and
  workflow-fingerprint claims separate. The invariant's credible sibling
  surfaces named by the finding are covered: the marked block is rechecked
  after replacement in an existing target (demonstrated), and the recorded
  procedure is the canonical renewal procedure for later T-005 call leaves.
  No installer or shared-helper repair was made or indicated.
- **V-06 (unchecked row) — preparation supplied:** the discovery report
  routes the remaining V-06 evidence to "fresh discovery after preparation
  of explicit input manifests/sets by task owner". This round supplies that
  preparation: the machine-auditable consumer-visible handoff input
  manifests in `fixtures.md` (command E2 basis, command N2 audit). The
  independent assembly of the remaining consumer input sets stays with fresh
  discovery; this leaf claims preparation only, not V-06 closure.

## Coverage ledger (discovery-01 rows; correction evidence attached to failed/unprepared rows, reviewer statuses unchanged)

| Row | Prior status | This round's implementation evidence | Reviewer status carried forward |
|---|---|---|---|
| V-01 | pass | navigation context only — no inventory identity/selector bytes changed this round; audit rerun green in N2/M2 | unchanged; fresh discovery re-verifies over corrected bytes |
| V-02 | pass | navigation context only — receipts untouched this round | unchanged; fresh discovery |
| V-03 | fail (F-01) | C2 + corrected `evidence/V-03-install-projection.md`: complete independent managed-projection comparison incl. marked block, reproducible invocation, replacement recheck; `--check`/fingerprint/preservation separate | failed row with correction evidence attached; fresh discovery reruns the full independent block/file comparison over the corrected bytes |
| V-04 | pass | navigation context only — receipt unchanged; its drift comparison is the same procedure recorded in the corrected V-03 receipt | unchanged; fresh discovery |
| V-05 | pass | changed/new checks first (N2), owning suite green (M2) | unchanged; fresh discovery owns any justified aggregate of changed test owners |
| V-06 | unchecked | preparation only: explicit consumer-visible input manifests + evaluator-only exclusions + unstaged positions per claimed handoff (E2/N2 audited); remaining consumer-set assembly not performed here | unchanged (unchecked); fresh discovery assembles the remaining handoffs from these manifests, keeping evaluator-only facts out |

## AC and scenario evidence

Implementation evidence, not independent acceptance. Every verification
scenario of [docs/tasks/T-005.1/verification.md](https://github.com/trusovn/personal-skills/blob/0ad1706cecc6f7d115e510762bf74c58d732cb6a/docs/tasks/T-005.1/verification.md) (revision 1) is accounted
for.

| AC / scenario | Evidence (command, setup/oracle, result) |
|---|---|
| AC-01 / V-01 / S-01 | `fixtures.md` inventory (47 identities) audited by N2/M2: every inherited case, record and applicable INT-FLOW input resolves to setup, workspace, authority, oracle, producer/consumer, owning leaf, owner test and evidence level or an explicit gap; cross-checked against the T-002.4/T-003.4 composition records, current fixture scenario dispatch, `tests/fixtures/review-composition/tasks/index.json` leaf registration and evidence pointers; P-01–P-07 represented with owning leaves — OK. Omitted-mapping variant (V-01): the wrong control identifies a dropped mapping, a stale selector and an unresolved pointer rather than accepting green rows — OK |
| AC-02 / V-03 / S-02 | command C2 + corrected `evidence/V-03-install-projection.md`: fresh disposable committed Git target; canonical install + read-only `--check` match over 86 managed paths; independent full managed-projection comparison — complete managed file-set equality, 85/85 copied-file byte identity, and independent marked-block equality against `installer.AGENTS_BLOCK.rstrip()` — with the exact reproducible invocation retained; marked-block replacement recheck on the existing target; target-local sibling `.agents/scripts/` helpers available (`available: true`, `scripts_root` inside the target); workflow fingerprint equal but recorded as workflow-identity only; unmanaged target bytes and the active installation unchanged; target HEAD stable — OK |
| AC-02 / V-04 / S-02 | command P4 + `evidence/V-04-drift-contrast.md` (unchanged): fingerprint-excluded copied eval file changed in the target only; workflow identity still matches while `--check` exits 1 naming the exact path; snapshots around the read-only observation; byte-exact restoration then matching recheck; no fault left — OK |
| AC-01, AC-03 / V-02 / S-01 | commands P1/P2 + `evidence/V-02-setup-reconstruction.md`: one public-boundary case (INV-CASE-01 `queue-defect`) reconstructed in a fresh disposable workspace with its public probe observed at the real CLI boundary; one unrun handoff (IFQ-01 `correction-round`) reconstructed with all 57 input files present, retained unrun with reason and owner; existing staging reused; no role call launched — OK |
| AC-01, AC-03 / V-05 / S-01 | commands F/T/C/N/M (original) + N2/M2 (correction): the focused module's red-at-HEAD stale tokens were reproduced first, narrowed mechanically, repaired to the current Q-01-accepted committed bytes, and the module is green (21/21); the new checks discriminate good/wrong fixture behavior via the audits' wrong controls; no unrun check is claimed as green and no staged report is relabeled — OK |
| AC-01, AC-04 / V-06 / S-01 | **partial — preparation supplied, assembly owed to fresh discovery.** Supplied: the consumer-visible handoff input manifests in `fixtures.md` (per owning leaf: exact staged input sets, consumer-visible paths, evaluator-only exclusions with reasons, unstaged producer-output positions with producing roles, placeholder→raw-actual mapping), audited at the real staged boundary by N2 (all 10 fixture-backed sets staged; every listed path resolves; held-back records and answer keys classified evaluator-only; unstaged positions verified genuinely unstaged) with a wrong control rejecting a degraded manifest copy. Original evidence retained: the placeholder-replacement table, the IFQ-01 reconstruction (P2 receipt) and `test_unrun_role_boundaries_and_receipt_references_stay_visible`. Not claimed: independent assembly of every remaining consumer input set (discovery-01 leaves that evidence to fresh discovery) and any role behavior |

## Filesystem/Git proof versus unrun behavior

Everything above is filesystem/Git/CLI proof: real fixture staging, real
installer/check calls in disposable local Git targets, byte comparisons and
snapshots. No skill invocation, role call, model-budget or live check was
run or claimed; those boundaries stay unrun with their owners (T-005.2–.5
role calls; T-005.6 cross-child audit and ART-012). The preflight's carried
warning remains: no acceptance-decision artifact exists yet for T-001.4,
T-002.4, T-003.4, T-004.1–.3, INT-FLOW-001 or TEST-STAB-001.1/.2; the user
override that authorized this task does not record those dispositions, and
commit-message "(accepted)" labels are not decision artifacts. Actual
contract impact:

- added/changed/removed durable cross-task surface: none (task-local
  qualification inputs, receipts and focused test additions only;
  ART-009/010/011 contracts and existing fixture contracts preserved; inputs
  supplied for ART-012; no `docs/contracts` registry exists and none was
  created).
- Executable contract declarations changed: none.

## Local decisions (reversible, task-local)

- Original submission's decisions (owning-leaf assignment per inherited
  case; evidence-level assignment per composition categories; the inventory
  JSON embedded in `fixtures.md` with a shared audit oracle; the two-tuple
  stale-token repair) are retained.
- Correction round: the corrected V-03 receipt records the complete
  independent comparison as one reproducible inline invocation reusing the
  owning suite's helpers, instead of adding a new script or shared harness
  (no shared infrastructure was created).
- The manifest structure separates staged input sets (per scenario) from
  handoff rows (per owning leaf) so one staging shared by several handoffs
  is declared once; consumer assembly is defined as `consumer_visible_inputs`
  minus `evaluator_only` paths.
- Evaluator-only classifications follow each fixture's own held-back
  contract and the discovery finding: the maintainability grading oracle and
  the correction-round facts (which carry expected next-report identity
  obligations) stay outside reviewer inputs, and the route-cases
  change-effect `cases.json` (expected submission routes) is excluded from
  consumer inputs; `record-correction`'s `authority/` anchored record is
  consumer-visible because the staged tests themselves consume it.
- The installer-owner module (`test_install_development_skills.py`) was not
  re-run this round: installer, declaration and selected source-profile
  bytes are unchanged by this task, and the corrected C2 probe exercises the
  real installer/CLI boundary directly; renewal is needed only when source
  or installer bytes change.

## Remaining obligations and carried warnings

- Owed dependency acceptance dispositions (see preflight warning) — owners:
  fresh `task-acceptance-review` decisions per package, before T-005.6's
  ART-012 audit; carried forward to every consuming leaf.
- V-06 independent assembly of the remaining consumer input sets — owner:
  fresh `task-review-discovery` over these corrected bytes, assembling each
  claimed handoff from the supplied manifests and keeping evaluator-only
  facts out.
- All actual role calls, conditional-stage calls, durable-report writing and
  behavioral qualification — unrun, owners T-005.2–.5; T-005.6 owns the
  final audited report. This leaf's outputs are inputs only.
- Conditional maintainability review of the corrected bytes (the correction
  adds significant new test/fixture code — the manifest data, loader/audit
  and two staging checks) — see the review handoff below.

## Review handoff

Per `review: immediate` and the correction route, the corrected bytes go
next, in order, to: a fresh `task-maintainability-review` of the changed
bytes (applicable: this correction round adds significant new
test/fixture/harness code — the machine-readable manifests, the shared
manifest audit oracle and the two staging checks; discovery-01 records that
this conditional stage remains separately owned and owed for these bytes),
then fresh independent `task-review-discovery` (rerunning the F-01 full
independent block/file comparison and assembling the remaining V-06 consumer
sets from the supplied manifests), then its report to a separate fresh
`task-acceptance-review`. Conditional-stage judgment: no canonical
deterministic architecture command is declared in this repository (no
architecture gate to run), and no `docs/contracts` registry exists (the
registry stage is absent, not skipped); fresh reviewers may challenge this
judgment. Naming this route does not execute it; the implementer invocation
ends here without a self-issued verdict.