"""Printer pass for Jac AST."""
from jaseci.jac.passes.ir_pass import AstNode, Pass


# Should be able to mix in this pass to any other pass to get
# a printout of the AST
class PrinterPass(Pass):
    """Printer Pass for Jac AST."""

    def enter_node(self: "Pass", node: AstNode) -> None:
        """Run on entering node."""
        print("Entering:", node)
        super().enter_node(node)

    def exit_node(self: "Pass", node: AstNode) -> None:
        """Run on exiting node."""
        super().exit_node(node)
        print("Exiting:", node)
