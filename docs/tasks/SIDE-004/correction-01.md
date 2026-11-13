# SIDE-004 correction-01

Restored the three required official Python background references while retaining
all local policy rules. Removed only the extra trailing blank line from supporting
context, as separately authorized by the coordinator. These document checks are
implementation evidence; fresh discovery and separate acceptance remain owed.

Implemented: **READY_FOR_REVIEW**

- Authority: `docs/tasks/SIDE-004/brief.md`, AC-01, plus the owner's instruction
  to fix discovered issues and rerun verification.
- Preflight/context reference: `docs/tasks/SIDE-004/preflight.md` (ready),
  `verification.md` revision 1, `organization-context.md`; readiness remains
  applicable to this bounded documentation correction.
- Preceding verdict: none; independent `reviews/discovery-01.md` published F-01
  and its ledger before an acceptance decision.
- Finding/scenario IDs: F-01; V-01, V-02, V-03, V-04, V-05a, V-05b, V-06, V-07.
- Complete finding and invariant: F-01, all three AC-01 background references
  absent from delivered guidance. The invariant requires the modules tutorial,
  Functional Programming HOWTO and PEP 8 interface reference as background while
  actionable local rules govern placement/review.
- Influenced sibling surfaces: all three references and both consumers of the
  shared policy; restored all references together. No consumer instructions,
  installer, runtime, registry semantics or tests changed.
- Attempts and discarded hypotheses: reproduced all three missing URLs before
  edit; one correction attempt; no discarded production hypothesis.
- Current scoped diff: `docs/code-organization.md`, seven-line Background append;
  `docs/tasks/SIDE-004/organization-context.md`, one extra EOF blank removed;
  this new correction report. Index remains unchanged, so corrections are
  unstaged. Existing staged policy/context still retain the original defect and
  formatting; acceptance must state its actual reviewed index/worktree scope.
- Measurement: N/A, Markdown-only; no supported Python edit or baseline pair.
- Native evidence: canonical architecture command below, four cases passed on
  corrected worktree, correction-implementation stage; registry command below
  passed, 8 subsystems / 37 references, structural evidence only.
- Report transfer: shared raw directory `/tmp/SIDE-004-correction-01/` contains
  pre-edit-map.json (all eight rows mapped before edits), index-before.patch,
  policy-before.md, context-before.md, references-before.json,
  references-after.json, check_references.py and architecture.log. No metric
  JSON/text pair applies. Fresh isolated reviewers need these exact files.

## Coverage ledger

Prior statuses are discovery-01 statuses, preserved without asserting fresh
reviewer status for corrected bytes.

| Row | Prior status | Implementation evidence / navigation use | Incomplete reason / next owner |
|---|---|---|---|
| V-01 | fail (F-01) | Exact three URLs absent before, all present once afterward; original policy remains unchanged as prefix; supporting context changes only EOF whitespace | Implementation correction supported; fresh discovery owns independent closure |
| V-02 | pass, source-guided | Existing cohesive-extension inputs and consumer sections unchanged; navigation only | Fresh discovery corroborates current scope |
| V-03 | pass, source-guided | Existing lifecycle-owner inputs and consumer sections unchanged; navigation only | Fresh discovery corroborates current scope |
| V-04 | pass, source-guided | Reverse-edge/context-bag and transaction cases unchanged; navigation only | Fresh discovery corroborates current scope |
| V-05a | pass, setup/instruction | No-policy setup and instructions unchanged; navigation only | Fresh discovery corroborates current scope |
| V-05b | pass, source-guided | Equivalent routed authority unchanged; navigation only | Fresh discovery corroborates current scope |
| V-06 | pass, distribution | Installer/profile packages and ownership boundary unchanged; navigation only | Fresh discovery corroborates current scope |
| V-07 | unchecked, aggregate suppressed | Architecture four passed, registry validation passed, worktree diff check passed; historical aggregate remains suppressed record | Fresh discovery owns current reconciled aggregate |

- Reviewer reproducer: `.venv/bin/python /tmp/SIDE-004-correction-01/check_references.py docs/code-organization.md`
  — exit 0; exact AC-01 URLs present. Prior snapshot reproduces missing references.
  This is static document evidence, not executed-agent behavior or link-server availability.
- Owning suite: no maintained executable tests changed or added for prose links.
  Direct policy/background inspection is decisive for this correction; the prior
  independent installer suite is navigation context, not new implementation evidence.
- Native architecture: `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -p test_architecture.py`
  — exit 0, four tests; `/tmp/SIDE-004-correction-01/architecture.log`.
- Registry: `.venv/bin/python tools/check_contracts.py --root .` — exit 0,
  8 subsystems / 37 indexed references; unchanged supplementary unstaged registry.
- Worktree formatting: `git diff --check` — exit 0. Index still intentionally
  contains pre-correction formatting; no staging was performed.
- Broad/aggregate gate: `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python tools/verify.py`
  — not run by correction author; fresh discovery owns reconciliation, clean
  targeted closure and any justified current aggregate. Expected active-install
  drift must remain visible and the active installation must not be refreshed.
- Remaining reviewer coverage: V-01 corrected bytes and V-07 aggregate require
  fresh reviewer evidence; all other row statuses need current-scope admission.

## Current identities and optional instrumentation

Policy worktree SHA-256:
`3ff833bf7f12c03858d8a41229ed334282c9b4ddc567e86dbb2d589e4fe59d3f`.
Context worktree SHA-256:
`4424ecce8f3b479ed23524f6fe55550f04292573c1ca15890864e99f3ed979f9`.
The correction check compared the exact cached binary diff with index-before.patch
and confirmed unchanged index bytes; no other source or active-install edit made.

Optional installed sidecar availability/active/begin succeeded and created
`run-20261113T165411Z-7ad6e713a6c0` under `.git/personal-skills/run-evidence/`.
The first check-wrapper operation failed before architecture execution because
the run-id positional argument was omitted. The invocation-local skip-once rule
was applied: no evidence-operation retry and no instrumented check/completion
claim. Architecture ran directly afterward and passed. The optional open run is
retained truthfully; later lifecycle recovery owns it. This does not replace the
raw correction evidence or authorize altering reviewed source/index state.

## Next

Fresh independent `task-review-discovery` correction pass, then separate fresh
`task-acceptance-review` decision. Maintainability is explicitly skipped by owner
for instructions-only scope. Reference restoration and EOF cleanup change no
registered contract semantics, so the already updated registry remains the
coordinator's supplied context without another synchronization edit. This
implementer invocation ends here without a review verdict or advancement.
