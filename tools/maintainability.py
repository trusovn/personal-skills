"""Static Python measurements for the first local maintainability experiment."""

import argparse
import ast
import base64
from collections import Counter
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import io
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
import tokenize
import tomllib


ROOT = Path(__file__).resolve().parents[1]
QUALITY = ROOT / ".quality"
FORMAT_VERSION = 1


def digest(data):
    return hashlib.sha256(data).hexdigest()


def command(args, cwd):
    result = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=120)
    return {"command": args, "exit_code": result.returncode,
            "stdout": result.stdout, "stderr": result.stderr}


def git_context(root):
    records = [command(["git", "rev-parse", "HEAD"], root),
               command(["git", "--no-optional-locks", "status", "--porcelain=v1", "--untracked-files=all"], root)]
    return {"head": records[0]["stdout"].strip() if records[0]["exit_code"] == 0 else None,
            "status": records[1]["stdout"], "commands": records}


def asset_group(path):
    parts = Path(path).parts
    if "tests" in parts or Path(path).name.startswith("test_"):
        return "test"
    if "evals" in parts or "fixtures" in parts or "benchmark" in parts:
        return "eval_or_harness"
    return "implementation"


def discover(root, scopes, excluded):
    files = set()
    skipped = set()
    for scope in scopes:
        path = root / scope
        if not path.exists():
            raise ValueError(f"Scope does not exist: {scope}")
        if path.is_symlink() or not path.resolve().is_relative_to(root):
            raise ValueError(f"Scope must be inside --root and not a symlink: {scope}")
        if set(Path(scope).parts) & excluded:
            raise ValueError(f"Explicit scope is excluded: {scope}")
        if path.is_file():
            if path.suffix != ".py":
                raise ValueError(f"Expected a Python file: {scope}")
            files.add(path.relative_to(root).as_posix())
            continue
        for folder, dirs, names in os.walk(path, onerror=raise_walk_error):
            parent = Path(folder)
            for name in list(dirs):
                child = parent / name
                if name in excluded or child.is_symlink():
                    skipped.add(child.relative_to(root).as_posix())
                    dirs.remove(name)
            for name in names:
                child = parent / name
                if child.suffix != ".py":
                    continue
                if child.is_symlink():
                    skipped.add(child.relative_to(root).as_posix())
                else:
                    files.add(child.relative_to(root).as_posix())
    if not files:
        raise ValueError("Scope contains no included Python files")
    return sorted(files), sorted(skipped)


def raise_walk_error(error):
    raise error


def capture(root, paths):
    return {path: (root / path).read_bytes() for path in paths}


def function_nodes(tree, scope=()):
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            qualified = (*scope, node.name)
            if not isinstance(node, ast.ClassDef):
                yield ".".join(qualified), node
            yield from function_nodes(node, qualified)
        else:
            yield from function_nodes(node, scope)


def complexity(sources, target):
    from radon.complexity import cc_visit_ast

    values, errors = [], []
    for path, data in sources.items():
        try:
            encoding, _ = tokenize.detect_encoding(io.BytesIO(data).readline)
            tree = ast.parse(data.decode(encoding), filename=path)
            for name, node in function_nodes(tree):
                # Each function is visited by Radon, including closures and local-class methods.
                # Class aggregates are never used as function scores.
                score = cc_visit_ast(node)[0].complexity
                values.append({"path": path, "symbol": name, "line": node.lineno,
                               "end_line": node.end_lineno, "value": score,
                               "target": target, "metric": "cyclomatic_complexity",
                               "asset_group": asset_group(path)})
        except (SyntaxError, UnicodeError, LookupError) as error:
            errors.append({"path": path, "error": str(error)})
    return values, errors


def tool_version(name):
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return None


def run_ruff(sources, config):
    with tempfile.TemporaryDirectory(prefix="maintainability-") as temporary:
        snapshot = Path(temporary).resolve()
        for path, data in sources.items():
            destination = snapshot / path
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
        config_path = snapshot / "experiment-ruff.toml"
        config_path.write_bytes(config)
        args = [sys.executable, "-m", "ruff", "check", "--config", str(config_path),
                "--no-cache", "--no-fix", "--ignore-noqa", "--output-format", "json", "."]
        record = command(args, snapshot)
        record["snapshot_root"] = str(snapshot)
        if record["exit_code"] not in (0, 1):
            return record, [], ["Ruff failed; see raw command output"]
        findings = json.loads(record["stdout"])
        normalized = []
        locations = {}
        for finding in findings:
            relative = Path(finding["filename"]).relative_to(snapshot).as_posix()
            if relative not in locations:
                try:
                    locations[relative] = {node.lineno: name for name, node in function_nodes(ast.parse(sources[relative]))}
                except SyntaxError:
                    locations[relative] = {}
            normalized.append({"path": relative, "line": finding["location"]["row"],
                               "code": finding["code"], "message": finding["message"],
                               "symbol": locations[relative].get(finding["location"]["row"]),
                               "asset_group": asset_group(relative)})
        syntax = [item for item in normalized if item["code"] not in ("PLR0913", "PLR0915")]
        return record, normalized, syntax


def measure(sources, checks, policy, ruff_config):
    results = {}
    for check in checks:
        version = tool_version("radon" if check == "complexity" else "ruff")
        result = {"status": "unavailable" if version is None else "completed",
                  "version": version, "errors": [], "values": []}
        results[check] = result
        if version is None:
            result["errors"].append("Install .quality/requirements.txt into .quality/venv")
            continue
        try:
            if check == "complexity":
                result["api"] = "radon.complexity.cc_visit_ast(function_node), defaults"
                result["values"], result["errors"] = complexity(sources, policy["complexity_target"])
            else:
                result["raw"], result["values"], result["errors"] = run_ruff(sources, ruff_config)
            if result["errors"]:
                result["status"] = "failed"
        except (OSError, ValueError, subprocess.TimeoutExpired) as error:
            result["status"] = "failed"
            result["errors"].append(str(error))
    return results


def symbol_key(item):
    return item["path"], item["symbol"]


def compare_complexity(current, previous):
    before = {symbol_key(item): item for item in previous}
    old_counts = Counter(map(symbol_key, previous))
    new_counts = Counter(map(symbol_key, current))
    missing = set(before) - set(new_counts)
    rows = []
    for item in current:
        key = symbol_key(item)
        old = before.get(key)
        row = dict(item, before=None, delta=None)
        if new_counts[key] > 1 or old_counts[key] > 1:
            row.update(classification="unmatched", requires_response=True)
        elif old is None:
            # Never guess move/rename/split relationships from similar scores or bodies.
            row.update(classification="unmatched" if missing else "new",
                       requires_response=bool(missing) or item["value"] > item["target"])
        else:
            delta = item["value"] - old["value"]
            classification = "worsened" if delta > 0 else "improved" if delta < 0 else "unchanged"
            row.update(before=old["value"], delta=delta, classification=classification,
                       requires_response=delta > 0)
        rows.append(row)
    for key in sorted(missing):
        rows.append(dict(before[key], before=before[key]["value"], value=None, delta=None,
                         classification="unmatched", requires_response=True))
    return rows


def comparison(report, baseline):
    if baseline is None:
        return {"status": "not_requested", "complexity": [], "ruff": []}
    reasons = []
    if baseline.get("format_version") != FORMAT_VERSION:
        reasons.append("report format differs")
    if baseline.get("identity") != report["identity"]:
        reasons.append("scope, tools, interpreter, adapter, or configuration differs")
    if baseline.get("measurement_status") != "complete" or report["measurement_status"] != "complete":
        reasons.append("baseline or current measurement is incomplete")
    if reasons:
        return {"status": "incompatible", "reasons": reasons, "complexity": [], "ruff": []}
    result = {"status": "compared", "complexity": [], "ruff": []}
    if "complexity" in report["checks"]:
        result["complexity"] = compare_complexity(report["checks"]["complexity"]["values"],
                                                 baseline["checks"]["complexity"]["values"])
    if "ruff" in report["checks"]:
        def finding_key(item):
            return item["path"], item["symbol"], item["code"], item["message"]

        old_findings = Counter(map(finding_key, baseline["checks"]["ruff"]["values"]))
        current_findings = Counter(map(finding_key, report["checks"]["ruff"]["values"]))
        for item in report["checks"]["ruff"]["values"]:
            key = finding_key(item)
            existed = key in old_findings
            ambiguous = item["symbol"] is None or old_findings[key] > 1 or current_findings[key] > 1
            classification = "unmatched" if ambiguous else "existing_diagnostic" if existed else "new_diagnostic"
            result["ruff"].append(dict(item, classification=classification,
                                       requires_response=ambiguous or not existed))
    return result


def summary_location(item):
    symbol = f" {item['symbol']}" if item.get("symbol") else ""
    return f"{item['path']}:{item['line']}{symbol} [{item['asset_group']}]"


def summary_change(item):
    if item["value"] is None:
        return f"CC {item['before']}->none"
    if item["before"] is None:
        return f"CC {item['value']}"
    return f"CC {item['before']}->{item['value']} ({item['delta']:+d})"


def summary_response(item):
    # Complexity comparison rows always carry "delta"; Ruff findings never do.
    if "delta" in item:
        return f"{item['classification']} {summary_change(item)}"
    return f"{item['classification']} {item['code']} {item['message']}"


def summary_comparison_lines(report):
    lines = [f"Required response items: {len(report['required_response'])}"]
    lines.extend(f"  Response required: {summary_response(item)}: {summary_location(item)}"
                 for item in report["required_response"])
    changed = [row for row in report["comparison"]["complexity"]
               if row["classification"] in ("new", "improved", "worsened")]
    lines.append(f"Changed symbols: {len(changed)}")
    lines.extend(f"  {row['classification'].capitalize()} {summary_change(row)}: {summary_location(row)}"
                 for row in changed)
    return lines


def summarize(report):
    groups = Counter(item["asset_group"] for item in report["files"].values())
    lines = [f"Measurement: {report['measurement_status']}; comparison: {report['comparison']['status']}",
             f"Files: {len(report['files'])} {dict(groups)}"]
    for name, check in report["checks"].items():
        lines.append(f"{name}: {check['status']} ({len(check['values'])} records)")
        if name == "complexity":
            breaches = sum(item["value"] > item["target"] for item in check["values"])
            lines.append(f"  Functions above target: {breaches}")
    if report["comparison"]["status"] == "compared":
        # Response identities and changed-symbol deltas come before the legacy top five.
        lines.extend(summary_comparison_lines(report))
    else:
        lines.append("Required response items: not evaluated (no compatible comparison)")
    complexity_values = report["checks"].get("complexity", {}).get("values", [])
    lines.append("Top five by complexity:")
    for item in sorted(complexity_values, key=lambda item: -item["value"])[:5]:
        lines.append(f"  CC {item['value']}: {item['path']}:{item['line']} {item['symbol']} [{item['asset_group']}]")
    lines.extend(f"Limit: {limit}" for limit in report["limitations"])
    lines.extend(f"Error: {error}" for error in report["errors"])
    lines.extend(f"Comparison: {reason}" for reason in report["comparison"].get("reasons", []))
    return "\n".join(lines) + "\n"


def build_report(root, scopes, checks):
    root = root.resolve()
    policy_bytes = (QUALITY / "maintainability.toml").read_bytes()
    ruff_bytes = (QUALITY / "ruff.toml").read_bytes()
    policy = tomllib.loads(policy_bytes.decode())
    context = git_context(root)
    paths, skipped = discover(root, scopes, set(policy["exclude_directories"]))
    sources = capture(root, paths)
    results = measure(sources, checks, policy, ruff_bytes)
    errors = []
    after_paths, _ = discover(root, scopes, set(policy["exclude_directories"]))
    if paths != after_paths or sources != capture(root, after_paths):
        errors.append("Source inputs changed during scanning; remeasure before comparison")
    after_context = git_context(root)
    if context != after_context:
        errors.append("Git context changed during scanning; remeasure before comparison")
    identity = {"root": str(root), "scope": scopes, "checks": checks,
                "python": platform.python_version(),
                "tools": {name: check["version"] for name, check in results.items()},
                "adapter_sha256": digest(Path(__file__).read_bytes()),
                "policy": policy_bytes.decode(), "ruff_config": ruff_bytes.decode()}
    complete = not errors and all(check["status"] == "completed" for check in results.values())
    return {"format_version": FORMAT_VERSION, "profile": policy["profile"],
            "captured_at": datetime.now(timezone.utc).isoformat(),
            "requested_checks": checks, "full_profile": checks == sorted(policy["checks"]),
            "identity": identity, "repository": context, "invocation": sys.argv,
            "excluded_directories": policy["exclude_directories"], "skipped_paths": skipped,
            "files": {path: {"sha256": digest(data), "source_base64": base64.b64encode(data).decode(),
                              "asset_group": asset_group(path)} for path, data in sources.items()},
            "checks": results, "measurement_status": "complete" if complete else "incomplete",
            "hard_rules": "not_run", "errors": errors,
            "limitations": ["Advisory experiment; metrics do not establish design or functional acceptance.",
                             "Ruff supplies target diagnostics only; statement/argument no-increase comparison is unavailable.",
                             "Moves, renames, splits, and duplicate qualified names require explicit human matching.",
                             "Coverage, cognitive complexity, and architecture rules are not collected."]}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=["measure", "baseline", "compare"])
    parser.add_argument("paths", nargs="*", help="Python files/folders relative to --root; default: .")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--checks", nargs="+", choices=["complexity", "ruff"])
    parser.add_argument("--baseline", type=Path, help="Previously captured report; required for compare")
    parser.add_argument("--output", type=Path, help="Save JSON and text reports; otherwise print the summary only")
    args = parser.parse_args(argv)
    if (args.operation == "compare") != (args.baseline is not None):
        parser.error("Use --baseline only with compare, which requires it")
    if args.operation == "baseline" and args.output is None:
        parser.error("baseline requires --output to preserve the measurement")
    try:
        if args.output is not None:
            if args.output.exists() or args.output.with_suffix(".txt").exists():
                raise ValueError("Report or summary already exists; choose a new --output")
            if args.output.suffix != ".json":
                raise ValueError("--output must end in .json")
        root = args.root.resolve(strict=True)
        scopes = []
        for value in args.paths or ["."]:
            path = Path(value)
            if ".." in path.parts:
                raise ValueError("Scope cannot contain '..'")
            scopes.append((path if path.is_absolute() else root / path).relative_to(root).as_posix())
        baseline = json.loads(args.baseline.read_text()) if args.baseline else None
        if baseline is not None and not isinstance(baseline, dict):
            raise ValueError("Baseline must be a JSON report object")
        default_checks = tomllib.loads((QUALITY / "maintainability.toml").read_text())["checks"]
        checks = sorted(set(args.checks or default_checks))
        if not checks or set(checks) - {"complexity", "ruff"}:
            raise ValueError("Profile must select supported checks: complexity, ruff")
        report = build_report(root, sorted(set(scopes)), checks)
        report["operation"] = args.operation
        report["baseline_path"] = str(args.baseline.resolve()) if args.baseline else None
        report["comparison"] = comparison(report, baseline)
        if report["comparison"]["status"] == "compared":
            items = report["comparison"]["complexity"] + report["comparison"]["ruff"]
            report["required_response"] = [item for item in items if item["requires_response"]]
        else:
            report["required_response"] = []
        summary = summarize(report)
        if args.output is not None:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with args.output.open("x") as stream:
                json.dump(report, stream, indent=2)
                stream.write("\n")
            with args.output.with_suffix(".txt").open("x") as stream:
                stream.write(summary)
        print(summary, end="")
        if args.output is not None:
            print(f"Report: {args.output}")
        return 2 if report["measurement_status"] != "complete" or report["comparison"]["status"] == "incompatible" else 0
    except (OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as error:
        print(f"Measurement error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
