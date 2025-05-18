"""Pass to fuse comments into the AST."""

import jaclang.compiler.unitree as uni
from jaclang.compiler.passes import UniPass


class FuseCommentsPass(UniPass):
    """Fuses comment tokens into the AST at appropriate positions."""

    def before_pass(self) -> None:
        self.all_tokens: list[uni.Token] = []
        self.comments: list[uni.CommentToken] = []
        if isinstance(self.ir_out, uni.Module):
            self.comments = self.ir_out.source.comments
        return super().before_pass()

    def exit_node(self, node: uni.UniNode) -> None:
        if isinstance(node, uni.Token):
            self.all_tokens.append(node)

    def after_pass(self) -> None:
        # Early exit if no comments
        if not self.comments:
            return
        # Merge comments and code tokens in correct order
        merged_tokens = self._merge_tokens()
        # Insert comments into the AST structure
        self._insert_comments_in_ast(merged_tokens)

    def _merge_tokens(self) -> list[uni.Token]:
        """Merge comments and code tokens in correct order based on position."""
        merged: list[uni.Token] = []
        code_tokens = iter(self.all_tokens)
        comments = iter(self.comments)
        try:
            next_code = next(code_tokens)
        except StopIteration:
            next_code = None
        try:
            next_comment = next(comments)
        except StopIteration:
            next_comment = None

        # Handle possible leading comments
        if next_comment and (not next_code or _is_before(next_comment, next_code)):
            self.ir_out.terminals.insert(0, next_comment)

        # Merge streams in order
        while next_comment or next_code:
            if next_comment and (not next_code or _is_before(next_comment, next_code)):
                # Add comment token
                if merged and (last_token := merged[-1]):
                    self.ir_out.terminals.insert(
                        self.ir_out.terminals.index(last_token) + 1, next_comment
                    )
                merged.append(next_comment)
                try:
                    next_comment = next(comments)
                except StopIteration:
                    next_comment = None
            elif next_code:  # Check that next_code is not None
                # Add code token
                merged.append(next_code)
                try:
                    next_code = next(code_tokens)
                except StopIteration:
                    next_code = None

        return merged

    def _insert_comments_in_ast(self, merged_tokens: list[uni.Token]) -> None:
        """Insert comment tokens into the appropriate places in the AST."""
        for i, token in enumerate(merged_tokens):
            if not isinstance(token, uni.CommentToken):
                continue
            if i == len(merged_tokens) - 1:
                # Last token - add to end of tree
                self.ir_out.add_kids_right([token])
            else:
                # Insert before the next token in its parent's children
                next_token = merged_tokens[i + 1]
                if next_token.parent is None:
                    raise self.ice("Token without parent in AST")
                parent_kids = next_token.parent.kid
                insert_index = parent_kids.index(next_token)
                parent_kids.insert(insert_index, token)
                next_token.parent.set_kids(parent_kids)


def _is_before(comment: uni.CommentToken, code: uni.Token) -> bool:
    """Determine if comment should come before the code token."""
    if comment.loc.first_line < code.loc.first_line:
        return True
    elif comment.loc.first_line == code.loc.first_line:
        comment.is_inline = True
        return comment.loc.col_start < code.loc.col_start
    return False
