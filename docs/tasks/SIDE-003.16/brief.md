# Task Brief: SIDE-003.16 — Conditional loading for foundation and review skills

## Outcome

architecture-guardrails, foundation-readiness-review, project-direction, and
project-plan-verification load only what their flows need. Every
workflow-participating reference has an explicit when-to-read condition and
timing in its `SKILL.md`; genuinely conditional sections are extracted into
references where safely separable, or the per-skill decision is a justified
no-op recorded with reason; a reference established as background or unused
gains no new mandatory read — its disposition is recorded instead. Behavior
is unchanged; per-skill instruction maps and measured deltas are recorded in
this leaf's section of `docs/tasks/SIDE-003/rollout-results.md`.

## Authority and scope

| Item | Contract |
|---|---|
| Authority | [SIDE-003 plan](../SIDE-003/plan.md), "Body design and mandatory loading" (conditional extraction, no invented profiles, near-universal material stays inline, missing-reference rule), "Delivery sequence" phase 4, "Measurement and decision rules" layer 2; owner instruction (2026-11-03): clear when-to-read instructions are the acceptance center, and safe extraction is allowed rather than deferred; [parent brief](../SIDE-003/brief.md) |
| Dependencies | SIDE-003.1–.6 complete (baseline, route inventories, and these skills' descriptions final) |
| Allowed changes | The four packages' `SKILL.md` bodies, their `references/` (new and existing), their `evals/` inputs, owning test expectations that assert their text, and this leaf's section in `rollout-results.md` |
| Read-only context | The SIDE-003.1 read graph and route inventories; architecture-guardrails: `enforcement-model.md` plus four language guides; foundation-readiness-review: `delivery-routing.md`; project-direction: `direction-template.md`; project-plan-verification: `plan-verification-report-template.md` and `review-checklist.md`; `skills/senior-code-review/SKILL.md` (the mandatory-read pattern); `tests/test_install_development_skills.py` (asserts architecture-guardrails `SKILL.md` text); `docs/contracts/measurement.json` (declares architecture-guardrails `SKILL.md`) |
| Out of scope | The `description` frontmatter (compressed in SIDE-003.2/SIDE-003.3 — do not change); any behavior change; deleting or renaming existing references; `skills/architecture-guardrails/templates/gates.yaml` (a declared asset, not a reference); other skills; the active `.agents/` installation; introducing mandatory reads for resources established as background or unused |
| Assumptions / unresolved | `project-plan-verification/references/review-checklist.md`'s existing purpose is UNKNOWN — establish it first (mentions, tests, evals, package history) and record its disposition; do not add a workflow read for it merely because the file exists |

## Work and acceptance criteria

Required work:

1. Per skill, freeze a proportionate obligation inventory (scope rules, gates,
   output requirements, stop rules) with current authority locations,
   recorded in the rollout-results section.
2. Enumerate every owned reference and establish its existing purpose first
   (`SKILL.md` mentions, tests, evals, package history). Add explicit read
   conditions and timing only for references that participate in a workflow;
   replace vague pointers ("See `references/…`", "Use `references/…`") with
   conditions; record the disposition of background or unused resources
   instead of adding reads.
3. Where genuinely conditional sections exist, extract them into
   `references/` files with explicit conditions and timing (safe
   extraction); otherwise record a justified no-op. Keep near-universal
   material inline; do not invent profiles.
4. State the missing-reference rule where references exist after this work:
   a required reference that is missing or unreadable stops the affected
   action with the exact gap reported; no inferred bypass. Do not read every
   reference at startup.
5. Update owning assertions: behavior-preservation assertions pass unchanged
   before and after the edit; new loading-structure assertions (condition
   presence, reference existence, relocated obligations) reject the pre-edit
   layout.
6. Record per reference: condition and timing, verified-or-clarified status;
   per skill: extraction or no-op decision with reason, instruction map for
   any moved obligation, and the measured delta (entry-only and route sums,
   before/after, from the SIDE-003.1 baseline record's file table and route
   inventories).

- **AC-01:** Every workflow-participating reference of the four skills has an
  explicit when-to-read condition and timing reachable from its `SKILL.md`;
  dispositions are recorded for background or unused resources; no read is
  introduced merely because a file exists.
- **AC-02:** No behavior change; for any extraction, the instruction map
  covers every moved obligation, behavior-preservation assertions pass
  unchanged before and after the edit, and new loading-structure assertions
  reject the pre-edit layout; conditions match actual applicability, and the
  measurement-contract-declared authority of architecture-guardrails'
  `SKILL.md` is not altered in meaning; installer-suite assertions quoting
  changed lines are synced in the same change.
- **AC-03:** This leaf's `rollout-results.md` section records per-reference
  results, per-skill extraction/no-op decisions with reasons, instruction maps
  for moved obligations, and measured deltas; the description frontmatter is
  unchanged.

## Verification

| Evidence | Scenario and oracle | Command |
|---|---|---|
| Fail-first | New loading-structure assertions (condition presence; reference existence where added or moved) reject the pre-edit layout; behavior-preservation assertions pass unchanged before and after; where references were added or moved, removing one required link or bypassing one route in a disposable candidate is detected by the relevant check | derived verification owns the concrete fixture/command pair |
| Targeted | Per-reference condition matches actual applicability (the reviewer probes one condition per skill against its workflow); measured deltas reproduce from the SIDE-003.1 record | read of the four `SKILL.md` files plus the SIDE-003.1 record |
| Owning suite | Assertions quoting changed lines, from the SIDE-003.1 prerequisites map (the installer suite reads architecture-guardrails) | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py` |
| Broader gate | Aggregate gate and disposable-install reference resolution at SIDE-003.18 (these four skills are profile members); live behavioral qualification only with separately approved budget, else recorded pending | SIDE-003.18 |

## Execution

Status: `ready`; task kind: `executable`; guided profile.
Readiness route: standalone guided preflight after derived verification —
confirm the current read graph, route inventories, and description-phase
state of the four files.
Verification-design recommendation: separate — obligation-preservation
coverage applies wherever extraction happens; the derived verification also
owns the per-reference applicability probes and the background/unused
disposition checks.

```yaml
agent_tier: standard
reasoning: high
review: immediate
budget: 18 tool calls / 50 minutes / four packages, conditions, possible extraction, results section
```

Sizing: `default@1`; estimate 16 implementation calls / 45 minutes;
confidence medium; triggered `max_agent_calls` and `max_duration_minutes`.
Decomposition override: `cannot_split_safely` — candidate boundary
(architecture-guardrails as its own leaf plus a three-skill remainder)
rejected: per-skill micro-leaves of roughly 3–5 calls would multiply
preparation and review stages for units that share one results section, one
measurement basis, and — for architecture-guardrails — the same
installer-suite and contract-record surfaces. Residual risk: scope discovery
on architecture-guardrails; mitigated by the proportionate obligation
inventory, staged commits, and the immediate fresh review.

Stops: a reference whose purpose or correct condition cannot be established
without a policy decision (stop and report); an obligation that cannot be
preserved by extraction (stop; do not delete it to shrink bytes); a cluster
genuinely needing deeper restructuring than this leaf's scope (record and
route back through the parent); behavior changes (never); profile drift in
the active installation (report, do not fix).

Next action: derive `verification.md`, obtain a ready `preflight.md` through
standalone guided preflight, then implement.
Required follow-on: immediately after implementation or correction and any
applicable conditional stages, hand the completed bytes to a fresh independent
`task-review-discovery` call, and hand its report to a separate
`task-acceptance-review` decision.

Expected contract impact: `docs/contracts/measurement.json` declares
architecture-guardrails' `SKILL.md` for foundation-native-and-advisory-
discovery and native-check-policy-discovery; if extraction moves declared
authority text, synchronize that record through this leaf's designated
`task-contract-registry-updater` stage with the explicit `--write-index`
command, in the same change. Behavior is unchanged, so summaries and
invariants are preserved, not rewritten. Otherwise record no registry change.