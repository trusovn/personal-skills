# Java architecture guardrails

Use this reference only for Java repositories that need executable package/class
architecture rules.

## Preference order

1. Reuse existing architecture tests/static analysis if present.
2. Otherwise prefer ArchUnit inside the repo's existing test framework.
3. Expose a narrow architecture-test command through Gradle/Maven or the current
   task runner.

Upstream: https://www.archunit.org/
Repository: https://github.com/TNG/ArchUnit

Do not pin the library version from this reference. Use a version compatible
with the repository's current Java/test stack.

## Example package dependency rule

Adapt package names to a boundary that actually exists:

```java
import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.noClasses;

ArchRule domainMustNotDependOnInfrastructure =
    noClasses()
        .that().resideInAPackage("..domain..")
        .should().dependOnClassesThat().resideInAPackage("..infrastructure..");
```

Run the rule through the repo's existing JUnit/ArchUnit integration or normal
test class convention.

ArchUnit also supports layered architecture and cycle rules. Use them only when
those constraints are genuinely part of the repository architecture.

## Canonical command

Prefer a stable repo command such as an existing Gradle/Maven task or filtered
architecture-test target, for example conceptually:

```text
./gradlew architectureTest
```

or the repo's existing test task with an architecture-test filter.

Do not invent a new build tool solely to give the check a name. If architecture
tests are already a fast subset of the normal test suite, the canonical command
may simply be a documented filtered test invocation.

## Existing-debt handling

Prefer explicit narrow exceptions inside architecture tests or a dedicated
legacy rule/allow-list whose scope is inspectable. Avoid one giant assertion
that excludes entire packages merely to make the initial suite green.

The expected no-regression property is:

- known exact legacy dependency can remain temporarily;
- newly introduced equivalent dependencies fail;
- removing legacy debt does not create permission for it to return.

If exact baseline comparison is awkward in the chosen ArchUnit style, consider
starting with the clean subset of boundaries that can already be enforced rather
than creating a complex custom framework.

## Advisory signals

Do not turn class length, method count, constructor parameter count, or package
size into universal hard architecture tests without an explicit project reason.
Those facts are better used as semantic-review leads.

## Sentinel

Use a disposable test fixture/class or isolated worktree to create one forbidden
package dependency, prove the architecture test fails, remove it, and prove the
canonical command passes again.
