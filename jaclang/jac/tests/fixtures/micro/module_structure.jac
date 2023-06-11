"""
A
Docstring
"""

global ver = "0.0.1";  # global variable

import:jac .utils;  # import a module

object mytype {}  # define a new type

node mynode:this:that {}  # define a new node

edge parent {}  # define a new edge

walker travelor {  # define a new walker
    can say_hello;
}

:walker:travelor:ability:say_hello {
    "Hello" |> print;  # |> is a pipe forward operator
}

spawner myspawner {} # define a new spawner

func myfunc(): None {} # define a function

test mytest
"A test of my functionality" {
   # test code here
}