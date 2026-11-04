# Review evidence cases

Existing `evals.json` cases 1–10 and their multi-finding, correction, test-asset
and semantic fixtures remain unchanged. Analyzer-dependent representative actor
definitions live separately in opt-in `review-evals.json`; they require the
explicit prepared-interpreter/distribution environment below, and are not part
of the dependency-free legacy eval execution. `files/review_cases.json` adds the finite T-004 case
catalog. Each ID is an independently runnable preparation case with its exact
situation, artifact oracle and reused seed. Variants split only separately
required input faults or controls; they are not a Cartesian product. V-03 uses
complexity as the representative decision metric; existing owning measurement
tests exercise actual statement/argument target boundaries. V-03j supplies two
related metrics for grouped disposition.

Use a fresh authorized disposable directory for each case. Supply the source
distribution explicitly and an already prepared pinned interpreter. Never point
EVAL_WORK_ROOT at user work: existing fixture setup owns/replaces its generated
workspace. Setup installs only into that disposable target, not this session's
active installation. No dependency provisioning or provider calls occur.

```sh
EVAL_SOURCE_ROOT=/absolute/personal-skills \
EVAL_MEASUREMENT_PYTHON=/absolute/already-prepared/bin/python \
EVAL_WORK_ROOT=/tmp/review-case-unique \
PYTHONDONTWRITEBYTECODE=1 python3 evals/files/setup_fixture.py review:V-01a
```

The setup prints the target and records it in `workspace.txt`. Start a fresh
review actor in that target using `review-request.md` and the target installation.
The same-session controls V-01c/d explicitly supply contrary authorship; they
must yield SELF_CHECK_ONLY. Setup histories (I, R-control, prior verdicts and
conditional records) are labeled inputs, never evidence that a reviewer ran.
Keep the setup, case catalog and `task-runs/` outside reviewer read scope until
raw output, edit/command history and the new numbered report have been saved.

A qualified operator grades each case against `task-runs/oracle.json`, the
preserved snapshot and raw command records. Reconcile actual fields and code:

- R must be the reviewer's fresh public CLI invocation against B on actual
  affected changed/added/deleted assets. Compare file hashes, baseline path,
  effective identities and source/index/history preservation. I or R-control
  alone cannot pass. Stale I is deliberately retained in V-01b.
- Missing/incompatible/partial evidence must retain its precise gap and owner.
  Check recovery artifacts and execution, never only an unavailable keyword or
  exit code. JSON-only and text-only collisions must preserve old bytes.
- Check each rationale obligation against actual function/report values, diff
  relationships, cohesion and plausible alternative cost. Below/equal targets
  and untouched siblings need no defense. Justified breach is an ACCEPT control.
  Counterarguments need concrete future maintenance cost and bounded correction;
  smaller metrics cannot excuse the held-back semantic defects.
- Native results need actual command history, full governed scope, policy,
  checked bytes and producer/stage. Current aggregate controls have real native
  history; deliberately edited claims are labeled. Reject stale/narrow/omitted
  policy coverage. Recovery must preserve the old failure and add current proof.
- V-07 must reconcile all four rationale obligations, four distinct original
  blockers, the gap/owner and complete coverage, while only optional warnings
  are capped. A genuine stop keeps all outstanding rows; an early blocker is no
  reason to truncate. Original fixture oracles preserve distinct defect/control
  and stable finding-ID observations.
- Corrections compare both edits with unchanged B and preserve every prior pair.
  R-control proves CLI history only. Agent output must bind to current corrected
  assets and retain surviving/resolved IDs and all coverage rows.
- Expansion uses real outside paths, authorization and exact preserved bytes or
  an explicit before gap. Never relabel an edited-tree capture as original.
- Route variants have separate discovery/acceptance requests and labeled upstream
  numbered history. Grade actual scope/byte applicability and the ordered
  remainder: applicable registry → fresh discovery → separate acceptance;
  re-enter only affected conditional duties and execute no downstream stage.

As negative grading controls, remove one required disposition from a candidate
report, substitute I's stale hash for R's current hash, and replace V-10a's route
with acceptance alone. Each must fail its respective ledger/identity/route oracle
while an unchanged complete control remains admissible. These are operator
artifact checks, not a new automatic semantic grader. Save the modified candidate,
rejection reason and controlling actual input beside raw qualification output.
V-11b is not qualified merely by setup or a syntactically valid report.

Local setup/tool checks:

```sh
EVAL_SOURCE_ROOT=/absolute/personal-skills \
EVAL_MEASUREMENT_PYTHON=/absolute/already-prepared/bin/python \
PYTHONDONTWRITEBYTECODE=1 python3 evals/files/check_review_fixture.py
```

They exercise all finite preparations, actual fresh/stale comparisons, native
failure/recovery, immutable histories and four real over-target obligations.
They do not execute or grade an agent. Installer projection and the owning
measurement suite provide the separate portable/runtime evidence. Live actor
runs and independent grading need separate approval; T-005 owns the complete
installed producer-to-consumer journey.
