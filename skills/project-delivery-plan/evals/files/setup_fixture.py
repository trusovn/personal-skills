#!/usr/bin/env python3
"""Stage supplied authority and evidence for reading-experience evals."""

import os
from pathlib import Path
import sys


def stage(work: Path, scenario: str) -> Path:
    root = work / scenario
    root.mkdir(parents=True, exist_ok=False)
    docs = root / "docs"
    docs.mkdir()
    (root / "AGENTS.md").write_text(
        "Use supplied docs as authority. Write only planning outputs under docs/. "
        "No implementation, network, dependency installation, or commits.\n"
    )
    (docs / "foundation-review.md").write_text(
        "# Foundation readiness\n\n"
        "Synthetic supplied input: foundation ready; PERSONAL_FLOW. "
        "Existing Python standard-library CLI, JSON storage and unittest commands. "
        "No AI runtime, external services or new dependencies. "
        "No architecture gate beyond current local tests.\n"
    )
    if scenario == "small-change":
        authority = (
            "# Approved request\n\n"
            "Support staff need the existing local CSV export to include a header "
            "so they can identify columns without a separate field list. "
            "Only add the header name,status in that order; retain row order and values. "
            "Do not add UI, imports or change storage. First useful proof: export "
            "two stored records and compare the header and both rows. "
            "The owner approved this request, not implementation completion.\n"
        )
    elif scenario == "multi-task":
        authority = (
            "# Approved direction\n\n"
            "Volunteer coordinators lose track of unassigned requests in a local "
            "JSON file. Extend the existing CLI so they can record a request, "
            "list unassigned requests and assign one to a named volunteer. "
            "Priority: preserve requests, then prevent accidental reassignment. "
            "Requests have stable IDs and states unassigned or assigned. "
            "Reject reassignment without writing; persistence survives restart. "
            "No login, notifications, remote sync or automatic allocation. "
            "Separate durable request operations, CLI integration and a restart "
            "journey into composing tasks. First proof: record, restart, list, "
            "assign, restart and confirm the same assignment. "
            "The owner approved this direction; no implementation is approved as done.\n"
        )
    else:
        authority = (
            "# Unresolved request\n\n"
            "Make the tool better. No beneficiary, practical problem, intended "
            "behavior or priority was supplied. Foundation readiness does not "
            "supply product direction. The owner must clarify the purpose.\n"
        )
    (docs / "request.md").write_text(authority)
    (docs / "current-report.md").write_text(
        "# Interrupted work\n\n"
        "The maintainer inspected the current CLI. No implementation edits or "
        "behavior checks followed before interruption. The next implementer "
        "must implement and check the approved scope after planning and preparation. "
        "Independent discovery and acceptance have not run.\n"
    )
    (docs / "historical-acceptance.md").write_text(
        "# Historical acceptance\n\n"
        "ACCEPT for the original CLI before the current request. "
        "This decision covers the old version only.\n"
    )
    (docs / "handover-note.md").write_text(
        "# Unverified handover\n\n"
        "A note says the requested improvement is complete. It supplies no "
        "changed-file identity, command or output and conflicts with current-report.md. "
        "The maintainer must resolve this conflict before any current success claim.\n"
    )
    return root


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in {
        "small-change", "multi-task", "missing-direction"
    }:
        raise SystemExit("usage: setup_fixture.py small-change|multi-task|missing-direction")
    print(stage(Path(os.environ.get("EVAL_WORK_ROOT", "/work")), sys.argv[1]))
