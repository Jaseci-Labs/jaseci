"""'Link the symbol tables across the modules."""

import jaclang.compiler.absyntree as ast
from jaclang.compiler.passes import Pass
from jaclang.compiler.symtable import InheritedSymbolTable


class SymTabLinkPass(Pass):
    """Link the symbol table."""

    def enter_module_path(self, node: ast.ModulePath) -> None:
        """Link the symbol tables."""
        from jaclang.runtimelib.machine import JacMachine

        machine = JacMachine.get()
        imported_mod_symtab = machine.jac_program.modules[
            node.resolve_relative_path()
        ].sym_tab

        all_import = False
        symbols_str_list: list[str] = []
        if node.parent and isinstance(node.parent, ast.SubNodeList):
            all_import = True
        else:
            if node.parent and isinstance(node.parent, ast.Import):
                for mod_items in node.parent.items.items:
                    if isinstance(mod_items, ast.ModuleItem):
                        symbols_str_list.append(mod_items.name.value)
        inher_tab = InheritedSymbolTable(
            base_symbol_table=imported_mod_symtab,
            load_all_symbols=True,
            symbols=[] if all_import else symbols_str_list,
        )
        node.sym_tab.inherit.append(inher_tab)
