"""Control flow graph build pass.

This pass builds the control flow graph for the Jac program by filling in  details in UniBasicBlock.
These nodes will be linked together in the CFG pass.
"""

# from typing import TypeVar

import jaclang.compiler.unitree as uni
from jaclang.compiler.passes import AstPass


class CFGBuildPass(AstPass):
    """Jac Symbol table build pass."""

    def before_pass(self) -> None:
        """Before pass."""
        pass

    def get_parent_bb(self, node: uni.UniNode) -> uni.UniBasicBlock | None:
        """Get parent basic block."""
        if not isinstance(node, uni.Module):
            parent_bb = node.parent_of_type(uni.UniBasicBlock)
            return parent_bb
        else:
            return None

    def enter_node(self, node: uni.UniNode) -> None:
        """Enter UniBasicBlock nodes."""
        if isinstance(node, uni.UniBasicBlock):
            parent_bb = self.get_parent_bb(node)
            if isinstance(parent_bb, uni.UniBasicBlock):
                if isinstance(parent_bb, uni.IfStmt):
                    node.bb_stmts.append(node)
                    if node.control_in_bbs:
                        node.control_in_bbs.append(parent_bb)
                    if parent_bb.control_out_bbs:
                        parent_bb.control_out_bbs.append(parent_bb)
                else:
                    parent_bb.bb_stmts.append(node)
                    node.bb_stmts = parent_bb.bb_stmts
