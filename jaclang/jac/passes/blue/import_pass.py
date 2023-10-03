"""Static Import Pass."""
from os import path

import jaclang.jac.absyntree as ast
from jaclang.jac.passes import Pass
from jaclang.jac.passes.blue import SubNodeTabPass


class ImportPass(Pass):
    """Jac statically imports all modules."""

    def before_pass(self) -> None:
        """Run once before pass."""
        self.import_table = {}

    def enter_module(self, node: ast.Module) -> None:
        """Run Importer."""
        self.cur_node = node
        self.terminate()  # Turns off auto traversal for deliberate traversal
        self.run_again = True
        while self.run_again:
            self.run_again = False
            for i in self.get_all_sub_nodes(node, ast.Import):
                if i.lang.value == "jac" and not i.sub_module:
                    self.run_again = True
                    mod = self.import_module(i, node.mod_path)
                    if not mod:
                        self.run_again = False
                        continue
                    ast.append_node(i, mod)
                    i.sub_module = i.kid[-1]
                self.enter_import(i)
            SubNodeTabPass(prior=self, mod_path=node.mod_path, input_ir=node)
        node.meta["sub_import_tab"] = self.import_table

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
        if node.alias and node.sub_module:
            node.sub_module.name = node.alias.value
        # Items matched during def/decl pass

    # Utility functions
    # -----------------

    def import_module(self, node: ast.Import, mod_path: str) -> ast.AstNode | None:
        """Import a module."""
        from jaclang.jac.transpiler import jac_file_to_pass
        from jaclang.jac.passes.blue.ast_build_pass import AstBuildPass

        base_dir = path.dirname(mod_path)
        target = path.normpath(
            path.join(base_dir, *(node.path.path_str.split("."))) + ".jac"
        )

        if target in self.import_table:
            # self.warning(f"Circular import detected, module {target} already imported.")
            return self.import_table[target]

        if not path.exists(target):
            self.error(f"Could not find module {target}")
        try:
            mod_pass = jac_file_to_pass(
                file_path=target, base_dir=base_dir, target=AstBuildPass
            )
            mod = mod_pass.ir
        except Exception:
            mod = None
        if isinstance(mod, ast.Module):
            self.import_table[target] = mod
            mod.is_imported = True
        else:
            self.error(f"Module {target} is not a valid Jac module.")
        return mod
