# Task Review Discovery Report: T-001 — Audit preservation and retirement eligibility

| Field | Value |
|---|---|
| Producing stage | `task-review-discovery` |
| Coverage completeness | `partial — the reviewed submission (results.md 798906e8…) is unchanged since discovery-03 and is still authored under verification revision 1; a revision-2-authorized correction has not been applied. The refreshed preflight is ready and is the material new context.` |
| Discovery iteration | Fourth independent discovery; second under verification revision 2 |
| Created at | `2026-10-14T16:27:00Z` |
| Repository root | `/Users/mtrusov/work/skill-sources/personal-skills` |
| Durable report path | `ideas/documentation-consolidation/tasks/T-001/reviews/discovery-04.md` |
| Task brief | `ideas/documentation-consolidation/tasks/T-001/brief.md` (SHA-256 `94cc2e18…`, revision 2 authority) |
| Verification design / task context | `ideas/documentation-consolidation/tasks/T-001/verification.md` revision 2 (`962a9b13…`); `ideas/documentation-consolidation/tasks/T-001/preflight.md` (`e30752d7…`, revision-2 refresh); prior reports `reviews/discovery-01/02/03.md`; cleanup-v1 `project-plan.md` / `task-map.json` |
| Current submission | `ideas/documentation-consolidation/tasks/T-001/results.md`, SHA-256 `798906e82414c4c25f16e994a508e63e4eef2806c067ea6953b02347b23407ee` (worktree = index blob `8ee24f00…`); declares `NON-COMPLETE`, overall `BLOCKED` |

This report publishes evidence only. It contains no acceptance verdict, no
approved deferral, and no advancement. The separate acceptance decision call
consumes it. It applies only to the reviewed bytes identified below; any
correction requires a new discovery report. This report does not review or
authenticate itself.

## 1. Discovery provenance

| Question | Evidence |
|---|---|
| Did this session author any reviewed production bytes? | `no — independent`. This session created no submission, preparation, prior-report or tracked byte. Its only repository write is this report. |
| Independent evidence authority | `yes` — fresh session, no authorship of the reviewed diff. |
| Current byte identity | HEAD `b65f900e7515ccfe36335b793b0c058b7b2bfa8c` (tree `5bd4772805fd7aa5160c1b641bc8417944925017`); reviewed submission `798906e8…`; raw index `22161aeabf…`, normalized index `cf47b13b…`; normalized refs `bab2e328…` |

Selected skill: `task-implementation-flow/task-review-discovery`. Its sibling
`references/discovery-report-template.md` supplied this format. No installation
refresh, subagent, optional evidence lifecycle, fixture process, consumer suite,
network operation or git side effect was performed by this discovery.

## 2. Findings, ordered by suggested severity

The submission bytes are identical to those reviewed by discovery-03; F-01–F-03
are preserved with their prior statuses and re-corroborated against the current
repository state. F-04 and F-05 are newly observed on the current bytes.

### F-02 [suggested P1] Three included preservation originals have obsolete identities and the index/ignored baselines are stale

| Field | Evidence |
|---|---|
| Finding ID | `F-02` (prior ID preserved; prior status `fail` in discovery-03) |
| Suggested severity | `P1` |
| Current location | `results.md:55–71` (baseline/ignored block) and `:622–624` (rows for `tasks/T-001/brief.md`, `preflight.md`, `verification.md`) |
| Triggering state/input | Consume ART-002 after `brief.md` (revision 2), `verification.md` (revision 2) and the refreshed `preflight.md` were edited in the worktree. |
| Consequence | T-002 would freeze wrong byte identities for included preservation inputs. The manifest's assertion that the included preparation rows have identical HEAD/index/worktree versions is false for current bytes, and its recorded index and ignored-set baselines no longer describe the repository. |
| Evidence | DISC-01 finds exactly three `identity` and three `versions` problems, all on these paths. Current worktree: `brief.md` `94cc2e18…`/16836 B, `verification.md` `962a9b13…`/16095 B, `preflight.md` `e30752d7…`/15969 B; current index blobs `62e32efa…`, `46664958…`, `3d4c3ee7…`. Manifest rows record `5f417e6d…`/16049 B, `bbeafc7a…`/15163 B, `9d79cb44…`/12830 B with HEAD blobs `bea1daa9…`, `15e7f391…`, `81c33d33…`. Recorded ignored set is 159 paths incl. `2 docs`; current ignored set is 155 (`89 .agents, 1 .handoff, 4 .pytest_cache, 7 scripts, 33 skills, 21 tests`). |
| Affected AC | AC-01, AC-05 |
| Broken invariant | Current intended originals must carry exact version identity, and changed inputs invalidate facts that depend on them (R-01/R-04, INV-001/INV-006). |
| Credible sibling surface | Any later-changed preparation or task-report asset included under Q-001, especially untracked additions T-002 must freeze. This surface is now realized: the revision-2 `preflight.md` is a third stale included row, beyond the two named in discovery-03. |
| Smallest corrective direction | Reconcile the whole current Git/index/worktree inventory and update the preservation identities plus the drift account for the entire affected inclusion set, retaining distinct index and worktree versions where they differ. |

### F-04 [suggested P2] Protected Git index drifted after the output; the task package is now staged outside the audit's write boundary

| Field | Evidence |
|---|---|
| Finding ID | `F-04` (new) |
| Suggested severity | `P2` |
| Current location | Repository index; `results.md:55–71`, `:284–291` (final identity claim), `:380–387` (correction comparison) |
| Triggering state/input | Inspect AC-05 (index preservation) against the current index after the reviewed output was authored. |
| Consequence | AC-05's "Git index … remains unchanged" oracle is not satisfied for current bytes; the submission's claims that HEAD/index/refs equal the recorded baseline (`71e86e4b…`, `7a225e39…`, refs `9ae5a239…`) are now false. Seven paths are staged (three modifications, four additions), which the brief lists as out-of-scope "staging files". Attribution is not established by the reviewed output. |
| Evidence | `git diff --cached --raw` shows only `ideas/documentation-consolidation/tasks/T-001/`: `M brief.md`, `M preflight.md`, `M verification.md`, `A results.md`, `A reviews/discovery-0{1,2,3}.md`; unstaged diff empty. Current raw index `22161aeabf…` vs recorded `7a225e39…`; normalized index `cf47b13b…` vs recorded `71e86e4b…`; tracked entries 521 vs the manifest's 517 rows; normalized refs `bab2e328…` vs recorded `9ae5a239…`. No staged path exists outside the task directory, and no audited input bytes changed. |
| Affected AC | AC-05 |
| Broken invariant | Audited inputs and Git index remain unchanged; task write scope does not include staging (R-04, INV-006). |
| Credible sibling surface | Any later ref/index mutation: the four added task/review index entries, the three modified preparation blobs, and the ref namespace as a whole. Authorized `refs/personal-skills/run-evidence/` instrumentation is a distinct, permitted sibling class (92 namespaced refs vs 40 protected refs outside the namespace). |
| Smallest corrective direction | Do not reset, restage or overwrite to restore a baseline. Record the index/ref drift as current fact, attribute it separately from authorized namespaced instrumentation, and re-establish protected-state baselines on the current bytes. |

### F-03 [suggested P2] Submission's AC-05 / overall disposition still applies the superseded ref rule

| Field | Evidence |
|---|---|
| Finding ID | `F-03` (prior ID preserved; prior status `fail` in discovery-03) |
| Suggested severity | `P2` |
| Current location | `results.md:3` (summary), `:300–324` (final ref exception), `:326–407` (F-01 correction) |
| Triggering state/input | Consume the audit under current brief AC-05 and verification revision 2. |
| Consequence | The output declares itself `NON-COMPLETE` because a run-evidence finish ref was written and states the correction "excludes all evidence lifecycle operations" under the former stricter boundary, although current authority expressly authorizes `refs/personal-skills/run-evidence/` and requires its effects to be attributed separately. The AC-05 disposition and handoff mislead the reader about what is actually prohibited. |
| Evidence | Brief AC-05 and verification V-05 revision 2 permit the namespace; the disclosed finish ref is inside it and `results.md` itself attributes it to the helper (`.agents/scripts/run_evidence.py:284` `update-ref`). Current protected refs outside the namespace = 40; namespaced = 92. Prior F-01 was a revision-1 finding, not a current-rule violation. |
| Affected AC | AC-05 |
| Broken invariant | Report protected-state changes separately from authorized instrumentation and apply current authority to the assessment (R-04, INV-006). |
| Credible sibling surface | Begin and recovery snapshot refs, metadata, and snapshot objects receive the same revised treatment; changes to files, index or refs outside the namespace remain prohibited. |
| Smallest corrective direction | Reconcile the occurrence against revision 2, attribute the authorized instrumentation separately, and restate only the current AC-05/scenario/overall claims after current protected-state checks. |

### F-05 [suggested P3] Four `.DS_Store` inputs are labelled "ignored" but are untracked and not ignored

| Field | Evidence |
|---|---|
| Finding ID | `F-05` (new) |
| Suggested severity | `P3` |
| Current location | `results.md:62–71`, `:75–78` |
| Triggering state/input | Reconcile AC-01's untracked/ignored input classification. |
| Consequence | The exclusion decision stands, but the classification is factually wrong: these are untracked-unignored files, and the "Full ignored listing: 159 paths" statement conflates the untracked set with the ignored set. A consumer trusting the label may mis-apply `.gitignore` semantics. |
| Evidence | `git check-ignore -v` on all four `.DS_Store` paths exits 1 (not ignored); `git ls-files --others --ignored --exclude-standard` returns 155 paths that exclude them; `git ls-files --others --exclude-standard` returns exactly the four `.DS_Store`. Appendix B confirms the four `.DS_Store` byte identities and the `.handoff` identity still match the recorded exclusion table. |
| Affected AC | AC-01 |
| Broken invariant | Relevant untracked and ignored inputs are recorded explicitly and correctly (R-01). |
| Credible sibling surface | The `.handoff/` exclusion (genuinely ignored) and any other untracked-but-not-ignored artifact under the candidate/preservation roots. |
| Smallest corrective direction | Reclassify these inputs as untracked-not-ignored while keeping the EXCLUDE reason and identities; keep the untracked and ignored sets distinct. |

### F-01 [historical; applicability superseded by revision 2] Optional instrumentation wrote snapshot refs

F-01 (discovery-01/02) is retained as historical revision-1 evidence: the
original occurrence wrote `refs/personal-skills/run-evidence/…` refs via
`git update-ref`. Under current brief AC-05 and verification revision 2 that
namespace is authorized instrumentation and is not itself a current violation.
Its disposition remains with separate acceptance/owner authority; it must not be
erased or relabelled retroactively.

## 3. Completeness ledger

Row IDs V-01–V-06 are the stable verification-design scenarios and cover every
AC and finite-risk row (R-01–R-04). Prior `pass` results guided probe selection
but are not current proof; every row below was re-examined against current bytes.

| Row ID | AC / invariant | Explicit material cases | Setup / oracle | Submitted evidence | Independent probe / current evidence | Result / reason |
|---|---|---|---|---|---|---|
| V-01 | AC-01; R-01/INV-001, INV-006 | Tracked unchanged/staged/unstaged/untracked/ignored; index↔worktree divergence; modes/types; external-content boundary; candidate vs retained membership | Rebuild scoped inventory from Git objects/index and filesystem; compare membership, versions, hashes, modes, decisions | 517 INCLUDE rows, 182 candidates, five exclusions; claims all versions identical | DISC-01: 521 tracked entries, 517 manifest rows, `extra=[]`, 182 candidates, 15 future files; problems = 3×`identity` + 3×`versions` on `brief.md`/`verification.md`/`preflight.md`; 4 tracked entries (results + three reports) absent from the manifest. No symlink/gitlink/divergence, no `.gitmodules`/`.gitattributes`, no candidate LFS pointer | **fail** — F-02; current worktree identities and index/ignored baselines absent or wrong |
| V-02 | AC-02, AC-04; R-02/INV-004, INV-006 | `docs/tasks/`, old plan, old map; completed/unfinished/unknown; retained `future-work` incl. `stale/` and old plan review | Reconcile each family with original report/verdict/obligation; unknowns cannot appear eligible | Family evidence/disposition table; unknowns preserved; Q-003 disposition | DISC-02: all 32 directories present, none omitted; original verdicts hold (T-005.2 `INCONCLUSIVE`, T-005.3 partial, T-005.6 documentary `ACCEPT`, Q-01 unrun qualification). All 15 future-work files and old plan review remain outside retirement | **pass** for current candidate evidence; incomplete qualification is not upgraded |
| V-03 | AC-03; R-03/INV-003 | Executable reads, fixture/setup closure, active navigation, historical-only references, owners/oracles/selectors | Trace real readers through constants, embedded data, setup roots; compare with existing coverage/helpers | 13 live candidate inputs; composition selector; migration owners | DISC-02: 47 cases, 11 staged sets, 5 handoffs, no embedded existing candidate missing from inventory. DISC-04 corroborates `tests/test_review_composition.py:34–37,62–64` constants, `docs/tasks/T-005.1/setup_consumer.py:10` `parents[3]`, and `tests/README.md:24,40` owner/selector. Installer sources contain no candidate path | **pass** for current consumer source; migration equivalence remains unclaimed |
| V-04 | AC-04; R-02/INV-004, INV-006 | Q-001–Q-003 sources; per-candidate and global gates; overall assessment | Compare decisions with cited owner sources; reconcile blockers with rows | Q-001/Q-003 owner replies; Q-002 recommendation only; all candidates gated; overall `BLOCKED` | DISC-03: proposed local tag absent; `origin` exists with no publication proof; candidate archive/dependency gates and overall `BLOCKED` remain consistent. Q-001/Q-003 sourced from discovery-01 §3 durable record; no silence/plan acceptance treated as authority | **pass** for owner gates; Q-002 stays a downstream owner/T-002 gate |
| V-05 | AC-05; R-04/INV-006 | Audit start→write→final: protected files/index/refs-outside-namespace; namespaced instrumentation attributed | Compare actual before/after state and claimed disposition | Original namespaced finish ref disclosed but classified as a violation; correction excludes the lifecycle | DISC-01/DISC-03 confirm protected candidate bytes and 40 protected refs outside the namespace; 92 namespaced refs are authorized instrumentation. Current index is staged (`22161aeabf…` vs recorded `7a225e39…`). Submission AC-05 disposition still uses the superseded rule | **fail** — F-03 (assessment under superseded rule) and F-04 (index/protected-state drift) |
| V-06 | AC-05; R-04/INV-006 | Observed drift invalidates affected facts; reinspection uses current bytes; no restoring user files | Compare recorded initial/final identities with actual state; trace affected rows to reinspection or blocker | Correction claims stable old brief/verification bindings and no drift | Current `brief.md`/`verification.md`/`preflight.md` bytes differ from manifest/index; no corrected ART-002 reinspects them. Ref baseline moved `9ae5a239…`→`bab2e328…`; index moved. No user file was restored or overwritten | **fail** — F-02 and F-04; changed inputs not yet reinspected |

## 4. Adversarial state and evidence checks

| Ledger row / invariant | Cases exercised | Result and evidence |
|---|---|---|
| Exact set membership (not sample counts) | Manifest rows vs full tracked set | `extra=[]`; 182 candidates and 15 future-work files fully accounted; 4 new staged task artifacts are outside the manifest's 517-row set (F-02/F-04) |
| Index/worktree divergence | HEAD vs index vs worktree for every tracked path | Worktree == index for all seven staged paths; index differs from HEAD for the three modified preparation files and holds four additions absent at HEAD (F-02/F-04) |
| Type / mode / external boundary | Regular vs symlink/gitlink/LFS/submodule | All entries regular stage-0 `100644`; no `.gitmodules`/`.gitattributes`; no candidate LFS pointer (DISC-01/DISC-02) |
| Completion vs unfinished (terminal coherence) | Candidate family verdicts and retained families | `INCONCLUSIVE`/partial/documentary-`ACCEPT` and the parent waiver preserved; unknowns not upgraded; retained `future-work` stays outside deletion (V-02) |
| Selected vs non-selected coherence | 182 candidates vs 15 retained future-work + old plan review | Retained families are not in the candidate boundary; no candidate leaks into retained scope (V-02) |
| Persisted type strictness | N/A — evidence-only audit, no persisted typed boundary | Not applicable; no schema boundary is claimed by this task |
| Coherent tampering | N/A — no tamper claim; state is Git-verifiable | Not applicable; current facts are read directly from Git/filesystem |

## 5. Independent probes and command results

All probes ran offline from the repository root without escalation; Python used
`PYTHONDONTWRITEBYTECODE=1`; no fixture or long-lived process was launched.

| ID | Exact command / probe | Working directory / environment | Purpose / ACs | Result and observed signal | Side effects / cleanup | Independence / gap |
|---|---|---|---|---|---|---|
| DISC-01 | Extraction-and-run of `discovery-01.md` Appendix A embedded Python (inventory/version/state reconciliation) | repo root; read-only | V-01, V-05, V-06 | exit 0; 521 entries/517 rows, `extra=[]`; 182 candidates; 15 future files; problems = 3×identity + 3×versions (`brief.md`,`preflight.md`,`verification.md`); 4 tracked artifacts absent from manifest; normalized index `cf47b13b…`, raw index `22161aeabf…`, HEAD `b65f900e…`, ignored 155 | none | Independent rerun on current bytes; diagnostic exit 0 is not a pass |
| DISC-02 | Extraction-and-run of `discovery-01.md` Appendix B embedded Python (family/embedded-closure/exclusion reconciliation) | repo root; read-only | V-01, V-02, V-03 | exit 0; 32 families none omitted; 47 cases/11 sets/5 handoffs; `embedded-missing-from-manifest=[]`; all five exclusion identities (4 `.DS_Store` + `.handoff`) agree; helper `update-ref` at `.agents/scripts/run_evidence.py:284` | none | Corroborates exclusions and consumer closure on current bytes |
| DISC-03 | `git status --porcelain=v2 -uall`; `git diff --cached --raw`; `git diff --raw`; `git for-each-ref --exclude='refs/personal-skills/run-evidence/**'`; `git ls-files --others --ignored --exclude-standard`; `git check-ignore -v .DS_Store …`; `sha256sum .git/index` | repo root; read-only | V-04, V-05, V-06 | 7 staged T-001 paths only; unstaged diff empty; 40 protected refs vs 92 namespaced; ignored set 155 paths, scoped ignored `[]` (so the four `.DS_Store` are untracked-unignored, `check-ignore` exit 1) | none | Establishes index/ref drift and the `.DS_Store` misclassification |
| DISC-04 | `grep -n` over `tests/test_review_composition.py`, `docs/tasks/T-005.1/setup_consumer.py`, `tests/README.md`; focused source reads | repo root; read-only | V-03 | Composition constants resolve `T-002.4`/`T-003.4` composition, `T-003.4/results.md`, `T-005.1` package; `ROOT = Path(__file__).resolve().parents[3]`; README maps composition ownership and selector | none | Confirms mapped consumer source; searches/source reads alone do not prove runtime behavior |
| DISC-05 | Pre/post identity capture: sha256 of 521 tracked paths + 3 modified prep files + prior reports; raw `.git/index`; normalized index; normalized refs; ignored listing; full status | repo root; read-only | V-05, V-06 and write isolation | Pre-write identity recorded in §7; post-write recheck adds only this report | none | Confirms this discovery changed no reviewed byte |

Required-but-unrun checks: the T-003 consumer suite
`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_review_composition.py`
is selected historical wiring for later migration proof, **not run** here (T-001
does not require it). No schema validator, process-lifecycle probe or live-model
eval belongs to this evidence-only audit.

Reviewer regressions to rerun after any correction: DISC-01/DISC-02 extraction
command (as recorded in `results.md:351–362` and `reviews/discovery-02.md:94–106`),
plus DISC-03's status/index/ref/ignored probes and DISC-04's source reads.

## 6. Aggregate-gate decision

| Field | Value |
|---|---|
| Gate / exact command | Full manifest, obligation and consumer reconciliation required by the brief — manual, no prescribed executable command |
| Status | `not run` |
| Owner and stage | This reviewer; fourth discovery (second under revision 2) |
| Reason | Decisive targeted failures V-01/V-05/V-06 (F-02/F-03/F-04) suppress the aggregate gate; it is not run merely for completeness. There is no corrected submission whose clean targeted evidence could justify it. |
| Current evidence | V-02/V-03/V-04 pass on current candidate/consumer/owner bytes; V-01/V-05/V-06 fail. No prior aggregate label is reused. No gate or command was added. |

## 7. Scope and baseline comparison

| Item | Recorded baseline | Current reviewed state | Classification / evidence |
|---|---|---|---|
| `HEAD` | `b65f900e7515ccfe36335b793b0c058b7b2bfa8c` | `b65f900e7515ccfe36335b793b0c058b7b2bfa8c` | expected — unchanged |
| Exact `git status --short` | discovery-03 pre-write: two ` M` prep + three `??` task artifacts, no staged changes | seven staged T-001 paths (`M brief/preflight/verification`; `A results + 3 reports`) + four `?? .DS_Store` | task/preparation/packet staging + untracked user metadata — staging is out of scope (F-04); not absorbed |
| Raw index hash | `7a225e39…` | `22161aeabf…` | unexplained drift — F-04 |
| Normalized index hash | `71e86e4b…` | `cf47b13b…` | unexplained drift — F-04 |
| Normalized refs hash | `9ae5a239…` (discovery-02) | `bab2e328…`; protected refs outside namespace = 40 (`c751e4ed…`), namespaced = 92 | namespaced instrumentation is authorized; no protected-only baseline was recorded, so protected-ref invariance across the occurrence cannot be independently confirmed (residual limitation) |
| Dirty path index/worktree identities | manifest rows `5f417e6d…`/`bbeafc7a…`/`9d79cb44…` | worktree `94cc2e18…`/`962a9b13…`/`e30752d7…`; index blobs `62e32efa…`/`46664958…`/`3d4c3ee7…` | mismatch — all three are separable preparation/user revisions (F-02) |
| Task-owned paths | `results.md` (plus later review artifacts) | `results.md` present and staged; three prior review reports staged | in scope as task artifacts, but now index entries outside the manifest (F-04) |
| Durable package artifacts | brief `94cc2e18…`, verification rev 2 `962a9b13…`, preflight bound rev 1 `9d79cb44…` | brief `94cc2e18…`, verification rev 2 `962a9b13…`, preflight `e30752d7…` (revision-2 refresh, `Status: ready`) | brief/verification current; preflight refreshed and current; no new brief revision |
| Authority / policy / dependencies | cleanup-v1 plan/task-map, owner direction | unchanged; no `docs/contracts/` registry | unchanged |

Pre-report status (exact, before this report):

```text
M  ideas/documentation-consolidation/tasks/T-001/brief.md
M  ideas/documentation-consolidation/tasks/T-001/preflight.md
A  ideas/documentation-consolidation/tasks/T-001/results.md
A  ideas/documentation-consolidation/tasks/T-001/reviews/discovery-01.md
A  ideas/documentation-consolidation/tasks/T-001/reviews/discovery-02.md
A  ideas/documentation-consolidation/tasks/T-001/reviews/discovery-03.md
M  ideas/documentation-consolidation/tasks/T-001/verification.md
?? .DS_Store
?? docs/.DS_Store
?? docs/tasks/T-005.3/.DS_Store
?? skills/.DS_Store
```

Post-report status must add only `?? ideas/documentation-consolidation/tasks/T-001/reviews/discovery-04.md`; all other entries and all recorded identities must be unchanged.

## 8. Questions, unchecked work, and residual risks

| Type / row ID | Evidence or reason unverified | Blocking? | Owner / follow-up |
|---|---|---|---|
| `question` — Q-002 | Tag/destination/publication/navigation authorization has only a recommendation; `origin` exists, proposed tag absent | no (downstream gate) | Owner; T-002 — record a sourced decision or keep the explicit gate |
| `blocked` — F-02/F-03/F-04 disposition | Correction under verification revision 2 has not been applied; `results.md` remains revision-1-authored | yes (for T-001 advancement) | T-001 implementer for the preflight-authorized correction; fresh discovery after corrected bytes |
| `residual risk` — protected-ref baseline | No protected-refs-only baseline was recorded by the producer, so invariance of the 40 protected refs across the occurrence cannot be independently proven | no | Fresh discovery after correction; record a protected-only baseline then |
| `residual risk` — index staging attribution | The staging of the seven T-001 paths is not authored by the reviewed `results.md`; its owner/session is unknown | no (but invalidates current-bytes AC-05) | Repository owner / task workflow; do not reset or restage |
| `unchecked` — consumer runtime behavior | No consumer suite ran; migration equivalence is not claimed by T-001 | no | T-003 with the recorded selector |
| `residual risk` — historical records | Missing raw transcripts, unrun role qualification, archive recovery and migration equivalence remain unproved | no | Out of T-001 scope; preserved historical limits |

A failed required behavior (AC-01/AC-05 rows) is a finding, not residual risk.
No required row is silently omitted.

## 9. Coverage completeness and next route

| Field | Value |
|---|---|
| Coverage completeness | `partial — the reviewed submission is unchanged since discovery-03 and still applies revision-1 authority; a revision-2-authorized correction has not been applied. All six required rows have current dispositions (V-02/V-03/V-04 pass; V-01/V-05/V-06 fail).` |
| Basis | Rows V-01–V-06; findings F-01 (historical) and F-02/F-03/F-04/F-05; probes DISC-01–DISC-05; §7 scope comparison; §8 questions |
| Next owner | Separate `task-acceptance-review` decision call consumes this report; the concrete blocker owner is the T-001 implementer for the preflight-authorized correction, then fresh independent discovery |
| Exact next action | Apply the bounded correction already authorized by `preflight.md` (`e30752d7…`) to `ideas/documentation-consolidation/tasks/T-001/results.md` — refresh the current Git/index/worktree inventory and ignored/untracked classification (F-02/F-05), restate AC-05/overall under revision 2 with namespaced instrumentation attributed separately (F-03), and record the index/ref drift without resetting or restaging anything (F-04) — then take the corrected bytes through a fresh independent discovery and a separate acceptance decision. |

## 10. Discovery continuation

```markdown
Discovery continuation:
- Iteration / current byte identity: fourth independent discovery, second under verification revision 2; HEAD b65f900e7515ccfe36335b793b0c058b7b2bfa8c; results.md SHA-256 798906e82414c4c25f16e994a508e63e4eef2806c067ea6953b02347b23407ee (worktree = index blob 8ee24f00…), unchanged since discovery-03; brief 94cc2e18…; verification 962a9b13…; refreshed preflight e30752d7…; raw index 22161aeabf…; normalized index cf47b13b…; normalized refs bab2e328… (40 protected / 92 namespaced).
- Coverage rows: V-01 fail (F-02: three stale included prep identities + stale index/ignored baselines); V-02 pass (candidate evidence); V-03 pass (consumer source closure); V-04 pass (owner gates; Q-002 downstream); V-05 fail (F-03 superseded ref-rule assessment; F-04 index drift); V-06 fail (F-02 and F-04, changed inputs not reinspected). No row omitted.
- Finding IDs: F-01 historical/revision-1 (applicability superseded by revision 2, disposition with acceptance/owner); F-02 suggested P1; F-03 suggested P2; F-04 suggested P2; F-05 suggested P3.
- Finding/scenario continuity: discovery-03 F-02/F-03 re-corroborated on identical submission bytes; sibling surface of F-02 realized by the refreshed preflight as a third stale row. F-04 additionally records post-authorship index/ref drift and out-of-scope staging (attribution unknown; not authored by results.md). Correction owner: T-001 implementer (preflight e30752d7… authorizes it). Readiness owner: focused preflight — already ready. Evidence owner: fresh discovery after corrected bytes. Authority/disposition owners: separate acceptance and repository owner. Do not reset/restage.
- Preparation/context: T-001 brief.md 94cc2e18…; verification.md revision 2 962a9b13…; preflight.md e30752d7… (revision-2 refresh, Status: ready); cleanup-v1 project-plan.md/task-map.json; prior discovery-01/02/03.
- Reviewer regressions: discovery-01.md Appendix A/B extraction command (as in results.md:351–362); DISC-03 status/index/ref/ignored probes; DISC-04 source reads. No new test files.
- Aggregate gate: not run; owner this discovery; manual full reconciliation has no prescribed executable command; decisive V-01/V-05/V-06 failures suppress it. No gate or command added.
- Next: separate acceptance decision call consumes this report; the T-001 implementer applies the preflight-authorized revision-2 correction, then a fresh independent discovery reviews the corrected bytes before the next acceptance decision.
```
