"""
Command line tool for Jaseci
"""

import click
import sys
from inspect import signature, getmembers, isfunction

from core.utils.mem_hook import mem_hook
from core.master import master as master_class


master = master_class(h=mem_hook())


def test():
    print('a')
    pass


# Introspection on master interface to generate view class for master apis
for i in dir(master):
    if (i.startswith('api_')):
        func_sig = signature(getattr(master, i))
        globals()[i] = func_sig


def main():
    print(getmembers(sys.modules[__name__], isfunction))
