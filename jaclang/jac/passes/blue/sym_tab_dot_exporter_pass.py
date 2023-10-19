"""Jac Blue pass for drawing AST."""
from __future__ import annotations

from typing import List, Optional

import jaclang.jac.absyntree as ast
from jaclang.jac.passes import Pass


class SymtabDotGraphPass(Pass):
    """Jac AST convertion to DOT graph."""

    class __SymbolTree:
        def __init__(
                self,
                node_name: str,
                parent: Optional[SymtabDotGraphPass.__SymbolTree] = None,
                children: Optional[List[SymtabDotGraphPass.__SymbolTree]] = None
        ) -> None:
            self.parent = parent
            self.kid = children if children is not None else []
            self.name = node_name

        @property
        def parent(self) -> Optional[SymtabDotGraphPass.__SymbolTree]:
            return self.__parent

        @parent.setter
        def parent(self, parent_node: SymtabDotGraphPass.__SymbolTree) -> None:
            if parent_node:
                self.__parent = parent_node
                parent_node.kid.append(self)

    OUTPUT_FILE_PATH: str = "out.dot"

    def before_pass(self) -> None:
        """Initialize pass."""
        self.__dot_lines: list[str] = []
        self.__id_map: dict[int, int] = {}
        self.__lase_id_used = 0
        self.__gen_dot_graph(self.__build_symbol_tree(self.ir.sym_tab))
        self.terminate()
        return super().before_pass()

    def __build_symbol_tree(self, node: ast.SymbolTable, parent_node: Optional[__SymbolTree] = None) -> __SymbolTree:
        root = self.__SymbolTree(node_name=f"SymTable::{node.owner.__class__.__name__}({node.name})", parent=parent_node)
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
