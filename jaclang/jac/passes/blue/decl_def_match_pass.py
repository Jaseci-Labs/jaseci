"""Connect Decls and Defs in AST."""
import jaclang.jac.absyntree as ast
from jaclang.jac.passes import Pass
from jaclang.jac.passes.blue import SubNodeTabPass
from jaclang.jac.symtable import SymbolHitType, SymbolTable, SymbolType


class DeclDefMatchPass(Pass):
    """Decls and Def matching pass."""

    def before_pass(self) -> None:
        """Before pass."""
        self.need_match = []
        if not self.ir.sym_tab:
            return self.ice("Expected symbol table on node.")
        self.connect_decl_def(self.ir.sym_tab)
        self.terminate()

    def after_pass(self) -> None:
        """Rebuild sub node table."""
        self.ir = SubNodeTabPass(
            prior=self, mod_path=self.mod_path, input_ir=self.ir
        ).ir

    def connect_decl_def(self, sym_tab: SymbolTable) -> None:
        """Connect Decls and Defs."""
        for sym in sym_tab.tab.values():
            if sym.sym_type == SymbolType.IMPL:
                # currently strips the type info from impls
                arch_refs = [x[3:] for x in sym.name.split(".")]
                lookup = sym_tab.lookup(arch_refs[0], sym_hit=SymbolHitType.DECL_DEFN)
                decl_node = lookup.decl if lookup else None
                for name in arch_refs[1:]:
                    if decl_node:
                        lookup = (
                            decl_node.sym_tab.lookup(
                                name, sym_hit=SymbolHitType.DECL_DEFN
                            )
                            if decl_node.sym_tab
                            else None
                        )
                        decl_node = lookup.decl if lookup else None
                    else:
                        break
                if not decl_node:
                    self.error(
                        f"Unable to match implementation {sym.name} to a declaration.",
                        sym.defn[-1],
                    )
                    continue
                elif isinstance(decl_node, ast.Ability) and decl_node.is_abstract:
                    self.error(
                        f"Abstract ability {decl_node.py_resolve_name()} should not have a definition.",
                        decl_node,
                    )
                    continue
                ast.append_node(decl_node, sym.defn[-1].body)  # type: ignore
                decl_node.body = sym.defn[-1].body  # type: ignore
                decl_node.sym_tab.tab = sym.defn[-1].sym_tab.tab  # type: ignore
                sym.decl = decl_node

        for i in sym_tab.kid:
            self.connect_decl_def(i)
