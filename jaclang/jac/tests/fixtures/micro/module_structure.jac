"""
A
Docstring
"""

a="blah";
global ver = "0.0.1";  # global variable

import:jac .utils;  # import a module
import:py os; # import a python module
include:jac .mod_defs;  # includes a file

object mytype {}  # define a new type

node mynode:this:that {}  # define a new node

edge parent {}  # define a new edge

walker travelor {  # define a new walker
    can say_hello;
}

:walker:travelor:ability:say_hello {
    "Hello" |> print;  # |> is a pipe forward operator
}

can myablty -> int {} # define a data spacial freestyle ability

can myfunc() -> None {} # define a function

with entry {
    # module level freestyle code
}

test mytest
"A test of my functionality" {
   # test code here
}