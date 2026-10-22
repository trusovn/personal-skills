# Task Review Discovery Report: T-001 — Local runtime support

| Field | Value |
|---|---|
| Producing stage | task-review-discovery, project-local installation |
| Coverage completeness | complete for the investigation contract; runtime qualification remains blocked |
| Discovery iteration | 2 — continuation of discovery-01, fresh independent session |
| Created at | 2026-10-22T18:13:45.933763+00:00 |
| Repository root | /Users/mtrusov/work/skill-sources/personal-skills |
| Durable report | skills/task-orchestrator/docs/tasks/T-001/reviews/discovery-02.md |
| Preparation | brief.md; verification.md revision 1; preflight.md including Decision context |
| Submission | harness-contract.md v1.0, READY_FOR_REVIEW; probe_local.py; runtime qualification BLOCKED |

This report supplies evidence only. It gives no acceptance verdict, approved
deferral or advancement. It applies to the bytes below and does not review or
authenticate itself.

## 1. Discovery provenance

This session authored none of the reviewed implementation, evidence fixture or
preparation bytes. Its only repository write is this new report. Evidence below
is independently gathered. Loading the skill did not supply independence.

HEAD: `8efffca9e38855e8229764851d570a72aa7a857b`. The implementation delta consists of the untracked
`harness-contract.md` and `probe_local.py`. The owner brief, preparation
documents and previous review are separate existing artifacts. Tracked
production code and tests are reference evidence, unchanged from HEAD.

The prior report did not record individual worktree digests. Its passing labels
therefore do not establish current identity. This pass corroborated current
bytes and closed its unavailable-CLI row on Darwin arm64 with the selected
binary. Previous Linux observations are historical, not current-host evidence.

## 2. Findings

No findings.

ART-008 consistently distinguishes observed fixture behavior, source,
documentation and proposed interfaces. It does not claim real runtime
permission enforcement, exactly-once launch, context measurement, finalization
or notification delivery. Those limitations are permitted investigation outcomes
under AC-05 and remain downstream blockers.

## 3. Completeness ledger

These rows were reconstructed from the brief, verification revision 1 and prior
continuation before behavioral checks. All required material rows have current
evidence. A pass here assesses the investigation's evidence and honest
disposition, not qualification of a capability marked unverified.

| Row ID | AC / invariant | Explicit cases and setup / oracle | Submitted evidence | Independent probe / current evidence | Result / reason |
|---|---|---|---|---|---|
| V-01 | AC-01 | Python subprocess vs interactive tools; one selection; exact installed version; CLI help is parser evidence only | E1/E2/E6, selection section | C1–C4: /opt/homebrew/bin/codex, codex-cli 0.163.0; exec/resume/sandbox/app-server help all exit 0. Source lists internal start/resume and public controller init/run-next/inspect/revise-flow. Interactive tools have no supplied Python API. | pass; prior CLI environment blocker closed |
| V-02 / R1 | AC-02; one active operation | First launch; repeated operation; live, terminal, unknown; missing receipt; replacement coordinator. Real wrapper subprocess/files with fake runtime; source distinguishes existing from proposed operations. | E3/E4; proposed envelope and case table | C5–C7, A1: first result persisted; real first turn followed by resume reaches turn 2 on same fake thread; live PID refuses new invocation; missing thread/result stays stopped. Starting-before-Popen and PID-after-Popen trace confirms missing-receipt window. | pass; duplicate service/real launch recovery explicitly unsupported |
| V-03 / R2 | AC-03; enforced roles and frozen policy | Allowed implementation write; denied review/run/controller/skill writes; unknown usage; exact model/effort and 0.5 threshold. Oracle for enforcement must be effective runtime boundary. | E1/E2/E6; policy source; all denial proof marked missing | C1–C4/C9 and source: help exposes options only; no runtime write probe is offered as evidence. Draft202012Validator and runtime validator accept actual default and reject threshold 0.6, unapproved strong model and boolean correction limit. Mapping is gpt-5.6-sol at low/medium/high, threshold 0.5. No occupancy source in inspected scripts. | pass for report/policy facts; actual actor permissions and usage remain unverified |
| V-04 / R3 | AC-04; no false commit success | Accepted path plus unrelated staged, unstaged and mixed owner changes; before publication, after publication before receipt; stale CAS; unavailable/unknown finalization. Disposable Git object/ref and byte oracles. | E5 | C8: exact task-only tree; owner index and worktree bytes unchanged; HEAD unchanged before publication; replacement reads persisted intent and matches commit/tree/parent; stale expected-parent update refused; exactly two commits including base. Source/report clearly exclude integrated crashes and accepted-path staging overlap. | pass at primitive boundary only |
| V-05 / R3 | AC-04; honest delivery | Delivered, failed, unknown/unavailable; no real message authorized. Oracle is channel acknowledgement, not invocation. | E7/docs, proposed notifier | C10 source search finds no notifier; D3 confirms notify is a JSON-payload command hook, not acknowledged controller delivery. Proposed envelope returns delivered/failed/unknown and preserves status/manual action; no delivery state releases dependencies. | pass; unsupported current controller and unverified real delivery are explicit |
| V-06 | AC-05 | Supported/unsupported/unverified; Q-001/Q-002; T-002..006 impacts. Report-to-authority trace. | dispositions, consumer handoff, submission ledger | All capabilities above mapped. Q-001 partially resolved to conditional CLI bridge, Q-002 unresolved; no policy change or successor implementation release. T-002 request contract, T-003 lifecycle/permissions/notifier, T-004 review/context, T-005 commit, T-006 authorized full pilot remain separately owned. | pass |
| R1-trace | R1 | Duplicate same key and spawn-without-receipt; actor IDs cannot establish provenance | recovery case table | Source at codex_worker.py:244–254, 349–353, 415–439: state-path refusal is not atomic idempotency; PID record follows spawn. Adapter receipt must bind observed process/thread and controller assignment outside actor writes. Unknown blocks relaunch. | pass |
| R2-level | R2 | Actual selected permission boundary vs fake argv/configuration | explicit evidence-level labels | No allow/deny execution claimed. Separate verification_runner Seatbelt policy is expressly excluded from actor qualification. Same effective policy/all enabled write tools and protected-root layout are named missing proof. | pass |
| R3-assume | R3 | Commit interruption before/after; unavailable commit; delivery failure visibility | E5 plus limitations | C8 and source/report trace: primitive intent simulation does not claim real crash/fsync proof; task-path index remains baseline, reconciliation pending; unknown commit blocks release, failure/unknown notification visible. | pass |

## 4. Adversarial state and evidence checks

- Repeated occurrence: C6 executes an actual wrapper start and then resume in
  its persisted state; argv and turn/thread observations prove the second
  occurrence. This qualifies fake-runtime wrapper behavior only.
- Cleanup: A1 instruments the existing sleeping fixture to record its process
  group before waiting. Existing SIGTERM test synchronizes on recorded running
  state, thread and child PID. Timeout remains bounded at 0.2 seconds. In both
  cases, descendant PID and process group became absent within bounded polling,
  and captured pipes reached EOF. Observed groups 33649/33653 and children
  33650/33654 were absent. No fixture process was left.
- Policy type/boundary checks: C9 used the declared Draft 2020-12 validator,
  valid default input and three deliberate invalid inputs. No schema-text-only
  inference was used. C11 separately exercised worker schema and real
  result_status on valid result and invalid status, collection type and summary.
- Owner state separation: C8 covers unrelated staged and unstaged content,
  including unstaged edits on an already staged owner file. Accepted-path owner
  staging, additions/deletions/renames/modes and real crash recovery are explicitly
  unqualified, not silently included.
- No authentication claim: mutable receipts/digests are not presented as an
  independent authenticity anchor. Duplicate/unknown handling is proposed;
  unsupported cardinality and spawn windows remain visible.

## 5. Commands, observations and cleanup

All shell commands ran from the repository root with local Python/Git and
Darwin arm64. No live actor, model request, notification, project commit,
server start or permission expansion occurred.

| ID | Exact command / reproducible probe | Observed result / boundary | Side effects / cleanup |
|---|---|---|---|
| C1 | `command -v codex; codex --version; uname -sm` | /opt/homebrew/bin/codex; codex-cli 0.163.0; Darwin arm64 | none; PATH-alias permission warning, command still exits 0 |
| C2 | `codex exec --help` | exit 0, schema/JSONL/model/config/sandbox/output options | no actor started |
| C3 | `codex --ask-for-approval never exec resume --json --output-schema skills/task-orchestrator/assets/worker-result.schema.json -o /tmp/t001-unused-result.json -c 'sandbox_mode="read-only"' --help` | exit 0, exact resume parser shape | help only; no result produced |
| C4 | `codex sandbox --help; codex app-server --help` | both exit 0; direct sandbox command/profile/state JSON; app server stdio/schema generation | neither service nor sandbox write probe started |
| C5 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_codex_worker.py -k test_start_persists_thread_and_structured_result` | 1 test OK, 0.449s | disposable existing fixture; no bytecode |
| C6 | `PYTHONDONTWRITEBYTECODE=1 python3 -`, A1 below | 6 selected tests OK, 2.269s; bounded process/pipe cleanup | disposable fixtures removed |
| C7 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_codex_worker.py` | 15 tests OK, 4.250s, after clean targeted checks | existing disposable fixtures; no bytecode |
| C8 | `PYTHONDONTWRITEBYTECODE=1 python3 skills/task-orchestrator/docs/tasks/T-001/probe_local.py` | exit 0; all six preservation/reconciliation flags true; commit_count 2 | TemporaryDirectory removes Git repository |
| C9 | `PYTHONDONTWRITEBYTECODE=1 python3 -`, A2 below | default accepted; .6 threshold, model change, boolean limit rejected by schema and runtime | memory only |
| C10 | `rg -n 'notify\|notifier\|notify_intervention\|occupancy\|context_window\|token_usage\|input_tokens' skills/task-orchestrator/scripts` | no matches; read controller_git.py and worker spawn/resume/termination paths | source evidence only |
| C11 | `PYTHONDONTWRITEBYTECODE=1 python3 -`, A3 below | valid complete result accepted; invalid status, string files_changed, boolean summary rejected by schema and worker | disposable result removed |
| C12 | `git rev-parse HEAD; git diff --stat; git diff --cached --stat; git ls-files --stage skills/task-orchestrator/docs/tasks`; SHA-256 snapshot below | HEAD matches; both tracked diffs empty; task paths have no index entries; authority hashes match preparation | read only |

Documentation was fetched on 2026-10-22 through web open/find, not a runtime
smoke test:
D1 [Non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode)
corroborates JSONL thread events, final schema output, resume and terminal usage;
it does not establish a context occupancy denominator.
D2 [Agent approvals and security](https://learn.chatgpt.com/docs/agent-approvals-security)
describes macOS Seatbelt; its platform-subcommand example differs from installed
help, as ART-008 states.
D3 [Configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)
defines notify as a command receiving JSON, without qualifying this controller's
delivery acknowledgement.

## 6. Aggregate-gate record

| Field | Value |
|---|---|
| Gate / exact command | ART-008 documentary reconciliation; shell aggregate command: not run |
| Status | passed evidence reconciliation |
| Owner / stage | this independent continuation discovery session, after targeted evidence |
| Reason | Frozen V-01..V-06/R1..R3 ledger reconciled against all ACs, brief finite risks and scoped files; no failed/unchecked investigation row or remaining selected probe. Verification design specifies report reconciliation, not a full-repository suite. |
| Current evidence | C1–C12, D1–D3, source traces and current identities; C7 is the existing owning transport module, not an invented broad gate |

The prior reconciliation did not close its CLI blocker. This pass owns current
reconciliation after re-observing those CLI boundaries. No old gate is copied
as current proof, and no downstream capability proof is waived.

## 7. Scope and baseline comparison

HEAD unchanged from investigation/preflight and discovery-01. No tracked staged
or unstaged changes exist. All six pre-existing package paths are untracked and
have no index blobs. Implementation ownership is limited to harness-contract.md
and probe_local.py; brief/preparation/prior review are preserved.

Discovery-01 also listed three .DS_Store entries on its host. They are absent
from this session's status. This is historical environment drift outside the
task, not an attributed task change.

Exact pre-write `git status --short`:

```text
?? skills/task-orchestrator/docs/tasks/
```

Exact pre-write `git status --short --untracked-files=all`:

```text
?? skills/task-orchestrator/docs/tasks/T-001/brief.md
?? skills/task-orchestrator/docs/tasks/T-001/harness-contract.md
?? skills/task-orchestrator/docs/tasks/T-001/preflight.md
?? skills/task-orchestrator/docs/tasks/T-001/probe_local.py
?? skills/task-orchestrator/docs/tasks/T-001/reviews/discovery-01.md
?? skills/task-orchestrator/docs/tasks/T-001/verification.md
```

Index file SHA-256: `cdbb187a67e8e4cea3c0e7290c462aabb9828e36c69cfc0c3abbcc38039d4f79`.
Current worktree SHA-256 identities:

| Path | SHA-256 |
|---|---|
| skills/task-orchestrator/docs/tasks/T-001/brief.md | 3eaa6df3972c254764c1b92992a52dfdbc832f637abb8c89826ea56a994462c2 |
| skills/task-orchestrator/docs/tasks/T-001/harness-contract.md | 3187faae4080b072e76b3304a872f5d2913468e2484d23569494d607a79f51ab |
| skills/task-orchestrator/docs/tasks/T-001/preflight.md | 99fbd591aee2b9dc7610c110d216376c44137ce4223b85ff9706569e86ab2e1e |
| skills/task-orchestrator/docs/tasks/T-001/probe_local.py | aef89b60af9fc6fee8938006d4c48fa7402d1d5bee9f8eaaf214dd69d53c4a27 |
| skills/task-orchestrator/docs/tasks/T-001/reviews/discovery-01.md | 2d18cf671a6054a0b2ff221379d6eac885fd65b1184cee67b0fd5df0ae46b869 |
| skills/task-orchestrator/docs/tasks/T-001/verification.md | 1c7091c9651a85323a5b8acbe7ca3409eee15e307769ab5b53997fa7ff5ef483 |
| skills/task-orchestrator/docs/local-harness-orchestration-plan.md | 98fab11ed34846bbe7c0596ea293be5908b763573ac8b0b988f3f4f5441452fd |
| skills/task-orchestrator/docs/local-harness-task-map.json | 7e6a0a379c360c373934cfa88ee03dcdf32175aae4cc8ac1286cb7a73f9ad440 |
| skills/task-orchestrator/docs/direction-local-harness.md | 0d17e2787866e1f4872705d6df2ec18e6289e15b97c42cf5e94b6196b3e17f2e |
| skills/task-orchestrator/docs/project-plan-review.md | 9bc7cfeab8f956c7607cd1b915ed8c24613196b68e7b476474809d396ec4c8f0 |
| skills/task-orchestrator/scripts/codex_worker.py | 001a2f5fbf78a0532d342f71e9f8467f1d35073f0133868503d6bb15e70f3ba2 |
| skills/task-orchestrator/scripts/controller_state.py | b3ebc6c5244982b33cacf563b70d46c01336c4a476e46940d75ee595dca2bb02 |
| skills/task-orchestrator/scripts/controller_git.py | 49f8685c5a33850250f70587f111d84fba40c33412e9ad11c1590ab13a42c905 |
| skills/task-orchestrator/assets/flow-profile.schema.json | 6c3c0f3e1c3ab05203a02b4c57adcaa81a6cf83ce0a73e3725b76ebc28f621d5 |
| skills/task-orchestrator/assets/worker-result.schema.json | 32effc1988202bb7b16280169c4914b7300d6632d22ac805827b517675fec9ac |
| skills/task-orchestrator/tests/test_codex_worker.py | 30dabec6e379918c4f20bd00778997628c7363a16aecccbcc725606a50b7fdcd |

Post-write status is recorded after publication below. This report is outside
its own reviewed byte set.

## 8. Questions and residual capability risks

No blocked or unchecked investigation row remains. Unverified capability
dispositions remain requirements for their named downstream owners:

| Surface | Missing proof / next owner | Effect |
|---|---|---|
| Effective permissions | Capability owner: same-policy allowed task write and denied review/run/controller/skill writes across enabled tools | affected runtime implementation blocked |
| Launch/recovery | T-002/003: reservation, process-start identity, missing receipt and unhandled crash windows | no duplicate launch or unknown-liveness release permitted |
| Model/context | Capability owner: exact frozen-model sessions and reliable occupancy source; owner alone decides a policy change | Q-002 unresolved; correction reuse blocked |
| Git finalization | T-005: integrated durable intent/receipt, exact index reconciliation, overlap/layout/crash cases | no dependency release based on primitive support |
| Notification | Owner selects/authorizes channel/test; T-003 connects it, T-006 proves intervention branch | real delivery remains unverified |
| Full flow | T-006, separately authorized model-driven correction/review/commit pilot | harness remains unqualified |

No additional permission or live test is requested by this discovery pass.

## 9. Coverage and next route

Discovery coverage is complete for this proof-only task. The prior missing CLI
observations are now independently corroborated. Give the separate
task-acceptance-review call this report, brief.md, the scoped untracked
harness-contract.md/probe_local.py bytes, verification.md revision 1,
preflight.md including Decision context, discovery-01.md, and all reviewer
commands/probes below. That call owns the decision; this report advances nothing.

## 10. Discovery continuation

- Iteration / current byte identity: 2; HEAD 8efffca9e38855e8229764851d570a72aa7a857b; scoped SHA-256 values in §7.
- Coverage rows: V-01 pass (was CLI-blocked, now local re-observation); V-02/R1 pass; V-03/R2 pass for evidence/disposition; V-04/R3 pass at Git primitive boundary; V-05/R3 pass for honest unsupported disposition; V-06 pass; R1-trace pass; R2-level pass; R3-assume pass.
- Finding IDs: none in either discovery pass.
- Finding/scenario continuity: prior passes are navigation only; current C1–C12/D1–D3 evidence belongs to this reviewer. Implementation E1–E7 remains producer-attributed. No correction owner needed for a confirmed finding; unresolved capability owners and influenced sibling surfaces are preserved in §8. Authority owner remains the user; acceptance owner is the separate decision call.
- Preparation/context: brief SHA-256 3eaa6df3972c254764c1b92992a52dfdbc832f637abb8c89826ea56a994462c2; verification revision 1; ready preflight and its Decision context; ART-008 v1.0.
- Reviewer regressions: existing test_codex_worker.py focused C5 and full C7, probe_local.py C8; in-report A1–A3 reproduce additional current evidence. No repository test file added.
- Aggregate gate: current documentary reconciliation passed; shell aggregate not run; owned by this independent continuation reviewer after clean targeted checks.
- Next: separate task-acceptance-review decision call with the exact packet and reviewed bytes named in §9.

## Appendix: reproducible reviewer probes

Run each Python block with `PYTHONDONTWRITEBYTECODE=1 python3 -` from the repository root.
No source or test file must be edited.

### A1 — Selected lifecycle probes

The executed probe imported the existing test class, selected the six methods
below, and wrapped its sleeping-fixture factory to record os.getpgrp() just
before signal.pause(). It also bounded run_worker at eight seconds. The
equivalent reproduction below preserves those inputs, assertions and cleanup
oracle. The original tests retain their observable running-state/child-PID
synchronization and pipe communication.

```python
import importlib.util, os, subprocess, sys, time, unittest
s = importlib.util.spec_from_file_location(
    "wt", "skills/task-orchestrator/tests/test_codex_worker.py")
m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
class Reviewed(m.CodexWorkerTest):
    def write_sleeping_fake_codex(self):
        p = super().write_sleeping_fake_codex()
        text = p.read_text().replace("import json\n", "import json\nimport os\n", 1)
        text = text.replace("signal.pause()\n",
            "Path(" + repr(str(self.root/"group.pid")) +
            ").write_text(str(os.getpgrp()))\nsignal.pause()\n")
        p.write_text(text)
        return p
    def run_worker(self, *args):
        return subprocess.run([sys.executable, str(m.SCRIPT), *args],
            text=True, capture_output=True, timeout=8)
    def tearDown(self):
        try:
            for name, kill in [("group.pid", os.killpg), ("child.pid", os.kill)]:
                p = self.root/name
                if not p.exists(): continue
                pid = int(p.read_text()); deadline = time.monotonic()+3
                while True:
                    try: kill(pid, 0)
                    except ProcessLookupError: break
                    if time.monotonic() >= deadline:
                        self.fail(f"surviving {name}: {pid}")
                    time.sleep(.01)
        finally: super().tearDown()
names = [
 "test_resume_reuses_saved_thread_instead_of_starting_over",
 "test_resume_rejects_live_recorded_process_without_starting_another",
 "test_failure_before_thread_start_is_not_resumable",
 "test_zero_exit_without_result_is_missing_result_not_success",
 "test_timeout_terminates_process_group_and_records_terminal_state",
 "test_signal_interruption_terminates_process_group_and_records_terminal_state"]
r = unittest.TextTestRunner(verbosity=2).run(
    unittest.TestSuite(Reviewed(n) for n in names))
raise SystemExit(not r.wasSuccessful())
```

### A2 — Frozen policy validator

```python
import copy, importlib.util, json
from pathlib import Path
from jsonschema import Draft202012Validator
root = Path("skills/task-orchestrator")
s = importlib.util.spec_from_file_location("state", root/"scripts/controller_state.py")
m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
schema = json.loads((root/"assets/flow-profile.schema.json").read_text())
Draft202012Validator.check_schema(schema)
v = Draft202012Validator(schema); base = m._default_reviewed_flow()
v.validate(base); m.validate_flow_profile(base)
for path, value in [
 (["implementation_session_reuse_threshold"], .6),
 (["actor_levels", "strong", "model"], "unapproved-model"),
 (["correction", "limit"], True)]:
    bad = copy.deepcopy(base); obj = bad
    for key in path[:-1]: obj = obj[key]
    obj[path[-1]] = value
    assert list(v.iter_errors(bad))
    try: m.validate_flow_profile(bad)
    except ValueError: pass
    else: raise AssertionError(path)
print("valid accepted; three invalid policy inputs rejected")
```

### A3 — Result schema and worker boundary

```python
import copy, importlib.util, json, tempfile
from pathlib import Path
from jsonschema import Draft202012Validator
root = Path("skills/task-orchestrator")
s = importlib.util.spec_from_file_location("worker", root/"scripts/codex_worker.py")
m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
schema = json.loads((root/"assets/worker-result.schema.json").read_text())
v = Draft202012Validator(schema); v.check_schema(schema)
valid = dict(status="complete", task_id="T1", summary="done",
 files_changed=["task"], verification=[], decisions=[], questions=[],
 risks=[], next_action="inspect")
with tempfile.TemporaryDirectory(prefix="t001-schema-") as tmp:
    p = Path(tmp)/"result.json"; p.write_text(json.dumps(valid))
    v.validate(valid); assert m.result_status(p) == "complete"
    for field, value in [
        ("status", "invalid"), ("files_changed", "task"), ("summary", True)]:
        bad = copy.deepcopy(valid); bad[field] = value
        assert list(v.iter_errors(bad)); p.write_text(json.dumps(bad))
        assert m.result_status(p) is None
print("valid accepted; three invalid result inputs rejected")
```

## Post-write scope check

Observed after creating this report: `git status --short` remains exactly
`?? skills/task-orchestrator/docs/tasks/`. Expanded status is:

```text
?? skills/task-orchestrator/docs/tasks/T-001/brief.md
?? skills/task-orchestrator/docs/tasks/T-001/harness-contract.md
?? skills/task-orchestrator/docs/tasks/T-001/preflight.md
?? skills/task-orchestrator/docs/tasks/T-001/probe_local.py
?? skills/task-orchestrator/docs/tasks/T-001/reviews/discovery-01.md
?? skills/task-orchestrator/docs/tasks/T-001/reviews/discovery-02.md
?? skills/task-orchestrator/docs/tasks/T-001/verification.md
```

Compared with the pre-write expanded status, only discovery-02.md was added.
All six pre-existing package file hashes, HEAD and the index-file hash matched
the recorded baseline. This observation covers repository scope preservation;
it does not authenticate this report.

