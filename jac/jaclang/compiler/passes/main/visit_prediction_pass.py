"""Visit statement detection.

Helps provide some static information about the visit statement.
"""

import jaclang.compiler.unitree as uni
from jaclang.compiler.passes import UniPass


class VisitPredictionPass(UniPass):
    """Visit statement detection.

    Helps provide some static information about the visit statement.
    """

    def _get_edge_list(self, node: uni.VisitStmt) -> uni.EdgeRefTrailer | None:
        for kid in node.kid:
            if isinstance(kid, uni.EdgeRefTrailer):
                return kid
        return None

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

    def enter_visit_stmt(self, _: uni.VisitStmt) -> None:
        """Process a visit statement.

        It will return some information potentially useful to runtime data mapping.
        """
        pass
        # edge_ref_trailer = self.get_edge_list(node)
        # walker = self.get_name(self.get_walker(node))
        # func = self.get_name(self.get_function(node))
        #
        # pprint.pprint(edge_ref_trailer.to_dict())
