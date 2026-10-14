# T-002 — original-context archive

State: ARCHIVE_RECOVERABLE.

Owner snapshot commit: `0ad1706cecc6f7d115e510762bf74c58d732cb6a`. Fixed tag:
`archive/documentation-pre-cleanup-2026-10-14`. Destination: `https://github.com/trusovn/personal-skills.git`.
Owner committed T-001; this invocation made no branch commit. Local and remote
tag absence were checked before creating the tag; no existing tag was moved.

Commands, from the original repository unless stated:

```sh
git ls-remote --tags origin refs/tags/archive/documentation-pre-cleanup-2026-10-14
git tag archive/documentation-pre-cleanup-2026-10-14 HEAD
git push origin refs/tags/archive/documentation-pre-cleanup-2026-10-14:refs/tags/archive/documentation-pre-cleanup-2026-10-14
git init -q /tmp/documentation-cleanup-recovery-a3qlq044
git -C /tmp/documentation-cleanup-recovery-a3qlq044 fetch --no-tags https://github.com/trusovn/personal-skills.git refs/tags/archive/documentation-pre-cleanup-2026-10-14:refs/tags/archive/documentation-pre-cleanup-2026-10-14
git -C /tmp/documentation-cleanup-recovery-a3qlq044 checkout -q --detach archive/documentation-pre-cleanup-2026-10-14
```

Publication succeeded. Fresh retrieval has no original-clone alternates. Its
peeled commit equals the recorded SHA; all 524 paths, Git blob IDs,
file bytes/SHA-256, lengths and modes match preservation-manifest.json. This
includes all 182 retirement candidates, original reviews, repository context,
and the final T-001 results/discovery/acceptance outputs. Missing-ref recovery
was rejected with no fallback. No LFS, submodule or external object is required.

The first manifest probe incorrectly restricted regular blobs to mode 100644
and failed on executable scripts. The tag was published before that local probe
was repaired. No original was changed or retired. Reinspection captured all 13
100755 scripts outside the deletion set and proved every path against committed
and freshly recovered content. The earlier audit's all-100644 context summary
is a historical limitation; its candidate modes and all stable bytes agree.

Local network sandbox denied DNS initially; the approved network execution
path was used for remote lookup, publication and fresh retrieval.
Generated installations, caches, Finder metadata and the unrelated handoff
remain excluded under Q-001. Unavailable raw historical records remain missing;
archive success does not supply historical behavioral qualification.

Next: retain the 13 live executable inputs, rebind their consumers, then retire
the owner-approved candidates only after local dependency checks pass.
