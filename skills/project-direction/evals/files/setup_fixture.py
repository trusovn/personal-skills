#!/usr/bin/env python3
"""Create deterministic repositories used by project-direction evals."""

from pathlib import Path
import os
import shutil
import subprocess
import sys
import textwrap

WORK = Path(os.environ.get("EVAL_WORK_ROOT", "/work"))


def write(root: Path, relative: str, content: str) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")


def initialize(root: Path) -> None:
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


def commit(root: Path) -> None:
    subprocess.run(["git", "-C", str(root), "add", "."], check=True)
    subprocess.run(
        ["git", "-C", str(root), "commit", "-qm", "fixture baseline"],
        check=True,
    )


def initial_direction() -> None:
    root = WORK / "reading-helper"
    initialize(root)
    write(
        root,
        "AGENTS.md",
        """
        # Fixture rules

        Write planning artifacts only under `docs/`. Do not add implementation
        files or choose a software architecture.
        """,
    )
    write(
        root,
        "notes/reading-helper.md",
        """
        # Reading helper notes

        I want a private personal tool that turns articles and my highlights
        into a short weekly reading review. It is for me, on my own computer.
        The first useful result is one real review assembled from five saved
        articles, with links back to every source.

        My priority order is: never invent or lose source attribution; give me
        a useful draft quickly; then make the writing polished. If those
        compete, attribution wins and the tool should leave an explicit gap
        rather than guess.

        Normal: I add articles during the week and ask for a review on Friday.
        Recovery: if processing stops, it should preserve completed source work
        and tell me what remains. Stop: if a claim cannot be tied to a source
        or two sources conflict, ask me rather than smoothing it over.

        It may organize, summarize, and draft. It may not publish, contact
        anyone, buy subscriptions, or silently discard sources. I trust my
        local files and myself. Article text and automated summaries can be
        incomplete or wrong. I decide what is published and any change to
        privacy or source-handling rules.
        """,
    )
    commit(root)


def technical_audit() -> None:
    root = WORK / "orchestrator-audit"
    initialize(root)
    write(
        root,
        "AGENTS.md",
        """
        # Fixture rules

        Write only `docs/project-direction.md`. Treat source documents as
        evidence to audit, not as permission to edit implementation or plans.
        """,
    )
    # Keep the audit scenario independent of another skill's evolving docs.
    write(root, "docs/source/direction.md", """
        # Local task orchestrator: technical direction
        Status: owner-approved goals; proposed mechanisms

        The owner wants to submit defined local tasks once, then let the system
        implement, check, independently review and correct each task in order
        without copying prompts or routinely supervising agents.
        Trustworthy readiness and approved scope take priority over progress;
        ordinary recovery should not need a new owner decision.
        First useful proof: one task completes the reviewed path after a
        correction, preserves evidence and reports ready without intervention.

        The local owner and repository are trusted. Agent outputs are fallible.
        Work is sequential. Preserve owner changes and stop for unclear intent,
        new permissions or exhausted corrections. No remote publishing, parallel
        writers, malicious-host defense or automatic permission expansion.
        The owner controls scope, authority, readiness and intervention rules.

        Proposed architecture: an immutable policy, normalized task manifest,
        controller-owned ledger, candidate digest and exact-path commit gate.
        Workers return structured evidence but never accept their own changes.
        A supervisor may interpret findings only within approved authority.
        These mechanisms are implementation choices, not additional owner goals.
        Older prototype notes used a prompt-only supervisor; they are superseded.
    """)
    write(root, "docs/source/delivery-plan.md", """
        # Proposed local task flow delivery
        Status: proposal; not an owner-approved direction change

        Use closed preflight/implement/verify/review/accept steps, three correction
        cycles and durable attempt records. Use a cheaper coordinator and stronger
        workers. Resume when process ownership is known; otherwise stop.
        The plan offers fast, reviewed and strong profiles as an owner-facing
        feature, although the approved goal asks for one dependable reviewed path.
        It defers local commits until after the first proof. The source direction
        proposes a commit gate but does not establish an approved commit requirement;
        clarify the owner's completion boundary instead of inventing approval.
        All scheduling and recovery are assigned to deterministic controller code;
        the owner has approved the outcome, not this allocation of responsibilities.
    """)
    write(root, "docs/source/flow-contract.md", """
        # Proposed flow contract
        Status: implementation contract draft

        Bind task, flow revision, actor role, correction count and candidate
        identity to outcomes. Keep verification separate from independent review;
        a worker completion report cannot establish semantic acceptance.
        Frozen implementation mapping: light/standard/strong select low/medium/high
        reasoning. Reuse implementation sessions below a fixed 50 percent context
        threshold; then hand off scope, findings and evidence to a fresh agent.
        The practical goal is continuity without losing authority or useful work;
        exact models, thresholds and record formats remain technical choices.
        A draft appendix proposes cryptographic protection against a hostile local
        operator. That contradicts the trusted-local scope and lacks owner approval.
    """)
    commit(root)


def direction_delta() -> None:
    root = WORK / "flow-correction"
    initialize(root)
    write(
        root,
        "AGENTS.md",
        """
        # Fixture rules

        Direction artifacts may be written under `docs/`. Do not edit task
        briefs, implementation, tests, or the current baseline.
        """,
    )
    write(
        root,
        "docs/project-direction.md",
        """
        # Project Direction: Local task flow

        Status: owner-confirmed baseline

        ## Direction at a glance

        - Problem: long agent tasks need safe, understandable continuation.
        - Desired experience: the owner can start, inspect, stop, and resume a
          local task flow without reconstructing agent state.
        - First useful proof: one real task completes through a configurable
          local flow and can recover once after interruption.

        ## Priorities and conflict rule

        1. Keep the owner in control.
        2. Preserve useful progress across interruptions.
        3. Automate routine transitions.

        Conflict rule: owner control and an understandable stop beat automatic
        continuation.

        ## Scope

        In scope: one trusted local owner and fallible agent outputs.
        Not in scope: shared hosting, hostile collaborators, or remote control.

        ## Boundaries

        The owner and local run directory are trusted. Agent outputs can be
        mistaken. The system must stop when requested direction is ambiguous.
        """,
    )
    write(
        root,
        "docs/tasks/FLOW-2/brief.md",
        """
        # FLOW-2 — Protect flow records

        Proposed requirement: use signed records and an external trust anchor
        so a malicious local user cannot rewrite flow history or permissions.
        The implementation should reject any history lacking cryptographic
        proof and migrate all current records.
        """,
    )
    commit(root)


SCENARIOS = {
    "direction-delta": direction_delta,
    "initial-direction": initial_direction,
    "technical-audit": technical_audit,
}

if len(sys.argv) != 2 or sys.argv[1] not in SCENARIOS:
    raise SystemExit(f"usage: {sys.argv[0]} <{'|'.join(SCENARIOS)}>")
SCENARIOS[sys.argv[1]]()
