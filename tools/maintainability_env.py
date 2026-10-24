"""Select or explicitly provision native dependencies; never share venv binaries."""

import hashlib
import importlib.metadata
import os
from pathlib import Path
import platform
import runpy
import subprocess
import sys
import venv


ROOT = Path(__file__).resolve().parents[1]
REQUIREMENTS = ROOT / ".quality/requirements.txt"


def environment_path():
    pins = hashlib.sha256(REQUIREMENTS.read_bytes()).hexdigest()[:12]
    key = f"{platform.system()}-{platform.machine()}-{sys.implementation.name}-{platform.python_version()}-{pins}"
    return ROOT / ".quality/envs" / key


def environment_python(environment):
    return environment / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def pins_available():
    for line in REQUIREMENTS.read_text().splitlines():
        name, version = line.split("==")
        try:
            if importlib.metadata.version(name) != version:
                return False
        except importlib.metadata.PackageNotFoundError:
            return False
    return True


def main():
    if sys.version_info < (3, 11):
        print("Maintainability requires Python 3.11 or later.", file=sys.stderr)
        return 2
    environment = environment_path()
    python = environment_python(environment)
    if sys.argv[1:] == ["setup"]:
        # Re-running setup repairs interrupted installs without deleting other environments.
        venv.EnvBuilder(with_pip=True).create(environment)
        subprocess.run([str(python), "-m", "pip", "install", "-r", str(REQUIREMENTS)], check=True)
        print(f"Environment: {environment}")
        return 0
    if python.is_file() and Path(sys.prefix) != environment:
        os.execv(str(python), [str(python), str(ROOT / "scripts/measure_maintainability.py"), *sys.argv[1:]])
    if not pins_available() and not any(arg in ("-h", "--help") for arg in sys.argv[1:]):
        print("Pinned tools unavailable. Run: python3 scripts/measure_maintainability.py setup", file=sys.stderr)
        return 2
    runpy.run_path(str(ROOT / "tools/maintainability.py"), run_name="__main__")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, subprocess.CalledProcessError) as error:
        print(f"Maintainability environment error: {error}. Run the setup command in this environment.", file=sys.stderr)
        sys.exit(2)
