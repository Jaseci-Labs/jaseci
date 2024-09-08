"""Connect Decls and Defs in AST.

This pass creates links in the ast between Decls of Architypes and Abilities
that are separate from their implementations (Defs). This pass creates a link
in the ast between the Decls and Defs of Architypes and Abilities through the
body field.
"""

import jaclang.compiler.absyntree as ast
from jaclang.compiler.passes import Pass
from jaclang.compiler.passes.main import SubNodeTabPass
from jaclang.compiler.symtable import Symbol, SymbolTable


class DeclImplMatchPass(Pass):
    """Decls and Def matching pass."""

    def enter_module(self, node: ast.Module) -> None:
        """Enter module."""
        if not node.sym_tab:
            self.error(
                f"Expected symbol table on node {node.__class__.__name__}. Perhaps an earlier pass failed."
            )
        else:
            self.connect_def_impl(node.sym_tab)

    def after_pass(self) -> None:
        """Rebuild sub node table."""
        self.ir = SubNodeTabPass(input_ir=self.ir, prior=self).ir

    def defn_lookup(self, lookup: Symbol) -> ast.NameAtom | None:
        """Lookup a definition in a symbol table."""
        for defn in range(len(lookup.defn)):
            candidate = lookup.defn[len(lookup.defn) - (defn + 1)]
            if (
                isinstance(candidate.name_of, ast.AstImplNeedingNode)
                and candidate.name_of.needs_impl
            ):
                return candidate
        return None

    def connect_def_impl(self, sym_tab: SymbolTable) -> None:
        """Connect Decls and Defs."""
        for sym in sym_tab.tab.values():
            if isinstance(sym.decl.name_of, ast.AstImplOnlyNode):
                # currently strips the type info from impls
                arch_refs = [x[3:] for x in sym.sym_name.split(".")]
                name_of_links: list[ast.NameAtom] = []  # to link archref names to decls
                lookup = sym_tab.lookup(arch_refs[0])
                # If below may need to be a while instead of if to skip over local
                # import name collisions (see test: test_impl_decl_resolution_fix)
                if lookup and not isinstance(
                    lookup.decl.name_of, ast.AstImplNeedingNode
                ):
                    lookup = (
                        sym_tab.parent.lookup(arch_refs[0]) if sym_tab.parent else None
                    )
                decl_node = (
                    self.defn_lookup(lookup)
                    if len(arch_refs) == 1 and lookup
                    else lookup.defn[-1] if lookup else None
                )
                name_of_links.append(decl_node) if decl_node else None
                for name in arch_refs[1:]:
                    if decl_node:
                        lookup = (
                            decl_node.name_of.sym_tab.lookup(name, deep=False)
                            if decl_node.name_of.sym_tab
                            else None
                        )
                        decl_node = (
                            self.defn_lookup(lookup)
                            if len(arch_refs) == 1 and lookup
                            else lookup.defn[-1] if lookup else None
                        )
                        name_of_links.append(decl_node) if decl_node else None
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
                if not isinstance(
                    valid_decl := decl_node.name_of, ast.AstImplNeedingNode
                ) or not (valid_decl.sym_tab and sym.decl.name_of.sym_tab):
                    raise self.ice(
                        f"Expected AstImplNeedingNode, got {valid_decl.__class__.__name__}. Not possible."
                    )
                valid_decl.body = sym.decl.name_of
                sym.decl.name_of.decl_link = valid_decl
                for idx, a in enumerate(sym.decl.name_of.target.archs):
                    a.name_spec.name_of = name_of_links[idx].name_of
                    a.name_spec.sym = name_of_links[idx].sym
                sym.decl.name_of.sym_tab.tab.update(valid_decl.sym_tab.tab)
                valid_decl.sym_tab.tab = sym.decl.name_of.sym_tab.tab
        for i in sym_tab.kid:
            self.connect_def_impl(i)
