"""Static Import Pass."""
from os import path

import jaclang.jac.absyntree as ast
from jaclang.jac.ast_build import jac_file_to_ast
from jaclang.jac.passes.ir_pass import Pass
from jaclang.jac.passes.sub_node_tab_pass import SubNodeTabPass


class ImportPass(Pass):
    """Jac statically imports all modules."""

    def exit_module(self, node: ast.Module) -> None:
        """Run Importer."""
        run_again = True
        while run_again:
            run_again = False
            for i in self.get_all_sub_nodes(node, ast.Import, brute_force=True):
                if i.lang.value == "jac" and not i.sub_module:
                    run_again = True
                    i.kid.append(self.import_module(i, node.mod_path))
                    i.sub_module = i.kid[-1]
            SubNodeTabPass(mod_path=node.mod_path, input_ir=node)

    def import_module(self, node: ast.Import, mod_path: str) -> ast.AstNode:
        """Import a module."""
        target = path.normpath(
            path.join(path.dirname(mod_path), *(node.path.path_str.split("."))) + ".jac"
        )
        if not path.exists(target):
            raise FileNotFoundError(f"Could not find module {target}")
        return jac_file_to_ast(
            path.join(*(node.path.path_str.split("."))) + ".jac",
            base_dir=path.dirname(mod_path),
        )
