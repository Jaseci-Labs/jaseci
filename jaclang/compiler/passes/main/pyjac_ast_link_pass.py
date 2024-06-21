"""Jac to python ast link pass.

This pass is needed so cases where there are multiple Jac nodes relevant to a
single python node can be linked. For example FuncDef doesn't have a Name node
however Ability does.
"""

import ast as ast3

import jaclang.compiler.absyntree as ast
from jaclang.compiler.passes import Pass


class PyJacAstLinkPass(Pass):
    """Link jac ast to python ast nodes."""

    def link_jac_py_nodes(
        self, jac_node: ast.AstNode, py_nodes: list[ast3.AST]
    ) -> None:
        """Link jac name ast to py ast nodes."""
        jac_node.gen.py_ast = py_nodes
        for i in py_nodes:
            if isinstance(i.jac_link, list):  # type: ignore
                i.jac_link.append(jac_node)  # type: ignore

    def exit_module_path(self, node: ast.ModulePath) -> None:
        """Sub objects.

        path: Sequence[Token],
        alias: Optional[Name],
        path_str: str,
        """
        if node.alias:
            self.link_jac_py_nodes(jac_node=node.alias, py_nodes=node.gen.py_ast)

    def exit_architype(self, node: ast.Architype) -> None:
        """Sub objects.

        name: Name,
        arch_type: Token,
        access: Optional[SubTag[Token]],
        base_classes: Optional[SubNodeList[AtomType]],
        body: Optional[SubNodeList[ArchBlockStmt] | ArchDef],
        doc: Optional[String],
        decorators: Optional[SubNodeList[ExprType]],
        """
        self.link_jac_py_nodes(jac_node=node.name, py_nodes=node.gen.py_ast)
        if isinstance(node.body, ast.ArchDef):
            self.link_jac_py_nodes(jac_node=node.body, py_nodes=node.gen.py_ast)

    def exit_arch_def(self, node: ast.ArchDef) -> None:
        """Sub objects.

        target: ArchRefChain,
        body: SubNodeList[ArchBlockStmt],
        doc: Optional[String],
        decorators: Optional[SubNodeList[ExprType]],
        """
        for i in node.target.archs:
            if i.name_spec.name_of.sym:
                self.link_jac_py_nodes(
                    jac_node=i, py_nodes=i.name_spec.name_of.sym.decl.gen.py_ast
                )
                self.link_jac_py_nodes(
                    jac_node=i.name_spec,
                    py_nodes=i.name_spec.name_of.sym.decl.gen.py_ast,
                )

    def exit_enum(self, node: ast.Enum) -> None:
        """Sub objects.

        name: Name,
        access: Optional[SubTag[Token]],
        base_classes: Optional[Optional[SubNodeList[AtomType]]],
        body: Optional[SubNodeList[EnumBlockStmt] | EnumDef],
        doc: Optional[String],
        decorators: Optional[SubNodeList[ExprType]],
        """
        if isinstance(node.body, ast.EnumDef):
            self.link_jac_py_nodes(jac_node=node.body, py_nodes=node.gen.py_ast)

    def exit_enum_def(self, node: ast.EnumDef) -> None:
        """Sub objects.

        target: ArchRefChain,
        body: SubNodeList[EnumBlockStmt],
        doc: Optional[String],
        decorators: Optional[SubNodeList[ExprType]],
        """
        for i in node.target.archs:
            if i.name_spec.name_of.sym:
                self.link_jac_py_nodes(
                    jac_node=i, py_nodes=i.name_spec.name_of.sym.decl.gen.py_ast
                )
                self.link_jac_py_nodes(
                    jac_node=i.name_spec,
                    py_nodes=i.name_spec.name_of.sym.decl.gen.py_ast,
                )

    def exit_ability(self, node: ast.Ability) -> None:
        """Sub objects.

        name_ref: NameType,
        is_func: bool,
        is_async: bool,
        is_static: bool,
        is_abstract: bool,
        access: Optional[SubTag[Token]],
        signature: Optional[FuncSignature | ExprType | EventSignature],
        body: Optional[SubNodeList[CodeBlockStmt] | AbilityDef | FuncCall],
        doc: Optional[String],
        decorators: Optional[SubNodeList[ExprType]],
        """
        self.link_jac_py_nodes(jac_node=node.name_ref, py_nodes=node.gen.py_ast)
        if isinstance(node.body, ast.AbilityDef):
            self.link_jac_py_nodes(jac_node=node.body, py_nodes=node.gen.py_ast)

    def exit_ability_def(self, node: ast.AbilityDef) -> None:
        """Sub objects.

        target: ArchRefChain,
        signature: FuncSignature | EventSignature,
        body: SubNodeList[CodeBlockStmt],
        doc: Optional[String],
        decorators: Optional[SubNodeList[ExprType]],
        """
        for i in node.target.archs:
            if i.name_spec.name_of.sym:
                self.link_jac_py_nodes(
                    jac_node=i, py_nodes=i.name_spec.name_of.sym.decl.gen.py_ast
                )
                self.link_jac_py_nodes(
                    jac_node=i.name_spec,
                    py_nodes=i.name_spec.name_of.sym.decl.gen.py_ast,
                )

        if isinstance(node.parent, ast.Ability) and node.parent.signature:
            if isinstance(node.signature, ast.FuncSignature) and node.signature.params:
                for src_prm in node.signature.params.items:
                    if (
                        isinstance(node.parent.signature, ast.FuncSignature)
                        and node.parent.signature.params
                    ):
                        for trg_prm in node.parent.signature.params.items:
                            if src_prm.name.sym_name == trg_prm.name.sym_name:
                                self.link_jac_py_nodes(
                                    jac_node=src_prm, py_nodes=trg_prm.gen.py_ast
                                )
                                self.link_jac_py_nodes(
                                    jac_node=src_prm.name,
                                    py_nodes=trg_prm.name.gen.py_ast,
                                )
            if (
                isinstance(node.signature, ast.FuncSignature)
                and node.signature.return_type
            ) and (
                isinstance(node.parent.signature, ast.FuncSignature)
                and node.parent.signature.return_type
            ):
                self.link_jac_py_nodes(
                    jac_node=node.signature.return_type,
                    py_nodes=node.parent.signature.return_type.gen.py_ast,
                )

    def exit_param_var(self, node: ast.ParamVar) -> None:
        """Sub objects.

        name: Name,
        unpack: Optional[Token],
        type_tag: SubTag[ExprType],
        value: Optional[ExprType],
        """
        self.link_jac_py_nodes(jac_node=node.name, py_nodes=node.gen.py_ast)

    def exit_except(self, node: ast.Except) -> None:
        """Sub objects.

        ex_type: ExprType,
        name: Optional[Name],
        body: SubNodeList[CodeBlockStmt],
        """
        if node.name:
            self.link_jac_py_nodes(jac_node=node.name, py_nodes=node.gen.py_ast)

    def exit_expr_as_item(self, node: ast.ExprAsItem) -> None:
        """Sub objects.

        expr: ExprType,
        alias: Optional[ExprType],
        """
        self.link_jac_py_nodes(jac_node=node.expr, py_nodes=node.gen.py_ast)
        if node.alias:
            self.link_jac_py_nodes(jac_node=node.alias, py_nodes=node.gen.py_ast)

    def exit_global_stmt(self, node: ast.GlobalStmt) -> None:
        """Sub objects.

        target: SubNodeList[NameType],
        """
        for x, y in enumerate(node.target.items):
            self.link_jac_py_nodes(jac_node=y, py_nodes=[node.gen.py_ast[x]])

    def exit_non_local_stmt(self, node: ast.NonLocalStmt) -> None:
        """Sub objects.

        target: SubNodeList[NameType],
        """
        for x, y in enumerate(node.target.items):
            self.link_jac_py_nodes(jac_node=y, py_nodes=[node.gen.py_ast[x]])

    def exit_k_w_pair(self, node: ast.KWPair) -> None:
        """Sub objects.

        key: NameType,
        value: ExprType,
        """
        if node.key:
            self.link_jac_py_nodes(jac_node=node.key, py_nodes=node.gen.py_ast)

    def exit_atom_trailer(self, node: ast.AtomTrailer) -> None:
        """Sub objects.

        target: Expr,
        right: AtomExpr | Expr,
        is_attr: bool,
        is_null_ok: bool,
        is_genai: bool = False,
        """
        if node.is_attr and isinstance(node.right, ast.AstSymbolNode):
            self.link_jac_py_nodes(
                jac_node=node.right.name_spec, py_nodes=node.gen.py_ast
            )
