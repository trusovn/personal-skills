# Task Brief: SIDE-003.1 — Freeze the loading-cost baseline

## Outcome

One reproducible repo-only command measures the current instruction cost of
every source skill package: per-file SHA-256, file bytes, body bytes, and
normalized description characters for all 26 `SKILL.md` files, totals for all
26 and the 20-skill development profile subset, a file-level read graph, and a
command-prerequisites map. The baseline record also carries explicit
representative-route inventories — the file list each execution route loads
(entry file, route-applicable references and templates, invoked sibling
skills, and the repository's agent instructions) with summed sizes — so later
leaves can report cumulative before/after costs per route. The recorded
baseline verifies the plan's table and is the attribution basis for every
later SIDE-003 leaf. No skill bytes change; no general loader framework is
built.

## Authority and scope

| Item | Contract |
|---|---|
| Authority | [SIDE-003 plan](../SIDE-003/plan.md), "Current source baseline", "Measurement and decision rules" (layers 1–2 basis), "Delivery sequence" phase 1; [parent brief](../SIDE-003/brief.md) |
| Owner adjustment | 2026-11-03: no snapshot/rollback machinery. Git history is the revert path; hashes exist only for before/after attribution |
| Allowed changes | One repo-only measurement script under `tools/` (standard library only); `docs/tasks/SIDE-003/baseline.md` plus one machine-readable record (e.g. `baseline-measurements.json`) beside the plan, including the route inventories |
| Read-only context | Everything under `skills/`, `scripts/`, `tests/`; [docs/development.md](../../development.md), [docs/project-map.md](../../project-map.md); the repository's `AGENTS.md` |
| Out of scope | Shared runtime dependencies (`scripts/`), skill content edits, a general loader framework (route inventories are recorded data, not runtime), tokenizer installation (byte/character counts are the labeled initial basis; a tokenizer may be used only if already available, labeled with version; no bytes/4 token claims), session-use telemetry |
| Assumptions / unresolved | Frontmatter parsing and the exact counting helpers are discovered during implementation from the plan's counting definitions; route file lists are static unique-file estimates derived from each skill's instructions and the read graph — repeated reads are counted at execution time, not here; rendered-catalog observation (host wrapping, visible/truncated/omitted entries) is environment-dependent and recorded as unobservable locally when it is |

## Work and acceptance criteria

Required work:

1. Add a `tools/` script that computes, from the current working tree:
   per-file SHA-256, file bytes, body bytes (everything after the closing
   frontmatter delimiter, including its following whitespace), and
   description characters (normalized scalar text of the description field
   only, excluding other frontmatter fields) for every `skills/**/SKILL.md`;
   totals for all 26 and the 20-skill profile subset; and the file-level read
   graph (each skill's own `references/` entries plus cross-package
   reference links into other skills' `references/`). The script also sums
   the sizes of any explicitly supplied file list, so every recorded route
   sum reproduces deterministically.
2. Record `baseline.md` and the machine-readable measurements beside the
   plan, including the recording commit and a command-prerequisites map: per
   affected skill, its owning suites/evals and how to run them (from
   `docs/development.md`, `docs/project-map.md`, and the `tools/verify.py`
   discovery roots).
3. Record representative-route inventories: (a) a per-file size table for
   every instruction file any route can touch (the 26 entry files, every
   `references/` file, instruction-bearing module docs named in routes, and
   the repository's `AGENTS.md`); (b) for the plan's named representative
   routes (direct guided, packaged guided, high-assurance, corrections,
   optional evidence available/unavailable, and a representative acceptance
   path), the explicit file list each route loads and its summed size —
   including route-applicable references and templates, invoked sibling
   skills' entry files and their route references, and the agent
   instructions; (c) for each remaining body-work target (SIDE-003.9 and
   .11–.17), its ordinary-route and conditional-route file lists (entry file
   plus applicable references) with summed sizes. Later leaves derive their
   after-layout route lists from the same per-file table.
4. Compare the measured table with the plan's "Current source baseline" table
   (26 files, 404,992 total file bytes, 388,640 body bytes, per-file rows);
   record agreement or the exact delta and its cause.

- **AC-01:** Re-running the command on an unchanged tree reproduces identical
  numbers, every recorded route sum reproduces from the script, and the
  recorded table either matches the plan's table or documents the exact delta
  and cause (the plan's commit `aa94e28` differs from the current tree's; the
  current tree is the baseline that matters).
- **AC-02:** The record covers all 26 files, the 20-skill subset, the read
  graph, the representative-route inventories with summed sizes (labeled
  static unique-file estimates), and command prerequisites; counts are
  labeled as byte/character evidence, not tokens.
- **AC-03:** Measurement is read-only over `skills/`: the working tree shows
  only the new `tools/` script and the baseline artifacts.

## Verification

| Evidence | Scenario and oracle | Command |
|---|---|---|
| Fail-first | Not applicable: read-only measurement; the determinism check replaces it — a second run must produce byte-identical output, including route sums | `<the new script>`, twice |
| Targeted | Counts match the plan's table or deltas are explained per file; each representative route's file list is consistent with the read graph and the named instructions, and its summed size reproduces from the command | `<the new script>` |
| Owning suite | Architecture policy accepts the new `tools/` script (declared imports only) | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py` |
| Broader gate | None at this leaf; aggregate gates run at SIDE-003.18 | N/A |

## Execution

Status: `ready`; task kind: `executable`; guided profile.
Readiness route: standalone guided preflight after derived verification —
confirm the counting definitions, the route taxonomy, and the current
recording commit.
Verification-design recommendation: inline — the decisive oracle is the
plan's own table plus deterministic reproduction; the route inventories are
recorded data, not behavior.

```yaml
agent_tier: standard
reasoning: medium
review: immediate
budget: 19 tool calls / 55 minutes / measurement script, baseline artifacts, route inventories, comparison
```

Sizing: `default@1`; estimate 17 implementation calls / 50 minutes;
confidence medium; triggered `max_agent_calls` and `max_duration_minutes`.
Decomposition override: `cannot_split_safely` — candidate boundary
(mechanical measurement vs route-inventory analysis) rejected: the route
inventories reuse the same per-file reads, one script, and one counting
basis; a separate task would re-read all 26 packages and renegotiate the
counting definitions. Residual risk: a longer single leaf; the sums are
script-computed and deterministic, and the immediate fresh review checks the
route lists.

Stops: a dirty working tree with unrelated changes (record it and confirm
the measuring commit before proceeding); counting definitions or a route
list that cannot be derived from the plan's method or the skills' current
instructions (stop and report — later leaves depend on it); any need to
touch `scripts/`, skill bytes, or to build a loader framework.

Next action: derive `verification.md`, obtain a ready `preflight.md` through
standalone guided preflight, then implement.
Required follow-on: immediately after implementation or correction and any
applicable conditional stages, hand the completed bytes to a fresh independent
`task-review-discovery` call, and hand its report to a separate
`task-acceptance-review` decision.

Expected contract impact: none — repo-only measurement tooling; no registered
contract surface changes.