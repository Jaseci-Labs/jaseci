# type: ignore
"""Lexer for Jac language."""

from jaclang.utils.sly.lex import Lexer, Token


class JacLexer(Lexer):
    """Jac Lexer."""

    tokens = {
        "FLOAT",
        "STRING",
        "DOC_STRING",
        "FSTRING",
        "BOOL",
        "INT",
        "HEX",
        "BIN",
        "OCT",
        "NULL",
        "NAME",
        "TYP_STRING",
        "TYP_INT",
        "TYP_FLOAT",
        "TYP_LIST",
        "TYP_TUPLE",
        "TYP_SET",
        "TYP_DICT",
        "TYP_BOOL",
        "TYP_BYTES",
        "KW_OBJECT",
        "TYP_ANY",
        "TYP_TYPE",
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
        "KW_SYNC",
        "KW_TEST",
        "KW_ASSERT",
        "COLON",
        "PIPE_FWD",
        "PIPE_BKWD",
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
        "CARROW_BI",
        "CARROW_L_p1",
        "CARROW_L_p2",
        "CARROW_R_p1",
        "CARROW_R_p2",
        "GLOBAL_OP",
        "HERE_OP",
        "VISITOR_OP",
        "WALKER_OP",
        "NODE_OP",
        "EDGE_OP",
        "OBJECT_OP",
        "ABILITY_OP",
        "SPAWN_OP",
        "ELVIS_OP",
        "RETURN_HINT",
        "NULL_OK",
    }

    # Ignored patterns
    ignore_ws = r"[ \t]+"
    ignore_newline = r"[\r\n]+"
    ignore_comment = r"/\*(.|\n|\r)*\*/"
    ignore_line_comment = r"//.*"
    ignore_py_comment = r"#.*"

    # Regular expression rules for tokens
    FLOAT = r"(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?"
    DOC_STRING = r'"""[^"]*"""|\'\'\'[^\']*\'\'\''
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
    NAME = r"[a-zA-Z_][a-zA-Z0-9_]*"

    # Keywords
    NAME["str"] = "TYP_STRING"
    NAME["int"] = "TYP_INT"
    NAME["float"] = "TYP_FLOAT"
    NAME["list"] = "TYP_LIST"
    NAME["tuple"] = "TYP_TUPLE"
    NAME["set"] = "TYP_SET"
    NAME["dict"] = "TYP_DICT"
    NAME["bool"] = "TYP_BOOL"
    NAME["bytes"] = "TYP_BYTES"
    NAME["object"] = "KW_OBJECT"
    NAME["any"] = "TYP_ANY"
    NAME["type"] = "TYP_TYPE"
    NAME["node"] = "KW_NODE"
    NAME["ignore"] = "KW_IGNORE"
    NAME["visit"] = "KW_VISIT"
    NAME["revisit"] = "KW_REVISIT"
    NAME["spawn"] = "KW_SPAWN"
    NAME["with"] = "KW_WITH"
    NAME["entry"] = "KW_ENTRY"
    NAME["exit"] = "KW_EXIT"
    NAME["import"] = "KW_IMPORT"
    NAME["include"] = "KW_INCLUDE"
    NAME["from"] = "KW_FROM"
    NAME["as"] = "KW_AS"
    NAME["edge"] = "KW_EDGE"
    NAME["walker"] = "KW_WALKER"
    NAME["async"] = "KW_ASYNC"
    NAME["sync"] = "KW_SYNC"
    NAME["test"] = "KW_TEST"
    NAME["assert"] = "KW_ASSERT"
    NAME["and"] = "KW_AND"
    NAME["or"] = "KW_OR"
    NAME["if"] = "KW_IF"
    NAME["elif"] = "KW_ELIF"
    NAME["else"] = "KW_ELSE"
    NAME["for"] = "KW_FOR"
    NAME["to"] = "KW_TO"
    NAME["by"] = "KW_BY"
    NAME["while"] = "KW_WHILE"
    NAME["continue"] = "KW_CONTINUE"
    NAME["break"] = "KW_BREAK"
    NAME["disengage"] = "KW_DISENGAGE"
    NAME["yield"] = "KW_YIELD"
    NAME["skip"] = "KW_SKIP"
    NAME["report"] = "KW_REPORT"
    NAME["return"] = "KW_RETURN"
    NAME["del"] = "KW_DELETE"
    NAME["try"] = "KW_TRY"
    NAME["except"] = "KW_EXCEPT"
    NAME["finally"] = "KW_FINALLY"
    NAME["in"] = "KW_IN"
    NAME["is"] = "KW_IS"
    NAME["not"] = "NOT"
    NAME["priv"] = "KW_PRIV"
    NAME["pub"] = "KW_PUB"
    NAME["prot"] = "KW_PROT"
    NAME["has"] = "KW_HAS"
    NAME["global"] = "KW_GLOBAL"
    NAME["can"] = "KW_CAN"

    # Special Arrow Tokens
    ARROW_L = r"<--"
    ARROW_R = r"-->"
    ARROW_BI = r"<-->"
    ARROW_L_p1 = r"<-\["
    ARROW_L_p2 = r"]-"
    ARROW_R_p1 = r"-\["
    ARROW_R_p2 = r"]->"
    CARROW_L = r"<\+\+"
    CARROW_R = r"\+\+>"
    CARROW_BI = r"<\+\+>"
    CARROW_L_p1 = r"<\+\["
    CARROW_R_p2 = r"]\+>"
    CARROW_L_p2 = r"]\+"
    CARROW_R_p1 = r"\+\["

    # Just special
    GLOBAL_OP = r":g:|:global:"
    HERE_OP = r":h:|:here:"
    VISITOR_OP = r":v:|:visitor:"
    WALKER_OP = r":w:|:walker:"
    NODE_OP = r":n:|:node:"
    EDGE_OP = r":e:|:edge:"
    OBJECT_OP = r":o:|:object:"
    ABILITY_OP = r":a:|:ability:"
    SPAWN_OP = r":\+:"
    RETURN_HINT = r"->"
    ELVIS_OP = r"\?:"
    NULL_OK = r"\?"

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
    PIPE_FWD = r"\|>"
    PIPE_BKWD = r"<\|"
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

    def ignore_newline(self, t: Token) -> Token:
        """Increment line number."""
        self.lineno += len(t.value)
        return t

    def DOC_STRING(self, t: Token) -> Token:  # noqa: N802
        """Add docstring to lexer."""
        self.lineno += t.value.count("\n")
        self.lineno += t.value.count("\r")
        return t

    # Error handling rule
    def error(self, t: Token) -> None:
        """Raise an error for illegal characters."""
        print(f"Illegal character '{t.value[0]}' at line {self.lineno}")
        self.index += 1
