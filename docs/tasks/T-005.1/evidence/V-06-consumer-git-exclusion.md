# V-06 / F-02 implementation evidence

Authority: `docs/tasks/T-005.1/brief.md`, AC-04; verification revision 1.
Context: `../reviews/discovery-02.md`, F-02 and V-06. Implementation evidence
only; prior reviewer status remains fail until fresh independent review.

The original DISC-03 retrieval reproduced `0 0 True`: deleting the raw fixture
file does not hide its committed JSON. The shared fixture remains read-only.
The manifest now invokes task-local `setup_consumer.py route-cases` and grants
only the new `route-consumer` root. Original `route-cases`, its Git repository,
the enclosing staging directory and setup code remain evaluator-only.

Setup reuses the original fixture, copies review files without `.git`, removes
the key before initializing Git, and commits a fresh consumer baseline. There
is no original object database, index, ref, reflog, configuration or alternate
object reference in the consumer. The original fixture has a single clean
baseline; all its other review file bytes are preserved. No role was called.

Commands ran sequentially at repository root, with disposable staging cleaned
by the existing `stage_setup` helper. No live/network/installer probe ran.

| Command | Setup and oracle | Result |
|---|---|---|
| `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_review_composition.T0051QualificationInputTests.test_route_consumer_excludes_answers_and_preserves_review_context` | Fresh manifest setup; delete original worktree key, retrieve through `git show HEAD:change-effects/cases.json` and `git show :change-effects/cases.json`. Raw evaluator retrieval must return identical key bytes; consumer retrieval must fail. All remaining review bytes match, consumer key absent and Git status clean. | 1 test OK |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_review_composition.T0051QualificationInputTests` | Eleven manifest sets resolve; each held-back record compared against consumer worktree files and every blob from `git cat-file --batch-all-objects`, including unreachable/index-only objects. Existing inventory/link/manifest good-wrong controls remain. | 6 tests OK |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_review_composition.py` | Owning module, implementation evidence only. | 22 tests OK |

The first regression was followed by the focused class, then the owning suite.
Two in-memory controls below confirm that the visibility check rejects unsafe
assembly rather than merely verifying manifest labels. They change disposable
state only; neither modifies the repository's manifest or test bytes.

Unsafe original root control:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 - <<'PY'
from unittest.mock import patch
import test_review_composition as c
manifest=c.t0051_manifests()
route=next(s for s in manifest['staged_input_sets'] if s['staging_id']=='route-cases')
route['consumer_visible_inputs']=['route-cases']
case=c.T0051QualificationInputTests('test_handoff_manifests_resolve_exact_consumer_visible_inputs')
try:
    with patch.object(c,'t0051_manifests',return_value=manifest):
        try:
            case.test_handoff_manifests_resolve_exact_consumer_visible_inputs()
        except AssertionError as exc:
            assert 'cases.json' in str(exc), str(exc)
            print('Unsafe original consumer rejected at evaluator-byte visibility assertion')
        else:
            raise AssertionError('unsafe control accepted')
finally:
    case.doCleanups()
PY
```

Result: exit 0; `Unsafe original consumer rejected at evaluator-byte visibility assertion`.

Unreachable Git object control (no answer file, ref or index entry is added):

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 - <<'PY'
from unittest.mock import patch
import subprocess
import test_review_composition as c
original_stage=c.stage_setup
case=c.T0051QualificationInputTests('test_handoff_manifests_resolve_exact_consumer_visible_inputs')
def injected(*args):
    work=original_stage(*args)
    if args[2]=='route-cases':
        answer=(work/'route-cases/change-effects/cases.json').read_bytes()
        subprocess.run(['git','hash-object','-w','--stdin'],input=answer,cwd=work/'route-consumer',check=True,capture_output=True,timeout=10)
    return work
try:
    with patch.object(c,'stage_setup',side_effect=injected):
        try:
            case.test_handoff_manifests_resolve_exact_consumer_visible_inputs()
        except AssertionError as exc:
            assert 'route-cases' in str(exc), str(exc)
            print('Unreachable answer-key blob rejected by all-object assertion')
        else:
            raise AssertionError('unreachable oracle accepted')
finally:
    case.doCleanups()
PY
```

Result: exit 0; `Unreachable answer-key blob rejected by all-object assertion`.

Limits: these checks detect the declared held-back records as complete byte
sequences, and directly reject the reported history/index leak. They do not
claim detection of every possible transformed answer or role compliance.
Consumer access must be restricted to the manifest roots; giving a role the
evaluator staging directory would defeat the supplied boundary. Future actual
preparation records must identify the new consumer Git baseline. V-01–V-05
prior independent passes remain navigation; unchanged installation/runtime
receipts were not renewed in this correction.

Next: separate maintainability review, fresh independent discovery, then a
separate acceptance decision. No independent verdict is issued here.
