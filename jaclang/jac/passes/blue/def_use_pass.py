"""Ast build pass for Jaseci Ast."""
from typing import Optional

import jaclang.jac.absyntree as ast
from jaclang.jac.passes import Pass
from jaclang.jac.symtable import Symbol, SymbolTable


class DefUsePass(Pass):
    """Jac Ast build pass."""

    def before_pass(self) -> None:
        """Before pass."""
        self.marked: set[ast.AstSymbolNode] = set()  # Marked for ignoring
        self.unlinked: set[ast.AstSymbolNode] = set()  # Failed use lookups
        self.linked: set[ast.AstSymbolNode] = set()  # Successful use lookups

    def after_pass(self) -> None:
        """After pass."""
        for i in self.unlinked:
            self.warning(f"Unlinked {i.__class__.__name__} {i.sym_name}")

    def use_lookup(
        self, node: ast.AstSymbolNode, sym_table: Optional[SymbolTable] = None
    ) -> Optional[Symbol]:
        """Link to symbol."""
        deep = True
        if not sym_table:
            sym_table = node.sym_tab
            deep = False
        if node.sym_link:
            return node.sym_link
        if sym_table:
            node.sym_link = (
                sym_table.lookup(node.sym_name, deep=deep) if sym_table else None
            )
            if node.sym_link:
                self.linked.add(node)
                sym_table.uses.append(node)
        return node.sym_link

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

    def enter_arch_ref(self, node: ast.ArchRef) -> None:
        """Sub objects.

        name_ref: NameType,
        arch: Token,
        """
        if node in self.marked:
            return
        self.use_lookup(node)
        if not node.sym_link:
            self.unlinked.add(node)

    def enter_arch_ref_chain(self, node: ast.ArchRefChain) -> None:
        """Sub objects.

        archs: list[ArchRef],
        """
        cur_sym_tab = node.sym_tab
        for i in node.archs:
            if cur_sym_tab is None:
                self.marked.add(i)
                continue
            lookup = self.use_lookup(i, cur_sym_tab)
            if lookup:
                cur_sym_tab = lookup.decl.sym_tab
            else:
                self.unlinked.add(i)
                cur_sym_tab = None

    def enter_param_var(self, node: ast.ParamVar) -> None:
        """Sub objects.

        name: Name,
        unpack: Optional[Token],
        type_tag: SubTag[ExprType],
        value: Optional[ExprType],
        """

    def enter_arch_has(self, node: ast.ArchHas) -> None:
        """Sub objects.

        is_static: bool,
        access: Optional[SubTag[Token]],
        vars: SubNodeList[HasVar],
        is_frozen: bool,
        doc: Optional[Constant],
        """

    def enter_has_var(self, node: ast.HasVar) -> None:
        """Sub objects.

        name: Name,
        type_tag: SubTag[SubNodeList[TypeSpec]],
        value: Optional[ExprType],
        """

    def enter_typed_ctx_block(self, node: ast.TypedCtxBlock) -> None:
        """Sub objects.

        type_ctx: SubNodeList[TypeSpec],
        body: SubNodeList[CodeBlockStmt],
        """

    def enter_if_stmt(self, node: ast.IfStmt) -> None:
        """Sub objects.

        condition: ExprType,
        body: SubNodeList[CodeBlockStmt],
        elseifs: Optional[ElseIfs],
        else_body: Optional[ElseStmt],
        """

    def enter_else_ifs(self, node: ast.ElseIfs) -> None:
        """Sub objects.

        condition: ExprType,
        body: SubNodeList[CodeBlockStmt],
        elseifs: Optional[ElseIfs],
        """

    def enter_else_stmt(self, node: ast.ElseStmt) -> None:
        """Sub objects.

        body: SubNodeList[CodeBlockStmt],
        """

    def enter_try_stmt(self, node: ast.TryStmt) -> None:
        """Sub objects.

        body: SubNodeList[CodeBlockStmt],
        excepts: Optional[SubNodeList[Except]],
        finally_body: Optional[FinallyStmt],
        """

    def enter_except(self, node: ast.Except) -> None:
        """Sub objects.

        ex_type: ExprType,
        name: Optional[Token],
        body: SubNodeList[CodeBlockStmt],
        """

    def enter_finally_stmt(self, node: ast.FinallyStmt) -> None:
        """Sub objects.

        body: SubNodeList[CodeBlockStmt],
        """

    def enter_iter_for_stmt(self, node: ast.IterForStmt) -> None:
        """Sub objects.

        iter: Assignment,
        condition: ExprType,
        count_by: ExprType,
        body: SubNodeList[CodeBlockStmt],
        """

    def enter_in_for_stmt(self, node: ast.InForStmt) -> None:
        """Sub objects.

        name_list: SubNodeList[Name],
        collection: ExprType,
        body: SubNodeList[CodeBlockStmt],
        """

    def enter_while_stmt(self, node: ast.WhileStmt) -> None:
        """Sub objects.

        condition: ExprType,
        body: SubNodeList[CodeBlockStmt],
        """

    def enter_with_stmt(self, node: ast.WithStmt) -> None:
        """Sub objects.

        exprs: SubNodeList[ExprAsItem],
        body: SubNodeList[CodeBlockStmt],
        """

    def enter_expr_as_item(self, node: ast.ExprAsItem) -> None:
        """Sub objects.

        expr: ExprType,
        alias: Optional[Name],
        """

    def enter_raise_stmt(self, node: ast.RaiseStmt) -> None:
        """Sub objects.

        cause: Optional[ExprType],
        """

    def enter_assert_stmt(self, node: ast.AssertStmt) -> None:
        """Sub objects.

        condition: ExprType,
        error_msg: Optional[ExprType],
        """

    def enter_ctrl_stmt(self, node: ast.CtrlStmt) -> None:
        """Sub objects.

        ctrl: Token,
        """

    def enter_delete_stmt(self, node: ast.DeleteStmt) -> None:
        """Sub objects.

        target: ExprType,
        """

    def enter_report_stmt(self, node: ast.ReportStmt) -> None:
        """Sub objects.

        expr: ExprType,
        """

    def enter_return_stmt(self, node: ast.ReturnStmt) -> None:
        """Sub objects.

        expr: Optional[ExprType],
        """

    def enter_yield_stmt(self, node: ast.YieldStmt) -> None:
        """Sub objects.

        expr: Optional[ExprType],
        """

    def enter_ignore_stmt(self, node: ast.IgnoreStmt) -> None:
        """Sub objects.

        target: ExprType,
        """

    def enter_visit_stmt(self, node: ast.VisitStmt) -> None:
        """Sub objects.

        vis_type: Optional[SubTag[SubNodeList[Name]]],
        target: ExprType,
        else_body: Optional[ElseStmt],
        """

    def enter_revisit_stmt(self, node: ast.RevisitStmt) -> None:
        """Sub objects.

        hops: Optional[ExprType],
        else_body: Optional[ElseStmt],
        """

    def enter_disengage_stmt(self, node: ast.DisengageStmt) -> None:
        """Sub objects."""

    def enter_await_stmt(self, node: ast.AwaitStmt) -> None:
        """Sub objects.

        target: ExprType,
        """

    def enter_assignment(self, node: ast.Assignment) -> None:
        """Sub objects.

        target: AtomType,
        value: ExprType,
        is_static: bool,
        mutable: bool =True,
        """

    def enter_binary_expr(self, node: ast.BinaryExpr) -> None:
        """Sub objects.

        left: ExprType,
        right: ExprType,
        op: Token | DisconnectOp | ConnectOp,
        """

    def enter_unary_expr(self, node: ast.UnaryExpr) -> None:
        """Sub objects.

        operand: ExprType,
        op: Token,
        """

    def enter_if_else_expr(self, node: ast.IfElseExpr) -> None:
        """Sub objects.

        condition: ExprType,
        value: ExprType,
        else_value: ExprType,
        """

    def enter_multi_string(self, node: ast.MultiString) -> None:
        """Sub objects.

        strings: list[Constant | FString],
        """

    def enter_f_string(self, node: ast.FString) -> None:
        """Sub objects.

        parts: Optional[SubNodeList[Constant | ExprType]],
        """

    def enter_expr_list(self, node: ast.ExprList) -> None:
        """Sub objects.

        values: Optional[SubNodeList[ExprType]],
        """

    def enter_list_val(self, node: ast.ListVal) -> None:
        """Sub objects.

        values: Optional[SubNodeList[ExprType]],
        """

    def enter_set_val(self, node: ast.SetVal) -> None:
        """Sub objects.

        values: Optional[SubNodeList[ExprType]],
        """

    def enter_tuple_val(self, node: ast.TupleVal) -> None:
        """Sub objects.

        values: Optional[SubNodeList[ExprType | Assignment]],
        """

    def enter_dict_val(self, node: ast.DictVal) -> None:
        """Sub objects.

        kv_pairs: list[KVPair],
        """

    def enter_k_v_pair(self, node: ast.KVPair) -> None:
        """Sub objects.

        key: ExprType,
        value: ExprType,
        """

    def enter_inner_compr(self, node: ast.InnerCompr) -> None:
        """Sub objects.

        out_expr: ExprType,
        names: SubNodeList[Name],
        collection: ExprType,
        conditional: Optional[ExprType],
        """

    def enter_list_compr(self, node: ast.ListCompr) -> None:
        """Sub objects.

        compr: InnerCompr,
        """

    def enter_gen_compr(self, node: ast.GenCompr) -> None:
        """Sub objects.

        compr: InnerCompr,
        """

    def enter_set_compr(self, node: ast.SetCompr) -> None:
        """Sub objects.

        compr: InnerCompr,
        """

    def enter_dict_compr(self, node: ast.DictCompr) -> None:
        """Sub objects.

        kv_pair: KVPair,
        names: SubNodeList[Name],
        collection: ExprType,
        conditional: Optional[ExprType],
        """

    def enter_atom_trailer(self, node: ast.AtomTrailer) -> None:
        """Sub objects.

        target: AtomType,
        right: AtomType,
        null_ok: bool,
        """

    def enter_func_call(self, node: ast.FuncCall) -> None:
        """Sub objects.

        target: AtomType,
        params: Optional[SubNodeList[ExprType | Assignment]],
        """

    def enter_index_slice(self, node: ast.IndexSlice) -> None:
        """Sub objects.

        start: Optional[ExprType],
        stop: Optional[ExprType],
        is_range: bool,
        """

    def enter_special_var_ref(self, node: ast.SpecialVarRef) -> None:
        """Sub objects.

        var: Token,
        """

    def enter_edge_op_ref(self, node: ast.EdgeOpRef) -> None:
        """Sub objects.

        filter_type: Optional[ExprType],
        filter_cond: Optional[SubNodeList[BinaryExpr]],
        edge_dir: EdgeDir,
        from_walker: bool,
        """

    def enter_disconnect_op(self, node: ast.DisconnectOp) -> None:
        """Sub objects.

        edge_spec: EdgeOpRef,
        """

    def enter_connect_op(self, node: ast.ConnectOp) -> None:
        """Sub objects.

        conn_type: Optional[ExprType],
        conn_assign: Optional[SubNodeList[Assignment]],
        edge_dir: EdgeDir,
        """

    def enter_filter_compr(self, node: ast.FilterCompr) -> None:
        """Sub objects.

        compares: SubNodeList[BinaryExpr],
        """

    def enter_token(self, node: ast.Token) -> None:
        """Sub objects.

        name: str,
        value: str,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        """

    def enter_name(self, node: ast.Name) -> None:
        """Sub objects.

        name: str,
        value: str,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        """

    def enter_constant(self, node: ast.Constant) -> None:
        """Sub objects.

        name: str,
        value: str,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        """

    def enter_builtin_type(self, node: ast.BuiltinType) -> None:
        """Sub objects.

        name: str,
        value: str,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        """
