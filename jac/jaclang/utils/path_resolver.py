"""Path resolution utilities for the Jaclang project.

This module provides a centralized set of utilities for resolving paths,
module names, and import references throughout the Jaclang codebase.
"""

from __future__ import annotations

import os
import site
from os import getcwd, path
from typing import List, Optional, Tuple


class PathResolver:
    """Utilities for resolving paths and module names."""

    @staticmethod
    def resolve_relative_path(
        target: str,
        base_path: str,
        target_item: Optional[str] = None,
        jacpath: Optional[str] = None,
    ) -> str:
        """Convert an import target string into a relative file path.

        Args:
            target: The target module name (e.g. "module.submodule" or ".relative.module")
            base_path: The base path to resolve relative imports from
            target_item: Optional specific item within the target module
            jacpath: Optional JACPATH environment variable value

        Returns:
            The resolved file path
        """
        # Build the target module name
        full_target = target + (f".{target_item}" if target_item else "")
        site_packages = site.getsitepackages()[0]

        # Split the target into parts and determine how many levels to traverse
        parts = full_target.split(".")
        traversal_levels = 0

        # Count leading dots for relative imports
        if target.startswith("."):
            traversal_levels = 0
            chomp_target = target
            while chomp_target.startswith("."):
                traversal_levels += 1
                chomp_target = chomp_target[1:]

        # Adjust traversal_levels to be at least 0
        traversal_levels = max(traversal_levels - 1, 0)
        actual_parts = parts[traversal_levels:]

        def candidate_from(base: str) -> str:
            """Generate a candidate path from a base directory."""
            candidate = os.path.join(base, *actual_parts)
            candidate_jac = candidate + ".jac"
            return candidate_jac if os.path.exists(candidate_jac) else candidate

        # 1. Try resolving using the first site-packages directory
        candidate = candidate_from(site_packages)
        if os.path.exists(candidate):
            return candidate

        # 2. Adjust the base path by moving up for each traversal level
        caller_dir = base_path if path.isdir(base_path) else path.dirname(base_path)
        caller_dir = caller_dir if caller_dir else getcwd()

        for _ in range(traversal_levels):
            caller_dir = path.dirname(caller_dir)

        candidate = candidate_from(caller_dir)

        # 3. If candidate doesn't exist and JACPATH is provided, search recursively
        if not os.path.exists(candidate) and jacpath:
            jacpath_dirs = jacpath.split(":")
            for jacpath_dir in jacpath_dirs:
                jacpath_dir = jacpath_dir.strip()
                if not jacpath_dir:
                    continue

                jacpath_candidate = candidate_from(jacpath_dir)
                if os.path.exists(jacpath_candidate):
                    return jacpath_candidate

                # Try recursive search if it's a specific file
                if target_item:
                    target_filename = actual_parts[-1] + ".jac"
                    for root, _, files in os.walk(jacpath_dir):
                        if target_filename in files:
                            return os.path.join(root, target_filename)

        return candidate

    @staticmethod
    def get_module_name(file_path: str, base_dir: Optional[str] = None) -> str:
        """Generate a proper module name from a file path.

        Args:
            file_path: The full path to the file
            base_dir: Optional base directory for relative path calculation

        Returns:
            The module name as a dot-separated string
        """
        full_path = os.path.abspath(file_path)

        # If the file is located within a site-packages directory, strip that prefix
        sp_index = full_path.find("site-packages")
        if sp_index != -1:
            # Remove the site-packages part and any leading separator
            rel = full_path[sp_index + len("site-packages") :]
            rel = rel.lstrip(os.sep)
        else:
            # Use the provided base_dir or the current directory
            base = base_dir or getcwd()
            rel = path.relpath(full_path, start=base)

        # Remove file extension and handle __init__ files
        rel = os.path.splitext(rel)[0]
        if os.path.basename(rel) == "__init__":
            rel = os.path.dirname(rel)

        # Convert path separators to dots for module name
        module_name = rel.replace(os.sep, ".").strip(".")
        return module_name

    @staticmethod
    def get_module_path(node_path: str, module_parts: List[str]) -> str:
        """Return the full path of a module.

        Args:
            node_path: The path of the node requesting the module
            module_parts: The parts of the module path

        Returns:
            The full module path as a dot-separated string
        """
        # Join the parts and return the full path
        return ".".join(module_parts)

    @staticmethod
    def get_caller_dir(target: str, base_path: str) -> str:
        """Get the directory of the caller for import resolution.

        Args:
            target: The target module name
            base_path: The base path to resolve from

        Returns:
            The resolved caller directory
        """
        caller_dir = base_path if path.isdir(base_path) else path.dirname(base_path)
        caller_dir = caller_dir if caller_dir else getcwd()

        # Handle relative imports by traversing up directories
        chomp_target = target
        if chomp_target.startswith("."):
            chomp_target = chomp_target[1:]
            while chomp_target.startswith("."):
                caller_dir = path.dirname(caller_dir)
                chomp_target = chomp_target[1:]

        # Extract directory path from the target
        dir_path = os.path.dirname(os.path.join(*(target.split("."))))
        return path.join(caller_dir, dir_path)

    @staticmethod
    def infer_language(file_path: str) -> str:
        """Infer the language of a file based on its extension.

        Args:
            file_path: The path to the file

        Returns:
            The language of the file ('jac' or 'py')
        """
        if file_path.endswith(".jac"):
            return "jac"
        elif file_path.endswith(".py"):
            return "py"

        # If the file doesn't have an extension, check if both .jac and .py versions exist
        if os.path.exists(file_path + ".jac"):
            return "jac"
        elif os.path.exists(file_path + ".py"):
            return "py"

        # If we can't determine the language, default to 'jac'
        return "jac"

    @staticmethod
    def get_file_with_extension(file_path: str) -> Tuple[str, str]:
        """Get the file path with the appropriate extension and the language.

        Args:
            file_path: The path to the file, with or without extension

        Returns:
            A tuple containing (file_path_with_extension, language)
        """
        # If the file already has an extension, return it with the inferred language
        if file_path.endswith(".jac") or file_path.endswith(".py"):
            return file_path, PathResolver.infer_language(file_path)

        # Check if .jac or .py versions exist
        if os.path.exists(file_path + ".jac"):
            return file_path + ".jac", "jac"
        elif os.path.exists(file_path + ".py"):
            return file_path + ".py", "py"

        # If neither exists, default to .jac
        return file_path + ".jac", "jac"
