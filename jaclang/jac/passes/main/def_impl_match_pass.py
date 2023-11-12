"""Connect Decls and Defs in AST.

This pass creates links in the ast between Decls of Architypes and Abilities
that are separate from their implementations (Defs). This pass creates a link
in the ast between the Decls and Defs of Architypes and Abilities through the
body field.
"""
import jaclang.jac.absyntree as ast
from jaclang.jac.passes import Pass
from jaclang.jac.passes.main import SubNodeTabPass
from jaclang.jac.symtable import SymbolTable, SymbolType


class DeclDefMatchPass(Pass):
    """Decls and Def matching pass."""

    def before_pass(self) -> None:
        """Before pass."""
        if not self.ir.sym_tab:
            self.error(
                f"Expected symbol table on node {self.ir.__class__.__name__}. Perhaps an earlier pass failed."
            )
        else:
            self.connect_def_impl(self.ir.sym_tab)
        self.terminate()

    def after_pass(self) -> None:
        """Rebuild sub node table."""
        self.ir = SubNodeTabPass(input_ir=self.ir, prior=self).ir

    def connect_def_impl(self, sym_tab: SymbolTable) -> None:
        """Connect Decls and Defs."""
        for sym in sym_tab.tab.values():
            if sym.sym_type == SymbolType.IMPL:
                # currently strips the type info from impls
                arch_refs = [x[3:] for x in sym.sym_name.split(".")]
                lookup = sym_tab.lookup(arch_refs[0])
                decl_node = lookup.decl if lookup else None
                for name in arch_refs[1:]:
                    if decl_node:
                        lookup = (
                            decl_node.sym_tab.lookup(name)
                            if decl_node.sym_tab
                            else None
                        )
                        decl_node = lookup.decl if lookup else None
                    else:
                        break
                if not decl_node:
                    continue
                elif isinstance(decl_node, ast.Ability) and decl_node.is_abstract:
                    self.warning(
                        f"Abstract ability {decl_node.py_resolve_name()} should not have a definition.",
                        decl_node,
                    )
                    continue
                decl_node.body = sym.decl  # type: ignore
                sym.decl.decl_link = decl_node  # type: ignore
                decl_node.add_kids_right([sym.decl], pos_update=False)  # type: ignore
                decl_node.sym_tab.tab = sym.decl.sym_tab.tab  # type: ignore
        for i in sym_tab.kid:
            self.connect_def_impl(i)
