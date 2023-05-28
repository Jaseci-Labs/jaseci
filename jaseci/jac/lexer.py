"""Lexer for Jac language."""

from sly.lex import Lexer, Token


class JacLexer(Lexer):
    """Jac Lexer."""

    tokens = {
        "FLOAT",
        "STRING",
        "BOOL",
        "INT",
        "NULL",
        "NAME",
        "TYP_STRING",
        "TYP_INT",
        "TYP_FLOAT",
        "TYP_LIST",
        "TYP_DICT",
        "TYP_BOOL",
        "KW_TYPE",
        "KW_GRAPH",
        "KW_NODE",
        "KW_IGNORE",
        "KW_TAKE",
        "KW_SPAWN",
        "KW_WITH",
        "KW_ENTRY",
        "KW_EXIT",
        "KW_LENGTH",
        "KW_KEYS",
        "KW_CONTEXT",
        "KW_INFO",
        "KW_DETAILS",
        "KW_ACTIVITY",
        "KW_IMPORT",
        "KW_EDGE",
        "KW_WALKER",
        "KW_ASYNC",
        "KW_SYNC",
        "KW_TEST",
        "KW_ASSERT",
        "COLON",
        "DBL_COLON",
        "LBRACE",
        "RBRACE",
        "SEMI",
        "EQ",
        "PEQ",
        "MEQ",
        "TEQ",
        "DEQ",
        "CPY_EQ",
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
        "KW_DESTROY",
        "KW_TRY",
        "KW_REF",
        "DOT",
        "NOT",
        "EE",
        "LT",
        "GT",
        "LTE",
        "GTE",
        "NE",
        "KW_IN",
        "KW_ANCHOR",
        "KW_HAS",
        "KW_GLOBAL",
        "KW_PRIVATE",
        "COMMA",
        "KW_CAN",
        "PLUS",
        "MINUS",
        "STAR_MUL",
        "DIV",
        "MOD",
        "POW",
        "LPAREN",
        "RPAREN",
        "LSQUARE",
        "RSQUARE",
    }

    # Ignored patterns
    ignore_ws = r"[ \t]+"
    ignore_newline = r"[\r\n]+"
    ignore_comment = r"/\*.*?\*/"
    ignore_line_comment = r"//.*"
    ignore_py_comment = r"#.*"

    # Regular expression rules for tokens
    FLOAT = r"(\d+)?\.\d+"
    STRING = r'"[^"\r\n]*"|\'[^\'\r\n]*\''
    BOOL = r"True|False"
    INT = r"\d+"
    NULL = r"None"
    NAME = r"[a-zA-Z_][a-zA-Z0-9_]*"

    # Token rules
    TYP_STRING = r"str"
    TYP_INT = r"int"
    TYP_FLOAT = r"float"
    TYP_LIST = r"list"
    TYP_DICT = r"dict"
    TYP_BOOL = r"bool"
    KW_TYPE = r"type"
    KW_GRAPH = r"graph"
    KW_NODE = r"node"
    KW_IGNORE = r"ignore"
    KW_TAKE = r"take"
    KW_SPAWN = r"spawn"
    KW_WITH = r"with"
    KW_ENTRY = r"entry"
    KW_EXIT = r"exit"
    KW_LENGTH = r"length"
    KW_KEYS = r"keys"
    KW_CONTEXT = r"context"
    KW_INFO = r"info"
    KW_DETAILS = r"details"
    KW_ACTIVITY = r"activity"
    KW_IMPORT = r"import"
    KW_EDGE = r"edge"
    KW_WALKER = r"walker"
    KW_ASYNC = r"async"
    KW_SYNC = r"sync"
    KW_TEST = r"test"
    KW_ASSERT = r"assert"
    COLON = r":"
    DBL_COLON = r"::"
    LBRACE = r"{"
    RBRACE = r"}"
    SEMI = r";"
    EQ = r"="
    PEQ = r"\+="
    MEQ = r"-="
    TEQ = r"\*="
    DEQ = r"/="
    CPY_EQ = r":="
    KW_AND = r"and|&&"
    KW_OR = r"or|\|\|"
    KW_IF = r"if"
    KW_ELIF = r"elif"
    KW_ELSE = r"else"
    KW_FOR = r"for"
    KW_TO = r"to"
    KW_BY = r"by"
    KW_WHILE = r"while"
    KW_CONTINUE = r"continue"
    KW_BREAK = r"break"
    KW_DISENGAGE = r"disengage"
    KW_YIELD = r"yield"
    KW_SKIP = r"skip"
    KW_REPORT = r"report"
    KW_DESTROY = r"destroy"
    KW_TRY = r"try"
    KW_REF = r"&"
    DOT = r"\."
    NOT = r"!|not"
    EE = r"=="
    LT = r"<"
    GT = r">"
    LTE = r"<="
    GTE = r">="
    NE = r"!="
    KW_IN = r"in"
    KW_ANCHOR = r"anchor"
    KW_HAS = r"has"
    KW_GLOBAL = r"global"
    KW_PRIVATE = r"private"
    COMMA = r","
    KW_CAN = r"can"
    PLUS = r"\+"
    MINUS = r"-"
    STAR_MUL = r"\*"
    DIV = r"/"
    MOD = r"%"
    POW = r"\^"
    LPAREN = r"\("
    RPAREN = r"\)"
    LSQUARE = r"\["
    RSQUARE = r"\]"

    def ignore_newline(self: "JacLexer", t: Token) -> Token:
        """Increment line number."""
        self.lineno += len(t.value)
        return t

    # Error handling rule
    def error(self: "JacLexer", t: Token) -> None:
        """Raise an error for illegal characters."""
        print(f"Illegal character '{t.value[0]}' at line {self.lineno}")
        self.index += 1
