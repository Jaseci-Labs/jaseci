"""
Command line tool for Jaseci
"""

import click
from inspect import signature

from core.utils.mem_hook import mem_hook
from core.master import master as master_class


master = master_class(h=mem_hook())


def api_to_cmd(**kwargs):
    print(kwargs)


# Introspection on master interface to generate view class for master apis
api_funcs = {}
for i in dir(master):
    if (i.startswith('api_')):
        func_sig = signature(getattr(master, i))
        api_funcs[i] = func_sig


def main():
    print(api_funcs)
