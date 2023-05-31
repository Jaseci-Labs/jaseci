"""Lexer for Jac language."""

from sly.lex import Lexer, Token


class JacLexer(Lexer):
    """Jac Lexer."""

    tokens = {
        "FLOAT",
        "STRING",
        "DOC_STRING",
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
        "TYP_BYTES",
        "KW_TYPE",
        "KW_GRAPH",
        "KW_NODE",
        "KW_IGNORE",
        "KW_TAKE",
        "KW_SPAWN",
        "KW_WITH",
        "KW_ENTRY",
        "KW_EXIT",
        "KW_CONTEXT",
        "KW_INFO",
        "KW_DETAILS",
        "KW_IMPORT",
        "KW_FROM",
        "KW_AS",
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
        "ADD_EQ",
        "SUB_EQ",
        "MUL_EQ",
        "DIV_EQ",
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
        "KW_DELETE",
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
        "KW_HIDDEN",
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
    }

    # Ignored patterns
    ignore_ws = r"[ \t]+"
    ignore_newline = r"[\r\n]+"
    ignore_comment = r"/\*.*?\*/"
    ignore_line_comment = r"//.*"
    ignore_py_comment = r"#.*"

    # Regular expression rules for tokens
    FLOAT = r"(\d+)?\.\d+"
    DOC_STRING = r'"""[^"]*"""|\'\'\'[^\']*\'\'\''
    STRING = r'"[^"\r\n]*"|\'[^\'\r\n]*\''
    BOOL = r"True|False"
    INT = r"\d+"
    NULL = r"None"
    NAME = r"[a-zA-Z_][a-zA-Z0-9_]*"

    # Keywords
    NAME["str"] = "TYP_STRING"
    NAME["int"] = "TYP_INT"
    NAME["float"] = "TYP_FLOAT"
    NAME["list"] = "TYP_LIST"
    NAME["dict"] = "TYP_DICT"
    NAME["bool"] = "TYP_BOOL"
    NAME["bytes"] = "TYP_BYTES"
    NAME["type"] = "KW_TYPE"
    NAME["graph"] = "KW_GRAPH"
    NAME["node"] = "KW_NODE"
    NAME["ignore"] = "KW_IGNORE"
    NAME["take"] = "KW_TAKE"
    NAME["spawn"] = "KW_SPAWN"
    NAME["with"] = "KW_WITH"
    NAME["entry"] = "KW_ENTRY"
    NAME["exit"] = "KW_EXIT"
    NAME["context"] = "KW_CONTEXT"
    NAME["info"] = "KW_INFO"
    NAME["details"] = "KW_DETAILS"
    NAME["import"] = "KW_IMPORT"
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
    NAME["del"] = "KW_DELETE"
    NAME["try"] = "KW_TRY"
    NAME["in"] = "KW_IN"
    NAME["not"] = "NOT"
    NAME["anchor"] = "KW_ANCHOR"
    NAME["has"] = "KW_HAS"
    NAME["global"] = "KW_GLOBAL"
    NAME["hidden"] = "KW_HIDDEN"
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
    CARROW_L_p2 = r"]\+"
    CARROW_R_p1 = r"\+\["
    CARROW_R_p2 = r"]\+>"

    # Token rules
    KW_AND = r"&&"
    KW_OR = r"\|\|"
    NOT = r"!"
    DBL_COLON = r"::"
    COLON = r":"
    LBRACE = r"{"
    RBRACE = r"}"
    SEMI = r";"
    EE = r"=="
    EQ = r"="
    ADD_EQ = r"\+="
    SUB_EQ = r"-="
    MUL_EQ = r"\*="
    DIV_EQ = r"/="
    CPY_EQ = r":="
    KW_REF = r"&"
    DOT = r"\."
    LT = r"<"
    GT = r">"
    LTE = r"<="
    GTE = r">="
    NE = r"!="
    COMMA = r","
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

    def DOC_STRING(self: "JacLexer", t: Token) -> Token:  # noqa: N802
        """Add docstring to lexer."""
        self.lineno += t.value.count("\n")
        self.lineno += t.value.count("\r")
        return t

    # Error handling rule
    def error(self: "JacLexer", t: Token) -> None:
        """Raise an error for illegal characters."""
        print(f"Illegal character '{t.value[0]}' at line {self.lineno}")
        self.index += 1
