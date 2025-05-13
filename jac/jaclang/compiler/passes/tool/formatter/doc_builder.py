"""Doc builder for converting AST to Doc IR.

This module contains the DocBuilder class that transforms the AST into the Doc IR.
"""

import re
from typing import Dict, List, Optional

import jaclang.compiler.unitree as uni
from jaclang.compiler.constant import Tokens as Tok
from jaclang.compiler.unitree import UniNode

from jaclang.compiler.passes.tool.formatter.doc_ir import (
    Align,
    Concat,
    Doc,
    Group,
    IfBreak,
    Indent,
    Line,
    Text,
)
from jaclang.compiler.passes.tool.formatter.options import FormatterOptions


class DocBuilder:
    """DocBuilder transforms AST nodes into Doc IR."""

    def __init__(self, options: FormatterOptions):
        """Initialize the DocBuilder.

        Args:
            options: Formatter options to use
        """
        self.options = options
        self.comments: List[uni.CommentToken] = []

    def build(self, node: UniNode) -> Doc:
        """Build Doc IR from an AST node.

        Args:
            node: The root AST node to convert

        Returns:
            Doc IR representation of the node
        """
        if isinstance(node, uni.Module):
            self.comments = node.source.comments

        return self._build_node(node)

    def _build_node(self, node: UniNode) -> Doc:
        """Build Doc IR for a specific node.

        This method dispatches to specific node type handlers.

        Args:
            node: The AST node to convert

        Returns:
            Doc IR representation of the node
        """
        # Dispatch to specific node type handler
        handler_name = f"_build_{node.__class__.__name__.lower()}"
        if hasattr(self, handler_name):
            return getattr(self, handler_name)(node)

        # If we have children, process them
        if hasattr(node, "kid") and node.kid:
            parts = []
            for kid in node.kid:
                if isinstance(kid, UniNode):
                    parts.append(self._build_node(kid))
                else:
                    parts.append(Text(str(kid)))
            return Concat(parts)

        # Fallback for simple nodes
        if hasattr(node, "gen") and hasattr(node.gen, "jac"):
            return Text(node.gen.jac)
        else:
            return Text(str(node))

    def _build_module(self, node: uni.Module) -> Doc:
        """Build Doc IR for a Module node.

        Args:
            node: The Module node

        Returns:
            Doc IR representation
        """
        parts = []

        for kid in node.kid:
            if isinstance(kid, UniNode):
                parts.append(self._build_node(kid))
                parts.append(Line(hard=True))

        return Concat(parts)

    def _build_ability(self, node: uni.Ability) -> Doc:
        """Build Doc IR for an Ability node.

        Args:
            node: The Ability node

        Returns:
            Doc IR representation
        """
        parts = []

        # Handle ability signature
        signature_parts = []
        for kid in node.kid:
            if isinstance(kid, uni.SubNodeList):
                # We'll handle the code block separately
                continue
            elif isinstance(kid, UniNode):
                signature_parts.append(self._build_node(kid))
            elif isinstance(kid, str):
                signature_parts.append(Text(kid))
            else:
                signature_parts.append(Text(str(kid)))

        # Add the signature
        parts.append(Group(Concat(signature_parts)))

        # Handle code block
        for kid in node.kid:
            if isinstance(kid, uni.SubNodeList):
                parts.append(Text(" "))
                parts.append(Text("{"))
                parts.append(Line())
                parts.append(Indent(self._build_subnodelist(kid)))
                parts.append(Line())
                parts.append(Text("}"))
                break

        return Group(Concat(parts))

    def _build_subnodelist(self, node: uni.SubNodeList) -> Doc:
        """Build Doc IR for a SubNodeList node containing CodeBlockStmt nodes.

        Args:
            node: The SubNodeList node containing CodeBlockStmt nodes

        Returns:
            Doc IR representation
        """
        parts = []

        # Access the kids via the proper attribute name
        if hasattr(node, "nodes"):
            nodes = node.nodes
        elif hasattr(node, "kid"):
            nodes = node.kid
        else:
            nodes = []

        for kid in nodes:
            if isinstance(kid, UniNode):
                stmt_doc = self._build_node(kid)
                parts.append(stmt_doc)

                # Add semicolon and line break
                if self.options.semicolons and not isinstance(
                    kid, (uni.IfStmt, uni.ForStmt, uni.WhileStmt)
                ):
                    parts.append(Text(";"))
                parts.append(Line(hard=True))

        return Concat(parts)

    def _build_assignment(self, node: uni.Assignment) -> Doc:
        """Build Doc IR for an Assignment node.

        Args:
            node: The Assignment node

        Returns:
            Doc IR representation
        """
        parts = []

        for kid in node.kid:
            if isinstance(kid, uni.Token) and kid.name == Tok.KW_LET:
                parts.append(Text(kid.gen.jac))
                parts.append(Text(" "))
            elif isinstance(kid, uni.Token) and "=" in kid.gen.jac:
                parts.append(Text(" "))
                parts.append(Text(kid.gen.jac))
                parts.append(Text(" "))
            elif isinstance(kid, UniNode):
                parts.append(self._build_node(kid))
            else:
                parts.append(Text(str(kid)))

        return Group(Concat(parts))

    def _build_ifstmt(self, node: uni.IfStmt) -> Doc:
        """Build Doc IR for an IfStmt node.

        Args:
            node: The IfStmt node

        Returns:
            Doc IR representation
        """
        parts = []
        condition = None
        then_block = None
        else_block = None

        # Find condition and blocks
        for kid in node.kid:
            if isinstance(kid, uni.Token) and kid.name == Tok.KW_IF:
                parts.append(Text("if "))
            elif isinstance(kid, uni.Token) and kid.name == Tok.KW_ELIF:
                parts.append(Text("elif "))
            elif isinstance(kid, uni.Token) and kid.name == Tok.KW_ELSE:
                parts.append(Text("else"))
            elif (
                condition is None
                and isinstance(kid, UniNode)
                and not isinstance(kid, uni.SubNodeList)
            ):
                condition = kid
                parts.append(self._build_node(condition))
            elif isinstance(kid, uni.SubNodeList):
                if then_block is None:
                    then_block = kid
                    # Add the then block
                    parts.append(Text(" {"))
                    parts.append(Line())
                    parts.append(Indent(self._build_subnodelist(then_block)))
                    parts.append(Line())
                    parts.append(Text("}"))
                else:
                    else_block = kid
                    # Add the else block
                    parts.append(Text(" {"))
                    parts.append(Line())
                    parts.append(Indent(self._build_subnodelist(else_block)))
                    parts.append(Line())
                    parts.append(Text("}"))

        return Group(Concat(parts))

    def _build_binaryexpr(self, node: uni.BinaryExpr) -> Doc:
        """Build Doc IR for a BinaryExpr node.

        Args:
            node: The BinaryExpr node

        Returns:
            Doc IR representation
        """
        if len(node.kid) < 3:
            # Simple case, not enough kids for a proper binary expression
            return self._build_default(node)

        left = node.kid[0]
        op = node.kid[1]
        right = node.kid[2]

        left_doc = (
            self._build_node(left) if isinstance(left, UniNode) else Text(str(left))
        )
        right_doc = (
            self._build_node(right) if isinstance(right, UniNode) else Text(str(right))
        )

        # Format with spaces around operator
        parts = [
            left_doc,
            Text(f" {op.gen.jac if hasattr(op, 'gen') else str(op)} "),
            right_doc,
        ]

        # Group it, allowing breaks after operators if needed
        return Group(Concat(parts))

    def _build_default(self, node: UniNode) -> Doc:
        """Default builder for nodes without specific handlers.

        Args:
            node: The node to convert

        Returns:
            Doc IR representation
        """
        if hasattr(node, "kid") and node.kid:
            parts = []
            for kid in node.kid:
                if isinstance(kid, UniNode):
                    parts.append(self._build_node(kid))
                else:
                    parts.append(Text(str(kid)))
            return Concat(parts)

        # Fallback for simple nodes
        if hasattr(node, "gen") and hasattr(node.gen, "jac"):
            return Text(node.gen.jac)
        else:
            return Text(str(node))
