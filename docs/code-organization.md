# Code organization policy

This policy governs new and materially changed production code, tests, evals,
fixtures and harnesses. The [project map](project-map.md) and relevant subsystem
maps, including the [orchestrator map](../skills/task-orchestrator/references/architecture-map.md),
describe current ownership; this policy does not authorize unrelated legacy cleanup.

## Required rules

Before structural additions or material growth, briefly explain the responsibility
owner, proposed placement and dependency changes. Apply these rules to the affected
cluster and its collaborators; explain any exception with a concrete reason.
Material unresolved architecture or scope decisions return to the owner.

1. **Group by responsibility.** Keep behavior together when it owns one
   coherent concern and changes for related reasons. Use concern names such as
   `acceptance` or `candidate_checks`; do not introduce generic `utils` or
   `helpers` dumping grounds or arbitrary halves of a file. An existing large
   file is not the default owner of a new responsibility. Small private helpers
   that serve their enclosing concern belong there.
2. **Encapsulate through modules.** Expose a small set of named operations and
   keep implementation helpers internal. Consumers use those operations rather
   than reaching through private internals. Python does not require a class to
   group stateless functions; replacing a large controller with one equally
   broad class does not establish responsibility boundaries.
3. **Separate decisions from effects where useful.** Prefer explicit facts in
   and decisions out for deterministic rules; let the imperative shell read
   files, invoke processes and apply mutations. Keep inherently effectful
   operations at their real integration boundary. Do not force artificial
   purity through a forest of callbacks that hides operation order.
4. **Give rules and state explicit owners.** Each invariant and its determining
   policy has one authoritative component. Consumers call that owner rather than
   repeat its conditions. Separate trust-boundary validation may be legitimate,
   but must not become competing policy authority. Identify mutation ownership;
   avoid hidden global state and order-dependent mutable setup, including in
   shared fixtures.
5. **Declare dependency direction.** CLI/composition depends on application
   operations; those operations depend on rules and infrastructure boundaries
   as needed. Extracted components must not import the controller or receive its
   namespace through a passed module/context bag. Pass explicit facts or narrow
   collaborators instead. Prevent cycles and preserve existing declared import
   rules; adding an interface is justified by a concrete boundary, variation or
   test seam, not a requirement to put every dependency behind one.
6. **Choose functions and classes proportionately.** Prefer functions for
   stateless decisions and transformations. Use a class when it owns meaningful
   state, lifecycle or invariants, such as a lock or process session. Existing
   framework or integration requirements may determine the form; explain that
   constraint rather than imposing an interface/class per component.
7. **Preserve coherent transactions.** Keep lock scope, authorization, state
   transitions and durable publication order understandable under one transaction
   owner. Helpers may perform individual steps, but their contracts and call
   site must retain the governing sequence and failure obligations. Extraction
   must not scatter lock acquisition, authorization or publication across
   independently mutating owners.
8. **Align verification with ownership.** Exercise deterministic rules directly
   through their owning module. Use public-command integration checks for
   wiring, persistence, process behavior and transactions. Real integration
   behavior stays at that boundary; do not require pure unit tests for effects.
   Shared fixture facts have an explicit owner; each occurrence owns its mutable
   state. Reuse relevant setup without hidden mutation or duplicated scenario
   authority. [Testing discipline](../skills/testing-discipline/SKILL.md) owns
   test design; resolve the available installation when invoking that skill.
9. **Record module responsibilities.** For a new or materially reorganized
   module, briefly record what it owns, what belongs elsewhere, its public
   operations and allowed dependencies. Use a module docstring, nearby module
   document or its existing map; do not create a parallel inventory. A small
   cohesive extension may rely on a still-accurate existing description.
10. **Assess accumulated responsibilities.** Assess the resulting module with its
    helpers and consumers before retaining structural additions or material
    growth. Extract when a concrete responsibility boundary improves navigation,
    independent testing or change locality. Do not split solely to reduce line
    counts, function sizes or complexity. Explain why responsibilities belong
    together and the cost of a useful alternative; smaller functions or a bare
    assertion of cohesion do not establish good organization.

## Enforcement

Size and complexity are advisory investigation triggers, not numerical hard limits.
Mandatory rules govern introduced or materially worsened structure; untouched debt
stays outside scope. Use the existing review process to distinguish rule violations
from advisory concerns; this policy adds no review stage.

## Background

The official [modules tutorial](https://docs.python.org/3/tutorial/modules.html),
[Functional Programming HOWTO](https://docs.python.org/3/howto/functional.html) and
[PEP 8 interface conventions](https://peps.python.org/pep-0008/#public-and-internal-interfaces)
inform these choices; the local rules above govern placement and review.
