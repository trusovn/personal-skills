#!/usr/bin/env python3
"""Structural/freshness helper for project plan verification.

Checks required headings, validates task-map references/graph, and prints SHA-256
hashes. No third-party dependencies. Semantic completeness still requires the skill's
independent review protocol.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

REQUIRED_HEADINGS = [
    "Planning authority",
    "Scope",
    "Actors and capabilities",
    "Artifact and state catalog",
    "Lifecycle/state models",
    "Cross-task invariants",
    "System interface map",
    "End-to-end data/process/state flows",
    "Capability-to-flow coverage",
    "Implementation task map",
    "System verification map",
    "Risks, assumptions, and delegated choices",
    "Plan-verification handoff",
]

PREFIXES = {
    "capabilities": "CAP-",
    "artifacts": "ART-",
    "interfaces": "IF-",
    "invariants": "INV-",
    "flows": "FLOW-",
    "tasks": "T-",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: verify_plan_artifacts.py <docs/project-plan.md> <docs/task-map.json>", file=sys.stderr)
        return 2

    plan_path, map_path = map(Path, sys.argv[1:])
    errors: list[str] = []

    for path in (plan_path, map_path):
        if not path.exists():
            errors.append(f"missing required artifact: {path}")

    if errors:
        for e in errors:
            print("ERROR:", e)
        return 1

    plan = plan_path.read_text(encoding="utf-8")
    headings = [m.group(1).strip() for m in re.finditer(r"^#{1,6}\s+(.+?)\s*$", plan, re.MULTILINE)]
    normalized_headings = [re.sub(r"^\d+(?:\.\d+)*\.\s+", "", h).strip().lower() for h in headings]
    for required in REQUIRED_HEADINGS:
        if required.lower() not in normalized_headings:
            errors.append(f"project plan missing heading: {required}")

    try:
        data = json.loads(map_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"task map invalid JSON: {exc}")
        data = {}

    ids: dict[str, set[str]] = {}
    if isinstance(data, dict):
        if data.get("schema_version") != "1.0":
            errors.append("task map schema_version must be '1.0'")
        for section, prefix in PREFIXES.items():
            rows = data.get(section)
            if not isinstance(rows, list):
                errors.append(f"task map {section} must be an array")
                ids[section] = set()
                continue
            section_ids = []
            for i, row in enumerate(rows):
                if not isinstance(row, dict) or not isinstance(row.get("id"), str):
                    errors.append(f"{section}[{i}] missing string id")
                    continue
                ident = row["id"]
                if not ident.startswith(prefix):
                    errors.append(f"{section}[{i}] id {ident!r} must start with {prefix!r}")
                section_ids.append(ident)
            if len(section_ids) != len(set(section_ids)):
                errors.append(f"duplicate IDs in {section}")
            ids[section] = set(section_ids)

        def refs(owner: str, row: dict, field: str, allowed: set[str]):
            value = row.get(field, [])
            if not isinstance(value, list):
                errors.append(f"{owner}.{field} must be an array")
                return
            for ref in value:
                if ref not in allowed:
                    errors.append(f"{owner}.{field} unresolved reference: {ref!r}")

        for row in data.get("capabilities", []) if isinstance(data.get("capabilities"), list) else []:
            if isinstance(row, dict) and isinstance(row.get("id"), str):
                refs(row["id"], row, "flows", ids.get("flows", set()))

        for row in data.get("interfaces", []) if isinstance(data.get("interfaces"), list) else []:
            if isinstance(row, dict) and isinstance(row.get("id"), str):
                refs(row["id"], row, "inputs", ids.get("artifacts", set()))
                refs(row["id"], row, "outputs", ids.get("artifacts", set()))

        allowed_inv = ids.get("artifacts", set()) | ids.get("flows", set()) | ids.get("interfaces", set())
        for row in data.get("invariants", []) if isinstance(data.get("invariants"), list) else []:
            if isinstance(row, dict) and isinstance(row.get("id"), str):
                refs(row["id"], row, "applies_to", allowed_inv)

        for flow in data.get("flows", []) if isinstance(data.get("flows"), list) else []:
            if not isinstance(flow, dict) or not isinstance(flow.get("id"), str):
                continue
            for i, step in enumerate(flow.get("steps", []) if isinstance(flow.get("steps"), list) else []):
                if not isinstance(step, dict):
                    errors.append(f"{flow['id']}.steps[{i}] must be object")
                    continue
                owner = f"{flow['id']}.steps[{i}]"
                refs(owner, step, "consumes", ids.get("artifacts", set()))
                refs(owner, step, "produces", ids.get("artifacts", set()))
                refs(owner, step, "interfaces", ids.get("interfaces", set()))
                refs(owner, step, "invariants", ids.get("invariants", set()))

        tasks = data.get("tasks", []) if isinstance(data.get("tasks"), list) else []
        graph: dict[str, list[str]] = {}
        for task in tasks:
            if not isinstance(task, dict) or not isinstance(task.get("id"), str):
                continue
            tid = task["id"]
            refs(tid, task, "depends_on", ids.get("tasks", set()))
            refs(tid, task, "capabilities", ids.get("capabilities", set()))
            refs(tid, task, "flows", ids.get("flows", set()))
            refs(tid, task, "consumes", ids.get("artifacts", set()))
            refs(tid, task, "produces", ids.get("artifacts", set()))
            refs(tid, task, "interfaces", ids.get("interfaces", set()))
            refs(tid, task, "invariants", ids.get("invariants", set()))
            deps = task.get("depends_on", [])
            graph[tid] = [d for d in deps if isinstance(d, str) and d in ids.get("tasks", set())] if isinstance(deps, list) else []

        # Cycle detection.
        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(node: str, chain: list[str]):
            if node in visiting:
                idx = chain.index(node) if node in chain else 0
                errors.append("task dependency cycle: " + " -> ".join(chain[idx:] + [node]))
                return
            if node in visited:
                return
            visiting.add(node)
            chain.append(node)
            for dep in graph.get(node, []):
                visit(dep, chain)
            chain.pop()
            visiting.remove(node)
            visited.add(node)

        for node in graph:
            visit(node, [])

    print(f"project-plan sha256: {sha256(plan_path)}")
    print(f"task-map     sha256: {sha256(map_path)}")

    if errors:
        print(f"FAIL: {len(errors)} structural issue(s)")
        for e in errors:
            print(f"- {e}")
        return 1

    print("PASS: planning artifacts are structurally reviewable")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
