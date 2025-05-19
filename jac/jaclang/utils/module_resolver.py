"""Module resolver utilities."""

from __future__ import annotations

import os
import site
from typing import Optional, Tuple


def _candidate_from(base: str, parts: list[str]) -> Optional[Tuple[str, str]]:
    candidate = os.path.join(base, *parts)
    if os.path.isdir(candidate):
        if os.path.isfile(os.path.join(candidate, "__init__.jac")):
            return os.path.join(candidate, "__init__.jac"), "jac"
        if os.path.isfile(os.path.join(candidate, "__init__.py")):
            return os.path.join(candidate, "__init__.py"), "py"
    if os.path.isfile(candidate + ".jac"):
        return candidate + ".jac", "jac"
    if os.path.isfile(candidate + ".py"):
        return candidate + ".py", "py"
    return None


def resolve_module(target: str, base_path: str) -> Tuple[str, str]:
    """Resolve module path and infer language."""
    parts = target.split(".")
    level = 0
    while level < len(parts) and parts[level] == "":
        level += 1
    actual_parts = parts[level:]

    for sp in site.getsitepackages():
        res = _candidate_from(sp, actual_parts)
        if res:
            return res

    base_dir = base_path if os.path.isdir(base_path) else os.path.dirname(base_path)
    for _ in range(max(level - 1, 0)):
        base_dir = os.path.dirname(base_dir)
    res = _candidate_from(base_dir, actual_parts)
    if res:
        return res

    jacpath = os.getenv("JACPATH")
    if jacpath:
        res = _candidate_from(jacpath, actual_parts)
        if res:
            return res
        target_jac = actual_parts[-1] + ".jac"
        target_py = actual_parts[-1] + ".py"
        for root, _, files in os.walk(jacpath):
            if target_jac in files:
                return os.path.join(root, target_jac), "jac"
            if target_py in files:
                return os.path.join(root, target_py), "py"

    return os.path.join(base_dir, *actual_parts), "py"


def infer_language(target: str, base_path: str) -> str:
    """Infer language for target relative to base path."""
    _, lang = resolve_module(target, base_path)
    return lang


def resolve_relative_path(target: str, base_path: str) -> str:
    """Resolve only the path component for a target."""
    path, _ = resolve_module(target, base_path)
    return path
