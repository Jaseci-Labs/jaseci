"""Jac Blue pass for drawing AST."""
from __future__ import annotations

from typing import Optional

from jaclang.compiler.passes import Pass
from jaclang.compiler.symtable import SymbolTable
from jaclang.utils.treeprinter import (
    SymbolTree,
    _build_symbol_tree_common,
    print_symtab_tree,
)


class SymbolTablePrinterPass(Pass):
    """Jac symbol table conversion to ASCII tree."""

    SAVE_OUTPUT: Optional[str] = None

    def before_pass(self) -> None:
        """Initialize pass."""
        if isinstance(self.ir.sym_tab, SymbolTable):
            print_symtab_tree(self.ir.sym_tab, output_file=self.SAVE_OUTPUT)
        self.terminate()
        return super().before_pass()


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

    def __gen_node_id(self, node: SymbolTree) -> int:
        if id(node) not in self.__id_map:
            self.__id_map[id(node)] = self.__lase_id_used
            self.__lase_id_used += 1
        return self.__id_map[id(node)]

    def __gen_node_parameters(self, node: SymbolTree) -> str:
        shape = ""
        fillcolor = ""
        style = ""
        label = f'"{node.name}"'
        label = f"{label} {shape} {style} {fillcolor}".strip()
        return f"[label={label}]"

    def __gen_dot_graph(self, node: SymbolTree) -> None:
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
