#!/usr/bin/env python3
"""Stage disposable review targets for task-maintainability-review evals.

Each scenario creates a Git workspace holding a legitimate task, a committed
baseline, and changed production bytes under review. The four-blockers
scenario introduces four distinct, independently observable maintainability
blockers plus one non-blocking style preference. The correction-round
scenario stages a prior durable report with those four finding IDs and a
correction that applies only MNT-B2's smallest correction direction, so the
next review must preserve finding identity. Oracle records next to the
workspace describe the independent defect observations and the complete,
genuine-stop, and correction-round reporting expectations; they are
qualification inputs, not durable review reports.
"""

from pathlib import Path
import os
import shutil
import subprocess
import sys
import textwrap


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


SCENARIOS = {
    "correction-round": correction_round,
    "four-blockers": four_blockers,
    "genuine-stop": genuine_stop,
}

if len(sys.argv) != 2 or sys.argv[1] not in SCENARIOS:
    raise SystemExit(f"usage: {sys.argv[0]} <{'|'.join(SCENARIOS)}>")
SCENARIOS[sys.argv[1]]()