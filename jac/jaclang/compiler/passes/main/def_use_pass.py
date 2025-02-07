"""Ast build pass for Jaseci Ast.

This pass adds a more complete set of symbols from the AST to the
symbol table. This includes assignments, parameters, arch ref chains,
and more. This pass also links the symbols in the AST to their corresponding
sybmols in the symbol table (including uses).
"""

import ast as ast3

import jaclang.compiler.absyntree as ast
from jaclang.compiler.constant import Tokens as Tok
from jaclang.compiler.passes import Pass


class DefUsePass(Pass):

    def after_pass(self) -> None:
        pass

    def enter_architype(self, node: ast.Architype) -> None:
        node.sym_tab.inherit_baseclasses_sym(node)

        def inform_from_walker(node: ast.AstNode) -> None:
            for i in (
                node.get_all_sub_nodes(ast.VisitStmt)
                + node.get_all_sub_nodes(ast.IgnoreStmt)
                + node.get_all_sub_nodes(ast.DisengageStmt)
                + node.get_all_sub_nodes(ast.EdgeOpRef)
            ):
                i.from_walker = True

        if node.arch_type.name == Tok.KW_WALKER:
            inform_from_walker(node)
            for i in self.get_all_sub_nodes(node, ast.Ability):
                if isinstance(i.body, ast.AbilityDef):
                    inform_from_walker(i.body)

    def enter_enum(self, node: ast.Enum) -> None:
        node.sym_tab.inherit_baseclasses_sym(node)

    def enter_arch_ref(self, node: ast.ArchRef) -> None:
        node.sym_tab.use_lookup(node)

    def enter_arch_ref_chain(self, node: ast.ArchRefChain) -> None:
        node.sym_tab.chain_use_lookup(node.archs)

    def enter_param_var(self, node: ast.ParamVar) -> None:
        node.sym_tab.def_insert(node)

    def enter_has_var(self, node: ast.HasVar) -> None:
        if isinstance(node.parent, ast.SubNodeList) and isinstance(
            node.parent.parent, ast.ArchHas
        ):
            node.sym_tab.def_insert(
                node,
                single_decl="has var",
                access_spec=node.parent.parent,
            )
        else:
            self.ice("Inconsistency in AST, has var should be under arch has")

    def enter_assignment(self, node: ast.Assignment) -> None:
        for i in node.target.items:
            if isinstance(i, ast.AtomTrailer):
                i.sym_tab.chain_def_insert(i.as_attr_list)
            elif isinstance(i, ast.AstSymbolNode):
                i.sym_tab.def_insert(i)
            else:
                self.error("Assignment target not valid")

    def enter_inner_compr(self, node: ast.InnerCompr) -> None:
        if isinstance(node.target, ast.AtomTrailer):
            node.target.sym_tab.chain_def_insert(node.target.as_attr_list)
        elif isinstance(node.target, ast.AstSymbolNode):
            node.target.sym_tab.def_insert(node.target)
        else:
            self.error("Named target not valid")

    def enter_atom_trailer(self, node: ast.AtomTrailer) -> None:
        chain = node.as_attr_list
        node.sym_tab.chain_use_lookup(chain)

    def enter_func_call(self, node: ast.FuncCall) -> None:
        pass

    def enter_index_slice(self, node: ast.IndexSlice) -> None:
        pass

    def enter_special_var_ref(self, node: ast.SpecialVarRef) -> None:
        node.sym_tab.use_lookup(node)

    def enter_edge_op_ref(self, node: ast.EdgeOpRef) -> None:
        pass

    def enter_disconnect_op(self, node: ast.DisconnectOp) -> None:
        pass

    def enter_connect_op(self, node: ast.ConnectOp) -> None:
        pass

    def enter_filter_compr(self, node: ast.FilterCompr) -> None:
        pass

    def enter_token(self, node: ast.Token) -> None:
        pass

    def enter_float(self, node: ast.Float) -> None:
        node.sym_tab.use_lookup(node)

    def enter_int(self, node: ast.Int) -> None:
        node.sym_tab.use_lookup(node)

    def enter_string(self, node: ast.String) -> None:
        node.sym_tab.use_lookup(node)

    def enter_bool(self, node: ast.Bool) -> None:
        node.sym_tab.use_lookup(node)

    def enter_builtin_type(self, node: ast.BuiltinType) -> None:
        node.sym_tab.use_lookup(node)

    def enter_name(self, node: ast.Name) -> None:
        if not isinstance(node.parent, ast.AtomTrailer):
            node.sym_tab.use_lookup(node)

    def enter_in_for_stmt(self, node: ast.InForStmt) -> None:
        if isinstance(node.target, ast.AtomTrailer):
            node.target.sym_tab.chain_def_insert(node.target.as_attr_list)
        elif isinstance(node.target, ast.AstSymbolNode):
            node.target.sym_tab.def_insert(node.target)
        else:
            self.error("For loop assignment target not valid")

    def enter_delete_stmt(self, node: ast.DeleteStmt) -> None:
        items = (
            node.target.values.items
            if isinstance(node.target, ast.TupleVal) and node.target.values
            else [node.target]
        )
        for i in items:
            if isinstance(i, ast.AtomTrailer):
                i.as_attr_list[-1].name_spec.py_ctx_func = ast3.Del
            elif isinstance(i, ast.AstSymbolNode):
                i.name_spec.py_ctx_func = ast3.Del
            else:
                self.error("Delete target not valid")

    def enter_expr_as_item(self, node: ast.ExprAsItem) -> None:
        if node.alias:
            if isinstance(node.alias, ast.AtomTrailer):
                node.alias.sym_tab.chain_def_insert(node.alias.as_attr_list)
            elif isinstance(node.alias, ast.AstSymbolNode):
                node.alias.sym_tab.def_insert(node.alias)
            else:
                self.error("For expr as target not valid")
