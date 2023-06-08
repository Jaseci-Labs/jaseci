"""
A
Docstring
"""

global ver = "0.0.1", what=6777;  # global variable

import:jac .utils;  # import a module

object mytype {}  # define a new type

node mynode {}  # define a new node

edge parent {}  # define a new edge

walker travelor {  # define a new walker
    can say_hello;
}

:walker:travelor:ability:say_hello {
    "Hello" |> print;  # |> is a pipe forward operator
}

test mytest
"A test of my functionality" {
   # test code here
}