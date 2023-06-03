"""Error handling for Jac."""
import sys

from jaseci.utils.sly.yacc import YaccProduction


class JacParseErrorMixIn:
    """Error handling for Jac Parse Errors."""

    def __init__(self: "JacParseErrorMixIn") -> None:
        """Initialize Jac Parse Error Mixin."""
        super().__init__()
        self.had_error = False

    def error(self: "JacParseErrorMixIn", p: YaccProduction) -> None:
        """Improved error handling for Jac Parser."""
        self.had_error = True
        error = f'Jac Parse Error on line {p.lineno}, incorrect usage of "{p.value}"\n'
        sys.stderr.write(error)
        if not p:
            sys.stderr.write("Escaping at end of File!")
            return

        # Read ahead looking for a closing '}'
        while True:
            tok = next(self.tokens, None)
            if not tok or tok.type == "RBRACE":
                break
        self.restart()
