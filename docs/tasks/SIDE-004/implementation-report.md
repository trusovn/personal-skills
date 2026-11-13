# SIDE-004 implementation submission

Implemented: **READY_FOR_REVIEW**

The repository now has a standalone organization policy and both source skill
consumers resolve target-owned guidance before placement/review. No runtime
refactoring, AGENTS.md edit, official-plan update, index staging or active skill
refresh was performed. Independent acceptance is still owed.

## Authority, preparation and placement

Consumed [brief.md](brief.md), [verification.md](verification.md) revision 1
and ready [preflight.md](preflight.md), including its decision context and native
obligations. T-005.1 closure/acceptance establishes the cross-index prerequisite.
Preparation used the installed project-local verification-design and preflight
skills; implementation used the installed project-local implementer and testing
discipline. Edited source skills are development assets, not newly active
instructions. The reviewer source was read as an editing target, not invoked
as an independent review of this submission.

Placement decisions: project policy belongs at docs/code-organization.md, with
maps retaining current inventories. Generic target-policy resolution belongs
in each consumer's existing protocol. Existing eval READMEs own the worked
cases; the reviewer README links to one common input/oracle table rather than
duplicating scenario authority. Existing no-policy cases retain their setup
and original assertions, adding only the missing portable-policy expectation.
No Python or shared runtime dependency changed; measurement is **N/A** with no
baseline/comparison pair required.

## Changes and self-check

- [Policy](../../code-organization.md): ten required organization rules, scoped
  exceptions, advisory investigation triggers, review treatment, placement
  examples and the explicitly future controller-boundary discussion. All three
  requested official Python references are background, not delegated policy.
- Project and orchestrator maps route to that policy. The orchestrator map now
  distinguishes current controller entry points from placement of a new concern.
- Source implementer reads target policy/module guidance before choosing
  placement, explains owner/placement/dependencies before structural editing,
  and applies policy during implementation and final self-check.
- Source maintainability review checks the actual affected cluster, helpers,
  consumers and dependency changes against the same target authority. Findings
  require rule/evidence/consequence/bounded correction; mandatory violations
  and advisory concerns retain distinct treatment and untouched debt protection.
- Task-flow/profile guides and README explain portable consumption and that
  project policy remains project-owned. Installer membership, managed guide,
  shared-file list, focused coverage and documentation were inspected. Existing
  whole-package projection already distributes all changed consumer resources;
  no installer code, managed path or ownership expansion was needed.

## Scenario evidence

These are implementation self-checks. They supply no independent verdict or
executed-agent behavioral qualification.

| Scenario | Current evidence and result |
|---|---|
| V-01 | Document review maps all ten AC-01 recommendations to the policy's numbered rules. Scope covers production/tests/evals/fixtures/harnesses. Mandatory rules and advisory signals, examples, current-map routing, future candidate boundaries and transaction/interface caveats are explicit. 26 local reference targets across policy/maps/preparation/eval docs exist; that last check is structural only. |
| V-02 | Worked O-01 supplies a target policy, module map and extra disposition-current fact in eligibility. Both consumers resolve that authority and assess the same owner/inputs/consumers. Cohesive retention is supported; size alone cannot force extraction. Source-guided result only. |
| V-03 | Worked O-02 puts session cancellation/teardown and session state into acceptance. The policy's lifecycle owner and explicit composition rules determine placement; both consumers require an owner/dependency explanation and allow a necessary new module. Review consequence is coupling cancellation changes to unrelated acceptance state. Source-guided result only. |
| V-04 | Worked O-03 supplies both controller import and whole-module context variants, plus scattered lock ownership. Consumer instructions require cluster/caller inspection against the mandatory dependency/transaction rules. Explicit facts and the existing transaction owner are the bounded correction; lower metrics cannot excuse the split. Source-guided result only. |
| V-05a | Existing `api-guided` and `semantic-control` source setup commands executed at fresh disposable roots and each produced a Git target without a standalone policy. Existing eval 3/10 expectations now require continuing under supplied authority, without source-policy substitution or policy generation. Fixture/setup evidence only; agent compliance unqualified. |
| V-05b | O-01 equivalent-policy variant explicitly routes `design/organization.md` from target authority. Both consumer sections honor equivalent routed guidance and return material conflicts to the owner. Source-guided resolution result only. |
| V-06 | Real disposable install/check/refresh/recheck all passed; both installed SKILL.md files equal source bytes. Existing owner policy and unrelated sentinel remained byte-identical. A separate policy-free target received no source policy. Captured active .agents files stayed byte-identical. Focused installer suite: 36 passed. |
| V-07 | All executed maintained tests and architecture/registry constituents passed. Aggregate exits 1 solely for active profile drift, explicitly retained below. No live eval, skipped capability or source-guided example is counted as successful agent behavior. |

Shared worked inputs/oracles: [implementer eval preparation](../../../skills/task-implementation-flow/bounded-task-implementer/evals/README.md#organization-policy-source-guided-worked-cases).
No new harness, fixture generator, string-assertion suite or test family was
added. Existing installer coverage and disposable filesystem observations are
the executed distribution evidence; prose/expectation checks remain distinct.

## Commands, native evidence and retained raw artifacts

Commands ran from the repository root with the project interpreter. Submitted
source identities are `/tmp/SIDE-004-submitted-identities.json`; the staged
owner brief equals its worktree bytes and is excluded from authored changes.
No supported Python path changed. The identity file covers the 14 changed/new
source and preparation documents, excluding this explanatory submission report.

| Command / observation | Result / raw location |
|---|---|
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -p test_install_development_skills.py` | 36 passed, exit 0; `/tmp/SIDE-004-installer-tests.log` |
| Disposable installer probe, using `.venv/bin/python scripts/install_development_skills.py <target>` and `--check <target>` | Install/check/refresh/recheck exit 0; owner policy content `Owner policy: session lifecycle belongs in process_sessions.` and sentinel `preserve unrelated owner work` preserved. Fresh no-policy target lacks docs/code-organization.md. Targets, command logs and exact active-file hashes: `/tmp/SIDE-004-install-h0w6ucsh/`, result.json. |
| `.venv/bin/python -B <source-skill>/evals/files/setup_fixture.py api-guided` / `semantic-control`, each with a fresh `EVAL_WORK_ROOT` | Both exit 0; target policy absence observed. Exact target paths and setup logs: `/tmp/SIDE-004-preparation-uhr0wu9c/`, result.json. No role/model launched. |
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python tools/verify.py` | 7 checks, 1 failed, exit 1; `/tmp/SIDE-004-verify.log`. Five unittest roots: 3, 13, 4, 283 and 311 tests, all successful for executed cases; 52 skips. |
| Canonical architecture policy | Four test_architecture cases passed in the aggregate's root `unittest discover -s tests -p test_*.py -v` constituent against current bytes. This covers the canonical `discover -s tests -p test_architecture.py` scope; not rerun solely for reporting. CLEAN static policy only, implementer stage. |
| `.venv/bin/python tools/check_contracts.py --root .` | Aggregate constituent passed: 8 subsystems, 37 indexed references. Structural agreement only; updater-owned semantic reconciliation remains owed. |
| `.venv/bin/python scripts/install_development_skills.py --check .` | Aggregate constituent failed as expected: seven changed managed files (profile guide plus SKILL.md, eval README and eval JSON in each consumer). No missing/unexpected paths. Active installation deliberately remains unchanged. |
| `git diff --check` | Passed. |

The 20 containment skips require macOS /usr/bin/sandbox-exec; the 32 optional
measurement skips require real pinned Radon/Ruff. Neither capability is
qualified here. Live/model evaluation was not authorized or run; policy
compliance remains unqualified. Optional run-evidence availability succeeded,
but the first lifecycle attempt used the invalid `status` subcommand. The
implementer skip-once rule was applied: no retries or run started, and no
instrumented lifecycle/completion claim is made. Raw native logs above remain
available independently of that optional sidecar.

## Ordered handoff

Next owner: fresh applicable **task-maintainability-review**, then
**task-contract-registry-updater**, then fresh independent
**task-review-discovery**, then the separate **task-acceptance-review** decision.
Publish numbered review evidence in this package. This invocation has not
launched, managed or substituted for those stages and issues no acceptance.

Registry updater should reconcile the new shared-policy consumption and
placement/cluster reporting contracts under implementer-feedback and
reviewer-feedback, along with affected guide/map discovery references. Inspect
installation/foundation-tools for any actual reference delta; do not invent
new installer behavior or register candidate runtime decomposition. Registry
files and generated index remain with that designated post-review stage.

Reviewers may reuse the shared raw paths above. Isolated reviewers must receive
the exact identity JSON, installer/preparation result JSON and logs, focused
installer log and aggregate log; /tmp evidence does not travel with a commit.
No measurement pair exists to transfer for this docs-only scope.

Task is not closed or independently accepted. Active-install drift remains
visible; any refresh belongs to a later run, not this invocation. The later
runtime reorganization effort has not been launched.

## Owner-authorized policy cleanup

The subsequent owner request approved shortening the policy around its numbered
rules and moving examples/controller context into supporting task documentation.
The policy is now 87 lines, with all ten numbered rules unchanged, a short scope
and placement introduction, one enforcement paragraph and the three references.
[Organization context](organization-context.md) retains the examples and future
controller discussion. The orchestrator map routes that discussion to its new
location. V-01 now reads the policy plus this supporting context; the remaining
scenario inputs and consumer instructions are unchanged. This owner direction
supersedes the brief's original requirement to keep those illustrations inside
the policy; the brief and historical evidence were preserved.

Cleanup checks: all ten rule numbers and local reference targets verified;
architecture 4 passed (`/tmp/SIDE-004-cleanup-architecture.log`); registry passed,
8 subsystems / 37 references (`/tmp/SIDE-004-cleanup-contracts.log`);
`git diff --check` passed. Fresh identities for the policy, context and changed
map are `/tmp/SIDE-004-cleanup-identities.json`, superseding their earlier byte
identities. These are document/static checks, not agent behavioral evidence.
The aggregate was not repeated for this prose-only cleanup; its earlier
active-install drift and capability skips remain recorded above. The independent
review route remains outstanding; no independent verdict is issued here.
