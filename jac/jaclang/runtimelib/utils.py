"""Helper for construct."""

from __future__ import annotations

import ast as ast3
import sys
from contextlib import contextmanager
from types import UnionType
from typing import Callable, Iterator, TYPE_CHECKING

import jaclang.compiler.unitree as uni

if TYPE_CHECKING:
    from jaclang.runtimelib.constructs import NodeAnchor, NodeArchitype


@contextmanager
def sys_path_context(path: str) -> Iterator[None]:
    """Add a path to sys.path temporarily."""
    novel_path = path not in sys.path
    try:
        if novel_path:
            sys.path.append(path)
        yield
    finally:
        if novel_path:
            sys.path.remove(path)


def collect_node_connections(
    current_node: NodeAnchor,
    visited_nodes: set,
    connections: set,
) -> None:
    """Nodes and edges representing the graph are collected in visited_nodes and connections."""
    if current_node not in visited_nodes:
        visited_nodes.add(current_node)
        edges = current_node.edges
        for edge_ in edges:
            target = edge_.target
            if target:
                connections.add(
                    (
                        current_node.architype,
                        target.architype,
                        edge_.__class__.__name__,
                    )
                )
                collect_node_connections(target, visited_nodes, connections)


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
) -> None:
    """Traverse the graph using Breadth-First Search (BFS) or Depth-First Search (DFS)."""
    for edge in node.__jac__.edges:
        is_self_loop = id(edge.source) == id(edge.target)
        is_in_edge = edge.target == node.__jac__
        if (traverse and is_in_edge) or edge.architype.__class__.__name__ in edge_type:
            continue
        if is_self_loop:
            continue  # lets skip self loop for a while, need to handle it later
        elif (other_nda := edge.target if not is_in_edge else edge.source) and (
            other_nd := other_nda.architype
        ):
            new_con = (
                (node, other_nd, edge.architype)
                if not is_in_edge
                else (other_nd, node, edge.architype)
            )
            if node in node_depths and node_depths[node] is not None:
                if other_nd in node_depths:
                    node_depths[node] = min(
                        cur_depth, node_depths[node], node_depths[other_nd] + 1
                    )
                    node_depths[other_nd] = min(
                        cur_depth + 1, node_depths[node] + 1, node_depths[other_nd]
                    )
                else:
                    if other_nd:
                        node_depths[other_nd] = min(
                            cur_depth + 1, node_depths[node] + 1
                        )
                    else:
                        raise ValueError("Edge is detached from node in graph")
            if (
                other_nd
                and new_con not in connections
                and (
                    (
                        depth < 0
                        or min(node_depths[node], node_depths[other_nd]) + 1 <= depth
                    )
                    and node_limit > len(visited_nodes)
                    and edge_limit > len(connections)
                )
            ):
                connections.append(new_con)
                if bfs:
                    queue.append([other_nd, cur_depth + 1])
                else:

                    dfs(other_nd, cur_depth + 1)


def extract_type(node: uni.UniNode) -> list[str]:
    """Collect type information in assignment using bfs."""
    extracted_type = []
    if isinstance(node, (uni.BuiltinType, uni.Token)):
        extracted_type.append(node.value)
    for child in node.kid:
        extracted_type.extend(extract_type(child))
    return extracted_type


def extract_params(
    body: uni.FuncCall,
) -> tuple[dict[str, uni.Expr], list[tuple[str, ast3.AST]], list[tuple[str, ast3.AST]]]:
    """Extract model parameters, include and exclude information."""
    model_params = {}
    include_info = []
    exclude_info = []
    if body.params:
        for param in body.params.items:
            if isinstance(param, uni.KWPair) and isinstance(param.key, uni.Name):
                key = param.key.value
                value = param.value
                if key not in ["incl_info", "excl_info"]:
                    model_params[key] = value
                elif key == "incl_info":
                    if isinstance(value, uni.AtomUnit):
                        var_name = (
                            value.value.right.value
                            if isinstance(value.value, uni.AtomTrailer)
                            and isinstance(value.value.right, uni.Name)
                            else (
                                value.value.value
                                if isinstance(value.value, uni.Name)
                                else ""
                            )
                        )
                        include_info.append((var_name, value.gen.py_ast[0]))
                    elif isinstance(value, uni.TupleVal) and value.values:
                        for i in value.values.items:
                            var_name = (
                                i.right.value
                                if isinstance(i, uni.AtomTrailer)
                                and isinstance(i.right, uni.Name)
                                else (i.value if isinstance(i, uni.Name) else "")
                            )
                            include_info.append((var_name, i.gen.py_ast[0]))
                elif key == "excl_info":
                    if isinstance(value, uni.AtomUnit):
                        var_name = (
                            value.value.right.value
                            if isinstance(value.value, uni.AtomTrailer)
                            and isinstance(value.value.right, uni.Name)
                            else (
                                value.value.value
                                if isinstance(value.value, uni.Name)
                                else ""
                            )
                        )
                        exclude_info.append((var_name, value.gen.py_ast[0]))
                    elif isinstance(value, uni.TupleVal) and value.values:
                        for i in value.values.items:
                            var_name = (
                                i.right.value
                                if isinstance(i, uni.AtomTrailer)
                                and isinstance(i.right, uni.Name)
                                else (i.value if isinstance(i, uni.Name) else "")
                            )
                            exclude_info.append((var_name, i.gen.py_ast[0]))
    return model_params, include_info, exclude_info


def is_instance(
    obj: object, target: type | UnionType | tuple[type | UnionType, ...]
) -> bool:
    """Check if object is instance of target type."""
    match target:
        case UnionType():
            return any((is_instance(obj, trg) for trg in target.__args__))
        case tuple():
            return any((is_instance(obj, trg) for trg in target))
        case type():
            return isinstance(obj, target)
        case _:
            return False


def all_issubclass(
    classes: type | UnionType | tuple[type | UnionType, ...], target: type
) -> bool:
    """Check if all classes is subclass of target type."""
    match classes:
        case type():
            return issubclass(classes, target)
        case UnionType():
            return all((all_issubclass(cls, target) for cls in classes.__args__))
        case tuple():
            return all((all_issubclass(cls, target) for cls in classes))
        case _:
            return False
