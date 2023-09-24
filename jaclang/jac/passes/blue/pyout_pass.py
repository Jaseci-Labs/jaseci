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
        base_path, file_name = os.path.split(node.mod_path)
        gen_path = os.path.join(base_path, Con.JAC_GEN_DIR)
        os.makedirs(gen_path, exist_ok=True)
        with open(os.path.join(gen_path, "__init__.py"), "w") as f:
            pass
        mods = [node] + self.get_all_sub_nodes(node, ast.Module)
        for mod in mods:
            self.gen_python(mod, base_path=base_path, gen_path=gen_path)
        self.terminate()

    def gen_python(self, node: ast.Module, base_path: str, gen_path: str) -> None:
        """Generate Python."""
        mod_dir, file_name = os.path.split(node.mod_path)
        mod_dir = mod_dir.replace(base_path, "").lstrip(os.sep)
        base_name, _ = os.path.splitext(file_name)
        file_name = f"{base_name}.py"
        out_dir = os.path.join(gen_path, mod_dir)
        out_path = os.path.join(out_dir, file_name)
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "__init__.py"), "w") as f:
            pass
        with open(out_path, "w") as f:
            f.write(node.meta["py_code"])