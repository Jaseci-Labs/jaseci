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

    _ast_head_map = {}

    def __init__(self, mod_name, jac_text=None,
                 parse_errors=None, start_rule='start', fresh_start=True):
        if(fresh_start):
            ast._ast_head_map = {}
        self.name = 'unparsed'
        self.kind = 'unparsed'
        self.context = {}
        self._parse_errors = parse_errors if parse_errors else []
        self._start_rule = start_rule
        self.mod_name = mod_name if mod_name is not None else "@default"
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

    def parse_jac_str(self, jac_str):
        """Parse language and build ast from string"""
        ast._ast_head_map[self.mod_name] = self
        input_stream = InputStream(jac_str)
        lexer = jacLexer(input_stream)
        stream = CommonTokenStream(lexer)
        errors = self.jac_tree_error(self)
        parser = jacParser(stream)
        parser.removeErrorListeners()
        parser.addErrorListener(errors)
        tree = getattr(parser, self._start_rule)()
        builder = self.jac_tree_builder(self)
        walker = ParseTreeWalker()
        walker.walk(builder, tree)

        if(self._parse_errors):
            logger.error(
                str(f"Parse errors encountered - {self}")
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

        def run_import_module(self, jac_ast):
            """
            import_module:
                KW_IMPORT LBRACE (import_items | '*') RBRACE
                KW_WITH STRING SEMI;

            TODO: Check for duplicate imports and ignore if imported
            """
            kid = jac_ast.kid
            fn = parse_str_token(kid[-2].token_text())
            mod_name = fn
            from_mod = self.tree_root.mod_name
            logger.debug(f"Importing items from {mod_name} to {from_mod}...")
            parsed_ast = None
            if(mod_name in ast._ast_head_map.keys()):
                parsed_ast = ast._ast_head_map[mod_name]
            elif(os.path.isfile(fn)):
                with open(fn, 'r') as file:
                    jac_text = file.read()
                parsed_ast = ast(jac_text=jac_text, mod_name=mod_name,
                                 fresh_start=False)
            else:
                err = f"Module not found for import! {mod_name} from" +\
                    f" {from_mod}"
                self.tree_root._parse_errors.append(err)
            if(parsed_ast):
                self.tree_root._parse_errors += parsed_ast._parse_errors
            import_elements = list(filter(lambda x:
                                          x.name == 'element',
                                          parsed_ast.kid))
            if(kid[2].name == 'STAR_MUL'):
                return import_elements
            else:
                return self.run_import_items(
                    kid[2], import_elements)

        def run_import_items(self, jac_ast, import_elements):
            """
            import_items:
                KW_WALKER (STAR_MUL | import_names) (COMMA import_items)?
                | KW_NODE (STAR_MUL | import_names) (COMMA import_items)?
                | KW_EDGE (STAR_MUL | import_names) (COMMA import_items)?
                | KW_GRAPH (STAR_MUL | import_names) (COMMA import_items)?;
            """
            kid = jac_ast.kid
            ret_elements = list(filter(lambda x:
                                       x.kid[0].kid[0].name == kid[0].name,
                                       import_elements))
            if(kid[1].name == "import_names"):
                ret_elements = list(filter(lambda x:
                                           x.kid[0].kid[1].token_text() in
                                           self.run_import_names(kid[1]),
                                           ret_elements))
            if(kid[-1].name == "import_items"):
                return ret_elements + self.run_import_items(kid[-1],
                                                            import_elements)

            return ret_elements

        def run_import_names(self, jac_ast):
            """
            import_names:
                DBL_COLON NAME
                | DBL_COLON LBRACE name_list RBRACE;
            """
            kid = jac_ast.kid
            if(kid[1].name == "NAME"):
                return [kid[1].token_text()]
            else:
                return self.run_name_list(kid[2])

        def run_name_list(self, jac_ast):
            """
            name_list: NAME (COMMA NAME)*;
            """
            kid = jac_ast.kid
            ret = []
            for i in kid:
                if(i.name == 'NAME'):
                    ret.append(i.token_text())
            return ret

        def enterEveryRule(self, ctx):
            """Visits every node in antlr parse tree"""
            if(len(self.node_stack) == 0):
                new_node = self.tree_root
            else:
                new_node = ast(mod_name=self.tree_root.mod_name,
                               fresh_start=False)
            new_node.name = jacParser.ruleNames[ctx.getRuleIndex()]
            new_node.kind = 'rule'
            new_node._parse_errors = self.tree_root._parse_errors
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
            new_node = ast(mod_name=self.tree_root.mod_name, fresh_start=False)
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
            self.tree_root._parse_errors.append(
                f"{str(self.tree_root.mod_name)}: line {str(line)}:"
                f"{str(column)} - {self.tree_root} - {msg}"
            )
