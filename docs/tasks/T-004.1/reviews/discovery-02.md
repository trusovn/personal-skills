# Task Review Discovery Report: T-004.1 — Install the development profile in genuine unborn repositories

| Field | Value |
|---|---|
| Producing stage | task-review-discovery; project-local installed skill |
| Coverage completeness | complete — V-01–V-08 have current passing evidence |
| Discovery iteration | correction discovery 1; second independent report |
| Created at | 2026-10-12T19:47:31.953554+01:00 |
| Repository root | /Users/mtrusov/work/skill-sources/personal-skills |
| Durable report path | docs/tasks/T-004.1/reviews/discovery-02.md |
| Task brief | docs/tasks/T-004.1/brief.md |
| Verification / context | verification.md revision 1; preflight.md; docs/project-plan.md sections 1–2, IF-004/007, FLOW-004, section 11; docs/tasks/T-004/brief.md; docs/task-map.json |
| Current submission | docs/tasks/T-004.1/implementation.md, correction round READY_FOR_REVIEW |
| Previous discovery | docs/tasks/T-004.1/reviews/discovery-01.md |

This report publishes evidence only. It gives no acceptance verdict, approved
deferral, or advancement. It applies only to the identified reviewed staged
bytes. Corrections require fresh evidence. It does not review or authenticate
itself or the historical report.

## 1. Discovery provenance

This session authored no reviewed production or test bytes. All current
behavioral probes below were run by this independent discovery session. The user
interrupted after CD-03 and then requested continuation. CD-01–CD-03 had
completed; no running command was abandoned. The exact status and byte identity
remained unchanged on continuation.

Active skills were the matching project-local task-review-discovery and
testing-discipline installations under .agents/skills/. No installation refresh,
subagent, external reviewer, network call, model call, reset, restage, commit,
or production/test write occurred. The sole repository write is this report.

HEAD: `9712879568751c16d6eff79d1977768b866c2dd1`.
Staged binary diff SHA-256: `9e629e82863caafffe5931ea4c7327b90f6eb008e4dccdd70a6db56053035d76`.
Index and worktree were compared separately, not inferred from short status.
All eight staged paths match their worktree blobs. All six implementation paths
also match the producer's correction finish snapshot
`7cbd6fceac107f1846c5a04ae375da8a54fd6e6c`.

## 2. Findings and correction continuity

No findings.

Prior F-01 [suggested P2] concerned fatal branch-ref lookup failures being
classified as unborn success. Current CD-04 independently rejects that trigger:
copied identity and availability exit 2; availability reports
`available: false`, `reason: workflow_unavailable`, with the injected Git
failure cause. The existing-ref control also remains an error. Genuine
missing-ref unborn success remains available.

The sibling surfaces named in discovery-01 were exercised: source identity,
copied identity, copied final availability, and the canonical installer's staged
availability gate, on both committed and genuine unborn targets. The staged
gate rejects the error and removes its temporary staging directory. A normal
canonical install executes both staged and final gates successfully (CD-02).

Correction direction addressed the invariant rather than one demonstrated
field: status 0 means the branch exists; status 1 confirms absence; every other
lookup status raises a Git error. The owning tests control only the Git lookup
boundary or PATH Git subprocesses. They do not replace identity or availability
logic. Existing malformed-HEAD and detached behavior remains separately covered.

F-01's prior failure is retained as historical evidence. Its corrected trigger
is not reproduced on the current bytes. This is an evidence disposition, not an
acceptance decision or approved deferral.

## 3. Completeness ledger

The prior V-01–V-08 identities are preserved. Brief AC-01–AC-04 and finite risks
R-01/R-02 were reconciled with verification revision 1 before the aggregate.
Producer checks are claims; prior passes are navigation context.

| Row | AC / invariant | Explicit cases; setup / oracle | Submitted evidence | Independent probe / current evidence | Result / reason |
|---|---|---|---|---|---|
| V-01 | AC-01/02; R-01 | Real git init, complete source inputs, no commit; canonical installer and copied identity/availability; original symbolic HEAD and recursive Git object path/byte inventory unchanged | C-R and C-W/C-R2/C-I claim success; historical F fail-first record | CD-02: installed success, final available=true, null commit, actual unborn branch, no created objects; CD-04 genuine absence control passes | pass — observed at installed public boundary |
| V-02 | AC-02; R-01 | Known attached and detached commit; canonical install and copied CLIs; actual commit and attachment must persist | Existing W/I and correction C-R control | CD-02 performs canonical installation and copied identity/availability in both states; CD-04 existing-ref control rejects failed HEAD resolution | pass — actual identities and existing error behavior persist |
| V-03 | AC-02; R-01 | Invalid Git target with complete copied package/tools; committed target with failed HEAD resolution plus existing/fatal ref lookup; genuine unborn target with fatal lookup; errors must remain failures | C-F reproduces prior defect; C-R/C-TW/C-TR claim correction; prior discovery fail F-01 | CD-01 three focused tests pass; CD-02 invalid target rejected by all three CLIs; CD-04 source, copied CLIs and staged gate reject fatal errors; cause preserved | pass — prior F-01 trigger and explicit sibling cases no longer yield unborn success |
| V-04 | AC-03; R-02 | Known fixture; unchanged fingerprint compared with pre-change HEAD algorithm; included tracked edit and untracked Unicode file; root evals/tests, nested cache/node_modules, .DS_Store/.pyc; repeated/reversed enumeration | C-W; fingerprint functions unchanged | CD-03 runs HEAD reference and current functions on same fixture, isolated selection transformations and reversed discovery | pass — framing, selection and ordering compatibility observed |
| V-05 | AC-03; R-02 | Independent included relative-path/byte comparison; standalone and project-local copies with and without .agents ignored; exclude empty-package hash | C-W copied-layout tests; C-I projection | CD-03 invokes copied identity CLIs in all three layout/ignore variants and checks exact included byte equality | pass — location/ignore independence and nonempty equal fingerprints |
| V-06 | AC-02/03; R-02 | Successful installed unborn target; actual first then later unrelated commits; package byte inventory, fingerprint, HEAD and copied availability after each | C-W/C-I transition evidence; C-R unborn control | CD-02 executes both real commits sequentially and checks identity/availability plus unchanged package bytes/fingerprint each time | pass — current commit tracks Git while fingerprint stays fixed |
| V-07 | AC-04 | Target with custom skill/script/other .agents files, application files and outside-block AGENTS text; exact source projection using current manifest/transient exclusions; unmanaged bytes preserved | C-I and unchanged installer selection/helper manifest | CD-02 compares all selected packages, every shared helper including corrected workflow_version.py, managed guide, and unmanaged bytes/text | pass — current helper distributed; ownership unchanged |
| V-08 | AC-04 | Guidance compared with exercised installation/identity/availability interfaces; no full collector lifecycle claim | Correction handoff says documented Git-error guarantee now satisfied; prior discovery fail F-01 | README.md:94–96, :177–179, :192–196, :209–212; skills/README.md:6–8; flow README reviewed; CD-02/CD-04 substantiate interfaces/error claim; run_evidence.py:281/289 still needs HEAD | pass — prior contradictory error behavior corrected; collector exclusion accurate |

No required/material row is blocked or unchecked. Every AC and finite risk is
represented. No executable schema supplies a material oracle for this change:
the runtime-context schema is unchanged and is not the unborn/error-classification
contract. No process-lifecycle behavior is claimed. Public calls are bounded,
synchronous CLI subprocesses; no persistent process fixture was started.

Historical fail-first chronology remains producer-attributed. The correction
manifest records fail-first exit 1 and corrected regression exit 0 with the
intended scenario. These records were inspected, not authenticated. Current
behavior was independently observed rather than inferred from those records.

## 4. Adversarial state and evidence checks

| Invariant | Cases exercised | Current evidence |
|---|---|---|
| R-01 truthful Git identity | Genuine unborn, attached, detached, actual invalid Git target | CD-02 pass |
| Missing ref versus failed lookup | Existing-ref control; fatal lookup on committed and unborn targets; normal unborn absence | CD-01/CD-04 pass; failure cause preserved |
| Identity/availability public wiring | Source identity, copied identity/availability, canonical staged gate; normal staged and final success | CD-02/CD-04 pass |
| R-02 commit independence | Unborn → first → later real unrelated commit; installed package bytes unchanged | CD-02 pass |
| R-02 fingerprint compatibility | Pre-change reference, Unicode/include changes, six exclusions, repeated/reversed enumeration, three layout/ignore variants | CD-03 pass |
| AC-04 narrow ownership | All selected packages, guide/helpers, unmanaged files and AGENTS text | CD-02 pass |

No broader matrix, persistent process probe, collector lifecycle, profile
checker, refresh-composition probe, or installed agent-call qualification is
added by this review.

## 5. Independent probes and command records

Commands ran from the repository root. Python probes set
PYTHONDONTWRITEBYTECODE=1. Public calls in reviewer code use 20-second timeouts;
the replay launchers use a 60-second outer bound. TemporaryDirectory cleanup
completed. Synchronous children returned and inherited pipes closed; no
persistent fixture process was created or remains.

CD-02 and CD-03 replay the exact code recorded in discovery-01 sections DISC-02
and DISC-04 using current bytes. Their launchers below identify those sections
unambiguously. The frozen historical file blob is recorded in section 7.
CD-04 is the corrected DISC-05 reviewer regression plus its explicitly named
source/staged/unborn sibling checks. No repository regression file was added.

### CD-01

Exact command (repository root):

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_workflow_version.UnbornWorkflowVersionTests.test_failed_branch_ref_lookup_is_not_reported_as_unborn test_workflow_version.UnbornWorkflowVersionTests.test_existing_branch_ref_keeps_head_resolution_failure test_run_evidence.RunEvidenceTests.test_availability_reports_failure_for_fatal_ref_lookups
```

Observed exit 0:

```text
...
----------------------------------------------------------------------
Ran 3 tests in 0.694s

OK
```

### CD-02

Exact command (repository root):

```sh
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import re, subprocess, sys
from pathlib import Path
report=Path('docs/tasks/T-004.1/reviews/discovery-01.md').read_text()
section=report.split('### DISC-02\n',1)[1].split('\n### DISC-03',1)[0]
command=re.search(r'```sh\n(.*?)\n```',section,re.S).group(1)
code=command.split("<<'PY'\n",1)[1].rsplit('\nPY',1)[0]
result=subprocess.run([sys.executable,'-'],input=code,text=True,timeout=60)
raise SystemExit(result.returncode)
PY
```

Observed exit 0:

```text
V-01/V-07 PASS: real unborn canonical+final availability, null identity, recursive object inventory unchanged, exact managed projection, preserved unmanaged bytes
V-06 PASS: first actual HEAD, final availability, unchanged package/fingerprint
V-06 PASS: later actual HEAD, final availability, unchanged package/fingerprint
V-02 PASS: attached canonical install + actual identity + final availability
V-02 PASS: detached canonical install + actual identity + final availability
V-03 PASS: real invalid Git target rejected by canonical install and complete copied identity/availability tools
Cleanup PASS: synchronous children finished; all disposable directories removed
```

### CD-03

Exact command (repository root):

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 - <<'PY'
import re, subprocess, sys
from pathlib import Path
report=Path('docs/tasks/T-004.1/reviews/discovery-01.md').read_text()
section=report.split('### DISC-04\n',1)[1].split('\n### DISC-05',1)[0]
command=re.search(r'```sh\n(.*?)\n```',section,re.S).group(1)
code=command.split("<<'PY'\n",1)[1].rsplit('\nPY',1)[0]
result=subprocess.run([sys.executable,'-'],input=code,text=True,timeout=60)
raise SystemExit(result.returncode)
PY
```

Observed exit 0:

```text
V-04 PASS: baseline algorithm compatibility, included tracked/Unicode, all six exclusion dimensions, repeated/reversed discovery
V-05 PASS: standalone ignored=False independent included byte equality; nonempty identical fingerprint
V-05 PASS: project-local ignored=False independent included byte equality; nonempty identical fingerprint
V-05 PASS: project-local ignored=True independent included byte equality; nonempty identical fingerprint
Cleanup: synchronous children completed, all temporary repos removed
```

### CD-04

Exact command (repository root):

```sh
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import importlib.util,json,os,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path.cwd(); real_git=shutil.which('git')
def run(*args,env=None,cwd=None):
    return subprocess.run([str(a) for a in args],capture_output=True,text=True,env=env,cwd=cwd,timeout=20)
def git(repo,*args):
    p=run(real_git,'-C',repo,*args); assert p.returncode==0,p.stderr
    return p.stdout.strip()
with tempfile.TemporaryDirectory() as td:
    base=Path(td); wrapper=base/'bin'; wrapper.mkdir(); shim=wrapper/'git'
    shim.write_text('#!'+sys.executable+'\nimport os,sys\nargs=sys.argv[1:]\nif args[2:]==["rev-parse","HEAD"] or (os.environ.get("FAIL_SHOW_REF")=="1" and args[2:] and args[2]=="show-ref"):\n print("fatal: controlled ref-database I/O failure",file=sys.stderr)\n sys.exit(128)\nos.execv('+repr(real_git)+',['+repr(real_git)+']+args)\n')
    shim.chmod(0o755)
    env=dict(os.environ,PATH=str(wrapper)+os.pathsep+os.environ['PATH'],PYTHONDONTWRITEBYTECODE='1')
    spec=importlib.util.spec_from_file_location('source_workflow',ROOT/'scripts/workflow_version.py')
    source=importlib.util.module_from_spec(spec); spec.loader.exec_module(source)
    for committed in (True,False):
        repo=base/('committed' if committed else 'unborn'); repo.mkdir()
        git(repo,'init','-q'); git(repo,'config','user.email','discovery@example.com'); git(repo,'config','user.name','Discovery')
        (repo/'app').write_text('app\n')
        if committed:
            git(repo,'add','.'); git(repo,'commit','-qm','real commit')
        actual=git(repo,'rev-parse','HEAD') if committed else None
        p=run(sys.executable,ROOT/'scripts/install_development_skills.py',repo)
        assert p.returncode==0,p.stderr
        source_skill=repo/'skills/bounded-task-implementer'; source_skill.mkdir(parents=True)
        (source_skill/'SKILL.md').write_text('---\nname: bounded-task-implementer\ndescription: probe\n---\nbody\n')
        for mode in (('0','1') if committed else ('1',)):
            env['FAIL_SHOW_REF']=mode
            for name,args in [('workflow_version.py',('bounded-task-implementer',)),('run_evidence.py',('--repo',repo,'availability'))]:
                p=run(sys.executable,repo/'.agents/scripts'/name,*args,env=env)
                assert p.returncode==2,(name,p.stdout,p.stderr)
                if name=='workflow_version.py':
                    assert 'controlled ref-database I/O failure' in p.stderr
                else:
                    data=json.loads(p.stdout)
                    assert data['available'] is False and data['reason']=='workflow_unavailable'
                    assert 'controlled ref-database I/O failure' in data['error']
                print('REGRESSION PASS:',repo.name,'mode='+mode,name,'rc=2')
            original=os.environ.copy()
            try:
                os.environ.update(env)
                try:
                    source.get_workflow_version(repo,'bounded-task-implementer')
                except source.WorkflowVersionError as exc:
                    assert 'controlled ref-database I/O failure' in str(exc)
                else:
                    raise AssertionError('source identity swallowed Git failure')
            finally:
                os.environ.clear(); os.environ.update(original)
            p=run(sys.executable,ROOT/'scripts/install_development_skills.py',repo,env=env)
            assert p.returncode==2 and 'staged run-evidence availability failed' in p.stderr,p
            assert 'controlled ref-database I/O failure' in p.stderr
            assert not list((repo/'.agents').glob('.development-install-*'))
            print('SIBLING PASS:',repo.name,'mode='+mode,'source identity and canonical staged gate reject error; staging cleaned')
        assert (git(repo,'rev-parse','HEAD') if committed else None)==actual
        if not committed:
            assert run(real_git,'-C',repo,'rev-parse','--verify','HEAD').returncode!=0
            p=run(sys.executable,repo/'.agents/scripts/workflow_version.py','bounded-task-implementer')
            assert p.returncode==0 and json.loads(p.stdout)['repository_commit'] is None
            p=run(sys.executable,repo/'.agents/scripts/run_evidence.py','--repo',repo,'availability')
            assert p.returncode==0 and json.loads(p.stdout)['available'] is True
            print('UNBORN CONTROL PASS: genuine absence remains successful identity and final availability')
print('Cleanup PASS: bounded synchronous children finished; temporary repos and wrapper removed')
PY
```

Observed exit 0:

```text
REGRESSION PASS: committed mode=0 workflow_version.py rc=2
REGRESSION PASS: committed mode=0 run_evidence.py rc=2
SIBLING PASS: committed mode=0 source identity and canonical staged gate reject error; staging cleaned
REGRESSION PASS: committed mode=1 workflow_version.py rc=2
REGRESSION PASS: committed mode=1 run_evidence.py rc=2
SIBLING PASS: committed mode=1 source identity and canonical staged gate reject error; staging cleaned
REGRESSION PASS: unborn mode=1 workflow_version.py rc=2
REGRESSION PASS: unborn mode=1 run_evidence.py rc=2
SIBLING PASS: unborn mode=1 source identity and canonical staged gate reject error; staging cleaned
UNBORN CONTROL PASS: genuine absence remains successful identity and final availability
Cleanup PASS: bounded synchronous children finished; temporary repos and wrapper removed
```

### CD-05 — assigned aggregate

Exact command:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_install_development_skills test_workflow_version test_run_evidence
```

Observed exit 0: 54 tests ran in 8.995 seconds, OK. This was the only aggregate
execution in this correction discovery.

### Read-only preparation and identity records

Read the active skill/template, testing-discipline, AGENTS.md, task brief,
verification, preflight, submission, historical discovery, scoped cached diff,
owning test cases, identity/availability functions, installer projection and
ownership code, parent brief, and relevant plan/task-map context.

Exact principal read/check commands:

```sh
git status --short
git diff --cached --stat
git diff --cached -- scripts/workflow_version.py README.md skills/README.md
git diff --cached -- tests/test_workflow_version.py tests/test_run_evidence.py tests/test_install_development_skills.py
git diff --cached --check
```

The formatting-only check reports a trailing blank line in the already-staged
historical discovery-01.md at line 481 (exit 2). It is not a behavioral gate or
a new implementation finding; the historical artifact was preserved. It
does not supply behavioral evidence.

Read the correction manifest:
`.git/personal-skills/run-evidence/runs/run-20261012T160101Z-11ff08a7052a/manifest.json`.
It contains seven submitted checks: fail-first exit 1, reviewer regression exit
0, two targeted checks exit 0, and three owning suites exit 0. Finish snapshot
is `7cbd6fceac107f1846c5a04ae375da8a54fd6e6c`.
Each implementation path was independently compared using:

```text
git rev-parse HEAD
git diff --cached --binary
git rev-parse HEAD:<path>
git rev-parse :<path>
git hash-object <path>
git rev-parse 7cbd6fceac107f1846c5a04ae375da8a54fd6e6c:<path>
```

SHA-256 was computed directly from subprocess output for the binary diff.
These read-only identity operations neither write a tree nor modify the index.
No required command remained unrun; no network, whole-repo, slow or privileged
gate was used.

## 6. Aggregate-gate record

| Field | Value |
|---|---|
| Exact command | PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_install_development_skills test_workflow_version test_run_evidence |
| Status | passed |
| Owner / stage | This independent correction discovery session |
| Reason | All eight authority rows have current clean targeted/static evidence; F-01 reviewer regression and named sibling surfaces rerun; no selected probe remains; correction discovery owns this gate under IF-004 and verification revision 1 |
| Current evidence | CD-01–CD-04 clean; CD-05 exit 0, 54 tests OK in 8.995 seconds |

Prior discovery correctly suppressed its aggregate after F-01. This report owns
a new execution on corrected bytes; it does not copy a prior pass. No omitted
material row was identified after reconciliation. Conditional stage duties
are not waived by this gate.

## 7. Scope and baseline comparison

All six implementation paths are allowed by the leaf brief. The two additional
staged paths are the supplied current submission and historical discovery
artifact. Neither is claimed as production owned by this discovery session.
No unexplained user-work overlap is present.

Compared with discovery-01, README.md, skills/README.md, and installer test blobs
are unchanged. The workflow helper and its identity/availability tests have
the explained correction deltas; implementation.md has the correction handoff.
The historical discovery file is preserved. The installer selection,
PROFILE_SKILLS_README, SHARED_SCRIPT_FILES and ownership implementation are
unchanged and still distribute the changed helper (CD-02).

| Path | HEAD blob | Index blob | Worktree blob |
|---|---|---|---|
| README.md | 2d8e11e74fe6acbf3df213f3ceaa535af7495554 | db87a49ddb6aae85dc851cf99a0e298519b71d28 | db87a49ddb6aae85dc851cf99a0e298519b71d28 |
| docs/tasks/T-004.1/implementation.md | absent | 481a9d54ccde763576b3d0d2f575a90088a4e2e7 | 481a9d54ccde763576b3d0d2f575a90088a4e2e7 |
| docs/tasks/T-004.1/reviews/discovery-01.md | absent | 2d47ea2f8dddb4745ac741284f8252541c1d1c14 | 2d47ea2f8dddb4745ac741284f8252541c1d1c14 |
| scripts/workflow_version.py | 1052d63ef66e8cb39f47b20dff759e7608dc11ae | 3480f3cd5b4476e92f4303cf545460ab46376aac | 3480f3cd5b4476e92f4303cf545460ab46376aac |
| skills/README.md | 93d95342c9d535643c459a4a801e4ed9a271064c | 9c401f834ab0f82af88a134b2982725a491d5fd7 | 9c401f834ab0f82af88a134b2982725a491d5fd7 |
| tests/test_install_development_skills.py | 9fea3b64724de08eec328892586f188e7c3d1a39 | 3f2e5ef98ba4738c17bcdc6237d542242f2d621a | 3f2e5ef98ba4738c17bcdc6237d542242f2d621a |
| tests/test_run_evidence.py | 2f2ec65002cd4980796120213f637ba29359cd7e | d524b0671be7c6fa6a41e260282ad38e6d55d635 | d524b0671be7c6fa6a41e260282ad38e6d55d635 |
| tests/test_workflow_version.py | bcea14ea4aa3d5b7cedaacc1eaa4578ab6b59837 | dbc47d3280d10d46f69de16acc8560ba34474f16 | dbc47d3280d10d46f69de16acc8560ba34474f16 |

Context/policy/current dependency hashes (HEAD, index, and worktree equal for
every entry below):

- `AGENTS.md`: `4d0be232d374928d125fdc3d4bb7eb844dad098f`
- `docs/tasks/T-004.1/brief.md`: `0744c01b6db8ece290e7dcdc527821de7ca144a2`
- `docs/tasks/T-004.1/verification.md`: `e27bb0080ac0cd945145667d37ced87ed38dd826`
- `docs/tasks/T-004.1/preflight.md`: `cef8a728a1a80966d27e629757b131065a4ebd9a`
- `docs/project-plan.md`: `b1df1bb0a145f91d7d7f99b451b32e1f0a192acd`
- `docs/tasks/T-004/brief.md`: `f8cc35c13dd5cc9d3e69ee103728169b24f856e8`
- `docs/task-map.json`: `8f546ae206e32859ecd2537abdd1656ae237e9ee`
- `scripts/install_development_skills.py`: `e1f139c134aadc5732d5cdd9126837af9fcf24dc`
- `scripts/run_evidence.py`: `526b884010d8f90a78a660f7d2062dd1a104d7c4`

The ready preflight's older HEAD is historical preparation; its named scope,
dependencies, interface facts and commands remain applicable. Authority and
verification revision are unchanged. The prior discovery already used the
current HEAD. No plan, tracker, installed .agents file, runtime evidence, or
historical report was edited.

Exact reviewed status immediately before the report write:

```text
M  README.md
A  docs/tasks/T-004.1/implementation.md
A  docs/tasks/T-004.1/reviews/discovery-01.md
M  scripts/workflow_version.py
M  skills/README.md
M  tests/test_install_development_skills.py
M  tests/test_run_evidence.py
M  tests/test_workflow_version.py
```

Post-report status (observed after writing; only the new report entry differs):

```text
M  README.md
A  docs/tasks/T-004.1/implementation.md
A  docs/tasks/T-004.1/reviews/discovery-01.md
M  scripts/workflow_version.py
M  skills/README.md
M  tests/test_install_development_skills.py
M  tests/test_run_evidence.py
M  tests/test_workflow_version.py
?? docs/tasks/T-004.1/reviews/discovery-02.md
```

The post-write read-only check confirms the staged binary diff digest,
all existing index/worktree path blobs, HEAD, and context identities stayed
unchanged. The report remains unstaged. Its own authenticity is not claimed.

## 8. Questions, unchecked work, and residual risks

No unresolved question, required blocked row, or unchecked row remains.
Controlled Git errors prove classification at the exercised boundary; they
do not estimate failure frequency. Historical producer records remain
producer-attributed.

This leaf excludes profile checker (.2), refresh composition (.3), collector
begin/finish/recover lifecycle, and installed agent-call qualification.
The source collector still requires HEAD; its documented exclusion remains
accurate. No conditional architecture/maintainability gate is mandated for this
bounded change by the applicable repository policy; no docs/contracts registry
exists. Discovery performs none of those stages and grants no deferral.

## 9. Coverage completeness and next route

Coverage is complete: V-01–V-08 pass on the current bytes; no current finding
or unfinished required evidence row remains.

Next owner: a separate task-acceptance-review decision call.
Provide docs/tasks/T-004.1/brief.md, the current staged diff identified here,
implementation.md, this report, discovery-01.md for F-01 history and regression
context, verification.md revision 1, preflight.md, and the cited project-plan,
parent brief and task-map context. Supply CD-01/CD-04 reviewer regression commands
and all ledger rows (there are no blocked/unchecked rows). Discovery does not
launch that call or advance the task.

## 10. Discovery continuation

```markdown
Discovery continuation:
- Iteration / current byte identity: correction discovery 1, report 02; HEAD 9712879568751c16d6eff79d1977768b866c2dd1; staged binary diff SHA-256 9e629e82863caafffe5931ea4c7327b90f6eb008e4dccdd70a6db56053035d76; index/worktree identities in section 7; six implementation blobs match submitted correction finish snapshot 7cbd6fceac107f1846c5a04ae375da8a54fd6e6c.
- Coverage rows: V-01 pass; V-02 pass; V-03 pass (prior fail F-01, current fatal/ref-error regression clean); V-04 pass; V-05 pass; V-06 pass; V-07 pass; V-08 pass (prior fail F-01, current documented error guarantee exercised). No blocked/unchecked rows.
- Finding IDs: no current findings; retain historical F-01 suggested P2, corrected trigger not reproduced.
- Finding/scenario continuity: discovery-01 V-03/V-08 failed F-01; producer correction run run-20261012T160101Z-11ff08a7052a claims C-F fail-first, C-R regression and C-TW/C-TR/C-W/C-R2/C-I success. CD-01/CD-04 independently corroborate corrected bytes and named source/copied identity, staged/final availability, and genuine-unborn lookup-error siblings; CD-02/CD-03 freshly corroborate prior pass rows. Incomplete reasons: none. Correction owner: implementer if separately routed; evidence owner: this discovery for current evidence, fresh discovery for later bytes; authority owner: task coordinator/designer. No approved deferral.
- Preparation/context: docs/tasks/T-004.1/brief.md blob 0744c01b6db8ece290e7dcdc527821de7ca144a2; verification.md revision 1; preflight.md; implementation.md; docs/project-plan.md IF-004/007, FLOW-004 and section 11; docs/tasks/T-004/brief.md; docs/task-map.json.
- Reviewer regressions: no new repository regression file; exact CD-01 and CD-04 commands in this report section 5; original DISC-05 in discovery-01.md section 5. Current oracle rejects fatal-lookup identity and availability, preserves existing-ref control and genuine unborn success, and checks source/staged/unborn sibling surfaces.
- Aggregate gate: passed, 54 tests OK; PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_install_development_skills test_workflow_version test_run_evidence; owner this correction discovery; run once after clean targeted reconciliation.
- Next: separate task-acceptance-review decision with brief, identified staged diff, current submission, both discovery reports, all ledger rows/regressions, verification revision 1, preflight and cited decision context.
```

