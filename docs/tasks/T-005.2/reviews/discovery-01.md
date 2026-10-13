# Task Review Discovery Report: T-005.2 — Exercise preparation and readiness recovery

| Field | Value |
|---|---|
| Producing stage | `task-review-discovery`, project-local installed skill |
| Coverage completeness | partial — preparation-call provenance and qualification are not independently established; required refusal/recovery/routing calls remain unrun |
| Discovery iteration | first discovery pass, discovery-01 |
| Created at | 2026-10-13T14:48:14Z |
| Repository root | /Users/mtrusov/work/skill-sources/personal-skills |
| Durable report path | docs/tasks/T-005.2/reviews/discovery-01.md |
| Task brief | docs/tasks/T-005.2/brief.md |
| Verification / context | docs/tasks/T-005.2/verification.md revision 1; preflight.md, including Decision context; parent docs/tasks/T-005/brief.md P-01/P-02 and evidence rules 1–7 |
| Current submission | results.md, READY_FOR_REVIEW; three evidence files; four staged additions |

This report publishes evidence only. It contains no acceptance verdict,
approved deferral, or advancement. It applies only to the bytes identified
below. It does not review or authenticate itself. Corrections require a fresh
discovery report and a separate acceptance decision.

## 1. Discovery provenance

This session authored no reviewed production, test, fixture, or submission
bytes. It began with the four staged additions below. It performed read-only
inspection and local disposable probes; its sole repository write is this report.
Evidence is independent within the stated probe limits.

- HEAD: `9127e5923e647d178581336b687663cd2e5fb899`.
- Scoped staged binary diff SHA-256: `eba5dedd258a5e6e8b645d0709656557d8ffd7c8a97ac1f9389a02d483fbb8a4`.
- Each of the four staged index contents equals the corresponding worktree
  content. Index blob identities were checked separately from worktree hashes.
- Active discovery instructions:
  `.agents/skills/task-implementation-flow/task-review-discovery/SKILL.md`
  and its report template. Verification selection used
  `.agents/skills/testing-discipline/SKILL.md`. Neither installation was refreshed.
- No earlier T-005.2 discovery report exists. T-005.1 acceptance-01 and its
  discovery-03 continuation are dependency context, not current proof of this leaf.

## 2. Findings

### F-01 [suggested P2] Claimed retained raw evidence is missing

| Field | Evidence |
|---|---|
| Current location | docs/tasks/T-005.2/results.md:77; evidence/run-log.md:120–134; evidence/preparation-and-recovery-observations.md:12–31 |
| Trigger | Follow P2's claim that verbatim control bytes are retained in run-log.md, then follow its cross-reference to preparation-and-recovery-observations.md. Both files contain descriptions, selected quotations and identities rather than the complete captured controls. The log says the raw capture directory was removed. |
| Consequence | A later reviewer cannot audit the historical captures or establish the claimed separate producer/consumer calls from retained raw records. V-01 and V-07's observed-pass claims exceed the evidence supplied. Recreating deterministic fixtures establishes new observations, not preservation of the earlier run's raw output. |
| Evidence | DISC-02: only three evidence Markdown files exist; both historical raw roots are absent; all six complete recovery control/history files compared against both cited reports are absent as byte sequences. The retained run manifest has `checks: []` and unavailable runtime identity. Its begin snapshot proves preparation files existed, but does not record calls or reads. |
| Affected AC | AC-04 directly; AC-01's claimed handoff provenance; AC-03's retained recovery artifacts; V-01/V-05/V-07 |
| Broken invariant | Parent evidence rule 3 and V-07 require raw producer output to be preserved before grading and consumed by reference. A summary, hash, or begin/finish snapshot does not replace the actual capture. |
| Credible sibling surface | FEASIBLE and UNAVAILABLE current/old verification and ready preflight; REV-1 and QR-12 controls; the claimed designer → preflight → implementer chain; INT-FLOW-001 I-04 preparation-reference parity consumed by later discovery/decision roles. These share the same raw-retention claim. |
| Smallest corrective direction | Restore or supply the retained raw artifacts and concrete producing/consuming invocation records for each claimed observation, bound to the recorded identities. Where historical capture cannot be recovered, downgrade that claim to an explicit evidence gap and preserve any separately authorized new run as new evidence. Apply the retention rule to the complete handoff and sibling controls. |

This finding does not assert that the preparation calls never happened.
It identifies the missing retained evidence and the unsupported strength of
the submitted observation labels. Explicitly unrun controls are gaps, not
invented policy defects.

## 3. Completeness ledger

Rows preserve the verification's V-01–V-07 IDs. Subrows isolate independently
proved local facts from unavailable role boundaries. “Blocked” here describes
missing evidence, not a verdict on the task. All rows are required/material
unless identified as scope preservation.

| Row ID | AC / invariant | Explicit material cases | Setup / oracle | Submitted evidence | Independent probe / current evidence | Result / reason |
|---|---|---|---|---|---|---|
| V-01 | AC-01; P-01/INV-001/002/003; INV-CASE-19 | Executable package actual design → ready → entry; compact documentation package | Separate authorized calls, preserved raw output and exact consumed identities in order; no staged reports counted as outputs | Own package chain claimed observed pass; QR-12 and PKG-1/DOCS variants unrun | DISC-02 proves preparation bytes existed before implementation; static trace verifies declared hashes. No raw separate-call/consumer-read records supplied; no compact-package role call | blocked — independent role-chain provenance is missing; coordinator owns call records/authorization; implementer owns claim correction (F-01) |
| V-01-A | AC-01 artifact existence/bindings only | Current brief, verification revision 1 and ready preflight existed before implementation | Compare current bytes with recorded hashes and retained begin snapshot | Three full hashes and begin run ID | DISC-02 compares all three against begin snapshot: exact match; §7 independently computed hashes match submission | pass — artifact existence/identity only, not role execution or reads |
| V-02 | AC-02; P-01/INV-001/002/003 | Omitted AC despite green included evidence; unsupported scenario; weak oracle; missing/foreign verification; missing/malformed/duplicate/foreign Source brief; valid ownership/coverage controls | Staged coverage-closure, verification-conflicts, readiness-cases; actual role refuses for intended reason and preserves foreign/conflict artifact bytes | Staged controls; green M1–M3; roles explicitly unrun, ledger 5 | DISC-01 discriminating-input/readiness checks pass; static audit retains all listed variants and their gap classification. No actual designer/preflight refusal output | blocked — coordinator has not authorized/launched the role assessments; tests prove fixture structure, not refusal |
| V-03 | AC-02; P-01/INV-001/002/003; INV-CASE-05/19/20/21 | Valid absent task-owned future test; missing indispensable fixture/capability; dependency; permission; resolved dirty ownership vs unresolved overlap; guided direct edit | readiness-cases plus scheduler-missing, queue-ready, api-overlap, queue-guided; available oracle must run; unavailable prerequisite stays absent; actual readiness names owner/recovery | Staged cases and structural tests; roles unrun | DISC-01 readiness test executes available baseline/session boundary while future test and secure clock remain absent; entry fixtures retain negative states. Actual readiness/ownership routing absent | blocked — missing authorized role observations; coordinator evidence owner, prerequisite/permission owners remain unchanged |
| V-04 | AC-01/02; P-01; INV-CASE-21/22; IFQ-02 / INT-FLOW-001 I-05 | Unpackaged direct edit; compact docs relabel attempt; decomposed parent; blocked design; direct legacy brief; integration leaf vs composite parent, sibling INT-10/system scope, unavailable or unresolved oracle | preparation-routes, integration-leaf, entry-cases; separate roles obey package/leaf authority and leave refused inputs unchanged | Staged controls; INV-CASE-22 prompt-only gap; roles unrun, ledger 2/5 | DISC-01 integration and entry fixtures pass; DOCS lacks preflight, relabel/direct requests and all entry contrasts present. No role-output or refused-input before/after execution | blocked — role boundaries unrun; coordinator owns; unresolved requirements remain task-design/decision owner |
| V-05 | AC-01/03; P-02/INV-003/005/008; INV-CASE-23, CCR-07, REV-01, I-04 | Coverage gap → reasoned retained-ID revision → old-ready rejection before recovery → focused ready → revised proof → separate new decision → old-ready reintroduced; unavailable-capability contrast | Actual separate revision/readiness/proof/discovery/decision calls with retained original artifacts; rejection must name obsolete revision both times | Staged rev-2 design beside old ready; current role recovery unrun, ledger 3/4 | DISC-01/02 prove staged history/reason/IDs and absent clock. Neither first rejection nor recovered readiness/proof/decision nor second rejection was run | blocked — no authorization/raw role chain; coordinator launches, preparation/proof/decision owners supply their separate outputs |
| V-05-H | AC-03 local historical-control integrity | FEASIBLE and UNAVAILABLE retain original V-01/V-02 bytes, revision reason/new V-03, old-ready rev 1 and old design | Fresh disposable revision-recovery; revision-2 text normalized only for comparison must start with original revision-1 bytes | Staged history summarized, claimed verbatim capture | DISC-02 confirms both original prefixes unchanged; all six full control/history file identities printed; DISC-01 confirms revisions/IDs and negative capability state | pass — current fixture history only; historical capture remains F-01 |
| V-06 | AC-02/03; P-02; CCR-07, REV-01 | Changed requirement vs unchanged-authority repair; expected implementation/report effects; authority/prerequisite/ownership/permission/capability changes; equal-status changed bytes | Actual before/after Git boundaries and role routing for intended reason, preserving user index/worktree state | Eight staged transitions plus freshness observation; routing unrun | DISC-01 transition setup and freshness checks pass; material vs expected-effect inputs are distinct. No authorized role assesses these transitions | blocked — routing evidence unrun; coordinator evidence owner; task design owns changed requirement |
| V-06-F | AC-03; INV-CASE-24 local freshness fact | Same short status and index, changed non-artifact worktree | Freshness fixture baseline versus actual status, index SHA-256 and worktree SHA-256; preserve supplied ownership | run-log probe 1 | DISC-01 asserts status/index equality and worktree inequality; also executes queue-ready public negative boundary, retains state and isolates expected packet effect | pass — local identity/runtime fact only; does not prove a role rejected staleness |
| V-07 | AC-04; P-01/P-02 raw retention | Observed authorized call; unapproved/unavailable call; inherited local/staged evidence; retained raw artifacts and identities | Audit durable receipts against full raw output and producer/consumer records before grading | “Raw”, “verbatim”, observed-pass claims; summaries; run sidecar; explicit unrun ledger | DISC-02 shows missing complete captures, deleted raw roots and empty checks; preparation begin snapshots are real but are not call transcripts | fail — F-01; implementer owns evidence/claim correction |
| V-07-U | AC-04 unrun honesty | Unrun ledger rows 1–7, unavailable decisive capability, inherited stages | Every unrun required boundary remains incomplete with reproducible setup/reason/owner | unrun-role-boundaries.md, V-02–V-06 prose | Static crosswalk confirms controls and unrun ledger cover required role gaps; does not relabel them as passed role behavior | pass — explicit unrun accounting, apart from the claimed observed chain/captures in F-01 |
| V-07-Q | AC-04; parent rule 2 / V-07 installed-copy qualification | Calls use qualified disposable installed profile and sibling helpers; full projection/check/source revision renewed before calls | Current per-call qualification receipt bound to the actual used installation; fingerprint alone insufficient | T-005.1 prior receipts; own package says active project-local chain and source scripts/run_evidence.py; no fresh qualification receipt | No installed-profile execution qualification is proved by DISC-01/02. Preflight permits repository-root artifacts, but this does not itself supply the mandated disposable-copy/renewal proof | blocked — task-preflight/coordinator own envelope reconciliation and current per-call receipts; no installation refreshed by discovery |
| SCOPE | AC-04 protected state | Four allowed docs additions; prepared artifacts, source/tests/active installation, authority, index and user OS files | Before/after SHA-256, exact status, separate index identities; only new report may differ | No other edits claimed | DISC-03: 547 initial files unchanged, four index blobs unchanged, diff digest unchanged; OS file hashes retained; post-write recheck below | pass — only discovery-01 report added |

The brief's two finite-risk rows are fully represented: P-01 maps to
V-01–V-04/V-07; P-02 maps to V-05–V-07. No material row was removed because
the owner tests passed. No optional broad regression was selected.

## 4. Adversarial state and evidence checks

| Invariant | Cases exercised / accounted for | Result and limit |
|---|---|---|
| Evidence strength | Begin snapshot/three hashes vs actual call/consumer-read proof; complete capture vs summaries/selected quotations | Snapshot/hash comparisons pass; raw-retention comparison fails (F-01); raw roots absent and manifest checks empty |
| Revision/history integrity | Current rev 2 vs old design/readiness rev 1; FEASIBLE and UNAVAILABLE siblings | Local prefix/ID/reason/history checks pass for both; neither obsolete-ready refusal was executed |
| Prerequisite distinction | Available baseline/public session oracle with future test absent; indispensable clock/dependency/permission contrasts | Available local behavior exercised by DISC-01; negative prerequisites retained; readiness decisions unrun |
| Freshness vs expected effect | Equal status/index with changed worktree; new in-scope packet; eight material/expected Git transition roots | Local contrasts pass; role routing still blocked |
| Authority scope | Integration leaf, parent, sibling requirement, unavailable oracle; compact relabel/direct/legacy cases | Input contrasts pass; role compliance unrun |
| Tamper/schema/lifecycle | No new executable validator contract, tamper guarantee or process-lifecycle change in reviewed diff | Not a substitute for role evidence. No schema/lifecycle qualification claimed or new probe added |

Ordinary fixture staging and synchronous subprocess invocations completed.
TemporaryDirectory roots were removed; no background server, worker group or
long-lived process was launched. These probes do not claim process-lifecycle
coverage for other qualification cases.

## 5. Independent probes and command results

All commands ran from the repository root, local-only, with bytecode writing
disabled for Python. No dependency install, network/model call, live eval,
subagent, source edit, Git mutation or active-installation refresh occurred.

| ID | Exact command / probe | Purpose | Result | Side effects / independence limit |
|---|---|---|---|---|
| DISC-01 | Focused command below | Current discriminating fixtures/runtime facts for V-02–V-06 | Six tests OK, 1.827s, exit 0 | Disposable fixture roots removed by existing test helpers; assertions over source fixtures are local setup/runtime evidence, not installed role behavior |
| DISC-02 | Full stdin driver below | Snapshot provenance and raw capture retention; recovery sibling history | Exit 0 inspection; retention oracle FAIL: all six full captures absent from both cited reports. Snapshot equality/history checks pass | One fresh disposable recovery root removed; old raw roots only inspected, not changed |
| DISC-03 | `git diff --check`; `git diff --cached --check`; snapshot comparison procedure in §7 | Scope/protected state | Both checks exit 0; 547 initial-file hashes and four index identities unchanged before report | Read-only; post-report comparison excludes only this new report |
| DISC-04 | Static read/trace of brief, verification revision 1, preflight Decision context, scoped additions, T-005.1 fixtures handoff manifest and acceptance-01 | Authority/scenario/permission reconciliation | Every required V-ID and inherited control accounted for; no raw separate-call receipt located in declared package evidence | Submitted claims remain producer-attributed; prior accepted fixture inputs are not renewed role proof |
| UNRUN | not run — separately authorized designer/preflight/implementer/discovery/acceptance scenario calls | V-01 provenance, V-02/03/04 decisions, both V-05 obsolete-ready substitutions, V-06 routing, V-07-Q qualification | Blocked as detailed in ledger | The present request authorizes discovery of this leaf, not a new model-budget qualification campaign or subagent/role runner |

### DISC-01 exact command

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_task_preparation_contracts.TaskBriefDesignerPackageTest.test_packaged_preparation_fixtures_supply_discriminating_inputs test_task_preparation_contracts.TaskBriefDesignerPackageTest.test_integration_leaf_fixture_supplies_qualification_inputs test_task_preflight.PreflightContractTest.test_readiness_fixture_supplies_independent_defects_and_feasible_future_test test_task_preflight.PreflightContractTest.test_revision_and_context_fixtures_preserve_supplied_contrasts test_task_preflight.PreflightContractTest.test_freshness_fixture_has_same_status_but_different_nonpacket_bytes test_bounded_task_implementer.ImplementerContractTest.test_entry_fixture_supplies_valid_and_every_invalid_state
```

These are existing targeted cases, not a newly added aggregate command.
No test/eval/fixture bytes were written.

### DISC-02 exact command and observed output

```sh
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import hashlib,json,os,subprocess,tempfile
from pathlib import Path
repo=Path.cwd()
manifest_path=repo/'.git/personal-skills/run-evidence/runs/run-20261013T143605Z-d20d1908061f/manifest.json'
m=json.loads(manifest_path.read_text())
print('manifest checks:',m['checks'],'runtime identity:',m['runtime']['identity_source'],'closure:',m['closure'])
for name in ('brief.md','verification.md','preflight.md'):
 p='docs/tasks/T-005.2/'+name
 data=subprocess.check_output(['git','show',m['repository']['begin']['snapshot']+':'+p])
 print('preexisting at begin',p,hashlib.sha256(data).hexdigest(),'equals current:',data==(repo/p).read_bytes())
print('retained evidence files:',sorted(str(p.relative_to(repo)) for p in (repo/'docs/tasks/T-005.2/evidence').rglob('*') if p.is_file()))
print('historical raw roots exist:',Path('/tmp/opencode/t0052').exists(),Path('/tmp/opencode/t0052-raw').exists())
reports=[repo/'docs/tasks/T-005.2/evidence/run-log.md',repo/'docs/tasks/T-005.2/evidence/preparation-and-recovery-observations.md']
with tempfile.TemporaryDirectory(prefix='t0052-discovery-') as tmp:
 env=os.environ|{'EVAL_WORK_ROOT':tmp,'PYTHONDONTWRITEBYTECODE':'1'}
 subprocess.run(['python3','skills/task-implementation-flow/task-preflight/evals/files/setup_fixture.py','revision-recovery'],env=env,check=True,timeout=20)
 root=Path(tmp)/'revision-recovery'
 for task in ('FEASIBLE','UNAVAILABLE'):
  for name in ('verification.md','preflight.md','verification-v1.md'):
   b=(root/'docs/tasks'/task/name).read_bytes()
   print(task+'/'+name,'sha256',hashlib.sha256(b).hexdigest(),'complete bytes in cited reports:',[b in p.read_bytes() for p in reports])
 print('original scenarios unchanged:',all((root/'docs/tasks'/t/'verification.md').read_text().replace('Verification revision: 2','Verification revision: 1').startswith((root/'docs/tasks'/t/'verification-v1.md').read_text()) for t in ('FEASIBLE','UNAVAILABLE')))
 print('unavailable clock absent:',not (root/'tools/secure_clock.py').exists())
print('disposable removed:',not Path(tmp).exists())
PY
```

```text
manifest checks: [] runtime identity: unavailable closure: {'kind': 'explicit_finish', 'outcome': 'completed', 'recovered_at': None}
preexisting at begin docs/tasks/T-005.2/brief.md 794247bc2477968d6394ce6bdbb9798ab6c06b96ed4d28ab7383da68ab391c77 equals current: True
preexisting at begin docs/tasks/T-005.2/verification.md 85f58c81d53fc6629baaf3eb663a5b3031d48f4b63982630e51fa7b77cd4431b equals current: True
preexisting at begin docs/tasks/T-005.2/preflight.md f7d367539891d51d1d07b428fc9953b4e10ad726446c74ad5d1af1b8b647b04d equals current: True
retained evidence files: ['docs/tasks/T-005.2/evidence/preparation-and-recovery-observations.md', 'docs/tasks/T-005.2/evidence/run-log.md', 'docs/tasks/T-005.2/evidence/unrun-role-boundaries.md']
historical raw roots exist: False False
FEASIBLE/verification.md sha256 5cbaac52c158485165fe94aa70a9cd5858241c347be6d2060b3a5aac6ffc80a4 complete bytes in cited reports: [False, False]
FEASIBLE/preflight.md sha256 da1b6e418e55502dafdc655026f1ffce207236a29b4805f2e932167b978b9076 complete bytes in cited reports: [False, False]
FEASIBLE/verification-v1.md sha256 1f57428100bc27d5b69e8f09ef40d52cafeded3c7b83101fc615b408213cf991 complete bytes in cited reports: [False, False]
UNAVAILABLE/verification.md sha256 7857d14b1fa1f3a8a922529a1304e4382584dd8c884baeabda9bffe675f23844 complete bytes in cited reports: [False, False]
UNAVAILABLE/preflight.md sha256 cd48359b6147bb4ed696292a3081d44ae1835feb558a00b318f056edde394c93 complete bytes in cited reports: [False, False]
UNAVAILABLE/verification-v1.md sha256 5d6b5abbf1f036853b70fd162953496acdf26b75632b0e8ea809dad8cfc33ad5 complete bytes in cited reports: [False, False]
original scenarios unchanged: True
unavailable clock absent: True
disposable removed: True
```

The driver's exit 0 means inspection completed; the decisive retained-byte
oracle is the displayed false comparison, not the process exit code. The
history comparison and available local boundaries do not repair that failure.

## 6. Aggregate-gate record

| Field | Value |
|---|---|
| Exact command | not run |
| Status | not run |
| Owner / stage | independent initial discovery, this report |
| Reason | Decisive targeted evidence-retention failure F-01 suppresses aggregate verification. Required role rows also retain concrete non-gate authorization/provenance blockers. |
| Current evidence | DISC-01 local targeted checks pass; DISC-02 raw-retention oracle fails; ledger explicitly retains every blocked row. |
| Submitted gates | M1/M2/M3 green labels are implementer claims. No prior pass is copied as this discovery's aggregate. |
| Conditional owners | Separate role/qualification owners retain their proof duties; acceptance consumes this record without inventing or re-owning a gate. |

No whole-repository/live/model gate was added. Nearest owning suites were not
run after the decisive failure merely for completeness. No earlier discovery
gate exists for this leaf to mark premature.

## 7. Scope and baseline comparison

The scoped diff consists exactly of the four new files listed in results.md,
all within the task's allowed documentation/evidence scope. Prepared brief,
verification and preflight are committed inputs. No production, test, fixture,
harness, installer or runtime contract bytes changed. No maintainability/registry
gate was invented for this documentation-only diff; the submission's conditional
stage judgment is consistent with the changed bytes.

| Item | Recorded baseline | Current reviewed state / classification |
|---|---|---|
| HEAD | Preflight: 3eba17c; implementation entry: 9127e59 | 9127e5923e647d178581336b687663cd2e5fb899; coordinator preparation commit expected; no discovery change |
| Status | Implementation log: three untracked OS .DS_Store files | Four staged task additions below; OS files still exist but are absent from current short status. No attribution of historical status housekeeping to this task is inferred. |
| Scope | results.md and evidence/, task-local missing adapters if needed | Exactly four allowed files; no adapter introduced |
| Artifact identities | Brief/design/preflight hashes supplied in results.md | Independently match current bytes and begin snapshot; artifact identity does not prove role reads |
| Dependency/context | T-005.1 acceptance-01; parent P-01/P-02; inherited warning | Read as authority context; no prior role qualification is promoted to this leaf's proof |
| Protected state | Initial snapshot of 547 tracked/installed files plus four index entries | All unchanged before/after local probes; report excluded only from its own post-write comparison |

Reviewed worktree SHA-256 equals independently computed index SHA-256 for each
staged file:

| Path | Index blob | Worktree/index SHA-256 |
|---|---|---|
| docs/tasks/T-005.2/evidence/preparation-and-recovery-observations.md | `b115f142afc36c87705c7e04f876d7222f3dfd63` | `079c621266d77603e590ed1f8784c2fb1ca3a66cbcc4ebcab5bf2fa46874259c` |
| docs/tasks/T-005.2/evidence/run-log.md | `f255b7c5bb0981d624a2ba85979c8ee6a44c089a` | `7ba753120e52996c90848ed07be859ec6a764e98040c9d460c4599235d2063bf` |
| docs/tasks/T-005.2/evidence/unrun-role-boundaries.md | `5972376bf4aa2a5e26f337c5888dd14a81818abf` | `5f421c5b58d3a907021eaff4f682a9dbf3bb47b147be27f81825738beab78dfe` |
| docs/tasks/T-005.2/results.md | `1efbf105f831fc9ec1aa57620fb416bb15e0bbe1` | `f97555d5e921abdfefbcdb5fc61be5cdd637eb3036aec1adc7f68773afd2f303` |

Package identities, independently computed:

| Path | SHA-256 |
|---|---|
| docs/tasks/T-005.2/preflight.md | `f7d367539891d51d1d07b428fc9953b4e10ad726446c74ad5d1af1b8b647b04d` |
| docs/tasks/T-005.2/verification.md | `85f58c81d53fc6629baaf3eb663a5b3031d48f4b63982630e51fa7b77cd4431b` |
| docs/tasks/T-005.2/results.md | `f97555d5e921abdfefbcdb5fc61be5cdd637eb3036aec1adc7f68773afd2f303` |
| docs/tasks/T-005.2/brief.md | `794247bc2477968d6394ce6bdbb9798ab6c06b96ed4d28ab7383da68ab391c77` |
| docs/tasks/T-005.2/evidence/unrun-role-boundaries.md | `5f421c5b58d3a907021eaff4f682a9dbf3bb47b147be27f81825738beab78dfe` |
| docs/tasks/T-005.2/evidence/run-log.md | `7ba753120e52996c90848ed07be859ec6a764e98040c9d460c4599235d2063bf` |
| docs/tasks/T-005.2/evidence/preparation-and-recovery-observations.md | `079c621266d77603e590ed1f8784c2fb1ca3a66cbcc4ebcab5bf2fa46874259c` |

Scope-comparison procedure: hash each existing `git ls-files` path and each
file under `.agents/`; record HEAD, `git status --short`, the staged binary
diff SHA-256, and for each staged path both `git rev-parse :<path>` and SHA-256
of `git show :<path>`. Recompute these facts before/after the sole report write
and require equality. The three OS files were separately hashed and preserved:

| Path | SHA-256 |
|---|---|
| .DS_Store | `d7fdda803578f7ea8b489dd449da62849316b0634bf1175d283a31e1a3820845` |
| docs/.DS_Store | `2d4740cf346bb2cfe93c70b6717aed1da0e4a05b42690f3587d7537cb76d8207` |
| skills/.DS_Store | `fce67661710597f67c9b69319a4afa537b05cb4dd1486cf358ae8ee8ce27ff8f` |

Exact `git status --short` immediately before the report write:

```text
A  docs/tasks/T-005.2/evidence/preparation-and-recovery-observations.md
A  docs/tasks/T-005.2/evidence/run-log.md
A  docs/tasks/T-005.2/evidence/unrun-role-boundaries.md
A  docs/tasks/T-005.2/results.md
```

Exact post-write `git status --short`, verified immediately after writing:

```text
A  docs/tasks/T-005.2/evidence/preparation-and-recovery-observations.md
A  docs/tasks/T-005.2/evidence/run-log.md
A  docs/tasks/T-005.2/evidence/unrun-role-boundaries.md
A  docs/tasks/T-005.2/results.md
?? docs/tasks/T-005.2/reviews/
```

With `--untracked-files=all`, the sole new entry is
`?? docs/tasks/T-005.2/reviews/discovery-01.md`. All pre-existing file/index
identities, OS files, HEAD and scoped staged-diff digest remained unchanged.
The report is not included in its own reviewed byte set.

## 8. Questions, unchecked work and residual risks

| Row / type | Concrete reason / implication | Owner / follow-up |
|---|---|---|
| V-01 provenance | Current files and snapshots prove existence, but the supplied raw record does not establish separate role invocations/reads. This is not an assertion they did not occur. | Coordinator supplies concrete call records; implementer corrects unsupported observation strength (F-01) |
| V-02/03/04 | Designer/preflight/entry role assessments explicitly unrun; structural tests cannot replace them | Coordinator authorizes/launches bounded calls; corresponding preparation/entry role owners supply raw outputs |
| V-05 | Both obsolete-ready checks, focused recovery, current revised proof and separate new decision unrun | Coordinator; preparation/proof/discovery/decision owners remain separate. No acceptance/advance inferred |
| V-06 | Local freshness fact reproduced; actual changed-requirement/material-change/expected-effect routing absent | Coordinator supplies role evidence; task design/decision owner owns changed requirements |
| V-07-Q | Per-call qualified installed-copy/source/helper identity and renewal receipt absent; preflight's root-artifact permission does not prove qualification | task-preflight/coordinator reconcile envelope and record current qualifications before any new campaign |
| Dependency warning | T-001.4, T-002.4, T-003.4, T-004.1–.3, INT-FLOW-001, TEST-STAB-001.1/.2 acceptance dispositions remain owed per recorded context | Coordinator + fresh per-package acceptance calls before T-005.6 ART-012 audit; commit-message labels are not artifacts |
| I-04 continuity | Submission names own chain plus prepared-ledger as parity evidence, but actual discovery/decision consumer reference observations are not retained in this submission | T-005.3 role evidence / coordinator; this report passes the real preparation references onward without retroactively proving earlier consumers |
| F-01 correction | Historical outputs must be recovered or claims downgraded; rerunning setup alone is new evidence | Implementer owns correction, fresh discovery owns corroboration; authority/authorization remains coordinator-owned |

The brief explicitly permits setup plus unrun records when further role
calls lack permission. These gaps are preserved under that fallback and are
not recorded as approved deferrals. Discovery does not decide whether this
submission is safe to advance.

## 9. Coverage completeness and next route

Coverage is **partial**: every required/material row is visible, local
identities/fixtures were corroborated, F-01 is confirmed, and real role-chain,
refusal, recovery and routing evidence remains blocked for concrete reasons.
No role compliance or overall flow qualification is declared.

Next: a **separate task-acceptance-review call on docs/tasks/T-005.2**
consumes the brief, current scoped diff, this report, V-01–V-07 and all
subrows, F-01, DISC-01/02 commands, verification revision 1, preflight
Decision context, parent evidence rules and T-005.1 dependency acceptance
context. That stage decides the disposition and the correction/evidence
route. This discovery call performs neither that decision nor advancement.

## 10. Discovery continuation

```markdown
Discovery continuation:
- Iteration / current byte identity: discovery-01, first independent pass; HEAD 9127e5923e647d178581336b687663cd2e5fb899; staged binary diff SHA-256 eba5dedd258a5e6e8b645d0709656557d8ffd7c8a97ac1f9389a02d483fbb8a4; four worktree/index SHA-256 and index blobs in §7; sole post-report delta discovery-01.md.
- Coverage rows: V-01=blocked (raw separate-call/read provenance and compact variant absent); V-01-A=pass (artifact hashes/existence only); V-02=blocked (role refusal unrun); V-03=blocked (readiness/ownership routing unrun); V-04=blocked (entry/integration/refusal roles unrun); V-05=blocked (both old-ready rejections + recovery/proof/new decision unrun); V-05-H=pass (fixture sibling history/IDs/reason); V-06=blocked (routing unrun); V-06-F=pass (local equal-status/index changed-worktree fact); V-07=fail (F-01 raw retention); V-07-U=pass (explicit unrun mapping); V-07-Q=blocked (current qualified installed-copy receipts/envelope); SCOPE=pass (preserved bytes/index; report only).
- Finding IDs: F-01, suggested P2, current confirmed retention/claim defect; no prior T-005.2 findings.
- Finding/scenario continuity: submission V-01 observed-pass remains producer-attributed, discovery blocks call provenance; submission V-07 observed-pass fails raw-retention audit; V-02/03/04/05/06 remain producer-declared role-unrun with local controls independently corroborated. Unrun ledger 1=QR-12 preparation; 2=integration leaf; 3=REV-1 design revision; 4=focused recovery/proof/new decision; 5=refusal controls; 6=prepared/direct discovery parity; 7=live/model campaign — all retain their setup/reason in unrun-role-boundaries.md and coordinator evidence/authorization ownership. Correction owner=implementer (F-01); evidence owners=coordinator plus separate producing/consuming roles, fresh discovery; authority owners=coordinator, task design for requirement changes, prerequisite/permission owners for unavailable boundaries. Sibling surfaces=recovery FEASIBLE/UNAVAILABLE, REV-1, QR-12, actual package preparation, I-04 consumer parity.
- Preparation/context: docs/tasks/T-005.2/brief.md (794247bc…91c77), verification.md revision 1 (85f58c81…4431b), preflight.md (f7d36753…7b04d), preflight Decision context, docs/tasks/T-005/brief.md evidence rules/P-01/P-02, docs/tasks/T-005.1/fixtures.md handoff manifest and reviews/acceptance-01.md; dependency-disposition warning retained.
- Reviewer regressions: no repository tests or fixtures created; repeat DISC-02 retained-capture/provenance audit and DISC-01 exact six-case command in §5 against corrected current bytes; historical re-creation alone cannot close missing original raw output.
- Aggregate gate: not run; owner=independent initial discovery; F-01 decisive targeted retention failure suppresses aggregate; role/qualification blockers remain concrete and no copied gate is admitted.
- Next: separate task-acceptance-review on docs/tasks/T-005.2 consumes current diff, this partial report, all blocked rows, F-01, regressions and preparation/context references.
```

