# High-assurance and machine contracts

The high-assurance input and freshness sections apply only when the entry
profile selector activates high assurance. The machine-output section also
applies to a conversational JSON-artifact request without changing its profile.

## High-assurance inputs

Require:

- one fresh preflight packet with status `ready`;
- its referenced packaged `brief.md` and run policy; a packet that references a
  direct legacy brief routes to `task-brief-designer` for normalization and
  then fresh `task-preflight`;
- its referenced verification-design artifact when the packet records one;
- the supplied worker-result schema and durable result path; and
- for correction, the acceptance findings and prior checkpoint/result.

Missing or inconsistent high-assurance inputs return the schema-valid
non-complete result required by the caller. Do not downgrade silently to guided
mode.

## High-assurance additions

Before editing, require the packet at the task package's `preflight.md` and
recalculate every packet freshness field exactly: brief bytes,
verification-design bytes when present, `HEAD`, the recorded post-packet short
status, separate
index/worktree identities for dirty paths, dependency/instruction/policy
digests, and task-specific environment fingerprints. Any unexplained mismatch
routes to fresh `task-preflight`.

The packet's own creation is the one expected baseline delta: its recorded
post-write status must equal current status before implementation, and all
non-packet paths and identities must still match the pre-write baseline. Do not
require the canonical packet to be ignored or status-neutral.

Treat the packet as the discovery and permission boundary:

- inspect and change only declared paths and cited context;
- map every recorded verification scenario to planned implementation evidence
  before editing, preserving blocked or unchecked coverage explicitly;
- establish the packet's highest-risk fail-first evidence;
- run its exact commands in order and record every attempted or required-but-
  skipped command truthfully;
- save logs and results only at authorized runtime paths; and
- validate the result against the supplied schema.

### Machine-contracted invocation

When the caller explicitly supplies an output schema or requires a machine-only
response, return exactly one schema-conforming JSON object and no prose. When a
conversational caller asks for a JSON artifact at a path, write and validate the
artifact, then return the human summary with a link to it.

Keep the JSON `summary` useful to a human: describe the implemented outcome and
evidence. Do not prefix it with the skill name, timestamp, packet path, or other
transport metadata unless the supplied schema explicitly requires that text.

For the existing worker-result schema:

- `status`: `complete`, `needs_input`, `blocked`, or `failed`; `complete` is a
  submission, not acceptance. Keep `complete` for successful immediate-review
  submissions; do not add `READY_FOR_REVIEW` or invent a machine field.
- `files_changed`: task-owned repository-relative paths only.
- `verification`: every run or required-but-unrun command with exact outcome.
- `decisions`: local reversible task choices only.
- `questions`: unresolved input/authority issues and whether they block.
- `risks`: residual gaps or skipped stronger evidence.
- `next_action`: one exact route. For immediate review, route to the first
  outstanding applicable conditional stage and the complete ordered remainder
  through fresh independent `task-review-discovery` evidence to the separate
  fresh `task-acceptance-review` decision.

For machine results, preserve measurement/rationale, transfer references and
native obligations in existing summary, verification, risks and next-action
fields or an authorized linked artifact. Never extend a strict result schema.
