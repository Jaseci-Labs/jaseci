"""Lark parser for Jac Lang."""

from typing import Optional

from jaclang.jac import JacLark
from jaclang.jac.transform import Transform


class JacParser(Transform):
    """Jac Parser."""

    def __init__(
        self,
        mod_path: str,
        input_ir: str,
        base_path: str = "",
        prior: Optional[Transform] = None,
    ) -> None:
        """Initialize parser."""
        self.comments = []
        self.parser = JacLark(lexer_callbacks={"COMMENT": self.comments.append})
        Transform.__init__(self, mod_path, input_ir, base_path, prior)

    def transform(self, ir: str) -> JacLark:
        """Transform input IR."""
        return self.parser.parse(ir)
