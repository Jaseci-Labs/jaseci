"""Symbol table tree build pass for Jaseci Ast.

This pass builds the symbol table tree for the Jaseci Ast. It also adds symbols
for globals, imports, architypes, and abilities declarations and definitions.
"""

import jaclang.compiler.unitree as uni
from jaclang.compiler.passes import UniPass
from jaclang.compiler.unitree import UniScopeNode


class SymTabBuildPass(UniPass):
    """Jac Symbol table build pass."""

    def before_pass(self) -> None:
        """Before pass."""
        self.cur_sym_tab: list[UniScopeNode] = []

    def push_scope_and_link(self, key_node: uni.UniScopeNode) -> None:
        """Push scope."""
        if not len(self.cur_sym_tab):
            self.cur_sym_tab.append(key_node)
        else:
            self.cur_sym_tab.append(self.cur_scope.link_kid_scope(key_node=key_node))

    def pop_scope(self) -> UniScopeNode:
        """Pop scope."""
        return self.cur_sym_tab.pop()

    @property
    def cur_scope(self) -> UniScopeNode:
        """Return current scope."""
        return self.cur_sym_tab[-1]

    def enter_module(self, node: uni.Module) -> None:
        self.push_scope_and_link(node)

    def exit_module(self, node: uni.Module) -> None:
        self.pop_scope()

    def enter_global_vars(self, node: uni.GlobalVars) -> None:
        pass

    def exit_global_vars(self, node: uni.GlobalVars) -> None:
        for i in self.get_all_sub_nodes(node, uni.Assignment):
            for j in i.target.items:
                if isinstance(j, uni.AstSymbolNode):
                    j.sym_tab.def_insert(j, access_spec=node, single_decl="global var")
                else:
                    self.ice("Expected name type for globabl vars")

    def enter_sub_tag(self, node: uni.SubTag) -> None:
        pass

    def enter_sub_node_list(self, node: uni.SubNodeList) -> None:
        pass

    def enter_test(self, node: uni.Test) -> None:
        self.push_scope_and_link(node)
        import unittest

        for i in [j for j in dir(unittest.TestCase()) if j.startswith("assert")]:
            node.sym_tab.def_insert(
                uni.Name.gen_stub_from_node(node, i, set_name_of=node)
            )

    def exit_test(self, node: uni.Test) -> None:
        self.pop_scope()

    def enter_module_code(self, node: uni.ModuleCode) -> None:
        # self.push_scope( node)
        pass

    def exit_module_code(self, node: uni.ModuleCode) -> None:
        # self.pop_scope()
        pass

    def enter_py_inline_code(self, node: uni.PyInlineCode) -> None:
        pass

    def enter_import(self, node: uni.Import) -> None:
        pass

    def enter_module_path(self, node: uni.ModulePath) -> None:
        pass

    def exit_module_path(self, node: uni.ModulePath) -> None:
        if node.alias:
            node.alias.sym_tab.def_insert(node.alias, single_decl="import")
        elif node.path and isinstance(node.path[0], uni.Name):
            if node.parent_of_type(uni.Import) and not (
                node.parent_of_type(uni.Import).from_loc
                and node.parent_of_type(uni.Import).is_jac
            ):
                node.path[0].sym_tab.def_insert(node.path[0])
        else:
            pass  # Need to support pythonic import symbols with dots in it

    def enter_module_item(self, node: uni.ModuleItem) -> None:
        pass

    def enter_architype(self, node: uni.Architype) -> None:
        self.push_scope_and_link(node)
        assert node.parent_scope is not None
        node.parent_scope.def_insert(node, access_spec=node, single_decl="architype")

    def exit_architype(self, node: uni.Architype) -> None:
        self.pop_scope()

    def enter_arch_def(self, node: uni.ArchDef) -> None:
        self.push_scope_and_link(node)
        assert node.parent_scope is not None
        node.parent_scope.def_insert(node, single_decl="arch def")

    def exit_arch_def(self, node: uni.ArchDef) -> None:
        self.pop_scope()

    def enter_ability(self, node: uni.Ability) -> None:
        self.push_scope_and_link(node)
        assert node.parent_scope is not None
        node.parent_scope.def_insert(node, access_spec=node, single_decl="ability")
        if node.is_method:
            node.sym_tab.def_insert(uni.Name.gen_stub_from_node(node, "self"))
            node.sym_tab.def_insert(
                uni.Name.gen_stub_from_node(
                    node, "super", set_name_of=node.owner_method
                )
            )

    def exit_ability(self, node: uni.Ability) -> None:
        self.pop_scope()

    def enter_ability_def(self, node: uni.AbilityDef) -> None:
        self.push_scope_and_link(node)
        assert node.parent_scope is not None
        node.parent_scope.def_insert(node, single_decl="ability def")

    def exit_ability_def(self, node: uni.AbilityDef) -> None:
        self.pop_scope()

    def enter_event_signature(self, node: uni.EventSignature) -> None:
        pass

    def enter_arch_ref_chain(self, node: uni.ArchRefChain) -> None:
        pass

    def enter_func_signature(self, node: uni.FuncSignature) -> None:
        pass

    def enter_param_var(self, node: uni.ParamVar) -> None:
        pass

    def enter_enum(self, node: uni.Enum) -> None:
        self.push_scope_and_link(node)
        assert node.parent_scope is not None
        node.parent_scope.def_insert(node, access_spec=node, single_decl="enum")

    def exit_enum(self, node: uni.Enum) -> None:
        self.pop_scope()

    def enter_enum_def(self, node: uni.EnumDef) -> None:
        self.push_scope_and_link(node)
        assert node.parent_scope is not None
        node.parent_scope.def_insert(node, single_decl="enum def")

    def exit_enum_def(self, node: uni.EnumDef) -> None:
        self.pop_scope()

    def enter_arch_has(self, node: uni.ArchHas) -> None:
        pass

    def enter_has_var(self, node: uni.HasVar) -> None:
        pass

    def enter_typed_ctx_block(self, node: uni.TypedCtxBlock) -> None:
        self.push_scope_and_link(node)

    def exit_typed_ctx_block(self, node: uni.TypedCtxBlock) -> None:
        self.pop_scope()

    def enter_if_stmt(self, node: uni.IfStmt) -> None:
        self.push_scope_and_link(node)

    def exit_if_stmt(self, node: uni.IfStmt) -> None:
        self.pop_scope()

    def enter_else_if(self, node: uni.ElseIf) -> None:
        self.push_scope_and_link(node)

    def exit_else_if(self, node: uni.ElseIf) -> None:
        self.pop_scope()

    def enter_else_stmt(self, node: uni.ElseStmt) -> None:
        self.push_scope_and_link(node)

    def exit_else_stmt(self, node: uni.ElseStmt) -> None:
        self.pop_scope()

    def enter_expr_stmt(self, node: uni.ExprStmt) -> None:
        pass

    def enter_try_stmt(self, node: uni.TryStmt) -> None:
        self.push_scope_and_link(node)

    def exit_try_stmt(self, node: uni.TryStmt) -> None:
        self.pop_scope()

    def enter_except(self, node: uni.Except) -> None:
        self.push_scope_and_link(node)

    def exit_except(self, node: uni.Except) -> None:
        self.pop_scope()

    def enter_finally_stmt(self, node: uni.FinallyStmt) -> None:
        self.push_scope_and_link(node)

    def exit_finally_stmt(self, node: uni.FinallyStmt) -> None:
        self.pop_scope()

    def enter_iter_for_stmt(self, node: uni.IterForStmt) -> None:
        self.push_scope_and_link(node)

    def exit_iter_for_stmt(self, node: uni.IterForStmt) -> None:
        self.pop_scope()

    def enter_in_for_stmt(self, node: uni.InForStmt) -> None:
        self.push_scope_and_link(node)

    def exit_in_for_stmt(self, node: uni.InForStmt) -> None:
        self.pop_scope()

    def enter_name(self, node: uni.Name) -> None:
        pass

    def enter_while_stmt(self, node: uni.WhileStmt) -> None:
        self.push_scope_and_link(node)

    def exit_while_stmt(self, node: uni.WhileStmt) -> None:
        self.pop_scope()

    def enter_with_stmt(self, node: uni.WithStmt) -> None:
        self.push_scope_and_link(node)

    def exit_with_stmt(self, node: uni.WithStmt) -> None:
        self.pop_scope()

    def enter_expr_as_item(self, node: uni.ExprAsItem) -> None:
        pass

    def enter_raise_stmt(self, node: uni.RaiseStmt) -> None:
        pass

    def enter_assert_stmt(self, node: uni.AssertStmt) -> None:
        pass

    def enter_check_stmt(self, node: uni.CheckStmt) -> None:
        pass

    def enter_ctrl_stmt(self, node: uni.CtrlStmt) -> None:
        pass

    def enter_delete_stmt(self, node: uni.DeleteStmt) -> None:
        pass

    def enter_report_stmt(self, node: uni.ReportStmt) -> None:
        pass

    def enter_return_stmt(self, node: uni.ReturnStmt) -> None:
        pass

    def enter_yield_expr(self, node: uni.YieldExpr) -> None:
        pass

    def enter_ignore_stmt(self, node: uni.IgnoreStmt) -> None:
        pass

    def enter_visit_stmt(self, node: uni.VisitStmt) -> None:
        pass

    def enter_revisit_stmt(self, node: uni.RevisitStmt) -> None:
        pass

    def enter_disengage_stmt(self, node: uni.DisengageStmt) -> None:
        pass

    def enter_await_expr(self, node: uni.AwaitExpr) -> None:
        pass

    def enter_global_stmt(self, node: uni.GlobalStmt) -> None:
        pass

    def enter_non_local_stmt(self, node: uni.NonLocalStmt) -> None:
        pass

    def enter_assignment(self, node: uni.Assignment) -> None:
        pass

    def enter_binary_expr(self, node: uni.BinaryExpr) -> None:
        pass

    def enter_compare_expr(self, node: uni.CompareExpr) -> None:
        pass

    def enter_if_else_expr(self, node: uni.IfElseExpr) -> None:
        pass

    def enter_unary_expr(self, node: uni.UnaryExpr) -> None:
        pass

    def enter_bool_expr(self, node: uni.BoolExpr) -> None:
        pass

    def enter_lambda_expr(self, node: uni.LambdaExpr) -> None:
        self.push_scope_and_link(node)

    def exit_lambda_expr(self, node: uni.LambdaExpr) -> None:
        self.pop_scope()

    def enter_multi_string(self, node: uni.MultiString) -> None:
        pass

    def enter_list_val(self, node: uni.ListVal) -> None:
        pass

    def enter_set_val(self, node: uni.SetVal) -> None:
        pass

    def enter_tuple_val(self, node: uni.TupleVal) -> None:
        pass

    def enter_dict_val(self, node: uni.DictVal) -> None:
        pass

    def enter_k_v_pair(self, node: uni.KVPair) -> None:
        pass

    def enter_k_w_pair(self, node: uni.KWPair) -> None:
        pass

    def enter_list_compr(self, node: uni.ListCompr) -> None:
        pass

    def enter_gen_compr(self, node: uni.GenCompr) -> None:
        pass

    def enter_set_compr(self, node: uni.SetCompr) -> None:
        pass

    def enter_inner_compr(self, node: uni.InnerCompr) -> None:
        self.push_scope_and_link(node)

    def exit_inner_compr(self, node: uni.InnerCompr) -> None:
        self.pop_scope()

    def enter_dict_compr(self, node: uni.DictCompr) -> None:
        self.push_scope_and_link(node)

    def exit_dict_compr(self, node: uni.DictCompr) -> None:
        self.pop_scope()

    def enter_atom_trailer(self, node: uni.AtomTrailer) -> None:
        pass

    def enter_atom_unit(self, node: uni.AtomUnit) -> None:
        pass

    def enter_func_call(self, node: uni.FuncCall) -> None:
        pass

    def enter_index_slice(self, node: uni.IndexSlice) -> None:
        pass

    def enter_arch_ref(self, node: uni.ArchRef) -> None:
        pass

    def enter_special_var_ref(self, node: uni.SpecialVarRef) -> None:
        pass

    def enter_edge_ref_trailer(self, node: uni.EdgeRefTrailer) -> None:
        pass

    def enter_edge_op_ref(self, node: uni.EdgeOpRef) -> None:
        pass

    def enter_disconnect_op(self, node: uni.DisconnectOp) -> None:
        pass

    def enter_connect_op(self, node: uni.ConnectOp) -> None:
        pass

    def enter_filter_compr(self, node: uni.FilterCompr) -> None:
        pass

    def enter_assign_compr(self, node: uni.AssignCompr) -> None:
        pass

    def enter_f_string(self, node: uni.FString) -> None:
        pass

    def enter_match_stmt(self, node: uni.MatchStmt) -> None:
        pass

    def enter_match_case(self, node: uni.MatchCase) -> None:
        self.push_scope_and_link(node)

    def exit_match_case(self, node: uni.MatchCase) -> None:
        self.pop_scope()

    def enter_match_or(self, node: uni.MatchOr) -> None:
        pass

    def enter_match_as(self, node: uni.MatchAs) -> None:
        pass

    def enter_match_wild(self, node: uni.MatchWild) -> None:
        pass

    def enter_match_value(self, node: uni.MatchValue) -> None:
        pass

    def enter_match_singleton(self, node: uni.MatchSingleton) -> None:
        pass

    def enter_match_sequence(self, node: uni.MatchSequence) -> None:
        pass

    def enter_match_mapping(self, node: uni.MatchMapping) -> None:
        pass

    def enter_match_k_v_pair(self, node: uni.MatchKVPair) -> None:
        pass

    def enter_match_star(self, node: uni.MatchStar) -> None:
        pass

    def enter_match_arch(self, node: uni.MatchArch) -> None:
        pass

    def enter_token(self, node: uni.Token) -> None:
        pass

    def enter_float(self, node: uni.Float) -> None:
        pass

    def enter_int(self, node: uni.Int) -> None:
        pass

    def enter_string(self, node: uni.String) -> None:
        pass

    def enter_bool(self, node: uni.Bool) -> None:
        pass

    def enter_null(self, node: uni.Null) -> None:
        pass

    def enter_ellipsis(self, node: uni.Ellipsis) -> None:
        pass

    def enter_builtin_type(self, node: uni.BuiltinType) -> None:
        pass

    def enter_semi(self, node: uni.Semi) -> None:
        pass

    def enter_comment_token(self, node: uni.CommentToken) -> None:
        pass
