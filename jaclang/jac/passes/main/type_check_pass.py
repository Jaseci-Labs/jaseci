"""Integrate mypy infrastructure into Jac.

This is used to call mypy type checking into Jac files by integrating
mypy apis into Jac and use jac py ast in it.
"""
import os
import pathlib
import sys
from typing import Callable, List


import jaclang.jac.absyntree as ast
from jaclang.jac.passes import Pass
from jaclang.vendor.mypy.build import BuildManager as MyPyBuildManager
from jaclang.vendor.mypy.build import BuildSource as MyPyBuildSource
from jaclang.vendor.mypy.build import BuildSourceSet as MyPyBuildSourceSet
from jaclang.vendor.mypy.build import FileSystemCache as MyPyFileSystemCache
from jaclang.vendor.mypy.build import State as MyPyState
from jaclang.vendor.mypy.build import compute_search_paths as mypy_compute_search_paths
from jaclang.vendor.mypy.build import load_graph as mypy_load_graph
from jaclang.vendor.mypy.build import load_plugins as mypy_load_plugins
from jaclang.vendor.mypy.build import process_graph as mypy_process_graph
from jaclang.vendor.mypy.errors import Errors as MyPyErrors
from jaclang.vendor.mypy.fastparse import ASTConverter as MyPyASTConverter
from jaclang.vendor.mypy.options import Options as MyPyOptions
from jaclang.vendor.mypy.semanal_main import (
    semantic_analysis_for_scc as mypy_sematic_analysis,
)


class JacTypeCheckPass(Pass):
    """Python and bytecode file printing pass."""

    mypy_message_cb: Callable[[str | None, List[str], bool], None]

    def before_pass(self) -> None:
        """Before pass."""
        self.__mypy_path = (
            pathlib.Path(os.path.dirname(__file__)).parent.parent.parent
            / "vendor"
            / "mypy"
        )
        return super().before_pass()

    def enter_module(self, node: ast.Module) -> None:
        """Call mypy checks on module level only."""
        jac_file_path = node.loc.mod_path
        if "corelib.jac" not in jac_file_path and "cli.jac" not in jac_file_path:
            self.mypy_api(node, node.loc.mod_path)
        self.terminate()

    def default_mypy_message_cb(
        self, filename: str | None, new_messages: list[str], is_serious: bool
    ) -> None:
        """Mypy errors reporter."""
        for msg in new_messages:
            print("Jac Checker:", msg)

    def mypy_api(self, node: ast.Module, mod_path: str) -> None:
        """Call mypy APIs to implement type checking in Jac."""
        # Creating mypy api obbjects
        mypy_options = MyPyOptions()
        mypy_errors = MyPyErrors(mypy_options)
        fs_cache = MyPyFileSystemCache()
        search_paths = mypy_compute_search_paths(
            [], mypy_options, str(self.__mypy_path)
        )
        plugin, snapshot = mypy_load_plugins(mypy_options, mypy_errors, sys.stdout, [])

        if self.mypy_message_cb is not None:
            mypy_message_cb = self.mypy_message_cb
        else:
            mypy_message_cb = self.default_mypy_message_cb

        manager = MyPyBuildManager(
            data_dir=".",
            search_paths=search_paths,
            ignore_prefix=os.getcwd(),
            source_set=MyPyBuildSourceSet([]),
            reports=None,
            options=mypy_options,
            version_id="1.8.0+dev",
            plugin=plugin,
            plugins_snapshot=snapshot,
            errors=mypy_errors,
            flush_errors=mypy_message_cb,
            fscache=fs_cache,
            stdout=sys.stdout,
            stderr=sys.stderr,
        )

        mypy_tree = MyPyASTConverter(
            options=mypy_options,
            is_stub=False,
            errors=mypy_errors,
            ignore_errors=False,
            strip_function_bodies=False,
        ).visit(node.gen.py_ast)

        st = MyPyState(
            id="Jac Module",
            path="File:" + mod_path,
            source="",
            manager=manager,
            root_source=False,
            jac_tree=mypy_tree,
        )

        graph = mypy_load_graph(
            [
                MyPyBuildSource(
                    path=str(self.__mypy_path / "typeshed" / "stdlib" / "builtins.pyi"),
                    module="builtins",
                )
            ],
            manager,
            old_graph={"JacTree": st},
        )
        mypy_process_graph(graph, manager)

        mypy_sematic_analysis(graph, ["JacTree"], mypy_errors)
