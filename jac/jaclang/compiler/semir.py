"""Semantic IR for Jaclang."""

from __future__ import annotations

from typing import Optional, TYPE_CHECKING
from jaclang.compiler.constant import SymbolAccess, SymbolType
from symtable import SymbolTable, Symbol

# if TYPE_CHECKING:
import jaclang.compiler.absyntree as ast


# class SemInfo:
#     """Semantic information class."""

#     def __init__(
#         self,
#         node: ast.AstNode,
#         name: str,
#         type_str: Optional[str] = None,
#         semstr: str = "",
#     ) -> None:
#         self.node_type: Optional[type[ast.AstNode]] = None
#         self.name: Optional[str] = None
#         self.type: Optional[str] = None
#         self.semstr: Optional[str] = None
#         self.scope: Optional[SemScope] = None


# class SemScope:
#     """Scope class."""

#     def __init__(
#         self, scope: str, type: str, parent: Optional[SemScope] = None
#     ) -> None:
#         self.parent: Optional[SymbolTable] = None
#         self.type: Optional[SymbolType] = None
#         self.scope: Optional[SymbolTable] = None


class SemIR:
    """Semantic IR class."""

    def __init__(self):
        self.tree: Optional[SemNode] = SemNode(name="root")

    def add_node(self, node: ast.AstNode, sem_node: SemNode) -> None:
        symboltable_trace = []
        curr_node = node
        while curr_node:
            symboltable_trace.append(
                (curr_node.sym_tab.name, str(type(curr_node)).split(".")[-1][0:-2])
            )
            curr_node = curr_node.parent
        symboltable_trace.reverse()
        symboltable_trace = symboltable_trace[0:-2]
        # print(symboltable_trace[0:-2])

        curr_sem_node = self.tree
        for name, node_type in symboltable_trace:
            if node_type in ["SubNodeList", "ArchHas"]:
                continue
            node_found = False
            for child in curr_sem_node.children:
                if child.name == name:
                    curr_sem_node = child
                    node_found = True
                    break
            if not node_found:
                curr_sem_node.add_child(SemNode(name=name, node_type=node_type))
                curr_sem_node = curr_sem_node.children[-1]
        curr_sem_node.add_child(sem_node)

    def pp(self):
        """Recursively print the tree."""

        def _print_node(node: SemNode, indent: int = 0):
            prefix = "  " * indent
            print(f"{prefix}- {node.node_type or 'Node'}: {node.name}")
            if node.available_symbols:
                for sym_name, sym_node in node.available_symbols.items():
                    print(
                        f"{prefix}    [symbol] {sym_name} -> {sym_node.node_type or 'Node'}: {sym_node.name}"
                    )
            for child in node.children:
                _print_node(child, indent + 1)

        print("Semantic IR Tree:")
        _print_node(self.tree)


class SemNode:
    """Semantic node class."""

    def __init__(self, name: str, node_type: Optional[str] = None) -> None:
        # self.node: Optional[ast.AstNode] = node
        self.name: Optional[str] = name
        self.node_type: Optional[str] = node_type
        self.semstr: Optional[str] = None
        self.children: Optional[list[SemNode]] = []
        self.parent: Optional[SemNode] = []
        self.available_symbols: Optional[dict[str, SemNode]] = {}
        self.meta: Optional[dict[str, int | str | bool | list | dict | None]] = {}

    def add_child(self, child: SemNode) -> None:
        """Add child to node."""
        child.parent = self
        self.children.append(child)

    def add_symbol(self, name: str, child: SemNode) -> None:
        """Add symbol to node."""
        self.available_symbols[name] = child

    def get_scope_chain(self) -> list[SemNode]:
        """Get scope chain."""
        scope = []
        current = self
        while current:
            scope.append(current)
            current = current.parent
        return scope
