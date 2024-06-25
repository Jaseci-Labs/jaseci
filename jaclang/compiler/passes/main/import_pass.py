"""Static Import Pass.

This pass statically imports all modules used in import statements in the
current module. This pass is run before the def/decl pass to ensure that all
symbols are available for matching.
"""

import ast as py_ast
import importlib.util
import os
import sys
from typing import Optional


import jaclang.compiler.absyntree as ast
from jaclang.compiler.passes import Pass
from jaclang.compiler.passes.main import SubNodeTabPass
from jaclang.settings import settings
from jaclang.utils.helpers import import_target_to_relative_path, is_standard_lib_module


class JacImportPass(Pass):
    """Jac statically imports Jac modules."""

    def before_pass(self) -> None:
        """Run once before pass."""
        self.import_table: dict[str, ast.Module] = {}

    def enter_module(self, node: ast.Module) -> None:
        """Run Importer."""
        self.cur_node = node
        self.import_table[node.loc.mod_path] = node
        self.__annex_impl(node)
        self.terminate()  # Turns off auto traversal for deliberate traversal
        self.run_again = True
        while self.run_again:
            self.run_again = False
            all_imports = self.get_all_sub_nodes(node, ast.ModulePath)
            for i in all_imports:
                self.process_import(node, i)
                self.enter_module_path(i)
            SubNodeTabPass(prior=self, input_ir=node)
        node.mod_deps = self.import_table

    def process_import(self, node: ast.Module, i: ast.ModulePath) -> None:
        """Process an import."""
        lang = i.parent_of_type(ast.Import).hint.tag.value
        if lang == "jac" and not i.sub_module:
            self.import_jac_module(
                node=i,
                mod_path=node.loc.mod_path,
            )

    def attach_mod_to_node(
        self, node: ast.ModulePath | ast.ModuleItem, mod: ast.Module | None
    ) -> None:
        """Attach a module to a node."""
        if mod:
            self.run_again = True
            node.sub_module = mod
            self.__annex_impl(mod)
            node.add_kids_right([mod], pos_update=False)

    def __annex_impl(self, node: ast.Module) -> None:
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
                if mod:
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

    def import_jac_module(self, node: ast.ModulePath, mod_path: str) -> None:
        """Import a module."""
        self.cur_node = node  # impacts error reporting
        target = import_target_to_relative_path(
            level=node.level,
            target=node.path_str,
            base_path=os.path.dirname(node.loc.mod_path),
        )
        # If the module is a package (dir)
        if os.path.isdir(target):
            self.attach_mod_to_node(node, self.import_jac_mod_from_dir(target))
            import_node = node.parent_of_type(ast.Import)
            # And the import is a from import and I am the from module
            if node == import_node.from_loc:
                # Import all from items as modules or packages
                for i in import_node.items.items:
                    if isinstance(i, ast.ModuleItem):
                        from_mod_target = import_target_to_relative_path(
                            level=node.level,
                            target=node.path_str + "." + i.name.value,
                            base_path=os.path.dirname(node.loc.mod_path),
                        )
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
            print(e)
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
        if not settings.py_raise:
            self.terminate()
        else:
            return super().before_pass()

    def process_import(self, node: ast.Module, i: ast.ModulePath) -> None:
        """Process an import."""
        lang = i.parent_of_type(ast.Import).hint.tag.value
        if lang == "py" and not i.sub_module and not is_standard_lib_module(i.path_str):
            mod = self.import_py_module(node=i, mod_path=node.loc.mod_path)
            if mod:
                i.sub_module = mod
                i.add_kids_right([mod], pos_update=False)
                if settings.py_raise_deep:
                    self.run_again = True

    def import_py_module(
        self, node: ast.ModulePath, mod_path: str
    ) -> Optional[ast.Module]:
        """Import a module."""
        from jaclang.compiler.passes.main import PyastBuildPass

        base_dir = os.path.dirname(mod_path)
        sys.path.append(base_dir)
        try:
            # Dynamically import the module
            spec = importlib.util.find_spec(node.path_str)
            sys.path.remove(base_dir)
            if spec and spec.origin and spec.origin not in {None, "built-in", "frozen"}:
                if spec.origin in self.import_table:
                    return self.import_table[spec.origin]
                with open(spec.origin, "r", encoding="utf-8") as f:
                    # print(f"\nImporting python module {node.path_str}")
                    mod = PyastBuildPass(
                        input_ir=ast.PythonModuleAst(
                            py_ast.parse(f.read()), mod_path=spec.origin
                        ),
                    ).ir
                if mod:
                    self.import_table[spec.origin] = mod
                    return mod
                else:
                    raise self.ice(
                        f"Failed to import python module {node.path_str}: {spec.origin}"
                    )
        except Exception as e:
            if "Empty kid for Token ModulePath" in str(e) or "utf-8" in str(e):  # FIXME
                return None
            self.error(
                f"Failed to import python module {node.path_str}: {e}",
                node_override=node,
            )
            raise e
        return None
