"""Disposable controller test occurrences and explicit run/authority builders.

ControllerFixture owns one repository, external runs and legacy transport setup.
Call initialize_fixture(register_cleanup) once per occurrence; cleanup is registered
before Git setup can fail. Public builders produce fresh policy/request values and
mutate only that occurrence. No assertions or test-case imports belong here;
scenario orchestration and behavioral oracles remain in the owning tests.
Dependencies: Python stdlib, orchestrator runtime loading, checked-in flow examples.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile


CONTROLLER_PATH = Path(__file__).parents[1] / "scripts" / "controller.py"


# Historical transport mechanics have no public launch route in the new policy.
# Exercise them explicitly, preserving Git/timeout/inspection regression oracles.
LEGACY_CONTROLLER = [sys.executable, "-c", (
    "import sys; from pathlib import Path; "
    f"sys.path.insert(0, {str(CONTROLLER_PATH.parent)!r}); "
    "import controller; parser = controller.build_parser(); args = parser.parse_args(); "
    "args.handler = controller._legacy_run_next if args.command == 'run-next' else args.handler; "
    "sys.exit(args.handler(args))"
)]


def load_controller(path=CONTROLLER_PATH):
    spec = importlib.util.spec_from_file_location("task_orchestrator_controller", path)
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise ImportError(f"No loader for {path}")
    spec.loader.exec_module(module)
    return module


def canonical_bytes(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def sha256_bytes(value):
    return hashlib.sha256(value).hexdigest()


def flow_profile(profile="fast-local"):
    path = Path(__file__).parents[1] / "assets" / "examples" / f"{profile}-flow.json"
    return json.loads(path.read_text())


def stage_transport_fixture(run_dir):
    """Seed the transport boundary; this does not prove readiness admission.

    T-002.1 has no ready/preflight admission adapter. Transport/inspection
    regressions start from this explicit fixture, while the pending-stage test
    exercises the real initial boundary without this setup.
    """
    path = run_dir / "ledger.json"
    ledger = json.loads(path.read_text())
    ledger.update(selected_task_id="T1", current_step="implement")
    path.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n")


class ControllerFixture:
    """Per-occurrence state and builders; no inherited test cases or assertions."""

    def initialize_fixture(self, register_cleanup):
        self.temp_dir = tempfile.TemporaryDirectory()
        register_cleanup(self.temp_dir.cleanup)
        self.root = Path(self.temp_dir.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        subprocess.run(["git", "-C", str(self.repo), "config", "user.name", "Test"], check=True)
        subprocess.run(
            ["git", "-C", str(self.repo), "config", "user.email", "test@example.invalid"],
            check=True,
        )
        (self.repo / "allowed.txt").write_text("baseline\n")
        subprocess.run(["git", "-C", str(self.repo), "add", "allowed.txt"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "commit", "-qm", "baseline"], check=True)


    def policy(self, *, commit_mode="off"):
        return {
            "version": 2,
            "execution_authorization": {"transport": "sbx", "yolo": True, "intervention": "active_chat"},
            "run_id": "run-1",
            "repository": str(self.repo),
            "task_ids": ["T1"],
            "verification": {
                "targeted_checks": ["python3 -m unittest test_targeted"],
                "repository_gate": "make verify",
                "authorized_gap": None,
            },
            "permissions": {
                "sandbox": "workspace-write",
                "approval_policy": "never",
                "network": False,
                "dependency_install": False,
                "writable_roots": [str(self.repo)],
                "danger_full_access_authorized": False,
            },
            "commit_policy": {"mode": commit_mode},
            "stop_policy": {
                "on_blocked": "stop",
                "on_failed": "stop",
                "on_needs_input": "escalate",
                "on_unexpected_changes": "stop",
            },
            "flow": flow_profile(),
        }


    def write_fake_codex(
        self, *, write_result=True, created_paths=("new.txt",),
        preflight_ready=None, preflight_release=None,
        worker_ready=None, worker_release=None, mutate_repository=True,
        clean_mutation=False, task_id="T1",
    ):
        """Write a fake codex that emits a thread and a valid result."""
        fake = self.root / "fake-codex"
        preflight_ready_path = str(preflight_ready) if preflight_ready else None
        preflight_release_path = str(preflight_release) if preflight_release else None
        worker_ready_path = str(worker_ready) if worker_ready else None
        worker_release_path = str(worker_release) if worker_release else None
        result_files = ["allowed.txt", *created_paths] if mutate_repository else []
        fake.write_text(
            f"""#!/usr/bin/env python3
import json
from pathlib import Path
import subprocess
import sys
import time

def signal_and_wait(ready_value, release_value):
    if ready_value is None:
        return
    Path(ready_value).write_text("ready\\n")
    deadline = time.monotonic() + 10
    release_path = Path(release_value)
    while not release_path.exists():
        if time.monotonic() >= deadline:
            raise SystemExit("timed out waiting for test release")
        time.sleep(0.01)

args = sys.argv[1:]
log_path = Path({str(self.root / 'argv.json')!r})
log = json.loads(log_path.read_text()) if log_path.exists() else []
log.append(args)
log_path.write_text(json.dumps(log))
if "--help" in args:
    signal_and_wait({preflight_ready_path!r}, {preflight_release_path!r})
    raise SystemExit(0)
signal_and_wait({worker_ready_path!r}, {worker_release_path!r})
if {mutate_repository!r}:
    allowed = Path.cwd() / "allowed.txt"
    if not {clean_mutation!r}:
        allowed.write_text("committed change\\n")
        subprocess.run(["git", "add", "allowed.txt"], check=True)
        subprocess.run(["git", "commit", "-qm", "unauthorized worker commit"], check=True)
        allowed.write_text("staged change\\n")
        subprocess.run(["git", "add", "allowed.txt"], check=True)
    allowed.write_text("worker change\\n")
    created_paths = {created_paths!r}
    for index, path in enumerate(created_paths):
        Path.cwd().joinpath(path).write_text(f"untracked content {{index}}\\n")
print(json.dumps({{"type": "thread.started", "thread_id": "thread-fake-001"}}), flush=True)
if {write_result!r} and "-o" in args:
    result_path = Path(args[args.index("-o") + 1])
    result_path.write_text(json.dumps({{
        "status": "complete",
        "task_id": {task_id!r},
        "summary": "Implemented task {task_id}.",
        "files_changed": {result_files!r},
        "verification": [],
        "decisions": [],
        "questions": [],
        "risks": [],
        "next_action": "Inspect the diff."
    }}))
raise SystemExit(0)
"""
        )
        fake.chmod(0o755)
        return fake


    def create_initialized_run(self, *, flow=None, name="run-flow"):
        controller = load_controller()
        run_dir = self.root / "runs" / name
        policy_path = self.root / f"{name}-policy.json"
        manifest_path = self.root / f"{name}-manifest.json"
        policy = self.policy()
        if flow is not None:
            policy["flow"] = flow
        controller.persist_run_policy(policy_path, policy)
        (self.repo / "tasks").mkdir(exist_ok=True)
        (self.repo / "tasks" / "T1.md").write_text("# T1\n")
        (self.repo / "tasks" / "verification.md").write_text("Source brief: T1.md\n")
        manifest_path.write_text(json.dumps({
            "version": 1,
            "manifest_id": "flow-boundary",
            "completed_task_ids": [],
            "tasks": [{
                "id": "T1",
                "title": "Test task",
                "brief_path": "tasks/T1.md",
                "dependencies": [],
                "allowed_paths": ["allowed.txt"],
                "required_checks": ["python3 -m unittest test_targeted"],
            }],
        }, indent=2, sort_keys=True) + "\n")
        controller.init_run(run_dir, policy_path, manifest_path, self.repo)
        return controller, run_dir


    def read_ledger(self, run_dir):
        return json.loads((run_dir / "ledger.json").read_text())


    def seed_successor(self, run_dir, *, stage=None, readiness=False, **changes):
        """Test-only T-003/004/005 admission; no production outcome is claimed."""
        ledger = self.read_ledger(run_dir)
        if ledger["actor_operations"]:
            ledger["actor_operations"][-1]["state"] = "terminal"
        ledger["active_operation_path"] = None
        if stage:
            ledger["current_step"] = stage
        if readiness:
            operation = ledger["actor_operations"][-1]
            ledger["readiness"] = {field: operation["assignment"][field] for field in
                                   ("task_id", "operation_id", "inputs_sha256", "policy_sha256", "flow_sha256")}
            ledger["readiness"]["status"] = "ready"
        ledger.update(changes)
        ledger["revision"] += 1
        (run_dir / "ledger.json").write_text(json.dumps(ledger))


    def reserve(self, run_dir, stage="preflight", key="first", reason="initial", **overrides):
        request = dict(expected_version=self.read_ledger(run_dir)["revision"], task_id="T1",
                       stage=stage, role={"correction": "implementer", "implement": "implementer",
                       "verify": "verifier", "semantic_review": "review_collector",
                       "acceptance": "acceptance_reviewer", "preflight": "preflight"}[stage],
                       operation_key=key, reason=reason)
        request.update(overrides)
        return load_controller().reserve_operation(run_dir, **request)


    def snapshot(self, run_dir):
        return {str(path): path.read_bytes() for root in (run_dir, self.repo)
                for path in root.rglob("*") if path.is_file() and path.name != "controller.lock"}


    def revision_request(self, run_dir, *, key="owner-revision", **changes):
        ledger = self.read_ledger(run_dir)
        if ledger.get("input_revisions"):
            prior = ledger["input_revisions"][-1]["request"]["payload"]
            payload = json.loads(json.dumps(prior))
        else:
            payload = {"policy": json.loads((run_dir / "run-policy.json").read_text()),
                       "manifest": json.loads((run_dir / "task-manifest.json").read_text()),
                       "documents": {name: item["content"] for name, item in
                                     json.loads((run_dir / "inputs.json").read_text())["documents"].items()}}
        payload["documents"]["brief"] += "\nOwner-approved requirement\n"
        request = dict(expected_version=ledger["revision"], task_id="T1", revision_key=key,
                       payload=payload)
        request.update(changes)
        self.bind_owner(request)
        return request


    def bind_owner(self, request):
        bound = {field: value for field, value in request.items() if field != "authorization"}
        request["authorization"] = dict(kind="owner_response", decision="authorize_input_revision",
                                       owner="task-owner", provenance="active-chat/response-17",
                                       request_sha256=sha256_bytes(canonical_bytes(bound).rstrip(b"\n")))


