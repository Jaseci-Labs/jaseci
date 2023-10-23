"""Ast build pass for Jaseci Ast.

This pass adds a more complete set of symbols from the AST to the
symbol table. This includes assignments, parameters, arch ref chains,
and more. This pass also links the symbols in the AST to their corresponding
sybmols in the symbol table (including uses).
"""
from typing import Optional, Sequence

import jaclang.jac.absyntree as ast
from jaclang.jac.passes import Pass
from jaclang.jac.symtable import Symbol, SymbolTable


class DefUsePass(Pass):
    """Jac Ast build pass."""

    def before_pass(self) -> None:
        """Before pass."""
        # self.marked: set[ast.AstSymbolNode] = set()  # Marked for ignoring
        self.unlinked: set[ast.AstSymbolNode] = set()  # Failed use lookups
        self.linked: set[ast.AstSymbolNode] = set()  # Successful use lookups

    def after_pass(self) -> None:
        """After pass."""
        for i in self.unlinked:
            self.warning(f"Unlinked {i.__class__.__name__} {i.sym_name}")

    def seen(self, node: ast.AstSymbolNode) -> bool:
        """Check if seen."""
        return node.sym_link is not None or node in self.linked or node in self.unlinked

    def def_insert(
        self,
        node: ast.AstSymbolNode,
        access_spec: Optional[ast.AstAccessNode] = None,
        single_use: Optional[str] = None,
        also_link: Optional[list[ast.AstSymbolNode]] = None,
    ) -> Optional[Symbol]:
        """Insert into symbol table."""
        if self.seen(node):
            return node.sym_link
        if (
            node.sym_tab
            and (
                collide := node.sym_tab.insert(
                    node=node, single=single_use is not None, access_spec=access_spec
                )
            )
            and single_use
        ):
            self.ice(
                "Symbol Table Should be present by now"
            ) if not node.sym_tab else None
            self.already_declared_err(
                name=node.sym_name,
                typ=single_use if single_use else "ICE",
                original=collide,
            )
        self.handle_hit_outcome(node, also_link)
        return node.sym_link

    def use_lookup(
        self,
        node: ast.AstSymbolNode,
        sym_table: Optional[SymbolTable] = None,
        also_link: Optional[list[ast.AstSymbolNode]] = None,
    ) -> Optional[Symbol]:
        """Link to symbol."""
        if self.seen(node):
            return node.sym_link
        deep = True
        if not sym_table:
            sym_table = node.sym_tab
            deep = False
        if sym_table:
            node.sym_link = (
                sym_table.lookup(name=node.sym_name, deep=deep) if sym_table else None
            )
            # If successful lookup mark linked, add to table uses, and link others
            if node.sym_link:
                sym_table.uses.append(node)
        self.handle_hit_outcome(node, also_link)
        return node.sym_link

    def chain_def_insert(self, node_list: Sequence[ast.AstSymbolNode]) -> None:
        """Link chain of containing names to symbol."""
        cur_sym_tab = node_list[0].sym_tab
        node_list = node_list[:1]  # Just performs lookup mappings of pre assign chain
        for i in node_list:
            if cur_sym_tab is None:
                break
            cur_sym_tab = (
                lookup.decl.sym_tab
                if (
                    lookup := self.use_lookup(
                        i,
                        sym_table=cur_sym_tab,
                        also_link=[i.sym_name_node]
                        if isinstance(i.sym_name_node, ast.AstSymbolNode)
                        else [],
                    )
                )
                else None
            )

    def chain_use_lookup(self, node_list: Sequence[ast.AstSymbolNode]) -> None:
        """Link chain of containing names to symbol."""
        cur_sym_tab = node_list[0].sym_tab
        for i in node_list:
            if cur_sym_tab is None:
                break
            cur_sym_tab = (
                lookup.decl.sym_tab
                if (
                    lookup := self.use_lookup(
                        i,
                        sym_table=cur_sym_tab,
                        also_link=[i.sym_name_node]
                        if isinstance(i.sym_name_node, ast.AstSymbolNode)
                        else [],
                    )
                )
                else None
            )

    def handle_hit_outcome(
        self,
        node: ast.AstSymbolNode,
        also_link: Optional[list[ast.AstSymbolNode]] = None,
    ) -> None:
        """Handle outcome of lookup or insert."""
        # If successful lookup mark linked, add to table uses, and link others
        if node.sym_link:
            self.linked.add(node)
            for i in also_link if also_link else []:
                i.sym_link = node.sym_link
        if not node.sym_link:
            # Mark nodes that were not successfully linked
            self.unlinked.add(node)
            for i in also_link if also_link else []:
                if not i.sym_link:
                    self.unlinked.add(i)

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

    def enter_inner_compr(self, node: ast.InnerCompr) -> None:
        """Sub objects.

        out_expr: ExprType,
        names: SubNodeList[Name],
        collection: ExprType,
        conditional: Optional[ExprType],
        """
        for i in node.names.items:
            self.def_insert(i, single_use="list compr var")

    def enter_dict_compr(self, node: ast.DictCompr) -> None:
        """Sub objects.

        kv_pair: KVPair,
        names: SubNodeList[Name],
        collection: ExprType,
        conditional: Optional[ExprType],
        """
        for i in node.names.items:
            self.def_insert(i, single_use="dict compr var")

    def enter_atom_trailer(self, node: ast.AtomTrailer) -> None:
        """Sub objects.

        target: AtomType,
        right: AtomType,
        is_scope_contained: bool,
        """
        left = node.right if isinstance(node.right, ast.AtomTrailer) else node.target
        right = node.target if isinstance(node.right, ast.AtomTrailer) else node.right
        left = (
            left.value if isinstance(left, ast.AtomUnit) and left.is_null_ok else left
        )
        trag_list: list[ast.AstSymbolNode] = []
        while isinstance(left, ast.AtomTrailer) and left.is_scope_contained:
            if not isinstance(right, ast.AtomSymbolType):
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
            left = left.value if isinstance(left, ast.AtomUnit) else left
        trag_list.insert(0, left)
        self.chain_use_lookup(trag_list)

    def enter_func_call(self, node: ast.FuncCall) -> None:
        """Sub objects.

        target: AtomType,
        params: Optional[SubNodeList[ExprType | Assignment]],
        """
        self.use_lookup(node.target, also_link=[node.target])

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
