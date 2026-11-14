"""Installation-bound component loading for CLI and file-based Python entry points.

No sys.path mutation. Each resolved scripts path has its own package/cache;
loading another installed copy never reuses this installation's rule owners.
"""

import hashlib
import importlib
import importlib.util
from pathlib import Path
import sys


def load_component(name: str):
    scripts_path = Path(__file__).resolve().parent
    package_name = "_task_orchestrator_" + hashlib.sha256(str(scripts_path).encode()).hexdigest()
    if package_name not in sys.modules:
        spec = importlib.util.spec_from_file_location(
            package_name, scripts_path / "__init__.py",
            submodule_search_locations=[str(scripts_path)],
        )
        assert spec is not None and spec.loader is not None
        package = importlib.util.module_from_spec(spec)
        sys.modules[package_name] = package
        spec.loader.exec_module(package)
    return importlib.import_module(f"{package_name}.{name}")
