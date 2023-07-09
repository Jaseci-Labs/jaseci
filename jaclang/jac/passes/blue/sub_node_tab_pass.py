"""Subnode Table building pass."""
from copy import copy

import jaclang.jac.absyntree as ast
from jaclang.jac.passes import Pass


class SubNodeTabPass(Pass):
    """AST Enrichment Pass for basic high level semantics."""

    def enter_node(self, node: ast.AstNode) -> None:
        """Table builder."""
        super().enter_node(node)
        node._sub_node_tab = {}  # clears on entry

    def exit_node(self, node: ast.AstNode) -> None:
        """Table builder."""
        super().exit_node(node)
        for i in node.kid:
            if not i:
                continue
            for k, v in i._sub_node_tab.items():
                if k in node._sub_node_tab:
                    node._sub_node_tab[k].extend(v)
                else:
                    node._sub_node_tab[k] = copy(v)
            if type(i) in node._sub_node_tab:
                node._sub_node_tab[type(i)].append(i)
            else:
                node._sub_node_tab[type(i)] = [i]
