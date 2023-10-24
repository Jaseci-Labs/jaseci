"""Jac Blue pass for drawing AST."""
from __future__ import annotations

from typing import List, Optional

from jaclang.jac.passes import Pass
from jaclang.jac.symtable import SymbolTable


class _SymbolTree:
    def __init__(
        self,
        node_name: str,
        parent: Optional["_SymbolTree"] = None,
        children: Optional[List["_SymbolTree"]] = None,
    ) -> None:
        self.parent = parent
        self.kid = children if children is not None else []
        self.name = node_name

    @property
    def parent(self) -> Optional["_SymbolTree"]:
        return self.__parent

    @parent.setter
    def parent(self, parent_node: Optional["_SymbolTree"]) -> None:
        if parent_node:
            self.__parent = parent_node
            parent_node.kid.append(self)


def _build_symbol_tree_common(
    node: SymbolTable, parent_node: Optional[_SymbolTree] = None
) -> _SymbolTree:
    root = _SymbolTree(
        node_name=f"SymTable::{node.owner.__class__.__name__}({node.name})",
        parent=parent_node,
    )
    symbols = _SymbolTree(node_name="Symbols", parent=root)
    children = _SymbolTree(node_name="Sub Tables", parent=root)

    for sym in node.tab.values():
        symbol_node = _SymbolTree(node_name=f"{sym.sym_name}", parent=symbols)
        _SymbolTree(node_name=f"{sym.access} {sym.sym_type}", parent=symbol_node)

        if sym.decl:
            _SymbolTree(
                node_name=f"decl: line {sym.decl.loc.first_line}, col {sym.decl.loc.col_start}",
                parent=symbol_node,
            )
        defn = _SymbolTree(node_name="defn", parent=symbol_node)
        [
            _SymbolTree(
                node_name=f"line {n.loc.first_line}, col {n.loc.col_start}", parent=defn
            )
            for n in sym.defn
        ]

    for k in node.kid:
        _build_symbol_tree_common(k, children)
    return root


class SymbolTablePrinterPass(Pass):
    """Jac symbol table conversion to ASCII tree."""

    SAVE_OUTPUT: Optional[str] = None

    def before_pass(self) -> None:
        """Initialize pass."""
        if isinstance(self.ir.sym_tab, SymbolTable):
            root = _build_symbol_tree_common(self.ir.sym_tab)
            self._print_tree(root)
        self.terminate()
        return super().before_pass()

    def _print_tree(
        self,
        root: _SymbolTree,
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
            self._print_tree(child, marker, [*level_markers, not is_last])


class SymbolTableDotGraphPass(Pass):
    """Jac AST conversion to DOT graph."""

    OUTPUT_FILE_PATH: Optional[str] = "out.dot"

    def before_pass(self) -> None:
        """Initialize pass."""
        self.__dot_lines: list[str] = []
        self.__id_map: dict[int, int] = {}
        self.__lase_id_used = 0
        if isinstance(self.ir.sym_tab, SymbolTable):
            self.__gen_dot_graph(_build_symbol_tree_common(self.ir.sym_tab))
        self.terminate()
        return super().before_pass()

    def __gen_node_id(self, node: _SymbolTree) -> int:
        if id(node) not in self.__id_map:
            self.__id_map[id(node)] = self.__lase_id_used
            self.__lase_id_used += 1
        return self.__id_map[id(node)]

    def __gen_node_parameters(self, node: _SymbolTree) -> str:
        shape = ""
        fillcolor = ""
        style = ""
        label = f'"{node.name}"'
        label = f"{label} {shape} {style} {fillcolor}".strip()
        return f"[label={label}]"

    def __gen_dot_graph(self, node: _SymbolTree) -> None:
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
