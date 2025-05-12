"""Python Dependency Collection Pass for the Jac compiler.

This pass identifies and collects Python dependencies referenced in Jac code by:

1. Analyzing references to Python modules, classes, and functions in Jac source code
2. Using mypy's dependency resolution to determine the actual Python files needed
3. Building a mapping between module names and their file paths
4. Filtering dependencies to include only those actually referenced from Jac
5. Handling both direct imports and nested module references
6. Supporting both .py and .pyi (type stub) files

This pass is crucial for the Python interoperability features of Jac, ensuring that
all necessary Python dependencies are available during compilation and runtime.
"""

from __future__ import annotations


import os

import jaclang.compiler.unitree as uni
from jaclang.compiler.passes import UniPass
from jaclang.settings import settings

import mypy.nodes as MypyNodes  # noqa N812


class PyCollectDepsPass(UniPass):
    """Python and bytecode file self.__debug_printing pass."""

    def __debug_print(self, msg: str) -> None:
        if settings.collect_py_dep_debug:
            self.log_info("CollectPythonDependencies::" + msg)

    def enter_node(self, node: uni.UniNode) -> None:
        """Collect python dependencies from all Jac Nodes."""
        if not isinstance(node, uni.AstSymbolNode):
            return

        # Adding the path of the file related to the py import
        path: str = ""
        if isinstance(node, uni.ModulePath):
            if node.path:
                path = ".".join([i.value for i in node.path.items])
            node.abs_path = self.ir_out.py_info.py_mod_dep_map.get(path)
            if node.abs_path and os.path.isfile(node.abs_path.replace(".pyi", ".py")):
                node.abs_path = node.abs_path.replace(".pyi", ".py")

        elif isinstance(node, uni.ModuleItem):
            imp = node.parent_of_type(uni.Import)
            mod_path_node = imp.get_all_sub_nodes(uni.ModulePath)[0]
            if mod_path_node.path:
                path = ".".join([i.value for i in mod_path_node.path.items])
            path += f".{node.name.value}"
            node.abs_path = self.ir_out.py_info.py_mod_dep_map.get(path)
            if node.abs_path and os.path.isfile(node.abs_path.replace(".pyi", ".py")):
                node.abs_path = node.abs_path.replace(".pyi", ".py")
