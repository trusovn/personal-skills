# Task Review Discovery Report: T-001 — revised-authority discovery

| Field | Value |
|---|---|
| Producing stage | `task-review-discovery`, project-local installation |
| Coverage completeness | Partial — current submission and ready preflight still bind revision 1; revision 2 has no corrected audit or refreshed preflight |
| Discovery iteration | Third independent discovery; first under verification revision 2 |
| Created at | 2026-10-14T16:20:46Z |
| Repository root | `/Users/mtrusov/work/skill-sources/personal-skills` |
| Durable report | `ideas/documentation-consolidation/tasks/T-001/reviews/discovery-03.md` |
| Authority | `../brief.md`; owner direction, cleanup plan and task map cited there |
| Preparation | `../verification.md` revision 2; `../preflight.md` still bound to revision 1 and old brief |
| Submission | `../results.md`, SHA-256 `798906e82414c4c25f16e994a508e63e4eef2806c067ea6953b02347b23407ee` |

This is evidence for a separate decision call, not an acceptance verdict, deferral or advancement. It applies only to the identified bytes. It does not review or authenticate itself.

## 1. Provenance and scope

This session authored no reviewed production, preparation or audit bytes. Its only repository write is this report. HEAD is `b65f900e7515ccfe36335b793b0c058b7b2bfa8c`. The audit output is an untracked task-owned addition. Two tracked preparation files, `brief.md` and `verification.md`, have unstaged user changes that revise authority. They are separable from the audit output; this review reads but does not claim ownership of them. `preflight.md` and the two earlier reports are existing context. There are no staged changes. No subagent, evidence lifecycle, network operation, consumer suite or fixture process was launched.

Current SHA-256 identities: brief `94cc2e185f1aef939a17d23db629cfef90bd33d6aca7727ad3de1ddaf65a2ebf`; verification `962a9b138d3491eff9ee4d6a372226af8cdbc9f7062d389308c1d8f699d616b1`; preflight `9d79cb44aa6d152536563a42928869a781bedd238277cabe48fd09615310612d`; prior discoveries `3d2ca9c430bf71c0dd521d42117a4ebdf54ece6d57c0b28983b5aa45e70d71c8` and `44375e4e35c126547d37b6050720f8af4574a0d9e30c27983b7eb8a1ba0f7337`. Brief and verification index blobs remain `bea1daa966eccbcfba28f346062a8b0dc2226caf` and `15e7f39148c939a7749de333f484bf232fc9c7b5` respectively; their current worktree bytes differ. Raw index SHA-256 remains `7a225e39f132005de82de9c15aba7e0a933c9e665f5ce556339c9cba644da7d0`.

## 2. Findings

### F-02 [suggested P1] Preservation manifest gives obsolete identities for two included originals

| Field | Evidence |
|---|---|
| Location | `results.md:30-57`, exact rows for `ideas/documentation-consolidation/tasks/T-001/brief.md` and `verification.md` |
| Trigger | Use ART-002 after the authority files changed in the worktree. |
| Consequence | T-002 would receive wrong byte identities for included preservation inputs; the assertion that all 517 HEAD/index/worktree versions agree is false. |
| Evidence | DISC-01 reports 517 entries and exactly four identity/version errors, all on those two paths. Current worktree hashes above differ from the recorded table and index blobs. The other 515 tracked rows and 182 retirement candidates reconcile. |
| Affected AC / invariant | AC-01, AC-05; V-01/V-06; R-01/R-04: current intended originals need exact version identity, and changed inputs invalidate dependent facts until reinspection. |
| Credible sibling surface | Any later changed preparation or task-report asset included under Q-001, especially untracked additions that T-002 must freeze, can invalidate the same exact-set assertion. |
| Smallest corrective direction | Reconcile the current Git/index/worktree inventory and update the preservation identities and drift account for the whole affected inclusion set; retain separate versions where they differ. |

### F-03 [suggested P2] Audit assessment still applies the superseded ref rule

| Field | Evidence |
|---|---|
| Location | `results.md:3`, `:252-257`, `:300-406` |
| Trigger | Consume the audit under current brief AC-05 and verification revision 2. |
| Consequence | The output declares itself `NON-COMPLETE` because a run-evidence finish ref was written, although the current authority expressly permits that namespace and requires its effects to be attributed separately. It also says the correction excluded the evidence lifecycle under the former stricter rule. This makes the audit's AC-05 disposition and handoff misleading. |
| Evidence | Brief AC-05 and V-05 revision 2 permit `refs/personal-skills/run-evidence/` instrumentation. The disclosed finish ref is in that namespace; `results.md` itself attributes it to the helper. The prior F-01 was a finding against revision 1 and remains historical evidence, not a current-rule violation by itself. |
| Affected AC / invariant | AC-05; V-05/R-04: report actual protected-state changes separately from authorized instrumentation and apply current authority to the assessment. |
| Credible sibling surface | Begin and recovery snapshot refs, metadata and snapshot objects receive the same revised treatment; changes to files, index or refs outside the namespace remain prohibited. |
| Smallest corrective direction | Reconcile the entire occurrence against revision 2, record authorized instrumentation separately, preserve historical reports, and update current scenario/overall claims only after current protected-state checks. |

No further confirmed finding was established. Prior F-01 remains in discovery-01/02 as a revision-1 finding. This report does not erase those reports or decide their acceptance disposition.

## 3. Completeness ledger

| Row | Contract and material cases; setup/oracle | Submitted evidence | Independent current probe | Result / reason |
|---|---|---|---|---|
| V-01 | AC-01/R-01: tracked, index, worktree, nontracked/ignored, mode/type and external boundary. Compare all current originals and versions to manifest. | 517 INCLUDE rows, 182 candidates, five explicit exclusions; claims all versions identical. | DISC-01 exact inventory finds two changed included paths and four errors. DISC-02 confirms five exclusion hashes, 32 candidate families, 182 candidates, 15 future files; no candidate LFS pointer, gitlink or submodule config. | **fail** — F-02; current worktree identities absent. |
| V-02 | AC-02/R-02: each candidate family; completed, unknown and unfinished evidence, retained `future-work/stale` and old plan review. Compare original verdicts and pending obligations. | Family table distinguishes unknown/unfinished and owner Q-003 disposition. | DISC-02 enumerates all 32 families. Focused original reads confirm T-005.2 `INCONCLUSIVE`, T-005.3 partial, T-005.6 documentary `ACCEPT`, and T-005 parent waiver. All 15 future-work files remain outside retirement. | **pass** for current candidate bytes; pending qualification is not called passed. |
| V-03 | AC-03/R-03: executable readers, fixture/setup closure, active navigation and historical pointers; inspect real source/embedded inputs and selectors. | 13 live candidate inputs, composition selector and migration owners. | DISC-02 finds 47 cases, 11 staged sets, five handoffs and no embedded existing candidate absent from inventory. Source trace confirms composition constants, manifest reader and `setup_consumer.py`'s `parents[3]`, child setup and separate Git baseline. Scoped search distinguishes active tests/readers from historical references. | **pass** for mapped current consumer source; migration equivalence remains unclaimed. |
| V-04 | AC-04/R-02: Q-001–Q-003 sources, per-candidate and global blockers. Check decisions versus `BLOCKED` assessment. | Q-001/Q-003 owner replies; Q-002 only recommendation; all candidates gated. | Prior discovery-01 records the supplied owner response; current tag lookup finds no proposed local tag and `origin` exists, with no publication proof. Candidate archive/dependency gates and overall `BLOCKED` remain consistent. | **pass** for owner gates; Q-002 stays downstream. |
| V-05 | AC-05/R-04: audit start/write/final, protected files/index/other refs stable, namespaced instrumentation attributed. Compare actual state and claimed disposition. | Original namespaced finish ref disclosed, but classified as a violation; correction excludes lifecycle. | DISC-01 confirms protected index and original candidate bytes; current outside-namespace refs and staged state show no detected change. Current AC-05 expressly permits the disclosed ref. Current audit disposition contradicts that authority. | **fail** — F-03 reporting/assessment. Original occurrence cannot be replayed; no new protected mutation is inferred. |
| V-06 | AC-05/R-04: observed drift invalidates affected facts; reinspection uses current bytes without restoring user work. | Correction claims stable old brief/verification bindings and no drift. | Current brief and verification hashes differ from manifest/index; current preflight still binds old hashes and revision 1. No updated ART-002 reinspection follows these changes. | **fail** — F-02 and stale preparation; correction/preflight owners must rebind. |

All six required rows have a current disposition. The report is partial because no corrected submission or ready preflight exists for revision 2. The historical start-to-finish process cannot be rerun as the same occurrence; present state and recorded changes are distinguished from historical claims.

## 4. Probe and aggregate record

| ID | Exact command / probe | Result and limits | Side effects |
|---|---|---|---|
| DISC-01 | `PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'` extracting and running Appendix A's code from `reviews/discovery-01.md` as recorded in `results.md:351-362` | Exit 0; 517 entries/rows, errors on two changed preparation paths; 182 candidates, 15 future files. Exit zero is diagnostic, not a pass. Current index hash matches; current refs hash differs as additional namespaced runs exist. | None. |
| DISC-02 | Same extraction command for Appendix B | Exit 0; 32 families covered; 47/11/5 embedded counts; no embedded existing candidate omitted; five exclusion identities agree. | None. |
| DISC-03 | `rg -n 'docs/tasks|docs/project-plan|docs/task-map|T0051|T0034' tests scripts skills README.md docs/future-work docs/project-plan-review.md --glob '*.py' --glob '*.md' --glob '*.json' -l`; focused source and historical-report reads | Active reader/setup closure and historical verdict distinctions corroborated. Searches alone do not prove behavior. | None. |
| DISC-04 | `git status --porcelain=v1 --untracked-files=all`; `git diff --raw`; `git diff --cached --raw`; `git ls-files --stage -- <two changed paths>`; `git for-each-ref --format='%(refname) %(objectname)' refs/heads refs/tags refs/remotes refs/stash`; SHA-256 reads | No staged diff; only two unstaged preparation paths and three untracked task artifacts before report. Index and HEAD stable. Current tag absent. Protected refs observed, but historical pre-run values depend on producer records. | None. |

Aggregate gate: **not run**. Owner: this discovery, initial revision-2 pass. The brief calls for a manual full manifest/obligation/consumer reconciliation, with no executable aggregate command. Targeted V-01/V-05/V-06 failures suppress any further aggregate. No gate or command was added. The consumer suite `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_review_composition.py` remains selected for T-003 and was not run as T-001 proof.

## 5. Scope, questions and route

Pre-report `git status --short` was exactly:

```text
 M ideas/documentation-consolidation/tasks/T-001/brief.md
 M ideas/documentation-consolidation/tasks/T-001/verification.md
?? ideas/documentation-consolidation/tasks/T-001/results.md
?? ideas/documentation-consolidation/tasks/T-001/reviews/discovery-01.md
?? ideas/documentation-consolidation/tasks/T-001/reviews/discovery-02.md
```

Post-report `git status --porcelain=v1 --untracked-files=all` adds only `?? ideas/documentation-consolidation/tasks/T-001/reviews/discovery-03.md`. HEAD and the raw index hash remain unchanged. Post-write `git show-ref | shasum -a 256` is `bab2e328f39472589e0da4cc46a942a7eab79ceedc205b7b5e6560d2843efa3c`; no evidence lifecycle was run by this review. Earlier reports, user preparation changes, audited originals, index and refs are not modified by this review. No overlap is absorbed into the task output. The exact author/session provenance of the preparation edits is unknown, so their ownership stays with the preparation/owner workflow.

Questions and unchecked work: the owner/T-002 still owns Q-002 destination, publication and navigation approval. Focused preflight owns readiness for verification revision 2; the implementer owns a current audit correction for F-02/F-03 and updated scenario evidence. Fresh discovery owns corroboration after corrected bytes. No schema or process-lifecycle contract is part of this documentation audit, so no validator or process fixture was run. Historical role qualification, archive recovery and migration equivalence remain outside T-001 proof.

The next route is focused `task-preflight` refresh for brief hash `94cc2e18...` and verification revision 2, then a bounded correction of `results.md`, then a fresh independent discovery. Give the separate acceptance decision call this report, both prior reports, current scoped diff, brief, verification revision 2, stale preflight/Decision context, all six row dispositions and reviewer Appendix A/B commands. This report makes no decision.

## 6. Discovery continuation

```markdown
Discovery continuation:
- Iteration / current byte identity: third discovery, first under revision 2; HEAD b65f900e7515ccfe36335b793b0c058b7b2bfa8c; results.md SHA-256 798906e82414c4c25f16e994a508e63e4eef2806c067ea6953b02347b23407ee; brief 94cc2e18...; verification 962a9b13....
- Coverage rows: V-01 fail (two included worktree identities stale); V-02 pass (candidate evidence); V-03 pass (consumer closure); V-04 pass (owner gates); V-05 fail (revision-1 ref assessment persists under revision 2); V-06 fail (changed preparation assets not reinspected). No row omitted.
- Finding IDs: F-02 suggested P1; F-03 suggested P2. Prior F-01 is historical revision-1 evidence; applicability changed by owner authority, not a review deferral.
- Finding/scenario continuity: prior V-01/02/03/04/06 pass and V-05 fail applied to old bytes/authority. Current producer results.md is unchanged since discovery-02 and still claims NON-COMPLETE; revision-2 preparation changed later. F-02 affects all included changed preparation/report inputs; F-03 affects begin/recovery/finish refs, metadata and objects while protecting files/index/other refs. Correction owner: T-001 implementer; readiness owner: focused preflight; evidence owner: fresh discovery; authority/disposition owner: separate acceptance/owner. No corrected producer evidence yet.
- Preparation/context: T-001 brief.md current hash 94cc2e18...; verification.md revision 2 hash 962a9b13...; preflight.md hash 9d79cb44... binds revision 1 and needs refresh; cleanup plan/task map and prior discovery-01/02.
- Reviewer regressions: discovery-01.md Appendix A/B exact embedded Python commands; rerun with the extraction invocation in results.md:351-362; source search and DISC-04 commands above. No new test files.
- Aggregate gate: not run; this discovery owns manual gate; decisive targeted failures V-01/V-05/V-06 suppress it. No prescribed executable command.
- Next: focused preflight refresh, bounded audit correction, then fresh independent discovery and separate acceptance decision.
```
