"""Data mapper.

This module is responsible for: 1. Predicting the data access pattern and 2. Calculate the best mapping to PIM
"""

from dataclasses import dataclass

from jaclang.compiler import unitree as uni
from jaclang.runtimelib.architype import NodeAnchor


@dataclass
class VisitStmtInfo:
    """Helpful information about a visit statment.

    Helps provide some more insights into the visit pattern
    """

    edge_type: str | None
    async_visit: bool


def _get_from_node_type_of_visit(visit_stmt: uni.VisitStmt) -> str:
    """Get the node type that the visit is from.

    For example, if a visit is in an ability:
        can xxx with XXX entry {...}, it will return XXX
    """
    ability = visit_stmt.parent_of_type(uni.Ability)
    return (
        ability.get_all_sub_nodes(uni.EventSignature)[0]
        .get_all_sub_nodes(uni.Name)[0]
        .value
    )


def _get_to_edge_type_of_visit(visit_stmt: uni.VisitStmt) -> str | None:
    filters = visit_stmt.get_all_sub_nodes(uni.FilterCompr)
    if len(filters) == 0:
        return None
    return filters[0].get_all_sub_nodes(uni.Name)[0].value


def _get_visit_info(visit_stmts: list[uni.VisitStmt]) -> dict[str, list[VisitStmtInfo]]:
    res: dict[str, list[VisitStmtInfo]] = {}
    for visit_stmt in visit_stmts:
        from_node = _get_from_node_type_of_visit(visit_stmt)
        if from_node not in res.keys():
            res[from_node] = []
        edge_type = _get_to_edge_type_of_visit(visit_stmt)
        async_visit = edge_type is not None and edge_type.startswith("async_")
        res[from_node].append(
            VisitStmtInfo(edge_type=edge_type, async_visit=async_visit)
        )
    return res


def _get_next_steps(
    current_node: NodeAnchor,
    visited: set[NodeAnchor],
    visit_stmt_info: dict[str, list[VisitStmtInfo]],
) -> list[list[NodeAnchor]]:
    next_nodes: list[list[NodeAnchor]] = []
    one_level: list[NodeAnchor] = []

    node_type_name = type(current_node.architype).__name__
    possible_visits = visit_stmt_info.get(node_type_name, [])

    for visit in possible_visits:
        for neighbor in current_node.edges:
            if (
                visit.edge_type is not None
                and str(neighbor.architype) != visit.edge_type + "()"
            ):
                continue
            if neighbor.target in visited:
                continue
            # TODO: Change this async to a better representation
            if str(neighbor.architype).startswith("async_"):
                one_level.append(neighbor.target)
            else:
                if one_level:
                    next_nodes.append(one_level)
                    one_level = []
                next_nodes.append([neighbor.target])

    if one_level:
        next_nodes.append(one_level)

    return next_nodes


def _traversal(
    start: NodeAnchor, visit_stmt_info: dict[str, list[VisitStmtInfo]]
) -> list[list[NodeAnchor]]:
    queue: list[list[NodeAnchor]] = [[start]]
    traversal: list[list[NodeAnchor]] = []
    visited: set[NodeAnchor] = set()
    while len(queue) > 0:
        print("running")
        node_level = queue.pop()
        traversal.append(node_level)
        next_nodes = [
            _get_next_steps(current_node, visited, visit_stmt_info)
            for current_node in node_level
        ]
        max_length = max([len(next_node) for next_node in next_nodes])
        for i in range(max_length):
            one_level: list[NodeAnchor] = []
            for next_node in next_nodes:
                if i < len(next_node):
                    one_level += next_node[i]
            for node in one_level:
                visited.add(node)
            if len(one_level) > 0:
                queue.append(one_level)

    return traversal


NUM_DPU = 8  # TODO: You should define this appropriately
MAX_NODE_NUM_PER_DPU = 640  # TODO: You should define this appropriately


def generate_data_mapping(
    visit_stmts: list[uni.VisitStmt], start: NodeAnchor
) -> dict[NodeAnchor, int]:
    """Generate data mapping."""
    traversal_order = _traversal(start, _get_visit_info(visit_stmts))
    dpu_node_count = [0] * NUM_DPU
    node_assignments: dict[NodeAnchor, int] = {}
    for layer in traversal_order:
        dpu_index = 0
        for node in layer:
            # Find the next DPU with available capacity
            for _ in range(NUM_DPU):
                if dpu_node_count[dpu_index] < MAX_NODE_NUM_PER_DPU:
                    break
                dpu_index = (dpu_index + 1) % NUM_DPU

            if dpu_node_count[dpu_index] >= MAX_NODE_NUM_PER_DPU:
                raise RuntimeError("Node assignment failed")

            node_assignments[node] = dpu_index
            dpu_node_count[dpu_index] += 1
            dpu_index = (dpu_index + 1) % NUM_DPU

    return node_assignments
