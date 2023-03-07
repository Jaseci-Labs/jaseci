import os
from antlr4 import ParseTreeListener
from antlr4.error.ErrorListener import ErrorListener
from jaseci.utils.utils import logger, parse_str_token
from jaseci.jac.jac_parse.jacParser import jacParser, ParseTreeWalker
from jaseci.jac.jac_parse.jacLexer import jacLexer
from antlr4 import InputStream, CommonTokenStream
from jaseci.jac.ir.ast import Ast


class JacAstBuilder:
    """
    Jac Code to AST Tree
    """

    _ast_head_map = {}

    def __init__(
        self,
        mod_name,
        mod_dir="./",
        jac_text=None,
        start_rule="start",
    ):
        self.root = Ast(mod_name)
        self._parse_errors = []
        self._start_rule = start_rule
        self._mod_dir = mod_dir
        self.dependencies = []
        if jac_text:
            self.jac_code_to_ast(jac_text)

    def jac_code_to_ast(self, jac_str):
        """Parse language and build ast from string"""
        JacAstBuilder._ast_head_map[self._mod_dir + self.root.loc[2]] = self
        input_stream = InputStream(jac_str)
        lexer = jacLexer(input_stream)
        stream = CommonTokenStream(lexer)
        errors = JacTreeError(self)
        parser = jacParser(stream)
        parser.removeErrorListeners()
        parser.addErrorListener(errors)
        tree = getattr(parser, self._start_rule)()
        builder = JacTreeBuilder(builder=self, code=jac_str)
        walker = ParseTreeWalker()
        walker.walk(builder, tree)

        if self._parse_errors:
            logger.error(str(f"Parse errors encountered - {self}"))


class JacTreeBuilder(ParseTreeListener):
    """Converter class from Antlr trees to Jaseci Tree"""

    def __init__(self, builder, code):
        self.builder = builder
        self.code = code
        self.node_stack = []

    def run_import_module(self, jac_ast):
        """
        import_module:
            KW_IMPORT LBRACE (import_items | '*') RBRACE
            KW_WITH STRING SEMI;

        TODO: Check for duplicate imports and ignore if imported
        """
        kid = jac_ast.kid
        fn = os.path.join(self.builder._mod_dir, parse_str_token(kid[-2].token_text()))
        full_path = os.path.realpath(fn)
        mod_name = os.path.basename(fn)
        mdir = os.path.dirname(full_path) + "/"
        from_mod = self.builder.root.loc[2]
        logger.debug(f"Importing items from {mod_name} to {from_mod}...")
        pre_build = None
        if (mdir + mod_name) in JacAstBuilder._ast_head_map.keys():
            pre_build = JacAstBuilder._ast_head_map[mdir + mod_name]
        elif os.path.isfile(fn):
            with open(fn, "r") as file:
                jac_text = file.read()
            pre_build = JacAstBuilder(
                jac_text=jac_text,
                mod_name=mod_name,
                mod_dir=mdir,
            )
        else:
            err = (
                f"Module not found for import! {mod_name} from" + f" {from_mod} - {fn}"
            )
            self.builder._parse_errors.append(err)
        if pre_build:
            self.builder._parse_errors += pre_build._parse_errors
            self.builder.dependencies += pre_build.dependencies
            import_elements = list(
                filter(lambda x: x.name == "element", pre_build.root.kid)
            )
            if kid[2].name == "STAR_MUL":
                ret = import_elements
            else:
                ret = self.run_import_items(kid[2], import_elements)
            for i in ret:
                self.builder.dependencies.append(i)
            return ret
        else:
            return []

    def run_import_items(self, jac_ast, import_elements):
        """
        import_items:
            WALKER_DBL_COLON (STAR_MUL | import_names) (
                COMMA import_items
            )?
            | NODE_DBL_COLON (STAR_MUL | import_names) (
                COMMA import_items
            )?
            | EDGE_DBL_COLON (STAR_MUL | import_names) (
                COMMA import_items
            )?
            | GRAPH_DBL_COLON (STAR_MUL | import_names) (
                COMMA import_items
            )?
            | KW_GLOBAL DBL_COLON (STAR_MUL | import_names) (
                COMMA import_items
            )?
            | TYPE_DBL_COLON (STAR_MUL | import_names) (
                COMMA import_items
            )?;
        """
        kid = jac_ast.kid
        type_name = (
            "KW_" + kid[0].name.split("_")[0]
            if not kid[0].name.startswith("KW_")
            else kid[0].name
        )
        kid = kid[2:] if kid[1].name == "DBL_COLON" else kid[1:]
        ret_elements = list(
            filter(
                lambda x: x in self.builder.dependencies
                or x.kid[0].kid[0].name == type_name,
                import_elements,
            )
        )
        if kid[0].name == "import_names":
            import_names = self.run_import_names(kid[0])
            ret_elements = list(
                filter(
                    lambda x: x in self.builder.dependencies
                    or x.kid[0].kid[1].token_text() in import_names,
                    ret_elements,
                )
            )
            if len(ret_elements) < len(import_names):
                err = (
                    f"{kid[0].loc[2]}: Line {kid[0].loc[0]}: "
                    + "Module name not found!"
                )
                self.builder._parse_errors.append(err)

        if kid[-1].name == "import_items":
            return ret_elements + self.run_import_items(kid[-1], import_elements)

        return ret_elements

    def run_import_names(self, jac_ast):
        """
        import_names: NAME | LBRACE name_list RBRACE;
        """
        kid = jac_ast.kid
        if kid[0].name == "NAME":
            return [kid[0].token_text()]
        else:
            return self.run_name_list(kid[1])

    def run_name_list(self, jac_ast):
        """
        name_list: NAME (COMMA NAME)*;
        """
        kid = jac_ast.kid
        ret = []
        for i in kid:
            if i.name == "NAME":
                ret.append(i.token_text())
        return ret

    def enterEveryRule(self, ctx):  # noqa
        """Visits every node in antlr parse tree"""
        if len(self.node_stack) == 0:
            new_node = self.builder.root
        else:
            new_node = Ast(mod_name=self.builder.root.loc[2])
        new_node.name = jacParser.ruleNames[ctx.getRuleIndex()]
        new_node.loc[0] = ctx.start.line
        if new_node.name == "architype":
            new_node.src = self.get_code(ctx)
        new_node.loc[1] = ctx.start.column

        if len(self.node_stack) and new_node.name != "import_module":
            self.node_stack[-1].kid.append(new_node)
        self.node_stack.append(new_node)

    def exitEveryRule(self, ctx):  # noqa
        """Overloaded function that visits every node on exit"""
        top = self.node_stack.pop()
        if top.name == "import_module":
            for i in self.run_import_module(top):
                if i not in self.node_stack[-1].kid:
                    self.node_stack[-1].kid.append(i)

    def visitTerminal(self, node):  # noqa
        """Visits terminals as walker walks, adds ast node"""
        new_node = Ast(mod_name=self.builder.root.loc[2])
        new_node.name = jacParser.symbolicNames[node.getSymbol().type]
        new_node.loc[0] = node.getSymbol().line
        new_node.loc[1] = node.getSymbol().column

        token = {
            "symbol": jacParser.symbolicNames[node.getSymbol().type],
            "text": node.getSymbol().text,
        }
        new_node.loc[3]["token"] = token

        self.node_stack[-1].kid.append(new_node)

    def get_code(self, ctx):
        out = ""
        lines = self.code.split("\n")

        for idx, i in enumerate(lines[ctx.start.line - 1 : ctx.stop.line]):
            out += i
            if idx != ctx.stop.line - 1:
                out += "\n"

        return out


class JacTreeError(ErrorListener):
    """Accumulate errors as parse tree is walked"""

    def __init__(self, builder):
        self.builder = builder

    def syntaxError(  # noqa
        self, recognizer, offendingSymbol, line, column, msg, e  # noqa
    ):
        """Add error to error list"""
        root = self.builder.root
        self.builder._parse_errors.append(
            f"{str(root.loc[2])}: line {str(line)}:" f"{str(column)} - {root} - {msg}"
        )
