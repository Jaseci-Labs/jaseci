"""Ast build pass for Jaseci Ast."""
import jaclang.jac.absyntree as ast
from jaclang.jac.passes import Pass
from jaclang.jac.symtable import Symbol, SymbolTable


class SymTabBuildPass(Pass):
    """Jac Ast build pass."""

    def before_pass(self) -> None:
        """Before pass."""
        self.cur_sym_tab = SymbolTable()

    def register_unique_name(self, name: str, typ: str, node: ast.AstNode) -> None:
        """Register unique name."""
        if not self.cur_sym_tab.insert(Symbol(name, node), fresh_only=True):
            original = self.cur_sym_tab.lookup(name)
            self.error(
                f"Name used for {typ} '{name}' already declared "
                f"on line {original.decl.line if original else self.ice()}",
            )

    def enter_module(self, node: ast.Module) -> None:
        """Sub objects.

        name: str,
        doc: Token,
        body: Optional['Elements'],
        mod_path: str,
        rel_mod_path: str,
        is_imported: bool,
        sym_tab: Optional[SymbolTable],
        """
        self.cur_sym_tab = SymbolTable()
        node.sym_tab = self.cur_sym_tab

    def exit_module(self, node: ast.Module) -> None:
        """Sub objects.

        name: str,
        doc: Token,
        body: Optional['Elements'],
        mod_path: str,
        rel_mod_path: str,
        is_imported: bool,
        sym_tab: Optional[SymbolTable],
        """
        self.cur_sym_tab = self.cur_sym_tab.parent

    def enter_elements(self, node: ast.Elements) -> None:
        """Sub objects.

        elements: list[GlobalVars | Test | ModuleCode | Import | Architype | Ability],
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_global_vars(self, node: ast.GlobalVars) -> None:
        """Sub objects.

        doc: Optional['Token'],
        access: Optional[Token],
        assignments: 'AssignmentList',
        is_frozen: bool,
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_test(self, node: ast.Test) -> None:
        """Sub objects.

        name: Name,
        doc: Optional[Token],
        description: Token,
        body: CodeBlock,
        sym_tab: Optional[SymbolTable],
        """
        self.register_unique_name(node.name.value, "test", node)
        self.cur_sym_tab = self.cur_sym_tab.push_scope()
        node.sym_tab = self.cur_sym_tab

    def exit_test(self, node: ast.Test) -> None:
        """Sub objects.

        name: Name,
        doc: Optional[Token],
        description: Token,
        body: CodeBlock,
        sym_tab: Optional[SymbolTable],
        """
        self.cur_sym_tab = self.cur_sym_tab.parent

    def enter_module_code(self, node: ast.ModuleCode) -> None:
        """Sub objects.

        doc: Optional[Token],
        body: 'CodeBlock',
        sym_tab: Optional[SymbolTable],
        """
        self.cur_sym_tab = self.cur_sym_tab.push_scope()
        node.sym_tab = self.cur_sym_tab

    def enter_import(self, node: ast.Import) -> None:
        """Sub objects.

        lang: Name,
        path: ModulePath,
        alias: Optional[Name],
        items: Optional[ModuleItems],
        is_absorb: bool,
        sym_tab: Optional[SymbolTable],
        sub_module: Optional[Module],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_module_path(self, node: ast.ModulePath) -> None:
        """Sub objects.

        path: list[Token],
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_module_item(self, node: ast.ModuleItem) -> None:
        """Sub objects.

        name: Name,
        alias: Optional[Token],
        sym_tab: Optional[SymbolTable],
        body: Optional[AstNode],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_module_items(self, node: ast.ModuleItems) -> None:
        """Sub objects.

        items: list['ModuleItem'],
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_architype(self, node: ast.Architype) -> None:
        """Sub objects.

        name: Name,
        arch_type: Token,
        doc: Optional[Token],
        decorators: Optional[Decorators],
        access: Optional[Token],
        base_classes: BaseClasses,
        body: Optional[ArchBlock],
        sym_tab: Optional[SymbolTable],
        """
        self.register_unique_name(node.name.value, "architype", node)
        self.cur_sym_tab = self.cur_sym_tab.push_scope()
        node.sym_tab = self.cur_sym_tab

    def exit_architype(self, node: ast.Architype) -> None:
        """Sub objects.

        name: Name,
        arch_type: Token,
        doc: Optional[Token],
        decorators: Optional[Decorators],
        access: Optional[Token],
        base_classes: BaseClasses,
        body: Optional[ArchBlock],
        sym_tab: Optional[SymbolTable],
        """
        self.cur_sym_tab = self.cur_sym_tab.parent

    def enter_arch_def(self, node: ast.ArchDef) -> None:
        """Sub objects.

        doc: Optional[Token],
        mod: Optional[DottedNameList],
        arch: ArchRef,
        body: ArchBlock,
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_decorators(self, node: ast.Decorators) -> None:
        """Sub objects.

        calls: list[ExprType],
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_base_classes(self, node: ast.BaseClasses) -> None:
        """Sub objects.

        base_classes: list[DottedNameList],
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_ability(self, node: ast.Ability) -> None:
        """Sub objects.

        name_ref: Name | SpecialVarRef | ArchRef,
        is_func: bool,
        is_async: bool,
        is_static: bool,
        doc: Optional[Token],
        decorators: Optional[Decorators],
        access: Optional[Token],
        signature: Optional[FuncSignature | TypeSpec | EventSignature],
        body: Optional[CodeBlock],
        sym_tab: Optional[SymbolTable],
        arch_attached: Optional[ArchBlock],
        """
        self.register_unique_name(node.py_resolve_name(), "ability", node)
        self.cur_sym_tab = self.cur_sym_tab.push_scope()
        node.sym_tab = self.cur_sym_tab

    def exit_ability(self, node: ast.Ability) -> None:
        """Sub objects.

        name_ref: Name | SpecialVarRef | ArchRef,
        is_func: bool,
        is_async: bool,
        is_static: bool,
        doc: Optional[Token],
        decorators: Optional[Decorators],
        access: Optional[Token],
        signature: Optional[FuncSignature | TypeSpec | EventSignature],
        body: Optional[CodeBlock],
        sym_tab: Optional[SymbolTable],
        arch_attached: Optional[ArchBlock],
        """
        self.cur_sym_tab = self.cur_sym_tab.parent

    def enter_ability_def(self, node: ast.AbilityDef) -> None:
        """Sub objects.

        doc: Optional[Token],
        target: Optional[DottedNameList],
        ability: ArchRef,
        signature: FuncSignature | EventSignature,
        body: CodeBlock,
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_event_signature(self, node: ast.EventSignature) -> None:
        """Sub objects.

        event: Token,
        arch_tag_info: Optional[TypeSpecList],
        return_type: Optional['TypeSpec'],
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_dotted_name_list(self, node: ast.DottedNameList) -> None:
        """Sub objects.

        names: list[Token | SpecialVarRef | ArchRef | Name],
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_func_signature(self, node: ast.FuncSignature) -> None:
        """Sub objects.

        params: Optional['FuncParams'],
        return_type: Optional['TypeSpec'],
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_func_params(self, node: ast.FuncParams) -> None:
        """Sub objects.

        params: list['ParamVar'],
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_param_var(self, node: ast.ParamVar) -> None:
        """Sub objects.

        name: Name,
        unpack: Optional[Token],
        type_tag: 'TypeSpec',
        value: Optional[ExprType],
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_enum(self, node: ast.Enum) -> None:
        """Sub objects.

        name: Name,
        doc: Optional[Token],
        decorators: Optional['Decorators'],
        access: Optional[Token],
        base_classes: 'BaseClasses',
        body: Optional['EnumBlock'],
        sym_tab: Optional[SymbolTable],
        """
        self.register_unique_name(node.name.value, "enum", node)
        self.cur_sym_tab = self.cur_sym_tab.push_scope()
        node.sym_tab = self.cur_sym_tab

    def enter_enum_def(self, node: ast.EnumDef) -> None:
        """Sub objects.

        doc: Optional[Token],
        enum: ArchRef,
        mod: Optional[DottedNameList],
        body: EnumBlock,
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_enum_block(self, node: ast.EnumBlock) -> None:
        """Sub objects.

        stmts: list['Name|Assignment'],
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_arch_block(self, node: ast.ArchBlock) -> None:
        """Sub objects.

        members: list['ArchHas | Ability'],
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_arch_has(self, node: ast.ArchHas) -> None:
        """Sub objects.

        doc: Optional[Token],
        is_static: bool,
        access: Optional[Token],
        vars: 'HasVarList',
        is_frozen: bool,
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_has_var(self, node: ast.HasVar) -> None:
        """Sub objects.

        name: Name,
        type_tag: 'TypeSpec',
        value: Optional[ExprType],
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_has_var_list(self, node: ast.HasVarList) -> None:
        """Sub objects.

        vars: list['HasVar'],
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_type_spec(self, node: ast.TypeSpec) -> None:
        """Sub objects.

        spec_type: Token | DottedNameList,
        list_nest: TypeSpec,
        dict_nest: TypeSpec,
        null_ok: bool,
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_type_spec_list(self, node: ast.TypeSpecList) -> None:
        """Sub objects.

        types: list[TypeSpec],
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_code_block(self, node: ast.CodeBlock) -> None:
        """Sub objects.

        stmts: list[StmtType],
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_typed_ctx_block(self, node: ast.TypedCtxBlock) -> None:
        """Sub objects.

        type_ctx: TypeSpecList,
        body: CodeBlock,
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_if_stmt(self, node: ast.IfStmt) -> None:
        """Sub objects.

        condition: ExprType,
        body: 'CodeBlock',
        elseifs: Optional['ElseIfs'],
        else_body: Optional['ElseStmt'],
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_else_ifs(self, node: ast.ElseIfs) -> None:
        """Sub objects.

        elseifs: list['IfStmt'],
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_else_stmt(self, node: ast.ElseStmt) -> None:
        """Sub objects.

        body: 'CodeBlock',
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_try_stmt(self, node: ast.TryStmt) -> None:
        """Sub objects.

        body: 'CodeBlock',
        excepts: Optional['ExceptList'],
        finally_body: Optional['FinallyStmt'],
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_except(self, node: ast.Except) -> None:
        """Sub objects.

        ex_type: ExprType,
        name: Optional[Token],
        body: 'CodeBlock',
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_except_list(self, node: ast.ExceptList) -> None:
        """Sub objects.

        excepts: list['Except'],
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_finally_stmt(self, node: ast.FinallyStmt) -> None:
        """Sub objects.

        body: 'CodeBlock',
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_iter_for_stmt(self, node: ast.IterForStmt) -> None:
        """Sub objects.

        iter: 'Assignment',
        condition: ExprType,
        count_by: ExprType,
        body: 'CodeBlock',
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_in_for_stmt(self, node: ast.InForStmt) -> None:
        """Sub objects.

        name_list: NameList,
        collection: ExprType,
        body: CodeBlock,
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_name(self, node: ast.Name) -> None:
        """Sub objects.

        name: str,
        value: str,
        col_start: int,
        col_end: int,
        already_declared: bool,
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_name_list(self, node: ast.NameList) -> None:
        """Sub objects.

        names: list[Name],
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_while_stmt(self, node: ast.WhileStmt) -> None:
        """Sub objects.

        condition: ExprType,
        body: 'CodeBlock',
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_with_stmt(self, node: ast.WithStmt) -> None:
        """Sub objects.

        exprs: 'ExprAsItemList',
        body: 'CodeBlock',
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_expr_as_item(self, node: ast.ExprAsItem) -> None:
        """Sub objects.

        expr: ExprType,
        alias: Optional[Name],
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_expr_as_item_list(self, node: ast.ExprAsItemList) -> None:
        """Sub objects.

        items: list['ExprAsItem'],
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_raise_stmt(self, node: ast.RaiseStmt) -> None:
        """Sub objects.

        cause: Optional[ExprType],
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_assert_stmt(self, node: ast.AssertStmt) -> None:
        """Sub objects.

        condition: ExprType,
        error_msg: Optional[ExprType],
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_ctrl_stmt(self, node: ast.CtrlStmt) -> None:
        """Sub objects.

        ctrl: Token,
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_delete_stmt(self, node: ast.DeleteStmt) -> None:
        """Sub objects.

        target: ExprType,
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_report_stmt(self, node: ast.ReportStmt) -> None:
        """Sub objects.

        expr: ExprType,
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_return_stmt(self, node: ast.ReturnStmt) -> None:
        """Sub objects.

        expr: Optional[ExprType],
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_yield_stmt(self, node: ast.YieldStmt) -> None:
        """Sub objects.

        expr: Optional[ExprType],
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_ignore_stmt(self, node: ast.IgnoreStmt) -> None:
        """Sub objects.

        target: ExprType,
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_visit_stmt(self, node: ast.VisitStmt) -> None:
        """Sub objects.

        vis_type: Optional[Token],
        target: ExprType,
        else_body: Optional['ElseStmt'],
        sym_tab: Optional[SymbolTable],
        from_walker: bool,
        """
        node.sym_tab = self.cur_sym_tab

    def enter_revisit_stmt(self, node: ast.RevisitStmt) -> None:
        """Sub objects.

        hops: Optional[ExprType],
        else_body: Optional['ElseStmt'],
        sym_tab: Optional[SymbolTable],
        from_walker: bool,
        """
        node.sym_tab = self.cur_sym_tab

    def enter_disengage_stmt(self, node: ast.DisengageStmt) -> None:
        """Sub objects.

        sym_tab: Optional[SymbolTable],
        from_walker: bool,
        """
        node.sym_tab = self.cur_sym_tab

    def enter_await_stmt(self, node: ast.AwaitStmt) -> None:
        """Sub objects.

        target: ExprType,
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_assignment(self, node: ast.Assignment) -> None:
        """Sub objects.

        is_static: bool,
        target: 'AtomType',
        value: ExprType,
        mutable: bool,
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_binary_expr(self, node: ast.BinaryExpr) -> None:
        """Sub objects.

        left: ExprType,
        right: ExprType,
        op: Token | DisconnectOp | ConnectOp,
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_if_else_expr(self, node: ast.IfElseExpr) -> None:
        """Sub objects.

        condition: 'BinaryExpr | IfElseExpr',
        value: ExprType,
        else_value: ExprType,
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_unary_expr(self, node: ast.UnaryExpr) -> None:
        """Sub objects.

        operand: ExprType,
        op: Token,
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_unpack_expr(self, node: ast.UnpackExpr) -> None:
        """Sub objects.

        target: ExprType,
        is_dict: bool,
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_multi_string(self, node: ast.MultiString) -> None:
        """Sub objects.

        strings: list['Token | FString'],
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_expr_list(self, node: ast.ExprList) -> None:
        """Sub objects.

        values: list[ExprType],
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_list_val(self, node: ast.ListVal) -> None:
        """Sub objects.

        values: list[ExprType],
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_set_val(self, node: ast.SetVal) -> None:
        """Sub objects.

        values: list[ExprType],
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_tuple_val(self, node: ast.TupleVal) -> None:
        """Sub objects.

        first_expr: Optional[ExprType],
        exprs: Optional[ExprList],
        assigns: Optional[AssignmentList],
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_dict_val(self, node: ast.DictVal) -> None:
        """Sub objects.

        kv_pairs: list['KVPair'],
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_inner_compr(self, node: ast.InnerCompr) -> None:
        """Sub objects.

        out_expr: ExprType,
        name_list: NameList,
        collection: ExprType,
        conditional: Optional[ExprType],
        is_list: bool,
        is_gen: bool,
        is_set: bool,
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_dict_compr(self, node: ast.DictCompr) -> None:
        """Sub objects.

        outk_expr: ExprType,
        outv_expr: ExprType,
        name_list: NameList,
        collection: ExprType,
        conditional: Optional[ExprType],
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_k_v_pair(self, node: ast.KVPair) -> None:
        """Sub objects.

        key: ExprType,
        value: ExprType,
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_atom_trailer(self, node: ast.AtomTrailer) -> None:
        """Sub objects.

        target: 'AtomType',
        right: 'IndexSlice | ArchRef | Token',
        null_ok: bool,
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_func_call(self, node: ast.FuncCall) -> None:
        """Sub objects.

        target: 'AtomType',
        params: Optional['ParamList'],
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_param_list(self, node: ast.ParamList) -> None:
        """Sub objects.

        p_args: Optional[ExprList],
        p_kwargs: Optional['AssignmentList'],
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_assignment_list(self, node: ast.AssignmentList) -> None:
        """Sub objects.

        values: list['Assignment'],
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_index_slice(self, node: ast.IndexSlice) -> None:
        """Sub objects.

        start: Optional[ExprType],
        stop: Optional[ExprType],
        is_range: bool,
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_arch_ref(self, node: ast.ArchRef) -> None:
        """Sub objects.

        name_ref: Name | SpecialVarRef,
        arch: Token,
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_special_var_ref(self, node: ast.SpecialVarRef) -> None:
        """Sub objects.

        var: Token,
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_edge_op_ref(self, node: ast.EdgeOpRef) -> None:
        """Sub objects.

        filter_type: Optional[ExprType],
        filter_cond: Optional[FilterCompr],
        edge_dir: EdgeDir,
        sym_tab: Optional[SymbolTable],
        from_walker: bool,
        """
        node.sym_tab = self.cur_sym_tab

    def enter_disconnect_op(self, node: ast.DisconnectOp) -> None:
        """Sub objects.

        filter_type: Optional[ExprType],
        filter_cond: Optional[FilterCompr],
        edge_dir: EdgeDir,
        sym_tab: Optional[SymbolTable],
        from_walker: bool,
        """
        node.sym_tab = self.cur_sym_tab

    def enter_connect_op(self, node: ast.ConnectOp) -> None:
        """Sub objects.

        conn_type: Optional[ExprType],
        conn_assign: Optional[AssignmentList],
        edge_dir: EdgeDir,
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_filter_compr(self, node: ast.FilterCompr) -> None:
        """Sub objects.

        compares: list[BinaryExpr],
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_f_string(self, node: ast.FString) -> None:
        """Sub objects.

        parts: list['Token | ExprType'],
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_parse(self, node: ast.Parse) -> None:
        """Sub objects.

        name: str,
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_token(self, node: ast.Token) -> None:
        """Sub objects.

        name: str,
        value: str,
        col_start: int,
        col_end: int,
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab

    def enter_constant(self, node: ast.Constant) -> None:
        """Sub objects.

        name: str,
        value: str,
        col_start: int,
        col_end: int,
        typ: type,
        sym_tab: Optional[SymbolTable],
        """
        node.sym_tab = self.cur_sym_tab
