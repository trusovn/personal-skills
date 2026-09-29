# Bounded implementation run evidence

`scripts/run_evidence.py` captures factual begin/finish boundaries around one
`bounded-task-implementer` invocation. It is optional sidecar infrastructure for
ordinary guided work; it does not make task packages, task IDs, runtime identity,
or evidence collection mandatory.

## Storage and snapshots

Evidence is stored under the current worktree's Git directory, resolved with
Git, at:

```text
<absolute-git-dir>/personal-skills/run-evidence/
```

Nothing is written into the worktree and no `.gitignore` change is required.
One open run is preferred per Git worktree.

Each repository boundary records `HEAD`, branch, dirty state, and an immutable
Git tree identity. The tree is built with a temporary `GIT_INDEX_FILE`: `HEAD`
is read into the temporary index, the current tracked worktree plus non-ignored
untracked files are added there, and `git write-tree` creates the snapshot. The
real index and worktree are not changed. A Git-local ref retains each snapshot
object so later worktree edits do not invalidate the recorded identity.

The collector does not generate patches, file-level deltas, additions/deletions,
or change statistics. Recovery after a missing explicit finish records the
later takeover state; it must not be interpreted as proof that every intervening
repository change came from the original run.

## Installation resolution and availability

Resolve run-evidence tooling from the same installation root as the active
`bounded-task-implementer`. For repository work, a matching project-local skill
under `.agents/skills/` takes precedence over user-global skill installations;
its shared tooling is the sibling `.agents/scripts/` directory. Once that
project-local skill is selected, do not fall back to or probe a user-global copy
for the same invocation.

In this source repository, the equivalent installation root is the repository
itself: `skills/` and `scripts/` are siblings. Do not mix a skill from one
installation root with helper scripts from another.

Before starting the lifecycle, verify that the resolved scripts directory
contains all of:

- `run_evidence.py`;
- `workflow_version.py`;
- `runtime_context.py`; and
- `runtime-context.schema.v1.json`.

Then run the cheap, non-run-starting probe:

```bash
python3 <resolved-scripts>/run_evidence.py --repo <worktree> availability
```

A successful probe returns JSON with `available: true`. The probe verifies the
shared dependency set, workflow discovery from that installation, and the
ability to create and remove a tiny probe file under the Git-metadata evidence
storage location. It does not create a run, active marker, snapshot, or worktree
change.

Unavailable probes return `available: false` with a reason such as
`missing_shared_dependencies`, `workflow_unavailable`, or
`git_metadata_unwritable`. In ordinary guided use, treat that as an
invocation-local best-effort skip: continue the bounded task and do not retry
evidence operations during that invocation. If a repository/user/machine
contract explicitly requires evidence, unavailability remains a blocking
instrumentation failure.

## Lifecycle

After a successful availability probe, from the target repository:

```bash
python3 <resolved-scripts>/run_evidence.py active
python3 <resolved-scripts>/run_evidence.py begin
python3 <resolved-scripts>/run_evidence.py finish <run-id> --outcome completed
python3 <resolved-scripts>/run_evidence.py finish <run-id> --outcome reported_interrupted
python3 <resolved-scripts>/run_evidence.py recover <run-id>
```

`begin` refuses to overwrite an existing open run. `active` exposes that run.
Use `recover` only when the prior invocation did not record an explicit finish
and the current invocation/operator is taking over the worktree.

Task association is optional:

```bash
python3 <resolved-scripts>/run_evidence.py begin \
  --task-id API-31 \
  --task-brief docs/tasks/API-31/brief.md
```

A trusted runtime-context JSON file may be supplied with
`--runtime-context <file>`. When it is omitted or missing, the existing generic
runtime-context helper supplies the normalized `identity_source: unavailable`
representation.

## Deterministic checks

A deterministic command can be executed through the collector so the exact
invocation facts are retained without interpreting them:

```bash
python3 <resolved-scripts>/run_evidence.py check <run-id> --kind architecture -- <command> <args...>
```

The manifest records the command, start timestamp, duration, exit code, raw
stdout, and raw stderr. The wrapper replays stdout/stderr and returns the
command's exit status, so a canonical architecture gate can be run once through
this wrapper rather than duplicated for evidence collection.

## Shared dependencies and manual copies

`run_evidence.py` consumes, rather than reimplements:

- `scripts/workflow_version.py` for the `bounded-task-implementer` fingerprint;
- `scripts/runtime_context.py` for runtime identity; and
- `scripts/runtime-context.schema.v1.json`, required by the runtime-context
  helper.

For a project-local installation, place the selected skill under
`.agents/skills/` and these shared files under `.agents/scripts/`, following
the root README's single installation/integration convention. Copy the shared
set together rather than installing only `.agents/skills/` when run evidence is
wanted.

If run-evidence tooling is absent or unavailable, an ordinary standalone
`bounded-task-implementer` remains usable; only an explicit
repository/user/machine contract may make instrumentation mandatory.
