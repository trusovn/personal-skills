"""Administrative link, whitespace and preservation check; no behavioral oracle."""

import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PACKAGE = Path("docs/tasks/T-005.6")
REPORT = Path("skills/task-implementation-flow/docs/standalone-policy-qualification-results-T-005.md")
DOCUMENTS = [PACKAGE / name for name in ("verification.md", "preflight.md", "results.md")]
DOCUMENTS.append(REPORT)
ALLOWED = {str(path) for path in DOCUMENTS}
ALLOWED.update(str(PACKAGE / "evidence" / name) for name in ("check_report.py", "protected-before.json"))


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True)


baseline = json.loads((ROOT / PACKAGE / "evidence/protected-before.json").read_text())
assert git("rev-parse", "HEAD").strip() == baseline["head"], "HEAD changed"
for name, expected in baseline["sha256"].items():
    path = ROOT / name
    assert path.is_file(), f"Protected file missing: {name}"
    assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, f"Protected file changed: {name}"

links = 0
for name in DOCUMENTS:
    path = ROOT / name
    content = path.read_text()
    assert content.endswith("\n"), f"Missing final newline: {name}"
    assert all(line == line.rstrip() for line in content.splitlines()), f"Trailing whitespace: {name}"
    for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", content):
        if "://" in target or target.startswith("#"):
            continue
        destination = target.split("#", 1)[0]
        assert (path.parent / destination).is_file(), f"Broken link in {name}: {target}"
        links += 1

status = git("status", "--short", "--untracked-files=all")
changed = {line[3:] for line in status.splitlines()}
assert changed <= ALLOWED, f"Out-of-scope changes: {sorted(changed - ALLOWED)}"
assert changed == ALLOWED, f"Expected new paths missing: {sorted(ALLOWED - changed)}"
assert all(line.startswith("?? ") for line in status.splitlines()), "Unexpected tracked or staged edit"
print(f"PASS: {links} local file links resolve; {len(baseline['sha256'])} protected files and HEAD unchanged")
print(f"PASS: new Markdown whitespace; exactly {len(changed)} allowed new paths; no tracked/staged edits")
print("Administrative checks only; semantic claims require source reading and independent discovery.")
