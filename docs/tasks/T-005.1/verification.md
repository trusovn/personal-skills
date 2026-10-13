# Verification Design: T-005.1 — Supply reproducible qualification inputs

Source brief: docs/tasks/T-005.1/brief.md
Source brief revision: SHA-256 `51c7a380f88cf493dd443b9e66d625609d9f10b8906eb71c723c566aa1a3b67b`
Verification revision: 1
Authority: derived from the task brief and its cited normative sources
Status: ready

This status means the verification design is ready. Dependency acceptance,
current selectors, disposable paths and permissions remain preflight checks.
This file does not establish implementation readiness or qualification.

## Coverage summary

| AC / risk row | Scenarios | Notes |
| --- | --- | --- |
| AC-01 | V-01, V-02, V-05, V-06 | Complete inherited coverage, current owners, reconstructable inputs and truthful evidence levels. |
| AC-02 | V-03, V-04 | Full managed projection, sibling helpers, preservation and fingerprint-excluded drift. |
| AC-03 | V-02, V-05 | Real local controls with decisive results; no inferred agent compliance or unrun pass. |
| AC-04 | V-02, V-06 | Reproducible setup and explicit placeholder replacement without evaluator leakage. |
| S-01 / INV-010 | V-01, V-02, V-05, V-06 | Every listed identity maps to setup/oracle/owner/evidence; representative public-boundary and unrun-handoff reconstruction. |
| S-02 / INV-009/010 | V-03, V-04 | All canonical managed surfaces; independent byte comparison, read-only CLI check and unchanged protected state. |

## Verification scenarios

### V-01 — The inventory reconciles every inherited obligation

Covers: AC-01; S-01 / INV-010

Intent: Reject a plausible-looking inventory that omits a case family, loses an
owner or relies on obsolete selectors and report labels.

Given:
- The brief, parent P-01–P-07 ownership table, T-002.4 and T-003.4 composition
  inputs, applicable INT-FLOW-001 inputs and current test-ownership guide.
- The supplied `fixtures.md`, results and evidence references.

When:
- Reconcile the inventory with those inputs and resolve its setup, oracle,
  owner, producer/consumer and evidence references.

Then:
- Every parent requirement is represented with its owning leaf; this leaf
  supplies P-01 inputs and P-07 evidence distinctions without claiming sibling
  behavior or final ART-012 closure.
- COMP-01–05, INV-CASE-01–24, CCR-01–08, ROUTE-01, FIND-01, ROWS-01,
  REV-01, EFF-01, GATE-01, DISP-01 and applicable INT-FLOW-001 inputs all
  resolve to setup/oracle, owner and existing evidence or an explicit gap.
- Each claimed case identifies command/environment, workspace, authority,
  inherited identity, producer/consumer, owning leaf and evidence level.
- Public, lifecycle, tamper, validator, process-cleanup and continuation
  obligations retain their inherited owners and decisive boundaries.
- Test-owner references use current selectors after TEST-STAB-001. Staged
  reports remain fixture data; historical results are identified as history.

Oracle / boundary:
- Reconcile identities and meaning against the cited inventories and current
  owner declarations. A path or selector that merely exists cannot prove a
  behavioral result. Missing capability or evidence has a reason and next owner.

Variants:
- All finite identities above; do not replace enumeration with a case count.
- Where feasible, omit one mapping in a disposable inventory copy: the audit
  must identify that omission rather than accept the remaining green rows.

### V-02 — Supplied setup reconstructs a public case and an unrun handoff

Covers: AC-01, AC-03, AC-04; S-01 / INV-010

Intent: Reject setup that depends on a previous workspace, absent inputs or a
fabricated producer output.

Given:
- One inherited public-boundary case and one unrun handoff selected from the
  inventory, each with its existing owner and authority-defined oracle.
- Fresh disposable workspaces and the supplied explicit `EVAL_WORK_ROOT`,
  setup commands and prerequisites.

When:
- Reconstruct both starting states using the supplied setup and existing
  `setup_fixture.py <scenario>` entry points where applicable.
- Exercise the public case's available local probe at its inherited boundary;
  reconstruct the unrun handoff's inputs without launching a role call.

Then:
- The resulting Git/filesystem state, task/context inputs, implementations,
  tests and ledgers needed by each selected case are present and identifiable.
- The public probe yields its specified observable result, or records a
  concrete capability gap without a success claim.
- The unrun handoff is reproducible as supplied input, retains its reason and
  owner, and remains unrun as role behavior.
- Existing staging/setup is reused; any added setup is only the missing
  task-local composition setup permitted by the brief.

Oracle / boundary:
- Observe the reconstructed files and Git state plus the public operation's
  actual output/state at its existing filesystem/process/validator boundary.
  Document presence alone does not prove that public operation works.

Variants:
- One inherited public-boundary case and one unrun handoff, as required by S-01;
  this sampling supplements V-01 and does not waive any inventory row.

### V-03 — A fresh installation has full projection and sibling-helper proof

Covers: AC-02; S-02 / INV-009/010

Intent: Reject qualification based only on a workflow fingerprint, partial
package copy or helpers from another installation.

Given:
- A fresh disposable Git target with identifiable unmanaged files/text, and
  the current canonical source profile.
- Recorded before-state for the active installation and protected repository
  bytes, plus the target's unmanaged files and AGENTS text.

When:
- Run the canonical installer on the disposable target, then its `--check`.
- Independently compare the complete managed projection and establish helper
  availability from that target's sibling `.agents/scripts/`.

Then:
- The CLI reports a match and the independent comparison finds identical
  managed bytes and the expected managed file set.
- Receipts identify source revision/current content, target, commands, actual
  results and full comparison scope. Workflow identity is a separate claim.
- Selected packages include references, evals and setup; the profile guide,
  selected shared scripts/config/schema and marked AGENTS block also match.
  Only canonical transient exclusions apply.
- Helpers are available at the target-local boundary. The active installation,
  protected repository bytes and target unmanaged bytes/text are unchanged.

Oracle / boundary:
- Real installer/check CLI outputs and exits; an independent source-to-target
  file-set/byte comparison against canonical declarations, not the check's own
  comparison result; target-local helper availability evidence; before/after
  file/Git snapshots. These establish installation/local availability only.

Variants:
- Every selected managed surface above; reuse inherited Git-journey evidence
  rather than duplicating all T-004 journeys.

### V-04 — Fingerprint-excluded drift invalidates full projection qualification

Covers: AC-02; S-02 / INV-009/010

Intent: Reject a full-match claim that survives an eval/setup change solely
because workflow identity still matches.

Given:
- A disposable target that passed V-03, its retained match receipt and workflow
  identity, and an installed eval/setup file excluded from that fingerprint.

When:
- Change that copied file's bytes in the disposable target only.
- Recheck workflow identity, run canonical `--check` and repeat the independent
  managed comparison, with snapshots around these read-only observations.

Then:
- Workflow identity may still match, but `--check` reports managed drift and
  the independent comparison identifies the changed file.
- The old full-match receipt cannot describe the modified installation as
  current qualified input.
- Checking does not repair the target, mutate Git state or change unmanaged
  bytes. Active installation and source remain unchanged; no temporary fault
  is left in a target presented as qualified.

Oracle / boundary:
- Actual CLI drift result, differing managed bytes, separately observed
  workflow identity and before/after filesystem/Git state. Use the full
  comparison result to judge projection identity.

Variants:
- A copied eval/setup file excluded from workflow fingerprinting, as required
  by the S-02 independent review probe.

### V-05 — Local checks discriminate fixture behavior and preserve evidence limits

Covers: AC-01, AC-03; S-01 / INV-010

Intent: Reject checks that validate only labels/schema, accept the wrong
fixture control or relabel green local tests as observed role compliance.

Given:
- Current owning checks and supplied good/wrong fixture inputs with inherited
  expected oracles. Results distinguish fixture verdict from qualification
  observation and identify the tested bytes and setup.

When:
- Run changed/new inventory checks first, then the focused
  `test_review_composition.py` module using the brief's command.
- At the real boundaries of claimed local behavior, exercise the supplied
  correct input and its wrong control or feasible controlled fault.

Then:
- Correct behavior satisfies its inherited oracle; the wrong control produces
  the contrasting inherited result. Green weak tests alone cannot establish
  that a deliberately wrong implementation satisfies the authority.
- Relevant claimed validator behavior includes valid and targeted-invalid
  instances. Required inputs are supplied, not inferred from metadata.
- Retained results name command, environment/setup, boundary, output identity,
  actual result and owner. Failures, blocked/unchecked rows and stops remain
  visible; an expected CHANGES_REQUESTED verdict is distinct from an eval pass.
- Structural, local-runtime and role-behavior evidence stay distinct. Unrun
  checks and role calls receive no pass claim; temporary faults leave no residue.

Oracle / boundary:
- Actual outputs and state from the existing local operations/probes compared
  with authority-defined expectations, plus retained command/results evidence.
  Text/schema checks prove only their stated structural properties.

Variants:
- Material good/wrong controls for claimed local behavior, including applicable
  validator instances. Reuse current inherited evidence where sufficient;
  this does not require rerunning every isolated case or a whole-repo aggregate.

### V-06 — Handoff instructions preserve provenance and exclude evaluator inputs

Covers: AC-01, AC-04; S-01 / INV-010

Intent: Reject a handoff that treats staged placeholders as actual producer
outputs or exposes the evaluator's answer to the consuming role.

Given:
- The supplied inventory/setup and existing staged producer/consumer records,
  with later owning leaves and separate evaluator material identified.

When:
- Reconstruct the intended consumer input set from supplied setup and inspect
  the instructions for replacing each staged producer placeholder.

Then:
- The instructions identify which raw actual producer output must replace
  which placeholder, with its provenance, preparation references and current
  identities; actual outputs must be retained before grading.
- Staged records are clearly supplied history, never current role results.
  Actual role production/consumption remains with its separately authorized leaf.
- Consumer inputs include necessary authority/context and task evidence but
  exclude evaluator setup code, expected answers and grading oracles.
- Setup and evidence remain task-local within the brief's allowed surfaces.
  No role runner, reusable harness or new policy is introduced.

Oracle / boundary:
- Inspect the assembled consumer-visible inputs and replacement instructions
  against the supplied producer/consumer records. This proves the input
  boundary and usable instructions; it does not prove that a role later follows
  them or that cross-child qualification is complete.

Variants:
- Each claimed staged producer-to-consumer handoff; missing actual output is
  an explicit gap with its owning leaf, never a fabricated observation.

## Implementation handoff

- Treat this file as derived verification guidance, not a replacement for the
  task brief. Obtain ready standalone guided preflight before implementation.
- Preserve stable scenario IDs across a reasoned coverage revision. A revised
  artifact supersedes affected readiness and evidence until focused preflight
  produces a ready result for the new revision.
- Implement the smallest production and test changes that satisfy the brief
  and exercise these scenarios, within its explicit scope. Reuse existing
  staging and inputs; do not repair policy, helpers or the installer here.
- Concrete test structure, framework usage, helpers and file placement remain
  implementation choices unless already fixed by repository authority.
- Follow the brief's sequential targeted-check route. Renew installation-owner
  evidence only when needed; no role/model, live or whole-repo checks are added.
- If implementation discovery shows that a scenario cannot be exercised at its
  stated boundary, route the conflict back to task design/preflight rather than
  silently weakening the oracle. Preserve explicit gaps and their next owners.
