# Implementer eval preparation

Original evals 1–9 and `entry-cases`, `route-cases`, `review-cases` remain separate.
The finite T-003 cases are in `files/measurement_cases.json`; their IDs retain
verification revision 1's row identities. V-01f varies tools/settings/checks;
V-03c varies rename/move/extraction; V-03e varies docs/unsupported; V-04a–g cover
all three metrics; V-05a–f each cover advisory/indispensable policy; V-10d covers
significant/trivial changes; V-06 retains each checkpoint. V-11 cases inspect
current guidance, generated inputs, installer projection and the submission.

Run setup from this source distribution with an already pinned interpreter:

```sh
export EVAL_SOURCE_ROOT="$PWD"
export EVAL_MEASUREMENT_PYTHON="$PWD/.quality/venv/bin/python"
EVAL_WORK_ROOT=/tmp/implementer-case python3 -B \
  skills/task-implementation-flow/bounded-task-implementer/evals/files/setup_fixture.py \
  measurement:V-04a-complexity
```

`EVAL_WORK_ROOT` must be disposable: existing scenario roots there are replaced
by the original fixture initializer. Setup explicitly installs the canonical
source profile **only in the disposable target**, never the active repository.
It requires the source distribution and an existing pinned Radon/Ruff interpreter;
setup fails if either is absent and never provisions dependencies. A runner that
stages eval files elsewhere must supply `EVAL_SOURCE_ROOT` and
`EVAL_MEASUREMENT_PYTHON` explicitly. Those are prerequisites for these prepared
agent evals, not permission to refresh an active installation or run live models.

Each input includes the bounded action/permission, actual baseline pair, target
code, scenario oracle and preserved-byte snapshot where applicable. Deliberately
altered/missing reports and capability faults are seeded inputs, not tool output
or evidence of attempted recovery. High-assurance variants reuse the queue
packet/schema/index-digest fixture; corrections reuse REC-44's complete ledger.
Both supplied report paths and fresh report-write permission are part of entry.
Direct cases' B is a setup control: the agent must capture its own actual start.

Run the local preparation check with the pinned interpreter:

```sh
EVAL_MEASUREMENT_PYTHON="$PWD/.quality/venv/bin/python" \
  .quality/venv/bin/python -B \
  skills/task-implementation-flow/bounded-task-implementer/evals/files/check_measurement_fixture.py
```

This exercises setup at disposable roots, source/index/report preservation,
actual threshold comparison values, and a real native success/failure/correction
sequence. The owning `tests/test_maintainability.py` supplies broader runtime
error, collision, relocation, native-exemption and empty-folder evidence.
Fixture checks cannot qualify an agent's attribution, rationale, refusal,
recovery, stage routing or aggregate reuse decision.

When an agent is run separately, grade the actual final code/diff, report source
hashes and identities, command/edit order, native history/invocation count and
submission against each case oracle. Reject a success claim based only on setup
exit status, keywords or plausible paths. B/C1 must stay byte-for-byte intact;
C2 must identify current bytes against B. Missing rationale must be recovered,
but a retained breach with a coherent local explanation is a valid control.
Unknown native counts cannot become zero. Native hard failure remains effective
with successful or N/A metrics. Changed bytes invalidate affected proof; prior
review ledger states remain separate from implementation checks. Unrun cases
remain unqualified for agent behavior; T-005 owns the full installed journey.
