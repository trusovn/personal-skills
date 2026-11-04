# Run-evidence lifecycle and recovery

Do not create a task brief, task ID, task package, runtime identity, or other
formal artifact solely for evidence collection. Pass task metadata only when it
already exists. Runtime identity is optional and must come through the shared
runtime-context contract, never model self-identification.

After the compact self-preflight and before the first implementation edit, when
evidence remains available:

- query the current worktree for an active evidence run;
- when taking over an open run whose original invocation never finished,
  recover that run before starting a new one, preserving the recovery boundary
  as uncertain rather than attributing all intervening changes to the prior
  agent;
- begin one new evidence run for this implementer invocation; and
- if any best-effort evidence operation fails in guided mode, apply the
  invocation-local skip in SKILL.md and continue the task.

On normal completion, close the evidence run with outcome `completed`. When
intentionally stopping or handing off before completion, close it with
`reported_interrupted` or `failed` as factually appropriate. A killed agent
may leave the run open; a later invocation may recover it before editing.

When the flow already requires one canonical deterministic architecture command
and an evidence run is active, that command may be executed once through
`run_evidence.py check ... --kind architecture -- <command>` so raw command,
timing, exit status, stdout, and stderr are captured. Do not add a duplicate
architecture execution only for evidence.
