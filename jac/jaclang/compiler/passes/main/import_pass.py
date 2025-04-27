"""Static Import Pass.

This pass statically imports all modules used in import statements in the
current module. This pass is run before the def/decl pass to ensure that all
symbols are available for matching.
"""

import ast as py_ast
import os
import pathlib
from typing import Optional


import jaclang.compiler.unitree as uni
from jaclang.compiler.passes import UniPass
from jaclang.compiler.passes.main import SymTabBuildPass
from jaclang.utils.log import logging


logger = logging.getLogger(__name__)


# TODO: This pass finds imports dependencies, parses them, and adds them to
# JacProgram's table, then table calls again if needed, should rename
class JacImportPass(UniPass):
    """Jac statically imports Jac modules."""

    def enter_module(self, node: uni.Module) -> None:
        """Run Importer."""
        self.cur_node = node
        self.terminate()  # Turns off auto traversal for deliberate traversal
        all_imports = self.get_all_sub_nodes(node, uni.ModulePath)
        for i in all_imports:
            self.process_import(i)

    def process_import(self, i: uni.ModulePath) -> None:
        """Process an import."""
        imp_node = i.parent_of_type(uni.Import)
        if imp_node.is_jac:
            self.import_jac_module(node=i)

    def import_jac_module(self, node: uni.ModulePath) -> None:
        """Import a module."""
        from jaclang.compiler.passes.main import CompilerMode as CMode

        self.cur_node = node  # impacts error reporting
        target = node.resolve_relative_path()
        # If the module is a package (dir)
        if os.path.isdir(target):
            self.load_mod(self.import_jac_mod_from_dir(target))
            import_node = node.parent_of_type(uni.Import)
            # And the import is a from import and I am the from module
            if node == import_node.from_loc:
                # Import all from items as modules or packages
                for i in import_node.items.items:
                    if isinstance(i, uni.ModuleItem):
                        from_mod_target = node.resolve_relative_path(i.name.value)
                        # If package
                        if os.path.isdir(from_mod_target):
                            self.load_mod(self.import_jac_mod_from_dir(from_mod_target))
                        # Else module
                        else:
                            if from_mod_target in self.prog.mod.hub:
                                return
                            self.load_mod(
                                self.prog.compile(
                                    file_path=from_mod_target, mode=CMode.PARSE
                                )
                            )
        else:
            if target in self.prog.mod.hub:
                return
            self.load_mod(self.prog.compile(file_path=target, mode=CMode.PARSE))

    def load_mod(self, mod: uni.Module | None) -> None:
        """Attach a module to a node."""
        if mod and mod.loc.mod_path not in self.prog.mod.hub:
            self.prog.mod.hub[mod.loc.mod_path] = mod
            self.prog.last_imported.append(mod)

    # TODO: Refactor this to a function for impl and function for test

    def import_jac_mod_from_dir(self, target: str) -> uni.Module:
        """Import a module from a directory."""
        from jaclang.compiler.passes.main import CompilerMode as CMode

        with_init = os.path.join(target, "__init__.jac")
        if os.path.exists(with_init):
            if with_init in self.prog.mod.hub:
                return self.prog.mod.hub[with_init]
            return self.prog.compile(file_path=with_init, mode=CMode.PARSE)
        else:
            return uni.Module.make_stub(
                inject_name=target.split(os.path.sep)[-1],
                inject_src=uni.Source("", target),
            )


class PyImportPass(JacImportPass):
    """Jac statically imports Python modules."""

    def enter_module(self, node: uni.Module) -> None:
        """Run Importer."""
        self.cur_node = node
        self.terminate()  # Turns off auto traversal for deliberate traversal
        all_imports = self.get_all_sub_nodes(node, uni.ModulePath)
        for i in all_imports:
            self.process_import(i)

    def before_pass(self) -> None:
        """Only run pass if settings are set to raise python."""
        self.import_from_build_list: list[tuple[uni.Import, uni.Module]] = []
        super().before_pass()
        self.__load_builtins()

    def after_pass(self) -> None:
        """Build symbol tables for import from nodes."""
        # self.__import_from_symbol_table_build()
        return super().after_pass()

    def process_import(self, i: uni.ModulePath) -> None:
        """Process an import."""
        # Process import is orginally implemented to handle ModulePath in Jaclang
        # This won't work with py imports as this will fail to import stuff in form of
        #      from a import b
        #      from a import (c, d, e)
        # Solution to that is to get the import node and check the from loc `then`
        # handle it based on if there a from loc or not
        imp_node = i.parent_of_type(uni.Import)

        if imp_node.is_py:
            if imp_node.from_loc:
                msg = "Processing import from node at href="
                msg += uni.Module.get_href_path(imp_node)
                msg += f' path="{imp_node.loc.mod_path}, {imp_node.loc}"'
                self.__process_import_from(imp_node)
            else:
                msg = "Processing import node at href="
                msg += uni.Module.get_href_path(imp_node)
                msg += f' path="{imp_node.loc.mod_path}, {imp_node.loc}"'
                self.__process_import(imp_node)

    def __process_import_from(self, imp_node: uni.Import) -> None:
        """Process imports in the form of `from X import I`."""
        assert isinstance(imp_node.from_loc, uni.ModulePath)

        # Attempt to import the Python module X and process it
        imported_mod = self.__import_py_module(
            parent_node_path=uni.Module.get_href_path(imp_node),
            mod_path=imp_node.from_loc.dot_path_str,
        )

        if imported_mod:
            # Cyclic imports will happen in case of import sys
            # sys stub file imports sys module which means that we need
            # to import sys stub file again in the sys stub file and so on
            # This can be detected by iterating over all the parents and make sure
            # that the parent is in another file than the imported module
            if self.__check_cyclic_imports(imp_node, imported_mod):
                return

            if imported_mod.name == "builtins":
                return

            msg = f"\tRegistering module:{imported_mod.name} to "
            msg += f"import_from handling with {imp_node.loc.mod_path}:{imp_node.loc}"

            self.load_mod(imported_mod)
            self.import_from_build_list.append((imp_node, imported_mod))
            SymTabBuildPass(ir_in=imported_mod, prog=self.prog)

    def __process_import(self, imp_node: uni.Import) -> None:
        """Process the imports in form of `import X`."""
        # Expected that each ImportStatement will import one item
        # In case of this assertion fired then we need to revisit this item
        assert len(imp_node.items.items) == 1
        imported_item = imp_node.items.items[0]
        assert isinstance(imported_item, uni.ModulePath)

        imported_mod = self.__import_py_module(
            parent_node_path=uni.Module.get_href_path(imported_item),
            mod_path=imported_item.dot_path_str,
            imported_mod_name=(
                # TODO: Check this replace
                imported_item.dot_path_str.replace(".", "")
                if not imported_item.alias
                else imported_item.alias.sym_name
            ),
        )
        if imported_mod:
            if (
                self.__check_cyclic_imports(imp_node, imported_mod)
                or imported_mod.name == "builtins"
            ):
                return
            self.load_mod(imported_mod)

            if imp_node.is_absorb:
                msg = f"\tRegistering module:{imported_mod.name} to "
                msg += f"import_from (import all) handling with {imp_node.loc.mod_path}:{imp_node.loc}"

                self.import_from_build_list.append((imp_node, imported_mod))
            SymTabBuildPass(ir_in=imported_mod, prog=self.prog)

    def __import_py_module(
        self,
        parent_node_path: str,
        mod_path: str,
        imported_mod_name: Optional[str] = None,
    ) -> Optional[uni.Module]:
        """Import a python module."""
        from jaclang.compiler.passes.main import PyastBuildPass

        python_raise_map = self.prog.py_raise_map
        file_to_raise: Optional[str] = None

        if mod_path in python_raise_map:
            file_to_raise = python_raise_map[mod_path]
        else:
            # TODO: Is it fine to use imported_mod_name or get it from mod_path?
            resolved_mod_path = f"{parent_node_path}.{mod_path}"
            resolved_mod_path = resolved_mod_path.replace("..", ".")
            resolved_mod_path = resolved_mod_path.replace(
                f"{list(self.prog.mod.hub.values())[0]}.", ""
            )
            file_to_raise = python_raise_map.get(resolved_mod_path)

        if file_to_raise is None:
            return None

        try:
            if file_to_raise in {None, "built-in", "frozen"}:
                return None

            with open(file_to_raise, "r", encoding="utf-8") as f:
                file_source = f.read()
                mod = PyastBuildPass(
                    ir_in=uni.PythonModuleAst(
                        py_ast.parse(file_source),
                        orig_src=uni.Source(file_source, file_to_raise),
                    ),
                    prog=self.prog,
                ).ir_out

            if mod:
                mod.name = imported_mod_name if imported_mod_name else mod.name
                if mod.name == "__init__":
                    # (thakee): This needs to be re-done after implementing path handling properly.
                    mod_name = mod.loc.mod_path.split(os.path.sep)[-2]
                    mod.name = mod_name
                    mod.nix_name = mod_name
                mod.py_info.is_raised_from_py = True
                return mod
            else:
                raise self.ice(f"\tFailed to import python module {mod_path}")

        except Exception as e:
            self.log_error(f"\tFailed to import python module {mod_path}")
            raise e

    def __load_builtins(self) -> None:
        """Pyraise builtins to help with builtins auto complete."""
        from jaclang.compiler.passes.main import PyastBuildPass

        file_to_raise = str(
            pathlib.Path(os.path.dirname(__file__)).parent.parent.parent
            / "vendor"
            / "mypy"
            / "typeshed"
            / "stdlib"
            / "builtins.pyi"
        )
        with open(file_to_raise, "r", encoding="utf-8") as f:
            file_source = f.read()
            mod = PyastBuildPass(
                ir_in=uni.PythonModuleAst(
                    py_ast.parse(file_source),
                    orig_src=uni.Source(file_source, file_to_raise),
                ),
                prog=self.prog,
            ).ir_out
            SymTabBuildPass(ir_in=mod, prog=self.prog)
            self.prog.mod.hub[file_to_raise] = mod
            mod.py_info.is_raised_from_py = True

    def annex_impl(self, node: uni.Module) -> None:
        """Annex impl and test modules."""
        return None

    def __handle_different_site_packages(self, mod_path: str) -> str:
        if "site-packages" in mod_path:
            mod_path = mod_path[mod_path.index("site-packages") :]
        return mod_path

    def __check_cyclic_imports(
        self, imp_node: uni.UniNode, imported_module: uni.Module
    ) -> bool:
        """Check cyclic imports that might happen."""
        # Example of cyclic imports is import os
        # In the os stub file it imports the real os module which will cause os
        # stub to be raised again and so on
        # Another example is numpy. numpy init file imports multidim array file
        # which imports again more items from numpy and so on.
        imp_node_file = self.__handle_different_site_packages(imp_node.loc.mod_path)
        imported_module_file = self.__handle_different_site_packages(
            imported_module.loc.mod_path
        )
        if imp_node_file == imported_module_file:
            return True

        parent: Optional[uni.UniNode] = imp_node.parent
        while parent is not None:
            parent_file = self.__handle_different_site_packages(parent.loc.mod_path)
            if parent_file == imported_module_file:
                return True
            else:
                parent = parent.find_parent_of_type(uni.Module)

        return False
