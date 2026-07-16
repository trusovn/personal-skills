# Stage 3 First-Three-Task Review

| Field | Value |
|---|---|
| Status / owner | `complete` / Codex review session |
| Dependencies | Stage 3 plan and Stage 2 contracts |
| Execution | `strong` agent; `high` reasoning |
| Review | `immediate` |
| Estimated budget | `30 tool calls / 90 minutes / 100k context` |

## Outcome

Review S3-01 through S3-03 for task-boundary clarity and test evidence that
distinguishes real behavior from false-positive or superficial completion, then
update only those briefs.

## Preserved pre-edit review

Verdict: `CHANGES REQUESTED`.

### [P1] S3-01 denial probes can pass without proving sandbox enforcement

- Location: `stage-3-tasks/S3-01-verification-sandbox-proof.md:42`
- Impact: An ambient filesystem permission or unavailable network endpoint can
  make both denial tests pass even if the selected runner enforces nothing.
- Evidence: The brief requires denied write and network attempts but does not
  first prove that the same local probes succeed without the restriction. It
  also does not require positive behavior for each supported policy mode.
- Required change: Use host-writable temporary paths and a local loopback
  listener as controls, then exercise the positive and negative permission
  matrix without external network access.

### [P2] S3-02's pre-refactor verification command cannot exist yet

- Location: `stage-3-tasks/S3-02-extract-controller-state.md:63`
- Impact: The implementer cannot run the stated "same owning suite before and
  after" because `test_controller_state.py` is a new task output. The task can
  start without a trustworthy baseline or report a misleading failure.
- Evidence: The allowed changes explicitly call `test_controller_state.py` new,
  while the verification section lists it as part of the before/after suite.
- Required change: Use `test_controller.py` as the pre-edit baseline and run the
  new direct-import module only after extraction.

### [P2] S3-02 does not require paired behavior-parity evidence

- Location: `stage-3-tasks/S3-02-extract-controller-state.md:40`
- Impact: Happy-path tests can pass even if invalid policies, stale identities,
  invalid transitions, or malformed records change exception or rejection
  behavior during the move.
- Evidence: The brief says behavior is unchanged but does not name positive and
  negative characterization oracles for the moved boundaries.
- Required change: Characterize representative valid outputs and invalid-input
  failures before extraction and assert the same results through the new module
  and compatibility exports afterward.

### [P2] S3-03 can pass without proving scope exclusion or failure behavior

- Location: `stage-3-tasks/S3-03-extract-controller-git.md:38`
- Impact: The extracted boundary could include unexpected or pre-existing user
  changes in a task patch, mishandle unusual path forms, or treat a failed Git
  observation as complete evidence while satisfying the listed category checks.
- Evidence: The brief enumerates positive repository states but does not require
  negative scope-exclusion assertions, controlled Git-command failure, or make
  its promised odd-path handling an acceptance oracle.
- Required change: Add explicit positive, exclusion, path-edge, and fail-closed
  cases, and stop back at Stage 2 if the promised pre-extraction behavior is not
  stable.

## Authority and boundary

- Reviewed: `stage-3-plan.md` and S3-01 through S3-03, with only the relevant
  Stage 2 Git/state contracts and owning tests used as supporting evidence.
- Changed: the three task briefs and this dedicated result note only.
- Preserved: no production code, tests, schemas, master-plan status, or existing
  result document is changed.

## Verification and acceptance record

- Positive/negative evidence requirements are explicit in each updated brief.
- Each brief has `agent_tier`, `reasoning`, `review`, and `estimated_budget`.
- Documentation checks and the final task-scoped diff are recorded after edits.

## Pilot measurement

| Session role | Session file | Tool calls | Final context input | Quota start | Quota end | Delta |
|---|---|---:|---:|---:|---:|---:|
| implementation | `not exposed in session` | 19 total combined calls | not exposed | not exposed | not exposed | not exposed |
| first review | `not run independently` | N/A | N/A | N/A | N/A | N/A |
| review fix | `not separately attributable` | included above | not exposed | not exposed | not exposed | not exposed |

- First independent review: `not run`
- Passed first review: `not reviewed`
- Review-rework calls: not separately attributable because review and edits share
  one session
- Task result: `accepted`
- Boundary adjustment for the next task: require paired controls for capability
  proofs and a distinct pre-edit baseline command when a task creates a new test
  module

## Post-edit result

Final self-review verdict: `APPROVE`.

- `rg` confirmed all four metadata fields plus explicit positive and negative
  evidence sections in S3-01, S3-02, and S3-03.
- `git diff --check` passed.
- The task-scoped diff confirms the master plan, production code, tests, schemas,
  and pre-existing user changes were not modified.
- Runtime tests were not run because this change updates task definitions only;
  the briefs now require those tests during their later implementation.

Residual risk: the required capability, state-parity, and Git-boundary tests are
specified but do not exist until their respective Stage 3 tasks execute. The
exact next action is to run S3-01 only after its Stage 2 entry contract is
confirmed.
