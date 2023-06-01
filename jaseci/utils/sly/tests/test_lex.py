import pytest
from sly import Lexer

class CalcLexer(Lexer):
    # Set of token names.   This is always required
    tokens = {
        'ID',
        'NUMBER',
        'PLUS',
        'MINUS',
        'TIMES',
        'DIVIDE',
        'ASSIGN',
        'LT',
        'LE',
        }

    literals = { '(', ')' }

    # String containing ignored characters between tokens
    ignore = ' \t'

    # Regular expression rules for tokens
    ID      = r'[a-zA-Z_][a-zA-Z0-9_]*'
    PLUS    = r'\+'
    MINUS   = r'-'
    TIMES   = r'\*'
    DIVIDE  = r'/'
    ASSIGN  = r'='
    LE      = r'<='
    LT      = r'<'

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    # Ignored text
    ignore_comment = r'\#.*'

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    # Attached rule
    def ID(self, t):
        t.value = t.value.upper()
        return t

    def error(self, t):
        self.errors.append(t.value)
        self.index += 1
        if hasattr(self, 'return_error'):
            return t

    def __init__(self):
        self.errors = []

# Test basic recognition of various tokens and literals
def test_tokens():
    lexer = CalcLexer()
    toks = list(lexer.tokenize('abc 123 + - * / = < <= ( )'))
    types = [t.type for t in toks]
    vals = [t.value for t in toks]
    assert types == ['ID','NUMBER','PLUS','MINUS','TIMES','DIVIDE','ASSIGN','LT','LE','(',')']
    assert vals == ['ABC', 123, '+', '-', '*', '/', '=', '<', '<=', '(', ')']

# Test position tracking
def test_positions():
    lexer = CalcLexer()
    text = 'abc\n( )'
    toks = list(lexer.tokenize(text))
    lines = [t.lineno for t in toks ]
    indices = [t.index for t in toks ]
    ends = [t.end for t in toks]
    values = [ text[t.index:t.end] for t in toks ]
    assert values == ['abc', '(', ')']
    assert lines == [1, 2, 2]
    assert indices == [0, 4, 6]
    assert ends == [3, 5, 7]

    
# Test ignored comments and newlines
def test_ignored():
    lexer = CalcLexer()
    toks = list(lexer.tokenize('\n\n# A comment\n123\nabc\n'))
    types = [t.type for t in toks]
    vals = [t.value for t in toks]
    linenos = [t.lineno for t in toks]
    assert types == ['NUMBER', 'ID']
    assert vals == [123, 'ABC']
    assert linenos == [4,5]
    assert lexer.lineno == 6

# Test error handling
def test_error():
    lexer = CalcLexer()
    toks = list(lexer.tokenize('123 :+-'))
    types = [t.type for t in toks]
    vals = [t.value for t in toks]
    assert types == ['NUMBER', 'PLUS', 'MINUS']
    assert vals == [123, '+', '-']
    assert lexer.errors == [ ':+-' ]

# Test error token return handling
def test_error_return():
    lexer = CalcLexer()
    lexer.return_error = True
    toks = list(lexer.tokenize('123 :+-'))
    types = [t.type for t in toks]
    vals = [t.value for t in toks]
    assert types == ['NUMBER', 'ERROR', 'PLUS', 'MINUS']
    assert vals == [123, ':+-', '+', '-']
    assert lexer.errors == [ ':+-' ]


class ModernCalcLexer(Lexer):
    # Set of token names.   This is always required
    tokens = { ID, NUMBER, PLUS, MINUS, TIMES, DIVIDE, ASSIGN, LT, LE, IF, ELSE }
    literals = { '(', ')' }

    # String containing ignored characters between tokens
    ignore = ' \t'

    # Regular expression rules for tokens
    ID      = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['if'] = IF
    ID['else'] = ELSE

    NUMBER  = r'\d+'
    PLUS    = r'\+'
    MINUS   = r'-'
    TIMES   = r'\*'
    DIVIDE  = r'/'
    ASSIGN  = r'='
    LE      = r'<='
    LT      = r'<'

    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    # Ignored text
    ignore_comment = r'\#.*'

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    # Attached rule
    def ID(self, t):
        t.value = t.value.upper()
        return t

    def error(self, t):
        self.errors.append(t.value)
        self.index += 1
        if hasattr(self, 'return_error'):
            return t

    def __init__(self):
        self.errors = []


# Test basic recognition of various tokens and literals
def test_modern_tokens():
    lexer = ModernCalcLexer()
    toks = list(lexer.tokenize('abc if else 123 + - * / = < <= ( )'))
    types = [t.type for t in toks]
    vals = [t.value for t in toks]
    assert types == ['ID','IF','ELSE', 'NUMBER','PLUS','MINUS','TIMES','DIVIDE','ASSIGN','LT','LE','(',')']
    assert vals == ['ABC','if','else', 123, '+', '-', '*', '/', '=', '<', '<=', '(', ')']

# Test ignored comments and newlines
def test_modern_ignored():
    lexer = ModernCalcLexer()
    toks = list(lexer.tokenize('\n\n# A comment\n123\nabc\n'))
    types = [t.type for t in toks]
    vals = [t.value for t in toks]
    linenos = [t.lineno for t in toks]
    assert types == ['NUMBER', 'ID']
    assert vals == [123, 'ABC']
    assert linenos == [4,5]
    assert lexer.lineno == 6

# Test error handling
def test_modern_error():
    lexer = ModernCalcLexer()
    toks = list(lexer.tokenize('123 :+-'))
    types = [t.type for t in toks]
    vals = [t.value for t in toks]
    assert types == ['NUMBER', 'PLUS', 'MINUS']
    assert vals == [123, '+', '-']
    assert lexer.errors == [ ':+-' ]

# Test error token return handling
def test_modern_error_return():
    lexer = ModernCalcLexer()
    lexer.return_error = True
    toks = list(lexer.tokenize('123 :+-'))
    types = [t.type for t in toks]
    vals = [t.value for t in toks]
    assert types == ['NUMBER', 'ERROR', 'PLUS', 'MINUS']
    assert vals == [123, ':+-', '+', '-']
    assert lexer.errors == [ ':+-' ]



