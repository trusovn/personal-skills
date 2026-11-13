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

## Organization policy: source-guided worked cases

These cases check the instructions by tracing concrete inputs through the
implementer and maintainability-review consumers. They are worked examples,
not executed agent evals. They need no new harness, analyzer or provider. Keep
the existing preparation/measurement cases and their independent oracles.

For O-01–O-03, assume the **target** repository supplies this policy at
`docs/code-organization.md` and module guidance at `src/README.md`:

```text
Mandatory: acceptance owns disposition eligibility. Transport owns process
sessions and must not know finding dispositions. Extracted components cannot
import controller or receive its entire namespace. Keep authorization, lock
scope and publication order visible under one transaction owner.
Advisory: increasing size or complexity triggers responsibility assessment;
there is no numerical cutoff. Preserve untouched legacy code.
Module guidance: src/acceptance.py exposes eligible(facts); src/transport.py
owns session start/stop; src/controller.py composes these operations and owns
the accept-and-publish transaction.
```

| Case | Concrete change request or submitted diff | Implementer decision before editing | Independent reviewer expectation |
|---|---|---|---|
| O-01 — cohesive extension | `eligible(facts)` currently checks `facts.reviews_current`; add `facts.dispositions_current` to the same eligibility decision. No I/O, state ownership or dependency change. | Read target policy/module guidance; retain acceptance as owner, explain that the same invariant and facts boundary remain together; directly test the changed rule and preserve command wiring evidence. | Retention is justified by the shared invariant. Assess the module and consumers, but do not require extraction solely for growth. A metric-only retention statement would be insufficient. |
| O-02 — distinct responsibility | Request session cancellation and teardown. Proposed placement adds `start_session` and `stop_session` plus mutable session registry to acceptance. | Choose the transport/lifecycle owner, keep eligibility in acceptance, compose explicit operations from controller. If a new lifecycle module is necessary within authorized scope, document public operations/dependencies; do not force it into acceptance for a smaller diff. Resolve any authorization/transaction coordination before moving mutations. | Cite the ownership rule if unrelated lifecycle state is retained: changing cancellation now requires understanding acceptance state. Bounded correction restores the lifecycle owner; no unrelated legacy refactor or mandatory class/interface. |
| O-03 — harmful extraction | New `acceptance.py` starts `import controller` and reads `controller.current_run`; alternative `eligible(context)` reads `context.current_run`, where context is the controller module. Controller calls it while publication helpers independently acquire/release the lock. | Reject both namespace dependencies. Pass explicit facts; keep the accept-and-publish transaction's authorization, lock and order under its existing owner. Check extracted helpers with the caller, even if function metrics fall. | Mandatory rule finding cites the actual reverse edge/context bag and scattered lock boundary, their coordination/order cost, and the bounded explicit-input/transaction correction. Lower metrics cannot justify retention. Gate success alone cannot accept the semantic context-bag variant. |
| O-04 — no standalone policy | Existing `api-guided` implementer eval 3 and reviewer `semantic-control` eval 10 are initialized by their unchanged setup functions without `docs/code-organization.md`. | Continue under their supplied task/module authority; do not read the skill source checkout's policy or create a new one. Preserve existing scope and review route. | Review under supplied authority, preserving justified protocol complexity and independence; absence alone causes neither a finding nor INCONCLUSIVE. |

For the equivalent-policy variant of O-01, put the same policy at
`design/organization.md` and explicitly route it from target repository/task
authority. Both consumers must use that guidance before judging placement.
If material authority conflicts, return the conflict to its owner rather than
silently choosing this source checkout's rules.

To record a source-guided check, identify the target inputs above, trace both
consumer sections, and explain how they lead to the expected decision. Merely
finding keywords is insufficient. To qualify actual agent behavior later, stage
the stated inputs in an authorized disposable target, run separately approved
fresh role sessions, retain read/edit/command order, diff and report, and grade
against these decisions and the existing scope/provenance oracles. For O-03 the
reviewer must inspect the real diff and both caller/callee, not just the supplied
description. No executed-agent outcome is claimed by this catalog.
