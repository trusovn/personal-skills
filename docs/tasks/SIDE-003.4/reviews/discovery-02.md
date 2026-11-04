# Independent discovery: SIDE-003.4 — Boundary groups 5–6

| Field | Value |
|---|---|
| Producing stage | Project-local `task-review-discovery` |
| Coverage completeness | Complete for local editorial/package checks; live routing unexecuted |
| Discovery iteration | Second independent discovery, requested by the user |
| Created | 2026-11-04 |
| Repository | `/Users/mtrusov/work/skill-sources/personal-skills` |
| Report | `docs/tasks/SIDE-003.4/reviews/discovery-02.md` |
| Authority | `docs/tasks/SIDE-003.4/brief.md`, AC-01–03; `docs/tasks/SIDE-003/plan.md`, Description design |
| Preparation | `docs/tasks/SIDE-003.4/verification.md`, revision 1; `preflight.md`, ready/guided |
| Submission | SIDE-003.4 section of `docs/tasks/SIDE-003/description-results.md` |
| Prior evidence | `reviews/discovery-01.md`, `reviews/acceptance-01.md` |

This report contains evidence and suggested severity only. It makes no acceptance
decision, approves no deferral, and advances no work. A separate acceptance call
consumes it. It applies only to the bytes identified below and does not review or
authenticate itself.

## 1. Provenance and reviewed bytes

This session authored no reviewed production, description, test, or submission
bytes. The changes were already staged at session start. The only repository
write by this session is this new report. The active skills were resolved from
the project-local `.agents/skills/` installation; source skills were read as the
review subject, without refreshing that installation.

HEAD: `b7b33378de819ec74897f288e28c6f6c0fa386e9`.
Scope: HEAD to the current index/worktree for the five named source skills and
the appended results section; preparation and prior reports are context.
Index bytes and worktree bytes were independently compared for all five source
skills and match. The source hashes also match those recorded by discovery-01.
Staging changed since that report; source content did not.

| Source skill | Worktree and index SHA-256 |
|---|---|
| bounded-task-implementer | `c0f596bc9508d0f17749fd50720cbbfe6a457896ce83e7805bff0cb2de9c5fc3` |
| task-maintainability-review | `c80582148ad4490a859d5400ab4cc7409dbd6682f13da2723be6f54c92cfec8a` |
| task-contract-registry-updater | `2cf8535599465000056d7ce8145febd81d52a1a3d0b300b4651a9ff4460f2cf9` |
| task-review-discovery | `4269c6f72d41b35d49ca3a1a2ebaaf46c02f98251c0093a1356cdbc35156955e` |
| task-acceptance-review | `81b51637a85c3942198842d2d7cfce2f926c0dc9d851c892eab9191e7fe03e83` |

Results SHA-256: `4e426c20eb6b943c3ccfcf1f40df40237b3798d459903e55b99af29eeecb4f5b`.
Full independent measurements and exact source hashes are retained in
`/tmp/side0034-independent/static.json` and `measurement.json`.

## 2. Findings

### F-01 [suggested P2] Preserve explicitly requested high assurance in the implementer description

Location: `skills/task-implementation-flow/bounded-task-implementer/SKILL.md:3`.

The new description limits strict freshness and raw JSON to supplied machine
contracts: “only for supplied machine contracts”. The unchanged body, lines
19–22, selects high assurance when **the user requests it OR the caller supplies
a machine contract**. Explicit user request is an independent entry route.

Trigger: a bounded implementation request that explicitly selects high assurance
without supplying a machine contract. For example: “Use bounded-task-implementer
in high-assurance mode for this bounded task; obtain any missing readiness inputs.”
The body must enter its high-assurance preparation path; the catalog description
instead excludes that profile's strict freshness/raw-JSON obligations for this
input. This is a demonstrated textual contradiction, not an observed model
misrouting claim.

AC-02 requires preservation of every valid current activation route. Verification
revision 1 also distinguishes explicit high-assurance invocation from V-01a-M.
Preserving the machine-contract case does not establish the explicit-request
case. The prior reports marked V-01a-FULL passed without resolving this mismatch.
The submission's removed-detail map even cites the body's user-request trigger,
but does not flag that the new description's exclusive condition contradicts it.

Consequence: discovery metadata can steer an explicitly requested high-assurance
implementation toward guided handling, or advertise output obligations that
disagree with the selected skill. This defeats the task's route-preservation
oracle even though all unchanged-body assertions pass.

Broken invariant: compression must not narrow a valid profile activation route.
Credible sibling surfaces: execute, resume, and correct requests with explicit
high assurance; supplied-machine-contract activation without that phrase; and
ordinary ready packages that must stay guided. Corrective direction: make the
description's profile conditions agree with the body's complete trigger set,
or remove exclusive procedural claims while retaining the required machine-contract
visibility. Preserve the packet-alone guided distinction. Recheck all three
profile cases and update this leaf's results evidence. No body change is needed.

## 3. Completeness ledger

E/P/N/B and FULL refer to the exact cases in verification revision 1. All pass
labels below are **editorial or local test evidence**, never observed model
selection. Prior rows are retained; grouped cells enumerate their individual IDs.
Submitted evidence for every row is the corresponding checklist/measurement/local
outcome in the SIDE-003.4 results section and the prior review ledger. Each was
corroborated against current bytes rather than accepted from its previous status.

| Row IDs | AC / setup and oracle | Independent evidence | Result |
|---|---|---|---|
| V-01a-E, V-01a-P, V-01a-N, V-01a-B | AC-01/02; exact explicit/guided implementation, architecture-wide negative, and maintainability-neighbor prompts | Current name/job retain implement/resume/correct, bounded request/brief/packet inputs, risk-based tests, progressive verification, user-work preservation and evidence; no product-wide redesign or review role added | pass editorially for these prompts |
| V-01a-M | AC-02; machine contract without a high-assurance request must remain visible | New scalar expressly names supplied machine contracts; body lines 19–22 agrees for this case | pass editorially |
| V-01a-FULL | AC-01/02; all original clauses and current activation routes must survive | Original 515-character scalar reconstructed from HEAD; guided human-readable mechanics remain in body, but the new exclusive machine-contract condition contradicts the independent user-request route; F-01 | fail; prior pass not corroborated |
| V-01a-EXPLICIT-HA | AC-02; separately requested high assurance without a supplied machine contract | Description line 3 versus body lines 19–22; concrete prompt in F-01. Additional named row makes the authority's separate route visible | fail editorially; F-01; model execution not performed |
| V-01b-E, V-01b-P, V-01b-N, V-01b-B, V-01b-FULL | AC-01/02; independent maintainability after implementation/correction, policy OR user trigger, before functional acceptance | All triggers, assets including test/eval/fixture/harness code, required architecture gate, verdicts and acceptance exclusion remain; removed regression dimensions remain in Review contract and Protocol steps 3/5/6/7 | pass editorially |
| V-01c-E, V-01c-P, V-01c-N, V-01c-B, V-01c-FULL | AC-01/02; synchronize current contracts and stale references after structural/maintainability review, before acceptance; exclude planned capability | Scalar and entire file equal HEAD; current-state/review timing and durable cross-task contract triggers remain. The unchanged 279-character scalar is a disclosed no-op expressly permitted by verification revision 1 | pass editorially |
| V-01d-E, V-01d-P, V-01d-N, V-01d-B, V-01d-FULL | AC-01/02; fresh independent evidence without a verdict, separate acceptance, six risk boundaries | All routing clauses remain; facts, severity, probes and continuation mechanics are present in Discovery workflow steps 7–9 and Output contract | pass editorially |
| V-01e-E, V-01e-P, V-01e-N, V-01e-B, V-01e-FULL | AC-01/02; admit independent evidence and decide advancement, report or equivalent evidence, immediate-review metadata, six risk boundaries | All original routing clauses and profile wording remain. Conditional-evidence details and no-new-discovery rules remain in Guided inputs and Decision workflow. No newly introduced exclusion of an original route found here | pass editorially |
| V-G5-DIST | AC-02; scoped authoring versus independent structural review | Implementer and maintainability neighbor prompts retain distinct jobs and review trigger; profile defect tracked separately under F-01 | pass editorially for group distinction |
| V-G6-DIST | AC-02; registry synchronization versus independent evidence versus separate decision | Three current descriptions preserve role, timing and evidence/decision separation | pass editorially |
| V-02 | AC-03; replace only description scalar with sentinel and compare to HEAD | All five masked remainders identical, including folded-block handling; four changed skill files, fifth disclosed no-op; other 21 source files equal HEAD; results are append-only | pass |
| V-03-BASE | AC-01/03; frozen target baseline must match pre-edit bytes | Independently recovered each target from HEAD; SHA-256 equals frozen baseline for all five; original counts 515/640/279/494/599 | pass |
| V-03-MEAS | AC-01/03; exact reduction, catalog sizes and invariant bodies | Fresh measurement: new counts 334/455/279/374/534; reduction 181+185+0+120+65=551; all-26 11,815→11,264, profile-20 8,176→7,625; body totals 388,640/320,123 unchanged; other 21 rows unchanged | pass |
| V-04-SUITES | AC-03; 13 exact focused suite commands from verification | Independently executed all 13; 210 discovered tests, 31 analyzer-dependent skips, no failures; command/count table below | pass for executed tests; skipped cases supply no evidence |
| V-04-LITERALS | AC-03; description-quoting consumers remain valid | Read/scanned all 13 suites plus review_fixture_support.py. AST string scan found zero literals present in an old skill and absent in its new full text; source diff contains no assertion edits | pass |
| V-04-VALIDATE | AC-03; optional quick_validate for five packages if YAML available | PyYAML is available in this session; all five actual validator invocations return exit 0, “Skill is valid!” | pass; current environment differs from prior recorded skip |
| GATE-ARCH | Required local architecture check | Current run: 4 tests, exit 0 | pass |
| GATE-CONTRACT | Required local contract check | Current run: 7 subsystems, 22 indexed plan refs, exit 0; no description is registered contract authority | pass structural check |
| AGG-VERIFY | Aggregate `python3 tools/verify.py` | Not run; SIDE-003.18 owns it; targeted F-01 also prevents a clean aggregate claim in this discovery | unchecked by this leaf; owner SIDE-003.18 |
| AGG-LIVE | Fresh-model E/P/N/B/M and distinct explicit-high-assurance inputs | Not run; no separately approved live-model budget | unchecked; evidence owner SIDE-003.18/coordinator after budget approval |

## 4. Adversarial and scope checks

- Compared selected five sources with non-selected 21; no other source changed.
- Masked the entire original folded description block for maintainability review,
  rather than masking only its first line; every non-description byte matches HEAD.
- Compared index blobs separately with worktree contents; all five match. The
  earlier reports' unstaged status is historical, not the present index state.
- Reconstructed baseline values from Git and compared target hashes with the
  frozen record, instead of trusting ephemeral producer measurement files.
- Checked machine-contract, explicit-request and packet-alone profile cases
  separately; preserving the first did not conceal failure of the second.
- No schema, process-lifecycle, network, migration or persistent-state behavior
  changed. Package checks do not prove model routing.

## 5. Commands and local outcomes

All commands ran from the repository root, without network access or dependency
installation. Independent artifacts remain under `/tmp/side0034-independent/`.
No source, test, prior report, installation, plan, registry, or staging state was
modified by these probes.

Static probe: Python read each target using `git show HEAD:<path>` and
`git show :<path>`, masked `description:` plus indented continuation lines,
and compared remainders with worktree bytes. It compared frozen-record hashes,
all 21 non-target files, and the results-file prefix. It invoked
`tools/baseline_measure.py` through its `measure(root, record)` function and
saved `measurement.json` and `static.json`. This is the same computation as the
documented CLI, with independently checked Git originals and byte masks.

Consumer probe: Python AST scan of string constants in the 14 named test/helper
files; for each old/new target file, report strings longer than three characters
present in the old file but absent from the new file. Result: no lost literals;
saved as `consumer-scan.json`. Passing literal assertions establish text
consistency, not the missing profile semantics in F-01.

Each suite command was:
`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p <pattern>`.
The first owning suite ran before the remaining sequential suites. The first
suite's output is retained in the tool transcript; the other 12 raw logs are
`/tmp/side0034-independent/<pattern>.log`, with summaries in `suites.json`.

| Pattern | Tests | Outcome |
|---|---:|---|
| test_bounded_task_implementer.py | 17 | OK |
| test_run_evidence.py | 18 | OK |
| test_run_evidence_availability.py | 5 | OK |
| test_maintainability.py | 33 | OK, 31 skipped: real Radon/Ruff required |
| test_review_composition.py | 22 | OK |
| test_task_preparation_contracts.py | 16 | OK |
| test_task_flow_guides.py | 14 | OK |
| test_task_maintainability_review.py | 26 | OK |
| test_task_review_discovery.py | 17 | OK |
| test_task_acceptance_review.py | 25 | OK |
| test_contextual_export_risks.py | 6 | OK |
| test_contextual_known_issues.py | 6 | OK |
| test_contextual_uncertainty_inputs.py | 5 | OK |

Other commands:

- `python3 skills/skill-creator/scripts/quick_validate.py skills/task-implementation-flow/<name>`
  for each of the five source names: exit 0 each. Raw logs: `<name>-validate.log`.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py`:
  exit 0, 4 tests OK; tool transcript.
- `python3 tools/check_contracts.py --root .`: exit 0, 7 subsystems and 22 refs;
  tool transcript. This is structural consistency, not behavioral qualification.
- `git diff HEAD --check`: exit 0.
- `git diff HEAD -- <five source paths>`, `git diff HEAD -- docs/tasks/SIDE-003/description-results.md`,
  `git diff --cached --stat`, `git status --short`: scope corroborated.
- Targeted reads of the brief, plan Description design, revision-1 verification,
  preflight, old/new descriptions and cited unchanged-body anchors: F-01 reproduced
  as a direct contradiction. No model was executed.

## 6. Aggregate-gate record

`python3 tools/verify.py`: **not run**. Owner: SIDE-003.18. Stage: second
independent discovery of SIDE-003.4. Reason: the leaf assigns this gate to the
closing task, and F-01 is a decisive targeted editorial failure. No aggregate
was used to hide it. The architecture and contract commands above are separately
required local checks, not a substitute aggregate. No gate was added.

Live fresh-model routing: **not run**. Owner: SIDE-003.18/coordinator after
separate budget approval. Current evidence is editorial only. F-01 must be
resolved and its local profile cases rechecked before any claim of clean routing.

## 7. Scope and baseline comparison

The brief, frozen baseline, measurement tool, installer and tests have no changes
against HEAD. The source diff is four description-scalar edits; the fifth target
is a documented no-op permitted by verification revision 1. The results diff is
an additive 110-line leaf section. Existing preparation and review artifacts
were staged before this session and remain untouched. No unsafe ownership
overlap was found.

Pre-report status:

```text
A  docs/tasks/SIDE-003.4/preflight.md
A  docs/tasks/SIDE-003.4/reviews/acceptance-01.md
A  docs/tasks/SIDE-003.4/reviews/discovery-01.md
A  docs/tasks/SIDE-003.4/verification.md
M  docs/tasks/SIDE-003/description-results.md
M  skills/task-implementation-flow/bounded-task-implementer/SKILL.md
M  skills/task-implementation-flow/task-acceptance-review/SKILL.md
M  skills/task-implementation-flow/task-maintainability-review/SKILL.md
M  skills/task-implementation-flow/task-review-discovery/SKILL.md
```

Post-report `git status --short`, checked after writing this report:

```text
A  docs/tasks/SIDE-003.4/preflight.md
A  docs/tasks/SIDE-003.4/reviews/acceptance-01.md
A  docs/tasks/SIDE-003.4/reviews/discovery-01.md
A  docs/tasks/SIDE-003.4/verification.md
M  docs/tasks/SIDE-003/description-results.md
M  skills/task-implementation-flow/bounded-task-implementer/SKILL.md
M  skills/task-implementation-flow/task-acceptance-review/SKILL.md
M  skills/task-implementation-flow/task-maintainability-review/SKILL.md
M  skills/task-implementation-flow/task-review-discovery/SKILL.md
?? docs/tasks/SIDE-003.4/reviews/discovery-02.md
```

Only the new report entry differs. Source hashes were rechecked after the write
and still match the reviewed values. The index was preserved.

## 8. Questions and residual risks

No local required row remains unaccounted for. F-01 is a confirmed editorial
failure, not a residual risk. Actual model routing is unproven and retains its
separate budget/evidence owner. The 31 analyzer-dependent skips do not qualify
the skipped behavior. Current successful package validation does not retroactively
invalidate the previous session's recorded PyYAML limitation.

The user's question about verdict names is an editorial improvement opportunity,
not a second correctness finding: `ACCEPT`, `CHANGES_REQUESTED`, and `INCONCLUSIVE`
are output mechanics already held in the bodies. Descriptions can usually omit
those literals while retaining the job and triggers. No edit was requested or made
as part of this read-only review.

## 9. Completeness and next route

Local discovery is complete, with one finding. Prior discovery's V-01a-FULL pass
is not corroborated by this pass; the other local dispositions were independently
checked above. Prior acceptance remains historical and was not edited.

Next: a separate `task-acceptance-review` decision call consumes this report,
the current scoped diff, brief, verification revision 1, ready preflight, prior
reports, all ledger rows and reviewer regression directions. It determines
the bounded correction route. This discovery does not make that decision or
implement the correction.

## 10. Discovery continuation

```text
Discovery continuation:
- Iteration / bytes: discovery-02; independent of production authorship; HEAD b7b33378de819ec74897f288e28c6f6c0fa386e9; source index == worktree; hashes above and /tmp/side0034-independent/static.json.
- Coverage: V-01a-E/P/N/B/M pass editorially; V-01a-FULL fail (previously pass); V-01a-EXPLICIT-HA fail (new explicit authority-derived row); V-01b-E/P/N/B/FULL, V-01c-E/P/N/B/FULL, V-01d-E/P/N/B/FULL, V-01e-E/P/N/B/FULL pass editorially; V-G5-DIST, V-G6-DIST pass; V-02, V-03-BASE, V-03-MEAS, V-04-SUITES, V-04-LITERALS, V-04-VALIDATE, GATE-ARCH, GATE-CONTRACT pass within stated limits. AGG-VERIFY and AGG-LIVE unchecked by this leaf for the concrete ownership/budget reasons in section 6.
- Findings: F-01 suggested P2, explicit-request high-assurance route contradicted by machine-contract-only description condition.
- Continuity: prior discovery and acceptance claimed all editorial rows passed for the same source bytes. Current independent evidence does not corroborate V-01a-FULL. No prior finding ID existed for this task. Correction owner: bounded implementer after acceptance decision; evidence owner: fresh discovery after correction; authority owner: task brief/plan owner, with no unresolved authority question. Sibling surfaces: explicit high-assurance execute/resume/correct, machine-contract-only activation, ordinary ready package stays guided.
- Preparation/context: brief.md AC-01–03; verification.md revision 1; ready guided preflight.md; SIDE-003 plan Description design and boundary groups 5–6; frozen baseline-measurements.json; SIDE-003.4 results section; prior discovery-01 and acceptance-01; this discovery-02.
- Reviewer regressions: compare candidate profile wording with implementer body lines 19–22; independently evaluate explicit user request with no machine contract, supplied machine contract without explicit request (V-01a-M), and packet alone. Recheck FULL, scalar-only byte masks, exact catalog deltas, owning suites and required architecture/contracts checks after correction; live routing only with separately approved budget.
- Aggregate: python3 tools/verify.py not run, SIDE-003.18 owns it and targeted F-01 prevents a clean aggregate claim; live routing not run, SIDE-003.18/coordinator owns budget and evidence. No new gate added.
- Next: separate task-acceptance-review decision call with this report and complete packaged context; no discovery verdict or advancement.
```
