from core import actions
import pkgutil
import importlib
from inspect import getmembers
from inspect import isfunction


def find_action(func_name):
    """
    Search for actions in action library and return func as [modname, funcname]
    if found
    """
    prefix = actions.__name__ + "."
    for importer, modname, ispkg in \
            pkgutil.iter_modules(actions.__path__, prefix):
        if(not ispkg):
            for i in dir(importlib.import_module(modname)):
                candidate = f'{modname}.{i}'
                if(candidate.endswith(func_name)):
                    return [modname, i]


def get_action_set(func_src):
    """
    Search for actions in action library and return func as [modname, funcname]
    if found
    """
    ret = []
    prefix = actions.__name__ + "."
    for importer, modname, ispkg in \
            pkgutil.iter_modules(actions.__path__, prefix):
        if(not ispkg):
            for i in getmembers(importlib.import_module(modname)):
                if (modname.endswith(func_src)):
                    if (isfunction(i[1])):
                        ret.append(f'{func_src}.{i[0]}')
    return ret
