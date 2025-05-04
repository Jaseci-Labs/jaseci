from dataclasses import dataclass
from jaclang.compiler import unitree as uni
from jaclang.runtimelib.architype import EdgeArchitype, GenericEdge

@dataclass
class VisitStmtInfo:
    """Helpful information about a visit statment

    Helps provide some more insights into the visit pattern
    """
    edgeType: EdgeArchitype
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

    def _get_name(self, node: uni.UniNode) -> str | None:
        for kid in node.kid:
            if isinstance(kid, uni.Name):
                return kid.value
        return None

    def get_visit_stmt_info(self, node: uni.VisitStmt) -> VisitStmtInfo:
        """Process a visit statement.

        It will return some information potentially useful to runtime data mapping.
        """
        edge_op_ref_trailer = self._get_edge_list(node)
        print(edge_op_ref_trailer.pp())
        result = VisitStmtInfo(edgeType=GenericEdge(), asyncVisit=False)
        return result
        # walker = self.get_name(self.get_walker(node))
        # func = self.get_name(self.get_function(node))
        #
        # pprint.pprint(edge_ref_trailer.to_dict())


def generate_data_mapping(visit_stmts: list[uni.VisitStmt]) -> None:
    static_analysis = VisitPredictionPass()
    static_info = [static_analysis.get_visit_stmt_info(visit_stmt) for visit_stmt in visit_stmts]

    
    
    pass
