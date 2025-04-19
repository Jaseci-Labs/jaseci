"""Static Import Pass.

This pass statically imports all modules used in import statements in the
current module. This pass is run before the def/decl pass to ensure that all
symbols are available for matching.
"""

import ast as py_ast
import os
import pathlib
from typing import Optional


import jaclang.compiler.absyntree as ast
from jaclang.compiler.passes import Pass
from jaclang.compiler.passes.main import DefUsePass, SubNodeTabPass, SymTabBuildPass
from jaclang.compiler.passes.main.sym_tab_build_pass import PyInspectSymTabBuildPass
from jaclang.settings import settings
from jaclang.utils.log import logging


logger = logging.getLogger(__name__)


# TODO: This pass finds imports dependencies, parses them, and adds them to
# JacProgram's table, then table calls again if needed, should rename
class JacImportPass(Pass):
    """Jac statically imports Jac modules."""

    def before_pass(self) -> None:
        """Run once before pass."""
        self.import_table: dict[str, ast.Module] = {}

    def enter_module(self, node: ast.Module) -> None:
        """Run Importer."""
        self.cur_node = node
        self.import_table[node.loc.mod_path] = node
        self.annex_impl(node)
        self.terminate()  # Turns off auto traversal for deliberate traversal
        all_imports = self.get_all_sub_nodes(node, ast.ModulePath)
        for i in all_imports:
            self.process_import(i)
        SubNodeTabPass(prior=self, ir_root=node)

        node.mod_deps.update(self.import_table)

    def process_import(self, i: ast.ModulePath) -> None:
        """Process an import."""
        imp_node = i.parent_of_type(ast.Import)
        if imp_node.is_jac and not i.sub_module:
            self.import_jac_module(node=i)

    def attach_mod_to_node(
        self, node: ast.ModulePath | ast.ModuleItem, mod: ast.Module | None
    ) -> None:
        """Attach a module to a node."""
        assert isinstance(self.ir, ast.Module)
        assert self.ir.jac_prog is not None

        if mod and mod.loc.mod_path not in self.ir.jac_prog.modules:
            self.ir.jac_prog.modules[mod.loc.mod_path] = mod
            self.ir.jac_prog.last_imported.append(mod)
            mod.jac_prog = self.ir.jac_prog
            # We should have only one py_raise_map in the program
            # TODO: Move py_raise_map to jac_program
            mod.py_info.py_raise_map = self.ir.py_info.py_raise_map

    # TODO: Refactor this to a function for impl and function for test
    def annex_impl(self, node: ast.Module) -> None:
        """Annex impl and test modules."""
        if node.stub_only:
            return
        if not node.loc.mod_path:
            self.error("Module has no path")
        if not node.loc.mod_path.endswith(".jac"):
            return
        base_path = node.loc.mod_path[:-4]
        directory = os.path.dirname(node.loc.mod_path)
        if not directory:
            directory = os.getcwd()
            base_path = os.path.join(directory, base_path)
        impl_folder = base_path + ".impl"
        test_folder = base_path + ".test"
        search_files = [
            os.path.join(directory, impl_file) for impl_file in os.listdir(directory)
        ]
        if os.path.exists(impl_folder):
            search_files += [
                os.path.join(impl_folder, impl_file)
                for impl_file in os.listdir(impl_folder)
            ]
        if os.path.exists(test_folder):
            search_files += [
                os.path.join(test_folder, test_file)
                for test_file in os.listdir(test_folder)
            ]
        for cur_file in search_files:
            if node.loc.mod_path.endswith(cur_file):
                continue
            if (
                cur_file.startswith(f"{base_path}.")
                or impl_folder == os.path.dirname(cur_file)
            ) and cur_file.endswith(".impl.jac"):
                mod = self.import_jac_mod_from_file(cur_file)
                if mod:
                    node.add_kids_left(mod.kid, parent_update=True, pos_update=False)
                    node.impl_mod.append(mod)
            if (
                cur_file.startswith(f"{base_path}.")
                or test_folder == os.path.dirname(cur_file)
            ) and cur_file.endswith(".test.jac"):
                mod = self.import_jac_mod_from_file(cur_file)
                if mod and not settings.ignore_test_annex:
                    node.test_mod.append(mod)
                    node.add_kids_right([mod], pos_update=False)
                    mod.parent = node

    def import_jac_module(self, node: ast.ModulePath) -> None:
        """Import a module."""
        self.cur_node = node  # impacts error reporting
        target = node.resolve_relative_path()
        # If the module is a package (dir)
        if os.path.isdir(target):
            self.attach_mod_to_node(node, self.import_jac_mod_from_dir(target))
            import_node = node.parent_of_type(ast.Import)
            # And the import is a from import and I am the from module
            if node == import_node.from_loc:
                # Import all from items as modules or packages
                for i in import_node.items.items:
                    if isinstance(i, ast.ModuleItem):
                        from_mod_target = node.resolve_relative_path(i.name.value)
                        # If package
                        if os.path.isdir(from_mod_target):
                            self.attach_mod_to_node(
                                i, self.import_jac_mod_from_dir(from_mod_target)
                            )
                        # Else module
                        else:
                            self.attach_mod_to_node(
                                i, self.import_jac_mod_from_file(from_mod_target)
                            )
        else:
            self.attach_mod_to_node(node, self.import_jac_mod_from_file(target))

    def import_jac_mod_from_dir(self, target: str) -> ast.Module | None:
        """Import a module from a directory."""
        with_init = os.path.join(target, "__init__.jac")
        if os.path.exists(with_init):
            return self.import_jac_mod_from_file(with_init)
        else:
            return ast.Module(
                name=target.split(os.path.sep)[-1],
                source=ast.JacSource("", mod_path=target),
                doc=None,
                body=[],
                terminals=[],
                is_imported=False,
                stub_only=True,
                kid=[ast.EmptyToken()],
            )

    def import_jac_mod_from_file(self, target: str) -> ast.Module | None:
        """Import a module from a file."""
        from jaclang.compiler.program import JacProgram

        if not os.path.exists(target):
            self.error(f"Could not find module {target}")
            return None
        if target in self.import_table:
            return self.import_table[target]
        try:
            mod_pass = JacProgram.jac_file_to_pass(file_path=target, schedule=[])
            self.errors_had += mod_pass.errors_had
            self.warnings_had += mod_pass.warnings_had
            mod = mod_pass.ir
        except Exception as e:
            logger.error(e)
            mod = None
        if isinstance(mod, ast.Module):
            self.import_table[target] = mod
            mod.is_imported = True
            mod.body = [x for x in mod.body if not isinstance(x, ast.AstImplOnlyNode)]
            return mod
        else:
            self.error(f"Module {target} is not a valid Jac module.")
            return None


class PyImportPass(JacImportPass):
    """Jac statically imports Python modules."""

    def enter_module(self, node: ast.Module) -> None:
        """Run Importer."""
        self.cur_node = node
        self.import_table[node.loc.mod_path] = node
        self.terminate()  # Turns off auto traversal for deliberate traversal
        all_imports = self.get_all_sub_nodes(node, ast.ModulePath)
        for i in all_imports:
            self.process_import(i)
        SubNodeTabPass(prior=self, ir_root=node)

        node.mod_deps.update(self.import_table)

    def __debug_print(self, msg: str) -> None:
        if settings.py_import_pass_debug:
            self.log_info("[PyImportPass] " + msg)

    def before_pass(self) -> None:
        """Only run pass if settings are set to raise python."""
        self.import_from_build_list: list[tuple[ast.Import, ast.Module]] = []
        super().before_pass()
        self.__load_builtins()

    def after_pass(self) -> None:
        """Build symbol tables for import from nodes."""
        # self.__import_from_symbol_table_build()
        return super().after_pass()

    def process_import(self, i: ast.ModulePath) -> None:
        """Process an import."""
        # Process import is orginally implemented to handle ModulePath in Jaclang
        # This won't work with py imports as this will fail to import stuff in form of
        #      from a import b
        #      from a import (c, d, e)
        # Solution to that is to get the import node and check the from loc `then`
        # handle it based on if there a from loc or not
        imp_node = i.parent_of_type(ast.Import)

        if imp_node.is_py and not i.sub_module:
            if imp_node.from_loc:
                msg = "Processing import from node at href="
                msg += ast.Module.get_href_path(imp_node)
                msg += f' path="{imp_node.loc.mod_path}, {imp_node.loc}"'
                self.__debug_print(msg)
                self.__process_import_from(imp_node)
            else:
                msg = "Processing import node at href="
                msg += ast.Module.get_href_path(imp_node)
                msg += f' path="{imp_node.loc.mod_path}, {imp_node.loc}"'
                self.__debug_print(msg)
                self.__process_import(imp_node)

    def __process_import_from(self, imp_node: ast.Import) -> None:
        """Process imports in the form of `from X import I`."""
        assert isinstance(self.ir, ast.Module)
        assert isinstance(imp_node.from_loc, ast.ModulePath)

        self.__debug_print(f"\tTrying to import {imp_node.from_loc.dot_path_str}")
        # Attempt to import the Python module X and process it
        imported_mod = self.__import_py_module(
            parent_node_path=ast.Module.get_href_path(imp_node),
            mod_path=imp_node.from_loc.dot_path_str,
        )

        if imported_mod:
            # Cyclic imports will happen in case of import sys
            # sys stub file imports sys module which means that we need
            # to import sys stub file again in the sys stub file and so on
            # This can be detected by iterating over all the parents and make sure
            # that the parent is in another file than the imported module
            if self.__check_cyclic_imports(imp_node, imported_mod):
                self.__debug_print(
                    f"\tCycled imports is found at {imp_node.loc.mod_path} {imp_node.loc}"
                )
                return

            if imported_mod.name == "builtins":
                self.__debug_print(
                    f"\tIgnoring attaching builtins {imp_node.loc.mod_path} {imp_node.loc}"
                )
                return

            self.__debug_print(
                f"\tAttaching {imported_mod.name} into {ast.Module.get_href_path(imp_node)}"
            )
            msg = f"\tRegistering module:{imported_mod.name} to "
            msg += f"import_from handling with {imp_node.loc.mod_path}:{imp_node.loc}"
            self.__debug_print(msg)

            self.attach_mod_to_node(imp_node.from_loc, imported_mod)
            self.import_from_build_list.append((imp_node, imported_mod))
            if imported_mod._sym_tab is None:
                self.__debug_print(
                    f"\tBuilding symbol table for module:{ast.Module.get_href_path(imported_mod)}"
                )
            else:
                self.__debug_print(
                    f"\tRefreshing symbol table for module:{ast.Module.get_href_path(imported_mod)}"
                )
            PyInspectSymTabBuildPass(ir_root=imported_mod, prior=self)
            DefUsePass(ir_root=imported_mod, prior=self)

    def __process_import(self, imp_node: ast.Import) -> None:
        """Process the imports in form of `import X`."""
        # Expected that each ImportStatement will import one item
        # In case of this assertion fired then we need to revisit this item
        assert len(imp_node.items.items) == 1
        imported_item = imp_node.items.items[0]
        assert isinstance(imported_item, ast.ModulePath)

        self.__debug_print(f"\tTrying to import {imported_item.dot_path_str}")
        imported_mod = self.__import_py_module(
            parent_node_path=ast.Module.get_href_path(imported_item),
            mod_path=imported_item.dot_path_str,
            imported_mod_name=(
                # TODO: Check this replace
                imported_item.dot_path_str.replace(".", "")
                if not imported_item.alias
                else imported_item.alias.sym_name
            ),
        )
        if imported_mod:
            if self.__check_cyclic_imports(imp_node, imported_mod):
                self.__debug_print(
                    f"\tCycled imports is found at {imp_node.loc.mod_path} {imp_node.loc}"
                )
                return
            elif imported_mod.name == "builtins":
                self.__debug_print(
                    f"\tIgnoring attaching builtins {imp_node.loc.mod_path} {imp_node.loc}"
                )
                return

            self.__debug_print(
                f"\tAttaching {imported_mod.name} into {ast.Module.get_href_path(imp_node)}"
            )
            self.attach_mod_to_node(imported_item, imported_mod)

            if imp_node.is_absorb:
                msg = f"\tRegistering module:{imported_mod.name} to "
                msg += f"import_from (import all) handling with {imp_node.loc.mod_path}:{imp_node.loc}"
                self.__debug_print(msg)

                self.import_from_build_list.append((imp_node, imported_mod))
                if imported_mod._sym_tab is None:
                    self.__debug_print(
                        f"\tBuilding symbol table for module:{ast.Module.get_href_path(imported_mod)}"
                    )
                else:
                    self.__debug_print(
                        f"\tRefreshing symbol table for module:{ast.Module.get_href_path(imported_mod)}"
                    )
                PyInspectSymTabBuildPass(ir_root=imported_mod, prior=self)
                DefUsePass(ir_root=imported_mod, prior=self)

            else:
                self.__debug_print(
                    f"\tBuilding symbol table for module:{ast.Module.get_href_path(imported_mod)}"
                )
                SymTabBuildPass(ir_root=imported_mod, prior=self)

    def __import_py_module(
        self,
        parent_node_path: str,
        mod_path: str,
        imported_mod_name: Optional[str] = None,
    ) -> Optional[ast.Module]:
        """Import a python module."""
        from jaclang.compiler.passes.main import PyastBuildPass

        assert isinstance(self.ir, ast.Module)
        assert self.ir.jac_prog is not None

        python_raise_map = self.ir.py_info.py_raise_map
        file_to_raise: Optional[str] = None

        if mod_path in python_raise_map:
            file_to_raise = python_raise_map[mod_path]
        else:
            # TODO: Is it fine to use imported_mod_name or get it from mod_path?
            resolved_mod_path = f"{parent_node_path}.{mod_path}"
            resolved_mod_path = resolved_mod_path.replace("..", ".")
            resolved_mod_path = resolved_mod_path.replace(
                f"{list(self.ir.jac_prog.modules.values())[0]}.", ""
            )
            file_to_raise = python_raise_map.get(resolved_mod_path)

        if file_to_raise is None:
            self.__debug_print("\tNo file is found to do the import")
            return None

        self.__debug_print(f"\tFile used to do the import is {file_to_raise}")

        try:
            if file_to_raise in {None, "built-in", "frozen"}:
                return None

            if file_to_raise in self.import_table:
                self.__debug_print(
                    f"\t{file_to_raise} was raised before, getting it from cache"
                )
                return self.import_table[file_to_raise]

            with open(file_to_raise, "r", encoding="utf-8") as f:
                file_source = f.read()
                mod = PyastBuildPass(
                    root_ir=ast.PythonModuleAst(
                        py_ast.parse(file_source),
                        orig_src=ast.JacSource(file_source, file_to_raise),
                    ),
                ).ir
                SubNodeTabPass(ir_root=mod, prior=self)

            if mod:
                mod.name = imported_mod_name if imported_mod_name else mod.name
                if mod.name == "__init__":
                    # (thakee): This needs to be re-done after implementing path handling properly.
                    mod_name = mod.loc.mod_path.split(os.path.sep)[-2]
                    self.__debug_print(
                        f"\tRaised the __init__ file and rename the mod to be {mod_name}"
                    )
                    mod.name = mod_name
                self.import_table[file_to_raise] = mod
                mod.py_info.is_raised_from_py = True
                self.__debug_print(
                    f"\t{file_to_raise} is raised, adding it to the cache"
                )
                return mod
            else:
                raise self.ice(f"\tFailed to import python module {mod_path}")

        except Exception as e:
            self.error(f"\tFailed to import python module {mod_path}")
            raise e

    def __load_builtins(self) -> None:
        """Pyraise builtins to help with builtins auto complete."""
        from jaclang.compiler.passes.main import PyastBuildPass

        assert isinstance(self.ir, ast.Module)
        assert self.ir.jac_prog is not None

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
                root_ir=ast.PythonModuleAst(
                    py_ast.parse(file_source),
                    orig_src=ast.JacSource(file_source, file_to_raise),
                ),
            ).ir
            SubNodeTabPass(ir_root=mod, prior=self)
            SymTabBuildPass(ir_root=mod, prior=self)
            self.ir.jac_prog.modules[file_to_raise] = mod
            mod.jac_prog = self.ir.jac_prog
            mod.py_info.is_raised_from_py = True
            mod.py_info.py_raise_map = self.ir.py_info.py_raise_map

    def annex_impl(self, node: ast.Module) -> None:
        """Annex impl and test modules."""
        return None

    def __handle_different_site_packages(self, mod_path: str) -> str:
        if "site-packages" in mod_path:
            mod_path = mod_path[mod_path.index("site-packages") :]
        return mod_path

    def __check_cyclic_imports(
        self, imp_node: ast.AstNode, imported_module: ast.Module
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

        parent: Optional[ast.AstNode] = imp_node.parent
        while parent is not None:
            parent_file = self.__handle_different_site_packages(parent.loc.mod_path)
            if parent_file == imported_module_file:
                return True
            else:
                parent = parent.find_parent_of_type(ast.Module)

        return False
