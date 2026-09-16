# Python architecture guardrails

Use this reference only when the target Python repo needs deterministic import
or module-boundary enforcement.

## Preference order

1. Reuse existing import/static rules if they already express the invariant.
2. Otherwise prefer Import Linter for package/module dependency contracts.
3. Keep Ruff/Pylint/complexity metrics advisory unless the project already has a
   justified hard convention.

Upstream: https://import-linter.readthedocs.io/

Import Linter provides contract types including `forbidden`, `protected`,
`layers`, `independence`, and `acyclic_siblings`. Choose the contract that maps
most directly to the repo's actual invariant rather than forcing everything
into layers.

## Example: forbidden dependency

Adapt package names to the real repository.

```ini
# .importlinter
[importlinter]
root_package = myapp

[importlinter:contract:domain-does-not-import-infrastructure]
name = Domain does not import infrastructure
type = forbidden
source_modules =
    myapp.domain
forbidden_modules =
    myapp.infrastructure
broken_contract_guidance =
    Depend on the application/domain boundary rather than a concrete adapter.
```

Canonical native command:

```text
lint-imports
```

Expose it through the repo's existing command surface, for example
`make architecture-check` or the existing task runner, rather than teaching
agents to rediscover configuration flags.

## Other useful contracts

Use only when they match a real boundary:

- `protected`: private/internal module may only be imported by allowed callers
- `independence`: named peer modules/packages must not depend on each other
- `layers`: declared layer direction/order
- `acyclic_siblings`: sibling packages must not form cycles

Do not add a layered contract just because it is available.

## No-regression / legacy imports

Import Linter supports `ignore_imports` entries such as:

```ini
ignore_imports =
    myapp.domain.legacy -> myapp.infrastructure.old_adapter
```

Use these as exact legacy exceptions, not broad wildcard escape hatches.
Set `unmatched_ignore_imports_alerting = error` explicitly on every contract
that has `ignore_imports`. This is the non-mutating baseline-freshness check:
when a fixed import no longer matches an exception, `lint-imports` fails without
rewriting the config. Do not rely on a version default or set this to `warn` or
`none`.

```ini
unmatched_ignore_imports_alerting = error
```

Prove the regression sequence in a disposable fixture/worktree: baseline one
forbidden import, remove it, verify `lint-imports` fails on the stale
`ignore_imports` entry, remove that reviewed entry, then reintroduce the import
and verify `lint-imports` fails the contract. This prevents the old exception
from masking a returned violation.

For large existing debt where `ignore_imports` becomes unwieldy, a small
repo-owned comparison wrapper may be more legible, but do not build a general
Python dependency analyzer.

The ordinary architecture command must not regenerate exceptions.

## Advisory signals

If Ruff, Pylint, Radon, or another existing tool already reports complexity,
size, or dependency-related facts, those can feed semantic review. Do not add a
second tool solely to enforce arbitrary thresholds such as "every function <=
30 lines".

## Sentinel

In a disposable fixture/worktree, create one import matching a hard forbidden
contract. Verify:

- canonical architecture command breaks the expected contract;
- output identifies the importing/imported modules;
- removing the disposable import returns the gate to green.
