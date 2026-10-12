# Task Review Discovery Report: T-004.2 — Read-only profile checking

| Field | Value |
|---|---|
| Producing stage | Project-local installed task-review-discovery |
| Coverage completeness | complete — V-01–V-07 and R-01–R-03 have current evidence |
| Discovery iteration | correction discovery 3, following discovery-03 F-03 |
| Created at | 2026-10-12, Europe/Lisbon |
| Repository root | /Users/mtrusov/work/skill-sources/personal-skills |
| Durable report | docs/tasks/T-004.2/reviews/discovery-04.md |
| Task brief | docs/tasks/T-004.2/brief.md |
| Verification / readiness | docs/tasks/T-004.2/verification.md revision 1; preflight.md ready |
| Submission | staged results.md, F-01/F-02/F-03 correction and scenario evidence |
| Conditional evidence | pre-existing untracked reviews/maintainability-02.md; reviewed production/test/guide index blobs match this pass |

This report publishes evidence only. It contains no acceptance verdict, approved
deferral or advancement. It applies only to the identified reviewed bytes.
The separate acceptance decision call consumes it. It does not review or
authenticate itself.

## 1. Discovery provenance

This session authored no reviewed production, test, guidance or submission
bytes. Evidence is independent of production authorship. The active skills
were the project-local task-review-discovery and testing-discipline copies
under .agents/skills. The discovery report template was read. No active
installation was refreshed and no subagents were launched.

HEAD: `f6046d8b1a48f1984ad025589dca4a01c2fa87c9`.
SHA-256 of `git diff --cached --binary`: `c3a871c55660d5ec1cfa70f49f6a7ab07ec6011066f0def66cce8ee89f38c7b5`.
Every staged path was separately read from the index and worktree and compared
byte for byte; all matched. `git diff --name-only` was empty.

## 2. Findings

No findings.

Historical F-01, F-02 and F-03 are independently corroborated as corrected
for their demonstrated triggers and the bounded sibling cases below.
This is current evidence, not an acceptance disposition.

## 3. Completeness ledger

The ledger was reconstructed before probing from the brief, verification
revision 1 and discovery-01–03 continuations. Prior passes were navigation
context. Submitted evidence is the implementer's results.md scenario map,
family tests, correction regressions and claimed Appendix B probes.

| Row | AC / invariant | Explicit cases; setup / oracle | Submitted evidence | Independent current evidence | Result / reason |
|---|---|---|---|---|---|
| V-01 | AC-01/02/05; R-01/02 | Real positional installs in unborn/committed repos; public check exit 0, true match, empty differences and full count; linked source layouts | Fresh-install and linked/alias regressions | D-01 fresh-install variants; D-02 both Git states and multiple/sibling/nested aliases with independently expected count | pass — actual installed projections match |
| V-02 | AC-01/02/03; R-01/02 | Changed/missing SKILL.md, reference, eval/setup, guide, helper/config/schema; every selected package/shared file; missing package; owned extra; fingerprint-excluded mutation; exact path/category | Drift-family, fingerprint, missing-package and alias tests | D-01 all family/fingerprint/missing-package cases; D-02 exact changed/missing for 20 packages and six shared files, per-copy alias deletion | pass — complete managed projection detected |
| V-03 | AC-02/03; R-01/02 | Unselected skill/helper, other .agents bytes, outside-block text, four transient patterns ignored; owned non-transient extra contrasted | Ownership/transient test | D-01 public CLI contrast; static trace shows same transient patterns and pruning as copytree ignore policy | pass — narrow ownership and exclusions hold |
| V-04 | AC-01/02/03; R-01/02 | Changed/absent block, absent AGENTS; unmatched, duplicate, reversed markers; exact drift or precise failure | Marker test | D-01 real CLI variants; extraction/main traced | pass — absent/changed drift, malformed exit 2 |
| V-05 | AC-01/03; R-02 | Missing/non-Git/non-root target; missing source; unreadable file/source/expected and unexpected target directories; dangling entry; symlink/wrong-type refusal families; genuine cycle | Failure/denial/cycle tests | D-01 non-root actual denial and dangling-entry cases, none skipped; D-03 all 14 refusal shapes and real relocated missing-source CLI; D-02 bounded linked ancestor cycle | pass — invalid inputs cannot match and diagnose scope/reason |
| V-06 | AC-04; R-03 | Match/drift/failure/absent in unborn/committed targets twice; source/target path/type/byte and Git/evidence snapshots; absent .agents stays absent | Snapshot test and claimed eight-case prior probes | D-02 all eight combinations, equal repeated output and unchanged full snapshots; alias match/drift/cycle snapshots; D-03 refusal/source-error snapshots; D-01 source snapshot; static read-only trace | pass — current point-in-time read-only evidence |
| V-07 | AC-05 | Positional install/check from unrelated CWD; unmanaged preservation; location-based source; guides state scope, 0/1/2, no versions and deliberate refresh | Unrelated-CWD/guide test | D-01 exercises unrelated CWD; staged guides and main inspected; D-02/03 relocated complete source distribution | pass — documented interface and ownership preserved |
| R-01 | AC-02/03; INV-009 | Full canonical projection and precise drift across managed families | V-01–04 producer map | V-01–04 current evidence | pass |
| R-02 | AC-01/03; INV-009 | Distinct outcomes, ownership and precise failures | V-01–05 producer map | V-01–05 current evidence | pass |
| R-03 | AC-04; INV-009 | All result classes, both Git states, repeated unchanged inputs | V-06 producer map | V-06 current evidence | pass |

No required row is blocked or unchecked. Schemas are compared as opaque managed
bytes; this task changes no executable schema validator contract. Process
lifecycle, full installed-flow qualification and refresh composition belong
outside .2. CLI subprocesses completed with captured pipes and bounded waits
in reviewer probes; all temporary fixtures were removed.

## 4. Adversarial checks

- Complete projection: changed/missing mutations cover all 20 selected packages
  and all six managed shared files, rather than one representative package.
- Ownership: unselected content remains irrelevant while extra selected-directory
  content reports unexpected drift; unreadable unexpected and expected subtrees
  fail instead of disappearing.
- Aliases: multiple links to one external subtree, a regular sibling plus alias,
  and a nested alias match after actual installation. Deleting only the nested
  copied file reports its exact missing path. Adding a back-link closing an
  ancestor cycle then fails within the bounded public CLI call.
- Repetition: all eight Git-state/result combinations run twice on unchanged
  inputs with unchanged Git/evidence/file snapshots. Missing installations
  remain missing; drift remains drift.
- Refusals: symlink and wrong-type shapes at three installation roots, selected
  destination, shared script, guide and AGENTS fail without altering target
  or outside content.

## 5. Independent probes and commands

All behavioral commands ran from the repository root, Python 3.14.6,
uid 501, with PYTHONDONTWRITEBYTECODE=1. No network, dependency installation,
privileged execution, active refresh, production mutation or test edit was used.

| ID | Exact command / probe | Purpose | Result | Side effects / cleanup |
|---|---|---|---|---|
| D-01 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py -k check_` | Current scenario tests and F-01/F-02/F-03 regressions | exit 0, 16 tests, 8.345s, no skips | Disposable local fixtures only |
| D-02 | Appendix A, `PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'` | Eight snapshot/repetition cases, all packages/shared files, alias siblings and true cycle | exit 0; all explicit assertions passed | TemporaryDirectory scope removed all fixtures |
| D-03 | Appendix B, same heredoc invocation | All 14 refusal cases and real missing-source CLI | exit 0; precise failures and unchanged snapshots | TemporaryDirectory scope removed all fixtures |
| D-04 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py` | Justified owning aggregate | exit 0, 33 tests, 12.291s, no skips | Disposable local fixtures only |

Static command records: `git status --short --untracked-files=all`,
`git diff --cached --stat`, `git diff --cached --numstat`,
`git diff --cached -- scripts/install_development_skills.py README.md skills/README.md`,
`git diff --cached -- tests/test_install_development_skills.py`,
`git diff --name-only`, `git rev-parse HEAD`,
`git diff --cached --binary`, `git show :<each staged path>`,
`git rev-parse :<each staged path>`. Read-only cat/sed/rg reads covered the
active skills/template, task brief/verification/preflight/results, prior
reviews, installer/tests/guides and governing plan/parent/task-map references.
Identity collection used hashlib SHA-256 over actual bytes, not a tree-writing
Git operation.

## 6. Aggregate-gate record

| Field | Value |
|---|---|
| Command | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py` |
| Status | passed |
| Owner / stage | this independent correction discovery 3 |
| Reason | V-01–V-07 and R-01–R-03 reconciled against authority and scoped diff; all selected targeted probes completed cleanly before launch; no blocked/unchecked rows |
| Current evidence | 33 tests OK, 12.291 seconds, exit 0, no skips |

Prior gates are historical, not this gate's proof. The pre-existing
maintainability-02 record matches current implementation/test/guide blobs;
its decision authority is separate. No registry or required architecture
command is declared by this task's applicable authority. No extra gate was added.

## 7. Scope and baseline

The four production/test/guide paths are exactly the task's allowed scope.
The staged results and four historical review artifacts are task submission
context, not production or independently authenticated claims. The untracked
maintainability-02 report predates this invocation and was preserved. There
is no unexplained overlap or tracked worktree/index divergence.

Preflight records the older .1 baseline HEAD 93cd0e4; current HEAD is f6046d8b1a48f1984ad025589dca4a01c2fa87c9.
The prior discovery reports also record current HEAD; the task brief hash
still matches verification/preflight. The .1 dependency interface is present
and the current aggregate exercises installation compatibility. No plan,
brief, prior report or installed skill was edited.

Separate index/worktree identities (matching staged bytes independently checked):

| Path | Index blob | Worktree SHA-256 |
|---|---|---|
| README.md | f71a050649d3ae91744649c709704e9ec8f2d807 | 34ba8cab489af2608eb4e2a70c1c4e947fd38d81430dbcd010e47bb317da5aec |
| docs/tasks/T-004.2/results.md | 409417ca54eb1878178431a07703534157fde599 | 7bad160af3b6d69826164fd2ba1403ec40e855c6e782e1decb3a83f345680a83 |
| docs/tasks/T-004.2/reviews/discovery-01.md | caa680abed8e73abcb183f3f2396f706da27edba | 3894d340174d81e5daef778c83e05ce96f394d56a03ab071bc81b27f6d3a0607 |
| docs/tasks/T-004.2/reviews/discovery-02.md | 50264cc9194fcadc74019cf3774fb1374f4ff040 | 4d1067142a42315b2baa75dbadb599ace564eea1c17a07f60704766c72639dc9 |
| docs/tasks/T-004.2/reviews/discovery-03.md | 098724582b7205cb0b2802c14769985619eda4e1 | eb7e3cc05a4f65c880a224aee88d91bccec0b7ea8b076c9d3d92ebd62eb29dbe |
| docs/tasks/T-004.2/reviews/maintainability-01.md | e1ec29948a4ee47bedd5d9afa7a01a8d1ed86530 | 555e42891ffe3e63afd6d6bf750ec5ecce10a929fa18f8b96bb8f8ba3e63c53a |
| scripts/install_development_skills.py | 72561b046b498f72a65b68f04122f1de716bb415 | 6815722f30ec1b8da0dffc1a47d0ce5d9c37d159377250bd519bebca2024aa87 |
| skills/README.md | 334a2364d1bc05026d2b12978a1cfba7b91b411f | 8e8e5b0db9169071e28f78a0af4d1de8661102ae83f48012014e127edf946503 |
| tests/test_install_development_skills.py | b61717e27319cd590247bce8f5820037c8901f0d | 0a501920618f2a9dadca726286bfef7d86fb7053173058c755fcb0f9a18094d1 |
| docs/tasks/T-004.2/brief.md | not staged; preparation or pre-existing review | ecf57bb5cb33dda3405269c3f6adf05628248d2a4510fe34358d98d8e027512e |
| docs/tasks/T-004.2/verification.md | not staged; preparation or pre-existing review | 4966f69350e20d8563532d172e26acb6a8536e0c64635a62be0fb11f393c24b8 |
| docs/tasks/T-004.2/preflight.md | not staged; preparation or pre-existing review | 8f8af39476e7d6d7960b9f3f0e14efe766383dee54d64db784445ee882c40d1b |
| docs/tasks/T-004.2/reviews/maintainability-02.md | not staged; preparation or pre-existing review | 305dadc736ddd6cf46d96512e24ff73f6b1cd037a4e263adbd74aa77094ce1b1 |

Exact status before the report write:

```text
M  README.md
A  docs/tasks/T-004.2/results.md
A  docs/tasks/T-004.2/reviews/discovery-01.md
A  docs/tasks/T-004.2/reviews/discovery-02.md
A  docs/tasks/T-004.2/reviews/discovery-03.md
A  docs/tasks/T-004.2/reviews/maintainability-01.md
M  scripts/install_development_skills.py
M  skills/README.md
M  tests/test_install_development_skills.py
?? docs/tasks/T-004.2/reviews/maintainability-02.md
```

Exact status after the report write:

```text
M  README.md
A  docs/tasks/T-004.2/results.md
A  docs/tasks/T-004.2/reviews/discovery-01.md
A  docs/tasks/T-004.2/reviews/discovery-02.md
A  docs/tasks/T-004.2/reviews/discovery-03.md
A  docs/tasks/T-004.2/reviews/maintainability-01.md
M  scripts/install_development_skills.py
M  skills/README.md
M  tests/test_install_development_skills.py
?? docs/tasks/T-004.2/reviews/discovery-04.md
?? docs/tasks/T-004.2/reviews/maintainability-02.md
```

The post-write audit confirmed that only this new report entry differs,
the index diff digest is unchanged and all reviewed index/worktree bytes
retain the identities above. This report is the sole repository write.

## 8. Questions and residual risks

No blocked/unchecked work or unresolved scope question.

Point-in-time path/type/byte snapshots do not prove absence of a write fully
undone before observation; static check tracing supplies complementary evidence:
check calls validation/comparison and Git root lookup, with no install,
staging, availability or run-start path. This local evidence does not establish
cross-platform behavior, concurrent filesystem mutation safety, retained
versions or installed skill-call compliance. Those claims are not made.
Preflight's note about no separate .1 acceptance report remains historical
plan-owner context, not an invented completed decision.

## 9. Coverage and next route

Coverage is complete for the bounded .2 authority. No findings.
Next: a separate task-acceptance-review call consumes this report, current
staged diff, task brief, verification revision 1, ready preflight, recorded
brief sizing/decision context, results.md, maintainability-02, historical
discovery-01–03 and the reviewer commands below. No acceptance decision was made.

## 10. Discovery continuation

```markdown
Discovery continuation:
- Iteration / current byte identity: correction discovery 3; HEAD f6046d8b1a48f1984ad025589dca4a01c2fa87c9; staged diff SHA-256 c3a871c55660d5ec1cfa70f49f6a7ab07ec6011066f0def66cce8ee89f38c7b5; index/worktree identities in section 7.
- Coverage rows: V-01, V-02, V-03, V-04, V-05, V-06, V-07, R-01, R-02, R-03 = pass on current bytes; none blocked or unchecked.
- Finding IDs: no current findings; historical F-01/F-02/F-03 triggers independently corroborated as corrected.
- Finding/scenario continuity: discovery-03 V-01/V-02/V-07/R-01/R-02 failed F-03; current producer correction claims in results.md corroborated by D-01/D-02; all now pass. Prior V-03/V-04/V-05/V-06/R-03 passes rerun rather than copied. F-01 denial siblings and F-02 linked-source siblings remain covered by D-01; multiple/sibling/nested aliases and true cycles by D-02. No incomplete reason. Correction owner: implementer if new bytes are needed; evidence owner: this discovery for identified bytes; authority/disposition owner: separate acceptance call.
- Preparation/context: docs/tasks/T-004.2/brief.md (recorded sizing/decision context); verification.md revision 1; preflight.md ready; results.md; reviews/maintainability-02.md; discovery-01–03.
- Reviewer regressions: tests/test_install_development_skills.py; exact focused command D-01; reproducible reviewer commands Appendices A/B.
- Aggregate gate: D-04 passed, owned by this correction discovery after clean targeted reconciliation; exact command in section 6.
- Next: separate task-acceptance-review using the brief, current staged diff, this report and all listed preparation/conditional references.
```

## Appendix A — D-02 exact reproducible probe

```bash
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import importlib.util, tempfile, pathlib, subprocess, sys, json, os, shutil
spec=importlib.util.spec_from_file_location("fixture", "tests/test_install_development_skills.py")
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
P=pathlib.Path
def run(cli, target, check=True):
    return subprocess.run([sys.executable,str(cli),*(["--check"] if check else []),str(target)],capture_output=True,text=True,timeout=20)
def twice(cli,target,code):
    before=m.snapshot_tree(target)
    a=run(cli,target); b=run(cli,target)
    assert a.returncode==b.returncode==code,(a,b)
    assert (a.stdout,a.stderr)==(b.stdout,b.stderr)
    assert before==m.snapshot_tree(target)
    return json.loads(a.stdout) if a.stdout else a.stderr
with tempfile.TemporaryDirectory() as td:
    base=P(td)
    source_before=m.source_projection_snapshot()
    for committed in (False,True):
        for kind in ("match","drift","failure","absent"):
            target=base/(str(committed)+kind); target.mkdir()
            m.init_repo(target,commit=committed)
            if kind!="absent":
                assert run(m.INSTALLER_PATH,target,False).returncode==0
            denied=None
            if kind=="drift":
                (target/".agents/skills/README.md").write_bytes(b"drift")
            if kind=="failure":
                denied=target/".agents/skills/project-direction/SKILL.md"
                denied.chmod(0)
            try:
                twice(m.INSTALLER_PATH,target,{"match":0,"drift":1,"failure":2,"absent":1}[kind])
                if kind=="absent": assert not (target/".agents").exists()
            finally:
                if denied: denied.chmod(0o644)
    assert source_before==m.source_projection_snapshot()
    print("eight result/Git combinations: repeated outputs and full snapshots unchanged")
    target=base/"families"; target.mkdir(); m.init_repo(target)
    assert run(m.INSTALLER_PATH,target,False).returncode==0
    paths=[f".agents/{rel}/SKILL.md" for _,rel in m.installer.DEVELOPMENT_SKILL_SOURCES]
    paths += [f".agents/scripts/{n}" for n in m.installer.SHARED_SCRIPT_FILES]
    for rel in paths:
        p=target/rel; original=p.read_bytes()
        for category in ("changed","missing"):
            if category=="changed": p.write_bytes(b"reviewer drift")
            else: p.unlink()
            info=twice(m.INSTALLER_PATH,target,1)
            assert info["differences"]==[{"category":category,"path":rel}],info
            p.write_bytes(original)
    print("20 selected packages and six shared files: changed/missing exact diagnostics")
    source,cli=m.DevelopmentProfileCheckTests().build_relocated_source_distribution(base)
    package=source/"skills/project-direction"
    outside=base/"outside"; outside.mkdir(); (outside/"proof.txt").write_bytes(b"alias proof")
    for name in ("alias-a","alias-b"): (package/name).symlink_to(outside,target_is_directory=True)
    (package/"sibling").symlink_to(package/"references",target_is_directory=True)
    nested=package/"nested"; nested.mkdir(); (nested/"alias-c").symlink_to(outside,target_is_directory=True)
    alias_target=base/"alias-target"; alias_target.mkdir(); m.init_repo(alias_target)
    assert run(cli,alias_target,False).returncode==0
    before=m.snapshot_tree(source)
    info=twice(cli,alias_target,0)
    assert info["compared_paths"]==len(m.expected_managed_paths())+3+len(m.collect_package_files(package/"references"))
    copied=alias_target/".agents/skills/project-direction/nested/alias-c/proof.txt"
    copied.unlink()
    info=twice(cli,alias_target,1)
    assert info["differences"]==[{"category":"missing","path":".agents/skills/project-direction/nested/alias-c/proof.txt"}]
    assert before==m.snapshot_tree(source)
    (outside/"back").symlink_to(package,target_is_directory=True)
    diagnostic=twice(cli,alias_target,2)
    assert "directory cycle" in diagnostic and "source skill directory" in diagnostic
    print("multiple, sibling and nested aliases: match, exact per-copy drift, bounded true-cycle failure")
print("all reviewer fixtures removed")
PY
```

## Appendix B — D-03 exact reproducible probe

```bash
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import importlib.util,tempfile,pathlib,subprocess,sys,os,shutil
spec=importlib.util.spec_from_file_location("fixture","tests/test_install_development_skills.py")
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
P=pathlib.Path
def run(cli,target):
    return subprocess.run([sys.executable,str(cli),"--check",str(target)],capture_output=True,text=True,timeout=20)
with tempfile.TemporaryDirectory() as td:
    base=P(td); target=base/"target"; target.mkdir(); m.init_repo(target)
    outside=base/"outside"; outside.mkdir(); (outside/"proof").write_bytes(b"preserve")
    paths=[".agents",".agents/skills",".agents/scripts",".agents/skills/project-direction",".agents/scripts/run_evidence.py",".agents/skills/README.md","AGENTS.md"]
    for rel in paths:
        p=target/rel; p.parent.mkdir(parents=True,exist_ok=True)
        original=p.read_bytes() if p.is_file() else None
        if original is not None: p.unlink()
        for shape in ("symlink","wrong-type"):
            if shape=="symlink": p.symlink_to(outside,target_is_directory=True)
            elif rel in paths[:4]: p.write_bytes(b"wrong")
            else: p.mkdir()
            before=m.snapshot_tree(target); external=m.snapshot_tree(outside)
            a=run(m.INSTALLER_PATH,target)
            assert a.returncode==2 and not a.stdout and str(p) in a.stderr,a
            assert before==m.snapshot_tree(target) and external==m.snapshot_tree(outside)
            if p.is_symlink() or p.is_file(): p.unlink()
            else: p.rmdir()
        if original is not None: p.write_bytes(original)
    source,cli=m.DevelopmentProfileCheckTests().build_relocated_source_distribution(base)
    (source/"scripts/ollama-models.json").unlink()
    before=m.snapshot_tree(source); target_before=m.snapshot_tree(target)
    a=run(cli,target)
    assert a.returncode==2 and not a.stdout and "scripts/ollama-models.json" in a.stderr,a
    assert before==m.snapshot_tree(source) and target_before==m.snapshot_tree(target)
print("14 unsafe path shapes and real relocated missing-source failure: precise exit 2, snapshots unchanged; fixtures removed")
PY
```

