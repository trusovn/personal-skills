#!/usr/bin/env python3
"""Measure a target repository with installation-local, platform-native tools."""

from pathlib import Path
import runpy


runpy.run_path(str(Path(__file__).resolve().with_name("maintainability_env.py")), run_name="__main__")
