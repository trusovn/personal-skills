# Task Brief: SIDE-003.14 — Restructure repo-foundation for conditional loading

## Outcome

`skills/repo-foundation` loads only the instructions the task at hand needs.
Scenario-conditional material — contract-registry mechanics, schema
consultation, ADR/module-doc guidance — moves into package references where
safely separable, each with an explicit when-to-read condition and timing; the
entry file keeps the placement rules, canonical commands, and a reference
loading table. Every preserved obligation is mapped old→new; behavior is
unchanged.

## Authority and scope

| Item | Contract |
|---|---|
| Authority | [SIDE-003 plan](../SIDE-003/plan.md), "Body design and mandatory loading", "Delivery sequence" phase 4 (inspect larger packages), "Measurement and decision rules" layer 2; owner adjustment (2026-11-03): figure the exact split places; clear when-to-read instructions are the acceptance center |
| Dependencies | SIDE-003.1–.6 complete (baseline + this skill's description final) |
| Allowed changes | This package's `SKILL.md` body, its `references/` (`contract-registry.md`, `contract-index.schema.json`, `subsystem-contract.schema.json`, new files), its `evals/` inputs, owning test expectations that assert its text, and this skill's section in `docs/tasks/SIDE-003/rollout-results.md` |
| Read-only context | The SIDE-003.1 baseline and read graph; `tests/test_install_development_skills.py` (asserts this `SKILL.md`'s text); `docs/contracts/measurement.json` (declares this `SKILL.md` for foundation-native-and-advisory-discovery and native-check-policy-discovery); `skills/architecture-guardrails/templates/gates.yaml` is another skill's asset — do not touch |
| Out of scope | The `description` frontmatter (compressed in SIDE-003.2 — do not change); any behavior change to placement rules, registry policy, or command guidance; renaming or moving the package; other skills; the active `.agents/` installation |
| Assumptions / unresolved | The exact conditional clusters are this leaf's design work; the schema files are data references — their loading condition is when an agent composes or edits records against them, and that condition must be explicit too |

## Work and acceptance criteria

Required work:

1. Before any edit, freeze the obligation inventory in the rollout-results
   section: every placement rule, command guidance rule, registry-policy
   rule, and stop/route rule in the current entry file, each with its current
   authority location.
2. Identify the actual conditional paths (registry mechanics and inclusion
   threshold; schema consultation when composing/editing records; ADR and
   module-doc workflows). The placement and command core stays inline. Do
   not invent profiles the skill lacks.
3. Extract qualifying clusters into `references/` files; give every reference —
   new and existing — an explicit read condition and timing in the entry file
   (`contract-registry.md` currently sits behind "Use … for the registry
   model" — replace vague pointers with explicit conditions and timing);
   keep near-universal material inline.
4. State the missing-reference rule: a required reference that is missing or
   unreadable stops the affected action with the exact gap reported; no
   inferred bypass. Do not read every reference at startup.
5. Update the owning assertions to assert the applicable instruction closure
   and required route rather than deleted literal text. Preserve distinct
   existing scenarios; extend fixtures only for missing loading-condition
   cases.
6. Record the instruction map (each old obligation → new location, loading
   condition, proving scenario), the per-route measured cost (entry-only and
   cumulative, before/after, from the SIDE-003.1 baseline record's file table
   and route inventories), and any no-op
   decisions with reasons.

- **AC-01:** Every reference this package owns has an explicit when-to-read
  condition and timing in the entry file; a reader following only the entry
  file knows, before each dependent action, whether a reference applies.
- **AC-02:** The instruction map covers every obligation from the pre-edit
  inventory; no placement, registry, or command obligation is lost or
  weakened; behavior-preservation fixtures pass unchanged before and
  after the edit; only the new loading-structure assertions (reference
  existence, explicit conditions, relocated obligations) reject the pre-edit
  layout and pass after; installer-suite assertions on this file are updated in the
  same change.
- **AC-03:** Entry-only and per-route cumulative costs are recorded
  before/after; a route that did not shrink is explained, not hidden; the
  description frontmatter is unchanged.

## Verification

| Evidence | Scenario and oracle | Command |
|---|---|---|
| Fail-first | Behavior-preservation fixtures pass unchanged against the pre-edit bytes; the new loading-structure assertions (reference existence, explicit conditions, relocated obligations) reject the pre-edit layout; in a disposable candidate, removing one required link or bypassing one route is detected by the relevant check | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py` |
| Targeted | Placement/registry behavior in the existing fixtures and evals is unchanged | the package's `evals/` inputs plus the installer suite above |
| Owning suite | Installer-suite assertions on this `SKILL.md` (whole-package copying and quoted-text assertions) | as above |
| Broader gate | Aggregate gate and disposable-install reference resolution at SIDE-003.18; live behavioral qualification only with separately approved budget, else recorded pending | SIDE-003.18 |

## Execution

Status: `ready`; task kind: `executable`; guided profile.
Readiness route: standalone guided preflight after derived verification —
confirm the current assertion inventory and that SIDE-003.2's description for
this skill is final before edits.
Verification-design recommendation: separate — obligation-preservation
coverage across relocation and the registry/schema condition split need
designed scenarios.

```yaml
agent_tier: standard
reasoning: high
review: immediate
budget: 17 tool calls / 50 minutes / one-package restructuring with obligation map and closure tests
```

Sizing: `default@1`; estimate 15 implementation calls / 45 minutes;
confidence medium; triggered `max_duration_minutes`.
Decomposition override: `cannot_split_safely` — candidate boundary (registry
mechanics vs placement-core extraction) rejected: one entry file plus shared
suites; both stages would re-edit the same placement contract and renegotiate
the same loading table. Residual risk: a longer single leaf, mitigated by the
pre-edit obligation inventory, staged commits, and the immediate fresh review.

Stops: an obligation that cannot be preserved by extraction (stop; do not
delete it to shrink bytes); any behavior change to placement or registry
policy (route back through the parent); profile drift in the active
installation (report, do not fix); missing live-eval budget (report
qualification pending).

Next action: derive `verification.md`, obtain a ready `preflight.md` through
standalone guided preflight, then implement.
Required follow-on: immediately after implementation or correction and any
applicable conditional stages, hand the completed bytes to a fresh independent
`task-review-discovery` call, and hand its report to a separate
`task-acceptance-review` decision.

Expected contract impact: `docs/contracts/measurement.json` declares this
package's `SKILL.md` for foundation-native-and-advisory-discovery and
native-check-policy-discovery; extraction is expected to move declared
authority text into new reference paths. Synchronize that record through this
leaf's designated `task-contract-registry-updater` stage with the explicit
`--write-index` command, in the same change. Behavior is unchanged, so
summaries and invariants are preserved, not rewritten.