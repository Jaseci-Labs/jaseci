"""Jac Blue pass for drawing AST."""
from typing import List, Optional

import jaclang.jac.absyntree as ast
from jaclang.jac.passes import Pass


class ASTPrinterPass(Pass):
    """Jac AST convertion to ascii tree."""

    SAVE_OUTPUT: Optional[str] = None

    def before_pass(self) -> None:
        """Initialize pass."""
        self.__print_tree(self.ir)
        self.terminate()
        return super().before_pass()

    def __print_tree(
        self,
        root: ast.AstNode,
        marker: str = "+-- ",
        level_markers: Optional[List[str]] = None,
    ) -> None:
        """Recursive function that prints the hierarchical structure of a tree."""
        if root is None:
            return

        empty_str = " " * len(marker)
        connection_str = "|" + empty_str[:-1]
        if not level_markers:
            level_markers = []
        level = len(level_markers)  # recursion level

        def mapper(draw: bool) -> str:
            return connection_str if draw else empty_str

        markers = "".join(map(mapper, level_markers[:-1]))
        markers += marker if level > 0 else ""
        if self.SAVE_OUTPUT:
            with open(self.SAVE_OUTPUT, "a+") as f:
                print(f"{markers}{self.__node_repr_in_tree(root)}", file=f)
        else:
            print(f"{markers}{self.__node_repr_in_tree(root)}")
        # After root has been printed, recurse down (depth-first) the child nodes.
        for i, child in enumerate(root.kid):
            # The last child will not need connection markers on the current level
            # (see example above)
            is_last = i == len(root.kid) - 1
            self.__print_tree(child, marker, [*level_markers, not is_last])

    def __node_repr_in_tree(self, node: ast.AstNode) -> str:
        if isinstance(node, ast.Token):
            node: ast.Token
            return f"{node.__class__.__name__}(name={node.name}, val={node.value})"
        else:
            return node.__class__.__name__
