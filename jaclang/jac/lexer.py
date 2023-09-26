"""Lexer for Jac language."""
from typing import Generator

from jaclang.jac.transform import ABCLexerMeta, Transform
from jaclang.vendor.sly.lex import Lexer, Token


class JacLexer(Lexer, Transform, metaclass=ABCLexerMeta):
    """Jac Lexer."""

    def __init__(
        self,
        mod_path: str,
        input_ir: str,
        base_path: str = "",
        prior: Transform | None = None,
        fstr_override: bool = False,
    ) -> None:
        """Initialize lexer."""
        self.fstr_override = fstr_override
        Transform.__init__(self, mod_path, input_ir, base_path, prior)  # type: ignore
        self.ir: Generator = self.ir

    tokens = {
        "FLOAT",
        "STRING",
        "DOC_STRING",
        "PYNLINE",
        "FSTRING",
        "BOOL",
        "INT",
        "HEX",
        "BIN",
        "OCT",
        "NULL",
        "NAME",
        "KWESC_NAME",
        "TYP_STRING",
        "TYP_INT",
        "TYP_FLOAT",
        "TYP_LIST",
        "TYP_TUPLE",
        "TYP_SET",
        "TYP_DICT",
        "TYP_BOOL",
        "TYP_BYTES",
        "TYP_ANY",
        "TYP_TYPE",
        "KW_FREEZE",
        "KW_ABSTRACT",
        "KW_OBJECT",
        "KW_ENUM",
        "KW_NODE",
        "KW_IGNORE",
        "KW_VISIT",
        "KW_REVISIT",
        "KW_SPAWN",
        "KW_WITH",
        "KW_ENTRY",
        "KW_EXIT",
        "KW_IMPORT",
        "KW_INCLUDE",
        "KW_FROM",
        "KW_AS",
        "KW_EDGE",
        "KW_WALKER",
        "KW_ASYNC",
        "KW_AWAIT",
        "KW_TEST",
        "KW_ASSERT",
        "COLON",
        "PIPE_FWD",
        "PIPE_BKWD",
        "DOT_FWD",
        "DOT_BKWD",
        "LBRACE",
        "RBRACE",
        "SEMI",
        "EQ",
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
        "WALRUS_EQ",
        "KW_AND",
        "KW_OR",
        "KW_IF",
        "KW_ELIF",
        "KW_ELSE",
        "KW_FOR",
        "KW_TO",
        "KW_BY",
        "KW_WHILE",
        "KW_CONTINUE",
        "KW_BREAK",
        "KW_DISENGAGE",
        "KW_YIELD",
        "KW_SKIP",
        "KW_REPORT",
        "KW_RETURN",
        "KW_DELETE",
        "KW_TRY",
        "KW_EXCEPT",
        "KW_FINALLY",
        "KW_RAISE",
        "DOT",
        "NOT",
        "EE",
        "LT",
        "GT",
        "LTE",
        "GTE",
        "NE",
        "KW_IN",
        "KW_IS",
        "KW_NIN",
        "KW_ISN",
        "KW_PRIV",
        "KW_PUB",
        "KW_PROT",
        "KW_HAS",
        "KW_GLOBAL",
        "COMMA",
        "KW_CAN",
        "KW_STATIC",
        "PLUS",
        "MINUS",
        "STAR_MUL",
        "FLOOR_DIV",
        "DIV",
        "MOD",
        "BW_AND",
        "BW_OR",
        "BW_XOR",
        "BW_NOT",
        "LSHIFT",
        "RSHIFT",
        "STAR_POW",
        "LPAREN",
        "RPAREN",
        "LSQUARE",
        "RSQUARE",
        "ARROW_L",
        "ARROW_R",
        "ARROW_BI",
        "ARROW_L_p1",
        "ARROW_L_p2",
        "ARROW_R_p1",
        "ARROW_R_p2",
        "CARROW_L",
        "CARROW_R",
        "CARROW_L_p1",
        "CARROW_L_p2",
        "CARROW_R_p1",
        "CARROW_R_p2",
        "GLOBAL_OP",
        "HERE_OP",
        "SELF_OP",
        "INIT_OP",
        "SUPER_OP",
        "ROOT_OP",
        "WALKER_OP",
        "NODE_OP",
        "EDGE_OP",
        "OBJECT_OP",
        "ENUM_OP",
        "ABILITY_OP",
        "A_PIPE_FWD",
        "A_PIPE_BKWD",
        "ELVIS_OP",
        "RETURN_HINT",
        "NULL_OK",
        "DECOR_OP",
    }

    # Ignored patterns
    ignore_ws = r"[ \t]+"
    ignore_newline = r"[\r\n]+"  # type: ignore
    ignore_comment = r"#\*(.|\n|\r)*?\*#"  # type: ignore
    ignore_py_comment = r"#.*"

    # Regular expression rules for tokens
    FLOAT = r"(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?"
    DOC_STRING = r'"""(.|\n|\r)*?"""|\'\'\'(.|\n|\r)*?\'\'\''  # type: ignore
    PYNLINE = r"::py::(.|\n|\r)*?::py::"  # type: ignore
    FSTRING = r'f"[^"\r\n]*"|f\'[^\'\r\n]*\''
    STRING = r'"[^"\r\n]*"|\'[^\'\r\n]*\''
    BOOL = r"True|False"
    KW_NIN = r"\bnot\s+in\b"
    KW_ISN = r"\bis\s+not\b"
    HEX = r"0[xX][0-9a-fA-F_]+"
    BIN = r"0[bB][01_]+"
    OCT = r"0[oO][0-7_]+"
    INT = r"[0-9][0-9_]*"
    NULL = r"None"
    KWESC_NAME = r"<>[a-zA-Z_][a-zA-Z0-9_]*"
    NAME = r"[a-zA-Z_][a-zA-Z0-9_]*"

    # Keywords
    NAME["str"] = "TYP_STRING"  # type: ignore
    NAME["int"] = "TYP_INT"  # type: ignore
    NAME["float"] = "TYP_FLOAT"  # type: ignore
    NAME["list"] = "TYP_LIST"  # type: ignore
    NAME["tuple"] = "TYP_TUPLE"  # type: ignore
    NAME["set"] = "TYP_SET"  # type: ignore
    NAME["dict"] = "TYP_DICT"  # type: ignore
    NAME["bool"] = "TYP_BOOL"  # type: ignore
    NAME["bytes"] = "TYP_BYTES"  # type: ignore
    NAME["any"] = "TYP_ANY"  # type: ignore
    NAME["type"] = "TYP_TYPE"  # type: ignore
    NAME["froz"] = "KW_FREEZE"  # type: ignore
    NAME["abstract"] = "KW_ABSTRACT"  # type: ignore
    NAME["object"] = "KW_OBJECT"  # type: ignore
    NAME["enum"] = "KW_ENUM"  # type: ignore
    NAME["node"] = "KW_NODE"  # type: ignore
    NAME["ignore"] = "KW_IGNORE"  # type: ignore
    NAME["visit"] = "KW_VISIT"  # type: ignore
    NAME["revisit"] = "KW_REVISIT"  # type: ignore
    NAME["spawn"] = "KW_SPAWN"  # type: ignore
    NAME["with"] = "KW_WITH"  # type: ignore
    NAME["entry"] = "KW_ENTRY"  # type: ignore
    NAME["exit"] = "KW_EXIT"  # type: ignore
    NAME["import"] = "KW_IMPORT"  # type: ignore
    NAME["include"] = "KW_INCLUDE"  # type: ignore
    NAME["from"] = "KW_FROM"  # type: ignore
    NAME["as"] = "KW_AS"  # type: ignore
    NAME["edge"] = "KW_EDGE"  # type: ignore
    NAME["walker"] = "KW_WALKER"  # type: ignore
    NAME["async"] = "KW_ASYNC"  # type: ignore
    NAME["await"] = "KW_AWAIT"  # type: ignore
    NAME["test"] = "KW_TEST"  # type: ignore
    NAME["assert"] = "KW_ASSERT"  # type: ignore
    NAME["and"] = "KW_AND"  # type: ignore
    NAME["or"] = "KW_OR"  # type: ignore
    NAME["if"] = "KW_IF"  # type: ignore
    NAME["elif"] = "KW_ELIF"  # type: ignore
    NAME["else"] = "KW_ELSE"  # type: ignore
    NAME["for"] = "KW_FOR"  # type: ignore
    NAME["to"] = "KW_TO"  # type: ignore
    NAME["by"] = "KW_BY"  # type: ignore
    NAME["while"] = "KW_WHILE"  # type: ignore
    NAME["continue"] = "KW_CONTINUE"  # type: ignore
    NAME["break"] = "KW_BREAK"  # type: ignore
    NAME["disengage"] = "KW_DISENGAGE"  # type: ignore
    NAME["yield"] = "KW_YIELD"  # type: ignore
    NAME["skip"] = "KW_SKIP"  # type: ignore
    NAME["report"] = "KW_REPORT"  # type: ignore
    NAME["return"] = "KW_RETURN"  # type: ignore
    NAME["del"] = "KW_DELETE"  # type: ignore
    NAME["try"] = "KW_TRY"  # type: ignore
    NAME["except"] = "KW_EXCEPT"  # type: ignore
    NAME["finally"] = "KW_FINALLY"  # type: ignore
    NAME["raise"] = "KW_RAISE"  # type: ignore
    NAME["in"] = "KW_IN"  # type: ignore
    NAME["is"] = "KW_IS"  # type: ignore
    NAME["not"] = "NOT"  # type: ignore
    NAME["private"] = "KW_PRIV"  # type: ignore
    NAME["public"] = "KW_PUB"  # type: ignore
    NAME["protected"] = "KW_PROT"  # type: ignore
    NAME["has"] = "KW_HAS"  # type: ignore
    NAME["global"] = "KW_GLOBAL"  # type: ignore
    NAME["can"] = "KW_CAN"  # type: ignore
    NAME["static"] = "KW_STATIC"  # type: ignore

    # Special Arrow Tokens
    ARROW_L = r"<--"
    ARROW_R = r"-->"
    ARROW_BI = r"<-->"
    ARROW_L_p1 = r"<-\["
    ARROW_R_p2 = r"]->"
    ARROW_L_p2 = r"]-"
    ARROW_R_p1 = r"-\["
    CARROW_L = r"<\+\+"
    CARROW_R = r"\+\+>"
    CARROW_L_p1 = r"<\+\["
    CARROW_R_p2 = r"]\+>"
    CARROW_L_p2 = r"]\+"
    CARROW_R_p1 = r"\+\["

    # Just special
    GLOBAL_OP = r":g:|:global:"
    HERE_OP = r"<h>|<here>"
    SELF_OP = r"<s>|<self>"
    INIT_OP = r"<i>|<init>"
    SUPER_OP = r"<super>"
    ROOT_OP = r"<r>|<root>"
    WALKER_OP = r":w:|:walker:"
    NODE_OP = r":n:|:node:"
    EDGE_OP = r":e:|:edge:"
    OBJECT_OP = r":o:|:object:"
    ENUM_OP = r":enum:"
    ABILITY_OP = r":a:|:ability:"
    A_PIPE_FWD = r":>"
    A_PIPE_BKWD = r"<:"
    PIPE_FWD = r"\|>"
    PIPE_BKWD = r"<\|"
    DOT_FWD = r"\.>"
    DOT_BKWD = r"<\."
    RETURN_HINT = r"->"
    ELVIS_OP = r"\?:"
    NULL_OK = r"\?"
    DECOR_OP = r"@"

    # Token rules
    KW_AND = r"&&"
    KW_OR = r"\|\|"
    ADD_EQ = r"\+="
    SUB_EQ = r"-="
    MUL_EQ = r"\*="
    FLOOR_DIV_EQ = r"//="
    DIV_EQ = r"/="
    MOD_EQ = r"%="
    BW_AND_EQ = r"&="
    BW_OR_EQ = r"\|="
    BW_XOR_EQ = r"\^="
    BW_NOT_EQ = r"~="
    LSHIFT_EQ = r"<<="
    RSHIFT_EQ = r">>="
    LSHIFT = r"<<"
    RSHIFT = r">>"
    LTE = r"<="
    GTE = r">="
    NE = r"!="
    NOT = r"!"
    WALRUS_EQ = r":="
    COLON = r":"
    LBRACE = r"{"
    RBRACE = r"}"
    SEMI = r";"
    EE = r"=="
    EQ = r"="
    DOT = r"\."
    LT = r"<"
    GT = r">"
    COMMA = r","
    PLUS = r"\+"
    MINUS = r"-"
    STAR_POW = r"\*\*"
    STAR_MUL = r"\*"
    FLOOR_DIV = r"//"
    DIV = r"/"
    MOD = r"%"
    BW_AND = r"&"
    BW_OR = r"\|"
    BW_XOR = r"\^"
    BW_NOT = r"~"
    LPAREN = r"\("
    RPAREN = r"\)"
    LSQUARE = r"\["
    RSQUARE = r"\]"

    def ignore_newline(self, t: Token) -> Token:  # noqa
        """Increment line number."""
        self.lineno += len(t.value)
        return t

    def ignore_comment(self, t: Token) -> Token:  # noqa
        """Add docstring to lexer."""
        self.lineno += t.value.count("\n")
        self.lineno += t.value.count("\r")
        return t

    def DOC_STRING(self, t: Token) -> Token:  # noqa
        """Add docstring to lexer."""
        self.lineno += t.value.count("\n")
        self.lineno += t.value.count("\r")
        return t

    def PYNLINE(self, t: Token) -> Token:  # noqa
        """Add docstring to lexer."""
        self.lineno += t.value.count("\n")
        self.lineno += t.value.count("\r")
        return t

    # Transform Implementations
    # -------------------------
    def transform(self, ir: str) -> Generator:
        """Tokenize the input."""
        return self.tokenize(ir)

    def tokenize(self, text: str) -> Generator:
        """Tokenize override for no module level docstring."""
        has_doc_string_start = False
        for tok in super().tokenize(text):
            if (
                tok.type != "DOC_STRING"
                and not has_doc_string_start
                and not self.fstr_override
            ):
                dtok = Token()
                dtok.type = "DOC_STRING"
                dtok.value = '""""""'
                dtok.lineno = 1
                dtok.lineidx = 0
                dtok.index = 0
                dtok.end = 0
                yield dtok
            has_doc_string_start = True
            yield tok

    def error(self, t: Token) -> None:
        """Raise an error for illegal characters."""
        self.cur_line = self.lineno
        self.log_error(msg=f"Illegal character '{t.value[0]}'")
        self.index += 1
