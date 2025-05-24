"""JacFormatPass for Jaseci Ast.

This is a pass for formatting Jac code.
"""

from typing import Optional

import jaclang.compiler.passes.tool.doc_ir as doc
import jaclang.compiler.unitree as uni
from jaclang.compiler.passes import Transform
from jaclang.settings import settings


class JacFormatPass(Transform[uni.Module, uni.Module]):
    """JacFormat Pass format Jac code."""

    def pre_transform(self) -> None:
        """Initialize pass."""
        self.indent_size = 4
        self.MAX_LINE_LENGTH = settings.max_line_length

    def transform(self, ir_in: uni.Module) -> uni.Module:
        """After pass."""
        ir_in.gen.jac = self.format_doc_ir()
        return ir_in

    def format_doc_ir(
        self,
        doc_node: Optional[doc.DocType] = None,
        indent_level: int = 0,
        width_remaining: Optional[int] = None,
        is_broken: bool = False,
    ) -> str:
        """Recursively print a Doc node or a list of Doc nodes."""
        if doc_node is None:
            doc_node = self.ir_in.gen.doc_ir
        if width_remaining is None:
            width_remaining = self.MAX_LINE_LENGTH

        def full_width_at_level(level: int) -> int:
            return self.MAX_LINE_LENGTH - (level * self.indent_size)

        if isinstance(doc_node, doc.Text):
            return doc_node.text

        elif isinstance(doc_node, doc.Line):
            if is_broken or doc_node.hard:
                return "\n" + " " * (indent_level * self.indent_size)
            elif doc_node.literal:
                return "\n"
            elif doc_node.tight:
                return ""
            else:
                return " "

        elif isinstance(doc_node, doc.Group):
            flat_contents_str = self.format_doc_ir(
                doc_node.contents, indent_level, width_remaining, is_broken=False
            )
            if (
                "\n" not in flat_contents_str
                and len(flat_contents_str) <= width_remaining
            ):
                return flat_contents_str
            else:
                return self.format_doc_ir(
                    doc_node.contents,
                    indent_level,
                    full_width_at_level(indent_level),
                    is_broken=True,
                )

        elif isinstance(doc_node, doc.Indent):
            new_indent_level = indent_level + 1
            return self.format_doc_ir(
                doc_node.contents,
                new_indent_level,
                full_width_at_level(new_indent_level),
                is_broken,
            )

        elif isinstance(doc_node, doc.Concat):
            result = ""
            current_line_budget = width_remaining

            for part in doc_node.parts:
                part_str = self.format_doc_ir(
                    part, indent_level, current_line_budget, is_broken
                )
                result += part_str

                if "\n" in part_str:
                    current_line_budget = full_width_at_level(indent_level)
                    last_line_of_part = part_str.splitlines()[-1]
                    indent_str_len = indent_level * self.indent_size

                    if last_line_of_part.startswith(" " * indent_str_len):
                        content_on_last_line = len(last_line_of_part) - indent_str_len
                    else:
                        content_on_last_line = len(last_line_of_part)

                    current_line_budget -= content_on_last_line
                else:
                    current_line_budget -= len(part_str)

                current_line_budget = max(0, current_line_budget)
            return result

        elif isinstance(doc_node, doc.IfBreak):
            contents = doc_node.break_contents if is_broken else doc_node.flat_contents
            return self.format_doc_ir(
                contents, indent_level, width_remaining, is_broken
            )

        elif isinstance(doc_node, doc.Align):
            align_spaces = doc_node.n if doc_node.n is not None else self.indent_size
            child_indent_level = indent_level + (align_spaces // self.indent_size)
            child_width_budget = max(0, width_remaining - align_spaces)
            return self.format_doc_ir(
                doc_node.contents, child_indent_level, child_width_budget, is_broken
            )

        else:
            raise ValueError(f"Unknown DocType: {type(doc_node)}")
