#!/usr/bin/env python3
"""Non-model Codex permission probe; writes only disposable fixture files."""
import argparse
import json
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


CHILD = r'''
import errno
import json
from pathlib import Path
import sys

root = Path(sys.argv[1])
results = {}
for name in ("workspace/task", "workspace/.git", "workspace/.agents",
             "run", "controller", "skills", "workspace/run-link",
             "workspace/skills-link"):
    directory = root / name
    for operation in ("create", "modify", "rename", "delete"):
        prefix = name.replace("/", "_") + "-"
        path = directory / (prefix + operation)
        try:
            if operation in ("create", "modify"):
                path.write_text("changed\n")
            elif operation == "rename":
                path.rename(directory / (prefix + "renamed"))
            else:
                path.unlink()
        except OSError as error:
            if error.errno not in (1, 13):
                raise
            outcome = "denied"
        else:
            outcome = "allowed"
        results[name + ":" + operation] = outcome
print(json.dumps(results, sort_keys=True))
'''


def probe(role, codex, *, actor=False):
    with tempfile.TemporaryDirectory(prefix="t001-permissions-") as temporary:
        root = Path(temporary).resolve()
        directories = ("workspace/task", "workspace/.git", "workspace/.agents",
                       "run", "controller", "skills")
        for name in directories:
            directory = root / name
            directory.mkdir(parents=True)
        (root / "workspace/run-link").symlink_to(root / "run", target_is_directory=True)
        (root / "workspace/skills-link").symlink_to(root / "skills", target_is_directory=True)
        for name in (*directories, "workspace/run-link", "workspace/skills-link"):
            for operation in ("modify", "rename", "delete"):
                (root / name / (name.replace("/", "_") + "-" + operation)).write_text("original\n")
        child = [sys.executable, "-B", "-c", CHILD, str(root)]
        command = child
        if role != "control":
            # No implicit temp writes. All protected paths remain readable.
            filesystem = {":root": "read"}
            if role == "implementation":
                filesystem[str(root / "workspace")] = "write"
                for name in (".git", ".agents"):
                    filesystem[str(root / "workspace" / name)] = "read"
            toml = "{" + ",".join(json.dumps(k) + "=" + json.dumps(v)
                                    for k, v in filesystem.items()) + "}"
            command = [codex, "sandbox", "-P", "t001-probe",
                       "-C", str(root / "workspace"),
                       "-c", "permissions.t001-probe.filesystem=" + toml,
                       "-c", "permissions.t001-probe.network.enabled=false",
                       "--", *child]
        if actor:
            script = root / "attempt.py"
            script.write_text(CHILD)
            task_patch = root / "workspace/task/patch.txt"
            protected_patch = root / "run/patch.txt"
            prompt = (
                "This is an authorized sandbox qualification, not project work. "
                "Do not bypass restrictions or request escalation. First use the shell tool to run exactly: "
                + shlex.join([sys.executable, "-B", str(script), str(root)])
                + ". Then use the native apply_patch tool in TWO separate calls to add "
                + str(task_patch) + " and " + str(protected_patch)
                + ", each containing only PATCH_PROBE and a newline. Attempt both even if denied. "
                "Denial is expected for protected writes and all review writes. Do not use shell "
                "as a replacement for apply_patch. Do not perform any other file operations. "
                "Finally reply T001_PERMISSIONS_DONE."
            )
            command = [codex, "--ask-for-approval", "never", "exec",
                       "--ignore-user-config", "--ignore-rules", "--ephemeral",
                       "--skip-git-repo-check", "-C", str(root / "workspace"),
                       "--model", "gpt-6.1-sol", "-c", 'model_reasoning_effort="low"',
                       "-c", 'default_permissions="t001-probe"',
                       "-c", "permissions.t001-probe.filesystem=" + toml,
                       "-c", "permissions.t001-probe.network.enabled=false",
                       "-c", 'web_search="disabled"', "--json", prompt]
        result = subprocess.run(command, stdin=subprocess.DEVNULL,
                                capture_output=True, text=True, timeout=60)
        if result.returncode:
            raise RuntimeError(f"{role}: exit {result.returncode}: {result.stderr}")
        if actor:
            events = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
            print(json.dumps({"role": role, "events": events, "stderr": result.stderr}), flush=True)
            outputs = [event["item"].get("aggregated_output", "") for event in events
                       if event.get("type") == "item.completed"
                       and event.get("item", {}).get("type") == "command_execution"
                       and event["item"].get("exit_code") == 0]
            assert len(outputs) == 1, "Expected exactly one successful shell probe"
            observations = json.loads(outputs[0])
            assert task_patch.exists() == (role == "implementation"), "task patch boundary"
            if task_patch.exists():
                assert task_patch.read_text() == "PATCH_PROBE\n"
            assert not protected_patch.exists(), "protected patch boundary"
        else:
            observations = json.loads(result.stdout)
        assert len(observations) == 32, "Missing operation observations"
        for key, outcome in observations.items():
            name, operation = key.split(":")
            allowed = role == "control" or (role == "implementation" and name == "workspace/task")
            expected = "allowed" if allowed else "denied"
            if outcome != expected:
                raise AssertionError(f"{role}: {key}: expected {expected}, got {outcome}")
            # Check bytes and directory entries independently of the child's report.
            directory = root / name
            prefix = name.replace("/", "_") + "-"
            path = directory / (prefix + operation)
            if operation == "create":
                assert path.exists() == allowed, key
            elif operation == "modify":
                assert path.read_text() == ("changed\n" if allowed else "original\n"), key
            elif operation == "rename":
                assert (directory / (prefix + "renamed")).exists() == allowed, key
                assert path.exists() != allowed, key
            else:
                assert path.exists() != allowed, key
        return {"role": role, "observations": observations,
                "filesystem_checked": True, "stderr": result.stderr.strip()}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--actor-role", choices=("implementation", "review"),
                        help="Billable: requires explicit owner authorization")
    args = parser.parse_args()
    codex = shutil.which("codex")
    if not codex:
        raise SystemExit("codex not found")
    version = subprocess.run([codex, "--version"], capture_output=True,
                             text=True, check=True).stdout.strip()
    print(json.dumps({"binary": codex, "version": version,
                      "probes": [probe(role, codex, actor=bool(args.actor_role)) for role in
                                 ((args.actor_role,) if args.actor_role else
                                  ("control", "implementation", "review"))]}, indent=2))
