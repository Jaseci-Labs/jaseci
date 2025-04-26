"""Connect Decls and Defs in AST.

This pass creates links in the ast between Decls of Architypes and Abilities
that are separate from their implementations (Defs). This pass creates a link
in the ast between the Decls and Defs of Architypes and Abilities through the
body field.
"""

import jaclang.compiler.unitree as uni
from jaclang.compiler.constant import Tokens as Tok
from jaclang.compiler.passes import AstPass
from jaclang.compiler.unitree import Symbol, UniScopeNode


class DeclImplMatchPass(AstPass):
    """Decls and Def matching pass."""

    def enter_module(self, node: uni.Module) -> None:
        """Enter module."""
        if not node.sym_tab:
            self.log_error(
                f"Expected symbol table on node {node.__class__.__name__}. Perhaps an earlier pass failed."
            )
        else:
            self.connect_def_impl(node.sym_tab)

    def defn_lookup(self, lookup: Symbol) -> uni.NameAtom | None:
        """Lookup a definition in a symbol table."""
        for defn in range(len(lookup.defn)):
            candidate = lookup.defn[len(lookup.defn) - (defn + 1)]
            if (
                isinstance(candidate.name_of, uni.AstImplNeedingNode)
                and candidate.name_of.needs_impl
            ):
                return candidate
        return None

    def connect_def_impl(self, sym_tab: UniScopeNode) -> None:
        """Connect Decls and Defs."""
        for sym in sym_tab.names_in_scope.values():
            if isinstance(sym.decl.name_of, uni.AstImplOnlyNode):
                # currently strips the type info from impls
                arch_refs = [x[3:] for x in sym.sym_name.split(".")]
                name_of_links: list[uni.NameAtom] = []  # to link archref names to decls
                lookup = sym_tab.lookup(arch_refs[0])
                # If below may need to be a while instead of if to skip over local
                # import name collisions (see test: test_impl_decl_resolution_fix)
                if lookup and not isinstance(
                    lookup.decl.name_of, uni.AstImplNeedingNode
                ):
                    lookup = (
                        sym_tab.parent_scope.lookup(arch_refs[0])
                        if sym_tab.parent_scope
                        else sym_tab.lookup(arch_refs[0])
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
                elif isinstance(decl_node, uni.Ability) and decl_node.is_abstract:
                    self.log_warning(
                        f"Abstract ability {decl_node.py_resolve_name()} should not have a definition.",
                        decl_node,
                    )
                    continue
                if not isinstance(
                    valid_decl := decl_node.name_of, uni.AstImplNeedingNode
                ) or not (valid_decl.sym_tab and sym.decl.name_of.sym_tab):
                    raise self.ice(
                        f"Expected AstImplNeedingNode, got {valid_decl.__class__.__name__}. Not possible."
                    )

                # Ensure if it's an ability def impl, the parameters are matched.
                self.validate_params_match(sym, decl_node.name_of)

                valid_decl.body = sym.decl.name_of
                sym.decl.name_of.decl_link = valid_decl
                for idx, a in enumerate(sym.decl.name_of.target.archs):
                    a.name_spec.name_of = name_of_links[idx].name_of
                    a.name_spec.sym = name_of_links[idx].sym
                sym.decl.name_of.sym_tab.names_in_scope.update(
                    valid_decl.sym_tab.names_in_scope
                )
                valid_decl.sym_tab.names_in_scope = (
                    sym.decl.name_of.sym_tab.names_in_scope
                )

        for i in sym_tab.kid_scope:
            self.connect_def_impl(i)

    def validate_params_match(self, sym: Symbol, valid_decl: uni.AstSymbolNode) -> None:
        """Validate if the parameters match."""
        if (
            isinstance(valid_decl, uni.Ability)
            and isinstance(sym.decl.name_of, uni.AbilityDef)
            and isinstance(valid_decl.signature, uni.FuncSignature)
            and isinstance(sym.decl.name_of.signature, uni.FuncSignature)
        ):

            params_decl = valid_decl.signature.params
            params_defn = sym.decl.name_of.signature.params

            if params_decl and params_defn:
                # Check if the parameter count is matched.
                if len(params_defn.items) != len(params_decl.items):
                    self.log_error(
                        f"Parameter count mismatch for ability {sym.sym_name}.",
                        sym.decl.name_of.name_spec,
                    )
                    self.log_error(
                        f"From the declaration of {valid_decl.name_spec.sym_name}.",
                        valid_decl.name_spec,
                    )
                else:
                    # Copy the parameter names from the declaration to the definition.
                    for idx in range(len(params_defn.items)):
                        params_decl.items[idx] = params_defn.items[idx]
                    for idx in range(len(params_defn.kid)):
                        params_decl.kid[idx] = params_defn.kid[idx]

    def exit_architype(self, node: uni.Architype) -> None:
        """Exit Architype."""
        if node.arch_type.name == Tok.KW_OBJECT and isinstance(
            node.body, uni.SubNodeList
        ):

            found_default_init = False
            for stmnt in node.body.items:
                if not isinstance(stmnt, uni.ArchHas):
                    continue
                for var in stmnt.vars.items:
                    if (var.value is not None) or (var.defer):
                        found_default_init = True
                    else:
                        if found_default_init:
                            self.log_error(
                                f"Non default attribute '{var.name.value}' follows default attribute",
                                node_override=var.name,
                            )
                            break

            post_init_vars: list[uni.HasVar] = []
            postinit_method: uni.Ability | None = None

            for item in node.body.items:

                if isinstance(item, uni.ArchHas):
                    for var in item.vars.items:
                        if var.defer:
                            post_init_vars.append(var)

                elif isinstance(item, uni.Ability):
                    if item.is_abstract:
                        continue
                    if (
                        isinstance(item.name_ref, uni.SpecialVarRef)
                        and item.name_ref.name == "KW_POST_INIT"
                    ):
                        postinit_method = item

            # Check if postinit needed and not provided.
            if len(post_init_vars) != 0 and (postinit_method is None):
                self.log_error(
                    'Missing "postinit" method required by un initialized attribute(s).',
                    node_override=post_init_vars[0].name_spec,
                )  # We show the error on the first uninitialized var.
