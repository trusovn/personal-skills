# S3-06 Result: Authorized Verification Command Plan

Status: complete; submitted for immediate acceptance review
Date: 2026-07-21

## Outcome

Added the pure `verification_runner.py` command planner. It builds the ordered
union of selected-task required checks, policy targeted checks, and the
optional repository gate. Each persisted string is parsed with
`shlex.split(posix=True)` and normalized by its exact argv tuple. Equal argv
collapses to the first command position while retaining every source path,
role, and original persisted spelling.

The returned version 1 plan is JSON-compatible and contains stable
`command-NNN` IDs, argv, ordered roles and provenance, repository-gap metadata,
gap-excusability, per-command SHA-256, and a canonical plan SHA-256. Digests use
sorted compact JSON and exclude only the digest field being computed. Plan
construction does not mutate inputs, execute a command, inspect Git, or write
an artifact.

## Rejected command forms

The planner rejects NUL and newline input, malformed quoting, empty argv,
leading `NAME=value`, the `env` launcher, and the explicit shell launchers
`bash`, `csh`, `dash`, `fish`, `ksh`, `sh`, `tcsh`, and `zsh`. It also rejects
standalone control/redirection tokens and `$()` or backtick command
substitution. Quoted ordinary arguments, paths with spaces, wildcards, and
metacharacters embedded in an argv token remain data because execution is
shell-free.

## Version 1 explicit-install table

When `dependency_install` is false, the following top-level executable and
subcommand forms are rejected. Executable matching uses the lower-cased
basename, so an absolute executable path does not bypass the rule.

| Rule | Rejected forms |
|---|---|
| `pip` | versioned/unversioned `pip`: `install`, `download`, `wheel` |
| `easy-install` | any versioned/unversioned `easy_install` invocation |
| `python-module-pip` | versioned/unversioned `python ... -m pip`: `install`, `download`, `wheel` |
| `python-module-ensurepip` | versioned/unversioned `python ... -m ensurepip` |
| `uv` | `add`, `sync`, `pip install`, `pip sync`, `tool install`, `tool upgrade` |
| `poetry` | `add`, `install`, `sync`, `update` |
| `pipenv` | `install`, `sync`, `update` |
| `npm` | `add`, `ci`, `i`, `install`, `update`, `upgrade`, `exec` |
| `npx` | any invocation |
| `pnpm` | `add`, `dlx`, `i`, `install`, `up`, `update` |
| `pnpx` | any invocation |
| `yarn` | `add`, `dlx`, `install`, `up`, `upgrade` |
| `bun` | `add`, `install`, `update`, `upgrade`, `x` |
| `bunx` | any invocation |
| `conda-family` | `conda`, `mamba`, or `micromamba`: `create`, `install`, `update`, `upgrade` |
| `gem` | `install`, `update` |
| `bundler` | `bundle` or `bundler`: `install`, `update` |
| `cargo` | `add`, `install` |
| `go` | `get`, `install` |
| `dotnet` | `restore`; `tool install`, `tool restore`, `tool update` |
| `dotnet-add-package` | `dotnet add ... package ...` |
| `composer` | `install`, `require`, `update` |
| `brew` | `bundle`, `install`, `reinstall`, `upgrade` |
| `apt` | `apt` or `apt-get`: `install`, `reinstall` |
| `dnf-yum` | `dnf` or `yum`: `install`, `reinstall`, `upgrade` |
| `apk` | `add`, `upgrade` |
| `pacman` | `-S`, `-U` (matched case-insensitively) |
| `zypper` | `in`, `install`, `update` |
| `winget` | `install`, `upgrade` |
| `choco` | `install`, `upgrade` |
| `scoop` | `install`, `update` |

Every rejection exposes the exact matched rule. This table is deliberately a
closed top-level argv preflight, not semantic proof that arbitrary test code
has no installation side effect. S3-01 filesystem/network sandboxing and
S3-08 Git-drift detection remain independent controls. With
`dependency_install: true`, the table is bypassed but no sandbox or network
authority changes.

## Gap semantics

A non-null authorized gap without a repository gate is rejected. Gap metadata
is copied only onto the normalized command that carries the `repository_gate`
role. If deduplication gives that command a `task_required` or
`policy_targeted` role too, `gap_excusable` is false, so targeted failure wins.

## Verification

- Fail-first: the explicit `/bin/sh -c ...` test failed because no `ValueError`
  was raised, proving the new assertion detected the missing launcher denial.
- After implementation, that same single test passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_verification_runner.py`
  passed 19 tests, including the pre-existing S3-01 capability proof.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py'`
  passed 124 tests.

The localhost-dependent checks were run with the required host permission;
the first ordinary sandbox attempt correctly failed at loopback bind rather
than being misreported as behavioral evidence.

## Residual risk and boundary

The explicit-install rules do not observe transitive child behavior, aliases
with unrecognized executable names, or arbitrary scripts that install as a
side effect. This is the accepted version 1 limitation, bounded independently
by S3-01 and later drift inspection. S3-07 still owns subprocess execution,
sandbox invocation, immutable logs/results, timeout handling, and cleanup.
