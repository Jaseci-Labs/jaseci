"""Transpilation pass for Jaseci Ast."""
from typing import List

import jaclang.jac.jac_ast as ast
from jaclang.jac.jac_ast import AstNode
from jaclang.jac.passes.ir_pass import Pass
from jaclang.utils.log import logging


logger = logging.getLogger(__name__)


class PyCodeGenPass(Pass):
    """Jac transpilation to python pass."""

    marked_incomplete: List[str] = []

    def __init__(self: "PyCodeGenPass") -> None:
        """Initialize pass."""
        self.indent_size = 4
        self.indent_level = 0
        self.cur_arch = None  # tracks current architype during transpilation
        super().__init__()

    def enter_node(self: Pass, node: AstNode) -> None:
        """Enter node."""
        if node:
            node.meta["py_code"] = ""
        return Pass.enter_node(self, node)

    def indent_str(self: "PyCodeGenPass", indent_delta: int) -> str:
        """Return string for indent."""
        return " " * self.indent_size * (self.indent_level + indent_delta)

    def emit_ln(
        self: "PyCodeGenPass", node: AstNode, s: str, indent_delta: int = 0
    ) -> None:
        """Emit code to node."""
        node.meta["py_code"] += (
            self.indent_str(indent_delta)
            + s.replace("\n", "\n" + self.indent_str(indent_delta))
            + "\n"
        )

    def emit(self: "PyCodeGenPass", node: AstNode, s: str) -> None:
        """Emit code to node."""
        node.meta["py_code"] += s

    def exit_token(self: "PyCodeGenPass", node: ast.Token) -> None:
        """Sub objects.

        name: str,
        value: str,
        """
        self.emit(node, node.value)

    def exit_parse(self: "PyCodeGenPass", node: ast.Parse) -> None:
        """Sub objects.

        name: str,
        """
        logger.critical("Parse node should not be in this AST!!")
        raise ValueError("Parse node should not be in AST after being Built!!")

    def exit_module(self: "PyCodeGenPass", node: ast.Module) -> None:
        """Sub objects.

        name: str,
        doc: Token,
        body: "Elements",
        """
        self.emit_ln(node, node.doc.value)
        self.emit(node, node.body.meta["py_code"])
        self.ir = node

    def exit_elements(self: "PyCodeGenPass", node: ast.Elements) -> None:
        """Sub objects.

        elements: List[GlobalVars | Test | ModuleCode | Import | Architype | Ability | AbilitySpec],
        """
        for i in node.elements:
            self.emit(node, i.meta["py_code"])

    @Pass.incomplete
    def exit_global_vars(self: "PyCodeGenPass", node: ast.GlobalVars) -> None:
        """Sub objects.

        doc: "DocString",
        access: Optional[Token],
        assignments: "AssignmentList",
        """
        self.emit_ln(node, node.assignments.meta["py_code"])

    @Pass.incomplete
    def exit_test(self: "PyCodeGenPass", node: ast.Test) -> None:
        """Sub objects.

        name: Token,
        doc: "DocString",
        description: Token,
        body: "CodeBlock",
        """

    def exit_module_code(self: "PyCodeGenPass", node: ast.ModuleCode) -> None:
        """Sub objects.

        doc: "DocString",
        body: "CodeBlock",
        """
        self.emit(node, node.doc.meta["py_code"])
        self.emit(node, node.body.meta["py_code"])

    def exit_doc_string(self: "PyCodeGenPass", node: ast.DocString) -> None:
        """Sub objects.

        value: Optional[Token],
        """
        if type(node.value) == ast.Token:
            self.emit_ln(node, node.value.value)

    @Pass.incomplete
    def exit_import(self: "PyCodeGenPass", node: ast.Import) -> None:
        """Sub objects.

        lang: Token,
        path: "ModulePath",
        alias: Optional[Token],
        items: Optional["ModuleItems"],
        is_absorb: bool,  # For includes
        """
        if not node.items:
            if not node.alias:
                self.emit_ln(node, f"import {node.path.meta['py_code']}")
            else:
                self.emit_ln(
                    node,
                    f"import {node.path.meta['py_code']} as {node.alias.meta['py_code']}",
                )
        else:
            self.emit_ln(
                node,
                f"from {node.path.meta['py_code']} import {node.items.meta['py_code']}",
            )

    def exit_module_path(self: "PyCodeGenPass", node: ast.ModulePath) -> None:
        """Sub objects.

        path: List[Token],
        """
        self.emit(node, "".join([i.value for i in node.path]))

    def exit_module_items(self: "PyCodeGenPass", node: ast.ModuleItems) -> None:
        """Sub objects.

        items: List["ModuleItem"],
        """
        self.emit(node, ", ".join([i.meta["py_code"] for i in node.items]))

    def exit_module_item(self: "PyCodeGenPass", node: ast.ModuleItem) -> None:
        """Sub objects.

        name: Token,
        alias: Optional[Token],
        """
        if type(node.alias) == ast.Token:
            self.emit(node, node.name.value + " as " + node.alias.value)
        else:
            self.emit(node, node.name.value)

    @Pass.incomplete
    def exit_architype(self: "PyCodeGenPass", node: ast.Architype) -> None:
        """Sub objects.

        name: Token,
        typ: Token,
        doc: DocString,
        access: Token,
        base_classes: "BaseClasses",
        body: "ArchBlock",
        """
        if not node.base_classes:
            self.emit_ln(node, f"class {node.name.meta['py_code']}:")
        else:
            self.emit_ln(
                node,
                f"class {node.name.meta['py_code']}({node.base_classes.meta['py_code']}):",
            )
        self.emit_ln(node, node.doc.meta["py_code"], indent_delta=1)
        self.emit(node, node.body.meta["py_code"])

    @Pass.incomplete
    def exit_arch_decl(self: "PyCodeGenPass", node: ast.ArchDecl) -> None:
        """Sub objects.

        doc: DocString,
        access: Token,
        typ: Token,
        name: Token,
        base_classes: "BaseClasses",
        self.def_link: Optional["ArchDef"] = None
        """

    @Pass.incomplete
    def exit_arch_def(self: "PyCodeGenPass", node: ast.ArchDef) -> None:
        """Sub objects.

        doc: DocString,
        mod: Token,
        arch: "ObjectRef | NodeRef | EdgeRef | WalkerRef",
        body: "ArchBlock",
        """

    def exit_base_classes(self: "PyCodeGenPass", node: ast.BaseClasses) -> None:
        """Sub objects.

        base_classes: List[Token],
        """
        self.emit(node, ", ".join([i.value for i in node.base_classes]))

    @Pass.incomplete
    def exit_ability(self: "PyCodeGenPass", node: ast.Ability) -> None:
        """Sub objects.

         name: Token,
        is_func: bool,
        doc: DocString,
        access: Optional[Token],
        signature: FuncSignature | TypeSpec,
        body: CodeBlock,
        """
        self.emit_ln(node, f"def {node.name.value}{node.signature.meta['py_code']}:")
        self.emit_ln(node, node.doc.meta["py_code"], indent_delta=1)
        self.emit(node, node.body.meta["py_code"])

    def exit_ability_decl(self: "PyCodeGenPass", node: ast.AbilityDecl) -> None:
        """Sub objects.

        doc: DocString,
        access: Optional[Token],
        name: Token,
        signature: FuncSignature | TypeSpec,
        is_func: bool,
        """

    def exit_ability_def(self: "PyCodeGenPass", node: ast.AbilityDef) -> None:
        """Sub objects.

        doc: DocString,
        mod: Optional[Token],
        ability: AbilityRef,
        body: CodeBlock,
        """

    def exit_ability_spec(self: "PyCodeGenPass", node: ast.AbilitySpec) -> None:
        """Sub objects.

        doc: DocString,
        name: Token,
        arch: ObjectRef | NodeRef | EdgeRef | WalkerRef,
        mod: Optional[Token],
        signature: Optional[FuncSignature],
        body: CodeBlock,
        """

    def exit_arch_block(self: "PyCodeGenPass", node: ast.ArchBlock) -> None:
        """Sub objects.

        members: List[ArchHas | ArchCan | ArchCanDecl ],
        """

    def exit_arch_has(self: "PyCodeGenPass", node: ast.ArchHas) -> None:
        """Sub objects.

        doc: DocString,
        access: Optional[Token],
        vars: HasVarList,
        """

    def exit_has_var(self: "PyCodeGenPass", node: ast.HasVar) -> None:
        """Sub objects.

        name: Token,
        type_tag: TypeSpec,
        value: Optional[AstNode],
        """

    def exit_has_var_list(self: "PyCodeGenPass", node: ast.HasVarList) -> None:
        """Sub objects.

        vars: List[HasVar],
        """

    def exit_type_spec(self: "PyCodeGenPass", node: ast.TypeSpec) -> None:
        """Sub objects.

        typ: Token,
        nested1: TypeSpec,
        nested2: TypeSpec,
        """

    def exit_arch_can(self: "PyCodeGenPass", node: ast.ArchCan) -> None:
        """Sub objects.

        name: Token,
        doc: DocString,
        access: Optional[Token],
        signature: Optional[EventSignature | FuncSignature],
        body: CodeBlock,
        """

    def exit_arch_can_decl(self: "PyCodeGenPass", node: ast.ArchCanDecl) -> None:
        """Sub objects.

        name: Token,
        doc: DocString,
        access: Optional[Token],
        signature: Optional[EventSignature | FuncSignature],
        """

    def exit_event_signature(self: "PyCodeGenPass", node: ast.EventSignature) -> None:
        """Sub objects.

        event: Token,
        arch_tag_info: Optional[NameList | Token],
        """

    def exit_name_list(self: "PyCodeGenPass", node: ast.NameList) -> None:
        """Sub objects.

        names: list,
        """

    def exit_func_signature(self: "PyCodeGenPass", node: ast.FuncSignature) -> None:
        """Sub objects.

        params: Optional[FuncParams],
        return_type: Optional[TypeSpec],
        """

    def exit_func_params(self: "PyCodeGenPass", node: ast.FuncParams) -> None:
        """Sub objects.

        params: list,
        """

    def exit_param_var(self: "PyCodeGenPass", node: ast.ParamVar) -> None:
        """Sub objects.

        name: Token,
        type_tag: TypeSpec,
        value: Optional[AstNode],
        """

    def exit_code_block(self: "PyCodeGenPass", node: ast.CodeBlock) -> None:
        """Sub objects.

        stmts: list,
        """

    def exit_if_stmt(self: "PyCodeGenPass", node: ast.IfStmt) -> None:
        """Sub objects.

        condition: ExprType,
        body: CodeBlock,
        elseifs: Optional[ElseIfs],
        else_body: Optional[ElseStmt],
        """

    def exit_else_ifs(self: "PyCodeGenPass", node: ast.ElseIfs) -> None:
        """Sub objects.

        elseifs: List[IfStmt],
        """

    def exit_else_stmt(self: "PyCodeGenPass", node: ast.ElseStmt) -> None:
        """Sub objects.

        body: CodeBlock,
        """

    def exit_try_stmt(self: "PyCodeGenPass", node: ast.TryStmt) -> None:
        """Sub objects.

        body: CodeBlock,
        excepts: Optional[ExceptList],
        finally_body: Optional[FinallyStmt],
        """

    def exit_except(self: "PyCodeGenPass", node: ast.Except) -> None:
        """Sub objects.

        typ: ExprType,
        name: Optional[Token],
        body: CodeBlock,
        """

    def exit_except_list(self: "PyCodeGenPass", node: ast.ExceptList) -> None:
        """Sub objects.

        excepts: List[Except],
        """

    def exit_finally_stmt(self: "PyCodeGenPass", node: ast.FinallyStmt) -> None:
        """Sub objects.

        body: CodeBlock,
        """

    def exit_iter_for_stmt(self: "PyCodeGenPass", node: ast.IterForStmt) -> None:
        """Sub objects.

        iter: Assignment,
        condition: ExprType,
        count_by: ExprType,
        body: CodeBlock,
        """

    def exit_in_for_stmt(self: "PyCodeGenPass", node: ast.InForStmt) -> None:
        """Sub objects.

        name: Token,
        collection: ExprType,
        body: CodeBlock,
        """

    def exit_dict_for_stmt(self: "PyCodeGenPass", node: ast.DictForStmt) -> None:
        """Sub objects.

        k_name: Token,
        v_name: Token,
        collection: ExprType,
        body: CodeBlock,
        """

    def exit_while_stmt(self: "PyCodeGenPass", node: ast.WhileStmt) -> None:
        """Sub objects.

        condition: ExprType,
        body: CodeBlock,
        """

    def exit_raise_stmt(self: "PyCodeGenPass", node: ast.RaiseStmt) -> None:
        """Sub objects.

        cause: Optional[ExprType],
        """

    def exit_assert_stmt(self: "PyCodeGenPass", node: ast.AssertStmt) -> None:
        """Sub objects.

        condition: ExprType,
        error_msg: Optional[ExprType],
        """

    def exit_ctrl_stmt(self: "PyCodeGenPass", node: ast.CtrlStmt) -> None:
        """Sub objects.

        ctrl: Token,
        """

    def exit_delete_stmt(self: "PyCodeGenPass", node: ast.DeleteStmt) -> None:
        """Sub objects.

        target: ExprType,
        """

    def exit_report_stmt(self: "PyCodeGenPass", node: ast.ReportStmt) -> None:
        """Sub objects.

        expr: ExprType,
        """

    def exit_return_stmt(self: "PyCodeGenPass", node: ast.ReturnStmt) -> None:
        """Sub objects.

        expr: Optional[ExprType],
        """

    def exit_yield_stmt(self: "PyCodeGenPass", node: ast.YieldStmt) -> None:
        """Sub objects.

        expr: Optional[ExprType],
        """

    def exit_ignore_stmt(self: "PyCodeGenPass", node: ast.IgnoreStmt) -> None:
        """Sub objects.

        target: ExprType,
        """

    def exit_visit_stmt(self: "PyCodeGenPass", node: ast.VisitStmt) -> None:
        """Sub objects.

        typ: Optional[Token],
        target: Optional[ExprType],
        else_body: Optional[ElseStmt],
        """

    def exit_revisit_stmt(self: "PyCodeGenPass", node: ast.RevisitStmt) -> None:
        """Sub objects.

        hops: Optional[ExprType],
        else_body: Optional[ElseStmt],
        """

    def exit_disengage_stmt(self: "PyCodeGenPass", node: ast.DisengageStmt) -> None:
        """Sub objects."""

    def exit_sync_stmt(self: "PyCodeGenPass", node: ast.SyncStmt) -> None:
        """Sub objects.

        target: ExprType,
        """

    def exit_assignment(self: "PyCodeGenPass", node: ast.Assignment) -> None:
        """Sub objects.

        is_static: bool,
        target: AtomType,
        value: ExprType,
        """

    def exit_binary_expr(self: "PyCodeGenPass", node: ast.BinaryExpr) -> None:
        """Sub objects.

        left: ExprType,
        right: ExprType,
        op: Token,
        """

    def exit_if_else_expr(self: "PyCodeGenPass", node: ast.IfElseExpr) -> None:
        """Sub objects.

        condition: BinaryExpr | IfElseExpr,
        value: ExprType,
        else_value: ExprType,
        """

    def exit_unary_expr(self: "PyCodeGenPass", node: ast.UnaryExpr) -> None:
        """Sub objects.

        operand: ExprType,
        op: Token,
        """

    def exit_spawn_object_expr(
        self: "PyCodeGenPass", node: ast.SpawnObjectExpr
    ) -> None:
        """Sub objects.

        target: ExprType,
        """

    def exit_unpack_expr(self: "PyCodeGenPass", node: ast.UnpackExpr) -> None:
        """Sub objects.

        target: ExprType,
        is_dict: bool,
        """

    def exit_multi_string(self: "PyCodeGenPass", node: ast.MultiString) -> None:
        """Sub objects.

        strings: List[Token],
        """

    def exit_list_val(self: "PyCodeGenPass", node: ast.ListVal) -> None:
        """Sub objects.

        values: List[ExprType],
        """

    def exit_expr_list(self: "PyCodeGenPass", node: ast.ExprList) -> None:
        """Sub objects.

        values: List[ExprType],
        """

    def exit_dict_val(self: "PyCodeGenPass", node: ast.DictVal) -> None:
        """Sub objects.

        kv_pairs: list,
        """

    def exit_comprehension(self: "PyCodeGenPass", node: ast.Comprehension) -> None:
        """Sub objects.

        key_expr: Optional[ExprType],
        out_expr: ExprType,
        name: Token,
        collection: ExprType,
        conditional: Optional[ExprType],
        """

    def exit_k_v_pair(self: "PyCodeGenPass", node: ast.KVPair) -> None:
        """Sub objects.

        key: ExprType,
        value: ExprType,
        """

    def exit_atom_trailer(self: "PyCodeGenPass", node: ast.AtomTrailer) -> None:
        """Sub objects.

        target: AtomType,
        right: IndexSlice | ArchRefType | Token,
        null_ok: bool,
        """

    def exit_func_call(self: "PyCodeGenPass", node: ast.FuncCall) -> None:
        """Sub objects.

        target: AtomType,
        params: Optional[ParamList],
        """

    def exit_param_list(self: "PyCodeGenPass", node: ast.ParamList) -> None:
        """Sub objects.

        p_args: Optional[ExprList],
        p_kwargs: Optional[AssignmentList],
        """

    def exit_assignment_list(self: "PyCodeGenPass", node: ast.AssignmentList) -> None:
        """Sub objects.

        values: List[ExprType],
        """

    def exit_index_slice(self: "PyCodeGenPass", node: ast.IndexSlice) -> None:
        """Sub objects.

        start: ExprType,
        stop: Optional[ExprType],
        """

    def exit_global_ref(self: "PyCodeGenPass", node: ast.GlobalRef) -> None:
        """Sub objects.

        name: Token,
        """

    def exit_here_ref(self: "PyCodeGenPass", node: ast.HereRef) -> None:
        """Sub objects.

        name: Optional[Token],
        """

    def exit_visitor_ref(self: "PyCodeGenPass", node: ast.VisitorRef) -> None:
        """Sub objects.

        name: Optional[Token],
        """

    def exit_node_ref(self: "PyCodeGenPass", node: ast.NodeRef) -> None:
        """Sub objects.

        name: Token,
        """

    def exit_edge_ref(self: "PyCodeGenPass", node: ast.EdgeRef) -> None:
        """Sub objects.

        name: Token,
        """

    def exit_walker_ref(self: "PyCodeGenPass", node: ast.WalkerRef) -> None:
        """Sub objects.

        name: Token,
        """

    def exit_func_ref(self: "PyCodeGenPass", node: ast.FuncRef) -> None:
        """Sub objects.

        name: Token,
        """

    def exit_object_ref(self: "PyCodeGenPass", node: ast.ObjectRef) -> None:
        """Sub objects.

        name: Token,
        """

    def exit_ability_ref(self: "PyCodeGenPass", node: ast.AbilityRef) -> None:
        """Sub objects.

        name: Token,
        """

    def exit_edge_op_ref(self: "PyCodeGenPass", node: ast.EdgeOpRef) -> None:
        """Sub objects.

        filter_cond: Optional[ExprType],
        edge_dir: EdgeDir,
        """

    def exit_disconnect_op(self: "PyCodeGenPass", node: ast.DisconnectOp) -> None:
        """Sub objects.

        filter_cond: Optional[ExprType],
        edge_dir: EdgeDir,
        """

    def exit_connect_op(self: "PyCodeGenPass", node: ast.ConnectOp) -> None:
        """Sub objects.

        spawn: Optional[ExprType],
        edge_dir: EdgeDir,
        """

    def exit_spawn_ctx(self: "PyCodeGenPass", node: ast.SpawnCtx) -> None:
        """Sub objects.

        spawns: List[Assignment],
        """

    def exit_filter_ctx(self: "PyCodeGenPass", node: ast.FilterCtx) -> None:
        """Sub objects.

        compares: List[BinaryExpr],
        """
