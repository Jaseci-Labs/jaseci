"""JacFormatPass for Jaseci Ast.

This is a pass for formatting Jac code.
"""

import jaclang.jac.absyntree as ast
from jaclang.jac.passes import Pass


class FuseCommentsPass(Pass):
    """JacFormat Pass format Jac code."""

    def before_pass(self) -> None:
        """Before pass."""
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
        chomp: list[ast.CommentToken] = [*self.comments]
        new_tokens: list[ast.Token] = []
        if not len(chomp):
            return
        for i in range(len(self.all_tokens)):
            chomp[0].is_inline = chomp[0].is_inline or (
                self.all_tokens[i].loc.first_line == chomp[0].loc.first_line
            )
            if i == len(self.all_tokens) - 1:
                if len(chomp):
                    new_tokens.append(self.all_tokens[i])
                    new_tokens += chomp
                break
            while (i < len(self.all_tokens) - 1) and (
                (
                    self.all_tokens[i].loc.first_line == chomp[0].loc.first_line
                    and self.all_tokens[i].loc.col_start > chomp[0].loc.col_start
                )
                or (self.all_tokens[i].loc.first_line > chomp[0].loc.first_line)
            ):
                new_tokens.append(chomp[0])
                chomp = chomp[1:]
                if not len(chomp):
                    new_tokens.extend(self.all_tokens[i + 1 :])
                    break
            new_tokens.append(self.all_tokens[i])
            if not len(chomp):
                break
        for i in range(len(new_tokens)):
            if isinstance(new_tokens[i], ast.CommentToken):
                if i == 0:
                    self.ir.add_kids_left([new_tokens[i]])
                    continue
                new_val = new_tokens[i - 1]
                if new_val.parent is not None:
                    new_kids = new_val.parent.kid
                    new_kids.insert(new_kids.index(new_val) + 1, new_tokens[i])
                    new_val.parent.set_kids(new_kids)
                else:
                    new_val.pp()
                    raise self.ice("Token without parent in AST should be impossible")
