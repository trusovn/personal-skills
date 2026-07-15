# Task Orchestrator: Stage 1 Transport Decision

Status: corrected Codex CLI selected
Date: 2026-07-15

## Decision

Keep the Codex CLI as the first worker transport. Defer an SDK spike.

The locally installed `codex-cli 0.144.4` accepts the required safe global
approval option when it precedes `exec`. The adapter now preflights the exact
start or resume command family before creating turn artifacts, records the
effective command and permission envelope, and fails closed when the safe form is
unsupported. It never substitutes the dangerous bypass flag, and its Stage 1
interface rejects `danger-full-access` because it does not yet consume an
immutable policy record carrying exact authorization.

## Evidence

- `codex --ask-for-approval never exec --help` exits successfully.
- `codex exec --ask-for-approval never --help` exits 2, confirming the original
  failure was flag position rather than absence of a safe mode.
- A strict fake CLI test proves start uses the global approval flag,
  `workspace-write`, and no bypass flag.
- Unsupported preflight fails before the run directory or launch is created.
- Start and resume have separate parse preflights; resume also reapplies the
  recorded sandbox.
- A real local process-group fixture proves a bounded timeout terminates the
  worker and its child, reaps the process, clears the active PID, and records
  `timed_out` as the attempt outcome.
- A live recorded PID rejects resume before preflight or second-process launch.
- Missing or invalid structured results become `missing_result`, never task
  acceptance.

All evidence is local and deterministic. No model request, credential, network,
or new dependency was used.

## Why no SDK spike

Stage 1 found no missing CLI property that justifies dependency or network cost.
The CLI provides the required safe option parsing, thread identity, structured
output path, resume command, and subprocess lifecycle control. The controller,
not an SDK, must still own policy, attempts, inspection, and acceptance.

Reconsider an SDK only if a later local or authorized pilot demonstrates that the
CLI cannot reliably preserve thread identity, cancel/reap the real Codex process,
or return structured output across a supported version change.

## Known boundary

The Stage 1 adapter proves transport behavior with local fakes and parse-only CLI
commands. A real no-network/no-commit worker smoke test remains optional and was
not authorized for this stage. Semantic diff review and queue execution are also
outside the transport decision.

