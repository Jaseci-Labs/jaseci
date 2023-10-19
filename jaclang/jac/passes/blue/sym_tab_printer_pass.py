"""Jac Blue pass for drawing AST."""
from __future__ import annotations

from typing import List, Optional

import jaclang.jac.absyntree as ast
from jaclang.jac.passes import Pass


class SymbolTablePrinterPass(Pass):
    """Jac symbol table convertion to ascii tree."""

    class __SymbolTree:
        def __init__(
                self,
                node_name: str,
                parent: Optional[SymbolTablePrinterPass.__SymbolTree] = None,
                children: Optional[List[SymbolTablePrinterPass.__SymbolTree]] = None
        ) -> None:
            self.parent = parent
            self.kid = children if children is not None else []
            self.name = node_name

        @property
        def parent(self) -> Optional[SymbolTablePrinterPass.__SymbolTree]:
            return self.__parent

        @parent.setter
        def parent(self, parent_node: SymbolTablePrinterPass.__SymbolTree) -> None:
            if parent_node:
                self.__parent = parent_node
                parent_node.kid.append(self)

    SAVE_OUTPUT = False

    def before_pass(self) -> None:
        """Initialize pass."""
        self.__root = self.__build_symbol_tree(self.ir.sym_tab)
        self.__print_tree(self.__root)
        # self.print_symtable(self.ir.sym_tab)
        self.terminate()
        return super().before_pass()

    def __build_symbol_tree(self, node: ast.SymbolTable, parent_node: Optional[__SymbolTree] = None) -> __SymbolTree:
        root = self.__SymbolTree(node_name=f"SymTable::{node.owner.__class__.__name__}({node.name})",
                                 parent=parent_node)
        symbols = self.__SymbolTree(node_name="Symbols", parent=root)
        children = self.__SymbolTree(node_name="Children", parent=root)

        for sym in node.tab:
            sym = node.tab[sym]
            symbol_node = self.__SymbolTree(node_name=f"Symbol({sym.name})", parent=symbols)
            self.__SymbolTree(node_name=f"declared in {sym.decl.__class__.__name__}", parent=symbol_node)
            defn = self.__SymbolTree(node_name="defn", parent=symbol_node)
            for n in sym.defn:
                self.__SymbolTree(node_name=n.__class__.__name__, parent=defn)
            uses = self.__SymbolTree(node_name="uses", parent=symbol_node)
            for n in sym.uses:
                self.__SymbolTree(node_name=n.__class__.__name__, parent=uses)

        for k in node.kid:
            self.__build_symbol_tree(k, children)
        return root

    def __print_tree(
            self,
            root: __SymbolTree,
            marker: str = "+-- ",
            level_markers: Optional[List[str]] = None
    ) -> None:
        """Recursive function that prints the hierarchical structure of a tree.

        Parameters:
        - root: Node instance, possibly containing children Nodes
        - marker: String to print in front of each node  ("+- " by default)
        - level_markers: Internally used by recursion to indicate where to
                        print markers and connections (see explanations below)

        Note: This implementation is found in https://simonhessner.de/python-3-recursively-print-structured-tree-including-hierarchy-markers-using-depth-first-search/  # noqa
        """
        if root is None:
            return

        empty_str = " " * len(marker)
        connection_str = "|" + empty_str[:-1]
        if not level_markers:
            level_markers = []
        level = len(level_markers)   # recursion level

        def mapper(draw: bool) -> str:
            return connection_str if draw else empty_str

        markers = "".join(map(mapper, level_markers[:-1]))
        markers += marker if level > 0 else ""
        if self.SAVE_OUTPUT:
            f = open(self.SAVE_OUTPUT, "a+")
            print(f"{markers}{root.__class__.__name__}", file=f)
            f.close()
        else:
            print(f"{markers}{root.name}")
        # After root has been printed, recurse down (depth-first) the child nodes.
        for i, child in enumerate(root.kid):
            # The last child will not need connection markers on the current level
            # (see example above)
            is_last = i == len(root.kid) - 1
            self.__print_tree(child, marker, [*level_markers, not is_last])
