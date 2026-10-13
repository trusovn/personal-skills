# Task Review Discovery Report: T-005.1 — Supply reproducible qualification inputs

| Field | Value |
|---|---|
| Stage | task-review-discovery; active project-local installation |
| Coverage | complete for six leaf discovery scenarios; V-06 fails |
| Iteration / date | correction discovery 02 / 2026-10-13T13:34:07Z |
| Repository | /Users/mtrusov/work/skill-sources/personal-skills |
| Report | docs/tasks/T-005.1/reviews/discovery-02.md |
| Authority | brief.md; parent ../T-005/brief.md |
| Preparation | verification.md revision 1; preflight.md and recorded dependency override |
| Submission | results.md, corrected READY_FOR_REVIEW submission |

This report supplies evidence only: no acceptance verdict, approved deferral or
advancement. It applies only to the identified bytes and does not review or
authenticate itself. Conditional review duties remain separately owned.

## 1. Provenance

This session authored no reviewed production, test or submission bytes. Its only
repository write is this report. Project-local discovery and testing-discipline
instructions were applied. No subagent, network, model or qualification role call
ran. Prior passes guide selection; they are not current proof.

## 2. Findings

### F-02 [suggested P2] Excluded evaluator answers remain in consumer Git history

| Field | Evidence |
|---|---|
| Location | fixtures.md:1128–1140, route-cases directory/excluded change-effects/cases.json; tests/test_review_composition.py:377–405, path-only exclusion checks |
| Trigger | Stage route-cases, expand its consumer directory and remove the declared evaluator-only change-effects/cases.json worktree file. Run git show HEAD:change-effects/cases.json inside that consumer Git workspace. |
| Result / consequence | Exit 0 and identical JSON before/after exclusion, including expected routes/policies for all nine cases. A consuming role can retrieve the grading answers from its allowed .git input, compromising independent routing evidence. |
| Evidence | DISC-03 below; expanded directory includes .git objects. Fixture setup_fixture.py:1072 writes the key and staging commits it. Green manifest checks do not exercise history visibility. |
| Affected AC / invariant | AC-04, V-06, S-01 / INV-010; parent evidence rule 3: expected answers and grading oracles stay outside consumer inputs. |
| Credible sibling surface | Other directory-based consumer sets retaining Git history/index or tracked evaluator records; later T-005.5 renewal from these manifests. No claim that every sibling currently leaks. |
| Smallest corrective direction | Supply task-local consumer states that retain necessary review Git context while excluding evaluator bytes from all accessible worktree/index/history surfaces. Verify with an adversarial retrieval control; route any necessary shared-fixture repair to its owner. |

F-01 from discovery-01 is corroborated as corrected: the revised receipt includes
the complete independent comparison invocation, managed block and replacement
recheck. Preserve its history; it is not a current finding. Missing conditional
review evidence is recorded separately, not manufactured as a code defect.

## 3. Completeness ledger

Rows were selected before probes. All finite inventory identities are represented
by V-01; this leaf does not claim execution of every inherited role scenario.

| Row | AC / invariant | Cases; setup/oracle | Submitted claims | Current independent evidence | Result |
|---|---|---|---|---|---|
| V-01 | AC-01; S-01 | INV-CASE-01–24; COMP-01–05; CCR-01–08; ROUTE/FIND/ROWS/REV/EFF/GATE/DISP-01; IFQ-01–03; P-01–07 owners. Reconcile inherited authority, setup/oracle/owner/evidence and current selectors; remove each mapping as control. | N2/M2, 47 entries | DISC-01/05: real inventory clean, all 47 individual omission controls rejected; current references resolve. Static parent/owner/unrun-role reconciliation. | pass |
| V-02 | AC-01/03/04; S-01 | Fresh queue-defect, two ready tasks and two real public CLI occurrences; fresh correction-round prior MNT-B1–B4 report. Oracle: TASK-1 then empty, TASK-2 remains ready; handoff role unrun. | P1/P2, V-02 receipt | DISC-02 observed first and next persisted occurrence and reconstructed handoff. | pass |
| V-03 | AC-02; S-02 | Fresh disposable committed Git target; exact full managed set/bytes/block, canonical CLI match, target sibling helper, unmanaged preservation, independent replaced-block equality. | C2, corrected V-03 receipt | DISC-04: 86 paths, 85 copied files and block match; replaced block/check match; helper available; unmanaged prefix/app and HEAD preserved. Receipt contains reproducible procedure. | pass; F-01 corrected |
| V-04 | AC-02; S-02 | Newline mutation of fingerprint-excluded evals.json; fingerprint stable, CLI exact drift, read-only filesystem/status/HEAD snapshots, restore. | P4, V-04 receipt | DISC-04: exit 1 names only eval path; workflow fingerprint unchanged, observation snapshots equal; restored check exit 0. | pass |
| V-05 | AC-01/03; S-01 | Good/wrong inventory and manifest controls; supplied public fixture runtime; structural checks are not role proof. | N2/M2 | DISC-01 five targeted tests green, including omission/stale selector/nonexistent input/misclassified held-back controls; DISC-02 runtime. V-06 separately tests full visibility. | pass for bounded local checks |
| V-06 | AC-01/04; S-01 | Assemble all eleven sets (ten stagings plus package); recursively expand inputs, subtract evaluator paths, check unstaged positions, inspect replacement/provenance/preparation instructions. Oracle: consumer lacks answers. | Explicit manifests; independent assembly owed | DISC-02 completes all assemblies and resolution; DISC-03 retrieves route key through included Git history after exclusion. | fail; F-02 |

Inherited public/lifecycle/tamper/validator/process-cleanup/continuation obligations
remain explicitly with their case owners. No new executable schema or long-lived
process success is claimed here. Actual qualification calls remain unrun.

## 4. Adversarial checks

All 47 inventory omission variants reject. Managed eval/block drift is observed
at the real CLI and restored/replaced independently. Consumer worktree exclusion
fails against Git-history retrieval. These are distinct structural, installation
and consumer-visibility evidence; green local tests do not close F-02.

## 5. Commands and current results

Cwd for all commands: repository root. PYTHONDONTWRITEBYTECODE=1 for Python.
Only local disposable operations; no live/network/role probes.

| ID | Exact command or reproducible probe | Result / cleanup |
|---|---|---|
| DISC-01 | `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_review_composition.T0051QualificationInputTests` | 5 OK, 1.024 seconds; existing staging helper cleanup |
| DISC-02 | Python stdin driver importing test_review_composition: for each t0051_manifests staged set invoke `[sys.executable, fixture, scenario]` with a separate EVAL_WORK_ROOT under TemporaryDirectory and timeout=20; expand each consumer path recursively, subtract evaluator_only, assert not_staged_positions absent and t0051_manifest_problems(manifest, roots)==[]. For queue-defect write external state with TASK-1/TASK-2 ready and invoke `[sys.executable, staged queue-runner/src/queue/run_next.py, state]` twice with timeout=10. For correction-round require MNT-B1–B4 in prior report. | All sets resolve; audit []; expanded file counts 48/43/49/51/61/55/56/282/56/65/5 in manifest order. Public stdout TASK-1 then empty; persisted TASK-2 ready. Temporary root removed, roles unrun. |
| DISC-03 | Exact regression below | Answer key readable after consumer exclusion; F-02. Temporary root removed. |
| DISC-04 | Python stdin probe using test_install_development_skills helpers and a fresh resolved TemporaryDirectory: init_repo with unmanaged trailing-whitespace AGENTS prefix; run_installer/run_check; compare expected_managed_paths against actual .agents files plus AGENTS.md, source_projection_snapshot bytes, independent AGENTS_BEGIN/END extraction against AGENTS_BLOCK.rstrip(). Invoke target sibling run_evidence.py availability; compare resolved scripts_root. Append newline to copied evals.json; snapshot all target file SHA-256/status/HEAD; run_check and installed_identity; require precise drift, unchanged fingerprint and snapshot. Restore bytes/check. Insert tampered line before AGENTS_END; snapshot/check precise AGENTS drift/read-only state; reinstall; independently compare replaced block/prefix/suffix, app.txt and stable HEAD; check match. | 86 paths/85 bytes/block match; eval drift precisely named, fingerprint stable and read-only snapshots equal; restored match; block replacement equality; helper available; unmanaged bytes/HEAD preserved. First run stopped at raw helper path string equality (/tmp vs /private/tmp); resolved-path rerun completed. This reviewer assertion error is not a product defect. Both disposable roots removed. |
| DISC-05 | Exact omission driver below | Every one of 47 omitted IDs rejected; original clean |
| DISC-06 | `git diff --check` | exit 0; structural only |
| DISC-07 | SHA-256 comparison of protected skills/scripts/.agents files and all reviewed bytes; compare each index blob separately; git status --short | unchanged before report write |

Full installation renewal code is retained in the corrected V-03 receipt;
DISC-04 corroborates the same invariants using a unique disposable target rather
than deleting/reusing its fixed path. The owning installer suite was not rerun:
installer/source bytes did not change and decisive CLI probes were obtained.

DISC-03 regression (no repository test added):

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 - <<'PY'
import tempfile, subprocess, os, sys
from pathlib import Path
import test_review_composition as c
with tempfile.TemporaryDirectory(prefix='t0051-oracle-') as d:
    s = next(x for x in c.t0051_manifests()['staged_input_sets'] if x['staging_id']=='route-cases')
    subprocess.run([sys.executable,s['fixture'],s['scenario']],env={**os.environ,'EVAL_WORK_ROOT':d},check=True,capture_output=True,timeout=20)
    workspace = Path(d)/'route-cases'
    before = subprocess.run(['git','show','HEAD:change-effects/cases.json'],cwd=workspace,text=True,capture_output=True,timeout=10)
    (workspace/'change-effects/cases.json').unlink()
    after = subprocess.run(['git','show','HEAD:change-effects/cases.json'],cwd=workspace,text=True,capture_output=True,timeout=10)
    print(before.returncode,after.returncode,before.stdout==after.stdout)
    print(after.stdout)
PY
```

DISC-05:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 - <<'PY'
import copy
import test_review_composition as c
real=c.t0051_inventory(); expected=c.t0051_expected_ids()
assert c.t0051_audit_problems(real,expected)==[]
for cid in sorted(expected):
    degraded=copy.deepcopy(real)
    degraded['case_inventory']=[x for x in degraded['case_inventory'] if x['id']!=cid]
    assert any(cid+': missing from inventory' in p for p in c.t0051_audit_problems(degraded,expected))
print('47 omission controls rejected; real inventory clean')
PY
```

All fixture subprocesses returned synchronously, public and retrieval calls had
bounded waits, disposable roots were removed. No daemon or lifecycle fixture was
launched; no surviving fixture process or inherited pipe remained.

## 6. Aggregate gate

| Field | Value |
|---|---|
| Exact command | PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_review_composition.py |
| Status | not run |
| Owner / stage | this independent correction discovery |
| Reason | Decisive targeted V-06 failure F-02 suppresses aggregate. |
| Evidence | Five targeted tests/installation probes pass; consumer retrieval fails. Producer M2's 21-test gate is submitted evidence, not a current reviewer gate. |

No new aggregate or whole-repository command added.

## 7. Scope and baseline

Six implementation paths match results.md's allowed scope. The seventh dirty
entry, discovery-01.md, is prior reviewer context, not implementation ownership.
All seven are staged, with individual index/worktree blob equality. No unexplained
overlap. User registration/preparation was committed in HEAD 58f5179. No active
installation refresh or source/shared helper/installer change occurred.

HEAD: `58f5179284bfb51ea2ef1ceee7232ae5db80f4a9`. SHA-256 of `git diff HEAD` (including prior report context): `c5b69b6487c0f1d89108adf95bf5ce7f070771bb6c0889af88510781d4b259fc`.

| Path | Index blob = worktree blob | Worktree SHA-256 |
|---|---|---|
| docs/tasks/T-005.1/evidence/V-02-setup-reconstruction.md | `d742119b31c4845fd05f7105c4a88fe6c9f6bda1` | `e07b655511b64b50fb0a528b9e61914c9186dfd110683bb98e9e528d7df0ed4a` |
| docs/tasks/T-005.1/evidence/V-03-install-projection.md | `e10bad98ab9c650e866ba77c5e5744cf2d942880` | `83b7b2dcd473f123f62774eeaab847800035ed769926feba042ebe4e7aa920ee` |
| docs/tasks/T-005.1/evidence/V-04-drift-contrast.md | `7c9b97658db4c01c246ff762b7c483c10b142310` | `6c967a07eb0f13119f7374dbe5b3e5771573c331e0c5fd66aaf95044818ef239` |
| docs/tasks/T-005.1/fixtures.md | `07c4d9df42023a3e46f13387610defefc34bc229` | `fb7f706bd2064c8c6409d525083cbe43dc9a338ae82081431ea78da97adbef50` |
| docs/tasks/T-005.1/results.md | `517c1951605f0ebc328116e0880b876370128a85` | `98ebadb641ffdf5819f9e4f0d07cdef079c64784b8e8a0945248caf4e117d94e` |
| docs/tasks/T-005.1/reviews/discovery-01.md | `fd26a628495e610db293618c9454c907b4cb0bcf` | `e2611400d2f5fbb4c8d06717edd7d6ebba96cbfbc1eb7b69ea71577dbb62048c` |
| tests/test_review_composition.py | `ef2a8c18e6d5f9067fc6e325d4ff8ce612106e6f` | `e47d5c045b8f45ec07cff043015ff87d5aa9ea120b9c94148162567af11e0896` |

Preparation identities:

- docs/tasks/T-005.1/brief.md: `51c7a380f88cf493dd443b9e66d625609d9f10b8906eb71c723c566aa1a3b67b`.
- docs/tasks/T-005.1/verification.md: `c7aacb05306660ae92548689ea69803f1314427e1559c74e8fd25b8b8ae3d105`.
- docs/tasks/T-005.1/preflight.md: `dd2e52866fffb3845134f0c9abd2bb70f0708738c669f6dc1af1b12ed03d761d`.

Exact reviewed status immediately before write:

```text
A  docs/tasks/T-005.1/evidence/V-02-setup-reconstruction.md
A  docs/tasks/T-005.1/evidence/V-03-install-projection.md
A  docs/tasks/T-005.1/evidence/V-04-drift-contrast.md
A  docs/tasks/T-005.1/fixtures.md
A  docs/tasks/T-005.1/results.md
A  docs/tasks/T-005.1/reviews/discovery-01.md
M  tests/test_review_composition.py
```

All 416 protected file hashes remain unchanged after probes.

## 8. Conditional evidence and residual risk

- Maintainability: results.md:238–258 requires fresh separate review of significant
  new test/fixture code; no maintainability report exists. Coordinator owns this
  stage before acceptance. This discovery neither executes nor waives it.
- Dependencies: preflight's recorded user override permits this leaf while owed
  dependency decisions remain warnings. Coordinator/per-package acceptance owners
  retain those duties before T-005.6 audit; no new override here.
- Role qualification: unrun with T-005.2–.5 owners; T-005.6 owns ART-012 audit.
- F-02: task implementer owns correction, fresh discovery owns corroboration,
  coordinator owns any authority/scope routing. No unchecked assembly rows remain.

## 9. Completeness and route

Complete discovery coverage: V-01–05 pass; V-06 fails. Future qualification and
conditional duties remain separate. Next: task-local F-02 correction, applicable
separate maintainability review, fresh independent discovery. Separate acceptance
consumes the brief, scoped diff, both discovery reports, verification revision 1,
preflight/decision context, regressions and conditional evidence.

## 10. Discovery continuation

```markdown
Discovery continuation:
- Iteration / current byte identity: correction discovery 02; HEAD 58f5179284bfb51ea2ef1ceee7232ae5db80f4a9; current diff/index/worktree identities in section 7.
- Coverage rows: V-01=pass (47 identities/omissions/owners); V-02=pass (public twice plus unrun handoff); V-03=pass (full projection/receipt/F-01 regression); V-04=pass (eval drift/read-only/restoration); V-05=pass (five targeted tests/good-wrong controls); V-06=fail (Git-history answer leak/F-02).
- Finding IDs: F-01 [prior suggested P2] independently corroborated as corrected; F-02 [suggested P2] current consumer evaluator-exclusion defect.
- Finding/scenario continuity: prior V-03 fail → pass after producer C2 and DISC-04; prior V-06 unchecked → fail after producer manifest preparation and DISC-02/03; prior other passes corroborated. F-02 correction owner=task implementer, evidence owner=fresh discovery, authority owner=coordinator/brief; sibling surfaces=consumer Git index/history and directory-based handoffs. No blocked/unchecked scenario rows; absent conditional maintainability evidence and dependency warnings remain separately owed. Producer M2 is not reviewer aggregate proof.
- Preparation/context: docs/tasks/T-005.1/brief.md; verification.md revision 1; preflight.md including recorded override; parent T-005/brief.md/P-01–07; results.md correction submission; discovery-01.md history.
- Reviewer regressions: no new repository files; exact DISC-03 retrieval and DISC-05 omission commands in section 5; PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_review_composition.T0051QualificationInputTests; full projection/block-replacement/drift procedure in corrected V-03 receipt and DISC-04.
- Aggregate gate: not run; PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_review_composition.py; owner=independent correction discovery; suppressed after F-02.
- Next: task-local F-02 correction → separate applicable maintainability review → fresh independent discovery; separate acceptance retains its authority and receives all context.
```

## Post-report preservation

Exact status after write, checked against the reviewed baseline:

```text
A  docs/tasks/T-005.1/evidence/V-02-setup-reconstruction.md
A  docs/tasks/T-005.1/evidence/V-03-install-projection.md
A  docs/tasks/T-005.1/evidence/V-04-drift-contrast.md
A  docs/tasks/T-005.1/fixtures.md
A  docs/tasks/T-005.1/results.md
A  docs/tasks/T-005.1/reviews/discovery-01.md
M  tests/test_review_composition.py
?? docs/tasks/T-005.1/reviews/discovery-02.md
```

Only the new report entry differs. Reviewed bytes, index and prior report remain unchanged.
