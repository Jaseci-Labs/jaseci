"""Jac Blue pass for Jaseci Ast.

At the end of this pass a meta['py_code'] is present with pure python code
in each node. Module nodes contain the entire module code.
"""
import ast as ast3
from typing import Optional, TypeVar

import jaclang.jac.absyntree as ast
from jaclang.jac.constant import Constants as Con
from jaclang.jac.passes import Pass

T = TypeVar("T", bound=ast3.AST)


class PyastGenPass(Pass):
    """Jac blue transpilation to python pass."""

    def before_pass(self) -> None:
        """Initialize pass."""
        self.debuginfo: dict[str, list[str]] = {"jac_mods": []}
        self.already_added = {
            "jimport": False,
            "enum": False,
            "test": False,
            "dataclass": False,
        }
        self.preamble: list[ast3.AST] = [
            ast3.ImportFrom(
                module="__future__",
                names=[ast3.alias(name="annotations", asname=None)],
                level=0,
            )
        ]

    def needs_jac_import(self) -> None:
        """Check if import is needed."""
        if self.already_added["jimport"]:
            return
        self.preamble.append(
            ast3.ImportFrom(
                module="jaclang",
                names=[ast3.alias(name="jac_blue_import", asname="__jac_import__")],
                level=0,
            )
        )
        self.already_added["jimport"] = True

    def needs_enum(self) -> None:
        """Check if enum is needed."""
        if self.already_added["enum"]:
            return
        self.preamble.append(
            ast3.ImportFrom(
                module="enum",
                names=[
                    ast3.alias(name="Enum", asname="__jac_Enum__"),
                    ast3.alias(name="auto", asname="__jac_auto__"),
                ],
                level=0,
            )
        )
        self.already_added["enum"] = True

    def needs_data_class(self) -> None:
        """Check if enum is needed."""
        if self.already_added["dataclass"]:
            return
        self.preamble.append(
            ast3.ImportFrom(
                module="dataclasses",
                names=[ast3.alias(name="dataclass", asname="__jac_dataclass__")],
                level=0,
            )
        )
        self.already_added["enum"] = True

    def needs_test(self) -> None:
        """Check if test is needed."""
        if self.already_added["test"]:
            return
        test_code = (
            "import unittest as __jac_unittest__\n"
            "__jac_tc__ = __jac_unittest__.TestCase()\n"
            "__jac_suite__ = __jac_unittest__.TestSuite()\n"
            "class __jac_check:\n"
            "    def __getattr__(self, name):\n"
            "        return getattr(__jac_tc__, 'assert'+name)"
        )
        self.preamble += ast3.parse(test_code).body
        self.already_added["test"] = True

    def flatten_ast_list(
        self, body: list[ast3.AST | list[ast3.AST] | None]
    ) -> list[ast3.AST]:
        """Flatten ast list."""
        new_body = []
        for i in body:
            if isinstance(i, list):
                new_body += i
            elif isinstance(i, ast3.AST):
                new_body.append(i) if i else None
        return new_body

    def sync(
        self, py_node: T, jac_node: Optional[ast.AstNode] = None, deep: bool = False
    ) -> T:
        """Sync ast locations."""
        if not jac_node:
            jac_node = self.cur_node
        py_node.lineno = jac_node.loc.first_line
        py_node.col_offset = jac_node.loc.col_start
        py_node.end_lineno = jac_node.loc.last_line
        py_node.end_col_offset = jac_node.loc.col_end
        if deep:
            for child in ast3.iter_child_nodes(py_node):
                self.sync(child, jac_node, deep=True)
        return py_node

    def sync_many(self, py_nodes: list[T], jac_node: ast.AstNode) -> list[T]:
        """Sync ast locations."""
        for py_node in py_nodes:
            self.sync(py_node, jac_node)
        return py_nodes

    def exit_sub_tag(self, node: ast.SubTag[ast.T]) -> None:
        """Sub objects.

        tag: T,
        """
        node.gen.py_ast = node.tag.gen.py_ast

    def exit_sub_node_list(self, node: ast.SubNodeList[ast.T]) -> None:
        """Sub objects.

        items: Sequence[T],
        """
        node.gen.py_ast = self.flatten_ast_list([i.gen.py_ast for i in node.items])

    def exit_module(self, node: ast.Module) -> None:
        """Sub objects.

        name: str,
        source: JacSource,
        doc: Optional[String],
        body: Sequence[ElementStmt],
        is_imported: bool,
        """
        body = (
            [
                node.doc.gen.py_ast,
                *self.preamble,
                *[x.gen.py_ast for x in node.body],
            ]
            if node.doc
            else [*self.preamble, *[x.gen.py_ast for x in node.body]]
        )
        new_body = []
        for i in body:
            if isinstance(i, list):
                new_body += i
            else:
                new_body.append(i) if i else None
        node.gen.py_ast = self.sync(
            ast3.Module(
                body=new_body,
                type_ignores=[],
            )
        )

    def exit_global_vars(self, node: ast.GlobalVars) -> None:
        """Sub objects.

        access: Optional[SubTag[Token]],
        assignments: SubNodeList[Assignment],
        is_frozen: bool,
        doc: Optional[String],
        """
        if node.doc:
            doc = node.doc.gen.py_ast
            if isinstance(doc, ast3.AST) and isinstance(
                node.assignments.gen.py_ast, list
            ):
                node.gen.py_ast = [doc] + node.assignments.gen.py_ast
            else:
                raise self.ice()
        else:
            node.gen.py_ast = node.assignments.gen.py_ast

    def exit_test(self, node: ast.Test) -> None:
        """Sub objects.

        name: Name | Token,
        body: SubNodeList[CodeBlockStmt],
        doc: Optional[String],
        """
        self.needs_test()
        test_name = node.name.sym_name
        func = self.sync(
            ast3.FunctionDef(
                name=test_name,
                args=None,
                body=node.body.gen.py_ast,
                decorator_list=[],
                returns=None,
                type_comment=None,
            ),
        )
        func.body.insert(
            0,
            self.sync(ast3.parse("check = __jac_check()").body[0]),
        )
        check = self.sync(
            ast3.parse(
                f"__jac_suite__.addTest(__jac_unittest__.FunctionTestCase(test_{test_name}))"
            ).body[0]
        )
        node.gen.py_ast = [func, check]

    def exit_module_code(self, node: ast.ModuleCode) -> None:
        """Sub objects.

        name: Optional[SubTag[Name]],
        body: SubNodeList[CodeBlockStmt],
        doc: Optional[String],
        """
        node.gen.py_ast = node.body.gen.py_ast

    def exit_py_inline_code(self, node: ast.PyInlineCode) -> None:
        """Sub objects.

        code: Token,
        doc: Optional[String],
        """
        node.gen.py_ast = [*ast3.parse(node.code.value).body]

    def exit_import(self, node: ast.Import) -> None:
        """Sub objects.

        lang: SubTag[Name],
        path: ModulePath,
        alias: Optional[Name],
        items: Optional[SubNodeList[ModuleItem]],
        is_absorb: bool,
        doc: Optional[String],
        sub_module: Optional[Module],
        """
        py_nodes: list[ast3.AST] = []
        level = 0
        py_compat_path_str = node.path.path_str
        if node.path.path_str.startswith(".."):
            level = 2
            py_compat_path_str = node.path.path_str[2:]
        elif node.path.path_str.startswith("."):
            level = 1
            py_compat_path_str = node.path.path_str[1:]
        if node.lang.tag.value == Con.JAC_LANG_IMP:  # injects module into sys.modules
            self.needs_jac_import()
            py_nodes.append(
                self.sync(
                    ast3.Expr(
                        value=self.sync(
                            ast3.Call(
                                func=self.sync(
                                    ast3.Name(id="__jac_import__", ctx=ast3.Load())
                                ),
                                args=[],
                                keywords=[
                                    self.sync(
                                        ast3.keyword(
                                            arg="target",
                                            value=ast3.Name(
                                                id=f"{node.path.path_str}",
                                                ctx=ast3.Load(),
                                            ),
                                        )
                                    ),
                                    self.sync(
                                        ast3.keyword(
                                            arg="base_path",
                                            value=self.sync(
                                                ast3.Name(
                                                    id="__file__", ctx=ast3.Load()
                                                )
                                            ),
                                        )
                                    ),
                                ],
                            )
                        )
                    ),
                )
            )
        if node.is_absorb:
            py_nodes.append(
                self.sync(
                    py_node=ast3.ImportFrom(
                        module=py_compat_path_str,
                        names=[self.sync(ast3.alias(name="*"), node)],
                        level=level,
                    ),
                    jac_node=node,
                )
            )
            if node.items:
                self.warning(
                    "Includes import * in target module into current namespace."
                )
            return
        if not node.items:
            py_nodes.append(self.sync(ast3.Import(names=[node.path.gen.py_ast])))
        else:
            py_nodes.append(
                self.sync(
                    ast3.ImportFrom(
                        module=py_compat_path_str,
                        names=node.items.gen.py_ast,
                        level=level,
                    )
                )
            )

    def exit_module_path(self, node: ast.ModulePath) -> None:
        """Sub objects.

        path: Sequence[Token],
        alias: Optional[Name],
        path_str: str,
        """
        node.gen.py_ast = self.sync(
            ast3.alias(
                name=f"{node.path_str}",
                asname=node.alias.value if node.alias else None,
            )
        )

    def exit_module_item(self, node: ast.ModuleItem) -> None:
        """Sub objects.

        name: Name,
        alias: Optional[Name],
        """
        node.gen.py_ast = self.sync(
            ast3.alias(
                name=f"{node.name.value}",
                asname=node.alias.value if node.alias else None,
            )
        )

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
        self.needs_data_class()
        body = (
            [self.sync(ast3.Pass(), node.body)]
            if isinstance(node.body, ast.SubNodeList) and not node.body.items
            else node.body.gen.py_ast
            if node.body
            else []
        )
        if not isinstance(body, list):
            raise self.ice()
        if node.doc:
            body = [node.doc.gen.py_ast, *body]
        decorators = (
            node.decorators.gen.py_ast
            if isinstance(node.decorators, ast.SubNodeList)
            else []
        )
        if isinstance(decorators, list):
            decorators.append(
                self.sync(ast3.Name(id="__jac_dataclass__", ctx=ast3.Load()))
            )
        else:
            raise self.ice()
        base_classes = node.base_classes.gen.py_ast if node.base_classes else []
        node.gen.py_ast = self.sync(
            ast3.ClassDef(
                name=node.name.value,
                bases=base_classes,
                keywords=[],
                body=body,
                decorator_list=decorators,
                type_params=[],
            )
        )

    def exit_arch_def(self, node: ast.ArchDef) -> None:
        """Sub objects.

        target: ArchRefChain,
        body: SubNodeList[ArchBlockStmt],
        doc: Optional[String],
        decorators: Optional[SubNodeList[ExprType]],
        """
        node.gen.py_ast = node.body.gen.py_ast

    def exit_enum(self, node: ast.Enum) -> None:
        """Sub objects.

        name: Name,
        access: Optional[SubTag[Token]],
        base_classes: Optional[Optional[SubNodeList[AtomType]]],
        body: Optional[SubNodeList[EnumBlockStmt] | EnumDef],
        doc: Optional[String],
        decorators: Optional[SubNodeList[ExprType]],
        """
        self.needs_enum()
        body = (
            [self.sync(ast3.Pass(), node.body)]
            if isinstance(node.body, ast.SubNodeList) and not node.body.items
            else node.body.gen.py_ast
            if node.body
            else []
        )
        if not isinstance(body, list):
            raise self.ice()
        if node.doc:
            body = [node.doc.gen.py_ast, *body]
        decorators = (
            node.decorators.gen.py_ast
            if isinstance(node.decorators, ast.SubNodeList)
            else []
        )
        if isinstance(decorators, list):
            decorators.append(
                self.sync(ast3.Name(id="__jac_dataclass__", ctx=ast3.Load()))
            )
        else:
            raise self.ice()
        base_classes = node.base_classes.gen.py_ast if node.base_classes else []
        if isinstance(base_classes, list):
            base_classes.append(
                self.sync(ast3.Name(id="__jac_Enum__", ctx=ast3.Load()))
            )
        else:
            raise self.ice()
        node.gen.py_ast = self.sync(
            ast3.ClassDef(
                name=node.name.value,
                bases=base_classes,
                keywords=[],
                body=body,
                decorator_list=decorators,
                type_params=[],
            )
        )

    def exit_enum_def(self, node: ast.EnumDef) -> None:
        """Sub objects.

        target: ArchRefChain,
        body: SubNodeList[EnumBlockStmt],
        doc: Optional[String],
        decorators: Optional[SubNodeList[ExprType]],
        """
        node.gen.py_ast = node.body.gen.py_ast

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

    def exit_ability_def(self, node: ast.AbilityDef) -> None:
        """Sub objects.

        target: ArchRefChain,
        signature: FuncSignature | EventSignature,
        body: SubNodeList[CodeBlockStmt],
        doc: Optional[String],
        decorators: Optional[SubNodeList[ExprType]],
        """

    def exit_func_signature(self, node: ast.FuncSignature) -> None:
        """Sub objects.

        params: Optional[SubNodeList[ParamVar]],
        return_type: Optional[SubTag[ExprType]],
        """

    def exit_event_signature(self, node: ast.EventSignature) -> None:
        """Sub objects.

        event: Token,
        arch_tag_info: Optional[ExprType],
        return_type: Optional[SubTag[ExprType]],
        """

    def exit_arch_ref(self, node: ast.ArchRef) -> None:
        """Sub objects.

        name_ref: NameType,
        arch: Token,
        """

    def exit_arch_ref_chain(self, node: ast.ArchRefChain) -> None:
        """Sub objects.

        archs: Sequence[ArchRef],
        """

    def exit_param_var(self, node: ast.ParamVar) -> None:
        """Sub objects.

        name: Name,
        unpack: Optional[Token],
        type_tag: SubTag[ExprType],
        value: Optional[ExprType],
        """

    def exit_arch_has(self, node: ast.ArchHas) -> None:
        """Sub objects.

        is_static: bool,
        access: Optional[SubTag[Token]],
        vars: SubNodeList[HasVar],
        is_frozen: bool,
        doc: Optional[String],
        """

    def exit_has_var(self, node: ast.HasVar) -> None:
        """Sub objects.

        name: Name,
        type_tag: SubTag[ExprType],
        value: Optional[ExprType],
        """

    def exit_typed_ctx_block(self, node: ast.TypedCtxBlock) -> None:
        """Sub objects.

        type_ctx: ExprType,
        body: SubNodeList[CodeBlockStmt],
        """

    def exit_if_stmt(self, node: ast.IfStmt) -> None:
        """Sub objects.

        condition: ExprType,
        body: SubNodeList[CodeBlockStmt],
        else_body: Optional[ElseStmt | ElseIf],
        """

    def exit_else_if(self, node: ast.ElseIf) -> None:
        """Sub objects.

        condition: ExprType,
        body: SubNodeList[CodeBlockStmt],
        else_body: Optional[ElseStmt | ElseIf],
        """

    def exit_else_stmt(self, node: ast.ElseStmt) -> None:
        """Sub objects.

        body: SubNodeList[CodeBlockStmt],
        """

    def exit_try_stmt(self, node: ast.TryStmt) -> None:
        """Sub objects.

        body: SubNodeList[CodeBlockStmt],
        excepts: Optional[SubNodeList[Except]],
        else_body: Optional[ElseStmt],
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
        is_async: bool,
        condition: ExprType,
        count_by: ExprType,
        body: SubNodeList[CodeBlockStmt],
        else_body: Optional[ElseStmt],
        """

    def exit_in_for_stmt(self, node: ast.InForStmt) -> None:
        """Sub objects.

        name_list: SubNodeList[Name],
        is_async: bool,
        collection: ExprType,
        body: SubNodeList[CodeBlockStmt],
        else_body: Optional[ElseStmt],
        """

    def exit_while_stmt(self, node: ast.WhileStmt) -> None:
        """Sub objects.

        condition: ExprType,
        body: SubNodeList[CodeBlockStmt],
        """

    def exit_with_stmt(self, node: ast.WithStmt) -> None:
        """Sub objects.

        is_async: bool,
        exprs: SubNodeList[ExprAsItem],
        body: SubNodeList[CodeBlockStmt],
        """

    def exit_expr_as_item(self, node: ast.ExprAsItem) -> None:
        """Sub objects.

        expr: ExprType,
        alias: Optional[ExprType],
        """

    def exit_raise_stmt(self, node: ast.RaiseStmt) -> None:
        """Sub objects.

        cause: Optional[ExprType],
        from_target: Optional[ExprType],
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

        target: SubNodeList[AtomType],
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

        vis_type: Optional[SubNodeList[AtomType]],
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

    def exit_global_stmt(self, node: ast.GlobalStmt) -> None:
        """Sub objects.

        target: SubNodeList[NameType],
        """

    def exit_non_local_stmt(self, node: ast.NonLocalStmt) -> None:
        """Sub objects.

        target: SubNodeList[NameType],
        """

    def exit_assignment(self, node: ast.Assignment) -> None:
        """Sub objects.

        target: SubNodeList[AtomType],
        value: Optional[ExprType | YieldStmt],
        type_tag: Optional[SubTag[ExprType]],
        mutable: bool =True,
        """

    def exit_binary_expr(self, node: ast.BinaryExpr) -> None:
        """Sub objects.

        left: ExprType,
        right: ExprType,
        op: Token | DisconnectOp | ConnectOp,
        """

    def exit_lambda_expr(self, node: ast.LambdaExpr) -> None:
        """Sub objects.

        params: Optional[SubNodeList[ParamVar]],
        return_type: Optional[SubTag[ExprType]],
        body: ExprType,
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

        strings: Sequence[String | FString],
        """

    def exit_f_string(self, node: ast.FString) -> None:
        """Sub objects.

        parts: Optional[SubNodeList[String | ExprType]],
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

        kv_pairs: Sequence[KVPair],
        """

    def exit_k_v_pair(self, node: ast.KVPair) -> None:
        """Sub objects.

        key: ExprType,
        value: ExprType,
        """

    def exit_inner_compr(self, node: ast.InnerCompr) -> None:
        """Sub objects.

        out_expr: ExprType,
        names: SubNodeList[AtomType],
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
        names: SubNodeList[AtomType],
        collection: ExprType,
        conditional: Optional[ExprType],
        """

    def exit_atom_trailer(self, node: ast.AtomTrailer) -> None:
        """Sub objects.

        target: AtomType,
        right: AtomType,
        is_scope_contained: bool,
        """

    def exit_atom_unit(self, node: ast.AtomUnit) -> None:
        """Sub objects.

        value: AtomType | ExprType,
        is_paren: bool,
        is_null_ok: bool,
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
        step: Optional[ExprType],
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

    def exit_match_stmt(self, node: ast.MatchStmt) -> None:
        """Sub objects.

        target: SubNodeList[ExprType],
        cases: list[MatchCase],
        """

    def exit_match_case(self, node: ast.MatchCase) -> None:
        """Sub objects.

        pattern: MatchPattern,
        guard: Optional[ExprType],
        body: SubNodeList[CodeBlockStmt],
        """

    def exit_match_or(self, node: ast.MatchOr) -> None:
        """Sub objects.

        patterns: list[MatchPattern],
        """

    def exit_match_as(self, node: ast.MatchAs) -> None:
        """Sub objects.

        name: NameType,
        pattern: MatchPattern,
        """

    def exit_match_wild(self, node: ast.MatchWild) -> None:
        """Sub objects."""

    def exit_match_value(self, node: ast.MatchValue) -> None:
        """Sub objects.

        value: ExprType,
        """

    def exit_match_singleton(self, node: ast.MatchSingleton) -> None:
        """Sub objects.

        value: Bool | Null,
        """

    def exit_match_sequence(self, node: ast.MatchSequence) -> None:
        """Sub objects.

        values: list[MatchPattern],
        """

    def exit_match_mapping(self, node: ast.MatchMapping) -> None:
        """Sub objects.

        values: list[MatchKVPair | MatchStar],
        """

    def exit_match_k_v_pair(self, node: ast.MatchKVPair) -> None:
        """Sub objects.

        key: MatchPattern | NameType,
        value: MatchPattern,
        """

    def exit_match_star(self, node: ast.MatchStar) -> None:
        """Sub objects.

        name: NameType,
        is_list: bool,
        """

    def exit_match_arch(self, node: ast.MatchArch) -> None:
        """Sub objects.

        name: NameType,
        arg_patterns: Optional[SubNodeList[MatchPattern]],
        kw_patterns: Optional[SubNodeList[MatchKVPair]],
        """

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
