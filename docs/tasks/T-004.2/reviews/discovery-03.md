# Task Review Discovery Report: T-004.2 — Read-only profile checking

| Field | Value |
|---|---|
| Producing stage | `task-review-discovery`, project-local installed skill |
| Coverage completeness | complete — all V-01–V-07 and R-01–R-03 have current behavioral evidence, including the failure below |
| Discovery iteration | correction discovery 2, following discovery-02 F-02 |
| Created at | 2026-10-12, Europe/Lisbon |
| Repository root | `/Users/mtrusov/work/skill-sources/personal-skills` |
| Durable report | `docs/tasks/T-004.2/reviews/discovery-03.md` |
| Authority | `docs/tasks/T-004.2/brief.md`; cited project-plan, parent T-004 brief and task-map |
| Preparation | `docs/tasks/T-004.2/verification.md`, revision 1; `docs/tasks/T-004.2/preflight.md`, ready |
| Submission | staged `docs/tasks/T-004.2/results.md`, `READY_FOR_REVIEW`, after F-01/F-02 corrections |

This report publishes evidence only. It contains no acceptance verdict, approved
deferral or advancement. It applies only to the identified reviewed bytes. A
separate acceptance decision call consumes it. This report does not review or
authenticate itself.

## 1. Discovery provenance

This session authored no reviewed production, test, guidance or submission bytes.
The evidence is independent of production authorship. Active skill installation:
`.agents/skills/task-implementation-flow/task-review-discovery/SKILL.md`; its
report template was read. Test inspection also used the installed project-local
`.agents/skills/testing-discipline/SKILL.md`. No installation was refreshed.

HEAD: `f6046d8b1a48f1984ad025589dca4a01c2fa87c9`.
SHA-256 of `git diff --cached --binary`:
`5786a6780f6fbf7ce4163f8066e5158ce96486812aced5e616bf351f626da57f`.
Each of the eight staged paths was independently read from the index and
worktree; bytes matched. `git diff --name-only` was empty. No index/tree writes
were used to identify the reviewed bytes.

## 2. Confirmed findings

### F-03 [suggested P2] Acyclic source aliases are falsely rejected as cycles

| Field | Evidence |
|---|---|
| Location | `scripts/install_development_skills.py:362`, `:379–383`, `_collect_projection_files`; install copying at `:200` |
| Trigger | Two directory links within one selected source package point to the same external directory, or an inner link points to an existing sibling directory. Run the real positional installer from that complete disposable source distribution, then `--check` on its successful installation. |
| Consequence | A fully installed, exact projection reports check failure (exit 2, empty stdout) with a false `directory cycle` diagnostic. The maintainer cannot obtain a match for these valid installer-supported distributions. |
| Evidence | D-03 / Appendix A: two external aliases install successfully and both copied files contain the expected bytes; two consecutive checks exit 2. Removing one alias and its copied target subtree restores exit 0 / true match. A real `references` directory plus `references-alias` also installs successfully, then exits 2 on check. |
| Affected AC | AC-01, AC-02, AC-05; V-01/V-02/V-07; R-01/R-02, INV-009 |
| Broken invariant | Check enumeration must describe the complete projection accepted and materialized by the canonical installer. A repeated directory identity at a different acyclic source path is valid copied content, not a recursion cycle. |
| Credible sibling surface | Directory-linked references, evals or setup trees in any selected package; multiple links to the same shared subtree and a regular subtree plus a link to it. All share the per-package global `visited` set. |
| Smallest corrective direction | Distinguish recursive ancestor cycles from independent acyclic paths to the same directory, and compare every path the installer materializes. Preserve bounded true-cycle failure, target traversal refusals, transient exclusions and enumeration-error propagation. |

Context and exposure: the source distribution explicitly supports linked
content, and the guides now document equivalence with install-time copying.
Aliases are a bounded source-layout case rather than a failure of ordinary
unlinked installations. The impact is incorrect profile qualification and a
misleading failure diagnostic; no data loss or check-time mutation was observed.
The single-alias contrast is a mitigation only for that narrower layout; it
does not satisfy the full projection contract. Disposition belongs to acceptance.

F-01 and F-02 remain historical IDs. Their original triggers are independently
corroborated as corrected here (D-02/D-04); F-03 is a distinct defect introduced
by treating any repeated directory identity as a cycle.

## 3. Completeness ledger

The ledger was reconstructed from the brief, verification revision 1 and prior
continuation before behavioral probes. Prior passes guided selection; producer
claims were not treated as current independent proof. Stable IDs are retained.

| Row | AC / invariant | Explicit cases and setup / oracle | Submitted evidence | Independent probe / current evidence | Result / reason |
|---|---|---|---|---|---|
| V-01 | AC-01/02/05; R-01/02 | Real installed unborn/committed targets; public check must return exit 0, true match, empty differences and full count | Fresh-install tests and corrected linked-source test | D-01 ordinary variants pass; D-02 single link matches with 87 paths; D-03 exact installations with acyclic aliases fail | fail — F-03 |
| V-02 | AC-01/02/03; R-01/02 | Changed/missing SKILL.md, references, eval/setup, guide, helper/config/schema; all selected packages/shared files; missing package; owned extra; fingerprint-excluded mutation; exact path/category oracle | Family, missing-package, fingerprint, linked-source and denial tests | D-01 family/fingerprint cases pass; D-05 exact changed/missing for all 20 packages and six shared files; D-02 copied-subtree deletion is exact missing drift; D-03 aliases prevent projection comparison | fail — F-03; other exercised cases pass |
| V-03 | AC-02/03; R-01/02 | Unselected skill/helper, other .agents content, outside-block text and four transient patterns ignored; owned non-transient extra contrasted | Unmanaged/transient test | D-01 real public CLI contrast passes; static pruning matches copy ignore patterns | pass — ownership/exclusion contrast holds |
| V-04 | AC-01/02/03; R-01/02 | Changed/absent block; absent AGENTS; unmatched, duplicate and reversed markers; exact drift or precise failure | Marker test | D-01 real public CLI cases; extraction and main error mapping traced | pass — absent/changed drift and malformed exit 2 |
| V-05 | AC-01/03; R-02 | Missing/non-Git/non-root target; missing source; denied file/source/target directory; dangling entry; symlink/wrong type at roots, selected destination, shared file, guide and AGENTS | Failure/denial/cycle tests | D-01, no skips; D-04 repeats F-01 expected/unexpected denied trees and relocated missing-source CLI; D-05 all 14 refusals with target/outside snapshots; actual ancestor cycle test exits 2 | pass — required invalid-input cases behave precisely; false rejection of valid aliases is recorded under V-01/02/07 |
| V-06 | AC-04; R-03 | Match/drift/failure/absent in unborn/committed repos twice each; source/target path/type/byte and Git/evidence snapshots; no .agents creation | Snapshot test and claimed prior Appendix B probes | D-01; D-05 independently runs all eight combinations twice with equal output and unchanged snapshots; D-04 missing-source snapshots; D-03 repeated alias failures leave source/target unchanged; static check path has no install/stage/availability/run-start calls | pass — current point-in-time read-only evidence |
| V-07 | AC-05 | Positional install/check from unrelated CWD, unmanaged preservation, location-based source and coherent documented scope/results/refresh | Unrelated-CWD and guidance test | D-01 ordinary invocation passes; both staged guides and CLI traced; D-02/03 relocated source resolves correctly, but documented equivalence to copying fails for aliases | fail — F-03; ordinary CLI compatibility and ownership pass |
| R-01 | AC-02/03; INV-009 | Complete canonical managed projection | Producer maps V-01–04 | V-01–04 above | fail — F-03 refuses valid copied projection |
| R-02 | AC-01/03; INV-009 | Truthful outcomes, ownership and precise failures | Producer maps V-01–05 | V-01–05 above | fail — F-03 misclassifies valid source aliases |
| R-03 | AC-04; INV-009 | All result classes, both Git states and repeated checks | Producer maps V-06 | V-06 above | pass |

No required behavioral row is blocked or unchecked. Managed JSON schemas are
compared as bytes; no executable validator contract was changed by this task.
No process-lifecycle invariant, whole-repository or live/model check is required.

## 4. Adversarial checks

Independent safe probes continued after F-03. D-03 crosses single/multiple
source paths with copied target paths, observes actual install success, repeats
check, then changes legitimate fixture state to prove the single-alias contrast.
D-04 covers both expected and unexpected denied subtrees. D-05 covers selected
versus unmanaged ownership and all repository/result repetition combinations.

## 5. Command record

All behavioral commands ran locally from the repository root with
`PYTHONDONTWRITEBYTECODE=1`, Python 3.14.6, non-root uid 501. No network,
privileged action, dependency installation, active refresh or production/test
edits occurred. Installs were fixture setup only. Temporary trees were cleaned,
denied permissions restored, and subprocesses returned. No fixture servers or
background processes were created.

| ID | Exact command / body | Current result |
|---|---|---|
| D-01 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py -k check_` | exit 0; 15 tests OK, 8.406s, no skips |
| D-02 | `PYTHONDONTWRITEBYTECODE=1 python3 -` with Appendix B replay selector for discovery-02 Appendix A | fresh linked-source install/check exits 0, 87 paths, true match; deleted copied subtree exits 1 with sole exact missing path; fixtures cleaned |
| D-03 | `PYTHONDONTWRITEBYTECODE=1 python3 -` with Appendix A below | both acyclic alias layouts install successfully but check exits 2 with `directory cycle`; single-alias contrast exit 0; repeated failure agrees and snapshots unchanged; fixtures cleaned |
| D-04 | `PYTHONDONTWRITEBYTECODE=1 python3 -` with Appendix B replay selector for discovery-02 Appendix C | both F-01 regressions exit 2 twice with scoped denial diagnostics; missing relocated source exits 2 with source/target unchanged; fixtures cleaned |
| D-05 | `PYTHONDONTWRITEBYTECODE=1 python3 -` with Appendix B replay selector for discovery-01 Appendix B | exit 0; 52 exact changed/missing mutations, 14 refusals, eight repeated source/target/Git/evidence snapshot combinations; fixtures cleaned |
| D-06 | `git diff --cached --check` | exit 0; formatting only, not behavioral evidence |
| D-07 | `git rev-parse HEAD`; `git diff --cached --binary`; `git diff --cached --name-only`; `git show :<path>` and `git rev-parse :<path>` for each staged path; independent worktree reads and SHA-256; `git diff --name-only`; preparation SHA-256; `git status --short --untracked-files=all` | eight index/worktree comparisons equal; no unstaged diff; identities below |

Appendix replay commands use exact prior probe bodies against current bytes,
not prior results. D-02's printed output is evaluated against the corrected
oracle; the historical probe's exit 0 alone is not proof.

## 6. Aggregate gate

| Field | Value |
|---|---|
| Existing command | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py` |
| Status | not run |
| Owner / stage | this independent reviewer, correction discovery |
| Reason | D-03 / F-03 is a decisive targeted failure; aggregate suppressed, independent safe sibling probes completed |
| Current evidence | D-01/02/04/05 pass their exercised cases; D-03 fails canonical projection compatibility; producer's 32-test gate claim is not this discovery's gate |

No gate or command was added. A future correction discovery owns the existing
aggregate after clean targeted evidence. This record waives no conditional duty.

## 7. Scope and byte identity

The four code/test/guide paths are brief-authorized. The results and three
existing staged review artifacts are task submission/history context; no
unexplained overlap or unrelated changes were observed. No plans, preparation,
earlier reports, active installation or index were changed by this session.

| Staged path | Index blob (index and worktree bytes independently confirmed equal) |
|---|---|
| README.md | `ba77360f5293be17f9c9eb9e969c2d484be92721` |
| docs/tasks/T-004.2/results.md | `e0baceac99322ca2d0b1d6b7468dd164ccb13609` |
| docs/tasks/T-004.2/reviews/discovery-01.md | `caa680abed8e73abcb183f3f2396f706da27edba` |
| docs/tasks/T-004.2/reviews/discovery-02.md | `50264cc9194fcadc74019cf3774fb1374f4ff040` |
| docs/tasks/T-004.2/reviews/maintainability-01.md | `e1ec29948a4ee47bedd5d9afa7a01a8d1ed86530` |
| scripts/install_development_skills.py | `ecd35fb317ec50ea0321eeff25255a2433d8998d` |
| skills/README.md | `e858165836ec4e70a0432e9c4d0f20be6cabca4e` |
| tests/test_install_development_skills.py | `f0ce049359de7ae81d824f0fbbd01896678e6388` |

Preparation hashes match the submission:

- brief: `ecf57bb5cb33dda3405269c3f6adf05628248d2a4510fe34358d98d8e027512e`.
- verification revision 1: `4966f69350e20d8563532d172e26acb6a8536e0c64635a62be0fb11f393c24b8`.
- preflight: `8f8af39476e7d6d7960b9f3f0e14efe766383dee54d64db784445ee882c40d1b`.

Preflight's dependency HEAD `93cd0e4` precedes current preparation HEAD
`f6046d8`; this is already attributed in submission/prior discovery. Its
operating context remains local read-only profile comparison for T-004.3 and
T-005, with no retained versions or active refresh. No new product decision is
needed to establish the copying mismatch.

Exact status immediately before the report write:

```text
M  README.md
A  docs/tasks/T-004.2/results.md
A  docs/tasks/T-004.2/reviews/discovery-01.md
A  docs/tasks/T-004.2/reviews/discovery-02.md
A  docs/tasks/T-004.2/reviews/maintainability-01.md
M  scripts/install_development_skills.py
M  skills/README.md
M  tests/test_install_development_skills.py
```

Post-write status (verified after creation):

```text
M  README.md
A  docs/tasks/T-004.2/results.md
A  docs/tasks/T-004.2/reviews/discovery-01.md
A  docs/tasks/T-004.2/reviews/discovery-02.md
A  docs/tasks/T-004.2/reviews/maintainability-01.md
M  scripts/install_development_skills.py
M  skills/README.md
M  tests/test_install_development_skills.py
?? docs/tasks/T-004.2/reviews/discovery-03.md
```

Only this new report entry differs. The staged diff and reviewed worktree
bytes are unchanged; the report remains unstaged.

## 8. Questions, conditional evidence and residual risks

| Type | Evidence / limitation | Owner / follow-up |
|---|---|---|
| Conditional evidence gap | `maintainability-01.md` reviewed installer blob `a925d043…` and tests `e3092e09…`, not current `ecd35fb…` / `f0ce049…`. The F-02 submission itself requires a fresh maintainability stage. None is present for this correction. This discovery did not perform or waive it. | Coordinator routes current/corrected scope to fresh `task-maintainability-review`; acceptance retains this missing proof separately from F-03. |
| Residual limit | Snapshot equality cannot exclude a write that completely restores itself; check-path static tracing and absent/drift repeated canaries supplement snapshots. | Acceptance consumes this bounded local evidence; no cross-platform or agent-call qualification claim. |
| Historical dependency context | T-004.1 has no separate acceptance report in the supplied package, as recorded by preflight; brief declares dependency completed/reviewed. | Authority owner retains that plan-state responsibility; no invented review. |

No behavioral ledger row is unchecked or blocked. The conditional evidence gap
is separate from the completeness of this discovery's behavioral ledger.

## 9. Next route and continuation

Next: separate acceptance decision call consumes the task brief, current staged
diff, this report, prior finding history, submission, verification revision 1,
ready preflight and its cited decision context. It must retain F-03 and the
missing current maintainability proof as separate obligations. This report
does not decide correction, deferral or advancement.

```markdown
Discovery continuation:
- Iteration / current byte identity: correction discovery 2; HEAD f6046d8b1a48f1984ad025589dca4a01c2fa87c9; staged binary diff SHA-256 5786a6780f6fbf7ce4163f8066e5158ce96486812aced5e616bf351f626da57f; eight staged index/worktree identities equal.
- Coverage rows: V-01 fail F-03; V-02 fail F-03; V-03 pass; V-04 pass; V-05 pass; V-06 pass; V-07 fail F-03; R-01 fail F-03; R-02 fail F-03; R-03 pass. No blocked/unchecked behavioral rows.
- Finding IDs: F-01 historical corrected (D-01/04); F-02 historical corrected for original trigger (D-01/02); F-03 current suggested P2, acyclic aliases falsely rejected as cycles (D-03).
- Finding/scenario continuity: prior V-01/02/R-01/R-02 failed F-02, producer claims all corrected/pass; current D-02 confirms that trigger, while D-03 establishes new alias failure in V-01/02/07/R-01/R-02. Prior V-03/04/05/06/R-03 passes currently corroborated; prior V-07 pass now fails documented projection equivalence. Influenced siblings: linked references/evals/setup in every package, multiple links and real-subtree-plus-alias. Correction owner: implementer if routed by acceptance/coordinator; evidence owner: fresh discovery after correction; authority owner: coordinator, unchanged brief. Separate incomplete conditional proof: current maintainability review absent, owner fresh task-maintainability-review via coordinator.
- Preparation/context: docs/tasks/T-004.2/brief.md; verification.md revision 1; preflight.md ready; results.md; parent T-004 brief; project-plan ART-009/010/011, IF-007, INV-009 and FLOW-004; task-map T-004 context.
- Reviewer regressions: this report Appendix A (D-03), discovery-02 Appendix A (D-02), discovery-02 Appendix C (D-04), discovery-01 Appendix B (D-05); exact python-stdin replay commands below; existing targeted check_ selector D-01.
- Aggregate gate: not run by current correction discovery after decisive D-03 failure; existing command PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py; future correction discovery owns it after clean targeted evidence; conditional maintainability duty retained.
- Next: separate task-acceptance-review call on staged scope with this evidence and the conditional gap; no acceptance verdict issued here.
```

## Appendix A — D-03 exact independent probe

Run `PYTHONDONTWRITEBYTECODE=1 python3 -` from the repository root with this
body. Its printed failure observations are findings; script exit 0 alone does
not mean the behavioral contract passes.

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
    outside=base/'outside'; outside.mkdir(); (outside/'copied.txt').write_text('shared source bytes\n')
    package=source/'skills/project-direction'
    for name in ('linked-a','linked-b'): (package/name).symlink_to(outside,target_is_directory=True)
    repo=base/'target'; repo.mkdir(); t.init_repo(repo)
    cli=source/'scripts/install_development_skills.py'
    def call(*args): return subprocess.run([sys.executable,str(cli),*map(str,args)],capture_output=True,text=True,timeout=30)
    r=call(repo); assert r.returncode==0,r.stderr
    for name in ('linked-a','linked-b'):
        p=repo/'.agents/skills/project-direction'/name/'copied.txt'
        assert p.read_text()=='shared source bytes\n' and not p.is_symlink()
    before=t.snapshot_tree(repo); source_before=t.snapshot_tree(source)
    a=call('--check',repo); b=call('--check',repo)
    print('fresh-install-two-acyclic-aliases',a.returncode,a.stdout.strip(),a.stderr.strip())
    assert (a.returncode,a.stdout,a.stderr)==(b.returncode,b.stdout,b.stderr)
    assert before==t.snapshot_tree(repo) and source_before==t.snapshot_tree(source)
    (package/'linked-b').unlink()
    shutil.rmtree(repo/'.agents/skills/project-direction/linked-b')
    r=call('--check',repo); assert r.returncode==0,r.stderr
    print('single-alias-contrast',r.returncode,json.loads(r.stdout)['match'])
    (package/'references-alias').symlink_to(package/'references',target_is_directory=True)
    r=call(repo); assert r.returncode==0,r.stderr
    r=call('--check',repo)
    print('fresh-install-real-directory-and-alias',r.returncode,r.stdout.strip(),r.stderr.strip())
print('all disposable fixtures cleaned')
```

## Appendix B — Exact replay command bodies

Each body is passed separately to `PYTHONDONTWRITEBYTECODE=1 python3 -`.

D-02:

```python
from pathlib import Path
text=Path('docs/tasks/T-004.2/reviews/discovery-02.md').read_text()
body=text.split('## Appendix A')[1].split('```python\n')[1].split('```')[0]
exec(compile(body,'discovery-02-appendix-A','exec'))
```

D-04:

```python
from pathlib import Path
text=Path('docs/tasks/T-004.2/reviews/discovery-02.md').read_text()
body=text.split('## Appendix C')[1].split('```python\n')[1].split('```')[0]
exec(compile(body,'discovery-02-appendix-C','exec'))
```

D-05:

```python
from pathlib import Path
text=Path('docs/tasks/T-004.2/reviews/discovery-01.md').read_text()
body=text.split('## Appendix B')[1].split('```python\n')[1].split('```')[0]
exec(compile(body,'discovery-01-appendix-B','exec'))
```
