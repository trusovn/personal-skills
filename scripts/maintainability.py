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
import re
import subprocess
import sys
import tempfile
import tokenize
import tomllib


SCRIPTS = Path(__file__).resolve().parent
DEFAULT_FILES = {"maintainability.toml": SCRIPTS / "maintainability-default.toml",
                 "ruff.toml": SCRIPTS / "maintainability-ruff-default.toml"}
FORMAT_VERSION = 4
RUFF_COLLECTION_LIMITS = {"lint.pylint.max-args": 0, "lint.pylint.max-statements": 0}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def validate_policy(policy):
    profile = policy.get("profile")
    if not isinstance(profile, str) or not profile.strip():
        raise ValueError("profile must be a non-empty string")
    checks = policy.get("checks")
    if (not isinstance(checks, list) or not checks
            or any(not isinstance(check, str) or check not in ("complexity", "ruff") for check in checks)):
        raise ValueError("checks must be a non-empty list of supported checks: complexity, ruff")
    target = policy.get("complexity_target")
    if type(target) is not int or target < 0:
        raise ValueError("complexity_target must be a non-negative integer")
    excluded = policy.get("exclude_directories")
    if (not isinstance(excluded, list)
            or any(not isinstance(name, str) or not name.strip() for name in excluded)):
        raise ValueError("exclude_directories must be a list of non-empty directory names")


def settings(root):
    contents, origins = {}, {}
    for name, default in DEFAULT_FILES.items():
        target = root / ".quality" / name
        path = target if target.exists() or target.is_symlink() else default
        data = path.read_bytes()
        try:
            parsed = tomllib.loads(data.decode())
            if name == "maintainability.toml":
                validate_policy(parsed)
        except ValueError as error:
            raise ValueError(f"Invalid settings {path}: {error}") from error
        contents[name] = data
        origins[name] = {"origin": "target" if path == target else "shipped",
                         "path": str(path), "sha256": digest(data)}
    return contents, origins


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


def discover(root, scopes, excluded, known_files=()):
    files = set()
    skipped = set()
    for scope in scopes:
        path = root / scope
        if path.is_symlink() or not path.resolve().is_relative_to(root):
            raise ValueError(f"Scope must be inside --root and not a symlink: {scope}")
        if set(Path(scope).parts) & excluded:
            raise ValueError(f"Explicit scope is excluded: {scope}")
        if not path.exists():
            if scope in known_files:
                continue
            raise ValueError(f"Scope does not exist: {scope}")
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
    if not files and not known_files:
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
    targets = tomllib.loads(config.decode())["lint"]["pylint"]
    with tempfile.TemporaryDirectory(prefix="maintainability-") as temporary:
        snapshot = Path(temporary).resolve()
        for path, data in sources.items():
            destination = snapshot / path
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
        config_path = snapshot / "experiment-ruff.toml"
        config_path.write_bytes(config)
        args = [sys.executable, "-m", "ruff", "check", "--config", str(config_path),
                "--no-cache", "--no-fix", "--ignore-noqa", "--output-format", "json"]
        for setting, value in RUFF_COLLECTION_LIMITS.items():
            args.extend(["--config", f"{setting}={value}"])
        args.append(".")
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
            if finding["code"] in ("PLR0913", "PLR0915"):
                count = re.search(r"\((\d+) > (\d+)\)$", finding["message"])
                if count is None:
                    raise ValueError(f"Unrecognized Ruff count: {finding['message']}")
                target_name = "max-args" if finding["code"] == "PLR0913" else "max-statements"
                normalized[-1].update(value=int(count[1]), collection_threshold=int(count[2]),
                                      target=targets[target_name], metric=finding["code"])
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
            result["errors"].append("Run python3 scripts/measure_maintainability.py setup")
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
    return item["path"], item["symbol"], item["metric"]


def numeric_change(item, old):
    delta = item["value"] - old["value"]
    classification = "worsened" if delta > 0 else "improved" if delta < 0 else "unchanged"
    highlights = ["got_worse"] if delta > 0 else ["improved"] if delta < 0 else []
    if old["value"] <= item["target"] < item["value"]:
        highlights.append("crossed_above_threshold")
    return {"before": old["value"], "delta": delta, "classification": classification, "highlights": highlights}


def compare_values(current, previous, diagnostics=False):
    before = {symbol_key(item): item for item in previous}
    old_counts = Counter(map(symbol_key, previous))
    new_counts = Counter(map(symbol_key, current))
    rows = []
    for item in current:
        key = symbol_key(item)
        old = before.get(key)
        row = dict(item, before=None, delta=None)
        if item["symbol"] is None or new_counts[key] > 1 or old_counts[key] > 1:
            row.update(classification="unmatched", highlights=["needs_interpretation"])
        elif old is None:
            # Never guess move/rename/split relationships from similar scores or bodies.
            if diagnostics:
                highlights = ["above_threshold"] if item["value"] > item["target"] else []
                row.update(classification="new_diagnostic", highlights=highlights + ["needs_interpretation"])
            else:
                highlights = ["new_above_threshold"] if item["value"] > item["target"] else []
                row.update(classification="new", highlights=highlights + ["needs_interpretation"])
        else:
            row.update(numeric_change(item, old))
        rows.append(row)
    for key in sorted(set(before) - set(new_counts)):
        rows.append(dict(before[key], before=before[key]["value"], value=None, delta=None,
                         classification="diagnostic_resolved" if diagnostics else "removed",
                         highlights=["needs_interpretation"]))
    return rows


def comparison_identity(report):
    identity = dict(report.get("identity", {}))
    # Mount paths and patch releases are provenance, not measurement settings.
    identity.pop("root", None)
    identity.pop("scope", None)
    identity.pop("scope_directories", None)
    identity.pop("settings", None)  # Origins are provenance; effective bytes below decide compatibility.
    identity["python"] = ".".join(identity.get("python", "").split(".")[:2])
    return identity


def within_scope(path, scopes):
    return any(Path(path).is_relative_to(scope) for scope in scopes)


def comparison(report, baseline):
    if baseline is None:
        return {"status": "not_requested", "complexity": [], "ruff": []}
    reasons = []
    if baseline.get("format_version") != FORMAT_VERSION:
        reasons.append("report format differs")
    if comparison_identity(baseline) != comparison_identity(report):
        reasons.append("tools, Python major/minor, adapter, or configuration differs")
    baseline_scopes = baseline.get("identity", {}).get("scope", [])
    baseline_directories = baseline.get("identity", {}).get("scope_directories", [])
    scopes = report["identity"]["scope"]
    if any(scope not in baseline_scopes and not within_scope(scope, baseline_directories) for scope in scopes):
        reasons.append("current scope is outside the baseline scope")
    if baseline.get("measurement_status") != "complete" or report["measurement_status"] != "complete":
        reasons.append("baseline or current measurement is incomplete")
    if reasons:
        return {"status": "incompatible", "reasons": reasons, "complexity": [], "ruff": []}
    result = {"status": "compared", "complexity": [], "ruff": []}
    for check in report["checks"]:
        previous = [item for item in baseline["checks"][check]["values"] if within_scope(item["path"], scopes)]
        result[check] = compare_values(report["checks"][check]["values"], previous, diagnostics=check == "ruff")
    return result


def summary_location(item):
    symbol = f" {item['symbol']}" if item.get("symbol") else ""
    return f"{item['path']}:{item['line']}{symbol} [{item['asset_group']}]"


def summary_change(item):
    label = "CC" if item["metric"] == "cyclomatic_complexity" else item["metric"]
    if item["value"] is None:
        return f"{label} {item['before']}->none"
    if item["before"] is None:
        return f"{label} {item['value']}"
    return f"{label} {item['before']}->{item['value']} ({item['delta']:+d})"


def report_highlights(report):
    if report["comparison"]["status"] == "compared":
        return [row for check in ("complexity", "ruff") for row in report["comparison"][check] if row["highlights"]]
    return [dict(item, before=None, delta=None, highlights=["above_threshold"])
            for check in report["checks"].values() for item in check["values"]
            if "value" in item and item["value"] > item["target"]]


def summarize(report):
    groups = Counter(item["asset_group"] for item in report["files"].values())
    lines = [f"Measurement: {report['measurement_status']}; comparison: {report['comparison']['status']}",
             f"Files: {len(report['files'])} {dict(groups)}"]
    for name, check in report["checks"].items():
        lines.append(f"{name}: {check['status']} ({len(check['values'])} records)")
        if name == "complexity":
            breaches = sum(item["value"] > item["target"] for item in check["values"])
            lines.append(f"  Functions above target: {breaches}")
        lines.extend(f"  Error: {error}" for error in check["errors"])
    lines.append(f"Highlights: {len(report['highlights'])}")
    for item in report["highlights"]:
        labels = ", ".join(item["highlights"]).replace("_", " ").capitalize()
        lines.append(f"  {labels}: {summary_change(item)}: {summary_location(item)}")
    if report["comparison"]["status"] != "compared":
        lines.append("Change highlights unavailable (no compatible comparison)")
    complexity_values = report["checks"].get("complexity", {}).get("values", [])
    lines.append("Top five by complexity:")
    for item in sorted(complexity_values, key=lambda item: -item["value"])[:5]:
        lines.append(f"  CC {item['value']}: {item['path']}:{item['line']} {item['symbol']} [{item['asset_group']}]")
    lines.extend(f"Limit: {limit}" for limit in report["limitations"])
    lines.extend(f"Error: {error}" for error in report["errors"])
    lines.extend(f"Comparison: {reason}" for reason in report["comparison"].get("reasons", []))
    return "\n".join(lines) + "\n"


def build_report(root, scopes, checks, baseline=None):
    root = root.resolve()
    effective, origins = settings(root)
    policy_bytes = effective["maintainability.toml"]
    ruff_bytes = effective["ruff.toml"]
    policy = tomllib.loads(policy_bytes.decode())
    context = git_context(root)
    known_files = baseline.get("files", {}) if baseline else ()
    paths, skipped = discover(root, scopes, set(policy["exclude_directories"]), known_files)
    sources = capture(root, paths)
    results = measure(sources, checks, policy, ruff_bytes)
    errors = []
    after_paths, _ = discover(root, scopes, set(policy["exclude_directories"]), known_files)
    if paths != after_paths or sources != capture(root, after_paths):
        errors.append("Source inputs changed during scanning; remeasure before comparison")
    after_context = git_context(root)
    if context != after_context:
        errors.append("Git context changed during scanning; remeasure before comparison")
    identity = {"root": str(root), "scope": scopes, "checks": checks,
                "scope_directories": [scope for scope in scopes if (root / scope).is_dir()],
                "python": platform.python_version(),
                "python_implementation": platform.python_implementation(),
                "tools": {name: check["version"] for name, check in results.items()},
                "adapter_sha256": digest(Path(__file__).read_bytes()),
                "policy": policy_bytes.decode(), "ruff_config": ruff_bytes.decode(),
                "settings": origins,
                "ruff_collection_limits": dict(RUFF_COLLECTION_LIMITS)}
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
                             "Ruff uses zero-limit collection with separate advisory targets. Missing diagnostics are unknown, not zero; native exemptions and return-only bodies can leave gaps. Deltas require numeric evidence on both sides.",
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
        root = args.root.resolve(strict=True)
        if args.output is not None:
            args.output = root / args.output
        if args.baseline is not None:
            args.baseline = root / args.baseline
        if args.output is not None:
            if args.output.exists() or args.output.with_suffix(".txt").exists():
                raise ValueError("Report or summary already exists; choose a new --output")
            if args.output.suffix != ".json":
                raise ValueError("--output must end in .json")
        scopes = []
        for value in args.paths or ["."]:
            path = Path(value)
            if ".." in path.parts:
                raise ValueError("Scope cannot contain '..'")
            scopes.append((path if path.is_absolute() else root / path).relative_to(root).as_posix())
        baseline = json.loads(args.baseline.read_text()) if args.baseline else None
        if baseline is not None and not isinstance(baseline, dict):
            raise ValueError("Baseline must be a JSON report object")
        effective, _ = settings(root)
        default_checks = tomllib.loads(effective["maintainability.toml"].decode())["checks"]
        checks = sorted(set(args.checks or default_checks))
        if not checks or set(checks) - {"complexity", "ruff"}:
            raise ValueError("Profile must select supported checks: complexity, ruff")
        report = build_report(root, sorted(set(scopes)), checks, baseline=baseline)
        report["operation"] = args.operation
        report["baseline_path"] = str(args.baseline.resolve()) if args.baseline else None
        report["comparison"] = comparison(report, baseline)
        report["highlights"] = report_highlights(report)
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
