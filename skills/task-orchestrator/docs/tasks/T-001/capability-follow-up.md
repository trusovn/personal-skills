# T-001 capability follow-up

Date: 2026-10-22. Producer evidence; independent review pending.

This supplements [ART-008 v1.0](harness-contract.md) and its
[accepted investigation](reviews/acceptance-01.md). It does not revise the
accepted report, official plan, production code, active installation or run state.
The current user request authorizes focused capability recovery before T-002.
The original verification revision 1 remains the scenario inventory; its old
no-model/no-notification permission envelope does not authorize new live checks.
The explicit owner decisions below supply the additional authority for this work.

## Owner decisions

The owner confirmed these decisions in this conversation:

- Use `gpt-6.1-sol` for all three actor tiers. Keep light/standard/strong reasoning
  at low/medium/high. Up to three minimal model sessions were authorized and used.
- When context occupancy is unknown, require a fresh implementation session for
  correction. Never treat unknown usage as zero. The existing `0.5` rule applies
  only if a reliable occupancy source is available; this work establishes none.
- Use only the active coordinator chat for intervention. Define the detailed
  protocol in this supplement. No external message channel is authorized.
- Two further bounded actor permission sessions were separately authorized and
  used, one per role. Total live sessions in this follow-up: five.

These are owner-approved changes to the earlier model/context/notification
contract. Existing source constants and schemas still describe the old model
mapping. A successor must synchronize the affected policy consumers and focused
tests before using the new mapping. Do not mix the new model with a run that
already froze the old policy. No installation refresh is authorized.

## Local permission evidence — V-03 / R2

Command from repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 skills/task-orchestrator/docs/tasks/T-001/probe_permissions.py
```

Observed binary: `/opt/homebrew/bin/codex`, `codex-cli 0.163.0`.
The enclosing sandbox initially refused nested Seatbelt setup with exit 71 and
`sandbox_apply: Operation not permitted`. The owner approved running the
non-model probes outside that enclosing sandbox. `codex sandbox -P :read-only
-- /usr/bin/true` then exited 0. This is sandbox availability evidence only.

The task-local probe creates disposable directories and invokes the real
`codex sandbox` command with an explicit permission profile. It uses root read
access, implementation workspace write access, explicit read-only `.git` and
`.agents`, and network disabled. It grants no implicit temporary write roots.
Run records, controller and skill fixtures are siblings outside the workspace.
The implementation profile must be selected explicitly by the future adapter;
the existing worker's `--sandbox workspace-write` flags do not select it.

| Boundary | Create / modify / rename / delete | Oracle |
|---|---|---|
| Unsandboxed fixture control | All 32 operations allowed | Establishes writable setup, including symlink targets |
| Implementation task files | All four allowed | Child observations plus independent parent filesystem checks |
| Implementation run/controller/skills, `.git`, `.agents` | All 20 denied | Only EPERM/EACCES count as denial; unchanged bytes and entries checked |
| Implementation symlinks to run and skills | All eight denied | Parent checks the target files and entries |
| Review at all eight paths | All 32 denied | Same operations and independent filesystem checks |

Result: exit 0; all 96 operation observations matched the expected outcomes.
All three fixture variants were removed by `TemporaryDirectory` cleanup.
This proves the selected profile's local-command boundary on this machine.
By itself it does not prove effective actor tool configuration or native patch
enforcement. The separate actor evidence below crosses those two boundaries.
MCP/browser/connector controls, hard-link behavior and integrated launch recovery
remain outside this probe's proof.
No actual controller, skill installation, Git metadata or owner file was a target.

The [official permission documentation](https://learn.chatgpt.com/docs/permissions)
describes path-specific profiles and separates command permissions from MCP,
apps, browser and computer-use controls. The future actor launch must isolate
user/project configuration and disable unused external tool surfaces; shell
denials alone cannot qualify those surfaces.

### Actual actor shell and native patch evidence

```sh
PYTHONDONTWRITEBYTECODE=1 python3 skills/task-orchestrator/docs/tasks/T-001/probe_permissions.py --actor-role implementation
PYTHONDONTWRITEBYTECODE=1 python3 skills/task-orchestrator/docs/tasks/T-001/probe_permissions.py --actor-role review
```

Both sessions used `gpt-6.1-sol`, low effort, approval `never`, ephemeral state,
ignored user configuration/rules, and disabled web search. Unlike the separate
model-only checks, they selected `default_permissions="t001-probe"` with the
explicit filesystem/network profile; they did not pass `--sandbox`, which could
override profile selection. No project configuration existed in the fixtures.

The actor was asked to run the same 32-operation child probe through its actual
shell tool, then use native `apply_patch` in separate calls on a task file and a
protected run file. The parent checked real filesystem contents after exit.

| Role / runtime thread | Shell result | Native patch evidence |
|---|---|---|
| Implementation / `01a1653e-5178-7670-a224-a920ad667776` | 4 task operations allowed, 28 protected/symlink operations denied; command exit 0 | `file_change` event completed for task patch and expected bytes observed; protected patch absent with router rejection in stderr |
| Review / `01a1653e-d93c-77a3-afa7-0ab74e21b5e4` | All 32 operations denied; command exit 0 | Both patch files absent; two runtime router errors explicitly reject writes under the read-only sandbox |

Both parent probes exited 0, and both runtime turns completed. Implementation
usage: input 65135, cached 58240, output 308. Review usage: input 64358, cached
57600, output 312. No reasoning output tokens were reported. Protected patch
rejections do not produce `file_change` events, so stderr plus the parent
filesystem observation supplies that evidence; the actor's final prose does not.
The native patch attempts covered creation, while the shell covered all four
operation types. No claim is made for native patch modify/delete variants.

The current helper prints real events and uses parent filesystem assertions.
Its actor success flag alone does not establish that every requested patch was
attempted; reviewers must inspect the runtime rejection diagnostics as above.
No timeout occurred. A future timeout must be treated as unknown actor liveness,
not permission to rerun blindly.

### Remaining tool-isolation gate

`codex features list` lists apps, browser, computer use, hooks, plugins, image
generation and multi-agent features as enabled in the ordinary local configuration.
This is feature inventory, not the effective tool list for the isolated actors.
`--ignore-user-config` is an `exec` option, not a top-level option for `features
list`; an attempted combined invocation was rejected and supplies no inventory.
Ignoring user configuration does not by itself prove absence of every external
write tool. No MCP/browser/connector calls were made in these sessions.

Before claiming full actor qualification, the selected launch contract must
explicitly disable unused side-effect surfaces (including hooks, plugin/MCP
autoload, apps, browser/computer use and delegation), verify the effective exposed
tool set, and admit only the tested local shell/native-patch path. An unavailable
or non-enforceable disable must fail closed. This is one remaining capability
gate, not a reason to build another transport or weaken the role boundary.
The current worker does not implement this isolated launch contract.

## Model availability evidence — V-01 / V-03

Each check ran sequentially outside the network-restricted enclosing sandbox,
with separate owner approvals for command execution. The actual commands were:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 skills/task-orchestrator/docs/tasks/T-001/probe_model.py low
PYTHONDONTWRITEBYTECODE=1 python3 skills/task-orchestrator/docs/tasks/T-001/probe_model.py medium
PYTHONDONTWRITEBYTECODE=1 python3 skills/task-orchestrator/docs/tasks/T-001/probe_model.py high
```

Setup: temporary working directory, approval `never`, read-only sandbox,
`--ignore-user-config`, `--ignore-rules`, `--ephemeral`, web search disabled,
requested model `gpt-6.1-sol`, and the named effort. Prompt: “Do not use any
tools. Reply with exactly T001_MODEL_OK.” No project files were given or edited.

| Effort | Runtime thread ID | Input / cached / output tokens | Result |
|---|---|---|---|
| low | `01a1653a-6b3a-7cf3-a116-718196f122ce` | 15332 / 9856 / 8 | exit 0, expected message, turn completed |
| medium | `01a1653a-b493-7c32-9365-4572d4d695c4` | 15332 / 9856 / 8 | exit 0, expected message, turn completed |
| high | `01a1653b-2746-7fb2-9c31-781930ff89d9` | 15330 / 0 / 8 | exit 0, expected message, turn completed |

No tool items appeared in any event stream. Reported reasoning output was zero
for all three trivial responses. Successful completion establishes that the CLI
and service accepted each requested setting for this account at this time; it
does not independently attest to backend reasoning or future availability.
The input includes runtime instructions, so a short user prompt did not imply
a tiny input-token count. Ephemeral sessions supply no reusable session record.
Terminal usage is not a context occupancy measurement.

The low check preceded the helper's explicit `stdin=DEVNULL` adjustment. The
prompt and event oracle were unchanged. All three outputs included only the
expected assistant message between runtime start/completion events. Reproduction
uses billable sessions and needs fresh authorization; do not rerun for syntax QA.
See [official non-interactive guidance](https://learn.chatgpt.com/docs/non-interactive-mode)
for configuration isolation and ephemeral execution options.

## Chat-only intervention protocol — V-05 / R3

This is a proposed downstream protocol, not an implemented controller notifier.
It uses the active coordinator session already required by the direction. Python
does not call an undocumented API to inject a message into this chat.

1. Controller persists a blocking intervention before any relay. Record a stable
   intervention ID, run/task and state version, reason, evidence references,
   requested owner decision, and permitted recovery actions. Stop affected work;
   do not release dependencies. Recoverable ordinary checks or corrections do
   not create an intervention.
2. Controller status returns an outstanding intervention as a permitted
   coordinator action. The coordinator presents the ID, concrete problem, bounded
   choices and consequences in the active chat. It asks only for the missing
   authority or decision. No success/progress notifications are sent.
3. A coordinator report that it posted the message is an unconfirmed relay
   claim. Record the attempt and coordinator/session reference; delivery remains
   `unknown`. Console output, a local file or an exit code cannot establish that
   the owner received it. A failed attempt is `failed`; the blocker stays visible.
4. An explicit owner reply that clearly answers this intervention is the chat
   acknowledgement. The coordinator submits its text and intervention identity
   through the proposed controller API. Retain reply provenance available from
   the harness; if no stable message ID is exposed, say so. This is a trusted
   coordinator observation, not a cryptographically verified delivery receipt.
5. Separate acknowledgement from resolution. “Seen” acknowledges receipt but
   grants no permission. Any scope/model/policy change requires an explicit
   decision and a new policy revision at a safe boundary. The controller validates
   the requested recovery action; chat prose cannot waive evidence or writer gates.
6. On coordinator loss, a replacement reads the outstanding intervention and
   presents the same ID. Do not infer delivery or approval from elapsed time,
   silence or an earlier relay claim. Repeated presentation retains attempt
   history; duplicate acknowledgement does not apply a decision twice. A reply
   to a superseded intervention requires reconciliation with the current state.

No timeout may convert unknown delivery into success. With no active coordinator,
automatic notification is unavailable: the durable status remains discoverable
by manual inspection or the next coordinator. There is no background monitoring
or external delivery promise. The owner's choice of this channel defines the
supported operating mode; it is not an end-to-end notifier test.

T-003 owns controller status/relay/acknowledgement records and truthful failures.
T-006 must prove a real intervention and owner acknowledgement in an active
session, plus replacement-coordinator handling. Required deterministic cases:
recoverable failure sends nothing; persisted intervention precedes relay; relay
failure/lost chat stays unknown or failed; acknowledgement does not itself grant
authority; replay cannot resolve twice or release dependencies.

## Coverage and remaining gates

| Scenario | Prior disposition | Current producer evidence / next owner |
|---|---|---|
| V-01 | Transport/parser supported; model availability unverified | Three real model completions above; fresh discovery corroborates |
| V-02 / R1 | Launch service unsupported; recovery gaps | No new recovery claims. T-002 owns reservations; T-003 owns process/receipt qualification |
| V-03 / R2 | Role boundaries and context unverified | Real command-profile and actor shell/native-patch proof; approved unknown-context fresh-session fallback; unused tool-surface isolation remains pending |
| V-04 / R3 | Git primitives supported, integrated finalization unverified | Unchanged accepted evidence. T-005 owns index/layout/crash qualification |
| V-05 / R3 | No selected delivery channel | Owner selected chat; explicit relay/acknowledgement contract above. Runtime integration and delivery proof remain T-003/006 work |
| V-06 | Honest blockers accepted, successor gate retained | This supplement preserves separate evidence levels and successor owners; fresh independent review must decide readiness |

Q-002 now has owner decisions for model and unknown-context behavior. Q-001 has
a tested command permission profile, real actor shell/native-patch evidence and
concrete chat protocol. Unused tool-surface isolation remains pending. No T-002
implementation release is claimed.
The T-002 gate must be reassessed against this supplement by a fresh reviewer;
the original accepted investigation alone does not release it.

No production architecture gate or registry update applies to these task-local
probes and evidence. Broad test suites would not qualify the missing runtime
boundary. Next required route after producer evidence is complete: fresh
independent `task-review-discovery`, then a separate `task-acceptance-review`.
This session cannot accept its own evidence or revise the previous review.

## Continuation checkpoint

- Changed paths: this supplement, `probe_permissions.py`, and `probe_model.py`.
  Existing accepted artifacts, official plans and production files are unchanged.
- Local evidence: 96 offline filesystem observations, 64 actor shell observations,
  one successful native task patch, three native patch rejections, three separate
  model setting completions. These are producer claims, not independent acceptance.
- Remaining capability work: resolve and prove the isolated actor tool inventory
  above. All five authorized live sessions have been used; any further billable
  run needs new authorization. Local non-model interface inspection is still in scope.
- Runtime work still belongs to its planned owners: T-002 reservations, T-003
  launch/recovery and chat records, T-004 evidence/review/correction, T-005 commit
  finalization, and T-006 the full pilot. None was implemented here.
- After capability evidence is complete, first outstanding review owner is fresh
  `task-review-discovery`; then a separate fresh `task-acceptance-review` decides
  readiness. No maintainability or registry stage is imposed on this task-local
  report/probe submission. Do not treat old acceptance as acceptance of these bytes.
