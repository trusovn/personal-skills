# Session Handoff

This file is a durable companion to the copy/paste handoff. The copy/paste
packet is still the primary resume context.

Generated: 2026-07-16 12:45 WEST
Workspace: `/Users/mtrusov/work/skill-sources/personal-skills`
Primary goal: Fix or truthfully reject the S3-01 verification-sandbox decision,
then perform the final readiness evaluation against the S3-01 acceptance
criteria.
Latest user request: Give another agent a targeted-TDD handoff for the fixes and
final S3-01 evaluation.

## Resume Prompt

Paste this into the next session:

```text
You are continuing S3-01 in /Users/mtrusov/work/skill-sources/personal-skills.
Use this handoff as authoritative context, but verify filesystem and Git state
before editing. Preserve all pre-existing user changes. Work only within the
files allowed by S3-01.

The current macOS sandbox-exec proof passes its stated direct-path matrix, but a
review reproduced a workspace-write escape through a pre-existing hard link:
an in-root alias allowed a sandboxed command to mutate an out-of-root inode.
Use targeted TDD: first add the smallest regression proof and show it fails for
the expected reason against the current profile. Then determine whether an
available local, standard-library-only mechanism can enforce the persisted
writable-root policy without a race or policy weakening. Do not make the test
pass by weakening its oracle, merely documenting the escape, or adding a
race-prone preflight scan. If the boundary cannot be enforced, update the
decision truthfully to rejected/blocked as S3-01 requires. Finally rerun the
exact S3-01 checks and issue an explicit complete-versus-blocked readiness
verdict, including AC-01 through AC-06 and whether S3-07 may proceed.
```

## Current State

- The staged S3-01 implementation consists of two new files:
  - `skills/task-orchestrator/docs/verification-sandbox-decision.md`
  - `skills/task-orchestrator/tests/test_verification_runner.py`
- The decision currently says macOS `/usr/bin/sandbox-exec` with a generated
  Seatbelt profile is "adopted and locally proven."
- The existing seven-test module passes on the current supported macOS host
  when run outside Codex's outer sandbox.
- Review verdict is `CHANGES REQUESTED` because the writable-root boundary has
  a demonstrated hard-link escape.
- S3-01 is not ready to be marked complete. S3-07 remains blocked by S3-01.
- S3-02 may proceed independently because it depends only on Stage 2, but that
  does not resolve this handoff.
- No source or staged file was changed during review. This handoff file is the
  only artifact created afterward.
- No background process or local server remains active.

## Review Finding And Reproduction

The generated workspace profile in
`skills/task-orchestrator/tests/test_verification_runner.py` uses a path filter:

```scheme
(deny file-write* (require-all
  (require-not (subpath (param "WRITABLE_ROOT_0")))))
```

That blocks a direct write to an outside pathname, but it permits writing an
inside pathname that is a hard link to an outside inode.

The successful local reproduction used this shape:

1. Create temporary `root/` and `outside/` directories.
2. Create `outside/victim` containing `original`.
3. Before sandbox launch, create `root/alias` with
   `os.link(outside_victim, inside_alias)`.
4. Run a Python child through `_run(...)` with `sandbox: workspace-write` and
   `writable_roots: [root]`.
5. Have the child write `mutated` through `root/alias`.

Observed result:

```text
returncode=0 victim='mutated' stderr=''
```

A separate probe showed that the sandboxed child cannot itself create a new
cross-boundary hard link: `os.link(outside_victim, inside_alias)` returned a
permission error. That does not remove the defect because a pre-existing alias
is sufficient and is not rejected by the current mechanism.

## Targeted TDD Contract

### Required red proof

Add the smallest deterministic regression scenario to
`tests/test_verification_runner.py`:

- create an out-of-root victim and an in-root hard link before sandbox launch;
- establish that the victim is host-writable and the alias refers to it;
- run the same child write through the proposed `workspace-write` boundary;
- require the out-of-root victim to remain unchanged;
- require a denied result or a fail-closed prelaunch rejection;
- ensure the fixture owns and cleans all files;
- use bounded subprocess behavior and no sleeps.

Run this regression against the current implementation and record the expected
failure before changing the mechanism. The expected failure is that the child
returns zero and the victim content changes.

### Acceptable green proof

A candidate fix is acceptable only if all of the following are true:

- the new hard-link regression passes for the intended boundary reason;
- the existing positive cases still run, including writes inside every
  configured root;
- direct out-of-root writes, read-only writes, and denied loopback connections
  still fail without side effects;
- authorized danger-full-access still works only in its isolated temporary
  path, and unauthorized danger-full-access is rejected before launch;
- unsupported hosts/configurations still fail closed;
- an unrestricted runner or equivalent controlled fault still makes the
  negative proof fail;
- the fix uses no dependency, external network endpoint, model call, production
  runner code, policy-version change, or shell execution;
- the mechanism does not rely on a scan/check that an external process can race
  before or during verification.

Do not treat an `st_nlink` preflight by itself as proof. It may reject the
static fixture but leaves a time-of-check/time-of-use question unless the
mechanism also prevents alias creation or mutation for the entire execution
window.

### Blocked outcome

If no allowed local mechanism can provide the green proof, follow S3-01's exit
contract:

- change the decision status and conclusion from adopted/complete to
  rejected/blocked;
- preserve the successful direct-path and network evidence as bounded facts;
- record the hard-link counterexample and why the mechanism cannot claim the
  persisted writable-root boundary;
- present the smallest user choices named by S3-01: approve a dependency,
  approve a versioned policy narrowing/weakening, or defer the executor;
- do not add production runner code and do not authorize S3-07.

If pathname-only authority is proposed as an interpretation of
`writable_roots`, stop and ask the user. The current Stage 3 risk statement and
S3-01 outcome are written as enforcement of the write boundary, so accepting
out-of-root inode mutation would be a material policy decision, not a silent
documentation clarification.

## Sources Of Truth

Read before editing:

- `AGENTS.md`
- `skills/task-orchestrator/docs/stage-3-plan.md`
- `skills/task-orchestrator/docs/stage-3-tasks/S3-01-verification-sandbox-proof.md`
- `skills/task-orchestrator/assets/run-policy.schema.json`
- `skills/task-orchestrator/docs/transport-decision.md`
- the two staged S3-01 files listed above

The S3-01 allowed change boundary remains:

- `docs/verification-sandbox-decision.md`
- `tests/test_verification_runner.py`

This handoff is context, not an expansion of the task's allowed production
scope.

## Commands And Verification Already Run

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_verification_runner.py`
  inside Codex's outer sandbox: failed before evaluating S3-01 because the
  outer sandbox denied binding the `127.0.0.1` control listener.
- The same command with approved execution outside Codex's outer sandbox:
  `Ran 7 tests ... OK`.
- Pre-existing hard-link escape probe outside the outer sandbox: child returned
  `0`; out-of-root victim changed to `mutated`.
- Sandboxed creation of a new cross-boundary hard link: denied with
  `PermissionError`; victim remained `original`.
- `git diff --cached --check`: passed.
- `git diff --check`: passed.
- Not run: aggregate task-orchestrator suite. The proven mechanism-level blocker
  made broader regression evidence irrelevant to the review verdict.

The local capability command needs approved execution outside Codex's outer
sandbox because the proof intentionally binds a loopback listener and applies a
nested Seatbelt profile. Do not reinterpret an outer-sandbox denial as S3-01
evidence.

## Final Evaluation Required

After the fix or blocked conclusion:

1. Inspect the effective change, not only the index:
   `git diff HEAD -- skills/task-orchestrator/docs/verification-sandbox-decision.md skills/task-orchestrator/tests/test_verification_runner.py`.
2. Run the new focused regression first and confirm it passes for the intended
   reason.
3. Run the complete S3-01 module outside the outer sandbox:
   `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest skills/task-orchestrator/tests/test_verification_runner.py`.
4. Run `git diff --check` and, if fixes are staged, also
   `git diff --cached --check`.
5. Inspect `git status --short` and verify no temporary or bytecode artifacts
   remain.
6. Evaluate AC-01 through AC-06 individually.
7. Return exactly one readiness result:
   - `complete`: one exact mechanism is locally proven against the full
     persisted boundary, and S3-07 may proceed; or
   - `blocked`: no allowed mechanism is proven, the decision is truthful about
     rejection, and S3-07 must not proceed.

Do not call a merely documented limitation `complete`.

## Files And Artifacts

- `skills/task-orchestrator/docs/verification-sandbox-decision.md` - staged new
  file; currently contains the disproven adoption conclusion.
- `skills/task-orchestrator/tests/test_verification_runner.py` - staged new file;
  currently contains the seven passing direct-path/configuration tests but no
  hard-link-alias regression.
- `skills/task-orchestrator/docs/stage-3-tasks/S3-01-targeted-tdd-handoff.md` -
  this new handoff.
- `AGENTS.md` - pre-existing untracked repository instruction file; preserve it.
- `skills/task-orchestrator/agent-output.analysis.md` - pre-existing untracked
  file; preserve it and do not include it in S3-01 changes.

Because the two S3-01 files are staged, subsequent edits may appear as unstaged
changes layered over staged additions. Review both index and worktree, or use
`git diff HEAD -- <paths>` to see the effective result. Do not assume the staged
snapshot automatically contains later fixes.

## Guardrails For The Next Agent

- Stay within S3-01's two allowed implementation files.
- Do not edit the Stage 3 plan or S3-01 task brief.
- Do not add production runner code.
- Do not browse, install dependencies, call a model, or contact an external
  endpoint.
- Do not weaken a denial into a warning or silently narrow policy semantics.
- Preserve all unrelated staged and untracked user work.
- Do not manufacture a passing test by skipping the hard-link case on the
  supported host.
- Keep the implementation/proof minimal; if the mechanism cannot satisfy the
  boundary, prefer the truthful blocked result over speculative complexity.
