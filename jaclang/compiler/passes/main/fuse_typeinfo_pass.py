"""Integrate mypy infrastructure into Jac.

This is used to call mypy type checking into Jac files by integrating
mypy apis into Jac and use jac py ast in it.
"""

import jaclang.compiler.absyntree as ast
from jaclang.compiler.passes import Pass

# import jaclang.compiler.passes.utils.mypy_ast_build as myab
# import mypy.nodes as mnodes


class FuseTypeInfo(Pass):
    """Python and bytecode file printing pass."""

    def enter_node(self, node: ast.AstNode) -> None:
        """Call mypy checks on module level only."""
        # print(node.__class__.__name__, len(node.gen.mypy_ast))
        # if node.__class__.__name__ == "Name" and len(node.gen.mypy_ast) > 0:
        #     print(node.loc, node.gen.mypy_ast[0].__class__.__name__, node.value)
        #     print(node.loc, dir(node.gen.mypy_ast[0]))
        # for i in node.gen.mypy_ast:
        #     if isinstance(i, mnodes.NameExpr):
        #         try:
        #             if isinstance(i.node, mnodes.Var):
        #                 print(node.loc, i.name, i.node.type)
        #         except Exception as e:
        #             print(e)
        #             print(node.loc, " I failed")
        # super().enter_node(node)
