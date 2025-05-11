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

    edge_type: uni.EdgeOpRef
    async_visit: bool


class VisitPredictionPass:
    """Visit statement detection.

    Helps provide some static information about the visit statement.
    """

    def _get_edge_list(self, node: uni.VisitStmt) -> uni.EdgeOpRef:
        op_refs = node.get_all_sub_nodes(uni.EdgeOpRef)
        return op_refs[0]

    def _get_function(self, node: uni.VisitStmt) -> uni.ArchBlockStmt:
        func = node.find_parent_of_type(uni.ArchBlockStmt)
        if func is None:
            raise RuntimeError()
        return func

    def _get_walker(self, node: uni.VisitStmt) -> uni.Architype:
        walker = node.find_parent_of_type(uni.Architype)
        if walker is None:
            raise RuntimeError()
        return walker

    def _get_edge_type_name(self, node: uni.EdgeOpRef) -> str:
        edge_type_name = ""
        type_filters = node.get_all_sub_nodes(uni.FilterCompr)
        if len(type_filters) > 0:
            type_filter = type_filters[0]
            name_node = type_filter.get_all_sub_nodes(uni.Name)
            edge_type_name = name_node[0].value
        return edge_type_name

    def _get_name(self, node: uni.UniNode) -> str | None:
        for kid in node.kid:
            if isinstance(kid, uni.Name):
                return kid.value
        return None

    def get_visit_stmt_info(self, node: uni.VisitStmt) -> VisitStmtInfo:
        """Process a visit statement.

        It will return some information potentially useful to runtime data mapping.
        """
        edge_op_ref = self._get_edge_list(node)
        result = VisitStmtInfo(
            edge_type=edge_op_ref,
            async_visit=self._get_edge_type_name(edge_op_ref).startswith("async_"),
        )
        return result


def _get_next_steps(
    current_node: NodeAnchor, visited: set[NodeAnchor]
) -> list[list[NodeAnchor]]:
    next_nodes: list[list[NodeAnchor]] = []
    one_level: list[NodeAnchor] = []

    for neighbor in current_node.edges:
        if neighbor.target in visited:
            continue
        print(str(neighbor.architype))
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


def _traversal(start: NodeAnchor) -> list[list[NodeAnchor]]:
    queue: list[list[NodeAnchor]] = [[start]]
    traversal: list[list[NodeAnchor]] = []
    visited: set[NodeAnchor] = set()
    print(type(start))
    while len(queue) > 0:
        node_level = queue.pop()
        traversal.append(node_level)
        next_nodes = [
            _get_next_steps(current_node, visited) for current_node in node_level
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
MAX_NODE_NUM_PER_DPU = 64  # TODO: You should define this appropriately


def generate_data_mapping(
    visit_stmts: list[uni.VisitStmt], start: NodeAnchor
) -> dict[NodeAnchor, int]:
    """Generate data mapping."""
    print(type(start.architype))

    traversal_order = _traversal(start)
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
