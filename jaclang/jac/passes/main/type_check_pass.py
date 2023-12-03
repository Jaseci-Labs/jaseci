"""Integrate mypy infrastructure into Jac.

This is used to call mypy type checking into Jac files by integrating
mypy apis into Jac and use jac py ast in it.
"""
import os
import pathlib
import sys
from typing import Callable, List, Optional


import jaclang.jac.absyntree as ast
import jaclang.jac.passes.utils.mypy_ast_build as myab
from jaclang.jac.passes import Pass


class JacTypeCheckPass(Pass):
    """Python and bytecode file printing pass."""

    message_cb: Optional[Callable[[str | None, List[str], bool], None]] = None

    def before_pass(self) -> None:
        """Before pass."""
        self.__path = (
            pathlib.Path(os.path.dirname(__file__)).parent.parent.parent
            / "vendor"
            / "mypy"
        )
        return super().before_pass()

    def enter_module(self, node: ast.Module) -> None:
        """Call mypy checks on module level only."""
        self.api(node, node.loc.mod_path)
        self.terminate()

    def default_message_cb(
        self, filename: str | None, new_messages: list[str], is_serious: bool
    ) -> None:
        """Mypy errors reporter."""
        for msg in new_messages:
            self.warning(msg)

    def api(self, node: ast.Module, mod_path: str) -> None:
        """Call mypy APIs to implement type checking in Jac."""
        # Creating mypy api obbjects
        options = myab.Options()
        errors = myab.Errors(options)
        fs_cache = myab.FileSystemCache()
        search_paths = myab.compute_search_paths([], options, str(self.__path))
        plugin, snapshot = myab.load_plugins(options, errors, sys.stdout, [])

        if self.message_cb is not None:
            message_cb = self.message_cb
        else:
            message_cb = self.default_message_cb

        manager = myab.BuildManager(
            data_dir=".",
            search_paths=search_paths,
            ignore_prefix=os.getcwd(),
            source_set=myab.BuildSourceSet([]),
            reports=None,
            options=options,
            version_id="1.8.0+dev",
            plugin=plugin,
            plugins_snapshot=snapshot,
            errors=errors,
            flush_errors=message_cb,
            fscache=fs_cache,
            stdout=sys.stdout,
            stderr=sys.stderr,
        )

        tree = myab.ASTConverter(
            options=options,
            is_stub=False,
            errors=errors,
            ignore_errors=False,
            strip_function_bodies=False,
        ).visit(node.gen.py_ast)

        st = myab.State(
            id="Jac Module",
            path="File:" + mod_path,
            source="",
            manager=manager,
            root_source=False,
            ast_override=tree,
        )

        graph = myab.load_graph(
            [
                myab.BuildSource(
                    path=str(self.__path / "typeshed" / "stdlib" / "builtins.pyi"),
                    module="builtins",
                )
            ],
            manager,
            old_graph={"JacTree": st},
        )
        myab.process_graph(graph, manager)

        myab.semantic_analysis_for_scc(graph, ["JacTree"], errors)
