# T-001.3 preflight

Status: ready
standalone_preflight_value: material

Source brief: docs/tasks/T-001.3/brief.md, SHA-256
`1fa661307ec3a32b7b7d1ff707e5ba38a1a09f7fa8826f227a372601a3e96357`.
Verification: [verification.md](verification.md), revision 1. Scope is the
brief's discovery guidance and installed composition proof; no alternative
briefs or T-002–T-005 workflow changes apply.

Accepted dependencies: T-001.1 `reviews/acceptance-01.md` and T-001.2
`reviews/acceptance-02.md`. Current `docs/contracts/index.json` resolves the
measurement, installation and foundation-tools records. Source runtime is
`scripts/measure_maintainability.py`; installed runtime is
`<target>/.agents/scripts/measure_maintainability.py`, with adjacent helpers,
defaults and requirements. The prepared interpreter is
`.quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python`.
Its installed versions match all five pins: Radon 6.0.1, Ruff 0.14.2,
mando 0.7.1, colorama 0.4.6, six 1.17.0. No download is needed.

Ownership: staged alternative briefs, verification.md and docs/tasks/index.json
are pre-existing user work. Preserve them. No implementation overlap exists.
Do not refresh `.agents/`. Optional evidence availability reported
`git_metadata_unwritable`; skip that sidecar for this invocation.

Feasibility and planned evidence:

- AC-01/02, R-05, V-01a–g/V-02: inspect four named source skills and optional
  template; write concrete discovery handoffs in results. Preserve native
  policy, scope, requiredness and owner. No new registry/runner or review stage.
- AC-03, R-06, V-03/04: extend existing measurement cases with relocated installer
  fixture; remove its disposable distribution before CLI execution from another
  cwd. Real Git/index, countable functions and hashes are the oracles.
- AC-04, V-05/06/07: reuse installed four-state settings, malformed/typed-setting
  and setup-dispatch cases. V-08: reuse native unknown/neutral/old-format cases;
  extend installed comparison/collision evidence. No provisioning/network call.
- AC-05, V-09: reuse installer resource and all-family refresh/drift journeys;
  existing explicit lists already include both source skills and shared runtime.
- AC-06, V-10: add real Ruff F401 command with clean control and violating input,
  then successful installed measurement. Record native whole-project authority
  and owner separately. This proves tool composition, not live agent compliance.

First targeted command (repository root):
`PYTHONDONTWRITEBYTECODE=1 .quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python -m unittest discover -s tests -p test_maintainability.py`.
Use selected cases first, then full measurement suite, installer suite and
`tools/verify.py` using that interpreter. Aggregate covers architecture/contracts
when the same commands run. Report active-profile drift without repair.

The material uncertainty resolved here is real-tool availability and the existing
distribution-removal isolation fixture. Retain this preflight route for similar
installation-boundary work. Source instructions are development specifications;
installed skill instructions govern execution. Intended consumer is T-002;
misleading advisory success could hide native failures, so preserve separate
observations. No product decision remains open. Stop for authority conflict,
missing real tools or unapproved network/expensive verification.

Next: implement scoped guidance and missing installed evidence, verify, then hand
completed bytes to the first applicable conditional review stage and fresh
independent discovery followed by separate acceptance. No reviewer verdict is
claimed by implementation.


## Focused reconciliation of H-01 — 2026-11-02

Status: ready
standalone_preflight_value: material

This is a readiness delta for acceptance-01 H-01, not an acceptance verdict.
The earlier preparation above remains historical; this section supersedes only
its gate-result applicability. Authority remains brief.md (SHA-256
`1fa661307ec3a32b7b7d1ff707e5ba38a1a09f7fa8826f227a372601a3e96357`),
verification.md revision 1, AC-02/AC-05, R-06 and V-02/V-09. No requirement or
scenario revision is made. The current task-owned staged changes and untracked
acceptance-01 report are pre-existing work and remain untouched. Only this
canonical readiness artifact is updated; it is not staged by this invocation.

### Policy and current capability

The brief's Verification section explicitly requires running the aggregate and
reporting failures and active-profile drift truthfully, and forbids repairing
that drift by refreshing this invocation. AC-02 and verification Shared setup /
V-09 likewise require preserving the active installation. The brief does not
require that this deliberately preserved active installation match newly edited
source during the current invocation. The development guide and tools/verify.py
correctly define the aggregate as nonzero when any constituent fails; that
command behavior remains unchanged.

These obligations are compatible: run and retain the aggregate result; report
expected source-versus-active-installation drift; qualify installation behavior
on disposable targets. No waiver of a native hard failure, command exit status,
or required scenario is implied. An all-green aggregate is not claimed. Treating
the four expected drift paths alone as a new requirement for same-session repair
would contradict the explicit preservation rule. This resolves H-01's policy
uncertainty; the next acceptance reviewer decides its disposition.

### Focused command and oracle

Repository-root command, run in this invocation:

`python3 scripts/install_development_skills.py --check .`

Observed exit: 1. Compared paths: 95. Exact differences, all category `changed`:

- `.agents/skills/README.md`
- `.agents/skills/architecture-guardrails/SKILL.md`
- `.agents/skills/architecture-guardrails/templates/gates.yaml`
- `.agents/skills/repo-foundation/SKILL.md`

Oracle: exactly the four source resources modified by this task, with no missing
or unrelated managed paths. This confirms the previously reported drift remains
bounded and expected. It is a read-only comparison, not behavioral installation
proof. It does not turn the failed aggregate into a passing command.

### Evidence applicability and decision context

- AC-01/AC-06, R-05, V-01a–g/V-10: unchanged authority, guidance and independently
  published discovery evidence remain applicable. No new execution is needed to
  resolve H-01. Native hard/advisory separation remains mandatory.
- AC-02/AC-05, V-02/V-09: source membership and active-installation preservation
  are consistent. Discovery D3/D4 independently qualify disposable fresh install,
  drift detection and refresh, including unrelated-byte preservation. The active
  installation comparison above is a separate expected mismatch.
- AC-03/AC-04, R-06, V-03/V-04/V-05a–d/V-06a–c/V-07/V-08a–g: no runtime,
  dependency, setup or scenario change; discovery D2/D7 remain applicable to the
  unchanged implementation bytes. These results are consumed, not rerun here.
- Aggregate: producer-attributed host execution ran 528 tests with no skips and
  retained exit 1 solely for these four drift paths. Discovery did not rerun the
  aggregate; D5/D6 independently cover architecture/current registry. No new
  broad run is justified solely to repeat the same expected mismatch. Any newly
  demonstrated failing constituent or changed behavioral bytes returns to its
  evidence owner rather than being covered by this reconciliation.

Intended consumer remains T-002. The material consequence to avoid is presenting
advisory success or an expected installation mismatch as overall native-gate
success. Existing mitigations are separate outcome reporting, independent
composition evidence and immutable historical review records. No approved
known-issue deferral is created. No policy change, active refresh, production
correction, network use or expensive test run is authorized or performed here.

### Warnings, stops and next action

Readiness is ready for a fresh acceptance decision on the reconciled gate record;
it does not authorize advancement. Stop if drift includes missing/unrelated
resources, implementation bytes change, a real required scenario lacks evidence,
or a non-drift gate failure appears. Do not refresh this active installation.

Standalone preflight added material value by distinguishing the aggregate's
truthful nonzero exit from a task requirement to repair active installation
state. Recommend this focused route for the same policy ambiguity, not a routine
repeat of clean discovery.

Implementer handoff:

```text
H-01: policy uncertainty reconciled; no production correction established.
Authority: T-001.3 brief Verification + AC-02/05; verification revision 1.
Current check: python3 scripts/install_development_skills.py --check .
Result: exit 1; exactly four expected changed task-managed profile resources;
95 paths compared; no missing/unrelated paths. Active installation preserved.
Aggregate remains producer-attributed exit 1; no all-green claim or gate waiver.
All V-01a–g, V-02, V-03, V-04, V-05a–d, V-06a–c, V-07,
V-08a–g, V-09 and V-10 discovery results remain unchanged and applicable.
Correction owner: none. Evidence owner: discovery. Readiness reconciliation:
this focused preflight. Final disposition owner: fresh acceptance reviewer.
Next: separate task-acceptance-review with acceptance-01, discovery-01,
results.md and this current preflight delta. No aggregate rerun just for reporting.
```

Write audit: only preflight.md was edited; the staged diff was verified unchanged.
The new worktree-only preflight delta is intentional and must be included in the
next review's evidence scope. Acceptance-01 remains unchanged historical evidence.
