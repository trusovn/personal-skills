# Task Review Discovery Report: T-005.1 — Supply reproducible qualification inputs

| Field | Value |
|---|---|
| Producing stage | task-review-discovery; active project-local installation |
| Coverage completeness | partial — V-06 has static evidence and one reconstructed handoff, but the other consumer-visible input sets have not been independently assembled |
| Discovery iteration | first discovery pass |
| Created at | 2026-10-13T13:15:06.608910+00:00 |
| Repository root | /Users/mtrusov/work/skill-sources/personal-skills |
| Durable report path | docs/tasks/T-005.1/reviews/discovery-01.md |
| Task brief | docs/tasks/T-005.1/brief.md |
| Verification design / task context | docs/tasks/T-005.1/verification.md revision 1; preflight.md, including recorded dependency-gate override and owed dispositions |
| Current submission | docs/tasks/T-005.1/results.md, READY_FOR_REVIEW; six staged paths |

This report publishes evidence only. It contains no acceptance verdict, approved
deferral or advancement. It applies only to the bytes identified below. It does
not review or authenticate itself. A separate acceptance decision call consumes
this evidence; corrected bytes require fresh discovery.

## 1. Discovery provenance

This session authored no reviewed production, test or submission bytes. Its only
repository write is this report. Evidence is independent of implementation
session authorship. The session used the project-local discovery skill and its
report template, plus project-local testing-discipline to review test evidence.
No subagent, model, network or role-qualification call was launched.

HEAD: `58f5179284bfb51ea2ef1ceee7232ae5db80f4a9`.
SHA-256 of `git diff HEAD -- <six reviewed paths>`:
`e305af64ac920069c7ac799c12c28a541027c967994eca074e0aed2f9958100a`.
All six index blobs equal their respective worktree bytes; identities appear in
section 7. Loading this skill did not reset or substitute session authorship.

## 2. Findings

### F-01 [suggested P2] Full-projection receipt omits independent managed-block proof

| Field | Evidence |
|---|---|
| Current location | docs/tasks/T-005.1/evidence/V-03-install-projection.md:40–50; results.md:103 |
| Triggering state/input | A later leaf consumes the retained V-03 receipt as independent full managed-projection proof. The receipt counts 86 managed paths, compares 85 copied files, and attributes the remaining AGENTS.md block only to the canonical --check. |
| Consequence | The retained independent evidence does not cover the complete managed projection it claims. A consumer must invent the missing comparison step or rely on the check's own verdict for that surface. |
| Evidence | Receipt line 48 explicitly says the block was compared by --check. `source_projection_snapshot()` omits AGENTS.md, whereas `expected_managed_paths()` includes it. The exact independent comparison invocation is also absent: results command P3 describes a comparison rather than supplying its command/body. DISC-04 independently compared the block and all 85 files on a new target; this proves current install behavior but does not change the submitted receipt. |
| Affected AC | AC-02; V-03; S-02 / INV-009/010; parent evidence rule 2 |
| Broken invariant | Retained full-projection receipts must cover every canonical managed surface with independent byte/file-set evidence, separately from a matching CLI check and workflow identity. |
| Credible sibling surface | Rechecking the marked block after replacement in an existing target, and later T-005 call leaves renewing projection identity from the same receipt procedure. The independent copied-file comparison also needs a reproducible invocation rather than just a result count. |
| Smallest corrective direction | Make the task-local receipt procedure reproducible and independently compare the entire managed projection, including the canonical marked block. Record the command/setup and resulting complete comparison; keep --check, unmanaged preservation and workflow fingerprint claims separate. No installer or shared-helper repair is indicated. |

Suggested severity describes an evidence defect, not a demonstrated installer
runtime defect. Current disposable installation and drift behavior passed the
independent probes below. No second confirmed finding is inferred from the
unfinished V-06 evidence.

## 3. Completeness ledger

The ledger was established before behavioral probes. V-01–V-06 retain the
verification design's stable identities. Task-owned evidence is distinct from
historical owning-test references and future role qualification.

| Row ID | AC / invariant | Explicit material cases | Setup / oracle | Submitted evidence | Independent probe / current evidence | Result / reason |
|---|---|---|---|---|---|---|
| V-01 | AC-01; S-01 / INV-010 | INV-CASE-01–24; COMP-01–05; CCR-01–08; ROUTE-01, FIND-01, ROWS-01, REV-01, EFF-01, GATE-01, DISP-01; IFQ-01–03; P-01–P-07; current selectors; honest evidence levels | Load fixtures.md JSON; reconcile exact identities with both inherited composition files and INT-FLOW results; inspect owner/source/eval references and P ownership table | fixtures.md; results N; audit class | DISC-01/02: exact 47-ID set, all declared eval IDs and owner files resolve, audit is clean; all 47 individual omission controls are rejected. Parent ownership and public/lifecycle/tamper/validator/cleanup/continuation kinds remain visible. | pass — inventory/link and evidence-level contract checked; no inherited role result inferred |
| V-02 | AC-01/03/04; S-01 | INV-CASE-01 queue-defect; IFQ-01 correction-round unrun handoff | Fresh EVAL_WORK_ROOT per setup. Run queue CLI twice over two ready tasks, observe persistence; reconstruct prior MNT IDs, corrected source and external facts without a role call | V-02 receipt; P1/P2 | DISC-03/05: queue outputs TASK-1 then empty, statuses running/ready, Git unchanged; handoff prior report MNT-B1–B4/CHANGES_REQUESTED, pricing.py and correction facts exist. | pass — observed supplied fixture behavior and setup; actual role behavior remains unrun with T-005.3/.5 |
| V-03 | AC-02; S-02 / INV-009/010 | All 85 copied managed files, guide/shared scripts/config/schema, marked AGENTS block, sibling helpers, unmanaged preservation | Fresh committed Git target; canonical install/check; independent file-set/byte equality and exact canonical block extraction; helper availability from target sibling directory | V-03 receipt; P3; full independent comparison claimed | DISC-04/05: 85/85 bytes/file set plus marked block match; CLI compared 86; helper available from resolved target-local scripts. Submission independently compares only copied files and leaves block to --check. | fail — F-01 retained receipt lacks the required full independent/reproducible comparison; current installer runtime probe passes |
| V-04 | AC-02; S-02 | Fingerprint-excluded copied eval file mutation; read-only checks; restoration | Append newline to installed bounded-task-implementer/evals/evals.json; compare fingerprint, CLI and source bytes; snapshot files/Git; restore | V-04 receipt; P4 | DISC-05: fingerprint unchanged; --check exits 1 naming changed eval; independent comparison names same file; snapshots, Git status and HEAD unchanged during observation; restored match | pass — drift discriminates at actual installer CLI and filesystem boundary |
| V-05 | AC-01/03; S-01 | Correct inventory; omitted mapping, stale selector, nonexistent evidence controls; public fixture runtime | Existing new test class; same audit oracle against real/degraded input; real queue operation. Structural audit results are not role qualification | N/M; tests/test_review_composition.py | DISC-01: 3/3 new checks pass, including wrong control. DISC-02: all 47 omission controls rejected. DISC-03: queue public result matches stated defect. Relevant validator/lifecycle obligations remain inherited owner references, not newly executed success claims. | pass — bounded changed-check and fixture evidence; full module gate deliberately not run after F-01 |
| V-06 | AC-01/04; S-01 | Every claimed staged producer-to-consumer handoff; raw output replacement; preparation/current identities; evaluator exclusion | Inspect replacement table and independently assemble the consumer-visible input sets without setup code or expected answers | fixtures.md:982–998; N token/receipt check; generic per-leaf replacement instructions | Table names raw producer types, byte retention and preparation refs. IFQ-01 reconstruction identifies external correction facts that include expected next-report answers; those must stay evaluator-side or be separated before consumption. Other claimed handoff input sets were not independently assembled. | unchecked — only partial independent boundary evidence; stop at task soft review budget rather than infer every consumer input boundary from token checks. Next evidence owner: fresh discovery after preparation of explicit input manifests/sets by task owner. |

All finite inventory IDs are covered by V-01's exact-set audit. This does not
claim individual execution of all inherited cases. Public, process-cleanup,
validator, coherent-tamper and continuation role obligations remain assigned to
the inventory's inherited owners. This task introduces no executable schema or
process-lifecycle implementation. No schema text check is called behavioral
validator proof; no pure mock is called lifecycle proof.

## 4. Adversarial state and evidence checks

| Invariant | Cases exercised | Evidence |
|---|---|---|
| Inventory exact set | Complete inventory, then each of 47 distinct single-case omissions | Every omission rejected with its stable ID; submitted wrong control also rejects stale scenario/evidence pointer |
| Public repeated state | First and next real queue invocation after legitimate persisted state change | TASK-1/running then empty/TASK-2 ready: staged defect observed, not qualification success |
| Full identity versus fingerprint | Good copied profile, eval-only mutation, byte-exact restoration | Real CLI and independent byte comparison reject drift while fingerprint stays equal |
| Consumer evaluator separation | IFQ-01 prior report within consumer repo; correction facts outside it | External facts contain expected next-report identity obligations. This supports the held-back boundary but does not prove all other consumer assemblies |
| Preservation | Exact initial status, separate index/worktree identities, 422 protected-file hashes | Unchanged before report; disposable targets and fixture state cleaned up |

## 5. Independent probes and command results

All commands ran from the repository root with `PYTHONDONTWRITEBYTECODE=1`.
Inline Python probes used only existing modules and disposable temporary paths;
no reviewer regression file or reusable harness was added. Each subprocess had
a 30-second timeout and completed synchronously. No detached/background process
or inherited pipe remained; TemporaryDirectory contexts removed every target,
including on failed probe assertions.

| ID | Exact command / reproducible probe | Purpose | Observed result / limits |
|---|---|---|---|
| DISC-01 | `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_review_composition.T0051QualificationInputTests` | Changed/new checks first | Exit 0; 3 tests OK in 0.011s |
| DISC-02 | Inline Python: import test_review_composition as t; load t.t0051_inventory()/t.t0051_expected_ids(); assert exact set size 47 and empty t.t0051_audit_problems(); deep-copy inventory per ID, remove that ID and require its missing-ID message; read each owner file and referenced skill evals.json ID | Independent audit/control and current references | All 47 omission controls rejected; all owner files/eval IDs resolve. Two preliminary README-membership assumptions failed: guide paths are basenames and the guide does not enumerate every test owner. Those were reviewer harness mistakes, not task findings; reference check was corrected to existing owner files and inherited declarations. |
| DISC-03 | `EVAL_WORK_ROOT=<fresh>/public python3 skills/task-implementation-flow/task-review-discovery/evals/files/setup_fixture.py queue-defect`; write external state.json with TASK-1/TASK-2 ready; invoke `python3 <fresh>/public/queue-runner/src/queue/run_next.py <fresh>/state.json` twice; compare persisted JSON and Git status | V-02 public first/next occurrence | Setup exit 0; CLI exits 0/0, stdout TASK-1 then empty; running/ready persisted; Git unchanged |
| DISC-04 | Canonical `python3 scripts/install_development_skills.py <fresh committed target>`, then `python3 scripts/install_development_skills.py --check <target>`; independently enumerate declared skill files/guide/scripts, compare exact target file set and bytes; extract target AGENTS text between AGENTS_BEGIN/AGENTS_END and compare AGENTS_BLOCK.rstrip() | Current full installation behavior | 85/85 files plus canonical block equal; CLI match/86. Preliminary helper-path equality assertion failed because temp path resolution uses /private; resolved-path check passed in DISC-05. No source/target defect inferred. |
| DISC-05 | Inline Python using existing tests/test_install_development_skills.py helpers: init_repo(target, agents_text with trailing spaces); source_projection_snapshot() mapped to .agents; exact file set/bytes and direct marked-block equality; target-local run_evidence.py availability and workflow_version.py bounded-task-implementer; append newline to copied evals.json; run --check and fingerprint again; independently locate changed bytes; snapshot entire target including .git; restore copied file and recheck. Then run correction-round setup and inspect prior report/source/external facts. See exact boundary commands below. | V-02/03/04 and partial V-06 | Exit 0; full match, local helper available, eval drift exit 1/exact path, unchanged fingerprint, read-only snapshots/status/HEAD, restored match; handoff reconstructed. A preliminary assumption that correction-round emits a separate oracle file failed; source shows it emits correction-round-facts instead. Final probe inspects that actual output. |
| DISC-06 | `git diff --check`; inline compare six worktree SHA-256s, six `git rev-parse :<path>` blobs, exact status and 422 protected-file hashes against pre-probe snapshot | Structural/preservation only | Exit 0; no whitespace errors; all identities/protected bytes unchanged |

DISC-05 exact public boundary invocations (target and EVAL_WORK_ROOT are fresh
TemporaryDirectory paths, never this source repo):

```text
python3 scripts/install_development_skills.py <target>
python3 scripts/install_development_skills.py --check <target>
python3 <target>/.agents/scripts/run_evidence.py --repo <target> availability
python3 <target>/.agents/scripts/workflow_version.py bounded-task-implementer
# append one newline to target-only bounded-task-implementer/evals/evals.json
python3 scripts/install_development_skills.py --check <target>
python3 <target>/.agents/scripts/workflow_version.py bounded-task-implementer
# restore original target-only bytes
python3 scripts/install_development_skills.py --check <target>
EVAL_WORK_ROOT=<fresh handoff root> python3 skills/task-implementation-flow/task-maintainability-review/evals/files/setup_fixture.py correction-round
```

Comparison algorithm: map source_projection_snapshot keys to `.agents/<key>`
(with the profile guide at `.agents/skills/README.md`), compare equality with the
entire fresh `.agents` file dictionary, then separately extract the exact
managed AGENTS block and compare it with the canonical AGENTS_BLOCK.rstrip().
For drift, require the changed-byte list to contain exactly the mutated path,
and require whole-target SHA-256 snapshots, status and HEAD equality before
and after both read-only observations. Compare fingerprint fields separately
from Git metadata. Preservation uses the original unmanaged AGENTS prefix,
including trailing whitespace, and app.txt baseline bytes.

No newly claimed validator or process-cleanup success needs an additional
validator/lifecycle probe here. Inherited role cases and their distinct decisive
proof duties remain with later leaves. No live or whole-repo suite ran.

## 6. Aggregate-gate record

| Field | Value |
|---|---|
| Exact command | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_review_composition.py` |
| Status | not run |
| Owner / stage | this independent initial discovery |
| Reason | F-01 is a decisive V-03 evidence failure; V-06 also remains unfinished. The skill suppresses aggregate execution after targeted failure. |
| Current evidence | New targeted class is green; independent runtime install/drift probes are green; these do not close receipt or consumer-boundary gaps. Implementer M's 19-test pass is a submitted claim, not this discovery's gate. |

The installer-owner module was not run: source profile/installer bytes are
unchanged and narrow current install/check/drift evidence was obtained. No
additional gate or whole-repository command was added.

## 7. Scope and baseline comparison

Preflight recorded HEAD f8050d1 with user-owned index.json/T-005 package work.
Submission explains the user's later commit 58f5179, which is current HEAD;
index.json and task preparation artifacts are now committed. No unexplained
working-tree overlap exists in the six reviewed paths. Submission initially
recorded unstaged work; current staging is separately identified here and was
preserved. Status hides ignored .DS_Store/runtime files; protected-file hashes
also cover existing files in skills/scripts/.agents.

Exact reviewed status immediately before this report:

```text
A  docs/tasks/T-005.1/evidence/V-02-setup-reconstruction.md
A  docs/tasks/T-005.1/evidence/V-03-install-projection.md
A  docs/tasks/T-005.1/evidence/V-04-drift-contrast.md
A  docs/tasks/T-005.1/fixtures.md
A  docs/tasks/T-005.1/results.md
M  tests/test_review_composition.py
```

| Path | Index blob | Worktree SHA-256 | Comparison |
|---|---|---|---|
| docs/tasks/T-005.1/evidence/V-02-setup-reconstruction.md | `d742119b31c4845fd05f7105c4a88fe6c9f6bda1` | `e07b655511b64b50fb0a528b9e61914c9186dfd110683bb98e9e528d7df0ed4a` | equal to index; task-owned |
| docs/tasks/T-005.1/evidence/V-03-install-projection.md | `0da49728e9a133c8b05c3f72637d0776cc0d12dd` | `a818fc66601e4ea06a6bb73270d24a7f943f0803f3c4a71a97d3671e258ac4b7` | equal to index; task-owned |
| docs/tasks/T-005.1/evidence/V-04-drift-contrast.md | `7c9b97658db4c01c246ff762b7c483c10b142310` | `6c967a07eb0f13119f7374dbe5b3e5771573c331e0c5fd66aaf95044818ef239` | equal to index; task-owned |
| docs/tasks/T-005.1/fixtures.md | `1a77cc219bd5649250976abc162d3ae5fb90186a` | `d4cad9e281303dee6a9ebf6fcf3815c7269e20090865145c6e97844b834079ea` | equal to index; task-owned |
| docs/tasks/T-005.1/results.md | `5a677feb83f70253fb4143f6ae8fb20dc2d1756a` | `eeb0519de98eeb87a08525fbea3ce501faea579530e4a3051d3f9f44fde17282` | equal to index; task-owned |
| tests/test_review_composition.py | `fc5e19745015c5878ac99ff2c3a2d468b53ed19b` | `20a3ad3876f7deaf84c48877f0eb366aec50dca70d2cd37ce2b148c0de19b85a` | equal to index; task-owned |

Allowed changes match brief/results. No source policy, helpers, installer,
active installation, plan or historical report changed. Before/after probes
preserved all 422 protected-file hashes. Authority hashes:

- brief.md: `51c7a380f88cf493dd443b9e66d625609d9f10b8906eb71c723c566aa1a3b67b`
- verification.md revision 1: `c7aacb05306660ae92548689ea69803f1314427e1559c74e8fd25b8b8ae3d105`
- preflight.md: `dd2e52866fffb3845134f0c9abd2bb70f0708738c669f6dc1af1b12ed03d761d`

## 8. Questions, unchecked work and residual risks

| Type / row | Reason | Owner / follow-up |
|---|---|---|
| unchecked V-06 | Generic replacement/exclusion text and token checks do not independently establish every assembled consumer input boundary. Only IFQ-01 was reconstructed in this pass. Soft task budget reached; remaining rows stay visible. | Task owner supplies/identifies exact consumer-visible manifests and placeholder mapping; fresh discovery assembles remaining handoffs, keeping evaluator-only facts out. No role call is needed for this setup check. |
| conditional review evidence | results.md says maintainability review is applicable before discovery. No maintainability report exists under this package's reviews directory. This call gathers discovery evidence only and does not waive that separate stage. | Coordinator routes current/corrected bytes to fresh task-maintainability-review before final acceptance context. |
| dependency warning | Preflight records a user override for this task, but dependency acceptance dispositions remain absent. The override is recorded task context, not a new approval issued here. | Coordinator and separate per-package acceptance calls; preserve warning before T-005.6 audit. |
| unrun role qualification | Every inventory role boundary remains explicitly unrun; this leaf provides inputs only. | T-005.2–.5; T-005.6 audits ART-012. |

No independent reviewer regression file was added. Regression directions are
F-01's full marked-block comparison and V-06's consumer assembly; exact narrow
existing test command is DISC-01. Current runtime evidence concerns local
filesystem/Git/CLI boundaries only.

## 9. Coverage completeness and next route

Coverage is **partial**: V-01, V-02, V-04 and V-05 pass; V-03 fails the retained
receipt requirement (runtime behavior passes); V-06 is unchecked beyond stated
partial evidence. F-01 is the sole confirmed finding. An unfinished consumer
boundary is not presented as clean.

Next owner: task coordinator/implementation owner. Smallest action: route F-01
for task-local receipt correction and identify the remaining V-06 input sets;
retain separate applicable maintainability review, then obtain a new independent
discovery report over corrected bytes. The separate acceptance call must receive
this report and subsequent evidence, the brief, scoped diff, verification revision
1, readiness/recorded decision context, all unfinished rows and reviewer commands.
No decision or advancement is performed in this report.

## 10. Discovery continuation

```markdown
Discovery continuation:
- Iteration / current byte identity: first discovery; HEAD 58f5179284bfb51ea2ef1ceee7232ae5db80f4a9; scoped diff SHA-256 e305af64ac920069c7ac799c12c28a541027c967994eca074e0aed2f9958100a; six separate index/worktree identities in section 7.
- Coverage rows: V-01=pass (47 IDs/omission controls/owners); V-02=pass (public twice + handoff setup); V-03=fail (F-01 receipt incompleteness; runtime full projection passes); V-04=pass (eval drift/fingerprint/read-only/restoration); V-05=pass (targeted good/wrong checks); V-06=unchecked (other consumer assemblies not independently reconstructed; static/IFQ-01 evidence only).
- Finding IDs: F-01 [suggested P2], full independent/reproducible projection receipt.
- Finding/scenario continuity: no prior discovery ledger or findings. Producer claims V-01–V-06 OK in results.md; current independent statuses above supersede those claims only as evidence for these bytes. F-01 correction owner=task implementer, evidence owner=fresh discovery, authority owner=task coordinator/brief. V-06 incomplete at soft budget; preparation owner=task implementer, evidence owner=fresh discovery, authority owner=task coordinator. Sibling surfaces: managed-block replacement/recheck and every later call leaf's projection refresh; consumer manifest/oracle exclusion across staged handoffs. Conditional maintainability evidence remains separately owned and owed; dependency warnings are carried.
- Preparation/context: docs/tasks/T-005.1/brief.md; verification.md revision 1/hash c7aacb05306660ae92548689ea69803f1314427e1559c74e8fd25b8b8ae3d105; preflight.md incl. recorded dependency override and warnings; docs/tasks/T-005/brief.md evidence rules/P-01–P-07.
- Reviewer regressions: no new repository files; existing focused command PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_review_composition.T0051QualificationInputTests; rerun DISC-05 full independent block/file comparison and remaining V-06 consumer assembly over corrected bytes.
- Aggregate gate: not run; PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_review_composition.py; owner=initial independent discovery; suppressed by F-01 and unfinished V-06. Producer gate is not current independent proof.
- Next: task-local correction/preparation, separate applicable maintainability review, then fresh independent discovery; separate acceptance consumes the complete or explicitly partial context without waived duties.
```

## Post-report preservation record

Exact `git status --short` after the report write:

```text
A  docs/tasks/T-005.1/evidence/V-02-setup-reconstruction.md
A  docs/tasks/T-005.1/evidence/V-03-install-projection.md
A  docs/tasks/T-005.1/evidence/V-04-drift-contrast.md
A  docs/tasks/T-005.1/fixtures.md
A  docs/tasks/T-005.1/results.md
M  tests/test_review_composition.py
?? docs/tasks/T-005.1/reviews/
```

`git status --short --untracked-files=all` resolves the sole new directory entry to
`?? docs/tasks/T-005.1/reviews/discovery-01.md`. Only this report entry differs from the reviewed status.
