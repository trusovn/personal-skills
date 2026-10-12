# Documentation and planning — direction

**Covers:** `D-01`–`D-07`, `Q-03`–`Q-05`. **Status:** Design hypotheses and candidates; no binding template change.

## Problem and desired outcome

Existing outputs are thorough but repeatedly restate the same policy, authority and task facts across plans, machine maps, briefs, verification specifications, preflights, results and reviews. At one audited revision, 47 generated files occupied roughly 608 KB; this is an illustrative documentation footprint, **not** measured token spend or failure rate.

The target is **less independent narrative, faster correct retrieval and unchanged or better correctness**. A person should quickly see current outcome, blockers, gaps and next owner. An agent should load the authority relevant to its role, then expand only the contested evidence. Every fact still has a verifiable source.

## Documentation capabilities

**D-01 — Clarify authority and role responsibility first.** Assign a single writer to each normative obligation, current observation and review verdict; define reference/derivation rules. Keep a small preventive execution-safety contract while moving adversarial review instructions to reviewers and transition mechanics to a future controller. This is primarily a responsibility map, not another skill or lengthy document.

**D-02 — Compare lean formats experimentally.** Using complex previously completed task packages and one small task, let independent agents answer the same questions from existing vs simplified representations. Measure correct scope, all ACs, decisive oracles, negative cases, stale-evidence decisions, next stage and unrun gaps; include adversarial omissions or stale links. Track complete workflow cost and correction rate, not just document length.

**D-03 — Adopt concise, stage-specific records only on evidence.** Briefs state unique task contracts. Verification designs keep AC→scenario identity and decisive setup/action/oracle/variants. Preflight records *new current-state facts* rather than repeating the brief or a full implementer handoff. Discovery records independent observed evidence and findings; acceptance cites discovery and records its own admission/verdict. Logs and large audit maps stay retrievable as evidence attachments rather than disappearing.

**D-04 — Normalize plan and machine-map ownership.** The plan must retain critical flows, decisions, interface ownership, invariants and system-proof ownership. Avoid separately maintaining long Markdown descriptions and JSON essays of the same contract. Decide which representation is normative before transforming it; prefer compact ID edges and generated or validated views. Do not implement a large universal registry merely for tidy data.

**D-05 — Derived status and navigation.** Build a read-only human view of accepted/current/blocked/unknown, recent changes, proof gaps and next owner from *actual* reports, identifiers and runtime observations where available. Do not make the static task index a competing state tracker, claim accepted from file existence or alter plan bytes during review.

**D-06 — Context extraction by role.** Given task/stage and canonical identity, retrieve only applicable contracts, evidence deltas, dependency boundaries and safety guards. Follow stable references for unusual cases. Optimize retrieval precision and recency before proposing another summarizing agent.

**D-07 — Mechanical validation.** Enforce objective source/digest/reference matching, mandatory coverage links, manifest completeness, allowed file changes and contract-compatible handoffs when reliable inputs exist. Passing a structural validator never proves behavior or reviewer independence.

## Planning and decomposition capabilities

**Q-03 — Improve task-boundary decisions.** Preserve the already introduced rule that size thresholds trigger judgment rather than automatic splitting. Make `keep whole because coupled`, `keep whole because coordination overhead dominates`, and `must split because of hard limits` distinguishable. Record why a selected split has stable ownership. Test agents on adverse examples where the correct partition is *not* supplied in the prompt.

**Q-04 — Settle shared decisions before independent task briefs.** Project planning should identify when related top-level tasks need a common interface, data, ownership or system-proof decision before briefing separately. Most briefs should be produced just in time as predecessor interfaces become real. This does not require a dedicated coordination skill.

**Q-05 — Progressive detail and calibration if observed need.** For decomposed parents, keep the child/dependency/coverage skeleton without freezing all executable detail for distant children. Elaborate a child when it becomes ready. Calibrate split judgment against actual rework, shared-file churn, repeated review and handoff costs; postpone any new schema until necessary.

## Deliberate limits and decision gates

- Do not shorten away authority, required evidence, negative tests, real boundaries, reviewed revision identities or valid independent decisions.
- Do not merge currently mandatory verification and preflight artifacts without a new explicit decision. A slim view can still reference distinct source records.
- Do not assume short skills are cheaper overall. Compare total implementation → discovery → acceptance → correction effort.
- Do not edit accepted templates/flows concurrently with active tasks owning those surfaces.
- Adopt D-03/D-04 only after D-01's source ownership and D-02's fidelity/cost evidence support them.

**A successful redesign** makes routine navigation substantially easier while independent agents still reject a planted stale reference, missing negative scenario and unauthorized write as reliably as before.
