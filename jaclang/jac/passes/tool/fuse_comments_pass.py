"""JacFormatPass for Jaseci Ast.

This is a pass for formatting Jac code.
"""

from typing import Any, List, Tuple

import jaclang.jac.absyntree as ast
from jaclang.jac.constant import Constants as Con
from jaclang.jac.constant import Tokens as Tok
from jaclang.jac.passes import Pass


class FuseCommentsPass(Pass):
    """JacFormat Pass format Jac code."""

    def before_pass(self) -> None:
        self.all_tokens: list[ast.Token] = []
        self.comments: list[ast.Token] = (
            self.ir.source.comments if isinstance(self.ir, ast.Module) else []
        )
        return super().before_pass()

    def exit_node(self, node: ast.AstNode) -> None:
        """Exit node."""
        if isinstance(node, ast.Token):
            self.all_tokens.append(node)

    def after_pass(self) -> None:
        """Insert comment tokens into all_tokens."""
        marker = 0
        new_tokens: list[ast.Token] = []
        for i in range(len(self.all_tokens)):
            new_tokens.append(self.all_tokens[i])
            if i >= len(self.all_tokens) - 1:
                break
            if marker >= len(self.comments):
                new_tokens.extend(self.all_tokens[i + 1 :])
                break
            elif (
                self.all_tokens[i].loc.first_line
                <= self.comments[marker].loc.first_line
                or self.all_tokens[i].loc.col_start
                <= self.comments[marker].loc.col_start
            ) and (
                self.all_tokens[i + 1].loc.last_line
                >= self.comments[marker].loc.last_line
                or self.all_tokens[i + 1].loc.col_end
                >= self.comments[marker].loc.col_end
            ):
                new_tokens.append(self.comments[marker])
                marker += 1

        for i in range(len(new_tokens)):
            if isinstance(new_tokens[i], ast.CommentToken):
                if i == 0:
                    self.ir.add_kids_left([new_tokens[i]])
                    continue
                new_val = new_tokens[i - 1]
                if new_val.parent is not None:
                    new_kids = new_val.parent.kid
                    new_kids.insert(new_kids.index(new_val), new_tokens[i])
                    new_val.parent.set_kids(new_kids)
                else:
                    raise self.ice("Token without parent in AST should be impossible")
