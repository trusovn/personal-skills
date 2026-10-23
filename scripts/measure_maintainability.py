#!/usr/bin/env python3
"""Run the repository-local experiment with its isolated Python environment."""

import os
from pathlib import Path
import runpy
import sys


ROOT = Path(__file__).resolve().parents[1]
PYTHON = ROOT / ".quality" / "venv" / "bin" / "python"
if PYTHON.is_file() and Path(sys.prefix) != PYTHON.parent.parent:
    os.execv(str(PYTHON), [str(PYTHON), str(Path(__file__).resolve()), *sys.argv[1:]])

runpy.run_path(str(ROOT / "tools" / "maintainability.py"), run_name="__main__")
