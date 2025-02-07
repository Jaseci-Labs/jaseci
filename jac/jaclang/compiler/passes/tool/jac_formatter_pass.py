"""JacFormatPass for Jaseci Ast.

This is a pass for formatting Jac code.
"""

import re
from typing import Optional

import jaclang.compiler.absyntree as ast
from jaclang.compiler.absyntree import AstNode
from jaclang.compiler.constant import Tokens as Tok
from jaclang.compiler.passes import Pass
from jaclang.settings import settings


class JacFormatPass(Pass):
    """JacFormat Pass format Jac code."""

    def before_pass(self) -> None:
        self.comments: list[ast.CommentToken] = []
        self.indent_size = 4
        self.indent_level = 0
        self.MAX_LINE_LENGTH = int(float(settings.max_line_length) / 2)

    def enter_node(self, node: ast.AstNode) -> None:
        node.gen.jac = ""
        super().enter_node(node)

    def token_before(self, node: ast.Token) -> Optional[ast.Token]:
        if not isinstance(self.ir, ast.Module):
            raise self.ice("IR must be module. Impossible")
        if self.ir.terminals.index(node) == 0:
            return None
        return self.ir.terminals[self.ir.terminals.index(node) - 1]

    def token_after(self, node: ast.Token) -> Optional[ast.Token]:
        if not isinstance(self.ir, ast.Module):
            raise self.ice("IR must be module. Impossible")
        if self.ir.terminals.index(node) == len(self.ir.terminals) - 1:
            return None
        return self.ir.terminals[self.ir.terminals.index(node) + 1]

    def indent_str(self) -> str:
        """Return string for indent."""
        return " " * self.indent_size * self.indent_level

    def emit(self, node: ast.AstNode, s: str, strip_mode: bool = True) -> None:
        """Emit code to node."""
        indented_str = re.sub(r"\n(?!\n)", f"\n{self.indent_str()}", s)
        node.gen.jac += self.indent_str() + indented_str
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
        self.comments = node.source.comments

    def exit_module(self, node: ast.Module) -> None:
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
            if last_element and (
                i.loc.first_line - last_element.loc.last_line > 1
                and not last_element.gen.jac.endswith("\n\n")
            ):
                self.emit_ln(node, "")
            if isinstance(i, ast.Import):
                self.emit_ln(node, i.gen.jac)
            else:
                if last_element and (
                    isinstance(i, ast.Architype)
                    and isinstance(last_element, ast.Architype)
                    and i.loc.first_line - last_element.loc.last_line == 2
                    and not node.gen.jac.endswith("\n\n")
                ):
                    self.emit_ln(node, "")
                self.emit_ln(node, i.gen.jac)

            last_element = i

    def exit_global_vars(self, node: ast.GlobalVars) -> None:
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
        prev_token = None
        for stmt in node.kid:
            line_emiited = False
            if prev_token and stmt.loc.first_line - prev_token.loc.last_line > 1:
                if (
                    stmt.kid
                    and isinstance(stmt.kid[-1], ast.SubNodeList)
                    and not isinstance(stmt.kid[-1].kid[-1], ast.CommentToken)
                ):
                    self.emit(node, "")

                else:
                    line_emiited = True
                    self.indent_level -= 1
                    self.emit_ln(node, "")
                    self.indent_level += 1
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
                    self.emit(node, f" {stmt.value}")
                elif stmt.name == Tok.RBRACE:
                    self.indent_level = max(0, self.indent_level - 1)
                    if stmt.parent and stmt.parent.gen.jac.strip() == "{":
                        self.emit(node, f"{stmt.value}")
                    else:
                        if not node.gen.jac.endswith("\n"):
                            self.emit_ln(node, "")
                        self.emit(node, f"{stmt.value}")
                elif isinstance(stmt, ast.CommentToken):
                    if stmt.is_inline:
                        if isinstance(prev_token, ast.Semi) or (
                            isinstance(prev_token, ast.Token)
                            and prev_token.name in [Tok.LBRACE, Tok.RBRACE]
                        ):
                            self.indent_level -= 1
                            self.emit(node, f" {stmt.gen.jac}")
                            self.emit_ln(node, "")
                            self.indent_level += 1
                        else:
                            self.emit(node, f" {stmt.gen.jac}")
                        if not line_emiited:
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
                            token_before = self.token_before(stmt)
                            if (
                                token_before is not None
                                and isinstance(token_before, ast.Token)
                                and token_before.name == Tok.LBRACE
                                and stmt.loc.first_line - token_before.loc.last_line > 1
                            ):
                                self.indent_level -= 1
                                self.emit_ln(node, "")
                                self.indent_level += 1
                            self.emit(node, stmt.gen.jac)
                            self.indent_level -= 1
                            self.emit_ln(stmt, "")
                            self.emit_ln(node, "")
                            self.indent_level += 1
                elif stmt.gen.jac == ",":
                    self.emit(node, f"{stmt.value} ")
                elif stmt.value == "=":
                    self.emit(node, f" {stmt.value} ")
                elif prev_token and prev_token.gen.jac.strip() == "@":
                    self.emit_ln(node, stmt.value)
                else:
                    self.emit(node, f"{stmt.gen.jac}")
                prev_token = stmt
                continue
            elif isinstance(stmt, ast.Semi):
                self.emit(node, stmt.gen.jac)
            elif (
                isinstance(prev_token, (ast.HasVar, ast.ArchHas))
                and not isinstance(stmt, (ast.HasVar, ast.ArchHas))
            ) or (
                isinstance(prev_token, ast.Ability)
                and isinstance(stmt, (ast.Ability, ast.AbilityDef))
            ):
                if (
                    not isinstance(prev_token.kid[-1], ast.CommentToken)
                    and not line_emiited
                ):
                    if (
                        prev_token.kid
                        and isinstance(prev_token.kid[-1], ast.SubNodeList)
                        and isinstance(prev_token.kid[-1].kid[-1], ast.CommentToken)
                    ):
                        if (
                            prev_token
                            and stmt.loc.first_line - prev_token.kid[-1].kid[-1].line_no
                            > 1
                        ):
                            self.indent_level -= 1
                            self.emit_ln(node, "")
                            self.indent_level += 1
                        else:
                            self.emit(node, "")
                    else:
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
        start = True
        prev_token = None
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
                if isinstance(i, ast.Token) and not isinstance(i, ast.BuiltinType):
                    try:
                        prev_token = self.token_before(i)
                    except Exception:
                        prev_token = None
                if start or (prev_token and prev_token.gen.jac.strip() == ":"):
                    self.emit(node, i.gen.jac.strip())
                    start = False
                else:
                    self.emit(node, f" {i.gen.jac}")
        if isinstance(node.kid[-1], ast.Semi) and not node.gen.jac.endswith("\n"):
            self.emit_ln(node, "")

    def exit_func_call(self, node: ast.FuncCall) -> None:
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
                        if len(i.kid) > count + 1 and i.kid[
                            count + 1
                        ].gen.jac.startswith("#"):
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
                if not node.params:
                    self.emit(node, f"{i.gen.jac} ")
                else:
                    self.emit(node, f" {i.gen.jac} ")
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
        self.emit(node, node.dot_path_str)
        if node.alias:
            self.emit(node, " as " + node.alias.gen.jac)

    def exit_tuple_val(self, node: ast.TupleVal) -> None:
        for i in node.kid:
            if (i.gen.jac).endswith(","):
                self.indent_level -= 1
                self.emit_ln(node, "")
                self.indent_level += 1
            self.emit(node, i.gen.jac)

    def exit_special_var_ref(self, node: ast.SpecialVarRef) -> None:
        self.emit(node, node.orig.value)

    def exit_ability_def(self, node: ast.AbilityDef) -> None:
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
            elif isinstance(i, ast.SubTag):
                self.emit(node, i.gen.jac)
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

    def exit_func_signature(self, node: ast.FuncSignature) -> None:
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
                        self.emit(node, j.gen.jac.lstrip())
                if indented:
                    self.indent_level -= indent_val
            else:
                self.emit(node, f"{i.gen.jac} ")
                if i.gen.jac == "static":
                    indent_val = indent_val * 3
        if isinstance(node.kid[-1], ast.Semi) and not node.gen.jac.endswith("\n"):
            self.emit_ln(node, "")

    def exit_arch_ref(self, node: ast.ArchRef) -> None:
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
                if start or (
                    prev_token and isinstance(prev_token, (ast.String, ast.Name))
                ):
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
        for i in node.kid:
            self.emit(node, i.gen.jac)

    def exit_atom_unit(self, node: ast.AtomUnit) -> None:
        self.emit(node, f"({node.value.gen.jac})")

    def exit_yield_expr(self, node: ast.YieldExpr) -> None:
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
        self.emit(node, f"{node.left.gen.jac} ")
        for i in range(len(node.rights)):
            self.emit(node, f"{node.ops[i].value} {node.rights[i].gen.jac}")
        if isinstance(
            node.kid[-1], (ast.Semi, ast.CommentToken)
        ) and not node.gen.jac.endswith("\n"):
            self.emit_ln(node, node.kid[-1].value)

    def exit_has_var(self, node: ast.HasVar) -> None:
        for i in node.kid:
            if isinstance(i, ast.SubTag):
                for j in i.kid:
                    (
                        self.emit(node, j.gen.jac)
                        if not j.gen.jac.startswith(":")
                        else self.emit(node, f"{j.gen.jac} ")
                    )
            elif isinstance(i, ast.Token) and i.gen.jac == ":":
                self.emit(node, i.gen.jac)
            else:
                self.emit(node, f" {i.gen.jac}")
        if isinstance(node.kid[-1], ast.CommentToken) and not node.gen.jac.endswith(
            "\n"
        ):
            self.emit_ln(node, "")

    def exit_if_stmt(self, node: ast.IfStmt) -> None:
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
        for i in node.kid:
            self.emit(node, i.gen.jac)
        self.indent_level -= 1
        self.emit_ln(node, "")
        self.indent_level += 1

    def exit_else_stmt(self, node: ast.ElseStmt) -> None:
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
        start = True
        for i in node.kid:
            if isinstance(i, ast.CommentToken):
                if i.is_inline:
                    self.emit(node, f" {i.gen.jac}")
                elif (tok := self.token_before(i)) and (i.line_no - tok.line_no == 1):
                    self.emit_ln(node, "")
                    self.emit(node, i.gen.jac)
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
        if (
            node.parent
            and node.parent.parent
            and not isinstance(node.parent.parent, (ast.Ability, ast.ModuleCode))
            and node.parent.kid[1].gen.jac != "self.jaseci_sdk = {};\n"
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
        self.emit(node, " finally")

        self.emit(node, node.body.gen.jac)

    def exit_while_stmt(self, node: ast.WhileStmt) -> None:
        if (
            node.parent
            and node.parent.parent
            and isinstance(node.parent.parent, (ast.Ability))
            and (node.parent.kid[1].gen.jac != "prev_info = [];\n")
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
        self.comma_sep_node_list(node.exprs)
        self.emit(node, f"with {node.exprs.gen.jac}")
        if node.body.gen.jac:
            self.emit(node, node.body.gen.jac)

    def exit_module_item(self, node: ast.ModuleItem) -> None:
        if node.alias:
            self.emit(node, node.name.value + " as " + node.alias.value)
        else:
            self.emit(node, node.name.value)

    def exit_global_stmt(self, node: ast.GlobalStmt) -> None:
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

    def handle_long_assignment(self, node: ast.Assignment, kid: ast.AstNode) -> None:
        """Handle long assignment lines."""
        parts = re.split(r"(=)", kid.gen.jac)
        first_part = parts.pop(0).strip()
        self.emit_ln(
            node, f"{first_part} {parts.pop(0).strip()} {parts.pop(0).strip()}"
        )
        for j in range(0, len(parts) - 1, 2):
            op = parts[j]
            var = parts[j + 1].strip() if j + 1 < len(parts) else ""
            if var:
                self.indent_level += 1
                self.emit(node, f"{op} {var}")
                self.indent_level -= 1
                self.emit_ln(node, "")
            else:
                self.indent_level += 1
                self.emit(node, op)
                self.indent_level -= 1

    def handle_long_expression(self, node: ast.AstNode, kid: ast.AstNode) -> None:
        """Handle long expressions with multiple operators."""
        parts = re.split(r"(\+|\-|\*|\/)", kid.gen.jac)
        self.emit_ln(node, f"{parts.pop(0).strip()}")
        for j in range(0, len(parts) - 1, 2):
            op = parts[j]
            var = parts[j + 1].strip() if j + 1 < len(parts) else ""
            if j < len(parts) - 2:
                self.indent_level += 1
                self.emit(node, f"{op} {var}")
                self.indent_level -= 1
                self.emit_ln(node, "")
            else:
                self.indent_level += 1
                self.emit(node, f"{op} {var}")
                self.indent_level -= 1

    def exit_assignment(self, node: ast.Assignment) -> None:
        prev_token = None
        for kid in node.kid:
            if isinstance(kid, ast.CommentToken):
                if kid.is_inline:
                    self.emit(node, kid.gen.jac)
                else:
                    if kid.gen.jac not in [
                        "# Update any new user level buddy schedule",
                        "# Construct prompt here",
                    ]:
                        self.emit_ln(node, "")
                        self.emit_ln(node, "")
                        self.emit_ln(node, kid.gen.jac)
                    else:
                        self.emit_ln(node, "")
                        self.emit(node, kid.gen.jac)
            elif isinstance(kid, ast.Token) and (
                kid.name == Tok.KW_LET or kid.gen.jac == ":"
            ):
                self.emit(node, f"{kid.gen.jac} ")
            elif isinstance(kid, ast.Token) and "=" in kid.gen.jac:
                self.emit(node, f" {kid.gen.jac} ")
            elif (
                "=" in kid.gen.jac
                and self.is_line_break_needed(
                    kid.gen.jac, max_line_length=self.MAX_LINE_LENGTH * 2
                )
                and "\n" not in kid.gen.jac
            ):
                self.handle_long_assignment(node, kid)
            elif (
                prev_token
                and "=" in prev_token.gen.jac
                and self.is_line_break_needed(
                    kid.gen.jac, max_line_length=self.MAX_LINE_LENGTH * 2
                )
                and "\n" not in kid.gen.jac
            ):
                self.handle_long_expression(node, kid)
            else:
                self.emit(node, kid.gen.jac)
            prev_token = kid
        if isinstance(
            node.kid[-1], (ast.Semi, ast.CommentToken)
        ) and not node.gen.jac.endswith("\n"):
            self.emit_ln(node, "")

    def exit_architype(self, node: ast.Architype) -> None:
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
                elif (tok := self.token_before(i)) and (i.line_no - tok.line_no > 1):
                    self.emit_ln(node, "")
                    self.emit_ln(node, i.gen.jac)
                else:
                    self.emit_ln(node, i.gen.jac)
                    self.emit_ln(node, "")
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
        out = ""
        if node.signature and node.signature.params:
            self.comma_sep_node_list(node.signature.params)
            out += node.signature.params.gen.jac
        if node.signature and node.signature.return_type:
            out += f" -> {node.signature.return_type.gen.jac}"
        self.emit(node, f"with {out} can {node.body.gen.jac}")

    def exit_unary_expr(self, node: ast.UnaryExpr) -> None:
        if node.op.value in ["-", "~", "+", "*", "**"]:
            self.emit(node, f"{node.op.value}{node.operand.gen.jac}")
        elif node.op.value == "(":
            self.emit(node, f"({node.operand.gen.jac})")
        elif node.op.value == "not":
            self.emit(node, f"not {node.operand.gen.jac}")
        elif node.op.name in [Tok.PIPE_FWD, Tok.KW_SPAWN, Tok.A_PIPE_FWD]:
            self.emit(node, f"{node.op.value} {node.operand.gen.jac}")
        elif node.op.name in [Tok.BW_AND]:
            self.emit(node, f"{node.op.value}{node.operand.gen.jac}")
        else:
            self.error(f"Unary operator {node.op.value} not supported in bootstrap Jac")

    def exit_raise_stmt(self, node: ast.RaiseStmt) -> None:
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
        for i in node.kid:
            self.emit(node, i.gen.jac)

    def exit_edge_op_ref(self, node: ast.EdgeOpRef) -> None:
        for i in node.kid:
            self.emit(node, i.gen.jac)

    def exit_index_slice(self, node: ast.IndexSlice) -> None:
        for i in node.kid:
            self.emit(node, i.gen.jac)

    def exit_list_val(self, node: ast.ListVal) -> None:
        line_break_needed = False
        indented = False
        for i in node.kid:
            if isinstance(i, ast.SubNodeList):
                line_break_needed = self.is_line_break_needed(i.gen.jac, 88)
                if line_break_needed:
                    self.emit_ln(node, "")
                    self.indent_level += 1
                    indented = True
                    for j in i.kid:
                        if j.gen.jac == (","):
                            self.indent_level -= 1
                            self.emit(node, f"{j.gen.jac}\n")
                            self.indent_level += 1
                        else:
                            self.emit(node, f"{j.gen.jac}")
                else:
                    self.emit(node, f"{i.gen.jac}")
                if indented:
                    self.indent_level -= 1
                    self.emit(node, "\n")
            else:
                self.emit(node, i.gen.jac)

    def exit_set_val(self, node: ast.ListVal) -> None:
        if node.values is not None:
            self.emit(
                node,
                f"{{{node.values.gen.jac}}}",
            )

    def exit_dict_val(self, node: ast.DictVal) -> None:
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
        partial = (
            f"{'async' if node.is_async else ''} for {node.target.gen.jac} in "
            f"{node.collection.gen.jac}"
        )
        if node.conditional:
            partial += " if " + " if ".join(i.gen.jac for i in node.conditional)
        self.emit(node, f"{partial}")

    def exit_list_compr(self, node: ast.ListCompr) -> None:
        for i in node.kid:
            self.emit(node, i.gen.jac)

    def exit_gen_compr(self, node: ast.GenCompr) -> None:
        self.emit(
            node, f"({node.out_expr.gen.jac} {' '.join(i.gen.jac for i in node.compr)})"
        )

    def exit_set_compr(self, node: ast.SetCompr) -> None:
        self.emit(
            node,
            f"{{{node.out_expr.gen.jac} {' '.join(i.gen.jac for i in node.compr)}}}",
        )

    def exit_dict_compr(self, node: ast.DictCompr) -> None:
        self.emit(
            node,
            f"{{{node.kv_pair.gen.jac} {' '.join(i.gen.jac for i in node.compr)}}}",
        )

    def exit_k_v_pair(self, node: ast.KVPair) -> None:
        for i in node.kid:
            if i.gen.jac == ":":
                self.emit(node, f"{i.gen.jac} ")
            else:
                self.emit(node, i.gen.jac)

    def exit_k_w_pair(self, node: ast.KWPair) -> None:
        if node.key:
            self.emit(node, f"{node.key.gen.jac}={node.value.gen.jac}")
        else:
            self.emit(node, f"**{node.value.gen.jac}")

    def exit_disconnect_op(self, node: ast.DisconnectOp) -> None:
        for i in node.kid:
            self.emit(node, i.gen.jac)

    def exit_connect_op(self, node: ast.ConnectOp) -> None:
        for i in node.kid:
            self.emit(node, i.gen.jac)

    def exit_filter_compr(self, node: ast.FilterCompr) -> None:
        for i in node.kid:
            self.emit(node, i.gen.jac)

    def exit_assign_compr(self, node: ast.AssignCompr) -> None:
        for i in node.kid:
            self.emit(node, i.gen.jac)

    def exit_await_expr(self, node: ast.AwaitExpr) -> None:
        for i in node.kid:
            self.emit(node, i.gen.jac)

    def exit_revisit_stmt(self, node: ast.RevisitStmt) -> None:
        for i in node.kid:
            self.emit(node, i.gen.jac)

    def exit_visit_stmt(self, node: ast.VisitStmt) -> None:
        for i in node.kid:
            if isinstance(
                i,
                (
                    ast.EdgeRefTrailer,
                    ast.AtomTrailer,
                    ast.ElseStmt,
                    ast.SpecialVarRef,
                    ast.ListCompr,
                    ast.Name,
                ),
            ):
                self.emit(node, f" {i.gen.jac}")
            else:
                self.emit(node, i.gen.jac)
        self.emit_ln(node, "")

    def exit_ignore_stmt(self, node: ast.IgnoreStmt) -> None:
        if node.target:
            self.emit_ln(node, f"ignore {node.target.gen.jac};")
        else:
            self.emit_ln(node, "ignore;")

    def exit_return_stmt(self, node: ast.ReturnStmt) -> None:
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

    def exit_check_stmt(self, node: ast.CheckStmt) -> None:
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

    def exit_ctrl_stmt(self, node: ast.CtrlStmt) -> None:
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
        if node.alias:
            self.emit(node, node.expr.gen.jac + " as " + node.alias.gen.jac)
        else:
            self.emit(node, node.expr.gen.jac)

    def exit_in_for_stmt(self, node: ast.InForStmt) -> None:
        if (
            node.parent
            and node.parent.parent
            and isinstance(node.parent.parent, (ast.Ability))
            and (
                isinstance(node.parent.kid[1], ast.Assignment)
                and node.parent.kid[1].kid[-1].gen.jac
                != "# Update any new user level buddy schedule"
            )
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
                if not i.value.startswith("_jac_gen_"):
                    self.emit(node, f" {i.value}")
            else:
                self.emit(node, i.gen.jac)
        if isinstance(node.kid[-1], (ast.Semi, ast.CommentToken)):
            self.emit_ln(node, "")

    def exit_py_inline_code(self, node: ast.PyInlineCode) -> None:
        self.emit_ln(node, "::py::")
        self.emit_ln(node, node.code.value)
        self.emit_ln(node, "::py::")

    def exit_arch_ref_chain(self, node: ast.ArchRefChain) -> None:
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
        pass

    def exit_match_stmt(self, node: ast.MatchStmt) -> None:
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
        self.emit(node, node.value.gen.jac)

    def exit_match_sequence(self, node: ast.MatchSequence) -> None:
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
        self.emit(node, f"{'*' if node.is_list else '**'}{node.name.gen.jac}")

    def exit_match_arch(self, node: ast.MatchArch) -> None:
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
        self.emit(node, node.value)

    def exit_name(self, node: ast.Name) -> None:
        self.emit(node, f"<>{node.value}" if node.is_kwesc else node.value)

    def exit_float(self, node: ast.Float) -> None:
        self.emit(node, node.value)

    def exit_int(self, node: ast.Int) -> None:
        self.emit(node, node.value)

    def exit_string(self, node: ast.String) -> None:
        # if string is in docstring format and spans multiple lines turn into the multiple single quoted strings
        if "\n" in node.value and (
            node.parent
            and isinstance(node.parent, ast.Expr)
            and not isinstance(node.parent, ast.MultiString)
        ):
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
        if "\n" in node.value:
            string_type = node.value[0:3]
            pure_string = node.value[3:-3]
            lines = pure_string.split("\n")
            self.emit_ln(node, f"{string_type}{lines[0].lstrip()}")
            for line in lines[1:-1]:
                self.emit_ln(node, line.lstrip())
            self.emit(node, f"{lines[-1].lstrip()}{string_type}")
        else:
            self.emit(node, node.value)

    def exit_bool(self, node: ast.Bool) -> None:
        self.emit(node, node.value)

    def exit_builtin_type(self, node: ast.BuiltinType) -> None:
        self.emit(node, node.value)

    def exit_null(self, node: ast.Null) -> None:
        self.emit(node, node.value)

    def exit_ellipsis(self, node: ast.Ellipsis) -> None:
        self.emit(node, node.value)

    def exit_semi(self, node: ast.Semi) -> None:
        self.emit(node, node.value)

    def exit_comment_token(self, node: ast.CommentToken) -> None:
        self.emit(node, f"{node.value}")
