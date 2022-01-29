"""
General action base class with automation for hot loading
"""
from jaseci.utils.utils import logger
from fastapi import FastAPI
from pydantic import validate_arguments, BaseModel
import inspect

remote_actions = []

app = FastAPI()


def jaseci_action(act_group=None):
    """Decorator for Jaseci Action interface"""
    caller_globals = dict(inspect.getmembers(
        inspect.stack()[1][0]))["f_globals"]
    if 'app' not in caller_globals:
        caller_globals['app'] = app

    def decorator_func(func):
        return assimilate_action(func, act_group)
    return decorator_func


def assimilate_action(func, act_group=None):
    """Helper for jaseci_action decorator"""
    # Construct list of action apis available
    act_group = [func.__module__.split(
        '.')[-1]] if act_group is None else act_group
    remote_actions.append(f"{'.'.join(act_group+[func.__name__])}")

    # Need to get pydatic model for func signature for fastAPI post
    model = validate_arguments(func).model

    keep_fields = {}
    for i in model.__fields__.keys():
        if i in func.__code__.co_varnames:
            keep_fields[i] = model.__fields__[i]
    model.__fields__ = keep_fields

    @app.post(f"/{func.__name__}/")
    def new_func(params: model):
        print(params)
        return params
    return new_func


@app.get("/jaseci/actions/")
def action_list():
    return remote_actions
