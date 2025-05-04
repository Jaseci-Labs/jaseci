"""Ast build pass for Jaseci Ast.

This pass adds a more complete set of symbols from the AST to the
symbol table. This includes assignments, parameters, arch ref chains,
and more. This pass also links the symbols in the AST to their corresponding
sybmols in the symbol table (including uses).
"""

import ast as ast3

import jaclang.compiler.unitree as uni
from jaclang.compiler.constant import Tokens as Tok
from jaclang.compiler.passes import UniPass


class DefUsePass(UniPass):
    """Jac Ast build pass."""

    def enter_architype(self, node: uni.Architype) -> None:
        node.sym_tab.inherit_baseclasses_sym(node)

        def inform_from_walker(node: uni.UniNode) -> None:
            for i in (
                node.get_all_sub_nodes(uni.VisitStmt)
                + node.get_all_sub_nodes(uni.IgnoreStmt)
                + node.get_all_sub_nodes(uni.DisengageStmt)
                + node.get_all_sub_nodes(uni.EdgeOpRef)
            ):
                i.from_walker = True

        if node.arch_type.name == Tok.KW_WALKER:
            inform_from_walker(node)
            for i in self.get_all_sub_nodes(node, uni.Ability):
                if isinstance(i.body, uni.AbilityDef):
                    inform_from_walker(i.body)

    def enter_enum(self, node: uni.Enum) -> None:
        node.sym_tab.inherit_baseclasses_sym(node)

    def enter_arch_ref(self, node: uni.ArchRef) -> None:
        node.sym_tab.use_lookup(node)

    def enter_arch_ref_chain(self, node: uni.ArchRefChain) -> None:
        node.sym_tab.chain_use_lookup(node.archs)

    def enter_param_var(self, node: uni.ParamVar) -> None:
        node.sym_tab.def_insert(node)

    def enter_has_var(self, node: uni.HasVar) -> None:
        if isinstance(node.parent, uni.SubNodeList) and isinstance(
            node.parent.parent, uni.ArchHas
        ):
            node.sym_tab.def_insert(
                node,
                single_decl="has var",
                access_spec=node.parent.parent,
            )
        else:
            self.ice("Inconsistency in AST, has var should be under arch has")

    def enter_assignment(self, node: uni.Assignment) -> None:
        for i in node.target.items:
            if isinstance(i, uni.AtomTrailer):
                i.sym_tab.chain_def_insert(i.as_attr_list)
            elif isinstance(i, uni.AstSymbolNode):
                i.sym_tab.def_insert(i)
            else:
                self.log_error("Assignment target not valid")

    def enter_inner_compr(self, node: uni.InnerCompr) -> None:
        if isinstance(node.target, uni.AtomTrailer):
            node.target.sym_tab.chain_def_insert(node.target.as_attr_list)
        elif isinstance(node.target, uni.AstSymbolNode):
            node.target.sym_tab.def_insert(node.target)
        else:
            self.log_error("Named target not valid")

    def enter_atom_trailer(self, node: uni.AtomTrailer) -> None:
        chain = node.as_attr_list
        node.sym_tab.chain_use_lookup(chain)

    def enter_special_var_ref(self, node: uni.SpecialVarRef) -> None:
        node.sym_tab.use_lookup(node)

    def enter_float(self, node: uni.Float) -> None:
        node.sym_tab.use_lookup(node)

    def enter_int(self, node: uni.Int) -> None:
        node.sym_tab.use_lookup(node)

    def enter_string(self, node: uni.String) -> None:
        node.sym_tab.use_lookup(node)

    def enter_bool(self, node: uni.Bool) -> None:
        node.sym_tab.use_lookup(node)

    def enter_builtin_type(self, node: uni.BuiltinType) -> None:
        node.sym_tab.use_lookup(node)

    def enter_name(self, node: uni.Name) -> None:
        if not isinstance(node.parent, uni.AtomTrailer):
            node.sym_tab.use_lookup(node)

    def enter_in_for_stmt(self, node: uni.InForStmt) -> None:
        if isinstance(node.target, uni.AtomTrailer):
            node.target.sym_tab.chain_def_insert(node.target.as_attr_list)
        elif isinstance(node.target, uni.AstSymbolNode):
            node.target.sym_tab.def_insert(node.target)
        else:
            self.log_error("For loop assignment target not valid")

    def enter_delete_stmt(self, node: uni.DeleteStmt) -> None:
        for i in node.py_ast_targets:
            if isinstance(i, uni.AtomTrailer):
                i.as_attr_list[-1].name_spec.py_ctx_func = ast3.Del
            elif isinstance(i, uni.AstSymbolNode):
                i.name_spec.py_ctx_func = ast3.Del
            else:
                self.log_error("Delete target not valid")

    def enter_expr_as_item(self, node: uni.ExprAsItem) -> None:
        if node.alias:
            if isinstance(node.alias, uni.AtomTrailer):
                node.alias.sym_tab.chain_def_insert(node.alias.as_attr_list)
            elif isinstance(node.alias, uni.AstSymbolNode):
                node.alias.sym_tab.def_insert(node.alias)
            else:
                self.log_error("For expr as target not valid")
