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

    def enter_module(self, node: uni.Module) -> None:
        """Enter module."""
        pass
