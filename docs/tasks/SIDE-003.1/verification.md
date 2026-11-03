# Verification Design: SIDE-003.1 — Freeze the loading-cost baseline

One repo-only measurement script turns the current working tree into a deterministic, reproducible loading-cost record: per-file hashes/bytes/description characters for all 26 `SKILL.md` files, totals for all 26 and the 20-skill profile subset, a file-level read graph, representative-route inventories with summed sizes, and a command-prerequisites map. The main promises are: (1) the numbers reproduce byte-identically on an unchanged tree and every recorded route sum reproduces from the script; (2) the record is complete and honestly labeled (byte/character evidence, static unique-file estimates, not tokens); (3) measurement is read-only over `skills/`. No skill bytes change and no loader framework is built.

## Shared setup

- Start from a clean working tree (the brief's stop rule: an unrelated dirty tree is recorded, not silently measured). All commands run from the repository root.
- The script name is an implementation choice; below, `python3 tools/baseline_measure.py` stands for the new script and is substituted with the actual name at implementation.
- The plan's "Current source baseline" table (26 files, 404,992 total file bytes, 388,640 body bytes, per-file rows, measured at commit `aa94e28`) is the comparison oracle; the current tree is the baseline that matters, so a documented exact delta with cause is an equally valid outcome where the tree has moved since `aa94e28`.
- Counting definitions (plan, "Current source baseline"): body bytes = everything after the closing frontmatter delimiter including its following whitespace; description characters = normalized scalar text of the `description` field only, excluding other frontmatter fields.

## Test cases

### V-01 — A second run on an unchanged tree is byte-identical

**Situation:** The script has produced its output (machine-readable record and/or stdout) once; the working tree is unchanged between runs.

**Action:** Run `python3 tools/baseline_measure.py` twice; capture each run's full output.

**Expected result:** The two outputs are byte-identical, including every recorded route sum, hash, byte count, and description-character count. No run rewrites `skills/` or any pre-existing file.

**Why test this:** This replaces fail-first evidence for a read-only measurement task. A script whose output drifts between runs (unordered file discovery, timestamp embedding, unstable hashing) cannot serve as the attribution basis for every later SIDE-003 leaf.

**How to check:** `python3 tools/baseline_measure.py > /tmp/run1.txt && python3 tools/baseline_measure.py > /tmp/run2.txt && cmp /tmp/run1.txt /tmp/run2.txt` (or `sha256sum` both captures and compare). If the script writes the machine-readable record, compare two generated records with `cmp` as well. This proves determinism of the measurement itself, not correctness of the counting definitions — that is V-02.

### V-02 — Measured table matches the plan's table, or every delta is exact and explained

**Situation:** The script's per-file table for all 26 `skills/**/SKILL.md` files, plus totals for all 26 and the 20-skill profile subset.

**Action:** Compare the measured table against the plan's "Current source baseline" table row by row.

**Expected result:** Either (a) all 26 per-file rows agree on file bytes, body bytes, and description characters, and the totals agree (26 files, 404,992 file bytes, 388,640 body bytes), or (b) `baseline.md` records, per diverging file, the exact measured value, the plan's value, and the cause (e.g., tree drift since `aa94e28`). The 20-skill subset contains exactly the 20 skills the plan marks "Development profile: yes". Agreement or documented delta is recorded; silent divergence is a failure.

**Why test this:** The plan's table is the leaf's stated oracle. A script that disagrees with the plan without explanation, or that silently drops or adds files, corrupts the attribution basis for all later leaves.

**How to check:** Diff the measured table against the plan's table (script-assisted or manual row-by-row diff in review). File count check: the record lists exactly 26 files and the subset lists exactly 20. This is a data-comparison check, not behavioral verification; the counting definitions are independently confirmed by V-02b.

### V-02b — Counting definitions confirmed on one file by an independent method

**Situation:** One representative `SKILL.md` (pick one with multi-line or quoted frontmatter if any exists, else any file).

**Action:** Independently recompute that file's four metrics without the new script: SHA-256 (`sha256sum <file>`), file bytes (`wc -c <file>`), body bytes (bytes after the closing `---` delimiter line, including following whitespace), and description characters (normalized scalar text of the `description` field only).

**Expected result:** All four independently computed values equal the script's recorded values for that file.

**Why test this:** V-02 can pass by coincidence if the tree matches `aa94e28` while the script mis-defines body bytes or counts a non-description frontmatter field. This case pins the exact counting definitions from the plan.

**How to check:** Shell one-liners or a short throwaway check outside the committed script (e.g., `awk`/`sed` to split frontmatter, `wc -c` for body bytes, manual normalization for the description scalar). Record the spot-check values in review evidence; do not commit the throwaway check. Limits: proves the definitions on one file, not all 26 — full-table agreement is V-02's job.

### V-03 — Every recorded route sum reproduces from the script, and each route's file list is consistent with the read graph and named instructions

**Situation:** The record contains representative-route inventories for the plan's named routes (direct guided, packaged guided, high-assurance, corrections, optional evidence available/unavailable, a representative acceptance path), plus ordinary-route and conditional-route lists for SIDE-003.9 and .11–.17, each with a summed size.

**Action:** For each recorded route, feed the route's explicit file list to the script's supplied-file-list summing mode and compare the result with the recorded sum; separately check each route's file list against the read graph and the named skills' current instructions.

**Expected result:** Every route sum reproduces exactly from the script. Each route's file list contains the entry file, route-applicable references and templates, invoked sibling skills' entry files and their route references, and the repository's `AGENTS.md` — and no file that the read graph or the named instructions do not justify for that route. Route lists are unique-file lists labeled as static unique-file estimates.

**Why test this:** Later leaves report cumulative before/after costs per route from these lists. A sum that cannot be reproduced, or a route list that omits a required reference or includes an unjustified file, makes every later per-route delta wrong in one direction or the other.

**How to check:** For each route: `python3 tools/baseline_measure.py --sum <route file list>` (or the script's equivalent supplied-list mode) and compare with the recorded sum. Consistency of the lists is a document review against the read graph and the skills' instructions — keep it visibly separate from the sum-reproduction check. Limits: these are static unique-file estimates; repeated reads and rendered-catalog observation are explicitly out of this leaf's observable scope and remain unproved here.

### V-04 — The record is complete: all 26 files, the 20-skill subset, the read graph, route inventories, and command prerequisites

**Situation:** The finished `baseline.md` and machine-readable record beside the plan.

**Action:** Inspect the record against the brief's required-work items 1–3.

**Expected result:** The record contains: (a) per-file SHA-256, file bytes, body bytes, and description characters for all 26 files; (b) totals for all 26 and the 20-skill profile subset; (c) the file-level read graph (each skill's own `references/` entries plus cross-package reference links into other skills' `references/`); (d) the per-file size table for every instruction file any route can touch (26 entry files, every `references/` file, instruction-bearing module docs named in routes, and `AGENTS.md`); (e) the representative-route inventories with summed sizes; (f) the ordinary/conditional route lists for SIDE-003.9 and .11–.17; (g) the recording commit; (h) the command-prerequisites map (per affected skill, its owning suites/evals and how to run them, derived from `docs/development.md`, `docs/project-map.md`, and the `tools/verify.py` discovery roots).

**Why test this:** AC-02's coverage is a finite material inventory; omitting any one of these sections (most credibly the read graph, the recording commit, or the prerequisites map) would let a happy-path "numbers look right" review pass while later leaves lack their required basis.

**How to check:** Checklist review of the record against the eight items above, with the recording commit verified against the actual measuring commit (`git rev-parse HEAD`). Prerequisites-map commands are checked for existence (named suites/evals resolvable in `docs/development.md` / `tools/verify.py`), not executed here.

### V-05 — Counts are labeled as byte/character evidence, never tokens

**Situation:** The finished `baseline.md` and machine-readable record.

**Action:** Read the record's labels and any explanatory text.

**Expected result:** All counts are labeled as UTF-8 bytes or characters. No count is presented as tokens, and no bytes/4 (or similar) conversion appears as measured token savings. If a tokenizer was used (only if already available), its name and version are recorded; otherwise the record states the byte/character basis explicitly. Route sums are labeled static unique-file estimates.

**Why test this:** The plan forbids token claims from byte counts; a record that implies token savings would mislead every later leaf's reporting and the owner's decision basis.

**How to check:** Text review of the record for the words "token", "byte", "character", and "estimate"; grep is a reasonable aid (`grep -in token docs/tasks/SIDE-003/baseline*.md`), with judgment on each hit. This is a labeling check on recorded data, not behavioral verification.

### V-06 — Measurement is read-only: the working tree shows only the new script and baseline artifacts

**Situation:** After the script has been run (including twice, per V-01).

**Action:** Inspect the working tree for changes.

**Expected result:** `git status --porcelain` (plus `git diff --stat` for tracked files) shows only: the new `tools/` script, `docs/tasks/SIDE-003/baseline.md`, and the one machine-readable record beside the plan. Required preparation artifacts `docs/tasks/SIDE-003.1/verification.md` and `preflight.md` are expected separately. Nothing under `skills/`, `scripts/`, or `tests/` is modified, and no `__pycache__` or other incidental artifacts remain (run with `PYTHONDONTWRITEBYTECODE=1` or clean up).

**Why test this:** AC-03. A script that "helpfully" normalizes whitespace or rewrites a `SKILL.md` while measuring it would silently change the very baseline it is freezing and violate the leaf's read-only boundary.

**How to check:** `git status --porcelain` before and after the runs; diff the two listings. Confirm no `skills/` path appears. This observes the working tree only; it does not prove the script never opens files for writing in other environments — the architecture check (V-07) and code review cover the declared-imports side.

### V-07 — Architecture policy accepts the new `tools/` script

**Situation:** The new script is present under `tools/` with standard-library imports only.

**Action:** Run the canonical architecture check.

**Expected result:** The suite passes with no hard failures attributable to the new script (declared imports only, CLEAN policy satisfied).

**Why test this:** The brief's owning-suite evidence row; a script that violates the repository's architecture policy (undeclared imports, disallowed dependencies) is not acceptable even if its numbers are correct.

**How to check:** `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py` — zero failures. Report any skip or failure without treating it as pass. This is policy conformance, not behavioral verification of the measurements.

## Coverage summary

| Promise from the brief | AC / risk row | Required cases |
|---|---|---|
| Deterministic reproduction on an unchanged tree, including route sums ([brief §Verification, Fail-first row](brief.md)) | AC-01 | V-01 |
| Measured table matches the plan's table or records the exact delta and cause ([brief §Work item 4](brief.md)) | AC-01 | V-02, V-02b |
| Every recorded route sum reproduces from the script; route lists consistent with the read graph and named instructions ([brief §Verification, Targeted row](brief.md)) | AC-01 | V-03 |
| Record covers 26 files, 20-skill subset, read graph, route inventories, recording commit, and command prerequisites ([brief §Work items 1–3](brief.md)) | AC-02 | V-04 |
| Counts labeled byte/character, route sums labeled static unique-file estimates, no token claims ([brief §AC-02](brief.md); plan "Measurement and decision rules") | AC-02 | V-05 |
| Read-only over `skills/`: only the new script and baseline artifacts appear ([brief §AC-03](brief.md)) | AC-03 | V-06 |
| Architecture policy accepts the new `tools/` script ([brief §Verification, Owning-suite row](brief.md)) | — | V-07 |

## Source and revision

Source brief: brief.md
Source brief revision: 1
Verification revision: 1
Authority: derived from the task brief and its cited normative sources ([SIDE-003 plan](../SIDE-003/plan.md), "Current source baseline", "Measurement and decision rules" layers 1–2 basis, "Delivery sequence" phase 1; parent brief; repository `AGENTS.md`)
Status: ready

