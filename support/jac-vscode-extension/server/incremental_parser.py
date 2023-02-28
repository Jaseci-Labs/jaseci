import pdb
from antlr4 import *
from jaseci.jac.ir.ast_builder import JacAstBuilder
from jaseci.jac.ir.passes import IrPass


class SymbolParser:
    symbols_map = {}

    def __init__(self, ast: JacAstBuilder):
        self.ast = ast
        self.symbols = []
        self.symbols_map = {}
        self._parse_symbols()
