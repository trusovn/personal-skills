# Stage 3 Retrieval Surface Follow-up

Status: current planning companion and deferred-work register

Date: 2026-07-23

Governing plan: [stage-3-mvp-rebaseline.md](stage-3-mvp-rebaseline.md)

## Purpose

This document preserves information-architecture work that should influence
later Stage 3 task actualization without changing the MVP ordering, runtime
contracts, or exit criteria. The governing rebaseline remains authoritative.

The pre-brief stabilization corrected the current operating route, added a
one-hop index and architecture map, supplied minimal current inputs, separated
current references from history, fixed the current broken link, and added
retrieval-focused eval definitions. These are planning-safety corrections, not
an additional MVP increment.

## Complete only when the owning behavior exists

MVP-6 should:

- replace the current controller-only operator guide with the final
  profile-driven prepare, confirm, start, continue, and escalation flow;
- update `SKILL.md` only after the corresponding public commands and structured
  outcomes exist;
- add examples for versioned workflow profiles and plan preparation;
- keep the final operator path one hop from `SKILL.md`;
- label each surviving current document as normative contract, operator
  reference, current plan, decision record, or historical evidence; and
- forward-run the retrieval evals against the finished skill, including “start
  a run,” “resume an interrupted attempt,” and “change Git drift detection.”

The MVP-6 brief should treat the present references as transitional current
truth, not as the final file layout.

## Decide after the MVP flow is stable

Consider, but do not make prerequisite:

- moving stable runtime contracts from `docs/` into `references/`;
- grouping evolution material under `docs/plans/` and `docs/decisions/`;
- fixing archival links that are not reachable from the current surface;
- converting `scripts/` into a normal importable Python package;
- replacing dynamic imports and compatibility re-exports;
- splitting large source files if pilot evidence shows navigation or ownership
  remains unclear; and
- adding broader search tooling that excludes history by default.

These changes should be justified by retrieval or maintenance evidence after
the end-to-end flow exists. They must not delay MVP-2 through MVP-5.

## Later-work guardrails

- Keep `docs/history/` opt-in and non-authoritative.
- Do not document commands before they exist and pass behavioral verification.
- Preserve controller ownership of state, Git evidence, permissions, recovery,
  and closure.
- Keep source-to-test ownership and canonical verification commands current.
- Prefer small moves with link checks over a single repository-wide
  reorganization.
- Record completed work beside the governing plan rather than rewriting
  historical plans or task briefs.
