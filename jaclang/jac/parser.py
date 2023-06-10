"""Parser for Jac."""
from jaclang.jac.errors import JacParseErrorMixIn
from jaclang.jac.lexer import JacLexer
from jaclang.utils.sly.yacc import Parser, YaccProduction

_ = None  # For flake8 linting


class JacParser(JacParseErrorMixIn, Parser):
    """Parser for Jac."""

    tokens = JacLexer.tokens
    debugfile = "parser.out"

    # All mighty start rule
    # ---------------------
    @_("element_list")
    def start(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Start rule."""
        return p

    # Jac program structured as a list of elements
    # --------------------------------------------
    @_(
        "element",
        "element_list element",
    )
    def element_list(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Element list rule."""
        return p

    # Element types
    # -------------
    @_(
        "DOC_STRING",
        "global_var",
        "test",
        "import_stmt",
        "architype",
        "ability_spec",
    )
    def element(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Element rule."""
        return p

    @_("access_tag KW_GLOBAL global_var_clause SEMI")
    def global_var(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Global variable rule."""
        return p

    @_(
        "KW_PRIV COLON",
        "KW_PUB COLON",
        "KW_PROT COLON",
        "empty",
    )
    def access_tag(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Permission tag rule."""
        return p

    @_(
        "NAME EQ expression",
        "global_var_clause COMMA NAME EQ expression",
    )
    def global_var_clause(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Global variable tail rule."""
        return p

    @_("KW_TEST NAME multistring code_block")
    def test(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Test rule."""
        return p

    # Import Statements
    # -----------------
    @_(
        "KW_IMPORT sub_name import_path SEMI",
        "KW_IMPORT sub_name import_path KW_AS NAME SEMI",
        "KW_IMPORT sub_name KW_FROM import_path COMMA name_as_list SEMI",
    )
    def import_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Import rule."""
        return p

    @_(
        "import_path_prefix",
        "import_path_prefix import_path_tail",
    )
    def import_path(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Import path rule."""
        return p

    @_(
        "NAME",
        "DOT NAME",
        "DOT DOT NAME",
    )
    def import_path_prefix(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Import path prefix rule."""
        return p

    @_(
        "DOT NAME",
        "import_path_tail DOT NAME",
    )
    def import_path_tail(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Import path tail rule."""
        return p

    @_(
        "NAME",
        "NAME KW_AS NAME",
        "name_as_list COMMA NAME",
        "name_as_list COMMA NAME KW_AS NAME",
    )
    def name_as_list(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Name as list rule."""
        return p

    # Architype elements
    # ------------------
    @_(
        "access_tag KW_NODE NAME arch_decl_tail",
        "access_tag KW_EDGE NAME arch_decl_tail",
        "access_tag KW_OBJECT NAME arch_decl_tail",
        "access_tag KW_WALKER NAME arch_decl_tail",
        "access_tag KW_SPAWNER NAME code_block",
    )
    def architype(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Architype rule."""
        return p

    @_(
        "member_block",
        "inherited_archs member_block",
    )
    def arch_decl_tail(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Architype tail rule."""
        return p

    @_(
        "sub_name",
        "inherited_archs sub_name",
    )
    def inherited_archs(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Sub name list rule."""
        return p

    @_("COLON NAME")
    def sub_name(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Sub name rule."""
        return p

    @_(
        "arch_ref ability_ref code_block",
        "arch_ref ability_ref func_decl code_block",
        "NAME arch_ref ability_ref code_block",
        "NAME arch_ref ability_ref func_decl code_block",
    )
    def ability_spec(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Ability rule."""
        return p

    # Attribute blocks
    # ----------------
    @_(
        "LBRACE RBRACE",
        "LBRACE member_stmt_list RBRACE",
        "SEMI",
    )
    def member_block(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Attribute block rule."""
        return p

    @_(
        "member_stmt",
        "member_stmt_list member_stmt",
    )
    def member_stmt_list(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Attribute statement list rule."""
        return p

    @_(
        "has_stmt",
        "can_stmt",
        "DOC_STRING",
    )
    def member_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Attribute statement rule."""
        return p

    # Has statements
    # --------------
    @_("access_tag KW_HAS has_assign_clause SEMI")
    def has_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Has statement rule."""
        return p

    @_(
        "typed_has",
        "has_assign_clause COMMA typed_has",
    )
    def has_assign_clause(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Has assign list rule."""
        return p

    @_(
        "has_tag NAME type_spec",
        "has_tag NAME type_spec EQ expression",
    )
    def typed_has(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Parameter variable rule rule."""
        return p

    @_(
        "has_tag KW_HIDDEN",
        "has_tag KW_ANCHOR",
        "empty",
    )
    def has_tag(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Has tag rule."""
        return p

    @_("COLON type_name")
    def type_spec(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Type hint rule."""
        return p

    @_(
        "builtin_type",
        "NULL",
        "NAME",
        "TYP_LIST LSQUARE type_name RSQUARE",
        "TYP_DICT LSQUARE type_name COMMA type_name RSQUARE",
    )
    def type_name(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Type hint rule."""
        return p

    @_(
        "TYP_STRING",
        "TYP_BYTES",
        "TYP_INT",
        "TYP_FLOAT",
        "TYP_LIST",
        "TYP_TUPLE",
        "TYP_SET",
        "TYP_DICT",
        "TYP_BOOL",
        "TYP_TYPE",
    )
    def builtin_type(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Any type rule."""
        return p

    # Can statements
    # --------------
    @_(
        "access_tag can_ds_ability",
        "access_tag can_func_ability",
    )
    def can_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Can statement rule."""
        return p

    @_(
        "KW_CAN NAME code_block",
        "KW_CAN NAME SEMI",
        "KW_CAN NAME event_clause code_block",
        "KW_CAN NAME event_clause SEMI",
    )
    def can_ds_ability(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Can statement rule."""
        return p

    @_(
        "KW_CAN NAME func_decl code_block",
        "KW_CAN NAME func_decl SEMI",
    )
    def can_func_ability(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Can statement rule."""
        return p

    @_(
        "KW_WITH KW_ENTRY",
        "KW_WITH KW_EXIT",
        "KW_WITH STAR_MUL KW_ENTRY",
        "KW_WITH STAR_MUL KW_EXIT",
        "KW_WITH name_list KW_ENTRY",
        "KW_WITH name_list KW_EXIT",
    )
    def event_clause(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Event clause rule."""
        return p

    @_(
        "LPAREN RPAREN type_spec",
        "LPAREN func_decl_param_list RPAREN type_spec",
    )
    def func_decl(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Func declaration parameter rule."""
        return p

    @_(
        "param_var",
        "func_decl_param_list COMMA param_var",
    )
    def func_decl_param_list(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Func declaration parameters list rule."""
        return p

    @_(
        "NAME type_spec",
        "NAME type_spec EQ expression",
    )
    def param_var(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Parameter variable rule rule."""
        return p

    @_(
        "NAME",
        "name_list COMMA NAME",
    )
    def name_list(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Name list rule."""
        return p

    @_(
        "LBRACE RBRACE",
        "LBRACE statement_list RBRACE",
    )
    def code_block(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Code block rule."""
        return p

    # Codeblock statements
    # --------------------
    @_(
        "statement statement_list",
        "statement",
    )
    def statement_list(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Statement list rule."""
        return p

    @_(
        "assignment SEMI",
        "expression SEMI",
        "if_stmt",
        "try_stmt",
        "for_stmt",
        "while_stmt",
        "assert_stmt SEMI",
        "ctrl_stmt SEMI",
        "delete_stmt SEMI",
        "report_stmt SEMI",
        "return_stmt SEMI",
        "walker_stmt",
    )
    def statement(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Statement rule."""
        return p

    @_(
        "KW_IF expression code_block",
        "KW_IF expression code_block else_stmt",
        "KW_IF expression code_block elif_stmt_list else_stmt",
    )
    def if_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """If statement rule."""
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
        "KW_TRY code_block",
        "KW_TRY code_block else_from_try",
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
        "KW_FOR assignment KW_TO expression KW_BY expression code_block",
        "KW_FOR atom KW_IN expression code_block",
        "KW_FOR atom COMMA atom KW_IN expression code_block",
    )
    def for_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """For statement rule."""
        return p

    @_("KW_WHILE expression code_block")
    def while_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """While statement rule."""
        return p

    @_("KW_ASSERT expression")
    def assert_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Assert statement rule."""
        return p

    @_(
        "KW_CONTINUE",
        "KW_BREAK",
        "KW_SKIP",
    )
    def ctrl_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Control statement rule."""
        return p

    @_("KW_DELETE expression")
    def delete_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Delete statement rule."""
        return p

    @_(
        "KW_REPORT expression",
    )
    def report_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Report statement rule."""
        return p

    @_(
        "KW_RETURN expression",
    )
    def return_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Report statement rule."""
        return p

    @_(
        "ignore_stmt",
        "visit_stmt",
        "revisit_stmt",
        "disengage_stmt",
        "yield_stmt",
        "sync_stmt",
    )
    def walker_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Walker statement rule."""
        return p

    @_("KW_IGNORE expression SEMI")
    def ignore_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Ignore statement rule."""
        return p

    @_(
        "KW_VISIT expression SEMI",
        "KW_VISIT sub_name expression SEMI",
        "KW_VISIT expression else_stmt",
        "KW_VISIT sub_name expression else_stmt",
    )
    def visit_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Visit statement rule."""
        return p

    @_(
        "KW_REVISIT SEMI",
        "KW_REVISIT expression SEMI",
        "KW_REVISIT else_stmt",
        "KW_REVISIT expression else_stmt",
    )
    def revisit_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Visit statement rule."""
        return p

    @_("KW_DISENGAGE SEMI")
    def disengage_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Disengage statement rule."""
        return p

    @_("KW_YIELD SEMI")
    def yield_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Yield statement rule."""
        return p

    @_("KW_SYNC expression SEMI")
    def sync_stmt(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Sync statement rule."""
        return p

    # Expression rules (precedence built into grammar)
    # ------------------------------------------------
    @_(
        "atom EQ expression",
        "KW_HAS NAME EQ expression",  # static variables
    )
    def assignment(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Rule for assignment statement."""
        return p

    @_(
        "walrus_assign",
        "walrus_assign KW_IF expression KW_ELSE expression",
    )
    def expression(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Expression rule."""
        return p

    @_(
        "pipe",
        "pipe walrus_op walrus_assign",
    )
    def walrus_assign(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Walrus assignment rule."""
        return p

    @_(
        "elvis_check",
        "elvis_check PIPE_FWD pipe",  # casting achieved here
        "elvis_check PIPE_FWD EQ filter_ctx",  # for comprehension on list, dict, etc.
        "elvis_check PIPE_FWD spawn_ctx",  # for rapid assignments to collections
    )
    def pipe(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Expression rule."""
        return p

    @_(
        "logical",
        "logical ELVIS_OP elvis_check",
    )
    def elvis_check(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Expression rule."""
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
        "arithmetic",
        "NOT compare",
        "arithmetic cmp_op compare",
    )
    def compare(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Compare rule."""
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
        "connect",
        "connect POW power",
    )
    def power(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Power rule."""
        return p

    @_(
        "spawn_walker NOT edge_op_ref connect",
        "spawn_walker connect_op connect",
        "spawn_walker",
    )
    def connect(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Connect rule."""
        return p

    @_(
        "spawn_op KW_TO atom COMMA spawn_object",  # should auto run walker here
        "spawn_object",
    )
    def spawn_walker(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Spawn walker rule."""
        return p

    @_(
        "spawn_op spawn_edge_node",
        "spawn_edge_node",
    )
    def spawn_object(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Spawn object rule."""
        return p

    @_(
        "spawn_op KW_TO spawn_object connect_op spawn_object",
        "unpack",
    )
    def spawn_edge_node(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Spawn edge and node rule."""
        return p

    @_(
        "STAR_MUL STAR_MUL atom",
        "STAR_MUL atom",
        "KW_REF atom",
        "atom",
    )
    def unpack(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Unpack rule."""
        return p

    @_(
        "WALRUS_EQ",
        "ADD_EQ",
        "SUB_EQ",
        "MUL_EQ",
        "DIV_EQ",
    )
    def walrus_op(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Production Assignment rule."""
        return p

    @_(
        "EE",
        "LT",
        "GT",
        "LTE",
        "GTE",
        "NE",
        "KW_IN",
        "KW_NIN",
    )
    def cmp_op(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Compare operator rule."""
        return p

    @_(
        "KW_SPAWN",
        "SPAWN_OP",
    )
    def spawn_op(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Spawn operator rule."""
        return p

    # Atom rules
    # --------------------
    @_(
        "atom_literal",
        "atom_collection",
        "LPAREN expression RPAREN",
        "global_ref",
        "atomic_chain",
        "arch_ref",
        "edge_op_ref",
        "KW_HERE",
        "KW_VISITOR",
    )
    def atom(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Atom rule."""
        return p

    @_(
        "INT",
        "FLOAT",
        "multistring",
        "DOC_STRING",
        "BOOL",
        "NULL",
        "NAME",
        "builtin_type",
    )
    def atom_literal(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Atom rule."""
        return p

    @_(
        "list_val",
        "dict_val",
        # sets and tuples are supported through the pipe forward semantic
    )
    def atom_collection(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Atom rule."""
        return p

    @_(
        "STRING",
        "FSTRING",
        "STRING multistring",
        "FSTRING multistring",
    )
    def multistring(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Multistring rule."""
        return p

    @_(
        "LSQUARE RSQUARE",
        "LSQUARE expr_list RSQUARE",
    )
    def list_val(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """List value rule."""
        return p

    @_(
        "expression",
        "expr_list COMMA expression",
    )
    def expr_list(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Expression list rule."""
        return p

    @_(
        "LBRACE RBRACE",
        "LBRACE kv_pairs RBRACE",
    )
    def dict_val(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Production for dictionary value rule."""
        return p

    @_(
        "expression COLON expression",
        "expression COLON expression COMMA kv_pairs",
    )
    def kv_pairs(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Key/value pairs rule."""
        return p

    @_(
        "DBL_COLON",
        "DBL_COLON NAME",  # :: for walkers, ::name for abilities
        "DBL_COLON KW_ASYNC",
        "DBL_COLON NAME KW_ASYNC",  # :: for walkers, ::name for abilities
    )
    def ability_run(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Ability operator rule."""
        return p

    @_(
        "atomic_chain_safe",
        "atomic_chain_unsafe",
    )
    def atomic_chain(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Atom trailer rule."""
        return p

    @_(
        "atom DOT NAME",
        "atom index_slice",
        "atom call",
        "atom arch_ref",
    )
    def atomic_chain_unsafe(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Atom trailer rule."""
        return p

    @_(
        "atom NULL_OK DOT NAME",
        "atom NULL_OK index_slice",
        "atom NULL_OK call",
        # "atom NULL_OK PIPE_FWD built_in",  # casting and creating tuples and sets
        # "atom NULL_OK PIPE_FWD filter_ctx",  # for comprehension on list, dict, etc.
        # "atom NULL_OK PIPE_FWD spawn_ctx",  # for rapid assignments to collections
        "atom NULL_OK arch_ref",
    )
    def atomic_chain_safe(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Atom trailer rule."""
        return p

    @_(
        "LPAREN RPAREN",
        "LPAREN param_list RPAREN",
        "ability_run",
    )
    def call(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Ability call rule."""
        return p

    @_(
        "expr_list",
        "assignment_list",
        "expr_list COMMA assignment_list",
    )
    def param_list(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Parameter list rule."""
        return p

    @_(
        "assignment",
        "assignment COMMA assignment_list",
    )
    def assignment_list(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Keyword expression list rule."""
        return p

    @_(
        "LSQUARE expression RSQUARE",
        "LSQUARE expression COLON expression RSQUARE",
    )
    def index_slice(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Index/slice rule."""
        return p

    @_("GLOBAL_OP NAME")
    def global_ref(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Global reference rule."""
        return p

    # Architype reference rules
    # -------------------------
    @_(
        "node_ref",
        "edge_ref",
        "walker_ref",
        "spawner_ref",
        "object_ref",
    )
    def arch_ref(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Architype reference rule."""
        return p

    @_("NODE_OP NAME")
    def node_ref(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Node reference rule."""
        return p

    @_("EDGE_OP NAME")
    def edge_ref(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Edge reference rule."""
        return p

    @_("WALKER_OP NAME")
    def walker_ref(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Walker reference rule."""
        return p

    @_("SPAWNER_OP NAME")
    def spawner_ref(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Spawner reference rule."""
        return p

    @_("OBJECT_OP NAME")
    def object_ref(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Object type reference rule."""
        return p

    @_("ABILITY_OP NAME")  # Not a arch, used for ability_spec
    def ability_ref(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Ability reference rule."""
        return p

    # Node / Edge reference and connection rules
    # ------------------------------------------
    @_(
        "edge_to",
        "edge_from",
        "edge_any",
    )
    def edge_op_ref(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Edge reference rule."""
        return p

    @_(
        "ARROW_R",
        "ARROW_R_p1 expression ARROW_R_p2",
    )
    def edge_to(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Edge to rule."""
        return p

    @_(
        "ARROW_L",
        "ARROW_L_p1 expression ARROW_L_p2",
    )
    def edge_from(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Edge from rule."""
        return p

    @_(
        "ARROW_BI",
        "ARROW_L_p1 expression ARROW_R_p2",
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
        "CARROW_R_p1 expression CARROW_R_p2",
    )
    def connect_to(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Connect to rule."""
        return p

    @_(
        "CARROW_L",
        "CARROW_L_p1 expression CARROW_L_p2",
    )
    def connect_from(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Connect from rule."""
        return p

    @_(
        "CARROW_BI",
        "CARROW_L_p1 expression CARROW_R_p2",
    )
    def connect_any(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Connect any rule."""
        return p

    @_(
        "LPAREN filter_compare_list RPAREN",
        # "",
    )
    def filter_ctx(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Filter context rule."""
        return p

    @_("LPAREN assignment_list RPAREN")
    def spawn_ctx(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Spawn context rule."""
        return p

    @_(
        "NAME cmp_op expression",
        "NAME cmp_op expression COMMA filter_compare_list",
        # "",
    )
    def filter_compare_list(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Filter comparison list rule."""
        return p

    @_("")
    def empty(self: "JacParser", p: YaccProduction) -> YaccProduction:
        """Empty rule."""
        return p
