# T-004.2 result

Completed and independently **ACCEPTED**, 2026-11-12.

The controller now admits fresh independent collection for the actual checked
candidate, executes collector-owned reruns, preserves findings/dispositions and
history, and supports the real failed-check → code correction → new checks →
fresh collection loop within the inherited shared correction budget. Collection
does not decide acceptance or completion.

The ordered route completed: ready preflight → implementation → CLEAN
architecture gate → fresh maintainability ACCEPT → registry synchronization →
fresh independent discovery → separate fresh acceptance ACCEPT. No discovery
finding or deferral remains; all 44 required finite scenario rows pass.

Authoritative results:

- [Acceptance decision](reviews/acceptance-01.md), including admitted coverage,
  reviewed identities and unchanged index evidence.
- [Independent discovery](reviews/discovery-01.md), including per-row setup,
  behavioral oracles, challenge probes, raw log locations and aggregate record.
- [Maintainability acceptance](reviews/maintainability-01.md), including independent
  original-baseline comparison and all 11 metric obligations.
- [Registry synchronization](reviews/contract-registry-01.md).
- [Implementation evidence](implementation-report.md) and
  [T-005 controller contract](../T-004/controller-contract.md).

Independent actor suite: 50 pass; state suite: 45 pass; architecture: 4 pass.
Contract registry: 8 subsystems / 36 indexed references. The current whole-repo
aggregate is **failed**, 1 of 7 checks: orchestrator has 6 failures, 7 errors and
20 skips; root tests have 32 skips. Discovery independently reproduced exactly
the same 13 failure/error identities on unmodified HEAD. These inherited Linux
legacy-containment limits are neither passes nor approved deferrals; no required
local T-004.2 row is host-blocked.

## Work requiring another environment

The operator must use macOS with Python 3, Git and permitted
`/usr/bin/sandbox-exec` to qualify the inherited containment/inspection cases.
Carry the same reviewed worktree and evidence; do not refresh active skills.
From that checkout run:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-orchestrator/tests -p 'test_*.py' -v
PYTHONDONTWRITEBYTECODE=1 python3 tools/verify.py
```

Retain full logs, actual failures/skips and checked-byte identities. Denial on a
supported macOS host is a failure. These checks do not need a model/provider.
This is remaining legacy qualification, not an unfinished T-004.2 scenario.

The 32 root skips concern optional real analyzer/pinned-dependency evidence.
Discovery documents how to run the aggregate with the already prepared pinned
interpreter; this can be done locally and does not require provisioning here.
T-006 separately owns real sbx/provider/model qualification. That live pilot was
not authorized or run; local actors do not establish provider identity, semantic
review quality or runtime-enforced collector read-only isolation.

## Successor

T-005 preparation may consume the [consolidated contract](../T-004/controller-contract.md),
[T-004.1 acceptance](../T-004.1/reviews/acceptance-02.md) and this task's acceptance.
T-005 owns ART-009 semantic admission and completion; it was not executed here.
The [parent closure](../T-004/result.md) records composed coverage without editing
the official plan, briefs or task index.

Original staged verification, index and owner files remain preserved. No commit,
installation refresh or tracker write occurred. Raw reports remain under ignored
`.quality/reports/T-004.2-*`; transfer them explicitly if moving checkouts.
Retained copied run trees keep original absolute provenance and are inspection
evidence, not rebased runnable runs.
