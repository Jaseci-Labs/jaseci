"""'Link the symbol tables across the modules."""

from typing import Optional

import jaclang.compiler.absyntree as ast
from jaclang.compiler.passes import Pass
from jaclang.compiler.passes.transform import Transform
from jaclang.compiler.symtable import InheritedSymbolTable


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
        assert node.parent and (
            isinstance(node.parent, ast.Import)
            or (node.parent.parent and isinstance(node.parent.parent, ast.Import))
        ), "Parent of ModulePath is not Import"
        imp_node = (
            node.parent if isinstance(node.parent, ast.Import) else node.parent.parent
        )
        all_import = False
        symbols_str_list: list[str] = []
        if isinstance(imp_node, ast.Import):
            if not imp_node.from_loc:
                all_import = True
            else:
                for mod_items in imp_node.items.items:
                    if isinstance(mod_items, ast.ModuleItem):
                        symbols_str_list.append(mod_items.name.value)
        if all_import:
            inher_tab = InheritedSymbolTable(
                base_symbol_table=imported_mod_symtab.sym_tab,
                load_all_symbols=True,
                symbols=[],
            )
        else:
            inher_tab = InheritedSymbolTable(
                base_symbol_table=imported_mod_symtab.sym_tab,
                load_all_symbols=False,
                symbols=symbols_str_list,
            )
        node.sym_tab.inherit.append(inher_tab)
