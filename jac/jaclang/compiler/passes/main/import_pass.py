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
from jaclang.compiler.passes.main import SubNodeTabPass, SymTabBuildPass
from jaclang.settings import settings
from jaclang.utils.log import logging


logger = logging.getLogger(__name__)


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
        self.run_again = True
        while self.run_again:
            self.run_again = False
            all_imports = self.get_all_sub_nodes(node, ast.ModulePath)
            for i in all_imports:
                self.process_import(i)
                self.enter_module_path(i)
            SubNodeTabPass(prior=self, input_ir=node)

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
        if mod:
            self.run_again = True
            node.sub_module = mod
            self.annex_impl(mod)
            node.add_kids_right([mod], pos_update=False)
            mod.parent = node

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
                    node.impl_mod.append(mod)
                    node.add_kids_left([mod], pos_update=False)
                    mod.parent = node
            if (
                cur_file.startswith(f"{base_path}.")
                or test_folder == os.path.dirname(cur_file)
            ) and cur_file.endswith(".test.jac"):
                mod = self.import_jac_mod_from_file(cur_file)
                if mod and not settings.ignore_test_annex:
                    node.test_mod.append(mod)
                    node.add_kids_right([mod], pos_update=False)
                    mod.parent = node

    def enter_module_path(self, node: ast.ModulePath) -> None:
        """Sub objects.

        path: Sequence[Token],
        alias: Optional[Name],
        sub_module: Optional[Module] = None,
        """
        if node.alias and node.sub_module:
            node.sub_module.name = node.alias.value
        # Items matched during def/decl pass

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
        from jaclang.compiler.compile import jac_file_to_pass
        from jaclang.compiler.passes.main import SubNodeTabPass

        if not os.path.exists(target):
            self.error(f"Could not find module {target}")
            return None
        if target in self.import_table:
            return self.import_table[target]
        try:
            mod_pass = jac_file_to_pass(file_path=target, target=SubNodeTabPass)
            self.errors_had += mod_pass.errors_had
            self.warnings_had += mod_pass.warnings_had
            mod = mod_pass.ir
        except Exception as e:
            logger.info(e)
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

    def before_pass(self) -> None:
        """Only run pass if settings are set to raise python."""
        super().before_pass()
        self.__load_builtins()

    def __get_current_module(self, node: ast.AstNode) -> str:
        parent = node.find_parent_of_type(ast.Module)
        mod_list = []
        while parent is not None:
            mod_list.append(parent)
            parent = parent.find_parent_of_type(ast.Module)
        mod_list.reverse()
        return ".".join(p.name for p in mod_list)

    def process_import(self, i: ast.ModulePath) -> None:
        """Process an import."""
        # Process import is orginally implemented to handle ModulePath in Jaclang
        # This won't work with py imports as this will fail to import stuff in form of
        #      from a import b
        #      from a import (c, d, e)
        # Solution to that is to get the import node and check the from loc then
        # handle it based on if there a from loc or not
        imp_node = i.parent_of_type(ast.Import)
        if imp_node.is_py and not i.sub_module:
            if imp_node.from_loc:
                for j in imp_node.items.items:
                    assert isinstance(j, ast.ModuleItem)
                    mod_path = f"{imp_node.from_loc.dot_path_str}.{j.name.sym_name}"
                    self.import_py_module(
                        parent_node=j,
                        mod_path=mod_path,
                        imported_mod_name=(
                            j.name.sym_name if not j.alias else j.alias.sym_name
                        ),
                    )
            else:
                for j in imp_node.items.items:
                    assert isinstance(j, ast.ModulePath)
                    self.import_py_module(
                        parent_node=j,
                        mod_path=j.dot_path_str,
                        imported_mod_name=(
                            j.dot_path_str.replace(".", "")
                            if not j.alias
                            else j.alias.sym_name
                        ),
                    )

    def import_py_module(
        self,
        parent_node: ast.ModulePath | ast.ModuleItem,
        imported_mod_name: str,
        mod_path: str,
    ) -> Optional[ast.Module]:
        """Import a module."""
        from jaclang.compiler.passes.main import PyastBuildPass

        assert isinstance(self.ir, ast.Module)

        python_raise_map = self.ir.py_raise_map
        file_to_raise = None

        if mod_path in python_raise_map:
            file_to_raise = python_raise_map[mod_path]
        else:
            resolved_mod_path = (
                f"{self.__get_current_module(parent_node)}.{imported_mod_name}"
            )
            assert isinstance(self.ir, ast.Module)
            resolved_mod_path = resolved_mod_path.replace(f"{self.ir.name}.", "")
            file_to_raise = python_raise_map.get(resolved_mod_path)

        if file_to_raise is None:
            return None

        try:
            if file_to_raise not in {None, "built-in", "frozen"}:
                if file_to_raise in self.import_table:
                    return self.import_table[file_to_raise]

                with open(file_to_raise, "r", encoding="utf-8") as f:
                    mod = PyastBuildPass(
                        input_ir=ast.PythonModuleAst(
                            py_ast.parse(f.read()), mod_path=file_to_raise
                        ),
                    ).ir
                    SubNodeTabPass(input_ir=mod, prior=self)
                if mod:
                    mod.name = imported_mod_name
                    self.import_table[file_to_raise] = mod
                    self.attach_mod_to_node(parent_node, mod)
                    SymTabBuildPass(input_ir=mod, prior=self)
                    return mod
                else:
                    raise self.ice(f"Failed to import python module {mod_path}")
        except Exception as e:
            self.error(f"Failed to import python module {mod_path}")
            raise e
        return None

    def __load_builtins(self) -> None:
        """Pyraise builtins to help with builtins auto complete."""
        from jaclang.compiler.passes.main import PyastBuildPass

        assert isinstance(self.ir, ast.Module)

        file_to_raise = str(
            pathlib.Path(os.path.dirname(__file__)).parent.parent.parent
            / "vendor"
            / "mypy"
            / "typeshed"
            / "stdlib"
            / "builtins.pyi"
        )
        with open(file_to_raise, "r", encoding="utf-8") as f:
            mod = PyastBuildPass(
                input_ir=ast.PythonModuleAst(
                    py_ast.parse(f.read()), mod_path=file_to_raise
                ),
            ).ir
            mod.parent = self.ir
            SubNodeTabPass(input_ir=mod, prior=self)
            SymTabBuildPass(input_ir=mod, prior=self)
            mod.parent = None

    def annex_impl(self, node: ast.Module) -> None:
        """Annex impl and test modules."""
        return None
