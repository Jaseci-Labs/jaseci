"""Helper for construct."""

from __future__ import annotations

import re
from enum import Enum
from typing import Any, Callable, TYPE_CHECKING


if TYPE_CHECKING:
    from jaclang.core.construct import NodeAnchor, NodeArchitype


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
            target = edge_._jac_.target
            if target:
                connections.add(
                    (current_node.obj, target._jac_.obj, edge_.__class__.__name__)
                )
                collect_node_connections(target._jac_, visited_nodes, connections)


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
    for edge in node._jac_.edges:
        is_self_loop = id(edge._jac_.source) == id(edge._jac_.target)
        is_in_edge = edge._jac_.target == node
        if (traverse and is_in_edge) or edge._jac_.obj.__class__.__name__ in edge_type:
            continue
        if is_self_loop:
            continue  # lets skip self loop for a while, need to handle it later
        else:
            other_nd = edge._jac_.target if not is_in_edge else edge._jac_.source
            new_con = (
                (node, other_nd, edge) if not is_in_edge else (other_nd, node, edge)
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


def get_type_annotation(data: Any) -> str:  # noqa: ANN401
    """Get the type annotation of the input data."""
    if isinstance(data, dict):
        class_name = next(
            (value.__class__.__name__ for value in data.values() if value is not None),
            None,
        )
        if class_name:
            return f"dict[str, {class_name}]"
        else:
            return "dict[str, Any]"
    else:
        return str(type(data).__name__)


def filter(scope: str, registry_data: dict, incl_info: tuple[str, str]) -> tuple:
    """Filter the registry data based on the scope and return the info string."""
    collected_types = []
    avail_scopes = [scope] + [
        ".".join(scope.split(".")[:i]) for i in range(1, len(scope.split(".")))
    ]
    filtered_data = {
        key: registry_data[key] for key in avail_scopes if key in registry_data
    }

    def key_exists(dictionary: dict, key: str) -> Any:  # noqa: ANN401
        """Check if key exists in registry."""
        for k, v in dictionary.items():
            if k == key:
                return v
            if isinstance(v, dict) and key_exists(v, key):
                return v[key]
        return False

    info_str = []
    for incl in incl_info:
        if not key_exists(filtered_data, incl[0]):
            raise ValueError(f"Invalid scope: {incl[0]}")
        res = key_exists(filtered_data, incl[0])
        collected_types.extend(extract_non_primary_type(res[0]))
        info_str.append(
            f"{res[1]} ({str(incl[0])}) ({res[0]}) = {get_object_string(incl[1])}"
        )
    return ("\n".join(info_str), collected_types)


def get_type_explanation(
    type_str: str, registry_data: dict
) -> tuple[str, set[Any]] | None:
    """Get the type explanation of the input type string."""
    main_registry_type_info = None
    scope = None
    for k, v in registry_data.items():
        if isinstance(v, dict):
            for i, j in v.items():
                if i == type_str:
                    main_registry_type_info = j
                    scope = k
                    break
    if not main_registry_type_info:
        return None
    type_type = main_registry_type_info[0]
    type_semstr = main_registry_type_info[1]
    type_info = registry_data[f"{scope}.{type_str}({type_type})"]
    type_info_str = []
    type_info_types = []
    if type_type == "Enum" and isinstance(type_info, dict):
        for k, v in type_info.items():
            if isinstance(v, list):
                type_info_str.append(f"{v[1]} ({k}) (EnumItem)")
    elif type_type in ["obj", "class", "node", "edge"] and isinstance(type_info, dict):
        for k, v in type_info.items():
            if isinstance(v, list):
                type_info_str.append(f"{v[1]} ({k}) ({v[0]})")
                if extract_non_primary_type(v[0]):
                    type_info_types.extend(extract_non_primary_type(v[0]))
    return (
        f"{type_semstr} ({type_str}) ({type_type}) = {', '.join(type_info_str)}",
        set(type_info_types),
    )


def extract_non_primary_type(type_str: str) -> list:
    """Extract non-primary types from the type string."""
    if not type_str:
        return []
    pattern = r"(?:\[|,\s*|\|)([a-zA-Z_][a-zA-Z0-9_]*)|([a-zA-Z_][a-zA-Z0-9_]*)"
    matches = re.findall(pattern, type_str)
    primary_types = [
        "str",
        "int",
        "float",
        "bool",
        "list",
        "dict",
        "tuple",
        "set",
        "Any",
        "None",
    ]
    non_primary_types = [m for t in matches for m in t if m and m not in primary_types]
    return non_primary_types


def get_all_type_explanations(type_list: list, registry_data: dict) -> dict:
    """Get all type explanations from the input type list."""
    collected_type_explanations = {}
    for type_item in type_list:
        type_explanation = get_type_explanation(type_item, registry_data)
        if type_explanation is not None:
            type_explanation_str, nested_types = type_explanation
            if type_item not in collected_type_explanations:
                collected_type_explanations[type_item] = type_explanation_str
            if nested_types:
                nested_collected_type_explanations = get_all_type_explanations(
                    list(nested_types), registry_data
                )
                for k, v in nested_collected_type_explanations.items():
                    if k not in collected_type_explanations:
                        collected_type_explanations[k] = v
    return collected_type_explanations


def get_object_string(obj: Any) -> Any:  # noqa: ANN401
    """Get the string representation of the input object."""
    if isinstance(obj, str):
        return f'"{obj}"'
    elif isinstance(obj, (int, float, bool)):
        return str(obj)
    elif isinstance(obj, list):
        return "[" + ", ".join(get_object_string(item) for item in obj) + "]"
    elif isinstance(obj, tuple):
        return "(" + ", ".join(get_object_string(item) for item in obj) + ")"
    elif isinstance(obj, dict):
        return (
            "{"
            + ", ".join(
                f"{get_object_string(key)}: {get_object_string(value)}"
                for key, value in obj.items()
            )
            + "}"
        )
    elif isinstance(obj, Enum):
        return f"{obj.__class__.__name__}.{obj.name}"
    elif hasattr(obj, "__dict__"):
        args = ", ".join(
            f"{key}={get_object_string(value)}"
            for key, value in vars(obj).items()
            if key != "_jac_"
        )
        return f"{obj.__class__.__name__}({args})"
    else:
        return str(obj)
