"""JacFormatPass for Jaseci Ast.

This is a pass for formatting Jac code.
"""

import jaclang.compiler.absyntree as ast
from jaclang.compiler.passes import Pass


class FuseCommentsPass(Pass):
    """JacFormat Pass format Jac code."""

    def before_pass(self) -> None:
        """Before pass."""
        self.all_tokens: list[ast.Token] = []
        self.comments: list[ast.CommentToken] = (
            self.ir.source.comments if isinstance(self.ir, ast.Module) else []
        )
        return super().before_pass()

    def exit_node(self, node: ast.AstNode) -> None:
        """Exit node."""
        if isinstance(node, ast.Token):
            self.all_tokens.append(node)

    def after_pass(self) -> None:
        """Insert comment tokens into all_tokens."""
        comment_stream = iter(self.comments)  # Iterator for comments
        code_stream = iter(self.all_tokens)  # Iterator for code tokens
        new_stream: list[ast.AstNode] = []  # New stream to hold ordered tokens

        try:
            next_comment = next(comment_stream)  # Get the first comment
        except StopIteration:
            next_comment = None

        try:
            next_code = next(code_stream)  # Get the first code token
        except StopIteration:
            next_code = None

        while next_comment or next_code:
            if next_comment and (
                not next_code or is_comment_next(next_comment, next_code)
            ):
                # Add the comment to the new stream
                new_stream.append(next_comment)
                try:
                    next_comment = next(comment_stream)
                except StopIteration:
                    next_comment = None
            elif next_code:
                # Add the code token to the new stream
                new_stream.append(next_code)
                try:
                    next_code = next(code_stream)
                except StopIteration:
                    next_code = None

        # Insert the tokens back into the AST
        for i, token in enumerate(new_stream):
            if isinstance(token, ast.CommentToken):
                if i == 0:
                    self.ir.add_kids_left([token])
                else:
                    prev_token = new_stream[i - 1]
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


def is_comment_next(cmt: ast.CommentToken, code: ast.Token) -> bool:
    """Compare two CodeLocInfo objects."""
    if cmt.loc.first_line < code.loc.first_line:
        return True
    elif cmt.loc.first_line == code.loc.first_line:
        cmt.is_inline = True
        return cmt.loc.col_start < code.loc.col_start
    return False
