#!/usr/bin/env python3
"""Capture real CLI tool assembly with a local fake provider; no billable model.

Requires loopback bind permission. This is evidence of the local request/router
boundary only, not live OpenAI compatibility, hook isolation or actor qualification.
"""
import http.server
import json
import os
import shutil
import subprocess
import tempfile
import threading
from pathlib import Path


DISABLED = (
    "apps", "browser_use", "browser_use_external", "browser_use_full_cdp_access",
    "computer_use", "hooks", "plugins", "remote_plugin", "plugin_sharing",
    "image_generation", "multi_agent", "multi_agent_v2", "multi_agent_v2_dynamic_tools",
    "code_mode", "tool_suggest", "skill_mcp_dependency_install", "in_app_browser",
    "in_app_local_automation", "realtime_conversation", "memories", "goals",
)


def main():
    with tempfile.TemporaryDirectory(prefix="t001-tools-") as temporary:
        root = Path(temporary).resolve()
        for name in ("home", "workspace"):
            (root / name).mkdir()
        requests = []

        class Handler(http.server.BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_POST(self):
                requests.append(json.loads(self.rfile.read(int(self.headers["Content-Length"]))))
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream")
                self.end_headers()
                response = {"id": "resp_fixture", "object": "response",
                            "status": "completed", "output": [],
                            "usage": {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}}
                events = [{"type": "response.created", "response": dict(response, status="in_progress")}]
                if len(requests) == 1:
                    call = {"type": "custom_tool_call", "id": "fc_fixture",
                            "call_id": "call_fixture", "name": "exec", "namespace": "functions",
                            "input": "text(ALL_TOOLS.map(x=>x.name));"}
                    events.append({"type": "response.output_item.done", "output_index": 0, "item": call})
                    response["output"] = [call]
                events.append({"type": "response.completed", "response": response})
                for event in events:
                    self.wfile.write(("data: " + json.dumps(event) + "\n\n").encode())

        server = http.server.HTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever)
        thread.start()
        command = [shutil.which("codex") or "codex", "--ask-for-approval", "never", "exec",
                   "--ignore-user-config", "--ignore-rules", "--ephemeral", "--skip-git-repo-check",
                   "-C", str(root / "workspace"), "--model", "gpt-6.1-sol", "--sandbox", "read-only",
                   "-c", 'model_provider="fixture"', "-c",
                   'model_providers.fixture={name="fixture",base_url="http://127.0.0.1:'
                   + str(server.server_port) + '/v1",wire_api="responses",requires_openai_auth=false}',
                   "-c", 'web_search="disabled"', "--json", "Do not use tools."]
        for flag in DISABLED:
            command.extend(("--disable", flag))
        # Never pass account credentials or an inherited provider/host selection.
        environment = {key: value for key, value in os.environ.items()
                       if not any(part in key for part in ("TOKEN", "SECRET", "API_KEY", "CODEX", "OPENAI"))}
        environment["CODEX_HOME"] = str(root / "home")
        environment["NO_PROXY"] = "127.0.0.1,localhost"
        try:
            result = subprocess.run(command, env=environment, stdin=subprocess.DEVNULL,
                                    capture_output=True, text=True, timeout=30)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)
        assert not thread.is_alive(), "fixture server survived shutdown"
        inventories = []
        outputs = []
        for request in requests:
            inventories.append([
                {"namespace": tool.get("name"), "tools": [nested.get("name") for nested in tool.get("tools", [])]}
                for item in request.get("input", []) if item.get("type") == "additional_tools"
                for tool in item["tools"]])
            outputs.extend(item for item in request.get("input", [])
                           if item.get("type") == "custom_tool_call_output")
        # An empty inventory or an unexecuted fixture call cannot qualify isolation.
        observed = result.returncode == 0 and len(requests) == 2 and bool(outputs)
        delegation = any(entry["namespace"] == "collaboration"
                         for inventory in inventories for entry in inventory)
        report = {"binary": command[0], "disabled_features": DISABLED,
                  "request_count": len(requests), "inventory_observed": observed,
                  "delegation_exposed": delegation, "isolation_gate_passed": observed and not delegation,
                  "inventories": inventories, "nested_inventory_outputs": outputs,
                  "exit_code": result.returncode, "stdout": result.stdout, "stderr": result.stderr}
        print(json.dumps(report, indent=2))
        return 0 if report["isolation_gate_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
