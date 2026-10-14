def select_names(names, prefix=""):
    """Return names that start with prefix, preserving input order and duplicates."""
    return [name for name in names if name.startswith(prefix)]
