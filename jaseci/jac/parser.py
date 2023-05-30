"""Parser for Jac."""
from jaseci.jac.lexer import JacLexer

from sly.yacc import Parser, YaccProduction

_ = None  # For flake8 linting


class JacParser(Parser):
    """Parser for Jac."""

    tokens = JacLexer.tokens
    debugfile = "parser.out"

    @_("element_list")
    def start(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Start rule."""
        print(type(p))
        return p

    @_(
        "element_list element",
        "",
    )
    def element_list(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Element list rule."""
        return p

    @_(
        "global_var",
        "architype",
        "test",
    )
    def element(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Element rule."""
        return p

    @_("KW_GLOBAL NAME global_var_tail SEMI")
    def global_var(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Global variable rule."""
        return p

    @_(
        "EQ expression global_var_tail",
        "COMMA NAME EQ expression global_var_tail",
        "",
    )
    def global_var_tail(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Global variable tail rule."""
        return p

    @_(
        "KW_NODE NAME sub_name_list attr_block",
        "KW_EDGE NAME sub_name_list attr_block",
        "KW_TYPE NAME sub_name_list attr_block",
        "KW_GRAPH NAME sub_name_list attr_block",
        "KW_WALKER NAME sub_name_list attr_block",
    )
    def architype(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Architype rule."""
        return p

    @_(
        "KW_TEST NAME multistring KW_WITH graph_ref KW_BY walker_ref spawn_ctx code_block"
    )
    def test(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Test rule."""
        return p

    @_(
        "LBRACE attr_stmt_list RBRACE",
        "COLON attr_stmt",
        "SEMI",
    )
    def attr_block(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Attribute block rule."""
        return p

    @_(
        "attr_stmt attr_stmt_list",
        "attr_stmt",
    )
    def attr_stmt_list(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Attribute statement list rule."""
        return p

    @_(
        "has_stmt",
        "can_stmt",
    )
    def attr_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Attribute statement rule."""
        return p

    @_("KW_HAS has_assign has_assign_list SEMI")
    def has_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Has statement rule."""
        return p

    @_(
        "COMMA has_assign has_assign_list",
        "",
    )
    def has_assign_list(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Has assign list rule."""
        return p

    @_(
        "has_tag NAME type_hint",
        "has_tag NAME type_hint EQ expression",
    )
    def has_assign(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Has assign rule."""
        return p

    @_(
        "KW_HIDDEN has_tag",
        "KW_ANCHOR has_tag",
        "",
    )
    def has_tag(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Has tag rule."""
        return p

    @_("COLON any_type")
    def type_hint(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Type hint rule."""
        return p

    @_("KW_CAN NAME event_clause code_block")
    def can_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Can statement rule."""
        return p

    @_(
        "KW_WITH name_list KW_ENTRY",
        "KW_WITH name_list KW_EXIT",
    )
    def event_clause(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Event clause rule."""
        return p

    @_(
        "NAME COMMA name_list",
        "NAME",
        "",
    )
    def name_list(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Name list rule."""
        return p

    @_(
        "expr_list",
        "kw_expr_list",
        "expr_list COMMA kw_expr_list",
        "",
    )
    def param_list(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Parameter list rule."""
        return p

    @_(
        "connect COMMA expr_list",
        "connect",
    )
    def expr_list(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Expression list rule."""
        return p

    @_(
        "NAME EQ connect COMMA kw_expr_list",
        "NAME EQ connect",
    )
    def kw_expr_list(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Keyword expression list rule."""
        return p

    @_(
        "LBRACE statement_list RBRACE",
        "COLON statement",
    )
    def code_block(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Code block rule."""
        return p

    @_(
        "statement statement_list",
        "statement",
    )
    def statement_list(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Statement list rule."""
        return p

    @_(
        "code_block",
        "expression SEMI",
        "if_stmt",
        "try_stmt",
        "for_stmt",
        "while_stmt",
        "assert_stmt SEMI",
        "ctrl_stmt SEMI",
        "delete_stmt SEMI",
        "report_stmt SEMI",
        "walker_stmt",
    )
    def statement(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Statement rule."""
        return p

    @_(
        "KW_IF expression code_block elif_stmt_list else_stmt",
        "KW_IF expression code_block elif_stmt_list",
    )
    def if_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """If statement rule."""
        return p

    @_(
        "KW_TRY code_block else_from_try",
        "KW_TRY code_block",
    )
    def try_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Try statement rule."""
        return p

    @_(
        "KW_ELSE KW_WITH NAME code_block",
        "KW_ELSE code_block",
    )
    def else_from_try(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Else from try rule."""
        return p

    @_(
        "KW_ELIF expression code_block",
        "KW_ELIF expression code_block elif_stmt_list",
    )
    def elif_stmt_list(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Else if statement list rule."""
        return p

    @_("KW_ELSE code_block")
    def else_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Else statement rule."""
        return p

    @_(
        "KW_FOR expression KW_TO expression KW_BY expression code_block",
        "KW_FOR NAME KW_IN expression code_block",
        "KW_FOR NAME COMMA NAME KW_IN expression code_block",
    )
    def for_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """For statement rule."""
        return p

    @_("KW_WHILE expression code_block")
    def while_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """While statement rule."""
        return p

    @_(
        "KW_CONTINUE",
        "KW_BREAK",
        "KW_SKIP",
    )
    def ctrl_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Control statement rule."""
        return p

    @_("KW_ASSERT expression")
    def assert_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Assert statement rule."""
        return p

    @_("KW_DELETE expression")
    def delete_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Delete statement rule."""
        return p

    @_(
        "KW_REPORT expression",
        "KW_REPORT sub_name EQ expression",
    )
    def report_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Report statement rule."""
        return p

    @_(
        "sub_name",
        "sub_name sub_name_list",
        "",
    )
    def sub_name_list(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Sub name list rule."""
        return p

    @_("COLON NAME")
    def sub_name(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Sub name rule."""
        return p

    @_(
        "ignore_stmt",
        "take_stmt",
        "disengage_stmt",
        "yield_stmt",
    )
    def walker_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Walker statement rule."""
        return p

    @_("KW_IGNORE expression SEMI")
    def ignore_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Ignore statement rule."""
        return p

    @_(
        "KW_TAKE expression SEMI",
        "KW_TAKE sub_name expression SEMI",
        "KW_TAKE expression else_stmt",
        "KW_TAKE sub_name expression else_stmt",
    )
    def take_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Take statement rule."""
        return p

    @_("KW_DISENGAGE SEMI")
    def disengage_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Disengage statement rule."""
        return p

    @_("KW_YIELD SEMI")
    def yield_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Yield statement rule."""
        return p

    @_(
        "connect",
        "connect assignment",
    )
    def expression(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Expression rule."""
        return p

    @_(
        "EQ expression",
        "CPY_EQ expression",
        "ADD_EQ expression",
        "SUB_EQ expression",
        "MUL_EQ expression",
        "DIV_EQ expression",
    )
    def assignment(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Production Assignment rule."""
        return p

    @_(
        "logical",
        "logical NOT edge_ref expression",
        "logical connect_op expression",
    )
    def connect(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Connect rule."""
        return p

    @_(
        "compare",
        "compare KW_AND logical",
        "compare KW_OR logical",
    )
    def logical(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Logical rule."""
        return p

    @_(
        "NOT arithmetic",
        "compare cmp_op arithmetic",
    )
    def compare(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Compare rule."""
        return p

    @_(
        "EE",
        "LT",
        "GT",
        "LTE",
        "GTE",
        "NE",
        "KW_IN",
        "NOT KW_IN",
    )
    def cmp_op(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Compare operator rule."""
        return p

    @_(
        "term",
        "term PLUS arithmetic",
        "term MINUS arithmetic",
    )
    def arithmetic(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Arithmetic rule."""
        return p

    @_(
        "factor",
        "factor STAR_MUL term",
        "factor DIV term",
        "factor MOD term",
    )
    def term(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Term rule."""
        return p

    @_(
        "PLUS factor",
        "MINUS factor",
        "power",
    )
    def factor(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Factor rule."""
        return p

    @_(
        "atom",
        "atom POW factor",
    )
    def power(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Power rule."""
        return p

    @_(
        "KW_GLOBAL DOT obj_built_in",
        "KW_GLOBAL DOT NAME",
    )
    def global_ref(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Global reference rule."""
        return p

    @_(
        "INT",
        "FLOAT",
        "multistring",
        "BOOL",
        "NULL",
        "NAME",
        "global_ref",
        "node_edge_ref",
        "list_val",
        "dict_val",
        "LPAREN expression RPAREN",
        "ability_op NAME spawn_ctx",
        "atom atom_trailer",
        "KW_SYNC atom",
        "spawn",
        "ref",
        "deref",
        "any_type",
    )
    def atom(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Atom rule."""
        return p

    @_(
        "DOT built_in",
        "DOT NAME",
        "index_slice",
        "ability_call",
    )
    def atom_trailer(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Atom trailer rule."""
        return p

    @_(
        "LPAREN param_list RPAREN",
        "ability_op NAME spawn_ctx",
    )
    def ability_call(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Ability call rule."""
        return p

    @_(
        "DBL_COLON",
        "DBL_COLON NAME COLON",
    )
    def ability_op(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Ability operator rule."""
        return p

    @_("KW_REF atom")
    def ref(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Production for reference rule."""
        return p

    @_("STAR_MUL atom")
    def deref(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Dereference rule."""
        return p

    @_(
        "string_built_in",
        "dict_built_in",
        "list_built_in",
        "obj_built_in",
        "cast_built_in",
    )
    def built_in(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Built-in rule."""
        return p

    @_("any_type")
    def cast_built_in(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Cast built-in rule."""
        return p

    @_(
        "KW_CONTEXT",
        "KW_INFO",
        "KW_DETAILS",
    )
    def obj_built_in(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Object built-in rule."""
        return p

    @_(
        "TYP_DICT DBL_COLON NAME",
        "TYP_DICT DBL_COLON NAME LPAREN expr_list RPAREN",
    )
    def dict_built_in(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Production for dictionary built-in rule."""
        return p

    @_(
        "TYP_LIST DBL_COLON NAME",
        "TYP_LIST DBL_COLON NAME LPAREN expr_list RPAREN",
    )
    def list_built_in(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """List built-in rule."""
        return p

    @_(
        "TYP_STRING DBL_COLON NAME",
        "TYP_STRING DBL_COLON NAME LPAREN expr_list RPAREN",
    )
    def string_built_in(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Production for string built-in rule."""
        return p

    @_(
        "node_ref filter_ctx",
        "edge_ref",
        "node_ref filter_ctx node_edge_ref",
        "edge_ref node_edge_ref",
    )
    def node_edge_ref(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Node/edge reference rule."""
        return p

    @_("KW_NODE DBL_COLON NAME")
    def node_ref(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Node reference rule."""
        return p

    @_("KW_WALKER DBL_COLON NAME")
    def walker_ref(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Walker reference rule."""
        return p

    @_("KW_GRAPH DBL_COLON NAME")
    def graph_ref(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Graph reference rule."""
        return p

    @_("KW_TYPE DBL_COLON NAME")
    def type_ref(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Type reference rule."""
        return p

    @_(
        "edge_to",
        "edge_from",
        "edge_any",
    )
    def edge_ref(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Edge reference rule."""
        return p

    @_(
        "ARROW_R",
        "ARROW_R_p1 NAME filter_ctx ARROW_R_p2",
    )
    def edge_to(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Edge to rule."""
        return p

    @_(
        "ARROW_L",
        "ARROW_L_p1 NAME filter_ctx ARROW_L_p2",
    )
    def edge_from(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Edge from rule."""
        return p

    @_(
        "ARROW_BI",
        "ARROW_L_p1 NAME filter_ctx ARROW_R_p2",
    )
    def edge_any(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Edge any rule."""
        return p

    @_(
        "connect_to",
        "connect_from",
        "connect_any",
    )
    def connect_op(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Connect operator rule."""
        return p

    @_(
        "CARROW_R",
        "CARROW_R_p1 NAME filter_ctx CARROW_R_p2",
    )
    def connect_to(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Connect to rule."""
        return p

    @_(
        "CARROW_L",
        "CARROW_L_p1 NAME filter_ctx CARROW_L_p2",
    )
    def connect_from(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Connect from rule."""
        return p

    @_(
        "CARROW_BI",
        "CARROW_L_p1 NAME filter_ctx CARROW_R_p2",
    )
    def connect_any(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Connect any rule."""
        return p

    @_(
        "LSQUARE RSQUARE",
        "LSQUARE expr_list RSQUARE",
    )
    def list_val(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """List value rule."""
        return p

    @_(
        "LSQUARE expression RSQUARE",
        "LSQUARE expression COLON expression RSQUARE",
    )
    def index_slice(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Index/slice rule."""
        return p

    @_("LBRACE kv_pairs RBRACE")
    def dict_val(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Production for dictionary value rule."""
        return p

    @_(
        "expression COLON expression",
        "expression COLON expression COMMA kv_pairs",
        "",
    )
    def kv_pairs(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Key/value pairs rule."""
        return p

    @_("KW_SPAWN spawn_object")
    def spawn(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Spawn rule."""
        return p

    @_(
        "node_spawn",
        "walker_spawn",
        "graph_spawn",
        "type_spawn",
    )
    def spawn_object(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Spawn object rule."""
        return p

    @_("expression connect_op")
    def spawn_edge(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Spawn edge rule."""
        return p

    @_(
        "node_ref spawn_ctx",
        "spawn_edge node_ref spawn_ctx",
    )
    def node_spawn(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Node spawn rule."""
        return p

    @_(
        "graph_ref",
        "spawn_edge graph_ref",
    )
    def graph_spawn(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Graph spawn rule."""
        return p

    @_(
        "expression walker_ref spawn_ctx",
        "expression KW_SYNC walker_ref spawn_ctx",
    )
    def walker_spawn(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Walker spawn rule."""
        return p

    @_("type_ref spawn_ctx")
    def type_spawn(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Type spawn rule."""
        return p

    @_(
        "LPAREN spawn_assign_list RPAREN",
        "",
    )
    def spawn_ctx(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Spawn context rule."""
        return p

    @_(
        "LPAREN filter_compare_list RPAREN",
        "",
    )
    def filter_ctx(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Filter context rule."""
        return p

    @_(
        "NAME EQ expression",
        "NAME EQ expression COMMA spawn_assign_list",
        "",
    )
    def spawn_assign_list(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Spawn assignment list rule."""
        return p

    @_(
        "NAME cmp_op expression",
        "NAME cmp_op expression COMMA filter_compare_list",
        "",
    )
    def filter_compare_list(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Filter comparison list rule."""
        return p

    @_(
        "TYP_STRING",
        "TYP_BYTES",
        "TYP_INT",
        "TYP_FLOAT",
        "TYP_LIST",
        "TYP_DICT",
        "TYP_BOOL",
        "KW_NODE",
        "KW_EDGE",
        "KW_TYPE",
    )
    def any_type(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Any type rule."""
        return p

    @_(
        "STRING multistring",
        "STRING",
    )
    def multistring(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Multistring rule."""
        return p
