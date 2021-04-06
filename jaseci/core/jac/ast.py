"""
AST for Jac
"""
from antlr4 import InputStream, CommonTokenStream, ParseTreeListener
from antlr4.error.ErrorListener import ErrorListener

from core.utils.utils import logger
from core.jac._jac_gen.jacLexer import jacLexer
from core.jac._jac_gen.jacParser import jacParser, ParseTreeWalker


class ast():
    """
    AST Nodes

    The kind field is used to represent the grammar rule
    TODO: Error handling if jac program has errors
    """

    def __init__(self, jac_text=None, parse_errors=None):
        self.name = None
        self.kind = None
        self.context = {}
        self.parse_errors = parse_errors if parse_errors else []
        self.line = 0
        self.column = 0
        self.kid = []
        if(jac_text):
            self.parse_jac_str(jac_text)

    def is_rule(self):
        """Returns true if node is a rule"""
        return self.kind == 'rule'

    def is_terminal(self):
        """Returns true if node is a terminal"""
        return self.kind == 'terminal'

    def token(self):
        if(not self.is_terminal()):
            logger.error(
                str(f"Non terminals (rules) don't have token info - {self}")
            )
            return None
        else:
            return self.context["token"]

    def token_text(self):
        if(self.is_terminal()):
            return self.token()['text']

    def token_symbol(self):
        if(self.is_terminal()):
            return self.token()['symbol']

    def parse_jac_file(self, jac_fn):
        """Parse language and build ast from jac file"""
        with open(jac_fn, 'r') as file:
            jac_str = file.read()
        self.parse_jac_str(jac_str)

    def parse_jac_str(self, jac_str):
        """Parse language and build ast from string"""
        input_stream = InputStream(jac_str)
        lexer = jacLexer(input_stream)
        stream = CommonTokenStream(lexer)
        errors = self.jac_tree_error(self)
        parser = jacParser(stream)
        parser.removeErrorListeners()
        parser.addErrorListener(errors)
        tree = parser.start()
        builder = self.jac_tree_builder(self)
        walker = ParseTreeWalker()
        walker.walk(builder, tree)

        if(self.parse_errors):
            for i in self.parse_errors:
                logger.error(
                    str(f"{i}")
                )
            logger.error(
                str(f"Above parse errors encountered - {self}")
            )

    def __str__(self):
        res = f'{self.kind}:{self.name}'
        if(self.is_terminal()):
            res += \
                f':{self.context["token"]["text"]}'
        return res

    def __repr__(self):
        return self.__str__()

    def get_tokens(self):
        """Return list of all tokens derived from this ast node"""
        tokens = []
        if('token' in self.context):
            tokens.append(self.context['token'])
            return tokens
        else:
            for i in self.kid:
                tokens = tokens + i.get_tokens()
        return tokens

    def get_text(self):
        """Get source text for this node"""
        ret = ''
        for i in self.get_tokens():
            ret += f"{i['text']} "
        return ret

    class jac_tree_builder(ParseTreeListener):
        """Converter class from Antlr trees to Jaseci Tree"""

        def __init__(self, tree_root):
            self.tree_root = tree_root
            self.node_stack = []

        def enterEveryRule(self, ctx):
            """Visits every node in antlr parse tree"""
            if(len(self.node_stack) == 0):
                new_node = self.tree_root
            else:
                new_node = ast()
            new_node.name = jacParser.ruleNames[ctx.getRuleIndex()]
            new_node.kind = 'rule'
            new_node.parse_errors = self.tree_root.parse_errors
            new_node.line = ctx.start.line
            new_node.column = ctx.start.column

            if(len(self.node_stack)):
                self.node_stack[-1].kid.append(new_node)
            self.node_stack.append(new_node)

        def exitEveryRule(self, ctx):
            """Overloaded function that visits every node on exit"""
            self.node_stack.pop()

        def visitTerminal(self, node):
            """Visits terminals as walker walks, adds ast node"""
            new_node = ast()
            new_node.name = jacParser.symbolicNames[node.getSymbol().type]
            new_node.kind = 'terminal'
            new_node.line = node.getSymbol().line
            new_node.column = node.getSymbol().column

            token = {
                'symbol':   jacParser.symbolicNames[node.getSymbol().type],
                'text':     node.getSymbol().text,
            }
            new_node.context['token'] = token

            self.node_stack[-1].kid.append(new_node)

    class jac_tree_error(ErrorListener):
        """Accumulate errors as parse tree is walked"""

        def __init__(self, tree_root):
            self.tree_root = tree_root

        def syntaxError(self, recognizer, offendingSymbol,
                        line, column, msg, e):
            """Add error to error list"""
            self.tree_root.parse_errors.append(
                f"{self.tree_root}: line {str(line)}: "
                f"{str(column)} - {msg}"
            )
