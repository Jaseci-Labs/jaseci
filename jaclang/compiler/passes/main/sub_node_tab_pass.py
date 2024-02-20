"""Subnode Table building pass.

This pass builds a table of subnodes for each node in the AST. This is used
for fast lookup of nodes of a certain type in the AST. This is just a utility
pass and is not required for any other pass to work.
"""

from copy import copy
from typing import Optional

import jaclang.compiler.absyntree as ast
from jaclang.compiler.passes import Pass


class SubNodeTabPass(Pass):
    """AST Enrichment Pass for basic high level semantics."""

    def before_pass(self) -> None:
        """Initialize pass."""
        self.cur_module: Optional[ast.Module] = None

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
