"""Git observations and immutable closure artifacts for the controller."""

from __future__ import annotations

import hashlib
import importlib.util
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
        path = entry[3:]
        worktree_path = repository / path
        if worktree_path.is_symlink():
            content = os.fsencode(worktree_path.readlink())
        elif worktree_path.is_file():
            content = worktree_path.read_bytes()
        else:
            content = b"<missing>"
        status[path] = f"{code}:{hashlib.sha256(content).hexdigest()}"
        if "R" in code or "C" in code:
            index += 1
        index += 1
    return status


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
    staged_name_status = _decode(
        _run_git(repository, "diff", "--cached", "--name-status").stdout
    )
    unstaged_name_status = _decode(
        _run_git(repository, "diff", "--name-status").stdout
    )
    staged_stat = _decode(_run_git(repository, "diff", "--cached", "--stat").stdout)
    unstaged_stat = _decode(_run_git(repository, "diff", "--stat").stdout)
    untracked_output = _run_git(
        repository, "ls-files", "--others", "--exclude-standard", "-z"
    ).stdout
    untracked_paths = sorted(path for path in _decode(untracked_output).split("\0") if path)
    task_patch_paths = [
        path for path in allowed_paths if path not in task_baseline["status"]
    ]
    if task_patch_paths:
        task_patch = _decode(
            _run_git(
                repository,
                "diff",
                "--binary",
                head_before,
                "--",
                *task_patch_paths,
            ).stdout
        )
    else:
        task_patch = ""
    for untracked_path in sorted(set(untracked_paths) & set(task_patch_paths)):
        untracked_patch = subprocess.run(
            [
                "git",
                "-C",
                str(repository),
                "diff",
                "--no-index",
                "--binary",
                "--",
                os.devnull,
                untracked_path,
            ],
            capture_output=True,
        )
        if untracked_patch.returncode not in {0, 1}:
            raise ValueError(
                f"Could not capture patch for untracked allowed path {untracked_path}"
            )
        task_patch += _decode(untracked_patch.stdout)
    index_tree = capture_index_tree(repository)

    artifact_contents = {
        "staged_name_status": staged_name_status,
        "unstaged_name_status": unstaged_name_status,
        "staged_stat": staged_stat,
        "unstaged_stat": unstaged_stat,
        "task_patch": task_patch,
    }
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
    mechanical_violations = []
    if head_changed:
        mechanical_violations.append("worker changed HEAD despite commit prohibition")
    if index_changed:
        mechanical_violations.append("worker changed the Git index")

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
            "mechanical_violations": mechanical_violations,
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
        "mechanical_violations": mechanical_violations,
        "closure_fields": closure_fields,
    }
