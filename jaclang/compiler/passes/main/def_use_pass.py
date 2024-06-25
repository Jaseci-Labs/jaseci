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
    """Jac Ast build pass."""

    def after_pass(self) -> None:
        """After pass."""

    def enter_architype(self, node: ast.Architype) -> None:
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

    def enter_arch_ref(self, node: ast.ArchRef) -> None:
        """Sub objects.

        name_ref: NameType,
        arch: Token,
        """
        node.sym_tab.use_lookup(node)

    def enter_arch_ref_chain(self, node: ast.ArchRefChain) -> None:
        """Sub objects.

        archs: list[ArchRef],
        """
        node.sym_tab.chain_use_lookup(node.archs)

    def enter_param_var(self, node: ast.ParamVar) -> None:
        """Sub objects.

        name: Name,
        unpack: Optional[Token],
        type_tag: SubTag[ExprType],
        value: Optional[ExprType],
        """
        node.sym_tab.def_insert(node)

    def enter_has_var(self, node: ast.HasVar) -> None:
        """Sub objects.

        name: Name,
        type_tag: SubTag[SubNodeList[TypeSpec]],
        value: Optional[ExprType],
        """
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
        """Sub objects.

        target: SubNodeList[AtomType],
        value: Optional[ExprType | YieldStmt],
        type_tag: Optional[SubTag[ExprType]],
        is_static: bool = False,
        mutable: bool = True,
        """
        for i in node.target.items:
            if isinstance(i, ast.AtomTrailer):
                i.sym_tab.chain_def_insert(i.as_attr_list)
            elif isinstance(i, ast.AstSymbolNode):
                i.sym_tab.def_insert(i)
            else:
                self.error("Assignment target not valid")

    def enter_inner_compr(self, node: ast.InnerCompr) -> None:
        """Sub objects.

        is_async: bool,
        target: ExprType,
        collection: ExprType,
        conditional: Optional[ExprType],
        """
        if isinstance(node.target, ast.AtomTrailer):
            node.target.sym_tab.chain_def_insert(node.target.as_attr_list)
        elif isinstance(node.target, ast.AstSymbolNode):
            node.target.sym_tab.def_insert(node.target)
        else:
            self.error("Named target not valid")

    def enter_atom_trailer(self, node: ast.AtomTrailer) -> None:
        """Sub objects.

        target: AtomType,
        right: AtomType,
        is_scope_contained: bool,
        """
        chain = node.as_attr_list
        node.sym_tab.chain_use_lookup(chain)

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
        node.sym_tab.use_lookup(node)

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

    def enter_float(self, node: ast.Float) -> None:
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

    def enter_int(self, node: ast.Int) -> None:
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

    def enter_string(self, node: ast.String) -> None:
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

    def enter_bool(self, node: ast.Bool) -> None:
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

    def enter_builtin_type(self, node: ast.BuiltinType) -> None:
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

    def enter_name(self, node: ast.Name) -> None:
        """Sub objects.

        name: str,
        value: str,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        """
        if not isinstance(node.parent, ast.AtomTrailer):
            node.sym_tab.use_lookup(node)

    def enter_in_for_stmt(self, node: ast.InForStmt) -> None:
        """Sub objects.

        target: ExprType,
        is_async: bool,
        collection: ExprType,
        body: SubNodeList[CodeBlockStmt],
        else_body: Optional[ElseStmt],
        """
        if isinstance(node.target, ast.AtomTrailer):
            node.target.sym_tab.chain_def_insert(node.target.as_attr_list)
        elif isinstance(node.target, ast.AstSymbolNode):
            node.target.sym_tab.def_insert(node.target)
        else:
            self.error("For loop assignment target not valid")

    def enter_delete_stmt(self, node: ast.DeleteStmt) -> None:
        """Sub objects.

        target: expression,
        """
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
        """Sub objects.

        expr: ExprType,
        alias: Optional[ExprType],
        """
        if node.alias:
            if isinstance(node.alias, ast.AtomTrailer):
                node.alias.sym_tab.chain_def_insert(node.alias.as_attr_list)
            elif isinstance(node.alias, ast.AstSymbolNode):
                node.alias.sym_tab.def_insert(node.alias)
            else:
                self.error("For expr as target not valid")
