#!/usr/bin/env python3
"""One owner-authorized minimal model check. No project files or tools needed."""
import argparse
import json
import shutil
import subprocess
import tempfile


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("effort", choices=("low", "medium", "high"))
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="t001-model-") as directory:
        command = [shutil.which("codex") or "codex", "--ask-for-approval", "never",
                   "exec", "--ignore-user-config", "--ignore-rules", "--ephemeral",
                   "--skip-git-repo-check", "-C", directory, "--sandbox", "read-only",
                   "--model", "gpt-6.1-sol", "-c", f'model_reasoning_effort="{args.effort}"',
                   "-c", 'web_search="disabled"', "--json",
                   "Do not use any tools. Reply with exactly T001_MODEL_OK."]
        result = subprocess.run(command, stdin=subprocess.DEVNULL,
                                capture_output=True, text=True, timeout=60)
        events = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
        messages = [event["item"].get("text") for event in events
                    if event.get("type") == "item.completed"
                    and event.get("item", {}).get("type") == "agent_message"]
        completed = any(event.get("type") == "turn.completed" for event in events)
        tool_items = [event for event in events if event.get("type") == "item.started"
                      and event.get("item", {}).get("type") != "agent_message"]
        passed = result.returncode == 0 and completed and messages == ["T001_MODEL_OK"] and not tool_items
        print(json.dumps({"model_requested": "gpt-6.1-sol", "effort_requested": args.effort,
                          "exit_code": result.returncode, "passed": passed,
                          "events": events, "stderr": result.stderr}, indent=2))
        raise SystemExit(0 if passed else 1)
