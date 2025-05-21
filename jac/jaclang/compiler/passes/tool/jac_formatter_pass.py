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

        if isinstance(doc_node, doc.Text):
            return doc_node.text

        elif isinstance(doc_node, doc.Line):
            if is_broken or doc_node.hard:
                return "\n" + " " * (indent_level * self.indent_size)
            elif doc_node.literal:  # literal soft line
                return "\n"
            elif doc_node.tight:
                return ""
            else:  # soft line, not broken
                return " "

        elif isinstance(doc_node, doc.Group):
            # Try to print flat first. For this attempt, the group itself isn't forced to break.
            flat_contents_str = self.format_doc_ir(
                doc_node.contents, indent_level, width_remaining, is_broken=False
            )
            if (
                "\n" not in flat_contents_str
                and len(flat_contents_str) <= width_remaining
            ):
                return flat_contents_str
            else:
                full_width_for_broken_content = self.MAX_LINE_LENGTH - (
                    indent_level * self.indent_size
                )
                return self.format_doc_ir(
                    doc_node.contents,
                    indent_level,
                    full_width_for_broken_content,
                    is_broken=True,
                )

        elif isinstance(doc_node, doc.Indent):
            new_indent_level = indent_level + 1

            width_for_indented_content = self.MAX_LINE_LENGTH - (
                new_indent_level * self.indent_size
            )
            return self.format_doc_ir(
                doc_node.contents,
                new_indent_level,
                width_for_indented_content,  # Budget for lines within indent
                is_broken,  # is_broken state propagates
            )

        elif isinstance(doc_node, doc.Concat):
            result = ""
            # current_line_budget is the space left on the current line for the current part.
            current_line_budget = width_remaining

            for part in doc_node.parts:
                part_str = self.format_doc_ir(
                    part, indent_level, current_line_budget, is_broken
                )
                result += part_str

                if "\n" in part_str:
                    # part_str created a newline. The next part starts on a new line.
                    # Its budget is the full width available at this indent level.
                    current_line_budget = self.MAX_LINE_LENGTH - (
                        indent_level * self.indent_size
                    )
                    # Subtract what the *last line* of part_str consumed from this budget.
                    # The characters on the last line after the indent string.
                    indent_str_len = indent_level * self.indent_size
                    last_line_of_part = part_str.splitlines()[-1]

                    content_on_last_line = 0
                    if last_line_of_part.startswith(" " * indent_str_len):
                        content_on_last_line = len(last_line_of_part) - indent_str_len
                    else:  # It was a line not starting with the full indent (e.g. literal \n)
                        content_on_last_line = len(last_line_of_part)

                    current_line_budget -= content_on_last_line
                else:
                    # part_str stayed on the same line. Reduce budget for next part on this line.
                    current_line_budget -= len(part_str)

                if current_line_budget < 0:  # Ensure budget isn't negative
                    current_line_budget = 0
            return result

        elif isinstance(doc_node, doc.IfBreak):
            if is_broken:
                return self.format_doc_ir(
                    doc_node.break_contents, indent_level, width_remaining, is_broken
                )
            else:
                return self.format_doc_ir(
                    doc_node.flat_contents, indent_level, width_remaining, is_broken
                )

        elif isinstance(doc_node, doc.Align):
            align_spaces = doc_node.n if doc_node.n is not None else self.indent_size
            # effective_total_indent_spaces_for_children = (
            #     indent_level * self.indent_size
            # ) + align_spaces
            child_indent_level_for_align = indent_level + (
                align_spaces // self.indent_size
            )

            child_width_budget = width_remaining - align_spaces
            if child_width_budget < 0:
                child_width_budget = 0

            return self.format_doc_ir(
                doc_node.contents,
                child_indent_level_for_align,  # Approximated level for Lines inside
                child_width_budget,  # Budget for content on first line
                is_broken,
            )
        else:
            raise ValueError(f"Unknown DocType: {type(doc_node)}")
