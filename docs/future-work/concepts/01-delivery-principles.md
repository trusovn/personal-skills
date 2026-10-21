# Delivery model — principles and boundaries

**Status:** Future-direction note, 2026-10-12. Not a task plan or authorization to change the current workflow.

## Desired outcome

A lean, trustworthy AI-assisted delivery system where each task has a clear owner and observable outcome; critical system behavior is demonstrated at the appropriate boundary; evidence survives corrections; independent decisions remain independent; and repeatable mechanics can eventually be automated.

## Principles to retain

1. **One source of authority per fact.** Plans own intended cross-task behavior, task briefs own task-local obligations, verification designs own planned proof, preflight owns *current* readiness observations, implementation owns work and reported observations, discovery owns independent findings, acceptance owns disposition, and a future controller owns stage transitions. References do not become competing copies.
2. **Distinguish planned, observed, and accepted.** A test scenario is not a passing test; a passing local fixture is not proof an agent followed a workflow; a commit message or document status is not independent acceptance. Show missing or stale evidence explicitly.
3. **Prevent irreversible harm before action.** The implementer and its environment must enforce ownership of user changes, authorized paths/actions, secrets and destructive-operation boundaries. Independent review cannot undo a leak or overwritten user work.
4. **Make verification adversarial and proportionate.** Define material acceptance criteria and feasible decisive oracles before implementation. An independent reviewer challenges actual effects, including negative and recovery cases, without inventing new requirements or extending scope by preference.
5. **Separate mechanical checks from engineering judgment.** Validate identities, required files, revision matching, allowed change surfaces and declared dependencies with code when practical. Agents interpret ambiguity, consequences and trade-offs; a validator's success does not grant acceptance authority.
6. **Retain durable provenance, not repeated prose.** Preserve unique decisions, issue occurrences, actual checks, reviewed revision identities and failure/unknown states. Present short, role-specific views with links to deeper records.
7. **Optimize the whole workflow.** Judge cost as preparation + implementation + verification + corrections + handoff + future maintenance, not single-prompt tokens or document length. A shorter instruction that increases corrections is a regression.
8. **Prefer incremental, greenfield-friendly changes.** Reuse current project/system information and inspect deeper only where a planned task or material risk requires it. Larger brownfield discovery and elaborate models are conditional needs.

## What each role must know

| Role | Primary job | Must not quietly take over |
|---|---|---|
| Planner / task designer | Outcomes, authority, boundaries, dependencies and acceptance obligations | Runtime observations or private reviewer rules |
| Verification designer | Complete, executable proof intent, negative cases, observable oracles and test ownership | New product requirements |
| Preflight | Can this scope be safely executed **now**, with which commands and current environment? | Rewriting task authority |
| Implementer | Make the authorized change, update existing tests appropriately, show true outcomes and gaps | Accepting its own work or adjudicating deferrals |
| Independent discovery | Inspect actual bytes, probe effects, surface findings and incomplete proof | Final disposition |
| Independent acceptance | Admit current evidence, judge materiality and decide advancement/deferral | Silent fixer, bulk rediscovery, portfolio planner |
| Future controller | Invoke stages, validate machine contracts, retain state and route authorized continuation | Semantic acceptance or reviewer independence |

These are responsibility boundaries, not a mandate to create a file or agent for each row.

## Decisions and authority

The `t-o-new-flow` delivery documents were retired; their historical identities and qualification limits remain in the [archive](../../../README.md#archived-delivery-documents). Current source skills, repository rules and authorized task contracts govern new work. This portfolio and its concept notes are **proposals**, not amendments. Current executable packages continue to require their specified preparation and verification artifacts. The independent plan reviewer should not edit the plan it certifies; a derived read model may report whether an acceptance decision still matches current artifact identities.

## General promotion rule for future ideas

Move from concept → pilot → authorized change only when there is (a) a real missing outcome or cost problem; (b) a named current owner and non-overlapping edit scope; (c) one decisive, independently checkable success/failure case; and (d) a comparison with the simpler existing approach. Record both the benefit and any newly introduced maintenance or safety burden.

**Not goals:** a mandatory agent at every step, a giant universal schema, automatic acceptance from green checks, exhaustive scenario quotas, or replacing current accepted contracts while another task is implementing them.
