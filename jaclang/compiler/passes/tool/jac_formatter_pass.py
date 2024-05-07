"""JacFormatPass for Jaseci Ast.

This is a pass for formatting Jac code.
"""

import re
from typing import Optional

import jaclang.compiler.absyntree as ast
from jaclang.compiler.absyntree import AstNode
from jaclang.compiler.constant import Tokens as Tok
from jaclang.compiler.passes import Pass


class JacFormatPass(Pass):
    """JacFormat Pass format Jac code."""

    def before_pass(self) -> None:
        """Initialize pass."""
        self.comments: list[ast.CommentToken] = []
        self.indent_size = 4
        self.indent_level = 0
        self.MAX_LINE_LENGTH = 44

    def enter_node(self, node: ast.AstNode) -> None:
        """Enter node."""
        node.gen.jac = ""
        super().enter_node(node)

    def indent_str(self) -> str:
        """Return string for indent."""
        return " " * self.indent_size * self.indent_level

    def emit(self, node: ast.AstNode, s: str, strip_mode: bool = True) -> None:
        """Emit code to node."""
        node.gen.jac += self.indent_str() + s.replace("\n", "\n" + self.indent_str())
        if "\n" in node.gen.jac:
            if strip_mode:
                node.gen.jac = node.gen.jac.rstrip(" ")
            else:
                node.gen.jac = node.gen.jac

    def emit_ln(self, node: ast.AstNode, s: str) -> None:
        """Emit code to node."""
        self.emit(node, s.strip().strip("\n"))
        self.emit(node, "\n")

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

    def enter_module(self, node: ast.Module) -> None:
        """Sub objects.

        name: str,
        source: JacSource,
        doc: Optional[String],
        body: Sequence[ElementStmt],
        is_imported: bool,
        """
        self.comments = node.source.comments

    def exit_module(self, node: ast.Module) -> None:
        """Sub objects.

        name: str,
        source: JacSource,
        doc: Optional[String],
        body: Sequence[ElementStmt],
        is_imported: bool,
        """
        prev_token = None
        for i in node.kid:
            if isinstance(i, ast.String):
                self.emit_ln(node, f" {i.gen.jac}")
                self.emit_ln(node, "")
            elif isinstance(i, ast.CommentToken):
                if i.is_inline:
                    self.emit(node, f" {i.gen.jac}")
                else:
                    if prev_token is not None:
                        self.emit_ln(node, "")
                    self.emit_ln(node, i.gen.jac)
            elif isinstance(i, ast.Token):
                self.emit(node, i.value.strip("") + " ")
            elif isinstance(i, ast.SubTag):
                for j in i.kid:
                    self.emit(node, j.gen.jac)
            prev_token = i
        last_element = None
        for counter, i in enumerate(node.body):
            counter += 1
            if isinstance(i, ast.Import):
                self.emit_ln(node, i.gen.jac)
            else:
                if isinstance(last_element, ast.Import):
                    self.emit_ln(node, "")
                self.emit_ln(node, i.gen.jac)
                if not node.gen.jac.endswith("\n"):
                    self.emit_ln(node, "")
                if counter <= len(node.body) - 1:
                    self.emit_ln(node, "")
            last_element = i

    def exit_global_vars(self, node: ast.GlobalVars) -> None:
        """Sub objects.

        access: Optional[SubTag[Token]],
        assignments: SubNodeList[Assignment],
        is_frozen: bool,
        doc: Optional[String] = None,
        """
        start = True
        prev_token = None
        for i in node.kid:
            if isinstance(i, ast.String):
                self.emit_ln(node, i.gen.jac)
            elif isinstance(i, ast.CommentToken):
                if i.is_inline:
                    self.emit(node, f" {i.gen.jac}")
                else:
                    if isinstance(prev_token, ast.Semi):
                        self.emit_ln(node, "")
                        self.emit_ln(node, "")
                    self.emit_ln(node, i.gen.jac)
            elif isinstance(i, ast.Semi):
                self.emit(node, f"{i.gen.jac}")
            else:
                if start:
                    self.emit(node, i.gen.jac)
                    start = False
                else:
                    self.emit(node, f" {i.gen.jac}")
            prev_token = i
        if isinstance(
            node.kid[-1], (ast.Semi, ast.CommentToken)
        ) and not node.gen.jac.endswith("\n"):
            self.emit_ln(node, "")

    def exit_module_code(self, node: ast.ModuleCode) -> None:
        """Sub objects.

        name: Optional[SubTag[Name]],
        body: SubNodeList[CodeBlockStmt],
        doc: Optional[Constant] = None,
        """
        start = True
        for i in node.kid:
            if isinstance(i, ast.String):
                self.emit_ln(node, i.gen.jac)
            elif isinstance(i, ast.Token):
                if start:
                    self.emit(node, i.gen.jac)
                    start = False
                else:
                    self.emit(node, f" {i.gen.jac}")
            elif isinstance(i, ast.SubTag):
                for j in i.kid:
                    self.emit(node, j.gen.jac)
        if node.body:
            self.emit(node, node.body.gen.jac)

    def exit_sub_node_list(self, node: ast.SubNodeList) -> None:
        """Sub objects.

        items: list[T],
        """
        prev_token = None
        for i, stmt in enumerate(node.kid):
            if isinstance(node.parent, (ast.EnumDef, ast.Enum)) and stmt.gen.jac == ",":
                self.indent_level -= 1
                self.emit_ln(node, f"{stmt.gen.jac}")
                self.indent_level += 1
                prev_token = stmt
                continue
            if (
                prev_token
                and prev_token.gen.jac.endswith("}")
                and not isinstance(prev_token, (ast.DictVal, ast.SetVal))
            ):
                self.indent_level -= 1
                self.emit_ln(node, "")
                self.indent_level += 1
            if isinstance(stmt, ast.Token):
                if (
                    isinstance(stmt, ast.Name)
                    and prev_token
                    and prev_token.gen.jac == "{"
                ):
                    self.emit_ln(node, "")
                    self.indent_level += 1
                if stmt.name == Tok.LBRACE:
                    next_kid = node.kid[i + 1]
                    if isinstance(next_kid, ast.CommentToken) and next_kid.is_inline:
                        self.emit(node, f" {stmt.value}")
                    else:
                        self.emit(node, f" {stmt.value}")
                elif stmt.name == Tok.RBRACE:
                    if self.indent_level > 0:
                        self.indent_level -= 1
                    if stmt.parent and stmt.parent.gen.jac.strip() == "{":
                        self.emit_ln(node, stmt.gen.jac.strip())
                    elif (
                        stmt.parent
                        and stmt.parent.parent
                        and isinstance(
                            stmt.parent.parent,
                            (ast.ElseIf, ast.IfStmt, ast.IterForStmt, ast.TryStmt),
                        )
                    ):
                        self.emit(node, f"{stmt.value}")
                    else:
                        next_kid = (
                            node.kid[i + 1]
                            if i < (len(node.kid) - 1)
                            else ast.EmptyToken()
                        )
                        if (
                            isinstance(next_kid, ast.CommentToken)
                            and next_kid.is_inline
                        ):
                            self.emit(node, f" {stmt.value}")
                        elif not (node.gen.jac).endswith("\n"):
                            self.indent_level -= 1
                            self.emit_ln(node, "")
                            self.indent_level += 1
                            self.emit(node, f"{stmt.value}")
                        else:
                            self.emit(node, f"{stmt.value}")
                elif isinstance(stmt, ast.CommentToken):
                    if stmt.is_inline:
                        if isinstance(prev_token, ast.Semi) or (
                            isinstance(prev_token, ast.Token)
                            and prev_token.name
                            in [
                                Tok.LBRACE,
                                Tok.RBRACE,
                            ]
                        ):
                            self.indent_level -= 1
                            self.emit(node, f" {stmt.gen.jac}")
                            self.emit_ln(node, "")
                            self.indent_level += 1
                        else:
                            self.emit(node, f" {stmt.gen.jac}")
                        self.indent_level -= 1
                        self.emit_ln(node, "")
                        self.indent_level += 1
                    else:
                        if not node.gen.jac.endswith("\n"):
                            self.indent_level -= 1
                            self.emit_ln(node, "")
                            self.indent_level += 1
                        if prev_token and prev_token.gen.jac.strip() == "{":
                            self.indent_level += 1
                        if prev_token and isinstance(prev_token, ast.Ability):
                            self.emit(node, f"{stmt.gen.jac}")
                        else:
                            self.emit(node, f"{stmt.gen.jac}\n")
                elif stmt.gen.jac == ",":
                    self.emit(node, f"{stmt.value} ")
                elif stmt.value == "=":
                    self.emit(node, f" {stmt.value} ")
                else:
                    self.emit(node, f"{stmt.value}")
                    prev_token = stmt
                    continue
            elif isinstance(stmt, ast.Semi):
                self.emit(node, stmt.gen.jac)
            elif isinstance(prev_token, (ast.HasVar, ast.ArchHas)) and not isinstance(
                stmt, (ast.HasVar, ast.ArchHas)
            ):
                if not isinstance(prev_token.kid[-1], ast.CommentToken):
                    self.indent_level -= 1
                    self.emit_ln(node, "")
                    self.indent_level += 1
                self.emit(node, stmt.gen.jac)
            elif isinstance(prev_token, ast.Ability) and isinstance(stmt, ast.Ability):
                if not isinstance(prev_token.kid[-1], ast.CommentToken) and (
                    prev_token.body and stmt.body
                ):
                    self.indent_level -= 1
                    self.emit_ln(node, "")
                    self.indent_level += 1
                self.emit(node, stmt.gen.jac)
            else:
                if prev_token and prev_token.gen.jac.strip() == "{":
                    self.emit_ln(node, "")
                    self.indent_level += 1
                self.emit(node, stmt.gen.jac)
            prev_token = stmt

    def exit_sub_tag(self, node: ast.SubTag) -> None:
        """Sub objects.

        tag: T,
        """
        start = True
        for i in node.kid:
            if isinstance(i, ast.CommentToken):
                if i.is_inline:
                    self.emit(node, f" {i.gen.jac}")
                elif not node.gen.jac.endswith("\n"):
                    self.emit_ln(node, "")
                    self.emit_ln(node, i.gen.jac)
                else:
                    self.emit_ln(node, i.gen.jac)
            elif isinstance(i, ast.Semi):
                self.emit(node, i.gen.jac)
            elif i.gen.jac == ",":
                self.emit(node, f"{i.gen.jac} ")
            else:
                if start:
                    self.emit(node, i.gen.jac)
                    start = False
                else:
                    self.emit(node, f" {i.gen.jac}")
        if isinstance(node.kid[-1], ast.Semi) and not node.gen.jac.endswith("\n"):
            self.emit_ln(node, "")

    def exit_func_call(self, node: ast.FuncCall) -> None:
        """Sub objects.

        target: AtomType,
        params: Optional[ParamList],
        """
        prev_token: Optional[AstNode] = None
        line_break_needed = False
        indented = False
        test_str = ""
        for i in node.kid:
            if isinstance(i, ast.SubNodeList):
                if prev_token and prev_token.gen.jac.strip() == "(":
                    for j in i.kid:
                        test_str += f" {j.gen.jac}"
                    test_str += ");"
                    line_break_needed = self.is_line_break_needed(test_str, 60)
                if line_break_needed:
                    self.emit_ln(node, "")
                    self.indent_level += 1
                    indented = True
                for count, j in enumerate(i.kid):
                    if j.gen.jac == ",":
                        if i.kid[count + 1].gen.jac.startswith("#"):
                            self.indent_level -= 1
                            self.emit(node, f"{j.gen.jac} ")
                            self.indent_level += 1
                        else:
                            if line_break_needed:
                                self.indent_level -= 1
                                self.emit_ln(node, f" {j.gen.jac}")
                                self.indent_level += 1
                            else:
                                self.emit(node, f"{j.gen.jac} ")
                    elif isinstance(j, ast.CommentToken):
                        if line_break_needed:
                            self.indent_level -= 1
                            self.emit(node, " ")
                            self.emit_ln(node, j.gen.jac)
                            self.indent_level += 1
                        else:
                            self.emit(node, f"{j.gen.jac} ")
                    else:
                        self.emit(node, j.gen.jac)
                if indented:
                    self.indent_level -= 1
                prev_token = i
                continue
            if isinstance(i, ast.CommentToken):
                if i.is_inline:
                    self.emit(node, f" {i.gen.jac}")
                else:
                    self.emit_ln(node, "")
                    self.emit_ln(node, i.gen.jac)
            if isinstance(i, ast.Token) and i.name == Tok.KW_BY:
                self.emit(node, f"{i.gen.jac} ")
            else:
                if (
                    line_break_needed
                    and prev_token
                    and isinstance(prev_token, ast.SubNodeList)
                ):
                    self.indent_level -= 1
                    self.emit_ln(node, "")
                    self.indent_level += 1
                self.emit(node, i.gen.jac)
            prev_token = i
            test_str += i.gen.jac
        if isinstance(node.kid[-1], (ast.Semi, ast.CommentToken)):
            self.emit_ln(node, "")

    def exit_multi_string(self, node: ast.MultiString) -> None:
        """Sub objects.

        strings: list[Token],
        """
        if len(node.strings) > 1:
            self.emit_ln(node, node.strings[0].gen.jac)
            self.indent_level += 1
            for string in range(1, len(node.strings) - 1):
                self.emit(node, f"{node.strings[string].gen.jac}\n")
            self.emit(node, node.strings[-1].gen.jac)
            self.indent_level -= 1
        else:
            self.emit(node, node.strings[0].gen.jac)

    def exit_module_path(self, node: ast.ModulePath) -> None:
        """Sub objects.

        path: list[Token],
        alias: Optional[Name],
        """
        self.emit(node, node.path_str)
        if node.alias:
            self.emit(node, " as " + node.alias.gen.jac)

    def exit_tuple_val(self, node: ast.TupleVal) -> None:
        """Sub objects.

        first_expr: Optional["ExprType"],
        exprs: Optional[ExprList],
        assigns: Optional[AssignmentList],
        """
        for i in node.kid:
            if (i.gen.jac).endswith(","):
                self.indent_level -= 1
                self.emit_ln(node, "")
                self.indent_level += 1
            self.emit(node, i.gen.jac)

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
        start = True
        prev_token = None
        for i in node.kid:
            if isinstance(i, ast.String):
                self.emit_ln(node, i.gen.jac)
            elif isinstance(i, ast.CommentToken):
                if i.is_inline:
                    self.emit(node, i.gen.jac)
                    if isinstance(prev_token, ast.Semi):
                        self.emit_ln(node, "")
                elif not node.gen.jac.endswith("\n"):
                    self.indent_level -= 1
                    self.emit_ln(node, "")
                    self.indent_level += 1
                    self.emit_ln(node, i.gen.jac)
                else:
                    self.emit_ln(node, i.gen.jac)
            elif isinstance(prev_token, ast.ArchRefChain) and isinstance(
                i, ast.FuncSignature
            ):
                m = next((True for j in i.kid if isinstance(j, ast.SubNodeList)), False)
                if m:
                    self.indent_level -= 1
                    self.emit_ln(node, "")
                    self.indent_level += 1
                self.emit(node, f"{i.gen.jac}")
            elif isinstance(i, ast.Semi):
                self.emit(node, i.gen.jac)
            elif isinstance(i, ast.SubNodeList) and i.gen.jac.startswith("@"):
                self.emit_ln(node, i.gen.jac)
            else:
                if start:
                    self.emit(node, i.gen.jac)
                    start = False
                elif i.gen.jac.startswith(" ") or i.gen.jac.startswith("("):
                    self.emit(node, i.gen.jac)
                else:
                    self.emit(node, f" {i.gen.jac}")
            prev_token = i
        if isinstance(node.kid[-1], ast.Semi) and not node.gen.jac.endswith("\n"):
            self.emit_ln(node, "")

    def exit_event_signature(self, node: ast.EventSignature) -> None:
        """Sub objects.

        event: Token,
        arch_tag_info: Optional["TypeList | TypeSpec"],
        return_type: Optional["TypeSpec"],
        """
        start = True
        for i in node.kid:
            if isinstance(i, ast.CommentToken):
                if i.is_inline:
                    self.emit(node, f" {i.gen.jac}")
                else:
                    self.emit_ln(node, i.gen.jac)
            elif isinstance(i, ast.Semi):
                self.emit(node, i.gen.jac)
            else:
                if start:
                    self.emit(node, i.gen.jac)
                    start = False
                else:
                    self.emit(node, f" {i.gen.jac}")
        if isinstance(node.kid[-1], (ast.Semi, ast.CommentToken)):
            self.emit_ln(node, "")

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
        start = True
        for i in node.kid:
            if isinstance(i, ast.CommentToken):
                if i.is_inline:
                    self.emit(node, f" {i.gen.jac}")
                elif not node.gen.jac.endswith("\n"):
                    self.emit_ln(node, "")
                    self.emit_ln(node, i.gen.jac)
                else:
                    self.emit_ln(node, i.gen.jac)
            elif isinstance(i, ast.Semi):
                self.emit(node, i.gen.jac)
            elif i.gen.jac.startswith(":"):
                self.emit(node, re.sub(r"\s+", "", i.gen.jac.strip()))
            else:
                if start or i.gen.jac == ",":
                    self.emit(node, i.gen.jac)
                    start = False
                else:
                    self.emit(node, f" {i.gen.jac}")
        if isinstance(node.kid[-1], ast.Semi) and not node.gen.jac.endswith("\n"):
            self.emit_ln(node, "")

    def exit_arch_def(self, node: ast.ArchDef) -> None:
        """Sub objects.

        target: ArchRefChain,
        body: SubNodeList[ArchBlockStmt],
        doc: Optional[Constant] = None,
        decorators: Optional[SubNodeList[ExprType]] = None,
        """
        start = True
        for i in node.kid:
            if isinstance(i, ast.CommentToken):
                if i.is_inline:
                    self.emit(node, f" {i.gen.jac}")
                elif not node.gen.jac.endswith("\n"):
                    self.indent_level -= 1
                    self.emit_ln(node, "")
                    self.indent_level += 1
                    self.emit_ln(node, i.gen.jac)
                else:
                    self.emit_ln(node, i.gen.jac)
            elif isinstance(i, ast.Semi):
                self.emit(node, i.gen.jac)
            else:
                if start or i.gen.jac == "," or i.gen.jac.startswith(":"):
                    self.emit(node, i.gen.jac)
                    start = False
                else:
                    self.emit(node, f" {i.gen.jac}")
        if isinstance(node.kid[-1], ast.Semi) and not node.gen.jac.endswith("\n"):
            self.emit_ln(node, "")

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
        start = True
        prev_token = None

        for i in node.kid:
            if i.gen.jac == "can" and node.is_static:
                i.gen.jac = "static can"
            if not i.gen.jac or i.gen.jac == "static":
                continue
            if isinstance(i, ast.String):
                if prev_token and prev_token.gen.jac.strip() == "can":
                    self.emit(node, " ")
                self.emit_ln(node, i.gen.jac)
            elif isinstance(i, ast.CommentToken):
                if i.is_inline:
                    self.emit(node, i.gen.jac)
                    if isinstance(prev_token, ast.Semi):
                        self.indent_level -= 1
                        self.emit_ln(node, "")
                        self.indent_level += 1
                elif not node.gen.jac.endswith("\n"):
                    self.indent_level -= 1
                    self.emit_ln(node, "")
                    self.indent_level += 1
                    self.emit_ln(node, i.gen.jac)
                else:
                    self.emit_ln(node, i.gen.jac)
            elif isinstance(i, ast.Semi):
                self.emit(node, i.gen.jac)
            elif isinstance(i, ast.SubNodeList) and i.gen.jac.startswith("@"):
                self.emit_ln(node, i.gen.jac)
            else:
                if start:
                    self.emit(node, i.gen.jac)
                    start = False
                elif i.gen.jac[0] in [" ", "("]:
                    self.emit(node, i.gen.jac)
                else:
                    if prev_token and isinstance(prev_token, ast.String):
                        self.emit(node, i.gen.jac)
                    else:
                        self.emit(node, f" {i.gen.jac}")
            prev_token = i
        if isinstance(node.kid[-1], ast.Semi) and not node.gen.jac.endswith("\n"):
            self.emit_ln(node, "")

    def exit_func_signature(self, node: ast.FuncSignature) -> None:
        """Sub objects.

        params: Optional[SubNodeList[ParamVar]],
        return_type: Optional[SubNodeList[TypeSpec]],
        """
        prev_token = None
        for i in node.kid:
            if isinstance(i, ast.SubTag):
                for j in i.kid:
                    if (
                        prev_token
                        and isinstance(prev_token, ast.Token)
                        and prev_token.gen.jac == "("
                    ):
                        self.emit(node, f"{j.gen.jac}")
                    else:
                        self.emit(node, f" {j.gen.jac}")
            elif isinstance(i, ast.SubNodeList):
                for j in i.kid:
                    if j.gen.jac == ",":
                        self.emit(node, f"{j.gen.jac.strip()} ")
                    else:
                        self.emit(node, f"{j.gen.jac.strip()}")
            elif isinstance(i, ast.Token) and i.gen.jac == ":":
                self.emit(node, f"{i.gen.jac} ")
            else:
                if i.gen.jac == "->":
                    self.emit(node, f" {i.gen.jac} ")
                else:
                    self.emit(node, i.gen.jac)
            prev_token = i

    def exit_arch_has(self, node: ast.ArchHas) -> None:
        """Sub objects.

        doc: Optional[Token],
        is_static: bool,
        access: Optional[Token],
        vars: "HasVarList",
        is_frozen: bool,
        """
        indented = False
        indent_val = 1
        for i in node.kid:
            if isinstance(i, ast.CommentToken):
                if i.is_inline:
                    self.emit(node, f" {i.gen.jac}")
                    self.emit_ln(node, "")
                elif not node.gen.jac.endswith("\n"):
                    self.emit(node, "\n")
                    self.emit_ln(node, i.gen.jac)
                else:
                    self.emit_ln(node, i.gen.jac)
            elif isinstance(i, ast.Semi):
                self.emit(node, i.gen.jac.strip())
            elif isinstance(i, ast.SubNodeList):
                for j in i.kid:
                    if j.gen.jac == ",":
                        if not indented:
                            self.emit_ln(node, j.gen.jac.strip())
                            self.indent_level += indent_val
                            indented = True
                        else:
                            self.indent_level -= indent_val
                            self.emit_ln(node, j.gen.jac.strip())
                            self.indent_level += indent_val
                            indented = True
                    else:
                        self.emit(node, f"{j.gen.jac.strip()}")
                if indented:
                    self.indent_level -= indent_val
            else:
                self.emit(node, f"{i.gen.jac} ")
                if i.gen.jac == "static":
                    indent_val = indent_val * 3
        if isinstance(node.kid[-1], ast.Semi) and not node.gen.jac.endswith("\n"):
            self.emit_ln(node, "")

    def exit_arch_ref(self, node: ast.ArchRef) -> None:
        """Sub objects.

        archs: list[ArchRef],
        """
        for i in node.kid:
            if isinstance(i, ast.CommentToken):
                if i.is_inline:
                    self.emit(node, f" {i.gen.jac}")
                elif not node.gen.jac.endswith("\n"):
                    self.indent_level -= 1
                    self.emit_ln(node, "")
                    self.indent_level += 1
                    self.emit_ln(node, i.gen.jac)
                else:
                    self.emit_ln(node, i.gen.jac)
            elif isinstance(i, ast.Semi):
                self.emit(node, i.gen.jac.strip())
            elif i.gen.jac == ",":
                self.emit(node, f"{i.gen.jac} ")
            else:
                self.emit(node, i.gen.jac)
        if isinstance(node.kid[-1], ast.Semi) and not node.gen.jac.endswith("\n"):
            self.emit_ln(node, "")

    def exit_param_var(self, node: ast.ParamVar) -> None:
        """Sub objects.

        name: Name,
        unpack: Optional[Token],
        type_tag: SubTag[Expr],
        value: Optional[Expr],
        """
        for i in node.kid:
            if isinstance(i, ast.SubTag):
                for j in i.kid:
                    (
                        self.emit(node, j.gen.jac)
                        if not j.gen.jac.startswith(":")
                        else self.emit(node, f"{j.gen.jac} ")
                    )
            elif isinstance(i, ast.Token) and i.gen.jac.startswith(":"):
                self.emit(node, f"{i.gen.jac} ")
            else:
                self.emit(node, i.gen.jac)

    def exit_enum(self, node: ast.Enum) -> None:
        """Sub objects.

        name: Name,
        doc: Optional[Token],
        decorators: Optional[Decorators],
        access: Optional[Token],
        base_classes: BaseClasses,
        body: Optional[EnumBlock],
        """
        start = True
        prev_token = None
        for i in node.kid:
            if isinstance(i, ast.String):
                if prev_token and prev_token.gen.jac.strip() == "enum":
                    self.emit(node, " ")
                self.emit_ln(node, i.gen.jac)
            elif isinstance(i, ast.CommentToken):
                if i.is_inline:
                    self.emit(node, f" {i.gen.jac}")
                else:
                    self.emit_ln(node, i.gen.jac)
            elif isinstance(i, ast.Semi):
                self.emit(node, i.gen.jac)
            elif isinstance(i, ast.SubNodeList) and i.gen.jac.startswith("@"):
                self.emit_ln(node, i.gen.jac)
            elif isinstance(i, ast.Token) and i.gen.jac == ":":
                self.emit(node, f"{i.gen.jac} ")
            else:
                if start or (prev_token and isinstance(prev_token, ast.String)):
                    self.emit(node, i.gen.jac)
                    start = False
                else:
                    self.emit(node, f" {i.gen.jac}")
            prev_token = i
        if isinstance(
            node.kid[-1], (ast.Semi, ast.CommentToken)
        ) and not node.gen.jac.endswith("\n"):
            self.emit_ln(node, "")

    def exit_enum_def(self, node: ast.EnumDef) -> None:
        """Sub objects.

        doc: Optional[Token],
        mod: Optional[DottedNameList],
        body: EnumBlock,
        """
        start = True
        for i in node.kid:
            if isinstance(i, ast.String):
                self.emit_ln(node, i.gen.jac)
            elif isinstance(i, ast.CommentToken):
                if i.is_inline:
                    self.emit(node, f" {i.gen.jac}")
                else:
                    self.emit_ln(node, i.gen.jac)
            elif isinstance(i, (ast.Semi, ast.ArchRefChain)):
                self.emit(node, i.gen.jac)
            elif isinstance(i, ast.SubNodeList) and i.gen.jac.startswith("@"):
                self.emit_ln(node, i.gen.jac)
            else:
                if start:
                    self.emit(node, i.gen.jac)
                    start = False
                else:
                    self.emit(node, f" {i.gen.jac}")
        if isinstance(
            node.kid[-1], (ast.Semi, ast.CommentToken)
        ) and not node.gen.jac.endswith("\n"):
            self.emit_ln(node, "")

    def exit_atom_trailer(self, node: ast.AtomTrailer) -> None:
        """Sub objects.

        target: AtomType,
        right: IndexSlice | ArchRefType | Token,
        null_ok: bool,
        """
        for i in node.kid:
            self.emit(node, i.gen.jac)

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
        if not node.with_from and node.expr:
            self.emit(node, f"yield {node.expr.gen.jac}")
        elif node.expr:
            self.emit(node, f"yield from {node.expr.gen.jac}")
        else:
            self.emit(node, "yield")
        if isinstance(node.kid[-1], ast.Token) and node.kid[-1].name == "SEMI":
            self.emit_ln(node, node.kid[-1].value + " ")

    def is_line_break_needed(self, content: str, max_line_length: int = 0) -> bool:
        """Check if the length of the current generated code exceeds the max line length."""
        if max_line_length == 0:
            max_line_length = self.MAX_LINE_LENGTH
        return len(content) > max_line_length

    def exit_binary_expr(self, node: ast.BinaryExpr) -> None:
        """Sub objects.

        left: ExprType,
        right: ExprType,
        op: Token | DisconnectOp | ConnectOp,
        """
        if isinstance(node.op, (ast.DisconnectOp, ast.ConnectOp)):
            self.emit(
                node,
                f"{node.left.gen.jac} {node.op.gen.jac} {node.right.gen.jac}",  # noqa
            )
        elif isinstance(node.op, ast.Token):
            if (
                node.op.value
                in [
                    *["+", "-", "*", "/", "%", "**"],
                    *["+=", "-=", "*=", "/=", "%=", "**="],
                    *[">>", "<<", ">>=", "<<="],
                    *["//=", "&=", "|=", "^=", "~="],
                    *["//", "&", "|", "^"],
                    *[">", "<", ">=", "<=", "==", "!=", ":="],
                    *["and", "or", "in", "not in", "is", "is not"],
                ]
                or node.op.name
                in [
                    Tok.PIPE_BKWD,
                    Tok.A_PIPE_BKWD,
                    Tok.PIPE_FWD,
                    Tok.KW_SPAWN,
                    Tok.A_PIPE_FWD,
                    Tok.ELVIS_OP,
                ]
                or (
                    node.op.name == Tok.PIPE_FWD
                    and isinstance(node.right, ast.TupleVal)
                )
            ):

                self.emit(
                    node,
                    f"{node.left.gen.jac} {node.op.value} {node.right.gen.jac}",
                )
            else:
                self.error(
                    f"Binary operator {node.op.value} not supported in bootstrap Jac"
                )
        if isinstance(
            node.kid[-1], (ast.Semi, ast.CommentToken)
        ) and not node.gen.jac.endswith("\n"):
            self.emit_ln(node, node.kid[-1].value)

    def exit_compare_expr(self, node: ast.CompareExpr) -> None:
        """Sub objects.

        left: Expr,
        rights: list[Expr],
        ops: list[Token],
        """
        self.emit(node, f"{node.left.gen.jac} ")
        for i in range(len(node.rights)):
            self.emit(node, f"{node.ops[i].value} {node.rights[i].gen.jac}")
        if isinstance(
            node.kid[-1], (ast.Semi, ast.CommentToken)
        ) and not node.gen.jac.endswith("\n"):
            self.emit_ln(node, node.kid[-1].value)

    def exit_has_var(self, node: ast.HasVar) -> None:
        """Sub objects.

        name: Token,
        type_tag: TypeSpec,
        value: Optional["ExprType"],
        """
        for i in node.kid:
            if isinstance(i, ast.SubTag):
                for j in i.kid:
                    (
                        self.emit(node, j.gen.jac)
                        if not j.gen.jac.startswith(":")
                        else self.emit(node, f"{j.gen.jac} ")
                    )
            else:
                self.emit(node, f" {i.gen.jac}")
        if isinstance(node.kid[-1], ast.CommentToken) and not node.gen.jac.endswith(
            "\n"
        ):
            self.emit_ln(node, "")

    def exit_if_stmt(self, node: ast.IfStmt) -> None:
        """Sub objects.

        condition: ExprType,
        body: CodeBlock,
        elseifs: Optional[ElseIfs],
        else_body: Optional[ElseStmt],
        """
        start = True
        for i in node.kid:
            if isinstance(i, ast.CommentToken):
                if i.is_inline:
                    self.emit(node, f" {i.gen.jac}")
                else:
                    self.emit_ln(node, i.gen.jac)
            elif isinstance(i, (ast.Semi, ast.SubNodeList)):
                self.emit(node, i.gen.jac)
            else:
                if start:
                    self.emit(node, i.gen.jac)
                    start = False
                else:
                    self.emit(node, f" {i.gen.jac}")
        if isinstance(
            node.kid[-1], (ast.Semi, ast.CommentToken)
        ) and not node.gen.jac.endswith("\n"):
            self.emit_ln(node, "")

    def exit_else_if(self, node: ast.ElseIf) -> None:
        """Sub objects.

        elseifs: list[IfStmt],
        """
        start = True
        for i in node.kid:
            if isinstance(i, ast.CommentToken):
                if i.is_inline:
                    self.emit(node, f" {i.gen.jac}")
                else:
                    self.emit_ln(node, i.gen.jac)
            elif isinstance(i, (ast.Semi, ast.SubNodeList)):
                self.emit(node, i.gen.jac)
            else:
                if start:
                    self.emit(node, i.gen.jac)
                    start = False
                else:
                    self.emit(node, f" {i.gen.jac}")

    def exit_disengage_stmt(self, node: ast.DisengageStmt) -> None:
        """Sub objects."""
        for i in node.kid:
            self.emit(node, i.gen.jac)
        self.indent_level -= 1
        self.emit_ln(node, "")
        self.indent_level += 1

    def exit_else_stmt(self, node: ast.ElseStmt) -> None:
        """Sub objects.

        body: CodeBlock,
        """
        start = True
        for i in node.kid:
            if isinstance(i, ast.CommentToken):
                if i.is_inline:
                    self.emit(node, f" {i.gen.jac}")
                else:
                    self.emit_ln(node, i.gen.jac)
            elif isinstance(i, (ast.Semi, ast.SubNodeList)):
                self.emit(node, i.gen.jac)
            else:
                if start:
                    self.emit(node, i.gen.jac)
                    start = False
                else:
                    self.emit(node, f" {i.gen.jac}")

    def exit_expr_stmt(self, node: ast.ExprStmt) -> None:
        """Sub objects.

        expr: ExprType,
        """
        start = True
        for i in node.kid:
            if isinstance(i, ast.CommentToken):
                if i.is_inline:
                    self.emit(node, f" {i.gen.jac}")
                else:
                    self.emit_ln(node, "")
                    self.emit_ln(node, "")
                    self.emit(node, i.gen.jac)
            elif isinstance(i, ast.Semi):
                self.emit(node, i.gen.jac)
            else:
                if start:
                    self.emit(node, i.gen.jac)
                    start = False
                else:
                    self.emit(node, f" {i.gen.jac}")
        if isinstance(
            node.kid[-1], (ast.Semi, ast.CommentToken)
        ):  # and not node.gen.jac.endswith("\n"):
            self.emit_ln(node, "")

    def exit_iter_for_stmt(self, node: ast.IterForStmt) -> None:
        """Sub objects.

        iter: Assignment,
        condition: ExprType,
        count_by: ExprType,
        body: CodeBlock,
        """
        if (
            node.parent
            and node.parent.parent
            and isinstance(node.parent.parent, (ast.Ability))
        ):
            self.emit_ln(node, "")

        start = True
        for i in node.kid:
            if i in [node.iter, node.condition, node.count_by]:
                i.gen.jac = i.gen.jac.replace(" ", "")
            if isinstance(i, ast.CommentToken):
                if i.is_inline:
                    self.emit(node, f" {i.gen.jac}")
                else:
                    self.emit_ln(node, i.gen.jac)
            elif isinstance(i, ast.Semi):
                self.emit(node, i.gen.jac)
            else:
                if start:
                    self.emit(node, i.gen.jac)
                    start = False
                else:
                    self.emit(node, f" {i.gen.jac}")
        if isinstance(node.kid[-1], (ast.Semi, ast.CommentToken)):
            self.emit_ln(node, "")

    def exit_try_stmt(self, node: ast.TryStmt) -> None:
        """Sub objects.

        body: CodeBlock,
        excepts: Optional[ExceptList],
        finally_body: Optional[FinallyStmt],
        """
        if (
            node.parent
            and node.parent.parent
            and isinstance(node.parent.parent, (ast.Ability))
        ):
            self.emit_ln(node, "")
        start = True
        for i in node.kid:
            if isinstance(i, ast.CommentToken):
                if i.is_inline:
                    self.emit(node, f" {i.gen.jac}")
                else:
                    if not node.gen.jac.endswith("\n"):
                        self.emit_ln(node, "")
                    self.emit_ln(node, "")
                    self.emit(node, i.gen.jac)
            elif isinstance(i, ast.Semi):
                self.emit(node, i.gen.jac)
            else:
                if isinstance(i, (ast.ElseStmt, ast.FinallyStmt)) or start:
                    self.emit(node, i.gen.jac)
                    start = False
                else:
                    self.emit(node, f" {i.gen.jac}")
        if isinstance(
            node.kid[-1], (ast.Semi, ast.CommentToken)
        ) and not node.gen.jac.endswith("\n"):
            self.emit_ln(node, "")

    def exit_except(self, node: ast.Except) -> None:
        """Sub objects.

        typ: ExprType,
        name: Optional[Token],
        body: CodeBlock,
        """
        if (
            node.parent
            and node.parent.parent
            and isinstance(node.parent.parent, (ast.Ability))
        ):
            self.emit_ln(node, "")
        start = True
        for i in node.kid:
            if isinstance(i, ast.CommentToken):
                if i.is_inline:
                    self.emit(node, f" {i.gen.jac}")
                else:
                    if not node.gen.jac.endswith("\n"):
                        self.emit_ln(node, "")
                    self.emit_ln(node, "")
                    self.emit(node, i.gen.jac)
            elif isinstance(i, ast.Semi):
                self.emit(node, i.gen.jac)
            else:
                if start or isinstance(i, ast.SubNodeList):
                    self.emit(node, i.gen.jac)
                    start = False
                else:
                    self.emit(node, f" {i.gen.jac}")
        if isinstance(
            node.kid[-1], (ast.Semi, ast.CommentToken)
        ) and not node.gen.jac.endswith("\n"):
            self.emit_ln(node, "")

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
        if (
            node.parent
            and node.parent.parent
            and isinstance(node.parent.parent, (ast.Ability))
        ):
            self.emit_ln(node, "")
        start = True
        for i in node.kid:
            if isinstance(i, ast.CommentToken):
                if i.is_inline:
                    self.emit(node, f" {i.gen.jac}")
                else:
                    if not node.gen.jac.endswith("\n"):
                        self.emit_ln(node, "")
                    self.emit_ln(node, "")
                    self.emit(node, i.gen.jac)
            elif isinstance(i, (ast.Semi, ast.SubNodeList)):
                self.emit(node, i.gen.jac)
            else:
                if start:
                    self.emit(node, i.gen.jac)
                    start = False
                else:
                    self.emit(node, f" {i.gen.jac}")
        if isinstance(
            node.kid[-1], (ast.Semi, ast.CommentToken)
        ) and not node.gen.jac.endswith("\n"):
            self.emit_ln(node, "")

    def exit_with_stmt(self, node: ast.WithStmt) -> None:
        """Sub objects.

        exprs: "ExprAsItemList",
        body: "CodeBlock",
        """
        self.comma_sep_node_list(node.exprs)
        self.emit(node, f"with {node.exprs.gen.jac}")
        if node.body.gen.jac:
            self.emit(node, node.body.gen.jac)

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
        for i in node.kid:
            if isinstance(i, ast.CommentToken):
                if i.is_inline:
                    self.emit(node, f" {i.gen.jac}")
                else:
                    self.emit_ln(node, i.gen.jac)
                    self.emit_ln(node, "")
            elif isinstance(i, ast.Semi):
                self.emit_ln(node, i.gen.jac)
            else:
                self.emit(node, f"{i.gen.jac} ")
        if isinstance(node.kid[-1], (ast.Semi, ast.CommentToken)):
            self.emit_ln(node, "")

    def exit_non_local_stmt(self, node: ast.GlobalStmt) -> None:
        """Sub objects.

        target: SubNodeList[NameType],
        """
        for i in node.kid:
            if isinstance(i, ast.CommentToken):
                if i.is_inline:
                    self.emit(node, f" {i.gen.jac}")
                else:
                    self.emit_ln(node, i.gen.jac)
                    self.emit_ln(node, "")
            elif isinstance(i, ast.Semi):
                self.emit_ln(node, i.gen.jac)
            else:
                self.emit(node, f"{i.gen.jac} ")
        if isinstance(node.kid[-1], (ast.Semi, ast.CommentToken)):
            self.emit_ln(node, "")

    def exit_assignment(self, node: ast.Assignment) -> None:
        """Sub objects.

        target: SubNodeList[AtomType],
        value: Optional[ExprType | YieldStmt],
        type_tag: Optional[SubTag[ExprType]],
        mutable: bool = True,
        aug_op: Optional[Token] = None
        """
        for i in node.kid:
            if isinstance(i, ast.CommentToken):
                if i.is_inline:
                    self.emit(node, i.gen.jac)
                else:
                    self.emit_ln(node, "")
                    self.emit_ln(node, "")
                    self.emit_ln(node, i.gen.jac)
            elif isinstance(i, ast.Token) and (
                i.name == Tok.KW_LET or i.gen.jac == ":"
            ):
                self.emit(node, f"{i.gen.jac} ")
            elif isinstance(i, ast.Token) and "=" in i.gen.jac:
                self.emit(node, f" {i.gen.jac} ")
            else:
                self.emit(node, i.gen.jac)
        if isinstance(
            node.kid[-1], (ast.Semi, ast.CommentToken)
        ) and not node.gen.jac.endswith("\n"):
            self.emit_ln(node, "")

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
        start = True
        prev_token = None
        for i in node.kid:
            if isinstance(i, ast.String):
                if prev_token and prev_token.gen.jac.strip() == "obj":
                    self.emit(node, " ")
                self.emit_ln(node, i.gen.jac)
            elif isinstance(i, ast.CommentToken):
                if i.is_inline:
                    self.emit(node, i.gen.jac)
                    if isinstance(prev_token, ast.Semi):
                        self.emit_ln(node, "")
                else:
                    self.emit_ln(node, i.gen.jac)
            elif isinstance(i, ast.Semi):
                self.emit(node, f"{i.gen.jac} ")
            elif isinstance(i, ast.SubNodeList) and i.gen.jac.startswith("@"):
                self.emit_ln(node, i.gen.jac)
            else:
                if start or (prev_token and isinstance(prev_token, ast.String)):
                    self.emit(node, i.gen.jac)
                    start = False
                elif i.gen.jac.startswith(" "):
                    self.emit(node, i.gen.jac)
                else:
                    self.emit(node, f" {i.gen.jac}")
            prev_token = i
        if isinstance(node.kid[-1], ast.Semi) and not node.gen.jac.endswith("\n"):
            self.emit_ln(node, "")

    def exit_f_string(self, node: ast.FString) -> None:
        """Sub objects.

        parts: list["Token | ExprType"],
        """
        self.emit(
            node, node.kid[0].value if isinstance(node.kid[0], ast.Token) else 'f"'
        )
        if node.parts:
            for part in node.parts.items:
                if isinstance(part, ast.String) and part.name in [
                    Tok.FSTR_PIECE,
                    Tok.FSTR_SQ_PIECE,
                    Tok.FSTR_BESC,
                ]:
                    self.emit(node, f"{part.gen.jac}")
                else:
                    self.emit(node, "{" + part.gen.jac + "}")
        self.emit(
            node, node.kid[-1].value if isinstance(node.kid[-1], ast.Token) else '"'
        )

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

    def exit_bool_expr(self, node: ast.BoolExpr) -> None:
        """Sub objects.

        op: Token,
        values: list[Expr],
        """
        end = node.values[-1]
        test_str = ""
        for i in node.values:
            test_str += f"{i.gen.jac}"
            if i != end:
                test_str += f" {node.op.value} "

        # Check if line break is needed
        if self.is_line_break_needed(test_str):
            for i in node.values:
                if i != end:
                    self.emit_ln(node, f"{i.gen.jac}")
                else:
                    self.emit(node, f"{i.gen.jac}")
                if i != end:
                    self.emit(
                        node,
                        " " * self.indent_size + f"{node.op.value} ",
                        strip_mode=False,
                    )
        else:
            self.emit(node, test_str)

    def exit_lambda_expr(self, node: ast.LambdaExpr) -> None:
        """Sub objects.

        signature: FuncSignature,
        body: Expr,
        """
        out = ""
        if node.signature and node.signature.params:
            self.comma_sep_node_list(node.signature.params)
            out += node.signature.params.gen.jac
        if node.signature and node.signature.return_type:
            out += f" -> {node.signature.return_type.gen.jac}"
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
        start = True
        for i in node.kid:
            if isinstance(i, ast.CommentToken):
                if i.is_inline:
                    self.emit(node, f" {i.gen.jac}")
                else:
                    self.emit_ln(node, i.gen.jac)
            elif isinstance(i, ast.Semi):
                self.emit(node, i.gen.jac)
            else:
                if start:
                    self.emit(node, i.gen.jac)
                    start = False
                else:
                    self.emit(node, f" {i.gen.jac}")
        if isinstance(node.kid[-1], (ast.Semi, ast.CommentToken)):
            self.emit_ln(node, "")

    def exit_edge_ref_trailer(self, node: ast.EdgeRefTrailer) -> None:
        """Sub objects.

        edge_ref: EdgeRef,
        """
        for i in node.kid:
            self.emit(node, i.gen.jac)

    def exit_edge_op_ref(self, node: ast.EdgeOpRef) -> None:
        """Sub objects.

        filter_cond: Optional[ExprType],
        edge_dir: EdgeDir,
        """
        for i in node.kid:
            self.emit(node, i.gen.jac)

    def exit_index_slice(self, node: ast.IndexSlice) -> None:
        """Sub objects.

        start: ExprType,
        stop: Optional[ExprType],
        """
        for i in node.kid:
            self.emit(node, i.gen.jac)

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
            self.emit(
                node,
                f"{{{node.values.gen.jac}}}",
            )

    def exit_dict_val(self, node: ast.DictVal) -> None:
        """Sub objects.

        kv_pairs: list["KVPair"],
        """
        start = True
        prev_token = None
        line_break_needed = False
        indented = False
        test_str = ""
        if node.kv_pairs:
            test_str = "{"
            for j in node.kv_pairs:
                test_str += f"{j.gen.jac}"
            test_str += "};"
        for i in node.kid:
            if isinstance(i, ast.CommentToken):
                if i.is_inline:
                    self.emit(node, f" {i.gen.jac}")
                else:
                    self.emit_ln(node, i.gen.jac)
            elif self.is_line_break_needed(test_str, 60) and i.gen.jac == "{":
                self.emit_ln(node, f"{i.gen.jac}")
                line_break_needed = True
            elif isinstance(prev_token, ast.Token) and prev_token.name == Tok.LBRACE:
                if line_break_needed and not indented:
                    self.indent_level += 1
                    indented = True
                self.emit(node, f"{i.gen.jac}")
            elif isinstance(i, ast.Semi) or i.gen.jac == ",":
                if line_break_needed and indented:
                    self.indent_level -= 1
                    self.emit_ln(node, f"{i.gen.jac}")
                    self.indent_level += 1
                else:
                    self.emit(node, f"{i.gen.jac}")
            else:
                if start or i.gen.jac == "}":
                    if line_break_needed:
                        self.indent_level -= 1
                        self.emit(node, f"\n{i.gen.jac}")
                        line_break_needed = False
                        indented = False
                    else:
                        self.emit(node, i.gen.jac)
                else:
                    if line_break_needed:
                        self.emit(node, f"{i.gen.jac}")
                    else:
                        self.emit(node, f" {i.gen.jac}")

            start = False
            prev_token = i
        if isinstance(node.kid[-1], (ast.Semi, ast.CommentToken)):
            self.emit_ln(node, "")

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
            partial += " if " + " if ".join(i.gen.jac for i in node.conditional)
        self.emit(node, f"{partial}")

    def exit_list_compr(self, node: ast.ListCompr) -> None:
        """Sub objects.

        out_expr: ExprType,
        compr: InnerCompr,
        """
        for i in node.kid:
            self.emit(node, i.gen.jac)

    def exit_gen_compr(self, node: ast.GenCompr) -> None:
        """Sub objects.

        out_expr: ExprType,
        compr: InnerCompr,
        """
        self.emit(
            node, f"({node.out_expr.gen.jac} {' '.join(i.gen.jac for i in node.compr)})"
        )

    def exit_set_compr(self, node: ast.SetCompr) -> None:
        """Sub objects.

        out_expr: ExprType,
        compr: InnerCompr,
        """
        self.emit(
            node,
            f"{{{node.out_expr.gen.jac} {' '.join(i.gen.jac for i in node.compr)}}}",
        )

    def exit_dict_compr(self, node: ast.DictCompr) -> None:
        """Sub objects.

        kv_pair: KVPair,
        compr: InnerCompr,
        """
        self.emit(
            node,
            f"{{{node.kv_pair.gen.jac} {' '.join(i.gen.jac for i in node.compr)}}}",
        )

    def exit_k_v_pair(self, node: ast.KVPair) -> None:
        """Sub objects.

        key: ExprType,
        value: ExprType,
        """
        for i in node.kid:
            if i.gen.jac == ":":
                self.emit(node, f"{i.gen.jac} ")
            else:
                self.emit(node, i.gen.jac)

    def exit_k_w_pair(self, node: ast.KWPair) -> None:
        """Sub objects.

        key: ExprType,
        value: ExprType,
        """
        if node.key:
            self.emit(node, f"{node.key.gen.jac}={node.value.gen.jac}")
        else:
            self.emit(node, f"**{node.value.gen.jac}")

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
        for i in node.kid:
            self.emit(node, i.gen.jac)

    def exit_assign_compr(self, node: ast.AssignCompr) -> None:
        """Sub objects.

        compares: list[BinaryExpr],
        """
        for i in node.kid:
            self.emit(node, i.gen.jac)

    def exit_await_expr(self, node: ast.AwaitExpr) -> None:
        """Sub objects.

        target: ExprType,
        """
        for i in node.kid:
            self.emit(node, i.gen.jac)

    def exit_revisit_stmt(self, node: ast.RevisitStmt) -> None:
        """Sub objects.

        hops: Optional[ExprType],
        else_body: Optional[ElseStmt],
        """
        for i in node.kid:
            self.emit(node, i.gen.jac)

    def exit_visit_stmt(self, node: ast.VisitStmt) -> None:
        """Sub objects.

        vis_type: Optional[SubTag[SubNodeList[Name]]],
        target: ExprType,
        else_body: Optional[ElseStmt],
        from_walker: bool = False,
        """
        for i in node.kid:
            if isinstance(
                i,
                (
                    ast.EdgeRefTrailer,
                    ast.AtomTrailer,
                    ast.ElseStmt,
                    ast.SpecialVarRef,
                    ast.ListCompr,
                ),
            ):
                self.emit(node, f" {i.gen.jac}")
            else:
                self.emit(node, i.gen.jac)
        self.emit_ln(node, "")

    def exit_ignore_stmt(self, node: ast.IgnoreStmt) -> None:
        """Sub objects.

        target: ExprType,
        """
        if node.target:
            self.emit_ln(node, f"ignore {node.target.gen.jac};")
        else:
            self.emit_ln(node, "ignore;")

    def exit_return_stmt(self, node: ast.ReturnStmt) -> None:
        """Sub objects.

        expr: Optional[ExprType],
        """
        start = True
        for i in node.kid:
            if isinstance(i, ast.CommentToken):
                if i.is_inline:
                    self.emit(node, f" {i.gen.jac}")
                else:
                    self.emit_ln(node, i.gen.jac)
            elif isinstance(i, ast.Semi):
                self.emit(node, i.gen.jac)
            else:
                if start:
                    self.emit(node, i.gen.jac)
                    start = False
                else:
                    self.emit(node, f" {i.gen.jac}")
        if isinstance(node.kid[-1], (ast.Semi, ast.CommentToken)):
            self.emit_ln(node, "")

    def exit_assert_stmt(self, node: ast.AssertStmt) -> None:
        """Sub objects.

        condition: ExprType,
        error_msg: Optional[ExprType],
        """
        start = True
        for i in node.kid:
            if isinstance(i, ast.CommentToken):
                if i.is_inline:
                    self.emit(node, f" {i.gen.jac}")
                else:
                    self.emit_ln(node, "")
                    self.emit_ln(node, "")
                    self.emit(node, i.gen.jac)
            elif isinstance(i, ast.Semi):
                self.emit(node, i.gen.jac)
            else:
                if start:
                    self.emit(node, i.gen.jac)
                    start = False
                else:
                    self.emit(node, f" {i.gen.jac}")
        if isinstance(node.kid[-1], (ast.Semi, ast.CommentToken)):
            self.emit_ln(node, "")

    def exit_ctrl_stmt(self, node: ast.CtrlStmt) -> None:
        """Sub objects.

        ctrl: Token,
        """
        start = True
        for i in node.kid:
            if isinstance(i, ast.CommentToken):
                if i.is_inline:
                    self.emit(node, f" {i.gen.jac}")
                else:
                    self.emit_ln(node, "")
                    self.emit_ln(node, "")
                    self.emit(node, i.gen.jac)
            elif isinstance(i, ast.Semi):
                self.emit(node, i.gen.jac)
            else:
                if start:
                    self.emit(node, i.gen.jac)
                    start = False
                else:
                    self.emit(node, f" {i.gen.jac}")
        if isinstance(node.kid[-1], (ast.Semi, ast.CommentToken)):
            self.emit_ln(node, "")

    def exit_delete_stmt(self, node: ast.DeleteStmt) -> None:
        """Sub objects.

        target: ExprType,
        """
        start = True
        for i in node.kid:
            if isinstance(i, ast.CommentToken):
                if i.is_inline:
                    self.emit(node, f" {i.gen.jac}")
                else:
                    if not node.gen.jac.endswith("\n"):
                        self.emit_ln(node, "")
                    self.emit_ln(node, "")
                    self.emit(node, i.gen.jac)
            elif isinstance(i, ast.Semi):
                self.emit(node, i.gen.jac)
            else:
                if start:
                    self.emit(node, i.gen.jac)
                    start = False
                else:
                    self.emit(node, f" {i.gen.jac}")
        if isinstance(node.kid[-1], (ast.Semi, ast.CommentToken)):
            self.emit_ln(node, "")

    def exit_report_stmt(self, node: ast.ReportStmt) -> None:
        """Sub objects.

        expr: ExprType,
        """
        start = True
        for i in node.kid:
            if isinstance(i, ast.CommentToken):
                if i.is_inline:
                    self.emit(node, f" {i.gen.jac}")
                else:
                    self.emit_ln(node, i.gen.jac)
            elif isinstance(i, ast.Semi):
                self.emit(node, i.gen.jac)
            else:
                if start:
                    self.emit(node, i.gen.jac)
                    start = False
                else:
                    self.emit(node, f" {i.gen.jac}")
        if isinstance(node.kid[-1], (ast.Semi, ast.CommentToken)):
            self.emit_ln(node, "")

    def exit_expr_as_item(self, node: ast.ExprAsItem) -> None:
        """Sub objects.

        expr: "ExprType",
        alias: Optional[Token],
        """
        if node.alias:
            self.emit(node, node.expr.gen.jac + " as " + node.alias.gen.jac)
        else:
            self.emit(node, node.expr.gen.jac)

    def exit_in_for_stmt(self, node: ast.InForStmt) -> None:
        """Sub objects.

        target: ExprType,
        collection: ExprType,
        body: SubNodeList[CodeBlockStmt],
        """
        if (
            node.parent
            and node.parent.parent
            and isinstance(node.parent.parent, (ast.Ability))
        ):
            self.indent_level -= 1
            self.emit_ln(node, "")
            self.indent_level += 1

        start = True
        for i in node.kid:
            if isinstance(i, ast.CommentToken):
                if i.is_inline:
                    self.emit(node, f" {i.gen.jac}")
                else:
                    self.emit_ln(node, i.gen.jac)
            elif isinstance(i, (ast.Semi, ast.SubNodeList)):
                self.emit(node, i.gen.jac)
            else:
                if start:
                    self.emit(node, i.gen.jac)
                    start = False
                else:
                    self.emit(node, f" {i.gen.jac}")
        if isinstance(node.kid[-1], (ast.Semi, ast.CommentToken)):
            self.emit_ln(node, "")

    def exit_test(self, node: ast.Test) -> None:
        """Sub objects.

        name: Optional[Name],
        doc: Optional[Token],
        body: CodeBlock,
        """
        start = True
        for i in node.kid:
            if isinstance(i, ast.CommentToken):
                if i.is_inline:
                    self.emit(node, f" {i.gen.jac}")
                else:
                    self.emit_ln(node, "")
                    self.emit_ln(node, i.gen.jac)
            elif isinstance(i, ast.Semi):
                self.emit(node, i.gen.jac)
            elif isinstance(i, ast.Name):
                if not i.value.startswith("test_t"):
                    self.emit(node, f" {i.value} ")
            else:
                if start:
                    self.emit(node, i.gen.jac)
                    start = False
                else:
                    self.emit(node, f" {i.gen.jac}")
        if isinstance(node.kid[-1], (ast.Semi, ast.CommentToken)):
            self.emit_ln(node, "")

    def exit_py_inline_code(self, node: ast.PyInlineCode) -> None:
        """Sub objects.

        code: Token,
        """
        self.emit_ln(node, "::py::")
        self.emit_ln(node, node.code.value)
        self.emit_ln(node, "::py::")

    def exit_arch_ref_chain(self, node: ast.ArchRefChain) -> None:
        """Sub objects.

        archs: list[ArchRef],
        """
        for i in node.kid:
            if isinstance(i, ast.CommentToken):
                if i.is_inline:
                    self.emit(node, f" {i.gen.jac}")
                elif not node.gen.jac.endswith("\n"):
                    self.emit_ln(node, "")
                    self.emit_ln(node, i.gen.jac)
                else:
                    self.emit_ln(node, i.gen.jac)
            elif isinstance(i, ast.Semi):
                self.emit(node, i.gen.jac)
            elif i.gen.jac == ",":
                self.emit(node, f"{i.gen.jac} ")
            else:
                self.emit(node, i.gen.jac)
        if isinstance(node.kid[-1], ast.Semi) and not node.gen.jac.endswith("\n"):
            self.emit_ln(node, "")

    def exit_typed_ctx_block(self, node: ast.TypedCtxBlock) -> None:
        """Sub objects.

        type_ctx: TypeList,
        body: CodeBlock,
        """

    def exit_match_stmt(self, node: ast.MatchStmt) -> None:
        """Sub objects.

        target: ExprType
        cases: list[MatchCase],
        """
        start = True
        for i in node.kid:
            if isinstance(i, ast.CommentToken):
                if i.is_inline:
                    self.emit(node, f" {i.gen.jac}")
                else:
                    self.emit_ln(node, "")
                    self.emit_ln(node, i.gen.jac)
            elif isinstance(i, ast.Semi):
                self.emit(node, i.gen.jac)
            elif isinstance(i, ast.Token):
                if i.name == Tok.LBRACE:
                    self.emit_ln(node, f" {i.value}")
                    self.indent_level += 1
                elif i.name == Tok.RBRACE:
                    self.indent_level -= 1
                    self.emit(node, f"{i.value}")
                else:
                    self.emit(node, f"{i.value} ")
            else:
                if start:
                    self.emit(node, i.gen.jac)
                    start = False
                else:
                    self.emit(node, f"{i.gen.jac}")
        if isinstance(node.kid[-1], (ast.Semi, ast.CommentToken)):
            self.emit_ln(node, "")

    def exit_match_case(self, node: ast.MatchCase) -> None:
        """Sub objects.

        pattern: ExprType,
        guard: Optional[ExprType],
        body: list[CodeBlockStmt],
        """
        start = True
        for i in node.kid:
            if isinstance(i, ast.CommentToken):
                if i.is_inline:
                    self.emit(node, f" {i.gen.jac}")
                else:
                    self.emit_ln(node, "")
                    self.emit_ln(node, i.gen.jac)
            elif isinstance(i, ast.Semi):
                self.emit(node, i.gen.jac)
            elif isinstance(i, ast.Token) and i.value == ":":
                self.emit_ln(node, i.gen.jac)
            elif isinstance(i, ast.CodeBlockStmt):
                self.indent_level += 1
                self.emit(node, i.gen.jac.strip())
                self.indent_level -= 1
                self.emit_ln(node, "")
            else:
                if start:
                    self.emit(node, i.gen.jac)
                    start = False
                else:
                    self.emit(node, f" {i.gen.jac}")
        if isinstance(node.kid[-1], (ast.Semi, ast.CommentToken)):
            self.emit_ln(node, "")

    def exit_match_or(self, node: ast.MatchOr) -> None:
        """Sub objects.

        list[MatchPattern],
        """
        start = True
        for i in node.kid:
            if isinstance(i, ast.CommentToken):
                if i.is_inline:
                    self.emit(node, f" {i.gen.jac}")
                else:
                    self.emit_ln(node, i.gen.jac)
            elif isinstance(i, ast.Semi):
                self.emit(node, i.gen.jac)
            else:
                if start:
                    self.emit(node, i.gen.jac)
                    start = False
                else:
                    self.emit(node, f" {i.gen.jac}")
        if isinstance(node.kid[-1], (ast.Semi, ast.CommentToken)):
            self.emit_ln(node, "")

    def exit_match_as(self, node: ast.MatchAs) -> None:
        """Sub objects.

        name: NameType,
        pattern: MatchPattern,
        """
        start = True
        for i in node.kid:
            if isinstance(i, ast.CommentToken):
                if i.is_inline:
                    self.emit(node, f" {i.gen.jac}")
                else:
                    self.emit_ln(node, "")
                    self.emit_ln(node, i.gen.jac)
            elif isinstance(i, ast.Semi):
                self.emit(node, i.gen.jac)
            else:
                if start:
                    self.emit(node, i.gen.jac)
                    start = False
                else:
                    self.emit(node, f" {i.gen.jac}")
        if isinstance(node.kid[-1], (ast.Semi, ast.CommentToken)):
            self.emit_ln(node, "")

    def exit_match_wild(self, node: ast.MatchWild) -> None:
        """Sub objects."""
        start = True
        for i in node.kid:
            if isinstance(i, ast.CommentToken):
                if i.is_inline:
                    self.emit(node, f" {i.gen.jac}")
                else:
                    self.emit_ln(node, "")
                    self.emit_ln(node, i.gen.jac)
            elif isinstance(i, ast.Semi):
                self.emit(node, i.gen.jac)
            else:
                if start:
                    self.emit(node, i.gen.jac)
                    start = False
                else:
                    self.emit(node, f" {i.gen.jac}")
        if isinstance(node.kid[-1], (ast.Semi, ast.CommentToken)):
            self.emit_ln(node, "")

    def exit_match_value(self, node: ast.MatchValue) -> None:
        """Sub objects.

        value: ExprType,
        """
        start = True
        for i in node.kid:
            if isinstance(i, ast.CommentToken):
                if i.is_inline:
                    self.emit(node, f" {i.gen.jac}")
                else:
                    self.emit_ln(node, "")
                    self.emit_ln(node, i.gen.jac)
            elif isinstance(i, ast.Semi):
                self.emit(node, i.gen.jac)
            else:
                if start:
                    self.emit(node, i.gen.jac)
                    start = False
                else:
                    self.emit(node, f" {i.gen.jac}")
        if isinstance(node.kid[-1], (ast.Semi, ast.CommentToken)):
            self.emit_ln(node, "")

    def exit_match_singleton(self, node: ast.MatchSingleton) -> None:
        """Sub objects.

        value: Bool | Null,
        """
        self.emit(node, node.value.gen.jac)

    def exit_match_sequence(self, node: ast.MatchSequence) -> None:
        """Sub objects.

        values: list[MatchPattern],
        """
        for i in node.kid:
            if isinstance(i, ast.CommentToken):
                if i.is_inline:
                    self.emit(node, f" {i.gen.jac}")
                else:
                    self.emit_ln(node, "")
                    self.emit_ln(node, i.gen.jac)
            elif isinstance(i, ast.Semi):
                self.emit(node, i.gen.jac)
            else:
                if i.gen.jac == ",":
                    self.emit(node, f"{i.gen.jac} ")
                else:
                    self.emit(node, i.gen.jac)
        if isinstance(node.kid[-1], (ast.Semi, ast.CommentToken)):
            self.emit_ln(node, "")

    def exit_match_mapping(self, node: ast.MatchMapping) -> None:
        """Sub objects.

        values: list[MatchKVPair | MatchStar],
        """
        for i in node.kid:
            if isinstance(i, ast.CommentToken):
                if i.is_inline:
                    self.emit(node, f" {i.gen.jac}")
                else:
                    self.emit_ln(node, "")
                    self.emit_ln(node, i.gen.jac)
            elif isinstance(i, ast.Semi):
                self.emit(node, i.gen.jac)
            else:
                if i.gen.jac == ",":
                    self.emit(node, f"{i.gen.jac} ")
                else:
                    self.emit(node, i.gen.jac)
        if isinstance(node.kid[-1], (ast.Semi, ast.CommentToken)):
            self.emit_ln(node, "")

    def exit_match_k_v_pair(self, node: ast.MatchKVPair) -> None:
        """Sub objects.

        key: MatchPattern | NameType,
        value: MatchPattern,
        """
        start = True
        for i in node.kid:
            if isinstance(i, ast.CommentToken):
                if i.is_inline:
                    self.emit(node, f" {i.gen.jac}")
                else:
                    self.emit_ln(node, "")
                    self.emit_ln(node, i.gen.jac)
            elif isinstance(i, ast.Semi):
                self.emit(node, i.gen.jac)
            else:
                if start:
                    self.emit(node, i.gen.jac)
                    start = False
                else:
                    self.emit(node, f" {i.gen.jac}")
        if isinstance(node.kid[-1], (ast.Semi, ast.CommentToken)):
            self.emit_ln(node, "")

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
        for i in node.kid:
            if isinstance(i, ast.CommentToken):
                if i.is_inline:
                    self.emit(node, f" {i.gen.jac}")
                else:
                    self.emit_ln(node, "")
                    self.emit_ln(node, i.gen.jac)
            elif isinstance(i, ast.Semi):
                self.emit(node, i.gen.jac)
            else:
                if i.gen.jac == ",":
                    self.emit(node, f"{i.gen.jac} ")
                else:
                    self.emit(node, i.gen.jac)
        if isinstance(node.kid[-1], (ast.Semi, ast.CommentToken)):
            self.emit_ln(node, "")

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
        is_kwesc: bool,
        """
        self.emit(node, f"<>{node.value}" if node.is_kwesc else node.value)

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
        # if string is in docstring format and spans multiple lines turn into the multiple single quoted strings
        if "\n" in node.value and node.parent and isinstance(node.parent, ast.Expr):
            string_type = node.value[0:3]
            pure_string = node.value[3:-3]
            lines = pure_string.split("\n")
            for line in lines[:-1]:
                self.emit_ln(node, f"{string_type}{line}\\n{string_type}")
            self.emit(node, f"{string_type}{lines[-1]}{string_type}")
            return
        if (
            node.value in ["{", "}"]
            and isinstance(node.parent, ast.SubNodeList)
            and isinstance(node.parent.parent, ast.FString)
        ):
            self.emit(node, node.value)
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

    def exit_ellipsis(self, node: ast.Ellipsis) -> None:
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

    def exit_comment_token(self, node: ast.CommentToken) -> None:
        """Sub objects."""
        self.emit(node, f"{node.value}")
