"""Static Import Pass.

This pass statically imports all modules used in import statements in the
current module. This pass is run before the def/decl pass to ensure that all
symbols are available for matching.
"""

import ast as py_ast
import importlib.util
import sys
from os import path
from typing import Optional


import jaclang.compiler.absyntree as ast
from jaclang.compiler.passes import Pass
from jaclang.compiler.passes.main import SubNodeTabPass
from jaclang.settings import settings
from jaclang.utils.helpers import import_target_to_relative_path


class ImportPass(Pass):
    """Jac statically imports all modules."""

    def before_pass(self) -> None:
        """Run once before pass."""
        self.import_table: dict[str, ast.Module] = {}

    def enter_module(self, node: ast.Module) -> None:
        """Run Importer."""
        self.cur_node = node
        self.annex_impl(node)
        self.terminate()  # Turns off auto traversal for deliberate traversal
        self.run_again = True
        while self.run_again:
            self.run_again = False
            all_imports = self.get_all_sub_nodes(node, ast.ModulePath)
            for i in all_imports:
                lang = i.parent_of_type(ast.Import).hint.tag.value
                if lang == "jac" and not i.sub_module:
                    self.run_again = True
                    mod = self.import_module(
                        node=i,
                        mod_path=node.loc.mod_path,
                    )
                    if not mod:
                        self.run_again = False
                        continue
                    self.annex_impl(mod)
                    i.sub_module = mod
                    i.add_kids_right([mod], pos_update=False)
                elif lang == "py" and settings.jac_proc_debug:
                    mod = self.import_py_module(node=i, mod_path=node.loc.mod_path)
                    i.sub_module = mod
                    i.add_kids_right([mod], pos_update=False)
                self.enter_module_path(i)
            SubNodeTabPass(prior=self, input_ir=node)
        self.annex_impl(node)
        node.mod_deps = self.import_table

    def annex_impl(self, node: ast.Module) -> None:
        """Annex impl and test modules."""
        if not node.loc.mod_path:
            self.error("Module has no path")
        if node.loc.mod_path.endswith(".jac") and path.exists(
            f"{node.loc.mod_path[:-4]}.impl.jac"
        ):
            mod = self.import_mod_from_file(f"{node.loc.mod_path[:-4]}.impl.jac")
            if mod:
                node.impl_mod = mod
                node.add_kids_left([mod], pos_update=False)
                mod.parent = node
        if node.loc.mod_path.endswith(".jac") and path.exists(
            f"{node.loc.mod_path[:-4]}.test.jac"
        ):
            mod = self.import_mod_from_file(f"{node.loc.mod_path[:-4]}.test.jac")
            if mod:
                node.test_mod = mod
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

    # Utility functions
    # -----------------

    def import_module(self, node: ast.ModulePath, mod_path: str) -> ast.Module | None:
        """Import a module."""
        self.cur_node = node  # impacts error reporting
        target = import_target_to_relative_path(
            node.level, node.path_str, path.dirname(node.loc.mod_path)
        )
        return self.import_mod_from_file(target)

    def import_mod_from_file(self, target: str) -> ast.Module | None:
        """Import a module from a file."""
        from jaclang.compiler.compile import jac_file_to_pass
        from jaclang.compiler.passes.main import SubNodeTabPass

        if not path.exists(target):
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

    def import_py_module(
        self, node: ast.ModulePath, mod_path: str
    ) -> Optional[ast.Module]:
        """Import a module."""
        from jaclang.compiler.passes.main import PyastBuildPass

        base_dir = path.dirname(mod_path)
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
            self.error(
                f"Failed to import python module {node.path_str}: {e}",
                node_override=node,
            )
            raise e
        return None
