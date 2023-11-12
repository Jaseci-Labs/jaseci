"""JacFormatPass for Jaseci Ast.

This is a pass for formatting Jac code.
"""

from typing import Any, List, Tuple

import jaclang.jac.absyntree as ast
from jaclang.jac import constant
from jaclang.jac.constant import Constants as Con
from jaclang.jac.constant import Tokens as Tok
from jaclang.jac.passes import Pass


class JacFormatPass(Pass):
    """JacFormat Pass format Jac code."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # noqa  # noqa
        """Initialize Formatter."""
        self.comments = []
        self.processed_comments = set()

        super().__init__(*args, **kwargs)

    def before_pass(self) -> None:
        """Initialize pass."""
        self.indent_size = 4
        self.indent_level = 0
        self.debuginfo = {"jac_mods": []}
        self.preamble = ast.EmptyToken()
        self.preamble.gen.jac = ""

    def get_comments_from_first_column(self) -> List[Tuple[int, str]]:
        """Get all comments that belong to column 1."""
        next_line_standalone_comments = []
        for comment in self.comments:
            formatted_comment_lines = self.format_comment_to_limit(comment.value)
            # for formatted_line in formatted_comment_lines:
            next_line_standalone_comments.append(
                (comment.line, formatted_comment_lines)
            )
        return next_line_standalone_comments

    def format_comment_to_limit(self, comment: str, char_limit: int = 80) -> List[str]:
        """Insert Line break for comments."""
        if comment.startswith("#"):
            comment = comment[1:].strip()

        words = comment.split()
        formatted_lines = []
        current_line = "#"

        for word in words:
            if len(current_line + " " + word) <= char_limit:
                current_line += " " + word
            else:
                formatted_lines.append(current_line.strip())
                current_line = "#" + " " + word

        if current_line != "#":
            formatted_lines.append(current_line.strip())

        return "\n".join(formatted_lines)

    def insert_line_breaks(self, line: str, max_len: int = 60) -> str:
        """Insert Line break for code."""
        if len(line) <= max_len:
            return line

        # Find the last occurrence of ',' or ')' before the max length
        break_point = max_len
        while break_point > 0:
            if line[break_point] in [",", ")"]:
                break_point += 1
                break
            break_point -= 1

        # If no comma or parenthesis is found, just split at max_len
        if break_point == 0:
            break_point = max_len

        # Split the line into two parts at the break_point
        part1 = line[:break_point]
        part2 = line[break_point:]
        # Add indentation to part2 if it starts with "|>"
        if part2.strip().startswith("|>"):
            part2 = (" " * 4) + part2.lstrip()
        # If the second part exceeds max_len, call the function recursively
        if len(part2) > max_len:
            part2 = self.insert_line_breaks(part2, max_len)

        return part1 + "\n" + part2

    def emit_comments_for_line(
        self, line: int
    ) -> Tuple[List[Tuple[int, str]], List[Tuple[int, str]]]:
        """Stitch comments associated with the given line."""
        if not line:
            return [], []

        inline_comments = []
        next_line_standalone_comments = []

        i = 0
        while i < len(self.comments):
            comment = self.comments[i]
            # Skip comments that start on the 1st column
            if comment.column == 1:
                i += 1
                continue
            # Check if this is a multiline comment
            if comment.value.startswith("#*"):
                end_line = comment.line
                while i < len(self.comments) and not self.comments[i].value.endswith(
                    "*#"
                ):
                    i += 1
                if i < len(self.comments):
                    end_line = self.comments[i].line  # noqa
                # Format the multiline comment and store it with the starting line
                formatted_comment_lines = self.format_comment_to_limit(comment.value)
                # for formatted_line in formatted_comment_lines:
                next_line_standalone_comments.append(
                    (comment.line, formatted_comment_lines)
                )

                i += 1  # Move past the multiline comment
            else:
                # Process regular inline or standalone comment
                if comment.line == line:
                    if (
                        comment.column < 10
                        and comment.value not in self.processed_comments
                    ):
                        next_line_standalone_comments.append(
                            (comment.line, comment.value)
                        )
                    else:
                        inline_comments.append((comment.line, comment.value))
                elif (
                    (comment.line == line + 1 or comment.line == line + 2)
                    and comment.value not in self.processed_comments
                    and comment.column < 10
                ):
                    next_line_standalone_comments.append((comment.line, comment.value))
                i += 1  # Move to the next comment

        return (
            inline_comments,
            next_line_standalone_comments,
        )

    def enter_node(self, node: ast.AstNode) -> None:
        """Enter node."""
        if node:
            node.gen.jac = ""
        return Pass.enter_node(self, node)

    def indent_str(self) -> str:
        """Return string for indent."""
        return " " * self.indent_size * self.indent_level

    def emit(self, node: ast.AstNode, s: str) -> None:
        """Emit code to node."""
        node.gen.jac += self.indent_str() + s.replace("\n", "\n" + self.indent_str())
        if "\n" in node.gen.jac:
            node.gen.jac = node.gen.jac.rstrip(" ")

    def emit_ln(self, node: ast.AstNode, s: str) -> None:
        """Emit code to node."""
        self.emit(node, s.strip().strip("\n"))
        self.emit(node, "\n")

    def emit_ln_unique(self, node: ast.AstNode, s: str) -> None:
        """Emit code to node."""
        if s not in node.gen.jac:
            ilev = self.indent_level
            self.indent_level = 0
            self.emit_ln(node, s)
            self.indent_level = ilev

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
            elif isinstance(i, ast.SubTag):
                self.emit(node, ":" + i.gen.jac.strip("") + " ")

        if node.body:
            self.emit(node, node.body.gen.jac)

    def enter_module(self, node: ast.Module) -> None:
        """Sub objects.

        name: Optional[SubTag[Name]],
        body: SubNodeList[CodeBlockStmt],
        doc: Optional[Constant] = None,
        """
        if node.source.comments:
            self.comments = node.source.comments

    def exit_module(self, node: ast.Module) -> None:
        """Sub objects.

        name: str,
        doc: Token,
        body: "Elements",
        """
        standalone_comments = self.get_comments_from_first_column()
        if node.doc:
            self.emit_ln(node, node.doc.value)
            self.emit_ln(node, "")
        if self.preamble:
            self.emit(node, self.preamble.gen.jac)
        if node.body:
            for i in node.body:
                for next_line_no, next_line_comment in standalone_comments:
                    if (
                        next_line_no <= i.loc.first_line
                        and next_line_comment not in self.processed_comments
                    ):
                        self.emit_ln(node, next_line_comment)
                        if next_line_comment.startswith("#*"):
                            self.emit_ln(node, "")
                        self.processed_comments.add(next_line_comment)
                        break
                self.emit(node, i.gen.jac)
        self.ir = node
        self.ir.gen.jac = self.ir.gen.jac.rstrip()

    def exit_sub_node_list(self, node: ast.SubNodeList) -> None:
        """Sub objects.

        items: list[T],
        """
        for stmt in node.kid:
            comment_str = ""
            (
                inline_comments,
                next_line_standalone_comments,
            ) = self.emit_comments_for_line(stmt.loc.first_line)
            if inline_comments:
                comment_str = " ; ".join(
                    comment_value for _, comment_value in inline_comments
                )
            if isinstance(stmt, ast.Token):
                if stmt.name == "LBRACE":
                    if comment_str not in self.processed_comments and comment_str != "":
                        self.emit_ln(node, f"{stmt.value} {comment_str}")
                        self.processed_comments.add(comment_str)
                    else:
                        self.emit_ln(node, f"{stmt.value}")
                    self.indent_level += 1
                    for (
                        next_line_no,
                        next_line_comment,
                    ) in next_line_standalone_comments:
                        if (
                            next_line_no == node.loc.first_line + 1
                            or next_line_no == node.loc.first_line + 2
                        ) and next_line_comment not in self.processed_comments:
                            # Emit the comment on the next line
                            self.emit_ln(node, next_line_comment)
                            self.processed_comments.add(next_line_comment)
                elif stmt.name == "RBRACE":
                    # self.emit_ln(node, "")
                    self.indent_level -= 1
                    if comment_str not in self.processed_comments and comment_str != "":
                        self.emit_ln(node, f"{stmt.value} {comment_str}")
                        self.processed_comments.add(comment_str)
                    elif isinstance(stmt.parent.parent, (ast.ElseIf, ast.IfStmt)):
                        self.emit(node, f"{stmt.value}")
                    else:
                        self.emit_ln(node, f"{stmt.value}")
                    # self.emit_ln(node, "")
                else:
                    self.emit(node, f"{stmt.value}")
                    continue
            elif isinstance(stmt, ast.Assignment):
                self.emit(node, f"{stmt.gen.jac}")
            else:
                if isinstance(stmt, ast.ExprStmt):
                    formatted_line = self.insert_line_breaks(stmt.gen.jac)
                    self.emit(node, f"{formatted_line}")
                else:
                    if comment_str not in self.processed_comments and comment_str != "":
                        self.emit_ln(node, f"{stmt.gen.jac} {comment_str}")
                        self.processed_comments.add(comment_str)
                    else:
                        self.emit(node, f"{stmt.gen.jac}")
                        continue
            for next_line_no, next_line_comment in next_line_standalone_comments:
                if (
                    next_line_no == node.loc.first_line + 1
                    or next_line_no == node.loc.first_line + 2
                ) and next_line_comment not in self.processed_comments:
                    # Emit the comment on the next line
                    self.emit_ln(node, next_line_comment)
                    self.processed_comments.add(next_line_comment)

    def exit_sub_tag(self, node: ast.SubTag) -> None:
        """Sub objects.

        tag: T,
        """
        self.emit(node, node.tag.gen.jac)

    def exit_func_call(self, node: ast.FuncCall) -> None:
        """Sub objects.

        target: AtomType,
        params: Optional[ParamList],
        """
        comment_str = ""
        (
            inline_comments,
            _,
        ) = self.emit_comments_for_line(node.loc.first_line)
        if inline_comments:
            comment_str = " ; ".join(
                comment_value for _, comment_value in inline_comments
            )
        if node.params:
            self.comma_sep_node_list(node.params)
            self.emit(
                node,
                f"{node.target.gen.jac}({node.params.gen.jac})",
            )
        else:
            self.emit(node, f"{node.target.gen.jac}()")
        if isinstance(node.kid[-1], ast.Token) and node.kid[-1].name == "SEMI":
            self.emit_ln(node, node.kid[-1].value + " " + comment_str)
            self.processed_comments.add(comment_str)

    def exit_expr_list(self, node: ast.ExprList) -> None:
        """Sub objects.

        values: Optional[SubNodeList[ExprType]],
        """
        if node.values is not None:
            self.sep_node_list(node.values, delim=";")
            self.emit(
                node,
                f"{', '.join([value.gen.jac for value in node.values.items])}",
            )

    def exit_multi_string(self, node: ast.MultiString) -> None:
        """Sub objects.

        strings: list[Token],
        """
        if len(node.strings) > 1:
            self.emit_ln(node, node.strings[0].gen.jac)
            self.indent_level += 1
            for string in range(1, len(node.strings) - 1):
                self.emit_ln(node, node.strings[string].gen.jac)
            self.emit(node, node.strings[-1].gen.jac)
            self.indent_level -= 1
        else:
            self.emit(node, node.strings[0].gen.jac)

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
                f"({node.values.gen.jac})",
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
            self.emit_ln(node, node.doc.gen.jac)
        if isinstance(node.signature, ast.EventSignature):
            # need to find a example and implement
            self.warning("This Event Defination is not available currently")
            return
        else:
            fun_def = ""
            for arch in node.target.archs:
                fun_def += arch.gen.jac
            if node.signature.gen.jac.strip():
                self.emit(node, f"{fun_def} {node.signature.gen.jac} ")
            else:
                self.emit(node, f"{fun_def} ")

        if node.body:
            self.emit(node, node.body.gen.jac)
        self.emit_ln(node, "")

    def exit_event_signature(self, node: ast.EventSignature) -> None:
        """Sub objects.

        event: Token,
        arch_tag_info: Optional["TypeList | TypeSpec"],
        return_type: Optional["TypeSpec"],
        """
        event_value = node.event.value if node.event else None
        if node.arch_tag_info:
            self.emit(node, f"{node.arch_tag_info.gen.jac} {event_value}")
        else:
            self.emit(node, f"{event_value}")

    def exit_import(self, node: ast.Import) -> None:
        """Sub objects.

        lang: SubTag[Name],
        path: ModulePath,
        alias: Optional[Name],
        items: Optional[SubNodeList[ModuleItem]],
        is_absorb: bool,  # For includes
        doc: Optional[Constant] = None,
        sub_module: Optional[Module] = None,
        """
        if node.items:
            self.emit(
                node,
                f"import:{node.lang.tag.value} from {node.path.gen.jac}, {node.items.gen.jac};",  # noqa
            )
        else:
            if node.is_absorb:
                self.emit_ln(
                    node,
                    f"include:{node.lang.tag.value} {node.path.gen.jac};",
                )
            else:
                self.emit(
                    node,
                    f"import:{node.lang.tag.value} {node.path.gen.jac};",
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
        target = f"{node.target.gen.jac} "
        self.emit(node, f"{doc}\n{target}")
        self.emit(node, node.body.gen.jac)

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
        comment_str = ""
        (
            inline_comments,
            next_line_standalone_comments,
        ) = self.emit_comments_for_line(node.loc.first_line)
        # for comment in standalone_comments:
        #     self.emit_ln(node, f"{comment}")
        if inline_comments:
            comment_str = " ; ".join(
                comment_value for _, comment_value in inline_comments
            )
        access_modifier = None
        if node.doc:
            self.emit_ln(node, node.doc.gen.jac)
        if node.access:
            access_modifier = node.access.gen.jac
        if node.decorators:
            self.emit(node, node.decorators.gen.jac)
        if isinstance(node.signature, (ast.FuncSignature, ast.EventSignature)):
            if isinstance(node.signature, ast.EventSignature):
                can_name = (
                    node.name_ref.value
                    if isinstance(node.name_ref, ast.Name)
                    else node.name_ref.sym_name
                )
                if node.body:
                    self.emit(
                        node,
                        f"can {can_name} with {node.signature.gen.jac}",  # noqa
                    )

                    self.emit(node, node.body.gen.jac)

                else:
                    self.emit(
                        node,
                        f"can {can_name} with {node.signature.gen.jac}",  # noqa
                    )
            elif isinstance(node.signature, ast.FuncSignature):
                if isinstance(node.name_ref, ast.SpecialVarRef):
                    if access_modifier:
                        fun_signature = f"can:{access_modifier} {node.name_ref.var.value}{node.signature.gen.jac}"  # noqa
                    else:
                        fun_signature = f"can {node.name_ref.var.value}{node.signature.gen.jac}"  # noqa
                else:
                    if access_modifier:
                        fun_signature = f"can:{access_modifier} {node.name_ref.sym_name}{node.signature.gen.jac}"  # noqa
                    else:
                        fun_signature = f"can {node.name_ref.sym_name}{node.signature.gen.jac}"  # noqa
                if node.body:
                    self.emit(node, f"{fun_signature}")
                    self.emit(node, node.body.gen.jac)
                else:
                    if node.is_abstract:
                        self.emit(node, f"{fun_signature} abstract")
                    else:
                        self.emit(node, f"{fun_signature}")
            if isinstance(node.kid[-1], ast.Token) and node.kid[-1].name == "SEMI":
                self.emit_ln(node, node.kid[-1].value + " " + comment_str)
                self.processed_comments.add(comment_str)

    def exit_func_signature(self, node: ast.FuncSignature) -> None:
        """Sub objects.

        params: Optional[SubNodeList[ParamVar]],
        return_type: Optional[SubNodeList[TypeSpec]],
        """
        empty_token = False
        return_sub_tag = None
        for kid in node.kid:
            if isinstance(kid, ast.EmptyToken):
                empty_token = True
            if isinstance(kid, ast.SubTag):
                return_sub_tag = kid.gen.jac
        if node.params:
            self.comma_sep_node_list(node.params)
            self.emit(node, f"({node.params.gen.jac})")
        if node.return_type:
            self.emit(node, f" -> {node.return_type.gen.jac} ")
        elif empty_token:
            self.emit(node, " ")
        elif return_sub_tag:
            self.emit(node, f" -> {return_sub_tag}")
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
        (
            inline_comments,
            _,
        ) = self.emit_comments_for_line(node.loc.first_line)
        if inline_comments:
            comment_str = " ; ".join(
                comment_value for _, comment_value in inline_comments
            )
        self.comma_sep_node_list(node.vars)
        if node.access:
            self.emit(
                node,
                f"has:{node.access.gen.jac} {node.vars.gen.jac}",  # {comment_str}",  # noqa
            )
        else:
            self.emit(
                node,
                f"has {node.vars.gen.jac}",
            )
        if isinstance(node.kid[-1], ast.Token) and node.kid[-1].name == "SEMI":
            if comment_str != "":
                self.emit_ln(node, node.kid[-1].value + " " + comment_str)
                self.processed_comments.add(comment_str)
            else:
                self.emit_ln(node, node.kid[-1].value.strip(" "))

    def exit_arch_ref(self, node: ast.ArchRef) -> None:
        """Sub objects.

        archs: list[ArchRef],
        """
        if isinstance(node.name_ref, ast.SpecialVarRef):
            self.emit(node, f"{node.arch.value}{node.name_ref.var.gen.jac}")
        else:
            self.emit(node, f"{node.arch.value}{node.name_ref.sym_name}")

    def exit_param_var(self, node: ast.ParamVar) -> None:
        """Sub objects.

        name: Name,
        unpack: Optional[Token],
        type_tag: SubTag[SubNodeList[TypeSpec]],
        value: Optional[ExprType],
        """
        if node.unpack:
            self.emit(node, f"{node.unpack.value}")
        if node.value:
            self.emit(
                node,
                f"{node.name.value}: {node.type_tag.gen.jac} = {node.value.gen.jac}",  # noqa
            )
        else:
            self.emit(node, f"{node.name.value}: {node.type_tag.gen.jac}")

    def exit_enum(self, node: ast.Enum) -> None:
        """Sub objects.

        name: Name,
        doc: Optional[Token],
        decorators: Optional[Decorators],
        access: Optional[Token],
        base_classes: BaseClasses,
        body: Optional[EnumBlock],
        """
        if node.doc:
            self.emit_ln(node, node.doc.value)
        if node.decorators:
            self.emit_ln(node, node.decorators.gen.jac)
        if node.base_classes:
            self.emit(
                node,
                f"enum {node.name.gen.jac}({node.base_classes.gen.jac})",  # noqa
            )
        else:
            self.emit(node, f"enum {node.name.value} ")
        if node.body:
            for stmt in node.body.kid:
                if isinstance(stmt, ast.Token):
                    if stmt.name == "LBRACE":
                        self.emit_ln(node, f"{stmt.value}")
                        self.indent_level += 1
                    elif stmt.name == "RBRACE":
                        self.emit_ln(node, "")
                        self.indent_level -= 1
                        self.emit_ln(node, f"{stmt.value}")
                        # self.emit_ln(node, "")
                    else:
                        self.indent_level -= 1
                        self.emit_ln(node, f"{stmt.value}")
                        self.indent_level += 1
                else:
                    self.emit(node, f"{stmt.gen.jac}")
        else:
            self.emit_ln(node, "")

    def exit_enum_def(self, node: ast.EnumDef) -> None:
        """Sub objects.

        doc: Optional[Token],
        mod: Optional[DottedNameList],
        body: EnumBlock,
        """
        if node.doc:
            self.emit_ln(node, node.doc.value)
        self.emit(node, node.target.gen.jac)
        if node.body:
            self.emit(node, node.body.gen.jac)

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
    #             f"dict[{node.list_nest.gen.jac}, {node.dict_nest.gen.jac}]",  # noqa
    #         )
    #     elif node.list_nest:
    #         self.emit(node, f"list[{node.list_nest.gen.jac}]")
    #     else:
    #         self.emit(node, node.spec_type.gen.jac)

    def exit_atom_trailer(self, node: ast.AtomTrailer) -> None:
        """Sub objects.

        target: AtomType,
        right: IndexSlice | ArchRefType | Token,
        null_ok: bool,
        """
        if isinstance(node.right, ast.IndexSlice):
            self.emit(
                node,
                f"{node.target.gen.jac}{node.right.gen.jac}",
            )
        else:
            self.emit(
                node,
                f"{node.target.gen.jac}.{node.right.gen.jac}",
            )

    def exit_atom_unit(self, node: ast.AtomUnit) -> None:
        """Sub objects.

        value: AtomType | ExprType,
        is_paren: bool,
        is_null_ok: bool,
        """
        self.emit(node, f"({node.value.gen.jac})")

    def exit_yield_expr(self, node: ast.YieldExpr) -> None:
        """Sub objects.

        expr: Optional[ExprType],
        """
        comment_str = ""
        (
            inline_comments,
            _,
        ) = self.emit_comments_for_line(node.loc.first_line)
        if inline_comments:
            comment_str = " ; ".join(
                comment_value for _, comment_value in inline_comments
            )
        if not node.with_from and node.expr:
            self.emit(node, f"yield {node.expr.gen.jac}")
        elif node.expr:
            self.emit(node, f"yield from {node.expr.gen.jac}")
        else:
            self.emit(node, "yield")
        if isinstance(node.kid[-1], ast.Token) and node.kid[-1].name == "SEMI":
            self.emit_ln(node, node.kid[-1].value + " " + comment_str)
            self.processed_comments.add(comment_str)

    def exit_binary_expr(self, node: ast.BinaryExpr) -> None:
        """Sub objects.

        left: ExprType,
        right: ExprType,
        op: Token | DisconnectOp | ConnectOp,
        """
        comment_str = ""
        (
            inline_comments,
            _,
        ) = self.emit_comments_for_line(node.loc.first_line)
        if inline_comments:
            comment_str = " ; ".join(
                comment_value for _, comment_value in inline_comments
            )
        if isinstance(node.op, (ast.DisconnectOp, ast.ConnectOp)):
            self.emit(
                node,
                f"{node.left.gen.jac} {node.op.gen.jac} {node.right.gen.jac}",  # noqa
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
                    f"{node.left.gen.jac} {node.op.value} {node.right.gen.jac}",  # noqa
                )
            elif node.op.name in [
                Tok.PIPE_FWD,
                Tok.KW_SPAWN,
                Tok.A_PIPE_FWD,
            ] and isinstance(node.left, ast.TupleVal):
                self.emit(
                    node,
                    f"{node.left.gen.jac} {node.op.gen.jac} {node.right.gen.jac}",  # noqa
                )
            elif node.op.name in [Tok.PIPE_BKWD, Tok.A_PIPE_BKWD] and isinstance(
                node.right, ast.TupleVal
            ):
                params = node.right.gen.jac
                params = params.replace(",)", ")") if params[-2:] == ",)" else params
                self.emit(node, f"{node.left.gen.jac}{params}")
            elif (
                node.op.name == Tok.PIPE_FWD and isinstance(node.right, ast.TupleVal)
            ) or node.op.name == Tok.PIPE_FWD:
                self.emit(
                    node,
                    f"{node.left.gen.jac} |> {node.right.gen.jac}",
                )
            elif node.op.name in [Tok.KW_SPAWN, Tok.A_PIPE_FWD]:
                self.emit(
                    node,
                    f"{node.left.gen.jac} :> {node.right.gen.jac}",
                )
            elif node.op.name in [Tok.PIPE_BKWD, Tok.A_PIPE_BKWD]:
                self.emit(
                    node,
                    f"{node.left.gen.jac} <: {node.right.gen.jac}",
                )
            elif node.op.name == Tok.ELVIS_OP:
                self.emit(
                    node,
                    f"{Con.JAC_TMP} "
                    f"if ({Con.JAC_TMP} := ({node.left.gen.jac})) is not None "
                    f"else {node.right.gen.jac}",
                )
            else:
                self.error(
                    f"Binary operator {node.op.value} not supported in bootstrap Jac"
                )
        if isinstance(node.kid[-1], ast.Token) and node.kid[-1].name == "SEMI":
            self.emit_ln(node, node.kid[-1].value + " " + comment_str)
            self.processed_comments.add(comment_str)

    def exit_has_var(self, node: ast.HasVar) -> None:
        """Sub objects.

        name: Token,
        type_tag: TypeSpec,
        value: Optional["ExprType"],
        """
        node.type_tag.gen.jac = node.type_tag.tag.gen.jac
        if node.value:
            self.emit(
                node,
                f"{node.name.gen.jac}: {node.type_tag.gen.jac} = {node.value.gen.jac}",  # noqa
            )
        else:
            self.emit(node, f"{node.name.value}: {node.type_tag.gen.jac}")

    def get_mod_index(self, node: ast.AstNode) -> int:
        """Get module index."""
        path = node.loc.mod_path
        if not path:
            return -1
        if path not in self.debuginfo["jac_mods"]:
            self.debuginfo["jac_mods"].append(path)
        return self.debuginfo["jac_mods"].index(path)

    def comma_sep_node_list(self, node: ast.SubNodeList) -> str:
        """Render comma separated node list."""
        node.gen.jac = ", ".join([i.gen.jac for i in node.items])
        return node.gen.jac

    def dot_sep_node_list(self, node: ast.SubNodeList) -> str:
        """Render dot separated node list."""
        node.gen.jac = ".".join([i.gen.jac for i in node.items])
        return node.gen.jac

    def nl_sep_node_list(self, node: ast.SubNodeList) -> str:
        """Render newline separated node list."""
        node.gen.jac = ""
        for i in node.items:
            node.gen.jac += f"{i.gen.jac}\n"
        return node.gen.jac

    def sep_node_list(self, node: ast.SubNodeList, delim: str = " ") -> str:
        """Render newline separated node list."""
        node.gen.jac = f"{delim}".join([i.gen.jac for i in node.items])
        return node.gen.jac

    def needs_jac_import(self) -> None:
        """Check if import is needed."""
        self.emit_ln_unique(
            self.preamble, "from jaclang import jac_import as __jac_import__"
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
        self.emit(node, f"if {node.condition.gen.jac} ")
        self.emit(node, node.body.gen.jac)

        if node.else_body:
            self.emit(node, node.else_body.gen.jac)

    def exit_else_if(self, node: ast.ElseIf) -> None:
        """Sub objects.

        elseifs: list[IfStmt],
        """
        self.emit(node, f" elif {node.condition.gen.jac} ")
        self.emit(node, node.body.gen.jac)

        if node.else_body:
            self.emit(node, node.else_body.gen.jac)

    def exit_disengage_stmt(self, node: ast.DisengageStmt) -> None:
        """Sub objects."""
        for i in node.kid:
            self.emit(node, i.gen.jac)
        self.emit_ln(node, "")

    def exit_else_stmt(self, node: ast.ElseStmt) -> None:
        """Sub objects.

        body: CodeBlock,
        """
        self.emit(node, " else ")
        self.emit(node, node.body.gen.jac)

    def exit_expr_stmt(self, node: ast.ExprStmt) -> None:
        """Sub objects.

        expr: ExprType,
        """
        self.emit(node, node.expr.gen.jac)
        if isinstance(node.kid[-1], ast.Token) and node.kid[-1].name == "SEMI":
            self.emit_ln(node, node.kid[-1].value)

    def exit_iter_for_stmt(self, node: ast.IterForStmt) -> None:
        """Sub objects.

        iter: Assignment,
        condition: ExprType,
        count_by: ExprType,
        body: CodeBlock,
        """
        self.emit(
            node,
            f"for {node.iter.gen.jac} to {node.condition.gen.jac} by {node.count_by.gen.jac} ",  # noqa
        )

        self.emit(node, node.body.gen.jac)

    def exit_try_stmt(self, node: ast.TryStmt) -> None:
        """Sub objects.

        body: CodeBlock,
        excepts: Optional[ExceptList],
        finally_body: Optional[FinallyStmt],
        """
        self.emit(node, "try")
        self.emit(node, node.body.gen.jac)
        if node.excepts:
            self.emit(node, node.excepts.gen.jac)
        if node.finally_body:
            self.emit(node, node.finally_body.gen.jac)

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
                f"except {node.ex_type.gen.jac} as {node.name.value}",  # noqa
            )
        else:
            self.emit(node, f"except {node.ex_type.gen.jac} {{ {comment_str}")
        self.emit(node, node.body.gen.jac)

    def exit_finally_stmt(self, node: ast.FinallyStmt) -> None:
        """Sub objects.

        body: CodeBlock,
        """
        self.emit(node, "finally")

        self.emit(node, node.body.gen.jac)

    def exit_while_stmt(self, node: ast.WhileStmt) -> None:
        """Sub objects.

        condition: ExprType,
        body: CodeBlock,
        """
        self.emit(node, f"while {node.condition.gen.jac}")

        self.emit(node, node.body.gen.jac)

    def exit_with_stmt(self, node: ast.WithStmt) -> None:
        """Sub objects.

        exprs: "ExprAsItemList",
        body: "CodeBlock",
        """
        self.comma_sep_node_list(node.exprs)
        self.emit(node, f"with {node.exprs.gen.jac}")
        if node.body.gen.jac:
            self.emit(node, node.body.gen.jac)

    def exit_global_vars(self, node: ast.GlobalVars) -> None:
        """Sub objects.

        access: Optional[SubTag[Token]],
        assignments: SubNodeList[Assignment],
        is_frozen: bool,
        doc: Optional[Constant] = None,
        """
        comment_str = ""
        (
            inline_comments,
            _,
        ) = self.emit_comments_for_line(node.loc.first_line)
        if inline_comments:
            comment_str = " ; ".join(
                comment_value for _, comment_value in inline_comments
            )
        if node.doc:
            self.emit_ln(node, node.doc.value)
        for i in node.kid:
            if isinstance(i, ast.Token):
                if i.name == "SEMI":
                    self.emit_ln(node, i.value + " " + comment_str)
                    self.processed_comments.add(comment_str)
                else:
                    self.emit(node, i.value + " ")
            elif isinstance(i, ast.SubNodeList):
                self.emit(node, node.assignments.gen.jac)
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

    def exit_global_stmt(self, node: ast.GlobalStmt) -> None:
        """Sub objects.

        target: SubNodeList[NameType],
        """
        self.emit(node, ":g:")
        self.comma_sep_node_list(node.target)
        self.emit_ln(node, f"{node.target.gen.jac}")

    def exit_non_local_stmt(self, node: ast.GlobalStmt) -> None:
        """Sub objects.

        target: SubNodeList[NameType],
        """
        self.emit(node, ":nl:")
        self.comma_sep_node_list(node.target)
        self.emit_ln(node, f"{node.target.gen.jac}")

    def exit_assignment(self, node: ast.Assignment) -> None:
        """Sub objects.

        target: SubNodeList[AtomType],
        value: Optional[ExprType | YieldStmt],
        type_tag: Optional[SubTag[ExprType]],
        mutable: bool = True,
        """
        comment_str = ""
        (
            inline_comments,
            _,
        ) = self.emit_comments_for_line(node.loc.first_line)
        if inline_comments:
            comment_str = " ; ".join(
                comment_value for _, comment_value in inline_comments
            )
        self.sep_node_list(node.target, delim="=")
        self.emit(node, node.target.gen.jac)
        if node.type_tag:
            self.emit(node, f": {node.type_tag.tag.gen.jac}")
        if node.value:
            self.emit(node, f" = {node.value.gen.jac}")
        if isinstance(node.kid[-1], ast.Token) and node.kid[-1].name == "SEMI":
            self.emit_ln(node, node.kid[-1].value + " " + comment_str)
            self.processed_comments.add(comment_str)

    def exit_architype(self, node: ast.Architype) -> None:
        """Sub objects.

        name: Name,
        arch_type: Token,
        access: Optional[SubTag[Token]],
        base_classes: Optional[SubNodeList[AtomType]],
        body: Optional[SubNodeList[ArchBlockStmt] | ArchDef],
        doc: Optional[Constant] = None,
        decorators: Optional[SubNodeList[ExprType]] = None,
        """
        self.emit_ln(node, "")
        if node.doc:
            self.emit_ln(node, node.doc.value)
        if node.decorators:
            self.emit_ln(node, node.decorators.gen.jac)
        if not node.base_classes:
            self.emit(
                node,
                f"{node.arch_type.value} {node.name.gen.jac} ",
            )
        else:
            self.sep_node_list(node.base_classes, delim=":")
            self.emit(
                node,
                f"{node.arch_type.value} {node.name.gen.jac}:{node.base_classes.gen.jac}: ",  # noqa
            )
        body = node.body.body if isinstance(node.body, ast.ArchDef) else node.body
        if body:
            self.emit(node, body.gen.jac)
        else:
            self.decl_def_missing(node.name.gen.jac)
        self.emit_ln(node, "")

    def exit_f_string(self, node: ast.FString) -> None:
        """Sub objects.

        parts: list["Token | ExprType"],
        """
        self.emit(node, 'f"')
        if node.parts:
            for part in node.parts.items:
                if isinstance(part, ast.String) and part.name in [
                    Tok.FSTR_PIECE,
                    Tok.FSTR_BESC,
                ]:
                    self.emit(node, f"{part.gen.jac}")
                else:
                    self.emit(node, "{" + part.gen.jac + "}")
        self.emit(node, '"')

    def exit_if_else_expr(self, node: ast.IfElseExpr) -> None:
        """Sub objects.

        condition: BinaryExpr | IfElseExpr,
        value: ExprType,
        else_value: ExprType,
        """
        self.emit(
            node,
            f"{node.value.gen.jac} if {node.condition.gen.jac} "
            f"else {node.else_value.gen.jac}",
        )

    def decl_def_missing(self, decl: str = "this") -> None:
        """Warn about declaration."""
        self.error(
            f"Unable to find definition for {decl} declaration. Perhaps there's an `include` missing?"  # noqa
        )

    def exit_lambda_expr(self, node: ast.LambdaExpr) -> None:
        """Sub objects.

        params: Optional[SubNodeList[ParamVar]],
        return_type: Optional[SubTag[ExprType]],
        body: ExprType,
        """
        out = ""
        if node.params:
            self.comma_sep_node_list(node.params)
            out += node.params.gen.jac
        if node.return_type:
            out += f" -> {node.return_type.tag.gen.jac}"
        self.emit(node, f"with {out} can {node.body.gen.jac}")

    def exit_unary_expr(self, node: ast.UnaryExpr) -> None:
        """Sub objects.

        operand: ExprType,
        op: Token,
        """
        if node.op.value in ["-", "~", "+", "*", "**"]:
            self.emit(node, f"{node.op.value}{node.operand.gen.jac}")
        elif node.op.value == "(":
            self.emit(node, f"({node.operand.gen.jac})")
        elif node.op.value == "not":
            self.emit(node, f"not {node.operand.gen.jac}")
        elif node.op.name in [Tok.PIPE_FWD, Tok.KW_SPAWN, Tok.A_PIPE_FWD]:
            self.emit(node, f"{node.op.value} {node.operand.gen.jac}")
        else:
            self.error(f"Unary operator {node.op.value} not supported in bootstrap Jac")

    def exit_raise_stmt(self, node: ast.RaiseStmt) -> None:
        """Sub objects.

        cause: Optional[ExprType],
        """
        if node.cause:
            node.gen.jac = f"raise {node.cause.gen.jac};"
        else:
            node.gen.jac = "raise;"

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
                f"[{node.start.gen.jac if node.start else ''}:"
                f"{node.stop.gen.jac if node.stop else ''}]",
            )
        elif node.start:
            self.emit(node, f"[{node.start.gen.jac}]")
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
                f"[{node.values.gen.jac}]",
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
                f"{{{node.values.gen.jac}}}",
            )

    def exit_dict_val(self, node: ast.DictVal) -> None:
        """Sub objects.

        kv_pairs: list["KVPair"],
        """
        self.emit(
            node,
            f"{{{', '.join([kv_pair.gen.jac for kv_pair in node.kv_pairs])}}}",
        )

    def exit_inner_compr(self, node: ast.InnerCompr) -> None:
        """Sub objects.

        is_async: bool,
        target: ExprType,
        collection: ExprType,
        conditional: Optional[ExprType],
        """
        partial = (
            f"{'async' if node.is_async else ''} for {node.target.gen.jac} in "
            f"{node.collection.gen.jac}"
        )
        if node.conditional:
            partial += f" if {node.conditional.gen.jac}"
        self.emit(node, f"({partial})")

    def exit_list_compr(self, node: ast.ListCompr) -> None:
        """Sub objects.

        out_expr: ExprType,
        compr: InnerCompr,
        """
        self.emit(node, f"[{node.out_expr.gen.jac} {node.compr.gen.jac}]")

    def exit_gen_compr(self, node: ast.GenCompr) -> None:
        """Sub objects.

        out_expr: ExprType,
        compr: InnerCompr,
        """
        self.emit(node, f"({node.out_expr.gen.jac} {node.compr.gen.jac},)")

    def exit_set_compr(self, node: ast.SetCompr) -> None:
        """Sub objects.

        out_expr: ExprType,
        compr: InnerCompr,
        """
        self.emit(node, f"{{{node.out_expr.gen.jac} {node.compr.gen.jac}}}")

    def exit_dict_compr(self, node: ast.DictCompr) -> None:
        """Sub objects.

        kv_pair: KVPair,
        compr: InnerCompr,
        """
        self.emit(node, f"{{{node.kv_pair.gen.jac} {node.compr.gen.jac}}}")

    def exit_k_v_pair(self, node: ast.KVPair) -> None:
        """Sub objects.

        key: ExprType,
        value: ExprType,
        """
        self.emit(node, f"{node.key.gen.jac}: {node.value.gen.jac}")

    def exit_k_w_pair(self, node: ast.KWPair) -> None:
        """Sub objects.

        key: ExprType,
        value: ExprType,
        """
        self.emit(node, f"{node.key.gen.jac}={node.value.gen.jac}")

    def exit_disconnect_op(self, node: ast.DisconnectOp) -> None:
        """Sub objects.

        filter_cond: Optional[ExprType],
        edge_dir: EdgeDir,
        """
        for i in node.kid:
            self.emit(node, i.gen.jac)

    def exit_connect_op(self, node: ast.ConnectOp) -> None:
        """Sub objects.

        spawn: Optional[ExprType],
        edge_dir: EdgeDir,
        """
        for i in node.kid:
            self.emit(node, i.gen.jac)

    def exit_filter_compr(self, node: ast.FilterCompr) -> None:
        """Sub objects.

        compares: list[BinaryExpr],
        """
        self.ds_feature_warn()

    def exit_assign_compr(self, node: ast.AssignCompr) -> None:
        """Sub objects.

        compares: list[BinaryExpr],
        """
        self.ds_feature_warn()

    def exit_await_expr(self, node: ast.AwaitExpr) -> None:
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

        vis_type: Optional[SubTag[SubNodeList[Name]]],
        target: ExprType,
        else_body: Optional[ElseStmt],
        from_walker: bool = False,
        """
        for i in node.kid:
            self.emit(node, i.gen.jac)
        self.emit_ln(node, "")

    def exit_ignore_stmt(self, node: ast.IgnoreStmt) -> None:
        """Sub objects.

        target: ExprType,
        """
        self.ds_feature_warn()

    def exit_return_stmt(self, node: ast.ReturnStmt) -> None:
        """Sub objects.

        expr: Optional[ExprType],
        """
        if node.expr:
            self.emit_ln(node, f"return {node.expr.gen.jac};")
        else:
            self.emit_ln(node, "return;")

    def exit_assert_stmt(self, node: ast.AssertStmt) -> None:
        """Sub objects.

        condition: ExprType,
        error_msg: Optional[ExprType],
        """
        comment_str = ""
        (
            inline_comments,
            _,
        ) = self.emit_comments_for_line(node.loc.first_line)
        if inline_comments:
            comment_str = " ; ".join(
                comment_value for _, comment_value in inline_comments
            )
        if node.error_msg:
            self.emit(
                node,
                f"assert {node.condition.gen.jac}, {node.error_msg.gen.jac}",  # noqa
            )
        else:
            self.emit(node, f"assert {node.condition.gen.jac}")

        if isinstance(node.kid[-1], ast.Token) and node.kid[-1].name == "SEMI":
            self.emit_ln(node, node.kid[-1].value + " " + comment_str)
            self.processed_comments.add(comment_str)

    def exit_ctrl_stmt(self, node: ast.CtrlStmt) -> None:
        """Sub objects.

        ctrl: Token,
        """
        comment_str = ""
        (
            inline_comments,
            next_line_standalone_comments,
        ) = self.emit_comments_for_line(node.loc.first_line)
        if inline_comments:
            comment_str = " ; ".join(
                comment_value for _, comment_value in inline_comments
            )

        if node.ctrl.name == Tok.KW_SKIP:
            self.ds_feature_warn()
        else:
            self.emit(node, node.ctrl.value)
        if isinstance(node.kid[-1], ast.Token) and node.kid[-1].name == "SEMI":
            self.emit_ln(node, node.kid[-1].value + " " + comment_str)
            self.processed_comments.add(comment_str)

    def exit_delete_stmt(self, node: ast.DeleteStmt) -> None:
        """Sub objects.

        target: ExprType,
        """
        comment_str = ""
        (
            inline_comments,
            _,
        ) = self.emit_comments_for_line(node.loc.first_line)
        if inline_comments:
            comment_str = " ; ".join(
                comment_value for _, comment_value in inline_comments
            )
        self.emit(node, f"del {node.target.gen.jac}")
        if isinstance(node.kid[-1], ast.Token) and node.kid[-1].name == "SEMI":
            self.emit_ln(node, node.kid[-1].value + " " + comment_str)
            self.processed_comments.add(comment_str)

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
            self.emit(node, node.expr.gen.jac + " as " + node.alias.value)
        else:
            self.emit(node, node.expr.gen.jac)

    def exit_in_for_stmt(self, node: ast.InForStmt) -> None:
        """Sub objects.

        target: ExprType,
        collection: ExprType,
        body: SubNodeList[CodeBlockStmt],
        """
        comment_str = ""
        (
            inline_comments,
            _,
        ) = self.emit_comments_for_line(node.loc.first_line)
        if inline_comments:
            comment_str = " ; ".join(
                comment_value for _, comment_value in inline_comments
            )
        names = node.target.gen.jac
        if comment_str not in self.processed_comments and comment_str != "":
            self.emit(
                node,
                f"for {names} in {node.collection.gen.jac}  {comment_str}",
            )
            self.processed_comments.add(comment_str)
        else:
            self.emit(node, f"for {names} in {node.collection.gen.jac} ")
        self.emit(node, node.body.gen.jac)

    def exit_test(self, node: ast.Test) -> None:
        """Sub objects.

        name: Optional[Name],
        doc: Optional[Token],
        body: CodeBlock,
        """
        test_name = node.name.value
        if test_name.startswith("test", 0, 4):
            test_name = ""
        if node.doc:
            self.emit_ln(node, node.doc.gen.jac)
        if test_name:
            self.emit(node, f"test {test_name}")
        else:
            self.emit(node, "test")
        self.emit(node, f"{node.body.gen.jac}")

    def exit_py_inline_code(self, node: ast.PyInlineCode) -> None:
        """Sub objects.

        code: Token,
        """
        self.emit_ln(node, node.code.value)

    def exit_arch_ref_chain(self, node: ast.ArchRefChain) -> None:
        """Sub objects.

        archs: list[ArchRef],
        """
        self.emit(node, ".".join([i.gen.jac for i in node.archs]))

    def exit_typed_ctx_block(self, node: ast.TypedCtxBlock) -> None:
        """Sub objects.

        type_ctx: TypeList,
        body: CodeBlock,
        """
        self.ds_feature_warn()

    def exit_match_stmt(self, node: ast.MatchStmt) -> None:
        """Sub objects.

        target: ExprType
        cases: list[MatchCase],
        """
        self.emit_ln(node, f"match {node.target.gen.jac} {{")
        self.indent_level += 1
        for case in node.cases:
            self.emit_ln(node, case.gen.jac)
        self.indent_level -= 1
        self.emit_ln(node, "}")

    def exit_match_case(self, node: ast.MatchCase) -> None:
        """Sub objects.

        pattern: ExprType,
        guard: Optional[ExprType],
        body: SubNodeList[CodeBlockStmt],
        """
        if node.guard:
            self.emit_ln(
                node,
                f"case {node.pattern.gen.jac} if {node.guard.gen.jac}:",  # noqa
            )
        else:
            self.emit(node, f"case {node.pattern.gen.jac}:")
        self.indent_level += 1
        self.nl_sep_node_list(node.body)
        self.emit_ln(node, node.body.gen.jac)
        self.indent_level -= 1

    def exit_match_or(self, node: ast.MatchOr) -> None:
        """Sub objects.

        list[MatchPattern],
        """
        self.emit(node, " | ".join([i.gen.jac for i in node.patterns]))

    def exit_match_as(self, node: ast.MatchAs) -> None:
        """Sub objects.

        name: NameType,
        pattern: MatchPattern,
        """
        if node.pattern:
            self.emit(node, f"{node.name.gen.jac} as {node.pattern.gen.jac}")
        else:
            self.emit(node, f"{node.name.gen.jac}")

    def exit_match_wild(self, node: ast.MatchWild) -> None:
        """Sub objects."""
        self.emit(node, "_")

    def exit_match_value(self, node: ast.MatchValue) -> None:
        """Sub objects.

        value: ExprType,
        """
        self.emit(node, node.value.gen.jac)

    def exit_match_singleton(self, node: ast.MatchSingleton) -> None:
        """Sub objects.

        value: Bool | Null,
        """
        self.emit(node, node.value.gen.jac)

    def exit_match_sequence(self, node: ast.MatchSequence) -> None:
        """Sub objects.

        values: list[MatchPattern],
        """
        self.emit(node, f"[{', '.join([i.gen.jac for i in node.values])}]")

    def exit_match_mapping(self, node: ast.MatchMapping) -> None:
        """Sub objects.

        values: list[MatchKVPair | MatchStar],
        """
        self.emit(node, f"{{{', '.join([i.gen.jac for i in node.values])}}}")

    def exit_match_k_v_pair(self, node: ast.MatchKVPair) -> None:
        """Sub objects.

        key: MatchPattern | NameType,
        value: MatchPattern,
        """
        self.emit(node, f"{node.key.gen.jac}: {node.value.gen.jac}")

    def exit_match_star(self, node: ast.MatchStar) -> None:
        """Sub objects.

        name: NameType,
        is_list: bool,
        """
        self.emit(node, f"{'*' if node.is_list else '**'}{node.name.gen.jac}")

    def exit_match_arch(self, node: ast.MatchArch) -> None:
        """Sub objects.

        name: NameType,
        arg_patterns: Optional[SubNodeList[MatchPattern]],
        kw_patterns: Optional[SubNodeList[MatchKVPair]],
        """
        self.emit(node, node.name.gen.jac)
        params = "("
        if node.arg_patterns:
            self.comma_sep_node_list(node.arg_patterns)
            params += node.arg_patterns.gen.jac
        if node.kw_patterns:
            self.comma_sep_node_list(node.kw_patterns)
            params += node.kw_patterns.gen.jac
        params += ")"
        self.emit(node, params)

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
        self.emit(node, node.value)

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
        self.emit(node, node.value)

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
        self.emit(node, node.value)

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
        self.emit(node, node.value)

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

    def exit_null(self, node: ast.Null) -> None:
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

    def exit_semi(self, node: ast.Semi) -> None:
        """Sub objects."""
        self.emit(node, node.value)
