#!/usr/bin/env python3
"""Offline Git primitive probe. Creates and removes only its temporary repository."""
import json
import os
from pathlib import Path
import subprocess
import tempfile


def probe(root):
    env = dict(os.environ, GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
               GIT_AUTHOR_NAME="Fixture", GIT_AUTHOR_EMAIL="fixture@example.invalid",
               GIT_COMMITTER_NAME="Fixture", GIT_COMMITTER_EMAIL="fixture@example.invalid")

    def git(*args, index=None, data=None, check=True):
        child_env = dict(env)
        if index:
            child_env["GIT_INDEX_FILE"] = str(index)
        return subprocess.run(["git", "-C", str(root), *args], env=child_env,
                              input=data, capture_output=True, check=check)

    git("init", "--quiet")
    for name in ("task", "owner-staged", "owner-unstaged"):
        (root / name).write_text("base\n")
    git("add", "--", "task", "owner-staged", "owner-unstaged")
    git("-c", "core.hooksPath=/dev/null", "commit", "--quiet", "-m", "fixture base")
    parent = git("rev-parse", "HEAD").stdout.strip().decode()
    (root / "owner-staged").write_text("staged owner\n")
    git("add", "--", "owner-staged")
    (root / "owner-staged").write_text("unstaged on staged owner\n")
    (root / "owner-unstaged").write_text("unstaged owner\n")
    (root / "task").write_text("accepted task\n")
    index_path = root / ".git/index"
    before_index = index_path.read_bytes()
    before_files = {name: (root / name).read_bytes()
                    for name in ("task", "owner-staged", "owner-unstaged")}
    temporary_index = root / ".git/task-index"
    git("read-tree", parent, index=temporary_index)
    git("add", "--", "task", index=temporary_index)
    tree = git("write-tree", index=temporary_index).stdout.strip().decode()
    commit = git("commit-tree", tree, "-p", parent,
                 data=b"T-001 disposable intent 1\n").stdout.strip().decode()
    # Pre-update interruption: object exists, but HEAD still proves no publication.
    assert git("rev-parse", "HEAD").stdout.strip().decode() == parent
    intent = {"parent": parent, "tree": tree, "commit": commit}
    (root / ".git/intent.json").write_text(json.dumps(intent))
    git("update-ref", "HEAD", commit, parent)
    # Simulate replacement after publication, before receipt. Reconcile, do not retry.
    recovered = json.loads((root / ".git/intent.json").read_text())
    assert git("rev-parse", "HEAD").stdout.strip().decode() == recovered["commit"]
    assert git("rev-parse", "HEAD^{tree}").stdout.strip().decode() == recovered["tree"]
    assert git("rev-parse", "HEAD^").stdout.strip().decode() == recovered["parent"]
    changed = git("diff-tree", "--no-commit-id", "--name-only", "-r", commit).stdout
    assert changed == b"task\n", changed
    assert index_path.read_bytes() == before_index
    assert all((root / name).read_bytes() == value for name, value in before_files.items())
    # A stale compare-and-swap cannot publish a second commit.
    refused = git("update-ref", "HEAD", parent, parent, check=False)
    assert refused.returncode != 0
    assert git("rev-list", "--count", "HEAD").stdout.strip() == b"2"
    return {"exact_paths": True, "owner_index_bytes_preserved": True,
            "all_worktree_bytes_preserved": True, "pre_publish_head_unchanged": True,
            "post_publish_reconciled": True, "stale_update_ref_refused": True,
            "commit_count": 2,
            "limits": ["No controller integration or real process kill",
                       "No fsync/power-loss proof", "Task-path owner staging must be refused",
                       "Original task index remains at baseline; reconciliation is downstream"]}


if __name__ == "__main__":
    with tempfile.TemporaryDirectory(prefix="t001-git-") as directory:
        print(json.dumps(probe(Path(directory)), indent=2))
