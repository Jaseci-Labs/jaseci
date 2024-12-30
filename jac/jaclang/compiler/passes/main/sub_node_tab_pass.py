"""Subnode Table building pass.

This pass builds a table of subnodes for each node in the AST. This is used
for fast lookup of nodes of a certain type in the AST. This is just a utility
pass and is not required for any other pass to work.
"""

from copy import copy

import jaclang.compiler.absyntree as ast
from jaclang.compiler.passes import Pass


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
        if isinstance(node, ast.Module) and node.mod_deps:
            full_path = next(iter(node.mod_deps))
            folder_path = os.path.join(os.path.dirname(full_path), "__jac_gen__")
            os.makedirs(folder_path, exist_ok=True)
            bc_file = os.path.join(folder_path, node.mod_deps[full_path].name + ".jbc")
            for i in node.mod_deps:
                self.dumped_modules[i] = pickle.dumps(node.mod_deps[i])
            with open(bc_file, "wb") as f:
                marshal.dump(self.dumped_modules, f)
                
