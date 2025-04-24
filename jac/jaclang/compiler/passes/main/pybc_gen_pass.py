"""Connect Decls and Defs in AST.

This pass creates and manages compilation of Python code from the AST. This pass
also creates bytecode files from the Python code, and manages the caching of
relevant files.
"""

import ast as ast3
import marshal


import jaclang.compiler.unitree as ast
from jaclang.compiler.passes import AstPass


class PyBytecodeGenPass(AstPass):
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
        mods = [node] + self.get_all_sub_nodes(node, ast.Module)
        for mod in mods:
            if not mod.gen.py_ast or not isinstance(node.gen.py_ast[0], ast3.Module):
                self.log_error(
                    f"Unable to find ast for module {node.loc.mod_path}.",
                    node,
                )
                continue
            root_node = mod.gen.py_ast[0]
            assert isinstance(root_node, ast3.Module)
            mod.gen.py_bytecode = marshal.dumps(
                compile(source=root_node, filename=mod.loc.mod_path, mode="exec")
            )
        self.terminate()
