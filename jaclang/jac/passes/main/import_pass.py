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


import jaclang.jac.absyntree as ast
from jaclang.jac.passes import Pass
from jaclang.jac.passes.main import SubNodeTabPass


class ImportPass(Pass):
    """Jac statically imports all modules."""

    def before_pass(self) -> None:
        """Run once before pass."""
        self.import_table: dict[str, ast.Module] = {}

    def enter_module(self, node: ast.Module) -> None:
        """Run Importer."""
        self.cur_node = node
        self.terminate()  # Turns off auto traversal for deliberate traversal
        self.run_again = True
        while self.run_again:
            self.run_again = False
            for i in self.get_all_sub_nodes(node, ast.Import):
                if i.lang.tag.value == "jac" and not i.sub_module:
                    self.run_again = True
                    mod = (
                        self.import_module(node=i, mod_path=node.loc.mod_path)
                        if i.lang.tag.value == "jac"
                        else self.import_py_module(node=i, mod_path=node.loc.mod_path)
                    )
                    if not mod:
                        self.run_again = False
                        continue
                    i.sub_module = mod
                    i.add_kids_right([mod], pos_update=False)
                # elif i.lang.tag.value == "py":
                #     self.import_py_module(node=i, mod_path=node.loc.mod_path)
                self.enter_import(i)
            SubNodeTabPass(prior=self, input_ir=node)
        node.mod_deps = self.import_table

    def enter_import(self, node: ast.Import) -> None:
        """Sub objects.

        lang: Name,
        path: ModulePath,
        alias: Optional[Name],
        items: Optional[ModuleItems], # Items matched during def/decl pass
        is_absorb: bool,
        self.sub_module = None
        """
        self.cur_node = node
        if node.path.alias and node.sub_module:
            node.sub_module.name = node.path.alias.value
        # Items matched during def/decl pass

    # Utility functions
    # -----------------

    def import_module(self, node: ast.Import, mod_path: str) -> ast.Module | None:
        """Import a module."""
        from jaclang.jac.transpiler import jac_file_to_pass
        from jaclang.jac.passes.main import SubNodeTabPass

        self.cur_node = node  # impacts error reporting
        base_dir = path.dirname(mod_path)
        target = path.normpath(
            path.join(base_dir, *(node.path.path_str.split("."))) + ".jac"
        )

        if target in self.import_table:
            return self.import_table[target]

        if not path.exists(target):
            self.error(f"Could not find module {target}", node_override=node)
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
            return mod
        else:
            self.error(
                f"Module {target} is not a valid Jac module.", node_override=node
            )
            return None

    def import_py_module(self, node: ast.Import, mod_path: str) -> Optional[ast.Module]:
        """Import a module."""
        from jaclang.jac.passes.main import PyastBuildPass

        base_dir = path.dirname(mod_path)
        sys.path.append(base_dir)

        try:
            # Dynamically import the module
            spec = importlib.util.find_spec(node.path.path_str)
            sys.path.remove(base_dir)
            if spec and spec.origin and spec.origin not in {None, "built-in", "frozen"}:
                if spec.origin in self.import_table:
                    return self.import_table[spec.origin]
                with open(spec.origin, "r", encoding="utf-8") as f:
                    mod = PyastBuildPass(
                        input_ir=ast.PythonModuleAst(
                            py_ast.parse(f.read()), mod_path=mod_path
                        ),
                    ).ir
                if mod:
                    self.import_table[spec.origin] = mod
                    return mod
                else:
                    raise self.ice(
                        f"Failed to import python module {node.path.path_str}: {spec.origin}"
                    )
        except Exception as e:
            self.error(
                f"Failed to import python module {node.path.path_str}: {e}",
                node_override=node,
            )
        return None
