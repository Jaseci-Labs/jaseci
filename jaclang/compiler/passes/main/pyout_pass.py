"""Connect Decls and Defs in AST.

This pass creates and manages compilation of Python code from the AST. This pass
also creates bytecode files from the Python code, and manages the caching of
relevant files.
"""

import ast as ast3
import os


import jaclang.compiler.absyntree as ast
from jaclang.compiler.constant import Constants as Con
from jaclang.compiler.passes import Pass


class PyOutPass(Pass):
    """Python and bytecode file printing pass."""

    def before_pass(self) -> None:
        """Before pass."""
        return super().before_pass()

    def enter_module(self, node: ast.Module) -> None:
        """Sub objects.

        name: str,
        doc: Token,
        body: Optional['Elements'],
        mod_path: str,
        is_imported: bool,
        sym_tab: Optional[SymbolTable],
        """
        if not (os.path.exists(node.loc.mod_path) and node.gen.py_ast):
            self.error(
                f"Unable to find module {node.loc.mod_path} or no code present.", node
            )
            return
        mods = [node] + self.get_all_sub_nodes(node, ast.Module)
        for mod in mods:
            mod_path, out_path_py, out_path_pyc = self.get_output_targets(mod)
            if os.path.exists(out_path_pyc) and os.path.getmtime(
                out_path_pyc
            ) > os.path.getmtime(mod_path):
                continue
            self.gen_python(mod, out_path=out_path_py)
            self.dump_bytecode(mod, mod_path=mod_path, out_path=out_path_pyc)
        self.terminate()

    def gen_python(self, node: ast.Module, out_path: str) -> None:
        """Generate Python."""
        try:
            with open(out_path, "w") as f:
                f.write(node.gen.py)
        except Exception as e:
            print(ast3.dump(node.gen.py_ast[0], indent=2))
            raise e

    def dump_bytecode(self, node: ast.Module, mod_path: str, out_path: str) -> None:
        """Generate Python."""
        if node.gen.py_bytecode:
            with open(out_path, "wb") as f:
                f.write(node.gen.py_bytecode)
        else:
            self.error(
                f"Soemthing went wrong with {node.loc.mod_path} compilation.", node
            )

    def get_output_targets(self, node: ast.Module) -> tuple[str, str, str]:
        """Get output targets."""
        base_path, file_name = os.path.split(node.loc.mod_path)
        gen_path = os.path.join(base_path, Con.JAC_GEN_DIR)
        os.makedirs(gen_path, exist_ok=True)
        with open(os.path.join(gen_path, "__init__.py"), "w"):
            pass
        mod_dir, file_name = os.path.split(node.loc.mod_path)
        mod_dir = mod_dir.replace(base_path, "").lstrip(os.sep)
        base_name, _ = os.path.splitext(file_name)
        out_dir = os.path.join(gen_path, mod_dir)
        os.makedirs(out_dir, exist_ok=True)
        out_path_py = os.path.join(out_dir, f"{base_name}.py")
        out_path_pyc = os.path.join(out_dir, f"{base_name}.jbc")
        return node.loc.mod_path, out_path_py, out_path_pyc
