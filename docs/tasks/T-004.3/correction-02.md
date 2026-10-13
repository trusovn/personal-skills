# T-004.3 correction of discovery-02

## Pre-edit coverage map

Authority: `docs/tasks/T-004.3/brief.md`; ready
`docs/tasks/T-004.3/preflight.md`; verification revision 1 in
`docs/tasks/T-004.3/verification.md`. Brief and verification SHA-256 values
still match readiness. Correction authority is the user's instruction to fix
`docs/tasks/T-004.3/reviews/discovery-02.md`. Discovery supplies findings, not
an acceptance verdict. There is no preceding acceptance decision supplied.
The staged installer, tests, results and reviews are the authorized correction
baseline; this invocation preserves the index and adds only worktree changes.

F-01: unmanaged AGENTS bytes must survive first insertion and existing-block
refresh. Default text input normalizes CRLF and lone CR before rendering.
Credible siblings are mixed LF/CRLF and lone-CR prefix/suffix bytes, in both
Git states. Correction owner: implementer; evidence owner: fresh discovery;
authority/disposition owner: user and separate acceptance stage.
F-02: earlier fingerprint overclaim is already corrected; preserve the limited
workflow-identity claim and its regression. No new fingerprint change.

| Row | Prior reviewer status | Planned implementation evidence / navigation | Next owner |
|---|---|---|---|
| V-01 | pass | Existing canonical journey test, both Git states; prior pass is navigation only | fresh discovery, then acceptance |
| V-02 | pass | Existing journey's managed projection restoration and full byte comparison; D-02 setup deletion remains fresh-review corroboration | fresh discovery, then acceptance |
| V-03 | fail | D-03 reproducer and raw-byte insertion/refresh regression for LF, CRLF, mixed and lone CR, both Git states; retained unmanaged journey sentinels | implementer correction, then fresh discovery and acceptance |
| V-04 | pass | Retained marker/unsafe-target refusal cases in installer suite; prior pass is navigation only | fresh discovery, then acceptance |
| V-05 | pass | Existing selection/guide/fingerprint regressions and unchanged README/constants reconciliation | fresh discovery, then acceptance |
| V-06 | fail | This correction report records exact commands/results and raw-byte proof; historic results are LF-only observations, superseded for current submission by this report | implementer evidence, then fresh discovery and acceptance |
| R-01 | pass | Existing ordered journey; D-02 reference/setup/extra probe remains fresh-review responsibility | fresh discovery, then acceptance |
| R-02 | fail | Raw-byte regression plus existing journey and refusal suite | implementer correction, then fresh discovery and acceptance |

No prior blocked or unchecked rows. All reviewer row statuses above remain
unchanged until fresh independent review. Final aggregate is discovery-owned:
`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_install_development_skills test_workflow_version test_run_evidence`.
Implementation runs targeted regressions, then the installer suite only.
The correction affects production in the previously reviewed module, so fresh
maintainability review is owed before discovery and separate acceptance.
No architecture gate is declared and no contract registry exists.

## Implementation evidence

Implemented: READY_FOR_REVIEW

This report supersedes the general preservation claims in the historical
`docs/tasks/T-004.3/results.md` for this submission. That file's recorded LF
observations remain historical evidence; it and all prior reviews are unchanged.
Current proof is the commands below, executed locally on the corrected worktree
on 2026-10-13. All filesystem fixtures are disposable real Git repositories;
no network, live model, role call, active-install refresh or acceptance ran.

Deliverables:
- Preserve UTF-8 AGENTS instruction bytes across the complete read/render/write
  boundary. Read bytes then decode, and disable output newline translation.
  The renderer, managed block, marker validation and ownership are unchanged.
- A focused CLI regression covers first insertion and existing-block refresh
  for LF, CRLF, mixed LF/CRLF/CR and lone CR in unborn and committed targets.
  It compares raw original/prefix/suffix bytes, canonical block bytes, singular
  markers, and the full target snapshot around the matching check.
- Three existing journey observation reads now decode raw bytes rather than
  normalizing newlines, so its preservation oracle cannot hide normalization.
- Current commands, outputs, installed identities and remaining route below.

Actual contract impact: none. This restores INV-009's existing preservation
contract without changing profile selection, helper dependencies, CLI or
fingerprint framing. Executable contract declarations changed: none.
`DEVELOPMENT_SKILL_SOURCES`, `PROFILE_SKILLS_README`, `SHARED_SCRIPT_FILES`,
their focused expectations and the three README guides remain applicable.
Guide/selection tests pass in S and R; root/skills guidance still describes a
read-only check with 0/1/2 results and explicit refresh between invocations.
The flow README makes no conflicting installer claim.

### Commands and exact outcomes

B — reviewer D-03, run before and after the production correction:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 - <<'PY'
from pathlib import Path
import re
report = Path('docs/tasks/T-004.3/reviews/discovery-02.md').read_text()
body = re.search(r'### D-03.*?```sh\n.*?<<\x27PY\x27\n(.*?)\nPY\n```', report, re.S).group(1)
exec(compile(body, 'discovery-02 D-03', 'exec'))
PY
```

Both executions exit 0 because the reviewer probe prints its preservation
oracle. Before correction, both Git states printed `insertion_preserved=false`
and `outside_preserved=false`, with both checks matching. After correction,
both print `insertion_preserved=true`, `outside_preserved=true` and
`checks_match=[true,true]`. Raw prefix and suffix remain respectively
`b'# Instructions\r\n\t \r\n\r\n'` and
`b'\r\n\tSuffix.  \r\n\r\n'` before/after refresh. This command exercises
the exact durable reviewer probe, including its original setup and oracles.

C — focused raw-byte regression:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_install_development_skills.DevelopmentProfileCheckTests.test_install_and_refresh_preserve_unmanaged_agents_line_ending_bytes
```

Before the production edit: exit 1, 1 test in 3.006s, six expected insertion
assertion failures (CRLF/mixed/CR in each Git state); LF variants succeed.
After correction: exit 0, 1 test in 5.063s, all eight subtests succeed,
including insertion and refresh. B independently demonstrated the refresh
failure before correction as well. One production fix was attempted; none
was discarded or remains partial.

J — discovery-02 D-01's exact two-selector command:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_install_development_skills.DevelopmentProfileCheckTests.test_journey_detects_drift_read_only_then_explicit_refresh_restores_every_family test_install_development_skills.DevelopmentProfileCheckTests.test_check_detects_managed_drift_that_the_workflow_fingerprint_excludes
```

Exit 0; 2 tests, 2.150s. Both Git states complete the canonical journey with
read-only checks and independent managed projection comparison; fingerprint
contrast still rejects the claim that fingerprint equality proves projection
equality. All expected managed families restore their source bytes.

R — remaining reviewer probes, exact durable commands extracted with a
line-anchored closing fence:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 - <<'PY'
from pathlib import Path
import re, subprocess
report = Path('docs/tasks/T-004.3/reviews/discovery-02.md').read_text()
for section in ('D-02', 'D-04', 'D-05'):
    command = re.search(r'^### '+section+r'.*?^```sh\n(.*?)^```$', report, re.S | re.M).group(1)
    print('Running discovery-02', section, flush=True)
    subprocess.run(['/bin/sh', '-c', command], check=True)
PY
```

Exit 0; tool wall time 7.602s. D-02 reruns DISC-02/DISC-04: both Git states
report insertion/outside preservation true and restoration/read-only checks
pass; setup deletion/restoration passes; unmatched, duplicate and reversed
markers refuse both install/check with exact target snapshot preservation.
D-04: 9 tests in 4.387s, OK. D-05: detached installation/check succeeds and
retains the real commit.

Installed identity observations from R:
- Unborn: branch `main`, commit null.
- Committed: branch `main`, commit `d07db7486e2ca72080479e51e51ddeaebbb0e598`.
- Detached: branch null, commit `39ec85c67afda7d722e1ebccfc66646d870ab47e`.
- Each: workflow `bounded-task-implementer`, fingerprint
  `sha256:a11a7689242a3ecf690971bcf7e85f3e745cebb7ea0168c40dbde08efa717da3`,
  `workflow_dirty=false`, `repository_dirty=true`. Fingerprint is workflow
  identity only; complete managed bytes are separately inspected in J/R.

An initial wrapper attempted D-01/D-02/D-04/D-05 using an unanchored closing
fence. D-01 passed (J), but extraction truncated D-02 at a literal fence in
its regex, yielding `SyntaxError: unterminated string literal`, exit 1.
No D-02 target action occurred. R fixes only wrapper extraction and executes
the original probes unchanged. This was a probe-wrapper failure, not a
failed production fix; no hypothesis or production change was discarded.

S — nearest owning suite, after all reviewer regressions passed:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py
```

Exit 0; 35 tests in 19.340s, no skips. Existing selection, guide, unborn,
detached, fingerprint, malformed-marker and unsafe/unreadable-content tests
remain intact. No dependency installation or repair was needed.

## Correction handoff

- Authority: `docs/tasks/T-004.3/brief.md`.
- Preflight/context reference: `docs/tasks/T-004.3/preflight.md`, its Decision
  context, `docs/tasks/T-004.3/verification.md` revision 1,
  `docs/tasks/T-004.3/results.md`,
  `docs/tasks/T-004.3/reviews/discovery-01.md`,
  `docs/tasks/T-004.3/reviews/discovery-02.md`, and
  `docs/tasks/T-004.3/reviews/maintainability-01.md` (historical, not current
  corrected-scope evidence). Authority bytes remain unchanged and their digests
  match readiness. Dependency, permission and capability boundaries are unchanged.
- Preceding verdict: none supplied. Discovery-02 reports complete coverage
  with F-01 remaining; discovery does not make an acceptance decision.
- Finding/scenario IDs: F-01, prior corrected F-02; V-01–V-06; R-01/R-02.
- Complete findings and invariant: F-01 unmanaged newline normalization is
  corrected across the file boundary; F-02's limited workflow-identity framing
  remains supported by J. No wider identity or check change is claimed.
- Influenced sibling surfaces: insertion/refresh, CRLF/mixed/lone-CR/LF prefix
  and suffix, both Git states (B/C); existing whitespace, unmanaged files,
  refusal, setup/reference restoration and detached compatibility (J/R/S).
- Attempts and discarded hypotheses: B/C fail-first; one boundary fix; B/C/J/R/S
  succeed; one extraction-wrapper failure corrected as recorded above. None
  discarded; no unresolved partial correction.
- Current scoped diff relative to the staged baseline:
  `scripts/install_development_skills.py` (one read replacement and disabled
  write translation); `tests/test_install_development_skills.py` (focused raw-byte
  CLI case and three observation reads); this new `correction-02.md`.
  The staged implementation/results/reviews, official plans and `.agents/`
  installation remain unchanged. No files were staged or committed.
- Reviewer reproducer: exact B command above — preservation true in both states.
- Owning suite: exact S command above — 35 tests OK.
- Broad/aggregate gate:
  `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_install_development_skills test_workflow_version test_run_evidence`
  — not run; authority assigns it to fresh discovery after clean targeted
  evidence. No current independent aggregate is claimed.
- Remaining reviewer coverage: no prior unchecked/blocked rows; all eight rows
  require fresh corrected-byte reconciliation. Prior pass/fail statuses remain
  unchanged below; implementation evidence is not reviewer disposition.
- Next: fresh `task-maintainability-review` → fresh independent
  `task-review-discovery` (regressions, complete ledger and owned aggregate) →
  separate fresh `task-acceptance-review`. No architecture gate or registry
  updater applies. Coordinator advancement and upstream .1/.2 acceptance
  recording remain separate; T-005 skill-call/model/role qualification is unrun.

| Coverage ledger row | Prior reviewer status | Current implementation evidence | Incomplete reason | Next owner / reviewer status |
|---|---|---|---|---|
| V-01 | pass | J/R/S: ordered CLI journey, stable Git identity and read-only checks succeed in both Git states | none in implementation; independent review pending | fresh discovery → acceptance; prior pass unchanged |
| V-02 | pass | J/R/S: changed/missing/extra families including setup restore; full managed projection agrees with source | none in implementation; independent review pending | fresh discovery → acceptance; prior pass unchanged |
| V-03 | fail | B/C/J/R/S: raw insertion/prefix/suffix bytes, singular markers and unmanaged files preserved | none in implementation; independent review pending | fresh discovery → acceptance; prior fail unchanged |
| V-04 | pass | R/S: malformed/unsafe refusals and unchanged-state snapshots succeed | none in implementation; independent review pending | fresh discovery → acceptance; prior pass unchanged |
| V-05 | pass | J/R/S and unchanged guide/constants reconciliation: selection, 0/1/2 semantics, explicit refresh, limited fingerprint, detached compatibility | none in implementation; independent review pending | fresh discovery → acceptance; prior pass unchanged |
| V-06 | fail | B/C/J/R/S and this report: exact runnable setup/commands, observed outputs/identities, accurate raw-byte claims and explicit T-005 gaps | none in implementation; independent evidence audit pending | fresh discovery → acceptance; prior fail unchanged |
| R-01 | pass | J/R/S: both-state real restoration, complete projection and read-only snapshots | none in implementation; independent review pending | fresh discovery → acceptance; prior pass unchanged |
| R-02 | fail | B/C/J/R/S: raw unmanaged preservation and retained refusal contract | none in implementation; independent review pending | fresh discovery → acceptance; prior fail unchanged |

Optional sidecar instrumentation: project-local `.agents/scripts/run_evidence.py`
availability returned `available=true`, active run was null; run
`run-20261013T111404Z-58f7ee80a6ed` began before edits. Its finish outcome is
recorded at handoff. Sidecar identity is for the active installed skill;
source corrections do not refresh that installation or qualify skill behavior.
