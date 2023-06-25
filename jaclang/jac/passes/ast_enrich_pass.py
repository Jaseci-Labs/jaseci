"""AST Enrichment Pass."""
import jaclang.jac.absyntree as ast
from jaclang.jac.passes.ir_pass import Pass


class AstEnrichmentPass(Pass):
    """AST Enrichment Pass for basic high level semantics."""

    def before_pass(self) -> None:
        """Initialize pass."""

    def exit_arch_block(self, node: ast.ArchBlock) -> None:
        """Sub objects.

        members: list["ArchHas | Ability"],
        """
        for i in node.kid:
            if type(i) == ast.Ability:
                i.is_attached = True
