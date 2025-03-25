"""'Link the symbol tables across the modules."""

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
        from jaclang.runtimelib.machine import JacMachine

        imp_node = node.parent_of_type(ast.Import)
        if imp_node.is_py:
            return None
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
                    symbols=[] if all_import else symbols_str_list,
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
