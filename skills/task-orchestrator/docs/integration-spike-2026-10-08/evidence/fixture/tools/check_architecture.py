import ast
from pathlib import Path
module = ast.parse(Path("catalog.py").read_text())
assert not any(isinstance(n, (ast.Import, ast.ImportFrom)) for n in ast.walk(module)), "catalog must stay dependency-free"
print("Architecture gate passed")
