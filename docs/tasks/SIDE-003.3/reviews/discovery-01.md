# Task Review Discovery Report: SIDE-003.3

| Field | Value |
|---|---|
| Producing stage | Installed `task-review-discovery` |
| Coverage completeness | Complete for the authorized editorial and local checks; live model routing was not authorized and is not claimed |
| Discovery iteration | First independent discovery |
| Created at | 2026-11-04, Europe/Lisbon |
| Repository root | `/Users/mtrusov/work/skill-sources/personal-skills` |
| Durable report | `docs/tasks/SIDE-003.3/reviews/discovery-01.md` |
| Authority | `docs/tasks/SIDE-003.3/brief.md`; SIDE-003 plan Description design, groups 3–4; parent brief and frozen baseline |
| Preparation | `docs/tasks/SIDE-003.3/verification.md`, revision 1; `docs/tasks/SIDE-003.3/preflight.md`, ready guided |
| Submission | SIDE-003.3 section of `docs/tasks/SIDE-003/description-results.md`, `READY_FOR_REVIEW` |

This report publishes evidence only. It gives no acceptance verdict, approved
deferral, or advancement. It applies only to the bytes below and does not review
or authenticate itself.

## 1. Discovery provenance

This separate reviewer session authored no reviewed production bytes. It read
the project-local installed `.agents/skills/task-implementation-flow/task-review-discovery/SKILL.md`
and its discovery-report template. Source skills were inspected as review
subjects, not substituted for the installed workflow. No installation refresh,
production edit, test edit, or subagent was used.

HEAD: `2504f1f249599ebf6d94d09a0ed95ff4ee5da3b4`.
SHA-256 of `git diff -- skills/ docs/tasks/SIDE-003/description-results.md`:
`ae28e852a7ae0db7b8b6b3e762c0da642870c0ebeaf2a12dbdfa27ae1032f3e4`.
The index has no differences from HEAD, independently checked with
`git diff --cached --name-only`.

Preparation SHA-256 identities:

| Artifact | SHA-256 |
|---|---|
| brief.md | `9284e44af286d343e84a407fe0bafd1e861854726a7179f6ecc44d06049322ca` |
| verification.md | `c499c932c175e5f6cda99fedec7f6d7575edbf45b3acff90447ee1fc97df6c1a` |
| preflight.md | `4e7b1f45b094c18ff8d5c0d2671d3359f90297cd1c6e33e1d7958d967b87457a` |

## 2. Findings

### F-01 [suggested P2] A distinct direct-edit activation condition is absent

| Field | Evidence |
|---|---|
| Location | `skills/task-implementation-flow/task-verification-designer/SKILL.md:3`; corresponding preserved-checklist and removed-detail claims in description-results.md |
| Trigger | An unpackaged direct edit needs verification because it has finite material cases, independently of non-obvious acceptance/failure/lifecycle semantics or test-design burden. Example: enumerate the three accepted configuration modes and their obvious expected outputs before a local edit. |
| Consequence | The discovery description no longer states this existing positive activation condition. A catalog-only selector must infer it from generic test-design needs; the body is unavailable before selection. The results section classifies the omission as removed detail and claims all routes survive. |
| Evidence | HEAD description independently lists `finite material cases` as an alternative trigger. Candidate lists `non-obvious acceptance, failure, lifecycle or test-design needs` and omits that alternative. The unchanged body, When this stage adds value, independently lists finite material cases or invariants where omission could permit false success. This is an activation reason, not report procedure. |
| Affected AC / rows | AC-01 positive trigger retention; AC-02 no dropped valid route; V-01d-FULL |
| Broken invariant | Description compression preserves every existing activation route; retaining an activation condition only in the body does not preserve the catalog trigger. |
| Credible sibling surface | Other unpackaged finite-case edits, such as an exhaustive set of allowed enum values or cardinalities with straightforward oracles and no lifecycle behavior. |
| Smallest corrective direction | Preserve the independent finite-case activation condition in the compressed description and correct its results checklist; retain the unchanged body. |

This is a confirmed editorial trigger omission. No observed model selection or
measured routing failure is claimed. Generic “test-design needs” could cause a
model to infer the route, but that possible inference does not establish the
explicit route preservation required here.

## 3. Completeness ledger

All V-01 rows use verification revision 1's exact prompts and the full HEAD and
candidate descriptions as setup. The oracle is editorial preservation of the
job, trigger, exclusions and plan group distinction, not a model response.
Submitted evidence for these rows is the results section's per-skill checklist.
The independent probe was direct comparison of each complete old/new scalar,
the cited body sections, and plan group rows 3–4. E means explicit invocation,
P implicit positive, N exclusion, and B nearest neighbor.

| Row | AC | Explicit case / independent observation | Result |
|---|---|---|---|
| V-01a-E | 01/02 | Explicit project-delivery-plan identity and composing-plan job preserved | pass editorially |
| V-01a-P | 01/02 | Ready foundation; flows and task inputs/outputs across composing tasks retained as flows/cross-task contracts | pass editorially |
| V-01a-N | 01/02 | Checkout implementation expressly excluded | pass editorially |
| V-01a-B | 01/02 | Existing-plan independent review belongs to verification, not plan authoring | pass editorially |
| V-01b-E | 01/02 | Explicit project-plan-verification identity and independent review job preserved | pass editorially |
| V-01b-P | 01/02 | Equivalent lightweight plan and fresh reviewer before implementation retained | pass editorially |
| V-01b-N | 01/02 | Repair/edit and implementation expressly excluded | pass editorially |
| V-01b-B | 01/02 | Creating plan/task map remains delivery-plan authoring | pass editorially |
| V-01c-E | 01/02 | Explicit task-brief-designer identity and bounded contract job preserved | pass editorially |
| V-01c-P | 01/02 | Tightening issue, acceptance/verification, sizing, justified splitting and handoff retained | pass editorially |
| V-01c-N | 01/02 | Product/architecture invention and repository readiness certification excluded | pass editorially |
| V-01c-B | 01/02 | Derived evidence scenarios remain verification designer's job | pass editorially |
| V-01d-E | 01/02 | Explicit task-verification-designer identity and implementation-neutral evidence job retained | pass editorially |
| V-01d-P | 01/02 | Supplied executable packages and direct edits with non-obvious lifecycle/failure cases retained | pass editorially for this representative prompt |
| V-01d-N | 01/02 | Tests/code, invented requirements and redesign excluded | pass editorially |
| V-01d-B | 01/02 | Current commands/ownership/prerequisites remain preflight | pass editorially |
| V-01e-E | 01/02 | Explicit task-preflight identity and bounded current-readiness job retained | pass editorially |
| V-01e-P | 01/02 | Readiness, commands/ownership and execution packets retained | pass editorially |
| V-01e-N | 01/02 | Implementation and requirements redesign excluded | pass editorially |
| V-01e-B | 01/02 | Contract repair remains brief design | pass editorially |
| V-01a-FULL | 01/02 | Complete original: small/medium, after foundation, before task planning, lightweight multi-task composition, system plan/task map, no implementation/overspecification; body map checked | pass editorially |
| V-01b-FULL | 01/02 | Complete original: delivery/equivalent plan, independent fresh review, coherent executable composition, authoritative inputs, three report verdicts, no repair; body map checked | pass editorially |
| V-01c-FULL | 01/02 | Complete original: request/issue/approved plan/specification/brief, create/tighten/gap-check, acceptance, sizing/coherent splitting, handoff/repair, lightweight delta and exclusions; body map checked | pass editorially |
| V-01d-FULL | 01/02 | Complete original includes finite material cases as an independent direct-edit trigger; remaining packaged/direct routes and exclusions retained | fail — F-01 |
| V-01e-FULL | 01/02 | Complete original: current safe execution readiness, commands/ownership/packet, derived verification, durable packages, inline requests, exact high-assurance freshness, ready/blocked, exclusions; body map checked | pass editorially |
| V-02 | 03 | Exactly five changed skill paths; masked-description HEAD/worktree comparison identical; names/paths unchanged; prior results preserved | pass — independent byte probe |
| V-03 | 01/03 | Recomputed current catalog matches submitted after JSON; before touched hashes equal HEAD; 26/20 counts; delta sums and body invariance | pass — independent measurement probe |
| V-04 | 03 | Assertions inspected; 16 preparation and 14 flow-guide tests rerun; five validators rerun; installer/profile guide/shared list/tests/README inspected | pass for local text/package consistency |
| AC-01 | all | Records, counts and most triggers present; finite-case trigger missing | fail — F-01 |
| AC-02 | all | Nearest neighbors retained; procedural maps valid, but one activation alternative moved out of description | fail — F-01 |
| AC-03 | all | Only description bytes in five skills; no quoted assertion requires change; validators pass | pass |

## 4. Adversarial and removed-detail checks

The adversarial editorial probe distinguishes a direct edit driven solely by
finite material cases from the representative lifecycle/failure prompt. That
extra case exposes F-01 despite all twenty representative variants passing
editorial comparison. No process lifecycle, persistence/schema validator,
concurrency, or cleanup probe is applicable to this metadata-only diff.

Removed procedural inventories were independently traced:

| Skill | Existing body authority / observation |
|---|---|
| project-delivery-plan | Core stance, Required outputs, Planning depth rule, Protocol 2–9 retain artifacts/state, interfaces, flows, ownership, producer/consumer closure, placement and evidence. “Lightweight” retains the non-full-SDD route. |
| project-plan-verification | Independence requirement, Inputs, Output, Verdicts and Protocol retain authoritative reconstruction, flow/closure/interface/lifecycle/invariant/dependency checks and separate report. |
| task-brief-designer | Guided and Workflow retain small additions; Sizing and decomposition contract retains coherent bounded splitting; Preparation and permission to start separates contract and execution readiness. |
| task-verification-designer | When this stage adds value, Artifact location, Authority/coverage/revision and Output retain state/finite cases, detailed evidence, compact specification and separate verification.md. Finite cases are retained in the body but are a trigger: this map does not close F-01. |
| task-preflight | Choose the profile, Guided/High assurance, Guided workflow and Output retain safe execution checks, canonical durable readiness, inline requests and freshness mechanics. |

## 5. Independent probes and commands

All ran from the repository root with local Python/Git. No providers, servers,
network, dependencies, tests, eval fixtures or installed files were changed.

| ID | Exact command or reproducible probe | Result / limit |
|---|---|---|
| DISC-01 | `git diff -- skills/`; full scalar/body and plan group comparison described above | F-01; all other rows compared independently |
| DISC-02 | Python byte/measurement probe below | exit 0; five description-only paths; other 21 inventory rows identical; delta 1,246 |
| DISC-03 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_task_preparation_contracts.py` | exit 0; 16 tests, no skips |
| DISC-04 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_task_flow_guides.py` | exit 0; 14 tests, no skips |
| DISC-05 | `python3 skills/skill-creator/scripts/quick_validate.py <package>` for each of the five changed package directories | all exit 0, `Skill is valid!`; structural only |
| DISC-06 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_architecture.py` | exit 0; 4 tests, no skips; required repository handoff check, not an aggregate |
| DISC-07 | `python3 tools/check_contracts.py --root .` | exit 0; 7 subsystems, 22 indexed references; structural only |
| DISC-08 | `rg -n 'description\|implementation-neutral\|A supplied executable task package always requires' tests/test_task_preparation_contracts.py tests/test_task_flow_guides.py` and targeted installer/guide/test/README reads | implementation-neutral is retained; other relevant quoted phrase is in unchanged body; stable package copying/identity requires no installer edit |

DISC-02 reproducible command (the original run also printed each count and the
diff digest recorded above):

```sh
python3 - <<'PY'
import hashlib, json, re, subprocess
from pathlib import Path
paths = subprocess.check_output(['git','diff','--name-only','--','skills/'], text=True).splitlines()
before = json.load(open('/tmp/side0033-before.json'))
after = json.load(open('/tmp/side0033-after.json'))
current = json.loads(subprocess.check_output(['python3','tools/baseline_measure.py']))
assert current['skills'] == after['skills'] and current['totals'] == after['totals']
b = {x['path']: x for x in before['skills']}
a = {x['path']: x for x in after['skills']}
assert len(paths) == 5
delta = 0
for p in paths:
    old = subprocess.check_output(['git','show','HEAD:' + p])
    new = Path(p).read_bytes()
    mask = lambda v: re.sub(rb'^description:.*$', b'description: SENTINEL', v, flags=re.M)
    assert mask(old) == mask(new)
    assert hashlib.sha256(old).hexdigest() == b[p]['sha256']
    delta += b[p]['description_characters'] - a[p]['description_characters']
for p in set(b) - set(paths):
    assert b[p] == a[p]
for k in ('all', 'development_profile'):
    assert before['totals'][k]['description_characters'] - after['totals'][k]['description_characters'] == delta
    assert before['totals'][k]['body_bytes'] == after['totals'][k]['body_bytes']
print(delta)
PY
```

Observed reductions: delivery 687→302; plan verification 649→307; brief
designer 571→331; verification designer 487→335; preflight 453→326.
All-26: 13,030→11,784 characters, body bytes 388,640 unchanged.
Profile-20: 9,391→8,145 characters, body bytes 320,123 unchanged.
The frozen baseline is not overwritten. The earlier accepted .2 reduction of
1,418 accounts for the difference from frozen totals of 14,448/10,809; current
cumulative reduction is 2,664. These are character/byte measurements, not
tokens or behavioral routing evidence.

Submitted `/tmp/side0033-{preparation,guides,architecture,contracts}.log` files
were inspected and corroborated by DISC-03/04/06/07. Their success does not
close F-01. No regression file was added; the finite-case editorial input in
F-01 is the reviewer regression to repeat after correction.

## 6. Aggregate-gate record

| Field | Value |
|---|---|
| Exact command | `python3 tools/verify.py` |
| Status | not run |
| Owner/stage | SIDE-003.18, not this discovery pass |
| Reason | Leaf explicitly assigns aggregate qualification there; current targeted finding also suppresses a completeness-only aggregate |
| Current evidence | Targeted ledger completed; F-01 remains; local structural and owning checks do not erase it |

Live catalog-routing probes: not run. No budget approval was supplied. They
remain with the coordinator for separate approval; neither metadata checks nor
editorial comparisons are behavioral qualification.

## 7. Scope and baseline comparison

The reviewed tracked diff contains the five skill scalars and a 115-line
append-only SIDE-003.3 results section. Existing SIDE-003.2 results are preserved.
The untracked preparation files are declared package artifacts, not unrelated
user work. There is no unexplained overlap. Brief, baseline, measurement tool,
policy, registry and installer surfaces have no tracked diff. Active installed
copies are intentionally separate from source changes.

Exact `git status --short` immediately before report creation:

```text
 M docs/tasks/SIDE-003/description-results.md
 M skills/project-delivery-plan/SKILL.md
 M skills/project-plan-verification/SKILL.md
 M skills/task-implementation-flow/task-brief-designer/SKILL.md
 M skills/task-implementation-flow/task-preflight/SKILL.md
 M skills/task-implementation-flow/task-verification-designer/SKILL.md
?? docs/tasks/SIDE-003.3/preflight.md
?? docs/tasks/SIDE-003.3/verification.md
```

Post-report status is the same snapshot plus exactly
`?? docs/tasks/SIDE-003.3/reviews/` (containing only discovery-01.md), verified
after creation. Tracked diff digest, preparation digests and index identity
remain unchanged. The report is the sole repository write of this session.

## 8. Limits and residual risks

| Type | Limit | Owner / next action |
|---|---|---|
| Confirmed finding | F-01 is failed required editorial behavior, not residual risk | Separate acceptance decision consumes the finding; implementer owns any subsequent correction |
| Optional behavioral evidence | All live E/P/N/B selections unexecuted; no claim that models select or reject a skill correctly | Coordinator obtains separate approval before routing evaluation |
| Deferred aggregate/distribution evidence | No aggregate or installed profile refresh/check run | SIDE-003.18 owns qualification; no waiver recorded |

## 9. Coverage completeness and next route

Discovery coverage is complete for the leaf's required editorial/local scope:
all twenty representative variants, full-original routes, removed-detail maps,
three remaining verification cases and all three ACs have a disposition.
Complete coverage includes a failed route; it does not mean the change is clean.
No required row is silently omitted. No acceptance decision is made here.

Next: give the separate acceptance decision call the brief, current scoped
diff, this report, verification revision 1, ready preflight and its decision
context, plus F-01's finite-case regression. Do not advance or correct on the
authority of this report alone.

## 10. Discovery continuation

```markdown
Discovery continuation:
- Iteration / byte identity: first independent pass; HEAD 2504f1f249599ebf6d94d09a0ed95ff4ee5da3b4; scoped diff SHA-256 ae28e852a7ae0db7b8b6b3e762c0da642870c0ebeaf2a12dbdfa27ae1032f3e4; index equals HEAD.
- Coverage rows: V-01a/b/c/d/e-E/P/N/B all pass editorially; V-01a/b/c/e-FULL pass; V-01d-FULL fail F-01; V-02/03/04 pass; AC-01/02 fail F-01; AC-03 pass. Live selections unexecuted and not required without approval.
- Finding IDs: F-01 suggested P2, finite-material-case direct-edit trigger omitted from verification-designer's catalog description.
- Finding/scenario continuity: no prior discovery; producer claimed all routes retained; independent full-original comparison contradicts that for finite cases. Corrective owner implementer; evidence owner fresh discovery reviewer; authority/decision owner separate acceptance reviewer. Siblings: other exhaustive enum/cardinality direct edits with obvious oracles, no lifecycle/test-design burden.
- Preparation/context: docs/tasks/SIDE-003.3/brief.md; verification.md revision 1; ready preflight.md including decision context; SIDE-003 plan groups 3–4 and frozen baseline.
- Reviewer regressions: no new files; repeat F-01's direct-edit finite-case-only editorial comparison against HEAD original, candidate, body trigger and results claim. Repeat DISC-02 for corrected bytes.
- Aggregate gate: python3 tools/verify.py not run; SIDE-003.18 owns it; targeted finding also suppresses a completeness-only aggregate. Live routing requires separate approval.
- Next: separate task-acceptance-review decision with current diff, this report and preparation references before any correction/advancement decision.
```
