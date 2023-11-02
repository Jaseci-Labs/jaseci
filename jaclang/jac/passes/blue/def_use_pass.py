"""Ast build pass for Jaseci Ast.

This pass adds a more complete set of symbols from the AST to the
symbol table. This includes assignments, parameters, arch ref chains,
and more. This pass also links the symbols in the AST to their corresponding
sybmols in the symbol table (including uses).
"""
import jaclang.jac.absyntree as ast
from jaclang.jac.passes.blue.sym_tab_build_pass import SymTabPass


class DefUsePass(SymTabPass):
    """Jac Ast build pass."""

    def after_pass(self) -> None:
        """After pass."""
        for i in self.unlinked:
            if not i.sym_name.startswith("["):
                self.warning(
                    f"{i.sym_name} used before being defined.",
                    node_override=i,
                )

    def enter_arch_ref(self, node: ast.ArchRef) -> None:
        """Sub objects.

        name_ref: NameType,
        arch: Token,
        """
        self.use_lookup(node, also_link=[node.name_ref])

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
        self.def_insert(node, single_use="func param", also_link=[node.name])

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
                single_use="has var",
                access_spec=node.parent.parent,
                also_link=[node.name],
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
            elif isinstance(i, ast.AtomType):
                self.def_insert(i)
            else:
                self.error("Assignment target not valid")

    def enter_inner_compr(self, node: ast.InnerCompr) -> None:
        """Sub objects.

        out_expr: ExprType,
        names: SubNodeList[Name],
        collection: ExprType,
        conditional: Optional[ExprType],
        """
        tuple_items = []
        if isinstance(node.target, ast.TupleVal):
            tuple_items = node.target.values.items if node.target.values else []
        else:
            tuple_items = [node.target]
        for i in tuple_items:
            if isinstance(i, ast.AtomTrailer):
                self.chain_def_insert(self.unwind_atom_trailer(i))
            elif isinstance(i, ast.AtomType):
                self.def_insert(i)
            else:
                self.error("Named target not valid")

    def enter_atom_trailer(self, node: ast.AtomTrailer) -> None:
        """Sub objects.

        target: AtomType,
        right: AtomType,
        is_scope_contained: bool,
        """
        self.chain_use_lookup(self.unwind_atom_trailer(node))

    def unwind_atom_trailer(self, node: ast.AtomTrailer) -> list[ast.AstSymbolNode]:
        """Sub objects.

        target: ExprType,
        right: AtomType,
        is_scope_contained: bool,
        """
        left = node.right if isinstance(node.right, ast.AtomTrailer) else node.target
        right = node.target if isinstance(node.right, ast.AtomTrailer) else node.right
        trag_list: list[ast.AstSymbolNode] = []
        while isinstance(left, ast.AtomTrailer) and left.is_attr:
            if not isinstance(right, ast.AtomType):
                break
            trag_list.insert(0, right)
            old_left = left
            left = (
                old_left.right
                if isinstance(old_left.right, ast.AtomTrailer)
                else old_left.target
            )
            right = (
                old_left.target
                if isinstance(old_left.right, ast.AtomTrailer)
                else old_left.right
            )
            if isinstance(left, ast.AtomType):
                trag_list.insert(0, left)
        return trag_list

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
