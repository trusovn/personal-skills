# Task Review Discovery Report: T-004.2 — Read-only profile checking

| Field | Value |
|---|---|
| Producing stage | `task-review-discovery`, project-local installed skill |
| Coverage completeness | complete — V-01–V-07 and R-01–R-03 have current evidence, including failures |
| Discovery iteration | correction discovery 1, after discovery-01 F-01 |
| Created at | 2026-10-12T20:52:24+01:00 |
| Repository root | `/Users/mtrusov/work/skill-sources/personal-skills` |
| Durable report | `docs/tasks/T-004.2/reviews/discovery-02.md` |
| Task brief | `docs/tasks/T-004.2/brief.md` |
| Preparation | `docs/tasks/T-004.2/verification.md`, revision 1; `preflight.md`, ready |
| Submission | staged `docs/tasks/T-004.2/results.md`, `READY_FOR_REVIEW` |

This report publishes evidence only. It contains no acceptance verdict,
approved deferral, or advancement. It applies only to the identified reviewed
bytes. A separate acceptance decision consumes it. This report does not review
or authenticate itself.

## 1. Discovery provenance

This session authored no reviewed production, test, guidance, or submission
bytes. Evidence is independent of production authorship. Active installation:
`.agents/skills/task-implementation-flow/task-review-discovery/SKILL.md`;
its sibling report template was read. Test inspection used the project-local
`.agents/skills/testing-discipline/SKILL.md`. Neither was refreshed.

HEAD: `f6046d8b1a48f1984ad025589dca4a01c2fa87c9`.
SHA-256 of `git diff --cached --binary`:
`3fab25587100e1cff5f1a3d35178e047b4f3b08b0f1e03de9386f429a5936564`.
Every staged path was read separately from the index and worktree; bytes
matched. `git diff --name-only` was empty. No Git tree-writing command was used.

## 2. Confirmed findings

### F-02 [suggested P2] Source directory symlinks shrink the expected projection

| Field | Evidence |
|---|---|
| Current location | `scripts/install_development_skills.py:359`, `_collect_projection_files`; copy boundary at line 200 |
| Trigger | In a disposable complete source distribution, add a directory symlink `skills/project-direction/linked-reference` to a disposable directory containing `copied.txt`. Run the real positional installer, then the real `--check` from that distribution. Remove the installed `linked-reference` subtree and check again. |
| Consequence | The successful fresh installation reports exit 1 and an unexpected copied file. After deletion of that required copied subtree, exit 0 reports `match: true` and no differences. The check therefore mislabels both an exact installed projection and an incomplete one. |
| Evidence | DISC-02 / Appendix A. Install exits 0 and produces the file as regular copied content. First check: exit 1, sole difference `unexpected` at `.agents/skills/project-direction/linked-reference/copied.txt`. Second check after deletion: exit 0, true match, empty differences. Both compare only 86 paths, omitting the copied source file. |
| Affected AC | AC-01, AC-02; V-01, V-02; R-01, R-02 / INV-009 |
| Broken invariant | The expected projection must cover every file the canonical installer copies, under its existing distribution contract. |
| Credible sibling surface | Directory-linked reference, eval, or setup subtrees within any selected source package: `shutil.copytree` dereferences them, whereas `os.walk` without `followlinks` skips them. This is distinct from the preserved top-level target symlink refusals. |
| Smallest corrective direction | Make source projection enumeration account for all content the existing installer materializes, including directory-linked content, while preserving target refusal and transient-copy boundaries. Do not silently omit a source subtree or label its installed files unexpected. |

F-01 from discovery-01 is independently corroborated as corrected for its
demonstrated expected/unexpected unreadable target trees and source-side
enumeration case. Its historical failure remains in discovery-01; it is not
renumbered or carried as a current failure. F-02 is a distinct remaining
projection mismatch, not a claim that the original chmod trigger still fails.

## 3. Completeness ledger

The ledger was reconstructed from the brief, verification revision 1, and prior
continuation before behavioral probes or aggregate consideration. Producer
claims are submission evidence, not proof. Prior row IDs are preserved.

| Row ID | AC / invariant | Explicit cases and setup / oracle | Submitted evidence | Independent probe / current evidence | Result / reason |
|---|---|---|---|---|---|
| V-01 | AC-01/02/05; R-01/02 | Public positional install and check in unborn/committed repos; exit 0, true match, empty differences and full projected path count; installer-accepted linked source subtree | Fresh-install match test; all V rows claimed passed | DISC-01 normal variants pass; DISC-02 installed copied symlink subtree is reported unexpected | fail — F-02; ordinary distributions pass |
| V-02 | AC-01/02/03; R-01/02 | Changed/missing SKILL.md, reference, eval/setup, guide, helper/config/schema; missing package; owned extra; eval drift with unchanged fingerprint; all packages/shared files; exact path/category oracle | Seven family tests, fingerprint/missing-package tests; correction claims Appendix B coverage | DISC-01; DISC-03 mutates all 20 package SKILL.md files and all six shared files, changed and missing; DISC-02 deletion of copied linked subtree falsely matches | fail — F-02; regular-file cases pass |
| V-03 | AC-02/03; R-01/02 | Unselected skill/helper, other .agents content, outside-block text and all four transient patterns ignored, contrasted with owned non-transient extra | Unmanaged/transient test | DISC-01 real CLI contrast; static `_is_transient` mirrors copy ignore patterns; DISC-02 source distribution copy uses existing exclusions | pass — ownership contrast behaves as documented |
| V-04 | AC-01/02/03; R-01/02 | Changed/absent block, missing AGENTS, unmatched, duplicated and reversed markers; exact AGENTS drift or precise failure | Marker test | DISC-01 real CLI variants; parser traced through `main` | pass — absent/changed drift and malformed exit 2 |
| V-05 | AC-01/03; R-02 | Missing/non-Git/non-root target; missing source; unreadable required file, source and target directories; dangling managed entry; symlink/wrong-type refusals at roots, selected destination, shared file, guide, AGENTS; outside preservation | Failure tests and new F-01 regressions; source case controls SOURCE_REPO but exercises real collector | DISC-01 all 13 tests, none skipped; DISC-04 explicit repeated F-01 public CLI regression and real relocated missing-source CLI; DISC-03 all 14 refusal cases with snapshots | pass — F-01 triggers now exit 2 with path/scope diagnostics |
| V-06 | AC-04; R-03 | Match/drift/failure/absent in unborn/committed targets, each twice; whole-tree path/type/byte Git/evidence snapshots and source snapshots; no created .agents for absence | Snapshot test covers five combinations; producer claims Appendix B all eight | DISC-01; DISC-03 independently executes all eight combinations twice, equal output and unchanged snapshots; DISC-04 source/target snapshots for missing-source failure; static check path has no install/stage/availability/run-start calls | pass — current point-in-time read-only evidence |
| V-07 | AC-05 | Positional install and check from unrelated CWD; unmanaged preservation; source from installer location; both guides agree on scope/0/1/2/refresh semantics | Unrelated-CWD and guidance test | DISC-01 plus staged guide and CLI trace; DISC-02 relocated distribution proves location-based resolution | pass — existing invocation/ownership preserved |
| R-01 | AC-02/03; INV-009 | Full canonical managed projection | Producer maps V-01–04 | V-01–04 above | fail — F-02 omits copied source content |
| R-02 | AC-01/03; INV-009 | Truthful outcomes, ownership, precise failures | Producer maps V-01–05 | V-01–05 above | fail — F-02 gives false drift and false match |
| R-03 | AC-04; INV-009 | All result classes, both Git states, repeated checks | Producer maps V-06 | V-06 above | pass |

No required row is blocked or unchecked. No changed executable schema-validator
contract exists: managed schemas are compared as file bytes. No process-lifecycle
invariant or live/model check belongs to this task.

## 4. Adversarial state and evidence checks

| Invariant | Cases exercised | Evidence |
|---|---|---|
| Selected versus unmanaged ownership | Extra selected file versus unselected helper; all 20 packages and six shared files altered/removed | DISC-01/03, exact drift or ignored unmanaged content |
| Expected versus unexpected inaccessible subtree | Denied references and denied extra target subtree; source-side denial | DISC-01/04, scoped exit 2; historical F-01 corrected |
| Complete install projection | Installer-accepted source directory link, copied target bytes, then actual deletion of copied subtree | DISC-02, F-02; observation uses real sequential filesystem state changes |
| Read-only repetition | Eight repository/result combinations, two consecutive CLI calls each | DISC-03, identical results and file/Git/evidence/source snapshots |

## 5. Independent commands and results

All probes ran locally from the repository root with
`PYTHONDONTWRITEBYTECODE=1`, Python 3.14.6, non-root uid 501. No network,
dependency installation, privileged action, active skill refresh, test edits,
or production mutation occurred. Installation was setup only in disposable
targets. Subprocesses returned and all temporary trees were cleaned; chmod
denials were restored in `finally` blocks. There are no fixture servers or
background process groups in these probes.

| ID | Exact command / reproducible probe | Purpose / result | Side effects / independence |
|---|---|---|---|
| DISC-01 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py -k check_` | 13 tests OK, 7.314s, no skips; current V-01–07 submitted cases rerun | Test temporary fixtures cleaned; current reviewer-owned execution |
| DISC-02 | `PYTHONDONTWRITEBYTECODE=1 python3 -` with Appendix A | Successful install; fresh check exit 1 / unexpected copied file; deleted subtree then exit 0 / match; F-02 | Full copied source distribution and Git target under TemporaryDirectory; cleaned |
| DISC-03 | `PYTHONDONTWRITEBYTECODE=1 python3 -` with Appendix B | Exit 0; 52 exact changed/missing mutations, 14 refusal cases, eight repeated snapshot combinations all passed | Uses existing fixture helpers; no reviewed bytes modified; cleaned |
| DISC-04 | `PYTHONDONTWRITEBYTECODE=1 python3 -` with Appendix C | Exit 0; both F-01 target regressions correctly exit 2 twice; restored baseline matches; real missing-source check exits 2 with unchanged source/target | Permissions restored before cleanup; no fabricated check result |
| DISC-05 | `git diff --name-only`; `git ls-files --stage README.md scripts/install_development_skills.py skills/README.md tests/test_install_development_skills.py`; independently read `git show :<path>` and worktree bytes for every staged path, hash both; hash `git diff --cached --binary`; hash preparation files | No unstaged diff; seven index/worktree byte comparisons equal; identities below | Read-only Git commands; no tree/index writes |
| DISC-06 | `git diff --cached --check` | Exit 0; formatting check only, not behavioral evidence | No writes |

## 6. Aggregate-gate record

| Field | Value |
|---|---|
| Exact command | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py` |
| Status | not run |
| Owner / stage | this independent reviewer, correction discovery |
| Reason | Decisive targeted failure DISC-02 / F-02 suppresses the aggregate; independent safe sibling probes continued. |
| Current evidence | DISC-01/03/04 are green for regular projection and F-01; DISC-02 fails full projection. Producer's 30-test suite claim and prior maintainability targeted run are not this discovery's gate. |

No gate or command was added. A future correction discovery owns the existing
installer aggregate after all current targeted regressions are clean. This
record waives no conditional stage duties.

## 7. Scope and baseline comparison

The four production/test/guide paths are brief-authorized. Results and the two
staged reports are task submission/history context, not unrelated user work
or current behavioral proof. There is no unexplained overlap. The staged
maintainability-01 implementation blobs match current index identities.
Preflight HEAD `93cd0e4` precedes current preparation HEAD `f6046d8`, as already
recorded by the submission/prior discovery. No plan or preparation was changed.

| Path | Index blob | Index and independently read worktree SHA-256 (equal) |
|---|---|---|
| README.md | `442906e38f2ee8d8b0d460fbbbe852ebc0cbeb88` | `61172bc35448f5fb236aa3d58527e0a7333721485395f8a7bdf541e03313fbd1` |
| docs/tasks/T-004.2/results.md | `28366cd99593399c2dbc46c524f5348ca6173a4d` | `24cc4224352a4a93f9aa6f6810f3dc459dd71d71e1e1ec3788b2f97e8a50e5b9` |
| docs/tasks/T-004.2/reviews/discovery-01.md | `caa680abed8e73abcb183f3f2396f706da27edba` | `3894d340174d81e5daef778c83e05ce96f394d56a03ab071bc81b27f6d3a0607` |
| docs/tasks/T-004.2/reviews/maintainability-01.md | `e1ec29948a4ee47bedd5d9afa7a01a8d1ed86530` | `555e42891ffe3e63afd6d6bf750ec5ecce10a929fa18f8b96bb8f8ba3e63c53a` |
| scripts/install_development_skills.py | `a925d0438b9e735ff5815cd12f013aa556b28d4c` | `ea8634c8097c142f2a496d6c53f2ab0ff47fa21bde9864dfaec9134a40bde1a5` |
| skills/README.md | `39cad5358292a8f88eb0acdd6034fcee60b30814` | `e48a41d12e83192f5127f656a62f012a26736d156ef1be222b77f9f50ae6ef5c` |
| tests/test_install_development_skills.py | `e3092e09628fc8355b1c47b3e2d5bcf6bfe1860a` | `9578304262f4513b29ab66e4a03cab040e751a0dbcc71102b160b4f5c6a76123` |

Preparation SHA-256 values agree with the submission:

- brief: `ecf57bb5cb33dda3405269c3f6adf05628248d2a4510fe34358d98d8e027512e`.
- verification revision 1: `4966f69350e20d8563532d172e26acb6a8536e0c64635a62be0fb11f393c24b8`.
- preflight: `8f8af39476e7d6d7960b9f3f0e14efe766383dee54d64db784445ee882c40d1b`.

Exact status immediately before writing (`git status --short --untracked-files=all`):

```text
M  README.md
A  docs/tasks/T-004.2/results.md
A  docs/tasks/T-004.2/reviews/discovery-01.md
A  docs/tasks/T-004.2/reviews/maintainability-01.md
M  scripts/install_development_skills.py
M  skills/README.md
M  tests/test_install_development_skills.py
```

Post-write status, verified after creating this report:

```text
M  README.md
A  docs/tasks/T-004.2/results.md
A  docs/tasks/T-004.2/reviews/discovery-01.md
A  docs/tasks/T-004.2/reviews/maintainability-01.md
M  scripts/install_development_skills.py
M  skills/README.md
M  tests/test_install_development_skills.py
?? docs/tasks/T-004.2/reviews/discovery-02.md
```

Only the new report differs; staged diff and reviewed worktree bytes remain
unchanged. No restaging, reset, commit, or ownership change occurred.

## 8. Questions, unchecked work, and residual risks

No required row is blocked or unchecked. The linked-source case is a confirmed
failure, not a residual risk. Snapshots prove observed state preservation, not
absence of a write that fully undoes itself; the static check call path provides
complementary evidence. This is local platform evidence, not cross-platform
qualification. No source symlink currently needs to exist in this repository
for the installer-accepted distribution case to demonstrate F-02.

Preflight notes no separate T-004.1 acceptance report; the brief explicitly
declares that dependency reviewed. No new dependency decision is made here.
No separate ART-003 decision-context file is packaged; context is the brief's
finite R-01–03 matrix and cited project plan ART-009–011, IF-007, INV-009,
FLOW-004. Refresh composition belongs to T-004.3; installed skill-call
qualification belongs to T-005.

## 9. Completeness and next route

Coverage is complete with F-02 and independently corrected F-01. Next: separate
`task-acceptance-review` with this report, brief, current staged diff, results,
verification revision 1, ready preflight, cited decision context, prior discovery
and maintainability reports, and Appendices A–C. No blocked/unchecked rows exist.
This route does not itself decide acceptance or authorize a correction.

## 10. Discovery continuation

```text
Discovery continuation:
- Iteration / current byte identity: correction discovery 1; HEAD f6046d8b1a48f1984ad025589dca4a01c2fa87c9; staged binary diff SHA-256 3fab25587100e1cff5f1a3d35178e047b4f3b08b0f1e03de9386f429a5936564; all seven staged paths equal worktree bytes.
- Coverage rows: V-01 fail F-02; V-02 fail F-02; V-03 pass; V-04 pass; V-05 pass; V-06 pass; V-07 pass; R-01 fail F-02; R-02 fail F-02; R-03 pass. No blocked/unchecked rows.
- Finding IDs: F-01 historical P2, demonstrated triggers now corrected; F-02 current suggested P2, installer-copied linked source directories omitted from expected projection.
- Finding/scenario continuity: prior V-01/03/04/06/07 pass, V-02/05 and R-01/02 fail F-01, R-03 pass. Producer claims corrected F-01 and all rows passed in results.md; current DISC-01/03/04 corroborate F-01 and regular projection, DISC-02 disproves V-01/02 full projection. No incomplete rows. Correction owner: implementer after decision route; evidence owner: fresh discovery; authority/decision owner: separate acceptance. Influenced siblings: directory-linked references/evals/setup in all selected source packages; retain unreadable expected/unexpected source/target and unsafe target-root regressions.
- Preparation/context: docs/tasks/T-004.2/brief.md; verification.md revision 1; ready preflight.md; brief R-01–03 and cited project-plan ART-009–011/IF-007/INV-009/FLOW-004; current maintainability-01 and prior discovery-01.
- Reviewer regressions: no test edits; run PYTHONDONTWRITEBYTECODE=1 python3 - with discovery-02 Appendices A–C; corrected Appendix A oracle requires fresh installed linked-source contents to match and their deletion to report exact missing drift; preserve Appendix C scoped exit-2 denial oracles and Appendix B siblings. Targeted command: PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py -k check_.
- Aggregate gate: not run; independent correction-discovery owner; DISC-02 F-02 suppresses PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py. Future correction discovery owns it after clean targeted evidence.
- Next: separate task-acceptance-review with the complete scoped diff and package/report context above.
```

## Appendix A — DISC-02 exact probe body

Run `PYTHONDONTWRITEBYTECODE=1 python3 -` from the repository root. Printed
results demonstrate the failure; the script's exit 0 is not a behavioral pass.

```python
import importlib.util, tempfile, subprocess, sys, shutil, json
from pathlib import Path
spec=importlib.util.spec_from_file_location('fixture','tests/test_install_development_skills.py'); t=importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
with tempfile.TemporaryDirectory() as td:
    base=Path(td); source=base/'source'; source.mkdir()
    for _, rel in t.installer.DEVELOPMENT_SKILL_SOURCES:
        shutil.copytree(t.ROOT/rel,source/rel,ignore=shutil.ignore_patterns(*t.installer.TRANSIENT_PATTERNS))
    (source/'scripts').mkdir()
    for name in (*t.installer.SHARED_SCRIPT_FILES,'install_development_skills.py'):
        shutil.copy2(t.ROOT/'scripts'/name,source/'scripts'/name)
    shutil.copy2(t.ROOT/'skills/README.md',source/'skills/README.md')
    outside=base/'outside'; outside.mkdir(); (outside/'copied.txt').write_text('copied source bytes\n')
    (source/'skills/project-direction/linked-reference').symlink_to(outside,target_is_directory=True)
    repo=base/'target'; repo.mkdir(); t.init_repo(repo)
    cli=source/'scripts/install_development_skills.py'
    def call(*args): return subprocess.run([sys.executable,str(cli),*map(str,args)],capture_output=True,text=True,timeout=30)
    r=call(repo); assert r.returncode==0,r.stderr
    installed=repo/'.agents/skills/project-direction/linked-reference/copied.txt'
    assert installed.read_text()=='copied source bytes\n'
    r=call('--check',repo); print('fresh-install-linked-source',r.returncode,r.stdout.strip(),r.stderr.strip())
    shutil.rmtree(installed.parent)
    r=call('--check',repo); print('omitted-copied-subtree',r.returncode,r.stdout.strip(),r.stderr.strip())
print('all disposable fixtures cleaned')
```

## Appendix B — DISC-03 exact probe body

Run `PYTHONDONTWRITEBYTECODE=1 python3 -` from the repository root. Reuses
the prior exact sibling probe against current bytes, not its prior result.

```python
from pathlib import Path
text=Path('docs/tasks/T-004.2/reviews/discovery-01.md').read_text()
body=text.split('## Appendix B')[1].split('```python\n')[1].split('```')[0]
exec(compile(body,'discovery-01-appendix-B','exec'))
```

## Appendix C — DISC-04 exact probe body

Run `PYTHONDONTWRITEBYTECODE=1 python3 -` from the repository root.

```python
import importlib.util, tempfile, shutil, subprocess, sys, os, json
from pathlib import Path
spec=importlib.util.spec_from_file_location('fixture','tests/test_install_development_skills.py'); t=importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
print('python',sys.version.split()[0],'uid',os.geteuid())
with tempfile.TemporaryDirectory() as td:
    base=Path(td); repo=base/'target'; repo.mkdir(); t.init_repo(repo)
    assert t.run_installer(repo).returncode==0
    extra=repo/'.agents/skills/project-direction/reviewer-unreadable'; extra.mkdir(); (extra/'extra.txt').write_bytes(b'extra owned bytes\n')
    assert t.run_check(repo).returncode==1
    for denied in (extra,repo/'.agents/skills/project-direction/references'):
        mode=denied.stat().st_mode & 0o777; denied.chmod(0)
        try:
            a=t.run_check(repo); b=t.run_check(repo)
            assert a.returncode==b.returncode==2 and a.stdout==b.stdout==''
            assert 'cannot enumerate installed skill directory' in a.stderr and str(denied) in a.stderr
            assert a.stderr==b.stderr
            print('F-01 regression',denied.name,'exit 2, scoped diagnostic, repeated agreement')
        finally: denied.chmod(mode)
    shutil.rmtree(extra); assert t.run_check(repo).returncode==0
    source=base/'source'; (source/'scripts').mkdir(parents=True); cli=source/'scripts/install_development_skills.py'; shutil.copy2(t.INSTALLER_PATH,cli)
    before=t.snapshot_tree(source); target_before=t.snapshot_tree(repo)
    r=subprocess.run([sys.executable,str(cli),'--check',str(repo)],capture_output=True,text=True,timeout=30)
    assert r.returncode==2 and r.stdout=='' and 'source repository is missing development-profile inputs' in r.stderr
    assert before==t.snapshot_tree(source) and target_before==t.snapshot_tree(repo)
    print('missing relocated source: real CLI exit 2; source and target unchanged')
print('all disposable fixtures cleaned')
```
