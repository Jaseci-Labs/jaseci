from jaseci.jac.ir.ast_builder import (
    JacAstBuilder,
)
from jaseci.jac.jac_parse.jacParser import jacParser, ParseTreeWalker
from jaseci.jac.jac_parse.jacLexer import jacLexer
from jaseci.jac.ir.ast_builder import JacTreeBuilder
from antlr4 import (
    InputStream,
    CommonTokenStream,
    PredictionMode,
)
from antlr4.error.Errors import ParseCancellationException


class JacAstBuilderSLL(JacAstBuilder):
    def __init__(
        self,
        mod_name,
        jac_text,
        mod_dir="./",
    ):
        super().__init__(mod_name, jac_text=jac_text, mod_dir=mod_dir)

    def jac_code_to_ast(self, jac_str):
        """Parse language and build ast from string"""
        JacAstBuilder._ast_head_map[self._mod_dir + self.root.loc[2]] = self
        input_stream = InputStream(jac_str)
        lexer = jacLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = jacParser(stream)
        # set a prediction mode based on performance and accuracy needs
        parser._interp.predictionMode = PredictionMode.SLL
        parser.removeErrorListeners()
        tree = getattr(parser, self._start_rule)()
        builder = JacTreeBuilder(builder=self, code=jac_str)
        walker = ParseTreeWalker()
        walker.walk(builder, tree)

    # def prepare_imports(self):
    # self.builder.run_import_module(self.root)
