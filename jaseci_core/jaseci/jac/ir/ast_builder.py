import os
from antlr4 import ParseTreeListener
from antlr4.error.ErrorListener import ErrorListener
from jaseci.utils.utils import logger, parse_str_token
from jaseci.jac.jac_parse.jacParser import jacParser


class JacTreeBuilder(ParseTreeListener):
    """Converter class from Antlr trees to Jaseci Tree"""

    def __init__(self, tree_root):
        self.tree_root = tree_root
        self.ast_cls = type(tree_root)
        self.node_stack = []

    def run_import_module(self, jac_ast):
        """
        import_module:
            KW_IMPORT LBRACE (import_items | '*') RBRACE
            KW_WITH STRING SEMI;

        TODO: Check for duplicate imports and ignore if imported
        """
        kid = jac_ast.kid
        fn = os.path.join(
            self.tree_root._mod_dir, parse_str_token(kid[-2].token_text())
        )
        full_path = os.path.realpath(fn)
        mod_name = os.path.basename(fn)
        mdir = os.path.dirname(full_path) + "/"
        from_mod = self.tree_root.loc[2]
        logger.debug(f"Importing items from {mod_name} to {from_mod}...")
        parsed_ast = None
        if (mdir + mod_name) in self.ast_cls._ast_head_map.keys():
            parsed_ast = self.ast_cls._ast_head_map[mdir + mod_name]
        elif os.path.isfile(fn):
            with open(fn, "r") as file:
                jac_text = file.read()
            parsed_ast = self.ast_cls(
                jac_text=jac_text,
                mod_name=mod_name,
                mod_dir=mdir,
                fresh_start=False,
            )
        else:
            err = (
                f"Module not found for import! {mod_name} from" + f" {from_mod} - {fn}"
            )
            self.tree_root._parse_errors.append(err)
        if parsed_ast:
            self.tree_root._parse_errors += parsed_ast._parse_errors
            import_elements = list(
                filter(lambda x: x.name == "element", parsed_ast.kid)
            )
            if kid[2].name == "STAR_MUL":
                ret = import_elements
            else:
                ret = self.run_import_items(kid[2], import_elements)
            for i in ret:
                i._keep = True
            return ret
        else:
            return []

    def run_import_items(self, jac_ast, import_elements):
        """
        import_items:
            KW_WALKER (STAR_MUL | import_names) (COMMA import_items)?
            | KW_NODE (STAR_MUL | import_names) (COMMA import_items)?
            | KW_EDGE (STAR_MUL | import_names) (COMMA import_items)?
            | KW_GRAPH (STAR_MUL | import_names) (COMMA import_items)?
            | KW_GLOBAL (STAR_MUL | import_names) (COMMA import_items)?;
        """
        kid = jac_ast.kid
        ret_elements = list(
            filter(
                lambda x: x._keep or x.kid[0].kid[0].name == kid[0].name,
                import_elements,
            )
        )
        if kid[1].name == "import_names":
            import_names = self.run_import_names(kid[1])
            ret_elements = list(
                filter(
                    lambda x: x._keep or x.kid[0].kid[1].token_text() in import_names,
                    ret_elements,
                )
            )
            if len(ret_elements) < len(import_names):
                err = (
                    f"{kid[1].loc[2]}: Line {kid[1].loc[0]}: "
                    + "Module name not found!"
                )
                self.tree_root._parse_errors.append(err)

        if kid[-1].name == "import_items":
            return ret_elements + self.run_import_items(kid[-1], import_elements)

        return ret_elements

    def run_import_names(self, jac_ast):
        """
        import_names:
            DBL_COLON NAME
            | DBL_COLON LBRACE name_list RBRACE;
        """
        kid = jac_ast.kid
        if kid[1].name == "NAME":
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
            if i.name == "NAME":
                ret.append(i.token_text())
        return ret

    def enterEveryRule(self, ctx):  # noqa
        """Visits every node in antlr parse tree"""
        if len(self.node_stack) == 0:
            new_node = self.tree_root
        else:
            new_node = self.ast_cls(
                mod_name=self.tree_root.loc[2],
                mod_dir=self.tree_root._mod_dir,
                fresh_start=False,
            )
        new_node.name = jacParser.ruleNames[ctx.getRuleIndex()]
        new_node.kind = "rule"
        new_node._parse_errors = self.tree_root._parse_errors
        new_node.loc[0] = ctx.start.line
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
        new_node = self.ast_cls(
            mod_name=self.tree_root.loc[2],
            mod_dir=self.tree_root._mod_dir,
            fresh_start=False,
        )
        new_node.name = jacParser.symbolicNames[node.getSymbol().type]
        new_node.kind = "terminal"
        new_node.loc[0] = node.getSymbol().line
        new_node.loc[1] = node.getSymbol().column

        token = {
            "symbol": jacParser.symbolicNames[node.getSymbol().type],
            "text": node.getSymbol().text,
        }
        new_node.context["token"] = token

        self.node_stack[-1].kid.append(new_node)


class JacTreeError(ErrorListener):
    """Accumulate errors as parse tree is walked"""

    def __init__(self, tree_root):
        self.tree_root = tree_root

    def syntaxError(  # noqa
        self, recognizer, offendingSymbol, line, column, msg, e  # noqa
    ):
        """Add error to error list"""
        self.tree_root._parse_errors.append(
            f"{str(self.tree_root.loc[2])}: line {str(line)}:"
            f"{str(column)} - {self.tree_root} - {msg}"
        )
