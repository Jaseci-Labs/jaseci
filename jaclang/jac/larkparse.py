"""Lark parser for Jac Lang."""
import os
from typing import Optional

from jaclang.vendor.lark import Lark, Transformer, v_args
import jaclang.jac.absyntree as ast
from jaclang.jac.transform import ABCParserMeta, Transform

with open(os.path.join(os.path.dirname(__file__), "jac.lark"), "r") as f:
    jac_grammar = f.read()


class JacParser(Transform):
    def __init__(
        self,
        mod_path: str,
        input_ir: str,
        base_path: str = "",
        prior: Optional[Transform] = None,
    ):
        self.parser = Lark(jac_grammar)
        self.ir = self.transform(input_ir)

    def transform(self, ir: str) -> ast.AstNode:
        return self.parser.parse(ir)
