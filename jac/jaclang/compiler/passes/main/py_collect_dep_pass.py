"""Collect Python dependencies based on reference sourced from Jac.

This pass will use mypy to calculate the python package/module dependencies
that are only relevant to actual references source from Jac code.
"""

from __future__ import annotations


import builtins
import os
import pathlib
import sys

import jaclang.compiler.absyntree as ast
from jaclang.compiler.passes import Pass
from jaclang.settings import settings


class PyCollectDepsPass(Pass):
    """Python and bytecode file self.__debug_printing pass."""

    def __debug_print(self, msg: str) -> None:
        if settings.collect_py_dep_debug:
            self.log_info("CollectPythonDependencies::" + msg)

    def enter_node(self, node: ast.AstNode) -> None:
        """Collect python dependencies from all Jac Nodes."""
        assert isinstance(self.ir, ast.Module)

        path: str = ""
        if isinstance(node, ast.ModulePath):
            if node.path:
                path = ".".join([i.value for i in node.path])
            node.abs_path = self.ir.py_info.py_mod_dep_map.get(path)
            if node.abs_path and os.path.isfile(node.abs_path.replace(".pyi", ".py")):
                node.abs_path = node.abs_path.replace(".pyi", ".py")
            if mode_path := self.find_module_path(
                path, os.path.dirname(node.loc.mod_path)
            ):
                self.ir.py_info.py_raise_map[path] = mode_path

        elif isinstance(node, ast.ModuleItem):
            imp = node.parent_of_type(ast.Import)
            mod_path_node = imp.get_all_sub_nodes(ast.ModulePath)[0]
            if mod_path_node.path:
                path = ".".join([i.value for i in mod_path_node.path])
            path += f".{node.name.value}"
            node.abs_path = self.ir.py_info.py_mod_dep_map.get(path)
            if node.abs_path and os.path.isfile(node.abs_path.replace(".pyi", ".py")):
                node.abs_path = node.abs_path.replace(".pyi", ".py")
            if mode_path := self.find_module_path(
                path, os.path.dirname(node.loc.mod_path)
            ):
                self.ir.py_info.py_raise_map[path] = mode_path

        elif isinstance(node, ast.AtomTrailer):
            full_list = [
                i.value
                for i in node.as_attr_list
                if (isinstance(i, ast.Name) and not isinstance(i.parent, ast.SubTag))
            ]
            if full_list:
                full = ".".join(full_list)
                if "." in full:
                    full = full[: full.rindex(".")]
                if self.ir.py_info.py_raise_map.get(full):
                    return
                base_path = os.path.dirname(node.loc.mod_path)
                outpath = self.find_module_path(full, base_path)
                if outpath:
                    self.ir.py_info.py_raise_map[full] = outpath
        elif isinstance(node, ast.Name):
            if not isinstance(node.parent, ast.AtomTrailer):
                npath = self.find_module_path(
                    node.value, os.path.dirname(node.loc.mod_path)
                )
                if npath:
                    self.ir.py_info.py_raise_map[node.value] = npath
                # else:
                #     print(f"Error: {node.value} not found")
            elif isinstance(node.parent, ast.ArchRef):
                npath = self.find_module_path(
                    "jaclang", os.path.dirname(node.loc.mod_path)
                )
                if npath:
                    self.ir.py_info.py_raise_map["jaclang"] = npath
            if node.value in dir(builtins):
                npath = self.find_module_path(
                    "builtins", os.path.dirname(node.loc.mod_path)
                )
                if npath:
                    self.ir.py_info.py_raise_map["builtins"] = npath
            elif node.value == "isfile":
                npath = self.find_module_path(
                    "genericpath", os.path.dirname(node.loc.mod_path)
                )
                if npath:
                    self.ir.py_info.py_raise_map["genericpath"] = npath

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
        elif os.path.exists(module_path + ".py"):
            return module_path + ".py"
        package_path = os.path.join(module_path, "__init__.pyi")
        if os.path.exists(package_path):
            return package_path
        package_path = os.path.join(module_path, "__init__.py")
        if os.path.exists(package_path):
            return package_path

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
