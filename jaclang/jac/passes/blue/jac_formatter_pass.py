"""JacFormatPass for Jaseci Ast."""

import jaclang.jac.absyntree as ast
from jaclang.jac import constant
from jaclang.jac.constant import Constants as Con
from jaclang.jac.constant import Tokens as Tok
from jaclang.jac.passes import Pass


class JacFormatPass(Pass):
    """JacFormat Pass format Jac code."""

    def before_pass(self) -> None:
        """Initialize pass."""
        self.indent_size = 4
        self.indent_level = 0
        self.debuginfo = {"jac_mods": []}
        self.preamble = ast.AstNode(parent=None, mod_link=None, kid=[], line=0)
        self.preamble.meta["jac_code"] = ""

    def enter_node(self, node: ast.AstNode) -> None:
        """Enter node."""
        if node:
            node.meta["jac_code"] = ""

    def indent_str(self) -> str:
        """Return string for indent."""
        return " " * self.indent_size * self.indent_level

    def emit(self, node: ast.AstNode, s: str) -> None:
        """Emit code to node."""
        node.meta["jac_code"] += self.indent_str() + s.replace(
            "\n", "\n" + self.indent_str()
        )
        if "\n" in node.meta["jac_code"]:
            node.meta["jac_code"] = node.meta["jac_code"].rstrip(" ")

    def emit_ln(self, node: ast.AstNode, s: str) -> None:
        """Emit code to node."""
        self.emit(node, s.strip().strip("\n"))
        self.emit(node, "\n")

    def emit_ln_unique(self, node: ast.AstNode, s: str) -> None:
        """Emit code to node."""
        if s not in node.meta["jac_code"]:
            ilev = self.indent_level
            self.indent_level = 0
            self.emit_ln(node, s)
            self.indent_level = ilev

    def exit_token(self, node: ast.Token) -> None:
        """Sub objects.

        name: str,
        value: str,
        col_start: int,
        col_end: int,
        """
        self.emit(node, node.value)

    def exit_name(self, node: ast.Name) -> None:
        """Sub objects.

        name: str,
        value: str,
        col_start: int,
        col_end: int,
        already_declared: bool,
        """
        self.emit(node, node.value)

    def exit_constant(self, node: ast.Constant) -> None:
        """Sub objects.

        name: str,
        value: str,
        col_start: int,
        col_end: int,
        typ: type,
        """
        self.emit(node, node.value)

    def exit_elements(self, node: ast.Elements) -> None:
        """Sub objects.

        elements: list[GlobalVars | Test | ModuleCode | Import | Architype | Ability | AbilitySpec], # noqa E501
        """
        for element in node.elements:
            self.emit(node, element.meta["jac_code"])
        self.emit_ln(node, "")

    def exit_module_code(self, node: ast.ModuleCode) -> None:
        """Sub objects.

        doc: Optional[Token],
        name: Optional[Name],
        body: CodeBlock,

        """
        if node.doc:
            self.emit_ln(node, node.doc.value)
        if isinstance(node.parent, ast.Elements):
            self.emit_ln(node, "with entry {")
        if node.body:
            self.indent_level += 1
            self.emit_ln(node, node.body.meta["jac_code"])
            self.indent_level -= 1
        self.emit_ln(node, "}")

    def exit_module(self, node: ast.Module) -> None:
        """Sub objects.

        name: str,
        doc: Token,
        body: "Elements",
        """
        if node.doc:
            self.emit_ln(node, node.doc.value)
            self.emit_ln(node, "")
        if self.preamble:
            self.emit(node, self.preamble.meta["jac_code"])
        if node.body:
            self.emit(node, node.body.meta["jac_code"])
        self.ir = node
        self.ir.meta["jac_code"] = self.ir.meta["jac_code"].rstrip()

    def exit_code_block(self, node: ast.CodeBlock) -> None:
        """Sub objects.

        stmts: list["StmtType"],
        """
        for stmt in node.stmts:
            unary_expr_found = any(isinstance(kid, ast.UnaryExpr) for kid in stmt.kid)
            if isinstance(
                stmt,
                (
                    ast.IfStmt,
                    ast.WhileStmt,
                    ast.TryStmt,
                    ast.IterForStmt,
                    ast.InForStmt,
                ),
            ):
                self.emit(node, f"{stmt.meta['jac_code']}")
            elif unary_expr_found:
                self.emit(node, f"{stmt.meta['jac_code']};")
            else:
                self.emit_ln(node, f"{stmt.meta['jac_code']};")

    def exit_func_call(self, node: ast.FuncCall) -> None:
        """Sub objects.

        target: AtomType,
        params: Optional[ParamList],
        """
        if node.params:
            self.emit(
                node,
                f"{node.target.meta['jac_code']}({node.params.meta['jac_code']})",
            )
        else:
            self.emit(node, f"{node.target.meta['jac_code']}()")

    def exit_param_list(self, node: ast.ParamList) -> None:
        """Sub objects.

        p_args: Optional[ExprList],
        p_kwargs: Optional[AssignmentList],
        """
        if node.p_args and node.p_kwargs:
            self.emit(
                node,
                f"{node.p_args.meta['jac_code']}, {node.p_kwargs.meta['jac_code']}",
            )
        elif node.p_args:
            self.emit(node, f"{node.p_args.meta['jac_code']}")
        elif node.p_kwargs:
            self.emit(node, f"{node.p_kwargs.meta['jac_code']}")

    def exit_expr_list(self, node: ast.ExprList) -> None:
        """Sub objects.

        values: list[ExprType],
        """
        self.emit(
            node, f"{', '.join([value.meta['jac_code'] for value in node.values])}"
        )

    def exit_multi_string(self, node: ast.MultiString) -> None:
        """Sub objects.

        strings: list[Token],
        """
        for string in node.strings:
            self.emit(node, string.meta["jac_code"])

    def exit_module_path(self, node: ast.ModulePath) -> None:
        """Sub objects.

        path: list[Token],
        """
        self.emit(node, "".join([i.value for i in node.path]))

    def exit_tuple_val(self, node: ast.TupleVal) -> None:
        """Sub objects.

        first_expr: Optional["ExprType"],
        exprs: Optional[ExprList],
        assigns: Optional[AssignmentList],
        """
        self.emit(node, "(")
        if node.first_expr:
            self.emit(node, f"{node.first_expr.meta['jac_code']}")
        if not node.exprs and not node.assigns:
            self.emit(node, ",)")
        if node.exprs:
            self.emit(node, f", {node.exprs.meta['jac_code']}")

        if node.assigns:
            if node.first_expr:
                self.emit(node, f", {node.assigns.meta['jac_code']}")
            else:
                self.emit(node, f"{node.assigns.meta['jac_code']}")
        self.emit(node, ")")

    def exit_special_var_ref(self, node: ast.SpecialVarRef) -> None:
        """Sub objects.

        var: Token,
        """
        self.emit(node, node.var.value)

    def exit_ability_def(self, node: ast.AbilityDef) -> None:
        """Sub objects.

        doc: Optional[Token],
        mod: Optional["DottedNameList"],
        ability: AbilityRef,
        body: CodeBlock,
        """
        self.emit_ln(node, "")
        if node.doc:
            self.emit_ln(node, node.doc.meta["jac_code"])
        if isinstance(node.signature, ast.EventSignature):
            # need to find a example and implement
            self.warning("This Event Defination is not available currently")
            return
        else:
            fun_def = ""
            for arch in node.target.archs:
                fun_def += arch.meta["jac_code"]
            if node.signature.meta:
                self.emit_ln(node, f"{fun_def} {node.signature.meta['jac_code']}{{")
            else:
                self.emit_ln(node, f"{fun_def} {{")
        self.indent_level += 1
        if node.body:
            self.emit_ln(node, node.body.meta["jac_code"])
        self.indent_level -= 1
        self.emit_ln(node, "}")
        self.emit_ln(node, "")

    def exit_event_signature(self, node: ast.EventSignature) -> None:
        """Sub objects.

        event: Token,
        arch_tag_info: Optional["TypeList | TypeSpec"],
        return_type: Optional["TypeSpec"],
        """
        event_value = node.event.value if node.event else None
        if node.arch_tag_info:
            self.emit(node, f"{node.arch_tag_info.meta['jac_code']} {event_value}")
        else:
            self.emit(node, f"{event_value}")

    def exit_import(self, node: ast.Import) -> None:
        """Sub objects.

        lang: Token,
        path: "ModulePath",
        alias: Optional[Token],
        items: Optional["ModuleItems"],
        is_absorb: bool,  # For includes
        self.sub_module = None
        """
        if node.items:
            self.emit_ln(
                node,
                f"import:{node.lang.value} from {node.path.meta['jac_code']}, {node.items.meta['jac_code']};",  # noqa
            )
        else:
            if node.is_absorb:
                self.emit_ln(
                    node, f"include:{node.lang.value} {node.path.meta['jac_code']};"
                )
            else:
                self.emit_ln(
                    node, f"import:{node.lang.value} {node.path.meta['jac_code']};"
                )
        self.emit_ln(node, "")

    def exit_arch_def(self, node: ast.ArchDef) -> None:
        """Sub objects.

        doc: Optional[Token],
        target: ArchRefChain,
        body: ArchBlock,
        """
        doc = node.doc.value if node.doc else ""
        target = f"{node.target.meta['jac_code']} "
        self.emit_ln(node, f"{doc}\n{target} {{")
        self.indent_level += 1
        self.emit(node, node.body.meta["jac_code"])
        self.indent_level -= 1
        self.emit(node, "}")
        self.emit_ln(node, "")

    def exit_arch_block(self, node: ast.ArchBlock) -> None:
        """Sub objects.

        members: list["ArchHas | Ability"],
        """
        for member in node.members:
            self.emit(node, member.meta["jac_code"])

    def exit_ability(self, node: ast.Ability) -> None:
        """Sub objects.

        name_ref: Name | SpecialVarRef,
        is_func: bool,
        is_async: bool,
        is_static: bool,
        is_abstract: bool,
        doc: Optional[Token],
        decorators: Optional[Decorators],
        access: Optional[Token],
        signature: Optional[FuncSignature | TypeSpec | EventSignature],
        body: Optional[CodeBlock],
        arch_attached: Optional["ArchBlock"] = None,
        """
        access_modifier = None
        if node.doc:
            self.emit_ln(node, node.doc.meta["jac_code"])
        if node.access:
            access_modifier = node.access.meta["jac_code"]
        if node.decorators:
            self.emit_ln(node, node.decorators.meta["jac_code"])
        if isinstance(node.signature, (ast.FuncSignature, ast.EventSignature)):
            if isinstance(node.signature, ast.EventSignature):
                can_name = (
                    node.name_ref.value
                    if isinstance(node.name_ref, ast.Name)
                    else node.name_ref.var.value
                )
                if node.body:
                    self.emit_ln(
                        node,
                        f"can {can_name} with {node.signature.meta['jac_code']} {{",
                    )
                    self.indent_level += 1
                    self.emit(node, node.body.meta["jac_code"])
                    self.indent_level -= 1
                    self.emit_ln(node, "}")
                else:
                    self.emit_ln(
                        node,
                        f"can {can_name} with {node.signature.meta['jac_code']};",
                    )
            elif isinstance(node.signature, ast.FuncSignature):
                if isinstance(node.name_ref, ast.SpecialVarRef):
                    if access_modifier:
                        fun_signature = f"can:{access_modifier} {node.name_ref.var.value}{node.signature.meta['jac_code']}"  # noqa
                    else:
                        fun_signature = f"can {node.name_ref.var.value}{node.signature.meta['jac_code']}"  # noqa
                else:
                    if access_modifier:
                        fun_signature = f"can:{access_modifier} {node.name_ref.value}{node.signature.meta['jac_code']}"  # noqa
                    else:
                        fun_signature = f"can {node.name_ref.value}{node.signature.meta['jac_code']}"  # noqa
                if node.body:
                    self.emit_ln(node, f"{fun_signature} {{")
                    self.indent_level += 1
                    self.emit_ln(node, node.body.meta["jac_code"])
                    self.indent_level -= 1
                    self.emit_ln(node, "}")
                else:
                    if node.is_abstract:
                        self.emit_ln(node, f"{fun_signature} abstract;")
                    else:
                        self.emit_ln(node, f"{fun_signature};")

    def exit_func_signature(self, node: ast.FuncSignature) -> None:
        """Sub objects.

        params: Optional[FuncParams],
        return_type: Optional[TypeSpec],
        self.is_arch_attached = False
        """
        params = node.params.meta["jac_code"] if node.params else ""
        return_type_jac_code = ""
        if node.return_type:
            return_type_jac_code = node.return_type.meta["jac_code"]
        if return_type_jac_code and params:
            self.emit(node, f"({params}) -> {return_type_jac_code}")
        elif params:
            self.emit(node, f"({params})")
        elif return_type_jac_code:
            self.emit(node, f"-> {return_type_jac_code}")

    def exit_arch_has(self, node: ast.ArchHas) -> None:
        """Sub objects.

        doc: Optional[Token],
        is_static: bool,
        access: Optional[Token],
        vars: "HasVarList",
        is_frozen: bool,
        """
        if node.access:
            self.emit_ln(
                node,
                f"has:{node.access.meta['jac_code']} {node.vars.meta['jac_code']};",
            )
        else:
            self.emit_ln(
                node,
                f"has {node.vars.meta['jac_code']};",
            )
        self.emit_ln(node, "")

    def exit_arch_ref(self, node: ast.ArchRef) -> None:
        """Sub objects.

        archs: list[ArchRef],
        """
        if isinstance(node.name_ref, ast.SpecialVarRef):
            self.emit(node, f"{node.arch.value}{node.name_ref.var.meta['jac_code']}")
        else:
            self.emit(node, f"{node.arch.value}{node.name_ref.value}")

    def exit_func_params(self, node: ast.FuncParams) -> None:
        """Sub objects.

        params: list["ParamVar"],
        """
        first_out = False
        for i in node.params:
            self.emit(node, ", ") if first_out else None
            self.emit(node, i.meta["jac_code"])
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
                f"{node.name.value}: {node.type_tag.meta['jac_code']} = {node.value.meta['jac_code']}",  # noqa
            )
        else:
            self.emit(node, f"{node.name.value}: {node.type_tag.meta['jac_code']}")

    def exit_enum(self, node: ast.Enum) -> None:
        """Sub objects.

        name: Name,
        doc: Optional[Token],
        decorators: Optional[Decorators],
        access: Optional[Token],
        base_classes: BaseClasses,
        body: Optional[EnumBlock],
        """
        if node.decorators:
            self.emit_ln(node, node.decorators.meta["jac_code"])

        if len(node.base_classes.base_classes):
            self.emit_ln(
                node,
                f"class {node.name.meta['jac_code']}({node.base_classes.meta['jac_code']}):",  # noqa
            )
        else:
            if node.body:
                self.emit_ln(node, f"enum {node.name.value} {{")
                self.indent_level += 1
                if node.doc:
                    self.emit_ln(node, node.doc.value)
                if node.body:
                    self.emit(node, node.body.meta["jac_code"])
                else:
                    self.decl_def_missing(node.name.meta["jac_code"])
                self.indent_level -= 1
                self.emit_ln(node, "}")
            else:
                self.emit_ln(node, f"enum {node.name.value};")

    def exit_enum_def(self, node: ast.EnumDef) -> None:
        """Sub objects.

        doc: Optional[Token],
        mod: Optional[DottedNameList],
        body: EnumBlock,
        """
        if node.doc:
            self.emit_ln(node, node.doc.value)
        self.emit_ln(node, node.target.meta["jac_code"] + "{")
        if node.body:
            self.indent_level += 1
            self.emit(node, node.body.meta["jac_code"])
            self.indent_level -= 1
        self.emit_ln(node, "}")

    def exit_enum_block(self, node: ast.EnumBlock) -> None:
        """Sub objects.

        stmts: list['Name|Assignment'],
        """
        for idx, i in enumerate(node.stmts):
            if idx < len(node.stmts) - 1:
                self.emit_ln(node, i.meta["jac_code"] + ",")
            else:
                self.emit_ln(node, i.meta["jac_code"])

    def exit_type_spec_list(self, node: ast.TypeSpecList) -> None:
        """Sub objects.

        types: list[TypeSpec],

        """
        self.emit(node, "|".join([i.meta["jac_code"] for i in node.types]))

    def exit_dotted_name_list(self, node: ast.DottedNameList) -> None:
        """Sub objects.

        names: list[all_refs],
        """
        self.emit(node, ".".join([i.meta["jac_code"] for i in node.names]))

    def exit_type_spec(self, node: ast.TypeSpec) -> None:
        """Sub objects.

        typ: "Token | DottedNameList",
        list_nest: TypeSpec,
        dict_nest: TypeSpec,
        """
        if node.dict_nest:
            self.emit(
                node,
                f"dict[{node.list_nest.meta['jac_code']}, {node.dict_nest.meta['jac_code']}]",  # noqa
            )
        elif node.list_nest:
            self.emit(node, f"list[{node.list_nest.meta['jac_code']}]")
        else:
            self.emit(node, node.spec_type.meta["jac_code"])

    def exit_atom_trailer(self, node: ast.AtomTrailer) -> None:
        """Sub objects.

        target: AtomType,
        right: IndexSlice | ArchRefType | Token,
        null_ok: bool,
        """
        if node.null_ok:
            if isinstance(node.right, ast.IndexSlice):
                self.emit(
                    node,
                    f"({node.target.meta['jac_code']}{node.right.meta['jac_code']} "
                    f"if {node.target.meta['jac_code']} is not None else None)",
                )
            else:
                self.emit(
                    node,
                    f"({node.target.meta['jac_code']}.{node.right.meta['jac_code']} "
                    f"if {node.target.meta['jac_code']} is not None else None)",
                )
        else:
            if isinstance(node.right, ast.IndexSlice):
                self.emit(
                    node,
                    f"{node.target.meta['jac_code']}{node.right.meta['jac_code']}",
                )
            else:
                self.emit(
                    node,
                    f"{node.target.meta['jac_code']}.{node.right.meta['jac_code']}",
                )

    def exit_binary_expr(self, node: ast.BinaryExpr) -> None:
        """Sub objects.

        left: ExprType,
        right: ExprType,
        op: Token | DisconnectOp | ConnectOp,
        """
        if isinstance(node.op, (ast.DisconnectOp, ast.ConnectOp)):
            self.emit(
                node,
                f"{node.left.meta['jac_code']} {node.op.meta['jac_code']} {node.right.meta['jac_code']}",  # noqa
            )
        if isinstance(node.op, ast.Token):
            if node.op.value in [
                *["+", "-", "*", "/", "%", "**"],
                *["+=", "-=", "*=", "/=", "%=", "**="],
                *[">>", "<<", ">>=", "<<="],
                *["//=", "&=", "|=", "^=", "~="],
                *["//", "&", "|", "^"],
                *[">", "<", ">=", "<=", "==", "!=", ":="],
                *["and", "or", "in", "not in", "is", "is not"],
            ]:
                self.emit(
                    node,
                    f"{node.left.meta['jac_code']} {node.op.value} {node.right.meta['jac_code']}",  # noqa
                )
            elif node.op.name in [
                Tok.PIPE_FWD,
                Tok.KW_SPAWN,
                Tok.A_PIPE_FWD,
            ] and isinstance(node.left, ast.TupleVal):
                self.emit(
                    node,
                    f"{node.left.meta['jac_code']} {node.op.meta['jac_code']} {node.right.meta['jac_code']}",  # noqa
                )
            elif node.op.name in [Tok.PIPE_BKWD, Tok.A_PIPE_BKWD] and isinstance(
                node.right, ast.TupleVal
            ):
                params = node.right.meta["jac_code"]
                params = params.replace(",)", ")") if params[-2:] == ",)" else params
                self.emit(node, f"{node.left.meta['jac_code']}{params}")
            elif (
                node.op.name == Tok.PIPE_FWD and isinstance(node.right, ast.TupleVal)
            ) or node.op.name == Tok.PIPE_FWD:
                self.emit(
                    node,
                    f"{node.left.meta['jac_code']} |> {node.right.meta['jac_code']}",
                )
            elif node.op.name in [Tok.KW_SPAWN, Tok.A_PIPE_FWD]:
                self.emit(
                    node,
                    f"{node.left.meta['jac_code']} :> {node.right.meta['jac_code']}",
                )
            elif node.op.name in [Tok.PIPE_BKWD, Tok.A_PIPE_BKWD]:
                self.emit(
                    node,
                    f"{node.left.meta['jac_code']} <: {node.right.meta['jac_code']}",
                )
            elif node.op.name == Tok.ELVIS_OP:
                self.emit(
                    node,
                    f"{Con.JAC_TMP} "
                    f"if ({Con.JAC_TMP} := ({node.left.meta['jac_code']})) is not None "
                    f"else {node.right.meta['jac_code']}",
                )
            else:
                self.error(
                    f"Binary operator {node.op.value} not supported in bootstrap Jac"
                )

    def exit_has_var_list(self, node: ast.HasVarList) -> None:
        """Sub objects.

        vars: list[HasVar],
        """
        first_out = False
        for i in node.vars:
            if first_out:
                self.emit_ln(node, ",")
                self.indent_level += 1
            self.emit(node, i.meta["jac_code"])
            first_out = True
        if self.indent_level > 0:
            self.indent_level -= 1

    def exit_has_var(self, node: ast.HasVar) -> None:
        """Sub objects.

        name: Token,
        type_tag: TypeSpec,
        value: Optional["ExprType"],
        """
        if node.value:
            self.emit(
                node,
                f"{node.name.meta['jac_code']}: {node.type_tag.meta['jac_code']} = {node.value.meta['jac_code']}",  # noqa
            )
        else:
            self.emit(node, f"{node.name.value}: {node.type_tag.meta['jac_code']}")

    def get_mod_index(self, node: ast.AstNode) -> int:
        """Get module index."""
        path = node.mod_link.mod_path if node.mod_link else None
        if not path:
            return -1
        if path not in self.debuginfo["jac_mods"]:
            self.debuginfo["jac_mods"].append(path)
        return self.debuginfo["jac_mods"].index(path)

    def ds_feature_warn(self) -> None:
        """Warn about feature."""
        self.warning("Data spatial features not supported in bootstrap Jac.")

    def exit_if_stmt(self, node: ast.IfStmt) -> None:
        """Sub objects.

        condition: ExprType,
        body: CodeBlock,
        elseifs: Optional[ElseIfs],
        else_body: Optional[ElseStmt],
        """
        self.emit_ln(node, f"if {node.condition.meta['jac_code']} {{")
        self.indent_level += 1
        self.emit(node, node.body.meta["jac_code"])
        self.indent_level -= 1
        self.emit(node, "} ")
        if node.elseifs:
            self.emit(node, node.elseifs.meta["jac_code"])
        if node.else_body:
            self.emit(node, node.else_body.meta["jac_code"])
        self.emit_ln(node, "")

    def exit_else_ifs(self, node: ast.ElseIfs) -> None:
        """Sub objects.

        elseifs: list[IfStmt],
        """
        for i in node.elseifs:
            self.emit(node, f" elif {i.condition.meta['jac_code']} {{\n")
            self.indent_level += 1
            self.emit(node, i.body.meta["jac_code"])
            self.indent_level -= 1
            self.emit(node, "} ")

    def exit_disengage_stmt(self, node: ast.DisengageStmt) -> None:
        """Sub objects."""
        self.emit(node, "disengage")

    def exit_else_stmt(self, node: ast.ElseStmt) -> None:
        """Sub objects.

        body: CodeBlock,
        """
        self.emit(node, " else {\n")
        self.indent_level += 1
        self.emit(node, node.body.meta["jac_code"])
        self.indent_level -= 1
        self.emit_ln(node, "}")

    def exit_iter_for_stmt(self, node: ast.IterForStmt) -> None:
        """Sub objects.

        iter: Assignment,
        condition: ExprType,
        count_by: ExprType,
        body: CodeBlock,
        """
        self.emit_ln(node, "")
        self.emit_ln(
            node,
            f"for {node.iter.meta['jac_code']} to {node.condition.meta['jac_code']} by {node.count_by.meta['jac_code']} {{",  # noqa
        )
        self.indent_level += 1
        self.emit(node, node.body.meta["jac_code"])
        self.indent_level -= 1
        self.emit_ln(node, "}")

    def exit_try_stmt(self, node: ast.TryStmt) -> None:
        """Sub objects.

        body: CodeBlock,
        excepts: Optional[ExceptList],
        finally_body: Optional[FinallyStmt],
        """
        self.emit_ln(node, "try {")
        self.indent_level += 1
        self.emit_ln(node, node.body.meta["jac_code"])
        self.indent_level -= 1
        self.emit_ln(node, "}")
        if node.excepts:
            self.emit_ln(node, node.excepts.meta["jac_code"])
        if node.finally_body:
            self.emit_ln(node, node.finally_body.meta["jac_code"] + "}")

    def exit_except(self, node: ast.Except) -> None:
        """Sub objects.

        typ: ExprType,
        name: Optional[Token],
        body: CodeBlock,
        """
        if node.name:
            self.emit_ln(
                node, f"except {node.ex_type.meta['jac_code']} as {node.name.value}:"
            )
        else:
            self.emit_ln(node, f"except {node.ex_type.meta['jac_code']} {{")
        self.indent_level += 1
        self.emit_ln(node, node.body.meta["jac_code"])
        self.indent_level -= 1
        self.emit_ln(node, "}")

    def exit_except_list(self, node: ast.ExceptList) -> None:
        """Sub objects.

        excepts: list[Except],
        """
        for i in node.excepts:
            self.emit_ln(node, i.meta["jac_code"])

    def exit_finally_stmt(self, node: ast.FinallyStmt) -> None:
        """Sub objects.

        body: CodeBlock,
        """
        self.emit_ln(node, "finally {")
        self.indent_level += 1
        self.emit_ln(node, node.body.meta["jac_code"])
        self.indent_level -= 1

    def exit_while_stmt(self, node: ast.WhileStmt) -> None:
        """Sub objects.

        condition: ExprType,
        body: CodeBlock,
        """
        self.emit_ln(node, f"while {node.condition.meta['jac_code']} {{")
        self.indent_level += 1
        self.emit_ln(node, node.body.meta["jac_code"])
        self.indent_level -= 1
        self.emit(node, "}")
        self.emit_ln(node, "")

    def exit_with_stmt(self, node: ast.WithStmt) -> None:
        """Sub objects.

        exprs: "ExprAsItemList",
        body: "CodeBlock",
        """
        self.emit(node, f"with {node.exprs.meta['jac_code']}{{")
        if node.body.meta["jac_code"]:
            self.emit_ln(node, "")
            self.indent_level += 1
            self.emit_ln(node, node.body.meta["jac_code"])
            self.indent_level -= 1
        self.emit(node, "}")

    def exit_decorators(self, node: ast.Decorators) -> None:
        """Sub objects.

        calls: list["ExprType"],
        """
        for i in node.calls:
            self.emit_ln(node, "@" + i.meta["jac_code"])

    def exit_module_items(self, node: ast.ModuleItems) -> None:
        """Sub objects.

        items: list["ModuleItem"],
        """
        self.emit(node, ", ".join([i.meta["jac_code"] for i in node.items]))

    def exit_global_vars(self, node: ast.GlobalVars) -> None:
        """Sub objects.

        doc: Optional["Token"],
        access: Optional[Token],
        assignments: "AssignmentList",
        is_frozen: bool,
        """
        if node.doc:
            self.emit_ln(node, node.doc.value)
        self.emit_ln(node, f"global {node.assignments.meta['jac_code']};")
        self.emit_ln(node, "")

    def exit_module_item(self, node: ast.ModuleItem) -> None:
        """Sub objects.

        name: Token,
        alias: Optional[Token],
        """
        if node.alias:
            self.emit(node, node.name.value + " as " + node.alias.value)
        else:
            self.emit(node, node.name.value)

    def exit_base_classes(self, node: ast.BaseClasses) -> None:
        """Sub objects.

        base_classes: list[DottedNameList],
        """
        self.emit(node, ":".join([i.meta["jac_code"] for i in node.base_classes]))

    def exit_assignment(self, node: ast.Assignment) -> None:
        """Sub objects.

        is_static: bool,
        target: AtomType,
        value: ExprType,
        """
        if node.is_static:
            self.emit(node, "has ")
        self.emit(
            node, f"{node.target.meta['jac_code']} = {node.value.meta['jac_code']}"
        )

    def exit_architype(self, node: ast.Architype) -> None:
        """Sub objects.

        name: Name,
        arch_type: Token,
        doc: Optional[Token],
        decorators: Optional["Decorators"],
        access: Optional[Token],
        base_classes: "BaseClasses",
        body: Optional["ArchBlock"],
        """
        self.emit_ln(node, "")
        if node.doc:
            self.emit_ln(node, node.doc.value)
        if node.decorators:
            self.emit_ln(node, node.decorators.meta["jac_code"])
        if not len(node.base_classes.base_classes):
            self.emit_ln(
                node, f"{node.arch_type.value} {node.name.meta['jac_code']} {{"
            )
        else:
            self.emit_ln(
                node,
                f"{node.arch_type.value} {node.name.meta['jac_code']}:{node.base_classes.meta['jac_code']} {{",  # noqa
            )
        if node.body:
            self.indent_level += 1
            self.emit(node, node.body.meta["jac_code"])
            self.indent_level -= 1
        else:
            self.decl_def_missing(node.name.meta["jac_code"])
        self.emit_ln(node, "}")
        self.emit_ln(node, "")

    def exit_f_string(self, node: ast.FString) -> None:
        """Sub objects.

        parts: list["Token | ExprType"],
        """
        self.emit(node, 'f"')
        for part in node.parts:
            if isinstance(part, ast.Token) and part.name == "PIECE":
                self.emit(node, f"{part.meta['jac_code']}")
            else:
                self.emit(node, "{" + part.meta["jac_code"] + "}")
        self.emit(node, '"')

    def exit_if_else_expr(self, node: ast.IfElseExpr) -> None:
        """Sub objects.

        condition: BinaryExpr | IfElseExpr,
        value: ExprType,
        else_value: ExprType,
        """
        self.emit(
            node,
            f"{node.value.meta['jac_code']} if {node.condition.meta['jac_code']} "
            f"else {node.else_value.meta['jac_code']}",
        )

    def decl_def_missing(self, decl: str = "this") -> None:
        """Warn about declaration."""
        self.error(
            f"Unable to find definition for {decl} declaration. Perhaps there's an `include` missing?"  # noqa
        )

    def exit_name_list(self, node: ast.NameList) -> None:
        """Sub objects.

        names: list[Name],
        """
        self.emit(node, ",".join([i.meta["jac_code"] for i in node.names]))

    def exit_unary_expr(self, node: ast.UnaryExpr) -> None:
        """Sub objects.

        operand: ExprType,
        op: Token,
        """
        if node.op.value in ["-", "~", "+"]:
            self.emit(node, f"{node.op.value}{node.operand.meta['jac_code']}")
        elif node.op.value == "(":
            self.emit(node, f"({node.operand.meta['jac_code']})")
        elif node.op.value == "not":
            self.emit(node, f"not {node.operand.meta['jac_code']}")
        elif node.op.name in [Tok.PIPE_FWD, Tok.KW_SPAWN, Tok.A_PIPE_FWD]:
            self.emit(node, f"{node.op.value} {node.operand.meta['jac_code']}")
        else:
            self.error(f"Unary operator {node.op.value} not supported in bootstrap Jac")

    def exit_raise_stmt(self, node: ast.RaiseStmt) -> None:
        """Sub objects.

        cause: Optional[ExprType],
        """
        if node.cause:
            node.meta["jac_code"] = f"raise {node.cause.meta['jac_code']}"
        else:
            node.meta["jac_code"] = "raise"

    def exit_edge_op_ref(self, node: ast.EdgeOpRef) -> None:
        """Sub objects.

        filter_cond: Optional[ExprType],
        edge_dir: EdgeDir,
        """
        edge_dir_map = {
            constant.EdgeDir.IN: "<--",
            constant.EdgeDir.OUT: "-->",
            constant.EdgeDir.ANY: "<-->",
        }

        edge_op_string = edge_dir_map.get(node.edge_dir)

        if edge_op_string:
            self.emit(node, edge_op_string)
        else:
            print(f"Unknown edge direction: {node.edge_dir}")

    def exit_index_slice(self, node: ast.IndexSlice) -> None:
        """Sub objects.

        start: ExprType,
        stop: Optional[ExprType],
        """
        if node.is_range:
            self.emit(
                node,
                f"[{node.start.meta['jac_code'] if node.start else ''}:"
                f"{node.stop.meta['jac_code'] if node.stop else ''}]",
            )
        elif node.start:
            self.emit(node, f"[{node.start.meta['jac_code']}]")
        else:
            self.ice("Something went horribly wrong.")

    def exit_list_val(self, node: ast.ListVal) -> None:
        """Sub objects.

        values: list[ExprType],
        """
        self.emit(
            node, f"[{', '.join([value.meta['jac_code'] for value in node.values])}]"
        )

    def exit_unpack_expr(self, node: ast.UnpackExpr) -> None:
        """Sub objects.

        target: ExprType,
        is_dict: bool,
        """
        if node.is_dict:
            self.emit(node, f"**{node.target.meta['jac_code']}")
        else:
            self.emit(node, f"*{node.target.meta['jac_code']}")

    def exit_set_val(self, node: ast.ListVal) -> None:
        """Sub objects.

        values: list[ExprType],
        """
        self.emit(
            node, f"{{{', '.join([value.meta['jac_code'] for value in node.values])}}}"
        )

    def exit_assignment_list(self, node: ast.AssignmentList) -> None:
        """Sub objects.

        values: list[Assignment],
        """
        self.emit(
            node, f"{', '.join([value.meta['jac_code'] for value in node.values])}"
        )

    def exit_dict_val(self, node: ast.DictVal) -> None:
        """Sub objects.

        kv_pairs: list["KVPair"],
        """
        self.emit(
            node,
            f"{{{', '.join([kv_pair.meta['jac_code'] for kv_pair in node.kv_pairs])}}}",
        )

    def exit_inner_compr(self, node: ast.InnerCompr) -> None:
        """Sub objects.

        out_expr: ExprType,
        name_list: NameList,
        collection: ExprType,
        conditional: Optional[ExprType],
        is_list: bool,
        is_gen: bool,
        is_set: bool,
        """
        names = node.name_list.meta["jac_code"]
        partial = (
            f"{node.out_expr.meta['jac_code']} for {names} "
            f"in {node.collection.meta['jac_code']}"
        )
        if node.conditional:
            partial += f" if {node.conditional.meta['jac_code']}"
        if node.is_list:
            self.emit(node, f"[{partial}]")
        elif node.is_set:
            self.emit(node, f"{{{partial}}}")
        elif node.is_gen:
            self.emit(node, f"({partial})")

    def exit_dict_compr(self, node: ast.DictCompr) -> None:
        """Sub objects.

        outk_expr: ExprType,
        outv_expr: ExprType,
        name_list: NameList,
        collection: ExprType,
        conditional: Optional[ExprType],
        """
        names = node.name_list.meta["jac_code"]
        partial = (
            f"{node.outk_expr.meta['jac_code']}: {node.outv_expr.meta['jac_code']} for "
            f"{names}"
        )
        partial += f" in {node.collection.meta['jac_code']}"
        if node.conditional:
            partial += f" if {node.conditional.meta['jac_code']}"
        self.emit(node, f"{{{partial}}}")

    def exit_k_v_pair(self, node: ast.KVPair) -> None:
        """Sub objects.

        key: ExprType,
        value: ExprType,
        """
        self.emit(node, f"{node.key.meta['jac_code']}: {node.value.meta['jac_code']}")

    def exit_disconnect_op(self, node: ast.DisconnectOp) -> None:
        """Sub objects.

        filter_cond: Optional[ExprType],
        edge_dir: EdgeDir,
        """
        for i in node.kid:
            self.emit(node, i.meta["jac_code"])

    def exit_connect_op(self, node: ast.ConnectOp) -> None:
        """Sub objects.

        spawn: Optional[ExprType],
        edge_dir: EdgeDir,
        """
        for i in node.kid:
            self.emit(node, i.meta["jac_code"])

    def exit_filter_compr(self, node: ast.FilterCompr) -> None:
        """Sub objects.

        compares: list[BinaryExpr],
        """
        self.ds_feature_warn()

    def exit_await_stmt(self, node: ast.AwaitStmt) -> None:
        """Sub objects.

        target: ExprType,
        """
        self.ds_feature_warn()

    def exit_revisit_stmt(self, node: ast.RevisitStmt) -> None:
        """Sub objects.

        hops: Optional[ExprType],
        else_body: Optional[ElseStmt],
        """
        self.ds_feature_warn()

    def exit_visit_stmt(self, node: ast.VisitStmt) -> None:
        """Sub objects.

        vis_type: Optional[Token],
        target: Optional["ExprType"],
        else_body: Optional["ElseStmt"],
        """
        self.emit(node, f"visit {node.target.meta['jac_code']}")

    def exit_ignore_stmt(self, node: ast.IgnoreStmt) -> None:
        """Sub objects.

        target: ExprType,
        """
        self.ds_feature_warn()

    def exit_yield_stmt(self, node: ast.YieldStmt) -> None:
        """Sub objects.

        expr: Optional[ExprType],
        """
        if node.expr:
            self.emit(node, f"yield {node.expr.meta['jac_code']}")
        else:
            self.emit(node, "yield")

    def exit_return_stmt(self, node: ast.ReturnStmt) -> None:
        """Sub objects.

        expr: Optional[ExprType],
        """
        if node.expr:
            self.emit(node, f"return {node.expr.meta['jac_code']}")
        else:
            self.emit(node, "return")

    def exit_assert_stmt(self, node: ast.AssertStmt) -> None:
        """Sub objects.

        condition: ExprType,
        error_msg: Optional[ExprType],
        """
        if node.error_msg:
            self.emit(
                node,
                f"assert {node.condition.meta['jac_code']}, {node.error_msg.meta['jac_code']}",  # noqa
            )
        else:
            self.emit_ln(node, f"assert {node.condition.meta['jac_code']}")

    def exit_ctrl_stmt(self, node: ast.CtrlStmt) -> None:
        """Sub objects.

        ctrl: Token,
        """
        if node.ctrl.name == Tok.KW_SKIP:
            self.ds_feature_warn()
        else:
            self.emit(node, node.ctrl.value)

    def exit_delete_stmt(self, node: ast.DeleteStmt) -> None:
        """Sub objects.

        target: ExprType,
        """
        self.emit(node, f"del {node.target.meta['jac_code']}")

    def exit_report_stmt(self, node: ast.ReportStmt) -> None:
        """Sub objects.

        expr: ExprType,
        """
        self.ds_feature_warn()

    def exit_expr_as_item_list(self, node: ast.ExprAsItemList) -> None:
        """Sub objects.

        items: list["ExprAsItem"],
        """
        self.emit(node, ", ".join([i.meta["jac_code"] for i in node.items]))

    def exit_expr_as_item(self, node: ast.ExprAsItem) -> None:
        """Sub objects.

        expr: "ExprType",
        alias: Optional[Token],
        """
        if node.alias:
            self.emit(node, node.expr.meta["jac_code"] + " as " + node.alias.value)
        else:
            self.emit(node, node.expr.meta["jac_code"])

    def exit_in_for_stmt(self, node: ast.InForStmt) -> None:
        """Sub objects.

        name_list: Token,
        collection: ExprType,
        body: CodeBlock,
        """
        names = node.name_list.meta["jac_code"]
        self.emit_ln(node, f"for {names} in {node.collection.meta['jac_code']} {{")
        if node.body:
            self.indent_level += 1
            self.emit(node, node.body.meta["jac_code"])
            self.indent_level -= 1
        self.emit_ln(node, "}")

    def exit_test(self, node: ast.Test) -> None:
        """Sub objects.

        name: Optional[Name],
        doc: Optional[Token],
        body: CodeBlock,
        """
        test_name = node.name.value
        if node.doc:
            self.emit_ln(node, node.doc.meta["jac_code"])
        if test_name:
            self.emit_ln(node, f"test {test_name} {{")
            self.indent_level += 1
        self.emit(node, f"{node.body.meta['jac_code']}")
        if self.indent_level > 0:
            self.indent_level -= 1
            self.emit_ln(node, "}")

    def exit_py_inline_code(self, node: ast.PyInlineCode) -> None:
        """Sub objects.

        code: Token,
        """
        self.emit_ln(node, node.code.value)

    def exit_arch_ref_chain(self, node: ast.ArchRefChain) -> None:
        """Sub objects.

        archs: list[ArchRef],
        """
        self.emit(node, ".".join([i.meta["jac_code"] for i in node.archs]))

    def exit_typed_ctx_block(self, node: ast.TypedCtxBlock) -> None:
        """Sub objects.

        type_ctx: TypeList,
        body: CodeBlock,
        """
        self.ds_feature_warn()

    def exit_parse(self, node: ast.Parse) -> None:
        """Sub objects.

        name: str,
        """
        self.error(f"Parse node should not be in this AST!! {node.name}")
