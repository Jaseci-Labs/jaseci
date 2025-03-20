"""Collect Python dependencies based on reference sourced from Jac.

This pass will use mypy to calculate the python package/module dependencies
that are only relevant to actual references source from Jac code.
"""

from __future__ import annotations

import os
import pathlib
import sys

import jaclang.compiler.absyntree as ast
from jaclang.compiler.passes import Pass
from jaclang.settings import settings

import mypy.nodes as MypyNodes  # noqa N812


class PyCollectDepsPass(Pass):
    """Python and bytecode file self.__debug_printing pass."""

    def __debug_print(self, msg: str) -> None:
        if settings.collect_py_dep_debug:
            self.log_info("CollectPythonDependencies::" + msg)

    def enter_node(self, node: ast.AstNode) -> None:
        """Collect python dependencies from all Jac Nodes."""
        assert isinstance(self.ir, ast.Module)

        if not isinstance(node, ast.AstSymbolNode):
            return

        # Adding the path of the file related to the py import
        path: str = ""
        if isinstance(node, ast.ModulePath):
            if node.path:
                path = ".".join([i.value for i in node.path])
            node.abs_path = self.ir.py_info.py_mod_dep_map.get(path)
            if node.abs_path and os.path.isfile(node.abs_path.replace(".pyi", ".py")):
                node.abs_path = node.abs_path.replace(".pyi", ".py")

        elif isinstance(node, ast.ModuleItem):
            imp = node.parent_of_type(ast.Import)
            mod_path_node = imp.get_all_sub_nodes(ast.ModulePath)[0]
            if mod_path_node.path:
                path = ".".join([i.value for i in mod_path_node.path])
            path += f".{node.name.value}"
            node.abs_path = self.ir.py_info.py_mod_dep_map.get(path)
            if node.abs_path and os.path.isfile(node.abs_path.replace(".pyi", ".py")):
                node.abs_path = node.abs_path.replace(".pyi", ".py")

        if isinstance(node, (ast.ModuleItem, ast.ModulePath)):
            mode_path = self.find_module_path(path, os.path.dirname(node.loc.mod_path))
            self.ir.py_info.py_raise_map[path] = mode_path

    def find_module_path(self, file_loc: str, base_path: str) -> str:
        """Find the path of the module."""
        # Search in directory of the current module
        module_path = os.path.join(base_path, *file_loc.split("."))  # noqa E501
        if os.path.exists(module_path + ".pyi"):
            return module_path + ".pyi"
        elif os.path.exists(module_path + ".py"):
            return module_path + ".py"
        package_path = os.path.join(module_path, "__init__.pyi")
        if os.path.exists(package_path):
            return package_path
        package_path = os.path.join(module_path, "__init__.py")
        if os.path.exists(package_path):
            return package_path

        # Search in mypy typeshed
        typeshed_path = str(
            pathlib.Path(os.path.dirname(__file__)).parent.parent.parent
            / "vendor"
            / "mypy"
            / "typeshed"
            / "stdlib"
        )
        module_path = os.path.join(typeshed_path, *file_loc.split("."))
        if os.path.exists(module_path + ".pyi"):
            return module_path + ".pyi"

        # Search in sys.path
        for path in sys.path:
            module_path = os.path.join(path, *file_loc.split("."))
            if os.path.exists(module_path + ".pyi"):
                return module_path + ".pyi"
            elif os.path.exists(module_path + ".py"):
                return module_path + ".py"
            package_path = os.path.join(module_path, "__init__.pyi")
            if os.path.exists(package_path):
                return package_path
            package_path = os.path.join(module_path, "__init__.py")
            if os.path.exists(package_path):
                return package_path

        return ""
