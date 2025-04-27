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

    # def enter_node(self, node: uni.UniNode) -> None:
    #     """Enter node."""
    #     if node.parent:
    #         if isinstance(node.parent, uni.ModuleCode):
    #             for bb in node.sub
    #             print(type(node).__name__)

    def get_parent_bb(self, node: uni.UniNode) -> uni.UniBasicBlock:
        """Get parent basic block."""
        parent_bb = node.parent_of_type(uni.UniBasicBlock)
        if not parent_bb:
            raise ValueError("Parent basic block not found")
        return parent_bb

    def enter_assignment(self, node: uni.Assignment) -> None:
        """Enter module."""
        parent_bb = self.get_parent_bb(node)
        parent_bb.bb_stmts.append(node)

    def enter_if_stmt(self, node: uni.IfStmt) -> None:
        """Enter module."""
        # print(f"If statement in basic block {node.condition}")
        pass
