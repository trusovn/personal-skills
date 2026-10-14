# T-001 audit — preservation and retirement eligibility

Submission: **READY_FOR_REVIEW — revision-2 correction**. Retirement advancement: **BLOCKED pending owner snapshot commit and archive/dependency gates**. Independent review owns current row status.
The owner approved preservation membership and retirement disposition. Archive
publication/recovery, input migration and reference repair remain unproved.
No archive, publication or retirement was performed.

## Current correction — revision 2, 2026-10-14

This section and the refreshed inventory supersede the original occurrence's
current-state, AC-05 and continuation claims below. Those older observations
remain historical evidence, including the revision-1 instrumentation finding.

Authority: current brief, verification revision 2, and preflight's Current
correction readiness. All V-01–V-06 remain in scope. User replies in discovery-01
§3 remain Q-001/Q-003 authority. In this session the owner chose:
“Use that tag, origin, and README; I will commit the snapshot.” Q-002 settings:
`archive/documentation-pre-cleanup-2026-10-14`, `origin`, root `README.md`.
The owner commit and actual publication/recovery are still pending. Every
candidate remains BLOCKED for retirement until T-002–T-004 gates pass.

### Complete correction ledger

| Row | Prior discovery-04 status | Current implementation evidence / next owner |
|---|---|---|
| V-01 | fail (F-02/F-05) | Rechecked current effective global ignore rules; regenerated all stable tracked rows from current Git/filesystem state; preparation and added review versions below; output freeze deferred explicitly. Fresh discovery owns corroboration. |
| V-02 | pass | All 182 candidate identities unchanged; original family evidence/dispositions below retained as navigation. Fresh discovery rechecks source verdicts and owner disposition. |
| V-03 | pass | Consumer code and all 13 mapped inputs unchanged; closure/scenario map below retained as navigation. Fresh discovery rechecks actual readers and embedded input closure. |
| V-04 | pass | Q-001/Q-003 sourced from discovery-01 §3; Q-002 actual owner reply recorded above. Archive/dependency gates remain explicit. Fresh discovery reconciles. |
| V-05 | fail (F-03/F-04) | Current index and protected refs preserved against correction baseline. Prior namespaced writes are authorized under revision 2; no retroactive rev1 pass. Existing staging predates this correction, actor unknown. Fresh discovery owns status. |
| V-06 | fail (F-02/F-04) | All changed preparation and added report bytes reinspected; distinct HEAD/index/worktree versions below. No reset, staging or restoration. Fresh discovery owns status. |

F-01 is historical under revision 1; revision 2 permits its namespace. F-02
affects the entire changed inclusion set, not just two files. F-03 applies the
current namespace rule to all begin/recovery/finish refs. F-04 records staging
and ref drift as pre-existing facts without attributing them to this correction
or claiming the old index baseline still holds. F-05 rechecks the effective ignore rules rather than copying a prior label.
Discovery-04 observed untracked-not-ignored Finder metadata; current
`git check-ignore -v` identifies `/Users/mtrusov/.gitignore_global:2:.DS_Store`
for all four files. Their current state is ignored and EXCLUDE. This external
configuration change is not attributed to the correction and does not change
preservation membership. No global configuration is modified. No original verdict is rewritten.

### Current Git state and preservation versions

HEAD: `b65f900e7515ccfe36335b793b0c058b7b2bfa8c`. Raw index SHA-256:
`fe4a868731cf3517853416b51d84ccf7c64eea4e2944313e6e3499af8ff7e190`. Normalized index SHA-256:
`ae8fa311ae523af35146e70b3f63f64f0de9bc8833e6abf27b9b7a06d66428cc`. Protected-ref SHA-256 (strip final newline):
`6b481fa4751bcad78aa2fd5d556a1941d1e042fefd056d486d9960b64d8896e7`. These are correction-start identities,
not retrospective proof of earlier read-only execution. Current tracked/index
set: 522 paths; 521 stable input rows below plus the mutable
`results.md` output. All entries are regular stage-0 mode 100644.

Pre-existing status (preserved, staging actor unknown):

```text
M  ideas/documentation-consolidation/tasks/T-001/brief.md
M  ideas/documentation-consolidation/tasks/T-001/preflight.md
A  ideas/documentation-consolidation/tasks/T-001/results.md
A  ideas/documentation-consolidation/tasks/T-001/reviews/discovery-01.md
A  ideas/documentation-consolidation/tasks/T-001/reviews/discovery-02.md
A  ideas/documentation-consolidation/tasks/T-001/reviews/discovery-03.md
A  ideas/documentation-consolidation/tasks/T-001/reviews/discovery-04.md
M  ideas/documentation-consolidation/tasks/T-001/verification.md
```

| Exact path | HEAD blob / SHA-256 | Index blob / SHA-256 | Worktree blob / SHA-256 |
|---|---|---|---|
| `ideas/documentation-consolidation/tasks/T-001/brief.md` | `bea1daa966eccbcfba28f346062a8b0dc2226caf` / `5f417e6d157800711d6d763592c4173932118c9dec7c18190dec947ac0404d42` | `62e32efa44c79980c657cdb163f097c5969de2a1` / `94cc2e185f1aef939a17d23db629cfef90bd33d6aca7727ad3de1ddaf65a2ebf` | `62e32efa44c79980c657cdb163f097c5969de2a1` / `94cc2e185f1aef939a17d23db629cfef90bd33d6aca7727ad3de1ddaf65a2ebf` |
| `ideas/documentation-consolidation/tasks/T-001/preflight.md` | `81c33d33f99d2ba1454a8b1ee5d93ebf048a590f` / `9d79cb44aa6d152536563a42928869a781bedd238277cabe48fd09615310612d` | `3d4c3ee7e32f1789d203dc5a5bab71d13033eead` / `e30752d743cca2682d8e05c6ba43400e8f1c1de87b91d1d30db9b01591876fee` | `7a59b0d5ddf1b07fd317c4b75cd198905abbb261` / `f60a74cd02f97ec032fc97a2fede49695729f1d383345ea94dd9ba20dab7ef5e` |
| `ideas/documentation-consolidation/tasks/T-001/reviews/discovery-01.md` | `absent` / `absent` | `27adaefa1091687a7eff58feb4e8848fc5707f0e` / `3d2ca9c430bf71c0dd521d42117a4ebdf54ece6d57c0b28983b5aa45e70d71c8` | `27adaefa1091687a7eff58feb4e8848fc5707f0e` / `3d2ca9c430bf71c0dd521d42117a4ebdf54ece6d57c0b28983b5aa45e70d71c8` |
| `ideas/documentation-consolidation/tasks/T-001/reviews/discovery-02.md` | `absent` / `absent` | `7858a5823f35fbf199f87bf8c4d7a219eb6e014c` / `44375e4e35c126547d37b6050720f8af4574a0d9e30c27983b7eb8a1ba0f7337` | `7858a5823f35fbf199f87bf8c4d7a219eb6e014c` / `44375e4e35c126547d37b6050720f8af4574a0d9e30c27983b7eb8a1ba0f7337` |
| `ideas/documentation-consolidation/tasks/T-001/reviews/discovery-03.md` | `absent` / `absent` | `6b7e1ec5a7d8ad8cd139a03483efcc6e7876723f` / `6485ca875fdf74ed8448cedc51e705b2df22985f10857aad50520a3fbc950aa7` | `6b7e1ec5a7d8ad8cd139a03483efcc6e7876723f` / `6485ca875fdf74ed8448cedc51e705b2df22985f10857aad50520a3fbc950aa7` |
| `ideas/documentation-consolidation/tasks/T-001/reviews/discovery-04.md` | `absent` / `absent` | `aeb5bda4eb433f962e98383ee3fb79454ebdea63` / `3b06c915f18c45fff8972ab4df74024cafca64bd1fba0972271269f5f6917362` | `aeb5bda4eb433f962e98383ee3fb79454ebdea63` / `3b06c915f18c45fff8972ab4df74024cafca64bd1fba0972271269f5f6917362` |
| `ideas/documentation-consolidation/tasks/T-001/verification.md` | `15e7f39148c939a7749de333f484bf232fc9c7b5` / `bbeafc7a85d7ef5f3c3974f5b178a0e2cf35efb9dbfa82d35faa21d3dc17f105` | `466649589415556db695b97200e5761151b91175` / `962a9b138d3491eff9ee4d6a372226af8cdbc9f7062d389308c1d8f699d616b1` | `466649589415556db695b97200e5761151b91175` / `962a9b138d3491eff9ee4d6a372226af8cdbc9f7062d389308c1d8f699d616b1` |

`results.md` itself is INCLUDE, mode 100644, a mutable task output. Its indexed
version is `8ee24f0015c53a4efe17d707a80423345bde62fb` /
`798906e82414c4c25f16e994a508e63e4eef2806c067ea6953b02347b23407ee`; HEAD is absent. Its final
worktree hash/length cannot be embedded in its own bytes. T-002 must freeze and
hash it and every later review/result output against the owner's snapshot commit
before tagging; they are not silently omitted or claimed already archived.
The four existing discovery outputs have stable inventory rows. New discovery
and acceptance files follow the same approved Q-001 task-output inclusion rule.

Current ignored set: 159 paths; all four Finder metadata exclusions are now
ignored by the effective global rule. Scoped ignored membership is exactly
`docs/tasks/T-005.3/.DS_Store`; no untracked-unignored input exists before new
review outputs. No relevant original was discovered
among generated/cache files. No tracked symlink/gitlink, .gitmodules or
.gitattributes exists; no retirement candidate is an LFS pointer.

### Current verification and remaining route

Implementation check: enumerate Git HEAD/index/worktree, rehash each stable
tracked input, compare every protected file with `/tmp/doc-cleanup-baseline.json`
except the two authorized output/preparation edits, compare raw/normalized index
and refs outside `refs/personal-skills/run-evidence/`, inspect exact untracked and
ignored sets. No consumer suite is run or claimed by this evidence-only audit.

Required run-evidence: `.agents/scripts/run_evidence.py`; active correction run
`run-20261014T163433Z-0ab95cffac52`. Its metadata, objects and namespaced refs are
authorized instrumentation, separate from protected state and archive refs.
No index, branch, tag, consumer source, original doc or installation is changed.
The first current verification probe passed stable-row and protected-state
checks, then failed its copied untracked-not-ignored assertion. A focused
`git check-ignore -v` probe identified the effective global rule above; the
classification was corrected without changing files/configuration outside the
audit. The completed initial evidence run remains factual; a second correction
run records this bounded classification repair.
Aggregate manual reconciliation belongs to fresh discovery; implementation does
not issue its verdict. No maintainability/registry stage applies.

Next: fresh independent discovery (all six rows and F-01–F-05) -> separate
acceptance -> prompt owner to commit the ready snapshot -> T-002 unused-tag
publication and fresh recovery -> T-003 migration -> T-004 retirement -> T-005
recovery/local behavioral evidence. No migration/deletion/publication has run.

## Historical occurrence — authority and owner gates

Consumed `ideas/documentation-consolidation/tasks/T-001/brief.md`,
`verification.md` revision 1 and existing ready `preflight.md`. Brief and
verification digests match their readiness bindings. The owner confirmed in
this continuation that these remain current and nothing material changed for
this scope. Record current Git state here; do not rewrite readiness or plans.
No results.md existed from the earlier invocation.

| Gate | Decision / source / next owner |
|---|---|
| Q-001 | Resolved by owner reply in this continuation: “Use that proposed set”. INCLUDE full tracked repository, this audit and later task reports. EXCLUDE generated installations, caches, .DS_Store and unrelated CV handoff. Exact current tracked membership is below. T-002 hashes later outputs before freezing. |
| Q-002 | Owner asked for recommendations. Recommend `archive/pre-documentation-cleanup-2026-10-14`, existing `origin`, and root `README.md`. Local tag lookup returns 1 (absent); remote name/availability unverified. Recommendation is not publication authorization. Owner/T-002 must confirm destination, publication and navigation, then prove exact-SHA retrieval from chosen destination. |
| Q-003 | Resolved by owner reply: “let’s retire everything”, keep a very brief note that something was missed, use new planning/work for future issues. All 182 candidates have owner-approved retirement disposition after preservation and dependency gates. Missing acceptance/qualification is not upgraded to pass; additional historical campaigns are not retirement prerequisites. |
| Terminology | “future-tasks” means existing `docs/future-work/`, as cleanup plan §12 states. All 15 files including stale/ remain active. No contrary scope instruction was found. |

Recommended active note for T-004:
“Completed delivery documents were archived and retired. Some qualification was
incomplete; future issues will use new work.” Add only fixed tag/SHA/recovery
command required by cleanup authority. Detailed historical evidence stays in
archive; do not recreate a verbose backlog of waived qualification work.

## Inventory rules and boundaries

Every tracked row below is INCLUDE under Q-001. C = retirement candidate, P =
cleanup planning/preparation, R = remaining full repository context. P/R are
OUT OF SCOPE for deletion. Every C row is BLOCKED pending archive recovery;
13 consumer inputs also need T-003 migration, and active pointers need T-004
repair. Q-003 resolves completion/disposition unknowns for retirement without
inventing proof. Each C row maps to its family evidence below.

S = tracked, stage 0, HEAD/index/worktree identical, no staged or unstaged delta.
All 517 tracked inputs are regular files. The table lists exact path, Unix/Git
mode, byte length, SHA-256 and index/HEAD blob. Filesystem bytes were checked
against Git blob identities; final comparison checks the recorded input set.
No divergent versions, deletion, symlink or gitlink exists in the tracked set.
No .gitmodules/.gitattributes exists; candidate bytes contain no LFS pointer.
Tar archives and JSON evidence are ordinary blobs, not externally fetched content.

Historical receipts reference disposable workspaces, unavailable raw transcripts,
ignored installations and .git evidence sidecars. Those referenced bytes are
not thereby in a snapshot. Missing raw history remains missing; T-005's waiver
permits personal-use closure without recovering it. Available historical records
are preserved. Snapshot history does not include unrelated reflogs/checkpoints.
Original branch/tag refs are unchanged; a finish-sidecar ref was added as recorded below. Ref identities are not an archive
claim. No inaccessible present tracked asset was found.

Audit-start UTC: `2026-10-14T12:17:59.872757+00:00`. HEAD: `b65f900e7515ccfe36335b793b0c058b7b2bfa8c`.
HEAD tree: `5bd4772805fd7aa5160c1b641bc8417944925017`.
Initial porcelain status: empty. Normalized index SHA-256: `71e86e4b76095c4b0611e08fb017e6d6a9b87c5e6dfee29b305ca4469a51586c`.
Normalized refs SHA-256: `66fb6142c08926570a5839c6a87091bc3f31dfb744deeccb70e4202f207df211`. Normalization strips final newline
from `git ls-files --stage` and `git show-ref` respectively.
Raw index SHA-256 after baseline capture: `7a225e39f132005de82de9c15aba7e0a933c9e665f5ce556339c9cba644da7d0`.

### Nontracked exclusions

Current reinspection: four Finder metadata files are ignored by the effective
global `.DS_Store` rule. Full ignored membership is 159 paths; scoped membership
is `docs/tasks/T-005.3/.DS_Store`. Discovery-04 observed a different effective
configuration and its original classification remains historical.
Q-001 excludes these generated/cache/unrelated inputs. Cache patterns are
__pycache__, *.py[cod] and pytest metadata. Installed .agents files are generated
copies, not original source or preserved qualification. No credentials or unrelated
contents are copied. Empty directories have no Git objects.

| Exact relevant exclusion | Type / Unix mode | Bytes | SHA-256 | State / reason |
|---|---|---:|---|---|
| `.DS_Store` | regular / `0644` | 10244 | `d7fdda803578f7ea8b489dd449da62849316b0634bf1175d283a31e1a3820845` | ignored (global rule); EXCLUDE Finder metadata, Q-001 |
| `docs/.DS_Store` | regular / `0644` | 6148 | `2d4740cf346bb2cfe93c70b6717aed1da0e4a05b42690f3587d7537cb76d8207` | ignored (global rule); EXCLUDE Finder metadata, Q-001 |
| `docs/tasks/T-005.3/.DS_Store` | regular / `0644` | 8196 | `699e5ad536cfb2781e27c4a00e09ce86713822082db5203666f0cfad42b0b627` | ignored (global rule); EXCLUDE Finder metadata, Q-001 |
| `skills/.DS_Store` | regular / `0644` | 6148 | `fce67661710597f67c9b69319a4afa537b05cb4dd1486cf358ae8ee8ce27ff8f` | ignored (global rule); EXCLUDE Finder metadata, Q-001 |
| `.handoff/session-handoff-20260813-1203.md` | regular / `0644` | 7588 | `d69566a2a0d1f0c3da76c4a0c7809df758a93092f0c294803b80a594dc091d0e` | ignored; EXCLUDE unrelated CV handoff, Q-001 |

results.md is this occurrence's new untracked output, distinguished from original
inputs. Its final whole-file digest is delivered separately; a document cannot
contain its own whole-file digest. T-002 hashes it and later review reports.
Preparation artifacts are P inputs, not old qualification outputs.
New optional evidence under .git/personal-skills/run-evidence is instrumentation,
not original archival membership or independent review. Excluded generated trees
need no preservation manifest of individual intended originals.

## Evidence and dispositions for every candidate family

All paths in this table are relative to docs/tasks/<family>/ unless stated.
Every exact candidate path below maps to this table. Completion remains unknown
where an original final verdict is unavailable; commit labels, task-index entries
and brief status do not establish completion. Owner Q-003 permits retirement
without manufacturing that evidence. Detailed original rows/findings stay in
archive; active context is the short owner-requested note, with pinned recovery.
Coordinator owns disposition, T-004 owns retirement after prior gates.

| Family | Original evidence / qualification limits | Pending obligation and disposition |
|---|---|---|
| `BRIEF-P0` | Brief/preparation only; no local result/final acceptance. Completion unknown. | Stated next-review/qualification obligations remain historical and unproved. Owner Q-003 permits retirement without new campaign/verdict. |
| `INT-FLOW-001` | results.md READY_FOR_REVIEW; discovery-01 no findings. | Discovery retains owed maintainability evidence/separate acceptance; no acceptance file. Results are live provenance input; T-003 retains it. |
| `Q-01` | reviews/acceptance-01.md:7,41 ACCEPT under amended source/fixture contract; qualification-handoff.md V-02-role–V-08-role unrun. Acceptance §8 consumes explicit repository-install override (“I’ll install the skills separately”), not an observed projection. | Q-01-QUALIFICATION seven trials are unrun, no ready executable package. Q-003 permits retirement; future work needs new authority. Nonblocking maintainability observations remain observations. |
| `T-001` | Decomposed parent brief; no parent completion/acceptance evidence. Completion unknown. | Stated next-review/qualification obligations remain historical and unproved. Owner Q-003 permits retirement without new campaign/verdict. |
| `T-001.1` | Brief/preparation only; no local result/final acceptance. Completion unknown. | Stated next-review/qualification obligations remain historical and unproved. Owner Q-003 permits retirement without new campaign/verdict. |
| `T-001.2` | Submission/correction records: result.md, correction-F-01.md. No durable final acceptance; completion unknown. | Stated next-review/qualification obligations remain historical and unproved. Owner Q-003 permits retirement without new campaign/verdict. |
| `T-001.3` | Submission/correction records: correction-results.md. No durable final acceptance; completion unknown. | Stated next-review/qualification obligations remain historical and unproved. Owner Q-003 permits retirement without new campaign/verdict. |
| `T-001.4` | Brief declares accepted, records projection/review context; no local result/review file. | Declared status alone is not original acceptance evidence; completion unknown. Q-003 permits retirement. |
| `T-002` | Decomposed parent brief; no parent completion/acceptance evidence. Completion unknown. | Stated next-review/qualification obligations remain historical and unproved. Owner Q-003 permits retirement without new campaign/verdict. |
| `T-002.1` | Brief/preparation only; no local result/final acceptance. Completion unknown. | Stated next-review/qualification obligations remain historical and unproved. Owner Q-003 permits retirement without new campaign/verdict. |
| `T-002.2` | Brief/preparation only; no local result/final acceptance. Completion unknown. | Stated next-review/qualification obligations remain historical and unproved. Owner Q-003 permits retirement without new campaign/verdict. |
| `T-002.3` | Submission/correction records: correction-result.md, correction-result-02.md. No durable final acceptance; completion unknown. | Stated next-review/qualification obligations remain historical and unproved. Owner Q-003 permits retirement without new campaign/verdict. |
| `T-002.4` | Submission/correction records: results.md. No durable final acceptance; completion unknown. | Stated next-review/qualification obligations remain historical and unproved. Owner Q-003 permits retirement without new campaign/verdict. |
| `T-003` | Decomposed parent brief; no parent completion/acceptance evidence. Completion unknown. | Stated next-review/qualification obligations remain historical and unproved. Owner Q-003 permits retirement without new campaign/verdict. |
| `T-003.1` | Brief/preparation only; no local result/final acceptance. Completion unknown. | Stated next-review/qualification obligations remain historical and unproved. Owner Q-003 permits retirement without new campaign/verdict. |
| `T-003.2` | Brief/preparation only; no local result/final acceptance. Completion unknown. | Stated next-review/qualification obligations remain historical and unproved. Owner Q-003 permits retirement without new campaign/verdict. |
| `T-003.3` | Submission/correction records: implementation.md, correction-implementation.md. No durable final acceptance; completion unknown. | Stated next-review/qualification obligations remain historical and unproved. Owner Q-003 permits retirement without new campaign/verdict. |
| `T-003.4` | Submission/correction records: results.md. No durable final acceptance; completion unknown. | Stated next-review/qualification obligations remain historical and unproved. Owner Q-003 permits retirement without new campaign/verdict. |
| `T-004` | Decomposed parent brief; no parent completion/acceptance evidence. Completion unknown. | Stated next-review/qualification obligations remain historical and unproved. Owner Q-003 permits retirement without new campaign/verdict. |
| `T-004.1` | implementation.md corrected READY_FOR_REVIEW; discovery-02 no findings; no acceptance file. | Historical unborn-install/local evidence only; final acceptance unknown. Q-003 permits retirement. |
| `T-004.2` | results.md corrected READY_FOR_REVIEW; discovery-01–04 with final no findings; no acceptance file. | F-01–F-03 historically corrected/probed; final acceptance unknown, installed role behavior unproved. Q-003 permits retirement. |
| `T-004.3` | results.md, correction-02.md and discovery-01–03; final discovery records 72 tests/no findings; no acceptance file. | Historical unmanaged-byte/projection repairs proved locally; final acceptance unknown. Q-003 permits retirement. |
| `T-005` | reassessment.md:9–65 ends campaign under accepted personal-use risk; .6 documentary ACCEPT satisfies revised report deliverable. | Coordinator may close personal-use scope, full qualification incomplete. No fresh parent-status acceptance inferred; Q-003 permits retirement. |
| `T-005.1` | reviews/acceptance-01.md ACCEPT for setup; discovery-03 corroborates projection and evaluator isolation, receipts preserve historical setup. | Point-in-time setup, not current installed-role qualification. 47-ID inventory/11 staged sets remain live inputs; T-003 migrates closure. |
| `T-005.2` | reviews/acceptance-01.md:6 INCONCLUSIVE; discovery-02 corroborates corrected F-01 claim and local evidence, historical 35 structural tests. | V-01–V-07 and V-07-Q decisive role/raw-history rows blocked. Parent reassessment waives further role proof and historical recovery; do not relabel ACCEPT. |
| `T-005.3` | results.md and reviews/discovery-01.md: partial independent coverage, 24 snapshots and historical 53 owner tests; no acceptance file. | Composed roles/runtime matrix remain unrun. evidence/deferral-gap.md has no actual approved deferral. Parent reassessment stops campaign/waives new proof. |
| `T-005.4` | Brief only; no result/review. | Known-issue consumption unrun and waived by parent reassessment; supplied KI-001 fixture history is not approved deferral. |
| `T-005.5` | Brief only; no result/review. | Correction/conditional/gate qualification unrun and waived by parent reassessment. |
| `T-005.6` | reviews/acceptance-01.md:3 ACCEPT for revised documentation only. results.md and retained ART-012 preserve incomplete behavioral qualification. | No full qualification; historical checker cannot pass at new HEAD/status. Keep administrative evidence historical; owner accepts personal-use risk. |
| `TEST-STAB-001` | Decomposed parent brief; no parent completion/acceptance evidence. Completion unknown. | Stated next-review/qualification obligations remain historical and unproved. Owner Q-003 permits retirement without new campaign/verdict. |
| `TEST-STAB-001.1` | results.md test-owner relocation proof; discovery-01 no findings; no acceptance file. | Final acceptance unknown; tests/README retains ownership-history pointer needing T-004 repair. |
| `TEST-STAB-001.2` | results.md implemented submission/unchanged test counts; no independent review file. | Final review/acceptance unknown. Active test/helper implementations stay active. |
| docs/tasks/index.json | Structural registrations/dependencies, not completion evidence. | Active manifest audit reads registered IDs; T-003 retains needed data. |
| docs/project-plan.md | Old planning authority; docs/project-plan-review.md:3–12 ACCEPT for identified planning bytes, not delivery acceptance. | Overall completed implementation unproved. Owner Q-003 permits retirement with reduced assurance preserved. |
| docs/task-map.json | Old FLOW/ART/task ownership, not status tracker. | Composition test requires T-005/ART-012 ownership; T-003 retains needed declaration before retirement. |

T-005 exporter-resume, ledger-cardinality/order/type, tamper/replay,
PROC-RESIST/PIPE/RACE cleanup, actual context/routes/correction/deferral and
provenance gaps preserve their IDs/statuses in original .2/.3 ledgers. Missing
raw records stay missing. Parent waiver is a disposition, never a pass.
No actual approved deferral is inferred; no synthetic known issue is created.
Future-work's remaining-T-003/T-004/T-005 selection lane and Q-01 candidate
wording are stale cautions, not completion evidence or new work authority.
T-004 keeps future-work and old plan review active; repairs only necessary
references and the owner's brief disposition note.

## Consumer closure and existing verification owners

Search roots: tracked tests/, scripts/, skills/, root README, docs/ and cleanup
planning. Patterns: docs/tasks, docs/project-plan, docs/task-map, composition.json,
T-005.1, T-005.3, consumer-inputs.json; split literals docs/tasks/task-map and
T0051/T0034 constants; normalized relative Markdown links. Initial rg also
named absent docs/README.md (error); rerun used existing roots. JSONL/raw transcript
matches are historical recordings. Searches were followed by actual reader,
fixture, input and existing-test inspection; searches alone do not prove closure.

| Reader / locations | Complete needed inputs / owner | Existing scenarios, oracle and selector |
|---|---|---|
| tests/test_review_composition.py:33–67,84–235,291–419 | Exact 13 candidate inputs below; data-driven current_evidence, owner_test, fixture/scenario, registered owner and handoff/preparation pointers are inputs too. Owner: composition module. | Inventory rejects missing CCR-04, stale INV-CASE-09 scenario and unresolved evidence. Good/wrong controls share oracle; all inherited IDs and registered owners retained. Baseline/post selector: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_review_composition.py`. Selected, not run. |
| Composition classes :424–842 / :843–1208 | T-002.4 composition + old task map; T-003.4 composition + results; eval catalogs/setup, public skills/guides and declared child-owner tests. | COMP-01–05, INV-CASE-01–24; CCR-01–08, ROUTE/FIND/ROWS/REV/EFF/GATE/DISP: mixed rows, conditional routes, stops, aggregate ownership and truthful unrun/installation claims. Same module selector. |
| T0051 class :1210–1380; fixtures.md embedded JSON | 47 IDs; 11 input sets; 5 owning-leaf handoffs. Staged sets use six active setup owners. Local t0051-package set resolves ROOT fixtures/results/three receipts and .6 brief; not found by constants alone. | Real disposable staging resolves every consumer/held-back input, proves unstaged producer slots absent, checks answer-byte exclusion from worktree/Git objects, rejects degraded handoff manifests. Same selector; retain assertions and input meaning, not only schema. |
| docs/tasks/T-005.1/setup_consumer.py:10–35 via embedded fixture pointer | parents[3] currently computes repository ROOT; invokes active implementer route-cases, copies worktree excluding .git, removes change-effects/cases.json, creates separate clean consumer Git baseline. | Rebind embedded path and recalculate root after placement change. Existing test_handoff_manifests_resolve_exact_consumer_visible_inputs and test_route_consumer_excludes_answers_and_preserves_review_context prove isolation. Same selector. |
| tests/review_fixture_support.py:11–29; tests/staging_fixture_support.py:30–53 | ROOT/source package paths, skills/eval catalogs/setups; disposable EVAL_WORK_ROOT; staging failure raises diagnostics, never pass. No retired file read directly. | Keep shared helpers/cleanup; use owning-module selectors, not duplicate infrastructure. |
| docs/tasks/T-005.6/evidence/check_report.py:9–34 | Historical protected-before.json (591 old hashes), HEAD/status precondition, .6 docs and retained ART-012 report. | Historical administrative oracle cannot pass at new HEAD/committed status; discovery DISC-06/acceptance preserves that limit. Archive as history; do not resurrect as live release gate or rewrite baseline. |
| scripts/install_development_skills.py:25–62,197–215 | Managed source packages, profile guide, six shared scripts; no current candidate is directly installed. Tests-owned placement avoids added installed input coupling. | If T-003 uses a managed skill-owned location, update relevant installer declarations/guide/docs/tests together. Conditional existing selector: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py`. Not run here. |

Exact live composition candidate-input closure:

- `docs/task-map.json`
- `docs/tasks/INT-FLOW-001/results.md`
- `docs/tasks/T-002.4/composition.json`
- `docs/tasks/T-003.4/composition.json`
- `docs/tasks/T-003.4/results.md`
- `docs/tasks/T-005.1/evidence/V-02-setup-reconstruction.md`
- `docs/tasks/T-005.1/evidence/V-03-install-projection.md`
- `docs/tasks/T-005.1/evidence/V-04-drift-contrast.md`
- `docs/tasks/T-005.1/fixtures.md`
- `docs/tasks/T-005.1/results.md`
- `docs/tasks/T-005.1/setup_consumer.py`
- `docs/tasks/T-005.6/brief.md`
- `docs/tasks/index.json`

Remaining source closure stays active: six flow setup_fixture.py files for
acceptance/discovery/maintainability/implementer/preflight/verification-designer;
acceptance/discovery/preflight eval catalogs; referenced source skills/templates;
child owner tests in inventory: bounded_task_implementer, task_maintainability_review,
task_review_discovery, task_acceptance_review, task_preflight,
task_preparation_contracts, contextual_export_risks, contextual_uncertainty_inputs,
review_composition (all tests/test_<name>.py). Their exact paths/hashes are R rows.
These fixtures generate synthetic disposable docs/tasks inputs, not copies of
current candidate packages. Preserve held-back keys and unstaged positions.
T-003 runs narrow composition baseline first, then affected owner modules using
existing tests/README selectors; installer suite only when managed closure changes.
No suite/staging run, migration equivalence or installed-role qualification is
claimed by this read-only audit.

### Reference carriers

Active tests/README.md:24,66 maps composition ownership and links historical
TEST-STAB-001.1 results; T-003/T-004 repair it. The retained ART-012 closure report
has 31 actual local candidate links; T-004 pins them to archive SHA, preserving
its historical wording/limits. Exact carriers:

- `skills/task-implementation-flow/docs/standalone-policy-qualification-results-T-005.md:7` → `docs/tasks/T-005/reassessment.md` (historical evidence pointer).
- `skills/task-implementation-flow/docs/standalone-policy-qualification-results-T-005.md:8` → `docs/tasks/T-005.6/brief.md` (historical evidence pointer).
- `skills/task-implementation-flow/docs/standalone-policy-qualification-results-T-005.md:19` → `docs/project-plan.md` (historical evidence pointer).
- `skills/task-implementation-flow/docs/standalone-policy-qualification-results-T-005.md:27` → `docs/tasks/T-005.1/reviews/acceptance-01.md` (historical evidence pointer).
- `skills/task-implementation-flow/docs/standalone-policy-qualification-results-T-005.md:27` → `docs/tasks/T-005.1/reviews/discovery-03.md` (historical evidence pointer).
- `skills/task-implementation-flow/docs/standalone-policy-qualification-results-T-005.md:28` → `docs/tasks/T-005.2/results.md` (historical evidence pointer).
- `skills/task-implementation-flow/docs/standalone-policy-qualification-results-T-005.md:28` → `docs/tasks/T-005.2/reviews/acceptance-01.md` (historical evidence pointer).
- `skills/task-implementation-flow/docs/standalone-policy-qualification-results-T-005.md:29` → `docs/tasks/T-005.3/results.md` (historical evidence pointer).
- `skills/task-implementation-flow/docs/standalone-policy-qualification-results-T-005.md:29` → `docs/tasks/T-005.3/reviews/discovery-01.md` (historical evidence pointer).
- `skills/task-implementation-flow/docs/standalone-policy-qualification-results-T-005.md:30` → `docs/tasks/T-005.4/brief.md` (historical evidence pointer).
- `skills/task-implementation-flow/docs/standalone-policy-qualification-results-T-005.md:30` → `docs/tasks/T-005.3/evidence/deferral-gap.md` (historical evidence pointer).
- `skills/task-implementation-flow/docs/standalone-policy-qualification-results-T-005.md:31` → `docs/tasks/T-005.5/brief.md` (historical evidence pointer).
- `skills/task-implementation-flow/docs/standalone-policy-qualification-results-T-005.md:32` → `docs/tasks/T-005.6/results.md` (historical evidence pointer).
- `skills/task-implementation-flow/docs/standalone-policy-qualification-results-T-005.md:32` → `docs/tasks/T-005.6/verification.md` (historical evidence pointer).
- `skills/task-implementation-flow/docs/standalone-policy-qualification-results-T-005.md:32` → `docs/tasks/T-005.6/preflight.md` (historical evidence pointer).
- `skills/task-implementation-flow/docs/standalone-policy-qualification-results-T-005.md:44` → `docs/tasks/T-005.1/fixtures.md` (historical evidence pointer).
- `skills/task-implementation-flow/docs/standalone-policy-qualification-results-T-005.md:53` → `docs/tasks/T-005.1/fixtures.md` (historical evidence pointer).
- `skills/task-implementation-flow/docs/standalone-policy-qualification-results-T-005.md:54` → `docs/tasks/T-005.2/evidence/preparation-and-recovery-observations.md` (historical evidence pointer).
- `skills/task-implementation-flow/docs/standalone-policy-qualification-results-T-005.md:55` → `docs/tasks/T-005.2/evidence/unrun-role-boundaries.md` (historical evidence pointer).
- `skills/task-implementation-flow/docs/standalone-policy-qualification-results-T-005.md:56` → `docs/tasks/T-005.3/evidence/coverage-ledger.json` (historical evidence pointer).
- `skills/task-implementation-flow/docs/standalone-policy-qualification-results-T-005.md:57` → `docs/tasks/T-005.3/reviews/discovery-01.md` (historical evidence pointer).
- `skills/task-implementation-flow/docs/standalone-policy-qualification-results-T-005.md:75` → `docs/tasks/T-005.1/evidence/V-03-install-projection.md` (historical evidence pointer).
- `skills/task-implementation-flow/docs/standalone-policy-qualification-results-T-005.md:76` → `docs/tasks/T-005.1/evidence/V-06-consumer-git-exclusion.md` (historical evidence pointer).
- `skills/task-implementation-flow/docs/standalone-policy-qualification-results-T-005.md:86` → `docs/tasks/T-005.3/results.md` (historical evidence pointer).
- `skills/task-implementation-flow/docs/standalone-policy-qualification-results-T-005.md:92` → `docs/tasks/T-005.2/evidence/run-log.md` (historical evidence pointer).
- `skills/task-implementation-flow/docs/standalone-policy-qualification-results-T-005.md:93` → `docs/tasks/T-005.2/evidence/correction-discovery-01.md` (historical evidence pointer).
- `skills/task-implementation-flow/docs/standalone-policy-qualification-results-T-005.md:94` → `docs/tasks/T-005.3/evidence/capture-command.md` (historical evidence pointer).
- `skills/task-implementation-flow/docs/standalone-policy-qualification-results-T-005.md:95` → `docs/tasks/T-005.3/evidence/staging.json` (historical evidence pointer).
- `skills/task-implementation-flow/docs/standalone-policy-qualification-results-T-005.md:96` → `docs/tasks/T-005.3/evidence/public-probes.json` (historical evidence pointer).
- `skills/task-implementation-flow/docs/standalone-policy-qualification-results-T-005.md:97` → `docs/tasks/T-005.3/evidence/owner-checks.json` (historical evidence pointer).
- `skills/task-implementation-flow/docs/standalone-policy-qualification-results-T-005.md:107` → `docs/tasks/T-005.6/evidence/protected-before.json` (historical evidence pointer).

Old plan review and future-work/stale carry historical plan/task mentions;
preserve verdicts/notes, repair essential pointers only. FEATURE-MAP/concepts
have stale current-work cautions: retain families and the brief owner disposition.
Cleanup ideas planning names originals and remains P context for later tasks.
Source contracts/templates/validator usage and synthetic eval prompts that use
generic docs/tasks or project-plan/task-map filenames describe target-repository
conventions, not reads of these originals; do not migrate those conventions.
Disposable test paths API-07/QR-12/MNT-42/ORD-04/CURRENT are fixture-local inputs.
Older orchestrator integration-spike script, fixture docs, JSONL/TXT and ledger
record SYN-01 historical experiments, not active readers of candidate originals.
No actual root README Markdown link to originals was found.

## Verification and limits

| Scenario / risk | Current implementation evidence | Next owner |
|---|---|---|
| V-01 / R-01 | Git/index/filesystem enumeration and byte/mode reconciliation; all current tracked paths recorded; nontracked/ignored boundaries explicit. Q-001 resolved. | Fresh discovery independently rebuilds inventory. |
| V-02 / R-02 | Original result/review/qualification evidence mapped for every candidate family; unknowns explicit; .2 INCONCLUSIVE/.3 partial/waivers retained; preserved future-work and old review outside deletion. | Fresh discovery challenges claims; T-004 carries brief disposition. |
| V-03 / R-03 | Source reader/setup/test inspection and embedded data reconciliation: 13 actual candidate inputs, setup-root/isolation and active source closure; existing wrong controls/selectors recorded. | Fresh discovery corroborates; T-003 proves migration. |
| V-04 / R-02 | Actual owner Q-001/Q-003 replies; recommended Q-002 still needs publication decision. All candidates archive/dependency gated; overall BLOCKED. | Owner/T-002 archive; T-003 consumers; T-004 retirement. |
| V-05 / R-04 | Before/after tracked contents/modes, scoped status and index agree; refs do not: sidecar added a namespaced finish ref. AC-05 strict ref-preservation condition is not satisfied. New audit attributed separately. | Fresh discovery checks submitted bytes/scope. |
| V-06 / R-04 | Preflight-to-occurrence planning commit revalidated at current HEAD; old audited docs unchanged and owner confirms applicability. In-occurrence additive sidecar ref drift found/reinspected below; no inputs restored/overwritten. | Next task reinspects affected facts on future drift. |

Actual read-only commands (cwd repository root): git rev-parse HEAD;
git rev-parse HEAD^{tree}; git status --porcelain=v1 --untracked-files=all;
git ls-files -z; git ls-files --stage; git show-ref;
git ls-files --others --exclude-standard;
git ls-files --others --ignored --exclude-standard (full and scoped);
git diff 32edda26bf82b0a494993afc17e564722e51808d HEAD -- docs/tasks
docs/project-plan.md docs/task-map.json docs/project-plan-review.md docs/future-work;
git remote; git show-ref --verify --quiet recommended-tag ref;
focused rg searches, source/report reads and Python standard-library
lstat/SHA-256/Git-blob/embedded-JSON/relative-link reconciliation.
Scratch captures use /tmp/, not repository source. One closure extraction failed
on a null fixture field; corrected read resolved 13 inputs. One report-generation
attempt failed at syntax parsing before any write; corrected generation changed
only this output. No failed read/generation changed originals.

No tests/evals/fixtures changed or added. No suite, live model, network,
installation refresh, archive-recovery, staging, branch commit or deletion ran. Optional sidecar did write its namespaced ref, an AC-05 exception.
Independent reviewer owns aggregate reconciliation; no broad gate ran here.
Optional same-installation evidence availability true, no open run;
run-20261014T121744Z-057fb9f63b88 closed completed. It creates optional Git snapshot
objects and a namespaced finish ref without moving branch refs; its final snapshot preceded this result-only
wording clarification. Sidecar is not acceptance.
No architecture, maintainability or registry stage applies to evidence-only output;
no docs/contracts/index.json exists.

Final identity comparison at `2026-10-14T12:34:02.715852+00:00`:
all 517 original tracked file hashes/types/modes unchanged; all 182 candidates
and 15 retained future-work files accounted for; 13 traced candidate inputs
resolve and have identity rows. HEAD, normalized index and raw index equal
the baseline identities above. Refs differ only by the additive sidecar finish ref below. Full ignored membership unchanged. Staged and
unstaged raw diffs empty. Final porcelain adds only
`?? ideas/documentation-consolidation/tasks/T-001/results.md`. V-05 strict all-refs-unchanged oracle fails; V-06 reinspection records the delta below. No fault injection occurred. Preflight-era
tracking change was revalidated at current HEAD, never repaired by overwriting.

Deliverable: ART-002 / IF-001 audit for cleanup-v1. Actual contract impact:
materialized planned audit facts for T-002–05; no reusable software contract change.
Executable contract declarations changed: none.
Next: fresh independent task-review-discovery → separate task-acceptance-review.
No archive recovery, historical qualification or deletion approval is proved here.


### Final ref-drift exception and continuation

After closing optional evidence, `git show-ref` gained exactly:

`6cb6a837746cdbf3e8f6d58e9bdcf529577d1f26 refs/personal-skills/run-evidence/run-20261014T121744Z-057fb9f63b88/finish`

No original ref was removed or changed. Final normalized refs SHA-256:
`9ae5a239c74eeb8fb4ddde47257b1c9000b911822d04dd60a0dcb194b7c3f135`.
The active helper `.agents/scripts/run_evidence.py:24,266–284` explicitly uses
`git update-ref` for snapshot capture. This identifies the source of the additive
ref; the brief's stricter no-ref-write boundary should have excluded that optional
lifecycle. It is an implementation-side instrumentation mistake, not user drift.
The audit-start baseline followed begin, so it already contains the corresponding
begin-sidecar ref; the finish ref is the observed additional delta. These namespaced
sidecar refs are excluded instrumentation, not archive refs or permission to retire.

All 517 protected file bytes remain current; HEAD/index, original branch/tag refs,
182 candidate identities, consumer closure and owner replies were rechecked and
are unaffected. V-06 affected ref facts have been reinspected; V-05/AC-05 remains
unsatisfied under its strict no-ref-write requirement. No ref was deleted to
conceal/undo the exception. This NON-COMPLETE result cannot advance cleanup.
Fresh independent discovery must corroborate this exception; separate acceptance
and the owner decide its disposition before T-001 advancement. Existing planning,
source, verdicts and installations are unchanged. No new qualification campaign
or production correction is proposed.

## F-01 correction — read-only revalidation

Correction baseline: `2026-10-14T15:38:29.979467+00:00`. This correction
changes only this audit output. The earlier NON-COMPLETE submission and ref
exception remain historical facts; this section does not supersede their verdicts.

Broken invariant: optional instrumentation must stay inside the task's write
boundary. The active helper writes snapshot refs at begin, recovery and finish.
The correction excludes **all** evidence lifecycle operations, including active
run takeover/recovery, begin, check and finish. The read-only availability probe
returned `available: true`; availability does not authorize ref writes. No
evidence run was opened or recovered. This task-specific exclusion follows the
brief's stronger read-only boundary, not a change to the installed skill/helper.

Pre-edit coverage map and correction evidence:

| Row | Prior reviewer status | Planned / current implementation evidence | Incomplete reason; next owner |
|---|---|---|---|
| V-01 | pass | Rerun discovery-01.md Appendix A: 517 inventory rows, zero missing/extra/identity/version errors; 182 candidates, 15 future-work files. Appendix B: all five exclusion identities agree. | None in targeted recheck; fresh discovery retains ownership of corrected-row status. |
| V-02 | pass | Prior source dispositions used as navigation only. Appendix B re-enumerates all 32 families with none omitted; protected source bytes remain identical. | Full evidence/disposition reconciliation belongs to fresh discovery. |
| V-03 | pass | Prior reader traces used as navigation only. Appendix B rechecks 47 cases, 11 input sets, five handoffs and zero embedded candidate inputs missing from the manifest; protected reader/setup bytes remain identical. | Full consumer closure corroboration belongs to fresh discovery. |
| V-04 | pass | Q-001/Q-003 now also have durable independent sourcing: discovery-01.md §3 records the owner's “Confirm both decisions” reply and exact question scope. Q-002 remains owner/T-002's downstream gate. | Fresh discovery reconciles corrected output and gates; no archive authorization added. |
| V-05 | fail / F-01 | Appendix A reproduces the historical ref exception. Correction before/after comparison checks all tracked bytes/modes, HEAD, normalized/raw index, refs, ignored membership, status and the untouched discovery report. No lifecycle operation is used. | Historical ref-write failure cannot be undone by this correction; fresh discovery checks current evidence, separate acceptance/owner decides disposition. Prior reviewer status remains fail. |
| V-06 | pass | Appendix A verifies current preparation digests and baseline identities. Preflight-HEAD-to-current diff of original audited roots remains empty. Correction baseline includes disclosed refs and both existing untracked artifacts. | Fresh discovery owns current drift corroboration; no original is restored. |

The map above was declared before editing. Probe results are implementation
evidence, not new independent row dispositions. No prior reviewer pass is
promoted to acceptance for these corrected bytes.

Exact repeatable reviewer probes (cwd repository root):

~~~sh
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
from pathlib import Path
import re, subprocess
report = Path('ideas/documentation-consolidation/tasks/T-001/reviews/discovery-01.md').read_text()
for label in ['A', 'B']:
    section = report.split('## Appendix ' + label + ' —')[1]
    code = re.search(r"python3 - <<'PY'\n(.*?)\nPY", section, re.S).group(1)
    result = subprocess.run(['python3', '-c', code])
    if result.returncode:
        raise SystemExit(result.returncode)
PY
~~~

Both appendix probes returned exit 0. Appendix A's diagnostic oracle still
reports the historical ref delta; process exit 0 does not turn V-05 into a pass.
Correction baseline HEAD, normalized/raw index and refs equal discovery-01.md
§7. Initial status contains only this results.md and discovery-01.md; no tracked
diff exists. Full ignored membership has 159 paths; its newline-preserving
listing SHA-256 is `fba05395bc3f3a6b21871fa8e04b89952aa29f376946092964173996beee4b3b`.
The untouched discovery report SHA-256 is
`3d2ca9c430bf71c0dd521d42117a4ebdf54ece6d57c0b28983b5aa45e70d71c8`.

Post-edit implementation comparison: all 517 protected file bytes/modes, HEAD,
normalized/raw index, refs, ignored listing, status and discovery report match
the correction baseline; zero differences. Appendix A/B reruns returned exit 0
with the same inventory results. `git diff --check` returned 0;
`git diff --no-index --check /dev/null ideas/documentation-consolidation/tasks/T-001/results.md`
returned 1 for the added-file difference with no whitespace diagnostics.
Only this output's bytes changed. The comparison is correction evidence only;
the original V-05 failure remains disclosed.

Preceding verdict: no acceptance decision supplied; discovery-01.md reports
F-01 (suggested P2), V-05 fail, V-01/02/03/04/06 pass. Complete finding
inventory: F-01. Influenced sibling surfaces: begin/recovery/finish snapshots,
all excluded from this correction. Attempts/discarded hypotheses: none;
deleting refs or changing shared tooling is outside this correction's scope.
Owning suite: not run; the composition suite belongs to T-003 migration proof.
Broad/aggregate gate: manual full reconciliation, no prescribed executable
command; not run here, owned by fresh independent discovery. No architecture,
maintainability or registry stage applies to this evidence-only correction.

Deliverable: updated ART-002 / IF-001 audit correction evidence. Actual contract
impact: existing audit handoff clarified; no new cross-task or executable
contract. Executable contract declarations changed: none.
Remaining coverage: fresh corroboration of every row, aggregate reconciliation
and F-01 disposition; no previously unchecked/blocked ledger row was dropped.
Next: fresh independent task-review-discovery → separate fresh
task-acceptance-review → owner disposition if the historical exception remains
unresolved. T-001 advancement remains blocked pending that decision; Q-002
continues to block downstream archive advancement separately.

## Exact tracked preservation inventory

Every row INCLUDE (Q-001), regular type. C family evidence/disposition above;
R/P kept active. SHA-256 and length describe current worktree bytes; the last
column is the index blob. Unlisted version differences are absent. Distinct
HEAD/index/worktree versions and mutable task-output handling are stated in
the current correction section.

| Exact path | Role / family | Unix / Git mode | Bytes | SHA-256 (worktree) | Index blob |
|---|---|---|---:|---|---|
| `.gitignore` | R | `0o644` / `100644` | 41 | `014d380a17e3e2445a29ee759e046bfad6452a29384e53b0438dd4cc46fccde0` | `1cec3400bc5f9cdfe8a51cf31b80d7f078513bbd` |
| `AGENTS.md` | R | `0o644` / `100644` | 4735 | `a1f46dd609e6a45de0c4c7887da7be3175f0b5a1dcc1f2455d3baa098dd2d5f0` | `4d0be232d374928d125fdc3d4bb7eb844dad098f` |
| `LICENSE` | R | `0o644` / `100644` | 1070 | `836a15b13285864fe1abc799a367cc78f2cf6eda828fd591411b3ba9cc1b4bb9` | `6125717b51440d7b6beec91d5dd2bd57d2d6e6ec` |
| `README.md` | R | `0o644` / `100644` | 24273 | `34ba8cab489af2608eb4e2a70c1c4e947fd38d81430dbcd010e47bb317da5aec` | `f71a050649d3ae91744649c709704e9ec8f2d807` |
| `docs/future-work/FEATURE-MAP.md` | R | `0o644` / `100644` | 12891 | `030aa49eecd2b20fbadb6cd286f81353277d786b065e19a1303b2ec1d7637661` | `d988cdc49557ad22bb4ad355e2d5cb5b2f9655e2` |
| `docs/future-work/concepts/01-delivery-principles.md` | R | `0o644` / `100644` | 5162 | `2e0176142a42cd4b93143bdc3ade5a428d2f8d0ce428d83382fc3ae08e27ceed` | `820fd3c6a55d5e4e24a2ae7ab2722e81f3638a78` |
| `docs/future-work/concepts/02-system-verification-and-test-quality.md` | R | `0o644` / `100644` | 5265 | `71c5155cbd41a763f6fa1dbde2c091eaafab85e4cead5412b3d346ec983bd7a8` | `d791f6026ffcc0e063b2b1ae6769937c1fcb8ff1` |
| `docs/future-work/concepts/03-documentation-and-task-planning.md` | R | `0o644` / `100644` | 5847 | `e8877d0afef364ea6106daba99075eb88f2428fe202b5e853765261fde9d1269` | `69dfcf6954268c89b0ec9c67a55022ec61d4a88d` |
| `docs/future-work/concepts/04-issue-knowledge-and-evidence.md` | R | `0o644` / `100644` | 7785 | `8cea1caccbfdd1ca32780198e3eaa6bfb20d13269bea005b37ecfa64aaf50bb0` | `f6da91837be49b53a1fbf75bc4a0aed47ba25fbb` |
| `docs/future-work/concepts/05-orchestration-and-sandboxing.md` | R | `0o644` / `100644` | 5472 | `9aa77422449935ec01fb446af668248f6b05fa07374760c990583f64b3d2426d` | `cb05f6377d5ee391d8cf6e93e4c386c5dc7ed973` |
| `docs/future-work/stale/deferred-work-after-t-o-new-flow.md` | R | `0o644` / `100644` | 15629 | `8a13153bc878dc98b538723c6601b21af9ba83fb1a99841e5a7c738a8b0c29f4` | `d29d61846ea48b0ddc456e1f85fd960999f38d43` |
| `docs/future-work/stale/issue_triage_portfolio_invariants_discussion_summary.md` | R | `0o644` / `100644` | 17922 | `d4833f9af0b7bcf58447fb63193a2d60a76eddee04aa3be87c4496b20274899d` | `b0945324b5d5852b1882d1116f22e63895c4d594` |
| `docs/future-work/stale/personal-skills-reconciled-roadmap-v2-2026-10-10.md` | R | `0o644` / `100644` | 52700 | `0db9fdd5bcec6a4bd255724b96601d8949fad623efb8bf45badfd48bfdf7872e` | `0db2c53037b546e0d1b9f62a4742aaa61426dd1d` |
| `docs/future-work/stale/personal-skills-system-verification-roadmap-2026-10-10.md` | R | `0o644` / `100644` | 41257 | `83168cc55514d38d15a75289890f65e96e84809bbc26a36ec2e01bc00262cccf` | `b644bc1a96571ab389cc82e882653e14796596c9` |
| `docs/future-work/stale/system-verification-workflow-implementation-plan.md` | R | `0o644` / `100644` | 29370 | `1abd1be4dac87fa0f942daf24736e565ed60201535cbb491ad7817caa2ec7f22` | `e881b56594b1cb9a69d84703673f259c9246bed7` |
| `docs/future-work/stale/t-o-new-flow-plan-amendment-handoff.md` | R | `0o644` / `100644` | 13662 | `35644bb13be3a28815ee12c278c3b39a9f01029b4e2711601197bf321219a5b2` | `e7293f493a70e5962fbd4d9ebca43f4eeccae33b` |
| `docs/future-work/stale/task-planning-coordination-guidance.md` | R | `0o644` / `100644` | 4650 | `7a46013d4921ada4593ba3f787975978865966b621ba238c9674579a6c6b8fb9` | `30dec060060315e6171f71328f17240ea9b16504` |
| `docs/future-work/stale/test-suite-maintainability-integration-proposal.md` | R | `0o644` / `100644` | 24542 | `4d61cc884e9fe05cd544fbd4b4eaf5babb59e5f9300ed8d4a7997b5bec58c6b2` | `0b1908ae034cc7784ad8ce64a3a2087b400d50d0` |
| `docs/future-work/stale/urgent-test-suite-guardrail-after-T-002.4.md` | R | `0o644` / `100644` | 16699 | `073c1b26ed815b4163d497aca3d6ccb5d6345082a88a8321838ed48acd118e62` | `88f636f6fa6e11e75bffc8117641416d07851548` |
| `docs/project-plan-review.md` | R | `0o644` / `100644` | 14786 | `a6405529bdea9b2820efc2cbf26f629ffb3618a0d8bb930daa41863d206c848c` | `384d070161e2d9cee41af6124acf1aca85a5f6b8` |
| `docs/project-plan.md` | C/root | `0o644` / `100644` | 44456 | `84168fadfc6d0f8b604f0357ef0c29ab01552b10795df70c3d258e430a4f5299` | `b1df1bb0a145f91d7d7f99b451b32e1f0a192acd` |
| `docs/task-map.json` | C/root | `0o644` / `100644` | 64169 | `2453a8470d0229bbac4b739cceb59e6480b7001c12116130b9141c2c39268e7a` | `8f546ae206e32859ecd2537abdd1656ae237e9ee` |
| `docs/tasks/BRIEF-P0/brief.md` | C/BRIEF-P0 | `0o644` / `100644` | 7827 | `7aa6aa807c906a2795c0b1fcb028eb85a2fa54b29647894e641ede7caea490fd` | `7e4d7ef9cc61a70abd9317a030e928ae1d805d9c` |
| `docs/tasks/INT-FLOW-001/brief.md` | C/INT-FLOW-001 | `0o644` / `100644` | 16257 | `93ec1b4614fb528f6664fc0b7b903986b0907589cc893039b96d88caa1ed15e5` | `3116f1f1aa4a8e6e81325020946b299608d33518` |
| `docs/tasks/INT-FLOW-001/preflight.md` | C/INT-FLOW-001 | `0o644` / `100644` | 4410 | `ebac6bc55e48de9c4dee843ebdf863747d3dd4d0c8fe7d2497c95212e459ef94` | `304c1911608b50bf66b786f9d4524a262ca9fb59` |
| `docs/tasks/INT-FLOW-001/results.md` | C/INT-FLOW-001 | `0o644` / `100644` | 9486 | `1afdd9f2ab12be47e0236d8cdce93386f9a259e06cf04898532bc729116118a3` | `f21363ab7a65a2c2a77f47e3bc4ae93e7cd66aca` |
| `docs/tasks/INT-FLOW-001/reviews/discovery-01.md` | C/INT-FLOW-001 | `0o644` / `100644` | 23865 | `62d4c46efb4225c57051a2c2b914b21e8a12f3168cdfae65a65fe357457831f8` | `99aa5b3038af649964105b26d30b7258d575fdbe` |
| `docs/tasks/INT-FLOW-001/verification.md` | C/INT-FLOW-001 | `0o644` / `100644` | 20678 | `55c5f2aad9e1ff89c00e374ec7db5edb7aec087dcb678cab44c7bc154b31537e` | `40ba778f32e7466f688c50929795b95dcbef3d7f` |
| `docs/tasks/Q-01/brief.md` | C/Q-01 | `0o644` / `100644` | 14817 | `48709a637a39c4c9ca14f4cd5b008a1b5f45158961bd94c2a8dbd28ad4665ad7` | `be80cdf7c8116ab74d8abdc5f3828de469d2e9c7` |
| `docs/tasks/Q-01/implementation.md` | C/Q-01 | `0o644` / `100644` | 8840 | `f6884fb62c758e9a03e9f947afb7faa337c3406ef36c6452a6bbef839e93b26c` | `0368238a4b69d8aa791399537c7fc97e2ef04095` |
| `docs/tasks/Q-01/preflight.md` | C/Q-01 | `0o644` / `100644` | 12383 | `44b2895f52a24730bf38f4f5bae3b173edb56ad2c9dee1abbdb1942b8286a590` | `e2ae0eafbdf31bd8e3d1a3764179242e39af37c1` |
| `docs/tasks/Q-01/qualification-handoff.md` | C/Q-01 | `0o644` / `100644` | 5246 | `0bba183b2b7c1a34f560266536dd6d1edb826b0109520482e89aa706b67b589f` | `918a8c54ffe0c1185fb71d6191e95ff591b1123f` |
| `docs/tasks/Q-01/reviews/acceptance-01.md` | C/Q-01 | `0o644` / `100644` | 15603 | `de813ec13b05ff147fc14a75c40a7f7295c27e2c9d119a11cb89936c20147849` | `1b6e932927b5175b82dec7d19797137008b6ff08` |
| `docs/tasks/Q-01/reviews/discovery-01.md` | C/Q-01 | `0o644` / `100644` | 23692 | `5379576272f9a0ef30d109917dee9ad723ba2de8e6f73389f80be74728926bc3` | `cff0cbb6e04dc6ac89662e823a6a921122282213` |
| `docs/tasks/Q-01/reviews/discovery-02.md` | C/Q-01 | `0o644` / `100644` | 25607 | `fcadff0adb23bdeb808f513aa2b3ceebc80fc7301004dcb8012e57ce68297f7a` | `074b894ab2bfe548cde9e64702b9696ea0dff14e` |
| `docs/tasks/Q-01/reviews/maintainability-01.md` | C/Q-01 | `0o644` / `100644` | 4055 | `83aa317161fe88c168d6c927503bb3063467236fd727c9efdb6d079a74e26959` | `a5f6ef90fc0d5a1abbb597d4b1bb836de01d25d7` |
| `docs/tasks/Q-01/verification.md` | C/Q-01 | `0o644` / `100644` | 20669 | `8824415c585825f0f32e81c75e23cb407856ab0f9419d95539234b5d2cf7da0a` | `3c5e9b04d96188927be1f71569a5ae182d1d39c7` |
| `docs/tasks/T-001.1/brief.md` | C/T-001.1 | `0o644` / `100644` | 8239 | `50bcec6eb320093de2d78b21280ab7030906c97c491e9a568eceacc47a2fc182` | `36f8c7ba45cf98a9401c2cf7899f89864072197f` |
| `docs/tasks/T-001.1/preflight.md` | C/T-001.1 | `0o644` / `100644` | 7325 | `405a631db56468bafbfd415a7c995d1775064e4620e93c1a4f0c38d8d76035c2` | `4af15cb32c0902522937f0a4f1b722e365debaf9` |
| `docs/tasks/T-001.1/verification.md` | C/T-001.1 | `0o644` / `100644` | 13895 | `237c9b1d95ee5d788dc4c60b02ff932cb5844664a09c63b0b9a6fd9bcf11bc4a` | `03f1a835520e248a988a3084f4c3f6e5739544b0` |
| `docs/tasks/T-001.2/brief.md` | C/T-001.2 | `0o644` / `100644` | 9196 | `9438e88d00d9e7199e71e41605b31e1fd02d2047d3c584ee55dee61ab72374b3` | `3ffad5e1f278c23667295439b6a688b6f283ad19` |
| `docs/tasks/T-001.2/correction-F-01.md` | C/T-001.2 | `0o644` / `100644` | 4907 | `ce0e09b1118e447543aff6fe930d4843e63590dbee980b0d37bc1034ae2821ea` | `ba2562da15c5e9193e55132562d8236f1f42cdaa` |
| `docs/tasks/T-001.2/preflight.md` | C/T-001.2 | `0o644` / `100644` | 6613 | `680dbab7614dd7b8793f5914746fb5d03bac5dd7081c6e25cab45ff247e7d8c4` | `8e886daaa36b47aaa0e8e2256ebf40dff97eeacb` |
| `docs/tasks/T-001.2/result.md` | C/T-001.2 | `0o644` / `100644` | 5340 | `5e2cf3f55aac0a60fa9859397ed9e6074ec2d90903a57552ca3c6ed4c117028f` | `8592ba5b08b70fd0811beac472c290569af7bc4d` |
| `docs/tasks/T-001.2/verification.md` | C/T-001.2 | `0o644` / `100644` | 15135 | `336ad0c9152513cf6411244385daf57fd6fca10999fbd4c579a1a2205d5829a6` | `0c756424369630d3b9eb3a9eec1cfc348bca8546` |
| `docs/tasks/T-001.3/brief.md` | C/T-001.3 | `0o644` / `100644` | 8661 | `e617a912e04ef854045b54fc34fe12983d6319a9f78336b3c0f148aab9d718d3` | `2bc2ccb2c44611629ea2d5dfe740d00f4c1a9497` |
| `docs/tasks/T-001.3/correction-results.md` | C/T-001.3 | `0o644` / `100644` | 4925 | `22453c0c6a266a58ed5657f07d0297b92fd731bca4806e2c4e8b42796a60be83` | `b469d95ffac7e0a26389e1045bf097002f579cfe` |
| `docs/tasks/T-001.3/preflight.md` | C/T-001.3 | `0o644` / `100644` | 8582 | `39af4e6746020326676c8c17e983cb867f869694d9fed3578b8fa1bab4e0c81f` | `4c1087fe077c72a5b97e529ef467be25208a6190` |
| `docs/tasks/T-001.3/verification.md` | C/T-001.3 | `0o644` / `100644` | 15038 | `09bfe5c789b7faa4851af024e282cf43b10ccd0681a7146ed055fa6954461357` | `b834cfcff8413755b77c83cd67a60fca92376ed1` |
| `docs/tasks/T-001.4/brief.md` | C/T-001.4 | `0o644` / `100644` | 8867 | `f961cc4a7a05c9ddcc936cc21b7982eae6ef6140710d4fcba7d04b6901b2c9cd` | `1a3407c14a290b514ca62d349541acf0a647df22` |
| `docs/tasks/T-001.4/preflight.md` | C/T-001.4 | `0o644` / `100644` | 7470 | `8a3ccb7b73b151de1f9e99e0afa477e7e57493cd2ed033e6466703446ae159da` | `9615cc402b760e9b92429a1c27affefbe935f6e2` |
| `docs/tasks/T-001.4/verification.md` | C/T-001.4 | `0o644` / `100644` | 11949 | `b174142ae420ad7cae946d752a5f29c3c4ddbc2954752fedb8adf0971da3311c` | `7c2dc4662abe5714155662a8b3938726906cebfa` |
| `docs/tasks/T-001/brief.md` | C/T-001 | `0o644` / `100644` | 5833 | `339730f0a562f8beb3c1ecaf2a4b70aa4bc40e4428b7420d8dbcfff27a5992bd` | `8ca21adfc5bf864030d5a8731a28876c60293b7d` |
| `docs/tasks/T-002.1/brief.md` | C/T-002.1 | `0o644` / `100644` | 9896 | `ddff79b2dd1f3b6c04114ed14f370b0e6a2034ad48b75a0d63bb4ce7989f9d7c` | `3f988c6bf6ddf3680617f32fb5a3e4ec8433b70d` |
| `docs/tasks/T-002.1/verification.md` | C/T-002.1 | `0o644` / `100644` | 19634 | `87fd489e60b83fac59d74c24cc9d3de5992a607e52b5645d9c8a2eddea5df64d` | `6208b2d52bd29fd234e865e7c70b06563a2dd16f` |
| `docs/tasks/T-002.2/brief.md` | C/T-002.2 | `0o644` / `100644` | 9153 | `2913f3e8d0b1fe76bdc6ace2e8a9004cd47fa676701e2de29fe4cc08775bb700` | `7cd329204c0f208c103767caaae8d64a43453cd1` |
| `docs/tasks/T-002.2/preflight.md` | C/T-002.2 | `0o644` / `100644` | 5499 | `9902161c2849f1a7f404beab692d7d0baffd753d6f32d41a64a495f59900a567` | `3dd8e3cf5e562fa81986ea0cf00a4873651e3cc3` |
| `docs/tasks/T-002.2/verification.md` | C/T-002.2 | `0o644` / `100644` | 20507 | `229c7562ed1c65cdca4d27a89141e0ec9115f716ec4fea0ab306d30ad4dd2b43` | `ae7a82786b63df3e8665f62b7fc2886a2bdc52b8` |
| `docs/tasks/T-002.3/brief.md` | C/T-002.3 | `0o644` / `100644` | 11117 | `5c8ae6113f6be1e38c1fda58efa7caba5b889306401978bf60e31b3867000ec2` | `88361b39ed1c7bd7e7cae8fec2e3d0ef7954e2b3` |
| `docs/tasks/T-002.3/correction-result-02.md` | C/T-002.3 | `0o644` / `100644` | 7499 | `19b1e3d420983751b4e8cdbf575a737d3c85b59bc71cdb86686bba84b27e909c` | `927873f63fdf67ad50178e97cf39828a5b30d81f` |
| `docs/tasks/T-002.3/correction-result.md` | C/T-002.3 | `0o644` / `100644` | 7381 | `1f9e70e547f330bb020595312da57326edfa04e1d01f3b75b40bd1d2ce11fb67` | `dcab22f4bbcf35de87808d435f11da558efbfbd3` |
| `docs/tasks/T-002.3/preflight.md` | C/T-002.3 | `0o644` / `100644` | 6909 | `e194494835f4819067ee33c27a47c0027be0e460a648ecac9e40e3c5aa8369c9` | `19815bf11074e2283714a8661972196e5166f3b2` |
| `docs/tasks/T-002.3/verification.md` | C/T-002.3 | `0o644` / `100644` | 19272 | `aa35a93ad6e196e9336e4652722263b3f72392c4819aaf671d395e76b115cf7f` | `2c70e210a3b75a8e77af5a304d7a3945ea5ca55b` |
| `docs/tasks/T-002.4/brief.md` | C/T-002.4 | `0o644` / `100644` | 9740 | `8593563b7b697f9e61412bb9074a59784bc88ec635086822c128105c6ba25240` | `42788c15a1bcf04f3d147d2443371f967cde2a2f` |
| `docs/tasks/T-002.4/composition.json` | C/T-002.4 | `0o644` / `100644` | 23059 | `91605a0a0531f5ee9d6fbbbd9b9e5313719e2a411e447406c272aefadfc1e0b4` | `ad9dbba6d6fd6725df55e078e9a39a4b1ab427f6` |
| `docs/tasks/T-002.4/preflight.md` | C/T-002.4 | `0o644` / `100644` | 9818 | `d5d4f2f75ebc8f8dd8c29b472c3b71f93eb638d7c962b9b39015f5935eedecad` | `de86c7e951d3e31c3ee9e4cd25237ce9023a595e` |
| `docs/tasks/T-002.4/results.md` | C/T-002.4 | `0o644` / `100644` | 8247 | `1f921a4073e83b9115e2718bb539b87ca860c328a13120d452d624f230b9b6ca` | `e03fc62349d298115b8ad0322749cd9914e91d14` |
| `docs/tasks/T-002.4/verification.md` | C/T-002.4 | `0o644` / `100644` | 19674 | `d12ab546b8b716e15311a5922b0cc0dc4777800ce9d5914d4d0ed575af096942` | `cd9bec9d1f32231f65535929190eeebdb4f5c71f` |
| `docs/tasks/T-002/brief.md` | C/T-002 | `0o644` / `100644` | 6680 | `ad805225aebe147079a7ea96fcafbf6464593aa7fb64683ff448b8b27a61ff5d` | `40268b468247d468adefbe8bb687d3a1b7aec851` |
| `docs/tasks/T-003.1/brief.md` | C/T-003.1 | `0o644` / `100644` | 7235 | `9693af27578075b1331e39335c185ab226f01a84df2c7718f8e36408e7acd803` | `ffaa83f2684cd9314cee9d3ff2fe9a6cdb255055` |
| `docs/tasks/T-003.1/preflight.md` | C/T-003.1 | `0o644` / `100644` | 4981 | `398f4c2d716703c0112d22a5468fb274a1f3aa21b87d59d3b6b98c988679d4c8` | `21c496a0dd37a9eda5799e4fd5b19071eba61d72` |
| `docs/tasks/T-003.1/verification.md` | C/T-003.1 | `0o644` / `100644` | 16037 | `82f31b596fbc99119db30e416cc22be4728ce4c207254f41de354655c7762605` | `73b74595879a0846cdc6925cbf896f93031da252` |
| `docs/tasks/T-003.2/brief.md` | C/T-003.2 | `0o644` / `100644` | 6786 | `9ef8e1459b99fab8deca899d21bf20215f9c5942ac6a081f5e93b3f51c98d88c` | `1d0f4c4e21cb9e9bf8b4fdc1120ef2187cbad6ae` |
| `docs/tasks/T-003.2/preflight.md` | C/T-003.2 | `0o644` / `100644` | 6062 | `dba7320bc9026d2a96cd77f4782237d157146340f9f1e30889d236c9db351604` | `f7d0e2aa9deafe266bcdab2b5d873bbcdb4f35b5` |
| `docs/tasks/T-003.2/verification.md` | C/T-003.2 | `0o644` / `100644` | 14238 | `1a0a1a3c842e50de31dcbe2a614750dcdfd6f9c3692ec4f040f4dc20991982a5` | `69f18ed3d31afdcae8f6dec4f073682c9394b443` |
| `docs/tasks/T-003.3/brief.md` | C/T-003.3 | `0o644` / `100644` | 10587 | `1b9e712aad4e5487459ab2db88c416b7a75395ea67dced7fba62f3c7871fae4c` | `a4d8fcf9f82b28e2c2f87315b286b23641e2f648` |
| `docs/tasks/T-003.3/correction-implementation.md` | C/T-003.3 | `0o644` / `100644` | 4612 | `513f094490e279bc91ae7acb90692c81da5261b77aedab4118c0f938e2e4ca3d` | `377e07d53c37e0118ff71a49b06a88c72f2e12ad` |
| `docs/tasks/T-003.3/implementation.md` | C/T-003.3 | `0o644` / `100644` | 7663 | `52e7a945e8b11f824d83407eb45110110b004976a6b3f7254485f2e39103d2e5` | `5b58366ee02abaef6a31ceed3ae67506cab3ccb7` |
| `docs/tasks/T-003.3/preflight.md` | C/T-003.3 | `0o644` / `100644` | 5220 | `fd82da4fddcb60d87a13b1e8575de721bb2ebdda061d136db067f1b0c62c4b87` | `e57c9c36e9c4300c70c9ec105746c9d125224b94` |
| `docs/tasks/T-003.3/verification.md` | C/T-003.3 | `0o644` / `100644` | 22226 | `fdda62c8d3e7d3a9e36c162a9714ff19ccf6d8617b3650f743eb4419b81c8b5e` | `75f63c1a18b1c4402523cab496149e2a916d14c1` |
| `docs/tasks/T-003.4/brief.md` | C/T-003.4 | `0o644` / `100644` | 9146 | `5834ac29048b28f5cc22e62adf8cbcd2ed0c7b6e104af48cc5aa5e2e90445313` | `42cb74a4d3eb29f60208f702b142518012f6ebee` |
| `docs/tasks/T-003.4/composition.json` | C/T-003.4 | `0o644` / `100644` | 23830 | `22be5d002effc2c1dc6823e0452411a5505deee63fab8222f1428bdfc1cb0fa4` | `9267b90f807c05d3baa511333b090e9bd49fa97b` |
| `docs/tasks/T-003.4/preflight.md` | C/T-003.4 | `0o644` / `100644` | 2605 | `6c7539c8dc62433b9192ddb1d3f97c771a6e776556092c5053ba6ed5bf8b2dff` | `02488b315e6ee2ec8e4a760e8f4e31ec03178761` |
| `docs/tasks/T-003.4/results.md` | C/T-003.4 | `0o644` / `100644` | 7085 | `efd9f2430b62483cbe7ac6b1b5a7216db17bc9efc44615f7926b755eef31f589` | `edfd856a419e46c583c370ec22cd16e6a611ac43` |
| `docs/tasks/T-003.4/verification.md` | C/T-003.4 | `0o644` / `100644` | 24490 | `577f425f11304fbf42bbb95110aa502d630e240f69e845cdaa05b98c59faa64c` | `66df63400e6d8cfb3f4839d9b63adf062ae19ae3` |
| `docs/tasks/T-003/brief.md` | C/T-003 | `0o644` / `100644` | 6200 | `72e0720e92e9c5c0e23982c057d3d4be3c76e03b358b75f282be290205af3661` | `cb64078f83760618a89613fda8facdc1f39f4c29` |
| `docs/tasks/T-004.1/brief.md` | C/T-004.1 | `0o644` / `100644` | 8667 | `161c03b2af0905d1c64809a0a9f63b3bb80b1532e51ed21392a12629bba16662` | `0744c01b6db8ece290e7dcdc527821de7ca144a2` |
| `docs/tasks/T-004.1/implementation.md` | C/T-004.1 | `0o644` / `100644` | 13254 | `cb64a3544c5b898661e51f6a4cd46bff8030d5834ffbb837bf8493bdd2edb51a` | `481a9d54ccde763576b3d0d2f575a90088a4e2e7` |
| `docs/tasks/T-004.1/preflight.md` | C/T-004.1 | `0o644` / `100644` | 6895 | `3c1ac9f8f5c88c07815c327999449da142c297275b983b8411abfa2fcfafa1a7` | `cef8a728a1a80966d27e629757b131065a4ebd9a` |
| `docs/tasks/T-004.1/reviews/discovery-01.md` | C/T-004.1 | `0o644` / `100644` | 37705 | `0c0e19e66f654d09f4cd2e2ec5a9e94e10b85a8995fe0a1c3a4234e53cb840fb` | `2d47ea2f8dddb4745ac741284f8252541c1d1c14` |
| `docs/tasks/T-004.1/reviews/discovery-02.md` | C/T-004.1 | `0o644` / `100644` | 29828 | `1d2503d96faac7dc3e6ed4e545dba5e05a8277990c3e2d813d51ee399fc60489` | `5e46d32d88d6ac75486386f2954485511d91b64a` |
| `docs/tasks/T-004.1/verification.md` | C/T-004.1 | `0o644` / `100644` | 15456 | `e37f02f4bd864892cc67fa8e03d678a4a32f3493b608715bef32d641eba68b95` | `e27bb0080ac0cd945145667d37ced87ed38dd826` |
| `docs/tasks/T-004.2/brief.md` | C/T-004.2 | `0o644` / `100644` | 9802 | `ecf57bb5cb33dda3405269c3f6adf05628248d2a4510fe34358d98d8e027512e` | `2fcc271eba983df31badc541eefdfd841927ea5d` |
| `docs/tasks/T-004.2/preflight.md` | C/T-004.2 | `0o644` / `100644` | 4884 | `8f8af39476e7d6d7960b9f3f0e14efe766383dee54d64db784445ee882c40d1b` | `461b53a417b84aec131e2efa1cafcd9d3af0770e` |
| `docs/tasks/T-004.2/results.md` | C/T-004.2 | `0o644` / `100644` | 31972 | `7bad160af3b6d69826164fd2ba1403ec40e855c6e782e1decb3a83f345680a83` | `409417ca54eb1878178431a07703534157fde599` |
| `docs/tasks/T-004.2/reviews/discovery-01.md` | C/T-004.2 | `0o644` / `100644` | 22653 | `3894d340174d81e5daef778c83e05ce96f394d56a03ab071bc81b27f6d3a0607` | `caa680abed8e73abcb183f3f2396f706da27edba` |
| `docs/tasks/T-004.2/reviews/discovery-02.md` | C/T-004.2 | `0o644` / `100644` | 23180 | `4d1067142a42315b2baa75dbadb599ace564eea1c17a07f60704766c72639dc9` | `50264cc9194fcadc74019cf3774fb1374f4ff040` |
| `docs/tasks/T-004.2/reviews/discovery-03.md` | C/T-004.2 | `0o644` / `100644` | 22444 | `eb7e3cc05a4f65c880a224aee88d91bccec0b7ea8b076c9d3d92ebd62eb29dbe` | `098724582b7205cb0b2802c14769985619eda4e1` |
| `docs/tasks/T-004.2/reviews/discovery-04.md` | C/T-004.2 | `0o644` / `100644` | 23217 | `fbcc7ca577ecfae19bf5048551fee0d1aeb1d63e0485ead43c0a844bec9978b9` | `f6943be00fde08b5578c62b76702550deae4753b` |
| `docs/tasks/T-004.2/reviews/maintainability-01.md` | C/T-004.2 | `0o644` / `100644` | 4434 | `555e42891ffe3e63afd6d6bf750ec5ecce10a929fa18f8b96bb8f8ba3e63c53a` | `e1ec29948a4ee47bedd5d9afa7a01a8d1ed86530` |
| `docs/tasks/T-004.2/reviews/maintainability-02.md` | C/T-004.2 | `0o644` / `100644` | 5094 | `305dadc736ddd6cf46d96512e24ff73f6b1cd037a4e263adbd74aa77094ce1b1` | `3fa2ce3ae9971e5354cd74f1038df1efa66cb8e5` |
| `docs/tasks/T-004.2/verification.md` | C/T-004.2 | `0o644` / `100644` | 14350 | `4966f69350e20d8563532d172e26acb6a8536e0c64635a62be0fb11f393c24b8` | `8f04ef7c68be835f2aad36e4c4fac0e055a7d0cb` |
| `docs/tasks/T-004.3/brief.md` | C/T-004.3 | `0o644` / `100644` | 9375 | `bdf0c28a9184c72438b69466046a7eece5971b34b30adf33e28f244adcdc4098` | `758a4aa7a4288e7b8e758442ae6c422a785099b9` |
| `docs/tasks/T-004.3/correction-02.md` | C/T-004.3 | `0o644` / `100644` | 15024 | `6a18772094c5dcaaf5eedd9df7b32d10c7f97d1a877220eabc7e6f571015bea7` | `71a208d075b4a7d13b57842cbf17005c71eb24ad` |
| `docs/tasks/T-004.3/preflight.md` | C/T-004.3 | `0o644` / `100644` | 12582 | `9f643161c31eb7ff1b90328e8f911b04ed79f82f3e80cafe5fabbe91bc1ea971` | `28f8dd107866e450e11c7386ff30dd1cad55cf4b` |
| `docs/tasks/T-004.3/results.md` | C/T-004.3 | `0o600` / `100644` | 27213 | `5189b2dc3a1ed2de8ca9b7fd673c3836b303af04f30b5cce9ed195990201a16e` | `af61ac08ebe4152ae2159796d1a8c064b4486d17` |
| `docs/tasks/T-004.3/reviews/discovery-01.md` | C/T-004.3 | `0o644` / `100644` | 26329 | `e22bdf908a5a27d772c302807f04acf72f5786b8bd40a8c5ba12eee27064fb96` | `ceafd28ba97536d6168aec12ca9fc588f76f250d` |
| `docs/tasks/T-004.3/reviews/discovery-02.md` | C/T-004.3 | `0o644` / `100644` | 24511 | `800e02e5bc5327f485f68d96da032429afadf6d34b3a63efaf94c254f030755a` | `acd7671760829a3b0f692ad77611aab177aa08b1` |
| `docs/tasks/T-004.3/reviews/discovery-03.md` | C/T-004.3 | `0o644` / `100644` | 18461 | `aa6243099ae3bce756205c5904526adecc96061ecdd292a7fab00731058776f8` | `e94cc36aab87216eb541697955c0b8b85601acd5` |
| `docs/tasks/T-004.3/reviews/maintainability-01.md` | C/T-004.3 | `0o644` / `100644` | 4940 | `cce4ecc9dd1bd829b868cd32da9ca1e29a5556da639bb4c3af511a5f44e1a567` | `a08f9965cee74d43d8d4ee8c0c5d9d568c5c6680` |
| `docs/tasks/T-004.3/reviews/maintainability-02.md` | C/T-004.3 | `0o644` / `100644` | 5383 | `d77f5a624788aa63171a84c76189840ca431864cb310066301e8bbab0e595d40` | `3d519da7a7280bf7cf8bfc6ad4a09aa74d1d4db6` |
| `docs/tasks/T-004.3/verification.md` | C/T-004.3 | `0o644` / `100644` | 14581 | `50bd1ef5fbd1e196ecfa130eea54d2a86daca0366e52a4b91654b51a7f1617d4` | `a5bddb43cefaffe6991246181afe8795571dd717` |
| `docs/tasks/T-004/brief.md` | C/T-004 | `0o644` / `100644` | 5683 | `f4d925897c25197118f915012c0802bc1378589812b82b03a240bc0f2b2e58d1` | `f8cc35c13dd5cc9d3e69ee103728169b24f856e8` |
| `docs/tasks/T-005.1/brief.md` | C/T-005.1 | `0o644` / `100644` | 7371 | `51c7a380f88cf493dd443b9e66d625609d9f10b8906eb71c723c566aa1a3b67b` | `dbc24f8a5ce6c23fd2975a81948984f5e08e8750` |
| `docs/tasks/T-005.1/evidence/V-02-setup-reconstruction.md` | C/T-005.1 | `0o644` / `100644` | 4414 | `e07b655511b64b50fb0a528b9e61914c9186dfd110683bb98e9e528d7df0ed4a` | `d742119b31c4845fd05f7105c4a88fe6c9f6bda1` |
| `docs/tasks/T-005.1/evidence/V-03-install-projection.md` | C/T-005.1 | `0o644` / `100644` | 13664 | `83b7b2dcd473f123f62774eeaab847800035ed769926feba042ebe4e7aa920ee` | `e10bad98ab9c650e866ba77c5e5744cf2d942880` |
| `docs/tasks/T-005.1/evidence/V-04-drift-contrast.md` | C/T-005.1 | `0o644` / `100644` | 3163 | `6c967a07eb0f13119f7374dbe5b3e5771573c331e0c5fd66aaf95044818ef239` | `7c9b97658db4c01c246ff762b7c483c10b142310` |
| `docs/tasks/T-005.1/evidence/V-06-consumer-git-exclusion.md` | C/T-005.1 | `0o644` / `100644` | 5539 | `b1113e1c4042f183bc7e5779902245e291996b4d074d794a10fe9d6c8a92eb80` | `f46f5cdf531b77e146f792a262d1131ba6019611` |
| `docs/tasks/T-005.1/fixtures.md` | C/T-005.1 | `0o644` / `100644` | 92045 | `f43aa5089c5a178662d505cac20c111ac757a3c6ffbc7ccc5f347df9cc66121e` | `062213e21636b696966040299850593b64b8b6ff` |
| `docs/tasks/T-005.1/preflight.md` | C/T-005.1 | `0o644` / `100644` | 12779 | `dd2e52866fffb3845134f0c9abd2bb70f0708738c669f6dc1af1b12ed03d761d` | `705fb3da9d845ea9aace91e9accc67c33d84a78a` |
| `docs/tasks/T-005.1/results.md` | C/T-005.1 | `0o644` / `100644` | 31050 | `0213374196e730f558980ab932d6a5dca89a76a2b9bf14a69e3346cc81e80803` | `90553f6ff2e7bfd824d9aa3010a84d0257d6065a` |
| `docs/tasks/T-005.1/reviews/acceptance-01.md` | C/T-005.1 | `0o644` / `100644` | 27980 | `9fe9fa63360383316037316e09705a0d2f8dc8de9cce59e277275b44bb4c7334` | `26442fff6727722743a2c58354f935f4b6933ea4` |
| `docs/tasks/T-005.1/reviews/discovery-01.md` | C/T-005.1 | `0o644` / `100644` | 25322 | `e2611400d2f5fbb4c8d06717edd7d6ebba96cbfbc1eb7b69ea71577dbb62048c` | `fd26a628495e610db293618c9454c907b4cb0bcf` |
| `docs/tasks/T-005.1/reviews/discovery-02.md` | C/T-005.1 | `0o644` / `100644` | 18418 | `fb5671278dd53c8d3981ddd2d47ae6a61ccf0f2a9e96520a1983d5193012ffc0` | `0c05c4c3b0227b2910b2b9295dd379b8f3575a9a` |
| `docs/tasks/T-005.1/reviews/discovery-03.md` | C/T-005.1 | `0o644` / `100644` | 17257 | `da388b57b7249fd94e0bd586d585534a3d474fd3bf72522d19cffe8f71bdaf4a` | `4c37841f00fe16a661bcb04533f89909f73f69ee` |
| `docs/tasks/T-005.1/reviews/maintainability-01.md` | C/T-005.1 | `0o644` / `100644` | 6396 | `2e3b470698ad584fbf24d04cd55b12ab944686e607bbebdde9ccf506e5cb3c16` | `f57648c98e43e76aea27455c6efb44cac42e1477` |
| `docs/tasks/T-005.1/setup_consumer.py` | C/T-005.1 | `0o644` / `100644` | 1186 | `9de04c2a82bbb84791583daa8e43bca7e9b984f3aef4fefa410a772afc5231fa` | `7e6abaf6d113fa46069ab660fb49adb5f991ccc9` |
| `docs/tasks/T-005.1/verification.md` | C/T-005.1 | `0o644` / `100644` | 13243 | `c7aacb05306660ae92548689ea69803f1314427e1559c74e8fd25b8b8ae3d105` | `d04a07a24be32993a913f2f348fbd30c0e966bac` |
| `docs/tasks/T-005.2/brief.md` | C/T-005.2 | `0o644` / `100644` | 7338 | `794247bc2477968d6394ce6bdbb9798ab6c06b96ed4d28ab7383da68ab391c77` | `7b7bea494086a04c04edff6e0b41dca527f40584` |
| `docs/tasks/T-005.2/evidence/correction-discovery-01.md` | C/T-005.2 | `0o644` / `100644` | 8147 | `bfb9d788653c56473073fd0025b43fc11767cdae449317a8c740d853f2984aac` | `e325ac043c11abbc4ca58bda461becf0a40507b6` |
| `docs/tasks/T-005.2/evidence/preparation-and-recovery-observations.md` | C/T-005.2 | `0o644` / `100644` | 13547 | `8851275160ea02f3ec00cc84fcfc60e11c6bf4ad8af8109a549f090c3268cc2c` | `e9d03877a0dbd465362d72e57d2a4da6bfdc2764` |
| `docs/tasks/T-005.2/evidence/run-log.md` | C/T-005.2 | `0o644` / `100644` | 9589 | `6472f642617bdfe1dd0f77d6bafe7b1afe13a36c86b3aa69b1859b39f72e5c59` | `97c9940a34621885270f5bf69f8e7dc770a0308f` |
| `docs/tasks/T-005.2/evidence/unrun-role-boundaries.md` | C/T-005.2 | `0o644` / `100644` | 6015 | `b63a5cd9f0dcab0a166aa2203a6b23a05627bfd69306e37d133fc99751deb752` | `b0bd1a5bed8342de1c16ebd460566b3ff5f1fa51` |
| `docs/tasks/T-005.2/preflight.md` | C/T-005.2 | `0o644` / `100644` | 15330 | `f7d367539891d51d1d07b428fc9953b4e10ad726446c74ad5d1af1b8b647b04d` | `5bde84ed969bea3c8f8428aac73cac25ec637640` |
| `docs/tasks/T-005.2/results.md` | C/T-005.2 | `0o644` / `100644` | 18788 | `d5ea695107b482fe3ebe7900b22f30b094350abc7206d455d9a9ca58471dc73f` | `13c1f938190bcf8b30f2d7d05583166024099d95` |
| `docs/tasks/T-005.2/reviews/acceptance-01.md` | C/T-005.2 | `0o644` / `100644` | 18408 | `a22ba852983fcd862061f9f7346dc8ef34c5677b53bdaba6b4a6e1d35a1f4d26` | `67f08ffd9baecd654be2786e5492f02e5048065a` |
| `docs/tasks/T-005.2/reviews/discovery-01.md` | C/T-005.2 | `0o644` / `100644` | 34964 | `61b130846b7c6365820837cb09b20d9be771227dbbb5a476fce436980cc62e09` | `4a3e3eccfa43cfe5b63e0bd0755a488d6b285e04` |
| `docs/tasks/T-005.2/reviews/discovery-02.md` | C/T-005.2 | `0o644` / `100644` | 28485 | `a641396c0dc1d1f068ec30997022ae03181eda02abb994e2bd94be9480d4167e` | `86aa2d332252a5473d3982abd2710f97042b9fae` |
| `docs/tasks/T-005.2/reviews/maintainability-01.md` | C/T-005.2 | `0o644` / `100644` | 8266 | `b0cd32c3cfc123c328765900b5d1c55d7ac8b0aaf38c000904445ad6de27020e` | `1d7baf1e9e3e575e50b4a25bb10c1ef71f36446a` |
| `docs/tasks/T-005.2/verification.md` | C/T-005.2 | `0o644` / `100644` | 16594 | `85f58c81d53fc6629baaf3eb663a5b3031d48f4b63982630e51fa7b77cd4431b` | `c36c8e2b44c5f6ca070d39c2916cdd2eb68f0021` |
| `docs/tasks/T-005.3/brief.md` | C/T-005.3 | `0o644` / `100644` | 9185 | `0f577d56b18fe48368d6b096a6ef625ca5b64c54e7a4c5db46037fb1d0169fe0` | `ae6fb51794871d429584e5e885acb9a16801079f` |
| `docs/tasks/T-005.3/evidence/authored-production-self-check.tar.gz` | C/T-005.3 | `0o644` / `100644` | 15515 | `4cc52c53380a2c4edd3fa091568405ef81c998da10e10423abcec1c9bae0618b` | `a8d279b1944f01a6b0ef7cd997c3ce950d54b365` |
| `docs/tasks/T-005.3/evidence/capture-command.md` | C/T-005.3 | `0o644` / `100644` | 6617 | `f9a724ed65b0e340cfbcd456b4c5a51f91cb69651b8945f1623fd88d3e9c09b8` | `c99925749830ba624cc663649eb6fddd97c237b7` |
| `docs/tasks/T-005.3/evidence/consequential-uncertainty-decision.tar.gz` | C/T-005.3 | `0o644` / `100644` | 18811 | `69fa8222441477c1c00f0f778f3a93b0a19c171187d8816ea67b630d2d8b1ab4` | `b6c3848045a9284abc4767c00b54b685172ab260` |
| `docs/tasks/T-005.3/evidence/consequential-uncertainty-resolved-decision.tar.gz` | C/T-005.3 | `0o644` / `100644` | 18997 | `f80000c869300a2bc1d90e5b0a998806c657f32be011c74422af2e22bd4465a3` | `6c1aaddf15f7ca7db8f8ec90071882349b75215e` |
| `docs/tasks/T-005.3/evidence/consumer-inputs.json` | C/T-005.3 | `0o644` / `100644` | 22651 | `66acca30ce56838988c60a1e5a31f741a2b476e4fbd4c018077b0d82908098ad` | `8a038183a151e6830ecc72cf589e799f59cc0861` |
| `docs/tasks/T-005.3/evidence/contextual-risk-blockers-decision.tar.gz` | C/T-005.3 | `0o644` / `100644` | 21107 | `6e703f89399b751146193f9ba52285151763b3827b8062178cd9fd88e6491bf8` | `f05fdbfb385a3faf66588a35ba9063653a11c178` |
| `docs/tasks/T-005.3/evidence/contextual-risk-mitigated-decision.tar.gz` | C/T-005.3 | `0o644` / `100644` | 20758 | `d67dea9f09b0338282e04feb522801e8391f602de37575fdb5de45c63535e906` | `e29102636ab531c524345ac1c4c4975547be0250` |
| `docs/tasks/T-005.3/evidence/correction-regression-decision.tar.gz` | C/T-005.3 | `0o644` / `100644` | 23533 | `7fede51bec25aa84f2b90bd9616f00ead5092040a63e902b53549716236de6e3` | `d845af402645ae8c3342c8657fdd4a5f297842b2` |
| `docs/tasks/T-005.3/evidence/coverage-ledger.json` | C/T-005.3 | `0o644` / `100644` | 26467 | `edcf1e9a0bce9e430835918b40db7618f22c1ca25d500a6e562139771814284e` | `3ffa57c26a1fc7b73c80e54aeb01e3bc9e107e47` |
| `docs/tasks/T-005.3/evidence/deferral-gap.md` | C/T-005.3 | `0o644` / `100644` | 1376 | `80ad85ea9c922aac233cd674471c5b9b2a40258c5ed08b901e6ac73cf6fb76b4` | `c49ec8a58685f2ec6713c4d6e62983e126d4ebd2` |
| `docs/tasks/T-005.3/evidence/discovery-correction-gate.tar.gz` | C/T-005.3 | `0o644` / `100644` | 21863 | `94bbbc8295eab1479e2d79c04910a9978b541d801b3b8ba1be89389e86118b7a` | `c983151fb9e55912eecd788cff6d06c627d35c11` |
| `docs/tasks/T-005.3/evidence/discovery-late-omission-clean.tar.gz` | C/T-005.3 | `0o644` / `100644` | 22057 | `f7c9608fc9521f95dbea38e01723f8bb8ea46c9a94477d57f5a45c4ed3bd7a9a` | `ccdcc276d1cd6fe5014b6ade23ddb5c7672f9052` |
| `docs/tasks/T-005.3/evidence/discovery-late-omission-fail.tar.gz` | C/T-005.3 | `0o644` / `100644` | 22054 | `1faf3b2f98e2ea984cd30137d60b355c6bc337336e0e5b06836a06918d71c78a` | `5f33e059afe1a4af71d2a178823b7b4ec14dc224` |
| `docs/tasks/T-005.3/evidence/discovery-prepared-ledger.tar.gz` | C/T-005.3 | `0o644` / `100644` | 19169 | `ebe9186ddcf359e3b21b30476b20068d55b339da82bfbd0327d61b58f21813bf` | `0548487a1c10e0499dcbeb9bdb1f9c4ad010f306` |
| `docs/tasks/T-005.3/evidence/exporter-accept.tar.gz` | C/T-005.3 | `0o644` / `100644` | 17901 | `69137b51e53d45c9ced417377bdb26e7fccb46a69c47743cd920d9c069f913d5` | `c2e3dd6eac3438272ac82c70188b705edb59b7dc` |
| `docs/tasks/T-005.3/evidence/exporter-restaged-stale.tar.gz` | C/T-005.3 | `0o644` / `100644` | 18097 | `79bf4f2c21054b314e709a7133ef64604f5f21835c6d10e0d9a00f0db91792c9` | `afc09e18c1484e448ca70a7d2e1638da3268a1ed` |
| `docs/tasks/T-005.3/evidence/final-checks.json` | C/T-005.3 | `0o644` / `100644` | 696 | `1204b630fe9ee1dca3c7df76dac62e8fc1886d7fd1278a815b03939f5083fe24` | `fa62aadc86fe1287634bd6156a94e314745e47b9` |
| `docs/tasks/T-005.3/evidence/known-issue-committed-work-decision.tar.gz` | C/T-005.3 | `0o644` / `100644` | 23086 | `652be8ab158032cbd29e5bc7a2fd37c916c4421ac396e5405e05976b1256c8a7` | `4b104fd74b1b33a91ba8ef9fba403e4534bcc405` |
| `docs/tasks/T-005.3/evidence/known-issue-no-links-decision.tar.gz` | C/T-005.3 | `0o644` / `100644` | 22817 | `d4f3a4cfd1ad2e5fc8055657cbd616e00f8fc422dc33bf921d0a1f666c321cf8` | `ad76e7326981f392b6642ad2ca27443ea0a6636c` |
| `docs/tasks/T-005.3/evidence/known-issue-proposed-work-decision.tar.gz` | C/T-005.3 | `0o644` / `100644` | 23135 | `48173584743f5c7581d2f09b30b63eac12a1248f08bc7ff6b2229a189488c1e3` | `550d55e337642302af2dffce4e61c43cea76cc47` |
| `docs/tasks/T-005.3/evidence/mixed-conditions-authorized-decision.tar.gz` | C/T-005.3 | `0o644` / `100644` | 18607 | `915fce357e59451ae967607bd33cf6a8a6d17b1e2284d84dd2aded4d8f31f3cb` | `722ac304dc2be8fb66a36d5a3a49142215879b8e` |
| `docs/tasks/T-005.3/evidence/mixed-conditions-forbidden-decision.tar.gz` | C/T-005.3 | `0o644` / `100644` | 18662 | `68c7df5c5d8f350304e629a9127686ede76fbf59539618a0d3b9d3a5e25f549f` | `08ba7087de9b46262d2fa2282a467e4515b1819f` |
| `docs/tasks/T-005.3/evidence/owner-checks.json` | C/T-005.3 | `0o644` / `100644` | 1541 | `d610841625ceeed5007f5716235591ca4a03b112a7d55104d3ef53b2ba62bee3` | `bfd4d0ee04efda6c744d2ffca9723b38810a534d` |
| `docs/tasks/T-005.3/evidence/protected-before.json` | C/T-005.3 | `0o644` / `100644` | 101618 | `28f580a7e5535df3498564764a6ad80938d755cb81b72bdaf402ef09b816dc9b` | `3f15c3bfe0dee36d1b3958467daa4dcbfdd1d405` |
| `docs/tasks/T-005.3/evidence/public-probes.json` | C/T-005.3 | `0o644` / `100644` | 11087 | `ba79efd632e90c819e307d020b0ed9757bc076430944dcdaceaca304c9326ee1` | `faa1e12c6c27307482f63565de2deb4a016fbac0` |
| `docs/tasks/T-005.3/evidence/queue-defect.tar.gz` | C/T-005.3 | `0o644` / `100644` | 17106 | `ecf3c54f9a9e61a56a74ec1052573f322a0c572a558757f24f6907fd2a2c3286` | `beecafcd81e34a85f964ddb9b23e92e4098ac75f` |
| `docs/tasks/T-005.3/evidence/repeated-review-changed-context-authority-decision.tar.gz` | C/T-005.3 | `0o644` / `100644` | 29745 | `9aba4c55612e88bc3d00cb03c4e3ffa27d47ad452c664f35ff47c7c2abd8d236` | `0653cf1eb98eddaeffd52bc969f70483017b68d0` |
| `docs/tasks/T-005.3/evidence/repeated-review-formerly-blocked-evidence-decision.tar.gz` | C/T-005.3 | `0o644` / `100644` | 30438 | `58dedce6758e7ef93d24de53e97ea8e03c49acca49b727cffa784cb74193d16f` | `c463bb23aff977849f31b0383ab8da4ffe9bb928` |
| `docs/tasks/T-005.3/evidence/repeated-review-missed-existing-obligation-decision.tar.gz` | C/T-005.3 | `0o644` / `100644` | 29807 | `e8be71cad7c182e4d0a0101145819373a47cbb2ec369e44b239a1ca082627c62` | `371d01ce80ce69b0ef5df4314574ce766dbdd6fb` |
| `docs/tasks/T-005.3/evidence/repeated-review-newly-demonstrated-material-risk-decision.tar.gz` | C/T-005.3 | `0o644` / `100644` | 31000 | `3131de762e72722488c336da55a8d4fcaa489a9132c73d4fb36dc406f2c2a075` | `3e0e5bbf7a816b9e3b9ba7edb2ed8b01421ac7df` |
| `docs/tasks/T-005.3/evidence/serious-delay-uncertainty-decision.tar.gz` | C/T-005.3 | `0o644` / `100644` | 19126 | `c99fbd294f80f1eb170d1b0c08998f1ed42910a46dfafe1971322c7b8faddd24` | `4f77021861a2a926231145a49274d3420fb0d600` |
| `docs/tasks/T-005.3/evidence/serious-delay-uncertainty-resolved-decision.tar.gz` | C/T-005.3 | `0o644` / `100644` | 19268 | `03eb741690cae128dba2a5dc1e2844514f740436fe3e9509e349134ef9ea12e5` | `6404c9e1710271ef7d1857ad2c1c94791604b44f` |
| `docs/tasks/T-005.3/evidence/staging.json` | C/T-005.3 | `0o644` / `100644` | 277050 | `69b96af4d58398a34f77b5360e5e3379d761fae63571ce75fee78a911d010fb2` | `ff4c3149b4bacfd2f177f833a209b50f2e333f2b` |
| `docs/tasks/T-005.3/evidence/submitted-targeted-checks.json` | C/T-005.3 | `0o644` / `100644` | 2387 | `1c172cd741715a9a13dd080c9e5fb7d73e0c46cf0eb38d618567772e09e2cf08` | `5e4c8945d8ae528b399ddbcd0b689a70b589c971` |
| `docs/tasks/T-005.3/preflight.md` | C/T-005.3 | `0o644` / `100644` | 13228 | `c076ff391a57d741948af9fcbca36d6a67028ac58e61326cb0049fde060bbc70` | `d34c67be7be04e14d959837c63b5ee2a8cf59998` |
| `docs/tasks/T-005.3/results.md` | C/T-005.3 | `0o644` / `100644` | 14659 | `2ba00570f2368e4ea7def50fed341c009c33073d70d56bab60712a4b5cc3dcfa` | `02ff2d8f6c87af6e0358db48dd7216c6b59f15f3` |
| `docs/tasks/T-005.3/reviews/discovery-01.md` | C/T-005.3 | `0o644` / `100644` | 56926 | `0a65b6235e1549692266b07b1951167cd5444a2455a8b3d4109577a20798c13e` | `aa766584d9fbba106d187d53fe70a8bd4be8c984` |
| `docs/tasks/T-005.3/verification.md` | C/T-005.3 | `0o644` / `100644` | 21080 | `2f30d900abb09d337d273dfed738e69fd8205a556551279969510be72ec06190` | `3500cf41b7c5da0695c9637fa39eb3103e8c480e` |
| `docs/tasks/T-005.4/brief.md` | C/T-005.4 | `0o644` / `100644` | 6697 | `ace5e94abcb08a22abdab6c00ae655ba65d7381dd570bbbb5951a92f0d187420` | `134e466def2888e96774094286370aecf74f6a67` |
| `docs/tasks/T-005.5/brief.md` | C/T-005.5 | `0o644` / `100644` | 10636 | `e792e6e31e5852205383b54bbf2f827775f7d492b6a64c3c4b8de69316e205d4` | `65e0c7099bb9e4338265ce9c7e310d32895dc94a` |
| `docs/tasks/T-005.6/brief.md` | C/T-005.6 | `0o644` / `100644` | 7286 | `4edb909f7de664c9dd9d9a05b9dfe87b861562294997bc9676d17cd3a044e0d5` | `ba6e03b374e3126beab344794e95e421515a109e` |
| `docs/tasks/T-005.6/evidence/check_report.py` | C/T-005.6 | `0o644` / `100644` | 2365 | `93c232d55e2a98af187cdc8457e7c88d72437c5a446ab3a674e3cc022b0238ed` | `8b221ce935a97d0c10975b6ca36f882c6500dc63` |
| `docs/tasks/T-005.6/evidence/protected-before.json` | C/T-005.6 | `0o644` / `100644` | 78963 | `7dbf3e5246d30831fd6eb92a9057d63776a425fbdd3d1c459c2f8d071f648b7f` | `bc31231243f179acabcdb6970f271874c98e1404` |
| `docs/tasks/T-005.6/preflight.md` | C/T-005.6 | `0o644` / `100644` | 4677 | `6a97a9a0f2de84d51dde5d1baa8ac0d67744596d3b07c4e86f38df865df54d4b` | `e38f9d310877fa974ff531b5aeb6a4e01de92981` |
| `docs/tasks/T-005.6/results.md` | C/T-005.6 | `0o644` / `100644` | 4763 | `68baef5312b3c42bfb5066936044a7b40ceb524dfa304446f3611adb795f3689` | `a521f6b4a3f440a96a0480f945af2f6c1b6e926a` |
| `docs/tasks/T-005.6/reviews/acceptance-01.md` | C/T-005.6 | `0o644` / `100644` | 5772 | `98e5d9d5df08f2e584d4f1d0c9b9fb945a49def751ec3439448a6e25d59f39d6` | `8113a7b1ac30265ed9c73e6dfdc1f839b9bad4ec` |
| `docs/tasks/T-005.6/reviews/discovery-01.md` | C/T-005.6 | `0o644` / `100644` | 23857 | `8223205a003e89da939a98ac761e09eeb167ccad9718b1892932d12866aa3d28` | `59e48ade9fd79ea7d2deceab572b1c742d3f41ff` |
| `docs/tasks/T-005.6/verification.md` | C/T-005.6 | `0o644` / `100644` | 4183 | `ab93f3b190a5f14b8a56a0470ffabfe7024ae4489e05b38f1b446aa22dae4ba3` | `b7c2fa3ad91bcd7270beaf1f77be40d2cb57340b` |
| `docs/tasks/T-005/brief.md` | C/T-005 | `0o644` / `100644` | 9923 | `00f606b4b83ec7ff31ffa9d69a88d7c5f32d4eaaceaaf042ca61d8a3035c8626` | `bb25098b9023249f26dc486ca5d2abb60007a44e` |
| `docs/tasks/T-005/reassessment.md` | C/T-005 | `0o644` / `100644` | 10735 | `5ad04df562f5babe3c408e4d5135eef976b818b03169e329bba2f123821ab6c0` | `ab3aa15735219ffba848615d1cae1db5670df957` |
| `docs/tasks/TEST-STAB-001.1/brief.md` | C/TEST-STAB-001.1 | `0o644` / `100644` | 9107 | `73471a7e4fdad30a72ee010b9936906f95227bec4a38f8267024efaaa568c100` | `57a6d6469d01b55a8af0cbd2f8f308194aa0fba0` |
| `docs/tasks/TEST-STAB-001.1/preflight.md` | C/TEST-STAB-001.1 | `0o644` / `100644` | 7092 | `508b90acaf1165948718b0b80bf4b4094c626d5e21f9719c8c05f9907b218fc4` | `027ed8234d760ea580a55070e78c12d3dc01cf65` |
| `docs/tasks/TEST-STAB-001.1/results.md` | C/TEST-STAB-001.1 | `0o644` / `100644` | 8851 | `15fb368c6e0068447241149908ca502d886796852ed9cfa156cb6b705038ec47` | `f53fa8ac593093235dce4b8632ed5e47bfa9694b` |
| `docs/tasks/TEST-STAB-001.1/reviews/discovery-01.md` | C/TEST-STAB-001.1 | `0o644` / `100644` | 46082 | `b49d315219ddd63b8dae2fd4b7c8d8a58661c1fdd7fa2a0247c24a8211b25a77` | `8c6e502fe536cb96df7337c47968188b2dda8587` |
| `docs/tasks/TEST-STAB-001.1/verification.md` | C/TEST-STAB-001.1 | `0o644` / `100644` | 14851 | `4abfd3a232e7b29689814cd20e65b061dc8b0c556b3ef591145a18840cd0850c` | `5577059cd81efcb2aaa81693e0b49def0fc56836` |
| `docs/tasks/TEST-STAB-001.2/brief.md` | C/TEST-STAB-001.2 | `0o644` / `100644` | 9816 | `4ae8ce1d11be7f1ac484f1afae108a0e9a390ba97687aaa6df5bbede913f3389` | `ea055db60d70267c33dca358d218162fe0eb478a` |
| `docs/tasks/TEST-STAB-001.2/preflight.md` | C/TEST-STAB-001.2 | `0o644` / `100644` | 7577 | `75e698a1ba0d09dc7f3491d9bce8c1b7806ffecf67721547a54e4ae54a21ec65` | `15b50b5645bb7fdcd7422aff3fca5cc82baa7d30` |
| `docs/tasks/TEST-STAB-001.2/results.md` | C/TEST-STAB-001.2 | `0o644` / `100644` | 9042 | `901a22ec4ea4c37783cbc90ebb1445e318a5bb323d927e2278765ac0c21a5fa8` | `7e78c93208cdd3fe046d1091e37fe6c7632b1546` |
| `docs/tasks/TEST-STAB-001.2/verification.md` | C/TEST-STAB-001.2 | `0o644` / `100644` | 18317 | `8fcdc8bc9c0adfd257e0fb86e12a3bf4a14123ff3dfc2d70af2b109d40f0254a` | `58b87b23f68ee9a5c1083a982d40d8b78af7d7ea` |
| `docs/tasks/TEST-STAB-001/brief.md` | C/TEST-STAB-001 | `0o644` / `100644` | 7126 | `07c773157e148056cba4f56fe8ffe0e95d2de51c1efb3fd0ba16be171b6fe0f9` | `42604661d02974bd8babb969ae96664844e6fe17` |
| `docs/tasks/index.json` | C/root | `0o644` / `100644` | 7334 | `5b859d147c0da2b1d864e8441269ebeae2fae574caf23254abf21640f2b40f36` | `333c15daac8add582daa71ef3b02551a47d39147` |
| `ideas/documentation-consolidation.brief.md` | P | `0o644` / `100644` | 12163 | `3f40854566a9fa9fdf9399870beb5e48167d7c97f5385906cd0efa709c8b3a08` | `0c127abcbdce9895096d56a5ef06932bebf97e75` |
| `ideas/documentation-consolidation/project-plan-review.md` | P | `0o644` / `100644` | 17391 | `31ffdb66574278512f8ff6292a0c425a429ff40eb9cb156f74e3eec51fde046c` | `ced43fba4e813b9fe4922b95c9ea76d934cfc2db` |
| `ideas/documentation-consolidation/project-plan.md` | P | `0o644` / `100644` | 29254 | `f1ddf8fd3c9c3865dfa5c5eac1b58b46ef309be74e9088037bae97b8df1ca22c` | `a8e4e0b25005896d684c5a4b84c8ffea46a59e0e` |
| `ideas/documentation-consolidation/task-map.json` | P | `0o644` / `100644` | 26011 | `6f5b838776eb4e0ddc7badecceb911562e5e3262af93a882ca2eca2fc69d9201` | `02fa20c7fa03d47a03049bd9b5fe54b6cdc3b802` |
| `ideas/documentation-consolidation/tasks/T-001/brief.md` | P | `0o644` / `100644` | 16836 | `94cc2e185f1aef939a17d23db629cfef90bd33d6aca7727ad3de1ddaf65a2ebf` | `62e32efa44c79980c657cdb163f097c5969de2a1` |
| `ideas/documentation-consolidation/tasks/T-001/preflight.md` | P | `0o644` / `100644` | 18224 | `f60a74cd02f97ec032fc97a2fede49695729f1d383345ea94dd9ba20dab7ef5e` | `3d4c3ee7e32f1789d203dc5a5bab71d13033eead` |
| `ideas/documentation-consolidation/tasks/T-001/reviews/discovery-01.md` | P | `0o644` / `100644` | 24402 | `3d2ca9c430bf71c0dd521d42117a4ebdf54ece6d57c0b28983b5aa45e70d71c8` | `27adaefa1091687a7eff58feb4e8848fc5707f0e` |
| `ideas/documentation-consolidation/tasks/T-001/reviews/discovery-02.md` | P | `0o644` / `100644` | 17475 | `44375e4e35c126547d37b6050720f8af4574a0d9e30c27983b7eb8a1ba0f7337` | `7858a5823f35fbf199f87bf8c4d7a219eb6e014c` |
| `ideas/documentation-consolidation/tasks/T-001/reviews/discovery-03.md` | P | `0o644` / `100644` | 15668 | `6485ca875fdf74ed8448cedc51e705b2df22985f10857aad50520a3fbc950aa7` | `6b7e1ec5a7d8ad8cd139a03483efcc6e7876723f` |
| `ideas/documentation-consolidation/tasks/T-001/reviews/discovery-04.md` | P | `0o644` / `100644` | 30074 | `3b06c915f18c45fff8972ab4df74024cafca64bd1fba0972271269f5f6917362` | `aeb5bda4eb433f962e98383ee3fb79454ebdea63` |
| `ideas/documentation-consolidation/tasks/T-001/verification.md` | P | `0o644` / `100644` | 16095 | `962a9b138d3491eff9ee4d6a372226af8cdbc9f7062d389308c1d8f699d616b1` | `466649589415556db695b97200e5761151b91175` |
| `scripts/install_development_skills.py` | R | `0o644` / `100644` | 23910 | `7423852ffc55738e28ff9562007fa4b511b537a20b2dd24275886fb237370d78` | `733660ddf14079482a000e1579254e5cd6dcb08f` |
| `scripts/ollama-models.json` | R | `0o644` / `100644` | 1609 | `fea9ac0f77cb02aa286e1dfbcc7794b42d76e07bd73f9aba3badc7129e7422cf` | `00abf37d2f599aadad8f2ac7ddf563ed5a8757f2` |
| `scripts/ollama_delegate.py` | R | `0o644` / `100644` | 19796 | `449f1b2b27ac008b12d595c70b2efecc8620cd4012c59d44a6c4eef3820ffeb9` | `3d8f095433a66c60268ed9f05587ddf21306b94d` |
| `scripts/run-evidence.md` | R | `0o644` / `100644` | 5564 | `6d22776ccfdc600a8edf4dff0d2aa3059ab1ec04201cafcc809ba45a639e6987` | `215d7e2edd9df56039f4a80e0f7f2bfe32533d5d` |
| `scripts/run_evidence.py` | R | `0o755` / `100755` | 20534 | `ca3aa13c4a4c443924938598935205099f639bd39da848f175149e5d5074209a` | `526b884010d8f90a78a660f7d2062dd1a104d7c4` |
| `scripts/runtime-context.md` | R | `0o644` / `100644` | 2361 | `7c8f3340a5f4c94dbc44947af07dc18fb729ff9373ddbb272048bd7a580222e0` | `56a673223d6a8a51f020325421c813d0b4c3c037` |
| `scripts/runtime-context.schema.v1.json` | R | `0o644` / `100644` | 1876 | `5ef06905b0112acd252f20e1e636444ba1c25d19805474bc6efcc67756176566` | `b37a1a5a196b36fd808ed05d69934ac2d49289ca` |
| `scripts/runtime_context.py` | R | `0o755` / `100755` | 7188 | `49392889c17a7f9f83a62695867a3bd31c4c1767997b5cad2e1dd0085d85ac42` | `b8158073604f5375c884595897653456417c527c` |
| `scripts/workflow_version.py` | R | `0o644` / `100644` | 10155 | `2dd89ff03a709d046992e9de6ecf9b04e8103edc0dbc4b2dc80e773010125e43` | `3480f3cd5b4476e92f4303cf545460ab46376aac` |
| `skills/README.md` | R | `0o644` / `100644` | 11491 | `8e8e5b0db9169071e28f78a0af4d1de8661102ae83f48012014e127edf946503` | `334a2364d1bc05026d2b12978a1cfba7b91b411f` |
| `skills/ai-flow-foundation/SKILL.md` | R | `0o644` / `100644` | 8634 | `fc26141c335975d262c3e1978129e06abbb35f3027a2dff89a00d4c725d291d6` | `a00e9d713d6bb180b4e03e1b651626725b3c7dc9` |
| `skills/ai-flow-foundation/templates/ai-foundation.md` | R | `0o644` / `100644` | 2065 | `ab8d1fc246a68ac081ed8a6a3704198732451ac5241acd61f9603cb60c2c15db` | `562a0a5176b84e373fab3e96bfb5f81268ff699c` |
| `skills/architecture-guardrails/SKILL.md` | R | `0o644` / `100644` | 15861 | `fde86e50f9f6037f7be61a067cfcb3cc55197e65565e1c07a5f06f83c5fcf016` | `089ae66082f1857c9309b3f9d360330ba867f6b6` |
| `skills/architecture-guardrails/evals/evals.json` | R | `0o644` / `100644` | 2895 | `7b50c746b46cf55a4e9da361314bca9a7ff7854793294531d8d9930eec5e4777` | `567e2c46f241d27482f33da641ecd9bc4a387742` |
| `skills/architecture-guardrails/references/dotnet.md` | R | `0o644` / `100644` | 2684 | `12609dc1e6c46a6372a7d37d0d48149b0eede0418944a4b2a37d5dddcb91bb48` | `bde33ee0fca295e39cba18e9cf033402f2aa56e1` |
| `skills/architecture-guardrails/references/enforcement-model.md` | R | `0o644` / `100644` | 6419 | `9fe3bf7d04e61b7859ba67d34c4825623c440c7ec948f2c4f6303cecc4e34885` | `7d242d7e3ec1301e97dd90a0f161094693f7d607` |
| `skills/architecture-guardrails/references/java.md` | R | `0o644` / `100644` | 2808 | `d7647076d4d646857a69d9d7d6b015b8f5183c905e95ac2c18e4175267f229ab` | `f41efae8389e391c90b7d2ce7b2af6fdeeea9837` |
| `skills/architecture-guardrails/references/javascript-typescript.md` | R | `0o644` / `100644` | 5520 | `dc4b59bff201c184798a27d33de1cea01fc656418cde9534aa9756235ca9db76` | `218b1ed932e44be82019a2ea70fb48ee41fa95a6` |
| `skills/architecture-guardrails/references/python.md` | R | `0o644` / `100644` | 3580 | `173a0dc18e2254082d980a1e518423b9ffeb01fde1864933cf17941657d5be20` | `9db6dba2bf5319750c7b29911a85eac49b33daa4` |
| `skills/architecture-guardrails/templates/gates.yaml` | R | `0o644` / `100644` | 668 | `9726dc7bea108e6068bec9cb6df8ffbb51d3a48b797726dfb706b660176bba36` | `195ee3b4be1800dc54ec38318d59a3954c645305` |
| `skills/ask-user-questions/SKILL.md` | R | `0o644` / `100644` | 5345 | `34a5d62b9c5cd9d6b16db91dfb96f989a35688e690d1324a45db4b6d70ccc5a2` | `36b90c0d5daf092bf2c0f3bec2f7fb80de7d44de` |
| `skills/ask-user-questions/evals/evals.json` | R | `0o644` / `100644` | 947 | `8aefe4692b6cf6fadfb7476b2756daa1f68b264fdf9407d8737f983c6bf30229` | `904beac1e3912bbc93fcd6cd5bd085af666afcbe` |
| `skills/foundation-readiness-review/SKILL.md` | R | `0o644` / `100644` | 9196 | `583235afffc4cc1685fd4b9b0b1e2fc7f0ac5a124dfafe013a3c473455fba844` | `f4e4a87f7cb3d07a1e23aa38d6836cc0e3358afb` |
| `skills/foundation-readiness-review/references/delivery-routing.md` | R | `0o644` / `100644` | 4977 | `3dd01ca2b63c33c3c591362430a61367332c178d056cb0a5bc28b1b47c9d53c7` | `82f5f1fc55182a9140b45b867ffa8957d2d0c135` |
| `skills/foundation-readiness-review/templates/foundation-review.md` | R | `0o644` / `100644` | 1816 | `cdc1fd4dec2325469d9e70ac79532b520ee94360b05d731eef1f2695f02775c2` | `75bb108c2ddc4a99a8c3488d43d27578ddc0b8e4` |
| `skills/idea-brief/SKILL.md` | R | `0o644` / `100644` | 7535 | `b3d9b5762814c427effcaac93ea428b9a163b022d425df34af68eee6321adc6f` | `14abc963b430be2ca79d4c950ad8606f0dbe2dbd` |
| `skills/idea-brief/evals/evals.json` | R | `0o644` / `100644` | 1732 | `2178078cf5e99dc6ec99d23b4fbcae9da1333cc26c0e72d39746d9b52adfd53a` | `68b774c90d9e641c5b00e418aed6e8d131eb7143` |
| `skills/idea-brief/references/vision-template.md` | R | `0o644` / `100644` | 2914 | `02c9338131dab83910192ef52e2d9238248422b6541956bc1325d17174d3d5aa` | `5bb5d0496eba6d280a9676591155de67f59c9ec4` |
| `skills/idea-challenger/SKILL.md` | R | `0o644` / `100644` | 6735 | `ef6d1ca29716e4310ce6a58ccc3311285ad44d9e445ea3b7cd71e98150481822` | `3d19944cf04ea9d7c8e26591b3abbbc25446a1b7` |
| `skills/idea-challenger/evals/evals.json` | R | `0o644` / `100644` | 1413 | `31d4da1a8edd8f7d68003aae64e55939dc9f6cf0d399a4589f8e91e01b03b7e9` | `3b368efb1684c682d033e6806df8a38d355cc9a4` |
| `skills/idea-investigator/SKILL.md` | R | `0o644` / `100644` | 10937 | `7bed4519379691eb019a7eeadcd5c77ed5d8aa05cd493bee2858298d1991fa42` | `6e3cedbd118a0ce78037c11c56789d555a3189cb` |
| `skills/idea-investigator/evals/evals.json` | R | `0o644` / `100644` | 1407 | `6edf10d2e21aa1306cda466e25dd3a75ea7c556cfe1daf8150aa121fdafe470e` | `df5f17358d134060ea9a69f467ee7b2e33525050` |
| `skills/ollama-delegate/README.md` | R | `0o644` / `100644` | 2751 | `bedf867803a49e7483076d2f12e06f5f848d2363586d12ae03e00e63dedaf743` | `389b06e7dd9775ce4a112756c8192387eb50be3c` |
| `skills/ollama-delegate/SKILL.md` | R | `0o644` / `100644` | 6124 | `bb775840081d3efe5ea4c50f4936f8539601c359b5555d396d8e8950d0ad75c9` | `f546b10a2cb7e08f55efe0f524dd4fcf9b22bfff` |
| `skills/project-bootstrap/SKILL.md` | R | `0o644` / `100644` | 11663 | `f4a10ad767a37f383c6be87e5828c1cc65aac9b336f51abd78129b39b56c4ce3` | `42992b2c736d8cea1483c4077769cf7139b2d2f6` |
| `skills/project-bootstrap/templates/foundation-plan.md` | R | `0o644` / `100644` | 1337 | `cb69fef2d25d3ba024fd44263fe84d5909eb8471267e224b1b884b4ae455110d` | `6ade3f6972374472b396a4dec02ad2441604f610` |
| `skills/project-bootstrap/templates/project-charter.md` | R | `0o644` / `100644` | 778 | `a964172375619bee52898e719e4076957008fe93c495be3a0d46f6bb16c03630` | `7fcf7011692d61121904cb0ad5356713427a2801` |
| `skills/project-delivery-plan/SKILL.md` | R | `0o644` / `100644` | 15829 | `4a06045e3f595ebccb2dfa311d890be00bdf6da84aea3b141f8e7c3cd27fa037` | `8e86ed44d936f4957f9f11e1e07cba99c3d8b959` |
| `skills/project-delivery-plan/evals/evals.json` | R | `0o644` / `100644` | 1507 | `a87fd7309847d598a56a253254aed5c5867ee20a2f1c42ac3e028f1f288ab007` | `fb28b930242e1304d7e87b5de0a1e376f7186b3d` |
| `skills/project-delivery-plan/references/project-plan-template.md` | R | `0o644` / `100644` | 3768 | `7b766a9173cfd69c6fe619441c8b0710c36f18a0b2fe00e3fae13e6aaf8c097e` | `e053690125c92600f388980981f09c7b37b464f4` |
| `skills/project-delivery-plan/references/task-map-contract.md` | R | `0o644` / `100644` | 3820 | `390c85a439d334783e05685584937d64b4098e6d8258f0f967d4f4a80b29effc` | `743cb76bdca8cad2c5d096b2aa8210ff3f086836` |
| `skills/project-delivery-plan/scripts/validate_task_map.py` | R | `0o755` / `100755` | 10668 | `9197993b30294d9b319270ea72918ed7de3ff52242f542ec2a021adcb1c8d50e` | `19992fea8a6b0bba6627dd5d2f3384d73b3df697` |
| `skills/project-direction/SKILL.md` | R | `0o644` / `100644` | 7936 | `37d3dcbbdd554fa892486663d0a5b7dbc0ca438faeddfc6ed7f15bc8dd108d55` | `e0e8feb3db515140aaa2935d0b1abda69dd0104d` |
| `skills/project-direction/evals/evals.json` | R | `0o644` / `100644` | 4043 | `3eb304b4dfaf38753622403ccbdb5c3e1606c6edceb4845507c6428717da0a10` | `9ec9378c507ad332ff0fa858f651c4cf168c8844` |
| `skills/project-direction/evals/files/setup_fixture.py` | R | `0o644` / `100644` | 5940 | `ca9a9ccf557d2b294ec22df1d3a681c97199d25b1592c4beb158ab06dee9590b` | `0268a89cb07f72c842771f9d1fef24e8434133be` |
| `skills/project-direction/references/direction-template.md` | R | `0o644` / `100644` | 3765 | `c24e84d2f3663bae45bf0b9dcccd53f1fb1465f9ea137755c77ac495212cad5d` | `e04a803becbfc90b27f8703b57a12894a5f2072e` |
| `skills/project-plan-verification/SKILL.md` | R | `0o644` / `100644` | 14058 | `8f7100d365ff4ae61a4936917e1c9279ea515d0844cadde8d0232fa63b05c4f4` | `6168bf455430c0c7bd6a0aa2c3f5576f531b0299` |
| `skills/project-plan-verification/evals/evals.json` | R | `0o644` / `100644` | 1577 | `96e612fd7597dda0ea64a624b2c4166b67227118b85c9c8f03654b51527ca0f9` | `c9494bdafe7b98e4b07f72ba40f90eb7aa214388` |
| `skills/project-plan-verification/references/plan-verification-report-template.md` | R | `0o644` / `100644` | 2349 | `a99edffaaaa97e670c77f17fc9b9ce8b331dc4d63b74d5fc977662a3f9da0a8b` | `2dc047e1d1a626cacc0b271b921e9f26e799136d` |
| `skills/project-plan-verification/references/review-checklist.md` | R | `0o644` / `100644` | 2270 | `001171e14aebc28f3948ac2f77154f2032787df7fa6018c4039bc1152fb7e92f` | `b53d50a0eef02b407c03b0741125e3af9df6d4db` |
| `skills/project-plan-verification/scripts/verify_plan_artifacts.py` | R | `0o755` / `100755` | 7538 | `9623b17eafadb68b41dc1647d0aca09b6327b049e2c5d3a9a1250dd883bb13a8` | `c151d93a84c2315655b8158e824dbc8573c17cbf` |
| `skills/repo-foundation/SKILL.md` | R | `0o644` / `100644` | 20419 | `f9f215c02b85ca0898c7f501ce705092b58f45c64b738b08f6318f147c85736c` | `c6b37f4bab27e705910898b8a4843913d9b7a229` |
| `skills/repo-foundation/references/contract-index.schema.json` | R | `0o644` / `100644` | 1144 | `20909763d0dd62ca41a5c501cf08c1b1f2858427beeb47a829c91daaf94df846` | `a1917502894744c75f156fd8f9745f5c2a46cd74` |
| `skills/repo-foundation/references/contract-registry.md` | R | `0o644` / `100644` | 4071 | `e3de6c72ae09b3344a486bcea27b0a41542e5034c5d6bac69c21b66ec8939c31` | `da9f84777084f1308baf8d892a47aa55c40927fa` |
| `skills/repo-foundation/references/subsystem-contract.schema.json` | R | `0o644` / `100644` | 2451 | `c7b243da6f3772f9fe1b3e5e03180c3ff271beee0a2990f634c66b5ad207ac6d` | `b9d71e1d270547e23498c3ab0d4e306bdc642bf2` |
| `skills/repo-foundation/scripts/check_contracts.py` | R | `0o755` / `100755` | 11039 | `00f38e439f5347804a1c78646ecf9bf8b9fba805cfbb88075226b447d987b928` | `e41fe59d79a45779ec4cdd9fc49c5f33b2dd196c` |
| `skills/senior-code-review/SKILL.md` | R | `0o644` / `100644` | 9387 | `9974ca642d3c562eef36ce085f5d07127b7fa902acf2f1d27764988293ced85d` | `b7dc897216d86bb791e1f7f0e332e88190a6d76c` |
| `skills/senior-code-review/evals/evals.json` | R | `0o644` / `100644` | 3470 | `75bda6a247ef9d5dc26089e9ad185156cb836a215abbeec38e827133c749e459` | `2c73187bc40d76549f3b3e48ec0e8f4ea79dc39c` |
| `skills/senior-code-review/evals/files/go-inventory-reservation.diff` | R | `0o644` / `100644` | 1288 | `ee4a0d78aae32dd21fc35f718156fc8d9c7d91220f08938f169818fbafb7eae1` | `2ec68258340049ffbe6368f7d99da772398bb858` |
| `skills/senior-code-review/evals/files/python-payment-status.diff` | R | `0o644` / `100644` | 1661 | `f24bce7d25a429194057fce0c393ed986f81f4b07eae4fbf3e75899f857206b5` | `395952f2b0d64d173fa5c0501a9a72a12af153b5` |
| `skills/senior-code-review/evals/files/typescript-account-email.diff` | R | `0o644` / `100644` | 1294 | `43702ff285594a3698c0d44f0d253ec63e4bd408fd1a2221f53d4db0619e6923` | `dff21eeec55a95a1c0137b756b4f0ec9fe9d08ee` |
| `skills/senior-code-review/references/review-dimensions.md` | R | `0o644` / `100644` | 6399 | `b79f2118e427c42129c6830f0bf4dc8bdf389b52b2aed9a3cc685527fb91e442` | `733898a8efce331d64c65d639d6ca161222007b6` |
| `skills/session-handoff/SKILL.md` | R | `0o644` / `100644` | 8307 | `eea77fa4f445c545cef8847452fc583aeb5221ea24ae991c2e69d52406057516` | `975a3a653522a691e20360f9da4e552fd8a9dd37` |
| `skills/session-handoff/evals/evals.json` | R | `0o644` / `100644` | 3629 | `cf5a61610ce35cb0e2f3e6ccf9945633f264d1900a711802b35a8f0cb9d624aa` | `d4d47a71fd578b2f7c96956806efd31aacad55ed` |
| `skills/skill-creator/LICENSE.txt` | R | `0o644` / `100644` | 11345 | `bc6b3af2f331cbc7fb0da1344efb2cbe5877a31498b4d70dbc7000f3405a1362` | `4f881c52d1f72f4cfb720e339e2d35c3058d01a9` |
| `skills/skill-creator/SKILL.md` | R | `0o644` / `100644` | 34440 | `949b7cc1a614a44bdcd0d143314e3923c630c5cd51378d4a1bbce91684318ac6` | `251d13a0ba09dfdab896ab3113e4e10e08aeb762` |
| `skills/skill-creator/agents/analyzer.md` | R | `0o644` / `100644` | 10376 | `bf68f4cac5a56c673a928c2e6d619586c5b93ea364026ab37547772cb45a663a` | `14e41d6068635f4dd3fb878fd1626312395dda63` |
| `skills/skill-creator/agents/comparator.md` | R | `0o644` / `100644` | 7287 | `fe1fc9787c495d864c5d6eada47396478572325fde1b33a96d78bf4b849b7a3e` | `80e00eb45db3ee53a132fc2ba97fd59a7339e563` |
| `skills/skill-creator/agents/grader.md` | R | `0o644` / `100644` | 9049 | `57134da0c1a4eea33fbd74a1c9c44aa814f07d6bc64de303edb586f941e5d21a` | `558ab05c0a9a8bb062ef4c51823d4d76c3acf7c4` |
| `skills/skill-creator/assets/eval_review.html` | R | `0o644` / `100644` | 7058 | `ce477dcc74dc1c0d1d3352646a79167b5a63634e936b1019160025065974e452` | `938ff32aed9bffabf723bd5492d720f4736c8e4d` |
| `skills/skill-creator/docs/codex-behavioral-eval-runner-future-work.md` | R | `0o644` / `100644` | 7834 | `719241edcb63e253936956c84b91f0a6ef65e256f7f7c03126c82bf518611923` | `79b9af05a822230d77fde850d6b7fd27e261a2cf` |
| `skills/skill-creator/docs/history/IMPLEMENTATION-BRIEF-codex-behavioral-eval-runner-mvp.md` | R | `0o644` / `100644` | 12081 | `b980eb7d87bf36b7136598e4bb1929df4501158997811ae27687125f942dbee1` | `9958fc92f2ac906af8ef52779a9c52a13583bfeb` |
| `skills/skill-creator/eval-viewer/generate_review.py` | R | `0o644` / `100644` | 16365 | `fc9d1b9243fe5ab6012ebd579bd76d0035de1b79fd3b969de114defab26478fb` | `7fa5978631fed1ed545591dbb2b0eb21ce3f3d08` |
| `skills/skill-creator/eval-viewer/viewer.html` | R | `0o644` / `100644` | 44998 | `a53213426ee1100441d701a3a0d49cda7a842f992d2c36463f4d3cc0258575fa` | `6d8e96348a02e66c3363d2ff3b3ae58ac11e6382` |
| `skills/skill-creator/references/schemas.md` | R | `0o644` / `100644` | 12996 | `b868d48f33dba6049870d1e2206d6dace266affb1e1a686c72d56613fd835aa8` | `9e43f2bc8834fd7fc52896fbdf4d6cf45729c782` |
| `skills/skill-creator/scripts/__init__.py` | R | `0o644` / `100644` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `skills/skill-creator/scripts/aggregate_benchmark.py` | R | `0o755` / `100755` | 14386 | `123ef128ea5ccc01a4b1ac212ef5567f21e9c13d3d240609780beeb3200c49aa` | `3e66e8c105be9bab9f0e9c61f0d1482619401580` |
| `skills/skill-creator/scripts/generate_report.py` | R | `0o755` / `100755` | 12847 | `13df7118a3c50c83c4c3250a606d5f2b20b25a3d44cbc392b3d669ec75281453` | `959e30a0014ec165c41a2bb7420b7dfe1416bbac` |
| `skills/skill-creator/scripts/improve_description.py` | R | `0o755` / `100755` | 11116 | `87d864570220b699fac52da309d2d6efdb060647bfebc74f768128e646accf80` | `06bcec76122446986e3610c20a39c466de36f495` |
| `skills/skill-creator/scripts/package_skill.py` | R | `0o755` / `100755` | 4234 | `1a33059b0db1ef73375d46d513e5ea81369d2e8838c970597b0d52ddef8d1c0f` | `f48eac444656ddc41204aac1760a217951ce609e` |
| `skills/skill-creator/scripts/quick_validate.py` | R | `0o755` / `100755` | 3972 | `67cf5703402013936c8fb75ad6a1afecd8841d45cc5e606b634eb05825fde365` | `ed8e1dddce77b16af13c6f36b3fe86c4ac7c590c` |
| `skills/skill-creator/scripts/run_behavior_evals.py` | R | `0o644` / `100644` | 12668 | `b8e478500c89fe531d51ed76606dabcb5fbe4c409013c257d9e7124b8a25bc18` | `a8380df3600db74baf7d2aa661035854c10612ca` |
| `skills/skill-creator/scripts/run_eval.py` | R | `0o755` / `100755` | 11464 | `43e3b8f80dbf69c343967ba77e268fae991d9fa3ed68b32a0ff02532cd48657f` | `e58c70bea39d5b252a1e819f242bbdcdf20e8b87` |
| `skills/skill-creator/scripts/run_loop.py` | R | `0o755` / `100755` | 13605 | `7bd6f674203168520517eec94c55f493c0d154339b061b4d7c0f0dad187d0f21` | `30a263d674ef19de11c756d6f7537f91a421909e` |
| `skills/skill-creator/scripts/utils.py` | R | `0o644` / `100644` | 1661 | `3af8ae62c40c73ab712207436a0d9a981e845f25c5a7040229eb189cc8e45bb1` | `51b6a07dd57174197a937034b7eecebd5768ff8a` |
| `skills/skill-creator/tests/test_run_behavior_evals.py` | R | `0o644` / `100644` | 14959 | `f3a3f0ba665d855434101cdee0860f949778f26c6e98b3057f0aefb76a8332fe` | `f4ce60a851bb78bdc191fb31161668323c4623f7` |
| `skills/task-implementation-flow/README.md` | R | `0o644` / `100644` | 34146 | `fa77bb70e2329ccb65f96b319b0f079862fed3975237271984f42740ba84aeec` | `edbb289f1bf5acd0b7a533cda38afd7ac2dcb219` |
| `skills/task-implementation-flow/bounded-task-implementer/SKILL.md` | R | `0o644` / `100644` | 32967 | `b7d54caf420cd17a99f9f872a531d43c9458fff6d1df0fa8d5225382416bbd8a` | `eac807fc776204f5b08bf17194c1d476e4bc5fd3` |
| `skills/task-implementation-flow/bounded-task-implementer/evals/evals.json` | R | `0o644` / `100644` | 18415 | `c39b31b8c4a492dcaf6bb3d5efb78593b74987ffa8512ac1e0ac0d51a911cc21` | `f2d1e5f72c783b4089c2bcf061ea520a1e7af285` |
| `skills/task-implementation-flow/bounded-task-implementer/evals/files/setup_fixture.py` | R | `0o644` / `100644` | 65968 | `eb1a52a7f9256fd84f7a1b1034c5cd450416a3712f9dc366380d8eb6c54753f4` | `77bca8bb765f473418d7b9f0ffaaaf2eb041de3d` |
| `skills/task-implementation-flow/docs/evaluations/EVALUATION-2026-07-21.md` | R | `0o644` / `100644` | 39237 | `c7fe5855c46d7b50f5a91a680da289681305cfbe04c6621d87d79a9aa7e64ee6` | `e96690c6d5c46780fb8d3dc469db4adfdc1d2273` |
| `skills/task-implementation-flow/docs/evaluations/GLOBAL-DECISIONS-task-implementation-flow.md` | R | `0o644` / `100644` | 18654 | `2bc7da7ef476328925bf4ba87bb212af065e094fa1edc6c8b463b4c4ad8d6b7d` | `81fddf5785d99ca346fe40ef63000ef541284473` |
| `skills/task-implementation-flow/docs/evaluations/IMPLEMENTATION-BRIEF-bounded-task-implementer.md` | R | `0o644` / `100644` | 15419 | `46709dd13a3828bd5ae752289c2014d79f606dc11222e614ede8bd4ac6762ee8` | `080de287ede14df007e9c4f0b109697b82591470` |
| `skills/task-implementation-flow/docs/evaluations/IMPLEMENTATION-BRIEF-task-acceptance-review.md` | R | `0o644` / `100644` | 20109 | `761aeafa1c110f97c024e5a0c0ce8c8b2ccd5b7937f11b8b015bd6ffbb736ca1` | `1f5c52310167891044f2d45faa838c2d61685b4b` |
| `skills/task-implementation-flow/docs/evaluations/IMPLEMENTATION-BRIEF-task-brief-designer.md` | R | `0o644` / `100644` | 15531 | `0575e6fbbcc11641d341aa2f3d714c8a6621053d02ae77d93a6f1def759d9988` | `241fea8255f8f73ebabf866d87c6ae8ac7d123f9` |
| `skills/task-implementation-flow/docs/evaluations/IMPLEMENTATION-BRIEF-task-preflight.md` | R | `0o644` / `100644` | 13391 | `8c1ba82d856e01b44c7dde9938a6070f96d28e6a7150dfd83be5646881ade00a` | `290eb57454f3eb5a66440346fc49dfb1f1ed80e7` |
| `skills/task-implementation-flow/docs/standalone-policy-qualification-results-T-005.md` | R | `0o644` / `100644` | 10301 | `edea218c6e7fa2b2f638ffcd9a36e5780cb53dcdd7f7b7cb0d3dd8df4f7b380d` | `fa87c15183001484e7a424caa1947293cbc5ba4d` |
| `skills/task-implementation-flow/docs/task-decomposition-follow-up-2026-10-09.md` | R | `0o644` / `100644` | 13047 | `07a4ae5a7db55199535937505faac86aba519908180d64c6089363470604c178` | `54ce6d679ea6c3b11c6a32f85cc544ee2697e75f` |
| `skills/task-implementation-flow/docs/verification-and-review-policy-plan-2026-10-08.md` | R | `0o644` / `100644` | 19289 | `5c2802017978f8509e78277c82be48c275c5b6663fbbef8079c9374b74c8e233` | `2396e4b780e24aa1e3eac4c5f90c334848d8283c` |
| `skills/task-implementation-flow/task-acceptance-review/SKILL.md` | R | `0o644` / `100644` | 30281 | `2c12b30de78b3617759e5bdad55b089d3044ac8ebd1945ff32d150a7714fd04b` | `d7bbda65a6c8a2a0ee3807f84fe6f1005e5962e1` |
| `skills/task-implementation-flow/task-acceptance-review/evals/evals.json` | R | `0o644` / `100644` | 56732 | `d563afe9cd7db881a8caae86d8473c859c7c93ca8c484c223669427f2707651c` | `d7f26884caeee13f405e7bdb100970d07ee1145c` |
| `skills/task-implementation-flow/task-acceptance-review/evals/files/setup_fixture.py` | R | `0o644` / `100644` | 126294 | `7299b8df33bac41317a7b7204c40e8b074ace1a7d09464b2ce4005d9726e4ef0` | `1d05cb0b6bf175dfd8a348613dea1b3ba01dd475` |
| `skills/task-implementation-flow/task-acceptance-review/references/acceptance-report-template.md` | R | `0o644` / `100644` | 14135 | `82d22bc6607b2730f5b171403e17dfeb247d27fb0fde6986fdf4b0868b6dd580` | `05c490af58cc4252bdf1adc9e2f9b48ded7a92ee` |
| `skills/task-implementation-flow/task-acceptance-review/references/tests-only-reproducer.md` | R | `0o644` / `100644` | 2932 | `e74b95d43c8d6123c7d95e64556db88ac21df5e21f5dac0b3949c8589b0d6276` | `8d5744712bc5fac7a533c4d6febca3223564ff2f` |
| `skills/task-implementation-flow/task-brief-designer/SKILL.md` | R | `0o644` / `100644` | 28731 | `40c3cd2c28a9499931a018fbb94a3ead1df503268f3660bf7e61fd097129ceba` | `86a486563c81543cdf2b569407ac4746e682f83f` |
| `skills/task-implementation-flow/task-brief-designer/evals/evals.json` | R | `0o644` / `100644` | 24913 | `ea3e6657def9279a6083d1740f0da610be814da5d9ba9a71e21b7d01c2a41310` | `794f98bb0006c3af1d52ad0e6fa3f5c1da16ddea` |
| `skills/task-implementation-flow/task-brief-designer/evals/files/setup_fixture.py` | R | `0o644` / `100644` | 17364 | `09391b99e5320b8f45d4ffebdc3aedf38b42f54a4069a7fa327a9168ecf55b32` | `de814635aa97ef7202395544ff06bec1e14a5452` |
| `skills/task-implementation-flow/task-brief-designer/references/task-artifact-layout.md` | R | `0o644` / `100644` | 5388 | `6cc29bbfbecdebf835bce4605a8a4d66fd4f4ea675bdfde30ab30e02534a87a2` | `849783e6b3a33411ea588ebd45fc9b5465c1ca0b` |
| `skills/task-implementation-flow/task-brief-designer/references/task-brief-template.md` | R | `0o644` / `100644` | 13362 | `92d0c95f53fcf50b389f5171c6b30649f94a2b97a87750f94593dfa61af237a7` | `7a5f47e040cfd2f143d6f1fe1967dc3eb8d573f9` |
| `skills/task-implementation-flow/task-brief-designer/references/task-sizing.yaml` | R | `0o644` / `100644` | 703 | `832e48267d8579a5183f4c7543dae2eea06bc44b65cce7b3bce15c917b917b7c` | `d5e0774afa47f947dfe536f17d56676321e3420c` |
| `skills/task-implementation-flow/task-brief-designer/tests/test_package_resources.py` | R | `0o644` / `100644` | 2469 | `0b4fd5fe47ae9a36df43d4c027d02cc5106e24087c92e01688fccc64c7e0987c` | `22acb8bdecf4818bab136e7f0de7ee450bbb90e0` |
| `skills/task-implementation-flow/task-contract-registry-updater/SKILL.md` | R | `0o644` / `100644` | 6998 | `2cf8535599465000056d7ce8145febd81d52a1a3d0b300b4651a9ff4460f2cf9` | `75c58c6d0888bbaa578c4da98ce3c0cacf1469d2` |
| `skills/task-implementation-flow/task-maintainability-review/SKILL.md` | R | `0o644` / `100644` | 21199 | `94021a76438f20800ce49db9c54c08cfb6c734daffc981844a57157dbc3b40d0` | `23c1ae0d3bcde15a8e9c1337b2ec84fa86aded9d` |
| `skills/task-implementation-flow/task-maintainability-review/evals/evals.json` | R | `0o644` / `100644` | 10623 | `947b0bd8c111c82c107db7cc1d7314e0d914f04c54b0295a5b187240cf184604` | `cd074d87beacdbba6f8b77a360d2879002c73fd9` |
| `skills/task-implementation-flow/task-maintainability-review/evals/files/setup_fixture.py` | R | `0o644` / `100644` | 25313 | `ab6e30ce9c4ea2f4651025e1fe8ca3b09520165b6abe28ea66443306096567bd` | `8314bb0d6615c2110197d171aa472b07bb8a99e5` |
| `skills/task-implementation-flow/task-preflight/SKILL.md` | R | `0o644` / `100644` | 17097 | `505a75b34979ca8e4cceaa774bdf6ce455ad424a371483f36beacfba604cc6e3` | `91d71a2e9fc326d78b682446de564f6accda22d3` |
| `skills/task-implementation-flow/task-preflight/evals/evals.json` | R | `0o644` / `100644` | 20167 | `eb577c81e2bd5ac252c56deedfd147684bb6308b73c3b8a87869a35d6ea93097` | `083433328357742f573faf0a4a21f7fe7c62a9c0` |
| `skills/task-implementation-flow/task-preflight/evals/files/setup_fixture.py` | R | `0o644` / `100644` | 25227 | `5f75155ed1e03fc88620fe7fdde35689fcd14aef726c96c9ced0a431c9343756` | `c7cc2eeb2b8b0dabfdd0f1c25df3cf869a83fc24` |
| `skills/task-implementation-flow/task-preflight/references/execution-packet-template.md` | R | `0o644` / `100644` | 6449 | `3a00012e9e1678203953f496beb209b8b7adc98eea78564d5833a1fc3f63f21b` | `7983b91d7e3956eb101c93987b44ee9fbdee0f2c` |
| `skills/task-implementation-flow/task-review-discovery/SKILL.md` | R | `0o644` / `100644` | 16195 | `200e789cffdf1f72fe5b3ecf2aab6688e587674f137542fe3f80805cd09ba910` | `007102f58db6ca9c5eccd710adf2aa58d454e3a9` |
| `skills/task-implementation-flow/task-review-discovery/evals/evals.json` | R | `0o644` / `100644` | 33855 | `27b05cab827331e3613a956878d4b9004f5eb8424eeb80bfb19c5679ea662a1a` | `63ce1c7eb2843cdf417d5beac72a6f277cbb4672` |
| `skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py` | R | `0o644` / `100644` | 55525 | `e80a210ac9602cf8f3c03960873aa23a00cc2289c36efd660c2616ab37f44c37` | `93831016d67ae49a0e006f151cf675d4a0a9fda8` |
| `skills/task-implementation-flow/task-review-discovery/references/discovery-report-template.md` | R | `0o644` / `100644` | 10007 | `bcd0db3b8e8d59cf145ae2e430b70cf67c218e3a2d44bca368d50864b6015605` | `5013239cc202d9c83f82b60030e236e66d4a0b8d` |
| `skills/task-implementation-flow/task-verification-designer/SKILL.md` | R | `0o644` / `100644` | 12949 | `b3d911b75c8b5c9481c7d77922ae2b3a88e31f2228f31c488f76bce24aebde0c` | `72c9fa4aa9422940be8b479ad33d11055666b997` |
| `skills/task-implementation-flow/task-verification-designer/evals/evals.json` | R | `0o644` / `100644` | 11784 | `2ac399c2e83892d83b004673a4fb6681c0f075cee62d79da4ef8deda8cd3eca1` | `a84aedd7bf791aac7f50bd6304079a101a320213` |
| `skills/task-implementation-flow/task-verification-designer/evals/files/setup_fixture.py` | R | `0o644` / `100644` | 12406 | `3383feb64e32b934271b6099d6c0d7321384d49f8284c6957a17a7d7b64da3e3` | `5c9175039fa8b9dfd4cfe0619c03f738455ff5b5` |
| `skills/task-orchestrator/SKILL.md` | R | `0o644` / `100644` | 7160 | `411565f1d5560aa11654a90ad2f2b9ff33f8d5b9165ab8d0406a3414d4cdc55b` | `6fca8407c73b189115682667b74ad90f2230f72a` |
| `skills/task-orchestrator/assets/examples/fast-local-flow.json` | R | `0o644` / `100644` | 850 | `4c0f7e1caf612419b817521c3811b924280245528f4c2b2a6e118bab365a8984` | `a9a7240963c7430ddbfa21e75c5a4b2947076fca` |
| `skills/task-orchestrator/assets/examples/minimal-run-policy.json` | R | `0o644` / `100644` | 2038 | `039bd87fbe6df6ac07390a42c63142b6be64d0db50c8b4bb12712321a95a9447` | `1a69eb0e43ec4a6e2fe53498d6bd89c94ae4e060` |
| `skills/task-orchestrator/assets/examples/minimal-task-manifest.json` | R | `0o644` / `100644` | 414 | `e91bd5f8d80a8b7cf48cdd5954b42e46c43014063671dfcd2e286119c06e1c3e` | `331ddaa34c137f3758e23ed11d8ff462ebec3a50` |
| `skills/task-orchestrator/assets/examples/reviewed-flow.json` | R | `0o644` / `100644` | 1018 | `f3d6b74ccedeeb62cdaf8aca3e8cb55cdb3dcd9075eba7c8b238ea416bb116b0` | `34b8d6c4103e18336dca0d7366541e36129c4887` |
| `skills/task-orchestrator/assets/examples/strong-local-flow.json` | R | `0o644` / `100644` | 1064 | `0418c45e7a6f8d14cf89cf18db30f268aa601cab4310f4430eeabaab0ba2606c` | `549182384874305a4f4ee59c2b18bceec3c7e03f` |
| `skills/task-orchestrator/assets/flow-profile.schema.json` | R | `0o644` / `100644` | 3288 | `6c3c0f3e1c3ab05203a02b4c57adcaa81a6cf83ce0a73e3725b76ebc28f621d5` | `8a331640e0fe5b21679fc619e22bbd62245dbb0e` |
| `skills/task-orchestrator/assets/handoff.schema.json` | R | `0o644` / `100644` | 1865 | `9e2bf070bd480b1ba75a18ccaceb2c851b23b3a04f6b4441e9004ed31d022829` | `f2342dc5d49e8076f876066dcc0e6d96cb41007b` |
| `skills/task-orchestrator/assets/run-policy.schema.json` | R | `0o644` / `100644` | 3334 | `be68d79efc8147549dbebb19ec762069312e302113c61f1347b6e0204b4b6837` | `e8f6817f58e0a632099a6ab323277267b6df1ec3` |
| `skills/task-orchestrator/assets/step-outcome.schema.json` | R | `0o644` / `100644` | 1323 | `698e4ff1a7067ae757f12fed19d78591b1205f9df30f63fdcdc26a4f36b9f17d` | `cc410f962a6d3af014ee2331a06986f941b8392c` |
| `skills/task-orchestrator/assets/task-manifest.schema.json` | R | `0o644` / `100644` | 1525 | `72fe5dd9612aec182f376da4f4f1807c123436780202efc2394ef488f00fd78b` | `b5c0e937159527eec19bfc7702bd08006bfa30b5` |
| `skills/task-orchestrator/assets/worker-result.schema.json` | R | `0o644` / `100644` | 1956 | `32effc1988202bb7b16280169c4914b7300d6632d22ac805827b517675fec9ac` | `b0c6f2120fe38c7232cdc8a9a20a4c42b06020e4` |
| `skills/task-orchestrator/docs/code-guided-orchestration.brief.md` | R | `0o644` / `100644` | 26877 | `3079de7c8e572f6db317d4e03bae36e0fe59299132baec93ad2605772f82c116` | `38afd44a1a71dcd610fb0db821872ddfbcb90c66` |
| `skills/task-orchestrator/docs/controller-contract.md` | R | `0o644` / `100644` | 5749 | `ec62a8356d02d61e20d9b9a4c63f12ad441706e127cc48a68b02abbbff175214` | `f4db7474ce08de4e1dba1b190b1577630a0780c8` |
| `skills/task-orchestrator/docs/direction-revised.md` | R | `0o644` / `100644` | 11769 | `33952de9ee979886ac55694adc7db722944a31eaf8aa0a1e8994d22dea33fdb0` | `55246f47a331b48ef7e88964fd146f4c2da551c2` |
| `skills/task-orchestrator/docs/direction.md` | R | `0o644` / `100644` | 15463 | `d361fb51bc41813b2893965172cc97892de3221b58b81cb05ac360eeab3be332` | `89502aa473370089f633a064fc5a8fffbe5a7612` |
| `skills/task-orchestrator/docs/execution-brief-pilot-measurement.md` | R | `0o644` / `100644` | 2520 | `fbe9c4cf9f03ee6a4c9fcc498c171a4c237a32451f9f58ee632a6c9dfaa8bb12` | `99ebd02e82966eccd792de8e41b2b1dd545a8451` |
| `skills/task-orchestrator/docs/execution-brief-template.md` | R | `0o644` / `100644` | 2178 | `9931aed81796dbbc409d8786815748e2a26c22598c47c8d1cccc0a0cdb1275e5` | `c1967b84a58400af5bf1277fa0f093db2341e89a` |
| `skills/task-orchestrator/docs/history/stage-1-handoff.md` | R | `0o644` / `100644` | 4327 | `7a4b5ebc45701db94a19ad68d7e52bbcb089491bae4424d368c0da4986e06d63` | `e6192fc711ffcefa80062c9546ae5fb0b95f0998` |
| `skills/task-orchestrator/docs/history/stage-1-plan.md` | R | `0o644` / `100644` | 11641 | `3c9eb38fe8858d2e09b4d3b5eec68facf70bb8a08def4e3b51c4f5b90e22a34c` | `d9c786c898d32b6f5fdf1ade1618b344663e9b3b` |
| `skills/task-orchestrator/docs/history/stage-2-handoff.md` | R | `0o644` / `100644` | 6666 | `b7bbfc2616ece62c2ab5303c23f9b9154ac2381c09689f153bf2a873da686ca8` | `fc53068514d0b0700da91fa53285a32933dc8abf` |
| `skills/task-orchestrator/docs/history/stage-2-plan.md` | R | `0o644` / `100644` | 24341 | `69e889c7e562298e4eb4a1815e7fb66593ddb094d30399262d42b82523deadaa` | `6b7c5588730a75fcee44a401c97b766fba88587d` |
| `skills/task-orchestrator/docs/history/stage-2-unusual-path-correction-result.md` | R | `0o644` / `100644` | 2156 | `c0254d9b9d3340c8f5049dab13604426d46937e8d70dfa9e038a1481741a9af9` | `7c615a2da7d2e4a506587825ea75faa4fbeb0207` |
| `skills/task-orchestrator/docs/history/stage-3-mid-review.md` | R | `0o644` / `100644` | 8596 | `e6d2fcaaaa5a5f0bdbacd5e33412ce20ea07d03dee8b2ff67fbe57531f4e8f7b` | `2e38b5138d94496fcee62334510ca227e21538ab` |
| `skills/task-orchestrator/docs/history/stage-3-plan.md` | R | `0o644` / `100644` | 19450 | `8f30291bda35be1568dcc4f38efbfed70e3190b1bae1ddb7b5a3067166fd1d14` | `6020eb31ebd136cdd7ef2a63befc7f43d528cf5f` |
| `skills/task-orchestrator/docs/history/stage-3-tasks/S3-01-result.md` | R | `0o644` / `100644` | 2125 | `e91a984ac591e38e649e246d4ed40552f61499186f3a9b71680712fc26578354` | `316c820b4031e1710574b1eb9e8530ab22082d3a` |
| `skills/task-orchestrator/docs/history/stage-3-tasks/S3-01-verification-sandbox-proof.md` | R | `0o644` / `100644` | 5146 | `1f70f479bfc41d6582b62418306b1e838510cfde31a0d313101ce00813500d0a` | `f37ed981a4d23a03c03ff28947fba186d5d810df` |
| `skills/task-orchestrator/docs/history/stage-3-tasks/S3-02-extract-controller-state.md` | R | `0o644` / `100644` | 4785 | `0533562add297670bb84df7004bcf0974f0bafbfc6b3d39a9ade3164bb21d438` | `48bb2af19212689733a04ed088718695b898889a` |
| `skills/task-orchestrator/docs/history/stage-3-tasks/S3-02-result.md` | R | `0o644` / `100644` | 2845 | `6c075f1726ff200a6587f4e43ac6e618053dbad77b07bdf874bb194dc8a19cff` | `83c6b1168dd69bf2204c417ea166936c7a6517e6` |
| `skills/task-orchestrator/docs/history/stage-3-tasks/S3-03-extract-controller-git.md` | R | `0o644` / `100644` | 4745 | `3d4fef02cda3ec1bb9ec205a32e7d00e2ee56ca6f3b8f7daf75c96594d63c5e9` | `bf490e3a558aab4072172e2696041573d40c392f` |
| `skills/task-orchestrator/docs/history/stage-3-tasks/S3-03-result.md` | R | `0o644` / `100644` | 4100 | `6229c8f6868c2227c91e11d1e1bdaf372b64534771e4e6deae30d6a662e7e85c` | `6ddbca03bcd25cedbe3fe9460449d02b854de0e9` |
| `skills/task-orchestrator/docs/history/stage-3-tasks/S3-03A-correct-git-baseline-contract-handoff.md` | R | `0o644` / `100644` | 9815 | `399097fe38b58c4566b4268c295c0170da11de41d98091a8109d2dfa0b7527d5` | `2b4d5a8ce1beb67f0aaa94c285531d0e33d3603d` |
| `skills/task-orchestrator/docs/history/stage-3-tasks/S3-03A-result.md` | R | `0o644` / `100644` | 5736 | `213091a62662d75e4144c32c54c3f457c702b8ea5d7ff3626600ec4102e484b1` | `e81f4e5a4c6195dd34151754802b180a83822eb9` |
| `skills/task-orchestrator/docs/history/stage-3-tasks/S3-03B-repair-controller-git-boundary-handoff.md` | R | `0o644` / `100644` | 10020 | `a1af0fb53bd0030eec626d7483467aa38934bae2d560f63366d6698244c5ec77` | `f5f48859acd9c7df5a44a84f5c95d904f1afcb2a` |
| `skills/task-orchestrator/docs/history/stage-3-tasks/S3-03B-result.md` | R | `0o644` / `100644` | 6566 | `6a43b13a430ca52fec110994279de8763784ce61870369e947214e82640466ba` | `19d23d041c9edc7102793d2be29f87340fd0171e` |
| `skills/task-orchestrator/docs/history/stage-3-tasks/S3-04-acceptance-report.md` | R | `0o644` / `100644` | 19065 | `bd2300f35878f103570bf1cbec34e1a358e10acb4c87f20189ff49dbf1f3c955` | `b0f61850b0dbe9016adf000a90437177f9388e8a` |
| `skills/task-orchestrator/docs/history/stage-3-tasks/S3-04-result.md` | R | `0o644` / `100644` | 10374 | `a6a99c4ee93aace57ff18768060fa88affa9130cc62fb1111f14e9b38c47cd0d` | `7a20be38c9839d8fdbff5cd1300ccf685375b814` |
| `skills/task-orchestrator/docs/history/stage-3-tasks/S3-04-stage-3-state-model.md` | R | `0o644` / `100644` | 33767 | `c3be72f8e5198c7618b5665cf451f7e8f839a63fc24379eff3f42c857d52f7d1` | `dc518a8d0155687088a9aa711164eb1233769af1` |
| `skills/task-orchestrator/docs/history/stage-3-tasks/S3-04A-post-acceptance-git-identity.md` | R | `0o644` / `100644` | 21481 | `016e417945a3a191d69cda038cb39028b0bce52072ead7c6e51e92a61087cb1a` | `f95e64ee874fcdec9c9dd8f2305098a4a27a378b` |
| `skills/task-orchestrator/docs/history/stage-3-tasks/S3-04A-repair-state-coherence-handoff.md` | R | `0o644` / `100644` | 17838 | `6d1671dad694de63b5c980e0eed19c0f81827cc0f29a7dc88f3d73292052d4d7` | `efb24e62b6dcdf4959e9ef90fc1c5c0bf68d6020` |
| `skills/task-orchestrator/docs/history/stage-3-tasks/S3-04A-result.md` | R | `0o644` / `100644` | 5143 | `7ca66f84e0467b803682ebc0ef3b8128d36c02d81c935fa154a3cfc957403386` | `51dbb8519f67143c950a962423782166cd2686fb` |
| `skills/task-orchestrator/docs/history/stage-3-tasks/S3-05-record-and-identity-contracts.md` | R | `0o644` / `100644` | 6755 | `16a9428b45af132119bec3de0b5e4ad47e638820d8021217da2434c837cfa69f` | `7d1f70bd02f1a9588662de0ed277d5564bf45538` |
| `skills/task-orchestrator/docs/history/stage-3-tasks/S3-05-result.md` | R | `0o644` / `100644` | 4231 | `85aabfdc366616ad79128279d798ba9f22bad8b4742bc97dab5f9f00537c7877` | `aab1e35e803e6079cffaa12c71243a0111df9d46` |
| `skills/task-orchestrator/docs/history/stage-3-tasks/S3-06-result.md` | R | `0o644` / `100644` | 5220 | `1f3d94c6983f89b6c25e6d5e450d3840ef41b01355b471e01148eee2e0f5c637` | `54d82bc0c2e0db972b8c6d2e4f33c5d0d779810c` |
| `skills/task-orchestrator/docs/history/stage-3-tasks/S3-06-verification-command-plan.md` | R | `0o644` / `100644` | 6784 | `0e343b31e9e66d60aa9b3ac275fd58c7f8d93f248a8d32d60d80a33fa58f680a` | `cc1b59c199dd2c57b34b05aecac021cffdca85ad` |
| `skills/task-orchestrator/docs/history/stage-3-tasks/S3-07-result.md` | R | `0o644` / `100644` | 7153 | `5bb97ebc51b0a479ba53ec1d1022127f8d048cab58c41f684d987736e6116874` | `88c16547aa4d60d0145f29b95bc43172ab2ea17c` |
| `skills/task-orchestrator/docs/history/stage-3-tasks/S3-07-verification-executor.md` | R | `0o644` / `100644` | 6970 | `5df9a5ed6f9c35175979a83794396810a86a8951f60619e7dfc33559d7b0b353` | `64fce3987bc7ff750d17b74b9d504991be373ca6` |
| `skills/task-orchestrator/docs/history/stage-3-tasks/S3-08-inspect-and-decide.md` | R | `0o644` / `100644` | 9689 | `efa85666fd2bd54b0ff3ace7abaf242e84dbf6635f9f5ecae6363656f0c49074` | `21b41426ea04e0ffddc59752d88ca8294649807f` |
| `skills/task-orchestrator/docs/history/stage-3-tasks/S3-08-result.md` | R | `0o644` / `100644` | 10000 | `08ab2bdd31483e5a1c59793edc16b06b8e1f1c2bc250881d295e911dbdb22f41` | `c0c438fb5846b4387feca9d80607b4194cbcc58d` |
| `skills/task-orchestrator/docs/history/stage-3-tasks/S3-09-recover-running-and-stop.md` | R | `0o644` / `100644` | 3117 | `989c37fa7f295f1e9f4cd2121eb066c5b22634ccd964ae6d269702afbf29a880` | `821ce73d4780601fb6f50eddbae84e767e5d85aa` |
| `skills/task-orchestrator/docs/history/stage-3-tasks/S3-10-same-thread-resume.md` | R | `0o644` / `100644` | 2980 | `f4bb5516e8271b8f8575cd6954472ed113a0e49ffc22afa20d3eaff857f3ed8f` | `84c3992962359abc962f8f8fe1f24200ba4c320e` |
| `skills/task-orchestrator/docs/history/stage-3-tasks/S3-11-acceptance-operation.md` | R | `0o644` / `100644` | 3160 | `b694e3e4a3556b9b5549f3365ae8dcc5503a8c3a12ef28a949637d972bbfe84d` | `40760d4cd2aee42b5dcdb53f682760f540322e35` |
| `skills/task-orchestrator/docs/history/stage-3-tasks/S3-12-release-dependencies.md` | R | `0o644` / `100644` | 3150 | `0378b536897d0eb0920b26f0636644e46c891a5d5a7dd4d72e2867ca3e12ffd2` | `767afe9bca0dc14f77682b7e21e3bd1ce7812169` |
| `skills/task-orchestrator/docs/history/stage-3-tasks/S3-13-exact-path-commit.md` | R | `0o644` / `100644` | 3184 | `9ce399fb0261d37319775b2f75417f5de2f5359dd4b695bef1cfe65fff63a109` | `d3a864ad888c1ea0122cc27265c08c62c761a33b` |
| `skills/task-orchestrator/docs/history/stage-3-tasks/S3-13B-exact-commit-publication.md` | R | `0o644` / `100644` | 2629 | `9401d8958f10e8bf0bfd29aa91f7554c1842affab957f1bda06ba776b00e432a` | `9b9ef9c1474e644f32e8aa941b66d01c7b64c550` |
| `skills/task-orchestrator/docs/history/stage-3-tasks/S3-14-commit-finalization.md` | R | `0o644` / `100644` | 2903 | `8fb3c288eb374c6602f3f2cd70f39aa5cd375f945d13ad4f0e90a11ef2b804dd` | `a28f5d31e498dd44f395d875dac84f368c1b4bfe` |
| `skills/task-orchestrator/docs/history/stage-3-tasks/S3-15-finalization-recovery.md` | R | `0o644` / `100644` | 2944 | `45c1db3806b6581c7ef8981a9e9ed68f868afb59ede58a2e2fcb1100f471bd42` | `97d8d149c7a0f598d1760768f14b9d0585666405` |
| `skills/task-orchestrator/docs/history/stage-3-tasks/S3-16-stage-3-closure.md` | R | `0o644` / `100644` | 2700 | `58daf1d697c7664f9906887a2a3d647ef2539d91a7c4e1c2c4d195dd946bfd1e` | `3e75b0872af5c09c5d27e59a0a25ae530203a221` |
| `skills/task-orchestrator/docs/history/stage-3-tasks/S3-T1-human-tracker-contract.md` | R | `0o644` / `100644` | 2695 | `1133857661ce03d622720863ee004cb4f5d261cff8ab08d4b93dc62e3dfc9ab4` | `93e72a2a567746109730f634a4cae9fe06f7a5f1` |
| `skills/task-orchestrator/docs/history/stage-3-tasks/S3-T2-human-tracker-adapter.md` | R | `0o644` / `100644` | 2401 | `9b5cc962e1f682851a710e049c04b4edabb4b805d7c22cf1b0cb2774ae33bf94` | `0acc61c443dcf620a106d56afc3d57f88d9766a2` |
| `skills/task-orchestrator/docs/history/stage-3-tasks/S3-T3-human-tracker-finalization.md` | R | `0o644` / `100644` | 2628 | `cb029ab21cff30504b676cf04b56da07f6e4de70af713a2c015409b2faa19a17` | `8b2099a8f18976d8eda46434ecd33d30778b26db` |
| `skills/task-orchestrator/docs/history/stage-3-tasks/stage-3-first-three-task-review.md` | R | `0o644` / `100644` | 5590 | `7e553f5d815817de26e694251726fab11b2b3d508830873e333c1fb0fe4fb668` | `b2c1c2e680f8e86a8cbd44a868363837d29444f6` |
| `skills/task-orchestrator/docs/history/stage-3-tasks/stage-3-tasks-04-08-review.md` | R | `0o644` / `100644` | 8539 | `bc8616742ae033b58fbe5cc8dbec22c8273a165fa7db611a10584f5a7e0e60cf` | `a085eb241a163e290266f2c59a21cbef30808207` |
| `skills/task-orchestrator/docs/history/v1-agent-output.analysis.md` | R | `0o644` / `100644` | 16275 | `359f89db1eee8193f66ff12d01c65cb3d94947747717fe2c895ba758552b00bb` | `8f78dfeca330cb7156573430da454e4278f007bc` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/README.md` | R | `0o644` / `100644` | 8228 | `7452f3d98528e1ec17f089a6655fe6f65ea53c5c4a194af4479cb0319ee8a80b` | `1b312805257bd66fcc0ccbaf35223ee88cbb6400` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/audit_spike.py` | R | `0o644` / `100644` | 5061 | `9dd9244ab084d6c197a50f966c7a0bcd8ac098773f07e947c28037ba4da312ec` | `a1b0436257c3579dd386bc9ec9a1ad0181b4b3f0` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/acceptance.events.jsonl` | R | `0o644` / `100644` | 93010 | `f34c4c404eea22e3f6142af6ed08e98aedb8783eb613c92c59d70ad4814d0d4e` | `bcc4f029c01553db0f5d43c5fc34a1d1e2bf32ba` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/acceptance.last.txt` | R | `0o644` / `100644` | 270 | `2b60adb9b4f66dec100dacd64601de2c364afa0c4480f175ad91d9d3f4b2aa4a` | `824cb6d039a26c6bcf72e3f09a586b54d91de73f` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/acceptance.prompt.txt` | R | `0o644` / `100644` | 1010 | `245f3d04eb5644f486a490edbd6293af87234e3785fb5ea2397e545600b5a0b1` | `4889e2fca798f151bfbf4067c857571e8d39c90c` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/acceptance.stderr.txt` | R | `0o644` / `100644` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/audit.json` | R | `0o644` / `100644` | 19859 | `cae9386ab9b9894d6175ba1a71c77b1ec180eb9cf619fa2dd077a1f440aed3c7` | `2df260c7d7442def58acd1979909a78b69b9951c` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/brief.events.jsonl` | R | `0o644` / `100644` | 70811 | `c9b116fddf5ad6ded9ed28966f439e824b27580c8f970b562f28fefb87d5bd11` | `f0bc5b94dbe2c3b1eba4a9d99e3d7d55316bb4a4` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/brief.last.txt` | R | `0o644` / `100644` | 335 | `d517fcda001a3d057883889f05310e2d3e80f4d1fee93686757057c824d6e744` | `b69602a23c30750673c9c7968af6a9d0f890481f` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/brief.prompt.txt` | R | `0o644` / `100644` | 737 | `aec096f02aac1f0631efcb8d92d49c10c1e343c4bba0d7fe982a09f48da6cecc` | `f5be83a197dbad82b418e74fe8c061567e1d35c2` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/brief.stderr.txt` | R | `0o644` / `100644` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/controller-architecture.txt` | R | `0o644` / `100644` | 25 | `f3041ab31340bb721b117d18070acc616ad307e62e833fcd1c84c398d69e9648` | `a82640bf3038164780f572a8f94b14bf1eee5eda` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/controller-behavior.txt` | R | `0o644` / `100644` | 431 | `c5d399a97b5a6c22c28c31ba03c030974da56bd3dbf6e1fd6691af7c446e5a59` | `0bd1fac0701092f4c25a1dedfdf6ba672a72caf5` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/final-integrity.txt` | R | `0o644` / `100644` | 152 | `995c9b85470cf2320ea0fda7da325b8a3aa606c8f0d33b632c7e6103c8658d4e` | `17461895afa5230bdce7bcb189bcda8b0c543c33` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/fixture-baseline.patch` | R | `0o644` / `100644` | 2348 | `07c11f28efb3377f4f367020724f231a966b33fa0399cab1dca77c804252f74a` | `2b06695c5b942988c3e8e097bab3659a22fd506a` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/fixture/.gitignore` | R | `0o644` / `100644` | 34 | `2bd5696b90495524e4c39e2179e5752973ad72d00117817a0bd09184202c1eab` | `ea047af3bd3424a548e0cd27164717c992012174` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/fixture/AGENTS.md` | R | `0o644` / `100644` | 2038 | `57fd2c7dd428e2ba3672d1dee9a9726f933cd51b1a5f66da290f6eb90ff654b9` | `e1668fcdc5c3bd3a0852797d34a90aed5107e969` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/fixture/README.md` | R | `0o644` / `100644` | 292 | `2f6dd9fcc6b1e1e6f92aa6f1e0bc3ecc14c70c8d3d308980f6afa5a03a51ba5f` | `67e1b07d8bfe34ce0d2e46b0aeaf620af7ffe19f` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/fixture/authority.md` | R | `0o644` / `100644` | 1260 | `4fc7349de4fdcd14ca1b2795307f0bbea1e7620884e5ef988e331417a62c5df3` | `3ff34bcaab281507eead33abc560b72085975899` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/fixture/catalog.py` | R | `0o644` / `100644` | 185 | `5198cf2f936aa18774bfa800f2700d35e2ed35fcebe951b4802efb3a4244ba18` | `4f3a0a757dc62cc1fb1699910dbad52c6b15ac25` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/fixture/dependencies.json` | R | `0o644` / `100644` | 15 | `e51cca7a311dfb4b19dfbb483d04f09e19529d180ee7aec53427185e1c4818d8` | `e4935ef7188edf59ecac0d1c964a83b9e67ec282` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/fixture/docs/contracts/catalog.json` | R | `0o644` / `100644` | 511 | `2e1c297f6d7a351bc53a4fcb8cbafdd1da023b3c88343cb48fd2a5168f6a97f2` | `c9defeb3f43980d471a7fbbd608061b2fa026ffd` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/fixture/docs/contracts/index.json` | R | `0o644` / `100644` | 210 | `8ec4f6f31a3dfbef65e09fa1b44df1cdd7be883a14db82a0c1017445df8f106c` | `7e130c44035538041c2d41ad7223c82a37904022` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/fixture/docs/tasks/SYN-01/brief.md` | R | `0o644` / `100644` | 11558 | `83cd92efeb30639a5475430aba4477150a84b133b98525752b6df488a3ffeee9` | `ca01f2592fdf3748a9210e361958ea65105fe085` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/fixture/docs/tasks/SYN-01/preflight.md` | R | `0o644` / `100644` | 10581 | `a5d4a284458da72f751e033b4590d96ecbe834aac85ff13f2b428f9567c1fd8e` | `34291a6bd935db84b261197983ba4ff46545cab2` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/fixture/docs/tasks/SYN-01/reviews/.gitkeep` | R | `0o644` / `100644` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/fixture/docs/tasks/SYN-01/reviews/acceptance-01.md` | R | `0o644` / `100644` | 10448 | `b016e1f6aa90d0853b52935ffa33347071ef9a2cf0fc673657cd57d1bcbc58fa` | `6e2d9e1ded0525282543b342872a52cdcc9fd4e3` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/fixture/docs/tasks/SYN-01/reviews/maintainability-01.md` | R | `0o644` / `100644` | 840 | `c05000a090a4828ee788ba1fb57d1955858665505110e0438e41cf42b3ab60d4` | `14bff56db9d64d211f563c985277ca52a619b63c` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/fixture/docs/tasks/SYN-01/verification.md` | R | `0o644` / `100644` | 3460 | `e8f4727604fded0551956f4cae661cd9d1d36ae3b9ff595aadbda2672d0caa1a` | `a59e3da3cd7250181b64cfa56d6b08f97cd9644b` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/fixture/run-policy.json` | R | `0o644` / `100644` | 1259 | `82ad4578dce7ca9468a90276a1e29100417fb559c5d6eb38333c937d049baa20` | `8728a72271614e1881f256f13343209572c71888` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/fixture/tests/__init__.py` | R | `0o644` / `100644` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/fixture/tests/test_catalog.py` | R | `0o644` / `100644` | 720 | `d1a39536a3741982377a7f3a374c9fa9c11baebfed868b920e0efc1f1f6bb0d1` | `4c647278c7b6af53577a9b9678ee4f75ffa81f2b` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/fixture/tools/check_architecture.py` | R | `0o644` / `100644` | 244 | `cd468098acf799dbca5be2724a3924e25725ec77f5d2441ba1f05ff5a198250d` | `c67e13d6d9e51da8450a6c7e4f5367e1c1221c18` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/fixture/tools/check_contracts.py` | R | `0o755` / `100755` | 11039 | `00f38e439f5347804a1c78646ecf9bf8b9fba805cfbb88075226b447d987b928` | `e41fe59d79a45779ec4cdd9fc49c5f33b2dd196c` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/fixture/worker-result.schema.json` | R | `0o644` / `100644` | 1956 | `32effc1988202bb7b16280169c4914b7300d6632d22ac805827b517675fec9ac` | `b0c6f2120fe38c7232cdc8a9a20a4c42b06020e4` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/implementation.events.jsonl` | R | `0o644` / `100644` | 90264 | `c90d2db2cc32f28e2c05fffa30b2a7c70295a732c9ede03d45f5d07b8fea5508` | `7d93397abdbcec26f1a3d83062db605f39bf2a0f` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/implementation.last.txt` | R | `0o644` / `100644` | 1891 | `700d63c66ba0dfa8a0903af4e69df5e77b167337d427c31577c3a8ff583831e4` | `c993a88dec83f481623824e1cd58216036dccbf7` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/implementation.prompt.txt` | R | `0o644` / `100644` | 845 | `3f559514022c86029009c68bb57663bd1cd1d2336df4ae569b298a9d172246de` | `cf5b22fda099732cb97cb1833b4c5b3d30e2e659` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/implementation.stderr.txt` | R | `0o644` / `100644` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/installed-bundle.tar.gz` | R | `0o644` / `100644` | 208250 | `1533645b594a2f169494bb5d4a2d7befa94c8b49a72a5ebf17c2abbd0251b628` | `178120f41cf99ab77b50d34fa7327dcf6b6d8517` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/installed-manifest.json` | R | `0o644` / `100644` | 11045 | `12204d81b787d8ffd123775fedf0617e8b18036b1a7403825da2bfefff00f5d3` | `b50bb6bcbdeaf3316147d85635115c0ff34f7755` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/ledger.json` | R | `0o644` / `100644` | 192890 | `cb8efac36a85dce00f2cb865c1da247a41f57762c71e3cafe51d18a373bf54a2` | `e696965ac3017bbe897fba04d2dfbd5901130b71` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/maintainability.events.jsonl` | R | `0o644` / `100644` | 48065 | `c294cf5a69fe26fcb5e2bb6d919551ae671bbf59d09785130eb1bccfadeaa985` | `260e490b1a188364a7acd72747b081ecf3a84997` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/maintainability.last.txt` | R | `0o644` / `100644` | 263 | `ab53c84ad2429d2142c5534ac33c07a45fa14d4917f980cdcb13a9c3583e54bd` | `27390d96ac7b0bdfb071051481e6c2438132c938` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/maintainability.prompt.txt` | R | `0o644` / `100644` | 871 | `04263872b295fc5c694202669f86f23587f2e5792e0924b418474e7d6c8355ff` | `f3bf39b58996c6cac537b8982204a0eb523df282` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/maintainability.stderr.txt` | R | `0o644` / `100644` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/preflight.events.jsonl` | R | `0o644` / `100644` | 68949 | `0f348e7dfadfe959da4f3d6559fea0e57534208c4c139f3ed75bad78dcf9ada6` | `040299abe9cc511eca42c5b6035d3ed37871ca47` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/preflight.last.txt` | R | `0o644` / `100644` | 374 | `c28e17fa687776c2c96857bcd4a2d48deaf360a6ec080d3d9518de8c8152ef16` | `e5d8a998ea344097a37ec564ad5c20f1b68f0325` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/preflight.prompt.txt` | R | `0o644` / `100644` | 741 | `af17380efae30e5d6dd378faa80f85d59b775511beac01049c89e4b8d4b6f05e` | `cab180a47564dfee4156d463bae4b5724e695fa1` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/preflight.stderr.txt` | R | `0o644` / `100644` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/registry.events.jsonl` | R | `0o644` / `100644` | 77399 | `dfcf7e51c015c654c789bdfaeda84f951524b9f9ec321dcec7dec74e3a10a0fe` | `60c97d1ba23ec27ecc74c4b588249de63c39b1e7` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/registry.last.txt` | R | `0o644` / `100644` | 589 | `c7eb7c4c7da1918503f7eb5ff9b369ff75484973a4238fd055ba7abc94119b6e` | `5339a83a9b3a943943fcdf70901759aef1782fa0` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/registry.prompt.txt` | R | `0o644` / `100644` | 905 | `cf48bdf4c9f84fe03386ddf85a0f3cbbc7e60694dbe5c177f76795416b571b1f` | `fcf2688aa48084796ed166ae8f5e03718a755e3a` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/registry.stderr.txt` | R | `0o644` / `100644` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/setup-observations.txt` | R | `0o644` / `100644` | 654 | `ad1af32ccf5de83d4d5fb11f77773cc0e16b28147b26a3640843e69ec8ec0db6` | `f6b54898feee28486213a9437fb52ed825644ef2` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/telemetry-audit.json` | R | `0o644` / `100644` | 3666 | `110dd3fbe6681d8c9c0defb46ce61ee88255c4c1ea004ff3b50d350c6fe4358b` | `1b04aca84223315a9f4824034b389a5dcaeed222` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/telemetry-verification.txt` | R | `0o644` / `100644` | 148 | `e42271d23e4e008b17ef03873c4bd74713464b50fd18f549fbf8dbf286c4ab34` | `3593d418aa32b22ff1bae064a79d1838b768c2bb` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/transport-attempt-1/brief.events.jsonl` | R | `0o644` / `100644` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/transport-attempt-1/brief.prompt.txt` | R | `0o644` / `100644` | 729 | `be80edba6c2b1455bd3ef09fc5999e82fc850a69b93cab4e91ffa584f2400115` | `d7c1108aa36e3d05c98d4228c9b419bc8157e1db` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/transport-attempt-1/brief.stderr.txt` | R | `0o644` / `100644` | 199 | `2d8b902fb51c4fb0108c58a40b037f3ed52641f00cdae67901d7cbda9b4b8473` | `f3bc6933f0a368082712d8956331a63915934503` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/transport-attempt-1/ledger.json` | R | `0o644` / `100644` | 26688 | `616823c0516103c8bcea0effd6cd6ddf622f45020fffd9659dfee511592f234d` | `06f7eda19e885e808ae6f27bf4f50b8276e6237e` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/transport-attempt-2/brief.events.jsonl` | R | `0o644` / `100644` | 719 | `28cf80f7e91b5c21a026c82ac61b44095fff3b4cde790d6aa03f541b8473bb00` | `e99faee28dd7a3064aff8c6a03f3dd1216cd0412` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/transport-attempt-2/brief.prompt.txt` | R | `0o644` / `100644` | 729 | `be80edba6c2b1455bd3ef09fc5999e82fc850a69b93cab4e91ffa584f2400115` | `d7c1108aa36e3d05c98d4228c9b419bc8157e1db` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/transport-attempt-2/brief.stderr.txt` | R | `0o644` / `100644` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/transport-attempt-2/ledger.json` | R | `0o644` / `100644` | 26688 | `616823c0516103c8bcea0effd6cd6ddf622f45020fffd9659dfee511592f234d` | `06f7eda19e885e808ae6f27bf4f50b8276e6237e` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/verification.events.jsonl` | R | `0o644` / `100644` | 42011 | `8677ad2fbe8ddfc37da7b3189e19ece06e5945c0aa2108c3edb165505d16bc5d` | `f4a9afaa9359b4b79f0f3d83f6cfca4caaa9499e` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/verification.last.txt` | R | `0o644` / `100644` | 352 | `9226081b3beceb43b97a482b86165335c6e85c449b532394301409d4d046982e` | `4a9b78509f29c50dd8755415fa9f2acc3fb9a2fc` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/verification.prompt.txt` | R | `0o644` / `100644` | 577 | `4a0c75a17a3598a2a08da1e0dc8ba7e52200b84209044e076d62e95d6e7d61c9` | `1e116fb1649022feb18e1edbbaa696831e3acc5b` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/evidence/verification.stderr.txt` | R | `0o644` / `100644` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/integration-guidance.md` | R | `0o644` / `100644` | 9594 | `b7fa157646db52d242078ed31a813698f69c53e17fce956bf71479c2d1d5cfbf` | `ba41b4f51c73a42a078e5b754bc8529889c88ed5` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/issues.md` | R | `0o644` / `100644` | 12975 | `c42b5dc8841b79f6a753b73a0dcb3df6c9c31c96bcd44a03baea5b8981985f20` | `24a67d8954cca9d2a3d8756b2b6593014642db6d` |
| `skills/task-orchestrator/docs/integration-spike-2026-10-08/run_spike.py` | R | `0o644` / `100644` | 15762 | `6b4387d122a4469d979ca12a3fcb79800fa9afff8d62d4fe4e917ab628a3b701` | `8cd58920a6339125da584d9838370c158097e5b9` |
| `skills/task-orchestrator/docs/stage-3-mvp-rebaseline.md` | R | `0o644` / `100644` | 26595 | `f8ff9753e62f3da6fbfe41444b317bb8304d89f406e5116b62953104765d715e` | `730aa389c498eca160866eb7995f65ed756d173d` |
| `skills/task-orchestrator/docs/stage-3-mvp-task-actualization-map.md` | R | `0o644` / `100644` | 10023 | `763db20de3952771e917f73e4fc7842db3b6fe5573031f8e539c4da874c2a87e` | `27b8a1f607c91637adeba590c73bdbcc1aa8ffd3` |
| `skills/task-orchestrator/docs/stage-3-mvp-tasks/MVP-2-flow-contract.md` | R | `0o644` / `100644` | 20746 | `1e7778efbf319c68cb8a1120e682d49865ce67ada8088263d79d94842d11337b` | `450fbc7ce8911466421b379052f20850cc1281d1` |
| `skills/task-orchestrator/docs/stage-3-mvp-tasks/MVP-2-result.md` | R | `0o644` / `100644` | 12922 | `6c170ababae4cb1db1e4906cca5ef1e95854e0c7fa145a47cc1c530bf3d1ac41` | `6e3c5f7f43d6c43e5b22563ffc964eda55a30277` |
| `skills/task-orchestrator/docs/stage-3-retrieval-surface-follow-up.md` | R | `0o644` / `100644` | 2882 | `d59f78cb02b8aca7fba272bd16d6d825e4cb498e5c0b49ed26ad134c9230cede` | `bad634e0a661db43e1ff1e574f55b8ba5999b563` |
| `skills/task-orchestrator/docs/transport-decision.md` | R | `0o644` / `100644` | 2543 | `d68f081d91c7b29f59d6c28d94e87135de8b0ff87a3daed3ee41655f69eb964e` | `4a7bad39cb11fead105efa5e3819fc7771745f77` |
| `skills/task-orchestrator/docs/verification-sandbox-decision.md` | R | `0o644` / `100644` | 8004 | `a2e8b556ad9313979e302a94e12772f74c4768ffb01ed79f074c4866ebbc8e86` | `74be7842782b61b5bb8d6695536118c2c2242f6b` |
| `skills/task-orchestrator/evals/evals.json` | R | `0o644` / `100644` | 6164 | `d0f4a2ae20e795e6a23995966b5b5fdb5bee2bd6b4b3684d5bf0449856f11def` | `3c11caba7994063197fb4d73e3b511497fc9f175` |
| `skills/task-orchestrator/references/architecture-map.md` | R | `0o644` / `100644` | 2496 | `d40cae50571a8da9a9bc47e9ecc84b42e7b9de514accdd8d2bc783f269016dd3` | `0ad791429a7ccace7b72dfa4db47c8e6da9844fb` |
| `skills/task-orchestrator/references/index.md` | R | `0o644` / `100644` | 1467 | `c8b6a16e85af0382bf53d9265d1fb5ed9958336ed92206c4348350f5cbfbeff1` | `4e406d74db1a00e625c87c0efaccfe271c15ad58` |
| `skills/task-orchestrator/references/operator-guide.md` | R | `0o644` / `100644` | 3408 | `0cbb91b2fb80850a99b6ebe316678f6c11c6cc179acffbda15c57cd53aa361ef` | `a0501a2bad0b972ea74747c67126756b8cbe45f2` |
| `skills/task-orchestrator/scripts/codex_worker.py` | R | `0o644` / `100644` | 18265 | `001a2f5fbf78a0532d342f71e9f8467f1d35073f0133868503d6bb15e70f3ba2` | `db8cafd5f044a008c0fd6ba570d30d84cb79beb9` |
| `skills/task-orchestrator/scripts/controller.py` | R | `0o644` / `100644` | 80429 | `ccce1556fde615a2490ea1234fcab68dfeabb5c57f9c8c28a1ad00bdfec60b50` | `3c36e12f294b2273a1b7fb28e3d34e66e98f4498` |
| `skills/task-orchestrator/scripts/controller_git.py` | R | `0o644` / `100644` | 19596 | `49f8685c5a33850250f70587f111d84fba40c33412e9ad11c1590ab13a42c905` | `8d6c3a0dacce0ce80767143315e2004e68cd7bbc` |
| `skills/task-orchestrator/scripts/controller_state.py` | R | `0o644` / `100644` | 67056 | `b3ebc6c5244982b33cacf563b70d46c01336c4a476e46940d75ee595dca2bb02` | `03a233e9c0f581c0ff60665f89942589a7623481` |
| `skills/task-orchestrator/scripts/verification_runner.py` | R | `0o644` / `100644` | 33595 | `7cb7bfd633dbb346f2b96bc3cb191818ed160035cfc6d665037b9797c1baf66a` | `15a3f6e90fc8765132c25a2307c597a5bc291afd` |
| `skills/task-orchestrator/tests/test_codex_worker.py` | R | `0o644` / `100644` | 19172 | `30dabec6e379918c4f20bd00778997628c7363a16aecccbcc725606a50b7fdcd` | `0b43d717cefc31623604271e204c6c2dfb338d0f` |
| `skills/task-orchestrator/tests/test_controller.py` | R | `0o644` / `100644` | 132081 | `62440a5d6ea1e7b451c7afa6944f8cc279eae3124a89f8212e02cec6105ef833` | `30d888831971ff1f305783d94afd7a05452fb05f` |
| `skills/task-orchestrator/tests/test_controller_git.py` | R | `0o644` / `100644` | 30973 | `d2618265009e03b7f2deb14522b02cc04f9458ccb3014675b699feb0dc67cc3d` | `5dbd77d5e96a9330b6712a765dcc72d2935832e7` |
| `skills/task-orchestrator/tests/test_controller_state.py` | R | `0o644` / `100644` | 73977 | `70466c992ee63602a9968bc72530a1f2b03b9479e4e38d7fe623d92b7fc1c1c2` | `4f12f95da72d8ed2797ec51502fa25ea8df2d4a9` |
| `skills/task-orchestrator/tests/test_retrieval_surface.py` | R | `0o644` / `100644` | 4961 | `8fc05fafe77505b3c54f58a24bb0a3ffe0ea0141f42164a7bc2d2b1303a5d1d8` | `16f64e6e4ccdf215efb2176a058fd1bf32c8d558` |
| `skills/task-orchestrator/tests/test_verification_runner.py` | R | `0o644` / `100644` | 37619 | `eef2132f63adce69d2b2d721b409b986f3ae3b1331e775120ee021f26277bc2c` | `7f91a096cdc8cf0b95e86266666c262603b53ee4` |
| `skills/testing-discipline/SKILL.md` | R | `0o644` / `100644` | 16646 | `67a3cb0fd90496d3ab12623ecae1298566ff1933cf21e8f8d47d24680dd26e38` | `0071374309007a23516a7460276ab19013b75db4` |
| `skills/testing-discipline/agents/openai.yaml` | R | `0o644` / `100644` | 237 | `f728e83185815d87e3854a31eb2b25c51548b6abbd96831ada1ac0e56cc34348` | `bb8d981421f15bae0c78918856675601dd53f644` |
| `skills/testing-discipline/references/test-catalog.md` | R | `0o644` / `100644` | 13210 | `05b9b5369d90d45aee1f15bdb96ac2e5f1be24c4b796e2c2ef219ab851e49b9d` | `77c5ddd0219c687848ab6853205a009239ac1d5e` |
| `tests/README.md` | R | `0o644` / `100644` | 5822 | `6e8d22932631a39a688fec4158f0cce978efb343cbebc96bb03865ed7c8d0adc` | `409f107d5bbabc0798b0f5446122c0c9082030bf` |
| `tests/review_fixture_support.py` | R | `0o644` / `100644` | 2450 | `9a79bd1fd7b5a8a245220d4a0b028fedb4b7b5c601eb2c651632ed89daa15dfe` | `f30fa9406a14d6dee44fa4a0626eaf6d17a3e525` |
| `tests/staging_fixture_support.py` | R | `0o644` / `100644` | 1776 | `a068cfb000446d4766f897f8ebc799988021590d92c545b64441cbb771c1e418` | `dfa1a568baa2f1ba5e07cca0bd5bdb0641e9d558` |
| `tests/test_bounded_task_implementer.py` | R | `0o644` / `100644` | 40654 | `94fadfa2b3087ffec5d0b7ac5d15c0f34a2b72744ef4aec9de3ec98c2bf986c4` | `a4a8703b5e1aa33774fec63013412602ffcb9fe0` |
| `tests/test_contextual_export_risks.py` | R | `0o644` / `100644` | 6825 | `c459ccbd2b5b0215fb046159bf2a29053457dd86e9de6d9c29417a7b9a18cf55` | `6cdd4309c233aeec5c0aef25f92fc5c8a9027a0a` |
| `tests/test_contextual_known_issues.py` | R | `0o644` / `100644` | 12774 | `2058a99ad6766a35453664cb91338e81576d23c4a014bcb8cbed892ffbb52cdb` | `a64580fcd4aad8bc75fb60729f813a432149dbc1` |
| `tests/test_contextual_uncertainty_inputs.py` | R | `0o644` / `100644` | 8571 | `d1c0c5b6699bd91d1d23e64fd441b051659223e6b29b0077f035b6f610b10528` | `c9b09eed014868f2b251493e026cd08210881467` |
| `tests/test_install_development_skills.py` | R | `0o644` / `100644` | 90643 | `5eead744e1a7315082fb73f91a19b81488d7371bc867c792fc34e0144e7d082d` | `e99aed8ebdffabff2d2fac1d089e55a66fdf95f4` |
| `tests/test_ollama_delegate.py` | R | `0o644` / `100644` | 12155 | `0b6c97a96d122bde90a984d2b26aed47a8f112e21282bc2db9f2ded59347f41b` | `951736e156e67c230700cc570224018b85c7aaf6` |
| `tests/test_review_composition.py` | R | `0o644` / `100644` | 62996 | `9c8c4eeb0162148ca24e2f353bec2dab3a8b7f01d91b9009cea6f2c48ad9d0cb` | `173d3c292e811ec223a3c2d51925cb718fda12ab` |
| `tests/test_run_evidence.py` | R | `0o644` / `100644` | 21441 | `a969a2e4ead9f502dbefa00b1a2db5cc1e48d0b396164b7ea2b0268970e5a9ad` | `d524b0671be7c6fa6a41e260282ad38e6d55d635` |
| `tests/test_run_evidence_availability.py` | R | `0o644` / `100644` | 7811 | `9570e4e84bb049ee01ef572a94c842cd7d0a9682ecb4f4ba5bd2227a6baae9fc` | `981317852e10bf420841f49ae9bf05f6d00c2a4b` |
| `tests/test_runtime_context.py` | R | `0o644` / `100644` | 7685 | `93bfbeb69b3502b9787c2165a1ba91a6f6d37856d70ed5f68b2cf559e7fd34f1` | `1354c0353b312c1e97b1fba8718cc1491dc7f4a5` |
| `tests/test_senior_review_discipline.py` | R | `0o644` / `100644` | 1305 | `f15a2984f1ed248f6b46aa84f539d907fdfc94fe6d525c5d8c5eada952a556f8` | `76aa4747c593b0431f6acfd61bce3ff2036ac447` |
| `tests/test_task_acceptance_review.py` | R | `0o644` / `100644` | 26901 | `2d1d08a9d2b6e8a09129950c3ff8a11bcbc155a2df4cd4950bdd63ab573d32a6` | `1d2974511649d0c73e16cdb1f520ed861e121ad5` |
| `tests/test_task_flow_guides.py` | R | `0o644` / `100644` | 25009 | `86e7132472b2a2da79e6b66974cbf24089b4c29f15a89e79a5f9757ea15a2ead` | `70bd0a5a198d55e7c7f631530ea6c9f91c7ad4cf` |
| `tests/test_task_maintainability_review.py` | R | `0o644` / `100644` | 34387 | `3a25b02f74b28c7a7ecce6b6b3c5d07012bff68e3ec5b3f96c9a919570a9e5eb` | `05836b14510804f4a583cba82c991810a72914b9` |
| `tests/test_task_preflight.py` | R | `0o644` / `100644` | 14667 | `1b539cdd78ad803c0a2244212dca59db7b60ee0c9556c651089cbacd54a50696` | `9846043043f24acf0baba88468827bde719c17e6` |
| `tests/test_task_preparation_contracts.py` | R | `0o644` / `100644` | 18261 | `51e7bb7afd57d4acca11a70d6670d89222cc712ab67874a4ebb1c16ab8fd1f00` | `ea74fac268ad9ea5674e8ebe3f79e2a573f38c1b` |
| `tests/test_task_review_discovery.py` | R | `0o644` / `100644` | 24510 | `75f0ec7b5f2dba7ef2ca82fee61ae3ff78c52f49ccdf06fa0df56622f6b5aff8` | `eb94ce17a10cc4df25ec9676b7ea3ef214883b71` |
| `tests/test_workflow_version.py` | R | `0o644` / `100644` | 17683 | `12aa118eff331c003505a97a5e0af9a7b8fcba1d54d099e837b54d8e8c5330a2` | `dbc47d3280d10d46f69de16acc8560ba34474f16` |
