"""'Link the symbol tables across the modules."""

from typing import Optional

import jaclang.compiler.absyntree as ast
from jaclang.compiler.passes import Pass
from jaclang.compiler.passes.transform import Transform


class SymTabLinkPass(Pass):
    """Link the symbol table."""

    def __init__(
        self,
        input_ir: ast.Module,
        all_mods: dict[str, ast.Module],
        prior: Optional[Pass] = None,
    ) -> None:
        """Initialize the pass."""
        self.ir = input_ir
        self.all_mods = all_mods
        self.term_signal = False
        self.prune_signal = False
        self.ir: ast.AstNode = input_ir
        self.time_taken = 0.0
        Transform.__init__(self, input_ir, prior)

    def enter_module_path(self, node: ast.ModulePath) -> None:
        """Link the symbol tables."""
        imported_mod_symtab = self.all_mods[node.resolve_relative_path()]
        node.sym_tab.inherit.append(imported_mod_symtab.sym_tab)
