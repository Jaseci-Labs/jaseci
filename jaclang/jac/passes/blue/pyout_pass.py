"""Connect Decls and Defs in AST."""
import os

import jaclang.jac.absyntree as ast
from jaclang.jac.constant import Constants as Con
from jaclang.jac.passes import Pass


class PyOutPass(Pass):
    """Decls and Def matching pass."""

    def before_pass(self) -> None:
        """Before pass."""
        return super().before_pass()

    def enter_module(self, node: ast.Module) -> None:
        """Sub objects.

        name: str,
        doc: Token,
        body: Optional['Elements'],
        mod_path: str,
        rel_mod_path: str,
        is_imported: bool,
        sym_tab: Optional[SymbolTable],
        """
        if (
            not os.path.exists(node.mod_path)
            or "py_code" not in node.meta
            or not node.meta["py_code"]
        ):
            return
        dir_name, file_name = os.path.split(node.mod_path)
        base_name, _ = os.path.splitext(file_name)
        file_name = f"{base_name}.py"
        os.makedirs(os.path.join(dir_name, Con.JAC_GEN_DIR), exist_ok=True)
        out_path = os.path.join(dir_name, Con.JAC_GEN_DIR, file_name)
        with open(out_path, "w") as f:
            f.write(node.meta["py_code"])
