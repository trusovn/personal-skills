# SIDE-004 discovery-01 — organization instructions

Producing stage: `task-review-discovery`. Coverage: complete targeted discovery;
V-07 aggregate remains explicitly unchecked after the decisive V-01 failure.
Created: 2026-11-13T16:53:49.989190+00:00.
This is evidence only, with no acceptance verdict, approved deferral or advancement.

## Provenance and authorities

Fresh child session `/root/discovery` authored no reviewed production, test,
preparation or submission bytes. Active instructions were resolved from
`.agents/skills/task-implementation-flow/task-review-discovery/SKILL.md` and
`.agents/skills/testing-discipline/SKILL.md`; its report template was consumed.
Source consumer instructions were editing targets under review, not active skills.
Read repository AGENTS instructions, docs/project-map.md, docs/development.md,
SIDE-004 brief.md, verification.md revision 1, ready preflight.md (decision context
and native obligations), organization-context.md and implementation-report.md.
T-005.1 result.md and acceptance-02.md establish the completed prerequisite.
Owner instruction explicitly skips maintainability for this instructions-only
change; no maintainability or measurement artifact is owed for this scope.
The implementation report records owner authorization to move examples/controller
illustrations out of the policy; that move is respected. It records no waiver of
the three official references required by AC-01.

## Findings

### F-01 [suggested P2] Required background references were removed

- Location: `docs/code-organization.md:81` (policy ends after enforcement);
  authority: `docs/tasks/SIDE-004/brief.md:84`–88.
- Trigger: read the staged standalone policy and supporting organization context
  as a consumer of the delivered instructions.
- Consequence: the delivered guidance lacks all three explicitly required
  official Python background references. The implementation-report cleanup's
  statement that three references remain is stale for current staged bytes.
- Evidence: all 81 policy lines and all 41 context lines inspected. Targeted
  search `rg -n 'modules.html|functional.html|public-and-internal-interfaces'
  docs/tasks/SIDE-004 docs/code-organization.md` finds URLs only in brief.md's
  requirement, not in either delivered guidance document.
- Affected AC/invariant: AC-01 / V-01 requires modules tutorial, Functional
  Programming HOWTO and PEP 8 public/internal-interface references as background.
- Credible sibling surface: both implementation and review consume the same
  policy; all three requested references and their supporting context share the
  missing-background-source obligation.
- Bounded corrective direction: restore the required background references in
  delivered organization guidance, with local actionable rules retaining authority.
  No runtime restructuring or broad documentation rewrite is indicated.

## Completeness ledger

Submitted evidence for every row is the corresponding V-row in
implementation-report.md; prior labels were treated as claims. Independent
probes below apply to current staged bytes, which equal their worktree copies.

| Row | Authority / material cases, setup and oracle | Independent current evidence | Result |
|---|---|---|---|
| V-01 | AC-01; ten concrete rules across production/tests/evals/fixtures/harnesses, mandatory/advisory distinction, three placement examples, future-only controller candidates, official references | Read full policy and context plus map diffs. Rules 1–10 map in order to all ten brief recommendations; concrete exceptions and scope limits are present. Context supplies cohesive eligibility extension, lifecycle ownership and harmful controller/context-bag split; candidate interfaces/transactions remain future decisions. Official refs absent as F-01. | fail — required references missing; remaining document requirements corroborated |
| V-02 | AC-01–03; O-01 target policy plus src/README module guidance; add dispositions_current to eligible(facts) with unchanged owner/dependencies | Traced both staged consumer sections against concrete shared O-01 inputs. Implementer resolves target guidance before placement and explains retaining same invariant/facts; reviewer assesses cluster/callers and allows cohesive retention without numerical cutoff. | pass — source-guided instruction conformance only |
| V-03 | AC-01–03; O-02 session cancellation/teardown plus mutable registry proposed in acceptance | Traced consumer rules against module map assigning lifecycle to transport and composition to controller. Implementer permits necessary new owner/module within scope; reviewer identifies cancellation coupling to unrelated acceptance state and bounded ownership correction, without untouched cleanup or mandatory class. | pass — source-guided only |
| V-04 | AC-01–03; O-03 extracted acceptance imports controller or receives its module as context; scattered lock acquisition | Both consumers require explicit direction/transaction ownership and review helper/caller cluster. Policy rules 5/7 prohibit both namespace variants and distributed mutation ownership; low metrics do not discharge them. Explicit facts and existing controller transaction are the bounded route. | pass — source-guided only |
| V-05a | AC-02–04; actual api-guided and semantic-control targets without standalone policy | Independent setup invocations in probe.py both exited 0 and produced Git targets with no code-organization.md. Both staged skills/eval 3 and 10 expectations require existing authority, no source-policy substitution and no manufactured policy. Setup alone is not agent judgment. | pass — fixture setup and instruction/expectation inspection only |
| V-05b | AC-02–03; O-01 equivalent policy at design/organization.md explicitly routed by target authority; material conflict | Both staged sections explicitly honor equivalent routed authority and route material conflict to owner. Source/install root policy substitution is prohibited. | pass — source-guided only |
| V-06 | AC-04; inspect source membership/profile/shared files/README/tests; install, check, refresh, recheck into two disposable Git roots with policy/sentinel and no-policy control | probe.py actual public installer invocations all exited 0. Both consumer packages and managed guide match source bytes, policy and sentinel preserved, no source policy copied into no-policy root. Active .agents file hashes unchanged. Existing projection suffices; no new installer runtime/dependency required. | pass — actual filesystem distribution behavior |
| V-07 | AC-04/native obligations; focused installer, architecture, registry, drift and aggregate outcomes remain distinguishable | 36 focused installer tests passed without skips; canonical architecture 4 passed; current worktree registry 8 subsystems/37 refs validated. Active drift exit 1: seven changed paths, no missing/extra paths. Aggregate not run after decisive V-01 failure. | unchecked — aggregate deliberately suppressed under discovery contract; targeted constituents have current evidence |

## Probes, raw evidence and limits

Repository cwd: `/Users/mtrusov/work/skill-sources/personal-skills`. No live providers or networked qualification ran.

| Exact command / probe | Current result / raw evidence |
|---|---|
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -p test_install_development_skills.py` | exit 0; 36 tests, no skips; /tmp/SIDE-004-discovery/installer-tests.log |
| `.venv/bin/python /tmp/SIDE-004-discovery/probe.py` | exit 0; reproducible source and results.json retained in same raw directory; targets /tmp/SIDE-004-discovery-targets-3ycr3_rm |
| `.venv/bin/python scripts/install_development_skills.py <target>` then `--check <target>`, repeated for refresh/recheck | each exit 0 in owned-policy and no-policy targets; per-invocation raw logs retained |
| `.venv/bin/python -B skills/task-implementation-flow/bounded-task-implementer/evals/files/setup_fixture.py api-guided` | exit 0 with EVAL_WORK_ROOT=/tmp/SIDE-004-discovery-targets-3ycr3_rm/api-guided; api-guided.log |
| `.venv/bin/python -B skills/task-implementation-flow/task-maintainability-review/evals/files/setup_fixture.py semantic-control` | exit 0 with EVAL_WORK_ROOT=/tmp/SIDE-004-discovery-targets-3ycr3_rm/semantic-control; semantic-control.log |
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -p test_architecture.py` | exit 0; 4 tests; native-results.txt retains observed outcome; static CLEAN check only |
| `.venv/bin/python tools/check_contracts.py --root .` | exit 0; 8 subsystems / 37 references; native-results.txt; structural registry validation only |
| `.venv/bin/python scripts/install_development_skills.py --check .` | exit 1; active-drift.log records seven changed managed paths; intentionally preserved, never repaired |
| `git diff --cached --check` | exit 2; organization-context.md:41 new blank line at EOF. Formatting observation only; no behavioral implication. |
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python tools/verify.py` | not run — suppressed after F-01/V-01 decisive targeted failure; next evidence owner is fresh correction discovery |

V-01–V-05 are document/source-guided observations, not executed-role behavior.
No new executable schema/validator contract is claimed by the change; the
unchanged registry validator is routing infrastructure, not skill behavior.
Disposable commands completed synchronously; no fixture server or surviving
background process was launched. Temporary artifacts remain for inspection.
The submission's older aggregate/skips are historical claims, not this pass's
current qualification. No current aggregate capability-skip totals are claimed.

## Aggregate-gate ownership

Owner/stage: `/root/discovery`, initial independent discovery.
Exact gate: `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python tools/verify.py`.
Status: not run. Reason: V-01 found a decisive AC violation before broad testing;
required discovery policy suppresses the aggregate. Focused independent remaining
rows were safe and completed. A fresh correction pass owns regression closure,
reconciliation and any justified aggregate. Acceptance consumes this record and
adds no gate.

## Scope, identities and registry separation

HEAD: `c620cbc02b3c7fb361ccb0611a1e8260e847f658`.
Exact staged binary diff SHA-256: `663e5d23ccdf2d88bcc6427b35760d5dfb3aea29b0f72425143c283763bf2fb1`.
`/tmp/SIDE-004-discovery/staged.patch`, worktree.patch and identities.json retain
all staged bytes, each staged Git blob, and separate index/worktree SHA-256s.
All 17 staged paths equal worktree bytes. The following supplementary registry
updates are **unstaged**, and are not silently included in the staged submission:
foundation-tools.json, implementer-feedback.json, reviewer-feedback.json and
index.json under docs/contracts/. Their worktree semantics describe the new
policy and two target-owned consumers without claiming future decomposition;
source guides/maps and installation ownership agree. Existing installation
contract needs no runtime delta. Registry validation passes on that working tree.
A staged-only commit would omit this synchronization; no staging authorization
was inferred and no index bytes were changed. Three .DS_Store files are pre-existing
untracked owner artifacts and are excluded. The staged task brief is supplied
owner authority; preparation and submission files are task-context artifacts.
No source, test, fixture, plan, prior review, active installation or index edited.

Exact status before report:

```text
M  README.md
A  docs/code-organization.md
 M docs/contracts/foundation-tools.json
 M docs/contracts/implementer-feedback.json
 M docs/contracts/index.json
 M docs/contracts/reviewer-feedback.json
M  docs/project-map.md
M  docs/tasks/SIDE-004/brief.md
A  docs/tasks/SIDE-004/implementation-report.md
A  docs/tasks/SIDE-004/organization-context.md
A  docs/tasks/SIDE-004/preflight.md
A  docs/tasks/SIDE-004/verification.md
M  skills/README.md
M  skills/task-implementation-flow/README.md
M  skills/task-implementation-flow/bounded-task-implementer/SKILL.md
M  skills/task-implementation-flow/bounded-task-implementer/evals/README.md
M  skills/task-implementation-flow/bounded-task-implementer/evals/evals.json
M  skills/task-implementation-flow/task-maintainability-review/SKILL.md
M  skills/task-implementation-flow/task-maintainability-review/evals/README.md
M  skills/task-implementation-flow/task-maintainability-review/evals/evals.json
M  skills/task-orchestrator/references/architecture-map.md
?? .DS_Store
?? docs/.DS_Store
?? skills/.DS_Store
```

Exact status after report is the above plus this sole added entry:

```text
?? docs/tasks/SIDE-004/reviews/discovery-01.md
```

The writer independently compared before/after using --untracked-files=all and
required that single new report entry be the only difference. The report applies
only to identified bytes and does not authenticate or review itself.

## Questions and next route

No decision-critical authority question was found. Optional formatting observation:
trailing blank EOF above. Residual qualification limit: real agent compliance
remains unqualified by design; no live/model evaluation was authorized.
F-01 remains open. V-07 aggregate is unchecked for the concrete suppression
reason, with fresh correction discovery owning recovery; no required row is
silently treated as clean. Registry staging remains coordinator-owned scope.
Next: separate acceptance decision consumes this report, current diff, brief,
verification revision 1, ready preflight/context, all rows and F-01. Discovery
makes no acceptance or advancement decision.

## Discovery continuation

- Iteration / identity: initial independent pass; HEAD c620cbc02b3c7fb361ccb0611a1e8260e847f658; staged diff SHA-256 663e5d23ccdf2d88bcc6427b35760d5dfb3aea29b0f72425143c283763bf2fb1; per-path index/worktree identities in /tmp/SIDE-004-discovery/identities.json.
- Coverage: V-01 fail (F-01); V-02, V-03, V-04, V-05a, V-05b, V-06 pass within stated evidence limits; V-07 unchecked (aggregate suppressed; focused constituents and drift recorded).
- Findings: F-01 suggested P2, required official background references missing; both skill consumers share the policy surface.
- Continuity: implementation self-check claims are prior context only. Current independently observed document/distribution/native evidence above supersedes copied pass claims. Correction owner: bounded-task-implementer; missing aggregate evidence owner: fresh correction discovery; decision owner: separate acceptance; registry index management owner: coordinator/updater.
- Preparation/context: docs/tasks/SIDE-004/brief.md; verification.md revision 1; ready preflight.md with native/decision context; organization-context.md; implementation-report.md including authorized cleanup scope.
- Reviewer regressions: no new maintained tests; re-read required background references in corrected delivered guidance; repeat affected V-01 and V-07 under current bytes, preserving other rows.
- Aggregate: not run; exact command/owner/reason in aggregate section.
- Next: separate task-acceptance-review call, without merging discovery and decision.
