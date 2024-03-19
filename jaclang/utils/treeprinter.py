"""Tree Printing Helpers for Jac."""

from __future__ import annotations

import ast as ast3
import html
from typing import Optional, TYPE_CHECKING

import jaclang.compiler.absyntree as ast


if TYPE_CHECKING:
    from jaclang.compiler.absyntree import AstNode, SymbolTable

id_bag: dict = {}
id_used: int = 0
CLASS_COLOR_MAP: dict[str, str] = {
    "Architype": "red",
    "Ability": "green",
    "ArchDef": "blue",
    "AbilityDef": "yellow",
}


def dotgen_ast_tree(
    root: AstNode,
    dot_lines: Optional[list[str]] = None,
) -> str:
    """Recursively generate ast tree in dot format."""
    global id_bag, id_used
    starting_call = False
    if dot_lines is None:
        starting_call = True
        dot_lines = []

    def gen_node_id(node: ast.AstNode) -> int:
        """Generate number for each nodes."""
        global id_bag, id_used
        if id(node) not in id_bag:
            id_bag[id(node)] = id_used
            id_used += 1
        return id_bag[id(node)]

    def gen_node_parameters(node: ast.AstNode) -> str:
        shape = ""
        fillcolor = ""
        style = ""
        _class__ = str(node.__class__)[35:-2]
        if _class__ in CLASS_COLOR_MAP:
            shape = 'shape="box"'
            style = 'style="filled"'
            fillcolor = f'fillcolor="{CLASS_COLOR_MAP[_class__]}"'
        info1: list[tuple[str, str, str]] = []
        if isinstance(node, ast.Token):
            """ "Only tokens and some declared types are box(others are oval )"""
            shape = 'shape="box"'
            info1.append(("name", "=", node.name))
            info1.append(("value", "=", html.escape(node.value)))

        if len(info1) == 0:
            label = f'"{node.__class__.__name__}"'
        else:
            label = f"<{node.__class__.__name__}"
            for i in info1:
                label += f"<BR/> {i[0]}{i[1]}{i[2]}"
            label += ">"

        label = f"{label} {shape} {style} {fillcolor}".strip()
        return f"[label={label}]"

    dot_lines.append(f"{gen_node_id(root)} {gen_node_parameters(root)};")
    for i in root.kid:
        dot_lines.append(f"{gen_node_id(root)}  -> {gen_node_id(i)};")
        dotgen_ast_tree(i, dot_lines)
    if starting_call:
        return "\ndigraph graph1 {" + "\n".join(list(set(dot_lines))) + "}"
    return " "


def print_ast_tree(
    root: AstNode | ast3.AST,
    marker: str = "+-- ",
    level_markers: Optional[list[bool]] = None,
    output_file: Optional[str] = None,
    max_depth: Optional[int] = None,
) -> str:
    """Recursively print ast tree."""
    from jaclang.compiler.absyntree import AstSymbolNode, Token

    def __node_repr_in_tree(node: AstNode) -> str:
        if isinstance(node, Token) and isinstance(node, AstSymbolNode):
            return (
                f"{node.__class__.__name__} - {node.value} - Type: {node.sym_info.typ}"
            )
        elif isinstance(node, Token):
            return f"{node.__class__.__name__} - {node.value}"
        elif isinstance(node, AstSymbolNode):
            return f"{node.__class__.__name__} - {node.sym_name} - Type: {node.sym_info.typ}"
        else:
            return f"{node.__class__.__name__}"

    def __node_repr_in_py_tree(node: ast3.AST) -> str:
        if isinstance(node, ast3.Constant):
            return f"{node.__class__.__name__} - {node.value}"
        elif isinstance(node, ast3.Name):
            return f"{node.__class__.__name__} - {node.id}"
        elif isinstance(node, ast3.FunctionDef | ast3.ClassDef | ast3.AsyncFunctionDef):
            return f"{node.__class__.__name__} - {node.name}"
        elif isinstance(node, ast3.Import):
            return f"{node.__class__.__name__} - {', '.join(alias.name for alias in node.names)}"
        elif isinstance(node, ast3.ImportFrom):
            return f"{node.__class__.__name__} - {node.module} : {', '.join(alias.name for alias in node.names)}"
        elif isinstance(node, ast3.alias):
            return f"{node.__class__.__name__} - {node.name}"
        elif isinstance(node, ast3.Attribute):
            return f"{node.__class__.__name__} - {node.attr}"
        elif isinstance(node, ast3.Call):
            if isinstance(node.func, ast3.Name):
                return f"{node.__class__.__name__} - {node.func.id}"
            elif isinstance(node.func, ast3.Attribute):
                return f"{node.__class__.__name__} - {node.func.attr}"
            else:
                return f"{node.__class__.__name__}"
        else:
            return f"{node.__class__.__name__}"

    def get_location_info(node: ast3.AST) -> str:
        if hasattr(node, "lineno"):
            start_pos = f"{node.lineno}:{node.col_offset + 1}"
            end_pos = f"{node.end_lineno}:{node.end_col_offset + 1 if node.end_col_offset else node.col_offset}"
            prefix = f"{start_pos} - {end_pos}"
            return prefix
        return "-:- - -:-"

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

    if isinstance(root, ast.AstNode):
        tree_str = f"{root.loc}\t{markers}{__node_repr_in_tree(root)}\n"
        for i, child in enumerate(root.kid):
            is_last = i == len(root.kid) - 1
            tree_str += print_ast_tree(
                child, marker, [*level_markers, not is_last], output_file, max_depth
            )
    elif isinstance(root, ast3.AST):
        tree_str = (
            f"{get_location_info(root)}\t{markers}{__node_repr_in_py_tree(root)}\n"
        )
        for i_a, child_a in enumerate(ast3.iter_child_nodes(root)):
            is_last = i_a == len(list(ast3.iter_child_nodes(root))) - 1
            tree_str += print_ast_tree(
                child_a, marker, [*level_markers, not is_last], output_file, max_depth
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

        # if isinstance(node.owner, ast.AstSymbolNode) and node.owner.sym_info:
        #     print("From tree printer", id(node.owner))
        #     SymbolTree(node_name=f"Datatype: {node.owner.sym_info.typ}", parent=symbol_node)

        if sym.decl and sym.decl.loc.first_line > 0:
            SymbolTree(
                node_name=f"decl: line {sym.decl.loc.first_line}, col {sym.decl.loc.col_start}",
                parent=symbol_node,
            )
            defn = SymbolTree(node_name="defn", parent=symbol_node)
            [
                SymbolTree(
                    node_name=f"line {n.loc.first_line}, col {n.loc.col_start}",
                    parent=defn,
                )
                for n in sym.defn
            ]

    for k in node.kid:
        _build_symbol_tree_common(k, children)
    return root


def print_symtab_tree(
    root: SymbolTable,
    marker: str = "+-- ",
    level_markers: Optional[list[bool]] = None,
    output_file: Optional[str] = None,
    depth: Optional[int] = None,
) -> str:
    """Recursively print symbol table tree."""
    return get_symtab_tree_str(
        _build_symbol_tree_common(root),
        marker,
        level_markers,
        output_file,
        depth,
    )


def get_symtab_tree_str(
    root: SymbolTree,
    marker: str = "+-- ",
    level_markers: Optional[list[bool]] = None,
    output_file: Optional[str] = None,
    depth: Optional[int] = None,
) -> str:
    """Recursively print symbol table tree."""
    if root is None or depth == 0:
        return ""

    level_markers = level_markers or []
    markers = "".join(
        [
            "|" + " " * (len(marker) - 1) if draw else " " * len(marker)
            for draw in level_markers[:-1]
        ]
    ) + (marker if level_markers else "")
    line = f"{markers}{root.name}\n"

    if output_file:
        with open(output_file, "a+") as f:
            f.write(line)

    return line + "".join(
        get_symtab_tree_str(
            child,
            marker,
            level_markers + [i < len(root.kid) - 1],
            output_file,
            None if depth is None else depth - 1,
        )
        for i, child in enumerate(root.kid)
    )


def dotgen_symtab_tree(node: SymbolTable) -> str:
    """Generate DOT graph representation of a symbol table tree."""
    dot_lines = []
    id_map = {}
    last_id_used = 0

    def gen_node_id(node: SymbolTree) -> int:
        nonlocal last_id_used
        if id(node) not in id_map:
            id_map[id(node)] = last_id_used
            last_id_used += 1
        return id_map[id(node)]

    def gen_node_parameters(node: SymbolTree) -> str:
        shape = ""
        fillcolor = ""
        style = ""
        label = f'"{node.name}"'
        label = f"{label} {shape} {style} {fillcolor}".strip()
        return f"[label={label}]"

    def gen_dot_graph(node: SymbolTree) -> None:
        nonlocal dot_lines
        dot_lines.append(f"{gen_node_id(node)} {gen_node_parameters(node)};")
        for kid_node in node.kid:
            if kid_node:
                dot_lines.append(f"{gen_node_id(node)}  -> {gen_node_id(kid_node)};")
                gen_dot_graph(kid_node)

    gen_dot_graph(_build_symbol_tree_common(node))

    dot_str = "digraph graph1 {" + "\n".join(dot_lines) + "}"

    return dot_str
