"""Pass used to add the inherited symbols for architypes."""

from __future__ import annotations

from typing import Optional

import jaclang.compiler.absyntree as ast
from jaclang.compiler.passes import Pass
from jaclang.compiler.symtable import Symbol, SymbolTable
from jaclang.settings import settings


class InheritancePass(Pass):
    """Add inherited abilities in the target symbol tables."""

    def __debug_print(self, msg: str) -> None:
        if settings.inherit_pass_debug:
            self.log_info("[PyImportPass] " + msg)

    def __lookup(self, name: str, sym_table: SymbolTable) -> Optional[Symbol]:
        symbol = sym_table.lookup(name)
        if symbol is None:
            # Check if the needed symbol in builtins
            builtins_symtable = self.ir.sym_tab.find_scope("builtins")
            assert builtins_symtable is not None
            symbol = builtins_symtable.lookup(name)
        return symbol

    def enter_architype(self, node: ast.Architype) -> None:
        """Fill architype symbol tables with abilities from parent architypes."""
        if node.base_classes is None:
            return

        for item in node.base_classes:
            # The assumption is that the base class can only be a name node
            # or an atom trailer only.
            assert isinstance(item, (ast.Name, ast.AtomTrailer))

            # In case of name node, then get the symbol table that contains
            # the current class and lookup for that name after that use the
            # symbol to get the symbol table of the base class
            if isinstance(item, ast.Name):
                assert node.sym_tab.parent is not None
                base_class_symbol = self.__lookup(item.sym_name, node.sym_tab.parent)
                if base_class_symbol is None:
                    msg = "Missing symbol for base class "
                    msg += f"{ast.Module.get_href_path(item)}.{item.sym_name}"
                    msg += f" needed for {ast.Module.get_href_path(node)}"
                    self.__debug_print(msg)
                    continue
                base_class_symbol_table = base_class_symbol.fetch_sym_tab
                if (
                    base_class_symbol_table is None
                    and base_class_symbol.defn[0]
                    .parent_of_type(ast.Module)
                    .py_info.is_raised_from_py
                ):
                    msg = "Missing symbol table for python base class "
                    msg += f"{ast.Module.get_href_path(item)}.{item.sym_name}"
                    msg += f" needed for {ast.Module.get_href_path(node)}"
                    self.__debug_print(msg)
                    continue
                assert base_class_symbol_table is not None
                node.sym_tab.inherit_sym_tab(base_class_symbol_table)

            # In case of atom trailer, unwind it and use each name node to
            # as the code above to lookup for the base class
            elif isinstance(item, ast.AtomTrailer):
                current_sym_table = node.sym_tab.parent
                not_found: bool = False
                assert current_sym_table is not None
                for name in item.as_attr_list:
                    sym = self.__lookup(name.sym_name, current_sym_table)
                    if sym is None:
                        msg = "Missing symbol for base class "
                        msg += f"{ast.Module.get_href_path(name)}.{name.sym_name}"
                        msg += f" needed for {ast.Module.get_href_path(node)}"
                        self.__debug_print(msg)
                        not_found = True
                        break
                    current_sym_table = sym.fetch_sym_tab

                    # In case of python nodes, the base class may not be
                    # raised so ignore these classes for now
                    # TODO Do we need to import these classes?
                    if (
                        sym.defn[0].parent_of_type(ast.Module).py_info.is_raised_from_py
                        and current_sym_table is None
                    ):
                        msg = "Missing symbol table for python base class "
                        msg += f"{ast.Module.get_href_path(name)}.{name.sym_name}"
                        msg += f" needed for {ast.Module.get_href_path(node)}"
                        self.__debug_print(msg)
                        not_found = True
                        break

                    assert current_sym_table is not None

                if not_found:
                    continue

                assert current_sym_table is not None
                node.sym_tab.inherit_sym_tab(current_sym_table)
