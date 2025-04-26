"""Pass used to add the inherited symbols for architypes."""

from __future__ import annotations

from typing import Optional

import jaclang.compiler.unitree as uni
from jaclang.compiler.passes import AstPass
from jaclang.compiler.unitree import Symbol, UniScopeNode
from jaclang.settings import settings


class InheritancePass(AstPass):
    """Add inherited abilities in the target symbol tables."""

    def __debug_print(self, msg: str) -> None:
        if settings.inherit_pass_debug:
            self.log_info("[PyImportPass] " + msg)

    def __lookup(self, name: str, sym_table: UniScopeNode) -> Optional[Symbol]:
        symbol = sym_table.lookup(name)
        if symbol is None:
            # Check if the needed symbol in builtins
            builtins_symtable = None
            for mod in self.prog.mod.hub.values():
                if mod.name == "builtins":
                    builtins_symtable = mod.sym_tab

            assert builtins_symtable is not None
            symbol = builtins_symtable.lookup(name)
        return symbol

    def enter_architype(self, node: uni.Architype) -> None:
        """Fill architype symbol tables with abilities from parent architypes."""
        if node.base_classes is None:
            return

        for item in node.base_classes.items:
            # The assumption is that the base class can only be a name node
            # or an atom trailer only.
            assert isinstance(item, (uni.Name, uni.AtomTrailer, uni.FuncCall))

            # In case of name node, then get the symbol table that contains
            # the current class and lookup for that name after that use the
            # symbol to get the symbol table of the base class
            if isinstance(item, uni.Name):
                assert node.sym_tab.parent_scope is not None
                base_class_symbol = self.__lookup(
                    item.sym_name, node.sym_tab.parent_scope
                )
                if base_class_symbol is None:
                    msg = "Missing symbol for base class "
                    msg += f"{uni.Module.get_href_path(item)}.{item.sym_name}"
                    msg += f" needed for {uni.Module.get_href_path(node)}"
                    self.__debug_print(msg)
                    continue
                base_class_symbol_table = base_class_symbol.fetch_sym_tab
                if (
                    base_class_symbol_table is None
                    and base_class_symbol.defn[0]
                    .parent_of_type(uni.Module)
                    .py_info.is_raised_from_py
                ):
                    msg = "Missing symbol table for python base class "
                    msg += f"{uni.Module.get_href_path(item)}.{item.sym_name}"
                    msg += f" needed for {uni.Module.get_href_path(node)}"
                    self.__debug_print(msg)
                    continue
                assert base_class_symbol_table is not None
                node.sym_tab.inherit_sym_tab(base_class_symbol_table)

            elif isinstance(item, uni.FuncCall):
                self.__debug_print(
                    "Base class depends on the type of a function call expression, this is not supported yet"
                )

            # In case of atom trailer, unwind it and use each name node to
            # as the code above to lookup for the base class
            elif isinstance(item, uni.AtomTrailer):
                current_sym_table = node.sym_tab.parent_scope
                not_found: bool = False
                assert current_sym_table is not None
                for name in item.as_attr_list:
                    sym = self.__lookup(name.sym_name, current_sym_table)
                    if sym is None:
                        msg = "Missing symbol for base class "
                        msg += f"{uni.Module.get_href_path(name)}.{name.sym_name}"
                        msg += f" needed for {uni.Module.get_href_path(node)}"
                        self.__debug_print(msg)
                        not_found = True
                        break
                    current_sym_table = sym.fetch_sym_tab

                    # In case of python nodes, the base class may not be
                    # raised so ignore these classes for now
                    # TODO Do we need to import these classes?
                    if (
                        sym.defn[0].parent_of_type(uni.Module).py_info.is_raised_from_py
                        and current_sym_table is None
                    ):
                        msg = "Missing symbol table for python base class "
                        msg += f"{uni.Module.get_href_path(name)}.{name.sym_name}"
                        msg += f" needed for {uni.Module.get_href_path(node)}"
                        self.__debug_print(msg)
                        not_found = True
                        break

                    if (
                        current_sym_table is None
                        and item.as_attr_list.index(name) < len(item.as_attr_list) - 1
                        and isinstance(
                            item.as_attr_list[item.as_attr_list.index(name) + 1],
                            uni.IndexSlice,
                        )
                    ):
                        msg = "Base class depends on the type of an "
                        msg += "Index slice expression, this is not supported yet"
                        self.__debug_print(msg)
                        not_found = True
                        break

                    assert current_sym_table is not None

                if not_found:
                    continue

                assert current_sym_table is not None
                node.sym_tab.inherit_sym_tab(current_sym_table)
