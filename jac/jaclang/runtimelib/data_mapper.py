from dataclasses import dataclass
from jaclang.compiler import unitree as uni
from jaclang.runtimelib.architype import EdgeArchitype, GenericEdge, NodeAnchor
import pprint

@dataclass
class VisitStmtInfo:
    """Helpful information about a visit statment

    Helps provide some more insights into the visit pattern
    """
    edgeType: uni.EdgeOpRef
    asyncVisit: bool

class VisitPredictionPass():
    """Visit statement detection.

    Helps provide some static information about the visit statement.
    """

    def _get_edge_list(self, node: uni.VisitStmt) -> uni.EdgeOpRef:
        opRefs = node.get_all_sub_nodes(uni.EdgeOpRef)
        return opRefs[0]

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
        type_filter = node.get_all_sub_nodes(uni.FilterCompr)
        if (len(type_filter) > 0):
            type_filter = type_filter[0]
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
        result = VisitStmtInfo(edgeType=edge_op_ref, asyncVisit=self._get_edge_type_name(edge_op_ref).startswith("async_"))
        return result


def _traversal(start: NodeAnchor):
    queue: list[list[NodeAnchor]] = [[start]]
    traversal: list[list[NodeAnchor]] = []
    while (len(queue) > 0):
        node_level = queue.pop()
        traversal.append(node_level)
        new_nodes: list[NodeAnchor] = []
        for node in node_level:
            new_nodes = new_nodes + [edge.target for edge in node.edges]
        queue.append(new_nodes)


def generate_data_mapping(visit_stmts: list[uni.VisitStmt]) -> None:
    static_analysis = VisitPredictionPass()
    static_info = [static_analysis.get_visit_stmt_info(visit_stmt) for visit_stmt in visit_stmts]
    pass
