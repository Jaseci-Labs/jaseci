"""Connect Decls and Defs in AST."""
import jaclang.jac.absyntree as ast
from jaclang.jac.passes import Pass
from jaclang.jac.passes.blue import SubNodeTabPass
from jaclang.jac.symtable import SymbolTable, SymbolType


class DeclDefMatchPass(Pass):
    """Decls and Def matching pass."""

    def before_pass(self) -> None:
        """Before pass."""
        self.need_match = []
        if not self.ir.sym_tab:
            return self.ice("Expected symbol table on node.")
        self.connect_decl_def(self.ir.sym_tab)

    #        self.terminate()

    def after_pass(self) -> None:
        """Rebuild sub node table."""
        self.ir = SubNodeTabPass(mod_path=self.mod_path, input_ir=self.ir).ir

    def connect_decl_def(self, sym_tab: SymbolTable) -> None:
        """Connect Decls and Defs."""
        # print(sym_tab)
        for sym in sym_tab.tab.values():
            if sym.sym_type in [SymbolType.ABILITY, SymbolType.ARCH]:
                if isinstance(sym.decl, ast.Ability) and sym.decl.is_abstract:
                    if sym.defn:
                        self.error(
                            f"Abstract ability {sym.name} should not have a definition.",
                            sym.defn[-1],
                        )
                    continue
                if not sym.decl:
                    self.error(
                        f"Unable to match implementation {sym.name} to an declaration.",
                        sym.defn[-1],
                    )
                if not sym.defn:
                    self.error(
                        f"Unable to match declaration {sym.name} to an implementation.",
                        sym.decl,
                    )
                if sym.decl and sym.defn and sym.decl != sym.defn[-1]:
                    ast.append_node(sym.decl, sym.defn[-1])
                    sym.decl.body = sym.defn[-1].body  # type: ignore
                    sym.decl.sym_tab = sym.defn[-1].sym_tab
        for i in sym_tab.kid:
            self.connect_decl_def(i)
