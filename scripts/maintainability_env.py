"""Select or explicitly provision native dependencies; never share venv binaries."""

import argparse
import hashlib
import importlib.metadata
import os
from pathlib import Path
import platform
import runpy
import shlex
import subprocess
import sys
import venv


SCRIPTS = Path(__file__).resolve().parent
REQUIREMENTS = SCRIPTS / "maintainability-requirements.txt"


def environment_path(root=None):
    root = Path.cwd() if root is None else root
    pins = hashlib.sha256(REQUIREMENTS.read_bytes()).hexdigest()[:12]
    key = f"{platform.system()}-{platform.machine()}-{sys.implementation.name}-{platform.python_version()}-{pins}"
    return root / ".quality/envs" / key


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


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args, remaining = parser.parse_known_args(argv)
    root = args.root.resolve(strict=True)
    if sys.version_info < (3, 11):
        print("Maintainability requires Python 3.11 or later.", file=sys.stderr)
        return 2
    environment = environment_path(root)
    python = environment_python(environment)
    if remaining == ["setup"]:
        # Re-running setup repairs interrupted installs without deleting other environments.
        venv.EnvBuilder(with_pip=True).create(environment)
        subprocess.run([str(python), "-m", "pip", "install", "-r", str(REQUIREMENTS)], check=True)
        print(f"Environment: {environment}")
        return 0
    if python.is_file() and Path(sys.prefix) != environment:
        os.execv(str(python), [str(python), str(SCRIPTS / "measure_maintainability.py"), *argv])
    if not pins_available() and not any(arg in ("-h", "--help") for arg in argv):
        recipe = shlex.join([sys.executable, str(SCRIPTS / "measure_maintainability.py"),
                            "setup", "--root", str(root)])
        print(f"Pinned tools unavailable. Run: {recipe}", file=sys.stderr)
        return 2
    runpy.run_path(str(SCRIPTS / "maintainability.py"), run_name="__main__")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, subprocess.CalledProcessError) as error:
        print(f"Maintainability environment error: {error}. Run the setup command in this environment.", file=sys.stderr)
        sys.exit(2)
