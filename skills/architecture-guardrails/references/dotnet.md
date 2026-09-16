# .NET architecture guardrails

Use this reference only for .NET repositories that need executable namespace or
type dependency rules.

## Preference order

1. Reuse existing analyzers/architecture tests when they already express the
   invariant.
2. Otherwise prefer ArchUnitNET inside an existing xUnit/NUnit architecture test
   project/suite.
3. Expose a stable filtered `dotnet test` or repo task command for agents/CI.

Upstream: https://github.com/TNG/ArchUnitNET

Use a version compatible with the repository. ArchUnitNET analyzes built
assemblies, so follow current upstream guidance and the repo's build/test
configuration rather than hardcoding a package version here.

## Example namespace dependency rule

The current ArchUnitNET fluent API supports rules of this shape:

```csharp
IArchRule rule = Types().That()
    .ResideInNamespace("MyApp.Domain")
    .Should()
    .NotDependOnAny(
        Types().That().ResideInNamespace("MyApp.Infrastructure"));

rule.Check(Architecture);
```

For nontrivial suites, define reusable `IObjectProvider<IType>` layers and load
the architecture once according to the existing test framework conventions.

Only encode namespace/type boundaries that the project actually owns.

## Canonical command

Prefer an existing architecture-test project/category and expose one repo-level
command, e.g. conceptually:

```text
dotnet test tests/MyApp.ArchitectureTests/MyApp.ArchitectureTests.csproj -c Debug
```

or an existing solution/test filter. ArchUnitNET upstream currently recommends
running architecture tests in Debug because it analyzes the built binaries; use
the repo's actual compatible configuration.

If a Make/Just/script/task runner already exists, alias the command there rather
than teaching implementation agents a long filter expression.

## Existing debt

Represent known legacy dependencies explicitly and narrowly in the architecture
test setup or an inspectable allow-list. Do not make the ordinary check rewrite
that list.

If exact no-regression handling would require a large custom harness, enforce
the clean high-value boundaries first and leave ambiguous legacy areas to
semantic review rather than over-engineering the gate.

## Advisory signals

Class length, number of methods, dependency count, and constructor size are
normally reviewer signals rather than universal hard rules. Use existing
analyzers if already present; do not install several metrics packages just to
score maintainability.

## Sentinel

Create a disposable class/reference that violates one hard namespace rule in an
isolated fixture/worktree, run the canonical architecture test, verify the
expected failure, restore, and rerun green.
