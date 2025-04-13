"""'Link the symbol tables across the modules."""

import os

import jaclang.compiler.absyntree as ast
from jaclang.compiler.passes import Pass
from jaclang.compiler.symtable import InheritedSymbolTable


class SymTabLinkPass(Pass):
    """Link the symbol table."""

    def enter_module_path(self, node: ast.ModulePath) -> None:
        """Link the symbol tables."""

        assert isinstance(self.ir, ast.Module)
        assert self.ir.jac_prog is not None

        imp_node = node.parent_of_type(ast.Import)
        if imp_node.is_py:
            return None

        rel_path = node.resolve_relative_path()
        if os.path.isdir(rel_path):
            rel_path = f"{rel_path}/__init__.jac"
        if rel_path not in self.ir.jac_prog.modules:
            self.ice()

        imported_mod_symtab = self.ir.jac_prog.modules[rel_path].sym_tab

        all_import = False
        symbols_str_list: list[str] = []
        if node.parent and isinstance(node.parent, ast.SubNodeList):
            all_import = True
        else:
            if node.parent and isinstance(node.parent, ast.Import):
                for mod_items in node.parent.items.items:
                    if isinstance(mod_items, ast.ModuleItem):
                        symbols_str_list.append(mod_items.name.value)

        # all import is set, need to add the imported symtable as a kid
        # to the current sym table
        if all_import:
            node.sym_tab.kid.append(imported_mod_symtab)
        else:
            if imported_mod_symtab not in [
                stab.base_symbol_table for stab in node.sym_tab.inherit
            ]:
                node.sym_tab.inherit.append(
                    InheritedSymbolTable(
                        base_symbol_table=imported_mod_symtab,
                        load_all_symbols=all_import,
                        symbols=symbols_str_list,
                    )
                )
            else:
                # if the imported symbol table is already in the kid list,
                # just add the symbols to it
                for sym_tab in node.sym_tab.kid:
                    if sym_tab == imported_mod_symtab:
                        for sym in symbols_str_list:
                            if sym not in sym_tab.tab.values():
                                sym_tab.tab[sym] = imported_mod_symtab.tab[sym]
                for symtb in node.sym_tab.inherit:
                    if symtb.base_symbol_table == imported_mod_symtab:
                        symtb.symbols.extend(symbols_str_list)
                        break
