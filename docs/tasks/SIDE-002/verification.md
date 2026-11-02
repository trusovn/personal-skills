# Verification Design: SIDE-002 — Concise briefs with separate verification detail

Check that task briefs state complete, readable obligations once, and that
verification design derives the cases needed to prove them. Shorter briefs must
preserve preparation, execution, review and split-task responsibilities.

## Shared setup

Use the existing brief-designer and verification-designer eval fixtures as
source authority. Review paired illustrative outputs under the changed source
instructions; retain their source references and a requirement-to-output map in
the task results. Do not rewrite existing task artifacts or refresh `.agents/`.
Source-guided examples demonstrate content coverage and usability; they are not
executed skill evals. Live/model evaluation requires a separately approved budget.

Inspect existing coverage before updating tests or eval expectations. Use the
owning preparation-contract suite and brief-designer package suite first, then
installer coverage if managed resources change, and the aggregate gate required
by the brief. Structural assertions can protect instructions and resources;
they cannot prove generated-document behavior.

## Test cases

### V-01 — A small brief stays complete without a risk section

**Situation:** Use the existing small API/name-change fixture with its approved
success and invalid-input/preserved-name behavior. It needs no additional risk
notes. Produce a compact brief and a derived verification design.

**Expected result:** The brief opens with the result, consumer and purpose.
Scope and critical boundaries remain explicit. Stable, descriptive ACs expose
the independent success and refusal/preservation obligations. Several obligations
use readable bullets or a table; cohesive conditions may use prose. There is no
mandatory direction trace, empty field, repeated requirement or risk block.
Verification still gives concrete success and invalid-input cases with decisive
results and unchanged-state observations. Neither document invents new behavior.

**How to check:** Compare each source obligation with its single authoritative
home and the verification cases. Check that implementation choices, setup and
assertion methods appear only where needed in verification. Read the pair as an
owner and as the next agent. A missing risk section must not cause missing-authority
routing or happy-path-only coverage. Record this as source-guided output review.

### V-02 — Finite resume obligations survive moving detailed proof out of the brief

**Situation:** Use brief-designer eval 5's `finite-risk-matrix` fixture and its
`docs/evidence-plan.md#EVD-12` authority. Preserve every named persisted artifact,
publication stage, legal prefix and contradictory orphan state from that source.

**Action:** Produce a brief and verification design under the changed instructions.

**Expected result:** Acceptance or precise cited authority retains policy,
manifest, attempt record, structured result and closure obligations; execution,
verification, decision and ledger ordering; all five legal prefixes; and the
named contradictory states. Required pre-side-effect refusal, legal byte reuse
and only-next-stage publication remain contract obligations. Essential proof
boundaries may remain concise local notes. Detailed scenario enumeration,
fixtures, observations, evidence reuse, independent probes and gate allocation
have one home in verification. No six-field block or R ID is required in the
brief; any supplied risk IDs remain traceable.

**How to check:** Map the fixture's exact finite values and transitions to ACs
or precise authority and then identifiable verification cases. Check each refusal
reaches its intended guard, has unchanged-state observations, and has a success
control. Inspect first invocation, state change and next invocation where the
source requires lifecycle proof. Keep implementation evidence separate from
fresh independent corroboration. Preserve the authority's final-reviewer
aggregate-gate ownership and targeted-before-aggregate order. Reuse/update the
existing eval rather than replacing these distinct cases with generic prose.

### V-03 — Execution stays actionable and downstream stages can consume the pair

**Situation:** Use the V-01 and V-02 pairs with the current preflight,
implementer, discovery and acceptance instructions and templates.

**Action:** Trace each consumer's required input to the brief, verification or
precise shared workflow reference. Inspect changed source guidance and examples
for fixed-heading or mandatory-risk-row assumptions.

**Expected result:** A consumer can find authority, scope, ACs, necessary evidence
boundaries and task-specific stops without a fixed section inventory or risk
matrix in the brief. Verification supplies detailed cases and evidence mapping.
Execution states status/task kind, the first pending preparation action, four
launch keys and sizing evidence once. It includes task-specific outputs,
consumers, deviations and stops when relevant. It omits repeated next-action
lists, generic status definitions, permission reminders and default report lists.
A precise shared reference supplies the default route: derived verification,
ready preflight, implementation, applicable conditional stages, fresh independent
discovery and a separate acceptance decision, including corrections. A prepared
brief does not authorize implementation.

**How to check:** Record a consumer-to-input map, including scenario evidence
mapping for implementation and complete AC coverage for review. Check reference
targets and conditional stage order, rather than only matching phrases. Preserve
SIDE-001's readable cases, singular source declaration and revision metadata.

### V-04 — Split tasks and high-assurance briefs retain their distinct obligations

| Case | Starting authority and action | Expected result |
|---|---|---|
| V-04a | Use an existing split-task eval with settled producer/consumer boundaries; inspect a composite and every executable child plus its verification design. | Parent requirements map to children; each shared artifact has one owner; dependencies and integration-proof ownership are explicit. Each child is independently understandable, sized and executable after preparation. Detailed proof stays in each owning verification design. The composite remains non-executable and carries no leaf launch metadata. |
| V-04b | Use the existing high-assurance queue-runner eval and inspect a brief/verification pair. | Exact provenance, direction decisions, knowledge/freshness requirements and explicit machine/audit obligations survive where applicable. References replace repeated verification matrices without losing their required contents or consumer access. First run, persisted change, next run, refusal and preservation proof remain identifiable. |

**How to check:** Compare source obligations and current sizing/high-assurance
policy with the paired outputs. Confirm the change does not alter thresholds,
decomposition decisions, freshness semantics or review policy. Record any
missing obligation as a failure, even if the output is shorter.

### V-05 — Verification derives cases but refuses to decide unresolved behavior

**Situation:** Contrast a complete no-risk brief from V-01 with the existing
ambiguous-retention fixture whose deletion policy is unresolved.

**Action:** Apply the changed verification-design guidance to each input.

**Expected result:** The complete brief supports derived material cases without
requiring risk rows. The unresolved expected behavior routes to task design or
the decision owner; no invented retention rule or ready verification artifact
settles the gap. Negative, boundary, lifecycle, preservation and interaction cases
are derived when justified, without speculative catalogs or Cartesian products.

**How to check:** Review both existing eval expectations and source-guided
outcomes. Preserve the ambiguity fixture's unchanged-artifact refusal coverage.

### V-06 — Source, distribution and maintained evidence agree

**Action:** Inspect the changed instructions, template, completion checks,
examples, evals and downstream resources. Inspect the canonical development
installer, focused installer tests, profile guide and README references.

**Expected result:** No active instruction requires detailed six-field risks in
the brief or contradicts the optional structure. Existing distinct coverage
survives revised expectations. Installer-managed references/resources change
only if affected; ownership stays narrow. Existing task artifacts/plans/review
history and the active installation remain untouched. Registry records change
only for an actual registered-authority change.

**How to check:** Run the owning focused suites, applicable installer suite,
`python3 tools/verify.py`, architecture and contract checks (current aggregate
coverage may supply the latter two). Inspect the final diff and report failures,
skips and installation drift. These are structural/local regression results;
report model-generated behavior as unqualified when no approved live eval ran.

## Coverage summary

| Promise from the brief | AC | Required cases |
|---|---|---|
| [Complete readable briefs with one home per fact](brief.md#acceptance) | AC-01 | V-01, V-02, V-04a–b |
| [Independent completion conditions remain visible](brief.md#acceptance) | AC-02 | V-01, V-02, V-04b |
| [Optional risks; detailed proof belongs to verification](brief.md#acceptance) | AC-03 | V-01, V-02 |
| [Derived coverage without new requirements](brief.md#acceptance) | AC-04 | V-01, V-02, V-05 |
| [Actionable execution with preserved stage responsibilities](brief.md#acceptance) | AC-05 | V-03, V-04a–b |
| [Consistent consumers, split/audit forms and evidence](brief.md#acceptance) | AC-06 | V-01–V-06, including V-04a–b |

## Source and revision

Source brief: docs/tasks/SIDE-002/brief.md
Source brief revision: SHA-256 `f92313465887e2aa977056f54991bdb76bcf28e2771c42fe2a4e8eb8f6debdb5`
Verification revision: 1
Authority: derived from SIDE-002 and its cited normative sources; SIDE-001 owns
verification presentation. The historical T-001.3 artifacts are read-only context.
Status: ready
