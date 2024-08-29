"""Collect Python dependencies based on reference sourced from Jac.

This pass will use mypy to calculate the python package/module dependencies
that are only relevant to actual references source from Jac code.
"""

from __future__ import annotations


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

        if len(node.gen.mypy_ast) == 0:
            return

        mypy_node = node.gen.mypy_ast[0]

        if isinstance(mypy_node, MypyNodes.RefExpr) and mypy_node.node:
            node_full_name = mypy_node.node.fullname
            if "." in node_full_name:
                mod_name = node_full_name[: node_full_name.rindex(".")]
            else:
                mod_name = node_full_name

            if mod_name not in self.ir.py_mod_dep_map:
                self.__debug_print(
                    f"Can't find a python file associated with {type(node)}::{node.loc}"
                )
                return

            mode_path = self.ir.py_mod_dep_map[mod_name]
            if mode_path.endswith(".jac"):
                return

            self.ir.py_raise_map[mod_name] = mode_path
        else:
            self.__debug_print(
                f"Collect python dependencies is not supported in {type(node)}::{node.loc}"
            )
