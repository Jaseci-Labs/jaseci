"""Tree Printing Helpers for Jac."""
from __future__ import annotations

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from jaclang.jac.absyntree import AstNode, SymbolTable


def print_ast_tree(
    root: AstNode,
    marker: str = "+-- ",
    level_markers: Optional[list[bool]] = None,
    output_file: Optional[str] = None,
    max_depth: Optional[int] = None,
) -> str:
    """Recursively print ast tree."""
    from jaclang.jac.absyntree import AstSymbolNode, Token

    def __node_repr_in_tree(node: AstNode) -> str:
        if isinstance(node, Token):
            return f"{node.__class__.__name__} - {node.value}"
        elif isinstance(node, AstSymbolNode):
            return f"{node.__class__.__name__} - {node.sym_name}"
        else:
            return f"{node.__class__.__name__}"

    if root is None or (
        max_depth is not None and len(level_markers or []) >= max_depth
    ):
        return ""

    empty_str = " " * len(marker)
    connection_str = "|" + empty_str[:-1]
    if not level_markers:
        level_markers = []
    level = len(level_markers)  # recursion level

    def mapper(draw: bool) -> str:
        return connection_str if draw else empty_str

    markers = "".join(map(mapper, level_markers[:-1]))
    markers += marker if level > 0 else ""

    tree_str = f"{root.loc}\t{markers}{__node_repr_in_tree(root)}\n"

    for i, child in enumerate(root.kid):
        is_last = i == len(root.kid) - 1
        tree_str += print_ast_tree(
            child, marker, [*level_markers, not is_last], output_file, max_depth
        )

    # Write to file only at the top level call
    if output_file and level == 0:
        with open(output_file, "w") as f:
            f.write(tree_str)

    return tree_str


class SymbolTree:
    """Symbol Tree Node."""

    def __init__(
        self,
        node_name: str,
        parent: Optional[SymbolTree] = None,
        children: Optional[list[SymbolTree]] = None,
    ) -> None:
        """Initialize Symbol Tree Node."""
        self.parent = parent
        self.kid = children if children is not None else []
        self.name = node_name

    @property
    def parent(self) -> Optional[SymbolTree]:
        """Get parent node."""
        return self.__parent

    @parent.setter
    def parent(self, parent_node: Optional[SymbolTree]) -> None:
        """Set parent node."""
        if parent_node:
            self.__parent = parent_node
            parent_node.kid.append(self)


def _build_symbol_tree_common(
    node: SymbolTable, parent_node: Optional[SymbolTree] = None
) -> SymbolTree:
    root = SymbolTree(
        node_name=f"SymTable::{node.owner.__class__.__name__}({node.name})",
        parent=parent_node,
    )
    symbols = SymbolTree(node_name="Symbols", parent=root)
    children = SymbolTree(node_name="Sub Tables", parent=root)

    for sym in node.tab.values():
        symbol_node = SymbolTree(node_name=f"{sym.sym_name}", parent=symbols)
        SymbolTree(node_name=f"{sym.access} {sym.sym_type}", parent=symbol_node)

        if sym.decl:
            SymbolTree(
                node_name=f"decl: line {sym.decl.loc.first_line}, col {sym.decl.loc.col_start}",
                parent=symbol_node,
            )
        defn = SymbolTree(node_name="defn", parent=symbol_node)
        [
            SymbolTree(
                node_name=f"line {n.loc.first_line}, col {n.loc.col_start}", parent=defn
            )
            for n in sym.defn
        ]

    for k in node.kid:
        _build_symbol_tree_common(k, children)
    return root


def print_symtab_tree(
    root: SymbolTree,
    marker: str = "+-- ",
    level_markers: Optional[list[bool]] = None,
    output_file: Optional[str] = None,
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
    if output_file:
        with open(output_file, "a+") as f:
            print(f"{markers}{root.name}", file=f)
    else:
        print(f"{markers}{root.name}")
    # After root has been printed, recurse down (depth-first) the child nodes.
    for i, child in enumerate(root.kid):
        # The last child will not need connection markers on the current level
        # (see example above)
        is_last = i == len(root.kid) - 1
        print_symtab_tree(
            child, marker, [*level_markers, not is_last], output_file=output_file
        )
