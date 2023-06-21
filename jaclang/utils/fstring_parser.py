"""Python Like F-String Parser."""
from jaclang.utils.sly.lex import Lexer
from jaclang.utils.sly.yacc import Parser, YaccProduction

_ = None  # For flake8 linting and sly compatibility


class FStringLexer(Lexer):
    """Python Like F-String Lexer."""

    tokens = {
        "STRING_START",
        "STRING_END",
        "EXPR_START",
        "EXPR_END",
        "PIECE",
    }
    # ignore = " \t"

    # Tokens

    STRING_START = r"f\""
    STRING_END = r"\""
    EXPR_START = r"(?<!\{)\{(?!\{)"
    EXPR_END = r"(?<!\})\}(?!\})"
    PIECE = r"[^\{\}\"']+|\{\{|\}\}"


class FStringParser(Parser):
    """Python Like F-String Parser."""

    tokens = FStringLexer.tokens

    def __init__(self) -> None:
        """Initialize the parser."""
        self.names = {}

    @_("STRING_START parts STRING_END")
    def fstring(self, p: YaccProduction) -> YaccProduction:
        """Start rule for fstring."""
        return p

    @_(
        "parts expr",
        "parts PIECE",
        "PIECE",
    )
    def parts(self, p: YaccProduction) -> YaccProduction:
        """Parts of the string both in string and in expression."""
        return p

    @_("EXPR_START parts EXPR_END")
    def expr(self, p: YaccProduction) -> YaccProduction:
        """Expressions rule."""
        return p


if __name__ == "__main__":
    """Run the parser for live testing."""
    lexer = FStringLexer()
    parser = FStringParser()
    while True:
        try:
            text = input("fstring > ")
        except EOFError:
            break
        if text:
            tokens = lexer.tokenize(text)
            result = parser.parse(tokens)
            print(result)
