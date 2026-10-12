# Task Review Discovery Report: T-004.2 — Read-only development-profile checking

| Field | Value |
|---|---|
| Producing stage | `task-review-discovery`, project-local installed skill |
| Coverage completeness | complete — all V-01–V-07 and R-01–R-03 have current evidence; failures remain visible |
| Iteration / date | first independent discovery; 2026-10-12, Europe/Lisbon |
| Repository | `/Users/mtrusov/work/skill-sources/personal-skills` |
| Report | `docs/tasks/T-004.2/reviews/discovery-01.md` |
| Authority | `docs/tasks/T-004.2/brief.md`; cited project plan ART-009–011, IF-007, INV-009, FLOW-004 |
| Preparation | `docs/tasks/T-004.2/verification.md`, revision 1; `docs/tasks/T-004.2/preflight.md` |
| Submission | staged `docs/tasks/T-004.2/results.md`, producer claim `READY_FOR_REVIEW` |

This report publishes evidence only. It gives no acceptance verdict, approved
deferral, or advancement. It applies to the identified staged bytes; it does
not review or authenticate itself. Corrections require fresh discovery.

## 1. Provenance and byte identity

This session authored none of the reviewed production, test, documentation,
or submission bytes. Its evidence is independent of production authorship.
The active skill was resolved from
`.agents/skills/task-implementation-flow/task-review-discovery/SKILL.md`;
its report template was read from that installation. Test inspection used
`.agents/skills/testing-discipline/SKILL.md`. Neither installation was refreshed.

- HEAD: `f6046d8b1a48f1984ad025589dca4a01c2fa87c9`.
- Index tree at review: `0932b5a8cbf8394a66fd3cb16b774be0b1985bd1`.
- SHA-256 of `git diff --cached --binary`:
  `6504c61e57a21ea936c80a92f79f2b1cbb123664c755cdfd74cd1c7b11430b71`.
- `git diff --name-only` was empty. All five staged files were separately
  read from the index and worktree and compared byte for byte.
- No prior T-004.2 discovery report or reviewer regression was present.

## 2. Confirmed finding

### F-01 [suggested P2] Unreadable managed directories can report a match

| Field | Evidence |
|---|---|
| Location | `scripts/install_development_skills.py:337`, `_collect_projection_files` |
| Trigger | Install a matching profile. Add `reviewer-unreadable/extra.txt` inside selected `project-direction`. Check while readable, then chmod its directory to `000` and check again as a non-root user. |
| Consequence | Readable extra content correctly produces exit 1 / unexpected drift. With enumeration denied, the same extra content disappears from comparison: exit 0, `match: true`, empty differences, empty stderr. Maintainers and subprocess callers receive a false clean result. |
| Additional observed case | Chmod installed `project-direction/references` to `000`: exit 1 reports `references/direction-template.md` as missing, with no read-failure diagnostic, despite the file still existing. Documented failure semantics require exit 2 for unreadable required content. |
| Evidence | DISC-02, real public CLI on Python 3.14.6, uid 501. `Path.rglob` silently skips directories it cannot enumerate; `_read_required` never sees omitted paths. Restoring permissions restores correct results. |
| Affected AC | AC-01, AC-02, AC-03; R-01 and R-02 / INV-009 |
| Broken invariant | A match requires complete managed-content comparison. Required enumeration failures must remain distinguishable from ordinary missing-content drift. |
| Credible sibling surface | Unreadable reference/eval/setup subdirectories in every selected source or target package, including additional owned target subtrees that have no corresponding expected source path. Both sides use this collector. |
| Corrective direction | Make managed-tree enumeration propagate inaccessible-directory and metadata failures with path/scope diagnostics. Preserve true absence and transient exclusions; add public-boundary evidence for expected and unexpected unreadable subtrees. |

## 3. Completeness ledger

The V-01–V-07 ledger was reconstructed from revision 1 before aggregate
consideration. DISC-01 corroborated the supplied tests; DISC-02 selected the
directory-enumeration adversary. DISC-03 filled submission omissions without
editing tests. Results below combine current test execution and independent
filesystem probes, not producer pass labels.

| Row | AC / risk | Cases and setup/oracle | Submitted evidence | Independent evidence | Result |
|---|---|---|---|---|---|
| V-01 | AC-01/02/05; R-01/02 | Real positional installs in committed/unborn repos; public check must return 0, true match, empty differences, independently enumerated path count | Fresh-install match test | DISC-01, both variants ran | pass |
| V-02 | AC-01/02/03; R-01/02 | Changed/missing SKILL.md, reference, eval/setup, guide, helper/config/schema; whole missing package; extra owned file; unchanged workflow fingerprint after eval mutation; exact path/category oracle | Seven drift families, whole-package and fingerprint tests | DISC-01 plus DISC-03's changed/missing mutations for all 20 packages and all six shared files; DISC-02 unreadable extra contrast | fail — F-01 bypasses unexpected-file detection; readable families pass |
| V-03 | AC-02/03; R-01/02 | Unselected skill/helper, other `.agents` content, outside-block text, all four transient patterns versus owned non-transient extra; public match/drift contrast | Unmanaged/transient test | DISC-01; static `_is_transient` trace mirrors existing copy patterns | pass |
| V-04 | AC-01/02/03; R-01/02 | Changed block, absent block/file, unmatched, duplicate and reversed markers; exact AGENTS drift or precise exit-2 failure | Marker test | DISC-01; marker parser traced to public CLI | pass |
| V-05 | AC-01/03; R-02 | Missing/non-Git/non-root target; real missing source; unreadable required file/directory; symlink and wrong-type refusal at installation roots, selected destination, shared file, guide, AGENTS; no outside changes | Target/source failure test; chmod-file test | DISC-01; DISC-02 real directory denial; DISC-03 all 14 refusal cases with target/outside snapshots; DISC-04 real missing-source public CLI | fail — unreadable file correctly fails, but directory failures are suppressed (F-01); other cases pass |
| V-06 | AC-04; R-03 | Match/drift/failure/absent installation in both Git states, each checked twice; compare source and complete target snapshots including Git/evidence, repeat stdout/stderr and no created `.agents` | Snapshot test covers five of eight combinations | DISC-01; DISC-03 independently covers all eight combinations and repeats; static path has no install/stage/availability/run-start call | pass — point-in-time snapshot/read-only boundary evidence |
| V-07 | AC-05 | Positional install and check from unrelated CWD; unchanged unmanaged bytes; source from installer location; both guides agree with outcomes/scope/refresh semantics | Unrelated-CWD and guide test | DISC-01 and inspection of both staged guides and `main` | pass |
| R-01 | AC-02/03; INV-009 | Full managed projection and exact drift | Producer V-01–04 claims | V-01–04 above | fail — F-01; normal readable projection covered |
| R-02 | AC-01/03; INV-009 | Truthful outcomes, ownership, unsafe/unreadable inputs | Producer V-01–05 claims | V-01–05 above | fail — F-01; failures otherwise distinct |
| R-03 | AC-04; INV-009 | All results, both Git states, repeated checks and absence | Producer V-06 claim | V-06 above | pass |

No required row is blocked or unchecked. There is no changed executable
schema contract: selected schemas are compared as bytes. This task does not
change their validator behavior. No process-lifecycle invariant is in scope.

## 4. Adversarial evidence and submission gaps

- Selected/unselected contrast: extra selected file reports drift; extra
  unselected helper is ignored. Denying enumeration of the selected extra
  subtree changes that result to a false match (DISC-01/02).
- Complete selection: changed and missing SKILL.md in each of 20 packages,
  and changed/missing each of six shared files, produced exact differences
  (DISC-03). Producer mutation tests cover three packages and three shared
  files; their baseline count test is not behavioral drift evidence for the
  omitted selections.
- Failure refusals: DISC-03 fills omitted source/target refusal families.
- Read-only matrix: DISC-03 fills unborn drift/failure and committed absence
  missing from the submitted snapshot test. These omissions are recorded as
  submitted-evidence gaps; they are not presented as production failures.

## 5. Commands and independent results

All commands ran from the repository root locally, with
`PYTHONDONTWRITEBYTECODE=1`; Python 3.14.6, non-root uid 501. No network/model
calls, dependency installation, privilege escalation, or active installation
refresh occurred. Disposable targets were installed only for probe setup.
All subprocesses returned and temporary fixtures were removed by their
context managers; permission changes were restored before cleanup.

| ID | Exact command or reproducible probe | Result / cleanup |
|---|---|---|
| DISC-01 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py -k check_` | 11 tests OK, 6.688s, no skips; submitted scenario behavior independently rerun |
| DISC-02 | `PYTHONDONTWRITEBYTECODE=1 python3 -` with Appendix A | Script exit 0 records behavioral failures: readable extra exit 1; denied extra exit 0 / true / empty; denied required directory exit 1 / missing reference. Permissions restored; final baseline matched; fixture cleaned. |
| DISC-03 | `PYTHONDONTWRITEBYTECODE=1 python3 -` with Appendix B | Exit 0; 52 exact changed/missing cases, 14 refusal cases, eight repeated read-only combinations; all assertions passed; fixtures cleaned. |
| DISC-04 | Copy current installer alone into `<temporary-source>/scripts/`; run `python3 <temporary-source>/scripts/install_development_skills.py --check <repository-root>` via `subprocess.run(capture_output=True, text=True)`; compare all copied-source file bytes before/after | Exit 2, empty stdout, stderr identifies `source repository is missing development-profile inputs`; copied-source bytes unchanged; temporary source cleaned. This validates from the relocated real CLI, without fabricating `check` results. |
| DISC-05 | `git rev-parse HEAD`; `git write-tree`; `git ls-files --stage README.md docs/tasks/T-004.2/results.md scripts/install_development_skills.py skills/README.md tests/test_install_development_skills.py`; `git diff --name-only`; compare `git show :<path>` bytes with each worktree file and SHA-256; hash `git diff --cached --binary` | Index/worktree equality and identities in sections 1/7. `git write-tree` returned the already-existing index tree. No status/index changes. |

## 6. Aggregate gate

| Field | Record |
|---|---|
| Command | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py` |
| Status | not run |
| Owner / stage | independent reviewer, initial discovery |
| Reason | Decisive targeted failure DISC-02 suppresses the aggregate under the active discovery workflow. Other safe independent probes continued. |
| Current evidence | DISC-01 green targeted tests; DISC-02 F-01; DISC-03/04 clean sibling probes. Producer's 28-test aggregate claim is submission evidence, not this review's aggregate. |

The results document says discovery consumes the producer aggregate without
repeating it. That sentence cannot override the brief/active discovery
workflow: fresh discovery owns the justified aggregate after clean targeted
evidence. A correction pass must rerun F-01 regressions and then own the gate.

## 7. Scope and baseline

The four production/test/guide paths are brief-authorized. The staged results
file is the repository-required submission artifact. No unexplained overlap,
unstaged modifications, or unrelated staged paths were found. Plans,
preparation, installed skills, tests and prior reports were not edited.

Preflight HEAD `93cd0e4` moved to current `f6046d8` by the package-preparation
commit as the producer records. Current brief hash matches its recorded
authority. No separate decision-context file is supplied; the brief's finite
risks and cited plan are the recorded context. T-004.1 acceptance is not
separately recorded, as preflight notes; the task authority declares that
dependency reviewed. This review makes no new dependency verdict.

| Path | Index blob | Worktree/index SHA-256 (separately read; equal) |
|---|---|---|
| README.md | `6323119b5e44dafefb4d582f95fdad3a48bb98e7` | `dea10a0e7469bb4bace1370045390cd9aaf4065ee3d832ad8b88405e6d58ce4b` |
| docs/tasks/T-004.2/results.md | `0a1ecf7b6c39de9267245a99752f5e3107da44ee` | `4e534a859c19999f8353361e64042ae7cd2cbd5fd3812e90cb80d417ee8c2430` |
| scripts/install_development_skills.py | `e6b41b60ec9f77afb3674d665367fafeffababe1` | `a50208d57ecf0c2435576cf1478bf6b8dbfd00fe4f1c42e16a0ece824b1a84f6` |
| skills/README.md | `26c00d7b00a88307c7748e4ed68fd82c37b1a7e0` | `444b828e60931e7501efe160144342c306b0a40fe330b7db5a0485d0e0d99b5c` |
| tests/test_install_development_skills.py | `95a286fa3d7d03f90fcc097cfa32e5d9725531aa` | `025bf67216c43e704efc3e0c91f8ec84bee129f892bd62557c283e0051dbae70` |

Preparation SHA-256:

- brief: `ecf57bb5cb33dda3405269c3f6adf05628248d2a4510fe34358d98d8e027512e`.
- verification revision 1: `4966f69350e20d8563532d172e26acb6a8536e0c64635a62be0fb11f393c24b8`.
- preflight: `8f8af39476e7d6d7960b9f3f0e14efe766383dee54d64db784445ee882c40d1b`.

Exact reviewed status before the report write (`git status --short --untracked-files=all`):

```text
M  README.md
A  docs/tasks/T-004.2/results.md
M  scripts/install_development_skills.py
M  skills/README.md
M  tests/test_install_development_skills.py
```

Observed and verified post-write status (same command):

```text
M  README.md
A  docs/tasks/T-004.2/results.md
M  scripts/install_development_skills.py
M  skills/README.md
M  tests/test_install_development_skills.py
?? docs/tasks/T-004.2/reviews/discovery-01.md
```

Only the new untracked report differs. The staged diff hash and all five
index/worktree byte comparisons were rechecked and unchanged. The report is
excluded from reviewed-byte identity. No staging, resetting, committing, or
ownership changes occurred.

## 8. Residual risks and next route

No required row is unfinished. Point-in-time snapshots do not prove the
absence of writes that fully undo themselves; the static check call path
supplements the observed snapshots. Evidence is local to this platform, not
cross-platform or installed skill-call qualification. Refresh composition
belongs to T-004.3. Discovery does not waive any applicable conditional
maintainability review; the acceptance owner must account for that policy.

Coverage is complete with F-01. Next: a separate `task-acceptance-review`
call consumes the brief, current staged diff, this report, verification
revision 1, preflight, cited plan context, and regression probes below.
There are no blocked/unchecked rows to omit or defer.

## 9. Discovery continuation

```text
Discovery continuation:
- Iteration / bytes: first independent pass; HEAD f6046d8b1a48f1984ad025589dca4a01c2fa87c9; staged diff SHA-256 6504c61e57a21ea936c80a92f79f2b1cbb123664c755cdfd74cd1c7b11430b71; index/worktree equal.
- Coverage: V-01 pass; V-02 fail F-01; V-03 pass; V-04 pass; V-05 fail F-01; V-06 pass; V-07 pass; R-01 fail; R-02 fail; R-03 pass. No blocked/unchecked rows.
- Findings: F-01 suggested P2, inaccessible managed-tree enumeration silently omitted.
- Continuity: no prior discovery. Producer claims all V rows passed (results.md); current independent DISC-02 disproves V-02/V-05 directory behavior. Other current evidence DISC-01/03/04. No incomplete rows. Correction owner: implementer; evidence owner: fresh discovery; authority/decision owner: separate acceptance. Siblings: source/target reference/eval/setup trees and unexpected selected-package subtrees.
- Preparation: docs/tasks/T-004.2/brief.md; verification.md revision 1; ready preflight.md; brief finite-risk R-01–03 and cited project-plan ART-009–011/IF-007/INV-009/FLOW-004 context.
- Reviewer regressions: no repository test edits. Rerun Appendix A via PYTHONDONTWRITEBYTECODE=1 python3 -; corrected oracle is exit 2 with scoped read/enumeration diagnostics for both denied directories. Appendix B and DISC-01 retain sibling coverage.
- Aggregate: not run; independent initial discovery owner; targeted F-01 suppresses PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py. Correction discovery owns it after clean targeted evidence.
- Next: separate task-acceptance-review with current staged diff and the complete package/report context.
```

## Appendix A — DISC-02 exact probe body

Run with `PYTHONDONTWRITEBYTECODE=1 python3 -` from the repository root.
The script prints the observed defect; its own exit 0 is not a behavioral pass.

```python
import importlib.util, json, os, sys, tempfile
from pathlib import Path
spec = importlib.util.spec_from_file_location('fixture', 'tests/test_install_development_skills.py')
t = importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
print('python', sys.version.split()[0], 'uid', os.geteuid())
with tempfile.TemporaryDirectory() as td:
    repo = Path(td); t.init_repo(repo)
    result = t.run_installer(repo); assert result.returncode == 0, result.stderr
    baseline = t.run_check(repo); assert baseline.returncode == 0, baseline.stderr
    hidden = repo / '.agents/skills/project-direction/reviewer-unreadable'
    hidden.mkdir(); (hidden / 'extra.txt').write_bytes(b'extra owned bytes\n')
    visible = t.run_check(repo)
    print('readable-owned-extra', visible.returncode, json.loads(visible.stdout)['differences'])
    hidden.chmod(0)
    try:
        result = t.run_check(repo)
        print('unreadable-owned-extra', result.returncode, json.loads(result.stdout)['match'], json.loads(result.stdout)['differences'], repr(result.stderr))
    finally:
        hidden.chmod(0o700)
    hidden.joinpath('extra.txt').unlink(); hidden.rmdir()
    refs = repo / '.agents/skills/project-direction/references'
    refs.chmod(0)
    try:
        result = t.run_check(repo)
        print('unreadable-required-directory', result.returncode, json.loads(result.stdout)['differences'], repr(result.stderr))
    finally:
        refs.chmod(0o755)
    assert t.run_check(repo).returncode == 0
print('fixture cleaned')
```

## Appendix B — DISC-03 exact probe body

Run with `PYTHONDONTWRITEBYTECODE=1 python3 -` from the repository root.

```python
import importlib.util, json, os, subprocess, sys, tempfile
from pathlib import Path
spec = importlib.util.spec_from_file_location('fixture', 'tests/test_install_development_skills.py')
t = importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
with tempfile.TemporaryDirectory() as td:
    base = Path(td); repo = base / 'projection'; repo.mkdir(); t.init_repo(repo)
    assert t.run_installer(repo).returncode == 0
    paths = ['.agents/' + relative + '/SKILL.md' for _, relative in t.installer.DEVELOPMENT_SKILL_SOURCES]
    paths += ['.agents/scripts/' + name for name in t.installer.SHARED_SCRIPT_FILES]
    for rel in paths:
        p = repo / rel; original = p.read_bytes()
        try:
            for category in ('changed', 'missing'):
                if category == 'changed': p.write_bytes(b'reviewer drift\n')
                else: p.unlink()
                r = t.run_check(repo)
                assert r.returncode == 1, (rel, r.stderr)
                assert json.loads(r.stdout)['differences'] == [{'category': category, 'path': rel}], r.stdout
                p.write_bytes(original)
        finally:
            p.write_bytes(original)
    print('V-02: changed/missing exact diagnostics for', len(paths), 'paths (20 packages, 6 shared files)')
    refusals = ['.agents', '.agents/skills', '.agents/scripts', '.agents/skills/project-direction', '.agents/scripts/run_evidence.py', '.agents/skills/README.md', 'AGENTS.md']
    outside = base / 'outside'; outside.mkdir(); (outside / 'canary').write_bytes(b'unchanged')
    outside_before = t.snapshot_tree(outside)
    for rel in refusals:
        p = repo / rel; saved = base / 'saved'; was_dir = p.is_dir(); p.rename(saved)
        try:
            for shape in ('symlink', 'wrong-type'):
                if shape == 'symlink': p.symlink_to(outside if was_dir else outside / 'canary')
                elif was_dir: p.write_bytes(b'wrong type')
                else: p.mkdir()
                before = t.snapshot_tree(repo)
                r = t.run_check(repo)
                assert r.returncode == 2 and not r.stdout and 'error:' in r.stderr, (rel, shape, r)
                assert str(p) in r.stderr, r.stderr
                assert before == t.snapshot_tree(repo)
                if p.is_symlink() or p.is_file(): p.unlink()
                else: p.rmdir()
        finally:
            if p.is_symlink() or p.is_file(): p.unlink()
            elif p.exists(): p.rmdir()
            saved.rename(p)
    assert outside_before == t.snapshot_tree(outside)
    print('V-05: 14 symlink/wrong-type refusal cases; unchanged target/outside snapshots')
    source_before = t.source_projection_snapshot()
    for commit in (False, True):
        for state, exit_code in [('match', 0), ('drift', 1), ('failure', 2), ('absent', 1)]:
            fixture = base / (state + str(commit)); fixture.mkdir(); t.init_repo(fixture, commit=commit)
            blocked = None
            if state != 'absent':
                assert t.run_installer(fixture).returncode == 0
            if state == 'drift': (fixture / '.agents/skills/README.md').write_bytes(b'drift')
            if state == 'failure':
                blocked = fixture / '.agents/skills/project-direction/SKILL.md'; blocked.chmod(0)
            before = t.snapshot_tree(fixture)
            try:
                first = t.run_check(fixture); second = t.run_check(fixture)
                assert first.returncode == second.returncode == exit_code, (state, first.stderr)
                assert (first.stdout, first.stderr) == (second.stdout, second.stderr)
                assert before == t.snapshot_tree(fixture), state
                if state == 'absent': assert not (fixture / '.agents').exists()
            finally:
                if blocked: blocked.chmod(0o644)
    assert source_before == t.source_projection_snapshot()
    print('V-06: all 8 result/repository combinations twice; unchanged file/Git/evidence/source snapshots')
print('all disposable fixtures cleaned')
```
