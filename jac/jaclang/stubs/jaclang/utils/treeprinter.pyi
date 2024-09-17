import ast as ast3
from _typeshed import Incomplete
from jaclang.compiler.absyntree import AstNode as AstNode, SymbolTable as SymbolTable
from jaclang.settings import settings as settings

id_bag: dict
id_used: int
CLASS_COLOR_MAP: dict[str, str]

def dotgen_ast_tree(root: AstNode, dot_lines: list[str] | None = None) -> str: ...
def print_ast_tree(
    root: AstNode | ast3.AST,
    marker: str = "+-- ",
    level_markers: list[bool] | None = None,
    output_file: str | None = None,
    max_depth: int | None = None,
) -> str: ...

class SymbolTree:
    kid: Incomplete
    name: Incomplete
    def __init__(
        self,
        node_name: str,
        parent: SymbolTree | None = None,
        children: list[SymbolTree] | None = None,
    ) -> None: ...
    @property
    def parent(self) -> SymbolTree | None: ...
    @parent.setter
    def parent(self, parent_node: SymbolTree | None) -> None: ...

def print_symtab_tree(
    root: SymbolTable,
    marker: str = "+-- ",
    level_markers: list[bool] | None = None,
    output_file: str | None = None,
    depth: int | None = None,
) -> str: ...
def get_symtab_tree_str(
    root: SymbolTree,
    marker: str = "+-- ",
    level_markers: list[bool] | None = None,
    output_file: str | None = None,
    depth: int | None = None,
) -> str: ...
def dotgen_symtab_tree(node: SymbolTable) -> str: ...
