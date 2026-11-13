# SIDE-004 organization context

These examples and candidate boundaries supported the creation of the
[code organization policy](../../code-organization.md). The owner authorized
moving them out of the policy during the subsequent cleanup. They are
illustrations and later-refactoring context, not additional mandatory rules.

## Placement examples

- **Cohesive extension:** acceptance already owns disposition eligibility. Add
  another eligibility decision there, using explicit existing facts and its
  public operation. Exercise the rule directly and the command's wiring at the
  integration boundary. Explain that the same invariant and dependencies remain
  together; a larger module alone is not a reason to extract.
- **Distinct new concern:** an acceptance module should not acquire process
  session creation, cancellation and teardown. Give that lifecycle a named owner
  with explicit state and public operations, composed by the CLI/application
  shell. Document its allowed dependencies and test its lifecycle at the process
  boundary. Resolve transaction coordination before moving mutations.
- **Harmful mechanical split:** moving half a controller into `helpers.py`, then
  importing controller globals or passing its whole module as `context`, leaves
  ownership coupled and hides dependencies. Splitting one transaction's steps
  among those helpers can also hide publication order. Instead identify a real
  concern, pass explicit facts/collaborators and keep transaction ownership
  visible. A lower function metric does not repair this split.

## Controller discussion: candidates for later investigation

Potential concern boundaries include run storage (durability, integrity,
locking and persistence), frozen run inputs, candidate inspection/checks,
review collection, acceptance/dispositions, operation policy, actor lifecycle,
and CLI/composition. These are candidate boundaries for a later refactoring
effort, not an approved eight-file implementation plan or today's module map.

For example, acceptance policy belongs with acceptance behavior; process
transport must not acquire knowledge of finding dispositions. The later effort
must resolve actual interfaces, dependency edges and transaction ownership
against the code before moving it. Storage locking and application transitions
may need a single explicit transaction coordinator even when their individual
operations have different owners. This policy does not launch that effort.
