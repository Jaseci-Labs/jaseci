"""Ast build pass for Jaseci Ast.

This pass adds a more complete set of symbols from the AST to the
symbol table. This includes assignments, parameters, arch ref chains,
and more. This pass also links the symbols in the AST to their corresponding
sybmols in the symbol table (including uses).
"""

import ast as ast3

import jaclang.compiler.absyntree as ast
from jaclang.compiler.constant import Tokens as Tok
from jaclang.compiler.passes.main.sym_tab_build_pass import SymTabPass


class DefUsePass(SymTabPass):
    """Jac Ast build pass."""

    def after_pass(self) -> None:
        """After pass."""

    def enter_architype(self, node: ast.Architype) -> None:
        """Sub objects.

        name: Name,
        doc: Optional[Token],
        body: Optional[SubNodeList[ArchStmt]],
        sym_tab: Optional[SymbolTable],
        """
        if node.arch_type.name == Tok.KW_WALKER:
            for i in (
                self.get_all_sub_nodes(node, ast.VisitStmt)
                + self.get_all_sub_nodes(node, ast.IgnoreStmt)
                + self.get_all_sub_nodes(node, ast.DisengageStmt)
                + self.get_all_sub_nodes(node, ast.EdgeOpRef)
            ):
                i.from_walker = True

    def enter_arch_ref(self, node: ast.ArchRef) -> None:
        """Sub objects.

        name_ref: NameType,
        arch: Token,
        """
        self.use_lookup(node)

    def enter_arch_ref_chain(self, node: ast.ArchRefChain) -> None:
        """Sub objects.

        archs: list[ArchRef],
        """
        self.chain_use_lookup(node.archs)

    def enter_param_var(self, node: ast.ParamVar) -> None:
        """Sub objects.

        name: Name,
        unpack: Optional[Token],
        type_tag: SubTag[ExprType],
        value: Optional[ExprType],
        """
        self.def_insert(node)

    def enter_has_var(self, node: ast.HasVar) -> None:
        """Sub objects.

        name: Name,
        type_tag: SubTag[SubNodeList[TypeSpec]],
        value: Optional[ExprType],
        """
        if isinstance(node.parent, ast.SubNodeList) and isinstance(
            node.parent.parent, ast.ArchHas
        ):
            self.def_insert(
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
                self.chain_def_insert(self.unwind_atom_trailer(i))
            elif isinstance(i, ast.AstSymbolNode):
                self.def_insert(i)
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
            self.chain_def_insert(self.unwind_atom_trailer(node.target))
        elif isinstance(node.target, ast.AstSymbolNode):
            self.def_insert(node.target)
        else:
            self.error("Named target not valid")

    def enter_atom_trailer(self, node: ast.AtomTrailer) -> None:
        """Sub objects.

        target: AtomType,
        right: AtomType,
        is_scope_contained: bool,
        """
        chain = self.unwind_atom_trailer(node)
        self.chain_use_lookup(chain)

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
        self.use_lookup(node)

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
        self.use_lookup(node)

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
        self.use_lookup(node)

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
        self.use_lookup(node)

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
        self.use_lookup(node)

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
        self.use_lookup(node)

    def enter_name(self, node: ast.Name) -> None:
        """Sub objects.

        name: str,
        value: str,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        """
        self.use_lookup(node)

    def enter_in_for_stmt(self, node: ast.InForStmt) -> None:
        """Sub objects.

        target: ExprType,
        is_async: bool,
        collection: ExprType,
        body: SubNodeList[CodeBlockStmt],
        else_body: Optional[ElseStmt],
        """
        if isinstance(node.target, ast.AtomTrailer):
            self.chain_def_insert(self.unwind_atom_trailer(node.target))
        elif isinstance(node.target, ast.AstSymbolNode):
            self.def_insert(node.target)
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
                self.unwind_atom_trailer(i)[-1].py_ctx_func = ast3.Del
            elif isinstance(i, ast.AstSymbolNode):
                i.py_ctx_func = ast3.Del
            else:
                self.error("Delete target not valid")

    def enter_expr_as_item(self, node: ast.ExprAsItem) -> None:
        """Sub objects.

        expr: ExprType,
        alias: Optional[ExprType],
        """
        if node.alias:
            if isinstance(node.alias, ast.AtomTrailer):
                self.chain_def_insert(self.unwind_atom_trailer(node.alias))
            elif isinstance(node.alias, ast.AstSymbolNode):
                self.def_insert(node.alias)
            else:
                self.error("For expr as target not valid")
