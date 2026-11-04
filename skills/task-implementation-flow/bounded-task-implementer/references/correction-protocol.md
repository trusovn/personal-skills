# Correction, resume and handoff

Resume incomplete work under the existing profile and entry/freshness gates.
Preserve the original baseline and prior evidence; the entry file's submission
route determines affected-stage re-entry.

On a same-thread `CHANGES_REQUESTED` correction, preserve the bounded partial
diff and apply only in-scope findings. Changed contract, scope, helpers,
dependencies, permissions, or authority route through the owning earlier stage.

## Correct at the invariant level

For each reviewer finding, state the broken invariant before editing. Enumerate
only credible sibling cases already implied by that invariant, the task
contract, or an explicit finite matrix. Preserve the reviewer regression and
make the smallest correction that protects the invariant instead of adding a
field-specific, input-specific, or interleaving-specific exception. When
several explicit values share one oracle, prefer a local table-driven or
parameterized test over a reusable test framework.

When a prior review supplies a coverage ledger, consume it completely and
preserve every row identity and status. Prior passes are navigation context,
not acceptance evidence for corrected bytes; leave unchecked and blocked rows
for the fresh reviewer.

Before any correction edit, write a concise row-to-evidence map for the complete
supplied ledger. Include every row identity exactly once with its prior status,
planned implementation evidence or navigation use, and next owner. Map failed
rows to reviewer regressions and planned correction evidence; map unchecked or
blocked rows to explicit fresh-review coverage; keep prior passes as navigation
context only. This is a pre-edit gate: do not modify production or test bytes
until the map is complete, and do not silently omit rows that implementation
will not exercise.

The correction handoff must carry:

- the authoritative brief reference and preceding verdict;
- the applicable verification revision and preflight/context references;
- the first outstanding applicable conditional stage and the complete remaining
  route;
- the complete coverage ledger and complete findings;
- stable finding/scenario IDs, incomplete reasons and separate correction,
  evidence/capability and authority owners, including influenced sibling surfaces;
- attempts, exact results and discarded hypotheses when correction has stopped;
- the current scoped diff and reviewer reproducer commands;
- correction evidence attached to the failed rows, separately from reviewer
  row status;
- the broad-gate decision and owner; and
- every remaining unchecked or blocked row.

Run reviewer regressions first and the nearest owning suite after they pass.
Determine broad-gate ownership from the authority before editing. When it
assigns a final reviewer, leave that reviewer's aggregate decision untouched.
Run a broader or aggregate gate during correction only when the authority or
blast radius assigns it to implementation, or when no final reviewer is
assigned to own it. Report it only as implementation evidence. Never replace
implementation checks with an acceptance pass.

### Correction handoff format

For guided correction work, use this explicit final structure. Preserve the
labels and fill every field from the supplied review state; do not replace an
exact authority path or command with prose such as “the task” or “the reviewer
regression passed.”

```markdown
<Explain the correction's practical result, current evidence limits, and next actor in plain language.>

Implemented: READY_FOR_REVIEW

- Authority: <exact authoritative brief path>
- Preflight/context reference: <exact readiness, verification revision and context paths>
- Preceding verdict: <verdict>
- Finding/scenario IDs: <complete stable inventories>
- Complete findings and invariant: <findings and broken invariant>
- Influenced sibling surfaces: <contract-implied cases and current evidence or remaining owner>
- Attempts and discarded hypotheses: <exact probes/results and retained partial diff, or none>
- Current scoped diff: <changed paths and concise diff summary>
- Measurement: <original JSON/text, current fresh comparison JSON/text, coverage/status and gaps; retained prior comparisons; affected-function relationships and required rationale>
- Native evidence: <command, governed scope/policy, checked-byte identity, result, producer/stage; reused aggregate constituent coverage or owed duty/owner>
- Report transfer: <exact JSON/text source and receiving paths for isolated consumers, or shared paths>
- Coverage ledger:
  - <row identity> — prior status: <status>; implementation evidence: <command, setup/oracle and result, or none>; Incomplete reason: <reason or none>; next owner/status: <owner and unchanged reviewer status>
- Reviewer reproducer: `<exact command>` — <implementation outcome>
- Owning suite: `<exact command>` — <implementation outcome>
- Broad/aggregate gate: <exact command, run-or-skipped decision, reason, owner and stage, current evidence>
- Remaining reviewer coverage: <unchecked or blocked rows, or none>
- Next: the first outstanding applicable stage and complete ordered remainder
  through fresh independent `task-review-discovery` evidence to a fresh
  `task-acceptance-review` decision
```

Report implementation outcomes separately from reviewer row status. Do not
mark a row accepted, passed, or checked for the corrected bytes unless a fresh
reviewer does so in a separate invocation.
