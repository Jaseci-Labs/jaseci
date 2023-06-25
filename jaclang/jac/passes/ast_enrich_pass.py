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
        # Tags all function signatures whether method style or not
        for i in self.get_all_sub_nodes(node, ast.FuncSignature):
            i.is_arch_attached = True
