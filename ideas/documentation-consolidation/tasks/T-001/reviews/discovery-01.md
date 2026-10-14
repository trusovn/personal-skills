# Task Review Discovery Report: T-001 — Audit preservation and retirement eligibility

| Field | Value |
|---|---|
| Producing stage | task-review-discovery; project-local installed skill |
| Coverage completeness | complete — all six scenarios have current dispositions; V-05 fails |
| Discovery iteration | First independent discovery |
| Created at | 2026-10-14T13:12:56Z |
| Repository root | /Users/mtrusov/work/skill-sources/personal-skills |
| Durable report path | ideas/documentation-consolidation/tasks/T-001/reviews/discovery-01.md |
| Task brief | ../brief.md |
| Verification / context | ../verification.md revision 1; ../preflight.md including Decision context; cleanup-v1 project-plan.md and task-map.json |
| Submission | ../results.md; NON-COMPLETE, overall BLOCKED |

This report publishes evidence only. It gives no acceptance verdict, approved
deferral or advancement. It applies only to the identified reviewed bytes.
It does not review or authenticate itself. No production, tests, plans,
preparation, prior reports, index or refs were changed by this discovery.

## 1. Discovery provenance

This session authored none of the reviewed implementation bytes. Its only
repository write is this report. Evidence below is independently corroborated
for the current submission, except historical claims explicitly attributed
to their original producers.

Selected skill: .agents/skills/task-implementation-flow/task-review-discovery/SKILL.md.
Its sibling references/discovery-report-template.md supplied this report format.
No global installation, helper lifecycle or subagent was used.

HEAD: `b65f900e7515ccfe36335b793b0c058b7b2bfa8c`.
Reviewed implementation: the untracked addition of results.md, SHA-256
`4c11c83aac32280b407e4696517c788049b78189ca152f6838ea2b4460698170`.
No HEAD or index version exists for this new output. Tracked staged and unstaged
diffs are empty. The artifact is task-owned and within allowed scope.

## 2. Findings

### F-01 [suggested P2] Optional audit instrumentation wrote Git refs despite AC-05

| Field | Evidence |
|---|---|
| Location | results.md:300–322; active helper .agents/scripts/run_evidence.py:266–284 |
| Trigger | Use the optional run-evidence snapshot lifecycle during this read-only audit. The helper calls git update-ref at each snapshot boundary. |
| Consequence | Audit execution violates AC-05 and the no-Git-ref-write scope. Unchanged branch refs and original file bytes do not satisfy the all-refs preservation oracle. |
| Independent evidence | DISC-01 reproduces final refs digest 9ae5a239…c3f135. Removing exactly the disclosed finish-ref line reproduces audit-start digest 66fb6142…df211. DISC-03 traces update-ref in the actual installed helper. |
| Affected AC / scenario | AC-05; V-05; R-04 / INV-006 |
| Broken invariant | Audited inputs, index and refs remain unchanged; instrumentation does not expand the authorized write boundary. |
| Credible sibling surface | The same helper writes begin/recovery snapshots as well as finish. The submission states that its audit-start capture followed begin, so the start digest already included the begin ref. A finish-only baseline comparison cannot establish no ref writes throughout the invocation. |
| Smallest corrective direction | Exclude every ref-writing evidence lifecycle from read-only audits. Preserve the disclosed exception and route its current disposition to separate acceptance/owner authority; do not delete refs to conceal or retroactively erase the occurrence. |

The submission already discloses this finding and makes no completion claim.
This report confirms the exception; it does not request a new qualification
campaign or claim other instrumentation defects.

## 3. Completeness ledger

The ledger was defined as V-01–V-06 before targeted probes. Every material
AC and R row maps to these scenarios. No prior T-001 discovery exists.

| Row | AC / invariant | Cases; setup / oracle | Submitted evidence | Independent probe / current evidence | Result / reason |
|---|---|---|---|---|---|
| V-01 | AC-01; R-01 | Compare actual Git/filesystem membership, hashes, modes, versions, ignored exclusions and external-content boundaries with manifest. Cover tracked, staged, unstaged, untracked, ignored and divergent/type cases when present. | 517 INCLUDE rows; 182 C candidates; five precise exclusions; no divergence or external-content boundary. | DISC-01 checks every row against filesystem, index and HEAD; zero missing/extra/identity/version errors. 517 regular stage-0 entries, 182 candidates, 15 future-work files. No tracked divergence/deletion/symlink/gitlink; no .gitmodules/.gitattributes or candidate LFS pointer. Only new results.md is untracked. DISC-02 confirms all five exclusion identities and embedded inputs are inventoried. | pass — exact inventory agrees; absent variants are established from current state, not fabricated |
| V-02 | AC-02/04; R-02 | Reconcile all candidate families with original result/review evidence, unfinished/unknown statuses and retained families; challenge apparent completion using source verdicts. | 32 family rows plus index, old plan and old task map; unknowns preserved; T-005 reassessment and qualification limits cited. | DISC-02 enumerates all 32 families, submissions and acceptance records. DISC-03 reads T-005 reassessment, .2 INCONCLUSIVE, .3 partial, .6 documentary ACCEPT, Q-01 unrun handoff, and final discovery limits for .1/.2/.3 installer tasks. Old planning acceptance is not delivery acceptance. User confirms Q-003 in this session. | pass — no completion inferred from structural registration; all 182 candidate paths map to family evidence or explicit unknown and gated disposition |
| V-03 | AC-03; R-03 | Trace real readers through constants, embedded data, setup roots and evidence pointers; compare input closure, owner scenarios/oracles/selectors and installer coupling. | 13 live candidate inputs, composition module selector, active setup/helper closure, historical checker and navigation classes. Suites selected, not run. | DISC-02/03 trace composition reader lines 33–67, 84–235, 291–419, 1266–1355; embedded JSON gives 47 cases, 11 sets, five handoffs. route-cases reaches candidate setup_consumer.py, parents[3], active implementer setup and answer-free consumer Git baseline. Local package set reads fixtures/results/three receipts; .6 brief is an evidence pointer. All 13 live paths have inventory identities. Generic validators take caller-supplied paths; synthetic fixture paths and older spike records are not active original reads. Installer sources contain no candidate path. | pass — current source/data closure agrees with audit; migration behavior remains for T-003 |
| V-04 | AC-04; R-02 | Reconcile actual owner decisions, unresolved global gates, per-candidate gates and overall assessment; no silence/plan acceptance as authority. | Q-001/Q-003 owner quotes; Q-002 recommendations only; all candidates archive/dependency gated; overall BLOCKED. | DISC-04: owner explicitly answers “Confirm both decisions” to exact Q-001/Q-003 scope described below. Q-002 remains publication/destination/navigation choice for owner/T-002. Submission says recommendations are not authorization and no deletion occurred. | pass — decisions now independently sourced; unresolved Q-002 is a truthful downstream gate |
| V-05 | AC-05; R-04 | Compare audit-start/final input content, index and refs; inspect attributed output and forbidden effects. | 517 inputs unchanged; finish ref added; strict ref oracle explicitly fails. | DISC-01 verifies every protected identity, normalized/raw index, HEAD and status. Final refs hash matches submission; minus finish equals start. DISC-03 installed helper confirms ref mutation. | fail — F-01; additive implementation-side ref mutation, not user drift |
| V-06 | AC-05; R-04 | Compare preflight baseline with actual occurrence and recorded ref drift; changed facts must be reinspected or blocked without overwriting user work. | Planning commit revalidated; ref drift disclosed/reinspected; NON-COMPLETE and BLOCKED maintained. | DISC-01 current brief/verification digests match readiness bindings. DISC-03 preflight-HEAD-to-current diff of all old audited roots is empty; current inventory, HEAD/index and final refs are rechecked. Ref facts are current and the unsatisfied invariant remains visible. | pass — reinspection does not turn V-05 into a pass; no restoration performed |

Owner confirmation in DISC-04: the reviewer asked whether to preserve the full
tracked repository plus audit/review outputs, exclude generated/cache/Finder/
unrelated handoff files, and retire all 182 candidates only after archive and
dependency gates while retaining the brief qualification-limit note. The owner
answered **“Confirm both decisions.”** This is current confirmation; it does
not authenticate the earlier conversation or authorize archive publication.

## 4. Adversarial evidence checks

- Version equality was checked separately for HEAD, index and worktree for every
  tracked path; matching status alone was not used as proof.
- Membership reconciliation used exact sets, not sample counts. All candidate
  families, retained future-work and old plan review are accounted for.
- Actual INCONCLUSIVE/partial/unrun source records challenge any completion
  inference. Q-003 disposition remains separate from historical proof.
- Embedded staging fixtures and local package inputs were inspected, including
  the candidate setup program missed by a constants-only search.
- No required executable schema, process-lifecycle or migration boundary is
  claimed by this evidence-only audit. Schema validation, runtime staging and
  consumer suite execution are not T-001 requirements and were not run.

## 5. Independent probes and command records

All commands ran from the repository root, offline, without escalation.
Read commands caused no repository content writes. Python used
PYTHONDONTWRITEBYTECODE=1. No fixture or long-lived process was launched.

| ID | Probe / exact command record | Purpose | Observed result |
|---|---|---|---|
| DISC-01 | Exact inventory/version/state Python command in Appendix A | V-01/05/06 | exit 0; 517 entries/rows, no extras/problems; hashes and status below |
| DISC-02 | Exact family/embedded-closure/exclusion Python command in Appendix B | V-01/02/03 | exit 0; 32 families, none omitted; 47 cases, 11 sets, five handoffs; five exclusion identities agree |
| DISC-03 | Read-only static probes listed below | V-02/03/05/06 | Source traces and original verdicts corroborate ledger. An early combined read exceeded output limits; bounded later reads supplied decisive evidence. No suite results inferred. |
| DISC-04 | request_user_input_async with Q-001/Q-003 confirmation question reproduced in §3 | V-02/04 | owner confirms both decisions; no Git/file side effects |
| DISC-05 | Rerun Appendix A; git status --short --untracked-files=all; git diff --check; git diff --no-index --check /dev/null ideas/documentation-consolidation/tasks/T-001/reviews/discovery-01.md | Reviewer write isolation | All 517 identities, results/preparation digests, HEAD, index and refs unchanged; only this new report added. Initial output check found a report-only blank line at EOF; removed before final check. |

DISC-03 exact decisive commands (read-only):

~~~sh
git diff --raw
git diff --cached --raw
git diff 32edda26bf82b0a494993afc17e564722e51808d HEAD -- docs/tasks docs/project-plan.md docs/task-map.json docs/project-plan-review.md docs/future-work
rg -l 'docs/tasks|docs/project-plan|docs/task-map|T-005\.1|T0051|T0034' tests scripts skills README.md docs/future-work docs/project-plan-review.md --glob '*.py' --glob '*.md' --glob '*.json'
sed -n '1,110p' tests/test_review_composition.py
sed -n '110,240p' tests/test_review_composition.py
sed -n '240,325p' tests/test_review_composition.py
sed -n '350,395p' tests/test_review_composition.py
sed -n '1255,1355p' tests/test_review_composition.py
cat tests/review_fixture_support.py tests/staging_fixture_support.py docs/tasks/T-005.1/setup_consumer.py
sed -n '24,63p' scripts/install_development_skills.py
sed -n '265,286p' .agents/scripts/run_evidence.py
sed -n '1,40p' docs/tasks/T-005.6/evidence/check_report.py
sed -n '1,85p' docs/tasks/T-005/reassessment.md
sed -n '1,55p' docs/tasks/T-005.2/reviews/acceptance-01.md
sed -n '1,55p' docs/tasks/T-005.6/reviews/acceptance-01.md
sed -n '1,32p' docs/tasks/T-005.3/reviews/discovery-01.md
sed -n '1,25p' docs/tasks/Q-01/qualification-handoff.md
sed -n '1,22p' docs/project-plan-review.md
rg -n 'READY_FOR_REVIEW|No findings|INCONCLUSIVE|ACCEPT|unrun|partial|owed|maintainability|acceptance' docs/tasks/INT-FLOW-001/results.md docs/tasks/INT-FLOW-001/reviews/discovery-01.md docs/tasks/Q-01/qualification-handoff.md docs/tasks/T-005.3/reviews/discovery-01.md docs/tasks/T-004.1/reviews/discovery-02.md docs/tasks/T-004.2/reviews/discovery-04.md docs/tasks/T-004.3/reviews/discovery-03.md docs/tasks/TEST-STAB-001.1/reviews/discovery-01.md docs/future-work/FEATURE-MAP.md
rg -n 'docs/tasks|docs/project-plan|docs/task-map' skills/README.md skills/project-plan-verification/scripts/verify_plan_artifacts.py skills/project-delivery-plan/scripts/validate_task_map.py skills/project-direction/evals/files/setup_fixture.py
~~~

Preparation/authority reads: cat of brief.md, verification.md, preflight.md,
root AGENTS.md, owner direction brief and cleanup task-map.json; bounded reads
of results.md sections 1–245 and 248–339. Skill and template were read before
discovery. Searches did not establish behavioral outcomes on their own.

## 6. Aggregate-gate record

| Field | Value |
|---|---|
| Gate | Full manifest, obligation and consumer reconciliation, as required by brief |
| Exact command | not run — manual aggregate, no separate prescribed executable command |
| Status | not run |
| Owner / stage | This reviewer / initial discovery |
| Reason | Decisive targeted V-05 failure suppresses aggregate reconciliation under the discovery skill. Other independent targeted rows were completed. |
| Current evidence | V-01/02/03/04/06 pass; V-05 fail. No broad test suite or prior aggregate label substitutes for these results. |

No consumer suite was run. The T-003 selector
`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_review_composition.py`
is selected historical wiring for later migration proof, not this discovery's gate.
No additional gate or test command was added.

## 7. Scope and baseline comparison

Preflight HEAD was 32edda26…; current HEAD b65f900e… committed the planning
package. The diff of all original candidate/retained roots between those commits
is empty. Preparation byte bindings match current files. All preparation files
are tracked original P inputs; results.md is the sole reviewed new output.

| Identity | Current observation |
|---|---|
| HEAD | b65f900e7515ccfe36335b793b0c058b7b2bfa8c |
| Normalized index SHA-256 | 71e86e4b76095c4b0611e08fb017e6d6a9b87c5e6dfee29b305ca4469a51586c |
| Raw index SHA-256 | 7a225e39f132005de82de9c15aba7e0a933c9e665f5ce556339c9cba644da7d0 |
| Final refs SHA-256 | 9ae5a239c74eeb8fb4ddde47257b1c9000b911822d04dd60a0dcb194b7c3f135 |
| Audit-start refs SHA-256 (minus finish) | 66fb6142c08926570a5839c6a87091bc3f31dfb744deeccb70e4202f207df211 |
| Brief SHA-256 | 5f417e6d157800711d6d763592c4173932118c9dec7c18190dec947ac0404d42 |
| Verification rev 1 SHA-256 | bbeafc7a85d7ef5f3c3974f5b178a0e2cf35efb9dbfa82d35faa21d3dc17f105 |
| Preflight SHA-256 | 9d79cb44aa6d152536563a42928869a781bedd238277cabe48fd09615310612d |
| Results SHA-256 | 4c11c83aac32280b407e4696517c788049b78189ca152f6838ea2b4460698170 |

Exact reviewed status immediately before report write:

~~~text
?? ideas/documentation-consolidation/tasks/T-001/results.md
~~~

Observed post-report status:

~~~text
?? ideas/documentation-consolidation/tasks/T-001/results.md
?? ideas/documentation-consolidation/tasks/T-001/reviews/discovery-01.md
~~~

DISC-05 reran Appendix A after the report write: all 517 inventory rows and
results/preparation identities still match; HEAD, normalized/raw index and refs
remain equal to the pre-report observations. Only the new report entry differs.
No unexplained overlap, staged work or unrelated untracked files was absorbed.

## 8. Questions and residual risks

No required row remains blocked or unchecked. Q-001/Q-003 are confirmed in this
session. Q-002 remains an explicit downstream owner/T-002 gate for archive
choices and publication authority; this audit does not need publication to
describe that blocker accurately.

Historical missing raw records, role qualification, recovery and migration
equivalence remain unproved, as stated in the audit. No historical acceptance
or independent discovery report is regraded here. Current byte equality
corroborates audited inputs but cannot prove all unobserved historical actions.

## 9. Coverage completeness and next route

Coverage is complete for the current T-001 evidence output, with F-01 and
V-05 failure explicitly retained. Complete coverage does not mean success or
permission to advance.

Next: a **separate task-acceptance-review decision call** consumes the brief,
the current untracked results.md addition, this report, verification revision 1,
ready preflight and its Decision context, cleanup-v1 authority, all six rows,
F-01 and current owner confirmation. It decides the disclosed ref exception's
disposition. No advancement was performed.

## 10. Discovery continuation

~~~markdown
Discovery continuation:
- Iteration / byte identity: first discovery; HEAD b65f900e7515ccfe36335b793b0c058b7b2bfa8c; results.md SHA-256 4c11c83aac32280b407e4696517c788049b78189ca152f6838ea2b4460698170; untracked output; no staged/unstaged tracked diff.
- Coverage rows: V-01 pass; V-02 pass; V-03 pass; V-04 pass; V-05 fail (AC-05 ref mutation/F-01); V-06 pass (current reinspection, failure retained).
- Finding IDs: F-01 suggested P2, already disclosed by producer and independently corroborated.
- Finding/scenario continuity: no prior T-001 report. Producer's inventory/evidence/consumer claims corroborated; producer V-05 failure persists. No incomplete rows. Siblings: begin/recovery/finish snapshot ref writes. Correction owner: T-001 implementer for any authorized new bytes; evidence owner: fresh discovery after correction; disposition/authority owners: separate acceptance and repository owner. Q-001/Q-003 confirmed during this discovery; Q-002 remains downstream owner gate.
- Preparation/context: ideas/documentation-consolidation/tasks/T-001/brief.md; verification.md revision 1 and recorded hashes; ready preflight.md including Decision context; cleanup-v1 project-plan.md/task-map.json; owner-approved direction brief.
- Reviewer regressions: no files added; rerun Appendix A ref/index/byte comparison and static helper trace if corrected. Preserve all six scenario IDs.
- Aggregate gate: not run; owner this initial discovery; manual full reconciliation suppressed by decisive V-05 failure; no executable aggregate command prescribed.
- Next: separate task-acceptance-review with current scoped addition, this report, all preparation/authority references, F-01 and all ledger rows.
~~~

## Appendix A — Exact DISC-01 command

~~~sh
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import subprocess, pathlib, hashlib, re, stat, json
p=pathlib.Path('.'); report=p/'ideas/documentation-consolidation/tasks/T-001/results.md'
sha=lambda b:hashlib.sha256(b).hexdigest()
git=lambda *a:subprocess.check_output(['git',*a])
rows={}
for line in report.read_text().splitlines():
 m=re.fullmatch(r'\| `([^`]+)` \| ([^|]+) \| `(0o[0-7]+)` / `([0-9]+)` \| ([0-9]+) \| `([a-f0-9]{64})` \| `([a-f0-9]{40})` \|',line)
 if m: rows[m[1]]=m.groups()[1:]
entries={}
for line in git('ls-files','--stage').decode().splitlines():
 meta,path=line.split('\t'); mode,blob,stage=meta.split(); entries[path]=(mode,blob,stage)
problems=[]
for path,(mode,blob,stage) in entries.items():
 f=p/path;b=f.read_bytes();s=f.lstat();r=rows.get(path)
 if not r: problems.append(('missing',path));continue
 role,unix,gm,size,digest,rb=r
 if (oct(stat.S_IMODE(s.st_mode)),mode,str(len(b)),sha(b),blob)!=(unix,gm,size,digest,rb): problems.append(('identity',path))
 if git('hash-object','--',path).decode().strip()!=blob or git('rev-parse','HEAD:'+path).decode().strip()!=blob: problems.append(('versions',path))
 if stage!='0' or not stat.S_ISREG(s.st_mode): problems.append(('type/stage',path))
print('inventory',json.dumps({'entries':len(entries),'rows':len(rows),'extra':sorted(set(rows)-set(entries)),'problems':problems,'candidates':sum(x.startswith('docs/tasks/') or x in ['docs/project-plan.md','docs/task-map.json'] for x in entries),'future':sum(x.startswith('docs/future-work/') for x in entries)}))
for name,args in [('index',('ls-files','--stage')),('refs',('show-ref',))]:
 raw=git(*args).rstrip(b'\n');print(name,sha(raw))
 if name=='refs':
  delta=b'6cb6a837746cdbf3e8f6d58e9bdcf529577d1f26 refs/personal-skills/run-evidence/run-20261014T121744Z-057fb9f63b88/finish'
  print('refs-minus-finish',sha(b'\n'.join(x for x in raw.splitlines() if x!=delta)))
print('raw-index',sha(pathlib.Path('.git/index').read_bytes()))
print('HEAD',git('rev-parse','HEAD').decode().strip())
print('status',repr(git('status','--porcelain=v1','--untracked-files=all').decode()))
for f in ['brief.md','verification.md','preflight.md','results.md']:
 print('package',f,sha((report.parent/f).read_bytes()))
ignored=git('ls-files','--others','--ignored','--exclude-standard').decode().splitlines()
print('ignored-count',len(ignored),'scoped',git('ls-files','--others','--ignored','--exclude-standard','--','docs/tasks','docs/future-work','ideas').decode().splitlines())
print('external-config',{x:(p/x).exists() for x in ['.gitmodules','.gitattributes']})
print('candidate-lfs',[x for x in entries if (x.startswith('docs/tasks/') or x in ['docs/project-plan.md','docs/task-map.json']) and (p/x).read_bytes().startswith(b'version https://git-lfs.github.com/spec/v1')])
PY
~~~

## Appendix B — Exact DISC-02 command

~~~sh
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
from pathlib import Path
import re,json,subprocess,hashlib,stat
r=Path('ideas/documentation-consolidation/tasks/T-001/results.md').read_text()
families=sorted(x.name for x in Path('docs/tasks').iterdir() if x.is_dir())
print('family-coverage',len(families),[x for x in families if '| `'+x+'` |' not in r])
for x in families:
 p=Path('docs/tasks')/x
 verdicts=[]
 for f in sorted((p/'reviews').glob('acceptance*.md')):
  text=f.read_text(); hits=[s for s in text.splitlines()[:20] if 'Verdict' in s or 'verdict' in s or 'ACCEPT' in s]
  verdicts.append((str(f),hits))
 print(x,'submission',[f.name for f in p.glob('*.md') if any(t in f.name for t in ['result','implementation','correction'])],'acceptance',verdicts)
text=Path('docs/tasks/T-005.1/fixtures.md').read_text()
blocks=[json.loads(s) for s in re.findall(r'```json\n(.*?)\n```',text,re.S)]
print('fixture-counts',[(list(x),len(x.get('case_inventory',[])),len(x.get('staged_input_sets',[])),len(x.get('handoff_manifests',[]))) for x in blocks])
m=next(x for x in blocks if 'staged_input_sets' in x)
for row in m['staged_input_sets']:
 print('staged-set',row['staging_id'],'fixture',row.get('fixture'),'local-inputs',row.get('consumer_visible_inputs') if not row.get('fixture') else 'generated workspace')
seen=set()
for x in blocks:
 def walk(o):
  if isinstance(o,dict):
   for v in o.values():walk(v)
  elif isinstance(o,list):
   for v in o:walk(v)
  elif isinstance(o,str):
   for p in re.findall(r'docs/(?:tasks/[^\s;()]+|task-map.json)',o):
    p=p.rstrip('.,'); f=Path(p)
    if f.is_file():seen.add(p)
 walk(x)
print('embedded-real-candidate-paths',sorted(seen))
print('embedded-missing-from-manifest',[p for p in seen if '`'+p+'`' not in r])
for line in r.splitlines():
 cells=line.split('|')
 if len(cells)==7 and cells[1].strip().startswith('`') and 'ignored; EXCLUDE' in line:
  f=Path(cells[1].strip().strip('`')); print('excluded-identity',str(f),len(f.read_bytes())==int(cells[3].strip()),hashlib.sha256(f.read_bytes()).hexdigest()==cells[4].strip().strip('`'))
print('helper-update-ref',[(i,l.strip()) for i,l in enumerate(Path('.agents/scripts/run_evidence.py').read_text().splitlines(),1) if 'update-ref' in l])
PY
~~~
