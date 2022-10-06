"""
AST for Jac
"""
from antlr4 import InputStream, CommonTokenStream
from jaseci.jac.jac_parse.jacLexer import jacLexer
from jaseci.jac.jac_parse.jacParser import jacParser, ParseTreeWalker
from jaseci.utils.utils import logger
from jaseci.jac.ir.ast_builder import JacTreeBuilder, JacTreeError


class Ast:
    """
    AST Nodes

    The kind field is used to represent the grammar rule
    TODO: Error handling if jac program has errors
    """

    _ast_head_map = {}

    def __init__(
        self,
        mod_name,
        mod_dir="./",
        jac_text=None,
        parse_errors=None,
        start_rule="start",
        fresh_start=True,
    ):
        if fresh_start:
            Ast._ast_head_map = {}
        self.name = "unparsed"
        self.kind = "unparsed"
        self.context = {}
        self._parse_errors = parse_errors if parse_errors else []
        self._start_rule = start_rule
        self.mod_name = mod_name if mod_name is not None else "@default"
        self._mod_dir = mod_dir
        self._keep = False
        self.line = 0
        self.column = 0
        self.kid = []
        if jac_text:
            self.parse_jac_str(jac_text)

    def parse_jac_str(self, jac_str):
        """Parse language and build ast from string"""
        Ast._ast_head_map[self._mod_dir + self.mod_name] = self
        input_stream = InputStream(jac_str)
        lexer = jacLexer(input_stream)
        stream = CommonTokenStream(lexer)
        errors = JacTreeError(self)
        parser = jacParser(stream)
        parser.removeErrorListeners()
        parser.addErrorListener(errors)
        tree = getattr(parser, self._start_rule)()
        builder = JacTreeBuilder(self)
        walker = ParseTreeWalker()
        walker.walk(builder, tree)

        if self._parse_errors:
            logger.error(str(f"Parse errors encountered - {self}"))

    def is_rule(self):
        """Returns true if node is a rule"""
        return self.kind == "rule"

    def is_terminal(self):
        """Returns true if node is a terminal"""
        return self.kind == "terminal"

    def token(self):
        if not self.is_terminal():
            logger.error(str(f"Non terminals (rules) don't have token info - {self}"))
            return None
        else:
            return self.context["token"]

    def token_text(self):
        if self.is_terminal():
            return self.token()["text"]

    def token_symbol(self):
        if self.is_terminal():
            return self.token()["symbol"]

    def __str__(self):
        res = f"{self.kind}:{self.name}"
        if self.is_terminal():
            res += f':{self.context["token"]["text"]}'
        return res

    def __repr__(self):
        return self.__str__()

    def get_tokens(self):
        """Return list of all tokens derived from this ast node"""
        tokens = []
        if "token" in self.context:
            tokens.append(self.context["token"])
            return tokens
        else:
            for i in self.kid:
                tokens = tokens + i.get_tokens()
        return tokens

    def get_text(self):
        """Get source text for this node"""
        ret = ""
        for i in self.get_tokens():
            ret += f"{i['text']} "
        return ret
