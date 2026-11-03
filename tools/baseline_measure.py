#!/usr/bin/env python3
"""Measure source instruction bytes; print JSON without changing repository files."""

import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess


RECORD = "docs/tasks/SIDE-003/baseline-measurements.json"


def file_metrics(path):
    data = path.read_bytes()
    return {"sha256": hashlib.sha256(data).hexdigest(), "file_bytes": len(data)}


def skill_metrics(path):
    data = path.read_bytes()
    frontmatter = re.match(rb"\A---\r?\n(.*?)^---(?=\r?$)", data, re.M | re.S)
    if frontmatter is None:
        raise ValueError(f"Missing frontmatter: {path}")
    lines = frontmatter[1].decode("utf-8").splitlines()
    index = next(i for i, line in enumerate(lines) if line.startswith("description:"))
    scalar = lines[index].split(":", 1)[1].strip()
    continuation = []
    for line in lines[index + 1:]:
        if line and not line[0].isspace():
            break
        continuation.append(line.strip())
    if scalar in {">", ">-", ">+"}:
        scalar = " ".join(continuation)
    elif continuation:
        scalar += " " + " ".join(continuation)
    description = " ".join(scalar.split())
    return {
        **file_metrics(path),
        "body_bytes": len(data) - frontmatter.end(),
        "description_characters": len(description),
    }


def profile_paths(root):
    tree = ast.parse((root / "scripts/install_development_skills.py").read_text())
    assignment = next(node for node in tree.body if isinstance(node, ast.AnnAssign)
                      and isinstance(node.target, ast.Name)
                      and node.target.id == "DEVELOPMENT_SKILL_SOURCES")
    return {relative + "/SKILL.md" for _, relative in ast.literal_eval(assignment.value)}


def sum_files(root, paths):
    files = sorted({(root / path).resolve().relative_to(root).as_posix() for path in paths})
    return {"files": files, "file_bytes": sum((root / path).stat().st_size for path in files)}


def read_graph(root, entries, instructions):
    """Separate package membership from literal, resolvable instruction links."""
    edges = set()
    for entry in entries:
        for reference in (root / entry).parent.joinpath("references").rglob("*"):
            if reference.is_file():
                edges.add((entry, reference.relative_to(root).as_posix(), "package_reference"))
    for source in instructions:
        text = (root / source).read_text()
        candidates = re.findall(r"\]\(([^)]+)\)", text)
        candidates += re.findall(r"`([^`\n]+)`", text)
        for candidate in candidates:
            candidate = candidate.split("#", 1)[0].strip("<>")
            if not re.fullmatch(r"[\w./-]+", candidate):
                continue
            target = ((root / source).parent / candidate).resolve()
            if target.is_relative_to(root) and target.is_file():
                relative = target.relative_to(root).as_posix()
                if relative in instructions:
                    edges.add((source, relative, "literal_link"))
    return [{"from": source, "to": target, "kind": kind}
            for source, target, kind in sorted(edges)]


def plan_comparison(root, skills):
    rows = re.findall(
        r"^\| ([\w-]+) \| (yes|no) \| ([\d,]+) \| ([\d,]+) \| ([\d,]+) \|$",
        (root / "docs/tasks/SIDE-003/plan.md").read_text(), re.M,
    )
    expected = {name: dict(zip(("file_bytes", "body_bytes", "description_characters"),
                              (int(value.replace(",", "")) for value in counts)))
                for name, _, *counts in rows}
    differences = []
    for skill in skills:
        before = expected[skill["name"]]
        delta = {key: skill[key] - value for key, value in before.items()}
        if any(delta.values()):
            differences.append({"path": skill["path"], "plan": before, "delta": delta})
    return {"plan_commit": "aa94e28eaf170b68b30300b3f7cb183943698076",
            "plan_skill_count": len(rows), "differences": differences}


def measure(root, record):
    profile = profile_paths(root)
    entries = sorted(path.relative_to(root).as_posix()
                     for path in (root / "skills").rglob("SKILL.md"))
    skills = [{"name": Path(path).parent.name, "path": path,
               "development_profile": path in profile, **skill_metrics(root / path)}
              for path in entries]
    routes = [{**route, **sum_files(root, route["files"])} for route in record["routes"]]
    instructions = set(entries) | {"AGENTS.md"}
    for entry in entries:
        for directory in ("references", "templates"):
            instructions.update(path.relative_to(root).as_posix()
                                for path in (root / entry).parent.joinpath(directory).rglob("*")
                                if path.is_file())
    instructions.update(path for route in routes for path in route["files"])
    totals = {}
    for label, selected in (("all", skills),
                            ("development_profile", [s for s in skills if s["development_profile"]])):
        totals[label] = {"skill_count": len(selected), **{
            key: sum(skill[key] for skill in selected)
            for key in ("file_bytes", "body_bytes", "description_characters")}}
    return {
        "schema_version": 1,
        "recording_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=root, text=True).strip(),
        "basis": record["basis"],
        "command_prerequisites": record["command_prerequisites"],
        "skills": skills,
        "totals": totals,
        "instruction_files": [{"path": path, **file_metrics(root / path)}
                              for path in sorted(instructions)],
        "read_graph": read_graph(root, entries, instructions),
        "routes": routes,
        "plan_comparison": plan_comparison(root, skills),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--record", default=RECORD, help="Static route/prerequisite input record")
    parser.add_argument("--sum", nargs="+", metavar="FILE", help="Sum an explicit unique-file list")
    args = parser.parse_args()
    root = args.root.resolve()
    result = (sum_files(root, args.sum) if args.sum else
              measure(root, json.loads((root / args.record).read_text())))
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))


if __name__ == "__main__":
    main()
