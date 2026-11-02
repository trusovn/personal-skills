# Verification Design: T-001.3 — Advisory discovery and installed composition

Check that foundation guidance exposes the installed advisory command while
preserving native check policy and ownership. Prove that the installed tools
capture and compare a separate repository with real analyzers, truthful failures,
and preserved source, index and reports. Guidance inspection proves documented
obligations; it does not qualify live agent compliance.

## Shared setup

Use disposable Git targets and a disposable projection of the distribution.
Install from that projection, then make it unavailable before measurement.
Leave the actual checkout and this session's active installation unchanged.
Run the installed CLI from a cwd outside both target and distribution. Remove
inherited Python helper paths and inspect resolved helper/default/pin paths to
exclude source-checkout and user-global fallback. The prepared pinned Python
and real Radon/Ruff are prerequisites confirmed by preflight; no download or
live model run is part of this design.

Record commands, interpreter/analyzer versions, target setup, exact input bytes,
outputs, exit codes and report paths. For every measurement, snapshot source
paths/bytes and real index bytes immediately before invocation and compare them
afterward. For report failures, also snapshot existing reports and requested
output siblings. Deliberate fixture edits occur between these snapshots.

Reuse current predecessor evidence and existing fixture facilities before adding
coverage. Relevant precedents are the installed launcher, settings, dirty-index,
empty-folder and collision cases in `tests/test_maintainability.py`, and the
relocated distribution, target preservation and drift/refresh cases in
`tests/test_install_development_skills.py`. `tests/staging_fixture_support.py`
owns setup-program staging if needed. These are precedents, not prescribed test
files or helpers. Accepted predecessor reports are
[T-001.1 acceptance](../T-001.1/reviews/acceptance-01.md) and
[T-001.2 acceptance](../T-001.2/reviews/acceptance-02.md). Reuse requires matching
current inputs and scope; add only missing installed-boundary evidence.

## Test cases

### V-01 — Advisory discovery preserves each native obligation

**Situation:** Concrete example repositories have the following discovery and
evidence states. Declare command, governed scope, policy reference, requiredness
and stage owner before applying the modified guidance.

| Case | Starting state | Action and expected result |
|---|---|---|
| V-01a | Existing registry/equivalent lists native checks | Trace one discovery pass to a compact handoff. It carries all five declared fields and the installed advisory reference without copying native policy or requiring a second registry. |
| V-01b | No registry; native commands are documented in agent instructions/map/native task configuration | Trace the documented discovery route. Those commands suffice; the same fields survive without introducing a registry or runner. |
| V-01c | No applicable native command exists | Trace the handoff. It records absence and invents no linter, typechecker or gate. |
| V-01d | A current aggregate result covers named constituents under the same scope/policy and checked-byte identity | Inspect the evidence handoff. It accepts applicable aggregate coverage without rerunning constituents merely for reporting. |
| V-01e | Required native evidence is missing | Inspect the handoff. The obligation remains owed under its native policy, with its owner and recovery route; advisory success does not fill the gap. |
| V-01f | Required native evidence covers older relevant bytes | Inspect the handoff. Stale evidence does not satisfy the obligation; recovery remains with the declared owner or an authorized focused run. |
| V-01g | Native gate governs the whole project; metrics compare affected Python paths | Trace scope into the handoff. The native gate retains whole-project scope and requiredness. |

**Why test this:** Discovery can silently weaken a hard gate or create duplicate
execution even when every command reference is valid.

**How to check:** Review concrete example handoffs against the modified source
`repo-foundation` and `architecture-guardrails`, including `templates/gates.yaml`.
Confirm that enabled advisory discovery identifies installed CLI, explicit
target setup, and independent target/default settings selection. The optional
template remains command discovery, carries no duplicated thresholds, and
does not itself require a new review stage. Existing conditional review duties
remain intact. This is structural policy evidence, not execution of the skills
by an agent. V-10 separately proves the mixed native/advisory tool outcome.

### V-02 — Integration guidance and installed membership agree

**Situation:** All four foundation skills named by AC-01/AC-02 and the optional
gates template are available as source. The installer has an explicit ownership
list and profile guide.

**Action:** Inspect `project-bootstrap` and `foundation-readiness-review` for
conflicts with the new discovery references. Trace all changed foundation
references through installer selections, managed shared files, profile guide,
README and focused installer coverage.

**Expected result:** Each inspected skill has a recorded change or no-change
disposition. Only integration-stale references change in bootstrap/readiness.
Actual additions are synchronized across installer declarations and guidance;
no installed dependency is reachable only through source. Policy/owners and
existing native rules are unchanged. The active installation is not refreshed.

**Why test this:** Correct source instructions do not establish a usable installed
contract, and stale bootstrap references can contradict that contract.

**How to check:** Compare source changes and disposable installed contents with
the explicit installer lists and guide. Review reference destinations and
dispositions, rather than relying only on phrase assertions. This is structural
evidence; V-03–V-10 exercise applicable runtime boundaries.

### V-03 — Dirty installed capture survives real additions and deletion

**Situation:** The separate target has committed Python, staged changes to one
file, different unstaged bytes in that same file, an untracked Python file, a
file to delete, and an untouched sibling. All are inside a selected folder.
Use small functions with independently countable complexity, such as four
unconditional `if` statements giving CC 5.

**Action and checkpoints:**

1. Capture a folder baseline through the installed CLI. Expect exit 0 and a
   complete format-5 JSON/text pair. Captured source bytes/hashes match the
   worktree, including untracked code, rather than HEAD or index contents.
2. Make a real edit to the tracked function, for example CC 5 to 7; add a file
   inside the captured folder and delete the captured deletion candidate.
3. Compare exactly the affected existing, added and deleted paths to that
   original baseline, saving a fresh report pair. Expect complete comparison,
   exit 0, CC 5 -> 7 with delta +2 for the retained function, added/removed
   classifications for new/deleted symbols, and no numeric history fabricated
   for the added symbol. Untouched siblings do not become affected rows.

**Expected result:** Both operations preserve source and the real index relative
to their invocation inputs. The baseline pair stays byte-identical after the
edit and comparison. Report file identities match supplied bytes, and effective
settings/runtime identity resolves to the target or this installation as
appropriate. Deleted paths are accepted through captured coverage.

**Why test this:** Separate unit proofs can miss installed wiring that captures
the wrong Git state, loses deleted paths or changes the real index.

**How to check:** Use real CLI subprocesses, real Git and real pinned analyzers.
Compare decoded snapshots and independently computed hashes to recorded fixture
bytes; inspect exact index bytes and staged content before/after. Check native
values against directly countable source/native output, not the adapter's own
calculation. Inspect path resolution as well as success after distribution
removal. This qualifies the local installed tool journey, not later workflow
retention enforcement or broader platform support.

### V-04 — Empty parent capture supports a later covered file

**Situation:** An explicitly selected existing directory has no included Python
files. Other prerequisites are valid.

**Action:** Capture that directory with the installed CLI. Add a Python file
inside it, then compare the added file against the saved empty baseline.

**Expected result:** Capture and comparison exit 0 and are complete. The baseline
records empty inventory with directory coverage. The added file has known prior
absence, current real values and unknown numeric before/delta values, not zero.
The original reports, source and index are preserved at each checkpoint.

**Why test this:** A successful ordinary baseline does not prove empty-folder
coverage can later authorize additions.

**How to check:** Run the real installed CLI and inspect saved coverage,
classification, native values and null numeric history. Reuse T-001.2's separate
ordinary-empty-measure, missing/excluded-folder and uncovered-addition refusals;
this case proves their positive installed composition boundary.

### V-05 — Each settings family selects its own origin

**Situation:** Use source with CC 5 and a three-argument function. Shipped targets
are 10/50/5; valid target overrides can set complexity to 3, statements to 3 and
arguments to 2. Keep native collection thresholds at zero. Each row starts clean.

| Case | Present target settings | Action and expected result |
|---|---|---|
| V-05a | Neither file | Installed measurement uses both shipped defaults. |
| V-05b | Maintainability only | Complexity target is 3; Ruff targets remain shipped. |
| V-05c | Ruff only | Complexity target remains 10; Ruff targets use target values. |
| V-05d | Both | Each family uses its target file and target values. |

**Expected result:** Every run completes with exit 0. Native counts remain
constant across rows. Each effective settings entry has the correct origin,
absolute path and SHA-256; shipped paths are adjacent to the installed runtime.
Target settings bytes remain unchanged. Breaches are successful observations.

**Why test this:** One target override must not select or suppress the other
family's fallback.

**How to check:** Reuse the existing real installed four-state settings case
when current. Its CLI reports and byte comparisons prove precedence; a settings
parser-only assertion would not prove installation-local resource resolution.

### V-06 — Invalid target settings fail without fallback

**Situation:** Start from V-05's valid successful controls and available real
tools. Change only the stated setting; request a fresh output path.

| Case | Invalid input | Action and expected result |
|---|---|---|
| V-06a | Target maintainability file contains malformed TOML | Installed measurement exits 2, identifies that file and does not fall back or publish a successful report. |
| V-06b | Target Ruff file contains malformed TOML | Same refusal for the Ruff file, despite a valid shipped default. |
| V-06c | Syntactically valid policy uses Boolean `complexity_target` or string `exclude_directories` | Installed measurement exits 2 before scanning/publication, names the file and invalid field, and leaves the target tree unchanged. |

**Why test this:** Silent fallback can create plausible metrics for a policy the
owner did not select. V-06c retains the predecessor's corrected failure boundary.

**How to check:** Reuse installed invalid-settings coverage and the accepted
full typed-field matrix from T-001.1; inspect exit/diagnostic/output absence and
tree preservation. Restore valid settings and observe successful measurement
to distinguish policy refusal from a broken setup or an always-failing command.

### V-07 — Missing tools produce an executable target-aware recovery reference

**Situation:** A separate target has valid settings and Python input, but neither
its native environment nor the invoking interpreter supplies the required pins.
No global/source helper fallback is available.

**Action:** Invoke the installed measurement command from the unrelated cwd.

**Expected result:** Exit 2 with explicit unavailable-tool evidence and a setup
recipe using the installed launcher and this target's root. No measurement is
claimed complete. No environment/package install, source/index change or report
overwrite occurs. Explicit setup selects the target-native destination and the
same installation's pinned requirements.

**Why test this:** A generic recipe can provision the wrong repository or hide
an implicit source/global dependency.

**How to check:** Reuse installed launcher refusal and setup-dispatch evidence
with captured subprocess arguments at the provisioning boundary. These checks
prove recipe execution/selection, not package download. V-03/V-05 are the
real-tool success controls; any new provisioning/network check needs approval.

### V-08 — Reports retain truthful labels, unknowns and immutable names

Use complete valid installed reports and real tools unless a row deliberately
changes the baseline format or creates an output collision.

| Case | Situation and action | Expected result |
|---|---|---|
| V-08a | Compare real numeric increases and decreases, including an over-target result | Exit 0; format-5 JSON and saved/console text use factual increased/decreased labels, retain values/targets/deltas and breach signals, and do not present a design verdict. |
| V-08b | Measure/compare an override-exempt function with a missing native count | Count and any uncomputable delta remain unknown, never zero or clean numeric improvement. |
| V-08c | Compare against an otherwise valid baseline with format 3 | Exit 2 with explicit incompatibility; no successful comparison or baseline rewrite. |
| V-08d | Repeat V-08c with format 4 | Same incompatible result. |
| V-08e | Save a second comparison against the original baseline under a fresh name | Exit 0; both comparison pairs coexist and all original report bytes stay unchanged. |
| V-08f | Requested JSON sibling alone already exists | Refuse overwrite with exit 2; sentinel bytes survive and the missing text sibling is not created. |
| V-08g | Requested text sibling alone already exists | Refuse overwrite with exit 2; sentinel bytes survive and the missing JSON sibling is not created. |

**Why test this:** A usable CLI can still misstate native evidence, accept an old
format, or destroy the reports needed to explain the comparison.

**How to check:** Reuse the full T-001.2 semantic cases, including its three
operations × two sibling collision matrix and both directions of missing native
counts. Add installed probes only where existing evidence lacks that boundary;
V-08f/g must establish installed refusal for comparison. Inspect report contents
and sibling existence, not exit codes alone. Each refusal retains V-03/V-08e's
valid comparison control. No second edit/reviewer correction journey is required
here; that remains T-005 scope.

### V-09 — Install, read-only drift and refresh preserve target ownership

**Situation:** A disposable target contains unrelated files, unselected skills
and helpers, target policy, environments/reports, source/index state and AGENTS
content outside the managed block. Use a disposable distribution whose selected
skills/shared resources can be changed without touching the actual checkout.

**Action and checkpoints:**

1. Fresh install: expect every declared managed skill, shared file and profile
   guide to match the distribution. Read-only check exits 0.
2. Change and remove representative managed resources, covering updated
   foundation skills and shared measurement files. Run drift detection; expect
   exit 1 with the changed/missing paths, no repair and an unchanged whole-tree
   snapshot. Reuse existing exhaustive managed-file coverage where current.
3. Explicitly refresh this disposable installation. Expect managed bytes restored
   and the next read-only check to exit 0.

**Expected result:** All three stages preserve unrelated target bytes, target
settings/environments/reports, real index and AGENTS content outside the marked
block. Managed resources remain self-contained. Neither the actual checkout's
active installation nor user-global installation is refreshed or used as fallback.

**Why test this:** Discovery updates can be correct in source but omitted during
refresh, or broaden the installer's ownership and destroy target evidence.

**How to check:** Reuse installer filesystem/Git journeys and managed-path
coverage, comparing byte snapshots at each step. Check all new shared files and
updated selected skills against declarations, then use V-03's distribution-free
invocation to corroborate runtime independence. Structural membership alone
does not prove preservation or executable operation.

### V-10 — A native hard failure survives successful advisory measurement

**Situation:** A disposable target declares a real existing static command,
native policy/config, whole-project scope, requiredness and owner. Supply valid
Python that violates a declared native rule while remaining measurable by the
pinned analyzers. Establish a clean control for the same command so a missing
tool or bad invocation cannot masquerade as the intended failure.

**Action:** Run that native command on the violating input and run the installed
advisory measurement on the same target bytes. Publish both observations through
the discovery handoff described in V-01.

**Expected result:** Native diagnostics name the seeded rule violation and the
native command fails under its declared policy. Measurement completes with exit
0 and real values. The published result retains the hard failure, full native
scope, requiredness and owner separately from the advisory result. Metric
success waives no gate and introduces no extra review stage or analyzer.

**Why test this:** Successful metrics can otherwise be presented as overall
verification success despite an existing required check failure.

**How to check:** Real separate-target subprocess execution with the existing
native executable and supplied rule configuration; record exact command,
fixture input, diagnostics and statuses in `results.md`. This proves tool
composition and the published distinction. V-01's handoff review proves the
instruction-only cases; neither establishes live agent obedience. R-05's later
fresh discovery independently reproduces this mixed result. R-06's later probe
invokes the installed command from another cwd and repeats one preservation or
failure case; this design does not perform those independent reviews.

## Coverage summary

| Promise from the brief | AC / risk row | Required cases |
|---|---|---|
| [Discover advisory CLI, settings/setup and preserve native authority](brief.md#work-and-acceptance-criteria) | AC-01 | V-01a–g, V-02 |
| [Inspect bootstrap/readiness; synchronize installer references without active refresh](brief.md#work-and-acceptance-criteria) | AC-02 | V-02, V-09 |
| [Real installed dirty capture/edit/compare, source independence, empty start and preservation](brief.md#work-and-acceptance-criteria) | AC-03 | V-03, V-04, V-08b |
| [Settings origins, truthful refusals, neutral reports and immutable output](brief.md#work-and-acceptance-criteria) | AC-04 | V-05a–d, V-06a–c, V-07, V-08a–g |
| [Fresh install, refresh and read-only drift preserve target ownership](brief.md#work-and-acceptance-criteria) | AC-05 | V-02, V-09, V-03 |
| [Hard/advisory separation and native scope/evidence duties](brief.md#work-and-acceptance-criteria) | AC-06 | V-01a–g, V-10 |
| [Registry/documented/absent commands, aggregate reuse, missing/stale proof, mixed result](brief.md#r-05--discovery-weakens-native-check-authority-ac-01ac-02-ac-06) | R-05 | V-01a–g, V-02, V-10 |
| [Installed edit/add/delete/empty journey, settings/format/unknown/collision and installation cases](brief.md#r-06--installed-first-proof-depends-on-source-or-loses-target-bytes-ac-03ac-05) | R-06 | V-03–V-09, including all named child cases |

## Source and revision

Source brief: docs/tasks/T-001.3/brief.md
Source brief revision: SHA-256 `1fa661307ec3a32b7b7d1ff707e5ba38a1a09f7fa8826f227a372601a3e96357`
Verification revision: 1
Authority: derived from the task brief and its cited normative sources, especially
project plan sections 6–7, T-001 and V-001/V-008; current contract index resolves
measurement, installation and foundation-tools authorities.
Status: ready

Preflight must confirm accepted predecessor outputs, actual installed paths,
the prepared pinned interpreter/analyzers and disposable source isolation before
execution. Follow the brief's targeted → measurement → installer → aggregate
verification order. Reuse applicable current aggregate coverage for architecture
and contract checks; report drift, failures and skips explicitly. No real-tool
skip satisfies AC-03/AC-04. This artifact contains planned evidence, not executed
behavioral results or implementation acceptance.
