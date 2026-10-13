# Verification Design: T-004.3 — Prove explicit refresh and distribution closure

Source brief: docs/tasks/T-004.3/brief.md
Source brief revision: SHA-256 bdf0c28a9184c72438b69466046a7eece5971b34b30adf33e28f244adcdc4098
Verification revision: 1
Authority: derived from the task brief and its cited normative sources
Status: ready

Paths in this artifact are repository-relative. Ready describes this design;
it does not certify dependency completion or implementation readiness.

## Coverage summary

| AC / risk row | Scenarios | Notes |
|---|---|---|
| AC-01 | V-01 | Both Git states cross the complete ordered journey; checks cannot repair drift. Detached compatibility remains .1 evidence. |
| AC-02 | V-02 | Representative managed families, changed/missing bytes and an owned extra; independent final projection inspection. |
| AC-03 | V-03, V-04 | Exact unmanaged preservation and marker singularity; retain malformed/unsafe refusal evidence. |
| AC-04 | V-05 | Selection, guide, helpers, tests and three READMEs agree with the consumed install/check interface and scope limits. |
| AC-05 | V-06 | Reproducible observations and installed identities reach T-005 with explicit qualification gaps. |
| R-01 / INV-009 | V-01, V-02 | Real CLI occurrences, Git/check snapshots and source-to-installed byte comparison. |
| R-02 / INV-009 | V-03, V-04 | First insertion versus existing block; byte preservation and unchanged refusal boundaries. |

## Verification scenarios

### V-01 — Drift persists until a separate explicit refresh

Covers: AC-01; R-01

Intent: Reject a checker that repairs drift, a refresh tested without the prior
drift occurrence, or an unborn fixture made committed during the journey.

Given:
- Disposable real Git targets: one initialized without any commit and one with
  an ordinary baseline commit. The source distribution is fixed for the journey.
- The canonical installer and the .2 check interface are available. This run's
  active `.agents/` installation is never a target.

When:
- In each target, call the positional installer, check the fresh installation,
  introduce controlled managed drift, check that drift, explicitly rerun the
  installer, recheck, and perform a second matching check, in that order.
- Capture source/target path, type and byte snapshots, including target Git
  metadata and evidence storage, immediately before and after each check.

Then:
- Both install calls succeed. The fresh, restored and second restored checks
  exit 0 with `match: true` and empty `differences`.
- The drift check exits 1 with `match: false` and the expected changed, missing
  or unexpected managed paths. The deliberate drift still exists afterwards.
- Every check leaves the captured state unchanged. Only the separate installer
  rerun repairs managed drift.
- The two restored checks agree on the JSON result for unchanged inputs.
- The unborn target has no resolvable HEAD commit throughout the journey and
  still has its unborn branch state; no commit identity is fabricated.

Oracle / boundary:
- Real canonical CLI exit status, stdout/stderr and filesystem/Git observations
  at each milestone. A final green result alone cannot prove the intermediate
  drift, absence of writes or explicit refresh requirement.

Variants:
- Genuine unborn and ordinary committed targets, each with the complete journey.
- V-02 supplies the controlled managed drift; the same occurrences can also
  carry V-03's preservation sentinels.

### V-02 — Refresh restores the managed projection across file families

Covers: AC-02; R-01

Intent: Reject restoration of only SKILL.md or fingerprint-covered content,
partial package copying, or a false matching check that overlooks owned extras.

Given:
- A freshly installed disposable target with an independently recorded current
  source projection: selected package files under the installer's transient
  exclusions, profile guide, explicit shared files and expected managed block.
- Representative files exist in each family below. The package cases include
  reference, eval and setup/fixture content that is actually copied by install.

When:
- Change or remove owned content across the families, and add a non-transient
  extra file inside a selected skill directory.
- Observe the real drift check, perform explicit installer rerun, and inspect
  the installed projection independently before relying on the matching recheck.

Then:
- The drift output names the actual changed/missing files and owned extra.
- Every changed or missing representative is restored to current source bytes;
  the managed block equals its current expected content and the extra is absent.
- The complete final installed managed path set and bytes agree with the source
  projection, including files outside workflow fingerprint coverage. That
  independent result agrees with the matching check output.

Oracle / boundary:
- Real install/check calls plus an independent enumeration and byte comparison
  of the final managed projection. A check's own `match` flag or a workflow
  fingerprint alone is insufficient.

Variants:
- Selected skill definition; reference; eval; setup/fixture; profile guide;
  shared helper; shared config; shared schema; marked AGENTS block; owned extra.
- Assign changed and missing representatives across file families, with both
  states exercised overall; do not multiply every state by every family or
  repeat .2's isolated comparator matrix. Use changed valid block content to
  keep this restoration case separate from V-04's malformed-marker refusal.
- Fresh discovery's R-01 probe independently deletes a managed reference and
  adds an owned extra, then observes drift, refresh and matching recheck.

### V-03 — Unmanaged bytes survive insertion and refresh

Covers: AC-03; R-02

Intent: Reject blanket replacement of `.agents/`, loss of unrelated project
files, or normalization of instructions outside an existing managed block.

Given:
- A disposable target contains an unselected local skill and its reference, a
  non-managed helper, other project files and original AGENTS instructions.
- For the existing-block case, record the bytes before the begin marker and
  after the end marker, including deliberate outside-block whitespace.

When:
- Install into a target without a block, inspect retention of original text,
  then introduce managed drift and refresh.
- Refresh a target with an existing valid block and recorded outside-block
  bytes. Inspect unmanaged state after each relevant install/refresh.

Then:
- Unselected skill/reference, helper and other project-file bytes are unchanged.
- First insertion retains the original instruction text. Refresh with an
  existing block preserves the prefix and suffix bytes exactly.
- Each successful insertion or refresh leaves exactly one begin marker and
  one end marker. The final check matches despite the unmanaged content.

Oracle / boundary:
- Before/after file bytes and separately compared outside-block byte segments,
  plus marker counts and the real matching check. Text-presence assertions
  alone cannot establish existing-block byte preservation.

Variants:
- First insertion and existing-block refresh. Reuse V-01's targets where useful.
- Fresh discovery's R-02 probe adds outside-block whitespace and an unmanaged
  helper before refresh and verifies exact preservation afterwards.

### V-04 — Refresh preserves the existing refusal boundary

Covers: AC-03; R-02

Intent: Reject silently repairing malformed markers or replacing an unsafe
target as though it were ordinary managed drift.

Given:
- Existing installer/check refusal fixtures provide malformed or ambiguous
  markers and unsafe target path shapes, with pre-action state recorded.

When:
- Exercise the applicable existing canonical install/check refusal cases
  against the completed .3 bytes.

Then:
- Inputs remain refused with their established diagnostics and failure
  semantics; the target is not silently repaired or overwritten.
- Protected target/outside state remains unchanged under the existing refusal
  contract. Missing ordinary owned files remain V-02 restoration cases.

Oracle / boundary:
- Retained behavioral refusal tests and their filesystem snapshots; inspect
  current evidence rather than replacing these cases with wording assertions.

Variants:
- Existing malformed/ambiguous-marker and unsafe-path cases; no new refusal
  policy or duplicated .2 fixture matrix.

### V-05 — Distribution guidance describes the implemented interface

Covers: AC-04

Intent: Reject stale profile selection or instructions that imply checking
updates installations, fingerprint equality proves profile equality, or source
edits automatically refresh an active invocation.

Given:
- Current `DEVELOPMENT_SKILL_SOURCES`, `PROFILE_SKILLS_README` and
  `SHARED_SCRIPT_FILES`, focused installer expectations, root README,
  `skills/README.md` and task-flow README are available for scoped comparison.
- .1 identity/compatibility and .2 CLI contracts are consumed, not redesigned.

When:
- Reconcile selected packages and helper dependencies with the installed guide
  and focused tests. Compare install/check/result/refresh instructions in all
  three READMEs with actual V-01/V-02 observations.
- Inspect applicable current .1 fingerprint and detached-compatibility evidence.

Then:
- Selected packages, installed guide and managed helper/config/schema files
  agree with the canonical selection and focused expectations.
- Guidance preserves positional install syntax and uses `--check <target>` for
  read-only comparison: exit 0 is match, 1 is drift/missing installation, and
  2 is inspection failure, which cannot be reported as match.
- Documented refresh is a separate installer rerun between invocations.
  Selection and ownership remain narrow and fingerprint framing stays compatible.
- Guidance makes no claim of full unborn collector lifecycle support, retained
  active-run versions or skill-call/model qualification from filesystem checks.

Oracle / boundary:
- Scoped source/guide/test reconciliation backed by real CLI evidence and
  applicable identity regression evidence. Documentation assertions establish
  distribution consistency, not semantic agent behavior.

Variants:
- Root, profile and task-flow READMEs; package/guide/shared-file selection.
- Existing .1 detached/fingerprint proof is reused only while applicable to
  completed bytes; preflight resolves current evidence and commands.

### V-06 — Results provide reproducible proof and a bounded T-005 handoff

Covers: AC-05

Intent: Reject a results file that records only green summaries, omits installed
identity, or presents filesystem qualification as observed skill-call behavior.

Given:
- Completed V-01–V-05 observations and current dependency evidence are available.
- The task writes a new `docs/tasks/T-004.3/results.md`; existing plans and
  historical reports remain read-only.

When:
- Inspect the results against the actual supplied setup, commands/probes,
  captured outputs and independently inspected installed projection.

Then:
- Results specify reproducible unborn/committed starting states, exact CLI and
  probes, observed statuses/results, deliberate mutations and recovery, and
  installed package/helper identity evidence tied to the source used.
- The handoff supplies the qualified ART-010 projection and ART-011 check
  interface, states the remaining T-005 qualification gaps and distinguishes
  filesystem/Git proof from unrun skill-call/model behavior.
- No unrun, stale or fabricated evidence is presented as completed proof.

Oracle / boundary:
- Evidence audit from each claim to its runnable setup and observed output;
  installed identities are inspected through the consumed distribution/identity
  boundaries. A schema-valid report alone cannot prove any behavioral claim.

Variants:
- Both Git states; proved local behavior versus explicitly unrun qualification.

## Execution ownership and commands

- Preflight confirms current reviewed .1/.2 outputs, exact CLI applicability and
  focused selectors. This design does not authenticate historical submissions.
- Canonical calls, with paths resolved for disposable targets:
  `python3 /path/to/personal-skills/scripts/install_development_skills.py <target>`
  and `python3 /path/to/personal-skills/scripts/install_development_skills.py --check <target>`.
- Implementer: targeted lifecycle/preservation cases first, then the owning
  installer suite:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py`.
  Reuse/consolidate rerun and .2 family/snapshot coverage. Controlled drift must
  demonstrate detection before restoration; if preservation requires a repair,
  record its fail-first regression before editing production bytes.
- Fresh discovery: independent R-01/R-02 probes, then one justified final
  aggregate after required targeted evidence is clean, including corrections:
  `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_install_development_skills test_workflow_version test_run_evidence`.
  This exact union follows the existing .1 distribution aggregate and .3's named
  installer/workflow-version/run-evidence scope. Acceptance consumes its current
  evidence and does not duplicate the aggregate.
- No whole-repository, network, model-budget or role-call qualification is
  required here. Concrete execution readiness belongs to preflight.

## Implementation handoff

- Treat this file as derived verification guidance, not a replacement for the
  task brief. Obtain ready standalone guided preflight before implementation.
- Preserve stable scenario IDs across a reasoned coverage revision. A revised
  artifact supersedes affected readiness and evidence until focused preflight
  produces a ready result for the new revision.
- Implement the smallest production and test changes that satisfy the brief and
  exercise these scenarios; add no shared harness or agent-role runner.
- Concrete test structure, framework usage, helpers and file placement remain
  implementation choices unless already fixed by repository authority.
- If a scenario cannot be exercised at its stated boundary, route the conflict
  to task design/preflight rather than silently weakening the oracle. Broader
  identity/check defects return to their owning leaf.
- After implementation/correction, follow the brief's applicable conditional
  stages, fresh independent discovery and separate acceptance decision. T-005
  qualification and coordinator advancement remain separate work.
