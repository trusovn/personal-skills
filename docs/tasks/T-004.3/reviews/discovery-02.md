# Task Review Discovery Report: T-004.3 — Prove explicit refresh and distribution closure

| Field | Value |
|---|---|
| Producing stage | project-local `task-review-discovery` |
| Coverage completeness | complete — all V-01–V-06 and R-01/R-02 rows have current dispositions; one confirmed finding remains |
| Discovery iteration | correction discovery, iteration 2 |
| Created at | 2026-10-13, Europe/Lisbon |
| Repository root | `/Users/mtrusov/work/skill-sources/personal-skills` |
| Durable report path | `docs/tasks/T-004.3/reviews/discovery-02.md` |
| Task brief | `docs/tasks/T-004.3/brief.md` |
| Verification / context | `docs/tasks/T-004.3/verification.md`, revision 1; ready `preflight.md`, including Decision context |
| Current submission | staged corrected `results.md`, producer state `READY_FOR_REVIEW` |

This report publishes evidence only. It gives no acceptance verdict, approved
deferral, or advancement. It applies only to the identified reviewed bytes.
It does not review or authenticate itself. A separate acceptance decision call
consumes the report.

## 1. Discovery provenance

This session authored none of the reviewed production, test, or submission
bytes. It independently reviewed the staged changes; it wrote only this report.
Active skills are the project-local `task-review-discovery` and
`testing-discipline`. No subagents were launched.

HEAD: `854642406b93f68ef413526db0945bc18c1aff8b`.
SHA-256 of `git diff --cached --binary`:
`cab836e27cc9c6ecc96fe5ee67bb049d012e026317e4213df67e9e399bfc7a72`.

Index and worktree bytes were compared separately for every staged path and
all three preparation artifacts. All match; the tracked unstaged diff is empty.
The report applies to that staged identity, including the corrected installer
and test. Prior evidence remains navigation context, not proof for these bytes.

## 2. Findings

### F-01 [suggested P2] Install and refresh still change unmanaged AGENTS line-ending bytes

| Field | Evidence |
|---|---|
| Finding continuity | discovery-01 F-01 remains open for a contract-implied sibling; its original LF boundary-whitespace trigger is corrected |
| Current location | `scripts/install_development_skills.py:299`; corrected renderer at line 164; test oracles at `tests/test_install_development_skills.py:1053`, 1066 and 1206 |
| Trigger | Valid UTF-8 AGENTS instructions with CRLF line endings, during first insertion or refresh of a valid block, in either unborn or committed Git state |
| Consequence | The installer changes bytes outside the managed block. Both pre-refresh and post-refresh checks report match, since unmanaged instructions are outside the check's ownership. A maintainer cannot rely on the claimed byte-preserving refresh. |
| Evidence | D-03: first insertion reports `insertion_preserved=false`; refresh reports `outside_preserved=false` in both states. Prefix `b'# Instructions\r\n\t \r\n\r\n'` becomes `b'# Instructions\n\t \n\n'`; suffix `b'\r\n\tSuffix.  \r\n\r\n'` becomes `b'\n\tSuffix.  \n\n'`. All installer calls exit 0; both checks report match. Python's default text read normalizes newline sequences before the corrected renderer sees them. |
| Affected AC / invariant | AC-03 and AC-05; V-03, V-06; R-02 / INV-009: exact preservation of unmanaged bytes during insertion and refresh |
| Credible sibling surface | Mixed LF/CRLF or lone-CR instructions in the unmanaged prefix or suffix use the same input path; first insertion and existing-block refresh share it. The new tests read both expected and actual segments through newline-normalizing text reads. |
| Smallest corrective direction | Preserve original newline bytes across the complete AGENTS read/render/write boundary; verify first insertion and replacement with raw-byte oracles covering the affected line-ending family. Reconcile submission claims with the resulting evidence. |

The CRLF case is within the existing exact-byte preservation requirement;
it does not introduce a new refusal policy or broaden managed ownership.

Prior F-02 is corrected in the current submission: `results.md` now limits
fingerprint equality to workflow identity and attributes full projection
equality to managed path/byte comparison plus the check. D-01 reruns the
fingerprint counterexample successfully. This is current evidence of the
correction, not an acceptance disposition.

## 3. Completeness ledger

The selected ledger retains discovery-01's V-01–V-06 and R-01/R-02 IDs.
Required cases came from verification revision 1 and the finite-risk contract.
The producer's scenario map reports OK; these are submitted claims. Current
independent evidence follows.

| Row | AC / invariant | Material cases; setup / oracle | Submitted evidence | Independent probe / current result |
|---|---|---|---|---|
| V-01 | AC-01 / R-01 | Real unborn/committed targets: install, fresh match, drift, read-only drift check, explicit refresh, match, repeated match; Git identity and target snapshots | T, RR-01, P; producer OK | **pass** — D-01 executes the consolidated journey; D-02 executes prior DISC-02 on current bytes, comparing full target snapshots including Git around fresh/drift/restored/repeated checks. Unborn commit remains null; restored JSON repeats exactly. D-05 retains detached install/check compatibility. |
| V-02 | AC-02 / R-01 | Changed skill/guide/helper/config/schema/valid block; missing reference/eval/setup; owned extra; complete expected managed path/byte projection | T covers all families except deliberate setup drift, with complete projection comparison | **pass** — D-01 covers the changed/missing families; D-02 deletes a reference, adds an extra, then explicitly refreshes, checks removal/restoration and all expected source bytes. Prior DISC-04 in D-02 independently deletes/restores setup bytes through canonical calls. |
| V-03 | AC-03 / R-02 | First insertion, existing-block refresh, boundary whitespace, exact unmanaged segments/helper/skill/reference/project file and singular markers | Corrected T, RR-01 and P claim byte preservation | **fail** — D-01 and D-02 pass LF whitespace and unmanaged-file cases, but D-03 demonstrates CRLF byte loss on insertion and refresh in both Git states: F-01. |
| V-04 | AC-03 / R-02 | Malformed/unmatched/duplicate/reversed markers; unsafe targets; refusal and unchanged protected state | Existing retained cases green in I | **pass** — D-04 reruns current marker/refusal/unreadable-content tests. D-02 executes prior DISC-04 after real installation: unmatched/duplicate/reversed markers make both install and check exit 2 with full-target snapshot equality. |
| V-05 | AC-04 | Canonical selection, guide, six shared files, three READMEs; positional install/check 0/1/2; explicit rerun; limited fingerprint scope | No selection or README change; reconciliation recorded | **pass** — static reconciliation of source constants, independent test expectations and README guidance; D-04 selection/guide/public-interface tests pass; D-01 fingerprint contrast, D-04 unborn identity and D-05 detached identity confirm consumed framing remains applicable. No active-run or model behavior claimed by guidance. |
| V-06 | AC-05 | Runnable setups/commands/output, installed identity and complete projection evidence, accurate preservation claims, T-005 gaps | Corrected results include full probe body and limited fingerprint argument; all producer rows OK | **fail** — fingerprint correction is supported by D-01; D-02 corroborates recorded fingerprint, null unborn identity and real committed identity, projection restoration and LF preservation. However, the results claim exact first-insertion/outside-block preservation and strictly byte-preserving rendering beyond what current bytes support: D-03/F-01. Skill-call/model/coordinator boundaries remain explicitly unrun. |
| R-01 | INV-009 | Both Git states; independent reference deletion and owned extra; drift survives check, explicit refresh restores source bytes, repeated check | V-01/V-02 | **pass** — D-02 prior DISC-02 and DISC-04 on current bytes |
| R-02 | INV-009 | Selected drift crossed with unmanaged helper/outside whitespace; first insertion and replacement; refusal retention | V-03/V-04 | **fail** — LF whitespace/helper/refusal cases pass; CRLF raw-byte preservation fails in D-03/F-01 |

There are no blocked or unchecked required behavioral rows. Complete coverage
means every required row has a disposition; it does not mean every row passes.
No semantic schema-validator change is claimed: schema restoration is a byte
copying case. No collector process-lifecycle qualification is in scope.

## 4. Adversarial state and evidence checks

Selected managed reference/setup deletion and owned extras were crossed with
unmanaged helper and outside-block whitespace through real refreshes. All
required restoration and helper survival cases pass. Ordered second matching
checks run after legitimate restoration; full-target snapshots remain unchanged.
Malformed marker cardinality/order is refused after a real first install.

The remaining failure sits at the text/file boundary: a pure string-splicing
check cannot prove byte preservation. The real CRLF probe observes raw bytes
before and after both public install occurrences. Both green check results
demonstrate why managed comparison cannot serve as an unmanaged preservation
oracle. The existing fingerprint contrast independently confirms its narrower
coverage.

## 5. Independent probes and commands

All commands ran from the repository root, locally, with
`PYTHONDONTWRITEBYTECODE=1`; unittest/probe imports use `PYTHONPATH=tests`.
No live/network/model/privileged checks ran. Each probe uses synchronous child
processes and context-managed disposable targets, removed on completion.
No server, background process or fixture process was left running.

### D-01 — corrected journey and fingerprint regression

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_install_development_skills.DevelopmentProfileCheckTests.test_journey_detects_drift_read_only_then_explicit_refresh_restores_every_family test_install_development_skills.DevelopmentProfileCheckTests.test_check_detects_managed_drift_that_the_workflow_fingerprint_excludes
```

Exit 0; 2 tests, 2.084 seconds, no skips. Both journey Git-state subtests pass.
The fingerprint test changes copied eval bytes, retaining fingerprint identity
while check detects drift.

### D-02 — rerun prior public-boundary probes on current bytes

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 - <<'PY'
from pathlib import Path
import re
report = Path('docs/tasks/T-004.3/reviews/discovery-01.md').read_text()
for section in ('DISC-02', 'DISC-04'):
    body = re.search(r'### '+section+r'.*?```python\n(.*?)```', report, re.S).group(1)
    print('Running prior regression', section)
    exec(compile(body, section, 'exec'))
PY
```

Exit 0; 2.760 seconds tool wall time. This executes the exact durable prior
DISC-02 and DISC-04 bodies from discovery-01 section 5, without modifying that
report. DISC-02 reports `insertion_retains_original_bytes=true` and
`outside_preserved=true` for its LF fixtures in both states; restoration,
owned-extra removal, complete expected managed-byte comparison and read-only
snapshots pass. Fingerprint:
`sha256:a11a7689242a3ecf690971bcf7e85f3e745cebb7ea0168c40dbde08efa717da3`.
The committed fixture's actual commit was
`2f3c9fb35aadb258c58954027aac249624c7b030`; unborn commit is null.
DISC-04 restores missing setup content byte-identically and refuses each
post-install malformed marker case without mutation. Prior DISC-02 is a
diagnostic that prints preservation results; those printed values, rather
than its exit status alone, supply the preservation oracle.

### D-03 — raw CRLF byte preservation

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 - <<'PY'
import json, tempfile
from pathlib import Path
import test_install_development_skills as t

def outside(data):
    begin = data.index(t.installer.AGENTS_BEGIN.encode())
    end = data.index(t.installer.AGENTS_END.encode()) + len(t.installer.AGENTS_END.encode())
    return data[:begin], data[end:]

for committed in (False, True):
    with tempfile.TemporaryDirectory(prefix='t0043-crlf-') as tmp:
        repo = Path(tmp)
        t.init_repo(repo, commit=committed)
        agents = repo / 'AGENTS.md'
        original = b'# Instructions\r\nKeep trailing spaces.  \r\n\r\n'
        agents.write_bytes(original)
        first = t.run_installer(repo)
        assert first.returncode == 0, first.stderr
        insertion_preserved = agents.read_bytes().startswith(original)
        prefix = b'# Instructions\r\n\t \r\n\r\n'
        suffix = b'\r\n\tSuffix.  \r\n\r\n'
        agents.write_bytes(prefix + t.installer.AGENTS_BLOCK.rstrip().encode() + suffix)
        before = t.snapshot_tree(repo)
        check_before = t.run_check(repo)
        assert check_before.returncode == 0, check_before.stderr
        assert before == t.snapshot_tree(repo)
        refreshed = t.run_installer(repo)
        assert refreshed.returncode == 0, refreshed.stderr
        actual = outside(agents.read_bytes())
        check_after = t.run_check(repo)
        assert check_after.returncode == 0, check_after.stderr
        print(json.dumps({'committed': committed, 'insertion_preserved': insertion_preserved,
            'outside_preserved': actual == (prefix, suffix),
            'before': [repr(prefix), repr(suffix)], 'after': [repr(x) for x in actual],
            'checks_match': [json.loads(check_before.stdout)['match'], json.loads(check_after.stdout)['match']]}))
PY
```

Exit 0; 1.231 seconds tool wall time. This diagnostic deliberately prints the
preservation outcomes rather than asserting a pass. Both states report:
`insertion_preserved=false`, `outside_preserved=false`,
`checks_match=[true,true]`. Exact before/after bytes are recorded in F-01.
The pre-refresh check leaves the full target snapshot unchanged.

### D-04 — retained narrow contract cases

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 - <<'PY'
from pathlib import Path
import re, subprocess, shlex
report = Path('docs/tasks/T-004.3/reviews/discovery-01.md').read_text()
command = re.search(r'### DISC-03.*?```sh\n(.*?)```', report, re.S).group(1).strip()
args = shlex.split(command)
subprocess.run(args[2:], check=True)
PY
```

Exit 0; 9 tests, 4.401 seconds, no skips. Exact selector command is stored
unchanged in discovery-01's DISC-03 block, which this command executes.
Covers marker refusal, unsafe/unreadable target content, repeated read-only
checks, public install/check guidance, canonical selection, complete guide
and unborn installation/identity. It is targeted row evidence, not the aggregate.

### D-05 — current detached compatibility

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 - <<'PY'
import tempfile, json
from pathlib import Path
import test_install_development_skills as t
with tempfile.TemporaryDirectory(prefix='t0043-detached-') as tmp:
    repo = Path(tmp)
    t.init_repo(repo)
    t.git(repo, 'checkout', '--detach')
    head = t.git(repo, 'rev-parse', 'HEAD').strip()
    result = t.run_installer(repo)
    assert result.returncode == 0, result.stderr
    assert t.git(repo, 'rev-parse', 'HEAD').strip() == head
    identity = t.installed_identity(repo)
    assert identity['repository_commit'] == head
    assert t.run_check(repo).returncode == 0
    print(json.dumps(identity, sort_keys=True))
PY
```

Exit 0; 0.345 seconds tool wall time. Detached commit
`bb3956f88aa22e9a52858f6709a4fc6391ff0a99` is unchanged; installed identity
has null branch, that real commit, the recorded workflow fingerprint and
`workflow_dirty=false`. Check matches.

### Static/scope evidence

Read the active skill and report template, package brief/verification/preflight,
submission, prior discovery/maintainability reports, scoped installer/test diff,
relevant installer read/render/write paths and current tests, and the root,
profile and flow README guidance. Canonical scope commands:
`git diff --cached -- scripts/install_development_skills.py tests/test_install_development_skills.py`,
`git diff --cached --numstat`, `git diff --stat`, `git rev-parse HEAD`,
`git ls-files -s docs/tasks/T-004.3 scripts/install_development_skills.py tests/test_install_development_skills.py`,
`git status --short --untracked-files=all`, and `git diff --quiet`.
Identity comparison independently hashes `git show :<path>` and
`Path(path).read_bytes()`; exact results are in section 7.

## 6. Aggregate-gate record

| Field | Value |
|---|---|
| Gate / exact authorized command | `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_install_development_skills test_workflow_version test_run_evidence` |
| Status | not run |
| Owner / stage | this independent correction discovery |
| Reason | D-03 decisively fails required AC-03 preservation; aggregate suppressed under the active discovery skill |
| Current evidence | Targeted rows are fully reconciled; V-03/V-06/R-02 fail. Passing sibling probes do not erase F-01. |

No new gate or command was added. The producer's installer-suite pass and
historic aggregate records are not current independently owned aggregate
evidence. A future correction discovery reruns regressions, reconciles all
rows, then owns one justified aggregate only after clean targeted evidence.

## 7. Scope and baseline comparison

Prior discovery reviewed HEAD `854642406b93f68ef413526db0945bc18c1aff8b`
with staged diff SHA-256
`e2f26b5d3b7bdac627fb1f1ee304e177a6fe67d0198fab75d665c68145766fef`.
HEAD remains the same. The new scope is the expressly permitted bounded
installer preservation repair, strengthened journey test and corrected results.
Prior reports are pre-existing staged evidence, not current production changes
or this session's work. No unexplained scope overlap was found.

| Path | Index blob | Index SHA-256 | Worktree comparison |
|---|---|---|---|
| `docs/tasks/T-004.3/results.md` | `af61ac08ebe4152ae2159796d1a8c064b4486d17` | `5189b2dc3a1ed2de8ca9b7fd673c3836b303af04f30b5cce9ed195990201a16e` | same SHA-256; bytes equal |
| `docs/tasks/T-004.3/reviews/discovery-01.md` | `ceafd28ba97536d6168aec12ca9fc588f76f250d` | `e22bdf908a5a27d772c302807f04acf72f5786b8bd40a8c5ba12eee27064fb96` | same SHA-256; bytes equal |
| `docs/tasks/T-004.3/reviews/maintainability-01.md` | `a08f9965cee74d43d8d4ee8c0c5d9d568c5c6680` | `cce4ecc9dd1bd829b868cd32da9ca1e29a5556da639bb4c3af511a5f44e1a567` | same SHA-256; bytes equal |
| `scripts/install_development_skills.py` | `11bc2da040f659fa38421e90e5b1527af3f54005` | `8f59cf6a61aa76d25203872ac2666d68380b10be7421c17f51ca917c39548481` | same SHA-256; bytes equal |
| `tests/test_install_development_skills.py` | `421a3ae666cfb899ff46b6a8968ae61f3fe91079` | `d211ef5df99f549797c33b5a2fd2cfa9b4eb25cb53541c6c73c91e330693924c` | same SHA-256; bytes equal |
| `docs/tasks/T-004.3/brief.md` | `758a4aa7a4288e7b8e758442ae6c422a785099b9` | `bdf0c28a9184c72438b69466046a7eece5971b34b30adf33e28f244adcdc4098` | same SHA-256; bytes equal |
| `docs/tasks/T-004.3/verification.md` | `a5bddb43cefaffe6991246181afe8795571dd717` | `50bd1ef5fbd1e196ecfa130eea54d2a86daca0366e52a4b91654b51a7f1617d4` | same SHA-256; bytes equal |
| `docs/tasks/T-004.3/preflight.md` | `28f8dd107866e450e11c7386ff30dd1cad55cf4b` | `9f643161c31eb7ff1b90328e8f911b04ed79f82f3e80cafe5fabbe91bc1ea971` | same SHA-256; bytes equal |

Brief and verification digests still match ready preflight. The preflight's
older HEAD is explained by the docs-only preparation commit as recorded in the
submission; no authority change was found.

Exact reviewed status immediately before the report write:

```text
A  docs/tasks/T-004.3/results.md
A  docs/tasks/T-004.3/reviews/discovery-01.md
A  docs/tasks/T-004.3/reviews/maintainability-01.md
M  scripts/install_development_skills.py
M  tests/test_install_development_skills.py
```

Exact post-report status:

```text
A  docs/tasks/T-004.3/results.md
A  docs/tasks/T-004.3/reviews/discovery-01.md
A  docs/tasks/T-004.3/reviews/maintainability-01.md
M  scripts/install_development_skills.py
M  tests/test_install_development_skills.py
?? docs/tasks/T-004.3/reviews/discovery-02.md
```

Only the new discovery-02 entry differs. Index entries, implementation bytes,
submission, plans, active installation and prior reports were not changed.
The post-write status and unchanged staged diff were independently checked.

## 8. Questions, residual risks and conditional evidence

| Item | Evidence / owner |
|---|---|
| Current maintainability evidence | `maintainability-01.md` describes production implementation as unchanged. The correction adds production changes; `results.md` explicitly requires a fresh maintainability review before discovery/acceptance, but no corrected-scope report is present. This is an outstanding conditional-stage evidence duty, not a fabricated behavioral finding. Coordinator / maintainability stage must resolve current applicability before advancement; this discovery waives no duty. |
| Historical producer outputs | Current probes corroborate selected claims; this report does not authenticate historic manual output, evidence-run records or prior reports. |
| T-005 and upstream disposition | Installed skill/role-call/model qualification remains unrun. Preflight/submission note absent durable .1/.2 acceptance reports. Coordinator owns disposition and qualification; filesystem proof does not replace them. |
| Active installation | Never refreshed or mutated. Source presence is not installed-skill qualification. |

No unproved behavioral question is promoted to a finding. No required row is
omitted or reported clean based solely on a submitted command.

## 9. Coverage and next route

Coverage is complete with one confirmed remaining preservation finding.
Send this report to a separate `task-acceptance-review` call together with the
brief, current scoped staged diff, corrected submission, verification revision 1,
ready preflight/Decision context, prior discovery and conditional maintainability
evidence. That call decides disposition; discovery makes no decision and performs
no correction. The missing corrected-scope maintainability evidence remains
explicitly owned and must not be treated as completed.

## 10. Discovery continuation

```markdown
Discovery continuation:
- Iteration / identity: correction discovery 2; HEAD 854642406b93f68ef413526db0945bc18c1aff8b; staged diff SHA-256 cab836e27cc9c6ecc96fe5ee67bb049d012e026317e4213df67e9e399bfc7a72; all reviewed index/worktree bytes equal.
- Coverage rows: V-01 pass; V-02 pass; V-03 fail (CRLF unmanaged bytes); V-04 pass; V-05 pass; V-06 fail (unsupported general byte-preservation claims); R-01 pass; R-02 fail (F-01). No blocked/unchecked required behavioral rows.
- Finding IDs: F-01 suggested P2 remains open for newline normalization; prior LF whitespace trigger corrected. F-02 corrected in current claims, corroborated by D-01.
- Finding/scenario continuity: prior V-01/V-02/V-04/V-05/R-01 passes re-probed; prior V-03/V-06/R-02 failures remain through CRLF sibling. Producer T/RR-01/RR-02/I/P claims are attributed to results.md; D-01–D-05 are current independent evidence. Correction owner: .3 implementer; evidence owner: fresh discovery after correction; authority/disposition owner: separate acceptance call. First insertion, existing-block refresh and mixed/lone-CR unmanaged segments share F-01's boundary.
- Preparation/context: docs/tasks/T-004.3/brief.md; verification.md revision 1 (SHA-256 50bd1ef5fbd1e196ecfa130eea54d2a86daca0366e52a4b91654b51a7f1617d4); ready preflight.md and its Decision context; results.md; prior discovery-01.md and maintainability-01.md. Corrected-scope maintainability evidence still missing; owner: maintainability stage/coordinator.
- Reviewer regressions: D-01 exact two-selector command; D-02 extraction/rerun of discovery-01 DISC-02/DISC-04; D-03 full CRLF probe in this report; D-04 prior DISC-03 selectors; D-05 detached probe. No test asset written.
- Aggregate: not run, owned by correction discovery; exact union is PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_install_development_skills test_workflow_version test_run_evidence; suppressed after required preservation failure.
- Next: separate task-acceptance-review consumes brief, staged diff, this report, current submission and all preparation/conditional references, preserving the outstanding conditional duty.
```

