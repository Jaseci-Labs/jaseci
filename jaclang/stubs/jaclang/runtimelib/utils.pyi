import ast as ast3
import jaclang.compiler.absyntree as ast
from jaclang.compiler.semtable import SemScope as SemScope
from jaclang.runtimelib.constructs import (
    NodeAnchor as NodeAnchor,
    NodeArchitype as NodeArchitype,
)
from typing import Callable, Iterator

def sys_path_context(path: str) -> Iterator[None]: ...
def collect_node_connections(
    current_node: NodeAnchor, visited_nodes: set, connections: set
) -> None: ...
def traverse_graph(
    node: NodeArchitype,
    cur_depth: int,
    depth: int,
    edge_type: list[str],
    traverse: bool,
    connections: list,
    node_depths: dict[NodeArchitype, int],
    visited_nodes: list,
    queue: list,
    bfs: bool,
    dfs: Callable,
    node_limit: int,
    edge_limit: int,
) -> None: ...
def get_sem_scope(node: ast.AstNode) -> SemScope: ...
def extract_type(node: ast.AstNode) -> list[str]: ...
def extract_params(
    body: ast.FuncCall,
) -> tuple[
    dict[str, ast.Expr], list[tuple[str, ast3.AST]], list[tuple[str, ast3.AST]]
]: ...
