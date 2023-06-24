"""Transpilation pass for Jaseci Ast."""
import jaclang.jac.absyntree as ast
from jaclang.jac.absyntree import AstNode
from jaclang.jac.passes.ir_pass import Pass


class BluePygenPass(Pass):
    """Jac transpilation to python pass."""

    marked_incomplete: list[str] = []

    def before_pass(self) -> None:
        """Initialize pass."""
        self.indent_size = 4
        self.indent_level = 0
        self.cur_arch = None  # tracks current architype during transpilation

    def enter_node(self, node: AstNode) -> None:
        """Enter node."""
        if node:
            node.meta["py_code"] = ""
        return Pass.enter_node(self, node)

    def indent_str(self, indent_delta: int) -> str:
        """Return string for indent."""
        return " " * self.indent_size * (self.indent_level + indent_delta)

    def emit_ln(self, node: AstNode, s: str, indent_delta: int = 0) -> None:
        """Emit code to node."""
        self.emit(node, s.strip().strip("\n"), indent_delta)
        self.emit(node, "\n")

    def emit(self, node: AstNode, s: str, indent_delta: int = 0) -> None:
        """Emit code to node."""
        node.meta["py_code"] += self.indent_str(indent_delta) + s.replace(
            "\n", "\n" + self.indent_str(indent_delta)
        )

    def access_check(self, node: ast.OOPAccessNode) -> None:
        """Check if node uses access."""
        if node.access:
            self.warning(
                f"Line {node.line}, Access specifiers not supported in bootstrap Jac."
            )

    def decl_def_warn(self) -> None:
        """Warn about declaration."""
        self.warning(
            "Separate declarations and definitions not supported in bootstrap Jac."
        )

    def ds_feature_warn(self) -> None:
        """Warn about feature."""
        self.warning("Data spatial features not supported in bootstrap Jac.")

    def exit_token(self, node: ast.Token) -> None:
        """Sub objects.

        name: str,
        value: str,
        """
        self.emit(node, node.value)

    def exit_parse(self, node: ast.Parse) -> None:
        """Sub objects.

        name: str,
        """
        self.error(f"Parse node should not be in this AST!! {node.name}")
        raise ValueError("Parse node should not be in AST after being Built!!")

    def exit_module(self, node: ast.Module) -> None:
        """Sub objects.

        name: str,
        doc: Token,
        body: "Elements",
        """
        self.emit_ln(node, node.doc.value)
        self.emit(node, node.body.meta["py_code"])
        self.ir = node

    def exit_elements(self, node: ast.Elements) -> None:
        """Sub objects.

        elements: list[GlobalVars | Test | ModuleCode | Import | Architype | Ability | AbilitySpec],
        """
        for i in node.elements:
            self.emit_ln(node, i.meta["py_code"])

    # NOTE: Incomplete for Jac Purple and Red
    def exit_global_vars(self, node: ast.GlobalVars) -> None:
        """Sub objects.

        doc: Optional["DocString"],
        access: Optional[Token],
        assignments: "AssignmentList",
        """
        self.access_check(node)
        self.emit_ln(node, node.assignments.meta["py_code"])

    # NOTE: Incomplete for Jac Purple and Red
    def exit_test(self, node: ast.Test) -> None:
        """Sub objects.

        name: Token,
        doc: Optional["DocString"],
        description: Token,
        body: "CodeBlock",
        """
        self.warning(f"Line {node.line}, Test feature not supported in bootstrap Jac.")

    def exit_module_code(self, node: ast.ModuleCode) -> None:
        """Sub objects.

        doc: Optional["DocString"],
        body: "CodeBlock",
        """
        if node.doc:
            self.emit(node, node.doc.meta["py_code"])
        self.emit(node, node.body.meta["py_code"])

    def exit_doc_string(self, node: ast.DocString) -> None:
        """Sub objects.

        value: Optional[Token],
        """
        if type(node.value) == ast.Token:
            self.emit_ln(node, node.value.value)

    # NOTE: Incomplete for Jac Purple and Red
    def exit_import(self, node: ast.Import) -> None:
        """Sub objects.

        lang: Token,
        path: "ModulePath",
        alias: Optional[Token],
        items: Optional["ModuleItems"],
        is_absorb: bool,  # For includes
        """
        if node.lang.value != "py":
            self.warning(
                f"Line {node.line}, Importing non-python modules not supported in bootstrap Jac."
            )
        if node.is_absorb:
            self.warning(f"Line {node.line}, Includes not supported in bootstrap Jac.")
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

    def exit_module_path(self, node: ast.ModulePath) -> None:
        """Sub objects.

        path: list[Token],
        """
        self.emit(node, "".join([i.value for i in node.path]))

    def exit_module_items(self, node: ast.ModuleItems) -> None:
        """Sub objects.

        items: list["ModuleItem"],
        """
        self.emit(node, ", ".join([i.meta["py_code"] for i in node.items]))

    def exit_module_item(self, node: ast.ModuleItem) -> None:
        """Sub objects.

        name: Token,
        alias: Optional[Token],
        """
        if type(node.alias) == ast.Token:
            self.emit(node, node.name.value + " as " + node.alias.value)
        else:
            self.emit(node, node.name.value)

    # NOTE: Incomplete for Jac Purple and Red
    def exit_architype(self, node: ast.Architype) -> None:
        """Sub objects.

        name: Token,
        typ: Token,
        doc: Optional[DocString],
        decorators: Optional["ExprList"],
        access: Optional[Token],
        base_classes: "BaseClasses",
        body: "ArchBlock",
        """
        self.access_check(node)
        if node.decorators:
            self.emit_ln(node, node.decorators.meta["py_code"])
        if not node.base_classes:
            self.emit_ln(node, f"class {node.name.meta['py_code']}:")
        else:
            self.emit_ln(
                node,
                f"class {node.name.meta['py_code']}({node.base_classes.meta['py_code']}):",
            )
        if node.doc:
            self.emit_ln(node, node.doc.meta["py_code"], indent_delta=1)
        if node.body:
            self.emit_ln(node, node.body.meta["py_code"], indent_delta=1)
        else:
            self.decl_def_warn()

    # NOTE: Incomplete for Jac Purple and Red
    def exit_arch_def(self, node: ast.ArchDef) -> None:
        """Sub objects.

        doc: Optional[DocString],
        mod: Optional["NameList"],
        arch: "ObjectRef | NodeRef | EdgeRef | WalkerRef",
        body: "ArchBlock",
        """
        self.decl_def_warn()

    def exit_decorators(self, node: ast.Decorators) -> None:
        """Sub objects.

        calls: list["ExprType"],
        """
        for i in node.calls:
            self.emit_ln(node, "@" + i.meta["py_code"])

    def exit_base_classes(self, node: ast.BaseClasses) -> None:
        """Sub objects.

        base_classes: list[NameList],
        """
        self.emit(node, ", ".join([i.meta["py_code"] for i in node.base_classes]))

    # NOTE: Incomplete for Jac Purple and Red
    def exit_ability(self, node: ast.Ability) -> None:
        """Sub objects.

        name: Token,
        is_func: bool,
        doc: Optional[DocString],
        decorators: Optional["Decorators"],
        access: Optional[Token],
        signature: FuncSignature | TypeSpec,
        body: CodeBlock,
        """
        self.access_check(node)
        if node.decorators:
            self.emit_ln(node, node.decorators.meta["py_code"])
        if node.is_func:
            self.emit_ln(
                node, f"def {node.name.value}{node.signature.meta['py_code']}:"
            )
        else:
            self.emit_ln(node, f"def {node.name.value}():")
            self.ds_feature_warn()
        if node.doc:
            self.emit_ln(node, node.doc.meta["py_code"], indent_delta=1)
        if node.body:
            self.emit_ln(node, node.body.meta["py_code"], indent_delta=1)
        else:
            self.decl_def_warn()

    # NOTE: Incomplete for Jac Purple and Red
    def exit_ability_def(self, node: ast.AbilityDef) -> None:
        """Sub objects.

        doc: Optional[DocString],
        mod: Optional["NameList"],
        ability: AbilityRef,
        body: CodeBlock,
        """
        self.decl_def_warn()

    # NOTE: Incomplete for Jac Purple and Red
    def exit_ability_spec(self, node: ast.AbilitySpec) -> None:
        """Sub objects.

        doc: Optional[DocString],
        name: Token,
        arch: ObjectRef | NodeRef | EdgeRef | WalkerRef,
        mod: Optional["NameList"],
        signature: Optional[FuncSignature],
        body: CodeBlock,
        """
        self.decl_def_warn()

    # NOTE: Incomplete for Jac Purple and Red
    def exit_arch_block(self, node: ast.ArchBlock) -> None:
        """Sub objects.

        members: list["ArchHas | Ability"],
        """
        init_func = None
        for i in node.members:
            if type(i) == ast.Ability and i.name.value == "init" and i.is_func:
                init_func = i
        if init_func:
            self.emit_ln(node, init_func.meta["py_code"])
        self.emit_ln(node, "def __init__(self):")
        self.emit_ln(node, '"""Init generated by Jac."""', indent_delta=1)

        for i in node.members:
            if type(i) == ast.ArchHas:
                self.emit_ln(node, f"self.has_{i.h_id}()", indent_delta=1)

        for i in node.members:
            self.emit_ln(node, i.meta["py_code"])

    def exit_arch_has(self, node: ast.ArchHas) -> None:
        """Sub objects.

        doc: Optional[DocString],
        access: Optional[Token],
        vars: HasVarList,
        self.h_id = HasVar.counter
        """
        self.emit_ln(node, f"def has_{node.h_id}(self):")
        if node.doc:
            self.emit_ln(node, node.doc.meta["py_code"], indent_delta=1)
        self.emit_ln(node, node.vars.meta["py_code"], indent_delta=1)

    def exit_has_var_list(self, node: ast.HasVarList) -> None:
        """Sub objects.

        vars: list[HasVar],
        """
        for i in node.vars:
            self.emit_ln(node, i.meta["py_code"])

    def exit_has_var(self, node: ast.HasVar) -> None:
        """Sub objects.

        name: Token,
        type_tag: TypeSpec,
        value: Optional["ExprType"],
        """
        if node.value:
            self.emit(
                node,
                f"self.{node.name.value}: {node.type_tag.meta['py_code']} = {node.value.meta['py_code']}",
            )
        else:
            self.emit(
                node, f"self.{node.name.value}: {node.type_tag.meta['py_code']} = None"
            )

    def exit_type_spec(self, node: ast.TypeSpec) -> None:
        """Sub objects.

        typ: "Token | NameList",
        list_nest: TypeSpec,
        dict_nest: TypeSpec,
        """
        if node.dict_nest:
            self.emit(
                node,
                f"Dict[{node.list_nest.meta['py_code']}, {node.dict_nest.meta['py_code']}]",
            )
        elif node.list_nest:
            self.emit(node, f"list[{node.list_nest.meta['py_code']}]")
        else:
            self.emit(node, node.typ.meta["py_code"])

    # NOTE: Incomplete for Jac Purple and Red
    def exit_event_signature(self, node: ast.EventSignature) -> None:
        """Sub objects.

        event: Token,
        arch_tag_info: Optional[NameList | Token],
        """
        self.error("Event style abilities not supported in bootstrap Jac")

    def exit_name_list(self, node: ast.NameList) -> None:
        """Sub objects.

        names: list[Token],
        dotted: bool,
        """
        if node.dotted:
            self.emit(node, ".".join([i.value for i in node.names]))
        else:
            self.emit(node, ", ".join([i.value for i in node.names]))

    def exit_func_signature(self, node: ast.FuncSignature) -> None:
        """Sub objects.

        params: Optional[FuncParams],
        return_type: Optional[TypeSpec],
        """
        self.emit(node, "(")
        if node.params:
            self.emit(node, node.params.meta["py_code"])
        self.emit(node, ")")
        if node.return_type:
            self.emit(node, f" -> {node.return_type.meta['py_code']}")

    def exit_func_params(self, node: ast.FuncParams) -> None:
        """Sub objects.

        params: list["ParamVar"],
        """
        first_out = False
        for i in node.params:
            self.emit(node, ", ") if first_out else None
            self.emit(node, i.meta["py_code"])
            first_out = True

    def exit_param_var(self, node: ast.ParamVar) -> None:
        """Sub objects.

        name: Token,
        unpack: Optional[Token],
        type_tag: "TypeSpec",
        value: Optional["ExprType"],
        """
        if node.unpack:
            self.emit(node, f"{node.unpack.value}")
        if node.value:
            self.emit(
                node,
                f"{node.name.value}: {node.type_tag.meta['py_code']} = {node.value.meta['py_code']}",
            )
        else:
            self.emit(node, f"{node.name.value}: {node.type_tag.meta['py_code']}")

    def exit_code_block(self, node: ast.CodeBlock) -> None:
        """Sub objects.

        stmts: list["StmtType"],
        """
        for i in node.stmts:
            self.emit_ln(node, i.meta["py_code"])

    def exit_if_stmt(self, node: ast.IfStmt) -> None:
        """Sub objects.

        condition: ExprType,
        body: CodeBlock,
        elseifs: Optional[ElseIfs],
        else_body: Optional[ElseStmt],
        """
        self.emit_ln(node, f"if {node.condition.meta['py_code']}:")
        self.emit_ln(node, node.body.meta["py_code"], indent_delta=1)
        if node.elseifs:
            self.emit_ln(node, node.elseifs.meta["py_code"])
        if node.else_body:
            self.emit_ln(node, node.else_body.meta["py_code"])

    def exit_else_ifs(self, node: ast.ElseIfs) -> None:
        """Sub objects.

        elseifs: list[IfStmt],
        """
        for i in node.elseifs:
            self.emit_ln(node, f"elif {i.condition.meta['py_code']}:")
            self.emit_ln(node, i.body.meta["py_code"], indent_delta=1)

    def exit_else_stmt(self, node: ast.ElseStmt) -> None:
        """Sub objects.

        body: CodeBlock,
        """
        self.emit_ln(node, "else:")
        self.emit_ln(node, node.body.meta["py_code"], indent_delta=1)

    def exit_try_stmt(self, node: ast.TryStmt) -> None:
        """Sub objects.

        body: CodeBlock,
        excepts: Optional[ExceptList],
        finally_body: Optional[FinallyStmt],
        """
        self.emit_ln(node, "try:")
        self.emit_ln(node, node.body.meta["py_code"], indent_delta=1)
        if node.excepts:
            self.emit_ln(node, node.excepts.meta["py_code"])
        if node.finally_body:
            self.emit_ln(node, node.finally_body.meta["py_code"])

    def exit_except(self, node: ast.Except) -> None:
        """Sub objects.

        typ: ExprType,
        name: Optional[Token],
        body: CodeBlock,
        """
        if node.name:
            self.emit_ln(
                node, f"except {node.typ.meta['py_code']} as {node.name.value}:"
            )
        else:
            self.emit_ln(node, f"except {node.typ.meta['py_code']}:")
        self.emit_ln(node, node.body.meta["py_code"], indent_delta=1)

    def exit_except_list(self, node: ast.ExceptList) -> None:
        """Sub objects.

        excepts: list[Except],
        """
        for i in node.excepts:
            self.emit_ln(node, i.meta["py_code"])

    def exit_finally_stmt(self, node: ast.FinallyStmt) -> None:
        """Sub objects.

        body: CodeBlock,
        """
        self.emit_ln(node, "finally:")
        self.emit_ln(node, node.body.meta["py_code"], indent_delta=1)

    def exit_iter_for_stmt(self, node: ast.IterForStmt) -> None:
        """Sub objects.

        iter: Assignment,
        condition: ExprType,
        count_by: ExprType,
        body: CodeBlock,
        """
        self.emit_ln(node, f"{node.iter.meta['py_code']}")
        self.emit_ln(node, f"while {node.condition.meta['py_code']}:")
        self.emit_ln(node, node.body.meta["py_code"], indent_delta=1)
        self.emit_ln(node, f"{node.count_by.meta['py_code']}", indent_delta=1)

    def exit_in_for_stmt(self, node: ast.InForStmt) -> None:
        """Sub objects.

        name: Token,
        collection: ExprType,
        body: CodeBlock,
        """
        self.emit_ln(
            node, f"for {node.name.value} in {node.collection.meta['py_code']}:"
        )
        self.emit_ln(node, node.body.meta["py_code"], indent_delta=1)

    def exit_dict_for_stmt(self, node: ast.DictForStmt) -> None:
        """Sub objects.

        k_name: Token,
        v_name: Token,
        collection: ExprType,
        body: CodeBlock,
        """
        self.emit_ln(
            node,
            f"for {node.k_name.value}, {node.v_name.value} in {node.collection.meta['py_code']}.items():",
        )
        self.emit_ln(node, node.body.meta["py_code"], indent_delta=1)

    def exit_while_stmt(self, node: ast.WhileStmt) -> None:
        """Sub objects.

        condition: ExprType,
        body: CodeBlock,
        """
        self.emit_ln(node, f"while {node.condition.meta['py_code']}:")
        self.emit_ln(node, node.body.meta["py_code"], indent_delta=1)

    def exit_raise_stmt(self, node: ast.RaiseStmt) -> None:
        """Sub objects.

        cause: Optional[ExprType],
        """
        if node.cause:
            self.emit_ln(node, f"raise {node.cause.meta['py_code']}")
        else:
            self.emit_ln(node, "raise")

    def exit_assert_stmt(self, node: ast.AssertStmt) -> None:
        """Sub objects.

        condition: ExprType,
        error_msg: Optional[ExprType],
        """
        if node.error_msg:
            self.emit_ln(
                node,
                f"assert {node.condition.meta['py_code']}, {node.error_msg.meta['py_code']}",
            )
        else:
            self.emit_ln(node, f"assert {node.condition.meta['py_code']}")

    # NOTE: Incomplete for Jac Purple and Red
    def exit_ctrl_stmt(self, node: ast.CtrlStmt) -> None:
        """Sub objects.

        ctrl: Token,
        """
        if node.ctrl.value == "skip":
            self.error("skip is not supported in bootstrap Jac")
        else:
            self.emit_ln(node, node.ctrl.value)

    def exit_delete_stmt(self, node: ast.DeleteStmt) -> None:
        """Sub objects.

        target: ExprType,
        """
        self.emit_ln(node, f"del {node.target.meta['py_code']}")

    # NOTE: Incomplete for Jac Purple and Red
    def exit_report_stmt(self, node: ast.ReportStmt) -> None:
        """Sub objects.

        expr: ExprType,
        """
        self.ds_feature_warn()

    # NOTE: Incomplete for Jac Purple and Red  # Need to have validation that return type specified if return present
    def exit_return_stmt(self, node: ast.ReturnStmt) -> None:
        """Sub objects.

        expr: Optional[ExprType],
        """
        if node.expr:
            self.emit_ln(node, f"return {node.expr.meta['py_code']}")
        else:
            self.emit_ln(node, "return")

    def exit_yield_stmt(self, node: ast.YieldStmt) -> None:
        """Sub objects.

        expr: Optional[ExprType],
        """
        if node.expr:
            self.emit_ln(node, f"yield {node.expr.meta['py_code']}")
        else:
            self.emit_ln(node, "yield")

    # NOTE: Incomplete for Jac Purple and Red
    def exit_ignore_stmt(self, node: ast.IgnoreStmt) -> None:
        """Sub objects.

        target: ExprType,
        """
        self.ds_feature_warn()

    # NOTE: Incomplete for Jac Purple and Red
    def exit_visit_stmt(self, node: ast.VisitStmt) -> None:
        """Sub objects.

        typ: Optional[Token],
        target: Optional[ExprType],
        else_body: Optional[ElseStmt],
        """
        self.ds_feature_warn()

    # NOTE: Incomplete for Jac Purple and Red
    def exit_revisit_stmt(self, node: ast.RevisitStmt) -> None:
        """Sub objects.

        hops: Optional[ExprType],
        else_body: Optional[ElseStmt],
        """
        self.ds_feature_warn()

    # NOTE: Incomplete for Jac Purple and Red
    def exit_disengage_stmt(self, node: ast.DisengageStmt) -> None:
        """Sub objects."""
        self.ds_feature_warn()

    # NOTE: Incomplete for Jac Purple and Red
    def exit_sync_stmt(self, node: ast.SyncStmt) -> None:
        """Sub objects.

        target: ExprType,
        """
        self.ds_feature_warn()

    # NOTE: Incomplete for Jac Purple and Red
    def exit_assignment(self, node: ast.Assignment) -> None:
        """Sub objects.

        is_static: bool,
        target: AtomType,
        value: ExprType,
        """
        if node.is_static:
            self.warning("Static variable semantics is not supported in bootstrap Jac")
        self.emit(node, f"{node.target.meta['py_code']} = {node.value.meta['py_code']}")

    # NOTE: Incomplete for Jac Purple and Red
    def exit_binary_expr(self, node: ast.BinaryExpr) -> None:
        """Sub objects.

        left: ExprType,
        right: ExprType,
        op: Token,
        """
        if node.op.value in [
            *["+", "-", "*", "/", "%", "**"],
            *["//", "&", "|", "^", "<<", ">>"],
            *[">", "<", ">=", "<=", "==", "!="],
            *["and", "or", "in", "not in", "is", "is not"],
        ]:
            self.emit(
                node,
                f"{node.left.meta['py_code']} {node.op.value} {node.right.meta['py_code']}",
            )
        else:
            self.error(
                f"Binary operator {node.op.value} not supported in bootstrap Jac"
            )

    def exit_if_else_expr(self, node: ast.IfElseExpr) -> None:
        """Sub objects.

        condition: BinaryExpr | IfElseExpr,
        value: ExprType,
        else_value: ExprType,
        """
        self.emit(
            node,
            f"{node.value.meta['py_code']} if {node.condition.meta['py_code']} else {node.else_value.meta['py_code']}",
        )

    def exit_unary_expr(self, node: ast.UnaryExpr) -> None:
        """Sub objects.

        operand: ExprType,
        op: Token,
        """
        if node.op.value in ["-", "~", "+"]:
            self.emit(node, f"{node.op.value}{node.operand.meta['py_code']}")
        elif node.op.value == "not":
            self.emit(node, f"not {node.operand.meta['py_code']}")
        else:
            self.error(f"Unary operator {node.op.value} not supported in bootstrap Jac")

    # NOTE: Incomplete for Jac Purple and Red
    def exit_spawn_object_expr(self, node: ast.SpawnObjectExpr) -> None:
        """Sub objects.

        target: ExprType,
        """
        self.ds_feature_warn()

    def exit_unpack_expr(self, node: ast.UnpackExpr) -> None:
        """Sub objects.

        target: ExprType,
        is_dict: bool,
        """
        if node.is_dict:
            self.emit(node, f"**{node.target.meta['py_code']}")
        else:
            self.emit(node, f"*{node.target.meta['py_code']}")

    # NOTE: Incomplete for Jac Purple and Red  # TODO: Need to add support for fstrings
    def exit_multi_string(self, node: ast.MultiString) -> None:
        """Sub objects.

        strings: list[Token],
        """
        for string in node.strings:
            if type(string) == ast.Token:
                self.emit(node, string.value)

    def exit_list_val(self, node: ast.ListVal) -> None:
        """Sub objects.

        values: list[ExprType],
        """
        self.emit(
            node, f"[{', '.join([value.meta['py_code'] for value in node.values])}]"
        )

    def exit_expr_list(self, node: ast.ExprList) -> None:
        """Sub objects.

        values: list[ExprType],
        """
        self.emit(
            node, f"{', '.join([value.meta['py_code'] for value in node.values])}"
        )

    def exit_dict_val(self, node: ast.DictVal) -> None:
        """Sub objects.

        kv_pairs: list["KVPair"],
        """
        self.emit(
            node,
            f"{{{', '.join([kv_pair.meta['py_code'] for kv_pair in node.kv_pairs])}}}",
        )

    def exit_list_compr(self, node: ast.ListCompr) -> None:
        """Sub objects.

        out_expr: "ExprType",
        name: Token,
        collection: "ExprType",
        conditional: Optional["ExprType"],
        """
        partial = (
            f"{node.out_expr.meta['py_code']} for {node.name.value} "
            f"in {node.collection.meta['py_code']}"
        )
        if node.conditional:
            partial += f" if {node.conditional.meta['py_code']}"
        self.emit(node, f"[{partial}]")

    def exit_dict_compr(self, node: ast.DictCompr) -> None:
        """Sub objects.

        outk_expr: "ExprType",
        outv_expr: "ExprType",
        k_name: Token,
        v_name: Optional[Token],
        collection: "ExprType",
        conditional: Optional["ExprType"],
        """
        partial = (
            f"{node.outk_expr.meta['py_code']}: {node.outv_expr.meta['py_code']} for "
            f"{node.k_name.value} in {node.collection.meta['py_code']}"
        )
        if node.v_name:
            partial += f", {node.v_name.value}"
        partial += f" in {node.collection.meta['py_code']}"
        if node.conditional:
            partial += f" if {node.conditional.meta['py_code']}"
        self.emit(node, f"[{partial}]")

    def exit_k_v_pair(self, node: ast.KVPair) -> None:
        """Sub objects.

        key: ExprType,
        value: ExprType,
        """
        self.emit(node, f"{node.key.meta['py_code']}: {node.value.meta['py_code']}")

    def exit_atom_trailer(self, node: ast.AtomTrailer) -> None:
        """Sub objects.

        target: AtomType,
        right: IndexSlice | ArchRefType | Token,
        null_ok: bool,
        """
        if type(node.right) == ast.IndexSlice:
            self.emit(
                node,
                f"{node.target.meta['py_code']}{node.right.meta['py_code']}",
            )
        elif type(node.right) == ast.Token:
            self.emit(
                node,
                f"{node.target.meta['py_code']}.{node.right.value}",
            )
        else:
            self.emit(
                node,
                f"{node.target.meta['py_code']}.{node.right.meta['py_code']}",
            )

    # NOTE: Incomplete for Jac Purple and Red
    def exit_func_call(self, node: ast.FuncCall) -> None:
        """Sub objects.

        target: AtomType,
        params: Optional[ParamList],
        """
        if node.params:
            self.emit(
                node,
                f"{node.target.meta['py_code']}({node.params.meta['py_code']})",
            )
        else:
            self.emit(node, f"{node.target.meta['py_code']}()")

    def exit_param_list(self, node: ast.ParamList) -> None:
        """Sub objects.

        p_args: Optional[ExprList],
        p_kwargs: Optional[AssignmentList],
        """
        if node.p_args and node.p_kwargs:
            self.emit(
                node,
                f"{node.p_args.meta['py_code']}, {node.p_kwargs.meta['py_code']}",
            )
        elif node.p_args:
            self.emit(node, f"{node.p_args.meta['py_code']}")
        elif node.p_kwargs:
            self.emit(node, f"{node.p_kwargs.meta['py_code']}")

    def exit_assignment_list(self, node: ast.AssignmentList) -> None:
        """Sub objects.

        values: list[ExprType],
        """
        self.emit(
            node, f"{', '.join([value.meta['py_code'] for value in node.values])}"
        )

    def exit_index_slice(self, node: ast.IndexSlice) -> None:
        """Sub objects.

        start: ExprType,
        stop: Optional[ExprType],
        """
        if node.stop:
            self.emit(
                node,
                f"[{node.start.meta['py_code']}:{node.stop.meta['py_code']}]",
            )
        else:
            self.emit(node, f"[{node.start.meta['py_code']}:]")

    def exit_global_ref(self, node: ast.GlobalRef) -> None:
        """Sub objects.

        name: Token,
        """
        self.emit(node, f"{node.name.value}")

    def exit_here_ref(self, node: ast.HereRef) -> None:
        """Sub objects.

        name: Optional[Token],
        """
        if node.name:
            self.emit(node, f"self.{node.name.value}")
        else:
            self.emit(node, "self")

    # NOTE: Incomplete for Jac Purple and Red
    def exit_visitor_ref(self, node: ast.VisitorRef) -> None:
        """Sub objects.

        name: Optional[Token],
        """
        self.ds_feature_warn()

    # NOTE: Incomplete for Jac Purple and Red
    def exit_node_ref(self, node: ast.NodeRef) -> None:
        """Sub objects.

        name: Token,
        """
        self.ds_feature_warn()

    # NOTE: Incomplete for Jac Purple and Red
    def exit_edge_ref(self, node: ast.EdgeRef) -> None:
        """Sub objects.

        name: Token,
        """
        self.ds_feature_warn()

    # NOTE: Incomplete for Jac Purple and Red
    def exit_walker_ref(self, node: ast.WalkerRef) -> None:
        """Sub objects.

        name: Token,
        """
        self.ds_feature_warn()

    def exit_object_ref(self, node: ast.ObjectRef) -> None:
        """Sub objects.

        name: Token,
        """
        self.emit(node, f"{node.name.value}")

    def exit_ability_ref(self, node: ast.AbilityRef) -> None:
        """Sub objects.

        name: Token,
        """
        self.emit(node, f"{node.name.value}")

    # NOTE: Incomplete for Jac Purple and Red
    def exit_edge_op_ref(self, node: ast.EdgeOpRef) -> None:
        """Sub objects.

        filter_cond: Optional[ExprType],
        edge_dir: EdgeDir,
        """
        self.ds_feature_warn()

    # NOTE: Incomplete for Jac Purple and Red
    def exit_disconnect_op(self, node: ast.DisconnectOp) -> None:
        """Sub objects.

        filter_cond: Optional[ExprType],
        edge_dir: EdgeDir,
        """
        self.ds_feature_warn()

    # NOTE: Incomplete for Jac Purple and Red
    def exit_connect_op(self, node: ast.ConnectOp) -> None:
        """Sub objects.

        spawn: Optional[ExprType],
        edge_dir: EdgeDir,
        """
        self.ds_feature_warn()

    # NOTE: Incomplete for Jac Purple and Red
    def exit_spawn_ctx(self, node: ast.SpawnCtx) -> None:
        """Sub objects.

        spawns: list[Assignment],
        """
        self.ds_feature_warn()

    # NOTE: Incomplete for Jac Purple and Red
    def exit_filter_ctx(self, node: ast.FilterCtx) -> None:
        """Sub objects.

        compares: list[BinaryExpr],
        """
        self.ds_feature_warn()

    def exit_f_string(self, node: ast.FString) -> None:
        """Sub objects.

        parts: list["Token | ExprType"],
        """
        for part in node.parts:
            if type(part) == ast.Token:
                self.emit(node, f"{part.value}")
            else:
                self.emit(node, f"{part.meta['py_code']}")
