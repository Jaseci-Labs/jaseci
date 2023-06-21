"""Error handling for Jac."""
import sys
from typing import Generator, Optional

from jaclang.utils.sly.yacc import YaccProduction


class JacParseErrorMixIn:
    """Error handling for Jac Parse Errors."""

    def __init__(self, cur_filename: str = "str_parse") -> None:
        """Initialize Jac Parse Error Mixin."""
        super().__init__()
        self.cur_file = cur_filename
        self.had_error = False

    def error(self, p: YaccProduction) -> None:
        """Improved error handling for Jac Parser."""
        self.had_error = True
        error = f'{self.cur_file}: Jac Parse Error on line {p.lineno}, incorrect usage of "{p.value}" ({p.type})\n'
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

    def parse(self, tokens: Generator, filename: Optional[str] = None) -> None:
        """Overload of parse to take filenames."""
        if filename:
            self.cur_file = filename
        self.had_error = False
        return super().parse(tokens)
