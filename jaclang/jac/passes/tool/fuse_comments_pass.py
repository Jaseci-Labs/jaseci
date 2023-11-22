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
        chomp = [*self.comments]  # Copy of self.comments
        new_tokens = []

        # Handle the case where the first comment is before any code token
        if chomp and (
            not self.all_tokens
            or chomp[0].loc.first_line < self.all_tokens[0].loc.first_line
        ):
            new_tokens.append(chomp.pop(0))

        for token in self.all_tokens:
            while chomp and (
                chomp[0].loc.first_line < token.loc.first_line
                or (
                    chomp[0].loc.first_line == token.loc.first_line
                    and chomp[0].loc.col_start < token.loc.col_start
                )
            ):
                new_tokens.append(chomp.pop(0))
            new_tokens.append(token)

        # Append any remaining comments after the last code token
        new_tokens.extend(chomp)

        # Insert the tokens back into the AST
        for i, token in enumerate(new_tokens):
            if isinstance(token, ast.CommentToken):
                if i == 0:
                    self.ir.add_kids_left([token])
                else:
                    prev_token = new_tokens[i - 1]
                    if prev_token.parent is not None:
                        parent_kids = prev_token.parent.kid
                        insert_index = parent_kids.index(prev_token) + 1
                        parent_kids.insert(insert_index, token)
                        prev_token.parent.set_kids(parent_kids)
                    else:
                        prev_token.pp()
                        raise self.ice(
                            "Token without parent in AST should be impossible"
                        )
