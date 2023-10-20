"""Ast build pass for Jaseci Ast."""
from typing import Optional

import jaclang.jac.absyntree as ast
from jaclang.jac.passes import Pass

# from jaclang.jac.symtable import SymbolHitType as Sht, SymbolType as St


class DefUsePass(Pass):
    """Jac Ast build pass."""

    def before_pass(self) -> None:
        """Before pass."""
        self.marked: list[ast.AstSymbolNode] = []

    def already_declared_err(
        self,
        name: str,
        typ: str,
        original: ast.AstNode,
        other_nodes: Optional[list[ast.AstNode]] = None,
    ) -> None:
        """Already declared error."""
        mod_path = (
            original.mod_link.rel_mod_path
            if original.mod_link
            else self.ice("Mod_link unknown")
        )
        err_msg = (
            f"Name used for {typ} '{name}' already declared at "
            f"{mod_path}, line {original.loc.first_line}"
        )
        if other_nodes:
            for i in other_nodes:
                mod_path = (
                    i.mod_link.rel_mod_path
                    if i.mod_link
                    else self.ice("Mod_link unknown")
                )
                err_msg += f", also see {mod_path}, line {i.loc.first_line}"
        self.warning(err_msg)

    def exit_global_vars(self, node: ast.GlobalVars) -> None:
        """Sub objects.

        access: Optional[SubTag[Token]],
        assignments: SubNodeList[Assignment],
        is_frozen: bool,
        doc: Optional[Constant],
        """
        # for i in node.assignments.items:
        #     node.sym_tab.lookup()

    def exit_sub_tag(self, node: ast.SubTag) -> None:
        """Sub objects.

        tag: T,
        """

    def exit_sub_node_list(self, node: ast.SubNodeList) -> None:
        """Sub objects.

        items: list[T],
        """

    def exit_test(self, node: ast.Test) -> None:
        """Sub objects.

        name: Name | Token,
        body: SubNodeList[CodeBlockStmt],
        doc: Optional[Constant],
        """

    def exit_module_code(self, node: ast.ModuleCode) -> None:
        """Sub objects.

        name: Optional[SubTag[Name]],
        body: SubNodeList[CodeBlockStmt],
        doc: Optional[Constant],
        """

    def exit_py_inline_code(self, node: ast.PyInlineCode) -> None:
        """Sub objects.

        code: Token,
        doc: Optional[Constant],
        """

    def exit_import(self, node: ast.Import) -> None:
        """Sub objects.

        lang: SubTag[Name],
        path: ModulePath,
        alias: Optional[Name],
        items: Optional[SubNodeList[ModuleItem]],
        is_absorb: bool,
        doc: Optional[Constant],
        sub_module: Optional[Module],
        """

    def exit_module_path(self, node: ast.ModulePath) -> None:
        """Sub objects.

        path: list[Token],
        """

    def exit_module_item(self, node: ast.ModuleItem) -> None:
        """Sub objects.

        name: Name,
        alias: Optional[Name],
        body: Optional[AstNode],
        """

    def exit_architype(self, node: ast.Architype) -> None:
        """Sub objects.

        name: Name,
        arch_type: Token,
        access: Optional[SubTag[Token]],
        base_classes: Optional[SubNodeList[SubTag[SubNodeList[NameType]]]],
        body: Optional[SubNodeList[ArchBlockStmt] | ArchDef],
        doc: Optional[Constant],
        decorators: Optional[SubNodeList[ExprType]],
        """

    def exit_arch_def(self, node: ast.ArchDef) -> None:
        """Sub objects.

        target: ArchRefChain,
        body: SubNodeList[ArchBlockStmt],
        doc: Optional[Constant],
        decorators: Optional[SubNodeList[ExprType]],
        """

    def exit_enum(self, node: ast.Enum) -> None:
        """Sub objects.

        name: Name,
        access: Optional[SubTag[Token]],
        base_classes: Optional[SubNodeList[SubTag[SubNodeList[NameType]]]],
        body: Optional[SubNodeList[EnumBlockStmt] | EnumDef],
        doc: Optional[Constant],
        decorators: Optional[SubNodeList[ExprType]],
        """

    def exit_enum_def(self, node: ast.EnumDef) -> None:
        """Sub objects.

        target: ArchRefChain,
        body: SubNodeList[EnumBlockStmt],
        doc: Optional[Constant],
        decorators: Optional[SubNodeList[ExprType]],
        """

    def exit_ability(self, node: ast.Ability) -> None:
        """Sub objects.

        name_ref: NameType,
        is_func: bool,
        is_async: bool,
        is_static: bool,
        is_abstract: bool,
        access: Optional[SubTag[Token]],
        signature: Optional[FuncSignature | SubNodeList[TypeSpec] | EventSignature],
        body: Optional[SubNodeList[CodeBlockStmt]],
        arch_attached: Optional[Architype],
        doc: Optional[Constant],
        decorators: Optional[SubNodeList[ExprType]],
        """

    def exit_ability_def(self, node: ast.AbilityDef) -> None:
        """Sub objects.

        target: ArchRefChain,
        signature: FuncSignature | EventSignature,
        body: SubNodeList[CodeBlockStmt],
        doc: Optional[Constant],
        decorators: Optional[SubNodeList[ExprType]],
        """

    def exit_func_signature(self, node: ast.FuncSignature) -> None:
        """Sub objects.

        params: Optional[SubNodeList[ParamVar]],
        return_type: Optional[SubNodeList[TypeSpec]],
        """

    def exit_event_signature(self, node: ast.EventSignature) -> None:
        """Sub objects.

        event: Token,
        arch_tag_info: Optional[SubNodeList[TypeSpec]],
        return_type: Optional[SubTag[SubNodeList[TypeSpec]]],
        """

    def exit_arch_ref(self, node: ast.ArchRef) -> None:
        """Sub objects.

        name_ref: NameType,
        arch: Token,
        """

    def exit_arch_ref_chain(self, node: ast.ArchRefChain) -> None:
        """Sub objects.

        archs: list[ArchRef],
        """

    def exit_param_var(self, node: ast.ParamVar) -> None:
        """Sub objects.

        name: Name,
        unpack: Optional[Token],
        type_tag: SubTag[SubNodeList[TypeSpec]],
        value: Optional[ExprType],
        """

    def exit_arch_has(self, node: ast.ArchHas) -> None:
        """Sub objects.

        is_static: bool,
        access: Optional[SubTag[Token]],
        vars: SubNodeList[HasVar],
        is_frozen: bool,
        doc: Optional[Constant],
        """

    def exit_has_var(self, node: ast.HasVar) -> None:
        """Sub objects.

        name: Name,
        type_tag: SubTag[SubNodeList[TypeSpec]],
        value: Optional[ExprType],
        """

    def exit_type_spec(self, node: ast.TypeSpec) -> None:
        """Sub objects.

        spec_type: Token | SubNodeList[NameType],
        list_nest: Optional[TypeSpec],
        dict_nest: Optional[TypeSpec],
        null_ok: bool,
        """

    def exit_typed_ctx_block(self, node: ast.TypedCtxBlock) -> None:
        """Sub objects.

        type_ctx: SubNodeList[TypeSpec],
        body: SubNodeList[CodeBlockStmt],
        """

    def exit_if_stmt(self, node: ast.IfStmt) -> None:
        """Sub objects.

        condition: ExprType,
        body: SubNodeList[CodeBlockStmt],
        elseifs: Optional[ElseIfs],
        else_body: Optional[ElseStmt],
        """

    def exit_else_ifs(self, node: ast.ElseIfs) -> None:
        """Sub objects.

        condition: ExprType,
        body: SubNodeList[CodeBlockStmt],
        elseifs: Optional[ElseIfs],
        """

    def exit_else_stmt(self, node: ast.ElseStmt) -> None:
        """Sub objects.

        body: SubNodeList[CodeBlockStmt],
        """

    def exit_try_stmt(self, node: ast.TryStmt) -> None:
        """Sub objects.

        body: SubNodeList[CodeBlockStmt],
        excepts: Optional[SubNodeList[Except]],
        finally_body: Optional[FinallyStmt],
        """

    def exit_except(self, node: ast.Except) -> None:
        """Sub objects.

        ex_type: ExprType,
        name: Optional[Token],
        body: SubNodeList[CodeBlockStmt],
        """

    def exit_finally_stmt(self, node: ast.FinallyStmt) -> None:
        """Sub objects.

        body: SubNodeList[CodeBlockStmt],
        """

    def exit_iter_for_stmt(self, node: ast.IterForStmt) -> None:
        """Sub objects.

        iter: Assignment,
        condition: ExprType,
        count_by: ExprType,
        body: SubNodeList[CodeBlockStmt],
        """

    def exit_in_for_stmt(self, node: ast.InForStmt) -> None:
        """Sub objects.

        name_list: SubNodeList[Name],
        collection: ExprType,
        body: SubNodeList[CodeBlockStmt],
        """

    def exit_while_stmt(self, node: ast.WhileStmt) -> None:
        """Sub objects.

        condition: ExprType,
        body: SubNodeList[CodeBlockStmt],
        """

    def exit_with_stmt(self, node: ast.WithStmt) -> None:
        """Sub objects.

        exprs: SubNodeList[ExprAsItem],
        body: SubNodeList[CodeBlockStmt],
        """

    def exit_expr_as_item(self, node: ast.ExprAsItem) -> None:
        """Sub objects.

        expr: ExprType,
        alias: Optional[Name],
        """

    def exit_raise_stmt(self, node: ast.RaiseStmt) -> None:
        """Sub objects.

        cause: Optional[ExprType],
        """

    def exit_assert_stmt(self, node: ast.AssertStmt) -> None:
        """Sub objects.

        condition: ExprType,
        error_msg: Optional[ExprType],
        """

    def exit_ctrl_stmt(self, node: ast.CtrlStmt) -> None:
        """Sub objects.

        ctrl: Token,
        """

    def exit_delete_stmt(self, node: ast.DeleteStmt) -> None:
        """Sub objects.

        target: ExprType,
        """

    def exit_report_stmt(self, node: ast.ReportStmt) -> None:
        """Sub objects.

        expr: ExprType,
        """

    def exit_return_stmt(self, node: ast.ReturnStmt) -> None:
        """Sub objects.

        expr: Optional[ExprType],
        """

    def exit_yield_stmt(self, node: ast.YieldStmt) -> None:
        """Sub objects.

        expr: Optional[ExprType],
        """

    def exit_ignore_stmt(self, node: ast.IgnoreStmt) -> None:
        """Sub objects.

        target: ExprType,
        """

    def exit_visit_stmt(self, node: ast.VisitStmt) -> None:
        """Sub objects.

        vis_type: Optional[SubTag[SubNodeList[Name]]],
        target: ExprType,
        else_body: Optional[ElseStmt],
        """

    def exit_revisit_stmt(self, node: ast.RevisitStmt) -> None:
        """Sub objects.

        hops: Optional[ExprType],
        else_body: Optional[ElseStmt],
        """

    def exit_disengage_stmt(self, node: ast.DisengageStmt) -> None:
        """Sub objects."""

    def exit_await_stmt(self, node: ast.AwaitStmt) -> None:
        """Sub objects.

        target: ExprType,
        """

    def exit_assignment(self, node: ast.Assignment) -> None:
        """Sub objects.

        target: AtomType,
        value: ExprType,
        is_static: bool,
        mutable: bool =True,
        """

    def exit_binary_expr(self, node: ast.BinaryExpr) -> None:
        """Sub objects.

        left: ExprType,
        right: ExprType,
        op: Token | DisconnectOp | ConnectOp,
        """

    def exit_unary_expr(self, node: ast.UnaryExpr) -> None:
        """Sub objects.

        operand: ExprType,
        op: Token,
        """

    def exit_if_else_expr(self, node: ast.IfElseExpr) -> None:
        """Sub objects.

        condition: ExprType,
        value: ExprType,
        else_value: ExprType,
        """

    def exit_multi_string(self, node: ast.MultiString) -> None:
        """Sub objects.

        strings: list[Constant | FString],
        """

    def exit_f_string(self, node: ast.FString) -> None:
        """Sub objects.

        parts: Optional[SubNodeList[Constant | ExprType]],
        """

    def exit_expr_list(self, node: ast.ExprList) -> None:
        """Sub objects.

        values: Optional[SubNodeList[ExprType]],
        """

    def exit_list_val(self, node: ast.ListVal) -> None:
        """Sub objects.

        values: Optional[SubNodeList[ExprType]],
        """

    def exit_set_val(self, node: ast.SetVal) -> None:
        """Sub objects.

        values: Optional[SubNodeList[ExprType]],
        """

    def exit_tuple_val(self, node: ast.TupleVal) -> None:
        """Sub objects.

        values: Optional[SubNodeList[ExprType | Assignment]],
        """

    def exit_dict_val(self, node: ast.DictVal) -> None:
        """Sub objects.

        kv_pairs: list[KVPair],
        """

    def exit_k_v_pair(self, node: ast.KVPair) -> None:
        """Sub objects.

        key: ExprType,
        value: ExprType,
        """

    def exit_inner_compr(self, node: ast.InnerCompr) -> None:
        """Sub objects.

        out_expr: ExprType,
        names: SubNodeList[Name],
        collection: ExprType,
        conditional: Optional[ExprType],
        """

    def exit_list_compr(self, node: ast.ListCompr) -> None:
        """Sub objects.

        compr: InnerCompr,
        """

    def exit_gen_compr(self, node: ast.GenCompr) -> None:
        """Sub objects.

        compr: InnerCompr,
        """

    def exit_set_compr(self, node: ast.SetCompr) -> None:
        """Sub objects.

        compr: InnerCompr,
        """

    def exit_dict_compr(self, node: ast.DictCompr) -> None:
        """Sub objects.

        kv_pair: KVPair,
        names: SubNodeList[Name],
        collection: ExprType,
        conditional: Optional[ExprType],
        """

    def exit_atom_trailer(self, node: ast.AtomTrailer) -> None:
        """Sub objects.

        target: AtomType,
        right: AtomType,
        null_ok: bool,
        """

    def exit_func_call(self, node: ast.FuncCall) -> None:
        """Sub objects.

        target: AtomType,
        params: Optional[SubNodeList[ExprType | Assignment]],
        """

    def exit_index_slice(self, node: ast.IndexSlice) -> None:
        """Sub objects.

        start: Optional[ExprType],
        stop: Optional[ExprType],
        is_range: bool,
        """

    def exit_special_var_ref(self, node: ast.SpecialVarRef) -> None:
        """Sub objects.

        var: Token,
        """

    def exit_edge_op_ref(self, node: ast.EdgeOpRef) -> None:
        """Sub objects.

        filter_type: Optional[ExprType],
        filter_cond: Optional[SubNodeList[BinaryExpr]],
        edge_dir: EdgeDir,
        from_walker: bool,
        """

    def exit_disconnect_op(self, node: ast.DisconnectOp) -> None:
        """Sub objects.

        edge_spec: EdgeOpRef,
        """

    def exit_connect_op(self, node: ast.ConnectOp) -> None:
        """Sub objects.

        conn_type: Optional[ExprType],
        conn_assign: Optional[SubNodeList[Assignment]],
        edge_dir: EdgeDir,
        """

    def exit_filter_compr(self, node: ast.FilterCompr) -> None:
        """Sub objects.

        compares: SubNodeList[BinaryExpr],
        """

    def exit_token(self, node: ast.Token) -> None:
        """Sub objects.

        name: str,
        value: str,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        """

    def exit_name(self, node: ast.Name) -> None:
        """Sub objects.

        name: str,
        value: str,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        """

    def exit_constant(self, node: ast.Constant) -> None:
        """Sub objects.

        name: str,
        value: str,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        """

    def exit_builtin_type(self, node: ast.BuiltinType) -> None:
        """Sub objects.

        name: str,
        value: str,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        """
