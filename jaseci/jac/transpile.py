"""Transpilation of Jaseci code to python code."""

from jaseci.jac.lexer import JacLexer
from jaseci.jac.parser import JacParser


class JacTranspiler:
    """Transpiler for Jaseci code to python code."""

    def __init__(self: "JacTranspiler", code: str) -> None:
        """Initialize transpiler."""
        self.code = code
        self.lexer = JacLexer()
        self.parser = JacParser()
        self.tree = self.parser.parse(self.lexer.tokenize(self.code))
        self.indent = 0
        self.output = self.transpile()

    def transpile(self: "JacTranspiler") -> str:
        """Transpile code."""
        return self.transpile_start()

    def emit(self: "JacTranspiler", code: str) -> str:
        """Emit code."""
        return code

    def transpile_start(self: "JacTranspiler") -> str:
        """Transpile code."""
