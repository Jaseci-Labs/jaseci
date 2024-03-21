"""Helper for construct."""

from __future__ import annotations

import re
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


def get_type_annotation(data: Any, type_collector: list) -> str:  # noqa: ANN401
    """Get the type annotation of the input data."""
    if isinstance(data, dict):
        class_name = next(
            (value.__class__.__name__ for value in data.values() if value is not None),
            None,
        )
        if class_name:
            ret = f"dict[str, {class_name}]"
            type_collector = extract_non_primary_type(ret, type_collector)
            return ret
        else:
            return "dict[str, Any]"
    else:
        ret = str(type(data).__name__)
        type_collector = extract_non_primary_type(ret, type_collector)
        return ret


def filter(
    scope: str, registry_data: dict, incl_info: tuple[str, str], type_collector: list
) -> tuple:
    """Filter the registry data based on the scope and return the info string."""
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

    info_str = ""
    for incl in incl_info:
        if not key_exists(filtered_data, incl[0]):
            raise ValueError(f"Invalid scope: {incl[0]}")
        res = key_exists(filtered_data, incl[0])
        type_collector = extract_non_primary_type(res[0], type_collector)
        info_str += f"{res[1]} ({str(incl[0])}) ({res[0]}) = {incl[1]}\n"
    return (info_str, filtered_data)


def type_explanation_func(
    type_collector: list, filtered_data: dict
) -> str:  # noqa: ANN401
    """Return the type explanation string."""
    result: dict = {}
    type_collector.append("personality_examples")
    duplicate = type_collector.copy()

    def capture_pattern(x: str) -> list[str]:
        """Capture the pattern."""
        return re.findall(r"(\w+)(?:\(\w+\))?", x)

    def get_data() -> dict:
        """Get the data."""
        for i in duplicate:
            for key, value in filtered_data.items():
                if isinstance(value, dict):
                    for inner_key, inner_value in value.items():
                        if inner_key == i:
                            result[i] = inner_value
                            break
                else:
                    if capture_pattern(key) in i:
                        result[i] = value
                        break
        for i in duplicate:
            for key, value in registry_data.items():
                expected_key = capture_pattern(key).pop()
                if expected_key == i:
                    result[i] = [result[i], value]
                    break
        return result

    get_data()
    type_info = ""
    for key, value in result.items():
        type_info += f"{key}\n"
        if isinstance(value[0], list):
            for i in value:  # TODO : need to implement this
                type_info += f"  {i}\n"
        else:
            type_info += f"  {value}\n"
    return type_info


def extract_non_primary_type(type_str: str, type_collector: list) -> list:
    """Extract non-primary types from the type string."""
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
    type_collector.extend(non_primary_types)
    return list(set(type_collector))


duplicate = ["personality_examples", "Personality", "Person"]
registry_data = {
    "get_emoji(Module)": {
        "model": ["obj", ""],
        "llm": [None, ""],
        "emoji_examples": ["list[dict[str,str]]", "Examples of Text to Emoji"],
        "PersonalityIndex": ["class", "Personality Index of a Person"],
        "Personality": ["enum", "Personality of the Person"],
        "personality_examples": [
            "dict[str,Personality|None]",
            "Personality Information of Famous People",
        ],
        "Person": ["obj", "Person"],
        "outer": ["obj", "main object "],
        "obj1": [None, ""],
        "pp": [None, ""],
    },
    "get_emoji(Module).PersonalityIndex(class)": {"": [None, ""]},
    "get_emoji(Module).Personality(Enum)": {
        "INTROVERT": [None, "Person who is shy and reticent"],
        "EXTROVERT": [None, "Person who is outgoing and socially confident"],
    },
    "get_emoji(Module).Person(obj)": {
        "name": ["str", "Name of the Person"],
        "age": ["int", "Age of the Person"],
    },
    "get_emoji(Module).outer(obj).inner(obj)": {"in_var": ["int", "inner variable"]},
    "get_emoji(Module).outer(obj)": {"inner": ["obj", "inner object"]},
}
