"""Ast build pass for Jaseci Ast.

This pass adds a more complete set of symbols from the AST to the
symbol table. This includes assignments, parameters, arch ref chains,
and more. This pass also links the symbols in the AST to their corresponding
sybmols in the symbol table (including uses).
"""

import ast as ast3

import jaclang.compiler.unitree as uni
from jaclang.compiler.constant import Tokens as Tok
from jaclang.compiler.passes import AstPass


class DefUsePass(AstPass):
    """Jac Ast build pass."""

    def after_pass(self) -> None:
        """After pass."""

    def enter_architype(self, node: uni.Architype) -> None:
        """Sub objects.

        name: Name,
        arch_type: Token,
        access: Optional[SubTag[Token]],
        base_classes: Optional[SubNodeList[Expr]],
        body: Optional[SubNodeList[ArchBlockStmt] | ArchDef],
        doc: Optional[String] = None,
        semstr: Optional[String] = None,
        decorators: Optional[SubNodeList[Expr]] = None,
        """
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
        """Sub objects.

        name: Name,
        access: Optional[SubTag[Token]],
        base_classes: Optional[SubNodeList[Expr]],
        body: Optional[SubNodeList[EnumBlockStmt] | EnumDef],
        doc: Optional[String] = None,
        semstr: Optional[String] = None,
        decorators: Optional[SubNodeList[Expr]] = None,
        """
        node.sym_tab.inherit_baseclasses_sym(node)

    def enter_arch_ref(self, node: uni.ArchRef) -> None:
        """Sub objects.

        name_ref: NameType,
        arch: Token,
        """
        node.sym_tab.use_lookup(node)

    def enter_arch_ref_chain(self, node: uni.ArchRefChain) -> None:
        """Sub objects.

        archs: list[ArchRef],
        """
        node.sym_tab.chain_use_lookup(node.archs)

    def enter_param_var(self, node: uni.ParamVar) -> None:
        """Sub objects.

        name: Name,
        unpack: Optional[Token],
        type_tag: SubTag[ExprType],
        value: Optional[ExprType],
        """
        node.sym_tab.def_insert(node)

    def enter_has_var(self, node: uni.HasVar) -> None:
        """Sub objects.

        name: Name,
        type_tag: SubTag[SubNodeList[TypeSpec]],
        value: Optional[ExprType],
        """
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
        """Sub objects.

        target: SubNodeList[AtomType],
        value: Optional[ExprType | YieldStmt],
        type_tag: Optional[SubTag[ExprType]],
        is_static: bool = False,
        mutable: bool = True,
        """
        for i in node.target.items:
            if isinstance(i, uni.AtomTrailer):
                i.sym_tab.chain_def_insert(i.as_attr_list)
            elif isinstance(i, uni.AstSymbolNode):
                i.sym_tab.def_insert(i)
            else:
                self.log_error("Assignment target not valid")

    def enter_inner_compr(self, node: uni.InnerCompr) -> None:
        """Sub objects.

        is_async: bool,
        target: ExprType,
        collection: ExprType,
        conditional: Optional[ExprType],
        """
        if isinstance(node.target, uni.AtomTrailer):
            node.target.sym_tab.chain_def_insert(node.target.as_attr_list)
        elif isinstance(node.target, uni.AstSymbolNode):
            node.target.sym_tab.def_insert(node.target)
        else:
            self.log_error("Named target not valid")

    def enter_atom_trailer(self, node: uni.AtomTrailer) -> None:
        """Sub objects.

        target: AtomType,
        right: AtomType,
        is_scope_contained: bool,
        """
        chain = node.as_attr_list
        node.sym_tab.chain_use_lookup(chain)

    def enter_func_call(self, node: uni.FuncCall) -> None:
        """Sub objects.

        target: AtomType,
        params: Optional[SubNodeList[ExprType | Assignment]],
        """

    def enter_index_slice(self, node: uni.IndexSlice) -> None:
        """Sub objects.

        slices: list[Slice],
        is_range: bool,
        """

    def enter_special_var_ref(self, node: uni.SpecialVarRef) -> None:
        """Sub objects.

        var: Token,
        """
        node.sym_tab.use_lookup(node)

    def enter_edge_op_ref(self, node: uni.EdgeOpRef) -> None:
        """Sub objects.

        filter_type: Optional[ExprType],
        filter_cond: Optional[SubNodeList[BinaryExpr]],
        edge_dir: EdgeDir,
        from_walker: bool,
        """

    def enter_disconnect_op(self, node: uni.DisconnectOp) -> None:
        """Sub objects.

        edge_spec: EdgeOpRef,
        """

    def enter_connect_op(self, node: uni.ConnectOp) -> None:
        """Sub objects.

        conn_type: Optional[ExprType],
        conn_assign: Optional[SubNodeList[Assignment]],
        edge_dir: EdgeDir,
        """

    def enter_filter_compr(self, node: uni.FilterCompr) -> None:
        """Sub objects.

        compares: SubNodeList[BinaryExpr],
        """

    def enter_token(self, node: uni.Token) -> None:
        """Sub objects.

        name: str,
        value: str,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        """

    def enter_float(self, node: uni.Float) -> None:
        """Sub objects.

        name: str,
        value: str,
        line: int,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        """
        node.sym_tab.use_lookup(node)

    def enter_int(self, node: uni.Int) -> None:
        """Sub objects.

        name: str,
        value: str,
        line: int,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        """
        node.sym_tab.use_lookup(node)

    def enter_string(self, node: uni.String) -> None:
        """Sub objects.

        name: str,
        value: str,
        line: int,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        """
        node.sym_tab.use_lookup(node)

    def enter_bool(self, node: uni.Bool) -> None:
        """Sub objects.

        name: str,
        value: str,
        line: int,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        """
        node.sym_tab.use_lookup(node)

    def enter_builtin_type(self, node: uni.BuiltinType) -> None:
        """Sub objects.

        name: str,
        value: str,
        line: int,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        typ: type,
        """
        node.sym_tab.use_lookup(node)

    def enter_name(self, node: uni.Name) -> None:
        """Sub objects.

        name: str,
        value: str,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        """
        if not isinstance(node.parent, uni.AtomTrailer):
            node.sym_tab.use_lookup(node)

    def enter_in_for_stmt(self, node: uni.InForStmt) -> None:
        """Sub objects.

        target: ExprType,
        is_async: bool,
        collection: ExprType,
        body: SubNodeList[CodeBlockStmt],
        else_body: Optional[ElseStmt],
        """
        if isinstance(node.target, uni.AtomTrailer):
            node.target.sym_tab.chain_def_insert(node.target.as_attr_list)
        elif isinstance(node.target, uni.AstSymbolNode):
            node.target.sym_tab.def_insert(node.target)
        else:
            self.log_error("For loop assignment target not valid")

    def enter_delete_stmt(self, node: uni.DeleteStmt) -> None:
        """Sub objects.

        target: expression,
        """
        items = (
            node.target.values.items
            if isinstance(node.target, uni.TupleVal) and node.target.values
            else [node.target]
        )
        for i in items:
            if isinstance(i, uni.AtomTrailer):
                i.as_attr_list[-1].name_spec.py_ctx_func = ast3.Del
            elif isinstance(i, uni.AstSymbolNode):
                i.name_spec.py_ctx_func = ast3.Del
            else:
                self.log_error("Delete target not valid")

    def enter_expr_as_item(self, node: uni.ExprAsItem) -> None:
        """Sub objects.

        expr: ExprType,
        alias: Optional[ExprType],
        """
        if node.alias:
            if isinstance(node.alias, uni.AtomTrailer):
                node.alias.sym_tab.chain_def_insert(node.alias.as_attr_list)
            elif isinstance(node.alias, uni.AstSymbolNode):
                node.alias.sym_tab.def_insert(node.alias)
            else:
                self.log_error("For expr as target not valid")
