# Verification Design: IMP-21 — Resume bundle import

Import each approved item with its specified name and bytes. After an
interruption, continue from the last complete item without duplication. Reject
invalid or oversized bundles before changing destination bytes.

## Shared setup

Use a fresh destination for each independent case, containing only
`sentinel.txt` with bytes `keep`. Retain its initial file list and bytes.
Approved bundle entries are `A.txt` = `alpha`, `B.txt` = `beta`, and
`C.txt` = `gamma`; the four-item bundle also has `D.txt` = `delta`.
Headers and manifests are valid unless a case explicitly changes one.

## Test cases

### V-01 — Import all three items once

**Situation:** `valid.bundle` contains A, B and C. No item has been imported.

**Action:** Run `bundle import valid.bundle` against the destination.

**Expected result:** The command succeeds. The destination contains exactly
A.txt = `alpha`, B.txt = `beta`, C.txt = `gamma` and sentinel.txt = `keep`.
Each approved item occurs once.

**Why test this:** An importer that refuses all bundles or writes incorrect
names or bytes must fail this check.

**How to check:** Exercise the public command and inspect actual persisted
file names and bytes after it exits. This proves command-to-filesystem behavior;
it does not prove interruption recovery, which V-02 checks separately.

### V-02 — Resume after the first committed item

**Situation:** The same valid three-item bundle starts in a fresh destination.

**Action:** Run the import and interrupt it immediately after A is durably
committed. Inspect the destination, then invoke the same import again.

**Expected result:**

1. At interruption, A.txt contains `alpha`, sentinel.txt contains `keep`, and
   no complete B.txt or C.txt exists. A is a complete committed item.
2. The next invocation resumes with B and succeeds. The destination contains
   exactly A.txt = `alpha`, B.txt = `beta`, C.txt = `gamma` and
   sentinel.txt = `keep`. A is not duplicated or imported again.

**Why test this:** A final correct file list alone could hide a restart that
reprocesses already committed items.

**How to check:** Use the real public command, durable destination and controlled
interruption at the first commit boundary. Retain the first checkpoint and
observe resumed item processing as well as final names and bytes. Do not seed a
completed A in place of exercising the first invocation. This sequence proves
the specified interruption boundary, not every possible crash timing.

### V-03 — Refuse each invalid input without changing destination bytes

**Situation:** Use separate fresh destinations and two-item bundles. Make only
the stated condition invalid so each intended validation guard is reached.

**Action:** Run `bundle import` with the bundle in each row.

**Expected result:**

| Case | Input | Result |
|---|---|---|
| V-03a | Malformed header; present valid manifest; two approved items | `invalid_header`; destination remains exactly sentinel.txt = `keep` |
| V-03b | Valid header; absent manifest; otherwise valid two-item bundle | `missing_manifest`; destination remains exactly sentinel.txt = `keep` |

**Why test this:** A generic exception or size refusal does not prove either
input guard. A rejection must not leave a partial import.

**How to check:** Inspect the public command's reported error and compare the
complete persisted destination inventory and bytes before and after. V-01 and
V-04a–V-04b are success controls against always refusing. These checks exercise
the actual write boundary, rather than checking a validation helper alone.

### V-04 — Accept the inclusive limit and refuse one item above it

**Situation:** Use separate fresh destinations and otherwise-valid bundles.

**Action:** Import the bundle in each row.

**Expected result:**

| Case | Submitted items | Result and destination |
|---|---|---|
| V-04a | A, B (two) | Success; exactly A.txt = `alpha`, B.txt = `beta`, sentinel.txt = `keep` |
| V-04b | A, B, C (three) | Success; exactly A.txt = `alpha`, B.txt = `beta`, C.txt = `gamma`, sentinel.txt = `keep` |
| V-04c | A, B, C, D (four) | `too_many_items`; exactly sentinel.txt = `keep`, with no imported item |

**Why test this:** Equality is permitted. Counting only remaining items or
writing some items before rejecting an oversized submitted bundle violates the
policy.

**How to check:** Run the public command and inspect success/error plus the
complete persisted inventory and bytes. Count the submitted bundle entries;
do not infer the limit from what was written. This proves the named boundary
values, not arbitrary bundle sizes.

## Coverage summary

| Promise from the fixture brief | AC / risk row | Required cases |
|---|---|---|
| [Persist approved items once](../../../skills/task-implementation-flow/task-verification-designer/evals/files/setup_fixture.py) | AC-01 | V-01 |
| [Resume from the first complete item](../../../skills/task-implementation-flow/task-verification-designer/evals/files/setup_fixture.py) | AC-02; ROW-RESUME | V-02 |
| [Reject invalid inputs before writing](../../../skills/task-implementation-flow/task-verification-designer/evals/files/setup_fixture.py) | AC-03; ROW-INVALID | V-03a, V-03b |
| [Enforce the inclusive submitted-item limit](../../../skills/task-implementation-flow/task-verification-designer/evals/files/setup_fixture.py) | AC-04; ROW-LIMIT | V-04a, V-04b, V-04c |

## Source and revision

Source brief: docs/tasks/IMP-21/brief.md
Source brief revision: lifecycle fixture in `skills/task-implementation-flow/task-verification-designer/evals/files/setup_fixture.py`, function `lifecycle`, as read on 2026-11-02
Verification revision: 1
Authority: derived from the fixture brief and its cited docs/import-policy.md
Status: ready

This is a manually authored worked example for SIDE-001, using the updated
source skill as a development specification. Source paths above refer to the
staged lifecycle fixture workspace. It is not installed-skill execution or live
model qualification. No importer tests were executed to create this example.
