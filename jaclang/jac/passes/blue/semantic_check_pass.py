"""Ast build pass for Jaseci Ast."""
import jaclang.jac.absyntree as ast
from jaclang.jac.passes import Pass


class SemanticCheckPass(Pass):
    """Jac Ast build pass."""

    def before_pass(self) -> None:
        """Before pass."""
        self.has_var_init_conflict_check()
        self.terminate()

    def has_var_init_conflict_check(self) -> None:
        """Check if there is a conflict in variable initialization."""
        for i in self.get_all_sub_nodes(self.ir, ast.ArchBlock):
            init_vars = []
            init_node = None
            for j in i.members:
                if isinstance(j, ast.Ability) and j.py_resolve_name() == "__init__":
                    init_node = j
                    if isinstance(j.signature, ast.FuncSignature) and isinstance(
                        j.signature.params, ast.FuncParams
                    ):
                        for k in j.signature.params.params:
                            init_vars.append(k.name.value)
                break
            if not init_vars:
                continue
            for j in i.members:
                if isinstance(j, ast.ArchHas):
                    for k in j.vars.vars:
                        if k.name.value in init_vars:
                            self.error(
                                f"Has variable {k.name.value} is implicitly initialized through this init",
                                init_node,
                            )
