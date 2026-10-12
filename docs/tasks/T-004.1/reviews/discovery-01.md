# Task Review Discovery Report: T-004.1 — Install the development profile in genuine unborn repositories

| Field | Value |
|---|---|
| Producing stage | `task-review-discovery`, active project-local installation |
| Coverage completeness | complete — all V-01–V-08 have current pass/fail dispositions; V-03 and V-08 fail |
| Discovery iteration | first independent discovery |
| Created at | 2026-10-12T16:22:07+01:00 |
| Repository root | /Users/mtrusov/work/skill-sources/personal-skills |
| Durable report path | docs/tasks/T-004.1/reviews/discovery-01.md |
| Task brief | docs/tasks/T-004.1/brief.md |
| Verification / context | docs/tasks/T-004.1/verification.md revision 1; preflight.md; docs/project-plan.md sections 1–2, IF-004/007, FLOW-004, section 11; docs/tasks/T-004/brief.md; docs/task-map.json |
| Current submission | docs/tasks/T-004.1/implementation.md, READY_FOR_REVIEW; supplied during discovery by the implementing agent at the user's request |

This report supplies evidence only. It gives no acceptance verdict, approved deferral, or advancement. It applies to the identified staged bytes. Corrections require fresh corroboration. The report does not review or authenticate itself.

## 1. Discovery provenance

This session authored no reviewed production or test bytes. Its behavioral observations are independent of implementation authorship. No subagents or external reviewers were launched. Active skills: project-local task-review-discovery and testing-discipline; no active installation was refreshed.

HEAD: `9712879568751c16d6eff79d1977768b866c2dd1`. Staged diff SHA-256 (`git diff --cached --binary`): `09f3b151cb3ae676eeaedb28f8cdb276390b6de4dc115bdf4f48bf611a02b5a4`. Index tree recorded by byte-capture command: `a4d2c39780bc7dfd3c463b22c2618b15851b5c4b`.

The implementation evidence manifest's finish snapshot is `68e7b1817c6d9f3a639825442494c2fa976e27af`. Each of the six scoped index blobs matches both the current worktree blob and that submission snapshot independently. Matching status alone was not used as identity proof.

## 2. Findings

### F-01 [suggested P2] Fatal ref lookup errors become successful unborn identity

| Field | Evidence |
|---|---|
| Location | scripts/workflow_version.py:38–46 and :236–240 |
| Trigger | A real committed target; controlled Git-boundary errors make `rev-parse HEAD` and `show-ref --verify --quiet <actual-branch>` exit 128 with an explicit ref-database I/O error. Other Git commands execute normally. |
| Consequence | Installed workflow identity exits 0 with `repository_commit: null`; installed availability exits 0 with `available: true`. A known committed repository is misreported as unborn and a genuine Git failure is hidden. |
| Evidence | DISC-05 below independently reproduces both public outcomes. Control variant fails only `rev-parse HEAD`: the same installed commands correctly exit 2 when `show-ref` succeeds. The wrapper controls only Git subprocesses, never identity or availability logic. |
| Affected AC / scenarios | AC-02, AC-04; V-03 and V-08; R-01 / INV-009 / IF-007 |
| Broken invariant | Unborn success requires evidence that the branch ref is absent. A fatal lookup failure supplies no such evidence. `_git_succeeded` collapses every nonzero code to false, and `_head_commit` treats false as absence. |
| Credible sibling surface | The same helper supplies source and copied installed identity, and both staged and final installer availability gates. Git lookup failures on genuine unborn targets must also remain errors when absence cannot be established. |
| Corrective direction | Preserve the distinction between confirmed missing branch refs and failed ref lookups throughout HEAD classification; propagate genuine lookup errors through every identity/availability consumer. Add focused Git-boundary regression evidence for that distinction. |

Exposure is bounded to the fallback following failed HEAD resolution; normal committed, detached, unborn and non-repository cases pass. The consequence is false provenance and false availability at a required interface, rather than data mutation. Existing invalid-target and malformed-HEAD cases do not exercise the fatal ref-lookup fallback. The README's unconditional promise that actual Git failures are never treated as missing first commits is contradicted by this observation.

## 3. Completeness ledger

The V-01–V-08 ledger was frozen from verification revision 1 before behavioral probes. No prior discovery ledger or correction findings were supplied; the task package had no prior review reports.

| Row | AC / invariant | Explicit cases and setup / oracle | Submitted evidence | Independent evidence | Result / reason |
|---|---|---|---|---|---|
| V-01 | AC-01/02; R-01 | Real `git init`, no commit, complete source inputs; canonical installer and copied identity/availability; original symbolic HEAD and recursive object path/byte inventory unchanged | F fail-first: exit 2, missing=[] and workflow_unavailable; T3 current unborn test claimed pass | DISC-01 current targeted case and DISC-02 independent public probe: installed=true, available=true, null commit, real unborn branch, no created objects | pass — current public behavior independently observed; historical fail-first remains producer-attributed |
| V-02 | AC-02; R-01 | Real attached then detached commit; canonical install, final availability and identity; actual commit and attachment unchanged | Existing W/I cases claimed pass; detached identity owning test | DISC-02 invokes canonical installation and both copied CLIs in each actual Git state | pass — both installation variants and actual HEAD identities preserved |
| V-03 | AC-02; R-01 | Complete copied tools/package on actual invalid Git target; controlled committed Git-boundary failures with known cause; errors must remain failures | T1/T2/T3 invalid-target and malformed HEAD cases claimed pass | DISC-02 rejects actual invalid target at all three CLIs; DISC-05 fatal lookup variant falsely succeeds, control variant correctly fails | fail — F-01; broad Git-error claim disproved |
| V-04 | AC-03; R-02 | Fixed pre-change algorithm from HEAD against unchanged staged fingerprint code; included tracked edit and untracked Unicode file; root evals/tests, nested cache/node_modules, .DS_Store/.pyc; repeated and reversed discovery | W owning cases and unchanged framing/selection code claimed | DISC-04 executes HEAD baseline and current fingerprints on the same known fixture before/after isolated transformations and controlled reversed enumeration | pass — framing compatibility, selection and ordering relations hold |
| V-05 | AC-03; R-02 | Exact included relative path/byte comparison; copied standalone and project-local tools, project-local ignored and not ignored; compare nonempty source fingerprint | W standalone/project-local/ignored cases claimed pass | DISC-04 copies known bytes, checks included bytes independently, invokes each copied identity CLI and excludes empty-package hash | pass — all three layout/ignore variants match |
| V-06 | AC-02/03; R-02 | Successfully installed unborn target; first and later unrelated real commits; actual HEAD, final availability and package bytes observed after each | T1/T3 transition variants claimed pass | DISC-02 executes both actual commits in sequence, invokes copied identity/availability each time, compares full installed package byte inventory | pass — commit identity advances; availability and package fingerprint persist |
| V-07 | AC-04 | Custom skill/script/other .agents bytes, app bytes and AGENTS text; canonical install; exact manifest-selected projection, helpers and guide against source | I projection/preservation suites claimed pass; unchanged installer manifest | DISC-02 compares every selected package under canonical transient exclusions, every helper and guide; asserts unmanaged bytes and AGENTS text preserved | pass — changed helper distributed, selection and ownership unchanged |
| V-08 | AC-04 | Semantic review of root/profile/flow guidance against observed CLI interfaces and scoped collector exclusion | Submitted guidance map claimed accurate; flow README has no affected install guidance | Static diff and existing collector HEAD traces; normal scope/interface wording matches DISC-02, but README Git-error promise fails under DISC-05 | fail — F-01 contradicts the documented Git-error guarantee; unborn scope and collector exclusion wording are otherwise accurate |

No required/material row is blocked or unchecked. All ACs and finite risks are represented. No executable schema contract changed or supplies a material oracle here. No process-lifecycle contract is part of this task: probes use synchronous CLI children with bounded timeouts, rather than persistent fixture processes.

## 4. Adversarial checks

- R-01: genuine unborn versus attached/detached HEAD, actual invalid repository, and controlled fatal Git ref lookup versus successful ref lookup.
- R-02: real unborn → first → later commit sequence, independent package-byte observations, three copied layouts/ignore combinations, all specified exclusions, included Unicode bytes, reversed enumeration.
- AC-04: every selected managed package and shared helper contrasted with custom unmanaged bytes.
- DISC-03 included an additional malformed-ref diagnostic that raised WorkflowVersionError instead of producing a new finding. It does not weaken DISC-05 or establish a public failure for the controlled fatal-lookup case.

## 5. Commands and independent evidence

All commands ran from the repository root. Python probes set PYTHONDONTWRITEBYTECODE=1. They used real disposable Git repositories and synchronous subprocesses, with a 20-second timeout for reviewer-created public calls. TemporaryDirectory cleanup ran even for the unsuccessful diagnostic. No local server, network/model call, privileged probe, test-file edit, persistent fixture process, or whole-repo suite ran.

Read-only preparation inspected the active skill/template, testing-discipline, AGENTS.md, brief, verification, preflight, current submission, scoped cached diff, relevant owning tests, canonical installer manifest/ownership logic, identity/availability code, parent brief and relevant plan/task-map context. `git diff --cached --check` exited 0; it supplies formatting evidence only.

The supplied manifest was read at:
`.git/personal-skills/run-evidence/runs/run-20261012T150815Z-86087759ea56/manifest.json`.
Its original fail-first result is exit 2 with `fatal: ambiguous argument 'HEAD'`, `missing: []`, `reason: workflow_unavailable`; submitted W/R/I runs each claim 17 tests OK. These are submitted records, not an independently run aggregate. The original disposable fail-first target was already removed; discovery neither re-created historical chronology nor authenticated the stored evidence.

### DISC-01

Exact command:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_install_development_skills.DevelopmentSkillInstallerTests.test_installs_profile_into_unborn_repository_without_creating_a_commit
```

Observed exit 0; output:

```text
.
----------------------------------------------------------------------
Ran 1 test in 0.718s

OK
```

### DISC-02

Exact command:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import importlib.util, json, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path.cwd()
spec=importlib.util.spec_from_file_location('installer',ROOT/'scripts/install_development_skills.py')
installer=importlib.util.module_from_spec(spec); spec.loader.exec_module(installer)
def run(*args,cwd=None):
    return subprocess.run([str(a) for a in args],cwd=cwd,capture_output=True,text=True,timeout=20)
def git(repo,*args):
    p=run('git','-C',repo,*args); assert p.returncode==0,(args,p.stderr); return p.stdout.strip()
def cli(repo,name,*args):
    return run(sys.executable,repo/'.agents/scripts'/name,*args,cwd=repo)
def identity(repo):
    p=cli(repo,'workflow_version.py','bounded-task-implementer')
    assert p.returncode==0,p.stderr
    return json.loads(p.stdout)
def available(repo):
    p=cli(repo,'run_evidence.py','--repo',repo,'availability')
    assert p.returncode==0,p.stderr
    data=json.loads(p.stdout); assert data['available']; return data
def inventory(root):
    return {p.relative_to(root).as_posix():p.read_bytes() for p in root.rglob('*') if p.is_file()}
def package(repo):
    return inventory(repo/'.agents/skills/task-implementation-flow/bounded-task-implementer')
with tempfile.TemporaryDirectory() as td:
    repo=Path(td)/'target'; repo.mkdir()
    git(repo,'init','-q'); git(repo,'config','user.email','discovery@example.com'); git(repo,'config','user.name','Discovery')
    (repo/'.gitignore').write_text('.agents/\n')
    (repo/'app.txt').write_text('app\n')
    (repo/'AGENTS.md').write_text('# Custom\n\nKeep user text.\n')
    custom=repo/'.agents/skills/custom/SKILL.md'; custom.parent.mkdir(parents=True)
    custom.write_text('---\nname: custom\ndescription: custom\n---\nbody\n')
    helper=repo/'.agents/scripts/custom.py'; helper.parent.mkdir(parents=True); helper.write_text('value=1\n')
    other=repo/'.agents/notes.txt'; other.write_text('notes\n')
    before={p:p.read_bytes() for p in (custom,helper,other,repo/'app.txt')}
    head_ref=git(repo,'symbolic-ref','HEAD'); objects=inventory(repo/'.git/objects')
    p=run(sys.executable,ROOT/'scripts/install_development_skills.py',repo)
    assert p.returncode==0,p.stderr
    assert json.loads(p.stdout)['availability']['available']
    info=identity(repo); available(repo)
    assert info['repository_commit'] is None
    assert info['repository_branch']==head_ref.removeprefix('refs/heads/')
    assert git(repo,'symbolic-ref','HEAD')==head_ref
    assert inventory(repo/'.git/objects')==objects
    assert run('git','-C',repo,'rev-parse','--verify','HEAD').returncode!=0
    assert all(p.read_bytes()==data for p,data in before.items())
    assert '# Custom\n\nKeep user text.' in (repo/'AGENTS.md').read_text()
    for name in installer.SHARED_SCRIPT_FILES:
        assert (repo/'.agents/scripts'/name).read_bytes()==(ROOT/'scripts'/name).read_bytes()
    assert (repo/'.agents/skills/README.md').read_bytes()==(ROOT/installer.PROFILE_SKILLS_README).read_bytes()
    for _,rel in installer.DEVELOPMENT_SKILL_SOURCES:
        src=inventory(ROOT/rel); dst=inventory(repo/'.agents'/rel)
        selected={k:v for k,v in src.items() if not any(x in ('__pycache__','node_modules') for x in Path(k).parts) and not k.endswith('.pyc') and Path(k).name!='.DS_Store'}
        assert selected==dst,rel
    print('V-01/V-07 PASS: real unborn canonical+final availability, null identity, recursive object inventory unchanged, exact managed projection, preserved unmanaged bytes')
    original=package(repo); fingerprint=info['fingerprint']
    for label in ('first','later'):
        (repo/'app.txt').write_text(label+'\n'); git(repo,'add','.'); git(repo,'commit','-qm',label)
        info=identity(repo); available(repo)
        assert info['repository_commit']==git(repo,'rev-parse','HEAD')
        assert info['fingerprint']==fingerprint and package(repo)==original
        print('V-06 PASS:',label,'actual HEAD, final availability, unchanged package/fingerprint')
    for detached in (False,True):
        if detached: git(repo,'checkout','--detach','-q')
        commit=git(repo,'rev-parse','HEAD'); branch=git(repo,'branch','--show-current') or None
        p=run(sys.executable,ROOT/'scripts/install_development_skills.py',repo); assert p.returncode==0,p.stderr
        info=identity(repo); available(repo)
        assert info['repository_commit']==commit and info['repository_branch']==branch
        assert git(repo,'rev-parse','HEAD')==commit and (git(repo,'branch','--show-current') or None)==branch
        print('V-02 PASS:', 'detached' if detached else 'attached','canonical install + actual identity + final availability')
    invalid=Path(td)/'invalid'; invalid.mkdir()
    import shutil
    shutil.copytree(repo/'.agents',invalid/'.agents')
    p=run(sys.executable,ROOT/'scripts/install_development_skills.py',invalid)
    assert p.returncode==2 and 'target repository is not usable' in p.stderr
    for name,args in [('workflow_version.py',('bounded-task-implementer',)),('run_evidence.py',('--repo',invalid,'availability'))]:
        p=cli(invalid,name,*args); assert p.returncode==2 and not p.stdout,p
    print('V-03 PASS: real invalid Git target rejected by canonical install and complete copied identity/availability tools')
print('Cleanup PASS: synchronous children finished; all disposable directories removed')

PY
```

Observed exit 0; output:

```text
V-01/V-07 PASS: real unborn canonical+final availability, null identity, recursive object inventory unchanged, exact managed projection, preserved unmanaged bytes
V-06 PASS: first actual HEAD, final availability, unchanged package/fingerprint
V-06 PASS: later actual HEAD, final availability, unchanged package/fingerprint
V-02 PASS: attached canonical install + actual identity + final availability
V-02 PASS: detached canonical install + actual identity + final availability
V-03 PASS: real invalid Git target rejected by canonical install and complete copied identity/availability tools
Cleanup PASS: synchronous children finished; all disposable directories removed
```

### DISC-03

Exact command:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import importlib.util,json,os,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path.cwd(); real_git=shutil.which('git')
def run(*args,env=None):
    return subprocess.run([str(a) for a in args],capture_output=True,text=True,env=env,timeout=20)
with tempfile.TemporaryDirectory() as td:
    base=Path(td); repo=base/'repo'; repo.mkdir()
    for args in [('init','-q'),('config','user.email','discovery@example.com'),('config','user.name','Discovery')]:
        p=run(real_git,'-C',repo,*args); assert p.returncode==0,p.stderr
    (repo/'app').write_text('app\n')
    for args in [('add','.'),('commit','-qm','real commit')]:
        p=run(real_git,'-C',repo,*args); assert p.returncode==0,p.stderr
    actual=run(real_git,'-C',repo,'rev-parse','HEAD').stdout.strip()
    p=run(sys.executable,ROOT/'scripts/install_development_skills.py',repo); assert p.returncode==0,p.stderr
    wrapper=base/'bin'; wrapper.mkdir()
    shim=wrapper/'git'
    shim.write_text('#!'+sys.executable+'\nimport os,sys\nargs=sys.argv[1:]\nif args[2:]==["rev-parse","HEAD"] or (args[2:] and args[2]=="show-ref"):\n print("fatal: controlled ref-database I/O failure",file=sys.stderr)\n sys.exit(128)\nos.execv('+repr(real_git)+',['+repr(real_git)+']+args)\n')
    shim.chmod(0o755)
    env=dict(os.environ,PATH=str(wrapper)+os.pathsep+os.environ['PATH'],PYTHONDONTWRITEBYTECODE='1')
    p=run('git','-C',repo,'show-ref','--verify','--quiet',run(real_git,'-C',repo,'symbolic-ref','HEAD').stdout.strip(),env=env)
    assert p.returncode==128
    print('CONTROL: real committed HEAD='+actual+'; injected show-ref rc=128 stderr='+p.stderr.strip())
    for name,args in [('workflow_version.py',('bounded-task-implementer',)),('run_evidence.py',('--repo',repo,'availability'))]:
        p=run(sys.executable,repo/'.agents/scripts'/name,*args,env=env)
        data=json.loads(p.stdout) if p.stdout else None
        print(name,'rc='+str(p.returncode),'repository_commit='+repr(data.get('repository_commit')) if name=='workflow_version.py' and data else 'available='+repr(data.get('available')) if data else p.stderr.strip())
    spec=importlib.util.spec_from_file_location('current',ROOT/'scripts/workflow_version.py')
    current=importlib.util.module_from_spec(spec);spec.loader.exec_module(current)
    # Real malformed existing branch ref demonstrates lower boundary error classification.
    ref=run(real_git,'-C',repo,'symbolic-ref','HEAD').stdout.strip()
    (repo/'.git'/ref).write_text('corrupt reference\n')
    p=run(real_git,'-C',repo,'show-ref','--verify','--quiet',ref)
    print('REAL CORRUPT REF: show-ref rc='+str(p.returncode)+' stderr='+p.stderr.strip())
    print('REAL CORRUPT REF: _head_commit='+repr(current._head_commit(repo)))
print('Cleanup: disposable wrappers/repos removed; subprocess calls completed with bounded timeout')

PY
```

Observed exit 1; output:

```text
CONTROL: real committed HEAD=126592fa4d500d135a5e67b86e9bb77db839e1f0; injected show-ref rc=128 stderr=fatal: controlled ref-database I/O failure
workflow_version.py rc=0 repository_commit=None
run_evidence.py rc=0 available=True
REAL CORRUPT REF: show-ref rc=1 stderr=
Traceback (most recent call last):
  File "<stdin>", line 34, in <module>
  File "/Users/mtrusov/work/skill-sources/personal-skills/scripts/workflow_version.py", line 235, in _head_commit
    raise original from None
  File "/Users/mtrusov/work/skill-sources/personal-skills/scripts/workflow_version.py", line 230, in _head_commit
    return _git(repo_root, "rev-parse", "HEAD").strip()
           ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/mtrusov/work/skill-sources/personal-skills/scripts/workflow_version.py", line 34, in _git
    raise WorkflowVersionError(message) from exc
current.WorkflowVersionError: fatal: ambiguous argument 'HEAD': unknown revision or path not in the working tree.
Use '--' to separate paths from revisions, like this:
'git <command> [<revision>...] -- [<file>...]'
```

### DISC-04

Exact command:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 - <<'PY'
import importlib.util,json,shutil,subprocess,sys,tempfile,types
from pathlib import Path
from unittest.mock import patch
import test_workflow_version as fixtures
ROOT=Path.cwd(); current=fixtures.workflow_version
baseline=types.ModuleType('baseline'); baseline.__file__=str(ROOT/'scripts/workflow_version.py')
old=subprocess.run(['git','show','HEAD:scripts/workflow_version.py'],capture_output=True,text=True,check=True).stdout
exec(compile(old,baseline.__file__,'exec'),baseline.__dict__)
case=fixtures.WorkflowVersionTests(); case.setUp()
try:
    repo,skill=case.repo,case.skill
    before=current.fingerprint_workflow(repo,skill)
    assert before==baseline.fingerprint_workflow(repo,skill)
    files=current.workflow_files(repo,skill)
    rev='\0'.join(p.relative_to(repo).as_posix() for p in reversed(files))+'\0'
    real=current._git
    def reversed_git(root,*args):
        return rev if args[0]=='ls-files' else real(root,*args)
    with patch.object(current,'_git',reversed_git):
        assert current.fingerprint_workflow(repo,skill)==before
    for relative in ['evals/input.json','tests/case.py','nested/__pycache__/cache','nested/node_modules/pkg','nested/.DS_Store','nested/code.pyc']:
        p=skill/relative;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('excluded\n')
        assert current.fingerprint_workflow(repo,skill)==before,relative
    (skill/'references/rules.md').write_text('changed included\n')
    changed=current.fingerprint_workflow(repo,skill); assert changed!=before
    (skill/'新-é.txt').write_text('unicode included\n')
    assert current.fingerprint_workflow(repo,skill)!=changed
    assert current.fingerprint_workflow(repo,skill)==baseline.fingerprint_workflow(repo,skill)
    assert current.fingerprint_workflow(repo,skill)==current.fingerprint_workflow(repo,skill)
    print('V-04 PASS: baseline algorithm compatibility, included tracked/Unicode, all six exclusion dimensions, repeated/reversed discovery')
    # Identical package bytes, copied identity CLI, both source and installed layouts.
    expected={p.relative_to(skill).as_posix():p.read_bytes() for p in current.workflow_files(repo,skill)}
    source=current.get_workflow_version(repo,'bounded-task-implementer')['fingerprint']
    for layout,ignored in [('standalone',False),('project-local',False),('project-local',True)]:
        with tempfile.TemporaryDirectory() as td:
            target=Path(td); fixtures.git(target,'init','-q')
            fixtures.git(target,'config','user.email','discovery@example.com')
            fixtures.git(target,'config','user.name','Discovery')
            if ignored:(target/'.gitignore').write_text('.agents/\n')
            root=target if layout=='standalone' else target/'.agents'
            dest=root/'skills/bounded-task-implementer';shutil.copytree(skill,dest)
            scripts=root/'scripts';scripts.mkdir();shutil.copy2(ROOT/'scripts/workflow_version.py',scripts/'workflow_version.py')
            assert {rel:(dest/rel).read_bytes() for rel in expected}==expected
            fixtures.git(target,'add','.'); fixtures.git(target,'commit','-qm','baseline')
            p=subprocess.run([sys.executable,str(scripts/'workflow_version.py'),'bounded-task-implementer'],cwd=target,capture_output=True,text=True,timeout=20)
            assert p.returncode==0,p.stderr
            value=json.loads(p.stdout)['fingerprint']
            import hashlib
            assert value==source and value!='sha256:'+hashlib.sha256(b'').hexdigest()
            print('V-05 PASS:',layout,'ignored='+str(ignored),'independent included byte equality; nonempty identical fingerprint')
finally:case.tearDown()
print('Cleanup: synchronous children completed, all temporary repos removed')

PY
```

Observed exit 0; output:

```text
V-04 PASS: baseline algorithm compatibility, included tracked/Unicode, all six exclusion dimensions, repeated/reversed discovery
V-05 PASS: standalone ignored=False independent included byte equality; nonempty identical fingerprint
V-05 PASS: project-local ignored=False independent included byte equality; nonempty identical fingerprint
V-05 PASS: project-local ignored=True independent included byte equality; nonempty identical fingerprint
Cleanup: synchronous children completed, all temporary repos removed
```

### DISC-05

Exact command:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import json,os,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path.cwd(); real_git=shutil.which('git')
def run(*args,env=None):
    return subprocess.run([str(a) for a in args],capture_output=True,text=True,env=env,timeout=20)
with tempfile.TemporaryDirectory() as td:
    base=Path(td); repo=base/'repo'; repo.mkdir()
    for args in [('init','-q'),('config','user.email','discovery@example.com'),('config','user.name','Discovery')]:
        p=run(real_git,'-C',repo,*args); assert p.returncode==0,p.stderr
    (repo/'app').write_text('app\n')
    for args in [('add','.'),('commit','-qm','real commit')]:
        p=run(real_git,'-C',repo,*args); assert p.returncode==0,p.stderr
    actual=run(real_git,'-C',repo,'rev-parse','HEAD').stdout.strip()
    p=run(sys.executable,ROOT/'scripts/install_development_skills.py',repo); assert p.returncode==0,p.stderr
    wrapper=base/'bin'; wrapper.mkdir(); shim=wrapper/'git'
    shim.write_text('#!'+sys.executable+'\nimport os,sys\nargs=sys.argv[1:]\nif args[2:]==["rev-parse","HEAD"] or (os.environ.get("FAIL_SHOW_REF")=="1" and args[2:] and args[2]=="show-ref"):\n print("fatal: controlled ref-database I/O failure",file=sys.stderr)\n sys.exit(128)\nos.execv('+repr(real_git)+',['+repr(real_git)+']+args)\n')
    shim.chmod(0o755)
    env=dict(os.environ,PATH=str(wrapper)+os.pathsep+os.environ['PATH'],PYTHONDONTWRITEBYTECODE='1')
    for mode in ('0','1'):
        env['FAIL_SHOW_REF']=mode
        for name,args in [('workflow_version.py',('bounded-task-implementer',)),('run_evidence.py',('--repo',repo,'availability'))]:
            p=run(sys.executable,repo/'.agents/scripts'/name,*args,env=env)
            if mode=='0':
                assert p.returncode==2,p.stdout
                print('CONTROL PASS: '+name+' rejects failed rev-parse when show-ref resolves real existing branch')
            else:
                assert p.returncode==0,p.stderr
                data=json.loads(p.stdout)
                if name=='workflow_version.py':
                    assert data['repository_commit'] is None
                    print('F-01 REPRODUCED: identity rc=0 repository_commit=null despite actual committed HEAD '+actual)
                else:
                    assert data['available'] is True
                    print('F-01 REPRODUCED: installed availability rc=0 available=true after fatal show-ref rc=128')
    # Controls guarantee wrapper caused failure only at Git commands, not identity/availability.
    branch=run(real_git,'-C',repo,'symbolic-ref','HEAD').stdout.strip()
    p=run('git','-C',repo,'show-ref','--verify','--quiet',branch,env=env)
    assert p.returncode==128 and 'controlled ref-database I/O failure' in p.stderr
    assert run(real_git,'-C',repo,'rev-parse','HEAD').stdout.strip()==actual
print('Cleanup: bounded synchronous children completed; disposable wrapper and repository removed')

PY
```

Observed exit 0; output:

```text
CONTROL PASS: workflow_version.py rejects failed rev-parse when show-ref resolves real existing branch
CONTROL PASS: run_evidence.py rejects failed rev-parse when show-ref resolves real existing branch
F-01 REPRODUCED: identity rc=0 repository_commit=null despite actual committed HEAD 52dc5046b56a0f592712b5a62e8d20c102f7a3d0
F-01 REPRODUCED: installed availability rc=0 available=true after fatal show-ref rc=128
Cleanup: bounded synchronous children completed; disposable wrapper and repository removed
```

DISC-03's command exited 1 at its extra malformed-ref diagnostic. Its earlier controlled public observations were reproduced with clean controls in DISC-05 (exit 0, meaning the probe successfully reproduced the defect, not that the product passed). Temporary cleanup completed through the context manager.

## 6. Aggregate-gate record

| Field | Value |
|---|---|
| Exact assigned command | `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_install_development_skills test_workflow_version test_run_evidence` |
| Status | not run |
| Owner / stage | this independent first discovery pass |
| Reason | Decisive targeted failure F-01; initial-discovery aggregate suppressed under IF-004 and verification revision 1 |
| Current evidence | All V rows reconciled; V-03/V-08 fail; remaining rows pass. No selected targeted probe remains. No distinct diagnostic aggregate purpose was requested. |

Correction discovery must corroborate corrected bytes, rerun DISC-05 with an oracle requiring both fatal-lookup outcomes to fail, check the influenced identity/availability surfaces, reconcile all rows, then own the assigned aggregate if targeted evidence is clean. Passing previously submitted owning suites cannot erase this failure.

## 7. Scope and baseline comparison

All six staged paths are authorized task-owned paths. There is no unstaged change to them. The brief hash matches the verification/preflight source revision. Preflight recorded HEAD 677904cc4df61292677e1876f1bafd06d412c693 and dirty task/index artifacts; current HEAD is 9712879568751c16d6eff79d1977768b866c2dd1. Submission attributes this baseline transition to the user's intervening commit. Current index/task planning documents are not edited by discovery.

The new implementation.md appeared during this review after the user stated that the implementing agent had created it. It is a supplied handoff artifact, outside the staged production diff; no discovery ownership is claimed. No unexplained overlap remains in the scoped diff.

| Path | HEAD blob | Index blob | Worktree blob | Submitted finish snapshot blob |
|---|---|---|---|---|
| README.md | 2d8e11e74fe6acbf3df213f3ceaa535af7495554 | db87a49ddb6aae85dc851cf99a0e298519b71d28 | db87a49ddb6aae85dc851cf99a0e298519b71d28 | db87a49ddb6aae85dc851cf99a0e298519b71d28 |
| scripts/workflow_version.py | 1052d63ef66e8cb39f47b20dff759e7608dc11ae | ff56ddf242fb9f924163e990820f7fe22c4e82de | ff56ddf242fb9f924163e990820f7fe22c4e82de | ff56ddf242fb9f924163e990820f7fe22c4e82de |
| skills/README.md | 93d95342c9d535643c459a4a801e4ed9a271064c | 9c401f834ab0f82af88a134b2982725a491d5fd7 | 9c401f834ab0f82af88a134b2982725a491d5fd7 | 9c401f834ab0f82af88a134b2982725a491d5fd7 |
| tests/test_install_development_skills.py | 9fea3b64724de08eec328892586f188e7c3d1a39 | 3f2e5ef98ba4738c17bcdc6237d542242f2d621a | 3f2e5ef98ba4738c17bcdc6237d542242f2d621a | 3f2e5ef98ba4738c17bcdc6237d542242f2d621a |
| tests/test_run_evidence.py | 2f2ec65002cd4980796120213f637ba29359cd7e | e8580119030cff5bcfabf4062954e69bbf740c74 | e8580119030cff5bcfabf4062954e69bbf740c74 | e8580119030cff5bcfabf4062954e69bbf740c74 |
| tests/test_workflow_version.py | bcea14ea4aa3d5b7cedaacc1eaa4578ab6b59837 | afa1349a2c26c79da6d1e51e7b30e75283455cba | afa1349a2c26c79da6d1e51e7b30e75283455cba | afa1349a2c26c79da6d1e51e7b30e75283455cba |

Package/context blob identities:

- `docs/tasks/T-004.1/brief.md`: `0744c01b6db8ece290e7dcdc527821de7ca144a2`
- `docs/tasks/T-004.1/verification.md`: `e27bb0080ac0cd945145667d37ced87ed38dd826`
- `docs/tasks/T-004.1/preflight.md`: `cef8a728a1a80966d27e629757b131065a4ebd9a`
- `docs/tasks/T-004.1/implementation.md`: `61ded34a4374c8b98518eb004d2d173c25914a69`
- `docs/project-plan.md`: `b1df1bb0a145f91d7d7f99b451b32e1f0a192acd`
- `docs/tasks/T-004/brief.md`: `f8cc35c13dd5cc9d3e69ee103728169b24f856e8`
- `docs/task-map.json`: `8f546ae206e32859ecd2537abdd1656ae237e9ee`

Byte capture used `git rev-parse HEAD`, `git diff --cached --binary`, separate `git rev-parse HEAD:<path>` / `:<path>` / submitted-snapshot lookups, `git hash-object <path>`, and `git status --short --untracked-files=all`. It also used `git write-tree` to capture the index tree: that command can add a tree object to Git metadata and was an unnecessary exception to the read-only boundary. It changed neither the index nor worktree. No reset, restage, commit, or production write occurred.

Exact reviewed status immediately before report write:

```text
M  README.md
M  scripts/workflow_version.py
M  skills/README.md
M  tests/test_install_development_skills.py
M  tests/test_run_evidence.py
M  tests/test_workflow_version.py
?? docs/tasks/T-004.1/implementation.md
```

Post-report status (checked after write; only the new report entry may differ):

```text
M  README.md
M  scripts/workflow_version.py
M  skills/README.md
M  tests/test_install_development_skills.py
M  tests/test_run_evidence.py
M  tests/test_workflow_version.py
?? docs/tasks/T-004.1/implementation.md
?? docs/tasks/T-004.1/reviews/discovery-01.md
```

## 8. Questions and residual risks

No unresolved required input, blocked row, or unchecked behavioral row remains. Historical implementer checks remain producer-attributed. Conditional maintainability/architecture gates were not mandated for this change according to the supplied handoff and applicable repo instructions; no contract registry exists to synchronize. This discovery does not perform those stages or waive future applicability.

The controlled fatal-error probe proves fallback error handling at the real copied CLIs; it is not a frequency claim about ref-database I/O failures. Normal invalid-target and malformed-HEAD handling are separate passing cases. Profile checking (.2), refresh composition (.3), full collector lifecycle and installed agent-call qualification remain outside this leaf.

## 9. Coverage and next route

Coverage is complete as evidence gathering, with one confirmed finding and two failed rows. The exact next route is a separate task-acceptance-review decision call consuming this report. Supply the brief, staged diff identified above, implementation.md, verification revision 1, preflight.md, cited project/parent decision context and the DISC-05 reviewer regression. Discovery does not start correction or advance work.

## 10. Discovery continuation

```markdown
Discovery continuation:
- Iteration / byte identity: first independent discovery; HEAD 9712879568751c16d6eff79d1977768b866c2dd1; staged diff SHA-256 09f3b151cb3ae676eeaedb28f8cdb276390b6de4dc115bdf4f48bf611a02b5a4; six scoped index/worktree/submission blobs match the table.
- Coverage rows: V-01 pass; V-02 pass; V-03 fail F-01; V-04 pass; V-05 pass; V-06 pass; V-07 pass; V-08 fail F-01. No blocked/unchecked rows.
- Finding IDs: F-01 suggested P2, fatal lookup errors classified as unborn.
- Finding/scenario continuity: no prior discovery findings; implementer claimed all V rows pass in implementation.md and recorded F/T/W/R/I evidence. Discovery contradicts V-03 and the V-08 Git-error guarantee. Incomplete reasons: none; aggregate suppressed by decisive failure. Correction owner: implementer if routed by separate decision/coordinator; new evidence owner: fresh correction discovery; authority owner: task coordinator/designer. Influenced siblings: source/copied identity, staged/final availability, genuine unborn lookup failures.
- Preparation/context: docs/tasks/T-004.1/brief.md blob 0744c01b6db8ece290e7dcdc527821de7ca144a2; verification.md revision 1; preflight.md; implementation.md; docs/project-plan.md IF-004/007, FLOW-004 and section 11; docs/tasks/T-004/brief.md; docs/task-map.json.
- Reviewer regressions: no repository regression file added; exact reproducible DISC-05 command is in docs/tasks/T-004.1/reviews/discovery-01.md, section 5. Correction oracle must reject both fatal-lookup CLI outcomes while preserving the single-failure control and genuine unborn success.
- Aggregate gate: not run; PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_install_development_skills test_workflow_version test_run_evidence; owner this first discovery; reason F-01 targeted failure. Fresh correction discovery owns justified execution after clean targeted rows.
- Next: separate task-acceptance-review call with this report and all scoped/preparation/submission inputs; no verdict or advancement issued here.
```

