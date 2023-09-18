"""Ast build pass for Jaseci Ast."""
# import jaclang.jac.absyntree as ast
from jaclang.jac.passes import Pass


class SemanticCheckPass(Pass):
    """Jac Ast build pass."""

    def before_pass(self) -> None:
        """Before pass."""
        self.terminate()

    # def has_var_init_conflict_check(self) -> None:
    #     """Check if there is a conflict in variable initialization."""
    #     abilities = [
    #         i for i in self.get_all_sub_nodes(self.ir, ast.Ability) if i.arch_attached
    #     ]
