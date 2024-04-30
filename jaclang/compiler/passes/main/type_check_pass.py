"""Integrate mypy infrastructure into Jac.

This is used to call mypy type checking into Jac files by integrating
mypy apis into Jac and use jac py ast in it.
"""

import os
import pathlib
import sys


import jaclang.compiler.absyntree as ast
import jaclang.compiler.passes.utils.mypy_ast_build as myab
from jaclang.compiler.passes import Pass


class JacTypeCheckPass(Pass):
    """Python and bytecode file printing pass."""

    def before_pass(self) -> None:
        """Before pass."""
        self.__path = (
            pathlib.Path(os.path.dirname(__file__)).parent.parent.parent
            / "vendor"
            / "mypy"
        )
        self.__modules: list[ast.Module] = []
        return super().before_pass()

    def enter_module(self, node: ast.Module) -> None:
        """Call mypy checks on module level only."""
        self.__modules.append(node)

    def after_pass(self) -> None:
        """Call mypy api after traversing all the modules."""
        try:
            self.api()
        except Exception as e:
            self.error(f"Unable to run type checking: {e}")
        return super().after_pass()

    def default_message_cb(
        self, filename: str | None, new_messages: list[str], is_serious: bool
    ) -> None:
        """Mypy errors reporter."""

    def api(self) -> None:
        """Call mypy APIs to implement type checking in Jac."""
        # Creating mypy api objects
        options = myab.myb.Options()
        errors = myab.Errors(self, options)
        fs_cache = myab.FileSystemCache()
        search_paths = myab.compute_search_paths([], options, str(self.__path))
        plugin, snapshot = myab.load_plugins(options, errors, sys.stdout, [])

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
            flush_errors=self.default_message_cb,
            fscache=fs_cache,
            stdout=sys.stdout,
            stderr=sys.stderr,
        )

        mypy_graph: myab.Graph = {}
        new_modules = []
        for module in self.__modules:
            tree = myab.ASTConverter(
                options=options,
                is_stub=False,
                errors=errors,
                strip_function_bodies=False,
                path=module.loc.mod_path,
            ).visit(module.gen.py_ast[0])

            st = myab.State(
                id=module.name,
                path="File:" + module.loc.mod_path,
                source="",
                manager=manager,
                root_source=False,
                ast_override=tree,
            )
            mypy_graph[module.name] = st
            new_modules.append(st)

        graph = myab.load_graph(
            [
                myab.BuildSource(
                    path=str(self.__path / "typeshed" / "stdlib" / "builtins.pyi"),
                    module="builtins",
                )
            ],
            manager,
            old_graph=mypy_graph,
            new_modules=new_modules,  # To parse the dependancies of modules
        )
        myab.process_graph(graph, manager)
