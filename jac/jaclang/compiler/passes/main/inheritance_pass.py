"""Pass used to add the inherited symbols for architypes."""

from __future__ import annotations

import jaclang.compiler.absyntree as ast
from jaclang.compiler.passes import Pass


class InheritancePass(Pass):
    """Add inherited abilities in the target symbol tables."""

    def enter_architype(self, node: ast.Architype) -> None:
        """Fill architype symbol tables with abilities from parent architypes."""
        if node.base_classes is None:
            return

        for item in node.base_classes.items:
            # The assumption is that the base class can only be a name node
            # or an atom trailer only.
            assert isinstance(item, (ast.Name, ast.AtomTrailer))

            # In case of name node, then get the symbol table that contains
            # the current class and lookup for that name after that use the
            # symbol to get the symbol table of the base class
            if isinstance(item, ast.Name):
                assert node.sym_tab.parent is not None
                base_class_symbol = node.sym_tab.parent.lookup(item.sym_name)
                if base_class_symbol is None:
                    continue
                base_class_symbol_table = base_class_symbol.fetch_sym_tab
                assert base_class_symbol_table is not None
                node.sym_tab.inherit_sym_tab(base_class_symbol_table)

            # In case of atom trailer, unwind it and use each name node to
            # as the code above to lookup for the base class
            elif isinstance(item, ast.AtomTrailer):
                current_sym_table = node.sym_tab.parent
                assert current_sym_table is not None
                for name in item.as_attr_list:
                    sym = current_sym_table.lookup(name.sym_name)
                    assert sym is not None
                    current_sym_table = sym.fetch_sym_tab
                    assert current_sym_table is not None

                    # In case of python nodes, the base class may not be
                    # raised so ignore these classes for now
                    # TODO Do we need to import these classes?
                    if (
                        sym.defn[0].parent_of_type(ast.Module).py_info.is_raised_from_py
                        and current_sym_table is None
                    ):
                        return
                node.sym_tab.inherit_sym_tab(current_sym_table)
