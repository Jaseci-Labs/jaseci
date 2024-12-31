"""Subnode Table building pass.

This pass builds a table of subnodes for each node in the AST. This is used
for fast lookup of nodes of a certain type in the AST. This is just a utility
pass and is not required for any other pass to work.
"""

import os
import pickle
from copy import copy

import jaclang.compiler.absyntree as ast
from jaclang.compiler.passes import Pass


class SubNodeTabPass(Pass):
    """AST Enrichment Pass for basic high level semantics."""

    def enter_node(self, node: ast.AstNode) -> None:
        """Table builder."""
        super().enter_node(node)
        node._sub_node_tab = {}  # clears on entry
        self.dumped_modules: dict = {}

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

    def after_pass(self) -> None:
        """Dump module dependencies."""
        super().after_pass()
        if isinstance(self.ir, ast.Module) and self.ir.mod_deps:
            full_path = next(iter(self.ir.mod_deps))
            folder_path = os.path.join(os.path.dirname(full_path), "__jac_gen__")
            os.makedirs(folder_path, exist_ok=True)
            bc_file = os.path.join(
                folder_path, self.ir.mod_deps[full_path].name + ".pkl"
            )
            for i in self.ir.mod_deps.keys():
                try:
                    self.dumped_modules[i] = pickle.dumps(self.ir.mod_deps[i])
                except Exception as e:
                    print(f"Failed to pickle module '{i}': {str(e)}")
            with open(bc_file, "wb") as f:
                pickle.dump(self.dumped_modules, f)
