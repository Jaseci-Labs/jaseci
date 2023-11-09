"""Jac Blue pass for Jaseci Ast.

At the end of this pass a meta['py_code'] is present with pure python code
in each node. Module nodes contain the entire module code.
"""
import ast as ast3
from typing import TypeVar

import jaclang.jac.absyntree as ast
from jaclang.jac.constant import Constants as Con, Tokens as Tok
from jaclang.jac.passes.main import PyastGenPass

T = TypeVar("T", bound=ast3.AST)


class PurplePyastGenPass(PyastGenPass):
    """Jac blue transpilation to python pass."""

    def needs_jac_import(self) -> None:
        """Check if import is needed."""
        if "jimport" in self.already_added:
            return
        self.preamble.append(
            self.sync(
                ast3.ImportFrom(
                    module="jaclang",
                    names=[
                        self.sync(
                            ast3.alias(
                                name="jac_purple_import", asname="__jac_import__"
                            )
                        )
                    ],
                    level=0,
                ),
                jac_node=self.ir,
            )
        )
        self.already_added.append("jimport")

    def needs_make_architype(self) -> None:
        """Check if make_architype is needed."""
        if "make_architype" in self.already_added:
            return
        self.preamble.append(
            self.sync(
                ast3.ImportFrom(
                    module="jaclang.jac.features",
                    names=[
                        self.sync(
                            ast3.alias(
                                name="make_architype", asname="_jac_make_architype_"
                            )
                        ),
                        self.sync(
                            ast3.alias(name="exec_ctx", asname=f"{Con.EXEC_CONTEXT}")
                        ),
                    ],
                    level=0,
                ),
                jac_node=self.ir,
            )
        )
        self.already_added.append("make_architype")

    def needs_edge_directions(self) -> None:
        """Check if edge directions is needed."""
        if "edge_directions" in self.already_added:
            return
        self.preamble.append(
            self.sync(
                ast3.ImportFrom(
                    module="jaclang.jac.constant",
                    names=[
                        self.sync(
                            ast3.alias(
                                name="EdgeDir",
                                asname=f"{Con.EDGE_DIR}",
                            )
                        )
                    ],
                    level=0,
                ),
                jac_node=self.ir,
            )
        )
        self.already_added.append("edge_directions")

    def add_element_import(self, element: str) -> None:
        """Import necessary jac architype base class feature."""
        self.needs_make_architype()
        if element in self.already_added:
            return
        self.preamble.append(
            self.sync(
                ast3.ImportFrom(
                    module="jaclang.jac.features",
                    names=[
                        self.sync(ast3.alias(name=element, asname=f"__jac_{element}__"))
                    ],
                    level=0,
                ),
                jac_node=self.ir,
            )
        )
        self.already_added.append(element)

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
        super().exit_architype(node)
        self.needs_make_architype()
        arch_type = node.arch_type.value
        if arch_type == Tok.KW_OBJECT:
            self.add_element_import("Object")
            dec = ast3.Call(
                func=self.sync(ast3.Name(id="_jac_make_architype_", ctx=ast3.Load())),
                args=[self.sync(ast3.Constant(value=Con.OBJECT_CLASS.value))],
                keywords=[],
            )
        elif arch_type == Tok.KW_NODE:
            self.add_element_import("Node")
            dec = ast3.Call(
                func=self.sync(ast3.Name(id="_jac_make_architype_", ctx=ast3.Load())),
                args=[self.sync(ast3.Constant(value=Con.NODE_CLASS.value))],
                keywords=[],
            )
        elif arch_type == Tok.KW_EDGE:
            self.add_element_import("Edge")
            dec = ast3.Call(
                func=self.sync(ast3.Name(id="_jac_make_architype_", ctx=ast3.Load())),
                args=[self.sync(ast3.Constant(value=Con.EDGE_CLASS.value))],
                keywords=[],
            )
        else:
            self.add_element_import("Walker")
            dec = ast3.Call(
                func=self.sync(ast3.Name(id="_jac_make_architype_", ctx=ast3.Load())),
                args=[self.sync(ast3.Constant(value=Con.WALKER_CLASS.value))],
                keywords=[],
            )
        if isinstance(node.gen.py_ast, ast3.ClassDef):
            node.gen.py_ast.decorator_list.append(self.sync(dec))
        else:
            self.error("Python ClassDef AST expected and not found")

    def exit_ability(self, node: ast.Ability) -> None:
        """Sub objects.

        name_ref: NameType,
        is_func: bool,
        is_async: bool,
        is_static: bool,
        is_abstract: bool,
        access: Optional[SubTag[Token]],
        signature: Optional[FuncSignature | ExprType | EventSignature],
        body: Optional[SubNodeList[CodeBlockStmt]],
        doc: Optional[String],
        decorators: Optional[SubNodeList[ExprType]],
        """
        super().exit_ability(node)
        if isinstance(node.signature, ast.EventSignature) and node.is_method:
            type_expr = (  # TODO: Need to update core to not expect list
                node.signature.arch_tag_info
                if node.signature.arch_tag_info
                else self.sync(ast3.Constant(value=None))
            )
            if node.signature.event.name == Tok.KW_ENTRY:
                self.add_element_import("Object")
                dec = ast3.Call(
                    func=self.sync(
                        ast3.Attribute(
                            value=self.sync(ast3.Name(id=Con.OBJECT_CLASS.value)),
                            attr=Con.ON_ENTRY.value,
                            ctx=ast3.Load(),
                        )
                    ),
                    args=[type_expr],
                    keywords=[],
                )
            else:
                self.add_element_import("Object")
                dec = ast3.Call(
                    func=self.sync(
                        ast3.Attribute(
                            value=self.sync(ast3.Name(id=Con.NODE_CLASS.value)),
                            attr=Con.ON_EXIT.value,
                            ctx=ast3.Load(),
                        )
                    ),
                    args=[type_expr],
                    keywords=[],
                )
            if isinstance(node.gen.py_ast, ast3.FunctionDef):
                node.gen.py_ast.decorator_list.append(self.sync(dec))
            else:
                self.error("Python FunctionDef AST expected and not found")

    def exit_event_signature(self, node: ast.EventSignature) -> None:
        """Sub objects.

        event: Token,
        arch_tag_info: Optional[ExprType],
        return_type: Optional[SubTag[ExprType]],
        """
        here = self.sync(
            ast3.arg(
                arg=f"{Con.HERE.value}",
                annotation=node.arch_tag_info.gen.py_ast
                if node.arch_tag_info
                else None,
            ),
            jac_node=node.arch_tag_info if node.arch_tag_info else node,
        )
        node.gen.py_ast = self.sync(
            ast3.arguments(
                posonlyargs=[],
                args=[here],
                kwonlyargs=[],
                vararg=None,
                kwargs=None,
                kw_defaults=[],
                defaults=[],
            )
        )

    def exit_ignore_stmt(self, node: ast.IgnoreStmt) -> None:
        """Sub objects.

        target: ExprType,
        """
        loc = self.sync(
            ast3.Name(id="self") if node.from_walker else ast3.Name(id=Con.HERE.value)
        )
        node.gen.py_ast = self.sync(
            ast3.Call(
                func=self.sync(
                    ast3.Attribute(
                        value=loc,
                        attr=Con.WALKER_IGNORE.value,
                        ctx=ast3.Load(),
                    )
                ),
                args=[node.target.gen.py_ast],
                keywords=[],
            )
        )

    def exit_visit_stmt(self, node: ast.VisitStmt) -> None:
        """Sub objects.

        vis_type: Optional[SubNodeList[AtomType]],
        target: ExprType,
        else_body: Optional[ElseStmt],
        """
        loc = self.sync(
            ast3.Name(id="self") if node.from_walker else ast3.Name(id=Con.HERE.value)
        )
        node.gen.py_ast = self.sync(
            ast3.If(
                test=self.sync(
                    ast3.UnaryOp(
                        op=self.sync(ast3.Not()),
                        operand=self.sync(
                            ast3.Call(
                                func=self.sync(
                                    ast3.Attribute(
                                        value=loc,
                                        attr=Con.WALKER_VISIT.value,
                                        ctx=ast3.Load(),
                                    )
                                ),
                                args=[node.target.gen.py_ast],
                                keywords=[],
                            )
                        ),
                    ),
                ),
                body=[self.sync(ast3.Pass())],
                orelse=node.else_body.gen.py_ast
                if node.else_body
                else [self.sync(ast3.Pass())],
            )
        )

    def exit_disengage_stmt(self, node: ast.DisengageStmt) -> None:
        """Sub objects."""
        loc = self.sync(
            ast3.Name(id="self") if node.from_walker else ast3.Name(id=Con.HERE.value)
        )
        node.gen.py_ast = self.sync(
            ast3.Call(
                func=self.sync(
                    ast3.Attribute(
                        value=loc,
                        attr=Con.DISENGAGE.value,
                        ctx=ast3.Load(),
                    )
                ),
                args=[],
                keywords=[],
            )
        )

    def exit_binary_expr(self, node: ast.BinaryExpr) -> None:
        """Sub objects.

        left: ExprType,
        right: ExprType,
        op: Token | DisconnectOp | ConnectOp,
        """
        if isinstance(node.op, ast.ConnectOp):
            self.needs_edge_directions()
            node.gen.py_ast = self.sync(
                ast3.Call(
                    func=self.sync(
                        ast3.Attribute(
                            value=node.left.gen.py_ast,
                            attr=Con.CONNECT_NODE.value,
                            ctx=ast3.Load(),
                        ),
                        jac_node=node.left,
                    ),
                    args=[
                        node.right.gen.py_ast,
                        node.op.gen.py_ast,
                    ],
                    keywords=[],
                )
            )
        else:
            super().exit_binary_expr(node)

    def exit_edge_op_ref(self, node: ast.EdgeOpRef) -> None:
        """Sub objects.

        filter_type: Optional[ExprType],
        filter_cond: Optional[SubNodeList[BinaryExpr]],
        edge_dir: EdgeDir,
        """

    def exit_disconnect_op(self, node: ast.DisconnectOp) -> None:
        """Sub objects.

        edge_spec: EdgeOpRef,
        """
        self.ds_feature_warn()
        node.gen.py_ast = self.sync(ast3.Constant(value=None))

    def exit_connect_op(self, node: ast.ConnectOp) -> None:
        """Sub objects.

        conn_type: Optional[ExprType],
        conn_assign: Optional[SubNodeList[Assignment]],
        edge_dir: EdgeDir,
        """
        self.ds_feature_warn()
        node.gen.py_ast = self.sync(ast3.Constant(value=None))

    def exit_filter_compr(self, node: ast.FilterCompr) -> None:
        """Sub objects.

        compares: SubNodeList[BinaryExpr],
        """
        self.ds_feature_warn()
        node.gen.py_ast = self.sync(ast3.Constant(value=None))

    def exit_match_stmt(self, node: ast.MatchStmt) -> None:
        """Sub objects.

        target: SubNodeList[ExprType],
        cases: list[MatchCase],
        """
        node.gen.py_ast = self.sync(
            ast3.Match(
                subject=node.target.gen.py_ast,
                cases=[x.gen.py_ast for x in node.cases],
            )
        )

    def exit_match_case(self, node: ast.MatchCase) -> None:
        """Sub objects.

        pattern: MatchPattern,
        guard: Optional[ExprType],
        body: SubNodeList[CodeBlockStmt],
        """
        node.gen.py_ast = self.sync(
            ast3.match_case(
                pattern=node.pattern.gen.py_ast,
                guard=node.guard.gen.py_ast if node.guard else None,
                body=self.resolve_stmt_block(node.body),
            )
        )

    def exit_match_or(self, node: ast.MatchOr) -> None:
        """Sub objects.

        patterns: list[MatchPattern],
        """
        node.gen.py_ast = self.sync(
            ast3.MatchOr(
                patterns=[x.gen.py_ast for x in node.patterns],
            )
        )

    def exit_match_as(self, node: ast.MatchAs) -> None:
        """Sub objects.

        name: NameType,
        pattern: MatchPattern,
        """
        node.gen.py_ast = self.sync(
            ast3.MatchAs(
                name=node.name.sym_name,
                pattern=node.pattern.gen.py_ast if node.pattern else None,
            )
        )

    def exit_match_wild(self, node: ast.MatchWild) -> None:
        """Sub objects."""
        node.gen.py_ast = self.sync(ast3.MatchAs())

    def exit_match_value(self, node: ast.MatchValue) -> None:
        """Sub objects.

        value: ExprType,
        """
        node.gen.py_ast = self.sync(ast3.MatchValue(value=node.value.gen.py_ast))

    def exit_match_singleton(self, node: ast.MatchSingleton) -> None:
        """Sub objects.

        value: Bool | Null,
        """
        node.gen.py_ast = self.sync(ast3.MatchSingleton(value=node.value.lit_value))

    def exit_match_sequence(self, node: ast.MatchSequence) -> None:
        """Sub objects.

        values: list[MatchPattern],
        """
        node.gen.py_ast = self.sync(
            ast3.MatchSequence(
                patterns=[x.gen.py_ast for x in node.values],
            )
        )

    def exit_match_mapping(self, node: ast.MatchMapping) -> None:
        """Sub objects.

        values: list[MatchKVPair | MatchStar],
        """
        mapping = self.sync(ast3.MatchMapping(keys=[], patterns=[], rest=None))
        for i in node.values:
            if isinstance(i, ast.MatchKVPair):
                mapping.keys.append(i.key.value.gen.py_ast)
                mapping.patterns.append(i.value.gen.py_ast)
            elif isinstance(i, ast.MatchStar):
                mapping.rest = i.name.sym_name
        node.gen.py_ast = mapping

    def exit_match_k_v_pair(self, node: ast.MatchKVPair) -> None:
        """Sub objects.

        key: MatchPattern | NameType,
        value: MatchPattern,
        """
        node.gen.py_ast = self.sync(
            ast3.MatchMapping(
                patterns=[node.key.gen.py_ast, node.value.gen.py_ast],
            )
        )

    def exit_match_star(self, node: ast.MatchStar) -> None:
        """Sub objects.

        name: NameType,
        is_list: bool,
        """
        node.gen.py_ast = self.sync(ast3.MatchStar(name=node.name.sym_name))

    def exit_match_arch(self, node: ast.MatchArch) -> None:
        """Sub objects.

        name: NameType,
        arg_patterns: Optional[SubNodeList[MatchPattern]],
        kw_patterns: Optional[SubNodeList[MatchKVPair]],
        """
        node.gen.py_ast = self.sync(
            ast3.MatchClass(
                cls=node.name.gen.py_ast,
                patterns=[x.gen.py_ast for x in node.arg_patterns.items]
                if node.arg_patterns
                else [],
                kwd_attrs=[x.key.sym_name for x in node.kw_patterns.items]
                if node.kw_patterns
                else [],
                kwd_patterns=[x.value.gen.py_ast for x in node.kw_patterns.items]
                if node.kw_patterns
                else [],
            )
        )

    def exit_token(self, node: ast.Token) -> None:
        """Sub objects.

        file_path: str,
        name: str,
        value: str,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        """
        if node.name == Tok.KW_AND:
            node.gen.py_ast = self.sync(ast3.And())
        elif node.name == Tok.KW_OR:
            node.gen.py_ast = self.sync(ast3.Or())
        elif node.name in [Tok.PLUS, Tok.ADD_EQ]:
            node.gen.py_ast = self.sync(ast3.Add())
        elif node.name in [Tok.BW_AND, Tok.BW_AND_EQ]:
            node.gen.py_ast = self.sync(ast3.BitAnd())
        elif node.name in [Tok.BW_OR, Tok.BW_OR_EQ]:
            node.gen.py_ast = self.sync(ast3.BitOr())
        elif node.name in [Tok.BW_XOR, Tok.BW_XOR_EQ]:
            node.gen.py_ast = self.sync(ast3.BitXor())
        elif node.name in [Tok.DIV, Tok.DIV_EQ]:
            node.gen.py_ast = self.sync(ast3.Div())
        elif node.name in [Tok.FLOOR_DIV, Tok.FLOOR_DIV_EQ]:
            node.gen.py_ast = self.sync(ast3.FloorDiv())
        elif node.name in [Tok.LSHIFT, Tok.LSHIFT_EQ]:
            node.gen.py_ast = self.sync(ast3.LShift())
        elif node.name in [Tok.MOD, Tok.MOD_EQ]:
            node.gen.py_ast = self.sync(ast3.Mod())
        elif node.name in [Tok.STAR_MUL, Tok.MUL_EQ]:
            node.gen.py_ast = self.sync(ast3.Mult())
        elif node.name in [Tok.DECOR_OP, Tok.MATMUL_EQ]:
            node.gen.py_ast = self.sync(ast3.MatMult())
        elif node.name in [Tok.STAR_POW, Tok.STAR_POW_EQ]:
            node.gen.py_ast = self.sync(ast3.Pow())
        elif node.name in [Tok.RSHIFT, Tok.RSHIFT_EQ]:
            node.gen.py_ast = self.sync(ast3.RShift())
        elif node.name in [Tok.MINUS, Tok.SUB_EQ]:
            node.gen.py_ast = self.sync(ast3.Sub())
        elif node.name in [Tok.BW_NOT, Tok.BW_NOT_EQ]:
            node.gen.py_ast = self.sync(ast3.Invert())
        elif node.name in [Tok.NOT, Tok.NE]:
            node.gen.py_ast = self.sync(ast3.Not())
        elif node.name == Tok.EE:
            node.gen.py_ast = self.sync(ast3.Eq())
        elif node.name == Tok.GT:
            node.gen.py_ast = self.sync(ast3.Gt())
        elif node.name == Tok.GTE:
            node.gen.py_ast = self.sync(ast3.GtE())
        elif node.name == Tok.KW_IN:
            node.gen.py_ast = self.sync(ast3.In())
        elif node.name == Tok.KW_IS:
            node.gen.py_ast = self.sync(ast3.Is())
        elif node.name == Tok.KW_ISN:
            node.gen.py_ast = self.sync(ast3.IsNot())
        elif node.name == Tok.LT:
            node.gen.py_ast = self.sync(ast3.Lt())
        elif node.name == Tok.LTE:
            node.gen.py_ast = self.sync(ast3.LtE())
        elif node.name == Tok.NE:
            node.gen.py_ast = self.sync(ast3.NotEq())
        elif node.name == Tok.KW_NIN:
            node.gen.py_ast = self.sync(ast3.NotIn())

    def exit_name(self, node: ast.Name) -> None:
        """Sub objects.

        file_path: str,
        name: str,
        value: str,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        """
        node.gen.py_ast = self.sync(ast3.Name(id=node.sym_name, ctx=node.py_ctx_func()))
        if node.is_enum_singleton:
            node.gen.py_ast.ctx = ast3.Store()
            node.gen.py_ast = self.sync(
                ast3.Assign(
                    targets=[node.gen.py_ast],
                    value=self.sync(
                        ast3.Call(
                            func=self.sync(
                                ast3.Name(id="__jac_auto__", ctx=ast3.Load())
                            ),
                            args=[],
                            keywords=[],
                        )
                    ),
                )
            )

    def exit_float(self, node: ast.Float) -> None:
        """Sub objects.

        file_path: str,
        name: str,
        value: str,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        """
        node.gen.py_ast = self.sync(ast3.Constant(value=float(node.value)))

    def exit_int(self, node: ast.Int) -> None:
        """Sub objects.

        file_path: str,
        name: str,
        value: str,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        """
        node.gen.py_ast = self.sync(ast3.Constant(value=int(node.value)))

    def exit_string(self, node: ast.String) -> None:
        """Sub objects.

        file_path: str,
        name: str,
        value: str,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        """
        node.gen.py_ast = self.sync(ast3.Constant(value=node.ast_str))

    def exit_bool(self, node: ast.Bool) -> None:
        """Sub objects.

        file_path: str,
        name: str,
        value: str,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        """
        node.gen.py_ast = self.sync(ast3.Constant(value=bool(node.value)))

    def exit_builtin_type(self, node: ast.BuiltinType) -> None:
        """Sub objects.

        file_path: str,
        name: str,
        value: str,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        """
        node.gen.py_ast = self.sync(ast3.Name(id=node.sym_name, ctx=node.py_ctx_func()))

    def exit_null(self, node: ast.Null) -> None:
        """Sub objects.

        file_path: str,
        name: str,
        value: str,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        """
        node.gen.py_ast = self.sync(ast3.Constant(value=None))

    def exit_semi(self, node: ast.Semi) -> None:
        """Sub objects.

        file_path: str,
        name: str,
        value: str,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        """
