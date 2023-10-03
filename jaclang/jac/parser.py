# type: ignore
"""Parser for Jac."""
from typing import Generator, Optional

import jaclang.jac.absyntree as ast
from jaclang.jac.constant import Constants as Con
from jaclang.jac.lexer import JacLexer
from jaclang.jac.transform import ABCParserMeta, Transform
from jaclang.utils.helpers import dedent_code_block
from jaclang.vendor.sly.yacc import Parser, YaccProduction


_ = None  # For flake8 linting


class JacParser(Transform, Parser, metaclass=ABCParserMeta):
    """Parser for Jac."""

    start = "module"

    def __init__(
        self,
        mod_path: str,
        input_ir: Generator,
        base_path: str = "",
        prior: Optional[Transform] = None,
    ) -> None:
        """Initialize parser."""
        Transform.__init__(self, mod_path, input_ir, base_path, prior)
        self.ir_tup = self.ir
        if not self.errors_had:
            self.ir: ast.AstNode = parse_tree_to_ast(self.ir)

    tokens = JacLexer.tokens
    # debugfile = "parser.out"

    # All mighty start rule
    # ---------------------
    @_(
        "DOC_STRING",
        "DOC_STRING element_list",
    )
    def module(self, p: YaccProduction) -> YaccProduction:
        """Start rule."""
        return p

    # Jac program structured as a list of elements
    # --------------------------------------------
    @_(
        "element",
        "element_list element",
    )
    def element_list(self, p: YaccProduction) -> YaccProduction:
        """Element list rule."""
        return p

    # Element types
    # -------------
    @_(
        "doc_tag global_var",
        "doc_tag test",
        "doc_tag mod_code",
        "import_stmt",
        "include_stmt",
        "doc_tag architype",
        "doc_tag ability",
        "python_code_block",
    )
    def element(self, p: YaccProduction) -> YaccProduction:
        """Element rule."""
        return p

    @_(
        "KW_GLOBAL access_tag assignment_list SEMI",
        "KW_FREEZE access_tag assignment_list SEMI",
    )
    def global_var(self, p: YaccProduction) -> YaccProduction:
        """Global variable rule."""
        return p

    @_(
        "KW_PRIV",
        "KW_PUB",
        "KW_PROT",
    )
    def access(self, p: YaccProduction) -> YaccProduction:
        """Permission tag rule."""
        return p

    @_(
        "COLON access",
        "empty",
    )
    def access_tag(self, p: YaccProduction) -> YaccProduction:
        """Permission tag rule."""
        return p

    @_(
        "KW_TEST NAME code_block",
        "KW_TEST code_block",
    )
    def test(self, p: YaccProduction) -> YaccProduction:
        """Test rule."""
        return p

    @_(
        "KW_WITH KW_ENTRY code_block",
        "KW_WITH KW_ENTRY sub_name code_block",
    )
    def mod_code(self, p: YaccProduction) -> YaccProduction:
        """Module-level free code rule."""
        return p

    @_(
        "empty",
        "DOC_STRING",
        "STRING",
    )
    def doc_tag(self, p: YaccProduction) -> YaccProduction:
        """Doc tag rule."""
        return p

    @_("PYNLINE")
    def python_code_block(self, p: YaccProduction) -> YaccProduction:
        """Python code block rule."""
        return p

    # Import Statements
    # -----------------
    @_(
        "KW_IMPORT sub_name import_path SEMI",
        "KW_IMPORT sub_name import_path KW_AS NAME SEMI",
        "KW_IMPORT sub_name KW_FROM import_path COMMA import_items SEMI",
    )
    def import_stmt(self, p: YaccProduction) -> YaccProduction:
        """Import rule."""
        return p

    @_("KW_INCLUDE sub_name import_path SEMI")
    def include_stmt(self, p: YaccProduction) -> YaccProduction:
        """Import rule."""
        return p

    @_(
        "import_path_prefix",
        "import_path_prefix import_path_tail",
    )
    def import_path(self, p: YaccProduction) -> YaccProduction:
        """Import path rule."""
        return p

    @_(
        "esc_name",
        "DOT esc_name",
        "DOT DOT esc_name",
    )
    def import_path_prefix(self, p: YaccProduction) -> YaccProduction:
        """Import path prefix rule."""
        return p

    @_(
        "DOT esc_name",
        "import_path_tail DOT esc_name",
    )
    def import_path_tail(self, p: YaccProduction) -> YaccProduction:
        """Import path tail rule."""
        return p

    @_(
        "named_refs",
        "named_refs KW_AS NAME",
        "import_items COMMA named_refs",
        "import_items COMMA named_refs KW_AS NAME",
    )
    def import_items(self, p: YaccProduction) -> YaccProduction:
        """Name as list rule."""
        return p

    # Architype elements
    # ------------------
    @_(
        "architype_decl",
        "architype_def",
        "enum",
        "decorator architype",
    )
    def architype(self, p: YaccProduction) -> YaccProduction:
        """Architype rule."""
        return p

    @_(
        "arch_type access_tag NAME inherited_archs SEMI",
        "arch_type access_tag NAME inherited_archs member_block",
    )
    def architype_decl(self, p: YaccProduction) -> YaccProduction:
        """Architype declaration rule."""
        return p

    @_("abil_to_arch_chain member_block")
    def architype_def(self, p: YaccProduction) -> YaccProduction:
        """Architype definition rule."""
        return p

    @_(
        "KW_NODE",
        "KW_EDGE",
        "KW_OBJECT",
        "KW_WALKER",
    )
    def arch_type(self, p: YaccProduction) -> YaccProduction:
        """Arch type rule."""
        return p

    @_("DECOR_OP atom")
    def decorator(self, p: YaccProduction) -> YaccProduction:
        """Python style decorator rule."""
        return p

    @_(
        "empty",
        "inherited_archs sub_name_dotted",
    )
    def inherited_archs(self, p: YaccProduction) -> YaccProduction:
        """Sub name list rule."""
        return p

    @_("COLON NAME")
    def sub_name(self, p: YaccProduction) -> YaccProduction:
        """Sub name rule."""
        return p

    @_("COLON dotted_name")
    def sub_name_dotted(self, p: YaccProduction) -> YaccProduction:
        """Sub name rule."""
        return p

    @_(
        "all_refs",
        "dotted_name DOT all_refs",
    )
    def dotted_name(self, p: YaccProduction) -> YaccProduction:
        """Strict arch reference rule."""
        return p

    @_(
        "NAME",
        "KWESC_NAME",
    )
    def esc_name(self, p: YaccProduction) -> YaccProduction:
        """Escaped name rule."""
        return p

    @_(
        "named_refs",
        "special_refs",
    )
    def all_refs(self, p: YaccProduction) -> YaccProduction:
        """All reference rules."""
        return p

    @_(
        "esc_name",
        "global_ref",
    )
    def named_refs(self, p: YaccProduction) -> YaccProduction:
        """All reference rules."""
        return p

    @_(
        "HERE_OP",
        "SELF_OP",
        "SUPER_OP",
        "ROOT_OP",
        "INIT_OP",
    )
    def special_refs(self, p: YaccProduction) -> YaccProduction:
        """All reference rules."""
        return p

    # Enum elements
    # ----------------
    @_(
        "enum_decl",
        "enum_def",
    )
    def enum(self, p: YaccProduction) -> YaccProduction:
        """Enum rule."""
        return p

    @_(
        "KW_ENUM access_tag NAME inherited_archs SEMI",
        "KW_ENUM access_tag NAME inherited_archs enum_block",
    )
    def enum_decl(self, p: YaccProduction) -> YaccProduction:
        """Enum decl rule."""
        return p

    @_("arch_to_enum_chain enum_block")
    def enum_def(self, p: YaccProduction) -> YaccProduction:
        """Enum def rule."""
        return p

    @_(
        "LBRACE RBRACE",
        "LBRACE enum_stmt_list RBRACE",
    )
    def enum_block(self, p: YaccProduction) -> YaccProduction:
        """Enum block rule."""
        return p

    @_(
        "NAME",
        "enum_op_assign",
        "enum_stmt_list COMMA NAME",
        "enum_stmt_list COMMA enum_op_assign",
    )
    def enum_stmt_list(self, p: YaccProduction) -> YaccProduction:
        """Enum op list rule."""
        return p

    @_(
        "NAME EQ expression",
    )
    def enum_op_assign(self, p: YaccProduction) -> YaccProduction:
        """Enum op assign rule."""
        return p

    # Ability elements
    # ----------------
    @_(
        "ability_decl",
        "KW_ASYNC ability_decl",
        "ability_def",
        "decorator ability",
    )
    def ability(self, p: YaccProduction) -> YaccProduction:
        """Ability rule."""
        return p

    @_(
        "static_tag KW_CAN access_tag all_refs event_clause SEMI",
        "static_tag KW_CAN access_tag all_refs func_decl SEMI",
        "static_tag KW_CAN access_tag all_refs event_clause code_block",
        "static_tag KW_CAN access_tag all_refs func_decl code_block",
    )
    def ability_decl(self, p: YaccProduction) -> YaccProduction:
        """Ability rule."""
        return p

    @_(
        "arch_to_abil_chain event_clause code_block",
        "arch_to_abil_chain func_decl code_block",
    )
    def ability_def(self, p: YaccProduction) -> YaccProduction:
        """Ability rule."""
        return p

    @_(
        "static_tag KW_CAN access_tag all_refs event_clause KW_ABSTRACT SEMI",
        "static_tag KW_CAN access_tag all_refs func_decl KW_ABSTRACT SEMI",
    )
    def abstract_ability(self, p: YaccProduction) -> YaccProduction:
        """Abstract ability rule."""
        return p

    @_(
        "KW_WITH KW_ENTRY return_type_tag",
        "KW_WITH KW_EXIT return_type_tag",
        "KW_WITH type_spec KW_ENTRY return_type_tag",
        "KW_WITH type_spec KW_EXIT return_type_tag",
    )
    def event_clause(self, p: YaccProduction) -> YaccProduction:
        """Event clause rule."""
        return p

    @_(
        "return_type_tag",
        "LPAREN RPAREN return_type_tag",
        "LPAREN func_decl_param_list RPAREN return_type_tag",
    )
    def func_decl(self, p: YaccProduction) -> YaccProduction:
        """Func declaration parameter rule."""
        return p

    @_(
        "param_var",
        "func_decl_param_list COMMA param_var",
    )
    def func_decl_param_list(self, p: YaccProduction) -> YaccProduction:
        """Func declaration parameters list rule."""
        return p

    @_(
        "NAME type_tag",
        "NAME type_tag EQ expression",
        "STAR_MUL NAME type_tag",
        "STAR_MUL NAME type_tag EQ expression",
        "STAR_POW NAME type_tag",
        "STAR_POW NAME type_tag EQ expression",
    )
    def param_var(self, p: YaccProduction) -> YaccProduction:
        """Parameter variable rule rule."""
        return p

    # Attribute blocks
    # ----------------
    @_(
        "LBRACE RBRACE",
        "LBRACE member_stmt_list RBRACE",
    )
    def member_block(self, p: YaccProduction) -> YaccProduction:
        """Attribute block rule."""
        return p

    @_(
        "member_stmt",
        "member_stmt_list member_stmt",
    )
    def member_stmt_list(self, p: YaccProduction) -> YaccProduction:
        """Attribute statement list rule."""
        return p

    @_(
        "doc_tag has_stmt",
        "doc_tag architype",
        "doc_tag ability",
        "doc_tag abstract_ability",
        "python_code_block",
    )
    def member_stmt(self, p: YaccProduction) -> YaccProduction:
        """Attribute statement rule."""
        return p

    # Has statements
    # --------------
    @_(
        "static_tag KW_HAS access_tag has_assign_clause SEMI",
        "static_tag KW_FREEZE access_tag has_assign_clause SEMI",
    )
    def has_stmt(self, p: YaccProduction) -> YaccProduction:
        """Has statement rule."""
        return p

    @_(
        "empty",
        "KW_STATIC",
    )
    def static_tag(self, p: YaccProduction) -> YaccProduction:
        """KW_Static tag rule."""
        return p

    @_(
        "typed_has_clause",
        "has_assign_clause COMMA typed_has_clause",
    )
    def has_assign_clause(self, p: YaccProduction) -> YaccProduction:
        """Has assign list rule."""
        return p

    @_(
        "esc_name type_tag",
        "esc_name type_tag EQ expression",
    )
    def typed_has_clause(self, p: YaccProduction) -> YaccProduction:
        """Parameter variable rule rule."""
        return p

    @_("COLON type_spec")
    def type_tag(self, p: YaccProduction) -> YaccProduction:
        """Type hint rule."""
        return p

    @_(
        "empty",
        "RETURN_HINT type_spec",
    )
    def return_type_tag(self, p: YaccProduction) -> YaccProduction:
        """Type hint rule."""
        return p

    @_(
        "single_type",
        "type_spec NULL_OK",
        "type_spec BW_OR single_type",
    )
    def type_spec(self, p: YaccProduction) -> YaccProduction:
        """Type hint rule."""
        return p

    @_(
        "builtin_type",
        "NULL",
        "dotted_name",
        "TYP_LIST LSQUARE single_type RSQUARE",
        "TYP_TUPLE LSQUARE single_type RSQUARE",
        "TYP_SET LSQUARE single_type RSQUARE",
        "TYP_DICT LSQUARE single_type COMMA single_type RSQUARE",
    )
    def single_type(self, p: YaccProduction) -> YaccProduction:
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
        "TYP_ANY",
        "TYP_TYPE",
    )
    def builtin_type(self, p: YaccProduction) -> YaccProduction:
        """Any type rule."""
        return p

    # Codeblock statements
    # --------------------
    @_(
        "LBRACE RBRACE",
        "LBRACE statement_list RBRACE",
    )
    def code_block(self, p: YaccProduction) -> YaccProduction:
        """Code block rule."""
        return p

    @_(
        "statement_list statement",
        "statement",
    )
    def statement_list(self, p: YaccProduction) -> YaccProduction:
        """Statement list rule."""
        return p

    @_(
        "import_stmt",
        "doc_tag architype",
        "doc_tag ability",
        "typed_ctx_block",
        "assignment SEMI",
        "static_assignment",
        "expression SEMI",
        "if_stmt",
        "try_stmt",
        "for_stmt",
        "while_stmt",
        "with_stmt",
        "raise_stmt SEMI",
        "assert_stmt SEMI",
        "ctrl_stmt SEMI",
        "delete_stmt SEMI",
        "report_stmt SEMI",
        "return_stmt SEMI",
        "yield_stmt SEMI",
        "await_stmt SEMI",
        "walker_stmt",
        "python_code_block",
    )
    def statement(self, p: YaccProduction) -> YaccProduction:
        """Statement rule."""
        return p

    @_("RETURN_HINT type_spec code_block")
    def typed_ctx_block(self, p: YaccProduction) -> YaccProduction:
        """Typed context block rule."""
        return p

    @_(
        "KW_IF expression code_block",
        "KW_IF expression code_block else_stmt",
        "KW_IF expression code_block elif_list",
        "KW_IF expression code_block elif_list else_stmt",
    )
    def if_stmt(self, p: YaccProduction) -> YaccProduction:
        """If statement rule."""
        return p

    @_(
        "KW_ELIF expression code_block",
        "elif_list KW_ELIF expression code_block",
    )
    def elif_list(self, p: YaccProduction) -> YaccProduction:
        """Else if statement list rule."""
        return p

    @_("KW_ELSE code_block")
    def else_stmt(self, p: YaccProduction) -> YaccProduction:
        """Else statement rule."""
        return p

    @_(
        "KW_TRY code_block",
        "KW_TRY code_block except_list",
        "KW_TRY code_block finally_stmt",
        "KW_TRY code_block except_list finally_stmt",
    )
    def try_stmt(self, p: YaccProduction) -> YaccProduction:
        """Try statement rule."""
        return p

    @_(
        "except_def",
        "except_list except_def",
    )
    def except_list(self, p: YaccProduction) -> YaccProduction:
        """Except statement list rule."""
        return p

    @_(
        "KW_EXCEPT expression code_block",
        "KW_EXCEPT expression KW_AS NAME code_block",
    )
    def except_def(self, p: YaccProduction) -> YaccProduction:
        """Except definition rule."""
        return p

    @_(
        "KW_FINALLY code_block",
    )
    def finally_stmt(self, p: YaccProduction) -> YaccProduction:
        """Except finally statement rule."""
        return p

    @_(
        "KW_FOR assignment KW_TO expression KW_BY expression code_block",
        "KW_FOR name_list KW_IN expression code_block",
    )
    def for_stmt(self, p: YaccProduction) -> YaccProduction:
        """For statement rule."""
        return p

    @_(
        "NAME",
        "name_list COMMA NAME",
    )
    def name_list(self, p: YaccProduction) -> YaccProduction:
        """List of names."""
        return p

    @_("KW_WHILE expression code_block")
    def while_stmt(self, p: YaccProduction) -> YaccProduction:
        """While statement rule."""
        return p

    @_("KW_WITH expr_as_list code_block")
    def with_stmt(self, p: YaccProduction) -> YaccProduction:
        """With statement rule."""
        return p

    @_(
        "expression",
        "expression KW_AS NAME",
        "expr_as_list COMMA NAME",
        "expr_as_list COMMA expression KW_AS NAME",
    )
    def expr_as_list(self, p: YaccProduction) -> YaccProduction:
        """Name as list rule."""
        return p

    @_(
        "KW_RAISE",
        "KW_RAISE expression",
    )
    def raise_stmt(self, p: YaccProduction) -> YaccProduction:
        """Raise statement rule."""
        return p

    @_(
        "KW_ASSERT expression",
        "KW_ASSERT expression COMMA expression",
    )
    def assert_stmt(self, p: YaccProduction) -> YaccProduction:
        """Assert statement rule."""
        return p

    @_(
        "KW_CONTINUE",
        "KW_BREAK",
        "KW_SKIP",
    )
    def ctrl_stmt(self, p: YaccProduction) -> YaccProduction:
        """Control statement rule."""
        return p

    @_("KW_DELETE expression")
    def delete_stmt(self, p: YaccProduction) -> YaccProduction:
        """Delete statement rule."""
        return p

    @_(
        "KW_REPORT expression",
    )
    def report_stmt(self, p: YaccProduction) -> YaccProduction:
        """Report statement rule."""
        return p

    @_(
        "KW_RETURN",
        "KW_RETURN expression",
    )
    def return_stmt(self, p: YaccProduction) -> YaccProduction:
        """Report statement rule."""
        return p

    @_(
        "KW_YIELD",
        "KW_YIELD expression",
    )
    def yield_stmt(self, p: YaccProduction) -> YaccProduction:
        """Yield statement rule."""
        return p

    @_(
        "ignore_stmt SEMI",
        "visit_stmt",
        "revisit_stmt",
        "disengage_stmt SEMI",
    )
    def walker_stmt(self, p: YaccProduction) -> YaccProduction:
        """Walker statement rule."""
        return p

    @_("KW_IGNORE expression")
    def ignore_stmt(self, p: YaccProduction) -> YaccProduction:
        """Ignore statement rule."""
        return p

    @_(
        "KW_VISIT expression SEMI",
        "KW_VISIT sub_name_dotted expression SEMI",
        "KW_VISIT expression else_stmt",
        "KW_VISIT sub_name_dotted expression else_stmt",
    )
    def visit_stmt(self, p: YaccProduction) -> YaccProduction:
        """Visit statement rule."""
        return p

    @_(
        "KW_REVISIT SEMI",
        "KW_REVISIT expression SEMI",
        "KW_REVISIT else_stmt",
        "KW_REVISIT expression else_stmt",
    )
    def revisit_stmt(self, p: YaccProduction) -> YaccProduction:
        """Visit statement rule."""
        return p

    @_("KW_DISENGAGE")
    def disengage_stmt(self, p: YaccProduction) -> YaccProduction:
        """Disengage statement rule."""
        return p

    @_("KW_AWAIT expression")
    def await_stmt(self, p: YaccProduction) -> YaccProduction:
        """Sync statement rule."""
        return p

    # Expression rules (precedence built into grammar)
    # ------------------------------------------------
    @_(
        "atom EQ expression",
        "KW_FREEZE atom EQ expression",
    )
    def assignment(self, p: YaccProduction) -> YaccProduction:
        """Rule for assignment statement."""
        return p

    @_("KW_HAS assignment_list SEMI")
    def static_assignment(self, p: YaccProduction) -> YaccProduction:
        """Rule for static assignment statement."""
        return p

    @_(
        "pipe",
        "pipe KW_IF expression KW_ELSE expression",
    )
    def expression(self, p: YaccProduction) -> YaccProduction:
        """Expression rule."""
        return p

    @_(
        "pipe_back",
        "pipe_back PIPE_FWD pipe",  # casting achieved here
    )
    def pipe(self, p: YaccProduction) -> YaccProduction:
        """Pipe forward rule."""
        return p

    @_(
        "elvis_check",
        "elvis_check PIPE_BKWD pipe_back",
    )
    def pipe_back(self, p: YaccProduction) -> YaccProduction:
        """Pipe backward rule."""
        return p

    @_(
        "bitwise_or",
        "bitwise_or ELVIS_OP elvis_check",
    )
    def elvis_check(self, p: YaccProduction) -> YaccProduction:
        """Expression rule."""
        return p

    @_(
        "bitwise_xor",
        "bitwise_xor BW_OR bitwise_or",
    )
    def bitwise_or(self, p: YaccProduction) -> YaccProduction:
        """Bitwise or rule."""
        return p

    @_(
        "bitwise_and",
        "bitwise_and BW_XOR bitwise_xor",
    )
    def bitwise_xor(self, p: YaccProduction) -> YaccProduction:
        """Bitwise xor rule."""
        return p

    @_(
        "shift",
        "shift BW_AND bitwise_and",
    )
    def bitwise_and(self, p: YaccProduction) -> YaccProduction:
        """Bitwise and rule."""
        return p

    @_(
        "logical",
        "logical LSHIFT shift",
        "logical RSHIFT shift",
    )
    def shift(self, p: YaccProduction) -> YaccProduction:
        """Shift expression rule."""
        return p

    @_(
        "compare",
        "compare KW_AND logical",
        "compare KW_OR logical",
        "NOT logical",
    )
    def logical(self, p: YaccProduction) -> YaccProduction:
        """Logical rule."""
        return p

    @_(
        "arithmetic",
        "arithmetic cmp_op compare",
    )
    def compare(self, p: YaccProduction) -> YaccProduction:
        """Compare rule."""
        return p

    @_(
        "term",
        "term PLUS arithmetic",
        "term MINUS arithmetic",
    )
    def arithmetic(self, p: YaccProduction) -> YaccProduction:
        """Arithmetic rule."""
        return p

    @_(
        "factor",
        "factor STAR_MUL term",
        "factor FLOOR_DIV term",
        "factor DIV term",
        "factor MOD term",
    )
    def term(self, p: YaccProduction) -> YaccProduction:
        """Term rule."""
        return p

    @_(
        "PLUS factor",
        "MINUS factor",
        "BW_NOT factor",
        "power",
    )
    def factor(self, p: YaccProduction) -> YaccProduction:
        """Factor rule."""
        return p

    @_(
        "connect",
        "connect STAR_POW power",
    )
    def power(self, p: YaccProduction) -> YaccProduction:
        """Power rule."""
        return p

    @_(
        "atomic_pipe disconnect_op connect",
        "atomic_pipe connect_op connect",
        "atomic_pipe",
    )
    def connect(self, p: YaccProduction) -> YaccProduction:
        """Connect rule."""
        return p

    @_(
        "atomic_pipe A_PIPE_FWD atomic_pipe_back",
        "atomic_pipe KW_SPAWN atomic_pipe_back",  # For high level readability
        "atomic_pipe_back",
    )
    def atomic_pipe(self, p: YaccProduction) -> YaccProduction:
        """Pipe forward rule."""
        return p

    @_(
        "atomic_pipe_back A_PIPE_BKWD unpack",
        "unpack",
    )
    def atomic_pipe_back(self, p: YaccProduction) -> YaccProduction:
        """Pipe backward rule."""
        return p

    @_(
        "STAR_POW atom",
        "STAR_MUL atom",
        "ref",
    )
    def unpack(self, p: YaccProduction) -> YaccProduction:
        """Unpack rule."""
        return p

    @_(
        "BW_AND walrus_assign",
        "walrus_assign",
    )
    def ref(self, p: YaccProduction) -> YaccProduction:
        """Unpack rule."""
        return p

    @_(
        "ds_call",
        "ds_call walrus_op walrus_assign",
    )
    def walrus_assign(self, p: YaccProduction) -> YaccProduction:
        """Walrus assignment rule."""
        return p

    @_(
        "KW_SPAWN atom",
        "A_PIPE_FWD atom",
        "PIPE_FWD atom",
        "atom",
    )
    def ds_call(self, p: YaccProduction) -> YaccProduction:
        """Unpack rule."""
        return p

    @_(
        "WALRUS_EQ",
        "ADD_EQ",
        "SUB_EQ",
        "MUL_EQ",
        "FLOOR_DIV_EQ",
        "DIV_EQ",
        "MOD_EQ",
        "BW_AND_EQ",
        "BW_OR_EQ",
        "BW_XOR_EQ",
        "BW_NOT_EQ",
        "LSHIFT_EQ",
        "RSHIFT_EQ",
    )
    def walrus_op(self, p: YaccProduction) -> YaccProduction:
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
        "KW_IS",
        "KW_ISN",
    )
    def cmp_op(self, p: YaccProduction) -> YaccProduction:
        """Compare operator rule."""
        return p

    # Atom rules
    # --------------------
    @_(
        "atom_literal",
        "atom_collection",
        "LPAREN expression RPAREN",
        "atomic_chain",
        "all_refs",
        "edge_op_ref",
    )
    def atom(self, p: YaccProduction) -> YaccProduction:
        """Atom rule."""
        return p

    @_(
        "INT",
        "HEX",
        "BIN",
        "OCT",
        "FLOAT",
        "multistring",
        "BOOL",
        "NULL",
        "builtin_type",
    )
    def atom_literal(self, p: YaccProduction) -> YaccProduction:
        """Atom rule."""
        return p

    @_(
        "list_val",
        "tuple_val",
        "set_val",
        "dict_val",
        "list_compr",
        "gen_compr",
        "set_compr",
        "dict_compr",
    )
    def atom_collection(self, p: YaccProduction) -> YaccProduction:
        """Atom rule."""
        return p

    @_(
        "STRING",
        "FSTRING",
        "multistring STRING",
        "multistring FSTRING",
    )
    def multistring(self, p: YaccProduction) -> YaccProduction:
        """Multistring rule."""
        return p

    @_(
        "LSQUARE RSQUARE",
        "LSQUARE expr_list RSQUARE",
    )
    def list_val(self, p: YaccProduction) -> YaccProduction:
        """List value rule."""
        return p

    @_(
        "LPAREN RPAREN",
        "LPAREN tuple_list RPAREN",
    )
    def tuple_val(self, p: YaccProduction) -> YaccProduction:
        """Tuple value rule."""
        return p

    @_(
        "LBRACE expr_list RBRACE",
    )
    def set_val(self, p: YaccProduction) -> YaccProduction:
        """Set value rule."""
        return p

    @_(
        "expression",
        "expr_list COMMA expression",
    )
    def expr_list(self, p: YaccProduction) -> YaccProduction:
        """Expression list rule."""
        return p

    @_(
        "expression COMMA",
        "expression COMMA expr_list",
        "assignment_list",
        "expression COMMA assignment_list",
        "expression COMMA expr_list COMMA assignment_list",
    )
    def tuple_list(self, p: YaccProduction) -> YaccProduction:
        """Tuple list rule."""
        return p

    @_(
        "LBRACE RBRACE",
        "LBRACE kv_pairs RBRACE",
    )
    def dict_val(self, p: YaccProduction) -> YaccProduction:
        """Production for dictionary value rule."""
        return p

    @_("LSQUARE inner_compr RSQUARE")
    def list_compr(self, p: YaccProduction) -> YaccProduction:
        """Comprehension rule."""
        return p

    @_("LPAREN inner_compr RPAREN")
    def gen_compr(self, p: YaccProduction) -> YaccProduction:
        """Comprehension rule."""
        return p

    @_("LBRACE inner_compr RBRACE")
    def set_compr(self, p: YaccProduction) -> YaccProduction:
        """Comprehension rule."""
        return p

    @_(
        "expression KW_FOR name_list KW_IN walrus_assign",
        "expression KW_FOR name_list KW_IN walrus_assign KW_IF expression",
    )
    def inner_compr(self, p: YaccProduction) -> YaccProduction:
        """Comprehension rule."""
        return p

    @_(
        "LBRACE expression COLON expression KW_FOR name_list KW_IN walrus_assign RBRACE",
        "LBRACE expression COLON expression KW_FOR name_list KW_IN walrus_assign KW_IF expression RBRACE",
    )
    def dict_compr(self, p: YaccProduction) -> YaccProduction:
        """Comprehension rule."""
        return p

    @_(
        "expression COLON expression",
        "kv_pairs COMMA expression COLON expression",
    )
    def kv_pairs(self, p: YaccProduction) -> YaccProduction:
        """Key/value pairs rule."""
        return p

    @_(
        "atomic_chain_safe",
        "atomic_chain_unsafe",
        "atomic_call",
    )
    def atomic_chain(self, p: YaccProduction) -> YaccProduction:
        """Atom trailer rule."""
        return p

    @_(
        "atom DOT all_refs",
        "atom DOT_FWD all_refs",
        "atom DOT_BKWD all_refs",
        "atom index_slice",
        "atom edge_op_ref",
        "atom filter_compr",
    )
    def atomic_chain_unsafe(self, p: YaccProduction) -> YaccProduction:
        """Atom trailer rule."""
        return p

    @_(
        "atom NULL_OK DOT all_refs",
        "atom NULL_OK DOT_FWD all_refs",
        "atom NULL_OK DOT_BKWD all_refs",
        "atom NULL_OK index_slice",
        "atom NULL_OK edge_op_ref",
        "atom NULL_OK filter_compr",
    )
    def atomic_chain_safe(self, p: YaccProduction) -> YaccProduction:
        """Atom trailer rule."""
        return p

    @_("atom func_call_tail")
    def atomic_call(self, p: YaccProduction) -> YaccProduction:
        """Ability call rule."""
        return p

    @_(
        "LPAREN RPAREN",
        "LPAREN param_list RPAREN",
    )
    def func_call_tail(self, p: YaccProduction) -> YaccProduction:
        """Rule for function calls."""
        return p

    @_(
        "expr_list",
        "assignment_list",
        "expr_list COMMA assignment_list",
    )
    def param_list(self, p: YaccProduction) -> YaccProduction:
        """Parameter list rule."""
        return p

    @_(
        "assignment",
        "assignment_list COMMA assignment",
    )
    def assignment_list(self, p: YaccProduction) -> YaccProduction:
        """Keyword expression list rule."""
        return p

    @_(
        "LSQUARE expression RSQUARE",
        "LSQUARE expression COLON expression RSQUARE",
        "LSQUARE expression COLON RSQUARE",
        "LSQUARE COLON expression RSQUARE",
        "LSQUARE COLON RSQUARE",
    )
    def index_slice(self, p: YaccProduction) -> YaccProduction:
        """Index/slice rule."""
        return p

    # Architype reference rules
    # -------------------------
    @_(
        "node_ref",
        "edge_ref",
        "walker_ref",
        "object_ref",
    )
    def arch_ref(self, p: YaccProduction) -> YaccProduction:
        """Strict Architype reference rule."""
        return p

    @_(
        "arch_ref",
        "ability_ref",
        "arch_or_ability_chain arch_ref",
        "arch_or_ability_chain ability_ref",
    )
    def arch_or_ability_chain(self, p: YaccProduction) -> YaccProduction:
        """Strict Architype reference rule."""
        return p

    @_(
        "arch_ref",
        "arch_or_ability_chain arch_ref",
    )
    def abil_to_arch_chain(self, p: YaccProduction) -> YaccProduction:
        """Strict Architype reference list rule."""
        return p

    @_(
        "ability_ref",
        "arch_or_ability_chain ability_ref",
    )
    def arch_to_abil_chain(self, p: YaccProduction) -> YaccProduction:
        """Strict Architype reference list rule."""
        return p

    @_(
        "enum_ref",
        "arch_or_ability_chain enum_ref",
    )
    def arch_to_enum_chain(self, p: YaccProduction) -> YaccProduction:
        """Strict Architype reference list rule."""
        return p

    @_("NODE_OP NAME")
    def node_ref(self, p: YaccProduction) -> YaccProduction:
        """Node reference rule."""
        return p

    @_("EDGE_OP NAME")
    def edge_ref(self, p: YaccProduction) -> YaccProduction:
        """Edge reference rule."""
        return p

    @_("WALKER_OP NAME")
    def walker_ref(self, p: YaccProduction) -> YaccProduction:
        """Walker reference rule."""
        return p

    @_("OBJECT_OP esc_name")
    def object_ref(self, p: YaccProduction) -> YaccProduction:
        """Object type reference rule."""
        return p

    @_("ENUM_OP NAME")
    def enum_ref(self, p: YaccProduction) -> YaccProduction:
        """Object type reference rule."""
        return p

    @_(
        "ABILITY_OP esc_name",
        "ABILITY_OP special_refs",  # only <init> is valid for now
    )
    def ability_ref(self, p: YaccProduction) -> YaccProduction:
        """Ability reference rule."""
        return p

    @_("GLOBAL_OP esc_name")
    def global_ref(self, p: YaccProduction) -> YaccProduction:
        """Global reference rule."""
        return p

    # Node / Edge reference and connection rules
    # ------------------------------------------
    @_(
        "edge_to",
        "edge_from",
        "edge_any",
    )
    def edge_op_ref(self, p: YaccProduction) -> YaccProduction:
        """Edge reference rule."""
        return p

    @_(
        "ARROW_R",
        "ARROW_R_p1 expression ARROW_R_p2",
        "ARROW_R_p1 expression COLON filter_compare_list ARROW_R_p2",
    )
    def edge_to(self, p: YaccProduction) -> YaccProduction:
        """Edge to rule."""
        return p

    @_(
        "ARROW_L",
        "ARROW_L_p1 expression ARROW_L_p2",
        "ARROW_L_p1 expression COLON filter_compare_list ARROW_L_p2",
    )
    def edge_from(self, p: YaccProduction) -> YaccProduction:
        """Edge from rule."""
        return p

    @_(
        "ARROW_BI",
        "ARROW_L_p1 expression ARROW_R_p2",
        "ARROW_L_p1 expression COLON filter_compare_list ARROW_R_p2",
    )
    def edge_any(self, p: YaccProduction) -> YaccProduction:
        """Edge any rule."""
        return p

    @_(
        "connect_to",
        "connect_from",
    )
    def connect_op(self, p: YaccProduction) -> YaccProduction:
        """Connect operator rule."""
        return p

    @_("NOT edge_op_ref")
    def disconnect_op(self, p: YaccProduction) -> YaccProduction:
        """Connect operator not rule."""
        return p

    @_(
        "CARROW_R",
        "CARROW_R_p1 expression CARROW_R_p2",
        "CARROW_R_p1 expression COLON assignment_list CARROW_R_p2",
    )
    def connect_to(self, p: YaccProduction) -> YaccProduction:
        """Connect to rule."""
        return p

    @_(
        "CARROW_L",
        "CARROW_L_p1 expression CARROW_L_p2",
        "CARROW_L_p1 expression COLON assignment_list CARROW_L_p2",
    )
    def connect_from(self, p: YaccProduction) -> YaccProduction:
        """Connect from rule."""
        return p

    @_("LPAREN EQ filter_compare_list RPAREN")
    def filter_compr(self, p: YaccProduction) -> YaccProduction:
        """Filter context rule."""
        return p

    @_(
        "esc_name cmp_op expression",
        "filter_compare_list COMMA esc_name cmp_op expression",
    )
    def filter_compare_list(self, p: YaccProduction) -> YaccProduction:
        """Filter comparison list rule."""
        return p

    @_("")
    def empty(self, p: YaccProduction) -> YaccProduction:
        """Empty rule."""
        return p

    # Transform Implementations
    # -------------------------
    def transform(self, ir: list) -> ast.AstNode:
        """Tokenize the input."""
        ir = self.parse(ir)
        return ir

    def error(self, p: YaccProduction) -> None:
        """Improved error handling for Jac Parser."""
        self.cur_line = p.lineno if p else 0
        if not p:
            self.log_error("Escaping at end of File! Not Valid Jac!\n")
            return
        self.log_error(f'JParse Error, incorrect usage of "{p.value}" ({p.type})\n')

        # Read ahead looking for a closing '}'
        while True:
            tok = next(self.tokens, None)  # type: ignore
            if not tok or tok.type == "RBRACE":
                break
        self.restart()


def fstr_sly_parser_hack() -> Optional[dict]:
    """Hack to map expression parser for fstrings in sly parser."""
    if "__file__" in globals():
        with open(__file__, "r") as file:
            module_data = file.read()

        new_module_data = module_data.replace(
            'start = "module"', 'start = "expression"'
        ).replace('debugfile = "parser.out"', "")
        new_module_namespace = {}
        exec(new_module_data, new_module_namespace)
        return (
            new_module_namespace["JacParser"]
            if "JacParser" in new_module_namespace
            else None
        )


JacParserExpr = fstr_sly_parser_hack()


def parse_tree_to_ast(
    tree: tuple, parent: Optional[ast.AstNode] = None, lineno: int = 0
) -> ast.AstNode:
    """Convert parser output to ast, also parses fstrings."""

    def find_and_concat_fstr_pieces(tup: tuple) -> str:
        result = ""
        for item in tup:
            if isinstance(item, tuple):
                result += find_and_concat_fstr_pieces(item)
            elif isinstance(item, LexToken) and item.type == "PIECE":
                result += item.value
        return result

    from jaclang.utils.fstring_parser import FStringLexer, FStringParser
    from jaclang.vendor.sly.lex import Token as LexToken

    ast_tree: ast.AstNode = None
    if not isinstance(tree, ast.AstNode):
        if isinstance(tree, tuple):
            if tree[0] == "fstr_expr":
                tree = JacParserExpr(
                    mod_path="",
                    input_ir=JacLexer(
                        mod_path="",
                        input_ir=find_and_concat_fstr_pieces(tree),
                        fstr_override=True,
                    ).ir,
                ).ir_tup[2]
            kids = tree[2:]
            ast_tree = ast.Parse(
                name=tree[0],
                parent=parent,
                mod_link=None,
                line=tree[1] if lineno == 0 else lineno,
                kid=[],
            )
            ast_tree.kid = [
                parse_tree_to_ast(x, parent=ast_tree, lineno=lineno) for x in kids
            ]
        elif isinstance(tree, LexToken):
            if tree.type == "FSTRING":
                lineno = tree.lineno
                ftree = FStringParser().parse(FStringLexer().tokenize(tree.value))
                return parse_tree_to_ast(ftree, parent=parent, lineno=lineno)
            else:
                meta = {
                    "name": tree.type,
                    "parent": parent,
                    "mod_link": None,
                    "value": tree.value,
                    "kid": [],
                    "line": tree.lineno if lineno == 0 else lineno,
                    "col_start": tree.index - tree.lineidx + 1,
                    "col_end": tree.end - tree.lineidx + 1,
                }
                if tree.type == "NAME":
                    ast_tree = ast.Name(already_declared=False, **meta)
                elif tree.type == "KWESC_NAME":
                    meta["value"] = meta["value"].replace("<>", "")
                    ast_tree = ast.Name(already_declared=False, **meta)
                elif tree.type == "FLOAT":
                    ast_tree = ast.Constant(typ=float, **meta)
                elif tree.type in ["INT", "HEX", "BIN", "OCT"]:
                    ast_tree = ast.Constant(typ=int, **meta)
                elif tree.type in ["STRING", "FSTRING"]:
                    ast_tree = ast.Constant(typ=str, **meta)
                elif tree.type == "BOOL":
                    ast_tree = ast.Constant(typ=bool, **meta)
                elif tree.type == "NULL":
                    ast_tree = ast.Constant(typ=type(None), **meta)
                elif tree.type.startswith("TYP_"):
                    ast_tree = ast.Constant(typ=type, **meta)
                elif tree.type == "PYNLINE":
                    ast_tree = ast.Token(**meta)
                    ast_tree.value = dedent_code_block(
                        ast_tree.value.replace(f"{Con.PYNLINE}", "")
                    )
                else:
                    ast_tree = ast.Token(**meta)
        else:
            raise ValueError("Syntax Error encountered while parsing Jac program.")
    if not ast_tree:
        raise ValueError(f"node must be AstNode: {tree}")
    return ast_tree
