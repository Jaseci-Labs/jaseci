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
            children: Optional[List[SymbolTablePrinterPass.__SymbolTree]] = None,
        ) -> None:
            self.parent = parent
            self.kid = children if children is not None else []
            self.name = node_name

        @property
        def parent(self) -> Optional[SymbolTablePrinterPass.__SymbolTree]:
            return self.__parent

        @parent.setter
        def parent(
            self, parent_node: Optional[SymbolTablePrinterPass.__SymbolTree]
        ) -> None:
            if parent_node:
                self.__parent = parent_node
                parent_node.kid.append(self)

    SAVE_OUTPUT: Optional[str] = None

    def before_pass(self) -> None:
        """Initialize pass."""
        if isinstance(self.ir.sym_tab, ast.SymbolTable):
            self.__root = self.__build_symbol_tree(self.ir.sym_tab)
            self.__print_tree(self.__root)
        self.terminate()
        return super().before_pass()

    def __build_symbol_tree(
        self, node: ast.SymbolTable, parent_node: Optional[__SymbolTree] = None
    ) -> __SymbolTree:
        root = self.__SymbolTree(
            node_name=f"SymTable::{node.owner.__class__.__name__}({node.name})",
            parent=parent_node,
        )
        symbols = self.__SymbolTree(node_name="Symbols", parent=root)
        children = self.__SymbolTree(node_name="Children", parent=root)

        for sym in node.tab:
            sym = node.tab[sym]
            symbol_node = self.__SymbolTree(
                node_name=f"Symbol({sym.name})", parent=symbols
            )
            self.__SymbolTree(
                node_name=f"declared in {sym.decl.__class__.__name__}",
                parent=symbol_node,
            )
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
        level_markers: Optional[List[bool]] = None,
    ) -> None:
        """Recursive function that prints the hierarchical structure of a tree."""
        if root is None:
            return

        empty_str = " " * len(marker)
        connection_str = "|" + empty_str[:-1]
        if not level_markers:
            level_markers = []
        level = len(level_markers)  # recursion level

        def mapper(draw: bool) -> str:
            return connection_str if draw else empty_str

        markers = "".join(map(mapper, level_markers[:-1]))
        markers += marker if level > 0 else ""
        if self.SAVE_OUTPUT:
            with open(self.SAVE_OUTPUT, "a+") as f:
                print(f"{markers}{root.name}", file=f)
        else:
            print(f"{markers}{root.name}")
        # After root has been printed, recurse down (depth-first) the child nodes.
        for i, child in enumerate(root.kid):
            # The last child will not need connection markers on the current level
            # (see example above)
            is_last = i == len(root.kid) - 1
            self.__print_tree(child, marker, [*level_markers, not is_last])


class SymbolTableDotGraphPass(Pass):
    """Jac AST convertion to DOT graph."""

    class __SymbolTree:
        def __init__(
            self,
            node_name: str,
            parent: Optional[SymbolTableDotGraphPass.__SymbolTree] = None,
            children: Optional[List[SymbolTableDotGraphPass.__SymbolTree]] = None,
        ) -> None:
            self.parent = parent
            self.kid = children if children is not None else []
            self.name = node_name

        @property
        def parent(self) -> Optional[SymbolTableDotGraphPass.__SymbolTree]:
            return self.__parent

        @parent.setter
        def parent(
            self, parent_node: Optional[SymbolTableDotGraphPass.__SymbolTree]
        ) -> None:
            if parent_node:
                self.__parent = parent_node
                parent_node.kid.append(self)

    OUTPUT_FILE_PATH: Optional[str] = "out.dot"

    def before_pass(self) -> None:
        """Initialize pass."""
        self.__dot_lines: list[str] = []
        self.__id_map: dict[int, int] = {}
        self.__lase_id_used = 0
        if isinstance(self.ir.sym_tab, ast.SymbolTable):
            self.__gen_dot_graph(self.__build_symbol_tree(self.ir.sym_tab))
        self.terminate()
        return super().before_pass()

    def __build_symbol_tree(
        self, node: ast.SymbolTable, parent_node: Optional[__SymbolTree] = None
    ) -> __SymbolTree:
        root = self.__SymbolTree(
            node_name=f"SymTable::{node.owner.__class__.__name__}({node.name})",
            parent=parent_node,
        )
        symbols = self.__SymbolTree(node_name="Symbols", parent=root)
        children = self.__SymbolTree(node_name="Children", parent=root)

        for sym in node.tab:
            sym = node.tab[sym]
            symbol_node = self.__SymbolTree(
                node_name=f"Symbol({sym.name})", parent=symbols
            )
            self.__SymbolTree(
                node_name=f"declared in {sym.decl.__class__.__name__}",
                parent=symbol_node,
            )
            defn = self.__SymbolTree(node_name="defn", parent=symbol_node)
            for n in sym.defn:
                self.__SymbolTree(node_name=n.__class__.__name__, parent=defn)
            uses = self.__SymbolTree(node_name="uses", parent=symbol_node)
            for n in sym.uses:
                self.__SymbolTree(node_name=n.__class__.__name__, parent=uses)

        for k in node.kid:
            self.__build_symbol_tree(k, children)
        return root

    def __gen_node_id(self, node: __SymbolTree) -> int:
        if id(node) not in self.__id_map:
            self.__id_map[id(node)] = self.__lase_id_used
            self.__lase_id_used += 1
        return self.__id_map[id(node)]

    def __gen_node_parameters(self, node: __SymbolTree) -> str:
        shape = ""
        fillcolor = ""
        style = ""
        label = f'"{node.name}"'
        label = f"{label} {shape} {style} {fillcolor}".strip()
        return f"[label={label}]"

    def __gen_dot_graph(self, node: __SymbolTree) -> None:
        self.__dot_lines.append(
            f"{self.__gen_node_id(node)} {self.__gen_node_parameters(node)};"
        )
        for kid_node in node.kid:
            if kid_node:
                self.__dot_lines.append(
                    f"{self.__gen_node_id(node)}  -> {self.__gen_node_id(kid_node)};"
                )
                self.__gen_dot_graph(kid_node)

    def after_pass(self) -> None:
        """Finalize pass by generating the dot file."""
        if self.OUTPUT_FILE_PATH:
            with open(self.OUTPUT_FILE_PATH, "w") as f:
                f.write("digraph graph1 {")
                f.write("\n".join(self.__dot_lines))
                f.write("}")
        else:
            print("digraph graph1 {")
            print("\n".join(self.__dot_lines))
            print("}")
        return super().after_pass()
