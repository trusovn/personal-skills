# Task Orchestrator: Verification Sandbox Decision

Status: adopted and locally proven for pathname-scoped writes
Date: 2026-07-16

## Decision

Use macOS `/usr/bin/sandbox-exec` with a generated version 1 Seatbelt profile as
the Stage 3 verification-command boundary. Invoke it directly with argv and
`shell=False`; do not pass verification commands through a shell.

The adopted contract is pathname-scoped. The profile denies writes whose
accessed path is outside every configured writable root; it does not provide
inode-level isolation when an in-root hard link aliases an out-of-root file.
The operator accepts responsibility for using repositories and writable roots
that contain no such cross-boundary hard-link aliases. The runner does not scan
for or manage this repository-hygiene precondition.

This decision is supported only on macOS hosts where the exact executable is
present and a local capability preflight can apply the required profile. The
proof passed on macOS 26.5.2 (build 25F84). `sandbox-exec` is deprecated and its
profile language is a private platform interface, so absence or changed
behavior on another host or OS release is an unsupported configuration that
must stop verification before the command starts. Do not substitute an
unrestricted subprocess.

The production executor remains S3-07 work. S3-01 adds only the reproducible
capability fixture in `tests/test_verification_runner.py`.

## Exact invocation

The selected shape is:

```text
/usr/bin/sandbox-exec \
  [-D WRITABLE_ROOT_0=<canonical-root> ...] \
  -p <generated-profile> \
  <verification-executable> <argument> ...
```

The command is an argv sequence. Profile parameters carry canonical writable
roots without interpolating them into Seatbelt source. The verification
executable and arguments follow the profile options and are never reparsed by a
shell. Descendant processes inherit the applied sandbox.

All profiles begin with:

```scheme
(version 1)
(allow default)
```

The generated restrictions below then remove authority not present in the
persisted permission envelope.

## Version 1 permission mapping

| Policy value | Runner representation | Fail-closed rule |
|---|---|---|
| `sandbox: read-only` | Add `(deny file-write*)`. Reads and ordinary process execution remain available. | A configured writable root does not override the write denial. |
| `sandbox: workspace-write` | Add one parameter per canonical writable root and deny `file-write*` when the accessed path is outside every root. An empty root list adds `(deny file-write*)`. | Each root must already be an absolute directory and is canonicalized with `realpath`; `/` and invalid roots are rejected before launch. The operator supplies roots without cross-boundary hard-link aliases. |
| `sandbox: danger-full-access` | Add no filesystem write denial. Network policy remains independent. | Reject before launch unless `danger_full_access_authorized` is exactly `true`. Exercise only against an isolated temporary path. |
| `approval_policy: never` | The non-interactive runner performs no approval exchange. | Reject any other or missing value before launch. |
| `network: false` | Add `(deny network*)`. | Failure to construct or apply this rule stops verification. |
| `network: true` | Add no network denial. | The proof uses only a local loopback listener; it does not contact an external endpoint. |
| `writable_roots` | Supply canonical roots through `-D WRITABLE_ROOT_<n>=...` and reference them with `(param ...)` plus `subpath` filters. Duplicate canonical roots collapse to one rule. | Missing, relative, nonexistent, non-directory, or filesystem-root values are rejected for enforcement. |
| `danger_full_access_authorized: false` | Valid for `read-only` and `workspace-write`; supplies no extra authority. | Reject a `danger-full-access` request before command execution. |
| `danger_full_access_authorized: true` | Enables only the separately selected `danger-full-access` mode. | It does not enable network or alter other sandbox modes. |
| `dependency_install: false` | Retain the same filesystem and network restrictions. | The sandbox is not semantic proof that an executable or argument is not an installer; S3-06 must reject install commands and arguments during command-plan preflight. |
| `dependency_install: true` | Retain the selected filesystem and network restrictions; installation still cannot exceed them. | This value does not grant shell syntax, unpersisted environment changes, or extra write/network authority. |

Unknown sandbox modes, incomplete permission objects, non-boolean flags, an
empty command argv, a non-macOS platform, or a substituted/missing executable
are rejected before subprocess launch.

## Local capability proof

The deterministic fixture first establishes that each denial probe could have
produced its side effect on this host:

- an unrestricted parent write creates and reads a file in the future denied
  directory;
- an unrestricted child connects to a parent-owned `127.0.0.1` listener and
  transfers a fixed payload.

It then proves the selected pathname and network boundary:

| Case | Expected and observed result |
|---|---|
| Ordinary command under `workspace-write` | `/usr/bin/true` exits zero. |
| In-root writes | A command creates one file in each of two configured roots. |
| Ordinary command under `read-only` | `/usr/bin/true` exits zero. |
| Write under `read-only` | The command exits nonzero and creates no file in an otherwise host-writable configured root. |
| Out-of-root write under `workspace-write` | The command exits nonzero and creates no file in the control-proven writable directory. |
| `network: true` | The sandboxed child reaches the local listener and transfers the fixed payload. |
| `network: false` | The same child cannot reach the same kind of local listener. |
| Authorized `danger-full-access` | The command writes to an isolated out-of-root control path. |
| Unauthorized `danger-full-access` | Invocation construction raises before launch and no marker appears. |
| Unsupported platform, mode, incomplete envelope, or invalid root | Invocation construction raises before launch. |

These negative assertions would fail if `_run` were replaced by an unrestricted
subprocess: both denied files would appear and the denied loopback connection
would succeed. The controls also prevent a host limitation from being mistaken
for sandbox enforcement.

The fixture uses bounded subprocess and socket timeouts rather than sleeps. A
temporary directory owns all proof files and removes them on exit; sockets and
accepted connections use context-managed cleanup. The test makes no model call,
external network request, dependency installation, production verification
call, or repository mutation outside its temporary fixture.

## Known limitation and chosen responsibility

A separate counterexample established that the profile's pathname rule cannot
provide inode isolation for a pre-existing hard link crossing the writable-root
boundary. A prelaunch hard-link scan would add complexity without closing the
race, so this design intentionally adds no scan or warning mechanism.

Stronger isolation—such as running the entire agent and verifier in a private
container or microVM workspace—would be useful defense-in-depth. It is deferred
and is not a responsibility of this skill or the Stage 3 executor.

For the current operator-controlled workflow, the operator owns repository
hygiene and confirms that configured writable roots contain no hard links whose
mutation would affect files outside those roots. Under that explicit
precondition, adopt the locally proven pathname-scoped mechanism and allow
S3-07 to proceed.

The filesystem/network boundary is necessary but not sufficient for controller
verification. S3-06 still owns command parsing, executable/argument preflight,
deduplication, and dependency-install semantics; S3-07 owns immutable execution
records, sequential execution, timeout handling, and cleanup.
