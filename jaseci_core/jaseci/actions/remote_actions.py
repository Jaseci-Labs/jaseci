"""
General action base class with automation for hot loading
"""
from importlib.util import spec_from_file_location, module_from_spec
from jaseci.utils.utils import logger
from fastapi import FastAPI

remote_actions = {}

app = FastAPI()


def jaseci_action(act_group=None):
    """Decorator for Jaseci Action interface"""
    def decorator_func(func):
        return assimilate_action(func, act_group)
    return decorator_func


def assimilate_action(func, act_group=None):
    """Helper for jaseci_action decorator"""
    global remote_actions
    act_group = [func.__module__.split(
        '.')[-1]] if act_group is None else act_group
    remote_actions[f"{'.'.join(act_group+[func.__name__])}"] = func
    return func
