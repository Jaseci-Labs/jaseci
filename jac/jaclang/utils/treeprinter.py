"""Tree Printing Helpers for Jac."""

from __future__ import annotations

import ast as ast3
import builtins
import html
from typing import Optional, TYPE_CHECKING

import jaclang.compiler.absyntree as ast
from jaclang.settings import settings

if TYPE_CHECKING:
    from jaclang.compiler.absyntree import AstNode, SymbolTable

id_bag: dict = {}
id_used: int = 0
CLASS_COLOR_MAP: dict[str, str] = {
    # "AstSymbolNode": "#a8dadc",
    # "AstSymbolStubNode": "#a8dadc",
    # "AstAccessNode": "#f4a261",
    # "AstDocNode": "#d8f3dc",
    # "AstSemStrNode": "#ffd700",
    # "AstAsyncNode": "#86c232",
    # "AstElseBodyNode": "#d8f3dc",
    # "AstTypedVarNode": "#f4a261",
    # "WalkerStmtOnlyNode": "#d8f3dc",
    "Expr": "#ffd700",
    "AtomExpr": "#ffd700",
    "ElementStmt": "#d8f3dc",
    "ArchBlockStmt": "#a8dadc",
    "EnumBlockStmt": "#89c6b3",
    "CodeBlockStmt": "#f4a261",
    "AstImplOnlyNode": "#a8dadc",
    "AstImplNeedingNode": "#457b9d",
    "NameAtom": "#d3d3d3",
    "ArchSpec": "#457b9d",
    "MatchPattern": "#a0d8b3",
    "SubTag": "#d3d3d3",
    "SubNodeList": "#d3d3d3",
    "Module": "#b19cd9",
    "GlobalVars": "#b19cd9",
    "Test": "#b19cd9",
    "ModuleCode": "#b19cd9",
    "PyInlineCode": "#b19cd9",
    "Import": "#b19cd9",
    "ModulePath": "#b19cd9",
    "ModuleItem": "#b19cd9",
    "Architype": "#a8dadc",
    "ArchDef": "#457b9d",
    "Enum": "#89c6b3",
    "EnumDef": "#89c6b3",
    "Ability": "#f6bd60",
    "AbilityDef": "#f6bd60",
    "FuncSignature": "#f6bd60",
    "EventSignature": "#f6bd60",
    "ArchRefChain": "#457b9d",
    "ParamVar": "#f4a261",
    "ArchHas": "#a8dadc",
    "HasVar": "#457b9d",
    "TypedCtxBlock": "#f4a261",
    "IfStmt": "#86c232",
    "ElseIf": "#86c232",
    "ElseStmt": "#d8f3dc",
    "ExprStmt": "#d8f3dc",
    "TryStmt": "#86c232",
    "Except": "#d8f3dc",
    "FinallyStmt": "#d8f3dc",
    "IterForStmt": "#86c232",
    "InForStmt": "#86c232",
    "WhileStmt": "#86c232",
    "WithStmt": "#86c232",
    "ExprAsItem": "#f4a261",
    "RaiseStmt": "#d8f3dc",
    "AssertStmt": "#d8f3dc",
    "CheckStmt": "#d8f3dc",
    "CtrlStmt": "#d8f3dc",
    "DeleteStmt": "#d8f3dc",
    "ReportStmt": "#d8f3dc",
    "ReturnStmt": "#d8f3dc",
    "IgnoreStmt": "#d8f3dc",
    "VisitStmt": "#d8f3dc",
    "RevisitStmt": "#d8f3dc",
    "DisengageStmt": "#d8f3dc",
    "AwaitExpr": "#ffd700",
    "GlobalStmt": "#f4a261",
    "NonLocalStmt": "#f4a261",
    "Assignment": "#f4a261",
    "BinaryExpr": "#ffd700",
    "CompareExpr": "#ffd700",
    "BoolExpr": "#ffd700",
    "LambdaExpr": "#ffd700",
    "UnaryExpr": "#ffd700",
    "IfElseExpr": "#ffd700",
    "MultiString": "#f4a261",
    "FString": "#f4a261",
    "ListVal": "#f4a261",
    "SetVal": "#f4a261",
    "TupleVal": "#f4a261",
    "DictVal": "#f4a261",
    "KVPair": "#f4a261",
    "KWPair": "#f4a261",
    "InnerCompr": "#ff99c8",
    "ListCompr": "#ff99c8",
    "GenCompr": "#ff99c8",
    "SetCompr": "#ff99c8",
    "DictCompr": "#ff99c8",
    "AtomTrailer": "#f4a261",
    "AtomUnit": "#f4a261",
    "YieldExpr": "#ffd700",
    "FuncCall": "#ffd700",
    "IndexSlice": "#ffd700",
    "ArchRef": "#a8dadc",
    "EdgeRefTrailer": "#ffd700",
    "EdgeOpRef": "#ffd700",
    "DisconnectOp": "#ffd700",
    "ConnectOp": "#ffd700",
    "FilterCompr": "#ff99c8",
    "AssignCompr": "#ff99c8",
    "MatchStmt": "#a0d8b3",
    "MatchCase": "#a0d8b3",
    "MatchOr": "#a0d8b3",
    "MatchAs": "#a0d8b3",
    "MatchWild": "#a0d8b3",
    "MatchValue": "#a0d8b3",
    "MatchSingleton": "#a0d8b3",
    "MatchSequence": "#a0d8b3",
    "MatchMapping": "#a0d8b3",
    "MatchKVPair": "#a0d8b3",
    "MatchStar": "#a0d8b3",
    "MatchArch": "#a0d8b3",
    "Token": "#d3d3d3",
    "Name": "#d3d3d3",
    "SpecialVarRef": "#d3d3d3",
    "Literal": "#e07a5f",
    "BuiltinType": "#e07a5f",
    "Float": "#e07a5f",
    "Int": "#e07a5f",
    "String": "#e07a5f",
    "Bool": "#e07a5f",
    "Null": "#e07a5f",
    "Ellipsis": "#e07a5f",
    "EmptyToken": "#e07a5f",
    "Semi": "#e07a5f",
    # "CommentToken": "#e07a5f",
    # "JacSource": "#d3d3d3",
    # "PythonModuleAst": "#b19cd9",
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

    print_py_raise: bool = settings.print_py_raised_ast

    def __node_repr_in_tree(node: AstNode) -> str:
        access = (
            f"Access: {node.access.tag.value} ,"
            if isinstance(node, ast.AstAccessNode) and node.access is not None
            else ""
        )
        sym_table_link = (
            f"SymbolTable: {node.type_sym_tab.name}"
            if isinstance(node, AstSymbolNode) and node.type_sym_tab
            else "SymbolTable: None" if isinstance(node, AstSymbolNode) else ""
        )

        if isinstance(node, Token) and isinstance(node, AstSymbolNode):
            out = (
                f"{node.__class__.__name__} - {node.value} - "
                f"Type: {node.expr_type}, {access} {sym_table_link}"
            )
            if settings.ast_symbol_info_detailed:
                symbol = (
                    node.sym.sym_dotted_name
                    if node.sym
                    else "<No Symbol is associated with this node>"
                )
                out += f", SymbolPath: {symbol}"
            return out
        elif isinstance(node, Token):
            return f"{node.__class__.__name__} - {node.value}, {access}"
        elif (
            isinstance(node, ast.Module)
            and node.py_info.is_raised_from_py
            and not print_py_raise
        ):
            return f"{node.__class__.__name__} - PythonModuleRaised: {node.name}"
        elif isinstance(node, (ast.ModuleItem, ast.ModulePath)):
            out = (
                f"{node.__class__.__name__} - {node.sym_name} - "
                f"abs_path: {node.abs_path}"
            )

            return out
        elif isinstance(node, AstSymbolNode):
            out = (
                f"{node.__class__.__name__} - {node.sym_name} - "
                f"Type: {node.expr_type}, {access} {sym_table_link}"
            )
            if settings.ast_symbol_info_detailed:
                symbol = (
                    node.sym.sym_dotted_name
                    if node.sym
                    else "<No Symbol is associated with this node>"
                )
                out += f" SymbolPath: {symbol}"
            return out
        elif isinstance(node, ast.Expr):
            return f"{node.__class__.__name__} - Type: {node.expr_type}"
        else:
            return f"{node.__class__.__name__}, {access}"

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
        if (
            isinstance(root, ast.Module)
            and root.py_info.is_raised_from_py
            and not print_py_raise
        ):
            kids: list[AstNode] = [
                *filter(
                    lambda x: x.py_info.is_raised_from_py,
                    root.get_all_sub_nodes(ast.Module),
                )
            ]
        else:
            kids = root.kid
        for i, child in enumerate(kids):
            is_last = i == len(kids) - 1
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
            uses = SymbolTree(node_name="uses", parent=symbol_node)
            [
                SymbolTree(
                    node_name=f"line {n.loc.first_line}, col {n.loc.col_start}",
                    parent=uses,
                )
                for n in sym.uses
            ]

    for k in node.kid:
        if k.name == "builtins":
            continue
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
    if (
        root is None
        or depth == 0
        or (settings.filter_sym_builtins and root.name in dir(builtins))
    ):
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
                if settings.filter_sym_builtins and kid_node.name in dir(builtins):
                    continue
                dot_lines.append(f"{gen_node_id(node)}  -> {gen_node_id(kid_node)};")
                gen_dot_graph(kid_node)

    gen_dot_graph(_build_symbol_tree_common(node))

    dot_str = "digraph graph1 {" + "\n".join(dot_lines) + "}"

    return dot_str
