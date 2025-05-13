"""PrettierFormatPass for Jaseci Ast.

This is a pass for formatting Jac code using a prettier-style architecture.
"""

import sys

import jaclang.compiler.unitree as uni
from jaclang.compiler.passes import UniPass
from jaclang.compiler.passes.tool.formatter.doc_builder import DocBuilder
from jaclang.compiler.passes.tool.formatter.options import FormatterOptions
from jaclang.compiler.passes.tool.formatter.printer import Printer
from jaclang.settings import settings


class PrettierFormatPass(UniPass):
    """PrettierFormat Pass formats Jac code using the prettier-style architecture."""

    def before_pass(self) -> None:
        """Initialize pass."""
        self.options = FormatterOptions(
            indent_size=4,
            max_line_length=settings.max_line_length,
        )
        self.doc_builder = DocBuilder(self.options)
        self.printer = Printer(self.options)

    def run_pass(self) -> None:
        """Execute the formatting pass."""
        print(
            "PrettierFormatPass.run_pass(): Input IR type:",
            type(self.ir_in),
            file=sys.stderr,
        )

        # Make sure we have a valid output IR
        self.ir_out = self.ir_in.copy()

        # Phase 1: Build Doc IR
        doc = self.doc_builder.build(self.ir_in)
        print("Built Doc IR:", str(doc)[:100], file=sys.stderr)

        # Phase 2: Print the Doc IR to formatted code
        formatted_code = self.printer.print(doc)
        print(
            "Formatted code (first 100 chars):", formatted_code[:100], file=sys.stderr
        )

        # Store the result in the output IR
        self.ir_out.gen.jac = formatted_code
        print(
            "Output IR has jac attribute:",
            hasattr(self.ir_out.gen, "jac"),
            file=sys.stderr,
        )
