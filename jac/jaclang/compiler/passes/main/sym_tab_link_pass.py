"""'Link the symbol tables across the modules."""

import os

import jaclang.compiler.absyntree as ast
from jaclang.compiler.passes import Pass
from jaclang.compiler.symtable import InheritedSymbolTable, SymbolTable


class SymTabLinkPass(Pass):
    """Link the symbol table."""

    def before_pass(self) -> None:
        self.__inherited_symbols: dict[str, InheritedSymbolTable] = {}
        self.__kid_symtabs: dict[str, SymbolTable] = {}
        return super().before_pass()

    def enter_module_path(self, node: ast.ModulePath) -> None:
        """Link the symbol tables."""

        assert isinstance(self.ir, ast.Module)
        assert self.ir.jac_prog is not None

        imp_node = node.parent_of_type(ast.Import)
        if imp_node.is_py or imp_node.is_absorb:
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

        sym_tab_owner_path: str = imported_mod_symtab.owner.loc.mod_path

        # all import is set, need to add the imported symtable as a kid
        # to the current sym table
        if all_import:
            self.__kid_symtabs[sym_tab_owner_path] = imported_mod_symtab

        else:
            if sym_tab_owner_path not in self.__inherited_symbols:
                self.__inherited_symbols[sym_tab_owner_path] = InheritedSymbolTable(
                    base_symbol_table=imported_mod_symtab,
                    load_all_symbols=all_import,
                    symbols=symbols_str_list,
                )

            else:
                self.__inherited_symbols[sym_tab_owner_path].symbols.extend(
                    symbols_str_list
                )

    def after_pass(self) -> None:
        for k in self.__inherited_symbols:
            self.ir.sym_tab.inherit.append(self.__inherited_symbols[k])
        for k in self.__kid_symtabs:
            self.ir.sym_tab.kid.append(self.__kid_symtabs[k])
        return super().after_pass()
