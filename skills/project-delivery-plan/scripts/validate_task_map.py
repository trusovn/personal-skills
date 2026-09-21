#!/usr/bin/env python3
"""Structural validator for docs/task-map.json.

No third-party dependencies. It intentionally validates references and graph structure,
not semantic completeness.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

PREFIXES = {
    "capabilities": "CAP-",
    "artifacts": "ART-",
    "interfaces": "IF-",
    "invariants": "INV-",
    "flows": "FLOW-",
    "tasks": "T-",
}


def fail(errors: list[str], msg: str) -> None:
    errors.append(msg)


def load(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        sys.exit(2)
    except json.JSONDecodeError as exc:
        print(f"ERROR: invalid JSON: {exc}", file=sys.stderr)
        sys.exit(2)


def ids_for(data: dict, section: str, errors: list[str]) -> set[str]:
    value = data.get(section)
    if not isinstance(value, list):
        fail(errors, f"{section}: must be an array")
        return set()
    ids: list[str] = []
    for idx, item in enumerate(value):
        if not isinstance(item, dict):
            fail(errors, f"{section}[{idx}]: must be an object")
            continue
        ident = item.get("id")
        if not isinstance(ident, str) or not ident:
            fail(errors, f"{section}[{idx}].id: required non-empty string")
            continue
        if not ident.startswith(PREFIXES[section]):
            fail(errors, f"{section}[{idx}].id: {ident!r} must start with {PREFIXES[section]!r}")
        ids.append(ident)
    if len(ids) != len(set(ids)):
        dups = sorted({x for x in ids if ids.count(x) > 1})
        fail(errors, f"{section}: duplicate IDs: {', '.join(dups)}")
    return set(ids)


def require_list_refs(errors: list[str], owner: str, item: dict, field: str, allowed: set[str]) -> None:
    refs = item.get(field, [])
    if not isinstance(refs, list):
        fail(errors, f"{owner}.{field}: must be an array")
        return
    for ref in refs:
        if not isinstance(ref, str):
            fail(errors, f"{owner}.{field}: references must be strings")
        elif ref not in allowed:
            fail(errors, f"{owner}.{field}: unresolved reference {ref!r}")


def detect_task_cycles(tasks: list[dict], task_ids: set[str], errors: list[str]) -> None:
    graph: dict[str, list[str]] = {}
    for task in tasks:
        tid = task.get("id")
        if tid not in task_ids:
            continue
        deps = task.get("depends_on", [])
        if not isinstance(deps, list):
            fail(errors, f"{tid}.depends_on: must be an array")
            deps = []
        graph[tid] = [d for d in deps if isinstance(d, str) and d in task_ids]

    WHITE, GRAY, BLACK = 0, 1, 2
    color = {n: WHITE for n in graph}
    stack: list[str] = []

    def visit(node: str) -> None:
        color[node] = GRAY
        stack.append(node)
        for dep in graph.get(node, []):
            if color.get(dep, WHITE) == WHITE:
                visit(dep)
            elif color.get(dep) == GRAY:
                try:
                    start = stack.index(dep)
                except ValueError:
                    start = 0
                cycle = stack[start:] + [dep]
                fail(errors, "task dependency cycle: " + " -> ".join(cycle))
        stack.pop()
        color[node] = BLACK

    for node in graph:
        if color[node] == WHITE:
            visit(node)


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_task_map.py <docs/task-map.json>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    data = load(path)
    errors: list[str] = []

    if not isinstance(data, dict):
        print("ERROR: top-level JSON must be an object", file=sys.stderr)
        return 2

    if data.get("schema_version") != "1.0":
        fail(errors, "schema_version: expected '1.0'")
    if not isinstance(data.get("project"), str) or not data.get("project", "").strip():
        fail(errors, "project: required non-empty string")
    if not isinstance(data.get("plan_path"), str) or not data.get("plan_path", "").strip():
        fail(errors, "plan_path: required non-empty string")

    ids = {section: ids_for(data, section, errors) for section in PREFIXES}

    # Capabilities -> flows.
    for cap in data.get("capabilities", []) if isinstance(data.get("capabilities"), list) else []:
        if isinstance(cap, dict) and isinstance(cap.get("id"), str):
            require_list_refs(errors, cap["id"], cap, "flows", ids["flows"])
            if not cap.get("flows"):
                fail(errors, f"{cap['id']}.flows: capability must map to at least one flow")

    # Interfaces -> artifact refs.
    for interface in data.get("interfaces", []) if isinstance(data.get("interfaces"), list) else []:
        if isinstance(interface, dict) and isinstance(interface.get("id"), str):
            require_list_refs(errors, interface["id"], interface, "inputs", ids["artifacts"])
            require_list_refs(errors, interface["id"], interface, "outputs", ids["artifacts"])
            if not isinstance(interface.get("contract"), str) or not interface.get("contract", "").strip():
                fail(errors, f"{interface['id']}.contract: required non-empty string")

    # Invariants may reference artifact, flow, or interface IDs.
    invariant_targets = ids["artifacts"] | ids["flows"] | ids["interfaces"]
    for inv in data.get("invariants", []) if isinstance(data.get("invariants"), list) else []:
        if isinstance(inv, dict) and isinstance(inv.get("id"), str):
            require_list_refs(errors, inv["id"], inv, "applies_to", invariant_targets)
            if not isinstance(inv.get("statement"), str) or not inv.get("statement", "").strip():
                fail(errors, f"{inv['id']}.statement: required non-empty string")

    # Flow steps.
    step_ids: list[str] = []
    for flow in data.get("flows", []) if isinstance(data.get("flows"), list) else []:
        if not isinstance(flow, dict) or not isinstance(flow.get("id"), str):
            continue
        fid = flow["id"]
        steps = flow.get("steps")
        if not isinstance(steps, list) or not steps:
            fail(errors, f"{fid}.steps: required non-empty array")
            continue
        if not isinstance(flow.get("trigger"), str) or not flow.get("trigger", "").strip():
            fail(errors, f"{fid}.trigger: required non-empty string")
        if not isinstance(flow.get("terminal_outcome"), str) or not flow.get("terminal_outcome", "").strip():
            fail(errors, f"{fid}.terminal_outcome: required non-empty string")
        for idx, step in enumerate(steps):
            owner = f"{fid}.steps[{idx}]"
            if not isinstance(step, dict):
                fail(errors, f"{owner}: must be an object")
                continue
            sid = step.get("id")
            if not isinstance(sid, str) or not sid:
                fail(errors, f"{owner}.id: required non-empty string")
            else:
                step_ids.append(sid)
                if not re.fullmatch(re.escape(fid) + r"-S\d+", sid):
                    fail(errors, f"{owner}.id: {sid!r} should match {fid}-S<digits>")
            require_list_refs(errors, owner, step, "consumes", ids["artifacts"])
            require_list_refs(errors, owner, step, "produces", ids["artifacts"])
            require_list_refs(errors, owner, step, "interfaces", ids["interfaces"])
            require_list_refs(errors, owner, step, "invariants", ids["invariants"])
            if not isinstance(step.get("action"), str) or not step.get("action", "").strip():
                fail(errors, f"{owner}.action: required non-empty string")
    if len(step_ids) != len(set(step_ids)):
        dups = sorted({x for x in step_ids if step_ids.count(x) > 1})
        fail(errors, "duplicate flow step IDs: " + ", ".join(dups))

    # Tasks.
    tasks = data.get("tasks", []) if isinstance(data.get("tasks"), list) else []
    for task in tasks:
        if not isinstance(task, dict) or not isinstance(task.get("id"), str):
            continue
        tid = task["id"]
        require_list_refs(errors, tid, task, "depends_on", ids["tasks"])
        require_list_refs(errors, tid, task, "capabilities", ids["capabilities"])
        require_list_refs(errors, tid, task, "flows", ids["flows"])
        require_list_refs(errors, tid, task, "consumes", ids["artifacts"])
        require_list_refs(errors, tid, task, "produces", ids["artifacts"])
        require_list_refs(errors, tid, task, "interfaces", ids["interfaces"])
        require_list_refs(errors, tid, task, "invariants", ids["invariants"])
        if not task.get("capabilities") and not task.get("flows"):
            fail(errors, f"{tid}: task must map to at least one capability or flow")
        for field in ("title", "outcome", "integration_boundary", "task_planner_context"):
            if not isinstance(task.get(field), str) or not task.get(field, "").strip():
                fail(errors, f"{tid}.{field}: required non-empty string")
    detect_task_cycles(tasks, ids["tasks"], errors)

    # Open questions.
    questions = data.get("open_system_questions")
    if not isinstance(questions, list):
        fail(errors, "open_system_questions: must be an array")
    else:
        allowed_blocks = ids["flows"] | ids["tasks"] | ids["interfaces"] | ids["artifacts"] | ids["invariants"]
        qids: list[str] = []
        for idx, q in enumerate(questions):
            if not isinstance(q, dict):
                fail(errors, f"open_system_questions[{idx}]: must be an object")
                continue
            qid = q.get("id")
            if not isinstance(qid, str) or not re.fullmatch(r"Q-\d+", qid):
                fail(errors, f"open_system_questions[{idx}].id: expected Q-<digits>")
            else:
                qids.append(qid)
            require_list_refs(errors, qid or f"question[{idx}]", q, "blocks", allowed_blocks)
            if not isinstance(q.get("question"), str) or not q.get("question", "").strip():
                fail(errors, f"open_system_questions[{idx}].question: required non-empty string")
        if len(qids) != len(set(qids)):
            dups = sorted({x for x in qids if qids.count(x) > 1})
            fail(errors, "duplicate open question IDs: " + ", ".join(dups))

    if errors:
        print(f"FAIL: {len(errors)} structural issue(s)")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS: task map is structurally consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
