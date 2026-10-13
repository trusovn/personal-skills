# Task Review Discovery Report: T-004.3 — Prove explicit refresh and distribution closure

| Field | Value |
|---|---|
| Producing stage | `task-review-discovery`, project-local installation |
| Coverage completeness | complete — V-01–V-06 and R-01/R-02 have current dispositions; two confirmed findings |
| Discovery iteration | first independent discovery |
| Created at | 2026-10-13, Europe/Lisbon |
| Repository root | `/Users/mtrusov/work/skill-sources/personal-skills` |
| Durable report path | `docs/tasks/T-004.3/reviews/discovery-01.md` |
| Task brief | `docs/tasks/T-004.3/brief.md` |
| Verification / context | `verification.md` revision 1; ready `preflight.md`, including Decision context, in the same package |
| Current submission | staged `results.md`, state `READY_FOR_REVIEW`; staged `reviews/maintainability-01.md` |

This report publishes evidence only. It contains no acceptance verdict, approved
deferral, or advancement. It applies only to the reviewed bytes below. It does
not review or authenticate itself.

## 1. Discovery provenance

This session authored none of the reviewed production, test, fixture, or
submission bytes. Evidence below is independently corroborated. Active skills:
project-local `task-review-discovery` and `testing-discipline`. No subagents,
live checks, model calls, or installation refresh in this repository were used.

Reviewed HEAD: `854642406b93f68ef413526db0945bc18c1aff8b`.
SHA-256 of `git diff --cached --binary`:
`e2f26b5d3b7bdac627fb1f1ee304e177a6fe67d0198fab75d665c68145766fef`.
Index and worktree identities were checked separately and match; the unstaged
tracked diff is empty. The staged scope contains only the new journey test,
submission results, and the conditional maintainability report.

## 2. Findings

### F-01 [suggested P2] Refresh changes unmanaged AGENTS bytes while the new preservation test stays green

| Field | Evidence |
|---|---|
| Current location | `tests/test_install_development_skills.py:1052` (fixture selection); unchanged implementation at `scripts/install_development_skills.py:176–184`; submitted preservation claim at `docs/tasks/T-004.3/results.md:150` |
| Trigger | A valid managed block with whitespace immediately before the begin marker and an indented first suffix line plus trailing whitespace after the end marker; explicit installer rerun in either committed or unborn Git state |
| Consequence | Refresh changes project instructions outside its ownership. Removing suffix indentation can change Markdown meaning. A subsequent matching check cannot detect this loss because outside-block bytes are correctly excluded from comparison. |
| Evidence | DISC-02: prefix `b'# Instructions\n\t \n\n\n'` becomes `b'# Instructions\n\n'`; suffix `b'\n\n\tSuffix.  \n\n\n'` becomes `b'\n\nSuffix.\n'`, in both Git states. Meanwhile DISC-01, the staged journey, passes. `_render_agents` calls `rstrip()` on the prefix, `strip()` on the suffix, then reconstructs separators. The test places its suffix indentation after a non-whitespace heading, so it avoids this boundary. |
| Affected AC / invariant | AC-03, AC-05; V-03, V-06; R-02 / INV-009: refresh must preserve exact bytes outside an existing block |
| Credible sibling surface | First insertion also uses `existing.rstrip()` and removes terminal instruction whitespace; DISC-02 observes that the original byte sequence is not retained. Blank-only prefixes/suffixes and indentation on the first suffix line share this mechanism. |
| Smallest corrective direction | Preserve unmanaged segments through insertion and block replacement, and make the existing lifecycle evidence exercise whitespace at the segment boundaries. Update the submission claims to the corrected evidence. A bounded preservation repair is explicitly allowed by this brief. |

### F-02 [suggested P2] Results use fingerprint equality to infer full installed-projection equality

| Field | Evidence |
|---|---|
| Current location | `docs/tasks/T-004.3/results.md:131–133` |
| Trigger | The results state that the installed fingerprint equals the source fingerprint, “so the installed distribution is the current source projection.” |
| Consequence | The T-005 evidence handoff gives an insufficient identity oracle for the complete distribution. Copied eval/setup content can drift while the workflow identity remains unchanged. |
| Evidence | DISC-05 executes the existing real-CLI contrast: change installed `bounded-task-implementer/evals/evals.json`; installed fingerprint remains equal and `workflow_dirty` remains false, but `--check` exits 1 with that exact changed path. The test passes. Separate projection comparisons in the submission are useful evidence; they do not make the quoted implication valid. |
| Affected AC / invariant | AC-04, AC-05; V-05, V-06: compatible fingerprint framing and evidence tied to the actual full projection |
| Credible sibling surface | Copied eval fixtures/setup files excluded from workflow fingerprint coverage, and future T-005 consumers that use the recorded identity in place of full managed-content comparison |
| Smallest corrective direction | State the fingerprint's limited identity scope and attribute full-projection equality to independent path/byte comparison and current check output. Keep these evidence boundaries explicit in the T-005 handoff. |

## 3. Completeness ledger

Ledger selected before behavioral execution: V-01–V-06 from verification
revision 1, including the brief's R-01/R-02 probes. No required row was omitted.
No prior discovery ledger exists in this package. Submitted scenario statuses
are all producer-attributed `OK`; they are not independent proof.

| Row | AC / risk | Cases, setup and oracle | Submitted evidence | Independent probe / current result |
|---|---|---|---|---|
| V-01 | AC-01 / R-01 | Real unborn and committed targets; install → fresh match → drift → read-only drift check → explicit refresh → match → repeated match; unchanged Git identity and snapshots around checks | New journey T; manual probe P | **pass** — DISC-01 and DISC-02 execute the ordered journey. DISC-02 snapshots the entire disposable target, including Git metadata, around fresh/drift/restored/repeated checks; no mutation; restored JSON repeats exactly. Unborn HEAD remains unresolvable. DISC-03 reruns current unborn/detached compatibility evidence. |
| V-02 | AC-02 / R-01 | Changed skill/guide/helper/config/schema/valid block; missing reference/eval/setup; owned extra; final source bytes and matching check | T mutates every listed family except setup; setup projection is inspected but not deliberately drifted | **pass** — DISC-01 covers submitted family restoration; DISC-02 deletes a reference and adds an extra, refreshes and compares every expected installed file to source bytes; DISC-04 independently deletes/restores setup content. Source projection, restored reference/setup and owned-extra removal agree with current matching checks. |
| V-03 | AC-03 / R-02 | First insertion and valid existing-block refresh; boundary whitespace; exact unmanaged prefix/suffix/helper bytes; unselected skill/reference and unrelated file; singular markers | T claims byte preservation, selects internal whitespace | **fail** — F-01 / DISC-02 in both Git states. Unmanaged helper survives; DISC-01 confirms unselected skill/reference and unrelated file survival and singular markers for its fixture, but cannot close outside-block preservation. |
| V-04 | AC-03 / R-02 | Malformed/unmatched/duplicate/reversed markers, unusable targets, symlinked `.agents`, wrong-type shared file and unreadable required content; refusal and snapshot preservation | Existing tests claimed green in I | **pass** — DISC-03 reruns retained cases; DISC-04 adds real post-install rerun refusal with exact full-target snapshots for unmatched, duplicate and reversed markers. Each installer/check exits 2 and preserves state. No silent repair. |
| V-05 | AC-04 | Canonical selection, profile guide, six shared files, positional install/check, 0/1/2 semantics, deliberate rerun, three README surfaces; unchanged fingerprint framing | Guidance reconciliation, no README changes | **pass** — static comparison of installer constants, independent focused expectations and all three READMEs; DISC-03 selection/guide/interface cases pass. Flow README contains shared-tool location guidance, no conflicting installer claims. DISC-05 confirms the fingerprint/full-check distinction in the executable interface. The incorrect submission inference is accounted for in V-06/F-02. |
| V-06 | AC-05 | New results: runnable setups, commands/outputs, installed identities, full-projection evidence, explicit unrun skill/model boundaries and T-005 gaps | Results declare every scenario covered and preserved; identity argument at lines 131–133 | **fail** — F-01 disproves the claimed preservation; F-02 disproves the fingerprint implication. DISC-02 corroborates fingerprint `sha256:a11a7689242a3ecf690971bcf7e85f3e745cebb7ea0168c40dbde08efa717da3`, null unborn commit, real committed identity and `workflow_dirty=false`. Historical manual-probe output is producer-attributed, not authenticated; its temporary script is not a durable full script body in results. The ordered CLI/setup description remains reproducible. Unrun skill/model and acceptance/coordinator boundaries are explicitly stated. |
| R-01 | INV-009 | Both real Git states; managed reference deletion + owned extra; explicit restoration and source comparison | V-01/V-02 | **pass** — DISC-02 plus DISC-04; no automatic restoration during check |
| R-02 | INV-009 | Selected drift crossed with unmanaged helper, outside-block whitespace and retained refusal boundaries | V-03/V-04 | **fail** — F-01; helper preservation and refusal subcases pass independently |

No executable schema-validation change or process-lifecycle claim is under
review. The schema file is copied/restored as bytes; semantic schema validation
is not an AC here. Synchronous installer/check subprocesses exited; temporary
targets were removed by `TemporaryDirectory`. No fixture process was left
running. No lifecycle sleeps, background processes or servers were launched.

## 4. Adversarial evidence

The selected/non-selected cross-product restores selected reference/setup
content and removes an owned extra while preserving a non-managed helper.
The same refresh changes outside-block whitespace. The real second restored
check agrees with the first and leaves the entire target snapshot unchanged.
Malformed marker cardinalities/order are refused after an actual first install.
The fingerprint contrast changes excluded copied content while retaining the
same identity, demonstrating the limit of that evidence rather than relying
on schema/syntax checks.

## 5. Independent probes and exact command records

All commands run at the repository root. Python commands use
`PYTHONDONTWRITEBYTECODE=1`; unittest imports use `PYTHONPATH=tests`. No test or
production file was edited. Temporary probe scripts below were passed directly
to Python stdin, not added as repository assets.

### DISC-01 — submitted lifecycle

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_install_development_skills.DevelopmentProfileCheckTests.test_journey_detects_drift_read_only_then_explicit_refresh_restores_every_family
```

Exit 0; 1 test, both Git-state subtests, 1.684 seconds. Establishes the submitted
fixture's behavior; F-01 shows its preservation oracle is incomplete.

### DISC-02 — independent R-01/R-02 public boundary

Executed as `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 - <<'PY'`
with this body and closing `PY`:

```python
import json, subprocess, tempfile
from pathlib import Path
import test_install_development_skills as t

def outside(data):
    begin = data.index(t.installer.AGENTS_BEGIN.encode())
    end = data.index(t.installer.AGENTS_END.encode()) + len(t.installer.AGENTS_END.encode())
    return data[:begin], data[end:]

for committed in (False, True):
    with tempfile.TemporaryDirectory(prefix='t0043-discovery-') as tmp:
        repo = Path(tmp)
        original = b'# Instructions\nKeep trailing spaces.  \n\n\n'
        t.init_repo(repo, agents_text=original.decode(), commit=committed)
        assert t.run_installer(repo).returncode == 0
        initial = (repo / 'AGENTS.md').read_bytes()
        insertion_retains_original = initial.startswith(original)
        for label in ('fresh',):
            before = t.snapshot_tree(repo)
            result = t.run_check(repo)
            assert result.returncode == 0 and json.loads(result.stdout)['match']
            assert before == t.snapshot_tree(repo)
        reference = repo / '.agents/skills/task-implementation-flow/task-review-discovery/references/discovery-report-template.md'
        reference.unlink()
        extra = repo / '.agents/skills/project-direction/discovery-extra.md'
        extra.write_bytes(b'owned extra\n')
        helper = repo / '.agents/scripts/local-discovery.py'
        helper.write_bytes(b'# unmanaged\n')
        agents = repo / 'AGENTS.md'
        # Valid managed block; whitespace immediately outside both markers.
        agents.write_bytes(b'# Instructions\n\t \n\n\n' + t.installer.AGENTS_BLOCK.rstrip().encode() + b'\n\n\tSuffix.  \n\n\n')
        expected_outside = outside(agents.read_bytes())
        before = t.snapshot_tree(repo)
        drift = t.run_check(repo)
        assert drift.returncode == 1
        assert before == t.snapshot_tree(repo)
        assert json.loads(drift.stdout)['differences'] == [
            {'category':'unexpected', 'path':'.agents/skills/project-direction/discovery-extra.md'},
            {'category':'missing', 'path':'.agents/skills/task-implementation-flow/task-review-discovery/references/discovery-report-template.md'}]
        assert t.run_installer(repo).returncode == 0
        assert reference.read_bytes() == (t.ROOT / 'skills/task-implementation-flow/task-review-discovery/references/discovery-report-template.md').read_bytes()
        assert not extra.exists() and helper.read_bytes() == b'# unmanaged\n'
        projection = t.source_projection_snapshot()
        for managed in t.expected_managed_paths() - {'AGENTS.md'}:
            assert (repo / managed).read_bytes() == projection[managed[len('.agents/'):]]
        actual_outside = outside(agents.read_bytes())
        results = []
        for label in ('restored', 'repeated'):
            before = t.snapshot_tree(repo)
            result = t.run_check(repo)
            assert result.returncode == 0 and json.loads(result.stdout)['match']
            assert before == t.snapshot_tree(repo)
            results.append(json.loads(result.stdout))
        assert results[0] == results[1]
        head = subprocess.run(['git','-C',str(repo),'rev-parse','--verify','HEAD'], capture_output=True)
        assert (head.returncode == 0) == committed
        identity = t.installed_identity(repo)
        print(json.dumps({'committed': committed, 'insertion_retains_original_bytes': insertion_retains_original,
            'outside_before': [repr(x) for x in expected_outside],
            'outside_after': [repr(x) for x in actual_outside],
            'outside_preserved': expected_outside == actual_outside,
            'restoration_and_read_only_checks': 'pass', 'identity':identity}, sort_keys=True))
```

Exit 0, 1.736 seconds tool wall time. This diagnostic prints preservation failure
instead of aborting, so exit 0 is not a preservation pass. Both variants report
`outside_preserved=false` and `insertion_retains_original_bytes=false`, with the
before/after bytes in F-01. Restoration and all read-only snapshots pass.

### DISC-03 — retained narrow contract cases

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_install_development_skills.DevelopmentSkillInstallerTests.test_malformed_managed_agents_block_fails_before_target_installation test_install_development_skills.DevelopmentProfileCheckTests.test_check_reports_agents_block_drift_and_precise_marker_failures test_install_development_skills.DevelopmentProfileCheckTests.test_check_failures_retain_existing_refusals_and_stay_distinct_from_drift test_install_development_skills.DevelopmentProfileCheckTests.test_check_reports_unreadable_required_content_as_failure test_install_development_skills.DevelopmentProfileCheckTests.test_check_results_and_repeated_checks_leave_all_state_unchanged test_install_development_skills.DevelopmentProfileCheckTests.test_check_matches_install_from_unrelated_cwd_and_guides_document_semantics test_install_development_skills.DevelopmentSkillInstallerTests.test_profile_contains_repo_stage_and_bounded_delivery_skills test_install_development_skills.DevelopmentSkillInstallerTests.test_profile_guide_covers_every_installed_skill_and_usage_contract test_install_development_skills.DevelopmentSkillInstallerTests.test_installs_profile_into_unborn_repository_without_creating_a_commit
```

Exit 0; 9 tests, 4.369 seconds, no skips. These are selected row probes,
not the task's aggregate gate.

### DISC-04 — setup restoration and post-install malformed-marker refusal

Executed as `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 - <<'PY'`
with this body and closing `PY`:

```python
import json, tempfile
from pathlib import Path
import test_install_development_skills as t
with tempfile.TemporaryDirectory(prefix='t0043-discovery-families-') as tmp:
    repo = Path(tmp)
    t.init_repo(repo, agents_text='# Instructions\n')
    assert t.run_installer(repo).returncode == 0
    relative = '.agents/skills/task-implementation-flow/bounded-task-implementer/evals/files/setup_fixture.py'
    (repo / relative).unlink()
    result = t.run_check(repo)
    assert result.returncode == 1
    assert json.loads(result.stdout)['differences'] == [{'category':'missing', 'path':relative}]
    assert t.run_installer(repo).returncode == 0
    assert (repo / relative).read_bytes() == (t.ROOT / relative[len('.agents/'):]).read_bytes()
    assert t.run_check(repo).returncode == 0
    print('setup fixture deletion -> drift -> explicit refresh -> byte equality -> match: pass')
    agents = repo / 'AGENTS.md'
    valid = agents.read_text()
    for label, content in (
        ('unmatched', t.installer.AGENTS_BEGIN + '\nincomplete\n'),
        ('duplicate', valid + valid),
        ('reversed', t.installer.AGENTS_END + '\n' + t.installer.AGENTS_BEGIN + '\n')):
        agents.write_text(content)
        before = t.snapshot_tree(repo)
        assert t.run_installer(repo).returncode == 2
        assert before == t.snapshot_tree(repo)
        assert t.run_check(repo).returncode == 2
        assert before == t.snapshot_tree(repo)
        print(label + ': install/check refused with exact snapshot preservation')
```

Exit 0, 0.883 seconds tool wall time; setup restored byte-identically; all three
malformed marker variants refused by both public calls without target mutation.

### DISC-05 — fingerprint evidence boundary

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_install_development_skills.DevelopmentProfileCheckTests.test_check_detects_managed_drift_that_the_workflow_fingerprint_excludes
```

Exit 0; 1 test, 0.449 seconds. Demonstrates F-02's counterexample through real
installed identity and check CLIs; altered copied eval bytes retain identity
but produce drift.

Static evidence commands included `git diff --cached -- tests/test_install_development_skills.py`,
reads of brief/verification/preflight/results/maintainability and the active
skill/template, `git ls-files -s docs/tasks/T-004.3 tests/test_install_development_skills.py`,
`git rev-parse HEAD`, `git diff --name-only`, `git diff --cached --check`,
and scoped reads/searches of installer, adjacent tests, the three READMEs and
cited plan/parent authority. `git diff --cached --check` passed; this is
formatting evidence only. Separate index/worktree comparisons used
`git rev-parse :<path>` and `git hash-object <path>`, plus Python SHA-256 of
file bytes and `git diff --cached --binary` output.

## 6. Aggregate-gate record

| Field | Value |
|---|---|
| Exact command | `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_install_development_skills test_workflow_version test_run_evidence` |
| Status | not run |
| Owner / stage | this independent initial discovery |
| Reason | Decisive R-02/V-03 failure suppresses the aggregate under the active discovery skill. Remaining independent, local and affordable row probes were completed; no aggregate was run for completeness. |
| Current evidence | Targeted commands pass for their fixtures; DISC-02 demonstrates preservation failure; DISC-05 demonstrates the incorrect submission inference. No copied implementer/maintainability gate substitutes for discovery evidence. |

A correction discovery must corroborate changed bytes, rerun both reviewer
regressions, reconcile all ledger rows and own this exact aggregate after clean
targeted evidence. Acceptance consumes the record and does not duplicate it.

## 7. Scope and baseline comparison

Preflight recorded HEAD `12c5c4a2901e5e8f3b1fb6bad22e87f69729ffd7`;
submission explains its advance to current HEAD as the docs-only preparation
commit. Brief and verification SHA-256 values still match their recorded
authority. The staged maintainability report identifies the same current HEAD,
test blob and results blob. Its maintainability decision is conditional-stage
context, not functional evidence or a discovery decision.

| Path | Index blob = separately computed worktree blob |
|---|---|
| `docs/tasks/T-004.3/brief.md` | `758a4aa7a4288e7b8e758442ae6c422a785099b9` |
| `docs/tasks/T-004.3/verification.md` | `a5bddb43cefaffe6991246181afe8795571dd717` |
| `docs/tasks/T-004.3/preflight.md` | `28f8dd107866e450e11c7386ff30dd1cad55cf4b` |
| `docs/tasks/T-004.3/results.md` | `93e5926ac1b0fafaa050b4b6d3656a698cc44a87` |
| `docs/tasks/T-004.3/reviews/maintainability-01.md` | `a08f9965cee74d43d8d4ee8c0c5d9d568c5c6680` |
| `tests/test_install_development_skills.py` | `d67286a8d8e4a8f153faf4da4dc20601421fef98` |
| `scripts/install_development_skills.py` | `72561b046b498f72a65b68f04122f1de716bb415` |

Brief SHA-256: `bdf0c28a9184c72438b69466046a7eece5971b34b30adf33e28f244adcdc4098`.
Verification revision 1 SHA-256:
`50bd1ef5fbd1e196ecfa130eea54d2a86daca0366e52a4b91654b51a7f1617d4`.
Preflight SHA-256:
`9f643161c31eb7ff1b90328e8f911b04ed79f82f3e80cafe5fabbe91bc1ea971`.

No unexplained user-work overlap. Production bytes, active `.agents/`, plans,
index entries and prior reports were preserved. The sole repository write is
this new, previously unused discovery path.

Exact status immediately before report creation:

```text
A  docs/tasks/T-004.3/results.md
A  docs/tasks/T-004.3/reviews/maintainability-01.md
M  tests/test_install_development_skills.py
```

Post-write status (confirmed after creation):

```text
A  docs/tasks/T-004.3/results.md
A  docs/tasks/T-004.3/reviews/maintainability-01.md
M  tests/test_install_development_skills.py
?? docs/tasks/T-004.3/reviews/discovery-01.md
```

Only the new report entry differs; reviewed staged diff identity remains the
same. The report stays untracked and was not staged by discovery.

## 8. Questions, unchecked work, and residual risks

No required coverage row remains blocked or unchecked. Findings are failures,
not residual risks. No whole-repository, network, live/model-budget or role-call
check was required or run. Installed skill-call behavior remains explicitly
unrun and belongs to separately authorized T-005 qualification. The preflight
and submission warning that .1/.2 acceptance dispositions are not durable in
their packages is carried forward for their acceptance/coordinator owners;
discovery does not infer those decisions from clean historical reports.

## 9. Coverage completeness and next route

Coverage is complete for this bounded discovery, with F-01/F-02 and failed
V-03/V-06/R-02 rows. Complete coverage does not mean passing behavior.
Next: a separate `task-acceptance-review` call receives the brief, current
staged diff, this report, verification revision 1, ready preflight including
Decision context, results and maintainability report. There are no blocked or
unchecked rows to omit. No advancement or T-005 qualification is recorded.

## 10. Discovery continuation

```text
Discovery continuation:
- Iteration / current byte identity: first independent pass; HEAD 854642406b93f68ef413526db0945bc18c1aff8b; staged binary diff SHA-256 e2f26b5d3b7bdac627fb1f1ee304e177a6fe67d0198fab75d665c68145766fef; index/worktree blobs in section 7.
- Coverage rows: V-01 pass; V-02 pass; V-03 fail F-01; V-04 pass; V-05 pass; V-06 fail F-01/F-02; R-01 pass; R-02 fail F-01. No blocked/unchecked rows.
- Finding IDs: F-01 suggested P2 unmanaged AGENTS whitespace loss; F-02 suggested P2 fingerprint/full-projection inference.
- Finding/scenario continuity: no prior discovery findings; producer claimed V-01–V-06 OK. Current independent evidence contradicts V-03/V-06/R-02 as above. Correction owner: T-004.3 implementer; evidence owner after correction: fresh discovery; authority/decision owner: separate acceptance reviewer, with brief owner for any scope change. Sibling surfaces: initial insertion, prefix/suffix boundary whitespace and indentation; copied eval/setup bytes outside fingerprint coverage. No unfinished evidence row; aggregate deliberately suppressed.
- Preparation/context: docs/tasks/T-004.3/brief.md; verification.md revision 1 and matching SHA-256; ready preflight.md and its Decision context; staged results.md; staged reviews/maintainability-01.md.
- Reviewer regressions: this report section 5 DISC-02 stdin command/body (preservation false in both Git states); DISC-05 exact existing test command (fingerprint contrast). DISC-04 records setup restoration and refusal continuation. No regression test files were written.
- Aggregate gate: not run; exact union in section 6; owner initial independent discovery; decisive preservation failure. Fresh correction discovery owns it after clean targeted evidence.
- Next: separate task-acceptance-review with the brief, staged diff, this report and preparation/submission/conditional evidence above. No discovery verdict or advancement.
```
