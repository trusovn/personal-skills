# T-004.3 Results — Prove explicit refresh and distribution closure

Status: corrected; submission state `READY_FOR_REVIEW`. This file records the
implementer's submission evidence for the completed bytes, including the
correction pass for the two findings of
`docs/tasks/T-004.3/reviews/discovery-01.md` (F-01: refresh/insertion changed
unmanaged `AGENTS.md` whitespace outside the managed block; F-02: this file
used fingerprint equality to infer full installed-projection equality). No
independent review has accepted these bytes. Created per the repository rule
that finished tasks write results next to their plan documents (the
`bounded-task-implementer` skill itself does not mandate a document).

Provenance: authority `docs/tasks/T-004.3/brief.md` (SHA-256
`bdf0c28a9184c72438b69466046a7eece5971b34b30adf33e28f244adcdc4098`), derived
`verification.md` revision 1 (SHA-256
`50bd1ef5fbd1e196ecfa130eea54d2a86daca0366e52a4b91654b51a7f1617d4`, `Source
brief:` resolves to the package brief) and ready `preflight.md`, all three
re-verified current before the first edit. The only post-preflight repository
change was HEAD advancing `12c5c4a` → `8546424` by a docs-only commit adding
this package's `preflight.md`/`verification.md` (bytes unchanged, digests
recomputed and matching). First-pass evidence run
`run-20261013T103149Z-6b47ee927291` (availability green, begin → finish
`completed`); correction-pass evidence run
`run-20261013T105444Z-27d8c09eefc3` (availability green, no open run; begin →
finish `completed` at handoff).

## Deliverables

- `tests/test_install_development_skills.py`: one new consolidated journey
  test, `DevelopmentProfileCheckTests.test_journey_detects_drift_read_only_then_explicit_refresh_restores_every_family`,
  exercising the complete ordered journey through the canonical CLI in both a
  genuine unborn and an ordinary committed disposable target:
  first install → matching fresh check → deliberate managed drift across all
  representative families (changed skill `SKILL.md`, profile guide, shared
  script, shared config, shared schema; missing skill reference and skill
  eval; an owned extra inside a selected package; a changed but still valid
  marked `AGENTS.md` block) → drift check that reports the exact sorted
  nine-entry `differences` list and provably writes nothing (full `.agents`
  tree/AGENTS/Git-status snapshot equality around the call, drifted bytes
  still present afterwards) → one separate explicit installer rerun →
  independent source-projection byte inspection of every managed path (not the
  check's own verdict) → matching recheck → second matching check with an
  identical JSON result. First insertion is asserted to retain the original
  instruction bytes, including terminal trailing whitespace. Outside-block
  `AGENTS.md` prefix/suffix bytes — including deliberate internal whitespace,
  a tab-space line directly before the begin marker, an indented first
  suffix line and trailing spaces/blank lines after the end marker — are
  compared byte-exactly across refresh; unselected skill/reference,
  non-managed helper and unrelated project file survive; markers stay
  singular; unborn branch state (no refs, same symbolic HEAD) or committed
  HEAD identity is asserted stable at every milestone.
- `scripts/install_development_skills.py` (correction for discovery-01 F-01):
  `_render_agents` previously applied `rstrip()`/`strip()` to the unmanaged
  `AGENTS.md` segments in both the refresh and first-insertion paths, so an
  explicit rerun changed project instructions outside its ownership (the
  reviewer observed prefix `b'# Instructions\n\t \n\n\n'` become
  `b'# Instructions\n\n'` and suffix `b'\n\n\tSuffix.  \n\n\n'` become
  `b'\n\nSuffix.\n'`). The repair replaces only the managed block: a refresh
  now splices the canonical block between the untouched prefix and suffix
  bytes, and a first insertion retains the original bytes exactly, adding
  only the newlines needed to place the block on its own line after a blank
  separator line. Rendering for every previously observed input shape whose
  existing text carries no boundary whitespace (prefix ending in zero, one or
  two newlines; empty or absent `AGENTS.md`) is byte-identical to the previous
  behavior — only the lossy whitespace normalization changed. Fail-first
  evidence recorded before the repair (commands F-01a/F-01b below).
- `docs/tasks/T-004.3/results.md`: this file, including the F-02 correction of
  its installed-identity evidence claims.
- No README changes: root `README.md` (installer/rerun/refresh guidance at
  lines 79–147, including "refresh deliberately by rerunning the installer
  between check invocations") and `skills/README.md` ("Checking the installed
  profile", lines 58–95, same semantics) already agree with the implemented
  install/check/result/refresh interface; the required phrases are locked by
  `CHECK_GUIDE_REQUIRED_PHRASES` in the green guides test.
  `skills/task-implementation-flow/README.md` makes no installer/check/refresh
  claims (only shared-tooling location notes), so there is nothing to
  reconcile there.

Local design decision (reversible): a new consolidated journey test rather
than extending the `.1`-era rerun case — the brief requires keeping `.1/.2`
local cases intact, and the journey composes `.2`'s isolated per-family
comparator coverage (reused unchanged) instead of duplicating its matrix. All
fixtures reuse existing module helpers (`init_repo`, `run_installer`,
`run_check`, `snapshot_tree`, `source_projection_snapshot`,
`expected_managed_paths`, `collect_package_files`, `git`); no new shared
helper, harness or fixture generator was added.

Actual contract impact: none — no durable cross-task interface changed (the
positional install and `--check` commands, exit codes, JSON result shape and
marker contract are unchanged; the internal `AGENTS.md` rendering became
strictly byte-preserving, which strengthens the already-documented
"preserves existing target `AGENTS.md` content" semantics) and no
`docs/contracts` registry exists. This task closes the
`ART-009/010/011`, `IF-007`, `FLOW-004`, `INV-009` composition with
filesystem/Git evidence, per the brief's expected contract impact.

Executable contract declarations changed: none.

## Exact commands and results

From the repository root (`PYTHONDONTWRITEBYTECODE=1`; the suite and probe
ran on this machine as a non-root user):

| ID | Exact command | Result |
|---|---|---|
| F-01a | reviewer regression DISC-02 body (`docs/tasks/T-004.3/reviews/discovery-01.md` §5) run as `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -` on uncorrected bytes | prints `outside_preserved=false` and `insertion_retains_original_bytes=false` in both Git states — F-01 reproduced on current bytes |
| F-01b | `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_install_development_skills.DevelopmentProfileCheckTests.test_journey_detects_drift_read_only_then_explicit_refresh_restores_every_family` (strengthened fixture, before the production edit) | FAILED (failures=2): the insertion-retention assertion is false in both Git states — fail-first regression for the `_render_agents` repair |
| T | `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_install_development_skills.DevelopmentProfileCheckTests.test_journey_detects_drift_read_only_then_explicit_refresh_restores_every_family` (after the repair) | 1 test OK (0.797s), both `commit=True/False` subTests green |
| RR-01 | reviewer regression DISC-02 body run again on corrected bytes | `outside_preserved=true`, `insertion_retains_original_bytes=true`; restoration, owned-extra removal, unmanaged-helper survival and read-only snapshot checks pass in both Git states |
| RR-02 | `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_install_development_skills.DevelopmentProfileCheckTests.test_check_detects_managed_drift_that_the_workflow_fingerprint_excludes` (DISC-05, the F-02 counterexample) | 1 test OK (0.215s) — altered copied eval bytes keep the workflow fingerprint equal and `workflow_dirty=false` while `--check` exits 1 naming that exact path; F-02 needs no code change, only corrected claims below |
| I | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py` | 34 tests OK (6.423s), no skips — 33 pre-existing `.1`/`.2` cases intact (incl. all refusal/malformed-marker and guides cases) + the journey test |
| P | canonical-CLI probe `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/opencode/t0043-journey-probe-correction.py <repository-root>` (full body recorded under "Reproducible starting states" below; disposable targets under `/tmp/opencode`, cleaned afterwards) | full journey observed in both Git states on corrected bytes; outputs below |

The `_render_agents` repair required the fail-first evidence above: F-01a
reproduced the reviewer's probe on current bytes, and F-01b turned the defect
into a suite-level red before the production edit, per the brief's
record-fail-first rule for preservation repairs. The journey test's
assertions are the direct inverse of the credible faults — a repairing
checker breaks the drift exit/1 + snapshot-equality assertions, and a lossy
insertion/refresh breaks the retention and outside-byte assertions.

## Reproducible starting states and observed journey (probe P)

Starting state per target: `git init` with `user.email/user.name` configured;
`AGENTS.md` = `# Project instructions\n\nKeep this line.   \n\nPrefix note:\n    keep this aligned detail.  \n\n\n`
(retaining terminal trailing spaces and blank lines); `app.txt` = `baseline\n`;
`.gitignore` = `.agents/\n`. The committed variant adds one `baseline`
commit; the unborn variant commits nothing. Drift introduced between checks:
`deliberately drifted\n` written to
`.agents/skills/project-direction/SKILL.md`, deletion of
`.agents/skills/task-implementation-flow/task-review-discovery/references/discovery-report-template.md`,
and `extra owned file\n` written to
`.agents/skills/project-direction/unexpected-local.md`. The unmanaged project
edit inserts a `"\t \n"` line directly before the begin marker and appends an
indented first suffix line ending in trailing spaces and blank lines.

Observed identically in both targets on corrected bytes (canonical calls
`python3 scripts/install_development_skills.py <target>` and
`python3 scripts/install_development_skills.py --check <target>`):

```text
install exit=0
fresh check exit=0          match=True  compared=86  differences=[]
insertion retains original AGENTS.md bytes (incl. terminal whitespace): True
drift check exit=1          match=False
  changed     .agents/skills/project-direction/SKILL.md
  unexpected  .agents/skills/project-direction/unexpected-local.md
  missing     .agents/skills/task-implementation-flow/task-review-discovery/references/discovery-report-template.md
after-drift SKILL.md bytes: deliberately drifted      (the check repaired nothing)
explicit refresh exit=0
outside-block bytes preserved across refresh (prefix and suffix): True
restored check exit=0       match=True  compared=86  differences=[]
second restored check exit=0  repeat-identical=True
```

Byte-level preservation observed in both targets — the unmanaged prefix and
suffix are identical before and after the explicit refresh:

```text
prefix before == after:  b'# Project instructions\n\nKeep this line.   \n\nPrefix note:\n    keep this aligned detail.  \n\n\n\t \n'
suffix before == after:  b'\n\n\tAfter-block project note:\n    indented suffix survives.  \n\n\n'
```

Git/identity observations:

```text
unborn target:    HEAD resolvable before/after journey: False/False   (no commit fabricated)
committed target: HEAD resolvable before/after journey: True/True     (baseline commit retained)
both targets:      installed fingerprint: sha256:a11a7689242a3ecf690971bcf7e85f3e745cebb7ea0168c40dbde08efa717da3
                  equals source availability fingerprint: True
```

The installed fingerprint equals this source repository's own
`run_evidence.py availability` workflow fingerprint. That equality is
workflow-identity evidence only: the fingerprint covers workflow-version
content, not the complete managed projection — copied eval/setup content can
drift while the fingerprint stays equal and `workflow_dirty` stays `false`
(the reviewer's DISC-05 contrast: changing installed
`bounded-task-implementer/evals/evals.json` leaves the fingerprint equal while
`--check` exits 1 naming that exact path). Full installed-projection equality
is attributed to the independent managed-path byte comparison — the journey
test's `source_projection_snapshot()`/`expected_managed_paths()` inspection of
all 86 managed paths — corroborated by the current matching `--check` output,
never to the fingerprint alone. The committed target's `repository_commit` is
its baseline commit — no commit was created or fabricated by any
install/check/refresh call. The suite-level journey test additionally proves
(both states) the multi-family restoration, exact sorted differences,
snapshot-equal non-mutating checks, independent projection equality,
first-insertion byte retention, outside-block byte preservation and
unmanaged survival summarized under Deliverables.

Exact probe body (run as `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/opencode/t0043-journey-probe-correction.py <repository-root>`; disposable targets under `/tmp/opencode`, removed by their context managers):

```python
#!/usr/bin/env python3
"""T-004.3 canonical-CLI journey probe (correction pass).

Runs the real positional installer and ``--check`` CLI of this repository in
one disposable unborn and one disposable committed Git target. Journey: first
install -> fresh matching check -> deliberate managed drift + unmanaged edit
with whitespace at both marker boundaries -> read-only drift check -> explicit
installer rerun (refresh) -> matching recheck -> repeated identical check.
Also observes first-insertion byte retention, outside-block byte preservation
across refresh, and installed identity via the installed run-evidence helper.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(sys.argv[1]).resolve()
INSTALLER = REPO / "scripts" / "install_development_skills.py"
BEGIN = b"<!-- personal-skills:development-install:begin -->"
END = b"<!-- personal-skills:development-install:end -->"
ORIGINAL = (
    "# Project instructions\n"
    "\n"
    "Keep this line.   \n"
    "\n"
    "Prefix note:\n"
    "    keep this aligned detail.  \n"
    "\n"
    "\n"
)


def cli(*args):
    return subprocess.run(
        [sys.executable, str(INSTALLER), *args],
        capture_output=True,
        text=True,
        cwd=str(REPO),
        check=False,
    )


def outside(data: bytes):
    begin = data.index(BEGIN)
    end = data.index(END) + len(END)
    return data[:begin], data[end:]


source_availability = subprocess.run(
    [sys.executable, str(REPO / "scripts" / "run_evidence.py"), "--repo", str(REPO), "availability"],
    capture_output=True,
    text=True,
    check=False,
)
source_fingerprint = json.loads(source_availability.stdout)["workflow"]["fingerprint"]
print("source availability fingerprint:", source_fingerprint)

for committed in (False, True):
    with tempfile.TemporaryDirectory(prefix="t0043-probe-", dir="/tmp/opencode") as tmp:
        target = Path(tmp)
        (target / "AGENTS.md").write_text(ORIGINAL, encoding="utf-8")
        (target / "app.txt").write_text("baseline\n", encoding="utf-8")
        (target / ".gitignore").write_text(".agents/\n", encoding="utf-8")
        subprocess.run(["git", "init"], cwd=target, capture_output=True, check=True)
        subprocess.run(["git", "-C", str(target), "config", "user.email", "probe@example.invalid"], check=True)
        subprocess.run(["git", "-C", str(target), "config", "user.name", "Probe"], check=True)
        if committed:
            subprocess.run(["git", "-C", str(target), "add", "-A"], check=True)
            subprocess.run(["git", "-C", str(target), "commit", "-m", "baseline"], check=True)

        state = "committed" if committed else "unborn"
        head_before = subprocess.run(
            ["git", "-C", str(target), "rev-parse", "--verify", "HEAD"], capture_output=True
        )

        install = cli(str(target))
        fresh = cli("--check", str(target))
        inserted = (target / "AGENTS.md").read_bytes()
        insertion_retains = inserted.startswith(ORIGINAL.encode())
        fresh_info = json.loads(fresh.stdout)

        # Deliberate managed drift: changed skill, missing reference, owned extra.
        (target / ".agents/skills/project-direction/SKILL.md").write_text("deliberately drifted\n")
        (target / ".agents/skills/task-implementation-flow/task-review-discovery/references/discovery-report-template.md").unlink()
        (target / ".agents/skills/project-direction/unexpected-local.md").write_text("extra owned file\n")

        # Unmanaged project edit: whitespace immediately at both marker boundaries.
        agents_bytes = inserted.replace(BEGIN, b"\t \n" + BEGIN)
        agents_bytes += b"\n\tAfter-block project note:\n    indented suffix survives.  \n\n\n"
        (target / "AGENTS.md").write_bytes(agents_bytes)
        prefix_before, suffix_before = outside((target / "AGENTS.md").read_bytes())

        drift = cli("--check", str(target))
        drift_info = json.loads(drift.stdout)
        skill_after_drift = (target / ".agents/skills/project-direction/SKILL.md").read_bytes()

        refresh = cli(str(target))
        prefix_after, suffix_after = outside((target / "AGENTS.md").read_bytes())

        restored = cli("--check", str(target))
        repeated = cli("--check", str(target))
        restored_info = json.loads(restored.stdout)
        repeated_info = json.loads(repeated.stdout)

        installed_availability = subprocess.run(
            [sys.executable, str(target / ".agents" / "scripts" / "run_evidence.py"), "--repo", str(target), "availability"],
            capture_output=True,
            text=True,
            check=False,
        )
        installed_fingerprint = json.loads(installed_availability.stdout)["workflow"]["fingerprint"]
        head_after = subprocess.run(
            ["git", "-C", str(target), "rev-parse", "--verify", "HEAD"], capture_output=True
        )

        print(f"[{state}] install exit={install.returncode}")
        print(
            f"[{state}] fresh check exit={fresh.returncode} match={fresh_info['match']} "
            f"compared={fresh_info['compared_paths']} differences={fresh_info['differences']}"
        )
        print(f"[{state}] insertion retains original bytes: {insertion_retains}")
        print(
            f"[{state}] drift check exit={drift.returncode} match={drift_info['match']} "
            f"differences={json.dumps(drift_info['differences'], sort_keys=True)}"
        )
        print(f"[{state}] after-drift SKILL.md bytes: {skill_after_drift.decode().strip()}")
        print(f"[{state}] explicit refresh exit={refresh.returncode}")
        print(f"[{state}] outside-block bytes preserved across refresh: {prefix_before == prefix_after and suffix_before == suffix_after}")
        print(f"[{state}] prefix repr before={prefix_before!r} after={prefix_after!r}")
        print(f"[{state}] suffix repr before={suffix_before!r} after={suffix_after!r}")
        print(
            f"[{state}] restored check exit={restored.returncode} match={restored_info['match']} "
            f"compared={restored_info['compared_paths']} differences={restored_info['differences']}"
        )
        print(f"[{state}] repeated check identical JSON: {restored.stdout == repeated.stdout}")
        print(f"[{state}] HEAD resolvable before/after journey: {head_before.returncode == 0}/{head_after.returncode == 0}")
        print(f"[{state}] installed fingerprint={installed_fingerprint} equals source: {installed_fingerprint == source_fingerprint}")
```

## Scenario and finite-risk evidence

Implementation checks, not independent acceptance evidence. Every verification
scenario ID is accounted for; none blocked or unchecked.

| Scenario | Evidence (test, oracle, result) |
|---|---|
| V-01 | Journey test (T): both Git states cross the complete ordered journey — install 0, fresh match with `compared_paths` equal to the independently enumerated 86-path projection, drift exit 1 with exact paths, snapshot-equal state across the drift check with drifted bytes persisting, explicit rerun 0, matching recheck 0, second matching check with identical JSON; unborn branch state / committed HEAD stable at every milestone — OK; probe P reproduced the ordered milestones at the canonical CLI — OK; `.1`'s untouched `test_installs_profile_into_unborn_repository_without_creating_a_commit` retains detached/unborn compatibility proof — OK in I |
| V-02 | Journey test (T): changed (skill, guide, shared script, config, schema, valid block) and missing (reference, eval) representatives plus an owned extra are all reported by the drift check and all restored to current source bytes by the explicit rerun; the independent `source_projection_snapshot()`/`expected_managed_paths()` byte inspection of every managed path agrees with the matching recheck; the extra is gone — OK; `.2`'s per-family changed/missing comparator tests reused intact (not duplicated) — OK in I |
| V-03 | Journey test (T): first insertion retains the original instruction bytes, including terminal trailing whitespace; outside-block prefix/suffix bytes — deliberate internal whitespace, a tab-space line directly before the begin marker, an indented first suffix line and trailing spaces/blank lines after the end marker — compared byte-exactly across refresh; unselected skill/reference, non-managed helper and unrelated project file byte-identical after refresh; exactly one begin/end marker — OK; reviewer regression DISC-02 rerun green on corrected bytes (RR-01: `outside_preserved=true`, `insertion_retains_original_bytes=true` both Git states); `.1` rerun test's whole-text AGENTS equality and `.2` sentinel coverage retained — OK in I |
| V-04 | Existing refusal cases — malformed/duplicate/reversed markers (exit 2, never a match), nonexistent/non-Git/non-root targets, symlinked `.agents`, wrong-type shared script, unreadable required content — rerun unchanged and green in I; the journey's block drift uses changed valid block content, keeping restoration separate from refusal |
| V-05 | Guides test `test_check_matches_install_from_unrelated_cwd_and_guides_document_semantics` green in I; scoped reconciliation: root README and `skills/README.md` document positional install, `--check` read-only scope, exit 0/1/2 result semantics, retained-versions denial and deliberate between-invocation refresh; the flow README makes no installer/check/refresh claims; no overclaim of unborn collector lifecycle, retained active-run versions or skill-call qualification found — no edits required |
| V-06 | This file: reproducible starting states, exact CLI/probes, observed outputs, installed identity evidence, filesystem/Git proof distinguished from unrun behavior, and the T-005 handoff below |

Risk rows: R-01 / INV-009 → V-01 + V-02 (ordered real occurrences with
check/Git snapshots and source-to-installed byte comparison); R-02 / INV-009
→ V-03 + V-04 (byte preservation, singular markers, unchanged refusal
boundaries). AC mapping: AC-01 → V-01; AC-02 → V-02; AC-03 → V-03/V-04;
AC-04 → V-05; AC-05 → V-06.

## Filesystem/Git proof versus unrun behavior

Everything above is filesystem/Git proof: real canonical CLI calls in
disposable local Git targets, byte snapshots, and Git identity observations.
No skill invocation, role call, live/model-budget behavior, or agent
qualification was run or is claimed; those belong to T-005 and are explicitly
unproven here.

## T-005 handoff

- Qualified `ART-010` projection: 20 selected skill packages (references,
  evals, setup files included), the profile guide, 6 shared scripts
  (config/schema included) and one marked `AGENTS.md` block installed
  byte-identically from source; refresh is a separate explicit installer
  rerun; identity fingerprint
  `sha256:a11a7689242a3ecf690971bcf7e85f3e745cebb7ea0168c40dbde08efa717da3`
  is stable across unborn and committed targets and equals the source
  repository's own. Fingerprint scope for T-005 consumers: it is
  workflow-identity evidence only and does not cover copied eval/setup
  content; full installed-projection equality is proven by the independent
  managed-path byte comparison plus a matching `--check`, not by the
  fingerprint.
- `ART-011` check interface: `--check <target>` exits 0 match / 1 drift or
  missing installation / 2 failure, printing one sorted JSON object with
  `match`, `compared_paths`, `differences` (`changed|missing|unexpected`);
  it is read-only and never repairs.
- Remaining T-005 qualification gaps: installed-flow skill invocation and
  role-call behavior, model-budget and live qualification — all unrun here;
  also no `acceptance-*.md` disposition is recorded yet for the T-004.1,
  T-004.2 or this package (preflight warning carried forward), and
  coordinator advancement remains separate authorized work.

## Skipped stronger checks and their owners

- The justified final aggregate
  `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_install_development_skills test_workflow_version test_run_evidence`
  is owned by the fresh correction `task-review-discovery` after it reruns both
  reviewer regressions (the DISC-02 probe body with the corrected oracle and
  the DISC-05 fingerprint-contrast test) and reconciles all ledger rows; this
  pass ran the owning installer suite (command I, 34 OK) and the reviewer
  regressions as implementation evidence.
- No whole-repo, network, or model-budget gate exists for this task (excluded
  by the brief).
- The brief's soft budget (10 tool calls / 25 minutes / 40k context) was
  crossed in the first implementation pass; both passes remained bounded and
  were completed safely per the soft-checkpoint rule.

## Review handoff

Per `review: immediate`, the corrected bytes go next, in order, to: a fresh
`task-maintainability-review` of the corrected scope, then fresh independent
`task-review-discovery`, then its report to a separate fresh
`task-acceptance-review`. Conditional-stage judgment: no repository policy
declares a deterministic architecture gate for these bytes (the completed
bytes' maintainability report records `ARCHITECTURE_GATE: NOT_AVAILABLE`) and
no `docs/contracts` registry exists, so no architecture gate or registry
stage applies. The maintainability stage re-enters for the corrected scope:
this correction changes production bytes (`_render_agents` in
`scripts/install_development_skills.py`) inside the module surface the
completed bytes' maintainability report described as unchanged, so its prior
ACCEPT does not cover the corrected bytes; fresh discovery may challenge this
judgment. The implementer invocation ends here without a self-issued verdict.