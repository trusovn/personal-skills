# Task Review Discovery Report: T-004.3 — Explicit refresh and distribution closure

| Field | Value |
|---|---|
| Producing stage | `task-review-discovery`, project-local installed skill |
| Coverage completeness | Complete behavioral discovery; outstanding conditional maintainability evidence remains separate |
| Discovery iteration | Third discovery, following correction-02 |
| Created at | 2026-10-13T11:21:11Z |
| Repository root | `/Users/mtrusov/work/skill-sources/personal-skills` |
| Durable report | `docs/tasks/T-004.3/reviews/discovery-03.md` |
| Task brief | `docs/tasks/T-004.3/brief.md` |
| Preparation | `verification.md` revision 1; ready `preflight.md`, including Decision context, in this package |
| Submission | Staged `correction-02.md`, with historical `results.md` |

This report publishes evidence only. It contains no acceptance verdict, approved
deferral or advancement. It applies to the identified reviewed bytes, and does
not review or authenticate itself. The separate acceptance call consumes it.

## 1. Discovery provenance

This session authored no reviewed production, test or submission bytes. All
probes below are independently executed against the current staged scope.
Worktree bytes equal index bytes for every staged path and preparation input;
there is no unstaged tracked diff. Thus worktree CLI execution exercises the
reviewed index implementation. No active `.agents/` installation was refreshed.

HEAD: `854642406b93f68ef413526db0945bc18c1aff8b`.
SHA-256 of `git diff --cached --binary`:
`bce72bd22814303da5a1903114c900ae5e3c59aa88ed832453da4026b715f641`.

## 2. Findings

No findings.

Prior F-01 [suggested P2] is no longer reproduced: first insertion and existing
block replacement preserve raw outside bytes, including CRLF, mixed and lone
CR siblings, in unborn and committed targets. P-01 and P-02 corroborate the
read/decode/render/write boundary correction. Prior F-02 remains corrected in
the submission claims: workflow fingerprint equality is only workflow identity
evidence; P-01 independently detects eval drift excluded from that fingerprint.
These are evidence statuses, not acceptance dispositions.

## 3. Completeness ledger

Rows retain the prior discovery identities. Producer commands B/C/J/R/S are
claims from `correction-02.md`; they were not copied as independent proof.

| Row | AC / invariant | Cases and setup / oracle | Submitted evidence | Independent current evidence | Result / reason |
|---|---|---|---|---|---|
| V-01 | AC-01 / R-01 | Real unborn and committed Git targets; install, fresh match, deliberate drift, read-only drift check, separate refresh, restored match, repeated match. Full target snapshots in independent public probe; branch/commit stability in journey. | J/R/S; historical journey | P-01 journey and P-02 D-02: ordered CLI results 0/0/1/0/0/0; checks retain snapshots; no unborn HEAD fabricated; repeated JSON agrees. | pass — current real occurrences corroborated |
| V-02 | AC-02 / R-01 | Changed skill/guide/helper/config/schema/block; missing reference/eval/setup; owned extra. Restore source bytes, block and expected projection; extra absent. | J/R/S | P-01 journey independently compares managed source bytes; P-02 D-02 independently removes reference and adds extra, restores them, checks expected managed bytes; prior DISC-04 deletes/restores setup fixture byte-identically. Matching check confirms exact managed set. | pass — all finite families represented |
| V-03 | AC-03 / R-02 | First insertion retains original bytes; existing block keeps raw prefix/suffix; singular markers. LF, CRLF, mixed LF/CRLF/CR, CR, both Git states; unmanaged skill/reference/helper/project file. | B/C/J/R/S | P-01 eight line-ending/Git subtests plus journey sentinels; P-02 D-02 LF whitespace/helper and D-03 CRLF raw-byte oracle print preservation true. | pass — F-01 no longer reproduced across sibling boundary |
| V-04 | AC-03 / R-02 | Malformed, duplicate, reversed markers and retained unsafe/unreadable target refusal. Install/check failure and unchanged target snapshots. | R/S | P-02 D-02 DISC-04: both calls exit 2 with exact snapshots; D-04 nine retained targeted cases cover unsafe/unreadable paths, repeated read-only checks and first insertion refusals. | pass — refusal policy retained |
| V-05 | AC-04 | Selection/guide/six helpers and three READMEs; positional install, check 0/1/2, separate refresh; unborn/detached identity; limited fingerprint scope. | J/R/S and unchanged guidance reconciliation | Static constants/expectations/guidance reconciliation; P-02 D-04 selection/guide/public CLI/unborn tests, D-05 detached identity; P-01 fingerprint contrast. | pass — distribution interface and framing agree |
| V-06 | AC-05 | Reproducible setups, exact commands, observations and installed identities; full projection versus fingerprint; explicit remaining T-005 gaps. | `correction-02.md` explicitly supersedes general preservation claims in historical results | Submission audit against P-01/P-02 observations; all correction commands identify runnable setup; current identity observations below. Results distinguish local filesystem/Git proof from unrun role/model behavior. | pass — current correction evidence supports corrected claims; historical LF claims are superseded explicitly |
| R-01 | INV-009 | Both states; missing reference/setup and owned extra; drift persists, explicit restoration, repeated match | V-01/V-02 claims | P-01 plus independent P-02 D-02 public probes | pass — restoration and read-only observations corroborated |
| R-02 | INV-009 | Selected drift crossed with unmanaged helper/outside whitespace; first insertion/replacement and refusal; newline siblings | V-03/V-04 claims | P-01 and P-02 D-02/D-03/D-04 | pass — preservation and refusal corroborated |

No required behavioral row is blocked or unchecked. No executable schema
constraint changed or is being claimed here: the schema file is copied content
whose restoration is compared byte-for-byte, not a validator qualification.
No process lifecycle change is in scope; probes invoke bounded synchronous
CLI calls and leave no persistent fixture service.

## 4. Adversarial checks

Selected managed deletion and owned extra coexist with unmanaged helper and
outside-block whitespace in P-02 D-02. Drift survives the first check, explicit
refresh removes only the owned extra, and the helper/raw outside bytes survive.
P-01 tests mixed and lone-CR sibling bytes so the original CRLF trigger cannot
hide a neighboring newline failure. P-02 preserves both target Git states and
exercises first insertion separately from existing block replacement.
P-02 DISC-04 retains malformed refusal after installation. P-01 retains the
fingerprint counterexample so a green identity cannot substitute for projection
equality. No generic concurrency or lifecycle matrix is applicable.

## 5. Independent commands and observations

All commands ran from the repository root, locally, without dependencies being
installed, network access, model calls, or privileged probes. Fixtures use
`TemporaryDirectory`; each probe exits and removes its disposable Git targets.

### P-01 — targeted corrected boundary, journey and fingerprint

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_install_development_skills.DevelopmentProfileCheckTests.test_install_and_refresh_preserve_unmanaged_agents_line_ending_bytes test_install_development_skills.DevelopmentProfileCheckTests.test_journey_detects_drift_read_only_then_explicit_refresh_restores_every_family test_install_development_skills.DevelopmentProfileCheckTests.test_check_detects_managed_drift_that_the_workflow_fingerprint_excludes
```

Exit 0; 3 tests, 7.115 seconds, no skips. Covers V-01/V-02/V-03/V-05 and both
risk rows. Raw byte subtests cover all eight line-ending/Git combinations.

### P-02 — original reviewer regressions and sibling public probes

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 - <<'PY'
from pathlib import Path
import re, subprocess
report = Path('docs/tasks/T-004.3/reviews/discovery-02.md').read_text()
for section in ('D-02','D-03','D-04','D-05'):
    command = re.search(r'^### '+section+r'.*?^```sh\n(.*?)^```$', report, re.S | re.M).group(1)
    print('Running discovery-02', section, flush=True)
    subprocess.run(['/bin/sh','-c',command],check=True)
PY
```

Exit 0; 9.326 seconds tool wall time. Exact underlying commands/setups are the
unchanged numbered sections in discovery-02, tied to its index identity below;
D-02 and D-04 consume unchanged DISC-02/03/04 from discovery-01. No probe was
rewritten. The preservation diagnostics print their oracle rather than fail on
false; their outputs were inspected, not inferred from exit status.

- D-02: both states print `insertion_retains_original_bytes=true`,
  `outside_preserved=true`, restoration/read-only pass. Setup deletion → drift
  → explicit refresh → byte equality → match passes. Unmatched, duplicate and
  reversed markers refuse install/check with exact snapshot preservation.
- D-03: both states print insertion/outside preservation true and
  `checks_match=[true,true]`. Prefix `b'# Instructions\r\n\t \r\n\r\n'` and
  suffix `b'\r\n\tSuffix.  \r\n\r\n'` remain exactly equal after refresh.
- D-04: 9 tests, 4.645 seconds, OK, no skips; retained refusal, guide, selection,
  identity and read-only contract cases.
- D-05: detached target retains its real commit and matches on check.

Installed identity observations: workflow `bounded-task-implementer`,
fingerprint `sha256:a11a7689242a3ecf690971bcf7e85f3e745cebb7ea0168c40dbde08efa717da3`,
`workflow_dirty=false`, `repository_dirty=true` in all three identity fixtures.
Unborn: branch main, commit null. Committed: branch main, commit
`d1d28546f275c7c480d3754ae43b52f7e9f0fd7a`. Detached: branch null, commit
`059039efe67f38aad29f5639713f33c73c4b424c`.

### Static and byte-identity evidence

Commands: `git status --short`, `git status --short --untracked-files=all`,
`git diff --cached --stat`, `git diff --cached -- scripts/install_development_skills.py tests/test_install_development_skills.py`,
`git diff --name-only`, `git rev-parse HEAD`, and scoped reads of the installed
skill/template, task preparation, submissions, historical reviews, installer,
tests, README guidance and cited plan/parent/task map.
For each path below, Python compared `git show :<path>` with `Path.read_bytes()`
and computed SHA-256; `git rev-parse :<path>` supplied independent index blobs.
The binary staged diff was hashed independently. These are identity/static
evidence, not behavioral proof.

`git diff --cached --check` exits 2: pre-existing discovery-02 line 351 has a
blank line at EOF. This historic report formatting issue is not a current
behavioral finding; nothing was edited to remove it.

## 6. Aggregate-gate record

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_install_development_skills test_workflow_version test_run_evidence
```

Status: passed, exit 0; 72 tests in 25.058 seconds, no skips.
Owner: this independent correction discovery. Stage: after P-01/P-02 and
reconciliation of V-01–V-06/R-01/R-02 against the frozen authority and scoped
diff. All selected safe targeted probes were clean; no material behavioral row
remained unrun. This is the prescribed union, not a whole-repository gate.
It does not waive the separate corrected-scope maintainability duty.

## 7. Scope and baseline comparison

Scope is separated: installer/tests are task changes; correction/results are
submission artifacts; prior numbered reviews are historical evidence. The
bounded installer repair is authorized by AC-03. All staged paths have equal
index/worktree bytes. No unexplained user-work overlap was found. Selection,
shared dependencies, source skill packages, active installation, official plans
and preparation inputs were unchanged. No staging, reset or commit occurred.

| Path | Index blob | Index/worktree SHA-256 (equal) |
|---|---|---|
| correction-02.md | `71a208d075b4a7d13b57842cbf17005c71eb24ad` | `6a18772094c5dcaaf5eedd9df7b32d10c7f97d1a877220eabc7e6f571015bea7` |
| results.md | `af61ac08ebe4152ae2159796d1a8c064b4486d17` | `5189b2dc3a1ed2de8ca9b7fd673c3836b303af04f30b5cce9ed195990201a16e` |
| reviews/discovery-01.md | `ceafd28ba97536d6168aec12ca9fc588f76f250d` | `e22bdf908a5a27d772c302807f04acf72f5786b8bd40a8c5ba12eee27064fb96` |
| reviews/discovery-02.md | `acd7671760829a3b0f692ad77611aab177aa08b1` | `800e02e5bc5327f485f68d96da032429afadf6d34b3a63efaf94c254f030755a` |
| reviews/maintainability-01.md | `a08f9965cee74d43d8d4ee8c0c5d9d568c5c6680` | `cce4ecc9dd1bd829b868cd32da9ca1e29a5556da639bb4c3af511a5f44e1a567` |
| scripts/install_development_skills.py | `733660ddf14079482a000e1579254e5cd6dcb08f` | `7423852ffc55738e28ff9562007fa4b511b537a20b2dd24275886fb237370d78` |
| tests/test_install_development_skills.py | `e99aed8ebdffabff2d2fac1d089e55a66fdf95f4` | `5eead744e1a7315082fb73f91a19b81488d7371bc867c792fc34e0144e7d082d` |
| brief.md | `758a4aa7a4288e7b8e758442ae6c422a785099b9` | `bdf0c28a9184c72438b69466046a7eece5971b34b30adf33e28f244adcdc4098` |
| verification.md | `a5bddb43cefaffe6991246181afe8795571dd717` | `50bd1ef5fbd1e196ecfa130eea54d2a86daca0366e52a4b91654b51a7f1617d4` |
| preflight.md | `28f8dd107866e450e11c7386ff30dd1cad55cf4b` | `9f643161c31eb7ff1b90328e8f911b04ed79f82f3e80cafe5fabbe91bc1ea971` |

Task-package-relative paths above are under `docs/tasks/T-004.3/`; script/test
paths are repository-relative. Preparation digests match recorded readiness.
HEAD is unchanged from discovery-02; its older staged diff is superseded by the
staged correction, not reused as current byte identity.

Exact status immediately before report write:

```text
A  docs/tasks/T-004.3/correction-02.md
A  docs/tasks/T-004.3/results.md
A  docs/tasks/T-004.3/reviews/discovery-01.md
A  docs/tasks/T-004.3/reviews/discovery-02.md
A  docs/tasks/T-004.3/reviews/maintainability-01.md
M  scripts/install_development_skills.py
M  tests/test_install_development_skills.py
```

Exact status after report write:

```text
A  docs/tasks/T-004.3/correction-02.md
A  docs/tasks/T-004.3/results.md
A  docs/tasks/T-004.3/reviews/discovery-01.md
A  docs/tasks/T-004.3/reviews/discovery-02.md
A  docs/tasks/T-004.3/reviews/maintainability-01.md
M  scripts/install_development_skills.py
M  tests/test_install_development_skills.py
?? docs/tasks/T-004.3/reviews/discovery-03.md
```

Only this new report entry differs. Index and reviewed worktree identities were
rechecked after writing; the report is the sole repository write.
The first report-audit assertion caught an incorrectly predicted ordering of
the untracked entry in this report's status block. The block was corrected to
the observed Git output; no reviewed bytes or behavioral evidence changed.

## 8. Questions, conditional evidence and residual risks

| Type | Evidence / reason | Owner and route |
|---|---|---|
| Outstanding conditional duty | Historical maintainability-01 reviewed unchanged installer production and an older test blob. Correction-02 requires fresh maintainability for production/read-write and test changes. No such report is supplied. This functional discovery does not substitute for it or record a deferral. | Maintainability stage/coordinator supplies current corrected-scope evidence; acceptance must account for the outstanding duty. |
| Residual qualification boundary | No skill-call, role-call, model-budget, live qualification, full unborn collector lifecycle or retained active-run versions exercised or claimed. | T-005, separately authorized qualification |
| Historical dependency disposition | Preflight/submission note no packaged acceptance reports for .1/.2. Discovery checks consumed local compatibility, not their acceptance record. | Separate acceptance/coordinator owners |

## 9. Completeness and next route

All eight behavioral/material rows are complete with current targeted evidence
and the owned aggregate. No current behavioral finding is confirmed. Hand the
brief, staged diff, this report, correction-02/results, verification revision 1,
ready preflight/Decision context, prior reviewer probes and conditional duty to
the separate `task-acceptance-review` call. Discovery does not authorize
advancement; that call must account for missing corrected-scope maintainability.

## 10. Discovery continuation

```markdown
Discovery continuation:
- Iteration / current byte identity: discovery 3 after correction-02; HEAD 854642406b93f68ef413526db0945bc18c1aff8b; staged binary diff SHA-256 bce72bd22814303da5a1903114c900ae5e3c59aa88ed832453da4026b715f641; all reviewed index/worktree bytes equal.
- Coverage rows: V-01 pass; V-02 pass; V-03 pass; V-04 pass; V-05 pass; V-06 pass; R-01 pass; R-02 pass. No blocked/unchecked required behavioral row.
- Finding IDs: no current findings. Prior F-01 P2 no longer reproduced across insertion/refresh and LF/CRLF/mixed/CR siblings, both Git states. Prior F-02 remains corrected in claims; fingerprint contrast passes.
- Finding/scenario continuity: prior V-03/V-06/R-02 fail now have current P-01/P-02 corroboration; prior passes rerun. Producer B/C/J/R/S are correction-02 claims, not discovery evidence. No incomplete behavioral reason. Correction owner: .3 implementer; evidence owner: fresh discovery for future bytes; authority/disposition owner: separate acceptance. Corrected-scope maintainability is still missing, owned by maintainability/coordinator, never waived here.
- Preparation/context: docs/tasks/T-004.3/brief.md; verification.md revision 1 SHA-256 50bd1ef5fbd1e196ecfa130eea54d2a86daca0366e52a4b91654b51a7f1617d4; ready preflight.md and Decision context; correction-02.md; historical results/discovery-01/discovery-02/maintainability-01.
- Reviewer regressions: P-01 exact three-selector command and P-02 exact extraction wrapper above; underlying discovery-02 D-02/D-03/D-04/D-05 and discovery-01 DISC-02/03/04. No reviewer test asset written.
- Aggregate gate: passed, 72 tests; PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_install_development_skills test_workflow_version test_run_evidence; owned by this independent correction discovery after clean targeted ledger reconciliation.
- Next: separate task-acceptance-review consumes this report and all preparation/submission/regression references, preserving the outstanding corrected-scope maintainability duty.
```
