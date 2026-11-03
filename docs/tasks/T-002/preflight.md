# T-002 preflight

Status: `ready`
Profile: guided
standalone_preflight_value: material

## Readiness summary

Source: [brief.md](brief.md), revision 1; [verification.md](verification.md), revision 1, declares the correct source brief. Coverage derives from AC-01–05 and project-plan FLOW-002, V-003/V-006/V-008. No requirements change is needed.

Material uncertainty resolved: the prepared pinned interpreter and same-installation measurement helpers are available; current real measurement tests pass without skips. The active profile matches source (95 managed paths). Standalone preflight remains useful for similar tasks that depend on installed analyzer capability.

Repository: `/Users/mtrusov/work/skill-sources/personal-skills`. Initial status: modified `docs/tasks/index.json`; untracked `docs/tasks/T-002/`. Treat these as pre-existing user work. Implementation source paths are clean and separable. Preserve the task package and index; this invocation adds only this packet.

Allowed implementation scope: source `skills/task-implementation-flow/task-preflight/`; distinct missing shared measurement/installer test evidence only; installer/profile documentation updates only when made stale. No runtime redesign, downstream T-003/T-004 edits, active installation refresh, master-plan changes, or implicit dependency installation.

## Decision context and applicability

The producer hands actual original source evidence and native obligations to T-003 and T-004. False freshness or replaced history would invalidate later comparisons. Advisory metrics must retain gaps and never waive native policy. See [project plan](../../project-plan.md), [project map](../../project-map.md), [development guide](../../development.md), [measurement contract](../../contracts/measurement.json), and [measurement guide](../../../scripts/measure-maintainability.md). T-001.1/1.2/1.3 accepted dependency outputs remain applicable: format-5 runtime, empty-folder capture and installed composition are present and the owning behavioral suite passes. Future producer guidance and live compliance remain unimplemented/unqualified.

Assumption: existing accepted scope and advisory policy remain authoritative. No decision-critical unknown remains. Reconsider readiness for changed authority, ownership, capability, or verification obligations. Expected source edits alone do not require full rediscovery.

## Acceptance evidence and commands

All commands use the repository root. Let the exact owning command be:

```sh
PYTHONDONTWRITEBYTECODE=1 .quality/envs/Darwin-arm64-cpython-3.14.6-79dbf22b5bc1/bin/python -m unittest discover -s tests -p test_maintainability.py
```

| Coverage | Feasibility and decisive oracle | Current result / implementation duty |
|---|---|---|
| AC-01; V-01, V-02a–d, V-03a–c | Existing disposable Git/install fixtures exercise dirty/index preservation, empty folders and sibling collisions. Observe report content and unchanged source/index/sentinels. | Owning command: 33 tests passed, no skips. New guidance/eval outcomes remain to implement. |
| AC-02; V-04a/b, V-05a–h, V-06a–c, V-07 | Real reports expose source inventory, hashes and effective identity; existing comparison/transfer fixtures support controlled changes. Inspect both packet branches and actual prepared report references. | Runtime boundary feasible; future prepared evals must cover every listed variant, retain original history and explicit clone transfer. Not yet run as agent behavior. |
| AC-03; V-08a/b, c–f with A/R variants; V-10f/g | Existing missing/incompatible/partial tool fixtures plus explicit advisory/required policies permit decisive ready/blocked grading. | Feasible within task-owned setup. Policy variants must supply all unrelated prerequisites; future agent outcomes unrun. |
| AC-04; V-09a–c, V-10a–g | Supply actual policy/command files and checked-byte evidence; real native F401 versus advisory success is already supported. Grade retained scope/owner/duties and command history. | Owning suite passes. Future evals must distinguish later-stage duties from entry prerequisites and reject stale/partial aggregate coverage. |
| AC-05; V-11 and all V-01–10 inputs | Existing evals.json and evals/files/setup_fixture.py are the owning surfaces. Reuse disposable fixture setup and installer preservation helpers; inspect prompts, write permissions and grading together. | Feasible future work; preserve eval IDs 1–12 and their distinct negative cases. Structural validation alone is insufficient. |

## Native obligations and verification results

- Owning measurement command above: exit 0, 33 tests, no skips; real analyzer prerequisite proved locally. Analyzer imports also succeeded.
- `python3 scripts/install_development_skills.py --check .`: exit 0, 95 paths, no differences. Read-only discovery; no active refresh.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py`: exit 0, 4 tests. Whole-project architecture policy remains required before implementation handoff; structural evidence only.
- `python3 tools/check_contracts.py --root .`: exit 0, 6 subsystems, 12 indexed plan references. Structural evidence only.

Implementation owns rerunning affected checks on edited bytes. If projection changes, run `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py`. For cross-cutting changes the implementation stage owns `python3 tools/verify.py` after focused success, subject to cost/permission policy. No aggregate or live model eval was run here. Live evaluation requires separate approval and actual grading; prepared fixtures do not qualify agent behavior.

## Stops and next action

No current blocker. Stop for user-owned overlap, missing indispensable capability, or scope/policy changes outside this brief. Do not repair negative fixtures to obtain green results. Do not install tools or refresh this invocation. Preserve source-guided versus installed execution distinctions. Independent discovery and separate acceptance remain required after implementation; this packet is readiness only.

## Implementer handoff

```text
Execute bounded-task-implementer on docs/tasks/T-002/brief.md using verification.md revision 1 and this guided readiness. Preserve the pre-existing task package/index. Edit only the authorized source preflight surfaces and necessary owning tests/profile projections. Reuse existing runtime and fixture boundaries; cover every V-01–V-11 variant with supplied inputs and decisive oracles. Use the pinned interpreter and owning command above first. Recheck relevant current scope/ownership/capabilities before editing; stop on material changes. Report live agent qualification as unrun unless separately approved and graded. Then follow fresh discovery, registry updating as applicable, and separate acceptance.
```
