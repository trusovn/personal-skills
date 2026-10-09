# Preflight: T-001.4

Status: ready
Profile: guided
standalone_preflight_value: material
Checked: 2026-10-09
Source brief: docs/tasks/T-001.4/brief.md
Source brief revision: ready brief at Git `700654acc294b1719f6a141f3b7c8243ee406e9a`
Verification design: docs/tasks/T-001.4/verification.md
Verification revision: 1

## Scope, dependencies and ownership

The packaged brief is an executable leaf. The verification design's singular
`Source brief:` resolves to this brief; V-01–V-05 cover AC-01–AC-04 and I-01/I-02.
The user explicitly confirmed in this preflight session that T-001.1, T-001.2
and T-001.3 were accepted. This confirmation clears the dependency condition;
older .2/.3 result files still report pending review and are not final verdicts.

Initial status contained only `?? docs/tasks/T-001.4/verification.md`.
Preserve that user-owned derived input. No intended implementation path is dirty.
This preflight adds only this packet; it does not refresh installed `.agents/`.

Implementation scope: cross-stage sections of root `README.md`, `skills/README.md`
and `skills/task-implementation-flow/README.md`; focused
`tests/test_install_development_skills.py` changes; minimal canonical installer
synchronization only if required. Predecessor skill sources, installed `.agents/`,
plans and reviews remain read-only. No new skill selection or helper is authorized.

The canonical installer already selects all four preparation skills from
`skills/task-implementation-flow/`, maps `PROFILE_SKILLS_README` to
`skills/README.md`, and explicitly lists its managed shared scripts. It copies
skill trees while excluding transient files, replaces only managed destinations,
and manages a marked AGENTS block. No membership/runtime change is needed now.

## Commands and capability

Working directory for all commands: repository root.

First targeted implementation selector, extend the existing test for V-03:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py -k test_installs_profile_preserves_agents_text_and_final_availability
```

Ran during preflight: PASS, 1 test, 0.334 seconds. This test creates a temporary
Git repository, configures local test identity, commits a baseline, and invokes
the actual canonical installer in a subprocess. It checks availability, guide
and shared-script bytes, selected skill file existence and retained AGENTS text.
It confirms usable Python/Git/installer capability, not the new full projection
oracles or agent compliance. No dependency installation or network is needed.

Focused refresh selector, extend the existing test for V-04:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py -k test_rerun_removes_stale_managed_files_and_preserves_unmanaged_installations
```

Not run during preflight. It already exercises two real installs in a committed
temporary target, stale managed-file removal, guide restoration and unmanaged
preservation. Add exact unrelated-skill/file byte checks and all four package
projections rather than relying on existence. Reuse `init_repo`/`run_installer`;
never use the active repository as an installer target.

After changed targeted evidence is green, run these authorized owning gates in
order, once for the current implementation:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_install_development_skills.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/task-implementation-flow/task-brief-designer/tests -p test_package_resources.py
```

Neither owning suite ran during preflight. Future task-owned assertions need
not exist at entry: their fixture, tool and filesystem boundary are available.

## Scenario oracles and remaining obligations

| Scenario | Observable implementation evidence |
| --- | --- |
| V-01 / AC-01 | Review overview, every example, role table and package layout across the three guides against predecessor source obligations, including packaged documentation and the unpackaged direct-edit exception. Focused assertions must reject old route wording; keywords alone cannot establish consistency. |
| V-02 / AC-02 | Compare authority, derived coverage/revision ownership, capability distinctions, context, material staleness and handoff passages against four predecessor sources and relevant references. Preserve review-stage policy. Return a predecessor semantic disagreement to its owning child. |
| V-03 / AC-03 | Initial actual committed-target install: compare all four managed package file sets and bytes, including references, and profile-guide bytes using canonical mappings and transient exclusions. Compare unmanaged bytes before/after. |
| V-04 / AC-03 | Same-target second actual install: stale managed file disappears, stale guide is restored, all four managed projections still match, unrelated skill/file and AGENTS text outside the block retain exact bytes, and the block occurs once. |
| V-05 / AC-04 | Inspect installer constants, guide, focused tests and README install instructions together. Keep selection/shared dependencies unchanged unless a scoped need is demonstrated. Report source consistency and actual projection separately from unrun semantic qualification. |

No scenario is claimed completed by this readiness decision. The existing baseline
is narrower than V-03/V-04: expanding byte/file-set oracles is authorized task work.
Actual semantic role calls and multi-call composition remain unrun T-005 proof;
no whole-repository, live-network or agent/model-budget checks are authorized here.

## Context, stops and next action

This task distributes human-coordinated preparation guidance to installed callers.
Material consequences are contradictory entry routes, omitted/stale installed
references, or refresh damage to unmanaged content. Disposable committed targets,
byte comparisons and narrow installer ownership mitigate those risks. No new
product decision is needed. Older pending-review result text is superseded for
dependency readiness by the user's acceptance confirmation, not by inferred tests.

Stop for a predecessor semantic disagreement, inseparable user-work overlap,
unsafe permission, missing decisive fixture capability or widened scope.
Requirement changes return to task design. A justified coverage revision retains
scenario IDs and requires focused readiness reconsideration. Expected scoped
source/test/report changes alone do not invalidate readiness.

Standalone value is material: it resolved an explicit reviewed-predecessor entry
condition through user confirmation and demonstrated the committed disposable
installer boundary with an actual cheap test. Recommend separate preflight for
similar tasks with uncertain reviewed dependencies or installer boundaries.

Implementer handoff:

```text
Implement T-001.4 from its brief and verification revision 1 under this ready
guided packet. Preserve the untracked verification.md and all read-only sources.
Extend the initial-install selector above with fail-first route/projection checks;
extend the refresh selector with managed file-set/byte and unmanaged-byte oracles.
Account for V-01–V-05, then run the installer suite and package suite in order.
Submit mapped current evidence and explicit unrun T-005 proof. Immediately hand
completed bytes to a fresh independent acceptance reviewer, preserving applicable
prior conditional stages, and end the implementer invocation.
```
