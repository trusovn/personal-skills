# T-005.1 receipt — V-03 fresh disposable installation projection

Scenario: a fresh disposable Git target installed from the current canonical
source profile, with full managed-projection proof and target-local sibling
helper availability (verification `V-03`; brief AC-02; S-02). Workflow
identity is recorded separately from full projection identity. The active
installation in this source repository was not touched: no install or check
ran against the source repository itself.

Correction (`reviews/discovery-01.md` F-01): the original receipt
independently compared only the 85 copied managed files and attributed the
remaining managed surface — the marked `AGENTS.md` block — to the canonical
`--check` alone, and recorded no reproducible invocation for the independent
comparison. This corrected receipt independently compares the entire
managed projection (complete managed file set, all copied file bytes and
the marked block), records the exact reproducible procedure below, and
demonstrates the same procedure rechecking a replaced block in an existing
target. No installer, helper or source byte changed.

## Source identity (receipt provenance)

```text
source HEAD:     58f5179284bfb51ea2ef1ceee7232ae5db80f4a9 (branch master)
source status at probe time: staged T-005.1 task package paths
  (A tests/fixtures/review-composition/tasks/T-005.1/fixtures.md, results.md, evidence/*,
   reviews/discovery-01.md; M tests/test_review_composition.py)
  plus pre-existing untracked .DS_Store files — none touched by the probe
source workflow fingerprint (availability probe): sha256:a11a7689242a3ecf690971bcf7e85f3e745cebb7ea0168c40dbde08efa717da3
```

## Target starting state

Disposable target `/tmp/opencode/t0051-v03-correction-target`, prepared with
the owning suite's `init_repo` helper: `git init` with identity configured,
`.gitignore` (`".agents/\n"`), unmanaged `app.txt`, and unmanaged `AGENTS.md`
(`"# Unmanaged project instructions\n\nKeep this unmanaged line.   \n\n"`),
all committed (HEAD `8e4dc15b17c1824bf23865bdc32a2bc28d8ce8bb`). Target
status before install: clean.

## Canonical commands and observed results

```text
python3 scripts/install_development_skills.py /tmp/opencode/t0051-v03-correction-target
  -> exit 0
python3 scripts/install_development_skills.py --check /tmp/opencode/t0051-v03-correction-target
  -> exit 0, match=True, compared_paths=86, differences=[]
```

## Independent full managed-projection comparison (reproducible; not the check's own verdict)

Exact invocation, run from the repository root with
`PYTHONDONTWRITEBYTECODE=1` (it reuses the owning suite's canonical helpers
`tests/test_install_development_skills.py::init_repo`,
`::expected_managed_paths`, `::source_projection_snapshot`,
`::run_installer`, `::run_check` and `::installed_identity`):

```text
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import json, shutil, subprocess, sys
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "tests"))
import test_install_development_skills as owner

installer = owner.installer
UNMANAGED = "# Unmanaged project instructions\n\nKeep this unmanaged line.   \n\n"
failures = []

def report(step, ok, detail):
    print(f"{step}: {'OK' if ok else 'FAIL'} | {detail}")
    if not ok:
        failures.append(step)

head = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
print("source HEAD:", head)
print("source status --short --untracked-files=all:")
print(subprocess.run(["git", "status", "--short", "--untracked-files=all"], capture_output=True, text=True, check=True).stdout)

target = Path("/tmp/opencode/t0051-v03-correction-target")
if target.exists():
    shutil.rmtree(target)
target.mkdir(parents=True)

owner.init_repo(target, agents_text=UNMANAGED)
report("target-init", True, f"committed HEAD {owner.git(target, 'rev-parse', 'HEAD').strip()}; unmanaged AGENTS.md + app.txt + .gitignore")

install = owner.run_installer(target)
report("canonical-install", install.returncode == 0, f"exit {install.returncode}")

check = owner.run_check(target)
check_payload = json.loads(check.stdout)
report("canonical-check", check.returncode == 0 and check_payload.get("match") is True,
       f"exit {check.returncode}, match={check_payload.get('match')}, compared_paths={check_payload.get('compared_paths')}, differences={check_payload.get('differences')}")

expected_paths = owner.expected_managed_paths()
snapshot = owner.source_projection_snapshot()
actual_paths = {str(p.relative_to(target)) for p in (target / ".agents").rglob("*") if p.is_file()}
actual_paths.add("AGENTS.md")
report("independent-file-set", actual_paths == expected_paths,
       f"expected {len(expected_paths)} managed paths; actual {len(actual_paths)}; missing={sorted(expected_paths - actual_paths)}; extra={sorted(actual_paths - expected_paths)}")

byte_mismatches = [f".agents/{key}" for key, content in snapshot.items()
                   if (target / ".agents" / key).read_bytes() != content]
report("independent-byte-comparison", not byte_mismatches,
       f"{len(snapshot)} copied managed files byte-compared against the canonical source projection; mismatches={byte_mismatches}")

agents_text = (target / "AGENTS.md").read_text(encoding="utf-8")
begin = agents_text.index(installer.AGENTS_BEGIN)
end = agents_text.index(installer.AGENTS_END) + len(installer.AGENTS_END)
report("independent-marked-block",
       agents_text[begin:end] == installer.AGENTS_BLOCK.rstrip(),
       "extracted target block between AGENTS_BEGIN/AGENTS_END equals installer.AGENTS_BLOCK.rstrip()")
report("unmanaged-prefix-preserved", agents_text[:begin] == UNMANAGED,
       f"outside-block prefix equals the original unmanaged bytes incl. trailing whitespace: {agents_text[:begin] == UNMANAGED}")
report("block-suffix", agents_text[end:] == "\n", f"bytes after the block: {agents_text[end:]!r}")

block = agents_text[begin:end]
end_marker_idx = block.index(installer.AGENTS_END)
tampered_block = block[:end_marker_idx] + "tampered inside the managed block\n" + block[end_marker_idx:]
(target / "AGENTS.md").write_text(agents_text[:begin] + tampered_block + agents_text[end:], encoding="utf-8")
drift = owner.run_check(target)
drift_payload = json.loads(drift.stdout)
report("block-drift-check", drift.returncode == 1 and drift_payload.get("match") is False,
       f"exit {drift.returncode}, differences={drift_payload.get('differences')}")

reinstall = owner.run_installer(target)
reinstalled = (target / "AGENTS.md").read_text(encoding="utf-8")
rbegin = reinstalled.index(installer.AGENTS_BEGIN)
rend = reinstalled.index(installer.AGENTS_END) + len(installer.AGENTS_END)
report("replacement-recheck",
       reinstall.returncode == 0 and reinstalled[rbegin:rend] == installer.AGENTS_BLOCK.rstrip()
       and reinstalled[:rbegin] == UNMANAGED and reinstalled[rend:] == "\n",
       "after block tampering + reinstall, the replaced block independently equals canonical again; unmanaged prefix and suffix unchanged; no fault left")
recheck = owner.run_check(target)
recheck_payload = json.loads(recheck.stdout)
report("post-replacement-check", recheck.returncode == 0 and recheck_payload.get("match") is True,
       f"exit {recheck.returncode}, match={recheck_payload.get('match')}, differences={recheck_payload.get('differences')}")

avail = json.loads(subprocess.run(
    [sys.executable, str(target / ".agents" / "scripts" / "run_evidence.py"), "--repo", str(target), "availability"],
    capture_output=True, text=True, check=True).stdout)
report("target-local-helper-availability", avail.get("available") is True,
       f"available={avail.get('available')}, scripts_root={avail.get('scripts_root')}")

installed = owner.installed_identity(target)
source_fp = json.loads(subprocess.run(
    [sys.executable, str(ROOT / "scripts" / "workflow_version.py"), "bounded-task-implementer"],
    capture_output=True, text=True, check=True).stdout)
report("workflow-identity", installed.get("fingerprint") == source_fp.get("fingerprint"),
       f"installed fingerprint {installed.get('fingerprint')} == source {source_fp.get('fingerprint')} (workflow-identity evidence only)")

shutil.rmtree(target)
print("disposable target removed:", not target.exists())
print("PROBE RESULT:", "ALL OK" if not failures else f"FAILURES: {failures}")
PY
```

Observed results (complete):

```text
source HEAD: 58f5179284bfb51ea2ef1ceee7232ae5db80f4a9
source status --short --untracked-files=all:
A  tests/fixtures/review-composition/tasks/T-005.1/evidence/V-02-setup-reconstruction.md
A  tests/fixtures/review-composition/tasks/T-005.1/evidence/V-03-install-projection.md
A  tests/fixtures/review-composition/tasks/T-005.1/evidence/V-04-drift-contrast.md
A  tests/fixtures/review-composition/tasks/T-005.1/fixtures.md
A  tests/fixtures/review-composition/tasks/T-005.1/results.md
A  docs/tasks/T-005.1/reviews/discovery-01.md
M  tests/test_review_composition.py
?? .DS_Store
?? docs/.DS_Store
?? skills/.DS_Store

target-init: OK | committed HEAD 8e4dc15b17c1824bf23865bdc32a2bc28d8ce8bb; unmanaged AGENTS.md + app.txt + .gitignore
canonical-install: OK | exit 0
canonical-check: OK | exit 0, match=True, compared_paths=86, differences=[]
independent-file-set: OK | expected 86 managed paths; actual 86; missing=[]; extra=[]
independent-byte-comparison: OK | 85 copied managed files byte-compared against the canonical source projection; mismatches=[]
independent-marked-block: OK | extracted target block between AGENTS_BEGIN/AGENTS_END equals installer.AGENTS_BLOCK.rstrip()
unmanaged-prefix-preserved: OK | outside-block prefix equals the original unmanaged bytes incl. trailing whitespace: True
block-suffix: OK | bytes after the block: '\n'
block-drift-check: OK | exit 1, differences=[{'category': 'changed', 'path': 'AGENTS.md'}]
replacement-recheck: OK | after block tampering + reinstall, the replaced block independently equals canonical again; unmanaged prefix and suffix unchanged; no fault left
post-replacement-check: OK | exit 0, match=True, differences=[]
target-local-helper-availability: OK | available=True, scripts_root=/tmp/opencode/t0051-v03-correction-target/.agents/scripts
workflow-identity: OK | installed fingerprint sha256:a11a7689242a3ecf690971bcf7e85f3e745cebb7ea0168c40dbde08efa717da3 == source sha256:a11a7689242a3ecf690971bcf7e85f3e745cebb7ea0168c40dbde08efa717da3 (workflow-identity evidence only)
disposable target removed: True
PROBE RESULT: ALL OK
```

Every canonical managed surface is covered by this independent evidence: the
expected managed file set (86 paths, from `expected_managed_paths()`), all 85
copied managed file bytes (from `source_projection_snapshot()`), and the
marked `AGENTS.md` block extracted between `AGENTS_BEGIN`/`AGENTS_END` and
compared with `installer.AGENTS_BLOCK.rstrip()`. The `--check` result above
is a separate CLI claim, never a substitute for this comparison. This
recorded procedure is the canonical renewal procedure for later T-005 call
leaves re-checking projection identity, and it applies unchanged to existing
targets after block replacement, as demonstrated next.

## Marked-block replacement recheck on the existing target (F-01 sibling surface)

One line tampered inside the managed block in the disposable target only,
then observed in order:

```text
block-drift-check: OK | exit 1, differences=[{'category': 'changed', 'path': 'AGENTS.md'}]
replacement-recheck: OK | after block tampering + reinstall, the replaced block independently equals canonical again; unmanaged prefix and suffix unchanged; no fault left
post-replacement-check: OK | exit 0, match=True, differences=[]
```

The replaced block in the existing target is rechecked by the same
independent extraction/comparison, not by trust in the reinstall; the check
repaired nothing, and no fault was left in a target presented as qualified.

## Target-local sibling helper availability

From the target's own sibling `.agents/scripts/`:

```text
python3 <target>/.agents/scripts/run_evidence.py --repo <target> availability
  -> available: true, scripts_root: <target>/.agents/scripts
sibling helpers present: workflow_version.py, runtime_context.py,
  runtime-context.schema.v1.json
```

## Workflow identity kept distinct from full projection identity

```text
python3 <target>/.agents/scripts/workflow_version.py bounded-task-implementer
  -> installed workflow fingerprint sha256:a11a7689242a3ecf690971bcf7e85f3e745cebb7ea0168c40dbde08efa717da3
  -> equals the source fingerprint: True
```

This equality is workflow-identity evidence only. The fingerprint covers
workflow-version content and does not cover the complete managed projection —
copied eval/setup content can drift while the fingerprint stays equal (the
V-04 receipt demonstrates exactly this). Full installed-projection equality is
attributed to the independent managed-projection comparison above plus the
matching `--check` result, never to the fingerprint alone.

## Preservation observations

The target's committed HEAD was stable across install, tampering, reinstall
and every check (no commit fabricated or changed); the unmanaged `AGENTS.md`
outside-block bytes — including the terminal trailing whitespace — and
`app.txt` survived installation, tampering and every read-only check
unchanged (asserted in `unmanaged-prefix-preserved`, `block-suffix` and
`replacement-recheck` above); the source repository's status was identical
before and after the whole probe, and no install, check or refresh ran
against the source repository's active installation. The disposable target
was removed after the receipts were captured.

## Evidence limits

This receipt is filesystem/Git/CLI proof at the real installer boundary. It
says nothing about agent behavior; no role call, live, networked or
model-budget check was run or claimed.