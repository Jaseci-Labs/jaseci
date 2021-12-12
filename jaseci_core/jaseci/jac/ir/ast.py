"""
AST for Jac
"""
from antlr4 import InputStream, CommonTokenStream, ParseTreeListener
from antlr4.error.ErrorListener import ErrorListener

from jaseci.utils.utils import logger, parse_str_token
from jaseci.jac.jac_parse.jacLexer import jacLexer
from jaseci.jac.jac_parse.jacParser import jacParser, ParseTreeWalker
import os


class ast():
    """
    AST Nodes

    The kind field is used to represent the grammar rule
    TODO: Error handling if jac program has errors
    """

    def __init__(self, jac_text=None, mod_name=None, imported=None,
                 parse_errors=None, start_rule='start'):
        self.name = 'unparsed'
        self.kind = 'unparsed'
        self.context = {}
        self.parse_errors = parse_errors if parse_errors else []
        self.start_rule = start_rule
        self.mod_name = mod_name if mod_name is not None else "@text_str"
        self.line = 0
        self.column = 0
        self.kid = []
        if(jac_text):
            if imported is None:
                imported = []
            self.parse_jac_str(jac_text, imported)

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

    def parse_jac_str(self, jac_str, imported):
        """Parse language and build ast from string"""
        input_stream = InputStream(jac_str)
        lexer = jacLexer(input_stream)
        stream = CommonTokenStream(lexer)
        errors = self.jac_tree_error(self)
        parser = jacParser(stream)
        parser.removeErrorListeners()
        parser.addErrorListener(errors)
        tree = getattr(parser, self.start_rule)()
        builder = self.jac_tree_builder(self, imported)
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

        def __init__(self, tree_root, imported):
            self.tree_root = tree_root
            self.node_stack = []
            self.imported = [tree_root.mod_name]+imported

        def run_import_module(self, jac_ast):
            """
            import_module: KW_IMPORT STRING SEMI;
            """
            kid = jac_ast.kid
            fn = parse_str_token(kid[1].token_text())
            mod_name = os.path.basename(fn)
            logger.info(f"{self.imported}")
            if(mod_name in self.imported):
                logger.error(
                    f"Already imported {mod_name}, may "
                    f"be circular from {self.tree_root.mod_name}")
            elif (os.path.isfile(fn)):
                with open(fn, 'r') as file:
                    jac_text = file.read()
                self.imported.append(mod_name)
                return filter(lambda x:
                              x.name == 'element',
                              ast(jac_text=jac_text,
                                  mod_name=mod_name,
                                  imported=self.imported).kid)
            else:
                err = f"Module not found for import! {mod_name} from" +\
                    f" {self.tree_root.mod_name}"
                self.tree_root.parse_errors.append(err)
            return []

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

            if(len(self.node_stack) and new_node.name != 'import_module'):
                self.node_stack[-1].kid.append(new_node)
            self.node_stack.append(new_node)

        def exitEveryRule(self, ctx):
            """Overloaded function that visits every node on exit"""
            top = self.node_stack.pop()
            if(top.name == 'import_module'):
                self.node_stack[-1].kid += self.run_import_module(top)

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
                f"{str(self.tree_root.mod_name)}: line {str(line)}:"
                f"{str(column)} - {self.tree_root} - {msg}"
            )
