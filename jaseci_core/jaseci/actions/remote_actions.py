"""
General action base class with automation for hot loading
"""
from jaseci.utils.utils import logger
from fastapi import FastAPI
from pydantic import validate_arguments
from time import time
import inspect

remote_actions = {}
ACTIONS_SPEC_LOC = "/jaseci_actions_spec/"

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
    remote_actions[f"{'.'.join(act_group+[func.__name__])}"] = \
        func.__code__.co_varnames

    # Need to get pydatic model for func signature for fastAPI post
    model = validate_arguments(func).model

    keep_fields = {}
    for i in model.__fields__.keys():
        if i in func.__code__.co_varnames:
            keep_fields[i] = model.__fields__[i]
    model.__fields__ = keep_fields

    @app.post(f"/{func.__name__}/")
    def new_func(params: model):
        pl_peek = str(dict(params.__dict__))[:256]
        logger.info(str(
            f'Incoming call to {func.__name__} with {pl_peek}'))
        start_time = time()
        TY = '\033[33m'
        TG = '\033[32m'
        EC = '\033[m'  # noqa
        ret = validate_arguments(func)(**(params.__dict__))
        tot_time = time()-start_time
        logger.info(str(
            f'API call to {TG}{func.__name__}{EC}'
            f' completed in {TY}{tot_time:.3f} seconds{EC}'))
        return ret
    return new_func


@app.get(ACTIONS_SPEC_LOC)
def action_list():
    return remote_actions
