#!/usr/bin/env python3
"""Run the repository-local experiment with platform-local dependencies."""

from pathlib import Path
import runpy


ROOT = Path(__file__).resolve().parents[1]
runpy.run_path(str(ROOT / "tools" / "maintainability_env.py"), run_name="__main__")
