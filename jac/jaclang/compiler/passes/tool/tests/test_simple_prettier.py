"""Simple test for the prettier formatter."""

import sys
import tempfile

import jaclang.compiler.unitree as uni
from jaclang.compiler.parser import JacParser
from jaclang.compiler.passes.tool.formatter.doc_builder import DocBuilder
from jaclang.compiler.passes.tool.formatter.options import FormatterOptions
from jaclang.compiler.passes.tool.formatter.printer import Printer
from jaclang.compiler.passes.tool.prettier_formatter_pass import PrettierFormatPass
from jaclang.compiler.program import JacProgram


def main():
    """Run a simple test of the prettier formatter."""
    test_code = """def simple() {
    print("Hello, world!");
}"""

    print("Testing PrettierFormatPass with code:", file=sys.stderr)
    print(test_code, file=sys.stderr)

    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix=".jac", mode="w+") as tmp:
        tmp.write(test_code)
        tmp.flush()

        # Parse the code to get the AST
        print("\nParsing the code...", file=sys.stderr)
        prog = JacProgram()
        with open(tmp.name) as file:
            source = uni.Source(file.read(), mod_path=tmp.name)
            parser = JacParser(root_ir=source, prog=prog)

        if prog.errors_had:
            print("Parsing errors:", prog.errors_had, file=sys.stderr)
            return

        print("\nDirect use of DocBuilder and Printer:", file=sys.stderr)
        options = FormatterOptions()
        doc_builder = DocBuilder(options)
        printer = Printer(options)

        doc = doc_builder.build(parser.ir_out)
        print("Doc IR:", str(doc)[:1000], file=sys.stderr)

        formatted_code = printer.print(doc)
        print("Formatted code:", formatted_code, file=sys.stderr)

        print("\nRunning PrettierFormatPass...", file=sys.stderr)
        formatter = PrettierFormatPass(ir_in=parser.ir_out, prog=prog)

        if prog.errors_had:
            print("Formatter errors:", prog.errors_had, file=sys.stderr)
            return

        print("\nFormatted output from pass:", file=sys.stderr)
        print(formatter.ir_out.gen.jac, file=sys.stderr)


if __name__ == "__main__":
    main()
