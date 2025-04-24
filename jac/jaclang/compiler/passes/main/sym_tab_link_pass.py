"""'Link the symbol tables across the modules."""

import os

import jaclang.compiler.unitree as ast
from jaclang.compiler.passes import AstPass
from jaclang.compiler.symtable import InheritedSymbolTable


class SymTabLinkPass(AstPass):
    """Link the symbol table."""

    def enter_module_path(self, node: ast.ModulePath) -> None:
        """Link the symbol tables."""
        imp_node = node.parent_of_type(ast.Import)

        if imp_node.is_jac:
            rel_path = node.resolve_relative_path()
            if os.path.isdir(rel_path):
                rel_path = f"{rel_path}/__init__.jac"
            if rel_path not in self.prog.mod.hub:
                self.log_error(
                    f"Module {rel_path} not found in the program. Something went wrong.",
                    node,
                )
                return
        else:
            if node.sym_name in self.prog.py_raise_map:
                rel_path = self.prog.py_raise_map[node.sym_name]
            elif (
                f"{self.ir_out.get_href_path(node)}.{node.sym_name}"
                in self.prog.py_raise_map
            ):
                rel_path = self.prog.py_raise_map[
                    f"{self.ir_out.get_href_path(node)}.{node.sym_name}"
                ]
            else:
                return

        imported_mod_symtab = self.prog.mod.hub[rel_path].sym_tab

        all_import = False
        symbols_str_list: list[str] = []
        if (
            imp_node.is_jac and node.parent and isinstance(node.parent, ast.SubNodeList)
        ) or (imp_node.is_py and imp_node.from_loc is None and not imp_node.is_absorb):
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
                # Check if the needed symbol will be inherited from the current symbol table
                # This will happen if you are doing `from . import X` check how path is imported in
                # os
                if node.sym_tab == imported_mod_symtab:
                    return

                node.sym_tab.inherit.append(
                    InheritedSymbolTable(
                        base_symbol_table=imported_mod_symtab,
                        # load_all_symbols will only be needed when doing from x imoport * in py imports
                        # is_absorb will set to true in case of jac include to py import *
                        load_all_symbols=imp_node.is_py and imp_node.is_absorb,
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
