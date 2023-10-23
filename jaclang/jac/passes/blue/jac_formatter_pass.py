"""JacFormatPass for Jaseci Ast."""

from typing import Any, List, Optional, Tuple

import jaclang.jac.absyntree as ast
from jaclang.jac import constant
from jaclang.jac.constant import Constants as Con
from jaclang.jac.constant import Tokens as Tok
from jaclang.jac.passes import Pass


class JacFormatPass(Pass):
    """JacFormat Pass format Jac code."""

    def __init__(
        self, comments: Optional[list] = None, *args: Any, **kwargs: Any  # noqa
    ) -> None:  # noqa
        """Initialize Formatter."""
        self.comments = comments if comments else []

        super().__init__(*args, **kwargs)

    def before_pass(self) -> None:
        """Initialize pass."""
        self.indent_size = 4
        self.indent_level = 0
        self.debuginfo = {"jac_mods": []}
        self.preamble = ast.EmptyToken()
        self.preamble.meta["jac_code"] = ""

    def emit_comments_for_line(self, line: int) -> Tuple[List[str], List[str]]:
        """Stitch comments associated with the given line."""
        if not line:
            return [], []

        inline_comments = []
        standalone_comments = []

        for comment in self.comments:
            if comment.line == line:
                if comment.column < 10:
                    standalone_comments.append(comment.value)
                else:
                    inline_comments.append(comment.value)
            elif comment.line == line - 1 or comment.line == line + 1:
                standalone_comments.append(comment.value)

        return standalone_comments, inline_comments

    def enter_node(self, node: ast.AstNode) -> None:
        """Enter node."""
        if node:
            node.meta["jac_code"] = ""
        return Pass.enter_node(self, node)

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
        if node.name != "SEMI":
            self.emit(node, node.value)
        else:
            self.emit(node, "")

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

    def exit_module_code(self, node: ast.ModuleCode) -> None:
        """Sub objects.

        name: Optional[SubTag[Name]],
        body: SubNodeList[CodeBlockStmt],
        doc: Optional[Constant] = None,
        """
        if node.doc:
            self.emit_ln(node, node.doc.value)
        for i in node.kid:
            if isinstance(i, ast.Token):
                self.emit(node, i.value.strip("") + " ")
        if node.body:
            self.emit_ln(node, node.body.meta["jac_code"])
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
            for i in node.body:
                self.emit(node, i.meta["jac_code"])
        self.ir = node
        self.ir.meta["jac_code"] = self.ir.meta["jac_code"].rstrip()

    def exit_sub_node_list(self, node: ast.SubNodeList) -> None:
        """Sub objects.

        items: list[T],
        """
        comment_str = ""
        standalone_comments, inline_comments = self.emit_comments_for_line(
            node.loc.first_line
        )
        # for comment in standalone_comments:
        #     self.emit_ln(node, f"{comment}")
        if inline_comments:
            comment_str = " ; ".join(inline_comments)
        if isinstance(node.kid[0], ast.Token) and node.kid[0].name == "LBRACE":
            self.emit_ln(node, node.kid[0].value + " " + comment_str)
            self.indent_level += 1
        if node.items:
            for stmt in node.items:
                self.emit(node, f"{stmt.meta['jac_code']}")
        if isinstance(node.kid[-1], ast.Token) and node.kid[-1].name == "RBRACE":
            self.indent_level -= 1
            self.emit_ln(node, "")
            self.emit_ln(node, node.kid[-1].value)

    def exit_sub_tag(self, node: ast.SubTag) -> None:
        """Sub objects.

        tag: T,
        """
        self.emit(node, node.tag.meta["jac_code"])

    def exit_func_call(self, node: ast.FuncCall) -> None:
        """Sub objects.

        target: AtomType,
        params: Optional[ParamList],
        """
        comment_str = ""
        standalone_comments, inline_comments = self.emit_comments_for_line(
            node.loc.first_line
        )
        # for comment in standalone_comments:
        #     self.emit_ln(node, f"{comment}")
        if inline_comments:
            comment_str = " ; ".join(inline_comments)
        if node.params:
            self.comma_sep_node_list(node.params)
            self.emit(
                node,
                f"{node.target.meta['jac_code']}({node.params.meta['jac_code']})",
            )
        else:
            self.emit(node, f"{node.target.meta['jac_code']}()")
        if isinstance(node.kid[-1], ast.Token) and node.kid[-1].name == "SEMI":
            self.emit_ln(node, node.kid[-1].value + " " + comment_str)

    def exit_expr_list(self, node: ast.ExprList) -> None:
        """Sub objects.

        values: Optional[SubNodeList[ExprType]],
        """
        if node.values is not None:
            self.sep_node_list(node.values, delim=";")
            self.emit(
                node,
                f"{', '.join([value.meta['jac_code'] for value in node.values.items])}",
            )

    def exit_multi_string(self, node: ast.MultiString) -> None:
        """Sub objects.

        strings: list[Token],
        """
        for string in range(0, len(node.strings) - 1):
            self.emit_ln(node, node.strings[string].meta["jac_code"])
        self.emit(node, node.strings[-1].meta["jac_code"])

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
        if node.values is not None:
            self.comma_sep_node_list(node.values)
            self.emit(
                node,
                f"({node.values.meta['jac_code']})",
            )

    def exit_special_var_ref(self, node: ast.SpecialVarRef) -> None:
        """Sub objects.

        var: Token,
        """
        self.emit(node, node.var.value)

    def exit_ability_def(self, node: ast.AbilityDef) -> None:
        """Sub objects.

        target: ArchRefChain,
        signature: FuncSignature | EventSignature,
        body: SubNodeList[CodeBlockStmt],
        kid: list[AstNode],
        doc: Optional[Constant] = None,
        decorators: Optional[SubNodeList[ExprType]] = None,
        """
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
                self.emit(node, f"{fun_def} {node.signature.meta['jac_code']}")
            else:
                self.emit(node, f"{fun_def}")

        if node.body:
            self.emit(node, node.body.meta["jac_code"])

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
            self.emit(
                node,
                f"import:{node.lang.tag.value} from {node.path.meta['jac_code']}, {node.items.meta['jac_code']};",  # noqa
            )
        else:
            if node.is_absorb:
                self.emit(
                    node,
                    f"include:{node.lang.tag.value} {node.path.meta['jac_code']};",
                )
            else:
                self.emit(
                    node,
                    f"import:{node.lang.tag.value} {node.path.meta['jac_code']};",
                )
        self.emit_ln(node, "")

    def exit_arch_def(self, node: ast.ArchDef) -> None:
        """Sub objects.

        target: ArchRefChain,
        body: SubNodeList[ArchBlockStmt],
        doc: Optional[Constant] = None,
        decorators: Optional[SubNodeList[ExprType]] = None,
        """
        doc = node.doc.value if node.doc else ""
        target = f"{node.target.meta['jac_code']} "
        self.emit(node, f"{doc}\n{target}")
        self.emit(node, node.body.meta["jac_code"])

    def exit_ability(self, node: ast.Ability) -> None:
        """Sub objects.

        name_ref: NameType,
        is_func: bool,
        is_async: bool,
        is_static: bool,
        is_abstract: bool,
        access: Optional[SubTag[Token]],
        signature: Optional[FuncSignature | SubNodeList[TypeSpec] | EventSignature],
        body: Optional[SubNodeList[CodeBlockStmt]],
        arch_attached: Optional[Architype] = None,
        doc: Optional[Constant] = None,
        decorators: Optional[SubNodeList[ExprType]] = None,
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
                    else node.name_ref.sym_name
                )
                if node.body:
                    self.emit_ln(
                        node,
                        f"can {can_name} with {node.signature.meta['jac_code']}",  # noqa
                    )

                    self.emit(node, node.body.meta["jac_code"])

                else:
                    self.emit_ln(
                        node,
                        f"can {can_name} with {node.signature.meta['jac_code']};",  # noqa
                    )
            elif isinstance(node.signature, ast.FuncSignature):
                if isinstance(node.name_ref, ast.SpecialVarRef):
                    if access_modifier:
                        fun_signature = f"can:{access_modifier} {node.name_ref.var.value}{node.signature.meta['jac_code']}"  # noqa
                    else:
                        fun_signature = f"can {node.name_ref.var.value}{node.signature.meta['jac_code']}"  # noqa
                else:
                    if access_modifier:
                        fun_signature = f"can:{access_modifier} {node.name_ref.sym_name}{node.signature.meta['jac_code']}"  # noqa
                    else:
                        fun_signature = f"can {node.name_ref.sym_name}{node.signature.meta['jac_code']}"  # noqa
                if node.body:
                    self.emit(node, f"{fun_signature}")
                    self.emit_ln(node, node.body.meta["jac_code"])
                else:
                    if node.is_abstract:
                        self.emit_ln(node, f"{fun_signature} abstract;")
                    else:
                        self.emit_ln(node, f"{fun_signature};")

    def exit_func_signature(self, node: ast.FuncSignature) -> None:
        """Sub objects.

        params: Optional[SubNodeList[ParamVar]],
        return_type: Optional[SubNodeList[TypeSpec]],
        """
        if node.params:
            self.comma_sep_node_list(node.params)
            self.emit(node, f"({node.params.meta['jac_code']})")
        if node.return_type:
            self.emit(node, f" -> {node.return_type.meta['jac_code']}")
        else:
            self.emit(node, " -> None")

    def exit_arch_has(self, node: ast.ArchHas) -> None:
        """Sub objects.

        doc: Optional[Token],
        is_static: bool,
        access: Optional[Token],
        vars: "HasVarList",
        is_frozen: bool,
        """
        comment_str = ""
        standalone_comments, inline_comments = self.emit_comments_for_line(
            node.loc.first_line
        )
        # for comment in standalone_comments:
        #     self.emit_ln(node, f"{comment}")
        if inline_comments:
            comment_str = " ; ".join(inline_comments)
        self.comma_sep_node_list(node.vars)
        if node.access:
            self.emit(
                node,
                f"has:{node.access.meta['jac_code']} {node.vars.meta['jac_code']}",  # {comment_str}",  # noqa
            )
        else:
            self.emit(
                node,
                f"has {node.vars.meta['jac_code']} {comment_str}",
            )
        if isinstance(node.kid[-1], ast.Token) and node.kid[-1].name == "SEMI":
            self.emit_ln(node, node.kid[-1].value + " " + comment_str)

    def exit_arch_ref(self, node: ast.ArchRef) -> None:
        """Sub objects.

        archs: list[ArchRef],
        """
        if isinstance(node.name_ref, ast.SpecialVarRef):
            self.emit(node, f"{node.arch.value}{node.name_ref.var.meta['jac_code']}")
        else:
            self.emit(node, f"{node.arch.value}{node.name_ref.sym_name}")

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

        if node.base_classes:
            self.emit(
                node,
                f"enum {node.name.meta['jac_code']}({node.base_classes.meta['jac_code']})",  # noqa
            )
        else:
            if node.body:
                self.emit(node, f"enum {node.name.value} ")

                if node.doc:
                    self.emit_ln(node, node.doc.value)
                if node.body:
                    self.emit(node, node.body.meta["jac_code"])
                else:
                    self.decl_def_missing(node.name.meta["jac_code"])

            else:
                self.emit(node, f"enum {node.name.value}")

    def exit_enum_def(self, node: ast.EnumDef) -> None:
        """Sub objects.

        doc: Optional[Token],
        mod: Optional[DottedNameList],
        body: EnumBlock,
        """
        if node.doc:
            self.emit_ln(node, node.doc.value)
        self.emit(node, node.target.meta["jac_code"])
        if node.body:
            self.emit(node, node.body.meta["jac_code"])

    # def exit_type_spec(self, node: ast.TypeSpec) -> None:
    #     """Sub objects.

    #     spec_type: Token | SubNodeList[NameType],
    #     list_nest: Optional[TypeSpec],  # needed for lists
    #     dict_nest: Optional[TypeSpec],  # needed for dicts, uses list_nest as key
    #     null_ok: bool = False,
    #     """
    #     if isinstance(node.spec_type, ast.SubNodeList):
    #         self.comma_sep_node_list(node.spec_type)

    #     if node.dict_nest:
    #         self.emit(
    #             node,
    #             f"dict[{node.list_nest.meta['jac_code']}, {node.dict_nest.meta['jac_code']}]",  # noqa
    #         )
    #     elif node.list_nest:
    #         self.emit(node, f"list[{node.list_nest.meta['jac_code']}]")
    #     else:
    #         self.emit(node, node.spec_type.meta["jac_code"])

    def exit_atom_trailer(self, node: ast.AtomTrailer) -> None:
        """Sub objects.

        target: AtomType,
        right: IndexSlice | ArchRefType | Token,
        null_ok: bool,
        """
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

    def exit_atom_unit(self, node: ast.AtomUnit) -> None:
        """Sub objects.

        value: AtomType | ExprType,
        is_paren: bool,
        is_null_ok: bool,
        """
        if node.is_paren:
            self.emit(node, f"({node.value.meta['jac_code']})")
        elif node.is_null_ok:
            self.emit(node, f"{node.value.meta['jac_code']}?")

    def exit_binary_expr(self, node: ast.BinaryExpr) -> None:
        """Sub objects.

        left: ExprType,
        right: ExprType,
        op: Token | DisconnectOp | ConnectOp,
        """
        comment_str = ""
        standalone_comments, inline_comments = self.emit_comments_for_line(
            node.loc.first_line
        )
        # for comment in standalone_comments:
        #     self.emit_ln(node, f"{comment}")
        if inline_comments:
            comment_str = " ; ".join(inline_comments)
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
        if isinstance(node.kid[-1], ast.Token) and node.kid[-1].name == "SEMI":
            self.emit_ln(node, node.kid[-1].value + " " + comment_str)

    def exit_has_var(self, node: ast.HasVar) -> None:
        """Sub objects.

        name: Token,
        type_tag: TypeSpec,
        value: Optional["ExprType"],
        """
        node.type_tag.meta["jac_code"] = node.type_tag.tag.meta["jac_code"]
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

    def comma_sep_node_list(self, node: ast.SubNodeList) -> str:
        """Render comma separated node list."""
        node.meta["jac_code"] = ", ".join([i.meta["jac_code"] for i in node.items])
        return node.meta["jac_code"]

    def dot_sep_node_list(self, node: ast.SubNodeList) -> str:
        """Render dot separated node list."""
        node.meta["jac_code"] = ".".join([i.meta["jac_code"] for i in node.items])
        return node.meta["jac_code"]

    def nl_sep_node_list(self, node: ast.SubNodeList) -> str:
        """Render newline separated node list."""
        node.meta["jac_code"] = ""
        for i in node.items:
            node.meta["jac_code"] += f"{i.meta['jac_code']}\n"
        return node.meta["jac_code"]

    def sep_node_list(self, node: ast.SubNodeList, delim: str = " ") -> str:
        """Render newline separated node list."""
        node.meta["jac_code"] = f"{delim}".join(
            [i.meta["jac_code"] for i in node.items]
        )
        return node.meta["jac_code"]

    def needs_jac_import(self) -> None:
        """Check if import is needed."""
        self.emit_ln_unique(
            self.preamble, "from jaclang import jac_blue_import as __jac_import__"
        )

    def needs_enum(self) -> None:
        """Check if enum is needed."""
        self.emit_ln_unique(
            self.preamble,
            "from enum import Enum as __jac_Enum__, auto as __jac_auto__",
        )

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
        self.emit(node, f"if {node.condition.meta['jac_code']}")
        self.emit(node, node.body.meta["jac_code"])
        if node.elseifs:
            self.emit(node, node.elseifs.meta["jac_code"])
        if node.else_body:
            self.emit(node, node.else_body.meta["jac_code"])

    def exit_else_ifs(self, node: ast.ElseIfs) -> None:
        """Sub objects.

        elseifs: list[IfStmt],
        """
        self.emit(node, f" elif {node.condition.meta['jac_code']}")

        self.emit(node, node.body.meta["jac_code"])

        if node.elseifs:
            self.emit(node, node.elseifs.meta["jac_code"])

    def exit_disengage_stmt(self, node: ast.DisengageStmt) -> None:
        """Sub objects."""
        self.emit(node, "disengage")

    def exit_else_stmt(self, node: ast.ElseStmt) -> None:
        """Sub objects.

        body: CodeBlock,
        """
        self.emit(node, " else")

        self.emit(node, node.body.meta["jac_code"])

    def exit_iter_for_stmt(self, node: ast.IterForStmt) -> None:
        """Sub objects.

        iter: Assignment,
        condition: ExprType,
        count_by: ExprType,
        body: CodeBlock,
        """
        self.emit(
            node,
            f"for {node.iter.meta['jac_code']} to {node.condition.meta['jac_code']} by {node.count_by.meta['jac_code']}",  # noqa
        )

        self.emit(node, node.body.meta["jac_code"])

    def exit_try_stmt(self, node: ast.TryStmt) -> None:
        """Sub objects.

        body: CodeBlock,
        excepts: Optional[ExceptList],
        finally_body: Optional[FinallyStmt],
        """
        self.emit(node, "try")
        self.emit(node, node.body.meta["jac_code"])
        if node.excepts:
            self.emit(node, node.excepts.meta["jac_code"])
        if node.finally_body:
            self.emit(node, node.finally_body.meta["jac_code"])

    def exit_except(self, node: ast.Except) -> None:
        """Sub objects.

        typ: ExprType,
        name: Optional[Token],
        body: CodeBlock,
        """
        comment_str = ""

        if node.name:
            self.emit(
                node,
                f"except {node.ex_type.meta['jac_code']} as {node.name.value}",  # noqa
            )
        else:
            self.emit(node, f"except {node.ex_type.meta['jac_code']} {{ {comment_str}")
        self.emit(node, node.body.meta["jac_code"])

    def exit_finally_stmt(self, node: ast.FinallyStmt) -> None:
        """Sub objects.

        body: CodeBlock,
        """
        self.emit(node, "finally")

        self.emit(node, node.body.meta["jac_code"])

    def exit_while_stmt(self, node: ast.WhileStmt) -> None:
        """Sub objects.

        condition: ExprType,
        body: CodeBlock,
        """
        self.emit(node, f"while {node.condition.meta['jac_code']}")

        self.emit(node, node.body.meta["jac_code"])

    def exit_with_stmt(self, node: ast.WithStmt) -> None:
        """Sub objects.

        exprs: "ExprAsItemList",
        body: "CodeBlock",
        """
        self.comma_sep_node_list(node.exprs)
        self.emit(node, f"with {node.exprs.meta['jac_code']}")
        if node.body.meta["jac_code"]:
            self.emit(node, node.body.meta["jac_code"])

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

    def exit_assignment(self, node: ast.Assignment) -> None:
        """Sub objects.

        is_static: bool,
        target: AtomType,
        value: ExprType,
        """
        comment_str = ""
        standalone_comments, inline_comments = self.emit_comments_for_line(
            node.loc.first_line
        )
        # for comment in standalone_comments:
        #     self.emit_ln(node, f"{comment}")
        if inline_comments:
            comment_str = " ; ".join(inline_comments)
        if node.is_static:
            self.emit(node, "has ")
        self.emit(
            node, f"{node.target.meta['jac_code']} = {node.value.meta['jac_code']}"
        )
        if isinstance(node.kid[-1], ast.Token) and node.kid[-1].name == "SEMI":
            self.emit_ln(node, node.kid[-1].value + " " + comment_str)

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
        if not node.base_classes:
            self.emit(
                node,
                f"{node.arch_type.value} {node.name.meta['jac_code']} ",
            )
        else:
            self.sep_node_list(node.base_classes, delim=":")
            self.emit(
                node,
                f"{node.arch_type.value} {node.name.meta['jac_code']}:{node.base_classes.meta['jac_code']}: ",  # noqa
            )
        body = node.body.body if isinstance(node.body, ast.ArchDef) else node.body
        if body:
            self.emit(node, body.meta["jac_code"])
        else:
            self.decl_def_missing(node.name.meta["jac_code"])
        self.emit_ln(node, "")

    def exit_f_string(self, node: ast.FString) -> None:
        """Sub objects.

        parts: list["Token | ExprType"],
        """
        self.emit(node, 'f"')
        if node.parts:
            for part in node.parts.items:
                if isinstance(part, ast.Constant) and part.name in [
                    Tok.FSTR_PIECE,
                    Tok.FSTR_BESC,
                ]:
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

        values: Optional[SubNodeList[ExprType]],
        """
        if node.values is not None:
            self.comma_sep_node_list(node.values)
            self.emit(
                node,
                f"[{node.values.meta['jac_code']}]",
            )
        else:
            self.emit(node, "[]")

    def exit_set_val(self, node: ast.ListVal) -> None:
        """Sub objects.

        values: list[ExprType],
        """
        if node.values is not None:
            # self.comma_sep_node_list(node.values)
            self.emit(
                node,
                f"{{{node.values.meta['jac_code']}}}",
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
        self.comma_sep_node_list(node.names)
        names = node.names.meta["jac_code"]
        partial = (
            f"{node.out_expr.meta['jac_code']} for {names} "
            f"in {node.collection.meta['jac_code']}"
        )
        if node.conditional:
            partial += f" if {node.conditional.meta['jac_code']}"
        self.emit(node, f"({partial})")

    def exit_list_compr(self, node: ast.ListCompr) -> None:
        """Sub objects.

        compr: InnerCompr,
        """
        self.emit(node, f"[{node.compr.meta['jac_code']}]")

    def exit_gen_compr(self, node: ast.GenCompr) -> None:
        """Sub objects.

        compr: InnerCompr,
        """
        self.emit(node, f"({node.compr.meta['jac_code']},)")

    def exit_set_compr(self, node: ast.SetCompr) -> None:
        """Sub objects.

        compr: InnerCompr,
        """
        self.emit(node, f"{{{node.compr.meta['jac_code']}}}")

    def exit_dict_compr(self, node: ast.DictCompr) -> None:
        """Sub objects.

        outk_expr: ExprType,
        outv_expr: ExprType,
        name_list: NameList,
        collection: ExprType,
        conditional: Optional[ExprType],
        """
        names = node.names.meta["jac_code"]
        partial = f"{node.kv_pair.meta['jac_code']} for " f"{names}"
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
        comment_str = ""
        standalone_comments, inline_comments = self.emit_comments_for_line(
            node.loc.first_line
        )
        for comment in standalone_comments:
            self.emit_ln(node, f"{comment}")
        if inline_comments:
            comment_str = " ; ".join(inline_comments)
        if node.expr:
            self.emit(node, f"yield {node.expr.meta['jac_code']}")
        else:
            self.emit(node, "yield")
        if isinstance(node.kid[-1], ast.Token) and node.kid[-1].name == "SEMI":
            self.emit_ln(node, node.kid[-1].value + " " + comment_str)

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
        comment_str = ""
        standalone_comments, inline_comments = self.emit_comments_for_line(
            node.loc.first_line
        )
        # for comment in standalone_comments:
        #     self.emit_ln(node, f"{comment}")
        if inline_comments:
            comment_str = " ; ".join(inline_comments)
        if node.error_msg:
            self.emit(
                node,
                f"assert {node.condition.meta['jac_code']}, {node.error_msg.meta['jac_code']}",  # noqa
            )
        else:
            self.emit(node, f"assert {node.condition.meta['jac_code']}")

        if isinstance(node.kid[-1], ast.Token) and node.kid[-1].name == "SEMI":
            self.emit_ln(node, node.kid[-1].value + " " + comment_str)

    def exit_ctrl_stmt(self, node: ast.CtrlStmt) -> None:
        """Sub objects.

        ctrl: Token,
        """
        if node.ctrl.name == Tok.KW_SKIP:
            self.ds_feature_warn()
        else:
            self.emit(node, node.ctrl.value)
        if isinstance(node.kid[-1], ast.Token) and node.kid[-1].name == "SEMI":
            self.emit_ln(node, node.kid[-1].value)

    def exit_delete_stmt(self, node: ast.DeleteStmt) -> None:
        """Sub objects.

        target: ExprType,
        """
        self.emit(node, f"del {node.target.meta['jac_code']}")
        if isinstance(node.kid[-1], ast.Token) and node.kid[-1].name == "SEMI":
            self.emit_ln(node, node.kid[-1].value)

    def exit_report_stmt(self, node: ast.ReportStmt) -> None:
        """Sub objects.

        expr: ExprType,
        """
        self.ds_feature_warn()

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

        name_list: SubNodeList[Name],
        collection: ExprType,
        body: SubNodeList[CodeBlockStmt],
        """
        names = node.name_list.meta["jac_code"]
        self.emit(node, f"for {names} in {node.collection.meta['jac_code']}")
        if node.body:
            self.emit(node, node.body.meta["jac_code"])

    def exit_test(self, node: ast.Test) -> None:
        """Sub objects.

        name: Optional[Name],
        doc: Optional[Token],
        body: CodeBlock,
        """
        comment_str = ""
        test_name = node.name.value
        if node.doc:
            self.emit_ln(node, node.doc.meta["jac_code"])
        if test_name:
            self.emit_ln(node, f"test {test_name} {{ {comment_str}")
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

    def exit_builtin_type(self, node: ast.BuiltinType) -> None:
        """Sub objects.

        name: str,
        value: str,
        line: int,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        """
        self.emit(node, node.value)
