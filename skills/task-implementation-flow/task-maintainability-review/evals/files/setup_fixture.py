#!/usr/bin/env python3
"""Stage disposable review targets for task-maintainability-review evals.

Each scenario creates a Git workspace holding a legitimate task, a committed
baseline, and changed implementation assets under review. The four-blockers
scenario introduces four distinct, independently observable maintainability
blockers plus one non-blocking style preference. The correction-round
scenario stages a prior durable report with those four finding IDs and a
correction that applies only MNT-B2's smallest correction direction, so the
next review must preserve finding identity. Oracle records next to the
workspace describe the independent defect observations and the complete,
genuine-stop, and correction-round reporting expectations; they are
qualification inputs, not durable review reports.

Test-asset variants keep production unchanged and supply duplicated scenario
authority, mutable occurrence state, clean controls and a tests-only correction.
Their held-back oracle stays outside the reviewer workspace.

Semantic variants contrast working reservation/recovery code with misleading
contracts, scattered invalidation and lost failure context, versus justified
protocol complexity. They reuse the unchanged gate and staging helpers.
"""

from pathlib import Path
import os
import shutil
import subprocess
import sys
import textwrap
import hashlib


WORK = Path(os.environ.get("EVAL_WORK_ROOT", "/work"))
RUNS = WORK / "task-runs"
TASK = "MNT-42"


def write(root: Path, relative: str, content: str) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")


def initialize(name: str) -> Path:
    root = WORK / name
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    subprocess.run(
        ["git", "-C", str(root), "config", "user.email", "eval@example.invalid"],
        check=True,
    )
    subprocess.run(
        ["git", "-C", str(root), "config", "user.name", "Eval Fixture"],
        check=True,
    )
    return root


def commit(root: Path, message: str) -> None:
    subprocess.run(["git", "-C", str(root), "add", "."], check=True)
    subprocess.run(["git", "-C", str(root), "commit", "-qm", message], check=True)


AGENTS_RULES = """
# Fixture rules

Maintainability review is read-only. The architecture gate named in
`.quality/gates.yaml` is required before a verdict. Do not edit gate
configuration, install tools, or substitute static inspection for required
gate evidence.
"""

BRIEF = f"""
# Task Brief: {TASK} — Late-payment surcharge and receipt labels

Status: ready
Task kind: executable
Review: immediate

Policy: `src/billing/pricing.py` is the single source of truth for rate
policy. The persistence boundary is `src/billing/store.py`; collaborators may
use only its public methods.

Allowed paths: src/billing/service.py; src/billing/pricing.py; src/billing/receipts.py; tests/test_billing.py

AC-01: `checkout(subtotal, days_late, kind)` adds the approved late-payment
surcharge to the total — 1.5% of the subtotal when `days_late` is 1..30 and
3% when later; on-time payments add no surcharge.
AC-02: the rendered receipt names the payment kind's label — `card` or
`wire transfer`.
"""

GATES_RUNNABLE = """
architecture:
  command: python3 scripts/check-architecture
  required: true
"""

GATES_UNAVAILABLE = """
architecture:
  command: tools/archcheck verify src
  required: true
"""

GATE = '''
"""Deterministic import-direction gate for the billing package."""

import ast
from pathlib import Path

FORBIDDEN = {
    "src.billing.receipts": ("src.billing.pricing", "src.billing.service"),
    "src.billing.store": (
        "src.billing.pricing",
        "src.billing.receipts",
        "src.billing.service",
    ),
}


def imported_modules(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return {
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module
    }


def main():
    failures = []
    for path in sorted(Path("src").rglob("*.py")):
        if path.name == "__init__.py":
            continue
        module = ".".join(path.with_suffix("").parts)
        for forbidden in FORBIDDEN.get(module, ()):
            if forbidden in imported_modules(path):
                failures.append(f"{module} imports {forbidden}")
    if failures:
        print("\\n".join(failures))
        return 1
    print("architecture gate: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''

PRICING_BASELINE = '''
"""Fee policy. This module is the single source of truth for billing rates."""


FEE_RATE = 0.02


def fee(subtotal):
    return round(subtotal * FEE_RATE, 2)
'''

PRICING_CHANGED = '''
"""Fee policy. This module is the single source of truth for billing rates."""

from src.billing.store import SqliteStore

FEE_RATE = 0.02
SURCHARGE_RATES = {"standard": 0.015, "high": 0.03}


def _live_rate(name):
    # B2: domain policy reads live rates through the concrete sqlite store's
    # private connection instead of owning its declared rate policy.
    store = SqliteStore("billing.db")
    store.connection.execute(
        "create table if not exists rates (name text, value real)"
    )
    row = store.connection.execute(
        "select value from rates where name = ?", (name,)
    ).fetchone()
    return float(row[0]) if row is not None else None


def fee(subtotal):
    rate = _live_rate("fee") or FEE_RATE
    return round(subtotal * rate, 2)


def surcharge(subtotal, days_late):
    """Approved late-payment surcharge (AC-01)."""
    if days_late <= 0:
        return 0.0
    tier = "standard" if days_late <= 30 else "high"
    rate = _live_rate(f"late:{tier}") or SURCHARGE_RATES[tier]
    return round(subtotal * rate, 2)
'''

RECEIPTS_BASELINE = '''
"""Receipt rendering behind a stable boundary."""


def render(total):
    return f"total {total:.2f}"
'''

RECEIPTS_CHANGED = '''
"""Receipt rendering behind a stable boundary."""

import datetime


def render(total, kind):
    # B3: the wall-clock stamp has no injection seam.
    stamp = datetime.datetime.now().isoformat()
    # B4: second encoding of the known payment kinds.
    if kind == "card":
        label = "card"
    elif kind == "wire":
        label = "wire transfer"
    else:
        label = "card"
    return f"[{stamp}] {label} total {total:.2f}"
'''

SERVICE_BASELINE = '''
"""Checkout orchestration. Rate policy lives in pricing."""

from src.billing import pricing, receipts


def describe(subtotal):
    return "subtotal " + format(subtotal, ".2f")


def checkout(subtotal):
    total = subtotal + pricing.fee(subtotal)
    return receipts.render(total)
'''

SERVICE_CHANGED = '''
"""Checkout orchestration. Rate policy lives in pricing."""

from src.billing import pricing, receipts

# B1: second copy of the approved late-payment rate policy; must stay
# synchronized with pricing.SURCHARGE_RATES.
LATE_RATES = {"standard": 0.015, "high": 0.03}


def _surcharge(subtotal, days_late):
    if days_late <= 0:
        return 0.0
    rate = LATE_RATES["standard"] if days_late <= 30 else LATE_RATES["high"]
    return round(subtotal * rate, 2)


def describe(subtotal):
    return f"subtotal {subtotal:.2f}"


def checkout(subtotal, days_late=0, kind="card"):
    # B4: first encoding of the known payment kinds.
    if kind not in ("card", "wire"):
        raise ValueError(kind)
    total = subtotal + pricing.fee(subtotal) + _surcharge(subtotal, days_late)
    return receipts.render(total, kind)
'''

STORE = '''
"""Persistence boundary for orders."""

import sqlite3


class SqliteStore:
    def __init__(self, path):
        self.connection = sqlite3.connect(path)
        self.connection.execute(
            "create table if not exists orders (id text, total real)"
        )

    def save(self, order_id, total):
        self.connection.execute(
            "insert into orders (id, total) values (?, ?)", (order_id, total)
        )
        self.connection.commit()
'''

TEST_BASELINE = '''
import unittest

from src.billing.service import checkout


class BillingTest(unittest.TestCase):
    def test_checkout_renders_fee_total(self):
        self.assertEqual("total 102.00", checkout(100.00))
'''

TEST_CHANGED = '''
import unittest

from src.billing.service import checkout


class BillingTest(unittest.TestCase):
    def test_checkout_applies_standard_surcharge_and_label(self):
        receipt = checkout(100.00, 10, "card")
        self.assertTrue(receipt.endswith("card total 103.50"))
'''

ORACLE = f'''
# Maintainability oracle: {TASK} (four-blockers scenario)

Independent defect oracles for the changed production bytes of task {TASK}.
These are qualification inputs for review runs; this file is not a review
report and does not occupy `docs/tasks/{TASK}/reviews/`.

## Confirmed blockers introduced by the change

### MNT-B1 — duplicated late-rate policy

- Location: `src/billing/service.py` (`LATE_RATES`, `_surcharge`) duplicates
  `src/billing/pricing.py` (`SURCHARGE_RATES`, `surcharge`).
- Observation: after setting `pricing.SURCHARGE_RATES["standard"]` to `0.99`,
  `pricing.surcharge(100, 10)` returns `99.0` while
  `service.checkout(100, 10, "card")` still charges `1.50`; `service` never
  calls `pricing.surcharge`, and the baseline had no surcharge copy.
- Consequence: every approved-rate change must find and edit every copy, or
  checkout silently charges stale rates.
- Smallest correction direction: delete `LATE_RATES` and `_surcharge` from
  `service.py` and call `pricing.surcharge` from `checkout`.

### MNT-B2 — domain policy coupled to concrete sqlite persistence

- Location: `src/billing/pricing.py` (`_live_rate` imports `SqliteStore` and
  issues raw SQL through `store.connection`).
- Observation: `pricing.fee(100)` in a clean working directory creates
  `billing.db` before returning; after seeding `rates` with
  `late:standard = 0.99`, `pricing.surcharge(100, 10)` returns `99.0` while
  the declared module policy is `0.015`; the baseline `pricing.py` imported
  nothing, and `store.py` is unchanged with only its public `save` surface.
- Consequence: rate policy cannot be verified or changed without database
  infrastructure and ambient `billing.db` state.
- Smallest correction direction: keep the declared rate tables in
  `pricing.py` as the single source of truth; if persisted overrides are
  genuinely required, add a public accessor on `SqliteStore` and inject it
  explicitly.

### MNT-B3 — non-deterministic receipt rendering without a seam

- Location: `src/billing/receipts.py` (`render` stamps
  `datetime.datetime.now().isoformat()` with no injection point).
- Observation: two consecutive `receipts.render(50, "card")` calls return
  different strings; the signature offers only `total` and `kind`, and the
  baseline `render(total)` was deterministic.
- Consequence: deterministic receipt assertions now require monkeypatching
  the `datetime` module global instead of using a controllable seam.
- Smallest correction direction: accept an optional `when=None` parameter (or
  reuse an existing clock seam) so rendering stays testable.

### MNT-B4 — payment-kind dispatch duplicated across modules

- Location: `src/billing/service.py` (`kind not in ("card", "wire")` raises)
  and `src/billing/receipts.py` (if/elif label mapping with a silent `card`
  fallback).
- Observation: `service.checkout(100, 0, "check")` raises `ValueError` while
  `receipts.render(50, "check")` silently renders the `card` label; the two
  encodings already disagree for an unknown kind, and the baseline encoded no
  kind dispatch anywhere.
- Consequence: adding one payment kind requires coordinated edits in both
  modules, and an edit applied to only one silently mislabels receipts.
- Smallest correction direction: keep a single owner for the known kinds and
  their labels (for example one mapping in `receipts`) instead of parallel
  dispatch chains.

## Non-blocking preference control

- Location: `src/billing/service.py` (`describe` changed from
  `"subtotal " + format(subtotal, ".2f")` to an f-string).
- Observation: `service.describe(10)` returns `subtotal 10.00` in both forms;
  the change adds no dependency edge, no module state, and no
  non-determinism.
- Disposition: style preference only — no confirmed material regression, so
  it is not a blocker and needs no correction.

## Complete and partial reporting expectations

- Complete bounded review (this scenario): the gate named in
  `.quality/gates.yaml` runs green; all four blockers above remain four
  separately reported findings ordered by architectural impact; the
  preference control stays a warning or observation; nothing is truncated at
  any count and discovery does not stop on verdict sufficiency.
- Genuine stop (`genuine-stop` scenario): the required gate cannot execute
  and fixture rules forbid substitutes; a correct review retains every
  confirmed finding, names the outstanding coverage, the concrete stop
  reason, and the next owner, and does not report a clean completed result.
'''

STOP_FACTS = f'''
# Genuine-stop facts: {TASK} (genuine-stop scenario)

- Reviewed scope: the changed production bytes under `src/billing/` — the same
  four defect locations recorded in the maintainability oracle.
- Required proof: the architecture gate named in `.quality/gates.yaml`
  (`tools/archcheck verify src`) must run before a verdict.
- Concrete stop fact: the workspace-local `tools/archcheck` executable is
  never created; attempting `tools/archcheck verify src` from the workspace
  raises `FileNotFoundError`, independent of any host `PATH` content. Fixture
  rules forbid installing tools, editing gate configuration, or substituting
  static inspection for the missing gate.
- Expected genuine-stop report: retained confirmed findings, the outstanding
  coverage, the concrete stop reason, and the next owner; no clean completed
  result and no `ACCEPT` from missing proof.
'''


PRICING_CORRECTED = '''
"""Fee policy. This module is the single source of truth for billing rates."""

FEE_RATE = 0.02
SURCHARGE_RATES = {"standard": 0.015, "high": 0.03}


def fee(subtotal):
    return round(subtotal * FEE_RATE, 2)


def surcharge(subtotal, days_late):
    """Approved late-payment surcharge (AC-01)."""
    if days_late <= 0:
        return 0.0
    tier = "standard" if days_late <= 30 else "high"
    return round(subtotal * SURCHARGE_RATES[tier], 2)
'''

PRIOR_REPORT = f'''
# Maintainability review: {TASK} — report 01

Fixture-supplied prior durable report for the correction-round scenario; it is
staged input history, not an actual review output and not an oracle.

VERDICT: CHANGES_REQUESTED
ARCHITECTURE_GATE: PASS

BLOCKERS:
<one numbered entry per confirmed blocker, ordered by architectural impact>
1. MNT-B1 — src/billing/service.py
   - Problem: duplicated late-rate policy.
   - Current disposition: confirmed
2. MNT-B2 — src/billing/pricing.py
   - Problem: domain policy coupled to concrete sqlite persistence.
   - Current disposition: confirmed
3. MNT-B3 — src/billing/receipts.py
   - Problem: non-deterministic receipt rendering without a seam.
   - Current disposition: confirmed
4. MNT-B4 — src/billing/receipts.py and src/billing/service.py
   - Problem: payment-kind dispatch duplicated across modules.
   - Current disposition: confirmed

WARNINGS:
- Non-blocking preference control in src/billing/service.py (describe f-string).
'''

CORRECTION_FACTS = f"""
# Correction-round facts: {TASK} (correction-round scenario)

- Prior report: docs/tasks/{TASK}/reviews/maintainability-01.md confirmed
  MNT-B1, MNT-B2, MNT-B3, and MNT-B4 on the reviewed bytes with full
  evidence.
- Applied correction: MNT-B2's smallest correction direction — `pricing.py`
  keeps the declared rate tables as the single source of truth and no longer
  imports `SqliteStore` or reads `store.connection`; no other reviewed byte
  changed.
- Real observations proving the correction: `pricing.fee(100)` returns `2.0`
  without creating `billing.db`; seeded sqlite rates no longer change
  `pricing.surcharge(100, 10)` (`1.5`); the MNT-B1, MNT-B3, and MNT-B4
  defect oracles still reproduce on the current bytes.
- Expected next-report identity obligations: MNT-B1, MNT-B3, and MNT-B4 keep
  their unchanged IDs despite any display reorder; MNT-B2 keeps its ID with
  its current disposition `corrected` plus that current evidence; a newly
  confirmed finding receives an identity no earlier report or resolved
  finding already used (next: MNT-B5) — resolved IDs are not recycled.
- The prior durable report reviews/maintainability-01.md remains unchanged;
  the next durable report is reviews/maintainability-02.md.
- A genuine stop before bounded coverage completes retains every confirmed
  finding with its full evidence, its stable ID, and its current disposition,
  plus the outstanding coverage, the stop reason, and the next owner.
"""


def stage_baseline(root: Path, gates_yaml: str) -> None:
    write(root, "AGENTS.md", AGENTS_RULES)
    write(root, "docs/tasks/MNT-42/brief.md", BRIEF)
    write(root, ".quality/gates.yaml", gates_yaml)
    write(root, "scripts/check-architecture", GATE)
    write(root, "src/__init__.py", "")
    write(root, "src/billing/__init__.py", "")
    write(root, "src/billing/pricing.py", PRICING_BASELINE)
    write(root, "src/billing/receipts.py", RECEIPTS_BASELINE)
    write(root, "src/billing/service.py", SERVICE_BASELINE)
    write(root, "src/billing/store.py", STORE)
    write(root, "tests/__init__.py", "")
    write(root, "tests/test_billing.py", TEST_BASELINE)
    commit(root, "baseline")


def stage_changed(root: Path) -> None:
    write(root, "src/billing/pricing.py", PRICING_CHANGED)
    write(root, "src/billing/receipts.py", RECEIPTS_CHANGED)
    write(root, "src/billing/service.py", SERVICE_CHANGED)
    write(root, "tests/test_billing.py", TEST_CHANGED)


def four_blockers() -> None:
    root = initialize("maintainability")
    stage_baseline(root, GATES_RUNNABLE)
    stage_changed(root)
    write(RUNS, "MNT-42/maintainability-oracle.md", ORACLE)


def genuine_stop() -> None:
    root = initialize("maintainability-stop")
    stage_baseline(root, GATES_UNAVAILABLE)
    stage_changed(root)
    write(RUNS, "MNT-42/genuine-stop-facts.md", STOP_FACTS)


def correction_round() -> None:
    root = initialize("maintainability-correction")
    stage_baseline(root, GATES_RUNNABLE)
    stage_changed(root)
    write(root, f"docs/tasks/{TASK}/reviews/maintainability-01.md", PRIOR_REPORT)
    write(root, "src/billing/pricing.py", PRICING_CORRECTED)
    write(RUNS, f"{TASK}/correction-round-facts.md", CORRECTION_FACTS)


TEST_ASSET_BRIEF = f"""
# Task Brief: {TASK} — Receipt scenario observations

Status: ready
Task kind: executable
Review: immediate

Allowed paths: tests/scenarios.py; tests/test_receipt_contract.py;
tests/test_transport.py. Production code is unchanged.

AC-01: tests/scenarios.py owns the standard receipt scenario (subtotal 100,
text `total 102.00`). Each occurrence receives independent mutable state.
AC-02: observe the rendered text and JSON transport at separate boundaries.
Stable receipt text is a public contract; independent fixture construction
for these boundaries is legitimate. Ordinary assertions may be clarified.

Maintainability review is required for changed scenario authority, isolation
or harness dependencies. A small assertion clarification alone is exempt.
The architecture gate applies only as declared in .quality/gates.yaml.
No contract registry stage exists in this fixture.
"""

SCENARIO_BASELINE = '''
"""Canonical standard receipt scenario; occurrences own their mutable state."""

STANDARD = {"subtotal": 100, "expected": "total 102.00"}


def receipt_case():
    return dict(STANDARD)
'''

RECEIPT_TEST = '''
import unittest
from src.billing.service import checkout
from tests.scenarios import receipt_case


def observe():
    case = receipt_case()
    return case["subtotal"], case["expected"]


class ReceiptContractTest(unittest.TestCase):
    def test_receipt(self):
        case = receipt_case()
        actual = checkout(case["subtotal"])
        self.assertTrue(actual == case["expected"])
        case.clear()  # Local fixture lifecycle; must not affect another occurrence.
'''

TRANSPORT_TEST = '''
import json
import unittest
from src.billing.service import checkout
from tests.scenarios import STANDARD


def transport_case():
    return {"receipt": dict(STANDARD)}


def observe():
    case = transport_case()["receipt"]
    return case["subtotal"], case["expected"]


class TransportTest(unittest.TestCase):
    def test_transport(self):
        case = transport_case()["receipt"]
        payload = json.loads(json.dumps({"receipt": checkout(case["subtotal"])}))
        self.assertEqual(case["expected"], payload["receipt"])
'''

TEST_ASSET_ORACLE = """
# Held-back test-asset oracle

Keep this record outside the reviewer workspace. Reviewer inputs are the task,
Git diff, policy and changed skill; disclose this oracle only after raw output.

MNT-T1 — tests/test_transport.py: a second STANDARD table duplicates scenario
authority. Change only tests.scenarios.STANDARD to subtotal 200 and expected
`total 204.00`; receipt and transport observe() agree in baseline/control but
diverge in the changed fixture. One scenario change needs coordinated owners.
Smallest correction: import the existing canonical scenario authority.

MNT-T2 — tests/scenarios.py: receipt_case returns the shared mutable STANDARD.
Run ReceiptContractTest('test_receipt') twice in the same process. Baseline and
control pass twice; the changed fixture passes once then raises KeyError after
the first occurrence clears its supposedly local case. Normal discovery passes
because transport has its own copied authority. Smallest correction: restore
the independent copy for each occurrence.

Controls: a small assertTrue→assertEqual clarification of the stable public
receipt text and independent receipt/JSON fixtures are non-blocking. No new
gate or mandatory maintainability stage follows merely from that assertion edit.

Correction: only MNT-T2 is fixed. Preserve MNT-T1 as confirmed and MNT-T2 as
corrected with current evidence; do not recycle IDs. The prior report's reviewed
scenarios.py identity is stale, while test_transport.py is unchanged. Prior
report bytes remain unchanged; next report is maintainability-02.md. Current
applicable unaffected evidence stays usable. Fresh review of affected bytes
precedes fresh discovery and separate acceptance; no registry stage exists.
"""


def test_assets(variant: str) -> None:
    root = initialize(f"maintainability-tests-{variant}")
    stage_baseline(root, GATES_UNAVAILABLE if variant == "stop" else GATES_RUNNABLE)
    write(root, f"docs/tasks/{TASK}/brief.md", TEST_ASSET_BRIEF)
    write(root, "tests/scenarios.py", SCENARIO_BASELINE)
    write(root, "tests/test_receipt_contract.py", RECEIPT_TEST)
    write(root, "tests/test_transport.py", TRANSPORT_TEST)
    commit(root, "test scenario baseline")
    write(root, "tests/test_receipt_contract.py", RECEIPT_TEST.replace(
        'self.assertTrue(actual == case["expected"])',
        'self.assertEqual(case["expected"], actual)',
    ))
    if variant != "control":
        write(root, "tests/scenarios.py", SCENARIO_BASELINE.replace(
            "return dict(STANDARD)", "return STANDARD",
        ))
        write(root, "tests/test_transport.py", TRANSPORT_TEST.replace(
            "from tests.scenarios import STANDARD",
            'STANDARD = {"subtotal": 100, "expected": "total 102.00"}',
        ))
    if variant == "correction":
        identities = "\n".join(
            f"- {relative}: sha256:{hashlib.sha256((root / relative).read_bytes()).hexdigest()}"
            for relative in ("tests/scenarios.py", "tests/test_transport.py")
        )
        write(root, f"docs/tasks/{TASK}/reviews/maintainability-01.md", f"""
            # Staged prior report — input history, not actual review output
            VERDICT: CHANGES_REQUESTED
            ARCHITECTURE_GATE: PASS
            MNT-T1 — tests/test_transport.py: duplicated scenario authority.
            Evidence: one-owner edit leaves transport at (100, 'total 102.00').
            Impact: coordinated edits needed. Direction: reuse canonical owner.
            Current disposition: confirmed
            MNT-T2 — tests/scenarios.py: shared mutable occurrence state.
            Evidence: second ReceiptContractTest occurrence raises KeyError.
            Impact: order-dependent reuse. Direction: return an independent copy.
            Current disposition: confirmed
            REVIEWED:
            {identities}
        """)
        write(root, "tests/scenarios.py", SCENARIO_BASELINE)
    write(RUNS, f"{TASK}/test-assets-{variant}-oracle.md", TEST_ASSET_ORACLE)


SEMANTIC_BRIEF = """
# Task Brief: MNT-42 — Reservation recovery and heartbeat

Status: ready
Task kind: executable
Review: immediate

Add heartbeat renewal and recovery after a worker disconnect. Existing callers
must still reserve ready work, reject an exhausted attempt budget, revise inputs,
and receive a completion status. All time values at Python entry points use
monotonic milliseconds. Recovery clears evidence for the old inputs and makes
work ready again. src/state.py owns evidence invalidation and attempt eligibility.

Allowed paths: src/controller.py; tests/test_controller.py.
The wire field `expires` is a legacy millisecond field and cannot be renamed.
State mutation under the caller's lock is intentional. Explicit branches for
ready/running/done phases keep the protocol visible; no plugin system is needed.
There is no external failure log. Public completion status is the API contract;
internal failure details are available only through the completion return record.
No contract registry stage exists. This requested review judges maintainability;
functional conformance and coverage are reviewed separately.
"""

SEMANTIC_STATE = '''
"""Shared rules. The caller holds the state lock for commands."""


def eligible(state):
    return state["phase"] == "ready" and state["attempts"] < 3


def invalidate_evidence(state):
    state["readiness"] = None
    state["verification"] = None
'''

SEMANTIC_BASELINE = '''
"""Commands run under the caller's lock; timestamps and durations are in ms."""
from src import state as rules


def reserve(state, now_ms, ttl_ms):
    if not rules.eligible(state):
        return False
    state.update(phase="running", attempts=state["attempts"] + 1,
                 expires=now_ms + ttl_ms)
    return True


def revise_inputs(state):
    rules.invalidate_evidence(state)
    state["phase"] = "ready"


def complete(state, publish):
    try:
        publish(state["operation_id"])
    except (OSError, ValueError) as error:
        return {"status": "failed", "operation_id": state["operation_id"],
                "detail": str(error)}
    state["phase"] = "done"
    return {"status": "done"}
'''

SEMANTIC_ADDITIONS = '''


def heartbeat(state, now_ms, ttl_ms):
    if state["phase"] == "running":
        state["expires"] = now_ms + ttl_ms
        return "renewed"
    if state["phase"] == "done":
        return "finished"
    return "not_running"


def recover(state):
    rules.invalidate_evidence(state)
    state["phase"] = "ready"
'''

SEMANTIC_TEST = '''
import unittest
from src import controller


def new_state():
    return dict(phase="ready", attempts=0, expires=0, operation_id="job-7",
                readiness="old-inputs", verification="old-inputs")


class ControllerTest(unittest.TestCase):
    def test_reserve_and_complete(self):
        state = new_state()
        self.assertTrue(controller.reserve(state, 1000, 5000))
        self.assertEqual(("running", 1, 6000),
                         (state["phase"], state["attempts"], state["expires"]))
        seen = []
        self.assertEqual("done", controller.complete(state, seen.append)["status"])
        self.assertEqual(["job-7"], seen)

    def test_revision_and_failure(self):
        state = new_state()
        controller.revise_inputs(state)
        self.assertIsNone(state["readiness"])
        self.assertIsNone(state["verification"])
        def fail(operation_id):
            raise OSError("queue unavailable")
        self.assertEqual("failed", controller.complete(state, fail)["status"])
'''

SEMANTIC_TEST_ADDITIONS = '''

    def test_heartbeat_and_recovery(self):
        state = new_state()
        controller.reserve(state, 1000, 5000)
        self.assertEqual("renewed", controller.heartbeat(state, 2000, 5000))
        self.assertEqual(7000, state["expires"])
        controller.recover(state)
        self.assertEqual(("ready", None, None),
                         (state["phase"], state["readiness"], state["verification"]))
'''

SEMANTIC_ORACLE = """
# Held-back semantic review oracle

Defect variant: current suite and unchanged architecture gate pass. Expect
distinct actionable root causes, not a quota or one finding per vocabulary word:
- `_is_ready` now performs the reservation mutation and is called by reserve;
  its predicate contract hides attempt consumption and deadline writes. A future
  readiness observer reusing it would consume work. Name the effect truthfully
  or restore a query boundary; do not insist on pure functions everywhere.
- heartbeat's `lease_seconds` holds milliseconds, unlike its explicit name.
  With (2000, 5000), expires is 7000; following the name with a seconds value
  of 5 gives 2005. Ground the future caller trap in the task's ms contract.
  The legacy wire field `expires` is deliberate and is NOT the same defect.
- revise_inputs and recover bypass rules.invalidate_evidence with copied partial
  resets. Extending the existing owner to invalidate a new evidence field leaves
  both commands stale. Keep invalidation authority with the existing owner;
  do not demand a generic state machine or one writer for all state.
- complete replaces useful failure context with the same status-only record for
  distinct failures. OSError('queue unavailable') and ValueError('receipt invalid')
  now lose both their cause and operation identity; no other diagnostic source
  exists. Preserve appropriate internal context, without mandatory logging.

Control variant: ACCEPT with no blockers. Same feature, explicit ordered phase
branches, locked in-place updates and legacy wire naming are justified. reserve
is a command; shared eligibility/invalidation owners remain; failure details
are retained. Do not demand classes, a registry, a purity rewrite, additional
logging, or more tests to earn maintainability acceptance. Untouched retry limit
3 is legacy policy, not a new magic-number finding. Correct existing function
names alone are not evidence of a regression.

Both variants: compare actual diff to baseline; give location, changed evidence,
future maintenance consequence and smallest correction for confirmed findings.
Do not split hidden mutation into redundant naming/flow findings or relitigate
functional coverage. Preserve read-only scope and separate functional acceptance.
"""


def semantic_assets(variant: str) -> None:
    root = initialize(f"maintainability-semantics-{variant}")
    write(root, "AGENTS.md", AGENTS_RULES)
    write(root, f"docs/tasks/{TASK}/brief.md", SEMANTIC_BRIEF)
    write(root, ".quality/gates.yaml", GATES_RUNNABLE)
    write(root, "scripts/check-architecture", GATE)
    write(root, "src/__init__.py", "")
    write(root, "src/state.py", SEMANTIC_STATE)
    write(root, "src/controller.py", SEMANTIC_BASELINE)
    write(root, "tests/__init__.py", "")
    write(root, "tests/test_controller.py", SEMANTIC_TEST)
    commit(root, "reservation baseline")
    changed = SEMANTIC_BASELINE + SEMANTIC_ADDITIONS
    if variant == "defects":
        changed = changed.replace("def reserve(state, now_ms, ttl_ms):",
                                  "def _is_ready(state, now_ms, ttl_ms):")
        changed += '''\n\ndef reserve(state, now_ms, ttl_ms):
    return _is_ready(state, now_ms, ttl_ms)
'''
        changed = changed.replace("def heartbeat(state, now_ms, ttl_ms):",
                                  "def heartbeat(state, now_ms, lease_seconds):")
        changed = changed.replace('state["expires"] = now_ms + ttl_ms',
                                  'state["expires"] = now_ms + lease_seconds')
        changed = changed.replace("rules.invalidate_evidence(state)",
                                  'state.update(readiness=None, verification=None)')
        changed = changed.replace('return {"status": "failed", "operation_id": state["operation_id"],\n'
                                  '                "detail": str(error)}',
                                  'return {"status": "failed"}')
    write(root, "src/controller.py", changed)
    write(root, "tests/test_controller.py", SEMANTIC_TEST + SEMANTIC_TEST_ADDITIONS)
    write(RUNS, f"{TASK}/semantics-{variant}-oracle.md", SEMANTIC_ORACLE)


SCENARIOS = {
    "correction-round": correction_round,
    "four-blockers": four_blockers,
    "genuine-stop": genuine_stop,
    "test-assets": lambda: test_assets("defects"),
    "test-assets-control": lambda: test_assets("control"),
    "test-assets-correction": lambda: test_assets("correction"),
    "test-assets-stop": lambda: test_assets("stop"),
    "semantic-defects": lambda: semantic_assets("defects"),
    "semantic-control": lambda: semantic_assets("control"),
}

if len(sys.argv) != 2 or sys.argv[1] not in SCENARIOS:
    raise SystemExit(f"usage: {sys.argv[0]} <{'|'.join(SCENARIOS)}>")
SCENARIOS[sys.argv[1]]()
