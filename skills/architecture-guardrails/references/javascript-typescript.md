# JavaScript / TypeScript architecture guardrails

Use this reference only when the target repo is JavaScript/TypeScript and needs
new or repaired deterministic architecture enforcement.

## Preference order

1. Reuse existing ESLint/import-boundary rules if they already express the
   required dependency invariant precisely.
2. Otherwise prefer `dependency-cruiser` for import/dependency graph rules.
3. Add other complexity/size tooling only when it already exists or a concrete
   project risk justifies it. Do not add several analyzers just to produce more
   numbers.

Upstream: https://github.com/sverweij/dependency-cruiser

## Dependency-cruiser fit

Useful capabilities include:

- path-based forbidden dependencies
- explicit `error` / `warn` / `info` severity
- circular dependency detection
- reporters suitable for human/CI use
- known-violation baselines (`--baseline`, `--ignore-known`, and shrink-only
  support in current versions)

Use the repo-compatible current version; inspect the installed CLI before
assuming a baseline option exists in an older locked version.

## Example rule shape

Adapt paths to real repo boundaries. Do not paste this architecture into an
unrelated project.

```js
// .dependency-cruiser.cjs
module.exports = {
  forbidden: [
    {
      name: "no-domain-to-infrastructure",
      severity: "error",
      comment: "Domain policy must not depend on concrete infrastructure.",
      from: { path: "^src/domain/" },
      to: { path: "^src/infrastructure/" },
    },
    {
      name: "no-production-to-tests",
      severity: "error",
      from: { path: "^src/" },
      to: { path: "(^|/)(test|tests|__tests__)(/|$)" },
    },
  ],
  options: {
    doNotFollow: { path: "node_modules" },
    skipAnalysisNotInRules: true,
  },
};
```

Only add a global cycle rule when the repository actually declares cycles
prohibited in the governed scope. When applicable the rule shape is:

```js
{
  name: "no-circular",
  severity: "error",
  from: {},
  to: { circular: true },
}
```

## Canonical command

Fit this into the existing package manager/task runner. For example:

```json
{
  "scripts": {
    "check:architecture": "dependency-cruiser --config -- src"
  }
}
```

If the config has a non-default path/name, pass it explicitly. Keep this direct
command runnable even if `npm run check` also calls it.

Do not require implementation agents to remember the underlying CLI flags;
document `npm run check:architecture` or the repo-equivalent command.

## Clean vs no-regression

### Clean

Normal error-severity rules are sufficient when the governed tree currently has
no violations.

### No-regression

Prefer dependency-cruiser's native known-violation baseline when the installed
version supports it. Verify the exact current CLI semantics before scripting.
`--ignore-known` lowers matching violations to ignored severity, so it alone
does not satisfy the "removed debt stays removed" contract. The canonical
command needs two checks, in this order:

1. a non-mutating freshness check that copies the tracked baseline to a
   temporary path, runs `--baseline --baseline-shrink-only` against that copy,
   and fails if the temporary result differs from the tracked baseline;
2. the ordinary `--ignore-known` architecture check.

For example, adapt this shape to the repo's package manager, source scope, and
temporary-file conventions:

```text
copy <tracked-baseline> <temporary-baseline>
dependency-cruiser --config <config> <scope> --baseline <temporary-baseline> --baseline-shrink-only
compare <tracked-baseline> <temporary-baseline>; fail when different
dependency-cruiser --config <config> <scope> --ignore-known <tracked-baseline>
```

The tracked baseline remains unchanged during verification. The explicit,
reviewed maintenance command may apply the same shrink-only operation to the
tracked file; it must not add entries. This preserves these behaviors:

- current known violations can be ignored by identity;
- a removed violation makes freshness fail until the baseline shrinks;
- after that shrink, reintroducing the same edge is absent from the baseline
  and the ordinary check fails;
- new violations still fail;
- baseline expansion is an explicit architecture change, not part of normal
  verification.

Prove the sequence in a disposable fixture/worktree: baseline one forbidden
edge, remove it, verify freshness requires a shrink, apply the reviewed shrink,
then reintroduce the edge and verify the ordinary gate exits non-zero.

If the repo's locked version cannot provide safe no-regression semantics, use
narrow `from`/`to` exclusions only if the tool also fails on unmatched stale
exceptions; otherwise use a small comparison wrapper that does. Do not suppress
an entire legacy folder unless that broad exception is an explicit architecture
decision.

## Advisory signals

Do not make these hard architecture failures by default:

- `max-lines`
- function complexity
- dependency count/fan-out
- generic module names

If existing ESLint or other tooling already reports them, keep them warnings and
pass the output to `task-maintainability-review`. A large file is evidence to
inspect, not proof of a god object.

## Sentinel

A useful safe sentinel is a disposable source file inside a fixture/worktree
that imports a specifically forbidden module. Verify the canonical command:

1. fails non-zero;
2. names the expected rule/edge;
3. passes again after the disposable change is removed.

Never mutate unrelated dirty files to prove the rule.
