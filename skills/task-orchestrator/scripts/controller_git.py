"""Git observations and immutable closure artifacts for the controller."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
from typing import Any


_state_spec = importlib.util.spec_from_file_location(
    "task_orchestrator_controller_state_for_git",
    Path(__file__).with_name("controller_state.py"),
)
_state_module = importlib.util.module_from_spec(_state_spec)
assert _state_spec.loader is not None
_state_spec.loader.exec_module(_state_module)

_sha256_text = _state_module.sha256_text
_canonical_json = _state_module.canonical_json


def _run_git(repository: Path, *args: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", "-C", str(repository), *args],
        check=True,
        capture_output=True,
    )


def _decode(output: bytes) -> str:
    return output.decode(errors="surrogateescape")


def _atomic_write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(value, errors="surrogateescape")
    temporary.replace(path)


def repository_top_level(repository: Path) -> Path:
    result = _run_git(repository, "rev-parse", "--show-toplevel")
    return Path(_decode(result.stdout).strip()).resolve()


def capture_head(repository: Path) -> str:
    result = _run_git(repository, "rev-parse", "HEAD")
    head_oid = _decode(result.stdout).strip()
    if not head_oid:
        raise ValueError("Repository has no HEAD (unborn repository)")
    return head_oid


def capture_index_tree(repository: Path) -> str:
    return _decode(_run_git(repository, "write-tree").stdout).strip()


def capture_git_status(repository: Path) -> dict[str, str]:
    result = _run_git(
        repository,
        "status",
        "--porcelain=v1",
        "-z",
        "--untracked-files=all",
    )
    entries = _decode(result.stdout).split("\0")
    status: dict[str, str] = {}
    index = 0
    while index < len(entries):
        entry = entries[index]
        if not entry:
            index += 1
            continue
        code = entry[:2]
        paths = [entry[3:]]
        if "R" in code or "C" in code:
            index += 1
            paths.append(entries[index])
        for path in paths:
            worktree_path = repository / path
            if worktree_path.is_symlink():
                content = os.fsencode(worktree_path.readlink())
            elif worktree_path.is_file():
                content = worktree_path.read_bytes()
            else:
                content = b"<missing>"
            status[path] = f"{code}:{hashlib.sha256(content).hexdigest()}"
        index += 1
    return status


def capture_workspace_identity(repository: Path) -> dict[str, str]:
    """Return the exact Git identity used across the inspection boundary."""
    return {
        "head_oid": capture_head(repository),
        "index_tree_oid": capture_index_tree(repository),
        "status_sha256": _sha256_text(_canonical_json(capture_git_status(repository))),
    }


def capture_initial_baseline(repository: Path) -> dict[str, Any]:
    return {
        "head_oid": capture_head(repository),
        "status": capture_git_status(repository),
    }


def capture_task_baseline(repository: Path) -> dict[str, Any]:
    return {
        "head_oid": capture_head(repository),
        "index_tree": capture_index_tree(repository),
        "status": capture_git_status(repository),
    }


def _capture_closure_artifacts(
    repository: Path,
    *,
    head_before: str,
    allowed_paths: list[str],
    baseline_status: dict[str, str],
) -> dict[str, str]:
    staged_name_status = _decode(
        _run_git(repository, "diff", "--cached", "--name-status").stdout
    )
    unstaged_name_status = _decode(
        _run_git(repository, "diff", "--name-status").stdout
    )
    staged_stat = _decode(_run_git(repository, "diff", "--cached", "--stat").stdout)
    unstaged_stat = _decode(_run_git(repository, "diff", "--stat").stdout)
    untracked_paths = sorted(
        path
        for path in _decode(
            _run_git(repository, "ls-files", "--others", "--exclude-standard", "-z").stdout
        ).split("\0")
        if path
    )
    task_patch_paths = [path for path in allowed_paths if path not in baseline_status]
    task_patch = (
        _decode(
            _run_git(
                repository, "diff", "--binary", head_before, "--", *task_patch_paths
            ).stdout
        )
        if task_patch_paths
        else ""
    )
    for untracked_path in sorted(set(untracked_paths) & set(task_patch_paths)):
        untracked_patch = subprocess.run(
            [
                "git", "-C", str(repository), "diff", "--no-index", "--binary",
                "--", os.devnull, untracked_path,
            ],
            capture_output=True,
        )
        if untracked_patch.returncode not in {0, 1}:
            raise ValueError(
                f"Could not capture patch for untracked allowed path {untracked_path}"
            )
        task_patch += _decode(untracked_patch.stdout)
    return {
        "staged_name_status": staged_name_status,
        "unstaged_name_status": unstaged_name_status,
        "staged_stat": staged_stat,
        "unstaged_stat": unstaged_stat,
        "task_patch": task_patch,
    }


def capture_closure_evidence(
    *,
    repository: Path,
    run_dir: Path,
    attempt_id: str,
    task_baseline: dict[str, Any],
    task_baseline_digest: str,
    allowed_paths: list[str],
    policy_sha256: str,
    manifest_sha256: str,
    prompt_sha256: str,
    adapter_state_digest: str,
) -> dict[str, Any]:
    """Capture Git evidence, then publish its immutable text artifacts."""
    current_status = capture_git_status(repository)
    head_before = task_baseline["head_oid"]
    head_after = capture_head(repository)
    untracked_output = _run_git(
        repository, "ls-files", "--others", "--exclude-standard", "-z"
    ).stdout
    untracked_paths = sorted(path for path in _decode(untracked_output).split("\0") if path)
    index_tree = capture_index_tree(repository)
    post_worker_status_sha256 = _sha256_text(_canonical_json(current_status))

    artifact_contents = _capture_closure_artifacts(
        repository,
        head_before=head_before,
        allowed_paths=allowed_paths,
        baseline_status=task_baseline["status"],
    )
    staged_name_status = artifact_contents["staged_name_status"]
    unstaged_name_status = artifact_contents["unstaged_name_status"]
    staged_stat = artifact_contents["staged_stat"]
    unstaged_stat = artifact_contents["unstaged_stat"]
    task_patch = artifact_contents["task_patch"]
    closure_dir = run_dir / "closure"
    artifact_paths = {
        "staged_name_status": closure_dir / f"{attempt_id}.staged.name-status.txt",
        "unstaged_name_status": closure_dir / f"{attempt_id}.unstaged.name-status.txt",
        "staged_stat": closure_dir / f"{attempt_id}.staged.stat.txt",
        "unstaged_stat": closure_dir / f"{attempt_id}.unstaged.stat.txt",
        "task_patch": closure_dir / f"{attempt_id}.diff.patch",
    }
    artifact_digests = {
        name: _sha256_text(content) for name, content in artifact_contents.items()
    }
    for name, content in artifact_contents.items():
        _atomic_write_text(artifact_paths[name], content)

    index_tree_digest = _sha256_text(index_tree)
    head_changed = head_before != head_after
    index_changed = task_baseline["index_tree"] != index_tree

    evidence_record = {
        "policy_sha256": policy_sha256,
        "manifest_sha256": manifest_sha256,
        "baseline_sha256": task_baseline_digest,
        "prompt_sha256": prompt_sha256,
        "head_before": head_before,
        "head_after": head_after,
        "index_tree_before": task_baseline["index_tree"],
        "index_tree_after": index_tree,
        "artifact_digests": artifact_digests,
        "untracked_paths": untracked_paths,
        "adapter_state_digest": adapter_state_digest,
        "post_worker_status_sha256": post_worker_status_sha256,
    }
    evidence_digest = _sha256_text(_canonical_json(evidence_record))
    baseline_status = task_baseline["status"]
    current_paths = set(current_status)
    baseline_paths = set(baseline_status)
    allowed_path_set = set(allowed_paths)
    allowed_changed_paths = sorted(
        path
        for path in current_paths
        if path in allowed_path_set
        and (path not in baseline_status or current_status[path] != baseline_status[path])
    )
    unexpected_paths = sorted(current_paths - baseline_paths - allowed_path_set)
    disappeared_preexisting_paths = sorted(baseline_paths - current_paths)
    modified_preexisting_paths = sorted(
        path
        for path in baseline_paths & current_paths
        if baseline_status[path] != current_status[path]
    )

    closure_fields = {
        "head_before": head_before,
        "head_after": head_after,
        "index_tree": index_tree,
        "index_tree_digest": index_tree_digest,
        "staged_changes": staged_name_status.strip(),
        "staged_digest": artifact_digests["staged_name_status"],
        "unstaged_changes": unstaged_name_status.strip(),
        "unstaged_digest": artifact_digests["unstaged_name_status"],
        "untracked_paths": untracked_paths,
        "task_patch": task_patch,
        "task_patch_digest": artifact_digests["task_patch"],
        "staged_stat_digest": artifact_digests["staged_stat"],
        "unstaged_stat_digest": artifact_digests["unstaged_stat"],
        "evidence_digest": evidence_digest,
        "adapter_state_digest": adapter_state_digest,
        "post_worker_status_sha256": post_worker_status_sha256,
        "evidence_artifacts": {
            name: {
                "path": str(path.relative_to(run_dir)),
                "sha256": artifact_digests[name],
            }
            for name, path in artifact_paths.items()
        },
        "controller_observations": {
            "head_changed": head_changed,
            "index_changed": index_changed,
            "allowed_changed_paths": allowed_changed_paths,
            "unexpected_paths": unexpected_paths,
            "disappeared_preexisting_paths": disappeared_preexisting_paths,
            "modified_preexisting_paths": modified_preexisting_paths,
            "staged_changes": staged_name_status.strip(),
            "staged_digest": artifact_digests["staged_name_status"],
            "unstaged_changes": unstaged_name_status.strip(),
            "unstaged_digest": artifact_digests["unstaged_name_status"],
            "untracked_paths": untracked_paths,
            "index_tree": index_tree,
            "index_tree_digest": index_tree_digest,
        },
    }
    return {
        "current_status": current_status,
        "head_changed": head_changed,
        "index_changed": index_changed,
        "closure_fields": closure_fields,
    }


def validate_accepted_workspace(
    *,
    repository: Path,
    run_dir: Path,
    task_baseline_ref: str,
    task_baseline_digest: str,
    closure_ref: str,
    allowed_paths: list[str],
    expected_identity: dict[str, str],
) -> None:
    """Require the current workspace to match existing accepted closure evidence."""
    attempt_id = expected_identity["attempt_id"]
    attempt_number = attempt_id.removeprefix("attempt-")
    if attempt_id != f"attempt-{attempt_number}" or not attempt_number.isdigit():
        raise ValueError("Accepted attempt identity is invalid")
    if task_baseline_ref != f"task-{attempt_number}.json":
        raise ValueError("Accepted task baseline reference does not match the attempt")
    if closure_ref != f"closure/{attempt_id}.json":
        raise ValueError("Accepted closure reference does not match the attempt")

    baseline_path = run_dir / "baselines" / task_baseline_ref
    closure_path = run_dir / closure_ref
    if not baseline_path.is_file() or not closure_path.is_file():
        raise ValueError("Accepted baseline or closure evidence is missing")
    task_baseline = json.loads(baseline_path.read_text())
    closure = json.loads(closure_path.read_text())
    if set(task_baseline) != {"head_oid", "index_tree", "status"}:
        raise ValueError("Accepted task baseline has an invalid shape")
    if _sha256_text(_canonical_json(task_baseline)) != task_baseline_digest:
        raise ValueError("Accepted task baseline digest mismatch")

    for field in (
        "run_id", "task_id", "attempt_id", "policy_sha256", "manifest_sha256",
        "prompt_sha256",
    ):
        if closure.get(field) != expected_identity[field]:
            raise ValueError(f"Accepted closure {field} mismatch")
    if closure.get("baseline_sha256") != task_baseline_digest:
        raise ValueError("Accepted closure baseline digest mismatch")

    expected_artifact_paths = {
        "staged_name_status": f"closure/{attempt_id}.staged.name-status.txt",
        "unstaged_name_status": f"closure/{attempt_id}.unstaged.name-status.txt",
        "staged_stat": f"closure/{attempt_id}.staged.stat.txt",
        "unstaged_stat": f"closure/{attempt_id}.unstaged.stat.txt",
        "task_patch": f"closure/{attempt_id}.diff.patch",
    }
    evidence_artifacts = closure.get("evidence_artifacts")
    if not isinstance(evidence_artifacts, dict) or set(evidence_artifacts) != set(
        expected_artifact_paths
    ):
        raise ValueError("Accepted closure artifact set mismatch")
    artifact_contents: dict[str, str] = {}
    artifact_digests: dict[str, str] = {}
    for name, expected_path in expected_artifact_paths.items():
        artifact = evidence_artifacts[name]
        if not isinstance(artifact, dict) or set(artifact) != {"path", "sha256"}:
            raise ValueError("Accepted closure artifact identity is invalid")
        if artifact["path"] != expected_path:
            raise ValueError("Accepted closure artifact path mismatch")
        artifact_path = run_dir / expected_path
        if not artifact_path.is_file():
            raise ValueError("Accepted closure artifact is missing")
        content = artifact_path.read_text(errors="surrogateescape")
        digest = _sha256_text(content)
        if digest != artifact["sha256"]:
            raise ValueError("Accepted closure artifact digest mismatch")
        artifact_contents[name] = content
        artifact_digests[name] = digest

    if closure.get("task_patch") != artifact_contents["task_patch"]:
        raise ValueError("Accepted closure task patch mismatch")
    if closure.get("task_patch_digest") != artifact_digests["task_patch"]:
        raise ValueError("Accepted closure task patch digest mismatch")
    for prefix in ("staged", "unstaged"):
        if closure.get(f"{prefix}_changes") != artifact_contents[
            f"{prefix}_name_status"
        ].strip():
            raise ValueError(f"Accepted closure {prefix} changes mismatch")
        if closure.get(f"{prefix}_digest") != artifact_digests[
            f"{prefix}_name_status"
        ]:
            raise ValueError(f"Accepted closure {prefix} digest mismatch")
        if closure.get(f"{prefix}_stat_digest") != artifact_digests[f"{prefix}_stat"]:
            raise ValueError(f"Accepted closure {prefix} stat digest mismatch")

    if closure.get("head_before") != task_baseline["head_oid"]:
        raise ValueError("Accepted closure baseline HEAD mismatch")
    if closure.get("head_after") != task_baseline["head_oid"]:
        raise ValueError("Accepted closure changed HEAD")
    if closure.get("index_tree") != task_baseline["index_tree"]:
        raise ValueError("Accepted closure changed the index")
    if closure.get("index_tree_digest") != _sha256_text(closure["index_tree"]):
        raise ValueError("Accepted closure index digest mismatch")

    evidence_record = {
        "policy_sha256": expected_identity["policy_sha256"],
        "manifest_sha256": expected_identity["manifest_sha256"],
        "baseline_sha256": task_baseline_digest,
        "prompt_sha256": expected_identity["prompt_sha256"],
        "head_before": closure["head_before"],
        "head_after": closure["head_after"],
        "index_tree_before": task_baseline["index_tree"],
        "index_tree_after": closure["index_tree"],
        "artifact_digests": artifact_digests,
        "untracked_paths": closure.get("untracked_paths"),
        "adapter_state_digest": closure.get("adapter_state_digest"),
        "post_worker_status_sha256": closure.get("post_worker_status_sha256"),
    }
    if closure.get("evidence_digest") != _sha256_text(_canonical_json(evidence_record)):
        raise ValueError("Accepted closure evidence digest mismatch")

    observations = closure.get("controller_observations")
    if not isinstance(observations, dict):
        raise ValueError("Accepted closure observations are missing")
    required_empty = (
        "unexpected_paths", "disappeared_preexisting_paths",
        "modified_preexisting_paths", "mechanical_violations",
    )
    if observations.get("head_changed") is not False:
        raise ValueError("Accepted closure records a HEAD change")
    if observations.get("index_changed") is not False:
        raise ValueError("Accepted closure records an index change")
    if any(observations.get(field) != [] for field in required_empty):
        raise ValueError("Accepted closure records repository violations")
    for field in (
        "staged_changes", "staged_digest", "unstaged_changes", "unstaged_digest",
        "index_tree", "index_tree_digest", "untracked_paths",
    ):
        if observations.get(field) != closure.get(field):
            raise ValueError(f"Accepted closure observation {field} mismatch")

    current_head = capture_head(repository)
    current_index = capture_index_tree(repository)
    current_status = capture_git_status(repository)
    if current_head != closure["head_after"]:
        raise ValueError("Repository HEAD changed after acceptance")
    if current_index != closure["index_tree"]:
        raise ValueError("Repository index changed after acceptance")
    baseline_status = task_baseline["status"]
    if any(current_status.get(path) != value for path, value in baseline_status.items()):
        raise ValueError("Pre-existing repository state changed after acceptance")
    if set(current_status) - set(baseline_status) - set(allowed_paths):
        raise ValueError("Unexpected repository path changed after acceptance")

    current_artifacts = _capture_closure_artifacts(
        repository,
        head_before=task_baseline["head_oid"],
        allowed_paths=allowed_paths,
        baseline_status=baseline_status,
    )
    if current_artifacts != artifact_contents:
        raise ValueError("Repository bytes changed after acceptance")
    current_untracked = sorted(
        path
        for path in _decode(
            _run_git(repository, "ls-files", "--others", "--exclude-standard", "-z").stdout
        ).split("\0")
        if path
    )
    if current_untracked != closure.get("untracked_paths"):
        raise ValueError("Repository untracked paths changed after acceptance")

    expected_allowed_changes = sorted(
        path
        for path in current_status
        if path in set(allowed_paths)
        and (path not in baseline_status or current_status[path] != baseline_status[path])
    )
    if observations.get("allowed_changed_paths") != expected_allowed_changes:
        raise ValueError("Accepted closure allowed-path observation mismatch")
