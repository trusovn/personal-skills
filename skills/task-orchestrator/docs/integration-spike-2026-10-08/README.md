# Task implementation flow: sequential integration spike

Date: 2026-10-08. Context: `../code-guided-orchestration.brief.md`.

## Result

The seven source skills ran successfully as separate stage actors in a fixed,
code-operated sequence. No AI selected or repaired a transition between skill
invocations. The synthetic task was implemented and independently accepted.

**Adoption decision:** retain these skills as the stage behavior base. Add a
small flow-owned machine integration contract before treating them as a reliable
unattended workflow. Do not make Markdown labels or free-text next actions the
transition authority. This experiment proves one successful route; it does not
qualify corrections, conditional skips, recovery, or upgrades.

The actors used the freshly installed source bytes, without skill edits. Model
and reasoning arguments were `gpt-5.6-terra` / `medium`, identified from the local
host catalog after unsupported `terra-medium` and `terra` launch attempts. All
seven successful actors had distinct sessions. No model reasoning-quality
assessment was performed.

## Synthetic task and observed sequence

Extend `catalog.select_names(names)` to `select_names(names, prefix="")` with
case-sensitive prefix matching. Preserve input order, duplicate entries, and
the caller's input. Default/empty prefix returns all values; empty input and no
matches return an empty list. Invalid input types were explicitly outside scope.

| Stage | Observed output | Observed repository effects |
|---|---|---|
| Brief designer | `ready_for_preflight`, executable leaf | One packaged brief |
| Verification designer | `ready`, AC-01–AC-03 mapped to V-01–V-03 | One `verification.md` |
| Preflight | `ready`, identities and command records | One `preflight.md` |
| Implementer | Schema-valid `complete` submission for SYN-01 | `catalog.py`, `tests/test_catalog.py` |
| Controller checks | Behavior and architecture passed | No file changes |
| Maintainability review | `ACCEPT`, architecture `PASS` | One numbered maintainability report |
| Registry updater | `REFERENCE_UPDATE: UPDATED` | Catalog record and README; generated index content unchanged |
| Acceptance review | `ACCEPT`, no findings | One numbered acceptance report |

The implementation establishes fail-first evidence against the old API, then
passes three focused tests, the owning suite, and architecture validation. The
functional reviewer independently exercises the public API and checks current
registry/discovery consistency. The final deterministic audit additionally
passes eight API cases, a valid registry instance, an invalid summary-type
instance, and rejection of three malformed worker/effect inputs.

The controller freezes preparation artifacts in one Git commit before preflight.
No actor commits, production commits, publication, external messages, or planning
document updates occur. Source skill files and the supplied orchestration brief
remain unchanged. The synthetic fixture is separate from the maintenance repo.

## Evidence and replay surface

- `run_spike.py`: actual fixed-sequence driver, actor prompts, launch arguments,
  per-stage scope checks, outcome checks, and controller checks.
- `audit_spike.py`: independent post-run behavioral and transport/effect audit.
- `evidence/ledger.json`: before/after file hashes, status, runtime arguments,
  changed paths, and stage admission results.
- `evidence/audit.json`: seven session IDs, continuity checks, validator results,
  and exact actor command strings/exit codes.
- `evidence/telemetry-audit.json`: requested runtime configuration and transport
  token usage for all seven stages, plus the shared instrumentation coverage gap.
- `evidence/*.prompt.txt`, `*.last.txt`, `*.events.jsonl`, `*.stderr.txt`: preserved
  invocation, result, and transcript evidence. Transport failures are archived
  separately and are not counted as skill attempts.
- `evidence/fixture/`: reviewable final implementation, tests, authority, policy,
  task package, registry, and helper tools.
- `evidence/fixture-baseline.patch`: task baseline versus final tracked files.
- `evidence/installed-manifest.json`, `installed-bundle.tar.gz`: installed bytes
  and hashes retained for this experiment.

Executed final audit command:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 skills/task-orchestrator/docs/integration-spike-2026-10-08/audit_spike.py
```

The original live fixture remains at `/private/tmp/task-flow-spike-2026-10-08`.
The driver uses fixed experiment paths and refuses to overwrite its fixture.
`setup` creates a new fixture; `run` performs the sequence. To repeat in another
location, update the fixture/output constants in a separate experiment copy.
Launching live actors consumes model budget; local artifact/audit inspection
does not require another live run.

## What must change before adoption

See `issues.md` for ten separately actionable items, each with evidence, owner,
bounded fix, and acceptance criteria.

1. **Flow-owned integration surfaces:** typed stage results and review evidence,
   explicit ordered prerequisites/applicability, consistent submission handoff,
   typed blocker/correction ownership, and canonical freshness/effect records.
   These are additions around existing skill behavior, not a request to rewrite
   the seven rubrics. FLOW-01 through FLOW-05 and LIVE-01 cover this work.
2. **Executor/distribution work:** validate evidence independently, retain runnable
   flow bundles, bind reviews to bytes and sessions, enforce path/command policy,
   and qualify supported flow versions. FLOW-06 concerns this boundary; shared
   fingerprint semantics should not change implicitly.
3. **Setup fixes:** define unborn-Git installation behavior and expose installed
   source drift. SETUP-01 and SETUP-02 can be fixed separately from execution.

`integration-guidance.md` lists the stage input/output boundaries, effect rules,
correction/invalidation matrix, installation resolution, and version pinning
points for the future executor.

## Limits and required follow-up qualification

Follow-up telemetry audit: the transport retained configuration, session IDs,
and token usage for every actor. No actor invoked `run_evidence.py`, no trusted
runtime-context file was supplied, and Git-local collector storage contains no
run manifests. The installer only established availability. Canonical evidence
begin/finish, check timing, snapshot retention, and recovery are unqualified.
TELEMETRY-01 records this missing integration coverage; it is not evidence that
the collector failed. The original happy-path claim does not include it.

The driver is a protocol smoke harness. It reads status labels from Markdown
and validates the implementation result with the existing worker adapter. It
checks actual file effects and separately records content identities. It does
not parse and enforce every freshness field, prove all required evidence is
complete, enforce permissions at the filesystem per-path level, or implement a
production runtime ledger/acceptance/dependency-release operation. LIVE-01 shows
why an actor verdict alone is insufficient. The post-run audit adds evidence;
it does not retroactively make the actor report a complete machine contract.

The brief's prose placed verification design after preflight. The declared driver
sequence placed it before preflight; the preflight packet correctly consumed the
existing verification artifact. No transition was changed to resolve that prose.
The brief used `review: milestone`; the explicit fixture authority required both
reviews, so the immediate-review conflict in FLOW-02 was inspected statically,
not triggered by this task.

No review required a correction. No stage was conditionally omitted. There was
one executable leaf with no dependencies and no user-owned dirty work. A future
qualification must exercise production correction, reference-only correction,
blocked/inconclusive results, justified skips, dirty staged/unstaged ownership,
unexpected artifact writes, interruption and sole-writer recovery, dependency
release, and resume after an installed-flow upgrade. Those require explicit
contracts and deterministic assertions; this happy path cannot stand in for them.
