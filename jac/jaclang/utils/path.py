"""Path resolution and language inference utilities."""

import os
import site
from typing import Optional


def _candidate_from(parts: list[str], base: str) -> Optional[str]:
    """Return candidate path for the given base and module parts."""
    candidate = os.path.join(base, *parts)
    # Package directory
    if os.path.isdir(candidate):
        for init_file in ["__init__.jac", "__init__.py"]:
            init_path = os.path.join(candidate, init_file)
            if os.path.isfile(init_path):
                return candidate
        return candidate
    # Module file
    if os.path.isfile(candidate + ".jac") or os.path.isfile(candidate + ".py"):
        return candidate
    return None


def resolve_module_path(target: str, base_path: str) -> str:
    """Resolve a module name to an absolute path."""
    parts = target.split(".")
    level = 0
    while level < len(parts) and parts[level] == "":
        level += 1
    actual_parts = parts[level:]
    traversal = max(level - 1, 0)

    # 1. Search site-packages
    for sp in site.getsitepackages():
        candidate = _candidate_from(actual_parts, sp)
        if candidate:
            return os.path.abspath(candidate)

    # 2. Relative to caller
    base_dir = base_path if os.path.isdir(base_path) else os.path.dirname(base_path)
    for _ in range(traversal):
        base_dir = os.path.dirname(base_dir)
    candidate = _candidate_from(actual_parts, base_dir)
    if candidate:
        return os.path.abspath(candidate)

    # 3. JACPATH search
    jacpath = os.getenv("JACPATH")
    if jacpath:
        candidate = _candidate_from(actual_parts, jacpath)
        if candidate:
            return os.path.abspath(candidate)
        target_files = [actual_parts[-1] + ".jac", actual_parts[-1] + ".py"]
        for root, _, files in os.walk(jacpath):
            for file in target_files:
                if file in files:
                    return os.path.abspath(os.path.join(root, file))

    return os.path.abspath(os.path.join(base_dir, *actual_parts))


def infer_language(target: str, base_path: str) -> str:
    """Infer whether the module is Jac or Python based on the file system."""
    path = resolve_module_path(target, base_path)
    if os.path.isdir(path):
        if os.path.isfile(os.path.join(path, "__init__.jac")):
            return "jac"
        if os.path.isfile(os.path.join(path, "__init__.py")):
            return "py"
    if path.endswith(".jac") or os.path.isfile(path + ".jac"):
        return "jac"
    if path.endswith(".py") or os.path.isfile(path + ".py"):
        return "py"
    return "py"

__all__ = ["resolve_module_path", "infer_language"]
