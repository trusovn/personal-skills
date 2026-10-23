# T-001 — Tool-isolation capability evidence

Date: 2026-10-22. Producer evidence; independent discovery and acceptance pending.
Companion to [capability-follow-up.md](capability-follow-up.md), not a revision
of ART-008, its acceptance, the plan, production code or an active installation.

**T-002 remains blocked.** The selected CLI still exposes delegation tools under
the tested disable configuration. No claim of complete actor isolation is made.
No additional billable model session was run.

## Scope and verification

Initial `git status --short` contained only the three untracked continuation
files: `capability-follow-up.md`, `probe_model.py`, `probe_permissions.py`.
Those files were preserved. This continuation adds this report and
[probe_tool_inventory.py](probe_tool_inventory.py). It implements no T-002 work.

Existing permission fixtures exercise shell/native patch operations, not tool
assembly. No existing local Responses fixture was found in the task's coverage.
The new standard-library fixture observes the real CLI request and executes a
read-only inventory expression through the real code-mode router. It replaces
only the model service. It does not introduce a production transport or select
another backend for the harness.

Reproduce from repository root, with loopback bind permission:

```sh
python3 -B skills/task-orchestrator/docs/tasks/T-001/probe_tool_inventory.py
```

The enclosing sandbox rejected the loopback bind with EPERM. After explicit
command approval, the saved probe ran outside that sandbox. Observed binary:
`/opt/homebrew/bin/codex`, version previously observed here as `codex-cli 0.163.0`.
Result: **probe exit 1**, CLI exit 0, two captured requests, inventory observed,
`delegation_exposed=true`, `isolation_gate_passed=false`.
Runtime thread: `01a1654a-6dee-7d30-beba-6aaf8816ebbc` (local fixture, not a real
model availability check). A successful CLI turn does not pass isolation.

Setup: disposable empty workspace and CODEX_HOME, no account credentials passed,
ignored user config and rules, ephemeral state, read-only sandbox, approval never,
web search disabled, requested model `gpt-6.1-sol`. The local fake Responses
endpoint returns a single inventory call, then a completed turn. Reported zero
usage comes from that fixture, not OpenAI billing telemetry. The loopback server
is shut down and joined; the CLI subprocess completes before temporary cleanup.

Explicitly disabled feature keys:

```text
apps browser_use browser_use_external browser_use_full_cdp_access
computer_use hooks plugins remote_plugin plugin_sharing image_generation
multi_agent multi_agent_v2 multi_agent_v2_dynamic_tools code_mode tool_suggest
skill_mcp_dependency_install in_app_browser in_app_local_automation
realtime_conversation memories goals
```

## Observations and limits

Both captured request inventories contained:

| Namespace | Exposed tools |
|---|---|
| functions | exec, wait, request_user_input, request_user_input_async |
| clock | sleep |
| collaboration | followup_task, interrupt_agent, list_agents, send_message, spawn_agent, wait_agent |

The synthetic service returned `functions.exec` with
`text(ALL_TOOLS.map(x=>x.name));`. The real router executed it and returned:

```text
apply_patch, clock__curr_time, exec_command, list_mcp_resource_templates,
list_mcp_resources, read_mcp_resource, view_image, write_stdin
```

The response's next captured request carried that actual tool output. The fixture
never called delegation, connectors, browser/computer use, MCP actions or hooks.
It never spawned a child agent. The `collaboration` exposure alone contradicts
the required unavailable-delegation inventory, regardless of whether an eventual
call would succeed. Prompt instructions prohibiting delegation are not enforcement.

An earlier exploratory variant also disabled `code_mode_host`. It emitted
“Code Mode is unavailable because code-mode host is disabled” and removed the
needed shell/patch wrapper. That is not a usable qualification. The saved probe
leaves that required host enabled and rejects an empty/unobserved inventory.

Request tools are encoded as `input` items of type `additional_tools`, not just
in a top-level `tools` array. The initial top-level-only inspection was corrected
before drawing conclusions. Neither `tools=null` nor absence of JSONL tool-call
events proves unavailable tools. Deferred tools require the nested inventory too.

The tested empty fixture has no connector/browser/plugin action tools in its
observed inventories. This is not proof for inherited user, managed, project or
plugin configuration. Hooks are not necessarily model-visible tools; no hostile
hook/MCP/plugin sentinel was configured and exercised here. Root-read access and
HOME-based skill discovery also remain: a disposable CODEX_HOME alone does not
remove the user's global skill catalog. No live OpenAI-provider parity, alternate
role/profile or configuration-autoload isolation was qualified by this fixture.
The earlier filesystem evidence cannot fill these gaps.

The [official configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)
documents `features.multi_agent` as the collaboration switch, connector controls
separate from command-network restrictions, and per-server MCP enablement.
The [hooks guide](https://learn.chatgpt.com/docs/hooks) documents disabling hooks
with `features.hooks=false`. These documented controls guide investigation; the
observed inventory overrides any assumption that flags already qualified this
installed runtime. Namespace exclusions documented for nested code-mode exposure
are not evidence of disabling direct collaboration tools.

## Coverage and next owners

| Row | Current evidence | Remaining gate / owner |
|---|---|---|
| V-01 | Real CLI request assembly and inventory router exercised with local service | No live provider compatibility claim; capability owner |
| V-02 / R1 | No launch/recovery changes or new claims | Existing T-002/003 ownership retained |
| V-03 / R2 | Explicit disable configuration still exposes delegation; empty fixture's nested inventory observed | Capability owner must establish a supported enforceable control and qualify inherited tool/hook configuration; unknowns stay blocked |
| V-04 / R3 | No changes | Existing T-005 ownership retained |
| V-05 / R3 | No changes to approved chat protocol | Existing T-003/006 ownership retained |
| V-06 | Isolation failure and evidence levels recorded; T-002 remains blocked | Fresh independent discovery, then separate acceptance decision; no release from producer evidence |

Smallest next capability action: identify a supported runtime control or corrected
runtime build that removes delegation while retaining the tested local execution
path. Do not patch production orchestration, disable its safeguards, or substitute
a backend to mask the failure. Any runtime replacement or further billable
qualification requires a concrete owner-authorized scope. After a viable control
is found, test inherited MCP/plugin/connector and hook startup with disposable
sentinels and both effective actor profiles, then obtain independent review.

The user requested fresh independent discovery and separate acceptance. Additional
billable review sessions have been requested separately; pending authorization is
not acceptance and does not permit a live actor qualification run. The discovery
must consume this report, the follow-up, all three prior probes, verification
revision 1, preflight decision context and acceptance-01. A separate acceptance
session must assess readiness for T-002 explicitly. Neither review may infer a
passed isolation gate from a successfully completed local fixture turn.

No broad suite was run: it cannot remove an exposed delegation surface. The
required next evidence is at the runtime tool/configuration boundary.
