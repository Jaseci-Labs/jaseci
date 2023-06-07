.. sly documentation master file, created by
   sphinx-quickstart on Wed Sep  7 13:23:26 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

SLY (Sly Lex Yacc)
==================

THIS IS A WORK IN PROGRESS.  NO OFFICIAL RELEASE HAS BEEN MADE.
USE AT YOUR OWN RISK.

Requirements
============

SLY requires the use of Python 3.6 or greater.  Older versions
of Python are not supported.

Overview
========

SLY is a 100% Python implementation of the lex and yacc tools
commonly used to write parsers and compilers.  Parsing is
based on the same LALR(1) algorithm used by many yacc tools.
Here are a few notable features:

 -  SLY provides *very* extensive error reporting and diagnostic 
    information to assist in parser construction.  The original
    implementation was developed for instructional purposes.  As
    a result, the system tries to identify the most common types
    of errors made by novice users.  

 -  SLY provides full support for empty productions, error recovery,
    precedence specifiers, and moderately ambiguous grammars.

 -  SLY uses various Python metaprogramming features to specify
    lexers and parsers.  There are no generated files or extra
    steps involved. You simply write Python code and run it.

 -  SLY can be used to build parsers for "real" programming languages.
    Although it is not ultra-fast due to its Python implementation,
    SLY can be used to parse grammars consisting of several hundred
    rules (as might be found for a language like C).  

SLY originates from the PLY project (http://www.dabeaz.com/ply/index.html).
However, it's been modernized a bit.  In fact, don't expect any code
previously written for PLY to work. That said, most of the things 
that were possible in PLY are also possible in SLY. 

An Example
==========

SLY is probably best illustrated by an example.  Here's what it
looks like to write a parser that can evaluate simple arithmetic
expressions and store variables::

    # -----------------------------------------------------------------------------
    # calc.py
    # -----------------------------------------------------------------------------

    from sly import Lexer, Parser

    class CalcLexer(Lexer):
        tokens = { NAME, NUMBER }
        ignore = ' \t'
        literals = { '=', '+', '-', '*', '/', '(', ')' }

        # Tokens
        NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

        @_(r'\d+')
        def NUMBER(self, t):
            t.value = int(t.value)
            return t

        @_(r'\n+')
        def newline(self, t):
            self.lineno += t.value.count('\n')

        def error(self, t):
            print("Illegal character '%s'" % t.value[0])
            self.index += 1

    class CalcParser(Parser):
        tokens = CalcLexer.tokens

        precedence = (
            ('left', '+', '-'),
            ('left', '*', '/'),
            ('right', 'UMINUS'),
            )

        def __init__(self):
            self.names = { }

        @_('NAME "=" expr')
        def statement(self, p):
            self.names[p.NAME] = p.expr

        @_('expr')
        def statement(self, p):
            print(p.expr)

        @_('expr "+" expr')
        def expr(self, p):
            return p.expr0 + p.expr1

        @_('expr "-" expr')
        def expr(self, p):
            return p.expr0 - p.expr1

        @_('expr "*" expr')
        def expr(self, p):
            return p.expr0 * p.expr1

        @_('expr "/" expr')
        def expr(self, p):
            return p.expr0 / p.expr1

        @_('"-" expr %prec UMINUS')
        def expr(self, p):
            return -p.expr

        @_('"(" expr ")"')
        def expr(self, p):
            return p.expr

        @_('NUMBER')
        def expr(self, p):
            return p.NUMBER

        @_('NAME')
        def expr(self, p):
            try:
                return self.names[p.NAME]
            except LookupError:
                print("Undefined name '%s'" % p.NAME)
                return 0

    if __name__ == '__main__':
        lexer = CalcLexer()
        parser = CalcParser()
        while True:
            try:
                text = input('calc > ')
            except EOFError:
                break
            if text:
                parser.parse(lexer.tokenize(text))
 

More Documentation
==================

Contents:

.. toctree::
   :maxdepth: 2

   sly

Resources
=========

For a detailed overview of parsing theory, consult the excellent
book "Compilers : Principles, Techniques, and Tools" by Aho, Sethi, and
Ullman.  The topics found in "Lex & Yacc" by Levine, Mason, and Brown
may also be useful.

The GitHub page for SLY can be found at:

     https://github.com/dabeaz/sly

Please direct bug reports and pull requests to the GitHub page.
To contact me directly, send email to dave@dabeaz.com or contact
me on Twitter (@dabeaz).

