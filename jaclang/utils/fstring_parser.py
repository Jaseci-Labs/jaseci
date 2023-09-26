# type: ignore
"""Python Like F-String Parser."""
from jaclang.vendor.sly.lex import Lexer
from jaclang.vendor.sly.yacc import Parser, YaccProduction

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
    PIECE = r"[^\{\}\"]+|\{\{|\}\}"
    EXPR_START = r"(?<!\{)\{(?!\{)"
    EXPR_END = r"(?<!\})\}(?!\})"


class FStringParser(Parser):
    """Python Like F-String Parser."""

    tokens = FStringLexer.tokens
    start = "fstring"

    @_("STRING_START fstr_parts STRING_END")
    def fstring(self, p: YaccProduction) -> YaccProduction:
        """Start rule for fstring."""
        return p

    @_(
        "fstr_parts fstr_expr",
        "fstr_parts PIECE",
        "PIECE",
        "fstr_expr",
        "fstring",
    )
    def fstr_parts(self, p: YaccProduction) -> YaccProduction:
        """Parts of the string both in string and in expression."""
        return p

    @_("EXPR_START fstr_parts EXPR_END")
    def fstr_expr(self, p: YaccProduction) -> YaccProduction:
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
            print("Tokens:")
            for i in tokens:
                print(i, end=", ")
            tokens = lexer.tokenize(text)
            result = parser.parse(tokens)
            print("\nParse Result:")
            print(result)
