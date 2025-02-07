"""Symbol table tree build pass for Jaseci Ast.

This pass builds the symbol table tree for the Jaseci Ast. It also adds symbols
for globals, imports, architypes, and abilities declarations and definitions.
"""

from typing import TypeVar

import jaclang.compiler.absyntree as ast
from jaclang.compiler.passes import Pass
from jaclang.compiler.symtable import SymbolTable


class SymTabBuildPass(Pass):
    """Jac Symbol table build pass."""

    def before_pass(self) -> None:
        self.cur_sym_tab: list[SymbolTable] = []

    def push_scope(self, name: str, key_node: ast.AstNode) -> None:
        inherit = key_node.parent

        if not len(self.cur_sym_tab) and not inherit:
            self.cur_sym_tab.append(SymbolTable(name, key_node))
        elif not len(self.cur_sym_tab) and inherit:
            self.cur_sym_tab.append(inherit.sym_tab)
            self.cur_sym_tab.append(self.cur_scope.push_kid_scope(name, key_node))
        else:
            self.cur_sym_tab.append(self.cur_scope.push_kid_scope(name, key_node))

    def pop_scope(self) -> SymbolTable:
        return self.cur_sym_tab.pop()

    @property
    def cur_scope(self) -> SymbolTable:
        return self.cur_sym_tab[-1]

    def sync_node_to_scope(self, node: ast.AstNode) -> None:
        node.sym_tab = self.cur_scope

    def enter_module(self, node: ast.Module) -> None:
        self.push_scope(node.name, node)
        self.sync_node_to_scope(node)

    def exit_module(self, node: ast.Module) -> None:
        self.pop_scope()

    def enter_global_vars(self, node: ast.GlobalVars) -> None:
        self.sync_node_to_scope(node)

    def exit_global_vars(self, node: ast.GlobalVars) -> None:
        for i in self.get_all_sub_nodes(node, ast.Assignment):
            for j in i.target.items:
                if isinstance(j, ast.AstSymbolNode):
                    j.sym_tab.def_insert(j, access_spec=node, single_decl="global var")
                else:
                    self.ice("Expected name type for globabl vars")

    def enter_sub_tag(self, node: ast.SubTag) -> None:
        self.sync_node_to_scope(node)

    def enter_sub_node_list(self, node: ast.SubNodeList) -> None:
        self.sync_node_to_scope(node)

    def enter_test(self, node: ast.Test) -> None:
        self.push_scope(node.sym_name, node)
        self.sync_node_to_scope(node)
        import unittest

        for i in [j for j in dir(unittest.TestCase()) if j.startswith("assert")]:
            node.sym_tab.def_insert(
                ast.Name.gen_stub_from_node(node, i, set_name_of=node)
            )

    def exit_test(self, node: ast.Test) -> None:
        self.pop_scope()

    def enter_module_code(self, node: ast.ModuleCode) -> None:
        # self.push_scope("module_code", node)
        self.sync_node_to_scope(node)

    def exit_module_code(self, node: ast.ModuleCode) -> None:
        pass  # self.pop_scope()

    def enter_py_inline_code(self, node: ast.PyInlineCode) -> None:
        self.sync_node_to_scope(node)

    def enter_import(self, node: ast.Import) -> None:
        self.sync_node_to_scope(node)

    def exit_import(self, node: ast.Import) -> None:
        if not node.is_absorb:
            for i in node.items.items:
                i.sym_tab.def_insert(i, single_decl="import item")
        elif node.is_absorb and node.is_jac:
            source = node.items.items[0]
            if not isinstance(source, ast.ModulePath) or not source.sub_module:
                self.error(
                    f"Module {node.from_loc.dot_path_str if node.from_loc else 'from location'}"
                    f" not found to include *, or ICE occurred!"
                )
            else:
                node.sym_tab.inherit_sym_tab(source.sub_module.sym_tab)

    def enter_module_path(self, node: ast.ModulePath) -> None:
        self.sync_node_to_scope(node)

    def exit_module_path(self, node: ast.ModulePath) -> None:
        if node.alias:
            node.alias.sym_tab.def_insert(node.alias, single_decl="import")
        elif node.path and isinstance(node.path[0], ast.Name):
            node.path[0].sym_tab.def_insert(node.path[0])
        else:
            pass  # Need to support pythonic import symbols with dots in it

    def enter_module_item(self, node: ast.ModuleItem) -> None:
        self.sync_node_to_scope(node)

    def enter_architype(self, node: ast.Architype) -> None:
        self.sync_node_to_scope(node)
        node.sym_tab.def_insert(node, access_spec=node, single_decl="architype")
        self.push_scope(node.name.value, node)
        self.sync_node_to_scope(node)

    def exit_architype(self, node: ast.Architype) -> None:
        self.pop_scope()

    def enter_arch_def(self, node: ast.ArchDef) -> None:
        self.sync_node_to_scope(node)
        node.sym_tab.def_insert(node, single_decl="arch def")
        self.push_scope(node.sym_name, node)
        self.sync_node_to_scope(node)

    def exit_arch_def(self, node: ast.ArchDef) -> None:
        self.pop_scope()

    def enter_ability(self, node: ast.Ability) -> None:
        self.sync_node_to_scope(node)
        node.sym_tab.def_insert(node, access_spec=node, single_decl="ability")
        self.push_scope(node.sym_name, node)
        self.sync_node_to_scope(node)
        if node.is_method:
            node.sym_tab.def_insert(ast.Name.gen_stub_from_node(node, "self"))
            node.sym_tab.def_insert(
                ast.Name.gen_stub_from_node(
                    node, "super", set_name_of=node.owner_method
                )
            )

    def exit_ability(self, node: ast.Ability) -> None:
        self.pop_scope()

    def enter_ability_def(self, node: ast.AbilityDef) -> None:
        self.sync_node_to_scope(node)
        node.sym_tab.def_insert(node, single_decl="ability def")
        self.push_scope(node.sym_name, node)
        self.sync_node_to_scope(node)

    def exit_ability_def(self, node: ast.AbilityDef) -> None:
        self.pop_scope()

    def enter_event_signature(self, node: ast.EventSignature) -> None:
        self.sync_node_to_scope(node)

    def enter_arch_ref_chain(self, node: ast.ArchRefChain) -> None:
        self.sync_node_to_scope(node)

    def enter_func_signature(self, node: ast.FuncSignature) -> None:
        self.sync_node_to_scope(node)

    def enter_param_var(self, node: ast.ParamVar) -> None:
        self.sync_node_to_scope(node)

    def enter_enum(self, node: ast.Enum) -> None:
        self.sync_node_to_scope(node)
        node.sym_tab.def_insert(node, access_spec=node, single_decl="enum")
        self.push_scope(node.sym_name, node)
        self.sync_node_to_scope(node)

    def exit_enum(self, node: ast.Enum) -> None:
        self.pop_scope()

    def enter_enum_def(self, node: ast.EnumDef) -> None:
        self.sync_node_to_scope(node)
        node.sym_tab.def_insert(node, single_decl="enum def")
        self.push_scope(node.sym_name, node)
        self.sync_node_to_scope(node)

    def exit_enum_def(self, node: ast.EnumDef) -> None:
        self.pop_scope()

    def enter_arch_has(self, node: ast.ArchHas) -> None:
        self.sync_node_to_scope(node)

    def enter_has_var(self, node: ast.HasVar) -> None:
        self.sync_node_to_scope(node)

    def enter_typed_ctx_block(self, node: ast.TypedCtxBlock) -> None:
        self.push_scope(f"{node.__class__.__name__}", node)
        self.sync_node_to_scope(node)

    def exit_typed_ctx_block(self, node: ast.TypedCtxBlock) -> None:
        self.pop_scope()

    def enter_if_stmt(self, node: ast.IfStmt) -> None:
        self.push_scope(f"{node.__class__.__name__}", node)
        self.sync_node_to_scope(node)

    def exit_if_stmt(self, node: ast.IfStmt) -> None:
        self.pop_scope()

    def enter_else_if(self, node: ast.ElseIf) -> None:
        self.push_scope("elif_stmt", node)
        self.sync_node_to_scope(node)

    def exit_else_if(self, node: ast.ElseIf) -> None:
        self.pop_scope()

    def enter_else_stmt(self, node: ast.ElseStmt) -> None:
        self.push_scope(f"{node.__class__.__name__}", node)
        self.sync_node_to_scope(node)

    def exit_else_stmt(self, node: ast.ElseStmt) -> None:
        self.pop_scope()

    def enter_expr_stmt(self, node: ast.ExprStmt) -> None:
        self.sync_node_to_scope(node)

    def enter_try_stmt(self, node: ast.TryStmt) -> None:
        self.push_scope(f"{node.__class__.__name__}", node)
        self.sync_node_to_scope(node)

    def exit_try_stmt(self, node: ast.TryStmt) -> None:
        self.pop_scope()

    def enter_except(self, node: ast.Except) -> None:
        self.push_scope(f"{node.__class__.__name__}", node)
        self.sync_node_to_scope(node)

    def exit_except(self, node: ast.Except) -> None:
        self.pop_scope()

    def enter_finally_stmt(self, node: ast.FinallyStmt) -> None:
        self.push_scope(f"{node.__class__.__name__}", node)
        self.sync_node_to_scope(node)

    def exit_finally_stmt(self, node: ast.FinallyStmt) -> None:
        self.pop_scope()

    def enter_iter_for_stmt(self, node: ast.IterForStmt) -> None:
        self.push_scope(f"{node.__class__.__name__}", node)
        self.sync_node_to_scope(node)

    def exit_iter_for_stmt(self, node: ast.IterForStmt) -> None:
        self.pop_scope()

    def enter_in_for_stmt(self, node: ast.InForStmt) -> None:
        self.push_scope(f"{node.__class__.__name__}", node)
        self.sync_node_to_scope(node)

    def exit_in_for_stmt(self, node: ast.InForStmt) -> None:
        self.pop_scope()

    def enter_name(self, node: ast.Name) -> None:
        self.sync_node_to_scope(node)

    def enter_while_stmt(self, node: ast.WhileStmt) -> None:
        self.push_scope(f"{node.__class__.__name__}", node)
        self.sync_node_to_scope(node)

    def exit_while_stmt(self, node: ast.WhileStmt) -> None:
        self.pop_scope()

    def enter_with_stmt(self, node: ast.WithStmt) -> None:
        self.push_scope(f"{node.__class__.__name__}", node)
        self.sync_node_to_scope(node)

    def exit_with_stmt(self, node: ast.WithStmt) -> None:
        self.pop_scope()

    def enter_expr_as_item(self, node: ast.ExprAsItem) -> None:
        self.sync_node_to_scope(node)

    def enter_raise_stmt(self, node: ast.RaiseStmt) -> None:
        self.sync_node_to_scope(node)

    def enter_assert_stmt(self, node: ast.AssertStmt) -> None:
        self.sync_node_to_scope(node)

    def enter_check_stmt(self, node: ast.CheckStmt) -> None:
        self.sync_node_to_scope(node)

    def enter_ctrl_stmt(self, node: ast.CtrlStmt) -> None:
        self.sync_node_to_scope(node)

    def enter_delete_stmt(self, node: ast.DeleteStmt) -> None:
        self.sync_node_to_scope(node)

    def enter_report_stmt(self, node: ast.ReportStmt) -> None:
        self.sync_node_to_scope(node)

    def enter_return_stmt(self, node: ast.ReturnStmt) -> None:
        self.sync_node_to_scope(node)

    def enter_yield_expr(self, node: ast.YieldExpr) -> None:
        self.sync_node_to_scope(node)

    def enter_ignore_stmt(self, node: ast.IgnoreStmt) -> None:
        self.sync_node_to_scope(node)

    def enter_visit_stmt(self, node: ast.VisitStmt) -> None:
        self.sync_node_to_scope(node)

    def enter_revisit_stmt(self, node: ast.RevisitStmt) -> None:
        self.sync_node_to_scope(node)

    def enter_disengage_stmt(self, node: ast.DisengageStmt) -> None:
        self.sync_node_to_scope(node)

    def enter_await_expr(self, node: ast.AwaitExpr) -> None:
        self.sync_node_to_scope(node)

    def enter_global_stmt(self, node: ast.GlobalStmt) -> None:
        self.sync_node_to_scope(node)

    def enter_non_local_stmt(self, node: ast.NonLocalStmt) -> None:
        self.sync_node_to_scope(node)

    def enter_assignment(self, node: ast.Assignment) -> None:
        self.sync_node_to_scope(node)

    def enter_binary_expr(self, node: ast.BinaryExpr) -> None:
        self.sync_node_to_scope(node)

    def enter_compare_expr(self, node: ast.CompareExpr) -> None:
        self.sync_node_to_scope(node)

    def enter_if_else_expr(self, node: ast.IfElseExpr) -> None:
        self.sync_node_to_scope(node)

    def enter_unary_expr(self, node: ast.UnaryExpr) -> None:
        self.sync_node_to_scope(node)

    def enter_bool_expr(self, node: ast.BoolExpr) -> None:
        self.sync_node_to_scope(node)

    def enter_lambda_expr(self, node: ast.LambdaExpr) -> None:
        self.push_scope(f"{node.__class__.__name__}", node)
        self.sync_node_to_scope(node)

    def exit_lambda_expr(self, node: ast.LambdaExpr) -> None:
        self.pop_scope()

    def enter_multi_string(self, node: ast.MultiString) -> None:
        self.sync_node_to_scope(node)

    def enter_list_val(self, node: ast.ListVal) -> None:
        self.sync_node_to_scope(node)

    def enter_set_val(self, node: ast.SetVal) -> None:
        self.sync_node_to_scope(node)

    def enter_tuple_val(self, node: ast.TupleVal) -> None:
        self.sync_node_to_scope(node)

    def enter_dict_val(self, node: ast.DictVal) -> None:
        self.sync_node_to_scope(node)

    def enter_k_v_pair(self, node: ast.KVPair) -> None:
        self.sync_node_to_scope(node)

    def enter_k_w_pair(self, node: ast.KWPair) -> None:
        self.sync_node_to_scope(node)

    def enter_list_compr(self, node: ast.ListCompr) -> None:
        self.sync_node_to_scope(node)

    def enter_gen_compr(self, node: ast.GenCompr) -> None:
        self.sync_node_to_scope(node)

    def enter_set_compr(self, node: ast.SetCompr) -> None:
        self.sync_node_to_scope(node)

    def enter_inner_compr(self, node: ast.InnerCompr) -> None:
        self.push_scope(f"{node.__class__.__name__}", node)
        self.sync_node_to_scope(node)

    def exit_inner_compr(self, node: ast.InnerCompr) -> None:
        self.pop_scope()

    def enter_dict_compr(self, node: ast.DictCompr) -> None:
        self.push_scope(f"{node.__class__.__name__}", node)
        self.sync_node_to_scope(node)

    def exit_dict_compr(self, node: ast.DictCompr) -> None:
        self.pop_scope()

    def enter_atom_trailer(self, node: ast.AtomTrailer) -> None:
        self.sync_node_to_scope(node)

    def enter_atom_unit(self, node: ast.AtomUnit) -> None:
        self.sync_node_to_scope(node)

    def enter_func_call(self, node: ast.FuncCall) -> None:
        self.sync_node_to_scope(node)

    def enter_index_slice(self, node: ast.IndexSlice) -> None:
        self.sync_node_to_scope(node)

    def enter_arch_ref(self, node: ast.ArchRef) -> None:
        self.sync_node_to_scope(node)

    def enter_special_var_ref(self, node: ast.SpecialVarRef) -> None:
        self.sync_node_to_scope(node)

    def enter_edge_ref_trailer(self, node: ast.EdgeRefTrailer) -> None:
        self.sync_node_to_scope(node)

    def enter_edge_op_ref(self, node: ast.EdgeOpRef) -> None:
        self.sync_node_to_scope(node)

    def enter_disconnect_op(self, node: ast.DisconnectOp) -> None:
        self.sync_node_to_scope(node)

    def enter_connect_op(self, node: ast.ConnectOp) -> None:
        self.sync_node_to_scope(node)

    def enter_filter_compr(self, node: ast.FilterCompr) -> None:
        self.sync_node_to_scope(node)

    def enter_assign_compr(self, node: ast.AssignCompr) -> None:
        self.sync_node_to_scope(node)

    def enter_f_string(self, node: ast.FString) -> None:
        self.sync_node_to_scope(node)

    def enter_match_stmt(self, node: ast.MatchStmt) -> None:
        self.sync_node_to_scope(node)

    def enter_match_case(self, node: ast.MatchCase) -> None:
        self.push_scope(f"{node.__class__.__name__}", node)
        self.sync_node_to_scope(node)

    def exit_match_case(self, node: ast.MatchCase) -> None:
        self.pop_scope()

    def enter_match_or(self, node: ast.MatchOr) -> None:
        self.sync_node_to_scope(node)

    def enter_match_as(self, node: ast.MatchAs) -> None:
        self.sync_node_to_scope(node)

    def enter_match_wild(self, node: ast.MatchWild) -> None:
        self.sync_node_to_scope(node)

    def enter_match_value(self, node: ast.MatchValue) -> None:
        self.sync_node_to_scope(node)

    def enter_match_singleton(self, node: ast.MatchSingleton) -> None:
        self.sync_node_to_scope(node)

    def enter_match_sequence(self, node: ast.MatchSequence) -> None:
        self.sync_node_to_scope(node)

    def enter_match_mapping(self, node: ast.MatchMapping) -> None:
        self.sync_node_to_scope(node)

    def enter_match_k_v_pair(self, node: ast.MatchKVPair) -> None:
        self.sync_node_to_scope(node)

    def enter_match_star(self, node: ast.MatchStar) -> None:
        self.sync_node_to_scope(node)

    def enter_match_arch(self, node: ast.MatchArch) -> None:
        self.sync_node_to_scope(node)

    def enter_token(self, node: ast.Token) -> None:
        self.sync_node_to_scope(node)

    def enter_float(self, node: ast.Float) -> None:
        self.sync_node_to_scope(node)

    def enter_int(self, node: ast.Int) -> None:
        self.sync_node_to_scope(node)

    def enter_string(self, node: ast.String) -> None:
        self.sync_node_to_scope(node)

    def enter_bool(self, node: ast.Bool) -> None:
        self.sync_node_to_scope(node)

    def enter_null(self, node: ast.Null) -> None:
        self.sync_node_to_scope(node)

    def enter_ellipsis(self, node: ast.Ellipsis) -> None:
        self.sync_node_to_scope(node)

    def enter_builtin_type(self, node: ast.BuiltinType) -> None:
        self.sync_node_to_scope(node)

    def enter_semi(self, node: ast.Semi) -> None:
        self.sync_node_to_scope(node)

    def enter_comment_token(self, node: ast.CommentToken) -> None:
        self.sync_node_to_scope(node)


T = TypeVar("T", bound=ast.AstNode)


class PyInspectSymTabBuildPass(SymTabBuildPass):
    """Jac Symbol table build pass."""

    def push_scope(self, name: str, key_node: ast.AstNode) -> None:
        if not len(self.cur_sym_tab):
            self.cur_sym_tab.append(SymbolTable(name, key_node))
        else:
            self.cur_sym_tab.append(self.cur_scope.push_kid_scope(name, key_node))
